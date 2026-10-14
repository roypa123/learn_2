# Chapter 40 — Finding and Fixing Bugs (Debugger and Breakpoints)

🍎 **Needs a Mac**

---

## What you will learn

- A simple **step-by-step method** for fixing any bug.
- Reading **build errors** and **warnings**.
- Debugging with `print`.
- **Breakpoints**: pausing the app to look inside.
- **Stepping** through code line by line.
- The **Variables view** and **LLDB** commands (`po`, `p`, `v`).
- **Conditional** breakpoints and **logpoints**.
- Understanding **crashes**.
- The **View Debugger** (see your screen in 3D).
- Tools for later: Instruments and Sanitizers.

---

## 1. Bugs are normal 🐛

Remember Chapter 1: a **bug** is a mistake in a program. Every programmer makes them **every day**.

> 📖 **New word: Debugger**
> A tool that lets you **pause** a running app and look inside: which line is running, what's in each variable.

Fun fact: one of the first computer "bugs" was a **real moth** 🦋 stuck in a computer in 1947!

---

## 2. A method for fixing any bug 🔍

Don't guess randomly. Be a **detective** 🕵️:

| Step | Question |
|---|---|
| 1. **Reproduce** | Can I make the bug happen again, every time? What exact steps? |
| 2. **Read** | What does the error message say? Which line? |
| 3. **Locate** | Where in the code does it go wrong? (Use `print` or breakpoints.) |
| 4. **Understand** | **Why** is it wrong? What value did I expect? What did I get? |
| 5. **Fix** | Change the code. |
| 6. **Test** | Does it work now? Did I break anything else? |

💡 **Tip:** Explain the bug **out loud** to a friend — or to a rubber duck 🦆! Often you find the answer while explaining. Programmers really call this **"rubber duck debugging"**.

---

## 3. Two kinds of problems

| Kind | When | Who finds it | Example |
|---|---|---|---|
| **Build error** 🔴 | Before running | The compiler | Missing `}`, wrong type, typo |
| **Runtime bug** 🐞 | While running | You (and users 😬) | Wrong total, crash, button does nothing |

Build errors are actually **friendly**: Xcode tells you exactly where they are!

---

## 4. Reading build errors and warnings

### Where to see them

- **In the editor**: a red 🔴 or yellow 🟡 marker on the line.
- **Issue navigator** (`Cmd + 5`): a list of all problems. Click one to jump to it.
- **Activity view** (toolbar): shows the count, e.g. 🔴 2 🟡 1.

### Example

```swift
let age: Int = "twelve"
```

```
🔴 Cannot convert value of type 'String' to specified type 'Int'
```

Read it slowly (like in Chapter 3):

| Part | Meaning |
|---|---|
| `Cannot convert value of type 'String'` | You gave a String… |
| `to specified type 'Int'` | …but the box is an Int. |

### Fix-its 🪄

Some errors show a **Fix** button. Click the red circle → Xcode suggests a fix → click **Fix**.

```
🔴 Variable 'name' was never mutated; consider changing to 'let' constant
                                                           [ Fix ]
```

⚠️ **Careful:** Read the suggested fix before clicking. It's usually right, but not always what **you** meant.

### The first error matters most

One mistake (like a missing `}`) can create **many** errors below it. **Always fix the first error first**, then build again (`Cmd + B`).

### Warnings 🟡

Warnings don't stop the build, but they often point to real problems. Try to keep **zero** warnings.

---

## 5. Debugging with `print`

The simplest tool. Add `print` to see what's happening.

```swift
func calculateTotal(prices: [Double]) -> Double {
    var total = 0.0
    for price in prices {
        print("Adding \(price), total before: \(total)")
        total += price
    }
    print("Final total: \(total)")
    return total
}
```

Run, open the Console (`Cmd + Shift + Y`), and read the output.

💡 **Tip:** Add emojis or labels to find your messages quickly: `print("🔵 total:", total)`.

### `dump` for structs and arrays

```swift
struct User {
    var name: String
    var age: Int
}

dump(User(name: "Ravi", age: 12))
```

**Console:**

```
▿ MyApp.User
  - name: "Ravi"
  - age: 12
```

`dump` shows **every property**, nicely indented.

⚠️ **Careful:** Remove extra `print`s when you're done (or wrap them in `#if DEBUG` — Chapter 35).

---

## 6. Breakpoints: pause the app ⏸️

`print` is useful, but you have to guess **what** to print. A **breakpoint** pauses the app so you can look at **everything**.

> 📖 **New word: Breakpoint**
> A marker on a line of code. When the app reaches that line, it **pauses**, so you can look inside.

### Adding a breakpoint

**Click the line number** in the left margin of the editor. A **blue arrow** appears:

```
  12      var total = 0.0
  13      for price in prices {
▶ 14          total += price         ← blue breakpoint arrow
  15      }
```

| Action | How |
|---|---|
| Add / remove a breakpoint | Click the line number (or `Cmd + \` on the current line). |
| Disable (keep it, but don't stop) | Click the blue arrow once — it turns **light blue / gray**. |
| Delete | **Drag** it out of the margin, or right-click → **Delete Breakpoint**. |
| Turn **all** breakpoints on/off | The **breakpoint button** in the debug bar (`Cmd + Y`). |
| See all breakpoints | **Breakpoint navigator** (`Cmd + 8`). |

### When the app pauses

Run the app (`Cmd + R`). When it reaches line 14:

```
┌──────────────────────────────────────────────────────────────┐
│  13      for price in prices {                               │
│▶ 14          total += price        ← green line: paused HERE │
│  15      }                                                   │
├──────────────────────────────────────────────────────────────┤
│ [⏸▶] [⤼] [⤓] [⤒]  ...                 ← debug bar           │
├─────────────────────────────┬────────────────────────────────┤
│ VARIABLES                   │ CONSOLE                        │
│  price = 9.99               │ (lldb) _                       │
│  total = 0                  │                                │
│ ▸ prices = 3 values         │                                │
└─────────────────────────────┴────────────────────────────────┘
```

- The line turns **green**: "the app is paused here, this line has **not** run yet."
- The **Variables view** shows the current values.
- The app on the Simulator is **frozen** — that's normal!

💡 **Tip:** Hover the mouse over any variable in the code while paused — a small popup shows its value. 👀

---

## 7. Stepping through code 👣

The **debug bar** has buttons to move forward:

| Button | Name | What it does | Shortcut |
|---|---|---|---|
| ▶ | **Continue** | Run until the next breakpoint. | `Ctrl + Cmd + Y` |
| ⤼ | **Step Over** | Run **this line**, stop at the next line. | `F6` |
| ⤓ | **Step Into** | If this line calls a function, **go inside** it. | `F7` |
| ⤒ | **Step Out** | Finish the current function, go back to the caller. | `F8` |

> 📖 **New word: Step**
> Running the code **one small piece at a time** while paused.

```
func main() {
    let a = add(2, 3)     ← paused here
    print(a)
}

func add(_ x: Int, _ y: Int) -> Int {
    return x + y
}

  Step Over → runs add() completely, pauses at print(a)
  Step Into → goes INSIDE add(), pauses at "return x + y"
  Step Out  → (when inside add) finishes add, goes back to main
```

💡 **Tip:** On some Mac keyboards, `F6` needs the **`fn`** key: `fn + F6`.

### Watching a loop

Put a breakpoint inside a loop. Press **Continue** each time. Watch the variables change each round — exactly like the tables we made in Chapters 12–13! 🎉

---

## 8. The Variables view

When paused, the left side of the debug area shows variables:

```
VARIABLES
 ▸ self = (MyApp.ContentView)
   price = (Double) 9.99
   total = (Double) 0
 ▾ prices = ([Double]) 3 values
     [0] = 9.99
     [1] = 5.5
     [2] = 20
```

| Feature | How |
|---|---|
| Open an array/struct | Click the ▸ arrow. |
| See details | Right-click → **Print Description**. |
| Quick Look 👁 | Select a variable → press `Space` (works for images, colors, strings). |
| Filter | Type in the search box at the bottom. |

---

## 9. LLDB: talk to the paused app

The **Console** shows `(lldb)` when paused. You can **type commands**!

> 📖 **New word: LLDB**
> The debugger engine inside Xcode. You can type commands into it while the app is paused.

| Command | Meaning | Example |
|---|---|---|
| `po something` | **P**rint **o**bject — show a value nicely. ⭐ | `po total` |
| `p something` | Print a value (with its type). | `p prices.count` |
| `v something` | Show a **v**ariable quickly (no code is run). | `v price` |
| `po expression` | Run a small piece of Swift! | `po prices.reduce(0, +)` |
| `bt` | **B**ack**t**race — which functions led here. | `bt` |
| `c` | **C**ontinue (same as the ▶ button). | `c` |

### Example session

```
(lldb) po total
0.0
(lldb) po price
9.99
(lldb) po prices.map { $0 * 2 }
▿ 3 elements
  - 0 : 19.98
  - 1 : 11.0
  - 2 : 40.0
(lldb) c
```

### Changing a value while paused 🪄

```
(lldb) expression total = 100
(lldb) po total
100.0
```

Now continue — the app uses `100`. Great for testing "what if?" without rebuilding!

---

## 10. Smarter breakpoints

**Right-click** a breakpoint → **Edit Breakpoint…**

```
┌──────────────────────────────────────────────┐
│ ContentView.swift:14                         │
│                                              │
│ Condition:  [ price > 10            ]        │
│ Ignore:     [ 0 ] times before stopping      │
│ Action:     [ Log Message ▾ ]  [ + ]         │
│             [ Price is @price@     ]         │
│ Options:    ☑ Automatically continue after   │
│               evaluating actions             │
└──────────────────────────────────────────────┘
```

### Conditional breakpoint

**Condition:** `price > 10` → the app **only** pauses when this is `true`.

Super useful in loops with 1000 rounds — stop only at the interesting one!

### Ignore count

**Ignore: 5** → skip the first 5 times, pause on the 6th.

### Logpoint (print without changing code!) ⭐

1. **Action → Log Message**.
2. Type: `Price is @price@` (put variable names between `@` signs).
3. ✅ **Automatically continue after evaluating actions**.

Now the breakpoint **prints a message** and **doesn't pause** — like a `print`, but you didn't change your code! No need to remember to delete it later.

### Exception / Swift Error breakpoints

In the **Breakpoint navigator** (`Cmd + 8`), click **+** at the bottom:

| Type | Pauses when… |
|---|---|
| **Swift Error Breakpoint** | Any Swift error is **thrown** (Chapter 26). |
| **Exception Breakpoint** | An exception happens (often helps find crash locations). |
| **Symbolic Breakpoint** | A function with a certain name is called. |

---

## 11. Understanding crashes 💥

When the app crashes, Xcode **pauses** and shows the problem line with a red message:

```swift
let numbers = [1, 2, 3]
let x = numbers[5]   // 🔴 Thread 1: Fatal error: Index out of range
```

### Common crashes (you've seen these before!)

| Message | Cause | Chapter |
|---|---|---|
| `Fatal error: Index out of range` | Array index too big | 14 |
| `Fatal error: Unexpectedly found nil while unwrapping an Optional value` | Used `!` on `nil` | 17 |
| `Fatal error: 'try!' expression unexpectedly raised an error` | Used `try!` and it failed | 26 |
| `Fatal error: Division by zero` | Divided an Int by 0 | 8 |
| `This app has crashed because it attempted to access privacy-sensitive data without a usage description` | Missing Info.plist privacy key | 37 |

### The call stack (Debug navigator)

When paused or crashed, open the **Debug navigator** (`Cmd + 7`):

```
▾ Thread 1  Queue: com.apple.main-thread
    0 calculateTotal(prices:)      ← where it crashed
    1 ContentView.body.getter      ← who called it
    2 ...SwiftUI internals...
```

> 📖 **New word: Call stack (backtrace)**
> The list of functions that were called to reach the current line, newest at the top. Like a trail of footprints 👣.

Click each line to see **your** code that led to the crash. Lines in **gray** are Apple's code — usually you look for the first line with **your** code.

### Reading the Console after a crash

Scroll **up** in the Console — there's often a helpful message **above** the `(lldb)` prompt that explains the crash.

---

## 12. The View Debugger (see your screen in 3D) 🧊

Is a button hidden? Is a view in the wrong place? Use the **View Debugger**.

1. Run the app.
2. In the debug bar, click **Debug View Hierarchy** (an icon with stacked rectangles), or **Debug → View Debugging → Capture View Hierarchy**.
3. The app pauses and shows your screen as **layers**.
4. **Click and drag** to rotate it in **3D**! 🤯

```
         ┌──────────┐
       ┌─┴────────┐ │      ← you can see each view
     ┌─┴────────┐ │ │        stacked on top of each other
     │  Button  │ │─┘
     │  Text    │─┘
     └──────────┘
```

- Click a view to see its size and position in the inspector.
- Find views that are **hidden behind** others or **outside** the screen.

---

## 13. Other tools (for later) 🧰

| Tool | Finds | Where |
|---|---|---|
| **Instruments** | Slow code, memory leaks, battery use | Product → Profile (`Cmd + I`) |
| **Memory Graph Debugger** | Objects that never get deleted (memory leaks) | Debug bar → memory graph icon |
| **Thread Sanitizer** | Data races (two threads changing data at once) | Edit Scheme → Run → Diagnostics |
| **Address Sanitizer** | Memory errors | Edit Scheme → Run → Diagnostics |
| **Main Thread Checker** | UI updated from the wrong thread | Edit Scheme → Run → Diagnostics (often on by default) |

> 📖 **New word: Memory leak**
> When objects are never removed from memory, so the app uses more and more memory over time.

You don't need these now. Just know they exist when your apps get bigger. 😊

---

## 14. Practice project: find the bugs! 🐞

Create a new project and paste this into `ContentView.swift`. It has **3 bugs**. Use print, breakpoints and the Console to find them.

```swift
import SwiftUI

struct ContentView: View {
    @State private var message = "Tap the button"

    var body: some View {
        VStack(spacing: 20) {
            Text(message)
                .font(.title2)
            Button("Calculate average") {
                let scores = [80, 90, 100]
                let avg = average(of: scores)
                message = "Average: \(avg)"
            }
            Button("Get third friend") {
                let friends = ["Ravi", "Meena"]
                message = "Third friend: \(friends[2])"
            }
        }
        .padding()
    }

    func average(of numbers: [Int]) -> Double {
        var total = 0
        for n in numbers {
            total = n
        }
        return Double(total / numbers.count)
    }
}

#Preview {
    ContentView()
}
```

(`@State` lets the screen change when `message` changes. Part 5 explains it.)

**Expected:** average of 80, 90, 100 = **90.0**.

Hints:
1. Put a breakpoint on `total = n`. Step through the loop. Watch `total`. Is it adding? 🤔
2. Look at `Double(total / numbers.count)`. Remember Chapter 8: what happens when you divide two `Int`s?
3. Tap "Get third friend". Read the crash message. How many friends are there?

<details>
<summary>Click to see the answers</summary>

**Bug 1:** `total = n` replaces the total each time. It should be `total += n`.

**Bug 2:** `total / numbers.count` divides two `Int`s first (decimals are lost), **then** converts to `Double`. Fix:

```swift
return Double(total) / Double(numbers.count)
```

**Bug 3:** `friends[2]` — there are only 2 friends (indexes 0 and 1). **Index out of range** crash. Fix: use a valid index, or check first:

```swift
if friends.count > 2 {
    message = "Third friend: \(friends[2])"
} else {
    message = "There is no third friend."
}
```

Fixed `average`:

```swift
func average(of numbers: [Int]) -> Double {
    guard !numbers.isEmpty else { return 0 }
    var total = 0
    for n in numbers {
        total += n
    }
    return Double(total) / Double(numbers.count)
}
```

</details>

---

## 🧠 Remember

- Method: **Reproduce → Read → Locate → Understand → Fix → Test**.
- Fix the **first** build error first.
- `print` and `dump` for quick checks.
- **Breakpoint**: click the line number. The app pauses there.
- **Step Over** (`F6`), **Step Into** (`F7`), **Step Out** (`F8`), **Continue** (`Ctrl + Cmd + Y`).
- In the Console: `po value` to see values, `expression x = 5` to change them.
- **Conditional breakpoints** and **logpoints** save time.
- After a crash: read the message, look at the **call stack** (`Cmd + 7`).
- **View Debugger** shows your screen in 3D.

---

## 🎉 Part 4 complete!

You now know your way around **Xcode**:

- Installing it and touring every area.
- Creating projects and using the Simulator.
- **Configurations** (Debug / Release / Staging), **targets**, **schemes**, **build settings**.
- Info.plist, icons, launch screen.
- Signing and running on a real iPhone.
- Debugging like a detective. 🕵️

Next is **Part 5: SwiftUI** — where you'll build beautiful iPhone screens, step by step! 🎨📱

---

⬅️ **Back:** [Chapter 39 — Running on a Real iPhone](39-running-on-iphone.md)
➡️ **Next:** [Chapter 41 — What Is SwiftUI?](../part-05-swiftui/41-what-is-swiftui.md)
