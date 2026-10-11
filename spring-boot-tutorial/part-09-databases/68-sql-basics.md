# Chapter 68 – SQL basics

[⬅ Previous chapter](67-what-is-a-database.md) | [Table of Contents](../README.md) | [Next chapter ➡](69-h2-database.md)

---

## 🎯 Goal

Databases speak a special language: **SQL**. 🗣️ Today you'll learn to speak it — and you'll type real commands into a real database!

At the end of this chapter you will know:

- How to start the **H2 Console** (a web page for talking to a database)
- How to **create** a table: `CREATE TABLE`
- How to **add** rows: `INSERT`
- How to **find** rows: `SELECT`, `WHERE`, `ORDER BY`, `LIKE` 🔍
- How to **count** and do math: `COUNT`, `AVG`, `MIN`, `MAX`, `GROUP BY`
- How to **change** and **remove** rows: `UPDATE`, `DELETE` (carefully! ⚠️)
- How the database **protects** your data with rules (`PRIMARY KEY`, `NOT NULL`, `UNIQUE`) 🛡️

> 🌱 Why learn SQL if Spring can write it for you (Chapter 70+)? Because you'll **see** SQL in your logs every day, you'll need it to **look into** your database, and you'll write your own queries sometimes (Chapter 74). It's like knowing how a car engine works — even if the car is automatic. 🚗

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **SQL** | **S**tructured **Q**uery **L**anguage — the language for relational databases. Say "S-Q-L" or "sequel". |
| **Statement** | One SQL command, like `SELECT * FROM students;`. |
| **Query** | A **question** to the database: "Which students are 12 or older?" |
| **Keyword** | A word with a special meaning in SQL: `SELECT`, `FROM`, `WHERE`... |
| **Constraint** | A **rule** the database checks: `NOT NULL`, `UNIQUE`, `PRIMARY KEY`. 🛡️ |
| **`NULL`** | "No value" / empty — like `null` in Java. |
| **Result set** | The rows you get back from a `SELECT`. |
| **Aggregate function** | A function that works on **many** rows and gives **one** answer: `COUNT`, `AVG`... |

---

## 📖 Story: Talking to the librarian 📚👵

The school library has a very old, very wise librarian. She knows **every** book. But she only understands questions asked in a **special, exact** way:

- ❌ "Hey, got any old books?" → she looks at you confused. 🤨
- ✅ "**SELECT** the titles **FROM** the books **WHERE** the year is before 1960." → she brings them immediately! 📚⚡

SQL is that special, exact way of asking. The words are English, the grammar is strict. Once you know it, the database answers **anything** in milliseconds. 🧙‍♀️

---

## 🧪 Part 1: Start the H2 Console

We need a database to practice with. We'll use **H2** — a small database that's just **one Java file** (a `.jar`). No installation! 🎉

### Step 1: Download H2

Download this file (it's the official H2 jar from Maven Central — Chapter 40):

```
https://repo1.maven.org/maven2/com/h2database/h2/2.4.240/h2-2.4.240.jar
```

Save it in a folder you can find, for example `C:\Users\YourName\h2` (Windows) or `~/h2` (Mac/Linux).

> 💡 A newer version is fine too. Just use your file name in the commands below.

### Step 2: Start the console

Open a terminal in that folder and type:

```
java -cp h2-2.4.240.jar org.h2.tools.Server -web -ifNotExists -browser
```

| Part | Meaning |
|---|---|
| `java -cp h2-2.4.240.jar` | Run Java, with the H2 jar on the **classpath** (Chapter 50). |
| `org.h2.tools.Server` | The H2 class that starts a server. |
| `-web` | Start the **web console** (a web page). |
| `-ifNotExists` | ⭐ "If the database doesn't exist yet, **create** it." (Without it, H2 refuses to create new databases from the console — for safety.) |
| `-browser` | Open the console in your browser automatically. |

The terminal says:

```
Web Console server running at http://192.168.1.8:8082 (only local connections)
```

(Your address will be different.) And your browser opens the **login page**:

```
┌───────────────────────────────────────────────────┐
│  English ▾   Preferences   Tools   Help            │
│                                                    │
│  Login                                             │
│  Saved Settings: [ Generic H2 (Embedded)      ▾ ]  │
│  Setting Name:   [ Generic H2 (Embedded) ] Save    │
│                                                    │
│  Driver Class:   [ org.h2.Driver             ]     │
│  JDBC URL:       [ jdbc:h2:~/test            ]     │
│  User Name:      [ sa                        ]     │
│  Password:       [                           ]     │
│                                                    │
│            [ Connect ]   [ Test Connection ]       │
└───────────────────────────────────────────────────┘
```

### Step 3: Connect

Change **JDBC URL** to:

```
jdbc:h2:~/sql-practice
```

Keep **User Name** `sa` and an **empty** password. Click **Connect**. 🔌

| Part of the URL | Meaning |
|---|---|
| `jdbc:` | "A Java database address." (JDBC = **J**ava **D**ata**b**ase **C**onnectivity — Chapter 70.) |
| `h2:` | "Use the H2 database." |
| `~/sql-practice` | "Store it in my **home folder**, in files starting with `sql-practice`." (`~` = your home folder.) |
| User `sa` | "**S**ystem **A**dministrator" — H2's default user. |

You see the **SQL page**: a list of tables on the left (empty for now), a big **text box** at the top for your SQL, and a **Run** button (or **Ctrl + Enter**). 🎉 The results appear at the bottom.

> 💡 **Stop the console:** press **Ctrl + C** in the terminal. Your data stays in the file (`sql-practice.mv.db` in your home folder). Start the console again tomorrow, connect with the same URL — your tables are still there! 💾

---

## 🏗️ Part 2: CREATE TABLE — build the table

Type this into the text box and click **Run**:

```sql
CREATE TABLE students (
    id    BIGINT       PRIMARY KEY,
    name  VARCHAR(50)  NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    age   INT
);
```

```
Update count: 0
```

✅ The table `STUDENTS` appears on the left!

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `CREATE TABLE students (` | "Make a new table called `students`, with these columns:" |
| `id BIGINT PRIMARY KEY,` | Column `id`, a big number, and it's the **primary key** 🔑 (unique, never empty — Chapter 67). |
| `name VARCHAR(50) NOT NULL,` | Column `name`: text, max **50** characters. **`NOT NULL`** = it must **always** have a value. |
| `email VARCHAR(100) NOT NULL UNIQUE,` | Text, max 100, never empty, and **`UNIQUE`** = no two rows may have the same email. 📧 |
| `age INT` | A whole number. No rule — it **may** be empty (`NULL`). |
| `);` | End of the column list. The **`;`** ends the statement (like in Java!). |

### 📏 SQL style rules

| Rule | Example |
|---|---|
| Keywords are usually written in **CAPITALS** (easier to read) | `SELECT`, `FROM`, `WHERE` |
| But SQL **doesn't care** about big/small letters in keywords and names | `select * from students` also works |
| Names: small letters and `_` | `students`, `teacher_note` |
| **Text** values in **single** quotes `' '` | `'Sara Ahmed'` |
| Numbers **without** quotes | `12` |
| End each statement with `;` | `SELECT * FROM students;` |

> 💡 H2 shows names in **CAPITALS** (`STUDENTS`, `NAME`). That's normal — H2 changes unquoted names to capitals internally. You can still type them in small letters.

---

## ➕ Part 3: INSERT — add rows

```sql
INSERT INTO students (id, name, email, age) VALUES (1, 'Sara Ahmed', 'sara@school.com', 12);
```

```
Update count: 1
```

"1 row was added." ✅ You can add **several** rows in one statement:

```sql
INSERT INTO students (id, name, email, age) VALUES
    (2, 'Tom Brown', 'tom@school.com', 13),
    (3, 'Lina Haddad', 'lina@school.com', 11);
```

```
Update count: 2
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `INSERT INTO students` | "Add a new row to `students`..." |
| `(id, name, email, age)` | "...filling these columns..." |
| `VALUES (1, 'Sara Ahmed', 'sara@school.com', 12)` | "...with these values" — in the **same order** as the columns. |
| `(2, ...), (3, ...)` | Several rows, separated by commas. |

> ⚠️ **Text needs single quotes:** `'Sara Ahmed'`. With double quotes (`"Sara Ahmed"`), SQL thinks you mean a **column name**! We tried: `Column "Omar Ali" not found`. 😅
>
> And a name **with** a single quote inside, like **Charlotte's Web**? Write the quote **twice**: `'Charlotte''s Web'`.

---

## 🔍 Part 4: SELECT — find rows

This is the command you'll use **most**. 🥇

### All rows, all columns

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

| Code | Meaning |
|---|---|
| `SELECT` | "Give me..." |
| `*` | "...**all** columns..." (the star means "everything" ⭐) |
| `FROM students` | "...from the table `students`." |

### Only some columns

```sql
SELECT name, age FROM students;
```

```
NAME        | AGE
Sara Ahmed  | 12
Tom Brown   | 13
Lina Haddad | 11
(3 rows)
```

### WHERE — only some rows 🎯

```sql
SELECT * FROM students WHERE age >= 12;
```

```
ID | NAME       | EMAIL           | AGE
1  | Sara Ahmed | sara@school.com | 12
2  | Tom Brown  | tom@school.com  | 13
(2 rows)
```

**`WHERE`** is a filter — just like `.filter(...)` in a Java stream (Chapter 36), or `?minAge=12` in our API (Chapter 59)! 🔍

Comparisons you can use:

| SQL | Meaning | Java |
|---|---|---|
| `=` | equal | `==` / `equals` |
| `<>` or `!=` | not equal | `!=` |
| `<`, `>`, `<=`, `>=` | smaller, bigger... | the same |
| `AND`, `OR`, `NOT` | combine | `&&`, `\|\|`, `!` |
| `IS NULL` / `IS NOT NULL` | empty / not empty | `== null` |
| `BETWEEN 11 AND 12` | from 11 to 12 (both included) | `>= 11 && <= 12` |
| `IN (1, 3)` | one of these | `List.of(1, 3).contains(...)` |

> ⚠️ In SQL, "equal" is **one** `=`, not two! And for `NULL` you must write `IS NULL` — `age = NULL` never finds anything. 🤯

### LIKE — search in text 🔤

```sql
SELECT * FROM students WHERE name LIKE '%a%';
```

```
ID | NAME        | EMAIL           | AGE
1  | Sara Ahmed  | sara@school.com | 12
3  | Lina Haddad | lina@school.com | 11
(2 rows)
```

| Pattern | Meaning |
|---|---|
| `%` | "any text (even nothing)" |
| `'%a%'` | contains an `a` |
| `'S%'` | starts with `S` |
| `'%.com'` | ends with `.com` |

⚠️ In H2 (and PostgreSQL), text comparisons **care about big/small letters**: `WHERE name = 'sara ahmed'` finds **nothing** — we tried it: `(0 rows)`. (Remember the `IgnoreCase` in our Java code? We'll meet it again in Chapter 74!)

### ORDER BY — sort ↕️

```sql
SELECT name, age FROM students ORDER BY age DESC;
```

```
NAME        | AGE
Tom Brown   | 13
Sara Ahmed  | 12
Lina Haddad | 11
(3 rows)
```

| Code | Meaning |
|---|---|
| `ORDER BY age` | Sort by age, small → big (`ASC` = ascending, the default). |
| `DESC` | **Desc**ending: big → small. |

> 💡 **Without `ORDER BY`, the order is NOT guaranteed!** The database may return rows in **any** order. If order matters, always write `ORDER BY`. ⚠️

### The order of the parts

A `SELECT` always has its parts in **this** order:

```sql
SELECT   name, age          -- 1. which columns
FROM     students           -- 2. which table
WHERE    age >= 12          -- 3. which rows
ORDER BY name;              -- 4. which order
```

(`--` starts a **comment** in SQL, like `//` in Java.)

---

## 🧮 Part 5: Counting and math

**Aggregate functions** look at **many** rows and give **one** answer:

```sql
SELECT COUNT(*) FROM students;
```

```
COUNT(*)
3
```

```sql
SELECT AVG(age), MIN(age), MAX(age) FROM students;
```

```
AVG(AGE) | MIN(AGE) | MAX(AGE)
12.0     | 11       | 13
```

| Function | Meaning |
|---|---|
| `COUNT(*)` | How many rows? |
| `AVG(age)` | The average |
| `MIN(age)` / `MAX(age)` | The smallest / biggest |
| `SUM(age)` | Add them all up |

### Nicer column names with `AS`

```sql
SELECT COUNT(*) AS total, AVG(age) AS average_age FROM students;
```

```
TOTAL | AVERAGE_AGE
3     | 12.0
```

`AS` gives a result column a **nickname**. 🏷️

### GROUP BY — count per group

"How many books does **each** author have?" That's `GROUP BY` — you'll try it in the mini project! 📚

---

## ✏️ Part 6: UPDATE — change rows

Tom has a new email:

```sql
UPDATE students SET email = 'tom.brown@school.com' WHERE id = 2;
```

```
Update count: 1
```

Check:

```sql
SELECT * FROM students WHERE id = 2;
```

```
ID | NAME      | EMAIL                | AGE
2  | Tom Brown | tom.brown@school.com | 13
```

| Code | Meaning |
|---|---|
| `UPDATE students` | "Change rows in `students`..." |
| `SET email = '...'` | "...set this column to this value..." (several: `SET email = '...', age = 14`) |
| `WHERE id = 2` | ⭐ "...but **only** in the row(s) where `id` is 2." |

### ⚠️⚠️⚠️ The most dangerous mistake in SQL

What happens if you **forget** the `WHERE`? 😱 We tried it on a practice table of books:

```sql
UPDATE books SET published = 2000;
```

```
Update count: 3
```

**Every** book now says it was published in 2000! 😱 There's **no** "undo" button. In a real company, this could change **millions** of rows in one second. 💥

**Golden rule:** 🥇 Before you run an `UPDATE` or `DELETE`, **always** check that it has a `WHERE`. Even better: first run a `SELECT` with the **same** `WHERE`, to see which rows will be changed.

---

## 🗑️ Part 7: DELETE — remove rows

Lina moves to another school:

```sql
DELETE FROM students WHERE id = 3;
```

```
Update count: 1
```

```sql
SELECT * FROM students;
```

```
ID | NAME       | EMAIL                | AGE
1  | Sara Ahmed | sara@school.com      | 12
2  | Tom Brown  | tom.brown@school.com | 13
(2 rows)
```

And the same warning: **`DELETE FROM students;`** without a `WHERE` removes **all** students. 😱🗑️ Always use a `WHERE`!

---

## 🛡️ Part 8: The database protects your data

Remember the rules (constraints) from `CREATE TABLE`? Let's try to **break** them. The database says **no**! These are real messages:

### Rule 1: PRIMARY KEY — no duplicate ids

```sql
INSERT INTO students (id, name, email, age) VALUES (1, 'Omar Ali', 'omar@school.com', 12);
```

```
Unique index or primary key violation: "PUBLIC.CONSTRAINT_9 PRIMARY KEY ON PUBLIC.STUDENTS(ID) ( /* key:0 */ CAST(1 AS BIGINT), 'Sara Ahmed', 'sara@school.com', 12)"
```

"There's already a row with id 1 — Sara!" 🔑

### Rule 2: NOT NULL — the name is required

```sql
INSERT INTO students (id, name, email, age) VALUES (4, NULL, 'omar@school.com', 12);
```

```
NULL not allowed for column "NAME"
```

### Rule 3: UNIQUE — no duplicate emails

```sql
INSERT INTO students (id, name, email, age) VALUES (4, 'Omar Ali', 'sara@school.com', 12);
```

```
Unique index or primary key violation: "PUBLIC.CONSTRAINT_9E INDEX PUBLIC.CONSTRAINT_INDEX_9 ON PUBLIC.STUDENTS(EMAIL NULLS FIRST) VALUES ( /* 1 */ 'sara@school.com' )"
```

"That email is already used!" 📧 Remember our **409 Conflict** rule from Chapter 63? The database can check it too — as a **second** safety net. 🛡️🛡️

### And a typo

```sql
SELEKT * FROM students;
```

```
Syntax error in SQL statement "[*]SELEKT * FROM students"
```

The `[*]` shows **where** H2 got confused. 🔍

> 💡 **Why is this good?** Your Java code has bugs sometimes (everyone's does! 🐛). The database is the **last guard** 💂: even if your code tries to save bad data, the database refuses.

---

## 🔢 Part 9: Let the database choose the id

Writing ids by hand (`1`, `2`, `3`) is annoying — and dangerous (which number is free?). Databases can create them **automatically**:

```sql
CREATE TABLE books (
    id        BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    title     VARCHAR(100) NOT NULL,
    author    VARCHAR(50)  NOT NULL,
    published INT
);
```

| Code | Meaning |
|---|---|
| `GENERATED BY DEFAULT AS IDENTITY` | ⭐ "If no id is given, the database **creates** the next number: 1, 2, 3..." 🔢 |

Now insert **without** an id:

```sql
INSERT INTO books (title, author, published) VALUES ('Matilda', 'Roald Dahl', 1988);
```

The database gives it id **1**, the next one **2**, and so on. This is **exactly** what Spring will use in Chapter 71! 🎉

> ⚠️ **Why `published` and not `year`?** We tried `year INT` first, and H2 said: `Syntax error ... [*]year INT ... expected "identifier"`. 😮 **`YEAR` is a reserved word** in H2 (a word with a special meaning, like `class` in Java). Avoid names like `year`, `order`, `user`, `value`, `key` for columns — or you'll get strange errors. Remember this in Chapter 71! 🧠

---

## 💻 Mini project: The library in SQL 📚

Use the `books` table from Part 9. Then:

1. Add 4 books **in one** `INSERT`: Matilda (Roald Dahl, 1988), The Hobbit (J.R.R. Tolkien, 1937), Charlotte's Web (E.B. White, 1952), The BFG (Roald Dahl, 1982).
2. Show all books.
3. Show the **titles and years** of books published **before 1960**, oldest first.
4. **How many** books did Roald Dahl write (in our table)?
5. Show **each author** with the **number** of their books. (Tip: `GROUP BY author`.)
6. Change Matilda's year to **1990**.
7. Delete The Hobbit (use its **id**).
8. Show all books, sorted by title.

<details>
<summary>Click to see the answer</summary>

```sql
-- 1.
INSERT INTO books (title, author, published) VALUES
    ('Matilda', 'Roald Dahl', 1988),
    ('The Hobbit', 'J.R.R. Tolkien', 1937),
    ('Charlotte''s Web', 'E.B. White', 1952),
    ('The BFG', 'Roald Dahl', 1982);

-- 2.
SELECT * FROM books;
```

```
ID | TITLE           | AUTHOR         | PUBLISHED
1  | Matilda         | Roald Dahl     | 1988
2  | The Hobbit      | J.R.R. Tolkien | 1937
3  | Charlotte's Web | E.B. White     | 1952
4  | The BFG         | Roald Dahl     | 1982
```

(See the ids? The database created them! 🔢)

```sql
-- 3.
SELECT title, published FROM books WHERE published < 1960 ORDER BY published;
```

```
TITLE           | PUBLISHED
The Hobbit      | 1937
Charlotte's Web | 1952
```

```sql
-- 4.
SELECT COUNT(*) FROM books WHERE author = 'Roald Dahl';
```

```
COUNT(*)
2
```

```sql
-- 5.
SELECT author, COUNT(*) AS books FROM books GROUP BY author ORDER BY author;
```

```
AUTHOR         | BOOKS
E.B. White     | 1
J.R.R. Tolkien | 1
Roald Dahl     | 2
```

`GROUP BY author` makes a **group** for each author, and `COUNT(*)` counts the rows **in each group**. 📦📦📦

```sql
-- 6.
UPDATE books SET published = 1990 WHERE title = 'Matilda';

-- 7.
DELETE FROM books WHERE id = 2;

-- 8.
SELECT * FROM books ORDER BY title;
```

```
ID | TITLE           | AUTHOR     | PUBLISHED
3  | Charlotte's Web | E.B. White | 1952
1  | Matilda         | Roald Dahl | 1990
4  | The BFG         | Roald Dahl | 1982
```

(All these results are real — we ran every statement in H2. ✅)

</details>

---

## ✋ Try it yourself

**Task 1:** Write a query: students whose email ends with `@school.com` **and** who are younger than 13.

<details>
<summary>Click to see the answer</summary>

```sql
SELECT * FROM students WHERE email LIKE '%@school.com' AND age < 13;
```

</details>

**Task 2:** What does this do? `SELECT name FROM students WHERE age IN (11, 13) ORDER BY name;`

<details>
<summary>Click to see the answer</summary>

It shows the **names** of students who are **11 or 13** years old, sorted A → Z.

</details>

**Task 3:** Find the mistakes:

```sql
SELECT * FROM students WHERE name = "Sara Ahmed"
UPDATE students SET age = 13
```

<details>
<summary>Click to see the answer</summary>

1. `"Sara Ahmed"` must be in **single** quotes: `'Sara Ahmed'` (double quotes mean a column name). Also, a `;` is missing at the end.
2. The `UPDATE` has **no `WHERE`** — it changes **every** student to 13! 😱 Add `WHERE id = ...`. (And a `;`.)

</details>

**Task 4:** Create a table `courses` with an automatic `id`, a `title` (required, unique, max 50 characters) and `hours` (a number). Add "Math" (5 hours) and "Art" (2 hours).

<details>
<summary>Click to see the answer</summary>

```sql
CREATE TABLE courses (
    id    BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    title VARCHAR(50) NOT NULL UNIQUE,
    hours INT
);

INSERT INTO courses (title, hours) VALUES ('Math', 5), ('Art', 2);
```

</details>

---

## ⚠️ Common mistakes

### Mistake 1: `UPDATE` or `DELETE` without `WHERE`

Changes or deletes **every** row. 😱 **Fix:** Always write `WHERE`. Test it first with a `SELECT ... WHERE ...`.

### Mistake 2: Double quotes for text

`"Sara"` → `Column "Sara" not found`. **Fix:** `'Sara'` (single quotes).

### Mistake 3: `= NULL`

`WHERE age = NULL` finds **nothing**, ever. **Fix:** `WHERE age IS NULL`.

### Mistake 4: Expecting an order without `ORDER BY`

The database may return rows in **any** order. **Fix:** `ORDER BY ...` whenever the order matters.

### Mistake 5: Reserved words as names

`year`, `order`, `user`, `group`, `value`... → strange syntax errors. **Fix:** Choose other names: `published`, `order_date`, `app_user`...

### Mistake 6: "Database not found" in the H2 Console

You started the console **without** `-ifNotExists`, and it says: `Database "..." not found, either pre-create it or allow remote database creation`. **Fix:** Start it with `-ifNotExists` (Part 1).

---

## ✅ Summary

- **SQL** is the language of relational databases. Keywords in CAPITALS, text in `'single quotes'`, `;` at the end.
- **H2 Console:** `java -cp h2-2.4.240.jar org.h2.tools.Server -web -ifNotExists -browser`, URL `jdbc:h2:~/sql-practice`, user `sa`.
- **`CREATE TABLE`** with column types and rules: `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, and `GENERATED BY DEFAULT AS IDENTITY` for automatic ids.
- **`INSERT INTO ... (columns) VALUES (...)`** adds rows.
- **`SELECT columns FROM table WHERE ... ORDER BY ...`** finds rows. `*` = all columns. `LIKE '%a%'` searches in text.
- **`COUNT`, `AVG`, `MIN`, `MAX`, `SUM`** + **`GROUP BY`** count and calculate. **`AS`** renames result columns.
- **`UPDATE ... SET ... WHERE ...`** changes rows, **`DELETE FROM ... WHERE ...`** removes rows. ⚠️ **Never forget the `WHERE`!**
- The database **refuses** bad data (duplicate keys, missing required values) — a second safety net. 🛡️
- Avoid **reserved words** like `year` as names.

---

## ❓ Quiz

1. What does SQL stand for?
2. Write a statement that shows only the names of all students.
3. What does `WHERE` do?
4. Which students does `WHERE name LIKE 'T%'` find?
5. How do you sort from the biggest to the smallest age?
6. What happens if you run `DELETE FROM students;`?
7. What does `NOT NULL` mean? What does `UNIQUE` mean?
8. How can the database create ids automatically?
9. Why does `WHERE age = NULL` never find anything?
10. Why did `year INT` give an error in H2?

<details>
<summary>Click to see the answers</summary>

1. **S**tructured **Q**uery **L**anguage.
2. `SELECT name FROM students;`
3. It keeps only the rows that match a condition (a filter).
4. Students whose name **starts** with `T` (like Tom Brown).
5. `ORDER BY age DESC`
6. **All** students are deleted! (No `WHERE`.)
7. `NOT NULL`: the column must always have a value. `UNIQUE`: no two rows may have the same value in this column.
8. With `GENERATED BY DEFAULT AS IDENTITY` on the id column.
9. In SQL, nothing is "equal" to `NULL`. You must write `IS NULL`.
10. `YEAR` is a **reserved word** in H2 — it has a special meaning, so it can't be used as a column name.

</details>

---

[⬅ Previous chapter](67-what-is-a-database.md) | [Table of Contents](../README.md) | [Next chapter: H2: a small database for learning ➡](69-h2-database.md)
