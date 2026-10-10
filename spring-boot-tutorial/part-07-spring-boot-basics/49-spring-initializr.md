# Chapter 49 – Create a project with Spring Initializr

[⬅ Previous chapter](48-spring-and-spring-boot.md) | [Table of Contents](../README.md) | [Next chapter ➡](50-project-tour.md)

---

## 🎯 Goal

Today is a big day: you create your **first real Spring Boot project**! 🎉

At the end of this chapter you will know:

- What **Spring Initializr** is
- What **every field** on the Spring Initializr page means
- How to add **dependencies** (like "Spring Web")
- How to **download**, **unzip** and **open** the project in IntelliJ
- How to fix the most common problems when opening a project
- A bonus trick: creating a project with **one curl command** 😎

> 🌱 We'll call this project **`hello`**. You'll use it in **all** chapters of Part 7. So please follow the steps exactly. 🙏

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Spring Initializr** | A free **website** that creates a new, empty Spring Boot project for you. (Yes, it's spelled "Initializr", without the "e" before "r". 😄) |
| **Project metadata** | Information **about** the project: its name, group, package, Java version. |
| **Group** | The name of your **company or team**, written backwards like a web address: `com.example`. |
| **Artifact** | The **name of the project** itself: `hello`. |
| **Dependency** | A library your project needs (Chapter 40). |
| **Packaging** | What kind of file Maven makes at the end: **Jar** (normal) or War (old style). |
| **SNAPSHOT** | A version that is **still being built**. Not finished. Don't use it for learning! |
| **M1, M2, RC1** | "Milestone" and "Release Candidate": **test** versions before the final one. |
| **Import** | When IntelliJ **reads** your project and downloads everything it needs. |

---

## 📖 Story: The pizza order form 🍕

When you order pizza online, you fill out a **form**:

- Size? 🍕 *Medium*
- Crust? *Thin*
- Toppings? *Cheese, mushrooms, olives*
- Delivery address? *My home*

You press **Order**, and 30 minutes later a ready pizza arrives. You didn't make the dough. You didn't build the oven. You **chose** what you wanted.

**Spring Initializr** is the **order form** for Spring Boot projects:

- Size and crust → **Maven, Java, Spring Boot version**
- Toppings → **dependencies** (Spring Web, database, security...)
- Name on the box → **group and artifact**

You press **Generate**, and you get a **ready project** as a zip file. 📦 You didn't write the folders, the `pom.xml`, or the main class. You **chose** what you wanted. 🎉

---

## 🌐 Part 1: Open Spring Initializr

1. Open your web browser.
2. Go to: **https://start.spring.io**

You'll see a page like this (simplified drawing):

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  🌱 spring initializr                                                          │
├──────────────────────────────────────┬───────────────────────────────────────┤
│ Project                              │ Dependencies        [ADD DEPENDENCIES] │
│  ○ Gradle - Groovy                   │                                        │
│  ○ Gradle - Kotlin                   │  No dependency selected                │
│  ● Maven                             │                                        │
│                                      │                                        │
│ Language                             │                                        │
│  ● Java   ○ Kotlin   ○ Groovy        │                                        │
│                                      │                                        │
│ Spring Boot                          │                                        │
│  ○ 4.2.0 (SNAPSHOT)  ○ 4.2.0 (M2)    │                                        │
│  ○ 4.1.2 (SNAPSHOT)  ● 4.1.1         │                                        │
│  ○ 4.0.9 (SNAPSHOT)  ○ 4.0.8         │                                        │
│                                      │                                        │
│ Project Metadata                     │                                        │
│  Group        [com.example        ]  │                                        │
│  Artifact     [demo               ]  │                                        │
│  Name         [demo               ]  │                                        │
│  Description  [Demo project for...]  │                                        │
│  Package name [com.example.demo   ]  │                                        │
│  Packaging     ● Jar   ○ War         │                                        │
│  Java          ○ 27  ○ 25  ○ 21  ● 17│                                        │
├──────────────────────────────────────┴───────────────────────────────────────┤
│        [ GENERATE  CTRL + ⏎ ]   [ EXPLORE  CTRL + SPACE ]   [ SHARE... ]       │
└──────────────────────────────────────────────────────────────────────────────┘
```

> 💡 The website changes a little over time. The **numbers** you see will be different (newer!). The colors and layout may move. That's OK — the **fields** are almost always the same. Read on, and you'll understand each one. 😊

---

## 📋 Part 2: Fill out the form — field by field

Let's go from top to bottom. ⬇️

### 1️⃣ Project: **Maven**

| Choice | Meaning |
|---|---|
| Gradle - Groovy | Another build tool, with settings in a Groovy file |
| Gradle - Kotlin | Another build tool, with settings in a Kotlin file |
| **Maven** ✅ | The build tool you learned in **Chapter 40**, with `pom.xml` (Chapter 41) |

👉 Choose **Maven**.

### 2️⃣ Language: **Java**

Spring Boot also works with Kotlin and Groovy (other languages that run on the Java machine). We learned Java. 👉 Choose **Java**.

### 3️⃣ Spring Boot version: **the newest one without extra words**

You'll see a list like:

```
○ 4.2.0 (SNAPSHOT)
○ 4.2.0 (M2)
○ 4.1.2 (SNAPSHOT)
● 4.1.1              ← ✅ this one!
○ 4.0.9 (SNAPSHOT)
○ 4.0.8
```

| Word after the number | Meaning | Use it? |
|---|---|---|
| **(SNAPSHOT)** | "Still being built. May change every day." 🏗️ | ❌ No |
| **(M1), (M2)...** | "Milestone": a test version. | ❌ No |
| **(RC1), (RC2)...** | "Release Candidate": almost finished, still a test. | ❌ No |
| **nothing** | A **finished, stable** version. ✅ | ✅ **Yes!** |

👉 Choose the **highest number** that has **no** word in brackets. Usually the website already selects it for you. (In this book, that was **4.1.1**. Yours will probably be newer — that's great!)

> ⚠️ **Version note:** In Chapter 41, our example `pom.xml` showed `4.0.0`. Now we see `4.1.1`. Spring Boot gets a new version **every few months**. Everything in this book works the same with newer `4.x` versions. If something has a different name in your version, **trust Spring Initializr**. 😊

### 4️⃣ Project Metadata

This is the "name on the pizza box" part. Fill it out **exactly** like this:

| Field | Type this | What it means |
|---|---|---|
| **Group** | `com.example` | Your company or team name, **backwards**. A company with the website `school.org` would use `org.school`. We don't have a company, so `com.example` is fine. |
| **Artifact** | `hello` | The **project name**. Use small letters, no spaces. It becomes the **folder name** and the **jar name** (`hello-0.0.1-SNAPSHOT.jar`). |
| **Name** | `hello` | A display name. It fills itself when you type the artifact. It's used for the main class name: `hello` → **`HelloApplication`**. |
| **Description** | `My first Spring Boot app` | A short sentence about the project. It goes into the `pom.xml`. Write anything you like. |
| **Package name** | `com.example.hello` | ⭐ The **base package** (Chapter 26). It fills itself: **group + artifact**. All your classes will live here. |
| **Packaging** | **Jar** | Make a `.jar` file. (**War** is an old style for putting apps into separate servers. We don't need it.) |
| **Java** | **25** | The Java version. Choose the version **you installed** in Chapter 3. |

> ⚠️ **Java version — very important!** The Java number you choose here must **not be higher** than the Java on your computer.
>
> - You installed Java **25** (Chapter 3)? → choose **25** ✅ (or 21, or 17 — lower is OK too).
> - You have Java **21**? → choose **21** or **17**. Not 25! ❌
>
> Not sure? Open a terminal and type `java -version` (Chapter 3).

> 💡 **Configuration: Properties / YAML** — some versions of the page also show this choice. If you see it, choose **Properties**. (We'll learn about both in Chapter 55.)

### 5️⃣ Dependencies: **Spring Web**

Now the **toppings**! 🍄🫒

1. Click **ADD DEPENDENCIES...** (top right). Or press **Ctrl + B**.
2. A search box opens. Type: **`web`**
3. You'll see a list. Click **Spring Web**:

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔍 web                                                           │
├─────────────────────────────────────────────────────────────────┤
│ Spring Web                                              WEB      │
│ Build web, including RESTful, applications using Spring MVC.    │
│ Uses Apache Tomcat as the default embedded container.           │
├─────────────────────────────────────────────────────────────────┤
│ Spring Reactive Web                                     WEB      │
│ ...                                                              │
└─────────────────────────────────────────────────────────────────┘
```

Read the description: "Build web, including **RESTful**, applications using Spring MVC. Uses **Apache Tomcat** as the default embedded container." — you understand **every word** of that now! 🤓 (REST = Chapter 46, embedded Tomcat = Chapter 48.)

4. Now under **Dependencies** you see:

```
Dependencies                                     [ADD DEPENDENCIES...]
┌────────────────────────────────────────────────────────────────┐
│ Spring Web  WEB                                            [ ✕ ] │
│ Build web, including RESTful, applications using Spring MVC... │
└────────────────────────────────────────────────────────────────┘
```

> ⚠️ Choose **Spring Web**, **not** "Spring Reactive Web". Reactive is a different, more advanced style. 🙅

> 💡 **Only Spring Web for now.** Later in the book, you'll add more: **Validation** (Chapter 65), **Spring Data JPA** and **H2 Database** (Part 9), **Spring Security** (Part 10)... You can always add dependencies **later** by editing `pom.xml`. You don't need to choose everything today.

### ✅ Your finished form

```
Project:       Maven
Language:      Java
Spring Boot:   4.1.1   (or the newest without SNAPSHOT/M/RC)
Group:         com.example
Artifact:      hello
Name:          hello
Description:   My first Spring Boot app
Package name:  com.example.hello
Packaging:     Jar
Java:          25      (or the version you installed)
Dependencies:  Spring Web
```

---

## 👀 Part 3: Look before you download — EXPLORE

Before downloading, click **EXPLORE** (bottom). Or press **Ctrl + Space**.

A window opens and shows **all files** of your future project. You can click on them and read them! 👀

```
hello
├── .mvn
│   └── wrapper
│       └── maven-wrapper.properties
├── src
│   ├── main
│   │   ├── java
│   │   │   └── com
│   │   │       └── example
│   │   │           └── hello
│   │   │               └── HelloApplication.java
│   │   └── resources
│   │       ├── static
│   │       ├── templates
│   │       └── application.properties
│   └── test
│       └── java
│           └── com
│               └── example
│                   └── hello
│                       └── HelloApplicationTests.java
├── .gitattributes
├── .gitignore
├── HELP.md
├── mvnw
├── mvnw.cmd
└── pom.xml
```

Click on **`pom.xml`**. Do you recognize it from Chapter 41? 😊 Click on **`HelloApplication.java`**. That's the main class. We'll read every line in the next chapter.

Close the window when you're done.

---

## 📦 Part 4: Generate and unzip

1. Click **GENERATE** (or press **Ctrl + Enter**).
2. Your browser downloads a file: **`hello.zip`** 📦 (very small — about 15 KB!).

> 🤔 **Only 15 KB?** Where is Spring Boot? Where is Tomcat? They're **not** in the zip! The zip has only **your** project files. Maven will download the libraries **later**, when you open the project (Chapter 40). 📥

3. Now **unzip** it. Where should you put it? A good place is your IntelliJ projects folder:

| Computer | Good folder |
|---|---|
| Windows | `C:\Users\YourName\IdeaProjects\` |
| Mac | `/Users/YourName/IdeaProjects/` |
| Linux | `/home/yourname/IdeaProjects/` |

**On Windows:**

- Go to your **Downloads** folder.
- **Right-click** `hello.zip` → **Extract All...**
- Change the folder to `C:\Users\YourName\IdeaProjects`
- Click **Extract**.

**On Mac:** double-click `hello.zip`. A `hello` folder appears. Move it to your `IdeaProjects` folder.

### ⚠️ The "folder in a folder" trap 🪆

The zip already **contains** a folder called `hello`. Sometimes Windows creates **another** `hello` folder around it:

```
IdeaProjects
└── hello            ← extra folder made by Windows 😕
    └── hello        ← ✅ the REAL project (pom.xml is here!)
        ├── pom.xml
        ├── src
        └── ...
```

That's not a big problem. Just remember: **the real project folder is the one that has `pom.xml` inside**. ✅ (You can also move the inner folder up, and delete the empty outer one.)

---

## 💡 Part 5: Open the project in IntelliJ

1. Start **IntelliJ IDEA**.
2. If you see the **Welcome** screen, click **Open**. If a project is already open, use **File → Open...**
3. Find the **`hello`** folder (the one with `pom.xml` inside!). Select the **folder** and click **OK** (or **Open**).

```
📁 IdeaProjects
   📁 hello           ← select THIS folder (it has pom.xml)
      📁 .mvn
      📁 src
      📄 pom.xml
```

4. IntelliJ may ask: **"Trust and Open Project 'hello'?"** — Click **Trust Project**. ✅ (It's your project. You made it!)
5. Now **wait**. ⏳ Look at the **bottom right** of IntelliJ. You'll see a small progress bar, something like:

```
Resolving dependencies of hello...    ▓▓▓▓▓▓░░░░░
```

IntelliJ is reading `pom.xml` and **Maven is downloading** Spring Boot, Tomcat, Jackson, and the other libraries from the internet. 📥

- The **first time** takes a few minutes (maybe 2–5, depending on your internet). ☕
- The **next** projects are much faster, because the libraries are saved on your computer (in the `.m2` folder — Chapter 40).

6. When the progress bar is gone, the project is ready! 🎉

### 🗂️ What you see now

On the left side, the **Project** window (press **Alt + 1** if you don't see it):

```
hello  C:\Users\YourName\IdeaProjects\hello
├── .idea                 ← IntelliJ's own settings (ignore it)
├── .mvn
├── src
│   ├── main
│   │   ├── java
│   │   │   └── com.example.hello
│   │   │       └── HelloApplication
│   │   └── resources
│   │       ├── static
│   │       ├── templates
│   │       └── application.properties
│   └── test
│       └── java
│           └── com.example.hello
│               └── HelloApplicationTests
├── .gitattributes
├── .gitignore
├── HELP.md
├── mvnw
├── mvnw.cmd
├── pom.xml
├── External Libraries     ← all the downloaded libraries! 📚
└── Scratches and Consoles
```

> 💡 IntelliJ shows packages **compact**: `com.example.hello` in one line instead of three folders. On your disk, they are still three folders: `com` → `example` → `hello` (Chapter 26).

Open **External Libraries** (click the little arrow ▶). You'll see a long list like:

```
< 25 >
Maven: org.springframework.boot:spring-boot:4.1.1
Maven: org.springframework.boot:spring-boot-autoconfigure:4.1.1
Maven: org.springframework:spring-core:7.0.9
Maven: org.springframework:spring-webmvc:7.0.9
Maven: org.apache.tomcat.embed:tomcat-embed-core:11.0.24
Maven: tools.jackson.core:jackson-databind:3.1.5
...
```

**All of these** came from **one** dependency (Spring Web)! That's the power of a **starter** (Chapter 41). 📦✨ And look: **Spring Framework 7**, **Tomcat 11**, **Jackson 3** — just like we said in Chapter 48.

---

## 🔍 Part 6: Your pom.xml — what's new?

Double-click **`pom.xml`** to open it. Here is the real file that Spring Initializr made:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>4.1.1</version>
		<relativePath/> <!-- lookup parent from repository -->
	</parent>
	<groupId>com.example</groupId>
	<artifactId>hello</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<name>hello</name>
	<description>My first Spring Boot app</description>
	<url/>
	<licenses>
		<license/>
	</licenses>
	<developers>
		<developer/>
	</developers>
	<scm>
		<connection/>
		<developerConnection/>
		<tag/>
		<url/>
	</scm>
	<properties>
		<java.version>25</java.version>
	</properties>
	<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-webmvc</artifactId>
		</dependency>

		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-webmvc-test</artifactId>
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

You know most of this from **Chapter 41**! 🎉 Let's look only at the parts that are **new** or **different**:

| Code | Meaning |
|---|---|
| `<version>4.1.1</version>` (in `<parent>`) | ⭐ The Spring Boot version you chose on the website. This one number decides the versions of **all** the libraries. |
| `<relativePath/>` | "Don't look for the parent on my disk. Download it." You never change this. |
| `<groupId>com.example</groupId>` | Your **Group** from the form. |
| `<artifactId>hello</artifactId>` | Your **Artifact** from the form. |
| `<version>0.0.1-SNAPSHOT</version>` | **Your** project's version. "0.0.1, still being built." (Yes — your project is a SNAPSHOT, because you're still building it! 😄) |
| `<description>My first Spring Boot app</description>` | Your **Description** from the form. |
| `<url/>`, `<licenses>`, `<developers>`, `<scm>` | **Empty** tags. They only **stop** Maven from copying Spring's own information (Spring's license, Spring's developers) into **your** project. You can ignore them. 🙈 |
| `<java.version>25</java.version>` | The **Java** version from the form. |
| `spring-boot-starter-webmvc` | ⭐ The **Spring Web** dependency you chose! Spring MVC + Tomcat + Jackson + more. No `<version>` — the parent decides. |
| `spring-boot-starter-webmvc-test` with `<scope>test</scope>` | Tools for **testing** web apps (Part 11). Only used for tests, not put in the final app. Spring Initializr adds it for you. |
| `spring-boot-maven-plugin` | The plugin that can **run** your app (`spring-boot:run`) and make the runnable **jar** (Chapter 98). |

> 💡 **Remember from Chapter 41:** you may also see `spring-boot-starter-web` and `spring-boot-starter-test` in older projects and older tutorials on the internet. Those are the **older names**. They do the same job. ✅

---

## 😎 Part 7: Bonus — a project with one curl command

You learned **curl** in Chapter 47. Spring Initializr also works with curl! This command makes **exactly** the same project as the form:

```bash
curl https://start.spring.io/starter.zip \
  -d type=maven-project \
  -d language=java \
  -d groupId=com.example \
  -d artifactId=hello \
  -d name=hello \
  -d "description=My first Spring Boot app" \
  -d packageName=com.example.hello \
  -d javaVersion=25 \
  -d dependencies=web \
  -d baseDir=hello \
  -o hello.zip
```

(Use **Git Bash** for this on Windows — Chapter 47.)

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `curl https://start.spring.io/starter.zip` | Ask Spring Initializr for a **zip** file. |
| `\` | "The command continues on the next line." (Only for readability.) |
| `-d type=maven-project` | Project: **Maven**. |
| `-d language=java` | Language: **Java**. |
| `-d groupId=com.example` | Group. |
| `-d artifactId=hello` | Artifact. |
| `-d name=hello` | Name. |
| `-d "description=My first Spring Boot app"` | Description. In quotes, because it has **spaces**. |
| `-d packageName=com.example.hello` | Package name. |
| `-d javaVersion=25` | Java version. |
| `-d dependencies=web` | Dependencies. `web` = Spring Web. More? Use commas: `web,validation`. |
| `-d baseDir=hello` | Put the files inside a folder called `hello` in the zip. |
| `-o hello.zip` | Save the answer in a file called `hello.zip`. |

We didn't write the **Spring Boot version**, so Spring Initializr uses its **default** (the newest stable one). 👍

> 💡 You don't **need** this trick. The website is perfect for beginners. But it shows something cool: **Spring Initializr is a REST API!** 🤯 The website is just a nice form that calls it. Everything you learned in Part 6 is everywhere!

---

## 🔧 Part 8: Other ways to create a project

| Way | Notes |
|---|---|
| **start.spring.io** (website) ✅ | Free, works for everybody. **We use this.** |
| IntelliJ IDEA **Ultimate** (paid) | Has **File → New → Project → Spring Boot**. It uses Spring Initializr **inside** IntelliJ. Same result. |
| IntelliJ free version | The Spring Boot wizard is **not** included. Use the website, then **Open**. (What you just did! ✅) |
| **VS Code** with "Spring Boot Extension Pack" | Press **Ctrl + Shift + P** → "Spring Initializr: Create a Maven Project". |
| curl | Part 7 above. 😎 |

All of them use **the same** Spring Initializr behind the scenes. So the project is always the same. 👍

---

## 💻 Mini project: Make a second project by yourself 🏋️

Practice makes perfect! Create **another** project, all alone, with these settings:

| Field | Value |
|---|---|
| Project | Maven |
| Language | Java |
| Spring Boot | newest stable |
| Group | `com.myschool` |
| Artifact | `school` |
| Description | `School information app` |
| Java | your version |
| Dependencies | Spring Web |

Before you click Generate, **guess** the answers:

1. What will the **package name** be?
2. What will the **main class** be called?
3. What will the **jar file** be called (Chapter 41: artifactId + version)?

Then click **EXPLORE** and check your guesses! Generate, unzip, and open it in IntelliJ (choose **New Window** when IntelliJ asks, so both projects stay open).

<details>
<summary>Click to see the answers</summary>

1. Package name: `com.myschool.school` (group + artifact).
2. Main class: `SchoolApplication` (the name, starting with a capital letter, plus "Application").
3. Jar file: `school-0.0.1-SNAPSHOT.jar`.

</details>

> 💡 We'll keep using the **`hello`** project in the next chapters. You can close the `school` project when you're done (**File → Close Project**).

---

## ✋ Try it yourself

**Task 1:** On start.spring.io, change **Artifact** to `my-shop`. What happens to **Name** and **Package name**?

<details>
<summary>Click to see the answer</summary>

Name becomes `my-shop`. Package name becomes `com.example.my_shop` — the **minus sign** `-` is changed to an **underscore** `_`, because a minus is **not allowed** in Java package names (Chapter 26). The main class will be `MyShopApplication`. 🧐

</details>

**Task 2:** On start.spring.io, add these dependencies by searching: **Validation**, **Spring Boot DevTools**, **H2 Database**. Then click **EXPLORE** and look at `pom.xml`. How many `<dependency>` blocks do you see? Then **remove** them again (click the ✕) — we don't need them yet!

<details>
<summary>Click to see the answer</summary>

With Spring Boot 4.1.1 we saw **7** blocks:

- `spring-boot-starter-webmvc` and `spring-boot-starter-webmvc-test` (Spring Web)
- `spring-boot-starter-validation` and `spring-boot-starter-validation-test` (Validation)
- `spring-boot-devtools` with `<scope>runtime</scope>` and `<optional>true</optional>` (DevTools)
- `h2` with `<scope>runtime</scope>` (the H2 database)
- `spring-boot-h2console` (a small web page to look inside H2 — Spring Initializr added it because you chose **both** Web and H2! 🤓)

Your number may be a little different in another version — that's fine. The point is: **every topping you choose becomes a `<dependency>` in pom.xml.** 🍕

</details>

**Task 3:** Look at the **Share...** button at the bottom of start.spring.io. Click it. What do you get?

<details>
<summary>Click to see the answer</summary>

A **link** (URL) that contains all your choices in its **query** (Chapter 43: `?type=maven-project&language=java&...`). Send it to a friend, and they get the **same** form, already filled out! 🔗

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Choosing a SNAPSHOT or M version

```
○ 4.2.0 (SNAPSHOT)    ← ❌ unfinished
○ 4.2.0 (M2)          ← ❌ test version
● 4.1.1               ← ✅
```

Test versions can have bugs, and tutorials (like this book) may not match. **Fix:** Create the project again with a **stable** version.

### Mistake 2: Java version on the website is higher than on your computer

You chose **Java 25** on the website, but your computer has **Java 21**. When IntelliJ (or Maven) builds the project, you see:

```
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.15.0:compile (default-compile) on project hello: Fatal error compiling: error: release version 25 not supported -> [Help 1]
```

"**release version 25 not supported**" = "You asked for Java 25, but I only know Java 21." 😕

**Fix (choose one):**
- Install Java 25 (Chapter 3), **or**
- Open `pom.xml` and change `<java.version>25</java.version>` to your version, like `21`. Then click the **Maven reload** button 🔄 (top right of the editor, or in the Maven window).

### Mistake 3: Forgetting the Spring Web dependency

Your project has **no** `spring-boot-starter-webmvc` in `pom.xml`. The app starts... and **stops immediately**! No Tomcat, no port 8080. 😮

**Fix:** Add it to `pom.xml` (inside `<dependencies>`):

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc</artifactId>
</dependency>
```

Then click **Maven reload** 🔄. (Or create the project again with Spring Web.)

### Mistake 4: Opening the zip file instead of the folder

IntelliJ can't open a `.zip` as a project. **Fix:** **Unzip** first, then open the **folder** with `pom.xml` inside.

### Mistake 5: Opening the wrong folder 🪆

You opened `IdeaProjects` (or the extra outer `hello`). IntelliJ shows folders, but **no Maven project**: no `External Libraries`, Java files look strange (no colors, red underlines). **Fix:** **File → Close Project**, then open the folder that **directly contains** `pom.xml`.

### Mistake 6: "Project JDK is not defined" / red code everywhere

At the top of a Java file, IntelliJ shows a yellow bar: **"Project JDK is not defined"** or **"Setup SDK"**.

**Fix:** Click **Setup SDK** (in that yellow bar) → choose your Java (**25**). Or: **File → Project Structure... → Project → SDK** → choose Java 25 → **OK**.

### Mistake 7: No internet / downloads hanging

The first import needs **internet**, to download the libraries. If the progress bar never ends, or you see "Could not resolve dependencies":

**Fix:** Check your internet. Then, in the **Maven** window (the **"m"** icon on the right side of IntelliJ), click **Reload All Maven Projects** 🔄.

---

## ✅ Summary

- **Spring Initializr** (**start.spring.io**) is the "order form" 🍕 for new Spring Boot projects.
- Choose: **Maven**, **Java**, the newest **stable** Spring Boot (no SNAPSHOT/M/RC), **Jar**, and **your** Java version (not higher than installed!).
- Metadata: **Group** `com.example` + **Artifact** `hello` → **package** `com.example.hello` → main class **`HelloApplication`**.
- Dependencies are the "toppings". For a web API, add **Spring Web**.
- **EXPLORE** shows the files before you download. **GENERATE** downloads a small zip (libraries come later).
- Unzip, then **Open** the folder with **`pom.xml`** in IntelliJ, **Trust** it, and **wait** for Maven to download everything.
- **External Libraries** shows all the libraries that one starter brought. 📚
- Spring Initializr is a **REST API** — you can even use it with **curl**. 😎

---

## ❓ Quiz

1. What is the address of Spring Initializr?
2. Which Spring Boot version should you choose: `4.2.0 (M2)`, `4.1.2 (SNAPSHOT)`, or `4.1.1`?
3. Group is `org.zoo` and artifact is `animals`. What is the package name?
4. What is the main class called if the name is `animals`?
5. Which dependency do you need to build a REST API?
6. Why is the downloaded zip so small?
7. In IntelliJ, which folder do you open?
8. You see `release version 25 not supported`. What does it mean? How do you fix it?
9. What does **EXPLORE** do?

<details>
<summary>Click to see the answers</summary>

1. **https://start.spring.io**
2. `4.1.1` — it's the only stable version (no SNAPSHOT/M/RC).
3. `org.zoo.animals`
4. `AnimalsApplication`
5. **Spring Web** (`spring-boot-starter-webmvc`).
6. It contains only your project files. Maven downloads the libraries later, when you open the project.
7. The project folder that directly contains `pom.xml`.
8. The project wants Java 25, but your computer's Java is older. Install Java 25, or change `<java.version>` in `pom.xml` to your Java version and reload Maven.
9. It shows all files of the project **before** you download it.

</details>

---

[⬅ Previous chapter](48-spring-and-spring-boot.md) | [Table of Contents](../README.md) | [Next chapter: A tour of the project folders ➡](50-project-tour.md)
