# Chapter 07 — Data Types: Numbers, Text, True/False

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What a **type** is.
- The 4 most common types: `Int`, `Double`, `String`, `Bool`.
- How Swift **guesses** the type.
- How to **write** the type yourself.
- How to **change** one type into another.

---

## 1. What is a type?

In a kitchen, you keep things in the right container:

- Water goes in a **bottle** 🍼.
- Eggs go in an **egg box** 🥚.
- Rice goes in a **bag** 🛍️.

You can't put water in an egg box!

In Swift, every value has a **type**. The type says **what kind of thing** it is.

> 📖 **New word: Type (or Data type)**
> The **kind** of a value. Is it a whole number? A decimal number? Text? Yes/No?

---

## 2. The four main types

| Type | What it holds | Examples |
|---|---|---|
| `Int` | Whole numbers (no dot) | `0`, `7`, `-3`, `2026` |
| `Double` | Numbers with a decimal point | `3.14`, `0.5`, `-2.75`, `99.0` |
| `String` | Text | `"Hello"`, `"Ravi"`, `"123"` |
| `Bool` | Only `true` or `false` | `true`, `false` |

Let's look at each one.

---

## 3. `Int` — whole numbers

```swift
let apples = 5
let temperature = -3
print(apples)
print(temperature)
```

**Output:**

```
5
-3
```

| Part | Meaning |
|---|---|
| `let apples = 5` | `5` has no decimal point → Swift makes `apples` an `Int`. |
| `let temperature = -3` | Negative whole numbers are also `Int`. |

> 📖 **New word: Int**
> Short for **Integer**. A whole number: no dot, no fraction.

Use `Int` for things you **count**: people, apples, lives, levels.

---

## 4. `Double` — decimal numbers

```swift
let price = 49.99
let height = 1.65
print(price)
print(height)
```

**Output:**

```
49.99
1.65
```

| Part | Meaning |
|---|---|
| `49.99` | Has a decimal point `.` → Swift makes `price` a `Double`. |

> 📖 **New word: Double**
> A number that can have a **decimal part**. Like `2.5` or `0.75`.

Use `Double` for things you **measure**: money, weight, height, distance.

⚠️ **Careful:** `5` is an `Int`. `5.0` is a `Double`. They look similar but they are **different types**.

---

## 5. `String` — text

```swift
let greeting = "Good morning"
let phone = "9876543210"
print(greeting)
print(phone)
```

**Output:**

```
Good morning
9876543210
```

| Part | Meaning |
|---|---|
| `"Good morning"` | In quotes → `String`. |
| `"9876543210"` | Also in quotes → `String`, **not** a number! |

💡 **Tip:** Why is a phone number a `String`? Because we never do math with it. We never add two phone numbers! Also, a phone number can start with `0` or have `+`.

---

## 6. `Bool` — true or false

```swift
let isRaining = true
let hasPassword = false
print(isRaining)
print(hasPassword)
```

**Output:**

```
true
false
```

| Part | Meaning |
|---|---|
| `true` | Means **yes**. No quotes! |
| `false` | Means **no**. No quotes! |

> 📖 **New word: Bool**
> Short for **Boolean** (named after a man called George Boole). It can only be `true` or `false`. Like a light switch: ON or OFF 💡.

Use `Bool` for yes/no questions: Is the game over? Is the user logged in? Is the light on?

💡 **Tip:** Good `Bool` names sound like questions: `isOpen`, `hasKey`, `canFly`, `isGameOver`.

⚠️ **Careful:** `true` and `"true"` are different!

```swift
let a = true     // Bool
let b = "true"   // String (just text)
```

---

## 7. Swift guesses the type (type inference)

When you write `let apples = 5`, you did not say "Int". Swift **guessed** it.

> 📖 **New word: Type inference**
> When Swift **looks at the value** and decides the type by itself.

| You write | Swift decides |
|---|---|
| `let a = 10` | `Int` |
| `let b = 10.5` | `Double` |
| `let c = "10"` | `String` |
| `let d = true` | `Bool` |

---

## 8. Writing the type yourself (type annotation)

You can also **tell** Swift the type. Use a colon `:` after the name.

```swift
let age: Int = 12
let weight: Double = 35.5
let name: String = "Meena"
let isStudent: Bool = true
```

Look at the first line:

| Part | Meaning |
|---|---|
| `let` | Make a constant. |
| `age` | Its name. |
| `:` | "The type is…" |
| `Int` | …whole number. |
| `= 12` | Put `12` inside. |

Read it like English: *"Let age, which is an Int, be 12."*

> 📖 **New word: Type annotation**
> Writing the type yourself, with `: Type`.

### When is this useful?

**Case 1:** You want a `Double`, but you wrote a whole number.

```swift
let speed = 60           // Swift guesses Int
let speed2: Double = 60  // Now it is a Double (60.0)
print(speed)
print(speed2)
```

**Output:**

```
60
60.0
```

**Case 2:** You make a box now but fill it later.

```swift
let message: String
message = "Welcome!"
print(message)
```

| Line | Meaning |
|---|---|
| `let message: String` | Make an empty box for text. No value yet. |
| `message = "Welcome!"` | Fill it now (only once, because it is `let`). |
| `print(message)` | Shows `Welcome!`. |

---

## 9. A box keeps its type forever

Once a box has a type, it **cannot** hold a different type.

```swift
var score = 10        // score is Int
score = 20            // ✅ OK, still an Int
score = "twenty"      // ❌ ERROR
```

**Error:**

```
error: cannot assign value of type 'String' to type 'Int'
```

Meaning: *"This box is for whole numbers. You can't put text in it."*

🧠 **Remember:** A box's type is decided **once** and never changes. Swift is a **type-safe** language. This stops many bugs.

---

## 10. Mixing types — not allowed directly

```swift
let a = 5      // Int
let b = 2.5    // Double
let c = a + b  // ❌ ERROR
```

**Error:**

```
error: binary operator '+' cannot be applied to operands of type 'Int' and 'Double'
```

Meaning: *"I can't add an `Int` and a `Double` directly."*

Swift doesn't want to guess what you want. So you must **convert**.

---

## 11. Converting types

You convert by writing the **type name** with the value in brackets.

### Int → Double

```swift
let a = 5
let b = 2.5
let c = Double(a) + b
print(c)
```

**Output:**

```
7.5
```

| Part | Meaning |
|---|---|
| `Double(a)` | Take the value of `a` (5) and make it a `Double` (5.0). |
| `+ b` | 5.0 + 2.5 = 7.5. Now both are `Double`, so it works. |

### Double → Int

```swift
let price = 9.99
let rounded = Int(price)
print(rounded)
```

**Output:**

```
9
```

⚠️ **Careful:** `Int(9.99)` gives `9`, **not** `10`. It just **cuts off** the decimal part. It does not round.

### Number → String

```swift
let age = 12
let text = String(age)
print("I am " + text)
```

**Output:**

```
I am 12
```

| Part | Meaning |
|---|---|
| `String(age)` | Turn the number `12` into the text `"12"`. |
| `"I am " + text` | `+` with two strings **joins** them: `"I am 12"`. |

### String → Int

```swift
let input = "42"
let number = Int(input)
print(number)
```

**Output:**

```
Optional(42)
```

Hmm, what is `Optional(42)`? 🤔

Text might not be a number. What is `Int("hello")`? It can't work!
So Swift says: *"Maybe I got a number, maybe not."* This is called an **Optional**.

We learn about Optionals in **Chapter 17**. For now, just know this is normal.

---

## 12. Checking the type

Want to know a box's type? Use `type(of:)`.

```swift
let x = 3.0
print(type(of: x))
```

**Output:**

```
Double
```

| Part | Meaning |
|---|---|
| `type(of: x)` | Ask Swift: "What type is `x`?" |

---

## 🏋️ Practice

1. What type is each? (a) `42` (b) `"42"` (c) `4.2` (d) `false` (e) `"false"`
2. Make a constant `pi` with type `Double` and value `3.14`. Print it.
3. Make `let books = 3` and `let pricePerBook = 120.5`. Calculate the total price. (Hint: you need to convert!)
4. Make `var lives = 3`. Try to put `"three"` in it. Read the error.
5. Print the type of `true` using `type(of:)`.

<details>
<summary>Click to see the answers</summary>

1. (a) `Int` (b) `String` (c) `Double` (d) `Bool` (e) `String`

```swift
// 2
let pi: Double = 3.14
print(pi)

// 3
let books = 3
let pricePerBook = 120.5
let total = Double(books) * pricePerBook
print(total)   // 361.5

// 4
var lives = 3
// lives = "three"   → error: cannot assign value of type 'String' to type 'Int'

// 5
print(type(of: true))   // Bool
```

</details>

---

## 🧠 Remember

| Type | Holds | Example |
|---|---|---|
| `Int` | whole numbers | `7` |
| `Double` | decimal numbers | `7.5` |
| `String` | text | `"seven"` |
| `Bool` | true/false | `true` |

- Swift **guesses** the type, or you write it with `: Type`.
- A box's type **never changes**.
- To mix types, **convert**: `Double(x)`, `Int(x)`, `String(x)`.

---

⬅️ **Back:** [Chapter 06 — Variables and Constants](06-variables-and-constants.md)
➡️ **Next:** [Chapter 08 — Doing Math](08-doing-math.md)
