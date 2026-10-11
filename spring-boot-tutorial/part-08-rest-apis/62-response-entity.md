# Chapter 62 – ResponseEntity and status codes

[⬅ Previous chapter](61-put-delete.md) | [Table of Contents](../README.md) | [Next chapter ➡](63-layers.md)

---

## 🎯 Goal

Our API works. But some answers aren't **perfect** yet: 🤏

- Creating a student says **200** — REST says **201 Created** (with a `Location` header).
- Deleting says **200** with an empty body — REST says **204 No Content**.

At the end of this chapter you will know:

- What **`ResponseEntity`** is: the **full control** over a response 🎛️ (status + headers + body)
- How to answer **201 Created** with a **`Location`** header
- How to answer **204 No Content**
- How to answer **404 Not Found** without throwing an exception
- How to add your **own headers**
- A shortcut for simple cases: **`@ResponseStatus`**
- When to use which way

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **`ResponseEntity`** | A Java object that is a **whole HTTP response**: status code + headers + body. 📦 |
| **Builder** | A style of code where you build something **step by step**, with dots: `.status(...).header(...).body(...)`. 🏗️ |
| **201 Created** | "I **created** something new for you." |
| **`Location` header** | "The new thing lives **here**": its URL. 🗺️ |
| **204 No Content** | "Done! And there's **nothing** to show." |
| **`@ResponseStatus`** | A label: "This method always answers with **this** status code." |
| **`URI`** | A Java class for an **address** like `/api/students/4`. |

---

## 📖 Story: Sending a parcel 📦

So far, your methods returned only the **gift** 🎁 (the body). Spring put it in a box, wrote the address and the stamp (status, headers) for you — always the **standard** ones.

With **`ResponseEntity`**, **you** pack the whole parcel yourself:

```
┌──────────────────────────────────────┐
│ 📮 STAMP:   201 Created              │  ← the status code
│ 🏷️ LABELS:  Location: /api/students/4│  ← the headers
│             X-Total-Count: 3         │
│ ┌──────────────────────────────────┐ │
│ │ 🎁 GIFT:  {"id":4, "name": ...}  │ │  ← the body
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘
          ResponseEntity 📦
```

You choose the **stamp**, the **labels**, and the **gift**. 🎛️

---

## 📦 Part 1: Your first `ResponseEntity`

Let's start with **get one student**. Change `getById` in `StudentController` (from Chapter 58) to:

```java
@GetMapping("/{id}")
public ResponseEntity<Student> getById(@PathVariable Long id) {
    Optional<Student> found = findStudent(id);
    if (found.isEmpty()) {
        return ResponseEntity.notFound().build();
    }
    return ResponseEntity.ok(found.get());
}

private Optional<Student> findStudent(Long id) {
    return students.stream()
            .filter(student -> student.id().equals(id))
            .findFirst();
}
```

Imports:

```java
import java.util.Optional;

import org.springframework.http.ResponseEntity;
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `ResponseEntity<Student>` | ⭐ The method returns a **whole response**, whose body is a `Student`. (The `<Student>` is **generics** — Chapter 34!) |
| `private Optional<Student> findStudent(Long id)` | A small **helper** method: find the student, as an `Optional` (Chapter 37). `private` = only for this class. |
| `if (found.isEmpty())` | Not found? |
| `ResponseEntity.notFound().build()` | ⭐ Build a response with status **404** and **no body**. |
| `ResponseEntity.ok(found.get())` | ⭐ Build a response with status **200** and the student as the body. |

### ✅ Test it

`GET /api/students/2`:

```
HTTP/1.1 200 
Content-Type: application/json

{"id":2,"name":"Tom Brown","email":"tom@school.com","age":13}
```

`GET /api/students/99`:

```
HTTP/1.1 404 
Content-Length: 0
```

✅ **404**, and this time with a completely **empty** body. No exception was needed — we just **built** a 404 response. 🏗️

### ⚠️ What about `ageIn`?

In Chapter 58, `ageIn` called `getById(id)` and got a `Student`. Now `getById` returns a `ResponseEntity`... 🤔 Use the helper instead:

```java
@GetMapping("/{id}/age-in/{years}")
public String ageIn(@PathVariable Long id, @PathVariable int years) {
    Student student = findStudent(id)
            .orElseThrow(() -> new ResponseStatusException(
                    HttpStatus.NOT_FOUND, "Student with id " + id + " was not found"));
    return "In " + years + " years, " + student.name() + " will be " + (student.age() + years) + ".";
}
```

(The same idea works for `update` (PATCH): use `findStudent(id)` instead of `getById(id)`. See the full controller in Part 7.)

### 🌊 A shorter way (if you like streams)

```java
@GetMapping("/{id}")
public ResponseEntity<Student> getById(@PathVariable Long id) {
    return findStudent(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
}
```

| Code | Meaning |
|---|---|
| `.map(ResponseEntity::ok)` | If there's a student, turn it into a **200** response. |
| `.orElse(ResponseEntity.notFound().build())` | If not, use a **404** response. |

Both versions do **exactly** the same (we tested both). Use the one you understand better! 😊

---

## 🆕 Part 2: 201 Created + `Location`

Remember the REST rule from Chapter 46? After **creating** something:

- status **201 Created** ✅
- a **`Location`** header with the URL of the new thing 🗺️
- the created thing in the body 🎁

Change `create`:

```java
@PostMapping
public ResponseEntity<Student> create(@RequestBody Student newStudent) {
    Student student = new Student(nextId, newStudent.name(), newStudent.email(), newStudent.age());
    nextId++;
    students.add(student);
    URI location = URI.create("/api/students/" + student.id());
    return ResponseEntity.created(location).body(student);
}
```

(Import: `java.net.URI`.)

| Code | Meaning |
|---|---|
| `URI location = URI.create("/api/students/" + student.id());` | Make the address of the new student: `/api/students/4`. |
| `ResponseEntity.created(location)` | ⭐ Status **201 Created** + the header **`Location: /api/students/4`**. |
| `.body(student)` | ⭐ ...and the new student as the body. |

### ✅ Test it

```bash
curl -i -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Omar Ali","email":"omar@school.com","age":12}'
```

Real answer:

```
HTTP/1.1 201 
Location: /api/students/4
Content-Type: application/json

{"id":4,"name":"Omar Ali","email":"omar@school.com","age":12}
```

🎉 **Perfect REST!** Exactly like the design in Chapter 46. The client can now go to `Location` to get the new student: `GET /api/students/4`. 🗺️

### 🌍 A full URL in `Location` (optional)

Some APIs put the **full** address in `Location` (with `http://localhost:8080`). Spring has a helper that knows the server's address:

```java
URI location = ServletUriComponentsBuilder.fromCurrentContextPath()
        .path("/api/students/{id}")
        .buildAndExpand(student.id())
        .toUri();
```

```
Location: http://localhost:8080/api/students/5
```

| Code | Meaning |
|---|---|
| `ServletUriComponentsBuilder.fromCurrentContextPath()` | Start with the server's address: `http://localhost:8080` (Spring reads it from the current request). |
| `.path("/api/students/{id}")` | Add a path with a placeholder. |
| `.buildAndExpand(student.id())` | Put the id into the placeholder. |
| `.toUri()` | Make a `URI`. |

Both styles are correct. The short `URI.create(...)` is fine for this book. 👍

---

## 🤐 Part 3: 204 No Content

After **deleting**, there's nothing to show. The perfect answer: **204 No Content**.

```java
@DeleteMapping("/{id}")
public ResponseEntity<Void> delete(@PathVariable Long id) {
    boolean removed = students.removeIf(student -> student.id().equals(id));
    if (!removed) {
        return ResponseEntity.notFound().build();
    }
    return ResponseEntity.noContent().build();
}
```

| Code | Meaning |
|---|---|
| `ResponseEntity<Void>` | ⭐ A response with **no body**. `Void` (capital V) is the "object version" of `void` — "nothing". |
| `ResponseEntity.notFound().build()` | 404, no body. |
| `ResponseEntity.noContent().build()` | ⭐ **204 No Content**, no body. |

Real answers:

```
DELETE /api/students/3   →   HTTP/1.1 204
DELETE /api/students/3   →   HTTP/1.1 404     (already gone)
```

✅

---

## 🏷️ Part 4: Your own headers

You can add **any** header. A popular one for lists: **`X-Total-Count`** — "how many items are in this list". (Headers starting with `X-` are **custom** headers, made up by developers.)

```java
@GetMapping
public ResponseEntity<List<Student>> getAll(@RequestParam(required = false) Integer minAge,
                                            @RequestParam(required = false) String name,
                                            @RequestParam(defaultValue = "id") String sort) {
    // ... the same filtering and sorting as in Chapter 59 ...
    List<Student> list = result.sorted(order).toList();
    return ResponseEntity.ok()
            .header("X-Total-Count", String.valueOf(list.size()))
            .body(list);
}
```

| Code | Meaning |
|---|---|
| `ResponseEntity<List<Student>>` | A response whose body is a **list** of students. (Generics inside generics! 🪆) |
| `ResponseEntity.ok()` | Start building a **200** response... |
| `.header("X-Total-Count", String.valueOf(list.size()))` | ...add a header. Header values are **text**, so we turn the number into a `String`. |
| `.body(list)` | ...and finish with the body. |

`GET /api/students?minAge=12` — real answer:

```
HTTP/1.1 200 
X-Total-Count: 2
Content-Type: application/json

[{"id":1,"name":"Sara Ahmed",...},{"id":2,"name":"Tom Brown",...}]
```

---

## 🧰 Part 5: The `ResponseEntity` toolbox

Here are the most useful builder methods. 🧰

| Code | Status | Body? |
|---|---|---|
| `ResponseEntity.ok(body)` | **200** OK | ✅ |
| `ResponseEntity.ok().header(...).body(body)` | **200** OK + headers | ✅ |
| `ResponseEntity.created(uri).body(body)` | **201** Created + `Location` | ✅ |
| `ResponseEntity.noContent().build()` | **204** No Content | ❌ |
| `ResponseEntity.badRequest().body(text)` | **400** Bad Request | ✅ |
| `ResponseEntity.notFound().build()` | **404** Not Found | ❌ |
| `ResponseEntity.status(HttpStatus.CONFLICT).body(...)` | **any** status you want | ✅ |

**Pattern:** `ResponseEntity.` + **status** + (optional `.header(...)`) + **`.body(...)`** or **`.build()`** (for no body).

### Two fun examples

**400 with a message:**

```java
@GetMapping("/check-age")
public ResponseEntity<String> checkAge(@RequestParam int age) {
    if (age < 5) {
        return ResponseEntity.badRequest().body("Students must be at least 5 years old.");
    }
    return ResponseEntity.ok("Age " + age + " is fine.");
}
```

| Request | Answer |
|---|---|
| `GET /api/students/check-age?age=3` | **400** `Students must be at least 5 years old.` |
| `GET /api/students/check-age?age=9` | **200** `Age 9 is fine.` |

**Any status — even a joke one! 🫖**

```java
@GetMapping("/teapot")
public ResponseEntity<String> teapot() {
    return ResponseEntity.status(HttpStatus.I_AM_A_TEAPOT).body("I'm a teapot. I can't make coffee! 🫖");
}
```

```
HTTP/1.1 418 
Content-Type: text/plain;charset=UTF-8

I'm a teapot. I can't make coffee! 🫖
```

**418 I'm a teapot** is a real status code — an old internet **joke** from 1998! 😄 (Don't use it in real APIs. But now you know you can choose **any** status.)

---

## 🏷️ Part 6: The shortcut — `@ResponseStatus`

If a method **always** answers with the **same** status, there's a shorter way: a label!

```java
@PostMapping
@ResponseStatus(HttpStatus.CREATED)
public Student create(@RequestBody Student newStudent) {
    Student student = new Student(nextId, newStudent.name(), newStudent.email(), newStudent.age());
    nextId++;
    students.add(student);
    return student;
}
```

| Code | Meaning |
|---|---|
| `@ResponseStatus(HttpStatus.CREATED)` | ⭐ "When this method finishes normally, answer **201** instead of 200." |
| `public Student create(...)` | A normal return type — no `ResponseEntity`! |

Real answer: `HTTP/1.1 201` with the student. ✅ But **no `Location` header** — a label can't add headers that change each time. 🤷

The same for DELETE:

```java
@DeleteMapping("/{id}")
@ResponseStatus(HttpStatus.NO_CONTENT)
public void delete(@PathVariable Long id) { ... }   // 204 when it works
```

### 🤔 `ResponseEntity` or `@ResponseStatus`?

| Situation | Best choice |
|---|---|
| Always the same status, no special headers | `@ResponseStatus` 🏷️ (short and clean) |
| The status **depends** on something (found / not found) | `ResponseEntity` 📦 |
| You need **headers** (`Location`, `X-Total-Count`...) | `ResponseEntity` 📦 |
| Just 200 with a body | Nothing! Return the object (Chapter 52). |

> 💡 In **Chapter 63–66**, we'll use **exceptions** for "not found" (thrown by the service), `@ResponseStatus` for DELETE, and `ResponseEntity` for POST (because of `Location`). That's a very common mix in real projects. 😊

---

## 📄 Part 7: The controller with perfect status codes

Here are all the methods that changed (the others stay as in Chapter 61):

```java
@GetMapping
public ResponseEntity<List<Student>> getAll(@RequestParam(required = false) Integer minAge,
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
    List<Student> list = result.sorted(order).toList();
    return ResponseEntity.ok()
            .header("X-Total-Count", String.valueOf(list.size()))
            .body(list);
}

@GetMapping("/{id}")
public ResponseEntity<Student> getById(@PathVariable Long id) {
    Optional<Student> found = findStudent(id);
    if (found.isEmpty()) {
        return ResponseEntity.notFound().build();
    }
    return ResponseEntity.ok(found.get());
}

@PostMapping
public ResponseEntity<Student> create(@RequestBody Student newStudent) {
    Student student = new Student(nextId, newStudent.name(), newStudent.email(), newStudent.age());
    nextId++;
    students.add(student);
    URI location = URI.create("/api/students/" + student.id());
    return ResponseEntity.created(location).body(student);
}

@PutMapping("/{id}")
public ResponseEntity<Student> replace(@PathVariable Long id, @RequestBody Student changed) {
    for (int i = 0; i < students.size(); i++) {
        if (students.get(i).id().equals(id)) {
            Student updated = new Student(id, changed.name(), changed.email(), changed.age());
            students.set(i, updated);
            return ResponseEntity.ok(updated);
        }
    }
    return ResponseEntity.notFound().build();
}

@PatchMapping("/{id}")
public ResponseEntity<Student> update(@PathVariable Long id, @RequestBody StudentPatch patch) {
    Optional<Student> found = findStudent(id);
    if (found.isEmpty()) {
        return ResponseEntity.notFound().build();
    }
    Student old = found.get();
    Student updated = new Student(
            id,
            patch.name() != null ? patch.name() : old.name(),
            patch.email() != null ? patch.email() : old.email(),
            patch.age() != null ? patch.age() : old.age());
    students.set(students.indexOf(old), updated);
    return ResponseEntity.ok(updated);
}

@DeleteMapping("/{id}")
public ResponseEntity<Void> delete(@PathVariable Long id) {
    boolean removed = students.removeIf(student -> student.id().equals(id));
    if (!removed) {
        return ResponseEntity.notFound().build();
    }
    return ResponseEntity.noContent().build();
}

private Optional<Student> findStudent(Long id) {
    return students.stream()
            .filter(student -> student.id().equals(id))
            .findFirst();
}
```

### 🏆 Our API now matches the Chapter 46 design

| Job | Request | Status ✅ |
|---|---|---|
| List all | `GET /api/students` | **200** + `X-Total-Count` |
| Get one | `GET /api/students/2` | **200** (or **404**) |
| Create | `POST /api/students` | **201** + `Location` |
| Replace | `PUT /api/students/2` | **200** (or **404**) |
| Change some | `PATCH /api/students/2` | **200** (or **404**) |
| Delete | `DELETE /api/students/2` | **204** (or **404**) |

🎉🎉🎉

---

## 💻 Mini project: The Book API, part 6 📚

Give your `BookController` perfect status codes:

1. `GET /api/books/{id}` → `ResponseEntity`: **200** or **404**.
2. `POST /api/books` → **201** + `Location: /api/books/{id}`.
3. `DELETE /api/books/{id}` → **204** or **404**.
4. Bonus: `GET /api/books` → add the header `X-Total-Count`.

(Remember: if other methods call `getById`, give them a `findBook` helper — like `findStudent`.)

<details>
<summary>Click to see the answer</summary>

```java
@GetMapping("/{id}")
public ResponseEntity<Book> getById(@PathVariable Long id) {
    return findBook(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
}

@PostMapping
public ResponseEntity<Book> create(@RequestBody Book newBook) {
    Book book = new Book(nextId, newBook.title(), newBook.author(), newBook.year());
    nextId++;
    books.add(book);
    return ResponseEntity.created(URI.create("/api/books/" + book.id())).body(book);
}

@DeleteMapping("/{id}")
public ResponseEntity<Void> delete(@PathVariable Long id) {
    boolean removed = books.removeIf(book -> book.id().equals(id));
    if (!removed) {
        return ResponseEntity.notFound().build();
    }
    return ResponseEntity.noContent().build();
}

private Optional<Book> findBook(Long id) {
    return books.stream()
            .filter(book -> book.id().equals(id))
            .findFirst();
}
```

Bonus, at the end of `getAll`:

```java
List<Book> list = result.sorted(order).toList();
return ResponseEntity.ok()
        .header("X-Total-Count", String.valueOf(list.size()))
        .body(list);
```

(and change its return type to `ResponseEntity<List<Book>>`). In `age(...)` and `update(...)`, use `findBook(id).orElseThrow(...)` instead of `getById(id)`.

Test:

- `POST /api/books` with The Gruffalo → **201**, `Location: /api/books/4`
- `DELETE /api/books/4` → **204**; again → **404**

</details>

---

## ✋ Try it yourself

**Task 1:** What does each line build? Write the status code (and the body, if any).

a) `ResponseEntity.ok("Hi")`
b) `ResponseEntity.noContent().build()`
c) `ResponseEntity.status(HttpStatus.CONFLICT).body("Email already used")`
d) `ResponseEntity.notFound().build()`

<details>
<summary>Click to see the answer</summary>

a) **200**, body `Hi` b) **204**, no body c) **409 Conflict**, body `Email already used` d) **404**, no body

</details>

**Task 2:** In `create`, refuse students under 5: answer **400** with the text `"Too young for school!"`. What's the problem with the return type?

<details>
<summary>Click to see the answer</summary>

The method returns `ResponseEntity<Student>`, but the error body is a `String` — the types don't match! 🤔 Possible fixes:

- Use `ResponseEntity.badRequest().build()` (no body), **or**
- throw `new ResponseStatusException(HttpStatus.BAD_REQUEST, "Too young for school!")`, **or**
- change the return type to `ResponseEntity<?>` (the `?` means "any type" — use it rarely!).

The **best** solution comes in Chapter 65 (validation) and Chapter 66 (error handling). 😉

</details>

**Task 3:** Add `@ResponseStatus(HttpStatus.CREATED)` to the `check` method from Chapter 60 (Task 4). What status do you get? Does that make sense?

<details>
<summary>Click to see the answer</summary>

You get **201**... but `check` doesn't create anything! That's a **lie** 🤥 — it should stay **200**. Use 201 **only** when something new was created.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: 200 for everything

Many beginner APIs answer **200** for everything — even errors, with `{"error": "not found"}` in the body. 😱 Clients then have to **read** every body to find out if it worked. **Fix:** Use the **right** status codes. They're the first thing a client checks. 🚦

### Mistake 2: Forgetting `.build()` or `.body(...)`

```java
return ResponseEntity.notFound();   // ❌ compile error
```

`notFound()` only **starts** the building. 🏗️ **Fix:** finish with `.build()` (no body) or `.body(...)`.

### Mistake 3: A body with 204

204 means "**no** content". Don't try to send a body with it. Clients will ignore it — or get confused. **Fix:** 204 → `.build()`.

### Mistake 4: Header values that aren't text

```java
.header("X-Total-Count", list.size())   // ❌ an int
```

Header values are **text**. **Fix:** `String.valueOf(list.size())`.

### Mistake 5: `@ResponseStatus(HttpStatus.CREATED)` but no `Location`

It's not **wrong**, but it's **incomplete** REST. If clients need to know where the new thing is, use `ResponseEntity.created(location)`.

---

## ✅ Summary

- **`ResponseEntity<T>`** = a whole response 📦: **status** + **headers** + **body** (of type `T`).
- Builders: `ok(body)`, `created(uri).body(body)`, `noContent().build()`, `notFound().build()`, `badRequest().body(...)`, `status(HttpStatus.X).body(...)`.
- Finish with **`.body(...)`** (with a body) or **`.build()`** (without).
- **Create** → **201** + **`Location`** header + the new object.
- **Delete** → **204 No Content** (`ResponseEntity<Void>`).
- **Not found** → **404**, built without an exception.
- Add headers with `.header("Name", "text value")`.
- **`@ResponseStatus(HttpStatus.CREATED)`** = a short label for "always this status" (but no dynamic headers).
- Rule of thumb: status **depends** on something or you need **headers** → `ResponseEntity`. Always the same → `@ResponseStatus`. Just 200 → return the object.

---

## ❓ Quiz

1. What three things does a `ResponseEntity` contain?
2. Which status code and which header should a successful POST (create) return?
3. Write the code for a 204 response.
4. What does `ResponseEntity<Void>` mean?
5. What's wrong with `return ResponseEntity.notFound();`?
6. Why must we write `String.valueOf(list.size())` in `.header(...)`?
7. When is `@ResponseStatus` a good choice? When is it not enough?
8. What does `ResponseEntity.status(HttpStatus.CONFLICT).body("...")` return?

<details>
<summary>Click to see the answers</summary>

1. A status code, headers, and a body.
2. **201 Created** and the **`Location`** header (with the URL of the new thing).
3. `return ResponseEntity.noContent().build();`
4. A response **without a body**.
5. It's not finished — it needs `.build()` at the end (it doesn't even compile).
6. Header values must be text (`String`), and `size()` is an `int`.
7. Good: when a method always answers with the same status (like 201 or 204). Not enough: when the status depends on something, or when you need headers like `Location`.
8. A response with status **409 Conflict** and that text as the body.

</details>

---

[⬅ Previous chapter](61-put-delete.md) | [Table of Contents](../README.md) | [Next chapter: Layers: Controller, Service, Repository ➡](63-layers.md)
