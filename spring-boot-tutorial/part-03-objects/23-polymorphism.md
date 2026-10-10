# Chapter 23 – Polymorphism: One Name, Many Shapes

[⬅ Previous chapter](22-inheritance.md) | [Table of Contents](../README.md) | [Next chapter ➡](24-abstract-classes.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What **polymorphism** means (it's a big word for a simple idea!)
- How a **parent-type variable** can hold a **child object**: `Animal a = new Dog();`
- How Java chooses **which method** to run (the child's version!)
- How to treat **many different objects the same way** (arrays and methods)
- How to check the real type with **`instanceof`**
- How to **cast** safely, and **pattern matching** (`instanceof Dog d`)
- Why polymorphism is **the secret** behind Spring Boot

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Polymorphism** | *Poly* = many, *morph* = shape. **One** variable type, **many** possible object types. Same method call, **different** behavior. |
| **Declared type** | The type you **write** for the variable: `Animal a` → `Animal`. |
| **Actual type** | The type of the **real object**: `new Dog()` → `Dog`. |
| **Upcasting** | Treating a child as its parent: `Animal a = new Dog();` Always safe. ⬆️ |
| **Downcasting** | Treating a parent variable as a child: `Dog d = (Dog) a;` Can be dangerous. ⬇️ |
| **`instanceof`** | A check: "Is this object really a ...?" |
| **Dynamic dispatch** | Java chooses the method version at **run time**, based on the **actual** object. |

---

## 📖 Story: The universal remote 📺

You have **one** remote control with a **power button** 🔴.

- Point it at the **TV** → the TV turns on. 📺
- Point it at the **air conditioner** → the AC turns on. ❄️
- Point it at the **radio** → the radio turns on. 📻

**One button**. The same action: "power on". But **each device** does it in **its own way**.

You don't need a different button for each device. You don't even need to know **how** each device turns on inside. You just press "power". 🔴

**That's polymorphism:** one method call (`makeSound()`), many different behaviors (Woof, Meow, Tweet), depending on the **real object**.

---

## ⬆️ Part 1: A parent variable can hold a child object

In Chapter 22 we wrote:

```java
Dog rex = new Dog("Rex");
```

But because a Dog **is an** Animal, this is **also** allowed:

```java
Animal rex = new Dog("Rex");
```

| Part | Type |
|---|---|
| `Animal rex` | **Declared type** = `Animal` (the type of the **variable**) |
| `new Dog("Rex")` | **Actual type** = `Dog` (the type of the **real object**) |

📦 **Story:** You put a dog 🐕 into a box with the label "**Animal**". That's true — a dog **is** an animal! The label is more general, but what's **inside** is still a dog.

The opposite is **not** allowed:

```java
Dog d = new Animal("???");   // ❌ error: incompatible types: Animal cannot be converted to Dog
```

Not every animal is a dog! (Maybe it's a fish 🐟.)

---

## 🎭 Part 2: Which method runs?

Here are our classes:

```java
public class Animal {
    protected String name;

    public Animal(String name) {
        this.name = name;
    }

    public void makeSound() {
        System.out.println(name + " makes a sound.");
    }
}

public class Dog extends Animal {
    public Dog(String name) { super(name); }

    @Override
    public void makeSound() {
        System.out.println(name + " says Woof! 🐕");
    }

    public void fetch() {
        System.out.println(name + " fetches the ball! 🎾");
    }
}

public class Cat extends Animal {
    public Cat(String name) { super(name); }

    @Override
    public void makeSound() {
        System.out.println(name + " says Meow! 🐈");
    }
}
```

Now the magic:

```java
Animal a = new Dog("Rex");
a.makeSound();
```

**Output:**

```
Rex says Woof! 🐕
```

😮 The variable is `Animal`, but Java runs **Dog's** `makeSound()`!

### 🧠 The two rules (very important!)

| Question | Who decides? | Example |
|---|---|---|
| **Which methods am I allowed to call?** | The **declared type** (the label on the box) — checked when you **compile**. | `a` is `Animal` → you can call `makeSound()`, but **not** `fetch()`. |
| **Which version of the method runs?** | The **actual object** (what's really in the box) — decided when the program **runs**. | The object is a Dog → **Dog's** `makeSound()` runs. |

```java
Animal a = new Dog("Rex");

a.makeSound();   // ✅ allowed (Animal has makeSound) → runs DOG's version
a.fetch();       // ❌ error: cannot find symbol — Animal doesn't have fetch()
```

📺 **Remote story again:** The remote (variable type) decides **which buttons exist**. The device (the object) decides **what happens** when you press a button.

This is called **dynamic dispatch** (Java "dispatches" — sends — the call to the right version at run time).

---

## 🎪 Part 3: The real power — treating many objects the same way

### An array of different animals

```java
Animal[] zoo = {
    new Dog("Rex"),
    new Cat("Tom"),
    new Dog("Bella"),
    new Cat("Luna")
};

for (Animal animal : zoo) {
    animal.makeSound();
}
```

**Output:**

```
Rex says Woof! 🐕
Tom says Meow! 🐈
Bella says Woof! 🐕
Luna says Meow! 🐈
```

🤯 **One** loop. **One** method call. But each animal does **its own** thing! We didn't write a single `if`!

### Without polymorphism, it would look like this 😩

```java
for (...) {
    if (it's a dog) {
        dog.bark();
    } else if (it's a cat) {
        cat.meow();
    } else if (it's a bird) {
        bird.tweet();
    } else if ...   // and every new animal needs a new "else if"!
}
```

### ✨ Adding a new animal

```java
public class Cow extends Animal {
    public Cow(String name) { super(name); }

    @Override
    public void makeSound() {
        System.out.println(name + " says Moo! 🐄");
    }
}
```

Add `new Cow("Daisy")` to the zoo array → it works! The loop **didn't change at all**. 🎉

👉 **This is the big idea:** You can add **new** types **without changing** the old code. Programmers call this the **Open/Closed Principle**: "open for extension, closed for modification".

### A method that accepts any animal

```java
public static void feedAndListen(Animal animal) {
    System.out.println("Feeding " + animal.name + "...");
    animal.makeSound();
}
```

```java
feedAndListen(new Dog("Rex"));    // works with a Dog
feedAndListen(new Cat("Tom"));    // works with a Cat
feedAndListen(new Cow("Daisy"));  // works with a Cow — and with any future animal!
```

**Output:**

```
Feeding Rex...
Rex says Woof! 🐕
Feeding Tom...
Tom says Meow! 🐈
Feeding Daisy...
Daisy says Moo! 🐄
```

The method asks for an `Animal`. You can give it **any** child of Animal. ✅

---

## 🔍 Part 4: `instanceof` — what is it really?

Sometimes you need to know the **real** type, to call a child-only method like `fetch()`.

```java
Animal a = new Dog("Rex");

System.out.println(a instanceof Dog);      // true
System.out.println(a instanceof Animal);   // true (a Dog is also an Animal)
System.out.println(a instanceof Cat);      // false
```

| Code | Question |
|---|---|
| `a instanceof Dog` | "Is the object in `a` really a Dog (or a child of Dog)?" |

### ⬇️ Downcasting — treat it as the child type

```java
Animal a = new Dog("Rex");

if (a instanceof Dog) {
    Dog d = (Dog) a;    // cast: "I know it's a Dog, treat it as one"
    d.fetch();          // ✅ now we can call Dog methods
}
```

| Part | Meaning |
|---|---|
| `(Dog) a` | **Cast**: "Look at `a` as a `Dog`." Like taking the dog out of the "Animal" box and putting it in a "Dog" box. |

### 💥 Casting the wrong type

```java
Animal a = new Cat("Tom");
Dog d = (Dog) a;   // 💥 ClassCastException: class Cat cannot be cast to class Dog
```

Java checks at run time. A cat is not a dog → crash! That's why we **always** check with `instanceof` first.

### ✨ Pattern matching (modern Java — use this!)

Since Java 16, you can check **and** cast in **one** step:

```java
if (a instanceof Dog d) {
    d.fetch();
}
```

| Part | Meaning |
|---|---|
| `a instanceof Dog d` | "If `a` is a Dog, **also** make a variable `d` of type Dog that points to it." |

Shorter and safer. 😎

### Example: only dogs fetch

```java
for (Animal animal : zoo) {
    animal.makeSound();
    if (animal instanceof Dog dog) {
        dog.fetch();
    }
}
```

**Output:**

```
Rex says Woof! 🐕
Rex fetches the ball! 🎾
Tom says Meow! 🐈
Bella says Woof! 🐕
Bella fetches the ball! 🎾
Luna says Meow! 🐈
```

> ⚠️ **Don't overuse `instanceof`.** If you write many `instanceof` checks, it's often a sign that the method should be in the parent class and **overridden** instead. Let polymorphism do the work! 💪

### `switch` with types (Java 21+)

```java
String describe(Animal animal) {
    return switch (animal) {
        case Dog d -> d.name + " is a loyal dog";
        case Cat c -> c.name + " is an independent cat";
        default    -> animal.name + " is some animal";
    };
}
```

A switch can check the **type** and give you a variable in one step. Nice for later! 🎁

---

## ⬆️⬇️ Part 5: Upcasting and downcasting — summary

```
          Animal          ▲  UPCASTING (child → parent)
            │             │  Always safe. Automatic.
          ┌─┴─┐           │  Animal a = new Dog("Rex");
         Dog  Cat
                          ▼  DOWNCASTING (parent → child)
                             Can fail! Check with instanceof.
                             if (a instanceof Dog d) { ... }
```

| | Upcasting ⬆️ | Downcasting ⬇️ |
|---|---|---|
| Direction | child → parent | parent → child |
| Safe? | ✅ always | ⚠️ only if the object really is that child |
| Need to write a cast? | no | yes `(Dog) a` — or use pattern matching |
| Example | `Animal a = dog;` | `Dog d = (Dog) a;` |

---

## 🧩 Part 6: Polymorphism with `Object`

Remember: every class is a child of `Object`. So an `Object` variable can hold **anything**:

```java
Object[] things = { "hello", 42, 3.14, new Dog("Rex"), true };

for (Object thing : things) {
    System.out.println(thing.toString());
}
```

**Output (Dog has no toString here):**

```
hello
42
3.14
Dog@5ca881b5
true
```

Each object uses **its own** `toString()`. That's polymorphism too! And it's exactly how `System.out.println(anything)` works — `println(Object x)` just calls `x.toString()`, and each class answers in its own way. 🖨️

> 💡 Wait — `42` and `true` are primitives (`int`, `boolean`), not objects! Java **automatically** wraps them into objects (`Integer`, `Boolean`). This is called **autoboxing**. We learn more in Chapter 30.

---

## 💻 Mini project: Shapes 🔷

**File: `Shape.java`**

```java
public class Shape {
    protected String name;

    public Shape(String name) {
        this.name = name;
    }

    public double area() {
        return 0;
    }

    public double perimeter() {
        return 0;
    }

    @Override
    public String toString() {
        return String.format("%-10s area=%7.2f  perimeter=%6.2f", name, area(), perimeter());
    }
}
```

**File: `Circle.java`**

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

**File: `Rectangle.java`**

```java
public class Rectangle extends Shape {
    private final double width;
    private final double height;

    public Rectangle(double width, double height) {
        super("Rectangle");
        this.width = width;
        this.height = height;
    }

    @Override
    public double area() {
        return width * height;
    }

    @Override
    public double perimeter() {
        return 2 * (width + height);
    }
}
```

**File: `Square.java`**

```java
public class Square extends Rectangle {
    public Square(double side) {
        super(side, side);
        this.name = "Square";
    }
}
```

**File: `ShapeDemo.java`**

```java
public class ShapeDemo {
    public static void main(String[] args) {
        Shape[] shapes = {
            new Circle(1),
            new Rectangle(3, 4),
            new Square(2),
            new Circle(2.5)
        };

        double totalArea = 0;
        Shape biggest = shapes[0];

        for (Shape shape : shapes) {
            System.out.println(shape);
            totalArea += shape.area();
            if (shape.area() > biggest.area()) {
                biggest = shape;
            }
        }

        System.out.printf("Total area: %.2f%n", totalArea);
        System.out.println("Biggest: " + biggest.name);
    }
}
```

**Output:**

```
Circle     area=   3.14  perimeter=  6.28
Rectangle  area=  12.00  perimeter= 14.00
Square     area=   4.00  perimeter=  8.00
Circle     area=  19.63  perimeter= 15.71
Total area: 38.78
Biggest: Circle
```

### 🔍 Where is the polymorphism?

| Code | What happens |
|---|---|
| `Shape[] shapes = { new Circle(1), ... }` | Upcasting: different shapes in **one** array. |
| `System.out.println(shape)` | Calls `toString()` from `Shape` — which calls `area()` and `perimeter()` → **each child's own version** runs! |
| `shape.area()` | Circle uses π·r², Rectangle uses w·h. Same call, different math. |
| `Square extends Rectangle` | A Square **is a** Rectangle. It **inherits** `area()` and `perimeter()` — no need to write them again! |

> 🤔 Notice: `Shape.area()` returns `0`. That's a bit strange — what is the area of "a shape"? It doesn't make sense to create a plain `new Shape("?")`. In the **next chapter**, **abstract classes** fix this! 🎯

---

## 🌱 Part 7: Why polymorphism matters for Spring Boot

In Spring Boot, you'll often write code like this:

```java
private final PaymentService paymentService;   // the TYPE is general

public void checkout(Order order) {
    paymentService.pay(order.getTotal());       // ONE call
}
```

And somewhere else, Spring decides **which real object** goes into `paymentService`:
- in development: a **fake** payment service (no real money! 💸❌)
- in production: a **real** credit card service 💳
- in tests: a **mock** service (Chapter 85)

The `checkout` code **never changes**. Just like our zoo loop. 🦁

This works with **interfaces** (Chapter 25), which are the next level of polymorphism. You're getting closer to Spring Boot! 🚀

---

## ✋ Try it yourself

**Task 1:** What does this print? Think first!

```java
Animal a = new Cat("Kitty");
a.makeSound();
System.out.println(a instanceof Animal);
System.out.println(a instanceof Dog);
```

<details>
<summary>Click to see the answer</summary>

```
Kitty says Meow! 🐈
true
false
```

</details>

**Task 2:** Which lines give a **compile error**? Which give a **run-time crash**?

```java
Animal a = new Dog("Rex");
Dog d1 = a;              // line 2
Dog d2 = (Dog) a;        // line 3
a.fetch();               // line 4
Cat c = (Cat) a;         // line 5
```

<details>
<summary>Click to see the answer</summary>

- Line 2: **compile error** — Animal can't be put into Dog without a cast.
- Line 3: ✅ OK — the object really is a Dog.
- Line 4: **compile error** — Animal has no `fetch()`.
- Line 5: compiles, but **crashes** at run time: `ClassCastException` (it's a Dog, not a Cat).

</details>

**Task 3:** Use your `Employee`, `Manager` and `Intern` classes from Chapter 22. Put them all in **one** `Employee[]` array. Use a loop to calculate the total pay. Use `instanceof` to count how many managers there are.

**Task 4:** Add a `Triangle` class (base, height, and 3 sides) to the Shapes project. Add it to the array. Did you need to change `ShapeDemo`'s loop?

<details>
<summary>Click to see the answer</summary>

```java
public class Triangle extends Shape {
    private final double base, height, sideA, sideB, sideC;

    public Triangle(double base, double height, double sideA, double sideB, double sideC) {
        super("Triangle");
        this.base = base;
        this.height = height;
        this.sideA = sideA;
        this.sideB = sideB;
        this.sideC = sideC;
    }

    @Override
    public double area() {
        return base * height / 2;
    }

    @Override
    public double perimeter() {
        return sideA + sideB + sideC;
    }
}
```

No! The loop didn't change. Just add `new Triangle(3, 4, 3, 4, 5)` to the array. 🎉

</details>

**Task 5:** Make a class `Notification` with a method `send(String message)`. Make children `EmailNotification`, `SmsNotification` and `PushNotification` that each print the message differently (📧, 📱, 🔔). Write a method `notifyAll(Notification[] list, String msg)`.

---

## ⚠️ Common mistakes

### Mistake 1: Calling a child method on a parent variable

```java
Animal a = new Dog("Rex");
a.fetch();   // ❌ error: cannot find symbol
```

**Fix:** `if (a instanceof Dog d) { d.fetch(); }` — or, if all animals should have it, put it in `Animal`.

### Mistake 2: Casting without checking

```java
Dog d = (Dog) someAnimal;   // 💥 ClassCastException if it's not a Dog
```

**Fix:** Check with `instanceof` first (pattern matching).

### Mistake 3: Thinking the declared type decides the method version

```java
Animal a = new Dog("Rex");
a.makeSound();   // Many beginners expect "Rex makes a sound." — but it's "Rex says Woof!"
```

The **object** decides the version. Always.

### Mistake 4: Too many `instanceof` checks

```java
if (s instanceof Circle) { ... } else if (s instanceof Square) { ... } else if ...
```

**Fix:** Put a method in the parent and override it in each child. Let polymorphism choose. 🎯

### Mistake 5: Fields are NOT polymorphic

```java
public class Animal { String sound = "..."; }
public class Dog extends Animal { String sound = "Woof"; }   // ⚠️ a NEW field, hides the parent's

Animal a = new Dog();
System.out.println(a.sound);   // "..." 😮 — fields use the DECLARED type!
```

Only **methods** are polymorphic. **Fix:** Use methods (getters), not public fields. Another reason for encapsulation (Chapter 21)!

### Mistake 6: Static methods are NOT polymorphic

`static` methods belong to the class, not the object — they don't get overridden. (Chapter 27.)

---

## ✅ Summary

- **Polymorphism** = one method call, many behaviors. 📺🔴
- A **parent variable** can hold a **child object**: `Animal a = new Dog();` (upcasting ⬆️, always safe).
- The **declared type** decides **which methods you may call**.
- The **actual object** decides **which version runs** (dynamic dispatch).
- Put different objects in **one array** of the parent type, and treat them **the same way**.
- Methods with a **parent-type parameter** accept **any child**.
- Add new child classes **without changing** old code. 🎉
- `instanceof` checks the real type. Use **pattern matching**: `if (a instanceof Dog d) { d.fetch(); }`
- Downcasting `(Dog) a` can **crash** (`ClassCastException`) — check first!
- Only **methods** are polymorphic — not fields, not static methods.

---

## ❓ Quiz

1. What does "polymorphism" mean?
2. Is `Animal a = new Dog();` allowed? Is `Dog d = new Animal();` allowed?
3. `Animal a = new Dog(); a.makeSound();` — whose `makeSound()` runs?
4. `Animal a = new Dog(); a.fetch();` — what happens? (Dog has `fetch()`, Animal doesn't.)
5. What does `instanceof` do?
6. What happens here? `Animal a = new Dog("Rex"); Cat c = (Cat) a;`
7. Write the modern one-line way to check if `a` is a Dog and call `fetch()`.
8. Why is polymorphism useful when you add a new class?

<details>
<summary>Click to see the answers</summary>

1. "Many shapes": the same method call can do different things, depending on the real object.
2. Yes. No.
3. **Dog's** version (the actual object decides).
4. Compile error — the declared type `Animal` has no `fetch()` method.
5. It checks if an object is really of a certain type (or a child of it). Returns `true`/`false`.
6. It compiles, but crashes at run time with `ClassCastException`.
7. `if (a instanceof Dog d) { d.fetch(); }`
8. Because code that works with the parent type (loops, methods) works with the new class **without any changes**.

</details>

---

[⬅ Previous chapter](22-inheritance.md) | [Table of Contents](../README.md) | [Next chapter: Abstract classes ➡](24-abstract-classes.md)
