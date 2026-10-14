# Chapter 58 — Getting Data From the Internet

🍎 **Needs a Mac** (and internet)

---

## What you will learn

- How apps talk to **servers** (request → response).
- What a **URL**, an **API** and **HTTP** are.
- `URLSession` with `async`/`await` — downloading data.
- Checking the **status code**.
- Handling errors (no internet, server problems).
- Showing **loading**, **success** and **error** states in SwiftUI.
- `.task` — loading when a screen appears.
- Sending data (POST) — a short introduction.

---

## 1. How apps get data 🌐

When the Weather app shows today's temperature, it **asks a server** on the internet.

```
   📱 Your app                           🖥️ Server
      │                                     │
      │ ── REQUEST: "Weather for Pune?" ──► │
      │                                     │  (looks it up)
      │ ◄── RESPONSE: "31°C, sunny" ─────── │
      │                                     │
```

> 📖 **New word: Server**
> A computer on the internet that stores data and answers requests.

> 📖 **New word: Request / Response**
> **Request** = the app's question. **Response** = the server's answer.

> 📖 **New word: API**
> **A**pplication **P**rogramming **I**nterface. A set of web addresses a server offers for apps to ask for data. Like a restaurant **menu** 📜: it tells you what you can order and how.

---

## 2. URLs

> 📖 **New word: URL**
> A web address, like `https://jsonplaceholder.typicode.com/users/1`.

```
https://jsonplaceholder.typicode.com/users/1?details=true
└─┬─┘   └────────────┬────────────┘└───┬───┘└─────┬─────┘
scheme            host               path       query
```

| Part | Meaning |
|---|---|
| `https` | The **scheme**. `s` = secure 🔒. iOS requires HTTPS by default (Chapter 37). |
| `jsonplaceholder.typicode.com` | The **host** — the server's name. |
| `/users/1` | The **path** — which data you want. |
| `?details=true` | The **query** — extra options. |

In Swift:

```swift
let url = URL(string: "https://jsonplaceholder.typicode.com/users/1")
```

`URL(string:)` returns an **Optional** (Chapter 17) — the text might not be a valid URL.

💡 **Tip:** In this chapter we use **JSONPlaceholder** (`jsonplaceholder.typicode.com`) — a free, fake API made for learning. No sign-up needed!

**Try it now:** open `https://jsonplaceholder.typicode.com/users/1` in your web browser (even on Windows!). You'll see the data the server sends back. 👀

---

## 3. HTTP methods and status codes

> 📖 **New word: HTTP**
> The language apps and servers use to talk over the web.

### Methods (what you want to do)

| Method | Meaning | Example |
|---|---|---|
| **GET** | **Get** data | Load a list of posts |
| **POST** | **Send** new data | Create a new post |
| **PUT** / **PATCH** | **Change** data | Edit a post |
| **DELETE** | **Delete** data | Remove a post |

### Status codes (how it went)

| Code | Meaning |
|---|---|
| **200** – 299 | ✅ **Success** (200 = OK, 201 = Created) |
| 301, 302 | ↪️ Moved somewhere else |
| **400** | ❌ Bad request (your request was wrong) |
| **401** / 403 | 🔒 Not logged in / not allowed |
| **404** | 🤷 Not found |
| **500** – 599 | 💥 Server error (the server has a problem) |

🧠 **Remember:** **2xx** = good. **4xx** = your mistake. **5xx** = the server's problem.

---

## 4. Your first download: `URLSession`

```swift
import Foundation

func downloadText() async throws -> String {
    let url = URL(string: "https://jsonplaceholder.typicode.com/users/1")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return String(decoding: data, as: UTF8.self)
}
```

| Line | Meaning |
|---|---|
| `async throws` | It takes time **and** can fail (Chapters 26 and 28). |
| `URL(string: ...)!` | We **know** this URL is valid, so `!` is OK here. |
| `URLSession.shared` | Apple's ready-to-use tool for internet requests. |
| `.data(from: url)` | Do a **GET** request. Returns the data **and** the response. |
| `try await` | Wait for it (it's slow), and it might throw (no internet!). |
| `let (data, _)` | Take the data. `_` ignores the response for now. |
| `String(decoding: data, as: UTF8.self)` | Turn the raw bytes into text. |

> 📖 **New word: URLSession**
> Apple's class for downloading and uploading data over the internet.

> 📖 **New word: Data**
> Raw bytes — the 0s and 1s the server sent. We turn them into text or objects.

### Using it in SwiftUI

```swift
struct ContentView: View {
    @State private var text = "Loading..."

    var body: some View {
        ScrollView {
            Text(text)
                .font(.system(.caption, design: .monospaced))
                .padding()
        }
        .task {
            do {
                text = try await downloadText()
            } catch {
                text = "Error: \(error.localizedDescription)"
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `.task { ... }` | Run **async** code when the view **appears**. ⭐ It's automatically cancelled if the view disappears. |
| `do { try await ... } catch { ... }` | Handle success and errors (Chapter 26). |

**Run it.** You'll see the JSON text from the server! (In Chapter 59 we'll turn it into Swift structs.)

```json
{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  ...
}
```

> 📖 **New word: `.task`**
> A modifier that starts async work when a view appears and stops it when the view goes away. Better than `.onAppear` + `Task { }` for loading.

---

## 5. Checking the response

The server might answer with an error page (404, 500…). `URLSession` does **not** throw for those — you must check!

```swift
enum NetworkError: Error {
    case badURL
    case badResponse(statusCode: Int)
}

func fetchData(from urlString: String) async throws -> Data {
    guard let url = URL(string: urlString) else {
        throw NetworkError.badURL
    }

    let (data, response) = try await URLSession.shared.data(from: url)

    guard let http = response as? HTTPURLResponse else {
        throw NetworkError.badResponse(statusCode: -1)
    }
    guard (200...299).contains(http.statusCode) else {
        throw NetworkError.badResponse(statusCode: http.statusCode)
    }

    return data
}
```

| Line | Meaning |
|---|---|
| `guard let url = URL(string:) else { throw ... }` | Safely make the URL (no `!`). |
| `response as? HTTPURLResponse` | Treat the response as an HTTP response (`as?` = "try to see it as this type"). |
| `(200...299).contains(http.statusCode)` | Is the status code a success? (Ranges — Chapter 11.) |
| `throw NetworkError.badResponse(...)` | If not, throw an error with the code. |

> 📖 **New word: `as?` (conditional cast)**
> "Try to treat this value as another type. If it isn't, give `nil`." It returns an Optional.

Try a wrong URL like `https://jsonplaceholder.typicode.com/nothing-here` — you'll get a **404** error. ✅

---

## 6. Three states: loading, success, error ⏳✅❌

A good app always shows **what's happening**. Use an **enum** (Chapter 23 — remember the `LoadingState` example?):

```swift
enum LoadState {
    case loading
    case loaded(String)
    case failed(String)
}

struct ContentView: View {
    @State private var state: LoadState = .loading

    var body: some View {
        Group {
            switch state {
            case .loading:
                ProgressView("Loading...")
            case .loaded(let text):
                ScrollView {
                    Text(text)
                        .font(.system(.caption, design: .monospaced))
                        .padding()
                }
            case .failed(let message):
                ContentUnavailableView {
                    Label("Couldn't load", systemImage: "wifi.exclamationmark")
                } description: {
                    Text(message)
                } actions: {
                    Button("Try again") {
                        Task { await load() }
                    }
                    .buttonStyle(.borderedProminent)
                }
            }
        }
        .task {
            await load()
        }
    }

    func load() async {
        state = .loading
        do {
            let data = try await fetchData(from: "https://jsonplaceholder.typicode.com/users/1")
            state = .loaded(String(decoding: data, as: UTF8.self))
        } catch {
            state = .failed(error.localizedDescription)
        }
    }
}
```

| Part | Meaning |
|---|---|
| `Group { switch state { ... } }` | Show a different view for each state. `Group` holds them without adding layout. |
| `ProgressView("Loading...")` | A spinning wheel with text. ⏳ |
| `ContentUnavailableView { } description: { } actions: { }` | A nice error screen with a **Try again** button. |
| `Task { await load() }` | Start async work from a button (Chapter 28). |

**Test the error:** turn off the Mac's Wi-Fi and run the app. You'll see the error screen. Turn Wi-Fi back on and tap **Try again**. 🎉

🧠 **Remember:** Always show **loading**, **success** and **error** states.

---

## 7. Pull to refresh 🔄

```swift
List { ... }
    .refreshable {
        await load()
    }
```

The user **pulls the list down** → a spinner appears → your `load()` runs → the spinner hides when it finishes. Free! ✨

---

## 8. Building URLs with query items

Don't build URLs by joining strings — special characters (spaces, `&`, emojis) can break them. Use `URLComponents`:

```swift
var components = URLComponents(string: "https://jsonplaceholder.typicode.com/posts")!
components.queryItems = [
    URLQueryItem(name: "userId", value: "1"),
    URLQueryItem(name: "search", value: "hello world")
]
let url = components.url!
print(url)
// https://jsonplaceholder.typicode.com/posts?userId=1&search=hello%20world
```

| Part | Meaning |
|---|---|
| `URLComponents` | A tool to build URLs piece by piece, safely. |
| `URLQueryItem(name:value:)` | One `?name=value` option. |
| `%20` | A space, safely **encoded** for URLs. Done automatically! |

Newer iOS versions also let you write `URL(string: "...")!.appending(queryItems: [...])`.

---

## 9. Sending data: POST (introduction) 📤

```swift
func createPost(title: String) async throws -> String {
    let url = URL(string: "https://jsonplaceholder.typicode.com/posts")!

    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.httpBody = try JSONEncoder().encode(["title": title, "body": "Hello!"])

    let (data, _) = try await URLSession.shared.data(for: request)
    return String(decoding: data, as: UTF8.self)
}
```

| Line | Meaning |
|---|---|
| `URLRequest(url:)` | A request you can customize. |
| `httpMethod = "POST"` | We're **sending** data. |
| `setValue("application/json", forHTTPHeaderField: "Content-Type")` | Tell the server "I'm sending JSON". |
| `httpBody = try JSONEncoder().encode(...)` | The data to send, as JSON (Chapter 59). |
| `.data(for: request)` | Note: `for:` with a request (not `from:` with a URL). |

> 📖 **New word: Header**
> Extra information sent with a request, like "Content-Type" or a login token.

JSONPlaceholder **pretends** to save it and sends back the new post with an `id`. (It doesn't really save — it's for practice.)

---

## 10. Important tips for networking 💡

| Tip | Why |
|---|---|
| **Always handle errors.** | The internet fails often: tunnels, airplanes, bad Wi-Fi. |
| **Show loading states.** | Users need to know something is happening. |
| **Use HTTPS.** | iOS blocks plain HTTP by default. Secure is better anyway. |
| **Don't put secret API keys in your app.** 🔐 | Anyone can extract them from the app file. Use your own server for secrets. |
| **Test with bad internet.** | On the Mac, the free **Network Link Conditioner** tool (from Apple's Additional Tools) can simulate slow internet. |
| **Use `.task`, not `.onAppear` + `Task`.** | `.task` cancels automatically when the screen closes. |

> 📖 **New word: API key**
> A secret code some APIs need, to know who is asking. Keep it secret!

---

## 11. Mini project: random user viewer 👤

Let's get a **random** user each time (users 1–10 exist on JSONPlaceholder) and show the raw info nicely. (In Chapter 59 we'll decode it into a struct properly.)

```swift
import SwiftUI

struct ContentView: View {
    @State private var userID = 1
    @State private var state: LoadState = .loading

    var body: some View {
        NavigationStack {
            Group {
                switch state {
                case .loading:
                    ProgressView("Fetching user \(userID)...")
                case .loaded(let json):
                    ScrollView {
                        Text(json)
                            .font(.system(.footnote, design: .monospaced))
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding()
                    }
                    .refreshable { await loadRandom() }
                case .failed(let message):
                    ContentUnavailableView("Error",
                                           systemImage: "exclamationmark.triangle",
                                           description: Text(message))
                }
            }
            .navigationTitle("User #\(userID)")
            .toolbar {
                Button("Random", systemImage: "shuffle") {
                    Task { await loadRandom() }
                }
            }
            .task { await load() }
        }
    }

    func loadRandom() async {
        userID = Int.random(in: 1...10)
        await load()
    }

    func load() async {
        state = .loading
        do {
            let data = try await fetchData(from: "https://jsonplaceholder.typicode.com/users/\(userID)")
            state = .loaded(String(decoding: data, as: UTF8.self))
        } catch {
            state = .failed(error.localizedDescription)
        }
    }
}
```

(Uses `LoadState` from section 6 and `fetchData` from section 5.)

Tap 🔀 or **pull down** to load a different user. 🎉

---

## 🏋️ Practice

1. Open `https://jsonplaceholder.typicode.com/posts/1` in your browser. Read the JSON.
2. Make an app that downloads that post and shows the raw text.
3. Add loading, success and error states with an enum.
4. Turn off Wi-Fi and check your error screen. Add a **Try again** button.
5. Add `.refreshable` to reload.
6. Try a URL that gives **404** and make sure your app shows the status code in the error.
7. Use `URLComponents` to build `.../comments?postId=1`.

---

## 🧠 Remember

- Apps send a **request** to a **server** and get a **response**.
- `let (data, response) = try await URLSession.shared.data(from: url)` downloads data.
- Check the **status code**: 200–299 = success.
- Use `.task { await load() }` to load when a view appears.
- Always show **loading / success / error** — an enum is perfect for this.
- `.refreshable { }` gives pull-to-refresh.
- Build URLs with `URLComponents`. Never put secret keys in the app.

---

⬅️ **Back:** [Chapter 57 — SwiftData](57-swiftdata.md)
➡️ **Next:** [Chapter 59 — Reading JSON](59-json-codable.md)
