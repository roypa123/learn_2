# Chapter 65 – Validation: checking the data

[⬅ Previous chapter](64-dtos.md) | [Table of Contents](../README.md) | [Next chapter ➡](66-error-handling.md)

---

## 🎯 Goal

Right now, our API accepts **anything**: an empty name, `"email": "banana"`, an age of `-5`... and a missing age even crashes the server with **500**! 😱 Today we add a **security guard** 💂 at the door: **validation**.

At the end of this chapter you will know:

- What **validation** is, and why you must **never trust** data from clients
- How to add the **Validation** starter to your project
- The most useful **validation labels**: `@NotBlank`, `@NotNull`, `@Size`, `@Min`, `@Max`, `@Email`, `@Pattern`...
- How to turn validation on with **`@Valid`**
- How to write **your own error messages** ✍️
- How to validate **path variables** and **request parameters** too
- What the client gets back when data is wrong (and why it's not perfect yet... 🤔)

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Validation** | **Checking** data before using it: "Is the email a real email? Is the age a number from 5 to 20?" ✅ |
| **Constraint** | A **rule** for one field: "must not be blank", "must be at least 5". |
| **Bean Validation** | The Java **standard** for validation labels (`jakarta.validation`). Spring uses it. |
| **Hibernate Validator** | The library that **does** the checking. It comes with the Validation starter. |
| **`@Valid`** | A label: "Please **check** this object before calling my method." |
| **Blank** | Empty **or only spaces**: `""`, `"   "`. |
| **Regular expression** (regex) | A **pattern** for text, like "only letters" or "5 digits". |

---

## 📖 Story: The security guard 💂

A big concert 🎸 has a **security guard** at the entrance. Before anyone gets in, the guard checks:

- ✅ "Do you have a **ticket**?" (not missing)
- ✅ "Is your ticket **real**?" (the right format)
- ✅ "Are you **old enough**?" (a number between limits)

If something is wrong, the guard says **at the door**: "Sorry, you can't come in — your ticket is for **tomorrow**." The problem never reaches the **stage**. 🎤

Without a guard, anybody walks in... and the problems happen **inside**, where they're much worse. 💥

| Concert | Spring Boot |
|---|---|
| The guard 💂 | **Validation** |
| The rules ("needs a ticket") | Labels like **`@NotBlank`**, **`@Min(5)`** |
| "Check this person!" | **`@Valid`** on the request body |
| "Sorry, you can't come in" | **400 Bad Request** |
| The stage 🎤 | Your **service** — it only gets **good** data |

---

## 🚨 Part 1: Never trust the client!

Who sends data to your API? **Anybody!** 🌍 Your own app, other people's apps, and... **bad people** 🕵️, **buggy apps** 🐛, and **tired humans** who type `"age": "twelwe"`. 😴

Here's what our API accepts **today** (from Chapter 64):

| Bad data | What happens now |
|---|---|
| `"name": ""` | ✅ saved with an **empty** name 😬 |
| `"email": "not-an-email"` | ✅ saved 😬 |
| `"age": -5` | ✅ a student who is **minus five** years old 😂 |
| `"age"` missing | 💥 **500** NullPointerException |

**Golden rule:** 🥇 **Every** piece of data from outside must be **checked** before you use it.

---

## 📦 Part 2: Add the Validation starter

Validation isn't in Spring Web — it's a **separate** starter. Open **`pom.xml`** and add this inside `<dependencies>` (for example, right after the `spring-boot-starter-webmvc` block):

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

Then click **Maven reload** 🔄 (the little "m" button that appears at the top right of the editor — Chapter 49).

| Code | Meaning |
|---|---|
| `spring-boot-starter-validation` | ⭐ The validation starter: the **Bean Validation** labels + **Hibernate Validator** (the library that checks them). |
| *(no `<version>`)* | The Spring Boot parent chooses it (Chapter 41). ✅ |

> 💡 On **start.spring.io**, this dependency is called **"Validation"** (Chapter 49, Task 2). Next time, you can choose it when you create the project!

---

## 🏷️ Part 3: Put rules on the request DTO

Validation rules go on the **request DTO** — the "form" that comes **in** (Chapter 64). Let's start with the simplest version:

**`dto/StudentRequest.java`**

```java
package com.example.school.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record StudentRequest(
        @NotBlank @Size(min = 2, max = 50) String name,
        @NotBlank @Email String email,
        @NotNull @Min(5) @Max(20) Integer age) {
}
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `import jakarta.validation.constraints...` | The labels come from **Jakarta** (the Java standard), not from Spring. |
| `@NotBlank` (on `name`) | ⭐ The name must **not** be `null`, **not** `""`, and **not** only spaces `"   "`. |
| `@Size(min = 2, max = 50)` | The text must be **2 to 50** characters long. |
| `@NotBlank @Email` (on `email`) | Must be there **and** look like an email (`something@something`). |
| `@NotNull` (on `age`) | ⭐ Must **not** be missing. (For numbers, use `@NotNull` — "blank" is only for text.) |
| `@Min(5)` | At least **5**. |
| `@Max(20)` | At most **20**. |

You can put **several** labels on one field — **all** of them must be OK. ✅✅

---

## 🔛 Part 4: Turn it on with `@Valid`

The labels alone do **nothing**! 😮 You must tell Spring **when** to check. Add **`@Valid`** before `@RequestBody` in the controller:

```java
@PostMapping
public ResponseEntity<StudentResponse> create(@Valid @RequestBody StudentRequest request) {
    StudentResponse created = studentService.create(request);
    URI location = URI.create("/api/students/" + created.id());
    return ResponseEntity.created(location).body(created);
}

@PutMapping("/{id}")
public StudentResponse replace(@PathVariable Long id, @Valid @RequestBody StudentRequest request) {
    return studentService.replace(id, request);
}
```

(Import: `jakarta.validation.Valid`.)

| Code | Meaning |
|---|---|
| `@Valid` | ⭐ "Spring, **check** this object's rules **before** calling my method. If anything is wrong, don't call me — answer **400**." 💂 |

### ✅ Test it

Send **really** bad data:

```bash
curl -i -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"","email":"not-an-email","age":3}'
```

```
HTTP/1.1 400 
Content-Type: application/json

{"timestamp":"2026-10-11T04:26:36.388Z","status":400,"error":"Bad Request","path":"/api/students"}
```

✅ **400 Bad Request** — the guard stopped it! 💂 Your service method was **never called**. Nothing was saved.

And the missing age?

```bash
-d '{"name":"Omar Ali","email":"omar@school.com"}'
```

```
HTTP/1.1 400 
```

✅ **400** instead of the **500** crash from Chapter 64! 🎉

### 🔍 But... what exactly was wrong?

The answer only says "Bad Request". 🤔 Which fields? Why? Look at the **console**:

```
... WARN ... Resolved [org.springframework.web.bind.MethodArgumentNotValidException: Validation failed for argument [0] in public org.springframework.http.ResponseEntity<com.example.school.dto.StudentResponse> com.example.school.controller.StudentController.create(com.example.school.dto.StudentRequest) with 4 errors: [Field error in object 'studentRequest' on field 'name': rejected value []; ... default message [size must be between 2 and 50]] [Field error in object 'studentRequest' on field 'name': rejected value []; ... default message [must not be blank]] [Field error in object 'studentRequest' on field 'email': rejected value [not-an-email]; ... default message [must be a well-formed email address]] [Field error in object 'studentRequest' on field 'age': ...
```

(We shortened it with `...` — the real line is **very** long! 😵) Let's find the important parts:

| Part | Meaning |
|---|---|
| `MethodArgumentNotValidException` | "A method argument (our `@RequestBody`) is **not valid**." |
| `with 4 errors` | 4 rules were broken. |
| `on field 'name': rejected value []` | The field `name` had the value `""` (empty)... |
| `default message [size must be between 2 and 50]` | ...which breaks `@Size`... |
| `default message [must not be blank]` | ...and `@NotBlank`. (Two errors for one field!) |
| `on field 'email': rejected value [not-an-email]` + `[must be a well-formed email address]` | The email is wrong. |
| (and the age: `must be greater than or equal to 5`) | `3` is too young. |

So **you** (the developer) can see the details. But the **client** only gets "Bad Request" with **no** details. 😕 That's not very friendly! In **Chapter 66**, we'll send these messages to the client — nicely. 💌

---

## 📚 Part 5: The most useful validation labels

| Label | Works on | Rule | Example |
|---|---|---|---|
| `@NotNull` | anything | not `null` (not missing) | `@NotNull Integer age` |
| `@NotBlank` | text | not `null`, not empty, not only spaces | `@NotBlank String name` |
| `@NotEmpty` | text, lists | not `null`, not empty (spaces are OK) | `@NotEmpty List<String> subjects` |
| `@Size(min, max)` | text, lists | length / number of items | `@Size(min = 2, max = 50)` |
| `@Min(n)` / `@Max(n)` | numbers | at least / at most | `@Min(5) @Max(20)` |
| `@Positive` | numbers | greater than 0 | `@Positive Integer pages` |
| `@PositiveOrZero` | numbers | 0 or more | `@PositiveOrZero Integer stock` |
| `@Email` | text | looks like an email | `@Email String email` |
| `@Pattern(regexp = "...")` | text | matches a **pattern** | see below |
| `@Past` / `@Future` | dates | before / after today | `@Past LocalDate birthday` |
| `@AssertTrue` | booleans | must be `true` | `@AssertTrue Boolean acceptedRules` |

### 🎯 `@NotNull` vs `@NotEmpty` vs `@NotBlank`

| Value | `@NotNull` | `@NotEmpty` | `@NotBlank` |
|---|---|---|---|
| `null` (missing) | ❌ | ❌ | ❌ |
| `""` (empty) | ✅ | ❌ | ❌ |
| `"   "` (spaces) | ✅ | ✅ | ❌ |
| `"Sara"` | ✅ | ✅ | ✅ |

👉 For **text** that people type (names, emails), use **`@NotBlank`** — it's the strictest. For **numbers** and **objects**, use **`@NotNull`**.

### ⚠️ Important: most labels **allow `null`**!

`@Email`, `@Size`, `@Min`, `@Max` and `@Pattern` say **nothing** about `null`. A `null` value **passes** them! 😮 So:

```java
@Min(5) Integer age          // null passes! ⚠️
@NotNull @Min(5) Integer age // null fails ✅
```

That's why we write **`@NotNull` + `@Min`** together for a required number. And it's also **useful** — see PATCH in Part 7! 🩹

### 🔤 A pattern example

A student code like `"AB123"`: two capital letters, then three digits:

```java
@Pattern(regexp = "[A-Z]{2}[0-9]{3}", message = "Code must look like AB123")
String code
```

| Piece | Meaning |
|---|---|
| `[A-Z]` | one capital letter |
| `{2}` | ...two times |
| `[0-9]` | one digit |
| `{3}` | ...three times |

(Regular expressions are a whole world 🌍 — you only need simple ones. Search "regex tester" online to try them.)

---

## ✍️ Part 6: Your own error messages

The default messages ("must not be blank", "size must be between 2 and 50") are OK, but not very **friendly**. Every label has a **`message`** option:

**`dto/StudentRequest.java`** — the final version:

```java
package com.example.school.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record StudentRequest(

        @NotBlank(message = "Name is required")
        @Size(min = 2, max = 50, message = "Name must be 2 to 50 characters long")
        String name,

        @NotBlank(message = "Email is required")
        @Email(message = "Email must be a valid email address")
        String email,

        @NotNull(message = "Age is required")
        @Min(value = 5, message = "Age must be at least 5")
        @Max(value = 20, message = "Age must be at most 20")
        Integer age) {
}
```

### 🔍 What's new

| Code | Meaning |
|---|---|
| `@NotBlank(message = "Name is required")` | Use **this** text when the rule is broken. ✍️ |
| `@Min(value = 5, message = "...")` | With `message`, you must write `value =` for the number. (Without `message`, `@Min(5)` is a shortcut for `@Min(value = 5)`.) |
| One label per line | Easier to read when there are many rules. 😊 |

Now the **console** shows your messages, like `default message [Age must be at least 5]`. And in Chapter 66, the **client** will see them too. 💌

---

## 🩹 Part 7: Validating PATCH

For PATCH, fields may be **missing** (`null` = "don't change" — Chapter 61). So **no** `@NotNull` / `@NotBlank`! But **if** a value is sent, it must still be **good**:

**`dto/StudentPatchRequest.java`**

```java
package com.example.school.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Size;

public record StudentPatchRequest(

        @Size(min = 2, max = 50, message = "Name must be 2 to 50 characters long")
        String name,

        @Email(message = "Email must be a valid email address")
        String email,

        @Min(value = 5, message = "Age must be at least 5")
        @Max(value = 20, message = "Age must be at most 20")
        Integer age) {
}
```

And in the controller:

```java
@PatchMapping("/{id}")
public StudentResponse update(@PathVariable Long id, @Valid @RequestBody StudentPatchRequest patch) {
    return studentService.update(id, patch);
}
```

Here the "`null` passes" rule (Part 5) is **perfect**:

| PATCH body | Result |
|---|---|
| `{"email":"sara.ahmed@school.com"}` | ✅ 200 (name and age are `null` → pass → "don't change") |
| `{"age":42}` | ❌ **400** (42 breaks `@Max(20)`) — we tested it! |
| `{"email":"banana"}` | ❌ **400** (not an email) |

---

## 🔢 Part 8: Validating path variables and parameters

You can put rules **directly** on `@PathVariable` and `@RequestParam` too! For example, ids must be **1 or more**:

```java
@GetMapping("/{id}")
public StudentResponse getById(@PathVariable @Min(1) Long id) {
    return studentService.getById(id);
}
```

(Import: `jakarta.validation.constraints.Min`.)

`GET /api/students/0`:

```
HTTP/1.1 400 
{"timestamp":"2026-10-11T04:26:36.978Z","status":400,"error":"Bad Request","path":"/api/students/0"}
```

✅ **400** — "0 isn't even a possible id". (Before, it was 404 — "no student 0". Both are OK, but 400 tells the client "your request makes no sense". 🤓)

> 💡 For path variables and parameters, Spring checks the labels **automatically** — no `@Valid` needed. `@Valid` is for **objects** like request bodies.

---

## 🏗️ Part 9: Where do the rules go? Validation vs business rules

You have **two** places for rules now. Which rule goes where?

| Kind of rule | Example | Where |
|---|---|---|
| About **one field's format** | "name not blank", "age 5–20", "valid email" | **Validation labels** on the DTO 🏷️ |
| Needs the **database** or **other data** | "email not used by **another** student" | **Service** 👨‍🍳 (Chapter 63) |
| About **several fields together** | "end date after start date" | Usually the **service** |

**Simple test:** 🧪 "Can I check it by looking **only** at this one request?" → a label. "Do I need to look at **other** data?" → the service.

```
 Request ──► 💂 Validation (@Valid)          "Is the form filled out correctly?"
               │  ❌ → 400
               ▼
            👨‍🍳 Service rules                "Is it allowed in our school?"
               │  ❌ → 409 (email used), 404 (not found)...
               ▼
            🧊 Repository                     save ✅
```

---

## 💻 Mini project: The Book API, part 9 📚

Add validation to **`BookRequest`**:

- `title`: required, 1 to 100 characters → messages "Title is required", "Title must be 1 to 100 characters long"
- `author`: required → "Author is required"
- `year`: required, at least **1450** (when book printing started! 🖨️) → "Year is required", "Year must be 1450 or later"

Add `@Valid` in the controller. Test with `{"title":"","author":"","year":1200}` — you should get **400**. Then look in the console: how many errors?

<details>
<summary>Click to see the answer</summary>

```java
package com.example.school.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record BookRequest(

        @NotBlank(message = "Title is required")
        @Size(min = 1, max = 100, message = "Title must be 1 to 100 characters long")
        String title,

        @NotBlank(message = "Author is required")
        String author,

        @NotNull(message = "Year is required")
        @Min(value = 1450, message = "Year must be 1450 or later")
        Integer year) {
}
```

Controller:

```java
@PostMapping
public ResponseEntity<BookResponse> create(@Valid @RequestBody BookRequest request) { ... }
```

`{"title":"","author":"","year":1200}` → **400**. The console shows **4** errors: title is blank, title is too short (an empty title is 0 characters), author is blank, and the year is before 1450.

And the "**not in the future**" rule? It stays in the **service** (`checkYear`) — because "the future" depends on **today's** date, not just on the request. (Bean Validation has `@Past` for **dates**, but our `year` is a simple number.) 📅

</details>

---

## ✋ Try it yourself

**Task 1:** Which label(s) would you use?

a) A phone number must be exactly 10 digits.
b) A list of hobbies must have at least 1 item.
c) The number of pages of a book must be more than 0.
d) A birthday must be in the past.
e) "I accept the school rules" must be checked.

<details>
<summary>Click to see the answer</summary>

a) `@NotBlank @Pattern(regexp = "[0-9]{10}")`
b) `@NotEmpty` (or `@Size(min = 1)`) on the `List`
c) `@NotNull @Positive Integer pages`
d) `@NotNull @Past LocalDate birthday`
e) `@AssertTrue Boolean acceptedRules` (and `@NotNull`)

</details>

**Task 2:** You removed `@Valid` from `create` by mistake. What happens when a client sends `{"name":"","email":"x","age":3}`?

<details>
<summary>Click to see the answer</summary>

**Nothing is checked!** The labels are still on the DTO, but without `@Valid`, Spring doesn't look at them. The bad student is **saved** with `201 Created`. 😱 (And a missing age crashes again with 500.) The labels alone do nothing — `@Valid` is the "**check now!**" button. 💂

</details>

**Task 3:** Is `"   "` (three spaces) a valid name with our rules? What about `" Sara "`?

<details>
<summary>Click to see the answer</summary>

`"   "` → ❌ breaks `@NotBlank` (only spaces). `" Sara "` → ✅ valid (it has letters, and it's 6 characters long). If you don't want the spaces, you could **trim** the name in the service: `request.name().trim()`. ✂️

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `@Valid`

The labels are there, but nothing is checked. **Fix:** `@Valid @RequestBody ...` — every time.

### Mistake 2: Forgetting the starter

Without `spring-boot-starter-validation`, IntelliJ can't even find `jakarta.validation...` — red imports, `cannot find symbol`. **Fix:** Add the dependency and **reload Maven** 🔄.

### Mistake 3: `@NotBlank` on a number

```java
@NotBlank Integer age   // ❌
```

`@NotBlank` is only for **text**. The app compiles and starts, but the first request fails with **500**. We tested it — the console says:

```
UnexpectedTypeException: HV000030: No validator could be found for constraint 'jakarta.validation.constraints.NotBlank' validating type 'java.lang.Integer'. Check configuration for 'age'
```

"I don't know how to check if a **number** is blank!" 🤷 **Fix:** `@NotNull` for numbers.

### Mistake 4: `@Min` without `@NotNull`

`@Min(5) Integer age` → a **missing** age passes the check! Then `null` reaches the model → NullPointerException → 500. 💥 **Fix:** `@NotNull @Min(5)` for required numbers.

### Mistake 5: `int` in the request DTO

```java
@NotNull @Min(5) int age   // 😕
```

An `int` can never be `null`, so `@NotNull` is useless — a missing age gives the confusing Jackson **400** from Chapter 60, without your message. **Fix:** Use `Integer` in request DTOs.

### Mistake 6: Putting rules on the model instead of the DTO

The **request DTO** is what the client sends — put the labels **there**. Different requests can have different rules (POST: all required; PATCH: all optional). 🏷️

---

## ✅ Summary

- **Never trust** data from clients. **Validate** everything at the door. 💂
- Add **`spring-boot-starter-validation`** to `pom.xml` (and reload Maven).
- Put **labels** on the request DTO's fields: `@NotBlank`, `@NotNull`, `@Size`, `@Min`, `@Max`, `@Email`, `@Pattern`, `@Positive`, `@Past`...
- **`@Valid`** before `@RequestBody` turns the checks on. No `@Valid` = no checking!
- Broken rules → **400 Bad Request**; your service is never called. The console (`MethodArgumentNotValidException`) shows the details.
- Text → `@NotBlank`. Numbers/objects → `@NotNull`. Most other labels let `null` **pass** — great for PATCH, but use `@NotNull` for required fields.
- **`message = "..."`** gives friendly error texts.
- Path variables and parameters can have labels too (`@PathVariable @Min(1) Long id`).
- **Format** rules → labels. Rules that need **other data** (email already used) → the **service**.
- The client only sees "Bad Request" without details... **Chapter 66** fixes that! 💌

---

## ❓ Quiz

1. Why must you validate data from clients?
2. Which dependency do you need for validation?
3. What's the difference between `@NotNull`, `@NotEmpty` and `@NotBlank`?
4. What does `@Valid` do? What happens without it?
5. Which labels would you use for a required age between 5 and 20?
6. Does `@Email` reject a `null` email?
7. How do you write your own message for `@Min(5)`?
8. Where does the rule "the email isn't used by another student" belong — a label or the service? Why?
9. What status code does a validation error give?

<details>
<summary>Click to see the answers</summary>

1. Because anybody can send anything — bad people, buggy apps, typing mistakes. Bad data can break your app or your data.
2. `spring-boot-starter-validation`
3. `@NotNull`: not missing. `@NotEmpty`: not missing and not empty. `@NotBlank` (text only): not missing, not empty, and not only spaces.
4. It tells Spring to check the object's rules before calling the method. Without it, nothing is checked.
5. `@NotNull @Min(5) @Max(20) Integer age`
6. No — `null` passes `@Email`. Add `@NotBlank` (or `@NotNull`) to make it required.
7. `@Min(value = 5, message = "Age must be at least 5")`
8. The **service** — it needs to look at **other** data (the other students), not just this request.
9. **400 Bad Request**

</details>

---

[⬅ Previous chapter](64-dtos.md) | [Table of Contents](../README.md) | [Next chapter: Handling errors nicely (@ControllerAdvice) ➡](66-error-handling.md)
