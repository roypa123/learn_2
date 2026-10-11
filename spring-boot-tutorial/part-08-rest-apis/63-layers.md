# Chapter 63 – Layers: Controller, Service, Repository

[⬅ Previous chapter](62-response-entity.md) | [Table of Contents](../README.md) | [Next chapter ➡](64-dtos.md)

---

## 🎯 Goal

Our `StudentController` has become a **monster** 👾: about 130 lines, and it does **everything** — HTTP, searching, storing data, rules, ids... Real apps don't look like that. They're built in **layers**. 🎂

At the end of this chapter you will know:

- What **layers** are, and why every professional Spring app uses them
- The job of each layer: **Controller** 🧑‍🍳, **Service** 👨‍🍳, **Repository** 🧊
- How to organize your code into **packages**: `controller`, `service`, `repository`, `model`, `exception`
- How to write **your own exceptions** like `StudentNotFoundException`
- How to add a **business rule**: "two students can't have the same email" 📧
- How to move classes safely with IntelliJ

> 🌱 You already know the idea from **Chapter 53** (the Joke API: Controller → Service → Repository). Now we do it for **real**, with the whole Student API.

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Layer** | A **level** of your app with **one job**, like a floor in a building. 🏢 |
| **Controller layer** | Talks **HTTP**: reads requests, sends responses. Nothing else! |
| **Service layer** | The **business logic**: the rules and decisions of your app. 🧠 |
| **Repository layer** | **Stores** and **finds** data. (Today: a map in memory. Part 9: a database.) |
| **Model** | The classes for your **data**: `Student`. |
| **Business rule** | A rule of your **school**, not of HTTP: "an email can only be used once". |
| **Separation of concerns** | "Every part has **one** job, and does it well." |
| **Custom exception** | An exception class **you** write, with a clear name: `StudentNotFoundException`. |
| **Refactoring** | Changing the **structure** of code **without** changing what it does. 🧹 |

---

## 📖 Story: The restaurant 🍽️

Imagine a restaurant where **one person** does everything: takes orders, cooks, washes dishes, buys vegetables, does the money... 😵 It works when there are 3 guests. With 100 guests? **Chaos!** 🔥

A real restaurant has **roles**:

| Role | Job | Doesn't do |
|---|---|---|
| 🧑‍💼 **Waiter** | Takes orders from guests, brings the food | Doesn't cook |
| 👨‍🍳 **Chef** | Cooks; knows the **recipes** and **rules** ("no fish on Mondays") | Doesn't talk to guests |
| 🧊 **Storage room** | Keeps the ingredients; gives them when asked | Doesn't decide anything |

The waiter **asks** the chef. The chef **takes** ingredients from storage. Each one has **one** job. If the restaurant gets a **new fridge**, the waiter doesn't even notice! 😎

| Restaurant | Spring Boot |
|---|---|
| 🧑‍💼 Waiter | **`StudentController`** — HTTP |
| 👨‍🍳 Chef | **`StudentService`** — the rules |
| 🧊 Storage room | **`StudentRepository`** — the data |
| A new fridge | Part 9: a **database** instead of a map |

---

## 🏢 Part 1: The three layers

```
          🌐 HTTP request
               │
               ▼
 ┌───────────────────────────┐
 │  StudentController        │  @RestController
 │  🧑‍💼 "What does the client │  • reads path / params / body
 │      want?"               │  • calls the service
 │                           │  • builds the HTTP response
 └─────────────┬─────────────┘
               │ calls
               ▼
 ┌───────────────────────────┐
 │  StudentService           │  @Service
 │  👨‍🍳 "Is this allowed?     │  • business rules (email unique!)
 │      How do we do it?"    │  • throws exceptions (not found...)
 └─────────────┬─────────────┘
               │ calls
               ▼
 ┌───────────────────────────┐
 │  StudentRepository        │  @Repository
 │  🧊 "Here's the data."    │  • save, find, delete
 │                           │  • no rules, no HTTP
 └───────────────────────────┘
```

### The rules of layers 📏

| Rule | Why |
|---|---|
| A layer only calls the layer **directly below** it. | The controller never touches the repository. Clean and simple. |
| Calls go **down**, never **up**. | The repository never calls the service. (Remember the 🐔🥚 cycle in Chapter 53!) |
| Only the **controller** knows about HTTP. | The service doesn't know about `ResponseEntity`, status codes, or URLs. |
| Only the **repository** knows **how** data is stored. | Map today, database tomorrow — nobody else notices. |

---

## 📁 Part 2: Packages for each layer

Let's organize our classes in **packages** (Chapter 26), one per kind of class:

```
com.example.school
├── SchoolApplication.java
├── controller
│   └── StudentController.java
├── service
│   └── StudentService.java
├── repository
│   └── StudentRepository.java
├── model
│   ├── Student.java
│   └── StudentPatch.java
└── exception
    ├── StudentNotFoundException.java
    └── EmailAlreadyUsedException.java
```

All packages are **below** `com.example.school`, so Spring finds everything (Chapter 50). ✅

### 🛠️ How to create them in IntelliJ

1. Right-click **`com.example.school`** → **New → Package** → type `controller` → Enter.
2. Do the same for `service`, `repository`, `model`, `exception`.
3. **Drag** `Student.java` and `StudentPatch.java` into **`model`** (in the Project window).
4. IntelliJ shows a **Move** window → click **Refactor**. ✨ IntelliJ changes the `package` line **and** fixes every `import` in other classes for you!

> 💡 **Always move classes with IntelliJ** (drag and drop, or **F6**), not with Windows Explorer. IntelliJ updates the code; Explorer doesn't! 🧹

> 📚 **What about your Book API?** Leave `Book`, `BookPatch` and `BookController` where they are for now. You'll give them layers in the mini project! 😉

---

## 🪪 Part 3: The model

**`model/Student.java`** and **`model/StudentPatch.java`** stay the same — only the `package` line changes:

```java
package com.example.school.model;

public record Student(Long id, String name, String email, int age) {
}
```

```java
package com.example.school.model;

public record StudentPatch(String name, String email, Integer age) {
}
```

---

## 🧊 Part 4: The repository — storing data

The repository is our "storage room". Create **`repository/StudentRepository.java`**:

```java
package com.example.school.repository;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import org.springframework.stereotype.Repository;

import com.example.school.model.Student;

@Repository
public class StudentRepository {

    private final Map<Long, Student> students = new LinkedHashMap<>();
    private long nextId = 1;

    public StudentRepository() {
        save(new Student(null, "Sara Ahmed", "sara@school.com", 12));
        save(new Student(null, "Tom Brown", "tom@school.com", 13));
        save(new Student(null, "Lina Haddad", "lina@school.com", 11));
    }

    public List<Student> findAll() {
        return new ArrayList<>(students.values());
    }

    public Optional<Student> findById(Long id) {
        return Optional.ofNullable(students.get(id));
    }

    public Optional<Student> findByEmail(String email) {
        return students.values().stream()
                .filter(student -> student.email().equalsIgnoreCase(email))
                .findFirst();
    }

    public Student save(Student student) {
        Long id = student.id();
        if (id == null) {
            id = nextId;
            nextId++;
        }
        Student saved = new Student(id, student.name(), student.email(), student.age());
        students.put(id, saved);
        return saved;
    }

    public boolean existsById(Long id) {
        return students.containsKey(id);
    }

    public void deleteById(Long id) {
        students.remove(id);
    }
}
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@Repository` | A bean that stores data (Chapter 54). |
| `Map<Long, Student> students` | ⭐ A **map** now, not a list! id → student (Chapter 31). Finding by id is **instant**: `students.get(id)`. No loops! ⚡ |
| `new LinkedHashMap<>()` | A map that **remembers the order** you added things (a normal `HashMap` mixes them up — Chapter 31). So the list stays 1, 2, 3... |
| `private long nextId = 1;` | The id counter now lives **here** — the storage room gives the numbers. |
| `public StudentRepository() { save(...); ... }` | The **constructor** adds our 3 starting students. They get ids **1, 2, 3** from `save`. |
| `findAll()` | All students, as a new list. |
| `findById(Long id)` | ⭐ Returns an **`Optional`**: maybe a student, maybe empty (Chapter 37). `Optional.ofNullable(x)` = "empty if `x` is `null`". |
| `findByEmail(String email)` | Search by email (ignoring big/small letters). |
| `save(Student student)` | ⭐ **Two jobs in one**: if the student has **no id** (`null`) → it's **new**: give it the next id. If it **has** an id → it's an **update**: replace the old one. `put` adds **or** replaces (Chapter 31). |
| `existsById(Long id)` | Is there a student with this id? `containsKey` (Chapter 31). |
| `deleteById(Long id)` | Remove from the map. |

### 🔮 A secret about these method names

`findAll`, `findById`, `save`, `existsById`, `deleteById`... these are **exactly** the names that **Spring Data JPA** uses (Part 9, Chapter 72)! 🤫 In Part 9, you'll **delete** this whole class and replace it with **one line**:

```java
public interface StudentRepository extends JpaRepository<Student, Long> { }
```

...and the service won't need to change, because the method names are the same. That's the **power of layers**! 🔌✨

---

## 🚨 Part 5: Custom exceptions

In the old controller, we threw `new ResponseStatusException(HttpStatus.NOT_FOUND, ...)`. But the **service** shouldn't know about HTTP status codes! 🙅 The service should just say **what happened**: "student not found". So we make **our own** exception classes.

**`exception/StudentNotFoundException.java`**

```java
package com.example.school.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class StudentNotFoundException extends RuntimeException {

    public StudentNotFoundException(Long id) {
        super("Student with id " + id + " was not found");
    }
}
```

**`exception/EmailAlreadyUsedException.java`**

```java
package com.example.school.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.CONFLICT)
public class EmailAlreadyUsedException extends RuntimeException {

    public EmailAlreadyUsedException(String email) {
        super("The email " + email + " is already used by another student");
    }
}
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `extends RuntimeException` | Our class **is** an exception (inheritance — Chapter 22). A **runtime** exception, so methods don't need `throws` everywhere (Chapter 33). |
| `public StudentNotFoundException(Long id)` | The constructor gets the id... |
| `super("Student with id " + id + " was not found")` | ...and gives a clear **message** to the parent class (`RuntimeException`). |
| `@ResponseStatus(HttpStatus.NOT_FOUND)` | ⭐ "If this exception reaches Spring, answer with **404**." (The same label as Chapter 62 — this time on a **class**!) |
| `@ResponseStatus(HttpStatus.CONFLICT)` | **409 Conflict** = "your request clashes with what's already there". Perfect for "email already used". |

The **name** of the exception tells the story: `StudentNotFoundException` — anyone reading the code understands it immediately. 📖

> 💡 Hmm, the exception still has an HTTP label (`@ResponseStatus`)... In **Chapter 66**, we'll remove it and decide the status in **one central place**. One step at a time! 🪜

---

## 👨‍🍳 Part 6: The service — the rules

**`service/StudentService.java`**

```java
package com.example.school.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.example.school.exception.EmailAlreadyUsedException;
import com.example.school.exception.StudentNotFoundException;
import com.example.school.model.Student;
import com.example.school.model.StudentPatch;
import com.example.school.repository.StudentRepository;

@Service
public class StudentService {

    private final StudentRepository studentRepository;

    public StudentService(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    public List<Student> getAll() {
        return studentRepository.findAll();
    }

    public Student getById(Long id) {
        return studentRepository.findById(id)
                .orElseThrow(() -> new StudentNotFoundException(id));
    }

    public Student create(Student newStudent) {
        if (studentRepository.findByEmail(newStudent.email()).isPresent()) {
            throw new EmailAlreadyUsedException(newStudent.email());
        }
        Student student = new Student(null, newStudent.name(), newStudent.email(), newStudent.age());
        return studentRepository.save(student);
    }

    public Student replace(Long id, Student changed) {
        getById(id);
        Student student = new Student(id, changed.name(), changed.email(), changed.age());
        return studentRepository.save(student);
    }

    public Student update(Long id, StudentPatch patch) {
        Student old = getById(id);
        Student updated = new Student(
                id,
                patch.name() != null ? patch.name() : old.name(),
                patch.email() != null ? patch.email() : old.email(),
                patch.age() != null ? patch.age() : old.age());
        return studentRepository.save(updated);
    }

    public void delete(Long id) {
        if (!studentRepository.existsById(id)) {
            throw new StudentNotFoundException(id);
        }
        studentRepository.deleteById(id);
    }
}
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@Service` | The "chef" bean (Chapter 53). |
| `private final StudentRepository studentRepository;` + constructor | 💉 Constructor injection: the service **needs** the repository. |
| `getById(Long id)` | Ask the repository. If the `Optional` is empty → **throw** `StudentNotFoundException`. |
| `create(...)` | ⭐ **Our first business rule!** 📧 |
| `findByEmail(...).isPresent()` | "Is this email **already** used?" |
| `throw new EmailAlreadyUsedException(...)` | Yes → refuse! → **409**. |
| `new Student(null, ...)` | `id = null` → "this is new" → the repository gives an id. (The client's id is ignored — Chapter 60! 🛡️) |
| `replace(...)` | `getById(id);` first — we don't **use** the result, we just want the **404** if the student doesn't exist. Then save with the id from the path. |
| `update(...)` | PATCH — the same ternaries as Chapter 61. |
| `delete(...)` | Doesn't exist → 404. Otherwise, delete. |

**Notice:** 👀 There's **no** `ResponseEntity`, **no** `@GetMapping`, **no** `HttpStatus` in the service. It's pure **school logic**. You could use this service from a website, a phone app, or a test — it doesn't care about HTTP. 🧠

---

## 🧑‍💼 Part 7: The controller — HTTP only

Now the controller becomes **thin** 🪶 — it just **passes** things to the service.

**`controller/StudentController.java`**

```java
package com.example.school.controller;

import java.net.URI;
import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.example.school.model.Student;
import com.example.school.model.StudentPatch;
import com.example.school.service.StudentService;

@RestController
@RequestMapping("/api/students")
public class StudentController {

    private final StudentService studentService;

    public StudentController(StudentService studentService) {
        this.studentService = studentService;
    }

    @GetMapping
    public List<Student> getAll() {
        return studentService.getAll();
    }

    @GetMapping("/{id}")
    public Student getById(@PathVariable Long id) {
        return studentService.getById(id);
    }

    @PostMapping
    public ResponseEntity<Student> create(@RequestBody Student newStudent) {
        Student created = studentService.create(newStudent);
        URI location = URI.create("/api/students/" + created.id());
        return ResponseEntity.created(location).body(created);
    }

    @PutMapping("/{id}")
    public Student replace(@PathVariable Long id, @RequestBody Student changed) {
        return studentService.replace(id, changed);
    }

    @PatchMapping("/{id}")
    public Student update(@PathVariable Long id, @RequestBody StudentPatch patch) {
        return studentService.update(id, patch);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        studentService.delete(id);
    }
}
```

### 🔍 What changed?

| Before (Ch 62) | Now |
|---|---|
| The controller had the **list** | The **repository** has the data |
| The controller searched with **streams** | The controller just **calls** `studentService...` |
| `ResponseEntity.notFound()` in many places | The service **throws** `StudentNotFoundException` → **404** automatically |
| ~130 lines | ~60 lines 🪶 |

Look at `getById` — **one line**! The "not found" case is handled by the **exception** (thrown in the service, turned into 404 by `@ResponseStatus`). The controller doesn't even need an `if`. ✨

`create` still uses `ResponseEntity`, because it needs the **`Location`** header (Chapter 62). `delete` uses `@ResponseStatus(HttpStatus.NO_CONTENT)` — always 204 when it works.

> 💡 To keep this chapter short, we left out the **filters**, sorting, `/count`, `/search` and the other extras from Chapters 57–59. Moving them into the layers is **Task 1** below! 💪

---

## ✅ Part 8: Test it — the same API, a new inside

**Restart** and test. From the **outside**, the API looks the same (that's the point of refactoring! 🧹). Real answers:

`GET /api/students/2`

```json
{"id":2,"name":"Tom Brown","email":"tom@school.com","age":13}
```

`GET /api/students/99`

```
HTTP/1.1 404 
{"timestamp":"...","status":404,"error":"Not Found","path":"/api/students/99"}
```

`POST /api/students` with Omar →

```
HTTP/1.1 201 
Location: /api/students/4

{"id":4,"name":"Omar Ali","email":"omar@school.com","age":12}
```

### 📧 And the new business rule!

Try to add **another** student with Sara's email — even in **capital letters**:

```bash
curl -i -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Sara Copy","email":"SARA@school.com","age":12}'
```

```
HTTP/1.1 409 
Content-Type: application/json

{"timestamp":"2026-10-11T04:24:39.528Z","status":409,"error":"Conflict","path":"/api/students"}
```

✅ **409 Conflict** — "that email is already used!" The rule works. 🛡️

`DELETE /api/students/3` → **204**. Again → **404**. ✅

### 🗺️ The journey of one request

`GET /api/students/99`:

```
 1. 🧑‍💼 StudentController.getById(99)       "Service, give me student 99."
 2. 👨‍🍳 StudentService.getById(99)          "Repository, find 99."
 3. 🧊 StudentRepository.findById(99)       "Optional.empty — I don't have it."
 4. 👨‍🍳 StudentService                      "Empty?! throw StudentNotFoundException!" 💥
 5.    (the exception flies UP through the controller...)
 6. 🌱 Spring sees @ResponseStatus(NOT_FOUND) on the exception
 7. 🌐 HTTP/1.1 404
```

---

## 🤔 Part 9: Why is this better?

| Benefit | Example |
|---|---|
| 📖 **Easy to read** | Want the rules? Look in the **service**. Want the URLs? Look in the **controller**. |
| 🔄 **Easy to change** | New storage (database)? Change only the **repository**. |
| 🧪 **Easy to test** | Test the service's rules **without** HTTP (Part 11, Chapter 85). |
| ♻️ **Reusable** | The same service could be used by **two** controllers (a REST API and a web page). |
| 👥 **Teamwork** | One person works on the controller, another on the service. Fewer conflicts in Git (Chapter 42)! |

> 💡 **Packages by layer or by feature?** We grouped by **layer** (`controller`, `service`...). Big projects often group by **feature** instead (`student`, `book`, `teacher` — each with its own controller, service, repository). Both are fine. By layer is easiest to learn. 😊

---

## 💻 Mini project: The Book API, part 7 📚

Give your Book API layers too! Create (in the right packages):

1. `model/Book` and `model/BookPatch` (move them).
2. `repository/BookRepository` — with a `LinkedHashMap`, and the 3 books added in the constructor.
3. `exception/BookNotFoundException` — 404.
4. `service/BookService` — `getAll`, `getById`, `create`, `update` (PATCH), `delete`.
5. `controller/BookController` — thin, like `StudentController`.

**Business rule:** 📅 A book's `year` can't be in the **future**. If it is → throw a new **`InvalidBookException`** with **400** (`HttpStatus.BAD_REQUEST`).

<details>
<summary>Click to see the answer</summary>

**`repository/BookRepository.java`**

```java
package com.example.school.repository;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import org.springframework.stereotype.Repository;

import com.example.school.model.Book;

@Repository
public class BookRepository {

    private final Map<Long, Book> books = new LinkedHashMap<>();
    private long nextId = 1;

    public BookRepository() {
        save(new Book(null, "Matilda", "Roald Dahl", 1988));
        save(new Book(null, "The Hobbit", "J.R.R. Tolkien", 1937));
        save(new Book(null, "Charlotte's Web", "E.B. White", 1952));
    }

    public List<Book> findAll() {
        return new ArrayList<>(books.values());
    }

    public Optional<Book> findById(Long id) {
        return Optional.ofNullable(books.get(id));
    }

    public Book save(Book book) {
        Long id = book.id();
        if (id == null) {
            id = nextId;
            nextId++;
        }
        Book saved = new Book(id, book.title(), book.author(), book.year());
        books.put(id, saved);
        return saved;
    }

    public boolean existsById(Long id) {
        return books.containsKey(id);
    }

    public void deleteById(Long id) {
        books.remove(id);
    }
}
```

**`exception/BookNotFoundException.java`**

```java
package com.example.school.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.NOT_FOUND)
public class BookNotFoundException extends RuntimeException {

    public BookNotFoundException(Long id) {
        super("Book with id " + id + " was not found");
    }
}
```

**`exception/InvalidBookException.java`**

```java
package com.example.school.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.BAD_REQUEST)
public class InvalidBookException extends RuntimeException {

    public InvalidBookException(String message) {
        super(message);
    }
}
```

**`service/BookService.java`**

```java
package com.example.school.service;

import java.time.Year;
import java.util.List;

import org.springframework.stereotype.Service;

import com.example.school.exception.BookNotFoundException;
import com.example.school.exception.InvalidBookException;
import com.example.school.model.Book;
import com.example.school.model.BookPatch;
import com.example.school.repository.BookRepository;

@Service
public class BookService {

    private final BookRepository bookRepository;

    public BookService(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    public List<Book> getAll() {
        return bookRepository.findAll();
    }

    public Book getById(Long id) {
        return bookRepository.findById(id)
                .orElseThrow(() -> new BookNotFoundException(id));
    }

    public Book create(Book newBook) {
        checkYear(newBook.year());
        return bookRepository.save(new Book(null, newBook.title(), newBook.author(), newBook.year()));
    }

    public Book update(Long id, BookPatch patch) {
        Book old = getById(id);
        if (patch.year() != null) {
            checkYear(patch.year());
        }
        Book updated = new Book(
                id,
                patch.title() != null ? patch.title() : old.title(),
                patch.author() != null ? patch.author() : old.author(),
                patch.year() != null ? patch.year() : old.year());
        return bookRepository.save(updated);
    }

    public void delete(Long id) {
        if (!bookRepository.existsById(id)) {
            throw new BookNotFoundException(id);
        }
        bookRepository.deleteById(id);
    }

    private void checkYear(int year) {
        if (year > Year.now().getValue()) {
            throw new InvalidBookException("The year " + year + " is in the future");
        }
    }
}
```

**`controller/BookController.java`**

```java
package com.example.school.controller;

import java.net.URI;
import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.example.school.model.Book;
import com.example.school.model.BookPatch;
import com.example.school.service.BookService;

@RestController
@RequestMapping("/api/books")
public class BookController {

    private final BookService bookService;

    public BookController(BookService bookService) {
        this.bookService = bookService;
    }

    @GetMapping
    public List<Book> getAll() {
        return bookService.getAll();
    }

    @GetMapping("/{id}")
    public Book getById(@PathVariable Long id) {
        return bookService.getById(id);
    }

    @PostMapping
    public ResponseEntity<Book> create(@RequestBody Book newBook) {
        Book created = bookService.create(newBook);
        return ResponseEntity.created(URI.create("/api/books/" + created.id())).body(created);
    }

    @PatchMapping("/{id}")
    public Book update(@PathVariable Long id, @RequestBody BookPatch patch) {
        return bookService.update(id, patch);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        bookService.delete(id);
    }
}
```

Test: `POST /api/books` with `{"title":"Future Book","author":"Time Traveler","year":3000}` → **400**. 🚀❌ With The Gruffalo (1999) → **201**. ✅

</details>

---

## ✋ Try it yourself

**Task 1:** Bring back the **filters and sorting** (`minAge`, `name`, `sort`) from Chapter 59. Where does each part go?

<details>
<summary>Click to see the answer</summary>

- The **controller** reads the parameters (HTTP!) and passes them on:

```java
@GetMapping
public List<Student> getAll(@RequestParam(required = false) Integer minAge,
                            @RequestParam(required = false) String name,
                            @RequestParam(defaultValue = "id") String sort) {
    return studentService.getAll(minAge, name, sort);
}
```

- The **service** does the filtering and sorting (that's logic!):

```java
public List<Student> getAll(Integer minAge, String name, String sort) {
    Stream<Student> result = studentRepository.findAll().stream();
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
```

- The **repository** just gives **all** students (`findAll`). (In Part 9, the **database** will do filtering and sorting much faster — Chapter 74 and 78!)

</details>

**Task 2:** Add a business rule to `update` (PATCH): if the patch has a **new email**, it must not be used by **another** student. What's the tricky part?

<details>
<summary>Click to see the answer</summary>

```java
if (patch.email() != null) {
    studentRepository.findByEmail(patch.email())
            .filter(other -> !other.id().equals(id))
            .ifPresent(other -> {
                throw new EmailAlreadyUsedException(patch.email());
            });
}
```

The tricky part: a student may "change" their email to their **own** current email — that's not a conflict! So we only complain if the email belongs to a **different** student (`!other.id().equals(id)`). 🧠

</details>

**Task 3:** Which layer should do each job? a) read `?minAge=12` b) "a student must be at least 5 years old" c) save to the map d) answer 201 with `Location` e) "a class can have at most 30 students"

<details>
<summary>Click to see the answer</summary>

a) **Controller** b) **Service** (a business rule) c) **Repository** d) **Controller** (HTTP) e) **Service** (a business rule)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: The controller talks to the repository

```java
@RestController
public class StudentController {
    private final StudentRepository studentRepository;   // ❌ skipping the service!
}
```

It works... but now rules (like "email unique") are **skipped**, or copied into many controllers. 😬 **Fix:** Controller → **Service** → Repository. Always.

### Mistake 2: HTTP things in the service

```java
public ResponseEntity<Student> getById(Long id) { ... }   // ❌ in the service
```

The service shouldn't know about HTTP. **Fix:** The service returns **data** or **throws exceptions**. The controller makes the HTTP response.

### Mistake 3: Rules in the repository

```java
public Student save(Student s) {
    if (s.age() < 5) throw ...;   // ❌ a business rule in the storage room!
}
```

**Fix:** Repository = store and find. **Rules** go into the service. (In Part 9, the repository will be an interface — there won't even be a place for rules!)

### Mistake 4: Moving classes without IntelliJ

You move `Student.java` with Windows Explorer → `package com.example.school;` is now **wrong** → red errors everywhere. 😱 **Fix:** Use IntelliJ's **drag and drop** or **Refactor → Move (F6)**.

### Mistake 5: A package outside the base package

`com.example.controller` instead of `com.example.school.controller` → Spring doesn't find the controller → **404** for everything (Chapter 50). **Fix:** Always create packages **inside** `com.example.school`.

---

## ✅ Summary

- Professional apps have **layers**, each with **one** job:
  - **Controller** 🧑‍💼 (`@RestController`) — HTTP: read the request, call the service, build the response.
  - **Service** 👨‍🍳 (`@Service`) — business **rules** and logic. No HTTP!
  - **Repository** 🧊 (`@Repository`) — **store** and **find** data. No rules!
- Calls go **down only**: Controller → Service → Repository.
- Packages: `controller`, `service`, `repository`, `model`, `exception` — all **inside** the base package.
- The repository uses a **`LinkedHashMap`** (id → student) and methods named like Spring Data JPA: `findAll`, `findById`, `save`, `existsById`, `deleteById`. 🔮
- **Custom exceptions** (`StudentNotFoundException`, `EmailAlreadyUsedException`) say **what** went wrong. `@ResponseStatus` on the class chooses the status (404, 409).
- First **business rule**: an email can only be used **once** → **409 Conflict**.
- Move classes with **IntelliJ** (it fixes the imports).

---

## ❓ Quiz

1. Name the three layers and the job of each.
2. Which layer may call the repository?
3. Where does the rule "an email can only be used once" belong?
4. Why does the service throw `StudentNotFoundException` instead of returning a `ResponseEntity`?
5. What does `@ResponseStatus(HttpStatus.NOT_FOUND)` on an exception class do?
6. What does status **409 Conflict** mean?
7. Why did we change the list into a `LinkedHashMap`?
8. In the repository's `save`, how do we know if a student is new or an update?
9. How do you move a class into another package safely?

<details>
<summary>Click to see the answers</summary>

1. **Controller** (HTTP: requests and responses), **Service** (business rules and logic), **Repository** (storing and finding data).
2. Only the **service**.
3. In the **service**.
4. Because the service shouldn't know about HTTP. It only says **what** happened (by throwing an exception). The controller layer (and Spring) turn it into HTTP.
5. When this exception reaches Spring, Spring answers with status **404**.
6. "Your request clashes with the current state" — for example, the email already exists.
7. To find students by id instantly (`get(id)`) without loops, while keeping the order they were added.
8. A new student has `id == null`. A student with an id is an update.
9. With IntelliJ: drag and drop in the Project window, or **Refactor → Move (F6)**. IntelliJ fixes the `package` line and the imports.

</details>

---

[⬅ Previous chapter](62-response-entity.md) | [Table of Contents](../README.md) | [Next chapter: DTOs: safe boxes for data ➡](64-dtos.md)
