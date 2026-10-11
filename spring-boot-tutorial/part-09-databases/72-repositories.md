# Chapter 72 – Repositories: save, find, delete

[⬅ Previous chapter](71-entities.md) | [Table of Contents](../README.md) | [Next chapter ➡](73-crud-student-app.md)

---

## 🎯 Goal

Remember the promise from **Chapter 63**? 🤫 "In Part 9, you'll replace the whole `StudentRepository` class with **one line**." Today is the day! 🎉

At the end of this chapter you will know:

- How to write a **repository interface** with **`JpaRepository`** — one line 🤯
- **Who** writes the code behind it (spoiler: Spring Data, at startup)
- The ready-made methods: **`save`**, **`saveAll`**, **`findById`**, **`findAll`**, **`count`**, **`existsById`**, **`deleteById`**...
- The **SQL** Hibernate sends for each one 👀
- How `save` knows if it should **insert** or **update**
- How to try things at startup with a **`CommandLineRunner`** 🏃

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Repository** | The class (or interface) that **stores and finds** entities. The "storage room" 🧊 (Chapter 63). |
| **`JpaRepository<T, ID>`** | A Spring Data interface with **all** the usual database methods, ready to use. |
| **Proxy** | An object that Spring **creates for you** at startup, to stand in for your interface. 🎭 |
| **`CommandLineRunner`** | An interface with a `run` method that Spring calls **once**, right after the app starts. 🏃 |
| **Insert** / **Update** | Adding a **new** row / changing an **existing** row. |
| **Merge** | JPA's word for "take this object and make the database match it". |

---

## 📖 Story: The magic genie 🧞

You find a magic lamp. 🪔 A genie comes out and says:

"Just **write down** what you want on a piece of paper. I'll make it happen."

You write: *"I want a storage room for **Students**, whose numbers are **Longs**."* ✍️

The genie snaps his fingers 🫰 — and there's a complete storage room, with workers who can **save**, **find**, **count** and **delete** students. You never built anything. You just **described** it.

That's **Spring Data JPA**:

| Story | Spring |
|---|---|
| The piece of paper ✍️ | Your **interface** `StudentRepository extends JpaRepository<Student, Long>` |
| The genie 🧞 | **Spring Data** |
| The storage room with workers | A **proxy** object that Spring creates at startup 🎭 |

---

## 🧹 Part 1: Make room — rename the old repository

Our map-based class from Chapter 63 is called `StudentRepository`, in the package `repository`. The new interface needs that name! So, like in Chapter 71:

1. Open **`repository/StudentRepository.java`** (the class with the `LinkedHashMap`).
2. Click on the class name, press **Shift + F6**, type **`OldStudentRepository`**, press **Enter**.

IntelliJ updates the service too. The API still works. ✅ (It goes in the 🗑️ in Chapter 73.)

---

## ✨ Part 2: The one-line repository

Create a new **interface** in the `repository` package: right-click → **New → Java Class** → choose **Interface** → **`StudentRepository`**:

```java
package com.example.school.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.school.entity.Student;

public interface StudentRepository extends JpaRepository<Student, Long> {
}
```

That's it. **That's the whole repository.** 🤯

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `public interface StudentRepository` | An **interface** (Chapter 25) — only a promise, no code. |
| `extends JpaRepository<...>` | ⭐ "I want **everything** that `JpaRepository` offers." (Interfaces can extend other interfaces.) |
| `<Student, Long>` | **Generics** (Chapter 34): "for the entity **`Student`**, whose id is a **`Long`**." |
| `{ }` | Empty! We don't add anything (yet — Chapter 74). |
| *(no `@Repository` label)* | Not needed — Spring Data finds interfaces that extend `JpaRepository` by itself. |

### 🧞 But... who writes the code?

An interface has **no code**. So who does the real work when you call `save(...)`? 🤔

**Spring Data**, at **startup**. Look at the log:

```
... Bootstrapping Spring Data JPA repositories in DEFAULT mode.
... Finished Spring Data repository scanning in 112 ms. Found 1 JPA repository interface.
```

"**Found 1 JPA repository interface**" — that's yours! 🎉 (In Chapter 69 it said "Found 0".) Spring Data then creates an object — a **proxy** 🎭 — that **implements** your interface, and puts it into the container as a **bean** (Chapter 54). When you ask for a `StudentRepository` in a constructor (Chapter 53), you get that proxy. 💉

```
   You write:                          Spring Data creates at startup:
   ┌─────────────────────────┐         ┌──────────────────────────────────┐
   │ interface               │  🧞     │ 🎭 a proxy (a bean)               │
   │ StudentRepository       │ ──────► │   save(...)     → INSERT/UPDATE  │
   │   extends JpaRepository │         │   findById(...) → SELECT ...     │
   │   <Student, Long> { }   │         │   findAll()     → SELECT ...     │
   └─────────────────────────┘         │   deleteById()  → DELETE ...     │
                                       └──────────────────────────────────┘
```

---

## 🧰 Part 3: The ready-made methods

`JpaRepository` gives you **lots** of methods. The most important ones:

| Method | Returns | What it does | SQL |
|---|---|---|---|
| `save(student)` | the saved `Student` | **Insert** a new one, or **update** an existing one | `INSERT` or `UPDATE` |
| `saveAll(list)` | a `List<Student>` | Save many | many `INSERT`s |
| `findById(id)` | `Optional<Student>` | Find one by id (maybe empty — Chapter 37) | `SELECT ... WHERE id=?` |
| `findAll()` | `List<Student>` | All of them | `SELECT ...` |
| `count()` | `long` | How many? | `SELECT count(*)` |
| `existsById(id)` | `boolean` | Is it there? | `SELECT count(*) ... WHERE id=?` |
| `deleteById(id)` | nothing | Delete one | `DELETE ... WHERE id=?` |
| `delete(student)` | nothing | Delete this object | `DELETE` |
| `deleteAll()` | nothing | Delete **all** ⚠️ | `DELETE` |
| `findAll(Sort)` | `List<Student>` | All, sorted | `... ORDER BY` (Chapter 76) |
| `findAll(Pageable)` | `Page<Student>` | One page | `... OFFSET ... FETCH` (Chapter 78) |

Look at the names: **`findAll`, `findById`, `save`, `existsById`, `deleteById`**... the **same names** we used in our map repository in Chapter 63! That's why the service will hardly need to change. 🔌✨

---

## 🏃 Part 4: Try it — a repository playground

Let's **try** every method and **watch** the SQL. We'll use a **`CommandLineRunner`**: a bean whose `run` method Spring calls **once**, right after the app has started. 🏃

First, **delete** `src/main/resources/data.sql` — the playground adds its own students.

Then create **`RepositoryPlayground.java`** in `com.example.school`:

```java
package com.example.school;

import java.util.List;
import java.util.Optional;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import com.example.school.entity.Student;
import com.example.school.repository.StudentRepository;

@Component
public class RepositoryPlayground implements CommandLineRunner {

    private final StudentRepository studentRepository;

    public RepositoryPlayground(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    @Override
    public void run(String... args) {
        System.out.println("=== 1. save");
        Student sara = studentRepository.save(new Student("Sara Ahmed", "sara@school.com", 12));
        Student tom = studentRepository.save(new Student("Tom Brown", "tom@school.com", 13));
        System.out.println("Sara got the id " + sara.getId() + ", Tom got the id " + tom.getId());

        System.out.println("=== 2. count");
        System.out.println("Students in the database: " + studentRepository.count());

        System.out.println("=== 3. findById");
        Optional<Student> found = studentRepository.findById(2L);
        System.out.println("Found: " + found.map(Student::getName).orElse("nobody"));
        System.out.println("Student 99: " + studentRepository.findById(99L).map(Student::getName).orElse("nobody"));

        System.out.println("=== 4. findAll");
        List<Student> all = studentRepository.findAll();
        for (Student student : all) {
            System.out.println(student.getId() + " " + student.getName() + " (" + student.getAge() + ")");
        }

        System.out.println("=== 5. update with save");
        tom.setEmail("tom.brown@school.com");
        studentRepository.save(tom);

        System.out.println("=== 6. existsById and deleteById");
        System.out.println("Exists 1? " + studentRepository.existsById(1L));
        studentRepository.deleteById(1L);
        System.out.println("Exists 1 after delete? " + studentRepository.existsById(1L));
        System.out.println("Students now: " + studentRepository.count());
    }
}
```

### 🔍 The new parts

| Code | Meaning |
|---|---|
| `implements CommandLineRunner` | ⭐ "Spring, call my `run` method once after startup." |
| `@Component` | It's a bean, so Spring finds it (and injects the repository 💉). |
| `public void run(String... args)` | The method Spring calls. (`String...` = any number of texts — the command-line arguments.) |
| `studentRepository.save(new Student(...))` | Save a **new** student. It **returns** the saved object — now **with** an id! |
| `found.map(Student::getName).orElse("nobody")` | `Optional` tricks (Chapter 37): the name if found, otherwise "nobody". |

---

## 👀 Part 5: Watch the SQL

Restart, and read the console **slowly**. Every Java line becomes SQL. (These are **real** outputs. We removed some empty lines.)

### 1️⃣ `save` a new student → `INSERT`

```
=== 1. save
Hibernate: 
    insert 
    into
        students
        (age, created_at, email, name, teacher_note, id) 
    values
        (?, ?, ?, ?, ?, default)
Hibernate: 
    insert 
    into
        students
        (age, created_at, email, name, teacher_note, id) 
    values
        (?, ?, ?, ?, ?, default)
Sara got the id 1, Tom got the id 2
```

- `?` placeholders — no SQL injection (Chapter 70)! 🛡️
- `id` gets **`default`** → the database creates it. And `save` gives us back the object **with** its id: **1** and **2**. 🔢

### 2️⃣ `count` → `select count(*)`

```
=== 2. count
Hibernate: 
    select
        count(*) 
    from
        students s1_0
Students in the database: 2
```

(`s1_0` is a short **nickname** Hibernate gives the table inside the query. Like `AS` in Chapter 68.)

### 3️⃣ `findById` → `SELECT ... WHERE id=?`

```
=== 3. findById
Hibernate: 
    select
        s1_0.id,
        s1_0.age,
        s1_0.created_at,
        s1_0.email,
        s1_0.name,
        s1_0.teacher_note 
    from
        students s1_0 
    where
        s1_0.id=?
Found: Tom Brown
```

…and for id 99, the same SELECT finds nothing → `Student 99: nobody`. No exception — just an **empty `Optional`**. 👍

### 4️⃣ `findAll` → `SELECT` without `WHERE`

```
=== 4. findAll
Hibernate: 
    select
        s1_0.id,
        ...
    from
        students s1_0
1 Sara Ahmed (12)
2 Tom Brown (13)
```

### 5️⃣ `save` an existing student → `SELECT` + `UPDATE`

```
=== 5. update with save
Hibernate: 
    select
        s1_0.id,
        ...
    from
        students s1_0 
    where
        s1_0.id=?
Hibernate: 
    update
        students 
    set
        age=?,
        email=?,
        name=?,
        teacher_note=? 
    where
        id=?
```

😮 Interesting! How did `save` know that Tom is **not** new?

| The object's id is... | `save` does... |
|---|---|
| **`null`** (never saved) | **INSERT** — a new row |
| **a number** (2) | **merge**: first a `SELECT` to load the row, then an **UPDATE** with the changes |

That's why `Long id` (which can be `null`) is so important! 🔑 And look: the `UPDATE` doesn't include `created_at` — remember `updatable = false` from Chapter 71? 🛡️

### 6️⃣ `existsById` + `deleteById`

```
=== 6. existsById and deleteById
Hibernate: 
    select
        count(*) 
    from
        students s1_0 
    where
        s1_0.id=?
Exists 1? true
Hibernate: 
    select
        ...
    where
        s1_0.id=?
Hibernate: 
    delete 
    from
        students 
    where
        id=?
...
Exists 1 after delete? false
...
Students now: 1
```

`deleteById` first **loads** the student (`SELECT`), then **deletes** it. ✅

### 🗺️ Java → SQL, all together

| Java | SQL |
|---|---|
| `save(new Student(...))` | `insert into students (...) values (?, ?, ?, ?, ?, default)` |
| `count()` | `select count(*) from students` |
| `findById(2L)` | `select ... from students where id=?` |
| `findAll()` | `select ... from students` |
| `save(tom)` (has an id) | `select ... where id=?` + `update students set ... where id=?` |
| `existsById(1L)` | `select count(*) from students where id=?` |
| `deleteById(1L)` | `select ... where id=?` + `delete from students where id=?` |

You wrote **zero** SQL — and **zero** repository code. 🧞✨

---

## 🧹 Part 6: Clean up

The playground was just for learning. **Delete `RepositoryPlayground.java`** now — otherwise, it runs at **every** start. 🗑️

(If you also want to keep `show-sql` quieter later, you can set it to `false`. For learning, keep it `true` — seeing the SQL is super useful! 👀)

---

## 💻 Mini project: The `BookRepository` 📚

1. Create **`repository/BookRepository`** for your `Book` entity from Chapter 71. (Tip: if you still have the Part 8 map class with that name, rename it to `OldBookRepository` first.)
2. Write a **`BookPlayground`** (a `CommandLineRunner`) that:
   - saves Matilda, The Hobbit and Charlotte's Web (with shelves `A-1`, `F-7`, `C-3`),
   - prints how many books there are,
   - finds book **3** and prints its title,
   - changes The Hobbit's shelf... wait — `Book` has no `setShelf`! 🤔 Change its **year** to **1938** instead, and save it,
   - prints all books with their years.

<details>
<summary>Click to see the answer</summary>

```java
package com.example.school.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.school.entity.Book;

public interface BookRepository extends JpaRepository<Book, Long> {
}
```

```java
package com.example.school;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import com.example.school.entity.Book;
import com.example.school.repository.BookRepository;

@Component
public class BookPlayground implements CommandLineRunner {

    private final BookRepository bookRepository;

    public BookPlayground(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    @Override
    public void run(String... args) {
        bookRepository.save(new Book("Matilda", "Roald Dahl", 1988, "A-1"));
        Book hobbit = bookRepository.save(new Book("The Hobbit", "J.R.R. Tolkien", 1937, "F-7"));
        bookRepository.save(new Book("Charlotte's Web", "E.B. White", 1952, "C-3"));

        System.out.println("Books: " + bookRepository.count());
        System.out.println("Book 3: " + bookRepository.findById(3L).map(Book::getTitle).orElse("none"));

        hobbit.setYear(1938);
        bookRepository.save(hobbit);

        for (Book book : bookRepository.findAll()) {
            System.out.println(book.getTitle() + " (" + book.getYear() + ")");
        }
    }
}
```

Output (between the SQL lines):

```
Books: 3
Book 3: Charlotte's Web
Matilda (1988)
The Hobbit (1938)
Charlotte's Web (1952)
```

Delete the playground when you're done! 🧹

</details>

---

## ✋ Try it yourself

**Task 1:** In the playground, add `studentRepository.deleteById(42L);` (an id that doesn't exist). What happens?

<details>
<summary>Click to see the answer</summary>

Nothing breaks — Spring Data first looks for student 42, finds nobody, and simply does **nothing**. No exception. (That's why our service checks `existsById` **first**, so it can answer **404** — Chapter 73.)

</details>

**Task 2:** What's the difference between `findById(5L)` returning an empty `Optional`, and throwing an exception?

<details>
<summary>Click to see the answer</summary>

`findById` **never** throws for "not found" — it returns an **empty** `Optional`. **You** decide what to do: return 404, use a default, etc. In our service: `.orElseThrow(() -> new StudentNotFoundException(id))`.

</details>

**Task 3:** Save a student with an email that's **already** used (`sara@school.com`) in the playground. What happens? Why?

<details>
<summary>Click to see the answer</summary>

The `INSERT` fails with a **unique constraint** violation (`Unique index or primary key violation ... EMAIL`). The **database** protects the `unique = true` rule from the entity! 🛡️ (In the API, our service checks the email first and answers **409** — but the database is the second safety net.)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Writing a class that implements the repository

```java
public class StudentRepositoryImpl implements StudentRepository { ... }   // ❌ not needed!
```

**Fix:** Just the **interface**. Spring Data writes the implementation. 🧞

### Mistake 2: Wrong id type in the generics

```java
public interface StudentRepository extends JpaRepository<Student, Integer> { }   // ❌ id is a Long!
```

The app **fails at startup** (the id types don't match). **Fix:** The second type must be the **type of the `@Id` field**: `Long`.

### Mistake 3: Forgetting that `save` returns the saved object

```java
Student student = new Student(...);
studentRepository.save(student);
```

Here this happens to work, because `IDENTITY` puts the id into the same object. But for **updates**, `save` may return a **different** object (from the merge). **Fix:** Always use the **returned** object: `Student saved = studentRepository.save(student);`.

### Mistake 4: Leaving the playground in your project

It runs at **every** start and adds students again and again (or fails on the unique email!). **Fix:** Delete it after learning. 🧹

### Mistake 5: Two classes called `StudentRepository`

The old class and the new interface in the **same** package → a compile error. **Fix:** Rename the old one first (Part 1).

---

## ✅ Summary

- A repository is **one interface**: `interface StudentRepository extends JpaRepository<Student, Long> { }` — the entity type and the **id** type. 🤯
- **Spring Data** creates the implementation (a **proxy** 🎭 bean) at startup: "Found 1 JPA repository interface".
- Ready-made methods: **`save`**, `saveAll`, **`findById`** (`Optional`), **`findAll`**, **`count`**, **`existsById`**, **`deleteById`**, `delete`, `deleteAll`, `findAll(Sort)`, `findAll(Pageable)`.
- **`save`**: id `null` → **INSERT**; id set → **SELECT + UPDATE** (merge). Use the **returned** object.
- A **`CommandLineRunner`** runs once after startup — great for experiments (delete it afterwards). 🏃
- With `show-sql`, you see every SQL statement Hibernate writes for you. 👀
- The method names match our Chapter 63 repository — so the service barely changes. Next chapter: we connect the API! 🔗

---

## ❓ Quiz

1. Write the one-line repository for an entity `Course` with a `Long` id.
2. Who creates the code behind a repository interface? When?
3. What does `findById` return? Why?
4. How does `save` decide between INSERT and UPDATE?
5. Which SQL does `count()` produce?
6. What is a `CommandLineRunner`?
7. Do you need `@Repository` on a Spring Data interface?
8. What happens with `deleteById` for an id that doesn't exist?

<details>
<summary>Click to see the answers</summary>

1. `public interface CourseRepository extends JpaRepository<Course, Long> { }`
2. Spring Data, at startup — it creates a proxy object that implements the interface.
3. An `Optional<Student>` — because the student may not exist.
4. If the id is `null`, it inserts. If the id is set, it loads the row and updates it (merge).
5. `select count(*) from students`
6. A bean whose `run` method Spring calls once, right after the app starts.
7. No — Spring Data finds interfaces that extend `JpaRepository` automatically.
8. Nothing — no exception, nothing is deleted.

</details>

---

[⬅ Previous chapter](71-entities.md) | [Table of Contents](../README.md) | [Next chapter: Full CRUD project: Student app ➡](73-crud-student-app.md)
