# Chapter 66 – Handling errors nicely (`@RestControllerAdvice`)

[⬅ Previous chapter](65-validation.md) | [Table of Contents](../README.md) | [Next chapter ➡](../part-09-databases/67-what-is-a-database.md)

---

## 🎯 Goal

Our API answers errors with the right **status codes**... but the **bodies** are not helpful: 😕

```json
{"timestamp":"...","status":400,"error":"Bad Request","path":"/api/students"}
```

"Bad Request" — **what** was bad? Which field? The client has **no idea**. Today, we fix that — for **every** error, in **one** place. 💌

At the end of this chapter you will know:

- What **Problem Details** are (the internet standard for error bodies — Chapter 46) and Spring's **`ProblemDetail`** class
- How **`@RestControllerAdvice`** + **`@ExceptionHandler`** handle errors for **all** controllers, in one central place 🏢
- How to send **clear messages** for "not found" (404) and "email already used" (409)
- How to send **every validation error**, field by field 📋
- How to make **Spring's own** errors (wrong JSON, wrong id type...) look the same
- How to catch **unexpected** errors safely — without showing secrets 🔒
- A dangerous trap with "catch everything" 🪤

> 🌱 This is the **last chapter of Part 8**. After it, your Student API is **complete and professional**! 🏆

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Problem Details** | An internet **standard** (RFC 9457) for how error bodies should look: `title`, `status`, `detail`, `instance`. |
| **`ProblemDetail`** | Spring's Java class for a Problem Details body. 📄 |
| **`@ExceptionHandler`** | A label on a method: "When **this** exception happens, call me to build the answer." |
| **`@RestControllerAdvice`** | A label on a class: "My `@ExceptionHandler` methods work for **all** controllers." 🌍 |
| **Global** | For the **whole** app, not just one class. |
| **`ResponseEntityExceptionHandler`** | A Spring class that already knows how to answer **Spring's own** errors with Problem Details. We'll **extend** it. |
| **Override** | Replace a parent's method with your own version (Chapter 22). |
| **Stack trace** | The long list of "at ... at ... at ..." lines that shows where an error happened. **Never** send it to clients! 🙈 |

---

## 📖 Story: The complaints desk 🏢

A big shopping mall has **50 shops**. When something goes wrong — a broken toy, a wrong price, a lost child — where do people go?

**Bad mall:** every shop handles complaints **differently**. One shop shouts, one gives a note in Chinese, one just says "No." 😵

**Good mall:** there's **one complaints desk** 🏢 for the **whole** mall. It knows **every** kind of problem, and always answers the **same, polite way**:

```
┌─────────────────────────────────────────┐
│ 📋 PROBLEM REPORT                        │
│ Problem:  Student not found              │
│ Code:     404                            │
│ Details:  Student with id 99 was not     │
│           found                          │
│ Where:    /api/students/99               │
└─────────────────────────────────────────┘
```

In Spring:

| Mall | Spring Boot |
|---|---|
| The complaints desk 🏢 | A class with **`@RestControllerAdvice`** |
| "For broken toys, do this..." | An **`@ExceptionHandler`** method for one kind of exception |
| The problem report form 📋 | **`ProblemDetail`** (the Problem Details standard) |
| The 50 shops | All your **controllers** |

---

## 📋 Part 1: Problem Details — the standard error format

Remember **Chapter 46**? There's an internet standard for error bodies, called **Problem Details** (RFC 9457). Its fields:

| Field | Meaning | Example |
|---|---|---|
| `title` | A **short** name for the problem | `"Student not found"` |
| `status` | The HTTP status code (again) | `404` |
| `detail` | A **human-friendly** explanation | `"Student with id 99 was not found"` |
| `instance` | **Which** request had the problem | `"/api/students/99"` |
| `type` | A URL with documentation about this kind of problem (optional) | `"about:blank"` = "no special page" |
| *(your own fields)* | Anything extra that helps | `"errors": {...}` |

And the `Content-Type` is **`application/problem+json`** — "this JSON is a problem report". 📋

Spring has a Java class for it: **`ProblemDetail`**. You create one like this:

```java
ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, "Student with id 99 was not found");
problem.setTitle("Student not found");
```

| Code | Meaning |
|---|---|
| `ProblemDetail.forStatusAndDetail(status, detail)` | Make a problem report with a **status** and a **detail** text. |
| `problem.setTitle("...")` | Set the short title. (Without it, Spring uses the status name, like `"Not Found"`.) |
| `problem.setProperty("errors", ...)` | Add your **own** extra field. |

Spring fills in `instance` (the path) **automatically**. 🪄

---

## 🏢 Part 2: Your first complaints desk

### Step 1: Remove `@ResponseStatus` from the exceptions

In Chapter 63, our exceptions had `@ResponseStatus(...)`. Now the **complaints desk** decides the status — so the exceptions become **plain** again. (Remember the promise from Chapter 63? Here it is! 😊)

**`exception/StudentNotFoundException.java`**

```java
package com.example.school.exception;

public class StudentNotFoundException extends RuntimeException {

    public StudentNotFoundException(Long id) {
        super("Student with id " + id + " was not found");
    }
}
```

**`exception/EmailAlreadyUsedException.java`**

```java
package com.example.school.exception;

public class EmailAlreadyUsedException extends RuntimeException {

    public EmailAlreadyUsedException(String email) {
        super("The email " + email + " is already used by another student");
    }
}
```

Now the exceptions know **nothing** about HTTP. 🧼 The service throws them, and the desk turns them into HTTP answers.

### Step 2: The complaints desk

Create **`exception/GlobalExceptionHandler.java`**:

```java
package com.example.school.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(StudentNotFoundException.class)
    public ProblemDetail handleStudentNotFound(StudentNotFoundException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
        problem.setTitle("Student not found");
        return problem;
    }

    @ExceptionHandler(EmailAlreadyUsedException.class)
    public ProblemDetail handleEmailAlreadyUsed(EmailAlreadyUsedException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, ex.getMessage());
        problem.setTitle("Email already used");
        return problem;
    }
}
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@RestControllerAdvice` | ⭐ "This class is the **complaints desk** for **all** `@RestController`s." (It's a bean, so it must be in the base package — Chapter 50.) |
| `@ExceptionHandler(StudentNotFoundException.class)` | ⭐ "When **any** controller (or the service below it) throws a `StudentNotFoundException`, call **this** method." |
| `public ProblemDetail handleStudentNotFound(StudentNotFoundException ex)` | The method gets the **exception** as a parameter, and returns the **answer**. |
| `ex.getMessage()` | The message we gave in the exception's constructor: `"Student with id 99 was not found"` (Chapter 33). |
| `ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ...)` | A problem report with **404** and that message. |
| `problem.setTitle("Student not found")` | A short, clear title. |
| `return problem;` | Spring sends it as **`application/problem+json`** with status **404**. |
| (the second method) | The same for `EmailAlreadyUsedException` → **409 Conflict**. |

### ✅ Test it

Restart. Real answers:

`GET /api/students/99`

```
HTTP/1.1 404 
Content-Type: application/problem+json

{"detail":"Student with id 99 was not found","instance":"/api/students/99","status":404,"title":"Student not found"}
```

🎉 **Finally a clear message!** Pretty-printed:

```json
{
  "detail": "Student with id 99 was not found",
  "instance": "/api/students/99",
  "status": 404,
  "title": "Student not found"
}
```

`POST /api/students` with Sara's email:

```json
{"detail":"The email sara@school.com is already used by another student","instance":"/api/students","status":409,"title":"Email already used"}
```

`DELETE /api/students/42` → the same nice 404 (the service throws the same exception). ✅

> 💡 **Where's `"type": "about:blank"`?** In Chapter 46, our example had it. Spring **leaves it out** when it's `about:blank`, because that's the **default** meaning ("no special documentation page"). Clients treat a missing `type` exactly like `about:blank`. ✅ (And the fields come in A→Z order. JSON doesn't care about order — Chapter 45.)

### 🗺️ How it works

```
 GET /api/students/99
   │
   ▼
 StudentController.getById(99)
   │
   ▼
 StudentService.getById(99) ──► throws StudentNotFoundException 💥
                                      │
   (the exception flies up through the controller...)
                                      ▼
 🌱 Spring: "Who handles StudentNotFoundException?"
   │
   ▼
 🏢 GlobalExceptionHandler.handleStudentNotFound(ex)
   │  builds ProblemDetail(404, "Student with id 99 was not found")
   ▼
 🌐 HTTP/1.1 404  application/problem+json
```

The controller and the service didn't change **at all**. One central place handles the problem for **all** controllers — `StudentController`, `BookController`, and any you write in the future. 🌍

---

## 📋 Part 3: Validation errors — field by field

Now the big one: **validation errors** (Chapter 65). When `@Valid` fails, Spring throws a **`MethodArgumentNotValidException`**. Inside it is a list of **all** the broken rules. Let's turn them into a **map**: field → message.

Add this method to the desk:

```java
@ExceptionHandler(MethodArgumentNotValidException.class)
public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
    Map<String, String> errors = new TreeMap<>();
    for (FieldError fieldError : ex.getBindingResult().getFieldErrors()) {
        errors.put(fieldError.getField(), fieldError.getDefaultMessage());
    }
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST,
            "The request has " + errors.size() + " invalid field(s)");
    problem.setTitle("Invalid data");
    problem.setProperty("errors", errors);
    return problem;
}
```

Imports:

```java
import java.util.Map;
import java.util.TreeMap;

import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@ExceptionHandler(MethodArgumentNotValidException.class)` | "When `@Valid` finds broken rules, call me." |
| `Map<String, String> errors = new TreeMap<>();` | A map for **field name → message**. A `TreeMap` keeps the keys in **A→Z order** (Chapter 31), so the answer always looks the same. |
| `ex.getBindingResult().getFieldErrors()` | ⭐ The list of **all** broken rules, one `FieldError` per problem. |
| `fieldError.getField()` | **Which** field: `"email"`. |
| `fieldError.getDefaultMessage()` | **Your** message from the label: `"Email must be a valid email address"` (Chapter 65). |
| `errors.put(...)` | Add it to the map. |
| `"The request has " + errors.size() + " invalid field(s)"` | A short summary for `detail`. |
| `problem.setProperty("errors", errors)` | ⭐ Add our **own** field `errors` to the problem report. Jackson turns the map into a JSON object. |

### ✅ Test it

```bash
curl -i -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"A","email":"not-an-email","age":3}'
```

Real answer:

```
HTTP/1.1 400 
Content-Type: application/problem+json

{"detail":"The request has 3 invalid field(s)","instance":"/api/students","status":400,"title":"Invalid data","errors":{"age":"Age must be at least 5","email":"Email must be a valid email address","name":"Name must be 2 to 50 characters long"}}
```

Pretty-printed:

```json
{
  "detail": "The request has 3 invalid field(s)",
  "instance": "/api/students",
  "status": 400,
  "title": "Invalid data",
  "errors": {
    "age": "Age must be at least 5",
    "email": "Email must be a valid email address",
    "name": "Name must be 2 to 50 characters long"
  }
}
```

🎉🎉🎉 **Every** problem, **every** field, with **your** friendly messages! A website could now show each message **next to** the right input box. 📝✨ This is almost **exactly** the error format we designed in **Chapter 46**!

> 💡 If one field breaks **two** rules (like an empty name: "required" **and** "too short"), the map keeps only **one** message per field — and which one can change between runs. That's fine: fix one problem, and the client tells you the next. 😊

---

## 😕 Part 4: Spring's own errors still look old

Our own exceptions look great now. But what about errors that **Spring** finds **before** your code even runs? We tested them:

| Request | Answer |
|---|---|
| `GET /api/students/abc` (not a number) | `{"timestamp":"...","status":400,"error":"Bad Request","path":"/api/students/abc"}` 😕 |
| `GET /nothing` (no such URL) | `{"timestamp":"...","status":404,"error":"Not Found","path":"/nothing"}` 😕 |

The **old** format — and no details! 😕 Two different error styles in one API is confusing for clients. Let's make **everything** look the same.

### ✅ The fix: extend `ResponseEntityExceptionHandler`

Spring has a ready class that already knows how to answer **all of Spring's own errors** (wrong types, broken JSON, wrong method, unknown URL, missing parameters...) with **Problem Details**: **`ResponseEntityExceptionHandler`**. We just **extend** it (inheritance — Chapter 22)!

```java
@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {
    ...
}
```

But wait — there's a catch. 🪤 If you keep your `@ExceptionHandler(MethodArgumentNotValidException.class)` method, the app **doesn't start**! We tested it:

```
Ambiguous @ExceptionHandler method mapped for [ExceptionHandler{exceptionType=org.springframework.web.bind.MethodArgumentNotValidException, mediaType=*/*}]: {public org.springframework.http.ProblemDetail com.example.school.exception.GlobalExceptionHandler.handleValidation(org.springframework.web.bind.MethodArgumentNotValidException), public final org.springframework.http.ResponseEntity org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler.handleException(java.lang.Exception,org.springframework.web.context.request.WebRequest) throws java.lang.Exception}
```

"**Ambiguous**" — two methods want to handle the same exception: **yours**, and the **parent's** `handleException`. Spring doesn't know which one to call. 😵

**Fix:** The parent class has a special method **for** validation errors: `handleMethodArgumentNotValid`. Instead of a new `@ExceptionHandler`, we **override** it (Chapter 22 — replace the parent's version with ours):

```java
@Override
protected ResponseEntity<Object> handleMethodArgumentNotValid(MethodArgumentNotValidException ex,
        HttpHeaders headers, HttpStatusCode status, WebRequest request) {
    Map<String, String> errors = new TreeMap<>();
    for (FieldError fieldError : ex.getBindingResult().getFieldErrors()) {
        errors.put(fieldError.getField(), fieldError.getDefaultMessage());
    }
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST,
            "The request has " + errors.size() + " invalid field(s)");
    problem.setTitle("Invalid data");
    problem.setProperty("errors", errors);
    return ResponseEntity.badRequest().body(problem);
}
```

| Code | Meaning |
|---|---|
| `@Override` | "I'm replacing the parent's method." (Chapter 22 — Java checks that the parent really has this method!) |
| `protected ResponseEntity<Object> handleMethodArgumentNotValid(...)` | The **exact** name and parameters of the parent's method. (Tip: in IntelliJ, press **Ctrl + O** → choose `handleMethodArgumentNotValid` → IntelliJ writes the first line for you! ✨) |
| `HttpHeaders headers, HttpStatusCode status, WebRequest request` | Extra information the parent gives us. We don't need it here. |
| *(the same map code as before)* | ... |
| `return ResponseEntity.badRequest().body(problem);` | The parent's method returns a `ResponseEntity`, so we wrap our problem in one (Chapter 62). |

---

## 🛡️ Part 5: Catch the unexpected — safely

Sometimes, something goes wrong that you **didn't** expect: a bug, a full disk, a database that's down... 💥 Spring answers **500**. But we want:

1. The **same** Problem Details format.
2. **No secrets** in the answer! Error messages can contain file names, passwords, or database details. Bad people love those. 🕵️
3. The **full** error in **our** log (console), so **we** can fix it. 🔍

Add a "catch everything" method:

```java
@ExceptionHandler(Exception.class)
public ProblemDetail handleEverythingElse(Exception ex) {
    logger.error("Unexpected error", ex);
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.INTERNAL_SERVER_ERROR,
            "Something went wrong on our side. Please try again later.");
    problem.setTitle("Server error");
    return problem;
}
```

| Code | Meaning |
|---|---|
| `@ExceptionHandler(Exception.class)` | ⭐ "Any exception that **no other** handler takes → me." (`Exception` is the parent of all exceptions — Chapter 33. More specific handlers always win.) |
| `logger.error("Unexpected error", ex);` | ⭐ Write the **full** error (with the stack trace) to the **console**. `logger` comes **for free** from the parent class `ResponseEntityExceptionHandler`. (More about logging in Chapter 88.) |
| `"Something went wrong on our side..."` | A **safe**, friendly message for the client. **No** details! 🔒 |

We tested it with a test endpoint that throws `new IllegalStateException("The database exploded")`. The **client** sees:

```json
{"detail":"Something went wrong on our side. Please try again later.","instance":"/api/oops","status":500,"title":"Server error"}
```

And **only the console** shows the real reason:

```
... ERROR ... c.e.s.exception.GlobalExceptionHandler   : Unexpected error

java.lang.IllegalStateException: The database exploded
	at ...
```

✅ Safe for the client, helpful for **you**. 🔒🔍

---

## 🏆 Part 6: The complete complaints desk

Here's the final **`exception/GlobalExceptionHandler.java`**:

```java
package com.example.school.exception;

import java.util.Map;
import java.util.TreeMap;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ProblemDetail;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(StudentNotFoundException.class)
    public ProblemDetail handleStudentNotFound(StudentNotFoundException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
        problem.setTitle("Student not found");
        return problem;
    }

    @ExceptionHandler(EmailAlreadyUsedException.class)
    public ProblemDetail handleEmailAlreadyUsed(EmailAlreadyUsedException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, ex.getMessage());
        problem.setTitle("Email already used");
        return problem;
    }

    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(MethodArgumentNotValidException ex,
            HttpHeaders headers, HttpStatusCode status, WebRequest request) {
        Map<String, String> errors = new TreeMap<>();
        for (FieldError fieldError : ex.getBindingResult().getFieldErrors()) {
            errors.put(fieldError.getField(), fieldError.getDefaultMessage());
        }
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST,
                "The request has " + errors.size() + " invalid field(s)");
        problem.setTitle("Invalid data");
        problem.setProperty("errors", errors);
        return ResponseEntity.badRequest().body(problem);
    }

    @ExceptionHandler(Exception.class)
    public ProblemDetail handleEverythingElse(Exception ex) {
        logger.error("Unexpected error", ex);
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.INTERNAL_SERVER_ERROR,
                "Something went wrong on our side. Please try again later.");
        problem.setTitle("Server error");
        return problem;
    }
}
```

### ✅ The big test — every error, one style

We sent **every** kind of bad request. All answers are **real**, and they're **all** `application/problem+json`: 🎉

| Request | Status | `title` | `detail` |
|---|---|---|---|
| `GET /api/students/99` | **404** | Student not found | Student with id 99 was not found |
| `POST` with `{"name":"A","email":"not-an-email","age":3}` | **400** | Invalid data | The request has 3 invalid field(s) *(+ `errors`)* |
| `PUT /api/students/1` without `age` | **400** | Invalid data | The request has 1 invalid field(s) *(+ `"age":"Age is required"`)* |
| `PATCH /api/students/1` with `{"age":42}` | **400** | Invalid data | The request has 1 invalid field(s) *(+ `"age":"Age must be at most 20"`)* |
| `POST` with Sara's email | **409** | Email already used | The email sara@school.com is already used by another student |
| `GET /api/students/abc` | **400** | Bad Request | Failed to convert 'id' with value: 'abc' |
| `GET /api/students/0` (`@Min(1)`) | **400** | Bad Request | Validation failure |
| `POST` with broken JSON `{"name":` | **400** | Bad Request | Failed to read request |
| `POST` with no `Content-Type` | **415** | Unsupported Media Type | Content-Type 'application/x-www-form-urlencoded;charset=UTF-8' is not supported. |
| `DELETE /api/students` (no id) | **405** | Method Not Allowed | Method 'DELETE' is not supported. |
| `GET /nothing` | **404** | Not Found | No static resource nothing. |
| A bug inside the app | **500** | Server error | Something went wrong on our side. Please try again later. |

The last 6 rows come from **`ResponseEntityExceptionHandler`** — we didn't write any code for them! 🎁 One style for **every** error. Clients will love your API. 💌

---

## 🪤 Part 7: The "catch everything" trap

Here's a mistake that **many** developers make. 😬 They write a catch-all `@ExceptionHandler(Exception.class)` — but **without** extending `ResponseEntityExceptionHandler`:

```java
@RestControllerAdvice
public class GlobalExceptionHandler {            // ❌ no "extends ResponseEntityExceptionHandler"

    @ExceptionHandler(Exception.class)
    public ProblemDetail handleEverythingElse(Exception ex) { ... 500 ... }
}
```

We tested it. Look what happened: 😱

| Request | Should be | Was |
|---|---|---|
| `GET /api/students/abc` | 400 | **500** "Something went wrong..." |
| `GET /nothing` | 404 | **500** "Something went wrong..." |
| `POST` with broken JSON | 400 | **500** "Something went wrong..." |

The catch-all **swallowed** Spring's own errors — the ones that should be 400 or 404 — and turned them all into **500**! 🪤 Now clients think **your server** is broken, when really **they** sent a bad request.

**Why?** Without the parent class, there's no **specific** handler for Spring's errors, so "catch **everything**" really catches **everything**.

**Fix:** Always `extends ResponseEntityExceptionHandler` when you have a catch-all. Then Spring's errors are handled by the parent's **more specific** handlers first. ✅

---

## 🔛 Part 8: A one-line alternative (good to know)

Spring Boot has a setting that turns Problem Details on for **Spring's own** errors:

```properties
spring.mvc.problemdetails.enabled=true
```

It's handy for small apps with **no** own handler. But be careful: with this setting, Spring Boot adds **its own** `ResponseEntityExceptionHandler` — and we tested that it then answers validation errors **before** your `@ExceptionHandler(MethodArgumentNotValidException.class)` gets a chance. You'd get `"detail":"Invalid request content."` **without** your `errors` map. 😕

👉 **Rule:** If you write your own complaints desk that **extends `ResponseEntityExceptionHandler`** (like we did), you **don't** need this setting. Spring Boot sees your desk and doesn't add its own. ✅

---

## 💻 Mini project: The Book API, part 10 📚 (the finale!)

1. Remove `@ResponseStatus` from `BookNotFoundException` and `InvalidBookException`.
2. Add two handlers to the **same** `GlobalExceptionHandler`:
   - `BookNotFoundException` → **404**, title `"Book not found"`
   - `InvalidBookException` → **400**, title `"Invalid book"`
3. Test: a missing book, a book from the future, and a book with an empty title.

<details>
<summary>Click to see the answer</summary>

```java
@ExceptionHandler(BookNotFoundException.class)
public ProblemDetail handleBookNotFound(BookNotFoundException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
    problem.setTitle("Book not found");
    return problem;
}

@ExceptionHandler(InvalidBookException.class)
public ProblemDetail handleInvalidBook(InvalidBookException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, ex.getMessage());
    problem.setTitle("Invalid book");
    return problem;
}
```

Real answers:

`GET /api/books/9`

```json
{"detail":"Book with id 9 was not found","instance":"/api/books/9","status":404,"title":"Book not found"}
```

`POST /api/books` with `{"title":"Future Book","author":"Time Traveler","year":3000}`

```json
{"detail":"The year 3000 is in the future","instance":"/api/books","status":400,"title":"Invalid book"}
```

`POST /api/books` with `{"title":"","author":"","year":1200}`

```json
{"detail":"The request has 3 invalid field(s)","instance":"/api/books","status":400,"title":"Invalid data","errors":{"author":"Author is required","title":"Title must be 1 to 100 characters long","year":"Year must be 1450 or later"}}
```

`POST /api/books` with The Gruffalo (1999) → **201**:

```json
{"id":4,"title":"The Gruffalo","author":"Julia Donaldson","year":1999,"ageInYears":27}
```

**One complaints desk for students AND books.** 🏢 That's the power of **global** error handling! 🎉

</details>

---

## ✋ Try it yourself

**Task 1:** Add a field `"timestamp"` (the current time) to **every** problem from your own handlers. Tip: `problem.setProperty("timestamp", Instant.now())` (import `java.time.Instant`).

<details>
<summary>Click to see the answer</summary>

Add the line before each `return problem;` (or write a small private helper method that all handlers use):

```java
problem.setProperty("timestamp", Instant.now());
```

We tested it — the answer gets an extra field:

```json
{"detail":"Student with id 99 was not found","instance":"/api/students/99","status":404,"title":"Student not found","timestamp":"2026-10-11T04:53:13.480810Z"}
```

(An `Instant` is a moment in **UTC** time — the `Z` at the end means UTC. Chapter 39.) Extra fields are allowed in Problem Details — that's what `setProperty` is for. 😊

</details>

**Task 2:** Write a handler for `IllegalArgumentException` that answers **400** with the exception's message, and title `"Bad argument"`. Why is it OK to show `ex.getMessage()` here, but not in the catch-all?

<details>
<summary>Click to see the answer</summary>

```java
@ExceptionHandler(IllegalArgumentException.class)
public ProblemDetail handleBadArgument(IllegalArgumentException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, ex.getMessage());
    problem.setTitle("Bad argument");
    return problem;
}
```

It's (mostly) OK when **you** throw `IllegalArgumentException` with messages **you** wrote for clients. But the catch-all handles **unknown** errors from **anywhere** — even from libraries — and their messages may contain secrets (file paths, database names...). So the catch-all always uses a **safe, fixed** message. 🔒

</details>

**Task 3:** Which handler answers each exception?
a) `StudentNotFoundException` b) `NullPointerException` c) `MethodArgumentNotValidException` d) `MethodArgumentTypeMismatchException` (for `/api/students/abc`)

<details>
<summary>Click to see the answer</summary>

a) `handleStudentNotFound` (404)
b) `handleEverythingElse` (500) — no more specific handler exists
c) our **override** `handleMethodArgumentNotValid` (400 with `errors`)
d) the parent `ResponseEntityExceptionHandler` (400, "Failed to convert 'id' with value: 'abc'")

</details>

---

## ⚠️ Common mistakes

### Mistake 1: The desk is outside the base package

`com.example.errors.GlobalExceptionHandler` → never found → nothing changes. 🙈 **Fix:** Put it in `com.example.school.exception` (or anywhere **below** the base package — Chapter 50).

### Mistake 2: Returning a plain text or record from the handler

```java
@ExceptionHandler(StudentNotFoundException.class)
public String handle(StudentNotFoundException ex) {
    return "not found";        // 😕 status 200?!
}
```

The answer would be `200 OK` with the text "not found" — the status code is **lost**! **Fix:** Return a **`ProblemDetail`** (it carries its own status) or a `ResponseEntity` (Chapter 62).

> 💡 You may also see **`@ControllerAdvice`** (without "Rest") in other projects. We tested it: when your handlers return `ProblemDetail` or `ResponseEntity`, it works the same. But **`@RestControllerAdvice`** is the safe choice for REST APIs — like `@RestController` vs `@Controller` (Chapter 52).

### Mistake 3: A catch-all without `extends ResponseEntityExceptionHandler`

400s and 404s turn into **500**s (Part 7). 🪤 **Fix:** Extend `ResponseEntityExceptionHandler`.

### Mistake 4: Two handlers for the same exception

`@ExceptionHandler(MethodArgumentNotValidException.class)` **and** `extends ResponseEntityExceptionHandler` → "Ambiguous @ExceptionHandler method" → the app **doesn't start**. **Fix:** **Override** `handleMethodArgumentNotValid` instead (Part 4).

### Mistake 5: Sending stack traces or secret messages to clients

```java
problem.setDetail(ex.toString());   // ❌ might show passwords, paths, SQL...
```

**Fix:** Clients get a **safe** message. The **log** gets the details (`logger.error(..., ex)`). 🔒

### Mistake 6: Forgetting to remove `@ResponseStatus` from exceptions

It still works (your handler wins), but it's confusing to have the status in **two** places. **Fix:** One place: the complaints desk. 🏢

---

## ✅ Summary

- **Problem Details** (RFC 9457) is the standard error format: `title`, `status`, `detail`, `instance` (+ your own fields), with `Content-Type: application/problem+json`. Spring's class: **`ProblemDetail`**.
- **`@RestControllerAdvice`** = a **global complaints desk** 🏢 for all controllers.
- **`@ExceptionHandler(SomeException.class)`** = "when this exception happens, build the answer here". Return a `ProblemDetail`.
- Exceptions stay **plain** (no HTTP). The desk decides the status: not found → **404**, email used → **409**, invalid → **400**, unexpected → **500**.
- Validation errors: read `ex.getBindingResult().getFieldErrors()` → a map **field → message** → `problem.setProperty("errors", errors)`. 📋
- **`extends ResponseEntityExceptionHandler`** → **Spring's own** errors (wrong type, broken JSON, 404, 405, 415...) also become Problem Details. Then **override** `handleMethodArgumentNotValid` (don't add a second `@ExceptionHandler` for it).
- A **catch-all** `@ExceptionHandler(Exception.class)`: log the details (`logger.error`), send a **safe** message. Only **with** `extends ResponseEntityExceptionHandler`! 🪤
- Now **every** error in your API looks the same. 💌

---

## ❓ Quiz

1. What are the four main fields of a Problem Details body?
2. What does `@RestControllerAdvice` do?
3. What does `@ExceptionHandler(StudentNotFoundException.class)` mean?
4. Why did we remove `@ResponseStatus` from our exception classes?
5. Which exception does Spring throw when `@Valid` finds broken rules?
6. How do you get the list of field errors from it?
7. Why do we extend `ResponseEntityExceptionHandler`?
8. What happens if you keep your own `@ExceptionHandler(MethodArgumentNotValidException.class)` **and** extend `ResponseEntityExceptionHandler`?
9. Why must the catch-all handler **not** send `ex.getMessage()` to the client?
10. What goes wrong with a catch-all **without** `extends ResponseEntityExceptionHandler`?

<details>
<summary>Click to see the answers</summary>

1. `title`, `status`, `detail`, `instance` (and optionally `type`).
2. It makes a class a global error handler: its `@ExceptionHandler` methods work for all controllers.
3. "When a `StudentNotFoundException` is thrown anywhere in a request, call this method to build the response."
4. So the status is decided in one central place (the handler), and the exceptions don't need to know about HTTP.
5. `MethodArgumentNotValidException`
6. `ex.getBindingResult().getFieldErrors()` — then `getField()` and `getDefaultMessage()` for each.
7. So Spring's own errors (wrong types, broken JSON, unknown URLs, wrong methods...) are also answered as Problem Details, and a catch-all doesn't swallow them.
8. The app doesn't start: "Ambiguous @ExceptionHandler method". Override `handleMethodArgumentNotValid` instead.
9. Because unexpected errors can contain secret details (file paths, database info...). Log them; send a safe message.
10. It catches Spring's own errors too, so 400s and 404s become 500s.

</details>

---

## 🎉 Part 8 complete!

You built a **complete, professional REST API**! 🏆 Look at everything it can do:

- ✅ **CRUD**: list, get, create, replace, change, delete — `@GetMapping`, `@PostMapping`, `@PutMapping`, `@PatchMapping`, `@DeleteMapping`
- ✅ **Path variables** (`/students/5`) and **request parameters** (`?minAge=12&sort=name`)
- ✅ **JSON bodies** with `@RequestBody`
- ✅ The **right status codes**: 200, 201 + `Location`, 204, 400, 404, 405, 409, 415, 500 — with `ResponseEntity`
- ✅ **Layers**: Controller → Service → Repository
- ✅ **DTOs** that protect private data 🛡️
- ✅ **Validation** at the door 💂
- ✅ **Beautiful error messages** in the Problem Details standard 💌
- ✅ And you built a **second API** (books 📚) all by yourself!

### 🏁 Where are we?

```
 Part 1 ✅ Getting ready          Part 6 ✅ How the web works
 Part 2 ✅ Java basics            Part 7 ✅ Spring Boot basics
 Part 3 ✅ Objects (OOP)          Part 8 ✅ Building REST APIs  ← you are here! 🎉
 Part 4 ✅ More Java              Part 9 ⏳ Databases           ← next!
 Part 5 ✅ Tools
```

There's just **one** big problem left: **restart the app, and all your students are gone!** 💨 Our "storage room" is only a map in memory.

In **Part 9**, you'll learn about **databases** 🗄️: what they are, how to talk to them with **SQL**, and how **Spring Data JPA** lets you save Java objects with almost **no code**. Remember the secret from Chapter 63? You'll replace the whole `StudentRepository` class with **one line**. 🤯

Let's go! 🚀

---

[⬅ Previous chapter](65-validation.md) | [Table of Contents](../README.md) | [Next chapter: What is a database? ➡](../part-09-databases/67-what-is-a-database.md)
