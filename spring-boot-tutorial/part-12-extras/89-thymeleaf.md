# Chapter 89 – Thymeleaf: making HTML pages

[⬅ Previous chapter](88-logging.md) | [Table of Contents](../README.md) | [Next chapter ➡](90-calling-apis.md)

---

## 🎯 Goal

Our app speaks **JSON** — perfect for other programs. 🤖 But a **person** in a browser sees this:

```
[{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12,"classroom":"5A"},...]
```

Not very pretty. 😅 Today you'll make **real web pages** 🌐 — with headings, tables and links — straight from Spring Boot, using **Thymeleaf**.

At the end of this chapter you will know:

- The difference between **`@RestController`** (JSON) and **`@Controller`** (HTML pages)
- What a **template** is, and how Thymeleaf fills it 🧩
- How to send data to a page with a **`Model`**
- Thymeleaf's most useful helpers: **`th:text`**, **`th:each`**, **`th:if`**, **`th:href`**
- How to build a **search form** 🔎
- How to open the pages in our **secured** app 🔓

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **HTML** | The language of web pages: `<h1>`, `<p>`, `<table>`... (Chapter 43). |
| **Template** | An HTML page with **holes** 🕳️ where data goes in. Like a form you fill out. |
| **Thymeleaf** | A **template engine**: it fills the holes in your templates with data. 🌿 (Say "time-leaf".) |
| **`@Controller`** | A controller that answers with a **page** (a template name), not with JSON. |
| **`Model`** | A **bag** 👜 of data that the controller hands to the template. |
| **Attribute** | One thing in the model bag, with a name: `"students"` → the list of students. |
| **Server-side rendering** | The **server** builds the finished HTML page, and the browser just shows it. |

---

## 📖 Story: The birthday invitation 🎉

Lina wants to invite 20 friends to her birthday. She doesn't write 20 letters by hand! ✍️😩 She makes **one** card with **holes**:

```
 ┌──────────────────────────────────────────┐
 │ Dear ______,                    ← name   │
 │ Come to my party on ______!    ← date    │
 │ Love, Lina 🎈                            │
 └──────────────────────────────────────────┘
```

Then she fills in the holes for each friend: "Dear **Tom**", "Dear **Sara**"... 🎉

- The card with holes is the **template**.
- The list of names is the **data** (the **model**).
- Lina filling in the holes is **Thymeleaf**. 🌿

---

## 📦 Part 1: Add Thymeleaf

Add to **`pom.xml`**:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

That's all the setup! Spring Boot now looks for templates in **`src/main/resources/templates/`** (a folder Spring Initializr already made for you in Chapter 50 👍).

---

## 🎮 Part 2: `@Controller` vs `@RestController`

| | `@RestController` (Part 8) | `@Controller` (today) |
|---|---|---|
| Who reads the answer? | a **program** 🤖 | a **person** in a browser 👩 |
| The method returns | **data** → turned into JSON | the **name of a template** → turned into HTML |
| Example answer | `{"name":"Sara Ahmed"}` | `<h1>Sara Ahmed</h1>` |

We keep our JSON API exactly as it is, and add a **separate** controller for pages, under the URL **`/pages/...`**. Create:

**`controller/PageController.java`**

```java
package com.example.school.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import com.example.school.service.StudentService;

@Controller
public class PageController {

    private final StudentService studentService;

    public PageController(StudentService studentService) {
        this.studentService = studentService;
    }

    @GetMapping("/pages/students")
    public String students(Model model) {
        model.addAttribute("students", studentService.getAll(null, null));
        return "students";
    }
}
```

| Code | Meaning |
|---|---|
| `@Controller` | ⭐ **Not** `@RestController`! "My methods return **page names**." |
| `StudentService studentService` | We reuse our service — the same one the JSON API uses. Layers pay off! 🎉 |
| `public String students(Model model)` | The method gets a **`Model`** (the bag 👜) from Spring, and returns a `String`. |
| `model.addAttribute("students", ...)` | Put the list of students into the bag, with the name **`"students"`**. |
| `return "students";` | ⭐ "Show the template **`students`**" → Spring finds `templates/students.html`. |

---

## 🧩 Part 3: The template

Create **`src/main/resources/templates/students.html`**:

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Our students</title>
    <style>
        body  { font-family: sans-serif; margin: 2em; }
        table { border-collapse: collapse; }
        th, td { border: 1px solid #ccc; padding: 6px 12px; }
        th { background: #eef; }
    </style>
</head>
<body>
    <h1>🏫 Our students</h1>

    <p>We have <span th:text="${students.size()}">0</span> students.</p>

    <table>
        <tr>
            <th>Name</th>
            <th>Age</th>
            <th>Classroom</th>
        </tr>
        <tr th:each="student : ${students}">
            <td th:text="${student.name()}">Name</td>
            <td th:text="${student.age()}">Age</td>
            <td th:text="${student.classroom()}">Classroom</td>
        </tr>
    </table>
</body>
</html>
```

Most of it is normal HTML. The magic is in the **`th:`** attributes:

| Code | Meaning |
|---|---|
| `xmlns:th="http://www.thymeleaf.org"` | "This page uses Thymeleaf's `th:` attributes." (Helps IntelliJ understand them.) |
| `${students}` | ⭐ "Take **`students`** out of the model bag." |
| `th:text="${students.size()}"` | ⭐ **Replace** the text inside this tag with the value. The `0` is only a **placeholder** — you see it when you open the file directly, without Spring. |
| `th:each="student : ${students}"` | ⭐ A **loop** (like `for (StudentResponse student : students)`, Chapter 30): repeat this `<tr>` for **each** student. |
| `${student.name()}` | Call the record's `name()` method (Chapter 29). |

Restart and open **http://localhost:8080/pages/students** in your browser...

### 🔓 Opening the door

...you get a **401**! 🔒 Of course — our security rules from Part 10 only open `GET /api/**`. Pages live under `/pages/`, so they fall down to `anyRequest().authenticated()`. Add a rule to **`SecurityConfig`**, next to the other `GET` rule:

```java
                .requestMatchers(HttpMethod.GET, "/pages/**").permitAll()
```

Restart, reload — and there it is:

```
 🏫 Our students

 We have 3 students.

 ┌──────────────┬─────┬───────────┐
 │ Name         │ Age │ Classroom │
 ├──────────────┼─────┼───────────┤
 │ Sara Ahmed   │ 12  │ 5A        │
 │ Tom Brown    │ 13  │ 6B        │
 │ Lina Haddad  │ 11  │ 5A        │
 └──────────────┴─────┴───────────┘
```

🎉 A real web page, with data from the database! Right-click → **View page source**: the browser got **finished** HTML — no `th:` left, every hole filled. That's **server-side rendering**.

---

## 🔀 Part 4: `th:if` and `th:href`

Some students have **no** classroom (`null`). Let's write "—" for them. And each name should be a **link** to a detail page.

Change the row in `students.html`:

```html
        <tr th:each="student : ${students}">
            <td><a th:href="@{/pages/students/{id}(id=${student.id()})}" th:text="${student.name()}">Name</a></td>
            <td th:text="${student.age()}">Age</td>
            <td>
                <span th:if="${student.classroom() != null}" th:text="${student.classroom()}">5A</span>
                <span th:if="${student.classroom() == null}">—</span>
            </td>
        </tr>
```

| Code | Meaning |
|---|---|
| `th:if="${student.classroom() != null}"` | ⭐ Show this tag **only if** the condition is true. Otherwise, it's left out completely. |
| `th:href="@{...}"` | ⭐ Make a **link** URL. `@{...}` is Thymeleaf's way to write URLs. |
| `@{/pages/students/{id}(id=${student.id()})}` | `{id}` is a hole **in the URL**; `(id=...)` fills it. For Sara → `/pages/students/1`. |

Now the detail page. Add to **`PageController`**:

```java
@GetMapping("/pages/students/{id}")
public String student(@PathVariable Long id, Model model) {
    model.addAttribute("student", studentService.getById(id));
    return "student";
}
```

(Import `org.springframework.web.bind.annotation.PathVariable`.)

**`templates/student.html`**

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title th:text="${student.name()}">Student</title>
</head>
<body style="font-family: sans-serif; margin: 2em;">
    <h1 th:text="${student.name()}">Student name</h1>
    <p>📧 <span th:text="${student.email()}">email</span></p>
    <p>🎂 <span th:text="${student.age()}">0</span> years old</p>
    <p>🏫 Classroom: <span th:text="${student.classroom() ?: 'none yet'}">5A</span></p>
    <p><a th:href="@{/pages/students}">⬅ All students</a></p>
</body>
</html>
```

| Code | Meaning |
|---|---|
| `${student.classroom() ?: 'none yet'}` | The **Elvis operator** `?:` 🕺: "Use the classroom — but if it's `null`, use `'none yet'`." A shorter way than two `th:if`s! |
| `@{/pages/students}` | A link back to the list. |

Click on "Sara Ahmed" → **http://localhost:8080/pages/students/1** shows her card. 🪪

🤔 And `/pages/students/99`? `getById` throws `StudentNotFoundException` → our `GlobalExceptionHandler` answers **404** with a ProblemDetail (as JSON). For a website, a nice **error page** would be better — see "Try it yourself".

---

## 🔎 Part 5: A search form

Let's add a search box: type part of a name → see matching students. Our service already supports it (`getAll(null, name)`, Chapter 74)!

Change the list method in **`PageController`**:

```java
@GetMapping("/pages/students")
public String students(@RequestParam(required = false) String name, Model model) {
    model.addAttribute("students", studentService.getAll(null, name));
    model.addAttribute("name", name);
    return "students";
}
```

(Import `org.springframework.web.bind.annotation.RequestParam`.)

And add a form to **`students.html`**, under the `<h1>`:

```html
    <form th:action="@{/pages/students}" method="get">
        <input type="text" name="name" th:value="${name}" placeholder="Search by name">
        <button type="submit">🔎 Search</button>
    </form>
```

| Code | Meaning |
|---|---|
| `<form ... method="get">` | When you click the button, the browser goes to `/pages/students?name=...` (Chapter 59). |
| `name="name"` | The input's value becomes the request parameter **`name`**. |
| `th:value="${name}"` | Put the search word **back** into the box, so you can see what you searched. |
| `@RequestParam(required = false) String name` | No search yet → `name` is `null` → **all** students. |

Type `sa` and press 🔎 → only **Sara Ahmed**. 🎉

💡 Why only `GET` forms here? A form that **changes** data (`POST`) would need a **login** and **CSRF protection** (Chapter 80), because a browser with cookies is exactly what CSRF attacks use. That's a bigger topic — for now, our pages only **show** data, and changes go through the secured JSON API. 🔒

---

## 💻 Mini project: A book shelf page 📚

Make a page **`/pages/books`** that shows all books from your Book API (the mini projects of Parts 8–9) in a table: title, author, year.

- The page title: "📚 Our library".
- Under the table: "Oldest book: *title* (*year*)" — but only if there **are** books (`th:if`).

**Hint:** Your `BookService` probably has a method that returns all books as `BookResponse`s. To find the oldest, you can do it in the **controller** with a stream (Chapter 36) and put it into the model.

<details>
<summary>Click to see the answer</summary>

(Your `BookService` method names may be different — use yours!)

**In `PageController`** (inject `BookService` in the constructor too):

```java
@GetMapping("/pages/books")
public String books(Model model) {
    List<BookResponse> books = bookService.getAll();
    model.addAttribute("books", books);
    model.addAttribute("oldest", books.stream()
            .min(Comparator.comparingInt(BookResponse::year))
            .orElse(null));
    return "books";
}
```

(Imports: `java.util.Comparator`, `java.util.List`, `com.example.school.dto.BookResponse`, `com.example.school.service.BookService`.)

| Code | Meaning |
|---|---|
| `.min(Comparator.comparingInt(BookResponse::year))` | The book with the **smallest** year → an `Optional<BookResponse>`. |
| `.orElse(null)` | No books → `null`. The template checks for that. |

**`templates/books.html`**

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Our library</title>
</head>
<body style="font-family: sans-serif; margin: 2em;">
    <h1>📚 Our library</h1>
    <table border="1" cellpadding="6">
        <tr><th>Title</th><th>Author</th><th>Year</th></tr>
        <tr th:each="book : ${books}">
            <td th:text="${book.title()}">Title</td>
            <td th:text="${book.author()}">Author</td>
            <td th:text="${book.year()}">2000</td>
        </tr>
    </table>
    <p th:if="${oldest != null}">
        Oldest book: <b th:text="${oldest.title()}">Title</b> (<span th:text="${oldest.year()}">1900</span>)
    </p>
</body>
</html>
```

With the three books from Part 9, the page ends with: **Oldest book: The Hobbit (1937)**. 🧙

</details>

---

## ✋ Try it yourself

1. Show the students' ages in **red** when they're 13 or older. (Hint: `th:style="${student.age() >= 13} ? 'color:red' : ''"`.)
2. Add a link "🏫 Back to all students" at the bottom of the search results — but only when a search word was used.
3. Make a friendly 404 page: create **`templates/error/404.html`** with a nice message. Which URL shows it?

<details>
<summary>Click to see the answers</summary>

1. ```html
   <td th:text="${student.age()}" th:style="${student.age() >= 13} ? 'color:red' : ''">Age</td>
   ```
2. ```html
   <p th:if="${name != null}"><a th:href="@{/pages/students}">🏫 Back to all students</a></p>
   ```
3. Spring Boot's error page system uses `templates/error/404.html` for 404 errors **of web pages** that don't exist, like **http://localhost:8080/pages/nothing-here** (Spring answers that one with a browser-friendly error page). Our **API** errors, like a missing student, are still answered by our `GlobalExceptionHandler` as JSON — that handler always wins for exceptions from controllers.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: `@RestController` instead of `@Controller`

The browser shows the word **`students`** instead of the page! 😅 A `@RestController` sends the returned `String` **as it is**. **Fix:** Use `@Controller` for pages.

### Mistake 2: The template name doesn't match

`return "student-list";` but the file is `students.html` → an error page saying the template can't be found (*"Error resolving template [student-list]"*). **Fix:** The name you return = the file name without `.html`.

### Mistake 3: Forgetting `xmlns:th` or the `th:` prefix

`text="${student.name()}"` (without `th:`) is just a normal HTML attribute — Thymeleaf ignores it, and the page shows the placeholder text. **Fix:** Always `th:text`, `th:each`, `th:if`...

### Mistake 4: A 401 for the page

The security rules don't know `/pages/**`. **Fix:** `.requestMatchers(HttpMethod.GET, "/pages/**").permitAll()`.

### Mistake 5: Field names instead of record methods

Our DTOs are **records** — call `${student.name()}`. (Thymeleaf also understands `${student.name}` for records in new versions, but the method call always works.)

---

## ✅ Summary

- **`@Controller`** returns a **template name** → an HTML page. **`@RestController`** returns data → JSON. One app can have both! 🌐🤖
- Templates live in **`src/main/resources/templates/`**. Add **`spring-boot-starter-thymeleaf`**.
- The controller fills a **`Model`** 👜: `model.addAttribute("students", list)`.
- Thymeleaf: **`th:text`** (fill text), **`th:each`** (loop), **`th:if`** (show only if), **`th:href="@{...}"`** (links), **`?:`** (default value).
- `GET` forms + `@RequestParam` make a **search**. Forms that **change** data need login + CSRF.
- Open the page URLs in `SecurityConfig`.

---

## ❓ Quiz

1. What's the difference between `@Controller` and `@RestController`?
2. What does `return "students";` do in a `@Controller`?
3. What is the `Model` for?
4. What does `th:each="student : ${students}"` do?
5. Why is there placeholder text like `<td th:text="${student.name()}">Name</td>`?
6. What does `${student.classroom() ?: 'none yet'}` show for a student without a classroom?
7. Why did the page first answer 401?

<details>
<summary>Click to see the answers</summary>

1. `@Controller` methods return template names (HTML pages). `@RestController` methods return data that becomes JSON.
2. It tells Spring to show the template `templates/students.html`.
3. It's a bag of data that the controller gives to the template.
4. It repeats that HTML tag once for every student in the list.
5. So the file still looks good when opened without Spring. Thymeleaf replaces it with the real value.
6. `none yet`.
7. Our security rules only opened `GET /api/**`. `/pages/students` fell under `anyRequest().authenticated()`.

</details>

---

[⬅ Previous chapter](88-logging.md) | [Table of Contents](../README.md) | [Next chapter: Calling other APIs ➡](90-calling-apis.md)
