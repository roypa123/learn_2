# Chapter 24 — Protocols

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What a **protocol** is.
- Making a type **conform** to a protocol.
- Protocols with properties and methods.
- Using a protocol as a type (`any`).
- Swift's built-in protocols: `Equatable`, `Comparable`, `Hashable`, `CustomStringConvertible`, `Identifiable`.

💡 **Why this matters:** In SwiftUI, every screen piece **conforms** to the `View` protocol. You'll write `struct MyScreen: View` hundreds of times!

---

## 1. What is a protocol?

Think of a **job description** 📋:

> **Wanted: Driver**
> Must be able to: drive a car, read a map.

The job description doesn't say **who** you are. It says **what you must be able to do**.
Anyone who can do these things can be a driver.

> 📖 **New word: Protocol**
> A list of **requirements** (properties and methods) that a type promises to have.

> 📖 **New word: Conform**
> When a type **follows** a protocol — it has everything the protocol asks for.

---

## 2. Making a protocol

```swift
protocol Greetable {
    func greet()
}
```

| Part | Meaning |
|---|---|
| `protocol` | "I'm making a protocol." |
| `Greetable` | Its name. Capital letter. Often ends in `-able` or `-ible`. |
| `func greet()` | A requirement: "You must have a `greet()` method." |

⚠️ Notice: **no `{ }` body** for the method. The protocol only says **what**, not **how**.

---

## 3. Conforming to a protocol

```swift
protocol Greetable {
    func greet()
}

struct Person: Greetable {
    var name: String

    func greet() {
        print("Hello, I'm \(name)! 👋")
    }
}

struct Robot: Greetable {
    var id: Int

    func greet() {
        print("BEEP. UNIT \(id) SAYS HELLO. 🤖")
    }
}

Person(name: "Meena").greet()
Robot(id: 42).greet()
```

**Output:**

```
Hello, I'm Meena! 👋
BEEP. UNIT 42 SAYS HELLO. 🤖
```

| Part | Meaning |
|---|---|
| `struct Person: Greetable` | "`Person` promises to follow `Greetable`." |
| `func greet() { ... }` | `Person` keeps its promise by writing `greet()`. |
| `struct Robot: Greetable` | `Robot` also promises — but greets **its own** way. |

If you forget `greet()`:

```swift
struct Cat: Greetable { }
```

**Error:**

```
error: type 'Cat' does not conform to protocol 'Greetable'
```

Swift checks the promise! ✅

---

## 4. Property requirements

```swift
protocol Named {
    var name: String { get }
}

struct Dog: Named {
    var name: String
}

struct City: Named {
    let name: String
    let population: Int
}

print(Dog(name: "Bruno").name)
print(City(name: "Chennai", population: 7_000_000).name)
```

**Output:**

```
Bruno
Chennai
```

| Part | Meaning |
|---|---|
| `var name: String { get }` | "You must have a `name` that can be **read**." |
| `{ get }` | Read-only is enough. (`let`, `var`, or a computed property all work.) |
| `{ get set }` | Would mean: must be readable **and** changeable (must be a `var`). |

💡 **Tip:** `7_000_000` is the same as `7000000`. The `_` just makes big numbers easier to read!

---

## 5. Using a protocol as a type

You can make an array of **different types**, as long as they all conform to the same protocol.

```swift
protocol Shape {
    var area: Double { get }
    var name: String { get }
}

struct Square: Shape {
    var side: Double
    var area: Double { side * side }
    var name: String { "Square" }
}

struct Circle: Shape {
    var radius: Double
    var area: Double { 3.14 * radius * radius }
    var name: String { "Circle" }
}

let shapes: [any Shape] = [Square(side: 2), Circle(radius: 1), Square(side: 3)]

for shape in shapes {
    print("\(shape.name): \(shape.area)")
}
```

**Output:**

```
Square: 4.0
Circle: 3.14
Square: 9.0
```

| Part | Meaning |
|---|---|
| `[any Shape]` | "An array of **anything** that is a `Shape`." |
| `any` | Means the real type can be **different** for each item. |
| `shape.area` | We can use `area` because every `Shape` promises to have it. |

This is like the `[Animal]` array in the classes chapter — but it works with **structs** too, and without inheritance!

> 📖 **New word: `any`**
> Written before a protocol name when you use it as a type: `any Shape`. "Any type that follows `Shape`."

### `some` — you'll see it in SwiftUI

```swift
func makeShape() -> some Shape {
    Square(side: 5)
}
```

`some Shape` means: *"This returns **one specific** type that is a `Shape`. I won't tell you which one, but it's always the same."*

| | `any Shape` | `some Shape` |
|---|---|---|
| Can be different types? | ✅ Yes (each item can differ) | ❌ No — one fixed type |
| Where you'll see it | arrays of mixed things | SwiftUI: `var body: some View` |

Don't worry if this feels hard. You'll understand it better when you use SwiftUI.

---

## 6. A type can follow many protocols

```swift
protocol Swimmer {
    func swim()
}

protocol Flyer {
    func fly()
}

struct Duck: Swimmer, Flyer {
    func swim() { print("🦆 paddles in the pond") }
    func fly() { print("🦆 flies over the trees") }
}

let d = Duck()
d.swim()
d.fly()
```

**Output:**

```
🦆 paddles in the pond
🦆 flies over the trees
```

Separate protocols with commas: `struct Duck: Swimmer, Flyer`.

💡 **Tip:** A class can inherit from only **one** class, but any type can follow **many** protocols. That's why Swift programmers love protocols.

---

## 7. Built-in protocols you'll use a lot

### `Equatable` — can be compared with `==`

```swift
struct Point: Equatable {
    var x: Int
    var y: Int
}

let a = Point(x: 1, y: 2)
let b = Point(x: 1, y: 2)
print(a == b)
```

**Output:**

```
true
```

Just add `: Equatable`. Swift writes the `==` for you (if all properties are `Equatable`). ✨

### `Comparable` — can be compared with `<`, `>` and sorted

```swift
struct Student: Comparable {
    var name: String
    var marks: Int

    static func < (lhs: Student, rhs: Student) -> Bool {
        lhs.marks < rhs.marks
    }
}

let students = [
    Student(name: "Ravi", marks: 78),
    Student(name: "Meena", marks: 92),
    Student(name: "Arun", marks: 65)
]

for s in students.sorted() {
    print(s.name, s.marks)
}
```

**Output:**

```
Arun 65
Ravi 78
Meena 92
```

| Part | Meaning |
|---|---|
| `: Comparable` | "Students can be compared." |
| `static func < (lhs:rhs:)` | We explain **how**: by marks. `lhs` = left-hand side, `rhs` = right-hand side. |
| `.sorted()` | Now works without a closure! |

### `Hashable` — can go in a `Set` or be a dictionary key

```swift
struct Tag: Hashable {
    var label: String
}

let tags: Set = [Tag(label: "swift"), Tag(label: "ios"), Tag(label: "swift")]
print(tags.count)
```

**Output:**

```
2
```

### `CustomStringConvertible` — control how it prints

```swift
struct Money: CustomStringConvertible {
    var amount: Double

    var description: String {
        "₹\(amount)"
    }
}

print(Money(amount: 99.5))
```

**Output:**

```
₹99.5
```

| Part | Meaning |
|---|---|
| `var description: String` | The protocol requires this. `print` uses it. |

### `Identifiable` — has a unique `id`

```swift
struct TodoItem: Identifiable {
    let id: Int
    var title: String
}
```

💡 **Look ahead:** SwiftUI's `List` and `ForEach` need items to be `Identifiable`, so it can tell each row apart. You'll see this in Chapter 48!

| Protocol | Gives you |
|---|---|
| `Equatable` | `==` and `!=` |
| `Comparable` | `<`, `>`, `.sorted()`, `.min()`, `.max()` |
| `Hashable` | use in `Set` and as dictionary keys |
| `CustomStringConvertible` | nice `print` output |
| `Identifiable` | a unique `id` (used by SwiftUI lists) |
| `CaseIterable` | `.allCases` for enums (Chapter 23) |

---

## 8. Protocol extensions: default behavior

You can give a protocol **default** code. We'll see more in the next chapter (Extensions).

```swift
protocol Greetable {
    var name: String { get }
    func greet()
}

extension Greetable {
    func greet() {
        print("Hi, I'm \(name).")
    }
}

struct Kid: Greetable {
    var name: String
}

Kid(name: "Priya").greet()
```

**Output:**

```
Hi, I'm Priya.
```

`Kid` didn't write `greet()`. It got the **default** version for free! 🎁

---

## 9. Mini project: a zoo 🦁

```swift
protocol Animal: CustomStringConvertible {
    var name: String { get }
    var sound: String { get }
    var legs: Int { get }
}

extension Animal {
    var description: String {
        "\(name) has \(legs) legs and says \"\(sound)\""
    }
}

struct Lion: Animal {
    let name = "Lion 🦁"
    let sound = "Roar"
    let legs = 4
}

struct Parrot: Animal {
    let name = "Parrot 🦜"
    let sound = "Hello!"
    let legs = 2
}

struct Snake: Animal {
    let name = "Snake 🐍"
    let sound = "Hiss"
    let legs = 0
}

let zoo: [any Animal] = [Lion(), Parrot(), Snake()]

for animal in zoo {
    print(animal)
}

let totalLegs = zoo.reduce(0) { $0 + $1.legs }
print("Total legs in the zoo: \(totalLegs)")
```

**Output:**

```
Lion 🦁 has 4 legs and says "Roar"
Parrot 🦜 has 2 legs and says "Hello!"
Snake 🐍 has 0 legs and says "Hiss"
Total legs in the zoo: 6
```

| Part | Meaning |
|---|---|
| `protocol Animal: CustomStringConvertible` | A protocol can **build on** another protocol. |
| `extension Animal { var description ... }` | Every animal gets a default `description`. |
| `[any Animal]` | Different structs in one array. |
| `print(animal)` | Uses `description`. |

---

## 🏋️ Practice

1. Make a protocol `Describable` with `func describe() -> String`. Make `Car` and `Phone` structs conform to it.
2. Make a protocol `Priced` with `var price: Double { get }`. Make two structs conform. Put them in a `[any Priced]` array and add up all prices.
3. Make `struct Fruit: Equatable` with `name` and `color`. Check if two fruits are equal.
4. Make `struct Song: Comparable` sorted by `duration: Int`. Sort an array of 3 songs.
5. Make `struct Temperature: CustomStringConvertible` that prints like `25.0°C`.

<details>
<summary>Click to see the answers</summary>

```swift
// 1
protocol Describable {
    func describe() -> String
}
struct Car: Describable {
    var brand: String
    func describe() -> String { "A \(brand) car" }
}
struct Phone: Describable {
    var model: String
    func describe() -> String { "A \(model) phone" }
}
print(Car(brand: "Tata").describe())
print(Phone(model: "iPhone").describe())

// 2
protocol Priced {
    var price: Double { get }
}
struct Pen: Priced { var price: Double }
struct Bag: Priced { var price: Double }
let things: [any Priced] = [Pen(price: 10), Bag(price: 499)]
print(things.reduce(0) { $0 + $1.price })   // 509.0

// 3
struct Fruit: Equatable {
    var name: String
    var color: String
}
print(Fruit(name: "Apple", color: "Red") == Fruit(name: "Apple", color: "Red"))   // true

// 4
struct Song: Comparable {
    var title: String
    var duration: Int
    static func < (lhs: Song, rhs: Song) -> Bool {
        lhs.duration < rhs.duration
    }
}
let songs = [Song(title: "A", duration: 240), Song(title: "B", duration: 180), Song(title: "C", duration: 300)]
for s in songs.sorted() { print(s.title, s.duration) }

// 5
struct Temperature: CustomStringConvertible {
    var celsius: Double
    var description: String { "\(celsius)°C" }
}
print(Temperature(celsius: 25))   // 25.0°C
```

</details>

---

## 🧠 Remember

- A **protocol** is a list of requirements: `protocol Greetable { func greet() }`.
- A type **conforms** with `: ProtocolName` and must provide everything.
- `{ get }` = readable. `{ get set }` = readable and changeable.
- `[any Shape]` = mixed types that all follow `Shape`.
- `some View` = one hidden, fixed type (you'll see it in SwiftUI).
- Many types → one protocol. One type → many protocols.
- Built-in: `Equatable`, `Comparable`, `Hashable`, `CustomStringConvertible`, `Identifiable`.

---

⬅️ **Back:** [Chapter 23 — Enums](23-enums.md)
➡️ **Next:** [Chapter 25 — Extensions](25-extensions.md)
