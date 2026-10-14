# Chapter 13 — Repeating: `while` Loops

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- How `while` repeats code **as long as** something is true.
- What an **infinite loop** is (and how to avoid it).
- `repeat ... while` — run at least once.
- When to use `for` and when to use `while`.

---

## 1. `for` vs `while` — the idea

- `for`: You know **how many times**. *"Do 10 push-ups."* 💪
- `while`: You **don't know** how many times. *"Keep eating **while** you are hungry."* 🍕

---

## 2. Your first `while` loop

```swift
var count = 1

while count <= 5 {
    print(count)
    count += 1
}
```

**Output:**

```
1
2
3
4
5
```

Every part:

| Part | Meaning |
|---|---|
| `var count = 1` | Make a counter box. Start at 1. |
| `while` | "Keep repeating…" |
| `count <= 5` | "…**as long as** this is true." |
| `{` | Start of code to repeat. |
| `print(count)` | Show the counter. |
| `count += 1` | Add 1 to the counter. **Very important!** |
| `}` | End. Go back up and check the condition again. |

Step by step:

| Check | `count <= 5`? | Prints | `count` becomes |
|---|---|---|---|
| 1 | `1 <= 5` ✅ | 1 | 2 |
| 2 | `2 <= 5` ✅ | 2 | 3 |
| 3 | `3 <= 5` ✅ | 3 | 4 |
| 4 | `4 <= 5` ✅ | 4 | 5 |
| 5 | `5 <= 5` ✅ | 5 | 6 |
| 6 | `6 <= 5` ❌ | — | loop stops |

🧠 **Remember:** `while` checks the condition **before** each round. When the condition is `false`, the loop stops.

---

## 3. ⚠️ Danger: infinite loops

What if we forget `count += 1`?

```swift
var count = 1

while count <= 5 {
    print(count)
    // forgot count += 1 !!!
}
```

`count` is **always** 1. `1 <= 5` is **always** true. The loop **never stops!**

```
1
1
1
1
1
... forever ...
```

> 📖 **New word: Infinite loop**
> A loop that never stops, because its condition never becomes `false`.

⚠️ **Careful:** In SwiftFiddle, an infinite loop will run until the website stops it (it has a time limit). In a real app, the app would **freeze**.

🧠 **Remember:** Inside a `while` loop, something **must change** so the condition can become `false`.

---

## 4. A real use: when you don't know the count

**Question:** I have 1000 rupees. I spend 150 every day. How many days until I can't pay anymore?

```swift
var money = 1000
var days = 0

while money >= 150 {
    money -= 150
    days += 1
}

print("I can pay for \(days) days.")
print("Money left: \(money)")
```

**Output:**

```
I can pay for 6 days.
Money left: 100
```

| Line | Meaning |
|---|---|
| `var money = 1000` | Start with 1000. |
| `var days = 0` | No days spent yet. |
| `while money >= 150` | Keep going while I have enough for one more day. |
| `money -= 150` | Spend 150. |
| `days += 1` | One more day passed. |

We didn't know the answer (6) before. The loop **found** it for us. That's why `while` is perfect here.

---

## 5. Another example: doubling 🌱

A plant is 1 cm tall. It doubles in size every week. When will it be taller than 100 cm?

```swift
var height = 1
var weeks = 0

while height <= 100 {
    height *= 2
    weeks += 1
}

print("After \(weeks) weeks, the plant is \(height) cm tall.")
```

**Output:**

```
After 7 weeks, the plant is 128 cm tall.
```

| Week | Height |
|---|---|
| 0 | 1 |
| 1 | 2 |
| 2 | 4 |
| 3 | 8 |
| 4 | 16 |
| 5 | 32 |
| 6 | 64 |
| 7 | 128 ← more than 100, stop |

---

## 6. A `while` loop that never runs

If the condition is `false` from the start, the code inside **never runs**.

```swift
var x = 10

while x < 5 {
    print("This will never print")
}

print("Done")
```

**Output:**

```
Done
```

`10 < 5` is `false` right away, so Swift skips the loop.

---

## 7. `repeat ... while` — run at least once

Sometimes you want to run the code **first**, then check.

```swift
var x = 10

repeat {
    print("x is \(x)")
    x += 1
} while x < 5
```

**Output:**

```
x is 10
```

| Part | Meaning |
|---|---|
| `repeat {` | "Do this…" |
| `print(...)` and `x += 1` | The code. Runs **first**, before any check. |
| `} while x < 5` | "…then check. If true, do it again." |

Here `11 < 5` is false, so it stops after **one** round.

| | `while` | `repeat ... while` |
|---|---|---|
| Checks the condition | **before** each round | **after** each round |
| Can run 0 times? | Yes | No — always at least once |

💡 **Tip:** Real-life example: a game menu. You show the menu **at least once**, then repeat it while the player doesn't choose "Quit".

---

## 8. `break` and `continue` work here too

```swift
var n = 0

while true {
    n += 1
    if n == 4 {
        break
    }
    print(n)
}
```

**Output:**

```
1
2
3
```

| Part | Meaning |
|---|---|
| `while true` | The condition is **always** true. This would be infinite… |
| `if n == 4 { break }` | …but `break` stops it when `n` is 4. |

💡 **Tip:** `while true` + `break` is a common pattern, but use it carefully. Make sure `break` will really happen!

---

## 9. Mini project: guess the number 🎯

We can't type input in SwiftFiddle easily, so the computer will guess for us.

```swift
let secret = Int.random(in: 1...10)
var guess = 0
var tries = 0

while guess != secret {
    guess = Int.random(in: 1...10)
    tries += 1
    print("Try \(tries): guessed \(guess)")
}

print("Found it! The secret was \(secret). It took \(tries) tries.")
```

**Example output** (will be different every time!):

```
Try 1: guessed 3
Try 2: guessed 9
Try 3: guessed 7
Found it! The secret was 7. It took 3 tries.
```

| Line | Meaning |
|---|---|
| `Int.random(in: 1...10)` | Pick a **random** whole number from 1 to 10. |
| `let secret = ...` | The number to find. |
| `var guess = 0` | Start with a guess that is surely wrong (0 is not in 1–10). |
| `while guess != secret` | Keep going while the guess is **not equal** to the secret. |
| `guess = Int.random(in: 1...10)` | Make a new random guess. |
| `tries += 1` | Count this try. |

> 📖 **New word: Random**
> Picked by chance, like rolling a dice 🎲. You can't know it before.

---

## 10. `for` or `while`?

| Situation | Use |
|---|---|
| "Do this 10 times." | `for` |
| "Do this for each item in a list." | `for` |
| "Do this **until** something happens." | `while` |
| "Do this at least once, then maybe more." | `repeat ... while` |

---

## 🏋️ Practice

1. Use `while` to print numbers from 1 to 10.
2. Use `while` to print even numbers from 2 to 20.
3. You save 200 every month. How many months until you have at least 3000? Use `while`.
4. Start with `var number = 100`. Keep dividing it by 2 (`number /= 2`) while it is greater than 1. Print it each time.
5. Write a `repeat ... while` loop that prints `"Hello"` once, even though the condition is `false`.

<details>
<summary>Click to see the answers</summary>

```swift
// 1
var i = 1
while i <= 10 {
    print(i)
    i += 1
}

// 2
var e = 2
while e <= 20 {
    print(e)
    e += 2
}

// 3
var savings = 0
var months = 0
while savings < 3000 {
    savings += 200
    months += 1
}
print("Months: \(months)")   // 15

// 4
var number = 100
while number > 1 {
    number /= 2
    print(number)
}
// 50, 25, 12, 6, 3, 1

// 5
repeat {
    print("Hello")
} while false
```

</details>

---

## 🧠 Remember

- `while condition { ... }` repeats **as long as** the condition is true.
- Something inside **must change**, or you get an **infinite loop**.
- `repeat { ... } while condition` always runs **at least once**.
- Use `for` when you know the count. Use `while` when you don't.

---

⬅️ **Back:** [Chapter 12 — `for` Loops](12-for-loops.md)
➡️ **Next:** [Chapter 14 — Lists of Things: Arrays](14-arrays.md)
