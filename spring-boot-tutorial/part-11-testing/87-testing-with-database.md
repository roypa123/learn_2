# Chapter 87 – Testing with a database

[⬅ Previous chapter](86-testing-controllers.md) | [Table of Contents](../README.md) | [Next chapter ➡](../part-12-extras/88-logging.md)

---

## 🎯 Goal

Our mock tests are fast — but they **trust** the repository blindly. 🙈 What if a query method has a typo? What if our native SQL is wrong? A mock would never notice!

Today we test with a **real** database — a fresh, empty one, made only for the tests, and thrown away afterwards. 🗄️🧪

At the end of this chapter you will know:

- How to test **repositories** with **`@DataJpaTest`** 🗄️
- Why every test gets a **clean** database (rollback!) 🧼
- How to keep tests **away** from your real data: a **test profile** 🧪
- How to test the **whole app** at once with **`@SpringBootTest`**: register → login → token → add a student 🎂
- How to choose between unit, slice and full tests 🔺

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **`@DataJpaTest`** | A slice test for the **database layer**: entities, repositories, and a database — nothing else. 🗄️ |
| **In-memory database** | A database that lives only in the computer's memory. When the test ends, it's **gone**. 💨 |
| **Rollback** | Undo all changes (Chapter 79). Each `@DataJpaTest` test is rolled back at the end. ↩️ |
| **Integration test** | A test that checks that **many** parts work **together**. 🧩🧩🧩 |
| **`@SpringBootTest`** | Start the **whole** app for a test. 🎂 |
| **Test profile** | A **profile** (Chapter 56) with settings only for tests — like a separate test database. |
| **Test pyramid** | A rule of thumb: **many** small fast tests, **fewer** big slow ones. 🔺 |

---

## 📖 Story: The driving test 🚗

Before you get a driver's license, there are **two** kinds of tests:

1. 📝 A **written** test: "What does a red light mean?" Fast, easy, you can do 50 questions in 20 minutes.
2. 🚗 A **driving** test: a real car, a real road, a real examiner. Slow, and only **one** per person — but it shows that everything works **together**: eyes, hands, feet, rules.

Nobody would get a license with **only** the written test. And nobody would do **50** driving tests! 😅

Our tests work the same way:

| | 📝 Written test | 🚗 Driving test |
|---|---|---|
| Our tests | unit tests (Ch. 84–85), slice tests (Ch. 86 + today's `@DataJpaTest`) | `@SpringBootTest` (today) |
| Speed | fast ⚡ | slow 🐢 |
| How many | **many** | **a few** |
| Shows | each part is right | the parts fit **together** |

---

## 📦 Part 1: The test dependency

Add the JPA test tools to **`pom.xml`**:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa-test</artifactId>
    <scope>test</scope>
</dependency>
```

| Code | Meaning |
|---|---|
| `spring-boot-starter-data-jpa-test` | Brings `@DataJpaTest` and its helpers. (In Spring Boot 4, every starter has its own `-test` partner, like `spring-boot-starter-webmvc-test` and `spring-boot-starter-security-test`.) |

---

## 🗄️ Part 2: Testing the `StudentRepository`

Create **`src/test/java/com/example/school/repository/StudentRepositoryTest.java`**:

```java
package com.example.school.repository;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;

import com.example.school.entity.Student;

@DataJpaTest
class StudentRepositoryTest {

    @Autowired
    private StudentRepository studentRepository;

    @BeforeEach
    void addStudents() {
        studentRepository.save(new Student("Sara Ahmed", "sara@school.com", 12));
        studentRepository.save(new Student("Tom Brown", "tom@school.com", 13));
        studentRepository.save(new Student("Lina Haddad", "lina@greenschool.org", 11));
    }

    @Test
    void findByEmailIgnoresBigAndSmallLetters() {
        assertThat(studentRepository.findByEmailIgnoreCase("SARA@School.com"))
                .isPresent()
                .get()
                .extracting(Student::getName)
                .isEqualTo("Sara Ahmed");
    }

    @Test
    void findByEmailFindsNothingForAnUnknownEmail() {
        assertThat(studentRepository.findByEmailIgnoreCase("nobody@school.com")).isEmpty();
    }

    @Test
    void findByAgeGreaterThanEqualIncludesTheBorder() {
        List<Student> students = studentRepository.findByAgeGreaterThanEqual(12);

        assertThat(students).extracting(Student::getName)
                .containsExactlyInAnyOrder("Sara Ahmed", "Tom Brown");
    }

    @Test
    void averageAgeIsCalculatedByTheDatabase() {
        assertThat(studentRepository.averageAge()).isEqualTo(12.0);
    }

    @Test
    void findByEmailDomainUsesOurNativeQuery() {
        List<Student> students = studentRepository.findByEmailDomain("school.com");

        assertThat(students).extracting(Student::getName)
                .containsExactlyInAnyOrder("Sara Ahmed", "Tom Brown");
    }

    @Test
    void theDatabaseStartsCleanForEveryTest() {
        assertThat(studentRepository.count()).isEqualTo(3);
    }
}
```

| Code | Meaning |
|---|---|
| `@DataJpaTest` | ⭐ Start only the **database slice**: our entities, our repositories, Hibernate — and a **brand-new in-memory H2** database instead of our file database. No controllers, no services, no security, no `DataLoader`. |
| `@Autowired private StudentRepository studentRepository;` | The **real** repository — not a mock! |
| `@BeforeEach void addStudents()` | Before **each** test: put three students into the empty database. |
| `.isPresent().get().extracting(Student::getName).isEqualTo(...)` | AssertJ for `Optional`: "There **is** something inside; take it; take its name; it must be Sara." |
| `.containsExactlyInAnyOrder(...)` | "Exactly these names — the **order** doesn't matter." (The database doesn't promise an order without `ORDER BY`.) |
| `findByAgeGreaterThanEqual(12)` | A **border** test again (Chapter 84): Sara is **exactly** 12 — she must be included. |
| `averageAge()` | Our `@Query` with `AVG` (Chapter 74): (12 + 13 + 11) / 3 = **12.0**. |
| `findByEmailDomain("school.com")` | Our **native SQL** query (Chapter 74). Lina is at `greenschool.org` → not included. If we had a typo in the SQL, **this** test would catch it — a mock never could! 🎯 |
| `theDatabaseStartsCleanForEveryTest` | Always **3**, never 6 or 9 — see below! 🧼 |

### 🧼 Why is the database clean for every test?

Each `@DataJpaTest` test runs inside a **transaction** — and at the end, Spring does a **rollback** ↩️ (Chapter 79):

```
 Test 1:  BEGIN → add 3 students → test → ROLLBACK ↩️   (the 3 students are gone)
 Test 2:  BEGIN → add 3 students → test → ROLLBACK ↩️   (gone again)
 ...
```

So every test starts with an **empty** database, and the `@BeforeEach` fills it with exactly 3 students. No test can disturb another one. 🎉

Run it:

```bash
./mvnw test -Dtest=StudentRepositoryTest
```

In the log, look for the database: it's an **in-memory** H2 with a random name like `jdbc:h2:mem:...` — **not** your `./data/school` file. And the result should be:

```
[INFO] Tests run: 6, Failures: 0, Errors: 0, Skipped: 0
```

🟢 All green — and your real data was never touched. 👍

---

## 🧪 Part 3: Keeping `@SpringBootTest` away from your real data

Remember Chapter 84? The old `contextLoads()` test started the **whole** app — with our **real** file database! The loaders even added users to it. 😬 A test should **never** touch real data.

The fix: a **test profile** (Chapter 56) with its **own** database.

Create **`src/test/resources/application-test.properties`** (make the `resources` folder inside `src/test` if it isn't there):

```properties
# Settings only for tests: a fresh in-memory database every time
spring.datasource.url=jdbc:h2:mem:schooltest
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.show-sql=false
```

| Code | Meaning |
|---|---|
| `src/test/resources/` | Files here are only used when **tests** run. |
| `application-test.properties` | Settings for the profile called **`test`**. They're added **on top** of `application.properties` and win where they differ. |
| `jdbc:h2:mem:schooltest` | An **in-memory** database 💨 instead of the file. Every test run starts empty. |
| `ddl-auto=create-drop` | Make all tables at the start, delete them at the end. |
| `spring.jpa.show-sql=false` | No SQL in the test output — less noise. |

Now switch the profile on in **`SchoolApplicationTests`**:

```java
@SpringBootTest
@ActiveProfiles("test")
class SchoolApplicationTests {

    @Test
    void contextLoads() {
    }
}
```

(Import `org.springframework.test.context.ActiveProfiles`.)

| Code | Meaning |
|---|---|
| `@ActiveProfiles("test")` | ⭐ "For this test, use the profile `test`." → `application-test.properties` is loaded → the in-memory database. |

Run it, and look at the log: the database URL is now `jdbc:h2:mem:schooltest`. Your `./data/school` file is safe. 🛡️

⚠️ **Don't** call the file `src/test/resources/application.properties`! A file with the **same** name as the main one **replaces** it completely during tests — then all your normal settings (the JWT secret, the admin password...) would be **missing**. With `application-test.properties`, you only **change** what you need. 👍

---

## 🎂 Part 4: The whole cake — an integration test

Now the "driving test" 🚗: start the **whole** app, with a real (in-memory) database, real security, real JWTs. One test that walks through a **real story**:

1. The teacher **logs in** → gets a token.
2. With the token, the teacher **adds** a student → 201.
3. **Anyone** can then **read** the new student → 200.

**`src/test/java/com/example/school/SchoolFlowIntegrationTest.java`**

```java
package com.example.school;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.assertj.MockMvcTester;
import org.springframework.test.web.servlet.assertj.MvcTestResult;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class SchoolFlowIntegrationTest {

    @Autowired
    private MockMvcTester mvc;

    @Test
    void teacherLogsInAndAddsAStudent() throws Exception {
        // 1. Log in
        MvcTestResult login = mvc.post().uri("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                        {"username":"teacher","password":"secret123"}
                        """)
                .exchange();
        assertThat(login).hasStatusOk();
        String token = tokenFrom(login.getResponse().getContentAsString());

        // 2. Add a student with the token
        MvcTestResult created = mvc.post().uri("/api/students")
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + token)
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                        {"name":"Mia Clark","email":"mia@school.com","age":11}
                        """)
                .exchange();
        assertThat(created).hasStatus(HttpStatus.CREATED);
        String location = created.getResponse().getHeader(HttpHeaders.LOCATION);

        // 3. Anyone can read the new student
        assertThat(mvc.get().uri(location))
                .hasStatusOk()
                .bodyJson()
                .extractingPath("$.name").isEqualTo("Mia Clark");
    }

    @Test
    void wrongPasswordGives401() {
        assertThat(mvc.post().uri("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                        {"username":"teacher","password":"wrong"}
                        """))
                .hasStatus(HttpStatus.UNAUTHORIZED)
                .bodyJson()
                .extractingPath("$.title").isEqualTo("Login failed");
    }

    private static String tokenFrom(String json) {
        String start = "\"token\":\"";
        int from = json.indexOf(start) + start.length();
        int to = json.indexOf("\"", from);
        return json.substring(from, to);
    }
}
```

| Code | Meaning |
|---|---|
| `@SpringBootTest` | ⭐ Start the **whole** app: all beans, the loaders, security, Hibernate, the database. 🎂 |
| `@AutoConfigureMockMvc` | "...and give me a `MockMvcTester` that sends requests to it." |
| `@ActiveProfiles("test")` | Use the **in-memory** test database. Our `UserLoader` and `DataLoader` fill it — so `teacher` / `secret123` exists! |
| `.exchange()` | Send the request **now** and give back the result (an `MvcTestResult`), so we can **use** parts of it later. |
| `login.getResponse().getContentAsString()` | The answer's body as text: `{"token":"eyJ...","tokenType":"Bearer","expiresIn":3600}`. It can throw a (checked) exception — that's why the test method says `throws Exception`. |
| `tokenFrom(...)` | Our small helper: find `"token":"`, and cut out the text up to the next `"` (Chapter 9: `indexOf`, `substring`). |
| `.header(HttpHeaders.AUTHORIZATION, "Bearer " + token)` | ⭐ A **real** token — made by our real `TokenService`, checked by our real `JwtDecoder`. No `jwt()` pretending this time! |
| `created.getResponse().getHeader(HttpHeaders.LOCATION)` | The `Location` header: `/api/students/4`. |
| `mvc.get().uri(location)` | Read the new student — **without** a token. |

This one test checks that **all** of these fit together: the login endpoint, the `AuthenticationManager`, BCrypt, the token maker, the token checker, the roles converter, the security rules, the controller, validation, the service, the repository, Hibernate and the database. 🧩🧩🧩 That's the power of an integration test!

The price: it starts the **whole** app, so it's the slowest test we have. 🐢 Spring is clever, though: test classes with the **same** settings share **one** started app (Spring **caches** it), so `SchoolApplicationTests` and `SchoolFlowIntegrationTest` don't start it twice.

---

## 🔺 Part 5: The test pyramid

Now you know **four** kinds of tests. How many of each should you write? Programmers draw it as a **pyramid**:

```
              ▲
             ╱ ╲          🎂 @SpringBootTest     a FEW   — slow, checks everything together
            ╱───╲
           ╱     ╲        🍰 @WebMvcTest,         SOME    — medium, checks one layer
          ╱───────╲          @DataJpaTest
         ╱         ╲
        ╱───────────╲     🧩 unit tests           MANY    — fast, checks small pieces
       ╱_____________╲       (JUnit + Mockito)
```

| Question | Best test |
|---|---|
| Is my calculation / `if` logic right? | 🧩 unit test |
| Does my query method / native SQL work? | 🍰 `@DataJpaTest` |
| Right URL, status, JSON, validation, security rule? | 🍰 `@WebMvcTest` |
| Does the whole story work end to end? | 🎂 `@SpringBootTest` |

Run **everything** now:

```bash
./mvnw test
```

You should see every test class from Part 11 — and at the end:

```
[INFO] BUILD SUCCESS
```

Make it a habit: **run all tests before you commit** (Chapter 42). 🟢 = safe to save. 🔴 = fix first!

---

## 💻 Mini project: Test the users table 👥

Write **`AppUserRepositoryTest`** with `@DataJpaTest`:

1. `existsByUsername("teacher")` is `true` after saving a `teacher`, and `existsByUsername("nobody")` is `false`.
2. `findByUsername("teacher")` finds the user with the right role.
3. Saving **two** users with the **same** username must **fail** — remember `unique = true` (Chapter 81)? Expect a `DataIntegrityViolationException`.

**Hint for 3:** `save` doesn't send the `INSERT` right away — Hibernate waits until the end of the transaction. Use **`saveAndFlush`**, which sends it **immediately**.

<details>
<summary>Click to see the answer</summary>

**`src/test/java/com/example/school/repository/AppUserRepositoryTest.java`**

```java
package com.example.school.repository;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.dao.DataIntegrityViolationException;

import com.example.school.entity.AppUser;

@DataJpaTest
class AppUserRepositoryTest {

    @Autowired
    private AppUserRepository appUserRepository;

    @Test
    void existsByUsername() {
        appUserRepository.save(new AppUser("teacher", "hash", "TEACHER"));

        assertThat(appUserRepository.existsByUsername("teacher")).isTrue();
        assertThat(appUserRepository.existsByUsername("nobody")).isFalse();
    }

    @Test
    void findByUsername() {
        appUserRepository.save(new AppUser("teacher", "hash", "TEACHER"));

        assertThat(appUserRepository.findByUsername("teacher"))
                .isPresent()
                .get()
                .extracting(AppUser::getRole)
                .isEqualTo("TEACHER");
    }

    @Test
    void usernamesMustBeUnique() {
        appUserRepository.saveAndFlush(new AppUser("sara", "hash1", "USER"));

        assertThatThrownBy(() -> appUserRepository.saveAndFlush(new AppUser("sara", "hash2", "USER")))
                .isInstanceOf(DataIntegrityViolationException.class);
    }
}
```

| Code | Meaning |
|---|---|
| `"hash"` | In a repository test, the password is just text — no `PasswordEncoder` needed. |
| `isTrue()` / `isFalse()` | AssertJ for `boolean`s. |
| `saveAndFlush(...)` | ⭐ Save **and** send the SQL to the database **now**. The database checks the `UNIQUE` rule → the second insert fails right here, inside `assertThatThrownBy`. |
| `DataIntegrityViolationException` | Spring's exception for "the database refused: a rule (like `UNIQUE` or `NOT NULL`) was broken". |

This test proves that the **database** itself protects us from two `sara`s — even if a bug in the service forgot to check. 🛡️

</details>

---

## ✋ Try it yourself

1. Add a test to `StudentRepositoryTest` for `findTop2ByOrderByAgeDesc()`. Which two names come back, and in which order?
2. Remove `@ActiveProfiles("test")` from `SchoolApplicationTests` and run it. Look at the database URL in the log. Put it back!
3. In `SchoolFlowIntegrationTest`, add a third step: log in as **admin** (`admin` / `admin12345`) and **delete** the new student → 204.

<details>
<summary>Click to see the answers</summary>

1. Tom (13) first, then Sara (12) — `ORDER BY age DESC` gives a fixed order, so here you **can** use `containsExactly("Tom Brown", "Sara Ahmed")`.
2. It's `jdbc:h2:file:./data/school` again — your real data. That's what we want to avoid.
3. Log in as admin exactly like the teacher (copy the login lines with the admin's name and password), then:
   ```java
   assertThat(mvc.delete().uri(location)
           .header(HttpHeaders.AUTHORIZATION, "Bearer " + adminToken))
           .hasStatus(HttpStatus.NO_CONTENT);
   ```
   (The admin's password comes from `${ADMIN_PASSWORD:admin12345}` — in tests, the default is used.)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Tests that use the real database

Without a test profile, `@SpringBootTest` uses `./data/school` — and your tests **change real data**. **Fix:** `application-test.properties` + `@ActiveProfiles("test")`.

### Mistake 2: Naming the test settings `application.properties`

It **replaces** the main settings completely. **Fix:** Use a profile file: `application-test.properties`.

### Mistake 3: Checking an order the database doesn't promise

`containsExactly("Sara Ahmed", "Tom Brown")` on a query **without** `ORDER BY` may work today and fail tomorrow. **Fix:** `containsExactlyInAnyOrder(...)`, or add `ORDER BY` to the query.

### Mistake 4: Expecting an error from `save` too early

`save` with a duplicate username often doesn't fail **at once** — Hibernate sends the `INSERT` later. **Fix:** `saveAndFlush` in the test (mini project).

### Mistake 5: Writing everything as `@SpringBootTest`

It works... but your test run takes minutes instead of seconds, and when one fails, you don't know **which** layer broke. **Fix:** Follow the pyramid 🔺: many unit tests, some slice tests, a few full tests.

---

## ✅ Summary

- **`@DataJpaTest`** 🗄️ tests repositories against a **fresh in-memory** database. Each test is **rolled back** ↩️ → always clean.
- Repository tests catch what mocks can't: wrong query names, wrong JPQL, wrong native SQL, missing database rules.
- A **test profile** (`src/test/resources/application-test.properties` + `@ActiveProfiles("test")`) keeps full tests away from your **real** data.
- **`@SpringBootTest` + `@AutoConfigureMockMvc`** 🎂 starts the whole app — perfect for a few **end-to-end stories** (login → token → add → read).
- `.exchange()` gives you an `MvcTestResult` to reuse parts of an answer (like a token or a `Location`).
- The **test pyramid** 🔺: many unit tests, some slice tests, a few full tests. Run **all** of them with `./mvnw test` before every commit.

---

## ❓ Quiz

1. What does `@DataJpaTest` start, and which database does it use?
2. Why does `theDatabaseStartsCleanForEveryTest` always find exactly 3 students?
3. Which bug could `StudentRepositoryTest` find that `StudentServiceTest` (with mocks) never could?
4. Why must the test settings file be called `application-test.properties` and not `application.properties`?
5. What does `@ActiveProfiles("test")` do?
6. In the integration test, why does `teacher` / `secret123` work, even though the test database starts empty?
7. Draw (or describe) the test pyramid.

<details>
<summary>Click to see the answers</summary>

1. Only the database layer: entities, repositories, Hibernate — with a new in-memory H2 database instead of the real one.
2. Every test runs in a transaction that is rolled back at the end, so the students from earlier tests are gone. `@BeforeEach` adds 3 new ones.
3. For example: a wrong native SQL query, a misspelled query method, or a missing `UNIQUE` rule.
4. A test `application.properties` would replace the main one completely, so all normal settings would be missing. A profile file only adds or changes settings.
5. It switches on the `test` profile for that test class, so `application-test.properties` is used.
6. `@SpringBootTest` starts the whole app, including `UserLoader`, which creates the teacher in the empty test database.
7. Bottom (many): unit tests. Middle (some): slice tests like `@WebMvcTest` and `@DataJpaTest`. Top (few): `@SpringBootTest` integration tests.

</details>

---

## 🎉 Part 11 complete!

Your app now has a **taste tester** 👩‍🔬 that never gets tired! Look at what you learned:

- ✅ **Why** we test, and the **Arrange – Act – Assert** steps
- ✅ **JUnit**: `@Test`, `@BeforeEach`, `assertEquals`, `assertThrows`, `@ParameterizedTest` 🔁
- ✅ **AssertJ**: `assertThat(...)` that reads like English 🗣️
- ✅ **Mockito**: `@Mock`, `@InjectMocks`, `when/thenReturn`, `verify`, `ArgumentCaptor` 🎭
- ✅ **Controller tests**: `@WebMvcTest`, `MockMvcTester`, `@MockitoBean`, `jwt()` 🍰
- ✅ **Database tests**: `@DataJpaTest`, rollback, test profiles 🗄️
- ✅ **Integration tests**: `@SpringBootTest` from login to database 🎂
- ✅ The **test pyramid** 🔺

### 🏁 Where are we?

```
 Part 1 ✅ Getting ready          Part 7  ✅ Spring Boot basics
 Part 2 ✅ Java basics            Part 8  ✅ Building REST APIs
 Part 3 ✅ Objects (OOP)          Part 9  ✅ Databases
 Part 4 ✅ More Java              Part 10 ✅ Security
 Part 5 ✅ Tools                  Part 11 ✅ Testing          ← you are here! 🎉
 Part 6 ✅ How the web works      Part 12 ⏳ Useful extras    ← next!
```

In **Part 12**, you'll fill your toolbox with **useful extras** 🧰: a diary for your app (logging), real HTML pages, calling other websites, jobs on a timer, file uploads, automatic API documentation, and health checks. Let's go!

---

[⬅ Previous chapter](86-testing-controllers.md) | [Table of Contents](../README.md) | [Next chapter: Logging ➡](../part-12-extras/88-logging.md)
