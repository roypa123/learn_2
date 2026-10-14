# Chapter 02 — What Are Swift, SwiftUI and Xcode?

✅ **Works in browser** — this chapter is just reading.

---

## What you will learn

- What **Swift** is.
- What **SwiftUI** is.
- What **Xcode** is.
- How these three work together.

---

## The big picture

To build a house, you need three things:

| House | iPhone app |
|---|---|
| 🧱 **Bricks** — the basic material | **Swift** — the language |
| 🪟 **Ready-made parts** — doors, windows | **SwiftUI** — ready-made screen parts |
| 🧰 **A toolbox** — hammer, saw, tape | **Xcode** — the app where you build |

Let's look at each one.

---

## 1. Swift — the language 🧱

> 📖 **New word: Swift**
> Swift is a programming language made by Apple in 2014.

With Swift, you write instructions like:

```swift
print("Hello!")
```

This tells the computer: *show the word Hello! on the screen.*

Good things about Swift:

- It is **easy to read**. It looks a little like English.
- It is **safe**. It helps you find mistakes early.
- It is **fast**.
- It is **free**.

🧠 **Remember:** Swift is the **language**. Everything else is built with it.

---

## 2. SwiftUI — building screens 🪟

> 📖 **New word: UI**
> UI means **User Interface**. It is everything you **see and touch** in an app:
> buttons, text, pictures, lists.

> 📖 **New word: SwiftUI**
> SwiftUI is a set of ready-made parts from Apple for building app screens with Swift.

For example, to show some text and a button, you write something like this:

```swift
VStack {
    Text("Hello!")
    Button("Tap me") { }
}
```

Don't worry about understanding this now. We will learn it in Part 5.
Just notice: it is **short**, and it **describes** what you want to see.

🧠 **Remember:** SwiftUI is for building **screens**. It is written **in Swift**.

---

## 3. Xcode — the workshop 🧰

> 📖 **New word: Xcode**
> Xcode is a free app from Apple. You use it to write, test and build iPhone apps.

Xcode gives you:

- A place to **type** your code.
- A **preview** that shows your screen while you type.
- A **Simulator** — a pretend iPhone on your computer screen.
- Tools to **find bugs**.
- Tools to **send your app** to the App Store.

⚠️ **Careful:** Xcode **only works on a Mac**. It does not work on Windows.

That is OK! In Parts 1, 2 and 3 we learn **Swift** without Xcode, using a website.
In Part 4 we will talk about how to get a Mac (you can even rent one online).

---

## 4. How they work together

```
    You write code in  ──►  XCODE
                              │
    The code is in     ──►  SWIFT
                              │
    Screens are made   ──►  SWIFTUI
    with                      │
                              ▼
                        📱 iPhone App
```

---

## 5. Why we learn Swift first

Imagine learning to write stories before you know the alphabet. Impossible!

- **Swift** is the alphabet.
- **SwiftUI** is writing stories.

So first, we learn Swift well (Parts 2 and 3).
Then, SwiftUI will be much easier.

---

## 🏋️ Practice

Answer these questions (you can say the answer out loud or write it):

1. Which one is the **language**: Swift, SwiftUI or Xcode?
2. Which one is used to build **screens**?
3. Which one only works on a **Mac**?

<details>
<summary>Click to see the answers</summary>

1. **Swift**
2. **SwiftUI**
3. **Xcode**

</details>

---

## 🧠 Remember

- **Swift** = the language.
- **SwiftUI** = ready-made parts for screens.
- **Xcode** = the app where you build everything (Mac only).
- We learn **Swift first**, in the browser.

---

⬅️ **Back:** [Chapter 01 — What Is Programming?](01-what-is-programming.md)
➡️ **Next:** [Chapter 03 — Running Swift in Your Browser](03-running-swift-in-browser.md)
