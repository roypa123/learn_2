# Chapter 25 — Extensions

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What an **extension** is.
- Adding methods and computed properties to **any** type — even `Int` and `String`!
- Adding new initializers.
- Using extensions to add protocol conformance.
- Protocol extensions (default code for a protocol).
- Using extensions to organize code.

---

## 1. What is an extension?

Imagine you have a phone 📱. You buy a **phone case with a stand**. Now your phone can stand on the table!

You didn't change the phone itself. You **added** something to it.

> 📖 **New word: Extension**
> A way to **add** new features (methods, computed properties, inits, protocols) to an **existing** type — even one you didn't write.

---

## 2. Your first extension

Let's add a method to `Int`, a type made by Apple!

```swift
extension Int {
    func squared() -> Int {
        self * self
    }
}

print(5.squared())
print(12.squared())
```

**Output:**

```
25
144
```

| Part | Meaning |
|---|---|
| `extension Int` | "I'm adding things to the `Int` type." |
| `func squared() -> Int` | A new method for every `Int`. |
| `self * self` | `self` is the number itself (5, then 12). |
| `5.squared()` | Now every `Int` has `squared()`! 🎉 |

---

## 3. Computed properties in extensions

```swift
extension Int {
    var isEven: Bool {
        self % 2 == 0
    }
}

print(4.isEven)
print(7.isEven)
```

**Output:**

```
true
false
```

⚠️ **Careful:** Extensions can add **computed** properties, but **not stored** properties.

```swift
extension Int {
    var nickname: String = "num"   // ❌ ERROR: extensions must not contain stored properties
}
```

---

## 4. Extending `String`

```swift
extension String {
    var isLong: Bool {
        count > 10
    }

    func shout() -> String {
        uppercased() + "!!!"
    }

    func repeated(_ times: Int) -> String {
        String(repeating: self, count: times)
    }
}

print("hello".shout())
print("ha".repeated(3))
print("Hi".isLong)
print("This is a long sentence".isLong)
```

**Output:**

```
HELLO!!!
hahaha
false
true
```

| Part | Meaning |
|---|---|
| `count > 10` | Inside the extension, `count` means `self.count`. |
| `uppercased() + "!!!"` | Use existing String methods inside. |
| `String(repeating:count:)` | A built-in way to repeat text. |

---

## 5. Extending `Double`

```swift
extension Double {
    var celsiusToFahrenheit: Double {
        self * 9 / 5 + 32
    }
}

let today = 30.0
print("\(today)°C = \(today.celsiusToFahrenheit)°F")
```

**Output:**

```
30.0°C = 86.0°F
```

---

## 6. Extending your own types

You can extend your **own** structs too. This is great for **organizing** code.

```swift
struct Book {
    var title: String
    var pages: Int
}

extension Book {
    var isShort: Bool {
        pages < 100
    }

    func summary() -> String {
        "\(title) (\(pages) pages)"
    }
}

let b = Book(title: "Tiny Tales", pages: 64)
print(b.summary())
print(b.isShort)
```

**Output:**

```
Tiny Tales (64 pages)
true
```

---

## 7. Adding an initializer — and keeping the automatic one!

Remember: if you write an `init` **inside** a struct, you lose the automatic one.

But if you write it in an **extension**, you keep **both**! 🎉

```swift
struct Point {
    var x: Double
    var y: Double
}

extension Point {
    init(both value: Double) {
        self.x = value
        self.y = value
    }
}

let p1 = Point(x: 1, y: 2)       // automatic init — still works!
let p2 = Point(both: 5)          // our new init

print(p1.x, p1.y)
print(p2.x, p2.y)
```

**Output:**

```
1.0 2.0
5.0 5.0
```

💡 **Tip:** This is a common trick. Put custom `init`s in an extension to keep the free one.

---

## 8. Adding protocol conformance with an extension

```swift
struct Player {
    var name: String
    var level: Int
}

extension Player: CustomStringConvertible {
    var description: String {
        "🎮 \(name) (Level \(level))"
    }
}

print(Player(name: "Arun", level: 7))
```

**Output:**

```
🎮 Arun (Level 7)
```

| Part | Meaning |
|---|---|
| `extension Player: CustomStringConvertible` | "Make `Player` follow this protocol." |
| `var description` | Provide what the protocol needs. |

💡 **Tip:** Many programmers put **each protocol in its own extension**. It keeps code tidy:

```swift
struct Player { ... }
extension Player: CustomStringConvertible { ... }
extension Player: Comparable { ... }
```

---

## 9. Protocol extensions: free code for everyone 🎁

When you extend a **protocol**, **every** type that follows it gets the new code.

```swift
protocol Shape {
    var area: Double { get }
}

extension Shape {
    func describe() -> String {
        "This shape has an area of \(area)."
    }

    var isBig: Bool {
        area > 50
    }
}

struct Square: Shape {
    var side: Double
    var area: Double { side * side }
}

struct Circle: Shape {
    var radius: Double
    var area: Double { 3.14 * radius * radius }
}

print(Square(side: 3).describe())
print(Circle(radius: 5).isBig)
```

**Output:**

```
This shape has an area of 9.0.
true
```

`Square` and `Circle` never wrote `describe()` or `isBig`. They got them **for free** from the protocol extension!

### Extending Apple's protocols

```swift
extension Collection {
    var isNotEmpty: Bool {
        !isEmpty
    }
}

print([1, 2, 3].isNotEmpty)
print("".isNotEmpty)
print(Set<Int>().isNotEmpty)
```

**Output:**

```
true
false
false
```

`Array`, `String`, `Set` and `Dictionary` all follow `Collection`, so they **all** get `isNotEmpty`. One extension, many types! ✨

---

## 10. Extending only some types: `where`

```swift
extension Array where Element == Int {
    var total: Int {
        reduce(0, +)
    }
}

print([1, 2, 3, 4].total)
// print(["a", "b"].total)   // ❌ ERROR — only for arrays of Int
```

**Output:**

```
10
```

| Part | Meaning |
|---|---|
| `extension Array` | Add to arrays… |
| `where Element == Int` | …but **only** arrays of `Int`. |
| `Element` | The type of items inside the array. |

---

## 11. Mini project: a toolbox of helpers 🧰

```swift
extension Int {
    var isPrime: Bool {
        if self < 2 { return false }
        for i in 2..<self where i * i <= self {
            if self % i == 0 { return false }
        }
        return true
    }

    func times(_ action: () -> Void) {
        for _ in 0..<self {
            action()
        }
    }
}

extension String {
    var isPalindrome: Bool {
        let clean = lowercased().filter { $0.isLetter }
        return clean == String(clean.reversed())
    }

    var wordCount: Int {
        split(separator: " ").count
    }
}

extension Array where Element == Double {
    var average: Double {
        isEmpty ? 0 : reduce(0, +) / Double(count)
    }
}

print((1...20).filter { $0.isPrime })
3.times { print("Hip hip hooray! 🎉") }
print("Race car".isPalindrome)
print("Swift is really fun".wordCount)
print([80.0, 90.0, 100.0].average)
```

**Output:**

```
[2, 3, 5, 7, 11, 13, 17, 19]
Hip hip hooray! 🎉
Hip hip hooray! 🎉
Hip hip hooray! 🎉
true
4
90.0
```

| Helper | What it does |
|---|---|
| `isPrime` | Is the number only divisible by 1 and itself? |
| `times(_:)` | Repeat a closure N times: `3.times { ... }` |
| `isPalindrome` | Same forwards and backwards? (ignores spaces and case) |
| `wordCount` | Splits the text at spaces and counts the pieces. |
| `average` | Average of an array of `Double`s. |

New things here:
- `for i in 2..<self where i * i <= self` — a `for` loop with a `where` filter: only run when the condition is true.
- `$0.isLetter` — is this character a letter?
- `split(separator: " ")` — cut a string into pieces at each space.

---

## 🏋️ Practice

1. Extend `Int` with `var isNegative: Bool`.
2. Extend `String` with `func addExclamation() -> String` that adds `"!"` at the end.
3. Extend `Double` with `var rounded2: Double` that rounds to 2 decimal places. (Hint: `(self * 100).rounded() / 100`)
4. Make a struct `Dog` with `name`. In an extension, make it `CustomStringConvertible` so it prints `"🐶 NAME"`.
5. Extend `Array where Element == String` with `var longest: String?` that returns the longest string (or `nil` if empty). (Hint: `self.max { $0.count < $1.count }`)

<details>
<summary>Click to see the answers</summary>

```swift
// 1
extension Int {
    var isNegative: Bool { self < 0 }
}
print((-5).isNegative)   // true

// 2
extension String {
    func addExclamation() -> String { self + "!" }
}
print("Wow".addExclamation())   // Wow!

// 3
extension Double {
    var rounded2: Double { (self * 100).rounded() / 100 }
}
print(3.14159.rounded2)   // 3.14

// 4
struct Dog { var name: String }
extension Dog: CustomStringConvertible {
    var description: String { "🐶 \(name)" }
}
print(Dog(name: "Bruno"))

// 5
extension Array where Element == String {
    var longest: String? {
        self.max { $0.count < $1.count }
    }
}
print(["cat", "elephant", "dog"].longest ?? "none")   // elephant
```

Note: in exercise 1 we write `(-5).isNegative` with brackets, so Swift reads the minus sign correctly.

</details>

---

## 🧠 Remember

- `extension TypeName { }` adds new features to an existing type.
- You can add: methods, **computed** properties, inits, protocol conformance.
- You **cannot** add stored properties.
- `init` in an extension keeps the automatic memberwise init.
- **Protocol extensions** give default code to every type that follows the protocol.
- `where` limits an extension to some types: `extension Array where Element == Int`.

---

⬅️ **Back:** [Chapter 24 — Protocols](24-protocols.md)
➡️ **Next:** [Chapter 26 — Error Handling](26-error-handling.md)
