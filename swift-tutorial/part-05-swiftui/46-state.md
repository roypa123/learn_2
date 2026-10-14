# Chapter 46 — `@State`: Making Screens Change

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- Why a normal `var` doesn't work in a view.
- What `@State` does.
- How SwiftUI **redraws** the screen when state changes.
- Building a **counter**, a **toggle**, and more.
- Rules for using `@State`.
- `.onChange` — reacting to changes.

⭐ This is one of the **most important** chapters in SwiftUI. Take your time!

---

## 1. The problem

Let's make a counter. Tap the button → the number goes up.

```swift
struct ContentView: View {
    var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Add 1") {
                count += 1     // ❌ ERROR
            }
        }
    }
}
```

**Error:**

```
Left side of mutating operator isn't mutable: 'self' is immutable
```

Why? Remember Chapter 20: a **struct** can't change its own properties without `mutating`. And SwiftUI views are structs that are **recreated** all the time — a normal `var` would be lost anyway.

We need a **special box** that:
1. **Lives outside** the view struct, so it isn't lost.
2. **Tells SwiftUI** to redraw the screen when it changes.

That box is `@State`.

---

## 2. `@State` to the rescue

```swift
struct ContentView: View {
    @State private var count = 0

    var body: some View {
        VStack(spacing: 20) {
            Text("Count: \(count)")
                .font(.largeTitle)

            Button("Add 1") {
                count += 1
            }
            .buttonStyle(.borderedProminent)
        }
    }
}

#Preview {
    ContentView()
}
```

**Try it:** Click **▶ Live** in the Canvas (or run the app). Tap the button. The number goes up! 🎉

| Part | Meaning |
|---|---|
| `@State` | "SwiftUI, please **keep** this value safe for me and **watch** it." |
| `private` | Only this view uses it. (Always write `private` with `@State`.) |
| `var count = 0` | Starting value. |
| `count += 1` | Change it. SwiftUI notices and **redraws** the view. |

> 📖 **New word: State**
> Data that can **change** over time and affects what the screen shows. Like the score in a game, or whether a light is on.

> 📖 **New word: Property wrapper**
> A word starting with `@` (like `@State`) that adds special behavior to a property.

---

## 3. What happens when you tap? 🔄

```
  1. You tap "Add 1"
          │
          ▼
  2. count changes: 0 → 1
          │
          ▼
  3. SwiftUI notices: "count changed!"
          │
          ▼
  4. SwiftUI runs `body` again
          │
          ▼
  5. Text now says "Count: 1"   ✅
```

🧠 **Remember:** You **never** update the screen yourself. You change the **state**, and SwiftUI updates the screen. The screen is always a **result** of the state.

```
     State  ──────►  body  ──────►  Screen
   (count = 1)     (describes)    ("Count: 1")
```

This is the heart of SwiftUI. 💙

---

## 4. Many buttons, one state

```swift
struct ContentView: View {
    @State private var count = 0

    var body: some View {
        VStack(spacing: 20) {
            Text("\(count)")
                .font(.system(size: 80, weight: .bold, design: .rounded))
                .foregroundStyle(count < 0 ? .red : .primary)

            HStack(spacing: 20) {
                Button("−") { count -= 1 }
                Button("Reset") { count = 0 }
                Button("+") { count += 1 }
            }
            .buttonStyle(.bordered)
            .font(.title)
        }
    }
}
```

| Part | Meaning |
|---|---|
| `count < 0 ? .red : .primary` | Red when negative, normal color otherwise (ternary — Chapter 10). |
| `.primary` | The normal text color (black in light mode, white in dark mode). |

Every time `count` changes, SwiftUI checks the color again. **Automatic!**

---

## 5. A `Bool` state: show / hide

```swift
struct ContentView: View {
    @State private var showSecret = false

    var body: some View {
        VStack(spacing: 20) {
            Button(showSecret ? "Hide secret" : "Show secret") {
                showSecret.toggle()
            }
            .buttonStyle(.borderedProminent)

            if showSecret {
                Text("🤫 SwiftUI is fun!")
                    .font(.title)
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `@State private var showSecret = false` | Hidden at the start. |
| `showSecret.toggle()` | Flip `true` ↔ `false`. (`toggle()` is a built-in Bool method.) |
| `if showSecret { ... }` | Only show the text when `true`. |
| Button title | Changes too, because it depends on `showSecret`. |

---

## 6. A `String` state

```swift
struct ContentView: View {
    @State private var mood = "😐"

    var body: some View {
        VStack(spacing: 30) {
            Text(mood)
                .font(.system(size: 120))

            HStack(spacing: 16) {
                Button("😊") { mood = "😊" }
                Button("😢") { mood = "😢" }
                Button("😡") { mood = "😡" }
                Button("😴") { mood = "😴" }
            }
            .font(.largeTitle)
        }
    }
}
```

Tap an emoji → the big emoji changes.

---

## 7. An array state

```swift
struct ContentView: View {
    @State private var fruits = ["🍎", "🍌"]

    let allFruits = ["🍎", "🍌", "🍇", "🍓", "🍍", "🥝", "🍑", "🍒"]

    var body: some View {
        VStack(spacing: 20) {
            Text(fruits.joined(separator: " "))
                .font(.largeTitle)

            Text("\(fruits.count) fruits")
                .foregroundStyle(.secondary)

            HStack {
                Button("Add random") {
                    fruits.append(allFruits.randomElement()!)
                }
                Button("Remove last") {
                    if !fruits.isEmpty {
                        fruits.removeLast()
                    }
                }
                .disabled(fruits.isEmpty)
            }
            .buttonStyle(.bordered)
        }
        .padding()
    }
}
```

| Part | Meaning |
|---|---|
| `@State private var fruits` | An array as state. Changing the array (append, remove) updates the screen. |
| `let allFruits` | A normal constant — it never changes, so it doesn't need `@State`. |
| `.randomElement()!` | A random item. Optional (empty arrays have none), but `allFruits` is never empty, so `!` is safe here. |
| `.disabled(fruits.isEmpty)` | Can't remove when there's nothing left. Updates automatically! |

---

## 8. A struct as state

```swift
struct Player {
    var name: String
    var score: Int
    var lives: Int
}

struct ContentView: View {
    @State private var player = Player(name: "Hero", score: 0, lives: 3)

    var body: some View {
        VStack(spacing: 16) {
            Text(player.name).font(.largeTitle.bold())
            Text("Score: \(player.score)")
            Text(String(repeating: "❤️", count: player.lives))
                .font(.title)

            HStack {
                Button("Collect coin 🪙") { player.score += 10 }
                Button("Get hit 💥") {
                    if player.lives > 0 { player.lives -= 1 }
                }
            }
            .buttonStyle(.bordered)

            if player.lives == 0 {
                Text("GAME OVER")
                    .font(.title.bold())
                    .foregroundStyle(.red)
                Button("Play again") {
                    player = Player(name: "Hero", score: 0, lives: 3)
                }
                .buttonStyle(.borderedProminent)
            }
        }
    }
}
```

Changing **any** property of the struct updates the screen. (Because structs are values — Chapter 22 — SwiftUI sees the whole value change.)

---

## 9. Rules for `@State` 📏

| Rule | Why |
|---|---|
| Always mark it `private` | `@State` belongs to **this** view only. |
| Give it a **starting value** | `@State private var count = 0` |
| Use it for **simple, local** data | Like "is this panel open?", "what did the user type?", a counter. |
| Use it with **value types** (Int, String, Bool, struct, array) | Classes need something else (`@Observable` — Chapter 53). |
| Don't use it for data that never changes | Use `let` instead. |
| Don't create a new value for `@State` from outside | The starting value is only used **once**. |

🧠 **Remember:** `@State` = **private**, **simple**, **owned by this view**.

To **share** state with a child view → `@Binding` (Chapter 52).
To share across **many** screens → `@Observable` (Chapter 53).

---

## 10. Computed properties from state

You don't need state for everything. If a value can be **calculated** from other state, use a **computed property** (Chapter 20):

```swift
struct ContentView: View {
    @State private var apples = 3
    @State private var oranges = 2

    var total: Int {
        apples + oranges
    }

    var message: String {
        total > 10 ? "That's a lot of fruit! 🧺" : "Keep shopping 🛒"
    }

    var body: some View {
        VStack(spacing: 12) {
            Stepper("🍎 Apples: \(apples)", value: $apples, in: 0...20)
            Stepper("🍊 Oranges: \(oranges)", value: $oranges, in: 0...20)
            Divider()
            Text("Total: \(total)").font(.title2.bold())
            Text(message)
        }
        .padding()
    }
}
```

| Part | Meaning |
|---|---|
| `var total: Int { apples + oranges }` | Calculated from state. **Not** `@State` itself. |
| `Stepper(..., value: $apples, ...)` | A − / + control. The `$` creates a **binding** — explained in the next chapter! |

🧠 **Remember:** Keep state **small**. Calculate everything else.

---

## 11. `.onChange` — react when state changes

Run some code **when** a value changes:

```swift
struct ContentView: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Add") { count += 1 }
        }
        .onChange(of: count) { oldValue, newValue in
            print("Count changed from \(oldValue) to \(newValue)")
            if newValue == 10 {
                print("🎉 You reached 10!")
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `.onChange(of: count)` | Watch `count`. |
| `{ oldValue, newValue in ... }` | Runs after each change, with the old and new values. |

💡 **Tip:** Use `.onChange` for **side effects** (saving, playing a sound, logging). Don't use it to calculate things for the screen — use computed properties for that.

---

## 12. Mini project: a tip calculator 💰

```swift
struct ContentView: View {
    @State private var bill = 1000
    @State private var tipPercent = 10
    @State private var people = 2

    let tipChoices = [0, 5, 10, 15, 20]

    var tip: Double {
        Double(bill) * Double(tipPercent) / 100
    }

    var total: Double {
        Double(bill) + tip
    }

    var perPerson: Double {
        total / Double(people)
    }

    var body: some View {
        VStack(spacing: 24) {
            Text("Tip Calculator 💰")
                .font(.largeTitle.bold())

            VStack {
                Text("Bill: ₹\(bill)")
                    .font(.title2)
                HStack {
                    Button("−100") { if bill >= 100 { bill -= 100 } }
                    Button("+100") { bill += 100 }
                }
                .buttonStyle(.bordered)
            }

            VStack {
                Text("Tip")
                    .font(.headline)
                HStack {
                    ForEach(tipChoices, id: \.self) { choice in
                        Button("\(choice)%") {
                            tipPercent = choice
                        }
                        .buttonStyle(.bordered)
                        .tint(choice == tipPercent ? .green : .gray)
                    }
                }
            }

            Stepper("People: \(people)", value: $people, in: 1...20)
                .padding(.horizontal)

            Divider()

            VStack(spacing: 8) {
                Text("Tip: ₹\(tip, specifier: "%.2f")")
                Text("Total: ₹\(total, specifier: "%.2f")")
                Text("Each person pays: ₹\(perPerson, specifier: "%.2f")")
                    .font(.title2.bold())
                    .foregroundStyle(.green)
            }
        }
        .padding()
    }
}
```

| Part | Meaning |
|---|---|
| Three `@State` values | The only things the user changes. |
| `tip`, `total`, `perPerson` | Computed from state — always correct. |
| `ForEach(tipChoices, id: \.self)` | Make one button per choice (Chapter 48). |
| `.tint(choice == tipPercent ? .green : .gray)` | The selected tip is green. |
| `\(tip, specifier: "%.2f")` | Show the Double with **2 decimal places**: `100.00`. |

> 📖 **New word: specifier `"%.2f"`**
> A format code: `%f` = a decimal number, `.2` = 2 digits after the dot.

---

## 🏋️ Practice

1. Make a counter that goes from 0 to 10 only. Disable "+" at 10 and "−" at 0.
2. Make a light bulb 💡: a button toggles `isOn`. Show `"lightbulb.fill"` in yellow when on, `"lightbulb"` in gray when off. Change the background to black when off.
3. Make a "dice roller" 🎲: a button picks a random number 1–6 (`Int.random(in: 1...6)`) and shows it big.
4. Make a "like" button: a heart that's filled and red when liked, empty when not. Show a like count that goes up and down.
5. Make a list of names in `@State`. Add a button that adds `"Guest \(names.count + 1)"`.
6. Add `.onChange` to the dice: print "🎉 Six!" when you roll a 6.

<details>
<summary>Click to see an answer for 2 and 4</summary>

```swift
// 2
struct ContentView: View {
    @State private var isOn = false

    var body: some View {
        ZStack {
            (isOn ? Color.white : Color.black)
                .ignoresSafeArea()
            Button {
                isOn.toggle()
            } label: {
                Image(systemName: isOn ? "lightbulb.fill" : "lightbulb")
                    .font(.system(size: 100))
                    .foregroundStyle(isOn ? .yellow : .gray)
            }
        }
    }
}

// 4
struct LikeButton: View {
    @State private var isLiked = false
    @State private var likes = 41

    var body: some View {
        Button {
            isLiked.toggle()
            likes += isLiked ? 1 : -1
        } label: {
            Label("\(likes)", systemImage: isLiked ? "heart.fill" : "heart")
                .foregroundStyle(isLiked ? .red : .gray)
                .font(.title)
        }
    }
}
```

</details>

---

## 🧠 Remember

- A normal `var` in a view **can't** change and wouldn't update the screen.
- `@State private var x = value` → SwiftUI **stores** it and **redraws** when it changes.
- You change the **state**; SwiftUI updates the **screen**. Screen = result of state.
- Use `@State` for simple, private data owned by **one** view.
- Calculate other values with **computed properties**.
- `.onChange(of:)` runs code when a value changes.

---

⬅️ **Back:** [Chapter 45 — Buttons](45-buttons.md)
➡️ **Next:** [Chapter 47 — Text Fields, Toggles, Sliders, Pickers](47-input-controls.md)
