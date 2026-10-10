# Chapter 29 – Records: Small Classes for Data

[⬅ Previous chapter](28-enums.md) | [Table of Contents](../README.md) | [Next chapter ➡](../part-04-more-java/30-lists.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **record** is, and why it saves **a lot** of typing
- What Java **writes for you** in a record
- How to read a record's data (`name()` — not `getName()`!)
- How to **check** values with a **compact constructor**
- How to add **methods** to a record
- What records **can't** do
- **Record patterns**: taking a record apart in `instanceof` and `switch`
- Why records are **perfect** for Spring Boot **DTOs** 🌱
- A **Part 3 review project** 🎓

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Record** | A short way to write an **immutable** class that just **carries data**. |
| **Component** | One piece of data in a record, like `name` or `age`. |
| **Accessor** | The method that reads a component: `name()`. |
| **Canonical constructor** | The **main** constructor with all the components. Java writes it for you. |
| **Compact constructor** | A short way to add **checks** to the canonical constructor. |
| **Boilerplate** | Boring code you must write again and again, that doesn't do anything special. |
| **DTO** | *Data Transfer Object.* A simple object that **carries data** from one place to another (for example, from the web to your program). |
| **Deconstruct** | Take an object **apart** into its pieces. |

---

## 📖 Story: The pre-printed form 🧾

In Chapters 19–21, you learned to write a good data class: private final fields, a constructor, getters, `toString`, `equals`, `hashCode`... That's a **lot** of writing for "a point has an x and a y"! ✍️😩

Imagine you go to a shop to order business cards. You could:
- **Option A:** Design the card yourself: choose the paper, draw the layout, pick the font, print it... 🎨🖨️
- **Option B:** Fill in a **simple form**: Name: ___, Phone: ___, Email: ___. The shop does **everything else**. ✅

A **record** is Option B. You only say **what data** you have. Java does everything else.

---

## 😩 Part 1: The problem — so much boilerplate

Here's a "proper" immutable class for a point (Chapters 19–21):

```java
import java.util.Objects;

public final class Point {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Point point = (Point) o;
        return x == point.x && y == point.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }

    @Override
    public String toString() {
        return "Point[x=" + x + ", y=" + y + "]";
    }
}
```

**About 35 lines** — just to say "a point has an x and a y". 😵

---

## ✨ Part 2: The same thing as a record

```java
public record Point(int x, int y) { }
```

**One line.** 🤯 And it does **everything** the 35-line class does!

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `public` | Everyone can use it. |
| `record` | "This is a **record**: a class that just carries data." |
| `Point` | The name. |
| `(int x, int y)` | The **components**: the data it carries. This is called the **header**. |
| `{ }` | The body. Empty — nothing more needed! |

### 🎁 What Java writes for you

From `record Point(int x, int y)`, Java **automatically** creates:

| Generated | Looks like |
|---|---|
| `private final` fields | `private final int x;` `private final int y;` |
| A constructor with all components | `public Point(int x, int y) { this.x = x; this.y = y; }` |
| **Accessor** methods | `public int x()` and `public int y()` |
| `equals()` | compares **all** components |
| `hashCode()` | made from **all** components |
| `toString()` | `Point[x=3, y=4]` |
| The class is `final` | no children |

### Using it

```java
public class Main {
    public static void main(String[] args) {
        Point a = new Point(3, 4);
        Point b = new Point(3, 4);
        Point c = new Point(0, 0);

        System.out.println(a);              // Point[x=3, y=4]
        System.out.println(a.x());          // 3
        System.out.println(a.y());          // 4
        System.out.println(a.equals(b));    // true  ✅ same content
        System.out.println(a == b);         // false (two different objects)
        System.out.println(a.equals(c));    // false
    }
}
```

### ⚠️ Accessors: `x()`, not `getX()`!

| Normal class (Chapter 21) | Record |
|---|---|
| `point.getX()` | `point.x()` |
| `person.getName()` | `person.name()` |
| `user.isActive()` | `user.active()` |

The accessor has the **same name** as the component. This is a common beginner mistake! 😊

> 🌱 **Good news:** Spring Boot (and the JSON library it uses, called **Jackson**) understands records perfectly. You don't need `getX()` for Spring to read your records.

---

## 🧊 Part 3: Records are immutable

All record fields are **`final`**. After creation, nothing can change:

```java
Point p = new Point(3, 4);
p.x = 10;       // ❌ error: cannot assign a value to final variable x
p.setX(10);     // ❌ error: cannot find symbol — there are no setters!
```

To "change" a record, make a **new** one (like `String` and `Money` in Chapter 21):

```java
Point moved = new Point(p.x() + 1, p.y());
```

👉 Immutable = **safe**. You can pass a record anywhere, and you know nobody will change it behind your back. 🛡️

---

## 🛡️ Part 4: Checking values — the compact constructor

What if someone creates a `Person` with a negative age? We want to **check**, just like in Chapter 19.

```java
public record Person(String name, int age) {

    public Person {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name cannot be empty");
        }
        if (age < 0 || age > 150) {
            throw new IllegalArgumentException("Invalid age: " + age);
        }
        name = name.strip();
    }
}
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `public Person {` | ⚠️ A **compact constructor**: no `( )` brackets and no parameters! Java already knows the parameters from the header. |
| `if (...) { throw ... }` | Check the values. If bad → **throw an exception** (stop with an error). We learn exceptions in Chapter 33 — for now, read it as "stop and complain". |
| `name = name.strip();` | You can **change the parameter** before it's saved. (Notice: **no** `this.` — you change the parameter, and Java saves it **after** your code.) |
| (no `this.name = name;`) | Java adds the field assignments **automatically at the end**. |

```java
Person ok = new Person("  Sara  ", 30);
System.out.println(ok);   // Person[name=Sara, age=30]  ← spaces removed!

Person bad = new Person("Tom", -5);
// 💥 Exception in thread "main" java.lang.IllegalArgumentException: Invalid age: -5
```

👉 Now it's **impossible** to create a Person with a bad age. 🛡️

---

## ➕ Part 5: Adding methods and more

A record body can have extra **methods**, **static methods** and **extra constructors**:

```java
public record Rectangle(double width, double height) {

    // extra constructor: a square
    public Rectangle(double side) {
        this(side, side);
    }

    // normal methods
    public double area() {
        return width * height;
    }

    public boolean isSquare() {
        return width == height;
    }

    // "wither": return a NEW record with one thing changed
    public Rectangle withWidth(double newWidth) {
        return new Rectangle(newWidth, height);
    }

    // static factory method
    public static Rectangle unit() {
        return new Rectangle(1, 1);
    }
}
```

```java
Rectangle r = new Rectangle(4, 3);
System.out.println(r.area());           // 12.0
System.out.println(r.isSquare());       // false

Rectangle wide = r.withWidth(10);
System.out.println(wide);               // Rectangle[width=10.0, height=3.0]
System.out.println(r);                  // Rectangle[width=4.0, height=3.0]  ← unchanged!

System.out.println(new Rectangle(5));   // Rectangle[width=5.0, height=5.0]
System.out.println(Rectangle.unit());   // Rectangle[width=1.0, height=1.0]
```

| Code | Meaning |
|---|---|
| `this(side, side)` | An extra constructor must call the **main** (canonical) constructor with `this(...)`. |
| `width * height` | Inside the record, you can use the fields directly. |
| `withWidth(...)` | A "**wither**" — a common pattern for immutable objects: "give me a copy **with** a different width". |

### Records can implement interfaces

```java
public interface Shape {
    double area();
}

public record Circle(double radius) implements Shape {
    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}

public record Square(double side) implements Shape {
    @Override
    public double area() {
        return side * side;
    }
}
```

```java
Shape[] shapes = { new Circle(1), new Square(2) };
for (Shape s : shapes) {
    System.out.printf("%s → area %.2f%n", s, s.area());
}
```

**Output:**

```
Circle[radius=1.0] → area 3.14
Square[side=2.0] → area 4.00
```

Polymorphism works with records too! 🎭

---

## 🚫 Part 6: What records can't do

| ❌ Not allowed | Why |
|---|---|
| `extends` another class | A record already extends `java.lang.Record`. (Only one parent — Chapter 22.) |
| Be extended (have children) | Records are `final`. |
| Have extra **instance fields** | All data must be in the header. (Static fields are OK.) |
| Have setters / change fields | All fields are `final`. |

```java
public record User(String name) {
    private int loginCount;   // ❌ error: field declaration must be static
}
```

### ⚠️ Careful with arrays and lists inside records

```java
public record Team(String name, String[] players) { }

String[] list = { "Ali", "Sara" };
Team team = new Team("Tigers", list);
list[0] = "HACKED";
System.out.println(team.players()[0]);   // HACKED 😱
```

The **field** `players` can't point to another array, but the array **itself** can still be changed (remember references — Chapter 18)! For true safety, make a **copy** in the compact constructor:

```java
public record Team(String name, String[] players) {
    public Team {
        players = players.clone();
    }
}
```

(With **lists**, you'll use `List.copyOf(...)` — Chapter 30.)

---

## 🆚 Part 7: Record or class?

| Use a **record** when... | Use a normal **class** when... |
|---|---|
| it's mostly **data** | it has important **behavior** and **changing state** |
| the data **doesn't change** | fields must **change** (a bank account's balance) |
| equality = "same data" | equality = "same identity" (same database row) |
| Examples: `Point`, `Money`, `Address`, `StudentRequest`, `ApiResponse` | Examples: `BankAccount`, `Hero`, `GameBoard`, `StudentService` |

> 🌱 **Spring Boot note:** Database **entities** (Chapter 71) are usually normal classes, not records, because the database tools need to **change** their fields and need an empty constructor. But **DTOs** (the data you send and receive on the web) are **perfect** for records!

---

## 🧩 Part 8: Record patterns (Java 21+)

Records can be **taken apart** (deconstructed) directly in `instanceof` and `switch`:

```java
Object obj = new Point(3, 4);

if (obj instanceof Point(int x, int y)) {
    System.out.println("x = " + x + ", y = " + y);   // x = 3, y = 4
}
```

| Part | Meaning |
|---|---|
| `obj instanceof Point(int x, int y)` | "If `obj` is a Point, **take it apart** and give me its `x` and `y` as variables." |

### With switch — very elegant ✨

```java
public static double area(Shape shape) {
    return switch (shape) {
        case Circle(double r) -> Math.PI * r * r;
        case Square(double side) -> side * side;
        default -> 0;
    };
}
```

You'll see this style more and more in modern Java. For now, just know it exists! 😊

---

## 🌱 Part 9: Records in Spring Boot — DTOs

In Spring Boot, data comes from the **web** as **JSON** (Chapter 45). For example, when someone creates a new student:

```json
{
  "name": "Sara",
  "email": "sara@mail.com",
  "age": 20
}
```

You write a record that **matches** it:

```java
public record CreateStudentRequest(String name, String email, int age) { }
```

And Spring **automatically** turns the JSON into your record (and records back into JSON):

```java
@PostMapping("/students")
public StudentResponse create(@RequestBody CreateStudentRequest request) {
    // request.name() → "Sara"
    // request.email() → "sara@mail.com"
    ...
}
```

Short, safe, immutable, with `toString` for logging and `equals` for testing. 🎉 This is why records are **loved** by Spring Boot developers. You'll write many of them in Part 8!

---

## 🎓 Part 10: Part 3 review project — Online Shop 🛒

This project uses **everything** from Part 3. Read it slowly and find each concept!

**File: `Category.java`** — an enum with fields (Chapter 28)

```java
public enum Category {
    BOOKS("📚", 0.0),
    ELECTRONICS("💻", 0.20),
    FOOD("🍎", 0.05);

    private final String icon;
    private final double taxRate;

    Category(String icon, double taxRate) {
        this.icon = icon;
        this.taxRate = taxRate;
    }

    public String getIcon()    { return icon; }
    public double getTaxRate() { return taxRate; }
}
```

**File: `Product.java`** — a record with validation (Chapter 29)

```java
public record Product(String name, double price, Category category) {
    public Product {
        if (price < 0) {
            throw new IllegalArgumentException("Price cannot be negative");
        }
    }

    public double priceWithTax() {
        return price * (1 + category.getTaxRate());
    }
}
```

**File: `Discount.java`** — an interface (Chapter 25)

```java
public interface Discount {
    double apply(double total);
    String describe();
}
```

**File: `NoDiscount.java`, `PercentDiscount.java`, `FixedDiscount.java`** — implementations

```java
public class NoDiscount implements Discount {
    @Override
    public double apply(double total) { return total; }

    @Override
    public String describe() { return "no discount"; }
}
```

```java
public class PercentDiscount implements Discount {
    private final double percent;

    public PercentDiscount(double percent) {
        this.percent = percent;
    }

    @Override
    public double apply(double total) {
        return total * (1 - percent / 100);
    }

    @Override
    public String describe() {
        return percent + "% off";
    }
}
```

```java
public class FixedDiscount implements Discount {
    private final double amount;

    public FixedDiscount(double amount) {
        this.amount = amount;
    }

    @Override
    public double apply(double total) {
        return Math.max(0, total - amount);
    }

    @Override
    public String describe() {
        return amount + " off";
    }
}
```

**File: `CartItem.java`** — a record (Chapter 29)

```java
public record CartItem(Product product, int quantity) {
    public CartItem {
        if (quantity <= 0) {
            throw new IllegalArgumentException("Quantity must be at least 1");
        }
    }

    public double total() {
        return product.priceWithTax() * quantity;
    }
}
```

**File: `ShoppingCart.java`** — encapsulation, static, `this`, loose coupling (Chapters 20, 21, 25, 27)

```java
public class ShoppingCart {
    private static final int MAX_ITEMS = 10;
    private static int cartsCreated = 0;

    private final String customer;
    private final CartItem[] items = new CartItem[MAX_ITEMS];
    private int count = 0;
    private final Discount discount;

    public ShoppingCart(String customer, Discount discount) {
        this.customer = customer;
        this.discount = discount;
        cartsCreated++;
    }

    public ShoppingCart(String customer) {
        this(customer, new NoDiscount());
    }

    public ShoppingCart add(Product product, int quantity) {
        if (count == MAX_ITEMS) {
            System.out.println("⚠️ Cart is full!");
            return this;
        }
        items[count] = new CartItem(product, quantity);
        count++;
        return this;
    }

    public double subtotal() {
        double sum = 0;
        for (int i = 0; i < count; i++) {
            sum += items[i].total();
        }
        return sum;
    }

    public double total() {
        return discount.apply(subtotal());
    }

    public void printReceipt() {
        System.out.println("🧾 Receipt for " + customer);
        for (int i = 0; i < count; i++) {
            CartItem item = items[i];
            Product p = item.product();
            System.out.printf("  %s %-12s x%d %8.2f%n",
                    p.category().getIcon(), p.name(), item.quantity(), item.total());
        }
        System.out.printf("  Subtotal: %26.2f%n", subtotal());
        System.out.printf("  Discount: %26s%n", discount.describe());
        System.out.printf("  TOTAL:    %26.2f%n%n", total());
    }

    public static int getCartsCreated() {
        return cartsCreated;
    }
}
```

**File: `ShopApp.java`** — polymorphism and putting it all together (Chapter 23)

```java
public class ShopApp {
    public static void main(String[] args) {
        Product book = new Product("Java Book", 30.00, Category.BOOKS);
        Product laptop = new Product("Laptop", 800.00, Category.ELECTRONICS);
        Product apple = new Product("Apple", 0.50, Category.FOOD);

        new ShoppingCart("Sara")
                .add(book, 2)
                .add(apple, 6)
                .printReceipt();

        new ShoppingCart("Tom", new PercentDiscount(10))
                .add(laptop, 1)
                .add(book, 1)
                .printReceipt();

        new ShoppingCart("Lina", new FixedDiscount(5))
                .add(apple, 4)
                .printReceipt();

        System.out.println("Carts created today: " + ShoppingCart.getCartsCreated());
    }
}
```

**Output:**

```
🧾 Receipt for Sara
  📚 Java Book    x2    60.00
  🍎 Apple        x6     3.15
  Subtotal:                      63.15
  Discount:                no discount
  TOTAL:                         63.15

🧾 Receipt for Tom
  💻 Laptop       x1   960.00
  📚 Java Book    x1    30.00
  Subtotal:                     990.00
  Discount:                  10.0% off
  TOTAL:                        891.00

🧾 Receipt for Lina
  🍎 Apple        x4     2.10
  Subtotal:                       2.10
  Discount:                    5.0 off
  TOTAL:                          0.00

Carts created today: 3
```

### 🔍 Find the concepts! 🕵️

| Concept | Where | Chapter |
|---|---|---|
| Classes and objects | `ShoppingCart`, `new ShoppingCart(...)` | 18 |
| Constructors, `this(...)` | `ShoppingCart(String customer)` calls the other one | 19 |
| `this`, method chaining | `add(...)` returns `this` | 20 |
| Encapsulation | `private` fields, `public` methods, no setters | 21 |
| Interface + implementations | `Discount`, `PercentDiscount`, `FixedDiscount`, `NoDiscount` | 25 |
| Polymorphism | `discount.apply(...)` — 3 different behaviors | 23 |
| Loose coupling (DI by hand) | the cart **receives** a `Discount` in its constructor | 25 |
| `static` | `MAX_ITEMS`, `cartsCreated`, `getCartsCreated()` | 27 |
| Enum with fields | `Category` with icon and tax rate | 28 |
| Records with validation and methods | `Product`, `CartItem` | 29 |
| Objects inside objects | `CartItem` has a `Product`, `Product` has a `Category` | 18 |

> 🤔 Lina's total is `0.00` because the fixed discount (5.0) is bigger than her subtotal (2.10). `Math.max(0, ...)` makes sure the total is never negative. Good rule! 👍

---

## ✋ Try it yourself

**Task 1:** Write a record `Book(String title, String author, int year)`. Create two equal books and check `equals`. Print one.

**Task 2:** Add a compact constructor to `Book` that refuses a `year` in the future (bigger than 2030) and an empty title.

**Task 3:** Write a record `Money(double amount, String currency)` with a method `Money plus(Money other)` that throws an exception if the currencies are different.

<details>
<summary>Click to see the answer</summary>

```java
public record Money(double amount, String currency) {
    public Money {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
    }

    public Money plus(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("Different currencies: " + currency + " and " + other.currency);
        }
        return new Money(amount + other.amount, currency);
    }
}

// in main:
Money a = new Money(10, "USD");
Money b = new Money(5, "USD");
System.out.println(a.plus(b));   // Money[amount=15.0, currency=USD]
```

</details>

**Task 4:** Change the `Point` class from Chapter 20 into a record. Add a method `double distanceTo(Point other)`.

**Task 5:** In the shop project, add a new discount type `BuyMoreSaveMore`: 5% off if the subtotal is over 50, 15% off if over 500. Did you need to change `ShoppingCart`? (You shouldn't! 😉)

**Task 6:** Add a new category `TOYS` (🧸, 10% tax) to the enum, and a teddy bear product. What did you need to change?

---

## ⚠️ Common mistakes

### Mistake 1: Using `getName()` on a record

```java
person.getName();   // ❌ error: cannot find symbol
person.name();      // ✅
```

### Mistake 2: Trying to change a record

```java
p.x = 5;   // ❌ error: cannot assign a value to final variable x
```

**Fix:** Create a new record: `new Point(5, p.y())` (or write a "wither" method).

### Mistake 3: Writing `this.name = name` in a compact constructor

```java
public Person {
    this.name = name;   // ❌ error: cannot assign a value to final variable name
}
```

In a compact constructor, Java assigns the fields **for you** at the end. Just change the **parameter**: `name = name.strip();`

### Mistake 4: Adding an instance field

```java
public record User(String name) {
    int visits;   // ❌ error: field declaration must be static
}
```

**Fix:** Add it to the header: `record User(String name, int visits)`.

### Mistake 5: Using a record where data must change

A `BankAccount` whose balance changes all the time is **not** a good record. Use a normal class.

### Mistake 6: Extra constructor not calling `this(...)`

```java
public record Rectangle(double w, double h) {
    public Rectangle(double side) {
        // ❌ error: constructor is not canonical, so its first statement must invoke another constructor
    }
}
```

**Fix:** `this(side, side);`

---

## ✅ Summary

- A **record** is a short way to write an **immutable data class**: `public record Point(int x, int y) { }`
- Java **generates**: private final fields, constructor, accessors (`x()`, **not** `getX()`), `equals`, `hashCode`, `toString`.
- Records are **immutable** and **final**. To "change" one, create a new one (a "wither").
- **Compact constructor** `public Person { ... }` — for checks and cleanup. Change the **parameters**; Java assigns the fields at the end.
- Records can have **methods**, **static methods**, **extra constructors** (that call `this(...)`), and can **implement interfaces**.
- Records **can't** extend classes, have children, or have extra instance fields.
- **Record patterns**: `if (obj instanceof Point(int x, int y))` and in `switch`.
- Use **records** for data (DTOs, values). Use **classes** for objects with changing state and behavior.
- Spring Boot loves records for **DTOs** (JSON in and out). 🌱

---

## ❓ Quiz

1. What does `record Point(int x, int y)` generate automatically? (Name 4 things.)
2. How do you read the `x` value of a Point record?
3. Can you change a record's field after it's created?
4. What is a compact constructor? What is it used for?
5. Can a record extend another class? Can it implement an interface?
6. Should a `BankAccount` with a changing balance be a record?
7. `new Point(1, 2).equals(new Point(1, 2))` — true or false?
8. Why are records good for Spring Boot DTOs?

<details>
<summary>Click to see the answers</summary>

1. Private final fields, a constructor, accessor methods (`x()`, `y()`), `equals()`, `hashCode()`, `toString()`.
2. `point.x()`
3. No — records are immutable.
4. A constructor without parentheses (`public Point { ... }`). It's used to check and clean the values before Java saves them in the fields.
5. No. Yes.
6. No — its data changes often. Use a normal class.
7. `true` — records compare their content.
8. They are short to write, immutable (safe), have `toString`/`equals` for free, and Spring turns JSON into records (and back) automatically.

</details>

---

## 🎉 Part 3 complete!

You now understand **Object-Oriented Programming** — the heart of Java:

- ✅ Classes and objects
- ✅ Constructors and `this`
- ✅ Encapsulation (`private`, getters, setters)
- ✅ Inheritance and polymorphism
- ✅ Abstract classes and interfaces
- ✅ Packages and access modifiers
- ✅ `static`
- ✅ Enums and records

This was the **hardest** part of Java. 🏔️ If some things are still a little unclear, that's **normal** — they will become clearer as you use them in Spring Boot. You can always come back to these chapters. 😊

In **Part 4**, we learn the tools that **every** Spring Boot program uses: **Lists**, **Maps**, **exceptions**, **lambdas** and **streams**. Let's go! 🚀

---

[⬅ Previous chapter](28-enums.md) | [Table of Contents](../README.md) | [Next chapter: Lists ➡](../part-04-more-java/30-lists.md)
