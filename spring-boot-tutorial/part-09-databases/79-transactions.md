# Chapter 79 – Transactions: all or nothing

[⬅ Previous chapter](78-paging-sorting.md) | [Table of Contents](../README.md) | [Next chapter ➡](../part-10-security/80-spring-security.md)

---

## 🎯 Goal

Some jobs have **several steps**. What if step 1 works, but step 2 fails? 😱 Half-done jobs make **broken data**. Today you'll learn the database's superpower against that: **transactions**. 🦸

At the end of this chapter you will know:

- What a **transaction** is: **all or nothing** ✅❌
- What **commit** and **rollback** mean
- How **`@Transactional`** works in Spring
- A **real** demo: the same request **with** and **without** a transaction — and the difference in the data 🔬
- What **`readOnly = true`** does, and what **dirty checking** is 🧹
- The **traps** where `@Transactional` silently does **nothing** 🪤

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Transaction** | A group of database steps that happen **all together — or not at all**. 📦 |
| **Commit** | "Everything worked — **save** it all for real." ✅ |
| **Rollback** | "Something failed — **undo** everything in this transaction." ↩️ |
| **Atomic** | "Can't be split": all steps count as **one**. (From the Greek *atomos*, "uncuttable".) ⚛️ |
| **`@Transactional`** | Spring's label: "Run this method **inside** a transaction." |
| **Proxy** | The object Spring puts **around** your bean to start and end transactions (Chapter 72). 🎭 |
| **Dirty checking** | Hibernate notices changes to loaded entities and saves them at commit. 🧹 |
| **Checked exception** | An exception you **must** catch or declare with `throws` (Chapter 33). |

---

## 📖 Story: Paying for the school trip 🚌💰

Sara pays **€20** for the school trip. Two things must happen:

1. Take €20 **from** Sara's school account. 💸
2. Put €20 **into** the trip account. 💰

Now imagine the computer crashes **between** step 1 and step 2. 💥

- Sara's money is **gone**...
- ...but the trip account **never got it**. 😱 €20 disappeared into thin air!

That must **never** happen. The two steps must be **one** unit: **both** happen, or **neither**. That's a **transaction**:

```
 BEGIN 📦
   1. Sara's account: -20
   2. Trip account:   +20
 COMMIT ✅     ← only now does anything become real

 ...or, if anything fails:
 ROLLBACK ↩️   ← everything is undone; Sara still has her €20
```

---

## 📦 Part 1: Transactions in the database

Databases have transactions **built in**. In SQL, they look like this:

```sql
BEGIN;                                            -- 📦 start
UPDATE accounts SET money = money - 20 WHERE owner = 'Sara';
UPDATE accounts SET money = money + 20 WHERE owner = 'Trip';
COMMIT;                                           -- ✅ make it real
```

If something goes wrong after `BEGIN`, you write `ROLLBACK;` — and the database **forgets** every change since `BEGIN`. ↩️

| Rule | Meaning |
|---|---|
| **All or nothing** ⚛️ | Either **every** step is saved, or **none**. |
| **Invisible until commit** 🙈 | Other users don't see the half-done changes. |
| **Safe after commit** 💾 | After `COMMIT`, the data survives even a power cut. |

You **won't** write `BEGIN` and `COMMIT` yourself — Spring does it for you with **one label**. 🏷️

---

## 🏷️ Part 2: `@Transactional`

```java
@Transactional
public void payForTrip(...) {
    // step 1
    // step 2
}
```

| What happens | When |
|---|---|
| Spring starts a transaction (`BEGIN`) 📦 | When the method **starts** |
| Your code runs — all database work uses **this** transaction | During the method |
| Spring **commits** ✅ | When the method **ends normally** |
| Spring **rolls back** ↩️ | When the method throws a **`RuntimeException`** (or an `Error`) |

### 🎭 How does a label do that?

Remember the **proxy** from Chapter 72? When a bean has `@Transactional` methods, Spring puts a **proxy** around it. Other beans get the **proxy**, not your real object:

```
 Controller ──► 🎭 Proxy of ClassroomService ──► your real ClassroomService
                  │ 1. BEGIN                        │ runs your code
                  │ 3. COMMIT or ROLLBACK  ◄────────┘ 2. returns or throws
```

The proxy wraps every call with "begin → your method → commit/rollback". You never see it — it just works. 🪄 (Remember this proxy — it explains the traps in Part 7!)

---

## 🔬 Part 3: The experiment — with and without a transaction

Let's **see** it. We add an endpoint that creates **several** students **at once** and puts them in a classroom: `POST /api/classrooms/{classroomId}/students`, with a **list** of students in the body.

**`ClassroomService`** — the new method:

```java
@Transactional
public List<StudentResponse> addNewStudents(Long classroomId, List<StudentRequest> requests) {
    Classroom classroom = findClassroom(classroomId);
    return requests.stream()
            .map(request -> {
                if (studentRepository.existsByEmailIgnoreCase(request.email())) {
                    throw new EmailAlreadyUsedException(request.email());
                }
                Student student = new Student(request.name(), request.email(), request.age());
                student.setClassroom(classroom);
                return StudentResponse.from(studentRepository.save(student));
            })
            .toList();
}
```

**`ClassroomController`**:

```java
@PostMapping("/{classroomId}/students")
public List<StudentResponse> addNewStudents(@PathVariable Long classroomId,
                                            @RequestBody List<@Valid StudentRequest> requests) {
    return classroomService.addNewStudents(classroomId, requests);
}
```

| Code | Meaning |
|---|---|
| `requests.stream().map(request -> { ... })` | For **each** student in the list: check, create, save. A lambda with **several** lines needs `{ }` and `return` (Chapter 35). |
| `throw new EmailAlreadyUsedException(...)` | If an email is taken → stop with an exception (a `RuntimeException`!). |
| `List<@Valid StudentRequest>` | Validate **each** item of the list (Chapter 65). If one is invalid → 400 `Validation failure`. |

### 🧪 The test

We send **two** new students. The **first** is fine (Omar). The **second** uses Sara's email — that one **must** fail:

```bash
curl -i -X POST http://localhost:8080/api/classrooms/1/students \
  -H "Content-Type: application/json" \
  -d '[{"name":"Omar Ali","email":"omar@school.com","age":12},{"name":"Sara Copy","email":"sara@school.com","age":12}]'
```

The answer is the same both times — **409**:

```json
{"detail":"The email sara@school.com is already used by another student","instance":"/api/classrooms/1/students","status":409,"title":"Email already used"}
```

But what's in the **database** afterwards? 🤔 We ran it twice — once **with** `@Transactional`, once **without**. Then we called `GET /api/students`:

**❌ Without `@Transactional`:**

```json
[{"id":1,"name":"Sara Ahmed",...},{"id":2,"name":"Tom Brown",...},{"id":3,"name":"Lina Haddad",...},{"id":4,"name":"Omar Ali","email":"omar@school.com","age":12,"classroom":"5A"}]
```

😱 **Omar was saved!** The request **failed** (409) — but **half** of it happened anyway. The client thinks "nothing worked", tries again... and now gets "omar@school.com is already used"! A mess. 🍝

**✅ With `@Transactional`:**

```json
[{"id":1,"name":"Sara Ahmed",...},{"id":2,"name":"Tom Brown",...},{"id":3,"name":"Lina Haddad",...}]
```

🎉 **Omar is NOT there.** The exception → **rollback** ↩️ → Omar's `INSERT` was **undone**. **All or nothing!** The client can fix Sara's email and send both again. 👍

### 🤔 Why was Omar saved without `@Transactional`?

Because **every** repository method (`save`, `findById`...) has its **own** small transaction built in. Without `@Transactional` on our method:

```
 save(Omar)      → its own transaction → COMMIT ✅ (Omar is saved for real)
 exists(Sara)?   → yes → throw 💥
                   ...but Omar is already committed. Too late! 😱
```

With `@Transactional` on our method, all the steps join **one big** transaction:

```
 BEGIN 📦
   save(Omar)       → joins the big transaction (not committed yet)
   exists(Sara)?    → yes → throw 💥
 ROLLBACK ↩️        → Omar's insert is undone
```

### 👀 Watch it in the log

Want to **see** the transaction? Add this to `application.properties` (only while learning):

```properties
logging.level.org.springframework.orm.jpa.JpaTransactionManager=DEBUG
```

Our real log for the request **with** `@Transactional` (shortened):

```
Creating new transaction with name [com.example.school.service.ClassroomService.addNewStudents]: PROPAGATION_REQUIRED,ISOLATION_DEFAULT
Opened new EntityManager [SessionImpl(187278003<open>)] for JPA transaction
...
Participating in existing transaction
...
Participating in existing transaction
...
Initiating transaction rollback
Rolling back JPA transaction on EntityManager [SessionImpl(187278003<open>)]
```

| Log line | Meaning |
|---|---|
| `Creating new transaction with name [...addNewStudents]` | 📦 `BEGIN` — the proxy started a transaction for our method. |
| `PROPAGATION_REQUIRED` | "Use the existing transaction, or start one." (The default.) |
| `Participating in existing transaction` | ⭐ The repository calls **joined** our transaction (instead of making their own). |
| `Initiating transaction rollback` / `Rolling back JPA transaction` | ↩️ The exception came → everything undone. |

For a normal, successful request, you'd see `Initiating transaction commit` / `Committing JPA transaction` instead. ✅

---

## 🧹 Part 4: Dirty checking — saving without `save`

In Chapters 75–76, we changed entities and **never called `save`** — and it was saved anyway! Now you can understand why:

```java
@Transactional
public StudentResponse addStudent(Long classroomId, Long studentId) {
    Classroom classroom = findClassroom(classroomId);
    Student student = studentRepository.findById(studentId).orElseThrow(...);
    student.setClassroom(classroom);     // just change the object...
    return StudentResponse.from(student);
}                                        // ...at COMMIT, Hibernate writes the UPDATE! 🧹
```

Inside a transaction, Hibernate **remembers** every entity it loaded. At **commit**, it compares them with how they were, and writes an `UPDATE` for everything that **changed** ("dirty" = changed). 🧹

| | Outside a transaction | Inside `@Transactional` |
|---|---|---|
| Change an entity + `save(...)` | ✅ saved | ✅ saved |
| Change an entity, **no** `save` | ❌ **not** saved | ✅ saved at commit (dirty checking) |

> 💡 Many developers still call `save(...)` anyway — it's clear to read and doesn't hurt. Both styles are fine. 😊

---

## 📖 Part 5: `readOnly = true`

For methods that only **read**, we wrote `@Transactional(readOnly = true)` (Chapter 75). What does it add?

| | `@Transactional` | `@Transactional(readOnly = true)` |
|---|---|---|
| Lazy loading works | ✅ | ✅ |
| Dirty checking at the end | ✅ (checks every entity) | ❌ skipped → a little **faster** ⚡ |
| Meaning for humans | "This method changes data" | "This method **only reads**" 📖 |

Our `StudentService` pattern from Chapter 75:

```java
@Service
@Transactional(readOnly = true)          // default for all methods: read-only
public class StudentService {

    public List<StudentResponse> getAll(...) { ... }      // read-only ✅

    @Transactional                                        // this one writes
    public StudentResponse create(StudentRequest request) { ... }
}
```

---

## 🧭 Part 6: Where to put `@Transactional`

| Put it on... | Why |
|---|---|
| ✅ **Service** methods | The service is where a "**job**" (one use case) lives — often several database steps. |
| ❌ Controller methods | The controller is for HTTP. Keep database work in the service (Chapter 63). |
| ❌ Repository interfaces | Spring Data already does it for each single method. |
| ✅ The service **class** (with `readOnly = true`) + methods that write | A clean default (Part 5). |

**Rule of thumb:** 📏 **One service method = one transaction = one job.** "Add these students", "move this student", "enroll in a course"...

---

## 🪤 Part 7: When `@Transactional` silently does nothing

`@Transactional` works through the **proxy** 🎭. If a call doesn't go **through** the proxy, there's **no** transaction — and **no** error message! 😬

### Trap 1: Calling your own method (self-invocation)

```java
@Service
public class ClassroomService {

    public void importStudents(...) {
        addNewStudents(...);        // ❌ calls the method DIRECTLY, not through the proxy!
    }

    @Transactional
    public List<StudentResponse> addNewStudents(...) { ... }
}
```

`importStudents` calls `addNewStudents` **inside** the same object — it never goes through the proxy, so **no** transaction starts. 🎭❌ **Fix:** Put `@Transactional` on the method that's called **from outside** (`importStudents`), or move the method into another bean.

### Trap 2: `private` methods

`@Transactional` on a `private` method does nothing — the proxy can't reach private methods. **Fix:** Use it on `public` methods.

### Trap 3: Catching the exception yourself

```java
@Transactional
public void addAll(...) {
    try {
        ...
        throw new EmailAlreadyUsedException(...);
    } catch (EmailAlreadyUsedException e) {
        System.out.println("Oops");   // ❌ the proxy never sees the exception → COMMIT!
    }
}
```

The method ends **normally** → the proxy **commits** the half-done work. 😱 **Fix:** Let the exception **leave** the method (or rethrow it).

### Trap 4: Checked exceptions don't roll back

By default, Spring rolls back only for **`RuntimeException`**s (and `Error`s). A **checked** exception (Chapter 33, like `IOException`) → **commit**! 😮

```java
@Transactional(rollbackFor = Exception.class)   // roll back for ALL exceptions
public void importFromFile(...) throws IOException { ... }
```

**Fix:** Use `RuntimeException`s for business errors (all our exceptions extend `RuntimeException` ✅), or add `rollbackFor`.

| Situation | Transaction? |
|---|---|
| A `public` method called from **another** bean ✅ | Yes 📦 |
| A method called from the **same** class | ❌ No |
| A `private` method | ❌ No |
| Exception caught inside the method | Commits! ⚠️ |
| Checked exception (without `rollbackFor`) | Commits! ⚠️ |

---

## 💻 Mini project: Move a whole classroom 🏫➡️🏫

The school merges classes! Write **`PUT /api/classrooms/{fromId}/move-to/{toId}?max=30`**: move **all** students from one classroom to another — but the new classroom may have **at most** `max` students. If it would be too many, **nothing** may move (all or nothing!) → **409** with a clear message.

1. Create a new exception **`ClassroomFullException`** (409, title `"Classroom full"`).
2. Write `moveAll(fromId, toId, max)` in `ClassroomService`: move the students **one by one**, and **after** the loop, check the new size — if it's over `max`, throw. 🧪 (Yes, on purpose **after** moving — to test the rollback!)
3. Test with `max=2` and `max=30`.

<details>
<summary>Click to see the answer</summary>

**`exception/ClassroomFullException.java`**

```java
package com.example.school.exception;

public class ClassroomFullException extends RuntimeException {

    public ClassroomFullException(String name, int max) {
        super("Classroom " + name + " can have at most " + max + " students");
    }
}
```

In **`GlobalExceptionHandler`**:

```java
@ExceptionHandler(ClassroomFullException.class)
public ProblemDetail handleClassroomFull(ClassroomFullException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, ex.getMessage());
    problem.setTitle("Classroom full");
    return problem;
}
```

In **`ClassroomService`**:

```java
@Transactional
public ClassroomResponse moveAll(Long fromId, Long toId, int max) {
    Classroom from = findClassroom(fromId);
    Classroom to = findClassroom(toId);
    for (Student student : List.copyOf(from.getStudents())) {
        student.setClassroom(to);
        from.getStudents().remove(student);
        to.getStudents().add(student);
    }
    if (to.getStudents().size() > max) {
        throw new ClassroomFullException(to.getName(), max);
    }
    return ClassroomResponse.from(to);
}
```

In **`ClassroomController`**:

```java
@PutMapping("/{fromId}/move-to/{toId}")
public ClassroomResponse moveAll(@PathVariable Long fromId, @PathVariable Long toId,
                                 @RequestParam(defaultValue = "30") int max) {
    return classroomService.moveAll(fromId, toId, max);
}
```

| Code | Meaning |
|---|---|
| `List.copyOf(from.getStudents())` | A **copy** of the list to loop over — we **change** the original list inside the loop (Chapter 30: never change a list while looping over it!). |
| `student.setClassroom(to)` | The owner side 👑 — this is what's saved. |
| `from.getStudents().remove(...)` / `to.getStudents().add(...)` | Keep the mirrors 🪞 correct, so `to.getStudents().size()` is right. |
| `throw new ClassroomFullException(...)` | → **rollback** ↩️: every `setClassroom` is undone! |

Test (starting data: 5A has Sara and Lina, 6B has Tom):

- `PUT /api/classrooms/1/move-to/2?max=2` → **409** `Classroom 6B can have at most 2 students` — and `GET /api/classrooms` still shows Sara and Lina in **5A**. Nothing moved! ✅
- `PUT /api/classrooms/1/move-to/2?max=30` → **200**, 6B now has Tom, Sara and Lina; 5A is empty. ✅

</details>

---

## ✋ Try it yourself

**Task 1:** Remove `@Transactional` from `moveAll` and repeat the `max=2` test. What happens? Why?

<details>
<summary>Click to see the answer</summary>

Without a transaction, the request still answers **409**... but did anything move? Each student is loaded, and `setClassroom` changes the object — but with **no** transaction, there's **no dirty checking**, so nothing is saved... and worse: `from.getStudents()` is a **lazy** list → `LazyInitializationException` → **500**! 😵 Either way: **always** use `@Transactional` for jobs that change data in several steps.

</details>

**Task 2:** Which of these roll back? a) `throw new StudentNotFoundException(5L)` b) `throw new IOException("disk full")` (in a method with `throws IOException`) c) an exception caught with `try/catch` inside the method

<details>
<summary>Click to see the answer</summary>

a) ✅ Rollback (a `RuntimeException`). b) ❌ Commit! (A checked exception — add `rollbackFor = Exception.class`.) c) ❌ Commit! (The proxy never sees it.)

</details>

**Task 3:** Why did our `DataLoader` (Chapter 75) get `@Transactional` on its `run` method?

<details>
<summary>Click to see the answer</summary>

So all the seed data (classrooms, courses, students and the relationships) is saved in **one** transaction: either everything, or — if something fails — nothing. No half-filled database! (It also lets us add courses to `sara.getCourses()` safely inside one session.)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: No `@Transactional` on multi-step jobs

The first steps are saved, the later ones fail → **half-done** data. 😱 **Fix:** `@Transactional` on the service method.

### Mistake 2: `@Transactional` on a method called from the same class

No proxy → no transaction → no error message. 🪤 **Fix:** Annotate the method that's called from **outside**.

### Mistake 3: Catching exceptions inside the transaction

The proxy commits half-done work. **Fix:** Let it fly out (the global handler turns it into a nice answer — Chapter 66).

### Mistake 4: Business exceptions as checked exceptions

`class EmailAlreadyUsedException extends Exception` → **no** rollback by default. **Fix:** `extends RuntimeException` (like all of ours) — or `rollbackFor`.

### Mistake 5: Huge transactions

A transaction that runs for minutes (for example, while calling another slow website 🐢) keeps database rows **locked**. **Fix:** Keep transactions **short**: only the database work inside.

---

## ✅ Summary

- A **transaction** = **all or nothing** ⚛️: **commit** ✅ makes everything real, **rollback** ↩️ undoes everything.
- **`@Transactional`** (on **public service** methods): the **proxy** 🎭 begins a transaction, **commits** when the method ends normally, and **rolls back** on a **`RuntimeException`**.
- Without it, each repository call is its **own** transaction → **half-done** work stays saved. We **saw** it: Omar saved by a failed request! 😱
- `logging.level.org.springframework.orm.jpa.JpaTransactionManager=DEBUG` shows "Creating new transaction", "Participating in existing transaction", "Rolling back".
- **Dirty checking** 🧹: inside a transaction, changed entities are saved at commit — even without `save`.
- **`readOnly = true`** for methods that only read (a little faster, clearer).
- 🪤 Traps: **self-invocation**, **private** methods, **caught** exceptions, **checked** exceptions (`rollbackFor`).
- One service method = one transaction = one job. Keep transactions **short**.

---

## ❓ Quiz

1. What does "all or nothing" mean for a transaction?
2. What's the difference between commit and rollback?
3. When does Spring roll back a `@Transactional` method?
4. In our experiment, why was Omar saved without `@Transactional`?
5. What is dirty checking?
6. What does `readOnly = true` do?
7. Why doesn't `@Transactional` work when a method calls another method of the same class?
8. A method throws an `IOException`. Is the transaction rolled back? How can you change that?

<details>
<summary>Click to see the answers</summary>

1. Either every step is saved, or none of them is.
2. Commit makes all changes permanent. Rollback undoes all changes since the transaction began.
3. When the method throws a `RuntimeException` (or an `Error`) out of the method.
4. Because each repository call (like `save`) ran in its own small transaction, which committed immediately — before the second student failed.
5. Inside a transaction, Hibernate notices changes to loaded entities and writes the UPDATEs automatically at commit.
6. It marks the transaction as read-only: no dirty checking at the end (a bit faster), and it tells readers the method doesn't change data.
7. The call doesn't go through Spring's proxy, so nobody starts a transaction.
8. No — by default, checked exceptions commit. Use `@Transactional(rollbackFor = Exception.class)`.

</details>

---

## 🎉 Part 9 complete!

Your app has a **real database** now! 🗄️🎉 Look at everything you learned:

- ✅ What databases, tables, primary keys and foreign keys are
- ✅ **SQL**: `CREATE`, `INSERT`, `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY`, `UPDATE`, `DELETE`
- ✅ **H2**: in memory, in a file, and the H2 Console
- ✅ **JDBC** underneath, and **JPA / Hibernate / Spring Data JPA** on top
- ✅ **Entities** that become tables, and **repositories** in **one line** 🧞
- ✅ A **full CRUD API** whose data survives restarts 💾
- ✅ **Query methods**, **JPQL** and **native SQL**
- ✅ **Relationships**: one-to-many 🏫 and many-to-many 📚
- ✅ **PostgreSQL** 🐘 and **MySQL** 🐬 — with **zero** Java changes
- ✅ **Paging** and **sorting** 📄
- ✅ **Transactions**: all or nothing ⚛️

### 🏁 Where are we?

```
 Part 1 ✅ Getting ready          Part 6 ✅ How the web works
 Part 2 ✅ Java basics            Part 7 ✅ Spring Boot basics
 Part 3 ✅ Objects (OOP)          Part 8 ✅ Building REST APIs
 Part 4 ✅ More Java              Part 9 ✅ Databases           ← you are here! 🎉
 Part 5 ✅ Tools                  Part 10 ⏳ Security           ← next!
```

But wait... 😟 Right now, **anybody** on the internet could call `DELETE /api/students/1`! There's no login, no password, no "only teachers may do this". In **Part 10**, you'll protect your API with **Spring Security** 🔒: users and passwords, roles like **ADMIN** and **USER**, and **JWT tokens** — the way modern apps log in. 🔑

Let's lock the doors! 🔐

---

[⬅ Previous chapter](78-paging-sorting.md) | [Table of Contents](../README.md) | [Next chapter: Spring Security: the introduction ➡](../part-10-security/80-spring-security.md)
