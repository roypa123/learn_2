# Chapter 38 – Annotations: The `@` Sign

[⬅ Previous chapter](37-optional.md) | [Table of Contents](../README.md) | [Next chapter ➡](39-dates-and-times.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What an **annotation** is (a **label** on your code 🏷️)
- Java's built-in annotations: `@Override`, `@Deprecated`, `@SuppressWarnings`, `@FunctionalInterface`
- Annotations **with values**: `@GetMapping("/hello")`
- **Where** you can put annotations
- **Who reads** annotations, and **when**
- How to make your **own** annotation, and read it (a peek behind the magic ✨)
- A **map of the Spring Boot annotations** you'll meet soon 🌱

> 🌱 **Why this chapter matters:** Spring Boot is **full** of annotations: `@SpringBootApplication`, `@RestController`, `@GetMapping`, `@Service`, `@Entity`, `@Autowired`... They tell Spring **what to do** with your classes. After this chapter, the `@` sign won't be a mystery anymore!

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Annotation** | A **label** with `@` that you put on code (a class, method, field...) to give **extra information**. |
| **Metadata** | "Data about data" — information **about** your code, not the code itself. |
| **Element** | A value inside an annotation: `@Size(max = 50)` → `max` is an element. |
| **Retention** | **How long** an annotation is kept: only in the source code, or also when the program runs. |
| **Reflection** | Java code that **looks at other code** while the program runs (reads classes, methods, annotations). |
| **Framework** | A big library (like Spring) that **calls your code** and reads your annotations. |

---

## 📖 Story: Labels in a moving truck 📦🚚

You're moving to a new house. You put **labels** on your boxes:

```
 📦 "FRAGILE ⚠️"        📦 "KITCHEN 🍳"        📦 "THIS SIDE UP ⬆️"        📦 "OPEN FIRST ⭐"
```

The labels **don't change** what's inside the boxes. Your plates are still plates. 🍽️

But the **movers** 🧑‍🔧 **read** the labels and act differently:
- "FRAGILE" → carry carefully
- "KITCHEN" → put it in the kitchen
- "OPEN FIRST" → put it near the door

**Annotations** are labels on your code:
- They **don't change** what your code does **by themselves**.
- But **tools** (the Java compiler, IntelliJ, **Spring**...) **read** them and **act** on them.

```java
@RestController          ← label: "Spring, this class answers web requests!"
public class HelloController {

    @GetMapping("/hello") ← label: "Spring, call this method for the address /hello!"
    public String hello() {
        return "Hi!";
    }
}
```

---

## 🏷️ Part 1: Annotations you already know

### `@Override` (Chapters 20, 22)

```java
@Override
public String toString() {
    return "Dog";
}
```

**Reader:** the **compiler**. **Meaning:** "I'm overriding a parent's method. Please **check** that it really exists." If you make a typo (`toStrng`), you get an error. 🛡️

### `@FunctionalInterface` (Chapter 35)

```java
@FunctionalInterface
public interface Calculator {
    int calculate(int a, int b);
}
```

**Reader:** the **compiler**. **Meaning:** "This interface must have **exactly one** abstract method." If someone adds a second one → error.

---

## 🧰 Part 2: More built-in annotations

### `@Deprecated` — "don't use this anymore" 🚫

```java
public class Calculator {

    @Deprecated
    public int add(int a, int b, int c) {
        return a + b + c;
    }

    public int add(int... numbers) {
        int sum = 0;
        for (int n : numbers) sum += n;
        return sum;
    }
}
```

When someone uses the old method, IntelliJ shows it with a ~~strikethrough~~ line, and the compiler gives a **warning**: "add(int,int,int) has been deprecated".

👉 *Deprecated* means "old, not recommended, may be removed in the future". You'll see it in Java's own library: old methods like `new Date(2020, 1, 1)` are deprecated. Use the newer way!

You can add more information:

```java
@Deprecated(since = "2.0", forRemoval = true)
```

"Deprecated since version 2.0, and it **will be removed**."

### `@SuppressWarnings` — "I know, stop warning me" 🤫

```java
@SuppressWarnings("unchecked")
List<String> list = (List<String>) someObject;
```

**Reader:** the **compiler**. **Meaning:** "I know this looks risky. Don't show the warning."

> ⚠️ Use it **rarely** and only when you're sure. Warnings usually exist for a good reason!

### `@SafeVarargs`, `@Serial`...

There are a few more, but you'll rarely need them. The important idea: **the compiler reads these labels and checks things for you**.

---

## 🎛️ Part 3: Annotations with values

Some annotations take **values** (called **elements**), written in brackets:

```java
@Deprecated(since = "2.0", forRemoval = true)
@SuppressWarnings("unused")
@SuppressWarnings({"unused", "unchecked"})
```

| Form | Example | Meaning |
|---|---|---|
| No value | `@Override` | just the label |
| One value | `@SuppressWarnings("unused")` | the value for the element called `value` (you can skip the name) |
| Named values | `@Deprecated(since = "2.0", forRemoval = true)` | `name = value`, separated by commas |
| Array value | `@SuppressWarnings({"unused", "unchecked"})` | many values in `{ }` |

You'll see this **a lot** in Spring Boot:

```java
@GetMapping("/students/{id}")                       // one value: the web address
@RequestMapping(value = "/api", method = RequestMethod.GET)   // named values
@Size(min = 2, max = 50)                             // named values: length rules
@Column(name = "first_name", nullable = false)       // named values: database column rules
```

---

## 📍 Part 4: Where can annotations go?

Almost **anywhere**! Usually on the line **above** the thing, or **right before** it:

```java
@Entity                                         // ← on a CLASS
public class Student {

    @Id                                         // ← on a FIELD
    @GeneratedValue
    private Long id;

    @NotBlank                                   // ← many annotations on one thing
    @Size(max = 50)
    private String name;

    public Student(@NotNull String name) {      // ← on a PARAMETER
        this.name = name;
    }

    @Override                                   // ← on a METHOD
    public String toString() {
        return name;
    }
}
```

| Target | Example |
|---|---|
| Class / interface / record / enum | `@RestController`, `@Entity`, `@FunctionalInterface` |
| Method | `@Override`, `@GetMapping`, `@Test` |
| Field | `@Id`, `@Column`, `@Autowired` |
| Parameter | `@PathVariable`, `@RequestBody`, `@NotNull` |
| Constructor | `@Autowired` |

👉 An annotation describes the **thing right after it**.

---

## 👀 Part 5: Who reads annotations? And when?

An annotation does **nothing** by itself. Someone must **read** it. There are three moments:

```
  📝 SOURCE CODE   ──compile──►   📦 .class FILE   ──run──►   🏃 RUNNING PROGRAM
       │                                                          │
   read by:                                                   read by:
   - the compiler                                             - Spring 🌱
     (@Override,                                              - JUnit (tests)
      @FunctionalInterface)                                   - Hibernate (database)
   - IntelliJ                                                 - Jackson (JSON)
   - Lombok (writes code for you)
```

| Who | When | Examples |
|---|---|---|
| The **compiler** | while compiling | `@Override`, `@FunctionalInterface`, `@Deprecated` |
| **Code generators** like Lombok | while compiling | `@Getter`, `@Setter`, `@Builder` (they **write code** for you!) |
| **Frameworks** like Spring | while the program **runs** | `@RestController`, `@Service`, `@Entity`, `@Test` |

### How does Spring read them? (A peek ✨)

When your Spring Boot app starts, Spring **scans** all your classes (in your base package — Chapter 26!) and asks:

> "Does this class have `@RestController`? Then I'll create an object of it, and send web requests to it!"
> "Does this method have `@GetMapping("/hello")`? Then I'll call it when someone visits `/hello`!"

It uses **reflection**: Java code that can look at classes and methods **while the program runs**. You'll see a tiny version of this in Part 6. 🔍

> 💡 This is why people sometimes say Spring Boot is "**magic**" 🪄. It's not magic — it's **annotations + reflection**. Spring reads your labels and does the boring work for you.

---

## 🛠️ Part 6: Make your own annotation (behind the magic)

You won't often make your own annotations as a beginner. But doing it **once** helps you understand how Spring works. Let's build a tiny **validator**, like Spring's `@NotBlank`!

### Step 1: Define the annotation

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
public @interface NotEmpty {
    String message() default "must not be empty";
}
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `public @interface NotEmpty` | `@interface` (with `@`!) defines a **new annotation** called `NotEmpty`. |
| `@Retention(RetentionPolicy.RUNTIME)` | "Keep this label when the program **runs**" — so our code can read it. (Without it, the label disappears after compiling!) |
| `@Target(ElementType.FIELD)` | "This label can only be put on **fields**." |
| `String message() default "must not be empty";` | An **element** called `message`, with a **default** value. It looks like a method, but it's a setting. |

Yes — annotations about annotations! 🤯 (`@Retention` and `@Target` are called **meta-annotations**.)

### Step 2: Use the annotation

```java
public class SignUpForm {
    @NotEmpty(message = "Please enter your name")
    String name;

    @NotEmpty
    String email;

    String nickname;   // no label → optional

    SignUpForm(String name, String email, String nickname) {
        this.name = name;
        this.email = email;
        this.nickname = nickname;
    }
}
```

### Step 3: Write the "reader" (a tiny framework!)

```java
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.List;

public class Validator {

    public static List<String> validate(Object object) {
        List<String> errors = new ArrayList<>();

        for (Field field : object.getClass().getDeclaredFields()) {
            NotEmpty label = field.getAnnotation(NotEmpty.class);
            if (label == null) {
                continue;   // no label → skip this field
            }

            try {
                field.setAccessible(true);
                Object value = field.get(object);
                if (value == null || value.toString().isBlank()) {
                    errors.add(field.getName() + ": " + label.message());
                }
            } catch (IllegalAccessException e) {
                throw new IllegalStateException(e);
            }
        }
        return errors;
    }
}
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `object.getClass()` | "What class is this object?" → `SignUpForm` |
| `.getDeclaredFields()` | "Give me **all the fields** of this class." (Reflection! 🔍) |
| `field.getAnnotation(NotEmpty.class)` | "Does this field have a `@NotEmpty` label? If yes, give it to me. If no → `null`." |
| `field.setAccessible(true)` | "Let me read it, even if it's private." |
| `field.get(object)` | "What is the **value** of this field in this object?" |
| `label.message()` | Read the `message` element from the label. |

### Step 4: Try it

```java
public class Main {
    public static void main(String[] args) {
        SignUpForm good = new SignUpForm("Sara", "sara@mail.com", null);
        SignUpForm bad = new SignUpForm("", null, "Tommy");

        System.out.println("Good form: " + Validator.validate(good));
        System.out.println("Bad form:  " + Validator.validate(bad));
    }
}
```

**Output:**

```
Good form: []
Bad form:  [name: Please enter your name, email: must not be empty]
```

🎉 **You just built a mini Spring-style validator!**

The `SignUpForm` class doesn't contain any checking code. It only has **labels**. The `Validator` reads the labels and does the work. This is **exactly** how Spring Boot's real validation works (Chapter 65):

```java
public record CreateStudentRequest(
        @NotBlank(message = "Name is required") String name,
        @Email String email,
        @Min(5) @Max(120) int age
) { }
```

> ⚠️ **Don't worry about reflection!** You almost never write reflection code in normal Spring Boot work — Spring does it for you. The goal here was only to **see** how annotations are read. 😊

---

## 🌱 Part 7: The Spring Boot annotation map

Here's a **preview** of the annotations you'll meet in the rest of this book. You don't need to remember them now — just notice that they're all **labels** that tell Spring what to do!

### 🚀 Starting the app

| Annotation | On | Meaning | Chapter |
|---|---|---|---|
| `@SpringBootApplication` | the main class | "This is a Spring Boot app. Start here, scan for my classes, set everything up." | 49 |

### 🫘 Beans (objects Spring creates for you)

| Annotation | On | Meaning | Chapter |
|---|---|---|---|
| `@Component` | class | "Spring, please create **one** object of this class and manage it." | 54 |
| `@Service` | class | Same as `@Component`, for **business logic** classes. | 54 |
| `@Repository` | class | Same, for **database** classes. | 54 |
| `@Configuration` + `@Bean` | class + method | "This method creates an object for Spring to manage." | 54 |
| `@Autowired` | constructor/field | "Spring, please **give** me this object (dependency injection)." | 53 |
| `@Value("${app.name}")` | field/parameter | "Put a value from the settings file here." | 55 |

### 🌐 Web

| Annotation | On | Meaning | Chapter |
|---|---|---|---|
| `@RestController` | class | "This class answers web requests with data (JSON)." | 57 |
| `@RequestMapping("/api")` | class/method | "All addresses in this class start with `/api`." | 57 |
| `@GetMapping("/students")` | method | "Call this method for **GET** `/students`." | 57 |
| `@PostMapping`, `@PutMapping`, `@DeleteMapping` | method | Same for POST, PUT, DELETE. | 60–61 |
| `@PathVariable` | parameter | "Take this value from the address: `/students/{id}`." | 58 |
| `@RequestParam` | parameter | "Take this from `?name=Ali`." | 59 |
| `@RequestBody` | parameter | "Turn the JSON body into this object." | 60 |

### 🗄️ Database

| Annotation | On | Meaning | Chapter |
|---|---|---|---|
| `@Entity` | class | "This class is a **table** in the database." | 71 |
| `@Id` | field | "This field is the **primary key** (the unique ID)." | 71 |
| `@GeneratedValue` | field | "The database creates the ID automatically." | 71 |
| `@Column(name = "...")` | field | "Settings for this column." | 71 |
| `@OneToMany`, `@ManyToOne` | field | Relationships between tables. | 75 |
| `@Transactional` | method/class | "Do all of this, or nothing at all." | 79 |

### ✅ Validation

| Annotation | Meaning | Chapter |
|---|---|---|
| `@NotNull`, `@NotBlank`, `@Size`, `@Min`, `@Max`, `@Email` | rules for values | 65 |
| `@Valid` | "Please check the rules on this object." | 65 |

### 🧪 Testing

| Annotation | Meaning | Chapter |
|---|---|---|
| `@Test` | "This method is a test." | 84 |
| `@SpringBootTest` | "Start Spring for this test." | 86 |

### 🧰 Lombok (a popular extra library)

| Annotation | Writes for you |
|---|---|
| `@Getter`, `@Setter` | getters and setters (Chapter 21) |
| `@NoArgsConstructor`, `@AllArgsConstructor` | constructors (Chapter 19) |
| `@ToString`, `@EqualsAndHashCode` | `toString`, `equals`, `hashCode` (Chapter 20) |
| `@Data` | all of the above |

👉 Look at this complete Spring Boot class — you can **already guess** what it does, just by reading the labels!

```java
@RestController
@RequestMapping("/api/students")
public class StudentController {

    private final StudentService studentService;

    public StudentController(StudentService studentService) {
        this.studentService = studentService;
    }

    @GetMapping("/{id}")
    public StudentDto getOne(@PathVariable Long id) {
        return studentService.findById(id);
    }

    @PostMapping
    public StudentDto create(@Valid @RequestBody CreateStudentRequest request) {
        return studentService.create(request);
    }
}
```

📖 "This class answers web requests at `/api/students`. It **receives** a StudentService (dependency injection — Chapter 25!). For **GET** `/api/students/5`, it takes `5` from the path and returns that student. For **POST**, it turns the JSON body into a request object, **checks** it, and creates a student."

🎉 You can read Spring Boot code now!

---

## ✋ Try it yourself

**Task 1:** Make a class with a method `oldGreeting()` marked `@Deprecated`, and a new method `greeting()`. Call the old one in `main`. What does IntelliJ show?

**Task 2:** Remove the `@Override` from a `toString()` method and misspell it as `tostring()`. Run the program and print the object. What happens? Then put `@Override` back. What changes?

<details>
<summary>Click to see the answer</summary>

Without `@Override`, `tostring()` is just a new method — `println` still prints something like `Dog@1b6d3586`, and **no error** appears (a silent bug 🐛). With `@Override`, the compiler shows: `method does not override or implement a method from a supertype`. 🛡️

</details>

**Task 3:** For each annotation, guess who reads it — **compiler** or **Spring (at run time)**?
1. `@Override`
2. `@GetMapping("/home")`
3. `@FunctionalInterface`
4. `@Entity`
5. `@Service`

<details>
<summary>Click to see the answers</summary>

1. Compiler
2. Spring
3. Compiler
4. Spring (via the database library, Hibernate)
5. Spring

</details>

**Task 4 (challenge):** Extend the mini validator with a second annotation `@MaxLength(int value)`. Put `@MaxLength(10)` on `nickname`, and make the validator report `"nickname: must be at most 10 characters"` when it's too long.

<details>
<summary>Click to see a hint</summary>

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
public @interface MaxLength {
    int value();
}
```

In the validator: `MaxLength max = field.getAnnotation(MaxLength.class);` and check `value.toString().length() > max.value()`.

</details>

**Task 5:** Read the `StudentController` example in Part 7 again. Without looking at the explanation, write in your own words what **each** annotation does.

---

## ⚠️ Common mistakes

### Mistake 1: Thinking annotations do things by themselves

An annotation is only a **label**. If nobody reads it, nothing happens. For example, `@NotEmpty` in our example does nothing until `Validator.validate(...)` is called. (In Spring, `@NotBlank` does nothing without `@Valid` — Chapter 65!)

### Mistake 2: Forgetting the import

```java
@GetMapping("/hi")   // ❌ error: cannot find symbol  class GetMapping
```

Annotations are classes too! **Fix:** **Alt + Enter** → import.

### Mistake 3: Annotation in the wrong place

```java
@Override
private String name;   // ❌ error: annotation interface not applicable to this kind of declaration
```

Each annotation has a `@Target` — `@Override` only works on methods.

### Mistake 4: Forgetting `@Retention(RUNTIME)` on your own annotation

Your reflection code finds **nothing**, because the label was thrown away after compiling.

### Mistake 5: Using `@SuppressWarnings` to hide real problems

Warnings are friends. Read them before you silence them. 🤫❌

---

## ✅ Summary

- An **annotation** is a **label** with `@` that adds information to code. 🏷️ It doesn't change the code by itself — **someone reads it**.
- Built-in: `@Override` (check overriding), `@FunctionalInterface`, `@Deprecated` (old, don't use), `@SuppressWarnings` (hide a warning).
- Annotations can have **values**: `@GetMapping("/hi")`, `@Size(min = 2, max = 50)`.
- They can go on classes, methods, fields, parameters, constructors.
- **Readers:** the compiler (while compiling), tools like Lombok (generate code), frameworks like **Spring** (while running, using **reflection**).
- You can define your own: `public @interface MyLabel { ... }` with `@Retention` and `@Target`.
- Spring Boot = **your classes + Spring's annotations**. Spring reads the labels and does the work: creates objects, connects them, answers web requests, talks to the database. 🌱

---

## ❓ Quiz

1. What is an annotation?
2. What does `@Override` do?
3. What does `@Deprecated` mean?
4. Does an annotation change what your code does by itself?
5. Who reads `@GetMapping`? When?
6. What is reflection?
7. What does `@Retention(RetentionPolicy.RUNTIME)` mean?
8. Guess: what does `@Service` on a class tell Spring?

<details>
<summary>Click to see the answers</summary>

1. A label with `@` that adds extra information to code.
2. It asks the compiler to check that the method really overrides a parent's method.
3. The thing is old and should not be used anymore; it may be removed in the future.
4. No — a tool or framework must read it and act on it.
5. Spring, while the program runs (at startup).
6. Java code that looks at classes, methods, fields and annotations while the program runs.
7. The annotation is kept in the running program, so code (like Spring) can read it.
8. "Create and manage an object of this class (it contains business logic), and give it to whoever needs it."

</details>

---

[⬅ Previous chapter](37-optional.md) | [Table of Contents](../README.md) | [Next chapter: Dates and times ➡](39-dates-and-times.md)
