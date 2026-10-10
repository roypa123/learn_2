# Chapter 26 – Packages and `import`

[⬅ Previous chapter](25-interfaces.md) | [Table of Contents](../README.md) | [Next chapter ➡](27-static.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **package** is (a folder for classes)
- How to **create** packages in IntelliJ
- The `package` line at the top of a file
- How to use classes from other packages with **`import`**
- How to **name** packages (the "reverse domain" rule)
- The full table of **access modifiers**: `public`, `protected`, (default), `private`
- What **`java.lang`** is, and why you never import `String`
- How a **real Spring Boot project** organizes its packages 🌱

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Package** | A **folder** that groups related classes together. |
| **`package`** | The first line in a file that says which package (folder) the class belongs to. |
| **`import`** | A line that says "I want to use a class from **another** package". |
| **Fully qualified name** | The **full** name of a class, with its package: `java.util.Scanner`. |
| **Default package** | No package at all (what we used until now). Fine for learning, not for real projects. |
| **Package-private** | The "no modifier" access level: visible only inside the **same package**. |
| **Reverse domain name** | Naming packages like a website address backwards: `com.example.shop`. |

---

## 📖 Story: The library and its shelves 📚

Imagine a library with **10,000 books** — all in **one big pile** on the floor. 😱 Finding a book would take forever!

A real library has **sections** and **shelves**:

```
 📚 Library
  ├── 📁 Science
  │     ├── 📁 Biology
  │     └── 📁 Physics
  ├── 📁 Stories
  │     ├── 📁 Adventure
  │     └── 📁 Fairy tales
  └── 📁 History
```

- Books about the **same topic** are together.
- Two books can have the **same title** if they're on **different shelves**. ("Introduction" in Biology ≠ "Introduction" in Physics.)
- To find a book, you need its **full address**: Science → Biology → "Introduction".

**Packages** are the shelves for your classes. 📁

---

## 📁 Part 1: Why packages?

Until now, all our classes were in the `src` folder directly. With 5 classes, that's fine. But a real Spring Boot app has **100+ classes**! 😵

Packages solve three problems:

| Problem | Solution |
|---|---|
| 🗂️ **Order** — too many files in one folder | Group related classes: all "student" classes together, all "payment" classes together |
| 🏷️ **Name clashes** — two classes called `Date` | Different packages → different full names: `java.util.Date` and `java.sql.Date` |
| 🔒 **Privacy** — some classes are only for internal use | Package-private access (Part 6) |

---

## 🛠️ Part 2: Creating a package in IntelliJ

1. In the **Project** window, right-click on `src`.
2. Choose **New → Package**.
3. Type the name: `com.mycompany.zoo`
4. Press **Enter**.

IntelliJ creates **folders inside folders**:

```
 src
  └── com
       └── mycompany
            └── zoo
```

5. Right-click on `zoo` → **New → Java Class** → `Animal`.

IntelliJ creates the file with a **new first line**:

**File: `src/com/mycompany/zoo/Animal.java`**

```java
package com.mycompany.zoo;

public class Animal {
    private final String name;

    public Animal(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
```

### 🔍 Line by line

`package com.mycompany.zoo;`

| Part | Meaning |
|---|---|
| `package` | "This class lives in the package..." |
| `com.mycompany.zoo` | The package name. Each **dot** `.` is a **folder level**: `com/mycompany/zoo`. |
| `;` | End. |

> ⚠️ **Rules:**
> - The `package` line must be the **very first** line of code (only comments may come before it).
> - The package name must **match** the folder path. `package com.mycompany.zoo;` → the file **must** be in the folder `com/mycompany/zoo/`.
> - IntelliJ takes care of this for you. If you move a file, IntelliJ updates the `package` line automatically (use **drag and drop** in the Project window, or **F6 → Move**).

---

## 🏷️ Part 3: Naming packages

### The rules

| Rule | ✅ Good | ❌ Bad |
|---|---|---|
| **All small letters** | `com.example.shop` | `com.Example.Shop` |
| No spaces or `-` | `com.example.onlineshop` | `com.example.online-shop` |
| Words separated by dots | `com.example.shop.payment` | `com_example_shop` |

### The "reverse domain" tradition

Companies use their **website address backwards** so their package names are **unique in the whole world**:

| Website | Package |
|---|---|
| `google.com` | `com.google...` |
| `spring.io` | `org.springframework...` (an older name) |
| `apache.org` | `org.apache...` |
| `mycompany.com` | `com.mycompany...` |

Then they add the **project** and **topic**:

```
 com.mycompany.shop.payment
 ───────────── ──── ───────
  company       app   topic
```

> 💡 **No website?** Use `com.example` (a name made for examples) or your name: `io.github.yourname`. For learning, `com.example.myapp` is perfect.

---

## 📥 Part 4: `import` — using classes from other packages

Let's make a second package and use `Animal` from it.

**File: `src/com/mycompany/app/Main.java`**

```java
package com.mycompany.app;

import com.mycompany.zoo.Animal;

public class Main {
    public static void main(String[] args) {
        Animal leo = new Animal("Leo");
        System.out.println(leo.getName());
    }
}
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `package com.mycompany.app;` | `Main` lives in the `app` package. |
| `import com.mycompany.zoo.Animal;` | "I want to use the class `Animal` from the package `com.mycompany.zoo`." |
| `Animal leo = new Animal("Leo");` | Now we can use the short name `Animal`. |

### 📋 Order in a Java file

```java
package com.mycompany.app;          // 1️⃣ package (one line, first)

import java.util.Scanner;           // 2️⃣ imports (zero or more)
import com.mycompany.zoo.Animal;

public class Main {                 // 3️⃣ the class
    ...
}
```

### Without `import`: the full name

You **can** skip the import and write the **fully qualified name** every time:

```java
com.mycompany.zoo.Animal leo = new com.mycompany.zoo.Animal("Leo");
```

That's long! 😅 `import` lets you use the **short** name.

### Same package → no import needed

Classes in the **same** package can see each other **without** import. (That's why we never needed imports for our own classes until now — they were all in the default package together!)

### Import everything from a package: `*`

```java
import java.util.*;   // all classes in java.util: Scanner, Arrays, List, Map...
```

The `*` (star) means "everything in this package".

> 💡 Many teams prefer **one import per class** (`import java.util.Scanner;`), so you can see exactly what is used. IntelliJ manages imports for you anyway.

> ⚠️ `*` does **not** include sub-packages. `import java.util.*;` does **not** import `java.util.function.Function`.

### 🪄 IntelliJ does imports for you

- Type a class name like `Scanner` → it turns **red** → press **Alt + Enter** → **Import class**. ✨
- Or: IntelliJ can add imports **automatically** as you type. (Settings → Editor → General → Auto Import → ✅ *Add unambiguous imports on the fly*.)
- **Ctrl + Alt + O** removes unused imports.

---

## ☕ Part 5: `java.lang` — the free package

Why didn't we ever import `String`, `System`, `Math`, `Integer`, `Object`?

They live in the package **`java.lang`** (*lang* = language). Java imports it **automatically** in every file, because these classes are needed **everywhere**.

| Package | Some classes | Import needed? |
|---|---|---|
| `java.lang` | `String`, `System`, `Math`, `Integer`, `Double`, `Object`, `Character` | ❌ **No** — automatic |
| `java.util` | `Scanner`, `Arrays`, `List`, `ArrayList`, `Map`, `HashMap`, `Random`, `Objects` | ✅ Yes |
| `java.time` | `LocalDate`, `LocalDateTime`, `Duration` | ✅ Yes |
| `java.io` | `File`, `IOException` | ✅ Yes |
| `java.math` | `BigDecimal`, `BigInteger` | ✅ Yes |

### When two classes have the same name

Java has **two** classes called `Date`: `java.util.Date` and `java.sql.Date`. If you need both:

```java
import java.util.Date;

public class Example {
    Date today = new Date();               // java.util.Date (imported)
    java.sql.Date dbDate = null;           // full name for the other one
}
```

### Static import (bonus)

You can import **static members** (Chapter 27) so you don't need the class name:

```java
import static java.lang.Math.PI;
import static java.lang.Math.sqrt;

double r = sqrt(16) * PI;   // instead of Math.sqrt(16) * Math.PI
```

Use it carefully — it can make code harder to read ("where does `sqrt` come from?"). You'll see it often in **tests** (Chapter 84): `import static org.junit.jupiter.api.Assertions.*;`

---

## 🔒 Part 6: Access modifiers — the full table

Now that you know packages, here's the **complete** picture of who can see what:

| Modifier | Same class | Same package | Child class (other package) | Everyone else |
|---|---|---|---|---|
| `public` | ✅ | ✅ | ✅ | ✅ |
| `protected` | ✅ | ✅ | ✅ | ❌ |
| *(nothing)* — **package-private** | ✅ | ✅ | ❌ | ❌ |
| `private` | ✅ | ❌ | ❌ | ❌ |

🏠 **Story:**
- `public` — the **street**: everyone can see it.
- `protected` — your **family**, even those who live in other cities.
- *(nothing)* — your **house**: everyone living in the same house (package).
- `private` — your **diary**: only you. 📔🔒

### Package-private (no modifier)

```java
package com.mycompany.zoo;

class ZooHelper {               // no "public" → only visible inside com.mycompany.zoo
    static void feedAll() { }
}
```

```java
package com.mycompany.app;

import com.mycompany.zoo.ZooHelper;   // ❌ error: ZooHelper is not public in com.mycompany.zoo;
                                      //    cannot be accessed from outside package
```

👉 Use package-private for **helper** classes that are only used **inside** one package. It keeps the "outside world" simple.

### Which one should I use? 🤔

| Thing | Usually |
|---|---|
| Fields | `private` (always!) |
| Methods others need | `public` |
| Helper methods inside the class | `private` |
| Methods only children need | `protected` |
| Classes | `public` (one per file), or package-private for internal helpers |
| Constructors | `public` (or `private` for special cases — Chapter 27) |

> 💡 **Rule of thumb:** Start with the **most private** option. Make it more public only when you **need** to. It's easy to open a door later; it's hard to close one that everyone already uses. 🚪

---

## 🌱 Part 7: How a Spring Boot project looks

Here's a typical Spring Boot project structure. You'll build exactly this in Part 7–9 of the book!

```
 src/main/java
  └── com
       └── example
            └── school                           ← base package
                 ├── SchoolApplication.java       ← the main class (starts everything)
                 │
                 ├── controller                   ← talks to the web 🌐
                 │    ├── StudentController.java
                 │    └── CourseController.java
                 │
                 ├── service                      ← business rules 🧠
                 │    ├── StudentService.java
                 │    └── CourseService.java
                 │
                 ├── repository                   ← talks to the database 🗄️
                 │    ├── StudentRepository.java
                 │    └── CourseRepository.java
                 │
                 ├── model                        ← data classes 📦
                 │    ├── Student.java
                 │    └── Course.java
                 │
                 └── dto                          ← data sent over the web 📨
                      ├── StudentRequest.java
                      └── StudentResponse.java
```

The file `StudentController.java` would start like this:

```java
package com.example.school.controller;

import com.example.school.model.Student;
import com.example.school.service.StudentService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StudentController {
    ...
}
```

Look at the imports:
- `com.example.school...` → **your own** classes from other packages
- `org.springframework...` → classes from the **Spring** library 🌱

> ⚠️ **Spring Boot rule:** All your classes must be in the **base package** (`com.example.school`) or **below** it. Spring searches for your classes starting from there. A class outside (like `com.other.Thing`) is **not found**! We'll see why in Chapter 54.

### Two ways to organize packages

| By **layer** (above) | By **feature** |
|---|---|
| `controller/`, `service/`, `repository/` | `student/`, `course/`, `teacher/` |
| Easy for beginners | Better for big projects |
| All controllers together | Everything about "student" together |

Both are fine. This book uses **by layer**, because it's easier to learn.

---

## 💻 Mini project: A zoo in packages 🦁

Let's build a small project with packages. Create this structure in IntelliJ:

```
 src
  └── com
       └── example
            └── zoo
                 ├── ZooApp.java
                 ├── animals
                 │    ├── Animal.java
                 │    ├── Lion.java
                 │    └── Penguin.java
                 └── staff
                      └── Keeper.java
```

**File: `com/example/zoo/animals/Animal.java`**

```java
package com.example.zoo.animals;

public abstract class Animal {
    private final String name;
    int mealsToday;   // package-private: only classes in "animals" can see it

    protected Animal(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public int getMealsToday() {
        return mealsToday;
    }

    public void eat() {
        mealsToday++;
        System.out.println("🍽️ " + name + " eats " + favoriteFood() + ".");
    }

    protected abstract String favoriteFood();
}
```

**File: `com/example/zoo/animals/Lion.java`**

```java
package com.example.zoo.animals;

public class Lion extends Animal {
    public Lion(String name) {
        super(name);
    }

    @Override
    protected String favoriteFood() {
        return "meat 🥩";
    }
}
```

**File: `com/example/zoo/animals/Penguin.java`**

```java
package com.example.zoo.animals;

public class Penguin extends Animal {
    public Penguin(String name) {
        super(name);
    }

    @Override
    protected String favoriteFood() {
        return "fish 🐟";
    }
}
```

**File: `com/example/zoo/staff/Keeper.java`**

```java
package com.example.zoo.staff;

import com.example.zoo.animals.Animal;

public class Keeper {
    private final String name;

    public Keeper(String name) {
        this.name = name;
    }

    public void feed(Animal[] animals) {
        System.out.println("👷 " + name + " starts feeding time!");
        for (Animal animal : animals) {
            animal.eat();
        }
    }
}
```

**File: `com/example/zoo/ZooApp.java`**

```java
package com.example.zoo;

import com.example.zoo.animals.Animal;
import com.example.zoo.animals.Lion;
import com.example.zoo.animals.Penguin;
import com.example.zoo.staff.Keeper;

public class ZooApp {
    public static void main(String[] args) {
        Animal[] animals = { new Lion("Leo"), new Penguin("Pingu") };
        Keeper keeper = new Keeper("Sam");

        keeper.feed(animals);
        keeper.feed(animals);

        for (Animal a : animals) {
            System.out.println(a.getName() + " ate " + a.getMealsToday() + " meals today.");
        }
    }
}
```

**Output:**

```
👷 Sam starts feeding time!
🍽️ Leo eats meat 🥩.
🍽️ Pingu eats fish 🐟.
👷 Sam starts feeding time!
🍽️ Leo eats meat 🥩.
🍽️ Pingu eats fish 🐟.
Leo ate 2 meals today.
Pingu ate 2 meals today.
```

### 🔍 Access check

| Code in `ZooApp` (package `com.example.zoo`) | Allowed? | Why |
|---|---|---|
| `a.getName()` | ✅ | `public` |
| `a.getMealsToday()` | ✅ | `public` |
| `a.mealsToday` | ❌ | package-private, and `ZooApp` is in a **different** package |
| `a.favoriteFood()` | ❌ | `protected`, and `ZooApp` is not a child |
| `new Animal("x")` | ❌ | abstract (and the constructor is `protected`) |

> 💡 `com.example.zoo` and `com.example.zoo.animals` are **different** packages! Even though one looks like it's "inside" the other, Java treats them as **completely separate**. Package-private does **not** reach into "sub-packages".

---

## ✋ Try it yourself

**Task 1:** Create the zoo project above in IntelliJ. Then add a `Monkey` class in the `animals` package (favorite food: bananas 🍌) and add it to the array.

**Task 2:** In `ZooApp`, try to write `animals[0].mealsToday = 100;`. What error do you get? Why?

<details>
<summary>Click to see the answer</summary>

```
error: mealsToday is not public in Animal; cannot be accessed from outside package
```

`mealsToday` has no modifier → package-private. `ZooApp` is in `com.example.zoo`, not in `com.example.zoo.animals`.

</details>

**Task 3:** Which `import` lines do you need?

```java
Scanner sc = new Scanner(System.in);
String name = sc.nextLine();
int[] nums = {3, 1, 2};
Arrays.sort(nums);
double r = Math.random();
```

<details>
<summary>Click to see the answer</summary>

```java
import java.util.Scanner;
import java.util.Arrays;
```

`String`, `System` and `Math` are in `java.lang` → no import needed.

</details>

**Task 4:** Your company's website is `sunnybakery.com`, and the app is called "orders". Write a good package name for the **payment** classes.

<details>
<summary>Click to see the answer</summary>

`com.sunnybakery.orders.payment`

</details>

**Task 5:** Move your **bank account** classes from Chapter 24 into a package `com.example.bank.account`, and the `Bank` main class into `com.example.bank`. Fix the imports and access modifiers so it compiles.

---

## ⚠️ Common mistakes

### Mistake 1: The package line doesn't match the folder

```java
// File is in: src/com/example/zoo/Animal.java
package com.example.animals;   // ❌ wrong — IntelliJ shows: Package name 'com.example.animals' does not correspond to the file path
```

**Fix:** Use **Alt + Enter** in IntelliJ → "Set package name to..." or move the file.

### Mistake 2: Forgetting the import

```java
Animal a = new Animal("Leo");   // ❌ error: cannot find symbol  class Animal
```

**Fix:** **Alt + Enter** → Import class.

### Mistake 3: Class is not public

```
error: Keeper is not public in com.example.zoo.staff; cannot be accessed from outside package
```

**Fix:** Add `public` before `class`.

### Mistake 4: Capital letters in package names

```java
package com.Example.MyApp;   // ⚠️ works, but breaks the convention
package com.example.myapp;   // ✅
```

### Mistake 5: Thinking sub-packages share access

`com.example.zoo` and `com.example.zoo.animals` are **different** packages for access rules.

### Mistake 6: Running a class in a package from the terminal

```
cd src/com/example/zoo
java ZooApp.java          ❌ may fail to find the other classes
```

**Fix:** Compile from the `src` folder and use the **full** name:

```
cd src
javac com/example/zoo/ZooApp.java com/example/zoo/animals/*.java com/example/zoo/staff/*.java
java com.example.zoo.ZooApp
```

(Or just use IntelliJ's ▶ button! Later, **Maven** will do all of this for you — Chapter 40.)

---

## ✅ Summary

- A **package** is a **folder** for related classes. It brings order, avoids name clashes, and controls access.
- First line: `package com.example.zoo;` — it must match the folder path.
- Package names: **small letters**, **reverse domain**: `com.company.project.topic`.
- `import com.example.zoo.Animal;` → use a class from another package by its short name. `import java.util.*;` → all classes in a package.
- Classes in the **same** package don't need imports.
- `java.lang` (`String`, `System`, `Math`...) is imported **automatically**.
- Access: `public` (everyone) › `protected` (package + children) › *nothing* (package only) › `private` (class only).
- Start with the **most private** access and open up only when needed.
- Spring Boot projects use packages like `controller`, `service`, `repository`, `model` under one **base package**.
- IntelliJ: **Alt + Enter** to import, **Ctrl + Alt + O** to clean imports, **F6** to move classes.

---

## ❓ Quiz

1. What is a package?
2. Where must the `package` line be written?
3. The class `Order` is in `com.shop.model`. Which line imports it?
4. Why don't you need to import `String`?
5. What does `import java.util.*;` do?
6. What access does a field with **no** modifier have?
7. Can a class in `com.example` use a package-private method of a class in `com.example.tools`?
8. Name 4 typical packages in a Spring Boot project.

<details>
<summary>Click to see the answers</summary>

1. A folder that groups related classes together.
2. At the very top of the file (only comments can be before it).
3. `import com.shop.model.Order;`
4. `String` is in `java.lang`, which is imported automatically.
5. It imports all classes in the `java.util` package (but not sub-packages).
6. Package-private: only classes in the same package can see it.
7. No — they are different packages.
8. For example: `controller`, `service`, `repository`, `model` (also `dto`, `config`).

</details>

---

[⬅ Previous chapter](25-interfaces.md) | [Table of Contents](../README.md) | [Next chapter: The word static ➡](27-static.md)
