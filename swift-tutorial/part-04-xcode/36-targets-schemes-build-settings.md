# Chapter 36 — Targets, Schemes and Build Settings

🍎 **Needs a Mac**

---

## What you will learn

- **Project** vs **Target** — what's the difference?
- The tabs of a target: **General**, **Signing & Capabilities**, **Info**, **Build Settings**, **Build Phases**.
- **Deployment target** (the minimum iOS version).
- What a **scheme** is and how to edit it.
- How build settings are inherited (**levels**).
- Important build settings for beginners.
- Adding a new target.

---

## 1. Project vs Target vs Scheme

These three words confuse many beginners. Let's use a **restaurant** 🍽️:

| Xcode | Restaurant | Meaning |
|---|---|---|
| **Project** | The **restaurant** | Holds everything: all files, all recipes, all settings. |
| **Target** | One **dish** on the menu | One thing to build: the iPhone app, a widget, a test bundle… Each has its own recipe (settings). |
| **Scheme** | An **order** from a waiter | "Make **this dish**, **this way** (Debug or Release), and **do this** with it (run, test, archive)." |

> 📖 **New word: Project**
> The container for all your files and targets. The `.xcodeproj` file.

> 📖 **New word: Target**
> One product that Xcode builds from your project: an app, a widget, a test bundle, a watch app…

> 📖 **New word: Scheme**
> Instructions for building and running a target: which target, which configuration, what to do.

```
 📘 Project: HelloApp
    │
    ├── 🎯 Target: HelloApp            (the iPhone app)
    ├── 🎯 Target: HelloAppWidget      (a home screen widget)
    └── 🎯 Target: HelloAppTests       (tests)

 📜 Schemes:
    ├── HelloApp         → builds HelloApp, Run uses Debug
    └── HelloAppWidget   → builds the widget
```

A simple new project has **one** target and **one** scheme. That's normal.

---

## 2. Opening project and target settings

1. Click the **blue project icon** 📘 in the Project navigator.
2. The editor shows a list on the left:

```
┌──────────────┬──────────────────────────────────────────────┐
│ PROJECT      │ [General] [Signing & Capabilities] [Resource │
│  📘 HelloApp │  Tags] [Info] [Build Settings] [Build Phases]│
│              │ [Build Rules]                                │
│ TARGETS      │                                              │
│  🎯 HelloApp │   ... settings for the selected item ...     │
│              │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

| Click | You see |
|---|---|
| **PROJECT → HelloApp** | Settings for the **whole project** (configurations, project-level build settings). |
| **TARGETS → HelloApp** | Settings for **this app only**. You'll use this most. |

💡 **Tip:** If you don't see the list on the left, click the small sidebar button at the top-left of the editor.

---

## 3. Target tab: General

Select the **target** → **General** tab.

### Supported Destinations

Which devices can run your app:

```
│ Supported Destinations                       │
│   iPhone                                     │
│   iPad                                       │
│   Mac (Designed for iPad)                    │
│   Apple Vision (Designed for iPad)           │
│   [+] [-]                                    │
```

Click **−** to remove one (for example, iPad if your app is iPhone-only). Click **+** to add.

### Minimum Deployments ⭐

```
│ Minimum Deployments                          │
│   iOS   [ 17.0 ▾ ]                           │
```

> 📖 **New word: Deployment target (Minimum Deployment)**
> The **oldest** iOS version your app can run on. Phones with older iOS **can't install** your app.

| Lower number (e.g. 16.0) | Higher number (e.g. 18.0) |
|---|---|
| ✅ More people can install your app | ❌ Fewer people (only newer iOS) |
| ❌ You can't use the newest Swift/SwiftUI features easily | ✅ You can use the newest features |

💡 **Tip:** For learning, use the default Xcode gives you. For a real app, many developers support **the current iOS and one or two versions before it**.

If you use a feature that needs a newer iOS than your deployment target, Xcode shows an error like:

```
'someFeature' is only available in iOS 18.0 or newer
```

You can then check the version in code:

```swift
if #available(iOS 18, *) {
    // use the new feature
} else {
    // do something simpler for older iOS
}
```

| Part | Meaning |
|---|---|
| `#available(iOS 18, *)` | "Is this phone running iOS 18 or newer?" (`*` = "and any other platform"). |

### Identity

```
│ Identity                                     │
│   Display Name   [ Hello        ]            │
│   Bundle Identifier [ com.ravikumar.HelloApp]│
│   Version        [ 1.0 ]                     │
│   Build          [ 1   ]                     │
```

| Field | Meaning |
|---|---|
| **Display Name** | The name under the icon on the home screen. Can have spaces: "My Hello App". |
| **Bundle Identifier** | The app's unique ID (Chapter 33). |
| **Version** | The version **users see** in the App Store: `1.0`, `1.1`, `2.0`. Also called **Marketing Version**. |
| **Build** | An **internal** number. Must go **up** every time you upload to the App Store: `1`, `2`, `3`… |

> 📖 **New word: Version vs Build**
> **Version** = for people (1.0, 1.1). **Build** = for Apple's system; each upload of the same version needs a new, bigger build number.

### Deployment Info

```
│ Deployment Info                              │
│   iPhone Orientation  ☑ Portrait             │
│                       ☐ Upside Down          │
│                       ☑ Landscape Left       │
│                       ☑ Landscape Right      │
│   Status Bar Style    [ Default ▾ ]          │
```

Uncheck **Landscape Left/Right** if your app should only work standing up (portrait).

> 📖 **New word: Portrait / Landscape**
> **Portrait** = phone standing up ▯. **Landscape** = phone on its side ▭.

### Frameworks, Libraries, and Embedded Content

Lists extra code libraries your app uses. Empty for now.

---

## 4. Target tab: Signing & Capabilities

- **Signing**: which team signs your app. (Chapter 38 explains this in detail.)
- **Capabilities**: special permissions, like Push Notifications, iCloud, Sign in with Apple. Add them with **+ Capability**.

---

## 5. Target tab: Info

Shows the app's **Info.plist** values — information the system reads about your app. (Chapter 37 explains this in detail.)

---

## 6. Target tab: Build Settings ⭐

Hundreds of settings! Don't worry — you only need a few.

At the top:

```
│ [Basic] [Customized] [All]     [Combined] [Levels]    🔍 search │
```

| Button | Shows |
|---|---|
| **Basic** | The most common settings. |
| **Customized** | Only settings **you** (or the template) changed. |
| **All** | Every setting. |
| **Combined** | The final value for each setting. |
| **Levels** | Where each value comes from (see next section). |

💡 **Tip:** Always use the 🔍 **search box**. Don't scroll through hundreds of settings!

### Levels: where does a value come from?

Click **Levels**:

```
Setting                  Resolved   HelloApp(target)  HelloApp(project)  iOS Default
Swift Language Version   Swift 6    Swift 6                              Swift 5
```

Settings are **inherited**, and the **most specific** level wins:

```
  iOS Default   ← weakest (Apple's default)
      ▲
  Project       ← overrides the default, for all targets
      ▲
  Target        ← overrides the project, for this target only  ← strongest
      ▲
  Resolved      = the final value used
```

| Level | Meaning |
|---|---|
| **iOS Default** | Apple's default value. |
| **Project** | Value set at the project level. Used by **all** targets (unless they override). |
| **Target** | Value set for **this** target. Wins over the project. |
| **Resolved** | The **final** value Xcode uses. |

A value shown in **bold** means it was **changed** at that level.

To **reset** a setting to the inherited value: select it, press `Delete`.

### Important build settings for beginners

| Setting (search for…) | What it does |
|---|---|
| **Product Name** | Name of the built product. |
| **Product Bundle Identifier** | The Bundle ID (same as in General). |
| **iOS Deployment Target** | The minimum iOS (same as General → Minimum Deployments). |
| **Swift Language Version** | Swift 5 or Swift 6 mode. Swift 6 mode has stricter safety checks for concurrency. |
| **Strict Concurrency Checking** | How strict Swift is about `async` code safety: Minimal, Targeted, Complete. |
| **Optimization Level** | `-Onone` (Debug) / `-O` (Release) — Chapter 35. |
| **Active Compilation Conditions** | Flags like `DEBUG` for `#if` — Chapter 35. |
| **Marketing Version** | The **Version** (1.0). |
| **Current Project Version** | The **Build** number (1). |
| **Development Team** | The signing team. |

> 📖 **New word: Swift 6 language mode**
> A stricter mode that catches **data race** problems (two tasks changing the same data at the same time) when building. New projects may use it. If you see lots of concurrency warnings in an older project, this is why.

---

## 7. Target tab: Build Phases

The **steps** Xcode does to build your target, in order:

```
│ ▸ Target Dependencies          (0 items)     │
│ ▸ Compile Sources              (2 items)     │  ← your .swift files
│ ▸ Link Binary With Libraries   (0 items)     │
│ ▸ Copy Bundle Resources        (1 item)      │  ← images, assets
```

| Phase | Meaning |
|---|---|
| **Target Dependencies** | Other targets that must be built **first**. |
| **Compile Sources** | Swift files that get compiled into this target. |
| **Link Binary With Libraries** | Libraries/frameworks to include. |
| **Copy Bundle Resources** | Non-code files to copy into the app (images, sounds, JSON). |

💡 **Tip:** If a file "doesn't exist" when your app runs, check that it's in **Copy Bundle Resources** (or that its **Target Membership** is checked — see section 10).

You can add a **Run Script** phase with **+** (for example, to run a code-formatting tool). That's advanced.

---

## 8. Schemes in detail

The scheme menu is in the toolbar, **left** of the run destination:

```
  [ HelloApp ▾ ]  ›  📱 iPhone 16
       │
       ▼
  ┌───────────────────────┐
  │ ✓ HelloApp            │
  │   HelloAppWidget      │
  │ ───────────────────── │
  │ Edit Scheme...        │
  │ New Scheme...         │
  │ Manage Schemes...     │
  └───────────────────────┘
```

### Edit Scheme (`Cmd + <`)

```
┌────────────┬────────────────────────────────────────────────┐
│ ▶ Build    │ [Info] [Arguments] [Options] [Diagnostics]     │
│ ▶ Run    ◀ │                                                │
│ ▶ Test     │ Build Configuration: [ Debug ▾ ]               │
│ ▶ Profile  │                                                │
│ ▶ Analyze  │                                                │
│ ▶ Archive  │                                                │
└────────────┴────────────────────────────────────────────────┘
```

Each **action** on the left has its own settings. For **Run**:

| Tab | Useful settings |
|---|---|
| **Info** | **Build Configuration** (Debug/Release/Staging). |
| **Arguments** | **Environment Variables** and **Launch Arguments** — values your app can read at start (useful for testing). |
| **Options** | **App Language** and **App Region** — run the app in another language without changing the Simulator! Also: simulated **location**. |
| **Diagnostics** | Extra checkers: **Address Sanitizer**, **Thread Sanitizer**, **Main Thread Checker** — they help find hard bugs. |

💡 **Tip:** **Options → App Language** is great to test translations quickly. 🌍

### Reading an environment variable

In Edit Scheme → Run → Arguments → **Environment Variables**, click **+** and add:

| Name | Value |
|---|---|
| `USE_FAKE_DATA` | `YES` |

In code:

```swift
import Foundation

let useFakeData = ProcessInfo.processInfo.environment["USE_FAKE_DATA"] == "YES"
print("Use fake data:", useFakeData)
```

| Part | Meaning |
|---|---|
| `ProcessInfo.processInfo.environment` | A dictionary (Chapter 15) of all environment variables. |
| `["USE_FAKE_DATA"]` | Read one. It's an Optional (might not exist). |
| `== "YES"` | Compare to get a `Bool`. |

⚠️ **Careful:** Environment variables from the scheme only exist when you run **from Xcode**. Not when users open the app. Use them for testing only.

### New Scheme / Duplicate

- **Manage Schemes…** → select a scheme → **gear ⚙️ → Duplicate**. Rename it, e.g. "HelloApp Staging", and set **Run → Build Configuration → Staging**.
- ✅ **Shared** checkbox: share the scheme with your team through Git.

---

## 9. Adding a new target

Example: adding a **Widget** (a small view on the home screen).

1. **File → New → Target…**
2. Choose **iOS** → **Widget Extension**.
3. Name it, for example `HelloWidget`. Click **Finish**.
4. Xcode may ask: *"Activate 'HelloWidget' scheme?"* Click **Activate** (or **Cancel** to stay on your app's scheme).

Now you have:
- A new **target** `HelloWidget` with its own files.
- A new **scheme** `HelloWidget`.

Other targets you might add one day:

| Target | For |
|---|---|
| **Unit Testing Bundle** | Tests for your code (Chapter 64). |
| **UI Testing Bundle** | Tests that tap through your app automatically. |
| **Widget Extension** | Home screen / lock screen widgets. |
| **watchOS App** | An Apple Watch version. |
| **App Intents / Share Extension** | Siri shortcuts, the share menu, etc. |

---

## 10. Target Membership — which target uses a file?

Each file can belong to **one or more** targets.

1. Select a file in the Project navigator.
2. Open the **File inspector** (`Cmd + Option + 1`).
3. Look at **Target Membership**:

```
│ Target Membership         │
│   ☑ 🎯 HelloApp           │
│   ☐ 🎯 HelloWidget        │
```

✅ = this file is compiled into that target.

⚠️ **Common error:** `Cannot find 'MyType' in scope` — even though the file exists! Often the file's **Target Membership** is not checked for the target you're building. Check the box ✅.

---

## 11. Quick map 🗺️

```
📘 PROJECT  ──► Info: Configurations (Debug/Release/Staging)
   │          Build Settings (shared defaults for all targets)
   │
   └─ 🎯 TARGET ──► General          (name, version, devices, min iOS)
                    Signing & Capab. (team, permissions)
                    Info             (Info.plist values)
                    Build Settings   (overrides, wins over project)
                    Build Phases     (compile, link, copy resources)

📜 SCHEME ──► Build / Run / Test / Profile / Analyze / Archive
               └─ each picks a Build Configuration + options
```

---

## 🏋️ Practice

1. Open your target's **General** tab. Change the **Display Name** to something with spaces, like "About Me". Run the app and look at the name on the Simulator's home screen.
2. Change **Version** to `1.1` and **Build** to `2`.
3. Uncheck **Landscape Left** and **Landscape Right**. Run the app and rotate the Simulator. What happens?
4. In **Build Settings**, search for **Swift Language Version**. Use **Levels** to see where its value comes from.
5. In **Edit Scheme → Run → Options**, change **App Language** to another language. Run and see the system texts change.
6. Add an environment variable `GREETING = Namaste` to the scheme, and show it in a `Text` using `ProcessInfo`.

---

## 🧠 Remember

- **Project** = everything. **Target** = one product to build. **Scheme** = how to build/run it.
- **General**: display name, Bundle ID, **Version** (for people), **Build** (must increase), **Minimum Deployments**, orientations.
- **Build Settings**: use search. **Target** level wins over **Project** level.
- **Edit Scheme** (`Cmd + <`): configuration, environment variables, app language, diagnostics.
- If a type "can't be found", check **Target Membership**.

---

⬅️ **Back:** [Chapter 35 — Debug vs Release](35-debug-vs-release.md)
➡️ **Next:** [Chapter 37 — Info.plist, App Icons and Launch Screen](37-info-plist-icons-launch.md)
