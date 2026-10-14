# Chapter 35 — Xcode Configurations: Debug vs Release

🍎 **Needs a Mac**

---

## What you will learn

- What a **build configuration** is.
- The two default configurations: **Debug** and **Release**.
- How they are different (speed, safety, size, debugging).
- Using `#if DEBUG` in your code.
- Choosing which configuration to use when running.
- Adding your **own** configuration (like **Staging**).
- Using `.xcconfig` files (a short introduction).

---

## 1. What is a build configuration?

When Xcode **builds** your app, it follows a set of **rules**: how fast to make the code, whether to include debugging help, which server to talk to, and so on.

A **build configuration** is a **named set of these rules**.

> 📖 **New word: Build configuration**
> A named group of build settings. Xcode starts with two: **Debug** and **Release**.

Think of a **car** 🚗:

| Mode | Like |
|---|---|
| **Debug** | A car in the **workshop**: the hood is open, the mechanic can see every part, sensors everywhere. Easy to fix, but not ready for the road. |
| **Release** | The car on the **road**: hood closed, fast, light, ready for customers. |

---

## 2. Debug vs Release — side by side

| | 🛠️ **Debug** | 🚀 **Release** |
|---|---|---|
| Used when | You're **developing**: running from Xcode (`Cmd + R`). | You're **publishing**: App Store, TestFlight (Archive). |
| Code speed | Slower (not optimized). | Faster (optimized). |
| Build speed | Faster to build. | Slower to build. |
| Debugger | Works perfectly: see every variable. | Harder: some variables are "optimized away". |
| App size | Bigger. | Smaller. |
| `DEBUG` flag | ✅ Set | ❌ Not set |
| Swift optimization level | `-Onone` (No Optimization) | `-O` (Optimize for Speed) |

> 📖 **New word: Optimize**
> To make code **faster or smaller**. The compiler rewrites your code in a smarter way. It takes extra build time.

> 📖 **New word: Compiler**
> The program that turns your Swift code into instructions the device understands.

🧠 **Remember:** You **write and test** with **Debug**. Users **download** the **Release** version.

---

## 3. Where to see configurations

1. Click the **blue project icon** 📘 at the top of the Project navigator.
2. In the editor, under **PROJECT**, click your project (not the target).
3. Click the **Info** tab.
4. Look at the **Configurations** section:

```
┌─────────────────────────────────────────────┐
│ Configurations                              │
│   Name           Based on Configuration File│
│   ▸ Debug        None                       │
│   ▸ Release      None                       │
│   [+] [-]                                   │
│                                             │
│ Use [Release] for command-line builds       │
└─────────────────────────────────────────────┘
```

| Part | Meaning |
|---|---|
| **Debug**, **Release** | The two configurations. |
| **Based on Configuration File** | An optional `.xcconfig` file (section 9). |
| **[+]** | Add a new configuration (section 8). |

---

## 4. Seeing the differences in Build Settings

1. Click the project 📘 → under **TARGETS**, click your app.
2. Click the **Build Settings** tab.
3. Click **All** and **Levels** (or **Combined**) at the top.
4. In the search box (top-right), type `optimization`.

```
┌───────────────────────────────────────────────────────────┐
│ Swift Compiler - Code Generation                          │
│   Optimization Level                                      │
│     Debug       No Optimization [-Onone]                  │
│     Release     Optimize for Speed [-O]                   │
└───────────────────────────────────────────────────────────┘
```

Click the small ▸ arrow next to a setting to see a different value **for each configuration**.

Now search for `active compilation`:

```
│ Active Compilation Conditions                             │
│     Debug       DEBUG                                     │
│     Release     (empty)                                   │
```

This `DEBUG` word is what makes `#if DEBUG` work (next section).

> 📖 **New word: Build setting**
> One rule for building, like "optimization level" or "app name". It can have a different value in Debug and Release.

---

## 5. `#if DEBUG` — code only for Debug ⭐

Sometimes you want code that **only** runs while developing. For example, extra `print` messages or a test button.

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            Text("Welcome!")

            #if DEBUG
            Text("🛠️ Debug build")
                .foregroundStyle(.red)
            #endif
        }
        .onAppear {
            #if DEBUG
            print("ContentView appeared (debug only)")
            #endif
        }
    }
}
```

| Part | Meaning |
|---|---|
| `#if DEBUG` | "Only include the following code **if** the `DEBUG` condition is set." |
| `#endif` | End of the special part. |

| Configuration | What happens |
|---|---|
| **Debug** | The red "Debug build" text **shows**, and the `print` **runs**. |
| **Release** | That code is **completely removed** from the app. Users never see it. |

> 📖 **New word: Compiler directive**
> A line starting with `#` that gives instructions to the **compiler**, not to the running app. `#if`, `#else`, `#endif` are compiler directives.

### `#else`

```swift
#if DEBUG
let serverURL = "https://test.example.com"
#else
let serverURL = "https://api.example.com"
#endif
```

| Configuration | `serverURL` is |
|---|---|
| Debug | the **test** server |
| Release | the **real** server |

⚠️ **Careful:** `#if DEBUG` is **not** the same as `if`. It's decided when **building**, not while the app runs. The other code doesn't even exist in the app.

💡 **Tip:** Use `#if DEBUG` for: extra logging, fake test data, developer menus, test servers. **Never** for important features — they'd disappear in Release!

---

## 6. Choosing the configuration when you run

By default:
- **Run** (`Cmd + R`) uses **Debug**.
- **Archive** (Product → Archive, for the App Store) uses **Release**.

To **test** the Release version on your Simulator:

1. Click the **scheme** name in the toolbar (left of the device) → **Edit Scheme…** (shortcut: `Cmd + <`, which is `Cmd + Shift + ,`).
2. On the left, click **Run**.
3. Click the **Info** tab.
4. Change **Build Configuration** from **Debug** to **Release**.
5. Click **Close**. Run with `Cmd + R`.

```
┌───────────────────────────────────────────────────┐
│ Scheme: HelloApp                                  │
│ ┌──────────┐  [Info] [Arguments] [Options] [Diag.]│
│ │ ▶ Build  │                                      │
│ │ ▶ Run  ◀ │  Build Configuration: [ Debug ▾ ]    │
│ │ ▶ Test   │  Executable:          HelloApp.app   │
│ │ ▶ Profile│  Debug executable:    ☑              │
│ │ ▶ Analyze│                                      │
│ │ ▶ Archive│                                      │
│ └──────────┘                       [ Close ]      │
└───────────────────────────────────────────────────┘
```

Now the red "Debug build" text is **gone**. ✅

⚠️ **Careful:** Remember to change it **back to Debug** after testing! Otherwise debugging will be harder.

💡 **Tip:** Why test Release? Sometimes a bug **only** happens in Release (because of optimization or missing `#if DEBUG` code). Testing Release before publishing catches these.

---

## 7. The scheme actions and their configurations

Each scheme action uses one configuration:

| Action | Menu | Default configuration |
|---|---|---|
| **Run** | Product → Run (`Cmd + R`) | Debug |
| **Test** | Product → Test (`Cmd + U`) | Debug |
| **Profile** | Product → Profile (`Cmd + I`) | Release |
| **Analyze** | Product → Analyze | Debug |
| **Archive** | Product → Archive | Release |

> 📖 **New word: Profile**
> Running the app with **Instruments**, a tool that measures speed and memory. It uses Release so you measure the real speed.

> 📖 **New word: Archive**
> Building the final app package to upload to the App Store or TestFlight.

---

## 8. Adding your own configuration: Staging 🎭

Many teams have **3** versions of their app:

| Configuration | Server | Who uses it |
|---|---|---|
| **Debug** | test server | developers |
| **Staging** | test server, but built like Release | testers, before launch |
| **Release** | real server | customers |

### Step 1: Duplicate a configuration

1. Project 📘 → **PROJECT** → **Info** tab → **Configurations**.
2. Click **+** → **Duplicate "Release" Configuration**.
3. Name it `Staging`.

### Step 2: Add a compilation condition

1. Target → **Build Settings** → search `active compilation`.
2. Open the ▸ arrow on **Active Compilation Conditions**.
3. Double-click the **Staging** row. Add `STAGING`.

```
│ Active Compilation Conditions                     │
│     Debug       DEBUG                             │
│     Release                                       │
│     Staging     STAGING                           │
```

### Step 3: Use it in code

```swift
enum AppEnvironment {
    static var name: String {
        #if DEBUG
        return "Development"
        #elseif STAGING
        return "Staging"
        #else
        return "Production"
        #endif
    }

    static var apiURL: String {
        #if DEBUG || STAGING
        return "https://test.example.com"
        #else
        return "https://api.example.com"
        #endif
    }
}

// Anywhere in the app:
// print(AppEnvironment.name, AppEnvironment.apiURL)
```

| Part | Meaning |
|---|---|
| `#elseif STAGING` | "Otherwise, if `STAGING` is set…" |
| `#if DEBUG \|\| STAGING` | "If either one is set…" (`\|\|` = OR, like in Chapter 10). |

> 📖 **New word: Production**
> The **real** version that customers use, with real data. Also called "prod".

### Step 4: Use Staging when running

Edit Scheme → **Run** → **Info** → **Build Configuration: Staging**.

💡 **Tip:** Many teams create a **separate scheme** for each configuration (e.g. "HelloApp Staging"), so they can switch quickly. We'll learn schemes in Chapter 36.

---

## 9. `.xcconfig` files (short introduction)

Changing many build settings by clicking is slow, and hard to see in Git. Teams often put settings in a **text file** instead.

> 📖 **New word: `.xcconfig` file**
> A plain text file with build settings, one per line. A configuration can be "based on" it.

### Create one

1. **File → New → File…** → search **Configuration Settings File** → name it `Debug.xcconfig`.
2. Repeat for `Release.xcconfig` (and `Staging.xcconfig` if you have it).

### Write settings inside

`Debug.xcconfig`:

```
// Debug settings
API_BASE_URL = test.example.com
APP_DISPLAY_NAME = Hello Dev
```

`Release.xcconfig`:

```
// Release settings
API_BASE_URL = api.example.com
APP_DISPLAY_NAME = Hello
```

| Line | Meaning |
|---|---|
| `// ...` | A comment. |
| `NAME = value` | A build setting and its value. You can make your own names. |

### Connect them

Project 📘 → **PROJECT** → **Info** → **Configurations** → open ▸ **Debug** → in the column **Based on Configuration File**, choose `Debug.xcconfig`. Do the same for Release.

### Use a setting

- **App name on the home screen:** Target → Build Settings → search `display name` → set **Bundle Display Name** to `$(APP_DISPLAY_NAME)`.
  Now the Debug app is called "Hello Dev" and the Release app is "Hello". 🎉

| Part | Meaning |
|---|---|
| `$(APP_DISPLAY_NAME)` | "Use the value of this setting here." |

⚠️ **Careful:** In `.xcconfig` files, `//` starts a comment. So a URL like `https://...` gets cut off at `//`! That's why we wrote just the domain (`test.example.com`) above. Add `https://` in code.

💡 **Tip:** This is an advanced topic. It's fine if you just **know it exists** for now. Come back when your app needs different servers.

---

## 10. Quick summary diagram

```
               ┌──────────────── Build Configuration ────────────────┐
               │                                                     │
          🛠️ Debug                     🎭 Staging                 🚀 Release
     (Run, Test, Analyze)          (for testers)              (Profile, Archive)
     -Onone, DEBUG flag            -O, STAGING flag            -O, no flag
     test server                   test server                 real server
     great debugging               real speed                  App Store
```

---

## 🏋️ Practice

1. In your project, find **Optimization Level** in Build Settings. Write down its Debug and Release values.
2. Add a red `Text("DEBUG MODE")` wrapped in `#if DEBUG`. Run it — you should see it.
3. Edit Scheme → Run → Build Configuration → **Release**. Run again. The text should be gone. Then switch back to **Debug**.
4. Write a constant `greeting` that is `"Hello, developer!"` in Debug and `"Hello!"` in Release, using `#if DEBUG` / `#else`. Show it in a `Text`.
5. (Challenge) Add a **Staging** configuration with a `STAGING` condition, and show `"Staging"` on screen when it's active.

---

## 🧠 Remember

- A **build configuration** is a named set of build settings.
- **Debug** = for developing (slow code, great debugging, `DEBUG` flag).
- **Release** = for users (fast, optimized, no `DEBUG` flag).
- `#if DEBUG ... #else ... #endif` includes code only in some builds.
- Change the configuration in **Edit Scheme → Run → Info → Build Configuration**.
- You can add your own (like **Staging**) and use `.xcconfig` files.

---

⬅️ **Back:** [Chapter 34 — The Simulator](34-simulator.md)
➡️ **Next:** [Chapter 36 — Targets, Schemes and Build Settings](36-targets-schemes-build-settings.md)
