# Chapter 75 – Relationships: One-to-Many

[⬅ Previous chapter](74-custom-queries.md) | [Table of Contents](../README.md) | [Next chapter ➡](76-many-to-many.md)

---

## 🎯 Goal

A school isn't just a list of students. 🏫 Students sit in **classrooms**: **one** classroom has **many** students. Today we connect two tables!

At the end of this chapter you will know:

- What a **one-to-many** relationship is (and its other side, **many-to-one**)
- How to build it with **`@ManyToOne`**, **`@JoinColumn`** and **`@OneToMany(mappedBy = ...)`**
- Which side **owns** the relationship (the one with the foreign key 🔗)
- What **lazy loading** is, and the famous **`LazyInitializationException`** 😱
- Why we use **`@Transactional`** in the services
- Why you must **never** return entities as JSON (the endless loop 🔁)
- A `Classroom` API: list classrooms, create one, put a student into a classroom

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Relationship** | A **connection** between two entities: a student **belongs to** a classroom. |
| **One-to-many** | **One** classroom has **many** students. 1️⃣ ➡️ 👥 |
| **Many-to-one** | **Many** students are in **one** classroom (the same relationship, seen from the other side). |
| **`@ManyToOne`** | The label on the "many" side: `Student.classroom`. |
| **`@JoinColumn`** | Chooses the **foreign key column**: `classroom_id`. 🔗 |
| **`@OneToMany(mappedBy = ...)`** | The label on the "one" side: `Classroom.students`. |
| **Owning side** | The side that has the **foreign key**. Only **its** changes are saved! |
| **Lazy loading** | Load related data **only when it's needed** (later). 😴 |
| **Eager loading** | Load related data **immediately**, always. ⚡ |
| **`@Transactional`** | "Do this whole method in **one** database **transaction**." (Fully explained in Chapter 79.) |

---

## 📖 Story: Classroom doors 🚪

Every classroom has a **door with a sign**: "**5A** — Mrs. Khan". 🚪 Every student has a **name tag** that says which classroom they belong to: "Sara — **5A**". 🏷️

- **One** classroom → **many** students. (5A has Sara and Lina.)
- **Each** student → **one** classroom. (Sara is only in 5A.)

Where do we write the connection? Not on the door (a door can't hold 30 names forever 😅)... but on **each student's name tag**. That's the **foreign key** from Chapter 67: the **student** row has a `classroom_id`. 🔗

```
 classrooms                         students
 ┌────┬──────┬───────────┐         ┌────┬─────────────┬──────────────┐
 │ id │ name │ teacher   │         │ id │ name        │ classroom_id │
 ├────┼──────┼───────────┤         ├────┼─────────────┼──────────────┤
 │ 1  │ 5A   │ Mrs. Khan │ ◄───────┤ 1  │ Sara Ahmed  │ 1            │
 │ 2  │ 6B   │ Mr. Brown │ ◄──┐ ┌──┤ 3  │ Lina Haddad │ 1            │
 └────┴──────┴───────────┘    └─┼──┤ 2  │ Tom Brown   │ 2            │
                                │  └────┴─────────────┴──────────────┘
   ONE classroom ...            └── ... MANY students point to it
```

---

## 🏫 Part 1: The `Classroom` entity

Create **`entity/Classroom.java`**:

```java
package com.example.school.entity;

import java.util.ArrayList;
import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

@Entity
@Table(name = "classrooms")
public class Classroom {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 10)
    private String name;

    @Column(nullable = false, length = 50)
    private String teacher;

    @OneToMany(mappedBy = "classroom")
    private List<Student> students = new ArrayList<>();

    protected Classroom() {
    }

    public Classroom(String name, String teacher) {
        this.name = name;
        this.teacher = teacher;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getTeacher() {
        return teacher;
    }

    public List<Student> getStudents() {
        return students;
    }
}
```

Most of it is like the `Student` entity (Chapter 71). The **new** part:

| Code | Meaning |
|---|---|
| `@OneToMany(mappedBy = "classroom")` | ⭐ "**One** classroom has **many** students. The connection is stored by the field **`classroom`** in the `Student` class." |
| `private List<Student> students = new ArrayList<>();` | The list of students in this classroom. Start with an **empty** list (never `null`). |
| `mappedBy = "classroom"` | "**I don't** store the connection — the **other side** does (the student's `classroom` field)." No extra column in `classrooms`! |

---

## 🧑‍🎓 Part 2: The other side — `Student.classroom`

Add a new **field** (and a getter and setter) to the **`Student`** entity:

```java
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "classroom_id")
private Classroom classroom;
```

```java
public Classroom getClassroom() {
    return classroom;
}

public void setClassroom(Classroom classroom) {
    this.classroom = classroom;
}
```

(Imports from `jakarta.persistence`: `FetchType`, `JoinColumn`, `ManyToOne`.)

| Code | Meaning |
|---|---|
| `@ManyToOne` | ⭐ "**Many** students → **one** classroom." |
| `(fetch = FetchType.LAZY)` | "Don't load the classroom until I **ask** for it." 😴 (Part 6.) |
| `@JoinColumn(name = "classroom_id")` | ⭐ "Store the connection in a column called **`classroom_id`**" — the **foreign key** 🔗. |
| `private Classroom classroom;` | A real **object**, not a number! In Java you write `sara.getClassroom().getName()` → `"5A"`. Hibernate turns it into `classroom_id = 1` in the table. 🗣️ |

### 👑 Who owns the relationship?

```
   Student.classroom   @ManyToOne + @JoinColumn     ← 👑 OWNER (has the foreign key column)
   Classroom.students  @OneToMany(mappedBy = ...)   ← 🪞 MIRROR (just a view of the other side)
```

| | Owner 👑 (`Student.classroom`) | Mirror 🪞 (`Classroom.students`) |
|---|---|---|
| Has a column in the database? | ✅ `classroom_id` | ❌ |
| Changing it is **saved**? | ✅ `sara.setClassroom(sixB)` | ❌ `fiveA.getStudents().add(sara)` alone does **nothing** in the database! |
| Used for | **Changing** the relationship | **Reading** "who is in this classroom?" |

**Rule:** 📏 To put a student into a classroom, **always** call **`student.setClassroom(classroom)`**. 👑

---

## 👀 Part 3: The tables Hibernate builds

Restart with a **fresh** database (delete the `data` folder). Hibernate writes (real output, shortened):

```sql
create table classrooms (
    id bigint generated by default as identity,
    name varchar(10) not null,
    teacher varchar(50) not null,
    primary key (id)
)

create table students (
    id bigint generated by default as identity,
    age integer not null,
    created_at timestamp(6) not null,
    email varchar(100) not null,
    name varchar(50) not null,
    teacher_note varchar(255),
    classroom_id bigint,
    primary key (id)
)

alter table if exists students
   add constraint FKn4i882kjg6fdyg2e641yh3jmk
   foreign key (classroom_id)
   references classrooms
```

| SQL | Meaning |
|---|---|
| `classroom_id bigint` in `students` | ⭐ The **foreign key column** from `@JoinColumn`. (It may be empty — a student without a classroom.) |
| *(no `students` column in `classrooms`)* | The mirror side (`mappedBy`) needs **no** column. 🪞 |
| `add constraint FK... foreign key (classroom_id) references classrooms` | ⭐ The **database rule**: `classroom_id` must point to a **real** classroom. 🛡️ (The strange name `FKn4i8...` is made up by Hibernate.) |

> 💡 With `ddl-auto=update`, Hibernate **adds** the new table and column to an existing database. But if things look strange, the easiest fix while learning is: stop the app, **delete the `data` folder**, start again. 🧹

---

## 🌱 Part 4: Starting data with classrooms

Create **`repository/ClassroomRepository.java`**:

```java
package com.example.school.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.school.entity.Classroom;

public interface ClassroomRepository extends JpaRepository<Classroom, Long> {
}
```

And change the **`DataLoader`** so it creates two classrooms and puts the students in them:

```java
@Component
public class DataLoader implements CommandLineRunner {

    private final StudentRepository studentRepository;
    private final ClassroomRepository classroomRepository;

    public DataLoader(StudentRepository studentRepository, ClassroomRepository classroomRepository) {
        this.studentRepository = studentRepository;
        this.classroomRepository = classroomRepository;
    }

    @Override
    @Transactional
    public void run(String... args) {
        if (studentRepository.count() > 0) {
            System.out.println("DataLoader: the database already has " + studentRepository.count() + " students");
            return;
        }
        Classroom fiveA = classroomRepository.save(new Classroom("5A", "Mrs. Khan"));
        Classroom sixB = classroomRepository.save(new Classroom("6B", "Mr. Brown"));

        Student sara = new Student("Sara Ahmed", "sara@school.com", 12);
        sara.setClassroom(fiveA);

        Student tom = new Student("Tom Brown", "tom@school.com", 13);
        tom.setClassroom(sixB);

        Student lina = new Student("Lina Haddad", "lina@school.com", 11);
        lina.setClassroom(fiveA);

        studentRepository.save(sara);
        studentRepository.save(tom);
        studentRepository.save(lina);
        System.out.println("DataLoader: added 2 classrooms and 3 students");
    }
}
```

(Import `org.springframework.transaction.annotation.Transactional`.)

| Code | Meaning |
|---|---|
| `Classroom fiveA = classroomRepository.save(...)` | Save the classroom **first** — it needs an id before students can point to it. |
| `sara.setClassroom(fiveA);` | ⭐ Connect them — on the **owner** side 👑. |
| `studentRepository.save(sara);` | The `INSERT` writes `classroom_id = 1`. 🔗 |
| `@Transactional` | Do it all in **one** transaction (Part 6 and Chapter 79). |
| `return;` | Leave the method early — nothing to do. |

---

## 📦 Part 5: DTOs and the Classroom API

### Show the classroom in `StudentResponse`

```java
package com.example.school.dto;

import com.example.school.entity.Student;

public record StudentResponse(Long id, String name, String email, int age, String classroom) {

    public static StudentResponse from(Student student) {
        String classroomName = student.getClassroom() != null ? student.getClassroom().getName() : null;
        return new StudentResponse(student.getId(), student.getName(), student.getEmail(),
                student.getAge(), classroomName);
    }
}
```

| Code | Meaning |
|---|---|
| `String classroom` | A new field: just the **name** of the classroom, like `"5A"`. (Not the whole object!) |
| `student.getClassroom() != null ? ... : null` | A student **may** have no classroom → then `null`. Without this check: `NullPointerException`! 💥 |

### DTOs for classrooms

**`dto/ClassroomRequest.java`**

```java
package com.example.school.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record ClassroomRequest(

        @NotBlank(message = "Name is required")
        @Size(max = 10, message = "Name must be at most 10 characters long")
        String name,

        @NotBlank(message = "Teacher is required")
        String teacher) {
}
```

**`dto/ClassroomResponse.java`**

```java
package com.example.school.dto;

import java.util.List;

import com.example.school.entity.Classroom;

public record ClassroomResponse(Long id, String name, String teacher, List<String> students) {

    public static ClassroomResponse from(Classroom classroom) {
        List<String> names = classroom.getStudents().stream()
                .map(student -> student.getName())
                .toList();
        return new ClassroomResponse(classroom.getId(), classroom.getName(), classroom.getTeacher(), names);
    }
}
```

| Code | Meaning |
|---|---|
| `List<String> students` | Just the **names** of the students — short and safe. |
| `classroom.getStudents()` | ⭐ The **mirror** side 🪞: "who is in this classroom?" Hibernate loads them **now** (lazy loading — Part 6!). |

### The exception, the service and the controller

**`exception/ClassroomNotFoundException.java`**

```java
package com.example.school.exception;

public class ClassroomNotFoundException extends RuntimeException {

    public ClassroomNotFoundException(Long id) {
        super("Classroom with id " + id + " was not found");
    }
}
```

And a handler in **`GlobalExceptionHandler`** (Chapter 66):

```java
@ExceptionHandler(ClassroomNotFoundException.class)
public ProblemDetail handleClassroomNotFound(ClassroomNotFoundException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
    problem.setTitle("Classroom not found");
    return problem;
}
```

**`service/ClassroomService.java`**

```java
package com.example.school.service;

import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.school.dto.ClassroomRequest;
import com.example.school.dto.ClassroomResponse;
import com.example.school.dto.StudentResponse;
import com.example.school.entity.Classroom;
import com.example.school.entity.Student;
import com.example.school.exception.ClassroomNotFoundException;
import com.example.school.exception.StudentNotFoundException;
import com.example.school.repository.ClassroomRepository;
import com.example.school.repository.StudentRepository;

@Service
public class ClassroomService {

    private final ClassroomRepository classroomRepository;
    private final StudentRepository studentRepository;

    public ClassroomService(ClassroomRepository classroomRepository, StudentRepository studentRepository) {
        this.classroomRepository = classroomRepository;
        this.studentRepository = studentRepository;
    }

    @Transactional(readOnly = true)
    public List<ClassroomResponse> getAll() {
        return classroomRepository.findAll().stream()
                .map(ClassroomResponse::from)
                .toList();
    }

    @Transactional(readOnly = true)
    public ClassroomResponse getById(Long id) {
        return ClassroomResponse.from(findClassroom(id));
    }

    @Transactional
    public ClassroomResponse create(ClassroomRequest request) {
        Classroom classroom = new Classroom(request.name(), request.teacher());
        return ClassroomResponse.from(classroomRepository.save(classroom));
    }

    @Transactional
    public StudentResponse addStudent(Long classroomId, Long studentId) {
        Classroom classroom = findClassroom(classroomId);
        Student student = studentRepository.findById(studentId)
                .orElseThrow(() -> new StudentNotFoundException(studentId));
        student.setClassroom(classroom);
        return StudentResponse.from(student);
    }

    private Classroom findClassroom(Long id) {
        return classroomRepository.findById(id)
                .orElseThrow(() -> new ClassroomNotFoundException(id));
    }
}
```

| Code | Meaning |
|---|---|
| `@Transactional(readOnly = true)` | ⭐ "Keep the database connection open for the **whole** method (only reading)." Needed so `getStudents()` can load the students (Part 6). |
| `@Transactional` | The same, for methods that **change** data. |
| `student.setClassroom(classroom);` | ⭐ Move the student — on the **owner** side 👑. |
| *(no `save(student)`!)* | 😮 Inside a transaction, Hibernate **notices** changes to loaded entities and writes the `UPDATE` **by itself** at the end. ("Dirty checking" 🧹 — Chapter 79.) |

**`controller/ClassroomController.java`**

```java
package com.example.school.controller;

import java.net.URI;
import java.util.List;

import jakarta.validation.Valid;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.school.dto.ClassroomRequest;
import com.example.school.dto.ClassroomResponse;
import com.example.school.dto.StudentResponse;
import com.example.school.service.ClassroomService;

@RestController
@RequestMapping("/api/classrooms")
public class ClassroomController {

    private final ClassroomService classroomService;

    public ClassroomController(ClassroomService classroomService) {
        this.classroomService = classroomService;
    }

    @GetMapping
    public List<ClassroomResponse> getAll() {
        return classroomService.getAll();
    }

    @GetMapping("/{id}")
    public ClassroomResponse getById(@PathVariable Long id) {
        return classroomService.getById(id);
    }

    @PostMapping
    public ResponseEntity<ClassroomResponse> create(@Valid @RequestBody ClassroomRequest request) {
        ClassroomResponse created = classroomService.create(request);
        return ResponseEntity.created(URI.create("/api/classrooms/" + created.id())).body(created);
    }

    @PutMapping("/{classroomId}/students/{studentId}")
    public StudentResponse addStudent(@PathVariable Long classroomId, @PathVariable Long studentId) {
        return classroomService.addStudent(classroomId, studentId);
    }
}
```

`PUT /api/classrooms/{classroomId}/students/{studentId}` — "put **this** student into **this** classroom". A **nested** URL, like we planned in Chapter 46! 🗺️

### ⚠️ One more change: `StudentService`

`StudentResponse.from(...)` now calls `student.getClassroom().getName()` — which needs the database (lazy loading!). So `StudentService` needs transactions too. Put **`@Transactional(readOnly = true)`** on the **class**, and **`@Transactional`** on the methods that **change** data:

```java
@Service
@Transactional(readOnly = true)
public class StudentService {
    ...
    @Transactional
    public StudentResponse create(StudentRequest request) { ... }

    @Transactional
    public StudentResponse replace(Long id, StudentRequest request) { ... }

    @Transactional
    public StudentResponse update(Long id, StudentPatchRequest patch) { ... }

    @Transactional
    public void delete(Long id) { ... }
    ...
}
```

| Code | Meaning |
|---|---|
| `@Transactional(readOnly = true)` on the class | Every method is a **read-only** transaction... |
| `@Transactional` on a method | ...except these, which may **write**. (The method's label wins.) |

---

## ✅ Part 6: Test it

Real answers (fresh database):

`GET /api/students`

```json
[{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12,"classroom":"5A"},{"id":2,"name":"Tom Brown","email":"tom@school.com","age":13,"classroom":"6B"},{"id":3,"name":"Lina Haddad","email":"lina@school.com","age":11,"classroom":"5A"}]
```

`GET /api/classrooms`

```json
[{"id":1,"name":"5A","teacher":"Mrs. Khan","students":["Sara Ahmed","Lina Haddad"]},{"id":2,"name":"6B","teacher":"Mr. Brown","students":["Tom Brown"]}]
```

🎉 The classroom **knows** its students — through the mirror side 🪞!

`POST /api/classrooms` with `{"name":"4C","teacher":"Ms. Lee"}`:

```
HTTP/1.1 201 
Location: /api/classrooms/3

{"id":3,"name":"4C","teacher":"Ms. Lee","students":[]}
```

Move Lina into 4C: `PUT /api/classrooms/3/students/3`

```json
{"id":3,"name":"Lina Haddad","email":"lina@school.com","age":11,"classroom":"4C"}
```

`GET /api/classrooms` now:

```json
[{"id":1,"name":"5A","teacher":"Mrs. Khan","students":["Sara Ahmed"]},{"id":2,"name":"6B","teacher":"Mr. Brown","students":["Tom Brown"]},{"id":3,"name":"4C","teacher":"Ms. Lee","students":["Lina Haddad"]}]
```

✅ Lina **moved** — and we never called `save`! (Dirty checking 🧹.) And a wrong classroom: `PUT /api/classrooms/9/students/1` →

```json
{"detail":"Classroom with id 9 was not found","instance":"/api/classrooms/9/students/1","status":404,"title":"Classroom not found"}
```

---

## 😴 Part 7: Lazy loading and the famous exception

When Hibernate loads a **classroom**, does it also load all its **students**? Not right away! The `@OneToMany` list is **lazy** 😴: Hibernate loads it only **when you use it** (`getStudents()`). The same for our `@ManyToOne(fetch = FetchType.LAZY)`.

| | Lazy 😴 (`LAZY`) | Eager ⚡ (`EAGER`) |
|---|---|---|
| When is the related data loaded? | Only when your code **uses** it | **Always**, immediately |
| Speed | ✅ Fast — loads only what's needed | ❌ Can load **lots** of data you don't need |
| Default for `@OneToMany` | ✅ LAZY | |
| Default for `@ManyToOne` | | ⚡ EAGER (that's why we wrote `LAZY` ourselves!) |

But lazy loading has **one** rule: the database connection must still be **open** when you use the data. 🚪

### 💥 What happens without `@Transactional`?

We **removed** `@Transactional(readOnly = true)` from `ClassroomService.getAll()` to see. `GET /api/classrooms` → **500**! The console:

```
LazyInitializationException: Cannot lazily initialize collection of role 'com.example.school.entity.Classroom.students' with key '1' (no session)
```

"I want to load the students of classroom 1 — but the **session** (the open connection) is already **closed**!" 😱

```
 findAll()      → Hibernate opens a session, loads the classrooms, CLOSES the session 🚪
 ...
 getStudents()  → "Load the students, please!" → 💥 no session anymore!
```

With **`@Transactional`**, the session stays **open** for the **whole** method:

```
 @Transactional getAll() {   ← 🚪 session opens
     findAll()               → loads the classrooms
     getStudents()           → loads the students ✅ (session still open)
 }                           ← 🚪 session closes
```

That's why our services have `@Transactional`. 🛡️ (Chapter 79 explains transactions fully.)

### 🤔 And `spring.jpa.open-in-view=false`?

Spring Boot **could** keep the session open for the **whole** HTTP request (even while Jackson writes the JSON). That's called "**open in view**", and it's **on** by default — Spring Boot warns about it in the log. We turned it **off** (Chapter 69), because it hides problems and keeps database connections busy too long. With it off, **all** database work happens inside the **service**, where it belongs. 🏠

### 🐢 A small warning: "N+1"

Look at the SQL log for `GET /api/students`: 1 query for the students... and then **one more** query **per classroom** (to get its name). For 3 students, no problem. For 10,000 students... 🐢 This is called the **N+1 problem**. Real projects fix it with special queries (`JOIN FETCH`). For now, just know it exists! 🧠

---

## 🔁 Part 8: Never return entities as JSON!

Why do we always use **DTOs**? Here's a scary example. 😱 We made a test endpoint that returns the **entity** `Classroom` directly (with `open-in-view` turned **on**):

```java
@GetMapping("/api/raw/classrooms/{id}")
public Classroom raw(@PathVariable Long id) {
    return classroomRepository.findById(id).orElseThrow();
}
```

Jackson writes the classroom... which has **students**... each student has a **classroom**... which has **students**... which have a **classroom**... 🔁🔁🔁 We got this (shortened a LOT):

```json
{"name":"5A","teacher":"Mrs. Khan","id":1,"students":[{"name":"Sara Ahmed","email":"sara@school.com","age":12,"classroom":{"name":"5A","teacher":"Mrs. Khan","id":1,"students":[{"name":"Sara Ahmed",...,"classroom":{"name":"5A",...
```

...on and on, **500 levels deep**, until Jackson gave up:

```
Document nesting depth (501) exceeds the maximum allowed (500, from `StreamWriteConstraints.getMaxNestingDepth()`)
```

😵 A broken, enormous answer — and the `teacherNote` would have leaked too (Chapter 64)!

**Fix:** ✅ **DTOs.** `ClassroomResponse` has only **names** of students, and `StudentResponse` has only the **name** of the classroom. No loops, no secrets. 🛡️

---

## 💻 Mini project: More classroom endpoints 🏫

1. **`GET /api/classrooms/{id}/students`** → the **full** `StudentResponse` list of one classroom.
2. **`DELETE /api/classrooms/{classroomId}/students/{studentId}`** → take a student **out** of the classroom (`classroom` becomes `null`). Answer **204**. If the student isn't in **that** classroom → **404** with a clear message... or simply ignore it — your choice! (Our answer ignores it.)

<details>
<summary>Click to see the answer</summary>

In **`ClassroomService`**:

```java
@Transactional(readOnly = true)
public List<StudentResponse> getStudents(Long classroomId) {
    return findClassroom(classroomId).getStudents().stream()
            .map(StudentResponse::from)
            .toList();
}

@Transactional
public void removeStudent(Long classroomId, Long studentId) {
    Classroom classroom = findClassroom(classroomId);
    Student student = studentRepository.findById(studentId)
            .orElseThrow(() -> new StudentNotFoundException(studentId));
    if (student.getClassroom() == classroom) {
        student.setClassroom(null);
    }
}
```

In **`ClassroomController`**:

```java
@GetMapping("/{id}/students")
public List<StudentResponse> getStudents(@PathVariable Long id) {
    return classroomService.getStudents(id);
}

@DeleteMapping("/{classroomId}/students/{studentId}")
@ResponseStatus(HttpStatus.NO_CONTENT)
public void removeStudent(@PathVariable Long classroomId, @PathVariable Long studentId) {
    classroomService.removeStudent(classroomId, studentId);
}
```

Test:

- `GET /api/classrooms/1/students` → Sara and Lina, with all their fields.
- `DELETE /api/classrooms/1/students/3` → **204**; then `GET /api/students/3` → `"classroom":null`.

`student.getClassroom() == classroom` works here, because inside **one** transaction, Hibernate gives you the **same** Java object for the same row. 🧠

</details>

---

## ✋ Try it yourself

**Task 1:** Which side is the **owner** in `Student.classroom` / `Classroom.students`? Which line moves Tom into 5A?

<details>
<summary>Click to see the answer</summary>

`Student.classroom` is the owner (it has `@JoinColumn` and the `classroom_id` column). Move Tom with `tom.setClassroom(fiveA);` (inside a transaction).

</details>

**Task 2:** In the `DataLoader`, replace `sara.setClassroom(fiveA)` with `fiveA.getStudents().add(sara)`. What does `GET /api/students` show for Sara?

<details>
<summary>Click to see the answer</summary>

`"classroom": null`! Adding to the **mirror** list 🪞 doesn't write anything to the database — only the **owner** side 👑 (`setClassroom`) fills `classroom_id`. (Change it back! Delete the `data` folder to start fresh.)

</details>

**Task 3:** Why is the `classroom` field in `StudentResponse` a `String` and not a `Classroom`?

<details>
<summary>Click to see the answer</summary>

A `Classroom` object would bring its **students**, who bring their **classroom**... → an endless loop 🔁 (Part 8). And it would show more data than needed. A simple name is short, safe and clear.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Changing only the mirror side

`classroom.getStudents().add(student)` → nothing is saved. **Fix:** `student.setClassroom(classroom)` 👑.

### Mistake 2: `LazyInitializationException`

`Cannot lazily initialize collection ... (no session)`. **Fix:** Do the database work inside a **`@Transactional`** service method, and return **DTOs** (built inside the transaction).

### Mistake 3: Returning entities from controllers

Endless JSON loops 🔁, leaked private fields 🙈, lazy loading errors 😴. **Fix:** Always **DTOs**.

### Mistake 4: Forgetting the `null` check

A student without a classroom → `student.getClassroom().getName()` → `NullPointerException` → 500. **Fix:** `student.getClassroom() != null ? ... : null`.

### Mistake 5: A wrong `mappedBy`

`@OneToMany(mappedBy = "room")` but the field in `Student` is called `classroom` → the app **doesn't start** (Hibernate can't find `room`). **Fix:** `mappedBy` = the **field name** on the owner side.

### Mistake 6: Saving the student before its classroom

The classroom has no id yet → the database can't store `classroom_id`. **Fix:** Save the "one" side (the classroom) **first**.

---

## ✅ Summary

- **One-to-many**: one classroom 🏫 → many students 👥. Seen from the student: **many-to-one**.
- **Owner** 👑 (`Student`): **`@ManyToOne(fetch = FetchType.LAZY)`** + **`@JoinColumn(name = "classroom_id")`** → a **foreign key** column. Change the relationship **here**: `student.setClassroom(...)`.
- **Mirror** 🪞 (`Classroom`): **`@OneToMany(mappedBy = "classroom")`** → no column; used for **reading**.
- Hibernate creates the column **and** the foreign key constraint 🛡️.
- **Lazy loading** 😴 loads related data only when used — but **only** while a session is open. Use **`@Transactional`** in services; otherwise: **`LazyInitializationException`**.
- Inside a transaction, Hibernate saves changes to loaded entities **automatically** (dirty checking 🧹).
- **Never** return entities as JSON (endless loops 🔁) — **DTOs** with names or ids.
- Watch out for **N+1** queries in big lists. 🐢

---

## ❓ Quiz

1. Give an example of a one-to-many relationship (not classrooms!).
2. Which side has `@JoinColumn`? Which side has `mappedBy`?
3. Which column does `@JoinColumn(name = "classroom_id")` create, and in which table?
4. How do you put a student into a classroom in Java?
5. What does `FetchType.LAZY` mean?
6. When does `LazyInitializationException` happen? How do we avoid it?
7. Why do we have `spring.jpa.open-in-view=false`?
8. What happens if you return the `Classroom` entity as JSON?

<details>
<summary>Click to see the answers</summary>

1. For example: one author → many books; one shelf → many books; one mother → many children.
2. The "many" side (`Student.classroom`, the owner) has `@JoinColumn`. The "one" side (`Classroom.students`, the mirror) has `mappedBy`.
3. A column `classroom_id` in the `students` table (a foreign key to `classrooms`).
4. `student.setClassroom(classroom);` — inside a transaction (or followed by `save`).
5. Related data is loaded only when the code uses it, not immediately.
6. When lazy data is used after the database session is closed. Avoid it by doing the work inside a `@Transactional` service method and returning DTOs.
7. So all database work happens inside the service, and connections aren't kept busy during the whole request (and lazy-loading problems show up early).
8. An endless loop: classroom → students → classroom → ... → the JSON breaks (nesting depth error), and private fields may leak.

</details>

---

[⬅ Previous chapter](74-custom-queries.md) | [Table of Contents](../README.md) | [Next chapter: Relationships: Many-to-Many ➡](76-many-to-many.md)
