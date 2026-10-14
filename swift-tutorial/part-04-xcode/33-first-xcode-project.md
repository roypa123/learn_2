# Chapter 33 — Your First Xcode Project

🍎 **Needs a Mac**

---

## What you will learn

- How to create a new iOS app project.
- What **every option** in the "new project" window means.
- What **every file** Xcode creates is for.
- Every line of the starter code, explained.
- How to run your app and change it.

---

## 1. Create a new project

1. Open Xcode.
2. In the Welcome window, click **Create New Project…**
   (Or from the menu: **File → New → Project…**, shortcut `Cmd + Shift + N`.)

---

## 2. Choose a template

```
┌───────────────────────────────────────────────────────────┐
│ Choose a template for your new project:                   │
│                                                           │
│ [ Multiplatform ] [ iOS ] [ macOS ] [ watchOS ] ...       │
│                                                           │
│  Application                                              │
│   ┌──────┐   ┌──────┐   ┌──────┐                          │
│   │ App  │   │ Doc  │   │ Game │                          │
│   └──────┘   └──────┘   └──────┘                          │
│                                                           │
│                              [ Cancel ]  [ Next ]         │
└───────────────────────────────────────────────────────────┘
```

1. Click the **iOS** tab at the top.
2. Under **Application**, choose **App**.
3. Click **Next**.

> 📖 **New word: Template**
> A ready-made starting point. Xcode creates the basic files for you.

| Template | Use it for |
|---|---|
| **App** ⭐ | A normal iPhone/iPad app. Use this one! |
| Document App | Apps that open and save files (like a text editor). |
| Game | Games using SpriteKit, SceneKit or Metal. |

---

## 3. Fill in the project options

```
┌────────────────────────────────────────────────────┐
│ Choose options for your new project:               │
│                                                    │
│   Product Name:            [ HelloApp           ]  │
│   Team:                    [ Ravi (Personal Team)▾]│
│   Organization Identifier: [ com.ravikumar      ]  │
│   Bundle Identifier:         com.ravikumar.HelloApp│
│                                                    │
│   Interface:               [ SwiftUI ▾ ]           │
│   Language:                [ Swift   ▾ ]           │
│   Testing System:          [ None    ▾ ]           │
│   Storage:                 [ None    ▾ ]           │
│                                                    │
│                       [ Previous ]  [ Next ]       │
└────────────────────────────────────────────────────┘
```

Let's explain **every** field:

| Field | What to type | Meaning |
|---|---|---|
| **Product Name** | `HelloApp` | The app's name. Avoid spaces and special characters for now. |
| **Team** | Your Personal Team (or **None**) | Who owns the app. Needed to run on a real iPhone. You can change it later. |
| **Organization Identifier** | `com.yourname` | A unique "address" for you, written backwards like a website: `com.ravikumar`. Use small letters, no spaces. |
| **Bundle Identifier** | (made automatically) | Organization Identifier + Product Name. The app's **unique ID** in the whole world. |
| **Interface** | **SwiftUI** | How screens are built. SwiftUI is the modern way. (The other choice, Storyboard, is the older way.) |
| **Language** | **Swift** | The programming language. |
| **Testing System** | **None** (for now) | Adds test files. We'll learn testing in Chapter 64. |
| **Storage** | **None** (for now) | Adds a database (SwiftData or Core Data). We'll learn this in Chapter 57. |

> 📖 **New word: Bundle Identifier (Bundle ID)**
> A unique name for your app, like `com.ravikumar.HelloApp`. No two apps on the App Store can have the same one.

> 📖 **New word: Organization Identifier**
> The first part of the Bundle ID. Usually a website address backwards (`example.com` → `com.example`). If you don't have a website, use `com.yourname`.

💡 **Tip:** Field names can be a little different in your Xcode version. If you see a checkbox like "Include Tests", leave it **off** for now.

Click **Next**.

---

## 4. Choose where to save

1. Choose a folder, for example **Documents → iOSProjects** (click **New Folder** to make one).
2. ✅ **Create Git repository on my Mac** — leave it checked. Git saves the history of your changes. (It's useful later.)
3. Click **Create**.

> 📖 **New word: Git**
> A tool that remembers every version of your code. You can go back if you break something.

🎉 Your project opens!

---

## 5. The files Xcode created

Look at the **Project navigator** (left, `Cmd + 1`):

```
📘 HelloApp                        ← project (settings)
 └─ 📁 HelloApp
     ├─ 📄 HelloAppApp.swift       ← where the app starts
     ├─ 📄 ContentView.swift       ← the first screen
     ├─ 🎨 Assets                   ← images, colors, app icon
     └─ 📁 Preview Content          ← (in some versions) preview-only assets
```

| File | What it is |
|---|---|
| **📘 HelloApp** (blue) | The **project**. Click it to open settings (targets, signing, build settings). |
| **HelloAppApp.swift** | The **starting point** of the app. Swift runs this first. |
| **ContentView.swift** | The **first screen** you see. You'll edit this most. |
| **Assets** | A **catalog** for images, colors and the app icon. |
| **Preview Content** | Images/data used **only** in previews, not in the real app. (Newer Xcode versions may not show this folder.) |

> 📖 **New word: Asset**
> A file your app uses that isn't code: an image, a color, an icon, a sound.

---

## 6. `HelloAppApp.swift` — line by line

Click it to open:

```swift
import SwiftUI

@main
struct HelloAppApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

| Line | Meaning |
|---|---|
| `import SwiftUI` | Bring in Apple's SwiftUI tools (Chapter 9 talked about `import`). |
| `@main` | "**This is where the app starts.**" Only one type in the app can have `@main`. |
| `struct HelloAppApp: App` | A struct (Chapter 20) that follows the `App` protocol (Chapter 24). Its name = Product Name + "App". |
| `var body: some Scene` | A computed property (Chapter 20). It returns `some Scene` (Chapter 24 explained `some`). |
| `WindowGroup { ... }` | A **window** for your app. On iPhone, it's the whole screen. |
| `ContentView()` | Create the first screen and show it inside the window. |

> 📖 **New word: `@main`**
> A special mark (an **attribute**) that tells Swift: "Start the app here."

> 📖 **New word: Scene**
> A part of the app's user interface that the system shows, like a window.

In short: *"When the app starts, open a window and show `ContentView` inside it."*

```
  App starts
     │
     ▼
 @main HelloAppApp
     │
     ▼
  WindowGroup (the window)
     │
     ▼
  ContentView (the screen)
```

---

## 7. `ContentView.swift` — line by line

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("Hello, world!")
        }
        .padding()
    }
}

#Preview {
    ContentView()
}
```

(Your version may be slightly different — that's OK.)

| Line | Meaning |
|---|---|
| `struct ContentView: View` | A screen is a **struct** that follows the **`View`** protocol. |
| `var body: some View` | The `View` protocol requires `body`: **what this screen shows**. |
| `VStack { ... }` | **V**ertical **Stack**: put things **on top of each other**, top to bottom. |
| `Image(systemName: "globe")` | Show a built-in icon called `"globe"` 🌐 (from **SF Symbols**). |
| `.imageScale(.large)` | A **modifier**: make the icon large. |
| `.foregroundStyle(.tint)` | Color it with the app's **tint** color (blue by default). |
| `Text("Hello, world!")` | Show some text. |
| `.padding()` | Add some space around the whole `VStack`. |
| `#Preview { ContentView() }` | Show `ContentView` in the **Canvas** preview. This code is **only** for Xcode — it's not in the real app. |

> 📖 **New word: View**
> Anything you can see on screen: text, image, button, or a whole screen.

> 📖 **New word: Modifier**
> A method that **changes** a view, like `.padding()` or `.font(.title)`. It starts with a dot.

Remember from Part 3:
- `struct ... : View` → a struct conforming to a **protocol** (Chapter 24).
- `var body: some View { }` → a **computed property** (Chapter 20) returning **some** type (Chapter 24).
- `VStack { ... }` → a **trailing closure** (Chapter 19)!

You already know all the Swift here. 🎉 Part 5 will teach SwiftUI properly.

---

## 8. See the preview 🖼️

1. Make sure `ContentView.swift` is open.
2. If you don't see the Canvas, press `Cmd + Option + Enter`.
3. If it says "Preview paused", press `Cmd + Option + P`.

You'll see a globe 🌐 and "Hello, world!" in a pretend iPhone.

---

## 9. Change something!

Change the text:

```swift
Text("Hello, world!")
```

to:

```swift
Text("Hi! My name is Ravi 👋")
```

Look at the Canvas — it updates **immediately**! ✨

Now try more changes:

```swift
VStack {
    Image(systemName: "star.fill")
        .imageScale(.large)
        .foregroundStyle(.yellow)
    Text("Hi! My name is Ravi 👋")
        .font(.largeTitle)
    Text("I am learning SwiftUI")
        .foregroundStyle(.gray)
}
.padding()
```

| Change | Effect |
|---|---|
| `"star.fill"` | A filled star icon ⭐ instead of a globe. |
| `.foregroundStyle(.yellow)` | Make it yellow. |
| `.font(.largeTitle)` | Make the text very big. |
| A second `Text` | A new line of text under the first. |
| `.foregroundStyle(.gray)` | Gray text. |

---

## 10. Run the app ▶

1. In the toolbar, click the **run destination** (it says something like `iPhone 16`).
2. Choose any iPhone Simulator.
3. Click ▶ **Run** (or `Cmd + R`).

What happens:

1. Xcode **builds** your app. The status says "Building…".
2. The **Simulator** opens (a pretend iPhone window). The first time can take a minute.
3. Your app starts! 🎉

To stop: click ■ **Stop** (or `Cmd + .`).

---

## 11. Seeing `print` output

Add a `print` that runs when the screen appears:

```swift
Text("Hi! My name is Ravi 👋")
    .font(.largeTitle)
    .onAppear {
        print("The screen appeared! 👀")
    }
```

| Part | Meaning |
|---|---|
| `.onAppear { ... }` | A modifier: "When this view appears on screen, run this closure." |
| `print(...)` | Your old friend from Chapter 4. |

Run the app (`Cmd + R`). Open the **debug area** (`Cmd + Shift + Y`). In the **Console** you'll see:

```
The screen appeared! 👀
```

💡 **Tip:** `print` output appears in the Console when you **run** the app (`Cmd + R`). Previews in the Canvas don't always show `print` output.

---

## 12. When something goes wrong 🔴

Let's make an error on purpose. Remove a `"`:

```swift
Text("Hi! My name is Ravi 👋)
```

You'll see:
- A **red** 🔴 icon next to the line.
- A message like `Unterminated string literal`.
- The **Issue navigator** (`Cmd + 5`) lists all errors.
- The Canvas shows "Preview paused" or an error.

Fix the `"` and everything works again.

| Color | Meaning |
|---|---|
| 🔴 Red | **Error** — the app can't build. Must fix. |
| 🟡 Yellow | **Warning** — the app builds, but something might be wrong. Should fix. |

💡 **Tip:** If Xcode shows strange errors that don't make sense, try **Product → Clean Build Folder** (`Cmd + Shift + K`), then build again (`Cmd + B`).

---

## 13. Opening your project again later

- In Finder, go to your project folder and double-click **`HelloApp.xcodeproj`**.
- Or open Xcode → in the Welcome window, click it under **Recent projects**.

> 📖 **New word: `.xcodeproj`**
> The project file. Double-click it to open the project in Xcode.

⚠️ **Careful:** Don't move or rename files using **Finder** while the project is open. Always rename/move files **inside Xcode's** Project navigator. Otherwise Xcode can lose track of them (they show in **red**).

---

## 🏋️ Practice

1. Create a new project called `AboutMe`.
2. Change `ContentView` to show:
   - An SF Symbol icon you like (try `"heart.fill"`, `"person.circle"`, `"sun.max.fill"`).
   - Your name in `.largeTitle` font.
   - Your city in `.title2` font.
   - Your favorite food in gray.
3. Run it in the Simulator.
4. Add an `.onAppear` with a `print` and find the message in the Console.
5. Make an error on purpose, read it in the Issue navigator, then fix it.

<details>
<summary>Click to see an example answer</summary>

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            Image(systemName: "person.circle")
                .imageScale(.large)
                .foregroundStyle(.blue)
            Text("Ravi Kumar")
                .font(.largeTitle)
            Text("Chennai")
                .font(.title2)
            Text("I love dosa")
                .foregroundStyle(.gray)
        }
        .padding()
        .onAppear {
            print("AboutMe screen is showing")
        }
    }
}

#Preview {
    ContentView()
}
```

</details>

---

## 🧠 Remember

- **File → New → Project → iOS → App**.
- **Bundle ID** = Organization Identifier + Product Name, and must be unique.
- **Interface: SwiftUI**, **Language: Swift**.
- `@main` marks where the app starts. `WindowGroup` shows `ContentView`.
- A screen is a `struct` that follows `View`, with a `body`.
- `#Preview` shows the screen in the Canvas.
- `Cmd + R` runs in the Simulator. `print` appears in the Console.

---

⬅️ **Back:** [Chapter 32 — A Tour of Xcode](32-xcode-tour.md)
➡️ **Next:** [Chapter 34 — The Simulator](34-simulator.md)
