# Chapter 55 – Settings: application.properties

[⬅ Previous chapter](54-beans.md) | [Table of Contents](../README.md) | [Next chapter ➡](56-profiles.md)

---

## 🎯 Goal

Your app has **values** inside the code: the port, a greeting text, opening hours... What if you want to **change** them **without** changing the code? 🤔 That's what **settings** are for! 🎛️

At the end of this chapter you will know:

- How the **`application.properties`** file works (the rules)
- Useful **Spring Boot settings**: port, banner, context path, logging...
- How to make **your own** settings and read them with **`@Value`**
- **Default values** (when a setting is missing)
- A cleaner way for groups of settings: **`@ConfigurationProperties`** with a **record** ✨
- The **YAML** format (`application.yml`) — another way to write settings
- How to **change settings from outside**: command line and **environment variables** 🌍
- Why **passwords** must **never** be in this file 🔒

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Setting / property** | A named value that controls your app: `server.port=8080`. |
| **Key** | The **name** of a setting: `server.port`. |
| **Value** | What the setting **is**: `8080`. |
| **Hard-coded** | A value written **directly in the Java code**. Hard to change! 🧱 |
| **Placeholder** | `${...}` — "put the value of this setting **here**". |
| **Default value** | The value to use if the setting is **missing**. |
| **`@Value`** | A label that **reads one setting** into a variable. |
| **`@ConfigurationProperties`** | A label that **reads a whole group** of settings into one object. |
| **YAML** | Another file format for settings (`.yml`), using **indentation** instead of dots. |
| **Environment variable** | A setting given by the **computer system** to a program (outside the code). |
| **Externalized configuration** | A fancy name for "settings live **outside** the code". |

---

## 📖 Story: The settings menu of a game 🎮

Every video game has a **Settings** menu: 🔊 volume, 🌐 language, 🎨 colors, 🏃 difficulty.

- The game **makers** didn't build a different game for each volume level. They wrote **one** game that **reads** the settings.
- You change the language → the game shows another language. No new game needed!
- Some settings come from **outside**: your phone's language setting may set the game's language automatically. 📱

Your Spring Boot app is the same:

| Game | Spring Boot |
|---|---|
| The Settings menu | `application.properties` 🎛️ |
| "Volume = 7" | `server.port=8080` |
| The game reads the settings | Spring reads the file at startup |
| Phone settings override the game | **Command line** and **environment variables** override the file 🌍 |

---

## 📄 Part 1: The file and its rules

The file is **`src/main/resources/application.properties`** (Chapter 50). Right now it has:

```properties
spring.application.name=hello
```

### The rules 📏

```properties
# This is a comment. Spring ignores it.
server.port=8080
app.shop.name=Sara's Bakery
app.shop.products=Bread,Cake,Cookies
```

| Rule | Example | Meaning |
|---|---|---|
| One setting per line | `server.port=8080` | **key** `=` **value** |
| `#` starts a comment | `# This is a comment` | For humans, like `//` in Java. |
| Dots make **groups** | `app.shop.name`, `app.shop.products` | Like folders: `app` → `shop` → `name`. 📁 |
| No quotes needed | `app.shop.name=Sara's Bakery` | Everything after `=` is the value — spaces and `'` included. |
| Lists with commas | `Bread,Cake,Cookies` | Spring can turn this into a `List` (Part 5). |
| Words in keys with `-` | `app.shop.open-hour=8` | Spring's style: small letters and `-` ("kebab-case" 🍢). |

> ⚠️ **Careful with spaces at the end!** `app.greeting=Hello   ` keeps the spaces after "Hello". They're invisible, so they're hard to find. 👻

---

## 🎛️ Part 2: Spring Boot's own settings

Spring Boot has **more than a thousand** settings! You'll only need a few. Here are useful ones:

| Setting | Example | What it does |
|---|---|---|
| `spring.application.name` | `hello` | The app's name (shown in the log as `[hello]` — Chapter 51). |
| `server.port` | `8081` | The port (Chapter 51). |
| `spring.main.banner-mode` | `off` | Turn off the banner (Chapter 51). |
| `server.servlet.context-path` | `/api` | A **start** for **all** URLs of the app. |
| `logging.level.root` | `WARN` | Show fewer log messages (only WARN and ERROR). |
| `logging.level.com.example.hello` | `DEBUG` | Show **more** messages (DEBUG too), but only from **your** package. |

### Example: context path

```properties
server.servlet.context-path=/api
```

The log now says:

```
Tomcat started on port 8080 (http) with context path '/api'
```

And **every** URL gets `/api` in front: `/hello` is now **`/api/hello`**! The old `/hello` gives **404**. (We tested it. Remove this line again after trying it — we don't use it in this book. 😉)

### Example: more log messages

```properties
logging.level.com.example.hello=DEBUG
```

Now you also see **DEBUG** messages from your package, like:

```
... DEBUG 17256 --- [hello] [main] com.example.hello.HelloApplication : Running with Spring Boot v4.1.1, Spring v7.0.9
```

(More about logging in Chapter 88. 📔)

> 💡 **Where's the full list?** Search for "**Spring Boot Common Application Properties**" — it's in the official documentation at **docs.spring.io**. IntelliJ **Ultimate** and VS Code (with the Spring Boot extension) also **suggest** setting names while you type. 🪄

---

## 🧱 Part 3: The problem with hard-coded values

Look at this controller:

```java
@GetMapping("/greeting")
public String greeting() {
    return "Hello from Sara's Bakery!";      // 🧱 hard-coded
}
```

The text is **hard-coded**. To change it, you must:

1. change the **Java code**,
2. **compile** it again,
3. make a **new jar** (Chapter 51),
4. put it on the server again.

😩 Just for a different text! And maybe the bakery in **another city** needs a **different** text, but the **same** program...

**Better:** put the text in **settings**, and let the code **read** it. 🎛️

---

## 🏷️ Part 4: Your own settings + `@Value`

### Step 1: Add your settings

Open `application.properties` and add your own settings. Start your own keys with **`app.`** — then they never clash with Spring's names:

```properties
spring.application.name=hello

# My own settings
app.greeting=Hello from the settings file
app.shop.name=Sara's Bakery
app.shop.open-hour=8
app.shop.close-hour=18
app.shop.products=Bread,Cake,Cookies
```

### Step 2: Read them with `@Value`

Create **`SettingsController`**:

```java
package com.example.hello;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SettingsController {

    private final String greeting;
    private final String welcome;
    private final int openHour;
    private final String appName;

    public SettingsController(@Value("${app.greeting}") String greeting,
                              @Value("${app.welcome:Welcome, friend!}") String welcome,
                              @Value("${app.shop.open-hour}") int openHour,
                              @Value("${spring.application.name}") String appName) {
        this.greeting = greeting;
        this.welcome = welcome;
        this.openHour = openHour;
        this.appName = appName;
    }

    @GetMapping("/settings")
    public String settings() {
        return greeting + " | " + welcome + " | opens at " + openHour
                + " (next hour: " + (openHour + 1) + ") | app: " + appName;
    }
}
```

Restart → `http://localhost:8080/settings`:

```
Hello from the settings file | Welcome, friend! | opens at 8 (next hour: 9) | app: hello
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `import org.springframework.beans.factory.annotation.Value;` | We use the `@Value` label. |
| `@Value("${app.greeting}") String greeting` | ⭐ "Spring, for this constructor parameter, give me the **value of the setting** `app.greeting`." |
| `${...}` | A **placeholder**: "the value of this setting". (You saw `${spring-boot.version}` in the banner — Chapter 51!) |
| `@Value("${app.welcome:Welcome, friend!}")` | ⭐ A **default value**: `app.welcome` is **not** in the file, so Spring uses the text after the **`:`** → `Welcome, friend!` |
| `@Value("${app.shop.open-hour}") int openHour` | The setting is **text** (`"8"`), but the parameter is an **`int`**. Spring **converts** it to the number `8` for you! 🔢 |
| `(openHour + 1)` | Proof that it's a real number: `8 + 1 = 9` (not the text `"81"` — Chapter 9!). |
| `@Value("${spring.application.name}")` | You can read **Spring's** settings too. |

> 💡 It's **constructor injection** again (Chapter 53)! But instead of a **bean**, Spring injects a **setting value**. 💉🎛️

### Step 3: Change the setting — not the code!

Change the file:

```properties
app.greeting=Good morning from the bakery!
```

Restart → `/settings`:

```
Good morning from the bakery! | Welcome, friend! | opens at 8 (next hour: 9) | app: hello
```

You changed the app's behavior **without touching Java**. 🎉

---

## 📦 Part 5: Groups of settings — `@ConfigurationProperties` ✨

`@Value` is great for **one or two** settings. But for a **group** — like all the `app.shop.*` settings — there's a cleaner way: put them **all** into **one record**!

### Step 1: The record

**`ShopProperties.java`**

```java
package com.example.hello;

import java.util.List;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "app.shop")
public record ShopProperties(String name, int openHour, int closeHour, List<String> products) {
}
```

| Code | Meaning |
|---|---|
| `@ConfigurationProperties(prefix = "app.shop")` | ⭐ "Fill this record with **all settings that start with `app.shop.`**." |
| `String name` | ← `app.shop.name` = `Sara's Bakery` |
| `int openHour` | ← `app.shop.open-hour` = `8`. Spring matches `open-hour` to `openHour` automatically! (This is called **relaxed binding** 🧘.) |
| `int closeHour` | ← `app.shop.close-hour` = `18` |
| `List<String> products` | ← `app.shop.products` = `Bread,Cake,Cookies` → split at the commas → a **list**! 📋 |

### Step 2: Turn it on

Spring doesn't look for `@ConfigurationProperties` records by itself. Add **one** label to your main class:

```java
package com.example.hello;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

@SpringBootApplication
@ConfigurationPropertiesScan
public class HelloApplication {

    public static void main(String[] args) {
        SpringApplication.run(HelloApplication.class, args);
    }
}
```

| Code | Meaning |
|---|---|
| `@ConfigurationPropertiesScan` | "Spring, also **search** for classes with `@ConfigurationProperties`, and make **beans** of them, filled with the settings." 🔍 (Like `@ComponentScan`, but for settings.) |

### Step 3: Inject the record like any bean

**`ShopController.java`**

```java
package com.example.hello;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ShopController {

    private final ShopProperties shop;

    public ShopController(ShopProperties shop) {
        this.shop = shop;
    }

    @GetMapping("/shop")
    public ShopProperties shop() {
        return shop;
    }

    @GetMapping("/shop/hours")
    public String hours() {
        int hours = shop.closeHour() - shop.openHour();
        return shop.name() + " is open " + hours + " hours a day.";
    }
}
```

Restart. Real answers:

`GET /shop`

```json
{"name":"Sara's Bakery","openHour":8,"closeHour":18,"products":["Bread","Cake","Cookies"]}
```

`GET /shop/hours`

```
Sara's Bakery is open 10 hours a day.
```

### 🔍 What's happening

| Code | Meaning |
|---|---|
| `public ShopController(ShopProperties shop)` | 💉 Inject the settings record. It's a **bean** now! |
| `return shop;` | Return the record → **JSON** (Chapter 52). A quick way to **see** all your settings. 👀 |
| `shop.closeHour() - shop.openHour()` | `18 - 8 = 10`. Real `int`s. Record accessor methods (Chapter 29). |

### 🆚 `@Value` or `@ConfigurationProperties`?

| | `@Value` | `@ConfigurationProperties` ✨ |
|---|---|---|
| Best for | **1–2** single settings | A **group** of settings |
| Typing mistakes in the key | Found at **start** (error) | Missing ones just stay empty/`0` — be careful! |
| Lists, nested groups | Hard | Easy 📋 |
| Clean code | OK | ✅ Very clean: one object, all settings |

> 💡 **Rule:** Many settings that belong together → `@ConfigurationProperties` record. Just one → `@Value`.

---

## 📐 Part 6: YAML — another way to write settings

Instead of `application.properties`, you can use **`application.yml`** (YAML = "**Y**AML **A**in't **M**arkup **L**anguage" 🙃). Same settings, different style:

**`application.properties`**

```properties
spring.application.name=hello

# My own settings
app.greeting=Hello from the settings file
app.shop.name=Sara's Bakery
app.shop.open-hour=8
app.shop.close-hour=18
app.shop.products=Bread,Cake,Cookies
```

**`application.yml`** (the same!)

```yaml
spring:
  application:
    name: hello

# My own settings
app:
  greeting: Hello from the settings file
  shop:
    name: Sara's Bakery
    open-hour: 8
    close-hour: 18
    products:
      - Bread
      - Cake
      - Cookies
```

### The YAML rules 📏

| Rule | Example |
|---|---|
| **Indentation** (spaces!) makes groups, instead of dots | `app:` → `  shop:` → `    name:` |
| Use **spaces**, **never tabs** | 2 spaces per level is normal |
| `key: value` — a **space after** the colon! | `name: hello` ✅ `name:hello` ❌ |
| Lists with `- ` | `- Bread` |
| `#` for comments | same as properties |

We tested it: the YAML file gives **exactly** the same results for `/settings` and `/shop`. ✅

### Which one should I use?

Both work equally well. Many companies use YAML (less repeating), many use properties (simpler rules). **This book uses `.properties`**.

> ⚠️ **Use only ONE of them.** If you have **both** files, Spring reads **both**, and for the same key, **`.properties` wins**. We had this happen by accident while testing: we changed the YAML file, but the old `.properties` file was still there... and our change "didn't work"! 😵 Very confusing. Pick one.

---

## 🌍 Part 7: Change settings from outside

Here's the coolest part. 😎 You can **override** (replace) any setting **when you start the app** — without changing **any** file!

### Way 1: Command-line arguments

```
java -jar target/hello-0.0.1-SNAPSHOT.jar --server.port=9090 --app.greeting=Hi-from-command-line
```

| Part | Meaning |
|---|---|
| `--server.port=9090` | Two minus signs + `key=value`. "For this run, the port is 9090." |
| `--app.greeting=Hi-from-command-line` | Your own settings work too! |

Real result: the log says `Tomcat started on port 9090`, and `/settings` says:

```
Hi-from-command-line | Welcome, friend! | opens at 8 (next hour: 9) | app: hello
```

Remember `args` in `SpringApplication.run(HelloApplication.class, args)` (Chapter 50)? **That's** how Spring gets these! 🤓

> 💡 With **spaces** in the value, use quotes: `"--app.greeting=Hi from the command line"`.

### Way 2: Environment variables

An **environment variable** is a setting that the **operating system** gives to a program. Real servers on the internet use them **a lot** (Chapter 99–100).

The name changes a little: **CAPITAL letters**, and **`_`** instead of `.` and `-`:

| Setting | Environment variable |
|---|---|
| `server.port` | `SERVER_PORT` |
| `app.greeting` | `APP_GREETING` |
| `app.shop.open-hour` | `APP_SHOP_OPENHOUR` |

How to set them **just for one run**:

**Git Bash / Mac / Linux:**

```bash
SERVER_PORT=7070 APP_GREETING="Hi from an environment variable" java -jar target/hello-0.0.1-SNAPSHOT.jar
```

**Windows PowerShell:**

```powershell
$env:SERVER_PORT="7070"; $env:APP_GREETING="Hi from an environment variable"; java -jar target/hello-0.0.1-SNAPSHOT.jar
```

Real result: `Tomcat started on port 7070`, and `/settings`:

```
Hi from an environment variable | Welcome, friend! | opens at 8 (next hour: 9) | app: hello
```

> ⚠️ In PowerShell, `$env:...` stays set until you **close** that terminal window. Open a new terminal to get rid of it.

### Way 3: In IntelliJ

1. At the top right, click on **HelloApplication** (next to ▶) → **Edit Configurations...**
2. In the **Program arguments** field, type: `--server.port=9090`
   (Don't see it? Click **Modify options** → **Program arguments**.)
3. For environment variables: **Modify options** → **Environment variables** → type `SERVER_PORT=9090`.
4. Click **OK** and run. ▶️

### 🏆 Who wins?

When the same setting is in several places, Spring uses this order (the **top** one wins):

| Priority | Where | Example |
|---|---|---|
| 🥇 1 | **Command-line arguments** | `--server.port=9090` |
| 🥈 2 | **Environment variables** | `SERVER_PORT=7070` |
| 🥉 3 | **`application.properties`** (or `.yml`) in your project | `server.port=8080` |
| 4 | Default value in `@Value("${...:default}")` | `:Welcome, friend!` |

**Why is this so useful?** 🤔 You build **one** jar. Then:

- On your laptop: no extra settings → port 8080. 💻
- On the test server: `SERVER_PORT=9000`. 🧪
- On the real server: `SERVER_PORT=80` and the real database password. 🌍

**Same jar, different settings.** That's the professional way! 🏆

---

## 🔒 Part 8: Never put secrets in `application.properties`!

Soon you'll have **database passwords** (Part 9) and **secret keys** (Part 10). It's tempting to write:

```properties
spring.datasource.password=MySuperSecret123      # ❌❌❌ NO!
```

Why is this terrible? 😱 `application.properties` is in your project → it goes into **Git** (Chapter 42) → it goes to **GitHub** → **everybody** who can see the code can see your password! (Some bad people **search** GitHub for passwords automatically. 🕵️)

**✅ The right way:** use a **placeholder** in the file, and give the real value from **outside**:

```properties
spring.datasource.password=${DB_PASSWORD}
```

| Code | Meaning |
|---|---|
| `${DB_PASSWORD}` | "Take the value from the **environment variable** `DB_PASSWORD`." |

Then on the server: `DB_PASSWORD=MySuperSecret123`. The password is **never** in your code or in Git. 🔐 (We'll use this in Part 9.)

---

## 💻 Mini project: The bakery sign 🥐🪧

Let's make a "shop sign" endpoint that changes **completely** through settings.

### Step 1: Add settings

```properties
app.shop.city=Lakeside
app.shop.closed-on=SUNDAY
```

### Step 2: Add them to the record

```java
@ConfigurationProperties(prefix = "app.shop")
public record ShopProperties(String name, int openHour, int closeHour, List<String> products,
                             String city, DayOfWeek closedOn) {
}
```

(Add `import java.time.DayOfWeek;`.) `DayOfWeek` is an **enum** (Chapter 28, Chapter 39) — Spring converts the text `SUNDAY` to `DayOfWeek.SUNDAY` automatically! 🪄

### Step 3: A sign endpoint

Add this to `ShopController`:

```java
@GetMapping("/shop/sign")
public String sign() {
    return "🥐 " + shop.name() + " (" + shop.city() + ")\n"
            + "Open " + shop.openHour() + ":00 - " + shop.closeHour() + ":00\n"
            + "Closed on " + shop.closedOn() + "\n"
            + "Today we have: " + String.join(", ", shop.products());
}
```

| Code | Meaning |
|---|---|
| `"\n"` | A new line (Chapter 9). |
| `shop.closedOn()` | The `DayOfWeek` enum → printed as `SUNDAY`. |
| `String.join(", ", shop.products())` | Join the list into one text: `Bread, Cake, Cookies`. |

Restart → `GET /shop/sign`:

```
🥐 Sara's Bakery (Lakeside)
Open 8:00 - 18:00
Closed on SUNDAY
Today we have: Bread, Cake, Cookies
```

### Step 4: Open a second bakery — same code! 🏪🏪

Start the **same** jar with different settings:

```
java -jar target/hello-0.0.1-SNAPSHOT.jar --server.port=8081 "--app.shop.name=Tom's Bakery" --app.shop.city=Hillview --app.shop.products=Pie,Muffins
```

`http://localhost:8081/shop/sign`:

```
🥐 Tom's Bakery (Hillview)
Open 8:00 - 18:00
Closed on SUNDAY
Today we have: Pie, Muffins
```

**One program, two bakeries.** 🎉 That's the power of settings!

---

## ✋ Try it yourself

**Task 1:** Add a setting `app.max-students=30` and read it with `@Value` into an `int` in a new controller. Return `"Max students: 30. Room for 5 more? true"` (calculate `30 - 25 >= 5`).

<details>
<summary>Click to see the answer</summary>

```java
package com.example.hello;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ClassroomController {

    private final int maxStudents;

    public ClassroomController(@Value("${app.max-students}") int maxStudents) {
        this.maxStudents = maxStudents;
    }

    @GetMapping("/classroom")
    public String classroom() {
        int current = 25;
        boolean room = maxStudents - current >= 5;
        return "Max students: " + maxStudents + ". Room for 5 more? " + room;
    }
}
```

</details>

**Task 2:** Use a default value: `@Value("${app.motto:Learn every day!}")`. Run without the setting, then add `app.motto=Code is fun!` to the file. What do you see each time?

<details>
<summary>Click to see the answer</summary>

Without the setting: `Learn every day!` (the default). With the setting: `Code is fun!` (the file wins over the default).

</details>

**Task 3:** Start the app with `--app.shop.open-hour=7`. What does `/shop/hours` say? Then try `APP_SHOP_OPENHOUR=6` as an environment variable (Git Bash or PowerShell).

<details>
<summary>Click to see the answer</summary>

With `--app.shop.open-hour=7`: `Sara's Bakery is open 11 hours a day.` (18 − 7 = 11). With `APP_SHOP_OPENHOUR=6`: `... open 12 hours a day.` (18 − 6 = 12).

</details>

**Task 4:** Convert this to YAML:

```properties
app.zoo.name=City Zoo
app.zoo.animals=Lion,Zebra,Penguin
```

<details>
<summary>Click to see the answer</summary>

```yaml
app:
  zoo:
    name: City Zoo
    animals:
      - Lion
      - Zebra
      - Penguin
```

</details>

---

## ⚠️ Common mistakes

### Mistake 1: A typo in the key

In the file: `app.greting=Hello` (missing "e"). In the code: `@Value("${app.greeting}")`. The app doesn't start. In the long error you find:

```
Caused by: org.springframework.util.PlaceholderResolutionException: Could not resolve placeholder 'app.greeting' in value "${app.greeting}"
```

"I can't find a setting called `app.greeting`!" 🔍 **Fix:** Check the spelling in **both** places. (Or add a default value with `:` if the setting is optional.)

### Mistake 2: Wrong type

`app.shop.open-hour=eight` 😅, but the code wants an `int`. With `@ConfigurationProperties`, you get a very clear message:

```
***************************
APPLICATION FAILED TO START
***************************

Description:

Failed to bind properties under 'app.shop.open-hour' to int:

    Property: app.shop.open-hour
    Value: "eight"
    Origin: class path resource [application.properties] from hello-0.0.1-SNAPSHOT.jar - 6:20
    Reason: failed to convert java.lang.String to int (caused by java.lang.NumberFormatException: For input string: "eight")

Action:

Update your application's configuration
```

| Line | Meaning |
|---|---|
| `Property: app.shop.open-hour` | **Which** setting. |
| `Value: "eight"` | **What** you wrote. |
| `Origin: ... application.properties ... - 6:20` | **Where**: the file, **line 6**, column 20! 📍 |
| `Reason: failed to convert java.lang.String to int` | "I can't turn the text 'eight' into a number." |

With `@Value`, the message is shorter (`Failed to convert value of type 'java.lang.String' to required type 'int'; For input string: "eight"`). **Fix:** Write `8`. 🔢

### Mistake 3: Strange letters (é, ü, ñ...) in `.properties`

We tested `app.cafe=Café` in `application.properties`, and the app showed... `CafÃ©`! 😵 The `.properties` format is old, and Spring reads it with an **old character set** (ISO-8859-1), not UTF-8.

**Fix (choose one):**
- Use **YAML** (`application.yml`) — Spring reads it as UTF-8. We tested it: `Café` ✅.
- Or write the letter as a **code**: `app.cafe=Café Sara` → shows `Café Sara` ✅. (`é` is the code for `é`. Search "unicode é" to find any letter's code.)

### Mistake 4: Forgot `@ConfigurationPropertiesScan`

Your `ShopProperties` record isn't found:

```
Parameter 0 of constructor in com.example.hello.ShopController required a bean of type 'com.example.hello.ShopProperties' that could not be found.
```

**Fix:** Add `@ConfigurationPropertiesScan` to `HelloApplication`.

### Mistake 5: Changed the file, but nothing changed

Settings are read **once**, at **startup**. **Fix:** Restart! 🔄 (And check that no **command-line argument** or **environment variable** overrides your setting — Part 7.)

### Mistake 6: Passwords in the file

**Fix:** `${DB_PASSWORD}` in the file, real value in an environment variable. 🔒 (Part 8.)

---

## ✅ Summary

- **`application.properties`** (in `src/main/resources`) holds settings: `key=value`, `#` comments, dots for groups.
- Spring Boot has **many** settings: `server.port`, `spring.main.banner-mode`, `server.servlet.context-path`, `logging.level...`.
- Don't **hard-code** values that may change. Put them in settings (start your own keys with **`app.`**).
- **`@Value("${app.greeting}")`** reads one setting. **`${key:default}`** gives a default. Spring **converts** types (`"8"` → `8`).
- **`@ConfigurationProperties(prefix = "app.shop")`** on a **record** reads a whole group ✨ (`open-hour` → `openHour`, `A,B,C` → `List`). Turn it on with **`@ConfigurationPropertiesScan`**.
- **YAML** (`application.yml`) is the same with indentation. Use **one** format, not both.
- Override from outside: **command line** (`--server.port=9090`) 🥇 > **environment variables** (`SERVER_PORT`) 🥈 > the file 🥉 > defaults.
- **Same jar, different settings** for laptop, test server, real server. 🏆
- 🔒 **Never** put passwords in the file. Use `${DB_PASSWORD}` + an environment variable.

---

## ❓ Quiz

1. Where is `application.properties`?
2. What does this do: `@Value("${app.color:blue}") String color`?
3. The file has `app.lucky-number=7`. Can you read it into an `int`?
4. What do you need to make `@ConfigurationProperties` records work?
5. With `@ConfigurationProperties(prefix = "app.pet")`, which record field gets `app.pet.favorite-food`?
6. Write `server.port=8081` in YAML.
7. The file says `server.port=8080`, you start with `--server.port=9090`, and `SERVER_PORT=7070` is set. Which port is used?
8. What's the environment variable name for `app.shop.name`?
9. Why should a database password not be in `application.properties`?
10. You see `Could not resolve placeholder 'app.title'`. What's wrong?

<details>
<summary>Click to see the answers</summary>

1. `src/main/resources/application.properties`
2. It reads the setting `app.color`. If it doesn't exist, it uses the default `blue`.
3. Yes. Spring converts the text `"7"` to the number `7`.
4. Add `@ConfigurationPropertiesScan` to the main class.
5. `favoriteFood` (relaxed binding: `favorite-food` → `favoriteFood`).
6. ```yaml
   server:
     port: 8081
   ```
7. 9090 — the command line wins.
8. `APP_SHOP_NAME`
9. Because the file goes into Git (and maybe GitHub), where other people can see it. Use an environment variable instead.
10. There's no setting `app.title` (it's missing or misspelled), and no default value was given.

</details>

---

[⬅ Previous chapter](54-beans.md) | [Table of Contents](../README.md) | [Next chapter: Profiles: dev and prod settings ➡](56-profiles.md)
