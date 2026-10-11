# Chapter 74 – Your own queries

[⬅ Previous chapter](73-crud-student-app.md) | [Table of Contents](../README.md) | [Next chapter ➡](75-one-to-many.md)

---

## 🎯 Goal

`findAll` and `findById` are great. But real apps ask **more** questions: "Which students are 12 or older?", "Who has this email?", "Who are the 2 oldest?" 🤔

At the end of this chapter you will know:

- How to write **query methods** that Spring Data understands **just by their name** 🧞: `findByAgeGreaterThanEqual(...)`
- The **grammar** of method names: `findBy`, `existsBy`, `countBy`, `And`, `Between`, `Containing`, `IgnoreCase`, `OrderBy`, `Top`...
- How to write your own **JPQL** queries with **`@Query`** ✍️
- How to write **native SQL** when you really need it
- How to use the new queries in the **filters** of our API (Chapter 59 is back! 🔍)
- What happens when you **misspell** a method name

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Query method** / **derived query** | A repository method whose **name** describes the query. Spring Data "derives" (works out) the SQL from the name. |
| **Property** | A field of the entity: `name`, `age`, `email`... |
| **JPQL** | **J**ava **P**ersistence **Q**uery **L**anguage: like SQL, but with **class and field names** instead of table and column names. |
| **`@Query`** | A label to write your **own** JPQL (or SQL) for a repository method. |
| **Native query** | A query in **real SQL** for your database, written by you. |
| **Named parameter** | A placeholder with a name, like `:minAge`. |

---

## 📖 Story: Ordering from a menu with a very exact waiter 🍽️

In a magical restaurant, you **don't** explain to the cook how to make the food. You just say the **name** of the dish, and it appears:

- "**Pizza with cheese and mushrooms**" 🍕 → a pizza with cheese and mushrooms.
- "**Pizza with cheese, no onions, big**" → exactly that.

But the waiter is **very** exact: if you say "Pizza with **chese**" 😅, he says: "I don't know 'chese'. Did you mean '**cheese**'?"

Spring Data is that waiter. 🧞 You write a method **name**:

```java
List<Student> findByAgeGreaterThanEqual(int age);
```

...and Spring Data reads it like a sentence: "**find** students **by age greater than or equal** to this number" — and writes the SQL for you.

---

## 🧞 Part 1: Query methods — the name is the query

Add these methods to **`StudentRepository`**:

```java
package com.example.school.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.school.entity.Student;

public interface StudentRepository extends JpaRepository<Student, Long> {

    boolean existsByEmailIgnoreCase(String email);

    Optional<Student> findByEmailIgnoreCase(String email);

    List<Student> findByAgeGreaterThanEqual(int age);

    List<Student> findByNameContainingIgnoreCase(String text);

    List<Student> findByAgeGreaterThanEqualAndNameContainingIgnoreCase(int age, String text);

    List<Student> findByAgeBetweenOrderByNameAsc(int min, int max);

    long countByAge(int age);

    List<Student> findTop2ByOrderByAgeDesc();
}
```

No code, only names. 🤯 Let's read them like sentences:

| Method name | Read it as... |
|---|---|
| `existsByEmailIgnoreCase(email)` | "Is there a student whose **email** equals this, ignoring big/small letters?" → `boolean` |
| `findByEmailIgnoreCase(email)` | "Find **the** student with this email (any letters)." → `Optional<Student>` (maybe none) |
| `findByAgeGreaterThanEqual(age)` | "Find students whose **age ≥** this number." → `List<Student>` |
| `findByNameContainingIgnoreCase(text)` | "Find students whose **name contains** this text." |
| `findByAgeGreaterThanEqualAndNameContainingIgnoreCase(age, text)` | "...age ≥ X **and** name contains Y." (Long, but very clear! 😅) |
| `findByAgeBetweenOrderByNameAsc(min, max)` | "...age **between** min and max, **sorted by name** A→Z." |
| `countByAge(age)` | "**How many** students are exactly this age?" → `long` |
| `findTop2ByOrderByAgeDesc()` | "The **top 2**, sorted by age, oldest first." |

### 📜 The grammar

A query method name is built from **pieces**:

```
 find  Top2  By  Age  GreaterThanEqual  And  Name  Containing  IgnoreCase  OrderBy  Name  Asc
 └┬─┘  └┬─┘  └┬┘ └┬┘  └──────┬──────┘  └┬┘  └┬─┘  └───┬────┘  └───┬────┘  └──┬──┘  └┬─┘  └┬┘
 what  how   "by" field   comparison    and  field  comparison   option    sorting  field  direction
       many
```

| Piece | Choices |
|---|---|
| **What** | `find...By` (rows), `exists...By` (`boolean`), `count...By` (a number), `delete...By` |
| **How many** (optional) | `First`, `Top2`, `Top10`... |
| **Field** | Any **property** of the entity — the **Java** name (`age`, `name`, `teacherNote`)! |
| **Comparison** | (nothing) = equal, `Not`, `GreaterThan`, `GreaterThanEqual`, `LessThan`, `LessThanEqual`, `Between`, `In`, `IsNull`, `IsNotNull`, `True`, `False`, `Containing`, `StartingWith`, `EndingWith`, `Like` |
| **Option** | `IgnoreCase` |
| **Combine** | `And`, `Or` |
| **Sorting** | `OrderBy` + field + `Asc` / `Desc` |

**Parameters** come in the **same order** as the fields in the name: `findByAgeGreaterThanEqualAndNameContainingIgnoreCase(int age, String text)` → first the age, then the text.

> 💡 IntelliJ **Ultimate** suggests these names while you type. In the free version, you just type them carefully — and Spring checks them at startup (Part 5). 👀

---

## 👀 Part 2: The SQL Spring Data writes

We tried the queries and looked at the log. These are **real** SQL statements Hibernate wrote **from the names**:

**`findByAgeGreaterThanEqual(12)`**

```sql
select s1_0.id, s1_0.age, s1_0.created_at, s1_0.email, s1_0.name, s1_0.teacher_note
from students s1_0
where s1_0.age>=?
```

**`findByNameContainingIgnoreCase("BR")`**

```sql
... where upper(s1_0.name) like upper(?) escape '\'
```

`Containing` → `LIKE '%...%'` (Spring adds the `%` around your text), and `IgnoreCase` → `upper(...)` on **both** sides. Smart! 🧠

**`findByEmailIgnoreCase("TOM@school.com")`**

```sql
... where upper(s1_0.email)=upper(?)
```

**`findByAgeBetweenOrderByNameAsc(11, 12)`**

```sql
... where s1_0.age between ? and ?
order by s1_0.name
```

→ `Lina Haddad 11`, `Sara Ahmed 12`.

**`countByAge(12)`**

```sql
select count(s1_0.id) from students s1_0 where s1_0.age=?
```

→ `1`

**`findTop2ByOrderByAgeDesc()`**

```sql
... order by s1_0.age desc
fetch first ? rows only
```

`Top2` → `fetch first 2 rows only` (H2's way of saying "only 2 rows"). 🥇🥈

---

## 🔍 Part 3: Use them in the API — filters are back!

In Chapter 63, we left out the **filters** (`?minAge=12&name=a`). Now the **database** can do the filtering — much faster than Java streams for big tables! ⚡

**`StudentService`** — a new `getAll` and a few new methods:

```java
public List<StudentResponse> getAll(Integer minAge, String name) {
    List<Student> students;
    if (minAge != null && name != null) {
        students = studentRepository.findByAgeGreaterThanEqualAndNameContainingIgnoreCase(minAge, name);
    } else if (minAge != null) {
        students = studentRepository.findByAgeGreaterThanEqual(minAge);
    } else if (name != null) {
        students = studentRepository.findByNameContainingIgnoreCase(name);
    } else {
        students = studentRepository.findAll();
    }
    return students.stream()
            .map(StudentResponse::from)
            .toList();
}

public StudentResponse findByEmail(String email) {
    return studentRepository.findByEmailIgnoreCase(email)
            .map(StudentResponse::from)
            .orElseThrow(() -> new StudentNotFoundException(email));
}

public List<StudentResponse> getOldest() {
    return studentRepository.findTop2ByOrderByAgeDesc().stream()
            .map(StudentResponse::from)
            .toList();
}
```

| Code | Meaning |
|---|---|
| `if (minAge != null && name != null)` | Both filters → the long "And" method. |
| `else if (minAge != null)` | Only the age filter. |
| `else if (name != null)` | Only the name filter. |
| `else` | No filters → all students. |
| `.map(StudentResponse::from)` on an `Optional` | If found, turn the entity into a DTO (Chapter 37). |
| `new StudentNotFoundException(email)` | A **second constructor** for our exception (below). |

Add the second constructor to **`StudentNotFoundException`**:

```java
public StudentNotFoundException(String email) {
    super("Student with email " + email + " was not found");
}
```

(Two constructors with different parameter types — **overloading**, Chapter 19!)

**`StudentController`** — the filters and two new endpoints:

```java
@GetMapping
public List<StudentResponse> getAll(@RequestParam(required = false) Integer minAge,
                                    @RequestParam(required = false) String name) {
    return studentService.getAll(minAge, name);
}

@GetMapping("/search")
public StudentResponse findByEmail(@RequestParam String email) {
    return studentService.findByEmail(email);
}

@GetMapping("/oldest")
public List<StudentResponse> getOldest() {
    return studentService.getOldest();
}
```

(Import `org.springframework.web.bind.annotation.RequestParam`.)

### ✅ Test it

Real answers (with a fresh database: Sara 12, Tom 13, Lina 11):

| Request | Answer |
|---|---|
| `GET /api/students?minAge=12` | Sara and Tom |
| `GET /api/students?name=BR` | Tom **Br**own |
| `GET /api/students?minAge=12&name=a` | Sara (Lina has an "a" but is 11; Tom has no "a") |
| `GET /api/students/search?email=TOM@school.com` | Tom ✅ (ignoring big/small letters) |
| `GET /api/students/search?email=x@y.z` | **404** `Student with email x@y.z was not found` |
| `GET /api/students/oldest` | Tom (13), Sara (12) |

For example, `GET /api/students?minAge=12&name=a`:

```json
[{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12}]
```

---

## ✍️ Part 4: Your own queries with `@Query`

Method names are great for **simple** questions. For harder ones (or when the name gets **way** too long 😵), write the query **yourself** with **`@Query`**.

### JPQL — queries with Java names

```java
@Query("SELECT s FROM Student s WHERE s.age >= :minAge ORDER BY s.name")
List<Student> findOlderStudents(int minAge);

@Query("SELECT AVG(s.age) FROM Student s")
Double averageAge();
```

(Import `org.springframework.data.jpa.repository.Query`.)

| Code | Meaning |
|---|---|
| `@Query("...")` | "Don't guess from the name — use **this** query." The method name can be anything you like. |
| `SELECT s FROM Student s` | ⭐ **JPQL**: `Student` is the **class** name (not the table `students`!), and `s` is a short nickname for "a student". |
| `WHERE s.age >= :minAge` | `s.age` is the **field** (not the column). **`:minAge`** is a **named parameter**... |
| `int minAge` | ...filled from the method parameter with the **same name**. 🔗 |
| `ORDER BY s.name` | Sorted by name. |
| `SELECT AVG(s.age) FROM Student s` | JPQL has `COUNT`, `AVG`, `MIN`, `MAX`, `SUM` too (Chapter 68). |
| `Double averageAge()` | `Double` (not `double`) — the average of an **empty** table is `null`! |

Real SQL that Hibernate made from the JPQL:

```sql
select s1_0.id, ... from students s1_0
where s1_0.age>=?
order by s1_0.name
```

→ `Sara Ahmed`, `Tom Brown`. And `averageAge()` → `12.0`.

> 💡 **JPQL vs SQL:** JPQL looks like SQL, but talks about **classes and fields**. Hibernate translates it into the right SQL for **your** database (H2, PostgreSQL, MySQL...). That's why your queries keep working when you switch databases in Chapter 77! 🔌

> 💡 **`:minAge` and the parameter name:** Spring Boot compiles your code so that parameter names are kept, so `:minAge` finds `int minAge` automatically. In older projects, you'll see `@Param("minAge") int minAge` — the same thing, written out.

### Native SQL — when you really need it

Sometimes you need a feature of **your** database that JPQL doesn't have. Then write **real SQL** with `nativeQuery = true`:

```java
@Query(value = "SELECT * FROM students WHERE email LIKE CONCAT('%@', :domain)", nativeQuery = true)
List<Student> findByEmailDomain(String domain);
```

| Code | Meaning |
|---|---|
| `value = "SELECT * FROM students ..."` | Real SQL: the **table** `students` and **column** names. |
| `nativeQuery = true` | "This is **real** SQL — send it as it is." |
| `CONCAT('%@', :domain)` | Builds the text `%@school.com` (from Chapter 68's `LIKE`). |

`findByEmailDomain("school.com")` → all 3 students. ✅

> ⚠️ Native SQL is tied to **one** database. If you switch from H2 to PostgreSQL, you might have to change it. **Prefer** query methods and JPQL. Use native SQL only when you must.

### 🤔 Which one should I use?

| Situation | Use |
|---|---|
| Simple: 1–2 conditions, sorting | **Query method** (just a name) 🧞 |
| The name would be **super long**, or you need `AVG`, special joins... | **`@Query` with JPQL** ✍️ |
| You need a special feature of your database | **Native query** (rarely!) |

---

## 💥 Part 5: Misspelled names — caught at startup!

What if you make a typo, like `agee` instead of `age`?

```java
List<Student> findByAgee(int age);   // ❌ typo!
```

The app **doesn't start**. We tested it:

```
Caused by: org.springframework.data.repository.query.QueryCreationException: Cannot create query for method [StudentRepository.findByAgee(int)]; No property 'agee' found for type 'Student'; Did you mean 'age'
```

"**No property 'agee' found for type 'Student'; Did you mean 'age'**" — Spring even suggests the fix! 🤓

This is a **good** thing: you find the mistake **at startup**, not when a user calls the endpoint. (Remember the JDBC typo in Chapter 70? That one was found only when the code **ran**. 😬)

---

## 💻 Mini project: Book queries 📚

Add these to **`BookRepository`**, and use them:

1. `findByAuthorContainingIgnoreCase(String text)` — books whose author contains a text.
2. `findByYearLessThanOrderByYearAsc(int year)` — books published **before** a year, oldest first. (Remember: the **field** is `year`, even if the column is `published`!)
3. `long countByAuthorIgnoreCase(String author)` — how many books by one author?
4. A **JPQL** query `findOldestBook()` that returns the book with the **smallest** year. (Tip: `ORDER BY b.year` and... `findFirstBy`? Or JPQL with `LIMIT 1`?) Try the **query method** way: `Optional<Book> findFirstByOrderByYearAsc();`

Then add **`GET /api/books?author=dahl&before=1990`** (one or both parameters).

<details>
<summary>Click to see the answer</summary>

```java
package com.example.school.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.school.entity.Book;

public interface BookRepository extends JpaRepository<Book, Long> {

    List<Book> findByAuthorContainingIgnoreCase(String text);

    List<Book> findByYearLessThanOrderByYearAsc(int year);

    List<Book> findByAuthorContainingIgnoreCaseAndYearLessThan(String text, int year);

    long countByAuthorIgnoreCase(String author);

    Optional<Book> findFirstByOrderByYearAsc();
}
```

In **`BookService`**:

```java
public List<BookResponse> getAll(String author, Integer before) {
    List<Book> books;
    if (author != null && before != null) {
        books = bookRepository.findByAuthorContainingIgnoreCaseAndYearLessThan(author, before);
    } else if (author != null) {
        books = bookRepository.findByAuthorContainingIgnoreCase(author);
    } else if (before != null) {
        books = bookRepository.findByYearLessThanOrderByYearAsc(before);
    } else {
        books = bookRepository.findAll();
    }
    return books.stream()
            .map(BookResponse::from)
            .toList();
}
```

In **`BookController`**:

```java
@GetMapping
public List<BookResponse> getAll(@RequestParam(required = false) String author,
                                 @RequestParam(required = false) Integer before) {
    return bookService.getAll(author, before);
}
```

Test (with the 3 starting books):

- `GET /api/books?author=dahl` → Matilda
- `GET /api/books?before=1960` → The Hobbit (1937), Charlotte's Web (1952)
- `GET /api/books?author=dahl&before=1980` → `[]` (Matilda is from 1988)
- `countByAuthorIgnoreCase("roald dahl")` → `1`
- `findFirstByOrderByYearAsc()` → The Hobbit

Notice: the **query method** uses the **field** name `year` — Spring Data and Hibernate know that it lives in the column `published`. You never write `published` in Java! 😎

</details>

---

## ✋ Try it yourself

**Task 1:** Write query methods for:

a) students whose name **starts with** a text (ignore case)
b) students **younger than** an age, sorted by age
c) **delete** all students of a certain age
d) does a student with this **name** exist?

<details>
<summary>Click to see the answer</summary>

a) `List<Student> findByNameStartingWithIgnoreCase(String start);`
b) `List<Student> findByAgeLessThanOrderByAgeAsc(int age);`
c) `void deleteByAge(int age);` (needs a transaction to run — Chapter 79!)
d) `boolean existsByName(String name);`

</details>

**Task 2:** Turn this query method into a JPQL `@Query`: `List<Student> findByAgeBetweenOrderByNameAsc(int min, int max);`

<details>
<summary>Click to see the answer</summary>

```java
@Query("SELECT s FROM Student s WHERE s.age BETWEEN :min AND :max ORDER BY s.name ASC")
List<Student> findInAgeRange(int min, int max);
```

</details>

**Task 3:** What's wrong with this JPQL? `SELECT * FROM students WHERE age > :age`

<details>
<summary>Click to see the answer</summary>

That's **SQL**, not JPQL! In JPQL: use the **class** name `Student` (not `students`), give it a nickname, and select the nickname: `SELECT s FROM Student s WHERE s.age > :age`. (Or add `nativeQuery = true` to use it as real SQL.)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Column names in method names

`findByTeacher_note(...)` or `findByPublished(...)` ❌ — query methods use **Java field names**: `findByTeacherNote(...)`, `findByYear(...)`. ✅

### Mistake 2: Typos in method names

The app doesn't start: `No property 'agee' found for type 'Student'; Did you mean 'age'`. **Fix:** Read the message — it often tells you the right name! 🤓

### Mistake 3: Parameters in the wrong order

```java
List<Student> findByAgeGreaterThanEqualAndNameContainingIgnoreCase(String text, int age);   // ❌
```

The **first** field in the name (`Age`) gets the **first** parameter. Here, Java would put a `String` into the age... and Spring complains. **Fix:** Same order as in the name.

### Mistake 4: Table names in JPQL

`@Query("SELECT s FROM students s")` → an error at startup: JPQL doesn't know `students`. **Fix:** Use the **class** name: `FROM Student s`.

### Mistake 5: `double` for an average

`double averageAge()` crashes when the table is **empty** (the average is `null`). **Fix:** `Double`.

---

## ✅ Summary

- **Query methods**: the **name** is the query 🧞 — `findBy...`, `existsBy...`, `countBy...`, `deleteBy...`, with fields (Java names!), comparisons (`GreaterThanEqual`, `Between`, `Containing`, `In`...), `IgnoreCase`, `And`/`Or`, `OrderBy...Asc/Desc`, `Top2`/`First`.
- Return types: `List<...>` (many), `Optional<...>` (zero or one), `boolean` (exists), `long` (count).
- Spring Data **checks** the names at startup — typos are found early (with a "Did you mean...?" 🤓).
- **`@Query("SELECT s FROM Student s WHERE s.age >= :minAge")`** = your own **JPQL** — class and field names, named parameters (`:minAge`).
- **Native SQL** (`nativeQuery = true`) = real SQL for one database. Use it rarely.
- Our filters (`?minAge=`, `?name=`) are back — and now the **database** does the filtering. ⚡

---

## ❓ Quiz

1. What does `findByAgeGreaterThanEqual(12)` return?
2. Write a query method: students whose email ends with a text.
3. What does `IgnoreCase` add to the SQL?
4. Which return type do you use when there may be **zero or one** result?
5. What's the difference between JPQL and SQL?
6. What is `:minAge` in a `@Query`?
7. What happens if you misspell a field in a method name?
8. When would you use a native query?

<details>
<summary>Click to see the answers</summary>

1. A `List<Student>` with all students aged 12 or older.
2. `List<Student> findByEmailEndingWith(String end);`
3. `upper(...)` around the column and the value, so big/small letters don't matter.
4. `Optional<Student>`
5. JPQL uses **class** and **field** names (`Student`, `s.age`); SQL uses **table** and **column** names (`students`, `age`). Hibernate translates JPQL into SQL for your database.
6. A **named parameter** — it's filled with the method parameter that has the same name.
7. The app doesn't start: "No property '...' found for type 'Student'" (often with "Did you mean ...?").
8. Only when you need a special feature of your database that query methods and JPQL can't do.

</details>

---

[⬅ Previous chapter](73-crud-student-app.md) | [Table of Contents](../README.md) | [Next chapter: Relationships: One-to-Many ➡](75-one-to-many.md)
