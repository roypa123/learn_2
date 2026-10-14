# Chapter 49 — Navigation: Moving Between Screens

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- `NavigationStack` — the container for moving between screens.
- `.navigationTitle` — screen titles.
- `NavigationLink` — tap to go to the next screen.
- Passing data to the next screen.
- Value-based navigation with `.navigationDestination`.
- Going back by code, and going back to the start.
- The **toolbar** (buttons at the top).

---

## 1. How navigation works on iPhone 📱

Think of a **stack of cards** 🃏:

```
 Start:            Tap a row:          Tap again:          Tap "Back":
 ┌──────────┐      ┌──────────┐        ┌──────────┐        ┌──────────┐
 │  List    │      │ Details  │        │  Photo   │        │ Details  │
 │          │  →   │┌─────────┤   →    │┌─────────┤   ←    │┌─────────┤
 │          │      ││  List   │        ││ Details │        ││  List   │
 └──────────┘      └┴─────────┘        │├─────────┤        └┴─────────┘
                                       ││  List   │
                                       └┴─────────┘
```

- Going **forward** = putting a new card **on top** ("**push**").
- Going **back** = taking the top card **off** ("**pop**").

> 📖 **New word: Push / Pop**
> **Push** = open a new screen on top. **Pop** = go back to the previous screen.

---

## 2. `NavigationStack` and a title

```swift
struct ContentView: View {
    var body: some View {
        NavigationStack {
            Text("Welcome!")
                .navigationTitle("Home")
        }
    }
}
```

**Preview:** a big bold "Home" title at the top, "Welcome!" in the middle.

| Part | Meaning |
|---|---|
| `NavigationStack { }` | The container that allows moving between screens. Put it around your **first** screen — **once**. |
| `.navigationTitle("Home")` | The title at the top. Put it on the view **inside** the stack. |

⚠️ **Careful:** `.navigationTitle` goes on the **content inside** `NavigationStack`, **not** on the `NavigationStack` itself.

### Title display mode

```swift
.navigationTitle("Settings")
.navigationBarTitleDisplayMode(.inline)
```

| Mode | Looks like |
|---|---|
| `.large` | Big bold title (shrinks when you scroll). |
| `.inline` | Small title in the middle of the top bar. |
| `.automatic` | SwiftUI decides. |

---

## 3. `NavigationLink` — go to another screen

```swift
struct ContentView: View {
    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                NavigationLink("Go to Details") {
                    DetailView()
                }
                .buttonStyle(.borderedProminent)
            }
            .navigationTitle("Home")
        }
    }
}

struct DetailView: View {
    var body: some View {
        Text("You found the details page! 🎉")
            .font(.title2)
            .navigationTitle("Details")
    }
}
```

**Try it:** Tap "Go to Details" → the Details screen **slides in**. A **"< Home"** back button appears automatically. Tap it to go back. ✨

| Part | Meaning |
|---|---|
| `NavigationLink("Go to Details")` | A tappable link with this text. |
| `{ DetailView() }` | The **destination**: the screen to open. |
| Back button | SwiftUI adds it **for free**. Swiping from the left edge also goes back. |

### Custom link label

```swift
NavigationLink {
    DetailView()
} label: {
    Label("Open settings", systemImage: "gearshape")
}
```

Same pattern as `Button` (Chapter 45): first closure = destination, `label:` = how it looks.

---

## 4. Navigation in a List ⭐ (the most common pattern)

```swift
struct Animal: Identifiable {
    let id = UUID()
    let name: String
    let emoji: String
    let fact: String
}

struct ContentView: View {
    let animals = [
        Animal(name: "Elephant", emoji: "🐘", fact: "Elephants can't jump."),
        Animal(name: "Octopus", emoji: "🐙", fact: "An octopus has three hearts."),
        Animal(name: "Penguin", emoji: "🐧", fact: "Penguins can drink salt water."),
        Animal(name: "Sloth", emoji: "🦥", fact: "Sloths can hold their breath for 40 minutes.")
    ]

    var body: some View {
        NavigationStack {
            List(animals) { animal in
                NavigationLink {
                    AnimalDetailView(animal: animal)
                } label: {
                    HStack {
                        Text(animal.emoji).font(.largeTitle)
                        Text(animal.name).font(.headline)
                    }
                }
            }
            .navigationTitle("Animals")
        }
    }
}

struct AnimalDetailView: View {
    let animal: Animal

    var body: some View {
        VStack(spacing: 20) {
            Text(animal.emoji)
                .font(.system(size: 120))
            Text(animal.name)
                .font(.largeTitle.bold())
            Text(animal.fact)
                .font(.title3)
                .multilineTextAlignment(.center)
                .padding()
        }
        .navigationTitle(animal.name)
        .navigationBarTitleDisplayMode(.inline)
    }
}
```

| Part | Meaning |
|---|---|
| `NavigationLink { AnimalDetailView(animal: animal) }` | Pass the tapped animal to the next screen. |
| `let animal: Animal` | The detail view receives the data as a **property** (Chapter 41). |
| The `>` chevron | Lists show a `>` arrow automatically for navigation links. |

```
  Animals (List)                  Octopus (Detail)
 ┌────────────────────┐          ┌────────────────────┐
 │ 🐘 Elephant      > │   tap    │ < Animals  Octopus │
 │ 🐙 Octopus       > │  ─────►  │       🐙           │
 │ 🐧 Penguin       > │          │     Octopus        │
 │ 🦥 Sloth         > │          │ An octopus has     │
 └────────────────────┘          │ three hearts.      │
                                 └────────────────────┘
```

🧠 **Remember:** Pass data to the next screen through its **properties**.

---

## 5. Value-based navigation ⭐ (modern way)

Instead of writing the destination inside each link, you can link to a **value** and say **once** which screen shows that kind of value.

```swift
struct Animal: Identifiable, Hashable {
    let id = UUID()
    let name: String
    let emoji: String
    let fact: String
}

struct ContentView: View {
    let animals = [
        Animal(name: "Elephant", emoji: "🐘", fact: "Elephants can't jump."),
        Animal(name: "Octopus", emoji: "🐙", fact: "An octopus has three hearts.")
    ]

    var body: some View {
        NavigationStack {
            List(animals) { animal in
                NavigationLink(value: animal) {
                    Text("\(animal.emoji) \(animal.name)")
                }
            }
            .navigationTitle("Animals")
            .navigationDestination(for: Animal.self) { animal in
                AnimalDetailView(animal: animal)
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `Hashable` | The value must follow `Hashable` (Chapter 24). Just add it. |
| `NavigationLink(value: animal)` | "When tapped, navigate to **this value**." |
| `.navigationDestination(for: Animal.self)` | "Whenever we navigate to an `Animal`, show this screen." Written **once**. |

Why is this better?
- The destination screen is only **created when tapped** (faster for long lists).
- You can **control navigation from code** (next section).

⚠️ **Careful:** Put `.navigationDestination` **inside** the `NavigationStack` (on the list or its content), **not** inside a `List` row or a lazy container.

---

## 6. Navigating with code: `NavigationPath`

Sometimes you want to go to a screen **without** a tap on a link — for example after a button action, or to jump back to the start.

```swift
struct ContentView: View {
    @State private var path: [Int] = []

    var body: some View {
        NavigationStack(path: $path) {
            VStack(spacing: 20) {
                Button("Go to level 1") {
                    path.append(1)
                }
                .buttonStyle(.borderedProminent)
            }
            .navigationTitle("Start")
            .navigationDestination(for: Int.self) { level in
                LevelView(level: level, path: $path)
            }
        }
    }
}

struct LevelView: View {
    let level: Int
    @Binding var path: [Int]

    var body: some View {
        VStack(spacing: 20) {
            Text("Level \(level)")
                .font(.largeTitle.bold())

            Button("Next level →") {
                path.append(level + 1)
            }
            .buttonStyle(.borderedProminent)

            Button("Back to start 🏠") {
                path.removeAll()
            }
        }
        .navigationTitle("Level \(level)")
    }
}
```

| Part | Meaning |
|---|---|
| `@State private var path: [Int] = []` | An array that **is** the stack of screens. Empty = at the start. |
| `NavigationStack(path: $path)` | Connect the stack to the array. |
| `path.append(1)` | Push a new screen (shows `LevelView(level: 1)`). |
| `path.append(level + 1)` | Push the next level. |
| `path.removeAll()` | Pop **everything** → back to the start! 🏠 |
| `path.removeLast()` | Go back one screen. |
| `@Binding var path` | The child can change the parent's path (Chapter 52 explains `@Binding`). |

> 📖 **New word: NavigationPath**
> A list of values that represents the screens on the stack. You can use a typed array like `[Int]`, or the type `NavigationPath` for mixed types.

💡 **Tip:** Changing `path` **is** navigation. Add to it → go forward. Remove from it → go back.

---

## 7. Going back with code: `dismiss`

A screen can close **itself**:

```swift
struct DetailView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        Button("Done") {
            dismiss()
        }
        .navigationTitle("Details")
    }
}
```

| Part | Meaning |
|---|---|
| `@Environment(\.dismiss)` | Get the "close this screen" action from SwiftUI. |
| `dismiss()` | Go back (pop) — same as tapping the back button. |

> 📖 **New word: Environment**
> Values that SwiftUI gives to all views automatically: color scheme, text size, the `dismiss` action, and more. Read them with `@Environment`.

`dismiss` also closes **sheets** (Chapter 51).

---

## 8. The toolbar 🔧

Add buttons to the **top bar** (or the bottom).

```swift
struct ContentView: View {
    @State private var count = 0

    var body: some View {
        NavigationStack {
            Text("Count: \(count)")
                .font(.largeTitle)
                .navigationTitle("Counter")
                .toolbar {
                    ToolbarItem(placement: .topBarTrailing) {
                        Button {
                            count += 1
                        } label: {
                            Image(systemName: "plus")
                        }
                    }
                    ToolbarItem(placement: .topBarLeading) {
                        Button("Reset") {
                            count = 0
                        }
                    }
                }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `.toolbar { }` | Add toolbar items. Put it on the content inside the stack (like `.navigationTitle`). |
| `ToolbarItem(placement: .topBarTrailing)` | Top **right**. |
| `ToolbarItem(placement: .topBarLeading)` | Top **left**. |

Other placements:

| Placement | Where |
|---|---|
| `.topBarLeading` / `.topBarTrailing` | Top left / right |
| `.principal` | Top center (replaces the title) |
| `.bottomBar` | A bar at the bottom |
| `.confirmationAction` / `.cancellationAction` | "Save" / "Cancel" positions in sheets |

💡 **Tip:** If you just write a `Button` inside `.toolbar { }` without `ToolbarItem`, SwiftUI puts it in a default place (usually top-right).

### Hiding the back button or bar

```swift
.navigationBarBackButtonHidden(true)
.toolbar(.hidden, for: .navigationBar)
```

Use these rarely — users expect a back button!

---

## 9. Mini project: a recipe book 📖

```swift
struct Recipe: Identifiable, Hashable {
    let id = UUID()
    let name: String
    let emoji: String
    let minutes: Int
    let ingredients: [String]
    let steps: [String]
}

struct ContentView: View {
    let recipes = [
        Recipe(name: "Masala Chai", emoji: "☕", minutes: 10,
               ingredients: ["Water", "Milk", "Tea leaves", "Ginger", "Sugar"],
               steps: ["Boil water with ginger", "Add tea leaves", "Add milk and sugar", "Boil, then strain"]),
        Recipe(name: "Fruit Salad", emoji: "🥗", minutes: 5,
               ingredients: ["Apple", "Banana", "Grapes", "Honey"],
               steps: ["Cut the fruit", "Mix in a bowl", "Add honey"]),
        Recipe(name: "Pancakes", emoji: "🥞", minutes: 20,
               ingredients: ["Flour", "Milk", "Egg", "Sugar", "Butter"],
               steps: ["Mix everything", "Heat a pan with butter", "Cook both sides"])
    ]

    var body: some View {
        NavigationStack {
            List(recipes) { recipe in
                NavigationLink(value: recipe) {
                    HStack {
                        Text(recipe.emoji).font(.largeTitle)
                        VStack(alignment: .leading) {
                            Text(recipe.name).font(.headline)
                            Label("\(recipe.minutes) min", systemImage: "clock")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
            }
            .navigationTitle("Recipes 📖")
            .navigationDestination(for: Recipe.self) { recipe in
                RecipeDetailView(recipe: recipe)
            }
        }
    }
}

struct RecipeDetailView: View {
    let recipe: Recipe

    var body: some View {
        List {
            Section {
                HStack {
                    Spacer()
                    Text(recipe.emoji).font(.system(size: 100))
                    Spacer()
                }
            }

            Section("Ingredients") {
                ForEach(recipe.ingredients, id: \.self) { item in
                    Label(item, systemImage: "circle.fill")
                        .labelStyle(.titleAndIcon)
                }
            }

            Section("Steps") {
                ForEach(Array(recipe.steps.enumerated()), id: \.offset) { index, step in
                    Text("\(index + 1). \(step)")
                }
            }
        }
        .navigationTitle(recipe.name)
        .toolbar {
            Button {
                print("Saved \(recipe.name)")
            } label: {
                Image(systemName: "heart")
            }
        }
    }
}
```

| New thing | Meaning |
|---|---|
| `Array(recipe.steps.enumerated())` | Pairs of (number, step) — Chapter 14. `ForEach` needs an array. |
| `id: \.offset` | Use the position number as the ID. |
| `{ index, step in ... }` | Each pair gives the number and the step. |

---

## 🏋️ Practice

1. Make a `NavigationStack` with a title and a `NavigationLink` to a second screen with its own title.
2. Make a list of 5 countries. Tap one → a detail screen shows its flag emoji big and its capital.
3. Change exercise 2 to use `NavigationLink(value:)` and `.navigationDestination`.
4. Add a "Done" button on the detail screen that uses `dismiss()`.
5. Add a `+` button in the toolbar that adds a new item to a `@State` list.
6. Make 3 levels of screens (Level 1 → 2 → 3) and a button on level 3 that goes **back to the start** using a path.

---

## 🧠 Remember

- Wrap your **first** screen in `NavigationStack { }` — once.
- `.navigationTitle("…")` goes on the content **inside** the stack.
- `NavigationLink { Destination() } label: { … }` — tap to push a screen.
- Pass data to the next screen as a **property**.
- Modern: `NavigationLink(value:)` + `.navigationDestination(for:)`.
- `NavigationStack(path: $path)` → navigate with code: `append` to go forward, `removeAll()` to go home.
- `@Environment(\.dismiss)` → `dismiss()` to go back.
- `.toolbar { ToolbarItem(placement:) { … } }` for top-bar buttons.

---

⬅️ **Back:** [Chapter 48 — Lists and `ForEach`](48-lists-foreach.md)
➡️ **Next:** [Chapter 50 — Tabs](50-tabs.md)
