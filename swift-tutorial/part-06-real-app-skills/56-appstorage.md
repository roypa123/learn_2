# Chapter 56 — Saving Small Data (`@AppStorage`)

🍎 **Needs a Mac**

---

## What you will learn

- Why apps forget everything when they close.
- `UserDefaults` — a small storage box for settings.
- `@AppStorage` — the SwiftUI way to use it.
- What you **can** and **cannot** save this way.
- Saving an enum (like a theme choice).
- Saving small structs with `Codable` (preview of Chapter 59).
- `@SceneStorage` — remembering screen state.

---

## 1. The problem: apps forget 🧠❌

Run any app from Part 5. Change some settings. Then **stop** the app (`Cmd + .`) and run it again.

Everything is **back to the start**! 😢

Why? `@State` and `@Observable` live in the app's **memory** (RAM). When the app closes, memory is cleared.

> 📖 **New word: Memory (RAM)**
> Fast, temporary storage. Cleared when the app closes. Like writing on a whiteboard.

> 📖 **New word: Persistent storage**
> Storage that **stays** after the app closes, like a notebook 📓. Also called "saving to disk".

> 📖 **New word: Persist**
> To **save** data so it's still there next time.

| Kind of data | Example | Tool |
|---|---|---|
| Small settings | Dark mode on/off, username, high score | **`@AppStorage`** (this chapter) |
| Lots of records | Notes, to-dos, contacts | **SwiftData** (Chapter 57) |
| Files | Photos, documents, JSON | **FileManager** (Chapter 61) |
| Passwords, tokens 🔐 | Login secrets | **Keychain** (not `@AppStorage`!) |

---

## 2. `UserDefaults` — the settings box 📦

iOS gives every app a small storage box called **UserDefaults**. It stores simple **key–value** pairs (like a dictionary — Chapter 15).

> 📖 **New word: UserDefaults**
> A small, simple storage for an app's settings. Saved automatically, survives app restarts.

The old way (still works anywhere in Swift):

```swift
// Save
UserDefaults.standard.set("Meena", forKey: "username")
UserDefaults.standard.set(42, forKey: "highScore")

// Read
let name = UserDefaults.standard.string(forKey: "username") ?? "Guest"
let score = UserDefaults.standard.integer(forKey: "highScore")
```

| Part | Meaning |
|---|---|
| `UserDefaults.standard` | The app's settings box. |
| `.set(value, forKey: "name")` | Save a value under a key (a label). |
| `.string(forKey:)` | Read a String. Returns an Optional (might not exist). |
| `.integer(forKey:)` | Read an Int. Returns `0` if not found. |

SwiftUI makes this **much** easier. 👇

---

## 3. `@AppStorage` ⭐

`@AppStorage` works like `@State`, but the value is **saved** in UserDefaults automatically.

```swift
struct ContentView: View {
    @AppStorage("tapCount") private var tapCount = 0

    var body: some View {
        VStack(spacing: 20) {
            Text("You tapped \(tapCount) times")
                .font(.title)
            Button("Tap me") {
                tapCount += 1
            }
            .buttonStyle(.borderedProminent)
        }
    }
}
```

**Try it:** Run the app. Tap 5 times. **Stop** the app. Run again. It still says **5**! 🎉

| Part | Meaning |
|---|---|
| `@AppStorage("tapCount")` | Save this value in UserDefaults under the key `"tapCount"`. |
| `= 0` | The **default** value, used only if nothing was saved yet. |
| `tapCount += 1` | Changes the value **and** saves it **and** updates the screen. |

🧠 **Remember:** `@AppStorage("key")` = `@State` that **remembers** after the app closes.

⚠️ **Careful:** In the **Canvas preview**, saved values may act differently. Test saving by **running** the app in the Simulator.

---

## 4. What types can `@AppStorage` save?

| ✅ Can save | ❌ Cannot save directly |
|---|---|
| `Bool` | Arrays (`[String]`) |
| `Int` | Dictionaries |
| `Double` | Your own structs |
| `String` | `Color` |
| `URL` | `Date` (directly) |
| `Data` | |
| Enums with an `Int` or `String` raw value ⭐ | |

For the ❌ types, see section 7 (Codable) or use SwiftData (Chapter 57).

---

## 5. A settings screen that remembers ⚙️

```swift
struct SettingsView: View {
    @AppStorage("username") private var username = ""
    @AppStorage("soundOn") private var soundOn = true
    @AppStorage("volume") private var volume = 0.7
    @AppStorage("fontSize") private var fontSize = 17.0

    var body: some View {
        NavigationStack {
            Form {
                Section("Profile") {
                    TextField("Your name", text: $username)
                }
                Section("Sound") {
                    Toggle("Sound effects", isOn: $soundOn)
                    Slider(value: $volume, in: 0...1)
                        .disabled(!soundOn)
                }
                Section("Text") {
                    Stepper("Font size: \(Int(fontSize))", value: $fontSize, in: 12...30)
                    Text("Preview text")
                        .font(.system(size: fontSize))
                }
            }
            .navigationTitle(username.isEmpty ? "Settings" : "Hi, \(username)!")
        }
    }
}
```

| Part | Meaning |
|---|---|
| `$username` | Bindings work exactly like `@State` (Chapter 47). |
| Every change | Saved **immediately**. No "Save" button needed! |

---

## 6. Saving an enum (theme choice) 🌗

Enums with a raw value (Chapter 23) can be saved directly:

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
    @AppStorage("theme") private var theme: AppTheme = .system

    var body: some View {
        Form {
            Picker("Theme", selection: $theme) {
                ForEach(AppTheme.allCases) { t in
                    Text(t.rawValue.capitalized)
                }
            }
            .pickerStyle(.segmented)
        }
        .preferredColorScheme(theme.colorScheme)
    }
}
```

This is the theme picker from Chapter 54 — but now it's **remembered**! 🎉

| Part | Meaning |
|---|---|
| `enum AppTheme: String` | A `String` raw value → `@AppStorage` saves `"dark"`, `"light"`… |
| `@AppStorage("theme") private var theme: AppTheme = .system` | Write the type, then the default. |

💡 **Tip:** Put `.preferredColorScheme(...)` at the top of your app (the `App` struct or the root view) so it affects **every** screen.

---

## 7. Saving a small struct with `Codable` (preview)

`@AppStorage` can't save a struct directly, but it **can** save `Data`. We can turn a struct into `Data` with **JSON** (Chapter 59 explains this fully).

```swift
struct Profile: Codable {
    var name: String
    var age: Int
    var favoriteColor: String
}

struct ContentView: View {
    @AppStorage("profileData") private var profileData = Data()
    @State private var profile = Profile(name: "", age: 10, favoriteColor: "Blue")

    var body: some View {
        Form {
            TextField("Name", text: $profile.name)
            Stepper("Age: \(profile.age)", value: $profile.age, in: 1...120)
            TextField("Favorite color", text: $profile.favoriteColor)
        }
        .onAppear(perform: load)
        .onChange(of: profile.name) { save() }
        .onChange(of: profile.age) { save() }
        .onChange(of: profile.favoriteColor) { save() }
    }

    func save() {
        if let data = try? JSONEncoder().encode(profile) {
            profileData = data
        }
    }

    func load() {
        if let saved = try? JSONDecoder().decode(Profile.self, from: profileData) {
            profile = saved
        }
    }
}
```

| Part | Meaning |
|---|---|
| `struct Profile: Codable` | "This struct can be turned into JSON and back." |
| `JSONEncoder().encode(profile)` | Struct → `Data`. Can throw, so `try?` (Chapter 26). |
| `JSONDecoder().decode(Profile.self, from:)` | `Data` → struct. |
| `.onChange(of:) { save() }` | Save whenever something changes. (This short form with no parameters works on iOS 17+.) |

⚠️ **Careful:** This is OK for **one small** struct. For **lists** of items, use SwiftData (Chapter 57) or a file (Chapter 61).

---

## 8. Rules for `@AppStorage` 📏

| ✅ Do | ❌ Don't |
|---|---|
| Save **small** settings and flags | Save big lists or images |
| Use clear, unique keys: `"soundOn"` | Use the same key for two different things |
| Give a sensible default | Store **passwords** or **tokens** 🔐 (use the Keychain) |
| Use the **same key** in every view that needs the value | Change a key name after release (users lose the old value) |

💡 **Tip:** To avoid typos in keys, keep them in one place:

```swift
enum StorageKeys {
    static let username = "username"
    static let soundOn = "soundOn"
}

@AppStorage(StorageKeys.username) private var username = ""
```

### Same key, many views

```swift
struct ViewA: View {
    @AppStorage("score") private var score = 0
    var body: some View { Button("Add") { score += 1 } }
}

struct ViewB: View {
    @AppStorage("score") private var score = 0
    var body: some View { Text("Score: \(score)") }
}
```

Both use `"score"` → when `ViewA` changes it, `ViewB` updates **automatically**. ✨

---

## 9. "First launch" — show onboarding only once 👋

A very common use:

```swift
struct RootView: View {
    @AppStorage("hasSeenOnboarding") private var hasSeenOnboarding = false

    var body: some View {
        if hasSeenOnboarding {
            Text("Main app 🏠")
                .font(.largeTitle)
        } else {
            VStack(spacing: 30) {
                Text("Welcome! 👋")
                    .font(.largeTitle.bold())
                Text("This screen only shows the first time.")
                Button("Get started") {
                    hasSeenOnboarding = true
                }
                .buttonStyle(.borderedProminent)
            }
        }
    }
}
```

Tap "Get started" → main app. Close and reopen → straight to the main app. 🎉

💡 **Tip:** To test onboarding again, delete the app from the Simulator (Chapter 34). That clears its UserDefaults.

---

## 10. `@SceneStorage` — remember where the user was

`@SceneStorage` saves **screen state** (like which tab was open, or a half-typed draft) so the app can **restore** it if iOS closes it in the background.

```swift
struct ContentView: View {
    @SceneStorage("selectedTab") private var selectedTab = 0
    @SceneStorage("draftMessage") private var draft = ""

    var body: some View {
        TabView(selection: $selectedTab) {
            TextField("Write a message...", text: $draft)
                .padding()
                .tabItem { Label("Write", systemImage: "pencil") }
                .tag(0)
            Text("Inbox")
                .tabItem { Label("Inbox", systemImage: "tray") }
                .tag(1)
        }
    }
}
```

| | `@AppStorage` | `@SceneStorage` |
|---|---|---|
| Saves | App **settings** | Screen **state** (UI position, drafts) |
| Shared between windows (iPad) | Yes, one value for the app | No, each window has its own |
| Survives | Always (until the app is deleted) | Mostly when iOS restores the app — not guaranteed |

---

## 11. Mini project: a high-score game 🏆

```swift
struct ContentView: View {
    @AppStorage("highScore") private var highScore = 0
    @AppStorage("playerName") private var playerName = "Player"
    @State private var score = 0
    @State private var timeLeft = 10
    @State private var isPlaying = false

    let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    var body: some View {
        VStack(spacing: 24) {
            TextField("Your name", text: $playerName)
                .textFieldStyle(.roundedBorder)
                .frame(width: 200)
                .multilineTextAlignment(.center)

            Text("🏆 Best: \(highScore)")
                .font(.headline)

            Text("\(score)")
                .font(.system(size: 80, weight: .bold, design: .rounded))
                .contentTransition(.numericText())

            Text(isPlaying ? "⏱️ \(timeLeft)s" : "Tap Start!")
                .font(.title2)

            if isPlaying {
                Button("TAP! 👆") {
                    withAnimation { score += 1 }
                }
                .font(.largeTitle)
                .buttonStyle(.borderedProminent)
                .controlSize(.extraLarge)
            } else {
                Button("Start") {
                    score = 0
                    timeLeft = 10
                    isPlaying = true
                }
                .buttonStyle(.bordered)
                .controlSize(.large)
            }
        }
        .padding()
        .onReceive(timer) { _ in
            guard isPlaying else { return }
            if timeLeft > 0 {
                timeLeft -= 1
            } else {
                isPlaying = false
                if score > highScore {
                    highScore = score
                }
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `@AppStorage("highScore")` | **Saved** — the best score survives restarts. |
| `@State private var score` | **Not** saved — each game starts at 0. |
| `Timer.publish(every: 1, ...)` | A timer that "ticks" every second. |
| `.onReceive(timer) { _ in ... }` | Run code on every tick. |
| `if score > highScore { highScore = score }` | New record? Save it! |

Play, close the app, reopen — your **best score** is still there. 🏆

---

## 🏋️ Practice

1. Make a counter with `@AppStorage`. Check that it remembers after restarting.
2. Make a settings form with a username, a "notifications" toggle and a "volume" slider — all remembered.
3. Save an enum `Language: String` (english, hindi, tamil) with a picker.
4. Add first-launch onboarding to one of your apps.
5. Show "Welcome back, NAME!" on the main screen using the saved username.
6. Add a "Reset high score" button to the game.

---

## 🧠 Remember

- `@State` is forgotten when the app closes. `@AppStorage` is **saved**.
- `@AppStorage("key") private var x = default` — use it just like `@State`.
- Saves: `Bool`, `Int`, `Double`, `String`, `URL`, `Data`, and raw-value **enums**.
- Use it for **small settings** only. Never for passwords.
- Same key in different views = shared, always in sync.
- `@SceneStorage` remembers screen state (tabs, drafts).

---

⬅️ **Back:** [Chapter 55 — Animations](../part-05-swiftui/55-animations.md)
➡️ **Next:** [Chapter 57 — Saving Big Data (SwiftData)](57-swiftdata.md)
