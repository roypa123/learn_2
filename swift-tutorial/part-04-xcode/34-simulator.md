# Chapter 34 — The Simulator: A Fake iPhone on Your Screen

🍎 **Needs a Mac**

---

## What you will learn

- What the **Simulator** is (and what it can't do).
- Choosing different iPhones and iPads.
- Using the Simulator with mouse and keyboard.
- Rotating, dark mode, text size, location.
- Taking screenshots and recordings.
- Adding new Simulators and fixing common problems.

---

## 1. What is the Simulator?

> 📖 **New word: Simulator**
> A program on your Mac that **acts like** an iPhone or iPad. You can run and test your app without a real device.

```
   Your Mac screen
 ┌────────────────────────────┐
 │  Xcode        ┌────────┐   │
 │               │ ▢▢▢▢▢▢ │   │
 │               │  Your  │   │  ← Simulator window
 │               │  App   │   │
 │               │        │   │
 │               └────────┘   │
 └────────────────────────────┘
```

| ✅ The Simulator CAN | ❌ The Simulator CANNOT (well) |
|---|---|
| Run your app on many iPhone/iPad models | Use the real camera 📷 |
| Show dark mode, big text, rotation | Feel exactly as fast/slow as a real device |
| Pretend a GPS location 📍 | Use some sensors (like real motion) |
| Take screenshots and videos | Make phone calls |
| Test notifications (partly) | Replace testing on a real device before launch |

🧠 **Remember:** The Simulator is great for **daily** work. Before publishing, test on a **real** iPhone too (Chapter 39).

---

## 2. Choosing a Simulator

In Xcode's toolbar, click the **run destination**:

```
  HelloApp  ›  📱 iPhone 16  ▾
                    │
                    ▼
  ┌─────────────────────────────┐
  │ iOS Device                  │
  │   Any iOS Device (arm64)    │
  │ iOS Simulators              │
  │   iPhone SE (3rd gen)       │  ← small screen
  │   iPhone 16                 │  ← normal
  │   iPhone 16 Pro Max         │  ← big screen
  │   iPad (A16)                │  ← tablet
  │   ...                       │
  │ Manage Run Destinations...  │
  └─────────────────────────────┘
```

Pick one and press `Cmd + R`.

💡 **Tip:** Test on a **small** iPhone (like iPhone SE) **and** a **big** one (Pro Max). Text that fits on a big screen may not fit on a small one!

(The model names in your list depend on your Xcode version.)

---

## 3. Using the Simulator

| On a real iPhone | In the Simulator |
|---|---|
| Tap | **Click** |
| Swipe / scroll | **Click and drag** (or scroll with the trackpad) |
| Pinch to zoom | Hold **`Option`** ⌥ and drag (two gray dots appear) |
| Type | Use your Mac **keyboard** |
| Home (go to home screen) | `Cmd + Shift + H` |
| Lock screen | `Cmd + L` |
| Open the app switcher | `Cmd + Shift + H` **twice** quickly |

---

## 4. The Simulator menu bar

When the Simulator window is active, the top menu bar shows its own menus.

### Device menu

| Item | What it does | Shortcut |
|---|---|---|
| **Rotate Left / Right** | Turn the phone sideways ↔ | `Cmd + ←` / `Cmd + →` |
| **Home** | Go to home screen | `Cmd + Shift + H` |
| **Lock** | Lock screen | `Cmd + L` |
| **Shake** | Pretend to shake the phone | `Ctrl + Cmd + Z` |
| **Erase All Content and Settings…** | Reset the Simulator like a new phone | |
| **Restart** | Restart the pretend phone | |

### I/O menu (Input/Output)

| Item | What it does |
|---|---|
| **Keyboard → Toggle Software Keyboard** (`Cmd + K`) | Show/hide the on-screen keyboard. |
| **Keyboard → Connect Hardware Keyboard** (`Cmd + Shift + K`) | Use the Mac keyboard directly (on/off). |

💡 **Tip:** If you tap a text field and **no keyboard** appears, it's because the Mac keyboard is connected. Press `Cmd + K` to show the on-screen keyboard.

### Features menu

| Item | What it does |
|---|---|
| **Toggle Appearance** (`Cmd + Shift + A`) | Switch **Light** ☀️ / **Dark** 🌙 mode. |
| **Location** | Pretend to be somewhere: Apple, City Run, Freeway Drive, or **Custom Location…** (type a latitude/longitude). |
| **Face ID / Touch ID** | Pretend to enroll and use Face ID ("Matching Face" / "Non-matching Face"). |
| **Increase / Decrease Preferred Text Size** | Test big and small text. |
| **Trigger Screenshot** | Take a screenshot inside the pretend phone. |

### File menu

| Item | What it does | Shortcut |
|---|---|---|
| **Save Screen** | Save a screenshot to your Mac's Desktop. | `Cmd + S` |
| **Record Screen** | Record a video of the Simulator. | `Cmd + R` (in Simulator) |

⚠️ **Careful:** `Cmd + R` means **Run** in Xcode, but **Record** in the Simulator. Make sure the right window is active!

### Window menu

| Item | What it does |
|---|---|
| **Physical Size** (`Cmd + 1`) | Same size as a real phone. |
| **Point Accurate** (`Cmd + 2`) | One point = one pixel on your screen. |
| **Fit Screen** (`Cmd + 3`) | Fit inside your Mac's screen. |

> 📖 **New word: Point**
> The unit iOS uses to measure size on screen. On high-quality screens, one point is made of 2 or 3 tiny pixels.

---

## 5. Test these 5 things on every screen ✅

Every time you build a screen, quickly check:

| Test | How |
|---|---|
| 1. Dark mode 🌙 | `Cmd + Shift + A` |
| 2. Rotate ↔ | `Cmd + ←` |
| 3. Small phone 📱 | Change the run destination to a small iPhone. |
| 4. Big text 🔠 | Features → Increase Preferred Text Size (several times). |
| 5. Keyboard ⌨️ | Tap text fields, check the keyboard doesn't hide important things. |

💡 **Tip:** You can also check dark mode and other variants right in the **Canvas** using the **Variants** button at the bottom of the preview. Faster than running!

---

## 6. Changing settings inside the Simulator

The Simulator has a **Settings** app, just like a real iPhone.

1. Press `Cmd + Shift + H` to go home.
2. Open **Settings** ⚙️.

Useful things to try:
- **General → Language & Region** — test your app in another language.
- **Accessibility → Display & Text Size** — bold text, bigger text.
- **Developer** — extra options for developers.

---

## 7. Deleting your app from the Simulator

Sometimes you want a **fresh start** (for example, to delete saved data).

1. Go to the home screen (`Cmd + Shift + H`).
2. **Click and hold** your app's icon.
3. Choose **Remove App** → **Delete App**.

Or reset everything: **Device → Erase All Content and Settings…**

---

## 8. Opening files and photos in the Simulator

- **Drag** an image from Finder onto the Simulator window → it goes into the **Photos** app.
- **Drag** a link (URL) onto it → it opens in Safari.

This is useful when testing an app that picks photos. 🖼️

---

## 9. Adding more Simulators

1. In Xcode: **Window → Devices and Simulators** (`Cmd + Shift + 2`).
2. Click the **Simulators** tab.
3. Click **+** at the bottom-left.
4. Choose a **Device Type** (for example, iPhone SE) and an **OS Version**.
5. Click **Create**.

To get **older iOS versions**: **Xcode → Settings → Components** → download the iOS version you need.

---

## 10. Common problems and fixes 🔧

| Problem | Fix |
|---|---|
| Simulator is very slow the first time | Normal — it's "booting". Wait. Next time is faster. |
| App shows an old version | Stop (`Cmd + .`) and run again. If still old, delete the app from the Simulator, then run. |
| No keyboard when typing | `Cmd + K` in the Simulator. |
| Simulator window is too big | **Window → Fit Screen** (`Cmd + 3`). |
| "Unable to boot device" | Quit the Simulator app. In Xcode: Devices and Simulators → right-click the device → **Erase All Content and Settings**. Or restart your Mac. |
| No Simulators in the list | Xcode → Settings → Components → download iOS. |
| Uses too much disk space | In Terminal, run `xcrun simctl delete unavailable` to remove old, unusable Simulators. |

> 📖 **New word: `xcrun simctl`**
> A command-line tool to control Simulators from the Terminal. You don't need it often.

---

## 🏋️ Practice

1. Run your `AboutMe` app (Chapter 33) on **3 different** Simulators: a small iPhone, a big iPhone and an iPad.
2. Switch to **dark mode**. Does your app still look good?
3. **Rotate** the Simulator. What happens to your layout?
4. Make the text size **much bigger**. Does everything still fit?
5. Take a **screenshot** (`Cmd + S`) and find it on your Desktop.
6. Delete your app from the Simulator, then run it again.

---

## 🧠 Remember

- The **Simulator** is a pretend iPhone/iPad on your Mac.
- Choose the device in Xcode's **run destination** menu.
- `Cmd + Shift + H` = Home. `Cmd + ←/→` = rotate. `Cmd + Shift + A` = dark mode. `Cmd + K` = keyboard. `Cmd + S` = screenshot.
- Test: dark mode, rotation, small phone, big text, keyboard.
- Always test on a **real device** before publishing.

---

⬅️ **Back:** [Chapter 33 — Your First Xcode Project](33-first-xcode-project.md)
➡️ **Next:** [Chapter 35 — Xcode Configurations: Debug vs Release](35-debug-vs-release.md)
