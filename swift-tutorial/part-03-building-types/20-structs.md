# Chapter 20 — Structs

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What a **struct** is and why we need it.
- **Properties**: the information inside a struct.
- **Methods**: the actions a struct can do.
- `mutating` methods.
- **Initializers** (`init`): how a struct is created.
- **Computed properties**.
- `static` properties.

---

## 1. The problem

Imagine you store information about a student:

```swift
let studentName = "Ravi"
let studentAge = 12
let studentGrade = 7
```

Now you have 30 students. That's 90 separate boxes! 😵
And nothing connects `studentName` with `studentAge`. It's messy.

We want **one thing** called "Student" that **holds everything together**.

---

## 2. What is a struct?

> 📖 **New word: Struct**
> Short for **structure**. A struct is **your own type** that groups related values together.

Think of a **form** 📝 you fill in at school:

```
┌──────── STUDENT FORM ────────┐
│ Name:  ____________          │
│ Age:   ____                  │
│ Grade: ____                  │
└──────────────────────────────┘
```

The **empty form** is the struct (the design).
Each **filled-in form** is one student (a real value).

---

## 3. Making a struct

```swift
struct Student {
    var name: String
    var age: Int
    var grade: Int
}
```

| Part | Meaning |
|---|---|
| `struct` | "I'm making a new type." |
| `Student` | The type's name. ⚠️ Types start with a **Capital** letter. |
| `{` | Start of what's inside. |
| `var name: String` | A **property**: every student has a name (a `String`). |
| `var age: Int` | Another property: age. |
| `var grade: Int` | Another property: grade. |
| `}` | End. |

> 📖 **New word: Property**
> A variable or constant that lives **inside** a struct.

💡 **Tip:** Remember the naming rule:
- **Types** (`Student`, `String`, `Int`) → **C**apital first letter.
- **Variables and functions** (`name`, `age`, `sayHello`) → small first letter.

---

## 4. Creating a value (an instance)

The struct is just the **design**. Now let's make a real student:

```swift
struct Student {
    var name: String
    var age: Int
    var grade: Int
}

let ravi = Student(name: "Ravi", age: 12, grade: 7)
let meena = Student(name: "Meena", age: 10, grade: 5)

print(ravi.name)
print(meena.age)
```

**Output:**

```
Ravi
10
```

| Part | Meaning |
|---|---|
| `Student(...)` | "Make a new `Student`." |
| `name: "Ravi", age: 12, grade: 7` | Fill in every property. |
| `let ravi = ...` | Store this student in `ravi`. |
| `ravi.name` | Use a **dot** to read a property. |

> 📖 **New word: Instance**
> One real value made from a type. `ravi` is an **instance** of `Student`.

```
   Student (design)
        │
   ┌────┴────┐
  ravi     meena      ← instances
```

---

## 5. Changing properties

```swift
var ravi = Student(name: "Ravi", age: 12, grade: 7)
ravi.age = 13
print(ravi.age)
```

**Output:**

```
13
```

⚠️ **Careful:** Two things must be `var`:

1. The **property** (`var age` inside the struct).
2. The **instance** (`var ravi`).

```swift
let ravi = Student(name: "Ravi", age: 12, grade: 7)
ravi.age = 13   // ❌ ERROR: cannot assign to property: 'ravi' is a 'let' constant
```

If you make the instance with `let`, **nothing** inside can change.

### `let` properties

```swift
struct Person {
    let birthYear: Int    // never changes
    var city: String      // can change
}

var p = Person(birthYear: 2010, city: "Pune")
p.city = "Delhi"          // ✅
// p.birthYear = 2011     // ❌ ERROR
```

---

## 6. Default values

```swift
struct Player {
    var name: String
    var score: Int = 0
    var lives: Int = 3
}

let p1 = Player(name: "Arun")
let p2 = Player(name: "Priya", score: 50)

print(p1.score, p1.lives)
print(p2.score, p2.lives)
```

**Output:**

```
0 3
50 3
```

| Part | Meaning |
|---|---|
| `var score: Int = 0` | If you don't give a score, it starts at 0. |
| `Player(name: "Arun")` | Only give the name. The rest use defaults. |

---

## 7. Methods: actions inside a struct

A struct can also have **functions** inside it. These are called **methods**.

```swift
struct Student {
    var name: String
    var age: Int

    func introduce() {
        print("Hi, I am \(name) and I am \(age).")
    }
}

let ravi = Student(name: "Ravi", age: 12)
ravi.introduce()
```

**Output:**

```
Hi, I am Ravi and I am 12.
```

| Part | Meaning |
|---|---|
| `func introduce()` | A function **inside** the struct = a **method**. |
| `\(name)` | Inside a method, you can use the struct's properties directly. |
| `ravi.introduce()` | Call the method with a dot. |

> 📖 **New word: Method**
> A function that belongs to a type.

You've used methods before: `"hi".uppercased()`, `array.append(5)`. Now you can make your own! 🎉

---

## 8. `mutating` methods

What if a method **changes** a property?

```swift
struct Counter {
    var count = 0

    func increase() {
        count += 1   // ❌ ERROR
    }
}
```

**Error:**

```
error: left side of mutating operator isn't mutable: 'self' is immutable
```

By default, struct methods **can't change** properties. To allow it, add `mutating`:

```swift
struct Counter {
    var count = 0

    mutating func increase() {
        count += 1
    }
}

var c = Counter()
c.increase()
c.increase()
print(c.count)
```

**Output:**

```
2
```

| Part | Meaning |
|---|---|
| `mutating` | "This method **changes** the struct." |
| `var c` | Must be `var`, because the method changes it. |
| `Counter()` | All properties have defaults, so no arguments needed. |

> 📖 **New word: Mutate**
> To **change**. A `mutating` method changes the struct's properties.

---

## 9. `self`

Inside a method, `self` means **"this instance"**.

```swift
struct Dog {
    var name: String

    func bark() {
        print("\(self.name) says Woof! 🐶")
    }
}

Dog(name: "Bruno").bark()
```

**Output:**

```
Bruno says Woof! 🐶
```

`self.name` and `name` mean the same thing here. Usually you can skip `self`.
You **need** it when a parameter has the **same name** as a property (see next section).

---

## 10. Initializers: `init`

When you write `Student(name: ..., age: ...)`, Swift runs an **initializer**.

> 📖 **New word: Initializer**
> Special code that runs when a new instance is **created**. Its job: give every property a value.

Swift makes one **automatically** for structs. That's called the **memberwise initializer**.

You can write your **own**:

```swift
struct Rectangle {
    var width: Double
    var height: Double

    init(side: Double) {
        self.width = side
        self.height = side
    }

    init(width: Double, height: Double) {
        self.width = width
        self.height = height
    }
}

let square = Rectangle(side: 5)
let rect = Rectangle(width: 4, height: 2)

print(square.width, square.height)
print(rect.width, rect.height)
```

**Output:**

```
5.0 5.0
4.0 2.0
```

| Part | Meaning |
|---|---|
| `init(side: Double)` | A custom way to create: give one side, make a square. |
| `self.width = side` | Put `side` into the property `width`. |
| `init(width:height:)` | Another way to create. |
| `self.width = width` | `self.width` = the **property**. `width` = the **parameter**. `self` tells them apart. |

⚠️ **Careful:** An `init` must give **every** property a value (unless it has a default).

⚠️ **Careful:** If you write your **own** `init` inside the struct, Swift **removes** the automatic one. That's why we wrote `init(width:height:)` ourselves above.

---

## 11. Computed properties

Some properties can be **calculated** from other properties.

```swift
struct Rectangle {
    var width: Double
    var height: Double

    var area: Double {
        width * height
    }
}

var r = Rectangle(width: 4, height: 3)
print(r.area)

r.width = 10
print(r.area)
```

**Output:**

```
12.0
30.0
```

| Part | Meaning |
|---|---|
| `var area: Double { ... }` | A **computed property**. It's not stored. It's **calculated** every time you read it. |
| `width * height` | How to calculate it. |
| After `r.width = 10` | `area` updates automatically! |

> 📖 **New word: Computed property**
> A property that calculates its value each time, instead of storing it.

| | Stored property | Computed property |
|---|---|---|
| Example | `var width: Double` | `var area: Double { width * height }` |
| Keeps a value in memory? | Yes | No, calculates every time |
| Must be | `var` or `let` | always `var` |

💡 **Tip:** SwiftUI uses computed properties a LOT. Every screen has `var body: some View { ... }` — that's a computed property!

---

## 12. Property observers: `didSet`

Run code **automatically** whenever a property changes.

```swift
struct Thermometer {
    var temperature: Double {
        didSet {
            print("Temperature changed from \(oldValue) to \(temperature)")
        }
    }
}

var t = Thermometer(temperature: 20)
t.temperature = 25
t.temperature = 18
```

**Output:**

```
Temperature changed from 20.0 to 25.0
Temperature changed from 25.0 to 18.0
```

| Part | Meaning |
|---|---|
| `didSet { ... }` | "After this property changes, run this code." |
| `oldValue` | A special name: the value **before** the change. |

---

## 13. `static`: belongs to the type, not an instance

```swift
struct Game {
    static let maxPlayers = 4
    var playerName: String
}

print(Game.maxPlayers)
```

**Output:**

```
4
```

| Part | Meaning |
|---|---|
| `static let maxPlayers` | Belongs to `Game` **itself**, not to any one game. All games share it. |
| `Game.maxPlayers` | Use the **type name**, not an instance. |

Think of a school rule 🏫: "Max 40 students per class." The rule belongs to the **school**, not to one student.

---

## 14. Structs are copied (value type)

This is **very important**:

```swift
struct Point {
    var x: Int
}

var a = Point(x: 1)
var b = a        // make a COPY
b.x = 100

print(a.x)
print(b.x)
```

**Output:**

```
1
100
```

| Line | What happens |
|---|---|
| `var b = a` | `b` gets its **own copy** of `a`. |
| `b.x = 100` | Only `b` changes. `a` stays 1. |

Think of a photocopy 📄📄: if you draw on the copy, the original stays clean.

> 📖 **New word: Value type**
> A type that is **copied** when you assign it. Structs, `Int`, `String`, `Array` are all value types.

We'll compare this with **classes** in the next chapters.

---

## 15. Mini project: a bank account 🏦

```swift
struct BankAccount {
    let owner: String
    var balance: Double = 0

    var isEmpty: Bool {
        balance == 0
    }

    mutating func deposit(_ amount: Double) {
        balance += amount
        print("Deposited \(amount). Balance: \(balance)")
    }

    mutating func withdraw(_ amount: Double) {
        if amount > balance {
            print("Not enough money! Balance is only \(balance).")
        } else {
            balance -= amount
            print("Withdrew \(amount). Balance: \(balance)")
        }
    }
}

var account = BankAccount(owner: "Meena")
print("Empty?", account.isEmpty)
account.deposit(500)
account.withdraw(200)
account.withdraw(1000)
print("Empty?", account.isEmpty)
```

**Output:**

```
Empty? true
Deposited 500.0. Balance: 500.0
Withdrew 200.0. Balance: 300.0
Not enough money! Balance is only 300.0.
Empty? false
```

| Part | Meaning |
|---|---|
| `let owner` | The owner never changes. |
| `var balance: Double = 0` | Starts at 0. Changes over time. |
| `var isEmpty: Bool { balance == 0 }` | Computed: is the account empty? |
| `mutating func deposit` | Changes `balance`, so it's `mutating`. |
| `withdraw` | Checks first. Doesn't allow taking more than you have. |

---

## 🏋️ Practice

1. Make a struct `Book` with `title: String`, `author: String` and `pages: Int`. Create two books and print their titles.
2. Add a method `describe()` to `Book` that prints `"TITLE by AUTHOR, PAGES pages"`.
3. Make a struct `Circle` with `radius: Double` and a computed property `area` (area = 3.14 × radius × radius).
4. Make a struct `Score` with `var points = 0` and a `mutating func add(_ n: Int)`. Add 10 three times and print the points.
5. Make `var a = Score()`, then `var b = a`. Add 5 to `b`. Print both. Why are they different?

<details>
<summary>Click to see the answers</summary>

```swift
// 1 & 2
struct Book {
    var title: String
    var author: String
    var pages: Int

    func describe() {
        print("\(title) by \(author), \(pages) pages")
    }
}
let b1 = Book(title: "Matilda", author: "Roald Dahl", pages: 240)
let b2 = Book(title: "Wonder", author: "R. J. Palacio", pages: 310)
print(b1.title)
print(b2.title)
b1.describe()

// 3
struct Circle {
    var radius: Double
    var area: Double {
        3.14 * radius * radius
    }
}
print(Circle(radius: 2).area)   // 12.56

// 4
struct Score {
    var points = 0
    mutating func add(_ n: Int) {
        points += n
    }
}
var s = Score()
s.add(10)
s.add(10)
s.add(10)
print(s.points)   // 30

// 5
var a = Score()
var b = a
b.add(5)
print(a.points)   // 0
print(b.points)   // 5
// Structs are copied. b is a separate copy of a.
```

</details>

---

## 🧠 Remember

- `struct Name { }` makes **your own type**. Type names start with a **Capital**.
- **Properties** store data. **Methods** are actions.
- Methods that change properties need `mutating`.
- `init` creates an instance. Swift writes one for you automatically.
- **Computed properties** calculate their value: `var area: Double { w * h }`.
- `static` belongs to the type itself.
- Structs are **copied** when assigned (value type).

---

⬅️ **Back:** [Chapter 19 — Closures](../part-02-swift-basics/19-closures.md)
➡️ **Next:** [Chapter 21 — Classes](21-classes.md)
