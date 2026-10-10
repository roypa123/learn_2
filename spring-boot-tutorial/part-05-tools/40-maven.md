# Chapter 40 – Maven: The Helper That Downloads Libraries

[⬅ Previous chapter](../part-04-more-java/39-dates-and-times.md) | [Table of Contents](../README.md) | [Next chapter ➡](41-pom-xml.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **library** and a **dependency** are
- What a **build tool** is, and why every real project needs one
- What **Maven** does for you
- The **standard Maven folder structure** (the same in every project in the world!)
- How to create a **Maven project in IntelliJ**
- How to **add a library** (dependency) and use it
- The **Maven lifecycle**: `clean`, `compile`, `test`, `package`
- The **Maven Wrapper** (`mvnw`) that comes with every Spring Boot project 🌱

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Library** | Code that **someone else** wrote, packed so you can use it. Like a box of LEGO pieces 🧱. |
| **Dependency** | A library your project **depends on** (needs). |
| **JAR file** | *Java ARchive.* A zip file full of `.class` files. Libraries come as JARs. |
| **Build** | Turning your source code into something that can run: compile, test, package. |
| **Build tool** | A program that does the build for you, automatically. Maven is one. |
| **Maven** | The most popular build tool for Java. |
| **Maven Central** | A huge online **warehouse** 🏬 with almost every Java library in the world. |
| **Coordinates** | The "address" of a library: `groupId`, `artifactId`, `version`. |
| **`pom.xml`** | The file where you describe your project to Maven (next chapter). |
| **Lifecycle / phase** | The steps of a build, in order: compile → test → package... |
| **Plugin** | An add-on that teaches Maven how to do a job. |

---

## 📖 Story: The kitchen helper 👨‍🍳

You want to cook a big dinner. 🍝 You need:

- 🍅 Tomatoes from the market
- 🧀 Cheese from the dairy shop
- 🍝 Pasta from the supermarket
- Then: wash, cut, cook, taste, put on plates...

**Without a helper**, you drive to 3 shops yourself, check every product, carry everything home, and do every step by hand. If you forget the cheese... drive again! 😩

**With a helper**, you write a **shopping list** and a **recipe card**:

```
 📝 SHOPPING LIST              📝 RECIPE
   - tomatoes (Italian, 1 kg)    1. wash
   - mozzarella                  2. cut
   - pasta (spaghetti)           3. cook
                                 4. taste
                                 5. serve
```

The helper **goes shopping** for you, **brings exactly** what's on the list, and **follows the steps** in order. Every time. Without forgetting. 🎉

**Maven is your kitchen helper:**
- The **shopping list** = your **dependencies** (libraries you need).
- The **shops** = **Maven Central** (the online warehouse).
- The **recipe** = the **build lifecycle** (compile, test, package).
- The **list + recipe card** = the file **`pom.xml`**.

---

## 🤔 Part 1: Why do we need Maven?

### Problem 1: Libraries

Java has a lot built in. But for many jobs, other people have already written great libraries:

| Job | Library |
|---|---|
| Web applications | **Spring Boot** 🌱 |
| Talking to databases | Hibernate, JDBC drivers |
| Reading/writing JSON | Jackson, Gson |
| Testing | JUnit, Mockito |
| Logging | Logback, SLF4J |

**Without Maven**, to use a library you must:
1. Find its website.
2. Download the right `.jar` file (the right **version**!).
3. Find out which **other** libraries **it** needs (and download those too... and **their** libraries... 😵).
4. Add them all to your project by hand.
5. Do it again on every computer, for every team member.

Spring Boot alone needs **dozens** of JAR files. By hand? Impossible! 😱

**With Maven:** you write **one line** in a file. Maven downloads **everything** — including the libraries' own dependencies (called **transitive dependencies**). ✨

### Problem 2: Building

A real project needs: compile all files → run all tests → package into a JAR → ... With Maven, it's **one command**: `mvn package`. Same steps, same result, on **every** computer. 🖥️💻🖥️

### Problem 3: Every project looks different

Without rules, every project has its own folder structure. With Maven, **every** Java project in the world has the **same** structure. Open any Maven project → you know exactly where everything is! 🗺️

> 💡 **Gradle** is another popular build tool (it does the same job, with a different file style). Spring Boot supports both. This book uses **Maven** because its file is very clear and easy to read for beginners.

---

## 🏬 Part 2: Maven Central — the library warehouse

**Maven Central** (`https://central.sonatype.com`) is a free online warehouse with **millions** of library versions.

Every library has an **address** made of 3 parts, called **coordinates**:

| Part | Meaning | Example (Gson — a JSON library by Google) |
|---|---|---|
| **groupId** | the **organization** (usually reverse domain — Chapter 26!) | `com.google.code.gson` |
| **artifactId** | the **name** of the library | `gson` |
| **version** | which **version** | `2.11.0` |

Short form: `com.google.code.gson:gson:2.11.0`

📦 **Like a postal address:** country (groupId) → street (artifactId) → house number (version).

### Where does Maven put the downloads?

In a folder on your computer called the **local repository**:

```
 C:\Users\YourName\.m2\repository\
```

Maven downloads a library **once** and keeps it there. The next project that needs it uses the **saved copy** — no download needed. 🚀

```
  Your project                 Your computer                  Internet
 ┌────────────┐   needs    ┌──────────────────┐   if missing  ┌──────────────┐
 │  pom.xml   │ ─────────► │ ~/.m2/repository │ ────────────► │ Maven Central│
 │ "I need    │            │ (local copy)     │ ◄──────────── │  🏬          │
 │  gson"     │ ◄───────── │                  │   download    │              │
 └────────────┘   uses     └──────────────────┘               └──────────────┘
```

---

## 🗂️ Part 3: The standard Maven folder structure

**Every** Maven project looks like this:

```
 my-project/
 ├── pom.xml                         ← 📝 the project description (shopping list + recipe)
 ├── src/
 │   ├── main/
 │   │   ├── java/                   ← ☕ YOUR Java code goes here
 │   │   │   └── com/example/app/
 │   │   │        └── App.java
 │   │   └── resources/              ← 📄 other files: settings, images, templates
 │   │        └── application.properties
 │   └── test/
 │       ├── java/                   ← 🧪 your TEST code goes here
 │       │   └── com/example/app/
 │       │        └── AppTest.java
 │       └── resources/              ← 📄 files used only by tests
 └── target/                         ← 🏭 Maven's OUTPUT (compiled classes, JAR). Created automatically.
```

| Folder | What goes there |
|---|---|
| `pom.xml` | The Maven file. **One** per project, at the top. |
| `src/main/java` | Your Java source code (with packages). |
| `src/main/resources` | Non-Java files your program needs: `application.properties` (Spring Boot settings — Chapter 55), HTML templates, images... |
| `src/test/java` | Test code (Chapter 84). Not included in the final program. |
| `src/test/resources` | Files only for tests. |
| `target/` | Everything Maven **produces**. ⚠️ **Never edit** — and you can **delete** it any time; Maven creates it again. |

> 💡 Compare with our IntelliJ projects in Parts 1–4: we had just `src/`. Now the code goes into `src/main/java`. That's the only big difference!

🌱 **A Spring Boot project has exactly this structure.** You'll recognize everything in Chapter 50!

---

## 🛠️ Part 4: Create a Maven project in IntelliJ

Good news: **IntelliJ already includes Maven**. You don't need to install anything! 🎉

1. **File → New → Project...**
2. Fill in:

```
 ┌────────────────────────────────────────────────────┐
 │ New Project                                        │
 │                                                    │
 │ Name:          hello-maven                         │
 │ Location:      C:\Users\YourName\IdeaProjects      │
 │ Language:      [Java]                              │
 │ Build system:  IntelliJ  [Maven]  Gradle   ◄── Maven!
 │ JDK:           25  Eclipse Temurin                 │
 │                                                    │
 │ [✓] Add sample code                                │
 │                                                    │
 │ ▼ Advanced Settings                                │
 │    GroupId:     com.example                        │
 │    ArtifactId:  hello-maven                        │
 │                                                    │
 │                               [ Create ]           │
 └────────────────────────────────────────────────────┘
```

| Setting | What to choose | Meaning |
|---|---|---|
| **Build system** | **Maven** ⚠️ | This is the important change! |
| **GroupId** | `com.example` | Your organization (reverse domain). |
| **ArtifactId** | `hello-maven` | The name of your project. |

3. Click **Create**.

IntelliJ creates the standard folders and a `pom.xml`. Look in the Project window:

```
 hello-maven
 ├── .idea
 ├── src
 │   ├── main
 │   │   ├── java
 │   │   │   └── com.example
 │   │   │        └── Main
 │   │   └── resources
 │   └── test
 │       └── java
 ├── .gitignore
 └── pom.xml          ← 📝
```

4. Open `Main.java` and click ▶ **Run**. It works like before! ✅

### 🪟 The Maven tool window

On the **right side** of IntelliJ, there's a **Maven** tab (an `m` icon). Click it:

```
 Maven
 └── hello-maven
      ├── Lifecycle
      │    ├── clean
      │    ├── validate
      │    ├── compile
      │    ├── test
      │    ├── package
      │    ├── verify
      │    ├── install
      │    └── ...
      ├── Plugins
      └── Dependencies
```

You can **double-click** any phase (like `package`) to run it. 🖱️ We'll explain these phases in Part 6.

---

## ➕ Part 5: Adding a library (dependency)

Let's use the **Gson** library to turn a Java object into **JSON** text (we'll learn JSON properly in Chapter 45).

### Step 1: Open `pom.xml`

You'll see something like:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project ...>
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>hello-maven</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>25</maven.compiler.source>
        <maven.compiler.target>25</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

</project>
```

(We explain **every** line in the next chapter. 😊)

### Step 2: Add a `<dependencies>` section

Put this **before** `</project>`:

```xml
    <dependencies>
        <dependency>
            <groupId>com.google.code.gson</groupId>
            <artifactId>gson</artifactId>
            <version>2.11.0</version>
        </dependency>
    </dependencies>
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `<dependencies>` | "Here is my **shopping list**." |
| `<dependency>` | "One item on the list:" |
| `<groupId>com.google.code.gson</groupId>` | the organization |
| `<artifactId>gson</artifactId>` | the library name |
| `<version>2.11.0</version>` | the version |
| `</dependency>` / `</dependencies>` | end of the item / end of the list |

### Step 3: Load the changes 🔄

After you change `pom.xml`, IntelliJ shows a small **Maven icon** 🔄 floating at the top right of the editor ("Load Maven Changes"). **Click it.** (Or press **Ctrl + Shift + O**.)

Maven downloads Gson from Maven Central. You can see it in the **Maven** tool window under **Dependencies**, and in the Project window under **External Libraries**. ✅

### Step 4: Use it!

```java
package com.example;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class Main {

    record Student(String name, int age, boolean active) { }

    public static void main(String[] args) {
        Student sara = new Student("Sara", 12, true);

        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        String json = gson.toJson(sara);

        System.out.println(json);
    }
}
```

**Output:**

```
{
  "name": "Sara",
  "age": 12,
  "active": true
}
```

🎉 You just used **someone else's code** that you didn't download by hand! The line `import com.google.gson.Gson;` works because Maven put the Gson JAR in your project.

> 💡 **How do I find the coordinates of a library?** Search on `https://central.sonatype.com` (or `https://mvnrepository.com`). Every library page shows a ready-to-copy `<dependency>` block. 📋 Always choose a **stable** version (not "alpha", "beta" or "RC").

> 🌱 **Spring Boot note:** In Spring Boot, you'll rarely write versions yourself! Spring Boot manages the versions of hundreds of libraries for you, so they all work together. You'll see this in Chapter 41. ✨

---

## 🔄 Part 6: The Maven lifecycle

A **lifecycle** is a list of **phases** (steps) in a fixed **order**. Like the recipe card:

```
 validate → compile → test → package → verify → install → deploy
    📋         ⚙️       🧪       📦        ✅         💾        🚀
```

| Phase | What it does |
|---|---|
| `validate` | Check that the project is correct (pom.xml OK). |
| `compile` | Compile `src/main/java` → `target/classes`. |
| `test` | Compile and run the tests in `src/test/java`. ❌ If a test fails → **stop**! |
| `package` | Put everything into a **JAR** file in `target/`. |
| `verify` | Run extra checks (integration tests). |
| `install` | Copy the JAR into your **local** repository (`~/.m2`), so your **other** projects can use it. |
| `deploy` | Upload the JAR to a **shared** repository (for your team / company). |

### ⚡ The magic rule: running one phase runs ALL the phases before it

```
 mvn package
   → validate ✅ → compile ✅ → test ✅ → package ✅
```

You can't get a package without compiling and testing first. 🛡️ If **any** test fails, there's **no** JAR. This protects you from shipping broken code!

### `clean` — start fresh 🧹

`clean` is a separate lifecycle. It **deletes** the `target/` folder.

```
 mvn clean package
   → delete target/ → validate → compile → test → package
```

👉 `mvn clean package` is the command you'll use **most**. If something strange happens in your build, try `clean` first!

### Running phases in IntelliJ

In the **Maven** tool window → **Lifecycle** → double-click `clean`, then double-click `package`. The output appears at the bottom:

```
[INFO] --- maven-compiler-plugin:3.13.0:compile ---
[INFO] Compiling 1 source file to C:\...\hello-maven\target\classes
[INFO] --- maven-surefire-plugin:3.2.5:test ---
[INFO] No tests to run.
[INFO] --- maven-jar-plugin:3.4.1:jar ---
[INFO] Building jar: C:\...\hello-maven\target\hello-maven-1.0-SNAPSHOT.jar
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
```

(Plugin version numbers may differ on your computer. That's fine.)

| Output | Meaning |
|---|---|
| `[INFO] --- maven-compiler-plugin ... ---` | A **plugin** is doing a phase. Each phase is done by a plugin. 🧩 |
| `Compiling 1 source file` | `compile` phase |
| `No tests to run.` | `test` phase (we have no tests yet) |
| `Building jar: ...hello-maven-1.0-SNAPSHOT.jar` | `package` phase — your JAR is ready! 📦 |
| **`BUILD SUCCESS`** | ✅ Everything worked. (If something failed: **`BUILD FAILURE`** and an error message.) |

> 💡 The JAR name comes from the pom: **artifactId** + `-` + **version** + `.jar`.

---

## 💻 Part 7: Maven in the terminal — and the Maven Wrapper

Professionals also run Maven in the **terminal**. The commands look like this:

```
mvn clean package
mvn test
mvn compile
```

| Part | Meaning |
|---|---|
| `mvn` | Start Maven. |
| `clean package` | The phases to run (in order). |

But `mvn` only works if Maven is **installed** on your computer (with PATH, like Java in Chapter 3). 😕

### ✨ The Maven Wrapper: `mvnw`

To avoid "install Maven first", projects include a **Maven Wrapper**: a small script that **downloads the right Maven version automatically** the first time you use it.

```
 my-project/
 ├── mvnw          ← script for Mac/Linux
 ├── mvnw.cmd      ← script for Windows
 ├── .mvn/
 │   └── wrapper/
 │        └── maven-wrapper.properties   ← which Maven version to use
 └── pom.xml
```

You use it **exactly like** `mvn`:

| Windows (cmd / PowerShell) | Mac / Linux |
|---|---|
| `mvnw clean package` (or `.\mvnw clean package`) | `./mvnw clean package` |

🌱 **Every Spring Boot project** from Spring Initializr **comes with the Maven Wrapper**! So you'll never need to install Maven yourself. 🎉

> 💡 **Want the wrapper in your own project now?** If you have Maven in IntelliJ, open the Maven window → **Execute Maven Goal** (the `m` icon) → type `wrapper:wrapper` → Enter. The `mvnw` files appear!

### Run your JAR

```
java -cp target/hello-maven-1.0-SNAPSHOT.jar com.example.Main
```

Hmm — this fails with `NoClassDefFoundError: com/google/gson/Gson` 😮. Why? Our JAR contains **only our code**, not Gson!

👉 For a simple project, it's easier to run from IntelliJ. And **Spring Boot solves this perfectly**: it makes a **"fat JAR"** with **everything** inside. You can then run it with just `java -jar app.jar`. (Chapter 98.) 🍔

---

## 🔍 Part 8: Seeing the dependency tree

Remember "transitive dependencies"? When you add Spring Boot, it brings **many** other libraries. You can see them all:

- **IntelliJ:** Maven window → **Dependencies** → expand the arrows ▶.
- **Terminal:** `mvnw dependency:tree`

Example (shortened) for a Spring Boot web project:

```
com.example:school:jar:0.0.1-SNAPSHOT
+- org.springframework.boot:spring-boot-starter-web:jar:...
|  +- org.springframework.boot:spring-boot-starter:jar:...
|  |  +- org.springframework.boot:spring-boot:jar:...
|  |  \- ch.qos.logback:logback-classic:jar:...
|  +- org.springframework.boot:spring-boot-starter-json:jar:...
|  |  \- com.fasterxml.jackson.core:jackson-databind:jar:...
|  +- org.springframework.boot:spring-boot-starter-tomcat:jar:...
|  \- org.springframework:spring-webmvc:jar:...
```

You added **one** dependency (`spring-boot-starter-web`) — Maven brought **dozens**: logging, JSON, a web server (Tomcat)... 🎁🎁🎁

---

## ✋ Try it yourself

**Task 1:** Create the `hello-maven` project in IntelliJ. Find these folders: `src/main/java`, `src/main/resources`, `src/test/java`. Where is `pom.xml`?

**Task 2:** Add the Gson dependency and run the JSON example. Then change the record to add a field `String city`. Run again — does the JSON change?

**Task 3:** Run `clean`, then `package` from the Maven tool window. Find the JAR file in `target/`. What is its full name? Now delete the whole `target` folder and run `package` again. What happens?

<details>
<summary>Click to see the answer</summary>

The JAR is `target/hello-maven-1.0-SNAPSHOT.jar`. After deleting `target/`, running `package` creates it again — `target/` is just output. 🏭

</details>

**Task 4:** Go to `https://central.sonatype.com` and search for `commons-lang3`. Find its groupId, artifactId and the newest stable version. Add it to your pom, load the changes, and try:

```java
import org.apache.commons.lang3.StringUtils;

System.out.println(StringUtils.capitalize("hello"));      // Hello
System.out.println(StringUtils.reverse("maven"));          // nevam
System.out.println(StringUtils.isBlank("   "));            // true
```

**Task 5:** In your own words: what is the difference between `mvn compile` and `mvn package`? What happens if a test fails during `mvn package`?

<details>
<summary>Click to see the answer</summary>

`compile` only compiles the main code. `package` runs validate, compile, **test**, and then makes a JAR. If a test fails, the build **stops** (`BUILD FAILURE`) and no JAR is made.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting to load Maven changes

You added a dependency, but `import com.google.gson.Gson;` is still **red**. 😕
**Fix:** Click the 🔄 **Load Maven Changes** button (or Ctrl + Shift + O, or Maven window → 🔄 Reload All).

### Mistake 2: Code in the wrong folder

Putting `.java` files directly in `src/` or in `src/main/resources/` → Maven doesn't compile them.
**Fix:** Java code goes in **`src/main/java`** (inside your package folders).

### Mistake 3: Typo in coordinates

```
[ERROR] Failed to execute goal ... Could not resolve dependencies ...
  com.google.code.gson:gsonn:jar:2.11.0 was not found in https://repo.maven.apache.org/maven2
```

**Fix:** Check the spelling of groupId, artifactId and version. Copy them from Maven Central.

### Mistake 4: No internet / company firewall

Maven needs internet the **first** time it downloads a library. If it can't connect, the build fails.
**Fix:** Check your connection. At some companies, Maven needs special proxy settings (ask your team).

### Mistake 5: Editing files in `target/`

Your changes disappear after the next build. 😱 **Fix:** Only edit files in `src/`.

### Mistake 6: Wrong Java version

```
[ERROR] error: release version 25 not supported
```

The pom asks for a Java version that your JDK doesn't have.
**Fix:** Change the version in the pom (next chapter) to match your JDK, or set the right JDK in **File → Project Structure**.

---

## ✅ Summary

- A **library** is code from others; a **dependency** is a library your project needs.
- **Maven** is a **build tool**: it **downloads** dependencies (and their dependencies) from **Maven Central**, and **builds** your project with one command. 👨‍🍳
- Libraries have **coordinates**: `groupId:artifactId:version`.
- Downloads are saved in `~/.m2/repository`.
- **Standard folders:** `src/main/java` (code), `src/main/resources` (files), `src/test/java` (tests), `target/` (output — never edit).
- Add a dependency in `pom.xml` → **Load Maven Changes** 🔄 → `import` and use it.
- **Lifecycle:** `validate → compile → test → package → verify → install → deploy`. Running a phase runs **all before it**.
- `mvn clean package` → fresh build → JAR in `target/`. Look for **BUILD SUCCESS**.
- The **Maven Wrapper** (`mvnw`) downloads Maven for you. Every Spring Boot project has it. 🌱

---

## ❓ Quiz

1. What is a dependency?
2. Name the 3 parts of a library's coordinates.
3. Where does your Java code go in a Maven project?
4. What is in the `target/` folder? Can you delete it?
5. What happens when you run `mvn package`? (Which phases run?)
6. What does `clean` do?
7. What is the Maven Wrapper, and why is it useful?
8. You added a dependency, but the import is red. What should you do?

<details>
<summary>Click to see the answers</summary>

1. A library that your project needs.
2. groupId, artifactId, version.
3. `src/main/java`
4. Maven's output (compiled classes, the JAR). Yes — Maven creates it again.
5. validate, compile, test, package (all phases up to package).
6. It deletes the `target/` folder.
7. A script (`mvnw`) that downloads and runs the right Maven version — no need to install Maven yourself.
8. Load the Maven changes (click the 🔄 button or Ctrl + Shift + O).

</details>

---

[⬅ Previous chapter](../part-04-more-java/39-dates-and-times.md) | [Table of Contents](../README.md) | [Next chapter: The pom.xml file ➡](41-pom-xml.md)
