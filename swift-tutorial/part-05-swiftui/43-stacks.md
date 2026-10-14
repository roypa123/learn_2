# Chapter 43 — Stacks: `VStack`, `HStack`, `ZStack`

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- `VStack` — top to bottom.
- `HStack` — left to right.
- `ZStack` — on top of each other (front to back).
- **Alignment** and **spacing**.
- `Spacer` — pushing views apart.
- `Divider` — a thin line.
- Nesting stacks to build real layouts.
- `Grid` and `LazyVGrid` (a short introduction).

---

## 1. Three directions

```
   VStack            HStack             ZStack
   (vertical)        (horizontal)       (depth)

   ┌───┐             ┌───┬───┬───┐      ┌─────────┐
   │ A │             │ A │ B │ C │      │ ┌─────┐ │
   ├───┤             └───┴───┴───┘      │ │  C  │ │ ← front
   │ B │                                │ └─────┘ │
   ├───┤                                │    A    │ ← back
   │ C │                                └─────────┘
   └───┘
```

| Stack | Direction | Like |
|---|---|---|
| `VStack` | **V**ertical: top → bottom | A tower of books 📚 |
| `HStack` | **H**orizontal: left → right | Books on a shelf 📗📘📕 |
| `ZStack` | **Z**-axis: back → front | Stickers on top of each other 🖼️ |

> 📖 **New word: Stack**
> A container view that arranges other views in one direction.

---

## 2. `VStack`

```swift
VStack {
    Text("🍎 Apple")
    Text("🍌 Banana")
    Text("🍇 Grapes")
}
```

**Preview:**

```
 🍎 Apple
🍌 Banana
🍇 Grapes
```

(Centered by default.)

### Alignment

```swift
VStack(alignment: .leading) {
    Text("🍎 Apple")
    Text("🍌 Banana")
    Text("🍇 Grapes")
}
```

**Preview:**

```
🍎 Apple
🍌 Banana
🍇 Grapes
```

| Part | Meaning |
|---|---|
| `alignment: .leading` | Line up everything on the **leading** (left) side. |

| `VStack` alignment | Effect |
|---|---|
| `.leading` | left edge |
| `.center` | center (default) |
| `.trailing` | right edge |

### Spacing

```swift
VStack(spacing: 30) {
    Text("One")
    Text("Two")
    Text("Three")
}
```

| Part | Meaning |
|---|---|
| `spacing: 30` | 30 points of space **between** each view. |

Both together:

```swift
VStack(alignment: .leading, spacing: 4) { ... }
```

---

## 3. `HStack`

```swift
HStack {
    Image(systemName: "star.fill")
    Text("4.8")
    Text("(120 reviews)")
        .foregroundStyle(.secondary)
}
```

**Preview:**

```
★ 4.8 (120 reviews)
```

### Vertical alignment in an HStack

```swift
HStack(alignment: .top) {
    Text("Small")
    Text("BIG").font(.largeTitle)
    Text("Small")
}
```

| `HStack` alignment | Effect |
|---|---|
| `.top` | line up the tops |
| `.center` | middle (default) |
| `.bottom` | line up the bottoms |
| `.firstTextBaseline` | line up the bottom of the **letters** — looks best with different font sizes ⭐ |

> 📖 **New word: Baseline**
> The invisible line that letters "sit" on, like the lines in a school notebook.

---

## 4. `ZStack`

Views are placed **on top** of each other. The **last** one is in **front**.

```swift
ZStack {
    Circle()
        .fill(.blue)
        .frame(width: 150, height: 150)

    Text("Hi!")
        .font(.largeTitle)
        .foregroundStyle(.white)
}
```

**Preview:** a blue circle with white "Hi!" in the middle. 🔵

| Line | Position |
|---|---|
| `Circle()` | First → at the **back**. |
| `Text("Hi!")` | Last → in **front**. |

> 📖 **New word: `Circle()`**
> A built-in **shape**. Others: `Rectangle()`, `RoundedRectangle(cornerRadius: 12)`, `Capsule()`, `Ellipse()`. Use `.fill(color)` to color it.

### ZStack alignment

```swift
ZStack(alignment: .topTrailing) {
    RoundedRectangle(cornerRadius: 16)
        .fill(.gray.opacity(0.3))
        .frame(width: 150, height: 100)

    Text("NEW")
        .font(.caption.bold())
        .padding(6)
        .background(.red)
        .foregroundStyle(.white)
}
```

**Preview:** a gray rounded box with a red "NEW" tag in the top-right corner.

| `ZStack` alignment | Position |
|---|---|
| `.topLeading`, `.top`, `.topTrailing` | top row |
| `.leading`, `.center`, `.trailing` | middle row |
| `.bottomLeading`, `.bottom`, `.bottomTrailing` | bottom row |

| New thing | Meaning |
|---|---|
| `.opacity(0.3)` | 30% visible (quite see-through). 0 = invisible, 1 = solid. |

### A background color for the whole screen

```swift
ZStack {
    Color.mint
        .ignoresSafeArea()

    Text("Full screen color!")
        .font(.title)
}
```

| Part | Meaning |
|---|---|
| `Color.mint` | A color is also a **view**! It fills all available space. |
| `.ignoresSafeArea()` | Go behind the notch and home bar too (Chapter 44). |

---

## 5. `Spacer` — push things apart

> 📖 **New word: Spacer**
> An invisible, stretchy view that takes up **all the free space**.

```swift
HStack {
    Text("Left")
    Spacer()
    Text("Right")
}
.padding()
```

**Preview:**

```
Left                        Right
```

`Spacer()` pushes `Left` to the left edge and `Right` to the right edge.

### More examples

```swift
// Push to the right
HStack {
    Spacer()
    Text("I'm on the right")
}

// Center between two spacers
HStack {
    Spacer()
    Text("Centered")
    Spacer()
}

// In a VStack: push content to the top
VStack {
    Text("At the top")
    Spacer()
}
```

```
 HStack { Text  Spacer  Text }
 ┌────────────────────────────────┐
 │ Left  ←── Spacer stretches ──→ Right │
 └────────────────────────────────┘
```

### Minimum length

```swift
Spacer(minLength: 20)    // at least 20 points, more if possible
```

---

## 6. `Divider` — a thin line

```swift
VStack {
    Text("Section 1")
    Divider()
    Text("Section 2")
}
```

In a `VStack`, the line is **horizontal**. In an `HStack`, it's **vertical**.

---

## 7. Nesting stacks 🪆

Real layouts use stacks **inside** stacks.

### Example: a contact row

```swift
HStack(spacing: 12) {
    Image(systemName: "person.circle.fill")
        .font(.system(size: 44))
        .foregroundStyle(.blue)

    VStack(alignment: .leading) {
        Text("Ravi Kumar")
            .font(.headline)
        Text("+91 98765 43210")
            .font(.subheadline)
            .foregroundStyle(.secondary)
    }

    Spacer()

    Image(systemName: "phone.fill")
        .foregroundStyle(.green)
}
.padding()
```

**Preview:**

```
 👤  Ravi Kumar                  📞
     +91 98765 43210
```

Plan it as boxes first:

```
 HStack ────────────────────────────────────────────┐
 │ Image │ VStack(leading) ──┐ │ Spacer │ Image     │
 │  👤   │  Ravi Kumar        │ │ ←───→  │  📞       │
 │       │  +91 98765...      │ │        │           │
 │       └────────────────────┘ │        │           │
 └──────────────────────────────────────────────────┘
```

💡 **Tip:** Before coding, **draw** your screen on paper as boxes. Mark each box as V, H or Z. Then write the code. ✏️

---

## 8. Making a card component

```swift
struct ProductCard: View {
    let emoji: String
    let name: String
    let price: Int

    var body: some View {
        VStack(spacing: 8) {
            Text(emoji)
                .font(.system(size: 60))
            Text(name)
                .font(.headline)
            Text("₹\(price)")
                .foregroundStyle(.green)
                .bold()
        }
        .padding()
        .background(.gray.opacity(0.15))
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }
}

struct ContentView: View {
    var body: some View {
        HStack(spacing: 16) {
            ProductCard(emoji: "🍕", name: "Pizza", price: 250)
            ProductCard(emoji: "🍔", name: "Burger", price: 120)
        }
    }
}
```

| New thing | Meaning |
|---|---|
| `.clipShape(RoundedRectangle(cornerRadius: 16))` | Round the corners of the card. |

---

## 9. Too many items? `ScrollView`

If a stack has more items than fit on screen, wrap it in a `ScrollView`:

```swift
ScrollView {
    VStack(spacing: 12) {
        ForEach(1...50, id: \.self) { number in
            Text("Item \(number)")
        }
    }
}
```

| Part | Meaning |
|---|---|
| `ScrollView { }` | The content can scroll up and down. |
| `ForEach(1...50, id: \.self)` | Repeat a view 50 times (Chapter 48 explains `ForEach`). |

Horizontal scrolling:

```swift
ScrollView(.horizontal) {
    HStack {
        ForEach(1...20, id: \.self) { n in
            Text("\(n)")
                .frame(width: 60, height: 60)
                .background(.orange)
        }
    }
}
```

---

## 10. Grids (introduction)

### `Grid` — a small table

```swift
Grid(horizontalSpacing: 20, verticalSpacing: 10) {
    GridRow {
        Text("Name").bold()
        Text("Score").bold()
    }
    GridRow {
        Text("Ravi")
        Text("78")
    }
    GridRow {
        Text("Meena")
        Text("92")
    }
}
```

**Preview:**

```
Name    Score
Ravi     78
Meena    92
```

### `LazyVGrid` — many items in columns

```swift
let columns = [
    GridItem(.flexible()),
    GridItem(.flexible()),
    GridItem(.flexible())
]

ScrollView {
    LazyVGrid(columns: columns, spacing: 16) {
        ForEach(1...30, id: \.self) { n in
            Text("\(n)")
                .frame(maxWidth: .infinity, minHeight: 60)
                .background(.blue.opacity(0.2))
                .clipShape(RoundedRectangle(cornerRadius: 8))
        }
    }
    .padding()
}
```

| Part | Meaning |
|---|---|
| `GridItem(.flexible())` | One column that stretches to share space. 3 items = 3 columns. |
| `LazyVGrid` | A vertical grid. "Lazy" = only creates the views you can **see** (fast with many items). |
| `.frame(maxWidth: .infinity)` | Fill the column's width (Chapter 44). |

> 📖 **New word: Lazy**
> Creates views only when they're about to appear on screen. Saves memory with long lists. Also: `LazyVStack`, `LazyHStack`.

---

## 11. Mini project: a weather card 🌤️

```swift
struct ContentView: View {
    var body: some View {
        ZStack {
            LinearGradient(colors: [.blue, .cyan],
                           startPoint: .top,
                           endPoint: .bottom)
                .ignoresSafeArea()

            VStack(spacing: 16) {
                Text("Chennai")
                    .font(.largeTitle.bold())

                Image(systemName: "cloud.sun.fill")
                    .symbolRenderingMode(.multicolor)
                    .font(.system(size: 100))

                Text("31°")
                    .font(.system(size: 80, weight: .thin))

                Text("Partly cloudy")
                    .font(.title3)

                Divider()
                    .background(.white)

                HStack {
                    VStack {
                        Text("Mon")
                        Image(systemName: "sun.max.fill")
                        Text("33°")
                    }
                    Spacer()
                    VStack {
                        Text("Tue")
                        Image(systemName: "cloud.rain.fill")
                        Text("28°")
                    }
                    Spacer()
                    VStack {
                        Text("Wed")
                        Image(systemName: "cloud.bolt.fill")
                        Text("27°")
                    }
                }
                .font(.title3)
            }
            .foregroundStyle(.white)
            .padding(30)
        }
    }
}
```

| Part | Layout |
|---|---|
| `ZStack` | Gradient at the back, content in front. |
| Big `VStack` | City, icon, temperature, description, divider, forecast — top to bottom. |
| `HStack` with `Spacer`s | Three days spread across the width. |
| Small `VStack`s | Each day: name, icon, temperature. |
| `.foregroundStyle(.white)` on the `VStack` | Makes **all** text and icons inside white. |

---

## 🏋️ Practice

1. Make a `VStack` with 4 texts, aligned **leading**, with spacing 20.
2. Make an `HStack` with an icon on the left, a title, and a `Spacer` and a "›" chevron (`Image(systemName: "chevron.right")`) on the right — like a Settings row.
3. Make a `ZStack` with a red circle and a white number "3" on top — like a notification badge.
4. Build this layout:
   ```
   ┌─────────────────────────┐
   │ 🧑  Arun         [Follow]│
   │     @arun_codes          │
   ├─────────────────────────┤
   │ 120 Posts  4K Followers  │
   └─────────────────────────┘
   ```
5. Make a 2-column `LazyVGrid` of 10 emoji cards.

<details>
<summary>Click to see an answer for 3</summary>

```swift
ZStack {
    Circle()
        .fill(.red)
        .frame(width: 40, height: 40)
    Text("3")
        .font(.headline)
        .foregroundStyle(.white)
}
```

</details>

---

## 🧠 Remember

- `VStack` ↓, `HStack` →, `ZStack` ⬆ (back to front — last is in front).
- `alignment:` and `spacing:` control the layout.
- `Spacer()` takes all free space and pushes views apart.
- `Divider()` draws a thin line.
- **Nest** stacks to build any layout. Draw boxes on paper first.
- `ScrollView` for content that's too long. `LazyVGrid` for grids.

---

⬅️ **Back:** [Chapter 42 — Text, Image and Modifiers](42-text-image-modifiers.md)
➡️ **Next:** [Chapter 44 — Spacing, Padding and Frames](44-padding-frames.md)
