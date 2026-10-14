# Chapter 51 — Sheets and Alerts

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- `.sheet` — a screen that slides **up** from the bottom.
- Closing a sheet (`dismiss`).
- Half-height sheets (`presentationDetents`).
- `.sheet(item:)` — a sheet for a selected item.
- `.fullScreenCover` — covers the whole screen.
- `.alert` — a pop-up message with buttons.
- `.confirmationDialog` — a menu of choices from the bottom.

---

## 1. Navigation vs sheets vs alerts

| Type | Looks like | Use for |
|---|---|---|
| **Navigation push** (Chapter 49) | Slides in from the **right** | Going **deeper**: list → details. |
| **Sheet** | Slides **up** from the bottom, a card on top | A **separate task**: "Add new item", "Edit profile", "Settings". |
| **Full screen cover** | Slides up and covers **everything** | Tasks that need full focus: camera, login, onboarding. |
| **Alert** | A small box in the middle | An important **message** or a **yes/no** question. |
| **Confirmation dialog** | A menu from the bottom | Choosing between **actions**: "Delete photo?" |

```
  Sheet                     Alert                    Confirmation dialog
 ┌──────────────┐          ┌──────────────┐          ┌──────────────┐
 │  (main app,  │          │              │          │              │
 │   dimmed)    │          │ ┌──────────┐ │          │              │
 ├──────────────┤          │ │ Title    │ │          │              │
 │ ▬▬           │          │ │ Message  │ │          │┌────────────┐│
 │ New Item     │          │ │[No][Yes] │ │          ││  Delete 🔴  ││
 │              │          │ └──────────┘ │          ││  Archive    ││
 │ [Save]       │          │              │          │├────────────┤│
 └──────────────┘          └──────────────┘          ││  Cancel     ││
                                                     └┴────────────┴┘
```

---

## 2. Showing a sheet

```swift
struct ContentView: View {
    @State private var showSheet = false

    var body: some View {
        Button("Show sheet") {
            showSheet = true
        }
        .buttonStyle(.borderedProminent)
        .sheet(isPresented: $showSheet) {
            Text("Hello from the sheet! 👋")
                .font(.title)
        }
    }
}
```

**Try it:** Tap the button → a sheet slides up. **Swipe down** to close it. ✨

| Part | Meaning |
|---|---|
| `@State private var showSheet = false` | Is the sheet showing? Starts hidden. |
| `showSheet = true` | Show it. |
| `.sheet(isPresented: $showSheet) { ... }` | "Show this content as a sheet when `showSheet` is `true`." |
| Swipe down | SwiftUI sets `showSheet` back to `false` **automatically** (through the binding). |

🧠 **Remember:** You don't "open" a sheet directly. You change a **Bool**, and SwiftUI shows or hides the sheet. (State → screen, like Chapter 46!)

---

## 3. A sheet with its own view and a close button

```swift
struct ContentView: View {
    @State private var showSettings = false

    var body: some View {
        Button("Open settings") {
            showSettings = true
        }
        .sheet(isPresented: $showSettings) {
            SettingsSheet()
        }
    }
}

struct SettingsSheet: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Form {
                Toggle("Sounds", isOn: .constant(true))
                Toggle("Vibration", isOn: .constant(false))
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `@Environment(\.dismiss)` | Get the "close" action (Chapter 49). |
| `dismiss()` | Closes the sheet. |
| `NavigationStack` inside the sheet | Gives the sheet a title bar and toolbar. |
| `.confirmationAction` | The standard place for "Done" / "Save" (top right). |
| `.constant(true)` | A fake binding that never changes — just for this demo. (Chapter 52.) |

💡 **Tip:** Always give sheets a visible **Done** or **Cancel** button. Not everyone knows they can swipe down.

---

## 4. Half-height sheets: `presentationDetents`

```swift
.sheet(isPresented: $showSheet) {
    VStack {
        Text("I'm a small sheet!")
            .font(.title2)
    }
    .presentationDetents([.medium, .large])
    .presentationDragIndicator(.visible)
}
```

| Modifier | Meaning |
|---|---|
| `.presentationDetents([.medium, .large])` | The sheet can be **half** height or **full** height. The user drags between them. |
| `.presentationDragIndicator(.visible)` | Show the small gray handle `▬` at the top. |

Detent options:

| Detent | Height |
|---|---|
| `.medium` | About half the screen |
| `.large` | Almost full screen (default) |
| `.height(200)` | Exactly 200 points |
| `.fraction(0.3)` | 30% of the screen |

> 📖 **New word: Detent**
> A height where the sheet "stops" when dragged.

### Prevent swipe-to-close

```swift
.interactiveDismissDisabled()
```

Useful when the user has unsaved changes — they must tap Save or Cancel.

---

## 5. Sending data back from a sheet

A common pattern: **"Add item"** sheet → returns the new item to the list.

```swift
struct ContentView: View {
    @State private var names = ["Ravi", "Meena"]
    @State private var showAdd = false

    var body: some View {
        NavigationStack {
            List(names, id: \.self) { Text($0) }
                .navigationTitle("Friends")
                .toolbar {
                    Button {
                        showAdd = true
                    } label: {
                        Image(systemName: "plus")
                    }
                }
                .sheet(isPresented: $showAdd) {
                    AddFriendSheet { newName in
                        names.append(newName)
                    }
                }
        }
    }
}

struct AddFriendSheet: View {
    @Environment(\.dismiss) private var dismiss
    @State private var name = ""
    let onSave: (String) -> Void

    var body: some View {
        NavigationStack {
            Form {
                TextField("Friend's name", text: $name)
            }
            .navigationTitle("New Friend")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        onSave(name)
                        dismiss()
                    }
                    .disabled(name.isEmpty)
                }
            }
        }
        .presentationDetents([.medium])
    }
}
```

| Part | Meaning |
|---|---|
| `let onSave: (String) -> Void` | The sheet receives a **closure** (Chapter 19) to call when saving. |
| `AddFriendSheet { newName in names.append(newName) }` | A **trailing closure**: "When you save, add the name to my list." |
| `onSave(name)` | Call the closure with the typed name. |

🧠 **Remember:** To send data **back** from a sheet, pass a **closure** (or a binding — Chapter 52).

---

## 6. `.sheet(item:)` — a sheet for a selected item

When a sheet shows details about **one item**, use `item:` instead of a Bool:

```swift
struct Planet: Identifiable {
    let id = UUID()
    let name: String
    let emoji: String
}

struct ContentView: View {
    let planets = [
        Planet(name: "Earth", emoji: "🌍"),
        Planet(name: "Mars", emoji: "🔴"),
        Planet(name: "Saturn", emoji: "🪐")
    ]
    @State private var selectedPlanet: Planet?

    var body: some View {
        List(planets) { planet in
            Button("\(planet.emoji) \(planet.name)") {
                selectedPlanet = planet
            }
        }
        .sheet(item: $selectedPlanet) { planet in
            VStack(spacing: 20) {
                Text(planet.emoji).font(.system(size: 120))
                Text(planet.name).font(.largeTitle.bold())
            }
            .presentationDetents([.medium])
        }
    }
}
```

| Part | Meaning |
|---|---|
| `@State private var selectedPlanet: Planet?` | An **Optional** (Chapter 17). `nil` = no sheet. |
| `selectedPlanet = planet` | Setting a value **shows** the sheet. |
| `.sheet(item: $selectedPlanet) { planet in ... }` | The sheet gets the **unwrapped** planet. |
| When closed | SwiftUI sets `selectedPlanet` back to `nil`. |

The item must be `Identifiable`.

---

## 7. `.fullScreenCover`

Same as `.sheet`, but covers **everything** and **can't** be swiped down:

```swift
struct ContentView: View {
    @State private var showWelcome = false

    var body: some View {
        Button("Show welcome") { showWelcome = true }
            .fullScreenCover(isPresented: $showWelcome) {
                WelcomeView()
            }
    }
}

struct WelcomeView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        ZStack {
            Color.indigo.ignoresSafeArea()
            VStack(spacing: 30) {
                Text("Welcome! 🎉")
                    .font(.largeTitle.bold())
                    .foregroundStyle(.white)
                Button("Get started") { dismiss() }
                    .buttonStyle(.borderedProminent)
                    .tint(.white)
                    .foregroundStyle(.indigo)
            }
        }
    }
}
```

⚠️ **Careful:** A full screen cover **must** have a button that calls `dismiss()`, or the user is stuck! 😱

---

## 8. Alerts ⚠️

```swift
struct ContentView: View {
    @State private var showAlert = false

    var body: some View {
        Button("Show alert") {
            showAlert = true
        }
        .alert("Hello!", isPresented: $showAlert) {
            Button("OK") { }
        } message: {
            Text("This is an alert message.")
        }
    }
}
```

| Part | Meaning |
|---|---|
| `.alert("Hello!", isPresented: $showAlert)` | Title and the Bool that controls it. |
| `{ Button("OK") { } }` | The buttons. Any button **closes** the alert automatically. |
| `message: { Text(...) }` | Optional smaller text under the title. |

### Yes / No alert with roles

```swift
struct ContentView: View {
    @State private var showDeleteAlert = false
    @State private var photos = 12

    var body: some View {
        VStack(spacing: 20) {
            Text("📷 \(photos) photos")
                .font(.title)
            Button("Delete all", role: .destructive) {
                showDeleteAlert = true
            }
        }
        .alert("Delete all photos?", isPresented: $showDeleteAlert) {
            Button("Delete", role: .destructive) {
                photos = 0
            }
            Button("Cancel", role: .cancel) { }
        } message: {
            Text("This can't be undone.")
        }
    }
}
```

| Button role | Look |
|---|---|
| `.destructive` | **Red** text. |
| `.cancel` | Placed in the standard "cancel" position, often bold. |

🧠 **Remember:** Ask for confirmation before **destructive** actions (deleting, logging out).

### Alert with a text field

```swift
@State private var showRename = false
@State private var newName = ""

.alert("Rename", isPresented: $showRename) {
    TextField("New name", text: $newName)
    Button("Save") { print("Renamed to \(newName)") }
    Button("Cancel", role: .cancel) { }
}
```

### Showing an error

```swift
@State private var errorMessage: String?

var showError: Binding<Bool> {
    Binding(
        get: { errorMessage != nil },
        set: { if !$0 { errorMessage = nil } }
    )
}

// ...
.alert("Something went wrong", isPresented: showError) {
    Button("OK") { }
} message: {
    Text(errorMessage ?? "")
}
```

| Part | Meaning |
|---|---|
| `Binding(get:set:)` | Make a custom binding: "showing" = "there is an error message". |
| `errorMessage = "No internet"` | Setting a message shows the alert. |

💡 **Tip:** Combine this with error handling (Chapter 26): in `catch`, set `errorMessage = error.localizedDescription`.

---

## 9. Confirmation dialog

A list of **actions** sliding up from the bottom:

```swift
struct ContentView: View {
    @State private var showOptions = false

    var body: some View {
        Button("Photo options") {
            showOptions = true
        }
        .confirmationDialog("What do you want to do?",
                            isPresented: $showOptions,
                            titleVisibility: .visible) {
            Button("Share") { print("Share") }
            Button("Save to Files") { print("Save") }
            Button("Delete", role: .destructive) { print("Delete") }
            Button("Cancel", role: .cancel) { }
        }
    }
}
```

| | Alert | Confirmation dialog |
|---|---|---|
| Position | Middle | Bottom (iPhone) |
| Best for | A message, or yes/no | Choosing between **several actions** |

---

## 10. Mini project: a notes app with sheets and alerts 📝

```swift
struct Note: Identifiable {
    let id = UUID()
    var title: String
    var body: String
}

struct ContentView: View {
    @State private var notes = [
        Note(title: "Shopping", body: "Milk, bread, eggs"),
        Note(title: "Idea 💡", body: "An app for tracking water")
    ]
    @State private var showNewNote = false
    @State private var selectedNote: Note?
    @State private var noteToDelete: Note?

    var body: some View {
        NavigationStack {
            List {
                ForEach(notes) { note in
                    Button {
                        selectedNote = note
                    } label: {
                        VStack(alignment: .leading) {
                            Text(note.title).font(.headline)
                            Text(note.body)
                                .font(.subheadline)
                                .foregroundStyle(.secondary)
                                .lineLimit(1)
                        }
                    }
                    .foregroundStyle(.primary)
                    .swipeActions {
                        Button("Delete", role: .destructive) {
                            noteToDelete = note
                        }
                    }
                }
            }
            .navigationTitle("Notes")
            .toolbar {
                Button {
                    showNewNote = true
                } label: {
                    Image(systemName: "square.and.pencil")
                }
            }
            .sheet(isPresented: $showNewNote) {
                NewNoteSheet { note in
                    notes.append(note)
                }
            }
            .sheet(item: $selectedNote) { note in
                NavigationStack {
                    ScrollView {
                        Text(note.body)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding()
                    }
                    .navigationTitle(note.title)
                }
                .presentationDetents([.medium, .large])
            }
            .alert("Delete note?",
                   isPresented: Binding(
                       get: { noteToDelete != nil },
                       set: { if !$0 { noteToDelete = nil } }
                   )) {
                Button("Delete", role: .destructive) {
                    notes.removeAll { $0.id == noteToDelete?.id }
                }
                Button("Cancel", role: .cancel) { }
            } message: {
                Text("\"\(noteToDelete?.title ?? "")\" will be removed.")
            }
        }
    }
}

struct NewNoteSheet: View {
    @Environment(\.dismiss) private var dismiss
    @State private var title = ""
    @State private var text = ""
    let onSave: (Note) -> Void

    var body: some View {
        NavigationStack {
            Form {
                TextField("Title", text: $title)
                TextField("Write your note...", text: $text, axis: .vertical)
                    .lineLimit(5...10)
            }
            .navigationTitle("New Note")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        onSave(Note(title: title, body: text))
                        dismiss()
                    }
                    .disabled(title.isEmpty)
                }
            }
        }
    }
}
```

| Feature | How |
|---|---|
| New note | `+` button → `.sheet(isPresented:)` → closure sends the note back. |
| Read a note | Tap → `selectedNote = note` → `.sheet(item:)`. |
| Delete | Swipe → `noteToDelete = note` → alert asks first → delete. |

---

## 🏋️ Practice

1. Make a button that opens a sheet with your name and a "Close" button.
2. Make the sheet half-height with a drag indicator.
3. Make an "Add fruit" sheet that sends a new fruit name back to a list.
4. Make a list of countries. Tap one → `.sheet(item:)` shows its flag big.
5. Make a "Log out" button that shows an alert with "Log out" (destructive) and "Cancel".
6. Make a confirmation dialog with 3 actions: "Copy", "Share", "Delete".

---

## 🧠 Remember

- Sheets, covers and alerts are controlled by **state**: a `Bool` or an Optional item.
- `.sheet(isPresented: $bool) { View }` — slides up. `dismiss()` closes it.
- `.presentationDetents([.medium, .large])` — half-height sheets.
- `.sheet(item: $optionalItem) { item in View }` — sheet for a chosen item.
- `.fullScreenCover` — covers everything; must have a close button.
- `.alert("Title", isPresented:) { buttons } message: { Text }` — use `role: .destructive` / `.cancel`.
- `.confirmationDialog` — several actions from the bottom.
- Send data back from a sheet with a **closure**.

---

⬅️ **Back:** [Chapter 50 — Tabs](50-tabs.md)
➡️ **Next:** [Chapter 52 — `@Binding`](52-binding.md)
