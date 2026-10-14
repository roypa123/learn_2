# Chapter 17 — Maybe There, Maybe Not: Optionals

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What an **Optional** is and why Swift has them.
- What `nil` means.
- 5 ways to safely open an Optional:
  1. `if let`
  2. `guard let`
  3. `??` (default value)
  4. `?.` (optional chaining)
  5. `!` (force unwrap — dangerous!)

🧠 This is one of the **most important** chapters. Swift and SwiftUI use Optionals **everywhere**. Take your time.

---

## 1. The problem

Earlier we saw some strange things:

```swift
print(Int("42"))           // Optional(42)
print(["a": 1]["b"])       // nil
print([Int]().first)       // nil
```

Why? Because sometimes there is **no answer**:

- `Int("hello")` → "hello" is not a number. No answer!
- `["a": 1]["b"]` → there is no key `"b"`. No answer!
- An empty array has no `first` item. No answer!

Swift needs a way to say: **"there might be a value, or there might be nothing."**

---

## 2. What is an Optional? 🎁

Think of a **gift box**:

```
   ┌───────────┐            ┌───────────┐
   │    🎁     │            │    🎁     │
   │  [ 42 ]   │            │  [     ]  │
   └───────────┘            └───────────┘
   Box with a value         Empty box (nil)
```

You can't see inside the box until you **open** it.

> 📖 **New word: Optional**
> A box that **might** contain a value, or might be **empty**.

> 📖 **New word: nil**
> Means "**nothing**" — the box is empty.

> 📖 **New word: Unwrap**
> To **open** the box and take out the value (if there is one).

---

## 3. Making an Optional

Add a `?` after the type:

```swift
var middleName: String? = nil
print(middleName)

middleName = "Kumar"
print(middleName)
```

**Output:**

```
nil
Optional("Kumar")
```

| Part | Meaning |
|---|---|
| `String?` | "A box that might hold a `String`, or might be empty." |
| `= nil` | Start with an empty box. |
| `middleName = "Kumar"` | Now put `"Kumar"` in the box. |
| `Optional("Kumar")` | Swift shows it's still **inside the box**. |

Not everybody has a middle name — that's why it's optional! 😊

⚠️ **Careful:** A normal type **cannot** be `nil`:

```swift
var name: String = nil   // ❌ ERROR: 'nil' cannot initialize specified type 'String'
```

This is Swift's **safety**: if a type has no `?`, it **always** has a value. You never need to worry.

---

## 4. You can't use an Optional directly

```swift
let input = "5"
let number = Int(input)   // number is Int? (Optional Int)
print(number + 1)         // ❌ ERROR
```

**Error:**

```
error: value of optional type 'Int?' must be unwrapped to a value of type 'Int'
```

Meaning: *"You can't add 1 to a box. Open the box first!"*

So how do we open it? Here are the ways. 👇

---

## 5. Way 1: `if let` ⭐ (most common)

```swift
let input = "5"

if let number = Int(input) {
    print("The number is \(number)")
    print("Plus one: \(number + 1)")
} else {
    print("That is not a number.")
}
```

**Output:**

```
The number is 5
Plus one: 6
```

| Part | Meaning |
|---|---|
| `if let` | "If the box has something inside…" |
| `number` | "…take it out and call it `number`." |
| `= Int(input)` | The box to open. |
| First `{ }` | Runs if there **was** a value. Here `number` is a normal `Int`. |
| `else { }` | Runs if the box was **empty** (`nil`). |

Now try with `let input = "hello"`:

**Output:**

```
That is not a number.
```

### Short form (Swift 5.7+)

If the Optional already has a name, you can write:

```swift
let nickname: String? = "Rocky"

if let nickname {
    print("Hi, \(nickname)!")
}
```

**Output:**

```
Hi, Rocky!
```

`if let nickname` is short for `if let nickname = nickname`.
Inside the `{ }`, `nickname` is a normal `String`.

⚠️ **Careful:** The unwrapped value only exists **inside** the `{ }`.

```swift
if let n = Int("5") {
    print(n)   // ✅ works
}
print(n)       // ❌ ERROR: cannot find 'n' in scope
```

---

## 6. Way 2: `guard let`

`guard` is like `if let`, but **upside down**:
*"Make sure there's a value. If not, leave now."*

`guard` is used inside **functions**. We learn functions in the next chapter, so here is a quick preview:

```swift
func greet(name: String?) {
    guard let name else {
        print("No name given.")
        return
    }
    print("Hello, \(name)!")
}

greet(name: "Meena")
greet(name: nil)
```

**Output:**

```
Hello, Meena!
No name given.
```

| Part | Meaning |
|---|---|
| `func greet(...)` | A function (Chapter 18). |
| `guard let name` | "Make sure `name` has a value." |
| `else { ... return }` | If **not**, run this and **leave** the function (`return`). |
| `print("Hello, \(name)!")` | After `guard`, `name` is a normal `String` — for the **rest** of the function. |

| | `if let` | `guard let` |
|---|---|---|
| Unwrapped value is usable… | only **inside** `{ }` | **after** the guard, until the end of the function |
| The `else` must… | (anything) | **leave** (`return`, `break`, …) |
| Good for… | "do something if there's a value" | "stop early if there's no value" |

💡 **Tip:** `guard` keeps your code flat and clean. You'll use it a lot in real apps.

---

## 7. Way 3: `??` — default value ⭐

"Use the value in the box. If the box is empty, use **this** instead."

```swift
let savedName: String? = nil
let name = savedName ?? "Guest"
print("Welcome, \(name)!")
```

**Output:**

```
Welcome, Guest!
```

| Part | Meaning |
|---|---|
| `savedName` | An Optional (here it's `nil`). |
| `??` | "If empty, use…" |
| `"Guest"` | …this default value. |
| `name` | A normal `String`, never `nil`. |

```swift
let input = "abc"
let number = Int(input) ?? 0
print(number)   // 0, because "abc" is not a number
```

> 📖 **New word: Nil-coalescing operator**
> The fancy name for `??`. You don't need to remember the name — just how it works!

---

## 8. Way 4: `?.` — optional chaining

Use `?.` to do something with an Optional **only if** it has a value.

```swift
let word: String? = "hello"
print(word?.uppercased())

let empty: String? = nil
print(empty?.uppercased())
```

**Output:**

```
Optional("HELLO")
nil
```

| Part | Meaning |
|---|---|
| `word?.uppercased()` | "If `word` has a value, call `uppercased()` on it. If it's `nil`, just give `nil`." |

The result is **still an Optional**. Often we combine it with `??`:

```swift
let empty: String? = nil
let result = empty?.uppercased() ?? "NO WORD"
print(result)
```

**Output:**

```
NO WORD
```

Example with an array:

```swift
let names: [String] = []
print(names.first?.count ?? 0)
```

**Output:**

```
0
```

"If there is a first name, give its letter count. Otherwise 0."

---

## 9. Way 5: `!` — force unwrap ⚠️ (dangerous)

`!` says: *"I am 100% sure the box is not empty. Open it!"*

```swift
let number = Int("42")!
print(number + 1)
```

**Output:**

```
43
```

But if you are **wrong**:

```swift
let number = Int("hello")!   // 💥 CRASH
```

**Error:**

```
Fatal error: Unexpectedly found nil while unwrapping an Optional value
```

The whole program **crashes**. In a real app, the app closes suddenly. Users hate that! 😡

🧠 **Remember:** Avoid `!`. Use `if let`, `guard let` or `??` instead. Use `!` only when it is **truly impossible** to be `nil`.

💡 **Tip:** Think of `!` as a warning sign ⚠️. Every time you write it, ask yourself: *"Am I really, really sure?"*

---

## 10. Which way should I use?

| Situation | Use |
|---|---|
| Do something only if there's a value | `if let` |
| Stop early in a function if there's no value | `guard let` |
| Use a backup value if empty | `??` |
| Call a method only if there's a value | `?.` |
| 100% sure it's not empty (rare!) | `!` |

---

## 11. Checking for nil directly

You can compare with `nil`:

```swift
let email: String? = nil

if email == nil {
    print("Please add your email.")
}
```

**Output:**

```
Please add your email.
```

But usually `if let` is better, because you also get the value.

---

## 12. Mini project: age checker 🎂

```swift
let inputs = ["25", "abc", "12", "", "70"]

for text in inputs {
    if let age = Int(text) {
        if age >= 18 {
            print("\(age): adult")
        } else {
            print("\(age): child")
        }
    } else {
        print("'\(text)': not a valid age")
    }
}
```

**Output:**

```
25: adult
'abc': not a valid age
12: child
'': not a valid age
70: adult
```

| Line | Meaning |
|---|---|
| `for text in inputs` | Go through each text. |
| `if let age = Int(text)` | Try to turn the text into a number. If it works, call it `age`. |
| `if age >= 18` | Normal check — `age` is a real `Int` here. |
| `else` (outer) | The text was not a number (`"abc"` and `""`). |

---

## 🏋️ Practice

1. Make `var favoriteColor: String? = nil`. Print it. Then set it to `"blue"` and print it again.
2. Use `if let` to convert `"100"` to an `Int` and print double the number.
3. Use `??` to convert `"oops"` to an `Int`, with a default of `-1`.
4. Make `let city: String? = nil`. Print `city?.count ?? 0`.
5. What happens with `let x = Int("seven")!`? Why? How can you fix it safely?
6. Loop through `["3", "x", "7"]`, convert each to `Int` with `?? 0`, and add them all up.

<details>
<summary>Click to see the answers</summary>

```swift
// 1
var favoriteColor: String? = nil
print(favoriteColor)          // nil
favoriteColor = "blue"
print(favoriteColor)          // Optional("blue")

// 2
if let n = Int("100") {
    print(n * 2)              // 200
}

// 3
let value = Int("oops") ?? -1
print(value)                  // -1

// 4
let city: String? = nil
print(city?.count ?? 0)       // 0

// 5
// Crash: "seven" is not digits, so Int("seven") is nil, and ! crashes on nil.
// Safe fix:
let x = Int("seven") ?? 0

// 6
var total = 0
for text in ["3", "x", "7"] {
    total += Int(text) ?? 0
}
print(total)                  // 10
```

</details>

---

## 🧠 Remember

- `Type?` = an Optional: might have a value, might be `nil`.
- You must **unwrap** an Optional before using it.
- `if let x = optional { }` → safe and common.
- `guard let x = optional else { return }` → stop early.
- `optional ?? default` → backup value.
- `optional?.something` → only if it has a value.
- `optional!` → crashes if `nil`. **Avoid it.**

---

⬅️ **Back:** [Chapter 16 — Sets](16-sets.md)
➡️ **Next:** [Chapter 18 — Functions](18-functions.md)
