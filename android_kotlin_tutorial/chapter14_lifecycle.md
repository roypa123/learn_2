# Chapter 14: The Life of an App — Activity Lifecycle 🔄

> **What you will learn in this chapter**
>
> 1. What an **Activity** really is
> 2. The **lifecycle**: the stages an Activity goes through 🌱➡️🌳➡️🍂
> 3. The 6 lifecycle functions: `onCreate`, `onStart`, `onResume`, `onPause`, `onStop`, `onDestroy`
> 4. Watching the lifecycle **live** in Logcat 🔍
> 5. What happens when you **rotate**, press **Home**, press **Back**, **lock** the phone… 📱
> 6. **Configuration changes** — why rotation destroys your screen
> 7. **Process death** — when Android kills your app in the background 💀
> 8. Where your state survives (and where it doesn't) 🧠
> 9. Using the lifecycle **inside Compose**
> 10. Building a **Lifecycle Explorer** app 🔬
>
> **Time needed:** about 3 to 4 hours.
>
> **Why this chapter matters:** Many app bugs — lost text, a video that keeps playing in the background, a battery-hungry app — come from **not understanding the lifecycle**. After this chapter, you will! 💪

---

## 14.1 What Is an Activity? 🏠

You've written this since Chapter 1:

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        ...
    }
}
```

An **Activity** is a **window** of your app that the user can see and touch. It's the **entry point** — Android starts your app by creating this Activity (because of the `MAIN` + `LAUNCHER` lines in the manifest, Chapter 1).

### One Activity, many screens

In **old** Android apps, every screen was a **separate** Activity.
In **modern** Compose apps, we usually have **just one** Activity, and **many Composable screens** inside it (with Navigation, Chapter 13).

```
┌─────────────── MainActivity (the window) ───────────────┐
│                                                          │
│   NavHost                                                │
│    ├── RecipeListScreen   (a Composable)                 │
│    ├── RecipeDetailScreen (a Composable)                 │
│    └── AboutScreen        (a Composable)                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Real-life example:** The Activity is the **TV** 📺. The Composable screens are the **channels**. You switch channels (screens) inside the same TV.

### Who controls the Activity?

**Not you!** **Android** controls it. Android decides when to create it, pause it, stop it, or destroy it — depending on what the **user** does and how much **memory** the phone has.

Android **tells** your Activity what's happening by calling special functions. These are the **lifecycle functions**. 📞

---

## 14.2 The Lifecycle — Stages of Life 🌱🌳🍂

Like a living thing, an Activity has **stages**:

```
                     ┌──────────────┐
                     │  onCreate()  │   🌱 Born. Set up the screen.
                     └──────┬───────┘
                            ▼
                     ┌──────────────┐
          ┌─────────▶│  onStart()   │   👀 Becoming VISIBLE.
          │          └──────┬───────┘
          │                 ▼
          │          ┌──────────────┐
          │          │  onResume()  │   👆 In FRONT. User can TOUCH it.
          │          └──────┬───────┘
          │                 │
          │       ═══ 🟢 RUNNING — the user is using the app ═══
          │                 │
          │                 ▼
          │          ┌──────────────┐
          │          │  onPause()   │   ⏸️ Losing focus (something is in front).
          │          └──────┬───────┘
          │                 ▼
          │          ┌──────────────┐
          │          │   onStop()   │   🙈 NOT visible anymore.
          │          └──────┬───────┘
          │                 │
  onRestart()               ├───── user comes back ─────┐
          │                 │                            │
          └─────────────────┼────────────────────────────┘
                            ▼
                     ┌──────────────┐
                     │ onDestroy()  │   🍂 Gone. Clean up.
                     └──────────────┘
```

### The 6 main functions

| Function | When Android calls it | Is the app visible? | Can the user touch it? | What to do here |
|---|---|---|---|---|
| `onCreate()` | Once, when the Activity is **created** | ❌ not yet | ❌ | Set up: `setContent { }` |
| `onStart()` | The Activity is becoming **visible** | ✅ | ❌ not yet | Start things that update the screen |
| `onResume()` | The Activity is in **front** and **active** | ✅ | ✅ | Start camera, sensors, animations, video ▶️ |
| `onPause()` | Something partly **covers** it, or the user is **leaving** | ✅ (maybe partly) | ❌ | Pause video ⏸️, camera, sensors |
| `onStop()` | The Activity is **not visible** anymore | ❌ | ❌ | Stop heavy work, save drafts 💾 |
| `onDestroy()` | The Activity is being **destroyed** | ❌ | ❌ | Final clean-up |

There's also `onRestart()` — called before `onStart()` when coming back from **stopped**.

### The pairs 👫

The functions come in **pairs** — whatever you start in one, you stop in its partner:

| Start in… | …stop in |
|---|---|
| `onCreate` 🌱 | `onDestroy` 🍂 |
| `onStart` 👀 | `onStop` 🙈 |
| `onResume` ▶️ | `onPause` ⏸️ |

**Real-life example:** A **shop** 🏪.

| Lifecycle | Shop |
|---|---|
| `onCreate` | The shop is **built** and the shelves are filled. |
| `onStart` | The **lights** are turned on. People outside can **see** in. |
| `onResume` | The **door is unlocked**. Customers can come in and **buy**. 🛒 |
| `onPause` | The shopkeeper takes a **short break**. The door is **locked**, but the lights are on. |
| `onStop` | **Closing time**. Lights **off**. Nobody can see in. |
| `onDestroy` | The shop is **torn down**. 🏚️ |

> ⚠️ **Always call `super`!** When you override a lifecycle function, call the parent's version first: `super.onStart()`. Android does important work there. Forgetting it causes a crash: *"did not call through to super.onStart()"*. 💥

---

## 14.3 Watching the Lifecycle Live 🔍

The **best** way to understand the lifecycle is to **watch** it happen.

Add this to `MainActivity` in any of your projects (keep your existing `onCreate` content):

```kotlin
private const val TAG = "Lifecycle"

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d(TAG, "🌱 onCreate (savedInstanceState is ${if (savedInstanceState == null) "null" else "NOT null"})")
        enableEdgeToEdge()
        setContent {
            // ... your app ...
        }
    }

    override fun onStart() {
        super.onStart()
        Log.d(TAG, "👀 onStart")
    }

    override fun onResume() {
        super.onResume()
        Log.d(TAG, "👆 onResume")
    }

    override fun onPause() {
        super.onPause()
        Log.d(TAG, "⏸️ onPause")
    }

    override fun onStop() {
        super.onStop()
        Log.d(TAG, "🙈 onStop")
    }

    override fun onRestart() {
        super.onRestart()
        Log.d(TAG, "🔁 onRestart")
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, "🍂 onDestroy (rotation? $isChangingConfigurations, finishing? $isFinishing)")
    }
}
```

| Code | Meaning |
|---|---|
| `private const val TAG = "Lifecycle"` | A constant for the Logcat tag (Chapter 4). `private` = only this file uses it. |
| `override fun onStart()` | Replace the parent's `onStart` with ours (Chapter 4: `override`). |
| `super.onStart()` | Let the parent do its work **first**. ⚠️ Don't forget! |
| `isChangingConfigurations` | `true` if the Activity is being destroyed **because of a configuration change** (like rotation). |
| `isFinishing` | `true` if the Activity is **really finishing** (going away for good). |

**Run the app.** Open **Logcat**, and type `Lifecycle` in the search box. 🔍

### Experiments 🧪 — try each one and watch Logcat!

#### Experiment 1: Open the app

```
🌱 onCreate (savedInstanceState is null)
👀 onStart
👆 onResume
```

Born → visible → active. `savedInstanceState` is `null` because this is a **fresh** start.

#### Experiment 2: Press the Home button 🏠

```
⏸️ onPause
🙈 onStop
```

The app goes to the **background**. It's **not** destroyed — it's waiting. 😴

#### Experiment 3: Open the app again (from recent apps or the icon)

```
🔁 onRestart
👀 onStart
👆 onResume
```

No `onCreate` — it was still **alive**! It just woke up. ☀️

#### Experiment 4: Rotate the phone 🔄

```
⏸️ onPause
🙈 onStop
🍂 onDestroy (rotation? true, finishing? false)
🌱 onCreate (savedInstanceState is NOT null)
👀 onStart
👆 onResume
```

😮 **The whole Activity was destroyed and created again!** This is a **configuration change** (14.4). Notice `savedInstanceState` is **not null** this time — it carries saved data (14.6).

#### Experiment 5: Press Back on the main screen ⬅️

On **Android 12 and newer**:

```
⏸️ onPause
🙈 onStop
```

On **older** Android (11 and below):

```
⏸️ onPause
🙈 onStop
🍂 onDestroy (rotation? false, finishing? true)
```

> ℹ️ Since **Android 12**, pressing Back on the app's **first** screen just sends the app to the **background** (like Home), so it opens faster next time. ⚡ Older versions **destroyed** it.

#### Experiment 6: Lock the screen 🔒

```
⏸️ onPause
🙈 onStop
```

Unlock → `onRestart`, `onStart`, `onResume`.

#### Experiment 7: Pull down the notification shade

On most phones: **nothing** happens, or just `onPause` / `onResume`. The app is still visible behind it.

#### Experiment 8: Switch dark mode on 🌙 (Quick Settings)

The same as rotation: **destroy** and **create** again! Dark mode is also a configuration change.

### Summary of experiments

| User does… | Lifecycle calls |
|---|---|
| Opens the app | `onCreate` → `onStart` → `onResume` |
| Presses Home 🏠 | `onPause` → `onStop` |
| Comes back | `onRestart` → `onStart` → `onResume` |
| Rotates 🔄 / dark mode 🌙 / language 🌍 | `onPause` → `onStop` → `onDestroy` → `onCreate` → `onStart` → `onResume` |
| Back on the first screen (Android 12+) | `onPause` → `onStop` |
| Locks the screen 🔒 | `onPause` → `onStop` |
| A dialog from **another** app or the system appears on top (e.g. permission dialog) | `onPause` only (the app is still partly visible) |

> 💡 Write this table in your notebook! 📒 You'll look at it many times as a developer.

---

## 14.4 Configuration Changes — Why Rotation Destroys Your Screen 🔄💥

### What is a configuration?

The **configuration** is a set of facts about the phone's current **setup**:

- 📐 **Orientation** — portrait (tall) or landscape (wide)?
- 🌙 **Dark mode** — on or off?
- 🌍 **Language** — English, Hindi, Spanish…?
- 🔤 **Font size** — normal or big?
- 📏 **Screen size** — changes on foldable phones 📱↔️📖 and in split-screen
- ⌨️ A **keyboard** is connected

### What happens when it changes?

Android **destroys** the Activity and **creates it again** with the new configuration.

**Why so extreme?** 🤔 Because your app might need **different** things for the new setup:
- Different **texts** for a new language (`strings.xml` in Hindi!)
- Different **colors** for dark mode
- A different **layout** for a wide screen

The safest way to load the right things is to **start fresh**. 🔄

**Real-life example:** You **move** to a new country 🌍. You don't just change one sign on your house — you get a **new house** with the right plugs, the right language on the mailbox… Everything set up fresh for the new place.

### The problem: lost state 😱

When the Activity is destroyed, **everything inside it is thrown away** — including all your Composables and their `remember` values!

```kotlin
var count by remember { mutableIntStateOf(0) }           // ❌ lost on rotation
var count by rememberSaveable { mutableIntStateOf(0) }   // ✅ survives rotation
```

This is exactly what you saw in **Chapter 8**! Now you know **why**: rotation **destroys** the Activity, and `remember` lives **inside** it.

### Can I stop Android from destroying the Activity?

There's a way (`android:configChanges` in the manifest), but it's **not recommended** for beginners:
- You must handle **every** change yourself. Easy to forget one → bugs. 🐛
- It **doesn't** protect against **process death** (next section) — you still need to save state properly.

> 💡 **The right approach:** Let Android recreate the Activity, and **save your state correctly** (`rememberSaveable`, ViewModel). Then your app works in **every** situation. ✅

---

## 14.5 Process Death — When Android Kills Your App 💀

### What is a process?

When your app runs, Android gives it a **process** — its own **space in memory** where all its code and data live. 🧠

### Why would Android kill it?

Phones have **limited memory**. When the user opens many apps (games, camera, browser…), Android needs space. It **kills** apps that are in the **background** (stopped), starting with the ones not used for the longest time. 🔪

**This happens silently.** The app is gone, but it's still shown in **Recent apps**. When the user comes back, Android **starts it again** and tries to bring back where the user was.

**Real-life example:** You leave your bag 🎒 on a table in a busy library to go get a book. A librarian needs the table, so they put your bag in **storage** with a **note** of what was on the table. When you come back, they set the table up again **from the note**. 📝 But anything **not** on the note is **lost**.

### What survives process death?

| Where the state is kept | Rotation 🔄 | Process death 💀 |
|---|---|---|
| A normal `var` in a Composable | ❌ | ❌ |
| `remember { }` | ❌ | ❌ |
| `rememberSaveable { }` | ✅ | ✅ (it's on the "note"!) |
| `ViewModel` (Chapter 15) | ✅ | ❌ (unless you use `SavedStateHandle`) |
| A global `object` in your code | ✅ | ❌ |
| **DataStore / Room** (on disk, Chapters 21–22) | ✅ | ✅ |
| The Navigation back stack | ✅ | ✅ |

### How to test process death 🧪

It's hard to make Android kill your app on purpose. But there's a developer trick:

**Option A: "Don't keep activities"**
1. Open **Settings → System → Developer options** (Chapter 1 showed how to turn these on).
2. Scroll down to **Apps** and turn on **"Don't keep activities"**.
3. Now, **every time** you press Home, Android **destroys** your Activity. Come back → it's recreated. You'll quickly see which state is lost! 🔍
4. ⚠️ **Turn it OFF** when you're done, or other apps will behave strangely.

**Option B: Stop the process from Android Studio**
1. Run your app, then press **Home** (the app must be in the background).
2. In Android Studio, open the **Logcat** panel or the **Running Devices / App Inspection** window and find your app's process, or use the **Terminal**:
   ```
   adb shell am kill com.example.myfirstapp
   ```
   (Use your package name.)
3. Open the app from **Recent apps** → it restarts and restores `rememberSaveable` state. ✨

> 💡 Professional developers **always** test rotation **and** process death before releasing an app. Most users never notice process death — **if** your app handles it well! 😉

---

## 14.6 `savedInstanceState` — The Note 📝

Look at `onCreate` again:

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
```

- A **`Bundle`** is a small **bag** of saved values (keys and values, like a `Map` from Chapter 3). 🎒
- Before destroying the Activity (rotation, process death), Android asks the app to **put important values** into a Bundle.
- When it creates the Activity **again**, it gives the Bundle back to `onCreate`.
- On a **fresh** start, it's `null` (Experiment 1). After rotation, it's **not** `null` (Experiment 4).

**`rememberSaveable` uses this Bundle for you!** That's how it survives. You don't need to touch the Bundle yourself in Compose. 🎉

### ⚠️ Keep saved state SMALL

The Bundle is meant for **small** things: a few numbers, short texts, ids, selected tab…

| ✅ Good for `rememberSaveable` | ❌ Too big |
|---|---|
| What the user typed in a text field | A list of 10,000 messages |
| The selected tab index | Pictures 🖼️ |
| A scroll position | Data downloaded from the internet |
| The id of the open item | A whole database |

If you save too much, the app can **crash** with: *TransactionTooLargeException*. 💥

**Big data** belongs in a **database** (Room, Chapter 22) or comes back from the **internet** (Chapter 19). Save only the **id** or the **search text** in `rememberSaveable`, and **load** the rest again.

---

## 14.7 The Lifecycle Inside Compose 🧩

In Compose, you usually **don't** override `onPause` in the Activity. Instead, a Composable can **listen** to the lifecycle **itself**.

### Step 1: Add the library (if needed)

The lifecycle helpers for Compose are in **`lifecycle-runtime-compose`**. In many projects it's already included. If `LifecycleResumeEffect` is red and Alt + Enter doesn't help, add it:

In `gradle/libs.versions.toml`, under `[libraries]` (the version `lifecycleRuntimeKtx` already exists in new projects):

```toml
androidx-lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycleRuntimeKtx" }
```

In `build.gradle.kts (Module :app)`:

```kotlin
dependencies {
    // ...
    implementation(libs.androidx.lifecycle.runtime.compose)
}
```

Click **Sync Now**. 🔄

### Step 2: React to one lifecycle event — `LifecycleEventEffect`

```kotlin
@Composable
fun WelcomeBackMessage() {
    val context = LocalContext.current

    LifecycleEventEffect(Lifecycle.Event.ON_RESUME) {
        Toast.makeText(context, "Welcome back! 👋", Toast.LENGTH_SHORT).show()
    }

    Text("Press Home, then come back.")
}
```

Imports:

```kotlin
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LifecycleEventEffect
```

- Every time the Activity **resumes** (comes to the front), the code runs → a Toast. 🍞
- Events you can use: `ON_CREATE`, `ON_START`, `ON_RESUME`, `ON_PAUSE`, `ON_STOP`, `ON_DESTROY`.

### Step 3: Start and stop in pairs — `LifecycleResumeEffect` ⭐

Remember the **pairs** from 14.2? This helper makes them easy:

```kotlin
@Composable
fun VideoPlayerDemo() {
    var playing by remember { mutableStateOf(false) }

    LifecycleResumeEffect(Unit) {
        playing = true                 // ▶️ app is in front → play
        Log.d("Video", "▶️ play")

        onPauseOrDispose {
            playing = false            // ⏸️ app leaves the front → pause
            Log.d("Video", "⏸️ pause")
        }
    }

    Text(if (playing) "▶️ Video is playing" else "⏸️ Video is paused")
}
```

Import: `androidx.lifecycle.compose.LifecycleResumeEffect`

| Code | Meaning |
|---|---|
| `LifecycleResumeEffect(Unit) { ... }` | The code runs on **resume**. `Unit` is a **key** — we don't need one, so we give `Unit` (it never changes). |
| `onPauseOrDispose { ... }` | ⚠️ **Required!** Runs on **pause**, **or** when the Composable **leaves the screen**. The perfect place to **stop** what you started. |

There's also **`LifecycleStartEffect`** with **`onStopOrDispose { }`** — for things that should run while the app is **visible** (`onStart` ↔ `onStop`).

**Real-life examples of when to use these:**

| Start on resume / start | Stop on pause / stop |
|---|---|
| ▶️ Play a video | ⏸️ Pause the video |
| 📷 Open the camera preview | Close the camera |
| 📍 Start location updates | Stop location updates (save battery! 🔋) |
| ⏱️ Start a game timer | Pause the game |
| 🔄 Refresh data | — |

> 💡 **Why is this important?** If you forget to **stop** things, they keep running in the **background**: the video plays with the app closed 🔊, the GPS drains the battery 🔋📉, the camera stays on 📷😱. Users **uninstall** apps like that!

### Composition vs Activity lifecycle — two different "lives" 🤔

A Composable has its **own**, simpler life:

```
Enters the composition  ──▶  Recomposes 0, 1, many times  ──▶  Leaves the composition
   (appears on screen)          (when state changes)              (removed from screen)
```

- A Composable **leaves** the composition when, for example, an `if` becomes `false`, or you **navigate** to another screen.
- `remember` values are **forgotten** when the Composable **leaves**.
- The **Activity** lifecycle is about the **whole window** (Home, rotation, lock…).

| Event | Activity lifecycle | Composable lifecycle |
|---|---|---|
| Navigate to another screen | No change (same Activity) | Old screen **leaves**, new screen **enters** |
| `if (show)` becomes `false` | No change | That Composable **leaves** |
| Press Home | `onPause`, `onStop` | Still in the composition (just not visible) |
| Rotate | Destroyed and created again | **Everything** leaves and enters again |

`onPauseOrDispose` covers **both**: it runs if the **app** pauses **or** if the **Composable** leaves. 👍

---

## 14.8 Build It: A Lifecycle Explorer App 🔬

Let's build an app that shows lifecycle events **on the screen**, so you can **see** them without Logcat. It also shows **which state survives** rotation.

```
┌──────────────────────────────────┐
│ 🔬 Lifecycle Explorer            │
├──────────────────────────────────┤
│ ╭──────────────╮ ╭─────────────╮ │
│ │ remember     │ │ rememberSa- │ │
│ │     3        │ │ veable  3   │ │   ← two counters
│ │   [ +1 ]     │ │   [ +1 ]    │ │
│ ╰──────────────╯ ╰─────────────╯ │
│                                  │
│ 👋 You were away for 12 seconds   │   ← LifecycleResumeEffect
│ Activity created 2 times         │
│                                  │
│ Events (newest first)    [Clear] │
│ 10:42:13  👆 onResume            │
│ 10:42:13  👀 onStart             │
│ 10:42:13  🌱 onCreate (restored) │
│ 10:42:12  🍂 onDestroy (rotation)│
│ ...                              │
└──────────────────────────────────┘
```

### Where do we keep the event list?

The list must survive **rotation** (or we'd lose the events about the rotation itself!). We use a **global `object`** (Chapter 4) — it lives as long as the **process**, not the Activity.

- ✅ Survives rotation (the process stays alive).
- ❌ **Doesn't** survive process death — and the app will **show** you that! Great for learning. 🎓

### The full code

Replace **everything** in `MainActivity.kt` (keep your own `package` line and theme name). Make sure `lifecycle-runtime-compose` is added (14.7, Step 1).

```kotlin
package com.example.myfirstapp

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.LifecycleResumeEffect
import com.example.myfirstapp.ui.theme.MyFirstAppTheme
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

private const val TAG = "Lifecycle"

// ---------- A global log that lives as long as the PROCESS ----------

data class LifecycleEvent(val id: Int, val time: String, val text: String)

object LifecycleLog {
    val events = mutableStateListOf<LifecycleEvent>()
    var activityCreatedCount by mutableIntStateOf(0)
    private var nextId = 0
    private val timeFormat = SimpleDateFormat("HH:mm:ss", Locale.getDefault())

    fun add(text: String) {
        Log.d(TAG, text)
        events.add(0, LifecycleEvent(nextId++, timeFormat.format(Date()), text))
    }

    fun clear() {
        events.clear()
    }
}

// ---------- Activity ----------

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        LifecycleLog.activityCreatedCount++
        val how = if (savedInstanceState == null) "fresh start" else "restored"
        LifecycleLog.add("🌱 onCreate ($how)")

        enableEdgeToEdge()
        setContent {
            MyFirstAppTheme {
                LifecycleExplorerApp()
            }
        }
    }

    override fun onStart() {
        super.onStart()
        LifecycleLog.add("👀 onStart")
    }

    override fun onResume() {
        super.onResume()
        LifecycleLog.add("👆 onResume")
    }

    override fun onPause() {
        super.onPause()
        LifecycleLog.add("⏸️ onPause")
    }

    override fun onStop() {
        super.onStop()
        LifecycleLog.add("🙈 onStop")
    }

    override fun onRestart() {
        super.onRestart()
        LifecycleLog.add("🔁 onRestart")
    }

    override fun onDestroy() {
        super.onDestroy()
        val why = when {
            isChangingConfigurations -> "rotation/config change"
            isFinishing -> "finishing"
            else -> "system"
        }
        LifecycleLog.add("🍂 onDestroy ($why)")
    }
}

// ---------- UI ----------

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LifecycleExplorerApp() {
    Scaffold(
        topBar = { TopAppBar(title = { Text("🔬 Lifecycle Explorer") }) },
        modifier = Modifier.fillMaxSize()
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            CountersRow()
            TimeAwayText()
            Text(
                text = "Activity created ${LifecycleLog.activityCreatedCount} times",
                style = MaterialTheme.typography.bodyMedium
            )
            HorizontalDivider()
            EventList(modifier = Modifier.weight(1f))
        }
    }
}

@Composable
fun CountersRow() {
    var normalCount by remember { mutableIntStateOf(0) }
    var savedCount by rememberSaveable { mutableIntStateOf(0) }

    Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
        CounterCard(
            title = "remember",
            count = normalCount,
            color = Color(0xFFFFCDD2),
            onAdd = { normalCount++ },
            modifier = Modifier.weight(1f)
        )
        CounterCard(
            title = "rememberSaveable",
            count = savedCount,
            color = Color(0xFFC8E6C9),
            onAdd = { savedCount++ },
            modifier = Modifier.weight(1f)
        )
    }
}

@Composable
fun CounterCard(
    title: String,
    count: Int,
    color: Color,
    onAdd: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        colors = CardDefaults.cardColors(containerColor = color, contentColor = Color.Black),
        modifier = modifier
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(title, style = MaterialTheme.typography.labelLarge, fontFamily = FontFamily.Monospace)
            Text("$count", style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold)
            Button(onClick = onAdd) { Text("+1") }
        }
    }
}

@Composable
fun TimeAwayText() {
    var pausedAt by remember { mutableLongStateOf(0L) }
    var message by remember { mutableStateOf("Press Home, wait, then come back. ⏳") }

    LifecycleResumeEffect(Unit) {
        if (pausedAt != 0L) {
            val seconds = (System.currentTimeMillis() - pausedAt) / 1000
            message = "👋 Welcome back! You were away for $seconds seconds."
        }
        onPauseOrDispose {
            pausedAt = System.currentTimeMillis()
        }
    }

    Text(text = message, style = MaterialTheme.typography.titleMedium)
}

@Composable
fun EventList(modifier: Modifier = Modifier) {
    Column(modifier = modifier) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = "Events (newest first)",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.weight(1f)
            )
            TextButton(onClick = { LifecycleLog.clear() }) { Text("Clear") }
        }
        LazyColumn(contentPadding = PaddingValues(bottom = 16.dp)) {
            items(LifecycleLog.events, key = { it.id }) { event ->
                Row(modifier = Modifier.padding(vertical = 4.dp)) {
                    Text(
                        text = event.time,
                        fontFamily = FontFamily.Monospace,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.width(12.dp))
                    Text(event.text)
                }
            }
        }
    }
}
```

> ⚠️ Keep **your own** `package` line and theme import.
> ℹ️ We don't add a `@Preview` for the whole app here, because it reads from the Activity's global log. That's OK — **run** this app on a device. 📱

### Every important part explained

#### Part 1: `LifecycleLog` — a global object with Compose state

```kotlin
object LifecycleLog {
    val events = mutableStateListOf<LifecycleEvent>()
    var activityCreatedCount by mutableIntStateOf(0)
    ...
}
```

| Code | Meaning |
|---|---|
| `object LifecycleLog` | **One** log for the whole app (Chapter 4). It lives in the **process**, **outside** the Activity → it survives rotation. |
| `mutableStateListOf<LifecycleEvent>()` | A list that **tells Compose** when it changes (Chapter 8) → the screen updates **live** when an event is added. ✨ |
| `var activityCreatedCount by mutableIntStateOf(0)` | State can live **outside** a Composable too! Without `remember` — because it's not inside a Composable, it's never "forgotten". |
| `events.add(0, ...)` | Add at position **0** → newest **first**. |
| `nextId++` | Each event gets a unique id → a **key** for the LazyColumn (Chapter 10). (`nextId++` gives the **current** value, **then** adds 1.) |

#### Part 2: The time with `SimpleDateFormat`

```kotlin
    private val timeFormat = SimpleDateFormat("HH:mm:ss", Locale.getDefault())
    ...
    timeFormat.format(Date())
```

| Code | Meaning |
|---|---|
| `Date()` | **Now** — the current date and time. 🕐 |
| `SimpleDateFormat("HH:mm:ss", ...)` | Show it as **hours:minutes:seconds** → `10:42:13`. (`HH` = 24-hour clock.) |
| `Locale.getDefault()` | Use the phone's language/region settings. |

> ℹ️ Kotlin and Java have newer date tools (`java.time`) — we'll meet them later. `SimpleDateFormat` is simple and works everywhere.

#### Part 3: The Activity reports every event

```kotlin
    override fun onDestroy() {
        super.onDestroy()
        val why = when {
            isChangingConfigurations -> "rotation/config change"
            isFinishing -> "finishing"
            else -> "system"
        }
        LifecycleLog.add("🍂 onDestroy ($why)")
    }
```

- A `when` without a value (Chapter 2) finds the **reason** for destroying.

#### Part 4: Two counters — the big lesson 🎓

```kotlin
    var normalCount by remember { mutableIntStateOf(0) }
    var savedCount by rememberSaveable { mutableIntStateOf(0) }
```

- 🟥 **Red card** (`remember`): goes back to **0** after rotation.
- 🟩 **Green card** (`rememberSaveable`): **keeps** its number after rotation (and even after process death!).

You can **see** the difference with your own eyes. 👀

> 🎨 We used **fixed** light colors with **black** text (`contentColor = Color.Black`) on purpose — so the red and green are clear in **both** light and dark mode.

#### Part 5: Time away — `LifecycleResumeEffect`

```kotlin
    LifecycleResumeEffect(Unit) {
        if (pausedAt != 0L) {
            val seconds = (System.currentTimeMillis() - pausedAt) / 1000
            message = "👋 Welcome back! You were away for $seconds seconds."
        }
        onPauseOrDispose {
            pausedAt = System.currentTimeMillis()
        }
    }
```

| Code | Meaning |
|---|---|
| `System.currentTimeMillis()` | The current time, as **milliseconds** (1/1000 of a second) since the year 1970. A big `Long` number. ⏱️ |
| `mutableLongStateOf(0L)` | State for a `Long` (Chapter 8's special versions). |
| `onPauseOrDispose { pausedAt = now }` | When the app **pauses**, remember **when**. |
| On **resume** | Now − then = time away. `/ 1000` → seconds. |
| `if (pausedAt != 0L)` | The very **first** resume (app just opened) has nothing to compare → skip. |

### Run it! ▶️ — and do the experiments

| Try this | What you'll see |
|---|---|
| Open the app | `🌱 onCreate (fresh start)`, `👀 onStart`, `👆 onResume` |
| Tap both **+1** a few times, then **rotate** 🔄 | Red card → **0**. Green card → **kept**! Events show the destroy/create. "Activity created **2** times". |
| Press **Home**, wait 10 s, come back | `⏸️ onPause`, `🙈 onStop`, `🔁 onRestart`, … and "**away for 10 seconds**" 👋 |
| Turn on **dark mode** 🌙 | Same as rotation — a config change! |
| Lock 🔒 and unlock | `onPause` / `onStop` … `onRestart` / `onStart` / `onResume` |
| Turn on **"Don't keep activities"**, press Home, come back | `onDestroy (system)`, then `onCreate (restored)`. Green card kept, red card lost. |
| **Kill the process** (`adb shell am kill …`) and come back from Recent apps | The **event list is empty** (the global object died with the process 💀), "created **1** times" — but the **green card is still kept**! 🟩✅ |

That last experiment proves the table in 14.5. 🎓

---

## 14.9 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| Forgot `super.onStart()` (or any `super` call) | 💥 *SuperNotCalledException: did not call through to super.onStart()* | Always call `super.xxx()` first. |
| Using `remember` for things the user typed | Lost on rotation / dark mode / process death | `rememberSaveable` (or a ViewModel + SavedStateHandle, Chapter 15). |
| Saving big lists in `rememberSaveable` | 💥 *TransactionTooLargeException* | Save only ids/small values; keep big data in a database. |
| Starting video/camera/GPS and never stopping | Plays in the background, drains battery 🔋 | Start in resume, stop in `onPauseOrDispose`. |
| Assuming `onDestroy` is always called | Data not saved when Android kills the process | Save important data **earlier** (e.g. in `onStop`, or immediately to a database). |
| Thinking Back always destroys the app | Confusing results on Android 12+ | On 12+, Back on the root screen just moves the app to the background. |
| `LifecycleResumeEffect` without `onPauseOrDispose` | Compile error: the block must end with `onPauseOrDispose { }` | Always add the `onPauseOrDispose { }` part. |
| `LifecycleResumeEffect` is red | Missing library | Add `lifecycle-runtime-compose` (14.7). |
| Setting `android:configChanges` to "fix" rotation | Bugs in other situations; still lost on process death | Save state properly instead. |
| Leaving "Don't keep activities" on | Other apps behave strangely | Turn it off after testing. |

---

## 14.10 Summary — What You Learned 🎓

✅ An **Activity** is the app's **window**. Modern apps: **one** Activity, many Composable screens.

✅ **Android** controls the lifecycle and calls: `onCreate` 🌱 → `onStart` 👀 → `onResume` 👆 → `onPause` ⏸️ → `onStop` 🙈 → `onDestroy` 🍂 (and `onRestart` 🔁).

✅ They come in **pairs**: create/destroy, start/stop, resume/pause. Always call **`super`**.

✅ **Home / lock** → pause + stop. **Coming back** → restart + start + resume.

✅ **Configuration changes** (rotation, dark mode, language, font size, screen size) → the Activity is **destroyed and recreated**. `remember` is lost; `rememberSaveable` survives.

✅ **Process death:** Android may kill a background app. Only **saved instance state** (`rememberSaveable`), the nav back stack, and **disk** storage survive. Test with **"Don't keep activities"** or `adb shell am kill`.

✅ **`savedInstanceState`** is a small **Bundle** — keep it small!

✅ **In Compose:** `LifecycleEventEffect(event) { }`, `LifecycleResumeEffect { ... onPauseOrDispose { } }`, `LifecycleStartEffect { ... onStopOrDispose { } }`.

✅ A **Composable's** life (enter → recompose → leave) is different from the **Activity's** life.

✅ You built a **Lifecycle Explorer** and **saw** everything happen! 🔬

---

## 14.11 Practice Time 🏋️

**Task 1 — Predict! 🔮**
Without running the app, write down the lifecycle calls for this story:
1. The user opens the app.
2. The user rotates the phone.
3. The user presses Home.
4. The user comes back.

Then run the Lifecycle Explorer and check your answer.

**Task 2 — Pause the game ⏸️**
Make a Composable `GameStatus` that shows `"🎮 Game running"` while the app is resumed, and `"⏸️ Game paused"` when it's not. Use `LifecycleResumeEffect`.

**Task 3 — Count the visits 🔢**
Show `"You opened this screen N times"`, where N goes up **every time the app comes to the front** (resume). The number must survive rotation.

**Task 4 — Which survives? 🤔**
For each, say whether it survives **(a) rotation** and **(b) process death**:
1. `var name by remember { mutableStateOf("") }`
2. `var name by rememberSaveable { mutableStateOf("") }`
3. A `var` inside a global `object`
4. The current screen in a NavHost

**Task 5 — Fix the bug 🐛**
This app keeps a "music" playing even when the user presses Home. Fix it.

```kotlin
@Composable
fun MusicPlayer() {
    var playing by remember { mutableStateOf(false) }

    LifecycleEventEffect(Lifecycle.Event.ON_RESUME) {
        playing = true
        Log.d("Music", "🎵 start music")
    }

    Text(if (playing) "🎵 Playing" else "🔇 Stopped")
}
```

---

### Answers

**Task 1:**

```
1. Open:        onCreate (fresh) → onStart → onResume
2. Rotate:      onPause → onStop → onDestroy (config change) → onCreate (restored) → onStart → onResume
3. Home:        onPause → onStop
4. Come back:   onRestart → onStart → onResume
```

**Task 2:**

```kotlin
@Composable
fun GameStatus() {
    var running by remember { mutableStateOf(false) }

    LifecycleResumeEffect(Unit) {
        running = true
        onPauseOrDispose {
            running = false
        }
    }

    Text(
        text = if (running) "🎮 Game running" else "⏸️ Game paused",
        style = MaterialTheme.typography.headlineSmall
    )
}
```

💡 To **see** "paused", open the **recent apps** screen — the app is still partly visible there while paused.

**Task 3:**

```kotlin
@Composable
fun VisitCounter() {
    var visits by rememberSaveable { mutableIntStateOf(0) }

    LifecycleEventEffect(Lifecycle.Event.ON_RESUME) {
        visits++
    }

    Text("You opened this screen $visits times")
}
```

⚠️ Notice: rotation **also** causes a resume, so it counts too. That's correct lifecycle behavior! 🔄

**Task 4:**

| | (a) Rotation | (b) Process death |
|---|---|---|
| 1. `remember` | ❌ | ❌ |
| 2. `rememberSaveable` | ✅ | ✅ |
| 3. Global `object` | ✅ | ❌ |
| 4. NavHost current screen | ✅ | ✅ |

**Task 5:**
The music **starts** on resume but **never stops**. Use the **pair** helper:

```kotlin
@Composable
fun MusicPlayer() {
    var playing by remember { mutableStateOf(false) }

    LifecycleResumeEffect(Unit) {
        playing = true
        Log.d("Music", "🎵 start music")

        onPauseOrDispose {
            playing = false
            Log.d("Music", "🔇 stop music")
        }
    }

    Text(if (playing) "🎵 Playing" else "🔇 Stopped")
}
```

Rule: **whatever you start, you must stop.** ▶️⏸️

---

## 14.12 What Is Next?

You've seen the problem clearly now:
- `remember` → lost on rotation. 😕
- `rememberSaveable` → good for small things, but not for **loaded data** or **logic**.
- State in the top Composable → the code gets **long and messy** as the app grows. 😵

There's a **better home** for a screen's data and logic. 🏡

In **Chapter 15: ViewModel — The Screen's Brain**, you will learn:

- What a **ViewModel** is, and why it **survives rotation** 🧠
- Moving state and logic **out** of Composables
- **`UiState`** — one data class for everything a screen shows
- **`StateFlow`** — state that the UI can watch 👀
- `collectAsStateWithLifecycle()` — lifecycle-aware watching
- **Events** from the UI to the ViewModel
- `SavedStateHandle` — surviving process death too
- Rebuilding the **Coffee Order** app the professional way ☕

**Great job finishing Chapter 14! 🎉 You now understand how Android really runs your app!**
