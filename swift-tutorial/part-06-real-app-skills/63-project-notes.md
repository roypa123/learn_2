# Chapter 63 — Project: Notes App 📝

🍎 **Needs a Mac** (iOS 17 or newer — uses SwiftData)

---

## What you will build

A **Notes app** saved with **SwiftData** (Chapter 57):

- 📝 Create, edit and delete notes — changes save **automatically**
- 📌 Pin important notes to the top
- 🎨 Give each note a color
- 📁 Folders (a **relationship** between models)
- 🔍 Search notes by title and text
- ↕️ Sort by date or title
- 📊 Word and character count

```
 ┌───────────────────────────────┐
 │ < Folders      All Notes   ⋯ ✎│
 │ 🔍 Search                     │
 │ PINNED                        │
 │ 📌 Shopping list         🟡   │
 │    Milk, eggs, bread...       │
 │ NOTES                         │
 │ Ideas for my app         🟣   │
 │    A weather app with...      │
 │ Holiday plan             🟢   │
 │    Goa in December...         │
 └───────────────────────────────┘
```

Skills used: SwiftData (`@Model`, `@Query`, `modelContext`, relationships, `#Predicate`) (Ch 57), `@Bindable` (Ch 53), navigation (Ch 49), search (Ch 48), focus (Ch 47), enums and Codable (Ch 23, 59).

---

## Step 0: Create the project

1. New project: `QuickNotes`, Interface **SwiftUI**, Storage: **None** (we'll add SwiftData by hand so you understand every line).
2. Files:

```
QuickNotes/
 ├─ QuickNotesApp.swift
 ├─ Models/
 │   ├─ Note.swift
 │   └─ Folder.swift
 └─ Views/
     ├─ FolderListView.swift
     ├─ NoteListView.swift
     ├─ NoteRow.swift
     └─ NoteEditorView.swift
```

---

## Step 1: Note color — part of `Note.swift`

```swift
import SwiftUI
import SwiftData

enum NoteColor: String, Codable, CaseIterable, Identifiable {
    case none, yellow, green, blue, purple, pink

    var id: Self { self }

    var color: Color {
        switch self {
        case .none: .clear
        case .yellow: .yellow
        case .green: .green
        case .blue: .blue
        case .purple: .purple
        case .pink: .pink
        }
    }
}
```

| Part | Meaning |
|---|---|
| `String, Codable` | SwiftData can save **Codable enums** (Ch 57). |
| `case none` | "No color" option. |

---

## Step 2: The models — `Note.swift` and `Folder.swift`

```swift
// Note.swift (continued)

@Model
class Note {
    var title: String
    var body: String
    var isPinned: Bool
    var colorTag: NoteColor
    var createdAt: Date
    var updatedAt: Date
    var folder: Folder?

    init(title: String = "",
         body: String = "",
         isPinned: Bool = false,
         colorTag: NoteColor = .none,
         folder: Folder? = nil) {
        self.title = title
        self.body = body
        self.isPinned = isPinned
        self.colorTag = colorTag
        self.createdAt = .now
        self.updatedAt = .now
        self.folder = folder
    }

    var displayTitle: String {
        title.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty ? "New Note" : title
    }

    var preview: String {
        let text = body.trimmingCharacters(in: .whitespacesAndNewlines)
        return text.isEmpty ? "No additional text" : text
    }

    var wordCount: Int {
        body.split { $0.isWhitespace || $0.isNewline }.count
    }
}
```

```swift
// Folder.swift
import Foundation
import SwiftData

@Model
class Folder {
    var name: String
    var icon: String
    var createdAt: Date

    @Relationship(deleteRule: .cascade, inverse: \Note.folder)
    var notes: [Note] = []

    init(name: String, icon: String = "folder") {
        self.name = name
        self.icon = icon
        self.createdAt = .now
    }
}
```

| Part | Meaning |
|---|---|
| `@Model class Note` | A savable note (Ch 57). |
| `var folder: Folder?` | Each note is in **one** folder — or none. |
| `var notes: [Note]` in `Folder` | A folder has **many** notes. |
| `@Relationship(deleteRule: .cascade, inverse: \Note.folder)` | Delete a folder → delete its notes. The two sides stay connected (Ch 57). |
| `displayTitle`, `preview`, `wordCount` | Computed properties — **not** saved, calculated when needed. |
| `body.split { $0.isWhitespace || $0.isNewline }` | Cut the text at spaces and new lines → count the words. |

```
   Folder "Work" 📁
     ├── Note "Meeting notes"
     ├── Note "Ideas"
     └── Note "To ask boss"

   Folder "Personal" 📁
     └── Note "Holiday plan"

   (No folder)
     └── Note "Random thought"
```

---

## Step 3: Set up the container — `QuickNotesApp.swift`

```swift
import SwiftUI
import SwiftData

@main
struct QuickNotesApp: App {
    var body: some Scene {
        WindowGroup {
            FolderListView()
        }
        .modelContainer(for: [Note.self, Folder.self])
    }
}
```

Both models are registered (Ch 57).

---

## Step 4: Sample data for previews

Add this to the bottom of `Folder.swift`:

```swift
@MainActor
enum PreviewData {
    static let container: ModelContainer = {
        let config = ModelConfiguration(isStoredInMemoryOnly: true)
        let container = try! ModelContainer(for: Note.self, Folder.self, configurations: config)

        let work = Folder(name: "Work", icon: "briefcase")
        let personal = Folder(name: "Personal", icon: "house")
        container.mainContext.insert(work)
        container.mainContext.insert(personal)

        let notes = [
            Note(title: "Shopping list", body: "Milk, eggs, bread, mangoes 🥭", isPinned: true, colorTag: .yellow, folder: personal),
            Note(title: "App idea", body: "A weather app with beautiful gradients.", colorTag: .purple, folder: work),
            Note(title: "Meeting notes", body: "Discuss the new design on Friday.", folder: work),
            Note(title: "Holiday plan", body: "Goa in December. Book tickets early!", colorTag: .green)
        ]
        for note in notes {
            container.mainContext.insert(note)
        }
        return container
    }()
}
```

| Part | Meaning |
|---|---|
| `enum PreviewData` | A place for preview helpers (an enum with no cases — Ch 54 `Theme`). |
| `static let container: ModelContainer = { ... }()` | A **closure that runs once** to build the value. The `()` at the end **calls** it. |
| `isStoredInMemoryOnly: true` | Not saved to disk — perfect for previews (Ch 57). |

---

## Step 5: The folders screen — `FolderListView.swift`

```swift
import SwiftUI
import SwiftData

struct FolderListView: View {
    @Environment(\.modelContext) private var modelContext
    @Query(sort: \Folder.createdAt) private var folders: [Folder]
    @Query private var allNotes: [Note]

    @State private var showNewFolder = false
    @State private var newFolderName = ""

    var body: some View {
        NavigationStack {
            List {
                Section {
                    NavigationLink {
                        NoteListView(folder: nil)
                    } label: {
                        folderLabel(name: "All Notes", icon: "tray.full", count: allNotes.count)
                    }
                }

                Section("My Folders") {
                    ForEach(folders) { folder in
                        NavigationLink {
                            NoteListView(folder: folder)
                        } label: {
                            folderLabel(name: folder.name, icon: folder.icon, count: folder.notes.count)
                        }
                    }
                    .onDelete { offsets in
                        for index in offsets {
                            modelContext.delete(folders[index])
                        }
                    }
                }
            }
            .navigationTitle("Folders")
            .toolbar {
                ToolbarItem(placement: .bottomBar) {
                    Button("New Folder", systemImage: "folder.badge.plus") {
                        showNewFolder = true
                    }
                }
            }
            .alert("New Folder", isPresented: $showNewFolder) {
                TextField("Name", text: $newFolderName)
                Button("Create") {
                    let name = newFolderName.trimmingCharacters(in: .whitespaces)
                    if !name.isEmpty {
                        modelContext.insert(Folder(name: name))
                    }
                    newFolderName = ""
                }
                Button("Cancel", role: .cancel) { newFolderName = "" }
            } message: {
                Text("Enter a name for this folder.")
            }
        }
    }

    private func folderLabel(name: String, icon: String, count: Int) -> some View {
        HStack {
            Label(name, systemImage: icon)
            Spacer()
            Text("\(count)")
                .foregroundStyle(.secondary)
        }
    }
}

#Preview {
    FolderListView()
        .modelContainer(PreviewData.container)
}
```

| Part | Meaning |
|---|---|
| `NoteListView(folder: nil)` | `nil` = show **all** notes. |
| `folder.notes.count` | The relationship gives us the folder's notes for free! |
| `.onDelete` | Deleting a folder **also deletes its notes** (cascade). ⚠️ |
| `.alert` with a `TextField` | A quick way to ask for a name (Ch 51). |
| `.bottomBar` | A toolbar at the bottom, like Apple's Notes app. |

---

## Step 6: One note row — `NoteRow.swift`

```swift
import SwiftUI

struct NoteRow: View {
    let note: Note

    var body: some View {
        HStack(alignment: .top, spacing: 10) {
            if note.colorTag != .none {
                RoundedRectangle(cornerRadius: 2)
                    .fill(note.colorTag.color)
                    .frame(width: 4)
            }

            VStack(alignment: .leading, spacing: 4) {
                HStack {
                    if note.isPinned {
                        Image(systemName: "pin.fill")
                            .font(.caption)
                            .foregroundStyle(.orange)
                    }
                    Text(note.displayTitle)
                        .font(.headline)
                        .lineLimit(1)
                }
                HStack(spacing: 6) {
                    Text(note.updatedAt, format: .dateTime.day().month(.abbreviated))
                        .foregroundStyle(.secondary)
                    Text(note.preview)
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                }
                .font(.subheadline)

                if let folder = note.folder {
                    Label(folder.name, systemImage: "folder")
                        .font(.caption2)
                        .foregroundStyle(.tertiary)
                }
            }
        }
        .padding(.vertical, 2)
    }
}
```

| Part | Meaning |
|---|---|
| Colored bar | A thin colored strip on the left if the note has a color. |
| `Text(date, format: .dateTime.day().month(.abbreviated))` | Shows "14 Oct" in the user's language. |
| `.foregroundStyle(.tertiary)` | A very soft color (Ch 54). |

---

## Step 7: The notes list — `NoteListView.swift`

This list needs **dynamic** search and sort, so we use the "child view with a custom `@Query` init" pattern from Chapter 57.

First, an important warning. You might think of creating a new note like this:

```swift
// ❌ DON'T do this
NavigationLink(value: Note(folder: folder)) {
    Image(systemName: "square.and.pencil")
}
```

⚠️ This creates a new `Note` **every time `body` runs** — and `body` runs often! Instead, create the note in a **button action**, which only runs when tapped.

Here is `NoteListView` (with a small `NoteSort` enum for the sort menu):

```swift
import SwiftUI
import SwiftData

enum NoteSort: String, CaseIterable, Identifiable {
    case updated = "Date Edited"
    case created = "Date Created"
    case title = "Title"
    var id: Self { self }
}
```


```swift
struct NoteListView: View {
    let folder: Folder?

    @Environment(\.modelContext) private var modelContext
    @State private var searchText = ""
    @AppStorage("noteSort") private var sort: NoteSort = .updated
    @State private var newNote: Note?

    var body: some View {
        FilteredNotes(folder: folder, searchText: searchText, sort: sort)
            .navigationTitle(folder?.name ?? "All Notes")
            .searchable(text: $searchText, prompt: "Search notes")
            .navigationDestination(for: Note.self) { note in
                NoteEditorView(note: note)
            }
            .navigationDestination(item: $newNote) { note in
                NoteEditorView(note: note, isNew: true)
            }
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Menu {
                        Picker("Sort by", selection: $sort) {
                            ForEach(NoteSort.allCases) { option in
                                Text(option.rawValue).tag(option)
                            }
                        }
                    } label: {
                        Image(systemName: "arrow.up.arrow.down.circle")
                    }
                }
                ToolbarItem(placement: .bottomBar) {
                    Button("New Note", systemImage: "square.and.pencil") {
                        let note = Note(folder: folder)
                        modelContext.insert(note)
                        newNote = note
                    }
                }
            }
    }
}
```

| Part | Meaning |
|---|---|
| `@State private var newNote: Note?` | The note we just created (Optional). |
| Button → `insert` → `newNote = note` | Create **once**, only when tapped. ✅ |
| `.navigationDestination(item: $newNote)` | When `newNote` gets a value, **push** the editor. When you go back, it becomes `nil` again. |
| `@AppStorage("noteSort")` | The sort choice is remembered (enum with raw value — Ch 56). |

💡 **Lesson:** Code inside `body` can run **many times**. Never create data there — create it in **actions** (buttons, `.task`, etc.).

### The filtered list (dynamic `@Query`)

Add this to the same file:

```swift
struct FilteredNotes: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var notes: [Note]
    private let searchText: String

    init(folder: Folder?, searchText: String, sort: NoteSort) {
        self.searchText = searchText

        let sortDescriptors: [SortDescriptor<Note>] = switch sort {
        case .updated: [SortDescriptor(\Note.updatedAt, order: .reverse)]
        case .created: [SortDescriptor(\Note.createdAt, order: .reverse)]
        case .title: [SortDescriptor(\Note.title)]
        }

        if let folderID = folder?.persistentModelID {
            _notes = Query(filter: #Predicate<Note> { note in
                note.folder?.persistentModelID == folderID
            }, sort: sortDescriptors)
        } else {
            _notes = Query(sort: sortDescriptors)
        }
    }

    private var visibleNotes: [Note] {
        guard !searchText.isEmpty else { return notes }
        return notes.filter {
            $0.title.localizedCaseInsensitiveContains(searchText) ||
            $0.body.localizedCaseInsensitiveContains(searchText)
        }
    }

    private var pinned: [Note] { visibleNotes.filter(\.isPinned) }
    private var others: [Note] { visibleNotes.filter { !$0.isPinned } }

    var body: some View {
        List {
            if !pinned.isEmpty {
                Section("Pinned") {
                    rows(for: pinned)
                }
            }
            Section(pinned.isEmpty ? "" : "Notes") {
                rows(for: others)
            }
        }
        .overlay {
            if visibleNotes.isEmpty {
                if searchText.isEmpty {
                    ContentUnavailableView("No Notes",
                                           systemImage: "note.text",
                                           description: Text("Tap ✎ to write your first note."))
                } else {
                    ContentUnavailableView.search(text: searchText)
                }
            }
        }
    }

    private func rows(for notes: [Note]) -> some View {
        ForEach(notes) { note in
            NavigationLink(value: note) {
                NoteRow(note: note)
            }
            .swipeActions(edge: .leading) {
                Button {
                    withAnimation { note.isPinned.toggle() }
                } label: {
                    Label(note.isPinned ? "Unpin" : "Pin",
                          systemImage: note.isPinned ? "pin.slash" : "pin")
                }
                .tint(.orange)
            }
            .swipeActions(edge: .trailing) {
                Button(role: .destructive) {
                    withAnimation { modelContext.delete(note) }
                } label: {
                    Label("Delete", systemImage: "trash")
                }
            }
        }
    }
}

#Preview {
    NavigationStack {
        NoteListView(folder: nil)
    }
    .modelContainer(PreviewData.container)
}
```

Important parts:

| Part | Meaning |
|---|---|
| `let sortDescriptors ... = switch sort { ... }` | A `switch` that **gives a value** (Ch 11). |
| `folder?.persistentModelID` | Every saved model has a unique database ID. We compare IDs in the predicate. |
| `#Predicate { note.folder?.persistentModelID == folderID }` | Only notes in **this** folder (Ch 57). |
| Search in Swift (`visibleNotes`) | We filter by search **after** loading — simple and reliable for a notes app. |
| `filter(\.isPinned)` | Key path as a closure (Ch 57). |
| Pin swipe | Changes `note.isPinned` → saved automatically → the list moves it to "Pinned". ✨ |

⚠️ **Careful:** Predicates with relationships can be picky between iOS versions. If the folder filter gives an error, an easy fix is to load all notes with `Query(sort:)` and filter in Swift: `notes.filter { $0.folder == folder }`.

---

## Step 8: The editor — `NoteEditorView.swift`

```swift
import SwiftUI
import SwiftData

struct NoteEditorView: View {
    @Bindable var note: Note
    var isNew: Bool = false

    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss
    @Query(sort: \Folder.name) private var folders: [Folder]
    @FocusState private var focusedField: Field?

    enum Field { case title, body }

    var body: some View {
        VStack(spacing: 0) {
            TextField("Title", text: $note.title, axis: .vertical)
                .font(.title.bold())
                .focused($focusedField, equals: .title)
                .submitLabel(.next)
                .onSubmit { focusedField = .body }
                .padding(.horizontal)
                .padding(.top, 8)

            Text(note.updatedAt.formatted(date: .long, time: .shortened))
                .font(.caption)
                .foregroundStyle(.secondary)
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(.horizontal)
                .padding(.vertical, 4)

            TextEditor(text: $note.body)
                .focused($focusedField, equals: .body)
                .padding(.horizontal, 12)
                .scrollContentBackground(.hidden)

            HStack {
                Text("\(note.wordCount) words • \(note.body.count) characters")
                Spacer()
            }
            .font(.caption)
            .foregroundStyle(.secondary)
            .padding()
        }
        .background(note.colorTag.color.opacity(0.08))
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                Menu {
                    Toggle(isOn: $note.isPinned) {
                        Label("Pin note", systemImage: "pin")
                    }

                    Picker(selection: $note.colorTag) {
                        ForEach(NoteColor.allCases) { c in
                            Label(c.rawValue.capitalized,
                                  systemImage: c == .none ? "circle.slash" : "circle.fill")
                                .tint(c.color)
                                .tag(c)
                        }
                    } label: {
                        Label("Color", systemImage: "paintpalette")
                    }

                    Picker(selection: $note.folder) {
                        Text("No folder").tag(Folder?.none)
                        ForEach(folders) { folder in
                            Text(folder.name).tag(Optional(folder))
                        }
                    } label: {
                        Label("Folder", systemImage: "folder")
                    }

                    Divider()

                    ShareLink(item: "\(note.displayTitle)\n\n\(note.body)") {
                        Label("Share", systemImage: "square.and.arrow.up")
                    }

                    Button("Delete", systemImage: "trash", role: .destructive) {
                        modelContext.delete(note)
                        dismiss()
                    }
                } label: {
                    Image(systemName: "ellipsis.circle")
                }
            }
            ToolbarItem(placement: .keyboard) {
                HStack {
                    Spacer()
                    Button("Done") { focusedField = nil }
                }
            }
        }
        .onAppear {
            if isNew { focusedField = .title }
        }
        .onChange(of: note.title) { note.updatedAt = .now }
        .onChange(of: note.body) { note.updatedAt = .now }
        .onDisappear {
            deleteIfEmpty()
        }
    }

    private func deleteIfEmpty() {
        let isEmpty = note.title.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty &&
                      note.body.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
        if isEmpty {
            modelContext.delete(note)
        }
    }
}

#Preview {
    NavigationStack {
        NoteEditorView(note: Note(title: "Hello", body: "This is a preview note."))
    }
    .modelContainer(PreviewData.container)
}
```

Important parts:

| Part | Meaning |
|---|---|
| `@Bindable var note: Note` | Edit the SwiftData model **directly** — every keystroke is saved automatically (Ch 57). No Save button! |
| `@FocusState private var focusedField: Field?` | Track **which** field is active, using an enum (Ch 47). |
| `.focused($focusedField, equals: .title)` | This field is "focused" when `focusedField == .title`. |
| `.onSubmit { focusedField = .body }` | Press return in the title → jump to the body. |
| `.scrollContentBackground(.hidden)` | Remove the TextEditor's own background so our color shows. |
| `Picker(selection: $note.folder)` with `.tag(Folder?.none)` / `.tag(Optional(folder))` | Picking an **Optional** value: tags must be the **same Optional type** as the selection. |
| `ShareLink(item:)` | The system **share sheet** — send the note by message, mail, etc. 📤 |
| `ToolbarItem(placement: .keyboard)` | A "Done" button **above the keyboard**. |
| `.onChange { note.updatedAt = .now }` | Remember when the note was last edited. |
| `.onDisappear { deleteIfEmpty() }` | Leaving an **empty** new note deletes it — no clutter! (Apple Notes does this too.) |

> 📖 **New word: ShareLink**
> A SwiftUI view that opens the iOS **share sheet** for text, URLs, images and more.

---

## Step 9: Run and test! 🧪

| Test | Expected |
|---|---|
| Create a folder "Work" | It appears under My Folders with `0`. |
| Open Work → ✎ | A new empty note opens; the cursor is in the title. |
| Type a title, press return, type text | Saved automatically. Word count updates. |
| Go back | The note appears in Work. The count is `1`. |
| ✎ then go back without typing | The empty note is deleted. ✅ |
| Swipe right on a note → Pin | It moves to "Pinned". |
| ⋯ → Color → Purple | A purple strip in the list, light purple background in the editor. |
| ⋯ → Folder → change | The note moves to another folder. |
| Search "goa" | Finds notes by title **or** text. |
| Sort → Title | A–Z. The choice is remembered. |
| Stop and re-run | Everything is still there. 💾 |
| Delete the Work folder | Its notes are deleted too (cascade). |

---

## 🏆 Challenges

1. **Trash:** instead of deleting, set `isDeleted = true` and show a "Recently Deleted" folder.
2. **Checklists:** if a line starts with `- [ ]`, show it as a tappable checkbox in a preview mode.
3. **Folder icons:** let users pick an SF Symbol for each folder.
4. **Lock notes:** use **Face ID** (LocalAuthentication framework) to open locked notes (needs the Face ID privacy key — Ch 37).
5. **Grid view:** add a toggle to show notes as colored cards in a `LazyVGrid` (Ch 43).
6. **iCloud sync:** with a paid developer account, SwiftData can sync through iCloud (Ch 38 capabilities).

---

## 🧠 What you practiced

- SwiftData with **two models** and a **relationship** (one folder → many notes, cascade delete).
- **Dynamic queries** built in an `init` (folder filter + sort), plus search in Swift.
- Editing models **live** with `@Bindable` — auto-save, no Save button.
- `@FocusState` with an enum to move between fields; a keyboard toolbar.
- Optional pickers, menus, `ShareLink`, swipe actions.
- An important lesson: **never create data inside `body`**.

---

⬅️ **Back:** [Chapter 62 — Project: Weather App](62-project-weather.md)
➡️ **Next:** [Chapter 64 — Testing Your App](64-testing.md)
