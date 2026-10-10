# Chapter 53 – Dependency Injection: the big idea

[⬅ Previous chapter](52-hello-endpoint.md) | [Table of Contents](../README.md) | [Next chapter ➡](54-beans.md)

---

## 🎯 Goal

This is the **most important idea** in all of Spring. ⭐⭐⭐ Every Spring Boot app in the world uses it, in almost every class.

At the end of this chapter you will know:

- What a **dependency** is
- Why creating your helpers yourself with **`new`** causes problems 🧲
- What **Dependency Injection (DI)** means — first **by hand**, in plain Java
- How **Spring** does DI for you, with **`@Service`** and a **constructor** ✨
- The **three kinds** of injection, and why **constructor injection** is the best
- How DI + **interfaces** lets you **swap** parts without changing code 🔌
- A full chain: **Controller → Service → Repository**

> 🌱 You already know the idea! In **Chapter 25** (interfaces) you gave an `OrderService` its `MessageSender` from outside. We said: "This is called Dependency Injection, and Spring does it for you. Chapter 53." Well... **this is Chapter 53!** 🎉

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Dependency** | Something a class **needs** to do its job. A `Chef` needs an `Oven`. The oven is the chef's **dependency**. |
| **Inject** | To **give** or **put in** from outside. (Like a doctor's injection 💉 — something goes **in**.) |
| **Dependency Injection (DI)** | A class **gets** its dependencies **from outside**, instead of creating them itself. |
| **Tight coupling** | Two classes are **glued** together. Changing one means changing the other. 🧲 |
| **Loose coupling** | Two classes are connected by a **plug** (an interface). Easy to swap. 🔌 |
| **Service** | A class that holds the **business logic** — the real "work" of the app (calculating, checking, deciding). |
| **`@Service`** | A label: "Spring, this class is a service. Make a bean of it." |
| **Constructor injection** | Spring gives the dependencies **through the constructor**. ✅ The best way. |
| **`@Autowired`** | A label that says "Spring, inject something here." (Often not needed — you'll see why.) |

---

## 📖 Story: The pizza chef and the oven 🍕

Chef Mario makes pizza. To bake pizza, he needs an **oven**. The oven is his **dependency**.

**Way 1: Mario builds his own oven** 🧱

Every morning, Mario **builds** an oven from bricks before he can cook. 😩

- If the restaurant wants a **better** oven (electric ⚡ instead of wood 🪵), Mario must **learn to build** a different oven. His whole routine changes.
- If an inspector wants to **test** Mario's cooking with a **small test oven**, he can't — Mario always builds his own.
- If there are **5 chefs**, there are **5 ovens**, even if one would be enough.

**Way 2: The restaurant gives Mario an oven** 🎁

The restaurant **owner** buys an oven and **places it** in Mario's kitchen. Mario just says: "I need **an** oven. Any oven that can **bake**."

- Better oven? The owner **swaps** it. Mario changes **nothing**. 😎
- Test? The inspector puts a **test oven** in. Mario cooks like always.
- 5 chefs can **share** one oven.

Way 2 is **Dependency Injection**: Mario doesn't **create** his dependency. It's **given** to him (injected 💉) from outside.

And in Spring Boot, the "**restaurant owner**" who buys and places everything is... **Spring**! 🌱

---

## 🧩 Part 1: What is a dependency?

When class **A** **uses** class **B** to do its job, **B** is a **dependency** of **A**. "A **depends on** B."

```
   Waiter ──needs──► Chef ──needs──► Oven
```

- `Waiter` depends on `Chef` (the waiter asks the chef to cook).
- `Chef` depends on `Oven` (the chef needs the oven to bake).

In a Spring Boot app, you'll see this **everywhere**:

```
   StudentController ──needs──► StudentService ──needs──► StudentRepository ──needs──► Database
```

The real question is: **who creates** these objects, and **how** does each one **get** the ones it needs? 🤔

---

## 🧲 Part 2: The problem — creating your own dependencies

Here's the "Way 1" chef in Java:

```java
class Chef {
    private final Oven oven = new Oven();    // 🧱 builds his own oven

    String cook(String dish) {
        return "Chef made: " + oven.bake(dish);
    }
}
```

It works! But look at `new Oven()`. The `Chef` class **decides** which oven, and **creates** it. This **glues** `Chef` to `Oven`. 🧲

| Problem | Example |
|---|---|
| 🔒 Can't swap | Want an `ElectricOven`? You must **change the `Chef` class**. |
| 🧪 Hard to test | A test can't give the chef a **fake** oven. He always makes a real one. |
| 🔁 No sharing | Every `Chef` makes its **own** `Oven`. 100 chefs = 100 ovens. |
| 🪆 Chains get ugly | If `Oven` needs a `GasPipe`, and `GasPipe` needs a `GasCompany`... `Chef` must know **all** of it! |

The last problem is the worst. Imagine:

```java
class Waiter {
    private final Chef chef = new Chef(new Oven(new GasPipe(new GasCompany("CityGas"))));  // 😱
}
```

The **waiter** has to know about the **gas company**?! That's crazy. 🤯 A waiter should only know: "I need a chef."

---

## 💉 Part 3: The solution — Dependency Injection (by hand)

**The idea:** A class doesn't **create** its dependencies. It **asks** for them in its **constructor**. Somebody else **gives** them.

Let's write a small restaurant in plain Java. Save it as **`Restaurant.java`** (a normal Java file, **not** in your Spring project — Chapter 5 style):

```java
public class Restaurant {
    public static void main(String[] args) {
        // The "assembler": WE build every object and plug them together
        Oven oven = new Oven();
        Chef chef = new Chef(oven);
        Waiter waiter = new Waiter(chef);

        System.out.println(waiter.takeOrder("Pizza"));
    }
}

class Oven {
    String bake(String food) {
        return food + " baked at 200 degrees";
    }
}

class Chef {
    private final Oven oven;

    Chef(Oven oven) {
        this.oven = oven;
        System.out.println("Chef is ready. I got an oven from outside!");
    }

    String cook(String dish) {
        return "Chef made: " + oven.bake(dish);
    }
}

class Waiter {
    private final Chef chef;

    Waiter(Chef chef) {
        this.chef = chef;
        System.out.println("Waiter is ready. I got a chef from outside!");
    }

    String takeOrder(String dish) {
        return "Here is your food: " + chef.cook(dish);
    }
}
```

Run it: `java Restaurant.java`

**Output:**

```
Chef is ready. I got an oven from outside!
Waiter is ready. I got a chef from outside!
Here is your food: Chef made: Pizza baked at 200 degrees
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `Oven oven = new Oven();` | Step 1: create the oven (it needs nothing). |
| `Chef chef = new Chef(oven);` | Step 2: create the chef and **give** him the oven. 💉 |
| `Waiter waiter = new Waiter(chef);` | Step 3: create the waiter and **give** him the chef. 💉 |
| `waiter.takeOrder("Pizza")` | Use the waiter. He asks the chef, the chef uses the oven. |
| `private final Oven oven;` | The chef **has** an oven field. `final` = it's set once and never changes. |
| `Chef(Oven oven) {` | ⭐ The constructor **asks** for an oven: "To create me, you must **give** me an oven." |
| `this.oven = oven;` | Save the oven we got (Chapter 20). |
| `oven.bake(dish)` | Use it. The chef doesn't care **where** the oven came from. |
| `private final Chef chef;` + `Waiter(Chef chef)` | Same idea: the waiter **asks** for a chef. He knows **nothing** about ovens! 🎉 |

**Look at `main`:** it's the only place that uses `new`, and it creates things in the right **order** (oven → chef → waiter). We call this part the **assembler** 🔧 — it **assembles** (puts together) the objects.

### 🎉 What did we win?

| Before (`new` inside) 🧲 | After (DI) 🔌 |
|---|---|
| `Chef` creates its own `Oven` | `Chef` **receives** an `Oven` |
| `Waiter` must know about ovens | `Waiter` only knows about `Chef` |
| Swap the oven → change `Chef` | Swap the oven → change **only** `main` |
| Can't share an oven | Give the **same** oven to many chefs |

---

## 🔄 Part 4: Inversion of Control — who's the boss?

In Part 3, **`main`** was the assembler. In a small program, that's fine. But a real Spring Boot app has **hundreds** of classes. 😵 Writing all the `new` lines by hand, in the right order, would be a nightmare.

So Spring says: "**Let me be the assembler!**" 🌱

| Plain Java | Spring Boot |
|---|---|
| **You** write `new Oven()`, `new Chef(oven)`... | **Spring** creates the objects. |
| **You** decide the order. | **Spring** figures out the order. |
| **You** give each object its dependencies. | **Spring** injects them. 💉 |

Remember **Inversion of Control** from Chapter 48? "Don't call us, we'll call you." 🎬 Here it means: you **don't create** your objects. Spring creates them and **gives** them to you. The control is **inverted** (turned around).

---

## 🌱 Part 5: Dependency Injection in Spring Boot

Let's do it for real in your **`hello`** project! We'll make a **service** that creates greetings, and a **controller** that uses it.

### Step 1: The service

Create a new class in `com.example.hello`: **`GreetingService`**

```java
package com.example.hello;

import org.springframework.stereotype.Service;

@Service
public class GreetingService {

    public String greet(String name) {
        return "Hello, " + name + "! Welcome to Spring Boot.";
    }
}
```

| Code | Meaning |
|---|---|
| `import org.springframework.stereotype.Service;` | We use the `@Service` label. |
| `@Service` | ⭐ "Spring, this is a **service**. Please create **one** object of it and keep it in your container (a **bean** 🫘). Others may need it." |
| `public class GreetingService` | A normal class. It knows **nothing** about HTTP or controllers. It just does its **job**: making greetings. |
| `public String greet(String name)` | The work: build a greeting text. (This is "business logic". Here it's tiny. In real apps it's the important part!) |

### Step 2: The controller that needs it

Create **`GreetingController`**:

```java
package com.example.hello;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GreetingController {

    private final GreetingService greetingService;

    public GreetingController(GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    @GetMapping("/greet")
    public String greet() {
        return greetingService.greet("Sara");
    }
}
```

| Code | Meaning |
|---|---|
| `private final GreetingService greetingService;` | The controller **has** a service field. `final` = set once, never changed. |
| `public GreetingController(GreetingService greetingService) {` | ⭐⭐ The constructor **asks** for a `GreetingService`. "To create me, give me a greeting service!" |
| `this.greetingService = greetingService;` | Save it. |
| `greetingService.greet("Sara")` | **Use** the service to do the work. The controller just **passes** the answer back. |

**Notice what's missing:** there's **no** `new GreetingService()` anywhere! 🤯 Not in the controller. Not in `main`. Not anywhere.

### Step 3: Restart and visit `http://localhost:8080/greet`

```
Hello, Sara! Welcome to Spring Boot.
```

🎉 It works! But **who** gave the controller its service? 🤔

### 🔬 What Spring did at startup

```
 1. 🔍 Scan:    found @Service GreetingService, found @RestController GreetingController
 2. 🫘 Create:  new GreetingService()                       → bean "greetingService"
 3. 🧐 Look:    GreetingController's constructor needs a GreetingService...
                "Do I have a bean of that type? YES! 🫘"
 4. 💉 Inject:  new GreetingController(greetingService)     → bean "greetingController"
 5. 📝 Map:     GET /greet → greetingController.greet()
```

Spring did **exactly** what `main` did in our Restaurant program — but **automatically**. It looked at the **constructor**, saw what was needed, and **gave** it. 💉✨

### 👀 Prove it!

Add one line to the constructor to **see** the injection happen:

```java
public GreetingController(GreetingService greetingService) {
    this.greetingService = greetingService;
    System.out.println("GreetingController got: " + greetingService);
}
```

Restart and look at the console. Between the log lines, you'll see:

```
... Root WebApplicationContext: initialization completed in 1745 ms
GreetingController got: com.example.hello.GreetingService@36a6bea6
... Tomcat started on port 8080 (http) with context path '/'
```

`com.example.hello.GreetingService@36a6bea6` is the **object** that Spring created and injected. (`@36a6bea6` is a code for this one object — yours will be different. Chapter 18.) It happens **before** Tomcat starts: first Spring builds and connects everything, **then** it opens the door. 🚪

(You can delete the `println` line now.)

---

## 💉 Part 6: Three ways to inject

Spring can inject dependencies in **three** ways. You'll see all three on the internet, so you should know them. But you should **use** only one. 😉

### 1️⃣ Constructor injection ✅ (the best — use this!)

```java
@RestController
public class GreetingController {

    private final GreetingService greetingService;

    public GreetingController(GreetingService greetingService) {
        this.greetingService = greetingService;
    }
}
```

What you just did. ⭐

### 2️⃣ Field injection with `@Autowired` ⚠️ (old style, not recommended)

```java
import org.springframework.beans.factory.annotation.Autowired;

@RestController
public class GreetingController {

    @Autowired
    private GreetingService greetingService;
}
```

| Code | Meaning |
|---|---|
| `@Autowired` | "Spring, **automatically wire** (connect) a bean into this field." |
| `private GreetingService greetingService;` | No constructor! Spring puts the bean **directly** into the private field (using reflection — Chapter 38). |

It's **shorter**, and it works (we tested it). That's why you see it in many old tutorials. But it has problems:

- ❌ The field **can't be `final`**, so the code could change it by mistake.
- ❌ Without Spring (for example, in a simple test), you **can't** give it a value. The field stays `null` → `NullPointerException` (Chapter 33). 💥
- ❌ You can't **see** what a class needs by looking at its constructor.

### 3️⃣ Setter injection (rare)

```java
@Autowired
public void setGreetingService(GreetingService greetingService) {
    this.greetingService = greetingService;
}
```

Spring calls the **setter** (Chapter 21). Only used in special cases (when a dependency is **optional**). You'll rarely need it.

### 🏆 Why constructor injection wins

| | Constructor ✅ | Field `@Autowired` ⚠️ | Setter |
|---|---|---|---|
| Can use `final` | ✅ yes | ❌ no | ❌ no |
| Works without Spring (e.g. tests) | ✅ `new GreetingController(fakeService)` | ❌ field stays `null` | ⚠️ must remember to call it |
| Shows what the class needs | ✅ in the constructor | ❌ hidden in fields | ❌ hidden in methods |
| Recommended by the Spring team | ✅ **yes** | ❌ | only for optional things |

### 🤔 Where is `@Autowired` in constructor injection?

You may see this in other code:

```java
@Autowired                                  // ← not needed!
public GreetingController(GreetingService greetingService) { ... }
```

If a class has **only one constructor**, Spring **automatically** uses it for injection. So `@Autowired` is **not needed** there. ✅ Less code, same result. (With **two or more** constructors, you must put `@Autowired` on the one Spring should use. But that's rare.)

> 💡 **Rule for this book:** Always use **constructor injection**. Fields are **`private final`**. No `@Autowired`. 🥇

---

## 🔌 Part 7: DI + interfaces = swap parts like LEGO

Here's the **real superpower**. 🦸 Remember **Chapter 25**? `MessageSender` was an interface, with `EmailSender` and `SmsSender`. Let's do it in Spring!

### Step 1: The interface

**`MessageSender.java`**

```java
package com.example.hello;

public interface MessageSender {
    String send(String to, String text);
}
```

### Step 2: Two implementations

**`EmailSender.java`**

```java
package com.example.hello;

import org.springframework.stereotype.Component;

@Component
public class EmailSender implements MessageSender {

    @Override
    public String send(String to, String text) {
        return "📧 Email to " + to + ": " + text;
    }
}
```

**`SmsSender.java`** — ⚠️ **without** `@Component` for now:

```java
package com.example.hello;

public class SmsSender implements MessageSender {

    @Override
    public String send(String to, String text) {
        return "📱 SMS to " + to + ": " + text;
    }
}
```

| Code | Meaning |
|---|---|
| `@Component` | "Spring, make a bean of this class." It's the **general** label. (`@Service` is a special kind of `@Component` — Chapter 54.) |
| `implements MessageSender` | This class **keeps the promise** of the interface (Chapter 25). |
| `SmsSender` **without** a label | Spring **ignores** it. No bean is created. |

### Step 3: The controller asks for the **interface**

**`NotifyController.java`**

```java
package com.example.hello;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NotifyController {

    private final MessageSender sender;

    public NotifyController(MessageSender sender) {
        this.sender = sender;
    }

    @GetMapping("/notify")
    public String notifyUser() {
        return sender.send("Sara", "Your book is ready");
    }
}
```

| Code | Meaning |
|---|---|
| `private final MessageSender sender;` | ⭐ The type is the **interface**, not `EmailSender`! |
| `public NotifyController(MessageSender sender)` | "Give me **any** `MessageSender`. I don't care which." |
| `sender.send(...)` | Use it. The controller doesn't know if it's email or SMS. 🙈 |

Restart → `http://localhost:8080/notify`:

```
📧 Email to Sara: Your book is ready
```

Spring looked for a bean that **is a** `MessageSender`. It found **one**: `EmailSender`. So it injected that. ✅

### Step 4: Swap! 🔄

Now **move** the `@Component` label: **remove** it from `EmailSender`, and **add** it to `SmsSender`. (Don't forget the import in `SmsSender`.)

Restart → `http://localhost:8080/notify`:

```
📱 SMS to Sara: Your book is ready
```

🤯 **The controller didn't change at all!** Not one letter. You swapped the whole way of sending messages by **moving one label**. That's **loose coupling** 🔌 + **Dependency Injection** 💉. This is why Spring apps are so easy to change and test.

```
     NotifyController ──needs──► «interface» MessageSender
                                       ▲            ▲
                                       │            │
                                 EmailSender     SmsSender
                                 (@Component?)   (@Component?)
                                       └─── Spring injects the one with the label
```

### ⚠️ What if **both** have `@Component`?

Put `@Component` on **both** classes and restart. 💥 The app **doesn't start**:

```
***************************
APPLICATION FAILED TO START
***************************

Description:

Parameter 0 of constructor in com.example.hello.NotifyController required a single bean, but 2 were found:
	- emailSender: defined in file [C:\...\hello\target\classes\com\example\hello\EmailSender.class]
	- smsSender: defined in file [C:\...\hello\target\classes\com\example\hello\SmsSender.class]

This may be due to missing parameter name information

Action:

Consider marking one of the beans as @Primary, updating the consumer to accept multiple beans, or using @Qualifier to identify the bean that should be consumed

Ensure that your compiler is configured to use the '-parameters' flag.
You may need to update both your build tool settings as well as your IDE.
(See https://github.com/spring-projects/spring-framework/wiki/Spring-Framework-6.1-Release-Notes#parameter-name-retention)
```

Let's read it like Chapter 51 taught us — **Description** and **Action**:

| Part | Meaning |
|---|---|
| `Parameter 0 of constructor in ...NotifyController` | "The **first** parameter (counting from 0!) of `NotifyController`'s constructor..." |
| `required a single bean, but 2 were found` | "...needs **one** `MessageSender`, but I have **two**! Which one?! 😵" |
| `- emailSender` / `- smsSender` | The two candidates (bean names = class names starting with a small letter). |
| `This may be due to missing parameter name information` | A hint for a rare special case. You can ignore it here — and also the last three lines about `-parameters`. |
| **Action:** `@Primary` ... `@Qualifier` | ⭐ The ways to fix it! We'll learn `@Primary` and `@Qualifier` in **Chapter 54**. |

For now, remove `@Component` from one of them again, so the app starts. ✅

---

## 💻 Mini project: The Joke API 😂 (Controller → Service → Repository)

Real Spring Boot apps have **three layers** (more in Chapter 63):

```
  🌐 Request
      │
      ▼
  ┌──────────────────┐
  │ JokeController   │  @RestController — talks HTTP (the waiter 🧑‍🍳)
  └────────┬─────────┘
           │ needs
           ▼
  ┌──────────────────┐
  │ JokeService      │  @Service — the logic: pick a random joke (the chef 👨‍🍳)
  └────────┬─────────┘
           │ needs
           ▼
  ┌──────────────────┐
  │ JokeRepository   │  @Repository — keeps the data (the fridge 🧊)
  └──────────────────┘
```

Each layer gets the one below it through **constructor injection**. 💉💉

### Step 1: The repository — where the data lives

**`JokeRepository.java`**

```java
package com.example.hello;

import java.util.List;

import org.springframework.stereotype.Repository;

@Repository
public class JokeRepository {

    private final List<String> jokes = List.of(
            "Why do Java developers wear glasses? Because they don't C#!",
            "Why was the computer cold? It left its Windows open!",
            "Why did the bean go to school? To become a Spring bean!");

    public List<String> findAll() {
        return jokes;
    }
}
```

| Code | Meaning |
|---|---|
| `@Repository` | "Spring, this class **stores and finds data**. Make a bean of it." (Another kind of `@Component` — Chapter 54.) |
| `private final List<String> jokes = List.of(...)` | Our "data": 3 jokes in a list. (In **Part 9**, data will come from a real **database**. The rest of the app won't even notice the change — thanks to layers! 😎) |
| `public List<String> findAll()` | "Give me all jokes." (`findAll` is the usual name for this in Spring — you'll see it again in Chapter 72.) |

> 😄 "They don't **C#**" sounds like "they don't **see sharp**". C# is another programming language!

### Step 2: The service — the logic

**`JokeService.java`**

```java
package com.example.hello;

import java.util.List;
import java.util.Random;

import org.springframework.stereotype.Service;

@Service
public class JokeService {

    private final JokeRepository jokeRepository;
    private final Random random = new Random();

    public JokeService(JokeRepository jokeRepository) {
        this.jokeRepository = jokeRepository;
    }

    public String randomJoke() {
        List<String> jokes = jokeRepository.findAll();
        int index = random.nextInt(jokes.size());
        return jokes.get(index);
    }

    public int countJokes() {
        return jokeRepository.findAll().size();
    }
}
```

| Code | Meaning |
|---|---|
| `@Service` | A service bean. |
| `private final JokeRepository jokeRepository;` | The service **needs** the repository. |
| `private final Random random = new Random();` | A random number maker. (Using `new` for a simple Java helper like `Random` is OK here. In Chapter 54 you'll see how to make it a bean too.) |
| `public JokeService(JokeRepository jokeRepository)` | 💉 Constructor injection: Spring gives the repository. |
| `jokeRepository.findAll()` | Get all jokes from the "fridge". |
| `random.nextInt(jokes.size())` | A random **index**: 0, 1 or 2 (Chapter 14 — indexes start at 0). |
| `jokes.get(index)` | The joke at that index. |
| `countJokes()` | How many jokes are there? |

### Step 3: The controller — HTTP

**`JokeController.java`**

```java
package com.example.hello;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class JokeController {

    private final JokeService jokeService;

    public JokeController(JokeService jokeService) {
        this.jokeService = jokeService;
    }

    @GetMapping("/joke")
    public String joke() {
        return jokeService.randomJoke();
    }

    @GetMapping("/jokes/count")
    public String count() {
        return "I know " + jokeService.countJokes() + " jokes.";
    }
}
```

| Code | Meaning |
|---|---|
| `private final JokeService jokeService;` | The controller **needs** the service. It does **not** know about the repository! |
| `public JokeController(JokeService jokeService)` | 💉 Constructor injection. |
| `jokeService.randomJoke()` | Ask the service. The controller just passes the answer to the client. |

### Step 4: Restart and test

Real answers from our test run:

```
curl http://localhost:8080/joke
Why did the bean go to school? To become a Spring bean!

curl http://localhost:8080/joke
Why did the bean go to school? To become a Spring bean!

curl http://localhost:8080/joke
Why was the computer cold? It left its Windows open!

curl http://localhost:8080/jokes/count
I know 3 jokes.
```

(The jokes are random, so yours will come in a different order. 🎲 Sometimes the same joke comes twice — that's random too!)

### 🔬 What Spring did

Spring figured out the **order** all by itself:

```
 1. JokeRepository needs nothing         → create it first        🫘
 2. JokeService needs a JokeRepository   → create it, inject 💉    🫘
 3. JokeController needs a JokeService   → create it, inject 💉    🫘
```

This is **exactly** the "assembler" (`main`) from our Restaurant program — but you didn't write it! 🎉

---

## ✋ Try it yourself

**Task 1:** Add a 4th joke to `JokeRepository`. Restart. What does `/jokes/count` say now? Did you have to change the service or controller?

<details>
<summary>Click to see the answer</summary>

`I know 4 jokes.` — and **no**, you changed only the repository. The other layers didn't need to know. That's the beauty of layers! 🎂

</details>

**Task 2:** Make a `MathService` (with `@Service`) that has a method `int square(int n)` returning `n * n`. Then make a `MathController` with `GET /square` that uses it to return the square of **7**.

<details>
<summary>Click to see the answer</summary>

```java
package com.example.hello;

import org.springframework.stereotype.Service;

@Service
public class MathService {

    public int square(int n) {
        return n * n;
    }
}
```

```java
package com.example.hello;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MathController {

    private final MathService mathService;

    public MathController(MathService mathService) {
        this.mathService = mathService;
    }

    @GetMapping("/square")
    public String square() {
        return "7 x 7 = " + mathService.square(7);
    }
}
```

Answer: `7 x 7 = 49`. (In Chapter 59 you'll learn to send **any** number, like `/square?n=12`!)

</details>

**Task 3:** In the Restaurant program (plain Java), make an `interface Oven` with two classes: `WoodOven` and `ElectricOven`. Change `main` so the chef uses an `ElectricOven`. Which classes did you have to change to swap ovens?

<details>
<summary>Click to see the answer</summary>

```java
interface Oven {
    String bake(String food);
}

class WoodOven implements Oven {
    public String bake(String food) {
        return food + " baked in a wood oven 🪵";
    }
}

class ElectricOven implements Oven {
    public String bake(String food) {
        return food + " baked in an electric oven ⚡";
    }
}
```

In `main`:

```java
Oven oven = new ElectricOven();
Chef chef = new Chef(oven);
```

To swap ovens, you change **only `main`** (the assembler). `Chef` and `Waiter` stay the **same**. 🔌 (`bake` must be `public` now, because methods from an interface are public — Chapter 25.)

</details>

**Task 4:** Change `JokeController` to use **field injection** with `@Autowired` instead of the constructor. Does it work? Then change it back. Why do we prefer the constructor?

<details>
<summary>Click to see the answer</summary>

```java
@Autowired
private JokeService jokeService;
```

(And delete the constructor. The field can't be `final` anymore.) It works. But we prefer the constructor because: the field can be `final`, the class can be created **without Spring** (for tests), and the constructor clearly **shows** what the class needs. Change it back! 😉

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `@Service` (or `@Component`) on the dependency

You wrote `GreetingService` but forgot the `@Service` label. The app doesn't start:

```
***************************
APPLICATION FAILED TO START
***************************

Description:

Parameter 0 of constructor in com.example.hello.GreetingController required a bean of type 'com.example.hello.GreetingService' that could not be found.


Action:

Consider defining a bean of type 'com.example.hello.GreetingService' in your configuration.
```

"`GreetingController` needs a `GreetingService`, but I don't **have** one!" 🤷 Spring only creates beans of classes with a **label**. **Fix:** Add `@Service` to `GreetingService`. (Also check: is it in the base package? Chapter 50!)

### Mistake 2: Creating the dependency yourself with `new`

```java
@RestController
public class JokeController {
    private final JokeService jokeService = new JokeService();   // ❌
}
```

Java says:

```
error: constructor JokeService in class JokeService cannot be applied to given types;
  required: JokeRepository
  found:    no arguments
```

Of course — `JokeService` needs a repository! So you'd write `new JokeService(new JokeRepository())`... and you're back to the **glued** world of Part 2. 🧲 Even when it compiles, your object is **not** the bean Spring made — it's a **second, separate** object that Spring doesn't know about. **Fix:** Never `new` your services, repositories or controllers. **Ask for them in the constructor.** 💉

### Mistake 3: `@Autowired` on a `final` field

```java
@Autowired
private final JokeService jokeService;    // ❌
```

```
error: variable jokeService not initialized in the default constructor
```

A `final` field **must** get its value in the constructor (Chapter 19). Field injection happens **after** the constructor — too late! **Fix:** Use **constructor injection** (and keep `final`). ✅

### Mistake 4: Two beans for one interface

`required a single bean, but 2 were found`. **Fix:** Keep the label on only one class — or learn `@Primary` and `@Qualifier` in Chapter 54.

### Mistake 5: A circle of dependencies 🐔🥚

```java
@Service
public class ChickenService {
    public ChickenService(EggService eggService) { ... }   // chicken needs egg
}

@Service
public class EggService {
    public EggService(ChickenService chickenService) { ... }   // egg needs chicken
}
```

Which comes first, the chicken or the egg? 🐔🥚 Spring can't decide either! We tested it:

```
***************************
APPLICATION FAILED TO START
***************************

Description:

The dependencies of some of the beans in the application context form a cycle:

┌─────┐
|  chickenService defined in file [C:\...\ChickenService.class]
↑     ↓
|  eggService defined in file [C:\...\EggService.class]
└─────┘


Action:

Relying upon circular references is discouraged and they are prohibited by default. Update your application to remove the dependency cycle between beans. As a last resort, it may be possible to break the cycle automatically by setting spring.main.allow-circular-references to true.
```

Spring even **draws** the circle for you! ↑↓ **Fix:** Change your design so dependencies go in **one direction** (Controller → Service → Repository, never back up). Often the shared part can be moved into a **third** class that both use. (Don't use the "last resort" setting. 🙅)

---

## ✅ Summary

- A **dependency** is something a class **needs** (a `Chef` needs an `Oven`).
- Creating dependencies with **`new` inside** a class **glues** classes together 🧲: hard to swap, hard to test, ugly chains.
- **Dependency Injection** 💉: a class **asks** for its dependencies (in its **constructor**), and **somebody else gives** them.
- In plain Java, **`main`** is the assembler. In Spring Boot, **Spring** is the assembler (**Inversion of Control**).
- Put **`@Service`**, **`@Component`**, **`@Repository`** or **`@RestController`** on a class → Spring makes a **bean** 🫘 → and injects it wherever a constructor asks for that type.
- ✅ Use **constructor injection**, with **`private final`** fields. With only one constructor, **no `@Autowired`** is needed.
- Ask for an **interface** → you can **swap** the implementation by moving one label 🔌.
- Two beans of the same type → `required a single bean, but 2 were found` (fix in Chapter 54).
- Typical chain: **Controller → Service → Repository**, each injected into the one above.

---

## ❓ Quiz

1. What is a dependency? Give an example.
2. What does "inject" mean?
3. Why is `private final Oven oven = new Oven();` inside `Chef` a problem? Give two reasons.
4. In plain Java, who is the "assembler"? And in Spring Boot?
5. What are the three kinds of injection? Which one should you use?
6. Why is `@Autowired` not needed on the constructor in our examples?
7. A controller asks for a `MessageSender` (interface). Only `SmsSender` has `@Component`. What gets injected?
8. What does `required a bean of type '...GreetingService' that could not be found` mean? How do you fix it?
9. What is wrong with `private final JokeService jokeService = new JokeService(new JokeRepository());` in a controller?
10. In what order does Spring create `JokeController`, `JokeService`, and `JokeRepository`? Why?

<details>
<summary>Click to see the answers</summary>

1. Something a class needs to do its job. Example: a `Chef` needs an `Oven`; a `JokeService` needs a `JokeRepository`.
2. To give it from outside (instead of the class creating it itself).
3. Any two: you can't swap the oven without changing `Chef`; you can't give a fake oven in tests; every chef makes its own oven (no sharing); long chains of `new` inside classes.
4. In plain Java: the `main` method (you). In Spring Boot: Spring (the container).
5. Constructor, field (`@Autowired` on a field), setter. Use **constructor** injection.
6. Because each class has only **one** constructor, and Spring automatically uses it.
7. `SmsSender` — it's the only `MessageSender` bean.
8. Spring has no bean of type `GreetingService`. Add `@Service` to the class (and make sure it's in the base package or below).
9. It glues the controller to the service and repository, and it creates **new** objects that are **not** Spring's beans. Use constructor injection instead.
10. `JokeRepository` first (it needs nothing), then `JokeService` (needs the repository), then `JokeController` (needs the service). Spring looks at the constructors to find the right order.

</details>

---

[⬅ Previous chapter](52-hello-endpoint.md) | [Table of Contents](../README.md) | [Next chapter: Beans: @Component, @Service, @Repository ➡](54-beans.md)
