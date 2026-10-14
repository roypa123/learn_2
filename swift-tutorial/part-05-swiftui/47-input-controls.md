# Chapter 47 — Text Fields, Toggles, Sliders, Pickers

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- What a **binding** (`$`) is.
- `TextField`, `SecureField`, `TextEditor` — typing text.
- `Toggle` — on/off switch.
- `Slider` — choose a number by sliding.
- `Stepper` — + / − buttons.
- `Picker` — choose from a list.
- `DatePicker` and `ColorPicker`.
- `Form` — nice settings-style screens.
- Keyboard types and focus.

---

## 1. The `$` sign: bindings

Input controls need to **read** a value **and** **change** it.

```swift
@State private var name = ""

TextField("Your name", text: $name)
```

| Part | Meaning |
|---|---|
| `name` | The **value** (read only). |
| `$name` | A **binding** to the value — a two-way connection. The control can **read and write** it. |

> 📖 **New word: Binding**
> A two-way connection to a piece of state. When the user types, the state changes. When the state changes, the control updates.

```
   @State name  ◄═══════ $name ═══════►  TextField
   (the data)       (two-way link)     (the control)

   User types "Ravi"  →  name becomes "Ravi"
   Code sets name = "" →  TextField becomes empty
```

Think of a **TV remote** 📺: the remote doesn't **own** the TV, but it can read and change the channel.

🧠 **Remember:**
- `name` → **read** the value (for `Text`, `if`, etc.).
- `$name` → give a control **permission to change** it.

---

## 2. `TextField`

```swift
struct ContentView: View {
    @State private var name = ""

    var body: some View {
        VStack(spacing: 20) {
            TextField("Enter your name", text: $name)
                .textFieldStyle(.roundedBorder)

            Text(name.isEmpty ? "Hello, stranger!" : "Hello, \(name)! 👋")
                .font(.title2)
        }
        .padding()
    }
}
```

**Try it:** Type in the field (Live preview or Simulator). The greeting updates **with every letter**! ✨

| Part | Meaning |
|---|---|
| `"Enter your name"` | **Placeholder**: gray hint text shown when the field is empty. |
| `text: $name` | Binding: what the user types goes into `name`. |
| `.textFieldStyle(.roundedBorder)` | A field with a visible border. |

> 📖 **New word: Placeholder**
> Gray hint text inside an empty field. It disappears when you type.

### Useful modifiers for text fields

```swift
TextField("Email", text: $email)
    .keyboardType(.emailAddress)
    .textInputAutocapitalization(.never)
    .autocorrectionDisabled()
    .textContentType(.emailAddress)
    .submitLabel(.next)
```

| Modifier | Meaning |
|---|---|
| `.keyboardType(.emailAddress)` | Show a keyboard with `@` and `.` keys. |
| `.textInputAutocapitalization(.never)` | Don't make the first letter capital. |
| `.autocorrectionDisabled()` | Don't "fix" spelling (bad for emails and usernames). |
| `.textContentType(.emailAddress)` | Help iOS suggest the user's saved email. |
| `.submitLabel(.next)` | The return key says "Next" instead of "return". |

Keyboard types:

| Keyboard | Use for |
|---|---|
| `.default` | Normal text |
| `.emailAddress` | Emails |
| `.numberPad` | Whole numbers (no dot) — PINs, quantities |
| `.decimalPad` | Numbers with a dot — prices |
| `.phonePad` | Phone numbers |
| `.URL` | Website addresses |

### Typing numbers directly

```swift
@State private var age = 0

TextField("Age", value: $age, format: .number)
    .keyboardType(.numberPad)
```

| Part | Meaning |
|---|---|
| `value: $age` | Bind to an **Int** (not a String). |
| `format: .number` | Convert between text and number automatically. |

### Running code when the user presses return

```swift
TextField("Search", text: $query)
    .onSubmit {
        print("Searching for \(query)")
    }
```

---

## 3. `SecureField` — passwords 🔒

```swift
@State private var password = ""

SecureField("Password", text: $password)
    .textFieldStyle(.roundedBorder)
    .textContentType(.password)
```

Each letter shows as a dot `•`. Same as `TextField` otherwise.

---

## 4. `TextEditor` — long text

```swift
@State private var notes = ""

TextEditor(text: $notes)
    .frame(height: 150)
    .padding(4)
    .overlay(RoundedRectangle(cornerRadius: 8).stroke(.gray.opacity(0.4)))
```

For many lines of text (notes, messages). It has no placeholder — add a border so people can see it.

💡 **Tip:** A `TextField` can also grow to several lines:
`TextField("Message", text: $message, axis: .vertical).lineLimit(3...6)`

---

## 5. Dismissing the keyboard: `@FocusState`

```swift
struct ContentView: View {
    @State private var name = ""
    @FocusState private var nameIsFocused: Bool

    var body: some View {
        VStack(spacing: 20) {
            TextField("Name", text: $name)
                .textFieldStyle(.roundedBorder)
                .focused($nameIsFocused)

            Button("Done") {
                nameIsFocused = false
            }
        }
        .padding()
    }
}
```

| Part | Meaning |
|---|---|
| `@FocusState private var nameIsFocused: Bool` | Tracks whether the field is **active** (keyboard showing). |
| `.focused($nameIsFocused)` | Connect the field to it. |
| `nameIsFocused = false` | Hide the keyboard. |
| `nameIsFocused = true` | Put the cursor in the field and show the keyboard. |

> 📖 **New word: Focus**
> The field that is currently active and receiving typed text.

You can also hide the keyboard when the user scrolls: add `.scrollDismissesKeyboard(.interactively)` to a `ScrollView` or `Form`.

---

## 6. `Toggle` — on/off switch

```swift
struct ContentView: View {
    @State private var notificationsOn = true
    @State private var darkMode = false

    var body: some View {
        VStack(spacing: 20) {
            Toggle("Notifications", isOn: $notificationsOn)
            Toggle("Dark mode", isOn: $darkMode)
                .tint(.purple)

            Text(notificationsOn ? "🔔 You'll get notifications" : "🔕 Notifications are off")
        }
        .padding()
    }
}
```

| Part | Meaning |
|---|---|
| `Toggle("Notifications", isOn: $notificationsOn)` | A switch with a label. Bound to a **Bool**. |
| `.tint(.purple)` | Color when ON. |

### Toggle with a custom label

```swift
Toggle(isOn: $wifiOn) {
    Label("Wi-Fi", systemImage: "wifi")
}
```

---

## 7. `Slider`

```swift
struct ContentView: View {
    @State private var volume = 50.0

    var body: some View {
        VStack(spacing: 20) {
            Text("Volume: \(Int(volume))")
                .font(.title2)

            Slider(value: $volume, in: 0...100, step: 1) {
                Text("Volume")
            } minimumValueLabel: {
                Image(systemName: "speaker.fill")
            } maximumValueLabel: {
                Image(systemName: "speaker.wave.3.fill")
            }
        }
        .padding()
    }
}
```

| Part | Meaning |
|---|---|
| `value: $volume` | Bound to a **Double** (must be a decimal type). |
| `in: 0...100` | The range (Chapter 11). |
| `step: 1` | Jump in steps of 1. |
| `{ Text("Volume") }` | A label (used by VoiceOver). |
| `minimumValueLabel` / `maximumValueLabel` | Icons at each end. |

The simplest form: `Slider(value: $volume, in: 0...100)`

⚠️ **Careful:** `Slider` needs a `Double` (or `Float`), not an `Int`. Use `Int(volume)` to show a whole number.

---

## 8. `Stepper`

```swift
@State private var quantity = 1

Stepper("Quantity: \(quantity)", value: $quantity, in: 1...10)
```

| Part | Meaning |
|---|---|
| `value: $quantity` | Bound to a number. |
| `in: 1...10` | Can't go below 1 or above 10. |
| `step: 2` (optional) | Change by 2 each tap. |

---

## 9. `Picker` — choose one option

```swift
struct ContentView: View {
    @State private var size = "Medium"
    let sizes = ["Small", "Medium", "Large"]

    var body: some View {
        VStack(spacing: 30) {
            Picker("Size", selection: $size) {
                ForEach(sizes, id: \.self) { s in
                    Text(s)
                }
            }
            .pickerStyle(.segmented)

            Text("You chose: \(size)")
        }
        .padding()
    }
}
```

| Part | Meaning |
|---|---|
| `Picker("Size", selection: $size)` | The label and the binding to the chosen value. |
| `ForEach(sizes, id: \.self) { s in Text(s) }` | One option per item. |
| `.pickerStyle(.segmented)` | Show as a row of buttons. |

### Picker styles

| Style | Looks like |
|---|---|
| `.menu` | A button that opens a menu (default in many places). |
| `.segmented` | A row of connected buttons. Best for 2–5 options. |
| `.wheel` | A spinning wheel 🎡. |
| `.inline` | All options shown in a list (in a Form). |
| `.navigationLink` | Opens a new screen with the options (in a Form inside navigation). |

### Picker with an enum ⭐ (best practice)

```swift
enum Flavor: String, CaseIterable, Identifiable {
    case vanilla, chocolate, strawberry
    var id: Self { self }
}

struct ContentView: View {
    @State private var flavor: Flavor = .chocolate

    var body: some View {
        VStack {
            Picker("Flavor", selection: $flavor) {
                ForEach(Flavor.allCases) { f in
                    Text(f.rawValue.capitalized)
                }
            }
            .pickerStyle(.segmented)

            Text("🍦 \(flavor.rawValue)")
        }
        .padding()
    }
}
```

| Part | Meaning |
|---|---|
| `enum Flavor: String, CaseIterable, Identifiable` | Chapter 23 + 24! |
| `var id: Self { self }` | Each case is its own ID. |
| `ForEach(Flavor.allCases)` | One option per case. |
| `.capitalized` | `"vanilla"` → `"Vanilla"`. |

💡 **Tip:** Using an enum means **no typos** and Swift checks everything. Much safer than strings!

---

## 10. `DatePicker`

```swift
@State private var birthday = Date.now

DatePicker("Birthday", selection: $birthday, displayedComponents: .date)
```

| Part | Meaning |
|---|---|
| `selection: $birthday` | Bound to a `Date`. |
| `displayedComponents: .date` | Only choose the **date** (not time). Also `.hourAndMinute`, or both: `[.date, .hourAndMinute]`. |

Limit the range:

```swift
DatePicker("Appointment",
           selection: $appointment,
           in: Date.now...,
           displayedComponents: [.date, .hourAndMinute])
```

`in: Date.now...` = only today or later (a one-sided range — Chapter 11).

Styles: `.datePickerStyle(.compact)` (default, small), `.graphical` (a calendar 📅), `.wheel`.

---

## 11. `ColorPicker`

```swift
@State private var favoriteColor = Color.blue

ColorPicker("Favorite color", selection: $favoriteColor)

Circle()
    .fill(favoriteColor)
    .frame(width: 100, height: 100)
```

Tap the color circle → choose any color → the big circle changes. 🎨

---

## 12. `Form` — settings-style screens ⭐

Wrap controls in a `Form` and they look like the iPhone **Settings** app:

```swift
struct ContentView: View {
    @State private var username = ""
    @State private var notifications = true
    @State private var volume = 0.5
    @State private var theme = "System"
    @State private var birthday = Date.now

    var body: some View {
        Form {
            Section("Profile") {
                TextField("Username", text: $username)
                DatePicker("Birthday", selection: $birthday, displayedComponents: .date)
            }

            Section("Preferences") {
                Toggle("Notifications", isOn: $notifications)
                Picker("Theme", selection: $theme) {
                    Text("System").tag("System")
                    Text("Light").tag("Light")
                    Text("Dark").tag("Dark")
                }
            }

            Section {
                Slider(value: $volume)
            } header: {
                Text("Sound")
            } footer: {
                Text("Volume: \(Int(volume * 100))%")
            }

            Section {
                Button("Save") { print("Saved \(username)") }
                Button("Log out", role: .destructive) { }
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `Form { }` | A scrolling, grouped list for input controls. |
| `Section("Profile") { }` | A group with a title. |
| `Text("Light").tag("Light")` | `.tag` says which **value** this option has. Needed when options aren't made with `ForEach`. |
| `header:` / `footer:` | Text above and below a section. |

> 📖 **New word: tag**
> The value a Picker option represents. When chosen, the binding gets this value.

---

## 13. Mini project: sign-up form 📝

```swift
struct ContentView: View {
    @State private var name = ""
    @State private var email = ""
    @State private var password = ""
    @State private var age = 18
    @State private var agreed = false
    @State private var message = ""

    var isEmailValid: Bool {
        email.contains("@") && email.contains(".")
    }

    var canSubmit: Bool {
        !name.isEmpty && isEmailValid && password.count >= 8 && agreed
    }

    var body: some View {
        Form {
            Section("Your details") {
                TextField("Full name", text: $name)
                    .textContentType(.name)

                TextField("Email", text: $email)
                    .keyboardType(.emailAddress)
                    .textInputAutocapitalization(.never)
                    .autocorrectionDisabled()

                if !email.isEmpty && !isEmailValid {
                    Text("Please enter a valid email")
                        .font(.caption)
                        .foregroundStyle(.red)
                }

                SecureField("Password (8+ characters)", text: $password)

                Stepper("Age: \(age)", value: $age, in: 13...100)
            }

            Section {
                Toggle("I agree to the terms", isOn: $agreed)
            }

            Section {
                Button("Create account") {
                    message = "Welcome, \(name)! 🎉"
                }
                .disabled(!canSubmit)

                if !message.isEmpty {
                    Text(message)
                        .foregroundStyle(.green)
                }
            }
        }
    }
}
```

| Part | What it does |
|---|---|
| 6 `@State` values | Everything the user can change. |
| `isEmailValid`, `canSubmit` | Computed from state (Chapter 46). |
| Red error text | Only shows when the email is typed **and** invalid. |
| `.disabled(!canSubmit)` | The button turns on only when everything is OK. Automatically! ✨ |

---

## 🏋️ Practice

1. Make a `TextField` and show the number of characters typed below it.
2. Make a `Toggle` "Show details". When on, show a paragraph of text.
3. Make 3 `Slider`s for red, green and blue (0...1). Show a rectangle with `Color(red:green:blue:)` using them.
4. Make a `Picker` with an enum of 4 pets (🐶 🐱 🐰 🐹), segmented style. Show the chosen pet big.
5. Build a "Pizza order" `Form`: name, size picker, extra cheese toggle, quantity stepper, and a summary text.
6. Use `@FocusState` to hide the keyboard with a "Done" button.

<details>
<summary>Click to see an answer for 3</summary>

```swift
struct ContentView: View {
    @State private var red = 0.5
    @State private var green = 0.5
    @State private var blue = 0.5

    var body: some View {
        VStack(spacing: 20) {
            RoundedRectangle(cornerRadius: 20)
                .fill(Color(red: red, green: green, blue: blue))
                .frame(height: 200)

            Slider(value: $red).tint(.red)
            Slider(value: $green).tint(.green)
            Slider(value: $blue).tint(.blue)
        }
        .padding()
    }
}
```

</details>

---

## 🧠 Remember

- `$value` = a **binding**: a two-way link so a control can **change** your state.
- `TextField("hint", text: $text)`, `SecureField` for passwords, `TextEditor` for long text.
- `Toggle(isOn: $bool)`, `Slider(value: $double, in:)`, `Stepper(value: $int, in:)`.
- `Picker(selection: $choice) { ... }` — use an **enum** for options. Style with `.pickerStyle()`.
- `DatePicker`, `ColorPicker` for dates and colors.
- `Form` + `Section` = Settings-style screens.
- `@FocusState` + `.focused()` controls the keyboard.

---

⬅️ **Back:** [Chapter 46 — `@State`](46-state.md)
➡️ **Next:** [Chapter 48 — Lists and `ForEach`](48-lists-foreach.md)
