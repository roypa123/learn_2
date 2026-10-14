# Chapter 28: Publishing Your App on Google Play — Sharing With the World 🌍🚀

> **What you will learn in this chapter**
>
> 1. The **big picture**: from your computer to millions of phones 🗺️
> 2. Getting the app **ready**: a unique **package name**, a good **app name**, and **version numbers** 🏷️
> 3. A beautiful **adaptive app icon** 🎨
> 4. The **release build**: smaller and faster with **R8**, and without debug logs 📦
> 5. **Signing** your app with your own **key** 🔑 — and why you must never lose it
> 6. The **Android App Bundle** (`.aab`) 🎁
> 7. The **Google Play Console**: your account, your app, and the **policy forms** 📋
> 8. The **store listing**: texts, screenshots, and graphics 🖼️
> 9. **Testing tracks** — friends first, then everyone 👫
> 10. Going **live**, watching **crashes**, and sending **updates** 🔁
> 11. 🎓 **The end of the book** — and where to go next
>
> **Time needed:** about 3–4 hours of reading and work — plus some **waiting days** for Google (account checks, tests, and review). ⏳
>
> **What you need to know:** Chapters 1–27. We'll publish the **Notes app** (Chapters 24–26) — but every step works for **any** app.

---

## 28.1 The Big Picture 🗺️

Until now, your apps traveled from Android Studio to your emulator or phone through a **cable** (or Wi-Fi). That's a **debug** version: made for **you**, the developer. 🛠️

To put an app on **Google Play** — where anyone in the world can find it — you need a **release** version, and a few things around it:

```
 🛠️ Your project
   │  1. Get ready: package name, app name, icon, version
   ▼
 📦 Release build (R8 makes it small and fast)
   │  2. Sign it with YOUR key 🔑
   ▼
 🎁 App Bundle (.aab file)
   │  3. Upload to the Play Console
   ▼
 📋 Play Console: store listing, policy forms, testers
   │  4. Google reviews it 🔍
   ▼
 🌍 Google Play — anyone can install it!
```

### Debug vs. release 🆚

| | **Debug** build 🛠️ | **Release** build 📦 |
|---|---|---|
| Made for | You, while building | Your **users** |
| Debugger can attach | ✅ Yes | ❌ No |
| Size and speed | Bigger, a bit slower | **Smaller**, **faster** (R8 shrinks and optimizes) |
| Signed with | A **debug key** Android Studio made automatically | **Your own** key 🔑 |
| Allowed on Google Play? | ❌ No | ✅ Yes |

> 💡 You've been using the debug version all along. In this chapter you'll make your **first release version**. 🎉

### Will it cost money? 💰

| Thing | Cost |
|---|---|
| Android Studio, Kotlin, all the libraries | **Free** |
| A **Google Play developer account** | A **one-time** fee of **25 US dollars** (pay once, publish many apps — forever) |
| A website for your **privacy policy** | Can be **free** (Google Sites, GitHub Pages…) |

---

## 28.2 Which App? And a Pre-Flight Check ✈️

We'll publish the **Notes app** — the biggest and most polished app in this book: Room, DataStore, Hilt, photos, reminders, animations, **and** tests. 📝✨

Before a plane takes off, the pilots go through a **checklist**. ✈️ Let's do the same:

| Check | Why | Chapter |
|---|---|---|
| ✅ All tests are **green** | You don't want to ship bugs | 27 |
| ✅ No **crashes** when you use it like a naughty user 😈 (empty notes, rotation, no permission…) | Crashes give **1-star** reviews ⭐ | 27 |
| ✅ Works in **dark mode** 🌙 and **light mode** ☀️ | Many users use dark mode | 7 |
| ✅ Works with **big font size** (Settings → Display → Font size) 🔠 | Accessibility ♿ | 26 |
| ✅ Works after **process death** | Users switch apps all the time | 14, 24 |
| ✅ Permissions are asked **politely**, and "no" doesn't break the app | Google checks this, and users hate pushy apps | 25 |
| ✅ No `TODO`s or test screens left in the app | Professional apps look finished | — |

> 🛠️ If one check fails — fix it **first**. Publishing is not a race. 🐢

---

## 28.3 A Unique Package Name — `applicationId` 🏷️

Every app on Google Play has a **unique ID**, like a **passport number** 🛂. No two apps in the world can have the same one. It's called the **application ID**, and it looks like a package name: `com.example.notes`.

Open **`build.gradle.kts (Module :app)`**:

```kotlin
android {
    namespace = "com.example.notes"                       // (1)
    // ...

    defaultConfig {
        applicationId = "com.example.notes"               // (2)
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
        // ...
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `namespace` | The package of your **Kotlin code** (and where Android puts generated code like `R`). It's **internal** — users never see it. |
| 2 | `applicationId` | The app's **passport number** for Google Play and for the phone. 🛂 It's what makes your app "**your** app". |

Usually they're the same, but they don't **have** to be.

### ⚠️ `com.example` is not allowed!

Google Play **refuses** any app whose ID starts with **`com.example`** — it's reserved for examples (that's why every project in this book used it!). So we must choose our **own** ID.

### Choosing your ID 🤔

The tradition is a **reversed web address** that belongs to you, plus the app name:

| You have… | Example `applicationId` |
|---|---|
| A website `mywebsite.com` | `com.mywebsite.notes` |
| A GitHub account `ana-codes` | `io.github.anacodes.notes` |
| Nothing (yet) | `com.yourname.notes` (for example `com.anasilva.notes`) — choose something **only you** would use |

**Rules:** only lowercase letters, digits, `_` and `.`; at least **two parts** (`com.anything`); each part starts with a **letter**. No `-`! (So `ana-codes` becomes `anacodes`.)

Change **only** the `applicationId` line (we keep `namespace` the same — then we don't have to move any code):

```kotlin
defaultConfig {
    applicationId = "io.github.anacodes.notes"            // 👈 use YOUR own!
    // ...
}
```

**Sync Now** 🔄 and **run** the app.

Notice: your phone now shows **two** Notes apps! 😮 That's because for Android, a different `applicationId` = a **different app**. The old one (`com.example.notes`) still has your old notes. You can uninstall it.

> 🔥 **The forever rule:** once your app is published, its `applicationId` can **never** change. A new ID = a **new app** on Google Play (with no users, no reviews). So choose carefully! 🧐

> ✅ **Good news:** remember the FileProvider authority from Chapter 25? We wrote `${applicationId}.fileprovider` — it updates **automatically**. And `PhotoStorage` uses `"${context.packageName}.fileprovider"`, and `context.packageName` **is** the `applicationId` while the app runs. Both sides still match. That's why we didn't write the name by hand. 😎

---

## 28.4 The App Name 📛

The name under the icon comes from **`res/values/strings.xml`**:

```xml
<resources>
    <string name="app_name">Notes</string>
</resources>
```

…and the manifest uses it: `android:label="@string/app_name"`.

"Notes" is **very** plain — there are hundreds of "Notes" apps. On the phone, a short name is good (it must fit under the icon, about **12 characters**). On Google Play, you can use a **longer** name (up to **30** characters). Let's pick something friendly:

```xml
<string name="app_name">Pocket Notes</string>
```

| Where | Name | Max |
|---|---|---|
| Under the icon on the phone 📱 | `Pocket Notes` | ~12 characters fit nicely |
| On Google Play 🏪 (set in the Play Console, 28.13) | `Pocket Notes – Simple Notes` | 30 characters |

> ⚠️ **Don't** use names of other companies or famous products ("Google Notes", "Notes for Instagram"). Google rejects apps that pretend to be someone else, and the owners can complain. ™️🚫

---

## 28.5 A Beautiful App Icon 🎨

The icon is the **first** thing people see — on Google Play **and** on their home screen. Until now, our apps used Android's default green robot icon 🤖. Time for our own!

### Adaptive icons — two layers 🥞

Different phones show icons in different **shapes**: circles ⚪, squircles, rounded squares, teardrops… So modern Android icons are **adaptive**: you give **two layers**, and the phone cuts the shape it likes.

```
   Background layer         Foreground layer          The phone cuts a shape
  ┌──────────────┐         ┌──────────────┐           ╭────────────╮
  │▓▓▓▓▓▓▓▓▓▓▓▓▓▓│    +    │              │    =     ╱   ┌──────┐   ╲
  │▓▓ (yellow) ▓▓│         │     📝      │          │    │  📝  │    │
  │▓▓▓▓▓▓▓▓▓▓▓▓▓▓│         │              │           ╲   └──────┘   ╱
  └──────────────┘         └──────────────┘            ╰────────────╯
```

| Layer | What goes in it |
|---|---|
| **Background** | A color or a simple pattern. It fills the whole shape. |
| **Foreground** | Your **symbol** (logo). It must stay inside the **safe zone** — a circle in the middle (about 66 of the 108 "dp units" of the layer). Anything outside might be **cut off** ✂️ by some phone shapes, or moved during animations. |
| **Monochrome** (optional) | A **one-color** version of your symbol. Since Android 13, users can turn on **themed icons** — all icons get the colors of their wallpaper. 🎨 Without this layer, your icon won't join in. |

### Making the icon with Image Asset Studio 🛠️

Android Studio has a built-in icon maker!

1. In the Project window, right-click **`res`** → **New → Image Asset**.
2. **Icon type:** `Launcher Icons (Adaptive and Legacy)`.
3. **Name:** keep `ic_launcher` (so you replace the robot).
4. **Foreground Layer** tab:
   - **Source Asset → Asset type:** choose **Clip art** (Material icons — for example search "edit note" 📝), **Image** (your own PNG or SVG drawing), or **Text** (a letter or emoji).
   - **Color:** for clip art, choose the symbol color (for example dark brown `#5D4037`).
   - **Resize:** move the slider until the symbol sits **inside** the safe-zone circle shown in the preview.
5. **Background Layer** tab: **Asset type: Color** → a warm yellow, for example `#FFE082` (our Notes yellow! 💛).
6. **Options** tab: make sure **Legacy icon** and **Round icon** are **Yes** (for very old phones), and **Google Play Store icon** is **Yes**.
7. Click **Next**. Android Studio shows which files it will create (and replace). Click **Finish**.

**Run the app** ▶️ and look at your home screen: your **own** icon! 🎉 Press and hold it, or look at it in the app drawer — round, square, whatever your phone likes.

### What did Image Asset Studio create? 📁

| File(s) | What it is |
|---|---|
| `res/mipmap-anydpi-v26/ic_launcher.xml` (and `ic_launcher_round.xml`) | The **adaptive** icon: "background = this, foreground = that". Used on Android 8+. |
| `res/drawable/ic_launcher_foreground.xml` / `res/values/ic_launcher_background.xml` | The two layers. |
| `res/mipmap-mdpi/`, `-hdpi/`, `-xhdpi/`… (`.webp` files) | **Legacy** pictures in different sizes, for older phones. |
| `src/main/ic_launcher-playstore.png` | A **512 × 512** pixel icon — the one you'll **upload** to Google Play (28.13). 📤 |

> 💡 The manifest already points to these files (`android:icon="@mipmap/ic_launcher"` and `android:roundIcon="@mipmap/ic_launcher_round"`), so you don't change anything there.

### Adding a monochrome (themed) icon 🎨

Image Asset Studio may not create the monochrome layer. Add it yourself in **`res/mipmap-anydpi-v26/ic_launcher.xml`**:

```xml
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
    <monochrome android:drawable="@drawable/ic_launcher_foreground" />   <!-- 👈 new -->
</adaptive-icon>
```

| Line | Meaning |
|---|---|
| `<background ...>` / `<foreground ...>` | The two layers (already there). Your file may say `@drawable/...` or `@mipmap/...` for the background — keep what it says. |
| `<monochrome ...>` | The themed-icon version. Android uses **only the shape** of this drawing and paints it in the wallpaper colors — so our foreground (a simple symbol) works well. |

Do the same in `ic_launcher_round.xml`. Then on an Android 13+ phone: long-press the home screen → **Wallpaper & style** → turn on **Themed icons**. Your icon joins the color party! 🥳

### Good icon tips 💡

| ✅ Do | ❌ Don't |
|---|---|
| **One** simple, bold symbol | Tiny details or text (unreadable at icon size) |
| Strong contrast between layers | Light gray on white |
| Check it **small**, on a **dark** and a **light** wallpaper | Only look at it big on your computer screen |
| Keep the symbol in the **safe zone** | Put important parts near the edges ✂️ |

> 🌟 **Bonus — the splash screen:** since Android 12, every app shows a short **splash screen** while it starts: your **icon** on a background color. You get it **automatically** — with your new icon, it already looks great!

---

## 28.6 Version Numbers 🔢

Look at `defaultConfig` again:

```kotlin
defaultConfig {
    applicationId = "io.github.anacodes.notes"
    minSdk = 24
    targetSdk = 35
    versionCode = 1                    // (1)
    versionName = "1.0"                // (2)
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `versionCode = 1` | A **whole number** for **computers**. 🤖 Google Play and the phone use it to know which version is **newer**. Every new upload must have a **bigger** number than **all** uploads before — and the same number can **never** be used twice. Users never see it. |
| 2 | `versionName = "1.0"` | A **text** for **humans**. 👀 Shown on Google Play and in the phone's app settings. You can write anything — but most people use **`MAJOR.MINOR.PATCH`**. |

### `MAJOR.MINOR.PATCH` — a simple system 📐

| Change | Example | When |
|---|---|---|
| **PATCH** (last number) | 1.0.0 → 1.0.**1** | Small **bug fixes** 🐛 |
| **MINOR** (middle) | 1.0.1 → 1.**1**.0 | **New features**, nothing removed ✨ |
| **MAJOR** (first) | 1.1.0 → **2**.0.0 | **Big** changes, a redesign 🏗️ |

Example history of Pocket Notes:

| Release | `versionCode` | `versionName` | What changed |
|---|---|---|---|
| First release | 1 | 1.0.0 | 🎉 |
| Fix: crash on empty search | 2 | 1.0.1 | 🐛 |
| New: note colors in widgets | 3 | 1.1.0 | ✨ |
| A test version that was never released | 4 | 1.2.0-beta | 🧪 (4 is now **used** — next must be 5!) |
| Big redesign | 5 | 2.0.0 | 🏗️ |

> 💡 `versionCode` just goes **+1** every time you upload. Simple! (It can be as big as 2 100 000 000, so you'll never run out. 😄)

### What about `targetSdk`? 🎯

| Value | Meaning |
|---|---|
| `minSdk = 24` | The **oldest** Android version that can install your app (Android 7.0). |
| `targetSdk = 35` | The Android version your app was **designed and tested for**. Android turns on the newest rules and behaviors up to this version. |
| `compileSdk` | The Android version whose **tools** you use to build (above `defaultConfig`). |

**Google Play requires a recent `targetSdk`**: new apps and updates must target an Android version that is at most about **one year old**. Google raises the requirement **every year** (usually at the end of August). Android Studio shows a **yellow warning** in `build.gradle.kts` when your `targetSdk` is too old, and the Play Console tells you the current rule when you upload. ✅

> ⚠️ When you increase `targetSdk`, **test your app again** — Android may behave differently (for example, Android 13 added the notification permission from Chapter 25). Read Google's "behavior changes" page for that version.

---

## 28.7 The Release Build — Small and Fast 📦⚡

### What is R8? ✂️

When you build a **release** version, a tool called **R8** can go through your app and its libraries and:

| R8 does… | Like… |
|---|---|
| **Shrink** — remove code that is **never used** (libraries are big, you use only a part!) | Packing for a trip: take only what you'll wear 🧳 |
| **Optimize** — make the remaining code faster | Taking a shorter road 🛣️ |
| **Obfuscate** — rename classes and functions to short names (`NotesListViewModel` → `a.b`) | Making the code smaller **and** harder for others to copy 🕶️ |
| **Shrink resources** (with `isShrinkResources`) — remove unused pictures and texts | Throwing away empty boxes 📦 |

The result: an app that is often **several times smaller** and starts **faster**. Users love small apps — especially people with slow internet or little storage. 🌍

### Turn it on — `build.gradle.kts (Module :app)`

Inside `android { }`, find `buildTypes`. New projects have R8 **off**. Turn it on:

```kotlin
buildTypes {
    release {
        isMinifyEnabled = true                                       // (1)
        isShrinkResources = true                                     // (2)
        proguardFiles(                                               // (3)
            getDefaultProguardFile("proguard-android-optimize.txt"),
            "proguard-rules.pro"
        )
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `isMinifyEnabled = true` | Turn on R8: shrink, optimize, obfuscate the **code**. |
| 2 | `isShrinkResources = true` | Also remove **unused resources** (only works when #1 is on). |
| 3 | `proguardFiles(...)` | The **rules** for R8. The first file is Google's standard rules (the "optimize" version). The second, **`proguard-rules.pro`**, is **your** file for extra rules. (The name comes from **ProGuard**, R8's older brother — the rule language is the same.) |

> 💡 This only affects the **release** build. Your debug build stays the same, so the debugger still works normally. 🐞

### Remove debug logs from the release 🧹📔

Remember Chapter 27's rule: debug messages are for **you**, not for users. R8 can **delete** all `Log.d` and `Log.v` calls in the release build automatically! Open **`proguard-rules.pro`** (in the Project window under **Gradle Scripts**) and add at the end:

```
-assumenosideeffects class android.util.Log {
    public static int v(...);
    public static int d(...);
}
```

| Line | Meaning |
|---|---|
| `-assumenosideeffects class android.util.Log` | "R8, these functions of `Log` do nothing important — if nobody uses their result, you may **remove** the calls." |
| `public static int v(...);` / `d(...)` | Which functions: **v**erbose and **d**ebug. (`...` = with any parameters.) We **keep** `i`, `w`, and `e` — warnings and errors can still be useful. |

> ⚠️ This only works with `proguard-android-optimize.txt` (the "optimize" version) — that's why we chose it. And still: **never** log passwords or private data, in any build. 🔐

### Do our libraries need extra rules? 📚

R8 removes what it thinks is **unused**. But some libraries find classes in **sneaky** ways (by name, at runtime), and R8 can't see that. Then R8 removes or renames something that's really needed — 💥.

Good news: modern libraries ship **their own** R8 rules inside them, which R8 uses automatically. Room, Hilt, Navigation, DataStore, kotlinx.serialization, Retrofit, Coil, WorkManager — all of them do. ✅ So for the apps in this book, you normally need **nothing** more.

If a class is still removed wrongly, you'll learn how to fix it in a moment. 👇

### Test the release build on your phone! 🧪📱

**Never** upload a release build you haven't **tried**. R8 changes your app — test it!

**1. Let the release build use the debug key for now.** A release build must be **signed** to install (28.8). For testing on your own phone, borrow the debug key **temporarily**:

```kotlin
buildTypes {
    release {
        isMinifyEnabled = true
        isShrinkResources = true
        proguardFiles(
            getDefaultProguardFile("proguard-android-optimize.txt"),
            "proguard-rules.pro"
        )
        signingConfig = signingConfigs.getByName("debug")           // 👈 TEMPORARY, for testing only
    }
}
```

**2. Choose the release variant:** **View → Tool Windows → Build Variants**. In the table, change `:app` from **debug** to **release**.

**3. Run ▶️** — it takes longer than usual (R8 is working hard 🏋️). Then use **every** feature: add, edit, search, sort, delete + Undo, pin, photos, camera, reminder, dark mode, rotation. 

**4. Switch back** to **debug** in Build Variants when you're done, and **remove** the `signingConfig` line. (The real signing comes in 28.8.)

> 📏 **Compare the sizes:** **Build → Analyze APK…** lets you open an APK and see what's inside, and how big it is. The release one is usually **much** smaller than the debug one. 🎉

### "It works in debug but crashes in release!" 😱

This is almost always R8. The stack trace looks strange — R8 **renamed** everything:

```
java.lang.NullPointerException
    at a.b.c(SourceFile:12)
    at d.e.f(SourceFile:4)
```

What can you do?

| Step | How |
|---|---|
| **1. Read the real names** | R8 writes a **dictionary** of all renames: `app/build/outputs/mapping/release/mapping.txt`. A small tool called **retrace** (part of the Android SDK command-line tools) uses this file to translate the strange names back into real ones. (When you upload an **App Bundle** to Google Play, the dictionary travels **inside** it, and the Play Console shows **readable** crash reports. 😊) |
| **2. Keep what was removed** | Add a **keep rule** to `proguard-rules.pro`, for example: `-keep class io.github.anacodes.notes.data.model.** { *; }` = "*don't remove or rename anything in this package*". Or put the **`@Keep`** annotation (`androidx.annotation.Keep`) on the class. |
| **3. Search** | Search for "R8" + the library name + the error. Usually someone found the right rule already. 🌍 |

> 💡 Use keep rules **carefully**: every rule makes the app a little bigger. Keep only what's needed.

---

## 28.8 Signing — Your App's Personal Seal 🔑✍️

In the old days, kings closed their letters with a **wax seal** 🔴 made with their **personal ring**. Everyone could check the seal — and nobody could fake it without the ring. 💍

Android apps work the same way. Every app must be **signed** with a **key**:

- When you **install** an update, Android checks: "*Is it signed with the **same** key as the app I already have?*" If not → **refused**. 🚫
- This protects users: nobody else can publish a fake "update" to **your** app and steal its users' data. 🛡️

Until now, Android Studio signed everything with a secret **debug key** it made for you automatically. That key is **not allowed** on Google Play. Now you'll make **your own**. 💍

### Words you need 📖

| Word | Meaning |
|---|---|
| **Keystore** 🗄️ | A **file** (ending in `.jks`) that holds one or more keys. Protected by a **password**. |
| **Key** 🔑 | The real "ring". It has a **name** (the **alias**) and its **own** password. |
| **Certificate** 📜 | Public information about the key's owner (your name, country…). It's attached to the app, so everyone can **check** the seal. |

### Create your key and sign the app ✍️

1. **Build → Generate Signed App Bundle or APK…**
2. Choose **Android App Bundle** → **Next**.
3. Under **Key store path**, click **Create new…**. A form opens:

| Field | What to write |
|---|---|
| **Key store path** | Where to save the file. Choose a folder **outside** your project, for example `C:\keys\pocket-notes-upload.jks`. 📁 |
| **Password** / **Confirm** | A **strong** password for the keystore. |
| **Alias** | A name for the key, for example `upload`. |
| **Password** / **Confirm** (under Key) | A password for the key (it can be the same as the keystore password). |
| **Validity (years)** | **25** or more. Google Play needs keys that are valid for a **long** time. ⏳ |
| **Certificate** | Fill **at least one** field — for example your **First and Last Name** and **Country Code** (like `DE`, `IN`, `BR`, `US`). |

4. Click **OK**. Back in the wizard, your new keystore, alias, and passwords are filled in. → **Next**.
5. Choose the **release** build variant → **Create**.

A message appears at the bottom right: *"App bundle(s) generated successfully"* → click **locate**. You'll find:

```
app/release/app-release.aab        ← 🎁 this is what you upload!
```

🎉 You just made your first **signed release** of an Android app!

### 🔥 THE MOST IMPORTANT RULE IN THIS CHAPTER 🔥

> **Never lose your keystore file or its passwords. Never share them. Never put them into Git.**

Why so serious? 😨 Because Google Play only accepts updates signed with **your** key. Lose the key → you can't easily update your app. Someone steals it → they could sign apps **as you**.

**Do this today:**

| ✅ | What |
|---|---|
| 💾 | Make **two backups** of the `.jks` file in **different** places (for example a USB stick in a drawer **and** a private cloud folder). |
| 🔐 | Save the passwords and the alias in a **password manager** (or at least written on paper next to the USB stick). |
| 🙈 | Add these lines to your project's **`.gitignore`** file, so Git never uploads them by accident: |

```
# Signing — never commit these!
*.jks
*.keystore
keystore.properties
```

| Line | Meaning |
|---|---|
| `# ...` | A comment. |
| `*.jks`, `*.keystore` | Ignore **all** keystore files, whatever their name (`*` = anything). |
| `keystore.properties` | A file some people use to store the passwords (see Challenge 2). |

### Play App Signing — Google's safety net 🛡️

Here's some good news. When you upload your first App Bundle, Google Play uses **Play App Signing** (it's required for new apps). It works with **two** keys:

```
  YOU 🧑‍💻                                  GOOGLE PLAY 🏪
  ┌──────────────┐   upload .aab        ┌────────────────────┐    signed APKs
  │ upload key 🔑 │ ───────────────────▶ │ checks: is it you? │ ───────────────▶ 📱📱📱
  └──────────────┘                      │ app signing key 🗝️ │
                                        └────────────────────┘
```

| Key | Who keeps it | Used for |
|---|---|---|
| **Upload key** 🔑 (the one you just made) | **You** | Proving to Google that an upload really comes from **you**. |
| **App signing key** 🗝️ | **Google**, in a very safe place | Signing the app that users **install**. |

So if you **lose** your upload key, it's not the end of the world: you can ask Google to **reset** it in the Play Console (it takes a few days, and you prove it's you). 😮‍💨 But that's a **rescue**, not a plan — **back up your key**! 💾

---

## 28.9 App Bundle or APK? 🎁📦

You've heard both words. What's the difference?

| | **APK** (`.apk`) 📦 | **App Bundle** (`.aab`) 🎁 |
|---|---|---|
| What is it | The **installable** app — one file with **everything** inside | A **package for Google Play** — not installable directly |
| Contains | Code, pictures for **all** screen sizes, **all** languages… | The same — but organized in pieces |
| Who uses it | Phones (to install) | **Google Play** (to build APKs) |
| Required on Google Play | ❌ No (not for new apps) | ✅ **Yes** |

**How the bundle works:** Google Play takes your bundle and, for **each** phone, builds **small APKs** with **only** what that phone needs: the right picture sizes for **its** screen, the right processor code, **its** languages. 🧩

```
            🎁 app-release.aab
           /        |         \
   📱 phone A    📱 phone B    📱 tablet C
  (only what A  (only what B  (only what C
    needs)        needs)        needs)
```

Result: users download a **smaller** app — often much smaller. 📉

### Sharing an APK with a friend directly 🤝

Sometimes you want to give a friend your app **without** Google Play — for example to show it to them. Then make an **APK**:

1. **Build → Generate Signed App Bundle or APK…** → **APK** → **Next**.
2. Use the **same** keystore and key → choose **release** → **Create**.
3. You get `app/release/app-release.apk`. Send it to your friend (email, cloud folder…).
4. On their phone, they open the file. Android asks them to allow **"Install unknown apps"** for the app they opened it with (for example Files or Chrome). Then **Install**.

> ⚠️ Installing apps from outside Google Play is less safe, and Google is adding **extra checks** for apps installed this way (from verified developers only, in more and more countries). For sharing with many people, use Google Play's **testing tracks** (28.14) — they're easy and safe. 👫

---

## 28.10 Your Google Play Developer Account 🧑‍💻🏪

The **Google Play Console** is the website where developers manage their apps: upload, describe, test, publish, and watch statistics. 📊

> 📝 Websites change their buttons and menus often. If something looks a little different from this chapter, look for **similar words** — the steps stay the same. And always read Google's **current** rules in the Play Console's Help Center.

### Create the account

1. Go to **play.google.com/console** and sign in with a Google account. 💡 Many developers create a **separate** Google account just for development — then personal email and app business stay apart.
2. Choose the account type:

| Type | For | Needs |
|---|---|---|
| **Personal** 👤 | You, as a person (hobby, learning, small apps) | Your name, address, a photo of your **ID** |
| **Organization** 🏢 | A company or organization | Company documents, a **D-U-N-S number** (a free company ID) |

   For this book, choose **Personal**.

3. Fill in your **developer name** — it's shown **publicly** under your apps (for example "Ana Silva" or "Ana's Little Apps"). ✏️
4. Add your **contact** details. Google **verifies** your identity (ID document) — this can take from a few minutes to a few days. ⏳
5. Pay the **one-time fee** (25 US dollars). 💳
6. Google may also ask you to verify that you own a real **Android phone** (with the Play Console app). 📱

### ⚠️ An important rule for new personal accounts

New **personal** accounts must **test** their app with real people before they can publish to **everyone**: a **closed test** with at least **12 testers** who stay opted in for at least **14 days in a row**. 👫📅 Only then can you apply for **production** (= everyone).

So **start early**: find 12+ friends, family members, or classmates with Android phones. We'll set up the test in 28.14. (Google sometimes changes these numbers — the Play Console always shows the current rule.)

---

## 28.11 Create the App in the Play Console 🆕

On the Play Console home page, click **Create app**:

| Field | What to choose | Why |
|---|---|---|
| **App name** | `Pocket Notes` | You can change it later. |
| **Default language** | English (or your language) | The main language of your store page. |
| **App or game** | **App** | It's not a game. 🎮❌ |
| **Free or paid** | **Free** | ⚠️ A free app can **never** become paid later. (A paid app can become free.) |
| **Declarations** | ✅ Developer Program Policies, ✅ US export laws | You promise to follow Google's rules. Read them once — really! 📜 |

Click **Create app**. 🎉 You land on the app's **Dashboard**, with a list of tasks: *"Set up your app"*, *"Test your app"*, *"Release your app"*. We'll do them in order. ✅

---

## 28.12 App Content — The Policy Forms 📋

Google wants to know **what** your app does with users and their data, so it can protect them and show honest information on the store page. Find these under **Policy → App content** (or in the Dashboard's "Set up your app" list).

Don't worry — for a simple, honest app like Pocket Notes, the answers are easy. 😊

### 1. Privacy policy 🔐

A **privacy policy** is a public web page that explains what your app does with user data. Google requires one for apps that handle personal or sensitive data — and our app uses the **camera** and **photos**, so we need one. (Having one is a good idea for **every** app.)

Here is a simple, honest example for Pocket Notes. Change the names and email to yours:

```
Privacy Policy for Pocket Notes

Last updated: [date]

Pocket Notes is made by [your name]. This policy explains how the app
handles your information.

What the app stores
- Your notes (titles, text, colors, pins) and photos you add to notes.
- Your settings (sort order, daily reminder on or off).

Where it is stored
- Everything is stored only on your device, inside the app.
- The app does not send your notes, photos, or settings to the internet.
- We do not collect, sell, or share any personal data.

Permissions
- Camera: only used when you choose to take a photo for a note.
- Notifications: only used for the daily reminder you can turn on.
- Photos you pick with the photo picker are copied into the app's
  private folder so they stay attached to your note.

Deleting your data
- Delete a note in the app to remove it and its photo.
- Uninstalling the app deletes all of its data from your device.

Contact
If you have questions, write to: [your email]
```

> ⚠️ A privacy policy must be **true**! 🙅 If you later add internet features, analytics, or ads, you **must** update it.

**Where to put it?** It must be a **public web page** (not a PDF, not a Google Doc only you can open). Free options:

| Option | How |
|---|---|
| **Google Sites** | sites.google.com → new site → paste the text → **Publish** → copy the link |
| **GitHub Pages** | A free website from a GitHub repository (if you use GitHub) |

Paste the link into **Privacy policy** in the Play Console. ✅

### 2. App access 🔓

"*Can Google's reviewers use **everything** in your app?*" Pocket Notes has no login → **All functionality is available without special access**. ✅

(If your app needs a login, you give the reviewers a test account here.)

### 3. Ads 📢

"*Does your app contain ads?*" → **No**. ✅

### 4. Content rating 🔞

A short **questionnaire** about your app's content (violence, scary things, bad language, gambling…). Choose the category **Utility, Productivity, Communication, or Other**, and answer honestly. For Pocket Notes, almost everything is **No**.

One tricky question: "*Can users interact or share content with each other?*" → **No** — notes are **private**; they never leave the phone. 

You get ratings for different countries (like **"Everyone"** or **"3+"**). ✅

### 5. Target audience 👨‍👩‍👧

Which **age groups** is your app for? 

> ⚠️ If you include **children under 13**, Google's **Families policy** applies, with **extra** strict rules. For your first app, unless it's really made **for kids**, choose **13 and older** (or 18 and older).

### 6. Data safety 🛡️ — the most important form

This form creates the **"Data safety"** section on your store page. Users read it to decide if they **trust** your app. 🔍

Google's key words:

| Word | Google's meaning |
|---|---|
| **Collected** | The data is **sent off the device** — to you, to a server, to a library's company. |
| **Shared** | The data is given to **another company** (third party). |

Data that stays **only on the phone** is **not** "collected". 📱🔒

For Pocket Notes, notes, photos, and settings stay **on the device**. We use **no** analytics, **no** ads, **no** internet. So:

| Question | Answer |
|---|---|
| *Does your app collect or share any of the required user data types?* | **No** ✅ |

The store page will then show: **"No data collected"** and **"No data shared with third parties"** — a great sign for users! 🌟

> ⚠️ **Be careful with libraries!** Some libraries (analytics, crash reporting, ads, maps…) **send data** in the background. If you add one, read its documentation — **its** data counts as **your** app's data. Wrong answers here can get your app **removed**.

### 7. The other declarations

You'll see a few more questions — **government apps**, **financial features**, **health**, **news**, the **advertising ID**. For Pocket Notes, the answer is **No / None** for all. ✅

When everything is done, each item gets a green ✅ in the App content page. 🎉

---

## 28.13 The Store Listing — Your Shop Window 🖼️🛍️

The **store listing** is your app's page on Google Play. It's like a **shop window**: it decides if people come in. ✨ Go to **Grow → Store presence → Main store listing** (the menu name may differ a little).

### The texts ✍️

| Field | Max length | Tip |
|---|---|---|
| **App name** | 30 characters | Clear and simple. **No** "#1", "Best", "Free", or emojis to get attention — Google doesn't allow that in the name. |
| **Short description** | 80 characters | **One** sentence: what does it do, and why is it nice? |
| **Full description** | 4 000 characters | The details: features, in short paragraphs or a list. Honest and friendly. |

**Example for Pocket Notes:**

**App name:** `Pocket Notes – Simple Notes`

**Short description:**
```
Simple, colorful notes with photos and a daily reminder. Private and offline.
```

**Full description:**
```
Pocket Notes is a simple and friendly notes app. Write down ideas,
shopping lists, and plans — and find them again in a second.

★ Write and edit notes with a title and text
★ 6 colors to organize your notes
★ Pin important notes to the top
★ Search your notes instantly
★ Sort by last edited, date created, or title
★ Add a photo to a note — from your gallery or the camera
★ Swipe to delete, with Undo
★ Optional daily reminder at 8 PM
★ Beautiful light and dark themes

Private by design
Your notes stay on your phone. No account, no ads, no tracking.
Pocket Notes works completely offline.

Made with love by a new Android developer. Feedback is welcome!
```

> 🎯 **Be honest.** Describe only what the app **really** does. Don't repeat words many times to "trick" the search (Google calls this **keyword spam** and can reject the app). Don't mention other apps' names.

### The graphics 🎨

| Graphic | Size | Notes |
|---|---|---|
| **App icon** | **512 × 512** px, PNG | Use `ic_launcher-playstore.png` that Image Asset Studio made (28.5)! ✅ |
| **Feature graphic** | **1024 × 500** px, JPG or PNG (no transparency) | A wide banner shown at the top of your page in some places. Your icon + app name on a nice background is enough. Make it with any drawing tool (Canva, Figma, even PowerPoint). |
| **Phone screenshots** | **2 to 8** pictures | The **most important** graphics! People look at screenshots more than they read. 👀 |

### Making great screenshots 📸

1. Run the app on the emulator. Fill it with **nice example notes** (not "test test asdf" 😅): "Shopping 🛒 Milk, eggs, bread", "Trip to the mountains ⛰️", "Birthday ideas 🎁"… with different colors, one pinned, one with a photo.
2. Take screenshots with the **camera button** 📷 in the emulator's toolbar (or the **Running Devices** window in Android Studio). They're saved as PNG files.
3. Take **4 to 8**: the list, the editor, the color picker, a note with a photo, search, dark mode 🌙…

> ⚠️ **Never** show real **personal data** (your real phone numbers, addresses, private photos) in screenshots. And no debug things (like "Debug" banners) — screenshots should show the **real** app.

### Store settings ⚙️

Under **Store settings**: choose the **category** → **Productivity**, and add a **contact email** (required — users and Google may write to you). ✉️ A website is optional.

Click **Save**. 💾

---

## 28.14 Testing Tracks — Friends First 👫🧪

Google Play has **four** places — called **tracks** — where you can release your app:

| Track | Who can install | Good for |
|---|---|---|
| **Internal testing** 🏠 | Up to **100** people you choose (by email) | Quick tests by you and your team — usually ready within **minutes** |
| **Closed testing** 🔒 | People you **invite** (email lists or groups) | Testing with friends and real users — **required** for new personal accounts (12+ testers, 14 days) |
| **Open testing** 🔓 | **Anyone** who joins from your store page | A public "beta" version |
| **Production** 🌍 | **Everyone** | The real release! |

Testers install the app from **Google Play**, like any app — no cables, no unknown sources. And they get **updates** automatically. 😊

### Your first internal test 🏠

1. In the Play Console: **Test and release → Testing → Internal testing**.
2. **Testers** tab → **Create email list** → name it "Me and friends" → add email addresses (the Google accounts testers use on their phones — add **your own** too!) → **Save**. Check the box next to the list.
3. **Releases** tab (or the button **Create new release**).
4. The first time, Google asks about **Play App Signing** → keep the recommended choice (**Google-generated key**). ✅
5. **Upload** your `app-release.aab` (from 28.8). Google checks it: right signature? `versionCode` not used yet? 📦✅
6. **Release name:** filled in automatically (like `1 (1.0.0)`). Fine.
7. **Release notes** — what's new, for testers:

```
<en-US>
First version of Pocket Notes! 🎉
Please try everything and tell me about any problems.
</en-US>
```

   The `<en-US>` … `</en-US>` tags say which **language** the text is in. (Add more blocks for more languages.)

8. **Next** → read any warnings (yellow is OK; red must be fixed) → **Save and publish** (or **Start rollout**). 🚀
9. Back on the **Testers** tab, copy the **"Join on the web"** link and send it to your testers. They open it, tap **Accept**, and then install the app from Google Play. 📲

> 💡 **Is the uploaded bundle broken?** Common upload errors:
> - *"You uploaded an APK or Android App Bundle that was signed in debug mode"* → you uploaded a **debug** build. Use **Generate Signed App Bundle** with your **release** key.
> - *"Version code 1 has already been used"* → increase `versionCode` (28.6).
> - *"Your app must target an API level of at least …"* → increase `targetSdk` (and test!).

### The closed test for production access 🔒📅

For **new personal accounts**, do the same in **Closed testing** (create a track, add your **12+ testers**, upload a release). Ask your testers to **really use** the app for those 14 days — and to send you feedback! 💬 After 14 days, the Dashboard shows **Apply for production**: you answer a few questions about your test (who tested, what you learned, what you fixed).

### The pre-launch report 🤖

When you upload to a testing track, Google **automatically** installs your app on several **real** devices in its labs, taps around for a few minutes, and writes a **pre-launch report**: crashes 💥, screenshots on different phones 📱, **accessibility** suggestions ♿ (like "this button is too small"), and more. Find it under **Test and release → Pre-launch report**. Free robot testers! 🤖🎁 (Remember Chapter 27? 😉)

---

## 28.15 Going Live — Production! 🌍🎉

When your testing is done (and, for new personal accounts, production access is granted):

1. **Test and release → Production → Create new release**.
2. Upload a bundle — or **promote** the release you already tested (often a button like **Promote release** on the testing track). 
3. **Countries / regions:** choose where your app is available — for example **all** countries. 🌍
4. **Release notes:**

```
<en-US>
Welcome to Pocket Notes 1.0! 📝
Simple, colorful, private notes — with photos and a daily reminder.
</en-US>
```

5. **Staged rollout** 🪜 (optional, but smart): release to only a **part** of users first — for example **20%**. If everything is fine, increase to 50%, then **100%**. If a bad bug appears, only some users get it, and you can **halt** the rollout. 🛑
6. **Next → Send for review** (sometimes **Start rollout to Production**).

### Google's review 🔍

Google checks your app against its rules. This can take from **a few hours** to **several days** — the **first** app usually takes longer. ⏳ You'll get an **email** and see the status in the Play Console:

| Status | Meaning |
|---|---|
| **In review** 🔍 | Google is checking. Wait. ☕ |
| **Approved / Available on Google Play** ✅ | 🎉🎉🎉 Your app is live! |
| **Rejected** ❌ | Google explains **why** (and which rule). Fix it, upload a new version (higher `versionCode`!), and send it again. It happens to everyone — don't give up! 💪 |

When it's live — **search for your app on Google Play**. 🔍 There it is. **Your** app, made by **you**, available to anyone in the world. 🌍📱 Take a screenshot of that moment! 📸🥳

---

## 28.16 After Launch — Watching Your App 👀📊

Publishing is not the end — it's the **beginning** of your app's life. 🌱

### Android vitals — crashes in the real world 💥

Under **Monitor and improve → Android vitals** (names may differ), Google shows how your app behaves on **real users'** phones:

| Number | Meaning |
|---|---|
| **User-perceived crash rate** | How many daily users saw a **crash** 💥 |
| **User-perceived ANR rate** | How many saw an **"App isn't responding"** freeze 🥶 |

If these get too high, Google shows your app **less** in the store — and warns users. So check them regularly!

Click **Crashes and ANRs** to see the **stack traces** — **readable**, thanks to the R8 mapping inside your bundle. Now you know **exactly** what to do with them (Chapter 27, section 27.3)! 🕵️ Then: write a test that shows the bug (🔴), fix it (🟢), and send an update. 🔁

### Ratings and reviews ⭐

Users can give **1–5 stars** and write reviews. You can **reply** in the Play Console (**Ratings and reviews**).

| ✅ Do | ❌ Don't |
|---|---|
| Thank people for good reviews 🙏 | Argue or be rude, even if a review is unfair |
| For problems: say sorry, ask for details, tell them when it's fixed | Ask for 5 stars in exchange for something (not allowed!) |
| Learn from repeated complaints | Take it personally 😌 — every app gets some bad reviews |

### Statistics 📈

**Statistics** shows installs, uninstalls, countries, Android versions, devices… Useful to decide things like: "*Only 0.5% of my users have Android 7 — maybe I can raise `minSdk`.*" 🤔

---

## 28.17 Sending an Update 🔁

You fixed a bug or added a feature. Let's send version **1.0.1**:

**1. Increase the version** in `build.gradle.kts`:

```kotlin
versionCode = 2                    // 👈 was 1 — ALWAYS higher
versionName = "1.0.1"              // 👈 a bug fix → PATCH +1
```

**2. Test** — run the tests (Chapter 27) ✅ and try the **release** build (28.7) 📱.

**3. Build:** **Build → Generate Signed App Bundle or APK…** → same keystore, same key (the passwords are remembered if you checked the box) → **release** → **Create**.

**4. Upload:** **Production → Create new release** → upload the new `.aab` → release notes:

```
<en-US>
🐛 Fixed: the app could crash when searching with an empty note list.
✨ Small speed improvements.
</en-US>
```

**5.** Choose a **staged rollout** → **Send for review**.

Users get the update **automatically** (or with a tap in Google Play). Their notes are **safe** — the update keeps all data, because it's the **same app** (same `applicationId`, same signature). And if you changed the database, your **migrations** (Chapter 22/25) move the data to the new version. 🗄️✅

> 💡 **The update cycle:** 🐛 a bug report → 🧪 a test → 🔧 a fix → 🔢 a higher `versionCode` → 📦 build → 🚀 upload → 👀 watch vitals. Professional teams do this **every week or two**!

---

## 28.18 Why Apps Get Rejected — and How to Avoid It 🚫✅

| Reason | Example | How to avoid |
|---|---|---|
| **`com.example`** package | `com.example.notes` | Your own `applicationId` (28.3) |
| **Missing / wrong privacy policy** | No link, a broken link, or "we collect nothing" while a library sends data | A real, public, **true** policy (28.12) |
| **Data safety doesn't match the app** | Says "no data collected", but an analytics library sends data | Check **every** library |
| **Crashes or doesn't work** | Crashes at start, buttons do nothing | Test the **release** build (28.7), use the pre-launch report |
| **Misleading name, icon, or description** | "Best #1 FREE Notes", features that don't exist | Honest store listing (28.13) |
| **Copying others** | Another brand's name or logo, "Google Notes" | Your own name and icon |
| **Permissions without reason** | Asking for location in a notes app | Ask only for what you **really** use (Chapter 25) |
| **Target SDK too old** | `targetSdk` from several years ago | Keep it up to date (28.6) |
| **Reviewers can't get in** | Login required, no test account given | Fill **App access** (28.12) |

---

## 28.19 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| Lost the keystore or password 😱 | Can't sign updates | Request an **upload key reset** in the Play Console — and **back up** the new key twice! |
| Keystore pushed to Git (GitHub) | Others could sign apps as you | Remove it from Git, add `*.jks` to `.gitignore`, and request a key reset if the repository was public |
| Forgot to increase `versionCode` | *"Version code X has already been used"* | `versionCode` + 1 |
| Uploaded a debug build | *"…signed in debug mode"* | **Generate Signed App Bundle**, **release** variant |
| Never tested the release build | Works in debug, **crashes** for users (R8!) | Always try the release build first (28.7) |
| Left `signingConfig = signingConfigs.getByName("debug")` in `release` | Your "release" is signed with the debug key → rejected | Remove the line; sign with your release key |
| Changed `applicationId` after publishing | Google Play sees a **brand-new** app | Never change it after the first release |
| Changed `namespace` instead of `applicationId` | Still `com.example…` on Google Play; or many red errors | Change only `applicationId` (28.3) |
| Debug logs with private data in the release | Anyone with a cable can read them | R8 rule for `Log.d`/`Log.v` (28.7) + never log private data |
| Testers can't find the app | They didn't accept the invitation, or use another Google account on the phone | Send the **opt-in link**; use the **same** account as on the phone |
| Free app → want to make it paid | Not possible | Decide before publishing (28.11); use in-app purchases instead |

---

## 28.20 Release Checklist ✅🚀

Print it, stick it on your wall, use it for **every** release! 📌

| Before building | ✅ |
|---|---|
| All tests green (`.\gradlew test` + UI tests) | ☐ |
| Tried the app like a naughty user 😈 (rotation, dark mode, big font, no permission, no internet) | ☐ |
| `applicationId` is **yours** (not `com.example`) | ☐ |
| `versionCode` increased, `versionName` updated | ☐ |
| `targetSdk` meets Google's current requirement | ☐ |
| App icon + monochrome layer ✨ | ☐ |
| `isMinifyEnabled` + `isShrinkResources` on; release build tested on a phone | ☐ |
| No debug `signingConfig` in `release` | ☐ |

| Building and uploading | ✅ |
|---|---|
| Signed App Bundle (`app-release.aab`) with the **release** key | ☐ |
| Keystore + passwords backed up in **two** places, and **not** in Git | ☐ |
| Release notes written (short, friendly, honest) | ☐ |

| In the Play Console (first release) | ✅ |
|---|---|
| Privacy policy link (public, true) | ☐ |
| App access, ads, content rating, target audience, data safety, other declarations | ☐ |
| Store listing: name, short + full description, 512 icon, 1024×500 feature graphic, 4–8 screenshots, category, email | ☐ |
| Internal test → closed test (12+ testers × 14 days for new personal accounts) | ☐ |
| Pre-launch report checked | ☐ |
| Production with a staged rollout | ☐ |

---

## 28.21 Summary — What You Learned 🎓

| Topic | Key points |
|---|---|
| **Debug vs. release** 🆚 | Release = for users: optimized, signed with **your** key |
| **`applicationId`** 🛂 | Unique, never `com.example`, never changes after publishing; `namespace` is for code |
| **App name** 📛 | `strings.xml` (`app_name`) on the phone; up to 30 characters on Google Play |
| **Adaptive icon** 🎨 | Background + foreground (safe zone) + monochrome; Image Asset Studio; 512 px Play icon |
| **Versions** 🔢 | `versionCode` (+1 every upload, for computers), `versionName` (`MAJOR.MINOR.PATCH`, for humans), `targetSdk` (yearly requirement) |
| **R8** ✂️ | `isMinifyEnabled`, `isShrinkResources`, `proguard-rules.pro`, remove `Log.d`, keep rules, mapping file — **test the release build** |
| **Signing** 🔑 | Keystore (`.jks`), alias, passwords; **back up**, never in Git; Play App Signing = upload key + app signing key |
| **App Bundle** 🎁 | `.aab` for Google Play → small APKs per device; APK for direct sharing |
| **Play Console** 🏪 | Account (25 USD once, identity check), create app, App content forms, Data safety, store listing |
| **Tracks** 👫 | Internal → closed (12 × 14 days for new personal accounts) → open → production; pre-launch report |
| **Launch and after** 🌍 | Staged rollout, review, Android vitals, reviews, statistics, updates |

---

## 28.22 Practice Time 🏋️

### Task 1: Good ID or bad ID? 🛂
Which of these `applicationId`s can be used on Google Play? For the bad ones, say **why**.
1. `com.example.doggallery`
2. `io.github.anacodes.doggallery`
3. `com.ana-silva.jokes`
4. `jokemachine`
5. `com.anasilva.2048game`
6. `com.anasilva.joke_machine`

### Task 2: Version numbers 🔢
Your app is at `versionCode = 7`, `versionName = "1.3.2"`. What are the next values for: **(a)** a small bug fix, **(b)** then a new feature, **(c)** then a complete redesign?

### Task 3: A short description 🐶
Write a **short description** (max 80 characters) for the **Dog Gallery** app (Chapter 20). Count the characters!

### Task 4: Spot the problems 🔍
What's wrong with this store listing?

> **Name:** `#1 BEST Free Notes App - like Google Keep`
> **Short description:** `notes notes notes app notes best notes free notes`
> **Data safety:** "No data collected" — but the app includes an analytics library.

### Task 5: Release notes ✍️
Version 1.1.0 of Pocket Notes adds **sorting by color** 🎨 and fixes **the reminder not appearing after restarting the phone**. Write the release notes (with language tags).

### Task 6: Keystore safety 🔑
Your friend says: "*I'll put my keystore in my public GitHub repository, so I never lose it!*" What do you tell them? What should they do instead?

---

### Answers

**Task 1:**

| ID | OK? | Why |
|---|---|---|
| `com.example.doggallery` | ❌ | `com.example` is not allowed on Google Play. |
| `io.github.anacodes.doggallery` | ✅ | A reversed address that belongs to Ana. |
| `com.ana-silva.jokes` | ❌ | `-` is not allowed. Use `com.anasilva.jokes` or `com.ana_silva.jokes`. |
| `jokemachine` | ❌ | Needs at least **two** parts with a dot (`com.anasilva.jokemachine`). |
| `com.anasilva.2048game` | ❌ | A part can't **start** with a digit. Use `com.anasilva.game2048`. |
| `com.anasilva.joke_machine` | ✅ | `_` is allowed. |

**Task 2:**

| Step | `versionCode` | `versionName` |
|---|---|---|
| (a) bug fix | 8 | `1.3.3` |
| (b) new feature | 9 | `1.4.0` (PATCH goes back to 0) |
| (c) redesign | 10 | `2.0.0` (MINOR and PATCH go back to 0) |

`versionCode` simply goes +1 every time, whatever the change is.

**Task 3** (one possible answer):

```
Endless cute dog photos 🐶 Pick a breed, scroll, and tap to see them big!
```

That's about 72 characters — under 80. ✅ (Emojis are fine in the **description**, just not to grab attention in the **name**.)

**Task 4:**

1. **Name:** "#1", "BEST", and "Free" are not allowed in the name (ranking and price claims). "like Google Keep" uses **another company's** product name. ❌ → Use for example `Pocket Notes – Simple Notes`.
2. **Short description:** **keyword spam** — repeating words to trick the search. ❌ → Write one honest sentence.
3. **Data safety:** **false**! Analytics libraries **send data** off the device → that's "collected". The form must say which data the library collects (for example app interactions, device IDs), and the privacy policy must explain it. ❌ This can get the app **removed**.

**Task 5:**

```
<en-US>
✨ New: sort your notes by color 🎨
🐛 Fixed: the daily reminder now comes back after restarting your phone.
Thank you for using Pocket Notes! 💛
</en-US>
```

(With `versionCode` + 1 and `versionName = "1.1.0"` — a new feature → MINOR.)

**Task 6:** **Never!** 🚫 A public repository means **anyone** can download the keystore. If they also guess or find the password, they can sign apps **as you**. Even a **private** repository is risky (it's shared with tools and people, and might become public one day). Instead: keep the `.jks` **outside** the project, add `*.jks` to `.gitignore`, and back it up in **two** safe places — for example a USB stick at home and a private cloud folder — with the passwords in a password manager. 🔐💾💾

---

## 28.23 Challenges 🚀

### Challenge 1: Publish a second app 🐶 ⭐⭐
Publish **Dog Gallery** (Chapter 20) to **internal testing**. This app uses the **internet** — think about the **Data safety** form: the app downloads pictures, but does it **send** any user data? Read Google's help pages and decide carefully. Remember: Retrofit and Coil are fine with R8, but **test the release build**!

### Challenge 2: Sign automatically with `keystore.properties` 🔑 ⭐⭐⭐
Typing passwords every time is boring. Create a file `keystore.properties` in the project's **root** folder (and add it to `.gitignore`!):
```
storeFile=C:/keys/pocket-notes-upload.jks
storePassword=...
keyAlias=upload
keyPassword=...
```
Then, in `build.gradle.kts`, load it with `java.util.Properties`, create a `signingConfigs { create("release") { ... } }` block that reads the four values, and use `signingConfig = signingConfigs.getByName("release")` in the `release` build type. Now **Build → Generate Signed App Bundle** isn't needed — **Build → Build Bundle(s) / APK(s) → Build Bundle(s)** with the **release** variant makes a signed bundle. Hint: make it work even when the file **doesn't** exist (for example on a friend's computer) — then just skip the signing config.

### Challenge 3: Speak another language 🌐 ⭐⭐⭐
Move all the texts of Pocket Notes into `res/values/strings.xml` and use `stringResource(R.string.…)` in Compose. Then add a translation: right-click `strings.xml` → **Open Translations Editor** → 🌐 **Add Locale** (for example Spanish or your own language). Change the phone's language and watch the app change! Also add a **translated store listing** in the Play Console.

### Challenge 4: Ask for a review politely ⭐⭐
Use Google's **In-App Review API** (the Play **review** library) to show the small "Rate this app" window **inside** the app — for example after the user has written 10 notes. Read the official guide: Google decides **when** the window really appears (to protect users from too many requests), so your code must work even if it doesn't.

### Challenge 5: A robot that tests every change 🤖 ⭐⭐⭐
If your project is on GitHub, create a **GitHub Actions** workflow that runs `./gradlew test` every time you push code. A red ❌ next to your commit means a test broke — before any user sees it!

---

## 28.24 The End of the Book — and a New Beginning 🎓🌅

Take a deep breath. 😮‍💨 Look back at where you started.

In **Chapter 1**, you installed Android Studio and maybe didn't know what a variable was. Now you have **published an app** on Google Play. 🌍📱 That's an **enormous** journey — and **you** did it, chapter by chapter, line by line. 👏👏👏

### What you learned 🗺️

| Part | You learned… |
|---|---|
| **1 — Getting Started** 🚀 | Installing Android Studio and running your very first app |
| **2 — The Kotlin Language** 🗣️ | Variables, functions, null safety, lists, classes, lambdas, enums, sealed classes |
| **3 — Building Screens With Jetpack Compose** 🎨 | Composables, layouts, Material 3, state, user input, lists, Scaffold and pop-ups — and the Tip Calculator |
| **4 — Many Screens and App Structure** 🏗️ | Navigation, the lifecycle, ViewModels, MVVM and repositories — and the Quiz app |
| **5 — Data, Internet, and Saving** 🌐💾 | Coroutines, Flow, Retrofit, Coil, DataStore, Room, Hilt — and the Notes app |
| **6 — Phone Features and Polish** ✨ | Permissions, location, camera, notifications, WorkManager, animations and gestures |
| **7 — Testing and Sharing Your App** 🏁 | Debugging, unit tests, UI tests — and publishing on Google Play |

That's the **same** toolbox professional Android developers use every day. 🧰 Really.

### Where to go next? 🧭

You're not a beginner anymore. Here are some paths — choose what makes you **curious**:

| Path | What it is |
|---|---|
| **Build YOUR app** 💡 | The best teacher. Think of something **you** or your family need — a habit tracker, a recipe app for grandma, a game for your little brother. Build it, publish it. You'll learn more than from any book. |
| **Read real code** 📖 | Google's open-source **"Now in Android"** app on GitHub shows how a big, modern Compose app is built — with everything from this book, and more. |
| **More Jetpack** 🧩 | **Paging** (endless lists from the internet), **Glance** (home-screen **widgets**), **CameraX** (your own camera screen), **Media3** (audio and video). |
| **Other screens** ⌚📺🚗 | Compose works on **Wear OS** (watches), and Android runs on **TVs** and **cars** too. |
| **Kotlin everywhere** 🌐 | **Kotlin Multiplatform** and **Compose Multiplatform** let you share code (and even screens) with **iOS**, desktop, and the web. |
| **A backend** ☁️ | Sync notes between phones with your own server — or with services like **Firebase**. |
| **Stay up to date** 📰 | **developer.android.com** (guides and codelabs), **kotlinlang.org**, the **Android Developers** YouTube channel and blog. Android changes every year — keep learning a little, often. 🌱 |

### Some last advice 💛

1. **You will get stuck.** Everyone does — every day, even experts. Read the error, search, take a break, try again. Getting **un**stuck is the real skill. 🧗
2. **Small steps.** Big apps are just many small pieces — like this book. One screen, one feature, one test at a time. 🧱
3. **Finish things.** A small, **finished** app teaches more than ten big, half-finished ones. 🏁
4. **Share and ask.** Show your apps to friends, join developer communities, help others who are one step behind you. Teaching is the best way to learn. 🤝
5. **Have fun.** You can now turn ideas into apps that anyone in the world can use. That's a **superpower**. 🦸

---

> 🎉 **Congratulations — you finished the book!** 🎉
>
> From "Hello, World!" to a published app on Google Play. 🌍📱
> Thank you for learning with this book. Now go and build something **amazing**. 🚀💛
>
> **Happy coding!** 👩‍💻👨‍💻
