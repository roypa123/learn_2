# Chapter 52 – Your first web page answer: the Hello endpoint

[⬅ Previous chapter](51-run-first-app.md) | [Table of Contents](../README.md) | [Next chapter ➡](53-dependency-injection.md)

---

## 🎯 Goal

Your server runs, but it says **404** for everything. 😢 Today, it learns to **answer**! 🗣️

At the end of this chapter you will know:

- How to write your first **controller** with **`@RestController`**
- How to make an **endpoint** with **`@GetMapping`**
- What happens **inside** Spring when a request arrives (step by step)
- How to return **text**, and how to return **objects** that become **JSON** automatically ✨
- How to give many endpoints a **common start** with **`@RequestMapping`**
- The most common reasons for **404**, **405**, and empty `{}` answers ⚠️

> 🌱 This is the moment you've been waiting for since Chapter 1! Everything you learned comes together: classes, methods, annotations, records, lists, HTTP, JSON. 🎉

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Controller** | A class that **receives requests** and **sends answers**. The "waiter" of your app. 🧑‍🍳 |
| **Endpoint** | **One address + one method** your API answers to. Example: `GET /hello`. (Chapter 46) |
| **Handler method** | The Java method that **handles** (answers) one endpoint. |
| **Mapping** | A **connection** between a URL path and a Java method: `/hello` → `hello()`. |
| **`@RestController`** | A label: "This class is a controller. What its methods **return** is the response body." |
| **`@GetMapping`** | A label: "Call this method for **GET** requests to this path." |
| **`@RequestMapping`** | A label on a class: "All paths in this class **start with** this." |
| **DispatcherServlet** | Spring's **receptionist**: it receives **every** request and sends it to the right method. 💁 |
| **Serialize** | Turn a Java object into text (here: JSON). Jackson does it for you. |

---

## 📖 Story: The hotel receptionist 🏨

A big hotel has **one front desk** with a **receptionist** 💁, and many **departments**: kitchen 🍳, cleaning 🧹, taxi service 🚕.

A guest comes and says: "I'd like breakfast, please."

1. The **receptionist** listens.
2. She checks her **list**: "Breakfast? → **kitchen**, Chef Tom."
3. She calls Chef Tom. Tom **makes** the breakfast. 🍳
4. The receptionist gives the breakfast to the guest, nicely on a tray. 🍽️

The guest **never** talks to the kitchen directly. And Chef Tom doesn't need to know where the guest came from. He just **cooks**.

In Spring Boot:

| Hotel | Spring Boot |
|---|---|
| The guest 🧑 | The **client** (browser, curl, Postman) |
| "I'd like breakfast" | The **request**: `GET /hello` |
| The receptionist 💁 | **DispatcherServlet** (built into Spring) |
| The list "breakfast → kitchen" | The **mappings**: `/hello` → `hello()` |
| Chef Tom 🍳 | **Your** method: `hello()` |
| The breakfast on a tray 🍽️ | The **response** (status code + headers + body) |

You only write **Chef Tom**. Spring is the receptionist. 😊

---

## 💻 Part 1: Your first controller

### Step 1: Create the class

1. In IntelliJ, **right-click** on the package **`com.example.hello`** (in `src/main/java`).
2. Choose **New → Java Class**.
3. Type the name: **`HelloController`** and press **Enter**.

> ⚠️ Right-click on **`com.example.hello`** — the base package! (Chapter 50.) Then the class is in the right place automatically.

### Step 2: Type the code

```java
package com.example.hello;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello, Spring Boot!";
    }
}
```

> 💡 **Imports:** When you type `@RestController`, IntelliJ shows it in **red**. Press **Alt + Enter** → **Import class**. IntelliJ adds the `import` line for you. Do the same for `@GetMapping`. (Chapter 26)

### Step 3: Restart and visit

1. **Restart** the app (Chapter 51: **Ctrl + F5**, or ⏹️ then ▶️).
2. Open your browser: **`http://localhost:8080/hello`**

```
Hello, Spring Boot!
```

🎉🎉🎉 **Your server answered!** Your first **endpoint** works! 🎉🎉🎉

Remember the `/hello` link on your home page from Chapter 51? Click it now — it works! ✅

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `package com.example.hello;` | The class is in the base package. ✅ Spring will **find** it. |
| `import org.springframework.web.bind.annotation.GetMapping;` | We use `@GetMapping` from Spring Web. |
| `import org.springframework.web.bind.annotation.RestController;` | We use `@RestController` from Spring Web. |
| `@RestController` | ⭐ Label 1: "Spring, this class is a **controller** for a **REST API**. Create **one** object of it (a **bean** 🫘), and use its methods to answer requests." |
| `public class HelloController {` | A normal class. The name ends with `Controller` — not required, but **everyone** does it. |
| `@GetMapping("/hello")` | ⭐ Label 2: "When a **GET** request comes for the path **`/hello`**, call the method below." |
| `public String hello() {` | A normal method. It returns a `String`. The name `hello` can be anything — the **path** is in the label. |
| `return "Hello, Spring Boot!";` | ⭐ The text we return becomes the **body** of the HTTP response. |

**Look how little code!** 😮 Compare with the tiny server from **Chapter 43**: there you had to create a server, choose a port, write headers, turn text into bytes, send them, and close the stream. Here: **one** class, **two** labels, **one** `return`. Spring Boot does everything else. 🪄

### 🔍 Look at the full response with curl

```
curl -i http://localhost:8080/hello
```

```
HTTP/1.1 200 
Content-Type: text/plain;charset=UTF-8
Content-Length: 19
Date: Sat, 10 Oct 2026 16:40:21 GMT

Hello, Spring Boot!
```

| Line | Meaning |
|---|---|
| `HTTP/1.1 200` | **200 OK** ✅ — Spring chose it for you, because your method finished without problems. |
| `Content-Type: text/plain;charset=UTF-8` | "The body is **plain text**, in UTF-8." Spring chose it because you returned a `String`. |
| `Content-Length: 19` | The body is 19 bytes long. ("Hello, Spring Boot!" has 19 characters.) Spring counted for you! |
| `Date: ...` | When the server answered. |
| *(empty line)* | End of headers. (Chapter 44) |
| `Hello, Spring Boot!` | The **body** = what your method returned. |

You wrote **one line** (`return ...`), and Spring made a **complete, correct HTTP response**. 🤩

---

## 🔬 Part 2: What happens inside? (step by step)

Let's follow **one request** through your app. 🔍

```
 🧑 Browser                 🐱 Tomcat            💁 DispatcherServlet         🍳 HelloController
    │                          │                        │                            │
    │ GET /hello               │                        │                            │
    │─────────────────────────►│                        │                            │
    │                          │ "here's a request"     │                            │
    │                          │───────────────────────►│                            │
    │                          │                        │ checks the mapping list:   │
    │                          │                        │ GET /hello → hello() ✅     │
    │                          │                        │───────────────────────────►│
    │                          │                        │                            │ return "Hello,
    │                          │                        │◄───────────────────────────│   Spring Boot!"
    │                          │                        │ String → text/plain body   │
    │                          │                        │ status 200                 │
    │                          │◄───────────────────────│                            │
    │ 200 OK                   │                        │                            │
    │ Hello, Spring Boot!      │                        │                            │
    │◄─────────────────────────│                        │                            │
```

**When the app starts** (once):

1. `@ComponentScan` finds `HelloController` (it has `@RestController`). 🔍
2. Spring creates **one** `HelloController` object — a **bean**. 🫘
3. Spring looks at its methods, finds `@GetMapping("/hello")`, and writes in its **list**: `GET /hello → HelloController.hello()`. 📝

**When a request comes** (every time):

4. **Tomcat** receives the HTTP request from the network (Chapter 43). 🐱
5. Tomcat gives it to **DispatcherServlet** — the receptionist. 💁
6. DispatcherServlet checks the list: "`GET /hello`? That's `hello()`!"
7. It **calls** `hello()` on the bean. (The framework calls **you**! 🎬 Chapter 48.)
8. Your method returns `"Hello, Spring Boot!"`.
9. Spring turns the return value into a **response body**, adds **status** and **headers**.
10. Tomcat sends it back to the browser. 📨

Does this remind you of something? It's exactly your **mini framework** from Chapter 48: a map of paths → methods, then `method.invoke(...)`. 🤓 Now you know Spring isn't magic!

---

## 🍱 Part 3: More endpoints in one controller

One controller can have **many** endpoints. Each method gets its own `@GetMapping`:

```java
package com.example.hello;

import java.time.LocalTime;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello, Spring Boot!";
    }

    @GetMapping("/goodbye")
    public String goodbye() {
        return "Goodbye! See you soon 👋";
    }

    @GetMapping("/time")
    public String time() {
        return "The time is " + LocalTime.now().withNano(0);
    }
}
```

Restart and try:

| URL | Answer |
|---|---|
| `http://localhost:8080/hello` | `Hello, Spring Boot!` |
| `http://localhost:8080/goodbye` | `Goodbye! See you soon 👋` |
| `http://localhost:8080/time` | `The time is 14:30:05` (your time!) |

### 🔍 The new lines

| Code | Meaning |
|---|---|
| `import java.time.LocalTime;` | We need `LocalTime` (Chapter 39). |
| `@GetMapping("/goodbye")` | A second endpoint, for the path `/goodbye`. |
| `"Goodbye! See you soon 👋"` | Emojis work too! Spring sends text as **UTF-8** (`charset=UTF-8`), which has all the emojis. 😊 |
| `LocalTime.now().withNano(0)` | The current time, without the tiny parts of a second (Chapter 39). |

**Refresh** `/time` a few times. The answer **changes**! ⏰ Your method runs **again** for **every** request. It's not a fixed file — it's **code** that runs each time. That's the difference from `static/index.html`. 🧠

---

## ✨ Part 4: Return objects → automatic JSON!

Here's where Spring Boot becomes **really** powerful. 💪 Real APIs don't return plain text. They return **JSON** (Chapter 45). And in Spring Boot, that's... **easy**.

### Step 1: A record for the data

Create a new class in `com.example.hello`: right-click → **New → Java Class** → choose **Record** → name it **`Student`**.

```java
package com.example.hello;

public record Student(String name, int age, boolean active) {
}
```

(A record — Chapter 29. Three fields: name, age, active.)

### Step 2: Return it from an endpoint

Add this method to `HelloController`:

```java
@GetMapping("/student")
public Student student() {
    return new Student("Sara", 12, true);
}
```

### Step 3: Restart and visit `http://localhost:8080/student`

```json
{"name":"Sara","age":12,"active":true}
```

🤯 **JSON!** You didn't write any JSON code. You didn't call Gson. You just **returned an object**.

### 🔍 What happened?

| Code / step | Meaning |
|---|---|
| `public Student student()` | The method returns a **`Student`** object, not a `String`. |
| `return new Student("Sara", 12, true);` | Create a student and return it. |
| *(Spring sees: "This isn't a String!")* | So it asks **Jackson** — the JSON library that came with the web starter (Chapter 48) — to turn it into JSON. |
| *(Jackson reads the record)* | Record components `name`, `age`, `active` → JSON keys `"name"`, `"age"`, `"active"`. |
| `{"name":"Sara","age":12,"active":true}` | The result: a JSON **object** (Chapter 45). Text in quotes, numbers and `true` without. |

With curl you also see the **Content-Type**:

```
curl -i http://localhost:8080/student
```

```
HTTP/1.1 200 
Content-Type: application/json
...

{"name":"Sara","age":12,"active":true}
```

`Content-Type: application/json` — Spring knows it's JSON now. ✅ (In Chapter 45 you did this **by hand** with Gson. Now it's automatic! The name for "turning an object into JSON" is **serializing**.)

> 💡 **Pretty JSON in the browser:** Chrome, Edge and Firefox can show JSON nicely with colors. Firefox does it automatically. In Chrome/Edge, check the **"Pretty-print"** box at the top of the page. 🎨

### Lists become JSON arrays

```java
@GetMapping("/students")
public List<Student> students() {
    return List.of(
            new Student("Sara", 12, true),
            new Student("Tom", 11, false));
}
```

(Add `import java.util.List;` at the top.)

`http://localhost:8080/students`:

```json
[{"name":"Sara","age":12,"active":true},{"name":"Tom","age":11,"active":false}]
```

A Java **`List`** → a JSON **array** `[ ... ]`. Each `Student` → a JSON **object** `{ ... }`. ✨

### Dates become nice text

```java
public record Day(LocalDate date, LocalTime time) {
}
```

```java
@GetMapping("/today")
public Day today() {
    return new Day(LocalDate.of(2026, 10, 10), LocalTime.of(14, 30));
}
```

```json
{"date":"2026-10-10","time":"14:30:00"}
```

Dates and times become **ISO text** (Chapter 39), the standard format for APIs. ✅

### 📋 What becomes what?

| Your method returns... | The client gets... | Content-Type |
|---|---|---|
| `String` | the text itself | `text/plain` |
| a **record** / an object with getters | a JSON **object** `{...}` | `application/json` |
| `List<...>` / `Set<...>` / array | a JSON **array** `[...]` | `application/json` |
| `Map<String, ...>` | a JSON **object** `{...}` (keys from the map) | `application/json` |
| `int`, `double`, `boolean` | a JSON number / `true` / `false` | `application/json` |
| `LocalDate`, `LocalTime` | ISO text like `"2026-10-10"` | (inside JSON) |

---

## 🚦 Part 5: Paths are strict!

Spring compares the path **exactly**. We tested all of these for real:

| Request | Result | Why |
|---|---|---|
| `GET /hello` | ✅ `200` `Hello, Spring Boot!` | Exact match. |
| `GET /Hello` | ❌ `404 Not Found` | Paths are **case-sensitive**: `H` ≠ `h`. |
| `GET /hello/` | ❌ `404 Not Found` | A **slash at the end** is a **different** path. |
| `POST /hello` | ❌ `405 Method Not Allowed` | The path exists, but only for **GET**. |

Here is the real `405` answer from curl:

```
curl -i -X POST http://localhost:8080/hello
```

```
HTTP/1.1 405 
Allow: GET
Content-Type: application/json

{"timestamp":"2026-10-10T16:40:21.431Z","status":405,"error":"Method Not Allowed","path":"/hello"}
```

Look: **`Allow: GET`** — Spring even tells the client **which methods are allowed**! 🤓 (Chapter 44: 405 means "right address, wrong method".)

> 💡 **404 vs 405:** **404** = "I don't know this **path**." **405** = "I know this path, but not with this **method**." This helps a lot when searching for bugs! 🐛

---

## 🏷️ Part 6: A common start for many paths — `@RequestMapping`

Real APIs often start every path with the same words, like `/api/school/...` (Chapter 46). Writing it again and again is boring: 😴

```java
@GetMapping("/api/school")
@GetMapping("/api/school/teachers")
@GetMapping("/api/school/teachers/count")
```

Put the common part on the **class** instead:

```java
@RestController
@RequestMapping("/api/school")
public class SchoolController {

    @GetMapping                       // → /api/school
    public School info() { ... }

    @GetMapping("/teachers")          // → /api/school/teachers
    public List<Teacher> teachers() { ... }
}
```

| Code | Meaning |
|---|---|
| `@RequestMapping("/api/school")` on the class | "**All** paths in this class start with `/api/school`." |
| `@GetMapping` (without a path) | The path is **just** the class part: `/api/school`. |
| `@GetMapping("/teachers")` | Class part + method part = `/api/school/teachers`. |

You'll use this in the mini project right now! ⬇️

---

## 💻 Mini project: The School Info API 🏫

Let's build a small, real **REST API** about a school. It will have **4 endpoints**:

| Method | Path | Answer |
|---|---|---|
| GET | `/api/school` | Information about the school (JSON object) |
| GET | `/api/school/teachers` | All teachers (JSON array) |
| GET | `/api/school/teachers/count` | How many teachers (a number) |
| GET | `/api/school/open` | Is the school open? (`true`/`false`) |

### Step 1: Two records

**`School.java`**

```java
package com.example.hello;

public record School(String name, String city, int students) {
}
```

**`Teacher.java`**

```java
package com.example.hello;

public record Teacher(String name, String subject) {
}
```

### Step 2: The controller

**`SchoolController.java`**

```java
package com.example.hello;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/school")
public class SchoolController {

    @GetMapping
    public School info() {
        return new School("Green Hill School", "Lakeside", 320);
    }

    @GetMapping("/teachers")
    public List<Teacher> teachers() {
        return List.of(
                new Teacher("Mr. Brown", "Math"),
                new Teacher("Ms. Lee", "English"),
                new Teacher("Mrs. Khan", "Science"));
    }

    @GetMapping("/teachers/count")
    public int teacherCount() {
        return teachers().size();
    }

    @GetMapping("/open")
    public boolean isOpen() {
        return true;
    }
}
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `@RestController` | This class answers requests. |
| `@RequestMapping("/api/school")` | Every path here starts with `/api/school`. |
| `@GetMapping` + `public School info()` | `GET /api/school` → returns one `School` → a JSON **object**. |
| `new School("Green Hill School", "Lakeside", 320)` | The data. (In Part 9 this will come from a **database**! For now, it's written in the code.) |
| `@GetMapping("/teachers")` | `GET /api/school/teachers` |
| `List.of(new Teacher(...), ...)` | A list of 3 teachers (Chapter 30) → a JSON **array**. |
| `@GetMapping("/teachers/count")` | `GET /api/school/teachers/count` — a path can have **several parts**. |
| `return teachers().size();` | We **call our own method** `teachers()` and count the list. It's a normal Java method too! 😊 |
| `public int teacherCount()` | Returns an `int` → the JSON number `3`. |
| `public boolean isOpen()` | Returns a `boolean` → JSON `true`. |

### Step 3: Restart and test

Test with curl (or the browser, or Postman — Chapter 47). These are **real** answers:

```
curl http://localhost:8080/api/school
```
```json
{"name":"Green Hill School","city":"Lakeside","students":320}
```

```
curl http://localhost:8080/api/school/teachers
```
```json
[{"name":"Mr. Brown","subject":"Math"},{"name":"Ms. Lee","subject":"English"},{"name":"Mrs. Khan","subject":"Science"}]
```

```
curl http://localhost:8080/api/school/teachers/count
```
```
3
```

```
curl http://localhost:8080/api/school/open
```
```
true
```

🎉 **You built a real REST API!** It follows the rules from Chapter 46: nouns in the path (`school`, `teachers`), GET for reading, JSON answers. 👏

### 📁 Your project now

```
src/main/java/com/example/hello/
├── HelloApplication.java
├── HelloController.java
├── SchoolController.java
├── School.java
├── Student.java
├── Day.java
└── Teacher.java
```

> 💡 It's getting full! In **Chapter 63**, you'll learn to organize classes into **packages** (layers). For now, one package is fine. 😊

---

## ✋ Try it yourself

**Task 1:** Add an endpoint `GET /api/school/principal` that returns a `Teacher` named `"Dr. Green"` with subject `"Everything"` 😄. What JSON do you get?

<details>
<summary>Click to see the answer</summary>

In `SchoolController`:

```java
@GetMapping("/principal")
public Teacher principal() {
    return new Teacher("Dr. Green", "Everything");
}
```

Restart. `http://localhost:8080/api/school/principal`:

```json
{"name":"Dr. Green","subject":"Everything"}
```

</details>

**Task 2:** Make a new controller `DiceController` with an endpoint `GET /dice` that returns `"You rolled a X"`, where X is a random number from 1 to 6. Refresh it many times. 🎲

<details>
<summary>Click to see the answer</summary>

```java
package com.example.hello;

import java.util.Random;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DiceController {

    private final Random random = new Random();

    @GetMapping("/dice")
    public String roll() {
        int number = random.nextInt(1, 7);
        return "You rolled a " + number;
    }
}
```

`random.nextInt(1, 7)` gives a number from 1 to 6 (7 is **not** included). Every refresh calls `roll()` again, so you get a new number: `You rolled a 6`, `You rolled a 4`... 🎲

</details>

**Task 3:** Add `GET /api/school/subjects` that returns a **list of all subjects** (just the texts, like `["Math","English","Science"]`). Use a **stream** (Chapter 36) on `teachers()`!

<details>
<summary>Click to see the answer</summary>

```java
@GetMapping("/subjects")
public List<String> subjects() {
    return teachers().stream()
            .map(Teacher::subject)
            .toList();
}
```

Answer: `["Math","English","Science"]`. A `List<String>` → a JSON array of texts. 🌊

</details>

**Task 4:** Try `http://localhost:8080/api/school/Teachers` (capital T) and `http://localhost:8080/api/school/teachers/`. What status codes do you get? Why?

<details>
<summary>Click to see the answer</summary>

Both give **404 Not Found**. Paths are case-sensitive (`Teachers` ≠ `teachers`), and a slash at the end makes a different path.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: 404 — the controller isn't found

You get `404 Not Found` for your new endpoint. Check these, in order: 🔍

1. ☐ Did you **restart** the app after writing the code? (The #1 reason! 😅)
2. ☐ Is the class in **`com.example.hello`** or **below**? (Chapter 50 — classes outside are silently ignored.)
3. ☐ Does the class have **`@RestController`**?
4. ☐ Does the method have **`@GetMapping`**?
5. ☐ Is the **path** exactly right? (`/hello` vs `/Hello` vs `/hello/`.)
6. ☐ With `@RequestMapping` on the class: did you include the **class part** in the URL? (`/api/school/teachers`, not `/teachers`.)

### Mistake 2: `@Controller` instead of `@RestController`

IntelliJ also suggests `@Controller` (without "Rest"). It looks almost the same... but it's **not**:

```java
@Controller            // ❌ not @RestController!
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello, Spring Boot!";
    }
}
```

We tested it: the answer is **404 Not Found**! 😮 Why? With `@Controller`, Spring thinks the returned text is the **name of an HTML page** (a template — Chapter 89). It searches for a page called "Hello, Spring Boot!"... and doesn't find it. 🤷

**Fix:** For REST APIs, always use **`@RestController`**. ✅

### Mistake 3: Two methods with the same path

```java
@GetMapping("/hello")
public String hello() { ... }

@GetMapping("/hello")       // ❌ the same path again! (maybe in another controller)
public String helloAgain() { ... }
```

The app **doesn't start**. Somewhere in the long error, you find:

```
Caused by: java.lang.IllegalStateException: Ambiguous mapping. Cannot map 'twinController' method 
com.example.hello.TwinController#helloAgain()
to {GET [/hello]}: There is already 'helloController' bean method
com.example.hello.HelloController#hello() mapped.
```

"**Ambiguous**" = "not clear". The receptionist 💁 doesn't know which chef to call! **Fix:** Every method + path combination must be **unique**. Change one of the paths.

### Mistake 4: Returning a class without getters → `{}`

```java
class Pet {
    private String name;
    private int age;
    // a constructor, but NO getters!
}

@GetMapping("/pet")
public Pet pet() {
    return new Pet("Rex", 3);
}
```

Answer: 

```json
{}
```

An **empty** JSON object! 😮 Jackson can only see what a class **shows**: **getters** (`getName()`) or public fields. Private fields without getters are **invisible** to it (Chapter 21 — encapsulation!).

**Fix:** Use a **record** (it has accessor methods automatically ✅), or add getters (`public String getName()`).

### Mistake 5: Sending POST to a GET endpoint (405)

`405 Method Not Allowed` with `Allow: GET` = your endpoint exists, but for a different method. **Fix:** Check the method in curl/Postman. (POST endpoints come in Chapter 60!)

### Mistake 6: Forgetting the imports

`@RestController` and `@GetMapping` are **red** in IntelliJ: "Cannot resolve symbol". **Fix:** **Alt + Enter** → Import class. Make sure you choose the one from **`org.springframework.web.bind.annotation`**.

---

## ✅ Summary

- A **controller** is a class with **`@RestController`**. It answers HTTP requests. 🍳
- **`@GetMapping("/path")`** on a method = "call this method for **GET** `/path`". That's an **endpoint**.
- Return a **`String`** → plain text (`text/plain`). Return a **record/object/list** → **JSON** (`application/json`), made automatically by **Jackson**. ✨
- Spring chooses **status 200**, the **Content-Type**, and the **Content-Length** for you.
- Behind the scenes: Tomcat 🐱 → **DispatcherServlet** 💁 → your method 🍳 → response. (Like your mini framework from Chapter 48!)
- Your method runs **again for every request**.
- **`@RequestMapping("/api/school")`** on the class = a common start for all paths in that class.
- Paths are **strict**: case-sensitive, and `/hello/` ≠ `/hello`. Wrong path → **404**. Wrong method → **405**.
- 404 checklist: **restart**? **base package**? **`@RestController`**? **`@GetMapping`**? **exact path**?
- No getters → `{}`. Use **records**! ✅

---

## ❓ Quiz

1. What two annotations do you need for a simple GET endpoint?
2. What is the URL for this method?
   ```java
   @RestController
   @RequestMapping("/api/zoo")
   public class ZooController {
       @GetMapping("/animals")
       public List<String> animals() { ... }
   }
   ```
3. What Content-Type does the client get if your method returns a `String`? And a record?
4. Who turns your records into JSON?
5. What is DispatcherServlet?
6. You get 404 for your new endpoint. Name three things to check.
7. What's the difference between 404 and 405?
8. Your endpoint returns `{}`. What's probably wrong?
9. What happens if two methods have `@GetMapping("/hello")`?
10. You use `@Controller` instead of `@RestController` and return `"Hi"`. What happens?

<details>
<summary>Click to see the answers</summary>

1. `@RestController` on the class and `@GetMapping("/path")` on the method.
2. `http://localhost:8080/api/zoo/animals`
3. `text/plain` for a String; `application/json` for a record.
4. **Jackson** (it comes with the Spring Web starter).
5. Spring's "receptionist": it receives every request and sends it to the right controller method.
6. Any three: Did you restart? Is the class in the base package (or below)? Does it have `@RestController`? Does the method have `@GetMapping`? Is the path exactly right (case, slash at the end, class prefix)?
7. 404 = the path doesn't exist. 405 = the path exists, but not for this HTTP method.
8. The returned class has no getters (or public fields), so Jackson can't see the data. Use a record or add getters.
9. The app fails to start: "Ambiguous mapping".
10. Spring thinks "Hi" is the name of an HTML template, can't find it, and the client gets a 404.

</details>

---

[⬅ Previous chapter](51-run-first-app.md) | [Table of Contents](../README.md) | [Next chapter: Dependency Injection: the big idea ➡](53-dependency-injection.md)
