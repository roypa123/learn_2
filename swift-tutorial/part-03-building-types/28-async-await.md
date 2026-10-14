# Chapter 28 — `async` and `await` (Waiting for Slow Things)

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- Why some work is **slow** and must not freeze the app.
- `async` — marking a function that takes time.
- `await` — waiting for it.
- `async throws` — slow work that can fail.
- Doing many things at the same time with `async let`.
- `Task` — starting async work.

💡 **Why this matters:** Apps download data from the internet all the time. That's slow! In Part 6 you'll use `async`/`await` to load weather, images and more.

---

## 1. Fast work and slow work

| Fast ⚡ (microseconds) | Slow 🐢 (seconds) |
|---|---|
| `2 + 3` | Downloading a photo |
| Sorting 10 numbers | Asking a server for the weather |
| Joining two strings | Reading a big file |

If an app **stops and waits** for slow work, the screen **freezes**. You can't tap anything. 😡

---

## 2. A real-life example 🍕

You order a pizza.

**Bad way (blocking):** You stand at the door and stare for 30 minutes. You can't do anything else.

**Good way (async):** You order, then watch TV 📺. When the doorbell rings 🔔, you get the pizza.

Swift's `async`/`await` is the **good way**.

> 📖 **New word: Asynchronous (async)**
> Work that **takes time** and finishes **later**. While waiting, other things can happen.

> 📖 **New word: await**
> "Wait here for the result — but let the rest of the app keep working."

---

## 3. Your first async function

```swift
func makeTea() async -> String {
    print("☕ Boiling water...")
    try? await Task.sleep(nanoseconds: 1_000_000_000)   // wait 1 second
    print("☕ Tea is ready!")
    return "Tea"
}

let drink = await makeTea()
print("I got: \(drink)")
```

**Output** (after about 1 second):

```
☕ Boiling water...
☕ Tea is ready!
I got: Tea
```

| Part | Meaning |
|---|---|
| `async` | Written before `->`. "This function **takes time**." |
| `Task.sleep(nanoseconds: 1_000_000_000)` | Pretend to do slow work: wait 1 second. (1 second = 1,000,000,000 nanoseconds.) |
| `try? await` | `sleep` can throw (if cancelled) and is async. We need both words. |
| `await makeTea()` | Call the async function and **wait** for its result. |

⚠️ **Careful:** You **must** write `await` before calling an async function:

```swift
let drink = makeTea()   // ❌ ERROR: expression is 'async' but is not marked with 'await'
```

💡 **Tip:** In SwiftFiddle, you can use `await` directly at the top level of your code. In a real app, you'll use it inside a `Task` or a SwiftUI `.task { }` (see below).

> 📖 **New word: Task.sleep**
> Pauses async code for some time **without** freezing everything. We use it here to **pretend** to do slow work, like downloading.

---

## 4. `async` and `await` work together like `throws` and `try`

| Throwing | Async |
|---|---|
| `func f() throws` | `func f() async` |
| call with `try f()` | call with `await f()` |

And you can have **both**:

```swift
enum DownloadError: Error {
    case noInternet
}

func downloadPhoto(name: String, internet: Bool) async throws -> String {
    try await Task.sleep(nanoseconds: 500_000_000)   // 0.5 seconds
    if !internet {
        throw DownloadError.noInternet
    }
    return "📷 \(name).jpg"
}

do {
    let photo = try await downloadPhoto(name: "beach", internet: true)
    print("Downloaded \(photo)")

    let photo2 = try await downloadPhoto(name: "mountain", internet: false)
    print("Downloaded \(photo2)")
} catch {
    print("Download failed: \(error)")
}
```

**Output:**

```
Downloaded 📷 beach.jpg
Download failed: noInternet
```

| Part | Meaning |
|---|---|
| `async throws` | "Takes time **and** might fail." Order: `async` first, then `throws`. |
| `try await` | Call it. Order: `try` first, then `await`. |

🧠 **Remember the order:**
- In the function: `async throws`
- When calling: `try await`

---

## 5. One after another (sequential)

```swift
func cook(_ dish: String, seconds: Double) async -> String {
    print("🍳 Start \(dish)")
    try? await Task.sleep(nanoseconds: UInt64(seconds * 1_000_000_000))
    print("✅ Done \(dish)")
    return dish
}

let a = await cook("rice", seconds: 1)
let b = await cook("curry", seconds: 1)
print("Dinner: \(a) and \(b)")
```

**Output** (takes about **2** seconds):

```
🍳 Start rice
✅ Done rice
🍳 Start curry
✅ Done curry
Dinner: rice and curry
```

Each `await` waits for the previous one to finish. Rice **then** curry. 1 + 1 = 2 seconds.

(`UInt64(...)` converts our seconds into the number type that `sleep` needs.)

---

## 6. At the same time: `async let` ⚡

A real cook makes rice and curry **at the same time** on two stoves!

```swift
async let rice = cook("rice", seconds: 1)
async let curry = cook("curry", seconds: 1)

let dinner = await [rice, curry]
print("Dinner: \(dinner)")
```

**Output** (takes about **1** second!):

```
🍳 Start rice
🍳 Start curry
✅ Done rice
✅ Done curry
Dinner: ["rice", "curry"]
```

(The order of "Start"/"Done" lines can be different each time — they're happening together!)

⚠️ **Careful (SwiftFiddle):** If `async let` gives an error at the top level of your code, put the code inside an async function and call it:

```swift
func main() async {
    async let rice = cook("rice", seconds: 1)
    async let curry = cook("curry", seconds: 1)
    print("Dinner: \(await [rice, curry])")
}

await main()
```

| Part | Meaning |
|---|---|
| `async let rice = ...` | "Start cooking rice **now**, but don't wait yet." |
| `async let curry = ...` | "Start curry **now** too." |
| `await [rice, curry]` | "**Now** wait for both to finish." |

```
Sequential:   [ rice  ][ curry ]        → 2 seconds
async let:    [ rice  ]
              [ curry ]                 → 1 second
```

> 📖 **New word: Concurrency**
> Doing several things **at the same time**.

💡 **Tip:** Use `async let` when tasks **don't depend** on each other. If curry needs the rice first, do them one after another.

---

## 7. `Task` — starting async work from normal code

Normal (non-async) functions **can't** use `await`:

```swift
func buttonTapped() {
    let tea = await makeTea()   // ❌ ERROR: 'async' call in a function that does not support concurrency
}
```

Solution: wrap it in a `Task`:

```swift
func buttonTapped() {
    Task {
        let tea = await makeTea()
        print("Enjoy your \(tea)!")
    }
    print("Button tapped! (this prints first)")
}
```

| Part | Meaning |
|---|---|
| `Task { ... }` | "Start this async work in the background." |
| The `print` after | Runs **right away**, without waiting for the tea. |

> 📖 **New word: Task**
> A unit of async work. `Task { }` starts it from normal code.

💡 **Look ahead:** In SwiftUI, you'll mostly use `.task { }` on a view, or `Task { }` inside a button. For example:

```swift
Button("Load") {
    Task {
        await loadWeather()
    }
}
```

⚠️ **Careful (SwiftFiddle):** If your top-level code ends before the `Task` finishes, you might not see its output. Add `try? await Task.sleep(nanoseconds: 2_000_000_000)` at the very end to give it time.

---

## 8. Async in loops

```swift
let cities = ["Delhi", "Mumbai", "Chennai"]

func fetchTemperature(for city: String) async -> Int {
    try? await Task.sleep(nanoseconds: 300_000_000)
    return Int.random(in: 20...40)
}

for city in cities {
    let temp = await fetchTemperature(for: city)
    print("🌡️ \(city): \(temp)°C")
}
```

**Example output** (numbers are random):

```
🌡️ Delhi: 34°C
🌡️ Mumbai: 29°C
🌡️ Chennai: 37°C
```

Each city waits for the one before it.

---

## 9. Many at once: `withTaskGroup` (preview)

When you have a **list** of things to do at the same time, use a **task group**:

```swift
let temps = await withTaskGroup(of: (String, Int).self) { group in
    for city in cities {
        group.addTask {
            (city, await fetchTemperature(for: city))
        }
    }

    var results: [String: Int] = [:]
    for await (city, temp) in group {
        results[city] = temp
    }
    return results
}

print(temps)
```

| Part | Meaning |
|---|---|
| `withTaskGroup(of: (String, Int).self)` | Make a group. Each task gives back a `(String, Int)` tuple. |
| `group.addTask { ... }` | Start one task per city — all at the same time. |
| `for await (city, temp) in group` | Collect results as each one finishes. |

This is more advanced. You don't need to master it now — just know it exists. 😊

---

## 10. Actors (one sentence preview)

When many tasks change the **same** data at the same time, things can get mixed up. Swift has **actors** — like a class with a "one at a time, please" 🚪 rule. In SwiftUI, you'll see `@MainActor`, which means "run this on the main thread, where the screen is updated". We'll meet it again in Part 5.

---

## 11. Mini project: loading a profile page 👤

```swift
struct User {
    let name: String
}

enum LoadError: Error {
    case serverDown
}

func fetchUser() async throws -> User {
    try await Task.sleep(nanoseconds: 800_000_000)
    return User(name: "Meena")
}

func fetchPosts() async throws -> [String] {
    try await Task.sleep(nanoseconds: 1_000_000_000)
    return ["My first post", "I love Swift!", "Holiday photos 🏖️"]
}

func fetchFollowers() async throws -> Int {
    try await Task.sleep(nanoseconds: 600_000_000)
    return 128
}

print("⏳ Loading profile...")

do {
    async let user = fetchUser()
    async let posts = fetchPosts()
    async let followers = fetchFollowers()

    let (u, p, f) = try await (user, posts, followers)

    print("👤 \(u.name)")
    print("👥 \(f) followers")
    print("📝 Posts:")
    for post in p {
        print("   - \(post)")
    }
} catch {
    print("❌ Could not load profile: \(error)")
}
```

**Output** (after about 1 second — the time of the **slowest** task, not all three added up!):

```
⏳ Loading profile...
👤 Meena
👥 128 followers
📝 Posts:
   - My first post
   - I love Swift!
   - Holiday photos 🏖️
```

| Part | Meaning |
|---|---|
| Three `async let` | Start all three downloads **at the same time**. |
| `try await (user, posts, followers)` | Wait for all three. If any one throws, we go to `catch`. |
| `let (u, p, f) = ...` | Take the three results out of the tuple. |

Without `async let`: 0.8 + 1.0 + 0.6 = **2.4 seconds**.
With `async let`: about **1.0 second**. 🚀

---

## 🏋️ Practice

1. Write `func boilEgg() async -> String` that sleeps 1 second and returns `"🥚 Boiled egg"`. Call it with `await` and print the result.
2. Write `func checkWeather(city: String) async throws -> String` that throws an error if `city` is empty. Call it with `try await` inside `do`/`catch` — once with `"Pune"` and once with `""`.
3. Use `async let` to run `boilEgg()` and a new `makeToast()` (sleeps 1 second) **at the same time**. Print both when done.
4. Why can't you write `await` inside a normal function? How do you fix it?

<details>
<summary>Click to see the answers</summary>

```swift
// 1
func boilEgg() async -> String {
    try? await Task.sleep(nanoseconds: 1_000_000_000)
    return "🥚 Boiled egg"
}
print(await boilEgg())

// 2
enum WeatherError: Error { case noCity }

func checkWeather(city: String) async throws -> String {
    try await Task.sleep(nanoseconds: 300_000_000)
    if city.isEmpty { throw WeatherError.noCity }
    return "☀️ Sunny in \(city)"
}

for city in ["Pune", ""] {
    do {
        print(try await checkWeather(city: city))
    } catch {
        print("Error: \(error)")
    }
}

// 3
func makeToast() async -> String {
    try? await Task.sleep(nanoseconds: 1_000_000_000)
    return "🍞 Toast"
}
async let egg = boilEgg()
async let toast = makeToast()
print("Breakfast:", await egg, await toast)   // about 1 second total
```

4. A normal function can't pause and wait. Fix it by wrapping the async code in `Task { ... }`, or by marking the function itself `async`.

</details>

---

## 🧠 Remember

- `async` marks a function that **takes time**. Call it with `await`.
- `async throws` + `try await` for slow work that can fail.
- Each `await` waits. To run things **at the same time**, use `async let`.
- `Task { }` starts async work from normal code (like a button tap).
- `Task.sleep` pretends to do slow work.

---

⬅️ **Back:** [Chapter 27 — Generics](27-generics.md)
➡️ **Next:** [Chapter 29 — Mini Project: Text Adventure Game](29-project-text-adventure.md)
