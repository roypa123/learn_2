# Chapter 61 – Changing and deleting: PUT, PATCH and DELETE

[⬅ Previous chapter](60-post-request-body.md) | [Table of Contents](../README.md) | [Next chapter ➡](62-response-entity.md)

---

## 🎯 Goal

Our API can **create** and **read** students. Now let's finish **CRUD**: **update** ✏️ and **delete** 🗑️!

At the end of this chapter you will know:

- How to **replace** a student with **`@PutMapping`**
- How to **change only some fields** with **`@PatchMapping`**
- The real difference between **PUT** and **PATCH** (we'll **see** it go wrong! 😱)
- How to **delete** a student with **`@DeleteMapping`**
- How to combine **`@PathVariable`** and **`@RequestBody`** in one method
- How to handle "student not found" for all of them

> 🎉 At the end of this chapter, your API has **all** the endpoints from the Chapter 46 design!

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Update** | Change something that **already exists**. |
| **PUT** | "**Replace** the whole thing with this new version." |
| **PATCH** | "Change **only** these fields. Keep the rest." 🩹 |
| **DELETE** | "Remove this thing." 🗑️ |
| **Idempotent** | Doing it **twice** gives the **same result** as doing it once. (Chapter 44) |
| **Partial update** | An update that changes only **part** of an object (that's what PATCH does). |

---

## 📖 Story: Changing the student card 🪪

Tom gets a new email address. The secretary has two ways to update his card:

**Way 1 — PUT: a brand-new card** 🆕
She **throws away** the old card and writes a **completely new** one. She must write **everything** again: name, email, age. If she forgets to write the age... the new card has **no age**! 😱

**Way 2 — PATCH: a sticker** 🩹
She keeps the old card and puts a small **sticker** over the email: "tom.brown@school.com". Everything else stays the same. 😊

And when **Lina** moves to another city, the secretary **removes** her card from the cabinet. That's **DELETE**. 🗑️

---

## 🆕 Part 1: PUT — replace a student

**PUT** sends the **whole** student. The path says **which** student, and the body says the **new** version.

```http
PUT /api/students/2 HTTP/1.1
Content-Type: application/json

{"name":"Tom Brown","email":"tom.brown@school.com","age":14}
```

Add this to `StudentController`:

```java
@PutMapping("/{id}")
public Student replace(@PathVariable Long id, @RequestBody Student changed) {
    for (int i = 0; i < students.size(); i++) {
        if (students.get(i).id().equals(id)) {
            Student updated = new Student(id, changed.name(), changed.email(), changed.age());
            students.set(i, updated);
            return updated;
        }
    }
    throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Student with id " + id + " was not found");
}
```

(Import: `org.springframework.web.bind.annotation.PutMapping`.)

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@PutMapping("/{id}")` | ⭐ "Call this method for **PUT** `/api/students/{id}`." |
| `@PathVariable Long id` | **Which** student — from the path (Chapter 58). |
| `@RequestBody Student changed` | The **new version** — from the JSON body (Chapter 60). Both helpers in **one** method! 🤝 |
| `for (int i = 0; i < students.size(); i++)` | A loop with an **index** (Chapter 12), because we need the **position** to replace the student. |
| `students.get(i).id().equals(id)` | Is the student at position `i` the one we want? |
| `new Student(id, changed.name(), ...)` | The new version. ⚠️ The id comes from the **path**, not from the body — the client can't change ids! 🛡️ |
| `students.set(i, updated);` | ⭐ **Replace** the old student at position `i` with the new one (Chapter 30). |
| `return updated;` | Send back the new version. |
| `throw new ResponseStatusException(HttpStatus.NOT_FOUND, ...)` | The loop finished without finding anyone → **404** (Chapter 58). |

### ✅ Test it

```bash
curl -i -X PUT http://localhost:8080/api/students/2 \
  -H "Content-Type: application/json" \
  -d '{"name":"Tom Brown","email":"tom.brown@school.com","age":14}'
```

Real answer:

```
HTTP/1.1 200 
Content-Type: application/json

{"id":2,"name":"Tom Brown","email":"tom.brown@school.com","age":14}
```

✅ Tom has a new email **and** is 14 now. And `PUT /api/students/99` → **404**.

(In Postman: choose **PUT**, URL `http://localhost:8080/api/students/2`, Body → raw → JSON. Same as POST — Chapter 60.)

---

## 😱 Part 2: The PUT trap — forgetting a field

Now let's be a **lazy** client. We only want to change Tom's **name** to "Tommy", so we send only the name and age:

```bash
curl -i -X PUT http://localhost:8080/api/students/2 \
  -H "Content-Type: application/json" \
  -d '{"name":"Tommy","age":14}'
```

Real answer:

```json
{"id":2,"name":"Tommy","email":null,"age":14}
```

😱 **Tom's email is GONE!** `"email": null`!

Why? Because **PUT means "replace everything"**. We didn't send an email, so Jackson made it `null` (Chapter 60, Part 5), and we **replaced** the whole student with that. The new card has **no email**. 🪪❌

**PUT rule:** The client must **always** send the **complete** object — every field — even the ones that don't change. (In Chapter 65, **validation** will reject a PUT with missing fields. ✅)

---

## 🩹 Part 3: PATCH — change only some fields

For "just change the email", REST has **PATCH**: the client sends **only** the fields that change. Everything else stays the same. 🩹

```http
PATCH /api/students/1 HTTP/1.1
Content-Type: application/json

{"email":"sara.ahmed@school.com"}
```

### Step 1: A record for the "sticker"

The fields must be able to be **missing** → `null`. So `age` must be an **`Integer`**, not an `int` (an `int` can't be `null` — and a missing `int` even gives **400** — Chapter 60!).

Create **`StudentPatch.java`**:

```java
package com.example.school;

public record StudentPatch(String name, String email, Integer age) {
}
```

| Field | Meaning |
|---|---|
| `String name` | The new name — or `null` = "don't change the name". |
| `String email` | The new email — or `null` = "don't change". |
| `Integer age` | ⭐ `Integer`, so it can be `null` = "don't change the age". |

### Step 2: The PATCH method

```java
@PatchMapping("/{id}")
public Student update(@PathVariable Long id, @RequestBody StudentPatch patch) {
    Student old = getById(id);
    Student updated = new Student(
            id,
            patch.name() != null ? patch.name() : old.name(),
            patch.email() != null ? patch.email() : old.email(),
            patch.age() != null ? patch.age() : old.age());
    students.set(students.indexOf(old), updated);
    return updated;
}
```

(Import: `org.springframework.web.bind.annotation.PatchMapping`.)

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@PatchMapping("/{id}")` | ⭐ "Call this method for **PATCH** `/api/students/{id}`." |
| `@RequestBody StudentPatch patch` | The "sticker" — only some fields filled in. |
| `Student old = getById(id);` | Find the current student. If it doesn't exist, `getById` throws the **404** (Chapter 58). ♻️ |
| `patch.name() != null ? patch.name() : old.name()` | ⭐ The **ternary operator** (Chapter 10): "If the patch **has** a name, use it. **Otherwise**, keep the old name." |
| (the same for `email` and `age`) | Each field: new value **or** old value. |
| `students.indexOf(old)` | Where is the old student in the list? (`indexOf` uses `equals` — records have it for free! Chapter 30.) |
| `students.set(..., updated)` | Replace it at that position. |

### ✅ Test it

```bash
curl -i -X PATCH http://localhost:8080/api/students/1 \
  -H "Content-Type: application/json" \
  -d '{"email":"sara.ahmed@school.com"}'
```

Real answer:

```json
{"id":1,"name":"Sara Ahmed","email":"sara.ahmed@school.com","age":12}
```

✅ New email — **and** name and age are still there! 🩹 Now a birthday 🎂:

```bash
-d '{"age":13}'
```

```json
{"id":1,"name":"Sara Ahmed","email":"sara.ahmed@school.com","age":13}
```

Only the age changed. The email from the last PATCH is still there. 🎉

### 🆚 PUT vs PATCH

| | PUT 🆕 | PATCH 🩹 |
|---|---|---|
| Means | "Replace **everything**" | "Change **only these** fields" |
| Client sends | the **whole** object | only the **changed** fields |
| A missing field becomes... | `null` / empty ⚠️ | stays the **same** ✅ |
| Our body type | `Student` | `StudentPatch` (all fields can be `null`) |
| Example | Editing a whole profile form | Changing only your profile picture |

> 💡 **Which should I offer?** Many APIs offer **both**. If you offer only one, PUT is simpler to build, but PATCH is nicer for clients. 😊

---

## 🗑️ Part 4: DELETE — remove a student

```http
DELETE /api/students/3 HTTP/1.1
```

No body — the path says everything. Add:

```java
@DeleteMapping("/{id}")
public void delete(@PathVariable Long id) {
    boolean removed = students.removeIf(student -> student.id().equals(id));
    if (!removed) {
        throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Student with id " + id + " was not found");
    }
}
```

(Import: `org.springframework.web.bind.annotation.DeleteMapping`.)

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@DeleteMapping("/{id}")` | ⭐ "Call this method for **DELETE** `/api/students/{id}`." |
| `public void delete(...)` | `void` = we return **nothing**. There's nothing to show after deleting! 🤷 |
| `students.removeIf(student -> student.id().equals(id))` | ⭐ "Remove every student whose id matches." (Chapter 30.) It returns **`true`** if it removed something, **`false`** if not. |
| `if (!removed)` | Nothing was removed → the student didn't exist... |
| `throw ... NOT_FOUND` | → **404**. |

### ✅ Test it

```bash
curl -i -X DELETE http://localhost:8080/api/students/3
```

Real answer:

```
HTTP/1.1 200 
Content-Length: 0
```

**200** with an **empty** body. Lina is gone. 👋 Check: `GET /api/students` doesn't show her anymore.

Now delete her **again**:

```
HTTP/1.1 404 
{"timestamp":"...","status":404,"error":"Not Found","path":"/api/students/3"}
```

**404** — she's already gone. ✅

> 🤔 **200 with nothing?** REST says the best answer for a successful DELETE is **204 No Content** — "done, and there's nothing to show" (Chapter 46). We'll do that in **Chapter 62**. 😉

### 🔁 Is DELETE idempotent?

Remember **idempotent** from Chapter 44? "Doing it twice = the same **result** as once." 🔁

- First DELETE: Lina is removed.
- Second DELETE: Lina is... still removed. The **data** is the same after 1 or 2 calls. ✅

The **status** is different (200, then 404), but the **result** (no Lina) is the same. So DELETE **is** idempotent. PUT is idempotent too (sending the same full student twice = same data). POST is **not** — two POSTs make **two** students! 👯

---

## 🗺️ Part 5: The complete Student API

Look what you built! 🏆 Every endpoint from the Chapter 46 design:

| Method | Path | Method in Java | What it does |
|---|---|---|---|
| `GET` | `/api/students` | `getAll(minAge, name, sort)` | List, filter, sort |
| `GET` | `/api/students/{id}` | `getById(id)` | One student, or 404 |
| `GET` | `/api/students/count` | `count()` | How many |
| `GET` | `/api/students/search?email=` | `findByEmail(email)` | Search by email |
| `POST` | `/api/students` | `create(newStudent)` | Create, server gives the id |
| `PUT` | `/api/students/{id}` | `replace(id, changed)` | Replace everything |
| `PATCH` | `/api/students/{id}` | `update(id, patch)` | Change some fields |
| `DELETE` | `/api/students/{id}` | `delete(id)` | Remove |

And `curl -i -X OPTIONS http://localhost:8080/api/students/1` now shows **all** the methods for one student: GET, PUT, PATCH, DELETE (plus HEAD and OPTIONS). 🤓

### 📄 The whole controller

Here's the complete `StudentController` after Chapters 57–61:

```java
package com.example.school;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Stream;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api/students")
public class StudentController {

    private final List<Student> students = new ArrayList<>(List.of(
            new Student(1L, "Sara Ahmed", "sara@school.com", 12),
            new Student(2L, "Tom Brown", "tom@school.com", 13),
            new Student(3L, "Lina Haddad", "lina@school.com", 11)));

    private long nextId = 4;

    @GetMapping
    public List<Student> getAll(@RequestParam(required = false) Integer minAge,
                                @RequestParam(required = false) String name,
                                @RequestParam(defaultValue = "id") String sort) {
        Stream<Student> result = students.stream();

        if (minAge != null) {
            result = result.filter(student -> student.age() >= minAge);
        }
        if (name != null) {
            result = result.filter(student -> student.name().toLowerCase().contains(name.toLowerCase()));
        }

        Comparator<Student> order = switch (sort) {
            case "name" -> Comparator.comparing(Student::name);
            case "age" -> Comparator.comparingInt(Student::age);
            default -> Comparator.comparing(Student::id);
        };
        return result.sorted(order).toList();
    }

    @GetMapping("/count")
    public int count() {
        return students.size();
    }

    @GetMapping("/names")
    public List<String> names() {
        return students.stream()
                .map(Student::name)
                .toList();
    }

    @GetMapping("/{id}")
    public Student getById(@PathVariable Long id) {
        return students.stream()
                .filter(student -> student.id().equals(id))
                .findFirst()
                .orElseThrow(() -> new ResponseStatusException(
                        HttpStatus.NOT_FOUND, "Student with id " + id + " was not found"));
    }

    @GetMapping("/{id}/age-in/{years}")
    public String ageIn(@PathVariable Long id, @PathVariable int years) {
        Student student = getById(id);
        return "In " + years + " years, " + student.name() + " will be " + (student.age() + years) + ".";
    }

    @GetMapping("/search")
    public Student findByEmail(@RequestParam String email) {
        return students.stream()
                .filter(student -> student.email().equalsIgnoreCase(email))
                .findFirst()
                .orElseThrow(() -> new ResponseStatusException(
                        HttpStatus.NOT_FOUND, "No student with email " + email));
    }

    @GetMapping("/by-ids")
    public List<Student> findByIds(@RequestParam List<Long> ids) {
        return students.stream()
                .filter(student -> ids.contains(student.id()))
                .toList();
    }

    @PostMapping
    public Student create(@RequestBody Student newStudent) {
        Student student = new Student(nextId, newStudent.name(), newStudent.email(), newStudent.age());
        nextId++;
        students.add(student);
        return student;
    }

    @PutMapping("/{id}")
    public Student replace(@PathVariable Long id, @RequestBody Student changed) {
        for (int i = 0; i < students.size(); i++) {
            if (students.get(i).id().equals(id)) {
                Student updated = new Student(id, changed.name(), changed.email(), changed.age());
                students.set(i, updated);
                return updated;
            }
        }
        throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Student with id " + id + " was not found");
    }

    @PatchMapping("/{id}")
    public Student update(@PathVariable Long id, @RequestBody StudentPatch patch) {
        Student old = getById(id);
        Student updated = new Student(
                id,
                patch.name() != null ? patch.name() : old.name(),
                patch.email() != null ? patch.email() : old.email(),
                patch.age() != null ? patch.age() : old.age());
        students.set(students.indexOf(old), updated);
        return updated;
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        boolean removed = students.removeIf(student -> student.id().equals(id));
        if (!removed) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Student with id " + id + " was not found");
        }
    }
}
```

It's getting **long**, isn't it? 😅 About 130 lines, and the controller does **everything**: HTTP, searching, storing, rules... In **Chapter 63**, we'll split it into **layers**, so each class has **one** job. 🧹

---

## 💻 Mini project: The Book API, part 5 📚

Add to your `BookController`:

1. **`PUT /api/books/{id}`** → replace a book (404 if not found).
2. **`PATCH /api/books/{id}`** → change some fields. Create a record `BookPatch(String title, String author, Integer year)`.
3. **`DELETE /api/books/{id}`** → remove a book (404 if not found).

Test: change the year of "Matilda" to **1990** with PATCH, then delete "The Hobbit", then list all books.

<details>
<summary>Click to see the answer</summary>

**`BookPatch.java`**

```java
package com.example.school;

public record BookPatch(String title, String author, Integer year) {
}
```

In `BookController`:

```java
@PutMapping("/{id}")
public Book replace(@PathVariable Long id, @RequestBody Book changed) {
    for (int i = 0; i < books.size(); i++) {
        if (books.get(i).id().equals(id)) {
            Book updated = new Book(id, changed.title(), changed.author(), changed.year());
            books.set(i, updated);
            return updated;
        }
    }
    throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Book with id " + id + " was not found");
}

@PatchMapping("/{id}")
public Book update(@PathVariable Long id, @RequestBody BookPatch patch) {
    Book old = getById(id);
    Book updated = new Book(
            id,
            patch.title() != null ? patch.title() : old.title(),
            patch.author() != null ? patch.author() : old.author(),
            patch.year() != null ? patch.year() : old.year());
    books.set(books.indexOf(old), updated);
    return updated;
}

@DeleteMapping("/{id}")
public void delete(@PathVariable Long id) {
    boolean removed = books.removeIf(book -> book.id().equals(id));
    if (!removed) {
        throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Book with id " + id + " was not found");
    }
}
```

Test:

- `PATCH /api/books/1` with `{"year":1990}` → `{"id":1,"title":"Matilda","author":"Roald Dahl","year":1990}`
- `DELETE /api/books/2` → **200**, empty
- `GET /api/books` → Matilda (1990) and Charlotte's Web. 🎉

</details>

---

## ✋ Try it yourself

**Task 1:** PATCH Tom (id 2) with an **empty** JSON object: `{}`. What happens? Why?

<details>
<summary>Click to see the answer</summary>

Nothing changes! You get Tom back exactly as he was. All fields in the patch are `null`, so the ternaries keep **all** the old values. (Some APIs would answer 400 here — "you didn't change anything" — but 200 is also fine.)

</details>

**Task 2:** Try `PUT /api/students/1` with this body: `{"id":77,"name":"Sara Ahmed","email":"sara@school.com","age":12}`. What's Sara's id afterwards? Why?

<details>
<summary>Click to see the answer</summary>

Still **1**! Our code uses the id from the **path** (`new Student(id, ...)`), and ignores the id in the body. The client can't change ids. 🛡️

</details>

**Task 3:** Which of these are idempotent? a) `GET /api/students` b) `POST /api/students` c) `PUT /api/students/1` d) `DELETE /api/students/1` e) `PATCH /api/students/1` with `{"age":13}`

<details>
<summary>Click to see the answer</summary>

a) ✅ yes b) ❌ no — every POST creates a **new** student c) ✅ yes d) ✅ yes e) ✅ yes for **this** patch — setting the age to 13 twice gives the same result. (A patch like "add 1 to the age" would **not** be idempotent. That's why HTTP doesn't promise that PATCH is idempotent — it depends on what the patch does.)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: PUT without all fields

Fields you don't send become `null` (or **400** for a missing `int`). **Fix:** With PUT, always send the **whole** object. Or use PATCH. (And add validation — Chapter 65.)

### Mistake 2: Using `int` in the patch record

```java
public record StudentPatch(String name, String email, int age)   // ❌
```

Then every PATCH **without** `age` fails with **400** ("Cannot map `null` into type `int`"). **Fix:** `Integer age`.

### Mistake 3: Using the id from the body

```java
new Student(changed.id(), ...)   // ❌
```

The client could send a different id, and you'd create a **mess** (two students with the same id, or a student "moving" to another number). **Fix:** Use the id from the **path**.

### Mistake 4: Removing while looping

```java
for (Student student : students) {
    if (student.id().equals(id)) {
        students.remove(student);    // 💥 ConcurrentModificationException
    }
}
```

You can't remove from a list while a for-each loop walks through it (Chapter 30). **Fix:** `removeIf(...)`. ✅

### Mistake 5: Forgetting `@PathVariable` or `@RequestBody`

Both are needed in PUT and PATCH: one for **which** student, one for the **new data**. Forgetting either one gives strange `null`s. 🤔

---

## ✅ Summary

- **PUT** `/{id}` = **replace** the whole object. `@PathVariable` (which) + `@RequestBody` (the new version). Missing fields become `null`! ⚠️
- **PATCH** `/{id}` = change **only** the sent fields. Use a patch record where **every** field can be `null` (`Integer`, not `int`), and `new != null ? new : old` for each field. 🩹
- **DELETE** `/{id}` = remove. `removeIf(...)` returns `true`/`false` → 404 if nothing was removed. 🗑️
- Always take the id from the **path**, never from the body. 🛡️
- **Idempotent:** GET, PUT, DELETE ✅ — POST ❌.
- Your API now has **every** CRUD endpoint! But the controller is big, and some status codes aren't perfect yet (200 instead of 201/204). Next: **`ResponseEntity`**! 🚀

---

## ❓ Quiz

1. What's the difference between PUT and PATCH?
2. You send `PUT /api/students/2` with `{"name":"Tommy","age":14}`. What happens to Tom's email?
3. Why does the patch record use `Integer age` and not `int age`?
4. What does `patch.name() != null ? patch.name() : old.name()` mean in simple words?
5. What does `removeIf` return? How do we use it?
6. Why do we take the id from the path and not from the body?
7. Is DELETE idempotent? Is POST?
8. What status does our DELETE return now? What would be better?

<details>
<summary>Click to see the answers</summary>

1. PUT replaces the **whole** object. PATCH changes **only** the fields that are sent.
2. It becomes `null` — PUT replaces everything, and the email wasn't sent.
3. So it can be `null` ("don't change"). An `int` can't be `null`, and a missing `int` even causes a 400.
4. "If the patch has a new name, use it. Otherwise, keep the old name."
5. `true` if something was removed, `false` if not. If it's `false`, we answer 404.
6. So the client can't change ids or create a mess. The path says which student — that's the truth.
7. DELETE: yes (twice = same result: it's gone). POST: no (twice = two new students).
8. **200** with an empty body. **204 No Content** would be better (Chapter 62).

</details>

---

[⬅ Previous chapter](60-post-request-body.md) | [Table of Contents](../README.md) | [Next chapter: ResponseEntity and status codes ➡](62-response-entity.md)
