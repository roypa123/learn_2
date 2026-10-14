# Chapter 31 — Installing Xcode

🍎 **Needs a Mac** (or a cloud Mac).

---

## What you will learn

- What you need before installing.
- Two ways to install Xcode.
- What happens the first time you open Xcode.
- Installing Simulators (pretend iPhones).
- Command Line Tools.
- Common install problems and fixes.

---

## 1. Before you start ✅

Check these things first:

| Check | How |
|---|---|
| **macOS is up to date** | Click the Apple menu  (top-left) → **System Settings** → **General** → **Software Update**. New Xcode often needs the newest macOS. |
| **Free space: 40 GB or more** | Apple menu  → **About This Mac** → **More Info** → **Storage**. |
| **Apple ID** | You need one to download from the App Store. |
| **Good internet** | Xcode is a very big download (many GB). |
| **Power** | If it's a laptop, plug it in. The install takes a long time. |

> 📖 **New word: Apple menu **
> The small Apple logo in the top-left corner of the Mac screen. It has system options.

---

## 2. Way 1: Mac App Store (easiest) ⭐

1. Click the **Launchpad** 🚀 or press `Cmd + Space` and type **App Store**. Press `Enter`.
2. In the App Store, click the **search** box. Type **Xcode**.
3. Find **Xcode** (by Apple, blue icon with a hammer 🔨).
4. Click **Get**, then **Install**.
5. Type your Apple ID password if asked.
6. **Wait.** ☕ This can take 30 minutes to a few hours.

> 📖 **New word: `Cmd` key**
> The **Command** key ⌘ on a Mac keyboard. It's like `Ctrl` on Windows. `Cmd + Space` opens **Spotlight** search.

💡 **Tip:** The progress bar may stay at "almost done" for a long time while it unpacks. That's normal. Don't cancel!

---

## 3. Way 2: Apple Developer website (for specific versions)

Sometimes you need a **specific** (older or beta) version.

1. Go to **developer.apple.com/download** (or search "Xcode download Apple developer").
2. Sign in with your Apple ID.
3. Download the **`.xip`** file for the version you want.
4. Double-click the `.xip` file. It unpacks into **Xcode.app**. (This is slow.)
5. Drag **Xcode.app** into your **Applications** folder.

> 📖 **New word: Beta**
> A test version that is not finished yet. It may have bugs. Beginners should use the normal (stable) version.

| | App Store | Developer website |
|---|---|---|
| Easy? | ✅ Very | Medium |
| Automatic updates? | ✅ Yes | ❌ No |
| Choose the version? | ❌ Latest only | ✅ Any |
| Best for | Beginners | Advanced users |

🧠 **Remember:** As a beginner, use the **App Store** version.

---

## 4. Opening Xcode for the first time

1. Open **Applications** (in Finder) and double-click **Xcode**. Or press `Cmd + Space`, type **Xcode**, press `Enter`.
2. Xcode may ask for your **Mac password** to install extra **components**. Type it and click **OK**.
3. A window asks which **platforms** to download.

```
┌──────────────────────────────────────────────┐
│  Select the platforms you want to develop for │
│                                              │
│   ☑ macOS       (built in)                   │
│   ☑ iOS         ⬇ download                   │
│   ☐ watchOS                                  │
│   ☐ tvOS                                     │
│   ☐ visionOS                                 │
│                                              │
│                 [ Download & Install ]       │
└──────────────────────────────────────────────┘
```

4. Make sure **iOS** is selected. ✅ (You can skip the others for now — they're big.)
5. Click **Download & Install**. Wait again. ☕

> 📖 **New word: Platform**
> A type of Apple device: iOS (iPhone), iPadOS (iPad), macOS (Mac), watchOS (Apple Watch), tvOS (Apple TV), visionOS (Apple Vision Pro).

> 📖 **New word: Component**
> An extra piece of software that Xcode needs, like the iOS Simulator.

⚠️ **Careful:** The window design can look a little different in each Xcode version. Look for **iOS** and a download button.

---

## 5. The Welcome window 👋

After everything installs, you'll see the **Welcome to Xcode** window:

```
┌────────────────────────────────────────────────────────────┐
│                                       │  Recent projects    │
│         🔨  Welcome to Xcode          │                     │
│            Version XX.X               │  (empty for now)    │
│                                       │                     │
│   ➕ Create New Project...             │                     │
│   ⬇️ Clone Git Repository...            │                     │
│   📂 Open Existing Project...          │                     │
│                                       │                     │
└────────────────────────────────────────────────────────────┘
```

| Button | What it does |
|---|---|
| **Create New Project…** | Start a new app. (We'll do this in Chapter 33.) |
| **Clone Git Repository…** | Download a project from GitHub (or similar). |
| **Open Existing Project…** | Open a project already on your Mac. |
| **Recent projects** (right side) | Your last opened projects. Double-click to open. |

💡 **Tip:** If you close this window, open it again with **Window → Welcome to Xcode** (or `Cmd + Shift + 1`).

---

## 6. Checking your Simulators

Simulators are pretend iPhones on your screen (Chapter 34).

1. In Xcode's top menu, click **Xcode → Settings…** (shortcut: `Cmd + ,`).
2. Click the **Components** tab (in some versions it's called **Platforms**).
3. You'll see the installed platforms, like **iOS XX.X Simulator**.
4. If iOS is missing, click **Get** or the **+** button to download it.

To see the list of Simulator devices:

1. Top menu: **Window → Devices and Simulators** (`Cmd + Shift + 2`).
2. Click the **Simulators** tab.
3. You'll see iPhones and iPads you can use.

---

## 7. Signing in to your Apple ID in Xcode

This is needed later for running apps on a real iPhone (Chapter 38–39).

1. **Xcode → Settings…** (`Cmd + ,`).
2. Click the **Accounts** tab.
3. Click the **+** button in the bottom-left.
4. Choose **Apple ID** → **Continue**.
5. Type your Apple ID email and password.

Now you'll see your name with a **team** like *"Your Name (Personal Team)"*.

> 📖 **New word: Team**
> In Xcode, a **team** is the account that "owns" your apps. A free Apple ID gives you a **Personal Team**.

---

## 8. Command Line Tools (useful extra)

Some tools (like `git` and `swift` in the Terminal) come with Xcode's **Command Line Tools**.

> 📖 **New word: Terminal**
> An app where you type text commands instead of clicking. Find it with `Cmd + Space` → type **Terminal**.

To check they're ready, open **Terminal** and type:

```bash
xcode-select -p
```

| Part | Meaning |
|---|---|
| `xcode-select` | A tool that says which Xcode the command line uses. |
| `-p` | "**P**rint the path." |

**Good output:**

```
/Applications/Xcode.app/Contents/Developer
```

If it shows something else, or an error, run:

```bash
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
```

| Part | Meaning |
|---|---|
| `sudo` | "Run as administrator." It asks for your Mac password. (You won't see the letters while typing — that's normal!) |
| `-s` | "**S**et the path to…" |

You can also test Swift in the Terminal:

```bash
swift --version
```

**Output (example):**

```
swift-driver version: ... Apple Swift version 6.x ...
```

---

## 9. Updating Xcode

- **App Store version:** Open the App Store → **Updates**. Xcode updates show there.
- Each new Xcode brings new iOS versions, new Swift features and bug fixes.

⚠️ **Careful:** Don't update Xcode in the middle of an important deadline. Updates are big and sometimes change things. Update when you have time.

---

## 10. Common problems and fixes 🔧

| Problem | Fix |
|---|---|
| "Xcode can't be installed — requires macOS XX or later" | Update macOS first (System Settings → General → Software Update). If your Mac is too old for the newest macOS, download an **older** Xcode from the developer website. |
| "Not enough disk space" | Delete big files you don't need. Empty the Trash. Xcode needs extra space **while** installing. |
| Download stuck at 0% or very slow | Check your internet. Restart the App Store app. Try again later. |
| Unpacking `.xip` takes forever | It's normal! It can take 20+ minutes. |
| Simulator missing | Xcode → Settings → Components → download iOS. |
| `xcode-select` error | Run the `sudo xcode-select -s ...` command from section 8. |

---

## 🏋️ Practice

1. Install Xcode (from the App Store).
2. Open it and install the **iOS** platform.
3. Open **Window → Devices and Simulators** and look at the list of Simulators.
4. Add your Apple ID in **Xcode → Settings → Accounts**.
5. Open **Terminal** and run `swift --version`. Write down your Swift version.

---

## 🧠 Remember

- Update macOS and free **40 GB+** before installing.
- Easiest way: **Mac App Store** → search **Xcode** → Get.
- First launch: install the **iOS** platform.
- Add your Apple ID: **Xcode → Settings → Accounts**.
- `Cmd + ,` opens Settings. `Cmd + Space` opens Spotlight search.

---

⬅️ **Back:** [Chapter 30 — Options When You Don't Own a Mac](30-options-without-a-mac.md)
➡️ **Next:** [Chapter 32 — A Tour of Xcode](32-xcode-tour.md)
