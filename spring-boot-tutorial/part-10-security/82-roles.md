# Chapter 82 – Roles: admin and user

[⬅ Previous chapter](81-users-and-passwords.md) | [Table of Contents](../README.md) | [Next chapter ➡](83-jwt.md)

---

## 🎯 Goal

At the end of the last chapter, we found a big hole 🕳️: **every** user who registers can add, change and **delete** students! A student like Sara shouldn't be able to delete her classmates. 😱

Logging in answers **"Who are you?"**. Today we answer the second big question: **"What may you do?"** — with **roles**. 🎭

At the end of this chapter you will know:

- What **roles** and **authorities** are, and what `ROLE_` means 🏷️
- How to give different users different **powers**: `USER`, `TEACHER`, `ADMIN`
- How to write rules with **`hasRole`** and **`hasAnyRole`**
- How to make the **first admin** safely, with a password from **outside** the code 🔑
- How to build **admin-only** endpoints 👑
- How to protect **methods** with **`@PreAuthorize`** — and the sneaky **500** trap 🪤

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Role** | A **kind** of user, like "student", "teacher" or "principal". Each role has its own **powers**. 🎭 |
| **Authority** | Spring's word for **one** permission stamp a user has, like `ROLE_TEACHER`. 🏷️ |
| **Admin** | Short for **administrator**: the user with **all** the powers. The "principal" of the app. 👑 |
| **`hasRole("X")`** | A rule: "Only users with the role `X` may go in." |
| **`hasAnyRole("X", "Y")`** | A rule: "Users with role `X` **or** `Y` may go in." |
| **Method security** | Rules on **Java methods**, not only on URLs. 🔐 |
| **`@PreAuthorize`** | "**Before** running this method, check this rule." (*pre* = before) |
| **Least privilege** | Give every user **only** the powers they really need — nothing more. 🤏 |
| **Promote** | Give a user a **higher** role (for example, USER → TEACHER). ⬆️ |

---

## 📖 Story: The school's key ring 🔑

The school's caretaker has a big **key ring**, and gives out keys like this:

```
 🧒 Students:    🔑 classroom key                          → may READ the notice board
 👩‍🏫 Teachers:   🔑 classroom + 🔑 grade book              → may ADD and CHANGE things
 👑 Principal:   🗝️ MASTER key (opens everything)          → may also DELETE and manage people
```

Nobody gets the master key "just in case". A student who only needs the classroom gets **only** the classroom key. That's called **least privilege** 🤏: if a student's key is lost or stolen, the damage is **small**.

Our app works the same way. Every user gets **one role**, and each role opens **certain doors**:

| | 😶 Stranger | 🧒 `USER` (student) | 👩‍🏫 `TEACHER` | 👑 `ADMIN` |
|---|---|---|---|---|
| Read students, books, courses (`GET`) | ✅ | ✅ | ✅ | ✅ |
| Register, see "me", change own password | register only | ✅ | ✅ | ✅ |
| Search students by email | ❌ | ✅ | ✅ | ✅ |
| Add and change (`POST`, `PUT`, `PATCH`) | ❌ | ❌ | ✅ | ✅ |
| Delete (`DELETE`) | ❌ | ❌ | ❌ | ✅ |
| Manage users (`/api/admin/...`) | ❌ | ❌ | ❌ | ✅ |

This table is our **plan**. 📋 Writing it down **first** is the most important part of security!

---

## 🏷️ Part 1: Roles and authorities

You already met authorities in Chapter 81: `GET /api/auth/me` showed `"authorities":["ROLE_USER","FACTOR_PASSWORD"]`.

- An **authority** is a **stamp** 🏷️ on the user's card. It's just a text.
- A **role** is an authority whose name starts with **`ROLE_`**.

```
 Our database:            role = "TEACHER"
                                   │
 .roles("TEACHER")         ───────►│ adds "ROLE_" in front
 (in SchoolUserDetailsService)     ▼
 Spring's user card 🪪:   authorities = [ "ROLE_TEACHER", "FACTOR_PASSWORD" ]
                                   ▲
 .hasRole("TEACHER")       ───────►│ also adds "ROLE_" in front, then compares ✅
```

| You write | Spring looks for the authority |
|---|---|
| `.roles("TEACHER")` (when building the user) | creates `ROLE_TEACHER` |
| `.hasRole("TEACHER")` (in a rule) | `ROLE_TEACHER` |
| `.hasAuthority("ROLE_TEACHER")` (in a rule) | `ROLE_TEACHER` (exactly as written) |

⭐ So: with `roles` and `hasRole`, you **never** write `ROLE_` yourself — Spring adds it on **both** sides. They always fit together. 🧩

---

## 📜 Part 2: The rules

Let's turn our plan into rules. Change `authorizeHttpRequests` in **`SecurityConfig`**:

```java
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(HttpMethod.POST, "/api/auth/register").permitAll()
                .requestMatchers("/api/auth/**").authenticated()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.GET, "/api/students/search").authenticated()
                .requestMatchers(HttpMethod.GET, "/api/**").permitAll()
                .requestMatchers(HttpMethod.DELETE, "/api/**").hasRole("ADMIN")
                .requestMatchers("/api/**").hasAnyRole("TEACHER", "ADMIN")
                .requestMatchers("/h2-console/**").permitAll()
                .requestMatchers("/error").permitAll()
                .anyRequest().authenticated())
```

Line by line — remember, **top to bottom**, the **first** match wins:

| # | Rule | Meaning |
|---|---|---|
| 1 | `POST /api/auth/register` → `permitAll()` | Strangers may sign up. |
| 2 | `/api/auth/**` → `authenticated()` | Everything **else** about "me" (`GET /me`, `PUT /password`): any logged-in user, **any** role. This **replaces** the `/api/auth/me` rule from Chapter 81. |
| 3 | `/api/admin/**` → `hasRole("ADMIN")` | 👑 The admin area: **all** methods, only admins. |
| 4 | `GET /api/students/search` → `authenticated()` | Emails: logged-in users only (Chapter 80). |
| 5 | `GET /api/**` → `permitAll()` | 📋 Reading is free. |
| 6 | `DELETE /api/**` → `hasRole("ADMIN")` | 🗑️ Only admins delete. |
| 7 | `/api/**` → `hasAnyRole("TEACHER", "ADMIN")` | ✏️ Everything that's **left** under `/api` — `POST`, `PUT`, `PATCH` — for teachers **and** admins. |
| 8–10 | console, `/error`, `anyRequest()` | Like before. |

🤔 **Why is the order so important here?** Look at rule 2 and rule 7. Sara (a `USER`) changes her password with `PUT /api/auth/password`:

```
 PUT /api/auth/password  (Sara, USER)
   1. POST /api/auth/register?   ❌ no
   2. /api/auth/** ?             ✅ YES → authenticated → Sara is logged in → OK! 🎉
```

If rule 2 were **missing**, the request would fall down to rule 7 → `hasAnyRole("TEACHER", "ADMIN")` → Sara is only a `USER` → **403**! 😱 (We tried it — see "Try it yourself".) The same goes for rules 6 and 7: `DELETE` must come **before** the general `/api/**` rule.

Don't forget the import: `HttpMethod` is already there from Chapter 80. 👍

---

## 👑 Part 3: The first admin

Our rules need an **admin** — but who makes the **first** admin? 🐔🥚 Nobody can register as admin (Chapter 81: everyone who registers gets `"USER"`). So the app makes one itself, in the **`UserLoader`**.

But the admin's password must **not** be inside the code! ⚠️ Code is shared, saved in Git (Chapter 42), maybe even put on the internet. Remember **settings with defaults** (Chapter 55) and **secrets from outside** (Chapter 77)? Add this to **`application.properties`**:

```properties
# The first admin (set ADMIN_PASSWORD outside the code in real life!)
school.admin.password=${ADMIN_PASSWORD:admin12345}
```

| Code | Meaning |
|---|---|
| `school.admin.password=` | Our **own** setting (any name works; we start ours with `school.`). |
| `${ADMIN_PASSWORD:admin12345}` | "Use the **environment variable** `ADMIN_PASSWORD`. If there is none, use `admin12345`." The default is only for learning on your computer! |

Now the new **`UserLoader`**:

**`security/UserLoader.java`**

```java
package com.example.school.security;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import com.example.school.entity.AppUser;
import com.example.school.repository.AppUserRepository;

@Component
public class UserLoader implements CommandLineRunner {

    private final AppUserRepository appUserRepository;
    private final PasswordEncoder passwordEncoder;
    private final String adminPassword;

    public UserLoader(AppUserRepository appUserRepository, PasswordEncoder passwordEncoder,
                      @Value("${school.admin.password}") String adminPassword) {
        this.appUserRepository = appUserRepository;
        this.passwordEncoder = passwordEncoder;
        this.adminPassword = adminPassword;
    }

    @Override
    public void run(String... args) {
        addUserIfMissing("admin", adminPassword, "ADMIN");
        addUserIfMissing("teacher", "secret123", "TEACHER");
    }

    private void addUserIfMissing(String username, String password, String role) {
        if (!appUserRepository.existsByUsername(username)) {
            appUserRepository.save(new AppUser(username, passwordEncoder.encode(password), role));
            System.out.println("UserLoader: added the user " + username + " with the role " + role);
        }
    }
}
```

| Code | Meaning |
|---|---|
| `@Value("${school.admin.password}") String adminPassword` | Spring puts the value of our setting into this constructor parameter (Chapter 55). |
| `addUserIfMissing("admin", adminPassword, "ADMIN")` | Make the admin — but only if there's no `admin` yet. |
| `addUserIfMissing("teacher", "secret123", "TEACHER")` | A **new** database gets a teacher with the role `TEACHER`. |
| `private void addUserIfMissing(...)` | A small **helper method** (Chapter 15), so we don't write the same `if` twice. `private`: only this class uses it. |

Restart. The log:

```
UserLoader: added the user admin with the role ADMIN
```

🤔 Only the **admin** was added — why not the teacher? Because `teacher` **already exists** in your database (from Chapter 81)... with the role **`USER`**! So right now, our teacher **can't** add students:

```bash
curl -i -u teacher:secret123 -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Mia Clark","email":"mia@school.com","age":11}'
```

```
HTTP/1.1 403 
Content-Type: application/json

{"timestamp":"2026-10-11T06:48:12.681Z","status":403,"error":"Forbidden","path":"/api/students"}
```

**403 Forbidden!** 🚫 "I know you, teacher — but a `USER` may not do this." Perfect: that's exactly our plan. We'll **promote** the teacher in a minute — with an **admin endpoint**. 👑

### 🌍 Using the environment variable

To give the admin a **real** password, set `ADMIN_PASSWORD` **before** the app starts **for the first time** (the admin is only made once!). In IntelliJ: **Run → Edit Configurations... → Environment variables** → `ADMIN_PASSWORD=Very-Long-Secret-42` (Chapter 77 showed the same for `DB_PASSWORD`).

We tested it with a brand-new database: `admin` / `Very-Long-Secret-42` → **200**, and `admin` / `admin12345` → **401**. ✅

---

## 🛠️ Part 4: The admin endpoints

The admin needs two tools:

- 📋 `GET /api/admin/users` — see all users.
- ⬆️ `PUT /api/admin/users/{id}/role` — change a user's role.

**1. A DTO for the new role:**

**`dto/RoleRequest.java`**

```java
package com.example.school.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

public record RoleRequest(
        @NotBlank(message = "Role is required")
        @Pattern(regexp = "USER|TEACHER|ADMIN", message = "Role must be USER, TEACHER or ADMIN")
        String role) {
}
```

| Code | Meaning |
|---|---|
| `@Pattern(regexp = "USER\|TEACHER\|ADMIN", ...)` | The text must match this **pattern**. The `\|` means "**or**": only `USER`, `TEACHER` or `ADMIN` are allowed. Anything else → 400. |

**2. An exception** for a user id that doesn't exist:

**`exception/UserNotFoundException.java`**

```java
package com.example.school.exception;

public class UserNotFoundException extends RuntimeException {

    public UserNotFoundException(Long id) {
        super("User with id " + id + " was not found");
    }
}
```

**In `GlobalExceptionHandler`:**

```java
@ExceptionHandler(UserNotFoundException.class)
public ProblemDetail handleUserNotFound(UserNotFoundException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
    problem.setTitle("User not found");
    return problem;
}
```

**3. Two new methods in `UserService`:**

```java
@Transactional(readOnly = true)
public List<UserResponse> getAll() {
    return appUserRepository.findAll(Sort.by("id")).stream()
            .map(UserResponse::from)
            .toList();
}

@Transactional
public UserResponse changeRole(Long id, String role) {
    AppUser appUser = appUserRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    appUser.setRole(role);
    return UserResponse.from(appUser);
}
```

(Imports: `java.util.List`, `org.springframework.data.domain.Sort`, `com.example.school.exception.UserNotFoundException`.)

| Code | Meaning |
|---|---|
| `findAll(Sort.by("id"))` | All users, sorted by id (Chapter 78). |
| `.map(UserResponse::from)` | Every entity → a DTO **without** the password. 🔒 |
| `appUser.setRole(role);` | Change the role. Saved automatically at commit — dirty checking (Chapter 79). 🧹 |

**4. The controller:**

**`controller/AdminController.java`**

```java
package com.example.school.controller;

import java.util.List;

import jakarta.validation.Valid;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.school.dto.RoleRequest;
import com.example.school.dto.UserResponse;
import com.example.school.service.UserService;

@RestController
@RequestMapping("/api/admin/users")
public class AdminController {

    private final UserService userService;

    public AdminController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<UserResponse> getAll() {
        return userService.getAll();
    }

    @PutMapping("/{id}/role")
    public UserResponse changeRole(@PathVariable Long id, @Valid @RequestBody RoleRequest request) {
        return userService.changeRole(id, request.role());
    }
}
```

Notice: there's **no** security code in here! The rule `/api/admin/** → hasRole("ADMIN")` protects the **whole** controller. 🛡️

---

## 🧪 Part 5: Test the roles

Restart. Here are our real results.

**The admin looks at all users:**

```bash
curl -i -u admin:admin12345 http://localhost:8080/api/admin/users
```

```
HTTP/1.1 200 
Content-Type: application/json

[{"id":1,"username":"teacher","role":"USER"},{"id":2,"username":"sara","role":"USER"},{"id":3,"username":"admin","role":"ADMIN"}]
```

(Your ids may be different — for example, if you registered more users in Chapter 81. And if you see big jumps, like `33`: no problem! When the app is stopped hard, H2 sometimes skips some numbers.)

**The teacher tries the same:**

```bash
curl -i -u teacher:secret123 http://localhost:8080/api/admin/users
```

```
HTTP/1.1 403 
Content-Type: application/json

{"timestamp":"2026-10-11T06:48:12.366Z","status":403,"error":"Forbidden","path":"/api/admin/users"}
```

🚫 Not for teachers!

**The admin promotes the teacher** ⬆️ (use the teacher's id from the list):

```bash
curl -i -u admin:admin12345 -X PUT http://localhost:8080/api/admin/users/1/role \
  -H "Content-Type: application/json" \
  -d '{"role":"TEACHER"}'
```

```
HTTP/1.1 200 
Content-Type: application/json

{"id":1,"username":"teacher","role":"TEACHER"}
```

**Now the teacher can add a student** — right away, no restart:

```bash
curl -i -u teacher:secret123 -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Mia Clark","email":"mia@school.com","age":11}'
```

```
HTTP/1.1 201 
Location: /api/students/6
Content-Type: application/json

{"id":6,"name":"Mia Clark","email":"mia@school.com","age":11,"classroom":null}
```

🎉 Why "right away"? With HTTP Basic, the name and password come with **every** request — so Spring calls our `UserDetailsService` **every** time, and reads the **new** role from the database. (Remember this! In the next chapter, it'll be different. 😉)

And `GET /api/auth/me` as teacher now says `"authorities":["ROLE_TEACHER","FACTOR_PASSWORD"]`. ✅

**All our real results in one table:**

| Request | Who | Result |
|---|---|---|
| `GET /api/admin/users` | admin | **200** ✅ |
| `GET /api/admin/users` | teacher (USER) | **403** 🚫 |
| `POST /api/students` | teacher while still USER | **403** 🚫 |
| `PUT /api/admin/users/1/role` `{"role":"TEACHER"}` | admin | **200** ✅ |
| `PUT .../role` `{"role":"BOSS"}` | admin | **400** `"Role must be USER, TEACHER or ADMIN"` |
| `PUT /api/admin/users/99/role` | admin | **404** `"User with id 99 was not found"` |
| `POST /api/students` | teacher (now TEACHER) | **201** ✅ |
| `DELETE /api/students/1` | teacher | **403** 🚫 (only admins delete) |
| `POST /api/students` | sara (USER) | **403** 🚫 |
| `PUT /api/auth/password` | sara (USER) | **204** ✅ (rule 2!) |
| `DELETE /api/students/1` | stranger | **401** 🔒 |

Look at the difference between the last two kinds of "no":

- 😶 **Stranger** → **401**: "Who are you?"
- 🧒 **Sara** → **403**: "I know you, Sara — but no."

That's authentication vs authorization, live! 🎉

---

## 🔐 Part 6: Method security — a second lock

URL rules are great, but they're **far away** from the code they protect. 😟 What if someone adds a new URL one day — say, `/api/teachers/promote` — that also calls `userService.changeRole(...)`? Our `/api/admin/**` rule wouldn't cover it!

**Method security** puts a lock **right on the method**. 🔐 Two steps:

**1. Turn it on** — one annotation on `SecurityConfig`:

```java
@Configuration
@EnableMethodSecurity
public class SecurityConfig {
```

(Import `org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity`.)

**2. Lock the method** in `UserService`:

```java
@PreAuthorize("hasRole('ADMIN')")
@Transactional
public UserResponse changeRole(Long id, String role) {
```

(Import `org.springframework.security.access.prepost.PreAuthorize`.)

| Code | Meaning |
|---|---|
| `@EnableMethodSecurity` | "Spring, please look for security annotations on methods." |
| `@PreAuthorize("hasRole('ADMIN')")` | "**Before** this method runs, check: does the caller have the role `ADMIN`?" Inside the text, we use **single** quotes `'ADMIN'`, because the whole thing is already inside double quotes. |

How does it work? With a **proxy** 🎭 — exactly like `@Transactional` (Chapter 79)! The proxy checks the rule **before** calling your real method:

```
 Controller ──► 🎭 Proxy of UserService ──► your real changeRole(...)
                  │ "hasRole('ADMIN')?"
                  ├── yes ✅ → call the method
                  └── no  ❌ → throw AccessDeniedException 💥
```

Now we have **two** locks: the URL rule **and** the method rule. That's like a door with **two** locks — if one is forgotten, the other still holds. 🔒🔒

### 🪤 The 500 trap

Let's **test** the second lock. For the test, we **remove** the URL rule `.requestMatchers("/api/admin/**").hasRole("ADMIN")` for a moment. Now `PUT /api/admin/users/...` falls down to rule 7 (`TEACHER` or `ADMIN`) — so the teacher passes the URL check and reaches `changeRole`. Will `@PreAuthorize` stop him?

```bash
curl -i -u teacher:secret123 -X PUT http://localhost:8080/api/admin/users/2/role \
  -H "Content-Type: application/json" \
  -d '{"role":"ADMIN"}'
```

Our real answer:

```
HTTP/1.1 500 
Content-Type: application/problem+json

{"detail":"Something went wrong on our side. Please try again later.","instance":"/api/admin/users/2/role","status":500,"title":"Server error"}
```

And the log:

```
ERROR ... c.e.s.exception.GlobalExceptionHandler   : Unexpected error
org.springframework.security.authorization.AuthorizationDeniedException: Access Denied
```

😮 The lock **worked** (the role did **not** change) — but the answer is **500**, not 403! Why?

```
 💂 Filters (URL rules)  →  ✅ teacher may pass
 🎮 Controller           →  calls userService.changeRole(...)
 🎭 Proxy                →  ❌ throws AuthorizationDeniedException (a kind of AccessDeniedException)
 🧯 Our GlobalExceptionHandler: "An Exception? I'll catch it!"
                            → handleEverythingElse → 500 😵
```

The exception was thrown **inside** the controller — so our **catch-all** handler for `Exception` (Chapter 66) grabbed it before Spring Security could turn it into a 403.

**The fix:** a handler for `AccessDeniedException` in **`GlobalExceptionHandler`**:

```java
@ExceptionHandler(AccessDeniedException.class)
public ProblemDetail handleAccessDenied(AccessDeniedException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.FORBIDDEN,
            "You are not allowed to do this");
    problem.setTitle("Access denied");
    return problem;
}
```

(Import `org.springframework.security.access.AccessDeniedException`.)

| Code | Meaning |
|---|---|
| `@ExceptionHandler(AccessDeniedException.class)` | Catches `AccessDeniedException` **and its children**, like `AuthorizationDeniedException`. A **more specific** handler wins over the catch-all (Chapter 66). |
| `HttpStatus.FORBIDDEN` | **403**. |

Same test again — our real answer:

```
HTTP/1.1 403 
Content-Type: application/problem+json

{"detail":"You are not allowed to do this","instance":"/api/admin/users/2/role","status":403,"title":"Access denied"}
```

✅ **403**, with a nice ProblemDetail. Now **put the URL rule back**! Two locks are better than one. 🔒🔒

💡 You may notice that a 403 from a **URL rule** looks different (`{"timestamp":...,"status":403,"error":"Forbidden",...}`) from a 403 from **`@PreAuthorize`** (a ProblemDetail). That's because URL rules answer **before** our controller and our `GlobalExceptionHandler` are reached. Both are correct 403s. (Big apps sometimes make them look the same with their own "access denied handler" — we won't need that.)

---

## 💻 Mini project: The admin removes users 🗑️👤

Add **`DELETE /api/admin/users/{id}`**:

1. Only admins (the URL rule already covers `/api/admin/**` 👍).
2. Unknown id → **404** (`UserNotFoundException`).
3. ⚠️ An admin must **not** delete **their own** account (what if they're the **only** admin? Nobody could manage the app anymore! 😱) → **409** with the title `"Cannot delete yourself"`.
4. Success → **204**.

**Hint:** Give the service method the **name** of the logged-in user: `delete(Long id, String currentUsername)`.

<details>
<summary>Click to see the answer</summary>

**`exception/CannotDeleteYourselfException.java`**

```java
package com.example.school.exception;

public class CannotDeleteYourselfException extends RuntimeException {

    public CannotDeleteYourselfException() {
        super("You cannot delete your own account");
    }
}
```

**In `GlobalExceptionHandler`:**

```java
@ExceptionHandler(CannotDeleteYourselfException.class)
public ProblemDetail handleCannotDeleteYourself(CannotDeleteYourselfException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, ex.getMessage());
    problem.setTitle("Cannot delete yourself");
    return problem;
}
```

**In `UserService`:**

```java
@Transactional
public void delete(Long id, String currentUsername) {
    AppUser appUser = appUserRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    if (appUser.getUsername().equals(currentUsername)) {
        throw new CannotDeleteYourselfException();
    }
    appUserRepository.delete(appUser);
}
```

| Code | Meaning |
|---|---|
| `appUser.getUsername().equals(currentUsername)` | Is the user to delete the **same** person who's asking? Compare texts with `equals` (Chapter 9)! |

**In `AdminController`:**

```java
@DeleteMapping("/{id}")
@ResponseStatus(HttpStatus.NO_CONTENT)
public void delete(@PathVariable Long id, Authentication authentication) {
    userService.delete(id, authentication.getName());
}
```

(Imports: `org.springframework.http.HttpStatus`, `org.springframework.security.core.Authentication`, `org.springframework.web.bind.annotation.DeleteMapping`, `org.springframework.web.bind.annotation.ResponseStatus`.)

Our real tests (in a fresh database, `admin` has id 1 and `sara` id 3):

| Request | Who | Result |
|---|---|---|
| `DELETE /api/admin/users/3` (sara) | admin | **204** ✅ |
| `DELETE /api/admin/users/1` (admin) | admin | **409** `{"detail":"You cannot delete your own account",...,"title":"Cannot delete yourself"}` |
| `DELETE /api/admin/users/99` | admin | **404** `"User with id 99 was not found"` |
| `DELETE /api/admin/users/1` | teacher | **403** 🚫 |

</details>

---

## ✋ Try it yourself

1. Remove the rule `.requestMatchers("/api/auth/**").authenticated()`. Can Sara still change her password? Can she still call `GET /api/auth/me`? Why?
2. Move the `DELETE` rule **below** the `/api/**` → `hasAnyRole("TEACHER", "ADMIN")` rule. What can the teacher do now that they couldn't before?
3. Register a new user `omar` and make him a `TEACHER` with the admin endpoint. Check with `GET /api/auth/me`.
4. Your **Book API**: who may add a book? Who may delete one? Test `POST /api/books` as `sara` and as `teacher`.
5. Lock **reading** the average age to teachers and admins with `@PreAuthorize` on `StudentService.getAverageAge()`. What does a stranger get? What does `sara` get?

<details>
<summary>Click to see the answers</summary>

1. Our real results: `PUT /api/auth/password` as Sara → **403** (it falls down to `/api/**` → `TEACHER` or `ADMIN`). But `GET /api/auth/me` still works → **200**, because it now matches `GET /api/**` → `permitAll` (and Sara **is** logged in, so `authentication` isn't `null`). Put the rule back!
2. The teacher can now **delete** students: our real result was **204**. 😱 `DELETE /api/students/3` matched `/api/**` → `hasAnyRole("TEACHER", "ADMIN")` first. The `DELETE` rule below it is **never** reached.
3. `POST /api/auth/register` with `omar`, then `GET /api/admin/users` as admin to find his id, then `PUT /api/admin/users/{id}/role` with `{"role":"TEACHER"}`. Then `GET /api/auth/me` as omar → `"authorities":["ROLE_TEACHER","FACTOR_PASSWORD"]`.
4. The rules care about the **method** and the **path**, not about students or books: `POST /api/books` → `sara` gets **403**, `teacher` gets **201**. `DELETE /api/books/{id}` → only `admin`.
5. Add `@PreAuthorize("hasAnyRole('TEACHER', 'ADMIN')")` to the method. `sara` → **403** (`"title":"Access denied"`, from our new handler). A stranger → also **403**, not 401! The URL rule (`GET /api/**` → `permitAll`) let the stranger in as **anonymous**, and then `@PreAuthorize` said "no" — and our handler always answers 403. That's one reason why **URL rules** should do most of the work: they know the difference between 401 and 403.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Writing `ROLE_` in `hasRole`

```java
.requestMatchers("/api/admin/**").hasRole("ROLE_ADMIN")   // ❌
```

Spring **refuses to start**. Our real error:

```
Caused by: java.lang.IllegalArgumentException: ROLE_ADMIN should not start with ROLE_ since ROLE_ is automatically prepended when using hasAnyRole. Consider using hasAnyAuthority instead.
```

**Fix:** `hasRole("ADMIN")` — Spring adds `ROLE_` itself.

### Mistake 2: `hasAuthority("ADMIN")` without `ROLE_`

```java
.requestMatchers("/api/admin/**").hasAuthority("ADMIN")   // ❌ looks for "ADMIN", but the user has "ROLE_ADMIN"
```

No error at start — but **even the admin** gets **403**! (We tried: `admin` → `GET /api/admin/users` → **403**.) **Fix:** `hasRole("ADMIN")`, or `hasAuthority("ROLE_ADMIN")`.

### Mistake 3: A general rule above a specific one

`/api/**` → `hasAnyRole("TEACHER", "ADMIN")` **above** `DELETE /api/**` → teachers can delete (Try it 2). **No** error, **no** warning. **Fix:** Specific rules on top, and **test every role** — with a table like ours in Part 5!

### Mistake 4: Forgetting `@EnableMethodSecurity`

Without it, `@PreAuthorize` is **silently ignored**. 😱 We tested it (without the `/api/admin/**` URL rule): the teacher made **himself** an admin:

```
HTTP/1.1 200 
Content-Type: application/json

{"id":2,"username":"teacher","role":"ADMIN"}
```

**Fix:** `@EnableMethodSecurity` on `SecurityConfig`. And keep the URL rules too — two locks! 🔒🔒

### Mistake 5: `@PreAuthorize` gives 500

Your catch-all `@ExceptionHandler(Exception.class)` catches the `AccessDeniedException`. **Fix:** Add an `AccessDeniedException` handler → 403 (Part 6).

### Mistake 6: Letting users choose their role

```java
public record RegisterRequest(String username, String password, String role) { }   // ❌
```

Anyone could send `"role":"ADMIN"` and become the boss! 👑😈 **Fix:** Register **always** gives `"USER"`. Only an **admin** can give out higher roles.

---

## ✅ Summary

- A **role** 🎭 is a kind of user. Spring stores it as an **authority** 🏷️ with the prefix **`ROLE_`**: `.roles("TEACHER")` → `ROLE_TEACHER`.
- **Plan first**: a table of "who may do what". Give everyone the **least** power they need 🤏.
- URL rules: **`hasRole("ADMIN")`**, **`hasAnyRole("TEACHER", "ADMIN")`**. Never write `ROLE_` in them. Order: **specific first**.
- 401 = "who are you?" (stranger). 403 = "I know you, but no." (wrong role)
- The first admin is made by the app (`UserLoader`), with a password from **outside** the code: `${ADMIN_PASSWORD:...}`.
- **Method security**: `@EnableMethodSecurity` + **`@PreAuthorize("hasRole('ADMIN')")`** — a second lock 🔒🔒, done by a **proxy**.
- Handle **`AccessDeniedException`** → 403, or your catch-all turns it into a 500.

---

## ❓ Quiz

1. What's the difference between a role and an authority?
2. Our database says `role = "ADMIN"`. Which authority does Spring give the user?
3. What does `hasAnyRole("TEACHER", "ADMIN")` mean?
4. Sara (a `USER`) sends `DELETE /api/students/1`. A stranger sends the same. Which status codes do they get, and why are they different?
5. Why must the `DELETE` rule come before the `/api/**` → `hasAnyRole(...)` rule?
6. Why isn't the admin's password written in the Java code?
7. What does `@PreAuthorize` do, and what must you add so that it works?
8. Why did `@PreAuthorize` first give a 500 instead of a 403?

<details>
<summary>Click to see the answers</summary>

1. An authority is any permission stamp (a text). A role is an authority whose name starts with `ROLE_`.
2. `ROLE_ADMIN` (because our `UserDetailsService` uses `.roles(...)`, which adds `ROLE_`).
3. Users who have the role `TEACHER` **or** the role `ADMIN` may go in.
4. Sara gets **403** (logged in, but the wrong role). The stranger gets **401** (not logged in at all).
5. The first matching rule wins. If `/api/**` → `hasAnyRole("TEACHER", "ADMIN")` comes first, it also matches `DELETE` requests, and teachers could delete.
6. Code is shared and saved in Git. Secrets come from **outside**: an environment variable (`ADMIN_PASSWORD`), with a default only for learning.
7. It checks a rule **before** a method runs. You need `@EnableMethodSecurity` on a configuration class — without it, `@PreAuthorize` is silently ignored.
8. The `AccessDeniedException` was thrown inside the controller call, and our catch-all `@ExceptionHandler(Exception.class)` turned it into a 500. An extra handler for `AccessDeniedException` fixes it.

</details>

---

[⬅ Previous chapter](81-users-and-passwords.md) | [Table of Contents](../README.md) | [Next chapter: JWT tokens ➡](83-jwt.md)
