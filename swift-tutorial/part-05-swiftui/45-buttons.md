# Chapter 45 — Buttons

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- Making a `Button` with an **action**.
- Buttons with custom **labels** (icons, stacks…).
- Built-in **button styles**.
- **Roles** (destructive, cancel).
- Disabling a button.
- `onTapGesture` and other gestures.

---

## 1. Your first button

```swift
Button("Tap me") {
    print("Button was tapped! 🎉")
}
```

| Part | Meaning |
|---|---|
| `Button` | A view that does something when tapped. |
| `"Tap me"` | The text on the button. |
| `{ print(...) }` | The **action**: a **trailing closure** (Chapter 19) that runs on each tap. |

> 📖 **New word: Action**
> The code that runs when the user taps a button.

**Test it:**
- In the **Canvas**: click the **▶ Live** button at the bottom, then click your button. (Live previews may not show `print` output.)
- Or **run** the app (`Cmd + R`), tap the button, and look in the **Console** (`Cmd + Shift + Y`).

⚠️ **Careful:** Right now the button can only `print`. To **change the screen** when tapped, we need `@State` — that's the next chapter! 🔜

---

## 2. Calling a function

For longer actions, call a function:

```swift
struct ContentView: View {
    var body: some View {
        Button("Say hello", action: sayHello)
    }

    func sayHello() {
        print("Hello!")
        print("Have a great day ☀️")
    }
}
```

| Part | Meaning |
|---|---|
| `action: sayHello` | Pass the function itself — no `()`! (Chapter 19: storing a function.) |

---

## 3. Custom labels

The text form is a shortcut. The full form has **two closures**: the **action** and the **label**.

```swift
Button {
    print("Liked!")
} label: {
    Label("Like", systemImage: "heart.fill")
}
```

| Part | Meaning |
|---|---|
| First `{ }` | The **action**. |
| `label: { }` | **What the button looks like** — any view! |

> 📖 **New word: Multiple trailing closures**
> When a function takes several closures, you write the first one after `()` and the others with their labels: `} label: {`.

### Any view can be a label

```swift
Button {
    print("Play!")
} label: {
    VStack {
        Image(systemName: "play.circle.fill")
            .font(.system(size: 60))
        Text("Play")
            .font(.headline)
    }
}
```

### Icon-only button

```swift
Button {
    print("Settings")
} label: {
    Image(systemName: "gearshape.fill")
        .font(.title)
}
.accessibilityLabel("Settings")
```

⚠️ **Careful:** Icon-only buttons need an `.accessibilityLabel`, so VoiceOver can say what the button does. ♿

---

## 4. Button styles 🎨

SwiftUI has ready-made styles:

```swift
VStack(spacing: 20) {
    Button("Automatic (default)") { }

    Button("Bordered") { }
        .buttonStyle(.bordered)

    Button("Bordered Prominent") { }
        .buttonStyle(.borderedProminent)

    Button("Borderless") { }
        .buttonStyle(.borderless)

    Button("Plain") { }
        .buttonStyle(.plain)
}
```

| Style | Looks like |
|---|---|
| (default) | Blue (accent color) text. |
| `.bordered` | Text with a light, tinted background. |
| `.borderedProminent` | Solid colored background, white text. ⭐ Main action. |
| `.borderless` | Text only, no background. |
| `.plain` | No special styling at all — looks like normal content. |

> 📖 **New word: Prominent**
> Easy to notice. Use `.borderedProminent` for the **main** action on a screen (like "Save" or "Continue").

💡 **Tip:** Newer iOS versions may add more styles (for example glass-like styles). The ones above work everywhere.

### Size and shape

```swift
VStack(spacing: 16) {
    Button("Small") { }
        .buttonStyle(.borderedProminent)
        .controlSize(.small)

    Button("Large") { }
        .buttonStyle(.borderedProminent)
        .controlSize(.large)

    Button("Capsule") { }
        .buttonStyle(.borderedProminent)
        .buttonBorderShape(.capsule)

    Button("Green") { }
        .buttonStyle(.borderedProminent)
        .tint(.green)
}
```

| Modifier | Effect |
|---|---|
| `.controlSize(.small)` | Size: `.mini`, `.small`, `.regular`, `.large`, `.extraLarge`. |
| `.buttonBorderShape(.capsule)` | Shape: `.capsule`, `.roundedRectangle`, `.circle`… |
| `.tint(.green)` | Button color (instead of the accent color). |

### Full-width button

```swift
Button {
    print("Continue")
} label: {
    Text("Continue")
        .frame(maxWidth: .infinity)
}
.buttonStyle(.borderedProminent)
.controlSize(.large)
.padding(.horizontal)
```

| Part | Why |
|---|---|
| `.frame(maxWidth: .infinity)` on the **label** | Makes the label (and so the button) full width. (Chapter 44) |

---

## 5. Roles

```swift
VStack(spacing: 16) {
    Button("Delete account", role: .destructive) {
        print("Deleting...")
    }
    .buttonStyle(.borderedProminent)

    Button("Cancel", role: .cancel) {
        print("Cancelled")
    }
}
```

| Role | Meaning | Look |
|---|---|---|
| `.destructive` | Deletes or removes something important. | **Red** 🔴 |
| `.cancel` | Cancels / closes. | Often bold in alerts. |

> 📖 **New word: Role**
> Tells SwiftUI **what kind** of action the button does, so it can style it correctly — especially in alerts and menus (Chapter 51).

---

## 6. Disabling a button

```swift
let isFormComplete = false

Button("Submit") {
    print("Submitted")
}
.buttonStyle(.borderedProminent)
.disabled(!isFormComplete)
```

| Part | Meaning |
|---|---|
| `.disabled(true)` | The button turns **gray** and **can't be tapped**. |
| `!isFormComplete` | NOT complete → disabled (Chapter 10). |

In the next chapters, `isFormComplete` will change when the user types — and the button will enable automatically! ✨

---

## 7. Your own button style (bonus)

```swift
struct BouncyButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .padding(.horizontal, 24)
            .padding(.vertical, 12)
            .background(.purple, in: Capsule())
            .foregroundStyle(.white)
            .scaleEffect(configuration.isPressed ? 0.9 : 1.0)
    }
}

// Use it:
Button("Bouncy!") { }
    .buttonStyle(BouncyButtonStyle())
```

| Part | Meaning |
|---|---|
| `struct ...: ButtonStyle` | Follow the `ButtonStyle` protocol (Chapter 24). |
| `makeBody(configuration:)` | Describe how the button looks. |
| `configuration.label` | The button's label (the text or view you gave it). |
| `configuration.isPressed` | `true` while the finger is pressing. |
| `.scaleEffect(...)` | Shrink to 90% while pressed — feels bouncy! |

---

## 8. Tapping things that aren't buttons: `onTapGesture`

```swift
Text("Tap this text")
    .padding()
    .background(.yellow)
    .onTapGesture {
        print("Text tapped")
    }
```

| Modifier | Meaning |
|---|---|
| `.onTapGesture { }` | Run code when this view is tapped. |
| `.onTapGesture(count: 2) { }` | Double tap. |
| `.onLongPressGesture { }` | Press and hold. |

> 📖 **New word: Gesture**
> A touch action: tap, double tap, long press, swipe, drag, pinch.

🧠 **Remember:** Prefer `Button` for actions. Buttons work better with **VoiceOver**, keyboards, and show a "pressed" effect automatically. Use `onTapGesture` only when you really need it.

### Making a whole area tappable

```swift
HStack {
    Text("Settings")
    Spacer()
    Image(systemName: "chevron.right")
}
.padding()
.contentShape(Rectangle())     // the empty space is tappable too
.onTapGesture {
    print("Row tapped")
}
```

| Modifier | Meaning |
|---|---|
| `.contentShape(Rectangle())` | Make the **whole rectangle** tappable — including the empty space in the middle. Without it, only the text and icon react. |

---

## 9. Menus (a button with choices)

```swift
Menu("Options") {
    Button("Copy", systemImage: "doc.on.doc") { print("Copy") }
    Button("Share", systemImage: "square.and.arrow.up") { print("Share") }
    Divider()
    Button("Delete", systemImage: "trash", role: .destructive) { print("Delete") }
}
```

Tap "Options" → a small menu appears with three choices. 📋

---

## 10. Mini project: a button showcase 🎛️

```swift
struct ContentView: View {
    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                Text("Choose your action")
                    .font(.title.bold())

                Button {
                    print("Order placed 🍕")
                } label: {
                    Label("Order Pizza", systemImage: "cart.fill")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.large)

                HStack {
                    Button("Save draft") { print("Saved") }
                        .buttonStyle(.bordered)
                    Button("Share") { print("Share") }
                        .buttonStyle(.bordered)
                        .tint(.green)
                }

                Button("Remove from cart", role: .destructive) {
                    print("Removed")
                }

                HStack(spacing: 30) {
                    iconButton("heart.fill", color: .pink, label: "Like")
                    iconButton("bookmark.fill", color: .orange, label: "Save")
                    iconButton("paperplane.fill", color: .blue, label: "Send")
                }

                Menu {
                    Button("Small") { print("Small") }
                    Button("Medium") { print("Medium") }
                    Button("Large") { print("Large") }
                } label: {
                    Label("Choose size", systemImage: "chevron.down.circle")
                }
            }
            .padding()
        }
    }

    func iconButton(_ icon: String, color: Color, label: String) -> some View {
        Button {
            print("\(label) tapped")
        } label: {
            Image(systemName: icon)
                .font(.title)
                .foregroundStyle(color)
                .frame(width: 60, height: 60)
                .background(color.opacity(0.15), in: Circle())
        }
        .accessibilityLabel(label)
    }
}
```

| New thing | Meaning |
|---|---|
| `func iconButton(...) -> some View` | A **function that returns a view** — a quick way to reuse a design without making a new struct. |
| `color: Color` | `Color` is a type — you can pass it as a parameter. |

---

## 🏋️ Practice

1. Make a button "Hello" that prints your name.
2. Make a button with a label made of a `VStack`: a big icon on top and text below.
3. Make 3 buttons with `.bordered`, `.borderedProminent` and `.borderless`. Compare them.
4. Make a full-width, large, green `.borderedProminent` button.
5. Make a red destructive "Delete" button that is **disabled**.
6. Make a `Menu` with 3 colors to choose from.

---

## 🧠 Remember

- `Button("Title") { action }` — the action is a trailing closure.
- Full form: `Button { action } label: { any view }`.
- Styles: `.bordered`, `.borderedProminent` ⭐, `.borderless`, `.plain`.
- `.controlSize()`, `.tint()`, `.buttonBorderShape()` change size, color, shape.
- `role: .destructive` → red. `.disabled(true)` → gray, can't tap.
- Prefer `Button` over `onTapGesture`. Add `.accessibilityLabel` to icon-only buttons.
- Buttons can't change the screen yet — next chapter: `@State`! 🔜

---

⬅️ **Back:** [Chapter 44 — Spacing, Padding and Frames](44-padding-frames.md)
➡️ **Next:** [Chapter 46 — `@State`: Making Screens Change](46-state.md)
