# Chapter 37 – `Optional`: Maybe There Is a Value, Maybe Not

[⬅ Previous chapter](36-streams.md) | [Table of Contents](../README.md) | [Next chapter ➡](38-annotations.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- Why **`null`** is so dangerous (the "billion-dollar mistake")
- What **`Optional`** is: a box that may be **empty** 📦
- How to **create** Optionals: `Optional.of`, `Optional.ofNullable`, `Optional.empty`
- How to **get the value safely**: `orElse`, `orElseGet`, `orElseThrow`
- How to **do something only if** there is a value: `ifPresent`, `ifPresentOrElse`
- How to **transform** it: `map`, `filter`
- **Good and bad** ways to use Optional
- How Spring Boot uses it: `repository.findById(id)` 🌱

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **`Optional<T>`** | A **box** that contains **one** T — or is **empty**. |
| **Present** | The box **has** a value. |
| **Empty** | The box has **no** value. |
| **Unwrap** | Take the value **out** of the box. |
| **Default value** | A value to use when the box is empty. |

---

## 📖 Story: The gift box 🎁

Your friend gives you a gift box. Before you open it, you **don't know** if there's something inside. Maybe it's a toy 🧸 — maybe it's **empty** (a joke! 😜).

**Without Optional** (`null`): your friend gives you... **nothing at all**. You reach out to take the gift, and your hand grabs **air**. You fall over. 💥 That's a **NullPointerException**.

**With Optional**: your friend **always** gives you a **box**. The box itself is never missing. And on the box, it's written clearly: "**might be empty**". So you **check** before you use what's inside:

- "If there's a toy, play with it." 🧸
- "If it's empty, play with my old ball instead." ⚽

---

## 💥 Part 1: The problem with `null`

Imagine a method that finds a user by name:

```java
public static String findEmail(String name) {
    if (name.equals("Sara")) {
        return "sara@mail.com";
    }
    return null;   // not found
}
```

```java
String email = findEmail("Tom");
System.out.println(email.toUpperCase());   // 💥 NullPointerException!
```

**The problem:** Looking at `String findEmail(String name)`, nothing **warns** you that it can return `null`. You **forget** to check. 💥

The inventor of `null`, Tony Hoare, called it his "**billion-dollar mistake**" 💸 — because of all the bugs and crashes it has caused in the world!

### ✅ With `Optional`

```java
public static Optional<String> findEmail(String name) {
    if (name.equals("Sara")) {
        return Optional.of("sara@mail.com");
    }
    return Optional.empty();
}
```

Now the **return type** says it clearly: `Optional<String>` = "**maybe** a String". You **can't** call `.toUpperCase()` on the box directly — Java **forces** you to think about the empty case:

```java
Optional<String> email = findEmail("Tom");
email.toUpperCase();   // ❌ error: cannot find symbol — the box is not a String!

String safe = email.orElse("no email");   // ✅ "no email"
```

👉 **`Optional` makes "maybe missing" visible in the type.** 🔍

---

## 📦 Part 2: Creating an Optional

| Code | Box | Use when |
|---|---|---|
| `Optional.of(value)` | 🎁 **with** the value | you're **sure** the value is not null |
| `Optional.empty()` | 📭 **empty** | there's no value |
| `Optional.ofNullable(value)` | 🎁 or 📭 | the value **might** be null — it chooses for you |

```java
Optional<String> full  = Optional.of("Hello");
Optional<String> empty = Optional.empty();

String maybeNull = null;
Optional<String> safe = Optional.ofNullable(maybeNull);   // → empty box

System.out.println(full);    // Optional[Hello]
System.out.println(empty);   // Optional.empty
System.out.println(safe);    // Optional.empty
```

> ⚠️ `Optional.of(null)` → 💥 `NullPointerException`. If the value might be null, use **`ofNullable`**.

Import: `java.util.Optional`.

---

## 🔍 Part 3: Checking the box

```java
Optional<String> name = Optional.of("Sara");

System.out.println(name.isPresent());   // true  — there IS a value
System.out.println(name.isEmpty());     // false
```

| Method | Question |
|---|---|
| `isPresent()` | Is there a value? |
| `isEmpty()` | Is the box empty? |

You **can** write this:

```java
if (name.isPresent()) {
    System.out.println(name.get());
}
```

But this is the **old-fashioned** way — it's just a `null` check with extra steps. 😕 The next parts show **better** ways!

---

## 🎁 Part 4: Getting the value out — safely

```java
Optional<String> found = Optional.of("Sara");
Optional<String> missing = Optional.empty();
```

### `orElse(default)` — use a default if empty

```java
String a = found.orElse("Guest");     // "Sara"
String b = missing.orElse("Guest");   // "Guest"
```

📖 "Give me what's in the box, **or else** give me 'Guest'."

### `orElseGet(supplier)` — make the default only if needed

```java
String c = missing.orElseGet(() -> "Guest-" + (int) (Math.random() * 1000));   // "Guest-482"
```

The lambda (a **Supplier** — Chapter 35) only runs **if** the box is empty. Use it when creating the default is **expensive** (for example, a database call).

### `orElseThrow(...)` — throw an exception if empty ⭐

```java
String d = found.orElseThrow();   // "Sara"
String e = missing.orElseThrow(() -> new IllegalArgumentException("User not found"));
// 💥 IllegalArgumentException: User not found
```

📖 "Give me the value — and if there is none, **pull the fire alarm** 🚨."

> 🌱 **This is the most common line in Spring Boot services!**
> ```java
> Student student = studentRepository.findById(id)
>         .orElseThrow(() -> new StudentNotFoundException(id));
> ```
> "Find the student; if there's no student with this id → throw an exception" → which becomes a **404 Not Found** for the user. 🎯

### ⚠️ `get()` — avoid it!

```java
String f = missing.get();   // 💥 NoSuchElementException: No value present
```

`get()` crashes on an empty box — it's just as dangerous as `null`! Use `orElse`, `orElseGet` or `orElseThrow` instead. (`orElseThrow()` without arguments does the same as `get()`, but its **name** makes the danger clear.)

### 📋 Summary

| Method | If present | If empty |
|---|---|---|
| `orElse(x)` | the value | `x` |
| `orElseGet(() -> x)` | the value | runs the lambda → `x` |
| `orElseThrow(() -> ex)` | the value | throws `ex` 🚨 |
| `orElseThrow()` | the value | throws `NoSuchElementException` |
| `get()` 👎 | the value | throws `NoSuchElementException` |

---

## 🎬 Part 5: Doing something only if there is a value

### `ifPresent(consumer)`

```java
Optional<String> email = findEmail("Sara");
email.ifPresent(e -> System.out.println("📧 Sending mail to " + e));
```

If the box is empty → **nothing** happens. No `if`, no crash. 😌

### `ifPresentOrElse(consumer, runnable)`

```java
findEmail("Tom").ifPresentOrElse(
        e -> System.out.println("📧 Sending mail to " + e),
        () -> System.out.println("⚠️ Tom has no email")
);
```

**Output:**

```
⚠️ Tom has no email
```

---

## 🔄 Part 6: Transforming: `map` and `filter`

Optional has `map` and `filter`, just like streams (Chapter 36)! Think of a stream with **0 or 1** item.

### `map` — change the value inside (if there is one)

```java
Optional<String> name = Optional.of("sara");

Optional<String> upper = name.map(String::toUpperCase);   // Optional[SARA]
Optional<Integer> length = name.map(String::length);       // Optional[4]

Optional<String> none = Optional.empty();
Optional<Integer> noLength = none.map(String::length);     // Optional.empty — no crash!
```

`map` only runs the function **if** there's a value. If empty → stays empty. 📭

### `filter` — keep the value only if it matches

```java
Optional<Integer> age = Optional.of(15);

Optional<Integer> adult = age.filter(a -> a >= 18);   // Optional.empty (15 is not >= 18)
Optional<Integer> teen = age.filter(a -> a >= 13);    // Optional[15]
```

### Chaining — the real power ✨

```java
record Address(String city) { }
record User(String name, Address address) { }

Optional<User> user = findUser("Sara");

String city = user
        .map(User::address)
        .map(Address::city)
        .map(String::toUpperCase)
        .orElse("UNKNOWN CITY");
```

Read it: "Take the user → their address → the city → in capitals → or else 'UNKNOWN CITY'."

If the user is missing, **or** has no address, **or** the city is `null` — no crash. You get `"UNKNOWN CITY"`. 🛡️

**Without Optional**, you'd write:

```java
String city = "UNKNOWN CITY";
User u = findUserOrNull("Sara");
if (u != null) {
    Address a = u.address();
    if (a != null) {
        String c = a.city();
        if (c != null) {
            city = c.toUpperCase();
        }
    }
}
```

😵 A staircase of `if (… != null)`. The Optional version is much cleaner!

> 💡 `map` uses `ofNullable` inside — if a step returns `null`, the box becomes empty.

---

## 🔗 Part 7: Optional with Streams

Many stream operations return an Optional (Chapter 36):

```java
List<Integer> numbers = List.of(4, 8, 15, 16, 23, 42);

Optional<Integer> firstBig = numbers.stream().filter(n -> n > 20).findFirst();
System.out.println(firstBig.orElse(-1));   // 23

Optional<Integer> firstHuge = numbers.stream().filter(n -> n > 100).findFirst();
System.out.println(firstHuge.orElse(-1));  // -1

int max = numbers.stream().max(Integer::compare).orElseThrow();   // 42
```

| Stream method | Returns |
|---|---|
| `findFirst()`, `findAny()` | `Optional<T>` |
| `min(...)`, `max(...)` | `Optional<T>` |
| `reduce(...)` (without start value) | `Optional<T>` |
| `IntStream.average()` | `OptionalDouble` |
| `IntStream.max()` | `OptionalInt` |

`OptionalInt`, `OptionalDouble` are versions for primitives. Use `getAsInt()`, `orElse(...)`.

---

## 👍👎 Part 8: Good and bad uses

Optional was made for **one** main purpose: **return values that might be missing**.

| ✅ Do | ❌ Don't |
|---|---|
| Return `Optional<T>` from methods that **might not find** something: `findById`, `findByEmail`, `findFirst` | Use Optional for **fields** in a class: `private Optional<String> nickname;` 👎 |
| Use `orElse`, `orElseThrow`, `map`, `ifPresent` | Use Optional for **method parameters**: `void greet(Optional<String> name)` 👎 |
| Return an **empty list** (not `Optional<List>`) when there are no results | Return `null` from a method whose type is `Optional` 😱 (the box itself must never be null!) |
| | Call `.get()` without checking |
| | Write `if (opt.isPresent()) { opt.get() ... }` everywhere (use `ifPresent` / `map` / `orElse`) |

### Empty collections instead of Optional

```java
// 👎
Optional<List<Order>> findOrders(String customer)

// 👍 — an empty list already means "nothing found"
List<Order> findOrders(String customer)   // returns List.of() if none
```

### Fields: just use null (carefully) or a default

```java
// 👎
private Optional<String> middleName;

// 👍 — keep the field normal, offer an Optional getter
private String middleName;   // may be null

public Optional<String> getMiddleName() {
    return Optional.ofNullable(middleName);
}
```

---

## 🌱 Part 9: Optional in Spring Boot

Spring Data repositories (Chapter 72) return `Optional` for single results:

```java
public interface StudentRepository extends JpaRepository<Student, Long> {
    Optional<Student> findByEmail(String email);
}
```

And in your service:

```java
public Student getStudent(Long id) {
    return studentRepository.findById(id)
            .orElseThrow(() -> new StudentNotFoundException(id));
}

public boolean emailIsTaken(String email) {
    return studentRepository.findByEmail(email).isPresent();
}

public String getStudentName(Long id) {
    return studentRepository.findById(id)
            .map(Student::getName)
            .orElse("Unknown student");
}
```

You now understand **every word** of these lines! 🎉

---

## 💻 Mini project: A user directory 📇

```java
import java.util.*;

public class UserDirectory {

    record User(int id, String name, String email, String city) { }

    static class UserNotFoundException extends RuntimeException {
        UserNotFoundException(int id) {
            super("No user with id " + id);
        }
    }

    private final Map<Integer, User> users = new HashMap<>();

    void add(User user) {
        users.put(user.id(), user);
    }

    Optional<User> findById(int id) {
        return Optional.ofNullable(users.get(id));
    }

    Optional<User> findByEmail(String email) {
        return users.values().stream()
                .filter(u -> email.equalsIgnoreCase(u.email()))
                .findFirst();
    }

    User getById(int id) {
        return findById(id).orElseThrow(() -> new UserNotFoundException(id));
    }

    public static void main(String[] args) {
        UserDirectory dir = new UserDirectory();
        dir.add(new User(1, "Sara", "sara@mail.com", "Cairo"));
        dir.add(new User(2, "Tom", null, "Lagos"));
        dir.add(new User(3, "Lina", "lina@mail.com", null));

        // 1. orElse with map
        System.out.println("User 1: " + dir.findById(1).map(User::name).orElse("?"));
        System.out.println("User 9: " + dir.findById(9).map(User::name).orElse("?"));

        // 2. chaining through values that may be null
        for (int id = 1; id <= 4; id++) {
            String city = dir.findById(id)
                    .map(User::city)
                    .map(String::toUpperCase)
                    .orElse("(unknown city)");
            System.out.println("City of " + id + ": " + city);
        }

        // 3. ifPresentOrElse
        dir.findByEmail("LINA@mail.com").ifPresentOrElse(
                u -> System.out.println("✅ Found by email: " + u.name()),
                () -> System.out.println("❌ Email not found"));

        dir.findByEmail("nobody@mail.com").ifPresentOrElse(
                u -> System.out.println("✅ Found by email: " + u.name()),
                () -> System.out.println("❌ Email not found"));

        // 4. orElseThrow
        try {
            User u = dir.getById(42);
            System.out.println(u);
        } catch (UserNotFoundException e) {
            System.out.println("🚨 " + e.getMessage());
        }
    }
}
```

**Output:**

```
User 1: Sara
User 9: ?
City of 1: CAIRO
City of 2: LAGOS
City of 3: (unknown city)
City of 4: (unknown city)
✅ Found by email: Lina
❌ Email not found
🚨 No user with id 42
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `Optional.ofNullable(users.get(id))` | `get` returns null if missing → turn it into a safe box. |
| `email.equalsIgnoreCase(u.email())` | ⚠️ We call it on `email` (never null), not on `u.email()` (Tom's is null!). A little trick to avoid a NPE. |
| `.map(User::city)` for user 3 | Lina's city is `null` → the box becomes empty → `"(unknown city)"`. No crash! |
| `getById` uses `orElseThrow` | Exactly the Spring Boot style. |

---

## ✋ Try it yourself

**Task 1:** What does each line print?

```java
Optional<String> a = Optional.of("java");
Optional<String> b = Optional.empty();

System.out.println(a.orElse("none"));
System.out.println(b.orElse("none"));
System.out.println(a.map(String::length).orElse(0));
System.out.println(b.map(String::length).orElse(0));
System.out.println(a.filter(s -> s.startsWith("x")).isPresent());
```

<details>
<summary>Click to see the answer</summary>

```
java
none
4
0
false
```

</details>

**Task 2:** Write a method `Optional<Integer> parseNumber(String text)` that returns the number if the text is a valid int, or an empty Optional otherwise (use try/catch from Chapter 33).

<details>
<summary>Click to see the answer</summary>

```java
public static Optional<Integer> parseNumber(String text) {
    try {
        return Optional.of(Integer.parseInt(text.strip()));
    } catch (NumberFormatException e) {
        return Optional.empty();
    }
}

// parseNumber("42").orElse(0)      → 42
// parseNumber("hello").orElse(0)   → 0
```

</details>

**Task 3:** Write `Optional<String> longestWord(List<String> words)` using a stream and `max`. What does it return for an empty list?

**Task 4:** Rewrite this with Optional (no `if`!):

```java
String nickname = findNicknameOrNull(user);
String display;
if (nickname != null) {
    display = nickname.toUpperCase();
} else {
    display = user.name();
}
```

<details>
<summary>Click to see the answer</summary>

```java
String display = Optional.ofNullable(findNicknameOrNull(user))
        .map(String::toUpperCase)
        .orElse(user.name());
```

</details>

**Task 5:** In the User Directory, add a method `Optional<User> findOldestByCity(String city)`... wait, users have no age! 😄 Add an `int age` to the record first, then write the method with a stream, `filter` and `max`.

---

## ⚠️ Common mistakes

### Mistake 1: Calling `get()` on an empty Optional

```
💥 NoSuchElementException: No value present
```

**Fix:** `orElse`, `orElseGet`, `orElseThrow(() -> ...)`.

### Mistake 2: `Optional.of(null)`

```
💥 NullPointerException
```

**Fix:** `Optional.ofNullable(value)`.

### Mistake 3: Returning `null` instead of an empty Optional

```java
public Optional<User> find(int id) {
    return null;   // 😱 the box itself is missing!
}
```

**Fix:** `return Optional.empty();`

### Mistake 4: Treating the Optional like the value

```java
Optional<String> name = find();
name.length();   // ❌ error: cannot find symbol
```

**Fix:** Unwrap it: `name.map(String::length).orElse(0)`.

### Mistake 5: `orElse` with expensive work

```java
user.orElse(loadDefaultUserFromDatabase());   // ⚠️ the database call ALWAYS runs, even if user is present!
user.orElseGet(() -> loadDefaultUserFromDatabase());   // ✅ only runs if needed
```

### Mistake 6: Optional everywhere

Don't use Optional for fields, parameters or collections. It's for **return values** that **might be missing**.

---

## ✅ Summary

- `null` is dangerous: methods don't warn you, and you forget to check → **NullPointerException**. 💥
- **`Optional<T>`** is a box that holds **one value or nothing**. It makes "maybe missing" **visible in the type**. 🎁
- Create: `Optional.of(x)` (not null!), `Optional.ofNullable(x)`, `Optional.empty()`.
- Unwrap safely:
  - `orElse(default)`
  - `orElseGet(() -> default)` (lazy)
  - **`orElseThrow(() -> new SomeException(...))`** ⭐ (Spring Boot favorite)
- Avoid `get()`.
- Act: `ifPresent(...)`, `ifPresentOrElse(..., ...)`.
- Transform: `map(...)`, `filter(...)` — chain them to avoid `if (x != null)` staircases.
- Streams return Optionals from `findFirst`, `min`, `max`.
- Use Optional for **return values** only — not for fields, parameters or collections.
- Spring: `repository.findById(id).orElseThrow(...)`. 🌱

---

## ❓ Quiz

1. Why is `null` dangerous?
2. What is an Optional?
3. What's the difference between `Optional.of(x)` and `Optional.ofNullable(x)`?
4. What does `Optional.empty().orElse("hi")` return?
5. Why should you avoid `get()`?
6. What does `map` do on an empty Optional?
7. Write the Spring Boot-style line that finds a student by id or throws `StudentNotFoundException`.
8. Should a class field be of type `Optional<String>`?

<details>
<summary>Click to see the answers</summary>

1. Methods don't show that they can return null, so people forget to check, and the program crashes with a NullPointerException.
2. A box that contains one value or is empty. It shows clearly that a value might be missing.
3. `of` requires a non-null value (it crashes on null). `ofNullable` creates an empty Optional if the value is null.
4. `"hi"`
5. It throws an exception if the Optional is empty — just as dangerous as null.
6. Nothing — it stays empty.
7. `repository.findById(id).orElseThrow(() -> new StudentNotFoundException(id));`
8. No — use Optional for return values. For fields, use a normal field (and maybe an Optional getter).

</details>

---

[⬅ Previous chapter](36-streams.md) | [Table of Contents](../README.md) | [Next chapter: Annotations ➡](38-annotations.md)
