# Chapter 06 — Variables and Constants (`var` and `let`)

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- How to **store** information with a name.
- What `var` (variable) means.
- What `let` (constant) means.
- When to use which one.
- Rules for good names.

---

## 1. Why do we need to store things?

Imagine a game. The player's score starts at 0. Then it becomes 10. Then 25.

The computer must **remember** the score somewhere.
We need a **box** with a **label** on it.

```
   ┌─────────┐
   │   25    │   ← the value inside
   └─────────┘
      score       ← the label (name)
```

In Swift, this box is called a **variable** or a **constant**.

---

## 2. Making a variable with `var`

```swift
var score = 0
print(score)
```

**Output:**

```
0
```

Let's look at **every part** of the first line:

| Part | What it means |
|---|---|
| `var` | Short for **variable**. It means: "Make a new box. Its value **can change** later." |
| `score` | The **name** (label) of the box. You choose this name. |
| `=` | "Put this value into the box." |
| `0` | The value we put in the box. |

And the second line:

| Part | What it means |
|---|---|
| `print(score)` | Show what is **inside** the box called `score`. |

⚠️ **Careful:** `print(score)` has **no quotes**. We want the **value inside** the box, not the word "score".

```swift
var score = 0
print(score)     // shows: 0      (the value inside)
print("score")   // shows: score  (just the text)
```

> 📖 **New word: Variable**
> A variable is a named box that stores a value. The value **can change**.

> 📖 **New word: Value**
> The thing stored inside the box. Example: `0`, `25`, `"Ravi"`.

---

## 3. Changing a variable

```swift
var score = 0
print(score)

score = 10
print(score)

score = 25
print(score)
```

**Output:**

```
0
10
25
```

Line by line:

| Line | What happens | Box now contains |
|---|---|---|
| `var score = 0` | Make a box called `score`, put `0` in it. | `0` |
| `print(score)` | Show the value. | `0` |
| `score = 10` | Throw away the old value. Put `10` in. | `10` |
| `print(score)` | Show the value. | `10` |
| `score = 25` | Throw away the old value. Put `25` in. | `25` |
| `print(score)` | Show the value. | `25` |

⚠️ **Careful:** We write `var` **only the first time**, when we **make** the box.
After that, we just use the name.

```swift
var score = 0
var score = 10   // ❌ ERROR: invalid redeclaration of 'score'
score = 10       // ✅ correct
```

The error `invalid redeclaration` means: *"You already made a box called `score`. You can't make it again."*

---

## 4. Making a constant with `let`

Some things **never change**. Your birthday. The number of days in a week.

For these, we use `let`.

```swift
let daysInWeek = 7
print(daysInWeek)
```

**Output:**

```
7
```

| Part | What it means |
|---|---|
| `let` | "Make a new box. Its value can **never** change." |
| `daysInWeek` | The name of the box. |
| `=` | "Put this value in." |
| `7` | The value. |

> 📖 **New word: Constant**
> A constant is a named box whose value **cannot change** after you set it.

Now try to change it:

```swift
let daysInWeek = 7
daysInWeek = 8   // ❌ ERROR
```

**Error:**

```
error: cannot assign to value: 'daysInWeek' is a 'let' constant
```

| Part of error | Meaning |
|---|---|
| `cannot assign to value` | You can't put a new value in. |
| `'daysInWeek' is a 'let' constant` | Because you made it with `let`. |

Good! Swift **protects** you. Nobody can change it by mistake. 🛡️

---

## 5. `var` or `let` — which one?

| Use | When | Example |
|---|---|---|
| `let` | The value will **not** change. | your name, birth year, number of days in a week |
| `var` | The value **will** change. | score, age, money in a bank account |

🧠 **Remember:** Always start with `let`. Change it to `var` only if you need to change the value.

💡 **Tip:** If you use `var` but never change the value, Swift gives a friendly **warning**:
`variable 'x' was never mutated; consider changing to 'let' constant`.
It means: *"You never changed this. Use `let` instead."*
A warning is not an error — your code still runs.

---

## 6. Storing text

Boxes can hold text (strings) too.

```swift
let name = "Ravi"
var city = "Chennai"

print(name)
print(city)

city = "Mumbai"
print(city)
```

**Output:**

```
Ravi
Chennai
Mumbai
```

| Line | What happens |
|---|---|
| `let name = "Ravi"` | Make a constant `name`, store the text `Ravi`. |
| `var city = "Chennai"` | Make a variable `city`, store `Chennai`. |
| `print(name)` | Shows `Ravi`. |
| `print(city)` | Shows `Chennai`. |
| `city = "Mumbai"` | Change `city` to `Mumbai`. Allowed, because it is `var`. |
| `print(city)` | Shows `Mumbai`. |

---

## 7. Using one box to fill another

```swift
let price = 50
let quantity = 3
let total = price * quantity
print(total)
```

**Output:**

```
150
```

| Line | What happens |
|---|---|
| `let price = 50` | Box `price` holds `50`. |
| `let quantity = 3` | Box `quantity` holds `3`. |
| `let total = price * quantity` | Swift looks inside `price` (50) and `quantity` (3). `*` means **multiply**. 50 × 3 = 150. Box `total` holds `150`. |
| `print(total)` | Shows `150`. |

---

## 8. Using a variable to change itself

```swift
var coins = 10
coins = coins + 5
print(coins)
```

**Output:**

```
15
```

The line `coins = coins + 5` looks strange. Let's read it **from right to left**:

1. `coins + 5` → look inside `coins` (10), add 5 → **15**.
2. `coins = ...` → put **15** back into `coins`.

💡 **Tip:** In Swift, `=` does **not** mean "is equal to" like in school math.
It means **"put the value on the right into the box on the left."**

---

## 9. Rules for names

### Names Swift allows ✅

| Name | OK? |
|---|---|
| `score` | ✅ |
| `playerName` | ✅ |
| `level2` | ✅ |
| `_hidden` | ✅ |

### Names Swift does NOT allow ❌

| Name | Problem |
|---|---|
| `2level` | Cannot **start** with a number. |
| `player name` | Cannot have **spaces**. |
| `player-name` | `-` means minus. Not allowed in names. |
| `var` | `var` is a special Swift word. You can't use it as a name. |

### Good style: camelCase 🐫

When a name has many words, Swift programmers write it like this:

- First word: all **small** letters.
- Each next word: starts with a **Capital** letter.
- No spaces.

| Words | camelCase name |
|---|---|
| player name | `playerName` |
| high score | `highScore` |
| number of lives left | `numberOfLivesLeft` |

It is called **camelCase** because the capital letters look like the humps of a camel 🐫.

### Choose names that explain

```swift
let x = 18           // ❌ What is x? Nobody knows.
let votingAge = 18   // ✅ Clear!
```

---

## 10. Common mistakes

| Wrong ❌ | Problem | Correct ✅ |
|---|---|---|
| `print(scroe)` | Spelling mistake. Swift says `cannot find 'scroe' in scope`. | `print(score)` |
| `Score = 5` (box is `score`) | Big `S`. Names are case-sensitive. | `score = 5` |
| `let age = 10` then `age = 11` | Can't change a `let`. | Use `var age = 10` |
| Using a box before making it | `print(total)` then `let total = 5` → error. Order matters! | Make the box first. |

---

## 🏋️ Practice

1. Make a constant `myName` with your name. Print it.
2. Make a variable `age` with your age. Print it. Then add 1 to it (`age = age + 1`) and print it again.
3. Make constants `apples = 4` and `oranges = 6`. Make a constant `fruits` that adds them. Print `fruits`.
4. Try to change `myName` to something else. Read the error. Why does it happen?
5. Which should be `let` and which `var`? (a) your country (b) your bank balance (c) the number of hours in a day (d) the temperature outside.

<details>
<summary>Click to see the answers</summary>

```swift
// 1
let myName = "Ravi"
print(myName)

// 2
var age = 10
print(age)
age = age + 1
print(age)

// 3
let apples = 4
let oranges = 6
let fruits = apples + oranges
print(fruits)   // 10

// 4
// myName = "Arun"   → error, because myName is a 'let' constant
```

5. (a) `let` (b) `var` (c) `let` (d) `var`

</details>

---

## 🧠 Remember

- `var` = a box whose value **can change**.
- `let` = a box whose value **cannot change**.
- Use `let` first. Use `var` only when needed.
- `=` means "put the right side into the box on the left".
- Use clear **camelCase** names.

---

⬅️ **Back:** [Chapter 05 — Comments](../part-01-getting-started/05-comments.md)
➡️ **Next:** [Chapter 07 — Data Types](07-data-types.md)
