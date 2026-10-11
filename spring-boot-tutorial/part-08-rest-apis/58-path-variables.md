# Chapter 58 – Path variables: `/students/5`

[⬅ Previous chapter](57-rest-controller.md) | [Table of Contents](../README.md) | [Next chapter ➡](59-request-params.md)

---

## 🎯 Goal

Our API can list **all** students. But how do we get **one** student — like student number 2? 🔍

At the end of this chapter you will know:

- What a **path variable** is: the changing part of a URL, like the `5` in `/api/students/5`
- How to read it with **`@PathVariable`**
- How to find **one** student in a list (with a loop, and with a stream)
- Why returning **`null`** is a bad idea ⚠️, and how to answer **404 Not Found** instead
- What happens with a wrong value like `/api/students/abc`
- How to use **two** path variables in one URL
- Why `/api/students/count` and `/api/students/{id}` don't fight 🥊

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Path variable** | A part of the URL **path** that **changes**: `/api/students/`**`5`**. |
| **Placeholder** | `{id}` in `@GetMapping("/{id}")` — "a value will be here". |
| **`@PathVariable`** | A label that says: "Put the value from the path **into this parameter**." |
| **Type conversion** | Spring changes the text `"5"` from the URL into the number `5`. 🔢 |
| **`ResponseStatusException`** | A special exception that says: "Stop and answer with **this** status code." |
| **Specific** | More **exact**. `/count` is more specific than `/{id}` (which matches anything). |

---

## 📖 Story: The lockers 🔐

The school has a long hallway with **lockers**, numbered 1, 2, 3... 🔢

You don't say "please open **a** locker". You say: "Please open locker **number 5**." The **number** tells exactly **which** one.

- Locker 5 exists → it opens. ✅
- Locker 99 doesn't exist → "Sorry, there's no locker 99." ❌ (404)
- Locker "banana" → "That's not even a number!" 🍌😄 (400)

In a URL, the locker number is the **path variable**:

```
/api/students/5
              ↑
        the locker number (path variable)
```

---

## 💻 Part 1: Get one student

Add this method to `StudentController` (from Chapter 57):

```java
@GetMapping("/{id}")
public Student getById(@PathVariable Long id) {
    for (Student student : students) {
        if (student.id().equals(id)) {
            return student;
        }
    }
    return null;   // ⚠️ we'll fix this in Part 3!
}
```

(Add the import: `import org.springframework.web.bind.annotation.PathVariable;`)

Restart → **`http://localhost:8080/api/students/2`**:

```json
{"id":2,"name":"Tom Brown","email":"tom@school.com","age":13}
```

🎉 Tom! Try `/api/students/1` and `/api/students/3` too.

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@GetMapping("/{id}")` | ⭐ The path has a **placeholder** `{id}`. It matches `/api/students/1`, `/api/students/2`, `/api/students/999`... anything in that spot. |
| `@PathVariable Long id` | ⭐ "Take the value from `{id}` in the path, turn it into a `Long`, and put it in the parameter `id`." |
| `for (Student student : students)` | Look at each student (Chapter 14 — the for-each loop). |
| `student.id().equals(id)` | Is this the student we want? ⚠️ We use **`equals`**, not `==`, because `Long` is an **object** (see below). |
| `return student;` | Found! Return it → JSON. |
| `return null;` | Not found... return nothing. (Bad idea — Part 3!) |

### 🔗 How does `{id}` connect to `id`?

By the **name**! The placeholder `{id}` and the parameter `Long id` have the **same name**:

```java
@GetMapping("/{id}")
public Student getById(@PathVariable Long id)
                                          ↑
                         same name as {id} → connected! 🔗
```

If you want a **different** parameter name, write the placeholder name in the label:

```java
@GetMapping("/{id}")
public Student getById(@PathVariable("id") Long studentId)   // also OK
```

### 🔢 Spring converts the type for you

The URL is just **text**: `"2"`. But the parameter is a **`Long`**. Spring **converts** `"2"` → `2L` automatically. You can use `Long`, `Integer`, `int`, `String`, `LocalDate`, even **enums** (Chapter 28) as path variables. ✨

### ⚠️ Why `equals` and not `==`?

Remember **Chapter 9** (strings)? For **objects**, `==` asks "is it the **same object**?", not "is it the **same value**?". `Long` is an object. Two `Long` objects with the value `200` can be **different objects** → `==` says `false`! 😱

| | `==` | `.equals(...)` |
|---|---|---|
| Compares | "Same object?" | "Same value?" ✅ |
| For `Long`, `Integer`, `String` | ❌ can be wrong | ✅ always right |

(For **small** numbers like 1, 2, 3, `==` often *seems* to work, because Java reuses small number objects. That makes the bug even **sneakier** — it breaks only with bigger numbers! 🐛 Always use `equals`.)

---

## 🌊 Part 2: The same with a stream

You know streams (Chapter 36) and `Optional` (Chapter 37). Here's a shorter way to find one student:

```java
@GetMapping("/{id}")
public Student getById(@PathVariable Long id) {
    return students.stream()
            .filter(student -> student.id().equals(id))
            .findFirst()
            .orElse(null);   // ⚠️ still null — fixed in Part 3
}
```

| Code | Meaning |
|---|---|
| `students.stream()` | Go through the students. 🌊 |
| `.filter(student -> student.id().equals(id))` | Keep only the student with this id. |
| `.findFirst()` | Take the first one → an **`Optional<Student>`** (maybe there is one, maybe not). |
| `.orElse(null)` | If there's one, give it; otherwise `null`. |

Both versions do the **same** thing. Use the one you understand better! 😊 (We'll use the stream version from now on.)

---

## 😱 Part 3: The `null` problem — and the 404 fix

What happens if we ask for a student who **doesn't exist**? Try `/api/students/99` with curl:

```
curl -i http://localhost:8080/api/students/99
```

```
HTTP/1.1 200 
Content-Length: 0
```

🤨 **200 OK** — but **empty**!

That's a **lie**. 🤥 "200 OK" means "here's what you asked for". But we have **nothing**. A client (an app, a website) would think everything is fine, then crash when it tries to read an empty answer. 💥

The **correct** answer is **404 Not Found** (Chapter 44). Remember the locker: "Sorry, there's no locker 99." ❌

### ✅ The fix: `ResponseStatusException`

Spring has a special exception: **`ResponseStatusException`**. When you **throw** it, Spring stops your method and answers with the **status code** you choose. 🛑

```java
@GetMapping("/{id}")
public Student getById(@PathVariable Long id) {
    return students.stream()
            .filter(student -> student.id().equals(id))
            .findFirst()
            .orElseThrow(() -> new ResponseStatusException(
                    HttpStatus.NOT_FOUND, "Student with id " + id + " was not found"));
}
```

Imports:

```java
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `.orElseThrow(() -> ...)` | "If the `Optional` is **empty**, **throw** this exception." (Chapter 37) |
| `new ResponseStatusException(...)` | ⭐ An exception that **carries a status code**. |
| `HttpStatus.NOT_FOUND` | The status: **404**. `HttpStatus` is an **enum** (Chapter 28) with all status codes: `OK`, `NOT_FOUND`, `BAD_REQUEST`... |
| `"Student with id " + id + " was not found"` | A message explaining the problem. |

Restart and try again:

```
curl -i http://localhost:8080/api/students/99
```

```
HTTP/1.1 404 
Content-Type: application/json

{"timestamp":"2026-10-11T04:20:43.119Z","status":404,"error":"Not Found","path":"/api/students/99"}
```

✅ **404 Not Found** — the truth! And `/api/students/2` still works with 200. 🎉

> 🤔 **Where is our message "Student with id 99 was not found"?** It's not in the answer! Spring Boot **hides** error messages by default, for safety (messages could show secrets to bad people 🕵️). In **Chapter 66**, you'll learn how to send **nice, safe** error messages. For now, the **status code** is the important part. ✅

---

## 🍌 Part 4: What if the id isn't a number?

Try: `http://localhost:8080/api/students/abc`

```
curl -i http://localhost:8080/api/students/abc
```

```
HTTP/1.1 400 
Content-Type: application/json

{"timestamp":"2026-10-11T04:20:43.560Z","status":400,"error":"Bad Request","path":"/api/students/abc"}
```

**400 Bad Request.** Spring tried to convert `"abc"` into a `Long`... and couldn't. 🍌 Your method was **never even called**.

What exactly went wrong? Look at the **console** in IntelliJ — Spring writes a `WARN` line:

```
... WARN ... Resolved [org.springframework.web.method.annotation.MethodArgumentTypeMismatchException: Method parameter 'id': Failed to convert value of type 'java.lang.String' to required type 'java.lang.Long'; For input string: "abc"]
```

| Part | Meaning |
|---|---|
| `MethodArgumentTypeMismatchException` | "The type of a method parameter didn't match." |
| `Method parameter 'id'` | **Which** parameter. |
| `Failed to convert value of type 'java.lang.String' to required type 'java.lang.Long'` | "I couldn't turn the text into a `Long`." |
| `For input string: "abc"` | **What** the client sent. |

> 💡 **Debugging tip:** When your API answers **400** and you don't know why, look at the **console**. Spring almost always writes a `WARN` line with the reason. 🔍

### 404 or 400? 🤔

| Request | Status | Why |
|---|---|---|
| `/api/students/2` | **200** ✅ | Exists. |
| `/api/students/99` | **404** ❌ | A **correct** id, but no such student. |
| `/api/students/abc` | **400** ❌ | Not even a **correct** id — the client sent nonsense. |

---

## 🥊 Part 5: `/count` vs `/{id}` — who wins?

Wait a moment. 🤔 We have **both**:

```java
@GetMapping("/count")   // /api/students/count
@GetMapping("/{id}")    // /api/students/ANYTHING
```

`{id}` matches **anything**... so does `/api/students/count` go to `getById` with `id = "count"`? Then it would fail with 400! 😱

**No!** It works perfectly. We tested both:

| Request | Answer |
|---|---|
| `GET /api/students/count` | `3` ✅ |
| `GET /api/students/2` | Tom ✅ |

**Rule:** When several paths match, Spring picks the **most specific** one. `/count` is a **fixed word** — very specific. `{id}` is a placeholder — it matches anything, so it's **less** specific. The fixed word wins! 🏆

```
GET /api/students/count
  ├── /count  ← exact word match 🏆 WINS
  └── /{id}   ← "anything" match
```

---

## 🔢🔢 Part 6: Two path variables

A path can have **more than one** variable. Let's make a fun one: "How old will a student be in X years?" 🎂

```java
@GetMapping("/{id}/age-in/{years}")
public String ageIn(@PathVariable Long id, @PathVariable int years) {
    Student student = getById(id);
    return "In " + years + " years, " + student.name() + " will be " + (student.age() + years) + ".";
}
```

`GET /api/students/1/age-in/5`:

```
In 5 years, Sara Ahmed will be 17.
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `"/{id}/age-in/{years}"` | Two placeholders: `{id}` and `{years}`, with the fixed word `age-in` between them. |
| `@PathVariable Long id` | ← from `{id}` (here: `1`) |
| `@PathVariable int years` | ← from `{years}` (here: `5`). A different type — `int` — no problem! |
| `Student student = getById(id);` | We **reuse** our own method! If the student doesn't exist, `getById` throws the 404 exception — and that works here too. 🎉 |
| `(student.age() + years)` | `12 + 5 = 17`. The brackets make Java **add** first, before joining the text (Chapter 9). |

Try `/api/students/99/age-in/5` → **404** (from `getById`). ✅

### 🗺️ This is how "nested resources" look

Remember **Chapter 46**? `/api/students/42/courses` — "the courses **of** student 42". That's the same idea: the first path variable says **which** student, and the rest of the path says **what about** them. You'll build real ones like this in **Part 9** (Chapter 75). 🔗

---

## 💻 Mini project: The Book API, part 2 📚

Continue your `BookController` from Chapter 57:

1. Add **`GET /api/books/{id}`** → one book, or **404** if it doesn't exist.
2. Add **`GET /api/books/{id}/age`** → `"Matilda is 38 years old."` (how many years since the book's year — use `java.time.Year.now().getValue()` for the current year).

<details>
<summary>Click to see the answer</summary>

```java
@GetMapping("/{id}")
public Book getById(@PathVariable Long id) {
    return books.stream()
            .filter(book -> book.id().equals(id))
            .findFirst()
            .orElseThrow(() -> new ResponseStatusException(
                    HttpStatus.NOT_FOUND, "Book with id " + id + " was not found"));
}

@GetMapping("/{id}/age")
public String age(@PathVariable Long id) {
    Book book = getById(id);
    int years = Year.now().getValue() - book.year();
    return book.title() + " is " + years + " years old.";
}
```

Imports: `java.time.Year`, `org.springframework.http.HttpStatus`, `org.springframework.web.bind.annotation.PathVariable`, `org.springframework.web.server.ResponseStatusException`.

Answers (in the year 2026):

- `GET /api/books/2` → `{"id":2,"title":"The Hobbit","author":"J.R.R. Tolkien","year":1937}`
- `GET /api/books/1/age` → `Matilda is 38 years old.`
- `GET /api/books/7` → **404**
- `GET /api/books/one` → **400**

(Your number of years depends on the current year! 📅)

</details>

---

## ✋ Try it yourself

**Task 1:** Add `GET /api/students/{id}/email` that returns only the email of one student (or 404).

<details>
<summary>Click to see the answer</summary>

```java
@GetMapping("/{id}/email")
public String email(@PathVariable Long id) {
    return getById(id).email();
}
```

`/api/students/3/email` → `lina@school.com`. Reusing `getById` gives us the 404 for free! ♻️

</details>

**Task 2:** What status code do you get for each request? Guess first, then test!

a) `/api/students/3` b) `/api/students/4` c) `/api/students/-1` d) `/api/students/1.5` e) `/api/students/names`

<details>
<summary>Click to see the answer</summary>

a) **200** (Lina) b) **404** (no student 4) c) **404** (`-1` **is** a valid `Long`, but no student has it) d) **400** (`1.5` is not a whole number — can't become a `Long`) e) **200** — the fixed word `/names` wins over `/{id}` (Chapter 57's endpoint)!

</details>

**Task 3:** Change `getById` so it returns `null` again. Then call `/api/students/99/age-in/5`. What happens? Why is that even worse?

<details>
<summary>Click to see the answer</summary>

`getById(99)` returns `null`, and then `student.name()` crashes with a **`NullPointerException`** → **500 Internal Server Error**! 💥 The client sees "server error" — but the real problem was just "student not found". That's why we **throw** a 404 instead of returning `null`. (Change it back! 😉)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `@PathVariable`

```java
@GetMapping("/{id}")
public Student getById(Long id) { ... }    // ❌ no @PathVariable!
```

No error message! But Spring doesn't know the parameter should come from the path. It looks for `?id=...` in the URL instead (Chapter 59), doesn't find it, and `id` is **`null`**. We tested it: `id` was `null` even for `/api/students/5`. So you get **404** for **every** student. 😵 **Fix:** Always write `@PathVariable`.

### Mistake 2: Different names

```java
@GetMapping("/{studentId}")
public Student getById(@PathVariable Long id)   // ❌ {studentId} ≠ id
```

The app starts, but **every call** fails with **500**, and the console says:

```
Required URI template variable 'id' for method parameter type Long is not present
```

"I looked for `{id}` in the path, but there's only `{studentId}`!" **Fix:** Use the same name, or `@PathVariable("studentId") Long id`.

### Mistake 3: Comparing `Long` with `==`

```java
if (student.id() == id)      // ❌ works for small numbers, breaks for big ones!
if (student.id().equals(id)) // ✅
```

### Mistake 4: Returning `null` for "not found"

`200 OK` with an empty body — a lie! 🤥 **Fix:** Throw `new ResponseStatusException(HttpStatus.NOT_FOUND, "...")`.

### Mistake 5: Forgetting the `/` between parts

```java
@GetMapping("/{id}age-in/{years}")    // ❌ missing "/" before age-in
```

Now the URL must look like `/api/students/1age-in/5` 😵. **Fix:** `"/{id}/age-in/{years}"`.

---

## ✅ Summary

- A **path variable** is the changing part of a URL path: `/api/students/`**`5`**.
- `@GetMapping("/{id}")` + `@PathVariable Long id` → Spring puts `5` into `id`, **converting** the type for you.
- Names must match: `{id}` ↔ `id`, or use `@PathVariable("id")`.
- Compare `Long` values with **`equals`**, never `==`.
- Don't return `null` (that's a lying **200**). Throw **`ResponseStatusException(HttpStatus.NOT_FOUND, ...)`** → **404**.
- A value that can't be converted (`/abc`) → **400**, and a `WARN` line in the console explains why. 🔍
- Fixed words (`/count`) beat placeholders (`/{id}`) — the **most specific** path wins. 🏆
- A path can have **several** variables: `/{id}/age-in/{years}`.

---

## ❓ Quiz

1. In `/api/students/7`, what is the path variable?
2. What does `@PathVariable` do?
3. Your method has `@GetMapping("/{bookId}")` and `@PathVariable Long id`. What's wrong? Give two fixes.
4. Why is returning `null` for a missing student a bad idea?
5. Which status code does `/api/students/99` give (no student 99)? And `/api/students/xyz`?
6. Where do you look to find out **why** you got a 400?
7. Both `@GetMapping("/count")` and `@GetMapping("/{id}")` exist. Which method answers `/api/students/count`? Why?
8. Why should you use `equals` and not `==` to compare two `Long` values?

<details>
<summary>Click to see the answers</summary>

1. `7`
2. It takes the value from the placeholder in the path (like `{id}`), converts it to the parameter's type, and puts it into the parameter.
3. The names don't match. Fix 1: rename the placeholder to `{id}`. Fix 2: write `@PathVariable("bookId") Long id`.
4. The client gets **200 OK** with an empty body — a lie. It should get **404 Not Found**. (And other code that uses the result may crash with a `NullPointerException`.)
5. `/api/students/99` → **404**. `/api/students/xyz` → **400**.
6. In the **console** — Spring writes a `WARN` line with the reason.
7. The `count()` method — a fixed word is more specific than a placeholder, and the most specific match wins.
8. `Long` is an object: `==` checks "same object?", which can be `false` even when the numbers are the same. `equals` checks the **value**.

</details>

---

[⬅ Previous chapter](57-rest-controller.md) | [Table of Contents](../README.md) | [Next chapter: Request parameters: ?name=Ali ➡](59-request-params.md)
