# Chapter 78 – Pages and sorting

[⬅ Previous chapter](77-mysql-postgresql.md) | [Table of Contents](../README.md) | [Next chapter ➡](79-transactions.md)

---

## 🎯 Goal

Our school has 3 students. A real school might have **10,000**! 😱 Sending all of them in **one** answer is slow, wastes memory, and no screen can show them anyway. Real APIs send **one page at a time**. 📄📄📄

At the end of this chapter you will know:

- What **paging** is, and how it works in SQL (`OFFSET` and `FETCH`)
- How to get a **page** with **`Pageable`** and **`Page`** — almost no code! 🧞
- How clients ask for pages: `?page=0&size=2&sort=name,desc`
- How to set **defaults** with `@PageableDefault`
- How to get a **short, stable** JSON format for pages
- How to protect your API: a **maximum page size**, and **unknown sort fields** 🛡️

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Paging** / **pagination** | Splitting a long list into **pages**: "students 1–20", "students 21–40"... 📄 |
| **Page number** | **Which** page: Spring counts from **0**! (page 0 = the first page) |
| **Page size** | **How many** items on one page. |
| **`Pageable`** | Spring's object for "which page, how big, sorted how?" |
| **`Page<T>`** | Spring's object for "one page of results **plus** information: total count, total pages..." |
| **`Sort`** | Spring's object for "sorted by which field, up or down?" |
| **`OFFSET`** | SQL: "**skip** this many rows". |
| **`FETCH FIRST n ROWS ONLY`** | SQL: "give me only **n** rows" (some databases write `LIMIT n`). |

---

## 📖 Story: The phone book 📖

Imagine a phone book with 10,000 names. Nobody reads it in **one** go! You open **one page** with 20 names. At the bottom it says:

```
                     — Page 3 of 500 —
```

From that line you know:

- **Where** you are (page 3)
- **How many** pages there are (500)
- So you can go **back** (page 2) or **forward** (page 4). 👈👉

A paged API answer is the same: **some** students + a little line of information at the bottom. 📄

---

## 🔢 Part 1: Paging in SQL

How does a database give you "page 2, with 2 students per page"? With **`OFFSET`** (skip) and **`FETCH`** (take):

```sql
SELECT * FROM students ORDER BY id OFFSET 2 ROWS FETCH FIRST 2 ROWS ONLY;
```

```
 all students (sorted by id):   1 Sara   2 Tom   3 Lina   4 Omar   5 Mia
                                └─ skip 2 ─┘     └── take 2 ──┘
 page 0 (size 2):               1 Sara   2 Tom
 page 1 (size 2):                                3 Lina   4 Omar
 page 2 (size 2):                                                  5 Mia
```

The math: **`OFFSET = page × size`**. Page 1 with size 2 → skip **1 × 2 = 2** rows. 🧮

You **won't** write this SQL yourself — Spring Data does it. But now you know what happens inside! 🧠

---

## 🧞 Part 2: Paging with `Pageable` — almost no code

Remember the table in Chapter 72? `JpaRepository` already has **`findAll(Pageable pageable)`**. So the repository needs **nothing new**! 🎉

**`StudentService`** — one new method:

```java
public Page<StudentResponse> getPage(Pageable pageable) {
    return studentRepository.findAll(pageable)
            .map(StudentResponse::from);
}
```

(Imports: `org.springframework.data.domain.Page`, `org.springframework.data.domain.Pageable`.)

| Code | Meaning |
|---|---|
| `Pageable pageable` | ⭐ "Which page, how many, sorted how" — comes from the controller. |
| `studentRepository.findAll(pageable)` | ⭐ Spring Data writes the SQL with `OFFSET`, `FETCH` and `ORDER BY` — **and** a second query to **count** all students. Returns a `Page<Student>`. |
| `.map(StudentResponse::from)` | A `Page` has its own `map`: turn each entity into a DTO, **keep** the page information. (Like `map` on streams — Chapter 36.) |

**`StudentController`** — one new endpoint:

```java
@GetMapping("/page")
public Page<StudentResponse> getPage(@PageableDefault(size = 5, sort = "id") Pageable pageable) {
    return studentService.getPage(pageable);
}
```

(Imports: `org.springframework.data.domain.Page`, `org.springframework.data.domain.Pageable`, `org.springframework.data.web.PageableDefault`.)

| Code | Meaning |
|---|---|
| `Pageable pageable` | ⭐ Spring **builds** it automatically from the request parameters `page`, `size` and `sort`! 🪄 |
| `@PageableDefault(size = 5, sort = "id")` | The **defaults** if the client doesn't say: 5 per page, sorted by `id`. |
| `"/page"` | Our paged endpoint: `GET /api/students/page`. (A fixed word — it wins over `/{id}`, Chapter 58!) |

---

## 📄 Part 3: A short, stable JSON format

Let's try it! But first, one setting. If you return a `Page` **as it is**, Spring Data writes a long, messy JSON — and even **warns** you in the log:

```
Serializing PageImpl instances as-is is not supported, meaning that there is no guarantee about the stability of the resulting JSON structure!
	For a stable JSON structure, please use Spring Data's PagedModel (globally via @EnableSpringDataWebSupport(pageSerializationMode = VIA_DTO))
```

"The format may **change** in the future — use the **stable** format!" Spring Boot has a setting for exactly that. Add to **`application.properties`**:

```properties
# Paging: a short, stable JSON format for pages
spring.data.web.pageable.serialization-mode=via-dto
```

Now restart and try **`GET /api/students/page?page=0&size=2`** — the real answer:

```json
{"content":[{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12,"classroom":"5A"},{"id":2,"name":"Tom Brown","email":"tom@school.com","age":13,"classroom":"6B"}],"page":{"size":2,"number":0,"totalElements":3,"totalPages":2}}
```

Pretty-printed:

```json
{
  "content": [
    { "id": 1, "name": "Sara Ahmed", "email": "sara@school.com", "age": 12, "classroom": "5A" },
    { "id": 2, "name": "Tom Brown",  "email": "tom@school.com",  "age": 13, "classroom": "6B" }
  ],
  "page": {
    "size": 2,
    "number": 0,
    "totalElements": 3,
    "totalPages": 2
  }
}
```

| Field | Meaning |
|---|---|
| `content` | ⭐ The students on **this** page. |
| `page.size` | How many per page (2). |
| `page.number` | **Which** page (0 = the first). |
| `page.totalElements` | How many students **in total** (3). |
| `page.totalPages` | How many pages there are (2). |

That's the "— Page 1 of 2 —" line from the phone book! 📖 A website can now show buttons like **« 1 2 »**.

(Without the setting, we got the same students plus about 15 extra fields like `pageable`, `first`, `last`, `numberOfElements`, `sort`... — and the warning.)

---

## 🎛️ Part 4: Ask for pages, sizes and sorting

Spring reads three request parameters (Chapter 59):

| Parameter | Meaning | Example |
|---|---|---|
| `page` | Which page (from **0**) | `page=1` |
| `size` | How many per page | `size=2` |
| `sort` | Field and direction | `sort=name` or `sort=name,desc` |

Real answers:

**`GET /api/students/page`** (defaults: page 0, size 5, sort by id)

```json
{"content":[{"id":1,"name":"Sara Ahmed",...},{"id":2,"name":"Tom Brown",...},{"id":3,"name":"Lina Haddad",...}],"page":{"size":5,"number":0,"totalElements":3,"totalPages":1}}
```

**`GET /api/students/page?page=1&size=2`** (the second page)

```json
{"content":[{"id":3,"name":"Lina Haddad","email":"lina@school.com","age":11,"classroom":"5A"}],"page":{"size":2,"number":1,"totalElements":3,"totalPages":2}}
```

Only Lina — the last page can be **shorter**. ✅

**`GET /api/students/page?size=2&sort=name,desc`** (names Z → A)

```json
{"content":[{"id":2,"name":"Tom Brown",...},{"id":1,"name":"Sara Ahmed",...}],"page":{"size":2,"number":0,"totalElements":3,"totalPages":2}}
```

**`GET /api/students/page?size=2&sort=age`** (youngest first)

```json
{"content":[{"id":3,"name":"Lina Haddad",...,"age":11,...},{"id":1,"name":"Sara Ahmed",...,"age":12,...}],"page":{"size":2,"number":0,"totalElements":3,"totalPages":2}}
```

**`GET /api/students/page?page=5&size=2`** (a page that doesn't exist)

```json
{"content":[],"page":{"size":2,"number":5,"totalElements":3,"totalPages":2}}
```

An **empty** page — not an error. (Like an empty search result — Chapter 59.) The client sees `totalPages: 2` and knows there's nothing more.

> 💡 **Sort by two fields:** `?sort=age,desc&sort=name` → oldest first, and for the same age, by name.

### 👀 The SQL

With `show-sql`, you see **two** queries for every page (real, shortened):

```sql
select s1_0.id, s1_0.age, ... from students s1_0
order by s1_0.age
offset ? rows
fetch first ? rows only

select count(s1_0.id) from students s1_0
```

1️⃣ The **page** itself (`OFFSET` + `FETCH`, just like Part 1), and 2️⃣ a **count** for `totalElements` and `totalPages`. 🧮

---

## 🛡️ Part 5: Protect your API

### A maximum page size

What if a client asks for `?size=1000000`? 😱 Your server would try to load a million students! By default, Spring Data allows up to **2000** per page. You can set your own limit:

```properties
spring.data.web.pageable.max-page-size=50
```

We tested it with a limit of **2**: `?size=500` gave `"size":2` — Spring simply **uses the maximum** instead. 🛡️ (And a negative page like `?page=-1` is treated as page **0**.)

### Unknown sort fields

What if a client sends `?sort=banana`? 🍌 We tried it: **500**, and the log said:

```
PropertyReferenceException: No property 'banana' found for type 'Student'
```

That's the client's mistake — it should be **400**, not 500! Let's add a handler to our **`GlobalExceptionHandler`** (Chapter 66):

```java
@ExceptionHandler(PropertyReferenceException.class)
public ProblemDetail handleUnknownProperty(PropertyReferenceException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, ex.getMessage());
    problem.setTitle("Unknown field");
    return problem;
}
```

(Import: `org.springframework.data.core.PropertyReferenceException`.)

Now `GET /api/students/page?sort=banana` → (real answer):

```json
{"detail":"No property 'banana' found for type 'Student'","instance":"/api/students/page","status":400,"title":"Unknown field"}
```

✅ A clear **400**. 🍌❌

> ⚠️ Clients can sort by **any** field of the entity this way — even `teacherNote`! That doesn't **show** the note, but it could leak a little information through the **order**. 🕵️ In very careful APIs, you check the allowed sort fields yourself. For our school, it's fine.

---

## 🧭 Part 6: Sorting without paging

Sometimes you want **all** rows, just **sorted**. `JpaRepository` has **`findAll(Sort sort)`** — you used it in Chapter 76:

```java
courseRepository.findAll(Sort.by("title"))
```

More examples:

| Code | Meaning |
|---|---|
| `Sort.by("name")` | By name, A → Z |
| `Sort.by(Sort.Direction.DESC, "age")` | By age, oldest first |
| `Sort.by("age").descending().and(Sort.by("name"))` | By age (desc), then by name |

And a `Pageable` can be made **in code** too, without a request:

```java
Pageable firstTen = PageRequest.of(0, 10, Sort.by("name"));
Page<Student> page = studentRepository.findAll(firstTen);
```

(Import `org.springframework.data.domain.PageRequest`.)

Query methods (Chapter 74) can take a `Pageable` too:

```java
Page<Student> findByAgeGreaterThanEqual(int age, Pageable pageable);
```

→ filtering **and** paging together! 🎯

---

## 💻 Mini project: Paged books 📚

1. Add **`GET /api/books/page`** to your Book API: default size **2**, sorted by **title**.
2. Test: `?page=1`, `?sort=year,desc`, `?sort=price` (a field that doesn't exist — what happens now?).

<details>
<summary>Click to see the answer</summary>

**`BookService`**:

```java
public Page<BookResponse> getPage(Pageable pageable) {
    return bookRepository.findAll(pageable)
            .map(BookResponse::from);
}
```

**`BookController`**:

```java
@GetMapping("/page")
public Page<BookResponse> getPage(@PageableDefault(size = 2, sort = "title") Pageable pageable) {
    return bookService.getPage(pageable);
}
```

With the 3 starting books (in 2026):

- `GET /api/books/page` → Charlotte's Web and Matilda (A → Z), `"page":{"size":2,"number":0,"totalElements":3,"totalPages":2}`
- `GET /api/books/page?page=1` → The Hobbit
- `GET /api/books/page?sort=year,desc` → Matilda (1988), Charlotte's Web (1952)
- `GET /api/books/page?sort=price` → **400** `No property 'price' found for type 'Book'` — our global handler works for books too! 🎉

Note: `sort=year` uses the **field** name `year` (the column is `published` — Spring Data knows). 😎

</details>

---

## ✋ Try it yourself

**Task 1:** You have 47 students and a page size of 10. How many pages are there? What's on the last page? What's the `OFFSET` for page 3?

<details>
<summary>Click to see the answer</summary>

**5** pages (10+10+10+10+7). The last page (page **4**, counting from 0) has **7** students. `OFFSET` for page 3 = 3 × 10 = **30**.

</details>

**Task 2:** Write the URL for "the second page, 20 per page, sorted by age (oldest first)".

<details>
<summary>Click to see the answer</summary>

`/api/students/page?page=1&size=20&sort=age,desc` (page **1** is the second page!)

</details>

**Task 3:** Add an endpoint `GET /api/students/page/older?minAge=12` that pages **only** students aged 12 or older. (Tip: a query method with a `Pageable`.)

<details>
<summary>Click to see the answer</summary>

Repository:

```java
Page<Student> findByAgeGreaterThanEqual(int age, Pageable pageable);
```

Service:

```java
public Page<StudentResponse> getOlderPage(int minAge, Pageable pageable) {
    return studentRepository.findByAgeGreaterThanEqual(minAge, pageable)
            .map(StudentResponse::from);
}
```

Controller:

```java
@GetMapping("/page/older")
public Page<StudentResponse> getOlderPage(@RequestParam int minAge,
                                          @PageableDefault(size = 5, sort = "id") Pageable pageable) {
    return studentService.getOlderPage(minAge, pageable);
}
```

(Having both `findByAgeGreaterThanEqual(int)` from Chapter 74 and this one is fine — Java allows methods with the same name and different parameters: **overloading**.)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Counting pages from 1

`?page=1` is the **second** page! Spring counts from **0**. 😅 (Some APIs start at 1 — read the documentation of each API.)

### Mistake 2: Returning a `Page` without `via-dto`

You get a huge, unstable JSON and a warning in the log. **Fix:** `spring.data.web.pageable.serialization-mode=via-dto`.

### Mistake 3: Paging without sorting

Without `ORDER BY`, the database may return rows in **any** order — the same student can appear on **two** pages, and another one on **none**! 😱 **Fix:** Always sort (`@PageableDefault(sort = "id")`).

### Mistake 4: No maximum page size

`?size=1000000` → your server loads a million rows. 💥 **Fix:** `spring.data.web.pageable.max-page-size`.

### Mistake 5: Unknown sort field → 500

**Fix:** Handle `PropertyReferenceException` → **400** (Part 5).

### Mistake 6: Paging in Java instead of in the database

```java
studentRepository.findAll().stream().skip(20).limit(10)   // ❌ loads ALL students first!
```

**Fix:** `findAll(pageable)` — the **database** skips and limits. ⚡

---

## ✅ Summary

- **Paging** = one page at a time 📄. In SQL: **`OFFSET`** (skip `page × size`) + **`FETCH FIRST n ROWS ONLY`** + a **count** query.
- `JpaRepository` has **`findAll(Pageable)`** → a **`Page<T>`**; `.map(StudentResponse::from)` turns it into DTOs.
- In a controller, a **`Pageable`** parameter is filled from **`?page=0&size=2&sort=name,desc`** 🪄; **`@PageableDefault(size = 5, sort = "id")`** sets defaults.
- **`spring.data.web.pageable.serialization-mode=via-dto`** → a short, stable JSON: **`content`** + **`page`** (`size`, `number`, `totalElements`, `totalPages`).
- Pages count from **0**; a page that doesn't exist is **empty** (not an error).
- Protect your API: **`max-page-size`**, and turn **`PropertyReferenceException`** (unknown sort field) into **400**. 🛡️
- `findAll(Sort.by(...))` sorts without paging; `PageRequest.of(page, size, sort)` makes a `Pageable` in code; query methods can take a `Pageable`.

---

## ❓ Quiz

1. Why do APIs use paging?
2. What does `?page=2&size=10` return? (Which students, by position?)
3. Which two SQL parts does paging use?
4. What's the difference between `Pageable` and `Page`?
5. What do `totalElements` and `totalPages` mean?
6. What happens if a client asks for a page that doesn't exist?
7. Why should paged results always be sorted?
8. How do you stop clients from asking for a million items per page?

<details>
<summary>Click to see the answers</summary>

1. Sending thousands of items at once is slow and wasteful; clients show only a few at a time.
2. The third page: students number 21 to 30 (skip 20, take 10).
3. `OFFSET` (skip rows) and `FETCH FIRST n ROWS ONLY` (or `LIMIT n`).
4. `Pageable` is the **question** (which page, size, sort). `Page` is the **answer** (the items plus page information).
5. `totalElements`: how many items exist in total. `totalPages`: how many pages there are with this page size.
6. An empty `content` list — not an error.
7. Without a fixed order, rows can move between pages: duplicates or missing items.
8. Set `spring.data.web.pageable.max-page-size` (Spring then uses the maximum).

</details>

---

[⬅ Previous chapter](77-mysql-postgresql.md) | [Table of Contents](../README.md) | [Next chapter: Transactions: all or nothing ➡](79-transactions.md)
