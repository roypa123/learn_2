# Chapter 60 – Sending data: `@PostMapping` and `@RequestBody`

[⬅ Previous chapter](59-request-params.md) | [Table of Contents](../README.md) | [Next chapter ➡](61-put-delete.md)

---

## 🎯 Goal

Until now, our API could only **give** data. Today it learns to **receive** data! 📥 We'll **create new students**.

At the end of this chapter you will know:

- How a client **sends** data: a **POST** request with a **JSON body**
- How to receive it with **`@PostMapping`** and **`@RequestBody`**
- How Spring turns **JSON → Java object** automatically (the opposite of Chapter 52!) ✨
- How the **server** gives each new student an **id**
- How to send POST requests with **curl** and **Postman** (and the Windows traps!)
- What happens with **broken JSON**, a **missing Content-Type**, missing fields, and extra fields

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Request body** | The **data** a client sends **inside** the request (not in the URL). Usually JSON. 📦 |
| **`@PostMapping`** | "Call this method for **POST** requests." POST = **create** something new. |
| **`@RequestBody`** | "Read the request body (JSON) and turn it into **this** Java object." |
| **Deserialize** | Turn **text** (JSON) into a Java **object**. (The opposite of **serialize** — Chapter 52.) |
| **`Content-Type`** | A header that says **what kind** of body it is: `application/json`. (Chapter 44) |
| **415 Unsupported Media Type** | "I don't understand this **kind** of body." |
| **Payload** | Another word for the data in the body. |

---

## 📖 Story: The new-student form 📝

A new boy, **Omar**, wants to join the school. His parents go to the office window and hand in a **form** 📝:

```
┌───────────────────────────┐
│ NEW STUDENT FORM          │
│ Name:  Omar Ali           │
│ Email: omar@school.com    │
│ Age:   12                 │
│ Student number: ________  │  ← left EMPTY! The office fills this in.
└───────────────────────────┘
```

The secretary 👩‍💼:

1. **reads** the form,
2. writes the **next free student number** on it (4!),
3. puts it in the **filing cabinet** 🗄️,
4. gives back a **copy** with the number: "Welcome! You're student number 4." 🎉

In HTTP:

| School office | HTTP |
|---|---|
| Handing in a form | A **POST** request |
| The form | The **request body** (JSON) |
| "This is a new-student form" | `Content-Type: application/json` |
| The secretary writes the number | The **server** gives the **id** |
| The copy with the number | The **response**: the created student, **with** its id |

---

## 📦 Part 1: What a POST request looks like

Here's the request a client sends (you saw this in Chapter 46):

```http
POST /api/students HTTP/1.1
Content-Type: application/json

{
  "name": "Omar Ali",
  "email": "omar@school.com",
  "age": 12
}
```

| Part | Meaning |
|---|---|
| `POST /api/students` | "**Create** something new in the students collection." |
| `Content-Type: application/json` | ⭐ "My body is **JSON**." Without this, the server doesn't know how to read it! |
| *(empty line)* | End of headers. |
| `{ "name": ... }` | ⭐ The **body**: the new student's data. **No `id`** — the server gives it! |

---

## 💻 Part 2: Receive it with `@PostMapping` + `@RequestBody`

Add a **counter** for the ids and a new method to `StudentController`:

```java
private long nextId = 4;

@PostMapping
public Student create(@RequestBody Student newStudent) {
    Student student = new Student(nextId, newStudent.name(), newStudent.email(), newStudent.age());
    nextId++;
    students.add(student);
    return student;
}
```

Imports:

```java
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
```

(Put the `nextId` field **under** the `students` list.)

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `private long nextId = 4;` | The **next free id**. We have students 1, 2, 3 — so the next one is 4. (A `long`, not `Long`, because it's **never** empty.) |
| `@PostMapping` | ⭐ "Call this method for **POST** `/api/students`." (No path → the class path.) |
| `@RequestBody Student newStudent` | ⭐⭐ "Read the **JSON body** and turn it into a `Student` object." Spring (with **Jackson**) does it for you! |
| `new Student(nextId, newStudent.name(), ...)` | Make a **new** record with **our** id and the client's name, email and age. (Records can't be changed — Chapter 29 — so we create a new one.) |
| `nextId++;` | The next student gets the next number: 5, 6, 7... |
| `students.add(student);` | Put it in the "filing cabinet". (This is why we needed `new ArrayList<>(...)` in Chapter 57! A `List.of` list would crash here. 💥) |
| `return student;` | Send back the created student — **with** its new id → JSON. |

### ✨ JSON → Java, automatically

In Chapter 52, Jackson turned **Java → JSON** (for the answer). Now it does the **opposite**:

```
 JSON body                                         Java object
 ─────────                                         ───────────
 {                                                 new Student(
   "name": "Omar Ali",          ── Jackson ──►        null,            ← no "id" in JSON → null
   "email": "omar@school.com",     (by the names!)    "Omar Ali",
   "age": 12                                          "omar@school.com",
 }                                                    12)
```

Jackson matches the JSON **keys** to the record **components** by **name**: `"name"` → `name`, `"age"` → `age`. The `id` isn't in the JSON, so it's **`null`** (another reason for `Long` — Chapter 57!). 🧠

---

## ⌨️ Part 3: Send a POST with curl

The browser's address bar **can't** send POST requests (Chapter 47). So we use curl or Postman.

### In Git Bash (recommended) 🐚

```bash
curl -i -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Omar Ali","email":"omar@school.com","age":12}'
```

| Part | Meaning |
|---|---|
| `-i` | Show the status and headers too. |
| `-X POST` | Use the **POST** method. |
| `-H "Content-Type: application/json"` | ⭐ Add the header: "my body is JSON". |
| `-d '{...}'` | The **body** (`d` = data). In **single quotes** `' '`, so the double quotes inside are kept. |
| `\` | "The command continues on the next line." |

Real answer:

```
HTTP/1.1 200 
Content-Type: application/json
Content-Length: 61

{"id":4,"name":"Omar Ali","email":"omar@school.com","age":12}
```

🎉 **Omar is student number 4!** Now check `GET /api/students` — there are **4** students. And `/api/students/count` says `4`. ✅

> 🤔 **200?** Hmm. For "created", REST says **201 Created** (Chapter 46). We'll fix that in **Chapter 62** with `ResponseEntity`. For now, 200 works. 😊

### In Windows PowerShell 🪟

Remember Chapter 47's trap: in PowerShell, use **`curl.exe`**, and put the JSON in a **file** — quotes inside quotes are a nightmare there. 😵

1. Create a file **`new-student.json`** (in the folder where your terminal is):

```json
{"name":"Omar Ali","email":"omar@school.com","age":12}
```

2. Send it:

```powershell
curl.exe -i -X POST http://localhost:8080/api/students -H "Content-Type: application/json" -d "@new-student.json"
```

| Part | Meaning |
|---|---|
| `curl.exe` | The real curl (not PowerShell's `curl` shortcut). |
| `-d "@new-student.json"` | ⭐ The `@` means: "read the body **from this file**". |

### 📮 In Postman

1. Choose **POST** and type `http://localhost:8080/api/students`.
2. Click the **Body** tab → choose **raw** → choose **JSON** (in the blue drop-down on the right).
3. Type the JSON:

```json
{
  "name": "Omar Ali",
  "email": "omar@school.com",
  "age": 12
}
```

4. Click **Send**.

```
┌────────────────────────────────────────────────────────────────────┐
│ POST ▾ │ http://localhost:8080/api/students               │ Send │
├────────────────────────────────────────────────────────────────────┤
│ Params  Authorization  Headers  [Body]  ...                        │
│ ○ none  ○ form-data  ○ x-www-form-urlencoded  ● raw   JSON ▾       │
│ 1  {                                                               │
│ 2    "name": "Omar Ali",                                           │
│ 3    "email": "omar@school.com",                                   │
│ 4    "age": 12                                                     │
│ 5  }                                                               │
├────────────────────────────────────────────────────────────────────┤
│ 200 OK                                                             │
│ { "id": 4, "name": "Omar Ali", "email": "omar@school.com", ... }   │
└────────────────────────────────────────────────────────────────────┘
```

Choosing **JSON** in step 2 adds the `Content-Type: application/json` header **for you**. 🎁 (Save it in your **collection** — Chapter 47 — you'll use it a lot!)

---

## 🙅 Part 4: The client can't choose the id

What if a sneaky client **sends** an id? 😈

```bash
curl -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"id":500,"name":"Mia Chen","email":"mia@school.com","age":10}'
```

Real answer:

```json
{"id":5,"name":"Mia Chen","email":"mia@school.com","age":10}
```

**5, not 500!** ✅ Jackson **did** put `500` into `newStudent.id()`... but our code **ignores** it and uses `nextId`. The **server** decides ids. Always. 🛡️

Why does this matter? A client could choose an id that **already exists** — and overwrite another student! Or choose `999999999`. Never trust ids from clients. (In Chapter 64 you'll see an even **better** way: a request object that doesn't even **have** an id field.)

---

## 🧪 Part 5: What can go wrong? (We tested everything!)

Let's be a "bad client" and see how Spring reacts. Each answer is **real**. 🔬

### 1️⃣ Broken JSON

A missing `}` at the end:

```bash
-d '{"name":"Sara",'
```

```
HTTP/1.1 400 
{"timestamp":"...","status":400,"error":"Bad Request","path":"/api/students"}
```

Console:

```
... Resolved [org.springframework.http.converter.HttpMessageNotReadableException: JSON parse error: Unexpected end-of-input within/between Object entries]
```

"**JSON parse error**: unexpected end-of-input" = "the JSON stopped in the middle!" ✂️ Check your brackets and commas (Chapter 45's JSON rules).

### 2️⃣ No `Content-Type` header

```bash
curl -i -X POST http://localhost:8080/api/students -d '{"name":"Sara"}'
```

```
HTTP/1.1 415 
Accept: application/json, application/*+json
{"timestamp":"...","status":415,"error":"Unsupported Media Type","path":"/api/students"}
```

**415 Unsupported Media Type!** Without `-H "Content-Type: ..."`, curl sends `Content-Type: application/x-www-form-urlencoded` (the old style of web forms). Spring says: "I don't read that kind of body." And look at the helpful header **`Accept: application/json, application/*+json`** — "**this** is what I accept!" 🤓

Console:

```
... Resolved [org.springframework.web.HttpMediaTypeNotSupportedException: Content-Type 'application/x-www-form-urlencoded;charset=UTF-8' is not supported]
```

### 3️⃣ A wrong type

```bash
-d '{"name":"Sara","age":"twelve"}'
```

→ **400**. Console: `Cannot deserialize value of type 'int' from String "twelve": not a valid 'int' value`. 🔢❌

### 4️⃣ A missing field

```bash
-d '{"name":"Omar Ali","email":"omar@school.com"}'
```

→ **400**! 😮 Console:

```
... JSON parse error: Cannot map `null` into type `int` (set `DeserializationFeature.FAIL_ON_NULL_FOR_PRIMITIVES` to 'false' to allow)
```

`age` is missing, so Jackson wants to put "nothing" (`null`) into `int age`... but an `int` can't be `null`! So it refuses. (A missing **`String`** field like `email` would just become `null` — no error. 😬 We'll handle that properly with **validation** in Chapter 65.)

### 5️⃣ An extra field

```bash
-d '{"name":"Sara","email":"s@x.com","age":12,"color":"red"}'
```

→ **200** ✅. The unknown field `"color"` is simply **ignored**. Spring Boot is friendly here: clients can send extra things without breaking your API. 😊

### 6️⃣ No body at all

```bash
curl -i -X POST http://localhost:8080/api/students -H "Content-Type: application/json"
```

→ **400**. Console: `Required request body is missing`. 📭

### 📋 Summary table

| Problem | Status | Console says |
|---|---|---|
| Broken JSON | **400** | `JSON parse error` |
| No `Content-Type: application/json` | **415** | `Content-Type '...' is not supported` |
| Wrong type (`"age":"twelve"`) | **400** | `Cannot deserialize value of type 'int'` |
| Missing `int` field | **400** | `Cannot map 'null' into type 'int'` |
| Missing `String` field | **200** 😬 | (nothing — it's just `null`!) |
| Extra unknown field | **200** ✅ | (nothing — ignored) |
| No body | **400** | `Required request body is missing` |

> 💡 **Remember:** When a POST fails with **400**, **look at the console**! The `WARN ... Resolved [...]` line tells you exactly what's wrong. 🔍

---

## 🔗 Part 6: `@RequestBody`, `@PathVariable`, `@RequestParam` — the three helpers

You now know **three** ways to get data from a request. Here they are together:

```
POST /api/students/5/notes?urgent=true          ← path + query
Content-Type: application/json

{"text": "Bring your sports clothes"}           ← body
```

| Data | Where in the request | Label | Example |
|---|---|---|---|
| **Which one** | The **path** | `@PathVariable` | `5` |
| **Small options** | The **query string** | `@RequestParam` | `urgent=true` |
| **Big data** (an object) | The **body** | `@RequestBody` | `{"text": "..."}` |

> 💡 A method can have **many** `@PathVariable`s and `@RequestParam`s, but only **one** `@RequestBody` — a request has only one body. 📦

---

## 💻 Mini project: The Book API, part 4 📚

Add `POST /api/books` to your `BookController`:

- The client sends `title`, `author` and `year`.
- The server gives the id (start at **4**).
- The answer is the created book.

Then add **"The Gruffalo"** by **Julia Donaldson** (**1999**) with curl or Postman, and check `GET /api/books`.

<details>
<summary>Click to see the answer</summary>

```java
private long nextId = 4;

@PostMapping
public Book create(@RequestBody Book newBook) {
    Book book = new Book(nextId, newBook.title(), newBook.author(), newBook.year());
    nextId++;
    books.add(book);
    return book;
}
```

curl (Git Bash):

```bash
curl -i -X POST http://localhost:8080/api/books \
  -H "Content-Type: application/json" \
  -d '{"title":"The Gruffalo","author":"Julia Donaldson","year":1999}'
```

Answer:

```json
{"id":4,"title":"The Gruffalo","author":"Julia Donaldson","year":1999}
```

`GET /api/books/count` → `4`. 🎉 (And after a restart → `3` again. In memory! 💨)

</details>

---

## ✋ Try it yourself

**Task 1:** Add 2 new students with Postman: **"Mia Chen"** (mia@school.com, 10) and **"Leo King"** (leo@school.com, 9). What ids do they get? Then call `GET /api/students?sort=age`. Who is first?

<details>
<summary>Click to see the answer</summary>

If Omar already got id 4, Mia gets **5** and Leo gets **6**. (After a restart, it starts at 4 again!) With `?sort=age`, **Leo (9)** is first, then Mia (10). The new students work with **all** your old endpoints — filters, sorting, `/{id}`... 🎉

</details>

**Task 2:** Send a POST **without** the `Content-Type` header. What status do you get? Which response header tells you what the server accepts?

<details>
<summary>Click to see the answer</summary>

**415 Unsupported Media Type**. The **`Accept`** response header: `Accept: application/json, application/*+json`.

</details>

**Task 3:** Use `curl -i -X OPTIONS http://localhost:8080/api/students`. What changed since Chapter 57?

<details>
<summary>Click to see the answer</summary>

The `Allow` header now includes **POST**: `Allow: POST,GET,HEAD,OPTIONS`. Spring found your new `@PostMapping` for that path! 🤓

</details>

**Task 4:** Add an endpoint `POST /api/students/check` that receives a `Student` and returns the text `"<name> is <age> years old."` — **without** saving anything.

<details>
<summary>Click to see the answer</summary>

```java
@PostMapping("/check")
public String check(@RequestBody Student student) {
    return student.name() + " is " + student.age() + " years old.";
}
```

Sending `{"name":"Zoe","email":"zoe@school.com","age":8}` → `Zoe is 8 years old.` (A POST doesn't **have to** save something. But usually it does. 😊)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `@RequestBody`

```java
@PostMapping
public Student create(Student newStudent)   // ❌ no @RequestBody
```

Spring doesn't read the JSON at all! 🙈 Instead, it tries to fill the record from **query parameters** (like `?name=...&age=...`). We tested it:

- Sending our normal JSON → **400**, because there's no `?age=...` and an `int` can't be empty. The console says `Failed to convert value of type 'null' to required type 'int'`. 😵
- Sending `POST /api/students?name=Omar&age=12` (no JSON) → it "works", with `email: null`. Even more confusing!

**Fix:** Write `@RequestBody`.

### Mistake 2: Forgetting `Content-Type: application/json`

→ **415**. **Fix:** In curl: `-H "Content-Type: application/json"`. In Postman: Body → raw → **JSON**.

### Mistake 3: Wrong JSON names

```json
{"Name": "Omar", "e-mail": "omar@school.com", "age": 12}
```

`"Name"` (capital N) and `"e-mail"` don't match `name` and `email` → they're **ignored** as unknown fields, and you get `null`s. 😮 **Fix:** Use **exactly** the record's names: `name`, `email`, `age`.

### Mistake 4: Trusting the client's id

`new Student(newStudent.id(), ...)` ❌ — the client could overwrite other students. **Fix:** The **server** chooses the id (`nextId`).

### Mistake 5: Single quotes in PowerShell or cmd

`-d '{"name":"Omar"}'` works in **Git Bash**, but **not** in Command Prompt or PowerShell. **Fix:** Use Git Bash, or the `-d "@file.json"` trick, or Postman.

### Mistake 6: An unchangeable list

`List.of(...)` → `students.add(...)` throws `UnsupportedOperationException` → **500**. **Fix:** `new ArrayList<>(List.of(...))` (Chapter 57).

---

## ✅ Summary

- To **create** something, a client sends **POST** with a **JSON body** and the header **`Content-Type: application/json`**.
- **`@PostMapping`** + **`@RequestBody Student newStudent`** → Spring (Jackson) turns the JSON into a Java object (**deserializing**), matching keys to names.
- The **server** gives the id (`nextId`), never the client. 🛡️
- Return the created object — **with** its id — so the client knows it.
- Send POST with **curl** (`-X POST -H "Content-Type: application/json" -d '...'`; in PowerShell: `curl.exe` and `-d "@file.json"`) or **Postman** (Body → raw → JSON).
- Errors: broken JSON → **400**; no Content-Type → **415**; wrong type or missing `int` → **400**; missing `String` → `null` (fix in Chapter 65); extra fields → ignored.
- Three helpers: **`@PathVariable`** (which one), **`@RequestParam`** (options), **`@RequestBody`** (the data object).

---

## ❓ Quiz

1. Which HTTP method do you use to create a new student?
2. What does `@RequestBody` do?
3. Which header must a client send with a JSON body?
4. Why does the server choose the id, and not the client?
5. What status code do you get without the `Content-Type` header?
6. The JSON has `"age"` missing, and `age` is an `int`. What happens? And if `"email"` is missing?
7. The JSON has an extra field `"hobby": "chess"`. What happens?
8. How do you send a JSON body from a **file** with curl?
9. How many `@RequestBody` parameters can one method have?

<details>
<summary>Click to see the answers</summary>

1. **POST**
2. It reads the JSON body of the request and turns it into a Java object.
3. `Content-Type: application/json`
4. So clients can't choose ids that already exist (overwriting others) or strange ids. The server knows which ids are free.
5. **415 Unsupported Media Type**
6. Missing `age` (an `int`) → **400** ("Cannot map `null` into type `int`"). Missing `email` (a `String`) → no error, it becomes `null`.
7. It's ignored. The request works.
8. `-d "@new-student.json"` (the `@` means "read from this file").
9. Only **one** — a request has only one body.

</details>

---

[⬅ Previous chapter](59-request-params.md) | [Table of Contents](../README.md) | [Next chapter: Changing and deleting: PUT and DELETE ➡](61-put-delete.md)
