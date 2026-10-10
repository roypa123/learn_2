# Chapter 27 – The Word `static`

[⬅ Previous chapter](26-packages-import.md) | [Table of Contents](../README.md) | [Next chapter ➡](28-enums.md)

---

## 🎯 Goal

At the end of this chapter you will **finally** understand:

- What **`static`** really means
- **Static fields**: one value **shared** by all objects
- **Static methods**: methods that belong to the **class**, not to an object
- Why `main` is `static`
- What **static methods can't do** (and why)
- **Constants**: `static final`
- **Utility classes** like `Math`
- **Static blocks**, and the **Singleton** idea
- When to use `static` — and when **not** to (very important for Spring Boot!)

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **`static`** | "Belongs to the **class**, not to each object." There's only **one**, shared by everyone. |
| **Instance member** | A field or method that belongs to **each object** (no `static`). |
| **Static member** | A field or method that belongs to the **class** itself. |
| **Class variable** | Another name for a **static field**. |
| **Utility class** | A class with only static methods — a **toolbox**, like `Math`. |
| **Static block** | Code that runs **once**, when the class is first loaded. |
| **Singleton** | A class that has **only one** object in the whole program. |

---

## 📖 Story: The classroom 🏫

In a classroom, every student has **their own** things:
- their own **name** 📛
- their own **notebook** 📓
- their own **pencil** ✏️

But some things are **shared** by the whole class:
- **one** clock on the wall 🕐
- **one** whiteboard 📋
- **one** class counter: "We have 25 students"

If one student writes on the whiteboard, **everyone** sees it. There's only **one** whiteboard!

| Classroom | Java |
|---|---|
| Each student's own name, notebook | **instance** fields (no `static`) |
| The **shared** clock, whiteboard | **`static`** fields |

---

## 🔢 Part 1: Static fields — shared by everyone

### The problem: counting objects

We want to count **how many** students have been created.

```java
public class Student {
    String name;
    int count = 0;   // ❌ each student has its OWN count

    Student(String name) {
        this.name = name;
        count++;
    }
}
```

```java
Student a = new Student("Ali");
Student b = new Student("Sara");
Student c = new Student("Tom");
System.out.println(c.count);   // 1 😕 — each student only counted itself!
```

Every student has a **private notebook** with "count = 1". Nobody knows the **total**.

### ✅ The fix: `static`

```java
public class Student {
    String name;              // each student has their own
    static int count = 0;     // ONE count, shared by all students

    Student(String name) {
        this.name = name;
        count++;              // add 1 to the SHARED count
    }
}
```

```java
new Student("Ali");
new Student("Sara");
new Student("Tom");
System.out.println(Student.count);   // 3 ✅
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `static int count = 0;` | **One** `count` for the **whole class**. Like the whiteboard 📋. |
| `count++;` | Every new student adds 1 to the **same** whiteboard. |
| `Student.count` | Read it using the **class name**, not an object. Because it belongs to the **class**. |

### 🗺️ The picture

```
                  ┌────────────────────────┐
                  │  class Student         │
                  │  static count = 3  📋  │   ← ONE shared value
                  └────────────────────────┘
                         ▲    ▲    ▲
                 shared  │    │    │  shared
       ┌──────────────┐  │ ┌──┴───────────┐  ┌──────────────┐
       │ name = "Ali" │──┘ │ name = "Sara"│  │ name = "Tom" │
       └──────────────┘    └──────────────┘  └──────────────┘
         object 1            object 2           object 3
         (own name)          (own name)         (own name)
```

> 💡 You **can** write `a.count` (through an object), and it works — but it's **confusing**, because it looks like it belongs to `a`. IntelliJ shows a warning. Always use `ClassName.staticField`.

### Example: giving each object an ID

```java
public class Ticket {
    private static int nextId = 1;   // shared counter

    private final int id;            // each ticket's own ID
    private final String event;

    public Ticket(String event) {
        this.id = nextId;   // take the current number
        nextId++;           // move the shared counter forward
        this.event = event;
    }

    @Override
    public String toString() {
        return "🎟️ Ticket #" + id + " for " + event;
    }
}
```

```java
System.out.println(new Ticket("Concert"));
System.out.println(new Ticket("Football"));
System.out.println(new Ticket("Cinema"));
```

**Output:**

```
🎟️ Ticket #1 for Concert
🎟️ Ticket #2 for Football
🎟️ Ticket #3 for Cinema
```

🏪 **Story:** At a bakery, there's **one** ticket machine 🎫 on the wall. Each customer takes a ticket with **their own** number. The machine (`nextId`) is shared; the ticket (`id`) is personal.

> 🌱 **Spring Boot note:** In real apps, IDs come from the **database**, not from a static counter. (A static counter starts at 1 again every time the program restarts!) We'll see this in Chapter 71.

---

## 🛠️ Part 2: Static methods — belong to the class

A **static method** belongs to the class. You call it with the **class name** — **no object needed**.

You've used many already! 😊

| Static method | Class |
|---|---|
| `Math.sqrt(16)` | `Math` |
| `Math.max(3, 7)` | `Math` |
| `Integer.parseInt("42")` | `Integer` |
| `String.valueOf(5)` | `String` |
| `Arrays.sort(arr)` | `Arrays` |
| `String.format(...)` | `String` |

You never wrote `new Math()`. You just used `Math.sqrt(...)` directly. That's because these methods are **static**.

### Writing your own

```java
public class Temperature {
    public static double celsiusToFahrenheit(double c) {
        return c * 9 / 5 + 32;
    }

    public static double fahrenheitToCelsius(double f) {
        return (f - 32) * 5 / 9;
    }
}
```

```java
System.out.println(Temperature.celsiusToFahrenheit(100));   // 212.0
System.out.println(Temperature.fahrenheitToCelsius(32));    // 0.0
```

No `new Temperature()` needed! These methods don't need any **object data** — they just take inputs and return an answer. 🧮

### 🤔 When should a method be static?

Ask: "**Does this method need the data of one specific object?**"

| Method | Needs object data? | Static? |
|---|---|---|
| `dog.bark()` — uses `name` | ✅ yes — which dog? | ❌ instance method |
| `account.deposit(100)` — changes `balance` | ✅ yes — whose account? | ❌ instance method |
| `Math.sqrt(16)` | ❌ no — just math | ✅ static |
| `Temperature.celsiusToFahrenheit(30)` | ❌ no — just a formula | ✅ static |
| `Student.getCount()` — uses static `count` | ❌ only shared data | ✅ static |

---

## 🚫 Part 3: What static methods CAN'T do

A static method belongs to the **class**, not to an object. So inside a static method, **there is no "this" object**!

```java
public class Dog {
    String name;

    static void describe() {
        System.out.println(name);    // ❌ error: non-static variable name cannot be referenced from a static context
        bark();                      // ❌ error: non-static method bark() cannot be referenced from a static context
        System.out.println(this);    // ❌ error: non-static variable this cannot be referenced from a static context
    }

    void bark() { ... }
}
```

🤔 **Why?** If you call `Dog.describe()`, **which** dog's name should it print? Rex's? Bella's? There may be **no** dog at all! Java can't know. 🤷

📖 **Story:** The school **principal** (static) makes an announcement: "Everyone, show me **your** homework!" — that works, she talks to all students. But if she says "Show me **my** homework" — whose? The principal has no homework! 😄

### ✅ The rules

| From... | can use **static** members? | can use **instance** members? |
|---|---|---|
| a **static** method | ✅ yes | ❌ **no** (no `this`!) — unless you have an object |
| an **instance** method | ✅ yes | ✅ yes |

A static method **can** use instance members if it has an **object**:

```java
static void describe(Dog dog) {
    System.out.println(dog.name);   // ✅ we have a specific dog now
    dog.bark();                     // ✅
}
```

---

## 🚪 Part 4: Why is `main` static?

Finally! Since Chapter 5, you've written:

```java
public static void main(String[] args)
```

When you run a program, **no objects exist yet**. 🏜️ The JVM needs to call `main` **without creating an object first**. That's only possible if `main` is **static**!

```
 JVM starts
   │
   │  "I need to start the program, but there are no objects yet..."
   │  "main is static → I can call Main.main(args) directly!" ✅
   ▼
 Main.main(args)
   │
   └─► now YOU create objects: new Dog(), new Scanner(...), ...
```

And now you understand why, in Part 2 (Chapters 6–17), **all** our methods were `static`: they were called from `main` (static), and we had no objects yet!

### The common beginner error — explained

```java
public class Main {
    public static void main(String[] args) {
        sayHello();   // ❌ error: non-static method sayHello() cannot be referenced from a static context
    }

    void sayHello() {
        System.out.println("Hello");
    }
}
```

`main` is static (no object). `sayHello` is an instance method (needs an object). **Two fixes:**

```java
// Fix 1: make sayHello static
static void sayHello() { ... }

// Fix 2: create an object, and call the method on it
public static void main(String[] args) {
    Main app = new Main();
    app.sayHello();
}
```

👉 In real programs, **Fix 2** is very common: `main` creates the first objects, and then **everything** else is done by objects. That's exactly what Spring Boot's `main` does! 🌱

---

## 🔒 Part 5: Constants — `static final`

You saw this in Chapter 17. Now you understand every word:

```java
public class Game {
    public static final int MAX_PLAYERS = 4;
    public static final double GRAVITY = 9.81;
    public static final String GAME_NAME = "Space Quest";
}
```

| Word | Meaning |
|---|---|
| `public` | everyone can read it |
| `static` | **one** copy for the whole class — no need to store it in every object |
| `final` | can never change |
| `MAX_PLAYERS` | UPPER_SNAKE_CASE name |

```java
System.out.println(Game.MAX_PLAYERS);   // 4
Game.MAX_PLAYERS = 10;                   // ❌ error: cannot assign a value to final variable MAX_PLAYERS
```

Java's own constants: `Math.PI`, `Integer.MAX_VALUE`, `Integer.MIN_VALUE`, `Double.MAX_VALUE`...

```java
System.out.println(Integer.MAX_VALUE);   // 2147483647
```

---

## 🧰 Part 6: Utility classes

A **utility class** is a **toolbox** 🧰 of static methods. It has **no** object data. `Math` and `Arrays` are utility classes.

```java
public final class TextUtils {

    private TextUtils() {
        // private constructor: nobody can create a TextUtils object
    }

    public static boolean isPalindrome(String text) {
        String clean = text.toLowerCase().replace(" ", "");
        String reversed = new StringBuilder(clean).reverse().toString();
        return clean.equals(reversed);
    }

    public static String capitalize(String word) {
        if (word == null || word.isEmpty()) {
            return word;
        }
        return word.substring(0, 1).toUpperCase() + word.substring(1).toLowerCase();
    }

    public static int countWords(String text) {
        if (text == null || text.isBlank()) {
            return 0;
        }
        return text.strip().split("\\s+").length;
    }
}
```

```java
System.out.println(TextUtils.isPalindrome("Never odd or even"));   // true
System.out.println(TextUtils.capitalize("hELLO"));                 // Hello
System.out.println(TextUtils.countWords("  I   love Java  "));     // 3
```

### 🔍 Key ideas

| Code | Meaning |
|---|---|
| `public final class` | No children (nobody should extend a toolbox). |
| `private TextUtils() { }` | A **private constructor**: `new TextUtils()` is **impossible** from outside. Creating an object would make no sense — there's no data! |
| `new StringBuilder(clean).reverse()` | `StringBuilder` is a "changeable String" with a handy `reverse()` method. |
| `split("\\s+")` | Split by "one or more spaces". `\\s+` is a **regular expression** (a pattern language for text) — just copy it for now. |

---

## ⚡ Part 7: Static blocks

A **static block** runs **once**, the first time the class is used. It's for preparing **complicated** static data:

```java
public class Countries {
    static final String[] NAMES;

    static {
        System.out.println("(loading country list...)");
        NAMES = new String[] { "Brazil", "Egypt", "India", "Japan", "Kenya" };
    }

    public static void main(String[] args) {
        System.out.println("Program starts");
        System.out.println(NAMES.length + " countries");
    }
}
```

**Output:**

```
(loading country list...)
Program starts
5 countries
```

The static block runs **before** `main`, because `main` is in this class. You won't need static blocks often — just know they exist. 😊

---

## 👑 Part 8: The Singleton idea

Sometimes you want **exactly one** object of a class in the whole program. For example: **one** settings object, **one** database connection pool.

```java
public class AppSettings {
    private static final AppSettings INSTANCE = new AppSettings();   // the ONE object

    private String language = "English";
    private boolean darkMode = false;

    private AppSettings() { }   // nobody else can call "new"

    public static AppSettings getInstance() {
        return INSTANCE;
    }

    public String getLanguage()           { return language; }
    public void setLanguage(String lang)  { this.language = lang; }
    public boolean isDarkMode()           { return darkMode; }
    public void setDarkMode(boolean on)   { this.darkMode = on; }
}
```

```java
AppSettings s1 = AppSettings.getInstance();
AppSettings s2 = AppSettings.getInstance();

s1.setDarkMode(true);
System.out.println(s2.isDarkMode());   // true — it's the SAME object!
System.out.println(s1 == s2);          // true
```

| Code | Meaning |
|---|---|
| `private static final AppSettings INSTANCE = new AppSettings();` | Create the **one** object, store it in a static field. |
| `private AppSettings()` | Nobody outside can make another one. |
| `public static AppSettings getInstance()` | The only way to get it. Always returns the **same** object. |

> 🌱 **Spring Boot note:** You will almost **never** write a Singleton yourself in Spring Boot. Why? Because **Spring does it for you!** By default, Spring creates **one** object of each of your services (`@Service`), controllers (`@RestController`), etc. — and gives that same object to everyone who needs it. These objects are called **beans** (Chapter 54). 🫘

---

## ⚠️ Part 9: Don't overuse `static`!

Beginners often think: "`static` makes errors go away, so let's make **everything** static!" 🙈 **Please don't.**

| Problem with too much `static` | Why it's bad |
|---|---|
| **Shared state everywhere** | Any code can change a static field at any time → bugs that are very hard to find 🕵️ |
| **No polymorphism** | Static methods can't be overridden (Chapter 23). You lose the power of interfaces. |
| **Hard to test** | You can't replace a static method with a fake one for testing (Chapter 85). |
| **Not OOP** | You're back to Part 2 style: data and functions separate. |
| **Spring can't help** | Spring's Dependency Injection works with **objects** (instances), not static methods. 🌱 |

```java
// 👎 Static everywhere — tight coupling, can't swap, can't test
public class OrderService {
    public static void placeOrder(String customer) {
        EmailSender.send(customer, "Thanks!");   // static call — glued forever 🧲
    }
}

// 👍 Objects + interfaces — loose coupling (Chapter 25)
public class OrderService {
    private final MessageSender sender;
    public OrderService(MessageSender sender) { this.sender = sender; }
    public void placeOrder(String customer) {
        sender.send(customer, "Thanks!");        // any sender can be plugged in 🔌
    }
}
```

### ✅ Good uses of `static`

- **Constants**: `static final int MAX = 10;`
- **Pure helper functions** that don't need object data: `Math.max`, `TextUtils.capitalize`
- **`main`**
- **Factory methods** that create objects: `List.of(...)`, `LocalDate.now()` (you'll see these soon)
- Simple **counters** for learning

### ❌ Bad uses of `static`

- To "fix" the error *"non-static ... cannot be referenced from a static context"* without thinking
- For data that belongs to **one** object (`name`, `balance`)
- For services, repositories, controllers in Spring Boot

---

## 💻 Mini project: Bank with interest rate 🏦

```java
public class SavingsAccount {
    // ----- static (shared by ALL accounts) -----
    private static double interestRate = 0.02;   // 2% — the same for everyone
    private static int accountCount = 0;
    private static double totalMoneyInBank = 0;

    // ----- instance (each account has its own) -----
    private final String owner;
    private double balance;

    public SavingsAccount(String owner, double balance) {
        this.owner = owner;
        this.balance = balance;
        accountCount++;
        totalMoneyInBank += balance;
    }

    // instance method: uses THIS account's balance + the shared rate
    public void addMonthlyInterest() {
        double interest = balance * interestRate;
        balance += interest;
        totalMoneyInBank += interest;
    }

    @Override
    public String toString() {
        return String.format("%-6s %8.2f", owner, balance);
    }

    // static methods: about the bank in general, not one account
    public static void setInterestRate(double newRate) {
        if (newRate >= 0 && newRate <= 0.1) {
            interestRate = newRate;
        }
    }

    public static void printBankSummary() {
        System.out.printf("🏦 Accounts: %d | Rate: %.1f%% | Total: %.2f%n",
                accountCount, interestRate * 100, totalMoneyInBank);
    }

    public static void main(String[] args) {
        SavingsAccount[] accounts = {
            new SavingsAccount("Sara", 1000),
            new SavingsAccount("Tom", 2500),
            new SavingsAccount("Lina", 400)
        };
        SavingsAccount.printBankSummary();

        for (SavingsAccount acc : accounts) {
            acc.addMonthlyInterest();
        }
        System.out.println("After month 1 (2%):");
        for (SavingsAccount acc : accounts) {
            System.out.println("  " + acc);
        }

        SavingsAccount.setInterestRate(0.05);   // the bank changes the rate for EVERYONE
        for (SavingsAccount acc : accounts) {
            acc.addMonthlyInterest();
        }
        System.out.println("After month 2 (5%):");
        for (SavingsAccount acc : accounts) {
            System.out.println("  " + acc);
        }
        SavingsAccount.printBankSummary();
    }
}
```

**Output:**

```
🏦 Accounts: 3 | Rate: 2.0% | Total: 3900.00
After month 1 (2%):
  Sara    1020.00
  Tom     2550.00
  Lina     408.00
After month 2 (5%):
  Sara    1071.00
  Tom     2677.50
  Lina     428.40
🏦 Accounts: 3 | Rate: 5.0% | Total: 4176.90
```

### 🔍 Static or not?

| Member | static? | Why |
|---|---|---|
| `interestRate` | ✅ | The **same** for all accounts. Change it once → all accounts use the new rate. |
| `accountCount`, `totalMoneyInBank` | ✅ | Information about the **whole bank**. |
| `owner`, `balance` | ❌ | **Each** account has its own. |
| `addMonthlyInterest()` | ❌ | Changes **one** account's balance. |
| `setInterestRate()`, `printBankSummary()` | ✅ | About the **bank**, not about one account. |

> 💡 `%%` in `printf` prints a real `%` sign (Chapter 9).

---

## ✋ Try it yourself

**Task 1:** Add a static method `getCount()` to the `Student` class from Part 1, and make `count` private.

<details>
<summary>Click to see the answer</summary>

```java
public class Student {
    private String name;
    private static int count = 0;

    public Student(String name) {
        this.name = name;
        count++;
    }

    public static int getCount() {
        return count;
    }
}

// in main:
new Student("A");
new Student("B");
System.out.println(Student.getCount());   // 2
```

</details>

**Task 2:** Make a utility class `MathUtils` with static methods `isEven(int)`, `factorial(int)` and `average(int[])`. Give it a private constructor.

**Task 3:** Find and fix the error **without** making `greet` static:

```java
public class Hello {
    public static void main(String[] args) {
        greet("Sara");
    }

    void greet(String name) {
        System.out.println("Hi " + name);
    }
}
```

<details>
<summary>Click to see the answer</summary>

```java
public static void main(String[] args) {
    Hello hello = new Hello();
    hello.greet("Sara");
}
```

</details>

**Task 4:** Static or instance? Decide for each member of a class `Car`:
1. `color`
2. `numberOfCarsMade`
3. `drive()`
4. `MAX_SPEED_LIMIT` (the law for all cars)
5. `convertKmToMiles(double km)`

<details>
<summary>Click to see the answer</summary>

1. instance — each car has its own color
2. static — shared counter
3. instance — a specific car drives
4. static final — a shared constant
5. static — a pure helper that doesn't need a car's data

</details>

**Task 5:** Make a class `IdGenerator` with a static method `nextId(String prefix)` that returns IDs like `"USER-1"`, `"USER-2"`... using a static counter.

---

## ⚠️ Common mistakes

### Mistake 1: "non-static ... cannot be referenced from a static context"

The most common Java error message! It means: **you're inside a static method, trying to use something that needs an object.**

**Fix:** Create an object and use it — or, if the member really doesn't need object data, make it static.

### Mistake 2: Making a field static by accident

```java
public class Player {
    static String name;   // ❌ ALL players share ONE name!
}

Player a = new Player(); a.name = "Ali";
Player b = new Player(); b.name = "Sara";
System.out.println(a.name);   // Sara 😱
```

**Fix:** Remove `static`.

### Mistake 3: Accessing static members through objects

```java
a.count   // ⚠️ works, but confusing
Student.count   // ✅ clear: it belongs to the class
```

### Mistake 4: Using `this` in a static method

```java
static void reset() {
    this.count = 0;   // ❌ error: no "this" in static methods
}
```

**Fix:** `count = 0;` or `Student.count = 0;`

### Mistake 5: Expecting static methods to be overridden

```java
class Animal { static void info() { System.out.println("Animal"); } }
class Dog extends Animal { static void info() { System.out.println("Dog"); } }

Animal a = new Dog();
a.info();   // "Animal" 😮 — static methods don't use polymorphism!
```

**Fix:** Use instance methods for behavior that should change in child classes.

---

## ✅ Summary

- **`static`** = belongs to the **class**, not to each object. There's only **one**, shared by all. 📋
- **Static field**: one shared value. Use `ClassName.field`.
- **Static method**: called with `ClassName.method()`. No object needed. Good for helpers like `Math.sqrt`.
- Static methods have **no `this`** → they can't use instance fields or methods directly.
- `main` is static because no objects exist when the program starts.
- Fix "non-static ... from a static context" by **creating an object** (or making the member static if it really should be).
- **`static final`** = a constant: `MAX_PLAYERS`.
- **Utility class**: `final` class, private constructor, only static methods.
- **Singleton**: only one object. (Spring Boot does this for you with **beans**.)
- **Don't overuse static!** It breaks polymorphism, testing and Spring's Dependency Injection. Use it for constants, pure helpers, and `main`.

---

## ❓ Quiz

1. What does `static` mean?
2. 3 `Dog` objects exist. A static field `count` exists how many times? A normal field `name`?
3. How do you call a static method `toKm` in class `Converter`?
4. Why can't a static method use `this`?
5. Why is `main` static?
6. What does `static final` mean?
7. Why does a utility class have a private constructor?
8. Give two reasons not to make everything static.

<details>
<summary>Click to see the answers</summary>

1. It belongs to the class itself, not to each object. There's only one copy, shared by all objects.
2. `count`: **once**. `name`: **3 times** (one per dog).
3. `Converter.toKm(...)`
4. Because a static method doesn't belong to any object — there's no "current object".
5. Because when the program starts, no objects exist. The JVM must be able to call `main` without creating an object.
6. A constant: one shared value that can never change.
7. So nobody can create an object of it — it has no object data, only static methods.
8. For example: static methods can't be overridden (no polymorphism); static code is hard to test; Spring's Dependency Injection works with objects; shared static state causes hard-to-find bugs.

</details>

---

[⬅ Previous chapter](26-packages-import.md) | [Table of Contents](../README.md) | [Next chapter: Enums ➡](28-enums.md)
