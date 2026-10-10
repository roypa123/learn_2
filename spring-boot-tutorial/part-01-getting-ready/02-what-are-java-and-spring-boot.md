# Chapter 2 – What are Java and Spring Boot?

[⬅ Previous chapter](01-what-is-programming.md) | [Table of Contents](../README.md) | [Next chapter ➡](03-install-java.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What **Java** is, and why so many people use it
- What the **JDK** and the **JVM** are
- What **Spring** and **Spring Boot** are
- What kind of things we will **build** in this book

Again, there is **no code to install** in this chapter. Only ideas.

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Java** | A programming language. We use it in this whole book. |
| **JDK** | *Java Development Kit.* The box of tools you install to **write and run** Java. |
| **JVM** | *Java Virtual Machine.* The part that **runs** Java programs. |
| **Compiler** | A tool that translates your code. In Java it is called `javac`. |
| **Library** | Code that other people already wrote, that you can use for free. |
| **Framework** | A big set of libraries plus rules. It gives your program a ready "skeleton". |
| **Spring** | A very popular Java framework. |
| **Spring Boot** | A part of Spring that makes starting a project **very easy and fast**. |
| **Server** | A computer (or program) that waits for questions and sends answers. |
| **Web application** | A program that people use through the internet. |
| **API** | A "door" that lets one program talk to another program. |

---

## ☕ Part 1: What is Java?

**Java** is a programming language. It was made in **1995** by a company called Sun Microsystems. Today the company **Oracle** takes care of it, together with many other people around the world.

The logo of Java is a **cup of coffee** ☕ — "Java" is also a word for coffee.

### Where is Java used?

Java is everywhere. Some examples:

| Place | Example |
|---|---|
| 🏦 Banks | Money transfer systems |
| 🛒 Online shops | The "server" part of big shopping websites |
| 📱 Android phones | Many Android apps were built with Java |
| 🏢 Big companies | Systems for workers, salaries, orders |
| 🎮 Games | *Minecraft* was made with Java |

👉 Because Java is used so much, **many companies want Java programmers**. Learning Java is good for getting a job.

### Why is Java good for beginners?

1. **Clear rules.** Java is strict. This sounds bad, but it is good: the compiler finds many mistakes **before** your program runs.
2. **Huge community.** Millions of people use Java. If you have a question, someone already asked it on the internet.
3. **Free.** You can download and use Java for free.
4. **Works on every computer.** Windows, Mac, Linux — the same Java code runs on all of them.

---

## ⚙️ Part 2: How does Java run? (JDK and JVM)

Remember from Chapter 1: a computer only understands 0 and 1. And different computers (Windows, Mac) understand **different** 0 and 1.

Java has a clever idea to solve this.

### 📖 Story: The translator in every country

Imagine you write a book in your language. You want people in **every country** to read it.

**Bad idea:** Write the book again in 100 languages. That is too much work! 😩

**Java's idea:**
1. You write the book **once**, in a special simple language that is the same everywhere.
2. In every country there is a **translator** who reads this special language and explains it to the people there.

In Java:

- The **special simple language** is called **bytecode**.
- The **translator** in every country is the **JVM** (Java Virtual Machine).

```
                        ┌─────────────┐
                    ┌──►│ JVM Windows │──► runs on Windows 🪟
 ┌────────┐  javac  │   └─────────────┘
 │ Your   │ ──────► │   ┌─────────────┐
 │ Java   │ bytecode├──►│ JVM Mac     │──► runs on Mac 🍎
 │ code   │         │   └─────────────┘
 └────────┘         │   ┌─────────────┐
                    └──►│ JVM Linux   │──► runs on Linux 🐧
                        └─────────────┘
```

The famous Java sentence is:

> **"Write once, run anywhere."**

### Step by step

1. You write a file called `Hello.java`. This is your **source code** (normal text).
2. The compiler `javac` turns it into `Hello.class`. This is **bytecode**.
3. The **JVM** reads `Hello.class` and runs it on your computer.

### What is the JDK?

The **JDK** (Java Development Kit) is the **toolbox** you install. Inside it:

| Tool inside the JDK | What it does |
|---|---|
| `javac` | The **compiler**. Turns `.java` into `.class`. |
| `java` | Starts the **JVM** and runs your program. |
| Many libraries | Ready-made code for text, math, dates, files, internet and much more. |

👉 **Easy rule:** Install the **JDK**, and you have everything. We do this in Chapter 3.

---

## 🌱 Part 3: What is Spring?

### 📖 Story: Building a house

You want to build a house. 🏠

**Way 1: Do everything yourself.**
You make your own bricks. You cut your own wood. You make your own windows, doors, pipes, electric wires...
This takes **years**. And you will make many mistakes.

**Way 2: Use ready-made parts.**
You buy bricks, doors and windows from a shop. You follow a good plan.
You only do the parts that make **your** house special — the colors, the rooms, the garden.
This is **much faster** and **safer**.

**Spring is Way 2 for programs.**

Many programs need the same things:

- Talking to a **database** (a place to save data)
- Answering requests from the **internet**
- **Login** and passwords (security)
- Sending **emails**
- Writing **logs** (a diary of what the program does)

Spring gives you **ready-made, well-tested parts** for all of these.
You only write the part that makes **your** program special.

The logo of Spring is a green **leaf** 🌱.

---

## 🚀 Part 4: What is Spring Boot?

Spring is very powerful. But in the past, starting a Spring project was **hard**. You needed to write many settings files before you could even say "Hello".

**Spring Boot** fixes this.

### 📖 Story: The furnished apartment

- **Spring** = An empty house with all the parts in boxes. You must put everything together yourself. 📦📦📦
- **Spring Boot** = A **furnished apartment**. The bed, the table, the lights — everything is already set up. You just bring your bag and move in. 🛋️

Spring Boot gives you:

| Feature | Meaning |
|---|---|
| **Starters** | Ready packages. Want a website? Add the "web" starter. Want a database? Add the "data" starter. |
| **Auto-configuration** | Spring Boot **guesses good settings** for you. You change them only if you want. |
| **Built-in server** | Your app has its own small web server inside. You just press "Run". |
| **Spring Initializr** | A website that creates a new project for you in seconds. |

With Spring Boot, a working web server needs only a few lines of code. Here is a **sneak peek**. Don't worry — you will understand every word later (Chapter 52):

```java
@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello from Spring Boot!";
    }
}
```

When this program runs, you can open a web browser, go to `http://localhost:8080/hello`, and you will see:

```
Hello from Spring Boot!
```

### 🔍 Very short explanation (details come later)

| Line | Simple meaning |
|---|---|
| `@RestController` | "This class answers requests from the internet." |
| `public class HelloController {` | "Here starts a part of the program called HelloController." |
| `@GetMapping("/hello")` | "When someone visits the address `/hello`..." |
| `public String hello() {` | "...do this job called `hello`, which gives back some text..." |
| `return "Hello from Spring Boot!";` | "...and the text is: Hello from Spring Boot!" |
| `}` | "End of the job." |
| `}` | "End of HelloController." |

Just 7 lines, and you have a working web server! That is the power of Spring Boot. 💪

---

## 🗺️ Part 5: Our road in this book

Here is the plan. Each step uses the step before it.

```
 Step 1          Step 2           Step 3          Step 4           Step 5
┌────────┐     ┌──────────┐     ┌─────────┐     ┌───────────┐     ┌──────────┐
│ Set up │ ──► │  Java    │ ──► │ Objects │ ──► │ How the   │ ──► │ Spring   │
│ tools  │     │  basics  │     │ in Java │     │ web works │     │ Boot!    │
└────────┘     └──────────┘     └─────────┘     └───────────┘     └──────────┘
 Ch. 1–5        Ch. 6–17         Ch. 18–42        Ch. 43–47        Ch. 48–100
```

👉 Many people want to jump directly to Spring Boot. **Please don't.** Spring Boot is built on Java. If you know Java well, Spring Boot will feel easy. If you skip Java, Spring Boot will feel like magic you cannot control. 🪄😵

### What will we build?

During this book you will build:

- Small Java programs: a calculator, a guessing game, a shopping list
- A **Student API**: add, see, change and delete students
- A **Library app** (final project): books, members, borrowing, login and security

---

## ✋ Try it yourself

No computer needed again. Think and write your answers.

**Task 1:** In your own words, explain the difference between the **JDK** and the **JVM**. Use the "translator" story if it helps.

**Task 2:** Think of an app you use every day (for example: a bank app, a shopping app, a food delivery app).
Write a list of things the "server" part must do. For example:
- Save the list of products
- Check the password when someone logs in
- ...

These are exactly the things Spring Boot helps with!

---

## ⚠️ Common mistakes (in thinking)

| Wrong idea | The truth |
|---|---|
| "Java and JavaScript are the same." | **No!** They are two very different languages. The names are similar only because of old marketing. "Java is to JavaScript like car is to carpet." 🚗 vs 🧶 |
| "Spring Boot is a different language." | No. Spring Boot is **Java**. It is Java code plus ready-made parts. |
| "I can learn Spring Boot without Java." | You will be lost. Learn Java first (Parts 2–4 of this book). |
| "I need to pay for Java." | No. The JDK we use (Eclipse Temurin) is free. Spring Boot is also free. |

---

## ✅ Summary

- **Java** is a popular, free, strict and clear programming language.
- Java code → `javac` compiles it → **bytecode** → the **JVM** runs it.
- "**Write once, run anywhere.**" The JVM makes Java work on every computer.
- The **JDK** is the toolbox you install. It has `javac`, `java`, and many libraries.
- **Spring** is a framework: ready-made parts for databases, web, security and more.
- **Spring Boot** makes Spring very easy to start: good default settings, a built-in server, and starters.
- We learn **Java first**, then the web, then Spring Boot.

---

## ❓ Quiz

1. What does JDK mean, and what is inside it?
2. What does the JVM do?
3. What does "Write once, run anywhere" mean?
4. In the house story, what is Spring?
5. What is the difference between Spring and Spring Boot?
6. Are Java and JavaScript the same?

<details>
<summary>Click to see the answers</summary>

1. Java Development Kit. It has the compiler (`javac`), the program runner (`java`), and many libraries.
2. It runs Java bytecode on your computer. It is the "translator".
3. You write and compile your Java code one time, and it runs on Windows, Mac and Linux without changes.
4. The ready-made parts (bricks, doors, windows) so you don't need to make everything yourself.
5. Spring is the big framework. Spring Boot makes it very easy and fast to start a Spring project, with good default settings.
6. No. They are two different languages.

</details>

---

[⬅ Previous chapter](01-what-is-programming.md) | [Table of Contents](../README.md) | [Next chapter: Install Java ➡](03-install-java.md)
