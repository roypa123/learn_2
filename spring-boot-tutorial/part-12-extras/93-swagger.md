# Chapter 93 – API documentation with Swagger

[⬅ Previous chapter](92-file-upload.md) | [Table of Contents](../README.md) | [Next chapter ➡](94-actuator.md)

---

## 🎯 Goal

Imagine a friend wants to build a phone app 📱 for our school API. They ask: "Which URLs are there? What JSON do I send? What comes back? Do I need a token?" 🤔

You could write it all down by hand... and forget to update it every time the code changes. 😩 Today the app **documents itself** — with a web page where you can even **try** every endpoint! 🪄

At the end of this chapter you will know:

- What **OpenAPI** and **Swagger UI** are 📖
- How to add **springdoc** and get documentation **for free**
- How to make it nicer with **`@Tag`**, **`@Operation`** and **`@Schema`**
- How to make the **🔒 Authorize** button work with our **JWT** tokens
- How to open the documentation in our secured app

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **API documentation** | A description of an API: its URLs, what to send, what comes back. 📖 |
| **OpenAPI** | A **standard** way to describe a REST API, in JSON (or YAML). Computers **and** people can read it. |
| **Swagger UI** | A **web page** that shows an OpenAPI description nicely — with "Try it out" buttons. 🖱️ |
| **springdoc** | A library that **looks** at your Spring controllers and **writes** the OpenAPI description automatically. 🤖 |
| **Schema** | The description of a JSON object: which fields, which types, which rules. |

---

## 📖 Story: The restaurant menu 🍽️

When you go to a restaurant, you don't walk into the kitchen and ask the cook "What can you make?" 👨‍🍳 You read the **menu**:

```
 🍕 Pizza Margherita ............ €9
    tomato, mozzarella, basil
 🍝 Spaghetti ................... €11
    choose: tomato or cream sauce
 ⚠️ Contains gluten
```

The menu tells you **what** you can order, **what you must choose**, and **what you'll get**. 🎉

**API documentation** is the menu of your API. And **Swagger UI** is a **magic** menu 🪄: you can tap on a dish and it's **cooked right away**, so you can taste it.

Even better: with springdoc, the menu is **written by the kitchen itself** — every time the cook adds a new dish, it appears on the menu automatically. No more old menus! ✨

---

## 📦 Part 1: Add springdoc

Add to **`pom.xml`**:

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>3.0.0</version>
</dependency>
```

| Code | Meaning |
|---|---|
| `org.springdoc` | springdoc isn't made by the Spring team — so it's **not** in Spring Boot's list of versions, and we must write a **`<version>`** ourselves (Chapter 41). |
| `springdoc-openapi-starter-webmvc-ui` | Writes the OpenAPI description **and** shows Swagger UI. |
| `<version>3.0.0</version>` | springdoc **3.x** is for Spring Boot **4**. (Version 2.x was for Spring Boot 3.) Check **https://springdoc.org** for the newest 3.x version. |

### 🔓 Open the doors

Our security rules lock everything that isn't `GET /api/**`. Add these rules to **`SecurityConfig`**, near the other `permitAll` rules:

```java
                .requestMatchers("/swagger-ui/**", "/swagger-ui.html", "/v3/api-docs/**").permitAll()
```

| Path | What lives there |
|---|---|
| `/swagger-ui/**`, `/swagger-ui.html` | The Swagger UI web page (and its pictures and scripts). |
| `/v3/api-docs/**` | The OpenAPI description as JSON. |

---

## 🪄 Part 2: Documentation for free

Restart, and open **http://localhost:8080/swagger-ui/index.html** in your browser. 😮

```
 ┌──────────────────────────────────────────────────────────┐
 │ OpenAPI definition   v0                                   │
 │                                                           │
 │ ▼ student-controller                                      │
 │   GET    /api/students           getAll                   │
 │   POST   /api/students           create                   │
 │   GET    /api/students/{id}      getById                  │
 │   PUT    /api/students/{id}      replace                  │
 │   DELETE /api/students/{id}      delete                   │
 │   ...                                                     │
 │ ▼ auth-controller                                         │
 │   POST   /api/auth/login         login                    │
 │   POST   /api/auth/register      register                 │
 │   ...                                                     │
 │ ▼ Schemas                                                 │
 │   StudentRequest, StudentResponse, LoginRequest, ...      │
 └──────────────────────────────────────────────────────────┘
```

We wrote **zero** lines of documentation — and **every** endpoint is there! springdoc read our `@RestController`s, `@GetMapping`s, `@PathVariable`s, our records **and** our validation rules (`@NotBlank`, `@Size`, `@Min`...). 🤖

Click on **`GET /api/students/{id}`** → **Try it out** → type `1` → **Execute**:

```
 Curl:          curl -X 'GET' 'http://localhost:8080/api/students/1' -H 'accept: */*'
 Response code: 200
 Response body: {"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12,"classroom":"5A"}
```

🎉 A real request, from the browser — it even shows the matching **curl** command!

And the raw description? Open **http://localhost:8080/v3/api-docs** — a big JSON file. That's the **OpenAPI** description. Other tools can read it — for example, to **generate** code for a phone app automatically! 📱

---

## ✨ Part 3: Making it nicer

"student-controller" and "getAll" are OK, but we can do better. springdoc has annotations for that.

### 📘 About the whole API

**`config/OpenApiConfig.java`**

```java
package com.example.school.config;

import org.springframework.context.annotation.Configuration;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;

@Configuration
@OpenAPIDefinition(info = @Info(
        title = "School API",
        version = "1.0",
        description = "Students, classrooms, courses and books of our school 🏫"))
public class OpenApiConfig {
}
```

| Code | Meaning |
|---|---|
| `@OpenAPIDefinition(info = @Info(...))` | The title, version and description at the **top** of the page. |
| `io.swagger.v3.oas.annotations` | The annotations come from the **Swagger** project (that's where springdoc gets them). |

### 🏷️ About a controller and its methods

In **`StudentController`**:

```java
@RestController
@RequestMapping("/api/students")
@Tag(name = "Students", description = "Read, add, change and delete students")
public class StudentController {
    ...

    @Operation(summary = "Get one student by id",
               description = "Everyone may read students. Answers 404 if the student doesn't exist.")
    @GetMapping("/{id}")
    public StudentResponse getById(@PathVariable @Min(1) Long id) {
        return studentService.getById(id);
    }
```

(Imports: `io.swagger.v3.oas.annotations.Operation`, `io.swagger.v3.oas.annotations.tags.Tag`.)

| Code | Meaning |
|---|---|
| `@Tag(name = "Students", ...)` | ⭐ The **group** name on the page: "Students" instead of "student-controller". |
| `@Operation(summary = "...")` | ⭐ A short sentence next to the URL. |
| `description = "..."` | A longer text, shown when you open the endpoint. Great for rules like "who may do this?". |

### 🧾 About a DTO

In **`StudentRequest`**, add examples:

```java
public record StudentRequest(

        @Schema(example = "Omar Ali")
        @NotBlank(message = "Name is required")
        @Size(min = 2, max = 50, message = "Name must be 2 to 50 characters long")
        String name,

        @Schema(example = "omar@school.com")
        @NotBlank(message = "Email is required")
        @Email(message = "Email must be a valid email address")
        String email,

        @Schema(example = "12")
        @NotNull(message = "Age is required")
        @Min(value = 5, message = "Age must be at least 5")
        @Max(value = 20, message = "Age must be at most 20")
        Integer age) {
}
```

(Import `io.swagger.v3.oas.annotations.media.Schema`.)

| Code | Meaning |
|---|---|
| `@Schema(example = "Omar Ali")` | ⭐ When someone clicks **Try it out**, the body is pre-filled with **these** values instead of `"string"`. Much friendlier! |

Restart and reload — the page now says **"School API"**, groups are called **"Students"**, and the example body is ready to send. 🎉

---

## 🔒 Part 4: The Authorize button — using our JWT

Try **`POST /api/students`** in Swagger UI → **401**. Of course: no token! 🎟️ Let's teach Swagger UI about our **Bearer tokens**.

Change **`OpenApiConfig`**:

```java
@Configuration
@OpenAPIDefinition(
        info = @Info(
                title = "School API",
                version = "1.0",
                description = "Students, classrooms, courses and books of our school 🏫"),
        security = @SecurityRequirement(name = "bearerAuth"))
@SecurityScheme(
        name = "bearerAuth",
        type = SecuritySchemeType.HTTP,
        scheme = "bearer",
        bearerFormat = "JWT")
public class OpenApiConfig {
}
```

(Imports: `io.swagger.v3.oas.annotations.enums.SecuritySchemeType`, `io.swagger.v3.oas.annotations.security.SecurityRequirement`, `io.swagger.v3.oas.annotations.security.SecurityScheme`.)

| Code | Meaning |
|---|---|
| `@SecurityScheme(name = "bearerAuth", ...)` | ⭐ "Our API uses a login method called `bearerAuth`: an HTTP **Bearer** token, in **JWT** format." |
| `security = @SecurityRequirement(name = "bearerAuth")` | "Use it for **all** endpoints." (Endpoints that don't need it just ignore the token.) |

Restart. Now there's a green **🔒 Authorize** button at the top! Here's how to use it:

1. Open **`POST /api/auth/login`** → Try it out → `{"username":"teacher","password":"secret123"}` → Execute.
2. Copy the **token** from the answer (without the quotes).
3. Click **🔒 Authorize**, paste the token, click **Authorize**, then **Close**.
4. Now **`POST /api/students`** → Try it out → Execute → **201**! 🎉

Swagger UI adds `Authorization: Bearer <token>` to **every** request for you. 🎟️

---

## 🤔 Part 5: Should the documentation be public?

On your computer: yes, of course! On the **internet**: it depends. 🤔

| | Public docs 🌍 | Hidden docs 🙈 |
|---|---|---|
| Good for | APIs that **others** should use (a public weather API) | APIs only **your** apps use |
| Risk | Attackers see every endpoint at once | — |

Hiding docs is **not** real security (your endpoints are still protected by **Spring Security**!), but there's no need to show the menu to everyone. To switch the docs off, for example in the `prod` profile:

```properties
springdoc.api-docs.enabled=false
springdoc.swagger-ui.enabled=false
```

---

## 💻 Mini project: Document the auth endpoints 🔐

Make the **Auth** part of the page friendly:

1. `@Tag(name = "Login and users", description = "Register, log in, and manage your own account")` on `AuthController`.
2. An `@Operation` summary for `register`, `login` and `me`. For `login`, the description should say how to use the token.
3. Examples in `LoginRequest` (`teacher` / `secret123`) and `RegisterRequest` (`sara` / `sunflower7`).

<details>
<summary>Click to see the answer</summary>

**In `AuthController`:**

```java
@RestController
@RequestMapping("/api/auth")
@Tag(name = "Login and users", description = "Register, log in, and manage your own account")
public class AuthController {
    ...

    @Operation(summary = "Create a new account", description = "Everyone may register. New users get the role USER.")
    @PostMapping("/register")
    public ResponseEntity<UserResponse> register(@Valid @RequestBody RegisterRequest request) { ... }

    @Operation(summary = "Log in and get a token",
               description = "Send your name and password. Copy the token from the answer and paste it into the Authorize button.")
    @PostMapping("/login")
    public TokenResponse login(@Valid @RequestBody LoginRequest request) { ... }

    @Operation(summary = "Who am I?", description = "Shows your username and your authorities. Needs a token.")
    @GetMapping("/me")
    public CurrentUserResponse me(Authentication authentication) { ... }
```

**`LoginRequest`:**

```java
public record LoginRequest(
        @Schema(example = "teacher")
        @NotBlank(message = "Username is required")
        String username,

        @Schema(example = "secret123")
        @NotBlank(message = "Password is required")
        String password) {
}
```

**`RegisterRequest`:** the same idea with `@Schema(example = "sara")` and `@Schema(example = "sunflower7")`.

⚠️ `secret123` as an example is only OK because it's our **learning** password. Never put **real** passwords into documentation! 🔒

</details>

---

## ✋ Try it yourself

1. Open `/v3/api-docs` and search (Ctrl+F) for `"minLength"`. Where does it come from?
2. Hide one endpoint from the docs with `@Hidden` (from `io.swagger.v3.oas.annotations`). Which one would you hide?
3. Use Swagger UI to upload a photo (Chapter 92). Does it show a "Choose file" button?

<details>
<summary>Click to see the answers</summary>

1. From our validation rules! `@Size(min = 2, ...)` on `name` becomes `"minLength": 2` in the schema. springdoc reads Bean Validation annotations. 🤖
2. For example, an endpoint only meant for testing or for admins' tools. `@Hidden` on the method (or the whole controller) removes it from the docs — but it still **works**! (It's not security.)
3. Yes — because of `consumes = MediaType.MULTIPART_FORM_DATA_VALUE` and the `MultipartFile` parameter, springdoc knows it's a file upload and shows a file picker. 📁

</details>

---

## ⚠️ Common mistakes

### Mistake 1: The wrong springdoc version

springdoc 2.x with Spring Boot 4 → errors at start or a blank page. **Fix:** springdoc **3.x** for Spring Boot 4.

### Mistake 2: Swagger UI answers 401

The security rules lock the page. **Fix:** `permitAll()` for `/swagger-ui/**`, `/swagger-ui.html` and `/v3/api-docs/**`.

### Mistake 3: Every "Try it out" gives 401

You didn't click **🔒 Authorize** — or the token expired (1 hour, Chapter 83). **Fix:** Log in again, paste the new token.

### Mistake 4: Pasting `Bearer eyJ...`

Swagger UI adds the word `Bearer` **itself** → the header becomes `Bearer Bearer eyJ...` → 401. **Fix:** Paste **only** the token.

### Mistake 5: Thinking hidden docs = security

**Fix:** Endpoints are protected by Spring Security, **not** by hiding them.

---

## ✅ Summary

- **OpenAPI** = a standard description of a REST API. **Swagger UI** = a web page that shows it with **Try it out** 🪄.
- Add **`springdoc-openapi-starter-webmvc-ui`** (version **3.x** for Spring Boot 4) → docs at **`/swagger-ui/index.html`**, JSON at **`/v3/api-docs`**. Open them in `SecurityConfig`.
- Nicer docs: `@OpenAPIDefinition(info = @Info(...))`, **`@Tag`**, **`@Operation(summary = ...)`**, **`@Schema(example = ...)`**.
- JWT: **`@SecurityScheme(type = HTTP, scheme = "bearer", bearerFormat = "JWT")`** → the 🔒 **Authorize** button.
- Turn docs off where you don't want them: `springdoc.swagger-ui.enabled=false`.

---

## ❓ Quiz

1. What's the difference between OpenAPI and Swagger UI?
2. How does springdoc know about our endpoints without us writing documentation?
3. Why do we need a `<version>` for springdoc, but not for Spring's starters?
4. What does `@Schema(example = "Omar Ali")` change?
5. What does the `@SecurityScheme` annotation make possible?
6. Is hiding the docs a way to secure your API?

<details>
<summary>Click to see the answers</summary>

1. OpenAPI is the standard **description** (a JSON file). Swagger UI is the **web page** that shows it and lets you try the endpoints.
2. It looks at our controllers, mappings, parameters, records and validation annotations when the app starts.
3. springdoc isn't part of Spring Boot's managed versions, so Maven doesn't know which version to use.
4. The example value shown (and pre-filled in Try it out) for the `name` field.
5. The **Authorize** button: you paste a JWT once, and Swagger UI sends it with every request.
6. No. Hiding only removes the "menu"; real protection comes from Spring Security.

</details>

---

[⬅ Previous chapter](92-file-upload.md) | [Table of Contents](../README.md) | [Next chapter: Actuator ➡](94-actuator.md)
