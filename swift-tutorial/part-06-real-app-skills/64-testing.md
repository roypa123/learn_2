# Chapter 64 — Testing Your App

🍎 **Needs a Mac**

---

## What you will learn

- What **automated tests** are and why they save time.
- Adding a **test target** to your project.
- **Swift Testing**: `@Test`, `#expect`, `#require`.
- Testing models, logic and errors.
- Testing many inputs with **arguments**.
- Testing `async` code.
- Making code **testable** (keep logic out of views).
- **XCTest** (the older framework) — just so you can read it.
- **UI tests** — a short introduction.

---

## 1. Why test? 🧪

Every time you change your code, something else might **break** without you noticing. 😱

Testing by hand (tapping through the app) is slow and you forget things.

**Automated tests** are small pieces of code that **check your code** for you — in seconds, every time.

> 📖 **New word: Test**
> Code that runs your code with some input and **checks** that the result is correct.

> 📖 **New word: Unit test**
> A test for one small **unit** of code — one function or one type.

Think of a **spell checker** ✍️: you write, it checks automatically. Tests are a "correctness checker" for your logic.

| Without tests | With tests |
|---|---|
| "I hope nothing broke…" 😰 | "All 50 tests pass ✅" 😎 |
| Find bugs when users complain | Find bugs **before** users see them |
| Afraid to change old code | Change code with confidence |

---

## 2. Adding a test target

### New project

When creating a project (Chapter 33), set **Testing System** to **Swift Testing** (newer Xcode) — Xcode creates a test target for you.

### Existing project

1. **File → New → Target…**
2. Choose **Unit Testing Bundle**. Click **Next**.
3. Testing System: **Swift Testing** (if offered). Target to be Tested: your app.
4. Click **Finish**.

You'll get a new folder like `TaskMasterTests` with a file `TaskMasterTests.swift`.

```
 📘 TaskMaster
  ├─ 📁 TaskMaster            ← your app
  └─ 📁 TaskMasterTests       ← your tests (a separate target — Chapter 36)
      └─ TaskMasterTests.swift
```

> 📖 **New word: Test target**
> A separate target (Chapter 36) that contains only tests. It's not part of the app users download.

---

## 3. Your first test

Open `TaskMasterTests.swift` and write:

```swift
import Testing
@testable import TaskMaster

@Test func additionWorks() {
    let result = 2 + 3
    #expect(result == 5)
}
```

| Part | Meaning |
|---|---|
| `import Testing` | Apple's modern testing framework, **Swift Testing**. |
| `@testable import TaskMaster` | Let tests see your app's code (even `internal` things). Use **your** app's module name. |
| `@Test` | "This function is a test." |
| `#expect(result == 5)` | "I expect this to be `true`." If it's `false`, the test **fails**. |

> 📖 **New word: `#expect`**
> A macro that checks a condition. If it's false, the test fails and Xcode shows **exactly** what the values were.

### Running tests

| How | Shortcut |
|---|---|
| Run **all** tests | **Product → Test** or `Cmd + U` |
| Run **one** test | Click the ◇ diamond next to the test function |
| See all tests | **Test navigator** (`Cmd + 6`) |

Results:
- ✅ **Green** checkmark = passed.
- ❌ **Red** X = failed. Xcode shows the line and the values.

### See a failure

```swift
@Test func badMath() {
    let result = 2 + 2
    #expect(result == 5)
}
```

Xcode shows something like:

```
❌ Expectation failed: (result → 4) == 5
```

It tells you **what** `result` really was (4). Very helpful! 🔍

---

## 4. Testing your models

Let's test the `TodoTask` from Chapter 61:

```swift
import Testing
import Foundation
@testable import TaskMaster

@Test func newTaskIsNotDone() {
    let task = TodoTask(title: "Buy milk")
    #expect(task.isDone == false)
    #expect(task.priority == .medium)
}

@Test func taskWithoutDueDateIsNotOverdue() {
    let task = TodoTask(title: "No date")
    #expect(!task.isOverdue)
}

@Test func pastTaskIsOverdue() {
    let yesterday = Calendar.current.date(byAdding: .day, value: -1, to: .now)!
    let task = TodoTask(title: "Late", dueDate: yesterday)
    #expect(task.isOverdue)
}

@Test func doneTaskIsNeverOverdue() {
    let lastWeek = Calendar.current.date(byAdding: .day, value: -7, to: .now)!
    let task = TodoTask(title: "Old but done", isDone: true, dueDate: lastWeek)
    #expect(!task.isOverdue)
}
```

| Part | Meaning |
|---|---|
| `Calendar.current.date(byAdding: .day, value: -1, to: .now)` | Yesterday's date. |
| Test names | Describe **what should be true**. Long names are fine — they explain the rule! |

### The 3 steps of a good test: **Arrange – Act – Assert** 🅰️

```swift
@Test func togglingMarksTaskAsDone() {
    // Arrange: set things up
    var task = TodoTask(title: "Read")

    // Act: do the thing
    task.isDone.toggle()

    // Assert: check the result
    #expect(task.isDone)
}
```

> 📖 **New word: Assert**
> To **check** that something is true. `#expect` is an assertion.

---

## 5. Testing a class with logic

Testing `TaskStore` (Chapter 61) is harder because it **saves to a file**. In tests, we don't want to touch the real file! 🙅

**Solution:** let the store accept a **file URL**, so tests can use a temporary file.

Change `TaskStore` a little:

```swift
@MainActor
@Observable
class TaskStore {
    var tasks: [TodoTask] = [] {
        didSet { save() }
    }

    private let fileURL: URL

    init(fileURL: URL = URL.documentsDirectory.appending(path: "tasks.json")) {
        self.fileURL = fileURL
        load()
    }
    // ... rest stays the same
}
```

The app still uses the default (Documents). Tests can pass a temporary file. This is called **dependency injection**.

> 📖 **New word: Dependency injection**
> Giving an object the things it needs (a file, a service…) from **outside**, instead of creating them inside. It makes code easy to test.

Now test it:

```swift
import Testing
import Foundation
@testable import TaskMaster

@MainActor
struct TaskStoreTests {
    let store: TaskStore

    init() {
        let tempFile = URL.temporaryDirectory.appending(path: "\(UUID().uuidString).json")
        store = TaskStore(fileURL: tempFile)
        store.tasks = []      // start empty (no example tasks)
    }

    @Test func addingATaskIncreasesCount() {
        store.add(TodoTask(title: "One"))
        #expect(store.tasks.count == 1)
    }

    @Test func remainingCountIgnoresDoneTasks() {
        store.add(TodoTask(title: "A"))
        store.add(TodoTask(title: "B", isDone: true))
        store.add(TodoTask(title: "C"))
        #expect(store.remainingCount == 2)
    }

    @Test func clearCompletedRemovesOnlyDoneTasks() {
        store.add(TodoTask(title: "Keep"))
        store.add(TodoTask(title: "Remove", isDone: true))
        store.clearCompleted()
        #expect(store.tasks.map(\.title) == ["Keep"])
    }

    @Test func activeFilterHidesDoneTasks() {
        store.add(TodoTask(title: "Active"))
        store.add(TodoTask(title: "Done", isDone: true))
        let result = store.filtered(by: .active, search: "")
        #expect(result.count == 1)
        #expect(result.first?.title == "Active")
    }

    @Test func highPriorityComesFirst() {
        store.add(TodoTask(title: "Low", priority: .low))
        store.add(TodoTask(title: "High", priority: .high))
        let result = store.filtered(by: .all, search: "")
        #expect(result.first?.title == "High")
    }
}
```

| Part | Meaning |
|---|---|
| `struct TaskStoreTests` | A **suite**: a group of related tests. |
| `init()` | Runs **before each** test. Every test gets a **fresh** store. ✨ |
| `URL.temporaryDirectory` | A temporary folder — safe for tests. |
| `UUID().uuidString` | A random file name, so tests never share a file. |
| `@MainActor` | `TaskStore` is `@MainActor`, so its tests run on the main actor too. |
| `store.tasks.map(\.title)` | Get just the titles (key path — Ch 57). |

> 📖 **New word: Test suite**
> A group of related tests, usually a `struct` with `@Test` functions inside.

---

## 6. Testing many inputs: arguments 🔢

Test the weather codes from Chapter 62 with **one** test and **many** inputs:

```swift
import Testing
@testable import SkyCast

@Test(arguments: [0])
func clearSky(code: Int) {
    #expect(WeatherCondition(code: code) == .clear)
}

@Test(arguments: [61, 63, 65, 80, 81, 82])
func rainCodes(code: Int) {
    #expect(WeatherCondition(code: code) == .rain)
}

@Test(arguments: [95, 96, 99])
func thunderstormCodes(code: Int) {
    #expect(WeatherCondition(code: code) == .thunderstorm)
}

@Test(arguments: [-1, 4, 1000])
func unknownCodes(code: Int) {
    #expect(WeatherCondition(code: code) == .unknown)
}
```

| Part | Meaning |
|---|---|
| `@Test(arguments: [61, 63, ...])` | Run this test **once for each** value. |
| `code: Int` | Each value comes in as a parameter. |

Xcode shows each input separately — if `82` fails, you see **exactly** which one. 🎯

(For `==` to work on `WeatherCondition`, enums without associated values are `Equatable` automatically — Ch 23. ✅)

### Pairs of input and expected output

```swift
@Test(arguments: [
    (0, "Clear sky"),
    (3, "Cloudy"),
    (71, "Snow")
])
func descriptions(code: Int, expected: String) {
    #expect(WeatherCondition(code: code).description == expected)
}
```

---

## 7. `#require` — stop if something is missing

```swift
@Test func firstTaskHasTitle() throws {
    let store = TaskStore(fileURL: URL.temporaryDirectory.appending(path: "t.json"))
    store.tasks = [TodoTask(title: "Hello")]

    let first = try #require(store.tasks.first)
    #expect(first.title == "Hello")
}
```

| Part | Meaning |
|---|---|
| `try #require(optional)` | Unwrap an Optional. If it's `nil`, the test **stops and fails** right there. |
| `throws` on the test | Needed because `#require` can throw. |

| | `#expect` | `#require` |
|---|---|---|
| If false | Records a failure, **continues** the test | Fails and **stops** the test |
| Use for | Normal checks | Things the rest of the test **needs** (like unwrapping) |

---

## 8. Testing errors

From Chapter 26 — test that the right error is thrown:

```swift
enum DivisionError: Error {
    case divideByZero
}

func divide(_ a: Int, _ b: Int) throws -> Int {
    if b == 0 { throw DivisionError.divideByZero }
    return a / b
}

@Test func divideByZeroThrows() {
    #expect(throws: DivisionError.divideByZero) {
        try divide(10, 0)
    }
}

@Test func normalDivisionWorks() throws {
    #expect(try divide(10, 2) == 5)
}
```

| Part | Meaning |
|---|---|
| `#expect(throws: SomeError.case) { ... }` | "I expect this code to throw **this** error." |

---

## 9. Testing async code

Just mark the test `async` and use `await` (Chapter 28):

```swift
func slowDouble(_ n: Int) async -> Int {
    try? await Task.sleep(nanoseconds: 100_000_000)
    return n * 2
}

@Test func slowDoubleWorks() async {
    let result = await slowDouble(21)
    #expect(result == 42)
}
```

### Testing JSON decoding (no internet needed!) ⭐

Don't call the real internet in unit tests (slow, and it can fail). Test the **decoding** with sample JSON instead:

```swift
import Testing
import Foundation
@testable import SkyCast

@Test func decodesWeatherJSON() throws {
    let json = """
    {
      "current": { "time": "2026-10-14T15:00", "temperature_2m": 30.5,
                   "weather_code": 2, "wind_speed_10m": 10.0 },
      "daily": { "time": ["2026-10-14", "2026-10-15"],
                 "weather_code": [2, 61],
                 "temperature_2m_max": [33.0, 29.0],
                 "temperature_2m_min": [26.0, 24.0] }
    }
    """
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase

    let weather = try decoder.decode(WeatherResponse.self, from: Data(json.utf8))

    #expect(weather.current.temperature2m == 30.5)
    #expect(weather.daily.days.count == 2)
    #expect(weather.daily.days[1].code == 61)
}
```

If the API changes and your structs break, **this test catches it**. 🎉

---

## 10. Make code testable 🧩

🧠 **Remember:** You can easily test **plain Swift** code. Testing **views** is much harder.

So:

| ❌ Hard to test | ✅ Easy to test |
|---|---|
| Logic inside a View's `body` or button closures | Logic in **models**, **stores**, **view models**, **functions** |
| Code that always uses the real internet / real files | Code that receives a URL, file or service from outside (dependency injection) |
| Huge functions doing everything | Small functions with clear inputs and outputs |

This is why we put logic in `TaskStore`, `WeatherCondition`, `WeatherViewModel`… in Part 6. Now you see the reward! 🏆

---

## 11. XCTest (older framework — so you can read it)

Many existing projects use **XCTest**:

```swift
import XCTest
@testable import TaskMaster

final class TodoTaskXCTests: XCTestCase {
    func testNewTaskIsNotDone() {
        let task = TodoTask(title: "Buy milk")
        XCTAssertFalse(task.isDone)
        XCTAssertEqual(task.priority, .medium)
    }

    func testOptionalUnwrap() throws {
        let tasks = [TodoTask(title: "A")]
        let first = try XCTUnwrap(tasks.first)
        XCTAssertEqual(first.title, "A")
    }
}
```

| Swift Testing (new) | XCTest (old) |
|---|---|
| `@Test func name()` | `func testName()` inside a `class ...: XCTestCase` |
| `#expect(a == b)` | `XCTAssertEqual(a, b)` |
| `#expect(x)` | `XCTAssertTrue(x)` |
| `#expect(!x)` | `XCTAssertFalse(x)` |
| `try #require(optional)` | `try XCTUnwrap(optional)` |
| `init()` in a struct | `setUp()` method |

Both can live in the same project. For new tests, use **Swift Testing**.

---

## 12. UI tests (introduction) 🤖

**UI tests** launch your app and **tap through it automatically**, like a robot user.

1. **File → New → Target → UI Testing Bundle**.
2. Write a test:

```swift
import XCTest

final class TaskMasterUITests: XCTestCase {
    func testAddingATask() {
        let app = XCUIApplication()
        app.launch()

        app.buttons["Add task"].tap()
        let field = app.textFields["What do you need to do?"]
        field.tap()
        field.typeText("Buy bananas")
        app.buttons["Add"].tap()

        XCTAssertTrue(app.staticTexts["Buy bananas"].exists)
    }
}
```

| Part | Meaning |
|---|---|
| `XCUIApplication()` / `.launch()` | Start the app in the Simulator. |
| `app.buttons["Add task"]` | Find a button by its **label** or **accessibility label**. (Remember `.accessibilityLabel("Add task")` in Ch 61? It helps here too!) |
| `.tap()`, `.typeText()` | Act like a user. |
| `.exists` | Is it on screen? |

💡 **Tip:** UI tests are **slow** and sometimes **fragile** (they break when the design changes). Write **many unit tests** and **a few UI tests** for the most important flows.

```
         ▲  few     UI tests (slow, test whole flows)
        ▲▲▲
       ▲▲▲▲▲ many   Unit tests (fast, test logic)
```

You can also **record** UI tests: put the cursor inside a UI test function and click the **record** button (●) at the bottom of the editor, then use the app. Xcode writes the code!

---

## 🏋️ Practice

1. Add a test target to your To-Do app (Ch 61).
2. Write tests for `TodoTask.isOverdue`: no date, past date, today, future date, done.
3. Write `TaskStore` tests with a temporary file: add, toggle, delete, search.
4. Write a test with `arguments:` for `Priority.title` (low → "Low", etc.).
5. Write a JSON decoding test for the `Post` struct from Chapter 59.
6. Break your code on purpose (for example, change `isOverdue`). Run the tests — do they catch it? Then fix it.

---

## 🧠 Remember

- Tests are code that **checks** your code automatically. Run them with `Cmd + U`.
- Swift Testing: `import Testing`, `@Test`, `#expect(condition)`, `try #require(optional)`.
- **Arrange – Act – Assert.**
- `@Test(arguments: [...])` tests many inputs at once.
- `#expect(throws:)` tests errors. Mark tests `async` to test async code.
- Don't use the real internet or real files in unit tests — pass them in (dependency injection).
- Keep logic **out of views** so it's easy to test.

---

⬅️ **Back:** [Chapter 63 — Project: Notes App](63-project-notes.md)
➡️ **Next:** [Chapter 65 — Putting Your App on the App Store](65-app-store.md)
