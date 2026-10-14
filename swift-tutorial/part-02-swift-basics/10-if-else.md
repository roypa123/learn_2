# Chapter 10 — Making Decisions: `if` and `else`

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- How to run code **only when** something is true: `if`.
- What to do **otherwise**: `else`.
- Checking many choices: `else if`.
- Joining conditions: `&&` (and), `||` (or), `!` (not).
- A short form: the ternary operator `? :`.

---

## 1. Decisions in real life

Every day you make decisions:

- **If** it is raining, **then** take an umbrella ☂️.
- **If** I am hungry, **then** eat. **Otherwise**, keep playing.

Programs make decisions too. We use `if`.

---

## 2. The `if` statement

```swift
let isRaining = true

if isRaining {
    print("Take an umbrella!")
}
```

**Output:**

```
Take an umbrella!
```

Let's look at every part:

| Part | Meaning |
|---|---|
| `if` | "Check something." |
| `isRaining` | The thing to check. It must be `true` or `false` (a `Bool`). |
| `{` | "Start of the code to run **if** it is true." |
| `print("Take an umbrella!")` | The code that runs only if it is true. |
| `}` | "End of that code." |

> 📖 **New word: Condition**
> The question that `if` checks. The answer must be `true` or `false`.

> 📖 **New word: Curly braces `{ }`**
> These make a **block** of code — a group of lines that belong together.

Now change it:

```swift
let isRaining = false

if isRaining {
    print("Take an umbrella!")
}
```

**Output:**

*(nothing)*

The condition is `false`, so Swift **skips** everything inside `{ }`.

💡 **Tip:** The code inside `{ }` is moved to the right with spaces. This is called **indentation**. Swift doesn't need it, but it makes code much easier for humans to read. Always do it!

---

## 3. Using comparisons in `if`

The condition is often a comparison (from Chapter 08).

```swift
let age = 20

if age >= 18 {
    print("You can vote.")
}
```

**Output:**

```
You can vote.
```

| Part | Meaning |
|---|---|
| `age >= 18` | Is 20 greater than or equal to 18? → `true` |
| So... | The `print` inside runs. |

---

## 4. `else` — what to do otherwise

```swift
let age = 15

if age >= 18 {
    print("You can vote.")
} else {
    print("You are too young to vote.")
}
```

**Output:**

```
You are too young to vote.
```

| Part | Meaning |
|---|---|
| `if age >= 18 {` | Is 15 >= 18? → `false`. Skip this block. |
| `} else {` | "Otherwise, run this block." |
| `print("You are too young to vote.")` | Runs. |

🧠 **Remember:** With `if`/`else`, **exactly one** of the two blocks runs. Never both. Never none.

```
          age >= 18 ?
          /         \
       true         false
        |             |
  "You can vote"   "Too young"
```

---

## 5. `else if` — many choices

```swift
let marks = 72

if marks >= 90 {
    print("Grade A")
} else if marks >= 75 {
    print("Grade B")
} else if marks >= 50 {
    print("Grade C")
} else {
    print("Try again")
}
```

**Output:**

```
Grade C
```

Swift checks **from top to bottom** and stops at the **first** `true`:

| Step | Check | Result | What happens |
|---|---|---|---|
| 1 | `72 >= 90` | `false` | Go to next. |
| 2 | `72 >= 75` | `false` | Go to next. |
| 3 | `72 >= 50` | `true` | Print `Grade C`. **Stop.** |
| — | `else` | — | Skipped, because we already found a `true`. |

⚠️ **Careful:** Order matters! Look at this wrong code:

```swift
let marks = 95

if marks >= 50 {
    print("Grade C")
} else if marks >= 90 {
    print("Grade A")
}
```

**Output:** `Grade C` 😢

`95 >= 50` is `true`, so Swift stops there. It never checks `>= 90`.
Always put the **most strict** check first.

---

## 6. AND: `&&`

Both things must be true.

```swift
let age = 25
let hasTicket = true

if age >= 18 && hasTicket {
    print("You can enter the movie.")
}
```

**Output:**

```
You can enter the movie.
```

| Part | Meaning |
|---|---|
| `age >= 18` | `true` |
| `&&` | **AND**: both sides must be true. |
| `hasTicket` | `true` |
| Result | `true && true` = `true` |

AND table:

| Left | Right | `Left && Right` |
|---|---|---|
| `true` | `true` | `true` |
| `true` | `false` | `false` |
| `false` | `true` | `false` |
| `false` | `false` | `false` |

💡 **Tip:** The `&` key is `Shift` + `7` on most keyboards.

---

## 7. OR: `||`

At least one thing must be true.

```swift
let isWeekend = false
let isHoliday = true

if isWeekend || isHoliday {
    print("No school today! 🎉")
}
```

**Output:**

```
No school today! 🎉
```

| Part | Meaning |
|---|---|
| `isWeekend` | `false` |
| `\|\|` | **OR**: at least one side must be true. |
| `isHoliday` | `true` |
| Result | `false \|\| true` = `true` |

OR table:

| Left | Right | `Left \|\| Right` |
|---|---|---|
| `true` | `true` | `true` |
| `true` | `false` | `true` |
| `false` | `true` | `true` |
| `false` | `false` | `false` |

💡 **Tip:** The `|` key (called "pipe") is usually above `Enter`, with `Shift` + `\`.

---

## 8. NOT: `!`

`!` flips `true` to `false`, and `false` to `true`.

```swift
let isLoggedIn = false

if !isLoggedIn {
    print("Please log in.")
}
```

**Output:**

```
Please log in.
```

| Part | Meaning |
|---|---|
| `isLoggedIn` | `false` |
| `!isLoggedIn` | NOT false = `true` |
| So... | The `print` runs. |

Read `!isLoggedIn` as **"not logged in"**.

---

## 9. Checking strings

```swift
let password = "swift123"

if password == "swift123" {
    print("Welcome!")
} else {
    print("Wrong password.")
}
```

**Output:**

```
Welcome!
```

```swift
let email = "ravi@mail.com"

if email.contains("@") {
    print("Looks like an email.")
} else {
    print("This is not an email.")
}
```

**Output:**

```
Looks like an email.
```

---

## 10. `if` inside `if` (nesting)

```swift
let hasTicket = true
let age = 10

if hasTicket {
    if age >= 12 {
        print("Enjoy the movie!")
    } else {
        print("You need an adult with you.")
    }
} else {
    print("Please buy a ticket.")
}
```

**Output:**

```
You need an adult with you.
```

| Step | Check | Result |
|---|---|---|
| 1 | `hasTicket` | `true` → go inside. |
| 2 | `age >= 12` → `10 >= 12` | `false` → go to the inner `else`. |
| 3 | | Print `You need an adult with you.` |

⚠️ **Careful:** Every `{` needs a matching `}`. Count them! Good indentation helps.

---

## 11. Short form: the ternary operator `? :`

For simple choices between two values, there is a short way.

```swift
let age = 20
let message = age >= 18 ? "Adult" : "Child"
print(message)
```

**Output:**

```
Adult
```

| Part | Meaning |
|---|---|
| `age >= 18` | The question. |
| `?` | "If true, use…" |
| `"Adult"` | …this value. |
| `:` | "Otherwise, use…" |
| `"Child"` | …this value. |

It is the same as:

```swift
let message: String
if age >= 18 {
    message = "Adult"
} else {
    message = "Child"
}
```

💡 **Tip:** Use `? :` only for **simple** cases. If it's hard to read, use `if`/`else`.

---

## 12. `if` as a value (modern Swift)

In new Swift versions (5.9 and later), `if` can also give a value directly:

```swift
let temperature = 35
let feeling = if temperature > 30 { "Hot 🥵" } else { "Nice 😊" }
print(feeling)
```

**Output:**

```
Hot 🥵
```

Each block must have **just one value** inside.

---

## 13. Mini project: even or odd checker

```swift
let number = 17

if number % 2 == 0 {
    print("\(number) is even.")
} else {
    print("\(number) is odd.")
}
```

**Output:**

```
17 is odd.
```

| Part | Meaning |
|---|---|
| `number % 2` | Remainder after dividing by 2 → `1`. |
| `== 0` | Is it 0? → `1 == 0` → `false`. |
| So... | The `else` block runs. |

---

## 🏋️ Practice

1. Make `let temperature = 10`. If it is less than 15, print `"Wear a jacket"`. Otherwise print `"T-shirt weather"`.
2. Make `let speed = 85`. Print `"Too fast!"` if over 80, `"Good speed"` if 40 to 80, and `"Too slow"` if under 40.
3. Make `let hasHomework = true` and `let isDone = false`. If you have homework AND it is NOT done, print `"Do your homework!"`.
4. Make `let day = "Sunday"`. If the day is `"Saturday"` OR `"Sunday"`, print `"Weekend!"`.
5. Use `? :` to make a string that is `"Pass"` if `marks >= 35`, otherwise `"Fail"`.

<details>
<summary>Click to see the answers</summary>

```swift
// 1
let temperature = 10
if temperature < 15 {
    print("Wear a jacket")
} else {
    print("T-shirt weather")
}

// 2
let speed = 85
if speed > 80 {
    print("Too fast!")
} else if speed >= 40 {
    print("Good speed")
} else {
    print("Too slow")
}

// 3
let hasHomework = true
let isDone = false
if hasHomework && !isDone {
    print("Do your homework!")
}

// 4
let day = "Sunday"
if day == "Saturday" || day == "Sunday" {
    print("Weekend!")
}

// 5
let marks = 50
let result = marks >= 35 ? "Pass" : "Fail"
print(result)
```

</details>

---

## 🧠 Remember

- `if condition { ... }` runs code only when the condition is `true`.
- `else { ... }` runs when it is `false`.
- `else if` checks more choices, top to bottom. First `true` wins.
- `&&` = AND (both true). `||` = OR (at least one true). `!` = NOT (flip).
- `a ? b : c` = short if/else for values.

---

⬅️ **Back:** [Chapter 09 — Working With Text](09-working-with-text.md)
➡️ **Next:** [Chapter 11 — Many Choices: `switch`](11-switch.md)
