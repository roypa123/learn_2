# Chapter 19 – Constructors: Building a New Object

[⬅ Previous chapter](18-classes-and-objects.md) | [Table of Contents](../README.md) | [Next chapter ➡](20-fields-methods-this.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **constructor** is, and why it's so useful
- The **default constructor** that Java gives you for free
- How to write constructors **with parameters**
- What `this.name = name` means
- How to have **many constructors** (overloading)
- How one constructor can call another with `this(...)`
- How to **check** values in a constructor

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Constructor** | A special method that runs **automatically** when you create an object with `new`. It **sets up** the new object. |
| **Default constructor** | A constructor with **no parameters** that Java creates for you if you write **no** constructor. |
| **`this`** | A word that means "**this object**" — the object we are inside right now. |
| **Overloading** | Many constructors (or methods) with the same name but different parameters. |
| **Constructor chaining** | One constructor calls another with `this(...)`. |
| **Initialize** | Give the first value. |

---

## 📖 Story: The baby hospital 👶

When a baby is born in a hospital, the nurses **immediately** do some things:

- Write the baby's **name** on a bracelet 📛
- Measure the **weight** ⚖️
- Write the **birth date** 📅

They do this **right away**, at the moment of birth. Not "maybe later". A baby **without** a name bracelet would be a problem!

A **constructor** is the same: it runs **at the moment the object is born** (`new`), and gives it everything it needs to start life correctly.

---

## 😩 Part 1: The problem

In Chapter 18, we made objects like this:

```java
Dog rex = new Dog();
rex.name = "Rex";
rex.age = 3;
rex.breed = "Labrador";
```

Problems:
1. **Long** — 4 lines for one dog.
2. **Easy to forget** a field — and then it's `null` or `0`. 🐛
3. You can make a "broken" dog with **no name** at all.

With a constructor:

```java
Dog rex = new Dog("Rex", 3, "Labrador");
```

**One** line. You **can't** forget anything — Java **forces** you to give all the values. 🎉

---

## 🏗️ Part 2: Your first constructor

**File: `Dog.java`**

```java
public class Dog {
    String name;
    int age;

    // This is the constructor
    Dog(String dogName, int dogAge) {
        name = dogName;
        age = dogAge;
        System.out.println("🐶 A new dog was born: " + name);
    }

    void bark() {
        System.out.println(name + " says: Woof!");
    }
}
```

**File: `Main.java`**

```java
public class Main {
    public static void main(String[] args) {
        Dog rex = new Dog("Rex", 3);
        Dog bella = new Dog("Bella", 5);

        rex.bark();
        bella.bark();
        System.out.println(bella.name + " is " + bella.age);
    }
}
```

**Output:**

```
🐶 A new dog was born: Rex
🐶 A new dog was born: Bella
Rex says: Woof!
Bella says: Woof!
Bella is 5
```

### 🔍 Line by line — the constructor

`Dog(String dogName, int dogAge) {`

| Part | Meaning |
|---|---|
| `Dog` | ⚠️ The constructor has **exactly the same name as the class**. |
| (nothing before `Dog`) | ⚠️ A constructor has **no return type** — not even `void`! |
| `(String dogName, int dogAge)` | Parameters, like a normal method. |
| `name = dogName;` | Put the parameter's value into the **field** `name`. |
| `age = dogAge;` | Same for `age`. |

### 🔍 What happens at `new Dog("Rex", 3)`?

```
 new Dog("Rex", 3)
   │
   ├─ 1. Java makes an EMPTY Dog object in memory
   │       (name = null, age = 0)
   │
   ├─ 2. Java runs the constructor with dogName = "Rex", dogAge = 3
   │       name = "Rex"
   │       age = 3
   │       prints "A new dog was born: Rex"
   │
   └─ 3. Java gives back the REFERENCE to the new object
           → it goes into the variable rex
```

### Constructor vs. method

| | Constructor | Method |
|---|---|---|
| Name | **same** as the class (`Dog`) | any name (`bark`) |
| Return type | **none** (not even `void`) | `void`, `int`, `String`... |
| When does it run? | **automatically**, once, at `new` | when **you** call it |
| Job | **set up** the new object | do any job |

---

## 🪞 Part 3: `this` — "this object"

Naming parameters `dogName`, `dogAge` works, but it's a little ugly. Most programmers give the parameters the **same names** as the fields:

```java
Dog(String name, int age) {
    name = name;   // ❌ ???
    age = age;     // ❌ ???
}
```

😵 Now there are **two** things called `name`: the field, and the parameter. Which one is which?

Java's rule: the **closest** one wins. Inside the constructor, `name` means the **parameter**. So `name = name` just puts the parameter into... itself. The field stays `null`! 🐛

### ✅ The fix: `this`

```java
Dog(String name, int age) {
    this.name = name;
    this.age = age;
}
```

| Code | Meaning |
|---|---|
| `this` | "**This** object" — the dog that is being built right now. |
| `this.name` | The **field** `name` of this object. |
| `name` | The **parameter** `name`. |
| `this.name = name;` | "Put the parameter `name` into **this object's** field `name`." |

```
     this.name    =    name
     ─────────         ────
     the FIELD         the PARAMETER
     (in the object)   (from the caller)
```

📖 **Story:** In a classroom, the teacher says "Give me **your** pencil" to a student named Sara. "Your" = **this** student. `this` is like saying "**my own**". 🙋

👉 **`this.name = name;`** is the **most common line** in Java constructors. You'll write it thousands of times. Get comfortable with it! 💪

### Full example

```java
public class Dog {
    String name;
    int age;
    String breed;

    Dog(String name, int age, String breed) {
        this.name = name;
        this.age = age;
        this.breed = breed;
    }

    void printInfo() {
        System.out.println(name + " (" + breed + "), " + age + " years old");
    }
}
```

```java
Dog rex = new Dog("Rex", 3, "Labrador");
rex.printInfo();   // Rex (Labrador), 3 years old
```

> 💡 **IntelliJ magic 🪄:** In a class, press **Alt + Insert** (Mac: **Cmd + N**) → **Constructor** → select the fields → **OK**. IntelliJ writes the whole constructor with `this.x = x` for you!

---

## 🎁 Part 4: The default constructor

In Chapter 18, our `Dog` class had **no** constructor, but `new Dog()` worked. How?

If you write **no constructor at all**, Java secretly adds an **empty** one:

```java
Dog() {
}
```

This is the **default constructor**. It does nothing — fields keep their default values (`null`, `0`).

### ⚠️ But: as soon as you write your own constructor, the free one is GONE!

```java
public class Dog {
    String name;

    Dog(String name) {
        this.name = name;
    }
}
```

```java
Dog a = new Dog("Rex");   // ✅
Dog b = new Dog();        // ❌ error: constructor Dog in class Dog cannot be applied to given types;
                          //    required: String   found: no arguments
```

Java thinks: "You wrote a constructor that needs a name. So you **want** every dog to have a name. I won't give you a way to make a dog without one." 🛡️

If you **also** want a no-argument constructor, write it yourself (see Part 5).

> 🌱 **Spring Boot note:** Some Spring tools (like JPA for databases — Chapter 71) **need** a no-argument constructor. You'll learn when.

---

## 🔀 Part 5: Many constructors (overloading)

A class can have **many constructors**, with different parameters. This gives users different ways to create an object:

```java
public class Pizza {
    String size;
    String topping;
    boolean extraCheese;

    // 1. Full control
    Pizza(String size, String topping, boolean extraCheese) {
        this.size = size;
        this.topping = topping;
        this.extraCheese = extraCheese;
    }

    // 2. No extra cheese
    Pizza(String size, String topping) {
        this.size = size;
        this.topping = topping;
        this.extraCheese = false;
    }

    // 3. The house special
    Pizza() {
        this.size = "medium";
        this.topping = "margherita";
        this.extraCheese = false;
    }

    void describe() {
        System.out.println("🍕 A " + size + " " + topping + " pizza"
                + (extraCheese ? " with extra cheese" : ""));
    }
}
```

```java
Pizza p1 = new Pizza("large", "pepperoni", true);
Pizza p2 = new Pizza("small", "mushroom");
Pizza p3 = new Pizza();

p1.describe();
p2.describe();
p3.describe();
```

**Output:**

```
🍕 A large pepperoni pizza with extra cheese
🍕 A small mushroom pizza
🍕 A medium margherita pizza
```

Java chooses the constructor by looking at the **number and types** of the arguments (just like method overloading — Chapter 15).

---

## ⛓️ Part 6: `this(...)` — one constructor calls another

Look at the Pizza class again. The same lines (`this.size = ...`, `this.topping = ...`) are repeated **3 times**. Not DRY! 😕

A constructor can call **another constructor** of the same class with `this(...)`:

```java
public class Pizza {
    String size;
    String topping;
    boolean extraCheese;

    Pizza(String size, String topping, boolean extraCheese) {
        this.size = size;
        this.topping = topping;
        this.extraCheese = extraCheese;
    }

    Pizza(String size, String topping) {
        this(size, topping, false);          // call constructor 1
    }

    Pizza() {
        this("medium", "margherita");        // call constructor 2 (which calls constructor 1)
    }
}
```

### 🔍 What happens at `new Pizza()`?

```
 new Pizza()
   └─► Pizza()                      → this("medium", "margherita")
         └─► Pizza(size, topping)   → this("medium", "margherita", false)
               └─► Pizza(size, topping, extraCheese)   → sets all 3 fields ✅
```

Now the real work is in **one** place. The other constructors just fill in the **default values**. 🎉

| Code | Meaning |
|---|---|
| `this(...)` | "Call **another constructor** of this class with these arguments." |

> ⚠️ **Rule:** `this(...)` must be the **very first line** in the constructor.
>
> ⚠️ Don't confuse them:
> - `this.name` → a **field** of this object
> - `this(...)` → **another constructor** of this class

---

## 🛡️ Part 7: Checking values in the constructor

A constructor is the **door** into the object. It's the perfect place to **check** that the values make sense:

```java
public class Person {
    String name;
    int age;

    Person(String name, int age) {
        if (name == null || name.isBlank()) {
            System.out.println("⚠️ Name is empty, using 'Unknown'.");
            name = "Unknown";
        }
        if (age < 0 || age > 150) {
            System.out.println("⚠️ Age " + age + " is not possible, using 0.");
            age = 0;
        }
        this.name = name;
        this.age = age;
    }
}
```

```java
Person p1 = new Person("Sara", 30);
Person p2 = new Person("", -5);

System.out.println(p1.name + ", " + p1.age);
System.out.println(p2.name + ", " + p2.age);
```

**Output:**

```
⚠️ Name is empty, using 'Unknown'.
⚠️ Age -5 is not possible, using 0.
Sara, 30
Unknown, 0
```

👉 Now it's **impossible** to create a Person with a negative age. The object is **always** in a good state. 🛡️

> 💡 Here we fix bad values and print a warning. In real programs, it's often better to **stop** and report an error (throw an **exception**). We learn that in Chapter 33:
> ```java
> if (age < 0) {
>     throw new IllegalArgumentException("Age cannot be negative: " + age);
> }
> ```

---

## 🧮 Part 8: Constructors can calculate

A constructor can do more than copy parameters. It can **calculate** fields:

```java
public class Rectangle {
    double width;
    double height;
    double area;

    Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
        this.area = width * height;   // calculated!
    }

    // A square is a rectangle with equal sides
    Rectangle(double side) {
        this(side, side);
    }
}
```

```java
Rectangle r = new Rectangle(4, 5);
Rectangle s = new Rectangle(3);

System.out.println(r.area);   // 20.0
System.out.println(s.area);   // 9.0
```

And fields can have **starting values** written directly:

```java
public class Game {
    String playerName;
    int score = 0;        // starts at 0
    int lives = 3;        // every game starts with 3 lives
    boolean isOver = false;

    Game(String playerName) {
        this.playerName = playerName;
    }
}
```

`new Game("Sara")` → `playerName = "Sara"`, `score = 0`, `lives = 3`, `isOver = false`.

---

## 💻 Mini project: Library books 📚

**File: `Book.java`**

```java
public class Book {
    String title;
    String author;
    int pages;
    boolean isBorrowed;

    Book(String title, String author, int pages) {
        this.title = title;
        this.author = author;
        this.pages = pages > 0 ? pages : 1;
        this.isBorrowed = false;
    }

    Book(String title, String author) {
        this(title, author, 100);
    }

    void borrow() {
        if (isBorrowed) {
            System.out.println("❌ '" + title + "' is already borrowed.");
        } else {
            isBorrowed = true;
            System.out.println("✅ You borrowed '" + title + "'.");
        }
    }

    void giveBack() {
        isBorrowed = false;
        System.out.println("📥 '" + title + "' was returned.");
    }

    void printInfo() {
        String status = isBorrowed ? "borrowed" : "available";
        System.out.println("📖 " + title + " by " + author + " (" + pages + " pages) — " + status);
    }
}
```

**File: `Library.java`**

```java
public class Library {
    public static void main(String[] args) {
        Book[] books = {
            new Book("The Hobbit", "J.R.R. Tolkien", 310),
            new Book("Charlotte's Web", "E.B. White", 192),
            new Book("My Diary", "Sara")
        };

        books[0].borrow();
        books[0].borrow();
        books[1].borrow();
        books[0].giveBack();

        System.out.println();
        System.out.println("=== All books ===");
        for (Book book : books) {
            book.printInfo();
        }
    }
}
```

**Output:**

```
✅ You borrowed 'The Hobbit'.
❌ 'The Hobbit' is already borrowed.
✅ You borrowed 'Charlotte's Web'.
📥 'The Hobbit' was returned.

=== All books ===
📖 The Hobbit by J.R.R. Tolkien (310 pages) — available
📖 Charlotte's Web by E.B. White (192 pages) — borrowed
📖 My Diary by Sara (100 pages) — available
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `Book[] books = { new Book(...), ... };` | Create the array **and** the objects in one step. Much shorter than Chapter 18! |
| `this.pages = pages > 0 ? pages : 1;` | Check the value with a ternary. |
| `this(title, author, 100);` | The short constructor uses 100 pages as a default. |
| `this.isBorrowed = false;` | Every new book starts **available**. |

---

## ✋ Try it yourself

**Task 1:** Add a constructor to the `Car` class from Chapter 18: `Car(String brand, String color)`. Speed should start at 0. Create 3 cars in one array.

<details>
<summary>Click to see the answer</summary>

```java
public class Car {
    String brand;
    String color;
    int speed;

    Car(String brand, String color) {
        this.brand = brand;
        this.color = color;
        this.speed = 0;
    }
}

// in main:
Car[] cars = {
    new Car("Toyota", "Red"),
    new Car("BMW", "Black"),
    new Car("Fiat", "White")
};
```

</details>

**Task 2:** Make a class `Student` with `name`, `grade` (int) and `school`. Write **two** constructors:
- `Student(String name, int grade, String school)`
- `Student(String name, int grade)` — uses `"Green Hill School"` as the school. Use `this(...)`!

<details>
<summary>Click to see the answer</summary>

```java
public class Student {
    String name;
    int grade;
    String school;

    Student(String name, int grade, String school) {
        this.name = name;
        this.grade = grade;
        this.school = school;
    }

    Student(String name, int grade) {
        this(name, grade, "Green Hill School");
    }
}
```

</details>

**Task 3:** Find the bug. Why is the name always `null`?

```java
public class Cat {
    String name;

    Cat(String name) {
        name = name;
    }
}
```

<details>
<summary>Click to see the answer</summary>

`name = name;` puts the **parameter** into **itself**. The field is never set.
**Fix:** `this.name = name;`

</details>

**Task 4:** Make a class `Temperature` with a field `celsius`. Add two constructors: one takes Celsius, and one takes a `double` and a `String` unit (`"C"` or `"F"`). If the unit is `"F"`, convert to Celsius: `C = (F − 32) × 5 / 9`.

**Task 5:** Make a class `Timer` whose constructor takes **seconds** and calculates the fields `hours`, `minutes` and `seconds` (use `/` and `%` like in Chapter 8).

---

## ⚠️ Common mistakes

### Mistake 1: Giving the constructor a return type

```java
public class Dog {
    String name;

    void Dog(String name) {     // ❌ this is NOT a constructor, it's a method called "Dog"!
        this.name = name;
    }
}

new Dog("Rex");   // ❌ error: constructor Dog in class Dog cannot be applied to given types
```

**Fix:** Remove `void`. Constructors have **no** return type.

### Mistake 2: Wrong name

```java
public class Dog {
    dog(String name) { }    // ❌ error: invalid method declaration; return type required
}
```

The constructor name must be **exactly** the class name (capital `D`).

### Mistake 3: Forgetting `this.`

```java
Dog(String name) {
    name = name;   // ❌ no error, but the field stays null
}
```

### Mistake 4: Expecting the default constructor after writing your own

```java
public class Dog {
    Dog(String name) { ... }
}
new Dog();   // ❌ error — the free empty constructor is gone
```

**Fix:** Write `Dog() { }` yourself if you need it.

### Mistake 5: `this(...)` not on the first line

```java
Pizza() {
    System.out.println("Making pizza");
    this("medium", "margherita");   // ❌ Java 21 and older: call to this must be first statement in constructor
}
```

(Java 25 relaxes this rule: simple code that doesn't use the object may come before `this(...)`. But keeping `this(...)` first is always safe and clear, and it works in every Java version.)

### Mistake 6: Wrong order of arguments

```java
Dog(String name, int age) { ... }

new Dog(3, "Rex");   // ❌ error: incompatible types
```

Arguments must match the parameters in **order** and **type**.

---

## ✅ Summary

- A **constructor** sets up a new object. It runs **automatically** at `new`.
- Same **name** as the class. **No** return type (not even `void`).
- `this.name = name;` → put the **parameter** into **this object's field**.
- If you write **no** constructor, Java gives you a free empty **default constructor**. If you write **any** constructor, the free one disappears.
- You can have **many constructors** with different parameters (overloading).
- `this(...)` calls another constructor — put it **first**. Keeps the code DRY.
- Use constructors to **check** values, so objects are always in a **good state**.
- Fields can have **starting values**: `int lives = 3;`
- IntelliJ: **Alt + Insert → Constructor** writes it for you.

---

## ❓ Quiz

1. When does a constructor run?
2. What is the return type of a constructor?
3. What does `this.age = age;` mean?
4. A class has **no** constructor. Can you write `new MyClass()`?
5. A class has only the constructor `MyClass(int x)`. Can you write `new MyClass()`?
6. What is the difference between `this.name` and `this(...)`?
7. Where must `this(...)` be written?
8. Why is a constructor a good place to check values?

<details>
<summary>Click to see the answers</summary>

1. Automatically, once, when the object is created with `new`.
2. It has **none** — not even `void`.
3. "Put the parameter `age` into the field `age` of this object."
4. Yes — Java adds a free default constructor.
5. No — you wrote a constructor, so the default one is gone.
6. `this.name` is a **field** of this object. `this(...)` calls **another constructor** of this class.
7. On the **first line** of a constructor.
8. Because every object must pass through it. If it checks the values, no object can ever be created in a bad state.

</details>

---

[⬅ Previous chapter](18-classes-and-objects.md) | [Table of Contents](../README.md) | [Next chapter: Fields, methods and this ➡](20-fields-methods-this.md)
