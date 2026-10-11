# Chapter 85 – Mockito: fake helpers for tests

[⬅ Previous chapter](84-junit.md) | [Table of Contents](../README.md) | [Next chapter ➡](86-testing-controllers.md)

---

## 🎯 Goal

`GradeCalculator` was easy to test: it needs **nobody**. But most of our classes have **helpers**. `StudentService` needs a `StudentRepository` — and the repository needs a **database**. 😟 How do we test the service **alone**, fast, without a database?

We give it a **fake** repository! 🎭 Today you'll meet **Mockito**, the tool that makes fakes.

At the end of this chapter you will know:

- What a **mock** is, and **why** we use one 🎭
- How to make mocks with **`@Mock`** and **`@InjectMocks`**
- How to tell a mock what to answer: **`when(...).thenReturn(...)`**
- How to check that a mock **was called** (or **not**): **`verify(...)`**, **`never()`**
- How to catch what was **given** to a mock: **`ArgumentCaptor`** 🪤
- How to test `StudentService` in **2 seconds**, without any database 🚀

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Mock** | A **fake** object that **pretends** to be a real helper. It only does what **you** tell it. 🎭 |
| **Mockito** | The most popular Java tool for making mocks. 🍸 |
| **Stub** / **stubbing** | Telling a mock what to **answer**: "When someone asks for student 1, give back Sara." |
| **Verify** | Checking **afterwards** that a mock **was called** — and with what. 🔍 |
| **Dependency** | A helper a class **needs** to work, like the repository for the service (Chapter 53). |
| **Isolation** | Testing a class **all alone**, without its real helpers. 🏝️ |
| **Argument** | A value given to a method when it's called: in `findById(1L)`, the argument is `1L`. |
| **Captor** | A trap 🪤 that **catches** the argument given to a mock, so you can look at it. |

---

## 📖 Story: The flight simulator ✈️

Pilots must practise for emergencies: an engine fire 🔥, a storm ⛈️, a broken wheel. But you can't set a **real** plane on fire to practise! 😱

So pilots use a **flight simulator**: a fake cockpit that looks and feels real. 🎮 The teacher can say:

- "**When** the pilot pulls the lever, **then** show an engine fire." 🔥
- Afterwards: "**Did** the pilot press the fire button? **How many times**?" 🔍

The simulator is **safe**, **fast**, and the teacher **controls** everything — even things that almost never happen in real life.

A **mock** is a flight simulator for your code:

| Flight simulator ✈️ | Mockito 🍸 |
|---|---|
| A fake cockpit instead of a real plane | A **fake** repository instead of a real database |
| "When the lever is pulled, show a fire" | `when(repository.findById(1L)).thenReturn(...)` — **stubbing** |
| "Did the pilot press the fire button?" | `verify(repository).deleteById(3L)` — **verifying** |
| Practise rare emergencies safely | Test "student not found", "email taken"... easily |

---

## 🤔 Part 1: Why fake helpers?

Look at `StudentService.getById` (from Part 9):

```java
public StudentResponse getById(Long id) {
    return StudentResponse.from(findStudent(id));
}

private Student findStudent(Long id) {
    return studentRepository.findById(id)
            .orElseThrow(() -> new StudentNotFoundException(id));
}
```

To test it with the **real** repository, we'd need: Spring 🌱, Hibernate, H2, a table, test data... That's **slow** (remember: `contextLoads()` took 19 seconds 🐢), and when the test fails, we don't know if the **service** is wrong — or the database, or the data.

With a **mock** repository:

```
 Real:   StudentService ──► StudentRepository ──► Hibernate ──► H2 database 🗄️   (slow, many parts)

 Test:   StudentService ──► 🎭 mock repository                                  (fast, only the service!)
                              "When findById(1) is called,
                               I answer: Sara. (I don't even know what a database is.)"
```

Now we test **only** the service's **own** logic: "If the repository finds nobody, do you throw `StudentNotFoundException`?" That's a real **unit test** 🧩 — one class, in **isolation** 🏝️.

💡 Mockito is already in your project — it comes with `spring-boot-starter-webmvc-test`, together with JUnit and AssertJ. 👍

---

## 🎭 Part 2: Your first mock test

Create **`src/test/java/com/example/school/service/StudentServiceTest.java`**:

```java
package com.example.school.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.when;

import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.example.school.dto.StudentResponse;
import com.example.school.entity.Student;
import com.example.school.exception.StudentNotFoundException;
import com.example.school.repository.StudentRepository;

@ExtendWith(MockitoExtension.class)
class StudentServiceTest {

    @Mock
    private StudentRepository studentRepository;

    @InjectMocks
    private StudentService studentService;

    @Test
    void getByIdReturnsTheStudent() {
        Student sara = new Student("Sara Ahmed", "sara@school.com", 12);
        when(studentRepository.findById(1L)).thenReturn(Optional.of(sara));

        StudentResponse response = studentService.getById(1L);

        assertThat(response.name()).isEqualTo("Sara Ahmed");
        assertThat(response.email()).isEqualTo("sara@school.com");
        assertThat(response.age()).isEqualTo(12);
    }

    @Test
    void getByIdThrowsWhenTheStudentDoesNotExist() {
        when(studentRepository.findById(99L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> studentService.getById(99L))
                .isInstanceOf(StudentNotFoundException.class)
                .hasMessage("Student with id 99 was not found");
    }
}
```

Line by line:

| Code | Meaning |
|---|---|
| `@ExtendWith(MockitoExtension.class)` | "JUnit, let **Mockito** help in this test class." Without it, the `@Mock` fields stay `null`! |
| `@Mock private StudentRepository studentRepository;` | ⭐ Mockito makes a **fake** `StudentRepository`. It has all the methods — but they do **nothing** until you say so. 🎭 |
| `@InjectMocks private StudentService studentService;` | ⭐ "Make a **real** `StudentService`, and give it the mocks through its constructor." Like Spring's dependency injection (Chapter 53) — but done by Mockito, **without** Spring. |
| `Student sara = new Student(...)` | **Arrange**: a normal Java object. No database! (Its `id` is `null` — nobody saved it. That's OK for this test.) |
| `when(studentRepository.findById(1L)).thenReturn(Optional.of(sara));` | ⭐ **Stubbing**: "**When** someone calls `findById(1L)` on the mock, **then return** Sara." |
| `studentService.getById(1L)` | **Act**: call the **real** service. Inside, it calls the **mock** repository — and gets Sara. |
| `assertThat(response.name()).isEqualTo("Sara Ahmed")` | **Assert**: did the service turn Sara into the right `StudentResponse`? |
| `thenReturn(Optional.empty())` | In the second test, the mock answers "nobody found". Practising the "emergency"! 🔥 |
| `assertThatThrownBy(...).isInstanceOf(StudentNotFoundException.class)` | The service must **throw** — with the right message. |

Here's what happens in the first test:

```
 Test                     StudentService (real)           🎭 mock StudentRepository
  │ getById(1L) ───────────► │
  │                          │ findById(1L) ─────────────────► │ "I was told: answer Sara!"
  │                          │ ◄──────────── Optional.of(sara) │
  │                          │ StudentResponse.from(sara)
  │ ◄──── response ──────────│
  │ assertThat(...) ✅
```

Run it (green ▶️, or `./mvnw test -Dtest=StudentServiceTest`). **Green**, in about **2 seconds**. 🚀

💡 You may see this message in the output:

```
Mockito is currently self-attaching to enable the inline-mock-maker. This will no longer work in future releases of the JDK. ...
WARNING: A Java agent has been loaded dynamically ...
```

That's just a **warning** about a future Java version — your tests work fine. You can ignore it for now. 🙂

---

## 🔍 Part 3: Did it really happen? — `verify`

Sometimes a method **returns nothing**, like `delete`. How do we check it worked? We check that the service **asked the repository** to delete! 🔍

Add these tests (plus the imports `import static org.mockito.Mockito.verify;`, `import static org.mockito.Mockito.never;` and `import static org.mockito.ArgumentMatchers.any;`):

```java
@Test
void deleteRemovesAnExistingStudent() {
    when(studentRepository.existsById(3L)).thenReturn(true);

    studentService.delete(3L);

    verify(studentRepository).deleteById(3L);
}

@Test
void deleteThrowsWhenTheStudentDoesNotExist() {
    when(studentRepository.existsById(99L)).thenReturn(false);

    assertThatThrownBy(() -> studentService.delete(99L))
            .isInstanceOf(StudentNotFoundException.class);
    verify(studentRepository, never()).deleteById(any());
}
```

| Code | Meaning |
|---|---|
| `verify(studentRepository).deleteById(3L);` | ⭐ "Check that `deleteById(3L)` **was called** on the mock — exactly **once**." If not → the test fails. |
| `verify(studentRepository, never()).deleteById(any());` | ⭐ "Check that `deleteById` was **never** called — with **any** argument." When the student doesn't exist, nothing must be deleted! |
| `any()` | An **argument matcher**: "it doesn't matter **which** value". |

The mock **remembers** every call — like a flight simulator recording every button the pilot pressed. 📼

---

## 🪤 Part 4: The email check — and `ArgumentCaptor`

Now the most interesting method: `create`.

```java
@Transactional
public StudentResponse create(StudentRequest request) {
    if (studentRepository.existsByEmailIgnoreCase(request.email())) {
        throw new EmailAlreadyUsedException(request.email());
    }
    Student student = new Student(request.name(), request.email(), request.age());
    return StudentResponse.from(studentRepository.save(student));
}
```

Two cases to test: the email is **free** → save; the email is **taken** → throw and **don't** save.

```java
@Test
void createSavesANewStudent() {
    StudentRequest request = new StudentRequest("Omar Ali", "omar@school.com", 12);
    when(studentRepository.existsByEmailIgnoreCase("omar@school.com")).thenReturn(false);
    when(studentRepository.save(any(Student.class))).thenAnswer(invocation -> invocation.getArgument(0));

    StudentResponse response = studentService.create(request);

    assertThat(response.name()).isEqualTo("Omar Ali");
    ArgumentCaptor<Student> captor = ArgumentCaptor.forClass(Student.class);
    verify(studentRepository).save(captor.capture());
    Student saved = captor.getValue();
    assertThat(saved.getEmail()).isEqualTo("omar@school.com");
    assertThat(saved.getAge()).isEqualTo(12);
    assertThat(saved.getCreatedAt()).isNotNull();
}

@Test
void createRefusesAnEmailThatIsAlreadyUsed() {
    StudentRequest request = new StudentRequest("Sara Copy", "sara@school.com", 12);
    when(studentRepository.existsByEmailIgnoreCase("sara@school.com")).thenReturn(true);

    assertThatThrownBy(() -> studentService.create(request))
            .isInstanceOf(EmailAlreadyUsedException.class);
    verify(studentRepository, never()).save(any());
}
```

(More imports: `org.mockito.ArgumentCaptor`, `com.example.school.dto.StudentRequest`, `com.example.school.exception.EmailAlreadyUsedException`.)

| Code | Meaning |
|---|---|
| `when(...save(any(Student.class)))` | "When `save` is called with **any** `Student`..." |
| `.thenAnswer(invocation -> invocation.getArgument(0))` | "...answer with the **same** student you were given." (A real `save` gives back the saved student, too.) `thenAnswer` takes a **lambda** that can look at the call; `getArgument(0)` = the **first** argument. |
| `ArgumentCaptor<Student> captor = ArgumentCaptor.forClass(Student.class);` | A **trap** 🪤 for `Student` arguments. |
| `verify(studentRepository).save(captor.capture());` | "Check that `save` was called — and **catch** the student it was given!" |
| `captor.getValue()` | The caught student. Now we can look **inside**: is the email right? The age? Was `createdAt` filled in? |
| `isNotNull()` | AssertJ: "it's **not** `null`". |
| `verify(studentRepository, never()).save(any());` | ⭐ When the email is taken, **nothing** may be saved. |

🤔 **Why the captor?** The service makes the `Student` object **inside** itself — the test never sees it. The captor lets us **peek** at exactly what the service handed to the database. 👀

### 🐛 Let's see a test catch a bug

Imagine someone "cleans up" `create` and accidentally swaps two arguments:

```java
Student student = new Student(request.email(), request.name(), request.age());   // 🐛 email and name swapped!
```

The code **compiles** (both are `String`s) and the app **starts**. But our test says (real output):

```
[ERROR] com.example.school.service.StudentServiceTest.createSavesANewStudent -- Time elapsed: 0.122 s <<< FAILURE!
org.opentest4j.AssertionFailedError: 

expected: "Omar Ali"
 but was: "omar@school.com"
```

🎯 Caught in **2 seconds** — long before a real student named "omar@school.com" shows up on a report card. 😄

---

## 📋 Part 5: Testing lists — and which query was used

`getAll(minAge, name)` picks **one** of four repository methods, depending on the filters. Let's test two of the four paths:

```java
@Test
void getAllWithoutFiltersReturnsEveryStudent() {
    when(studentRepository.findAll()).thenReturn(List.of(
            new Student("Sara Ahmed", "sara@school.com", 12),
            new Student("Tom Brown", "tom@school.com", 13)));

    List<StudentResponse> students = studentService.getAll(null, null);

    assertThat(students).hasSize(2);
    assertThat(students).extracting(StudentResponse::name).containsExactly("Sara Ahmed", "Tom Brown");
}

@Test
void getAllWithMinAgeUsesTheAgeQuery() {
    when(studentRepository.findByAgeGreaterThanEqual(13)).thenReturn(List.of(
            new Student("Tom Brown", "tom@school.com", 13)));

    List<StudentResponse> students = studentService.getAll(13, null);

    assertThat(students).extracting(StudentResponse::name).containsExactly("Tom Brown");
    verify(studentRepository, never()).findAll();
}
```

(Import `java.util.List`.)

| Code | Meaning |
|---|---|
| `assertThat(students).hasSize(2)` | The list has **2** items. |
| `.extracting(StudentResponse::name)` | ⭐ AssertJ magic: "From each item, take the **name**..." |
| `.containsExactly("Sara Ahmed", "Tom Brown")` | "...the names must be **exactly** these, in **this** order." |
| `verify(studentRepository, never()).findAll()` | With a `minAge`, the service must use the **age query** — not load **all** students. |

Run the whole class: our real result — **8 tests, all green**, in about 2 seconds:

```
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 2.026 s -- in com.example.school.service.StudentServiceTest
```

### 🤔 What does a mock answer if you **don't** stub it?

Mockito gives back "empty" answers: `null` for objects, `0` for numbers, `false` for `boolean`, an **empty** list for lists — and `Optional.empty()` for `Optional`s! For example, a test that calls `studentService.getById(1L)` **without** any `when(...)` gets (real output):

```
com.example.school.exception.StudentNotFoundException: Student with id 1 was not found
```

The mock said "nobody found" — because nobody told it otherwise. 🤷

---

## 📏 Part 6: What to mock — and what not

| ✅ Mock it | ❌ Don't mock it |
|---|---|
| Repositories (databases) 🗄️ | The class you're **testing** (then you test nothing!) |
| Services that call **other** websites 🌍 | Simple data objects: records, DTOs, entities — just `new` them |
| Things that are slow, or random, or about time ⏰ | Java's own classes like `String` or `List` |

⭐ A good rule: **mock the neighbours, test the house.** 🏠

And remember what a mock test **can't** tell you: whether the **real** repository works. Is the query method spelled right? Does the SQL work? For that, we need tests **with a database** — that's Chapter 87. And whether the **URL**, the **JSON** and the **security rules** work — that's Chapter 86. 🧩🧩🧩

---

## 💻 Mini project: Test `UserService.register` 🔐

Write **`UserServiceTest`** for `register` (Chapter 81). `UserService` has **two** helpers: `AppUserRepository` **and** `PasswordEncoder` — mock both!

1. **Name is free:** the service must save the **hash**, never the plain password. Let the mock encoder turn `"sunflower7"` into `"HASHED-sunflower7"`, catch the saved `AppUser` with a captor, and check its password. Also check the answer: username `sara`, role `USER`.
2. **Name is taken:** expect `UsernameTakenException` with the message `"The username sara is already taken"` — and check that the encoder and `save` were **never** called.

<details>
<summary>Click to see the answer</summary>

**`src/test/java/com/example/school/service/UserServiceTest.java`**

```java
package com.example.school.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import com.example.school.dto.RegisterRequest;
import com.example.school.dto.UserResponse;
import com.example.school.entity.AppUser;
import com.example.school.exception.UsernameTakenException;
import com.example.school.repository.AppUserRepository;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private AppUserRepository appUserRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserService userService;

    @Test
    void registerSavesTheHashNotThePassword() {
        when(appUserRepository.existsByUsername("sara")).thenReturn(false);
        when(passwordEncoder.encode("sunflower7")).thenReturn("HASHED-sunflower7");
        when(appUserRepository.save(any(AppUser.class))).thenAnswer(invocation -> invocation.getArgument(0));

        UserResponse response = userService.register(new RegisterRequest("sara", "sunflower7"));

        assertThat(response.username()).isEqualTo("sara");
        assertThat(response.role()).isEqualTo("USER");
        ArgumentCaptor<AppUser> captor = ArgumentCaptor.forClass(AppUser.class);
        verify(appUserRepository).save(captor.capture());
        assertThat(captor.getValue().getPassword()).isEqualTo("HASHED-sunflower7");
    }

    @Test
    void registerRefusesATakenUsername() {
        when(appUserRepository.existsByUsername("sara")).thenReturn(true);

        assertThatThrownBy(() -> userService.register(new RegisterRequest("sara", "sunflower7")))
                .isInstanceOf(UsernameTakenException.class)
                .hasMessage("The username sara is already taken");
        verify(passwordEncoder, never()).encode(any());
        verify(appUserRepository, never()).save(any());
    }
}
```

| Code | Meaning |
|---|---|
| `@Mock private PasswordEncoder passwordEncoder;` | A **fake** encoder. A real BCrypt would give a different, random hash every time — impossible to check exactly! The mock answers something **predictable**. 🎯 |
| `when(passwordEncoder.encode("sunflower7")).thenReturn("HASHED-sunflower7")` | "When asked to hash `sunflower7`, say `HASHED-sunflower7`." |
| `assertThat(captor.getValue().getPassword()).isEqualTo("HASHED-sunflower7")` | ⭐ The **saved** password is what the **encoder** made — so the service really hashed it before saving. 🔐 |
| `@InjectMocks` with **two** mocks | Mockito gives **both** to `UserService`'s constructor, matched by **type**. |

Our real result: `Tests run: 2, Failures: 0, Errors: 0`. ✅ (And no Spring, no database: a quarter of a second.)

</details>

---

## ✋ Try it yourself

1. In `deleteRemovesAnExistingStudent`, change the last line to `verify(studentRepository).deleteById(4L);`. Read the failure message.
2. In `getByIdReturnsTheStudent`, add one more line **before** the "Act" step: `when(studentRepository.existsById(1L)).thenReturn(true);`. Run it. What happens, and why?
3. In `createSavesANewStudent`, remove the `when(...save(...))...` line. What happens?
4. Write a test for `getAll(null, "sa")`: it must use `findByNameContainingIgnoreCase("sa")`.

<details>
<summary>Click to see the answers</summary>

1. Our real message:
   ```
   Argument(s) are different! Wanted:
   studentRepository.deleteById(4L);
   -> at com.example.school.service.StudentServiceTest...
   Actual invocations have different arguments:
   studentRepository.existsById(3L);
   ...
   studentRepository.deleteById(3L);
   ```
   Mockito shows what you **wanted** and what **really** happened. Very helpful! 🔍
2. The test **errors** with `UnnecessaryStubbingException`:
   ```
   Unnecessary stubbings detected.
   Clean & maintainable test code requires zero unnecessary code.
   Following stubbings are unnecessary (click to navigate to relevant line of code):
     1. -> at com.example.school.service.StudentServiceTest.getByIdReturnsTheStudent(...)
   ```
   `getById` never calls `existsById`. Mockito is **strict**: a `when(...)` that nobody uses usually means the test is wrong or out of date. Remove it.
3. `save` isn't stubbed → the mock returns `null` → `StudentResponse.from(null)` crashes. Our real error: `java.lang.NullPointerException: Cannot invoke "com.example.school.entity.Student.getClassroom()" because "student" is null`. A mock does **nothing** you didn't tell it!
4. ```java
   @Test
   void getAllWithNameUsesTheNameQuery() {
       when(studentRepository.findByNameContainingIgnoreCase("sa")).thenReturn(List.of(
               new Student("Sara Ahmed", "sara@school.com", 12)));

       List<StudentResponse> students = studentService.getAll(null, "sa");

       assertThat(students).extracting(StudentResponse::name).containsExactly("Sara Ahmed");
   }
   ```

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `@ExtendWith(MockitoExtension.class)`

Nobody makes the mocks → the fields stay `null`. Our real error:

```
java.lang.NullPointerException: Cannot invoke "com.example.school.repository.StudentRepository.findById(Object)" because "this.studentRepository" is null
```

**Fix:** Put `@ExtendWith(MockitoExtension.class)` on the test class.

### Mistake 2: Stubbing things that are never used

→ `UnnecessaryStubbingException` (Try it 2). **Fix:** Only stub what **this** test needs.

### Mistake 3: Forgetting to stub a method that returns something

→ the mock returns `null` (or empty), and your code crashes or takes the wrong path (Try it 3). **Fix:** Stub every call whose **answer** matters.

### Mistake 4: Mocking the class you're testing

```java
@Mock
private StudentService studentService;   // ❌ now you test a fake!
```

**Fix:** The class under test gets **`@InjectMocks`** (the real thing). Only its **helpers** get `@Mock`.

### Mistake 5: Thinking mock tests prove everything

A mock test passes even if the real query method has a typo, or the security rules are wrong. **Fix:** Mix your tests: **unit tests** with mocks (fast, many), plus **slice tests** and **integration tests** (Chapters 86–87).

---

## ✅ Summary

- A **mock** 🎭 is a fake helper that only does what you say. Mocks make unit tests **fast** and **isolated** 🏝️.
- **`@ExtendWith(MockitoExtension.class)`** on the class, **`@Mock`** on the helpers, **`@InjectMocks`** on the class under test.
- **Stubbing**: `when(mock.method(args)).thenReturn(value)` — or `.thenAnswer(invocation -> ...)`.
- **Verifying**: `verify(mock).method(args)`, `verify(mock, never()).method(any())`.
- **`ArgumentCaptor`** 🪤 catches what was given to a mock, so you can check it.
- Unstubbed mocks answer `null`, `0`, `false`, empty lists, `Optional.empty()`.
- Mockito is **strict**: unused stubs → `UnnecessaryStubbingException`.
- **Mock the neighbours, test the house.** 🏠

---

## ❓ Quiz

1. What is a mock, and why do we use one to test `StudentService`?
2. What's the difference between `@Mock` and `@InjectMocks`?
3. What does `when(studentRepository.findById(1L)).thenReturn(Optional.of(sara))` mean?
4. How do you check that `deleteById` was **never** called?
5. Why do we need an `ArgumentCaptor` in `createSavesANewStudent`?
6. What does an unstubbed mock return for a method with the return type `Optional<Student>`?
7. Why did we mock the `PasswordEncoder` in the mini project instead of using a real BCrypt encoder?
8. Name one thing a mock test of `StudentService` can **not** find.

<details>
<summary>Click to see the answers</summary>

1. A fake object that pretends to be a real helper. With a mock repository, we can test the service's own logic fast, without Spring or a database.
2. `@Mock` makes a fake helper. `@InjectMocks` makes the **real** class under test and gives it the mocks.
3. "When `findById(1L)` is called on the mock, return an `Optional` with Sara inside."
4. `verify(studentRepository, never()).deleteById(any());`
5. The service creates the `Student` object inside itself. The captor catches the object given to `save`, so the test can check its fields.
6. `Optional.empty()`.
7. A real BCrypt hash is different (random salt) every time, so we couldn't check the exact value. The mock returns a predictable value, which proves the service saved the encoder's result.
8. For example: a typo or wrong SQL in a repository query, wrong URLs, wrong JSON, or wrong security rules.

</details>

---

[⬅ Previous chapter](84-junit.md) | [Table of Contents](../README.md) | [Next chapter: Testing controllers ➡](86-testing-controllers.md)
