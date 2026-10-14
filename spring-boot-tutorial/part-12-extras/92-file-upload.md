# Chapter 92 – Uploading files

[⬅ Previous chapter](91-scheduling.md) | [Table of Contents](../README.md) | [Next chapter ➡](93-swagger.md)

---

## 🎯 Goal

Every student card needs a **photo**! 📸 But so far, our API only takes **JSON** — text. A photo is a **file** full of bytes. How do we send it?

Today you'll build **photo upload and download** for students.

At the end of this chapter you will know:

- What **multipart** requests are, and how to send a file with **curl** 📨
- How to receive a file with **`MultipartFile`**
- How to **check** a file: is it empty? is it really a picture? is it too big? 🔍
- How to **save** it on the disk — **safely** 🔒
- How to send a file **back** to the client 📤

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Upload** | Send a file **from** your computer **to** a server. ⬆️ |
| **Download** | Get a file **from** a server **to** your computer. ⬇️ |
| **Multipart** | A kind of request with **several parts**: for example, a file **and** some text. 📦📦 |
| **`MultipartFile`** | Spring's object for **one uploaded file**: its name, its type, its bytes. |
| **Content type** (MIME type) | The **kind** of a file: `image/jpeg` (a photo), `image/png`, `application/pdf`... |
| **Byte** | The smallest piece of data a computer stores. A photo has **millions** of them. |
| **Path** | Where a file lives on the disk, like `uploads/students/1.jpg`. 📁 |
| **413 Payload Too Large** | "Your file is too big for me!" 🐘 |

---

## 📖 Story: The school photographer 📸

Once a year, the school photographer comes. Every student gets a photo for their **student card**. The secretary puts each photo into a **folder** 📁 with the student's **number** on it — not the name the photographer wrote on the back, because that could be anything ("SuperCoolPhoto_FINAL_2.jpg" 😅).

And the secretary **checks** every photo:

- Is there really a **photo** in the envelope? (not empty) 📭
- Is it a **photo** — not a drawing or a sandwich? 🥪
- Is it a normal **size** — not a giant poster? 🖼️

That's exactly what our upload code will do. ✅

---

## 📨 Part 1: How a file travels — multipart

A JSON request has **one** body: text. A file upload uses a **multipart** request: the body is split into **parts**, and each part can be text **or** a file:

```
 POST /api/students/1/photo
 Content-Type: multipart/form-data; boundary=----XYZ

 ------XYZ
 Content-Disposition: form-data; name="file"; filename="sara.jpg"
 Content-Type: image/jpeg

 ÿØÿà..JFIF.....(millions of bytes of the photo)....
 ------XYZ--
```

| Part | Meaning |
|---|---|
| `multipart/form-data` | "This body has **parts**." |
| `boundary=----XYZ` | The "line" that separates the parts ✂️ — like dividers in a folder. |
| `name="file"` | The name of **this** part. Our controller will ask for the part called `file`. |
| `filename="sara.jpg"` | The file's name on the **sender's** computer. |
| `Content-Type: image/jpeg` | What kind of file it is. |

You don't have to write that yourself! **curl** does it with **`-F`** ("form"):

```bash
curl -i -X POST http://localhost:8080/api/students/1/photo \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@sara.jpg"
```

| Part | Meaning |
|---|---|
| `-F "file=@sara.jpg"` | ⭐ Make a multipart request with a part called `file`, filled with the **content** of the file `sara.jpg`. The **`@`** means "read this file". |

(Put any small photo called `sara.jpg` into the folder where you run curl. In **Postman**: Body → **form-data** → key `file`, change the type from "Text" to **"File"**, and choose a photo.)

---

## ⚙️ Part 2: Settings — where and how big

Add to **`application.properties`**:

```properties
# Uploads
school.upload.dir=uploads
spring.servlet.multipart.max-file-size=2MB
spring.servlet.multipart.max-request-size=2MB
```

| Code | Meaning |
|---|---|
| `school.upload.dir=uploads` | Our **own** setting: the folder for uploaded files (inside the project folder). |
| `spring.servlet.multipart.max-file-size=2MB` | ⭐ A file may be at most **2 MB**. (The default is only 1 MB.) Bigger → refused. 🐘 |
| `spring.servlet.multipart.max-request-size=2MB` | The whole request (all parts together) may be at most 2 MB. |

⚠️ Add `uploads/` to your **`.gitignore`** — photos of real students don't belong in Git! 🔒

---

## 🗂️ Part 3: The storage service

We put all the "file work" into **one** service.

**`exception/InvalidFileException.java`**

```java
package com.example.school.exception;

public class InvalidFileException extends RuntimeException {

    public InvalidFileException(String message) {
        super(message);
    }
}
```

**`service/PhotoService.java`**

```java
package com.example.school.service;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.Set;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.example.school.exception.InvalidFileException;
import com.example.school.exception.StudentNotFoundException;
import com.example.school.repository.StudentRepository;

@Service
public class PhotoService {

    private static final Set<String> ALLOWED_TYPES = Set.of("image/jpeg", "image/png");

    private final Path photoFolder;
    private final StudentRepository studentRepository;

    public PhotoService(@Value("${school.upload.dir}") String uploadDir, StudentRepository studentRepository) {
        this.photoFolder = Path.of(uploadDir, "students");
        this.studentRepository = studentRepository;
    }

    public void savePhoto(Long studentId, MultipartFile file) {
        if (!studentRepository.existsById(studentId)) {
            throw new StudentNotFoundException(studentId);
        }
        if (file.isEmpty()) {
            throw new InvalidFileException("The file is empty");
        }
        if (!ALLOWED_TYPES.contains(file.getContentType())) {
            throw new InvalidFileException("Only JPEG and PNG photos are allowed, but this file is " + file.getContentType());
        }
        try (InputStream input = file.getInputStream()) {
            Files.createDirectories(photoFolder);
            Files.copy(input, photoFolder.resolve(studentId + ".img"), StandardCopyOption.REPLACE_EXISTING);
            Files.writeString(photoFolder.resolve(studentId + ".type"), file.getContentType());
        } catch (IOException ex) {
            throw new IllegalStateException("Could not save the photo of student " + studentId, ex);
        }
    }
}
```

Lots of new Java tools! Slowly:

| Code | Meaning |
|---|---|
| `Set.of("image/jpeg", "image/png")` | The **allowed** kinds of files. Everything else is refused. (A `Set`, Chapter 32, because we only ask "is it in there?") |
| `Path` | Java's object for "a place on the disk". `Path.of("uploads", "students")` → the folder `uploads/students`. 📁 |
| `MultipartFile file` | ⭐ The uploaded file. |
| `file.isEmpty()` | Is it **0 bytes**? 📭 |
| `file.getContentType()` | The kind of file the client **says** it is: `"image/jpeg"`. |
| `try (InputStream input = file.getInputStream())` | Open the file's bytes for reading — a **stream** (like water from a tap 🚰). The `try ( ... )` form **closes** the tap automatically at the end (Chapter 33). |
| `Files.createDirectories(photoFolder)` | Make the folder (and its parents) if it doesn't exist yet. |
| `photoFolder.resolve(studentId + ".img")` | The path **inside** the folder: `uploads/students/1.img`. |
| `Files.copy(input, path, StandardCopyOption.REPLACE_EXISTING)` | ⭐ Pour the bytes into the file. A new photo **replaces** the old one. |
| `Files.writeString(... ".type", file.getContentType())` | A tiny second file that remembers the **type** (`image/jpeg`), so we can send the photo back correctly later. |
| `catch (IOException ex)` | Disk problems (full disk, no permission...) are **checked** exceptions → we wrap it in a `RuntimeException` (so our catch-all handles it → 500, which is right: it's **our** problem). |

### 🔒 Why `1.img` and not `sara.jpg`?

**Never** use the file name from the client! It could be:

- `../../application.properties` — a sneaky name that walks **out** of the folder and overwrites **your** files! 😈 (This trick is called **path traversal**.)
- `Sara Ahmed (copy) FINAL!!!.jpg` — strange characters.
- the **same** name as another student's photo.

**We** decide the name: the student's **id**. Safe, simple, unique. ✅

---

## 🎮 Part 4: The controller — upload

Add to **`StudentController`**:

```java
@PostMapping(value = "/{id}/photo", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
@ResponseStatus(HttpStatus.NO_CONTENT)
public void uploadPhoto(@PathVariable Long id, @RequestParam("file") MultipartFile file) {
    photoService.savePhoto(id, file);
}
```

(Inject `PhotoService photoService` in the constructor. Imports: `org.springframework.http.MediaType`, `org.springframework.web.multipart.MultipartFile`.)

| Code | Meaning |
|---|---|
| `consumes = MediaType.MULTIPART_FORM_DATA_VALUE` | "This endpoint only accepts **multipart** requests." |
| `@RequestParam("file") MultipartFile file` | ⭐ "Give me the **part** called `file`." (Yes, `@RequestParam` — parts are treated like form fields.) |
| `@ResponseStatus(HttpStatus.NO_CONTENT)` | Saved → **204**, nothing to send back. |

**Security:** `POST /api/...` → teachers and admins only (Chapter 82). Students can't change photos. 👍

And the new exception in **`GlobalExceptionHandler`**:

```java
@ExceptionHandler(InvalidFileException.class)
public ProblemDetail handleInvalidFile(InvalidFileException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, ex.getMessage());
    problem.setTitle("Invalid file");
    return problem;
}
```

### 🧪 Try it

Log in as teacher (Chapter 83), then:

```bash
curl -i -X POST http://localhost:8080/api/students/1/photo \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@sara.jpg"
```

```
HTTP/1.1 204 
```

📁 Look in your project: **`uploads/students/1.img`** and **`1.type`** are there!

A text file instead of a photo (`-F "file=@notes.txt"`) → curl sends it as `text/plain`:

```
HTTP/1.1 400 
Content-Type: application/problem+json

{"detail":"Only JPEG and PNG photos are allowed, but this file is text/plain","instance":"/api/students/1/photo","status":400,"title":"Invalid file"}
```

✅ Refused!

---

## 🐘 Part 5: Too big!

Try a photo bigger than 2 MB. Spring refuses it **before** our code even runs, with a **`MaxUploadSizeExceededException`**... and our catch-all would make it a **500**. 😕 It should be **413 Payload Too Large**. Add a handler:

```java
@ExceptionHandler(MaxUploadSizeExceededException.class)
public ProblemDetail handleTooBig(MaxUploadSizeExceededException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.PAYLOAD_TOO_LARGE,
            "The file is too big. The maximum is 2 MB.");
    problem.setTitle("File too big");
    return problem;
}
```

(Import `org.springframework.web.multipart.MaxUploadSizeExceededException`.)

Now:

```
HTTP/1.1 413 
Content-Type: application/problem+json

{"detail":"The file is too big. The maximum is 2 MB.","instance":"/api/students/1/photo","status":413,"title":"File too big"}
```

🐘 → 🚫. Limits protect your server's disk **and** memory!

---

## 📤 Part 6: Download — getting the photo back

Add to **`PhotoService`**:

```java
public byte[] loadPhoto(Long studentId) {
    Path photo = photoFolder.resolve(studentId + ".img");
    if (!Files.exists(photo)) {
        throw new StudentNotFoundException(studentId);
    }
    try {
        return Files.readAllBytes(photo);
    } catch (IOException ex) {
        throw new IllegalStateException("Could not read the photo of student " + studentId, ex);
    }
}

public String loadPhotoType(Long studentId) {
    try {
        return Files.readString(photoFolder.resolve(studentId + ".type"));
    } catch (IOException ex) {
        return "application/octet-stream";
    }
}
```

| Code | Meaning |
|---|---|
| `Files.exists(photo)` | Is there a photo for this student? |
| `Files.readAllBytes(photo)` | Read the **whole** file into a `byte[]` — an array of bytes (Chapter 14). Fine for small photos. |
| `"application/octet-stream"` | The type for "just some bytes, I don't know what". A safe fallback. |

And in **`StudentController`**:

```java
@GetMapping("/{id}/photo")
public ResponseEntity<byte[]> downloadPhoto(@PathVariable Long id) {
    return ResponseEntity.ok()
            .contentType(MediaType.parseMediaType(photoService.loadPhotoType(id)))
            .body(photoService.loadPhoto(id));
}
```

| Code | Meaning |
|---|---|
| `ResponseEntity<byte[]>` | The answer's body is **bytes**, not JSON (Chapter 62). |
| `.contentType(MediaType.parseMediaType(...))` | ⭐ Tell the browser what it is: `image/jpeg` → the browser **shows** the picture. |

It's a `GET /api/...` → open to everyone. Open **http://localhost:8080/api/students/1/photo** in your browser: Sara's photo appears! 📸🎉

(Hmm — the "not found" message says "Student with id 5 was not found" even when the student exists but has no photo. Good enough for now; in the mini project you could make a `PhotoNotFoundException`. 😉)

---

## 💻 Mini project: Delete a photo 🗑️

Add **`DELETE /api/students/{id}/photo`**:

- Only **admins** (the `DELETE` rule already does that 👍).
- It deletes **both** files (`.img` and `.type`).
- No photo → **404** with the title `"Photo not found"` (make a new `PhotoNotFoundException`).
- Success → **204**.

**Hint:** `Files.deleteIfExists(path)` returns `true` if it deleted something.

<details>
<summary>Click to see the answer</summary>

**`exception/PhotoNotFoundException.java`**

```java
package com.example.school.exception;

public class PhotoNotFoundException extends RuntimeException {

    public PhotoNotFoundException(Long studentId) {
        super("Student " + studentId + " has no photo");
    }
}
```

**In `GlobalExceptionHandler`:**

```java
@ExceptionHandler(PhotoNotFoundException.class)
public ProblemDetail handlePhotoNotFound(PhotoNotFoundException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
    problem.setTitle("Photo not found");
    return problem;
}
```

**In `PhotoService`:**

```java
public void deletePhoto(Long studentId) {
    try {
        boolean deleted = Files.deleteIfExists(photoFolder.resolve(studentId + ".img"));
        Files.deleteIfExists(photoFolder.resolve(studentId + ".type"));
        if (!deleted) {
            throw new PhotoNotFoundException(studentId);
        }
    } catch (IOException ex) {
        throw new IllegalStateException("Could not delete the photo of student " + studentId, ex);
    }
}
```

**In `StudentController`:**

```java
@DeleteMapping("/{id}/photo")
@ResponseStatus(HttpStatus.NO_CONTENT)
public void deletePhoto(@PathVariable Long id) {
    photoService.deletePhoto(id);
}
```

| Code | Meaning |
|---|---|
| `Files.deleteIfExists(...)` | Delete the file if it's there; `true` = something was deleted, `false` = there was nothing. No exception for a missing file. |
| `if (!deleted) throw new PhotoNotFoundException(...)` | No photo → 404. |

(Also a good idea: use `PhotoNotFoundException` in `loadPhoto` instead of `StudentNotFoundException`.)

</details>

---

## ✋ Try it yourself

1. Upload a **PNG** photo. Then download it — what `Content-Type` does the answer have?
2. Rename a text file to `fake.jpg` and upload it with `-F "file=@fake.jpg"`. Is it accepted? Why? Is that a problem?
3. Upload a photo for student **999**. What happens?

<details>
<summary>Click to see the answers</summary>

1. `Content-Type: image/png` — because we saved the type in `1.type`.
2. Probably **yes**! curl guesses the type from the **file name** (`.jpg` → `image/jpeg`), and we trust what the client says. 😬 A real app would also look at the **first bytes** of the file (every JPEG starts with the same "magic" bytes `FF D8 FF`) or use an image library to check it's really a picture.
3. **404** "Student with id 999 was not found" — our first check in `savePhoto`. No orphan photos! 👍

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Using the client's file name

Path traversal 😈, duplicates, strange characters. **Fix:** Choose the name **yourself** (the id, or a random UUID).

### Mistake 2: No size limit — or the default 1 MB

Phone photos are often 3–5 MB → refused with the default. And with **no** limit, someone could fill your disk. **Fix:** Set `spring.servlet.multipart.max-file-size` to what you really need, and handle `MaxUploadSizeExceededException` → 413.

### Mistake 3: Trusting the content type

The client **says** `image/jpeg` — it could lie. **Fix:** For important uploads, check the file's real content too (Try it 2).

### Mistake 4: Forgetting `-F` and the part name

`curl -d @sara.jpg ...` sends the bytes as a normal body, not as a multipart part → Spring can't find the `file` part (400 `Required part 'file' is not present` or 415). **Fix:** `-F "file=@sara.jpg"` — the name before `=` must match `@RequestParam("file")`.

### Mistake 5: Uploads in Git

**Fix:** `uploads/` into `.gitignore`.

---

## ✅ Summary

- Files travel in **multipart** requests 📦: curl `-F "file=@photo.jpg"`, Postman "form-data".
- Receive them with **`@RequestParam("file") MultipartFile file`** and `consumes = MediaType.MULTIPART_FORM_DATA_VALUE`.
- **Check** every file: empty? allowed type? size limit (`spring.servlet.multipart.max-file-size`)? Too big → handle `MaxUploadSizeExceededException` → **413**.
- **Save** with `Files.copy(...)` under a name **you** choose — never the client's name 🔒.
- **Send back** with `ResponseEntity<byte[]>` and the right `contentType`.
- Keep `uploads/` out of Git.

---

## ❓ Quiz

1. What is a multipart request?
2. What does the `@` mean in `curl -F "file=@sara.jpg"`?
3. Name three checks we do before saving a photo.
4. Why do we save the photo as `1.img` and not with the client's file name?
5. Which status code means "the file is too big"?
6. Why does the download answer set a `contentType`?
7. Why should `uploads/` be in `.gitignore`?

<details>
<summary>Click to see the answers</summary>

1. A request whose body is split into several parts; each part can be text or a file.
2. "Read the content of this file and send it."
3. The student exists, the file isn't empty, the type is JPEG or PNG (and the size limit, checked by Spring).
4. A client's file name could be dangerous (path traversal), strange, or the same as another file's name.
5. **413 Payload Too Large**.
6. So the browser knows what the bytes are (for example a JPEG picture) and can show them.
7. Uploaded files (like photos of real students) are private data and don't belong in the code's history.

</details>

---

[⬅ Previous chapter](91-scheduling.md) | [Table of Contents](../README.md) | [Next chapter: API documentation with Swagger ➡](93-swagger.md)
