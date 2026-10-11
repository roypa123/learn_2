# Chapter 80 – Spring Security: the introduction

[⬅ Previous chapter](../part-09-databases/79-transactions.md) | [Table of Contents](../README.md) | [Next chapter ➡](81-users-and-passwords.md)

---

## 🎯 Goal

Right now, **anybody** can delete your students. 😱 Just one line:

```bash
curl -X DELETE http://localhost:8080/api/students/1
```

...and Sara is gone. No password, no questions. Today you'll put a **guard** 💂 at the door of your app with **Spring Security**.

At the end of this chapter you will know:

- The two big questions: **"Who are you?"** and **"What may you do?"** 🤔
- What happens when you add Spring Security: **everything** gets locked 🔒
- What **401** and **403** mean
- How **HTTP Basic** sends a name and password (and why it needs HTTPS) 📨
- What **CSRF** is, and why a POST with the **right** password can still fail 🕵️
- How to write **your own rules**: "reading is free, changing needs a login" 📜
- How to keep the **H2 Console** working 🗄️

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Security** | Keeping your app and its data **safe** from people who shouldn't touch them. 🛡️ |
| **Authentication** | Checking **who you are**. "Show me your name and password." 🪪 |
| **Authorization** | Checking **what you may do**. "Are you allowed into this room?" 🚪 |
| **Credentials** | The things that prove who you are: usually a **username** and a **password**. 🔑 |
| **401 Unauthorized** | "I don't know who you are. Please log in." (The name is a bit wrong: it really means **un-authenticated**.) |
| **403 Forbidden** | "I know who you are — but you may **not** do this." ⛔ |
| **Filter** | A small check that runs **before** your controller. Like a guard at a door. 💂 |
| **Filter chain** | A **row** of filters. Every request walks past all of them, one by one. 💂💂💂 |
| **HTTP Basic** | A simple way to log in: the client sends the name and password in a **header** with **every** request. |
| **CSRF** | A trick where a bad website makes **your browser** send a request to another site. (Say "sea-surf".) 🏄 |
| **Stateless** | The server **doesn't remember** you between requests. Every request must show its credentials again. |

---

## 📖 Story: The school gate 🏫💂

Every school has a **gate**, and at the gate there's a **guard**. 💂

When you arrive, the guard asks **two** questions:

1. **"Who are you?"** You show your **student card** 🪪. The guard checks it's real. → That's **authentication**.
2. **"Where do you want to go?"** Students may go into the **classrooms**, but **not** into the **teachers' room** 🚫. → That's **authorization**.

The two can go wrong in **different** ways:

```
 😶 No card at all            → "Who are you? Go home and get your card!"   → 401
 🪪 Fake card                 → "This card is not real!"                     → 401
 🪪 Real student card,
    wants the teachers' room  → "I know you, Sara, but you may NOT go in."  → 403
 🪪 Real teacher card,
    wants the teachers' room  → "Welcome, Mr. Brown!" ✅                     → 200
```

And some places are **open to everyone**: the school's **notice board** 📋 at the gate. Anybody may **read** it — but only teachers may **pin** new notices on it.

That's exactly what we'll build today:

- 📋 **Reading** students (`GET`) → open to everyone.
- ✏️ **Changing** students (`POST`, `PUT`, `PATCH`, `DELETE`) → only with a login.

And **Spring Security** is our guard. 💂

---

## 🔐 Part 1: Authentication and authorization

These two long words are the **heart** of security. Let's make them easy:

| | Authentication 🪪 | Authorization 🚪 |
|---|---|---|
| The question | **Who are you?** | **What may you do?** |
| Example | "I'm Sara, and here's my password." | "Sara may read, but not delete." |
| Happens | **First** | **Second** (we must know you first!) |
| If it fails | **401** Unauthorized | **403** Forbidden |
| Short name | "auth**n**" | "auth**z**" |

💡 **Memory trick:** Authenti**c**ation = **c**ard 🪪 (who you are). Authori**z**ation = **z**one 🚪 (where you may go).

---

## 📦 Part 2: Add Spring Security — and everything is locked

We continue with our **`school`** project from Part 9. Open **`pom.xml`** and add **one** dependency, next to the others:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

| Code | Meaning |
|---|---|
| `spring-boot-starter-security` | The Spring Security **starter**: the guard, all the filters, and smart default settings. |

Reload Maven (the little 🔄 button in IntelliJ, Chapter 40) and **start** the app. We didn't change **any** Java code. Look at the log — there's a new **yellow** `WARN` message:

```
WARN 6196 --- [school] [           main] .s.a.UserDetailsServiceAutoConfiguration : 
Using generated security password: c0d7b4b8-e233-4fab-816b-76525672d515
This generated password is for development use only. Your security configuration must be updated before running your application in production.
```

| Log line | Meaning |
|---|---|
| `Using generated security password: c0d7b4b8-...` | Spring Boot made **one** user for you: name **`user`**, and this **random** password. 🎲 |
| `for development use only` | This is only for learning and testing. A real app needs real users (next chapter!). |

⚠️ Your password will be **different** — it's new **every** time the app starts!

### 🧪 Try it without a password

```bash
curl -i http://localhost:8080/api/students
```

Our real answer:

```
HTTP/1.1 401 
Set-Cookie: JSESSIONID=7C5F77FF72CBB02141EDC8556DE05B85; Path=/; HttpOnly
WWW-Authenticate: Basic realm="Realm", charset="UTF-8"
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Frame-Options: DENY
Content-Length: 0
```

😮 **401!** The list of students was open yesterday — now it's **locked**. And we didn't write any security code!

| Header | Meaning |
|---|---|
| `401` | "I don't know who you are." |
| `WWW-Authenticate: Basic ...` | "You can log in with **HTTP Basic**." (A hint for the client.) |
| `X-Frame-Options: DENY`, `Cache-Control: no-cache...` and friends | Extra **safety headers** Spring Security adds to **every** answer. For example: "Don't show my pages inside other websites" and "Don't save my answers in a cache." 🛡️ |

⭐ This is the **first big rule** of Spring Security:

> **When you add Spring Security, EVERYTHING is locked.** 🔒
> You must **open** things on purpose.

That's a good, safe default. It's much better to forget to **open** a door than to forget to **lock** it! 🚪

### 🧪 Try it with the password

`curl -u name:password` sends a name and password. Use **your** password from the log:

```bash
curl -i -u user:c0d7b4b8-e233-4fab-816b-76525672d515 http://localhost:8080/api/students/1
```

```
HTTP/1.1 200 
Content-Type: application/json

{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12,"classroom":"5A"}
```

🎉 **200!** The guard checked the name and password — and let us in.

And with a **wrong** password? `curl -i -u user:wrong ...` → **401** again. 🚫

### 🌐 Try it in the browser

Open **http://localhost:8080/api/students** in your browser. Spring **sends you** to a new page: **http://localhost:8080/login**:

```
 ┌───────────────────────────┐
 │      Please sign in       │
 │  ┌─────────────────────┐  │
 │  │ Username            │  │
 │  └─────────────────────┘  │
 │  ┌─────────────────────┐  │
 │  │ Password            │  │
 │  └─────────────────────┘  │
 │      [   Sign in   ]      │
 └───────────────────────────┘
```

We never made this page — Spring Security **made it for us**! 🪄 Type `user` and the password from the log → you see the students. ✅ To log out, open **http://localhost:8080/logout**.

🤔 Why did curl get a **401**, but the browser got a **login page**? Spring looks at **who** is asking:

| Who asks | How Spring knows | What Spring does |
|---|---|---|
| A **browser** 🌐 | It says `Accept: text/html` ("I want a web page") | **Redirects** (302) to the `/login` page |
| A **program** 🤖 (curl, Postman, an app) | It doesn't ask for HTML | Answers **401** |

---

## 📨 Part 3: How HTTP Basic sends your password

What did `curl -u` really send? Let's look with `-v` ("verbose": show everything):

```bash
curl -v -u teacher:secret123 http://localhost:8080/api/students/1
```

The part curl **sent** (lines starting with `>`):

```
> GET /api/students/1 HTTP/1.1
> Host: localhost:8080
> Authorization: Basic dGVhY2hlcjpzZWNyZXQxMjM=
> User-Agent: curl/8.21.0
> Accept: */*
```

There it is: an **`Authorization`** header. And that strange text `dGVhY2hlcjpzZWNyZXQxMjM=`?

It's just **`teacher:secret123`** written in **Base64** — a way to write any text with only "safe" letters. And Base64 is **NOT** a secret code! Anyone can turn it back:

```bash
echo dGVhY2hlcjpzZWNyZXQxMjM= | base64 -d
```

```
teacher:secret123
```

😱 **The password is readable by anyone who sees the request!**

```
 Base64 is like writing a letter in CAPITAL LETTERS. ✉️
 It looks different... but everyone can still read it!
```

### 🔒 So how is HTTP Basic safe?

Only with **HTTPS** 🔐 (the lock 🔒 in your browser's address bar). HTTPS **encrypts** the whole request — headers included — on its way through the internet. Nobody in between can read it.

| | Over `http://` | Over `https://` 🔐 |
|---|---|---|
| Can a spy on the Wi-Fi read the password? | **Yes!** 😱 | **No** ✅ |

On **your own computer** (`localhost`), `http://` is fine for learning — the request never leaves your computer. But a **real** app on the internet must **always** use HTTPS. (We'll come back to this in Chapter 100.)

💡 With HTTP Basic, the client sends the password with **every** request. That's simple — but not great. In Chapter 83, you'll learn **tokens** 🎟️, which are better.

---

## 💂 Part 4: The filter chain — a row of guards

How does Spring Security work? Remember the **DispatcherServlet** — Spring's "front desk" that sends each request to the right controller (Chapter 57)? Spring Security puts a **row of guards** **in front of** it:

```
                 ┌──────────────── Spring Security ────────────────┐
 Request 📨 ──►  │ 💂 filter → 💂 filter → 💂 filter → ... → 💂 filter │ ──► DispatcherServlet ──► Controller
                 └─────────────────────────────────────────────────┘
                     ⛔ any guard can stop the request
                        and answer 401 or 403 right away
```

This row is called the **filter chain**. Each filter has **one** small job. Want to see them? Add this line to `application.properties` (only while learning):

```properties
logging.level.org.springframework.security=DEBUG
```

At start, the log shows the whole row (our real log, with the default settings):

```
Will secure any request with filters: DisableEncodeUrlFilter, WebAsyncManagerIntegrationFilter, SecurityContextHolderFilter, HeaderWriterFilter, CsrfFilter, LogoutFilter, UsernamePasswordAuthenticationFilter, DefaultResourcesFilter, DefaultLoginPageGeneratingFilter, DefaultLogoutPageGeneratingFilter, BasicAuthenticationFilter, RequestCacheAwareFilter, SecurityContextHolderAwareRequestFilter, AnonymousAuthenticationFilter, ExceptionTranslationFilter, AuthorizationFilter
```

**16** guards! 😮 You don't need to know them all. Here are the important ones, in order:

| Filter | Its job |
|---|---|
| `HeaderWriterFilter` | Adds the **safety headers** (`X-Frame-Options` and friends). 🛡️ |
| `CsrfFilter` | Protects against **CSRF** (Part 5). 🏄 |
| `UsernamePasswordAuthenticationFilter` | Checks the name and password from the **login page** form. |
| `DefaultLoginPageGeneratingFilter` | **Makes** the `/login` page. 🪄 |
| `BasicAuthenticationFilter` | Reads the **`Authorization: Basic ...`** header and checks the name and password. 🪪 |
| `AnonymousAuthenticationFilter` | Nobody logged in? Then you're **"anonymous"** (a stranger). 😶 |
| `ExceptionTranslationFilter` | Turns security problems into **401** or **403** answers. |
| `AuthorizationFilter` | The **last** guard: "Is this person **allowed** to go to this URL?" 🚪 |

⭐ The big idea: the guards run **before** your controller. When a guard says **no**, your controller **never runs**. Your code doesn't need a single `if (password == ...)`! 🎉

---

## 🕵️ Part 5: The POST mystery — CSRF

Let's add a student, **with** the right password:

```bash
curl -i -u user:c0d7b4b8-e233-4fab-816b-76525672d515 -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Omar Ali","email":"omar@school.com","age":12}'
```

```
HTTP/1.1 401 
WWW-Authenticate: Basic realm="Realm", charset="UTF-8"
Content-Length: 0
```

😵 **401?!** The password is **correct** — the same one worked for `GET` a minute ago! What's going on?

Let's ask the DEBUG log (our real log for this request, shortened):

```
Securing POST /api/students
Invalid CSRF token found for http://localhost:8080/api/students
Responding with 403 status code
Securing GET /error
Set SecurityContextHolder to anonymous SecurityContext
...
```

🕵️ Now we can solve the mystery, step by step:

| Step | What happened |
|---|---|
| 1 | The **`CsrfFilter`** (guard number 5) said: "This POST has **no CSRF token**! ⛔ **403**." It stopped the request **before** `BasicAuthenticationFilter` even looked at the password. |
| 2 | For error answers, Spring Boot sends the request to its **error page**, `/error`. |
| 3 | But `/error` is locked too! 🔒 And on that new trip, **nobody** is logged in (anonymous)... |
| 4 | ...so the guard said **401**, and that's what we got. 🤯 |

Two lessons in one: CSRF protection blocks our POST, **and** `/error` should be open. Let's understand CSRF first.

### 🏄 What is CSRF?

**CSRF** = **C**ross-**S**ite **R**equest **F**orgery. "Forgery" means "a fake". Here's the trick:

```
 1. You log in to your bank website 🏦 in your browser. The browser remembers you (with a cookie 🍪).
 2. In another tab, you open a bad website 😈.
 3. The bad website has a hidden form that sends:  POST bank.com/send-money?to=badguy
 4. Your BROWSER sends it — and automatically adds your bank cookie! 🍪
 5. The bank thinks: "It's you!" → the money is gone. 😱
```

The fix: the real bank pages contain a **secret, random code**: the **CSRF token** 🎫. Every POST must send it back. The bad website **can't know** it → its fake POST is rejected. ✅ (Did you see the `_csrf` hidden field in the `/login` page? That's the token!)

### 🤔 Do we need CSRF protection?

CSRF attacks work because **browsers** add **cookies** automatically.

| Your app | Needs CSRF protection? |
|---|---|
| A **website** with forms, where the browser remembers the login with a **cookie** 🍪 | **Yes!** ✅ Keep it on. |
| A **REST API** where every client sends the credentials **itself**, in a header, every time | **No.** A bad website can't make your browser add an `Authorization` header. |

Our Student API is the **second** kind. So we'll turn CSRF protection **off** — and make sure our API **never** uses cookies (that's the **stateless** setting below). Both go together! 🤝

---

## 📜 Part 6: Our own rules — `SecurityConfig`

Time to tell the guard **our** rules:

- 📋 `GET` on `/api/...` → **everyone** (reading is free).
- 🚨 `/error` → **everyone** (so error answers work).
- ✏️ **everything else** → only **logged-in** users.

Create a new package **`config`** and in it, a new class **`SecurityConfig`**:

**`config/SecurityConfig.java`**

```java
package com.example.school.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(HttpMethod.GET, "/api/**").permitAll()
                .requestMatchers("/error").permitAll()
                .anyRequest().authenticated())
            .httpBasic(Customizer.withDefaults())
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
        return http.build();
    }
}
```

That looks like a lot! 😅 Let's go through it slowly:

| Code | Meaning |
|---|---|
| `@Configuration` | "This class holds **settings** — and makes beans with `@Bean` methods." (Chapter 54) |
| `@Bean public SecurityFilterChain securityFilterChain(...)` | We make our **own** filter chain bean. When Spring Boot sees it, it **stops** using its default one. |
| `HttpSecurity http` | A **builder** 🧱 that Spring gives us. We tell it what we want, step by step, and it builds the filter chain. |
| `.csrf(csrf -> csrf.disable())` | Turn **off** CSRF protection (fine for our stateless API — see Part 5). |
| `.authorizeHttpRequests(auth -> auth ...)` | Here come our **rules**: "who may go **where**". 🚪 |
| `.requestMatchers(HttpMethod.GET, "/api/**")` | Rule for: **GET** requests to any URL that starts with `/api/`. `**` means "**anything** after this, even with more `/`". |
| `.permitAll()` | "Let **everyone** in — even strangers." 🌍 |
| `.requestMatchers("/error").permitAll()` | The error page is open to all (all methods). |
| `.anyRequest().authenticated()` | "**Everything else**: only people who **logged in**." 🔒 |
| `.httpBasic(Customizer.withDefaults())` | "Allow login with **HTTP Basic** (the `Authorization: Basic ...` header), with the normal settings." |
| `.sessionManagement(...STATELESS)` | "**Never** make a session." The server doesn't remember anyone → no cookie → every request must log in again. Perfect for an API (and safe without CSRF). |
| `return http.build();` | Build the filter chain and give it to Spring. |

### 🧩 Those arrows again: `csrf -> csrf.disable()`

These are **lambdas** (Chapter 35)! Each method gets a small function that **sets up** one part:

```java
.csrf(csrf -> csrf.disable())
//    ▲          ▲
//    │          └── "...and here's what to do with it: disable it."
//    └── "Spring, give me the CSRF settings..."
```

`Customizer.withDefaults()` is just a ready-made lambda that means "change **nothing**, use the normal settings". 👍

### 📏 The rules are checked from top to bottom!

The guard reads the rules like a list, **from the top**, and uses the **first** one that matches:

```
 Request: GET /api/students
   1. GET /api/** ?          ✅ YES → permitAll → come in! (stop reading)

 Request: DELETE /api/students/1
   1. GET /api/** ?          ❌ no (it's DELETE)
   2. /error ?               ❌ no
   3. anyRequest ?           ✅ YES → authenticated → logged in? 🤔
```

⭐ So: **specific** rules at the **top**, `anyRequest()` always **last** (it matches everything!).

### 👤 A fixed user (for now)

The random password is annoying. 😩 Let's choose our own. Add to **`application.properties`**:

```properties
# One fixed user (only for learning!)
spring.security.user.name=teacher
spring.security.user.password=secret123
```

| Code | Meaning |
|---|---|
| `spring.security.user.name=teacher` | The name of Spring Boot's one user. |
| `spring.security.user.password=secret123` | Its password. Now the "generated password" message is **gone** from the log. |

⚠️ A password inside a file isn't safe for real apps. It's only for today — in the next chapter, users live in the **database**. 🗄️

---

## 🧪 Part 7: Test our rules

Restart the app. Here are our **real** results:

**1. Read without a login** 📋

```bash
curl -i http://localhost:8080/api/students/1
```

```
HTTP/1.1 200 
Content-Type: application/json

{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12,"classroom":"5A"}
```

✅ Reading is free again!

**2. Add a student without a login** ✏️

```bash
curl -i -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Omar Ali","email":"omar@school.com","age":12}'
```

```
HTTP/1.1 401 
WWW-Authenticate: Basic realm="Realm", charset="UTF-8"
Content-Type: application/json

{"timestamp":"2026-10-11T06:15:36.938Z","status":401,"error":"Unauthorized","path":"/api/students"}
```

✅ **Locked!** And look — now there's a **JSON body**, because `/error` is open. 👍

**3. Add a student with the login** 🪪

```bash
curl -i -u teacher:secret123 -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Omar Ali","email":"omar@school.com","age":12}'
```

```
HTTP/1.1 201 
Location: /api/students/4
Content-Type: application/json

{"id":4,"name":"Omar Ali","email":"omar@school.com","age":12,"classroom":null}
```

🎉 **201 Created!** The POST mystery is solved.

**4. Everything else still works** — for example, invalid data with the login:

```bash
curl -i -u teacher:secret123 -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"","email":"bad","age":12}'
```

```
HTTP/1.1 400 
Content-Type: application/problem+json

{"detail":"The request has 2 invalid field(s)","instance":"/api/students","status":400,"title":"Invalid data","errors":{"email":"Email must be a valid email address","name":"Name is required"}}
```

Our validation and error handling from Part 8 work **behind** the guard, just like before. ✅

| Request | Login? | Result |
|---|---|---|
| `GET /api/students/1` | no | **200** ✅ (open) |
| `POST /api/students` | no | **401** 🔒 |
| `POST /api/students` | wrong password | **401** 🔒 |
| `POST /api/students` | `teacher:secret123` | **201** ✅ |
| `DELETE /api/students/4` | `teacher:secret123` | **204** ✅ |

### 🍪 No more cookies

Look at the answers above: there's **no** `Set-Cookie: JSESSIONID=...` header anymore. Before our config, Spring made a **session** for strangers and sent a cookie (look at the very first 401 in Part 2). That's **`STATELESS`** at work: the server remembers **nobody**. 🧠❌

---

## 🗄️ Part 8: Opening the H2 Console again

Open **http://localhost:8080/h2-console** in your browser. 😟 A **pop-up** asks for a name and password! The console is locked too (it's not a `GET /api/...` URL). And even after logging in, the console doesn't show up — the browser shows an empty page or a "refused to connect" message. 🤔 Two problems:

| Problem | Why |
|---|---|
| 1. The console asks for a login | It's under `anyRequest().authenticated()`. |
| 2. The console doesn't show up | The H2 Console is made of **frames** (pages inside a page). The safety header **`X-Frame-Options: DENY`** says "never show my pages inside a frame" — so the browser refuses! 🖼️❌ |

The fix — two small changes in `SecurityConfig`:

```java
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(HttpMethod.GET, "/api/**").permitAll()
                .requestMatchers("/h2-console/**").permitAll()
                .requestMatchers("/error").permitAll()
                .anyRequest().authenticated())
            .httpBasic(Customizer.withDefaults())
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .headers(headers -> headers.frameOptions(frame -> frame.sameOrigin()));
```

| Code | Meaning |
|---|---|
| `.requestMatchers("/h2-console/**").permitAll()` | Open the console. (It has its **own** login page, with the database password.) |
| `.headers(headers -> headers.frameOptions(frame -> frame.sameOrigin()))` | Change the header to **`X-Frame-Options: SAMEORIGIN`**: "Frames are OK — but only from **my own** website." |

Restart → the console works again. ✅ We checked: the console logs in, and `SELECT COUNT(*) FROM STUDENTS` answers `3`.

⚠️ The H2 Console is a **learning tool**. In a real app on the internet, it must be **turned off** (`spring.h2.console.enabled=false`, or simply use a real database like in Chapter 77).

---

## 💻 Mini project: Protect the emails 📧🔒

Students' email addresses are **private**. 🙈 But right now, **anyone** can find a student by email:

```bash
curl "http://localhost:8080/api/students/search?email=sara@school.com"
```

**Your task:** Make **`GET /api/students/search`** need a login — while **all other** `GET` requests stay open.

1. Add **one** rule to `SecurityConfig`. Think carefully about **where** it goes! 📏
2. Test it **without** a login → should be **401**.
3. Test it **with** `teacher:secret123` → should be **200**.
4. Check that `GET /api/students/1` is **still** open.

<details>
<summary>Click to see the answer</summary>

The new rule must come **before** `GET /api/**` — otherwise the guard stops reading at the open rule and never sees ours!

```java
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(HttpMethod.GET, "/api/students/search").authenticated()
                .requestMatchers(HttpMethod.GET, "/api/**").permitAll()
                .requestMatchers("/h2-console/**").permitAll()
                .requestMatchers("/error").permitAll()
                .anyRequest().authenticated())
```

| Code | Meaning |
|---|---|
| `.requestMatchers(HttpMethod.GET, "/api/students/search").authenticated()` | **Specific** rule: searching by email needs a login. It's at the **top**, so it wins. 🥇 |

Our real tests:

```bash
curl -i "http://localhost:8080/api/students/search?email=sara@school.com"
```

```
HTTP/1.1 401 
WWW-Authenticate: Basic realm="Realm", charset="UTF-8"
Content-Type: application/json

{"timestamp":"2026-10-11T06:19:27.475Z","status":401,"error":"Unauthorized","path":"/api/students/search"}
```

```bash
curl -i -u teacher:secret123 "http://localhost:8080/api/students/search?email=sara@school.com"
```

```
HTTP/1.1 200 
Content-Type: application/json

{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12,"classroom":"5A"}
```

And `GET /api/students/1` without a login → still **200**. ✅

💡 Notice: the `?email=...` part is **not** part of the path. `requestMatchers` only looks at the **path**: `/api/students/search`.

🤔 **What if you put the rule after `GET /api/**`?** Then `GET /api/**` matches first → `permitAll` → the emails are open again. 😱 No error, no warning — the order **silently** decides.

</details>

---

## ✋ Try it yourself

1. Add Spring Security **without** a `SecurityConfig` (comment out `@Configuration`). Open `/api/students` in your browser and log in on the `/login` page with `teacher` / `secret123`. Then visit `/logout`.
2. Use `curl -v -u teacher:secret123 ...` and find the `Authorization` header. Decode it with `base64 -d`.
3. Your **Book API** (from the mini projects): which of its endpoints are open now, and which are locked? Test `GET /api/books/1` and `POST /api/books` without a login.
4. Make **everything** under `/api/classrooms/**` (also `GET`!) need a login. Where does the rule go?
5. Remove `.requestMatchers("/error").permitAll()`, and send a POST without a login. What's different about the 401 answer?

<details>
<summary>Click to see the answers</summary>

1. The browser is sent to `/login`. After signing in, you see the students. `/logout` shows a page "Are you sure you want to log out?" with a **Log Out** button. (Without our `SecurityConfig`, Spring Boot's default filter chain comes back — with the login page and CSRF protection.)
2. `Authorization: Basic dGVhY2hlcjpzZWNyZXQxMjM=` → `teacher:secret123`.
3. Our real results: `GET /api/books/1` → **200** (it matches `GET /api/**`). `POST /api/books` → **401**. The rules don't care if it's a student or a book — only the **method** and the **path** matter.
4. At the **top** (or at least before `GET /api/**`): `.requestMatchers("/api/classrooms/**").authenticated()`. Without a method, the rule works for **all** methods.
5. It's still **401**, but the body is **empty** (`Content-Length: 0`). With `/error` open, you get the JSON body with `"status":401`.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: `anyRequest()` before the other rules

```java
.authorizeHttpRequests(auth -> auth
    .anyRequest().authenticated()                            // ❌ first!
    .requestMatchers(HttpMethod.GET, "/api/**").permitAll()
    .requestMatchers("/error").permitAll())
```

Spring **refuses to start** 💥. Our real error:

```
Caused by: java.lang.IllegalStateException: Can't configure requestMatchers after anyRequest
```

**Fix:** `anyRequest()` is always the **last** rule. (Good thing Spring checks it — the rules after it could never match!)

### Mistake 2: A specific rule after a general one

`GET /api/students/search` **after** `GET /api/**` → the search is open. No error at all! 🙈 **Fix:** Specific rules at the **top**. Always **test** your rules with and without a login.

### Mistake 3: POST gives 401 or 403 with the right password

That's **CSRF protection**. When we left `.csrf(csrf -> csrf.disable())` out of our config, our real answer to a POST with `teacher:secret123` was:

```
HTTP/1.1 403 
Content-Type: application/json

{"timestamp":"2026-10-11T06:18:08.852Z","status":403,"error":"Forbidden","path":"/api/students"}
```

(**403** here, because `/error` was open. With the default settings, `/error` is locked, so it was a confusing **401** — see Part 5.) **Fix:** For a **stateless REST API**, disable CSRF. For a **website with a login form and cookies**, keep it on!

### Mistake 4: Forgetting `/error`

Error answers become an empty **401**, even for things like a 403. **Fix:** `.requestMatchers("/error").permitAll()`.

### Mistake 5: The H2 Console asks for a password or doesn't show up

**Fix:** `permitAll()` for `/h2-console/**` **and** `frameOptions(frame -> frame.sameOrigin())` (Part 8).

### Mistake 6: Sending passwords over `http://` on the internet

Base64 is **not** encryption. **Fix:** Real apps **always** use **HTTPS**. 🔐

---

## ✅ Summary

- **Authentication** 🪪 = **who** are you? Fails with **401**. **Authorization** 🚪 = **what** may you do? Fails with **403**.
- Add **`spring-boot-starter-security`** → **everything** is locked 🔒, with one user `user` and a random password in the log.
- Spring Security is a **filter chain** 💂💂💂 in **front** of your controllers. If a guard says no, your controller never runs.
- **HTTP Basic**: `Authorization: Basic <Base64 of name:password>`. Base64 is **not** secret → use **HTTPS**.
- **CSRF** 🏄 protects **cookie-based** websites. A **stateless** REST API can disable it.
- Your own **`SecurityFilterChain`** bean: `csrf`, `authorizeHttpRequests` (rules from **top to bottom**, `anyRequest()` last), `httpBasic`, `STATELESS`.
- `permitAll()` = everyone. `authenticated()` = logged-in users only.
- Open `/error`, and set up the H2 Console with `permitAll` + `sameOrigin`.

---

## ❓ Quiz

1. What's the difference between authentication and authorization?
2. What's the difference between 401 and 403?
3. You add `spring-boot-starter-security` and change nothing else. Can strangers still read `GET /api/students`?
4. Why isn't `Authorization: Basic dGVhY2hlcjpzZWNyZXQxMjM=` safe over plain `http://`?
5. What does the filter chain do, and when does your controller run?
6. Why can a stateless REST API turn off CSRF protection?
7. In which order are the rules in `authorizeHttpRequests` checked?
8. What does `STATELESS` mean?

<details>
<summary>Click to see the answers</summary>

1. Authentication checks **who** you are (name + password). Authorization checks **what** you may do (which URLs, which actions).
2. 401: "I don't know who you are" (no login or a wrong login). 403: "I know who you are, but you may not do this."
3. No. Everything is locked by default → 401 (or the login page in a browser).
4. Because Base64 is not encryption — anyone who sees the request can decode it to `teacher:secret123`. Only HTTPS hides it.
5. It's a row of filters that check every request **before** it reaches the DispatcherServlet. Your controller runs only if **all** filters let the request pass.
6. CSRF works because browsers add **cookies** automatically. A stateless API uses no cookies — every client sends its credentials in a header itself, which a bad website can't add.
7. From **top to bottom**. The **first** rule that matches decides. `anyRequest()` must be last.
8. The server doesn't remember anyone between requests (no session, no cookie). Every request must bring its own credentials.

</details>

---

[⬅ Previous chapter](../part-09-databases/79-transactions.md) | [Table of Contents](../README.md) | [Next chapter: Users and passwords ➡](81-users-and-passwords.md)
