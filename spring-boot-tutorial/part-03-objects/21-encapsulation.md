# Chapter 21 – Hiding Data: `private`, Getters and Setters

[⬅ Previous chapter](20-fields-methods-this.md) | [Table of Contents](../README.md) | [Next chapter ➡](22-inheritance.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What **encapsulation** is, and why it **protects** your objects
- The keywords **`private`** and **`public`**
- How to write **getters** and **setters**
- How to put **rules** (validation) inside setters
- When **not** to write a setter
- How to make an **immutable** class (an object that never changes)
- How IntelliJ generates getters and setters for you

> 🌱 **Spring Boot note:** In Spring Boot, almost every data class has `private` fields with getters and setters. Spring and its tools (like JSON conversion) **use** your getters and setters to read and write data. This chapter is essential! 🔑

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Encapsulation** | **Hiding** an object's data inside it, and only allowing access through **safe methods**. Like a capsule 💊. |
| **Access modifier** | A word that says **who** can see something: `public`, `private`, `protected`. |
| **`private`** | Only the class **itself** can see it. |
| **`public`** | **Everyone** can see it. |
| **Getter** | A method that **gives back** (gets) a field's value: `getName()`. |
| **Setter** | A method that **changes** (sets) a field's value: `setName(...)`. |
| **Validation** | **Checking** that a value is OK before accepting it. |
| **Immutable** | **Cannot be changed** after it is created. |
| **Read-only** | Can be read, but not changed from outside. |

---

## 📖 Story: The bank and the vault 🏦

Imagine a bank where the money is just lying on a table in the middle of the room. 💵💵💵
Anyone can walk in and take some, or add fake money. Nobody checks anything! 😱

A **real** bank:
- keeps the money in a **locked vault** 🔒 (nobody touches it directly),
- has a **counter** with a **cashier** 👩‍💼. You must ask the cashier:
  - "I want to **deposit** 100." → the cashier **checks** the money is real, then puts it in.
  - "I want to **withdraw** 50." → the cashier **checks** you have enough, then gives it.
  - "What's my **balance**?" → the cashier **tells** you.

This is **encapsulation**:
- The vault = **`private`** fields 🔒
- The cashier = **public methods** (getters, setters, deposit, withdraw...) that **check** everything

---

## 😱 Part 1: The problem — public fields

Look at this `BankAccount` from Chapter 18. All fields are open:

```java
public class BankAccount {
    String owner;
    double balance;
}
```

Anyone can do **anything**:

```java
BankAccount acc = new BankAccount();
acc.owner = "Sara";
acc.balance = 100;

acc.balance = -999999;      // 😱 negative money!
acc.balance = 1_000_000;    // 😱 free money!
acc.owner = "";             // 😱 no owner!
```

Java allows it. The object **can't protect itself**. In a real program, this means **bugs** that are very hard to find: "Who set the balance to −999999?!" 🕵️

---

## 🔒 Part 2: `private` — lock the fields

```java
public class BankAccount {
    private String owner;
    private double balance;
}
```

Now:

```java
BankAccount acc = new BankAccount();
acc.balance = -999999;   // ❌ error: balance has private access in BankAccount
```

🔒 **Locked!** Only code **inside** the `BankAccount` class can touch `balance`.

### Access modifiers (simple version)

| Modifier | Who can see it? | Picture |
|---|---|---|
| `private` | only **this class** | 🔒 your diary |
| (nothing) | classes in the **same package** (folder) | 🏠 your family |
| `protected` | same package + **child classes** (Chapter 22) | 👨‍👧 family + children |
| `public` | **everyone** | 📢 a public poster |

(Chapter 26 explains packages and the full table.)

👉 **Golden rule:** Make **fields `private`**. Make **methods `public`** (when other classes need them).

But wait — now **nobody** can read or change the fields. That's too locked! We need a **cashier**... 👩‍💼

---

## 📤 Part 3: Getters — let others **read**

A **getter** is a public method that returns the value of a private field:

```java
public class BankAccount {
    private String owner;
    private double balance;

    public BankAccount(String owner) {
        this.owner = owner;
        this.balance = 0;
    }

    public String getOwner() {
        return owner;
    }

    public double getBalance() {
        return balance;
    }
}
```

```java
BankAccount acc = new BankAccount("Sara");
System.out.println(acc.getOwner());     // Sara
System.out.println(acc.getBalance());   // 0.0
acc.balance = 500;                       // ❌ still locked!
```

### 🔍 Line by line

`public double getBalance() {`

| Part | Meaning |
|---|---|
| `public` | Everyone can call this method. |
| `double` | It returns the type of the field. |
| `getBalance` | Name: **`get`** + the field name with a **capital** first letter. |
| `()` | No parameters. |
| `return balance;` | Give back the value. |

### 📏 Naming rules for getters

| Field | Getter |
|---|---|
| `String name` | `getName()` |
| `int age` | `getAge()` |
| `double balance` | `getBalance()` |
| `boolean active` | **`isActive()`** ⚠️ (for `boolean`, use `is` instead of `get`) |

> ⚠️ These names are **very important**! Spring Boot and many Java tools **look for** methods called `getXxx()` and `isXxx()` to find the data in your objects. If you name it `fetchName()` or `name_get()`, they won't find it. 🔍

---

## 📥 Part 4: Setters — let others **change** (with rules!)

A **setter** is a public method that changes a private field — but it can **check** the value first:

```java
public class Person {
    private String name;
    private int age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        if (name == null || name.isBlank()) {
            System.out.println("❌ Name cannot be empty.");
            return;
        }
        this.name = name.strip();
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        if (age < 0 || age > 150) {
            System.out.println("❌ " + age + " is not a valid age.");
            return;
        }
        this.age = age;
    }
}
```

```java
Person p = new Person();
p.setName("  Sara  ");
p.setAge(30);
System.out.println(p.getName() + ", " + p.getAge());   // Sara, 30

p.setAge(-5);         // ❌ -5 is not a valid age.
p.setName("");        // ❌ Name cannot be empty.
System.out.println(p.getName() + ", " + p.getAge());   // Sara, 30  ← still good!
```

### 🔍 Line by line

`public void setAge(int age) {`

| Part | Meaning |
|---|---|
| `public` | Everyone can call it. |
| `void` | A setter returns nothing. |
| `setAge` | Name: **`set`** + the field name with a capital letter. |
| `(int age)` | The new value. |
| `if (age < 0 \|\| age > 150) { ... return; }` | 🛡️ **The guard.** Bad value? Refuse and leave. |
| `this.age = age;` | Good value → save it. |

👉 The object now **protects itself**. It's **impossible** to give it a bad age. If there's ever a bug with ages, you only need to look in **one** place: `setAge`. 🎯

> 💡 Here we print a message and ignore the bad value. In real programs, we usually **throw an exception** (Chapter 33) so the caller **knows** something went wrong:
> ```java
> if (age < 0) {
>     throw new IllegalArgumentException("Age cannot be negative");
> }
> ```

---

## 🧠 Part 5: Not every field needs a setter!

Think about the bank account. Should there be a `setBalance()`?

```java
public void setBalance(double balance) {   // 🤔 ???
    this.balance = balance;
}
```

**No!** In a real bank, you can't just "set" your balance to a million. 😄 The balance only changes through **deposit** and **withdraw** — with rules.

```java
public class BankAccount {
    private final String owner;
    private double balance;

    public BankAccount(String owner) {
        this.owner = owner;
    }

    public String getOwner() {
        return owner;
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        if (amount <= 0) {
            System.out.println("❌ Deposit must be positive.");
            return;
        }
        balance += amount;
    }

    public boolean withdraw(double amount) {
        if (amount <= 0 || amount > balance) {
            System.out.println("❌ Cannot withdraw " + amount);
            return false;
        }
        balance -= amount;
        return true;
    }
}
```

### 🔍 Design decisions

| Field | Getter? | Setter? | Why |
|---|---|---|---|
| `owner` | ✅ | ❌ | The owner never changes. It's `final` — set once in the constructor. |
| `balance` | ✅ | ❌ | Only changes through `deposit` / `withdraw`, which have **business rules**. |

👉 **Don't** automatically write a getter and setter for **every** field. Ask: "Should someone outside be allowed to **read** this? To **change** it? With which **rules**?"

### `private final` — set once, never change

```java
private final String owner;
```

| Part | Meaning |
|---|---|
| `private` | only this class can see it |
| `final` | can be set **only once** (in the constructor), then never changed — not even by the class itself |

This is a very common combination! 🔒🔒

---

## 🧊 Part 6: Immutable objects — objects that never change

Sometimes the best object is one that **can't change at all** after it's created. Like a **birth certificate** 📜 — once printed, it never changes.

```java
public final class Money {
    private final double amount;
    private final String currency;

    public Money(double amount, String currency) {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        this.amount = amount;
        this.currency = currency;
    }

    public double getAmount() {
        return amount;
    }

    public String getCurrency() {
        return currency;
    }

    public Money add(Money other) {
        return new Money(this.amount + other.amount, this.currency);
    }

    @Override
    public String toString() {
        return amount + " " + currency;
    }
}
```

```java
Money a = new Money(10, "USD");
Money b = new Money(5, "USD");
Money sum = a.add(b);

System.out.println(a);     // 10.0 USD  ← not changed!
System.out.println(sum);   // 15.0 USD  ← a NEW object
```

### 🔍 Rules for an immutable class

| Rule | In the code |
|---|---|
| All fields `private final` | `private final double amount;` |
| **No setters** | — |
| Methods that "change" return a **new** object | `add` returns `new Money(...)` |
| The class is `final` (no children can change it — Chapter 22) | `public final class Money` |

### 🤔 Why immutable?

- **Safe:** Nobody can change it by accident. Pass it anywhere — it stays the same. 🛡️
- **Simple:** It's always in the state it was created in.
- You already know one: **`String`** is immutable! (Chapter 9: `toUpperCase()` returns a **new** String.)

👉 In Chapter 29, **records** make immutable classes in **one line**!

---

## 🪄 Part 7: Let IntelliJ write it for you

Writing getters and setters by hand is boring. IntelliJ does it in seconds:

1. Write the class with its `private` fields:
   ```java
   public class Product {
       private String name;
       private double price;
       private int stock;
   }
   ```
2. Click inside the class.
3. Press **Alt + Insert** (Mac: **Cmd + N**).
4. Choose **Getter and Setter**.
5. Select the fields (Ctrl + A for all) → **OK**.

✨ IntelliJ writes:

```java
public String getName() {
    return name;
}

public void setName(String name) {
    this.name = name;
}

public double getPrice() {
    return price;
}

public void setPrice(double price) {
    this.price = price;
}

public int getStock() {
    return stock;
}

public void setStock(int stock) {
    this.stock = stock;
}
```

Then **add your rules** to the setters where needed.

> 🌱 **Spring Boot preview:** Many Spring projects use a tool called **Lombok**. You write `@Getter @Setter` above the class, and the getters and setters are created **invisibly**. You'll see it in real projects. But first, it's important to understand what it does — which you now do! 😊

---

## 🔁 Part 8: Inside the class — use fields or getters?

Inside its own class, an object **can** use its private fields directly:

```java
public class Rectangle {
    private double width;
    private double height;

    public double area() {
        return width * height;   // ✅ direct access is fine inside the class
    }
}
```

`private` means "private to the **class**". All methods in the class can use it.

And even **another object of the same class**:

```java
public boolean isBiggerThan(Rectangle other) {
    return this.area() > other.area();
    // also allowed: other.width, other.height (same class!)
}
```

---

## 💻 Mini project: A game character 🧙

```java
public class Hero {
    private static final int MAX_HEALTH = 100;

    private final String name;
    private int health;
    private int level;
    private int experience;

    public Hero(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("A hero needs a name!");
        }
        this.name = name;
        this.health = MAX_HEALTH;
        this.level = 1;
        this.experience = 0;
    }

    // ----- Getters (read-only from outside) -----
    public String getName()     { return name; }
    public int getHealth()      { return health; }
    public int getLevel()       { return level; }
    public int getExperience()  { return experience; }
    public boolean isAlive()    { return health > 0; }

    // ----- Actions with rules -----
    public void takeDamage(int damage) {
        if (damage < 0 || !isAlive()) {
            return;
        }
        health = Math.max(0, health - damage);
        System.out.println("💥 " + name + " takes " + damage + " damage. Health: " + health);
        if (!isAlive()) {
            System.out.println("☠️ " + name + " has fallen!");
        }
    }

    public void heal(int amount) {
        if (amount < 0 || !isAlive()) {
            return;
        }
        health = Math.min(MAX_HEALTH, health + amount);
        System.out.println("💚 " + name + " heals. Health: " + health);
    }

    public void gainExperience(int xp) {
        if (xp <= 0 || !isAlive()) {
            return;
        }
        experience += xp;
        while (experience >= level * 100) {
            experience -= level * 100;
            level++;
            System.out.println("⭐ " + name + " reached level " + level + "!");
        }
    }

    @Override
    public String toString() {
        return name + " [Lv " + level + ", HP " + health + "/" + MAX_HEALTH + ", XP " + experience + "]";
    }

    public static void main(String[] args) {
        Hero hero = new Hero("Aria");
        System.out.println(hero);

        hero.takeDamage(30);
        hero.heal(50);
        hero.gainExperience(250);
        hero.takeDamage(120);
        hero.heal(10);

        System.out.println(hero);
    }
}
```

**Output:**

```
Aria [Lv 1, HP 100/100, XP 0]
💥 Aria takes 30 damage. Health: 70
💚 Aria heals. Health: 100
⭐ Aria reached level 2!
💥 Aria takes 120 damage. Health: 0
☠️ Aria has fallen!
Aria [Lv 2, HP 0/100, XP 150]
```

### 🔍 How encapsulation protects the hero

| Rule | How it's enforced |
|---|---|
| Health is never above 100 | `Math.min(MAX_HEALTH, ...)` in `heal` |
| Health is never below 0 | `Math.max(0, ...)` in `takeDamage` |
| Dead heroes can't heal or level up | `!isAlive()` checks |
| The name never changes | `private final`, no setter |
| Level only goes up through experience | no `setLevel()` |

Try writing `hero.health = 9999;` in `main` — wait, it **works** here! 😮 Why? Because `main` is **inside** the `Hero` class. Move `main` to another class, and it becomes an error. 🔒

---

## ✋ Try it yourself

**Task 1:** Make a class `Product` with private fields `name`, `price`, `stock`. Write getters for all. Write setters with rules:
- `price` can't be negative
- `stock` can't be negative

**Task 2:** Instead of a setter for `stock`, write two methods: `addStock(int amount)` and `boolean sell(int amount)` (returns `false` if not enough stock).

<details>
<summary>Click to see one possible answer</summary>

```java
public class Product {
    private final String name;
    private double price;
    private int stock;

    public Product(String name, double price) {
        this.name = name;
        setPrice(price);
    }

    public String getName()  { return name; }
    public double getPrice() { return price; }
    public int getStock()    { return stock; }

    public void setPrice(double price) {
        if (price < 0) {
            System.out.println("❌ Price cannot be negative.");
            return;
        }
        this.price = price;
    }

    public void addStock(int amount) {
        if (amount > 0) {
            stock += amount;
        }
    }

    public boolean sell(int amount) {
        if (amount <= 0 || amount > stock) {
            return false;
        }
        stock -= amount;
        return true;
    }
}
```

Notice: the constructor calls `setPrice(price)` so the **same rule** is used. DRY! ✅

</details>

**Task 3:** Make an **immutable** class `Point` (`x`, `y`) with a method `Point move(int dx, int dy)` that returns a **new** point.

**Task 4:** Make a class `Password` that stores a password privately. It should have:
- **no** getter (nobody should read the password!)
- `boolean check(String attempt)` — returns true if it matches
- `void change(String oldPw, String newPw)` — only changes if `oldPw` is correct **and** `newPw` has at least 8 characters

**Task 5:** Which fields of a `Student` class (`id`, `name`, `email`, `averageGrade`) should have a setter? Explain why.

<details>
<summary>Click to see a possible answer</summary>

- `id`: ❌ no setter — an ID should never change (`final`).
- `name`: ✅ setter — names can change (marriage, typo fix), with a "not empty" rule.
- `email`: ✅ setter — with a rule like "must contain @".
- `averageGrade`: ❌ no setter — it should be **calculated** from the grades, not set by hand.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Accessing a private field from outside

```java
acc.balance = 100;   // ❌ error: balance has private access in BankAccount
```

**Fix:** Use a public method: `acc.deposit(100);`

### Mistake 2: Wrong getter name

```java
public boolean getActive() { ... }   // ⚠️ works, but for boolean use isActive()
public String name() { ... }         // ⚠️ tools like Spring won't see this as a getter
```

### Mistake 3: Setter that doesn't set

```java
public void setName(String name) {
    name = name;   // ❌ forgot "this." — the field never changes!
}
```

### Mistake 4: Getter that returns a private array (leak!)

```java
private int[] scores;

public int[] getScores() {
    return scores;   // ⚠️ the caller gets the REFERENCE and can change your array!
}
```

```java
student.getScores()[0] = 100;   // 😱 changed the private array from outside!
```

**Fix:** Return a **copy**:

```java
public int[] getScores() {
    return Arrays.copyOf(scores, scores.length);
}
```

### Mistake 5: Making everything public "because it's easier"

It's easier **today**, but in 3 months, when there's a bug, you won't know **who** changed the field. 🕵️ Keep fields **private**.

### Mistake 6: Setters for everything, without rules

If every field has a setter with no checks, it's almost the same as `public` fields. Think about **which** fields should change, and with **which rules**.

---

## ✅ Summary

- **Encapsulation** = hide data (`private` fields) + offer safe **public methods**. 💊
- `private` → only the class itself. `public` → everyone.
- **Getter**: `public Type getField() { return field; }` — for `boolean`: `isField()`.
- **Setter**: `public void setField(Type field) { /* check */ this.field = field; }`
- Put **rules** (validation) in setters and constructors. The object **protects itself**.
- **Not** every field needs a setter. Use **action methods** (`deposit`, `withdraw`) with business rules.
- `private final` → set once in the constructor, never changed.
- **Immutable** class: `final` class, `private final` fields, no setters, "changes" return **new** objects.
- Getter/setter names matter: **Spring Boot** and other tools look for `getX`, `setX`, `isX`.
- IntelliJ: **Alt + Insert → Getter and Setter**.

---

## ❓ Quiz

1. What does encapsulation mean?
2. Who can access a `private` field?
3. What are the getter and setter names for a field `email`? And for a `boolean` field `verified`?
4. Why is it useful to have a setter instead of a public field?
5. Should a bank account have `setBalance()`? Why or why not?
6. What does `private final` mean?
7. Name 3 rules for an immutable class.
8. Why is returning a private array from a getter dangerous?

<details>
<summary>Click to see the answers</summary>

1. Hiding the data inside the object (`private`) and only allowing access through safe public methods.
2. Only code inside the same class.
3. `getEmail()` / `setEmail(String email)`. For `verified`: `isVerified()` / `setVerified(boolean verified)`.
4. The setter can **check** the value (validation), so the object never gets a bad value.
5. No. The balance should only change through `deposit` and `withdraw`, which follow the bank's rules.
6. Only this class can see it, and it can be set only once (in the constructor).
7. Fields are `private final`; no setters; methods that "change" something return a new object (and the class is `final`).
8. The caller gets a reference to the **same** array and can change the private data from outside.

</details>

---

[⬅ Previous chapter](20-fields-methods-this.md) | [Table of Contents](../README.md) | [Next chapter: Inheritance ➡](22-inheritance.md)
