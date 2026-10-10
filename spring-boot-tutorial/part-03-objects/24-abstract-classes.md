# Chapter 24 – Abstract Classes

[⬅ Previous chapter](23-polymorphism.md) | [Table of Contents](../README.md) | [Next chapter ➡](25-interfaces.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What an **abstract class** is, and why you **can't** create objects from it
- What an **abstract method** is (a method with **no body**)
- How child classes **must** fill in the abstract methods
- How to mix **normal** and **abstract** methods in one class
- The **Template Method** pattern — a famous way to use abstract classes
- When to use an abstract class

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Abstract** | An **idea**, not a real, complete thing. "Animal" is an idea; a "dog" is real. |
| **Abstract class** | A class that is **not complete**. You **can't** make objects from it with `new`. It's only a parent for other classes. |
| **Abstract method** | A method with a **name** but **no body** (no `{ }`). Children **must** write the body. |
| **Concrete class** | A normal, **complete** class. You **can** make objects from it. |
| **Concrete method** | A normal method **with** a body. |
| **Template** | A pattern with some **empty spaces** that others fill in. |

---

## 📖 Story: The form with empty fields 📝

Your school gives every student a **form**:

```
 ┌─────────────────────────────────────────┐
 │  SCHOOL TRIP PERMISSION FORM            │
 │                                         │
 │  Trip: Visit to the Science Museum 🔬   │  ← already filled by the school
 │  Date: May 10                           │  ← already filled by the school
 │  Bus leaves at 8:00                     │  ← already filled by the school
 │                                         │
 │  Student name: ____________________     │  ← YOU must fill this
 │  Parent signature: ________________     │  ← YOU must fill this
 └─────────────────────────────────────────┘
```

- Some parts are **already written** (the school did it for everyone).
- Some parts are **empty** — every student **must** fill them in. The form is **not valid** until you do.
- An empty form is useless. You can't go on the trip with an **empty** form!

An **abstract class** is like this form:
- **Concrete methods** = parts already written ✅
- **Abstract methods** = empty fields that each child **must** fill in ✏️
- You **can't** use the empty form itself (`new` is not allowed) — only a **filled** one (a child class).

---

## 🤔 Part 1: The problem

In Chapter 23, our `Shape` class had this:

```java
public class Shape {
    public double area() {
        return 0;   // 🤔 ???
    }
}
```

Two problems:

1. **What is the area of "a shape"?** It doesn't make sense. `0` is a fake answer.
2. **Someone can forget** to override `area()` in a child:

```java
public class Hexagon extends Shape {
    // oops, forgot area()! 😱
}

new Hexagon().area();   // returns 0 — a silent bug, no error!
```

3. **Someone can create** a meaningless plain shape:

```java
Shape s = new Shape("???");   // what shape is this?? 🤷
```

**Abstract classes fix all three problems.** 🎯

---

## 🧩 Part 2: Your first abstract class

```java
public abstract class Shape {
    protected String name;

    public Shape(String name) {
        this.name = name;
    }

    public abstract double area();

    public abstract double perimeter();

    public void describe() {
        System.out.printf("%s: area = %.2f, perimeter = %.2f%n", name, area(), perimeter());
    }
}
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `public abstract class Shape {` | `abstract` → "This class is **not complete**. You can't use `new Shape(...)`." |
| `protected String name;` | Abstract classes **can** have fields. ✅ |
| `public Shape(String name) { ... }` | And **constructors**! (Children call them with `super(...)`.) ✅ |
| `public abstract double area();` | An **abstract method**: it has a name, parameters and return type... but **no body**. ⚠️ It ends with `;` instead of `{ }`. It means: "Every shape **must** have an `area()` method, but I don't know how to calculate it. **Each child must write it.**" |
| `public abstract double perimeter();` | Another empty field to fill in. |
| `public void describe() { ... }` | A **normal (concrete)** method with a body. Children **inherit** it as usual. It even **calls** the abstract methods — that's OK! At run time, the child's version will run (polymorphism!). |

### 🚫 You can't create an abstract class

```java
Shape s = new Shape("blob");   // ❌ error: Shape is abstract; cannot be instantiated
```

### ✅ Children must fill in ALL abstract methods

```java
public class Circle extends Shape {
    private final double radius;

    public Circle(double radius) {
        super("Circle");
        this.radius = radius;
    }

    @Override
    public double area() {
        return Math.PI * radius * radius;
    }

    @Override
    public double perimeter() {
        return 2 * Math.PI * radius;
    }
}
```

If a child **forgets** one:

```java
public class Hexagon extends Shape {
    public Hexagon() { super("Hexagon"); }

    @Override
    public double area() { return 42; }
    // forgot perimeter()!
}
```

```
❌ error: Hexagon is not abstract and does not override abstract method perimeter() in Shape
```

🎉 Java **forces** you to write it. **No more silent bugs!** The compiler is your safety net. 🥅

### Using it

```java
Shape[] shapes = { new Circle(1), new Circle(2) };

for (Shape s : shapes) {
    s.describe();
}
```

**Output:**

```
Circle: area = 3.14, perimeter = 6.28
Circle: area = 12.57, perimeter = 12.57
```

👉 You **can** use `Shape` as a **variable type** and **array type** (polymorphism works!). You just can't do `new Shape(...)`.

---

## 📋 Part 3: The rules of abstract classes

| Rule | Example |
|---|---|
| Write `abstract` before `class` | `public abstract class Shape` |
| ❌ Can't use `new` on it | `new Shape()` → error |
| ✅ Can have fields | `protected String name;` |
| ✅ Can have constructors | called by children with `super(...)` |
| ✅ Can have normal (concrete) methods | `describe()` |
| ✅ Can have abstract methods (no body, ends with `;`) | `public abstract double area();` |
| A class with **any** abstract method **must** be abstract | otherwise: error |
| A normal child must **override all** abstract methods | otherwise: error |
| An **abstract** child doesn't have to | it passes the job to **its** children |
| ✅ Can be used as a type | `Shape s = new Circle(1);` |

### Abstract children

A child can **also** be abstract, and fill in only **some** of the empty fields:

```java
public abstract class Polygon extends Shape {
    protected double[] sides;

    public Polygon(String name, double... sides) {
        super(name);
        this.sides = sides;
    }

    @Override
    public double perimeter() {         // ✅ filled in for ALL polygons
        double sum = 0;
        for (double s : sides) {
            sum += s;
        }
        return sum;
    }

    // area() is still abstract — each polygon calculates it differently
}

public class Rectangle extends Polygon {
    public Rectangle(double w, double h) {
        super("Rectangle", w, h, w, h);
    }

    @Override
    public double area() {
        return sides[0] * sides[1];
    }
}
```

> 💡 `double... sides` is called **varargs** ("variable arguments"). It means "**any number** of doubles". Inside the method, `sides` is an array. So `super("Rectangle", w, h, w, h)` passes 4 sides.

```
          Shape (abstract)            area() ❓  perimeter() ❓
             │
          Polygon (abstract)          area() ❓  perimeter() ✅
             │
          Rectangle (concrete)        area() ✅  perimeter() ✅ (inherited)
```

---

## 🍳 Part 4: The Template Method pattern

This is the **most famous** use of abstract classes. The parent writes the **steps** (the recipe), and the children fill in **some** of the steps.

### 📖 Story: Making a hot drink ☕🍵

Making **tea** and making **coffee** have the **same steps**:

1. Boil water
2. **Brew** (tea: steep the tea bag / coffee: drip through the coffee)
3. Pour into a cup
4. **Add extras** (tea: lemon / coffee: milk and sugar)

Steps 1 and 3 are **always the same**. Steps 2 and 4 are **different**.

```java
public abstract class HotDrink {

    // The TEMPLATE METHOD: the recipe. final = children can't change the order!
    public final void prepare() {
        boilWater();
        brew();
        pourInCup();
        addExtras();
        System.out.println("✅ Your " + getName() + " is ready!\n");
    }

    // Same for everyone
    private void boilWater() {
        System.out.println("💧 Boiling water...");
    }

    private void pourInCup() {
        System.out.println("🫗 Pouring into a cup...");
    }

    // Each drink fills these in
    protected abstract void brew();
    protected abstract void addExtras();
    protected abstract String getName();
}
```

```java
public class Tea extends HotDrink {
    @Override
    protected void brew() {
        System.out.println("🍵 Steeping the tea bag for 3 minutes...");
    }

    @Override
    protected void addExtras() {
        System.out.println("🍋 Adding a slice of lemon...");
    }

    @Override
    protected String getName() {
        return "tea";
    }
}
```

```java
public class Coffee extends HotDrink {
    @Override
    protected void brew() {
        System.out.println("☕ Dripping water through the coffee...");
    }

    @Override
    protected void addExtras() {
        System.out.println("🥛 Adding milk and sugar...");
    }

    @Override
    protected String getName() {
        return "coffee";
    }
}
```

```java
public class Cafe {
    public static void main(String[] args) {
        HotDrink[] orders = { new Tea(), new Coffee() };
        for (HotDrink drink : orders) {
            drink.prepare();
        }
    }
}
```

**Output:**

```
💧 Boiling water...
🍵 Steeping the tea bag for 3 minutes...
🫗 Pouring into a cup...
🍋 Adding a slice of lemon...
✅ Your tea is ready!

💧 Boiling water...
☕ Dripping water through the coffee...
🫗 Pouring into a cup...
🥛 Adding milk and sugar...
✅ Your coffee is ready!
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `public final void prepare()` | The **template**: the order of steps. `final` → children **can't** change the order. 🔒 |
| `private void boilWater()` | Common steps. `private` → children can't even see or change them. |
| `protected abstract void brew();` | The **empty fields** in the form. Each child **must** fill them. `protected` → only the family uses them. |

👉 **Why is this great?**
- The **order** of steps is written **once** and can't be broken.
- A new drink (hot chocolate 🍫) only needs to fill in **3 small methods**.
- No repeated code.

> 🌱 **Spring Boot note:** Spring uses this pattern **a lot** internally. Classes with names like `AbstractXxx` (for example `OncePerRequestFilter` in Spring Security — Chapter 83) give you a template: you just fill in one method, and Spring handles the rest!

---

## 🤔 Part 5: When should a class be abstract?

Ask yourself:

> "Does it make sense to create a plain object of this class?"

| Class | Makes sense alone? | Abstract? |
|---|---|---|
| `Animal` | ❌ "an animal" — which one? | ✅ abstract |
| `Dog` | ✅ yes, a real dog | ❌ concrete |
| `Shape` | ❌ "a shape" — which one? | ✅ abstract |
| `Employee` | 🤔 maybe — a normal employee | depends on your program |
| `HotDrink` | ❌ "a hot drink" — which one? | ✅ abstract |
| `Account` | ❌ in a bank, every account is savings or checking | ✅ abstract |

👉 Make a class **abstract** when:
1. It's a **general idea**, and only its children are real things.
2. You want to **force** children to write certain methods.
3. You want to share **code and fields** between children (otherwise, an **interface** may be better — next chapter!).

---

## 💻 Mini project: Bank accounts 🏦

```java
public abstract class Account {
    private final String owner;
    protected double balance;

    public Account(String owner, double startBalance) {
        this.owner = owner;
        this.balance = startBalance;
    }

    public String getOwner()   { return owner; }
    public double getBalance() { return balance; }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }

    // Each account type has its own withdraw rules
    public abstract boolean withdraw(double amount);

    // Each account type has its own monthly update
    public abstract void monthEnd();

    public abstract String getType();

    @Override
    public String toString() {
        return String.format("%-9s %-6s %9.2f", getType(), owner, balance);
    }
}
```

```java
public class SavingsAccount extends Account {
    private static final double INTEREST_RATE = 0.02;   // 2% per month

    public SavingsAccount(String owner, double startBalance) {
        super(owner, startBalance);
    }

    @Override
    public boolean withdraw(double amount) {
        if (amount <= 0 || amount > balance) {
            return false;   // savings: never below 0
        }
        balance -= amount;
        return true;
    }

    @Override
    public void monthEnd() {
        balance += balance * INTEREST_RATE;   // earn interest 📈
    }

    @Override
    public String getType() {
        return "Savings";
    }
}
```

```java
public class CheckingAccount extends Account {
    private static final double OVERDRAFT_LIMIT = 500;
    private static final double MONTHLY_FEE = 5;

    public CheckingAccount(String owner, double startBalance) {
        super(owner, startBalance);
    }

    @Override
    public boolean withdraw(double amount) {
        if (amount <= 0 || balance - amount < -OVERDRAFT_LIMIT) {
            return false;   // checking: can go down to -500
        }
        balance -= amount;
        return true;
    }

    @Override
    public void monthEnd() {
        balance -= MONTHLY_FEE;   // pay a fee 💸
    }

    @Override
    public String getType() {
        return "Checking";
    }
}
```

```java
public class Bank {
    public static void main(String[] args) {
        Account[] accounts = {
            new SavingsAccount("Sara", 1000),
            new CheckingAccount("Tom", 200)
        };

        System.out.println("Sara withdraws 1500: " + accounts[0].withdraw(1500));
        System.out.println("Tom withdraws 600:   " + accounts[1].withdraw(600));

        for (Account acc : accounts) {
            acc.monthEnd();
        }

        System.out.println("\n=== After month end ===");
        for (Account acc : accounts) {
            System.out.println(acc);
        }
    }
}
```

**Output:**

```
Sara withdraws 1500: false
Tom withdraws 600:   true

=== After month end ===
Savings   Sara     1020.00
Checking  Tom      -405.00
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `abstract class Account` | There's no "plain" account. Every account is savings **or** checking. |
| `deposit()` is concrete | Depositing works the **same** for every account → write it once. |
| `withdraw()` is abstract | The **rules** are different → each child writes its own. |
| `acc.monthEnd()` in a loop | Polymorphism: savings earn interest, checking pays a fee. |

---

## ✋ Try it yourself

**Task 1:** Make an abstract class `Animal` with an abstract method `makeSound()` and a concrete method `sleep()`. Make `Dog`, `Cat` and `Duck` children. Try to write `new Animal()` — what error do you get?

**Task 2:** Add a `HotChocolate` class to the Template Method example. You only need to write 3 methods!

<details>
<summary>Click to see the answer</summary>

```java
public class HotChocolate extends HotDrink {
    @Override
    protected void brew() {
        System.out.println("🍫 Melting chocolate into hot milk...");
    }

    @Override
    protected void addExtras() {
        System.out.println("☁️ Adding marshmallows...");
    }

    @Override
    protected String getName() {
        return "hot chocolate";
    }
}
```

</details>

**Task 3:** Make an abstract class `Employee` with an abstract method `double calculatePay()`. Make:
- `SalariedEmployee` — fixed monthly salary
- `HourlyEmployee` — hours × hourly rate (with 1.5× pay for hours over 160)
- `Freelancer` — number of projects × price per project

Put them in one array and print the total pay.

**Task 4:** Make an abstract class `Game` with a template method `play()` that calls: `start()`, then `playTurn()` 3 times, then `end()`. Make `ChessGame` and `FootballGame`.

<details>
<summary>Click to see the answer</summary>

```java
public abstract class Game {
    public final void play() {
        start();
        for (int turn = 1; turn <= 3; turn++) {
            playTurn(turn);
        }
        end();
    }

    protected abstract void start();
    protected abstract void playTurn(int turn);
    protected abstract void end();
}

public class ChessGame extends Game {
    @Override protected void start() { System.out.println("♟️ Setting up the board"); }
    @Override protected void playTurn(int turn) { System.out.println("Move " + turn); }
    @Override protected void end() { System.out.println("Checkmate! 👑"); }
}
```

</details>

**Task 5:** True or false?
1. An abstract class can have a constructor.
2. An abstract class must have at least one abstract method.
3. An abstract method can have a body.
4. You can write `Shape s = new Circle(1);` if `Shape` is abstract.

<details>
<summary>Click to see the answers</summary>

1. ✅ True — children call it with `super(...)`.
2. ❌ False — it's allowed to have zero abstract methods (just to stop people from using `new`).
3. ❌ False — abstract methods have no body.
4. ✅ True — you can use an abstract class as a type.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Giving an abstract method a body

```java
public abstract double area() { return 0; }   // ❌ error: abstract methods cannot have a body
public abstract double area();                // ✅
```

### Mistake 2: Abstract method in a normal class

```java
public class Shape {
    public abstract double area();   // ❌ error: Shape is not abstract and does not override abstract method area()
}
```

**Fix:** Add `abstract` to the class.

### Mistake 3: Forgetting to override an abstract method

```
❌ error: Circle is not abstract and does not override abstract method perimeter() in Shape
```

**Fix:** Write all the missing methods. IntelliJ helps: put the cursor on the red class name → **Alt + Enter** → **Implement methods**. 🪄

### Mistake 4: Trying to use `new` on an abstract class

```java
new Shape("x");   // ❌ error: Shape is abstract; cannot be instantiated
```

**Fix:** Create a **child** object: `new Circle(1)`.

### Mistake 5: `private abstract`

```java
private abstract void brew();   // ❌ error: illegal combination of modifiers: abstract and private
```

A child can't see a `private` method, so it can never fill it in. Use `protected` or `public`.

### Mistake 6: `final abstract`

```java
public final abstract class Shape { }   // ❌ illegal combination
```

`abstract` = "needs children". `final` = "no children allowed". They contradict each other! 🤯

---

## ✅ Summary

- An **abstract class** is an **incomplete** class — a general idea. Write `abstract class`.
- You **can't** create objects of it with `new`. But you **can** use it as a **type** (polymorphism).
- An **abstract method** has **no body** (`;` instead of `{ }`). Every concrete child **must** override it — Java checks this for you. 🥅
- Abstract classes **can** have fields, constructors and normal methods.
- A class with **any** abstract method must be abstract.
- **Template Method pattern**: a `final` method in the parent defines the **steps**; children fill in some steps (abstract methods).
- Use an abstract class for a **general idea** that **shares code** with its children, and **forces** them to write certain methods.
- IntelliJ: **Alt + Enter → Implement methods**.

---

## ❓ Quiz

1. Can you write `new Animal()` if `Animal` is abstract?
2. What is an abstract method?
3. What happens if a child class doesn't override an abstract method?
4. Can an abstract class have a constructor? Why would it need one?
5. Can an abstract class have normal methods with bodies?
6. What is the Template Method pattern?
7. Why is the template method often `final`?
8. Why can't a method be both `abstract` and `private`?

<details>
<summary>Click to see the answers</summary>

1. No.
2. A method with no body. It only says "this method must exist"; children must write the body.
3. A compile error — unless the child is also abstract.
4. Yes. Children call it with `super(...)` to set up the fields that the abstract class has.
5. Yes.
6. A parent method that defines the **order of steps**, where some steps are abstract and filled in by the children.
7. So children can't change the **order** of the steps.
8. Because children can't see `private` methods, so they could never override (fill in) it.

</details>

---

[⬅ Previous chapter](23-polymorphism.md) | [Table of Contents](../README.md) | [Next chapter: Interfaces ➡](25-interfaces.md)
