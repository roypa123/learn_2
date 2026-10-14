# Chapter 37 — Info.plist, App Icons and Launch Screen

🍎 **Needs a Mac**

---

## What you will learn

- What **Info.plist** is and where to find it.
- **Privacy permission messages** (camera, photos, location…) — very important!
- Adding an **app icon**.
- The **Accent Color**.
- The **launch screen** (the first screen while the app loads).
- Adding images and colors to the **Asset Catalog**.

---

## 1. What is Info.plist?

Every app has an **information card** 🪪 that iOS reads **before** the app even starts:

- What's the app's name?
- What's its version?
- Which orientations does it support?
- What should we tell the user when the app asks for the camera?

This card is called **Info.plist**.

> 📖 **New word: Info.plist**
> A file with **key–value** information about your app (like a dictionary — Chapter 15). "plist" = **p**roperty **list**.

> 📖 **New word: Key**
> The name of one piece of information, like `CFBundleDisplayName` (the display name).

---

## 2. Where is it?

In modern Xcode projects, you may **not** see an `Info.plist` file in the Project navigator! Many values are stored in **Build Settings** instead.

To see and edit them:

1. Click the project 📘 → select your **target**.
2. Click the **Info** tab.

```
┌──────────────────────────────────────────────────────────────┐
│ Custom iOS Target Properties                                 │
│  Key                                   Type        Value     │
│  Bundle display name                   String      Hello     │
│  Bundle identifier                     String      $(PRODUCT…│
│  Bundle version                        String      $(CURRENT…│
│  Launch Screen                         Dictionary  (1 item)  │
│  Supported interface orientations      Array       (3 items) │
│  ...                                                [+]      │
└──────────────────────────────────────────────────────────────┘
```

| Column | Meaning |
|---|---|
| **Key** | The name. Xcode shows a friendly name (like "Bundle display name"). |
| **Type** | `String`, `Boolean`, `Number`, `Array`, `Dictionary` — the same types you know from Swift! |
| **Value** | The value. `$(SOMETHING)` means "use the build setting called SOMETHING" (Chapter 35). |

💡 **Tip:** **Right-click** the list → **Raw Keys & Values** to see the real key names (like `CFBundleDisplayName`). Do it again to switch back.

### Adding a new key

- Hover over any row → click the small **+** button.
- Start typing the name — Xcode suggests keys. Choose one.
- Set the value.

---

## 3. Privacy permission messages ⭐⭐⭐

This is the **most important** part of Info.plist for beginners.

When your app wants to use **private things** — camera, photos, location, microphone, contacts — iOS asks the user:

```
┌──────────────────────────────────────┐
│  "HelloApp" Would Like to Access     │
│  the Camera                          │
│                                      │
│  We use the camera so you can take   │  ← YOUR message
│  a profile picture.                  │
│                                      │
│    [ Don't Allow ]     [ Allow ]     │
└──────────────────────────────────────┘
```

**You** must write that message in Info.plist.

⚠️ **VERY Careful:** If your app uses the camera (or photos, location…) **without** this message, the app **crashes immediately** when it tries! 💥 Apple will also **reject** the app from the App Store.

> 📖 **New word: Usage description**
> The message that explains **why** your app needs a permission. Each permission has its own key.

### Common privacy keys

| Feature | Friendly name in Xcode | Raw key |
|---|---|---|
| 📷 Camera | Privacy - Camera Usage Description | `NSCameraUsageDescription` |
| 🖼️ Photo library (read) | Privacy - Photo Library Usage Description | `NSPhotoLibraryUsageDescription` |
| 🖼️ Save photos only | Privacy - Photo Library Additions Usage Description | `NSPhotoLibraryAddUsageDescription` |
| 🎤 Microphone | Privacy - Microphone Usage Description | `NSMicrophoneUsageDescription` |
| 📍 Location (while using) | Privacy - Location When In Use Usage Description | `NSLocationWhenInUseUsageDescription` |
| 👥 Contacts | Privacy - Contacts Usage Description | `NSContactsUsageDescription` |
| 📅 Calendar | Privacy - Calendars Full Access Usage Description | `NSCalendarsFullAccessUsageDescription` |
| 🔐 Face ID | Privacy - Face ID Usage Description | `NSFaceIDUsageDescription` |
| 🔵 Bluetooth | Privacy - Bluetooth Always Usage Description | `NSBluetoothAlwaysUsageDescription` |

### How to add one

1. Target → **Info** tab.
2. Hover a row → click **+**.
3. Type `Privacy - Camera` and choose **Privacy - Camera Usage Description**.
4. In **Value**, type a clear, honest message:

```
We use the camera so you can take a profile picture.
```

### Writing good messages ✍️

| ❌ Bad | ✅ Good |
|---|---|
| "Camera needed." | "We use the camera so you can scan QR codes on tickets." |
| "This app needs your location." | "Your location is used to show restaurants near you." |
| (empty) | Explain the **real reason**, in simple words. |

🧠 **Remember:** Using a private feature? → Add its **usage description** first. Always.

💡 **Tip:** Some features (like the SwiftUI `PhotosPicker` for choosing photos) **don't** need a permission, because the user picks photos in a safe system window. Apple's documentation for each feature tells you if a key is needed.

---

## 4. The Asset Catalog 🎨

Click **Assets** in the Project navigator.

```
┌──────────────┬─────────────────────────────────┐
│ AccentColor  │                                 │
│ AppIcon      │     (the selected item          │
│              │      appears here)              │
│              │                                 │
│ [+]          │                                 │
└──────────────┴─────────────────────────────────┘
```

> 📖 **New word: Asset Catalog**
> A special folder (`Assets.xcassets`) that organizes your app's images, colors and icons.

| Item | Meaning |
|---|---|
| **AccentColor** | The app's main color for buttons, links, toggles. |
| **AppIcon** | The icon on the home screen. |
| **[+]** (bottom) | Add a new image set, color set, etc. |

---

## 5. Adding the app icon 📱

### What you need

- **One** square image, **1024 × 1024 pixels**, **PNG** format.
- **No** transparent background (iOS doesn't allow transparency in app icons).
- **No** rounded corners — iOS adds them automatically.

> 📖 **New word: Pixel**
> One tiny dot of color on a screen. A 1024 × 1024 image has 1024 dots across and 1024 dots down.

💡 **Tip:** No design skills? Make a simple icon: one big emoji or letter on a colored square. Free tools like Canva or Figma can export 1024×1024 PNG files. (You can even make one on Windows and send it to the Mac!)

### Steps

1. Click **Assets** → **AppIcon**.
2. You'll see an empty square (or a few squares for **Any Appearance**, **Dark** and **Tinted**).

```
┌─────────────────────────────────────────────┐
│ AppIcon                                     │
│                                             │
│   ┌───────┐   ┌───────┐   ┌───────┐         │
│   │       │   │       │   │       │         │
│   │ Drop  │   │ Dark  │   │Tinted │         │
│   └───────┘   └───────┘   └───────┘         │
│     Any         Dark        Tinted          │
│                                             │
│   iOS  1024pt                               │
└─────────────────────────────────────────────┘
```

3. **Drag** your 1024×1024 PNG from Finder onto the **Any Appearance** square.
4. (Optional) Drag a dark version onto **Dark**, and a gray/white version onto **Tinted**.
5. Run the app (`Cmd + R`), then press `Cmd + Shift + H` in the Simulator to see your icon on the home screen. 🎉

| Square | When iOS uses it |
|---|---|
| **Any Appearance** | Normal (light) home screen. Required. |
| **Dark** | When the user chooses dark icons. Optional. |
| **Tinted** | When the user chooses tinted (one color) icons. Optional. |

⚠️ **Careful:** If the icon doesn't change in the Simulator, delete the app from the Simulator and run again. iOS sometimes remembers the old icon.

💡 **Tip:** Newer Xcode versions also include **Icon Composer**, an Apple tool for making layered icons with glass-like effects. It's optional — a simple 1024×1024 PNG always works.

---

## 6. Accent Color

1. Click **Assets** → **AccentColor**.
2. Click the color square in the middle.
3. Open the **Attributes inspector** (`Cmd + Option + 4`).
4. Under **Color**, choose **Content: sRGB** and pick a color with the sliders, or type a **Hex** value like `#FF6B00` (orange).

Now buttons, toggles and links in your app use this color automatically!

```swift
Button("Tap me") { }        // uses the accent color
Text("Hi").foregroundStyle(.tint)   // .tint = the accent color
```

### Different color in dark mode

In the Attributes inspector, set **Appearances** to **Any, Dark**. Now you get **two** squares — choose a different color for dark mode. 🌙

---

## 7. Adding your own images 🖼️

1. Click **Assets**.
2. **Drag** an image file (PNG or JPG) from Finder into the left list. Or click **+** → **Image Set**.
3. Rename it to something simple, like `logo` (small letters, no spaces).

You'll see three boxes: **1x**, **2x**, **3x**.

> 📖 **New word: 1x, 2x, 3x**
> Different sizes for different screen qualities. Modern iPhones use **2x** or **3x**.

💡 **Tip:** The easiest way: in the **Attributes inspector**, set **Scales** to **Single Scale**, then use **one** big image (or better, a **PDF** or **SVG** vector image with **Preserve Vector Data** ✅). It looks sharp on every phone.

### Using it in SwiftUI

```swift
Image("logo")
    .resizable()
    .scaledToFit()
    .frame(width: 120)
```

| Part | Meaning |
|---|---|
| `Image("logo")` | Show the image named `logo` from the Asset Catalog. The name must match **exactly**. |
| `.resizable()` | Allow the image to change size. |
| `.scaledToFit()` | Keep its shape (don't stretch). |
| `.frame(width: 120)` | Make it 120 points wide. |

(Part 5 explains images in detail.)

⚠️ **Careful:** `Image("Logo")` ≠ `Image("logo")`. Names are **case-sensitive** (like Swift — Chapter 3).

### Adding your own colors

1. Assets → **+** → **Color Set**. Name it `BrandBlue`.
2. Pick the color in the Attributes inspector.

```swift
Text("Hello")
    .foregroundStyle(Color("BrandBlue"))
```

Newer Xcode versions can also create Swift names automatically, so you can write `Color.brandBlue` or `.brandBlue` (with autocomplete!). If that works in your Xcode, it's safer than typing the name as a string.

---

## 8. The launch screen 🚀

When a user taps your app, iOS shows a **launch screen** for a moment while the app loads.

> 📖 **New word: Launch screen**
> A simple screen shown **while the app starts**. It should look like the first screen of your app, without text that changes.

In SwiftUI projects, the launch screen is set in **Info → Launch Screen**:

1. Target → **Info** tab.
2. Find **Launch Screen** (a Dictionary). Open it with the ▸ arrow.
3. Click **+** inside it to add keys:

| Key (friendly name) | Value | Effect |
|---|---|---|
| **Background color** | `LaunchBackground` (a Color Set name from Assets) | The background color. |
| **Image Name** | `logo` (an Image Set name from Assets) | An image in the center. |
| **Image respects safe area insets** | `YES` / `NO` | Keep the image away from the notch/edges. |

### Example

1. Assets → **+** → **Color Set** → name it `LaunchBackground` → choose a color.
2. Assets → add an image named `logo`.
3. Info → Launch Screen → add **Background color** = `LaunchBackground`, **Image Name** = `logo`.
4. Run the app. You'll see your logo on your color for a moment! ✨

⚠️ **Careful:** The launch screen should be **simple**:
- ❌ No "Loading…" text, no ads, no animations.
- ✅ A color, maybe a logo.

Apple wants the app to *feel* fast — the launch screen should look like the app is already opening.

💡 **Tip:** The launch screen is **cached** by iOS. If your changes don't appear, delete the app from the Simulator and run again.

---

## 9. Other useful Info.plist keys

| Friendly name | Raw key | What it does |
|---|---|---|
| Bundle display name | `CFBundleDisplayName` | Name under the icon. |
| Supported interface orientations | `UISupportedInterfaceOrientations` | Allowed rotations. |
| Appearance | `UIUserInterfaceStyle` | Set to `Light` to **force** light mode (not recommended — users like dark mode!). |
| App Transport Security Settings | `NSAppTransportSecurity` | Rules for internet connections. iOS requires **HTTPS** by default. |
| Required background modes | `UIBackgroundModes` | Let the app do things in the background (audio, location…). Usually added through **Signing & Capabilities → + Capability → Background Modes**. |
| URL types | `CFBundleURLTypes` | Let other apps open yours with a link like `myapp://`. |

> 📖 **New word: HTTPS**
> A **secure** way to talk to websites. The `s` means "secure" 🔒. iOS blocks plain `http://` by default.

---

## 🏋️ Practice

1. Open your target's **Info** tab. Right-click → **Raw Keys & Values**. Find `CFBundleDisplayName` (if present). Switch back.
2. Add **Privacy - Camera Usage Description** with a good, honest message.
3. Make a simple 1024×1024 PNG icon (an emoji on a colored background is fine) and add it to **AppIcon**. See it on the Simulator home screen.
4. Change the **AccentColor** to your favorite color. Add a `Button("Hello") { }` to your screen and see its color.
5. Add an image to Assets and show it with `Image("yourName").resizable().scaledToFit()`.
6. Set up a launch screen with a background color and your image.

---

## 🧠 Remember

- **Info.plist** = the app's information card. Edit it in **Target → Info**.
- Using camera, photos, location, mic…? Add the **Privacy - … Usage Description** key, or the app **crashes**.
- App icon: **one 1024×1024 PNG**, no transparency, no rounded corners → **Assets → AppIcon**.
- **AccentColor** = the app's main color.
- Images: drag into **Assets**, use with `Image("name")`.
- Launch screen: **Info → Launch Screen** → background color + image. Keep it simple.

---

⬅️ **Back:** [Chapter 36 — Targets, Schemes and Build Settings](36-targets-schemes-build-settings.md)
➡️ **Next:** [Chapter 38 — Signing, Certificates and Bundle IDs](38-signing-certificates.md)
