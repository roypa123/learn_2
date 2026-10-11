# Chapter 64 – DTOs: safe boxes for data

[⬅ Previous chapter](63-layers.md) | [Table of Contents](../README.md) | [Next chapter ➡](65-validation.md)

---

## 🎯 Goal

Right now, our API **sends** and **receives** the `Student` model directly. That seems easy... but it's **dangerous**! ⚠️ Today you'll see **why** — with real examples — and fix it with **DTOs**.

At the end of this chapter you will know:

- What can go wrong when an API uses its **model** classes directly 😱
- What a **DTO** (Data Transfer Object) is
- The difference between a **request DTO** (data coming **in**) and a **response DTO** (data going **out**)
- How to **convert** between models and DTOs
- How DTOs **protect** private data and make your API **stable** 🛡️

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **DTO** | **D**ata **T**ransfer **O**bject: a small object made **only** to carry data **in or out** of your API. 📦 |
| **Model** (or **entity**) | The class your app uses **inside**: `Student`, with **all** its fields. |
| **Request DTO** | What the client may **send** to you: `StudentRequest`. 📥 |
| **Response DTO** | What you **send back** to the client: `StudentResponse`. 📤 |
| **Mapping** / **converting** | Copying data from one kind of object to another: `Student` → `StudentResponse`. |
| **Expose** | To **show** something to the outside world. (Exposing private data = bad! 🙈) |
| **Static factory method** | A `static` method that **creates** an object: `StudentResponse.from(student)`. |

---

## 📖 Story: The teacher's notebook and the report card 📓📄

The teacher has a **notebook** 📓 about every student. It has **everything**:

```
📓 Sara Ahmed — age 12 — sara@school.com
   Joined: 1 Sept 2026, 8:00
   Teacher's note: "Very good at math" 🤫
```

At the end of the year, parents get a **report card** 📄. Does the school photocopy the **notebook** and send it home? 😱 **No!** The notebook has private notes. The school makes a **special** report card, with only the things parents **should** see.

And when parents want to **change** something (like a new email), they fill out a **special form** 📝 — they can't write directly in the teacher's notebook!

| School | API |
|---|---|
| The teacher's notebook 📓 | The **model** `Student` (everything, inside the app) |
| The report card 📄 | The **response DTO** `StudentResponse` (only what clients may **see**) |
| The change form 📝 | The **request DTO** `StudentRequest` (only what clients may **send**) |

---

## 😱 Part 1: The problem — let's see it happen!

Let's make our model more **realistic**. A real school stores more about each student:

```java
package com.example.school.model;

import java.time.LocalDateTime;

public record Student(Long id, String name, String email, int age,
                      String teacherNote, LocalDateTime createdAt) {
}
```

| New field | Meaning |
|---|---|
| `String teacherNote` | A **private** note from the teacher. 🤫 Only for the school! |
| `LocalDateTime createdAt` | When the student was added (Chapter 39). The **server** sets it. |

The repository gets notes and dates for our 3 students:

```java
public StudentRepository() {
    save(new Student(null, "Sara Ahmed", "sara@school.com", 12,
            "Very good at math", LocalDateTime.of(2026, 9, 1, 8, 0)));
    save(new Student(null, "Tom Brown", "tom@school.com", 13,
            "Talks a lot in class", LocalDateTime.of(2026, 9, 1, 8, 5)));
    save(new Student(null, "Lina Haddad", "lina@school.com", 11,
            "Needs help with reading", LocalDateTime.of(2026, 9, 2, 9, 30)));
}
```

(And `save` copies the two new fields: `new Student(id, student.name(), student.email(), student.age(), student.teacherNote(), student.createdAt())`.)

### 🙈 Problem 1: Private data leaks out

If the controller still returns the **model**, we tested what a client sees for `GET /api/students/3`:

```json
{"id":3,"name":"Lina Haddad","email":"lina@school.com","age":11,"teacherNote":"Needs help with reading","createdAt":"2026-09-02T09:30:00"}
```

😱😱😱 **The teacher's private note is on the internet!** Anybody using the API — other students, other parents, anybody — can read "Needs help with reading". That's a **privacy disaster**. 🚨

Jackson sends **every** field of the record. It doesn't know which ones are secret. 🤷

### 😈 Problem 2: Clients can set things they shouldn't

If `create` takes a `Student` and saves its fields, a sneaky client can send:

```json
{"id":99,"name":"Max Power","email":"max@school.com","age":12,
 "teacherNote":"Best student ever!","createdAt":"2000-01-01T00:00:00"}
```

And we tested what happens if the code trusts these fields:

```json
{"id":4,"name":"Max Power","email":"max@school.com","age":12,"teacherNote":"Best student ever!","createdAt":"2000-01-01T00:00:00"}
```

😈 Max wrote his **own** teacher's note ("Best student ever!") and pretended he joined in the year **2000**! (Our code still ignored the `id`, at least. 😅)

### 🧱 Problem 3: The API is glued to the model

If you **rename** a field in the model (say `email` → `emailAddress`), the JSON **changes** too. Every app that uses your API **breaks**! 💥 And in Part 9, the model will get **database** details... which clients should never see.

### 🧩 The cause of all three problems

**One** class (`Student`) is doing **three** jobs:

1. Being the data **inside** the app.
2. Being what clients **receive**.
3. Being what clients **send**.

These three jobs need **different** fields! 🧩

---

## 📦 Part 2: The solution — DTOs

A **DTO** is a simple object made **only** for carrying data **across the border** of your API. 🛂 We make **separate** DTOs for each direction:

```
                     🛂 the border of your API
                             │
 Client ── StudentRequest ──►│──► Service ──► Student (model) ──► Repository
         {name,email,age}    │       │          (all fields)
                             │       │
 Client ◄─ StudentResponse ──│◄──────┘
         {id,name,email,age} │
```

| Class | Fields | Why |
|---|---|---|
| `StudentRequest` 📥 | `name`, `email`, `age` | Only what a client **may** send. No `id`, no `teacherNote`, no `createdAt`! |
| `StudentPatchRequest` 🩹 | `name`, `email`, `age` (all may be `null`) | For PATCH (Chapter 61). |
| `StudentResponse` 📤 | `id`, `name`, `email`, `age` | Only what a client **may** see. No secrets! |
| `Student` (model) 📓 | everything | Stays **inside** the app. |

---

## 💻 Part 3: The DTO classes

Create a new package **`dto`** (inside `com.example.school`, of course!).

**`dto/StudentRequest.java`**

```java
package com.example.school.dto;

public record StudentRequest(String name, String email, Integer age) {
}
```

**`dto/StudentPatchRequest.java`** (this replaces `model/StudentPatch` — delete the old one)

```java
package com.example.school.dto;

public record StudentPatchRequest(String name, String email, Integer age) {
}
```

**`dto/StudentResponse.java`**

```java
package com.example.school.dto;

import com.example.school.model.Student;

public record StudentResponse(Long id, String name, String email, int age) {

    public static StudentResponse from(Student student) {
        return new StudentResponse(student.id(), student.name(), student.email(), student.age());
    }
}
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `record StudentRequest(String name, String email, Integer age)` | ⭐ The **form** 📝. There's **no `id`**, **no `teacherNote`**, **no `createdAt`** — so a client **can't** send them. Even if they try, Jackson ignores unknown fields (Chapter 60)! 🛡️ |
| `Integer age` | `Integer`, not `int` — so a missing age is `null` instead of a confusing 400. In Chapter 65, **validation** will give a **clear** message for it. |
| `record StudentResponse(Long id, String name, String email, int age)` | ⭐ The **report card** 📄 — only the public fields. |
| `public static StudentResponse from(Student student)` | ⭐ A **static factory method**: "Make a report card **from** a notebook entry." `static` = call it on the class: `StudentResponse.from(sara)` (Chapter 27). |
| `new StudentResponse(student.id(), ...)` | Copy only the **allowed** fields. The note and the date stay behind. 🤫 |

> 💡 **Why records?** DTOs are **just data** — no logic, no changes. That's exactly what records are made for (Chapter 29). One line per DTO! ✨

---

## 👨‍🍳 Part 4: The service speaks DTO

The service is the **translator** 🗣️: it takes **request DTOs**, works with **models**, and gives back **response DTOs**.

**`service/StudentService.java`**

```java
package com.example.school.service;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.stereotype.Service;

import com.example.school.dto.StudentPatchRequest;
import com.example.school.dto.StudentRequest;
import com.example.school.dto.StudentResponse;
import com.example.school.exception.EmailAlreadyUsedException;
import com.example.school.exception.StudentNotFoundException;
import com.example.school.model.Student;
import com.example.school.repository.StudentRepository;

@Service
public class StudentService {

    private final StudentRepository studentRepository;

    public StudentService(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    public List<StudentResponse> getAll() {
        return studentRepository.findAll().stream()
                .map(StudentResponse::from)
                .toList();
    }

    public StudentResponse getById(Long id) {
        return StudentResponse.from(findStudent(id));
    }

    public StudentResponse create(StudentRequest request) {
        if (studentRepository.findByEmail(request.email()).isPresent()) {
            throw new EmailAlreadyUsedException(request.email());
        }
        Student student = new Student(null, request.name(), request.email(), request.age(),
                "", LocalDateTime.now());
        return StudentResponse.from(studentRepository.save(student));
    }

    public StudentResponse replace(Long id, StudentRequest request) {
        Student old = findStudent(id);
        Student student = new Student(id, request.name(), request.email(), request.age(),
                old.teacherNote(), old.createdAt());
        return StudentResponse.from(studentRepository.save(student));
    }

    public StudentResponse update(Long id, StudentPatchRequest patch) {
        Student old = findStudent(id);
        Student updated = new Student(
                id,
                patch.name() != null ? patch.name() : old.name(),
                patch.email() != null ? patch.email() : old.email(),
                patch.age() != null ? patch.age() : old.age(),
                old.teacherNote(),
                old.createdAt());
        return StudentResponse.from(studentRepository.save(updated));
    }

    public void delete(Long id) {
        if (!studentRepository.existsById(id)) {
            throw new StudentNotFoundException(id);
        }
        studentRepository.deleteById(id);
    }

    private Student findStudent(Long id) {
        return studentRepository.findById(id)
                .orElseThrow(() -> new StudentNotFoundException(id));
    }
}
```

### 🔍 The important lines

| Code | Meaning |
|---|---|
| `List<StudentResponse> getAll()` | Returns **report cards**, not notebook entries. |
| `.map(StudentResponse::from)` | ⭐ Turn **each** `Student` into a `StudentResponse` (Chapter 36 — `map` changes each item). |
| `StudentResponse.from(findStudent(id))` | Find the model, then convert it. |
| `create(StudentRequest request)` | Takes the **form** 📝. |
| `new Student(null, request.name(), ..., "", LocalDateTime.now())` | ⭐ **The server** sets `id` (`null` → new), `teacherNote` (empty — the teacher writes it later), and `createdAt` (**now**). The client has **no say**! 🛡️ |
| `replace(...)` | PUT: new name/email/age from the request — but the **old** note and date are **kept**. A client can't erase the teacher's note! |
| `update(...)` | PATCH: the same idea. |
| `private Student findStudent(Long id)` | A **private** helper that returns the **model** (for use inside the service). `getById` is the **public** version that returns a DTO. |

---

## 🧑‍💼 Part 5: The controller speaks DTO

The controller changes only its **types**:

```java
@GetMapping
public List<StudentResponse> getAll() {
    return studentService.getAll();
}

@GetMapping("/{id}")
public StudentResponse getById(@PathVariable Long id) {
    return studentService.getById(id);
}

@PostMapping
public ResponseEntity<StudentResponse> create(@RequestBody StudentRequest request) {
    StudentResponse created = studentService.create(request);
    URI location = URI.create("/api/students/" + created.id());
    return ResponseEntity.created(location).body(created);
}

@PutMapping("/{id}")
public StudentResponse replace(@PathVariable Long id, @RequestBody StudentRequest request) {
    return studentService.replace(id, request);
}

@PatchMapping("/{id}")
public StudentResponse update(@PathVariable Long id, @RequestBody StudentPatchRequest patch) {
    return studentService.update(id, patch);
}

@DeleteMapping("/{id}")
@ResponseStatus(HttpStatus.NO_CONTENT)
public void delete(@PathVariable Long id) {
    studentService.delete(id);
}
```

(Imports: `com.example.school.dto.StudentPatchRequest`, `...dto.StudentRequest`, `...dto.StudentResponse`. Remove the old `model` imports — IntelliJ shows unused imports in **gray**. **Ctrl + Alt + O** cleans them up!)

**Notice:** 👀 The controller doesn't import `model.Student` anymore. The **model never leaves** the service. 🔒

---

## ✅ Part 6: Test it — all problems solved!

Real answers:

### 🙈 Problem 1 solved: no more leaks

`GET /api/students/3`

```json
{"id":3,"name":"Lina Haddad","email":"lina@school.com","age":11}
```

✅ No `teacherNote`, no `createdAt`. The note is still **stored** — it's just never **sent**. 🤫

### 😈 Problem 2 solved: clients can't set secret fields

A sneaky client sends an `id` and a `teacherNote`:

```bash
curl -i -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"id":99,"name":"Omar Ali","email":"omar@school.com","age":12,"teacherNote":"Best student ever!"}'
```

```
HTTP/1.1 201 
Location: /api/students/4

{"id":4,"name":"Omar Ali","email":"omar@school.com","age":12}
```

✅ The id is **4** (the server's choice), and the fake note was **ignored** — `StudentRequest` doesn't even **have** a `teacherNote` field! The note in the model is `""` (empty), and `createdAt` is the **real** time. 🛡️

### 🧱 Problem 3 solved: the API is stable

The JSON now comes from the **DTOs**. You can rename, add, or remove fields in the **model** — the API stays the **same**, as long as `from(...)` still fills the DTO. Apps that use your API don't break. 🧱✅

---

## 🔄 Part 7: Where should the converting happen?

There are a few common styles. All are OK!

| Style | Example | Notes |
|---|---|---|
| **Static method in the DTO** ✅ (our choice) | `StudentResponse.from(student)` | Short and easy to find. |
| A separate **mapper** class | `StudentMapper.toResponse(student)` | Nice when there are **many** DTOs. |
| A **library** (like MapStruct) | generates the mapping code for you | For big projects. Not needed now. |

And **where** do you call it? In our app: in the **service**. The controller receives DTOs and returns DTOs — it never sees the model. (Some teams convert in the controller instead. Both work — just be **consistent**. 😊)

---

## 💥 Part 8: One new problem... (a cliffhanger!)

What if a client forgets the `age`?

```bash
curl -i -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"No Age","email":"noage@school.com"}'
```

```
HTTP/1.1 500 
{"timestamp":"...","status":500,"error":"Internal Server Error","path":"/api/students"}
```

😱 **500 Internal Server Error!** The console shows:

```
java.lang.NullPointerException: Cannot invoke "java.lang.Integer.intValue()" because the return value of "com.example.school.dto.StudentRequest.age()" is null
```

`request.age()` is `null` (it's an `Integer` now), and Java tried to put `null` into the model's `int age`... 💥 A **500** says "the **server** made a mistake" — but really, the **client** sent bad data! It should be **400 Bad Request**, with a **clear message** like "Age is required".

And what about an **empty** name, or `"email": "not-an-email"`, or `"age": -5`? Right now, we accept all of that! 😬

👉 **That's exactly what the next chapter is about: validation!** ✅

---

## 💻 Mini project: The Book API, part 8 📚

Give your Book API DTOs:

1. Add a **private** field to the `Book` model: `String shelf` (like `"B-12"`, where the book stands in the library). Give the 3 books shelves: Matilda `"A-1"`, The Hobbit `"F-7"`, Charlotte's Web `"C-3"`. New books get the shelf `"NEW"`.
2. `dto/BookRequest(String title, String author, Integer year)`
3. `dto/BookResponse(Long id, String title, String author, int year, int ageInYears)` — ⭐ a **computed** field! `ageInYears` = current year − `year`.
4. The service and controller use the DTOs. The `shelf` must **never** be in the JSON.

<details>
<summary>Click to see the answer</summary>

**`model/Book.java`**

```java
package com.example.school.model;

public record Book(Long id, String title, String author, int year, String shelf) {
}
```

In **`BookRepository`**, the constructor and `save` include the shelf:

```java
save(new Book(null, "Matilda", "Roald Dahl", 1988, "A-1"));
save(new Book(null, "The Hobbit", "J.R.R. Tolkien", 1937, "F-7"));
save(new Book(null, "Charlotte's Web", "E.B. White", 1952, "C-3"));
```

```java
Book saved = new Book(id, book.title(), book.author(), book.year(), book.shelf());
```

**`dto/BookRequest.java`**

```java
package com.example.school.dto;

public record BookRequest(String title, String author, Integer year) {
}
```

**`dto/BookResponse.java`**

```java
package com.example.school.dto;

import java.time.Year;

import com.example.school.model.Book;

public record BookResponse(Long id, String title, String author, int year, int ageInYears) {

    public static BookResponse from(Book book) {
        int age = Year.now().getValue() - book.year();
        return new BookResponse(book.id(), book.title(), book.author(), book.year(), age);
    }
}
```

In **`BookService`**:

```java
public List<BookResponse> getAll() {
    return bookRepository.findAll().stream()
            .map(BookResponse::from)
            .toList();
}

public BookResponse getById(Long id) {
    return BookResponse.from(findBook(id));
}

public BookResponse create(BookRequest request) {
    checkYear(request.year());
    Book book = new Book(null, request.title(), request.author(), request.year(), "NEW");
    return BookResponse.from(bookRepository.save(book));
}

private Book findBook(Long id) {
    return bookRepository.findById(id)
            .orElseThrow(() -> new BookNotFoundException(id));
}
```

(and `update` keeps `old.shelf()`). The controller uses `BookRequest` and `BookResponse`.

`GET /api/books/1` (in 2026):

```json
{"id":1,"title":"Matilda","author":"Roald Dahl","year":1988,"ageInYears":38}
```

✅ No shelf — and a useful **computed** field that the model doesn't even have! A response DTO can be **shaped** for what clients need. 🎨

</details>

---

## ✋ Try it yourself

**Task 1:** The office staff want to see **when** each student joined. Make a second response DTO **`StudentDetailsResponse`** with `id`, `name`, `email`, `age` and `createdAt` (but **not** the note), and a new endpoint `GET /api/students/{id}/details`.

<details>
<summary>Click to see the answer</summary>

```java
package com.example.school.dto;

import java.time.LocalDateTime;

import com.example.school.model.Student;

public record StudentDetailsResponse(Long id, String name, String email, int age, LocalDateTime createdAt) {

    public static StudentDetailsResponse from(Student student) {
        return new StudentDetailsResponse(student.id(), student.name(), student.email(),
                student.age(), student.createdAt());
    }
}
```

Service:

```java
public StudentDetailsResponse getDetails(Long id) {
    return StudentDetailsResponse.from(findStudent(id));
}
```

Controller:

```java
@GetMapping("/{id}/details")
public StudentDetailsResponse getDetails(@PathVariable Long id) {
    return studentService.getDetails(id);
}
```

`GET /api/students/1/details` → `{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12,"createdAt":"2026-09-01T08:00:00"}`. Different DTOs for different needs! 📦📦

</details>

**Task 2:** Why is `StudentRequest` missing an `id`, but `StudentResponse` has one?

<details>
<summary>Click to see the answer</summary>

Clients must **not** choose ids (the server does), so the request has no `id`. But clients **need** to know the id of a student (to call `/api/students/{id}` later), so the response has it.

</details>

**Task 3:** A teammate adds a field `String password` to the `Student` model (for a login, later). Do you need to change any DTO to keep the password safe?

<details>
<summary>Click to see the answer</summary>

**No!** 🎉 `StudentResponse.from(...)` only copies `id`, `name`, `email` and `age`. The password **can't** leak, because no DTO has a `password` field. That's the safety of DTOs: new model fields are **private by default**. (Without DTOs, the password would be in **every** response! 😱)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Returning the model "just this once"

"It's only one small endpoint..." → and suddenly the private note is public. 🙈 **Fix:** **Never** return the model from a controller. Always a response DTO.

### Mistake 2: One DTO for everything

Using `StudentResponse` (with `id`) as the **request** too → clients can send an id again. 😈 **Fix:** Separate DTOs for **in** (request) and **out** (response).

### Mistake 3: Forgetting to convert a list

```java
public List<StudentResponse> getAll() {
    return studentRepository.findAll();   // ❌ a List<Student>, not List<StudentResponse>
}
```

Java says: `incompatible types: List<Student> cannot be converted to List<StudentResponse>`. **Fix:** `.stream().map(StudentResponse::from).toList()`.

### Mistake 4: Putting logic in DTOs

DTOs are **boxes** 📦, not **workers**. Checking emails or saving data inside a DTO is wrong. **Fix:** Logic goes into the **service**. (A small `from(...)` method or a simple computed value like `ageInYears` is fine.)

### Mistake 5: Letting PUT erase server-only fields

```java
new Student(id, request.name(), request.email(), request.age(), null, null)   // ❌
```

The teacher's note and the date are **gone** after every PUT! **Fix:** Copy them from the **old** student: `old.teacherNote()`, `old.createdAt()`.

---

## ✅ Summary

- Using the **model** directly in the API causes 3 problems: **private data leaks** 🙈, **clients set fields** they shouldn't 😈, and the API is **glued** to the model 🧱.
- A **DTO** (Data Transfer Object) is a small object **only** for carrying data in or out. Records are perfect for DTOs.
- **Request DTO** 📥 (`StudentRequest`): only what clients may **send** — no `id`, no server fields.
- **Response DTO** 📤 (`StudentResponse`): only what clients may **see**.
- Convert with a **static factory method**: `StudentResponse.from(student)`; lists with `.map(StudentResponse::from)`.
- The **service** translates: request DTO → model → response DTO. The model **never leaves** the service. 🔒
- The **server** sets `id`, `createdAt`, and private fields. PUT/PATCH **keep** the server-only fields.
- New problem: bad data (missing age → **500**!). Next chapter: **validation**. ✅

---

## ❓ Quiz

1. What does DTO stand for?
2. Name three problems of using the model directly in the API.
3. Why doesn't `StudentRequest` have an `id` field?
4. A client sends `"teacherNote": "Best student!"` in a POST. What happens with our DTOs?
5. What does `StudentResponse.from(student)` do?
6. How do you turn a `List<Student>` into a `List<StudentResponse>`?
7. In which layer do we convert between DTOs and models?
8. Why does a missing `age` now give a 500 error? What should it give instead?

<details>
<summary>Click to see the answers</summary>

1. **D**ata **T**ransfer **O**bject.
2. Private data leaks out; clients can set fields they shouldn't (like ids or notes); the API changes whenever the model changes.
3. Because the **server** chooses ids, not the client.
4. Nothing! `StudentRequest` has no `teacherNote` field, so Jackson ignores it.
5. It creates a new `StudentResponse` with only the public fields of the student.
6. `students.stream().map(StudentResponse::from).toList()`
7. In the **service**.
8. `age` is `null` in the request, and putting `null` into the model's `int age` throws a `NullPointerException`. It should be **400 Bad Request** with a clear message — that's validation (Chapter 65).

</details>

---

[⬅ Previous chapter](63-layers.md) | [Table of Contents](../README.md) | [Next chapter: Validation: checking the data ➡](65-validation.md)
