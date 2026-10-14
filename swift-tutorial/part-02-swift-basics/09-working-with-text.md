# Chapter 09 — Working With Text (Strings)

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- Joining strings with `+`.
- Putting values inside strings with `\( )`.
- Special characters like new line `\n`.
- Multi-line strings `"""`.
- Useful string tools: `count`, `uppercased()`, `contains()` and more.

---

## 1. Joining strings with `+`

```swift
let first = "Good"
let second = "morning"
let message = first + " " + second
print(message)
```

**Output:**

```
Good morning
```

| Part | Meaning |
|---|---|
| `first` | `"Good"` |
| `+` | With strings, `+` means **join together**. |
| `" "` | A string with just a **space** inside. |
| `+ second` | Join `"morning"` at the end. |
| Result | `"Good" + " " + "morning"` = `"Good morning"` |

> 📖 **New word: Concatenation**
> Joining strings together. (A long word for a simple idea!)

⚠️ **Careful:** Without the `" "`, you get `"Goodmorning"`.

⚠️ **Careful:** You **cannot** use `+` to join a String and a number.

```swift
let age = 12
print("I am " + age)          // ❌ ERROR
print("I am " + String(age))  // ✅ works
```

There is an easier way — keep reading! 👇

---

## 2. String interpolation `\( )` ⭐

This is the **best** way to put values inside text.

```swift
let name = "Meena"
let age = 12
print("My name is \(name) and I am \(age) years old.")
```

**Output:**

```
My name is Meena and I am 12 years old.
```

| Part | Meaning |
|---|---|
| `"My name is ` | Normal text. |
| `\(name)` | **Backslash + brackets.** "Put the value of `name` here." → `Meena` |
| ` and I am ` | Normal text. |
| `\(age)` | "Put the value of `age` here." → `12`. Works with numbers too! |
| ` years old."` | Normal text. |

> 📖 **New word: String interpolation**
> Putting a value **inside** a string using `\( )`.

💡 **Tip:** The backslash `\` is usually above the `Enter` key. It leans **left**: `\`. The normal slash `/` leans **right**.

### You can even do math inside

```swift
let apples = 3
let oranges = 4
print("Total fruits: \(apples + oranges)")
```

**Output:**

```
Total fruits: 7
```

Swift calculates `apples + oranges` = `7` and puts it in the text.

🧠 **Remember:** Use `\(something)` to put any value inside a string.

---

## 3. Special characters (escape characters)

Some characters are hard to type inside a string. Swift uses `\` for them.

| Write | Means |
|---|---|
| `\n` | **new line** |
| `\t` | **tab** (a big space) |
| `\"` | a quote mark `"` inside a string |
| `\\` | a backslash `\` |

### New line `\n`

```swift
print("Line one\nLine two")
```

**Output:**

```
Line one
Line two
```

`\n` means "go to the next line here".

### Quote marks inside a string

```swift
print("She said \"Hello!\"")
```

**Output:**

```
She said "Hello!"
```

| Part | Meaning |
|---|---|
| `\"` | "This quote is **part of the text**, not the end of the string." |

Without the `\`, Swift would think the string ends at `"Hello`. Error!

> 📖 **New word: Escape character**
> A `\` before a character to give it a special meaning.

---

## 4. Multi-line strings `"""`

For long text with many lines, use **three** quote marks.

```swift
let poem = """
Twinkle, twinkle,
little star,
how I wonder
what you are.
"""
print(poem)
```

**Output:**

```
Twinkle, twinkle,
little star,
how I wonder
what you are.
```

| Part | Meaning |
|---|---|
| `"""` (first) | Start a multi-line string. Must be at the **end of its line**. |
| The middle lines | The text, exactly as you type it. |
| `"""` (last) | End the string. Must be on its **own line**. |

---

## 5. How long is a string? `count`

```swift
let word = "Swift"
print(word.count)
```

**Output:**

```
5
```

| Part | Meaning |
|---|---|
| `word` | The string `"Swift"`. |
| `.` | "Use something that belongs to `word`." |
| `count` | The number of characters: S-w-i-f-t = **5**. |

> 📖 **New word: Property**
> Information that belongs to a value. `count` is a **property** of a string. You use it with a dot: `word.count`.

Spaces count too!

```swift
print("Hi there".count)   // 8   (H-i-space-t-h-e-r-e)
```

---

## 6. Is the string empty? `isEmpty`

```swift
let a = ""
let b = "Hello"
print(a.isEmpty)
print(b.isEmpty)
```

**Output:**

```
true
false
```

| Part | Meaning |
|---|---|
| `""` | An **empty string**: quotes with nothing inside. |
| `isEmpty` | `true` if there are no characters. |

---

## 7. Big and small letters

```swift
let name = "Meena"
print(name.uppercased())
print(name.lowercased())
```

**Output:**

```
MEENA
meena
```

| Part | Meaning |
|---|---|
| `uppercased()` | Make a new string with ALL CAPITAL letters. |
| `lowercased()` | Make a new string with all small letters. |

Notice the `()` brackets at the end. `uppercased()` is an **action**, not just information.

> 📖 **New word: Method**
> An **action** that belongs to a value. You call it with a dot and brackets: `name.uppercased()`.

| | Property | Method |
|---|---|---|
| What | information | action |
| Brackets? | No: `name.count` | Yes: `name.uppercased()` |

⚠️ **Careful:** `uppercased()` does **not** change `name`. It gives back a **new** string.

```swift
let name = "Meena"
let loud = name.uppercased()
print(name)   // Meena   (unchanged)
print(loud)   // MEENA
```

---

## 8. Searching in strings

### `contains` — is this text inside?

```swift
let sentence = "I love Swift"
print(sentence.contains("Swift"))
print(sentence.contains("Java"))
```

**Output:**

```
true
false
```

### `hasPrefix` and `hasSuffix` — starts with? ends with?

```swift
let file = "photo.png"
print(file.hasPrefix("photo"))   // starts with "photo"?
print(file.hasSuffix(".png"))    // ends with ".png"?
print(file.hasSuffix(".jpg"))    // ends with ".jpg"?
```

**Output:**

```
true
true
false
```

⚠️ **Careful:** These are **case-sensitive**. `"Swift".contains("swift")` is `false`.

💡 **Tip:** To search without caring about case, make both lowercase first:
`sentence.lowercased().contains("swift")`

---

## 9. Replacing text

```swift
let text = "I like cats"
let newText = text.replacingOccurrences(of: "cats", with: "dogs")
print(newText)
```

**Output:**

```
I like dogs
```

| Part | Meaning |
|---|---|
| `replacingOccurrences` | "Replace every place where you find…" |
| `of: "cats"` | …this text… |
| `with: "dogs"` | …with this text. |

⚠️ **Careful:** In SwiftFiddle this method may need `import Foundation` at the top of your code. If you get an error, add this as the **first line**:

```swift
import Foundation
```

> 📖 **New word: import**
> `import` brings in extra tools. `Foundation` is a big box of useful tools from Apple.

---

## 10. Adding to a string

```swift
var story = "Once upon a time"
story += ", there was a cat."
print(story)
```

**Output:**

```
Once upon a time, there was a cat.
```

| Part | Meaning |
|---|---|
| `var story` | Must be `var`, because we change it. |
| `story += "..."` | Add text to the **end** of `story`. |

---

## 11. Comparing strings

```swift
let password = "abc123"
print(password == "abc123")
print(password == "ABC123")
```

**Output:**

```
true
false
```

Strings are equal only if **every character** is exactly the same — including big and small letters.

---

## 12. Mini project: a name card 🪪

```swift
let firstName = "Arun"
let lastName = "Kumar"
let age = 25
let city = "Bengaluru"

let fullName = firstName + " " + lastName

let card = """
=======================
  Name : \(fullName)
  Age  : \(age)
  City : \(city.uppercased())
  Letters in name: \(fullName.count)
=======================
"""

print(card)
```

**Output:**

```
=======================
  Name : Arun Kumar
  Age  : 25
  City : BENGALURU
  Letters in name: 10
=======================
```

| Part | What happens |
|---|---|
| `firstName + " " + lastName` | Join → `"Arun Kumar"`. |
| `"""` ... `"""` | A multi-line string. |
| `\(fullName)` | Put the full name here. |
| `\(age)` | Put the age here. |
| `\(city.uppercased())` | Put the city in capital letters here. |
| `\(fullName.count)` | Count characters in `"Arun Kumar"` = 10 (the space counts). |

---

## 🏋️ Practice

1. Make `let animal = "tiger"` and `let legs = 4`. Use `\( )` to print: `A tiger has 4 legs.`
2. Print your name in ALL CAPITAL letters.
3. How many characters are in `"Hello, World!"`? Guess, then check with `.count`.
4. Print this in **one** `print`, using `\n`:
   ```
   Apple
   Banana
   Cherry
   ```
5. Print: `He said "Swift is fun!"` (with the quote marks).
6. Check if `"swiftfiddle.com"` ends with `".com"`.

<details>
<summary>Click to see the answers</summary>

```swift
// 1
let animal = "tiger"
let legs = 4
print("A \(animal) has \(legs) legs.")

// 2
print("Ravi".uppercased())

// 3
print("Hello, World!".count)   // 13

// 4
print("Apple\nBanana\nCherry")

// 5
print("He said \"Swift is fun!\"")

// 6
print("swiftfiddle.com".hasSuffix(".com"))   // true
```

</details>

---

## 🧠 Remember

- `+` joins strings. Use `" "` for spaces.
- `\(value)` puts any value inside a string. ⭐ Use this most.
- `\n` = new line. `\"` = quote inside a string.
- `"""` for multi-line text.
- `.count`, `.isEmpty` → properties (no brackets).
- `.uppercased()`, `.contains("x")` → methods (with brackets).

---

⬅️ **Back:** [Chapter 08 — Doing Math](08-doing-math.md)
➡️ **Next:** [Chapter 10 — Making Decisions: `if` and `else`](10-if-else.md)
