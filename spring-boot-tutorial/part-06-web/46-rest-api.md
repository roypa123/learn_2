# Chapter 46 – What Is a REST API?

[⬅ Previous chapter](45-json.md) | [Table of Contents](../README.md) | [Next chapter ➡](47-postman-and-curl.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What an **API** is
- What **REST** means, in simple words
- What a **resource** is, and how to name **URLs** well
- How HTTP **methods** + **URLs** + **status codes** work together
- How to design a complete **Student API** on paper ✏️
- **Path** vs. **query** parameters
- **Filtering**, **sorting** and **pagination**
- How to return **errors** nicely
- **Versioning** your API (`/api/v1/...`)

> 🌱 **This is the plan for everything we build in Part 8!** In Spring Boot, you'll turn each line of the API table below into a Java method. Design first, code later. ✏️ → ☕

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **API** | *Application Programming Interface.* A list of things a program **offers** to other programs — and the rules for asking. Like a **menu**. 📋 |
| **REST** | *REpresentational State Transfer.* A popular **style** (a set of good habits) for building web APIs with HTTP. |
| **RESTful** | "Following the REST style." |
| **Resource** | A **thing** your API is about: a student, a book, an order. |
| **Collection** | A **group** of resources: all students. |
| **Endpoint** | One **method + URL** combination: `GET /api/students`. |
| **Representation** | How a resource **looks** when sent: usually JSON. |
| **Pagination** | Sending a big list **page by page**. 📄📄📄 |
| **Versioning** | Giving your API a version number, so you can change it later without breaking old clients. |

---

## 📖 Story: The restaurant menu 📋

Back to our restaurant (Chapter 43)! 🍽️

You don't walk into the kitchen and cook yourself. You use the **menu**. The menu tells you:

- **What** you can order (pizza, pasta, salad...)
- **How** to order ("say the number of the dish")
- **What you'll get** (a plate of food, or "sorry, sold out")

The menu is the **API** of the restaurant. It **hides** how the kitchen works inside, and **offers** a simple, clear way to get things. 📋

**REST** is a set of **good habits** for writing a menu that **every** customer understands immediately — because **all** REST menus follow the **same** style. 😊

```
 Without rules:                       With REST:
 "/getAllTheStudentsPlease"           GET    /api/students
 "/student_create.php"                POST   /api/students
 "/deleteStudent?id=5"                DELETE /api/students/5
 "/updateStudentNow?id=5"             PUT    /api/students/5
  → every API different 😵             → every API the same shape 😌
```

---

## 🔌 Part 1: What is an API?

**API** = Application **Programming** **Interface**.

- **Interface** — a "**connection point**" (remember Java interfaces in Chapter 25: a **promise** of what's offered!).
- **Programming** — it's used by **programs**, not directly by people.

Examples of APIs you use **every day** without knowing:

| App | Uses the API of... |
|---|---|
| 🌦️ A weather app | a weather service ("give me the weather for Cairo") |
| 🗺️ A taxi app | a map service ("how far is it from A to B?") |
| 🛒 An online shop | a payment service ("charge 50 dollars to this card") |
| 📱 Instagram app | Instagram's own server ("give me the newest posts") |

A **web API** (or **HTTP API**) is an API you talk to with **HTTP requests** (Chapter 44), usually sending and receiving **JSON** (Chapter 45).

```
  📱 Phone app    ──┐
  🌐 Web page     ──┼──►  🌱 YOUR API  ──►  🗄️ database
  🖥️ Other server ──┘    (Spring Boot)
```

👉 **One** backend API can serve **many** different frontends: a website, an Android app, an iPhone app... (And in the **Blazor** book, your Blazor app will call a Spring Boot API! 🎉)

---

## 🧭 Part 2: REST in 5 simple rules

REST has a long theory, but in practice it means these **5 habits**:

| # | Rule | In short |
|---|---|---|
| 1 | Everything is a **resource** with a **URL** | `/api/students/42` = "student 42" |
| 2 | Use **HTTP methods** for actions | GET read, POST create, PUT replace, PATCH change, DELETE remove |
| 3 | Use **status codes** for results | 200, 201, 204, 400, 404... |
| 4 | Send **representations** (usually JSON) | `{ "id": 42, "name": "Sara" }` |
| 5 | Be **stateless** | every request carries everything needed (Chapter 44) |

That's REST! 🎉 The rest of this chapter shows how to use these rules well.

---

## 🏷️ Part 3: Resources and URLs — use NOUNS, not verbs

A **resource** is a **thing** (a noun): student, course, book, order, user.

### ✅ Rule: URLs are **nouns**, the **method** is the verb

| ❌ Bad (verbs in the URL) | ✅ Good (method + noun) |
|---|---|
| `GET /getStudents` | `GET /api/students` |
| `POST /createStudent` | `POST /api/students` |
| `GET /getStudentById?id=42` | `GET /api/students/42` |
| `POST /updateStudent` | `PUT /api/students/42` |
| `GET /deleteStudent?id=42` 😱 | `DELETE /api/students/42` |

📖 The URL says **what** (the thing). The method says **what to do** with it. Like a sentence: **DELETE** (verb) **student 42** (noun). 🗣️

### ✅ Naming habits

| Habit | ✅ Good | ❌ Bad |
|---|---|---|
| **Plural** nouns for collections | `/students` | `/student` |
| **Small letters** | `/students` | `/Students` |
| Words joined with **`-`** (kebab-case) | `/school-classes` | `/schoolClasses`, `/school_classes` |
| An **ID** after the collection | `/students/42` | `/students?id=42` (for one specific item) |
| A common **prefix** for the API | `/api/students` | — |
| No file endings | `/students` | `/students.json` |

### Collection and item

```
 /api/students          ← the COLLECTION (all students) 📚
 /api/students/42       ← ONE ITEM (student number 42) 📘
```

### Nested resources (relationships)

When something **belongs to** something else:

```
 /api/students/42/courses        ← the courses of student 42
 /api/courses/7/students         ← the students in course 7
 /api/orders/1001/items          ← the items in order 1001
```

> 💡 Don't nest too deep. `/api/schools/1/classes/5/students/42/grades/3` is too long 😵. Usually **1 level** of nesting is enough.

---

## 🎯 Part 4: Methods + URLs + status codes — the full picture

For **one** resource (students), here are the **5 standard endpoints**. Learn this table — it's the heart of REST! ❤️

| Action | Method | URL | Request body | Success status | Response body |
|---|---|---|---|---|---|
| List all | `GET` | `/api/students` | — | **200 OK** | array of students |
| Get one | `GET` | `/api/students/{id}` | — | **200 OK** | one student |
| Create | `POST` | `/api/students` | new student (JSON) | **201 Created** + `Location` header | the created student (with its new id) |
| Replace | `PUT` | `/api/students/{id}` | full student (JSON) | **200 OK** | the updated student |
| Change part | `PATCH` | `/api/students/{id}` | only the changed fields | **200 OK** | the updated student |
| Delete | `DELETE` | `/api/students/{id}` | — | **204 No Content** | — |

`{id}` is a **placeholder**: `/api/students/42`, `/api/students/7`...

### And when things go wrong

| Situation | Status |
|---|---|
| The JSON is broken, or a required field is missing | **400 Bad Request** |
| Not logged in | **401 Unauthorized** |
| Logged in, but not allowed (not an admin) | **403 Forbidden** |
| Student `{id}` doesn't exist | **404 Not Found** |
| The email is already used by another student | **409 Conflict** |
| A bug in the server 🐛 | **500 Internal Server Error** |

---

## 🎬 Part 5: A full conversation with the Student API

Let's see **real** requests and responses (this is exactly what you'll build in Part 8!).

### 1️⃣ Create a student

**Request:**

```http
POST /api/students HTTP/1.1
Content-Type: application/json

{
  "name": "Sara Ahmed",
  "email": "sara@school.com",
  "age": 12
}
```

**Response:**

```http
HTTP/1.1 201 Created
Location: /api/students/1
Content-Type: application/json

{
  "id": 1,
  "name": "Sara Ahmed",
  "email": "sara@school.com",
  "age": 12
}
```

👉 The client did **not** send an `id` — the **server** gives the new student its id (often the database does). The `Location` header says where to find the new student. 🗺️

### 2️⃣ List all students

**Request:**

```http
GET /api/students HTTP/1.1
Accept: application/json
```

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  { "id": 1, "name": "Sara Ahmed", "email": "sara@school.com", "age": 12 },
  { "id": 2, "name": "Tom Brown",  "email": "tom@school.com",  "age": 13 }
]
```

### 3️⃣ Get one student

```http
GET /api/students/2 HTTP/1.1
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{ "id": 2, "name": "Tom Brown", "email": "tom@school.com", "age": 13 }
```

### 4️⃣ Get a student that doesn't exist

```http
GET /api/students/99 HTTP/1.1
```

```http
HTTP/1.1 404 Not Found
Content-Type: application/problem+json

{
  "type": "about:blank",
  "title": "Not Found",
  "status": 404,
  "detail": "Student with id 99 was not found",
  "instance": "/api/students/99"
}
```

(See Part 8 for this error format.)

### 5️⃣ Change Tom's email (PATCH)

```http
PATCH /api/students/2 HTTP/1.1
Content-Type: application/json

{ "email": "tom.brown@school.com" }
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{ "id": 2, "name": "Tom Brown", "email": "tom.brown@school.com", "age": 13 }
```

### 6️⃣ Delete Tom

```http
DELETE /api/students/2 HTTP/1.1
```

```http
HTTP/1.1 204 No Content
```

(No body — nothing to say. 🤐)

### PUT vs. PATCH 🤔

| | PUT | PATCH |
|---|---|---|
| Sends | the **whole** resource | only the **changed** fields |
| Missing fields | become empty/default ⚠️ | stay the same ✅ |
| Example body | `{ "name": "Tom Brown", "email": "new@x.com", "age": 13 }` | `{ "email": "new@x.com" }` |
| Story | "Here's a **new** form, throw the old one away." 📄 | "Please **correct** this one line on the form." ✏️ |

> 💡 Many simple APIs only offer **PUT**. That's fine — just be clear about it in your documentation.

---

## 🔍 Part 6: Path parameters vs. query parameters

Remember the URL parts (Chapter 43)? Both are used in REST — for **different** jobs:

| | **Path** parameter | **Query** parameter |
|---|---|---|
| Looks like | `/api/students/42` | `/api/students?grade=5` |
| Used for | **identifying ONE** resource ("which one?") | **filtering, sorting, paging** a collection ("which ones? in what order?") |
| Required? | yes — it's part of the address | usually optional |
| 🌱 Spring Boot | `@PathVariable` (Chapter 58) | `@RequestParam` (Chapter 59) |

📖 **Story:** In a library 📚:
- "Give me book **number 42**" → path: `/books/42`
- "Show me books **by Dahl**, **sorted by title**" → query: `/books?author=Dahl&sort=title`

---

## 🔎 Part 7: Filtering, sorting and pagination

A school may have **10,000** students. Sending all of them in **one** response is slow and wasteful! 🐢 Clients usually want **some** of them, in **some** order, **one page** at a time.

### Filtering 🔎

```
GET /api/students?grade=5
GET /api/students?grade=5&city=Cairo
GET /api/books?author=Dahl&available=true
```

### Sorting 🔢

```
GET /api/students?sort=name            ← A → Z
GET /api/students?sort=age,desc        ← oldest first
```

### Pagination 📄

```
GET /api/students?page=0&size=20       ← the first 20 students
GET /api/students?page=1&size=20       ← the next 20
```

A paginated response often includes **information about the pages**:

```json
{
  "content": [
    { "id": 21, "name": "Ali" },
    { "id": 22, "name": "Ben" }
  ],
  "page": 1,
  "size": 20,
  "totalElements": 10000,
  "totalPages": 500
}
```

📖 **Story:** A **book** 📖 doesn't put 10,000 lines on one giant page. It has **pages**, and page numbers so you know where you are.

🌱 Spring Boot has **built-in** support for this: `Pageable` and `Page<Student>` (Chapter 78). It even reads `?page=1&size=20&sort=name` **automatically**! ✨

> 💡 Remember `skip` + `limit` in streams (Chapter 36)? That's the same idea: page 1 with size 20 = skip 20, limit 20.

---

## 🚨 Part 8: Good error responses

When something goes wrong, help the client understand **what** and **why**. A status code **plus** a clear JSON body.

### 👎 Bad

```http
HTTP/1.1 200 OK

Error!!!
```

(Status 200 for an error?! No details?! 😱)

### 👍 Good — the "Problem Details" standard

There's an internet standard for error bodies, called **Problem Details** (RFC 9457). It looks like this:

```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "The request has 2 invalid fields",
  "instance": "/api/students",
  "errors": {
    "email": "must be a well-formed email address",
    "age": "must be greater than or equal to 5"
  }
}
```

| Field | Meaning |
|---|---|
| `title` | a short summary |
| `status` | the HTTP status code again |
| `detail` | a human-friendly explanation |
| `instance` | which request had the problem |
| (extra fields) | you can add more, like `errors` for each wrong field |

🌱 **Spring Boot supports Problem Details** out of the box (a class called `ProblemDetail`). We'll use it in Chapter 66. 🎉

### Rules for error messages

- ✅ Say **what** is wrong and **how** to fix it: "email must be a well-formed email address".
- ✅ Use the **right** status code.
- ❌ **Never** show the stack trace or internal secrets to clients (hackers love those 🕵️). Log them on the server instead (Chapter 88).

---

## 🏷️ Part 9: Versioning

Your API will **change** over time. But old phone apps (that people haven't updated) still call the **old** way! 📱 If you change the API, they **break**. 💥

**Solution:** put a **version** in the URL:

```
 /api/v1/students      ← version 1 (old apps keep using this)
 /api/v2/students      ← version 2 (new apps use this)
```

| When do you need a new version? | Example |
|---|---|
| You **remove** or **rename** a field | `name` → `firstName` + `lastName` |
| You change the **meaning** of a field | `age` in months instead of years |
| You **don't** need a new version for... | **adding** a new optional field (old clients just ignore it 😊) |

> 💡 For learning projects, `/api/students` without a version is fine. For real apps that others use, start with `/api/v1/...`.

---

## 📝 Part 10: Design the Library API ✏️

Before coding, **design** your API on paper. Here's a complete design for a library. 📚 (You'll build something like this in the final project — Chapter 95!)

### Resources

- **Books** 📕
- **Members** 👤
- **Loans** 🔄 (a member borrows a book)

### Endpoints

| # | Method | URL | Meaning | Success |
|---|---|---|---|---|
| 1 | GET | `/api/v1/books` | list books (filter: `?author=`, `?available=true`; paging: `?page=&size=`) | 200 |
| 2 | GET | `/api/v1/books/{id}` | one book | 200 |
| 3 | POST | `/api/v1/books` | add a book | 201 |
| 4 | PUT | `/api/v1/books/{id}` | replace a book's data | 200 |
| 5 | DELETE | `/api/v1/books/{id}` | remove a book | 204 |
| 6 | GET | `/api/v1/members` | list members | 200 |
| 7 | GET | `/api/v1/members/{id}` | one member | 200 |
| 8 | POST | `/api/v1/members` | register a member | 201 |
| 9 | GET | `/api/v1/members/{id}/loans` | a member's loans | 200 |
| 10 | POST | `/api/v1/loans` | borrow a book (body: `bookId`, `memberId`) | 201 |
| 11 | POST | `/api/v1/loans/{id}/return` | return a book | 200 |
| 12 | GET | `/api/v1/loans?late=true` | all late loans | 200 |

### Errors

| Situation | Status |
|---|---|
| Borrow a book that is already borrowed | 409 Conflict |
| Borrow with an unknown `bookId` | 404 Not Found |
| Missing `memberId` in the body | 400 Bad Request |

> 💡 Look at #11: `POST /loans/{id}/return`. "Return" is an **action**, not a thing. Sometimes an action doesn't fit perfectly into CRUD. It's OK to use a **POST** with an action word at the end in these special cases. REST is a **style**, not a prison. 😊

### A body example

`POST /api/v1/loans`

```json
{ "bookId": 7, "memberId": 3 }
```

Response `201 Created`:

```json
{
  "id": 55,
  "book": { "id": 7, "title": "Matilda" },
  "member": { "id": 3, "name": "Sara" },
  "borrowedOn": "2025-03-01",
  "dueOn": "2025-03-15",
  "returnedOn": null
}
```

👀 Notice: dates in **ISO format** (Chapter 39), nested objects, `null` for "not returned yet". Everything you've learned comes together! 🎉

---

## ✋ Try it yourself

**Task 1:** Fix these bad URLs (write the method + the good URL):
1. `GET /getAllCourses`
2. `POST /course/new`
3. `GET /showCourse?courseId=8`
4. `POST /removeCourse/8`
5. `GET /Courses/8/Students`

<details>
<summary>Click to see the answers</summary>

1. `GET /api/courses`
2. `POST /api/courses`
3. `GET /api/courses/8`
4. `DELETE /api/courses/8`
5. `GET /api/courses/8/students` (small letters)

</details>

**Task 2:** For a **to-do list** app, design the 5 standard endpoints (list, get one, create, update, delete) with methods, URLs and success status codes.

<details>
<summary>Click to see the answer</summary>

| Action | Method | URL | Status |
|---|---|---|---|
| list | GET | `/api/todos` | 200 |
| get one | GET | `/api/todos/{id}` | 200 |
| create | POST | `/api/todos` | 201 |
| update | PUT (or PATCH) | `/api/todos/{id}` | 200 |
| delete | DELETE | `/api/todos/{id}` | 204 |

</details>

**Task 3:** Path or query parameter?
1. The product with id 15
2. Only products cheaper than 20
3. Page 3 of the results
4. The reviews of product 15
5. Sort by price

<details>
<summary>Click to see the answers</summary>

1. path: `/products/15`
2. query: `/products?maxPrice=20`
3. query: `?page=3`
4. path (nested): `/products/15/reviews`
5. query: `?sort=price`

</details>

**Task 4:** Write the JSON body for `POST /api/todos` to create a to-do "Buy milk", due on March 20, 2025, with priority `HIGH`. Then write the response the server should send (status line, `Location` header and body).

**Task 5:** Design an API for a **movie cinema** 🎬: movies, showtimes and ticket bookings. Write at least 8 endpoints in a table. Think about errors: what if the show is sold out?

---

## ⚠️ Common mistakes

### Mistake 1: Verbs in URLs

`/createUser`, `/getOrders` → use methods instead: `POST /users`, `GET /orders`.

### Mistake 2: Wrong status codes

Returning `200` for everything (even errors). Clients can't react correctly. Use 201, 204, 400, 404...

### Mistake 3: Using GET to change data

`GET /api/students/5/delete` 😱 — use `DELETE /api/students/5`.

### Mistake 4: Sending huge lists without paging

`GET /api/orders` returns 1,000,000 orders → the server and the client both struggle. 🐢 Add `?page=&size=`.

### Mistake 5: Showing internal details in errors

Stack traces, database errors, server paths in error responses → a **security** risk. Show a **clean** message; log the details on the server.

### Mistake 6: Changing the API and breaking old clients

Renaming a field without a new version → old apps crash. 💥 Use **versioning** for breaking changes.

---

## ✅ Summary

- An **API** is a **menu** 📋: it offers things to other programs and hides the details.
- A **REST** API uses HTTP the "normal" way:
  1. **Resources** with **URLs** (nouns, plural, small letters): `/api/students`, `/api/students/42`
  2. **Methods** for actions: GET, POST, PUT, PATCH, DELETE
  3. **Status codes** for results: 200, 201, 204, 400, 404, 409...
  4. **JSON** representations
  5. **Stateless**
- The **5 standard endpoints**: list, get one, create (201 + Location), update, delete (204).
- **Path** parameters identify **one** thing; **query** parameters **filter / sort / page**.
- Big lists → **pagination** (`?page=0&size=20`).
- Good errors: right status + clear JSON body (**Problem Details**), never stack traces.
- **Version** your API (`/api/v1/...`) when you make breaking changes.
- **Design first** ✏️, then build with Spring Boot ☕🌱.

---

## ❓ Quiz

1. What is an API? Use the restaurant story.
2. Why should URLs contain nouns, not verbs?
3. Write the method and URL to delete the book with id 5.
4. What status code and header should a successful POST return?
5. What's the difference between PUT and PATCH?
6. When do you use a path parameter, and when a query parameter?
7. What is pagination, and why is it useful?
8. What should an error response contain? What should it NOT contain?

<details>
<summary>Click to see the answers</summary>

1. A menu that a program offers to other programs: it lists what you can ask for and how, and hides how the "kitchen" works.
2. Because the HTTP method is already the verb. The URL should name the thing (resource).
3. `DELETE /api/books/5`
4. `201 Created` with a `Location` header pointing to the new resource.
5. PUT replaces the whole resource; PATCH changes only the fields you send.
6. Path: to identify one specific resource (`/students/42`). Query: to filter, sort or page a collection (`?grade=5&page=2`).
7. Sending a big list in small pages. It's faster and uses less memory and network.
8. It should contain the right status code and a clear message (what's wrong, how to fix it). It should NOT contain stack traces or internal secrets.

</details>

---

[⬅ Previous chapter](45-json.md) | [Table of Contents](../README.md) | [Next chapter: Testing APIs with Postman and curl ➡](47-postman-and-curl.md)
