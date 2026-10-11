# Chapter 67 – What is a database?

[⬅ Previous chapter](../part-08-rest-apis/66-error-handling.md) | [Table of Contents](../README.md) | [Next chapter ➡](68-sql-basics.md)

---

## 🎯 Goal

Welcome to **Part 9**! 🎉 Our Student API from Part 8 has one big problem: **restart the app, and every new student is gone.** 💨 Today we learn about the solution: a **database**. 🗄️

At the end of this chapter you will know:

- Why keeping data in a Java list (in **memory**) is not enough
- What a **database** is, and what a **database server** does
- How data is organized in **tables**, **rows** and **columns** 📊
- What a **primary key** is (and why every row needs one) 🔑
- What a **foreign key** is (how tables are connected) 🔗
- The most popular databases: **PostgreSQL**, **MySQL**, **H2**... and which one we use
- How a Spring Boot app talks to a database (the big picture)

> 🌱 This chapter has **no code**. It's a "thinking" chapter, with lots of pictures. From Chapter 68 on, you'll type real database commands! ⌨️

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Database** | A program that **stores** data **safely** and lets you **find** it quickly. 🗄️ |
| **Persistent** | Data that **stays** — even after the app stops or the computer restarts. (The opposite of "in memory".) |
| **Table** | A **grid** of data, like a spreadsheet: `students`. 📊 |
| **Row** | **One** thing in a table: one student. (Also called a **record**.) |
| **Column** | **One kind** of information: `name`, `age`... (Also called a **field**.) |
| **Primary key** | A column whose value is **unique** for every row, like a student number: `id`. 🔑 |
| **Foreign key** | A column that **points** to a row in **another** table. 🔗 |
| **Relational database** | A database made of **tables** that are connected by keys. |
| **SQL** | The **language** we use to talk to relational databases. (Chapter 68) |
| **Database server** | A program that runs the database and answers questions from apps, like a web server answers browsers. |
| **Schema** | The **plan** of the database: which tables, which columns, which types. |

---

## 📖 Story: The forgetful secretary 🧠💨

Remember our school secretary from Part 8? 👩‍💼 She keeps all the student cards **in her head**. She's very fast!

But every evening, she goes home and sleeps... and the next morning, she has **forgotten** everything except the 3 students she learned on her first day. 😱 New students? Changed emails? **Gone.**

That's our app right now: the `LinkedHashMap` in `StudentRepository` lives in the computer's **memory** (RAM). When the app stops — **poof** 💨 — everything is gone.

The school needs a **filing cabinet** 🗄️ with real paper cards. Cards stay in the cabinet overnight, over the weekend, even if the secretary is sick. And any secretary can open the cabinet and find any card.

That filing cabinet is a **database**. 🗄️✨

---

## 💨 Part 1: Memory vs. a database

| | In memory (a Java `List` / `Map`) 🧠 | In a database 🗄️ |
|---|---|---|
| Where | The computer's **RAM** | Files on the **disk** (managed by a database program) |
| After a restart | ❌ **Gone** | ✅ Still there |
| Size | Limited by RAM (a few GB) | Huge — millions or billions of rows |
| Many apps at once | ❌ Each app has its own copy | ✅ Many apps share the **same** data |
| Searching | You write loops and streams | The database searches **very** fast for you ⚡ |
| Safety | A crash loses data | Built to **never** lose data, even if the power goes out |
| Rules | Only in your Java code | The database itself can check rules (no duplicate emails!) |

Real apps **always** keep important data in a database. Your bank, your school, your online games... all of them. 🏦🏫🎮

---

## 📊 Part 2: Tables, rows and columns

A **relational database** keeps data in **tables**. A table looks like a spreadsheet:

```
 Table: students
 ┌────┬──────────────┬──────────────────┬─────┐
 │ id │ name         │ email            │ age │   ← COLUMNS (the kinds of information)
 ├────┼──────────────┼──────────────────┼─────┤
 │ 1  │ Sara Ahmed   │ sara@school.com  │ 12  │   ← ROW 1 (one student)
 │ 2  │ Tom Brown    │ tom@school.com   │ 13  │   ← ROW 2
 │ 3  │ Lina Haddad  │ lina@school.com  │ 11  │   ← ROW 3
 └────┴──────────────┴──────────────────┴─────┘
```

| Word | In the picture | In Java (Part 8) |
|---|---|---|
| **Table** `students` | the whole grid | the whole list/map of students |
| **Column** `name` | one column, top to bottom | a field: `String name` |
| **Row** | one line, left to right | one `Student` object |
| **Cell** | one box | one value: `"Tom Brown"` |

Does it remind you of something? 🤔 Our `Student` record has **the same 4 fields** as this table has columns! That's not an accident. In Chapter 71, Java classes and database tables will be **connected** automatically. 🔗✨

### Every column has a type

Like Java variables (Chapter 7), every column has a **type**. Database types have different names:

| Database type | Meaning | Java type |
|---|---|---|
| `BIGINT` | a big whole number | `Long` / `long` |
| `INT` / `INTEGER` | a whole number | `Integer` / `int` |
| `VARCHAR(50)` | text, **at most** 50 characters | `String` |
| `BOOLEAN` | true / false | `boolean` |
| `DATE` | a day | `LocalDate` |
| `TIMESTAMP` | a day and a time | `LocalDateTime` |
| `DECIMAL(10,2)` | an exact number with decimals (money!) | `BigDecimal` |

---

## 🔑 Part 3: The primary key

Imagine two students are both called **"Ali Hassan"**. 👦👦 How do you say **which** one you mean?

You need something that is **always different** for each row: a **primary key**. In our table, it's the **`id`** column:

```
 ┌────┬─────────────┬────────────────────┬─────┐
 │ id │ name        │ email              │ age │
 ├────┼─────────────┼────────────────────┼─────┤
 │ 7  │ Ali Hassan  │ ali.h@school.com   │ 10  │
 │ 8  │ Ali Hassan  │ ali.hassan@...     │ 12  │   ← same name, different id ✅
 └────┴─────────────┴────────────────────┴─────┘
   🔑
```

Rules for a primary key:

| Rule | Why |
|---|---|
| **Unique** — no two rows have the same value | So it points to **exactly one** row |
| **Never empty** (`NULL`) | Every row must be findable |
| **Never changes** | Other tables point to it (Part 4)! |

Usually, the **database creates** the id for you: 1, 2, 3, 4... automatically. You saw this idea in Part 8 — the **server** chooses the id, never the client. Now the **database** will do it! 🎉

> 💡 This is exactly what `/api/students/{id}` uses! The path variable (Chapter 58) is the **primary key** of the row. 🔑

---

## 🔗 Part 4: Connected tables — the foreign key

A school has more than students. It has **classrooms** too. 🏫 Each student is in **one** classroom. How do we store that?

**❌ Bad idea:** put all classroom information into the students table:

```
 ┌────┬─────────────┬───────────┬────────────────┐
 │ id │ name        │ classroom │ teacher        │
 ├────┼─────────────┼───────────┼────────────────┤
 │ 1  │ Sara Ahmed  │ 5A        │ Mrs. Khan      │
 │ 3  │ Lina Haddad │ 5A        │ Mrs. Khan      │   ← "Mrs. Khan" written again...
 │ 2  │ Tom Brown   │ 6B        │ Mr. Brown      │
 └────┴─────────────┴───────────┴────────────────┘
```

Mrs. Khan's name is written **again and again**. If she gets married and changes her name, you must change **every** row... and you'll forget one. 😬

**✅ Good idea:** **two** tables, connected by a **key**:

```
 Table: classrooms                       Table: students
 ┌────┬──────┬────────────┐              ┌────┬─────────────┬──────────────┐
 │ id │ name │ teacher    │              │ id │ name        │ classroom_id │
 ├────┼──────┼────────────┤              ├────┼─────────────┼──────────────┤
 │ 1  │ 5A   │ Mrs. Khan  │ ◄────────────┤ 1  │ Sara Ahmed  │ 1            │
 │ 2  │ 6B   │ Mr. Brown  │ ◄──┐   ┌─────┤ 3  │ Lina Haddad │ 1            │
 └────┴──────┴────────────┘    └───┼─────┤ 2  │ Tom Brown   │ 2            │
   🔑 primary key                  │     └────┴─────────────┴──────────────┘
                                   │                          🔗 foreign key
```

The column **`classroom_id`** in `students` is a **foreign key**: it holds the **primary key** of a row in **another** table. "Sara is in classroom **1**" → look up classroom 1 → "5A, Mrs. Khan". 🔍

- Mrs. Khan's name is written only **once**. ✅
- The database **checks** foreign keys: you **can't** put `classroom_id = 99` if there's no classroom 99! 🛡️

That's why it's called a **relational** database: the tables have **relations** (connections). You'll build this for real in **Chapter 75**. 🔗

---

## 🗄️ Part 5: The database server

A real database is a **separate program** — a **database server** — that runs all the time and waits for questions. Sounds familiar? It's like your web server (Chapter 43)! 🍽️

```
  📱 Phone app  ──┐
                  │  HTTP           ┌───────────────────┐   SQL      ┌──────────────────┐
  🌐 Website   ───┼───────────────► │ Your Spring Boot  │ ─────────► │ Database server  │
                  │                 │ app (port 8080)   │ ◄───────── │ (port 5432)  🗄️  │
  🖥️ curl      ───┘                 └───────────────────┘   rows     └──────────────────┘
                                                                         files on disk 💾
```

- **Clients** talk to **your app** with **HTTP** and **JSON** (Part 6–8).
- **Your app** talks to the **database server** with **SQL** (Chapter 68).
- The database server stores everything in **files** on the disk. 💾

Your app is a **client** of the database — just like a browser is a client of your app! 🔄

---

## 🌍 Part 6: Popular databases

There are many database programs. Here are the ones you'll hear about most:

| Database | Free? | Notes |
|---|---|---|
| **PostgreSQL** ("Postgres") 🐘 | ✅ | Very popular, very powerful. Loved by Spring developers. |
| **MySQL** 🐬 | ✅ | Very popular, especially for websites. |
| **MariaDB** 🦭 | ✅ | A "twin" of MySQL, made by the same original creator. |
| **Microsoft SQL Server** | 💰 (free small version) | Common in big companies using Microsoft tools. |
| **Oracle Database** | 💰 | Common in banks and very big companies. |
| **SQLite** 🪶 | ✅ | Tiny; lives inside phone apps and browsers. |
| **H2** 🧪 | ✅ | A small database **written in Java**. Perfect for **learning** and **tests**! |

All of these are **relational** databases, and they all speak **SQL**. Learn SQL once, and you can use **all** of them. 🎉 (Each one has small differences — like dialects of a language. 🗣️)

### Which one do we use?

| Chapters | Database | Why |
|---|---|---|
| 68–76, 78–79 | **H2** 🧪 | Nothing to install! It comes as a Maven dependency and runs **inside** your app. |
| 77 | **PostgreSQL** and **MySQL** | How to switch to a "real" database server — with almost **no code changes**. |

> 💡 **NoSQL databases** (like MongoDB or Redis) don't use tables. They store data as documents or key-value pairs. They're useful for special cases, but most apps start with a relational database. We won't use NoSQL in this book.

---

## 🧭 Part 7: The plan for Part 9

Here's the road from "memory" to "real database": 🗺️

| Chapter | What you'll learn |
|---|---|
| **67** | What a database is (today!) |
| **68** | **SQL**: the language of databases — create tables, add, find, change and delete rows |
| **69** | **H2** inside your Spring Boot app, and the **H2 console** (a web page to look into the database) |
| **70** | **JPA**: how Java objects and tables are connected — and why it saves **so much** code |
| **71** | **Entities**: Java classes that become tables |
| **72** | **Repositories**: `save`, `findAll`, `findById`... with **one line** of code 🤯 |
| **73** | The **Student API** with a real database — data survives restarts! 🎉 |
| **74** | Your **own queries**: `findByAgeGreaterThan(...)` |
| **75–76** | **Relationships**: classrooms ↔ students, students ↔ courses |
| **77** | **PostgreSQL** and **MySQL** |
| **78** | **Pages** and **sorting** for big lists |
| **79** | **Transactions**: all or nothing |

---

## 💻 Mini project: Design the library database on paper 📚✏️

No computer today — take a **pencil and paper**! ✏️ Our school library (your Book API from Part 8) needs a database. Design **two** tables:

1. A table **`books`** with columns for: an id, the title, the author, the year, and **which shelf** it's on.
2. A table **`shelves`** with: an id, a code (like `"A-1"`), and the room (like `"Library 1st floor"`).

Questions:

- a) Which column is the **primary key** of each table?
- b) How does a book "know" which shelf it's on? Which kind of key is that?
- c) Write 2 shelves and 3 books as **rows** in your tables.
- d) Choose a **type** for each column (from the table in Part 2).

<details>
<summary>Click to see an example answer</summary>

```
 Table: shelves
 ┌────┬──────┬────────────────────┐
 │ id │ code │ room               │
 ├────┼──────┼────────────────────┤
 │ 1  │ A-1  │ Library 1st floor  │
 │ 2  │ F-7  │ Library 2nd floor  │
 └────┴──────┴────────────────────┘
   🔑

 Table: books
 ┌────┬─────────────────┬────────────────┬──────┬──────────┐
 │ id │ title           │ author         │ year │ shelf_id │
 ├────┼─────────────────┼────────────────┼──────┼──────────┤
 │ 1  │ Matilda         │ Roald Dahl     │ 1988 │ 1        │
 │ 2  │ The Hobbit      │ J.R.R. Tolkien │ 1937 │ 2        │
 │ 3  │ Charlotte's Web │ E.B. White     │ 1952 │ 1        │
 └────┴─────────────────┴────────────────┴──────┴──────────┘
   🔑                                                🔗 foreign key → shelves.id
```

- a) `id` in both tables.
- b) The column `shelf_id` in `books` holds the id of a shelf. It's a **foreign key**.
- d) Types: `id` → `BIGINT`, `title` → `VARCHAR(100)`, `author` → `VARCHAR(50)`, `year` → `INT`, `shelf_id` → `BIGINT`, `code` → `VARCHAR(10)`, `room` → `VARCHAR(50)`.

Your names and sizes can be different — that's fine! The important ideas: **one table per kind of thing**, a **primary key** in each, and a **foreign key** to connect them. 🔗

</details>

---

## ✋ Try it yourself

**Task 1:** In this table, what is a) one row, b) one column, c) the primary key?

```
 ┌────┬───────────┬───────┐
 │ id │ subject   │ hours │
 ├────┼───────────┼───────┤
 │ 1  │ Math      │ 5     │
 │ 2  │ English   │ 4     │
 └────┴───────────┴───────┘
```

<details>
<summary>Click to see the answer</summary>

a) For example `2 | English | 4` b) For example `subject` (Math, English) c) `id`

</details>

**Task 2:** Could `email` be a primary key for students? What could go wrong?

<details>
<summary>Click to see the answer</summary>

It **is** unique... but it can **change** (Tom changed his email in Part 8!). A primary key should **never** change, because other tables point to it. That's why we use a simple number `id` as the primary key, and just make `email` **unique** (a rule the database checks — Chapter 68).

</details>

**Task 3:** Why is it a bad idea to write the teacher's name in every student row?

<details>
<summary>Click to see the answer</summary>

The same information is stored many times. If it changes, you must update every row — and if you forget one, your data is wrong (two different names for the same teacher). Better: a separate `classrooms` table, and a **foreign key** in `students`.

</details>

---

## ⚠️ Common mistakes (in thinking)

### Mistake 1: "I'll just save my data in a text file"

It works for one tiny program. But what if two users save at the **same moment**? What if the computer crashes **while** writing? 💥 Databases solve these problems for you. Use one!

### Mistake 2: Putting everything in one big table

One huge table with students **and** classrooms **and** teachers → the same data written many times, and mistakes when it changes. **Fix:** One table per kind of thing, connected by keys. 🔗

### Mistake 3: Using a name as the primary key

Names are **not** unique (two "Ali Hassan"s!) and they can change. **Fix:** A simple number `id`, created by the database. 🔑

### Mistake 4: Thinking "database" means "Excel file"

Tables **look** like spreadsheets, but a database is much more: types, rules, keys, safety, speed, and many users at once. 🗄️⚡

---

## ✅ Summary

- Data in **memory** (a Java list or map) is **lost** when the app stops. A **database** keeps it **persistent**. 💾
- A **relational database** stores data in **tables** 📊: **columns** (kinds of information, with **types**) and **rows** (one thing each).
- A **primary key** 🔑 (usually `id`) is unique, never empty, and never changes. The database can create it for you.
- A **foreign key** 🔗 points to a row in another table — that's how tables are **connected**.
- A **database server** is a separate program. Your app talks to it with **SQL**, like browsers talk to your app with HTTP.
- Popular databases: **PostgreSQL** 🐘, **MySQL** 🐬, MariaDB, SQL Server, Oracle, SQLite — and **H2** 🧪, a small Java database for learning and tests.
- We'll use **H2** first, then switch to PostgreSQL/MySQL in Chapter 77.

---

## ❓ Quiz

1. Why do our new students disappear when we restart the app?
2. What is a table? A row? A column?
3. What are the three rules of a primary key?
4. What is a foreign key? Give an example.
5. Which language do apps use to talk to relational databases?
6. Name three popular databases.
7. Why do we start with H2?
8. Your app is a server for browsers. What is your app for the database?

<details>
<summary>Click to see the answers</summary>

1. They're stored only in memory (a Java map). When the app stops, the memory is cleared.
2. A table is a grid of data about one kind of thing. A row is one thing (one student). A column is one kind of information (like `name`).
3. Unique, never empty, never changes.
4. A column that holds the primary key of a row in another table. Example: `classroom_id` in `students` points to `id` in `classrooms`.
5. **SQL**
6. Any three: PostgreSQL, MySQL, MariaDB, SQL Server, Oracle, SQLite, H2.
7. It's small, written in Java, needs no installation, and runs inside the app — perfect for learning.
8. A **client** (it sends questions in SQL and gets rows back).

</details>

---

[⬅ Previous chapter](../part-08-rest-apis/66-error-handling.md) | [Table of Contents](../README.md) | [Next chapter: SQL basics ➡](68-sql-basics.md)
