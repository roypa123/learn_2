# Chapter 51 – Run your first Spring Boot app

[⬅ Previous chapter](50-project-tour.md) | [Table of Contents](../README.md) | [Next chapter ➡](52-hello-endpoint.md)

---

## 🎯 Goal

It's time to press **Run**! ▶️🎉

At the end of this chapter you will know:

- **Three ways** to run a Spring Boot app (IntelliJ, `mvnw`, `java -jar`)
- How to **read the console log**, line by line
- What the **"Whitelabel Error Page"** is (and why it's actually good news! 😄)
- How to **stop** and **restart** your app
- How to fix **"Port 8080 was already in use"** ⚠️
- How to change the **port**
- How to show your **own web page** at `http://localhost:8080/` 🏠
- How to make your **own banner** (the big logo) 🎨

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Run** | Start the program. ▶️ |
| **Console** | The window at the bottom of IntelliJ where your program writes text. |
| **Log** | Messages a program writes about **what it is doing**, like a diary. 📔 |
| **Log level** | How important a log message is: `ERROR` ❗, `WARN` ⚠️, `INFO` ℹ️, `DEBUG` 🐛. |
| **PID** | Process ID: the **number** your computer gives to a running program. |
| **Thread** | A "worker" inside your program. `main` is the first worker. 👷 |
| **Banner** | The big "Spring" logo printed at start. |
| **Whitelabel Error Page** | Spring Boot's simple, plain **error page** (a "white label" = no brand, no design). |
| **Port in use** | Another program is already listening at that port (door). 🚪 |
| **Restart** | Stop the app and start it again. 🔄 |

---

## 📖 Story: Opening a new shop 🏪

You built a new shop. Today is **opening day**!

1. You **unlock the door** and turn on the lights. 💡 (= **Run**)
2. You check your **list**: shelves ✅, cash register ✅, open sign ✅. (= the **log**)
3. You flip the sign to **"OPEN"**. 🪧 (= `Tomcat started on port 8080`)
4. The first customer comes in and asks: "Do you sell bicycles?" 🚲 You say: "Sorry, nothing here yet!" (= **404 Whitelabel Error Page** — the shop works, but the shelves are empty.)
5. In the evening, you **close** the shop. 🔒 (= **Stop**)

And one day, by mistake, you try to open a **second** shop at the **same address**. 😅 "Sorry, this address is already taken!" (= **Port 8080 was already in use**)

Let's open your shop! 🎉

---

## ▶️ Part 1: Run it in IntelliJ (way 1 — the easiest)

1. Open **`HelloApplication.java`**.
2. Look at the left side of the code, next to `public class HelloApplication` and `public static void main`. You see small green **▶** arrows.
3. Click the green **▶** next to `public static void main` → **Run 'HelloApplication.main()'**.

```
  6   @SpringBootApplication
▶ 7   public class HelloApplication {
  8
▶ 9       public static void main(String[] args) {
 10           SpringApplication.run(HelloApplication.class, args);
 11       }
```

> 💡 After the first run, IntelliJ remembers it. Next time, just click the green **▶** at the **top right** of IntelliJ, or press **Shift + F10**. 🚀

The **Run** window opens at the bottom, and text starts appearing. ⏳ After a few seconds, you see the Spring banner and some log lines. When you see this line, your app is **ready**:

```
... Started HelloApplication in 3.825 seconds (process running for 4.928)
```

🎉🎉🎉 **Congratulations! Your first Spring Boot app is running!** 🎉🎉🎉

Notice: the program **doesn't stop**. The red square ⏹️ (Stop button) is active. Your server is **waiting** for visitors, like the tiny server in Chapter 43. 🚪👂

---

## 📔 Part 2: Read the log, line by line

Here is the full output from a real run (we only shortened the long folder names with `...`):

```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

2026-10-10T22:08:29.588+05:30  INFO 11632 --- [hello] [           main] com.example.hello.HelloApplication       : Starting HelloApplication using Java 25 with PID 11632 (C:\...\hello\target\classes started by Sara in C:\...\hello)
2026-10-10T22:08:29.600+05:30  INFO 11632 --- [hello] [           main] com.example.hello.HelloApplication       : No active profile set, falling back to 1 default profile: "default"
2026-10-10T22:08:31.314+05:30  INFO 11632 --- [hello] [           main] o.s.boot.tomcat.TomcatWebServer          : Tomcat initialized with port 8080 (http)
2026-10-10T22:08:31.349+05:30  INFO 11632 --- [hello] [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2026-10-10T22:08:31.349+05:30  INFO 11632 --- [hello] [           main] o.apache.catalina.core.StandardEngine    : Starting Servlet engine: [Apache Tomcat/11.0.24]
2026-10-10T22:08:31.396+05:30  INFO 11632 --- [hello] [           main] b.w.c.s.WebApplicationContextInitializer : Root WebApplicationContext: initialization completed in 1635 ms
2026-10-10T22:08:32.149+05:30  INFO 11632 --- [hello] [           main] o.s.boot.tomcat.TomcatWebServer          : Tomcat started on port 8080 (http) with context path '/'
2026-10-10T22:08:32.174+05:30  INFO 11632 --- [hello] [           main] com.example.hello.HelloApplication       : Started HelloApplication in 3.825 seconds (process running for 4.928)
```

Wow, long lines! 😵 Don't worry. **Every** log line has the **same 7 parts**. Let's take one line apart:

```
2026-10-10T22:08:32.149+05:30  INFO 11632 --- [hello] [           main] o.s.boot.tomcat.TomcatWebServer          : Tomcat started on port 8080 (http) with context path '/'
└──────────── 1 ────────────┘ └─2─┘ └─3─┘    └──4──┘ └───────5────────┘ └────────────────6─────────────────┘   └──────────────────────────7──────────────────────────┘
```

| # | Part | Example | Meaning |
|---|---|---|---|
| 1 | **Date and time** | `2026-10-10T22:08:32.149+05:30` | **When** it happened: date, `T`, time with milliseconds, and the time zone (Chapter 39). |
| 2 | **Level** | `INFO` | **How important**: `ERROR` ❗ > `WARN` ⚠️ > `INFO` ℹ️ > `DEBUG` 🐛. INFO = "just telling you". |
| 3 | **PID** | `11632` | The process number of your app (every run gets a new one). |
| 4 | **App name** | `[hello]` | From `spring.application.name=hello` in `application.properties` (Chapter 50)! |
| 5 | **Thread** | `[main]` | Which "worker" wrote it. `main` = the starting worker. |
| 6 | **Logger** | `o.s.boot.tomcat.TomcatWebServer` | **Which class** wrote it. Long names are shortened: `o.s` = `org.springframework`. |
| 7 | **Message** | `Tomcat started on port 8080...` | ⭐ **What happened.** Usually, you read only this part! |

> 💡 **Tip:** Your eyes can skip parts 1–6 and read only the **message** at the end. Experienced developers do that! 😎 (Unless something goes wrong — then the **level** helps: look for `WARN` and `ERROR`.)

### 🔍 The messages, one by one

| Message | Meaning | Chapter 48 step |
|---|---|---|
| The banner + `:: Spring Boot :: (v4.1.1)` | "Hello! I'm Spring Boot version 4.1.1." | Step 2 |
| `Starting HelloApplication using Java 25 with PID 11632 (...)` | "I'm starting your app with Java 25. My classes are in `target\classes`. Sara started me." | Step 1 |
| `No active profile set, falling back to 1 default profile: "default"` | "You didn't choose a **profile** (like 'dev' or 'prod'), so I use 'default'." We'll learn profiles in **Chapter 56**. | Step 3 |
| `Tomcat initialized with port 8080 (http)` | "I prepared the Tomcat web server for port 8080." 🐱 | Step 5 |
| `Starting service [Tomcat]` | "Tomcat is starting..." | |
| `Starting Servlet engine: [Apache Tomcat/11.0.24]` | "I'm using **Tomcat version 11.0.24**." | |
| `Root WebApplicationContext: initialization completed in 1635 ms` | "The Spring **container** (the toy box 🧸 of beans) is ready. It took 1.6 seconds." | Step 6 |
| `Tomcat started on port 8080 (http) with context path '/'` | ⭐ "**The door is open!** 🚪 I'm listening at port 8080. The context path is `/` — your URLs start right after the port." | Step 8 |
| `Started HelloApplication in 3.825 seconds (process running for 4.928)` | ⭐ "**Everything is ready!** Spring took 3.8 seconds. The whole Java program has been running for 4.9 seconds." | Step 9 |

Your numbers (times, PID, versions) will be **different**. That's normal. 😊

---

## 🌐 Part 3: Visit your app — the Whitelabel Error Page

Your server is running. Let's visit it! Open your browser and go to:

```
http://localhost:8080
```

You'll see:

```
┌─────────────────────────────────────────────────────────────────┐
│ Whitelabel Error Page                                            │
│                                                                  │
│ This application has no explicit mapping for /error, so you are │
│ seeing this as a fallback.                                       │
│                                                                  │
│ Sat Oct 10 22:08:33 IST 2026                                     │
│ There was an unexpected error (type=Not Found, status=404).      │
└─────────────────────────────────────────────────────────────────┘
```

"Error"?! 😱 Did we do something wrong?

**No! This is good news!** 🎉 Look at it carefully:

| Line | Meaning |
|---|---|
| **Whitelabel Error Page** | Spring Boot's plain, simple error page. ("White label" = a product with **no brand** on it.) |
| `This application has no explicit mapping for /error...` | "You haven't made your **own** error page, so I'm showing my simple one." (Totally fine.) |
| `Sat Oct 10 22:08:33 IST 2026` | When the error happened. |
| `type=Not Found, status=404` | ⭐ **404 Not Found** (Chapter 44). "I don't have anything at this address." |

Remember the shop story: the customer asks for bicycles, and you say "Sorry, nothing here yet!" 🚲❌ That means:

- ✅ The server is **running** (otherwise the browser would say "This site can't be reached").
- ✅ Tomcat **received** your request.
- ✅ Spring **answered** with a proper HTTP status code.
- ❌ We just haven't built any **pages** or **endpoints** yet. That's the **next chapter**! 😉

### 🔍 The same thing with curl

The browser asks for **HTML**, so Spring answers with an HTML page. curl doesn't ask for HTML, so Spring answers with **JSON**! 🤯 Try it (Git Bash, or `curl.exe` in PowerShell — Chapter 47):

```
curl -i http://localhost:8080
```

```
HTTP/1.1 404 
Content-Type: application/json
Transfer-Encoding: chunked
Date: Sat, 10 Oct 2026 16:38:33 GMT

{"timestamp":"2026-10-10T16:38:33.449Z","status":404,"error":"Not Found","path":"/"}
```

| Part | Meaning |
|---|---|
| `HTTP/1.1 404` | Status code **404** (Chapter 44). |
| `Content-Type: application/json` | "The body is **JSON**." (Chapter 45) |
| `"timestamp"` | When it happened (in UTC — that's why the hour is different from the log). |
| `"status":404` | The status code again, inside the JSON. |
| `"error":"Not Found"` | The name of the status. |
| `"path":"/"` | Which path you asked for. |

**Same error, two formats** — Spring Boot looks at **who** is asking (the `Accept` header — Chapter 44) and answers in the best format. 🧠 Smart, right?

---

## ⏹️ Part 4: Stop and restart

### Stop

- In IntelliJ: click the red **square ⏹️** (in the Run window or at the top right). Or press **Ctrl + F2**.
- In a terminal: press **Ctrl + C**.

You'll see a few last lines (like "Commencing graceful shutdown..."), and then:

```
Process finished with exit code ...
```

Now visit `http://localhost:8080` again. The browser says: **"This site can't be reached"** / **"localhost refused to connect"**. 🚫 The shop is closed. 🔒

### Restart 🔄

**Very important:** when you **change your code**, the running app does **not** change by itself! ☝️ You must **restart** it.

- In IntelliJ: click **Rerun** 🔄 (the circle arrow in the Run window) or press **Ctrl + F5**.
- If you click ▶ while the app is running, IntelliJ asks:

```
┌────────────────────────────────────────────────┐
│  Process 'HelloApplication' Is Running          │
│                                                 │
│        [ Stop and Rerun ]     [ Cancel ]        │
└────────────────────────────────────────────────┘
```

👉 Choose **Stop and Rerun**. ✅

**Rule:** 📏 **Change code → Restart → Test.** Every time. (Many "it doesn't work!" moments are really "I forgot to restart!" 😅)

---

## 🚪 Part 5: "Port 8080 was already in use" ⚠️

Sooner or later, you **will** see this. Everybody does! 😄 It happens when you start the app **twice**. (For example: it's already running in IntelliJ, and you start it again from a terminal.) We tried it for real. The second copy printed:

```
***************************
APPLICATION FAILED TO START
***************************

Description:

Web server failed to start. Port 8080 was already in use.

Action:

Identify and stop the process that's listening on port 8080 or configure this application to listen on another port.
```

Spring Boot errors have a **friendly format**: 💌

| Part | Meaning |
|---|---|
| `APPLICATION FAILED TO START` | "I could not start." ❌ |
| **Description:** | **What** went wrong: "Port 8080 is already taken." |
| **Action:** | **How to fix it**: "Stop the other program, or use another port." ✅ |

Always read the **Description** and **Action** parts first! They're written for **humans**. 😊

Remember Chapter 43: **only one program can listen at one port** (one shop per address 🏪). The first app is still using port 8080.

### ✅ Fix 1: Stop the other one

Look at IntelliJ's **Run** window — maybe there are **two tabs** (`HelloApplication` twice). Stop the old one (⏹️). Or close the terminal where it's running.

### ✅ Fix 2: Find and stop the program (if you can't find it)

Sometimes the old app keeps running in the background. Find it by its port:

**Windows (Command Prompt or PowerShell):**

```
netstat -ano | findstr :8080
```

```
  TCP    0.0.0.0:8080     0.0.0.0:0     LISTENING     11632
```

The last number (`11632`) is the **PID**. Stop it:

```
taskkill /PID 11632 /F
```

**Mac / Linux:**

```
lsof -i :8080
kill 11632
```

(Use the PID **you** see, not `11632`.)

### ✅ Fix 3: Use another port

Open `src/main/resources/application.properties` and add a line:

```properties
spring.application.name=hello
server.port=8081
```

| Code | Meaning |
|---|---|
| `server.port` | The setting for Tomcat's port. |
| `=8081` | "Use door number 8081 instead." 🚪 |

Restart. The log now says:

```
Tomcat started on port 8081 (http) with context path '/'
```

and your app is at `http://localhost:8081`. ✅ (This was your **first Spring Boot setting**! 🎛️ Much more in Chapter 55.)

> 💡 For the rest of this book, we use **8080**. If you changed it, change it back (delete the `server.port` line), or remember to use your own number.

---

## ⌨️ Part 6: Run it with the Maven Wrapper (way 2)

You can also run the app **without** IntelliJ's ▶ button. Open a terminal **in the project folder** (in IntelliJ: the **Terminal** tab, **Alt + F12**) and type:

| Terminal | Command |
|---|---|
| Windows Command Prompt | `mvnw spring-boot:run` |
| Windows PowerShell | `.\mvnw spring-boot:run` |
| Git Bash, Mac, Linux | `./mvnw spring-boot:run` |

| Part | Meaning |
|---|---|
| `mvnw` | The Maven Wrapper (Chapter 40). |
| `spring-boot:run` | Use the **spring-boot** plugin (from `pom.xml`, Chapter 49) and its **run** goal: "compile and start the app". |

First, Maven prints its own lines (compiling...), then your app starts:

```
[INFO] --- compiler:3.15.0:compile (default-compile) @ hello ---
[INFO] Compiling 1 source file with javac [debug parameters release 25] to target\classes
...
[INFO] --- spring-boot:4.1.1:run (default-cli) @ hello ---
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
...
... Started HelloApplication in 3.6 seconds (process running for 4.5)
```

**Stop:** press **Ctrl + C** in the terminal. (If Windows asks `Terminate batch job (Y/N)?`, type `Y` and Enter.)

---

## 📦 Part 7: Run the jar (way 3 — like a real server)

This is how apps run on **real servers** on the internet. 🌍 First, **build** the jar:

```
mvnw package
```

(PowerShell: `.\mvnw package`. Git Bash/Mac/Linux: `./mvnw package`.)

Maven compiles, **runs the tests** (Chapter 50 — they must be green!), and makes the jar:

```
[INFO] Building jar: C:\...\hello\target\hello-0.0.1-SNAPSHOT.jar
...
[INFO] BUILD SUCCESS
```

Now run the jar with **plain Java**:

```
java -jar target/hello-0.0.1-SNAPSHOT.jar
```

| Part | Meaning |
|---|---|
| `java` | Start Java (Chapter 3). |
| `-jar` | "Run the program inside this **jar** file." |
| `target/hello-0.0.1-SNAPSHOT.jar` | The jar Maven just made (artifactId + version — Chapter 41). |

Your app starts — with **no IntelliJ** and **no Maven**! Just Java. 🎉 This one file (about **20 MB**) has your code **plus** Spring, Tomcat, Jackson... everything. (More in Chapter 98.)

**Stop:** **Ctrl + C**.

### 🆚 Which way should I use?

| Way | When |
|---|---|
| ▶️ IntelliJ | ✅ **Every day** while learning and coding. Easiest. Has the debugger (Chapter 17). |
| `mvnw spring-boot:run` | When you don't have IntelliJ open, or on another computer. |
| `java -jar` | On a **real server**, or to test the "finished product". |

---

## 🎨 Part 8: Make your own banner (just for fun!)

Don't like the Spring logo? Make your own! 😄

1. Right-click **`src/main/resources`** → **New → File** → name it **`banner.txt`**.
2. Type (or paste) this:

```
  _   _      _ _       _
 | | | | ___| | | ___ | |
 | |_| |/ _ \ | |/ _ \| |
 |  _  |  __/ | | (_) |_|
 |_| |_|\___|_|_|\___/(_)

 My first app - Spring Boot ${spring-boot.version}
```

3. Restart. The console now shows **your** banner:

```
  _   _      _ _       _
 | | | | ___| | | ___ | |
 | |_| |/ _ \ | |/ _ \| |
 |  _  |  __/ | | (_) |_|
 |_| |_|\___|_|_|\___/(_)

 My first app - Spring Boot 4.1.1
```

| Code | Meaning |
|---|---|
| `banner.txt` | If this file exists in `resources`, Spring Boot prints it **instead** of the Spring logo. |
| `${spring-boot.version}` | A **placeholder**: Spring Boot puts the real version number here. (`${...}` placeholders come back in Chapter 55!) |

> 💡 Search the internet for "**ASCII art text generator**" to make big letters from any word. 🔤

**Don't want any banner?** Add this to `application.properties`:

```properties
spring.main.banner-mode=off
```

---

## ⚡ Part 9: Faster restarts with DevTools (optional)

Restarting by hand gets boring. 😴 Spring Boot has a helper called **DevTools** that restarts your app **automatically** (and faster!) when your code changes.

Add this to `pom.xml` inside `<dependencies>`, then click **Maven reload** 🔄:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-devtools</artifactId>
    <scope>runtime</scope>
    <optional>true</optional>
</dependency>
```

| Code | Meaning |
|---|---|
| `spring-boot-devtools` | The DevTools library. |
| `<scope>runtime</scope>` | Only needed when running, not for compiling (Chapter 41). |
| `<optional>true</optional>` | "Don't pass this on to others who use my project." DevTools is **never** used on real servers. |

In IntelliJ: after changing code, press **Build → Build Project** (**Ctrl + F9**). DevTools notices the new classes and restarts the app in about a second. ⚡

> 💡 This is **optional**. In this book, we simply say "restart". If you use DevTools, "restart" means "build". Both work! 😊

---

## 💻 Mini project: Your shop's front window 🪟🏠

Let's replace the 404 Whitelabel page with your **own** home page — **without any Java code**!

1. Right-click **`src/main/resources/static`** → **New → File** → name it **`index.html`**.
2. Type this:

```html
<!DOCTYPE html>
<html>
<body>
  <h1>Welcome to my first Spring Boot app!</h1>
  <p>Try <a href="/hello">/hello</a></p>
</body>
</html>
```

3. Restart the app.
4. Open `http://localhost:8080` in your browser.

You see:

```
Welcome to my first Spring Boot app!
Try /hello
```

🎉 Your first page on your own server!

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `<!DOCTYPE html>` | "This is an HTML page." |
| `<html>` ... `</html>` | The start and end of the page. |
| `<body>` ... `</body>` | The visible part of the page. |
| `<h1>Welcome ...</h1>` | A big **heading** (h1 = heading level 1). |
| `<p>Try ... </p>` | A **paragraph** of normal text. |
| `<a href="/hello">/hello</a>` | A **link**. Click it → the browser goes to `/hello`. |

### 🤔 Why does it work?

Spring Boot has a rule: if somebody asks for `/` and there's a file **`static/index.html`**, send it! It's the **home page** of your website. 🏠 Let's check with curl:

```
curl -i http://localhost:8080/
```

```
HTTP/1.1 200 
Content-Type: text/html;charset=UTF-8
Content-Length: 135

<!DOCTYPE html>
<html>
<body>
  <h1>Welcome to my first Spring Boot app!</h1>
  <p>Try <a href="/hello">/hello</a></p>
</body>
</html>
```

(We left out a few less important headers, like `Date` and `Last-Modified`.)

**200 OK** ✅ and `Content-Type: text/html` — "this is a web page".

Now **click the `/hello` link**. What do you see? 🤔 The Whitelabel page with **404**! Because `/hello` doesn't exist... **yet**. In the **next chapter**, you'll write your first **Java endpoint** for `/hello`. 🚀

---

## ✋ Try it yourself

**Task 1:** Change your app's port to **9090**. Restart. What's the new address of your home page? Then change it back to 8080.

<details>
<summary>Click to see the answer</summary>

Add `server.port=9090` to `application.properties` and restart. The log says `Tomcat started on port 9090`, and the address is `http://localhost:9090`. To change back, delete the line (or set it to 8080) and restart.

</details>

**Task 2:** Put a picture (any `.png` or `.jpg` file, for example `cat.png`) into `src/main/resources/static`. Restart. How do you see it in the browser? Then add it to `index.html`.

<details>
<summary>Click to see the answer</summary>

Go to `http://localhost:8080/cat.png`. To show it on the home page, add this line inside `<body>`:

```html
<img src="/cat.png" width="300">
```

(`img` = image, `src` = where the picture is, `width` = how wide.)

</details>

**Task 3:** Start the app in IntelliJ. While it's running, open a terminal and run `mvnw spring-boot:run` (or `.\mvnw spring-boot:run`). What happens? Read the **Description** and **Action**.

<details>
<summary>Click to see the answer</summary>

The second app fails with `Web server failed to start. Port 8080 was already in use.` The Action says to stop the other process or choose another port. Only **one** program can listen at port 8080! 🚪

</details>

**Task 4:** Look at the log line with `Started HelloApplication in ... seconds`. Run the app three times. Is the time always the same?

<details>
<summary>Click to see the answer</summary>

No, it changes a little every time (for example 3.8, 3.4, 3.6 seconds). The speed depends on what else your computer is doing at that moment. 😊

</details>

---

## ⚠️ Common mistakes

### Mistake 1: The app "does nothing" / "is stuck"

After `Started HelloApplication...`, nothing more happens and the program doesn't end. Beginners think it's frozen! 🥶 It's **not**. A server **waits** for requests. That's its job. 🚪👂 **Fix:** Nothing to fix! Open the browser and visit it.

### Mistake 2: Thinking the Whitelabel page is a real error

**404 Whitelabel** at `http://localhost:8080` = "the server works, there's just nothing at this address." ✅ **Fix:** Nothing — or add `static/index.html`, or (next chapter) an endpoint.

### Mistake 3: "This site can't be reached"

The browser can't connect at all. The app is **not running** (you stopped it, or it failed to start), **or** you're using the wrong port. **Fix:** Look at the Run window. Is it running? What port does the log say? 👀

### Mistake 4: Forgetting to restart after a change

You changed code or `application.properties`, but the browser shows the old result. **Fix:** Restart! 🔄 (Or use DevTools + Build.)

### Mistake 5: Port 8080 already in use

**Fix:** Stop the other copy (look for a **second tab** in IntelliJ's Run window!), or use `netstat`/`taskkill`, or change `server.port`. (Part 5.)

### Mistake 6: The app starts and then stops immediately

The log shows `Started HelloApplication...` and then `Process finished with exit code 0`. No Tomcat lines at all! 😮 **Reason:** The **Spring Web** dependency is missing. Without it, there's no web server, so there's nothing to wait for. **Fix:** Add `spring-boot-starter-webmvc` to `pom.xml` (Chapter 49, Mistake 3) and reload Maven.

### Mistake 7: Reading the wrong part of a long error

When an app fails, there may be **100 lines** of red text. 😱 **Fix:** Scroll up and find the box:

```
***************************
APPLICATION FAILED TO START
***************************
```

Read **Description** and **Action**. If there's no box, look for the **first** line that says `ERROR`, and lines that start with `Caused by:` — the **last** `Caused by:` is often the real reason. 🔍

---

## ✅ Summary

- Run your app in IntelliJ with the green **▶** next to `main` (later: **Shift + F10**).
- When you see **`Started HelloApplication in ... seconds`**, the app is ready. A server keeps **running and waiting**.
- Every log line has: **time**, **level**, **PID**, **[app name]**, **[thread]**, **logger**, **message**. Usually, read just the **message**.
- **Whitelabel Error Page (404)** = the server works, but nothing is at that address yet. With curl, the same error comes as **JSON**.
- **Stop:** red square ⏹️ or **Ctrl + C**. **Change code → restart → test.**
- **"Port 8080 was already in use"** → stop the other copy, or set `server.port=8081`.
- Three ways to run: **IntelliJ** ▶️, **`mvnw spring-boot:run`**, **`java -jar target/...jar`**.
- `static/index.html` becomes your **home page** 🏠. `banner.txt` changes the banner 🎨.
- Spring Boot error boxes have **Description** + **Action** — read them first!

---

## ❓ Quiz

1. Which log message tells you the app is completely ready?
2. What are the 7 parts of a log line? Which one do you usually read?
3. You visit `http://localhost:8080` and see a Whitelabel Error Page with status 404. Is your app broken?
4. Why does curl get JSON, but the browser gets an HTML page, for the same 404?
5. You changed your code, but the browser shows the old answer. What did you forget?
6. What does `Port 8080 was already in use` mean? Give two fixes.
7. Which setting changes the port?
8. What is the command to run the app with the Maven Wrapper in Git Bash?
9. Where must `index.html` be, so it's shown at `http://localhost:8080/`?
10. In a Spring Boot error box, which two parts should you read first?

<details>
<summary>Click to see the answers</summary>

1. `Started HelloApplication in ... seconds`
2. Time, level, PID, app name, thread, logger, message. Usually you read the **message**.
3. No! The server works. There's just nothing at that address yet.
4. Spring Boot looks at what the client asks for (the `Accept` header). The browser asks for HTML; curl doesn't, so it gets JSON.
5. To restart the app.
6. Another program (often a second copy of your app) is already listening at port 8080. Fixes: stop the other program, or change the port with `server.port`.
7. `server.port` (in `application.properties`).
8. `./mvnw spring-boot:run`
9. In `src/main/resources/static/index.html`.
10. **Description** (what's wrong) and **Action** (how to fix it).

</details>

---

[⬅ Previous chapter](50-project-tour.md) | [Table of Contents](../README.md) | [Next chapter: Your first web page answer: Hello endpoint ➡](52-hello-endpoint.md)
