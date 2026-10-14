# Chapter 55 — Animations

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- How SwiftUI animates **changes in state**.
- `withAnimation { }` — explicit animations.
- `.animation(_:value:)` — implicit animations.
- Animation types: ease, spring, bouncy, duration, delay, repeat.
- Animatable modifiers: scale, rotation, opacity, offset, color.
- **Transitions**: how views appear and disappear.
- SF Symbol effects.
- Small polish: `.contentTransition`, haptics-style feedback.

💡 **Tip:** Animations only move in **Live** preview or in the Simulator. Click **▶ Live** in the Canvas.

---

## 1. The big idea 🎬

In SwiftUI, you **don't** draw each frame of an animation. You just change the **state**, and tell SwiftUI to **animate** the change.

```
   State before        State after
   size = 1.0    ──►   size = 2.0

   Without animation:  jumps instantly  🟦 → 🟦🟦
   With animation:     grows smoothly   🟦 → 🟦▫ → 🟦🟦
```

SwiftUI calculates all the **in-between** frames for you. ✨

> 📖 **New word: Animation**
> A smooth change from one look to another over time.

---

## 2. `withAnimation` — explicit animation

```swift
struct ContentView: View {
    @State private var isBig = false

    var body: some View {
        VStack(spacing: 40) {
            Circle()
                .fill(.blue)
                .frame(width: isBig ? 200 : 80, height: isBig ? 200 : 80)

            Button("Grow / Shrink") {
                withAnimation {
                    isBig.toggle()
                }
            }
            .buttonStyle(.borderedProminent)
        }
    }
}
```

**Try it:** Tap the button. The circle grows and shrinks **smoothly**. Remove `withAnimation` and try again — it **jumps**.

| Part | Meaning |
|---|---|
| `withAnimation { isBig.toggle() }` | "Change the state, and **animate** every view that changes because of it." |

> 📖 **New word: Explicit animation**
> You **say exactly** which change to animate, using `withAnimation`.

🧠 **Remember:** Put the **state change** inside `withAnimation { }`.

---

## 3. `.animation(_:value:)` — implicit animation

Attach an animation to a **view**. It animates whenever a certain **value** changes.

```swift
struct ContentView: View {
    @State private var isBig = false

    var body: some View {
        VStack(spacing: 40) {
            Circle()
                .fill(isBig ? .orange : .blue)
                .frame(width: isBig ? 200 : 80, height: isBig ? 200 : 80)
                .animation(.spring, value: isBig)

            Button("Toggle") {
                isBig.toggle()       // no withAnimation needed
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `.animation(.spring, value: isBig)` | "When `isBig` changes, animate the changes **above this line** with a spring." |

> 📖 **New word: Implicit animation**
> The view **automatically** animates when a watched value changes.

⚠️ **Careful:** `.animation` affects modifiers **above** it (Chapter 41: order matters!).

| | `withAnimation { }` | `.animation(_, value:)` |
|---|---|---|
| Where | Around the **state change** (in a button action) | On the **view** |
| Animates | Every view affected by that change | Only this view, when `value` changes |
| Good for | Button taps, one-off actions | A view that should always animate a certain change |

---

## 4. Animation types ⏱️

```swift
withAnimation(.easeInOut(duration: 1.0)) { ... }
```

| Animation | Feels like |
|---|---|
| `.default` | SwiftUI's standard (a smooth spring). |
| `.linear` | Constant speed, like a robot 🤖. |
| `.easeIn` | Starts slow, ends fast. |
| `.easeOut` | Starts fast, ends slow — like a ball rolling to a stop. |
| `.easeInOut` | Slow → fast → slow. Very natural. |
| `.spring` | Moves like a spring — a natural bounce at the end. ⭐ |
| `.bouncy` | More bounce! 🏀 |
| `.snappy` | Quick, with a tiny bounce. |
| `.smooth` | Smooth, no bounce. |

### Changing duration and bounce

```swift
.easeInOut(duration: 2)                 // takes 2 seconds
.spring(duration: 0.6, bounce: 0.5)     // more bounce (0 = none, 1 = lots)
.bouncy(duration: 0.5, extraBounce: 0.2)
```

### Delay, speed, repeat

```swift
.easeInOut.delay(0.5)                       // wait 0.5 s before starting
.easeInOut.speed(2)                         // twice as fast
.easeInOut(duration: 1).repeatCount(3)      // do it 3 times
.easeInOut(duration: 1).repeatForever(autoreverses: true)   // forever, back and forth
```

### Try them all!

```swift
struct ContentView: View {
    @State private var moveRight = false

    let animations: [(String, Animation)] = [
        ("linear", .linear(duration: 1)),
        ("easeInOut", .easeInOut(duration: 1)),
        ("spring", .spring(duration: 1)),
        ("bouncy", .bouncy(duration: 1, extraBounce: 0.3))
    ]

    var body: some View {
        VStack(alignment: .leading, spacing: 24) {
            ForEach(animations, id: \.0) { name, animation in
                VStack(alignment: .leading) {
                    Text(name).font(.caption)
                    Circle()
                        .fill(.purple)
                        .frame(width: 30, height: 30)
                        .offset(x: moveRight ? 250 : 0)
                        .animation(animation, value: moveRight)
                }
            }
            Button("Go!") { moveRight.toggle() }
                .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```

| New thing | Meaning |
|---|---|
| `[(String, Animation)]` | An array of **tuples** (Chapter 18). |
| `id: \.0` | Use the first part of each tuple (the name) as the ID. |
| `{ name, animation in ... }` | Take the two parts of the tuple. |

Tap **Go!** and compare how each circle moves. 🏁

---

## 5. What can be animated?

Almost any change to a **number-like** value:

| Modifier | Animates |
|---|---|
| `.frame(width:height:)` | Size |
| `.scaleEffect(1.5)` | Grow/shrink (without changing layout) |
| `.rotationEffect(.degrees(180))` | Spin |
| `.rotation3DEffect(.degrees(180), axis: (x: 0, y: 1, z: 0))` | 3D flip! 🃏 |
| `.opacity(0.2)` | Fade |
| `.offset(x:y:)` | Move |
| `.foregroundStyle(color)` / `.fill(color)` | Color |
| `.blur(radius: 10)` | Blur |
| `.cornerRadius` / shapes | Shape changes |
| `.padding()` | Spacing |

### Example: a spinning, growing star

```swift
struct ContentView: View {
    @State private var animate = false

    var body: some View {
        VStack(spacing: 50) {
            Image(systemName: "star.fill")
                .font(.system(size: 80))
                .foregroundStyle(animate ? .yellow : .gray)
                .scaleEffect(animate ? 1.5 : 1.0)
                .rotationEffect(.degrees(animate ? 360 : 0))
                .opacity(animate ? 1 : 0.5)

            Button("Animate ⭐") {
                withAnimation(.spring(duration: 0.8, bounce: 0.4)) {
                    animate.toggle()
                }
            }
            .buttonStyle(.borderedProminent)
        }
    }
}
```

All four changes animate **together** with one `withAnimation`. 🌟

### Example: card flip 🃏

```swift
struct ContentView: View {
    @State private var flipped = false

    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: 20)
                .fill(flipped ? .green : .blue)
                .frame(width: 200, height: 280)
            Text(flipped ? "🎉" : "?")
                .font(.system(size: 80))
                .rotation3DEffect(.degrees(flipped ? 180 : 0), axis: (x: 0, y: 1, z: 0))
        }
        .rotation3DEffect(.degrees(flipped ? 180 : 0), axis: (x: 0, y: 1, z: 0))
        .onTapGesture {
            withAnimation(.easeInOut(duration: 0.6)) {
                flipped.toggle()
            }
        }
    }
}
```

(The text is flipped **again** inside so it doesn't appear mirrored. 🪞)

---

## 6. Repeating animations (pulse, breathe) 💓

```swift
struct ContentView: View {
    @State private var pulse = false

    var body: some View {
        Image(systemName: "heart.fill")
            .font(.system(size: 100))
            .foregroundStyle(.red)
            .scaleEffect(pulse ? 1.2 : 1.0)
            .animation(.easeInOut(duration: 0.6).repeatForever(autoreverses: true), value: pulse)
            .onAppear {
                pulse = true
            }
    }
}
```

| Part | Meaning |
|---|---|
| `.repeatForever(autoreverses: true)` | Go to the end, come back, repeat forever. |
| `.onAppear { pulse = true }` | Start the animation when the view appears. |

---

## 7. Transitions — appearing and disappearing 🚪

When a view is **added** or **removed** (with `if`), a **transition** decides **how** it comes in and goes out.

```swift
struct ContentView: View {
    @State private var showBox = false

    var body: some View {
        VStack(spacing: 30) {
            Button(showBox ? "Hide" : "Show") {
                withAnimation {
                    showBox.toggle()
                }
            }
            .buttonStyle(.borderedProminent)

            if showBox {
                RoundedRectangle(cornerRadius: 16)
                    .fill(.mint)
                    .frame(width: 200, height: 120)
                    .transition(.scale)
            }

            Spacer()
        }
        .padding()
    }
}
```

| Part | Meaning |
|---|---|
| `if showBox { ... }` | The view is **added** or **removed**. |
| `.transition(.scale)` | Grow in from nothing, shrink out to nothing. |
| `withAnimation` | **Needed!** Without it, transitions don't animate. |

> 📖 **New word: Transition**
> How a view **enters** or **leaves** the screen.

### Transition types

| Transition | Effect |
|---|---|
| `.opacity` | Fade in/out (default). |
| `.scale` | Grow/shrink. |
| `.slide` | Slide in from the leading edge, out to the trailing edge. |
| `.move(edge: .bottom)` | Slide from/to an edge (`.top`, `.bottom`, `.leading`, `.trailing`). |
| `.push(from: .trailing)` | Push in like a new card. |
| `.blurReplace` | Blur in/out. |

### Combining transitions

```swift
.transition(.scale.combined(with: .opacity))
```

### Different in and out

```swift
.transition(.asymmetric(insertion: .move(edge: .bottom),
                        removal: .opacity))
```

| Part | Meaning |
|---|---|
| `.asymmetric(insertion:removal:)` | **Enter** one way, **leave** another way. |

---

## 8. Animating lists

Adding and removing items in a `List` or `ForEach` animates when you use `withAnimation`:

```swift
struct ContentView: View {
    @State private var items = ["🍎", "🍌", "🍇"]
    let pool = ["🍓", "🍍", "🥝", "🍑", "🍒", "🥭"]

    var body: some View {
        VStack {
            HStack {
                Button("Add") {
                    withAnimation(.bouncy) {
                        items.insert(pool.randomElement()!, at: 0)
                    }
                }
                Button("Shuffle") {
                    withAnimation(.spring) {
                        items.shuffle()
                    }
                }
            }
            .buttonStyle(.bordered)

            List {
                ForEach(items, id: \.self) { item in
                    Text(item).font(.largeTitle)
                }
                .onDelete { offsets in
                    withAnimation { items.remove(atOffsets: offsets) }
                }
            }
        }
    }
}
```

(Because we use `id: \.self`, duplicate fruits may confuse the animation — Chapter 48. Using `Identifiable` items is better for real apps.)

---

## 9. SF Symbol effects ✨

SF Symbols have **built-in** animations:

```swift
struct ContentView: View {
    @State private var bellTaps = 0
    @State private var isOn = false

    var body: some View {
        VStack(spacing: 40) {
            Image(systemName: "bell.fill")
                .font(.system(size: 60))
                .symbolEffect(.bounce, value: bellTaps)
                .onTapGesture { bellTaps += 1 }

            Image(systemName: "wifi")
                .font(.system(size: 60))
                .symbolEffect(.variableColor.iterative, isActive: isOn)
                .onTapGesture { isOn.toggle() }

            Image(systemName: isOn ? "speaker.wave.3.fill" : "speaker.slash.fill")
                .font(.system(size: 60))
                .contentTransition(.symbolEffect(.replace))
                .onTapGesture { withAnimation { isOn.toggle() } }
        }
    }
}
```

| Effect | What it does |
|---|---|
| `.symbolEffect(.bounce, value: x)` | Bounce once each time `x` changes. 🔔 |
| `.symbolEffect(.pulse)` | Gently pulse. |
| `.symbolEffect(.variableColor.iterative, isActive:)` | Animate the parts one by one (great for Wi-Fi, speaker). |
| `.contentTransition(.symbolEffect(.replace))` | Smoothly morph from one symbol to another. |

(Newer iOS versions add even more effects, like `.wiggle` and `.rotate`.)

### Animating numbers

```swift
Text("\(score)")
    .font(.system(size: 60, weight: .bold))
    .contentTransition(.numericText())
```

With `withAnimation { score += 1 }`, the digits **roll** like a scoreboard! 🔢

---

## 10. Gesture-driven animation (drag) 👆

```swift
struct ContentView: View {
    @State private var dragOffset = CGSize.zero

    var body: some View {
        Circle()
            .fill(.orange.gradient)
            .frame(width: 100, height: 100)
            .offset(dragOffset)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        dragOffset = value.translation
                    }
                    .onEnded { _ in
                        withAnimation(.bouncy) {
                            dragOffset = .zero
                        }
                    }
            )
    }
}
```

| Part | Meaning |
|---|---|
| `DragGesture()` | Follow the finger as it drags. |
| `.onChanged { value in ... }` | While dragging: move the circle with the finger. |
| `value.translation` | How far the finger moved from where it started. |
| `.onEnded { _ in ... }` | When the finger lifts: **bounce** back to the center. 🏀 |
| `CGSize.zero` | A size of width 0, height 0 — "no offset". |

---

## 11. Animation tips 💡

| Tip | Why |
|---|---|
| Keep animations **short** (0.2–0.5 s). | Long animations feel slow. |
| Use `.spring` / `.bouncy` / `.snappy`. | They feel natural and alive. |
| Animate with **purpose**. | Show what changed, guide the eye. Don't animate everything! |
| Respect **Reduce Motion**. | Some people feel sick with motion. ♿ |

### Respecting Reduce Motion

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

// ...
withAnimation(reduceMotion ? nil : .bouncy) {
    showBox.toggle()
}
```

If the user turned on **Reduce Motion** in Settings, no animation is used. ♿

---

## 12. Mini project: a tap game 🎯

```swift
struct ContentView: View {
    @State private var score = 0
    @State private var targetPosition = CGPoint(x: 150, y: 250)
    @State private var targetColor = Color.red
    @State private var showPlus = false
    @State private var bounce = 0

    let colors: [Color] = [.red, .orange, .green, .blue, .purple, .pink]

    var body: some View {
        GeometryReader { geo in
            ZStack {
                Color(.systemGroupedBackground).ignoresSafeArea()

                VStack {
                    Text("\(score)")
                        .font(.system(size: 64, weight: .heavy, design: .rounded))
                        .contentTransition(.numericText())
                    Text("Tap the circle!")
                        .foregroundStyle(.secondary)
                    Spacer()
                }
                .padding(.top)

                Circle()
                    .fill(targetColor.gradient)
                    .frame(width: 80, height: 80)
                    .overlay(
                        Image(systemName: "hand.tap.fill")
                            .foregroundStyle(.white)
                            .font(.title)
                            .symbolEffect(.bounce, value: bounce)
                    )
                    .shadow(radius: 6)
                    .position(targetPosition)
                    .onTapGesture {
                        hit(in: geo.size)
                    }

                if showPlus {
                    Text("+1")
                        .font(.largeTitle.bold())
                        .foregroundStyle(.green)
                        .position(x: targetPosition.x, y: targetPosition.y - 60)
                        .transition(.move(edge: .bottom).combined(with: .opacity))
                }
            }
        }
    }

    func hit(in size: CGSize) {
        withAnimation(.snappy) {
            score += 1
            showPlus = true
            bounce += 1
        }
        withAnimation(.spring(duration: 0.5, bounce: 0.4)) {
            targetPosition = CGPoint(
                x: CGFloat.random(in: 60...(size.width - 60)),
                y: CGFloat.random(in: 180...(size.height - 80))
            )
            targetColor = colors.randomElement()!
        }
        withAnimation(.easeOut.delay(0.4)) {
            showPlus = false
        }
    }
}
```

| Part | What it does |
|---|---|
| `GeometryReader { geo in ... }` | Gets the screen size, so the circle stays on screen (Chapter 44). |
| `.position(targetPosition)` | Place the circle at an exact point (a good use of `.position` — a game!). |
| `hit(in:)` | Adds a point, shows "+1", bounces the icon, and moves the circle. |
| `CGFloat.random(in:)` | A random position. |
| `.contentTransition(.numericText())` | The score rolls up. |
| `.easeOut.delay(0.4)` | Hide "+1" a little later. |

Tap as fast as you can! 🏃‍♂️💨

---

## 🏋️ Practice

1. Make a square that changes from blue to red and gets bigger when tapped, using `withAnimation`.
2. Make the same with `.animation(_:value:)` instead.
3. Make a button that rotates an arrow icon 180° each tap (`chevron.down` pointing up and down).
4. Make a heart that pulses forever.
5. Show/hide a text with `.transition(.move(edge: .top).combined(with: .opacity))`.
6. Make a counter whose number rolls with `.contentTransition(.numericText())`.
7. Make a draggable card that springs back when released.

---

## 🧠 Remember

- Change **state** → SwiftUI animates the in-between frames.
- `withAnimation(.spring) { state change }` — explicit.
- `.animation(.spring, value: x)` — implicit, on the view.
- Types: `.easeInOut`, `.spring`, `.bouncy`, `.snappy`, plus `duration`, `.delay()`, `.repeatForever()`.
- Animate scale, rotation, opacity, offset, color, size…
- `.transition(...)` + `withAnimation` for views appearing/disappearing.
- `.symbolEffect(...)` and `.contentTransition(...)` for symbols and numbers.
- Keep animations short and respect **Reduce Motion**.

---

## 🎉 Part 5 complete!

You can now build **real SwiftUI screens**:

- Text, images, stacks, padding and frames.
- Buttons and every input control.
- `@State`, `@Binding` and `@Observable` — the three ways to manage data.
- Lists, navigation, tabs, sheets and alerts.
- Colors, dark mode, fonts and animations.

That's a **huge** amount! 🏆

In **Part 6**, you'll learn real app skills: **saving data**, **loading from the internet**, **reading JSON** — and you'll build three complete apps: a **To-Do list**, a **Weather app** and a **Notes app**. Then you'll learn **testing** and how to put your app on the **App Store**! 🚀

---

⬅️ **Back:** [Chapter 54 — Colors, Fonts and Dark Mode](54-colors-fonts-dark-mode.md)
➡️ **Next:** Chapter 56 — Saving Small Data (`@AppStorage`) *(coming soon)*
