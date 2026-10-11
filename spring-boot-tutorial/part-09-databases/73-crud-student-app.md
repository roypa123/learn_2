# Chapter 73 – Full CRUD project: the Student app with a real database

[⬅ Previous chapter](72-repositories.md) | [Table of Contents](../README.md) | [Next chapter ➡](74-custom-queries.md)

---

## 🎯 Goal

This is the big moment! 🥁 We connect our **Student API** (Part 8) to the **database** (Chapters 69–72). After today: **restart the app, and your students are still there.** 💾🎉

At the end of this chapter you will know:

- How to switch the **service** from the old map to the **JPA repository**
- How to **update** an entity with **setters** (instead of creating new records)
- How to load **starting data** safely with a `DataLoader` 🏃
- How to store the database in a **file**, with `ddl-auto=update` 💾
- How to **prove** that the data survives a restart ✅
- How to remove the old code (`OldStudent`, `OldStudentRepository`) 🧹

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **CRUD** | **C**reate, **R**ead, **U**pdate, **D**elete — all four jobs with data. |
| **Refactoring** | Changing the **inside** of the code without changing what it does (Chapter 63). 🧹 |
| **Seed data** | Starting data for an **empty** database, like our 3 students. 🌱 |
| **`.gitignore`** | The file that tells Git **not** to save some files (Chapter 50). |

---

## 📖 Story: Moving to a new house 🏠➡️🏡

The school office is **moving** to a new building with a real filing cabinet 🗄️. The secretary (the **controller**) and the head teacher with the rules (the **service**) move too. What changes for **parents**? 🤔

**Nothing!** They still come to the **same window**, ask the **same questions**, fill out the **same forms**. Only **behind** the window, things are different: the cards are now in a cabinet that never forgets. 🗄️✨

That's today's refactoring:

| What | Changes? |
|---|---|
| The URLs, JSON, status codes (the **API**) | ❌ No — clients don't notice anything |
| The **controller** | ❌ No — not one line! |
| The **DTOs**, validation, error handling | ❌ No |
| The **service** | ✏️ A little (it uses the entity now) |
| The **repository** | ✅ The new JPA interface (Chapter 72) |
| Where data lives | 🧠 memory ➡️ 🗄️ database file |

Layers (Chapter 63) and DTOs (Chapter 64) make this **easy**. Let's see! 🔌

---

## 🔁 Part 1: `StudentResponse` reads the entity

The response DTO (Chapter 64) converted the old **record**. Now it converts the **entity** — with **getters** instead of record accessors:

**`dto/StudentResponse.java`**

```java
package com.example.school.dto;

import com.example.school.entity.Student;

public record StudentResponse(Long id, String name, String email, int age) {

    public static StudentResponse from(Student student) {
        return new StudentResponse(student.getId(), student.getName(), student.getEmail(), student.getAge());
    }
}
```

| What changed | Why |
|---|---|
| `import com.example.school.entity.Student;` | The **entity** now, not `model.OldStudent`. |
| `student.getId()` instead of `student.id()` | Entities have **getters** (Chapter 71); records had `id()`. |

The JSON stays **exactly** the same: `{"id":..., "name":..., "email":..., "age":...}`. Clients won't notice a thing. 😎

---

## 🔍 Part 2: One extra method in the repository

The service checks "is this email already used?" (Chapter 63). Add **one** method to the repository interface:

```java
package com.example.school.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.school.entity.Student;

public interface StudentRepository extends JpaRepository<Student, Long> {

    boolean existsByEmailIgnoreCase(String email);
}
```

| Code | Meaning |
|---|---|
| `boolean existsByEmailIgnoreCase(String email);` | ⭐ Just a method **name** — no code! Spring Data **reads the name** and writes the SQL: "does a student exist whose **email** equals this one, **ignoring** big/small letters?" 🧞 |

Magic? Not quite — it's a **naming rule**. You'll learn all about it in **Chapter 74**! 🔮

---

## 👨‍🍳 Part 3: The new service

Here's the whole **`service/StudentService.java`** — now using the JPA repository and the entity:

```java
package com.example.school.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.example.school.dto.StudentPatchRequest;
import com.example.school.dto.StudentRequest;
import com.example.school.dto.StudentResponse;
import com.example.school.entity.Student;
import com.example.school.exception.EmailAlreadyUsedException;
import com.example.school.exception.StudentNotFoundException;
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
        if (studentRepository.existsByEmailIgnoreCase(request.email())) {
            throw new EmailAlreadyUsedException(request.email());
        }
        Student student = new Student(request.name(), request.email(), request.age());
        return StudentResponse.from(studentRepository.save(student));
    }

    public StudentResponse replace(Long id, StudentRequest request) {
        Student student = findStudent(id);
        student.setName(request.name());
        student.setEmail(request.email());
        student.setAge(request.age());
        return StudentResponse.from(studentRepository.save(student));
    }

    public StudentResponse update(Long id, StudentPatchRequest patch) {
        Student student = findStudent(id);
        if (patch.name() != null) {
            student.setName(patch.name());
        }
        if (patch.email() != null) {
            student.setEmail(patch.email());
        }
        if (patch.age() != null) {
            student.setAge(patch.age());
        }
        return StudentResponse.from(studentRepository.save(student));
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

### 🔍 What changed (compared to Chapter 64)

| Method | Before (map + record) | Now (JPA + entity) |
|---|---|---|
| `getAll` | `studentRepository.findAll()` on the map | `findAll()` on the **JPA** repository — the **same** name! ✨ |
| `create` | `findByEmail(...).isPresent()` | `existsByEmailIgnoreCase(...)` (one `SELECT count(*)`, a bit faster) |
| `create` | `new Student(null, ..., "", LocalDateTime.now())` | `new Student(name, email, age)` — the **entity's constructor** sets the note and the time (Chapter 71) |
| `replace` | built a **new** record with the old note/date | ⭐ loads the entity and changes it with **setters** |
| `update` (PATCH) | ternaries `x != null ? x : old` | ⭐ `if (x != null) student.setX(x);` — only change what was sent |
| `delete`, `findStudent` | `existsById`, `findById` | the **same**! |

### 🔍 The interesting lines

| Code | Meaning |
|---|---|
| `Student student = new Student(request.name(), request.email(), request.age());` | A new entity. Its `id` is `null` → `save` will **INSERT** (Chapter 72). |
| `studentRepository.save(student)` | Returns the saved student — **with** its new id from the database. 🔢 |
| `Student student = findStudent(id);` | Load the existing entity from the database. |
| `student.setName(request.name());` | ⭐ Change the object. Entities are **changeable** — that's why they're classes! (Chapter 71) |
| `studentRepository.save(student)` | The id is set → `save` does an **UPDATE**. |
| `if (patch.age() != null) { student.setAge(patch.age()); }` | PATCH: change **only** what the client sent. Simpler than the ternaries! 🩹 |

> 💡 The **controller** doesn't change at all — not one line! It still calls `studentService.getAll()`, `create(...)`, etc. That's the power of **layers**. 🎂

---

## 🌱 Part 4: Starting data with a `DataLoader`

We deleted `data.sql` in Chapter 72. Who adds our 3 students now? A **`CommandLineRunner`** (Chapter 72) — but a **careful** one: it only adds them if the database is **empty**.

**`DataLoader.java`** (in `com.example.school`):

```java
package com.example.school;

import java.util.List;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import com.example.school.entity.Student;
import com.example.school.repository.StudentRepository;

@Component
public class DataLoader implements CommandLineRunner {

    private final StudentRepository studentRepository;

    public DataLoader(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    @Override
    public void run(String... args) {
        if (studentRepository.count() == 0) {
            studentRepository.saveAll(List.of(
                    new Student("Sara Ahmed", "sara@school.com", 12),
                    new Student("Tom Brown", "tom@school.com", 13),
                    new Student("Lina Haddad", "lina@school.com", 11)));
            System.out.println("DataLoader: added 3 students");
        } else {
            System.out.println("DataLoader: the database already has " + studentRepository.count() + " students");
        }
    }
}
```

| Code | Meaning |
|---|---|
| `implements CommandLineRunner` | Runs once after startup. 🏃 |
| `if (studentRepository.count() == 0)` | ⭐ **Only** if the table is empty! Otherwise, we'd add Sara again at every restart — and crash on the unique email. 💥 |
| `saveAll(List.of(...))` | Save three at once. |
| `System.out.println(...)` | A message, so we can **see** what happened. |

> 💡 **Why Java and not `data.sql`?** With a **file** database (next part), `data.sql` would run at **every** start and try to insert Sara again. A `DataLoader` can **check first**. 🧠

---

## 💾 Part 5: A database that remembers — the file

Now the big switch: from **memory** to a **file**. Change **`application.properties`** to:

```properties
spring.application.name=school

# The database: a FILE in the folder "data" of the project
spring.datasource.url=jdbc:h2:file:./data/school
spring.datasource.username=sa
spring.datasource.password=

# The H2 console (a web page to look inside the database)
spring.h2.console.enabled=true

# JPA / Hibernate
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.open-in-view=false
```

### 🔍 What changed

| Setting | Meaning |
|---|---|
| `spring.datasource.url=jdbc:h2:file:./data/school` | ⭐ A **file** database: `./` = the project folder, so H2 creates **`data/school.mv.db`**. 💾 |
| `spring.jpa.hibernate.ddl-auto=update` | ⭐ **Very important!** For an H2 **file**, Spring Boot would still use `create-drop` (it's still an "embedded" database) — and **delete everything** at every start! 😱 `update` means: "create missing tables, but **never** delete data." |
| *(removed)* `defer-datasource-initialization` | Not needed anymore — no `data.sql`. |

### 🙈 Don't save the database in Git

The file `data/school.mv.db` is **data**, not code. Open **`.gitignore`** (Chapter 50) and add a line at the end:

```
data/
```

Now Git ignores the whole `data` folder. ✅ (Every developer has their **own** local database.)

---

## 🧹 Part 6: Delete the old code

The old classes are not used anymore. Delete them (right-click → **Delete**):

- 🗑️ `model/OldStudent.java`
- 🗑️ `repository/OldStudentRepository.java`
- 🗑️ `RepositoryPlayground.java` (if you still have it)

If IntelliJ shows **red** anywhere, something still uses them — read the error, and use the entity or the new repository instead.

Your student classes now look like this:

```
com.example.school
├── SchoolApplication.java
├── DataLoader.java                   🌱 new
├── controller/StudentController.java   (unchanged!)
├── service/StudentService.java         ✏️ changed
├── repository/StudentRepository.java   ✨ the JPA interface
├── entity/Student.java                 🧱 the entity
├── dto/StudentRequest.java, StudentPatchRequest.java, StudentResponse.java
└── exception/...                       (unchanged)
```

---

## ✅ Part 7: Test everything!

Restart. In the log, Hibernate creates the table (it's a new, empty file), and then:

```
DataLoader: added 3 students
```

Now test the API — these are **real** answers:

`GET /api/students`

```json
[{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12},{"id":2,"name":"Tom Brown","email":"tom@school.com","age":13},{"id":3,"name":"Lina Haddad","email":"lina@school.com","age":11}]
```

`POST /api/students` with Omar →

```
HTTP/1.1 201 
Location: /api/students/4

{"id":4,"name":"Omar Ali","email":"omar@school.com","age":12}
```

`PATCH /api/students/2` with `{"email":"tom.brown@school.com"}` →

```json
{"id":2,"name":"Tom Brown","email":"tom.brown@school.com","age":13}
```

`DELETE /api/students/3` → **204**. Then `GET /api/students/3` →

```json
{"detail":"Student with id 3 was not found","instance":"/api/students/3","status":404,"title":"Student not found"}
```

`POST` with `SARA@school.com` → **409** `Email already used`. ✅ (Our `IgnoreCase` method works!)

`POST` with `{"name":"A","email":"x","age":3}` → **400** with the `errors` map. ✅ (Validation still works — we didn't touch it!)

**Everything** from Part 8 works — now with a real database. 🎉

### 💾 The moment of truth: restart!

**Stop** the app ⏹️ and **start** it again ▶️. Look at the log:

```
DataLoader: the database already has 3 students
```

Hibernate created **no** table this time (`update` saw it's already there). Now:

`GET /api/students`

```json
[{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12},{"id":2,"name":"Tom Brown","email":"tom.brown@school.com","age":13},{"id":4,"name":"Omar Ali","email":"omar@school.com","age":12}]
```

🎉🎉🎉 **Omar is still there! Tom's new email is still there! Lina is still deleted!** The data **survived the restart**. Your app finally has a memory. 🧠💾

### 🔍 Look inside with the console

Open `/h2-console` and use the URL **`jdbc:h2:file:./data/school`** (the same as in the settings!). Run `SELECT * FROM students;` — the same rows, straight from the file. 🗄️

> ⚠️ The H2 file database can be opened by **one** program at a time. Don't try to open the file with the **standalone** console from Chapter 68 while the app is running — use the console **inside** the app (`/h2-console`).

---

## 🗺️ Part 8: The journey of a request — now with a database

`POST /api/students` with Omar:

```
 🌐 POST /api/students {"name":"Omar Ali",...}
   │
   ▼  💂 @Valid checks the StudentRequest (Chapter 65)
 🧑‍💼 StudentController.create(request)
   │
   ▼
 👨‍🍳 StudentService.create(request)
   │   existsByEmailIgnoreCase("omar@school.com") ──► 🗄️ select count(...) where upper(email)=upper(?)
   │   new Student("Omar Ali", ...)   (id = null, createdAt = now)
   │   studentRepository.save(student) ─────────────► 🗄️ insert into students (...) values (...)
   │   StudentResponse.from(saved)    (id = 4!)
   ▼
 🧑‍💼 ResponseEntity.created("/api/students/4").body(...)
   │
   ▼
 🌐 201 Created  {"id":4,"name":"Omar Ali",...}
```

Every layer does **its** job. 🎂

---

## 💻 Mini project: The Book API with a database 📚

Connect your **Book API** to the database, the same way:

1. Use the `Book` **entity** (Chapter 71) and **`BookRepository`** (Chapter 72).
2. Change `BookResponse.from(...)` to use getters.
3. Change **`BookService`**: `create` makes `new Book(title, author, year, "NEW")` and saves it; `update` (PATCH) uses setters; `delete` uses `existsById` + `deleteById`. Keep the "year not in the future" rule!
4. Add the 3 books in the **`DataLoader`** (only if there are no books yet).
5. Delete the old map repository and the old `model.Book` record.
6. Test: create **The Gruffalo** (1999), restart, and check that it's still there.

<details>
<summary>Click to see the answer</summary>

**`dto/BookResponse.java`**

```java
package com.example.school.dto;

import java.time.Year;

import com.example.school.entity.Book;

public record BookResponse(Long id, String title, String author, int year, int ageInYears) {

    public static BookResponse from(Book book) {
        int age = Year.now().getValue() - book.getYear();
        return new BookResponse(book.getId(), book.getTitle(), book.getAuthor(), book.getYear(), age);
    }
}
```

**`service/BookService.java`**

```java
package com.example.school.service;

import java.time.Year;
import java.util.List;

import org.springframework.stereotype.Service;

import com.example.school.dto.BookPatchRequest;
import com.example.school.dto.BookRequest;
import com.example.school.dto.BookResponse;
import com.example.school.entity.Book;
import com.example.school.exception.BookNotFoundException;
import com.example.school.exception.InvalidBookException;
import com.example.school.repository.BookRepository;

@Service
public class BookService {

    private final BookRepository bookRepository;

    public BookService(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

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
        Book book = new Book(request.title(), request.author(), request.year(), "NEW");
        return BookResponse.from(bookRepository.save(book));
    }

    public BookResponse update(Long id, BookPatchRequest patch) {
        Book book = findBook(id);
        if (patch.title() != null) {
            book.setTitle(patch.title());
        }
        if (patch.author() != null) {
            book.setAuthor(patch.author());
        }
        if (patch.year() != null) {
            checkYear(patch.year());
            book.setYear(patch.year());
        }
        return BookResponse.from(bookRepository.save(book));
    }

    public void delete(Long id) {
        if (!bookRepository.existsById(id)) {
            throw new BookNotFoundException(id);
        }
        bookRepository.deleteById(id);
    }

    private Book findBook(Long id) {
        return bookRepository.findById(id)
                .orElseThrow(() -> new BookNotFoundException(id));
    }

    private void checkYear(int year) {
        if (year > Year.now().getValue()) {
            throw new InvalidBookException("The year " + year + " is in the future");
        }
    }
}
```

In the **`DataLoader`**, inject `BookRepository` too, and add:

```java
if (bookRepository.count() == 0) {
    bookRepository.saveAll(List.of(
            new Book("Matilda", "Roald Dahl", 1988, "A-1"),
            new Book("The Hobbit", "J.R.R. Tolkien", 1937, "F-7"),
            new Book("Charlotte's Web", "E.B. White", 1952, "C-3")));
}
```

`BookController` doesn't change. 😎 Test: `POST /api/books` with The Gruffalo → **201** with `"id":4`; restart; `GET /api/books/4` → still there! 💾

</details>

---

## ✋ Try it yourself

**Task 1:** Change `ddl-auto=update` to `create-drop` (just for a test!) and restart twice. What happens to Omar?

<details>
<summary>Click to see the answer</summary>

He's **gone** — `create-drop` deletes and recreates the tables at every start, and the `DataLoader` adds the 3 starting students again. 😱 That's why we use `update` for a file database. (Change it back!)

</details>

**Task 2:** Stop the app and look in the project folder. Which new folder and file do you see?

<details>
<summary>Click to see the answer</summary>

A folder `data` with the file `school.mv.db` — the whole database! (Sometimes also a `school.trace.db` with H2's own error notes.) Delete the folder → the next start begins with an **empty** database, and the `DataLoader` adds the 3 students again.

</details>

**Task 3:** Why didn't we change **any** line in `StudentController`?

<details>
<summary>Click to see the answer</summary>

Because the controller only talks to the **service**, using **DTOs**. The service's methods and the DTOs stayed the same — only the **inside** of the service and the repository changed. That's exactly why we built layers (Chapter 63) and DTOs (Chapter 64)! 🎂

</details>

---

## ⚠️ Common mistakes

### Mistake 1: A file database with `create-drop`

Without `ddl-auto=update`, Spring Boot treats the H2 **file** like any embedded database and uses `create-drop` → **all data is deleted at every start**. 😱 **Fix:** `spring.jpa.hibernate.ddl-auto=update`.

### Mistake 2: A `DataLoader` without the `count()` check

At the second start, it tries to insert Sara **again** → the unique email rule fails → the app **doesn't start**. 💥 **Fix:** `if (studentRepository.count() == 0)`.

### Mistake 3: Different URLs in the app and the console

The app uses `jdbc:h2:file:./data/school`, the console uses `jdbc:h2:mem:school` → an empty database in the console. **Fix:** The **same** URL.

### Mistake 4: Committing the database file to Git

`data/school.mv.db` ends up on GitHub — with everyone's test data. 😬 **Fix:** Add `data/` to `.gitignore`.

### Mistake 5: Forgetting to use the entity's getters

`student.name()` → `cannot find symbol`. The entity is a **class** with **getters**: `student.getName()`.

---

## ✅ Summary

- The **service** switched from the map to the **JPA repository** — the method names (`findAll`, `findById`, `save`, `existsById`, `deleteById`) stayed the same. 🔌
- `existsByEmailIgnoreCase(...)` — a repository method with **only a name**; Spring Data writes the query (Chapter 74).
- **Create:** `new Student(...)` + `save` → INSERT. **Update:** load the entity, use **setters**, `save` → UPDATE.
- A **`DataLoader`** (`CommandLineRunner`) adds **seed data** — **only** if the table is empty.
- **File database:** `jdbc:h2:file:./data/school` + **`ddl-auto=update`** (never `create-drop` for data you want to keep!). Add `data/` to `.gitignore`.
- The **controller**, **DTOs**, **validation** and **error handling** didn't change — clients see the same API.
- **Restart → the data is still there!** 💾🎉

---

## ❓ Quiz

1. Which classes changed in this chapter? Which didn't?
2. How does the service update a student now?
3. Why does the `DataLoader` check `count() == 0`?
4. What does `jdbc:h2:file:./data/school` mean?
5. Why must we set `ddl-auto=update` for the file database?
6. Where is the database file? Should it go into Git?
7. You restart the app. Which log line tells you that the data was kept?

<details>
<summary>Click to see the answers</summary>

1. Changed: `StudentService`, `StudentResponse`, `StudentRepository` (new interface), the settings, plus the new `DataLoader`. Not changed: `StudentController`, the request DTOs, validation, exceptions and the error handler.
2. It loads the entity (`findById`), changes it with setters, and calls `save` (which does an UPDATE).
3. So it only adds the starting students to an **empty** database — otherwise it would try to add them again at every start (and fail on the unique email).
4. An H2 database stored in a file: the folder `data` in the project, file name `school.mv.db`.
5. Because otherwise Spring Boot uses `create-drop` for H2, which deletes all tables (and data) at every start.
6. In `data/school.mv.db` in the project folder. No — add `data/` to `.gitignore`.
7. `DataLoader: the database already has ... students`

</details>

---

[⬅ Previous chapter](72-repositories.md) | [Table of Contents](../README.md) | [Next chapter: Your own queries ➡](74-custom-queries.md)
