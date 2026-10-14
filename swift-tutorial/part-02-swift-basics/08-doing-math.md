# Chapter 08 — Doing Math

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- The math signs: `+`, `-`, `*`, `/`, `%`.
- Why `7 / 2` gives `3` (and how to get `3.5`).
- Shortcuts like `+=`.
- Which math happens first.
- Comparing numbers: `>`, `<`, `==` and more.

---

## 1. The math signs

> 📖 **New word: Operator**
> A sign that does something with values. `+` is an operator.

| Operator | Name | Example | Result |
|---|---|---|---|
| `+` | add | `5 + 2` | `7` |
| `-` | subtract | `5 - 2` | `3` |
| `*` | multiply | `5 * 2` | `10` |
| `/` | divide | `10 / 2` | `5` |
| `%` | remainder | `5 % 2` | `1` |

⚠️ **Careful:** Multiply is `*` (star), **not** `x`. Divide is `/` (slash), **not** `÷`.

---

## 2. Adding, subtracting, multiplying

```swift
let a = 10
let b = 3

print(a + b)
print(a - b)
print(a * b)
```

**Output:**

```
13
7
30
```

| Line | Calculation | Result |
|---|---|---|
| `print(a + b)` | 10 + 3 | `13` |
| `print(a - b)` | 10 − 3 | `7` |
| `print(a * b)` | 10 × 3 | `30` |

---

## 3. Dividing — a surprise!

```swift
print(7 / 2)
```

**Output:**

```
3
```

What? 7 ÷ 2 should be 3.5! 😮

Here is why:

- `7` is an `Int`. `2` is an `Int`.
- An `Int` divided by an `Int` gives an **`Int`**.
- An `Int` can't have a decimal part, so Swift **throws away** the `.5`.

> 📖 **New word: Integer division**
> When you divide two `Int`s, the answer is a whole number. The decimal part is dropped.

### How to get 3.5

Use `Double`s:

```swift
print(7.0 / 2.0)
```

**Output:**

```
3.5
```

Or convert:

```swift
let total = 7
let people = 2
let each = Double(total) / Double(people)
print(each)
```

**Output:**

```
3.5
```

| Part | Meaning |
|---|---|
| `Double(total)` | 7 → 7.0 |
| `Double(people)` | 2 → 2.0 |
| `/` | 7.0 ÷ 2.0 = 3.5 |

🧠 **Remember:** `Int / Int` = `Int` (no decimals). Use `Double` if you need decimals.

---

## 4. Remainder `%`

`%` gives what is **left over** after dividing.

Imagine 7 sweets 🍬 and 2 children. Each child gets 3. **1 is left over.**

```swift
print(7 % 2)
```

**Output:**

```
1
```

More examples:

| Code | Think | Result |
|---|---|---|
| `10 % 3` | 10 sweets, 3 kids: each gets 3, left over 1 | `1` |
| `12 % 4` | 12 sweets, 4 kids: each gets 3, left over 0 | `0` |
| `5 % 7` | 5 sweets, 7 kids: nobody gets one, left over 5 | `5` |

💡 **Tip:** `%` is very useful to check if a number is **even** or **odd**:
- `number % 2` is `0` → even.
- `number % 2` is `1` → odd.

---

## 5. Which math happens first?

```swift
print(2 + 3 * 4)
```

**Output:**

```
14
```

Not 20! Why?

Just like in school math, `*` and `/` happen **before** `+` and `-`.

1. First: `3 * 4` = `12`
2. Then: `2 + 12` = `14`

### Use brackets to choose the order

```swift
print((2 + 3) * 4)
```

**Output:**

```
20
```

1. First the brackets: `2 + 3` = `5`
2. Then: `5 * 4` = `20`

| Order | What |
|---|---|
| 1st | `( )` brackets |
| 2nd | `*`, `/`, `%` |
| 3rd | `+`, `-` |

💡 **Tip:** If you are not sure, **use brackets**. They make code easier to read too.

---

## 6. Shortcuts: `+=`, `-=`, `*=`, `/=`

Changing a variable is very common:

```swift
var score = 10
score = score + 5
```

Swift has a **shortcut**:

```swift
var score = 10
score += 5
print(score)
```

**Output:**

```
15
```

| Part | Meaning |
|---|---|
| `score += 5` | Same as `score = score + 5`. "Add 5 to score." |

All shortcuts:

| Shortcut | Same as | Meaning |
|---|---|---|
| `x += 3` | `x = x + 3` | add 3 to x |
| `x -= 3` | `x = x - 3` | subtract 3 from x |
| `x *= 3` | `x = x * 3` | multiply x by 3 |
| `x /= 3` | `x = x / 3` | divide x by 3 |

### Example: a game

```swift
var lives = 3
lives -= 1      // hit by an enemy
print(lives)
lives += 1      // found a heart
print(lives)
```

**Output:**

```
2
3
```

⚠️ **Careful:** Some languages have `x++` to add 1. **Swift does not.** Use `x += 1`.

---

## 7. Comparing numbers

> 📖 **New word: Comparison**
> Checking two values against each other. The answer is always a `Bool` (`true` or `false`).

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `==` | is equal to | `5 == 5` | `true` |
| `!=` | is NOT equal to | `5 != 3` | `true` |
| `>` | is greater than | `5 > 3` | `true` |
| `<` | is less than | `5 < 3` | `false` |
| `>=` | is greater than or equal to | `5 >= 5` | `true` |
| `<=` | is less than or equal to | `4 <= 5` | `true` |

```swift
let age = 15
print(age >= 18)
print(age == 15)
```

**Output:**

```
false
true
```

| Line | Question | Answer |
|---|---|---|
| `age >= 18` | Is 15 greater than or equal to 18? | `false` |
| `age == 15` | Is 15 equal to 15? | `true` |

⚠️ **Careful:** `=` and `==` are very different!

| Sign | Meaning |
|---|---|
| `=` | **Put** a value in a box. |
| `==` | **Ask**: are these equal? |

You can store the answer in a box:

```swift
let age = 20
let canVote = age >= 18
print(canVote)
```

**Output:**

```
true
```

`canVote` is a `Bool`, because comparisons give `true` or `false`.

---

## 8. Useful number helpers

```swift
print(abs(-7))       // 7   → distance from zero (removes minus)
print(max(4, 9))     // 9   → the bigger one
print(min(4, 9))     // 4   → the smaller one
```

**Output:**

```
7
9
4
```

### Rounding Doubles

```swift
let x = 2.6
print(x.rounded())   // 3.0  → nearest whole number
```

| Part | Meaning |
|---|---|
| `x.rounded()` | Round `x` to the nearest whole number. `2.6` → `3.0`. |

The `.` (dot) means "use something that belongs to `x`". We will learn more about this later.

---

## 9. A tiny project: shopping bill 🧾

```swift
let pricePerPen = 12.5
let pens = 4
let discount = 5.0

let subtotal = pricePerPen * Double(pens)
let total = subtotal - discount

print("Subtotal:", subtotal)
print("Discount:", discount)
print("Total:", total)
```

**Output:**

```
Subtotal: 50.0
Discount: 5.0
Total: 45.0
```

| Line | What happens |
|---|---|
| `let pricePerPen = 12.5` | One pen costs 12.5 (a `Double`). |
| `let pens = 4` | We buy 4 pens (an `Int`). |
| `let discount = 5.0` | We get 5.0 off. |
| `let subtotal = pricePerPen * Double(pens)` | Convert 4 → 4.0, then 12.5 × 4.0 = 50.0. |
| `let total = subtotal - discount` | 50.0 − 5.0 = 45.0. |
| The `print` lines | Show each value with a label. |

---

## 🏋️ Practice

1. Print the result of `17 / 5` and `17 % 5`. Explain both answers.
2. Print `17.0 / 5.0`.
3. What does `10 - 2 * 3` give? Guess first, then check. Then use brackets to make it give `24`.
4. Start with `var money = 100`. Spend 30 (`-=`). Earn 50 (`+=`). Double it (`*=`). Print the final value.
5. Is `27` even or odd? Use `%` to check.
6. Make `let temperature = 32`. Print whether it is greater than 30.

<details>
<summary>Click to see the answers</summary>

```swift
// 1
print(17 / 5)   // 3   (5 fits into 17 three times)
print(17 % 5)   // 2   (17 - 15 = 2 left over)

// 2
print(17.0 / 5.0)   // 3.4

// 3
print(10 - 2 * 3)     // 4   (2*3 first = 6, then 10-6)
print((10 - 2) * 3)   // 24

// 4
var money = 100
money -= 30   // 70
money += 50   // 120
money *= 2    // 240
print(money)

// 5
print(27 % 2)   // 1 → odd

// 6
let temperature = 32
print(temperature > 30)   // true
```

</details>

---

## 🧠 Remember

- `+ - * /` for math, `%` for remainder.
- `Int / Int` drops the decimals. Use `Double` for decimals.
- `*` and `/` happen before `+` and `-`. Use `( )` to change the order.
- `x += 1` is a shortcut for `x = x + 1`.
- `==` asks "are they equal?". `=` puts a value in a box.
- Comparisons give `true` or `false`.

---

⬅️ **Back:** [Chapter 07 — Data Types](07-data-types.md)
➡️ **Next:** [Chapter 09 — Working With Text](09-working-with-text.md)
