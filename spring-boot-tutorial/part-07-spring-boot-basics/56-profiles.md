# Chapter 56 – Profiles: dev and prod settings

[⬅ Previous chapter](55-application-properties.md) | [Table of Contents](../README.md) | [Next chapter ➡](../part-08-rest-apis/57-rest-controller.md)

---

## 🎯 Goal

Your app runs on **your laptop** today. One day it will run on a **real server** on the internet. 🌍 These two places need **different settings**. How do you manage that **cleanly**? With **profiles**! 🎭

At the end of this chapter you will know:

- What a **profile** is, and why apps need them
- How to make **profile files**: `application-dev.properties`, `application-prod.properties`
- **Three ways** to choose (activate) a profile
- How to **see** which profile is active
- How to make **beans** that exist **only** in one profile, with **`@Profile`** 🫘
- The **"not"** trick: `@Profile("!prod")`
- Good habits (and common traps) with profiles

> 🌱 This is the **last chapter of Part 7**! After this, you know the **basics** of Spring Boot. 🎉

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Profile** 🎭 | A **named set of settings** for one situation: `dev`, `test`, `prod`... |
| **Environment** | **Where** the app runs: your laptop, a test server, the real server. |
| **dev** | Short for "**development**": your own computer, while you write code. 💻 |
| **test** | A test server, where the team checks the app before it goes live. 🧪 |
| **prod** | Short for "**production**": the **real** server, with **real** users. 🌍 |
| **Active profile** | The profile that is **turned on** right now. |
| **Profile-specific file** | A settings file just for one profile: `application-dev.properties`. |
| **`@Profile`** | A label: "Make this bean **only** when this profile is active." |
| **Default profile** | The profile Spring uses when you didn't choose one. It's called `default`. |

---

## 📖 Story: The phone modes 📱

Your phone has **modes**:

- 🏫 **School mode:** sound off, games blocked, alarm at 7:00.
- 🏠 **Home mode:** sound on, games allowed.
- ✈️ **Airplane mode:** no internet, no calls.

It's the **same phone**. You don't buy a new phone for school! You just **switch the mode**, and many settings change **at once**.

Spring Boot **profiles** are the same:

| Phone | Spring Boot |
|---|---|
| The phone 📱 | Your app (the **same** jar) |
| A mode (School, Home) | A **profile** (`dev`, `prod`) |
| The settings of each mode | `application-dev.properties`, `application-prod.properties` |
| Switching the mode | **Activating** a profile |
| Normal settings (wallpaper, contacts) that are the same in every mode | `application.properties` — used in **every** profile |

---

## 🤔 Part 1: Why do we need profiles?

Your laptop and the real server are **very** different:

| Thing | 💻 dev (your laptop) | 🌍 prod (the real server) |
|---|---|---|
| Port | `8081` (so it doesn't clash with other things) | `80` or `8080` |
| Database | A small test database with fake data (Part 9) | The **real** database with **real** customer data 😱 |
| Sending emails | **Fake**! Just print them (don't spam real people) 📝 | **Real** emails 📧 |
| Log messages | **Many** (DEBUG), to find bugs 🐛 | **Few** (INFO, WARN), to stay fast |
| Error details | Show a lot, to help you | Show little (bad people could learn from them 🕵️) |

Without profiles, you'd need to **change the settings by hand** every time you move the app. 😩 You **will** forget something. And sending **real** emails to **real** customers from your laptop, while testing, is a **disaster**! 📧💥

With profiles: write the settings **once** for each environment, then **switch** with one word. 🎭

---

## 📄 Part 2: Profile files

The idea: next to `application.properties`, create a file for **each profile**. The name **must** be:

```
application-{profile}.properties
```

### Step 1: Create the files

In **`src/main/resources`**, create two new files (right-click → **New → File**):

**`application-dev.properties`**

```properties
server.port=8081
app.greeting=Hello from DEV
```

**`application-prod.properties`**

```properties
server.port=8090
app.greeting=Hello from PROD
```

Your `resources` folder now looks like this:

```
src/main/resources/
├── static/
├── templates/
├── application.properties         ← 🌍 ALWAYS used (shared settings)
├── application-dev.properties     ← 💻 only when "dev" is active
└── application-prod.properties    ← 🌍 only when "prod" is active
```

### Step 2: How Spring combines them 🧩

When a profile is active, Spring reads **two** files:

1. First **`application.properties`** — the **shared** settings (always). 📄
2. Then **`application-dev.properties`** — the **profile** settings, which **win** over the shared ones. 📄⬆️

```
 application.properties              application-dev.properties          RESULT (dev active)
 ───────────────────────             ──────────────────────────          ───────────────────
 spring.application.name=hello                                     →     hello
 app.greeting=Hello from the main... app.greeting=Hello from DEV   →     Hello from DEV  ⬆️ (dev wins)
 app.shop.name=Sara's Bakery                                       →     Sara's Bakery
                                     server.port=8081              →     8081
```

**Rule:** Put settings that are the **same** everywhere in `application.properties`. Put only the **differences** in the profile files. ✂️

---

## 🔛 Part 3: Activate a profile

Creating the files isn't enough — you must **turn a profile on**. There are 3 ways.

### Way 1: In `application.properties`

Add this line to **`application.properties`**:

```properties
spring.profiles.active=dev
```

| Code | Meaning |
|---|---|
| `spring.profiles.active` | The setting that **chooses** the profile. |
| `=dev` | "Turn on the `dev` profile." |

Restart and look at the log. Remember this line from Chapter 51?

```
No active profile set, falling back to 1 default profile: "default"
```

Now it says:

```
The following 1 profile is active: "dev"
```

🎉 And a few lines later:

```
Tomcat started on port 8081 (http) with context path '/'
```

Port **8081** — from `application-dev.properties`! ✅ And `http://localhost:8081/settings` (Chapter 55) shows:

```
Hello from DEV | Welcome, friend! | opens at 8 (next hour: 9) | app: hello
```

`Hello from DEV` — the dev file **won** over the shared file. ⬆️

> 💡 **Tip:** Writing `spring.profiles.active=dev` in `application.properties` makes **dev** the normal choice. That's handy: on your laptop, you just press ▶️. On the real server, you **override** it (Way 2 or 3) with `prod`. Command line and environment variables **win** over the file — remember Chapter 55! 🥇

### Way 2: Command line

```
java -jar target/hello-0.0.1-SNAPSHOT.jar --spring.profiles.active=prod
```

Real log:

```
The following 1 profile is active: "prod"
...
Tomcat started on port 8090 (http) with context path '/'
```

And `http://localhost:8090/settings`:

```
Hello from PROD | Welcome, friend! | opens at 8 (next hour: 9) | app: hello
```

### Way 3: Environment variable

```bash
SPRING_PROFILES_ACTIVE=prod java -jar target/hello-0.0.1-SNAPSHOT.jar
```

(PowerShell: `$env:SPRING_PROFILES_ACTIVE="prod"; java -jar target/hello-0.0.1-SNAPSHOT.jar`)

This is the **most common** way on real servers and in **Docker** (Chapter 99). 🐳

### In IntelliJ

**Run → Edit Configurations...** → your `HelloApplication` → **Program arguments**: `--spring.profiles.active=prod` (or **Modify options → Environment variables**: `SPRING_PROFILES_ACTIVE=prod`). → **OK** → ▶️

(IntelliJ **Ultimate** also has a special **Active profiles** field for Spring Boot apps. Same result.)

---

## 👀 Part 4: Which profile is active? Ask the app!

Spring has a bean called **`Environment`** that knows everything about settings and profiles. You can **inject** it like any bean (Chapter 53)!

**`ProfileController.java`**

```java
package com.example.hello;

import java.util.Arrays;

import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ProfileController {

    private final Environment environment;

    public ProfileController(Environment environment) {
        this.environment = environment;
    }

    @GetMapping("/profile")
    public String profile() {
        return "Active profiles: " + Arrays.toString(environment.getActiveProfiles());
    }
}
```

| Code | Meaning |
|---|---|
| `import org.springframework.core.env.Environment;` | Spring's `Environment` type. (Careful: from `org.springframework.core.env`!) |
| `public ProfileController(Environment environment)` | 💉 Spring injects its own `Environment` bean. (One of the ~150 beans Spring Boot makes for you — Chapter 54!) |
| `environment.getActiveProfiles()` | Returns an **array** of the active profile names. |
| `Arrays.toString(...)` | Turns the array into nice text like `[dev]` (Chapter 14). |

With `dev` active → `GET /profile`:

```
Active profiles: [dev]
```

With `prod` → `Active profiles: [prod]`. 🎭

---

## 🫘 Part 5: Beans for one profile only — `@Profile`

Settings aren't the only difference. Sometimes you need **different code**! 📧 Remember the problem: on your laptop, you **don't** want to send real emails.

**Solution:** two beans for the same interface — and each one exists **only** in one profile.

### Step 1: The interface

**`MailService.java`**

```java
package com.example.hello;

public interface MailService {
    String sendWelcomeMail(String to);
}
```

### Step 2: A fake one for dev

**`FakeMailService.java`**

```java
package com.example.hello;

import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Service;

@Service
@Profile("dev")
public class FakeMailService implements MailService {

    @Override
    public String sendWelcomeMail(String to) {
        System.out.println("FAKE mail to " + to + " (not really sent)");
        return "DEV: pretended to send a mail to " + to;
    }
}
```

### Step 3: A real one for prod

**`RealMailService.java`**

```java
package com.example.hello;

import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Service;

@Service
@Profile("prod")
public class RealMailService implements MailService {

    @Override
    public String sendWelcomeMail(String to) {
        // In a real app, this would talk to a mail server.
        return "PROD: really sent a mail to " + to;
    }
}
```

| Code | Meaning |
|---|---|
| `@Profile("dev")` | ⭐ "Make this bean **only** if the `dev` profile is active. Otherwise, **ignore** this class." |
| `@Profile("prod")` | "Only if `prod` is active." |
| `System.out.println("FAKE mail ...")` | The fake one just **prints** — no real email. 📝 |
| `// In a real app...` | We don't really send emails in this book. (It needs a mail server and a password.) The idea is what matters! |

### Step 4: Use it

Add to **`ProfileController`**: a `MailService` in the constructor, and a new endpoint.

```java
private final MailService mailService;
private final Environment environment;

public ProfileController(MailService mailService, Environment environment) {
    this.mailService = mailService;
    this.environment = environment;
}

@GetMapping("/mail")
public String mail() {
    return mailService.sendWelcomeMail("sara@example.com");
}
```

The controller asks for **a** `MailService`. It doesn't know (or care!) which one. 🙈 (Loose coupling — Chapter 53. 🔌)

### Step 5: Test both profiles

**With `dev`** → `GET http://localhost:8081/mail`:

```
DEV: pretended to send a mail to sara@example.com
```

and in the console:

```
FAKE mail to sara@example.com (not really sent)
```

**With `prod`** (`--spring.profiles.active=prod`) → `GET http://localhost:8090/mail`:

```
PROD: really sent a mail to sara@example.com
```

🎉 **Same code, same jar** — but a different bean was created! Only **one** `MailService` exists at a time, so there's no "2 beans found" problem. ✅

```
                  dev active? 💻                      prod active? 🌍
  ┌──────────────────────────────┐    ┌──────────────────────────────┐
  │ 🫘 FakeMailService  ✅ created │    │ 🫘 FakeMailService  ❌ skipped │
  │ 🫘 RealMailService  ❌ skipped │    │ 🫘 RealMailService  ✅ created │
  └──────────────────────────────┘    └──────────────────────────────┘
```

---

## 😱 Part 6: The "no profile" trap — and the `!` trick

What if **no** profile is active? Remove `spring.profiles.active=dev` from `application.properties`, and start without arguments. The log says:

```
No active profile set, falling back to 1 default profile: "default"
```

and then... 💥

```
***************************
APPLICATION FAILED TO START
***************************

Description:

Parameter 0 of constructor in com.example.hello.ProfileController required a bean of type 'com.example.hello.MailService' that could not be found.


Action:

Consider defining a bean of type 'com.example.hello.MailService' in your configuration.
```

Of course! The active profile is `default`. `FakeMailService` wants `dev`, `RealMailService` wants `prod`. **Neither** is created. No `MailService` at all! 🤷

### ✅ Fix: `@Profile("!prod")` — "NOT prod"

Change `FakeMailService`:

```java
@Service
@Profile("!prod")
public class FakeMailService implements MailService {
```

| Code | Meaning |
|---|---|
| `"!prod"` | `!` means **NOT** (like in Java — Chapter 10!). "Make this bean in **every** profile **except** `prod`." |

Now:

| Active profile | FakeMailService (`!prod`) | RealMailService (`prod`) | Result |
|---|---|---|---|
| `default` (none chosen) | ✅ | ❌ | Fake ✅ |
| `dev` | ✅ | ❌ | Fake ✅ |
| `test` | ✅ | ❌ | Fake ✅ |
| `prod` | ❌ | ✅ | Real ✅ |

We tested it: with **no** profile, the app starts, and `/mail` says `DEV: pretended to send a mail to sara@example.com`. ✅

**Why is this the safe choice?** 🛡️ Real emails are sent **only** when you **clearly** say `prod`. If you forget to choose a profile, you get the **fake** — not a disaster. 😌

---

## 🎭🎭 Part 7: More than one profile at once

You can activate **several** profiles, separated by **commas**:

```bash
SPRING_PROFILES_ACTIVE=dev,extra java -jar target/hello-0.0.1-SNAPSHOT.jar
```

Real log:

```
The following 2 profiles are active: "dev", "extra"
```

and `/profile` says `Active profiles: [dev, extra]`.

If both `application-dev.properties` and `application-extra.properties` have the **same key**, the **last** profile in the list (`extra`) wins. (You'll rarely need several profiles while learning. But you'll see it in real projects!)

---

## 🏆 Part 8: Good habits with profiles

| ✅ Do | ❌ Don't |
|---|---|
| Put **shared** settings in `application.properties` | Copy the same settings into every profile file |
| Put only the **differences** in profile files | Make huge profile files |
| Use common names: **`dev`**, **`test`**, **`prod`** | Invent confusing names like `sara-laptop-2` |
| Make the **safe** choice the normal one (`!prod` for fakes) | Make `prod` the normal one (dangerous on laptops!) |
| Activate `prod` **from outside** (env variable) on the server | Write `spring.profiles.active=prod` in the file |
| Keep **passwords** in environment variables (Chapter 55) | Put prod passwords in `application-prod.properties` 🔓 |

---

## 💻 Mini project: Three environments 💻🧪🌍

Let's add a **third** profile, **`test`**, and fill in a table.

### Step 1: Create `application-test.properties`

```properties
server.port=8095
app.greeting=Hello from TEST
app.shop.name=Test Bakery (not real!)
```

### Step 2: Predict, then check! 🔮

Fill in the table **before** you run. Then start the app 3 times (once per profile) and check with `/profile`, `/settings`, `/shop/hours` and `/mail`.

| | `dev` | `test` | `prod` |
|---|---|---|---|
| Port | ? | ? | ? |
| `/settings` starts with | ? | ? | ? |
| `/shop/hours` says | ? | ? | ? |
| `/mail` says | ? | ? | ? |

<details>
<summary>Click to see the answers</summary>

| | `dev` | `test` | `prod` |
|---|---|---|---|
| Port | `8081` | `8095` | `8090` |
| `/settings` starts with | `Hello from DEV` | `Hello from TEST` | `Hello from PROD` |
| `/shop/hours` says | `Sara's Bakery is open 10 hours a day.` | `Test Bakery (not real!) is open 10 hours a day.` | `Sara's Bakery is open 10 hours a day.` |
| `/mail` says | `DEV: pretended...` | `DEV: pretended...` (`test` is "not prod" → fake ✅) | `PROD: really sent...` |

Notice: `test` changes the shop name, but `dev` and `prod` **don't** — so they use the shared value from `application.properties`. And the opening hours are the same everywhere, because **no** profile file changes them. 🧩

</details>

---

## ✋ Try it yourself

**Task 1:** In `application-dev.properties`, turn off the banner. In `application-prod.properties`, set `logging.level.root=WARN`. Start with each profile. What's different in the console?

<details>
<summary>Click to see the answer</summary>

```properties
# application-dev.properties
spring.main.banner-mode=off
```

```properties
# application-prod.properties
logging.level.root=WARN
```

- **dev:** no Spring banner, but all the INFO log lines.
- **prod:** the banner is there, but almost **no** log lines — only WARN and ERROR messages are shown. Even "Tomcat started on port 8090" and "Started HelloApplication..." are hidden, because they're INFO! 🤫 (The app still works — try `/profile`.)

</details>

**Task 2:** Make a `WelcomeService` interface with a method `String welcome()`. Make two beans: `KidsWelcome` (`@Profile("kids")`) returning `"Hi kiddo! 🧸"`, and `NormalWelcome` (`@Profile("!kids")`) returning `"Welcome."`. Add an endpoint `/welcome`. Test with and without the `kids` profile.

<details>
<summary>Click to see the answer</summary>

```java
public interface WelcomeService {
    String welcome();
}
```

```java
@Service
@Profile("kids")
public class KidsWelcome implements WelcomeService {
    @Override
    public String welcome() {
        return "Hi kiddo! 🧸";
    }
}
```

```java
@Service
@Profile("!kids")
public class NormalWelcome implements WelcomeService {
    @Override
    public String welcome() {
        return "Welcome.";
    }
}
```

```java
@RestController
public class WelcomeController {

    private final WelcomeService welcomeService;

    public WelcomeController(WelcomeService welcomeService) {
        this.welcomeService = welcomeService;
    }

    @GetMapping("/welcome")
    public String welcome() {
        return welcomeService.welcome();
    }
}
```

(Each class in its own file, with `package com.example.hello;` and the imports.)

- Without `kids` (for example `dev`) → `Welcome.`
- With `--spring.profiles.active=kids` → `Hi kiddo! 🧸`
- With `dev,kids` → `Hi kiddo! 🧸` (because `kids` is active)

</details>

**Task 3:** Your friend wrote `application_dev.properties` (with an underscore `_`). They activate `dev`, but the port is still 8080. Why?

<details>
<summary>Click to see the answer</summary>

The file name must be `application-dev.properties` — with a **minus sign** `-`, not `_`. Spring doesn't know `application_dev.properties`, so it simply **ignores** it (no error!). 🙈

</details>

---

## ⚠️ Common mistakes

### Mistake 1: A wrong file name

`application_dev.properties`, `application-Dev.properties`, `dev.properties`, `application-dev.propertis`... ❌ All **silently ignored**. **Fix:** Exactly `application-{profile}.properties`, in `src/main/resources`, with the profile name written the same way (small letters are best).

### Mistake 2: Forgetting to activate the profile

You created `application-dev.properties`, but the log says `No active profile set, falling back to 1 default profile: "default"`. **Fix:** Activate it (Part 3). **Always** check this log line when settings seem "wrong". 👀

### Mistake 3: No bean for the active profile

`required a bean of type '...MailService' that could not be found` — because your beans only exist in `dev` and `prod`, but neither is active. **Fix:** Use `@Profile("!prod")` for the safe/fake version (Part 6).

### Mistake 4: Choosing the profile inside a profile file

Writing `spring.profiles.active=prod` **inside** `application-dev.properties`. ❌ Spring refuses to start:

```
org.springframework.boot.context.config.InvalidConfigDataPropertyException: Property 'spring.profiles.active' imported from location 'class path resource [application-dev.properties]' is invalid in a profile specific resource [origin: class path resource [application-dev.properties] from hello-0.0.1-SNAPSHOT.jar - 3:24]
```

"You can't choose a profile **from inside** a profile file." (That would be confusing — like a mode on your phone that switches to **another** mode! 🌀) **Fix:** Choose profiles only in `application.properties`, on the command line, or with an environment variable.

### Mistake 5: Real things happening in dev 😱

Your laptop sends **real** emails or uses the **real** database because the prod settings are in `application.properties`. **Fix:** Shared file = **safe** settings. Real/dangerous things → **only** in `prod`, and activate `prod` **only** on the real server.

---

## ✅ Summary

- A **profile** 🎭 is a named set of settings (and beans) for one environment: **`dev`** 💻, **`test`** 🧪, **`prod`** 🌍.
- Profile files: **`application-{profile}.properties`**. `application.properties` is **always** read; the active profile's file **wins** for the same keys.
- **Activate** a profile: `spring.profiles.active=dev` in `application.properties`, **`--spring.profiles.active=prod`** on the command line, or **`SPRING_PROFILES_ACTIVE=prod`** as an environment variable.
- The log tells you: `The following 1 profile is active: "dev"` (or `No active profile set...`).
- Inject Spring's **`Environment`** to ask which profiles are active.
- **`@Profile("dev")`** on a bean → the bean exists **only** in `dev`. **`@Profile("!prod")`** → everywhere **except** `prod` — the **safe** choice for fakes. 🛡️
- Several profiles: `dev,extra` — the last one wins for the same key.
- Same jar, different profiles — the professional way to run one app in many places. 🏆

---

## ❓ Quiz

1. What is a profile?
2. What do `dev` and `prod` mean?
3. What must the settings file for the profile `test` be called?
4. `application.properties` says `app.color=blue`. `application-dev.properties` says `app.color=green`. `dev` is active. What's the color?
5. Name three ways to activate the `prod` profile.
6. Which log line tells you that **no** profile was chosen?
7. What does `@Profile("dev")` on a class do?
8. What does `@Profile("!prod")` mean? Why is it a safe choice for a fake email sender?
9. Can you write `spring.profiles.active=prod` inside `application-dev.properties`?
10. How can your code find out which profiles are active?

<details>
<summary>Click to see the answers</summary>

1. A named set of settings (and beans) for one situation or environment, like `dev` or `prod`.
2. `dev` = development (your own computer while coding). `prod` = production (the real server with real users).
3. `application-test.properties`
4. `green` — the active profile's file wins.
5. `spring.profiles.active=prod` in `application.properties`; `--spring.profiles.active=prod` on the command line; the environment variable `SPRING_PROFILES_ACTIVE=prod`. (Also: IntelliJ's run configuration.)
6. `No active profile set, falling back to 1 default profile: "default"`
7. Spring creates that bean **only** when the `dev` profile is active.
8. "Every profile except `prod`." It's safe because the fake is used everywhere unless you **clearly** choose `prod` — so you never send real emails by accident.
9. No. Spring refuses to start: the property is invalid in a profile-specific file.
10. Inject Spring's `Environment` bean and call `getActiveProfiles()`.

</details>

---

## 🎉 Part 7 complete!

You now know the **basics of Spring Boot**! 🌱🎉

- ✅ What Spring and Spring Boot are (and you built a mini framework!)
- ✅ Creating a project with Spring Initializr
- ✅ Every folder and file in a project
- ✅ Running, reading logs, fixing "port in use"
- ✅ Your first endpoints — text **and JSON**
- ✅ **Dependency Injection** — the big idea 💉
- ✅ **Beans**: labels, singletons, `@Bean`, lifecycle, `@Primary`, `@Qualifier`
- ✅ **Settings**: `@Value`, `@ConfigurationProperties`, YAML, overrides
- ✅ **Profiles**: dev, test, prod, `@Profile`

### 🏁 Where are we?

```
 Part 1 ✅ Getting ready          Part 5 ✅ Tools (Maven, Git)
 Part 2 ✅ Java basics            Part 6 ✅ How the web works
 Part 3 ✅ Objects (OOP)          Part 7 ✅ Spring Boot basics  ← you are here! 🎉
 Part 4 ✅ More Java              Part 8 ⏳ Building REST APIs   ← next!
```

Your apps can **answer** questions now. But so far, they only **give** data. In **Part 8**, your API learns to **receive** data too: **path variables** (`/students/5`), **query parameters** (`?name=Ali`), **POST** with JSON bodies, **PUT** and **DELETE**, **status codes**, **validation**, and **nice error messages**. You'll build a complete **Student API**! 🚀

Let's go! 💪

---

[⬅ Previous chapter](55-application-properties.md) | [Table of Contents](../README.md) | [Next chapter: @RestController and @GetMapping ➡](../part-08-rest-apis/57-rest-controller.md)
