# Chapter 05 — Comments: Notes for Humans

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What a comment is.
- How to write one-line comments `//`.
- How to write many-line comments `/* */`.
- When comments are useful.

---

## 1. What is a comment?

> 📖 **New word: Comment**
> A comment is a **note** in your code. It is for **humans** to read.
> Swift **ignores** comments completely.

Think of a recipe book 📕. Someone wrote in pencil next to a step:
*"Use less salt — Grandma likes it this way."*

The cook reads it. But it is not a cooking step.
A comment is the same: a helpful note, not an instruction.

---

## 2. One-line comments: `//`

Write two slashes `//`. Everything after them, **on that line**, is a comment.

```swift
// This line shows a greeting
print("Hello")
```

**Output:**

```
Hello
```

| Line | What Swift does |
|---|---|
| `// This line shows a greeting` | Starts with `//` → Swift **skips** it. |
| `print("Hello")` | Normal code → Swift **runs** it. |

💡 **Tip:** The `/` key is usually next to the right `Shift` key on the keyboard.

### Comment at the end of a line

You can also put `//` **after** code on the same line:

```swift
print("Hello")   // say hello to the user
```

**Output:**

```
Hello
```

| Part | What Swift does |
|---|---|
| `print("Hello")` | Runs it. |
| `// say hello to the user` | Skips it. |

---

## 3. Many-line comments: `/* ... */`

If your note is long, use `/*` to **start** and `*/` to **end**.

```swift
/*
 This program says hello.
 It was written by Ravi.
 Date: Monday
*/
print("Hello")
```

**Output:**

```
Hello
```

| Part | Meaning |
|---|---|
| `/*` | "Comment **starts** here." |
| The lines in the middle | All skipped by Swift. |
| `*/` | "Comment **ends** here." |
| `print("Hello")` | Normal code. Swift runs it. |

⚠️ **Careful:** If you forget `*/`, then **all** the code after `/*` becomes a comment, and nothing runs!

---

## 4. "Turning off" code with comments

Comments are also useful to **turn off** a line of code without deleting it.

```swift
print("Line 1")
// print("Line 2")
print("Line 3")
```

**Output:**

```
Line 1
Line 3
```

`Line 2` is not shown, because that line is now a comment.

> 📖 **New word: Commenting out**
> Putting `//` in front of code to turn it off is called **commenting out** code.

💡 **Tip:** This is very useful when you are looking for a bug. Turn off one line at a time and see what changes.

---

## 5. Good comments vs bad comments

A good comment explains **why**, or something that is not obvious.

```swift
// ✅ Good: explains WHY
// We add 1 because people count from 1, not from 0
print(0 + 1)
```

A bad comment just repeats what the code already says:

```swift
// ❌ Not useful: the code already says this
// print hello
print("hello")
```

In this tutorial, we will use **many** comments, because you are learning.
That is fine! Later, when you are more experienced, you will write fewer.

---

## 🏋️ Practice

1. Write a program with **3** `print` lines. Add a `//` comment above each one explaining it.
2. Comment out the **middle** `print`. Run it. Which lines show?
3. Add a `/* */` comment at the top with your name and today's date.
4. Remove the `*/` from your comment. Run it. What happens? Then fix it.

<details>
<summary>Click to see an example answer</summary>

```swift
/*
 Name: Ravi
 Date: 14 October
*/

// Show a greeting
print("Hello")

// Show my favorite color
// print("Blue")

// Say goodbye
print("Bye")
```

**Output:**

```
Hello
Bye
```

</details>

---

## 🧠 Remember

- Comments are notes for **humans**. Swift **ignores** them.
- `//` → comment until the end of the line.
- `/* ... */` → comment across many lines.
- You can **comment out** code to turn it off for a while.

---

## 🎉 Part 1 complete!

You now know:

- What programming is.
- What Swift, SwiftUI and Xcode are.
- How to run Swift in your browser.
- How to use `print`.
- How to write comments.

In **Part 2**, we start learning real Swift: storing information with **variables**.

---

⬅️ **Back:** [Chapter 04 — Your First Program: `print`](04-first-program-print.md)
➡️ **Next:** Chapter 06 — Variables and Constants *(coming soon)*
