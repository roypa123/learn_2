# Chapter 39 — Running on a Real iPhone

🍎 **Needs a Mac** (a real Mac — this is very hard or impossible with a cloud Mac) and an **iPhone**.

---

## What you will learn

- What you need.
- Connecting your iPhone with a cable.
- Turning on **Developer Mode**.
- Trusting the computer and the developer.
- Running wirelessly (no cable).
- Fixing common problems.

💡 **Tip:** No iPhone? No problem — you can keep learning with the Simulator. Read this chapter so you know the steps for later.

---

## 1. What you need ✅

| Thing | Notes |
|---|---|
| A **Mac** with Xcode | Chapter 31. |
| An **iPhone** (or iPad) | With an iOS version that your Xcode supports. Newer Xcode supports newer iOS. |
| A **cable** | USB-C or Lightning, depending on your iPhone and Mac. Use a **data** cable — some cheap cables only charge! |
| A **free Apple ID** added to Xcode | Chapter 38. |
| Your project with a **Team** selected | Signing & Capabilities → Team (Chapter 38). |

⚠️ **Careful:** If your iPhone's iOS is **newer** than your Xcode supports, Xcode can't run apps on it. **Update Xcode** first.

---

## 2. Step 1: Connect the iPhone

1. **Unlock** your iPhone.
2. Connect it to the Mac with the cable.
3. On the iPhone, a message appears:

```
┌────────────────────────────────┐
│   Trust This Computer?         │
│                                │
│   Your settings and data will  │
│   be accessible from this      │
│   computer when connected.     │
│                                │
│   [ Trust ]   [ Don't Trust ]  │
└────────────────────────────────┘
```

4. Tap **Trust**. Type your iPhone **passcode**.

> 📖 **New word: Trust (a computer)**
> Allowing your Mac to talk to your iPhone. Only trust **your own** computers.

💡 **Tip:** On the Mac, a message may also ask "Allow accessory to connect?" — click **Allow**.

---

## 3. Step 2: Turn on Developer Mode

Since iOS 16, iPhones need **Developer Mode** to run apps from Xcode.

> 📖 **New word: Developer Mode**
> A special iPhone setting that allows apps from Xcode to run. It's **off** by default for safety.

The **Developer Mode** option often only **appears** after you connect the phone to Xcode once (or after you try to run an app on it). So:

1. In Xcode, select your iPhone in the **run destination** menu (it appears under **iOS Device**).
2. Press **Run** (`Cmd + R`). Xcode may say Developer Mode is disabled. That's OK.
3. On the iPhone, open **Settings → Privacy & Security**.
4. Scroll **all the way down** to **Developer Mode**. Tap it.
5. Turn it **on**. 🔛
6. Tap **Restart**.
7. After the restart, unlock the iPhone. A message asks **"Turn On Developer Mode?"** → tap **Turn On** and type your passcode.

```
 Settings
  └─ Privacy & Security
       └─ (scroll down)
           └─ Developer Mode  [ ON ]
```

⚠️ **Careful:** If you **don't see** Developer Mode in Settings: connect the phone, open Xcode, select the phone as the run destination, and wait a minute. Then check Settings again.

---

## 4. Step 3: Let Xcode prepare the device

The first time, Xcode needs to **prepare** your iPhone:

- The toolbar status may say **"Preparing iPhone…"** or **"Copying shared cache symbols…"**.
- This can take **several minutes**. ☕
- Keep the phone **connected** and **unlocked**.

You can watch it in **Window → Devices and Simulators** (`Cmd + Shift + 2`) → **Devices** tab.

```
┌──────────────┬─────────────────────────────────────────┐
│ DEVICES      │  Ravi's iPhone                          │
│  📱 Ravi's   │  iOS 18.x                               │
│     iPhone   │  Model: iPhone 15                       │
│              │  ☐ Connect via network                  │
│ SIMULATORS   │                                         │
│  ...         │  Installed Apps:                        │
│              │   ...                                   │
└──────────────┴─────────────────────────────────────────┘
```

---

## 5. Step 4: Run your app! ▶

1. Run destination → choose **your iPhone** (by its name, e.g. "Ravi's iPhone").
2. Press **Run** (`Cmd + R`).
3. Xcode builds, installs, and tries to open the app.

### The first time: "Untrusted Developer" (free Apple ID)

With a **free** account, the first launch shows:

```
┌──────────────────────────────────────┐
│   Untrusted Developer                │
│                                      │
│   Your device management settings    │
│   do not allow using apps from       │
│   developer "Apple Development:      │
│   ravi@…" on this iPhone. You can    │
│   allow using these apps in          │
│   Settings.                          │
│                [ Cancel ]            │
└──────────────────────────────────────┘
```

And Xcode may show: *"Could not launch 'HelloApp' — Verify the Developer App certificate for your account is trusted on your device."*

**Fix, on the iPhone:**

1. **Settings → General → VPN & Device Management**.
2. Under **Developer App**, tap your Apple ID email.
3. Tap **Trust "Apple Development: …"** → **Trust** again.

```
 Settings
  └─ General
       └─ VPN & Device Management
            └─ Developer App
                 └─ Apple Development: ravi@…
                      └─ [ Trust "Apple Development: ravi@…" ]
```

4. Go back to Xcode and press **Run** again.

🎉 **Your app is running on your real iPhone!** Tap it, show your friends! 📱✨

---

## 6. While the app runs from Xcode

- `print` messages still appear in Xcode's **Console** (`Cmd + Shift + Y`).
- **Breakpoints** work (Chapter 40).
- Press ■ **Stop** (`Cmd + .`) to stop. The app **stays installed** on the phone — you can open it from the home screen any time (until the free profile expires after 7 days).

---

## 7. Running wirelessly 📶 (no cable)

After the first time with a cable, you can usually run apps **over Wi-Fi**.

Requirements:
- Mac and iPhone on the **same Wi-Fi network**.
- The iPhone is **unlocked** (at least at the start).

Steps:
1. Connect with the cable once (sections 2–5).
2. **Window → Devices and Simulators** → select your iPhone.
3. ✅ Check **Connect via network** (in newer Xcode versions this may happen automatically).
4. Unplug the cable. A small **network icon** 🌐 appears next to your iPhone in the run destination menu.
5. Press **Run**.

⚠️ **Careful:** Wireless is **slower** and sometimes disconnects. If it doesn't work, use the cable.

---

## 8. Why test on a real device? 🤔

| The real iPhone shows… | The Simulator might hide… |
|---|---|
| **Real speed** — is the app smooth? | The Mac is much faster than a phone. |
| **Real touch** — are buttons big enough for a finger? | A mouse pointer is very precise. |
| **Camera, motion, Bluetooth, NFC** | Not available (or fake). |
| **Real battery and heat** | Not measured. |
| **Notifications, background behavior** | Can be different. |
| **Bright sunlight, one-hand use** | You're sitting at a desk. 😄 |

🧠 **Remember:** Develop with the Simulator. **Test on a real device** often, and always before publishing.

---

## 9. Common problems and fixes 🔧

| Problem | Fix |
|---|---|
| iPhone doesn't appear in Xcode | Unlock the phone. Try another cable (a **data** cable). Tap **Trust**. Restart Xcode. |
| "iPhone is not available. Please reconnect the device." | Unplug and plug in again. Unlock the phone. Restart the iPhone. |
| "The device is locked" | Unlock the iPhone and keep it unlocked while Xcode installs. |
| "Developer Mode disabled" | Section 3. |
| "This iPhone is running iOS XX, which may not be supported by this version of Xcode" | **Update Xcode** (and macOS if needed). |
| "Untrusted Developer" | Section 5 — trust the developer in Settings → General → VPN & Device Management. |
| "Signing for … requires a development team" | Chapter 38 — choose your Team. |
| App opened yesterday, now crashes immediately / won't open | **Free account 7-day limit.** Connect and run from Xcode again. |
| "Unable to install — The maximum number of apps for free development profiles has been reached." | Delete one of your **other** Xcode-installed apps from the iPhone, then run again. |
| Stuck at "Preparing device / Copying shared cache" | Wait (can be 10+ minutes the first time). Keep it connected and unlocked. |
| Works with cable, not wireless | Same Wi-Fi? iPhone unlocked? Some office/school Wi-Fi blocks devices from seeing each other — use the cable. |

---

## 10. Removing your app from the iPhone

Like any app: **press and hold** the icon → **Remove App** → **Delete App**.

To turn **Developer Mode off** later: Settings → Privacy & Security → Developer Mode → off (the phone restarts).

---

## 🏋️ Practice

1. Connect your iPhone (if you have one) and **trust** the Mac.
2. Turn on **Developer Mode**.
3. Run your `AboutMe` app on your iPhone. Trust the developer if asked.
4. Add a `print` in `.onAppear` and see it in Xcode's Console **while the app runs on your phone**.
5. Try running **wirelessly**.
6. Compare: does your app look the same on the phone as in the Simulator? Write down any differences.

---

## 🧠 Remember

- Connect → **Trust** → turn on **Developer Mode** → select the iPhone → **Run**.
- Free account: trust the developer in **Settings → General → VPN & Device Management**.
- Free account apps stop working after **7 days** — just run again from Xcode.
- After the first cable connection, you can run **wirelessly** on the same Wi-Fi.
- Always test on a **real device** before publishing.

---

⬅️ **Back:** [Chapter 38 — Signing, Certificates and Bundle IDs](38-signing-certificates.md)
➡️ **Next:** [Chapter 40 — Finding and Fixing Bugs](40-debugging.md)
