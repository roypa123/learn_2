# Chapter 48 — Lists and `ForEach`

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- `ForEach` — repeat a view for each item.
- Why items need an **ID** (`Identifiable` and `id: \.self`).
- `List` — a scrolling list like the Settings or Contacts app.
- Sections, list styles.
- **Deleting**, **moving** and **swipe actions**.
- Searching with `.searchable`.
- An empty-list message.

---

## 1. `ForEach` — repeat a view

```swift
VStack {
    ForEach(1...5, id: \.self) { number in
        Text("Row \(number)")
    }
}
```

**Preview:**

```
Row 1
Row 2
Row 3
Row 4
Row 5
```

| Part | Meaning |
|---|---|
| `ForEach` | "For each item, make a view." Like a `for` loop (Chapter 12), but it **creates views**. |
| `1...5` | The items. |
| `id: \.self` | How to tell items apart (see next section). |
| `{ number in ... }` | A closure. `number` is the current item. Return a view. |

⚠️ **Careful:** You **can't** use a normal `for` loop inside `body`. Use `ForEach`.

```swift
var body: some View {
    VStack {
        for i in 1...5 { Text("\(i)") }   // ❌ ERROR
    }
}
```

### Looping over an array

```swift
let fruits = ["🍎 Apple", "🍌 Banana", "🍇 Grapes"]

VStack(alignment: .leading) {
    ForEach(fruits, id: \.self) { fruit in
        Text(fruit)
    }
}
```

---

## 2. Why does SwiftUI need an ID? 🆔

When a list changes (an item is added, removed or moved), SwiftUI must know **which** row is **which**, so it can update the right one and animate correctly.

Think of students in a class 🧑‍🎓: if two have the same name, the teacher uses their **roll number** to tell them apart.

> 📖 **New word: ID (identifier)**
> A value that is **different for every item**, so SwiftUI can tell items apart.

### Option 1: `id: \.self`

Use the item **itself** as the ID.

```swift
ForEach(fruits, id: \.self) { ... }
```

✅ Fine for simple values that are **unique**: numbers, unique strings.
⚠️ If two items are **the same** (two `"Apple"`s), SwiftUI gets confused.

> 📖 **New word: `\.self`**
> A **key path** meaning "the item itself". A key path is a way to point to a property, like `\.name`.

### Option 2: `Identifiable` ⭐ (best for your own types)

```swift
struct Friend: Identifiable {
    let id = UUID()
    let name: String
    let emoji: String
}

let friends = [
    Friend(name: "Ravi", emoji: "🧑"),
    Friend(name: "Meena", emoji: "👩"),
    Friend(name: "Arun", emoji: "👨")
]

VStack(alignment: .leading) {
    ForEach(friends) { friend in
        Text("\(friend.emoji) \(friend.name)")
    }
}
```

| Part | Meaning |
|---|---|
| `: Identifiable` | The protocol from Chapter 24. It requires an `id` property. |
| `let id = UUID()` | A **random unique ID** made automatically for each friend. |
| `ForEach(friends)` | No `id:` needed — SwiftUI uses `friend.id`. |

> 📖 **New word: UUID**
> **U**niversally **U**nique **ID**entifier. A long random code like `E621E1F8-C36C-495A-93FC-0C247A3E6E5F`. Practically never repeats.

🧠 **Remember:** For your own structs, follow `Identifiable` and add `let id = UUID()`.

---

## 3. `List` — a real list

```swift
List {
    Text("🍎 Apple")
    Text("🍌 Banana")
    Text("🍇 Grapes")
}
```

**Preview:** a scrolling list with lines between rows, like the Settings app.

### List from an array

```swift
struct ContentView: View {
    let friends = [
        Friend(name: "Ravi", emoji: "🧑"),
        Friend(name: "Meena", emoji: "👩"),
        Friend(name: "Arun", emoji: "👨"),
        Friend(name: "Priya", emoji: "👧")
    ]

    var body: some View {
        List(friends) { friend in
            HStack {
                Text(friend.emoji)
                    .font(.largeTitle)
                Text(friend.name)
                    .font(.headline)
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `List(friends) { friend in ... }` | One row per friend. Scrolls automatically if there are many. |

`List` vs `VStack + ForEach`:

| | `List` | `ScrollView + VStack + ForEach` |
|---|---|---|
| Scrolls | ✅ | ✅ (with ScrollView) |
| Lines between rows | ✅ automatic | ❌ |
| Swipe to delete | ✅ | ❌ |
| Fast with 1000s of rows | ✅ (lazy) | Use `LazyVStack` |
| Full design control | Less | More |

---

## 4. A custom row view

Keep `List` code short by making a row view:

```swift
struct FriendRow: View {
    let friend: Friend

    var body: some View {
        HStack(spacing: 12) {
            Text(friend.emoji)
                .font(.system(size: 40))
            VStack(alignment: .leading) {
                Text(friend.name)
                    .font(.headline)
                Text("Tap to say hi")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

// In ContentView:
List(friends) { friend in
    FriendRow(friend: friend)
}
```

---

## 5. Sections

```swift
List {
    Section("Fruits") {
        Text("🍎 Apple")
        Text("🍌 Banana")
    }
    Section("Vegetables") {
        Text("🥕 Carrot")
        Text("🥦 Broccoli")
    }
}
```

With data:

```swift
let fruits = ["🍎 Apple", "🍌 Banana"]
let veggies = ["🥕 Carrot", "🥦 Broccoli", "🌽 Corn"]

List {
    Section("Fruits") {
        ForEach(fruits, id: \.self) { Text($0) }
    }
    Section {
        ForEach(veggies, id: \.self) { Text($0) }
    } header: {
        Text("Vegetables")
    } footer: {
        Text("\(veggies.count) vegetables")
    }
}
```

`{ Text($0) }` — the short closure form from Chapter 19!

---

## 6. List styles

```swift
List { ... }
    .listStyle(.insetGrouped)
```

| Style | Looks like |
|---|---|
| `.automatic` | SwiftUI chooses (default). |
| `.insetGrouped` | Rounded groups with space around (like Settings). |
| `.grouped` | Groups across the full width. |
| `.plain` | Simple rows, no groups. |
| `.sidebar` | For iPad sidebars. |

---

## 7. A list that changes (with `@State`)

```swift
struct ContentView: View {
    @State private var tasks = ["Buy milk", "Do homework", "Call grandma"]
    @State private var newTask = ""

    var body: some View {
        VStack {
            HStack {
                TextField("New task", text: $newTask)
                    .textFieldStyle(.roundedBorder)
                Button("Add") {
                    tasks.append(newTask)
                    newTask = ""
                }
                .disabled(newTask.isEmpty)
            }
            .padding()

            List {
                ForEach(tasks, id: \.self) { task in
                    Text(task)
                }
            }
        }
    }
}
```

Type a task → tap **Add** → it appears in the list! ✨

---

## 8. Swipe to delete 🗑️

```swift
List {
    ForEach(tasks, id: \.self) { task in
        Text(task)
    }
    .onDelete { indexSet in
        tasks.remove(atOffsets: indexSet)
    }
}
```

| Part | Meaning |
|---|---|
| `.onDelete { ... }` | Add **swipe left to delete**. Put it on the **`ForEach`**, not the `List`. |
| `indexSet` | Which rows to delete (a set of positions). |
| `tasks.remove(atOffsets: indexSet)` | Remove them from the array. The row disappears with an animation. |

> 📖 **New word: IndexSet**
> A set of index numbers (positions), like {0, 3}.

### Move rows (reorder)

```swift
NavigationStack {
    List {
        ForEach(tasks, id: \.self) { task in
            Text(task)
        }
        .onDelete { tasks.remove(atOffsets: $0) }
        .onMove { from, to in
            tasks.move(fromOffsets: from, toOffset: to)
        }
    }
    .toolbar {
        EditButton()
    }
}
```

| Part | Meaning |
|---|---|
| `.onMove { from, to in ... }` | Allow dragging rows to a new place. |
| `EditButton()` | A built-in "Edit" / "Done" button that turns on edit mode (delete circles and drag handles). |
| `NavigationStack` and `.toolbar` | Needed to show the button at the top. Chapter 49 explains them. |

---

## 9. Custom swipe actions

```swift
List {
    ForEach(tasks, id: \.self) { task in
        Text(task)
            .swipeActions(edge: .trailing) {
                Button(role: .destructive) {
                    tasks.removeAll { $0 == task }
                } label: {
                    Label("Delete", systemImage: "trash")
                }
                Button {
                    print("Pin \(task)")
                } label: {
                    Label("Pin", systemImage: "pin")
                }
                .tint(.orange)
            }
            .swipeActions(edge: .leading) {
                Button {
                    print("Done: \(task)")
                } label: {
                    Label("Done", systemImage: "checkmark")
                }
                .tint(.green)
            }
    }
}
```

| Part | Meaning |
|---|---|
| `.swipeActions(edge: .trailing)` | Buttons that appear when you swipe **left** (from the right edge). |
| `.swipeActions(edge: .leading)` | Swipe **right**. |
| `.tint(.orange)` | Button color. |
| `tasks.removeAll { $0 == task }` | Remove matching items (a closure — Chapter 19). |

---

## 10. Searching with `.searchable` 🔍

```swift
struct ContentView: View {
    let countries = ["India", "Japan", "Kenya", "Brazil", "Canada", "France", "Indonesia"]
    @State private var searchText = ""

    var filteredCountries: [String] {
        if searchText.isEmpty {
            return countries
        }
        return countries.filter { $0.localizedCaseInsensitiveContains(searchText) }
    }

    var body: some View {
        NavigationStack {
            List(filteredCountries, id: \.self) { country in
                Text(country)
            }
            .navigationTitle("Countries")
            .searchable(text: $searchText, prompt: "Search countries")
        }
    }
}
```

| Part | Meaning |
|---|---|
| `.searchable(text: $searchText)` | Adds a search bar at the top. Bound to `searchText`. |
| `filteredCountries` | A **computed property** (Chapter 20) using `filter` (Chapter 19). |
| `localizedCaseInsensitiveContains` | "Contains, ignoring big/small letters" — `"ind"` matches `"India"`. |

Type "ind" → only India and Indonesia show. ✨

---

## 11. Empty list message

```swift
List {
    ForEach(tasks, id: \.self) { Text($0) }
}
.overlay {
    if tasks.isEmpty {
        ContentUnavailableView(
            "No tasks yet",
            systemImage: "checklist",
            description: Text("Add a task to get started.")
        )
    }
}
```

| Part | Meaning |
|---|---|
| `.overlay { }` | Put something on top of the list (Chapter 44). |
| `ContentUnavailableView` | A built-in, nice-looking "nothing here" message with an icon. |

For search with no results: `ContentUnavailableView.search(text: searchText)`.

---

## 12. Mini project: a to-do list ✅

```swift
struct TodoItem: Identifiable {
    let id = UUID()
    var title: String
    var isDone = false
}

struct ContentView: View {
    @State private var items = [
        TodoItem(title: "Learn SwiftUI lists"),
        TodoItem(title: "Drink water 💧"),
        TodoItem(title: "Go for a walk 🚶", isDone: true)
    ]
    @State private var newTitle = ""

    var remaining: Int {
        items.filter { !$0.isDone }.count
    }

    var body: some View {
        NavigationStack {
            List {
                Section {
                    HStack {
                        TextField("New to-do", text: $newTitle)
                            .onSubmit(addItem)
                        Button("Add", action: addItem)
                            .disabled(newTitle.isEmpty)
                    }
                }

                Section("\(remaining) left") {
                    ForEach($items) { $item in
                        HStack {
                            Image(systemName: item.isDone ? "checkmark.circle.fill" : "circle")
                                .foregroundStyle(item.isDone ? .green : .gray)
                                .font(.title2)
                                .onTapGesture {
                                    item.isDone.toggle()
                                }
                            Text(item.title)
                                .strikethrough(item.isDone)
                                .foregroundStyle(item.isDone ? .secondary : .primary)
                        }
                    }
                    .onDelete { items.remove(atOffsets: $0) }
                }
            }
            .navigationTitle("My To-Dos")
            .overlay {
                if items.isEmpty {
                    ContentUnavailableView("All clear! 🎉",
                                           systemImage: "checkmark.seal",
                                           description: Text("Nothing to do."))
                }
            }
        }
    }

    func addItem() {
        guard !newTitle.isEmpty else { return }
        items.append(TodoItem(title: newTitle))
        newTitle = ""
    }
}
```

The new, important part:

```swift
ForEach($items) { $item in
    ...
    item.isDone.toggle()
}
```

| Part | Meaning |
|---|---|
| `ForEach($items)` | Loop over **bindings** to each item (note the `$`). |
| `{ $item in ... }` | Each row gets a **binding** to its item, so it can **change** it. |
| `item.isDone.toggle()` | Changes the real item inside the `@State` array! ✨ |

Without the `$`, `item` would be a **copy** (Chapter 20), and changing it would do nothing.

---

## 🏋️ Practice

1. Use `ForEach` to show the numbers 1–10 in a `VStack`.
2. Make a struct `Movie: Identifiable` with `title` and `year`. Show 5 movies in a `List` with a custom row.
3. Group movies into two `Section`s: "Old" (before 2000) and "New". (Hint: `filter`.)
4. Add swipe-to-delete to a list of names in `@State`.
5. Add `.searchable` to your movie list.
6. Add a leading swipe action to the to-do app that marks an item as done.

---

## 🧠 Remember

- `ForEach(items) { item in View }` makes one view per item. No normal `for` in `body`.
- Items need an **ID**: `id: \.self` for simple unique values, or `Identifiable` with `let id = UUID()`.
- `List` = scrolling rows. Use `Section`s and `.listStyle()`.
- `.onDelete` (on `ForEach`) for swipe-to-delete. `.swipeActions` for custom swipes.
- `.searchable(text:)` + a filtered computed property = search.
- `ForEach($items) { $item in }` lets each row **change** its item.
- `ContentUnavailableView` for empty lists.

---

⬅️ **Back:** [Chapter 47 — Input Controls](47-input-controls.md)
➡️ **Next:** [Chapter 49 — Navigation](49-navigation.md)
