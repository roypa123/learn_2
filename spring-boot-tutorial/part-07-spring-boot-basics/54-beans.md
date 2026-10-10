# Chapter 54 – Beans: @Component, @Service, @Repository

[⬅ Previous chapter](53-dependency-injection.md) | [Table of Contents](../README.md) | [Next chapter ➡](55-application-properties.md)

---

## 🎯 Goal

In Chapter 53 you used beans to do **Dependency Injection**. Now let's look at the beans themselves, up close. 🔍🫘

At the end of this chapter you will know:

- What a **bean** is, exactly, and where beans **live** (the container)
- The **labels** that make beans: `@Component`, `@Service`, `@Repository`, `@Controller`, `@RestController`, `@Configuration` — and **when** to use which 🏷️
- How beans get their **names**
- Why each bean is a **singleton** (only **one** object!) and what that means for you
- How to make beans from classes you **can't** label, with **`@Configuration`** + **`@Bean`**
- The **life of a bean**: born, ready, working, goodbye 👶➡️👴
- How to choose between **two** beans of the same type: **`@Primary`** and **`@Qualifier`** ⚖️

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Bean** 🫘 | An object that **Spring** created and **manages** (keeps, connects, and destroys at the end). |
| **Container / ApplicationContext** 🧸 | The "box" where Spring keeps all the beans. |
| **Stereotype annotation** | A label that says **what kind** of bean a class is: `@Service`, `@Repository`... ("Stereotype" = a typical role.) |
| **Bean name** | The bean's **name** in the container, like `greetingService`. |
| **Scope** | **How many** objects Spring makes for one bean. |
| **Singleton** | Scope "**only one**": one object, shared by everybody. (The default!) |
| **Prototype** | Scope "**new every time**": a new object each time someone asks. |
| **`@Configuration`** | A label: "This class has **bean recipes** inside." |
| **`@Bean`** | A label on a **method**: "What this method returns is a bean." |
| **Lifecycle** | The **life** of a bean: created → ready → used → destroyed. |
| **`@Primary`** | "If there are several beans of this type, **I'm** the main one." |
| **`@Qualifier`** | "I want **this exact** bean, by name." |

---

## 📖 Story: The school's supply cabinet 🗄️

A school has a big **supply cabinet**. Inside: **one** projector 📽️, **one** printer 🖨️, **one** first-aid kit 🩹... Every item has a **name tag**.

- When a teacher needs the projector, she doesn't buy a new one. She asks the **caretaker**: "Projector, please!" The caretaker gives her **the** projector from the cabinet. The next teacher gets the **same** projector. (**Singleton** — one object, shared! 📽️)
- Items have **labels** that say what kind they are: "📚 teaching", "🧹 cleaning", "🩹 safety". The caretaker uses the labels to **find** things. (**Stereotypes**: `@Service`, `@Repository`...)
- Some things come **from outside** in a box, like a ready-made microscope 🔬 from a shop. You can't put your own label on the factory parts... so the caretaker writes a **recipe card**: "Microscope: order it from the shop, put it in the cabinet." (**`@Configuration` + `@Bean`**)
- There are **two** printers: a color one 🌈 and a black-and-white one. If a teacher just says "printer!", the caretaker gives the **main** one — the one with a ⭐ (**`@Primary`**). If she says "the **color** printer!", she gets that one (**`@Qualifier`**).
- But **pencils** ✏️ are different: every student gets a **new** one. (**Prototype**.)

In Spring: the cabinet is the **container** 🧸, the items are **beans** 🫘, and the caretaker is **Spring**. 🌱

---

## 🫘 Part 1: What exactly is a bean?

A **bean** is a normal Java object, with one difference: **Spring** created it, and **Spring** takes care of it.

| | Normal object | Bean 🫘 |
|---|---|---|
| Who creates it? | **You**, with `new` | **Spring** |
| Who gives it its dependencies? | **You** | **Spring** (DI — Chapter 53) |
| How many? | As many as you create | Usually **one** (singleton) |
| Where does it live? | In a variable | In the **container** 🧸 |
| Who destroys it at the end? | Java's garbage collector (Chapter 18) | **Spring** first says goodbye, then Java cleans it up |

Example: `GreetingService` with `@Service` → Spring makes **one** `GreetingService` object at startup → that object is a **bean**.

> 💡 **Not everything is a bean!** Records like `Student` and `Teacher` (Chapter 52) are **not** beans. You create **many** of them with `new`, and that's correct. **Beans** are for the **workers** of your app (controllers, services, repositories). **Data objects** are created with `new`. 👷 vs 📦

---

## 🏷️ Part 2: The labels — stereotype annotations

You've already used several labels. Here they all are, in one table:

| Label | Use it for | Layer | Example |
|---|---|---|---|
| **`@Component`** | Any helper class. The **general** label. | any | `VisitCounter`, `EmailSender` |
| **`@Service`** | **Business logic** — the real "work". | Service layer | `GreetingService`, `JokeService` |
| **`@Repository`** | Classes that **store and find data**. | Data layer | `JokeRepository` |
| **`@Controller`** | Web controllers that return **HTML pages** (Chapter 89). | Web layer | — |
| **`@RestController`** | Web controllers that return **data** (text/JSON). | Web layer | `HelloController`, `JokeController` |
| **`@Configuration`** | Classes with **bean recipes** (`@Bean` methods). | setup | `AppConfig` (Part 6) |

### 🤫 A secret: they're all `@Component`!

Hold **Ctrl** and click on `@Service` in IntelliJ. You'll see (simplified):

```java
@Component
public @interface Service {
    ...
}
```

`@Service` **has `@Component` on it**! The same is true for `@Repository`, `@Controller`, and `@Configuration`. And `@RestController` has `@Controller` on it (which has `@Component`). 🪆

```
                          @Component
          ┌──────────────┬────┴─────┬────────────────┐
      @Service      @Repository  @Controller   @Configuration
                                     │
                              @RestController
```

So for Spring's **component scan**, they're all the **same**: "make a bean of this class". 🫘

### 🤔 Then why different names?

1. **For humans** 👀: When you see `@Repository`, you know immediately: "This class works with data." It makes the code **easier to read**.
2. **A few extra powers** ⚡:
   - `@RestController` → the methods' return values become the **response body** (Chapter 52).
   - `@Repository` → database errors are turned into **Spring's** error types (useful in Part 9).
   - `@Configuration` → its `@Bean` methods are special (Part 6).

> 💡 **Rule:** Use the **most specific** label. Logic → `@Service`. Data → `@Repository`. REST → `@RestController`. Anything else → `@Component`.

---

## 🔍 Part 3: Look inside the container!

Let's **open** the cabinet and look at the beans. 👀

`SpringApplication.run(...)` **returns** the container! Change your `HelloApplication` like this:

```java
package com.example.hello;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

@SpringBootApplication
public class HelloApplication {

    public static void main(String[] args) {
        ApplicationContext context = SpringApplication.run(HelloApplication.class, args);

        GreetingService first = context.getBean(GreetingService.class);
        GreetingService second = context.getBean(GreetingService.class);
        System.out.println("Same object? " + (first == second));
        System.out.println("Number of beans: " + context.getBeanDefinitionCount());
        System.out.println("Has bean 'greetingService'? " + context.containsBean("greetingService"));
        System.out.println("Has bean 'GreetingService'? " + context.containsBean("GreetingService"));
    }
}
```

Restart. After `Started HelloApplication...`, you'll see:

```
Same object? true
Number of beans: 168
Has bean 'greetingService'? true
Has bean 'GreetingService'? false
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `import org.springframework.context.ApplicationContext;` | The type of the container. |
| `ApplicationContext context = SpringApplication.run(...)` | `run` gives back the **container** 🧸. We keep it in a variable. |
| `context.getBean(GreetingService.class)` | "Container, give me the bean of type `GreetingService`!" (`.class` — Chapter 38.) |
| `first == second` | Are they the **same object**? (`==` on objects checks "same object?" — Chapter 9.) |
| `Same object? true` | ⭐ **Yes!** Asking twice gives the **same** bean. Singleton! 📽️ |
| `context.getBeanDefinitionCount()` | How many beans are in the container? |
| `Number of beans: 168` | 😮 **168?!** You only made about 15! The rest were made by **Spring Boot's auto-configuration**: Tomcat, Jackson, DispatcherServlet... (Your number will be different. That's fine.) |
| `context.containsBean("greetingService")` | Is there a bean with **this name**? |
| `true` for `greetingService`, `false` for `GreetingService` | The bean name starts with a **small** letter! (Part 4) |

> ⚠️ **This is only for learning!** In real code, you **never** call `getBean(...)` yourself — you use **constructor injection** (Chapter 53). Delete these lines after you've tried them, and change `main` back to the one line. 🧹

---

## 📛 Part 4: Bean names

Every bean has a **name**. Spring makes it from the class name: **first letter small**.

| Class | Bean name |
|---|---|
| `GreetingService` | `greetingService` |
| `JokeRepository` | `jokeRepository` |
| `EmailSender` | `emailSender` |
| `HelloController` | `helloController` |

You saw these names in error messages already (`emailSender`, `smsSender` in Chapter 53). 👀

You can choose **your own** name, in the label:

```java
@Service("greeter")
public class GreetingService { ... }
```

Now the bean is called `greeter`. (You'll rarely need this. The name matters mostly for **`@Qualifier`** — Part 8.)

---

## 📽️ Part 5: Singletons — one object for everybody

By default, every bean is a **singleton**: Spring makes **exactly one** object, and gives that **same** object to **everyone** who asks. (You learned the singleton idea in **Chapter 27**. Spring does it **for you**!)

Let's **see** it with a visit counter. 🔢

### Step 1: The counter (one bean)

**`VisitCounter.java`**

```java
package com.example.hello;

import org.springframework.stereotype.Component;

@Component
public class VisitCounter {

    private int count = 0;

    public int addVisit() {
        count++;
        return count;
    }
}
```

### Step 2: Two controllers that use it

**`VisitController.java`**

```java
package com.example.hello;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class VisitController {

    private final VisitCounter counter;

    public VisitController(VisitCounter counter) {
        this.counter = counter;
    }

    @GetMapping("/visit")
    public String visit() {
        return "You are visitor number " + counter.addVisit();
    }
}
```

**`StatsController.java`**

```java
package com.example.hello;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StatsController {

    private final VisitCounter counter;

    public StatsController(VisitCounter counter) {
        this.counter = counter;
    }

    @GetMapping("/stats")
    public String stats() {
        return "Stats page. Visits so far (this one too): " + counter.addVisit();
    }
}
```

### Step 3: Restart and visit — in this order

| # | Request | Real answer |
|---|---|---|
| 1 | `GET /visit` | `You are visitor number 1` |
| 2 | `GET /visit` | `You are visitor number 2` |
| 3 | `GET /stats` | `Stats page. Visits so far (this one too): 3` |
| 4 | `GET /visit` | `You are visitor number 4` |

😮 Look at request **3** and **4**! `/stats` said **3**, and then `/visit` said **4**. Both controllers use the **same** `VisitCounter` object. If there were **two** counters, `/stats` would say **1**.

```
 VisitController ─────┐
                      ├────► 🫘 VisitCounter (count = 4)   ← ONE object!
 StatsController ─────┘
```

### 🔍 What this means

1. ✅ **Good:** Spring makes only **one** object per bean. Fast and saves memory, even with **thousands** of requests.
2. ✅ **Good:** Beans can **share** things — like this counter.
3. ⚠️ **Careful:** **All users** share that one object! If user A and user B visit at the **same moment**, both change `count` at the same time. In rare cases, the number can be wrong. 😬

> ⚠️ **Rule for beans:** Don't keep **changing data** in fields of a bean (like `count++`) in real apps. Keep **user data** in a **database** (Part 9), not in bean fields. Fields in beans should be **dependencies** (like `private final JokeService jokeService`) or **fixed** values. Our counter is OK for **learning**. (For a counter in a real app, Java has a special safe class: `AtomicInteger`.)

### 🎟️ The other scope: prototype (new every time)

Rarely, you **want** a new object each time. Then add `@Scope("prototype")`:

```java
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

@Component
@Scope("prototype")
public class Ticket {

    public Ticket() {
        System.out.println("A new Ticket was made!");
    }
}
```

If you ask the container twice (like in Part 3), you get:

```
A new Ticket was made!
A new Ticket was made!
Same ticket? false
```

Two **different** tickets. 🎟️🎟️ (You'll almost never need this. **Singleton** is right 99% of the time.)

| Scope | How many objects? | Like... |
|---|---|---|
| **singleton** (default) | **One**, shared | The school's projector 📽️ |
| **prototype** | **New** each time it's asked for | Pencils for each student ✏️ |

---

## 🍳 Part 6: `@Configuration` + `@Bean` — recipes for other people's classes

Labels like `@Component` only work on **your own** classes. But what about classes from **Java** or **libraries**, like `Random`, `Clock`, or `Gson`? You can't open `java.util.Random` and type `@Component` on it! 🔒

**Solution:** write a **recipe** 📜. A method that **creates** the object, with **`@Bean`** on it, inside a class with **`@Configuration`**.

### Step 1: The recipe class

**`AppConfig.java`**

```java
package com.example.hello;

import java.util.Random;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {

    @Bean
    public Random random() {
        return new Random();
    }
}
```

| Code | Meaning |
|---|---|
| `@Configuration` | "Spring, this class has **bean recipes** inside." (It's also a `@Component`, so it's found by the scan.) |
| `@Bean` | ⭐ "Call this method **once** at startup. Whatever it returns becomes a **bean**." 🫘 |
| `public Random random()` | The method. Its **name** (`random`) becomes the **bean name**. Its **return type** (`Random`) is the bean's type. |
| `return new Random();` | Here, **you** use `new` — once, inside the recipe. That's allowed! Spring calls this method and keeps the result. |

### Step 2: Inject it like any other bean

**`DiceController.java`**

```java
package com.example.hello;

import java.util.Random;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DiceController {

    private final Random random;

    public DiceController(Random random) {
        this.random = random;
    }

    @GetMapping("/dice")
    public String roll() {
        int number = random.nextInt(1, 7);
        return "You rolled a " + number;
    }
}
```

`GET /dice` → `You rolled a 6` → `You rolled a 4` → ... 🎲

The controller asks for a `Random` in its constructor, and Spring gives the bean from the recipe. 💉 (In Chapter 52, Task 2, `DiceController` made its own `new Random()`. Now it **receives** one. In tests, you could give it a "fake random" that always returns 6! 😎)

### 🤔 When do I use `@Bean` instead of `@Component`?

| Situation | Use |
|---|---|
| **Your own** class | `@Component` / `@Service` / `@Repository` on the class ✅ |
| A class from **Java** or a **library** (you can't change it) | `@Bean` method in a `@Configuration` class ✅ |
| Creating the object needs **special settings** | `@Bean` method (you can write any code in it) |

You'll see `@Bean` a lot in **Spring Security** (Part 10) — for example, a `@Bean` that makes a `PasswordEncoder`. 🔒

---

## 👶➡️👴 Part 7: The life of a bean

Every bean lives through the **same steps**:

```
 1. 👶 Created      Spring calls the constructor (with dependencies injected 💉)
 2. ✅ Ready         Spring calls the @PostConstruct method (if there is one)
 3. 💼 Working       The app runs; the bean answers requests... for hours, days, months
 4. 👋 Goodbye       The app stops; Spring calls the @PreDestroy method (if there is one)
```

You can **hook into** steps 2 and 4 with two labels. Let's add them to `VisitCounter`:

```java
package com.example.hello;

import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import org.springframework.stereotype.Component;

@Component
public class VisitCounter {

    private int count = 0;

    public VisitCounter() {
        System.out.println("1. VisitCounter constructor");
    }

    @PostConstruct
    public void ready() {
        System.out.println("2. VisitCounter is ready");
    }

    public int addVisit() {
        count++;
        return count;
    }

    @PreDestroy
    public void goodbye() {
        System.out.println("3. VisitCounter says goodbye. Total visits: " + count);
    }
}
```

| Code | Meaning |
|---|---|
| `import jakarta.annotation.PostConstruct;` | `@PostConstruct` comes from **Jakarta** (the standard for Java server apps), not from Spring. It's included in the web starter. |
| `@PostConstruct` | "Call this method **after** the bean is created and **all** its dependencies are injected." ("Post" = after, "construct" = build.) |
| `@PreDestroy` | "Call this method **before** the bean is destroyed, when the app stops." ("Pre" = before.) |

Restart. During startup:

```
1. VisitCounter constructor
2. VisitCounter is ready
... Tomcat started on port 8080 (http) with context path '/'
```

Visit `/visit` once, then **stop** the app (⏹️). At the end:

```
... Commencing graceful shutdown. Waiting for active requests to complete
... Graceful shutdown complete
3. VisitCounter says goodbye. Total visits: 1
```

### 🤔 When do I need these?

| Label | Use it for | Example |
|---|---|---|
| `@PostConstruct` | Work to do **once** at the start, after all dependencies are there | Load some data, check settings, print "ready" |
| `@PreDestroy` | Cleaning up at the end | Close a file, say goodbye to another server |

You won't need them often. But now you know what they mean when you see them! 🤓

> 💡 Note: when you stop the app very **hard** (for example, "kill" the process), `@PreDestroy` may **not** run. The red square ⏹️ in IntelliJ usually stops it nicely.

---

## ⚖️ Part 8: Two beans, one type — `@Primary` and `@Qualifier`

In Chapter 53, you got this error when both `EmailSender` and `SmsSender` had `@Component`:

```
Parameter 0 of constructor in com.example.hello.NotifyController required a single bean, but 2 were found:
	- emailSender: ...
	- smsSender: ...
```

and the **Action** said: "Consider marking one of the beans as **@Primary**, updating the consumer to accept **multiple beans**, or using **@Qualifier**...". Let's learn all three fixes! 🔧

### Fix 1: `@Primary` — "I'm the main one" ⭐

```java
package com.example.hello;

import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

@Component
@Primary
public class EmailSender implements MessageSender {

    @Override
    public String send(String to, String text) {
        return "📧 Email to " + to + ": " + text;
    }
}
```

| Code | Meaning |
|---|---|
| `@Primary` | "If someone asks for a `MessageSender` and doesn't say **which**, give them **me**." ⭐ |

Now **both** classes can have `@Component`. When a constructor asks for **a** `MessageSender`, Spring gives the **primary** one: `EmailSender`. ✅

### Fix 2: `@Qualifier` — "I want **that** one" 🎯

Sometimes, one class needs a **specific** bean. Use `@Qualifier` with the **bean name**:

```java
package com.example.hello;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NotifyController {

    private final MessageSender mainSender;
    private final MessageSender smsSender;

    public NotifyController(MessageSender mainSender,
                            @Qualifier("smsSender") MessageSender smsSender) {
        this.mainSender = mainSender;
        this.smsSender = smsSender;
    }

    @GetMapping("/notify")
    public String notifyUser() {
        return mainSender.send("Sara", "Your book is ready")
                + " | " + smsSender.send("Sara", "Your book is ready");
    }
}
```

| Code | Meaning |
|---|---|
| `MessageSender mainSender` | No qualifier → Spring gives the **`@Primary`** one: `EmailSender`. |
| `@Qualifier("smsSender") MessageSender smsSender` | ⭐ "For **this** parameter, give me the bean **named** `smsSender`." (Bean name = class name with a small first letter — Part 4.) |
| `+ " \| " +` | Join the two answers with a `|` between them. |

Restart → `GET /notify`:

```
📧 Email to Sara: Your book is ready | 📱 SMS to Sara: Your book is ready
```

The first came from the **primary** (email), the second from the **qualifier** (SMS). 🎯

### Fix 3: Ask for **all** of them — `List<...>` 📋

Sometimes you want **every** bean of a type. Just ask for a **`List`**!

**`AllSendersController.java`**

```java
package com.example.hello;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AllSendersController {

    private final List<MessageSender> senders;

    public AllSendersController(List<MessageSender> senders) {
        this.senders = senders;
    }

    @GetMapping("/notify-all")
    public List<String> notifyEverybody() {
        return senders.stream()
                .map(sender -> sender.send("Tom", "School starts at 8"))
                .toList();
    }
}
```

| Code | Meaning |
|---|---|
| `List<MessageSender> senders` | ⭐ "Give me **all** beans that are `MessageSender`s, in a list." Spring collects them for you! |
| `senders.stream()` | Go through all senders (Chapter 36). |
| `.map(sender -> sender.send(...))` | Let each sender send the message, and keep the result text. (A lambda — Chapter 35.) |
| `.toList()` | Collect the texts into a list → a JSON array. |

`GET /notify-all`:

```json
["📧 Email to Tom: School starts at 8","📱 SMS to Tom: School starts at 8"]
```

Both senders were used! 📧📱 Add a third sender class (with `@Component`) — like `PigeonSender` 🐦 — and it's **automatically** in the list. You don't change the controller at all. 🤯

### 📋 Which fix when?

| Situation | Fix |
|---|---|
| One implementation is **normally** used | `@Primary` on it ⭐ |
| One class needs a **specific** other one | `@Qualifier("beanName")` on the parameter 🎯 |
| You want to use **all** of them | Ask for `List<TheInterface>` 📋 |

---

## 💻 Mini project: The bean detective 🕵️

Let's put it **all** together. Make sure your project has these classes (from this chapter and Chapter 53):

- `MessageSender` (interface), `EmailSender` (`@Component @Primary`), `SmsSender` (`@Component`)
- `NotifyController` (with `@Qualifier`), `AllSendersController` (with `List`)
- `VisitCounter` (with `@PostConstruct`/`@PreDestroy`), `VisitController`, `StatsController`
- `AppConfig` (with `@Bean Random`), `DiceController`

Now be a detective 🕵️ and answer **before** you test! Then test with curl or the browser.

1. 🔎 What will `/notify` return?
2. 🔎 You add a new class `PigeonSender implements MessageSender` with `@Component` that returns `"🐦 Pigeon to " + to + ": " + text`. What does `/notify-all` return now?
3. 🔎 You restart the app. You visit `/stats` first. What number does it show?
4. 🔎 You put `@Primary` on **both** `EmailSender` and `SmsSender`. What happens?
5. 🔎 You change `@Qualifier("smsSender")` to `@Qualifier("smsSendr")` (a typo). What happens?

<details>
<summary>Click to see the answers</summary>

1. `📧 Email to Sara: Your book is ready | 📱 SMS to Sara: Your book is ready`

2. Three items now (the order can be different):
   ```json
   ["📧 Email to Tom: School starts at 8","🐦 Pigeon to Tom: School starts at 8","📱 SMS to Tom: School starts at 8"]
   ```

3. `Stats page. Visits so far (this one too): 1` — after a restart, Spring creates a **new** `VisitCounter`, so the count starts again from 0. (Data in bean fields is **lost** on restart. That's another reason to use a database! 🗄️)

4. The app doesn't start. Two "main ones" is like no main one — Spring can't choose. In the long error text, you find:
   ```
   more than one 'primary' bean found among candidates: [emailSender, smsSender]
   ```

5. The app doesn't start. We tested it:
   ```
   Description:

   Parameter 1 of constructor in com.example.hello.NotifyController required a bean of type 'com.example.hello.MessageSender' that could not be found.

   The injection point has the following annotations:
   	- @org.springframework.beans.factory.annotation.Qualifier("smsSendr")

   The following candidates were found but could not be injected:
   	- User-defined bean
   	- User-defined bean
   ```
   "**Parameter 1**" = the **second** parameter (counting from 0). Spring found two `MessageSender` beans, but **none** is named `smsSendr`. Check the spelling! 🔤

</details>

---

## ✋ Try it yourself

**Task 1:** Add a `@Bean` method to `AppConfig` that creates a `java.time.Clock`: `Clock.systemDefaultZone()`. Then make a `ClockController` with `GET /now` that uses the injected `Clock` and returns `LocalTime.now(clock).withNano(0)` as text.

<details>
<summary>Click to see the answer</summary>

In `AppConfig` (add `import java.time.Clock;`):

```java
@Bean
public Clock clock() {
    return Clock.systemDefaultZone();
}
```

```java
package com.example.hello;

import java.time.Clock;
import java.time.LocalTime;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ClockController {

    private final Clock clock;

    public ClockController(Clock clock) {
        this.clock = clock;
    }

    @GetMapping("/now")
    public String now() {
        return "Now: " + LocalTime.now(clock).withNano(0);
    }
}
```

Why inject a `Clock`? In tests, you can give a **fixed** clock that always says "8:00", so your tests are always the same. ⏰ (Professional trick! 😎)

</details>

**Task 2:** Which label would you use for each class?

a) `OrderService` — calculates prices and discounts
b) `ProductRepository` — saves and finds products
c) `ProductController` — REST API for products
d) `PriceFormatter` — turns `12.5` into `"$12.50"`
e) A class with a `@Bean` method that makes a `Gson` object

<details>
<summary>Click to see the answer</summary>

a) `@Service` b) `@Repository` c) `@RestController` d) `@Component` (a general helper) e) `@Configuration`

</details>

**Task 3:** Remove `@Primary` from `EmailSender`, and add it to `SmsSender` instead. What does `/notify` return now? Why?

<details>
<summary>Click to see the answer</summary>

```
📱 SMS to Sara: Your book is ready | 📱 SMS to Sara: Your book is ready
```

Now **SMS** is the primary one, so `mainSender` is SMS too. And `smsSender` (with the qualifier) is also SMS. Both parts are SMS! 📱📱

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Thinking every class should be a bean

Putting `@Component` on **records** like `Student` or `Teacher`. ❌ They're **data**, not workers. You need **many** different students, not one shared student! **Fix:** Beans for **workers** (controllers, services, repositories, helpers). `new` for **data**.

### Mistake 2: Keeping user data in bean fields

```java
@Service
public class CartService {
    private List<String> items = new ArrayList<>();   // ❌ shared by ALL users!
}
```

User A adds "apple" 🍎 to their cart... and user B sees it in **their** cart! 😱 (Singleton = **one** object for everybody.) **Fix:** Keep user data in a **database** (Part 9), or pass it in method parameters.

### Mistake 3: Calling `getBean(...)` everywhere

`context.getBean(...)` was for **looking** inside the container. In real code, it hides what a class needs and makes testing harder. **Fix:** Use **constructor injection**. Always. 💉

### Mistake 4: Two `@Primary` beans, or a wrong `@Qualifier` name

Both stop the app from starting. **Fix:** Only **one** `@Primary` per type. And check the `@Qualifier` name = class name with a **small first letter** (or the name you gave in `@Component("...")`).

### Mistake 5: Forgetting `@Configuration` on the recipe class

`@Bean` methods in a class **without** `@Configuration` (and without any other component label) are **never found** — the class isn't scanned! Then you get `required a bean of type 'java.util.Random' that could not be found`. **Fix:** Put `@Configuration` on the class.

---

## ✅ Summary

- A **bean** 🫘 is an object **created and managed by Spring**, kept in the **container** (`ApplicationContext`) 🧸.
- Labels that make beans: **`@Component`** (general), **`@Service`** (logic), **`@Repository`** (data), **`@RestController`** (REST), **`@Controller`** (HTML), **`@Configuration`** (recipes). They're **all** `@Component` inside.
- Bean **name** = class name with a **small first letter** (`greetingService`), or your own: `@Service("greeter")`.
- Beans are **singletons** by default: **one** object, shared by everybody 📽️. Don't keep changing user data in bean fields! (`@Scope("prototype")` = new each time ✏️.)
- For classes you **can't** label: **`@Configuration`** class + **`@Bean`** method 📜.
- **Lifecycle:** constructor → **`@PostConstruct`** → working → **`@PreDestroy`**.
- Two beans of one type: **`@Primary`** ⭐ (the default one), **`@Qualifier("name")`** 🎯 (a specific one), or **`List<Type>`** 📋 (all of them).
- Spring Boot itself creates **many** beans (Tomcat, Jackson...) — over 150 in our small app!

---

## ❓ Quiz

1. What is a bean?
2. Name four labels that make a class a bean.
3. What's the bean name of a class called `StudentService`?
4. What does "singleton" mean for a bean?
5. Two controllers both increase the same `VisitCounter`. Why do they see the same number?
6. When do you use `@Bean` instead of `@Component`?
7. In what order do these happen: `@PreDestroy`, constructor, `@PostConstruct`?
8. What does `@Primary` do?
9. What does `@Qualifier("smsSender")` do?
10. How can a class get **all** beans of the type `MessageSender`?
11. Should a record like `Student(String name, int age)` be a bean? Why or why not?

<details>
<summary>Click to see the answers</summary>

1. An object that Spring creates and manages, kept in Spring's container.
2. Any four: `@Component`, `@Service`, `@Repository`, `@Controller`, `@RestController`, `@Configuration`.
3. `studentService`
4. Spring creates only **one** object of it and gives that same object to everyone who needs it.
5. Because `VisitCounter` is a singleton: both controllers got the **same** object injected.
6. When the class is not yours (from Java or a library), so you can't put a label on it — or when creating it needs special code.
7. Constructor → `@PostConstruct` → (working) → `@PreDestroy`.
8. It marks the bean that Spring uses by default when there are several beans of the same type.
9. It tells Spring to inject the bean with the name `smsSender`.
10. Ask for `List<MessageSender>` in the constructor.
11. No. It's a data object — you need many different students, created with `new`. Beans are for the "workers" of the app.

</details>

---

[⬅ Previous chapter](53-dependency-injection.md) | [Table of Contents](../README.md) | [Next chapter: Settings: application.properties ➡](55-application-properties.md)
