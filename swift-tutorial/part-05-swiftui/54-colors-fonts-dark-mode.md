# Chapter 54 — Colors, Fonts and Dark Mode

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- Built-in colors and **semantic** colors (that adapt to dark mode).
- Making your own colors (code and Assets).
- Opacity, gradients and materials (blur).
- Dark mode: testing, adapting, reading the color scheme.
- Fonts: system fonts, Dynamic Type, custom fonts.
- Making a simple **theme** for your app.

---

## 1. Built-in colors

```swift
HStack {
    ForEach([Color.red, .orange, .yellow, .green, .mint, .teal,
             .cyan, .blue, .indigo, .purple, .pink, .brown], id: \.self) { color in
        Circle()
            .fill(color)
            .frame(width: 24, height: 24)
    }
}
```

| Colors | |
|---|---|
| Rainbow | `.red`, `.orange`, `.yellow`, `.green`, `.mint`, `.teal`, `.cyan`, `.blue`, `.indigo`, `.purple`, `.pink`, `.brown` |
| Neutral | `.black`, `.white`, `.gray` |
| Special | `.clear` (invisible), `.accentColor` (your app's color — Chapter 37) |

💡 **Tip:** Apple's built-in colors change **slightly** in dark mode, so they always look good. 🌗

---

## 2. Semantic colors ⭐ (they adapt automatically)

> 📖 **New word: Semantic color**
> A color named by its **purpose** ("main text", "background"), not by how it looks. It changes automatically for light and dark mode.

```swift
VStack(alignment: .leading, spacing: 8) {
    Text("Primary text").foregroundStyle(.primary)
    Text("Secondary text").foregroundStyle(.secondary)
    Text("Tertiary text").foregroundStyle(.tertiary)
    Text("Quaternary text").foregroundStyle(.quaternary)
}
```

| Style | Light mode | Dark mode | Use for |
|---|---|---|---|
| `.primary` | black | white | Main text |
| `.secondary` | gray | light gray | Less important text |
| `.tertiary` | lighter gray | darker gray | Hints |
| `.quaternary` | very light | very dark | Very subtle things |

### System background colors

```swift
Color(.systemBackground)           // white in light, black in dark
Color(.secondarySystemBackground)  // light gray / dark gray — good for cards
Color(.systemGroupedBackground)    // the gray behind grouped lists
Color(.label)                      // the main text color
Color(.separator)                  // the color of thin lines
```

These come from **UIKit** (Apple's older UI framework) — that's why they use `Color(.name)`.

🧠 **Remember:** Use **semantic colors** for text and backgrounds. Then dark mode works **for free**.

❌ Bad: `.foregroundStyle(.black)` → black text on a black background in dark mode = invisible! 😱
✅ Good: `.foregroundStyle(.primary)`

---

## 3. Your own colors in code

```swift
Color(red: 1.0, green: 0.4, blue: 0.0)     // orange — values from 0.0 to 1.0
Color(red: 255/255, green: 107/255, blue: 0/255)  // same, from 0–255 values
Color(hue: 0.6, saturation: 0.8, brightness: 0.9) // a blue
Color.blue.opacity(0.5)                    // 50% see-through blue
```

| Part | Meaning |
|---|---|
| `red:green:blue:` | Mix red, green and blue light. 0 = none, 1 = full. |
| `hue:saturation:brightness:` | Hue = which color (0–1 around the rainbow), saturation = how strong, brightness = how light. |
| `.opacity(0.5)` | How see-through: 0 = invisible, 1 = solid. |

> 📖 **New word: RGB**
> **R**ed, **G**reen, **B**lue. Screens make every color by mixing these three lights.

### A hex color helper (handy extension!)

Designers often give colors as **hex codes** like `#FF6B00`. Let's add support with an **extension** (Chapter 25):

```swift
extension Color {
    init(hex: UInt) {
        self.init(
            red: Double((hex >> 16) & 0xFF) / 255,
            green: Double((hex >> 8) & 0xFF) / 255,
            blue: Double(hex & 0xFF) / 255
        )
    }
}

// Use it:
Color(hex: 0xFF6B00)   // orange
Color(hex: 0x1E90FF)   // dodger blue
```

| Part | Meaning |
|---|---|
| `0xFF6B00` | A number written in **hex** (base 16). `FF` = red 255, `6B` = green 107, `00` = blue 0. |
| `>> 16`, `& 0xFF` | Bit tricks to pick out each pair of digits. You don't need to understand them now — just use the helper! |

> 📖 **New word: Hex code**
> A color written as 6 characters (0–9, A–F), like `#FF6B00`. Two characters each for red, green, blue.

---

## 4. Colors from Assets (best for brand colors) ⭐

Chapter 37 showed how to add a **Color Set** in Assets. The big advantage: you can set a **different color for dark mode**.

1. **Assets** → **+** → **Color Set**. Name it `BrandPrimary`.
2. In the Attributes inspector, set **Appearances** → **Any, Dark**.
3. Choose a color for **Any** (light mode) and a different one for **Dark**.

```swift
Text("Hello")
    .foregroundStyle(Color("BrandPrimary"))

// Newer Xcode also generates names you can use directly:
// .foregroundStyle(.brandPrimary)
```

🧠 **Remember:** Put **brand colors** in Assets with light **and** dark versions.

---

## 5. Gradients 🌈

```swift
VStack(spacing: 20) {
    RoundedRectangle(cornerRadius: 16)
        .fill(LinearGradient(colors: [.purple, .blue],
                             startPoint: .topLeading,
                             endPoint: .bottomTrailing))
        .frame(height: 100)

    Circle()
        .fill(RadialGradient(colors: [.yellow, .orange, .red],
                             center: .center,
                             startRadius: 5,
                             endRadius: 80))
        .frame(width: 160, height: 160)

    Circle()
        .fill(AngularGradient(colors: [.red, .yellow, .green, .blue, .purple, .red],
                              center: .center))
        .frame(width: 120, height: 120)

    RoundedRectangle(cornerRadius: 16)
        .fill(.green.gradient)
        .frame(height: 60)
}
.padding()
```

| Gradient | Looks like |
|---|---|
| `LinearGradient` | Colors change in a **straight line**. |
| `RadialGradient` | Colors spread from the **center outward**, like a sun ☀️. |
| `AngularGradient` | Colors go **around** a circle, like a color wheel 🎨. |
| `.green.gradient` | A soft, simple gradient from one color. Very easy! |

---

## 6. Materials (frosted glass) 🧊

**Materials** are see-through backgrounds that **blur** what's behind them.

```swift
ZStack {
    Image(systemName: "photo.artframe")
        .resizable()
        .scaledToFill()
        .foregroundStyle(.orange.gradient)
        .ignoresSafeArea()

    VStack {
        Text("Frosted glass")
            .font(.title.bold())
        Text("The background is blurred")
    }
    .padding(30)
    .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 20))
}
```

| Material | Blur |
|---|---|
| `.ultraThinMaterial` | Very see-through |
| `.thinMaterial` | |
| `.regularMaterial` | Medium |
| `.thickMaterial` | |
| `.ultraThickMaterial` | Almost solid |

Materials adapt to light and dark mode automatically. 💎

💡 **Tip:** Newer iOS versions also have a **glass effect** (`.glassEffect()`) for a "liquid glass" look. If your minimum iOS supports it, try it! Materials work on all recent versions.

---

## 7. Dark mode 🌙

### Testing dark mode

| Where | How |
|---|---|
| **Canvas** | Add a second preview with `.preferredColorScheme(.dark)`, or use the **Variants** button → Color Scheme Variants. |
| **Simulator** | `Cmd + Shift + A` (Chapter 34). |
| **Real iPhone** | Settings → Display & Brightness → Dark. |

```swift
#Preview("Light") {
    ContentView()
}

#Preview("Dark") {
    ContentView()
        .preferredColorScheme(.dark)
}
```

### Reading the current color scheme

```swift
struct ContentView: View {
    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        VStack {
            Image(systemName: colorScheme == .dark ? "moon.stars.fill" : "sun.max.fill")
                .font(.system(size: 80))
                .foregroundStyle(colorScheme == .dark ? .indigo : .orange)
            Text(colorScheme == .dark ? "Good night 🌙" : "Good day ☀️")
                .font(.title)
        }
    }
}
```

| Part | Meaning |
|---|---|
| `@Environment(\.colorScheme)` | Read whether the phone is in `.light` or `.dark` mode. |

💡 **Tip:** You rarely need this! Semantic colors and Asset colors handle dark mode automatically. Use `colorScheme` only for special cases (like a different image).

### Letting the user choose (inside your app)

```swift
enum AppTheme: String, CaseIterable, Identifiable {
    case system, light, dark
    var id: Self { self }

    var colorScheme: ColorScheme? {
        switch self {
        case .system: nil
        case .light: .light
        case .dark: .dark
        }
    }
}

struct ContentView: View {
    @State private var theme: AppTheme = .system

    var body: some View {
        Form {
            Picker("Theme", selection: $theme) {
                ForEach(AppTheme.allCases) { t in
                    Text(t.rawValue.capitalized)
                }
            }
            .pickerStyle(.segmented)
            Text("This text follows the theme.")
        }
        .preferredColorScheme(theme.colorScheme)
    }
}
```

| Part | Meaning |
|---|---|
| `.preferredColorScheme(nil)` | Follow the phone's setting. |
| `.preferredColorScheme(.dark)` | Force dark mode for this app. |

(In Chapter 56 you'll learn to **save** the user's choice with `@AppStorage`.)

---

## 8. Fonts in depth 🔤

### System fonts (recap from Chapter 42)

```swift
.font(.title)                                   // text style — supports Dynamic Type ✅
.font(.title.weight(.semibold))                 // style + weight
.font(.system(.body, design: .rounded))         // style + design
.font(.system(size: 40, weight: .bold))         // fixed size ⚠️
```

### Dynamic Type — test it!

```swift
#Preview("Huge text") {
    ContentView()
        .dynamicTypeSize(.accessibility3)
}
```

Sizes go from `.xSmall` up to `.accessibility5` (very big). Make sure your layout still works!

💡 **Tip:** If a layout breaks with big text, a `ViewThatFits` or switching from `HStack` to `VStack` can help:

```swift
ViewThatFits {
    HStack { Text("Name"); Spacer(); Text("Meena Sharma") }   // try this first
    VStack(alignment: .leading) { Text("Name"); Text("Meena Sharma") }  // if it doesn't fit
}
```

### Scaling a fixed size with Dynamic Type

```swift
@ScaledMetric private var iconSize = 40.0

Image(systemName: "star.fill")
    .font(.system(size: iconSize))
```

`@ScaledMetric` makes a number **grow** with the user's text size. ♿

### Custom fonts

1. Get a font file (`.ttf` or `.otf`) — for example from Google Fonts (check its license).
2. **Drag** it into your Xcode project. ✅ Check your app **target** in the dialog.
3. In **Target → Info**, add the key **Fonts provided by application** (`UIAppFonts`), and add an item with the **file name**, e.g. `Poppins-Bold.ttf`.
4. Use it:

```swift
Text("Custom font!")
    .font(.custom("Poppins-Bold", size: 28, relativeTo: .title))
```

| Part | Meaning |
|---|---|
| `"Poppins-Bold"` | The font's **PostScript name** (often the file name without `.ttf`). |
| `relativeTo: .title` | Grow and shrink with Dynamic Type, like the `.title` style. ✅ |

⚠️ **Careful:** If the custom font doesn't appear, the name is probably wrong. Open the font file on your Mac (Font Book app) to see its real PostScript name.

---

## 9. A simple theme 🎨

Keep your app's colors and fonts in **one** place:

```swift
enum Theme {
    static let primary = Color(hex: 0x6C5CE7)
    static let accent = Color(hex: 0xFD79A8)
    static let card = Color(.secondarySystemBackground)

    static let titleFont = Font.system(.title, design: .rounded, weight: .bold)
    static let bodyFont = Font.system(.body, design: .rounded)

    static let cornerRadius: CGFloat = 16
    static let padding: CGFloat = 16
}

struct ThemedCard: View {
    let title: String
    let text: String

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(Theme.titleFont)
                .foregroundStyle(Theme.primary)
            Text(text)
                .font(Theme.bodyFont)
                .foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(Theme.padding)
        .background(Theme.card, in: RoundedRectangle(cornerRadius: Theme.cornerRadius))
    }
}
```

| Part | Meaning |
|---|---|
| `enum Theme` with `static let` | A namespace for constants (Chapter 20: `static`). An enum with no cases can't be created by mistake. |
| `CGFloat` | The number type SwiftUI uses for sizes. Like `Double`. |
| `Theme.primary` | Use the same color everywhere. Change it **once** → the whole app changes! |

---

## 10. Mini project: a light/dark-friendly profile card 🪪

```swift
struct ContentView: View {
    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        ZStack {
            Color(.systemGroupedBackground)
                .ignoresSafeArea()

            VStack(spacing: 16) {
                Circle()
                    .fill(LinearGradient(colors: [.pink, .orange],
                                         startPoint: .topLeading,
                                         endPoint: .bottomTrailing))
                    .frame(width: 110, height: 110)
                    .overlay(
                        Text("MS")
                            .font(.system(.largeTitle, design: .rounded, weight: .bold))
                            .foregroundStyle(.white)
                    )
                    .shadow(color: .pink.opacity(colorScheme == .dark ? 0.6 : 0.3), radius: 12)

                Text("Meena Sharma")
                    .font(.title.bold())
                    .foregroundStyle(.primary)

                Text("SwiftUI learner • Bengaluru")
                    .foregroundStyle(.secondary)

                HStack(spacing: 30) {
                    stat("128", "Posts")
                    stat("4.2K", "Followers")
                    stat("310", "Following")
                }
                .padding()
                .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 16))
            }
            .padding(24)
            .background(Color(.secondarySystemGroupedBackground),
                        in: RoundedRectangle(cornerRadius: 28))
            .padding()
        }
    }

    func stat(_ number: String, _ label: String) -> some View {
        VStack {
            Text(number).font(.headline)
            Text(label).font(.caption).foregroundStyle(.secondary)
        }
    }
}

#Preview("Light") { ContentView() }
#Preview("Dark") { ContentView().preferredColorScheme(.dark) }
```

Check **both** previews. Everything looks good in light **and** dark — because we used semantic colors and materials. 🌗

---

## 🏋️ Practice

1. Make a screen with `.primary`, `.secondary` and `.tertiary` texts on `Color(.systemBackground)`. Check it in light and dark previews.
2. Add the `Color(hex:)` extension and make 3 circles with hex colors.
3. Add a Color Set in Assets with a different light and dark color. Use it as a background.
4. Make a card with a `LinearGradient` background and white text.
5. Put text on `.ultraThinMaterial` over a colorful background.
6. Add a theme picker (System / Light / Dark) using `.preferredColorScheme`.
7. Test your screen with `.dynamicTypeSize(.accessibility3)`. Fix anything that breaks.

---

## 🧠 Remember

- Use **semantic colors** (`.primary`, `.secondary`, `Color(.systemBackground)`) → dark mode works automatically.
- Brand colors → **Assets Color Set** with light and dark versions.
- `Color(red:green:blue:)`, `.opacity()`, gradients, and `.gradient`.
- Materials (`.ultraThinMaterial`…) = frosted glass.
- Test dark mode with `.preferredColorScheme(.dark)` and `Cmd + Shift + A`.
- Use **text styles** for fonts; `@ScaledMetric` and `relativeTo:` for Dynamic Type.
- Keep colors and fonts in one `Theme`.

---

⬅️ **Back:** [Chapter 53 — `@Observable`](53-observable.md)
➡️ **Next:** [Chapter 55 — Animations](55-animations.md)
