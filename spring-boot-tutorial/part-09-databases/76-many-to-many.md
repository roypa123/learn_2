# Chapter 76 – Relationships: Many-to-Many

[⬅ Previous chapter](75-one-to-many.md) | [Table of Contents](../README.md) | [Next chapter ➡](77-mysql-postgresql.md)

---

## 🎯 Goal

A student is in **one** classroom. But a student takes **many** courses: Math, Art, Music... 🎨🎵➗ And each course has **many** students. That's a **many-to-many** relationship!

At the end of this chapter you will know:

- What a **many-to-many** relationship is, and why it needs a **third table** (a **join table**)
- How to build it with **`@ManyToMany`**, **`@JoinTable`** and **`mappedBy`**
- Why we use a **`Set`** here
- How to **enroll** a student in a course, and **leave** a course
- A `Course` API: list courses, create a course, the courses of a student, the students of a course
- How to **sort** with `Sort.by(...)`

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Many-to-many** | **Many** students ↔ **many** courses. 👥 ↔ 📚 |
| **Join table** | A **third** table that stores the **pairs**: "student 1 takes course 2". 🔗🔗 |
| **`@ManyToMany`** | The label for a many-to-many relationship. |
| **`@JoinTable`** | Chooses the **name** and the **columns** of the join table. |
| **Composite key** | A primary key made of **two** columns together: `(student_id, course_id)`. |
| **Enroll** | To **sign up** for a course. ✍️ |
| **`Set`** | A collection **without duplicates** (Chapter 32) — perfect: you can't take Math twice! |

---

## 📖 Story: The club sign-up sheets 📋

The school has clubs: **Math club** ➗, **Art club** 🎨, **Music club** 🎵.

- Sara is in the **Math** club **and** the **Art** club.
- Tom is in the **Math** club.
- The **Math** club has Sara **and** Tom.

Where do we write this down? 🤔

- On the **student's** card? Sara's card would need a space for "all my clubs" — how many spaces? 3? 10? 😕
- On the **club's** card? The Math club would need a space for "all members" — 100 spaces? 😕

The school uses a **sign-up sheet**: a list of **pairs**:

```
 ┌─────────┬─────────┐
 │ student │ club    │
 ├─────────┼─────────┤
 │ Sara    │ Math    │
 │ Sara    │ Art     │
 │ Tom     │ Math    │
 └─────────┴─────────┘
```

One line per "student takes club". Easy to add, easy to remove, no limits! ✅ That sheet is a **join table**. 🔗🔗

---

## 🔗🔗 Part 1: Why a third table?

With one-to-many (Chapter 75), the "many" side got a foreign key column (`classroom_id`). But with many-to-many, **both** sides are "many" — a single column on either side can't hold **many** values. 😕

So we use **three** tables:

```
 students                 student_courses (join table)        courses
 ┌────┬─────────────┐     ┌────────────┬───────────┐          ┌────┬───────┐
 │ id │ name        │     │ student_id │ course_id │          │ id │ title │
 ├────┼─────────────┤     ├────────────┼───────────┤          ├────┼───────┤
 │ 1  │ Sara Ahmed  │◄────┤ 1          │ 1         ├─────────►│ 1  │ Math  │
 │ 2  │ Tom Brown   │◄─┐  │ 1          │ 2         ├────┐     │ 2  │ Art   │
 │ 3  │ Lina Haddad │  └──┤ 2          │ 1         │    └────►│ 3  │ Music │
 └────┴─────────────┘     └────────────┴───────────┘          └────┴───────┘
```

Each row in **`student_courses`** says: "**this** student takes **that** course". 🔗

---

## 📚 Part 2: The `Course` entity

Create **`entity/Course.java`**:

```java
package com.example.school.entity;

import java.util.HashSet;
import java.util.Set;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.Table;

@Entity
@Table(name = "courses")
public class Course {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 50)
    private String title;

    @ManyToMany(mappedBy = "courses")
    private Set<Student> students = new HashSet<>();

    protected Course() {
    }

    public Course(String title) {
        this.title = title;
    }

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public Set<Student> getStudents() {
        return students;
    }
}
```

| Code | Meaning |
|---|---|
| `@ManyToMany(mappedBy = "courses")` | ⭐ "Many courses ↔ many students. The **other** side (the field `courses` in `Student`) stores it." This is the **mirror** 🪞. |
| `Set<Student> students = new HashSet<>()` | A **`Set`** (Chapter 32): no duplicates — a student can't be in a course twice. Start **empty**. |

---

## 🧑‍🎓 Part 3: The owner side — `Student.courses`

Add this field to the **`Student`** entity, plus a getter:

```java
@ManyToMany
@JoinTable(name = "student_courses",
        joinColumns = @JoinColumn(name = "student_id"),
        inverseJoinColumns = @JoinColumn(name = "course_id"))
private Set<Course> courses = new HashSet<>();
```

```java
public Set<Course> getCourses() {
    return courses;
}
```

(Imports: `java.util.HashSet`, `java.util.Set`, `jakarta.persistence.JoinTable`, `jakarta.persistence.ManyToMany`.)

| Code | Meaning |
|---|---|
| `@ManyToMany` | ⭐ The **owner** side 👑 (no `mappedBy`). Changes **here** are saved! |
| `@JoinTable(name = "student_courses", ...)` | ⭐ The join table is called `student_courses`. |
| `joinColumns = @JoinColumn(name = "student_id")` | The column that points to **this** side (the student). |
| `inverseJoinColumns = @JoinColumn(name = "course_id")` | The column that points to the **other** side (the course). |
| `Set<Course> courses = new HashSet<>()` | The courses this student takes. |

### 👀 The tables Hibernate builds

Real output (delete the `data` folder and restart):

```sql
create table courses (
    id bigint generated by default as identity,
    title varchar(50) not null,
    primary key (id)
)

create table student_courses (
    student_id bigint not null,
    course_id bigint not null,
    primary key (student_id, course_id)
)

alter table if exists student_courses
   add constraint FKsfpq78oyrqua1h0obpl7ulc18
   foreign key (course_id)
   references courses

alter table if exists student_courses
   add constraint FKwj1l0mta35u161acdl2tupoo
   foreign key (student_id)
   references students
```

| SQL | Meaning |
|---|---|
| `create table student_courses` | ⭐ The join table — Hibernate made it from `@JoinTable`! You **don't** need an entity for it. |
| `primary key (student_id, course_id)` | A **composite key**: the **pair** must be unique. (Sara can't take Math twice! 🛡️) |
| two `foreign key` constraints | Both columns must point to **real** rows. 🔗🔗 |

---

## 🌱 Part 4: Starting data

Create **`repository/CourseRepository.java`**:

```java
package com.example.school.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.school.entity.Course;

public interface CourseRepository extends JpaRepository<Course, Long> {
}
```

In the **`DataLoader`**, inject `CourseRepository` too, and add courses (inside `run`, after the classrooms):

```java
Course math = courseRepository.save(new Course("Math"));
Course art = courseRepository.save(new Course("Art"));
courseRepository.save(new Course("Music"));

Student sara = new Student("Sara Ahmed", "sara@school.com", 12);
sara.setClassroom(fiveA);
sara.getCourses().add(math);
sara.getCourses().add(art);

Student tom = new Student("Tom Brown", "tom@school.com", 13);
tom.setClassroom(sixB);
tom.getCourses().add(math);
```

(Lina takes no courses yet.) And the message:

```java
System.out.println("DataLoader: added 2 classrooms, 3 courses and 3 students");
```

| Code | Meaning |
|---|---|
| `sara.getCourses().add(math);` | ⭐ Add a course on the **owner** side 👑 → when Sara is saved, Hibernate writes a row into `student_courses`: `(1, 1)`. |

---

## 📦 Part 5: DTOs, service and controller

### DTOs

**`dto/CourseRequest.java`**

```java
package com.example.school.dto;

import jakarta.validation.constraints.NotBlank;

public record CourseRequest(@NotBlank(message = "Title is required") String title) {
}
```

**`dto/CourseResponse.java`**

```java
package com.example.school.dto;

import com.example.school.entity.Course;

public record CourseResponse(Long id, String title, int studentCount) {

    public static CourseResponse from(Course course) {
        return new CourseResponse(course.getId(), course.getTitle(), course.getStudents().size());
    }
}
```

| Code | Meaning |
|---|---|
| `int studentCount` | Not the whole student list — just **how many** (short and safe; no loops 🔁). |
| `course.getStudents().size()` | Uses the **mirror** side 🪞 — lazy loading, so we need a transaction (Chapter 75). |

### The exception

**`exception/CourseNotFoundException.java`**

```java
package com.example.school.exception;

public class CourseNotFoundException extends RuntimeException {

    public CourseNotFoundException(Long id) {
        super("Course with id " + id + " was not found");
    }
}
```

...and a handler in `GlobalExceptionHandler`, like the classroom one (title `"Course not found"`, status 404).

### The service

**`service/CourseService.java`**

```java
package com.example.school.service;

import java.util.List;

import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.school.dto.CourseRequest;
import com.example.school.dto.CourseResponse;
import com.example.school.dto.StudentResponse;
import com.example.school.entity.Course;
import com.example.school.entity.Student;
import com.example.school.exception.CourseNotFoundException;
import com.example.school.exception.StudentNotFoundException;
import com.example.school.repository.CourseRepository;
import com.example.school.repository.StudentRepository;

@Service
public class CourseService {

    private final CourseRepository courseRepository;
    private final StudentRepository studentRepository;

    public CourseService(CourseRepository courseRepository, StudentRepository studentRepository) {
        this.courseRepository = courseRepository;
        this.studentRepository = studentRepository;
    }

    @Transactional(readOnly = true)
    public List<CourseResponse> getAll() {
        return courseRepository.findAll(Sort.by("title")).stream()
                .map(CourseResponse::from)
                .toList();
    }

    @Transactional
    public CourseResponse create(CourseRequest request) {
        return CourseResponse.from(courseRepository.save(new Course(request.title())));
    }

    @Transactional(readOnly = true)
    public List<StudentResponse> getStudents(Long courseId) {
        return findCourse(courseId).getStudents().stream()
                .map(StudentResponse::from)
                .toList();
    }

    @Transactional(readOnly = true)
    public List<CourseResponse> getCoursesOf(Long studentId) {
        return findStudent(studentId).getCourses().stream()
                .map(CourseResponse::from)
                .toList();
    }

    @Transactional
    public List<CourseResponse> enroll(Long studentId, Long courseId) {
        Student student = findStudent(studentId);
        Course course = findCourse(courseId);
        student.getCourses().add(course);
        course.getStudents().add(student);
        return student.getCourses().stream()
                .map(CourseResponse::from)
                .toList();
    }

    @Transactional
    public void leave(Long studentId, Long courseId) {
        Student student = findStudent(studentId);
        Course course = findCourse(courseId);
        student.getCourses().remove(course);
        course.getStudents().remove(student);
    }

    private Student findStudent(Long id) {
        return studentRepository.findById(id)
                .orElseThrow(() -> new StudentNotFoundException(id));
    }

    private Course findCourse(Long id) {
        return courseRepository.findById(id)
                .orElseThrow(() -> new CourseNotFoundException(id));
    }
}
```

### 🔍 The interesting lines

| Code | Meaning |
|---|---|
| `courseRepository.findAll(Sort.by("title"))` | ⭐ `findAll` **with sorting**: by the field `title`, A → Z. (Without it, the order is **not** guaranteed — we really got Art, Math, Music in a strange order before adding it! Chapter 68.) |
| `student.getCourses().add(course);` | ⭐ **Enroll** — on the **owner** side 👑 → Hibernate inserts a row into `student_courses`. |
| `course.getStudents().add(student);` | Also update the **mirror** 🪞 — so that `studentCount` in the answer is **right** immediately. (It's not saved — only the owner is.) |
| `student.getCourses().remove(course);` | **Leave** → Hibernate **deletes** the row from `student_courses`. |
| *(no `save`!)* | Dirty checking 🧹 inside `@Transactional` (Chapter 75). |

> 💡 **Keep both sides in sync.** Change the **owner** (to save) **and** the **mirror** (so your Java objects are correct right now). It's a good habit. 🤝

### The controller

**`controller/CourseController.java`**

```java
package com.example.school.controller;

import java.net.URI;
import java.util.List;

import jakarta.validation.Valid;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.example.school.dto.CourseRequest;
import com.example.school.dto.CourseResponse;
import com.example.school.dto.StudentResponse;
import com.example.school.service.CourseService;

@RestController
public class CourseController {

    private final CourseService courseService;

    public CourseController(CourseService courseService) {
        this.courseService = courseService;
    }

    @GetMapping("/api/courses")
    public List<CourseResponse> getAll() {
        return courseService.getAll();
    }

    @PostMapping("/api/courses")
    public ResponseEntity<CourseResponse> create(@Valid @RequestBody CourseRequest request) {
        CourseResponse created = courseService.create(request);
        return ResponseEntity.created(URI.create("/api/courses/" + created.id())).body(created);
    }

    @GetMapping("/api/courses/{courseId}/students")
    public List<StudentResponse> getStudents(@PathVariable Long courseId) {
        return courseService.getStudents(courseId);
    }

    @GetMapping("/api/students/{studentId}/courses")
    public List<CourseResponse> getCoursesOf(@PathVariable Long studentId) {
        return courseService.getCoursesOf(studentId);
    }

    @PutMapping("/api/students/{studentId}/courses/{courseId}")
    public List<CourseResponse> enroll(@PathVariable Long studentId, @PathVariable Long courseId) {
        return courseService.enroll(studentId, courseId);
    }

    @DeleteMapping("/api/students/{studentId}/courses/{courseId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void leave(@PathVariable Long studentId, @PathVariable Long courseId) {
        courseService.leave(studentId, courseId);
    }
}
```

| Endpoint | Meaning |
|---|---|
| `GET /api/courses` | All courses, A → Z, with the number of students |
| `POST /api/courses` | Create a course |
| `GET /api/courses/{courseId}/students` | Who takes this course? |
| `GET /api/students/{studentId}/courses` | Which courses does this student take? |
| `PUT /api/students/{studentId}/courses/{courseId}` | Enroll ✍️ (PUT, because doing it twice has the same result — idempotent! Chapter 61) |
| `DELETE /api/students/{studentId}/courses/{courseId}` | Leave the course 👋 |

> 💡 No `@RequestMapping` on the class, because the paths start differently (`/api/courses/...` and `/api/students/...`). Both are fine REST style (Chapter 46). 😊

---

## ✅ Part 6: Test it

Real answers (fresh database):

`GET /api/courses`

```json
[{"id":2,"title":"Art","studentCount":1},{"id":1,"title":"Math","studentCount":2},{"id":3,"title":"Music","studentCount":0}]
```

Sorted by **title** ✅. Math has 2 students (Sara, Tom), Art has 1 (Sara).

`GET /api/students/1/courses` (Sara)

```json
[{"id":2,"title":"Art","studentCount":1},{"id":1,"title":"Math","studentCount":2}]
```

`GET /api/courses/1/students` (Math)

```json
[{"id":2,"name":"Tom Brown","email":"tom@school.com","age":13,"classroom":"6B"},{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12,"classroom":"5A"}]
```

> 💡 The order inside these lists can be different on your computer — a **`Set`** has **no** order (Chapter 32). If the order matters, sort the stream: `.sorted(Comparator.comparing(StudentResponse::name))`.

Lina enrolls in **Music** (3), then **Math** (1):

`PUT /api/students/3/courses/3`

```json
[{"id":3,"title":"Music","studentCount":1}]
```

`PUT /api/students/3/courses/1`

```json
[{"id":3,"title":"Music","studentCount":1},{"id":1,"title":"Math","studentCount":3}]
```

Math now has **3** students! 🎉 And Sara leaves Art: `DELETE /api/students/1/courses/2` → **204**. Then `GET /api/courses`:

```json
[{"id":2,"title":"Art","studentCount":0},{"id":1,"title":"Math","studentCount":3},{"id":3,"title":"Music","studentCount":1}]
```

✅ And a course that doesn't exist: `PUT /api/students/3/courses/99` →

```json
{"detail":"Course with id 99 was not found","instance":"/api/students/3/courses/99","status":404,"title":"Course not found"}
```

### 👀 Look in the console

`SELECT * FROM student_courses;` in the H2 Console shows the **pairs** — just like the sign-up sheet in the story! 📋

---

## 🗺️ Part 7: The three relationship types

| Type | Example | How it's stored | JPA labels |
|---|---|---|---|
| **One-to-one** | One student ↔ one locker 🔐 | A foreign key in **one** of the tables | `@OneToOne` + `@JoinColumn` |
| **One-to-many** / **many-to-one** | One classroom → many students | A foreign key on the **"many"** side | `@ManyToOne` + `@JoinColumn`, and `@OneToMany(mappedBy = ...)` |
| **Many-to-many** | Students ↔ courses | A **join table** with two foreign keys | `@ManyToMany` + `@JoinTable`, and `@ManyToMany(mappedBy = ...)` |

> 💡 **When the pair needs more information** — like a **grade** ("Sara got an A in Math") — a simple join table isn't enough. Then you make the join table a **real entity** (`Enrollment` with `student`, `course`, `grade`), with **two** `@ManyToOne` relationships. That's a common next step in real apps! 🎓

---

## 💻 Mini project: Popular courses 🌟

Add **`GET /api/courses/popular?min=2`** → the courses with **at least** `min` students (default **2**).

Use a **JPQL** query (Chapter 74) in `CourseRepository`. Tip: JPQL has a function **`SIZE(...)`** that counts the items of a collection!

<details>
<summary>Click to see the answer</summary>

**`CourseRepository`**:

```java
@Query("SELECT c FROM Course c WHERE SIZE(c.students) >= :min ORDER BY c.title")
List<Course> findPopular(int min);
```

**`CourseService`**:

```java
@Transactional(readOnly = true)
public List<CourseResponse> getPopular(int min) {
    return courseRepository.findPopular(min).stream()
            .map(CourseResponse::from)
            .toList();
}
```

**`CourseController`**:

```java
@GetMapping("/api/courses/popular")
public List<CourseResponse> getPopular(@RequestParam(defaultValue = "2") int min) {
    return courseService.getPopular(min);
}
```

With the starting data: `GET /api/courses/popular` →

```json
[{"id":1,"title":"Math","studentCount":2}]
```

and `GET /api/courses/popular?min=1` → Art and Math. (`SIZE(c.students)` becomes a `count(...)` in the SQL — look at the log! 👀)

⚠️ `/api/courses/popular` is a fixed word, so it doesn't clash with other paths. (And we have no `/api/courses/{id}` — but even if we had, the fixed word would win. Chapter 58!)

</details>

---

## ✋ Try it yourself

**Task 1:** Enroll Tom (2) in Math (1) **again**. What happens? Why?

<details>
<summary>Click to see the answer</summary>

Nothing changes — Tom is already in Math, and a **`Set`** ignores duplicates. The answer still lists Math once. (And the join table's composite primary key would refuse a duplicate pair anyway! 🛡️) That's why PUT is the right method — doing it twice is the same as once.

</details>

**Task 2:** In `enroll`, remove the line `course.getStudents().add(student);`. Is the enrollment still saved? What's wrong in the answer?

<details>
<summary>Click to see the answer</summary>

Yes, it's **saved** — the owner side (`student.getCourses()`) is what counts. But the `studentCount` in the answer may be **too small**, because the mirror list in memory wasn't updated. After the next request (new transaction), the count is right again. That's why we update **both** sides. 🤝

</details>

**Task 3:** Which relationship type? a) a book and its author (one author per book) b) a student and their school ID card c) teachers and subjects (teachers teach many subjects, subjects have many teachers)

<details>
<summary>Click to see the answer</summary>

a) Many-to-one (many books → one author) b) One-to-one c) Many-to-many

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Changing only the mirror

`course.getStudents().add(student)` alone → nothing saved. **Fix:** Change the owner: `student.getCourses().add(course)` 👑 (and the mirror too, for correct objects).

### Mistake 2: `mappedBy` on both sides — or on none

Both sides with `mappedBy` → no owner → nothing is saved (or an error). No `mappedBy` at all → Hibernate creates **two** join tables! 😵 **Fix:** Exactly **one** side has `mappedBy`.

### Mistake 3: A `List` and duplicates

With a `List`, adding the same course twice can cause duplicate-key errors in the join table. **Fix:** Use a **`Set`** for many-to-many.

### Mistake 4: Returning entity sets as JSON

`Student` → `courses` → `students` → `courses`... 🔁 **Fix:** DTOs (`CourseResponse` with a **count**).

### Mistake 5: Forgetting `@Transactional`

`course.getStudents().size()` outside a transaction → `LazyInitializationException` (Chapter 75). **Fix:** `@Transactional` in the service.

---

## ✅ Summary

- **Many-to-many**: many students ↔ many courses. It needs a **join table** with **two** foreign keys and a **composite primary key** `(student_id, course_id)`. 🔗🔗
- **Owner** 👑 (`Student.courses`): **`@ManyToMany`** + **`@JoinTable(name = "student_courses", joinColumns = ..., inverseJoinColumns = ...)`**.
- **Mirror** 🪞 (`Course.students`): **`@ManyToMany(mappedBy = "courses")`**.
- Use a **`Set`** (no duplicates) and start with an empty `new HashSet<>()`.
- **Enroll** = `student.getCourses().add(course)`; **leave** = `remove(course)`. Update the mirror too, inside **`@Transactional`**.
- **`findAll(Sort.by("title"))`** sorts — without `ORDER BY`, the order is not guaranteed.
- The three types: **one-to-one**, **one-to-many / many-to-one**, **many-to-many**. If a pair needs extra data (a grade), make the join table an **entity**.

---

## ❓ Quiz

1. Give an example of a many-to-many relationship.
2. Why can't a many-to-many relationship be stored with one foreign key column?
3. What's in the join table `student_courses`?
4. What is a composite key?
5. Which side has `@JoinTable`? Which side has `mappedBy`?
6. Why do we use a `Set` and not a `List`?
7. How do you enroll a student in a course in Java?
8. What would you do if each enrollment needs a grade?

<details>
<summary>Click to see the answers</summary>

1. For example: students ↔ courses, books ↔ readers, teachers ↔ subjects.
2. Because both sides have "many": one column can only hold **one** value per row.
3. Pairs of ids: `student_id` and `course_id` — one row per "this student takes that course".
4. A primary key made of two (or more) columns together, like `(student_id, course_id)`.
5. The owner (`Student.courses`) has `@JoinTable`; the mirror (`Course.students`) has `mappedBy`.
6. A `Set` has no duplicates — a student can't take the same course twice.
7. `student.getCourses().add(course);` (and `course.getStudents().add(student);`) inside a `@Transactional` method.
8. Make the join table a real entity (like `Enrollment`) with two `@ManyToOne` relationships and a `grade` field.

</details>

---

[⬅ Previous chapter](75-one-to-many.md) | [Table of Contents](../README.md) | [Next chapter: Using MySQL or PostgreSQL ➡](77-mysql-postgresql.md)
