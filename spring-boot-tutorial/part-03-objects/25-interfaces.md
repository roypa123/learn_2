# Chapter 25 – Interfaces: A Promise

[⬅ Previous chapter](24-abstract-classes.md) | [Table of Contents](../README.md) | [Next chapter ➡](26-packages-import.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What an **interface** is (a **promise** or **contract**)
- How a class **implements** an interface
- How one class can implement **many** interfaces
- How to use an interface as a **type** (polymorphism without a family!)
- **`default`** and **`static`** methods in interfaces
- The difference between an **interface** and an **abstract class**
- Java's own interfaces: **`Comparable`** and **`Runnable`**
- **Loose coupling** — the idea that makes **Spring Boot** possible 🌱

> 🌱 **This is one of the most important chapters for Spring Boot.** Spring is built on interfaces. Your repositories will be interfaces. Dependency Injection (Chapter 53) works because of interfaces. Read slowly! 🐢

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Interface** | A list of methods that a class **promises** to have. A **contract**. |
| **Implement** | **Keep the promise**: write all the methods of an interface. |
| **`implements`** | The keyword to say "this class keeps this interface's promise". |
| **Contract** | An agreement: "If you are an X, you **must** be able to do Y." |
| **Default method** | A method in an interface **with** a body. Classes get it for free, but can override it. |
| **Coupling** | How much one class **depends on** another class's details. |
| **Loose coupling** | Classes depend on **interfaces**, not on specific classes. Easy to change! 👍 |
| **Tight coupling** | Classes depend on specific classes. Hard to change. 👎 |

---

## 📖 Story: The power socket 🔌

Look at the power socket in your wall. It's a **standard shape**.

- A **lamp** 💡 can plug in.
- A **phone charger** 📱 can plug in.
- A **TV** 📺 can plug in.
- A **toaster** 🍞 can plug in.

The socket doesn't care **what** you plug in. It only cares that the plug has the **right shape**. And the lamp doesn't care **how** the electricity is made (sun ☀️, wind 🌬️, water 💧). They only agree on the **plug shape**.

That **plug shape** is an **interface**: a **promise** that says "If you have this shape, you can connect."

- The lamp, charger, TV and toaster are **completely different** things. They are **not family** (no common parent class).
- But they all **keep the same promise** (the plug shape).

---

## 🤝 Part 1: Your first interface

Let's say different things in our program can **fly**: a bird 🐦, a plane ✈️, a superhero 🦸. They are **not** family — a plane is **not** an animal! So inheritance doesn't fit. But they share an **ability**: flying.

**File: `Flyable.java`**

```java
public interface Flyable {
    void fly();
    int getMaxHeight();
}
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `public interface Flyable {` | `interface` instead of `class`. "Here is a **promise** called Flyable." |
| `void fly();` | "Anyone who is Flyable **must** have a `fly()` method." No body — just the promise. (Like an abstract method.) |
| `int getMaxHeight();` | "...and a `getMaxHeight()` method that returns an int." |

> 💡 In an interface, methods are automatically **`public`** and **`abstract`**. You don't need to write those words.

> 💡 **Naming:** Interface names are often **adjectives** ending in **-able**: `Flyable`, `Comparable`, `Runnable`, `Printable`. Or **nouns** for a role: `PaymentService`, `StudentRepository`.

### Keeping the promise — `implements`

**File: `Bird.java`**

```java
public class Bird implements Flyable {
    private final String name;

    public Bird(String name) {
        this.name = name;
    }

    @Override
    public void fly() {
        System.out.println("🐦 " + name + " flaps its wings and flies!");
    }

    @Override
    public int getMaxHeight() {
        return 1000;
    }
}
```

**File: `Airplane.java`**

```java
public class Airplane implements Flyable {
    private final String model;

    public Airplane(String model) {
        this.model = model;
    }

    @Override
    public void fly() {
        System.out.println("✈️ " + model + " starts its engines and takes off!");
    }

    @Override
    public int getMaxHeight() {
        return 12000;
    }
}
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `class Bird implements Flyable` | "Bird **promises** to do everything in Flyable." |
| `@Override public void fly()` | Keep the promise: write the method. ⚠️ It **must** be `public`. |

If the class **forgets** a method:

```
❌ error: Bird is not abstract and does not override abstract method getMaxHeight() in Flyable
```

Java checks that you **keep your promise**. 🤝

---

## 🎭 Part 2: The interface as a type

Here's the magic. You can use the **interface** as a variable type:

```java
Flyable f1 = new Bird("Tweety");
Flyable f2 = new Airplane("Boeing 747");

f1.fly();
f2.fly();
```

**Output:**

```
🐦 Tweety flaps its wings and flies!
✈️ Boeing 747 starts its engines and takes off!
```

And arrays and methods:

```java
public class Sky {
    public static void main(String[] args) {
        Flyable[] flyers = {
            new Bird("Tweety"),
            new Airplane("Boeing 747"),
            new Bird("Eagle")
        };

        for (Flyable f : flyers) {
            f.fly();
        }

        System.out.println("Highest: " + findHighest(flyers) + " m");
    }

    public static int findHighest(Flyable[] flyers) {
        int max = 0;
        for (Flyable f : flyers) {
            max = Math.max(max, f.getMaxHeight());
        }
        return max;
    }
}
```

**Output:**

```
🐦 Tweety flaps its wings and flies!
✈️ Boeing 747 starts its engines and takes off!
🐦 Eagle flaps its wings and flies!
Highest: 12000 m
```

👉 **Polymorphism without a family!** A bird and an airplane have **nothing** in common — except the promise to fly. 🐦✈️

```
              «interface»
               Flyable
              fly()
              getMaxHeight()
              ▲         ▲
   implements │         │ implements
              │         │
           Bird      Airplane
      (an animal)   (a machine)
```

> ⚠️ Just like abstract classes, you **can't** do `new Flyable()`. An interface is only a promise — there's nothing inside to create!

---

## 🦸 Part 3: Many interfaces at once

A class can extend only **one** class (Chapter 22). But it can implement **many** interfaces! 🎉

```java
public interface Swimmable {
    void swim();
}

public interface Walkable {
    void walk();
}
```

```java
public class Duck implements Flyable, Swimmable, Walkable {
    @Override
    public void fly() {
        System.out.println("🦆 Duck flies over the lake!");
    }

    @Override
    public int getMaxHeight() {
        return 500;
    }

    @Override
    public void swim() {
        System.out.println("🦆 Duck swims in the pond!");
    }

    @Override
    public void walk() {
        System.out.println("🦆 Duck walks: waddle waddle!");
    }
}
```

```java
Duck donald = new Duck();

Flyable f = donald;     // a duck can be seen as a Flyable
Swimmable s = donald;   // ...or as a Swimmable
Walkable w = donald;    // ...or as a Walkable

f.fly();
s.swim();
w.walk();
```

**Output:**

```
🦆 Duck flies over the lake!
🦆 Duck swims in the pond!
🦆 Duck walks: waddle waddle!
```

🎭 **Story:** A person can be a **student**, a **swimmer** and a **guitar player** at the same time. Each is a different "role" with different abilities. Interfaces are **roles**.

### Extend a class AND implement interfaces

```java
public class Penguin extends Animal implements Swimmable, Walkable {
    ...
}
```

Rule: `extends` first (only one), then `implements` (as many as you want).

---

## 🎁 Part 4: `default` methods — a method with a body

Since Java 8, an interface can have methods **with** a body, using the word **`default`**:

```java
public interface Greeter {
    String getName();

    default void greet() {
        System.out.println("Hello, I am " + getName() + "! 👋");
    }
}
```

```java
public class Robot implements Greeter {
    @Override
    public String getName() {
        return "R2-D2";
    }
    // greet() comes for free!
}

public class Pirate implements Greeter {
    @Override
    public String getName() {
        return "Captain Jack";
    }

    @Override
    public void greet() {                  // override the default
        System.out.println("Ahoy! I be " + getName() + "! 🏴‍☠️");
    }
}
```

```java
new Robot().greet();    // Hello, I am R2-D2! 👋
new Pirate().greet();   // Ahoy! I be Captain Jack! 🏴‍☠️
```

| | |
|---|---|
| `default void greet() { ... }` | A method with a body. Every class that implements `Greeter` **gets it for free**. |
| Override it? | Optional. A class **can** write its own version. |

👉 **Why do default methods exist?** To add **new** methods to an old interface **without breaking** all the classes that already implement it. The Java team used this to add many new features to old interfaces.

### `static` methods in interfaces

An interface can also have `static` helper methods:

```java
public interface Greeter {
    String getName();

    static Greeter of(String name) {
        return () -> name;   // a lambda — Chapter 35!
    }
}
```

You call them on the interface: `Greeter.of("Sara")`. (Don't worry about `() -> name` yet — it's a **lambda**, a short way to implement a one-method interface. Chapter 35.)

### Constants in interfaces

Fields in an interface are automatically `public static final` (constants):

```java
public interface Speeds {
    int WALKING = 5;        // public static final int WALKING = 5;
    int CYCLING = 20;
}
```

(But many programmers prefer to put constants in a class or enum — Chapter 28.)

---

## ⚖️ Part 5: Interface vs. abstract class

This is a **common job interview question**! 🎤

| | Abstract class | Interface |
|---|---|---|
| Keyword | `abstract class` / `extends` | `interface` / `implements` |
| How many can a class use? | **one** | **many** |
| Fields (state) | ✅ any fields | ❌ only constants |
| Constructors | ✅ yes | ❌ no |
| Methods with body | ✅ yes | ✅ only `default`, `static`, `private` |
| Abstract methods | ✅ yes | ✅ yes (all normal methods) |
| Relationship | "**is-a**" — a family | "**can-do**" — an ability / role |
| Example | `Dog extends Animal` | `Bird implements Flyable` |

### 🤔 Which one should I use?

| Use an **abstract class** when... | Use an **interface** when... |
|---|---|
| the classes are a real **family** ("is-a") | unrelated classes share an **ability** ("can-do") |
| they share **fields** and **code** | you only need to describe **what** to do, not **how** |
| you need a **constructor** | a class may need **many** of them |
| | you want **loose coupling** (Part 7) ⭐ |

👉 **Modern advice:** **Start with an interface.** Use an abstract class only if you really need to share fields or code. In Spring Boot, you'll see **many more interfaces** than abstract classes.

### Both together!

Often, they work together:

```java
public interface Shape {               // the PROMISE
    double area();
    double perimeter();
}

public abstract class Polygon implements Shape {   // SHARED CODE for some shapes
    protected double[] sides;
    @Override
    public double perimeter() { ... sum the sides ... }
}

public class Rectangle extends Polygon { ... }     // REAL shape
public class Circle implements Shape { ... }       // a circle is not a polygon, but still a Shape!
```

---

## ☕ Part 6: Java's own interfaces

Java comes with many interfaces. Here are two you'll meet a lot.

### `Comparable` — "I can be sorted"

Remember `Arrays.sort()` (Chapter 14)? It works for numbers and Strings. But how can it sort **your** objects? Java doesn't know if students should be sorted by name, age or grade!

You must **promise** that your objects can be compared — by implementing `Comparable`:

```java
public class Student implements Comparable<Student> {
    private final String name;
    private final int grade;

    public Student(String name, int grade) {
        this.name = name;
        this.grade = grade;
    }

    @Override
    public int compareTo(Student other) {
        return Integer.compare(this.grade, other.grade);
    }

    @Override
    public String toString() {
        return name + "(" + grade + ")";
    }
}
```

```java
import java.util.Arrays;

Student[] students = {
    new Student("Sara", 92),
    new Student("Tom", 75),
    new Student("Lina", 88)
};

Arrays.sort(students);
System.out.println(Arrays.toString(students));
```

**Output:**

```
[Tom(75), Lina(88), Sara(92)]
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `implements Comparable<Student>` | "Students can be compared **with other Students**." The `<Student>` is a **generic** — Chapter 34 explains it. |
| `int compareTo(Student other)` | The promised method. It must return: **negative** if `this` comes **before** `other`, **0** if equal, **positive** if `this` comes **after**. |
| `Integer.compare(a, b)` | A helper that returns exactly that: negative / 0 / positive. |

`Arrays.sort` doesn't know anything about students. It just calls `compareTo` — the **promise**. 🤝

### `Runnable` — "I can be run"

```java
public interface Runnable {
    void run();
}
```

Used for tasks that can run on their own (for example, in the background). You'll see it when we learn about **scheduling** (Chapter 91).

---

## 🔌 Part 7: Loose coupling — the secret of Spring Boot 🌱

This part is **the most important** for your future with Spring Boot. Let's see the problem first.

### 😩 Tight coupling (bad)

```java
public class EmailSender {
    public void send(String to, String message) {
        System.out.println("📧 Email to " + to + ": " + message);
    }
}

public class OrderService {
    private final EmailSender sender = new EmailSender();   // ← tightly coupled!

    public void placeOrder(String customer) {
        System.out.println("🛒 Order placed for " + customer);
        sender.send(customer, "Thank you for your order!");
    }
}
```

**Problems:**
- What if the boss says: "Let's send **SMS** instead of email"? You must **change** `OrderService`. 😩
- What if you want to **test** `OrderService` without sending real emails? You can't — it **always** creates a real `EmailSender`.
- `OrderService` is **glued** to `EmailSender`. 🧲

### 😍 Loose coupling (good)

**Step 1:** Make an interface — the **promise**:

```java
public interface MessageSender {
    void send(String to, String message);
}
```

**Step 2:** Make classes that **keep** the promise:

```java
public class EmailSender implements MessageSender {
    @Override
    public void send(String to, String message) {
        System.out.println("📧 Email to " + to + ": " + message);
    }
}

public class SmsSender implements MessageSender {
    @Override
    public void send(String to, String message) {
        System.out.println("📱 SMS to " + to + ": " + message);
    }
}

public class FakeSender implements MessageSender {
    @Override
    public void send(String to, String message) {
        System.out.println("🧪 (test) pretending to send: " + message);
    }
}
```

**Step 3:** `OrderService` depends on the **interface**, and **receives** the sender from outside (in the constructor):

```java
public class OrderService {
    private final MessageSender sender;   // ← only the INTERFACE!

    public OrderService(MessageSender sender) {   // ← someone GIVES us a sender
        this.sender = sender;
    }

    public void placeOrder(String customer) {
        System.out.println("🛒 Order placed for " + customer);
        sender.send(customer, "Thank you for your order!");
    }
}
```

**Step 4:** Choose the sender when you **build** the objects:

```java
public class Shop {
    public static void main(String[] args) {
        OrderService emailShop = new OrderService(new EmailSender());
        OrderService smsShop = new OrderService(new SmsSender());
        OrderService testShop = new OrderService(new FakeSender());

        emailShop.placeOrder("sara@mail.com");
        smsShop.placeOrder("+1-555-0100");
        testShop.placeOrder("test-user");
    }
}
```

**Output:**

```
🛒 Order placed for sara@mail.com
📧 Email to sara@mail.com: Thank you for your order!
🛒 Order placed for +1-555-0100
📱 SMS to +1-555-0100: Thank you for your order!
🛒 Order placed for test-user
🧪 (test) pretending to send: Thank you for your order!
```

### 🎉 What did we win?

| Before (tight) | After (loose) |
|---|---|
| `OrderService` creates `EmailSender` itself | `OrderService` **receives** any `MessageSender` |
| Switch to SMS → **change** OrderService | Switch to SMS → **don't touch** OrderService |
| Can't test without sending real emails | Use `FakeSender` for tests 🧪 |
| 🧲 glued | 🔌 plug and play |

```
     OrderService ───uses───►  «interface» MessageSender
                                     ▲        ▲        ▲
                                     │        │        │
                              EmailSender SmsSender FakeSender
```

### 🌱 This is EXACTLY what Spring Boot does!

What we did in Step 4 — **creating** the objects and **giving** each one what it needs — is called **Dependency Injection** (DI). 💉

In Spring Boot, **you don't write Step 4**. Spring does it **for you**, automatically! You just write:

```java
@Service
public class OrderService {
    private final MessageSender sender;

    public OrderService(MessageSender sender) {   // Spring sees this and gives you a sender! ✨
        this.sender = sender;
    }
}
```

We'll learn this properly in **Chapter 53**. But now you already understand the **idea** behind it. 🧠🎉

---

## 💻 Mini project: Payment system 💳

```java
public interface PaymentMethod {
    boolean pay(double amount);
    String getName();

    default void printReceipt(double amount) {
        System.out.printf("🧾 Paid %.2f with %s%n", amount, getName());
    }
}
```

```java
public class CreditCard implements PaymentMethod {
    private final String number;
    private double limit;

    public CreditCard(String number, double limit) {
        this.number = number;
        this.limit = limit;
    }

    @Override
    public boolean pay(double amount) {
        if (amount > limit) {
            return false;
        }
        limit -= amount;
        return true;
    }

    @Override
    public String getName() {
        return "Credit card ****" + number.substring(number.length() - 4);
    }
}
```

```java
public class Wallet implements PaymentMethod {
    private double cash;

    public Wallet(double cash) {
        this.cash = cash;
    }

    @Override
    public boolean pay(double amount) {
        if (amount > cash) {
            return false;
        }
        cash -= amount;
        return true;
    }

    @Override
    public String getName() {
        return "Cash wallet";
    }
}
```

```java
public class GiftCard implements PaymentMethod {
    private double balance;

    public GiftCard(double balance) {
        this.balance = balance;
    }

    @Override
    public boolean pay(double amount) {
        if (amount > balance) {
            return false;
        }
        balance -= amount;
        return true;
    }

    @Override
    public String getName() {
        return "Gift card";
    }

    @Override
    public void printReceipt(double amount) {
        System.out.printf("🎁 Gift card used for %.2f. Remaining: %.2f%n", amount, balance);
    }
}
```

```java
public class Checkout {
    private final PaymentMethod[] methods;

    public Checkout(PaymentMethod[] methods) {
        this.methods = methods;
    }

    public void buy(String item, double price) {
        System.out.println("🛍️ Buying " + item + " for " + price);
        for (PaymentMethod method : methods) {
            if (method.pay(price)) {
                method.printReceipt(price);
                return;
            }
            System.out.println("   ❌ " + method.getName() + " declined, trying next...");
        }
        System.out.println("   😢 No payment method worked.");
    }

    public static void main(String[] args) {
        PaymentMethod[] myMethods = {
            new GiftCard(20),
            new Wallet(50),
            new CreditCard("4111222233334444", 500)
        };

        Checkout checkout = new Checkout(myMethods);
        checkout.buy("Book", 15);
        checkout.buy("Shoes", 80);
        checkout.buy("Laptop", 1200);
    }
}
```

**Output:**

```
🛍️ Buying Book for 15.0
🎁 Gift card used for 15.00. Remaining: 5.00
🛍️ Buying Shoes for 80.0
   ❌ Gift card declined, trying next...
   ❌ Cash wallet declined, trying next...
🧾 Paid 80.00 with Credit card ****4444
🛍️ Buying Laptop for 1200.0
   ❌ Gift card declined, trying next...
   ❌ Cash wallet declined, trying next...
   ❌ Credit card ****4444 declined, trying next...
   😢 No payment method worked.
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `interface PaymentMethod` | The promise: every payment method can `pay` and has a `getName`. |
| `default void printReceipt` | A free method — `GiftCard` overrides it, the others use the default. |
| `Checkout` only knows `PaymentMethod` | **Loose coupling**: add `PayPal` or `BankTransfer` tomorrow — `Checkout` doesn't change! |
| `new Checkout(myMethods)` | We **give** Checkout what it needs (dependency injection, by hand). |

---

## ✋ Try it yourself

**Task 1:** Make an interface `Playable` with `play()` and `stop()`. Make `Song`, `Video` and `Podcast` classes. Put them in a `Playable[]` and play them all.

**Task 2:** Make an interface `Resizable` with `resize(double factor)`. Let your `Circle` and `Rectangle` (Chapter 24) implement both `Shape` and `Resizable`.

**Task 3:** Make `Product` implement `Comparable<Product>` so that `Arrays.sort` sorts products by **price**. Then change it to sort by **name** (hint: `this.name.compareTo(other.name)`).

<details>
<summary>Click to see the answer</summary>

```java
public class Product implements Comparable<Product> {
    private final String name;
    private final double price;

    public Product(String name, double price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public int compareTo(Product other) {
        return Double.compare(this.price, other.price);
        // by name: return this.name.compareTo(other.name);
    }

    @Override
    public String toString() {
        return name + " $" + price;
    }
}
```

</details>

**Task 4:** Add a `PayPal` payment method to the mini project. Did you need to change `Checkout`?

**Task 5:** Make an interface `Logger` with `log(String message)`. Make `ConsoleLogger` (prints to the screen) and `SilentLogger` (does nothing). Make a class `Calculator` that **receives** a `Logger` in its constructor and logs every calculation. Create one calculator with each logger.

<details>
<summary>Click to see the answer</summary>

```java
public interface Logger {
    void log(String message);
}

public class ConsoleLogger implements Logger {
    @Override
    public void log(String message) {
        System.out.println("[LOG] " + message);
    }
}

public class SilentLogger implements Logger {
    @Override
    public void log(String message) {
        // do nothing 🤫
    }
}

public class Calculator {
    private final Logger logger;

    public Calculator(Logger logger) {
        this.logger = logger;
    }

    public int add(int a, int b) {
        int result = a + b;
        logger.log(a + " + " + b + " = " + result);
        return result;
    }
}

// in main:
new Calculator(new ConsoleLogger()).add(2, 3);   // [LOG] 2 + 3 = 5
new Calculator(new SilentLogger()).add(2, 3);    // (nothing printed)
```

This is exactly the "loose coupling" idea! 🔌

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Using `extends` instead of `implements`

```java
public class Bird extends Flyable { }      // ❌ error: no interface expected here
public class Bird implements Flyable { }   // ✅
```

(But an interface **extends** another interface: `interface Pet extends Animal { }`.)

### Mistake 2: Forgetting `public` on the implemented method

```java
public class Bird implements Flyable {
    void fly() { }   // ❌ error: attempting to assign weaker access privileges; was public
}
```

Interface methods are **always public**, so your version must be `public` too.

### Mistake 3: Not implementing all methods

```
❌ error: Bird is not abstract and does not override abstract method getMaxHeight() in Flyable
```

**Fix:** **Alt + Enter → Implement methods** in IntelliJ. 🪄

### Mistake 4: `new` on an interface

```java
Flyable f = new Flyable();   // ❌ error: Flyable is abstract; cannot be instantiated
```

### Mistake 5: Calling a class-only method through the interface type

```java
Flyable f = new Duck();
f.swim();   // ❌ error: cannot find symbol — Flyable has no swim()
```

The variable type decides which methods you may call (Chapter 23).

### Mistake 6: Creating dependencies inside the class

```java
private final MessageSender sender = new EmailSender();   // 👎 tight coupling
```

**Better:** Receive it in the constructor. 👍

---

## ✅ Summary

- An **interface** is a **promise** (contract): a list of methods a class **must** have.
- `interface Flyable { void fly(); }` — methods are automatically `public abstract`.
- `class Bird implements Flyable` — the class **keeps the promise** by writing all the methods (as `public`).
- A class can implement **many** interfaces (but extend only **one** class).
- Use the interface as a **type**: `Flyable f = new Bird();` → polymorphism for **unrelated** classes.
- `default` methods have a body; classes get them for free. Interfaces can also have `static` methods and constants.
- **Abstract class** = "is-a" family with shared code and fields. **Interface** = "can-do" ability. Prefer interfaces.
- `Comparable<T>` with `compareTo` lets `Arrays.sort` sort your objects.
- **Loose coupling**: depend on **interfaces**, and **receive** the real object in the constructor. This is **Dependency Injection** — the heart of Spring Boot. 🌱💉

---

## ❓ Quiz

1. What is an interface?
2. What keyword does a class use to keep an interface's promise?
3. How many interfaces can a class implement? How many classes can it extend?
4. Can an interface have a method with a body?
5. Can you write `new Flyable()`?
6. Give one difference between an abstract class and an interface.
7. What must `compareTo` return?
8. Why is `private final MessageSender sender;` (received in the constructor) better than `private final EmailSender sender = new EmailSender();`?

<details>
<summary>Click to see the answers</summary>

1. A promise/contract: a list of methods that implementing classes must have.
2. `implements`
3. Many interfaces. Only one class.
4. Yes — `default` (and `static` / `private`) methods.
5. No.
6. For example: an abstract class can have fields and constructors; an interface can't. A class can implement many interfaces but extend only one abstract class.
7. A negative number (this comes first), 0 (equal) or a positive number (this comes after).
8. Because it's **loosely coupled**: you can give it any sender (email, SMS, fake for tests) without changing the class.

</details>

---

[⬅ Previous chapter](24-abstract-classes.md) | [Table of Contents](../README.md) | [Next chapter: Packages and import ➡](26-packages-import.md)
