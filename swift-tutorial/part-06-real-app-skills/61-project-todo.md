# Chapter 61 — Project: To-Do List App ✅

🍎 **Needs a Mac**

---

## What you will build

A complete **To-Do app** with:

- ✅ Add, complete, edit and delete tasks
- 🎯 Priorities (low, medium, high) with colors
- 📅 Optional due dates — overdue tasks turn red
- 🔍 Search and filter (All / Active / Done)
- 💾 **Saving to a file** with `Codable` + `FileManager` (so you learn a third way to save!)
- 🎉 Animations and a nice empty state

Skills used: structs, enums, `Codable` (Ch 59), `@Observable` (Ch 53), lists (Ch 48), navigation (Ch 49), sheets (Ch 51), forms (Ch 47), animations (Ch 55).

```
 ┌─────────────────────────────┐
 │ My Tasks                 +  │
 │ 🔍 Search                   │
 │ [ All | Active | Done ]     │
 │ ─────────────────────────── │
 │ ○ Buy milk          🔴 High │
 │   📅 Today                  │
 │ ○ Read chapter 61   🟠 Med  │
 │ ✓ Drink water       🟢 Low  │
 │ ─────────────────────────── │
 │ 2 tasks left                │
 └─────────────────────────────┘
```

---

## Step 0: Create the project

1. **File → New → Project → iOS → App**.
2. Product Name: `TaskMaster`. Interface: **SwiftUI**. Storage: **None** (we'll save files ourselves).
3. Create these **files** (File → New → File → Swift File / SwiftUI View):

```
TaskMaster/
 ├─ TaskMasterApp.swift     (already exists)
 ├─ Models/
 │   ├─ TodoTask.swift
 │   └─ TaskStore.swift
 └─ Views/
     ├─ ContentView.swift   (already exists — move it here)
     ├─ TaskRow.swift
     └─ TaskEditor.swift
```

💡 **Tip:** Make folders with right-click → **New Group** (Chapter 32). Organized projects are easier to work with.

---

## Step 1: The model — `TodoTask.swift`

```swift
import SwiftUI

enum Priority: Int, Codable, CaseIterable, Identifiable {
    case low = 0
    case medium = 1
    case high = 2

    var id: Self { self }

    var title: String {
        switch self {
        case .low: "Low"
        case .medium: "Medium"
        case .high: "High"
        }
    }

    var color: Color {
        switch self {
        case .low: .green
        case .medium: .orange
        case .high: .red
        }
    }
}

struct TodoTask: Identifiable, Codable, Equatable {
    var id = UUID()
    var title: String
    var notes: String = ""
    var isDone: Bool = false
    var priority: Priority = .medium
    var dueDate: Date? = nil
    var createdAt: Date = .now

    var isOverdue: Bool {
        guard let dueDate, !isDone else { return false }
        return dueDate < Calendar.current.startOfDay(for: .now)
    }
}
```

Let's explain:

| Part | Meaning |
|---|---|
| `enum Priority: Int, Codable, CaseIterable, Identifiable` | An enum (Ch 23) that can be saved (Codable), listed (CaseIterable), and used in pickers (Identifiable). |
| `case low = 0` … | `Int` raw values — so we can **sort** by priority. |
| `var color: Color` | Each priority has a color. |
| `struct TodoTask: Identifiable, Codable, Equatable` | One task. Identifiable for lists, Codable for saving, Equatable for comparing. |
| `var id = UUID()` | A unique ID (Ch 48). `var` (not `let`) so `Codable` can **load** it from the file. |
| `var dueDate: Date? = nil` | Optional: not every task has a due date. |
| `isOverdue` | A computed property: due **before today** and **not done**. |
| `guard let dueDate, !isDone else { return false }` | If there's no due date, or it's done → not overdue. |
| `Calendar.current.startOfDay(for: .now)` | Today at 00:00 — so a task due **today** is not overdue yet. |

> 📖 **New word: Calendar**
> A Foundation type for date math: start of day, adding days, comparing dates.

---

## Step 2: The store — `TaskStore.swift`

This class **holds** all tasks, **changes** them, and **saves** them to a file.

```swift
import SwiftUI

enum TaskFilter: String, CaseIterable, Identifiable {
    case all = "All"
    case active = "Active"
    case done = "Done"
    var id: Self { self }
}

@MainActor
@Observable
class TaskStore {
    var tasks: [TodoTask] = [] {
        didSet { save() }
    }

    private let fileURL: URL = URL.documentsDirectory.appending(path: "tasks.json")

    init() {
        load()
    }

    // MARK: - Reading

    func filtered(by filter: TaskFilter, search: String) -> [TodoTask] {
        tasks
            .filter { task in
                switch filter {
                case .all: true
                case .active: !task.isDone
                case .done: task.isDone
                }
            }
            .filter { search.isEmpty || $0.title.localizedCaseInsensitiveContains(search) }
            .sorted { a, b in
                if a.isDone != b.isDone { return !a.isDone }          // active first
                if a.priority != b.priority { return a.priority.rawValue > b.priority.rawValue }  // high first
                return a.createdAt > b.createdAt                     // newest first
            }
    }

    var remainingCount: Int {
        tasks.filter { !$0.isDone }.count
    }

    // MARK: - Changing

    func add(_ task: TodoTask) {
        tasks.append(task)
    }

    func update(_ task: TodoTask) {
        guard let index = tasks.firstIndex(where: { $0.id == task.id }) else { return }
        tasks[index] = task
    }

    func toggle(_ task: TodoTask) {
        guard let index = tasks.firstIndex(where: { $0.id == task.id }) else { return }
        tasks[index].isDone.toggle()
    }

    func delete(_ task: TodoTask) {
        tasks.removeAll { $0.id == task.id }
    }

    func clearCompleted() {
        tasks.removeAll { $0.isDone }
    }

    // MARK: - Saving

    private func save() {
        do {
            let data = try JSONEncoder().encode(tasks)
            try data.write(to: fileURL, options: [.atomic])
        } catch {
            print("❌ Save failed: \(error)")
        }
    }

    private func load() {
        do {
            let data = try Data(contentsOf: fileURL)
            tasks = try JSONDecoder().decode([TodoTask].self, from: data)
        } catch {
            // First launch: no file yet. Start with example tasks.
            tasks = [
                TodoTask(title: "Welcome to TaskMaster! 👋", priority: .high),
                TodoTask(title: "Swipe left to delete", priority: .low),
                TodoTask(title: "Tap the circle to complete", isDone: false)
            ]
        }
    }
}
```

Let's explain the important parts:

### Saving to a file 💾

| Part | Meaning |
|---|---|
| `URL.documentsDirectory` | The app's private **Documents** folder on the device. Files here are kept (and backed up). |
| `.appending(path: "tasks.json")` | The full path to our file. |
| `JSONEncoder().encode(tasks)` | Turn the array into JSON data (Ch 59). |
| `data.write(to: fileURL, options: [.atomic])` | Write it to the file. `.atomic` = write safely (a new file first, then swap) so a crash can't leave a half-written file. |
| `Data(contentsOf: fileURL)` | Read the file. Throws if it doesn't exist. |
| `catch` in `load()` | No file yet (first launch) → use example tasks. |

> 📖 **New word: FileManager / Documents directory**
> Every app has its own private folders. **Documents** is for the user's data. Other apps can't see it. 🔒

### `didSet` — save automatically

```swift
var tasks: [TodoTask] = [] {
    didSet { save() }
}
```

Remember **property observers** (Ch 20)? Every time `tasks` changes — add, delete, toggle — `save()` runs **automatically**. ✨

### `// MARK: -`

| Part | Meaning |
|---|---|
| `// MARK: - Saving` | A special comment. Xcode shows it as a **section header** in the jump bar (Ch 32). Helps you find code quickly. |

### The sort

```swift
.sorted { a, b in
    if a.isDone != b.isDone { return !a.isDone }
    if a.priority != b.priority { return a.priority.rawValue > b.priority.rawValue }
    return a.createdAt > b.createdAt
}
```

Read it as rules, in order:
1. **Active** tasks before done tasks.
2. Then **higher** priority first.
3. Then **newer** first.

---

## Step 3: Connect the store — `TaskMasterApp.swift`

```swift
import SwiftUI

@main
struct TaskMasterApp: App {
    @State private var store = TaskStore()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(store)
        }
    }
}
```

The store is created **once** and shared with **every** view through the environment (Ch 53).

---

## Step 4: One row — `TaskRow.swift`

```swift
import SwiftUI

struct TaskRow: View {
    let task: TodoTask
    let onToggle: () -> Void

    var body: some View {
        HStack(spacing: 12) {
            Button(action: onToggle) {
                Image(systemName: task.isDone ? "checkmark.circle.fill" : "circle")
                    .font(.title2)
                    .foregroundStyle(task.isDone ? .green : .secondary)
                    .contentTransition(.symbolEffect(.replace))
            }
            .buttonStyle(.borderless)
            .accessibilityLabel(task.isDone ? "Mark as not done" : "Mark as done")

            VStack(alignment: .leading, spacing: 4) {
                Text(task.title)
                    .strikethrough(task.isDone)
                    .foregroundStyle(task.isDone ? .secondary : .primary)

                if let due = task.dueDate {
                    Label(due.formatted(date: .abbreviated, time: .omitted), systemImage: "calendar")
                        .font(.caption)
                        .foregroundStyle(task.isOverdue ? .red : .secondary)
                }
            }

            Spacer()

            Text(task.priority.title)
                .font(.caption.bold())
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(task.priority.color.opacity(0.15), in: Capsule())
                .foregroundStyle(task.priority.color)
        }
        .padding(.vertical, 4)
    }
}

#Preview {
    List {
        TaskRow(task: TodoTask(title: "Buy milk", priority: .high, dueDate: .now), onToggle: {})
        TaskRow(task: TodoTask(title: "Done task", isDone: true, priority: .low), onToggle: {})
    }
}
```

| Part | Meaning |
|---|---|
| `let onToggle: () -> Void` | A closure (Ch 19, 51) — the row doesn't change data itself; it **tells** the parent. |
| `.contentTransition(.symbolEffect(.replace))` | Circle ↔ checkmark animates smoothly (Ch 55). |
| `due.formatted(date: .abbreviated, time: .omitted)` | Show a date like "14 Oct 2026" in the user's language. |
| `task.isOverdue ? .red : .secondary` | Overdue dates are **red**. |
| Priority "chip" | A colored capsule (Ch 44). |

---

## Step 5: Add / edit screen — `TaskEditor.swift`

The **same** screen is used to **add** a new task and **edit** an existing one.

```swift
import SwiftUI

struct TaskEditor: View {
    @Environment(TaskStore.self) private var store
    @Environment(\.dismiss) private var dismiss

    @State private var task: TodoTask
    @State private var hasDueDate: Bool
    private let isNew: Bool

    init(task: TodoTask? = nil) {
        let startTask = task ?? TodoTask(title: "")
        _task = State(initialValue: startTask)
        _hasDueDate = State(initialValue: startTask.dueDate != nil)
        isNew = (task == nil)
    }

    var body: some View {
        NavigationStack {
            Form {
                Section("Task") {
                    TextField("What do you need to do?", text: $task.title)
                    TextField("Notes (optional)", text: $task.notes, axis: .vertical)
                        .lineLimit(2...5)
                }

                Section("Priority") {
                    Picker("Priority", selection: $task.priority) {
                        ForEach(Priority.allCases) { p in
                            Text(p.title).tag(p)
                        }
                    }
                    .pickerStyle(.segmented)
                }

                Section("Due date") {
                    Toggle("Has due date", isOn: $hasDueDate.animation())
                    if hasDueDate {
                        DatePicker("Due",
                                   selection: Binding(
                                       get: { task.dueDate ?? .now },
                                       set: { task.dueDate = $0 }
                                   ),
                                   displayedComponents: .date)
                            .datePickerStyle(.graphical)
                    }
                }

                if !isNew {
                    Section {
                        Button("Delete task", role: .destructive) {
                            store.delete(task)
                            dismiss()
                        }
                    }
                }
            }
            .navigationTitle(isNew ? "New Task" : "Edit Task")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button(isNew ? "Add" : "Save") {
                        save()
                    }
                    .disabled(task.title.trimmingCharacters(in: .whitespaces).isEmpty)
                }
            }
        }
    }

    private func save() {
        if !hasDueDate { task.dueDate = nil }
        else if task.dueDate == nil { task.dueDate = .now }

        if isNew {
            store.add(task)
        } else {
            store.update(task)
        }
        dismiss()
    }
}

#Preview {
    TaskEditor()
        .environment(TaskStore())
}
```

Important parts:

| Part | Meaning |
|---|---|
| `init(task: TodoTask? = nil)` | `nil` → **new** task. A task → **edit** it. |
| `_task = State(initialValue: startTask)` | Set the **starting value** of a `@State` in an `init`. The `_` means "the wrapper itself" (like `_books` in Ch 57). |
| `@State private var task` | The editor works on a **copy** (struct = value type, Ch 22). Changes are only applied when you tap **Save**. **Cancel** = nothing changes! ✅ |
| `$hasDueDate.animation()` | A binding that **animates** whatever changes because of it — the date picker slides in. |
| `Binding(get:set:)` | A custom binding (Ch 51): the DatePicker needs a `Date`, but `dueDate` is `Date?`. |
| `trimmingCharacters(in: .whitespaces)` | Remove spaces at the start/end — so a title of only spaces is "empty". |

🧠 **Remember:** Edit a **copy**, then save it back. This makes **Cancel** work for free.

---

## Step 6: The main screen — `ContentView.swift`

```swift
import SwiftUI

struct ContentView: View {
    @Environment(TaskStore.self) private var store
    @State private var filter: TaskFilter = .all
    @State private var searchText = ""
    @State private var showNewTask = false
    @State private var editingTask: TodoTask?

    var visibleTasks: [TodoTask] {
        store.filtered(by: filter, search: searchText)
    }

    var body: some View {
        NavigationStack {
            List {
                Section {
                    Picker("Filter", selection: $filter.animation()) {
                        ForEach(TaskFilter.allCases) { f in
                            Text(f.rawValue).tag(f)
                        }
                    }
                    .pickerStyle(.segmented)
                    .listRowBackground(Color.clear)
                }

                Section {
                    ForEach(visibleTasks) { task in
                        TaskRow(task: task) {
                            withAnimation(.snappy) {
                                store.toggle(task)
                            }
                        }
                        .contentShape(Rectangle())
                        .onTapGesture {
                            editingTask = task
                        }
                        .swipeActions(edge: .trailing) {
                            Button(role: .destructive) {
                                withAnimation { store.delete(task) }
                            } label: {
                                Label("Delete", systemImage: "trash")
                            }
                        }
                        .swipeActions(edge: .leading) {
                            Button {
                                withAnimation { store.toggle(task) }
                            } label: {
                                Label(task.isDone ? "Undo" : "Done",
                                      systemImage: task.isDone ? "arrow.uturn.backward" : "checkmark")
                            }
                            .tint(.green)
                        }
                    }
                } footer: {
                    if !store.tasks.isEmpty {
                        Text("\(store.remainingCount) task\(store.remainingCount == 1 ? "" : "s") left")
                    }
                }
            }
            .navigationTitle("My Tasks")
            .searchable(text: $searchText, prompt: "Search tasks")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        showNewTask = true
                    } label: {
                        Image(systemName: "plus.circle.fill")
                            .font(.title2)
                    }
                    .accessibilityLabel("Add task")
                }
                ToolbarItem(placement: .topBarLeading) {
                    Menu {
                        Button("Clear completed", systemImage: "trash", role: .destructive) {
                            withAnimation { store.clearCompleted() }
                        }
                        .disabled(store.tasks.allSatisfy { !$0.isDone })
                    } label: {
                        Image(systemName: "ellipsis.circle")
                    }
                }
            }
            .sheet(isPresented: $showNewTask) {
                TaskEditor()
            }
            .sheet(item: $editingTask) { task in
                TaskEditor(task: task)
            }
            .overlay {
                if visibleTasks.isEmpty {
                    emptyState
                }
            }
        }
    }

    @ViewBuilder
    private var emptyState: some View {
        if !searchText.isEmpty {
            ContentUnavailableView.search(text: searchText)
        } else if store.tasks.isEmpty {
            ContentUnavailableView {
                Label("No tasks yet", systemImage: "checklist")
            } description: {
                Text("Tap + to add your first task.")
            } actions: {
                Button("Add a task") { showNewTask = true }
                    .buttonStyle(.borderedProminent)
            }
        } else {
            ContentUnavailableView("Nothing here",
                                   systemImage: filter == .done ? "tray" : "party.popper",
                                   description: Text(filter == .done ? "No completed tasks yet." : "All done! 🎉"))
        }
    }
}

#Preview {
    ContentView()
        .environment(TaskStore())
}
```

New things:

| Part | Meaning |
|---|---|
| `$filter.animation()` | Switching the filter **animates** the list. |
| `.listRowBackground(Color.clear)` | No white box behind the picker row. |
| `.sheet(item: $editingTask)` | Tap a row → edit that task (Ch 51). |
| `store.tasks.allSatisfy { !$0.isDone }` | `true` if **no** task is done → disable "Clear completed". |
| `@ViewBuilder private var emptyState` | A computed view that can return **different** views with `if/else`. |

> 📖 **New word: `@ViewBuilder`**
> Lets a function or property build views with `if`, `else` and `switch` — just like inside `body`.

---

## Step 7: Run and test! 🧪

Run the app (`Cmd + R`) and check:

| Test | Expected |
|---|---|
| Tap **+**, type a title, choose High, tap **Add** | The task appears at the top with a red "High" chip. |
| Tap the circle | It's checked, crossed out, moves down. |
| Swipe left → Delete | It disappears with an animation. |
| Tap a task, change it, tap **Cancel** | Nothing changed. ✅ |
| Tap a task, change it, tap **Save** | The change is saved. |
| Give a task a due date in the past | The date is **red**. |
| Filter: **Done** | Only completed tasks. |
| Search "milk" | Only matching tasks. |
| **Stop** the app and run again | Everything is still there! 💾 |

💡 **Tip:** Want to see the saved file? Add `print(URL.documentsDirectory)` in `TaskStore.init()`. Run, copy the path from the Console, and in Finder use **Go → Go to Folder…**. You'll find `tasks.json` — open it with TextEdit! 👀

---

## 🏆 Challenges

1. **Categories:** add an enum `Category` (Work, Home, School) with an icon, and a picker in the editor. Show the icon in the row.
2. **Today section:** split the list into "Overdue", "Today", "Later" and "No date" sections.
3. **Statistics screen:** add a tab or sheet showing total, done, and a progress bar.
4. **Haptics:** add `.sensoryFeedback(.success, trigger: store.remainingCount)` to the list — the phone gives a small vibration when a task is completed (real device only).
5. **SwiftData version:** rewrite the storage using SwiftData (Chapter 57) instead of a JSON file.
6. **Undo delete:** after deleting, show a small "Undo" button for 3 seconds.

---

## 🧠 What you practiced

- Designing **models** with enums and structs, and computed properties.
- An `@Observable` **store** with all the logic, shared through `.environment`.
- **Saving** with `Codable` + a file in the Documents folder, automatically with `didSet`.
- One editor screen for **add and edit**, working on a **copy** so Cancel is free.
- Lists with **search**, **filter**, **sort**, **swipe actions**, and **empty states**.
- Small **animations** that make the app feel great.

---

⬅️ **Back:** [Chapter 60 — Images From the Internet](60-async-image.md)
➡️ **Next:** [Chapter 62 — Project: Weather App](62-project-weather.md)
