# Chapter 43 – Client and Server: The Restaurant Story

[⬅ Previous chapter](../part-05-tools/42-git.md) | [Table of Contents](../README.md) | [Next chapter ➡](44-http.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **client** and a **server** are
- What happens when you type a web address and press **Enter** 🌐
- What **IP addresses**, **domain names** and **DNS** are
- What a **port** is (and why Spring Boot uses **8080**)
- How to read a **URL**: `https://shop.com:443/products/42?color=red`
- What **localhost** means
- How to see web traffic with your browser's **Developer Tools** 🔍
- How to build a **tiny web server in plain Java** — before Spring Boot! 🚀

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Client** | The program that **asks** for something. Usually a web browser or a phone app. |
| **Server** | The program that **answers**. It waits for requests and sends responses. |
| **Request** | The **question** the client sends. |
| **Response** | The **answer** the server sends back. |
| **IP address** | The **number address** of a computer on a network: `142.250.74.110`. |
| **Domain name** | The **human-friendly name** of a server: `google.com`. |
| **DNS** | The internet's **phone book**: turns domain names into IP addresses. |
| **Port** | A **door number** on a computer. Each server program listens at one door. |
| **URL** | The full **web address**: `https://example.com/page`. |
| **localhost** | "**This** computer." |
| **Backend** | The **server** part of an app (Spring Boot! 🌱). |
| **Frontend** | The part the user **sees**: web pages, phone apps. |

---

## 📖 Story: The restaurant 🍽️

You go to a restaurant.

```
     🧑 YOU                    🧑‍🍳 WAITER                 👨‍🍳 KITCHEN
   (the customer)          (takes the order)        (makes the food)
        │                         │                         │
        │  "One pizza, please!"   │                         │
        │ ──────────────────────► │  "Table 5: one pizza"   │
        │                         │ ──────────────────────► │
        │                         │                         │ 🍕 cooking...
        │                         │      🍕                 │
        │                         │ ◄────────────────────── │
        │        🍕               │                         │
        │ ◄────────────────────── │                         │
        │   "Here is your pizza!" │                         │
```

1. You **ask** for something (the **order**).
2. The kitchen **prepares** it.
3. You **get** the food back (the **answer**).

On the web, it's the same:

| Restaurant | Web |
|---|---|
| 🧑 You, the customer | **Client** (your browser 🌐 or a phone app 📱) |
| 📝 Your order | **Request** |
| 👨‍🍳 The kitchen | **Server** (a program on another computer) |
| 🍕 The food | **Response** (a web page, data, an image...) |
| 📋 The menu | The list of things the server can do (the **API** — Chapter 46) |

Important rules of the restaurant:
- The **customer always starts**. The kitchen never brings food you didn't order. (The client always asks first.)
- The kitchen serves **many customers** at the same time. (A server answers many clients.)
- Every order gets **one** answer — food, or "sorry, we don't have that" (an **error**).

👉 **With Spring Boot, you will build the kitchen!** 👨‍🍳🌱

---

## 🖥️ Part 1: Clients and servers

### Clients 🧑

A **client** is any program that **sends requests**:

| Client | Example |
|---|---|
| A web browser | Chrome, Edge, Firefox, Safari 🌐 |
| A phone app | Instagram, a weather app 📱 |
| Another server | A shop's server asking a bank's server "Is this payment OK?" 🏦 |
| A tool for developers | Postman, curl (Chapter 47) 🧰 |

### Servers 👨‍🍳

A **server** is a program that **waits** for requests and **answers** them. It runs **all the time** (24 hours a day, 7 days a week) on a computer, usually in a big **data center** (the "cloud" ☁️).

> 💡 "Server" means **both** the program and the computer it runs on. Usually the meaning is clear from the sentence.

### Frontend and backend

```
   FRONTEND (what users see)              BACKEND (the kitchen)               DATABASE
 ┌──────────────────────────┐         ┌────────────────────────┐        ┌──────────────┐
 │ 🌐 web page               │ request │  🌱 Spring Boot app     │ asks   │  🗄️ stored    │
 │ 📱 phone app              │ ──────► │  - business rules       │ ─────► │  data         │
 │ (buttons, forms, colors) │ ◄────── │  - security             │ ◄───── │  (students,   │
 │                          │ response│  - calculations         │        │   orders...)  │
 └──────────────────────────┘         └────────────────────────┘        └──────────────┘
   HTML, CSS, JavaScript,              Java + Spring Boot ☕              MySQL, PostgreSQL,
   Blazor (Part 2 of our books!)                                         H2...
```

👉 This book teaches the **backend** (Spring Boot). The **Blazor** book (later!) teaches a **frontend**. Together, they make a full application! 🎉

---

## 🔢 Part 2: IP addresses — the house numbers of computers

Every computer on the internet has an **address**, like a house has a street number. 🏠 It's called an **IP address**:

```
 142.250.74.110          ← IPv4: 4 numbers, each from 0 to 255
 2a00:1450:4001:82a::200e ← IPv6: a newer, longer format
```

When your browser wants to talk to a server, it must know the server's IP address. But who remembers numbers like `142.250.74.110`? 🤯

---

## 📒 Part 3: Domain names and DNS — the phone book

Humans like **names**: `google.com`, `wikipedia.org`, `spring.io`. These are **domain names**.

**DNS** (Domain Name System) is the internet's **phone book** 📒. It turns names into IP addresses:

```
 You type: spring.io
      │
      ▼
 ┌─────────────────────────────┐
 │ 📒 DNS: "spring.io?"         │
 │    → "That's 104.18.x.x"     │
 └─────────────────────────────┘
      │
      ▼
 Your browser connects to 104.18.x.x 🔌
```

📞 **Story:** You want to call your friend Sara. You don't remember her number, so you look up "Sara" in your phone's **contacts**. The phone finds the number and calls it. DNS does this for websites!

---

## 🚪 Part 4: Ports — the door numbers

One computer can run **many** server programs at the same time: a web server, an email server, a database... How does a request find the **right** program?

With a **port** — a **door number** 🚪 (from 0 to 65535).

```
 🏢 One server computer (IP 203.0.113.5)
 ┌──────────────────────────────────────────┐
 │  🚪 door 80    → web server (http)        │
 │  🚪 door 443   → web server (https) 🔒    │
 │  🚪 door 5432  → PostgreSQL database 🗄️    │
 │  🚪 door 8080  → YOUR Spring Boot app 🌱  │
 └──────────────────────────────────────────┘
```

📮 **Story:** An apartment building has **one street address** (IP), but **many apartments** (ports). The letter needs **both**: "Main Street 5, apartment 8080".

### Ports you'll meet

| Port | Used by |
|---|---|
| **80** | HTTP websites (the default) |
| **443** | HTTPS websites 🔒 (the default) |
| **8080** | 🌱 **Spring Boot** (the default for development!) |
| 3306 | MySQL database |
| 5432 | PostgreSQL database |
| 3000, 5000, 5173 | Other development servers (JavaScript tools, .NET...) |

> 💡 You don't see `:80` or `:443` in normal web addresses, because they're the **defaults** — the browser adds them secretly. For other ports, you must write them: `http://localhost:8080`.

---

## 🏠 Part 5: localhost — "this computer"

When you develop, the **client** (your browser) and the **server** (your Spring Boot app) run on the **same** computer: yours! 💻

The special name **`localhost`** means "**this computer**". Its IP address is **`127.0.0.1`**.

```
 💻 Your computer
 ┌───────────────────────────────────────────────────────┐
 │  🌐 Browser                     🌱 Spring Boot app     │
 │  "http://localhost:8080/hello"  listening at door 8080 │
 │        │                              ▲                │
 │        └──────── request ─────────────┘                │
 │        ◄──────── response ────────────┘                │
 └───────────────────────────────────────────────────────┘
```

The request **never leaves your computer**. No internet needed! 😊

> 💡 Other people **can't** reach your `localhost` — it's private to your computer. To make your app public, you **deploy** it to a server (Chapter 100). 🚀

---

## 🔗 Part 6: Reading a URL

A **URL** (Uniform Resource Locator) is a complete web address. Let's take one apart:

```
 https://shop.example.com:443/products/42?color=red&size=M#reviews
 └─┬──┘   └──────┬───────┘└┬┘└────┬────┘ └────────┬───────┘└──┬──┘
 scheme         host      port   path           query       fragment
```

| Part | Example | Meaning |
|---|---|---|
| **Scheme** | `https` | **How** to talk: `http` or `https` (🔒 secure, encrypted). |
| **Host** | `shop.example.com` | **Which** server (domain name or IP). |
| **Port** | `443` | **Which door**. Usually hidden (default). |
| **Path** | `/products/42` | **What** you want on that server — like a folder path. |
| **Query** | `?color=red&size=M` | **Extra options**: `name=value` pairs, starting with `?`, separated by `&`. |
| **Fragment** | `#reviews` | A spot **inside** the page (only for the browser; the server never sees it). |

### More examples

| URL | Host | Port | Path | Query |
|---|---|---|---|---|
| `http://localhost:8080/hello` | localhost | 8080 | `/hello` | — |
| `https://en.wikipedia.org/wiki/Java` | en.wikipedia.org | 443 (hidden) | `/wiki/Java` | — |
| `http://localhost:8080/api/students?page=2&size=10` | localhost | 8080 | `/api/students` | `page=2&size=10` |
| `https://www.google.com/search?q=spring+boot` | www.google.com | 443 (hidden) | `/search` | `q=spring+boot` |

🌱 **In Spring Boot**, you'll decide **paths** (`@GetMapping("/students")` — Chapter 57) and read **path parts** (`/students/42` — Chapter 58) and **query parameters** (`?page=2` — Chapter 59). Now you know what they are!

### Special characters in URLs

URLs can't contain spaces or some special characters. They are **encoded**:

| Character | Encoded |
|---|---|
| space | `%20` (or `+` in queries) |
| `é` | `%C3%A9` |
| `&` (inside a value) | `%26` |

Example: searching for "spring boot" → `?q=spring%20boot`. The browser does this for you. 😊

---

## 🎬 Part 7: What happens when you press Enter?

You type `https://spring.io` and press **Enter**. In less than a second: ⚡

```
 1. 📒 DNS        Browser asks: "What's the IP of spring.io?" → gets an IP address.
 2. 🔌 Connect    Browser connects to that IP, at door 443.
 3. 🔒 Secure     Browser and server agree on encryption (because of https).
 4. 📨 Request    Browser sends: "GET / please" (the request — Chapter 44).
 5. 👨‍🍳 Work       The server prepares the answer (maybe reads a database).
 6. 📬 Response   Server sends: "200 OK, here is the HTML page".
 7. 🎨 Show       Browser reads the HTML and draws the page.
 8. 🔁 Repeat     The page needs images, styles, scripts → more requests! (often 50+)
```

All of this happens **every time** you open a page. 🤯

---

## 🔍 Part 8: See it yourself — Developer Tools

Every browser has hidden **Developer Tools** that show **all** the requests and responses! 🕵️

1. Open Chrome or Edge.
2. Press **F12** (or right-click the page → **Inspect**).
3. Click the **Network** tab.
4. Go to any website (or reload with **F5**).

You'll see a list of every request:

```
 Name                 Status   Type        Size     Time
 ─────────────────────────────────────────────────────────
 spring.io            200      document    45 kB    120 ms
 main.css             200      stylesheet  30 kB     40 ms
 logo.svg             200      svg          3 kB     15 ms
 analytics.js         200      script      12 kB     60 ms
 ...
```

Click on one → you see its **Headers**, its **Response**, and more. We'll understand all of these in Chapter 44!

👉 Developer Tools will be **very useful** when you test your own Spring Boot app. 🛠️

---

## 🚀 Part 9: A tiny server in plain Java

Time to **build a kitchen**! 👨‍🍳 Java has a small built-in web server. Let's use it to see that a server is **just a program** that waits and answers.

> ⚠️ This is **only for learning**. Real apps use Spring Boot (it's much more powerful and easier). But seeing the basics first helps you understand what Spring Boot does for you! 🧠

Create a plain Java project (or any folder) with this file:

**File: `TinyServer.java`**

```java
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.LocalTime;

public class TinyServer {
    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);

        server.createContext("/hello", exchange -> {
            String answer = "Hello from my tiny Java server! The time is " + LocalTime.now().withNano(0);
            byte[] bytes = answer.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
            exchange.sendResponseHeaders(200, bytes.length);
            try (OutputStream body = exchange.getResponseBody()) {
                body.write(bytes);
            }
            System.out.println("📨 Someone asked for /hello");
        });

        server.start();
        System.out.println("🚀 Server is running. Open http://localhost:8080/hello");
    }
}
```

### 🔍 Line by line

| Code | Meaning | Restaurant |
|---|---|---|
| `HttpServer.create(new InetSocketAddress(8080), 0)` | Create a server that listens at **port 8080**. | Open the restaurant at door 8080 🚪 |
| `server.createContext("/hello", exchange -> { ... })` | "When someone asks for the **path** `/hello`, run this **lambda** (Chapter 35)." | A menu item: "hello" 📋 |
| `exchange` | One request + its response (the "exchange" between client and server). | One customer's order 📝 |
| `String answer = ...` | Prepare the answer text. | Cook the food 🍳 |
| `getResponseHeaders().set("Content-Type", ...)` | Tell the client **what kind** of answer this is: plain text. (Chapter 44.) | "This is a pizza" label 🏷️ |
| `sendResponseHeaders(200, bytes.length)` | Send the **status** `200` = "OK, success!" (Chapter 44.) | "Here's your order!" ✅ |
| `body.write(bytes)` | Send the answer itself. (try-with-resources closes it — Chapter 33!) | Put the food on the table 🍕 |
| `server.start()` | Start waiting for requests. The program keeps running! | Open the doors 🔓 |

### Run it ▶️

Run `TinyServer` in IntelliJ (or `java TinyServer.java` in the terminal).

```
🚀 Server is running. Open http://localhost:8080/hello
```

Notice: the program **doesn't stop**! A server **waits** for customers. ⏳

### Visit it 🌐

Open your browser and go to:

```
http://localhost:8080/hello
```

You see:

```
Hello from my tiny Java server! The time is 21:50:38
```

🎉🎉🎉 **You built a web server!** Your browser (the **client**) sent a **request** to your program (the **server**), and got a **response**!

Look at IntelliJ's Run window:

```
📨 Someone asked for /hello
```

Reload the page (F5) → a new time, and a new line in the log. Every reload = one new request. 🔁

### Try another path

```
http://localhost:8080/pizza
```

```
404 Not Found
No context found for request
```

We didn't create a `/pizza` "menu item", so the server says **404 — not found**. (Chapter 44 explains status codes.)

### Stop the server ⏹️

Click the red **■ Stop** button in IntelliJ (or **Ctrl + C** in the terminal).

---

## 🌱 Part 10: What will Spring Boot do for us?

Our tiny server works, but imagine building a **real** app this way: 😰

| Real app needs | Plain Java `HttpServer` | Spring Boot 🌱 |
|---|---|---|
| Many paths (`/students`, `/courses`, ...) | write each one by hand | `@GetMapping("/students")` — one line |
| Read parts of the URL (`/students/42`) | cut the String yourself | `@PathVariable Long id` |
| Turn objects into JSON | do it by hand (or add a library) | **automatic** ✨ |
| Read JSON from the client | by hand | `@RequestBody` |
| Errors (404, 400, 500) | by hand | automatic + customizable |
| Database | everything by hand | Spring Data JPA |
| Security, login | 😱 | Spring Security |
| Many requests at once, fast | basic | a professional server (Tomcat) built in |

Here's the **same** "hello" in Spring Boot (Chapter 52):

```java
@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello from Spring Boot! The time is " + LocalTime.now().withNano(0);
    }
}
```

That's it. Spring Boot does all the rest. 🪄 But now you **understand** what happens underneath: a server, at port 8080, waiting for requests to the path `/hello`, sending back a response with a status code. 🧠✨

---

## ✋ Try it yourself

**Task 1:** Take apart this URL. Write the scheme, host, port, path and query:
`http://localhost:8080/api/books?author=Dahl&sort=title`

<details>
<summary>Click to see the answer</summary>

- scheme: `http`
- host: `localhost`
- port: `8080`
- path: `/api/books`
- query: `author=Dahl&sort=title` (two parameters: `author` = `Dahl`, `sort` = `title`)

</details>

**Task 2:** Open the Developer Tools (F12) → **Network** tab, and visit a website you like. How many requests did it make? Find the first one (usually type **document**). What is its status?

**Task 3:** Run `TinyServer`. Add a **second** context: `/time` that returns only the current time. Visit both paths.

<details>
<summary>Click to see one possible answer</summary>

```java
server.createContext("/time", exchange -> {
    byte[] bytes = LocalTime.now().withNano(0).toString().getBytes(StandardCharsets.UTF_8);
    exchange.sendResponseHeaders(200, bytes.length);
    try (OutputStream body = exchange.getResponseBody()) {
        body.write(bytes);
    }
});
```

</details>

**Task 4:** Change `TinyServer` to use port **9090**. Which URL do you need now? What happens if you start **two** copies of the server on the same port?

<details>
<summary>Click to see the answer</summary>

`http://localhost:9090/hello`. The second copy crashes with `java.net.BindException: Address already in use` — only **one** program can listen at one door! 🚪 (You'll see this error with Spring Boot too, if you start your app twice — Chapter 51.)

</details>

**Task 5:** In your own words, explain the restaurant story to a friend: who is the client, who is the server, what is a request, what is a response?

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting the port

```
http://localhost/hello       ❌ goes to port 80 — nothing there
http://localhost:8080/hello  ✅
```

### Mistake 2: Wrong scheme

```
https://localhost:8080/hello   ❌ our development server doesn't use https
http://localhost:8080/hello    ✅
```

The browser may show "This site can't provide a secure connection".

### Mistake 3: "Address already in use"

```
java.net.BindException: Address already in use
```

Another program (maybe an **old copy** of your server!) is using the port. **Fix:** Stop the other program (IntelliJ: look for other running tabs in the Run window and click ■), or use another port.

### Mistake 4: "This site can't be reached" / "Connection refused"

Your server is **not running**. **Fix:** Start it first! ▶️

### Mistake 5: Trying to open your `localhost` from another device

Your phone can't open `http://localhost:8080` — on the phone, "localhost" means **the phone itself**! 📱 (Later you'll deploy your app to the internet — Chapter 100.)

---

## ✅ Summary

- A **client** asks (browser, app); a **server** answers (your Spring Boot app 🌱). The client always starts.
- **Request** = the question; **response** = the answer. 🍽️
- **Frontend** = what users see; **backend** = the "kitchen" on the server.
- **IP address** = a computer's number; **domain name** = its human name; **DNS** = the phone book that connects them. 📒
- A **port** is a door number 🚪. HTTP = 80, HTTPS = 443, **Spring Boot = 8080**.
- **localhost** (127.0.0.1) = this computer.
- **URL parts:** scheme `https` · host `shop.com` · port `:8080` · path `/products/42` · query `?color=red` · fragment `#top`.
- **F12 → Network** shows every request and response.
- A server is **just a program** that waits at a port and answers requests. Spring Boot makes writing one **easy**. 🚀

---

## ❓ Quiz

1. In the restaurant story, who is the client and who is the server?
2. Who always starts the conversation — the client or the server?
3. What does DNS do?
4. What is a port? What is Spring Boot's default port?
5. What does `localhost` mean?
6. In `http://localhost:8080/api/students?page=2`, what is the path? What is the query?
7. Which browser tool shows all requests and responses?
8. What happens if two programs try to use the same port?

<details>
<summary>Click to see the answers</summary>

1. The customer (you) is the client; the kitchen is the server.
2. The client.
3. It turns domain names (like `spring.io`) into IP addresses.
4. A door number on a computer, so requests reach the right program. Spring Boot uses 8080.
5. "This computer" (IP 127.0.0.1).
6. Path: `/api/students`. Query: `page=2`.
7. Developer Tools (F12) → Network tab.
8. The second one fails with "Address already in use".

</details>

---

[⬅ Previous chapter](../part-05-tools/42-git.md) | [Table of Contents](../README.md) | [Next chapter: HTTP ➡](44-http.md)
