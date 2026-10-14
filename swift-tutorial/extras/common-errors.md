# 🔧 Common Errors and How to Fix Them

A quick-help page. When you see an error, search this page for a few words of the message (`Ctrl + F` / `Cmd + F`).

**How to use:** find the error → read **what it means** → try the **fix** → read the chapter if you need more help.

🧠 **Remember the method** (Chapter 40): **Read** the message slowly → find the **line** → fix the **first** error first → build again.

---

## 🟥 Part A — Swift errors (Parts 1–3)

### "cannot find 'X' in scope"

```
error: cannot find 'scroe' in scope
```

**Means:** Swift doesn't know this name.

**Fix:**
- Check the **spelling** (`score` not `scroe`).
- Check **big/small letters** (`Score` ≠ `score`). (Ch 3)
- Did you **create** it before using it? Order matters. (Ch 6)
- Was it created **inside** a function, `if` or loop? It only exists there. (Ch 18 — scope)
- In Xcode: is the file in the right **target**? (Ch 36 — Target Membership)

---

### "invalid redeclaration of 'X'"

**Means:** You made two things with the same name.

**Fix:** Use `var`/`let` only the **first** time. After that, just use the name: `score = 10`. (Ch 6)

---

### "cannot assign to value: 'X' is a 'let' constant"

**Means:** You tried to change a `let`.

**Fix:** Change `let` to `var` — or don't change it. (Ch 6)

---

### "cannot assign value of type 'String' to type 'Int'"

**Means:** The box is for one type, you gave another.

**Fix:** Use the correct type, or convert: `Int("42")`, `String(42)`, `Double(x)`. (Ch 7)

---

### "binary operator '+' cannot be applied to operands of type 'Int' and 'Double'"

**Means:** You mixed types in math.

**Fix:** Convert one side: `Double(a) + b`. (Ch 7, 8)

---

### My division is wrong! `7 / 2` gives `3`

**Means:** `Int / Int` drops the decimals.

**Fix:** Use Doubles: `Double(7) / Double(2)` → `3.5`. (Ch 8)

---

### "value of optional type 'Int?' must be unwrapped"

**Means:** You used an Optional as if it were a normal value.

**Fix:** Unwrap it: `if let`, `guard let`, `?? default`. (Ch 17)

```swift
let n = Int("5") ?? 0
```

---

### 💥 "Fatal error: Unexpectedly found nil while unwrapping an Optional value"

**Means:** You used `!` on something that was `nil`. **Crash.**

**Fix:** Replace `!` with `if let`, `guard let` or `??`. (Ch 17)

---

### 💥 "Fatal error: Index out of range"

**Means:** You asked for an array position that doesn't exist.

**Fix:**
- Remember indexes start at **0**. The last is `count - 1`. (Ch 14)
- Check first: `if index < array.count { ... }`
- Use `array.first` / `array.last` (Optionals) instead of `[0]`.

---

### 💥 "Fatal error: Division by zero"

**Fix:** Check before dividing: `guard b != 0 else { return 0 }`. (Ch 8)

---

### "switch must be exhaustive"

**Means:** Your `switch` doesn't cover every possible value.

**Fix:** Add `default:` — or for enums, add the missing `case`s. (Ch 11, 23)

---

### "missing return in global function expected to return 'X'"

**Means:** Some path through your function doesn't `return` a value.

**Fix:** Make sure **every** path (every `if`/`else` branch) returns something. (Ch 18)

---

### "missing argument label 'name:' in call" / "incorrect argument label"

**Means:** You called a function without the right labels.

**Fix:** Use the labels from the definition: `greet(name: "Ravi")`. Or define with `_` for no label. (Ch 18)

---

### "left side of mutating operator isn't mutable: 'self' is immutable"

**Means:** A struct method (or a SwiftUI view) tried to change a property.

**Fix:**
- In a normal struct: add `mutating` to the method. (Ch 20)
- In a SwiftUI view: use `@State private var`. (Ch 46)

---

### "class 'X' has no initializers"

**Fix:** Give every property a default value, or write an `init`. (Ch 21)

---

### "overriding declaration requires an 'override' keyword"

**Fix:** Add `override` before `func` in the subclass. (Ch 21)

---

### "type 'X' does not conform to protocol 'Y'"

**Means:** You promised to follow a protocol but forgot something.

**Fix:** Add the missing property/method. In Xcode, click the error → **Fix** to add stubs. (Ch 24)

---

### "call can throw but is not marked with 'try'"

**Fix:** Add `try` and handle errors with `do { } catch { }` (or use `try?`). (Ch 26)

---

### "expression is 'async' but is not marked with 'await'"

**Fix:** Add `await` before the call. (Ch 28)

### "'async' call in a function that does not support concurrency"

**Fix:** Wrap it in `Task { await ... }` or mark the function `async`. In SwiftUI, use `.task { }`. (Ch 28, 58)

---

### Concurrency warnings: "…is not concurrency-safe", "main actor-isolated…", "sending … risks causing data races"

**Means:** Swift 6's safety checker thinks two tasks might change the same data at once.

**Fix (beginner-friendly):**
- Mark classes used by the UI with `@MainActor` (Ch 53).
- Use structs (value types) for data passed between tasks.
- Check **Build Settings → Swift Language Version / Strict Concurrency Checking** (Ch 36). Learning projects can use Swift 5 mode while you learn.

---

## 🟧 Part B — Xcode errors (Part 4)

### "Signing for 'X' requires a development team"

**Fix:** Target → **Signing & Capabilities** → choose your **Team**. Add your Apple ID in **Xcode → Settings → Accounts** if needed. (Ch 38)

---

### "Failed to register bundle identifier" / "not available"

**Fix:** Make your Bundle ID more unique: `com.yourfullname.AppName`. (Ch 38)

---

### "Untrusted Developer" on iPhone

**Fix:** iPhone **Settings → General → VPN & Device Management** → your account → **Trust**. (Ch 39)

---

### "Developer Mode disabled"

**Fix:** iPhone **Settings → Privacy & Security → Developer Mode** → On → restart. (Ch 39)

---

### App on my iPhone stopped opening after a week

**Means:** Free Apple ID apps expire after **7 days**.

**Fix:** Connect the phone and run from Xcode again. (Ch 38, 39)

---

### Files show in **red** in the Project navigator

**Means:** Xcode can't find the file on disk (it was moved or renamed in Finder).

**Fix:** Select the file → File inspector (`Cmd + Option + 1`) → click the folder icon to locate it. Next time, move/rename **inside Xcode**. (Ch 33)

---

### Strange errors that make no sense / old code keeps running

**Fix, in order:**
1. **Product → Clean Build Folder** (`Cmd + Shift + K`), then build (`Cmd + B`).
2. Quit and reopen Xcode.
3. Delete the app from the Simulator and run again.
4. Restart the Mac.

(Ch 32, 34)

---

### "Archive" is grayed out

**Fix:** Change the run destination from a Simulator to **Any iOS Device (arm64)**. (Ch 65)

---

### Upload error: build number already used

**Fix:** Increase the **Build** number (Target → General). (Ch 36, 65)

---

## 🟨 Part C — SwiftUI errors (Part 5)

### "Cannot use mutating member on immutable value: 'self' is immutable" (in a View)

**Means:** You changed a plain `var` in a view.

**Fix:** Make it `@State private var`. If the value belongs to a parent, use `@Binding`. (Ch 46, 52)

---

### The screen doesn't update when I change a value

**Checklist:**
- Is the property `@State`, `@Binding`, `@AppStorage`, or inside an `@Observable` class? A plain `var` won't update the screen. (Ch 46)
- Did a child view get a **copy** (`@State` in the child) instead of a **binding**? (Ch 52)
- In a `ForEach` that edits items, did you use `ForEach($items) { $item in }`? (Ch 48)
- Is your `@Observable` class created with `@State` in the owner (not recreated every time)? (Ch 53)

---

### "The compiler is unable to type-check this expression in reasonable time"

**Means:** Your `body` is too big or complicated for Swift to understand quickly.

**Fix:** **Break it into smaller views** or computed properties. Also check for a small typo (like a wrong type) hidden inside a big view. (Ch 41)

---

### "Generic parameter 'X' could not be inferred" / weird errors on a whole view

**Means:** Often a **small typo somewhere inside** the view confuses Swift.

**Fix:** Comment out parts of `body` (`Cmd + /`) until the error disappears — then you know where the problem is. (Ch 5, 40)

---

### "Instance method 'X' requires that 'Y' conform to 'Identifiable'" (List / ForEach)

**Fix:** Make your type `Identifiable` (add `let id = UUID()`), or use `id: \.self` for simple unique values. (Ch 48)

---

### "Referencing initializer … requires that 'X' conform to 'Hashable'" (NavigationLink(value:))

**Fix:** Add `Hashable` to your type: `struct Recipe: Identifiable, Hashable`. (Ch 49)

---

### Image is huge / won't resize

**Fix:** Add `.resizable()` **first**, then `.scaledToFit()` or `.scaledToFill()`, then `.frame(...)`. (Ch 42)

---

### Navigation title doesn't show

**Fix:** Put `.navigationTitle(...)` on the view **inside** `NavigationStack`, not on the stack itself. Check there **is** a `NavigationStack`. (Ch 49)

---

### Tab bar disappears or titles act strangely with tabs

**Fix:** Put a `NavigationStack` **inside** each tab — not around the `TabView`. (Ch 50)

---

### Sheet doesn't close / no way to close

**Fix:** Use `@Environment(\.dismiss) private var dismiss` and call `dismiss()`. Always add a Done/Cancel button. (Ch 51)

---

### Preview crashes / "Cannot preview in this file"

**Fix:**
- Fix red errors first, then `Cmd + Option + P`.
- Views using `@Environment(SomeModel.self)` need it in the preview: `.environment(SomeModel())`. (Ch 53)
- Views with `@Query` need `.modelContainer(for: X.self, inMemory: true)`. (Ch 57)
- Views with `@Binding` need `.constant(value)` or `@Previewable @State`. (Ch 52)

---

### 💥 Crash: "No Observable object of type X found" (or similar)

**Means:** A view asks `@Environment(X.self)` but no one provided it.

**Fix:** Add `.environment(xObject)` higher up — in the App or root view (and in previews). (Ch 53)

---

### Keyboard covers my text field / won't go away

**Fix:** Put content in a `ScrollView` or `Form`. Use `@FocusState` and set it to `nil` to hide the keyboard, or add `.scrollDismissesKeyboard(.interactively)`. (Ch 47)

---

### Animation doesn't animate

**Checklist:**
- Is the state change inside `withAnimation { }`, or is `.animation(_, value:)` on the view **with the right value**? (Ch 55)
- For transitions: the view must be added/removed with `if`, **and** the change must be inside `withAnimation`. (Ch 55)
- Testing in the Canvas? Use **Live** mode or the Simulator.

---

## 🟩 Part D — Data, networking and JSON errors (Part 6)

### `@AppStorage` value isn't remembered

**Fix:** Test by **running** the app (not only the preview). Use the **same key** everywhere. Deleting the app clears it. (Ch 56)

---

### SwiftData app crashes after I changed my model

**Fix (while learning):** delete the app from the Simulator (clears the old database). For new properties, give them **default values**. (Ch 57)

---

### "`#Predicate` …" errors

**Fix:** Keep predicates simple: comparisons, `&&`, `||`, `!`, `contains`. If it still fails, load with `@Query` and filter in Swift with `.filter { }`. (Ch 57, 63)

---

### 💥 "This app has crashed because it attempted to access privacy-sensitive data without a usage description"

**Fix:** Add the matching **Privacy - … Usage Description** key in Target → Info. (Ch 37)

---

### "The resource could not be loaded because the App Transport Security policy requires the use of a secure connection"

**Means:** You used `http://` instead of `https://`.

**Fix:** Use an **HTTPS** URL. (Ch 37, 58)

---

### "The Internet connection appears to be offline" / "A server with the specified hostname could not be found"

**Fix:** Check Wi-Fi on the Mac/iPhone. Check the URL spelling. Show a friendly error with **Try again**. (Ch 58)

---

### My request "works" but data is wrong / empty

**Fix:** Check the **status code** (200–299 = OK). Print the raw response: `print(String(decoding: data, as: UTF8.self))`. (Ch 58)

---

### JSON decoding errors

| Message contains | Means | Fix | Ch |
|---|---|---|---|
| `keyNotFound` | A key is missing in the JSON. | Check spelling; make the property Optional; use `.convertFromSnakeCase` or `CodingKeys`. | 59 |
| `typeMismatch` | Wrong type (e.g. expected `Int`, got `9.99` or `"10"`). | Change the property's type. | 59 |
| `valueNotFound` | The value is `null`. | Make the property Optional. | 59 |
| `dataCorrupted` | Not valid JSON (maybe an HTML error page). | Print the raw text; check the URL and status code. | 58, 59 |
| Date errors | Date format doesn't match. | Set `dateDecodingStrategy` (`.iso8601`, etc.). | 59 |

---

### `AsyncImage` shows nothing / stays gray

**Fix:** Check the URL (HTTPS? correct?). Use the `phase` form to show `.failure`. Add `.resizable()` inside the content closure. (Ch 60)

---

### Tests can't see my app's code: "cannot find 'X' in scope" in tests

**Fix:** Add `@testable import YourAppName` at the top of the test file. Check the test target's "Target to be Tested". (Ch 64)

---

## 🆘 Still stuck?

1. **Read the error again**, slowly. Copy the important words.
2. **Search the web** for the exact error message (in quotes). Many people had the same problem! (Stack Overflow, Swift Forums, Apple Developer Forums.)
3. **Make it smaller:** comment out code until it works, then add back piece by piece. (Ch 40)
4. **Rubber duck:** explain the problem out loud. 🦆 (Ch 40)
5. **Take a break.** Seriously — many bugs are solved after a walk. 🚶

---

🏠 **Home:** [Table of Contents](../README.md) • **Also see:** [Glossary](glossary.md)
