# Chapter 20 – Fields, Methods and the Word `this`

[⬅ Previous chapter](19-constructors.md) | [Table of Contents](../README.md) | [Next chapter ➡](21-encapsulation.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- The difference between **fields**, **parameters** and **local variables**
- All the uses of **`this`**
- How objects **talk to each other** (one object calls another object's method)
- **Method chaining**: `order.add("tea").add("cake").pay()`
- **`toString()`**: how to print an object nicely
- **`equals()`** and **`hashCode()`**: how to check if two objects are "the same"
- The secret parent of every class: **`Object`**

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Instance variable** | Another name for a **field**. Each instance (object) has its own. |
| **Local variable** | A variable made **inside** a method. It disappears when the method ends. |
| **Lifetime** | How long a variable **exists**. |
| **Method chaining** | Calling many methods in a row on one line: `a.b().c().d()`. |
| **`toString()`** | A method that turns an object into **text**. |
| **`equals()`** | A method that checks if two objects have the **same content**. |
| **`hashCode()`** | A number made from an object's content. Used by `HashMap` and `HashSet` (Chapters 31–32). |
| **Override** | Write your **own version** of a method that already exists in a parent class. |
| **`@Override`** | An **annotation** (a label) that says "I am overriding a method". |

---

## 📖 Story: A student's backpack and a notebook 🎒📓

Think of a **student** (an object).

- Things in the student's **backpack** stay with the student **all day**: books, pencil case, lunch box. → These are **fields**. They live as long as the object lives.
- During math class, the student uses a **scrap paper** to calculate something. After class, they throw it away. 🗑️ → This is a **local variable**. It lives only during the method.
- The teacher **gives** the student a worksheet for the lesson. → This is a **parameter**. It comes from outside, for this one job.

---

## 📦 Part 1: Three kinds of variables

```java
public class Student {
    String name;          // ① FIELD
    int totalPoints;      // ① FIELD

    void addPoints(int points) {            // ② PARAMETER: points
        int bonus = points / 10;            // ③ LOCAL VARIABLE: bonus
        totalPoints += points + bonus;
        System.out.println(name + " got " + points + " + " + bonus + " bonus");
    }
}
```

| Kind | Where is it written? | Lives how long? | Default value? | Who can use it? |
|---|---|---|---|---|
| ① **Field** | in the class, outside methods | as long as the **object** lives | ✅ yes (`0`, `null`...) | all methods of the object |
| ② **Parameter** | in the method's `( )` | during **one** method call | — (gets the argument) | only that method |
| ③ **Local variable** | inside a method's `{ }` | during **one** method call (or block) | ❌ no — must be set | only that method/block |

```java
Student s = new Student();
s.name = "Sara";
s.addPoints(50);   // Sara got 50 + 5 bonus
s.addPoints(30);   // Sara got 30 + 3 bonus
System.out.println(s.totalPoints);   // 88
```

- `totalPoints` **remembers** between calls (50+5, then +30+3 = 88). It's a field. 🎒
- `bonus` is **new** every call, and forgotten after. It's local. 📝

👉 **Rule of thumb:** If the object needs to **remember** it → field. If you only need it **during** a calculation → local variable.

---

## 🪞 Part 2: All the uses of `this`

`this` means "**the object we are inside right now**". It has 4 uses:

### Use 1: Field vs. parameter with the same name (you know this!)

```java
Student(String name) {
    this.name = name;
}
```

### Use 2: Make it clear that it's a field (optional)

```java
void printName() {
    System.out.println(this.name);   // same as: System.out.println(name);
}
```

Here there's no parameter called `name`, so `this.` is **optional**. Some programmers like it for clarity.

### Use 3: Call another constructor (you know this too!)

```java
Student() {
    this("Unknown");
}
```

### Use 4: Give **yourself** to someone else

An object can pass **itself** to another object's method:

```java
public class Student {
    String name;

    Student(String name) {
        this.name = name;
    }

    void joinClub(Club club) {
        club.addMember(this);   // "Club, please add ME"
    }
}
```

```java
public class Club {
    String clubName;
    Student[] members = new Student[10];
    int count = 0;

    Club(String clubName) {
        this.clubName = clubName;
    }

    void addMember(Student student) {
        members[count] = student;
        count++;
        System.out.println(student.name + " joined the " + clubName + " club!");
    }
}
```

```java
Club chess = new Club("Chess ♟️");
Student sara = new Student("Sara");
sara.joinClub(chess);   // Sara joined the Chess ♟️ club!
```

| Code | Meaning |
|---|---|
| `club.addMember(this)` | `this` is the student object Sara. She passes **herself** to the club. |

### Use 5: Return yourself (for method chaining — see Part 4)

```java
Order add(String item) {
    ...
    return this;
}
```

---

## 🤝 Part 3: Objects talking to each other

In OOP, a program is a team of objects that **send messages** (call methods) to each other. 📨

### Example: a coffee shop ☕

**File: `CoffeeMachine.java`**

```java
public class CoffeeMachine {
    int beans = 100;   // grams

    String makeCoffee(String type) {
        int needed = type.equals("espresso") ? 10 : 15;
        if (beans < needed) {
            return null;   // can't make it
        }
        beans -= needed;
        return "☕ " + type;
    }
}
```

**File: `Barista.java`**

```java
public class Barista {
    String name;
    CoffeeMachine machine;

    Barista(String name, CoffeeMachine machine) {
        this.name = name;
        this.machine = machine;
    }

    void serve(String customer, String coffeeType) {
        String coffee = machine.makeCoffee(coffeeType);   // talk to the machine
        if (coffee == null) {
            System.out.println(name + ": Sorry " + customer + ", we're out of beans! 😢");
        } else {
            System.out.println(name + ": Here is your " + coffee + ", " + customer + "!");
        }
    }
}
```

**File: `CoffeeShop.java`**

```java
public class CoffeeShop {
    public static void main(String[] args) {
        CoffeeMachine machine = new CoffeeMachine();
        Barista lina = new Barista("Lina", machine);

        lina.serve("Tom", "espresso");
        lina.serve("Sara", "latte");
        System.out.println("Beans left: " + machine.beans + "g");
    }
}
```

**Output:**

```
Lina: Here is your ☕ espresso, Tom!
Lina: Here is your ☕ latte, Sara!
Beans left: 75g
```

### 🔍 Who talks to whom?

```
  main ──── serve("Tom", "espresso") ───►  Barista lina
                                              │
                                              │ makeCoffee("espresso")
                                              ▼
                                          CoffeeMachine
                                              │ returns "☕ espresso"
                                              ▼
                                          lina prints the message
```

👉 Each object has **one job**: the machine makes coffee, the barista serves customers. Neither needs to know **how** the other does its job. This is **good design**. 🏆

> 🌱 **This is exactly how Spring Boot works!** A `StudentController` talks to a `StudentService`, which talks to a `StudentRepository`. Each one has **one job**. Just like the barista and the coffee machine! (Chapter 63.)

---

## ⛓️ Part 4: Method chaining

If a method returns `this`, you can call **another method right after it**:

```java
public class Order {
    String[] items = new String[10];
    int count = 0;
    double total = 0;

    Order add(String item, double price) {
        items[count] = item;
        count++;
        total += price;
        return this;          // give back THIS order
    }

    Order addTip(double tip) {
        total += tip;
        return this;
    }

    void pay() {
        System.out.println("Paid " + total + " for " + count + " items. 💳");
    }
}
```

```java
new Order()
    .add("Tea", 2.50)
    .add("Cake", 4.00)
    .add("Water", 1.00)
    .addTip(1.50)
    .pay();
```

**Output:**

```
Paid 9.0 for 3 items. 💳
```

### 🔍 How it works

```
 new Order()             → an Order object (let's call it O)
   .add("Tea", 2.50)     → returns O
   .add("Cake", 4.00)    → returns O
   .add("Water", 1.00)   → returns O
   .addTip(1.50)         → returns O
   .pay()                → prints
```

Every method returns the **same** object, so the next `.` is called on it again.

👉 You already used chaining with Strings: `text.strip().toLowerCase()` (but Strings return a **new** String each time). And you'll see chaining **everywhere** in Spring Boot, like:

```java
ResponseEntity.status(201).body(student);
```

---

## 🖨️ Part 5: `toString()` — print an object nicely

What happens if you print an object?

```java
Dog rex = new Dog("Rex", 3);
System.out.println(rex);
```

**Output:**

```
Dog@4e50df2e
```

😕 Strange! This is the **class name** + `@` + a number (like an ID). Not useful.

### Write your own `toString()`

```java
public class Dog {
    String name;
    int age;

    Dog(String name, int age) {
        this.name = name;
        this.age = age;
    }

    @Override
    public String toString() {
        return "Dog{name='" + name + "', age=" + age + "}";
    }
}
```

```java
Dog rex = new Dog("Rex", 3);
System.out.println(rex);
System.out.println("My dog: " + rex);
```

**Output:**

```
Dog{name='Rex', age=3}
My dog: Dog{name='Rex', age=3}
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `@Override` | A **label** that says: "I'm writing my **own version** of a method that already exists." Java checks that it really exists — if you make a typo (like `tostring`), you get an error. 🛡️ |
| `public` | Must be `public` (because the original is public). |
| `String toString()` | Exactly this name and return type. |
| `return "Dog{...}";` | Return any text you want. |

### ✨ The magic

Java calls `toString()` **automatically** when:
- you `println` an object
- you glue an object with a String using `+`

👉 **Always** write a `toString()` for your classes. It makes debugging **much** easier — you can just print the object and see what's inside!

> 💡 **IntelliJ:** **Alt + Insert** → **toString()** → select fields → **OK**. Done! 🪄

---

## 🟰 Part 6: `equals()` — are two objects "the same"?

Remember: `==` on objects asks "is it the **same object**?" (same remote target).

```java
Dog a = new Dog("Rex", 3);
Dog b = new Dog("Rex", 3);

System.out.println(a == b);        // false — two different objects
System.out.println(a.equals(b));   // false 😕 — why?!
```

By default, `equals()` does the **same** thing as `==`. Java doesn't know what "equal" means for **your** class. Is a dog equal when the name is the same? The name **and** age? You must decide!

### Write your own `equals()`

```java
@Override
public boolean equals(Object other) {
    if (this == other) return true;                       // ① same object
    if (other == null || getClass() != other.getClass()) return false;   // ② not a Dog
    Dog dog = (Dog) other;                                 // ③ treat it as a Dog
    return age == dog.age && name.equals(dog.name);        // ④ compare the fields
}
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `equals(Object other)` | The parameter type is `Object` (any object — see Part 8). |
| ① `if (this == other) return true;` | If it's literally the same object → equal. Fast shortcut. |
| ② `if (other == null \|\| getClass() != other.getClass()) return false;` | If `other` is nothing, or not the same class (comparing a Dog with a Cat 🐱) → not equal. |
| ③ `Dog dog = (Dog) other;` | **Cast**: "I know `other` is a Dog, treat it as one" — so we can read its fields. |
| ④ `return age == dog.age && name.equals(dog.name);` | Equal if **all** important fields are equal. Use `==` for numbers, `.equals()` for Strings. |

```java
Dog a = new Dog("Rex", 3);
Dog b = new Dog("Rex", 3);
Dog c = new Dog("Max", 3);

System.out.println(a.equals(b));   // true ✅
System.out.println(a.equals(c));   // false
```

### `hashCode()` — always together with `equals()`

**Rule:** If you write `equals()`, you **must** also write `hashCode()`. Two equal objects must have the same hash code. Otherwise `HashMap` and `HashSet` (Chapters 31–32) will behave strangely.

```java
@Override
public int hashCode() {
    return java.util.Objects.hash(name, age);
}
```

`Objects.hash(...)` makes a number from the fields. Same fields → same number. ✅

> 💡 **IntelliJ:** **Alt + Insert** → **equals() and hashCode()** → select fields → done! You rarely write these by hand. 🪄
>
> 💡 **Records** (Chapter 29) write `equals`, `hashCode` and `toString` for you **automatically**!

### 🤔 When do you need `equals()`?

When you want to compare objects by their **content**: "Is this the same student (same ID)?", "Is this product already in the cart?"

> 🌱 **Spring Boot note:** For database objects (entities), `equals` and `hashCode` matter a lot. We'll come back to this in Chapter 71.

---

## 👴 Part 7: `Object` — the parent of everything

Where do `toString()` and `equals()` come from, if we didn't write them?

Every class in Java secretly **extends** (is a child of) a class called **`Object`**:

```java
public class Dog { ... }
// is really:
public class Dog extends Object { ... }
```

`Object` gives **every** class some basic methods:

| Method | What the default version does |
|---|---|
| `toString()` | returns `ClassName@number` |
| `equals(Object o)` | same as `==` |
| `hashCode()` | a number based on the memory location |
| `getClass()` | returns the class of the object |

When you write your own `toString()` with `@Override`, you **replace** `Object`'s version. We learn all about parents and children (**inheritance**) in Chapter 22. 👨‍👧

---

## 💻 Mini project: A to-do list ✅

**File: `Task.java`**

```java
public class Task {
    String title;
    int priority;     // 1 = high, 2 = medium, 3 = low
    boolean done;

    Task(String title, int priority) {
        this.title = title;
        this.priority = priority;
        this.done = false;
    }

    void complete() {
        done = true;
    }

    @Override
    public String toString() {
        String box = done ? "[x]" : "[ ]";
        String stars = "!".repeat(4 - priority);
        return box + " " + title + " " + stars;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) return true;
        if (other == null || getClass() != other.getClass()) return false;
        Task task = (Task) other;
        return title.equalsIgnoreCase(task.title);
    }

    @Override
    public int hashCode() {
        return title.toLowerCase().hashCode();
    }
}
```

**File: `TodoList.java`**

```java
public class TodoList {
    Task[] tasks = new Task[20];
    int count = 0;

    TodoList add(String title, int priority) {
        Task newTask = new Task(title, priority);
        for (int i = 0; i < count; i++) {
            if (tasks[i].equals(newTask)) {
                System.out.println("⚠️ '" + title + "' is already in the list.");
                return this;
            }
        }
        tasks[count] = newTask;
        count++;
        return this;
    }

    void complete(String title) {
        for (int i = 0; i < count; i++) {
            if (tasks[i].title.equalsIgnoreCase(title)) {
                tasks[i].complete();
                return;
            }
        }
        System.out.println("⚠️ No task called '" + title + "'.");
    }

    void print() {
        System.out.println("===== TO-DO =====");
        for (int i = 0; i < count; i++) {
            System.out.println(tasks[i]);
        }
    }

    public static void main(String[] args) {
        TodoList list = new TodoList();

        list.add("Learn Java", 1)
            .add("Buy milk", 3)
            .add("Call grandma", 2)
            .add("learn java", 2);

        list.complete("Buy milk");
        list.complete("Fly to the moon");

        list.print();
    }
}
```

**Output:**

```
⚠️ 'learn java' is already in the list.
⚠️ No task called 'Fly to the moon'.
===== TO-DO =====
[ ] Learn Java !!!
[x] Buy milk !
[ ] Call grandma !!
```

### 🔍 What we used

| Code | Concept |
|---|---|
| `title`, `priority`, `done` | Fields |
| `Task newTask = ...` in `add` | Local variable |
| `return this;` | Method chaining |
| `System.out.println(tasks[i])` | Calls our `toString()` automatically |
| `tasks[i].equals(newTask)` | Our own `equals()` — ignores big/small letters |
| `TodoList` uses `Task` objects | Objects talking to each other |

---

## ✋ Try it yourself

**Task 1:** Add a `toString()` to your `Car` class from Chapter 19. Print an array of cars with a for-each loop.

**Task 2:** Make a class `Point` with `int x` and `int y`. Write `toString()` (like `(3, 4)`), `equals()` and `hashCode()`. Test that `new Point(3, 4).equals(new Point(3, 4))` is `true`.

<details>
<summary>Click to see the answer</summary>

```java
import java.util.Objects;

public class Point {
    int x;
    int y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public String toString() {
        return "(" + x + ", " + y + ")";
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) return true;
        if (other == null || getClass() != other.getClass()) return false;
        Point p = (Point) other;
        return x == p.x && y == p.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }

    public static void main(String[] args) {
        Point a = new Point(3, 4);
        Point b = new Point(3, 4);
        System.out.println(a);              // (3, 4)
        System.out.println(a == b);         // false
        System.out.println(a.equals(b));    // true
    }
}
```

</details>

**Task 3:** Add a method `double distanceTo(Point other)` to `Point`. Formula: √((x₂−x₁)² + (y₂−y₁)²). Test: distance from (0,0) to (3,4) is 5.0.

**Task 4:** Make a `Calculator` class with a field `value` and chainable methods `plus(double)`, `minus(double)`, `times(double)`, `dividedBy(double)` and `result()`. Example: `new Calculator(10).plus(5).times(2).result()` → `30.0`.

<details>
<summary>Click to see the answer</summary>

```java
public class Calculator {
    double value;

    Calculator(double start) {
        this.value = start;
    }

    Calculator plus(double n)      { value += n; return this; }
    Calculator minus(double n)     { value -= n; return this; }
    Calculator times(double n)     { value *= n; return this; }
    Calculator dividedBy(double n) { value /= n; return this; }

    double result() {
        return value;
    }
}
```

</details>

**Task 5:** Which kind of variable (field, parameter, local) is each one?

```java
public class Shop {
    String shopName;
    double sell(double price, int amount) {
        double total = price * amount;
        return total;
    }
}
```

<details>
<summary>Click to see the answer</summary>

`shopName` → field. `price`, `amount` → parameters. `total` → local variable.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Using a local variable when you need a field

```java
public class Counter {
    void click() {
        int count = 0;   // ❌ new variable every click → always 1
        count++;
        System.out.println(count);
    }
}
```

**Fix:** Make `count` a **field** so it remembers between calls.

### Mistake 2: Typo in `toString`

```java
public String tostring() { ... }   // small 's' → a NEW method, not an override. println still shows Dog@4e50df2e
```

**Fix:** Always add `@Override`. Then Java gives an error for the typo: `method does not override or implement a method from a supertype`.

### Mistake 3: `toString` not public

```java
@Override
String toString() { ... }   // ❌ error: attempting to assign weaker access privileges; was public
```

### Mistake 4: Writing `equals(Dog other)` instead of `equals(Object other)`

```java
public boolean equals(Dog other) { ... }   // ⚠️ this is overloading, not overriding!
```

Java's tools (like `HashSet`) call `equals(Object)`, and they won't use your version. **Fix:** The parameter must be `Object`. `@Override` will catch this mistake.

### Mistake 5: `equals` without `hashCode`

Objects will seem to "disappear" from `HashSet` and `HashMap`. **Always write both** (or let IntelliJ generate both).

### Mistake 6: `this` in a static method

```java
public static void main(String[] args) {
    System.out.println(this.name);   // ❌ error: non-static variable this cannot be referenced from a static context
}
```

`static` methods don't belong to any object, so there's no "this". (Chapter 27.)

---

## ✅ Summary

- **Fields** live as long as the object. **Parameters** and **local variables** live only during a method call.
- `this` = "the current object". Uses: `this.field`, `this(...)`, pass yourself (`club.add(this)`), return yourself (`return this`).
- Objects **talk** to each other by calling methods. Give each object **one job**.
- **Method chaining**: methods `return this;` so you can write `a.x().y().z()`.
- **`toString()`**: how an object looks as text. Called automatically by `println` and `+`. Always write one!
- **`equals()`**: compare objects by **content**. Parameter must be `Object`. Always write **`hashCode()`** too.
- **`@Override`**: says "I'm replacing a parent's method". It catches typos.
- Every class is a child of **`Object`**, which gives default `toString`, `equals`, `hashCode`.
- IntelliJ: **Alt + Insert** generates constructors, `toString`, `equals` and `hashCode`.

---

## ❓ Quiz

1. What is the difference between a field and a local variable?
2. What does `return this;` allow you to do?
3. What is printed by `System.out.println(obj)` if the class has no `toString()`?
4. Why should you write `@Override` above `toString()`?
5. `a == b` is `false`, but `a.equals(b)` is `true`. Is that possible? When?
6. If you write `equals()`, which other method must you write?
7. What is the parent class of every class in Java?
8. In `void join(Club c) { c.add(this); }` — what is `this`?

<details>
<summary>Click to see the answers</summary>

1. A field belongs to the object and lives as long as the object. A local variable lives only inside one method call and has no default value.
2. Method chaining: calling another method right after on the same object.
3. Something like `ClassName@4e50df2e`.
4. So Java checks that you are really overriding a method. A typo becomes an error instead of a silent bug.
5. Yes — when they are two **different objects** with the **same content**, and the class has its own `equals()`.
6. `hashCode()`
7. `Object`
8. The current object — the one whose `join` method is running.

</details>

---

[⬅ Previous chapter](19-constructors.md) | [Table of Contents](../README.md) | [Next chapter: Hiding data (encapsulation) ➡](21-encapsulation.md)
