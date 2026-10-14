# Chapter 86 – Testing controllers

[⬅ Previous chapter](85-mockito.md) | [Table of Contents](../README.md) | [Next chapter ➡](87-testing-with-database.md)

---

## 🎯 Goal

In Chapter 85 we tested the **service** alone. But a lot can go wrong **before** the service is even called: 😟

- Is the **URL** right? Is it `GET` or `POST`?
- Does the JSON come **in** and go **out** correctly?
- Does **validation** say 400 for bad data?
- Do the **security rules** say 401 and 403 at the right times?

Today you'll test all that — **without** starting Tomcat and **without** a database. 🚀

At the end of this chapter you will know:

- What a **slice test** is, and what **`@WebMvcTest`** loads 🍰
- How to send **fake requests** with **`MockMvcTester`**
- How to replace the service with a mock bean: **`@MockitoBean`**
- How to check the **status**, the **headers** and the **JSON** of an answer
- How to test **security**: no token → 401, wrong role → 403, with **`jwt()`** 🎟️

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Slice test** | A test that starts **only one slice** of the app — for example, only the web part. 🍰 |
| **`@WebMvcTest`** | A slice test for **controllers**: it loads the web part of Spring, but **no** services, repositories or database. |
| **`MockMvcTester`** | A tool that sends **pretend** HTTP requests to your controllers — no real network, no Tomcat. |
| **`@MockitoBean`** | "Put a **Mockito mock** into Spring's container, in place of the real bean." |
| **Request post-processor** | A small helper that changes a pretend request before it's sent — for example, to add a **login**. |
| **`jwt()`** | A post-processor from Spring Security's test tools: "Pretend this request has a valid JWT." 🎟️ |
| **JSON path** | A short "address" inside JSON, like `$.name` (the `name` of the main object) or `$[0].name` (the name of the **first** item in a list). |

---

## 📖 Story: The cake slice 🍰

A big wedding cake has **four** layers: 🎂

```
 🍓 top:     the web layer       (controllers, JSON, security rules)
 🍫 middle:  the service layer   (business logic)
 🍰 bottom:  the repository layer (database)
 🍽️ plate:   the database itself
```

To check if the **strawberry** layer tastes right, you don't need to eat the **whole** cake! You cut **one slice** of the top layer and taste only that. 🍓

- **Unit test** (Chapter 85): one ingredient alone. 🥚
- **Slice test** (today): one **layer**. 🍓
- **Full test** (Chapter 87): the **whole** cake, plate and all. 🎂

| Kind of test | What starts | Speed | Finds |
|---|---|---|---|
| Unit test | one class (+ mocks) | ⚡ milliseconds | logic bugs |
| Slice test `@WebMvcTest` | web layer of Spring | 🚀 seconds | URL, JSON, validation, security bugs |
| Full test `@SpringBootTest` | everything + database | 🐢 many seconds | "Do all parts fit together?" |

---

## 📦 Part 1: One more test dependency

To pretend a user is logged in, we need **Spring Security's test tools**. Add to **`pom.xml`**, next to `spring-boot-starter-webmvc-test`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-test</artifactId>
    <scope>test</scope>
</dependency>
```

| Code | Meaning |
|---|---|
| `spring-boot-starter-security-test` | Helpers like `jwt()` for testing secured apps. |
| `<scope>test</scope>` | Only for tests — it won't be inside your finished app (Chapter 41). |

---

## 🍓 Part 2: The test class

Create **`src/test/java/com/example/school/controller/StudentControllerTest.java`**. We start with the "frame" and one test:

```java
package com.example.school.controller;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.assertj.MockMvcTester;

import com.example.school.config.JwtConfig;
import com.example.school.config.SecurityConfig;
import com.example.school.dto.StudentResponse;
import com.example.school.service.StudentService;

@WebMvcTest(StudentController.class)
@Import({SecurityConfig.class, JwtConfig.class})
class StudentControllerTest {

    @Autowired
    private MockMvcTester mvc;

    @MockitoBean
    private StudentService studentService;

    @MockitoBean
    private UserDetailsService userDetailsService;

    @Test
    void getByIdReturnsTheStudentAsJson() {
        when(studentService.getById(1L))
                .thenReturn(new StudentResponse(1L, "Sara Ahmed", "sara@school.com", 12, "5A"));

        assertThat(mvc.get().uri("/api/students/1"))
                .hasStatusOk()
                .bodyJson()
                .isLenientlyEqualTo("""
                        {"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12,"classroom":"5A"}
                        """);
    }
}
```

Lots of new things! Let's go slowly:

| Code | Meaning |
|---|---|
| `@WebMvcTest(StudentController.class)` | ⭐ "Start only the **web slice** of Spring, with **only** `StudentController`." Our `GlobalExceptionHandler` (a `@RestControllerAdvice`) is loaded too — it belongs to the web layer. Services, repositories, the database: **not** loaded. |
| `@Import({SecurityConfig.class, JwtConfig.class})` | ⭐ A slice test doesn't load **our** `@Configuration` classes by itself. We bring in our **security rules** and our **JWT beans** on purpose — we **want** to test the rules! |
| `@Autowired private MockMvcTester mvc;` | Spring gives us the request-sender. (In tests, we use **field** injection with `@Autowired` — it's the normal way there.) |
| `@MockitoBean private StudentService studentService;` | ⭐ The controller needs a `StudentService`, but services aren't loaded... so we put a **Mockito mock** into Spring in its place. Then we stub it with `when(...)` like in Chapter 85. |
| `@MockitoBean private UserDetailsService userDetailsService;` | Our `SecurityConfig` makes an `AuthenticationManager` that needs a `UserDetailsService`. The real one needs the database — so a mock it is. (We never call it in these tests.) |
| `mvc.get().uri("/api/students/1")` | Build a pretend **`GET /api/students/1`** request. |
| `assertThat(...)` | AssertJ again! It sends the request and lets us check the **answer**. |
| `.hasStatusOk()` | The status must be **200**. |
| `.bodyJson()` | "Now look at the body as JSON..." |
| `.isLenientlyEqualTo("""...""")` | "...it must have **these** fields and values." **Leniently** = the order of fields doesn't matter, and extra fields would be OK. |
| `"""` ... `"""` | A **text block**: text over many lines, and you don't need `\"` for quotes inside. Very handy for JSON! |

What really happens:

```
 Test ──► MockMvcTester ──► 💂 security filters (our real rules!)
                                   │
                                   ▼
                              StudentController (real)
                                   │ studentService.getById(1L)
                                   ▼
                              🎭 mock StudentService → "Sara!"
                                   │
          ◄── 200 + JSON ◄─────────┘   (Jackson really turned it into JSON)
```

The **controller**, the **JSON** conversion, the **security rules** and the **error handler** are all **real**. Only the service is fake. 🎯

---

## 🚨 Part 3: Testing errors

What if the service throws `StudentNotFoundException`? Our `GlobalExceptionHandler` should make a **404** with a ProblemDetail:

```java
@Test
void getByIdAnswers404WhenTheStudentDoesNotExist() {
    when(studentService.getById(99L)).thenThrow(new StudentNotFoundException(99L));

    assertThat(mvc.get().uri("/api/students/99"))
            .hasStatus(HttpStatus.NOT_FOUND)
            .bodyJson()
            .extractingPath("$.title").isEqualTo("Student not found");
}
```

(Imports: `org.springframework.http.HttpStatus`, `com.example.school.exception.StudentNotFoundException`.)

| Code | Meaning |
|---|---|
| `.thenThrow(new StudentNotFoundException(99L))` | Stubbing can also **throw**: "When asked for 99, explode!" 💥 |
| `.hasStatus(HttpStatus.NOT_FOUND)` | The status must be **404**. |
| `.extractingPath("$.title")` | ⭐ Take **one** value out of the JSON with a **JSON path**. `$` = the whole JSON, `.title` = its `title` field. |
| `.isEqualTo("Student not found")` | ...and check it. |

---

## 🔐 Part 4: Testing security — 401, 403 and `jwt()`

Now the interesting part: **who** may add a student? (Chapter 82: teachers and admins.)

```java
@Test
void createWithoutATokenAnswers401() {
    assertThat(mvc.post().uri("/api/students")
            .contentType(MediaType.APPLICATION_JSON)
            .content("""
                    {"name":"Omar Ali","email":"omar@school.com","age":12}
                    """))
            .hasStatus(HttpStatus.UNAUTHORIZED);
    verify(studentService, never()).create(any());
}
```

| Code | Meaning |
|---|---|
| `mvc.post().uri("/api/students")` | A pretend **POST**. |
| `.contentType(MediaType.APPLICATION_JSON)` | The header `Content-Type: application/json`. |
| `.content("""...""")` | The **body**. |
| `.hasStatus(HttpStatus.UNAUTHORIZED)` | **401** — no token! |
| `verify(studentService, never()).create(any())` | ⭐ And the service was **never** reached. The guard stopped it at the door. 💂 |

Now **with** a login. We need a pretend JWT. Spring Security's test tools have **`jwt()`**:

```java
private static RequestPostProcessor userWithRole(String role) {
    return jwt().authorities(new SimpleGrantedAuthority("ROLE_" + role));
}
```

(Imports: `import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.jwt;`, `org.springframework.security.core.authority.SimpleGrantedAuthority`, `org.springframework.test.web.servlet.request.RequestPostProcessor`.)

| Code | Meaning |
|---|---|
| `jwt()` | "Pretend this request carries a **valid** JWT." No secret key, no login endpoint needed — Spring just **believes** it. 🎟️ |
| `.authorities(new SimpleGrantedAuthority("ROLE_" + role))` | "...and the user has **this** authority." `userWithRole("TEACHER")` → `ROLE_TEACHER`. |
| `private static ... userWithRole(...)` | Our own small helper, so each test reads nicely. |

Now three more tests:

```java
@Test
void createAsTeacherAnswers201() {
    when(studentService.create(any(StudentRequest.class)))
            .thenReturn(new StudentResponse(4L, "Omar Ali", "omar@school.com", 12, null));

    assertThat(mvc.post().uri("/api/students")
            .with(userWithRole("TEACHER"))
            .contentType(MediaType.APPLICATION_JSON)
            .content("""
                    {"name":"Omar Ali","email":"omar@school.com","age":12}
                    """))
            .hasStatus(HttpStatus.CREATED)
            .hasHeader("Location", "/api/students/4")
            .bodyJson()
            .extractingPath("$.name").isEqualTo("Omar Ali");
}

@Test
void createAsUserAnswers403() {
    assertThat(mvc.post().uri("/api/students")
            .with(userWithRole("USER"))
            .contentType(MediaType.APPLICATION_JSON)
            .content("""
                    {"name":"Omar Ali","email":"omar@school.com","age":12}
                    """))
            .hasStatus(HttpStatus.FORBIDDEN);
}

@Test
void createWithInvalidDataAnswers400() {
    assertThat(mvc.post().uri("/api/students")
            .with(userWithRole("TEACHER"))
            .contentType(MediaType.APPLICATION_JSON)
            .content("""
                    {"name":"","email":"not-an-email","age":12}
                    """))
            .hasStatus(HttpStatus.BAD_REQUEST)
            .bodyJson()
            .extractingPath("$.errors")
            .isEqualTo(Map.of("name", "Name is required", "email", "Email must be a valid email address"));
    verify(studentService, never()).create(any());
}
```

(More imports: `java.util.Map`, `org.springframework.http.MediaType`, `com.example.school.dto.StudentRequest`, and the Mockito ones from Chapter 85: `any`, `never`, `verify`.)

| Code | Meaning |
|---|---|
| `.with(userWithRole("TEACHER"))` | ⭐ Add the pretend login to **this** request. |
| `.hasHeader("Location", "/api/students/4")` | Check a **header** of the answer (Chapter 62). |
| `userWithRole("USER")` → `.hasStatus(HttpStatus.FORBIDDEN)` | A student may **not** add students → **403**. Our Chapter 82 rule, tested! ✅ |
| `.extractingPath("$.errors").isEqualTo(Map.of(...))` | The `errors` part of our ProblemDetail (Chapter 66) must be exactly this **map**. |
| `verify(studentService, never()).create(any())` | Invalid data never reaches the service. Validation stopped it. 🛑 |

And two tests for `DELETE`:

```java
@Test
void deleteAsAdminAnswers204() {
    assertThat(mvc.delete().uri("/api/students/3").with(userWithRole("ADMIN")))
            .hasStatus(HttpStatus.NO_CONTENT);
    verify(studentService).delete(3L);
}

@Test
void deleteAsTeacherAnswers403() {
    assertThat(mvc.delete().uri("/api/students/3").with(userWithRole("TEACHER")))
            .hasStatus(HttpStatus.FORBIDDEN);
    verify(studentService, never()).delete(any());
}
```

---

## ▶️ Part 5: Run them

```bash
./mvnw test -Dtest=StudentControllerTest
```

Our real result:

```
[INFO] Running com.example.school.controller.StudentControllerTest
...
 :: Spring Boot ::                (v4.1.1)
...
c.e.s.controller.StudentControllerTest   : Started StudentControllerTest in 7.914 seconds (process running for 10.858)
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 11.51 s -- in com.example.school.controller.StudentControllerTest
```

🟢 **8 tests, all green!** You'll see the Spring Boot banner: a slice test **does** start Spring — but only a **small** part of it, so it's much faster than the whole app. And Spring starts **once** for all 8 tests. 🚀

Look at what we tested — **without** curl, **without** starting the app:

| Test | Checks |
|---|---|
| `getByIdReturnsTheStudentAsJson` | URL, 200, JSON output |
| `getByIdAnswers404WhenTheStudentDoesNotExist` | error handler → 404 ProblemDetail |
| `createWithoutATokenAnswers401` | security: strangers can't add |
| `createAsTeacherAnswers201` | teachers can add; 201 + `Location` |
| `createAsUserAnswers403` | security: students can't add |
| `createWithInvalidDataAnswers400` | validation → 400 with `errors` |
| `deleteAsAdminAnswers204` | admins can delete |
| `deleteAsTeacherAnswers403` | security: teachers can't delete |

That's most of the curl table from Chapter 82 — now checked **automatically**, every time you run `./mvnw test`. 🤖✅

### 💡 You'll also see `MockMvc`

Many examples on the internet use the **older** `MockMvc` with `perform(...)` and `andExpect(...)`:

```java
mockMvc.perform(get("/api/students/1"))
       .andExpect(status().isOk())
       .andExpect(jsonPath("$.name").value("Sara Ahmed"));
```

It does the same job. `MockMvcTester` is the **newer** way, and it uses AssertJ like the rest of our tests. If you meet `MockMvc` in another project, now you know what it is! 👍

---

## 💻 Mini project: Test the admin area 👑

Write **`AdminControllerTest`** for `GET /api/admin/users` (Chapter 82):

1. As **ADMIN** → **200**, and the **second** user in the list is `teacher`. (Stub `userService.getAll()` with two users.)
2. As **TEACHER** → **403**.
3. With **no** token → **401**.

**Hint:** `AdminController` needs a `UserService` → `@MockitoBean`. The JSON path to the second item's username is `$[1].username` (lists start at 0!).

<details>
<summary>Click to see the answer</summary>

**`src/test/java/com/example/school/controller/AdminControllerTest.java`**

```java
package com.example.school.controller;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.jwt;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.assertj.MockMvcTester;

import com.example.school.config.JwtConfig;
import com.example.school.config.SecurityConfig;
import com.example.school.dto.UserResponse;
import com.example.school.service.UserService;

@WebMvcTest(AdminController.class)
@Import({SecurityConfig.class, JwtConfig.class})
class AdminControllerTest {

    @Autowired
    private MockMvcTester mvc;

    @MockitoBean
    private UserService userService;

    @MockitoBean
    private UserDetailsService userDetailsService;

    @Test
    void adminSeesAllUsers() {
        when(userService.getAll()).thenReturn(List.of(
                new UserResponse(1L, "admin", "ADMIN"),
                new UserResponse(2L, "teacher", "TEACHER")));

        assertThat(mvc.get().uri("/api/admin/users")
                .with(jwt().authorities(new SimpleGrantedAuthority("ROLE_ADMIN"))))
                .hasStatusOk()
                .bodyJson()
                .extractingPath("$[1].username").isEqualTo("teacher");
    }

    @Test
    void teacherIsForbidden() {
        assertThat(mvc.get().uri("/api/admin/users")
                .with(jwt().authorities(new SimpleGrantedAuthority("ROLE_TEACHER"))))
                .hasStatus(HttpStatus.FORBIDDEN);
    }

    @Test
    void strangerMustLogIn() {
        assertThat(mvc.get().uri("/api/admin/users"))
                .hasStatus(HttpStatus.UNAUTHORIZED);
    }
}
```

| Code | Meaning |
|---|---|
| `@WebMvcTest(AdminController.class)` | This time, only the **admin** controller. |
| `$[1].username` | `$` = the list, `[1]` = the **second** item, `.username` = its field. |

Three tests, three green ticks: the admin rule from Chapter 82 is now **guarded by tests**. 🛡️

</details>

---

## ✋ Try it yourself

1. Write a test: `GET /api/students/1` with **no** token is still **200** (reading is free).
2. Write a test: `DELETE /api/students/3` as **ADMIN**, but the service throws `StudentNotFoundException(3L)` → **404**. (Hint: for `void` methods, stubbing looks different: `doThrow(new StudentNotFoundException(3L)).when(studentService).delete(3L);`)
3. Change the `DELETE` rule in `SecurityConfig` to `hasAnyRole("TEACHER", "ADMIN")` and run the tests. Which one turns red? Change it back.

<details>
<summary>Click to see the answers</summary>

1. ```java
   @Test
   void readingIsFreeForEveryone() {
       when(studentService.getById(1L))
               .thenReturn(new StudentResponse(1L, "Sara Ahmed", "sara@school.com", 12, "5A"));

       assertThat(mvc.get().uri("/api/students/1")).hasStatusOk();
   }
   ```
2. ```java
   @Test
   void deleteAnswers404WhenTheStudentDoesNotExist() {
       doThrow(new StudentNotFoundException(3L)).when(studentService).delete(3L);

       assertThat(mvc.delete().uri("/api/students/3").with(userWithRole("ADMIN")))
               .hasStatus(HttpStatus.NOT_FOUND);
   }
   ```
   (Import `static org.mockito.Mockito.doThrow`.) `when(...)` needs a method that **returns** something — for `void` methods, Mockito uses the "backwards" style `doThrow(...).when(mock).method(...)`.
3. `deleteAsTeacherAnswers403` fails: it expected 403, but the teacher got 204. That's exactly why we write security tests — a wrong rule is caught **before** it reaches real users. 🛡️

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `@Import` of your security configuration

Without it, the slice test doesn't use **your** rules — Spring Security falls back to its **default** settings (everything locked, Basic login, CSRF on). Your 401/403 tests then test the **wrong** rules! **Fix:** `@Import({SecurityConfig.class, JwtConfig.class})`.

### Mistake 2: A missing `@MockitoBean`

If the controller (or your configuration) needs a bean that the slice doesn't load, Spring **can't start** the test. You'll see an error like *"No qualifying bean of type 'com.example.school.service.StudentService' available"*. **Fix:** Add a `@MockitoBean` for every helper the web layer needs.

### Mistake 3: Using `@MockBean`

Older tutorials use `@MockBean`. It was **removed** in Spring Boot 4. **Fix:** Use **`@MockitoBean`** (package `org.springframework.test.context.bean.override.mockito`).

### Mistake 4: Forgetting the `Content-Type`

A POST without `.contentType(MediaType.APPLICATION_JSON)` can't be read as JSON → you get **415 Unsupported Media Type** instead of what you expected. **Fix:** Always set it for JSON bodies.

### Mistake 5: Testing logic in controller tests

Don't test "is the email already taken?" here — that's the **service's** job (Chapter 85). **Fix:** Controller tests check the **web** things: URLs, status codes, JSON, validation, security.

---

## ✅ Summary

- A **slice test** starts only one layer. **`@WebMvcTest(XController.class)`** loads the controller, JSON, validation and `@RestControllerAdvice` — no services, no database. 🍰
- **`@Import({SecurityConfig.class, JwtConfig.class})`** brings in your own security rules.
- **`@MockitoBean`** puts a mock into Spring in place of a real bean.
- **`MockMvcTester`**: `mvc.get().uri(...)`, `mvc.post()...contentType(...).content(...)`.
- Check the answer with AssertJ: `hasStatusOk()`, `hasStatus(...)`, `hasHeader(...)`, `bodyJson().isLenientlyEqualTo(...)`, `bodyJson().extractingPath("$.name").isEqualTo(...)`.
- **`jwt().authorities(...)`** pretends a logged-in user with roles. Test **401**, **403** and the happy path for every rule. 🔐

---

## ❓ Quiz

1. What does `@WebMvcTest(StudentController.class)` load, and what not?
2. Why do we need `@MockitoBean` for `StudentService`?
3. Why do we `@Import` our `SecurityConfig`?
4. What does `jwt().authorities(new SimpleGrantedAuthority("ROLE_TEACHER"))` do?
5. What does the JSON path `$.errors.name` point to?
6. In `createWithoutATokenAnswers401`, why do we also `verify(studentService, never()).create(any())`?
7. How do you make a mock `void` method throw an exception?

<details>
<summary>Click to see the answers</summary>

1. It loads the web layer: the controller, JSON conversion, validation, `@RestControllerAdvice` classes and Spring Security's filters. It doesn't load services, repositories, or the database.
2. The controller needs a `StudentService`, but services aren't part of the slice. `@MockitoBean` puts a mock in its place, which we can stub.
3. Without it, the slice uses Spring Security's default settings, not our own rules.
4. It makes the request look like it carries a valid JWT for a user with the role `TEACHER`.
5. The `name` field inside the `errors` object of the JSON answer.
6. To prove that the security filter stopped the request **before** it reached the service.
7. `doThrow(new SomeException()).when(mock).method(args);`

</details>

---

[⬅ Previous chapter](85-mockito.md) | [Table of Contents](../README.md) | [Next chapter: Testing with a database ➡](87-testing-with-database.md)
