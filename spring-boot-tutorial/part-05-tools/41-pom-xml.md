# Chapter 41 – The `pom.xml` File, Line by Line

[⬅ Previous chapter](40-maven.md) | [Table of Contents](../README.md) | [Next chapter ➡](42-git.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- How to read **XML** (the language of `pom.xml`)
- **Every line** of a simple `pom.xml`
- What **properties**, **dependencies**, **scopes** and **plugins** are
- **Every line** of a real **Spring Boot** `pom.xml` 🌱
- What a **parent POM** and **starters** are
- Why you don't need to write **versions** in Spring Boot
- How to fix the most common pom problems

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **POM** | *Project Object Model.* Maven's description of your project. |
| **XML** | A text format with **tags** like `<name>Sara</name>`. Used for settings files. |
| **Tag** | A label in angle brackets: `<version>`. |
| **Element** | An opening tag, its content, and a closing tag: `<version>1.0</version>`. |
| **Property** | A **named value** you can reuse: `${java.version}`. |
| **Scope** | **When** a dependency is used: always, only for tests, only at run time... |
| **Plugin** | An add-on that does a job in the build (compile, test, make a JAR...). |
| **Parent POM** | Another pom that your pom **inherits** settings from (like inheritance — Chapter 22!). |
| **Starter** | A Spring Boot dependency that brings a **whole set** of libraries for one job. |
| **SNAPSHOT** | A version that is "still in progress", not finished. |

---

## 📖 Story: The ID card of your project 🪪

Every person has an **ID card**: name, birth date, address, photo...

Your project also has an **ID card**: the `pom.xml`. It says:

- **Who am I?** → name, group, version
- **Which Java do I use?** → properties
- **What do I need?** → dependencies (the shopping list 🛒)
- **How do I get built?** → plugins (the recipe 📝)
- **Who is my parent?** → parent pom (inheritance 👨‍👧)

When Maven (or IntelliJ, or a teammate) opens your project, it reads this ID card **first**.

---

## 🏷️ Part 1: XML in 5 minutes

`pom.xml` is written in **XML**. XML is easy — it's just **tags** in **boxes inside boxes**. 📦

### Elements

```xml
<name>Sara</name>
```

| Part | Meaning |
|---|---|
| `<name>` | **opening** tag |
| `Sara` | the **content** (the value) |
| `</name>` | **closing** tag — notice the `/` |

### Nesting (boxes inside boxes)

```xml
<person>
    <name>Sara</name>
    <age>12</age>
    <address>
        <city>Cairo</city>
        <country>Egypt</country>
    </address>
</person>
```

```
 📦 person
   ├── 📄 name: Sara
   ├── 📄 age: 12
   └── 📦 address
         ├── 📄 city: Cairo
         └── 📄 country: Egypt
```

Like Java's `{ }` blocks — every opening tag needs a matching closing tag, in the right order.

### Other things you'll see

| XML | Meaning |
|---|---|
| `<?xml version="1.0" encoding="UTF-8"?>` | The **first line**: "this is an XML file, in UTF-8". |
| `<project xmlns="...">` | `xmlns="..."` is an **attribute** (extra info inside a tag). Here: the "dictionary" for the tag names. You never change it. |
| `<!-- this is a comment -->` | A **comment** (like `//` in Java). |
| `<relativePath/>` | An **empty** element (opening + closing in one: `<x></x>` = `<x/>`). |

### ⚠️ XML rules

- Tags are **case-sensitive**: `<Version>` ≠ `<version>`.
- Every `<tag>` needs a `</tag>`.
- Tags must close **in the right order**: `<a><b></b></a>` ✅ — `<a><b></a></b>` ❌

That's all the XML you need! 😊

---

## 📄 Part 2: A simple pom, line by line

Here's the pom from Chapter 40, with the Gson dependency:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>hello-maven</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>Hello Maven</name>
    <description>My first Maven project</description>

    <properties>
        <maven.compiler.release>25</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <gson.version>2.11.0</gson.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>com.google.code.gson</groupId>
            <artifactId>gson</artifactId>
            <version>${gson.version}</version>
        </dependency>

        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.11.3</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

</project>
```

### 🔍 Section 1: The header

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" ...>
    <modelVersion>4.0.0</modelVersion>
```

| Line | Meaning |
|---|---|
| `<?xml ... ?>` | "This is an XML file." |
| `<project ...>` | The **main box**. Everything else is inside it. The long `xmlns` / `xsi` texts tell IntelliJ which tags are allowed (for auto-complete ✨). **Never change them** — just copy them. |
| `<modelVersion>4.0.0</modelVersion>` | The version of the **pom format**. Always `4.0.0`. Don't touch. |

### 🔍 Section 2: Who am I? (coordinates)

```xml
    <groupId>com.example</groupId>
    <artifactId>hello-maven</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>
```

Your **own** project has coordinates too (Chapter 40)! If someone wanted to use **your** library, they'd write these 3 values.

| Line | Meaning |
|---|---|
| `groupId` | Your organization (reverse domain). |
| `artifactId` | Your project's name. Used for the JAR name. |
| `version` | Your project's version. |
| `packaging` | What to build: `jar` (the default — you can leave this line out) or `war` (old-style web apps) or `pom`. |

### 📌 Versions: what does `SNAPSHOT` mean?

| Version | Meaning |
|---|---|
| `1.0-SNAPSHOT` | "Version 1.0, **still being worked on**." 🚧 It can change at any time. |
| `1.0` | "Version 1.0, **finished** and released." 🎉 It never changes. |
| `1.0.1` | A small **bug fix**. |
| `1.1.0` | **New features**, nothing broken. |
| `2.0.0` | **Big changes** — old code may need updates. |

This **MAJOR.MINOR.PATCH** style is called **Semantic Versioning**.

### 🔍 Section 3: Description (optional)

```xml
    <name>Hello Maven</name>
    <description>My first Maven project</description>
```

Human-friendly name and description. Optional, but nice. 😊

### 🔍 Section 4: Properties

```xml
    <properties>
        <maven.compiler.release>25</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <gson.version>2.11.0</gson.version>
    </properties>
```

**Properties** are **named values** — like **variables** in the pom.

| Property | Meaning |
|---|---|
| `maven.compiler.release` | "Compile my code for **Java 25**." ⚠️ Must match (or be lower than) your installed JDK. If you have Java 21, write `21`. |
| `project.build.sourceEncoding` | "My source files are in **UTF-8**." (So letters like é, ü, 你 and emojis 🎉 work.) |
| `gson.version` | **Our own** property! We invent it to keep the Gson version in one place. |

Use a property with **`${...}`**:

```xml
<version>${gson.version}</version>
```

→ Maven replaces it with `2.11.0`. Like a variable in Java! When there are many related libraries with the same version, you change **one** line. DRY! 🎯

> 💡 Older poms use two properties: `maven.compiler.source` and `maven.compiler.target`. `maven.compiler.release` is the modern, safer way.

### 🔍 Section 5: Dependencies

```xml
    <dependencies>
        <dependency>
            <groupId>com.google.code.gson</groupId>
            <artifactId>gson</artifactId>
            <version>${gson.version}</version>
        </dependency>

        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.11.3</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
```

The **shopping list** 🛒. The second dependency is **JUnit** (for tests — Chapter 84), and it has a new line: **`<scope>test</scope>`**.

---

## 🎯 Part 3: Dependency scopes — "when do I need this?"

Not every library is needed **all the time**. A **scope** tells Maven **when** to use it:

| Scope | Used when compiling `src/main`? | Used in tests? | Inside the final app? | Example |
|---|---|---|---|---|
| `compile` (**default**) | ✅ | ✅ | ✅ | Gson, Spring Boot starters |
| `test` | ❌ | ✅ | ❌ | JUnit, Mockito 🧪 |
| `runtime` | ❌ | ✅ | ✅ | database drivers (like PostgreSQL) 🗄️ |
| `provided` | ✅ | ✅ | ❌ (someone else provides it) | Lombok, old web servers |

📖 **Story:** Packing for a trip ✈️
- `compile` → clothes 👕: you need them **always**.
- `test` → the bathroom scale ⚖️: you use it **at home** to check your bag, but you don't take it on the trip.
- `runtime` → a power adapter 🔌: you don't need it to **pack**, but you need it **when you arrive**.

If you don't write a `<scope>`, it's **`compile`**.

👉 With `<scope>test</scope>`, JUnit is **only** available in `src/test/java`. If you try to `import org.junit...` in `src/main/java` → red error. That's correct! Tests and real code are **separate**. 🧪🚧☕

---

## 🧩 Part 4: Plugins — the build section

Plugins **do the work** of each lifecycle phase (Chapter 40). Maven has default plugins, so a simple pom doesn't need a `<build>` section. But you can **configure** them, or add new ones:

```xml
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
                <configuration>
                    <release>25</release>
                </configuration>
            </plugin>
        </plugins>
    </build>
```

| Line | Meaning |
|---|---|
| `<build>` | "How to build my project." |
| `<plugins>` | The list of plugins. |
| `<plugin>` | One plugin — with coordinates, like a dependency! (Plugins are also downloaded from Maven Central.) |
| `<configuration>` | Settings for this plugin. Each plugin has its own settings. |

### Common plugins

| Plugin | Job | Phase |
|---|---|---|
| `maven-compiler-plugin` | compiles Java code | `compile` |
| `maven-surefire-plugin` | runs tests | `test` |
| `maven-jar-plugin` | makes the JAR | `package` |
| **`spring-boot-maven-plugin`** 🌱 | makes a runnable "fat JAR", and lets you run the app with `mvnw spring-boot:run` | `package` |

---

## 🌱 Part 5: A real Spring Boot `pom.xml`, line by line

This is what you get from **Spring Initializr** (Chapter 49) for a web project with a database. Read it slowly — you'll see this file in **every** Spring Boot project! 🎉

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>4.0.0</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>

    <groupId>com.example</groupId>
    <artifactId>school</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>school</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>25</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

> ⚠️ **About version numbers:** Spring Boot gets new versions often. Your number (here `4.0.0`) will probably be **different** — and that's fine! **Always use the version that Spring Initializr gives you.** Also, the names of a few starters can change a little between big versions (for example, newer versions may show `spring-boot-starter-webmvc` instead of `spring-boot-starter-web`). Spring Initializr always gives you the **right** names for your version. 😊

### 🔍 Section 1: `<parent>` — inheriting from Spring Boot 👨‍👧

```xml
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>4.0.0</version>
        <relativePath/>
    </parent>
```

Remember **inheritance** (Chapter 22)? A pom can have a **parent** pom! Your pom **inherits** many settings from Spring Boot's parent:

| What you inherit | Why it's great |
|---|---|
| **Versions** of hundreds of libraries 📚 | You don't need to write `<version>` for Spring's libraries — they're chosen to **work together**. |
| Java compiler settings | Uses `java.version` automatically. |
| UTF-8 encoding | Already set. |
| Plugin settings | Tests, JAR building, resources... all configured. |

| Line | Meaning |
|---|---|
| `spring-boot-starter-parent` | The parent's name. |
| `<version>4.0.0</version>` | ⭐ The **Spring Boot version**. This **one number** decides the versions of **everything** else! |
| `<relativePath/>` | "Don't look for the parent in a nearby folder — download it from Maven Central." (Just copy it.) |

### 🔍 Section 2: Your project

```xml
    <groupId>com.example</groupId>
    <artifactId>school</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>school</name>
    <description>Demo project for Spring Boot</description>
```

Same as before — your project's ID card. 🪪

### 🔍 Section 3: Properties

```xml
    <properties>
        <java.version>25</java.version>
    </properties>
```

Just **one** property! The parent uses `java.version` to set up the compiler for you. Change it to `21` if you use Java 21.

### 🔍 Section 4: Dependencies — notice: NO versions! 😮

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
```

**No `<version>` line!** Where does the version come from? From the **parent**! Spring Boot's parent has a big list (called **dependency management**) that says: "for Spring Boot 4.0.0, use Jackson version X, Tomcat version Y, Hibernate version Z..." — all tested together. ✅

📖 **Story:** Buying a **LEGO set** 🧱 instead of single bricks. All the pieces in the box are made to **fit together**. You don't need to check each piece.

### 🔍 What are "starters"?

A **starter** is a dependency that brings a **whole package** of libraries for one job. 🎁

| Starter | What it brings | Chapter |
|---|---|---|
| `spring-boot-starter-web` | Spring MVC (web), Jackson (JSON), **Tomcat** (a web server inside your app!), validation basics | 51+ |
| `spring-boot-starter-data-jpa` | Spring Data JPA, Hibernate (talks to the database) | 70+ |
| `spring-boot-starter-validation` | `@NotBlank`, `@Email`, `@Size`... (Chapter 38!) | 65 |
| `spring-boot-starter-security` | login, passwords, roles | 80+ |
| `spring-boot-starter-test` | JUnit, Mockito, AssertJ, Spring test tools | 84+ |
| `spring-boot-starter-thymeleaf` | HTML pages | 89 |
| `spring-boot-starter-actuator` | health checks, metrics | 94 |

👉 Want a web app? Add **one** starter. Want a database? Add **one** starter. That's why it's called Spring **Boot** — it "boots" (starts) your project fast. 🚀

### 🔍 The database driver

```xml
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>
```

**H2** is a small database that runs **inside** your app (Chapter 69). Scope `runtime`: your code never `import`s H2 classes directly — Spring uses it **when the app runs**. 🔌

### 🔍 The test starter

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
```

All the testing tools, only for `src/test`. 🧪

### 🔍 Section 5: The Spring Boot plugin

```xml
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
```

This plugin gives you two superpowers:

| Command | What it does |
|---|---|
| `mvnw spring-boot:run` | **Starts** your Spring Boot app from the terminal. ▶️ |
| `mvnw clean package` | Makes a **fat JAR** 🍔 with **everything** inside (your code + all libraries + the web server). Run it anywhere with `java -jar target/school-0.0.1-SNAPSHOT.jar`. (Chapter 98.) |

Remember the `NoClassDefFoundError` in Chapter 40? The fat JAR fixes that problem. 🎉

---

## 🗺️ Part 6: The whole pom on one page

```
 pom.xml
 ├── 🏷️  header (xml, project, modelVersion)        → copy, don't touch
 ├── 👨‍👧 parent (spring-boot-starter-parent + version) → THE Spring Boot version
 ├── 🪪  groupId / artifactId / version / name       → who am I
 ├── ⚙️  properties (java.version)                   → settings / variables
 ├── 🛒 dependencies                                 → what I need
 │      ├── starters (no version needed!)
 │      ├── drivers (scope runtime)
 │      └── test tools (scope test)
 └── 🏗️  build / plugins                              → how to build me
        └── spring-boot-maven-plugin
```

---

## 🛠️ Part 7: Adding a dependency to a Spring Boot project

Let's say you want **Lombok** (Chapter 38) in your Spring Boot project.

**Way 1: Spring Initializr** — choose it when you create the project. ✅ Easiest.

**Way 2: By hand** — add to `<dependencies>`:

```xml
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
```

No version — the Spring Boot parent knows it! Then **Load Maven Changes** 🔄.

> 💡 How do you know if Spring Boot manages a library's version? Try **without** a version. If IntelliJ shows **red** (`'dependencies.dependency.version' for ... is missing`), Spring Boot doesn't manage it → add a `<version>`.

**Way 3: IntelliJ helper** — in `pom.xml`, press **Alt + Insert** → **Dependency** → search by name. ✨

---

## ✋ Try it yourself

**Task 1:** Read this XML. What is the city? What is wrong with the last line?

```xml
<school>
    <name>Green Hill</name>
    <address>
        <city>Nairobi</city>
    </address>
    <students>350</Students>
</school>
```

<details>
<summary>Click to see the answer</summary>

The city is Nairobi. The last element is wrong: `<students>` is closed with `</Students>` (capital S). XML is case-sensitive → it must be `</students>`.

</details>

**Task 2:** In your `hello-maven` project, add a property `<my.name>YourName</my.name>` and change `<name>` to `<name>${my.name}'s project</name>`. Reload. Does IntelliJ show the new name in the Maven window?

**Task 3:** Which scope would you choose?
1. A library to create fake test data, only for tests
2. The MySQL database driver
3. Gson, used in your main code

<details>
<summary>Click to see the answers</summary>

1. `test`
2. `runtime`
3. `compile` (the default — no `<scope>` needed)

</details>

**Task 4:** Look at the Spring Boot pom in Part 5. Answer without looking back at the explanations:
1. What is the Spring Boot version?
2. Which Java version does it use?
3. Why don't the starters have a `<version>`?
4. Which dependency is only for tests?
5. What does `spring-boot-maven-plugin` let you do?

**Task 5:** Version numbers! A library goes from `2.3.1` to:
- `2.3.2` → what kind of change?
- `2.4.0` → ?
- `3.0.0` → ?

<details>
<summary>Click to see the answers</summary>

- `2.3.2` → a small bug fix (PATCH)
- `2.4.0` → new features, nothing broken (MINOR)
- `3.0.0` → big changes, may break old code (MAJOR)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Broken XML

```
[FATAL] Non-parseable POM ... end tag name </dependecy> must match start tag name <dependency>
```

**Fix:** Check spelling and closing tags. IntelliJ shows XML errors in **red** right away.

### Mistake 2: Dependency outside `<dependencies>`

A `<dependency>` must be **inside** `<dependencies>`, which is **inside** `<project>`. Not inside `<build>` or `<properties>`!

### Mistake 3: Missing version (outside Spring Boot)

```
'dependencies.dependency.version' for com.google.code.gson:gson:jar is missing.
```

**Fix:** Add `<version>`. Only libraries managed by a parent (like Spring Boot's) can skip it.

### Mistake 4: Java version too high

```
error: release version 25 not supported
```

**Fix:** Change `java.version` (or `maven.compiler.release`) to your JDK version, e.g. `21`.

### Mistake 5: Mixing Spring Boot versions

Adding a Spring library with its **own** version number (that doesn't match the parent) → strange errors at startup. 😵
**Fix:** For Spring libraries, **don't** write a version. Let the parent decide.

### Mistake 6: Forgetting to reload

After **every** change in `pom.xml`: **Load Maven Changes** 🔄.

---

## ✅ Summary

- `pom.xml` is your project's **ID card** 🪪, written in **XML** (tags inside tags).
- **Coordinates:** `groupId`, `artifactId`, `version` (`SNAPSHOT` = in progress).
- **Properties** are variables: define `<gson.version>2.11.0</gson.version>`, use `${gson.version}`.
- **Dependencies** = the shopping list. **Scopes:** `compile` (default), `test`, `runtime`, `provided`.
- **Plugins** do the build work; configure them in `<build>`.
- **Spring Boot pom:**
  - `<parent>` = `spring-boot-starter-parent` → **one version number** decides all library versions.
  - `java.version` property.
  - **Starters** (`spring-boot-starter-web`, `-data-jpa`, `-test`...) bring whole packages — **no versions needed**.
  - `spring-boot-maven-plugin` → `spring-boot:run` and **fat JARs**.
- Always use the version and starter names that **Spring Initializr** gives you.
- After changing the pom → **reload**! 🔄

---

## ❓ Quiz

1. What does POM stand for?
2. In XML, what is the difference between `<version>` and `</version>`?
3. How do you use a property called `lib.version` in the pom?
4. What does `<scope>test</scope>` mean?
5. Why don't Spring Boot starters need a `<version>`?
6. What is a starter?
7. What does `spring-boot-maven-plugin` give you?
8. Where is the Spring Boot version written in the pom?

<details>
<summary>Click to see the answers</summary>

1. Project Object Model.
2. `<version>` is the opening tag; `</version>` is the closing tag.
3. `${lib.version}`
4. The library is only available for tests (`src/test`), not in the main code or the final app.
5. Because the parent (`spring-boot-starter-parent`) manages their versions.
6. A dependency that brings a whole set of libraries for one job (web, database, tests...).
7. Running the app with `spring-boot:run`, and building a runnable fat JAR.
8. In the `<parent>` section: `<version>` of `spring-boot-starter-parent`.

</details>

---

[⬅ Previous chapter](40-maven.md) | [Table of Contents](../README.md) | [Next chapter: Git ➡](42-git.md)
