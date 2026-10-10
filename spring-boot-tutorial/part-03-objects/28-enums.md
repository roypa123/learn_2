# Chapter 28 – Enums: A Fixed List of Choices

[⬅ Previous chapter](27-static.md) | [Table of Contents](../README.md) | [Next chapter ➡](29-records.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What an **enum** is, and why it's **safer** than Strings or numbers
- How to **create** and **use** an enum
- How to use enums in **`switch`**
- Useful enum methods: `values()`, `valueOf()`, `name()`, `ordinal()`
- How to give enums **fields**, **constructors** and **methods**
- How enums are used in **Spring Boot** 🌱

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Enum** | Short for *enumeration* (a numbered list). A type with a **fixed list** of possible values. |
| **Constant** | One value in the enum, like `MONDAY` or `RED`. |
| **Type-safe** | The compiler **checks** that you use only allowed values. Typos become **errors**, not bugs. |
| **`values()`** | A method that gives **all** the constants of an enum. |
| **`valueOf()`** | A method that turns a **String** into an enum constant. |
| **`ordinal()`** | The **position** of a constant (starting at 0). |

---

## 📖 Story: The traffic light 🚦

A traffic light can be **only** these colors:

🔴 RED · 🟡 YELLOW · 🟢 GREEN

Never purple. Never "rde" (a typo). Never 42. **Only** these three.

Or think of a **multiple-choice question** on a test:

```
 What is the capital of France?
   (A) London   (B) Paris   (C) Rome   (D) Berlin
```

You **can't** answer "(E)" or "banana". 🍌 There's a **fixed list** of choices.

An **enum** is a type with a **fixed list** of choices. Java **refuses** anything else.

---

## 😩 Part 1: The problem with Strings and numbers

How would you store the size of a coffee? ☕

### Option 1: Strings

```java
String size = "MEDIUM";
```

Problems:

```java
String size = "medum";     // 😱 typo — Java doesn't notice!
String size = "Medium";    // 😱 different capital letters — is it the same?
String size = "HUGE";      // 😱 not on the menu!
String size = "banana";    // 😱😱
```

Java accepts **any** text. Bugs appear **later**, when the program runs.

### Option 2: Numbers

```java
int size = 2;   // 1 = small, 2 = medium, 3 = large
```

Problems:
- What does `2` mean? You need to remember (or look up) the code. 🤔
- `int size = 7;` — Java accepts it. 😱

### ✅ Option 3: an enum

```java
public enum CoffeeSize {
    SMALL, MEDIUM, LARGE
}
```

```java
CoffeeSize size = CoffeeSize.MEDIUM;   // ✅
CoffeeSize size = CoffeeSize.MEDUM;    // ❌ error: cannot find symbol — typo caught immediately!
CoffeeSize size = CoffeeSize.HUGE;     // ❌ error — not in the list!
CoffeeSize size = "MEDIUM";            // ❌ error — a String is not a CoffeeSize
```

🎉 **Only** the three values are possible. Typos are caught **before** the program even runs. This is called **type-safe**.

---

## 🏗️ Part 2: Creating and using an enum

**File: `Day.java`**

```java
public enum Day {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `public enum Day` | `enum` instead of `class`. "Here is a type called `Day` with a fixed list of values." |
| `MONDAY, TUESDAY, ...` | The **constants** (the allowed values), separated by commas. Written in **UPPER_CASE** (they are constants!). |

An enum usually lives in its **own file**, like a class (`Day.java`). It can also be written **inside** a class.

### Using it

```java
public class Main {
    public static void main(String[] args) {
        Day today = Day.FRIDAY;

        System.out.println("Today is " + today);

        if (today == Day.SATURDAY || today == Day.SUNDAY) {
            System.out.println("Weekend! 🎉");
        } else {
            System.out.println("Work day. 💼");
        }
    }
}
```

**Output:**

```
Today is FRIDAY
Work day. 💼
```

### 🔍 Key ideas

| Code | Meaning |
|---|---|
| `Day today` | A variable of type `Day`. It can hold **only** one of the 7 days (or `null`). |
| `Day.FRIDAY` | One constant. Use `EnumName.CONSTANT`. |
| `println(today)` | Prints the **name**: `FRIDAY`. |
| `today == Day.SATURDAY` | ✅ For enums, **`==` is correct and safe**! Each constant exists **only once** in the whole program (like a Singleton — Chapter 27). |

> 💡 Remember: for **Strings**, use `.equals()`. For **enums**, `==` is perfect (and `.equals()` also works).

---

## 🔀 Part 3: Enums in `switch`

Enums and `switch` are **best friends**! 🤝

```java
public static String activity(Day day) {
    return switch (day) {
        case MONDAY, TUESDAY, WEDNESDAY, THURSDAY -> "Go to school 🏫";
        case FRIDAY -> "School, then movie night 🍿";
        case SATURDAY -> "Football ⚽";
        case SUNDAY -> "Visit grandma 👵";
    };
}
```

```java
System.out.println(activity(Day.FRIDAY));    // School, then movie night 🍿
System.out.println(activity(Day.SUNDAY));    // Visit grandma 👵
```

### 🔍 Two nice things

| | |
|---|---|
| `case MONDAY` | Inside a switch, you write just `MONDAY`, **not** `Day.MONDAY`. Java already knows the type. |
| No `default` needed! | We listed **all 7** days. Java **knows** that every possibility is covered. 🎯 |

And if you **forget** one day in a switch expression:

```
❌ error: the switch expression does not cover all possible input values
```

Java reminds you! If you later **add** a new constant to the enum (like `HOLIDAY`), Java shows an error in **every** switch that forgot it. No more missing cases. 🛡️

---

## 🧰 Part 4: Built-in enum methods

Every enum gets some methods **for free**:

```java
public enum Planet {
    MERCURY, VENUS, EARTH, MARS
}
```

### `values()` — all constants, as an array

```java
for (Planet p : Planet.values()) {
    System.out.println(p);
}
```

**Output:**

```
MERCURY
VENUS
EARTH
MARS
```

Great for menus and dropdown lists!

### `name()` and `toString()` — the name as a String

```java
Planet home = Planet.EARTH;
String text = home.name();   // "EARTH"
```

### `ordinal()` — the position (from 0)

```java
System.out.println(Planet.MERCURY.ordinal());   // 0
System.out.println(Planet.EARTH.ordinal());     // 2
```

> ⚠️ Don't build important logic on `ordinal()`. If someone adds a planet in the middle, all the numbers change! 😱 Use **fields** instead (Part 5).

### `valueOf()` — String → enum

```java
Planet p = Planet.valueOf("MARS");
System.out.println(p);   // MARS
```

Very useful when the user **types** a value, or when data comes from a **file** or the **web**:

```java
Scanner scanner = new Scanner(System.in);
System.out.print("Choose a size (SMALL, MEDIUM, LARGE): ");
String input = scanner.nextLine().strip().toUpperCase();
CoffeeSize size = CoffeeSize.valueOf(input);
```

> ⚠️ If the text doesn't match **exactly**, it crashes:
> ```java
> Planet.valueOf("Pluto");   // 💥 IllegalArgumentException: No enum constant Planet.Pluto
> Planet.valueOf("mars");    // 💥 (small letters don't match!)
> ```
> Use `.toUpperCase()` on user input, and handle errors with `try/catch` (Chapter 33).

### `compareTo()` — enums are comparable

```java
System.out.println(Planet.MERCURY.compareTo(Planet.MARS) < 0);   // true — MERCURY comes first
```

Enums sort in the **order you wrote them**.

### 📋 Summary table

| Method | Returns | Example | Result |
|---|---|---|---|
| `Enum.values()` | array of all constants | `Day.values().length` | `7` |
| `Enum.valueOf("X")` | the constant named "X" | `Day.valueOf("MONDAY")` | `Day.MONDAY` |
| `c.name()` | the name as String | `Day.MONDAY.name()` | `"MONDAY"` |
| `c.ordinal()` | position from 0 | `Day.WEDNESDAY.ordinal()` | `2` |
| `c.compareTo(d)` | negative / 0 / positive | | by order in the list |

---

## 💎 Part 5: Enums with fields, constructors and methods

Here's where enums become **really powerful**. An enum is actually a special **class**. Each constant is an **object**! So enums can have **fields**, a **constructor** and **methods**.

### Example: coffee sizes with prices ☕

```java
public enum CoffeeSize {
    SMALL(250, 2.50),
    MEDIUM(350, 3.20),
    LARGE(500, 4.00);

    private final int milliliters;
    private final double price;

    CoffeeSize(int milliliters, double price) {
        this.milliliters = milliliters;
        this.price = price;
    }

    public int getMilliliters() {
        return milliliters;
    }

    public double getPrice() {
        return price;
    }

    public String describe() {
        return name().charAt(0) + name().substring(1).toLowerCase()
                + " (" + milliliters + " ml) — $" + price;
    }
}
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `SMALL(250, 2.50),` | A constant **with arguments**. Java calls the constructor: `new CoffeeSize(250, 2.50)` — automatically! |
| `LARGE(500, 4.00);` | ⚠️ The **last** constant ends with `;` (semicolon) when more code follows. |
| `private final int milliliters;` | A field. Every constant has its **own** value. |
| `CoffeeSize(int milliliters, double price)` | The constructor. ⚠️ Enum constructors are **always private** — you can **never** call `new CoffeeSize(...)` yourself. Only the constants in the list exist! |
| `getPrice()` | A normal method. |

### Using it

```java
for (CoffeeSize size : CoffeeSize.values()) {
    System.out.println(size.describe());
}

CoffeeSize order = CoffeeSize.LARGE;
int cups = 3;
System.out.println("Total: $" + order.getPrice() * cups);
```

**Output:**

```
Small (250 ml) — $2.5
Medium (350 ml) — $3.2
Large (500 ml) — $4.0
Total: $12.0
```

👉 The price **belongs** to the size. You don't need a separate `if` or `switch` to find the price. Everything about "LARGE" is **in one place**. 🎯

### Example: planets with real data 🪐

```java
public enum Planet {
    MERCURY(3.303e+23, 2.4397e6),
    VENUS(4.869e+24, 6.0518e6),
    EARTH(5.976e+24, 6.37814e6),
    MARS(6.421e+23, 3.3972e6);

    private static final double G = 6.67300E-11;   // gravity constant

    private final double mass;     // in kg
    private final double radius;   // in meters

    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }

    public double surfaceGravity() {
        return G * mass / (radius * radius);
    }

    public double weightOf(double earthWeight) {
        double massOfPerson = earthWeight / EARTH.surfaceGravity();
        return massOfPerson * surfaceGravity();
    }
}
```

```java
double myWeight = 60;   // kg on Earth
for (Planet p : Planet.values()) {
    System.out.printf("On %-8s you would weigh %6.2f%n", p, p.weightOf(myWeight));
}
```

**Output:**

```
On MERCURY  you would weigh  22.67
On VENUS    you would weigh  54.30
On EARTH    you would weigh  60.00
On MARS     you would weigh  22.72
```

> 💡 `3.303e+23` is **scientific notation**: 3.303 × 10²³. Useful for very big or very small numbers.

---

## 🎭 Part 6: Enums can implement interfaces and have different behavior

Each constant can even have its **own version** of a method:

```java
public enum Operation {
    PLUS("+") {
        @Override
        public double apply(double a, double b) { return a + b; }
    },
    MINUS("-") {
        @Override
        public double apply(double a, double b) { return a - b; }
    },
    TIMES("*") {
        @Override
        public double apply(double a, double b) { return a * b; }
    },
    DIVIDE("/") {
        @Override
        public double apply(double a, double b) { return a / b; }
    };

    private final String symbol;

    Operation(String symbol) {
        this.symbol = symbol;
    }

    public String getSymbol() {
        return symbol;
    }

    public abstract double apply(double a, double b);
}
```

```java
double x = 12, y = 4;
for (Operation op : Operation.values()) {
    System.out.println(x + " " + op.getSymbol() + " " + y + " = " + op.apply(x, y));
}
```

**Output:**

```
12.0 + 4.0 = 16.0
12.0 - 4.0 = 8.0
12.0 * 4.0 = 48.0
12.0 / 4.0 = 3.0
```

Polymorphism inside an enum! 🤯 (This is an **advanced** trick — you don't need it often, but it's cool to know.)

---

## 🌱 Part 7: Enums in Spring Boot

Enums are used **everywhere** in real applications:

```java
public enum OrderStatus {
    NEW, PAID, SHIPPED, DELIVERED, CANCELLED
}

public enum Role {
    USER, ADMIN, MODERATOR
}

public enum Gender {
    FEMALE, MALE, OTHER, PREFER_NOT_TO_SAY
}
```

In Spring Boot:

| Where | How enums are used |
|---|---|
| **Database** (Chapter 71) | Save an enum in a table column with `@Enumerated(EnumType.STRING)` → stored as `"PAID"` |
| **JSON / web** (Chapter 45) | Spring turns `OrderStatus.PAID` into `"PAID"` in JSON, and back again — automatically! |
| **Security** (Chapter 82) | Roles like `ADMIN` and `USER` decide who can do what |
| **Spring itself** | `HttpStatus.NOT_FOUND`, `HttpMethod.GET`, `RequestMethod.POST` are all enums! |

> ⚠️ **Database tip:** Always store enums as **text** (`STRING`), not as numbers (`ORDINAL`). If you add a new constant in the middle, the numbers change and your old data becomes **wrong**! 😱 (Remember the `ordinal()` warning in Part 4.)

---

## 💻 Mini project: Order tracking 📦

```java
public enum OrderStatus {
    NEW("🆕", "Order received"),
    PAID("💳", "Payment confirmed"),
    SHIPPED("🚚", "On the way"),
    DELIVERED("📦", "Delivered"),
    CANCELLED("❌", "Cancelled");

    private final String icon;
    private final String description;

    OrderStatus(String icon, String description) {
        this.icon = icon;
        this.description = description;
    }

    public String getIcon()        { return icon; }
    public String getDescription() { return description; }

    public boolean canMoveTo(OrderStatus next) {
        return switch (this) {
            case NEW -> next == PAID || next == CANCELLED;
            case PAID -> next == SHIPPED || next == CANCELLED;
            case SHIPPED -> next == DELIVERED;
            case DELIVERED, CANCELLED -> false;   // final states
        };
    }
}
```

```java
public class Order {
    private final int id;
    private OrderStatus status = OrderStatus.NEW;

    public Order(int id) {
        this.id = id;
    }

    public void moveTo(OrderStatus next) {
        if (status.canMoveTo(next)) {
            System.out.println("Order #" + id + ": " + status + " → " + next + " " + next.getIcon());
            status = next;
        } else {
            System.out.println("Order #" + id + ": ⛔ can't go from " + status + " to " + next);
        }
    }

    public void printStatus() {
        System.out.println("Order #" + id + " is " + status.getIcon() + " " + status.getDescription());
    }

    public static void main(String[] args) {
        Order order = new Order(1001);
        order.printStatus();

        order.moveTo(OrderStatus.SHIPPED);     // ⛔ not paid yet!
        order.moveTo(OrderStatus.PAID);
        order.moveTo(OrderStatus.SHIPPED);
        order.moveTo(OrderStatus.CANCELLED);   // ⛔ too late!
        order.moveTo(OrderStatus.DELIVERED);

        order.printStatus();
    }
}
```

**Output:**

```
Order #1001 is 🆕 Order received
Order #1001: ⛔ can't go from NEW to SHIPPED
Order #1001: NEW → PAID 💳
Order #1001: PAID → SHIPPED 🚚
Order #1001: ⛔ can't go from SHIPPED to CANCELLED
Order #1001: SHIPPED → DELIVERED 📦
Order #1001 is 📦 Delivered
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `private OrderStatus status = OrderStatus.NEW;` | Every new order starts as `NEW`. The status can **only** be one of 5 values. |
| `canMoveTo(...)` in the enum | The **rules** live with the data. Everything about statuses is in **one place**. |
| `switch (this)` | Inside the enum, `this` is the current constant (`NEW`, `PAID`...). |
| No `default` in the switch | All 5 statuses are covered. Add a 6th → Java tells you to update this switch. 🛡️ |

This kind of design is called a **state machine** 🔄 — very common for orders, tickets, payments, and workflows.

---

## ✋ Try it yourself

**Task 1:** Make an enum `Season` (`WINTER`, `SPRING`, `SUMMER`, `AUTUMN`). Write a method that returns a clothing tip for each season using a `switch`.

**Task 2:** Make an enum `Size` with `S`, `M`, `L`, `XL`. Ask the user to type a size with `Scanner`. Use `valueOf` (with `toUpperCase()`) and print `"You chose: M"`. What happens if they type `XXL`?

**Task 3:** Make an enum `Coin` with `PENNY(1)`, `NICKEL(5)`, `DIME(10)`, `QUARTER(25)`. Add a field `cents` and a getter. Calculate the total of an array of coins: `{QUARTER, QUARTER, DIME, PENNY}` → 61 cents.

<details>
<summary>Click to see the answer</summary>

```java
public enum Coin {
    PENNY(1), NICKEL(5), DIME(10), QUARTER(25);

    private final int cents;

    Coin(int cents) {
        this.cents = cents;
    }

    public int getCents() {
        return cents;
    }
}

// in main:
Coin[] pocket = { Coin.QUARTER, Coin.QUARTER, Coin.DIME, Coin.PENNY };
int total = 0;
for (Coin c : pocket) {
    total += c.getCents();
}
System.out.println(total + " cents");   // 61 cents
```

</details>

**Task 4:** Make an enum `TrafficLight` (`RED`, `YELLOW`, `GREEN`) with a method `next()` that returns the next light (RED → GREEN → YELLOW → RED). Loop 6 times and print the lights.

<details>
<summary>Click to see the answer</summary>

```java
public enum TrafficLight {
    RED, YELLOW, GREEN;

    public TrafficLight next() {
        return switch (this) {
            case RED -> GREEN;
            case GREEN -> YELLOW;
            case YELLOW -> RED;
        };
    }
}

// in main:
TrafficLight light = TrafficLight.RED;
for (int i = 0; i < 6; i++) {
    System.out.println(light);
    light = light.next();
}
```

</details>

**Task 5:** Add a `Role` enum (`GUEST`, `USER`, `ADMIN`) with a method `boolean canDelete()` — only `ADMIN` can delete. Add a field `level` (0, 1, 2) and a method `boolean isAtLeast(Role other)`.

---

## ⚠️ Common mistakes

### Mistake 1: Using `new` on an enum

```java
Day d = new Day();   // ❌ error: enum classes may not be instantiated
```

**Fix:** Use a constant: `Day d = Day.MONDAY;`

### Mistake 2: Writing `Day.MONDAY` in a switch case

```java
switch (day) {
    case Day.MONDAY -> ...   // ❌ error before Java 21 (allowed in Java 21+, but not needed)
    case MONDAY -> ...       // ✅
}
```

### Mistake 3: `valueOf` with wrong text

```java
Day.valueOf("monday");   // 💥 IllegalArgumentException
```

**Fix:** `Day.valueOf(input.strip().toUpperCase())` and handle bad input.

### Mistake 4: Forgetting the `;` after the last constant

```java
public enum Size {
    SMALL(1), LARGE(2)     // ❌ missing ; before the fields
    private final int n;
}
```

**Fix:** `LARGE(2);`

### Mistake 5: Relying on `ordinal()`

```java
if (status.ordinal() > 2) { ... }   // 👎 breaks if someone adds a constant
```

**Fix:** Use a field or a method like `canMoveTo`.

### Mistake 6: A public enum constructor

```java
public CoffeeSize(int ml) { ... }   // ❌ error: modifier public not allowed here
```

Enum constructors are always private. Just leave out the modifier.

---

## ✅ Summary

- An **enum** is a type with a **fixed list** of values: `enum Day { MONDAY, TUESDAY, ... }`.
- **Type-safe**: typos and invalid values are compile **errors**. Much safer than Strings or ints.
- Use a value: `Day.FRIDAY`. Compare with `==`.
- Great in **`switch`**: write `case FRIDAY ->`. If all constants are covered, no `default` needed — and Java warns you when you forget one.
- Free methods: `values()`, `valueOf("X")`, `name()`, `ordinal()`, `compareTo()`.
- Enums are special **classes**: they can have **fields**, a (private) **constructor** and **methods**. Each constant is **one object**.
- Put data and rules **with** the enum (prices, icons, allowed transitions).
- Spring Boot uses enums for statuses, roles, `HttpStatus`... Store them as **STRING** in databases.

---

## ❓ Quiz

1. What is an enum?
2. Why is an enum safer than a String for a coffee size?
3. How do you compare two enum values?
4. What does `Day.values()` return?
5. What happens with `Day.valueOf("Funday")`?
6. Can an enum have fields and methods?
7. Can you call `new CoffeeSize(...)`?
8. Why should you not depend on `ordinal()`?

<details>
<summary>Click to see the answers</summary>

1. A type with a fixed list of possible values (constants).
2. Java only allows the listed values. Typos or invalid values cause a compile error, not a hidden bug.
3. With `==` (`.equals()` also works).
4. An array with all the constants, in the order they were written.
5. It crashes with `IllegalArgumentException` (no such constant).
6. Yes — fields, a constructor and methods.
7. No. Enum constructors are private; only the listed constants exist.
8. Because if someone adds or moves a constant, all the positions change.

</details>

---

[⬅ Previous chapter](27-static.md) | [Table of Contents](../README.md) | [Next chapter: Records ➡](29-records.md)
