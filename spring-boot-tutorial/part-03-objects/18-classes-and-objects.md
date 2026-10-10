# Chapter 18 – Classes and Objects: The Cookie Cutter and the Cookies

[⬅ Previous chapter](../part-02-java-basics/17-comments-clean-code.md) | [Table of Contents](../README.md) | [Next chapter ➡](19-constructors.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What **Object-Oriented Programming (OOP)** is
- What a **class** is and what an **object** is
- How to write your **own class** with **fields** (data) and **methods** (actions)
- How to **create** objects with `new`
- How to use the **dot** `.` to read fields and call methods
- What a **reference** is, and what **`null`** means
- How to keep many objects in an **array**

> 🌱 **Why this matters for Spring Boot:** In Spring Boot, **everything** is a class: a `Student`, a `StudentController`, a `StudentService`, a `StudentRepository`... If you understand classes and objects, Spring Boot will make sense. This is the **most important part** of the book. Take your time! 🐢

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **OOP** | *Object-Oriented Programming.* A way to write programs using **objects** that look like things in the real world. |
| **Class** | A **plan** or **template** for making objects. Like a cookie cutter. 🍪 |
| **Object** | A real **thing** made from a class. Like a cookie. |
| **Instance** | Another word for **object**. "An instance of the class Dog" = "a Dog object". |
| **Field** | A **variable inside a class**. It keeps the object's data. (Also called *attribute* or *property*.) |
| **Method** | A function inside a class. It's what the object can **do**. |
| **`new`** | The keyword that **creates** a new object. |
| **Reference** | The "address" of an object. A variable of a class type keeps a reference, not the object itself. |
| **`null`** | "No object." The variable points to **nothing**. |
| **State** | The current values of an object's fields. |

---

## 📖 Story: The cookie cutter 🍪

You want to make cookies. You have a **cookie cutter** in the shape of a star ⭐.

- The **cookie cutter** is not a cookie. You can't eat it. 😅 It's a **plan** that says what shape every cookie will have.
- With **one** cutter, you can make **many** cookies.
- Every cookie has the **same shape**, but each cookie can be **different**: one has chocolate 🍫, one has sugar, one is a little bigger.

```
       CLASS (the plan)                       OBJECTS (the real things)
  ┌──────────────────────┐
  │   Cookie cutter ⭐    │  ──── new ───►   🍪 Cookie 1: chocolate, big
  │                      │  ──── new ───►   🍪 Cookie 2: sugar, small
  │  - topping           │  ──── new ───►   🍪 Cookie 3: nuts, medium
  │  - size              │
  └──────────────────────┘
```

In Java:
- The **class** is the cookie cutter (the plan).
- An **object** is a cookie (a real thing made from the plan).
- `new` is the action of **pressing the cutter** into the dough.

### Another story: the house plan 🏠

An architect draws **one** house plan. Builders use it to build **many** houses on a street. All houses have the same rooms, but each house has its own **color**, its own **owner**, its own **address**.

| Real world | Java |
|---|---|
| House plan 📐 | Class `House` |
| A real house 🏠 | An object: `new House()` |
| Color, owner, number of rooms | Fields |
| Open the door, turn on lights | Methods |

---

## 🧠 Part 1: What is OOP?

Until now, we had **data** (variables) and **actions** (methods) separate, everywhere:

```java
String dogName = "Rex";
int dogAge = 3;
String dog2Name = "Bella";
int dog2Age = 5;

public static void bark(String name) { ... }
```

With 100 dogs, this becomes a mess! 😵

**OOP idea:** Put the data **and** the actions that belong together into **one** thing — an **object**.

```
   ┌──────────────── Dog object ────────────────┐
   │  DATA (fields):     name = "Rex"            │
   │                     age = 3                 │
   │                                             │
   │  ACTIONS (methods): bark()                  │
   │                     eat()                   │
   └─────────────────────────────────────────────┘
```

Every object **knows** things (fields) and **can do** things (methods). Just like real things:

| Real thing | Knows (fields) | Can do (methods) |
|---|---|---|
| 🐕 Dog | name, age, breed | bark, eat, sleep |
| 🚗 Car | color, speed, fuel | drive, brake, honk |
| 🏦 Bank account | owner, balance | deposit, withdraw |
| 👩‍🎓 Student | name, grade, scores | study, getAverage |

---

## ✍️ Part 2: Your first class

Let's make a `Dog` class. In IntelliJ, right-click `src` → **New → Java Class** → name it `Dog`.

**File: `Dog.java`**

```java
public class Dog {
    String name;
    int age;

    void bark() {
        System.out.println(name + " says: Woof! 🐕");
    }
}
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `public class Dog {` | Start a class named `Dog`. This is the **plan** for dogs. |
| `String name;` | A **field**. Every dog will have its **own** `name`. |
| `int age;` | Another field. Every dog has its own `age`. |
| `void bark() {` | A **method**. Every dog can bark. ⚠️ Notice: **no `static`** here! (See below.) |
| `System.out.println(name + ...)` | The method can use the fields directly. `name` means "**this** dog's name". |
| `}` | End of the method. |
| `}` | End of the class. |

> ⚠️ **This class has no `main` method!** It's just a **plan**. It doesn't do anything by itself. We need **another** class with `main` to create and use dogs.

### 🤔 Why no `static` now?

In Part 2, all methods were `static`. A `static` method belongs to the **class** (the plan), not to any object.

But `bark()` must know **which** dog is barking — Rex or Bella? So it must belong to **each object**. That's why there's **no** `static`.

| | `static` method | method without `static` (instance method) |
|---|---|---|
| Belongs to | the **class** (the plan) | each **object** |
| Can use the object's fields? | ❌ No (which object?) | ✅ Yes |
| Called like | `Dog.someMethod()` | `rex.bark()` |

We explain `static` fully in Chapter 27.

---

## 🏭 Part 3: Creating objects with `new`

Now make a second file with `main`:

**File: `Main.java`**

```java
public class Main {
    public static void main(String[] args) {
        Dog rex = new Dog();
        rex.name = "Rex";
        rex.age = 3;

        Dog bella = new Dog();
        bella.name = "Bella";
        bella.age = 5;

        rex.bark();
        bella.bark();

        System.out.println(rex.name + " is " + rex.age + " years old.");
        System.out.println(bella.name + " is " + bella.age + " years old.");
    }
}
```

**Output:**

```
Rex says: Woof! 🐕
Bella says: Woof! 🐕
Rex is 3 years old.
Bella is 5 years old.
```

### 🔍 Line by line

**`Dog rex = new Dog();`**

| Part | Meaning |
|---|---|
| `Dog` | The **type** of the variable. Our own class is now a type, just like `int` or `String`! |
| `rex` | The **name** of the variable. |
| `=` | Put into. |
| `new` | "**Create** a new object." 🏭 |
| `Dog()` | "...from the `Dog` plan." (The `()` call a **constructor** — Chapter 19.) |

**`rex.name = "Rex";`**

| Part | Meaning |
|---|---|
| `rex` | The object. |
| `.` | "Go **inside** this object." |
| `name` | The field `name` of **this** object. |
| `= "Rex"` | Put `"Rex"` into it. |

**`rex.bark();`**

"Rex, please bark!" — calls the `bark` method **on the object `rex`**. Inside `bark`, `name` means **rex's** name.

### 🗺️ The picture in memory

```
  Variables                       Objects (in memory)
                              ┌─────────────────────┐
  rex   ───────────────────►  │ Dog                 │
                              │   name = "Rex"      │
                              │   age  = 3          │
                              └─────────────────────┘
                              ┌─────────────────────┐
  bella ───────────────────►  │ Dog                 │
                              │   name = "Bella"    │
                              │   age  = 5          │
                              └─────────────────────┘
```

👉 **Two** objects, made from **one** class. Each object has its **own** fields. Changing `rex.age` does **not** change `bella.age`.

### 📂 Where are the files?

In IntelliJ, your `src` folder now looks like this:

```
src
 ├── Dog.java     ← the plan
 └── Main.java    ← the program that uses the plan
```

Run `Main` (it has the `main` method). Java finds `Dog` automatically because it's in the same folder.

> 💡 **Rule:** One `public class` per file, and the file name = the class name. Most classes live in their own file.

---

## 🎨 Part 4: Default values of fields

What if you don't set a field?

```java
Dog mystery = new Dog();
System.out.println(mystery.name);   // null
System.out.println(mystery.age);    // 0
```

Fields get **default values** automatically (the same as array elements — Chapter 14):

| Field type | Default value |
|---|---|
| `int`, `long`, `double`... | `0` / `0.0` |
| `boolean` | `false` |
| `char` | empty character |
| `String` and other objects | `null` |

> ⚠️ This is different from **local variables** inside a method. Local variables have **no** default value — you must set them before using them (Chapter 6). Fields get defaults.

---

## 🛠️ Part 5: Methods that use and change fields

Let's make a more useful class: a **bank account**. 🏦

**File: `BankAccount.java`**

```java
public class BankAccount {
    String owner;
    double balance;

    void deposit(double amount) {
        balance = balance + amount;
        System.out.println(owner + " deposited " + amount + ". New balance: " + balance);
    }

    void withdraw(double amount) {
        if (amount > balance) {
            System.out.println("❌ Not enough money! " + owner + " has only " + balance);
        } else {
            balance = balance - amount;
            System.out.println(owner + " withdrew " + amount + ". New balance: " + balance);
        }
    }

    double getBalance() {
        return balance;
    }

    void printInfo() {
        System.out.println("Account of " + owner + ": " + balance + " dollars");
    }
}
```

**File: `Main.java`**

```java
public class Main {
    public static void main(String[] args) {
        BankAccount sara = new BankAccount();
        sara.owner = "Sara";

        BankAccount tom = new BankAccount();
        tom.owner = "Tom";

        sara.deposit(100);
        tom.deposit(50);
        sara.withdraw(30);
        tom.withdraw(80);

        sara.printInfo();
        tom.printInfo();

        double total = sara.getBalance() + tom.getBalance();
        System.out.println("Total money in the bank: " + total);
    }
}
```

**Output:**

```
Sara deposited 100.0. New balance: 100.0
Tom deposited 50.0. New balance: 50.0
Sara withdrew 30.0. New balance: 70.0
❌ Not enough money! Tom has only 50.0
Account of Sara: 70.0 dollars
Account of Tom: 50.0 dollars
Total money in the bank: 120.0
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `void deposit(double amount)` | A method with a **parameter**. It **changes** the object's field `balance`. |
| `balance = balance + amount;` | `balance` is **this object's** balance. When we call `sara.deposit(100)`, it changes **Sara's** balance only. |
| `if (amount > balance)` | The object **protects** itself: you can't take more money than there is. |
| `double getBalance()` | A method that **returns** a field's value. |
| `sara.getBalance() + tom.getBalance()` | Ask each object for its balance. |

👉 See how **natural** it reads? `sara.deposit(100)`, `tom.withdraw(80)`. The code looks like the real world! That's the power of OOP. 💪

### 🎬 What happens in `sara.deposit(100)`?

```
 sara.deposit(100)
   │
   ├─ Java finds the object that "sara" points to
   ├─ Java runs deposit() with amount = 100
   │     inside: "balance" means sara's balance (0.0)
   │     balance = 0.0 + 100 = 100.0
   └─ back to main
```

---

## 🔗 Part 6: References — the remote control 📺

This is **very** important. Remember Chapter 14 (arrays are shared)? Objects work the same way.

A variable like `rex` does **not** contain the dog. It contains a **reference** — like a **remote control** that points to the TV.

```java
Dog a = new Dog();
a.name = "Rex";

Dog b = a;          // copy the REMOTE, not the dog!
b.name = "Max";

System.out.println(a.name);   // Max 😮
```

```
   a ───────┐
            ├──────►  ┌──────────────┐
   b ───────┘         │ Dog          │
                      │ name = "Max" │   ← ONE dog, two remotes
                      └──────────────┘
```

📺 **Story:** You and your brother each have a **remote control** for the **same** TV. If your brother changes the channel, **you** see the new channel too. There's only **one** TV!

### `==` with objects

```java
Dog d1 = new Dog();
d1.name = "Rex";
Dog d2 = new Dog();
d2.name = "Rex";
Dog d3 = d1;

System.out.println(d1 == d2);   // false — two different dogs (that happen to have the same name)
System.out.println(d1 == d3);   // true  — the same dog (two remotes)
```

`==` asks: "Do these two remotes point to the **same** object?" — not "Are the objects similar?". (That's why Strings need `.equals()` — Strings are objects! We'll write our own `equals` in Chapter 20.)

### Objects in methods

Because methods get a copy of the **remote**, a method **can change** the object:

```java
public static void birthday(Dog dog) {
    dog.age++;
}

// in main:
Dog rex = new Dog();
rex.age = 3;
birthday(rex);
System.out.println(rex.age);   // 4 ✅ changed!
```

| Type | Method gets a copy of... | Can the method change the original? |
|---|---|---|
| `int`, `double`, `boolean`, `char` | the **value** | ❌ No |
| Objects (and arrays) | the **reference** (remote) | ✅ Yes, the object's fields |

---

## 🕳️ Part 7: `null` — no object

A variable of a class type can point to **nothing**. This is called **`null`**.

```java
Dog dog = null;   // a remote control with no TV 📺❌
```

If you try to use it:

```java
dog.bark();   // 💥 NullPointerException
```

```
Exception in thread "main" java.lang.NullPointerException:
  Cannot invoke "Dog.bark()" because "dog" is null
```

📺 **Story:** You press buttons on a remote control, but there's **no TV** connected. Nothing can happen. Java crashes with a **NullPointerException** (often called **NPE**).

👉 The **NullPointerException** is the most famous error in Java. Every Java programmer has seen it thousands of times. 😅

### How to avoid it

**Check before using:**

```java
if (dog != null) {
    dog.bark();
} else {
    System.out.println("There is no dog.");
}
```

**Make sure fields get a value** — the next chapter (Constructors) helps a lot with this!

> 💡 Modern Java gives **helpful** NPE messages: `because "dog" is null`. Read them — they tell you exactly which variable was `null`.

---

## 📚 Part 8: Many objects in an array

You can make arrays of **your own** classes:

```java
public class Main {
    public static void main(String[] args) {
        Dog[] dogs = new Dog[3];

        dogs[0] = new Dog();
        dogs[0].name = "Rex";
        dogs[0].age = 3;

        dogs[1] = new Dog();
        dogs[1].name = "Bella";
        dogs[1].age = 5;

        dogs[2] = new Dog();
        dogs[2].name = "Max";
        dogs[2].age = 1;

        for (Dog dog : dogs) {
            dog.bark();
        }

        int totalAge = 0;
        for (Dog dog : dogs) {
            totalAge += dog.age;
        }
        System.out.println("Total age: " + totalAge);
    }
}
```

**Output:**

```
Rex says: Woof! 🐕
Bella says: Woof! 🐕
Max says: Woof! 🐕
Total age: 9
```

### 🔍 Key ideas

| Code | Meaning |
|---|---|
| `Dog[] dogs = new Dog[3];` | An array with **3 places** for Dog references. ⚠️ Right now, **all 3 are `null`**! The array has **places** for dogs, but **no dogs** yet. |
| `dogs[0] = new Dog();` | Now create a real dog and put it in place 0. |
| `dogs[0].name = "Rex";` | Set the name of the dog in place 0. |
| `for (Dog dog : dogs)` | For each dog in the array... |

🥚 **Story:** `new Dog[3]` buys an **empty egg box** with 3 places. `new Dog()` puts a real **egg** in one place.

> ⚠️ If you forget `dogs[0] = new Dog();` and write `dogs[0].name = "Rex";` → 💥 NullPointerException. The place is empty!

👉 Setting every field by hand is long and boring (`dogs[0].name = ...; dogs[0].age = ...;`). In the **next chapter**, constructors will let us write `new Dog("Rex", 3)` in **one** line! 🎉

---

## 🧩 Part 9: Objects inside objects

A field can be **another object**:

**File: `Owner.java`**

```java
public class Owner {
    String name;
    String phone;
}
```

**File: `Dog.java`** (updated)

```java
public class Dog {
    String name;
    int age;
    Owner owner;   // a Dog HAS an Owner

    void bark() {
        System.out.println(name + " says: Woof! 🐕");
    }

    void printOwner() {
        if (owner == null) {
            System.out.println(name + " has no owner. 😢");
        } else {
            System.out.println(name + "'s owner is " + owner.name + " (📞 " + owner.phone + ")");
        }
    }
}
```

**File: `Main.java`**

```java
public class Main {
    public static void main(String[] args) {
        Owner sara = new Owner();
        sara.name = "Sara";
        sara.phone = "555-1234";

        Dog rex = new Dog();
        rex.name = "Rex";
        rex.owner = sara;

        Dog stray = new Dog();
        stray.name = "Shadow";

        rex.printOwner();
        stray.printOwner();

        System.out.println(rex.owner.name);   // Sara — go into rex, then into owner
    }
}
```

**Output:**

```
Rex's owner is Sara (📞 555-1234)
Shadow has no owner. 😢
Sara
```

| Code | Meaning |
|---|---|
| `Owner owner;` | A field whose type is **another class**. Default: `null`. |
| `rex.owner = sara;` | Rex's `owner` field now points to the Sara object. |
| `rex.owner.name` | Chain dots: go into `rex` → into its `owner` → get `name`. |
| `if (owner == null)` | Shadow has no owner → we check to avoid a NullPointerException. |

This is called a **"has-a"** relationship: a Dog **has an** Owner. 🔗

> 🌱 **In Spring Boot**, this is how you'll connect data: a `Student` **has** a list of `Course`s, an `Order` **has** a `Customer`... (Chapter 75).

---

## 🎨 Part 10: How to design a class

When you need a class, ask two questions:

1. **What does it KNOW?** → fields (nouns, data)
2. **What can it DO?** → methods (verbs, actions)

### Example: a `Rectangle` 📐

| Knows (fields) | Can do (methods) |
|---|---|
| `width`, `height` | `area()`, `perimeter()`, `isSquare()` |

```java
public class Rectangle {
    double width;
    double height;

    double area() {
        return width * height;
    }

    double perimeter() {
        return 2 * (width + height);
    }

    boolean isSquare() {
        return width == height;
    }
}
```

```java
Rectangle r = new Rectangle();
r.width = 4;
r.height = 3;

System.out.println("Area: " + r.area());             // Area: 12.0
System.out.println("Perimeter: " + r.perimeter());   // Perimeter: 14.0
System.out.println("Square? " + r.isSquare());       // Square? false
```

### 📏 Drawing a class (UML)

Programmers often draw classes as boxes with 3 parts. This is called a **UML class diagram**:

```
 ┌──────────────────────┐
 │      Rectangle       │   ← class name
 ├──────────────────────┤
 │ width: double        │   ← fields
 │ height: double       │
 ├──────────────────────┤
 │ area(): double       │   ← methods
 │ perimeter(): double  │
 │ isSquare(): boolean  │
 └──────────────────────┘
```

You'll see diagrams like this in many books and at work. Now you can read them! 📖

---

## ✋ Try it yourself

**Task 1:** Make a class `Car` with fields `brand`, `color`, `speed` (int). Add methods:
- `accelerate(int amount)` — adds to speed
- `brake()` — sets speed to 0
- `printInfo()` — prints all fields

Create 2 cars in `main` and test the methods.

<details>
<summary>Click to see one possible answer</summary>

```java
// Car.java
public class Car {
    String brand;
    String color;
    int speed;

    void accelerate(int amount) {
        speed += amount;
    }

    void brake() {
        speed = 0;
    }

    void printInfo() {
        System.out.println(color + " " + brand + " driving at " + speed + " km/h");
    }
}
```

```java
// Main.java
public class Main {
    public static void main(String[] args) {
        Car car1 = new Car();
        car1.brand = "Toyota";
        car1.color = "Red";

        Car car2 = new Car();
        car2.brand = "BMW";
        car2.color = "Black";

        car1.accelerate(50);
        car2.accelerate(30);
        car2.accelerate(40);

        car1.printInfo();   // Red Toyota driving at 50 km/h
        car2.printInfo();   // Black BMW driving at 70 km/h

        car1.brake();
        car1.printInfo();   // Red Toyota driving at 0 km/h
    }
}
```

</details>

**Task 2:** Make a class `Circle` with a field `radius` and methods `area()` and `circumference()`. (Hint: `Math.PI`.)

**Task 3:** What does this print? Think first!

```java
Dog a = new Dog();
a.age = 2;
Dog b = new Dog();
b.age = 2;
Dog c = a;
c.age = 10;

System.out.println(a.age);
System.out.println(b.age);
System.out.println(a == b);
System.out.println(a == c);
```

<details>
<summary>Click to see the answer</summary>

```
10
2
false
true
```

`a` and `c` point to the **same** dog. `b` is a **different** dog.

</details>

**Task 4:** Make a class `Student` with `name` and `int[] scores`. Add a method `average()` that returns the average score. Create an array of 3 students and print who has the **best** average.

**Task 5:** Design (on paper first!) a class for a **light bulb** 💡. What does it know? What can it do? Then write it.

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `new`

```java
Dog rex;
rex.name = "Rex";   // ❌ error: variable rex might not have been initialized
```

```java
Dog rex = new Dog();   // ✅
rex.name = "Rex";
```

### Mistake 2: Using a `null` object → NullPointerException

```java
Dog[] dogs = new Dog[3];
dogs[0].name = "Rex";   // 💥 NullPointerException — the place is empty!
```

**Fix:** `dogs[0] = new Dog();` first.

### Mistake 3: Using `static` on instance methods

```java
public class Dog {
    String name;
    static void bark() {
        System.out.println(name);   // ❌ error: non-static variable name cannot be referenced from a static context
    }
}
```

A `static` method doesn't belong to any dog, so it doesn't know **which** dog's name to use. **Fix:** Remove `static`.

### Mistake 4: Calling an instance method on the class

```java
Dog.bark();   // ❌ error: non-static method bark() cannot be referenced from a static context
```

**Fix:** Call it on an **object**: `rex.bark();`

### Mistake 5: Thinking `b = a` copies the object

`b = a` copies the **reference** (the remote). Both point to the **same** object. (Part 6.)

### Mistake 6: Two public classes in one file

```java
// File: Main.java
public class Main { ... }
public class Dog { ... }   // ❌ error: class Dog is public, should be declared in a file named Dog.java
```

**Fix:** Put each public class in its own file.

> 💡 For quick tests, you **can** put a second class **without** `public` in the same file:
> ```java
> public class Main { ... }
> class Dog { ... }        // ✅ allowed (not public)
> ```
> But for real projects, use one file per class.

---

## ✅ Summary

- **OOP** puts data (fields) and actions (methods) together in **objects**.
- A **class** is a **plan** (cookie cutter 🍪). An **object** is a real thing made from it (a cookie).
- Fields = what an object **knows**. Methods = what an object **can do**.
- Instance methods (no `static`) belong to **each object** and can use its fields.
- Create an object: `Dog rex = new Dog();`
- Use the dot: `rex.name = "Rex";`, `rex.bark();`
- Each object has its **own** copy of the fields.
- Fields have **default values** (`0`, `false`, `null`).
- A class variable holds a **reference** (a remote control 📺). `b = a` → both point to the **same** object.
- `==` on objects asks "same object?", not "same content?".
- `null` = no object. Using it → **NullPointerException**. Check with `if (x != null)`.
- An array of objects starts full of `null`s. Fill it with `new`.
- A field can be another object ("has-a").

---

## ❓ Quiz

1. What is the difference between a class and an object?
2. What keyword creates a new object?
3. What are fields? What are methods?
4. `Dog d = new Dog();` — What is the value of `d.name` right after this line?
5. Why doesn't `bark()` have `static`?
6. What is `null`? What happens if you call a method on `null`?
7. `Dog[] dogs = new Dog[5];` — How many Dog objects exist now?
8. `Car a = new Car(); Car b = a; b.speed = 100;` — What is `a.speed`?
9. Name 3 fields and 3 methods for a class `Phone`. 📱

<details>
<summary>Click to see the answers</summary>

1. A class is a **plan/template**. An object is a **real thing** made from the plan.
2. `new`
3. Fields are variables inside a class (what an object **knows**). Methods are functions inside a class (what an object **can do**).
4. `null` (the default for a String field).
5. Because it must know **which** dog is barking. It belongs to each object, not to the class.
6. `null` means "no object". Calling a method on it causes a **NullPointerException**.
7. **Zero**! The array has 5 empty places (`null`).
8. `100` — `a` and `b` point to the same car.
9. Example — fields: `brand`, `batteryLevel`, `phoneNumber`. Methods: `call(String number)`, `charge()`, `sendMessage(String text)`.

</details>

---

[⬅ Previous chapter](../part-02-java-basics/17-comments-clean-code.md) | [Table of Contents](../README.md) | [Next chapter: Constructors ➡](19-constructors.md)
