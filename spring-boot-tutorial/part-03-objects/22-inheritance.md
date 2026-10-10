# Chapter 22 – Inheritance: Children Get Things from Parents

[⬅ Previous chapter](21-encapsulation.md) | [Table of Contents](../README.md) | [Next chapter ➡](23-polymorphism.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What **inheritance** is, and why it saves you from repeating code
- How to make a **child class** with `extends`
- What a child **gets** from the parent, and what it can **add**
- How to **override** (replace) a parent's method
- How to use **`super`** to call the parent's constructor and methods
- What **`protected`** means
- The **"is-a"** test: when to use inheritance, and when **not** to
- What **`final`** means for classes and methods

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Inheritance** | A class **gets** (inherits) the fields and methods of another class. |
| **Parent class** | The class that **gives**. Also called **superclass** or **base class**. |
| **Child class** | The class that **gets**. Also called **subclass** or **derived class**. |
| **`extends`** | The keyword to say "this class is a child of that class". |
| **Override** | The child writes its **own version** of a parent's method. |
| **`super`** | A word that means "**my parent**". |
| **`protected`** | Visible to the class, its package, and its **children**. |
| **"is-a"** | A test: "A Dog **is an** Animal" → inheritance is OK. |
| **Hierarchy** | A family tree of classes. 🌳 |

---

## 📖 Story: The family tree 👨‍👩‍👧

A child **inherits** things from their parents: eye color, hair color, the family name. The child doesn't have to "make" these — they just **get** them.

But the child is also **unique**: they can have their own hobbies 🎸, their own skills, and sometimes they do things **differently** than their parents.

```
              👴 Parent: Animal
              - name, age
              - eat(), sleep()
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   🐕 Dog        🐈 Cat        🐦 Bird
   + fetch()    + scratch()    + fly()
   (gets name,  (gets name,    (gets name,
    age, eat,    age, eat,      age, eat,
    sleep)       sleep)         sleep)
```

- Every Dog, Cat, Bird **is an** Animal.
- They all **get** `name`, `age`, `eat()`, `sleep()` from Animal — written only **once**!
- Each one **adds** its own special skill.

---

## 😩 Part 1: The problem — repeated code

Without inheritance:

```java
public class Dog {
    String name;
    int age;
    void eat()   { System.out.println(name + " is eating."); }
    void sleep() { System.out.println(name + " is sleeping."); }
    void fetch() { System.out.println(name + " fetches the ball! 🎾"); }
}

public class Cat {
    String name;                                                   // 😩 again
    int age;                                                       // 😩 again
    void eat()   { System.out.println(name + " is eating."); }    // 😩 again
    void sleep() { System.out.println(name + " is sleeping."); }  // 😩 again
    void scratch() { System.out.println(name + " scratches! 🐾"); }
}
```

The same code **two times**. With 10 animals → 10 times! And if you want to change `eat()`, you must change it in **10 places**. 😱 Not DRY!

---

## 👨‍👧 Part 2: `extends` — making a child class

**File: `Animal.java`** (the parent)

```java
public class Animal {
    String name;
    int age;

    void eat() {
        System.out.println(name + " is eating. 🍖");
    }

    void sleep() {
        System.out.println(name + " is sleeping. 💤");
    }
}
```

**File: `Dog.java`** (a child)

```java
public class Dog extends Animal {
    void fetch() {
        System.out.println(name + " fetches the ball! 🎾");
    }
}
```

**File: `Cat.java`** (another child)

```java
public class Cat extends Animal {
    void scratch() {
        System.out.println(name + " scratches the sofa! 🐾");
    }
}
```

**File: `Main.java`**

```java
public class Main {
    public static void main(String[] args) {
        Dog rex = new Dog();
        rex.name = "Rex";       // from Animal
        rex.eat();              // from Animal
        rex.fetch();            // Dog's own method

        Cat tom = new Cat();
        tom.name = "Tom";       // from Animal
        tom.sleep();            // from Animal
        tom.scratch();          // Cat's own method
    }
}
```

**Output:**

```
Rex is eating. 🍖
Rex fetches the ball! 🎾
Tom is sleeping. 💤
Tom scratches the sofa! 🐾
```

### 🔍 Line by line

`public class Dog extends Animal {`

| Part | Meaning |
|---|---|
| `class Dog` | A new class called Dog. |
| `extends` | "is a child of" / "builds on". |
| `Animal` | The parent class. |

So: **"Dog is a child of Animal."** Dog **automatically** gets `name`, `age`, `eat()` and `sleep()`. It only needs to write what is **new**: `fetch()`.

### 🗺️ What's inside a Dog object?

```
  rex ───►  ┌────────────────────────────┐
            │ Dog object                 │
            │ ┌────────────────────────┐ │
            │ │ from Animal:           │ │
            │ │   name = "Rex"         │ │
            │ │   age  = 0             │ │
            │ │   eat(), sleep()       │ │
            │ └────────────────────────┘ │
            │ from Dog:                  │
            │   fetch()                  │
            └────────────────────────────┘
```

👉 A child = **everything** from the parent **+** its own extra things.

### ⚠️ It only goes one way

```java
Animal a = new Animal();
a.fetch();   // ❌ error: cannot find symbol — an Animal doesn't know how to fetch!
```

The **child** knows everything the parent knows. The **parent** does **not** know the child's extras. (A dog is an animal, but not every animal can fetch. 🐟🎾❓)

---

## 🔄 Part 3: Overriding — doing it differently

Every animal makes a sound, but **different** sounds! Let's give `Animal` a `makeSound()` method, and let each child **override** it:

```java
public class Animal {
    String name;

    void makeSound() {
        System.out.println(name + " makes a sound.");
    }
}
```

```java
public class Dog extends Animal {
    @Override
    void makeSound() {
        System.out.println(name + " says: Woof! 🐕");
    }
}
```

```java
public class Cat extends Animal {
    @Override
    void makeSound() {
        System.out.println(name + " says: Meow! 🐈");
    }
}
```

```java
public class Fish extends Animal {
    // no override — uses the parent's version
}
```

```java
Dog rex = new Dog();   rex.name = "Rex";
Cat tom = new Cat();   tom.name = "Tom";
Fish nemo = new Fish(); nemo.name = "Nemo";

rex.makeSound();
tom.makeSound();
nemo.makeSound();
```

**Output:**

```
Rex says: Woof! 🐕
Tom says: Meow! 🐈
Nemo makes a sound.
```

### 🔍 What is overriding?

| | Meaning |
|---|---|
| **Override** | The child writes a method with the **same name and same parameters** as the parent. The child's version **replaces** the parent's version — for objects of the child class. |
| `@Override` | A label that asks Java to **check**: "Does the parent really have this method?" If you make a typo (`makeSond`), you get an error instead of a silent bug. ✅ Always use it! |

👉 You already did this in Chapter 20: `toString()` overrides `Object`'s version!

### 🆚 Overriding vs. overloading

These words sound alike, but they are **different**:

| | **Overloading** (Chapter 15) | **Overriding** (this chapter) |
|---|---|---|
| Where | in the **same** class | in a **child** class |
| Name | same | same |
| Parameters | **different** | **same** |
| Purpose | different ways to call | **replace** the parent's behavior |
| Example | `add(int, int)` and `add(double, double)` | `Dog.makeSound()` replaces `Animal.makeSound()` |

---

## 👆 Part 4: `super` — talking to the parent

### `super.method()` — use the parent's version **and** add something

Sometimes the child doesn't want to **replace** the parent's method completely. It wants to do the parent's work **plus** something extra:

```java
public class Animal {
    String name;

    void eat() {
        System.out.println(name + " is eating.");
    }
}

public class Dog extends Animal {
    @Override
    void eat() {
        super.eat();                                   // ① do what the parent does
        System.out.println(name + " wags its tail! 🐕");  // ② then add something
    }
}
```

```java
Dog rex = new Dog();
rex.name = "Rex";
rex.eat();
```

**Output:**

```
Rex is eating.
Rex wags its tail! 🐕
```

| Code | Meaning |
|---|---|
| `super.eat()` | "Call **my parent's** `eat()` method." |

### `super(...)` — call the parent's constructor

This is **very** important. Let's give `Animal` a proper constructor and private fields (Chapters 19 & 21):

```java
public class Animal {
    private String name;
    private int age;

    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() { return name; }
    public int getAge()     { return age; }
}
```

Now the child **must** call the parent's constructor:

```java
public class Dog extends Animal {
    private String breed;

    public Dog(String name, int age, String breed) {
        super(name, age);       // ① let the PARENT set up its part
        this.breed = breed;     // ② then set up MY part
    }

    public String getBreed() { return breed; }

    @Override
    public String toString() {
        return getName() + " (" + breed + ", " + getAge() + " years)";
    }
}
```

```java
Dog rex = new Dog("Rex", 3, "Labrador");
System.out.println(rex);   // Rex (Labrador, 3 years)
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `super(name, age);` | "Parent, please run **your** constructor with these values." The parent sets `name` and `age`. |
| `this.breed = breed;` | Then the child sets its **own** field. |
| `getName()` | The child can't use `name` directly (it's `private` in Animal!). So it uses the **getter**. |

### 🏗️ Why must the parent go first?

📖 **Story:** Building a house 🏠. You can't paint the walls (child) before the foundation is built (parent)! The parent part of the object must be ready **first**.

```
 new Dog("Rex", 3, "Labrador")
   │
   ├─ 1. Dog constructor starts
   ├─ 2. super(name, age) → Animal constructor runs → name, age are set
   ├─ 3. back in Dog: this.breed = "Labrador"
   └─ 4. done! ✅
```

> ⚠️ **Rules:**
> - `super(...)` must be the **first line** of the child's constructor.
> - If you don't write `super(...)`, Java **secretly** adds `super();` (no arguments). If the parent has no such constructor → **error**!

```java
public class Cat extends Animal {
    public Cat(String name) {
        // Java adds: super();  ← but Animal has no Animal() constructor!
        // ❌ error: constructor Animal in class Animal cannot be applied to given types
    }
}
```

**Fix:** Call the right parent constructor: `super(name, 0);`

### 🆚 `this` vs. `super`

| | `this` | `super` |
|---|---|---|
| Means | **me** (this object) | **my parent** part |
| Field / method | `this.name`, `this.eat()` | `super.eat()` |
| Constructor | `this(...)` → another constructor in **my** class | `super(...)` → my **parent's** constructor |

---

## 🛡️ Part 5: `protected` — for the family

With `private`, even **children** can't see the parent's fields. That's why we used `getName()` above.

`protected` is in the middle: **children can see it**, but strangers (other classes) can't.

```java
public class Animal {
    protected String name;     // children can use it directly

    public Animal(String name) {
        this.name = name;
    }
}

public class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }

    public void fetch() {
        System.out.println(name + " fetches! 🎾");   // ✅ allowed — protected
    }
}
```

| Modifier | The class itself | Children | Same package | Everyone |
|---|---|---|---|---|
| `private` | ✅ | ❌ | ❌ | ❌ |
| `protected` | ✅ | ✅ | ✅ | ❌ |
| `public` | ✅ | ✅ | ✅ | ✅ |

> 💡 Many programmers prefer `private` fields + `protected` or `public` **getters**. It keeps the parent in control. Both ways are common.

---

## 🌳 Part 6: Levels of inheritance

A child can have its own children! 🌳

```java
public class Animal { ... }
public class Dog extends Animal { ... }
public class Puppy extends Dog { ... }
```

```
 Object          ← every class's great-great-grandparent!
   └── Animal
         └── Dog
               └── Puppy
```

A `Puppy` gets **everything** from `Dog`, which got everything from `Animal`, which got everything from `Object`.

### ⚠️ Only ONE parent

In Java, a class can extend **only one** class:

```java
public class FlyingDog extends Dog, Bird { }   // ❌ error — only one parent allowed!
```

This avoids confusion: "If both parents have `move()`, which one should I use?" 🤔
(But a class **can** implement many **interfaces** — Chapter 25. That's Java's solution.)

---

## 🧪 Part 7: The "is-a" test — when to use inheritance

Inheritance is powerful, but **don't use it everywhere**. Use this test:

> Can you say "**A [child] is a [parent]**" and it sounds true?

| Sentence | True? | Inheritance? |
|---|---|---|
| A Dog **is an** Animal | ✅ yes | ✅ `Dog extends Animal` |
| A Car **is a** Vehicle | ✅ yes | ✅ `Car extends Vehicle` |
| A Manager **is an** Employee | ✅ yes | ✅ `Manager extends Employee` |
| A Car **is an** Engine | ❌ no! A car **has an** engine | ❌ use a **field** |
| A Student **is a** School | ❌ no! A school **has** students | ❌ use a field (array/list) |

### "is-a" vs. "has-a"

```java
// ✅ "is-a" → inheritance
public class Car extends Vehicle { }

// ✅ "has-a" → a field (this is called COMPOSITION)
public class Car extends Vehicle {
    private Engine engine;     // a car HAS an engine
    private Wheel[] wheels;    // a car HAS wheels
}
```

👉 **Tip:** Many experienced programmers say: "**Prefer has-a over is-a**" (composition over inheritance). Use inheritance only when "is-a" is **really** true. When in doubt, use a field.

> 🌱 **Spring Boot note:** In Spring Boot you'll use **composition** (has-a) much more than inheritance. A `StudentService` **has a** `StudentRepository`. You'll see this in Chapter 53 (Dependency Injection).

---

## 🚫 Part 8: `final` — no children, no changes

### A `final` class can't have children

```java
public final class Money { ... }

public class FakeMoney extends Money { }   // ❌ error: cannot inherit from final Money
```

Used for classes that must **never** be changed by a child — like `String` (it's `final`!).

### A `final` method can't be overridden

```java
public class Bank {
    public final double calculateInterest() { ... }
}

public class MyBank extends Bank {
    @Override
    public double calculateInterest() { ... }   // ❌ error: cannot override; overridden method is final
}
```

Used when the parent says: "This rule is **important**. Children may not change it." 🔒

### Summary of `final`

| `final` on... | Means |
|---|---|
| a variable | can't be **reassigned** (Chapter 6) |
| a method | can't be **overridden** |
| a class | can't be **extended** (no children) |

---

## 💻 Mini project: Employees and salaries 💼

**File: `Employee.java`**

```java
public class Employee {
    private final String name;
    private final double baseSalary;

    public Employee(String name, double baseSalary) {
        this.name = name;
        this.baseSalary = baseSalary;
    }

    public String getName()       { return name; }
    public double getBaseSalary() { return baseSalary; }

    public double calculatePay() {
        return baseSalary;
    }

    public String getRole() {
        return "Employee";
    }

    @Override
    public String toString() {
        return String.format("%-8s %-10s %10.2f", getRole(), name, calculatePay());
    }
}
```

**File: `Manager.java`**

```java
public class Manager extends Employee {
    private final double bonus;

    public Manager(String name, double baseSalary, double bonus) {
        super(name, baseSalary);
        this.bonus = bonus;
    }

    @Override
    public double calculatePay() {
        return super.calculatePay() + bonus;
    }

    @Override
    public String getRole() {
        return "Manager";
    }
}
```

**File: `Intern.java`**

```java
public class Intern extends Employee {
    public Intern(String name, double baseSalary) {
        super(name, baseSalary);
    }

    @Override
    public double calculatePay() {
        return super.calculatePay() * 0.5;   // interns work half-time
    }

    @Override
    public String getRole() {
        return "Intern";
    }
}
```

**File: `Payroll.java`**

```java
public class Payroll {
    public static void main(String[] args) {
        Employee sara = new Employee("Sara", 3000);
        Manager tom = new Manager("Tom", 4000, 1500);
        Intern lina = new Intern("Lina", 2000);

        System.out.println(sara);
        System.out.println(tom);
        System.out.println(lina);

        double total = sara.calculatePay() + tom.calculatePay() + lina.calculatePay();
        System.out.printf("Total payroll: %.2f%n", total);
    }
}
```

**Output:**

```
Employee Sara          3000.00
Manager  Tom           5500.00
Intern   Lina          1000.00
Total payroll: 9500.00
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `extends Employee` | Manager and Intern **are** Employees. They get `name`, `baseSalary`, getters, `toString()`. |
| `super(name, baseSalary)` | Let the parent set up its fields first. |
| `super.calculatePay() + bonus` | Use the parent's calculation, then **add** the bonus. |
| `toString()` is only in `Employee` | But it calls `getRole()` and `calculatePay()` — and for a Manager, Java uses **Manager's** versions! 🤯 That's **polymorphism** — next chapter! |

---

## ✋ Try it yourself

**Task 1:** Make a parent class `Vehicle` with `brand` and `speed`, and a method `describe()`. Make two children: `Car` (adds `doors`) and `Bicycle` (adds `hasBell`). Each child should override `describe()` and use `super.describe()`.

<details>
<summary>Click to see one possible answer</summary>

```java
public class Vehicle {
    protected String brand;
    protected int speed;

    public Vehicle(String brand, int speed) {
        this.brand = brand;
        this.speed = speed;
    }

    public void describe() {
        System.out.print(brand + " at " + speed + " km/h");
    }
}

public class Car extends Vehicle {
    private int doors;

    public Car(String brand, int speed, int doors) {
        super(brand, speed);
        this.doors = doors;
    }

    @Override
    public void describe() {
        super.describe();
        System.out.println(", " + doors + " doors 🚗");
    }
}

public class Bicycle extends Vehicle {
    private boolean hasBell;

    public Bicycle(String brand, int speed, boolean hasBell) {
        super(brand, speed);
        this.hasBell = hasBell;
    }

    @Override
    public void describe() {
        super.describe();
        System.out.println(hasBell ? ", ring ring! 🚲🔔" : ", no bell 🚲");
    }
}
```

</details>

**Task 2:** Use the "is-a" test. Which should use inheritance?
1. `Square` and `Shape`
2. `Library` and `Book`
3. `Teacher` and `Person`
4. `Computer` and `Keyboard`

<details>
<summary>Click to see the answer</summary>

1. ✅ A Square **is a** Shape → `Square extends Shape`
2. ❌ A Library **has** Books → field
3. ✅ A Teacher **is a** Person → `Teacher extends Person`
4. ❌ A Computer **has a** Keyboard → field

</details>

**Task 3:** Find the error and fix it:

```java
public class Person {
    private String name;
    public Person(String name) { this.name = name; }
}

public class Student extends Person {
    private int grade;
    public Student(String name, int grade) {
        this.grade = grade;
    }
}
```

<details>
<summary>Click to see the answer</summary>

`Student`'s constructor doesn't call `super(name)`. Java adds `super()` automatically, but `Person` has no empty constructor → error.

```java
public Student(String name, int grade) {
    super(name);
    this.grade = grade;
}
```

</details>

**Task 4:** Add a `Director` class that extends `Manager` (3 levels!). A director gets the manager's pay **plus** 10% extra.

**Task 5:** Make a `Shape` parent with a method `double area()` that returns 0. Make `Circle`, `Rectangle` and `Triangle` children that override `area()`.

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `super(...)` when the parent has no empty constructor

See Task 3. **Fix:** Call `super(...)` with the right arguments, on the **first line**.

### Mistake 2: Accessing a `private` parent field from the child

```java
public class Dog extends Animal {
    void show() {
        System.out.println(name);   // ❌ error: name has private access in Animal
    }
}
```

**Fix:** Use the getter `getName()`, or make the field `protected`.

### Mistake 3: Typo when overriding (without `@Override`)

```java
public class Dog extends Animal {
    void makesound() { ... }   // small 's' → a NEW method, not an override! 🐛
}
```

**Fix:** Always write `@Override`. Then Java says: `method does not override or implement a method from a supertype`.

### Mistake 4: Making the override "more private"

```java
public class Animal {
    public void eat() { }
}
public class Dog extends Animal {
    @Override
    void eat() { }   // ❌ error: attempting to assign weaker access privileges; was public
}
```

A child can't make a method **less** visible than the parent did.

### Mistake 5: Extending two classes

```java
class A extends B, C { }   // ❌ only one parent
```

### Mistake 6: Using inheritance for "has-a"

```java
public class Car extends Engine { }   // ❌ a car is NOT an engine
```

**Fix:** `private Engine engine;` inside `Car`.

---

## ✅ Summary

- **Inheritance**: a child class **gets** all the fields and methods of its parent. Write common code **once**.
- `class Child extends Parent` — "Child **is a** Parent".
- The child can **add** new fields and methods.
- The child can **override** a parent's method (same name, same parameters). Always use **`@Override`**.
- `super.method()` → call the parent's version. `super(...)` → call the parent's constructor (**first line**!).
- `protected` → visible to children (and the package).
- Java allows only **one** parent class. Every class's top ancestor is **`Object`**.
- Use the **"is-a"** test. For "has-a", use a **field** (composition). Prefer composition when in doubt.
- `final` class → no children. `final` method → can't be overridden.

---

## ❓ Quiz

1. What keyword makes a class a child of another class?
2. What does a child class get from its parent?
3. What is the difference between overriding and overloading?
4. What does `super(name)` do? Where must it be written?
5. What does `super.eat()` do?
6. Can a class extend two classes?
7. "A Car has an Engine." Should `Car` extend `Engine`?
8. What does `final` mean on a class? On a method?
9. Who can see a `protected` field?

<details>
<summary>Click to see the answers</summary>

1. `extends`
2. All its fields and methods (but `private` ones can't be used **directly** — only through public/protected methods).
3. Overriding: a child replaces a parent's method (same name, same parameters). Overloading: same name, **different** parameters, in the same class.
4. It calls the parent's constructor with `name`. It must be the **first line** of the child's constructor.
5. It calls the **parent's** version of `eat()`.
6. No, only one.
7. No — "has-a" means use a field: `private Engine engine;`
8. Class: it can't have children. Method: it can't be overridden.
9. The class itself, its children, and classes in the same package.

</details>

---

[⬅ Previous chapter](21-encapsulation.md) | [Table of Contents](../README.md) | [Next chapter: Polymorphism ➡](23-polymorphism.md)
