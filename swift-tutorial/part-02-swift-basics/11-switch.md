# Chapter 11 — Many Choices: `switch`

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- How `switch` picks one choice from many.
- What `case` and `default` mean.
- Matching many values in one case.
- Matching ranges like `1...5`.
- When to use `switch` instead of `if`.

---

## 1. The problem

Imagine a traffic light 🚦. We want to tell the driver what to do.

With `if`, it looks like this:

```swift
let light = "red"

if light == "red" {
    print("Stop")
} else if light == "yellow" {
    print("Slow down")
} else if light == "green" {
    print("Go")
} else {
    print("Light is broken")
}
```

It works, but we write `light ==` again and again. 😩

`switch` makes this cleaner.

---

## 2. The `switch` statement

```swift
let light = "red"

switch light {
case "red":
    print("Stop")
case "yellow":
    print("Slow down")
case "green":
    print("Go")
default:
    print("Light is broken")
}
```

**Output:**

```
Stop
```

Every part:

| Part | Meaning |
|---|---|
| `switch light {` | "Look at the value of `light`. Find the matching case." |
| `case "red":` | "If `light` is `"red"`, run the code below." |
| `print("Stop")` | The code for this case. |
| `case "yellow":` | "If `light` is `"yellow"`…" |
| `case "green":` | "If `light` is `"green"`…" |
| `default:` | "If **nothing** above matched, run this." |
| `}` | End of the switch. |

> 📖 **New word: case**
> One possible choice inside a `switch`.

> 📖 **New word: default**
> The choice to use when no `case` matches. Like `else`.

How Swift thinks:

```
light = "red"
   │
   ├── is it "red"?    YES → print "Stop" → DONE ✅
   ├── is it "yellow"? (not checked)
   ├── is it "green"?  (not checked)
   └── default         (not checked)
```

🧠 **Remember:** Swift runs **only the first matching case**, then leaves the `switch`.

---

## 3. `default` is required (usually)

```swift
let light = "red"

switch light {
case "red":
    print("Stop")
case "green":
    print("Go")
}
```

**Error:**

```
error: switch must be exhaustive
```

> 📖 **New word: Exhaustive**
> Covering **every** possible value.

A string could be **anything**: `"blue"`, `"pizza"`, `""`…
Swift wants you to handle **all** of them. So you need `default`.

💡 **Tip:** This is a safety feature. Swift makes sure you never forget a case.

---

## 4. Many values in one case

Use a comma `,` to match more than one value.

```swift
let day = "Sunday"

switch day {
case "Saturday", "Sunday":
    print("Weekend! 🎉")
case "Monday", "Tuesday", "Wednesday", "Thursday", "Friday":
    print("School day 📚")
default:
    print("That is not a day.")
}
```

**Output:**

```
Weekend! 🎉
```

| Part | Meaning |
|---|---|
| `case "Saturday", "Sunday":` | Match if `day` is `"Saturday"` **or** `"Sunday"`. |

---

## 5. Switch with numbers

```swift
let dice = 6

switch dice {
case 1:
    print("One")
case 6:
    print("Six! Roll again! 🎲")
default:
    print("You rolled \(dice)")
}
```

**Output:**

```
Six! Roll again! 🎲
```

---

## 6. Ranges: `...` and `..<`

A **range** is a group of numbers from a start to an end.

> 📖 **New word: Range**
> A sequence of numbers between two ends.

| Range | Meaning | Numbers included |
|---|---|---|
| `1...5` | from 1 **to** 5 (includes 5) | 1, 2, 3, 4, 5 |
| `1..<5` | from 1 **up to but not** 5 | 1, 2, 3, 4 |

💡 **Tip:** `...` (three dots) = **closed** range, includes the end.
`..<` (two dots and less-than) = **half-open** range, stops before the end.

```swift
let marks = 82

switch marks {
case 90...100:
    print("Grade A")
case 75..<90:
    print("Grade B")
case 50..<75:
    print("Grade C")
case 0..<50:
    print("Try again")
default:
    print("Invalid marks")
}
```

**Output:**

```
Grade B
```

| Case | Numbers | Does 82 match? |
|---|---|---|
| `90...100` | 90 to 100 | No |
| `75..<90` | 75 to 89 | **Yes!** ✅ |

The `default` catches strange values like `-5` or `150`.

---

## 7. One-sided ranges

```swift
let age = 70

switch age {
case ..<13:
    print("Child")
case 13...19:
    print("Teenager")
case 20...59:
    print("Adult")
case 60...:
    print("Senior")
default:
    print("Unknown")
}
```

**Output:**

```
Senior
```

| Range | Meaning |
|---|---|
| `..<13` | anything **less than** 13 |
| `60...` | 60 **or more** (no end) |

---

## 8. More code in one case

A case can have **many lines**:

```swift
let command = "jump"

switch command {
case "jump":
    print("The player jumps!")
    print("Energy -5")
case "run":
    print("The player runs!")
    print("Energy -2")
default:
    print("Unknown command")
}
```

**Output:**

```
The player jumps!
Energy -5
```

⚠️ **Careful:** Every case must have **at least one line** of code. An empty case is an error.

If you really want "do nothing", use `break`:

```swift
switch command {
case "wait":
    break          // do nothing
default:
    print("Doing something")
}
```

> 📖 **New word: break**
> "Stop here and leave the switch."

---

## 9. Extra condition with `where`

You can add a check to a case with `where`.

```swift
let number = 8

switch number {
case let n where n % 2 == 0:
    print("\(n) is even")
default:
    print("\(number) is odd")
}
```

**Output:**

```
8 is even
```

| Part | Meaning |
|---|---|
| `case let n` | "Take the value and call it `n` for a moment." |
| `where n % 2 == 0` | "…but only match if `n` is even." |

This is a more advanced trick. Don't worry if it feels strange now.

---

## 10. `switch` as a value

Like `if`, a `switch` can give back a value (Swift 5.9 and later):

```swift
let light = "green"

let action = switch light {
case "red": "Stop"
case "yellow": "Slow down"
case "green": "Go"
default: "Broken"
}

print(action)
```

**Output:**

```
Go
```

---

## 11. `if` or `switch`?

| Use `switch` when… | Use `if` when… |
|---|---|
| You check **one value** against many choices. | You check **different** things. |
| Example: day of the week, menu option, grade. | Example: `age >= 18 && hasTicket`. |

---

## 12. Mini project: a simple menu 🍔

```swift
let choice = 2

switch choice {
case 1:
    print("You ordered a Burger. Price: 120")
case 2:
    print("You ordered a Pizza. Price: 250")
case 3:
    print("You ordered a Juice. Price: 60")
default:
    print("Please choose 1, 2 or 3.")
}
```

**Output:**

```
You ordered a Pizza. Price: 250
```

---

## 🏋️ Practice

1. Make `let month = 2`. Use `switch` to print the month name for 1, 2 and 3. For anything else, print `"Other month"`.
2. Make `let letter = "e"`. Print `"Vowel"` if it is a, e, i, o or u. Otherwise print `"Consonant"`.
3. Make `let hour = 14`. Print `"Morning"` for 5–11, `"Afternoon"` for 12–16, `"Evening"` for 17–20, and `"Night"` for anything else.
4. Remove `default` from exercise 1. Read the error.

<details>
<summary>Click to see the answers</summary>

```swift
// 1
let month = 2
switch month {
case 1:
    print("January")
case 2:
    print("February")
case 3:
    print("March")
default:
    print("Other month")
}

// 2
let letter = "e"
switch letter {
case "a", "e", "i", "o", "u":
    print("Vowel")
default:
    print("Consonant")
}

// 3
let hour = 14
switch hour {
case 5...11:
    print("Morning")
case 12...16:
    print("Afternoon")
case 17...20:
    print("Evening")
default:
    print("Night")
}

// 4 → error: switch must be exhaustive
```

</details>

---

## 🧠 Remember

- `switch value { case ...: }` picks **one** matching case.
- Only the **first** match runs.
- `default:` handles everything else. Swift needs every value covered.
- Use commas for many values: `case "a", "e":`
- Use ranges: `1...5` (includes 5), `1..<5` (stops before 5).

---

⬅️ **Back:** [Chapter 10 — Making Decisions](10-if-else.md)
➡️ **Next:** [Chapter 12 — Repeating: `for` Loops](12-for-loops.md)
