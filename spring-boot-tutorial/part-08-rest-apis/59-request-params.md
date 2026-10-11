# Chapter 59 – Request parameters: `?name=Ali`

[⬅ Previous chapter](58-path-variables.md) | [Table of Contents](../README.md) | [Next chapter ➡](60-post-request-body.md)

---

## 🎯 Goal

Path variables say **which one** (`/students/5`). But what about questions like: "Show me the students **older than 12**, **sorted by name**"? 🤔 For that, we use **request parameters** (also called **query parameters**).

At the end of this chapter you will know:

- What **request parameters** are: the part after the **`?`** in a URL
- How to read them with **`@RequestParam`**
- How to make them **optional** (`required = false`) and give **default values** (`defaultValue`)
- How to **filter** and **sort** a list with them 🔍↕️
- How to read **several values** for one parameter (`?ids=1,3`)
- What happens when a required parameter is **missing**
- When to use a **path variable** and when to use a **request parameter**

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Query string** | The part of a URL after the `?`: `?minAge=12&sort=name`. (Chapter 43) |
| **Request parameter** / **query parameter** | One `name=value` pair in the query string: `minAge=12`. |
| **`@RequestParam`** | A label: "Put the value of this request parameter **into this parameter**." |
| **Required** | **Must** be there. If it's missing → 400. |
| **Optional** | **May** be missing. Then the value is `null` — or a **default value**. |
| **Default value** | The value to use when the parameter is **missing**. |
| **Filter** | Keep only the items that match a rule: "only students aged 12 or older". |

---

## 📖 Story: Ordering at the ice-cream shop 🍦

At the ice-cream shop, you say:

> "One ice cream, please — **flavor: chocolate**, **size: big**, **sprinkles: yes**!" 🍫🍦✨

- "**One ice cream**" = **what** you want (like the **path**: `/api/students`).
- "flavor: chocolate, size: big, sprinkles: yes" = **extra wishes** (like **request parameters**: `?flavor=chocolate&size=big&sprinkles=yes`).

Some wishes are **optional**: if you don't say the size, you get the **normal** size (a **default value**). Some are **required**: if you don't say the flavor, the seller asks "Which flavor?!" (a **400 Bad Request** 😄).

---

## 🔍 Part 1: The query string, taken apart

```
http://localhost:8080/api/students?minAge=12&sort=name
└────────── path ──────────────┘ └──── query string ────┘
                                  ↑      ↑   ↑     ↑
                                  ?  name=value & name=value
```

| Symbol | Meaning |
|---|---|
| `?` | "The query string **starts** here." (Only once!) |
| `minAge=12` | One parameter: name `minAge`, value `12`. |
| `&` | "And another parameter." |
| `sort=name` | Another parameter. |

The **order** of parameters doesn't matter: `?minAge=12&sort=name` = `?sort=name&minAge=12`. 👍

---

## 💻 Part 2: Your first `@RequestParam`

Let's start with a tiny example. Add this to `StudentController`:

```java
@GetMapping("/hello")
public String hello(@RequestParam String name) {
    return "Hello, " + name + "!";
}
```

(Import: `org.springframework.web.bind.annotation.RequestParam`.)

Restart → `http://localhost:8080/api/students/hello?name=Ali`:

```
Hello, Ali!
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@GetMapping("/hello")` | `GET /api/students/hello` (the query string is **not** part of the path!) |
| `@RequestParam String name` | ⭐ "Find the parameter **`name`** in the query string, and put its value here." |
| `"Hello, " + name + "!"` | Use it. |

Like `@PathVariable`, the **parameter name** (`name`) must match the name in the URL (`?name=...`). You can also write `@RequestParam("name") String who`.

### ❌ What if it's missing?

`http://localhost:8080/api/students/hello` (no `?name=...`):

```json
{"timestamp":"2026-10-11T04:20:47.531Z","status":400,"error":"Bad Request","path":"/api/students/hello"}
```

**400 Bad Request.** By default, a `@RequestParam` is **required**. The console explains:

```
... WARN ... Resolved [org.springframework.web.bind.MissingServletRequestParameterException: Required request parameter 'name' for method parameter type String is not present]
```

"Required request parameter `name` ... is not present." — the ice-cream seller asking "Which flavor?!" 🍦😄

> 💡 That was just a warm-up. You can delete `hello` now. Let's do the **real** thing: filtering students!

---

## 🔍 Part 3: Filtering students — optional parameters

Our goal:

| Request | Answer |
|---|---|
| `GET /api/students` | **all** students (like before) |
| `GET /api/students?minAge=12` | only students aged **12 or older** |
| `GET /api/students?name=a` | only students whose name **contains** "a" |
| `GET /api/students?minAge=12&name=a` | **both** rules |

The parameters must be **optional** — without them, the endpoint should work like before. Use **`required = false`**:

```java
@GetMapping
public List<Student> getAll(@RequestParam(required = false) Integer minAge,
                            @RequestParam(required = false) String name) {
    Stream<Student> result = students.stream();

    if (minAge != null) {
        result = result.filter(student -> student.age() >= minAge);
    }
    if (name != null) {
        result = result.filter(student -> student.name().toLowerCase().contains(name.toLowerCase()));
    }
    return result.toList();
}
```

(This **replaces** the old `getAll()` from Chapter 57. Import: `java.util.stream.Stream`.)

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@RequestParam(required = false) Integer minAge` | ⭐ An **optional** parameter. If the URL has no `minAge`, the value is **`null`**. |
| `Integer` (not `int`) | Because it must be able to be `null`! An `int` can't be `null` (the same reason as `Long id` — Chapter 57). |
| `Stream<Student> result = students.stream();` | Start with **all** students, as a stream. 🌊 |
| `if (minAge != null)` | Only filter if the client **sent** `minAge`. |
| `result = result.filter(...)` | Add a filter to the stream, and keep the new stream in `result`. (Streams are **lazy** — nothing really runs until `toList()`. Chapter 36.) |
| `student.age() >= minAge` | Keep students aged `minAge` or older. |
| `student.name().toLowerCase().contains(name.toLowerCase())` | Does the name contain the text? Both sides in **small letters**, so `?name=SARA` also finds "Sara Ahmed". (Chapter 9) |
| `return result.toList();` | Run the stream and collect the results. |

### ✅ Test it

Real answers:

`GET /api/students?minAge=12`

```json
[{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12},{"id":2,"name":"Tom Brown","email":"tom@school.com","age":13}]
```

Lina (11) is gone. ✅

`GET /api/students?name=a`

```json
[{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12},{"id":3,"name":"Lina Haddad","email":"lina@school.com","age":11}]
```

"Tom Brown" has no "a" — gone. ✅

`GET /api/students` (no parameters) → all 3 students, like before. ✅

### 🍌 A wrong value

`GET /api/students?minAge=old` → **400 Bad Request**. Spring can't turn `"old"` into an `Integer` — just like `/api/students/abc` in Chapter 58. 🍌

---

## ↕️ Part 4: Sorting — a default value

Now let's add **sorting**: `?sort=name` or `?sort=age`. If the client doesn't say anything, sort by **id**. That's a job for **`defaultValue`**:

```java
@GetMapping
public List<Student> getAll(@RequestParam(required = false) Integer minAge,
                            @RequestParam(required = false) String name,
                            @RequestParam(defaultValue = "id") String sort) {
    Stream<Student> result = students.stream();

    if (minAge != null) {
        result = result.filter(student -> student.age() >= minAge);
    }
    if (name != null) {
        result = result.filter(student -> student.name().toLowerCase().contains(name.toLowerCase()));
    }

    Comparator<Student> order = switch (sort) {
        case "name" -> Comparator.comparing(Student::name);
        case "age" -> Comparator.comparingInt(Student::age);
        default -> Comparator.comparing(Student::id);
    };
    return result.sorted(order).toList();
}
```

(Import: `java.util.Comparator`.)

### 🔍 The new lines

| Code | Meaning |
|---|---|
| `@RequestParam(defaultValue = "id") String sort` | ⭐ If `sort` is missing, use `"id"`. A parameter with a default value is **automatically optional**. |
| `Comparator<Student> order` | A **comparator** = a rule for **ordering** things (Chapter 36). |
| `switch (sort) { ... }` | Choose the rule based on the text (the arrow `switch` — Chapter 11). |
| `Comparator.comparing(Student::name)` | Order by name: A → Z. |
| `Comparator.comparingInt(Student::age)` | Order by age: youngest first. (`comparingInt` because `age` is an `int`.) |
| `default -> Comparator.comparing(Student::id)` | Anything else (including `"id"`) → order by id. |
| `result.sorted(order)` | Sort the stream with the chosen rule. |

### ✅ Test it

`GET /api/students?sort=age`

```json
[{"id":3,"name":"Lina Haddad","email":"lina@school.com","age":11},{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12},{"id":2,"name":"Tom Brown","email":"tom@school.com","age":13}]
```

Youngest first: Lina (11), Sara (12), Tom (13). ✅

`GET /api/students?name=a&sort=name`

```json
[{"id":3,"name":"Lina Haddad","email":"lina@school.com","age":11},{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12}]
```

Filter **and** sort together: names with "a", in A → Z order: **L**ina before **S**ara. ✅

`GET /api/students?minAge=12&sort=age` → Sara (12), Tom (13). ✅

### 📋 The three kinds of `@RequestParam`

| Code | Missing in URL → | Use for |
|---|---|---|
| `@RequestParam String name` | ❌ **400** | Things the endpoint **can't** work without |
| `@RequestParam(required = false) Integer minAge` | `null` | Optional filters |
| `@RequestParam(defaultValue = "id") String sort` | `"id"` | Optional settings with a **normal** choice |

> ⚠️ `defaultValue` is always written as **text** (`"10"`, `"true"`, `"id"`), even for numbers. Spring converts it, like a value from the URL.

---

## 🔎 Part 5: A search endpoint with a required parameter

Sometimes the parameter is **required**. Let's search a student by **email**:

```java
@GetMapping("/search")
public Student findByEmail(@RequestParam String email) {
    return students.stream()
            .filter(student -> student.email().equalsIgnoreCase(email))
            .findFirst()
            .orElseThrow(() -> new ResponseStatusException(
                    HttpStatus.NOT_FOUND, "No student with email " + email));
}
```

| Request | Answer |
|---|---|
| `GET /api/students/search?email=TOM@school.com` | Tom ✅ (`equalsIgnoreCase` ignores big/small letters) |
| `GET /api/students/search?email=x@y.z` | **404** (no such student) |
| `GET /api/students/search` | **400** (the required `email` is missing) |

Real answer for the first one:

```json
{"id":2,"name":"Tom Brown","email":"tom@school.com","age":13}
```

> 🥊 **Remember Chapter 58?** `/search` is a fixed word, so it wins over `/{id}`. ✅

---

## 🔢🔢 Part 6: Several values for one parameter

What if the client wants students **1 and 3**? Use a **`List`**:

```java
@GetMapping("/by-ids")
public List<Student> findByIds(@RequestParam List<Long> ids) {
    return students.stream()
            .filter(student -> ids.contains(student.id()))
            .toList();
}
```

The client can send the values in **two** ways — both work (we tested them):

| Request | Answer |
|---|---|
| `GET /api/students/by-ids?ids=1,3` | Sara and Lina |
| `GET /api/students/by-ids?ids=1&ids=2` | Sara and Tom |

| Code | Meaning |
|---|---|
| `@RequestParam List<Long> ids` | ⭐ Spring collects **all** values into a list — split at commas, or from repeated `ids=` parameters. |
| `ids.contains(student.id())` | Is this student's id in the wanted list? (`contains` uses `equals` — Chapter 30.) |

---

## 🤔 Part 7: Path variable or request parameter?

This is a question every API developer asks. Here's the simple rule from **Chapter 46**:

| Use a **path variable** when... | Use a **request parameter** when... |
|---|---|
| it says **which one** thing | it **filters**, **sorts**, **searches** or **pages** a list |
| without it, the URL means something else | the endpoint also works **without** it |
| `/api/students/5` | `/api/students?minAge=12` |
| `/api/books/2` | `/api/books?author=Dahl&sort=year` |

**A trick to remember:** 🧠 Think of a **folder** 📁 on your computer. The **path** is the folder where you are: `/students/5`. The **parameters** are like the **search box and the "sort by" button** of that folder. 🔍↕️

---

## ⌨️ Part 8: Testing parameters — the `&` trap!

In the **browser**, just type the URL. In **Postman**, use the **Params** tab — Postman builds the `?...&...` for you (Chapter 47). ✅

In **curl**, there's a trap you met in Chapter 47:

```
curl http://localhost:8080/api/students?minAge=12&sort=age     ❌
```

The terminal sees `&` as a **special command** ("run in the background") and **cuts** your URL at the `&`! 😱 Only `?minAge=12` reaches the server.

**Fix:** Put the URL in **quotes**:

```
curl "http://localhost:8080/api/students?minAge=12&sort=age"   ✅
```

---

## 💻 Mini project: The Book API, part 3 📚

Add these to your `BookController`:

1. `GET /api/books` gets optional parameters:
   - `author` → only books whose author **contains** the text (ignore big/small letters)
   - `before` → only books from **before** this year
   - `sort` → `title` or `year`; default: `id`
2. `GET /api/books/search?title=...` → the first book whose title **contains** the text, or **404**.

Then test:

- `/api/books?before=1960`
- `/api/books?sort=year`
- `/api/books?author=dahl`
- `/api/books/search?title=hob`

<details>
<summary>Click to see the answer</summary>

```java
@GetMapping
public List<Book> getAll(@RequestParam(required = false) String author,
                         @RequestParam(required = false) Integer before,
                         @RequestParam(defaultValue = "id") String sort) {
    Stream<Book> result = books.stream();

    if (author != null) {
        result = result.filter(book -> book.author().toLowerCase().contains(author.toLowerCase()));
    }
    if (before != null) {
        result = result.filter(book -> book.year() < before);
    }

    Comparator<Book> order = switch (sort) {
        case "title" -> Comparator.comparing(Book::title);
        case "year" -> Comparator.comparingInt(Book::year);
        default -> Comparator.comparing(Book::id);
    };
    return result.sorted(order).toList();
}

@GetMapping("/search")
public Book searchByTitle(@RequestParam String title) {
    return books.stream()
            .filter(book -> book.title().toLowerCase().contains(title.toLowerCase()))
            .findFirst()
            .orElseThrow(() -> new ResponseStatusException(
                    HttpStatus.NOT_FOUND, "No book with a title like " + title));
}
```

Answers:

- `/api/books?before=1960` → The Hobbit (1937) and Charlotte's Web (1952)
- `/api/books?sort=year` → The Hobbit (1937), Charlotte's Web (1952), Matilda (1988)
- `/api/books?author=dahl` → Matilda
- `/api/books/search?title=hob` → The Hobbit

</details>

---

## ✋ Try it yourself

**Task 1:** Add an optional parameter `maxAge` to `GET /api/students`. Then `?minAge=12&maxAge=12` should return only Sara.

<details>
<summary>Click to see the answer</summary>

Add the parameter:

```java
@RequestParam(required = false) Integer maxAge
```

and the filter:

```java
if (maxAge != null) {
    result = result.filter(student -> student.age() <= maxAge);
}
```

`?minAge=12&maxAge=12` → only Sara Ahmed (age 12). ✅

</details>

**Task 2:** Add a parameter `desc` (a `boolean`, default `false`). If it's `true`, reverse the order. Example: `?sort=age&desc=true` → oldest first.

<details>
<summary>Click to see the answer</summary>

```java
@RequestParam(defaultValue = "false") boolean desc
```

After the `switch`:

```java
if (desc) {
    order = order.reversed();
}
```

`?sort=age&desc=true` → Tom (13), Sara (12), Lina (11). (`reversed()` turns a comparator around.)

</details>

**Task 3:** What does each URL return? Guess first!

a) `/api/students?name=BROWN` b) `/api/students?minAge=20` c) `/api/students?sort=color` d) `/api/students?minAge=` (empty value)

<details>
<summary>Click to see the answer</summary>

a) Tom Brown (small/big letters are ignored).
b) An **empty list** `[]` — no student is 20 or older. That's **200 OK** with `[]`, **not** 404! An empty search result is still a correct answer. ✅
c) All students, sorted by **id** (`color` goes to `default`).
d) All students — an **empty** value for an optional `Integer` is treated as "not there" (`null`).

</details>

---

## ⚠️ Common mistakes

### Mistake 1: `int` for an optional parameter

```java
@RequestParam(required = false) int minAge     // ❌
```

When `minAge` is missing, Spring wants to put `null` into an `int`... impossible! We tested it: the request fails with **500**, and the console says:

```
Optional int parameter 'minAge' is present but cannot be translated into a null value due to being declared as a primitive type. Consider declaring it as object wrapper for the corresponding primitive type.
```

"Declare it as an **object wrapper**" = use `Integer`! Spring even tells you the fix. 😊 **Fix:** Use `Integer` (it can be `null`) — or give a `defaultValue`.

### Mistake 2: Forgetting the quotes in curl

`curl http://...?a=1&b=2` → the terminal cuts at `&`. **Fix:** `curl "http://...?a=1&b=2"`. 🧷

### Mistake 3: Two `?` in one URL

```
/api/students?minAge=12?sort=age     ❌
/api/students?minAge=12&sort=age     ✅
```

Only the **first** parameter starts with `?`. All others start with `&`.

### Mistake 4: Returning 404 for an empty search result

"Show me students older than 20" → nobody. That's **not** "not found" — the **list** exists, it's just empty. **Fix:** Return `200` with `[]`. Use **404** only when **one specific thing** (like student 99) doesn't exist.

### Mistake 5: Using parameters for "which one"

```
/api/students?id=5    😕 works, but not REST style
/api/students/5       ✅
```

**Fix:** One specific thing → **path variable** (Chapter 58). Filters → **parameters**.

---

## ✅ Summary

- **Request parameters** are the `name=value` pairs after the **`?`** in a URL, separated by **`&`**.
- **`@RequestParam String name`** reads one. The names must match (or use `@RequestParam("name")`).
- By default, a `@RequestParam` is **required** → missing = **400**.
- **`required = false`** → missing = `null` (use `Integer`, not `int`!).
- **`defaultValue = "id"`** → missing = the default (and it's automatically optional).
- Filtering: start with `students.stream()`, add a `.filter(...)` for **each** parameter that was sent, then `.toList()`.
- Sorting: choose a **`Comparator`** with a `switch`, then `.sorted(order)`.
- **`@RequestParam List<Long> ids`** accepts `?ids=1,3` and `?ids=1&ids=3`.
- **Path variable** = which one 📁. **Request parameter** = filter / sort / search 🔍.
- In curl, put URLs with **`&`** in **quotes**!

---

## ❓ Quiz

1. In `/api/books?author=Dahl&year=1988`, what are the parameter names and values?
2. What happens when a required `@RequestParam` is missing?
3. Why do we write `Integer minAge` and not `int minAge` for an optional parameter?
4. What's the difference between `required = false` and `defaultValue = "..."`?
5. `GET /api/students?minAge=50` finds nobody. What should the answer be: 404, or 200 with `[]`?
6. Path variable or request parameter? a) one student by id b) students sorted by name c) books by an author
7. Why does `curl http://localhost:8080/api/students?minAge=12&sort=age` not work as expected?
8. How can a client send several ids in one parameter?

<details>
<summary>Click to see the answers</summary>

1. `author` = `Dahl`, `year` = `1988`.
2. The answer is **400 Bad Request** ("Required request parameter ... is not present").
3. Because a missing optional parameter is `null`, and an `int` can't be `null`.
4. With `required = false`, a missing parameter becomes `null`. With `defaultValue`, it becomes the default value.
5. **200 OK** with an empty list `[]`. An empty result is still a correct answer.
6. a) path variable b) request parameter c) request parameter
7. The terminal treats `&` as a special symbol and cuts the URL. Put the URL in quotes.
8. With a `List` parameter: `?ids=1,3` or `?ids=1&ids=3`.

</details>

---

[⬅ Previous chapter](58-path-variables.md) | [Table of Contents](../README.md) | [Next chapter: Sending data: @PostMapping and @RequestBody ➡](60-post-request-body.md)
