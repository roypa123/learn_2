# Chapter 59 — Reading JSON

✅ **Sections 1–9 work in the browser** (https://swiftfiddle.com — add `import Foundation` at the top).
🍎 Section 10 (the app) needs a Mac.

---

## What you will learn

- What **JSON** is and how to read it.
- `Codable` — turning JSON into Swift structs (and back).
- `JSONDecoder` and `JSONEncoder`.
- Different names: `CodingKeys` and `convertFromSnakeCase`.
- Nested JSON, arrays, optional values.
- Dates in JSON.
- Debugging decoding errors.
- Building a full "load and show" app.

---

## 1. What is JSON? 📄

Most APIs send data as **JSON**.

> 📖 **New word: JSON**
> **J**ava**S**cript **O**bject **N**otation. A simple **text** format for data. Easy for humans to read and for computers to understand.

```json
{
  "name": "Meena",
  "age": 12,
  "isStudent": true,
  "height": 1.45,
  "hobbies": ["drawing", "chess"],
  "school": {
    "name": "Green Valley School",
    "city": "Pune"
  },
  "nickname": null
}
```

JSON looks a lot like Swift **dictionaries** and **arrays**!

| JSON | Example | Swift type |
|---|---|---|
| String (in `" "`) | `"Meena"` | `String` |
| Number | `12`, `1.45` | `Int`, `Double` |
| Boolean | `true`, `false` | `Bool` |
| Array `[ ]` | `["drawing", "chess"]` | `[String]` |
| Object `{ }` | `{ "name": "...", "city": "..." }` | a `struct` |
| `null` | `null` | `nil` (an Optional) |

> 📖 **New word: Key–value pair (in JSON)**
> `"name": "Meena"` — the **key** is `"name"`, the **value** is `"Meena"`. Like a dictionary (Chapter 15).

---

## 2. `Codable`: JSON ⟷ Swift

The magic word is **`Codable`**.

```swift
struct User: Codable {
    let name: String
    let age: Int
}
```

| Part | Meaning |
|---|---|
| `: Codable` | "This struct can be **decoded** from JSON and **encoded** to JSON." |

> 📖 **New word: Codable**
> A protocol (Chapter 24) that lets a type be converted to and from formats like JSON. It's really two protocols: `Decodable` (JSON → Swift) + `Encodable` (Swift → JSON).

> 📖 **New word: Decode / Encode**
> **Decode** = JSON text → Swift value. **Encode** = Swift value → JSON text.

🧠 **Remember:** The struct's **property names** must match the JSON **keys** (by default).

---

## 3. Decoding JSON ⬇️

```swift
import Foundation

struct User: Codable {
    let name: String
    let age: Int
}

let json = """
{
  "name": "Meena",
  "age": 12
}
"""

let data = Data(json.utf8)

do {
    let user = try JSONDecoder().decode(User.self, from: data)
    print(user.name)
    print(user.age)
} catch {
    print("Decoding failed: \(error)")
}
```

**Output:**

```
Meena
12
```

| Line | Meaning |
|---|---|
| `"""..."""` | A multi-line string (Chapter 9) holding JSON text. |
| `Data(json.utf8)` | Turn the text into raw `Data` (what the internet gives you). |
| `JSONDecoder()` | The tool that reads JSON. |
| `.decode(User.self, from: data)` | "Read this data as a `User`." `User.self` = the **type**. |
| `try` | Decoding can **fail** (wrong JSON) — so it throws (Chapter 26). |

✨ Swift matched `"name"` → `name` and `"age"` → `age` **automatically**!

---

## 4. Encoding to JSON ⬆️

```swift
let user = User(name: "Arun", age: 14)

let encoder = JSONEncoder()
encoder.outputFormatting = .prettyPrinted

if let data = try? encoder.encode(user) {
    print(String(decoding: data, as: UTF8.self))
}
```

**Output:**

```json
{
  "name" : "Arun",
  "age" : 14
}
```

| Part | Meaning |
|---|---|
| `JSONEncoder()` | The tool that writes JSON. |
| `.outputFormatting = .prettyPrinted` | Nice, readable formatting with new lines. (Without it, JSON is all on one line.) |
| `.encode(user)` | Swift value → `Data`. |

(The order of keys in the output may be different. That's fine — order doesn't matter in JSON objects.)

---

## 5. Arrays of objects

APIs often return a **list**:

```swift
let json = """
[
  { "name": "Ravi", "age": 12 },
  { "name": "Meena", "age": 10 },
  { "name": "Arun", "age": 14 }
]
"""

let users = try JSONDecoder().decode([User].self, from: Data(json.utf8))

for user in users {
    print("\(user.name) is \(user.age)")
}
```

**Output:**

```
Ravi is 12
Meena is 10
Arun is 14
```

| Part | Meaning |
|---|---|
| `[User].self` | "Decode an **array** of users." |

(In SwiftFiddle, top-level `try` works. In an app, put it in `do`/`catch`.)

---

## 6. Nested objects

```swift
struct School: Codable {
    let name: String
    let city: String
}

struct Student: Codable {
    let name: String
    let school: School       // a struct inside a struct
    let hobbies: [String]    // an array
}

let json = """
{
  "name": "Meena",
  "school": { "name": "Green Valley", "city": "Pune" },
  "hobbies": ["drawing", "chess"]
}
"""

let student = try JSONDecoder().decode(Student.self, from: Data(json.utf8))
print(student.school.city)
print(student.hobbies.count)
```

**Output:**

```
Pune
2
```

🧠 **Remember:** Each `{ }` in JSON → a **struct** in Swift. Each `[ ]` → an **array**.

### Tip: you don't need every key

If the JSON has 20 keys but you only need 3, just put **those 3** in your struct. Extra keys are **ignored**. 😊

---

## 7. Missing values and `null` → Optionals

```swift
struct Product: Codable {
    let name: String
    let price: Double
    let discount: Double?     // might be missing or null
}

let json = """
[
  { "name": "Pen", "price": 10, "discount": 2 },
  { "name": "Book", "price": 150, "discount": null },
  { "name": "Bag", "price": 499 }
]
"""

let products = try JSONDecoder().decode([Product].self, from: Data(json.utf8))
for p in products {
    print(p.name, p.discount ?? 0)
}
```

**Output:**

```
Pen 2.0
Book 0.0
Bag 0.0
```

| Part | Meaning |
|---|---|
| `let discount: Double?` | Optional (Chapter 17): works if the key is **missing** or `null`. |

⚠️ **Careful:** If a property is **not** Optional and the key is missing, decoding **fails** with a `keyNotFound` error. When unsure, make it Optional.

---

## 8. Different names: snake_case and `CodingKeys`

Many APIs use **snake_case** (`first_name`). Swift uses **camelCase** (`firstName`).

> 📖 **New word: snake_case**
> Words joined with underscores: `first_name`, `created_at`. 🐍

### Way 1: `convertFromSnakeCase` (easy) ⭐

```swift
struct Person: Codable {
    let firstName: String
    let lastName: String
    let phoneNumber: String
}

let json = """
{ "first_name": "Ravi", "last_name": "Kumar", "phone_number": "98765" }
"""

let decoder = JSONDecoder()
decoder.keyDecodingStrategy = .convertFromSnakeCase

let person = try decoder.decode(Person.self, from: Data(json.utf8))
print(person.firstName, person.lastName)
```

**Output:**

```
Ravi Kumar
```

| Part | Meaning |
|---|---|
| `.keyDecodingStrategy = .convertFromSnakeCase` | Automatically match `first_name` → `firstName`. |

(For encoding: `encoder.keyEncodingStrategy = .convertToSnakeCase`.)

### Way 2: `CodingKeys` (full control)

When names are **completely different**:

```swift
struct Movie: Codable {
    let title: String
    let year: Int
    let rating: Double

    enum CodingKeys: String, CodingKey {
        case title = "movie_title"
        case year = "release_year"
        case rating = "imdb_score"
    }
}

let json = """
{ "movie_title": "Lagaan", "release_year": 2001, "imdb_score": 8.1 }
"""

let movie = try JSONDecoder().decode(Movie.self, from: Data(json.utf8))
print(movie.title, movie.year, movie.rating)
```

**Output:**

```
Lagaan 2001 8.1
```

| Part | Meaning |
|---|---|
| `enum CodingKeys: String, CodingKey` | A special enum (it **must** be named `CodingKeys`) that maps property names to JSON keys. |
| `case title = "movie_title"` | "My `title` comes from the JSON key `movie_title`." |

⚠️ **Careful:** Once you write `CodingKeys`, list **every** property you want to decode. Properties not listed must have a default value.

---

## 9. Dates in JSON 📅

JSON has no date type. Dates are usually **strings** like `"2026-10-14T09:30:00Z"` (called **ISO 8601** format).

```swift
struct Event: Codable {
    let name: String
    let date: Date
}

let json = """
{ "name": "Hackathon", "date": "2026-10-14T09:30:00Z" }
"""

let decoder = JSONDecoder()
decoder.dateDecodingStrategy = .iso8601

let event = try decoder.decode(Event.self, from: Data(json.utf8))
print(event.name)
print(event.date)
```

**Output:**

```
Hackathon
2026-10-14 09:30:00 +0000
```

| Part | Meaning |
|---|---|
| `let date: Date` | A real Swift `Date`. |
| `.dateDecodingStrategy = .iso8601` | "Dates look like `2026-10-14T09:30:00Z`." |

> 📖 **New word: ISO 8601**
> A world standard for writing dates as text: `YYYY-MM-DDTHH:MM:SSZ`.

Other strategies: `.secondsSince1970` (a number like `1792000000`), `.millisecondsSince1970`, or `.formatted(someDateFormatter)` for custom formats.

---

## 10. Debugging decoding errors 🐛

When decoding fails, **print the error**. Swift tells you **exactly** what's wrong:

```swift
do {
    let user = try JSONDecoder().decode(User.self, from: data)
} catch {
    print(error)
}
```

Common errors:

| Error | Meaning | Fix |
|---|---|---|
| `keyNotFound(... "age" ...)` | The JSON doesn't have key `age`. | Make the property Optional, or check the spelling. |
| `typeMismatch(Swift.Int, ... "price" ...)` | Expected an `Int`, but the JSON has something else (like `9.99` or `"10"`). | Change the type (`Double`, `String`). |
| `valueNotFound(... )` | The value is `null`, but the property isn't Optional. | Make it Optional. |
| `dataCorrupted(... )` | Not valid JSON at all (maybe an HTML error page!). | Print the raw text to see what the server sent. |

💡 **Tip:** If decoding fails, first **print the raw JSON** text: `print(String(decoding: data, as: UTF8.self))`. Then compare it with your struct, key by key.

💡 **Tip:** Some websites (search "JSON to Swift") can generate `Codable` structs from a JSON example. Useful — but always check the result!

---

## 11. Putting it together: a posts app 📰 (🍎 Mac)

Using **JSONPlaceholder** (Chapter 58): `https://jsonplaceholder.typicode.com/posts` returns:

```json
[
  {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident...",
    "body": "quia et suscipit\nsuscipit recusandae..."
  },
  ...
]
```

(The text is fake Latin — it's placeholder data!)

### Step 1: The model

```swift
struct Post: Codable, Identifiable {
    let userId: Int
    let id: Int
    let title: String
    let body: String
}
```

| Part | Why |
|---|---|
| `Codable` | To decode from JSON. |
| `Identifiable` | The JSON already has a unique `id` → perfect for `List` (Chapter 48)! |

### Step 2: A service that loads data

```swift
enum APIError: LocalizedError {
    case badResponse(Int)

    var errorDescription: String? {
        switch self {
        case .badResponse(let code): "The server answered with code \(code)."
        }
    }
}

struct PostService {
    func fetchPosts() async throws -> [Post] {
        let url = URL(string: "https://jsonplaceholder.typicode.com/posts")!
        let (data, response) = try await URLSession.shared.data(from: url)

        if let http = response as? HTTPURLResponse, !(200...299).contains(http.statusCode) {
            throw APIError.badResponse(http.statusCode)
        }

        return try JSONDecoder().decode([Post].self, from: data)
    }
}
```

> 📖 **New word: Service**
> A type whose job is to talk to an API. Keeping network code in one place makes views simpler.

### Step 3: An observable model (Chapter 53)

```swift
@MainActor
@Observable
class PostsViewModel {
    var posts: [Post] = []
    var isLoading = false
    var errorMessage: String?

    private let service = PostService()

    func load() async {
        isLoading = true
        errorMessage = nil
        do {
            posts = try await service.fetchPosts()
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }
}
```

| Part | Meaning |
|---|---|
| `@MainActor` | UI data changes on the main thread (Chapter 53). |
| `posts`, `isLoading`, `errorMessage` | The three things the screen needs to know. |
| `load()` | Loads posts and updates the state. |

> 📖 **New word: ViewModel**
> A model made **for one screen**: it holds that screen's data and logic. A common pattern called **MVVM** (Model–View–ViewModel).

### Step 4: The views

```swift
struct ContentView: View {
    @State private var viewModel = PostsViewModel()

    var body: some View {
        NavigationStack {
            Group {
                if viewModel.isLoading && viewModel.posts.isEmpty {
                    ProgressView("Loading posts...")
                } else if let message = viewModel.errorMessage, viewModel.posts.isEmpty {
                    ContentUnavailableView {
                        Label("Couldn't load posts", systemImage: "wifi.slash")
                    } description: {
                        Text(message)
                    } actions: {
                        Button("Try again") {
                            Task { await viewModel.load() }
                        }
                        .buttonStyle(.borderedProminent)
                    }
                } else {
                    List(viewModel.posts) { post in
                        NavigationLink {
                            PostDetailView(post: post)
                        } label: {
                            VStack(alignment: .leading, spacing: 4) {
                                Text(post.title.capitalized)
                                    .font(.headline)
                                    .lineLimit(2)
                                Text("Post #\(post.id) • User \(post.userId)")
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }
                    .refreshable {
                        await viewModel.load()
                    }
                }
            }
            .navigationTitle("Posts 📰")
            .task {
                if viewModel.posts.isEmpty {
                    await viewModel.load()
                }
            }
        }
    }
}

struct PostDetailView: View {
    let post: Post

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text(post.title.capitalized)
                    .font(.title2.bold())
                Text(post.body)
                    .font(.body)
            }
            .padding()
        }
        .navigationTitle("Post #\(post.id)")
        .navigationBarTitleDisplayMode(.inline)
    }
}

#Preview {
    ContentView()
}
```

```
  Internet  ──JSON──►  PostService  ──[Post]──►  PostsViewModel  ──►  ContentView
                       (download +              (@Observable:          (shows loading,
                        decode)                  posts, isLoading,      list, or error)
                                                 errorMessage)
```

Run it — 100 posts load from the internet, with loading, error, pull-to-refresh and a detail screen. 🎉

---

## 🏋️ Practice

1. (Browser ✅) Decode `{ "city": "Delhi", "temp": 31.5, "isRaining": false }` into a struct.
2. (Browser ✅) Decode an array of 3 fruits with `name` and `color`.
3. (Browser ✅) Decode `{ "user_name": "ravi", "joined_at": "2026-01-15T10:00:00Z" }` using `convertFromSnakeCase` and `.iso8601`.
4. (Browser ✅) Encode a struct to pretty JSON and print it.
5. (Browser ✅) Make decoding fail on purpose (wrong type). Read the error message.
6. (Mac 🍎) Change the posts app to load **users** from `https://jsonplaceholder.typicode.com/users` and show their `name` and `email`.
7. (Mac 🍎) Add a search bar that filters posts by title.

<details>
<summary>Click to see an answer for 3</summary>

```swift
import Foundation

struct Member: Codable {
    let userName: String
    let joinedAt: Date
}

let json = """
{ "user_name": "ravi", "joined_at": "2026-01-15T10:00:00Z" }
"""

let decoder = JSONDecoder()
decoder.keyDecodingStrategy = .convertFromSnakeCase
decoder.dateDecodingStrategy = .iso8601

let member = try decoder.decode(Member.self, from: Data(json.utf8))
print(member.userName, member.joinedAt)
```

</details>

---

## 🧠 Remember

- **JSON** = text data: `{ }` objects → structs, `[ ]` arrays → arrays, `null` → `nil`.
- Add `: Codable` to a struct. Property names must match JSON keys.
- **Decode:** `try JSONDecoder().decode(Type.self, from: data)`.
- **Encode:** `try JSONEncoder().encode(value)`.
- Use **Optionals** for keys that may be missing or `null`.
- `.convertFromSnakeCase` for `snake_case` keys. `CodingKeys` for totally different names.
- `.dateDecodingStrategy = .iso8601` for dates.
- When decoding fails, **print the error** and the **raw JSON**.

---

⬅️ **Back:** [Chapter 58 — Networking](58-networking.md)
➡️ **Next:** [Chapter 60 — Showing Images From the Internet](60-async-image.md)
