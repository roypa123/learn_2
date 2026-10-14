# Chapter 53 — `@Observable`: Sharing Data Across the App

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- The problem: passing bindings through **many** views is tiring.
- `@Observable` — a **class** that SwiftUI watches.
- Owning it with `@State`.
- Passing it to child views.
- `@Environment` — sharing with **all** views, without passing.
- `@Bindable` — making bindings from an observable object.
- Putting app logic in a **model** (a simple architecture).

---

## 1. The problem: "prop drilling" 🕳️

Imagine a shopping app. The **cart** is needed by:
- The product list (to add items),
- The product detail (to add items),
- The cart tab (to show items),
- The tab bar (to show a badge).

With `@State` + `@Binding`, you'd pass `$cart` through **every** view in between — even views that don't use it.

```
 App
  └ TabView          ← passes $cart
     └ ShopTab        ← passes $cart
        └ ProductList  ← passes $cart
           └ ProductRow ← passes $cart
              └ AddButton ← finally uses it! 😩
```

This is called **prop drilling**. It's messy.

We want **one shared object** that any view can reach. That's `@Observable`.

---

## 2. Making an `@Observable` class

```swift
import SwiftUI
import Observation

@Observable
class Counter {
    var count = 0

    func increment() {
        count += 1
    }

    func reset() {
        count = 0
    }
}
```

| Part | Meaning |
|---|---|
| `import Observation` | The framework for `@Observable`. (Importing `SwiftUI` usually brings it in too.) |
| `@Observable` | A **macro**: "SwiftUI, watch every property of this class. When one changes, update the views that use it." |
| `class Counter` | It must be a **class** (shared, reference type — Chapter 21). |
| `var count = 0` | A normal property. No `@State` needed inside! |
| `func increment()` | Logic lives **in** the model. |

> 📖 **New word: Macro**
> A word starting with `@` or `#` that **writes extra code for you** when building. `@Observable` and `#Preview` are macros.

> 📖 **New word: Observable**
> Something that can be **watched**. When it changes, watchers are told.

Why a class? Because a class is **shared** (Chapter 22): every view that has it sees the **same** object. Change it in one place → everyone sees the change.

---

## 3. Using it in a view

```swift
struct ContentView: View {
    @State private var counter = Counter()

    var body: some View {
        VStack(spacing: 20) {
            Text("\(counter.count)")
                .font(.system(size: 80, weight: .bold))
            HStack {
                Button("Add 1") { counter.increment() }
                Button("Reset") { counter.reset() }
            }
            .buttonStyle(.bordered)
        }
    }
}
```

| Part | Meaning |
|---|---|
| `@State private var counter = Counter()` | This view **creates and owns** the object. `@State` keeps it alive while the view exists. |
| `counter.count` | Reading it → SwiftUI remembers "this view uses `count`". |
| `counter.increment()` | Changes `count` → SwiftUI updates the view. ✨ |

🧠 **Remember:** The view that **creates** the observable object holds it with `@State`.

---

## 4. Passing it to child views

Just pass it like a normal value — **no `$`, no `@Binding`!**

```swift
struct ContentView: View {
    @State private var counter = Counter()

    var body: some View {
        VStack(spacing: 30) {
            CounterDisplay(counter: counter)
            CounterButtons(counter: counter)
        }
    }
}

struct CounterDisplay: View {
    let counter: Counter

    var body: some View {
        Text("\(counter.count)")
            .font(.system(size: 80, weight: .bold))
    }
}

struct CounterButtons: View {
    let counter: Counter

    var body: some View {
        HStack {
            Button("−") { counter.count -= 1 }
            Button("+") { counter.increment() }
        }
        .font(.largeTitle)
        .buttonStyle(.bordered)
    }
}
```

| Part | Meaning |
|---|---|
| `let counter: Counter` | The child receives the **same object** (a reference). |
| `counter.count -= 1` in the child | Allowed! It's a class — `let` only means "always the same object" (Chapter 21). |
| Display updates | Because both views share the **same** `Counter`. |

```
          ContentView
       @State counter ──────┐
          /       \         │  all point to
  CounterDisplay  CounterButtons   the SAME object
   let counter     let counter ────┤
                                   ▼
                          ┌─────────────────┐
                          │ Counter object  │
                          │   count = 5     │
                          └─────────────────┘
```

---

## 5. `@Environment`: share with everyone, no passing needed 🌍

Put the object into the **environment** at the top, and **any** view below can grab it.

```swift
@Observable
class Cart {
    var items: [String] = []

    var count: Int { items.count }

    func add(_ item: String) {
        items.append(item)
    }
}

struct ContentView: View {
    @State private var cart = Cart()

    var body: some View {
        TabView {
            ShopView()
                .tabItem { Label("Shop", systemImage: "bag.fill") }

            CartView()
                .tabItem { Label("Cart", systemImage: "cart.fill") }
                .badge(cart.count)
        }
        .environment(cart)
    }
}

struct ShopView: View {
    let products = ["🍎 Apple", "🍌 Banana", "🥭 Mango"]

    var body: some View {
        NavigationStack {
            List(products, id: \.self) { product in
                ProductRow(product: product)
            }
            .navigationTitle("Shop")
        }
    }
}

struct ProductRow: View {
    @Environment(Cart.self) private var cart
    let product: String

    var body: some View {
        HStack {
            Text(product)
            Spacer()
            Button("Add") {
                cart.add(product)
            }
            .buttonStyle(.bordered)
        }
    }
}

struct CartView: View {
    @Environment(Cart.self) private var cart

    var body: some View {
        NavigationStack {
            List(cart.items, id: \.self) { item in
                Text(item)
            }
            .navigationTitle("Cart (\(cart.count))")
        }
    }
}
```

| Part | Meaning |
|---|---|
| `.environment(cart)` | Put the cart into the environment for **all** views inside the `TabView`. |
| `@Environment(Cart.self) private var cart` | "Give me the `Cart` from the environment." |
| `ShopView` | Doesn't mention the cart at all! No drilling. 🎉 |
| `ProductRow` | Grabs the cart directly. |

⚠️ **Careful:** If a view asks for `@Environment(Cart.self)` but **no one** put a `Cart` into the environment above it, the app **crashes**. In previews, add it too:

```swift
#Preview {
    CartView()
        .environment(Cart())
}
```

💡 **Tip:** Put `.environment(...)` at the **top** of your app — often in the `App` struct (Chapter 33):

```swift
@main
struct MyShopApp: App {
    @State private var cart = Cart()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(cart)
        }
    }
}
```

---

## 6. `@Bindable`: bindings from an observable object

Controls like `TextField` and `Toggle` need a **binding** (`$`). How do you get one from an `@Observable` object?

### If the view **owns** it with `@State` → `$` works:

```swift
@State private var profile = Profile()
TextField("Name", text: $profile.name)    // ✅
```

### If the view **receives** it (`let`) → use `@Bindable`:

```swift
@Observable
class Profile {
    var name = ""
    var notifications = true
}

struct ProfileEditor: View {
    @Bindable var profile: Profile

    var body: some View {
        Form {
            TextField("Name", text: $profile.name)
            Toggle("Notifications", isOn: $profile.notifications)
        }
    }
}
```

| Part | Meaning |
|---|---|
| `@Bindable var profile: Profile` | "I received this object, and I want to make **bindings** (`$`) to its properties." |
| `$profile.name` | A binding to the `name` property. |

### If you got it from `@Environment` → make a `@Bindable` inside `body`:

```swift
struct SettingsView: View {
    @Environment(Profile.self) private var profile

    var body: some View {
        @Bindable var profile = profile
        Form {
            TextField("Name", text: $profile.name)
        }
    }
}
```

### Summary table

| How you got the object | To read & call methods | To make `$` bindings |
|---|---|---|
| Created it: `@State private var x = Model()` | `x.value` | `$x.value` ✅ |
| Received it: `let x: Model` | `x.value` | Change to `@Bindable var x: Model` |
| From environment: `@Environment(Model.self) var x` | `x.value` | `@Bindable var x = x` inside `body` |

---

## 7. When to use what? 🧭

| Situation | Use |
|---|---|
| Simple data used by **one** view (is the sheet open? text typed?) | `@State` with a value type |
| A **child** needs to change the parent's simple data | `@Binding` |
| Data with **logic**, or shared by **several** views | `@Observable` class + `@State` in the owner |
| Data needed **everywhere** in the app (user, cart, settings) | `@Observable` + `.environment()` + `@Environment` |
| Need `$` bindings from an observable object you received | `@Bindable` |

> 📖 **New word: Model**
> The part of your code that holds **data and logic**, separate from the views. Your `@Observable` classes are models.

---

## 8. Older code: `ObservableObject` (just so you know)

You will see **older** SwiftUI code (before iOS 17) that looks like this:

```swift
class OldCounter: ObservableObject {
    @Published var count = 0
}

struct OldView: View {
    @StateObject private var counter = OldCounter()
    // child views: @ObservedObject var counter: OldCounter
    // environment: @EnvironmentObject var counter: OldCounter
}
```

| Old (iOS 13–16) | New (iOS 17+) |
|---|---|
| `class X: ObservableObject` | `@Observable class X` |
| `@Published var` | just `var` |
| `@StateObject` | `@State` |
| `@ObservedObject` | `let` (or `@Bindable`) |
| `@EnvironmentObject` | `@Environment(X.self)` |

🧠 **Remember:** For new apps, use `@Observable`. It's simpler and faster. But you'll understand old tutorials now! 😊

---

## 9. Main actor (one sentence)

UI must be updated on the **main thread**. If your model loads data with `async` code (Chapter 28), mark the class `@MainActor` so its changes always happen on the main thread:

```swift
@MainActor
@Observable
class WeatherModel {
    var temperature = 0
    func load() async { ... }
}
```

> 📖 **New word: `@MainActor`**
> "Run this on the main thread" — the thread that updates the screen. (Chapter 28 mentioned actors.)

New Xcode projects may even make this the **default** for your app code. Part 6 uses this when loading data from the internet.

---

## 10. Mini project: a habit tracker ✅

```swift
import SwiftUI

struct Habit: Identifiable {
    let id = UUID()
    var name: String
    var emoji: String
    var streak = 0
    var doneToday = false
}

@Observable
class HabitStore {
    var habits: [Habit] = [
        Habit(name: "Drink water", emoji: "💧"),
        Habit(name: "Read 10 pages", emoji: "📚"),
        Habit(name: "Walk", emoji: "🚶")
    ]

    var doneCount: Int {
        habits.filter { $0.doneToday }.count
    }

    var progress: Double {
        habits.isEmpty ? 0 : Double(doneCount) / Double(habits.count)
    }

    func toggle(_ habit: Habit) {
        guard let index = habits.firstIndex(where: { $0.id == habit.id }) else { return }
        habits[index].doneToday.toggle()
        habits[index].streak += habits[index].doneToday ? 1 : -1
    }

    func add(name: String, emoji: String) {
        habits.append(Habit(name: name, emoji: emoji))
    }

    func delete(at offsets: IndexSet) {
        habits.remove(atOffsets: offsets)
    }
}

struct ContentView: View {
    @State private var store = HabitStore()

    var body: some View {
        NavigationStack {
            VStack {
                ProgressHeader()
                HabitList()
            }
            .navigationTitle("Habits")
            .toolbar {
                AddHabitButton()
            }
        }
        .environment(store)
    }
}

struct ProgressHeader: View {
    @Environment(HabitStore.self) private var store

    var body: some View {
        VStack(spacing: 8) {
            ProgressView(value: store.progress)
                .tint(.green)
            Text("\(store.doneCount) of \(store.habits.count) done today")
                .font(.subheadline)
                .foregroundStyle(.secondary)
        }
        .padding()
    }
}

struct HabitList: View {
    @Environment(HabitStore.self) private var store

    var body: some View {
        List {
            ForEach(store.habits) { habit in
                HStack {
                    Text(habit.emoji).font(.largeTitle)
                    VStack(alignment: .leading) {
                        Text(habit.name).font(.headline)
                        Text("🔥 \(habit.streak) day streak")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                    Spacer()
                    Button {
                        store.toggle(habit)
                    } label: {
                        Image(systemName: habit.doneToday ? "checkmark.circle.fill" : "circle")
                            .font(.title)
                            .foregroundStyle(habit.doneToday ? .green : .gray)
                    }
                    .buttonStyle(.borderless)
                }
            }
            .onDelete { store.delete(at: $0) }
        }
    }
}

struct AddHabitButton: View {
    @Environment(HabitStore.self) private var store
    @State private var showAlert = false
    @State private var name = ""

    var body: some View {
        Button {
            showAlert = true
        } label: {
            Image(systemName: "plus")
        }
        .alert("New habit", isPresented: $showAlert) {
            TextField("Habit name", text: $name)
            Button("Add") {
                store.add(name: name, emoji: "⭐")
                name = ""
            }
            Button("Cancel", role: .cancel) { name = "" }
        }
    }
}

#Preview {
    ContentView()
}
```

| Part | Role |
|---|---|
| `struct Habit` | Simple data (value type). |
| `@Observable class HabitStore` | The **model**: holds all habits + all logic (toggle, add, delete, progress). |
| `@State private var store` in `ContentView` | The **one** owner / source of truth. |
| `.environment(store)` | Shared with every view below. |
| `ProgressHeader`, `HabitList`, `AddHabitButton` | Each grabs the store from the environment. **Nothing is passed down!** |
| `ProgressView(value:)` | A built-in progress bar (0.0 to 1.0). |

Tap a circle → the progress bar, the count and the streak **all** update. 🎉

🧠 **Remember:** Views **show** data and **call** model methods. The model **holds** data and **does** the logic. This keeps views simple.

---

## 🏋️ Practice

1. Make an `@Observable class Scoreboard` with `homeScore` and `awayScore` and methods to add points. Use it in a view.
2. Split it into two child views (`ScoreDisplay`, `ScoreButtons`) that receive the object with `let`.
3. Change it to use `.environment()` and `@Environment` instead.
4. Make an `@Observable class UserSettings` with `username` and `darkMode`. Make a `SettingsForm` that receives it with `@Bindable` and uses a `TextField` and `Toggle`.
5. Add a "Reset all" method to `HabitStore` that sets every `doneToday` to `false`, and a toolbar button for it.

---

## 🧠 Remember

- `@Observable class Model { var x = 0 }` — SwiftUI watches its properties automatically.
- The owner creates it with `@State private var model = Model()`.
- Pass it to children as a normal value (`let`). Changes are shared — it's a class.
- `.environment(model)` at the top + `@Environment(Model.self)` anywhere below = no prop drilling.
- `@Bindable` to make `$` bindings from an object you received.
- Put **logic** in the model, keep **views** simple.
- Old code uses `ObservableObject` / `@Published` / `@StateObject` — new code uses `@Observable`.

---

⬅️ **Back:** [Chapter 52 — `@Binding`](52-binding.md)
➡️ **Next:** [Chapter 54 — Colors, Fonts and Dark Mode](54-colors-fonts-dark-mode.md)
