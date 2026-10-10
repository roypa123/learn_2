# Chapter 48 – What are Spring and Spring Boot? (A deeper look)

[⬅ Previous chapter](../part-06-web/47-postman-and-curl.md) | [Table of Contents](../README.md) | [Next chapter ➡](49-spring-initializr.md)

---

## 🎯 Goal

In Chapter 2 you met Spring Boot for the first time. You did not know Java then. Now you know **a lot**! 💪 So now we can look **deeper**.

At the end of this chapter you will know:

- The difference between a **library** and a **framework**
- What **Spring** is, and what **Spring Boot** adds on top of it
- The **Spring family**: Spring Data, Spring Security, and friends
- What the **Spring container** is (the "toy box" full of objects 🧸)
- What **auto-configuration** and **starters** really do
- What happens, step by step, when you press **Run** ▶️
- How everything you learned in Parts 1–6 is used by Spring Boot

> 🌱 This chapter has **only one** small program, and it is plain Java. It is a **"thinking" chapter**. From the next chapter on, you will build real Spring Boot apps. 🚀

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Library** | Ready code that **you call** when you need it. Example: Gson (Chapter 45). |
| **Framework** | Ready code that **calls your code**. It is the "skeleton" of your app, and you fill in the parts. |
| **Spring** (Spring Framework) | A very popular Java **framework** for building apps, especially for servers. |
| **Spring Boot** | A helper **on top of** Spring. It makes Spring **easy and fast** to start. |
| **Container** | The part of Spring that **creates your objects** and **connects** them. Also called the **ApplicationContext**. |
| **Bean** | An object that **Spring** created and keeps in its container. 🫘 |
| **Inversion of Control (IoC)** | "Turning control around": the **framework** controls the program, not you. |
| **Auto-configuration** | Spring Boot **looks at your project** and sets things up automatically. |
| **Starter** | A ready **package of libraries** for one job (web, database, security...). |
| **Embedded server** | A web server (Tomcat) that lives **inside** your app. |
| **Convention over configuration** | "We choose good default settings for you. Change them only if you want." |

---

## 📖 Story: Building a house 🏠

Imagine you want to build a house.

**Way 1: The toolbox 🧰**
You buy a toolbox: a hammer, a saw, a drill. **You** decide everything. **You** pick up the hammer when you need it. The tools wait for you.
👉 This is a **library**. You call it.

**Way 2: The building company 🏗️**
You hire a building company. They already have a **plan**: foundation first, then walls, then the roof. They do the hard parts. They only **ask you** about your choices: "What color for the kitchen? How many bedrooms?" Then **they** put your choices in the right place, at the right time.
👉 This is a **framework**. It calls you.

**Way 3: The building company with a "ready house" package 🏡✨**
The company says: "Most families want 3 bedrooms, a kitchen, and a garden. We'll build **that** for you **by default**. If you want something different, just tell us." You move in after one day!
👉 This is **Spring Boot**: a framework (Spring) + **good default choices** + a **fast start**.

---

## 🧰 Part 1: Library vs framework

You already used a **library**: **Gson** (Chapter 45).

```java
Gson gson = new Gson();
String json = gson.toJson(student);   // YOU call Gson
```

**You** are the boss. You call `gson.toJson(...)` when **you** want. Gson waits. 🧰

Now remember the Spring Boot "hello" from Chapter 2:

```java
@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello from Spring Boot!";
    }
}
```

Look carefully: **who calls `hello()`?** 🤔

- Not you! There is no line like `controller.hello()` anywhere in your code.
- **Spring** calls it, when a request for `/hello` arrives from a browser.

You write the **pieces**. Spring decides **when** to use them. 🏗️

| | Library 🧰 | Framework 🏗️ |
|---|---|---|
| Who is the boss? | **You** | **The framework** |
| Who calls whom? | Your code **calls** the library | The framework **calls** your code |
| Example | Gson, `Math`, `Scanner` | **Spring**, Spring Boot |
| Like... | a toolbox | a building company |

This idea has a funny nickname: the **Hollywood principle** 🎬:

> "**Don't call us, we'll call you.**"

(In Hollywood, actors go to a film test. At the end, the director says: "Don't call us. **We** will call **you** if we want you." 😄)

The fancy name is **Inversion of Control** (IoC). "Inversion" means "turning around". Normally **you** control the program. With a framework, the control is **turned around**: the framework controls the program, and your code is called **by** it.

---

## 💻 Part 2: Build a tiny framework yourself! 🛠️

The best way to understand a framework is to **build a tiny one**. 😄 Remember **annotations** and **reflection** from Chapter 38? We'll use them to make our own mini version of `@GetMapping`.

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Map;

public class MiniSpring {
    public static void main(String[] args) throws Exception {
        MiniFramework framework = new MiniFramework(new MyController());
        System.out.println("---");
        System.out.println(framework.handle("/hello"));
        System.out.println(framework.handle("/lunch"));
        System.out.println(framework.handle("/pizza"));
    }
}

// 1. Our own label, like Spring's @GetMapping
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@interface Get {
    String value();
}

// 2. YOUR code: normal methods with labels. No server code!
class MyController {

    @Get("/hello")
    public String hello() {
        return "Hello from my mini framework!";
    }

    @Get("/lunch")
    public String lunch() {
        return "Pizza today!";
    }
}

// 3. The FRAMEWORK: it finds your methods and calls them
class MiniFramework {

    private final Map<String, Method> routes = new HashMap<>();
    private final Object controller;

    MiniFramework(Object controller) {
        this.controller = controller;
        for (Method method : controller.getClass().getDeclaredMethods()) {
            Get label = method.getAnnotation(Get.class);
            if (label != null) {
                routes.put(label.value(), method);
                System.out.println("Found " + label.value() + " -> " + method.getName() + "()");
            }
        }
    }

    String handle(String path) throws Exception {
        Method method = routes.get(path);
        if (method == null) {
            return path + " -> 404 Not Found";
        }
        Object answer = method.invoke(controller);
        return path + " -> 200 OK: " + answer;
    }
}
```

Save it as `MiniSpring.java` and run `java MiniSpring.java`.

**Output:**

```
Found /lunch -> lunch()
Found /hello -> hello()
---
/hello -> 200 OK: Hello from my mini framework!
/lunch -> 200 OK: Pizza today!
/pizza -> 404 Not Found
```

> 💡 The two "Found" lines may come in a **different order** on your computer. Java does not promise an order for `getDeclaredMethods()`. That's fine!

### 🔍 Line by line

**The main method:**

| Code | Meaning |
|---|---|
| `new MiniFramework(new MyController())` | Start the framework and **give it** your controller. |
| `framework.handle("/hello")` | Pretend a browser asked for `/hello`. (A real framework gets this from a real HTTP request — Chapter 43!) |

> 💡 **Why is `main` at the top?** When you run `java MiniSpring.java`, Java starts the **first** class in the file. So the class with `main` must come first. If you put it at the bottom, Java says: `error: can't find main(String[]) method in class: Get`.

**Part 1 – the label:**

| Code | Meaning |
|---|---|
| `@Retention(RetentionPolicy.RUNTIME)` | Keep this label when the program **runs**, so the framework can **read** it. (Chapter 38) |
| `@Target(ElementType.METHOD)` | This label can only be put on **methods**. |
| `@interface Get` | We create a new annotation called `@Get`. |
| `String value();` | The label holds one text: the **path**, like `"/hello"`. |

**Part 2 – your code:**

| Code | Meaning |
|---|---|
| `class MyController` | A normal class. It knows **nothing** about servers, ports or HTTP. |
| `@Get("/hello")` | A label: "please call me for the path `/hello`". |
| `public String hello()` | A normal method that returns a text. |

**Part 3 – the framework:**

| Code | Meaning |
|---|---|
| `Map<String, Method> routes` | A map (Chapter 31): path → method. Like a **phone book** 📒: "/hello" → `hello()`. |
| `controller.getClass().getDeclaredMethods()` | **Reflection**: "show me **all** methods of this object's class". |
| `method.getAnnotation(Get.class)` | "Does this method have a `@Get` label? If yes, give it to me. If no, `null`." |
| `routes.put(label.value(), method)` | Remember: this path belongs to this method. |
| `routes.get(path)` | When a request comes: find the method for this path. |
| `if (method == null)` | No method for this path → **404 Not Found** (Chapter 44). |
| `method.invoke(controller)` | **Call** the method! ⭐ This is the moment the **framework calls your code**. |

### 🎉 What did you just build?

You built the **heart idea** of Spring's web part! The real Spring does the **same thing**, just much bigger and better:

| Your mini framework | Real Spring Boot |
|---|---|
| `@Get("/hello")` | `@GetMapping("/hello")` |
| You give it **one** controller with `new` | Spring **finds all** your controllers **by itself** |
| `handle("/hello")` with a fake path | A **real** web server (Tomcat) gets **real** HTTP requests |
| Returns a text | Returns text **or JSON**, with status codes and headers |
| ~40 lines | ~1 million lines, tested by millions of developers 😄 |

**Spring is not magic.** It uses the **same Java** you learned: annotations, reflection, interfaces, maps. It's just very well made. 🧠✨

---

## 🌸 Part 3: What is Spring? A short history

| Year | What happened |
|---|---|
| ~2000 | Building Java server apps was **very hard**. Lots of complicated rules, lots of boring code. 😫 |
| 2002 | A developer named **Rod Johnson** wrote a book with a simpler idea, and code to go with it. |
| 2004 | **Spring Framework 1.0** came out. The name "Spring" means a **fresh start after the winter** 🌸 (the "winter" was the old, hard way). |
| 2004–2013 | Spring became the **most popular** Java framework. But setting it up still needed **a lot of settings** (long XML files 📜). |
| 2014 | **Spring Boot 1.0** came out: "Let's make Spring **easy to start**!" 🚀 |
| Today | Spring Boot **4** (built on Spring Framework **7**). Used by banks, shops, streaming companies, governments... |

### Life before Spring Boot 😵

Here is a **small part** of how people set up a Spring web app **before** Spring Boot (don't try to understand it, just look at it):

```xml
<!-- web.xml -->
<servlet>
    <servlet-name>dispatcher</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <init-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>/WEB-INF/spring-config.xml</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
    <servlet-name>dispatcher</servlet-name>
    <url-pattern>/</url-pattern>
</servlet-mapping>
<!-- ...and another long file, spring-config.xml... -->
<!-- ...and then: install a server program, copy your app into it... -->
```

And this was **only the beginning**! You also had to:

- write **more** XML files,
- choose versions of **20+ libraries** that work together (and hope they do 🤞),
- **install** a separate server program (Tomcat) and copy your app into it.

**With Spring Boot:** you click a few buttons on a website, press **Run**, and your server is running. ✨ No XML. No separate server. No version puzzles.

---

## 👨‍👩‍👧‍👦 Part 4: The Spring family

"Spring" is not one thing. It's a **family** of projects. They all work together.

| Project | What it does | In this book |
|---|---|---|
| **Spring Framework** | The **core**: the container (beans, DI) + **Spring MVC** (the web part) | Everywhere! |
| **Spring Boot** | Makes all Spring projects **easy to start and run** | Everywhere! |
| **Spring Data JPA** | Talks to **databases** with very little code | Part 9 |
| **Spring Security** | **Login**, passwords, roles, tokens 🔒 | Part 10 |
| **Spring Boot Actuator** | Health checks, numbers about your running app ❤️ | Chapter 94 |
| Spring Cloud | Tools for **very big** systems with many small apps | (not in this book) |
| Spring Batch | Processing **huge** amounts of data in steps | (not in this book) |

```
                    ┌───────────────────────────┐
                    │        Spring Boot 🚀       │  ← makes it all easy
                    └─────────────┬─────────────┘
       ┌──────────────┬───────────┴──┬──────────────┐
  Spring MVC 🌐   Spring Data 🗄️  Spring Security 🔒  Actuator ❤️
       └──────────────┴──────┬───────┴──────────────┘
                    ┌────────┴────────┐
                    │ Spring Framework │  ← the core: container + beans
                    │      (core)      │
                    └────────┬────────┘
                    ┌────────┴────────┐
                    │      Java ☕     │
                    └─────────────────┘
```

> 💡 When people say "**Spring**", they often mean the **whole family**. When they say "**Spring Boot**", they mean the **easy way** to use it. In daily life, most new projects use Spring Boot. So "I know Spring Boot" really means "I know how to build apps with the Spring family, the easy way". 😊

---

## 🧸 Part 5: The heart of Spring — the container

This is the **most important idea** in this chapter. ⭐

In a normal Java program, **you** create objects with `new`:

```java
Oven oven = new Oven();
Chef chef = new Chef(oven);
Waiter waiter = new Waiter(chef);
```

In a Spring app, you **don't** write these lines. Instead:

1. You put a **label** on your classes, like `@Service` or `@RestController`.
2. When the app starts, **Spring** finds these classes.
3. **Spring** creates **one object** of each with `new`.
4. **Spring** gives each object the **other objects it needs** (it "plugs them together").
5. **Spring** keeps all these objects in a big **box**. This box is called the **container** (or **ApplicationContext**).
6. The objects inside are called **beans**. 🫘

```
   Your classes with labels               The Spring container 🧸
   ────────────────────────               ───────────────────────────
   @Service   GreetingService    ─┐       ┌───────────────────────────┐
   @RestController HelloController├─────► │  🫘 greetingService        │
   @Repository StudentRepository ─┘ Spring │  🫘 helloController        │
                                   creates │  🫘 studentRepository      │
                                   them    │  🫘 ...and ~150 beans that │
                                           │     Spring Boot made too!  │
                                           └───────────────────────────┘
```

Why "**bean**"? Java is named after **coffee** ☕ (Java is an island famous for coffee). Coffee is made from... **beans**! So the objects in Spring are called **beans**. 🫘😄

Why is this so good? 🤔

| Without a container | With the Spring container |
|---|---|
| You write `new` everywhere | Spring creates the objects |
| You must create things in the **right order** | Spring figures out the order |
| Changing one class can mean changing **many** `new` lines | Change in **one** place |
| Hard to swap a real email sender for a fake one in tests | Easy to swap 🔌 |

You'll learn all of this **properly** in **Chapter 53** (Dependency Injection) and **Chapter 54** (Beans). You already know the idea from **Chapter 25** (loose coupling with interfaces) and **Chapter 27** (singletons). 🧠

---

## 🚀 Part 6: What Spring Boot adds

Spring (the framework) gives the container and the web part. **Spring Boot** adds **five big helpers**:

### Helper 1: Starters 📦

Remember **Chapter 41**? A **starter** is **one** dependency that brings **a whole set** of libraries that work well together.

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webmvc</artifactId>
</dependency>
```

This **one** dependency brings: Spring MVC, a **Tomcat** web server, **Jackson** (for JSON), logging, and more. All with versions that are **tested together**. ✅

> 💡 In older Spring Boot versions this starter was called `spring-boot-starter-web`. Today Spring Initializr gives you `spring-boot-starter-webmvc`. Both mean "**I want to build a web app**". Always use the name Spring Initializr gives you.

### Helper 2: Auto-configuration 🪄

When your app starts, Spring Boot **looks around** in your project and asks questions:

```
❓ Is the Tomcat library here?          → Yes! ✅  Then I'll start a web server on port 8080.
❓ Is the Jackson library here?          → Yes! ✅  Then I'll turn objects into JSON automatically.
❓ Is a database library (like H2) here? → No.  ❌  Then I won't set up a database.
❓ Did the developer set server.port?    → No.  ❌  Then I'll use the default: 8080.
```

This is **auto-configuration**: "If you **have** this library, I'll **set it up** for you with good default settings." 🪄

And the most important rule: **you are always the boss.** If you don't like a default, you **change** it — usually with **one line** in a settings file (Chapter 55):

```properties
server.port=9090
```

### Helper 3: An embedded server 🍽️

In Chapter 43 you built a tiny server with `HttpServer`. Real apps use a **professional** server called **Tomcat** 🐱.

- **Old way:** install Tomcat separately, then copy your app **into** Tomcat.
- **Spring Boot way:** Tomcat is **inside** your app (it's "embedded"). You just press **Run**. ▶️

### Helper 4: Good defaults (convention over configuration) 🎯

Spring Boot makes **smart choices** for you:

| Question | Spring Boot's default answer |
|---|---|
| Which port? | `8080` |
| Which JSON library? | Jackson |
| Where are settings? | `src/main/resources/application.properties` |
| Where to find your classes? | In the **package of the main class**, and below it |
| What happens on an error? | A clear error answer (JSON or a simple page) |

You only write code for what is **special** about **your** app. 🎯

### Helper 5: One runnable file 📦

Spring Boot can pack your whole app — **your code + all libraries + Tomcat** — into **one `.jar` file**. Then anybody with Java can run it:

```
java -jar hello-0.0.1-SNAPSHOT.jar
```

That's how apps go to real servers on the internet (Chapter 98 and 100). 🌍

### 🍔 Summary of Part 6

```
   Spring Boot  =  Spring Framework
                 + Starters             (easy dependencies) 📦
                 + Auto-configuration   (smart automatic setup) 🪄
                 + Embedded Tomcat      (server inside) 🐱
                 + Good defaults        (less to decide) 🎯
                 + Runnable jar         (easy to ship) 🚚
```

---

## ▶️ Part 7: What happens when you press Run?

In Chapter 50 you'll see this file. It's in **every** Spring Boot app:

```java
@SpringBootApplication
public class HelloApplication {

    public static void main(String[] args) {
        SpringApplication.run(HelloApplication.class, args);
    }
}
```

Just **one** line inside `main`! But a **lot** happens behind it. Here is the story, step by step: 📜

| Step | What Spring Boot does | Like in the building company story 🏗️ |
|---|---|---|
| 1 | Java starts `main`. `main` calls `SpringApplication.run(...)`. | You call the company: "Start, please!" |
| 2 | It prints the **banner** (the big "Spring" logo). | They put up their sign. 😄 |
| 3 | It reads the **settings** (`application.properties`). | They read your wishes list. |
| 4 | It **scans** your package for classes with labels (`@RestController`, `@Service`...). | They look at your plans. |
| 5 | It runs **auto-configuration** (Tomcat? Jackson? Database?). | They decide which machines are needed. |
| 6 | It **creates all beans** and **plugs them together**. | They build the walls and connect the pipes. |
| 7 | It finds all `@GetMapping` methods and remembers their paths. | They put name plates on every door. |
| 8 | It **starts Tomcat** on port 8080. | They open the front door. 🚪 |
| 9 | It prints `Started HelloApplication in 3.6 seconds`. | "Your house is ready!" 🏡 |
| 10 | It **waits** for requests... forever (until you stop it). | You live in it. 😊 |

And here is what you'll **really** see in the console (from a real run — Chapter 51 explains every line):

```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/

 :: Spring Boot ::                (v4.1.1)

... Starting HelloApplication using Java 25 with PID 11632 ...
... No active profile set, falling back to 1 default profile: "default"
... Tomcat initialized with port 8080 (http)
... Starting service [Tomcat]
... Starting Servlet engine: [Apache Tomcat/11.0.24]
... Root WebApplicationContext: initialization completed in 1635 ms
... Tomcat started on port 8080 (http) with context path '/'
... Started HelloApplication in 3.825 seconds (process running for 4.928)
```

Can you find the steps from the table in these lines? 🔍 (The banner = step 2. "Tomcat started on port 8080" = step 8. "Started HelloApplication" = step 9.)

---

## 🗺️ Part 8: Everything you learned is used here!

You may have wondered: "Why did I learn **all that** before Spring Boot?" Here's the answer. 😊

| You learned... | Spring Boot uses it for... |
|---|---|
| Classes and objects (Ch 18) | Every controller, service, and repository is a class |
| Constructors (Ch 19) | Spring gives beans their helpers **through constructors** (Ch 53) |
| `private` fields, getters (Ch 21) | Data classes and entities (Part 9) |
| **Interfaces** (Ch 25) | Loose coupling, repositories, swapping parts 🔌 |
| Packages (Ch 26) | Spring scans your **base package** to find classes |
| `static` and singletons (Ch 27) | Beans are singletons by default — Spring makes them for you |
| Enums (Ch 28) | Status values, roles (`ADMIN`, `USER`) |
| **Records** (Ch 29) | Request and response data (DTOs, Ch 64) |
| Lists and maps (Ch 30–31) | Returning lists of things as JSON arrays |
| Exceptions (Ch 33) | Error handling (Ch 66) |
| Generics (Ch 34) | `List<Student>`, `ResponseEntity<Student>`, `JpaRepository<Student, Long>` |
| Lambdas and streams (Ch 35–36) | Filtering and changing data in services |
| Optional (Ch 37) | `findById(...)` returns an `Optional` (Part 9) |
| **Annotations** (Ch 38) | `@RestController`, `@GetMapping`, `@Service`... **everywhere!** |
| Dates (Ch 39) | Dates in your data, turned into JSON |
| **Maven and pom.xml** (Ch 40–41) | Every Spring Boot project is a Maven project |
| Git (Ch 42) | Saving your project's history |
| **HTTP, JSON, REST** (Ch 43–46) | **This is what your Spring Boot app speaks!** |
| curl and Postman (Ch 47) | Testing your Spring Boot APIs |

**Nothing was wasted.** 🎉 You are ready.

---

## 🙅 Part 9: What Spring Boot is NOT

Some beginners have wrong ideas about Spring Boot. Let's fix them:

| ❌ Wrong idea | ✅ The truth |
|---|---|
| "Spring Boot is a new programming language." | No. It's **Java**. Spring Boot is Java code that someone else wrote for you. |
| "Spring Boot is only for websites." | It's mostly used for **web APIs**, but it can also make command-line tools, background jobs, and more. |
| "Spring Boot is magic. I can't understand it." | It uses annotations, reflection, interfaces — **normal Java**. You even built a mini version! |
| "I don't need to know Java to use Spring Boot." | You **do** need Java. That's why Parts 2–4 exist. 😉 |
| "Spring Boot makes the HTML pages people see." | Mostly, Spring Boot is the **kitchen** 🍳 (the server). The pages people see are often made with other tools (like **Blazor** — your next book! — or React). Spring Boot can make simple pages too (Chapter 89). |

---

## ✋ Try it yourself

**Task 1:** Add a third method to `MyController` in the mini framework:

```java
@Get("/weather")
public String weather() { ... }
```

Return `"Sunny ☀️"`. Then add `framework.handle("/weather")` in `main`. Run it.

<details>
<summary>Click to see the answer</summary>

```java
@Get("/weather")
public String weather() {
    return "Sunny ☀️";
}
```

In `main`:

```java
System.out.println(framework.handle("/weather"));
```

New output line:

```
/weather -> 200 OK: Sunny ☀️
```

And at the top, a new line: `Found /weather -> weather()`. You did **not** touch the framework! You only added a labeled method. That's the power of a framework. 🎉

</details>

**Task 2:** Remove the `@Get("/lunch")` label (keep the method). Run again. What happens to `/lunch`? Why?

<details>
<summary>Click to see the answer</summary>

`/lunch -> 404 Not Found`. The method still exists, but without the label, the framework **doesn't know** it should use it. The same thing happens in Spring Boot when you forget `@GetMapping`! (Chapter 52)

</details>

**Task 3:** Library or framework? Put each one in the right group:
`Gson`, `Spring Boot`, `Scanner`, `Math`, `Spring Framework`, `JUnit` (a testing tool that finds your `@Test` methods and runs them — Chapter 84).

<details>
<summary>Click to see the answer</summary>

- **Library** (you call it): `Gson`, `Scanner`, `Math`
- **Framework** (it calls you): `Spring Boot`, `Spring Framework`, `JUnit` ✅

JUnit is a small framework: **you** never call your test methods. JUnit finds the `@Test` labels and calls them — just like our mini framework! 🎬

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Thinking Spring and Spring Boot are two different choices

Beginners ask: "Should I learn Spring **or** Spring Boot?" It's not "or". Spring Boot **is** Spring, made easy. When you use Spring Boot, you use Spring. ✅

### Mistake 2: Trying to understand everything at once

Spring is **huge**. Nobody knows all of it — not even experts! 😄 Learn one piece at a time, like in this book. When you see a strange annotation, it's **normal** to look it up.

### Mistake 3: Calling your controller methods yourself

In Spring Boot, you **don't** write `new HelloController().hello()`. Spring creates the controller and calls the method when a request arrives. Let the framework do its job. 🎬

### Mistake 4: Fighting the defaults

Spring Boot's defaults are good. Don't change things "just because". Change a default only when you **need** something different. 🎯

---

## ✅ Summary

- A **library** is called **by you** 🧰. A **framework** **calls you** 🏗️ ("Don't call us, we'll call you" 🎬 = **Inversion of Control**).
- You built a **mini framework** with annotations + reflection. Spring works with the same idea, but much bigger.
- **Spring Framework** = the core: the **container** (creates objects called **beans** 🫘 and plugs them together) + the web part.
- **Spring Boot** = Spring + **starters** 📦 + **auto-configuration** 🪄 + **embedded Tomcat** 🐱 + **good defaults** 🎯 + **runnable jar** 🚚.
- The **Spring family** also has Spring Data (databases), Spring Security (login), Actuator (health), and more.
- When you press **Run**: settings → scan → auto-configure → create beans → start Tomcat → wait for requests.
- Everything you learned in Parts 1–6 is used by Spring Boot. You are ready! 🚀

---

## ❓ Quiz

1. What is the difference between a library and a framework?
2. What is the "Hollywood principle"?
3. In your mini framework, which line actually **calls** your method?
4. What is a **bean**?
5. What is the Spring **container**?
6. Name three things that Spring Boot adds on top of Spring.
7. What does auto-configuration do when it finds the Tomcat library in your project?
8. Which port does Spring Boot use by default?
9. True or false: "Spring Boot is a different language than Java."

<details>
<summary>Click to see the answers</summary>

1. You call a library when you need it. A framework controls the program and calls your code.
2. "Don't call us, we'll call you." The framework calls your code, not the other way around.
3. `method.invoke(controller)`.
4. An object that Spring creates and keeps in its container.
5. The "box" (also called the ApplicationContext) where Spring creates, connects and keeps all the beans.
6. Any three of: starters, auto-configuration, an embedded server (Tomcat), good defaults, a runnable jar.
7. It sets up and starts a web server automatically (on port 8080).
8. 8080.
9. False. Spring Boot is Java code. You write Java.

</details>

---

[⬅ Previous chapter](../part-06-web/47-postman-and-curl.md) | [Table of Contents](../README.md) | [Next chapter: Create a project with Spring Initializr ➡](49-spring-initializr.md)
