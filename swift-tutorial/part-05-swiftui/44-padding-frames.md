# Chapter 44 — Spacing, Padding and Frames

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- How SwiftUI decides the **size** of views.
- `.padding()` in all its forms.
- `.frame()` — fixed size, min/max size, and **`.infinity`**.
- `.background()` and `.overlay()`.
- Rounded corners, borders and shadows.
- The **safe area**.
- `.offset()` and `.position()` (moving views).

---

## 1. How SwiftUI decides sizes 📏

This is the **secret rule** of SwiftUI layout. Once you understand it, layouts become easy.

It's a conversation in **3 steps**:

```
  1. PARENT:  "Here is the space I have. How big do you want to be?"
                     │
                     ▼
  2. CHILD:   "I'll be THIS big."  (the child decides!)
                     │
                     ▼
  3. PARENT:  "OK, I'll put you here."  (the parent places it)
```

Examples:

| View | How big it wants to be |
|---|---|
| `Text("Hi")` | Just big enough for its text. |
| `Image("photo")` (not resizable) | Its original size. |
| `Color.red`, `Rectangle()`, `Spacer()` | **As big as possible** — all space offered. |
| `VStack`/`HStack` | Just big enough for its children. |

🧠 **Remember:** **Parent offers, child chooses, parent places.**

---

## 2. `.padding()`

Adds **empty space** around a view.

```swift
Text("Hello")
    .padding()
    .background(.yellow)
```

| Form | Meaning |
|---|---|
| `.padding()` | Default space (about 16 points) on **all 4** sides. |
| `.padding(30)` | 30 points on all sides. |
| `.padding(.horizontal)` | Default space on **left and right** only. |
| `.padding(.vertical, 8)` | 8 points on **top and bottom** only. |
| `.padding(.top, 20)` | Only on top. Also `.bottom`, `.leading`, `.trailing`. |
| `.padding([.top, .leading], 10)` | Several sides at once (an array!). |
| `.padding(EdgeInsets(top: 1, leading: 2, bottom: 3, trailing: 4))` | Different amount on each side. |

```swift
VStack(spacing: 20) {
    Text("all").padding().background(.yellow)
    Text("horizontal").padding(.horizontal, 40).background(.orange)
    Text("top").padding(.top, 30).background(.pink)
}
```

> 📖 **New word: Point**
> The unit for sizes in SwiftUI (Chapter 34). About the size of a tiny dot. A normal button is about 44 points tall.

---

## 3. `.frame()` — fixed size

```swift
Text("Box")
    .frame(width: 200, height: 100)
    .background(.blue.opacity(0.3))
```

**Preview:** a 200×100 light blue box with "Box" in the center.

| Part | Meaning |
|---|---|
| `.frame(width: 200, height: 100)` | Make a 200×100 box **around** the text. The text stays its own size, centered inside. |

### Alignment inside a frame

```swift
Text("Top left")
    .frame(width: 200, height: 100, alignment: .topLeading)
    .background(.green.opacity(0.3))
```

Same alignment options as `ZStack` (Chapter 43): `.topLeading`, `.center`, `.bottomTrailing`, etc.

⚠️ **Careful:** `.frame()` doesn't stretch the **text** itself. It makes an invisible box **around** it. That's why order with `.background` matters:

```swift
Text("A").background(.red).frame(width: 100, height: 100)   // small red behind text only
Text("B").frame(width: 100, height: 100).background(.red)   // big red box 100×100
```

---

## 4. Flexible frames: `maxWidth: .infinity` ⭐

The **most useful** frame trick:

```swift
Text("Full width")
    .frame(maxWidth: .infinity)
    .padding()
    .background(.blue)
    .foregroundStyle(.white)
```

**Preview:** a blue bar stretching across the **whole** width of the screen.

| Part | Meaning |
|---|---|
| `maxWidth: .infinity` | "Be as wide as the parent allows." |

> 📖 **New word: `.infinity`**
> "As much as possible" — no limit.

| Frame | Meaning |
|---|---|
| `.frame(maxWidth: .infinity)` | Full width. |
| `.frame(maxHeight: .infinity)` | Full height. |
| `.frame(maxWidth: .infinity, maxHeight: .infinity)` | Fill everything. |
| `.frame(maxWidth: .infinity, alignment: .leading)` | Full width, content on the left. ⭐ |
| `.frame(minHeight: 50)` | At least 50 tall, more if needed. |
| `.frame(maxWidth: 400)` | Up to 400 wide (good for iPad — not too wide). |

### Full-width button

```swift
Text("Continue")
    .font(.headline)
    .frame(maxWidth: .infinity)
    .padding()
    .background(.blue)
    .foregroundStyle(.white)
    .clipShape(RoundedRectangle(cornerRadius: 12))
    .padding(.horizontal)
```

**Preview:** a big blue rounded "Continue" button across the screen, with a little space on the sides. (You'll make real buttons in Chapter 45.)

### Text on the left of a full row

```swift
VStack {
    Text("Name").frame(maxWidth: .infinity, alignment: .leading)
    Text("Email address").frame(maxWidth: .infinity, alignment: .leading)
}
.padding()
```

---

## 5. `.background()` and `.overlay()`

| Modifier | Puts the new view… |
|---|---|
| `.background(...)` | **behind** the view |
| `.overlay(...)` | **in front of** the view |

```swift
Text("Hello")
    .padding()
    .background(.yellow)                         // behind
    .overlay(alignment: .topTrailing) {          // in front
        Circle()
            .fill(.red)
            .frame(width: 12, height: 12)
    }
```

**Preview:** "Hello" on yellow, with a small red dot in the top-right corner.

Both can take **any view**, not just colors:

```swift
Text("Gradient background")
    .padding()
    .background(
        LinearGradient(colors: [.purple, .blue], startPoint: .leading, endPoint: .trailing)
    )
    .foregroundStyle(.white)
```

### Background with a shape

```swift
Text("Capsule")
    .padding(.horizontal, 20)
    .padding(.vertical, 10)
    .background(.mint, in: Capsule())
```

| Part | Meaning |
|---|---|
| `.background(.mint, in: Capsule())` | A mint background **shaped** like a capsule (pill). |

---

## 6. Corners, borders, shadows

```swift
VStack(spacing: 30) {
    Text("Rounded")
        .padding()
        .background(.orange)
        .clipShape(RoundedRectangle(cornerRadius: 12))

    Text("Border")
        .padding()
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(.blue, lineWidth: 2)
        )

    Text("Shadow")
        .padding()
        .background(.white)
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .shadow(color: .black.opacity(0.2), radius: 8, x: 0, y: 4)
}
.padding()
.background(.gray.opacity(0.1))
```

| Modifier | Effect |
|---|---|
| `.clipShape(RoundedRectangle(cornerRadius: 12))` | Cut the view into a rounded rectangle. |
| `.overlay(RoundedRectangle(...).stroke(.blue, lineWidth: 2))` | Draw a rounded **outline** on top. |
| `.border(.blue, width: 2)` | A simple **square** border (no rounded corners). |
| `.shadow(color:radius:x:y:)` | A shadow. `radius` = blur, `x`/`y` = move the shadow. |

> 📖 **New word: Stroke**
> Drawing only the **outline** of a shape (not filling it).

💡 **Tip:** Short form for rounded clipping: `.clipShape(.rect(cornerRadius: 12))`.

---

## 7. The safe area 📱

Modern iPhones have a **notch** or **Dynamic Island** at the top and a **home bar** at the bottom. SwiftUI keeps your content **away** from them automatically. This safe zone is called the **safe area**.

```
 ┌──────── ▬▬▬ ────────┐  ← Dynamic Island (not safe)
 │ ┌─────────────────┐ │
 │ │                 │ │
 │ │   SAFE AREA     │ │  ← your content goes here
 │ │                 │ │
 │ └─────────────────┘ │
 └──────── ─── ────────┘  ← home bar (not safe)
```

> 📖 **New word: Safe area**
> The part of the screen that isn't covered by the notch, Dynamic Island, status bar or home bar.

### Going outside the safe area

For **backgrounds** (colors, images), you usually want them to fill the **whole** screen:

```swift
ZStack {
    Color.indigo
        .ignoresSafeArea()      // color fills everything

    Text("Content stays safe")
        .foregroundStyle(.white)   // text stays inside the safe area
}
```

| Modifier | Meaning |
|---|---|
| `.ignoresSafeArea()` | This view goes **under** the notch and home bar. |
| `.ignoresSafeArea(edges: .top)` | Only ignore at the top. |

🧠 **Remember:** Let **backgrounds** ignore the safe area. Keep **text and buttons** inside it.

Even simpler for backgrounds:

```swift
VStack {
    Text("Hello")
}
.frame(maxWidth: .infinity, maxHeight: .infinity)
.background(.indigo)     // backgrounds extend into the safe area automatically in many cases
```

---

## 8. Moving views: `.offset()` and `.position()`

### `.offset()` — move it a little

```swift
Text("Moved")
    .background(.yellow)
    .offset(x: 30, y: -10)
```

| Part | Meaning |
|---|---|
| `x: 30` | 30 points to the **right**. Negative = left. |
| `y: -10` | 10 points **up**. Positive = down. ⚠️ (In SwiftUI, **y goes down**!) |

⚠️ **Careful:** `.offset` only moves where it's **drawn**. Other views still act like it's in its old place. Use it for small adjustments and animations.

### `.position()` — place it at exact coordinates

```swift
ZStack {
    Color.clear
    Text("Here!")
        .position(x: 100, y: 200)
}
```

`.position` puts the **center** of the view at (100, 200) inside its parent.

💡 **Tip:** Avoid `.position` for normal layouts. Stacks, `Spacer` and `frame` work on **all** screen sizes. `.position` is for special things like games or drawings.

---

## 9. `GeometryReader` (just so you know)

If you need to know the **exact size** of the available space:

```swift
GeometryReader { geometry in
    Text("Width: \(Int(geometry.size.width))")
        .frame(width: geometry.size.width / 2)
        .background(.yellow)
}
```

| Part | Meaning |
|---|---|
| `GeometryReader { geometry in ... }` | Gives you the size offered by the parent. |
| `geometry.size.width` | That width, in points. |

⚠️ **Careful:** `GeometryReader` takes **all** available space and can make layouts confusing. Beginners should use it rarely. Try stacks and frames first. Newer iOS versions also have `.containerRelativeFrame(...)` for some of these cases.

---

## 10. Mini project: a login card 🔐

```swift
struct ContentView: View {
    var body: some View {
        ZStack {
            LinearGradient(colors: [.orange, .pink],
                           startPoint: .topLeading,
                           endPoint: .bottomTrailing)
                .ignoresSafeArea()

            VStack(spacing: 16) {
                Image(systemName: "lock.shield.fill")
                    .font(.system(size: 60))
                    .foregroundStyle(.pink)

                Text("Welcome back!")
                    .font(.title.bold())

                Text("Please sign in to continue")
                    .foregroundStyle(.secondary)

                Text("Email")
                    .foregroundStyle(.secondary)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .overlay(
                        RoundedRectangle(cornerRadius: 10)
                            .stroke(.gray.opacity(0.4))
                    )

                Text("Password")
                    .foregroundStyle(.secondary)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .overlay(
                        RoundedRectangle(cornerRadius: 10)
                            .stroke(.gray.opacity(0.4))
                    )

                Text("Sign In")
                    .font(.headline)
                    .foregroundStyle(.white)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(.pink, in: RoundedRectangle(cornerRadius: 10))
            }
            .padding(24)
            .background(.white, in: RoundedRectangle(cornerRadius: 24))
            .shadow(radius: 20)
            .padding(24)
        }
    }
}
```

(The Email/Password boxes are just `Text` placeholders for now. In Chapter 47 we'll make real text fields!)

| Part | What it does |
|---|---|
| Gradient + `.ignoresSafeArea()` | Full-screen colorful background. |
| `.frame(maxWidth: .infinity, alignment: .leading)` | Fake input boxes fill the width, text on the left. |
| `.overlay(RoundedRectangle(...).stroke(...))` | Gray rounded border. |
| `.background(.white, in: RoundedRectangle(cornerRadius: 24))` | White rounded card. |
| `.padding(24)` (last) | Space between the card and the screen edges. |

---

## 🏋️ Practice

1. Make a `Text` with padding **only** on the leading side (40 points) and a yellow background.
2. Make a 150×150 square with text in the **bottom-trailing** corner.
3. Make a full-width green bar with white text aligned to the **left**.
4. Make a "chip" with text, a capsule background, and a thin border.
5. Make a card with rounded corners and a soft shadow, on a light gray background.
6. Make a full-screen color background with text that stays inside the safe area.

<details>
<summary>Click to see an answer for 2 and 4</summary>

```swift
// 2
Text("Corner")
    .frame(width: 150, height: 150, alignment: .bottomTrailing)
    .background(.teal.opacity(0.3))

// 4
Text("Swift")
    .padding(.horizontal, 14)
    .padding(.vertical, 6)
    .background(.blue.opacity(0.15), in: Capsule())
    .overlay(Capsule().stroke(.blue, lineWidth: 1))
```

</details>

---

## 🧠 Remember

- **Parent offers space, child chooses its size, parent places it.**
- `.padding()` adds space around a view (all sides, or chosen sides).
- `.frame(width:height:)` = fixed box. `.frame(maxWidth: .infinity)` = full width. ⭐
- `.background()` = behind. `.overlay()` = in front.
- `.clipShape(RoundedRectangle(cornerRadius:))`, `.stroke()`, `.shadow()` for cards.
- Backgrounds can `.ignoresSafeArea()`. Keep content inside the safe area.
- `.offset()` moves the drawing a little. Avoid `.position()` for normal layouts.

---

⬅️ **Back:** [Chapter 43 — Stacks](43-stacks.md)
➡️ **Next:** [Chapter 45 — Buttons](45-buttons.md)
