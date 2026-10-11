# Chapter 57 – @RestController and @GetMapping: the Student API begins

[⬅ Previous chapter](../part-07-spring-boot-basics/56-profiles.md) | [Table of Contents](../README.md) | [Next chapter ➡](58-path-variables.md)

---

## 🎯 Goal

Welcome to **Part 8**! 🎉 In the next 10 chapters, you'll build a **complete, professional REST API** for students — step by step. 🏫

At the end of this chapter you will know:

- The **plan** for the whole Student API (what we'll build in Part 8)
- How to start a **new project** for it, all by yourself
- How to keep data **in memory** (in a list) while we don't have a database yet
- How to return a **list** of students as JSON
- The whole **family** of mapping labels: `@GetMapping`, `@PostMapping`, `@PutMapping`, `@PatchMapping`, `@DeleteMapping`
- Two methods Spring gives you **for free**: `HEAD` and `OPTIONS` 🎁

> 🌱 You already wrote controllers in Chapter 52. Now we go **deeper**, and we build something **real**: the Student API you designed on paper in **Chapter 46**. ✏️➡️💻

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Resource** | A "thing" your API talks about: a **student**. (Chapter 46) |
| **Collection** | A **group** of resources: **all** students → `/api/students`. |
| **CRUD** | **C**reate, **R**ead, **U**pdate, **D**elete — the 4 basic jobs with data. (Chapter 44) |
| **In-memory** | Kept in the computer's **memory** (in a Java list), **not** in a database. Lost when the app stops! 💨 |
| **Mapping annotation** | A label that connects an **HTTP method + path** to a Java method: `@GetMapping`, `@PostMapping`... |
| **Wrapper type** | The "object version" of a simple type: `Long` for `long`, `Integer` for `int`. It can be `null`. |
| **HEAD** | Like GET, but the server sends **only the headers**, no body. |
| **OPTIONS** | "Which methods can I use here?" The server answers in the `Allow` header. |

---

## 📖 Story: The school office 🏫🗂️

Every school has an **office** with a **secretary** 👩‍💼. People come to the office window and ask:

- "Can I see the list of **all** students?" 📋
- "Can I see student number **2**?" 🔍
- "Please **add** a new student!" ➕
- "Tom has a new email — please **change** it." ✏️
- "Lina moved to another school — please **remove** her." 🗑️

The secretary keeps the student cards in a **filing cabinet** 🗄️, and answers each question with the right card... or a polite "Sorry, we don't have that student" (404). 😊

In Part 8, **you** build this office:

| School office | Your app |
|---|---|
| The office window 🪟 | `/api/students` |
| The secretary 👩‍💼 | `StudentController` (later also a **service** — Chapter 63) |
| The filing cabinet 🗄️ | A **list** in memory (later a real **database** — Part 9) |
| A student card 🪪 | A `Student` record |
| "Show me all students" | `GET /api/students` |

Today, the office opens, and the secretary can answer the **first** question: "Show me **all** students." 📋

---

## 🗺️ Part 1: The plan for Part 8

Remember the **5 standard endpoints** from **Chapter 46**? This is our map for the whole Part 8:

| # | Job | Method | Path | Chapter |
|---|---|---|---|---|
| 1 | List all students | `GET` | `/api/students` | **57** (today!) |
| 2 | Get one student | `GET` | `/api/students/{id}` | 58 |
| 3 | Search and filter | `GET` | `/api/students?minAge=12&sort=name` | 59 |
| 4 | Create a student | `POST` | `/api/students` | 60 |
| 5 | Replace / change a student | `PUT` / `PATCH` | `/api/students/{id}` | 61 |
| 6 | Delete a student | `DELETE` | `/api/students/{id}` | 61 |

And then we make it **professional**:

| Chapter | What we add |
|---|---|
| 62 | The **right status codes** (201 Created, 204 No Content, 404...) with `ResponseEntity` |
| 63 | **Layers**: Controller → Service → Repository |
| 64 | **DTOs**: safe boxes for data coming in and going out |
| 65 | **Validation**: "the email must be a real email!" ✅ |
| 66 | **Nice error messages** for everything |

At the end of Part 8, you'll have an API that looks like what real companies build. 💼🚀

---

## 🆕 Part 2: Create the `school` project

We start a **fresh** project for the Student API. You know how to do this (Chapter 49)! Go to **https://start.spring.io**:

| Field | Value |
|---|---|
| Project | **Maven** |
| Language | **Java** |
| Spring Boot | newest **stable** (no SNAPSHOT/M/RC) |
| Group | `com.example` |
| Artifact | `school` |
| Name | `school` |
| Description | `Student API` |
| Package name | `com.example.school` |
| Packaging | **Jar** |
| Java | **25** (or your version) |
| Dependencies | **Spring Web** |

**GENERATE** → unzip → **open** the `school` folder in IntelliJ → **Trust** → wait for Maven. ⏳ (Chapter 49 has the details if you forget something.)

You get the main class **`SchoolApplication`** in the package **`com.example.school`** — our **base package** (Chapter 50). All new classes go **here or below**. ✅

> 💡 You can **close** the old `hello` project (**File → Close Project**). We'll use `school` for all of Part 8.

---

## 🪪 Part 3: The `Student` record

Right-click **`com.example.school`** → **New → Java Class** → choose **Record** → name: **`Student`**.

```java
package com.example.school;

public record Student(Long id, String name, String email, int age) {
}
```

These are the **same 4 fields** as in our Chapter 46 design: `id`, `name`, `email`, `age`. ✅

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `public record Student(...)` | A record (Chapter 29): a small class for **data**, with a constructor, accessor methods (`name()`, `age()`...), `equals`, and `toString` for free. |
| `Long id` | The student's **number**. ⚠️ `Long` with a **capital L**! (See below.) |
| `String name` | The name, like `"Sara Ahmed"`. |
| `String email` | The email, like `"sara@school.com"`. |
| `int age` | The age, like `12`. |

### 🤔 Why `Long` and not `long`?

`long` is a **simple type** (Chapter 7): it **always** has a number. It can never be "empty".

`Long` is its **wrapper type** — the "object version". It can be a number **or `null`** (empty). Why do we want that? 🤔

Think about a **new** student who isn't saved yet. What's their id? **They don't have one yet!** The **server** gives the id (Chapter 46). So before saving, the id is `null` — "no id yet". With `long`, we'd have to invent a fake number like `0`... confusing! 😕

| Type | Can be `null`? | Example values |
|---|---|---|
| `long` | ❌ no | `0`, `1`, `42` |
| `Long` | ✅ yes | `null`, `1`, `42` |

> 💡 In **Part 9**, the **database** will create the ids, and it also expects a `Long` that is `null` for new things. So `Long id` is the professional habit. 👍

---

## 💻 Part 4: The `StudentController` — list all students

Create a new class **`StudentController`** in `com.example.school`:

```java
package com.example.school;

import java.util.ArrayList;
import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/students")
public class StudentController {

    private final List<Student> students = new ArrayList<>(List.of(
            new Student(1L, "Sara Ahmed", "sara@school.com", 12),
            new Student(2L, "Tom Brown", "tom@school.com", 13),
            new Student(3L, "Lina Haddad", "lina@school.com", 11)));

    @GetMapping
    public List<Student> getAll() {
        return students;
    }
}
```

**Run** `SchoolApplication` (▶️) and open **`http://localhost:8080/api/students`**:

```json
[{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12},{"id":2,"name":"Tom Brown","email":"tom@school.com","age":13},{"id":3,"name":"Lina Haddad","email":"lina@school.com","age":11}]
```

🎉 Your Student API answers its first question!

Easier to read, with spaces and new lines (the browser's **Pretty-print** — Chapter 52):

```json
[
  { "id": 1, "name": "Sara Ahmed",  "email": "sara@school.com", "age": 12 },
  { "id": 2, "name": "Tom Brown",   "email": "tom@school.com",  "age": 13 },
  { "id": 3, "name": "Lina Haddad", "email": "lina@school.com", "age": 11 }
]
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@RestController` | This class answers HTTP requests; return values become the response body (Chapter 52). |
| `@RequestMapping("/api/students")` | ⭐ **All** paths in this class start with `/api/students` (Chapter 52, Part 6). |
| `private final List<Student> students` | Our "filing cabinet" 🗄️: a list of students. `final` = this variable always points to the **same** list (but the list's **content** can change). |
| `new ArrayList<>(List.of(...))` | Make a list with 3 students in it. (Why two parts? See below! ⬇️) |
| `new Student(1L, "Sara Ahmed", "sara@school.com", 12)` | One student. `1L` = the number 1 as a `long` (the `L` is needed for `Long` — Chapter 7). |
| `@GetMapping` | **No path** → just the class path: `GET /api/students`. |
| `public List<Student> getAll()` | Returns the whole list → Jackson makes a JSON **array** (Chapter 52). |

### 🤔 Why `new ArrayList<>(List.of(...))`?

Remember **Chapter 30**? `List.of(...)` makes a list that **can't be changed** (immutable) 🔒. If we try to `add` a student later (Chapter 60), Java throws `UnsupportedOperationException`. 💥

`new ArrayList<>(...)` **copies** it into a normal list that **can** change. ✅

```
List.of(Sara, Tom, Lina)            🔒 can't add, can't remove
        │ copy
        ▼
new ArrayList<>(...)                ✅ can add, remove, change
```

### 🤔 Where does the data live?

The list is a **field** of the controller. And the controller is a **bean** — a **singleton** (Chapter 54). So there is **one** controller, with **one** list, shared by **all** requests. 🗄️

But it's **only in memory**:

- ✅ While the app runs, all users see the same list.
- ❌ When you **stop** the app, the list is **gone**. On the next start, you have the 3 students again — and every change is **forgotten**. 💨

That's OK for learning! In **Part 9**, we'll put the students into a real **database**, where they stay forever. 🗄️💾

---

## ➕ Part 5: Two more GET endpoints

Let's add two small endpoints to `StudentController`:

```java
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
```

Restart and try them. Real answers:

`GET /api/students/count`

```
3
```

`GET /api/students/names`

```json
["Sara Ahmed","Tom Brown","Lina Haddad"]
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@GetMapping("/count")` | Class path + method path = `GET /api/students/count`. |
| `return students.size();` | How many students? An `int` → the JSON number `3`. |
| `@GetMapping("/names")` | `GET /api/students/names` |
| `students.stream()` | Go through the students one by one (Chapter 36). 🌊 |
| `.map(Student::name)` | Change each student into **just** their name. (A method reference — Chapter 35.) |
| `.toList()` | Collect the names into a new list → a JSON array of texts. |

---

## 🏷️ Part 6: The mapping family 👨‍👩‍👧‍👦

You know `@GetMapping`. It has **brothers and sisters** — one for each HTTP method (Chapter 44):

| Label | HTTP method | CRUD job | We use it in |
|---|---|---|---|
| `@GetMapping` | **GET** | **R**ead | Ch 57–59 |
| `@PostMapping` | **POST** | **C**reate | Ch 60 |
| `@PutMapping` | **PUT** | **U**pdate (replace all) | Ch 61 |
| `@PatchMapping` | **PATCH** | **U**pdate (change some) | Ch 61 |
| `@DeleteMapping` | **DELETE** | **D**elete | Ch 61 |

They all work the same way: the label **+ an optional path**:

```java
@GetMapping            // GET    /api/students
@GetMapping("/{id}")   // GET    /api/students/5        (Chapter 58)
@PostMapping           // POST   /api/students          (Chapter 60)
@DeleteMapping("/{id}")// DELETE /api/students/5        (Chapter 61)
```

### The "big sister": `@RequestMapping`

All of them are **shortcuts** for `@RequestMapping` with a `method`:

```java
@GetMapping("/count")
// is the same as:
@RequestMapping(value = "/count", method = RequestMethod.GET)
```

Old code (from before 2016) uses the long form. You'll see it on the internet sometimes. Today, everybody uses the **short** ones. 👍 (And `@RequestMapping` **without** a method is still used **on the class**, for the common path — like we do.)

### One method, two paths

You can give **several** paths in curly braces `{ }`:

```java
@GetMapping({"/count", "/total"})
public int count() {
    return students.size();
}
```

Now both `/api/students/count` **and** `/api/students/total` answer `3`. (Useful when you rename a path but old apps still use the old name.)

---

## 🎁 Part 7: Free gifts — HEAD and OPTIONS

For **every** `@GetMapping`, Spring answers **two more** HTTP methods automatically. You don't write any code! 🎁

### HEAD — "just the headers, please"

```
curl -I http://localhost:8080/api/students/count
```

(`-I` = send a HEAD request.)

```
HTTP/1.1 200 
Content-Type: application/json
Content-Length: 1
```

Only the **headers** — no body. Why is that useful? A client can **check** if something exists, or how **big** it is, without downloading it. (Like reading the label on a box without opening it. 📦👀)

### OPTIONS — "what can I do here?"

```
curl -i -X OPTIONS http://localhost:8080/api/students/count
```

```
HTTP/1.1 200 
Allow: GET,HEAD,OPTIONS
Accept-Patch: 
Content-Length: 0
```

The **`Allow`** header lists the methods this path accepts. (Ignore the empty `Accept-Patch` header — it's about PATCH, which you'll meet in Chapter 61.) Right now: GET (yours), plus HEAD and OPTIONS (the free gifts). When you add `@PostMapping` in Chapter 60, POST will appear in this list too! 🤓

---

## 💻 Mini project: The Book API 📚 (your own project!)

From now on, every chapter in Part 8 has a mini project: you build a **second API** — for **books** 📚 — next to the Student API. Same ideas, **your** code. This is the best way to really learn! 💪

**Today's task:** In the **same** `school` project (a school has a library! 😊):

1. Create a record **`Book`** with: `Long id`, `String title`, `String author`, `int year`.
2. Create a **`BookController`** with the path **`/api/books`** and 3 books in a list:

| id | title | author | year |
|---|---|---|---|
| 1 | Matilda | Roald Dahl | 1988 |
| 2 | The Hobbit | J.R.R. Tolkien | 1937 |
| 3 | Charlotte's Web | E.B. White | 1952 |

3. Add 3 endpoints:
   - `GET /api/books` → all books
   - `GET /api/books/count` → how many books
   - `GET /api/books/titles` → only the titles

Try it **alone** first! Then check the answer. 🙈

<details>
<summary>Click to see the answer</summary>

**`Book.java`**

```java
package com.example.school;

public record Book(Long id, String title, String author, int year) {
}
```

**`BookController.java`**

```java
package com.example.school;

import java.util.ArrayList;
import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/books")
public class BookController {

    private final List<Book> books = new ArrayList<>(List.of(
            new Book(1L, "Matilda", "Roald Dahl", 1988),
            new Book(2L, "The Hobbit", "J.R.R. Tolkien", 1937),
            new Book(3L, "Charlotte's Web", "E.B. White", 1952)));

    @GetMapping
    public List<Book> getAll() {
        return books;
    }

    @GetMapping("/count")
    public int count() {
        return books.size();
    }

    @GetMapping("/titles")
    public List<String> titles() {
        return books.stream()
                .map(Book::title)
                .toList();
    }
}
```

Answers:

`GET /api/books`

```json
[{"id":1,"title":"Matilda","author":"Roald Dahl","year":1988},{"id":2,"title":"The Hobbit","author":"J.R.R. Tolkien","year":1937},{"id":3,"title":"Charlotte's Web","author":"E.B. White","year":1952}]
```

`GET /api/books/count` → `3`

`GET /api/books/titles`

```json
["Matilda","The Hobbit","Charlotte's Web"]
```

Keep this code — you'll grow the Book API in every chapter! 🌱📚

</details>

---

## ✋ Try it yourself

**Task 1:** Add `GET /api/students/emails` that returns a list of all emails.

<details>
<summary>Click to see the answer</summary>

```java
@GetMapping("/emails")
public List<String> emails() {
    return students.stream()
            .map(Student::email)
            .toList();
}
```

Answer: `["sara@school.com","tom@school.com","lina@school.com"]`

</details>

**Task 2:** Add `GET /api/students/average-age` that returns the average age as a `double`. (Tip: Chapter 36 — `mapToInt(...)` and `average()`.)

<details>
<summary>Click to see the answer</summary>

```java
@GetMapping("/average-age")
public double averageAge() {
    return students.stream()
            .mapToInt(Student::age)
            .average()
            .orElse(0);
}
```

`(12 + 13 + 11) / 3 = 12.0` → the answer is `12.0`. (`orElse(0)` is for an **empty** list, where there's no average — Chapter 37.)

</details>

**Task 3:** Use `curl -i -X OPTIONS` on `http://localhost:8080/api/students`. What does the `Allow` header say?

<details>
<summary>Click to see the answer</summary>

`Allow: GET,HEAD,OPTIONS` — only GET (and the two free gifts), because we only have a `@GetMapping` for that path so far.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Using `List.of(...)` alone for data that will change

```java
private final List<Student> students = List.of(...);   // 🔒 can never change!
```

Today it works. But in Chapter 60, `students.add(...)` will crash with `UnsupportedOperationException`. 💥 **Fix:** `new ArrayList<>(List.of(...))`.

### Mistake 2: `1` instead of `1L`

```java
new Student(1, "Sara Ahmed", "sara@school.com", 12)   // ❌
```

Java says:

```
error: constructor Student in record Student cannot be applied to given types;
  required: Long,String,String,int
  found:    int,String,String,int
  reason: argument mismatch; int cannot be converted to Long
```

"**int cannot be converted to Long**": the number `1` is an `int`, and Java won't turn an `int` into a `Long` automatically. **Fix:** Write `1L`. ✅

### Mistake 3: The path is doubled or missing

With `@RequestMapping("/api/students")` on the class:

| On the method | Final URL | OK? |
|---|---|---|
| `@GetMapping("/count")` | `/api/students/count` | ✅ |
| `@GetMapping("/api/students/count")` | `/api/students/api/students/count` 😵 | ❌ |
| `@GetMapping("count")` | `/api/students/count` | ✅ (works, but write the `/` — it's clearer) |

**Fix:** On the method, write **only** the part **after** the class path.

### Mistake 4: Expecting changes to survive a restart

Everything is **in memory**. Restart = the original 3 students again. That's not a bug — it's how in-memory lists work. 💨 (Part 9 fixes this with a database.)

### Mistake 5: The old `hello` app is still running

You start `school`, and it fails with `Port 8080 was already in use`. The `hello` app from Part 7 is still running! **Fix:** Stop it (⏹️ in its Run tab). (Chapter 51.)

---

## ✅ Summary

- Part 8 builds the **Student API** from Chapter 46, step by step: list, get one, filter, create, update, delete, then status codes, layers, DTOs, validation and errors.
- New project **`school`** (Spring Web), base package **`com.example.school`**.
- `record Student(Long id, String name, String email, int age)` — **`Long`** so the id can be `null` before the server gives one.
- `@RequestMapping("/api/students")` on the class + `@GetMapping` on methods.
- Data lives **in memory**: `new ArrayList<>(List.of(...))` — a changeable list. One controller bean = one shared list. Restart = reset. 💨
- Returning a `List<Student>` → a JSON **array**. `int` → a JSON number.
- The mapping family: **`@GetMapping`**, **`@PostMapping`**, **`@PutMapping`**, **`@PatchMapping`**, **`@DeleteMapping`** (all shortcuts for `@RequestMapping(method = ...)`).
- Free gifts: **HEAD** (headers only) and **OPTIONS** (`Allow` header) for every GET endpoint. 🎁

---

## ❓ Quiz

1. Which HTTP method and path lists all students?
2. Why is the `id` a `Long` and not a `long`?
3. What's wrong with `private final List<Student> students = List.of(...)` if we want to add students later?
4. The class has `@RequestMapping("/api/students")`. The method has `@GetMapping("/count")`. What's the full path?
5. Which mapping label do you use for creating? For deleting?
6. What happens to the students you added when you restart the app? Why?
7. What does a HEAD request return?
8. How can a client find out which methods a path accepts?

<details>
<summary>Click to see the answers</summary>

1. `GET /api/students`
2. Because a new student has **no** id yet — `Long` can be `null`, `long` can't.
3. `List.of(...)` can't be changed. `add` would throw `UnsupportedOperationException`. Use `new ArrayList<>(List.of(...))`.
4. `/api/students/count`
5. `@PostMapping` for creating, `@DeleteMapping` for deleting.
6. They're gone — the list is only in memory, and a restart creates a new list with the first 3 students.
7. Only the status line and headers — no body.
8. Send an **OPTIONS** request and read the `Allow` header.

</details>

---

[⬅ Previous chapter](../part-07-spring-boot-basics/56-profiles.md) | [Table of Contents](../README.md) | [Next chapter: Path variables: /students/5 ➡](58-path-variables.md)
