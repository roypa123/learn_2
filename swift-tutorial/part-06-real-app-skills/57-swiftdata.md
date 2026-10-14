# Chapter 57 — Saving Big Data (SwiftData)

🍎 **Needs a Mac** (iOS 17 or newer)

---

## What you will learn

- What a **database** is.
- **SwiftData**: Apple's modern way to save lots of data.
- `@Model` — making a class that can be saved.
- `.modelContainer` — setting up storage.
- `@Query` — reading saved data (it updates automatically!).
- `modelContext` — adding, changing and deleting.
- Sorting and filtering with `#Predicate`.
- Relationships between models.
- Previews with sample data.

---

## 1. What is a database? 🗄️

When your app needs to save **many** things — 500 notes, 2000 expenses, a list of books — `@AppStorage` is not enough.

You need a **database**.

> 📖 **New word: Database**
> An organized storage for **lots** of records, on the device's disk. You can add, find, change, sort and delete records quickly.

Think of a **library** 📚:
- Each **book** is a **record**.
- Each book has **properties**: title, author, year.
- The librarian can **find**, **sort** and **add** books quickly.

> 📖 **New word: Record**
> One saved item in a database, like one note or one book.

---

## 2. What is SwiftData?

> 📖 **New word: SwiftData**
> Apple's framework (iOS 17+) for saving your Swift objects in a database — with very little code.

You write a **normal Swift class**, add `@Model`, and SwiftData handles the saving. 🪄

(Older apps use **Core Data**, which SwiftData is built on. SwiftData is much easier for beginners.)

---

## 3. Step 1: Create a model with `@Model`

Create a new project (or use an existing one). Make a new Swift file `Book.swift`:

```swift
import Foundation
import SwiftData

@Model
class Book {
    var title: String
    var author: String
    var year: Int
    var isRead: Bool
    var dateAdded: Date

    init(title: String, author: String, year: Int, isRead: Bool = false) {
        self.title = title
        self.author = author
        self.year = year
        self.isRead = isRead
        self.dateAdded = Date.now
    }
}
```

| Part | Meaning |
|---|---|
| `import SwiftData` | Bring in SwiftData. |
| `@Model` | A **macro** (Chapter 53): "Save objects of this class in the database." It also makes the class **observable**, like `@Observable`! |
| `class Book` | Must be a **class**. |
| Properties | Normal properties. SwiftData saves all of them. |
| `init(...)` | Classes need an `init` (Chapter 21). |

> 📖 **New word: Model**
> A type that describes one kind of saved data (Chapter 53). Here, `Book` is a model.

What types can properties have?

| ✅ Supported | Examples |
|---|---|
| Basic types | `String`, `Int`, `Double`, `Bool`, `Date`, `URL`, `UUID`, `Data` |
| Optionals | `String?`, `Date?` |
| Arrays of basic types | `[String]` |
| `Codable` structs and enums | An enum `Priority: String, Codable` |
| Other `@Model` classes | Relationships (section 10) |

💡 **Tip:** If you create a project with **Storage: SwiftData** (Chapter 33), Xcode sets up an example model for you.

---

## 4. Step 2: Set up the container

Open your `App` file (`YourAppNameApp.swift`):

```swift
import SwiftUI
import SwiftData

@main
struct BookshelfApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Book.self)
    }
}
```

| Part | Meaning |
|---|---|
| `.modelContainer(for: Book.self)` | "Create a database for `Book` objects, and give it to all views." |
| `Book.self` | The **type** itself (not one book). |

> 📖 **New word: Model container**
> The database itself — where all records are stored on disk.

For several models: `.modelContainer(for: [Book.self, Author.self])`

🧠 **Remember:** You set up the container **once**, at the top of the app.

---

## 5. Step 3: Read data with `@Query` ⭐

```swift
import SwiftUI
import SwiftData

struct ContentView: View {
    @Query private var books: [Book]

    var body: some View {
        NavigationStack {
            List(books) { book in
                VStack(alignment: .leading) {
                    Text(book.title).font(.headline)
                    Text("\(book.author), \(book.year)")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
            }
            .navigationTitle("My Books 📚")
        }
    }
}
```

| Part | Meaning |
|---|---|
| `@Query private var books: [Book]` | "Load **all** saved books from the database." |
| `List(books)` | `@Model` classes are automatically `Identifiable` — no ID needed! |
| **Automatic updates** | When books are added, changed or deleted, `@Query` updates the list **by itself**. ✨ |

> 📖 **New word: Query**
> A **question** to the database: "Give me all books", "Give me unread books sorted by title".

The list is empty for now — let's add books!

---

## 6. Step 4: Add, change, delete with `modelContext`

```swift
struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var books: [Book]

    var body: some View {
        NavigationStack {
            List {
                ForEach(books) { book in
                    HStack {
                        VStack(alignment: .leading) {
                            Text(book.title).font(.headline)
                            Text(book.author)
                                .font(.subheadline)
                                .foregroundStyle(.secondary)
                        }
                        Spacer()
                        Button {
                            book.isRead.toggle()
                        } label: {
                            Image(systemName: book.isRead ? "checkmark.circle.fill" : "circle")
                                .foregroundStyle(book.isRead ? .green : .gray)
                                .font(.title2)
                        }
                        .buttonStyle(.borderless)
                    }
                }
                .onDelete(perform: deleteBooks)
            }
            .navigationTitle("My Books 📚")
            .toolbar {
                Button("Add sample", systemImage: "plus") {
                    addSampleBook()
                }
            }
        }
    }

    func addSampleBook() {
        let samples = [
            ("Matilda", "Roald Dahl", 1988),
            ("Wonder", "R. J. Palacio", 2012),
            ("The Little Prince", "Antoine de Saint-Exupéry", 1943)
        ]
        let pick = samples.randomElement()!
        let book = Book(title: pick.0, author: pick.1, year: pick.2)
        modelContext.insert(book)
    }

    func deleteBooks(at offsets: IndexSet) {
        for index in offsets {
            modelContext.delete(books[index])
        }
    }
}
```

**Try it:** Run the app. Tap **+** a few times. Tick some books. Swipe to delete one. **Stop and re-run** — everything is **still there**! 🎉

| Action | Code |
|---|---|
| Get the context | `@Environment(\.modelContext) private var modelContext` |
| **Add** | `modelContext.insert(book)` |
| **Change** | Just change the property: `book.isRead.toggle()` |
| **Delete** | `modelContext.delete(book)` |
| **Save** | Automatic! (SwiftData saves for you.) |

> 📖 **New word: Model context**
> Your "workspace" for the database. You insert, change and delete objects through it. SwiftData then saves the changes.

🧠 **Remember:** **Insert** to add. **Change properties** directly. **Delete** to remove. Saving happens **automatically**.

💡 **Tip:** If you need to save **immediately** (for example before the app closes), you can call `try? modelContext.save()`.

---

## 7. Sorting

```swift
@Query(sort: \Book.title) private var books: [Book]
```

| Part | Meaning |
|---|---|
| `sort: \Book.title` | Sort by `title`, A → Z. `\Book.title` is a **key path** (Chapter 48). |

More options:

```swift
@Query(sort: \Book.year, order: .reverse) private var books: [Book]   // newest first

@Query(sort: [SortDescriptor(\Book.isRead),
              SortDescriptor(\Book.title)])
private var books: [Book]                                            // unread first, then by title
```

---

## 8. Filtering with `#Predicate` 🔍

```swift
@Query(filter: #Predicate<Book> { book in
    book.isRead == false
}, sort: \Book.title)
private var unreadBooks: [Book]
```

| Part | Meaning |
|---|---|
| `#Predicate<Book> { book in ... }` | A rule: "only books where…". It's a **macro** that turns your Swift condition into a database question. |
| `book.isRead == false` | Only unread books. |

More examples:

```swift
#Predicate<Book> { $0.year < 2000 }                    // old books
#Predicate<Book> { $0.author.contains("Dahl") }        // by an author
#Predicate<Book> { $0.year >= 2000 && !$0.isRead }     // new and unread
```

> 📖 **New word: Predicate**
> A **true/false rule** used to filter data. "Is this book unread?" → keep it if `true`.

⚠️ **Careful:** Not every Swift function works inside `#Predicate`. Simple comparisons, `&&`, `||`, `!`, and `contains` work well. If you get a strange error, simplify the condition.

---

## 9. Dynamic search and sort

A `@Query` is set when the view is created. To **change** the filter (for example, as the user types), create a **child view** with an `init` that builds the query:

```swift
struct BookListView: View {
    @Query private var books: [Book]

    init(searchText: String) {
        _books = Query(filter: #Predicate<Book> { book in
            searchText.isEmpty || book.title.localizedStandardContains(searchText)
        }, sort: \Book.title)
    }

    var body: some View {
        List(books) { book in
            Text(book.title)
        }
    }
}

struct ContentView: View {
    @State private var searchText = ""

    var body: some View {
        NavigationStack {
            BookListView(searchText: searchText)
                .searchable(text: $searchText)
                .navigationTitle("Books")
        }
    }
}
```

| Part | Meaning |
|---|---|
| `init(searchText:)` | Every time `searchText` changes, SwiftUI recreates `BookListView` with a new query. |
| `_books = Query(...)` | The `_` means "the property wrapper itself", not the array. This is how you set up a `@Query` in an `init`. |
| `localizedStandardContains` | Search ignoring big/small letters and accents. |

This is an advanced pattern — copy it when you need it! 😊

---

## 10. Relationships 🔗

Models can point to other models.

```swift
@Model
class Author {
    var name: String
    @Relationship(deleteRule: .cascade, inverse: \Novel.author)
    var novels: [Novel] = []

    init(name: String) {
        self.name = name
    }
}

@Model
class Novel {
    var title: String
    var author: Author?

    init(title: String, author: Author? = nil) {
        self.title = title
        self.author = author
    }
}
```

| Part | Meaning |
|---|---|
| `var novels: [Novel]` | An author has **many** novels. |
| `var author: Author?` | A novel has **one** author (or none). |
| `@Relationship(deleteRule: .cascade, ...)` | If an author is deleted, **delete their novels too**. |
| `inverse: \Novel.author` | The two sides are connected: adding a novel to `author.novels` also sets `novel.author`. |

| Delete rule | When the author is deleted… |
|---|---|
| `.nullify` (default) | Novels stay, but `novel.author` becomes `nil`. |
| `.cascade` | Novels are deleted too. |

Usage:

```swift
let dahl = Author(name: "Roald Dahl")
let matilda = Novel(title: "Matilda", author: dahl)
modelContext.insert(matilda)        // inserting the novel also saves the author
print(dahl.novels.count)            // 1
```

Remember to register both: `.modelContainer(for: [Author.self, Novel.self])`.

---

## 11. Previews with SwiftData

`@Query` needs a container — also in previews! Use an **in-memory** container (not saved to disk):

```swift
#Preview {
    let config = ModelConfiguration(isStoredInMemoryOnly: true)
    let container = try! ModelContainer(for: Book.self, configurations: config)

    container.mainContext.insert(Book(title: "Matilda", author: "Roald Dahl", year: 1988))
    container.mainContext.insert(Book(title: "Wonder", author: "R. J. Palacio", year: 2012, isRead: true))

    return ContentView()
        .modelContainer(container)
}
```

| Part | Meaning |
|---|---|
| `isStoredInMemoryOnly: true` | A temporary database — perfect for previews and tests. |
| `try!` | OK here — it's only a preview (Chapter 26 says avoid `try!` in real code). |
| `container.mainContext.insert(...)` | Add sample data. |
| `.modelContainer(container)` | Give it to the view. |

The simplest form (empty database): `.modelContainer(for: Book.self, inMemory: true)`

---

## 12. Editing a model with `@Bindable`

`@Model` objects are observable, so you can edit them in a form with `@Bindable` (Chapter 53):

```swift
struct BookEditView: View {
    @Bindable var book: Book

    var body: some View {
        Form {
            TextField("Title", text: $book.title)
            TextField("Author", text: $book.author)
            Stepper("Year: \(book.year)", value: $book.year, in: 1000...2100)
            Toggle("Read", isOn: $book.isRead)
        }
        .navigationTitle("Edit Book")
    }
}
```

Use it with navigation:

```swift
NavigationLink(book.title) {
    BookEditView(book: book)
}
```

Changes are **saved automatically**. No Save button needed! ✨

---

## 13. Changing your model later ⚠️

If you **add** a property after people have saved data, give it a **default value**:

```swift
var rating: Int = 0      // ✅ new property with a default
```

SwiftData can then upgrade the old database automatically. Bigger changes (renaming, changing types) need a **migration** plan — an advanced topic.

> 📖 **New word: Migration**
> Upgrading saved data from an old model design to a new one.

💡 **Tip:** While **learning**, if the app crashes after you change a model, just **delete the app** from the Simulator. That deletes the old database.

---

## 14. Mini project: a reading tracker 📚

`Book.swift` (from section 3) — plus this:

```swift
// ContentView.swift
import SwiftUI
import SwiftData

struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @Query(sort: [SortDescriptor(\Book.isRead), SortDescriptor(\Book.title)])
    private var books: [Book]
    @State private var showAdd = false

    var readCount: Int { books.filter(\.isRead).count }

    var body: some View {
        NavigationStack {
            List {
                if !books.isEmpty {
                    Section {
                        ProgressView(value: Double(readCount), total: Double(books.count)) {
                            Text("\(readCount) of \(books.count) books read")
                        }
                        .tint(.green)
                    }
                }
                Section {
                    ForEach(books) { book in
                        NavigationLink {
                            BookEditView(book: book)
                        } label: {
                            HStack {
                                Image(systemName: book.isRead ? "book.closed.fill" : "book")
                                    .foregroundStyle(book.isRead ? .green : .orange)
                                VStack(alignment: .leading) {
                                    Text(book.title).font(.headline)
                                    Text("\(book.author) • \(String(book.year))")
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }
                            }
                        }
                    }
                    .onDelete { offsets in
                        for i in offsets { modelContext.delete(books[i]) }
                    }
                }
            }
            .navigationTitle("Reading 📚")
            .toolbar {
                Button("Add", systemImage: "plus") { showAdd = true }
            }
            .sheet(isPresented: $showAdd) {
                AddBookView()
            }
            .overlay {
                if books.isEmpty {
                    ContentUnavailableView("No books yet",
                                           systemImage: "books.vertical",
                                           description: Text("Tap + to add your first book."))
                }
            }
        }
    }
}

struct AddBookView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss
    @State private var title = ""
    @State private var author = ""
    @State private var year = 2020

    var body: some View {
        NavigationStack {
            Form {
                TextField("Title", text: $title)
                TextField("Author", text: $author)
                Stepper("Year: \(String(year))", value: $year, in: 1000...2100)
            }
            .navigationTitle("New Book")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        modelContext.insert(Book(title: title, author: author, year: year))
                        dismiss()
                    }
                    .disabled(title.isEmpty || author.isEmpty)
                }
            }
        }
    }
}

// BookEditView from section 12

#Preview {
    ContentView()
        .modelContainer(for: Book.self, inMemory: true)
}
```

| New thing | Meaning |
|---|---|
| `books.filter(\.isRead)` | A key path can be used as a closure: same as `filter { $0.isRead }`. |
| `ProgressView(value:total:)` | A progress bar with a label. |
| `String(book.year)` | Show `2012`, not `2,012` (Text formats numbers with commas otherwise). |
| `AddBookView` inserts directly | It gets `modelContext` from the environment — no closure needed. |

Add books, mark them read, edit them, delete them — and **everything is saved**. 🎉

---

## 🏋️ Practice

1. Make a `@Model class Expense` with `title`, `amount: Double`, `date: Date`. List them with `@Query`.
2. Add a button that inserts a random expense. Run, restart — are they still there?
3. Add swipe-to-delete.
4. Sort expenses by date, newest first.
5. Show the **total** of all expenses at the top (`reduce` — Chapter 19).
6. Make an edit screen with `@Bindable`.
7. Add a filter: only expenses over 500.

---

## 🧠 Remember

- **SwiftData** saves lots of records in a database (iOS 17+).
- `@Model class X { ... }` — a savable model. Must be a class with an `init`.
- `.modelContainer(for: X.self)` — set up once, in the `App`.
- `@Query var items: [X]` — load data. Updates automatically. Add `sort:` and `filter: #Predicate`.
- `@Environment(\.modelContext)` → `insert(x)`, `delete(x)`. Change properties directly. Saving is automatic.
- Edit with `@Bindable var item: X`.
- Previews: `.modelContainer(for: X.self, inMemory: true)`.

---

⬅️ **Back:** [Chapter 56 — `@AppStorage`](56-appstorage.md)
➡️ **Next:** [Chapter 58 — Getting Data From the Internet](58-networking.md)
