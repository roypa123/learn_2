# Chapter 03 — Running Swift in Your Browser (No Install!)

✅ **Works in browser** — this chapter shows you how.

---

## What you will learn

- How to write and run Swift code using only a website.
- What each part of the website does.
- What "run", "output" and "error" mean.

---

## 1. Why use a website?

Xcode only works on a Mac.
But to **learn Swift**, we don't need Xcode.

There are free websites that can run Swift code for you.
You type code → you press a button → you see the result.

> 📖 **New word: Run**
> To **run** code means to tell the computer: *"Do these instructions now."*

---

## 2. Open the website

1. Open your web browser (Chrome, Edge, Firefox or Safari).
2. Go to: **https://swiftfiddle.com**
3. Wait a few seconds for the page to load.

💡 **Tip:** Save this page as a **bookmark** (press `Ctrl + D` on Windows). You will use it a lot.

💡 **Tip:** If the website does not work, search the internet for **"online Swift playground"**. There are other free websites that work the same way.

---

## 3. The parts of the page

The page has **two main areas**:

```
┌─────────────────────────────────────────────┐
│  [ Run ▶ ]     Swift version: 6.x           │  ← top bar
├─────────────────────────────────────────────┤
│                                             │
│   print("Hello, world!")                    │  ← EDITOR
│                                             │     (you type code here)
│                                             │
├─────────────────────────────────────────────┤
│   Hello, world!                             │  ← OUTPUT
│                                             │     (the result shows here)
└─────────────────────────────────────────────┘
```

| Part | What it does |
|---|---|
| **Run button** ▶ | Starts your code. |
| **Editor** | The big white (or dark) box where you **type** code. |
| **Output** | The box where the **result** appears. |

> 📖 **New word: Editor**
> A place where you type and change code. Like a notebook for code.

> 📖 **New word: Output**
> What the program shows after it runs.

⚠️ **Careful:** Websites change their design sometimes. The buttons may look a little different. Look for a button that says **Run** or has a ▶ play sign.

---

## 4. Let's try it!

### Step 1: Clean the editor

There may be some code in the editor already.
Click inside the editor. Press `Ctrl + A` (select all). Press `Delete`.
Now the editor is empty.

### Step 2: Type this line

```swift
print("Hello, world!")
```

Type it **exactly**. Every small mark is important:

| You type | Name of the mark |
|---|---|
| `print` | the word print, all small letters |
| `(` | open bracket |
| `"` | quote mark (on the keyboard, press `Shift` + `'`) |
| `Hello, world!` | your text |
| `"` | quote mark again |
| `)` | close bracket |

### Step 3: Press Run ▶

Wait 1–3 seconds.

### Step 4: Look at the output

You should see:

```
Hello, world!
```

🎉 **Congratulations! You just ran your first Swift program!**

---

## 5. When something goes wrong: errors

Let's make a mistake **on purpose**.
Remove the last `)` so the code looks like this:

```swift
print("Hello, world!"
```

Press **Run**. You will see an **error**, something like:

```
error: expected ')' in expression list
```

> 📖 **New word: Error**
> An error is a message from Swift. It means: *"I don't understand this. Please fix it."*

Let's read this error slowly:

| Part of the error | Meaning |
|---|---|
| `error:` | Something is wrong. |
| `expected ')'` | Swift was **waiting** for a `)` close bracket. |
| `in expression list` | Inside the brackets of `print`. |

So Swift is telling us: *"You forgot the `)`."*
Put the `)` back and press **Run** again. It works!

🧠 **Remember:** Errors are **helpers**, not enemies. They tell you what to fix.

💡 **Tip:** Error messages look scary at first. Read them slowly. After some time, you will understand them quickly.

---

## 6. Capital letters matter

Try this:

```swift
Print("Hello, world!")
```

(Big `P` instead of small `p`.)

Press **Run**. You get an error like:

```
error: cannot find 'Print' in scope
```

| Part | Meaning |
|---|---|
| `cannot find 'Print'` | Swift does not know any command called `Print`. |
| `in scope` | In the places Swift is looking. |

Swift knows `print` (small p), but **not** `Print` (big P).

> 📖 **New word: Case-sensitive**
> Swift is **case-sensitive**. This means big letters and small letters are **different**.
> `print`, `Print` and `PRINT` are three different words to Swift.

---

## 🏋️ Practice

1. Make Swift show your **name**. Example: `print("Ravi")`
2. Remove the first `"` quote mark. Run it. Read the error.
3. Write `PRINT("hi")`. Run it. Read the error.
4. Fix everything so it works again.

---

## 🧠 Remember

- Use **swiftfiddle.com** (or another online Swift playground) to run Swift.
- Type code in the **editor**, press **Run**, see the **output**.
- An **error** means Swift needs you to fix something.
- Swift is **case-sensitive**: `print` is not the same as `Print`.

---

⬅️ **Back:** [Chapter 02 — What Are Swift, SwiftUI and Xcode?](02-what-are-swift-swiftui-xcode.md)
➡️ **Next:** [Chapter 04 — Your First Program: `print`](04-first-program-print.md)
