# Chapter 69 – H2: a small database for learning

[⬅ Previous chapter](68-sql-basics.md) | [Table of Contents](../README.md) | [Next chapter ➡](70-spring-data-jpa.md)

---

## 🎯 Goal

You can speak SQL now! 🗣️ Today we put a database **inside** your Spring Boot app.

At the end of this chapter you will know:

- The two ways H2 can store data: **in memory** and **in a file**
- How to add **H2** (and Spring Data JPA) to the `school` project
- How to set the **database address** in `application.properties`
- How to open the **H2 Console inside your app** at `/h2-console` 🖥️
- How Spring Boot runs **`schema.sql`** and **`data.sql`** for you at startup
- What all the new **log lines** mean

> 🌱 Today the database and our API live **side by side** — they don't talk to each other yet. In Chapters 70–73, we'll connect them. One step at a time! 🪜

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Embedded database** | A database that runs **inside** your app (no separate server). H2 can do that! |
| **In-memory database** | A database that keeps everything in **RAM**. Super fast, but gone after a restart. 💨 |
| **File database** | A database that saves everything in a **file** on the disk. Stays after a restart. 💾 |
| **DataSource** | The Java object that knows **how to connect** to the database (address, user, password). |
| **Connection pool** | A box of **ready** database connections, so the app doesn't have to open a new one every time. 🏊 |
| **HikariCP** | The connection pool Spring Boot uses. (Hikari = "light" in Japanese — it's very fast! ⚡) |
| **`schema.sql`** | A file with `CREATE TABLE` statements that Spring Boot runs at startup. |
| **`data.sql`** | A file with `INSERT` statements that Spring Boot runs at startup. |

---

## 📖 Story: A fridge in your kitchen 🧊

Until now, our app was a cook who keeps all ingredients **in his hands**. 🤲 When he goes home, he drops everything. 💨

**Option 1: A big supermarket** 🏬 (a database **server**, like PostgreSQL): a separate building, very big, many cooks can use it. But you need to drive there, and someone must run it. (Chapter 77.)

**Option 2: A small fridge in the kitchen** 🧊 (an **embedded** database, like H2): right next to the cook, nothing to install, ready immediately. Perfect for **learning** and **testing**!

And the small fridge has two modes:

- **Party mode** 🎉 (in memory): super fast, but emptied every night.
- **Normal mode** 💾 (a file): keeps the food overnight.

---

## 🧪 Part 1: H2 — memory or file?

H2 chooses the mode from the **URL**:

| JDBC URL | Mode | After a restart |
|---|---|---|
| `jdbc:h2:mem:school` | 🧠 **In memory**, database name `school` | ❌ Empty again |
| `jdbc:h2:file:./data/school` | 💾 **File** `data/school.mv.db` in the project folder | ✅ Still there |
| `jdbc:h2:~/sql-practice` | 💾 File in your **home** folder (Chapter 68) | ✅ Still there |

Today we use **memory** — it's perfect for trying things. In Chapter 73, we'll switch to a **file**, so our students survive restarts. 🎉

---

## 📦 Part 2: Add the dependencies

Open the **`pom.xml`** of your `school` project (from Part 8) and add these **three** dependencies inside `<dependencies>`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-h2console</artifactId>
</dependency>
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
</dependency>
```

Then click **Maven reload** 🔄.

| Dependency | What it brings |
|---|---|
| `spring-boot-starter-data-jpa` | **Spring Data JPA** + **Hibernate** + JDBC + the **HikariCP** pool. Everything to work with databases in Java. (Chapter 70 explains it.) |
| `spring-boot-h2console` | The **H2 Console** web page, **inside** your app. |
| `h2` with `<scope>runtime</scope>` | The **H2 database** itself. `runtime` = "needed when the app runs, not to compile" (Chapter 41) — your code never uses H2 classes directly. |

> 💡 On **start.spring.io**, these are called **Spring Data JPA** and **H2 Database**. If you choose H2 **and** Spring Web, Spring Initializr adds `spring-boot-h2console` for you (we saw that in Chapter 49!).

---

## 🎛️ Part 3: Tell Spring where the database is

Open **`src/main/resources/application.properties`** and make it look like this:

```properties
spring.application.name=school

# The database
spring.datasource.url=jdbc:h2:mem:school
spring.datasource.username=sa
spring.datasource.password=

# The H2 console (a web page to look inside the database)
spring.h2.console.enabled=true

spring.jpa.open-in-view=false
```

### 🔍 Line by line

| Setting | Meaning |
|---|---|
| `spring.datasource.url=jdbc:h2:mem:school` | ⭐ The database **address**: H2, in memory, named `school`. |
| `spring.datasource.username=sa` | The user name (H2's default). |
| `spring.datasource.password=` | The password: **empty**. (Fine for a learning database on your laptop. **Never** for a real one! 🔒) |
| `spring.h2.console.enabled=true` | ⭐ Turn on the H2 Console at `/h2-console`. It's **off** by default — we tested: without this line, `/h2-console` gives **404**. |
| `spring.jpa.open-in-view=false` | A technical setting we'll explain in Chapter 75. Spring Boot even **warns** you in the log if you don't set it. Just keep it. 😊 |

> 💡 **What if you don't set the URL?** Spring Boot still starts an in-memory H2 — but with a **random** name like `jdbc:h2:mem:ac1b8494-4d63-4aec-95a6-b9087267629e` (a real one from our test!). Hard to type in the console. 😅 That's why we choose the name `school` ourselves.

---

## 📜 Part 4: `schema.sql` and `data.sql`

Spring Boot has a nice trick: if it finds these two files in `src/main/resources`, it runs them **at startup**:

| File | Runs... | Put in it |
|---|---|---|
| **`schema.sql`** | first | `CREATE TABLE ...` |
| **`data.sql`** | second | `INSERT INTO ...` |

(By default, it only does this for **embedded** databases like H2.)

Create **`src/main/resources/schema.sql`**:

```sql
CREATE TABLE students (
    id    BIGINT       PRIMARY KEY,
    name  VARCHAR(50)  NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    age   INT
);
```

And **`src/main/resources/data.sql`**:

```sql
INSERT INTO students (id, name, email, age) VALUES (1, 'Sara Ahmed', 'sara@school.com', 12);
INSERT INTO students (id, name, email, age) VALUES (2, 'Tom Brown', 'tom@school.com', 13);
INSERT INTO students (id, name, email, age) VALUES (3, 'Lina Haddad', 'lina@school.com', 11);
```

The **same** SQL you typed in Chapter 68! Now Spring types it for you, every time the app starts. 🤖

---

## ▶️ Part 5: Run and read the new log lines

Restart the app. The log has **new** lines (shortened, from a real run):

```
... Bootstrapping Spring Data JPA repositories in DEFAULT mode.
... Finished Spring Data repository scanning in 22 ms. Found 0 JPA repository interfaces.
... HikariPool-1 - Starting...
... HikariPool-1 - Added connection conn0: url=jdbc:h2:mem:school user=SA
... HikariPool-1 - Start completed.
... HHH000001: Hibernate ORM core version 7.4.5.Final
... HHH10001005: Database info:
	Database JDBC URL [jdbc:h2:mem:school]
	Database driver: H2 JDBC Driver
	Database dialect: H2Dialect
	Database version: 2.4.240
... Initialized JPA EntityManagerFactory for persistence unit 'default'
... H2 console available at '/h2-console'. Database available at 'jdbc:h2:mem:school'
... Tomcat started on port 8080 (http) with context path '/'
... Started SchoolApplication in 7.369 seconds
```

| Log message | Meaning |
|---|---|
| `Bootstrapping Spring Data JPA repositories` / `Found 0 JPA repository interfaces` | Spring Data looked for **repository interfaces**. None yet — Chapter 72! |
| `HikariPool-1 - Starting...` / `Added connection conn0: url=jdbc:h2:mem:school` | 🏊 The **connection pool** opened its first connection to **our** database. ✅ |
| `Hibernate ORM core version 7.4.5.Final` | **Hibernate** started (the library that does JPA — Chapter 70). |
| `Database driver: H2 JDBC Driver` / `Database dialect: H2Dialect` / `Database version: 2.4.240` | Hibernate found an **H2** database and will speak H2's "dialect" of SQL. 🗣️ |
| `Initialized JPA EntityManagerFactory` | JPA is ready. |
| ⭐ `H2 console available at '/h2-console'. Database available at 'jdbc:h2:mem:school'` | The console is on, and it even tells you the **URL** to use! 🎁 |

The app starts a bit **slower** now (7 seconds instead of 4). Starting a database and Hibernate takes a moment. ⏳

---

## 🖥️ Part 6: Look inside — the H2 Console

Open your browser: **`http://localhost:8080/h2-console`**

You see the **same** login page as in Chapter 68. Fill in:

| Field | Value |
|---|---|
| Driver Class | `org.h2.Driver` |
| JDBC URL | ⭐ **`jdbc:h2:mem:school`** (exactly as in `application.properties`!) |
| User Name | `sa` |
| Password | *(empty)* |

Click **Connect**. On the left, you see the table **`STUDENTS`**. Type:

```sql
SELECT * FROM students;
```

Real result:

```
ID | NAME        | EMAIL           | AGE
1  | Sara Ahmed  | sara@school.com | 12
2  | Tom Brown   | tom@school.com  | 13
3  | Lina Haddad | lina@school.com | 11
(3 rows)
```

🎉 The table from `schema.sql`, filled by `data.sql` — **inside your Spring Boot app**!

Try things from Chapter 68: add a student, update one, count them... It all works.

> ⚠️ **Wrong URL = empty database!** If you type `jdbc:h2:mem:test` (or anything else), H2 creates a **new, empty** in-memory database with that name — and you see **no** tables. 😕 Always copy the URL from the log line `Database available at '...'`.

---

## 🤔 Part 7: Two separate worlds (for now)

Now try your **API**: `GET http://localhost:8080/api/students`. It still works — and shows the same 3 students. But... 🤔

Add a student **in the console**:

```sql
INSERT INTO students (id, name, email, age) VALUES (4, 'Omar Ali', 'omar@school.com', 12);
```

Then call the API again. **Omar is not there!** 😮

Why? Because our API still uses the **`LinkedHashMap`** in `StudentRepository` (Chapter 63) — it doesn't know the database exists! Right now, there are **two separate worlds**:

```
   🌐 API  ──► StudentService ──► StudentRepository ──► 🧠 LinkedHashMap  (Part 8)

   🖥️ H2 Console ─────────────────────────────────────► 🗄️ H2 database    (today)
```

In the next chapters, we'll connect them, so the API reads and writes the **database**:

```
   🌐 API  ──► StudentService ──► StudentRepository ──► 🗄️ H2 database    (Chapter 73 🎯)
```

And remember: it's **in memory**. Restart the app → Omar is gone, and `data.sql` adds the 3 students again. 💨

---

## 💻 Mini project: The library shelf 📚

Add a **`books`** table to your database at startup:

1. In **`schema.sql`**, add a `books` table: an **automatic** `id` (Chapter 68, Part 9), `title` (required, max 100), `author` (required, max 50), `published` (a number — remember, **not** `year`! 😉).
2. In **`data.sql`**, add Matilda, The Hobbit and Charlotte's Web.
3. Restart, open the console, and run: `SELECT * FROM books ORDER BY published;`

<details>
<summary>Click to see the answer</summary>

Add to **`schema.sql`**:

```sql
CREATE TABLE books (
    id        BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    title     VARCHAR(100) NOT NULL,
    author    VARCHAR(50)  NOT NULL,
    published INT
);
```

Add to **`data.sql`**:

```sql
INSERT INTO books (title, author, published) VALUES ('Matilda', 'Roald Dahl', 1988);
INSERT INTO books (title, author, published) VALUES ('The Hobbit', 'J.R.R. Tolkien', 1937);
INSERT INTO books (title, author, published) VALUES ('Charlotte''s Web', 'E.B. White', 1952);
```

(Remember the **double** `''` in Charlotte''s Web!)

`SELECT * FROM books ORDER BY published;`

```
ID | TITLE           | AUTHOR         | PUBLISHED
2  | The Hobbit      | J.R.R. Tolkien | 1937
3  | Charlotte's Web | E.B. White     | 1952
1  | Matilda         | Roald Dahl     | 1988
```

</details>

---

## ✋ Try it yourself

**Task 1:** Remove the line `spring.h2.console.enabled=true` and restart. What happens at `http://localhost:8080/h2-console`? Then put it back.

<details>
<summary>Click to see the answer</summary>

**404 Not Found** — the console is **off** by default. (That's good for safety: you never want the console open on a real server! 🔒)

</details>

**Task 2:** In the console, run `SELECT COUNT(*) FROM students;` Then restart the app and run it again. Why is it always 3 after a restart, even if you added students?

<details>
<summary>Click to see the answer</summary>

The database is **in memory** (`jdbc:h2:mem:...`): it's empty after every restart, and then `schema.sql` and `data.sql` create the same 3 students again.

</details>

**Task 3:** Change the URL to `jdbc:h2:mem:library`. What must you type in the console now?

<details>
<summary>Click to see the answer</summary>

`jdbc:h2:mem:library` — the console URL must **match** `spring.datasource.url`. The log line `Database available at '...'` shows it. (Change it back to `school` afterwards.)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: `/h2-console` gives 404

**Fix:** Add `spring.h2.console.enabled=true`. (And make sure `spring-boot-h2console` is in `pom.xml`.)

### Mistake 2: The console shows no tables

You typed a different JDBC URL in the console → an **empty** database. **Fix:** Use **exactly** the URL from `application.properties` (`jdbc:h2:mem:school`).

### Mistake 3: Forgetting the Maven reload

You added the dependencies, but `spring.datasource...` settings do nothing and imports are red. **Fix:** Click **Maven reload** 🔄 after changing `pom.xml`.

### Mistake 4: Using `year` as a column name

`schema.sql` fails at startup with a syntax error, and the app **doesn't start**. **Fix:** Use another name, like `published` (Chapter 68).

### Mistake 5: Leaving the console on in production

The H2 Console lets anybody who can reach it **read and change all your data**. 😱 **Fix:** Only enable it on your laptop (a `dev` profile — Chapter 56!). We'll set that up in Chapter 77.

---

## ✅ Summary

- **H2** is a small database written in Java. It can run **embedded** (inside your app) — no installation. 🧊
- The URL decides the mode: **`jdbc:h2:mem:school`** (in memory, gone after a restart 💨) or **`jdbc:h2:file:./data/school`** (a file, stays 💾).
- Dependencies: **`spring-boot-starter-data-jpa`**, **`spring-boot-h2console`**, **`h2`** (runtime).
- Settings: **`spring.datasource.url`**, `username`, `password`, and **`spring.h2.console.enabled=true`**.
- Spring Boot runs **`schema.sql`** (tables) and then **`data.sql`** (rows) at startup.
- The **H2 Console** at **`/h2-console`** lets you run SQL inside your app's database. Use the **same** JDBC URL as in the settings.
- New log lines: **HikariPool** (connections 🏊), **Hibernate** (JPA), **H2Dialect**, and the console address.
- Right now, the API (a map) and the database are **two separate worlds**. Next chapters: we connect them! 🔗

---

## ❓ Quiz

1. What's the difference between `jdbc:h2:mem:school` and `jdbc:h2:file:./data/school`?
2. Which three dependencies did we add?
3. Why does `h2` have `<scope>runtime</scope>`?
4. What do `schema.sql` and `data.sql` do? Which one runs first?
5. How do you open the H2 Console in your app?
6. You open the console, connect, and see no tables. What's the most likely reason?
7. You add a student in the console. Why doesn't the API show it?
8. Why should the H2 Console never be enabled on a real server?

<details>
<summary>Click to see the answers</summary>

1. `mem` keeps the database in memory (it's empty after a restart). `file` saves it in a file (it stays).
2. `spring-boot-starter-data-jpa`, `spring-boot-h2console`, `h2`.
3. Our code never uses H2 classes directly — it's only needed when the app **runs**.
4. `schema.sql` creates the tables, `data.sql` adds rows. `schema.sql` runs first.
5. Enable it with `spring.h2.console.enabled=true`, then go to `http://localhost:8080/h2-console`.
6. The JDBC URL in the console is different from `spring.datasource.url`, so you connected to a new, empty database.
7. The API still reads from the `LinkedHashMap` in `StudentRepository`, not from the database.
8. Anyone who can reach it can read and change all the data.

</details>

---

[⬅ Previous chapter](68-sql-basics.md) | [Table of Contents](../README.md) | [Next chapter: Spring Data JPA: the introduction ➡](70-spring-data-jpa.md)
