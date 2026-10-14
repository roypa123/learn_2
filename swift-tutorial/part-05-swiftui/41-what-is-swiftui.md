# Chapter 41 — What Is SwiftUI?

🍎 **Needs a Mac** (or an iPad with Swift Playgrounds — most of Part 5 works there too!)

---

## What you will learn

- What SwiftUI is and how it thinks.
- **Declarative** vs **imperative** — a simple explanation.
- What a **View** is.
- What **modifiers** are, and why their **order** matters.
- How the **preview** works.
- How to make your own small views.

---

## 1. Before you start

Create a new project for Part 5:

1. **File → New → Project → iOS → App**.
2. Product Name: `LearnSwiftUI`. Interface: **SwiftUI**. Language: **Swift**.
3. Open `ContentView.swift`. Show the Canvas (`Cmd + Option + Enter`).

For every example in Part 5: **replace** the code inside `ContentView` (or the whole file) and watch the preview.

💡 **Tip:** You can also make a **new file** for each example: **File → New → File → SwiftUI View**. Each file gets its own `#Preview`.

---

## 2. What is SwiftUI?

> 📖 **New word: SwiftUI**
> Apple's modern way to build app screens using Swift code. It works on iPhone, iPad, Mac, Apple Watch, Apple TV and Vision Pro.

You **describe** what the screen should look like. SwiftUI **draws** it for you.

---

## 3. Declarative vs imperative 🍕

Imagine ordering a pizza.

**Imperative** (old way) — you give **every step**:
> "Take dough. Roll it flat. Add sauce. Add cheese. Put it in the oven at 220°C for 12 minutes. Take it out. Cut it into 8 pieces."

**Declarative** (SwiftUI way) — you **describe the result**:
> "I want a medium cheese pizza, cut into 8 pieces."

The chef (SwiftUI) knows **how** to make it.

> 📖 **New word: Declarative**
> You describe **what** you want. The system figures out **how** to do it.

> 📖 **New word: Imperative**
> You write **every step** of **how** to do it.

In SwiftUI:

```swift
VStack {
    Text("Hello")
    Text("World")
}
```

You're saying: *"I want two texts, one on top of the other."* That's it. You don't calculate positions, sizes or pixels.

---

## 4. Everything is a View

> 📖 **New word: View**
> Anything on the screen: a text, an image, a button, a list — or a whole screen made of other views.

Views are like **LEGO bricks** 🧱. Small bricks build bigger bricks, and bigger bricks build a whole screen.

```
 ┌─ Screen (a View) ─────────────┐
 │  ┌─ VStack (a View) ────────┐ │
 │  │  Image   (a View)        │ │
 │  │  Text    (a View)        │ │
 │  │  Button  (a View)        │ │
 │  └──────────────────────────┘ │
 └───────────────────────────────┘
```

---

## 5. Your own view

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        Text("Hello, SwiftUI!")
    }
}

#Preview {
    ContentView()
}
```

| Part | Meaning |
|---|---|
| `import SwiftUI` | Bring in SwiftUI. |
| `struct ContentView` | A view is a **struct** (Chapter 20). Name it with a Capital letter. |
| `: View` | It follows the **`View` protocol** (Chapter 24). |
| `var body: some View` | The protocol's **only** requirement: a computed property called `body`. |
| `some View` | "Returns some kind of View" (Chapter 24 explained `some`). |
| `Text("Hello, SwiftUI!")` | What to show. |
| `#Preview { ContentView() }` | Show it in the Canvas. |

🧠 **Remember:** Every SwiftUI view is a `struct` that follows `View` and has a `body`.

---

## 6. Views are cheap and are recreated often

SwiftUI views are **small structs**, not heavy objects. SwiftUI creates and throws them away **many times** — every time something changes.

That's why:
- Views are **structs** (fast to copy — Chapter 22).
- You don't store important data inside a plain `var` in a view. You'll use `@State` (Chapter 46) and others.

---

## 7. Modifiers

A **modifier** changes how a view looks or behaves.

```swift
Text("Hello")
    .font(.largeTitle)
    .foregroundStyle(.blue)
    .padding()
```

| Line | Meaning |
|---|---|
| `Text("Hello")` | A text view. |
| `.font(.largeTitle)` | Make the font very big. |
| `.foregroundStyle(.blue)` | Make the text blue. |
| `.padding()` | Add space around it. |

> 📖 **New word: Modifier**
> A method (starting with `.`) that returns a **new, changed** view.

💡 **Tip:** Put each modifier on its **own line**, indented. It's much easier to read.

### How it really works

Each modifier **wraps** the view in a new view:

```
 padding( foregroundStyle( font( Text("Hello") ) ) )
```

Like putting a gift 🎁 in a box, then that box in a bigger box, then wrapping paper.

---

## 8. Order matters! ⚠️

Compare these two:

```swift
Text("A")
    .padding()
    .background(.yellow)
```

```swift
Text("B")
    .background(.yellow)
    .padding()
```

```
   Example A               Example B
 ┌───────────┐
 │           │               ┌──┐
 │     A     │  ← big          │B │  ← small yellow
 │           │    yellow      └──┘     (padding is outside,
 └───────────┘                         not colored)
```

| | Steps |
|---|---|
| **A** | 1. Add padding (space) → 2. color **everything** (text + space) yellow. |
| **B** | 1. Color the text yellow → 2. add **clear** space around it. |

🧠 **Remember:** Modifiers apply **from top to bottom**. Each one changes the result of the one before.

Another example:

```swift
Text("Hi")
    .padding()
    .background(.yellow)
    .padding()
    .background(.orange)
```

This makes a yellow box inside an orange box! 🟧🟨 Try it.

---

## 9. The preview in detail

```swift
#Preview {
    ContentView()
}
```

- Only used by **Xcode**. Not part of the real app.
- You can have **many** previews in one file:

```swift
#Preview("Light") {
    ContentView()
}

#Preview("Dark") {
    ContentView()
        .preferredColorScheme(.dark)
}
```

| Part | Meaning |
|---|---|
| `#Preview("Light")` | A preview with a name. Shows as a tab in the Canvas. |
| `.preferredColorScheme(.dark)` | Show it in dark mode. |

💡 **Tip:** If the preview stops updating, press `Cmd + Option + P`.

---

## 10. Splitting into smaller views 🧩

When `body` gets long, make **smaller views** and combine them.

```swift
struct ContentView: View {
    var body: some View {
        VStack {
            HeaderView()
            Text("Welcome to my app!")
            FooterView()
        }
    }
}

struct HeaderView: View {
    var body: some View {
        Text("⭐ My App ⭐")
            .font(.largeTitle)
    }
}

struct FooterView: View {
    var body: some View {
        Text("Made with SwiftUI")
            .font(.caption)
            .foregroundStyle(.gray)
    }
}

#Preview {
    ContentView()
}
```

| Part | Meaning |
|---|---|
| `HeaderView()` | Use your own view like any built-in view. |
| `struct HeaderView: View` | A small, reusable view. |

### Views with inputs

Views are structs, so they can have **properties**:

```swift
struct Greeting: View {
    let name: String

    var body: some View {
        Text("Hello, \(name)! 👋")
    }
}

struct ContentView: View {
    var body: some View {
        VStack {
            Greeting(name: "Ravi")
            Greeting(name: "Meena")
            Greeting(name: "Arun")
        }
    }
}
```

**Preview:**

```
Hello, Ravi! 👋
Hello, Meena! 👋
Hello, Arun! 👋
```

`Greeting(name: "Ravi")` uses the **automatic memberwise init** from Chapter 20! 🎉

💡 **Tip:** Make a new view whenever a part of the screen is **repeated** or **gets long**. Small views = easy to read and reuse.

---

## 11. What can `body` contain?

`body` must return **one** view. But containers like `VStack` hold many.

```swift
var body: some View {
    Text("One")
    Text("Two")
}
```

This works — SwiftUI puts them in a list automatically. But to control the layout, **always wrap** multiple views in a container (`VStack`, `HStack`, `ZStack` — Chapter 43).

You can also use `if` inside:

```swift
struct ContentView: View {
    let isMorning = true

    var body: some View {
        VStack {
            if isMorning {
                Text("Good morning ☀️")
            } else {
                Text("Good evening 🌙")
            }
        }
    }
}
```

And `for`-style repeating with `ForEach` (Chapter 48).

---

## 🏋️ Practice

1. Show your name with `.font(.largeTitle)` and a color you like.
2. Try the two padding/background examples from section 8. Explain the difference in your own words.
3. Make a yellow box inside an orange box inside a red box using padding and background.
4. Make a `Badge` view with a `text: String` property that shows the text with padding and a colored background. Use it 3 times with different texts.
5. Add a second `#Preview` in dark mode.

<details>
<summary>Click to see an answer for 3 and 4</summary>

```swift
// 3
Text("🎁")
    .padding()
    .background(.yellow)
    .padding()
    .background(.orange)
    .padding()
    .background(.red)

// 4
struct Badge: View {
    let text: String
    var body: some View {
        Text(text)
            .padding(8)
            .background(.mint)
    }
}

struct ContentView: View {
    var body: some View {
        VStack {
            Badge(text: "New")
            Badge(text: "Sale")
            Badge(text: "Hot 🔥")
        }
    }
}
```

</details>

---

## 🧠 Remember

- SwiftUI is **declarative**: describe **what**, not **how**.
- A view is a **struct** that follows `View` and has `var body: some View`.
- **Modifiers** (`.font()`, `.padding()`) return new, changed views.
- **Order of modifiers matters** — top to bottom.
- Split big screens into **small views**. Views can have properties.
- `#Preview` shows views in the Canvas.

---

⬅️ **Back:** [Chapter 40 — Debugging](../part-04-xcode/40-debugging.md)
➡️ **Next:** [Chapter 42 — Text, Image and Modifiers](42-text-image-modifiers.md)
