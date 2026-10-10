# Chapter 44 – HTTP: GET, POST, PUT, DELETE

[⬅ Previous chapter](43-client-and-server.md) | [Table of Contents](../README.md) | [Next chapter ➡](45-json.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What **HTTP** is: the **language** clients and servers speak
- What an HTTP **request** looks like, part by part
- What an HTTP **response** looks like, part by part
- The **methods**: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- The **status codes**: 200, 201, 204, 400, 401, 403, 404, 405, 409, 500... 🚦
- Important **headers**: `Content-Type`, `Accept`, `Authorization`, `Location`...
- Why HTTP is **stateless**, and how apps still "remember" you (cookies, tokens)
- What **HTTPS** adds 🔒

> 🌱 **Spring Boot note:** Every Spring Boot web app is about HTTP. `@GetMapping`, `@PostMapping`, `ResponseEntity.status(201)`, `@RequestHeader`... they're all HTTP ideas with Java names. Learn HTTP well, and Spring Boot's web part will feel natural!

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **HTTP** | *HyperText Transfer Protocol.* The **rules** for how clients and servers talk on the web. |
| **Protocol** | An agreed set of **rules** for communication. |
| **Method** (or verb) | **What** the client wants to do: GET (read), POST (create)... |
| **Status code** | A **3-digit number** in the response that says how it went: 200 = OK, 404 = not found... |
| **Header** | An extra piece of information: `Content-Type: application/json`. |
| **Body** | The main content: the data sent or received. |
| **Stateless** | The server **doesn't remember** previous requests by itself. |
| **Cookie** | A small piece of data the server asks the browser to **keep** and send back. 🍪 |
| **Token** | A "ticket" 🎟️ that proves who you are, sent with each request. |
| **HTTPS** | HTTP + **encryption** 🔒. |

---

## 📖 Story: The letter 💌

HTTP is like sending **letters** with a very strict format.

Every letter from the client looks like this:

```
 ┌───────────────────────────────────────────┐
 │ WHAT I WANT:  GET  /notes                  │  ← the request line
 │                                           │
 │ From: Chrome browser                      │  ← headers (extra info,
 │ I understand: text, JSON                  │     like on an envelope)
 │ Language: English                         │
 │                                           │
 │ (empty line)                              │
 │                                           │
 │ Dear server, here is my note: "Buy milk"  │  ← body (optional)
 └───────────────────────────────────────────┘
```

And every answer from the server:

```
 ┌───────────────────────────────────────────┐
 │ RESULT:  201 Created ✅                    │  ← the status line
 │                                           │
 │ Type of content: plain text               │  ← headers
 │ Length: 19 characters                     │
 │                                           │
 │ (empty line)                              │
 │                                           │
 │ Saved note number 1                       │  ← body
 └───────────────────────────────────────────┘
```

Both sides **must** follow the format. That's why any browser can talk to any server in the world! 🌍

---

## 📨 Part 1: The HTTP request

Here is a **real** request, sent to a small server we'll build in Part 6:

```http
POST /notes HTTP/1.1
Host: localhost:8080
User-Agent: curl/8.21.0
Accept: */*
Content-Type: application/x-www-form-urlencoded
Content-Length: 12

Call grandma
```

### 🔍 Line by line

**Line 1 — the request line**

```
POST /notes HTTP/1.1
```

| Part | Meaning |
|---|---|
| `POST` | The **method**: what to do. Here: "**create** something new". |
| `/notes` | The **path**: which thing (Chapter 43). Including the query, if any: `/notes?page=2`. |
| `HTTP/1.1` | The **version** of HTTP. (Newer versions HTTP/2 and HTTP/3 are faster, but the ideas are the same.) |

**Next lines — headers** (one per line, `Name: value`)

| Header | Meaning |
|---|---|
| `Host: localhost:8080` | Which server I'm talking to. |
| `User-Agent: curl/8.21.0` | **Who** I am (which program). Browsers send something like `Mozilla/5.0 ... Chrome/...`. |
| `Accept: */*` | Which kinds of answer I understand. `*/*` = anything. |
| `Content-Type: ...` | What **kind** of data is in **my** body. |
| `Content-Length: 12` | How **long** my body is (12 bytes: `Call grandma`). |

**An empty line** — means "headers are finished, the body starts now".

**The body**

```
Call grandma
```

The actual data. A `GET` request usually has **no** body. A `POST` or `PUT` usually **has** one (often **JSON** — Chapter 45).

---

## 📬 Part 2: The HTTP response

The server's answer:

```http
HTTP/1.1 201 Created
Date: Sat, 10 Oct 2026 16:22:29 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 19

Saved note number 3
```

### 🔍 Line by line

**Line 1 — the status line**

```
HTTP/1.1 201 Created
```

| Part | Meaning |
|---|---|
| `HTTP/1.1` | version |
| `201` | the **status code**: a number that says **how it went**. |
| `Created` | a short **text** for humans (the "reason phrase"). |

**Headers**

| Header | Meaning |
|---|---|
| `Date: ...` | When the answer was made. |
| `Content-Type: text/plain; charset=utf-8` | What kind of data is in the body: plain text, UTF-8 letters. |
| `Content-Length: 19` | The body is 19 bytes long. |

**Empty line**, then the **body**:

```
Saved note number 3
```

---

## 🛠️ Part 3: HTTP methods — what do you want to do?

The **method** is the **verb** — the action. 🎬

| Method | Meaning | Restaurant 🍽️ | Has a body? |
|---|---|---|---|
| **GET** | **Read** / get something | "Show me the menu" / "What's my order?" | ❌ no |
| **POST** | **Create** something new | "Place a **new** order" | ✅ yes |
| **PUT** | **Replace** something completely | "**Change** my whole order to: pasta + water" | ✅ yes |
| **PATCH** | **Change part** of something | "Just add extra cheese to my order" | ✅ yes |
| **DELETE** | **Remove** something | "**Cancel** my order" | ❌ usually no |

### CRUD — the 4 basic actions

Almost every app does 4 things with data. Programmers call them **CRUD**:

| CRUD | Meaning | HTTP method | Example |
|---|---|---|---|
| **C**reate | make new | `POST` | add a new student |
| **R**ead | look at | `GET` | show a student |
| **U**pdate | change | `PUT` / `PATCH` | change a student's email |
| **D**elete | remove | `DELETE` | remove a student |

🌱 In Spring Boot (Chapters 57–61):

| HTTP | Spring Boot annotation |
|---|---|
| GET | `@GetMapping` |
| POST | `@PostMapping` |
| PUT | `@PutMapping` |
| PATCH | `@PatchMapping` |
| DELETE | `@DeleteMapping` |

### Two important properties

**Safe** = only **reads**, never changes anything on the server. 🛡️
**Idempotent** = doing it **2 times** has the **same result** as doing it **1 time**.

| Method | Safe? | Idempotent? | Why |
|---|---|---|---|
| GET | ✅ | ✅ | Reading the menu 10 times changes nothing. |
| POST | ❌ | ❌ | Ordering a pizza 2 times → **2 pizzas**! 🍕🍕 |
| PUT | ❌ | ✅ | "Set my order to pasta" 2 times → still just pasta. |
| DELETE | ❌ | ✅ | Canceling 2 times → it's still canceled. |

👉 **Why care?** Browsers and tools may **repeat** safe/idempotent requests automatically (for example, if the network is slow). They will **never** silently repeat a POST. That's why, when you reload a page after submitting a form, the browser asks: "Do you want to send the form **again**?" 🤔

> ⚠️ **Rule:** A `GET` must **never change** data. Never write `GET /deleteStudent?id=5`! Use `DELETE /students/5`. (A search engine visiting all your links could delete everything! 😱)

---

## 🚦 Part 4: Status codes — how did it go?

Every response has a **3-digit status code**. The **first digit** tells you the **family**:

| Family | Meaning | Mood |
|---|---|---|
| **1xx** | "Wait, still working..." (rare) | ⏳ |
| **2xx** | **Success!** | ✅😀 |
| **3xx** | "It's somewhere else" (redirect) | ➡️ |
| **4xx** | **The client made a mistake** | ❌🙋 "your fault" |
| **5xx** | **The server made a mistake** | 💥👨‍🍳 "our fault" |

### The codes you must know ⭐

| Code | Name | When | Restaurant 🍽️ |
|---|---|---|---|
| **200** | OK | Success. Here's your data. | "Here's your food." |
| **201** | Created | Success. Something **new** was created (after POST). | "Your order is placed — order #42." |
| **204** | No Content | Success, but nothing to send back (often after DELETE). | "Done. Nothing more to say." 🤐 |
| **301** / **302** | Moved | The thing is at another address. | "We moved to the restaurant next door." |
| **304** | Not Modified | "You already have the newest version." (caching) | "You already have the menu." |
| **400** | Bad Request | The request is **wrong** (bad data, missing field). | "I can't read your order." 📝❓ |
| **401** | Unauthorized | You must **log in** first. (Really means "unauthenticated".) | "Who are you? Show your membership card." 🪪 |
| **403** | Forbidden | You're logged in, but **not allowed**. | "Sorry, the kitchen is staff only." 🚫 |
| **404** | Not Found | This thing **doesn't exist**. | "We don't have that dish." 🤷 |
| **405** | Method Not Allowed | This path exists, but not with this method. | "You can't **cancel** the menu." |
| **409** | Conflict | Clash with the current state (e.g. email already used). | "That table is already booked." |
| **422** | Unprocessable | The data format is OK but the content breaks rules. | "We can't make pizza without dough." |
| **429** | Too Many Requests | Slow down! | "One order at a time, please!" 🐢 |
| **500** | Internal Server Error | The server **crashed** (a bug, an exception!). | "The kitchen is on fire!" 🔥 |
| **503** | Service Unavailable | The server is down or too busy. | "We're closed for cleaning." 🧹 |

> 💡 **Easy memory trick:** 4xx = **"you"** did something wrong. 5xx = **"we"** (the server) did something wrong.

🌱 **In Spring Boot:**
- Return data normally → **200** automatically.
- Throw an unhandled exception → **500** automatically. 💥
- You choose others with `ResponseEntity` and `@ResponseStatus` (Chapters 62, 66). For example, "student not found" → **404**.

> 😄 Fun fact: there's a joke status code **418 I'm a teapot** ☕ — a server that refuses to make coffee because it's a teapot!

---

## 🏷️ Part 5: Headers — the information on the envelope

Headers carry **extra information** about the request or response. There are many, but you'll mostly use these:

### `Content-Type` — "what kind of data is in my body?"

| Value | Meaning |
|---|---|
| `application/json` | **JSON** data (Chapter 45) — ⭐ the most common for APIs |
| `text/plain` | plain text |
| `text/html` | an HTML web page |
| `application/x-www-form-urlencoded` | data from a simple HTML form (`name=Sara&age=12`) |
| `multipart/form-data` | a form with **files** (uploads — Chapter 92) |
| `image/png`, `image/jpeg` | images |

The format is called a **media type** (or MIME type): `type/subtype`.

### `Accept` — "what kind of answer do I want?"

```
Accept: application/json
```

"Please answer in JSON." The server tries to follow it.

### `Authorization` — "here's my proof of who I am" 🎟️

```
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzYXJhIn0.abc123
```

Used to send a **token** (Chapter 83 — JWT). "Bearer" means "the person **carrying** this token".

### `Location` — "here's where the new thing is"

After a `POST` that creates something, the server answers:

```
HTTP/1.1 201 Created
Location: /api/students/42
```

"Created! You can find it at `/api/students/42`." 🗺️

### Other useful headers

| Header | Direction | Meaning |
|---|---|---|
| `Content-Length` | both | size of the body |
| `User-Agent` | request | which program is asking |
| `Cookie` / `Set-Cookie` | request / response | cookies 🍪 (Part 7) |
| `Cache-Control` | response | how long the client may keep a copy |
| `Access-Control-Allow-Origin` | response | **CORS** — which websites may call this API (you'll meet this later!) |

> 💡 Header names are **not** case-sensitive: `Content-Type` = `content-type`. (That's why our tiny server showed `Content-type`.)

🌱 In Spring Boot, you read headers with `@RequestHeader("Accept") String accept`, and set them with `ResponseEntity.ok().header(...)`.

---

## 🔬 Part 6: See HTTP for real — a notes server

Let's make our tiny Java server from Chapter 43 understand **methods** and **status codes**!

**File: `NotesServer.java`**

```java
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class NotesServer {
    private static final List<String> notes = new ArrayList<>();

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);

        server.createContext("/notes", exchange -> {
            String method = exchange.getRequestMethod();
            System.out.println("📨 " + method + " " + exchange.getRequestURI());

            switch (method) {
                case "GET" -> send(exchange, 200, "Notes: " + notes);
                case "POST" -> {
                    String text = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8).strip();
                    if (text.isEmpty()) {
                        send(exchange, 400, "A note cannot be empty");
                    } else {
                        notes.add(text);
                        send(exchange, 201, "Saved note number " + notes.size());
                    }
                }
                default -> send(exchange, 405, "Method " + method + " is not allowed here");
            }
        });

        server.start();
        System.out.println("🚀 Notes server running at http://localhost:8080/notes");
    }

    private static void send(HttpExchange exchange, int status, String text) throws IOException {
        byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream body = exchange.getResponseBody()) {
            body.write(bytes);
        }
    }
}
```

### 🔍 Key lines

| Code | HTTP idea |
|---|---|
| `exchange.getRequestMethod()` | Read the **method** (GET, POST...). |
| `case "GET" -> send(exchange, 200, ...)` | Reading → **200 OK**. |
| `exchange.getRequestBody().readAllBytes()` | Read the request **body** (the note text). |
| `send(exchange, 400, ...)` | Empty note → **400 Bad Request** (client's fault). |
| `send(exchange, 201, ...)` | New note saved → **201 Created**. |
| `default -> send(exchange, 405, ...)` | Any other method → **405 Method Not Allowed**. |
| `set("Content-Type", "text/plain; charset=utf-8")` | A **header** saying what's in the body. |

### Try it 🧪

Run `NotesServer`. Then open `http://localhost:8080/notes` in your browser:

```
Notes: []
```

A browser address bar can **only** send **GET** requests. 😕 To send POST and DELETE, we need a tool like **curl** or **Postman** (Chapter 47 explains them fully). Here's a sneak peek with **curl** (it's already installed on Windows 10/11, Mac and Linux). Open a **second** terminal:

```
curl -i -X POST -d "Buy milk" http://localhost:8080/notes
```

```
HTTP/1.1 201 Created
Date: Sat, 10 Oct 2026 16:22:28 GMT
Content-type: text/plain; charset=utf-8
Content-length: 19

Saved note number 1
```

(`-i` = show the status and headers, `-X POST` = use the POST method, `-d "..."` = the body.)

```
curl -i -X POST -d "" http://localhost:8080/notes
```

```
HTTP/1.1 400 Bad Request
Content-type: text/plain; charset=utf-8
Content-length: 22

A note cannot be empty
```

```
curl -i -X DELETE http://localhost:8080/notes
```

```
HTTP/1.1 405 Method Not Allowed
Content-type: text/plain; charset=utf-8
Content-length: 33

Method DELETE is not allowed here
```

Reload the browser page:

```
Notes: [Buy milk]
```

🎉 You see **real HTTP**: methods, status codes, headers and bodies — the same things Spring Boot works with!

> 💡 **Windows PowerShell note:** In older Windows PowerShell, `curl` may be a different command. If it behaves strangely, type **`curl.exe`** instead of `curl`. (Chapter 47.)

---

## 🧠 Part 7: HTTP is stateless — so how does the server remember me?

**Stateless** means: every request is **independent**. The server does **not** automatically remember your earlier requests. 🐠 (Like a goldfish! 😄)

📖 **Story:** Imagine a bakery where the baker **forgets every customer** the moment they leave. Each time you come back: "Hello! Who are you? What do you want?" Even if you were there 5 seconds ago.

That's simple and **scales well** (any server in a big group can answer any request). But then — how does Instagram know you're logged in? 🤔

**Answer:** the **client** sends a "**reminder**" with **every** request.

### Way 1: Cookies 🍪

1. You log in. The server answers with:
   ```
   Set-Cookie: SESSION=abc123; HttpOnly; Secure
   ```
   "Browser, please **keep** this cookie."
2. The browser **automatically** sends it with every next request to that site:
   ```
   Cookie: SESSION=abc123
   ```
3. The server looks up `abc123` → "Ah, that's Sara!" 👋

### Way 2: Tokens 🎟️ (common for APIs)

1. You log in. The server gives you a **token** (like a concert wristband).
2. The client sends it in **every** request:
   ```
   Authorization: Bearer eyJhbGciOi...
   ```
3. The server checks the token → "Valid! This is Sara."

🌱 Spring Security handles both (Chapters 80–83). **JWT tokens** are very popular with Spring Boot APIs.

---

## 🔒 Part 8: HTTPS — HTTP with a lock

With plain **HTTP**, everything is sent as **readable text**. Anyone between you and the server (on public Wi-Fi ☕📶, for example) could **read** your passwords! 😱

**HTTPS** = HTTP + **TLS encryption**. The content is scrambled 🔐 — only the browser and the server can read it.

```
 HTTP:   "password=secret123"        ← anyone can read 👀
 HTTPS:  "x8$kQ!2@zL#9pW..."          ← scrambled 🔒
```

| | HTTP | HTTPS |
|---|---|---|
| Encrypted? | ❌ | ✅ |
| Default port | 80 | 443 |
| Browser shows | "Not secure" ⚠️ | 🔒 lock icon |
| Use for | local development (`localhost`) | **everything** on the real internet |

👉 During development, `http://localhost:8080` is fine. When you **deploy** (Chapter 100), your app **must** use HTTPS. Usually the hosting platform does it for you. 😊

---

## ✋ Try it yourself

**Task 1:** Which method?
1. Show all products
2. Add a new product
3. Change the price of product 7 (only the price)
4. Remove product 7
5. Replace all the information of product 7

<details>
<summary>Click to see the answers</summary>

1. GET
2. POST
3. PATCH (or PUT, if the API only offers PUT)
4. DELETE
5. PUT

</details>

**Task 2:** Which status code?
1. A student was created successfully
2. The student with id 99 doesn't exist
3. The email field is missing in the request
4. The server threw a `NullPointerException`
5. A user tries to delete something, but they're not an admin
6. A user is not logged in at all
7. A student was deleted, nothing to send back

<details>
<summary>Click to see the answers</summary>

1. 201 Created
2. 404 Not Found
3. 400 Bad Request
4. 500 Internal Server Error
5. 403 Forbidden
6. 401 Unauthorized
7. 204 No Content

</details>

**Task 3:** Read this request. What does the client want? What kind of data does it send? What does it want back?

```http
PUT /api/students/12 HTTP/1.1
Host: school.example.com
Content-Type: application/json
Accept: application/json
Authorization: Bearer abc.def.ghi

{"name": "Sara Ali", "email": "sara@school.com"}
```

<details>
<summary>Click to see the answer</summary>

It wants to **replace** (PUT) the student with id 12. It sends **JSON** (Content-Type). It wants **JSON** back (Accept). It proves who it is with a **token** (Authorization). The body has the new name and email.

</details>

**Task 4:** Run the `NotesServer`. Use curl to add 3 notes, then view them in the browser. Try `PUT`. What status do you get?

**Task 5:** Open the Developer Tools (F12 → Network) on any website. Click on the first request. Find: the **method**, the **status code**, the **Content-Type** of the response, and the **User-Agent** of your request.

---

## ⚠️ Common mistakes

### Mistake 1: Using GET to change data

```
GET /deleteNote?id=5   ❌
DELETE /notes/5        ✅
```

GET must be **safe** — never change anything.

### Mistake 2: Always returning 200

Returning `200 OK` with the text "Error: not found" confuses clients. 😕 **Use the right status code** (404). Programs read the **number**, not your text!

### Mistake 3: Mixing up 401 and 403

- **401** = "I don't know **who** you are" → log in.
- **403** = "I know who you are, but you're **not allowed**."

### Mistake 4: Wrong `Content-Type`

Sending JSON but saying `Content-Type: text/plain` → the server may refuse it (**415 Unsupported Media Type**) or not understand it. 🌱 Spring Boot needs `Content-Type: application/json` to read a JSON body!

### Mistake 5: Expecting the browser address bar to send POST

The address bar always sends **GET**. Use curl, Postman, or a form/JavaScript.

### Mistake 6: Sending passwords over HTTP on the internet

Always use **HTTPS** for real apps. 🔒

---

## ✅ Summary

- **HTTP** is the language of the web: the client sends a **request**, the server sends a **response**. 💌
- **Request** = request line (`METHOD /path HTTP/1.1`) + headers + empty line + optional body.
- **Response** = status line (`HTTP/1.1 200 OK`) + headers + empty line + body.
- **Methods (CRUD):** GET = read, POST = create, PUT = replace, PATCH = change part, DELETE = remove.
- GET is **safe** (never changes data). POST is **not idempotent** (twice = two things).
- **Status codes:** 2xx success ✅, 3xx redirect ➡️, 4xx **client** error ❌, 5xx **server** error 💥.
  - Know: **200, 201, 204, 400, 401, 403, 404, 405, 409, 500**.
- **Headers:** `Content-Type` (what I send), `Accept` (what I want), `Authorization` (who I am), `Location` (where the new thing is).
- HTTP is **stateless** → cookies 🍪 or tokens 🎟️ remind the server who you are.
- **HTTPS** = encrypted HTTP 🔒. Always use it on the real internet.
- Spring Boot: `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `ResponseEntity`... are HTTP in Java. 🌱

---

## ❓ Quiz

1. What are the parts of an HTTP request?
2. What does the status code family 4xx mean? And 5xx?
3. Which method creates something new? Which one reads?
4. What status code means "created successfully"?
5. What is the `Content-Type` header for?
6. What does "stateless" mean? How does a server still know who you are?
7. Why should GET never change data?
8. What's the difference between HTTP and HTTPS?

<details>
<summary>Click to see the answers</summary>

1. The request line (method, path, version), headers, an empty line, and an optional body.
2. 4xx: the client made a mistake. 5xx: the server made a mistake.
3. POST creates. GET reads.
4. 201 Created.
5. It says what kind of data is in the body (for example `application/json`).
6. The server doesn't remember earlier requests by itself. The client sends a cookie or a token with every request.
7. Because GET is supposed to be safe — browsers, tools and search engines may send GET requests at any time (even repeat them).
8. HTTPS encrypts the data (🔒); HTTP sends readable text.

</details>

---

[⬅ Previous chapter](43-client-and-server.md) | [Table of Contents](../README.md) | [Next chapter: JSON ➡](45-json.md)
