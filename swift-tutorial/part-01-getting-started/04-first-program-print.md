# Chapter 04 — Your First Program: `print`

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- How `print` works, part by part.
- How to print many lines.
- How to print numbers.
- What a "string" is.

---

## 1. The `print` command

```swift
print("Good morning")
```

**Output:**

```
Good morning
```

Let's look at **every part**:

| Part | Name | What it means |
|---|---|---|
| `print` | function name | A command that **shows** something in the output. |
| `(` | open bracket | "Here comes the thing to show." |
| `"` | opening quote | "Text starts here." |
| `Good morning` | the text | The words we want to show. |
| `"` | closing quote | "Text ends here." |
| `)` | close bracket | "That's all. Finished." |

> 📖 **New word: Function**
> A function is a command with a name. You **call** it to make it do its job.
> `print` is a function. Its job is to show things.

> 📖 **New word: Call**
> To **call** a function means to **use** it. Writing `print("Hi")` is *calling* `print`.

💡 **Tip:** Think of `print` like a loudspeaker 📢. Whatever you put inside the brackets, it says out loud.

---

## 2. What is a string?

Text inside quote marks is called a **string**.

```swift
"Good morning"
```

> 📖 **New word: String**
> A **string** is a piece of text. In Swift, strings are always inside `"double quotes"`.

Why "string"? Think of letters on a string, like beads on a necklace:
`G-o-o-d- -m-o-r-n-i-n-g` 📿

The quotes tell Swift: *"This is text. Don't try to understand it as code."*

⚠️ **Careful:** Use **double** quotes `"`, not single quotes `'`.

```swift
print('Hello')   // ❌ ERROR — single quotes do not work in Swift
print("Hello")   // ✅ correct
```

(The `//` part is a comment. We learn about it in the next chapter. Swift ignores it.)

---

## 3. Printing many lines

Swift reads code from **top to bottom**.

```swift
print("One")
print("Two")
print("Three")
```

**Output:**

```
One
Two
Three
```

Line by line:

| Line | What happens |
|---|---|
| `print("One")` | Swift shows `One`, then moves to a new line. |
| `print("Two")` | Swift shows `Two`, then moves to a new line. |
| `print("Three")` | Swift shows `Three`, then moves to a new line. |

🧠 **Remember:** Every `print` puts its text on a **new line**.

Now change the order:

```swift
print("Three")
print("Two")
print("One")
```

**Output:**

```
Three
Two
One
```

The output follows the **order** of the code.

---

## 4. Printing numbers

Numbers do **not** need quotes.

```swift
print(7)
```

**Output:**

```
7
```

| Part | What it means |
|---|---|
| `print` | Show something. |
| `(7)` | The thing to show is the number 7. No quotes, because it is a number, not text. |

Swift can also **do math** inside `print`:

```swift
print(2 + 3)
```

**Output:**

```
5
```

Swift **calculates** `2 + 3` first, gets `5`, and then prints `5`.

Now look at this — with quotes:

```swift
print("2 + 3")
```

**Output:**

```
2 + 3
```

Why? Because of the quotes, Swift sees `2 + 3` as **text**, not math.
It just shows the text exactly.

| Code | Output | Why |
|---|---|---|
| `print(2 + 3)` | `5` | No quotes → math. |
| `print("2 + 3")` | `2 + 3` | Quotes → text. |

🧠 **Remember:** Quotes mean **text**. No quotes on numbers means **number** (Swift can do math).

---

## 5. An empty line

```swift
print("Hello")
print()
print("Bye")
```

**Output:**

```
Hello

Bye
```

| Line | What happens |
|---|---|
| `print("Hello")` | Shows `Hello`. |
| `print()` | Nothing inside the brackets → shows an **empty line**. |
| `print("Bye")` | Shows `Bye`. |

---

## 6. Printing several things at once

You can put more than one thing inside `print`, with a **comma** `,` between them.

```swift
print("I am", 10, "years old")
```

**Output:**

```
I am 10 years old
```

| Part | What it means |
|---|---|
| `"I am"` | First thing: a string. |
| `,` | Comma — separates the things. |
| `10` | Second thing: a number. |
| `,` | Comma again. |
| `"years old"` | Third thing: a string. |

Notice: Swift puts **one space** between each thing automatically.

---

## 7. Common mistakes

| Wrong code ❌ | Problem | Correct code ✅ |
|---|---|---|
| `print(Hello)` | Text without quotes. Swift thinks `Hello` is a name it should know. | `print("Hello")` |
| `print("Hello)` | Missing closing quote. | `print("Hello")` |
| `print "Hello"` | Missing brackets. | `print("Hello")` |
| `Print("Hello")` | Big `P`. | `print("Hello")` |
| `print('Hello')` | Single quotes. | `print("Hello")` |

---

## 🏋️ Practice

1. Print your name, your city and your favorite food, each on its own line.
2. Print the answer to `100 + 250`.
3. Print `100 + 250` as **text** (so the output is exactly `100 + 250`).
4. Print this, using an empty line in the middle:
   ```
   Roses are red

   Violets are blue
   ```
5. Use **one** `print` with commas to show: `My lucky number is 7`

<details>
<summary>Click to see the answers</summary>

```swift
// 1
print("Ravi")
print("Chennai")
print("Dosa")

// 2
print(100 + 250)

// 3
print("100 + 250")

// 4
print("Roses are red")
print()
print("Violets are blue")

// 5
print("My lucky number is", 7)
```

</details>

---

## 🧠 Remember

- `print(...)` shows something in the output.
- Text must be inside `"double quotes"`. Text is called a **string**.
- Numbers don't need quotes, and Swift can do math with them.
- Each `print` makes a **new line**.
- Use commas to print several things in one line.

---

⬅️ **Back:** [Chapter 03 — Running Swift in Your Browser](03-running-swift-in-browser.md)
➡️ **Next:** [Chapter 05 — Comments: Notes for Humans](05-comments.md)
