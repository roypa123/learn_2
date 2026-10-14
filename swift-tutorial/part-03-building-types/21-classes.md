# Chapter 21 — Classes

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What a **class** is.
- How classes are **different** from structs.
- Classes **must** have an `init`.
- **Inheritance**: one class built on another.
- `override` and `super`.
- `final`.
- `deinit`.

---

## 1. A class looks like a struct

```swift
class Dog {
    var name: String
    var age: Int

    init(name: String, age: Int) {
        self.name = name
        self.age = age
    }

    func bark() {
        print("\(name) says Woof! 🐶")
    }
}

let bruno = Dog(name: "Bruno", age: 3)
bruno.bark()
```

**Output:**

```
Bruno says Woof! 🐶
```

| Part | Meaning |
|---|---|
| `class Dog` | "I'm making a new type called `Dog`." Like `struct`, but with the word `class`. |
| `var name`, `var age` | Properties — same as in a struct. |
| `init(name:age:)` | The initializer. **Classes need this** (see below). |
| `func bark()` | A method — same as in a struct. |

> 📖 **New word: Class**
> Another way to make your own type. Similar to a struct, but with some important differences.

> 📖 **New word: Object**
> An instance of a class is often called an **object**. `bruno` is an object.

---

## 2. Difference 1: classes need an `init`

Structs get an automatic `init`. Classes **don't**.

```swift
class Cat {
    var name: String
}
```

**Error:**

```
error: class 'Cat' has no initializers
```

Fix: either give default values…

```swift
class Cat {
    var name: String = "Kitty"
}
let c = Cat()
```

…or write an `init`:

```swift
class Cat {
    var name: String
    init(name: String) {
        self.name = name
    }
}
let c = Cat(name: "Tom")
```

---

## 3. Difference 2: classes are shared, not copied ⭐

This is the **biggest** difference. Read carefully!

```swift
class Box {
    var value: Int
    init(value: Int) {
        self.value = value
    }
}

let a = Box(value: 1)
let b = a           // NOT a copy! Same box!
b.value = 100

print(a.value)
print(b.value)
```

**Output:**

```
100
100
```

😮 Both changed! Why?

| Line | What happens |
|---|---|
| `let a = Box(value: 1)` | Make **one** box. `a` points to it. |
| `let b = a` | `b` points to the **same** box. No copy is made. |
| `b.value = 100` | Change the box. |
| `a.value` | `a` points to the same box → 100. |

```
 Struct (copy):                 Class (shared):

  a ──► [ 1 ]                    a ──┐
  b ──► [ 100 ]                      ├──► [ 100 ]
                                 b ──┘
```

Think of it like this:
- **Struct** = a **photocopy** 📄📄. Two separate papers.
- **Class** = a **shared Google Doc** 🌐. Two people, one document. If one edits, the other sees it.

> 📖 **New word: Reference type**
> A type where variables **point to the same** object instead of copying. Classes are reference types.

> 📖 **New word: Reference**
> A pointer, like an address 🏠. Many people can have the same address and visit the same house.

---

## 4. Difference 3: `let` doesn't freeze a class

```swift
let myBox = Box(value: 1)
myBox.value = 5     // ✅ Allowed with a class!
print(myBox.value)
```

**Output:**

```
5
```

With a class, `let` only means: *"`myBox` will always point to **this same** box."*
But the **inside** of the box can still change (if the properties are `var`).

```swift
myBox = Box(value: 9)   // ❌ ERROR: can't point to a different box
```

| | Struct with `let` | Class with `let` |
|---|---|---|
| Change a `var` property? | ❌ No | ✅ Yes |
| Point to a new instance? | ❌ No | ❌ No |

Also: class methods **don't need** `mutating`.

---

## 5. Checking if two variables are the same object: `===`

```swift
let x = Box(value: 1)
let y = x
let z = Box(value: 1)

print(x === y)
print(x === z)
```

**Output:**

```
true
false
```

| Operator | Meaning |
|---|---|
| `===` | "Are these the **same object**?" (same house) |

`x` and `z` have the same value inside, but they are **two different boxes**.

---

## 6. Inheritance: building on another class

Classes can **inherit** from another class. The new class gets **everything** the old one has — and can add more.

> 📖 **New word: Inheritance**
> When a class takes all the properties and methods of another class.

Think of family 👨‍👦: a child inherits things from a parent (like eye color), but also has their own things.

```swift
class Animal {
    var name: String

    init(name: String) {
        self.name = name
    }

    func eat() {
        print("\(name) is eating.")
    }
}

class Bird: Animal {
    func fly() {
        print("\(name) is flying! 🐦")
    }
}

let tweety = Bird(name: "Tweety")
tweety.eat()
tweety.fly()
```

**Output:**

```
Tweety is eating.
Tweety is flying! 🐦
```

| Part | Meaning |
|---|---|
| `class Animal` | The **parent** class (also called **superclass**). |
| `class Bird: Animal` | `Bird` **inherits from** `Animal`. The `:` means "is a kind of". |
| `tweety.eat()` | `Bird` didn't write `eat()`, but it **inherited** it! |
| `tweety.fly()` | `Bird`'s own new method. |

> 📖 **New word: Superclass / Subclass**
> **Superclass** = the parent (`Animal`). **Subclass** = the child (`Bird`).

```
      Animal          ← superclass
     /      \
   Bird     Fish      ← subclasses
```

⚠️ **Careful:** Structs **cannot** inherit. Only classes can.

---

## 7. `override`: changing an inherited method

```swift
class Animal {
    func makeSound() {
        print("Some sound...")
    }
}

class Cow: Animal {
    override func makeSound() {
        print("Moo! 🐄")
    }
}

class Cat: Animal {
    override func makeSound() {
        print("Meow! 🐱")
    }
}

let animals: [Animal] = [Animal(), Cow(), Cat()]

for a in animals {
    a.makeSound()
}
```

**Output:**

```
Some sound...
Moo! 🐄
Meow! 🐱
```

| Part | Meaning |
|---|---|
| `override func makeSound()` | "Replace the parent's version with my own." |
| `[Animal]` | An array of animals. A `Cow` **is an** `Animal`, so it fits. |
| `a.makeSound()` | Each animal uses **its own** version! |

⚠️ **Careful:** If you forget `override`, Swift gives an error: `overriding declaration requires an 'override' keyword`.

> 📖 **New word: Override**
> To replace a parent's method with a new version in the child class.

---

## 8. `super`: using the parent's version too

```swift
class Animal {
    func describe() {
        print("I am an animal.")
    }
}

class Dog: Animal {
    override func describe() {
        super.describe()
        print("I am also a dog. 🐶")
    }
}

Dog().describe()
```

**Output:**

```
I am an animal.
I am also a dog. 🐶
```

| Part | Meaning |
|---|---|
| `super.describe()` | "First, run the **parent's** version." |
| Then | Add the child's extra lines. |

---

## 9. `init` with inheritance

When a subclass adds new properties, it needs its own `init` and must call `super.init`.

```swift
class Animal {
    var name: String
    init(name: String) {
        self.name = name
    }
}

class Pet: Animal {
    var owner: String

    init(name: String, owner: String) {
        self.owner = owner           // 1. set MY properties first
        super.init(name: name)       // 2. then let the parent set its properties
    }
}

let p = Pet(name: "Bruno", owner: "Ravi")
print("\(p.name) belongs to \(p.owner)")
```

**Output:**

```
Bruno belongs to Ravi
```

| Step | Meaning |
|---|---|
| `self.owner = owner` | The child sets its own new property **first**. |
| `super.init(name: name)` | Then call the parent's `init` to set `name`. |

🧠 **Remember the order:** your own properties **first**, then `super.init(...)`.

---

## 10. `final`: no more inheritance

```swift
final class Robot {
    var model = "R2"
}

class SuperRobot: Robot { }   // ❌ ERROR: inheritance from a final class 'Robot'
```

`final` means "nobody can inherit from this class". It also makes your code a little faster.

💡 **Tip:** Many Swift programmers write `final class` by default, and remove `final` only if they need inheritance.

---

## 11. `deinit`: when an object is destroyed

A class can run code when it is **removed from memory**.

```swift
class Balloon {
    let color: String
    init(color: String) {
        self.color = color
        print("🎈 \(color) balloon created")
    }
    deinit {
        print("💥 \(color) balloon popped")
    }
}

var b: Balloon? = Balloon(color: "Red")
b = nil
print("Done")
```

**Output:**

```
🎈 Red balloon created
💥 Red balloon popped
Done
```

| Part | Meaning |
|---|---|
| `deinit { }` | Runs when nobody uses this object anymore. |
| `b = nil` | Nobody points to the balloon now → Swift removes it → `deinit` runs. |

> 📖 **New word: deinit**
> Short for **de-initializer**. The opposite of `init`. Runs when the object is destroyed.

Swift counts how many variables point to each object. When the count reaches **0**, the object is removed. This is called **ARC** (Automatic Reference Counting). You don't usually need to think about it. 😊

---

## 12. Mini project: a shared scoreboard 🏆

Because classes are **shared**, they're great when many parts of your code need to see the **same** data.

```swift
class Scoreboard {
    var scores: [String: Int] = [:]

    func add(points: Int, to player: String) {
        scores[player, default: 0] += points
    }

    func show() {
        for (player, score) in scores.sorted(by: { $0.value > $1.value }) {
            print("\(player): \(score)")
        }
    }
}

class Referee {
    let board: Scoreboard
    init(board: Scoreboard) {
        self.board = board
    }
    func giveGoal(to player: String) {
        board.add(points: 1, to: player)
    }
}

let board = Scoreboard()
let ref1 = Referee(board: board)
let ref2 = Referee(board: board)

ref1.giveGoal(to: "Ravi")
ref2.giveGoal(to: "Meena")
ref2.giveGoal(to: "Ravi")

board.show()
```

**Output:**

```
Ravi: 2
Meena: 1
```

| Part | Meaning |
|---|---|
| `let board = Scoreboard()` | **One** scoreboard. |
| `ref1` and `ref2` | Both referees get the **same** board (a reference, not a copy). |
| `giveGoal` | Each referee updates the shared board. |
| `board.show()` | Shows all goals from both referees. |

If `Scoreboard` were a **struct**, each referee would have their **own copy**, and the main board would stay empty!

---

## 🏋️ Practice

1. Make a class `Car` with `brand: String` and `speed: Int`. Write an `init`. Add a method `accelerate()` that adds 10 to `speed`.
2. Make `let car1 = Car(...)`, then `let car2 = car1`. Call `car2.accelerate()`. Print `car1.speed`. Explain the result.
3. Make a class `Shape` with a method `describe()` that prints `"I am a shape"`. Make subclasses `Square` and `Triangle` that override it.
4. Make a class `Vehicle` with `wheels: Int`. Make a subclass `Bike` with an extra property `hasBell: Bool`. Write `Bike`'s `init` correctly with `super.init`.

<details>
<summary>Click to see the answers</summary>

```swift
// 1 & 2
class Car {
    var brand: String
    var speed: Int
    init(brand: String, speed: Int) {
        self.brand = brand
        self.speed = speed
    }
    func accelerate() {
        speed += 10
    }
}
let car1 = Car(brand: "Tata", speed: 0)
let car2 = car1
car2.accelerate()
print(car1.speed)   // 10 — car1 and car2 are the SAME object

// 3
class Shape {
    func describe() { print("I am a shape") }
}
class Square: Shape {
    override func describe() { print("I am a square ⬛") }
}
class Triangle: Shape {
    override func describe() { print("I am a triangle 🔺") }
}
for s in [Shape(), Square(), Triangle()] {
    s.describe()
}

// 4
class Vehicle {
    var wheels: Int
    init(wheels: Int) {
        self.wheels = wheels
    }
}
class Bike: Vehicle {
    var hasBell: Bool
    init(hasBell: Bool) {
        self.hasBell = hasBell
        super.init(wheels: 2)
    }
}
let bike = Bike(hasBell: true)
print(bike.wheels, bike.hasBell)   // 2 true
```

</details>

---

## 🧠 Remember

- `class` is like `struct`, but:
  - Classes **need** an `init` (or default values).
  - Classes are **shared** (reference type), not copied.
  - Classes can **inherit**: `class Bird: Animal`.
- `override` replaces a parent's method. `super` calls the parent's version.
- In a subclass `init`: set your properties **first**, then `super.init(...)`.
- `final` stops inheritance. `deinit` runs when the object is destroyed.

---

⬅️ **Back:** [Chapter 20 — Structs](20-structs.md)
➡️ **Next:** [Chapter 22 — Struct vs Class](22-struct-vs-class.md)
