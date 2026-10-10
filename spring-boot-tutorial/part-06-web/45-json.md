# Chapter 45 – JSON: How Computers Send Data

[⬅ Previous chapter](44-http.md) | [Table of Contents](../README.md) | [Next chapter ➡](46-rest-api.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What **JSON** is, and why the whole web uses it
- The **6 kinds of values** in JSON
- **Objects** `{ }` and **arrays** `[ ]`, and how to **nest** them
- The **strict rules** of JSON (and the most common mistakes)
- How JSON **matches Java**: objects ↔ records/classes, arrays ↔ lists
- How to turn Java objects into JSON (and back) with a library
- How Spring Boot does it **automatically** 🌱

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **JSON** | *JavaScript Object Notation.* A simple **text format** for data. Say it like the name "Jason". |
| **Object** | A group of **name → value** pairs in `{ }`. Like a Java object or a Map. |
| **Array** | A **list** of values in `[ ]`. Like a Java List. |
| **Key** | The **name** in a pair: `"name"`. Always in double quotes. |
| **Value** | The data: `"Sara"`, `12`, `true`... |
| **Nested** | Something **inside** something else (an object inside an object). |
| **Serialize** | Turn a Java object **into** JSON text. ☕ → 📄 |
| **Deserialize** | Turn JSON text **into** a Java object. 📄 → ☕ |
| **Jackson** | The library Spring Boot uses to read and write JSON. |

---

## 📖 Story: The universal form 📋

Imagine people from many countries want to send each other information about students. 🌍

- One writes in a notebook: "Sara, twelve years old, likes math".
- One uses a table in Excel.
- One sends a voice message. 🎤

What a mess! 😵 Nobody can read everyone else's format.

So they agree on **one simple form** that **everyone** — and every **computer** — can read:

```json
{
  "name": "Sara",
  "age": 12,
  "likesMath": true
}
```

That form is **JSON**. Java, JavaScript, Python, C#, phones, browsers... **all** of them understand it. It's the **common language** of data on the web. 🗣️🌍

> 💡 In Chapter 44, our server sent **plain text**. Real APIs almost always send **JSON**, with the header `Content-Type: application/json`.

---

## 🧱 Part 1: A first look

```json
{
  "id": 42,
  "name": "Sara Ahmed",
  "email": "sara@school.com",
  "age": 12,
  "active": true,
  "nickname": null,
  "grades": [92, 88, 75],
  "address": {
    "city": "Cairo",
    "country": "Egypt"
  }
}
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `{` | Start of an **object**. |
| `"id": 42,` | Key `"id"`, value **number** `42`. A **comma** separates pairs. |
| `"name": "Sara Ahmed",` | Key `"name"`, value **string** `"Sara Ahmed"`. |
| `"active": true,` | A **boolean** value. |
| `"nickname": null,` | **`null`** = "no value". |
| `"grades": [92, 88, 75],` | An **array** (list) of numbers. |
| `"address": { ... }` | A **nested object** — an object inside the object! ⚠️ No comma after it, because it's the **last** pair. |
| `}` | End of the object. |

It reads almost like English. 😊 That's why everyone likes JSON!

---

## 🔤 Part 2: The 6 kinds of values

JSON has **only 6** kinds of values. That's it! 🎉

| Kind | Example | Java equivalent |
|---|---|---|
| **string** | `"Sara"`, `"hello world"`, `""` | `String` |
| **number** | `42`, `-7`, `3.14`, `1.5e3` | `int`, `long`, `double`... |
| **boolean** | `true`, `false` | `boolean` |
| **null** | `null` | `null` |
| **object** | `{ "a": 1, "b": 2 }` | an object (record/class) or a `Map` |
| **array** | `[1, 2, 3]`, `["a", "b"]`, `[]` | `List` (or an array) |

### Strings 📝

- Always **double** quotes `"..."`. Never single quotes `'...'`!
- Special characters use a backslash (like Java — Chapter 5):

| Write | Means |
|---|---|
| `\"` | a quote inside the text |
| `\\` | a backslash |
| `\n` | a new line |
| `\t` | a tab |
| `\u00e9` | the letter é (Unicode) |

```json
{ "quote": "She said \"Hi!\"", "path": "C:\\Users\\Sara" }
```

### Numbers 🔢

- No quotes: `42`, not `"42"` (that would be a **string**!).
- Decimals use a **dot**: `3.14`.
- No leading zeros: `07` ❌ → `7` ✅.
- JSON has **one** number type — it doesn't care about int vs. double.

### Booleans and null ✅

- Small letters only: `true`, `false`, `null`. Not `True`, not `NULL`, not `"true"`.

---

## 📦 Part 3: Objects `{ }`

An **object** is a group of **key → value** pairs inside curly braces:

```json
{
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "pages": 310,
  "available": true
}
```

| Rule | Example |
|---|---|
| Keys are **strings** in double quotes | `"title"` ✅, `title` ❌ |
| Key and value separated by `:` | `"pages": 310` |
| Pairs separated by `,` | `"a": 1, "b": 2` |
| **No comma after the last pair** | `"available": true }` ✅ |
| Keys should be unique | |
| Order of pairs doesn't matter | `{"a":1,"b":2}` = `{"b":2,"a":1}` |

An empty object: `{}`

🗄️ An object is like a **Map** (Chapter 31) or a Java **object** with fields (Chapter 18).

---

## 📚 Part 4: Arrays `[ ]`

An **array** is an **ordered list** of values inside square brackets:

```json
["apple", "banana", "cherry"]
```

```json
[10, 20, 30]
```

```json
[]
```

Items are separated by commas. The order **matters** (first, second, third...).

### Arrays of objects ⭐ (very common!)

```json
[
  { "id": 1, "name": "Sara", "grade": 92 },
  { "id": 2, "name": "Tom",  "grade": 75 },
  { "id": 3, "name": "Lina", "grade": 88 }
]
```

This is what an API sends when you ask "**give me all students**" (`GET /api/students`). 🎓🎓🎓

In Java: a `List<Student>`.

> 💡 Technically, an array **may** mix types (`[1, "two", true]`), but **don't** do that. Keep all items the **same** kind — it makes life easy for Java.

---

## 🪆 Part 5: Nesting — boxes inside boxes

Objects and arrays can be placed **inside** each other, as deep as you need:

```json
{
  "school": "Green Hill",
  "classes": [
    {
      "name": "5A",
      "teacher": { "name": "Mr. Brown", "subject": "Math" },
      "students": [
        { "name": "Sara", "hobbies": ["chess", "piano"] },
        { "name": "Ali",  "hobbies": [] }
      ]
    },
    {
      "name": "5B",
      "teacher": { "name": "Ms. Green", "subject": "Science" },
      "students": [
        { "name": "Tom", "hobbies": ["football"] }
      ]
    }
  ]
}
```

### 🔍 How to read it — like a folder tree 🌳

```
 📦 (object)
  ├── school: "Green Hill"
  └── classes: 📚 (array)
        ├── [0] 📦
        │     ├── name: "5A"
        │     ├── teacher: 📦 { name: "Mr. Brown", subject: "Math" }
        │     └── students: 📚
        │           ├── [0] 📦 { name: "Sara", hobbies: 📚 ["chess", "piano"] }
        │           └── [1] 📦 { name: "Ali",  hobbies: 📚 [] }
        └── [1] 📦
              ├── name: "5B"
              ├── teacher: 📦 { name: "Ms. Green", ... }
              └── students: 📚 [ { name: "Tom", ... } ]
```

**Question:** What is Sara's second hobby?
**Path:** `classes` → item `[0]` → `students` → item `[0]` → `hobbies` → item `[1]` → **`"piano"`** 🎹

> 💡 **Tip:** Good indentation (spaces at the start of lines) makes JSON easy to read. IntelliJ formats JSON with **Ctrl + Alt + L**. Most tools also have a "pretty print" button.

---

## ⚠️ Part 6: JSON is STRICT — the rules

JSON looks like JavaScript or Java, but it's **very strict**. One small mistake → the **whole** text is invalid, and the server answers **400 Bad Request**. 😱

| ❌ Wrong | ✅ Right | Rule |
|---|---|---|
| `{ name: "Sara" }` | `{ "name": "Sara" }` | Keys need **double quotes** |
| `{ 'name': 'Sara' }` | `{ "name": "Sara" }` | Only **double** quotes, never single |
| `{ "a": 1, "b": 2, }` | `{ "a": 1, "b": 2 }` | **No comma** after the last item |
| `[1, 2, 3,]` | `[1, 2, 3]` | No trailing comma in arrays either |
| `{ "a": 1 "b": 2 }` | `{ "a": 1, "b": 2 }` | Comma **between** pairs |
| `{ "ok": True }` | `{ "ok": true }` | Small letters: `true`, `false`, `null` |
| `{ "n": 007 }` | `{ "n": 7 }` | No leading zeros |
| `{ "price": 4,50 }` | `{ "price": 4.50 }` | Decimal **dot** |
| `{ "a": 1 } // comment` | `{ "a": 1 }` | **No comments** in JSON! |
| `{ "a": undefined }` | `{ "a": null }` | Only the 6 value kinds |

### How to check your JSON ✅

- **IntelliJ:** create a file ending in `.json` — errors are shown in **red**. 🔴
- **Online:** search for "JSON validator" (for example *jsonlint.com*) and paste your text.

---

## ☕ Part 7: JSON ↔ Java

When JSON comes into a Spring Boot app, it becomes a **Java object**. When a Java object leaves, it becomes **JSON**. Here's how they match:

| JSON | Java |
|---|---|
| object `{ }` | a **record** or **class** (or `Map<String, Object>`) |
| array `[ ]` | `List<...>` (or an array) |
| string `"..."` | `String` (also `LocalDate`, enums...) |
| number | `int`, `long`, `double`, `BigDecimal`... |
| `true` / `false` | `boolean` |
| `null` | `null` |
| key name | field / component name |

### Example

**JSON:**

```json
{
  "name": "Sara",
  "age": 12,
  "hobbies": ["chess", "piano"],
  "address": { "city": "Cairo", "country": "Egypt" },
  "level": "BEGINNER",
  "birthday": "2013-05-20"
}
```

**Java (records — Chapter 29):**

```java
public record Address(String city, String country) { }

public enum Level { BEGINNER, INTERMEDIATE, EXPERT }

public record Student(
        String name,
        int age,
        List<String> hobbies,
        Address address,
        Level level,
        LocalDate birthday
) { }
```

### 🔍 How they match

| JSON | Java |
|---|---|
| `"name": "Sara"` | `String name` |
| `"age": 12` | `int age` |
| `"hobbies": [...]` | `List<String> hobbies` (Chapter 30) |
| `"address": { ... }` | `Address address` — a **nested record** for the nested object |
| `"level": "BEGINNER"` | `Level level` — an **enum** (Chapter 28)! The text must match a constant name. |
| `"birthday": "2013-05-20"` | `LocalDate birthday` — ISO date text (Chapter 39)! |

👉 **The key names must match the Java names** (`"name"` ↔ `name`). That's why JSON keys are usually in **camelCase**: `firstName`, `createdAt`... — just like Java! 🐫

---

## 🔄 Part 8: Serialize and deserialize — try it!

A **library** does the conversion. Spring Boot uses one called **Jackson**. To practice in plain Java, let's use **Gson** (you added it in Chapter 40!), which works the same way.

In your `hello-maven` project (with the Gson dependency):

```java
package com.example;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import java.util.List;

public class JsonDemo {

    record Address(String city, String country) { }

    record Student(String name, int age, List<String> hobbies, Address address) { }

    public static void main(String[] args) {
        Gson gson = new GsonBuilder().setPrettyPrinting().create();

        // ☕ → 📄  Java object to JSON (serialize)
        Student sara = new Student("Sara", 12, List.of("chess", "piano"), new Address("Cairo", "Egypt"));
        String json = gson.toJson(sara);
        System.out.println("=== Java → JSON ===");
        System.out.println(json);

        // 📄 → ☕  JSON to Java object (deserialize)
        String incoming = """
                {
                  "name": "Tom",
                  "age": 13,
                  "hobbies": ["football"],
                  "address": { "city": "Lagos", "country": "Nigeria" }
                }
                """;
        Student tom = gson.fromJson(incoming, Student.class);
        System.out.println("=== JSON → Java ===");
        System.out.println(tom);
        System.out.println(tom.name() + " lives in " + tom.address().city());

        // 📄 → ☕  A JSON array to a List
        String listJson = """
                [ {"name": "Ali", "age": 11, "hobbies": [], "address": null},
                  {"name": "Lina", "age": 12, "hobbies": ["art"], "address": null} ]
                """;
        List<Student> students = gson.fromJson(listJson, new TypeToken<List<Student>>() { }.getType());
        System.out.println("=== JSON array → List ===");
        students.forEach(s -> System.out.println("- " + s.name() + " (" + s.age() + ")"));
    }
}
```

**Output:**

```
=== Java → JSON ===
{
  "name": "Sara",
  "age": 12,
  "hobbies": [
    "chess",
    "piano"
  ],
  "address": {
    "city": "Cairo",
    "country": "Egypt"
  }
}
=== JSON → Java ===
Student[name=Tom, age=13, hobbies=[football], address=Address[city=Lagos, country=Nigeria]]
Tom lives in Lagos
=== JSON array → List ===
- Ali (11)
- Lina (12)
```

### 🔍 Key lines

| Code | Meaning |
|---|---|
| `gson.toJson(sara)` | **Serialize**: Java object → JSON text. ☕ → 📄 |
| `gson.fromJson(incoming, Student.class)` | **Deserialize**: JSON text → a `Student` object. 📄 → ☕ |
| `"""..."""` | A **text block** (Chapter 9) — perfect for JSON in Java code! |
| `new TypeToken<List<Student>>() { }.getType()` | A trick to tell Gson "I want a **List of Students**" (because of **type erasure** — Chapter 34!). Don't worry about it; Spring Boot handles this for you. |

---

## 🌱 Part 9: JSON in Spring Boot — automatic! ✨

In Spring Boot, you **never** call `toJson` or `fromJson` yourself. **Jackson** does it **automatically**:

```java
@RestController
public class StudentController {

    @GetMapping("/api/students/1")
    public Student getOne() {
        return new Student("Sara", 12, List.of("chess"), new Address("Cairo", "Egypt"));
        // ☕ → 📄 Spring turns this into JSON automatically!
    }

    @PostMapping("/api/students")
    public Student create(@RequestBody Student student) {
        // 📄 → ☕ Spring already turned the incoming JSON into a Student!
        return student;
    }
}
```

| Direction | What you write | What Spring does |
|---|---|---|
| Response ☕ → 📄 | `return student;` | Jackson **serializes** it, sets `Content-Type: application/json`. |
| Request 📄 → ☕ | `@RequestBody Student student` | Jackson **deserializes** the body. If the JSON is broken → **400 Bad Request**. |

🎉 That's one of the biggest reasons people love Spring Boot!

### Useful Jackson annotations (preview)

| Annotation | Meaning |
|---|---|
| `@JsonProperty("first_name")` | use a different key name in JSON |
| `@JsonIgnore` | never put this field in JSON (for example, a password! 🔐) |
| `@JsonFormat(pattern = "dd/MM/yyyy")` | a special date format |
| `@JsonInclude(JsonInclude.Include.NON_NULL)` | leave out fields that are `null` |

---

## ✋ Try it yourself

**Task 1:** Find the **5 mistakes** in this JSON:

```
{
  name: "Lina",
  'age': 12,
  "active": True,
  "scores": [90, 85, 77,],
  "city": "Paris"
  "pet": null
}
```

<details>
<summary>Click to see the answer</summary>

1. `name` has no quotes → `"name"`
2. `'age'` uses single quotes → `"age"`
3. `True` → `true`
4. Trailing comma in the array → `[90, 85, 77]`
5. Missing comma after `"city": "Paris"`

```json
{
  "name": "Lina",
  "age": 12,
  "active": true,
  "scores": [90, 85, 77],
  "city": "Paris",
  "pet": null
}
```

</details>

**Task 2:** Write JSON for **yourself**: name, age, a list of 3 favorite foods, and an object `favoriteBook` with `title` and `author`.

**Task 3:** Write JSON for an **array of 3 products**, each with `id`, `name`, `price` (decimal) and `inStock` (boolean).

<details>
<summary>Click to see one possible answer</summary>

```json
[
  { "id": 1, "name": "Pencil", "price": 0.99, "inStock": true },
  { "id": 2, "name": "Notebook", "price": 2.50, "inStock": true },
  { "id": 3, "name": "Backpack", "price": 24.90, "inStock": false }
]
```

</details>

**Task 4:** In the nested "school" JSON in Part 5, write the **path** to: (a) the subject of 5B's teacher; (b) Tom's first hobby.

<details>
<summary>Click to see the answer</summary>

(a) `classes` → `[1]` → `teacher` → `subject` = `"Science"`
(b) `classes` → `[1]` → `students` → `[0]` → `hobbies` → `[0]` = `"football"`

</details>

**Task 5:** Write the Java **records** that match the JSON from Task 3. Then use Gson to read it into a `List<Product>` and print the total price of products **in stock**.

**Task 6:** What happens if you use Gson to read `{"name": "Sara", "age": "twelve"}` into the `Student` record? Try it! (Hint: think about the 400 error in Spring Boot.)

---

## ⚠️ Common mistakes

### Mistake 1: Trailing commas

```json
{ "a": 1, "b": 2, }   ❌
```

The most common JSON error! Remove the last comma.

### Mistake 2: Single quotes or no quotes around keys

JavaScript allows `{ name: 'Sara' }` — JSON does **not**. Use `{ "name": "Sara" }`.

### Mistake 3: Numbers as strings (or the other way)

```json
{ "age": "12" }   ← a String, not a number!
```

Java may fail to put `"12"` into an `int` (or convert it silently, depending on the library). Send numbers **without** quotes.

### Mistake 4: Key names don't match Java names

```json
{ "Name": "Sara" }   ← capital N
```

```java
record Student(String name) { }   // name stays null!
```

Names are **case-sensitive**. Match them exactly — or use `@JsonProperty`.

### Mistake 5: Comments in JSON

```json
{ "a": 1 }  // the answer   ❌
```

JSON has **no** comments.

### Mistake 6: Forgetting `Content-Type: application/json`

The server may not read your JSON body (Chapter 44 → **415 Unsupported Media Type**). Tools like Postman set it for you when you choose "JSON" (Chapter 47).

---

## ✅ Summary

- **JSON** is a simple **text format** for data that **every** language understands. 🌍
- **6 value kinds:** string `"..."`, number `42`, boolean `true`/`false`, `null`, object `{ }`, array `[ ]`.
- **Object** = `{ "key": value, ... }` → a Java record/class or Map.
- **Array** = `[ value, value, ... ]` → a Java `List`.
- Objects and arrays can be **nested** as deep as needed. 🪆
- **Strict rules:** double quotes on keys and strings, no trailing commas, no comments, small `true`/`false`/`null`, dot for decimals.
- **Serialize** ☕ → 📄 and **deserialize** 📄 → ☕ with a library (Jackson in Spring Boot, Gson for practice).
- Key names must **match** Java field names (camelCase 🐫).
- **Spring Boot does it automatically:** `return object;` → JSON; `@RequestBody` → object. 🌱✨

---

## ❓ Quiz

1. What does JSON stand for?
2. Name the 6 kinds of values in JSON.
3. What's the difference between `{ }` and `[ ]`?
4. Is this valid JSON? `{ "ok": true, }`
5. Which Java type matches a JSON array?
6. What is "serialize"? What is "deserialize"?
7. In Spring Boot, which annotation turns the request's JSON body into a Java object?
8. What does `"birthday": "2013-05-20"` become in Java, if the field type is `LocalDate`?

<details>
<summary>Click to see the answers</summary>

1. JavaScript Object Notation.
2. string, number, boolean, null, object, array.
3. `{ }` is an object (key → value pairs). `[ ]` is an array (an ordered list).
4. No — there's a trailing comma.
5. `List` (or an array).
6. Serialize: Java object → JSON text. Deserialize: JSON text → Java object.
7. `@RequestBody`
8. A `LocalDate` for May 20, 2013 (ISO format is understood automatically).

</details>

---

[⬅ Previous chapter](44-http.md) | [Table of Contents](../README.md) | [Next chapter: What is a REST API? ➡](46-rest-api.md)
