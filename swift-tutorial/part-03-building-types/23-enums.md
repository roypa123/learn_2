# Chapter 23 — Enums

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What an **enum** is.
- Using enums with `switch`.
- Raw values (`String`, `Int`).
- `CaseIterable` — loop over all cases.
- Methods and computed properties in enums.
- **Associated values** — extra data attached to a case.

---

## 1. The problem

Imagine a direction in a game: north, south, east, west.

You could use strings:

```swift
var direction = "north"
direction = "nroth"   // typo! 😱 Swift doesn't notice.
```

Strings can be **anything**. Typos are not caught.

We want a type that can **only** be one of a few fixed choices.

---

## 2. What is an enum?

> 📖 **New word: Enum**
> Short for **enumeration**. A type with a **fixed list of choices**.

Think of a traffic light 🚦: it can **only** be red, yellow or green. Never "purple".

```swift
enum Direction {
    case north
    case south
    case east
    case west
}

var heading = Direction.north
print(heading)

heading = .east
print(heading)
```

**Output:**

```
north
east
```

| Part | Meaning |
|---|---|
| `enum Direction` | "Make a new type called `Direction`." Capital letter. |
| `case north` | One possible choice. Cases use small letters. |
| `Direction.north` | Use the choice `north`. |
| `heading = .east` | Swift already knows `heading` is a `Direction`, so you can skip the type name and write just `.east`. |

You can also write cases on one line:

```swift
enum Direction {
    case north, south, east, west
}
```

Now typos are caught:

```swift
heading = .nroth   // ❌ ERROR: type 'Direction' has no member 'nroth'
```

🎉 Swift protects you!

---

## 3. Enums and `switch` — best friends 🤝

```swift
enum TrafficLight {
    case red, yellow, green
}

let light = TrafficLight.yellow

switch light {
case .red:
    print("Stop 🛑")
case .yellow:
    print("Slow down ⚠️")
case .green:
    print("Go ✅")
}
```

**Output:**

```
Slow down ⚠️
```

Notice: **no `default`** needed! 🎉

Why? An enum has a **fixed** list. Swift knows we covered **all** cases. The switch is exhaustive.

💡 **Tip:** If you later add `case blinking` to the enum, Swift will show an error in every `switch` that forgot it. That helps you never miss a case!

---

## 4. Comparing enums

```swift
let light = TrafficLight.red

if light == .red {
    print("Wait...")
}
```

**Output:**

```
Wait...
```

---

## 5. Raw values

You can give each case a fixed **value** behind it.

### String raw values

```swift
enum Planet: String {
    case mercury = "Mercury ☿"
    case earth = "Earth 🌍"
    case mars = "Mars 🔴"
}

print(Planet.earth.rawValue)
```

**Output:**

```
Earth 🌍
```

| Part | Meaning |
|---|---|
| `enum Planet: String` | Each case has a `String` value behind it. |
| `case earth = "Earth 🌍"` | The value for `earth`. |
| `.rawValue` | Get that value. |

> 📖 **New word: Raw value**
> A fixed value (like a String or Int) stored behind each enum case.

If you don't give a value, Swift uses the **case name**:

```swift
enum Size: String {
    case small, medium, large
}
print(Size.medium.rawValue)   // medium
```

### Int raw values

```swift
enum Level: Int {
    case easy = 1
    case medium      // 2 (automatic)
    case hard        // 3 (automatic)
}

print(Level.hard.rawValue)
```

**Output:**

```
3
```

With `Int`, Swift counts up automatically from the last number.

### Making an enum from a raw value

```swift
let size = Size(rawValue: "large")
print(size)

let wrong = Size(rawValue: "huge")
print(wrong)
```

**Output** (something like):

```
Optional(Size.large)
nil
```

(Some versions show the module name too, like `Optional(main.Size.large)`. That's fine.)

It's an **Optional**, because the text might not match any case! Use `if let`:

```swift
if let s = Size(rawValue: "small") {
    print("Found size: \(s)")
}
```

---

## 6. Looping over all cases: `CaseIterable`

```swift
enum Weekday: CaseIterable {
    case monday, tuesday, wednesday, thursday, friday
}

for day in Weekday.allCases {
    print(day)
}

print("There are \(Weekday.allCases.count) school days.")
```

**Output:**

```
monday
tuesday
wednesday
thursday
friday
There are 5 school days.
```

| Part | Meaning |
|---|---|
| `: CaseIterable` | "Give me a list of all cases." |
| `Weekday.allCases` | An array of every case. |

You can combine: `enum Size: String, CaseIterable { ... }`

---

## 7. Methods and computed properties

Enums can have methods and computed properties, just like structs!

```swift
enum Weather {
    case sunny, rainy, snowy

    var emoji: String {
        switch self {
        case .sunny: "☀️"
        case .rainy: "🌧️"
        case .snowy: "❄️"
        }
    }

    func advice() -> String {
        switch self {
        case .sunny: return "Wear sunglasses."
        case .rainy: return "Take an umbrella."
        case .snowy: return "Wear a warm coat."
        }
    }
}

let today = Weather.rainy
print(today.emoji, today.advice())
```

**Output:**

```
🌧️ Take an umbrella.
```

| Part | Meaning |
|---|---|
| `var emoji: String { ... }` | A computed property. |
| `switch self` | `self` is the current case (here `.rainy`). |
| `case .sunny: "☀️"` | Short form: each case gives one value (switch as a value, Swift 5.9+). |
| `func advice() -> String` | A method that returns a string. |

### `mutating` methods in enums

```swift
enum Switch {
    case on, off

    mutating func toggle() {
        self = (self == .on) ? .off : .on
    }
}

var lamp = Switch.off
lamp.toggle()
print(lamp)
lamp.toggle()
print(lamp)
```

**Output:**

```
on
off
```

`self = ...` changes the enum to a different case.

---

## 8. Associated values ⭐

Sometimes each case needs **extra information**.

Example: a payment can be:
- **cash** (how much?)
- **card** (card number?)
- **UPI** (UPI ID?)

Each case needs **different** data.

```swift
enum Payment {
    case cash(amount: Double)
    case card(number: String)
    case upi(id: String)
}

let p1 = Payment.cash(amount: 500)
let p2 = Payment.card(number: "1234-5678")
let p3 = Payment.upi(id: "ravi@bank")
```

| Part | Meaning |
|---|---|
| `case cash(amount: Double)` | The `cash` case carries a `Double` called `amount`. |
| `case card(number: String)` | The `card` case carries a `String`. |
| `Payment.cash(amount: 500)` | Make a cash payment with 500 attached. |

> 📖 **New word: Associated value**
> Extra data attached to one enum case. Each case can have different data.

### Reading associated values with `switch`

```swift
func describe(_ payment: Payment) {
    switch payment {
    case .cash(let amount):
        print("Paid \(amount) in cash 💵")
    case .card(let number):
        print("Paid with card \(number) 💳")
    case .upi(let id):
        print("Paid with UPI \(id) 📱")
    }
}

describe(p1)
describe(p2)
describe(p3)
```

**Output:**

```
Paid 500.0 in cash 💵
Paid with card 1234-5678 💳
Paid with UPI ravi@bank 📱
```

| Part | Meaning |
|---|---|
| `case .cash(let amount):` | "If it's cash, take out the attached value and call it `amount`." |

### Checking just one case with `if case`

```swift
if case .upi(let id) = p3 {
    print("UPI ID is \(id)")
}
```

**Output:**

```
UPI ID is ravi@bank
```

---

## 9. Enums vs raw values vs associated values

| Kind | Example | Use when |
|---|---|---|
| Simple enum | `case red, green` | Just a fixed list of choices. |
| Raw value | `case red = "Red"` | Each case has **one fixed value** (same for all instances). |
| Associated value | `case cash(amount: Double)` | Each instance carries **its own** data. |

---

## 10. Mini project: app loading state ⏳

Real apps often use an enum like this to show what's happening:

```swift
enum LoadingState {
    case idle
    case loading
    case success(data: [String])
    case failure(message: String)
}

func show(_ state: LoadingState) {
    switch state {
    case .idle:
        print("Tap the button to load.")
    case .loading:
        print("Loading... ⏳")
    case .success(let data):
        print("Loaded \(data.count) items: \(data)")
    case .failure(let message):
        print("Error: \(message) ❌")
    }
}

show(.idle)
show(.loading)
show(.success(data: ["Apple", "Banana"]))
show(.failure(message: "No internet"))
```

**Output:**

```
Tap the button to load.
Loading... ⏳
Loaded 2 items: ["Apple", "Banana"]
Error: No internet ❌
```

💡 **Look ahead:** In SwiftUI, you'll use exactly this kind of enum to decide what the screen shows: a spinner, a list, or an error message.

---

## 🏋️ Practice

1. Make an enum `Season` with 4 cases. Use a `switch` to print a different message for each.
2. Make `enum Coin: Int` with `penny = 1`, `nickel = 5`, `dime = 10`, `quarter = 25`. Print the raw value of `.dime`.
3. Make `Season` `CaseIterable` and print all seasons with a loop.
4. Add a computed property `emoji` to `Season`.
5. Make `enum Shape` with `case circle(radius: Double)` and `case rectangle(width: Double, height: Double)`. Write a function `area(_ s: Shape) -> Double`.

<details>
<summary>Click to see the answers</summary>

```swift
// 1, 3, 4
enum Season: CaseIterable {
    case spring, summer, autumn, winter

    var emoji: String {
        switch self {
        case .spring: "🌸"
        case .summer: "☀️"
        case .autumn: "🍂"
        case .winter: "⛄"
        }
    }
}

let now = Season.summer
switch now {
case .spring: print("Flowers are blooming")
case .summer: print("Time for ice cream")
case .autumn: print("Leaves are falling")
case .winter: print("Stay warm")
}

for s in Season.allCases {
    print(s, s.emoji)
}

// 2
enum Coin: Int {
    case penny = 1, nickel = 5, dime = 10, quarter = 25
}
print(Coin.dime.rawValue)   // 10

// 5
enum Shape {
    case circle(radius: Double)
    case rectangle(width: Double, height: Double)
}

func area(_ s: Shape) -> Double {
    switch s {
    case .circle(let r):
        return 3.14 * r * r
    case .rectangle(let w, let h):
        return w * h
    }
}
print(area(.circle(radius: 1)))                 // 3.14
print(area(.rectangle(width: 2, height: 5)))    // 10.0
```

</details>

---

## 🧠 Remember

- `enum` = a type with a **fixed list of choices**.
- Use `.caseName` when Swift knows the type.
- `switch` on an enum needs **no `default`** if all cases are covered.
- **Raw values**: `enum Size: String { case small }` → `.rawValue`.
- `CaseIterable` → `.allCases`.
- **Associated values**: `case cash(amount: Double)` → read with `case .cash(let amount)`.

---

⬅️ **Back:** [Chapter 22 — Struct vs Class](22-struct-vs-class.md)
➡️ **Next:** [Chapter 24 — Protocols](24-protocols.md)
