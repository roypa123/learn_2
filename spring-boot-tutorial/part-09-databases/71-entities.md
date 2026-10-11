# Chapter 71 – Entities: Java classes that become tables

[⬅ Previous chapter](70-spring-data-jpa.md) | [Table of Contents](../README.md) | [Next chapter ➡](72-repositories.md)

---

## 🎯 Goal

Time to meet the translator! 🗣️ Today you'll write your first **entity**: a Java class that **is** a database table.

At the end of this chapter you will know:

- What an **entity** is, and the labels that make one: **`@Entity`**, **`@Table`**, **`@Id`**, **`@GeneratedValue`**, **`@Column`**
- Why entities are **classes** (not records)
- How **Hibernate creates the table** for you (and the `ddl-auto` setting) 🏗️
- How to **see** the SQL Hibernate writes (`show-sql`) 👀
- How Java names become table and column names (`teacherNote` → `teacher_note`)
- How to fill the new table with `data.sql`

> 🌱 Our API keeps using its old map for one more chapter. In Chapter 72 we add the repository, and in Chapter 73 we connect everything. 🔗

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Entity** | A Java class whose objects are **saved as rows** in a table. 🧱↔📊 |
| **`@Entity`** | The label that says: "This class is an entity." |
| **`@Table`** | Chooses the **table name**. |
| **`@Id`** | Marks the **primary key** field. 🔑 |
| **`@GeneratedValue`** | "The **database** creates this value (the id) for me." |
| **`@Column`** | Settings for one column: name, length, required, unique... |
| **DDL** | **D**ata **D**efinition **L**anguage: SQL that **builds** tables (`CREATE TABLE`, `DROP TABLE`). |
| **`ddl-auto`** | A setting: should Hibernate build the tables **automatically**? |
| **Snake case** | Names with `_` between words: `teacher_note`. 🐍 (Java uses **camel case**: `teacherNote` 🐫.) |

---

## 📖 Story: The cookie cutter, again 🍪

Remember **Chapter 18**? A **class** is a cookie cutter, and **objects** are the cookies. 🍪

Now imagine a **cookie box** with numbered spaces 📦: every cookie you make goes into the next space, and stays there.

- The **cookie cutter** = the entity **class** `Student`
- The **box** = the **table** `students`
- Each **cookie** = an object = a **row**
- The **number** on each space = the **id** 🔑

With **one** label (`@Entity`) on the cookie cutter, Hibernate builds the box **for** you, with exactly the right spaces. 📦✨

---

## 🧹 Part 1: First, make room — rename the old record

We'll create a new class called `Student` (in a new package). But our Part 8 code already has a **record** `model.Student`. Two classes with the same name are confusing! 😵 Let's rename the old one first.

1. Open **`model/Student.java`** (the record).
2. Click on the name `Student` (after `record`) and press **Shift + F6** (Rename).
3. Type **`OldStudent`** and press **Enter**.

IntelliJ renames the record **and** changes every place that uses it (the service, the repository, `StudentResponse`...). ✨ Run the app — the API still works exactly like before. ✅

(Like the old **`StudentRepository`**, the **`OldStudent`** record will be **deleted** in Chapter 73, when the new code is ready. 🧹)

---

## 🧱 Part 2: The `Student` entity

Create a new package **`com.example.school.entity`**, and inside it, a **class** (not a record!) **`Student`**:

```java
package com.example.school.entity;

import java.time.LocalDateTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "students")
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 50)
    private String name;

    @Column(nullable = false, unique = true, length = 100)
    private String email;

    private int age;

    private String teacherNote;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    protected Student() {
    }

    public Student(String name, String email, int age) {
        this.name = name;
        this.email = email;
        this.age = age;
        this.teacherNote = "";
        this.createdAt = LocalDateTime.now();
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getTeacherNote() {
        return teacherNote;
    }

    public void setTeacherNote(String teacherNote) {
        this.teacherNote = teacherNote;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
}
```

> 💡 **Tip:** You don't have to type all the getters and setters! In IntelliJ, put the cursor inside the class, press **Alt + Insert** → **Getter and Setter** → choose the fields. ✨ (Then delete the setters you don't want, like `setId` and `setCreatedAt`.)

### 🔍 Line by line — the labels

| Code | Meaning |
|---|---|
| `import jakarta.persistence...` | The JPA labels come from **Jakarta Persistence** (the JPA standard — Chapter 70). |
| `@Entity` | ⭐ "This class is an **entity**: save its objects as rows." |
| `@Table(name = "students")` | The table is called `students` (plural, like our REST paths). Without it, the table would be called `student`. |
| `@Id` | ⭐ The `id` field is the **primary key** 🔑. Every entity **must** have one! |
| `@GeneratedValue(strategy = GenerationType.IDENTITY)` | ⭐ "The **database** creates the id" — with `GENERATED BY DEFAULT AS IDENTITY` (Chapter 68!). |
| `private Long id;` | `Long`, so a **new** student can have `id = null` ("not saved yet") — Chapter 57. |
| `@Column(nullable = false, length = 50)` | The `name` column: **required** (`NOT NULL`) and max **50** characters (`VARCHAR(50)`). |
| `@Column(nullable = false, unique = true, length = 100)` | The `email` column: required, **unique** 📧, max 100. |
| `private int age;` | No label → a normal column with **default** settings. |
| `private String teacherNote;` | No label → a column called... `teacher_note`! (Part 5.) |
| `@Column(nullable = false, updatable = false)` | `createdAt` is required, and **never** changes after the first save. |

### 🔍 Line by line — the constructors

| Code | Meaning |
|---|---|
| `protected Student() { }` | ⭐ An **empty** constructor. **JPA needs it!** When Hibernate reads a row, it first creates an **empty** object, then fills the fields. `protected` = "only for JPA (and subclasses), please don't use it yourself". |
| `public Student(String name, String email, int age)` | The constructor **we** use to create a **new** student. |
| `this.teacherNote = "";` | New students start with an empty note. |
| `this.createdAt = LocalDateTime.now();` | The **server** sets the time (Chapter 64)! ⏰ |
| *(no `id` in the constructor)* | The **database** gives the id when we save. 🔢 |

### 🔍 The getters and setters

| Code | Meaning |
|---|---|
| `getId()`, `getName()`... | Getters (Chapter 21), to **read** the fields. |
| `setName(...)`, `setEmail(...)`... | Setters, to **change** a student (for PUT and PATCH). |
| *(no `setId`, no `setCreatedAt`)* | Nobody may change the id or the creation time! 🛡️ |

---

## 🤔 Part 3: Why a class and not a record?

In Part 8, we loved **records**. Why not here? Because JPA has a few needs that records **can't** meet:

| JPA needs... | Record | Class |
|---|---|---|
| An **empty** constructor (to build an object, then fill it) | ❌ A record's constructor needs **all** values | ✅ `protected Student() {}` |
| Fields that can **change** (Hibernate fills them; PUT changes them) | ❌ Records are **unchangeable** (final fields) | ✅ normal private fields + setters |
| To **extend** your class sometimes (lazy loading — Chapter 75) | ❌ Records are `final` | ✅ |

**Rule:** 📏 **Entities** = normal **classes**. **DTOs** = **records** (Chapter 64). That's exactly how most real projects do it. 👍

---

## 🏗️ Part 4: Let Hibernate build the table

Now **delete** `src/main/resources/schema.sql`. 🗑️ We don't need it anymore — **Hibernate** will create the table from the entity!

Who decides that? The setting **`spring.jpa.hibernate.ddl-auto`**:

| Value | What Hibernate does at startup | When to use |
|---|---|---|
| `create-drop` | **Delete** the tables, **create** them new — and delete them again when the app stops | 🧪 Learning, tests (**the default for H2 in memory**) |
| `create` | Delete and create new at startup | Rarely |
| `update` | **Add** missing tables and columns; **never delete** data | 💻 Your laptop, with a file database (Chapter 73) |
| `validate` | Only **check** that the tables match the entities | 🌍 Real servers |
| `none` | Nothing | 🌍 Real servers (with other tools for the tables) |

For H2 in memory, Spring Boot uses **`create-drop`** automatically. Perfect for now! 👍

> ⚠️ **Never** use `create` or `create-drop` on a real server — they **delete all your data** at every start! 😱

### 👀 See the SQL!

Add these two lines to **`application.properties`**:

```properties
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```

| Setting | Meaning |
|---|---|
| `spring.jpa.show-sql=true` | "Print every SQL statement Hibernate sends." 👀 |
| `spring.jpa.properties.hibernate.format_sql=true` | "...and make it pretty, on several lines." |

Restart. In the log, you'll see (real output!):

```
Hibernate: 
    drop table if exists students cascade 
Hibernate: 
    create table students (
        age integer not null,
        created_at timestamp(6) not null,
        id bigint generated by default as identity,
        name varchar(50) not null,
        email varchar(100) not null unique,
        teacher_note varchar(255),
        primary key (id)
    )
```

🤯 **Hibernate wrote the `CREATE TABLE` for you** — from your Java class!

---

## 🔄 Part 5: From Java to table — the rules

Compare the entity with the SQL Hibernate wrote:

| Java (entity) | SQL (table) | Why |
|---|---|---|
| `@Table(name = "students")` | `create table students` | Our chosen name |
| `@Id @GeneratedValue(IDENTITY) Long id` | `id bigint generated by default as identity` + `primary key (id)` | `Long` → `bigint`, and the database creates ids 🔢 |
| `@Column(nullable = false, length = 50) String name` | `name varchar(50) not null` | Our settings |
| `@Column(nullable = false, unique = true, length = 100) String email` | `email varchar(100) not null unique` | Our settings 📧 |
| `int age` | `age integer not null` | An `int` can't be `null` in Java, so Hibernate adds `not null` by itself! 🧠 |
| `String teacherNote` | `teacher_note varchar(255)` | ⭐ **camelCase → snake_case**, and the default text length is **255** |
| `LocalDateTime createdAt` | `created_at timestamp(6) not null` | A date+time (with microseconds) |

### 🐫 → 🐍 The naming rule

Spring Boot tells Hibernate to change Java names into **snake_case** for the database:

| Java (camelCase 🐫) | Database (snake_case 🐍) |
|---|---|
| `teacherNote` | `teacher_note` |
| `createdAt` | `created_at` |
| `classroomId` | `classroom_id` |

Both sides keep their **own** style. Nice! 😊

> 💡 Notice: the columns in the `CREATE TABLE` are in **alphabetical** order (`age`, `created_at`, `id`...), not in the order of your fields. That's fine — column order doesn't matter in SQL.

---

## 📜 Part 6: Fill the table with `data.sql`

Our old `data.sql` inserted ids by hand, and didn't know the new columns. Replace it with:

```sql
INSERT INTO students (name, email, age, teacher_note, created_at)
VALUES ('Sara Ahmed', 'sara@school.com', 12, 'Very good at math', '2026-09-01 08:00:00');
INSERT INTO students (name, email, age, teacher_note, created_at)
VALUES ('Tom Brown', 'tom@school.com', 13, 'Talks a lot in class', '2026-09-01 08:05:00');
INSERT INTO students (name, email, age, teacher_note, created_at)
VALUES ('Lina Haddad', 'lina@school.com', 11, 'Needs help with reading', '2026-09-02 09:30:00');
```

| Code | Meaning |
|---|---|
| *(no `id` column!)* | ⭐ The database creates the ids. (Part 7 explains why this matters!) |
| `teacher_note`, `created_at` | The **database** names (snake_case), because this is SQL. |
| `'2026-09-01 08:00:00'` | A timestamp as text: `year-month-day hours:minutes:seconds`. |

And add one more line to **`application.properties`**:

```properties
spring.jpa.defer-datasource-initialization=true
```

| Setting | Meaning |
|---|---|
| `spring.jpa.defer-datasource-initialization=true` | ⭐ "**Wait** with `data.sql` until **Hibernate** has created the tables." ("Defer" = do it later.) |

Why? Without it, Spring Boot runs `data.sql` **first**... when the table doesn't exist yet! We tested it:

```
Caused by: org.h2.jdbc.JdbcSQLSyntaxErrorException: Table "STUDENTS" not found (this database is empty); SQL statement:
```

"The table isn't there yet!" 😅 With the setting, the order is right:

```
 1. 🏗️ Hibernate: create table students (...)
 2. 📜 Spring Boot: data.sql → INSERT, INSERT, INSERT
```

Your **`application.properties`** now looks like this:

```properties
spring.application.name=school

# The database
spring.datasource.url=jdbc:h2:mem:school
spring.datasource.username=sa
spring.datasource.password=

# The H2 console (a web page to look inside the database)
spring.h2.console.enabled=true

# JPA / Hibernate
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.defer-datasource-initialization=true
spring.jpa.open-in-view=false
```

---

## 🖥️ Part 7: Look in the console

Restart, open **`http://localhost:8080/h2-console`** (URL `jdbc:h2:mem:school`), and run:

```sql
SELECT * FROM students;
```

Real result:

```
AGE | CREATED_AT          | ID | NAME        | EMAIL           | TEACHER_NOTE
12  | 2026-09-01 08:00:00 | 1  | Sara Ahmed  | sara@school.com | Very good at math
13  | 2026-09-01 08:05:00 | 2  | Tom Brown   | tom@school.com  | Talks a lot in class
11  | 2026-09-02 09:30:00 | 3  | Lina Haddad | lina@school.com | Needs help with reading
(3 rows)
```

✅ The table Hibernate built, with the rows from `data.sql`, and ids **1, 2, 3** made by the database. 🎉

### ⚠️ Why no ids in `data.sql`?

If `data.sql` writes ids **by hand** (`VALUES (1, 'Sara Ahmed', ...)`), the database's **id counter doesn't move**. It still thinks "the next id is **1**". Then, when your app saves a **new** student, the database gives it id **1**... which **Sara already has**! 💥 We tested this trap — the save fails:

```
Unique index or primary key violation: "PUBLIC.CONSTRAINT_9E PRIMARY KEY ON PUBLIC.STUDENTS(ID) ( /* key:1 */ ...
```

**Rule:** 📏 When the database creates the ids (`IDENTITY`), **never** write ids yourself in `data.sql`.

---

## 💻 Mini project: The `Book` entity 📚

Create an entity **`entity/Book`** for the library:

| Field | Type | Rules |
|---|---|---|
| `id` | `Long` | primary key, created by the database |
| `title` | `String` | required, max 100 |
| `author` | `String` | required, max 50 |
| `year` | `int` | ⚠️ the **column** must not be called `year`! (Chapter 68 — reserved word) |
| `shelf` | `String` | max 10 |

Then restart and check the log: what `CREATE TABLE` does Hibernate write?

> 💡 Hint: `@Column(name = "...")` chooses the column name. The Java **field** can still be called `year`!

<details>
<summary>Click to see the answer</summary>

```java
package com.example.school.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "books")
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String title;

    @Column(nullable = false, length = 50)
    private String author;

    @Column(name = "published")
    private int year;

    @Column(length = 10)
    private String shelf;

    protected Book() {
    }

    public Book(String title, String author, int year, String shelf) {
        this.title = title;
        this.author = author;
        this.year = year;
        this.shelf = shelf;
    }

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    public String getShelf() {
        return shelf;
    }
}
```

| Code | Meaning |
|---|---|
| `@Column(name = "published")` | ⭐ The Java field is `year`, but the **column** is `published`. Problem solved! 🎉 |

Hibernate writes (real output — the columns may come in a different order for you):

```
    create table books (
        id bigint generated by default as identity,
        author varchar(50) not null,
        shelf varchar(10),
        title varchar(100) not null,
        published integer,
        primary key (id)
    )
```

🤓 Notice: `published integer` — **without** `not null`! When you write your **own** `@Column`, its setting `nullable` (default: `true`) wins over the "an `int` is never null" rule. Want it required? Write `@Column(name = "published", nullable = false)`.

And **without** `@Column(name = "published")`? We tested it. Hibernate can't create the table — it only writes a **warning** in the log:

```
WARN ... GenerationTarget encountered exception accepting command : Error executing DDL "
    create table books ( ... [*]year integer not null, ...
```

...and then, the first time the app uses books: `Table "BOOKS" not found`. 💥 (Try it, then fix it!)

(If you still have `books` in `schema.sql`/`data.sql` from Chapter 69, delete them — Hibernate makes the table now.)

</details>

---

## ✋ Try it yourself

**Task 1:** Change `@Column(nullable = false, length = 50)` on `name` to `length = 30`. What changes in the `CREATE TABLE`?

<details>
<summary>Click to see the answer</summary>

`name varchar(30) not null`. The entity **controls** the table. (Change it back to 50.)

</details>

**Task 2:** Add a field `private boolean active = true;` (with a getter). Restart. What column appears? What's in it for the 3 students from `data.sql`?

<details>
<summary>Click to see the answer</summary>

A column `active boolean not null` (a `boolean` can't be `null`, like `int`). But `data.sql` doesn't fill it... so the `INSERT`s **fail** — the database refuses a missing value for a `not null` column! 😮 You'd have to add `active` to the `INSERT`s, or give the column a default. (Remove the field again for now.)

</details>

**Task 3:** Remove `@Table(name = "students")`. What's the table called now?

<details>
<summary>Click to see the answer</summary>

`student` — the **class** name, in snake_case. Then `data.sql` (`INSERT INTO students ...`) fails, because there's no table `students`! Put `@Table` back. 😉

</details>

---

## ⚠️ Common mistakes

### Mistake 1: No `@Id`

The app **doesn't start**. We tested it:

```
Caused by: org.hibernate.AnnotationException: Entity 'com.example.school.entity.Student' has no identifier (every '@Entity' class must declare or inherit at least one '@Id' or '@EmbeddedId' property)
```

"Every entity needs a primary key!" 🔑 **Fix:** Add `@Id` (and `@GeneratedValue`) to the id field.

### Mistake 2: No empty constructor

The app starts... but as soon as Hibernate **reads** a student, it crashes:

```
Caused by: org.hibernate.InstantiationException: No default constructor for entity 'com.example.school.entity.Student'
```

**Fix:** Add `protected Student() { }`.

### Mistake 3: `data.sql` runs too early

`Table "STUDENTS" not found (this database is empty)`. **Fix:** `spring.jpa.defer-datasource-initialization=true`.

### Mistake 4: Ids written by hand in `data.sql`

Later saves fail with a primary key violation (Part 7). **Fix:** Let the database create the ids.

### Mistake 5: A reserved word as a column name

A field called `year`, `order` or `user` → the `CREATE TABLE` fails. **Fix:** `@Column(name = "published")` (or rename the field).

### Mistake 6: Using `jakarta.persistence.Table`'s cousins by mistake

IntelliJ may suggest **other** classes with the same names, like `org.hibernate.annotations.Table`. **Fix:** Always import from **`jakarta.persistence`**.

---

## ✅ Summary

- An **entity** is a Java **class** whose objects are saved as **rows**: **`@Entity`** (+ **`@Table(name = "students")`**).
- **`@Id`** 🔑 + **`@GeneratedValue(strategy = GenerationType.IDENTITY)`**: the primary key, created by the database. Use **`Long`**.
- **`@Column(nullable = false, unique = true, length = 50)`** sets the rules. `int`/`boolean` fields are automatically `not null`.
- Entities need a **`protected` empty constructor**, private fields, getters, and setters only where changes are allowed. Entities = **classes**, DTOs = **records**.
- **Hibernate creates the tables** (`spring.jpa.hibernate.ddl-auto`; `create-drop` is the default for H2 in memory). ⚠️ Never `create`/`create-drop` on a real server.
- **`spring.jpa.show-sql=true`** + `format_sql` show the SQL. 👀
- Names: **camelCase → snake_case** (`teacherNote` → `teacher_note`).
- `data.sql` + **`spring.jpa.defer-datasource-initialization=true`**, and **no ids** by hand.
- Reserved words (`year`) → **`@Column(name = "...")`**.

---

## ❓ Quiz

1. Which label turns a class into an entity?
2. Which two labels do you put on the primary key field?
3. Why do entities need an empty constructor?
4. Why can't an entity be a record?
5. What does `ddl-auto=create-drop` do? Why is it dangerous on a real server?
6. What will the column for a field `firstName` be called?
7. Why do we need `spring.jpa.defer-datasource-initialization=true`?
8. Why shouldn't `data.sql` contain ids?
9. How can a field called `year` be saved in a column called `published`?

<details>
<summary>Click to see the answers</summary>

1. `@Entity`
2. `@Id` and `@GeneratedValue(strategy = GenerationType.IDENTITY)`
3. Because Hibernate first creates an empty object, then fills its fields from the row.
4. Records have no empty constructor, their fields can't change, and they are `final`. JPA needs all three.
5. It deletes and creates the tables at startup, and deletes them again at shutdown. On a real server, all data would be lost.
6. `first_name`
7. So `data.sql` runs **after** Hibernate has created the tables.
8. The database's id counter doesn't move for ids written by hand, so the next automatic id would clash with an existing one.
9. With `@Column(name = "published")` on the field.

</details>

---

[⬅ Previous chapter](70-spring-data-jpa.md) | [Table of Contents](../README.md) | [Next chapter: Repositories: save, find, delete ➡](72-repositories.md)
