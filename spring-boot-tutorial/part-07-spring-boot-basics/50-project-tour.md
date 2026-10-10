# Chapter 50 – A tour of the project folders

[⬅ Previous chapter](49-spring-initializr.md) | [Table of Contents](../README.md) | [Next chapter ➡](51-run-first-app.md)

---

## 🎯 Goal

You have a new project called **`hello`**. It has many folders and files. What are they all? 🤔

At the end of this chapter you will know:

- What **every folder and file** in a Spring Boot project is for
- The main class **`HelloApplication`**, line by line
- What **`@SpringBootApplication`** really means (it's 3 annotations in 1!)
- The **base package rule** — the most common beginner trap ⚠️
- What the test class does, and how to run it ✅
- Which files you will **edit** often, and which ones you can **ignore**

> 🌱 Open your **`hello`** project in IntelliJ now. We'll walk through it together, like a tour guide in a new house. 🏠🚶

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Main class** | The class with the `main` method. Your app **starts** here. |
| **Base package** | The package of the main class (`com.example.hello`). Spring looks for your classes **here and below**. |
| **Component scan** | Spring **searching** your packages for classes with labels like `@RestController`. 🔍 |
| **Resources** | Files that are **not Java code**, but your app needs them: settings, web pages, pictures. |
| **Static files** | Files the server sends **as they are**: HTML, CSS, pictures. "Static" = they don't change. |
| **Template** | An HTML page with **holes** that the server fills with data (Chapter 89). |
| **Classpath** | The list of places where Java looks for classes and resources when the app runs. |
| **Build output** | The files Maven **makes** from your code (in the `target` folder). |

---

## 📖 Story: A tour of a new house 🏠

You just moved into a new house. A guide shows you around:

- "This is the **front door** 🚪 — everyone comes in here." → `HelloApplication.java`
- "This is the **living room** 🛋️ — you'll spend most of your time here." → `src/main/java`
- "This is the **control panel** 🎛️ for lights and heating." → `application.properties`
- "This is the **window display** 🪟 — people outside can see it." → `static/`
- "This is the **safety-check room** 🧪." → `src/test`
- "This is the **storage room** 📦 — machines put things here. Don't keep your own stuff here!" → `target/`
- "And this is the **instruction manual** 📖 for the house builder." → `pom.xml`

Let's take the tour! 🚶

---

## 🗺️ Part 1: The map

Here is the **whole** project (on your disk), with a short note for each part:

```
hello/                                   ← 🏠 the project folder
├── .idea/                               ← IntelliJ's own settings (ignore)
├── .mvn/
│   └── wrapper/
│       └── maven-wrapper.properties     ← which Maven version the wrapper uses
├── src/
│   ├── main/                            ← 🛋️ YOUR APP
│   │   ├── java/
│   │   │   └── com/example/hello/
│   │   │       └── HelloApplication.java   ← 🚪 the front door (main class)
│   │   └── resources/
│   │       ├── static/                  ← 🪟 HTML, CSS, pictures (sent as they are)
│   │       ├── templates/               ← HTML pages with "holes" (Chapter 89)
│   │       └── application.properties   ← 🎛️ settings (Chapter 55)
│   └── test/                            ← 🧪 TESTS
│       └── java/
│           └── com/example/hello/
│               └── HelloApplicationTests.java
├── target/                              ← 📦 build output (made by Maven, appears later)
├── .gitattributes                       ← Git: how to save line endings
├── .gitignore                           ← Git: which files NOT to save
├── HELP.md                              ← useful links
├── mvnw                                 ← Maven Wrapper for Mac/Linux
├── mvnw.cmd                             ← Maven Wrapper for Windows
└── pom.xml                              ← 📖 the project's instructions for Maven
```

Does this look familiar? It's the **standard Maven layout** from **Chapter 40**! ✅ Spring Boot just adds a few things.

Let's visit each part. 🚶

---

## 🚪 Part 2: The front door — `HelloApplication.java`

Open **`src/main/java/com/example/hello/HelloApplication.java`**. Here's the real file:

```java
package com.example.hello;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class HelloApplication {

	public static void main(String[] args) {
		SpringApplication.run(HelloApplication.class, args);
	}

}
```

Only **13 lines**! But this is the most important class in the project. Let's read it.

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `package com.example.hello;` | This class lives in the package `com.example.hello` (Chapter 26). ⭐ This is the **base package**. |
| `import org.springframework.boot.SpringApplication;` | We use the class `SpringApplication` from Spring Boot. |
| `import org.springframework.boot.autoconfigure.SpringBootApplication;` | We use the annotation `@SpringBootApplication` from Spring Boot. |
| `@SpringBootApplication` | ⭐ The **big label**: "This is a Spring Boot app! Turn on all the Spring Boot magic." (Part 3 explains it.) |
| `public class HelloApplication {` | A normal public class. Its name = your project name + `Application`. |
| `public static void main(String[] args) {` | The **normal** Java `main` method (Chapter 5). Java starts here. ☕ |
| `SpringApplication.run(HelloApplication.class, args);` | ⭐ "Spring Boot, **start** the app!" This one line does **everything** from Chapter 48, Part 7: read settings, scan, create beans, start Tomcat... |
| `HelloApplication.class` | We tell Spring: "**This** class is the main one. Read its labels, and start searching from **its** package." |
| `args` | The command-line words given to the program (Chapter 5). Spring Boot can read settings from them, like `--server.port=9090` (Chapter 55). |
| `}` `}` | The end of the method and the class. |

> 💡 **Tabs, not spaces?** Spring Initializr uses **tabs** for indentation in this file. That's why it may look a little different from the code in this book (we use 4 spaces). Both are fine! IntelliJ can change it: **Code → Reformat Code** (Ctrl + Alt + L).

> ⚠️ **Don't rename or move this class without a good reason.** And don't delete it! Without it, your app has no front door. 🚪❌

---

## 🏷️ Part 3: `@SpringBootApplication` = 3 labels in 1

`@SpringBootApplication` is a **shortcut**. It's like a "combo meal" 🍔🍟🥤 — three things in one box:

```
@SpringBootApplication  =   @SpringBootConfiguration       🍔
                          + @EnableAutoConfiguration       🍟
                          + @ComponentScan                 🥤
```

| Inside label | What it says | Simple meaning |
|---|---|---|
| `@SpringBootConfiguration` | "This class is a **configuration** class." | "You may put settings and `@Bean` methods here." (Chapter 54) |
| `@EnableAutoConfiguration` | "Turn on **auto-configuration**." 🪄 | "Look at my libraries and set things up for me." (Chapter 48) |
| `@ComponentScan` | "**Scan** for components." 🔍 | "Search **this package and all packages below it** for classes with labels like `@RestController` and `@Service`." |

Want to see it with your own eyes? 👀 In IntelliJ, hold **Ctrl** (Mac: **Cmd**) and **click** on `SpringBootApplication`. IntelliJ opens the real source code of the annotation. You'll see (simplified):

```java
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = { ... })
public @interface SpringBootApplication {
    ...
}
```

It's an **annotation with annotations on it** — just like you learned in Chapter 38. 🤓 Close the tab when you're done (you can't change it anyway — it's Spring's code, not yours).

---

## ⚠️ Part 4: The base package rule (very important!)

Remember from Chapter 26: "All your classes must be in the base package **or below it**." Now you understand **why**: because of **`@ComponentScan`**! 🔍

Spring starts searching at the package of `HelloApplication`: **`com.example.hello`**. It searches **down**, never **up** or **sideways**.

```
com
└── example
    ├── hello                         ← 🔍 Spring starts HERE (base package)
    │   ├── HelloApplication.java
    │   ├── HelloController.java      ✅ found
    │   ├── student
    │   │   └── StudentController.java ✅ found (below the base package)
    │   └── shop
    │       └── ShopService.java      ✅ found (below the base package)
    └── other
        └── OutsideController.java    ❌ NOT found (sideways — outside!)
```

What happens to `OutsideController`? It's **silently ignored**. 😱 No error! Your endpoint just doesn't work, and you get a **404 Not Found**. We tested this for real — a controller in `com.example.other` with a `/outside` endpoint:

```
curl http://localhost:8080/outside
```
```json
{"timestamp":"2026-10-10T16:42:53.750Z","status":404,"error":"Not Found","path":"/outside"}
```

Spring never even **looked** in that package. 🙈

| Your class is in... | Found by Spring? |
|---|---|
| `com.example.hello` | ✅ yes (same package) |
| `com.example.hello.student` | ✅ yes (below) |
| `com.example.hello.a.b.c` | ✅ yes (far below — still below!) |
| `com.example` | ❌ no (above) |
| `com.example.other` | ❌ no (sideways) |
| `org.school` | ❌ no (somewhere else) |

**Golden rule:** 🥇 Always create new packages **inside** `com.example.hello`. In IntelliJ: **right-click on `com.example.hello`** → **New → Package** (or **New → Java Class**).

---

## 🗂️ Part 5: `src/main/resources` — the non-Java files

Open the **`resources`** folder. It has three things:

### 🎛️ `application.properties`

The **control panel** of your app. Right now it has only **one** line:

```properties
spring.application.name=hello
```

| Code | Meaning |
|---|---|
| `spring.application.name` | The **name** of the setting. |
| `=` | "is" |
| `hello` | The **value**. |

"The application's name is `hello`." Spring Boot shows this name in the console log (you'll see `[hello]` in every log line in Chapter 51). You'll add **many** settings here in Chapter 55 (like changing the port). 🎛️

### 🪟 `static/`

An **empty** folder for **static files**: HTML pages, CSS, JavaScript, pictures. Spring Boot sends them to the browser **as they are**.

- Put `index.html` here → people see it at `http://localhost:8080/` 🏠
- Put `cat.png` here → people see it at `http://localhost:8080/cat.png` 🐱

(You'll try this in Chapter 51!)

### 📄 `templates/`

An **empty** folder for **templates**: HTML pages with "holes" that the server fills with data, like "Hello, `___`!" → "Hello, Sara!". We use it in **Chapter 89** (Thymeleaf). For now, ignore it.

> 💡 **Why "resources" and not "java"?** Maven treats them differently: files in `java` are **compiled** into `.class` files. Files in `resources` are just **copied**. When the app runs, both end up in the same place (the **classpath**), so Spring can find them. 📋

---

## 🧪 Part 6: `src/test` — the safety-check room

Open **`src/test/java/com/example/hello/HelloApplicationTests.java`**:

```java
package com.example.hello;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class HelloApplicationTests {

	@Test
	void contextLoads() {
	}

}
```

An **empty** test? 🤔 Yes, and it's still useful! Let's see why.

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `package com.example.hello;` | The **same** package as the main class, but in the `test` folder. |
| `import org.junit.jupiter.api.Test;` | **JUnit** — the testing framework (Chapter 84). |
| `import org.springframework.boot.test.context.SpringBootTest;` | A Spring Boot testing tool. |
| `@SpringBootTest` | "For this test, **start the whole Spring app** (all beans, settings...)." |
| `class HelloApplicationTests {` | The test class. (No `public` needed for tests.) |
| `@Test` | "This method is a test. JUnit, please run it." (JUnit is a framework — it calls **your** method! 🎬 Chapter 48.) |
| `void contextLoads() {` | The test's name: "the context (the Spring container) loads". |
| `}` (empty body) | The test does **nothing** by itself... |

**So what does it check?** Because of `@SpringBootTest`, Spring **starts the whole app** before the test. If **anything** is broken — a missing bean, a wrong setting, two beans fighting — the start **fails**, and the test turns **red** ❌. If the app starts fine, the test is **green** ✅.

It's a **smoke test** 💨: "Turn it on. Does smoke come out? No? Good!" 😄

### ▶️ Run the test

In IntelliJ, click the green **▶** next to `class HelloApplicationTests` → **Run 'HelloApplicationTests'**.

You'll see the Spring banner, some log lines, and then at the bottom:

```
✅ Tests passed: 1 of 1 test
```

🎉 Your first green test!

With the Maven Wrapper in a terminal (Chapter 40), it's `mvnw test`. The end of the output looks like this:

```
[INFO] Running com.example.hello.HelloApplicationTests
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 4.449 s -- in com.example.hello.HelloApplicationTests
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

> 💡 **How to type the wrapper command:**
>
> | Terminal | Command |
> |---|---|
> | Windows Command Prompt | `mvnw test` |
> | Windows PowerShell | `.\mvnw test` |
> | Git Bash, Mac, Linux | `./mvnw test` |
>
> Run it **inside** the project folder (the one with `pom.xml`). In IntelliJ, open the **Terminal** tab at the bottom (**Alt + F12**) — it's already in the right folder! 👍

---

## 🔧 Part 7: The Maven Wrapper — `mvnw`, `mvnw.cmd`, `.mvn`

You met these in **Chapter 40**. Quick reminder:

| File | What it is |
|---|---|
| `mvnw` | A **script** for Mac and Linux (and Git Bash): "Run Maven. If Maven is missing, **download** the right version first." |
| `mvnw.cmd` | The **same** script for Windows (`cmd` = Command Prompt). |
| `.mvn/wrapper/maven-wrapper.properties` | Which Maven version to download. |

Here's the real `maven-wrapper.properties`:

```properties
wrapperVersion=3.3.4
distributionType=only-script
distributionUrl=https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.10.0/apache-maven-3.10.0-bin.zip
```

| Line | Meaning |
|---|---|
| `wrapperVersion=3.3.4` | The version of the **wrapper script** itself. |
| `distributionType=only-script` | "Use only the script, no extra jar file." |
| `distributionUrl=...apache-maven-3.10.0-bin.zip` | ⭐ "Download **Maven 3.10.0** from here." Everybody on your team gets the **same** Maven. 🤝 |

**Result:** You never need to install Maven yourself. 🎉 (Your numbers may be different. That's fine.)

> ⚠️ Don't delete these files. And don't edit them unless you know why.

---

## 🐙 Part 8: Git files — `.gitignore` and `.gitattributes`

Remember **Git** (Chapter 42)? Spring Initializr prepares your project for Git, too. 😊

### `.gitignore` — "Don't save these!"

Here are the first lines of the real file:

```
HELP.md
target/
.mvn/wrapper/maven-wrapper.jar
!**/src/main/**/target/
!**/src/test/**/target/

### STS ###
...

### IntelliJ IDEA ###
.idea
*.iws
*.iml
*.ipr
...
```

| Line | Meaning |
|---|---|
| `HELP.md` | Don't save the help file. |
| `target/` | ⭐ Don't save the **build output**. Maven can make it again any time. |
| `.mvn/wrapper/maven-wrapper.jar` | Don't save this downloaded file. |
| `!**/src/main/**/target/` | `!` means "**except**": if **your own code** has a folder called `target` somewhere inside `src`, **do** save it. |
| `### IntelliJ IDEA ###` | A comment (starts with `#`). |
| `.idea`, `*.iml`... | Don't save IntelliJ's personal settings. (Every developer has their own.) |

The file also has sections for other editors (STS, NetBeans, VS Code). They're ready for everybody! 🤝

### `.gitattributes` — line endings

```
/mvnw text eol=lf
*.cmd text eol=crlf
```

| Line | Meaning |
|---|---|
| `/mvnw text eol=lf` | The Mac/Linux script must use **Mac/Linux line endings** (LF). |
| `*.cmd text eol=crlf` | Windows scripts must use **Windows line endings** (CRLF). |

"Line endings" are invisible characters at the end of each line. Windows and Mac/Linux use **different** ones. 🙃 If they're wrong, the scripts **break**. This file makes Git keep them correct. You'll never need to touch it. 👍

---

## 📖 Part 9: `HELP.md` and `pom.xml`

### `HELP.md`

A small **Markdown** file (`.md` — the same format as this book! 😄) with **links** to official guides for your dependencies, like "Building a RESTful Web Service". Read it if you're curious, delete it if you want. It's not part of your app.

### `pom.xml`

The **instruction manual for Maven** — you read it line by line in **Chapter 49** (and Chapter 41). 📖 You'll edit it when you need **new dependencies**. After you change it, always click **Maven reload** 🔄.

---

## 📦 Part 10: `target/` — the storage room (appears later)

You don't see `target` yet? That's normal! It appears **after** the first build or run. Maven puts everything it **makes** there:

```
target/
├── classes/                       ← your compiled .class files + copied resources
│   ├── application.properties
│   └── com/example/hello/HelloApplication.class
├── test-classes/                  ← compiled tests
├── generated-sources/             ← code made by tools (usually empty)
├── maven-status/                  ← Maven's own notes
└── hello-0.0.1-SNAPSHOT.jar       ← the finished app (only after "package" — Chapter 98)
```

**Rules for `target`:** 📏

- ❌ **Never** put your own files in it.
- ❌ **Never** edit files in it (your changes will be **deleted** on the next build).
- ✅ You **can** delete the whole folder any time. Maven makes it again. (`mvnw clean` deletes it for you.)
- ✅ It's in `.gitignore`, so Git doesn't save it.

---

## 💡 Part 11: IntelliJ's extra parts

These are **not** on your disk as normal project files — IntelliJ shows them to help you:

| Part | What it is |
|---|---|
| **`.idea/`** | IntelliJ's settings for this project (on disk, but ignored by Git). Don't edit it. |
| **External Libraries** | All the libraries Maven downloaded (Chapter 49). You can open them and read their code! |
| **Scratches and Consoles** | A place for quick notes and test code. Not part of your project. |
| **Maven window** (the **m** icon on the right) | Buttons for Maven: **Reload** 🔄, **Lifecycle** (clean, compile, test, package...) — Chapter 40. |

---

## 🎯 Part 12: Which files will you edit?

Here's the most useful table in this chapter. 😊

| File / folder | How often you'll edit it |
|---|---|
| `src/main/java/com/example/hello/...` (your classes) | 🔥🔥🔥 **All the time!** Controllers, services, records... |
| `src/main/resources/application.properties` | 🔥🔥 Often (settings) |
| `src/test/java/...` | 🔥🔥 Often (tests — Part 11) |
| `pom.xml` | 🔥 Sometimes (new dependencies) |
| `src/main/resources/static/` | 🔥 Sometimes (simple web pages, pictures) |
| `src/main/resources/templates/` | Only with Thymeleaf (Chapter 89) |
| `HelloApplication.java` | Rarely (it's almost always just these 13 lines) |
| `.gitignore` | Rarely |
| `mvnw`, `mvnw.cmd`, `.mvn/`, `.gitattributes` | ❌ Never |
| `target/`, `.idea/` | ❌ Never |

---

## 💻 Mini project: The project treasure hunt 🗺️💎

Use IntelliJ to find the answers. Write them down on paper (or in a text file). Then check below!

1. 📍 What is the **full path** (on your disk) of `HelloApplication.java`? (Tip: right-click the file → **Copy Path/Reference... → Absolute Path**.)
2. 🔢 Which **Spring Boot version** does your project use? (Tip: `pom.xml`.)
3. 🐱 Which **Tomcat version** did Maven download? (Tip: **External Libraries**, look for `tomcat-embed-core`.)
4. 🔧 Which **Maven version** will the wrapper download? (Tip: `.mvn/wrapper/...`.)
5. 🙈 Will Git save the `target` folder? (Tip: `.gitignore`.)
6. 🧪 Run the test `HelloApplicationTests`. Is it green? ✅
7. 📦 After running the test, did a **new folder** appear in your project? Which one? What's inside `target/classes`?
8. 🔍 Hold **Ctrl** and click on `SpringApplication` in `HelloApplication.java`. What opens?

<details>
<summary>Click to see the answers</summary>

1. Something like `C:\Users\YourName\IdeaProjects\hello\src\main\java\com\example\hello\HelloApplication.java`. Notice: `com.example.hello` is really **three folders** on disk!
2. The `<version>` inside `<parent>`, for example `4.1.1`.
3. Something like `Maven: org.apache.tomcat.embed:tomcat-embed-core:11.0.24` (your number may be different).
4. The version in `distributionUrl`, for example `3.10.0`.
5. No. `target/` is in `.gitignore`.
6. Yes: "Tests passed: 1 of 1 test" ✅
7. Yes: `target`. Inside `target/classes` you find `application.properties` (copied) and `com/example/hello/HelloApplication.class` (compiled). (The empty `static` and `templates` folders are **not** copied — Maven skips empty folders. They appear as soon as you put a file in them.)
8. The **source code** of Spring Boot's `SpringApplication` class (IntelliJ downloads or decompiles it). It's a **long** file — Spring Boot is real Java code written by people, not magic! 🧙‍♂️❌

</details>

---

## ✋ Try it yourself

**Task 1:** In IntelliJ, create a new package **`com.example.hello.student`** (right-click `com.example.hello` → New → Package → type `student`). Will Spring find classes in it? Why?

<details>
<summary>Click to see the answer</summary>

Yes! ✅ `com.example.hello.student` is **below** the base package `com.example.hello`, and `@ComponentScan` searches the base package **and everything below it**.

</details>

**Task 2:** A friend made a project with group `org.zoo` and artifact `animals`. They put a controller in the package `org.zoo.controllers`. It doesn't work (404). Why? Where should it be?

<details>
<summary>Click to see the answer</summary>

The base package is `org.zoo.animals` (where `AnimalsApplication` lives). `org.zoo.controllers` is **sideways**, not below it, so Spring never scans it. Move the controller to `org.zoo.animals` or below, for example `org.zoo.animals.controllers`. ✅

</details>

**Task 3:** Delete the `target` folder (right-click → Delete). Then run the test again. What happens?

<details>
<summary>Click to see the answer</summary>

The test runs fine, and `target` **comes back**. Maven builds everything again. That's why it's safe to delete `target` — and why you should never keep your own files there. 📦

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Putting classes outside the base package

The most common Spring Boot beginner mistake! 🏆😅 Your endpoint gives **404**, and there's **no error message**. **Fix:** Move the class into `com.example.hello` or a package below it. (In IntelliJ: drag and drop the class into the right package. IntelliJ fixes the `package` line for you.)

### Mistake 2: Putting Java files in `resources` (or resources in `java`)

- A `.java` file in `resources` is **not compiled**. Spring never sees the class.
- `application.properties` in `java` is **not found**, so your settings are ignored.

**Fix:** Java code → `src/main/java`. Everything else → `src/main/resources`.

### Mistake 3: Editing files in `target`

You change `target/classes/application.properties`... and on the next build, your change is **gone**. 😢 **Fix:** Always edit files in `src`.

### Mistake 4: Deleting the main class or `@SpringBootApplication`

Without `@SpringBootApplication`, there is no auto-configuration and no component scan. Nothing works. 🙈 **Fix:** Keep the main class exactly as Spring Initializr made it.

### Mistake 5: Creating a second `main` class

Some beginners write a new class with `public static void main` to "test something" inside the Spring project, and run **that** one instead. Spring never starts! **Fix:** Run `HelloApplication`. (To try plain-Java things, use a separate project, or a **scratch file**: **File → New → Scratch File → Java**.)

### Mistake 6: `mvnw` not found

```
mvnw : The term 'mvnw' is not recognized...
```

You're in **PowerShell** — it needs `.\mvnw`. Or you're in the **wrong folder**. **Fix:** Go to the folder with `pom.xml`, and use `.\mvnw` (PowerShell) or `./mvnw` (Git Bash, Mac, Linux).

---

## ✅ Summary

- A Spring Boot project uses the **standard Maven layout**: `src/main/java`, `src/main/resources`, `src/test/java`, `pom.xml`.
- **`HelloApplication`** is the front door 🚪: `main` calls **`SpringApplication.run(...)`**, which starts everything.
- **`@SpringBootApplication`** = `@SpringBootConfiguration` + `@EnableAutoConfiguration` + **`@ComponentScan`** 🍔🍟🥤.
- ⚠️ **Base package rule:** Spring only finds classes in the main class's package **and below**. Outside → silently ignored → 404.
- `resources/`: **`application.properties`** (settings 🎛️), **`static/`** (files sent as they are 🪟), **`templates/`** (Chapter 89).
- **`HelloApplicationTests`** starts the whole app — a **smoke test** 💨. Green = the app can start.
- **`mvnw`/`mvnw.cmd`/`.mvn`** = the Maven Wrapper. **`.gitignore`/`.gitattributes`** = Git helpers.
- **`target/`** = build output 📦. Never edit it; safe to delete.
- You'll edit **your classes** all the time, `application.properties` often, `pom.xml` sometimes.

---

## ❓ Quiz

1. What is the base package of the `hello` project?
2. What three annotations are inside `@SpringBootApplication`?
3. Which of the three is responsible for **finding** your controllers?
4. Is `com.example.hello.shop.cart` scanned? Is `com.example.shop`?
5. Where do you put a picture `logo.png` so the browser can see it?
6. What does the empty test `contextLoads()` really check?
7. Why should you never edit files in `target`?
8. Which file tells Git not to save `target`?
9. How do you run the tests with the Maven Wrapper in Windows PowerShell?

<details>
<summary>Click to see the answers</summary>

1. `com.example.hello`
2. `@SpringBootConfiguration`, `@EnableAutoConfiguration`, `@ComponentScan`.
3. `@ComponentScan`.
4. `com.example.hello.shop.cart` — yes (below the base package). `com.example.shop` — no (sideways).
5. In `src/main/resources/static/`. Then it's at `http://localhost:8080/logo.png`.
6. That the whole Spring app can **start** without errors (all beans and settings are OK).
7. Maven makes `target` again on every build, so your changes would be deleted. Always edit in `src`.
8. `.gitignore`
9. `.\mvnw test` (inside the project folder).

</details>

---

[⬅ Previous chapter](49-spring-initializr.md) | [Table of Contents](../README.md) | [Next chapter: Run your first Spring Boot app ➡](51-run-first-app.md)
