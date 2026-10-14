# Chapter 12 — Repeating: `for` Loops

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What a **loop** is.
- How to repeat code with `for ... in`.
- Counting with ranges.
- Using `_` when you don't need the number.
- Counting by 2s, 5s, or backwards with `stride`.
- Skipping with `continue` and stopping with `break`.

---

## 1. Why loops?

Imagine your teacher says: *"Write 'I will not talk in class' 100 times."* 😩

In code, you could write:

```swift
print("I will not talk in class")
print("I will not talk in class")
print("I will not talk in class")
// ... 97 more times
```

That is boring and silly. A **loop** does the repeating for you.

> 📖 **New word: Loop**
> Code that **repeats** again and again.

---

## 2. Your first `for` loop

```swift
for number in 1...5 {
    print(number)
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
| `for` | "Repeat this code…" |
| `number` | A temporary box. Each time, it holds the **current** number. You choose this name. |
| `in` | "…for each value in…" |
| `1...5` | …the range 1, 2, 3, 4, 5. |
| `{` | Start of the code to repeat. |
| `print(number)` | The code that repeats. |
| `}` | End of the code to repeat. |

How it runs, step by step:

| Round | `number` is | What prints |
|---|---|---|
| 1st | `1` | `1` |
| 2nd | `2` | `2` |
| 3rd | `3` | `3` |
| 4th | `4` | `4` |
| 5th | `5` | `5` |
| — | no more numbers | loop ends |

> 📖 **New word: Iteration**
> One round of a loop. This loop has 5 iterations.

---

## 3. Using the number

```swift
for i in 1...5 {
    print("\(i) x 3 = \(i * 3)")
}
```

**Output:**

```
1 x 3 = 3
2 x 3 = 6
3 x 3 = 9
4 x 3 = 12
5 x 3 = 15
```

| Part | Meaning |
|---|---|
| `i` | A short name, very common for loop counters. "i" for "index". |
| `\(i)` | Put the current number in the text. |
| `\(i * 3)` | Multiply it by 3, put the answer in the text. |

We made a **times table** with just 3 lines! ✨

---

## 4. `...` vs `..<` in loops

```swift
for i in 0..<3 {
    print(i)
}
```

**Output:**

```
0
1
2
```

| Range | Numbers |
|---|---|
| `0...3` | 0, 1, 2, 3 (four numbers) |
| `0..<3` | 0, 1, 2 (three numbers — stops **before** 3) |

💡 **Tip:** `0..<count` is very common in programming. It runs exactly `count` times.

---

## 5. When you don't need the number: `_`

Sometimes you just want to repeat, and you don't care about the number.

```swift
for _ in 1...3 {
    print("Hip hip hooray! 🎉")
}
```

**Output:**

```
Hip hip hooray! 🎉
Hip hip hooray! 🎉
Hip hip hooray! 🎉
```

| Part | Meaning |
|---|---|
| `_` | Underscore. It means: "I don't need a name. Just repeat." |

---

## 6. Adding things up in a loop

A very common pattern: **start with 0, add in each round.**

```swift
var total = 0

for n in 1...5 {
    total += n
}

print("Total: \(total)")
```

**Output:**

```
Total: 15
```

Step by step:

| Round | `n` | `total` before | `total += n` | `total` after |
|---|---|---|---|---|
| 1 | 1 | 0 | 0 + 1 | 1 |
| 2 | 2 | 1 | 1 + 2 | 3 |
| 3 | 3 | 3 | 3 + 3 | 6 |
| 4 | 4 | 6 | 6 + 4 | 10 |
| 5 | 5 | 10 | 10 + 5 | 15 |

⚠️ **Careful:** `var total = 0` must be **outside** (before) the loop.
If it is inside, it would reset to 0 in every round!

```swift
// ❌ Wrong
for n in 1...5 {
    var total = 0   // resets every round!
    total += n
}
```

---

## 7. Looping over a string's characters

A `for` loop can go through **each letter** of a string.

```swift
for letter in "Swift" {
    print(letter)
}
```

**Output:**

```
S
w
i
f
t
```

| Round | `letter` |
|---|---|
| 1 | `S` |
| 2 | `w` |
| 3 | `i` |
| 4 | `f` |
| 5 | `t` |

💡 **Tip:** In Chapter 14 we will loop over **lists** (arrays). This is where loops become super useful.

---

## 8. Counting by steps: `stride`

What if you want 0, 2, 4, 6, 8, 10?

```swift
for i in stride(from: 0, through: 10, by: 2) {
    print(i)
}
```

**Output:**

```
0
2
4
6
8
10
```

| Part | Meaning |
|---|---|
| `stride` | "Walk with big steps." |
| `from: 0` | Start at 0. |
| `through: 10` | Go up to 10, **including** 10. |
| `by: 2` | Each step adds 2. |

There is also `to:`, which **stops before** the end:

```swift
for i in stride(from: 0, to: 10, by: 5) {
    print(i)
}
```

**Output:**

```
0
5
```

| Word | Includes the end? |
|---|---|
| `through:` | Yes |
| `to:` | No |

### Counting backwards 🚀

```swift
for i in stride(from: 5, through: 1, by: -1) {
    print(i)
}
print("Liftoff! 🚀")
```

**Output:**

```
5
4
3
2
1
Liftoff! 🚀
```

`by: -1` means "go down by 1 each step".

Another way to go backwards:

```swift
for i in (1...5).reversed() {
    print(i)
}
```

This also prints 5, 4, 3, 2, 1.

---

## 9. `continue` — skip this round

```swift
for i in 1...6 {
    if i == 3 {
        continue
    }
    print(i)
}
```

**Output:**

```
1
2
4
5
6
```

| Part | Meaning |
|---|---|
| `if i == 3` | When `i` is 3… |
| `continue` | …**skip** the rest of this round. Go to the next number. |

`3` is missing! ✨

---

## 10. `break` — stop the loop completely

```swift
for i in 1...10 {
    if i == 4 {
        break
    }
    print(i)
}
print("Loop finished")
```

**Output:**

```
1
2
3
Loop finished
```

| Part | Meaning |
|---|---|
| `if i == 4` | When `i` is 4… |
| `break` | …**stop** the whole loop right now. |

| Keyword | Effect |
|---|---|
| `continue` | Skip **this** round, keep looping. |
| `break` | Stop the **whole** loop. |

---

## 11. Loops inside loops

```swift
for row in 1...3 {
    for column in 1...3 {
        print("(\(row), \(column))")
    }
}
```

**Output:**

```
(1, 1)
(1, 2)
(1, 3)
(2, 1)
(2, 2)
(2, 3)
(3, 1)
(3, 2)
(3, 3)
```

How it works:

- The **outer** loop (`row`) runs 3 times.
- For **each** `row`, the **inner** loop (`column`) runs 3 times.
- Total: 3 × 3 = **9** prints.

Think of a clock ⏰: the minute hand goes all the way around for every one step of the hour hand.

---

## 12. Mini project: star triangle ⭐

```swift
for row in 1...5 {
    var line = ""
    for _ in 1...row {
        line += "⭐"
    }
    print(line)
}
```

**Output:**

```
⭐
⭐⭐
⭐⭐⭐
⭐⭐⭐⭐
⭐⭐⭐⭐⭐
```

| Line | What happens |
|---|---|
| `for row in 1...5` | Do 5 rows. |
| `var line = ""` | Start each row with an empty string. |
| `for _ in 1...row` | Repeat `row` times (1 time, then 2, then 3...). |
| `line += "⭐"` | Add one star. |
| `print(line)` | Show the row. |

---

## 🏋️ Practice

1. Print the numbers from 10 to 20.
2. Print the 7 times table from 1 to 10 (`1 x 7 = 7` … `10 x 7 = 70`).
3. Add up all numbers from 1 to 100. Print the total. (Answer: 5050)
4. Print all **even** numbers from 2 to 20 using `stride`.
5. Count down from 10 to 1, then print `"Happy New Year! 🎆"`.
6. Print numbers 1 to 20, but **skip** numbers that can be divided by 3. (Hint: `continue` and `%`)

<details>
<summary>Click to see the answers</summary>

```swift
// 1
for i in 10...20 {
    print(i)
}

// 2
for i in 1...10 {
    print("\(i) x 7 = \(i * 7)")
}

// 3
var total = 0
for n in 1...100 {
    total += n
}
print(total)   // 5050

// 4
for n in stride(from: 2, through: 20, by: 2) {
    print(n)
}

// 5
for i in stride(from: 10, through: 1, by: -1) {
    print(i)
}
print("Happy New Year! 🎆")

// 6
for i in 1...20 {
    if i % 3 == 0 {
        continue
    }
    print(i)
}
```

</details>

---

## 🧠 Remember

- `for item in collection { ... }` repeats code for each item.
- `1...5` includes 5. `1..<5` stops before 5.
- Use `_` if you don't need the counter.
- `stride(from:through:by:)` for steps or counting backwards.
- `continue` skips one round. `break` stops the loop.

---

⬅️ **Back:** [Chapter 11 — Many Choices: `switch`](11-switch.md)
➡️ **Next:** [Chapter 13 — Repeating: `while` Loops](13-while-loops.md)
