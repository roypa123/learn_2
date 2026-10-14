# Chapter 38 — Signing, Certificates and Bundle IDs

🍎 **Needs a Mac**

---

## What you will learn

- What **code signing** is and why Apple needs it.
- The 4 pieces: **Bundle ID**, **Certificate**, **Provisioning Profile**, **Team**.
- **Free** Apple ID vs **paid** Apple Developer Program.
- Setting up **automatic signing** (the easy way).
- **Capabilities**.
- Fixing the most common signing errors.

This topic confuses **everyone** at first — even experienced developers. 😅 Go slowly. With automatic signing, Xcode does most of the work for you.

---

## 1. Why does Apple need signing?

Imagine you receive a letter ✉️ that says "From your bank". How do you know it's **really** from your bank and not from a thief?

The bank puts a **special stamp** 🔏 that only they have.

**Code signing** is that stamp for apps. It proves:

1. **Who** made the app (it's really you).
2. The app was **not changed** by anyone after you signed it.
3. The app is **allowed** to run on this device.

> 📖 **New word: Code signing**
> Adding a digital "stamp" to your app that proves who made it and that nobody changed it.

🧠 **Remember:** iPhones **only** run apps that are signed. The **Simulator** doesn't need signing — that's why you could run apps there already!

---

## 2. The 4 pieces of the puzzle 🧩

| Piece | Like… | What it is |
|---|---|---|
| **Bundle ID** | The app's **passport number** 🛂 | The app's unique name: `com.ravikumar.HelloApp` (Chapter 33). |
| **Team** | The **company** that owns the app 🏢 | Your Apple account (Personal Team or a paid team). |
| **Certificate** | Your **ID card** 🪪 | Proves **you** are a trusted developer. Stored in your Mac's **Keychain**. |
| **Provisioning Profile** | A **permission slip** 📄 | Connects everything: "This **developer** may install this **app** on these **devices**, with these **capabilities**." |

```
            ┌──────────────── Provisioning Profile 📄 ────────────────┐
            │                                                          │
            │   Team 🏢  +  Certificate 🪪  +  Bundle ID 🛂               │
            │   + list of devices 📱 + capabilities (iCloud, Push…)     │
            │                                                          │
            └──────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                          App can be signed ✅
                          and installed on the iPhone
```

> 📖 **New word: Certificate**
> A digital ID file from Apple that proves you're a registered developer. It lives in your Mac's **Keychain** (the Mac's password safe).

> 📖 **New word: Provisioning profile**
> A file from Apple that says which **app**, made by which **developer**, may run on which **devices**.

> 📖 **New word: Keychain**
> The Mac's safe for passwords and certificates. App: **Keychain Access**.

---

## 3. Free Apple ID vs paid Developer Program

| | 🆓 **Free Apple ID** (Personal Team) | 💳 **Apple Developer Program** (yearly fee) |
|---|---|---|
| Run in the Simulator | ✅ | ✅ |
| Run on **your own** iPhone | ✅ (with limits) | ✅ |
| App stops working after | **7 days** — then reinstall from Xcode | 1 year (development profile) |
| Number of apps on device | A small limit (a few apps at a time) | No practical limit |
| **TestFlight** (send to testers) | ❌ | ✅ |
| **App Store** | ❌ | ✅ |
| Some capabilities (Push Notifications, iCloud, Sign in with Apple…) | ❌ Not available | ✅ |

> 📖 **New word: TestFlight**
> Apple's app for sending **test versions** of your app to friends and testers before it's on the App Store.

🧠 **Remember:** For **learning**, the **free** Apple ID is enough! Pay only when you want to publish or need special capabilities.

💡 **Tip:** If your app on your iPhone suddenly won't open after a week, that's the **7-day limit** of the free account. Just connect the phone and run from Xcode again.

---

## 4. Setting up automatic signing ⭐ (the easy way)

### Step 1: Add your Apple ID to Xcode

(You may have done this in Chapter 31.)

**Xcode → Settings (`Cmd + ,`) → Accounts → + → Apple ID**.

### Step 2: Choose your team in the target

1. Click the project 📘 → select your **target**.
2. Click **Signing & Capabilities**.

```
┌────────────────────────────────────────────────────────────┐
│ [All] [Debug] [Release]                                    │
│                                                            │
│ ▾ Signing                                                  │
│     ☑ Automatically manage signing                         │
│                                                            │
│     Team               [ Ravi Kumar (Personal Team) ▾ ]    │
│     Bundle Identifier  [ com.ravikumar.HelloApp       ]    │
│     Provisioning Profile  Xcode Managed Profile  ⓘ        │
│     Signing Certificate   Apple Development: Ravi…         │
│                                                            │
│ [+ Capability]                                             │
└────────────────────────────────────────────────────────────┘
```

3. ✅ Make sure **Automatically manage signing** is checked.
4. Choose your **Team** from the menu.
5. Wait a few seconds. Xcode talks to Apple and creates the certificate and profile for you. 🪄

If there's no red error message — **you're done!** 🎉

| Field | Meaning |
|---|---|
| **Automatically manage signing** | Xcode creates and updates certificates and profiles for you. ✅ Keep it on. |
| **Team** | Who signs the app. |
| **Bundle Identifier** | The app's unique ID. |
| **Provisioning Profile** | "Xcode Managed Profile" = Xcode made it automatically. |
| **Signing Certificate** | "Apple Development: Your Name" = your development certificate. |

> 📖 **New word: Automatic signing**
> Xcode handles certificates and profiles for you. The opposite is **manual signing**, where you create them yourself on Apple's website. Beginners should always use automatic.

---

## 5. Development vs Distribution

There are two kinds of certificates and profiles:

| | 🛠️ **Development** | 📦 **Distribution** |
|---|---|---|
| Used for | Running on **your** devices from Xcode | **TestFlight** and the **App Store** |
| Certificate name | Apple Development | Apple Distribution |
| Needs paid program? | No (free works) | Yes |
| When | `Cmd + R` to your iPhone | Product → Archive → upload |

With automatic signing, Xcode chooses the right one. When you **Archive** for the App Store (Chapter 65), Xcode uses **Distribution**.

---

## 6. Capabilities

**Capabilities** are special features that need Apple's permission, because they use Apple services or private data.

To add one:

1. **Signing & Capabilities** tab.
2. Click **+ Capability** (top-left).
3. Double-click the one you want.

| Capability | Lets your app… | Free Apple ID? |
|---|---|---|
| **Background Modes** | Play audio, track location, etc. in the background | ✅ |
| **App Groups** | Share data between your app and its widget | ✅ (some limits) |
| **Keychain Sharing** | Share saved passwords between your apps | ✅ |
| **Push Notifications** | Receive notifications from a server | ❌ needs paid |
| **iCloud** | Save data to the user's iCloud | ❌ needs paid |
| **Sign in with Apple** | Let users log in with their Apple ID | ❌ needs paid |
| **In-App Purchase** | Sell things inside the app | ❌ needs paid |
| **HealthKit** | Read/write health data | ❌ needs paid |

When you add a capability, Xcode:
- Adds an **entitlements file** (`YourApp.entitlements`) to your project.
- Updates the provisioning profile automatically.

> 📖 **New word: Entitlements**
> A file listing the special permissions (capabilities) your app has.

⚠️ **Careful:** Capabilities ≠ privacy permissions. The **camera** doesn't need a capability — it needs a **usage description** in Info.plist (Chapter 37). Some features need **both**.

---

## 7. Bundle ID rules and tips

| Rule | Example |
|---|---|
| Use reverse-domain style | `com.yourname.AppName` |
| Only letters, numbers, `-` and `.` | ✅ `com.ravi-kumar.hello-app` ❌ `com.ravi kumar.hello app` |
| Must be **unique worldwide** | If someone else already registered `com.example.HelloApp`, you can't use it. |
| Hard to change after publishing | Once on the App Store, the Bundle ID is **permanent** for that app. |

### Free account tip

With a free account, Bundle IDs that someone else (or you, in another team) already used are **blocked**. If you see an error about the Bundle ID, just change it a little:

`com.ravikumar.HelloApp` → `com.ravikumar.HelloApp2` or `com.ravikumar2026.HelloApp`

---

## 8. Common signing errors and fixes 🔧

### Error 1: "Signing for 'HelloApp' requires a development team."

```
❌ Signing for "HelloApp" requires a development team.
   Select a development team in the Signing & Capabilities editor.
```

**Fix:** Signing & Capabilities → **Team** → choose your team. (If the list is empty, add your Apple ID in Xcode → Settings → Accounts.)

### Error 2: "Failed to register bundle identifier."

```
❌ Failed Registering Bundle Identifier: The app identifier
   "com.example.HelloApp" cannot be registered to your development team
   because it is not available.
```

**Meaning:** Someone already uses this Bundle ID.
**Fix:** Change the Bundle ID to something more unique, like `com.yourfullname.HelloApp`.

### Error 3: "Your maximum App ID limit has been reached."

**Meaning:** Free accounts can only create a limited number of new app IDs per week.
**Fix:** Wait a few days, or reuse an older Bundle ID from a project you don't need.

### Error 4: "Cannot create a iOS App Development provisioning profile…" / "No devices"

**Meaning:** Xcode needs at least one **real device** registered to make a development profile.
**Fix:** Connect your iPhone with a cable, select it as the run destination, and try again (Chapter 39).

### Error 5: "Personal development teams… do not support the Push Notifications capability."

**Meaning:** Your free account can't use this capability.
**Fix:** Remove the capability (click the **🗑** / **×** next to it in Signing & Capabilities), or join the paid program.

### Error 6: "Untrusted Developer" on the iPhone

```
Untrusted Developer
Your device management settings do not allow using apps
from developer "Apple Development: ravi@…" on this iPhone.
```

**Fix (on the iPhone):** **Settings → General → VPN & Device Management** → tap your developer account → **Trust**. (Chapter 39 shows this step by step.)

### Error 7: Strange signing problems that don't make sense

**Try, in order:**
1. Uncheck and re-check **Automatically manage signing**.
2. Choose **None** as team, then choose your team again.
3. **Product → Clean Build Folder** (`Cmd + Shift + K`).
4. **Xcode → Settings → Accounts** → select your account → **Download Manual Profiles** (or remove and re-add the account).
5. Quit Xcode and open it again.

---

## 9. Manual signing (just so you know)

Big companies sometimes use **manual signing**: they create certificates and profiles on **developer.apple.com** themselves, download them, and choose them in Xcode.

| | Automatic | Manual |
|---|---|---|
| Who creates certificates/profiles | Xcode | You, on Apple's website |
| Good for | Beginners, small teams | Large teams, CI servers |
| Difficulty | Easy | Hard |

🧠 **Remember:** Stay with **automatic** signing until you have a real reason to change.

---

## 10. One-page summary 📋

```
  Want to run on…           You need…
  ─────────────────────     ─────────────────────────────────────────
  Simulator                 Nothing! No signing needed.

  Your own iPhone           Free Apple ID + Team selected
                            + Automatically manage signing ✅
                            (app expires after 7 days on free account)

  Friends (TestFlight)      Paid Apple Developer Program
  App Store                 + Archive with Distribution signing
```

---

## 🏋️ Practice

1. Open **Signing & Capabilities** for your project. Check that **Automatically manage signing** is on and choose your Personal Team.
2. Look at the **Signing Certificate** name. Write it down.
3. Click **+ Capability**. Look at the list (don't add anything you don't need). Which ones do you recognize?
4. Change your Bundle ID to `com.yourname.SigningTest`. Is there an error? If so, read it and fix it.
5. Open the **Keychain Access** app on the Mac and search for "Apple Development". You'll see your certificate there.

---

## 🧠 Remember

- iPhones only run **signed** apps. The Simulator doesn't need signing.
- 4 pieces: **Bundle ID** (app's ID), **Team** (owner), **Certificate** (your ID card), **Provisioning Profile** (permission slip).
- Use **Automatically manage signing** ✅ and pick your **Team**.
- **Free** account: your own device, apps expire after **7 days**, no App Store.
- **Paid** program: TestFlight, App Store, Push, iCloud, etc.
- Most errors are fixed by: choosing a team, changing the Bundle ID, or connecting a device.

---

⬅️ **Back:** [Chapter 37 — Info.plist, App Icons and Launch Screen](37-info-plist-icons-launch.md)
➡️ **Next:** [Chapter 39 — Running on a Real iPhone](39-running-on-iphone.md)
