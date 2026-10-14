# Chapter 88 – Logging: writing a diary for your app

[⬅ Previous chapter](../part-11-testing/87-testing-with-database.md) | [Table of Contents](../README.md) | [Next chapter ➡](89-thymeleaf.md)

---

## 🎯 Goal

When your app runs on a server somewhere, you can't watch it. 👀 Something goes wrong at 3 o'clock at night... how will you ever know **what** happened? 🤔

The answer: your app writes a **diary** 📔 — a **log**. You've seen Spring's log lines since Chapter 51. Today you'll learn to write **your own**.

At the end of this chapter you will know:

- Why **`System.out.println`** isn't good enough 🙅
- How to write log lines with a **`Logger`** (SLF4J)
- The five **log levels**: `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR` 🚦
- How to choose **how much** to log, for each package, in `application.properties`
- How to write the log into a **file** 📄
- What you must **never** write into a log 🔒

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Log** | The app's **diary**: one line for each interesting thing that happens. 📔 |
| **Logger** | The object you use to **write** log lines. ✍️ |
| **SLF4J** | "Simple Logging Facade for Java": the **standard way** to write logs in Java. Spring uses it. |
| **Logback** | The library that really **prints** the lines (to the screen or a file). Comes with Spring Boot. |
| **Log level** | How **important** a log line is: from `TRACE` (tiny details) to `ERROR` (something broke). 🚦 |
| **Placeholder** | `{}` in a log message: "put a value **here**". |
| **Stack trace** | The list of method calls that led to an exception — "where did it happen?" 🗺️ |

---

## 📖 Story: The ship's logbook ⛵

On old sailing ships, the captain kept a **logbook** 📔. Every hour, someone wrote:

```
 08:00  INFO   Wind from the west, speed 5 knots.
 09:00  INFO   Saw an island to the north.
 10:00  WARN   Dark clouds in the south. Watching them.
 11:00  ERROR  Storm! The main sail is torn!
```

Later, back in port, people could read the book and understand **exactly** what happened — even if they weren't on the ship. 🕵️

(Fun fact: that's where the word **"log"** comes from! Sailors measured the speed by throwing a wooden **log** into the water. 🪵)

Your app's log is its logbook:

- Normal things (a student was added) → **INFO**
- Strange things (someone tried a wrong password 5 times) → **WARN**
- Broken things (the database is down) → **ERROR**

---

## 🙅 Part 1: Why not `System.out.println`?

So far, our loaders used `System.out.println`:

```
DataLoader: the database already has 3 students
```

But compare that to a **Spring** log line:

```
2026-10-11T11:43:49.851+05:30  INFO 6196 --- [school] [           main] com.example.school.SchoolApplication     : Started SchoolApplication in 10.929 seconds
```

| Part | Meaning |
|---|---|
| `2026-10-11T11:43:49.851+05:30` | **When** — to the millisecond. ⏰ |
| `INFO` | **How important**. |
| `6196` | The process number (which running program). |
| `[school]` | The app's name. |
| `[           main]` | The **thread** — which "worker" wrote it. (Each web request has its own, like `nio-8080-exec-1`.) |
| `com.example.school.SchoolApplication` | **Who** wrote it (which class). |
| `Started SchoolApplication in ...` | **What** happened. |

`System.out.println` has **none** of that. And there's more:

| `System.out.println` | A real logger |
|---|---|
| No time, no level, no class name | All of it, automatically ⭐ |
| Can't be switched off | Each level can be switched **on or off** — without changing code |
| Only to the screen | Screen **and/or** file |
| Prints everything, always | You choose **how much** detail, per package |

---

## ✍️ Part 2: Your first logger

Let's give **`StudentService`** a diary. Add a logger at the top of the class:

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
@Transactional(readOnly = true)
public class StudentService {

    private static final Logger log = LoggerFactory.getLogger(StudentService.class);

    private final StudentRepository studentRepository;
    ...
```

| Code | Meaning |
|---|---|
| `import org.slf4j.Logger;` | ⚠️ From **`org.slf4j`** — IntelliJ may offer other `Logger` classes too. Pick this one! |
| `private static final Logger log` | One logger for the whole class (`static`, Chapter 27), never changed (`final`). Most people call it `log` or `logger`. |
| `LoggerFactory.getLogger(StudentService.class)` | "Make a logger **named** after this class." That's the name you'll see in each line. |

Now write some diary entries in `create` and `delete`:

```java
@Transactional
public StudentResponse create(StudentRequest request) {
    if (studentRepository.existsByEmailIgnoreCase(request.email())) {
        log.warn("Tried to add a student with an email that is already used: {}", request.email());
        throw new EmailAlreadyUsedException(request.email());
    }
    Student student = new Student(request.name(), request.email(), request.age());
    Student saved = studentRepository.save(student);
    log.info("Added student {} with id {}", saved.getName(), saved.getId());
    return StudentResponse.from(saved);
}

@Transactional
public void delete(Long id) {
    if (!studentRepository.existsById(id)) {
        throw new StudentNotFoundException(id);
    }
    studentRepository.deleteById(id);
    log.info("Deleted student with id {}", id);
}
```

| Code | Meaning |
|---|---|
| `log.info("Added student {} with id {}", saved.getName(), saved.getId())` | ⭐ An **INFO** line. Each **`{}`** is a **placeholder**: the values after the text fill them **in order**. |
| `log.warn(...)` | A **WARN** line: "not broken, but strange — someone should maybe look". |

Add a student (as teacher, with a token — Chapter 83). In the app's log you'll see a line like this:

```
2026-10-14T10:15:02.331+05:30  INFO 8412 --- [school] [nio-8080-exec-3] c.e.school.service.StudentService        : Added student Mia Clark with id 6
```

And for a taken email:

```
2026-10-14T10:15:40.118+05:30  WARN 8412 --- [school] [nio-8080-exec-5] c.e.school.service.StudentService        : Tried to add a student with an email that is already used: sara@school.com
```

📏 Notice: the long class name is **shortened** to `c.e.school.service.StudentService` so the lines stay neat.

### 🤔 Why `{}` and not `+`?

```java
log.debug("Student: " + student);        // ❌ always builds the text — even if DEBUG is off!
log.debug("Student: {}", student);       // ✅ builds the text ONLY if DEBUG is on
```

With `{}`, the logger first checks "is this level switched on?" — and only **then** puts the text together. When DEBUG is off (the normal case), no time is wasted. 🚀

---

## 🚦 Part 3: The five log levels

| Level | When to use it | Example |
|---|---|---|
| `TRACE` 🔬 | The tiniest details. Almost never. | "Entering method findStudent with id 5" |
| `DEBUG` 🐛 | Details that help **programmers** find bugs. | "Found 3 students for the filter minAge=12" |
| `INFO` ℹ️ | **Normal**, important events. | "Added student Mia Clark with id 6" |
| `WARN` ⚠️ | Something **strange**, but the app keeps working. | "Wrong password for user sara" |
| `ERROR` 🔥 | Something **broke**. Someone must look! | "Could not connect to the database" |

The levels are like a **ladder** 🪜. When you set the level to `INFO`, you see `INFO` **and everything above it**:

```
 ERROR  🔥  ┐
 WARN   ⚠️  │ shown when the level is INFO
 INFO   ℹ️  ┘
 DEBUG  🐛     hidden
 TRACE  🔬     hidden
```

Spring Boot's **default** level is **`INFO`**. That's why you never saw DEBUG lines — until you switched them on yourself, like in Chapter 79 (`JpaTransactionManager=DEBUG`) and Chapter 80 (`org.springframework.security=DEBUG`). Now you know what those settings did! 🎉

---

## ⚙️ Part 4: Choosing the level — per package

You can set the level for **any** package or class, in `application.properties`:

```properties
# Our own code: show DEBUG lines too
logging.level.com.example.school=DEBUG

# Spring Security: only warnings and errors
logging.level.org.springframework.security=WARN

# Everything else
logging.level.root=INFO
```

| Code | Meaning |
|---|---|
| `logging.level.com.example.school=DEBUG` | ⭐ Every logger whose name starts with `com.example.school` → level DEBUG. |
| `logging.level.org.springframework.security=WARN` | Spring Security: be quiet unless something is wrong. |
| `logging.level.root=INFO` | **root** = "everybody else". |

The **most specific** setting wins. A logger named `com.example.school.service.StudentService` uses `com.example.school=DEBUG`, not `root=INFO`. 🎯

Let's add a DEBUG line to `getAll`:

```java
public List<StudentResponse> getAll(Integer minAge, String name) {
    log.debug("Getting students with minAge={} and name={}", minAge, name);
    ...
```

With `logging.level.com.example.school=DEBUG`, calling `GET /api/students?minAge=12` writes:

```
... DEBUG 8412 --- [school] [nio-8080-exec-7] c.e.school.service.StudentService        : Getting students with minAge=12 and name=null
```

Remove the `DEBUG` setting → the line disappears. **No** code change needed! 🪄

💡 **Profiles** (Chapter 56) are perfect here: `DEBUG` in `application-dev.properties`, `INFO` or `WARN` in `application-prod.properties`.

---

## 🔥 Part 5: Logging errors — with the stack trace

Remember our catch-all handler from Chapter 66?

```java
@ExceptionHandler(Exception.class)
public ProblemDetail handleEverythingElse(Exception ex) {
    logger.error("Unexpected error", ex);
    ...
```

There it is — a logger! (`ResponseEntityExceptionHandler` already has one called `logger`, so we didn't need to make our own.) Look at the **two** arguments:

| Code | Meaning |
|---|---|
| `"Unexpected error"` | The message. |
| `ex` | ⭐ The exception itself, as the **last** argument → the logger prints the whole **stack trace** 🗺️ — exactly **where** it happened. |

You saw the result in Chapter 82:

```
ERROR ... c.e.s.exception.GlobalExceptionHandler   : Unexpected error
org.springframework.security.authorization.AuthorizationDeniedException: Access Denied
	at ...
```

⚠️ A common mistake:

```java
log.error("Unexpected error: " + ex.getMessage());   // ❌ only the message — WHERE did it happen? Nobody knows!
log.error("Unexpected error", ex);                    // ✅ message + stack trace
```

You can mix placeholders and the exception — the exception just has to come **last**:

```java
log.error("Could not save student {}", request.email(), ex);
```

---

## 📄 Part 6: Writing the log into a file

On a server, nobody watches the screen. So we write the log into a **file**:

```properties
logging.file.name=logs/school.log
```

| Code | Meaning |
|---|---|
| `logging.file.name=logs/school.log` | Write every log line into this file **as well** (the screen still works). Spring makes the `logs` folder if needed. |

Restart, and look in your project folder: there's `logs/school.log` with the same lines as the console. 📄

What if the file gets **huge**? Spring Boot takes care of it: when the file reaches **10 MB**, it's packed away (like `school.log.2026-10-14.0.gz`) and a new one starts. Old files are deleted after **7 days**. You can change both:

```properties
logging.logback.rollingpolicy.max-file-size=5MB
logging.logback.rollingpolicy.max-history=30
```

⚠️ Add `logs/` to your **`.gitignore`** (Chapter 42) — log files don't belong in Git!

---

## 🔒 Part 7: What NEVER goes into a log

Logs are read by **many** people (other programmers, the people who run servers...), and they're kept for a long time. So **never** log:

| ❌ Never log | Why |
|---|---|
| Passwords (even wrong ones!) 🔑 | A "wrong" password is often the **right** one with a typo. |
| Tokens (JWTs) 🎟️ | Anyone with the log could use them (Chapter 83). |
| Password hashes | They should never leave the database. |
| Secret keys, `JWT_SECRET`, `DB_PASSWORD` | The keys to everything. 👑 |
| Too much private data (addresses, birthdays...) | People have a right to privacy. |

```java
log.info("User {} logged in with password {}", username, password);   // ❌❌❌ NEVER!
log.info("User {} logged in", username);                                // ✅
```

---

## 💻 Mini project: A diary for the users 👥

Add a logger to **`UserService`** (Chapters 81–82) and log:

1. **INFO** when a new user registers: `"New user registered: sara"`.
2. **WARN** when someone tries to register a name that is taken.
3. **INFO** when an admin changes a role: `"Role of user 2 changed from USER to TEACHER"`.
4. **WARN** when someone tries to change their password with a **wrong** current password — but of course **without** the password! 🔒

<details>
<summary>Click to see the answer</summary>

**In `UserService`:**

```java
private static final Logger log = LoggerFactory.getLogger(UserService.class);
```

(Imports: `org.slf4j.Logger`, `org.slf4j.LoggerFactory`.)

```java
@Transactional
public UserResponse register(RegisterRequest request) {
    if (appUserRepository.existsByUsername(request.username())) {
        log.warn("Someone tried to register the taken username {}", request.username());
        throw new UsernameTakenException(request.username());
    }
    String hash = passwordEncoder.encode(request.password());
    AppUser saved = appUserRepository.save(new AppUser(request.username(), hash, "USER"));
    log.info("New user registered: {}", saved.getUsername());
    return UserResponse.from(saved);
}

@Transactional
public void changePassword(String username, ChangePasswordRequest request) {
    AppUser appUser = appUserRepository.findByUsername(username).orElseThrow();
    if (!passwordEncoder.matches(request.currentPassword(), appUser.getPassword())) {
        log.warn("User {} sent a wrong current password", username);
        throw new WrongPasswordException();
    }
    appUser.setPassword(passwordEncoder.encode(request.newPassword()));
    log.info("User {} changed their password", username);
}

@PreAuthorize("hasRole('ADMIN')")
@Transactional
public UserResponse changeRole(Long id, String role) {
    AppUser appUser = appUserRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    String oldRole = appUser.getRole();
    appUser.setRole(role);
    log.info("Role of user {} changed from {} to {}", id, oldRole, role);
    return UserResponse.from(appUser);
}
```

| Code | Meaning |
|---|---|
| `String oldRole = appUser.getRole();` | Remember the old role **before** changing it — otherwise we can't write "from USER". |
| `log.warn("User {} sent a wrong current password", username)` | ⭐ The **name**, but **never** the password. 🔒 |

</details>

---

## ✋ Try it yourself

1. Set `logging.level.root=WARN`. Start the app. What happened to all the start-up lines?
2. Set `logging.level.org.hibernate.SQL=DEBUG` (and `spring.jpa.show-sql=false`). Do you see the SQL now? What's different from `show-sql`?
3. Replace the `System.out.println` lines in `DataLoader` and `UserLoader` with `log.info(...)`.

<details>
<summary>Click to see the answers</summary>

1. Almost all of them are gone — they're `INFO` lines. Only warnings and errors remain. (Even "Started SchoolApplication" disappears! That's why `INFO` is the usual setting.)
2. Yes — Hibernate's SQL now goes through the **logger**: each line has a time, a level and the name `org.hibernate.SQL`. `show-sql` uses `System.out` (no time, no level). Many people prefer the logger way.
3. For example, in `UserLoader`:
   ```java
   private static final Logger log = LoggerFactory.getLogger(UserLoader.class);
   ...
   log.info("Added the user {} with the role {}", username, role);
   ```

</details>

---

## ⚠️ Common mistakes

### Mistake 1: The wrong `Logger` import

IntelliJ offers several `Logger` classes (`java.util.logging.Logger`, ...). Then `LoggerFactory` doesn't fit. **Fix:** `import org.slf4j.Logger;` and `import org.slf4j.LoggerFactory;`.

### Mistake 2: Building messages with `+`

Slower, and harder to read. **Fix:** Use `{}` placeholders.

### Mistake 3: Losing the stack trace

`log.error("Failed: " + ex.getMessage())` → no "where". **Fix:** Pass the exception as the **last** argument: `log.error("Failed", ex)`.

### Mistake 4: Logging secrets

Passwords, tokens, keys. **Fix:** Log **who** and **what**, never the secret itself.

### Mistake 5: Too much logging

An `INFO` line in a loop that runs a million times → a giant, useless log. 🐘 **Fix:** Details → `DEBUG`. Only important events → `INFO`.

---

## ✅ Summary

- A **log** 📔 is your app's diary. Use a **`Logger`** (SLF4J), not `System.out.println`.
- `private static final Logger log = LoggerFactory.getLogger(MyClass.class);`
- Levels 🚦: `TRACE` < `DEBUG` < `INFO` < `WARN` < `ERROR`. The default is `INFO`.
- Use **`{}`** placeholders: `log.info("Added {} with id {}", name, id)`.
- For errors, pass the **exception last** → stack trace 🗺️.
- Set levels per package: `logging.level.com.example.school=DEBUG`. Write to a file with `logging.file.name`.
- **Never** log passwords, tokens or secrets. 🔒

---

## ❓ Quiz

1. Name three things a log line has that `System.out.println` doesn't.
2. Put the five levels in order, from least to most important.
3. The level is `WARN`. Which lines do you see?
4. Why is `log.debug("x = {}", x)` better than `log.debug("x = " + x)`?
5. How do you make the logger print the stack trace of an exception?
6. What does `logging.level.com.example.school=DEBUG` do?
7. Name two things you must never log.

<details>
<summary>Click to see the answers</summary>

1. The time, the level, the class name (also the thread and the app name).
2. `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`.
3. `WARN` and `ERROR` lines.
4. With `{}`, the text is only built when DEBUG is switched on. It's faster and easier to read.
5. Pass the exception as the last argument: `log.error("message", ex)`.
6. It shows DEBUG (and higher) lines for all loggers in the package `com.example.school` and below.
7. For example: passwords, tokens, password hashes, secret keys.

</details>

---

[⬅ Previous chapter](../part-11-testing/87-testing-with-database.md) | [Table of Contents](../README.md) | [Next chapter: Thymeleaf ➡](89-thymeleaf.md)
