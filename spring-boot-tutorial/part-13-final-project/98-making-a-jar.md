# Chapter 98 – Making a .jar file

[⬅ Previous chapter](97-library-security-tests.md) | [Table of Contents](../README.md) | [Next chapter ➡](99-docker.md)

---

## 🎯 Goal

Until now, your app only ran **inside IntelliJ** (or with `./mvnw spring-boot:run`). But a server on the internet has **no** IntelliJ! 🙅 It needs your app as **one** file it can start.

Today you'll pack the Library app into a **`.jar` file** 📦 — and run it like a real server would.

At the end of this chapter you will know:

- What a **`.jar`** file is, and why Spring Boot's is "**fat**" 🍔
- How to build it with **`./mvnw clean package`**
- How to start it with **`java -jar`**
- How to change **settings** without rebuilding: arguments, environment variables, profiles ⚙️
- How to prepare a **`prod`** profile with a real database 🐘
- How to **stop** the app nicely

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **JAR** | **J**ava **AR**chive: a **zip** file full of Java classes (and other files). 📦 |
| **Fat jar** | A jar that contains your code **and** all the libraries it needs. Everything in **one** file. 🍔 |
| **Build** | Turning your source code into something that can run: compile, test, pack. 🏭 |
| **Artifact** | The **result** of a build — here, the `.jar` file. |
| **Command-line argument** | Extra text you give a program when you start it: `java -jar app.jar --server.port=9090`. |
| **Environment variable** | A setting stored in the **computer's** environment, outside your app (Chapter 77). 🌍 |
| **Graceful shutdown** | Stopping nicely: finish the requests that are running, then stop. 🙇 |

---

## 📖 Story: Packing for a school trip 🎒

Before a school trip, you pack **one** backpack 🎒 with **everything** you need: clothes, a toothbrush, snacks, your water bottle. At the camp, there's no shop — if you forgot something, you don't have it! 😬

But your **parents** can still call the camp and say: "Sara should go to bed at 9 tonight!" — they change the **rules** without unpacking the backpack. 📞

A **fat jar** is your app's backpack:

| School trip 🎒 | Your app 📦 |
|---|---|
| The backpack | The `.jar` file |
| Clothes, snacks, toothbrush | Your classes **plus** Spring, Tomcat, Hibernate, H2, Jackson... |
| "No shop at the camp" | The server only needs **Java** — nothing else |
| Parents call with new rules | Arguments and environment variables change the **settings** |

---

## 🏭 Part 1: Build the jar

Open a terminal in the **`library`** project folder and run:

```bash
./mvnw clean package
```

(Windows Command Prompt: `mvnw clean package`. PowerShell: `.\mvnw clean package` — Chapter 50.)

| Part | Meaning |
|---|---|
| `clean` | Delete the old `target` folder first — a fresh start. 🧹 |
| `package` | Compile → **run all tests** → pack the jar. 📦 |

Maven works for a while (the **tests** take most of the time!) and ends with something like:

```
[INFO] Tests run: 21, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] --- jar:3.4.2:jar (default-jar) @ library ---
[INFO] Building jar: .../library/target/library-0.0.1-SNAPSHOT.jar
[INFO] 
[INFO] --- spring-boot:4.1.1:repackage (repackage) @ library ---
[INFO] Replacing main artifact .../library/target/library-0.0.1-SNAPSHOT.jar with repackaged archive, adding nested dependencies in BOOT-INF/.
[INFO] BUILD SUCCESS
```

(The exact numbers and versions on your computer may be a bit different.)

| Line | Meaning |
|---|---|
| `Tests run: 21, Failures: 0` | ⭐ **All** tests ran first. A red test → **no** jar! Broken code can't be packed. 🛡️ |
| `Building jar: ...library-0.0.1-SNAPSHOT.jar` | Maven packs **your** classes into a normal jar. |
| `spring-boot:...:repackage` | ⭐ The **Spring Boot Maven plugin** (from `pom.xml`, Chapter 41) makes it **fat**: it adds all libraries. 🍔 |

Look into **`target/`**: there's **`library-0.0.1-SNAPSHOT.jar`**. Its size? About **60 MB**! Your own code is only a few hundred KB — the rest is Spring, Tomcat, Hibernate... all packed in. 🎒

| Name part | Meaning |
|---|---|
| `library` | The `artifactId` from `pom.xml`. |
| `0.0.1-SNAPSHOT` | The `version` from `pom.xml`. **SNAPSHOT** = "still being worked on". A finished version would be `1.0.0`. |

### 🔍 Look inside

A jar **is** a zip file. Make a copy, rename it to `.zip`, and open it:

```
 library-0.0.1-SNAPSHOT.jar
 ├── BOOT-INF/
 │   ├── classes/        ← YOUR code: com/example/library/..., application.properties
 │   └── lib/            ← ALL libraries: spring-core-....jar, tomcat-embed-core-....jar, hibernate-core-....jar, h2-....jar, ...
 ├── META-INF/
 │   └── MANIFEST.MF     ← "how to start me"
 └── org/springframework/boot/loader/...   ← Spring Boot's little starter program
```

Jars **inside** a jar! 🪆 That's the fat jar trick.

---

## ▶️ Part 2: Run it

Stop the app in IntelliJ (only one program can use port 8080!). Then:

```bash
java -jar target/library-0.0.1-SNAPSHOT.jar
```

The well-known Spring Boot banner appears, and the same log as in IntelliJ:

```
 :: Spring Boot ::                (v4.1.1)
...
... Tomcat started on port 8080 (http) with context path '/'
... Started LibraryApplication in 4.2 seconds
```

🎉 Your app runs **without** IntelliJ, **without** Maven — only **Java** is needed. Test it: `curl http://localhost:8080/api/books` works! 📚

⭐ This **one** command is what every server in the world will do with your app — including Docker in the next chapter. 🌍

### 🛑 Stopping it

Press **Ctrl+C** in the terminal. Spring Boot shuts down **gracefully** 🙇: it stops taking new requests, lets the running ones finish, closes the database connections... and only then stops. You'll see lines like:

```
... Commencing graceful shutdown. Waiting for active requests to complete
... Graceful shutdown complete
```

---

## ⚙️ Part 3: Changing settings without rebuilding

The jar is packed — but you can still change **any** setting from `application.properties` when you **start** it. 📞

### 1️⃣ Command-line arguments

```bash
java -jar target/library-0.0.1-SNAPSHOT.jar --server.port=9090 --library.loan.days=21
```

| Part | Meaning |
|---|---|
| `--server.port=9090` | ⭐ Any setting, written as `--name=value`. Now the app listens on port **9090**. |
| `--library.loan.days=21` | Summer holidays: loans last 21 days! ☀️ No code change, no rebuild. |

### 2️⃣ Environment variables

You know these from Chapter 77 (`DB_PASSWORD`) and 83 (`JWT_SECRET`). Spring also turns **any** setting name into an environment variable name: **big letters**, and `_` instead of `.` and `-`:

| Setting | Environment variable |
|---|---|
| `server.port` | `SERVER_PORT` |
| `library.loan.days` | `LIBRARY_LOAN_DAYS` |
| `spring.profiles.active` | `SPRING_PROFILES_ACTIVE` |

```bash
# Git Bash / Mac / Linux: set it just for this one command
LIBRARY_LOAN_DAYS=21 java -jar target/library-0.0.1-SNAPSHOT.jar
```

```powershell
# Windows PowerShell
$env:LIBRARY_LOAN_DAYS = "21"
java -jar target\library-0.0.1-SNAPSHOT.jar
```

### 🏆 Who wins?

When the same setting comes from several places, Spring uses this order (highest wins):

```
 1. Command-line arguments       --server.port=9090        🥇
 2. Environment variables        SERVER_PORT=9090          🥈
 3. application-{profile}.properties                       🥉
 4. application.properties  (inside the jar)
```

So `application.properties` holds **sensible defaults**, and the server **overrides** what it needs. 👍

---

## 🐘 Part 4: A `prod` profile

On a real server, we don't want an H2 file — we want a **real** database like PostgreSQL (Chapter 77). Let's prepare a **`prod`** profile.

Add the PostgreSQL driver to **`pom.xml`**:

```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

Create **`src/main/resources/application-prod.properties`**:

```properties
# Production: a real PostgreSQL database
spring.datasource.url=${DB_URL}
spring.datasource.username=${DB_USERNAME}
spring.datasource.password=${DB_PASSWORD}

# Secrets MUST come from outside: no defaults here!
library.jwt.secret=${JWT_SECRET}
library.librarian.password=${LIBRARIAN_PASSWORD}

# Quieter logs, and a log file
logging.level.root=INFO
logging.file.name=logs/library.log
```

| Code | Meaning |
|---|---|
| `${DB_URL}` | ⭐ **No** default value after a `:`. If the variable is **missing**, the app **refuses to start** (*"Could not resolve placeholder 'DB_URL'"*). That's **good**: better no app than an app with a learning password! 🛡️ |
| `library.jwt.secret=${JWT_SECRET}` | Overrides the learning default from `application.properties`. |
| `logging.file.name` | A log file for the server (Chapter 88). |

Start it with the `prod` profile:

```bash
SPRING_PROFILES_ACTIVE=prod \
DB_URL=jdbc:postgresql://localhost:5432/library \
DB_USERNAME=library \
DB_PASSWORD=change-me \
JWT_SECRET=a-long-random-production-secret-at-least-32-characters \
LIBRARIAN_PASSWORD=Novak-Strong-Pass-2026 \
java -jar target/library-0.0.1-SNAPSHOT.jar
```

(The `\` at the end of a line means "the command goes on in the next line". You need a PostgreSQL database called `library` for this — see Chapter 77. In the next chapter, **Docker** will give us one with a single command! 🐳)

⚠️ That's a **lot** to type every time — and passwords in your terminal history aren't great either. On real servers, these values are set **once** in the server's settings, never typed by hand. Chapters 99 and 100 show how.

---

## 🏷️ Part 5: A real version number

`0.0.1-SNAPSHOT` sounds like "not finished". Our library is finished! 🎉 In **`pom.xml`**, change:

```xml
<version>1.0.0</version>
```

Rebuild → **`target/library-1.0.0.jar`**. 🏷️

Programmers often use **semantic versioning** — three numbers: **MAJOR.MINOR.PATCH**:

| Change | Example | When |
|---|---|---|
| PATCH | 1.0.0 → 1.0**.1** | A small bug fix 🐛 |
| MINOR | 1.0.1 → 1.**1**.0 | A new feature that doesn't break old clients (reservations! 📝) |
| MAJOR | 1.1.0 → **2**.0.0 | A big change that **breaks** old clients (renamed URLs...) 💥 |

---

## 💻 Mini project: A start script 📜

Typing the long `prod` command is annoying. Write a small script **`start-prod.sh`** (Git Bash, Mac, Linux) that:

1. Stops with an error if `DB_PASSWORD` or `JWT_SECRET` is not set.
2. Starts the jar with the `prod` profile and port **8080**.

<details>
<summary>Click to see the answer</summary>

**`start-prod.sh`**

```bash
#!/bin/bash
# Starts the library app in production mode.
# The secrets must be set in the environment BEFORE running this script.

if [ -z "$DB_PASSWORD" ] || [ -z "$JWT_SECRET" ]; then
  echo "Please set DB_PASSWORD and JWT_SECRET first!"
  exit 1
fi

java -jar target/library-1.0.0.jar \
  --spring.profiles.active=prod \
  --server.port=8080
```

| Code | Meaning |
|---|---|
| `#!/bin/bash` | "Run this file with bash." |
| `[ -z "$DB_PASSWORD" ]` | `-z` = "is it **empty**?" |
| `\|\|` | "or". |
| `exit 1` | Stop with an error (any number other than 0 means "something went wrong"). |
| `--spring.profiles.active=prod` | The profile as a command-line argument. |

Run it with `bash start-prod.sh`. Without the variables → `Please set DB_PASSWORD and JWT_SECRET first!` 🛑

(Notice: the script contains **no** secrets — it only **checks** that they're there. It can safely go into Git. 👍)

</details>

---

## ✋ Try it yourself

1. Build the jar with `./mvnw clean package -DskipTests`. How much faster is it? Why is that dangerous?
2. Start **two** copies of the jar at the same time — one on 8080, one on 8081. Do both work? Do they share the books?
3. Start the jar with `--spring.profiles.active=prod` but **without** any environment variables. Read the error.

<details>
<summary>Click to see the answers</summary>

1. Much faster — the tests are skipped. But then a broken app can be packed and shipped! 😱 Only use it when you **really** know the tests are green (for example, they already ran in a build server a minute ago).
2. Both start. And — with the H2 **file** database — they might fight over the same file: H2's file mode is meant for **one** app at a time, so the second one may fail with a "database may be already in use" error. That's one reason real servers use PostgreSQL! 🐘
3. The app stops at start with an error like *"Could not resolve placeholder 'DB_URL' in value "${DB_URL}""*. Good! No accidental start with missing secrets. 🛡️

</details>

---

## ⚠️ Common mistakes

### Mistake 1: "Port 8080 was already in use"

The app is still running in IntelliJ (or another terminal). Spring Boot says *"Web server failed to start. Port 8080 was already in use."* **Fix:** Stop the other one, or use `--server.port=8081`.

### Mistake 2: Running the wrong jar

`target/library-0.0.1-SNAPSHOT.jar.original` is the **thin** jar (only your code) — it can't start. **Fix:** Run the one **without** `.original`.

### Mistake 3: Old Java on the server

The jar was built for Java 25, the server has Java 17 → *"UnsupportedClassVersionError"*. **Fix:** The server needs the **same** (or a newer) Java version. (Docker solves this for good — next chapter!)

### Mistake 4: Secrets with defaults in `prod`

`library.jwt.secret=${JWT_SECRET:learning-only...}` in production → if someone forgets the variable, the app runs with the **learning** secret. 😱 **Fix:** No defaults for secrets in the `prod` profile.

### Mistake 5: Skipping tests "to be faster"

**Fix:** Let the tests run. They're your last guard before the real world. 🛡️

---

## ✅ Summary

- **`./mvnw clean package`** → tests → **`target/<name>-<version>.jar`**. A failing test → no jar. 🛡️
- Spring Boot makes a **fat jar** 🍔: your code + all libraries (`BOOT-INF/classes`, `BOOT-INF/lib`). The server only needs **Java**.
- Start: **`java -jar target/library-1.0.0.jar`**. Stop: **Ctrl+C** (graceful shutdown).
- Change settings **without rebuilding**: `--name=value` 🥇 > environment variables (`LIBRARY_LOAN_DAYS`) 🥈 > profile files 🥉 > `application.properties`.
- A **`prod`** profile with PostgreSQL and secrets **only** from the environment (no defaults!).
- Version numbers: **MAJOR.MINOR.PATCH**.

---

## ❓ Quiz

1. What is a fat jar, and why is it so big?
2. What does `./mvnw clean package` do, step by step?
3. Which command starts the jar?
4. How do you start the jar on port 9090 without changing any file?
5. What's the environment variable name for the setting `library.loan.max-active`?
6. Why do the secrets in `application-prod.properties` have no default values?
7. What does SNAPSHOT mean in a version?

<details>
<summary>Click to see the answers</summary>

1. A jar that contains your code and all the libraries it needs (Spring, Tomcat, Hibernate...). The libraries make it big.
2. Delete the old `target` folder, compile, run all tests, pack the classes into a jar, and repackage it as a fat jar.
3. `java -jar target/library-1.0.0.jar` (with your jar's name).
4. `java -jar target/library-1.0.0.jar --server.port=9090` (or the environment variable `SERVER_PORT=9090`).
5. `LIBRARY_LOAN_MAX_ACTIVE`.
6. So the app refuses to start when a secret is missing, instead of running with an unsafe learning value.
7. "Still being worked on" — not a finished version yet.

</details>

---

[⬅ Previous chapter](97-library-security-tests.md) | [Table of Contents](../README.md) | [Next chapter: Docker basics ➡](99-docker.md)
