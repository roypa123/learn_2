# Chapter 19 — Closures: Functions Without Names

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What a **closure** is.
- How to store a function in a variable.
- How to pass a closure to another function.
- **Trailing closure** syntax (very common in SwiftUI!).
- Short names: `$0`, `$1`.
- Super useful array tools: `map`, `filter`, `reduce`, `sorted(by:)`, `forEach`.

💡 **Why this matters:** SwiftUI uses closures **everywhere**. Every button, every list. If you understand this chapter, SwiftUI will feel much easier later.

---

## 1. Functions are values too

In Swift, you can put a function into a box (variable), just like a number or a string.

```swift
func sayHi() {
    print("Hi!")
}

let action = sayHi
action()
```

**Output:**

```
Hi!
```

| Part | Meaning |
|---|---|
| `let action = sayHi` | Put the function `sayHi` into the box `action`. **No `()`** — we are not calling it, just storing it. |
| `action()` | Call the function that is inside the box. |

⚠️ **Careful:**

| Code | Meaning |
|---|---|
| `sayHi` | The function itself (like a recipe 📜). |
| `sayHi()` | **Run** the function (cook the recipe 🍳). |

---

## 2. What is a closure?

A **closure** is a function **without a name**, written directly where you need it.

> 📖 **New word: Closure**
> A block of code you can store in a variable or pass to a function. Like a function without a name.

```swift
let sayHello = {
    print("Hello!")
}

sayHello()
```

**Output:**

```
Hello!
```

| Part | Meaning |
|---|---|
| `let sayHello =` | A box called `sayHello`. |
| `{ print("Hello!") }` | A **closure** — a block of code with no name. |
| `sayHello()` | Run the code inside. |

---

## 3. Closures with inputs and outputs

A normal function:

```swift
func double(n: Int) -> Int {
    return n * 2
}
```

The **same thing** as a closure:

```swift
let double = { (n: Int) -> Int in
    return n * 2
}

print(double(5))
```

**Output:**

```
10
```

| Part | Meaning |
|---|---|
| `{` | Start of the closure. |
| `(n: Int)` | Input: `n`, an `Int`. |
| `-> Int` | Output: an `Int`. |
| `in` | **Important!** Means: "inputs and output are done. The code starts **now**." |
| `return n * 2` | The code. |
| `}` | End. |
| `double(5)` | Call it. **No label** needed for closures. |

Side by side:

```
func double(n: Int) -> Int {   return n * 2 }
   {       (n: Int) -> Int in  return n * 2 }
```

The closure moves the `{` to the **front** and adds `in`.

---

## 4. Passing a closure to a function ⭐

This is **the main reason** closures exist.

```swift
func doTwice(action: () -> Void) {
    action()
    action()
}

doTwice(action: {
    print("Jump! 🦘")
})
```

**Output:**

```
Jump! 🦘
Jump! 🦘
```

| Part | Meaning |
|---|---|
| `action: () -> Void` | A parameter that is a **function**. `()` = no inputs. `-> Void` = gives nothing back. |
| `action()` | Run the function we were given. |
| `doTwice(action: { ... })` | Give a closure as the argument. |

> 📖 **New word: Void**
> Means "**nothing**". A function that returns `Void` doesn't give anything back.

Think of it like this: you give a friend a **note with instructions** 📝. Your friend decides **when** (and how many times) to follow it.

---

## 5. Trailing closures ⭐⭐

When the **last** argument is a closure, you can write it **after** the brackets:

```swift
// Normal way
doTwice(action: {
    print("Jump!")
})

// Trailing closure — same thing, cleaner!
doTwice {
    print("Jump!")
}
```

| Part | Meaning |
|---|---|
| `doTwice` | Function name. |
| (no `()`) | If the closure is the **only** argument, you can drop the brackets. |
| `{ print("Jump!") }` | The closure, written after. |

> 📖 **New word: Trailing closure**
> A closure written **after** the function's brackets, because it is the last argument.

💡 **Look ahead:** In SwiftUI, you will write things like this all the time:

```swift
Button("Tap me") {
    print("Tapped!")
}
```

That `{ print("Tapped!") }` is a **trailing closure**! It means: *"When the button is tapped, run this."*

---

## 6. Closures with inputs, passed to functions

```swift
func doMath(a: Int, b: Int, operation: (Int, Int) -> Int) -> Int {
    return operation(a, b)
}

let sum = doMath(a: 6, b: 3) { (x: Int, y: Int) -> Int in
    return x + y
}

let product = doMath(a: 6, b: 3) { (x: Int, y: Int) -> Int in
    return x * y
}

print(sum)
print(product)
```

**Output:**

```
9
18
```

| Part | Meaning |
|---|---|
| `operation: (Int, Int) -> Int` | A function that takes two `Int`s and gives back an `Int`. |
| `operation(a, b)` | Run it with `a` and `b`. |
| `{ (x: Int, y: Int) -> Int in return x + y }` | The closure we pass: "add them". |

Same function `doMath`, **different** behavior, depending on the closure we give! 🎩✨

---

## 7. Making closures shorter

Swift lets you **remove** things it can guess. Watch the same closure get shorter:

```swift
let numbers = [5, 2, 8, 1]
```

**Step 1 — full form:**

```swift
let sorted1 = numbers.sorted(by: { (a: Int, b: Int) -> Bool in
    return a < b
})
```

**Step 2 — remove types** (Swift knows they're `Int` and `Bool`):

```swift
let sorted2 = numbers.sorted(by: { a, b in
    return a < b
})
```

**Step 3 — remove `return`** (only one line):

```swift
let sorted3 = numbers.sorted(by: { a, b in a < b })
```

**Step 4 — use `$0` and `$1`** (short names for the 1st and 2nd input):

```swift
let sorted4 = numbers.sorted(by: { $0 < $1 })
```

**Step 5 — trailing closure:**

```swift
let sorted5 = numbers.sorted { $0 < $1 }
```

All five give `[1, 2, 5, 8]`. ✅

| Short name | Means |
|---|---|
| `$0` | the **first** input |
| `$1` | the **second** input |
| `$2` | the third input… |

💡 **Tip:** Use `$0` only for **short, simple** closures. For longer code, real names are easier to read.

---

## 8. `map` — change every item

`map` makes a **new array** by changing **each** item.

```swift
let numbers = [1, 2, 3, 4]
let doubled = numbers.map { $0 * 2 }
print(doubled)
```

**Output:**

```
[2, 4, 6, 8]
```

| Part | Meaning |
|---|---|
| `numbers.map` | "Go through each item and change it." |
| `{ $0 * 2 }` | How to change: `$0` is the current item. Multiply by 2. |

```
[1, 2, 3, 4]
 ↓  ↓  ↓  ↓   × 2
[2, 4, 6, 8]
```

It can change the **type** too:

```swift
let names = ["ravi", "meena"]
let loud = names.map { $0.uppercased() }
let lengths = names.map { $0.count }
print(loud)
print(lengths)
```

**Output:**

```
["RAVI", "MEENA"]
[4, 5]
```

---

## 9. `filter` — keep only some items

`filter` keeps items where the closure says `true`.

```swift
let numbers = [1, 2, 3, 4, 5, 6]
let evens = numbers.filter { $0 % 2 == 0 }
print(evens)
```

**Output:**

```
[2, 4, 6]
```

| Part | Meaning |
|---|---|
| `numbers.filter` | "Keep only some items." |
| `{ $0 % 2 == 0 }` | Keep if the item is even (`true`). |

```
[1, 2, 3, 4, 5, 6]
 ✗  ✓  ✗  ✓  ✗  ✓
[   2,    4,    6]
```

```swift
let words = ["cat", "elephant", "dog", "giraffe"]
let longWords = words.filter { $0.count > 3 }
print(longWords)
```

**Output:**

```
["elephant", "giraffe"]
```

---

## 10. `reduce` — combine everything into one value

```swift
let numbers = [1, 2, 3, 4]
let total = numbers.reduce(0) { $0 + $1 }
print(total)
```

**Output:**

```
10
```

| Part | Meaning |
|---|---|
| `reduce(0)` | Start with `0`. |
| `$0` | The running total so far. |
| `$1` | The current item. |
| `$0 + $1` | New total = old total + item. |

Step by step:

| Item (`$1`) | Total before (`$0`) | New total |
|---|---|---|
| 1 | 0 | 1 |
| 2 | 1 | 3 |
| 3 | 3 | 6 |
| 4 | 6 | 10 |

Shortcut: `numbers.reduce(0, +)` does the same thing!

---

## 11. `forEach` — do something for each item

```swift
let fruits = ["🍎", "🍌", "🍇"]
fruits.forEach { print("I like \($0)") }
```

**Output:**

```
I like 🍎
I like 🍌
I like 🍇
```

It's like a `for` loop, but written as a closure.

---

## 12. Chaining them together 🔗

You can connect these tools one after another:

```swift
let scores = [45, 82, 67, 91, 38, 74]

let result = scores
    .filter { $0 >= 50 }      // keep passing scores
    .map { $0 + 5 }           // add 5 bonus points
    .sorted { $0 > $1 }       // biggest first

print(result)
```

**Output:**

```
[96, 87, 79, 72]
```

| Step | Result |
|---|---|
| Start | `[45, 82, 67, 91, 38, 74]` |
| `.filter { $0 >= 50 }` | `[82, 67, 91, 74]` |
| `.map { $0 + 5 }` | `[87, 72, 96, 79]` |
| `.sorted { $0 > $1 }` | `[96, 87, 79, 72]` |

---

## 13. Closures remember things (capturing)

Closures can **remember** variables from outside.

```swift
var counter = 0

let increment = {
    counter += 1
    print("Counter is \(counter)")
}

increment()
increment()
increment()
```

**Output:**

```
Counter is 1
Counter is 2
Counter is 3
```

The closure **captures** (holds on to) `counter` and can change it.

> 📖 **New word: Capture**
> When a closure uses and remembers a variable from outside itself.

That's actually where the name "closure" comes from — it "closes over" the variables around it. 📦

---

## 14. Mini project: student results 🎓

```swift
let students = ["Ravi": 78, "Meena": 92, "Arun": 45, "Priya": 66, "John": 30]

// 1. Names of students who passed (50 or more), A to Z
let passed = students
    .filter { $0.value >= 50 }
    .map { $0.key }
    .sorted()
print("Passed: \(passed)")

// 2. Class average
let total = students.values.reduce(0, +)
let average = Double(total) / Double(students.count)
print("Average: \(average)")

// 3. Top student
if let top = students.max(by: { $0.value < $1.value }) {
    print("Top student: \(top.key) with \(top.value)")
}
```

**Output:**

```
Passed: ["Meena", "Priya", "Ravi"]
Average: 62.2
Top student: Meena with 92
```

| Part | Meaning |
|---|---|
| `.filter { $0.value >= 50 }` | For a dictionary, each item has `.key` and `.value`. Keep if the mark is 50+. |
| `.map { $0.key }` | Keep only the names. |
| `.sorted()` | A to Z. |
| `students.values.reduce(0, +)` | Add all the marks. |
| `max(by: { $0.value < $1.value })` | Find the item with the biggest value. Returns an Optional (the dictionary might be empty), so we use `if let`. |

---

## 🏋️ Practice

1. Make a closure `let greet = { (name: String) in print("Hi, \(name)") }`. Call it with your name.
2. Use `map` to turn `[1, 2, 3, 4, 5]` into their squares: `[1, 4, 9, 16, 25]`.
3. Use `filter` to keep only names longer than 4 letters from `["Ravi", "Meena", "Jo", "Priya"]`.
4. Use `reduce` to multiply all numbers in `[1, 2, 3, 4, 5]` together. (Hint: start with `1`, not `0`!)
5. Sort `["banana", "kiwi", "apple"]` by **length** (shortest first) using `sorted { }`.
6. Write a function `func repeatAction(times: Int, action: () -> Void)` that runs `action` `times` times. Call it with a trailing closure.

<details>
<summary>Click to see the answers</summary>

```swift
// 1
let greet = { (name: String) in
    print("Hi, \(name)")
}
greet("Ravi")

// 2
let squares = [1, 2, 3, 4, 5].map { $0 * $0 }
print(squares)

// 3
let longNames = ["Ravi", "Meena", "Jo", "Priya"].filter { $0.count > 4 }
print(longNames)   // ["Meena", "Priya"]

// 4
let product = [1, 2, 3, 4, 5].reduce(1) { $0 * $1 }
print(product)     // 120

// 5
let byLength = ["banana", "kiwi", "apple"].sorted { $0.count < $1.count }
print(byLength)    // ["kiwi", "apple", "banana"]

// 6
func repeatAction(times: Int, action: () -> Void) {
    for _ in 1...times {
        action()
    }
}
repeatAction(times: 3) {
    print("Clap! 👏")
}
```

</details>

---

## 🧠 Remember

- A **closure** is a block of code `{ }` you can store or pass around.
- Form: `{ (inputs) -> Output in code }`.
- **Trailing closure**: put the last closure after `()` → `doTwice { ... }`. SwiftUI uses this everywhere.
- `$0`, `$1` = short names for inputs.
- `map` changes each item. `filter` keeps some items. `reduce` combines into one. `sorted { }` sorts your way.

---

## 🎉 Part 2 complete!

Amazing work! You now know the **core of Swift**:

- Variables, constants and types
- Math and text
- `if`, `switch`, loops
- Arrays, dictionaries, sets
- Optionals
- Functions and closures

That is a LOT. Be proud! 🏆

In **Part 3**, you will learn to build your **own types** with `struct`, `class`, `enum` and more. This is how real apps organize their code.

---

⬅️ **Back:** [Chapter 18 — Functions](18-functions.md)
➡️ **Next:** [Chapter 20 — Structs](../part-03-building-types/20-structs.md)
