# Chapter 1: Getting Ready — Install Android Studio and Make Your First App

> **What you will learn in this chapter**
>
> 1. What Android, Kotlin, and Android Studio are
> 2. How to install Android Studio on your computer
> 3. How to make your first app
> 4. What every file in your new project does
> 5. What every line of your first code means
> 6. How to run your app on a pretend phone (emulator)
> 7. How to run your app on your real phone
> 8. How to fix common problems
>
> **Time needed:** about 1 to 2 hours (most of it is waiting for downloads)

---

## 1.1 Some Easy Words First

Before we start, let us learn some words. Do not worry if you forget them. You can come back here any time.

| Word | Simple meaning | Example from real life |
|---|---|---|
| **App** | A program that runs on a phone. | WhatsApp, YouTube, Calculator |
| **Android** | The "brain software" inside many phones. It runs the apps. | Samsung, Pixel, Xiaomi phones use Android |
| **Kotlin** | A language we use to talk to the computer. We write instructions in Kotlin. | Like English is a language for people, Kotlin is a language for computers |
| **Code** | The instructions we write. | A recipe is "code" for cooking |
| **Android Studio** | The program on your computer where you write and test apps. | Like a kitchen where you cook |
| **Emulator** | A pretend phone that lives inside your computer. | Like a toy phone on your screen |
| **Jetpack Compose** | The modern way to draw screens (buttons, text, pictures) in Android apps. | Like LEGO blocks for building screens |
| **Project** | One folder that holds everything for one app. | Like a school bag for one subject |
| **Build** | Android Studio turning your code into a real app. | Like baking: ingredients (code) → cake (app) |
| **Run** | Starting your app on a phone or emulator. | Like turning on a TV |

### Why Kotlin?

Google (the company that makes Android) says: **"Kotlin first."**
This means Google wants new Android apps written in Kotlin.
Kotlin is:

- **Short** — you write less code.
- **Safe** — it helps stop many mistakes before they happen.
- **Modern** — almost all new Android apps today use it.

### Why Jetpack Compose?

Long ago, Android screens were made with a different system called **XML layouts**.
Today, Google recommends **Jetpack Compose**.
With Compose, you build the screen **with Kotlin code only**. You do not need a second language.

> 💡 **Remember:** In this whole book we use **Kotlin + Jetpack Compose**. This is what real Android developers use today.

---

## 1.2 Check Your Computer

Android Studio is a big program. Your computer needs to be strong enough.

| Thing | Minimum (it will work, but slow) | Better (it will work nicely) |
|---|---|---|
| Operating system | Windows 10 (64-bit) | Windows 11 (64-bit) |
| RAM (memory) | 8 GB | 16 GB or more |
| Free disk space | 8 GB | 30 GB or more, on an SSD |
| Screen | 1280 × 800 | 1920 × 1080 |
| Internet | Needed for the first setup | Fast internet helps |

### How to check your RAM on Windows

1. Press the **Windows key** and the **Pause/Break** key together.
   *Or:* right-click the **Start** button → click **System**.
2. Look for **"Installed RAM"**.
3. You will see something like `16.0 GB`.

### How to check free disk space

1. Open **File Explorer** (the yellow folder icon).
2. Click **This PC** on the left side.
3. Look at your **C:** drive. It shows how much space is free.

> ⚠️ **If you have less than 8 GB RAM:** Android Studio may be very slow. The emulator (pretend phone) may not work well. In that case, use your **real phone** to test apps (see section 1.9).

---

## 1.3 Download Android Studio

Android Studio is **free**. Only download it from the official Google website.

### Steps

1. Open your web browser (Chrome, Edge, Firefox…).
2. Go to: **https://developer.android.com/studio**
3. Click the big green button **"Download Android Studio"**.
4. A box with rules (Terms and Conditions) opens.
5. Scroll down, tick the box **"I have read and agree…"**.
6. Click **Download**.
7. Wait. The file is about 1 GB. It may take some minutes.

> 💡 The page always gives you the **newest version**. Each version has an animal name (like "Ladybug", "Meerkat", "Narwhal"). The name does not matter. Newest is best.

> ⚠️ **Never** download Android Studio from other websites. They can have viruses.

---

## 1.4 Install Android Studio

The file you downloaded has a name like `android-studio-xxxx-windows.exe`.

### Steps

1. Open your **Downloads** folder.
2. **Double-click** the `.exe` file.
3. Windows may ask: *"Do you want to allow this app to make changes?"* → click **Yes**.
4. The **Setup** window opens. Click **Next**.
5. You see a list of things to install:
   - ✅ **Android Studio**
   - ✅ **Android Virtual Device** (this is the emulator — keep it ticked!)
   Click **Next**.
6. Choose where to install. The normal place is fine:
   `C:\Program Files\Android\Android Studio`
   Click **Next**.
7. Click **Install**. Wait until the green bar is full.
8. Click **Next**, then **Finish**. Keep the box **"Start Android Studio"** ticked.

### First start — the Setup Wizard

When Android Studio opens for the first time, a helper called the **Setup Wizard** appears.

1. **"Import Android Studio Settings"** → choose **Do not import settings** → **OK**.
   (You have no old settings. You are new!)
2. **"Help improve Android Studio"** → choose what you like. Both are OK.
3. **Welcome** screen → click **Next**.
4. **Install Type** → choose **Standard** → **Next**.
   *(Standard means "use the normal, good settings". Perfect for beginners.)*
5. **Select UI Theme** → pick **Dark** or **Light**. This is only colors. Click **Next**.
6. **Verify Settings** → it shows what will be downloaded. Click **Next**.
7. **License Agreement** → on the left you see some items. Click each one and choose **Accept**. Then click **Finish**.
8. Now it downloads the **Android SDK** (tools to build apps). This can take **10–30 minutes**. Wait patiently. ☕
9. When it says done, click **Finish**.

### What is the Android SDK?

**SDK** means **Software Development Kit**.
Think of it as a **toolbox**. Inside the toolbox are:

- Tools to turn your code into an app
- Pieces of Android that your app needs
- The emulator (pretend phone)

Android Studio is the **kitchen**. The SDK is the **pots, pans, and knives** in the kitchen.

---

## 1.5 Make Your First Project

Now the fun part! 🎉

You should see the **Welcome to Android Studio** window.

### Steps

1. Click **New Project**.
2. A window shows many **templates** (ready-made starting points).
   On the left, make sure **Phone and Tablet** is selected.
3. Click **Empty Activity**.
   - It has a picture of a phone with the Compose logo.
   - ⚠️ Do **not** choose "Empty Views Activity". That is the old XML way.
4. Click **Next**.

### Fill in the project details

You now see a form. Here is what each box means:

| Box | What to type | What it means |
|---|---|---|
| **Name** | `My First App` | The name people see under the app icon. |
| **Package name** | `com.example.myfirstapp` | A unique ID for your app. Like a home address. No two apps in the Play Store can have the same one. |
| **Save location** | `C:\roy1\learn_2\MyFirstApp` (or any folder you like) | Where the project folder goes on your computer. |
| **Minimum SDK** | Keep the default (for example **API 24: Android 7.0**) | The **oldest** Android version your app will work on. |
| **Build configuration language** | **Kotlin DSL (build.gradle.kts)** | The language for the "settings files". Kotlin DSL is the modern choice. |

#### More about "Package name"

The package name is written **backwards** like a website address:

```
com.example.myfirstapp
 │     │        │
 │     │        └── your app name (small letters, no spaces)
 │     └── your company or your name
 └── "com" like in ".com"
```

If your website was `roy.com`, you could use `com.roy.myfirstapp`.
For learning, `com.example...` is perfectly fine.

#### More about "Minimum SDK"

Every Android version has a number called the **API level**.

| Android version | API level |
|---|---|
| Android 7.0 | 24 |
| Android 8.0 | 26 |
| Android 10 | 29 |
| Android 12 | 31 |
| Android 14 | 34 |
| Android 15 | 35 |

If you choose API 24, your app works on **Android 7.0 and every newer version**.
Android Studio shows you a message like *"Your app will run on approximately 98% of devices."* That is great.

5. Click **Finish**.

### Wait for Gradle

Now Android Studio is busy. At the bottom of the window you see small moving text, like:

```
Gradle sync in progress...
```

**What is Gradle?**
Gradle is a **helper robot** 🤖. Its job:

1. Download all the extra pieces your app needs (we call them **libraries** or **dependencies**).
2. Put your code and the pieces together.
3. Make the final app file (called an **APK**).

The **first time**, Gradle downloads a lot. It can take **5–15 minutes**. Later it is much faster.

✅ You know it is finished when the bottom bar is quiet and there are **no red errors**.

---

## 1.6 A Tour of Android Studio

Android Studio has many buttons. Do not be scared. You only need a few at the start.

```
┌──────────────────────────────────────────────────────────────────┐
│  [≡ Menu]  MyFirstApp  [app ▾] [Pixel ▾]  [▶ Run] [🐞] [■ Stop] │  ← 1. Toolbar
├────────────┬─────────────────────────────────────┬───────────────┤
│            │                                     │               │
│  2.        │   3. EDITOR                         │  4. PREVIEW   │
│  PROJECT   │   (you write code here)             │  (see your    │
│  (files)   │                                     │   screen)     │
│            │                                     │               │
├────────────┴─────────────────────────────────────┴───────────────┤
│  5. BOTTOM TOOLS: Build, Logcat, Terminal, Problems              │
└──────────────────────────────────────────────────────────────────┘
```

| Number | Name | What it does |
|---|---|---|
| 1 | **Toolbar** | The ▶ green **Run** button starts your app. Next to it you choose which phone. |
| 2 | **Project window** | Shows all your files, like File Explorer. |
| 3 | **Editor** | The big white (or dark) area. You read and write code here. |
| 4 | **Preview** | Shows a picture of your screen **without** running the app. |
| 5 | **Bottom tools** | Messages from Android Studio. **Logcat** shows messages from your running app. **Build** shows errors. |

### Change the Project view

At the top of the Project window there is a small drop-down. It usually says **Android**.

- **Android** view (default) → shows only the important files. **Use this one.** ✅
- **Project** view → shows every single file. Too much for now.

---

## 1.7 What Is Inside My Project?

In the **Android** view, open the folders by clicking the small arrows ▸. You will see:

```
app
 ├── manifests
 │    └── AndroidManifest.xml          ← the app's ID card
 ├── kotlin+java
 │    └── com.example.myfirstapp
 │         ├── MainActivity.kt          ← YOUR MAIN CODE ⭐
 │         └── ui.theme
 │              ├── Color.kt            ← colors of the app
 │              ├── Theme.kt            ← the app's style
 │              └── Type.kt             ← fonts and text sizes
 └── res                                ← "resources": pictures, words, icons
      ├── drawable                      ← pictures and shapes
      ├── mipmap                        ← the app icon
      ├── values
      │    ├── strings.xml              ← words/text used in the app
      │    └── themes.xml               ← basic style for Android
      └── xml                           ← extra settings files
Gradle Scripts
 ├── build.gradle.kts (Project: MyFirstApp)   ← settings for the whole project
 ├── build.gradle.kts (Module :app)           ← settings for your app ⭐
 ├── libs.versions.toml                       ← list of library versions
 ├── settings.gradle.kts                      ← which parts are in the project
 └── gradle.properties / local.properties     ← small extra settings
```

Let us look at the most important files one by one.

### 1.7.1 `MainActivity.kt` — your main code ⭐

- `.kt` means it is a **Kotlin** file.
- **Activity** means **one screen** of your app (more details in 1.8).
- **Main** means it is the **first** screen that opens.

We will read every line of this file in section 1.8.

### 1.7.2 `AndroidManifest.xml` — the app's ID card

Every app has exactly one manifest. It tells the phone:

- What is the app's name?
- What is the app's icon?
- Which screen opens first?
- What permissions does the app need? (for example: internet, camera)

Here is a short version of it, with explanations:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.MyFirstApp">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>
</manifest>
```

Line by line:

| Line | Meaning |
|---|---|
| `<manifest ...>` | "This is the ID card." Everything is inside it. |
| `<application ...>` | "Here is information about the whole app." |
| `android:icon="@mipmap/ic_launcher"` | "Use the picture called `ic_launcher` from the `mipmap` folder as the app icon." The `@` means "look in the res folder". |
| `android:label="@string/app_name"` | "The app name is the text called `app_name` in `strings.xml`." |
| `android:theme="..."` | "Use this basic style." |
| `<activity android:name=".MainActivity"` | "My app has a screen called `MainActivity`." The dot `.` means "inside my package". |
| `android:exported="true"` | "Other apps (like the phone's home screen) are allowed to open this screen." |
| `<intent-filter>` | "Here is **when** this screen should open." |
| `action ... MAIN` | "This is the **main** entrance of the app." |
| `category ... LAUNCHER` | "Show an icon for this screen in the phone's app list." |

> 💡 **Simple idea:** `MAIN` + `LAUNCHER` together say: *"When the user taps my app icon, open MainActivity."*

You will **not** change this file much at the start. Android Studio writes it for you.

### 1.7.3 `strings.xml` — the words of your app

```xml
<resources>
    <string name="app_name">My First App</string>
</resources>
```

| Part | Meaning |
|---|---|
| `<resources>` | "Here is a list of resources." |
| `<string name="app_name">` | "This text has the nickname `app_name`." |
| `My First App` | The actual text. |

**Why put text here instead of in the code?**
Because later you can translate your app. You make a second `strings.xml` in Hindi, Spanish, Arabic… and Android picks the right one by itself. 🌍

### 1.7.4 `build.gradle.kts (Module :app)` — your app's settings ⭐

This is the settings file that Gradle (the helper robot) reads. Here is a short version:

```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
}

android {
    namespace = "com.example.myfirstapp"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.myfirstapp"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
    }

    buildFeatures {
        compose = true
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.material3)
}
```

> ℹ️ Your numbers (like `35`) may be different. That is OK. Android Studio puts in the newest good numbers for you.

Let us explain each part:

**`plugins { ... }`** — "extra powers" for Gradle.

| Line | Meaning |
|---|---|
| `android.application` | "This project makes an **Android app**." |
| `kotlin.android` | "We write the code in **Kotlin**." |
| `kotlin.compose` | "We use **Jetpack Compose** for screens." |

**`android { ... }`** — settings about Android.

| Line | Meaning |
|---|---|
| `namespace = "com.example.myfirstapp"` | The package name for your code files. |
| `compileSdk = 35` | "Build my app using the tools of Android API 35." Use the newest. |
| `applicationId = "..."` | The unique ID of your app in the Play Store. Never change it after you publish! |
| `minSdk = 24` | The oldest Android your app works on (we chose this earlier). |
| `targetSdk = 35` | "My app is tested and made for API 35." |
| `versionCode = 1` | A number for **computers**. Make it bigger every time you publish a new version: 1, 2, 3… |
| `versionName = "1.0"` | A version text for **people**. Like "1.0", "1.1", "2.0". |
| `buildFeatures { compose = true }` | "Turn ON Jetpack Compose." |

**`dependencies { ... }`** — the extra libraries your app needs.

A **library** is code that someone else already wrote, so you don't have to.
Example: you don't build your own car engine. You buy one. 🚗

| Line | What the library gives you |
|---|---|
| `core.ktx` | Helpful small Kotlin tools for Android. |
| `activity.compose` | Lets an Activity show a Compose screen. |
| `compose.bom` | "Bill of Materials" — makes sure all Compose libraries have versions that **work well together**. |
| `ui` | The basic Compose building blocks. |
| `material3` | Beautiful ready-made parts (buttons, cards, text) in Google's **Material 3** design. |

`implementation(...)` means: *"My app needs this library to work."*

### 1.7.5 `libs.versions.toml` — the version list

You saw names like `libs.androidx.core.ktx`. Where do they come from?
From this file! It is a **list of all libraries and their version numbers**, in one place.

```toml
[versions]
coreKtx = "1.15.0"

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }
```

| Part | Meaning |
|---|---|
| `[versions]` | A list of version numbers with nicknames. |
| `coreKtx = "1.15.0"` | "The nickname `coreKtx` means version 1.15.0." |
| `[libraries]` | A list of libraries. |
| `androidx-core-ktx = {...}` | "The library with the nickname `androidx-core-ktx` is `androidx.core:core-ktx`, and its version is whatever `coreKtx` says." |

In `build.gradle.kts`, the dashes `-` become dots `.` → `libs.androidx.core.ktx`.

> 💡 **Why is this good?** When you want to update a library, you change the number **in one place only**.

> ⚠️ **Important rule:** After you change any Gradle file, Android Studio shows a yellow bar: **"Sync Now"**. Always click it!

---

## 1.8 Your First Code — Every Line Explained ⭐

Open `MainActivity.kt` (double-click it). You will see code like this:

```kotlin
package com.example.myfirstapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.myfirstapp.ui.theme.MyFirstAppTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyFirstAppTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    Greeting(
                        name = "Android",
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MyFirstAppTheme {
        Greeting("Android")
    }
}
```

This looks like a lot. But we will go **slowly**, piece by piece. 🐢

> ℹ️ In this chapter we explain the **idea** of each line. In Chapters 2–4 you will learn Kotlin and Compose in full detail, and everything here will become very clear.

---

### Part A: The `package` line

```kotlin
package com.example.myfirstapp
```

- `package` = "This file lives in this **folder name**."
- It is like writing your **address** at the top of a letter.
- It must match the folder where the file is. Android Studio does this for you.

---

### Part B: The `import` lines

```kotlin
import android.os.Bundle
import androidx.activity.ComponentActivity
...
```

- `import` = "I want to **use** something from another place."
- Think of a big library 📚. You can't carry all the books. You only take the books you need.
- Each `import` line takes **one book** (one tool).

Examples:

| Import | We take this tool | Used for |
|---|---|---|
| `android.os.Bundle` | `Bundle` | A small bag of saved information |
| `androidx.compose.material3.Text` | `Text` | Showing words on the screen |
| `androidx.compose.ui.Modifier` | `Modifier` | Changing size, space, color of things |
| `androidx.compose.runtime.Composable` | `@Composable` | Marking functions that draw the screen |

> 💡 **Good news:** You almost never write imports yourself. When you type a word like `Text`, Android Studio offers to add the import. Press **Alt + Enter** on a red word to add the missing import.

---

### Part C: The Activity (the screen)

```kotlin
class MainActivity : ComponentActivity() {
```

Let us break it into small pieces:

| Piece | Meaning |
|---|---|
| `class` | "I am making a new **kind of thing**." A class is like a **blueprint** (a drawing of a house before you build it). |
| `MainActivity` | The name of our new thing. |
| `:` | Read it as "**is a kind of**". |
| `ComponentActivity()` | A ready-made screen that Android gives us. |
| `{` | "The inside of my class starts here." |

So the whole line means:
> *"I am making `MainActivity`. It **is a kind of** `ComponentActivity` (a screen)."*

**Real-life example:**
"A **puppy** is a kind of **dog**." The puppy gets everything a dog has (4 legs, a tail, barking). Then it can add its own things.
In the same way, `MainActivity` gets everything a screen has, and then we add our own things.

---

### Part D: `onCreate` — "when the screen is born"

```kotlin
    override fun onCreate(savedInstanceState: Bundle?) {
```

| Piece | Meaning |
|---|---|
| `fun` | "Here is a **function**." A function is a **list of steps** with a name. Like a recipe called "Make Tea". |
| `onCreate` | The function's name. Android calls it **automatically** when the screen is **created** (born). |
| `override` | "The parent (`ComponentActivity`) already has `onCreate`. I am **replacing** it with my own version." |
| `savedInstanceState: Bundle?` | Some saved information Android gives us (we don't need it now). |
| `?` after `Bundle` | "This can be **empty** (null)." You will learn this in Chapter 3. |

**Real-life example:**
When a baby is born, the doctor does some things **automatically**: checks breathing, weighs the baby.
When your screen is born, Android **automatically** runs `onCreate`. So we put our "first things to do" inside it.

---

### Part E: `super.onCreate(...)`

```kotlin
        super.onCreate(savedInstanceState)
```

- `super` = "the **parent**" (here: `ComponentActivity`).
- This line says: *"Parent, please do your normal `onCreate` steps first."*
- The parent does important hidden work. **Never delete this line.**

**Real-life example:** Before you decorate a cake, the cake must be baked. `super.onCreate` bakes the cake. 🎂 Then we decorate.

---

### Part F: `enableEdgeToEdge()`

```kotlin
        enableEdgeToEdge()
```

- Modern phones show apps from **edge to edge**: under the top status bar (time, battery) and the bottom bar.
- This line says: *"Let my app use the **whole** screen."*
- This is the modern Android style.

---

### Part G: `setContent { ... }` — "this is what to show"

```kotlin
        setContent {
            ...
        }
```

- `setContent` = "Put this **Compose content** on the screen."
- Everything inside the `{ }` is what the user will **see**.
- This is the **door** between the old Android world (Activity) and the new Compose world.

---

### Part H: `MyFirstAppTheme { ... }` — the style

```kotlin
            MyFirstAppTheme {
                ...
            }
```

- A **theme** is the **style** of the app: colors, fonts, shapes.
- Everything inside the `{ }` uses this style.
- It comes from the file `ui/theme/Theme.kt`. Android Studio made it for you.
- It also supports **dark mode** automatically! 🌙

**Real-life example:** A school uniform. Every student inside the school wears the same colors.

---

### Part I: `Scaffold` — the frame of the screen

```kotlin
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    ...
                }
```

| Piece | Meaning |
|---|---|
| `Scaffold` | A ready-made **frame** for a screen. Later it can hold a top bar, bottom bar, and a floating button. |
| `modifier = Modifier.fillMaxSize()` | "Make the Scaffold **fill the whole screen**." |
| `{ innerPadding -> ... }` | Scaffold gives us a value called `innerPadding`. It is the **safe space** away from the status bar and bottom bar, so our text is not hidden under them. |

**Real-life example:** A **scaffold** on a building is the frame workers stand on. Here, it is the frame our screen is built on. 🏗️

The `->` arrow means: *"Here is the value you gave me (`innerPadding`). Now here are my steps."*

---

### Part J: Calling `Greeting`

```kotlin
                    Greeting(
                        name = "Android",
                        modifier = Modifier.padding(innerPadding)
                    )
```

- We **use** (call) a function named `Greeting`. (It is written lower in the file.)
- We give it two things:
  - `name = "Android"` → the word to greet. The quotes `" "` mean it is **text** (we call text a **String**).
  - `modifier = Modifier.padding(innerPadding)` → "Add the safe space around it."

**Real-life example:** You tell a friend: *"Please say hello to **Android**, and stand **a little away from the wall**."*

---

### Part K: The `Greeting` function — our own screen part

```kotlin
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}
```

**Line 1: `@Composable`**

- The `@` sign is a **label** (we call it an **annotation**).
- `@Composable` means: *"This function **draws something on the screen**."*
- Every function that shows UI (user interface) **must** have this label.

**Line 2: `fun Greeting(name: String, modifier: Modifier = Modifier)`**

| Piece | Meaning |
|---|---|
| `fun Greeting` | A function named `Greeting`. |
| `name: String` | It needs one input called `name`. It must be **text** (`String`). |
| `modifier: Modifier = Modifier` | A second input called `modifier`. The `= Modifier` part means: *"If nobody gives one, use an empty, normal Modifier."* This is called a **default value**. |

**Lines 3–6: `Text(...)`**

- `Text` is a ready-made Compose part that **shows words**.
- `text = "Hello $name!"` → the words to show.
  - The `$` sign means: *"Put the **value** of `name` here."*
  - If `name` is `"Android"`, the text becomes **`Hello Android!`**
  - This is called **string templates**.
- `modifier = modifier` → "Use the modifier we were given."
  - Left `modifier` = the box's name in `Text`.
  - Right `modifier` = our value.

**Tiny example of `$`:**

```kotlin
val name = "Roy"
println("Hello $name!")   // prints: Hello Roy!
```

---

### Part L: The Preview function

```kotlin
@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MyFirstAppTheme {
        Greeting("Android")
    }
}
```

| Line | Meaning |
|---|---|
| `@Preview(showBackground = true)` | "Show a **picture** of this in the Preview window. Use a white background." |
| `@Composable` | It draws UI. |
| `fun GreetingPreview()` | A function only for the preview. It has no inputs. |
| `MyFirstAppTheme { Greeting("Android") }` | Draw `Greeting` with our style. |

**Why is this useful?**
You can **see** your screen in Android Studio **without running the app**. It is very fast. ⚡

**How to see the preview:**

1. At the top-right of the editor, click **Split** (half code, half picture).
2. If you see "Build & Refresh", click it.
3. You will see a white box saying **Hello Android!**

> 💡 The Preview function is **only for you**, the developer. Users never see it.

---

### The big picture — how it all connects

```
User taps the app icon
        │
        ▼
AndroidManifest.xml says: "open MainActivity"
        │
        ▼
Android creates MainActivity and calls onCreate()
        │
        ▼
setContent { ... }  → "show this Compose screen"
        │
        ▼
MyFirstAppTheme → gives colors and fonts
        │
        ▼
Scaffold → gives the frame and safe space
        │
        ▼
Greeting("Android") → Text("Hello Android!")
        │
        ▼
📱 Screen shows:  Hello Android!
```

---

## 1.9 Run Your App on an Emulator (Pretend Phone)

### Step 1: Make a virtual phone

Often, Android Studio already made one for you during setup. Let us check.

1. Click the menu **View → Tool Windows → Device Manager**.
   (Or click the small phone icon on the right side.)
2. Do you see a phone in the list, like **"Medium Phone API 35"** or **"Pixel ..."**?
   - **Yes** → great! Skip to Step 2.
   - **No** → continue below.
3. Click the **+** button → **Create Virtual Device**.
4. Choose a phone, for example **Pixel 8** or **Medium Phone**. Click **Next**.
5. Choose a **system image** (the Android version for the pretend phone).
   - Pick the one at the top with the newest API (it says **Recommended**).
   - If there is a ⬇️ download icon next to it, click it and wait.
6. Click **Next**, then **Finish**.

### Step 2: Run the app

1. At the top toolbar, check the device drop-down. Choose your virtual phone.
2. Click the green **▶ Run** button. (Or press **Shift + F10**.)
3. Wait. The **first** time:
   - Gradle builds your app (1–3 minutes).
   - The emulator starts (it looks like a phone turning on).
4. 🎉 Your app opens. It shows: **Hello Android!**

> ⏳ The emulator is slow the first time. Leave it open. Next time you click Run, it is much faster.

### Step 3: Play with the emulator

- Use your **mouse** like a finger. Click = tap. Drag = swipe.
- The buttons on the side panel: power, volume, rotate, back, home.
- Swipe up from the bottom to see the app list. You will find **My First App** there with its icon!

---

## 1.10 Run Your App on Your Real Phone

Testing on a real phone is great. It is often **faster** than the emulator.

### Step 1: Turn on Developer Options (a secret menu!)

1. On your phone, open **Settings**.
2. Go to **About phone**.
   (On some phones: **Settings → About phone → Software information**.)
3. Find **Build number**.
4. **Tap it 7 times** quickly. 👆👆👆👆👆👆👆
5. The phone may ask for your PIN.
6. You see a message: **"You are now a developer!"** 🎉

### Step 2: Turn on USB debugging

1. Go back to **Settings**.
2. Find **Developer options**.
   (Often in **Settings → System → Developer options**.)
3. Turn ON **USB debugging**.

### Step 3: Connect the phone

1. Connect your phone to the computer with a **USB cable**.
   ⚠️ Some cables only charge. Use a cable that can also **send data**.
2. On the phone, a box appears: **"Allow USB debugging?"**
   - Tick **"Always allow from this computer"**.
   - Tap **Allow**.
3. In Android Studio, the device drop-down now shows **your phone's name**.
4. Select it and click **▶ Run**.
5. 🎉 Your app opens on your real phone!

### Bonus: Without a cable (Wireless debugging)

For phones with **Android 11 or newer**, on the **same Wi-Fi** as your computer:

1. In **Developer options**, turn on **Wireless debugging**.
2. In Android Studio's device drop-down, choose **Pair Devices Using Wi-Fi**.
3. On the phone, tap **Wireless debugging → Pair device with QR code**.
4. Scan the QR code shown in Android Studio.
5. Done! Now you can Run without a cable. 📶

---

## 1.11 Your First Change! ✏️

Let us change the app and see the result.

### Change 1: Say hello to yourself

Find this line in `MainActivity.kt`:

```kotlin
                        name = "Android",
```

Change it to your name:

```kotlin
                        name = "Roy",
```

Click **▶ Run** again. The screen now shows: **Hello Roy!** 🎉

**Why did it change?**
Because `Greeting` puts the `name` into `"Hello $name!"`.

### Change 2: Change the greeting words

Find this line inside the `Greeting` function:

```kotlin
        text = "Hello $name!",
```

Change it to:

```kotlin
        text = "Good morning, $name! Welcome to my first app.",
```

Run again. The screen shows: **Good morning, Roy! Welcome to my first app.**

### Change 3: Change the app name

1. Open `res/values/strings.xml`.
2. Change:
   ```xml
   <string name="app_name">My First App</string>
   ```
   to:
   ```xml
   <string name="app_name">Roy's App</string>
   ```
   ⚠️ In XML, an apostrophe `'` must have a backslash before it: `Roy\'s App`.
   So the correct line is:
   ```xml
   <string name="app_name">Roy\'s App</string>
   ```
3. Run the app. Go to the phone's home screen. The name under the icon is now **Roy's App**.

### Faster: Live Edit and Apply Changes

You don't always need the full Run:

- **Preview** updates by itself while you type (for small changes).
- **Apply Changes** button (the ⚡ lightning icon next to Run, or **Ctrl + F10**) updates the running app **without restarting it**.

---

## 1.12 Useful Keyboard Shortcuts (Windows)

| Keys | What it does |
|---|---|
| **Shift + F10** | Run the app |
| **Ctrl + F10** | Apply code changes |
| **Alt + Enter** | ⭐ Magic fix! Fixes red errors, adds imports |
| **Ctrl + Space** | Show suggestions while typing |
| **Ctrl + Alt + L** | Make the code neat (auto-format) |
| **Ctrl + /** | Turn a line into a comment (or back) |
| **Ctrl + Z** | Undo |
| **Ctrl + Shift + Z** | Redo |
| **Shift, Shift** (press Shift twice) | Search everything |
| **Ctrl + B** (or Ctrl + click) | Go to where something is made |

> 💡 If you learn only **one** shortcut, learn **Alt + Enter**. It fixes most small problems.

---

## 1.13 Comments — Notes for Humans

In code, you can write **notes** that the computer ignores. They are called **comments**.

```kotlin
// This is a one-line comment. The computer skips it.

/*
   This is a comment
   with many lines.
*/

val age = 10 // You can also write a comment at the end of a line.
```

| Symbol | Meaning |
|---|---|
| `//` | Everything after this, **on the same line**, is a comment. |
| `/* ... */` | Everything between them is a comment, even many lines. |

**Why use comments?** To remember **why** you wrote something. Your future self will thank you! 😊

Try it — add a comment above `Greeting`:

```kotlin
// This function shows a hello message on the screen.
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    ...
}
```

---

## 1.14 Common Problems and Fixes 🔧

### Problem 1: "Gradle sync failed"

**What it means:** The helper robot could not download or set things up.

**Fixes (try in order):**
1. Check your **internet**.
2. Click **File → Sync Project with Gradle Files** (the elephant icon 🐘).
3. Click **File → Invalidate Caches… → Invalidate and Restart**.
4. Read the red error message in the **Build** window. Search it on Google.

### Problem 2: The emulator does not start / "HAXM" or "virtualization" error

**What it means:** Your computer's **virtualization** feature is OFF. The emulator needs it.

**Fix:**
1. Restart your computer and open the **BIOS** (often press **F2**, **F10**, **Del**, or **Esc** while it starts — it depends on your computer brand).
2. Find **Intel Virtualization Technology (VT-x)** or **SVM Mode / AMD-V**.
3. Set it to **Enabled**. Save and exit.
4. In Windows, search **"Turn Windows features on or off"**. Tick **Windows Hypervisor Platform**. Restart.

### Problem 3: The emulator is very, very slow

**Fixes:**
- Close other big programs (Chrome with many tabs, games).
- In Device Manager, choose a phone with a **smaller screen**.
- Use your **real phone** instead (section 1.10).

### Problem 4: My real phone does not show in Android Studio

**Fixes:**
1. Use a **data** USB cable, not a charge-only cable.
2. On the phone, pull down the notifications. Tap the USB message. Choose **File transfer**.
3. Turn **USB debugging** off and on again.
4. Unplug and plug the cable in again. Look for the **"Allow USB debugging?"** box on the phone.
5. Some phones (Samsung, Xiaomi, Oppo…) need a **USB driver** for Windows. Search "*your phone brand* USB driver".

### Problem 5: Red words in my code

**What it means:** There is a mistake, or an import is missing.

**Fixes:**
1. Click on the red word.
2. Press **Alt + Enter**.
3. Choose **Import** (if it offers) or read the suggestion.
4. Check for typing mistakes: Kotlin cares about **BIG and small letters**. `Text` and `text` are **different**!

### Problem 6: "Unresolved reference"

**What it means:** Kotlin does not know this word.

**Fixes:**
- Check the spelling.
- Add the import (Alt + Enter).
- Check that you did not delete a `{` or `}`.

> 💡 **Brackets must be in pairs.** Every `{` needs a `}`. Every `(` needs a `)`. Click next to a bracket — Android Studio highlights its partner.

---

## 1.15 Summary — What You Learned 🎓

✅ **Android** is the software inside many phones. **Kotlin** is the language we use. **Android Studio** is where we build apps.

✅ Modern Android apps use **Kotlin + Jetpack Compose**.

✅ You **installed** Android Studio and the **SDK** (the toolbox).

✅ You made a project with the **Empty Activity** template.

✅ **Gradle** is the helper robot that builds your app.

✅ Important files:
- `MainActivity.kt` → your code
- `AndroidManifest.xml` → the app's ID card
- `strings.xml` → the app's text
- `build.gradle.kts (Module :app)` → the app's settings
- `libs.versions.toml` → library versions

✅ Important code ideas:
- `class MainActivity : ComponentActivity()` → our screen
- `onCreate` → runs when the screen is born
- `setContent { }` → what to show
- `@Composable` → this function draws UI
- `Text(...)` → shows words
- `"Hello $name!"` → put a value inside text
- `@Preview` → see the screen without running

✅ You ran the app on an **emulator** and on a **real phone**.

✅ You changed the text and the app name.

---

## 1.16 Practice Time 🏋️

Try these small tasks. The answers are below — but try first!

**Task 1:** Change the greeting to show: `Hi Mom!`

**Task 2:** Change the greeting so it shows: `Hello Roy, you are learning Kotlin!`
(Hint: change the `text = ...` line and the `name`.)

**Task 3:** Change the Preview so it shows `Hello Preview!` but the real app still shows your name.

**Task 4:** Add a comment above `class MainActivity` that says what this class is.

**Task 5:** Find the Android version (API level) of your emulator. (Hint: look in Device Manager.)

---

### Answers

**Task 1:** In `MainActivity`, change `name = "Android"` to `name = "Mom"`. The text becomes `Hello Mom!`.
*(Or change `text` to `"Hi $name!"` — then you also get "Hi".)*
Full answer:
```kotlin
// in setContent:
name = "Mom",

// in Greeting:
text = "Hi $name!",
```

**Task 2:**
```kotlin
// in setContent:
name = "Roy",

// in Greeting:
text = "Hello $name, you are learning Kotlin!",
```

**Task 3:** The preview has its own call. Change only that one:
```kotlin
@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MyFirstAppTheme {
        Greeting("Preview")   // changed here only
    }
}
```

**Task 4:**
```kotlin
// MainActivity is the first screen of my app. It opens when the user taps the icon.
class MainActivity : ComponentActivity() {
```

**Task 5:** Open **Device Manager**. The list shows the phone name and the API number, for example *"Medium Phone API 35"*.

---

## 1.17 What Is Next?

In **Chapter 2: Kotlin Basics**, you will learn the Kotlin language step by step:

- Variables (`val` and `var`) — boxes that hold values 📦
- Types — numbers, text, true/false
- Math in code ➕➖✖️➗
- Making decisions with `if` and `when`
- Repeating things with loops 🔁
- Writing your own functions

You will understand **every word** of `MainActivity.kt` even better after Chapter 2.

**Great job finishing Chapter 1! 🎉 You are now an Android developer in training.**
