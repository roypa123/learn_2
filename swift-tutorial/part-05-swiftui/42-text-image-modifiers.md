# Chapter 42 — `Text`, `Image` and Modifiers

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- Styling `Text`: fonts, weight, color, alignment, line limits.
- **Dynamic Type** (text that grows with the user's settings).
- **SF Symbols**: thousands of free icons.
- Showing images from your **Assets**.
- Making images resize correctly.
- `Label`: icon + text together.

---

## 1. Text basics

```swift
Text("Hello, world!")
```

That's all! SwiftUI chooses a good default font and color.

### Showing values

```swift
let name = "Meena"
let score = 42

Text("Player: \(name), Score: \(score)")
```

String interpolation (Chapter 9) works inside `Text`! ✨

---

## 2. Fonts

```swift
VStack(alignment: .leading) {
    Text("Large Title").font(.largeTitle)
    Text("Title").font(.title)
    Text("Title 2").font(.title2)
    Text("Title 3").font(.title3)
    Text("Headline").font(.headline)
    Text("Subheadline").font(.subheadline)
    Text("Body (default)").font(.body)
    Text("Callout").font(.callout)
    Text("Footnote").font(.footnote)
    Text("Caption").font(.caption)
    Text("Caption 2").font(.caption2)
}
```

**Preview:** each line gets smaller, from big Large Title to tiny Caption 2.

| Font style | Use for |
|---|---|
| `.largeTitle` | The main title of a screen. |
| `.title`, `.title2`, `.title3` | Section titles. |
| `.headline` | Important short text (bold). |
| `.body` | Normal text. The default. |
| `.subheadline`, `.callout` | A bit smaller than body. |
| `.footnote`, `.caption` | Small notes, dates, hints. |

> 📖 **New word: Text style**
> A named font size like `.title` or `.body`. It **automatically grows** if the user chooses bigger text in Settings. This is called **Dynamic Type**.

> 📖 **New word: Dynamic Type**
> An iPhone feature: users can make **all** text bigger or smaller in Settings. Text styles follow it automatically. ♿

🧠 **Remember:** Use **text styles** (`.title`, `.body`…) instead of fixed sizes. Your app will be easier to read for everyone, including people with poor eyesight.

### Fixed size (use carefully)

```swift
Text("Exactly 30 points").font(.system(size: 30))
```

⚠️ **Careful:** Fixed sizes **don't** grow with Dynamic Type. Use them only for special cases (like a big emoji or a number on a clock).

---

## 3. Weight, design, and more

```swift
VStack(alignment: .leading, spacing: 8) {
    Text("Bold").bold()
    Text("Italic").italic()
    Text("Heavy").fontWeight(.heavy)
    Text("Light").fontWeight(.light)
    Text("Rounded").fontDesign(.rounded)
    Text("Monospaced 123").fontDesign(.monospaced)
    Text("Serif").fontDesign(.serif)
    Text("Underline").underline()
    Text("Strikethrough").strikethrough()
    Text("Wide letters").kerning(3)
}
```

| Modifier | Effect |
|---|---|
| `.bold()` | **Bold** |
| `.italic()` | *Italic* |
| `.fontWeight(.heavy)` | How thick: `.ultraLight`, `.thin`, `.light`, `.regular`, `.medium`, `.semibold`, `.bold`, `.heavy`, `.black` |
| `.fontDesign(.rounded)` | Font family style: `.default`, `.rounded`, `.monospaced`, `.serif` |
| `.underline()` | Line under the text. |
| `.strikethrough()` | Line through the text. |
| `.kerning(3)` | Space between letters. |

You can combine them:

```swift
Text("Score: 100")
    .font(.title)
    .fontWeight(.bold)
    .fontDesign(.rounded)
```

Or in one modifier:

```swift
Text("Score: 100")
    .font(.system(.title, design: .rounded, weight: .bold))
```

---

## 4. Colors

```swift
VStack {
    Text("Blue").foregroundStyle(.blue)
    Text("Red").foregroundStyle(.red)
    Text("Gray (secondary)").foregroundStyle(.secondary)
    Text("Gradient!")
        .font(.largeTitle.bold())
        .foregroundStyle(
            LinearGradient(colors: [.purple, .pink, .orange],
                           startPoint: .leading,
                           endPoint: .trailing)
        )
}
```

| Part | Meaning |
|---|---|
| `.foregroundStyle(.blue)` | Text color. |
| `.secondary` | A softer gray that works in light **and** dark mode. |
| `LinearGradient(...)` | Colors that smoothly change from one to another. |
| `startPoint: .leading` | Start at the left… |
| `endPoint: .trailing` | …end at the right. |

> 📖 **New word: leading / trailing**
> **Leading** = the side where reading **starts** (left in English). **Trailing** = where it **ends** (right in English). In right-to-left languages like Arabic, they flip automatically! 🌍

More about colors in Chapter 54.

---

## 5. Long text: alignment and lines

```swift
Text("SwiftUI makes it easy to build beautiful apps for every Apple device. Let's learn it step by step!")
    .multilineTextAlignment(.center)
    .lineLimit(2)
    .padding()
```

| Modifier | Meaning |
|---|---|
| `.multilineTextAlignment(.center)` | When text has many lines, center each line. Also `.leading`, `.trailing`. |
| `.lineLimit(2)` | Show **at most 2** lines. Extra text ends with `…` |

More options:

```swift
Text("A very long title that might not fit")
    .lineLimit(1)
    .truncationMode(.middle)       // "A very lo…not fit"

Text("Shrink me if needed to fit in one line")
    .lineLimit(1)
    .minimumScaleFactor(0.5)       // can shrink to 50% size
```

| Modifier | Meaning |
|---|---|
| `.truncationMode(.middle)` | Put the `…` in the middle. Also `.head`, `.tail` (default). |
| `.minimumScaleFactor(0.5)` | If it doesn't fit, make the font smaller — down to half size. |

---

## 6. Styling parts of a text

You can join `Text` views with `+`:

```swift
Text("Hello, ")
    + Text("Ravi").bold().foregroundStyle(.blue)
    + Text("! 👋")
```

**Preview:** Hello, **Ravi**! 👋 (with "Ravi" in blue bold)

⚠️ **Careful:** In the newest Xcode versions, joining `Text` with `+` may show a yellow **deprecation warning**. The newer way is to put a styled `Text` **inside** another `Text` with `\( )`:

```swift
Text("Hello, \(Text("Ravi").bold().foregroundStyle(.blue))! 👋")
```

Both give the same result. If you see the warning, use this form.

> 📖 **New word: Deprecated**
> Still works, but Apple recommends a newer way. It may be removed in the future.

### Markdown in Text

```swift
Text("This is **bold**, this is *italic*, and this is a [link](https://apple.com).")
```

| You type | Shows as |
|---|---|
| `**bold**` | **bold** |
| `*italic*` | *italic* |
| `[link](url)` | a tappable link |

> 📖 **New word: Markdown**
> A simple way to style text with symbols like `**` and `*`. (This tutorial is written in Markdown!)

### Dates and numbers

```swift
Text(Date.now, style: .date)       // e.g. "14 October 2026"
Text(Date.now, style: .time)       // e.g. "10:30 AM"
Text(0.75, format: .percent)       // "75%"
Text(1234.5, format: .currency(code: "INR"))   // "₹1,234.50"
```

SwiftUI formats them correctly for the user's country and language. 🌍

---

## 7. SF Symbols ⭐

Apple gives you **thousands** of free icons called **SF Symbols**.

```swift
Image(systemName: "heart.fill")
```

| Part | Meaning |
|---|---|
| `Image(systemName:)` | Show an SF Symbol. |
| `"heart.fill"` | The symbol's name. |

### Finding symbol names

- Download the free **SF Symbols** app from Apple's developer website (on the Mac). Search and copy names.
- Or in Xcode: Library (`Cmd + Shift + L`) → **Symbols** tab.

Some useful names:

| Name | Icon idea |
|---|---|
| `star`, `star.fill` | ☆ ★ |
| `heart`, `heart.fill` | ♡ ♥ |
| `house.fill` | 🏠 |
| `gearshape.fill` | ⚙️ |
| `person.circle` | 👤 |
| `magnifyingglass` | 🔍 |
| `plus`, `minus`, `xmark`, `checkmark` | + − × ✓ |
| `trash` | 🗑️ |
| `cart.fill` | 🛒 |
| `bell.fill` | 🔔 |
| `sun.max.fill`, `moon.fill`, `cloud.rain.fill` | ☀️ 🌙 🌧️ |

💡 **Tip:** `.fill` at the end usually means the **filled** version.

### Styling symbols

Symbols act like **text**, so text modifiers work:

```swift
HStack(spacing: 20) {
    Image(systemName: "star.fill")
        .font(.largeTitle)
        .foregroundStyle(.yellow)

    Image(systemName: "heart.fill")
        .font(.system(size: 50))
        .foregroundStyle(.red)

    Image(systemName: "cloud.sun.rain.fill")
        .font(.largeTitle)
        .symbolRenderingMode(.multicolor)

    Image(systemName: "wifi", variableValue: 0.5)
        .font(.largeTitle)
}
```

| Modifier | Meaning |
|---|---|
| `.font(.largeTitle)` | Symbol size follows the font. |
| `.foregroundStyle(.yellow)` | Color. |
| `.symbolRenderingMode(.multicolor)` | Use the symbol's **built-in** colors (cloud white, sun yellow, rain blue). |
| `variableValue: 0.5` | Some symbols can show "how full" — here Wi-Fi at half strength. |

---

## 8. Images from Assets

Add an image to **Assets** (Chapter 37), named for example `dog`.

```swift
Image("dog")
```

⚠️ By default, the image shows at its **original size** — often **huge**, going off screen!

### Making it the right size

```swift
Image("dog")
    .resizable()
    .scaledToFit()
    .frame(width: 200)
```

| Modifier | Meaning |
|---|---|
| `.resizable()` | "You're allowed to change my size." **Must come first!** |
| `.scaledToFit()` | Keep the shape. Fit **inside** the space. (Might leave empty space.) |
| `.frame(width: 200)` | Make it 200 points wide. |

### Fit vs Fill

```
 Original: a wide photo  ▭

 .scaledToFit()            .scaledToFill()
 ┌──────────┐              ┌──────────┐
 │          │              │██████████│
 │▭▭▭▭▭▭▭▭▭▭│              │██████████│  ← fills, parts are
 │          │              │██████████│    outside the box
 └──────────┘              └──────────┘
 whole image visible       box fully covered
```

| Modifier | Effect |
|---|---|
| `.scaledToFit()` | Whole image visible. May leave empty bars. |
| `.scaledToFill()` | Box fully covered. Parts of the image may be **outside**. Add `.clipped()` to cut them off. |

```swift
Image("dog")
    .resizable()
    .scaledToFill()
    .frame(width: 150, height: 150)
    .clipped()
```

### Round profile picture 👤

```swift
Image("dog")
    .resizable()
    .scaledToFill()
    .frame(width: 120, height: 120)
    .clipShape(Circle())
    .overlay(Circle().stroke(.white, lineWidth: 4))
    .shadow(radius: 8)
```

| Modifier | Effect |
|---|---|
| `.clipShape(Circle())` | Cut the image into a circle. |
| `.overlay(Circle().stroke(...))` | Draw a white circle line **on top**. |
| `.shadow(radius: 8)` | A soft shadow underneath. |

⚠️ **Careful:** If `.resizable()` is not the **first** modifier, you get an error, or the size won't change. Order matters (Chapter 41)!

---

## 9. Accessibility for images ♿

People who are blind use **VoiceOver** — the iPhone reads the screen aloud.

```swift
Image("dog")
    .resizable()
    .scaledToFit()
    .accessibilityLabel("A brown dog playing in the park")

Image(systemName: "sparkles")
    .accessibilityHidden(true)   // just decoration — skip it
```

| Modifier | Meaning |
|---|---|
| `.accessibilityLabel("...")` | What VoiceOver says for this image. |
| `.accessibilityHidden(true)` | Decorative only — VoiceOver ignores it. |

> 📖 **New word: Accessibility**
> Making apps usable by **everyone**, including people with disabilities. ♿

---

## 10. `Label` — icon + text

```swift
VStack(alignment: .leading, spacing: 12) {
    Label("Home", systemImage: "house.fill")
    Label("Settings", systemImage: "gearshape.fill")
    Label("Favorites", systemImage: "heart.fill")
        .foregroundStyle(.pink)
    Label("Messages", systemImage: "message.fill")
        .labelStyle(.iconOnly)
}
.font(.title2)
```

| Part | Meaning |
|---|---|
| `Label("Home", systemImage: "house.fill")` | Text + icon, nicely lined up. |
| `.labelStyle(.iconOnly)` | Show only the icon. Also `.titleOnly`, `.titleAndIcon`. |
| `.font(.title2)` on the `VStack` | Applies to **all** views inside! |

💡 **Tip:** Many modifiers (like `.font` and `.foregroundStyle`) set the style for **everything inside** a container. Child views can still override it.

---

## 11. Mini project: a profile card 🪪

```swift
struct ContentView: View {
    var body: some View {
        VStack(spacing: 12) {
            Image(systemName: "person.crop.circle.fill")
                .font(.system(size: 90))
                .foregroundStyle(.blue.gradient)

            Text("Meena Sharma")
                .font(.title.bold())

            Text("iOS Developer in training 👩‍💻")
                .font(.subheadline)
                .foregroundStyle(.secondary)

            Label("Bengaluru, India", systemImage: "mappin.and.ellipse")
                .font(.callout)

            Text("I love **SwiftUI**, *dosa*, and long walks.")
                .multilineTextAlignment(.center)
                .padding(.top, 4)
        }
        .padding()
    }
}

#Preview {
    ContentView()
}
```

| New thing | Meaning |
|---|---|
| `.blue.gradient` | A soft gradient made from one color. |
| `.font(.title.bold())` | Title style, bold. |
| `.padding(.top, 4)` | 4 points of space only on the **top** (more in Chapter 44). |

---

## 🏋️ Practice

1. Show 3 texts using `.largeTitle`, `.headline` and `.caption`. Make the caption gray (`.secondary`).
2. Write a long sentence. Limit it to 2 lines and center it.
3. Show 5 SF Symbols in a row with different colors and sizes.
4. Add a photo to Assets. Show it as a **round** 150×150 profile picture with a border.
5. Make a `Label` list: Home, Profile, Settings, with icons.
6. Use `+` to make "Total: ₹500" where "₹500" is bold and green.

<details>
<summary>Click to see an answer for 6</summary>

```swift
Text("Total: ")
    + Text("₹500").bold().foregroundStyle(.green)
```

</details>

---

## 🧠 Remember

- Use **text styles** (`.title`, `.body`, `.caption`) — they support **Dynamic Type**.
- `.bold()`, `.fontWeight()`, `.fontDesign()`, `.foregroundStyle()` style text.
- `.lineLimit()` and `.multilineTextAlignment()` for long text.
- `Image(systemName: "star.fill")` = SF Symbol. Style it like text.
- `Image("name")` = asset image. Use `.resizable()` **first**, then `.scaledToFit()` / `.scaledToFill()`.
- `Label("Text", systemImage: "icon")` = text + icon.
- Add `.accessibilityLabel` to meaningful images.

---

⬅️ **Back:** [Chapter 41 — What Is SwiftUI?](41-what-is-swiftui.md)
➡️ **Next:** [Chapter 43 — Stacks](43-stacks.md)
