# Chapter 52 — `@Binding`: Sharing State With Child Views

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- The problem: a child view needs to **change** the parent's state.
- `@Binding` — a two-way link to someone else's state.
- Passing `$value` from parent to child.
- Making your own reusable controls.
- Previews with bindings (`.constant` and `@Previewable`).
- The rule: **one source of truth**.

---

## 1. The problem

The parent has a `@State`. A **child view** wants to change it.

```swift
struct ContentView: View {
    @State private var isOn = false

    var body: some View {
        VStack {
            Text(isOn ? "💡 Light is ON" : "🌑 Light is OFF")
            LightSwitch(isOn: isOn)     // child view
        }
    }
}

struct LightSwitch: View {
    var isOn: Bool

    var body: some View {
        Button("Flip") {
            isOn.toggle()     // ❌ ERROR: cannot use mutating member on immutable value
        }
    }
}
```

Why doesn't it work?

- `LightSwitch` gets a **copy** of `isOn` (Bool is a value type — Chapter 22).
- A plain `var` in a view can't change (Chapter 46).
- Even if it could, it would only change the **copy** — the parent wouldn't know.

What if we used `@State` in the child?

```swift
struct LightSwitch: View {
    @State var isOn: Bool    // ❌ wrong idea
    ...
}
```

Now the child has **its own separate** light. The parent's text never changes. Two lights, not one! 💡💡

We need the child to **reach back** and change the **parent's** value.

---

## 2. `@Binding` to the rescue

```swift
struct ContentView: View {
    @State private var isOn = false

    var body: some View {
        VStack(spacing: 20) {
            Text(isOn ? "💡 Light is ON" : "🌑 Light is OFF")
                .font(.title)
            LightSwitch(isOn: $isOn)
        }
    }
}

struct LightSwitch: View {
    @Binding var isOn: Bool

    var body: some View {
        Button(isOn ? "Turn off" : "Turn on") {
            isOn.toggle()
        }
        .buttonStyle(.borderedProminent)
        .tint(isOn ? .yellow : .gray)
    }
}

#Preview {
    ContentView()
}
```

**Try it:** Tap the button. The parent's text changes! ✨

| Part | Meaning |
|---|---|
| `@State private var isOn` (parent) | The parent **owns** the data. |
| `LightSwitch(isOn: $isOn)` | Pass a **binding** with `$`. "Here's a link to my value." |
| `@Binding var isOn: Bool` (child) | "I don't own this. I have a **link** to someone else's value." |
| `isOn.toggle()` (child) | Changes the **parent's** value through the link. |

> 📖 **New word: `@Binding`**
> A property wrapper for a value that **someone else owns**. The view can read **and** change it.

```
     ContentView                      LightSwitch
  ┌──────────────────┐            ┌──────────────────┐
  │ @State isOn  ◄───┼── $isOn ───┼─► @Binding isOn  │
  │ (owns the data)  │  (link)    │ (borrows it)     │
  └──────────────────┘            └──────────────────┘
```

Remember the **TV remote** from Chapter 47? `@Binding` **is** a remote. 📺

🧠 **Remember:**
- `@State` = I **own** this data.
- `@Binding` = I **borrow** someone else's data, and I can change it.
- Pass with `$`: `ChildView(value: $myState)`.

---

## 3. You've used bindings already!

```swift
TextField("Name", text: $name)
Toggle("Wi-Fi", isOn: $wifi)
Slider(value: $volume)
```

Apple's controls have `@Binding` properties inside! Now **you** can build controls the same way.

---

## 4. `@State` vs `@Binding` vs `let`

| You write | The view… | Use when |
|---|---|---|
| `let title: String` | **reads** a value. Can't change it. | Just displaying data. |
| `@State private var count = 0` | **owns** and changes the value. | Data that belongs to this view. |
| `@Binding var count: Int` | **borrows** and changes the parent's value. | A child that needs to change parent data. |

🧠 **Remember:** If the child only **reads**, use `let`. Only use `@Binding` when the child must **change** it.

---

## 5. Making a reusable control: a star rating ⭐

```swift
struct StarRating: View {
    @Binding var rating: Int
    var maxRating = 5

    var body: some View {
        HStack {
            ForEach(1...maxRating, id: \.self) { number in
                Image(systemName: number <= rating ? "star.fill" : "star")
                    .foregroundStyle(.yellow)
                    .font(.title)
                    .onTapGesture {
                        rating = number
                    }
            }
        }
    }
}

struct ContentView: View {
    @State private var foodRating = 3
    @State private var serviceRating = 4

    var body: some View {
        Form {
            Section("Food 🍕") {
                StarRating(rating: $foodRating)
            }
            Section("Service 🙋") {
                StarRating(rating: $serviceRating)
            }
            Section {
                Text("Average: \(Double(foodRating + serviceRating) / 2, specifier: "%.1f") ⭐")
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `@Binding var rating: Int` | The rating belongs to the parent. |
| `var maxRating = 5` | A normal property with a default value. |
| `number <= rating ? "star.fill" : "star"` | Filled stars up to the rating. |
| `rating = number` | Tapping star 4 sets the **parent's** rating to 4. |
| Used twice | The **same** control works for two different ratings! ♻️ |

---

## 6. A custom stepper

```swift
struct QuantityPicker: View {
    let label: String
    @Binding var quantity: Int

    var body: some View {
        HStack {
            Text(label)
            Spacer()
            Button {
                if quantity > 0 { quantity -= 1 }
            } label: {
                Image(systemName: "minus.circle.fill")
            }
            Text("\(quantity)")
                .frame(width: 30)
                .monospacedDigit()
            Button {
                quantity += 1
            } label: {
                Image(systemName: "plus.circle.fill")
            }
        }
        .font(.title2)
        .buttonStyle(.borderless)
    }
}

struct ContentView: View {
    @State private var samosas = 2
    @State private var teas = 1

    var total: Int { samosas * 15 + teas * 10 }

    var body: some View {
        List {
            QuantityPicker(label: "🥟 Samosa (₹15)", quantity: $samosas)
            QuantityPicker(label: "☕ Tea (₹10)", quantity: $teas)
            Text("Total: ₹\(total)")
                .font(.headline)
        }
    }
}
```

| New thing | Meaning |
|---|---|
| `.monospacedDigit()` | All numbers have the same width, so the layout doesn't jump when 9 → 10. |

---

## 7. Bindings to parts of a struct

You can pass a binding to **one property** of a struct:

```swift
struct Profile {
    var name: String
    var bio: String
    var isPublic: Bool
}

struct ContentView: View {
    @State private var profile = Profile(name: "Meena", bio: "I love Swift!", isPublic: true)

    var body: some View {
        Form {
            NameField(name: $profile.name)
            TextField("Bio", text: $profile.bio)
            Toggle("Public profile", isOn: $profile.isPublic)

            Section("Preview") {
                Text("\(profile.name) — \(profile.bio)")
                Text(profile.isPublic ? "🌍 Public" : "🔒 Private")
            }
        }
    }
}

struct NameField: View {
    @Binding var name: String

    var body: some View {
        TextField("Name", text: $name)
            .font(.headline)
    }
}
```

| Part | Meaning |
|---|---|
| `$profile.name` | A binding to **just** the `name` property. |
| `$name` inside `NameField` | A binding can be passed on again with `$`! |

---

## 8. Previews with bindings

A view with `@Binding` needs a binding in the preview. Two ways:

### Way 1: `.constant(...)` — a fake, frozen binding

```swift
#Preview {
    StarRating(rating: .constant(3))
}
```

| Part | Meaning |
|---|---|
| `.constant(3)` | A binding that is **always** 3. Tapping won't change it. Good for checking the **look**. |

### Way 2: `@Previewable @State` — a real, working binding

```swift
#Preview {
    @Previewable @State var rating = 3
    StarRating(rating: $rating)
}
```

| Part | Meaning |
|---|---|
| `@Previewable @State var rating = 3` | Real state, **only** for the preview. Tapping works in Live mode! |

(`@Previewable` needs a recent Xcode. If it doesn't work in yours, use `.constant` or a small wrapper view.)

---

## 9. One source of truth 🎯

This is a key idea in SwiftUI:

> **Every piece of data should live in exactly ONE place.**

> 📖 **New word: Source of truth**
> The **one** place where a piece of data is stored. Everyone else reads it or gets a binding to it.

❌ **Bad:** two copies that can disagree

```
  Parent: @State isOn = true
  Child:  @State isOn = false     ← two truths! 😵
```

✅ **Good:** one owner, others borrow

```
  Parent: @State isOn = true      ← the ONE source of truth
  Child:  @Binding isOn           ← borrows it
```

### Where should the `@State` live?

Put it in the **closest common parent** of all the views that need it.

```
            ContentView  ← @State favorites (both children need it)
            /         \
   ExploreView      FavoritesView
   (@Binding,        (let, only reads)
    changes it)
```

This is exactly what we did in the Chapter 50 tabs project! 🎉

---

## 10. Mini project: a settings screen with reusable rows ⚙️

```swift
struct SettingToggleRow: View {
    let icon: String
    let color: Color
    let title: String
    @Binding var isOn: Bool

    var body: some View {
        Toggle(isOn: $isOn) {
            HStack(spacing: 12) {
                Image(systemName: icon)
                    .foregroundStyle(.white)
                    .frame(width: 30, height: 30)
                    .background(color, in: RoundedRectangle(cornerRadius: 7))
                Text(title)
            }
        }
    }
}

struct Settings {
    var wifi = true
    var bluetooth = false
    var airplane = false
    var notifications = true
}

struct ContentView: View {
    @State private var settings = Settings()

    var enabledCount: Int {
        [settings.wifi, settings.bluetooth, settings.airplane, settings.notifications]
            .filter { $0 }
            .count
    }

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    SettingToggleRow(icon: "airplane", color: .orange,
                                     title: "Airplane Mode", isOn: $settings.airplane)
                    SettingToggleRow(icon: "wifi", color: .blue,
                                     title: "Wi-Fi", isOn: $settings.wifi)
                    SettingToggleRow(icon: "dot.radiowaves.left.and.right", color: .blue,
                                     title: "Bluetooth", isOn: $settings.bluetooth)
                }
                Section {
                    SettingToggleRow(icon: "bell.badge.fill", color: .red,
                                     title: "Notifications", isOn: $settings.notifications)
                }
                Section {
                    Text("\(enabledCount) of 4 settings are on")
                        .foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Settings")
            .onChange(of: settings.airplane) { _, isAirplane in
                if isAirplane {
                    settings.wifi = false
                    settings.bluetooth = false
                }
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `SettingToggleRow` | A reusable row: icon in a colored box + title + toggle. |
| `@State private var settings` | **One** source of truth for all settings. |
| `$settings.wifi` | A binding to one property. |
| `.onChange(of: settings.airplane)` | Turning on Airplane Mode turns off Wi-Fi and Bluetooth — and the rows update automatically! ✈️ |
| `{ _, isAirplane in ... }` | `_` = we don't need the old value (Chapter 12). |

---

## 🏋️ Practice

1. Make a `ColorToggle` child view with `@Binding var isRed: Bool`. The parent shows a circle that is red or blue.
2. Make a `LikeButton` with `@Binding var isLiked: Bool` and use it in a parent that shows "You liked this ❤️".
3. Make a reusable `LabeledSlider` with `label: String` and `@Binding var value: Double`. Use it 3 times.
4. Make a `struct Pizza { var size: String; var extraCheese: Bool }` in `@State`. Pass `$pizza.extraCheese` to a child view with a toggle.
5. Write two previews for your `StarRating`: one with `.constant`, one with `@Previewable @State`.

---

## 🧠 Remember

- `@State` = **owns** data. `@Binding` = **borrows** data and can change it.
- Parent passes a binding with `$`: `Child(value: $state)`.
- Child declares `@Binding var value: Type`.
- If the child only reads, use `let`, not `@Binding`.
- `$struct.property` → binding to one property.
- Previews: `.constant(x)` or `@Previewable @State`.
- **One source of truth**: store data in one place, in the closest common parent.

---

⬅️ **Back:** [Chapter 51 — Sheets and Alerts](51-sheets-alerts.md)
➡️ **Next:** [Chapter 53 — `@Observable`](53-observable.md)
