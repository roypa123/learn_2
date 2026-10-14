# Chapter 21: Saving Small Settings — DataStore 💾⚙️

> **What you will learn in this chapter**
>
> 1. The **forgetting** problem — what survives what? 🧠💨
> 2. The different ways an app can **save** data on the phone 🗄️
> 3. **Preferences DataStore** — saving small things with **keys** 🔑
> 4. **Reading** (with `Flow` 🌊) and **writing** (with `edit`) ✍️
> 5. A tiny **counter that remembers** — even after closing the app
> 6. Putting DataStore behind a **repository** — the MVVM way 🏪
> 7. 🛠️ Building **My Space** 🏠: a **Welcome screen shown only once**, the user's **name**, a **dark mode** setting, and an **app-open counter**
> 8. 🏅 Upgrading the **Quiz app** from Chapter 17 with **best scores**!
>
> **Time needed:** about 4–5 hours.
>
> **What you need to know:** Chapters 1–20, especially 14 (lifecycle), 16 (MVVM), and 18 (Flow).

---

## 21.1 The Forgetting Problem 🧠💨

Open the Quiz app from Chapter 17. Play a quiz. Get 5 / 5! 🏆 Now close the app completely and open it again…

Your score is **gone**. The app has **no memory** of you. 😢

We've learned many ways to **keep** values. Let's see what each one survives:

| Way | Recomposition 🔁 | Rotation 🔄 | Leave screen ⬅️ | Process death 💀 | **App closed / phone restarted** 📴 |
|---|---|---|---|---|---|
| `remember` (Ch. 8) | ✅ | ❌ | ❌ | ❌ | ❌ |
| `rememberSaveable` (Ch. 8) | ✅ | ✅ | ❌ | ✅ | ❌ |
| `ViewModel` (Ch. 15) | ✅ | ✅ | ❌ | ❌ | ❌ |
| `SavedStateHandle` (Ch. 15) | ✅ | ✅ | ❌ | ✅ | ❌ |
| **DataStore** (this chapter) | ✅ | ✅ | ✅ | ✅ | ✅ **Yes!** |
| **Room** (Ch. 22) | ✅ | ✅ | ✅ | ✅ | ✅ **Yes!** |

Everything before this chapter lives in the app's **memory** (RAM) 🧠. When the app is fully closed, memory is **wiped**. To truly remember, we must write data into the phone's **storage** 💾 — like writing in a **notebook** instead of just **thinking** about it.

> 💡 **"Closed completely"** means: swipe the app away from the **Recents** screen, or restart the phone. (Pressing Home only puts it in the background.)

---

## 21.2 Ways to Save Data on the Phone 🗄️

| Way | Good for | Like… |
|---|---|---|
| **Preferences DataStore** ⭐ (this chapter) | **Small** settings: dark mode, name, "seen the welcome", a high score | 📝 **Sticky notes** with labels |
| Proto DataStore | Small settings with a **strict** shape (advanced) | 📋 A printed **form** |
| **Room database** (Chapter 22) | **Lots** of structured data: notes, contacts, recipes, messages | 🗃️ A **filing cabinet** |
| Files | Photos, PDFs, big documents | 📦 Boxes in the storage room |
| `SharedPreferences` | The **old** way to save settings. ⚠️ Avoid in new apps — it can freeze the main thread. | 📜 An old paper list |

> 🎯 **Simple rule:**
> - A **few** values (under ~ a few dozen)? → **DataStore** 📝
> - **Lists** of things the user creates? → **Room** 🗃️

---

## 21.3 How Preferences DataStore Works 🔑

Imagine a shelf of **jars** 🫙 in a kitchen. Each jar has a **label**, and inside is **one** thing:

```
🫙 "user_name"        → "Sam"
🫙 "dark_mode"        → true
🫙 "open_count"       → 12
🫙 "has_seen_welcome" → true
```

That's **all** Preferences DataStore is: **labels** (called **keys** 🔑) and **values**. Like a `Map` (Chapter 3) that is **saved in a file**.

### Keys have types 🏷️

Each key knows **what kind** of value its jar holds:

| Key function | Value type | Example |
|---|---|---|
| `stringPreferencesKey("user_name")` | `String` | `"Sam"` |
| `booleanPreferencesKey("dark_mode")` | `Boolean` | `true` |
| `intPreferencesKey("open_count")` | `Int` | `12` |
| `longPreferencesKey("last_open")` | `Long` | `1718000000000` |
| `floatPreferencesKey("volume")` | `Float` | `0.8f` |
| `doublePreferencesKey("balance")` | `Double` | `12.5` |
| `stringSetPreferencesKey("tags")` | `Set<String>` | `setOf("a", "b")` |

### Reading and writing 📖✍️

| Job | How | Why this way? |
|---|---|---|
| **Read** | `dataStore.data` — a **`Flow`** 🌊 of all the jars | Reading a file takes time → it can't be instant. And when a value **changes**, the Flow sends the **new** values **automatically**. 🪄 |
| **Write** | `dataStore.edit { jars -> jars[KEY] = value }` — a **`suspend`** function | Writing a file takes time → call it from a coroutine. DataStore does the file work on a **background** thread for you (main-safe 🛡️). |

Your Chapter 18 skills are paying off! 🌊⚡

### One rule you must never break ⚠️

> **Only ONE DataStore object per file, in the whole app.**
> If two objects write the same file, DataStore throws an error: *"There are multiple DataStores active for the same file"*. 💥

The safe way: create it with a **property delegate** at the **top level** of a Kotlin file (outside any class). Then there is always exactly one:

```kotlin
val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "settings")
```

We'll explain every word of this line in a moment. 👇

---

## 21.4 Add the Library 📦

You'll need this in **every** project that uses DataStore (MyFirstApp, My Space, and the Quiz app).

### `gradle/libs.versions.toml`

```toml
[versions]
datastore = "1.1.4"

[libraries]
androidx-datastore-preferences = { group = "androidx.datastore", name = "datastore-preferences", version.ref = "datastore" }
```

### `build.gradle.kts (Module :app)`

```kotlin
dependencies {
    // ... existing lines ...
    implementation(libs.androidx.datastore.preferences)
}
```

**Sync Now** 🔄 ✅

---

## 21.5 A Tiny Example: A Counter That Remembers 🔢💾

Let's try DataStore in **MyFirstApp** (add the library there first). This is the simplest possible version, to **see** it work. Later we'll do it the **proper** way, with a repository.

### Step 1: Create the DataStore

Make a new file **`DataStore.kt`** next to `MainActivity.kt`:

```kotlin
package com.example.myfirstapp

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.preferencesDataStore

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "settings")   // (1)

val TAP_COUNT = intPreferencesKey("tap_count")                                               // (2)
```

**Every word of line (1)** 🔍:

| Part | Meaning |
|---|---|
| `val Context.dataStore` | An **extension property** (like extension functions, Chapter 4): now **every** `Context` (Activity, Application…) has a `.dataStore`. |
| `: DataStore<Preferences>` | Its type: a DataStore that holds **Preferences** (labeled jars 🫙). |
| `by preferencesDataStore(...)` | A **delegate** (like `by lazy` and `by remember`): "Create it **the first time** it's used, and **always** give back the **same one**." ✅ One per file — the rule is safe! |
| `name = "settings"` | The **file name**. DataStore saves to a file called `settings.preferences_pb` inside the app's private folder. 📁 |

| # | Code | Meaning |
|---|---|---|
| 2 | `val TAP_COUNT = intPreferencesKey("tap_count")` | A **key** 🔑 for an `Int` jar labeled `"tap_count"`. Written in `UPPER_CASE` because it never changes (a constant-like value). |

> ⚠️ The **label text** (`"tap_count"`) is what's saved in the file. If you **rename** it in a later version of your app, the old value is **lost** (the app looks for a jar that doesn't exist). Choose labels carefully and don't change them!

### Step 2: Use it in a Composable

```kotlin
@Composable
fun RememberingCounter() {
    val context = LocalContext.current                                         // (1)
    val scope = rememberCoroutineScope()

    val count by context.dataStore.data                                        // (2)
        .map { preferences -> preferences[TAP_COUNT] ?: 0 }                    // (3)
        .collectAsStateWithLifecycle(initialValue = 0)                         // (4)

    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("$count", style = MaterialTheme.typography.displayLarge)
        Text("taps — ever! 💾")
        Button(onClick = {
            scope.launch {
                context.dataStore.edit { preferences ->                        // (5)
                    val current = preferences[TAP_COUNT] ?: 0                  // (6)
                    preferences[TAP_COUNT] = current + 1                       // (7)
                }
            }
        }) {
            Text("Tap me 👆")
        }
    }
}
```

Imports:

```kotlin
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.platform.LocalContext
import androidx.datastore.preferences.core.edit
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.launch
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `LocalContext.current` | Get the `Context` inside a Composable (we need it for `.dataStore`). |
| 2 | `context.dataStore.data` | A `Flow<Preferences>` 🌊 — **all** the jars. It sends a new value every time **any** jar changes. |
| 3 | `.map { preferences -> preferences[TAP_COUNT] ?: 0 }` | We only want **one** jar. `preferences[TAP_COUNT]` reads it — it's `null` if the jar is **empty** (never saved yet), so `?: 0` gives a default (Chapter 3). Now it's a `Flow<Int>`. |
| 4 | `.collectAsStateWithLifecycle(initialValue = 0)` | Watch the flow as Compose state (Chapter 15). A plain `Flow` has no current value, so we give one to show **until** the file has been read: `0`. |
| 5 | `context.dataStore.edit { preferences -> ... }` | **Open the jars for writing.** Everything inside `{ }` is saved **together**, at once. It's `suspend`, so we use `scope.launch`. |
| 6 | `val current = preferences[TAP_COUNT] ?: 0` | Read the current value **inside** `edit`… |
| 7 | `preferences[TAP_COUNT] = current + 1` | …and write the new one. Like a `MutableMap` (Chapter 3). |

Call `RememberingCounter()` inside `setContent { MyFirstAppTheme { ... } }` and **run**.

### 🧪 The big test

1. Tap 7 times. → **7**
2. Rotate 🔄 → still **7** (of course)
3. **Close the app completely**: open **Recents** (the square button, or swipe up and hold) and **swipe the app away**. 👋
4. Open the app again… → **7**! 🎉🎉🎉

**Your app has a memory now!** 💾 Even after restarting the phone.

> 🤔 **Why read the value inside `edit` (line 6) instead of using `count`?**
> Because `count` might be **a moment old**. If you tap very fast, two taps could both read "7" and both write "8" — and one tap is lost! 😱 Reading **inside** `edit` always gets the **real, current** value, because DataStore runs edits **one at a time**. ✅

> ⚠️ This example uses DataStore **directly in a Composable** — just to learn. In real apps, the UI should **not** know where data is saved (Chapter 16). So let's do it properly! 🏗️

---

## 21.6 🛠️ Project: My Space 🏠

### What are we building?

```
 FIRST TIME ONLY                     EVERY TIME AFTER
┌──────────────────────┐           ┌──────────────────────┐           ┌──────────────────────┐
│                      │           │ My Space 🏠       ⚙️  │  tap ⚙️    │ ⬅️ Settings           │
│      👋 Welcome!      │           │                      │ ───────▶  │                      │
│                      │  Let's go │   Hello, Sam! 👋      │           │ Theme 🎨              │
│ What's your name?    │ ────────▶ │                      │           │ (•) System           │
│ [ Sam            ]   │           │ You've opened        │           │ ( ) Light ☀️          │
│                      │           │ My Space 12 times 🎉  │           │ ( ) Dark 🌙           │
│   [ Let's go 🚀 ]     │           │                      │           │                      │
│                      │           │                      │           │ Your name: Sam       │
└──────────────────────┘           └──────────────────────┘           │         [Change ✏️]   │
                                                                      │ [Reset everything 🗑️] │
                                                                      └──────────────────────┘
```

### Requirements 📋

1. The **Welcome** screen appears **only the very first time**. It asks for the user's **name**.
2. After that, the app **always** opens on **Home**: "Hello, Sam! 👋".
3. Home shows **how many times** the app was opened. 🔢
4. **Settings** ⚙️: choose the **theme** — System, Light ☀️, or Dark 🌙. The whole app changes **immediately**.
5. Settings: **change** the name with a dialog ✏️.
6. Settings: **Reset everything** 🗑️ (with a "Are you sure?" dialog) → back to the Welcome screen.
7. **Everything** survives closing the app. 💾

### Create the project

1. **File → New → New Project… → Empty Activity**.
2. **Name:** `My Space` · **Package:** `com.example.myspace` · **Finish**.
3. Your theme is **`MySpaceTheme`**.

### Libraries

Add **DataStore** (21.4) plus the usual Part 4 set — Navigation, serialization, and lifecycle (exactly like Chapter 17, section 17.3). **Sync** 🔄 ✅

### The files 📁

```
com.example.myspace
 ├── MySpaceApplication.kt
 ├── MainActivity.kt
 ├── data/
 │    ├── UserSettings.kt                 (UserSettings + ThemeMode)
 │    ├── SettingsRepository.kt           (interface)
 │    └── DataStoreSettingsRepository.kt
 ├── di/
 │    └── AppContainer.kt                 (the ONE DataStore lives here)
 └── ui/
      ├── theme/                          (already there)
      ├── MainViewModel.kt
      ├── navigation/
      │    ├── Routes.kt
      │    └── MySpaceNavHost.kt
      ├── welcome/WelcomeScreen.kt
      ├── home/HomeScreen.kt
      └── settings/SettingsScreen.kt
```

---

## 21.7 Step 1: The Data Layer 🏪

### `data/UserSettings.kt`

```kotlin
package com.example.myspace.data

enum class ThemeMode(val label: String) {                    // (1)
    SYSTEM("System default 📱"),
    LIGHT("Light ☀️"),
    DARK("Dark 🌙")
}

data class UserSettings(                                     // (2)
    val userName: String = "",
    val hasSeenWelcome: Boolean = false,
    val themeMode: ThemeMode = ThemeMode.SYSTEM,
    val openCount: Int = 0
)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `enum class ThemeMode` | The 3 theme choices. "System" = follow the phone's own dark mode setting. |
| 2 | `data class UserSettings` | **All** our saved settings in **one** clean object. The rest of the app uses **this** — it never sees keys or jars. 🫙🚫 The default values are what a **brand-new** user has. |

### `data/SettingsRepository.kt`

```kotlin
package com.example.myspace.data

import kotlinx.coroutines.flow.Flow

interface SettingsRepository {
    val settings: Flow<UserSettings>                         // (1)

    suspend fun finishWelcome(userName: String)              // (2)
    suspend fun setUserName(userName: String)
    suspend fun setThemeMode(themeMode: ThemeMode)
    suspend fun increaseOpenCount()
    suspend fun clearAll()
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `val settings: Flow<UserSettings>` | **Read:** a stream of settings 🌊. Every change → a new `UserSettings`. |
| 2 | `suspend fun ...` | **Write:** one function per **action**. They're `suspend` because writing a file takes time. |

> 💡 Notice: the interface says **nothing** about DataStore. Tomorrow we could save settings somewhere else, and only **one** class would change. (Chapter 16's promise 🤝)

### `data/DataStoreSettingsRepository.kt`

```kotlin
package com.example.myspace.data

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.emptyPreferences
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import java.io.IOException

class DataStoreSettingsRepository(
    private val dataStore: DataStore<Preferences>                              // (1)
) : SettingsRepository {

    private object Keys {                                                      // (2)
        val USER_NAME = stringPreferencesKey("user_name")
        val HAS_SEEN_WELCOME = booleanPreferencesKey("has_seen_welcome")
        val THEME_MODE = stringPreferencesKey("theme_mode")
        val OPEN_COUNT = intPreferencesKey("open_count")
    }

    override val settings: Flow<UserSettings> = dataStore.data
        .catch { error ->                                                      // (3)
            if (error is IOException) emit(emptyPreferences()) else throw error
        }
        .map { preferences ->                                                  // (4)
            UserSettings(
                userName = preferences[Keys.USER_NAME] ?: "",
                hasSeenWelcome = preferences[Keys.HAS_SEEN_WELCOME] ?: false,
                themeMode = themeModeFrom(preferences[Keys.THEME_MODE]),
                openCount = preferences[Keys.OPEN_COUNT] ?: 0
            )
        }

    override suspend fun finishWelcome(userName: String) {
        dataStore.edit { preferences ->                                        // (5)
            preferences[Keys.USER_NAME] = userName
            preferences[Keys.HAS_SEEN_WELCOME] = true
        }
    }

    override suspend fun setUserName(userName: String) {
        dataStore.edit { it[Keys.USER_NAME] = userName }
    }

    override suspend fun setThemeMode(themeMode: ThemeMode) {
        dataStore.edit { it[Keys.THEME_MODE] = themeMode.name }                // (6)
    }

    override suspend fun increaseOpenCount() {
        dataStore.edit { preferences ->
            preferences[Keys.OPEN_COUNT] = (preferences[Keys.OPEN_COUNT] ?: 0) + 1
        }
    }

    override suspend fun clearAll() {
        dataStore.edit { it.clear() }                                          // (7)
    }

    private fun themeModeFrom(savedName: String?): ThemeMode =                 // (8)
        ThemeMode.entries.find { it.name == savedName } ?: ThemeMode.SYSTEM
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `private val dataStore: DataStore<Preferences>` | The repository **receives** the DataStore — it doesn't create it. (The AppContainer does — one per file! ✅) |
| 2 | `private object Keys { ... }` | All the keys in **one** tidy place 🗂️ (an `object`, Chapter 4). `private` → only this class uses them. Write `Keys.USER_NAME` to use one. |
| 3 | `.catch { error -> ... }` | Reading the file **can** fail (for example, the file is broken 💔). If it's an `IOException`, act as if the jars were **empty** (`emptyPreferences()`) → the app uses the **defaults** instead of crashing. Other errors are **real bugs** → `throw` them. (Flow `catch`, Chapter 18) |
| 4 | `.map { preferences -> UserSettings(...) }` | Turn the **jars** into our clean **`UserSettings`**. Every jar can be empty (`null`), so each one gets a **default** with `?:`. |
| 5 | `dataStore.edit { ... }` with **two** writes | Name **and** "seen welcome" are saved **together**, in **one** step. Either both are saved or neither — never half. ✅ (This is called **atomic**.) |
| 6 | `themeMode.name` | DataStore can't save an **enum** — only simple types. So we save its **name** as a `String`: `"DARK"`. (Same trick as the Quiz routes! 🔤) |
| 7 | `it.clear()` | **Empty all the jars.** Back to a brand-new user. 🗑️ |
| 8 | `themeModeFrom(savedName)` | Turn `"DARK"` back into `ThemeMode.DARK`. `find { ... }` returns `null` if nothing matches → use `SYSTEM`. |

> 🤔 **Why `find` and not `ThemeMode.valueOf(savedName)`?**
> `valueOf` **crashes** 💥 if the name doesn't exist. Imagine in a future version you **rename** `DARK` to `NIGHT`. Users who saved `"DARK"` would crash **every time** they open the app! 😱 `find` + a default is **safe**. 🛡️ **Saved data comes from the past** — always expect surprises.

---

## 21.8 Step 2: The AppContainer and Application 🧰

The AppContainer now needs a **`Context`** to reach the DataStore. That's new!

### `di/AppContainer.kt`

```kotlin
package com.example.myspace.di

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.preferencesDataStore
import com.example.myspace.data.DataStoreSettingsRepository
import com.example.myspace.data.SettingsRepository

private val Context.settingsDataStore: DataStore<Preferences>
    by preferencesDataStore(name = "settings")                     // (1)

interface AppContainer {
    val settingsRepository: SettingsRepository
}

class DefaultAppContainer(
    private val context: Context                                   // (2)
) : AppContainer {

    override val settingsRepository: SettingsRepository by lazy {
        DataStoreSettingsRepository(context.settingsDataStore)     // (3)
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `private val Context.settingsDataStore ... by preferencesDataStore(...)` | The **one and only** DataStore for `"settings"` 🫙. At the **top level** of the file. `private` → only this file can touch it, so nobody else can accidentally use the file directly. 🔒 |
| 2 | `DefaultAppContainer(private val context: Context)` | The container now **receives** a Context. |
| 3 | `context.settingsDataStore` | Hand the DataStore to the repository. |

### `MySpaceApplication.kt`

```kotlin
package com.example.myspace

import android.app.Application
import com.example.myspace.di.AppContainer
import com.example.myspace.di.DefaultAppContainer

class MySpaceApplication : Application() {

    lateinit var container: AppContainer

    override fun onCreate() {
        super.onCreate()
        container = DefaultAppContainer(context = this)            // 👈 the Application IS a Context
    }
}
```

> 🤔 **Is it OK to keep a Context in the container?** Here, yes! ✅ The **Application** lives as long as the app itself, so keeping it is safe. ❌ **Never** keep an **Activity** — it's destroyed on every rotation, and holding on to it causes a **memory leak** 💧 (Chapter 15's rule).

### `AndroidManifest.xml`

```xml
<application
    android:name=".MySpaceApplication"
    ... the rest stays the same ... >
```

(No Internet permission needed — DataStore saves on the **phone**. 📱)

---

## 21.9 Step 3: The MainViewModel 🧠

All three screens of this small app show the **same** few settings. So we'll use **one** ViewModel for the whole app, created by the Activity.

> 💡 In Chapter 16 we gave **each screen its own** ViewModel. That's still the best plan for **bigger** apps. For a tiny app where every screen shares the same settings, one ViewModel keeps things simple. Both are fine — choose what keeps **your** code clear. 😊

### `ui/MainViewModel.kt`

```kotlin
package com.example.myspace.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.ViewModelProvider.AndroidViewModelFactory.Companion.APPLICATION_KEY
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.example.myspace.MySpaceApplication
import com.example.myspace.data.SettingsRepository
import com.example.myspace.data.ThemeMode
import com.example.myspace.data.UserSettings
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

sealed interface MainUiState {                                                // (1)
    data object Loading : MainUiState
    data class Ready(val settings: UserSettings) : MainUiState
}

class MainViewModel(
    private val settingsRepository: SettingsRepository
) : ViewModel() {

    val uiState: StateFlow<MainUiState> = settingsRepository.settings
        .map { settings -> MainUiState.Ready(settings) }                       // (2)
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = MainUiState.Loading                                 // (3)
        )

    init {
        viewModelScope.launch {
            settingsRepository.increaseOpenCount()                             // (4)
        }
    }

    fun onWelcomeFinished(name: String) {
        viewModelScope.launch {
            settingsRepository.finishWelcome(name.trim())                      // (5)
        }
    }

    fun onNameChange(name: String) {
        viewModelScope.launch {
            settingsRepository.setUserName(name.trim())
        }
    }

    fun onThemeModeChange(themeMode: ThemeMode) {
        viewModelScope.launch {
            settingsRepository.setThemeMode(themeMode)
        }
    }

    fun onResetConfirmed() {
        viewModelScope.launch {
            settingsRepository.clearAll()
        }
    }

    companion object {
        val Factory: ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val app = this[APPLICATION_KEY] as MySpaceApplication
                MainViewModel(settingsRepository = app.container.settingsRepository)
            }
        }
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `sealed interface MainUiState` | Two situations: **Loading** (we haven't read the file yet ⏳) and **Ready** (we know the settings ✅). |
| 2 | `.map { settings -> MainUiState.Ready(settings) }` | Every new `UserSettings` from the repository → wrap it in `Ready`. |
| 3 | `initialValue = MainUiState.Loading` | **Before** the file has been read, we **don't know** if the user has seen the Welcome screen — so we're `Loading`. This is **important**, see 21.11! |
| 4 | `init { ... increaseOpenCount() }` | The ViewModel is created **once** each time the app starts (not on rotation 🔄), so this counts **app opens**. 🔢 |
| 5 | `name.trim()` | Remove spaces at the start and end: `"  Sam "` → `"Sam"`. |

> 🎯 Every write is `viewModelScope.launch { repository.something() }`. **We never update the state by hand!** We write to DataStore → DataStore's `data` Flow sends new settings → `map` → `stateIn` → the screen updates. **One** source of truth, flowing in **one** direction. 🌊➡️📱 (Chapter 16)

---

## 21.10 Step 4: The Screens 🎨

### `ui/welcome/WelcomeScreen.kt`

```kotlin
package com.example.myspace.ui.welcome

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun WelcomeScreen(
    onStartClick: (name: String) -> Unit,
    modifier: Modifier = Modifier
) {
    var name by rememberSaveable { mutableStateOf("") }                   // (1)

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(32.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("👋", fontSize = 72.sp)
        Text("Welcome!", style = MaterialTheme.typography.headlineLarge)
        Text("What's your name?", style = MaterialTheme.typography.titleMedium)

        OutlinedTextField(
            value = name,
            onValueChange = { name = it },
            label = { Text("Your name") },
            singleLine = true,
            keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Words),
            modifier = Modifier.fillMaxWidth()
        )

        Button(
            onClick = { onStartClick(name) },
            enabled = name.isNotBlank()                                    // (2)
        ) {
            Text("Let's go 🚀")
        }
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `rememberSaveable { mutableStateOf("") }` | While typing, the name is **UI state** (Chapter 8) — we only **save** it to DataStore when the button is pressed. And remember Chapter 18: text fields want their text **immediately**, not through a Flow. ⌨️ |
| 2 | `enabled = name.isNotBlank()` | No empty names. `isNotBlank()` is `false` for `""` **and** for `"   "`. |

### `ui/home/HomeScreen.kt`

```kotlin
package com.example.myspace.ui.home

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.myspace.ui.theme.MySpaceTheme

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    userName: String,
    openCount: Int,
    onSettingsClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Scaffold(
        modifier = modifier,
        topBar = {
            TopAppBar(
                title = { Text("My Space 🏠") },
                actions = {
                    IconButton(onClick = onSettingsClick) {
                        Icon(Icons.Filled.Settings, contentDescription = "Settings")
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .padding(innerPadding)
                .fillMaxSize()
                .padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(24.dp, Alignment.CenterVertically),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Hello, ${userName.ifBlank { "friend" }}! 👋",          // (1)
                style = MaterialTheme.typography.headlineMedium,
                textAlign = TextAlign.Center
            )
            Text(
                text = openCountMessage(openCount),
                style = MaterialTheme.typography.titleMedium,
                textAlign = TextAlign.Center
            )
        }
    }
}

fun openCountMessage(count: Int): String = when (count) {                    // (2)
    0, 1 -> "This is your first visit. Nice to meet you! 🤝"
    else -> "You've opened My Space $count times 🎉"
}

@Preview(showBackground = true)
@Composable
fun HomeScreenPreview() {
    MySpaceTheme {
        HomeScreen(userName = "Sam", openCount = 12, onSettingsClick = {})
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `userName.ifBlank { "friend" }` | If the name is empty, use `"friend"` instead. (Just after "Let's go", the saved name may arrive a tiny moment later — this avoids "Hello, !" 😅.) |
| 2 | `when (count) { 0, 1 -> ... }` | `0, 1` = "0 **or** 1" (Chapter 2). A nicer message for the first visit. |

### `ui/settings/SettingsScreen.kt`

```kotlin
package com.example.myspace.ui.settings

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.myspace.data.ThemeMode
import com.example.myspace.ui.theme.MySpaceTheme

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    userName: String,
    themeMode: ThemeMode,
    onThemeModeChange: (ThemeMode) -> Unit,
    onNameChange: (String) -> Unit,
    onResetConfirmed: () -> Unit,
    onBackClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    var showNameDialog by rememberSaveable { mutableStateOf(false) }          // (1)
    var showResetDialog by rememberSaveable { mutableStateOf(false) }

    Scaffold(
        modifier = modifier,
        topBar = {
            TopAppBar(
                title = { Text("Settings") },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .padding(innerPadding)
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text("Theme 🎨", style = MaterialTheme.typography.titleMedium)

            Column(modifier = Modifier.selectableGroup()) {                    // (2)
                ThemeMode.entries.forEach { mode ->
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier
                            .fillMaxWidth()
                            .selectable(                                       // (3)
                                selected = mode == themeMode,
                                onClick = { onThemeModeChange(mode) },
                                role = Role.RadioButton
                            )
                            .padding(vertical = 8.dp)
                    ) {
                        RadioButton(selected = mode == themeMode, onClick = null)   // (4)
                        Text(mode.label, modifier = Modifier.padding(start = 12.dp))
                    }
                }
            }

            HorizontalDivider()

            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = "Your name: $userName",
                    style = MaterialTheme.typography.bodyLarge,
                    modifier = Modifier.weight(1f)
                )
                TextButton(onClick = { showNameDialog = true }) {
                    Text("Change ✏️")
                }
            }

            HorizontalDivider()

            Button(
                onClick = { showResetDialog = true },
                colors = ButtonDefaults.buttonColors(                          // (5)
                    containerColor = MaterialTheme.colorScheme.error,
                    contentColor = MaterialTheme.colorScheme.onError
                )
            ) {
                Text("Reset everything 🗑️")
            }
        }
    }

    if (showNameDialog) {
        ChangeNameDialog(
            currentName = userName,
            onSave = { newName ->
                onNameChange(newName)
                showNameDialog = false
            },
            onDismiss = { showNameDialog = false }
        )
    }

    if (showResetDialog) {
        AlertDialog(
            onDismissRequest = { showResetDialog = false },
            title = { Text("Reset everything?") },
            text = { Text("Your name, theme, and visit count will be deleted. This can't be undone.") },
            confirmButton = {
                TextButton(onClick = {
                    showResetDialog = false
                    onResetConfirmed()
                }) {
                    Text("Reset", color = MaterialTheme.colorScheme.error)
                }
            },
            dismissButton = {
                TextButton(onClick = { showResetDialog = false }) { Text("Cancel") }
            }
        )
    }
}

@Composable
fun ChangeNameDialog(
    currentName: String,
    onSave: (String) -> Unit,
    onDismiss: () -> Unit
) {
    var text by rememberSaveable { mutableStateOf(currentName) }               // (6)

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Change your name") },
        text = {
            OutlinedTextField(
                value = text,
                onValueChange = { text = it },
                singleLine = true,
                label = { Text("Name") }
            )
        },
        confirmButton = {
            TextButton(onClick = { onSave(text) }, enabled = text.isNotBlank()) {
                Text("Save")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        }
    )
}

@Preview(showBackground = true)
@Composable
fun SettingsScreenPreview() {
    MySpaceTheme {
        SettingsScreen(
            userName = "Sam",
            themeMode = ThemeMode.DARK,
            onThemeModeChange = {}, onNameChange = {}, onResetConfirmed = {}, onBackClick = {}
        )
    }
}
```

**The important parts:**

| # | Code | Meaning |
|---|---|---|
| 1 | `showNameDialog`, `showResetDialog` | "Is the dialog open?" is pure **UI** state → `rememberSaveable` (Chapter 11). Not saved to DataStore! |
| 2 | `Modifier.selectableGroup()` | Tells screen readers ♿ "these radio buttons belong **together**". |
| 3 | `.selectable(selected, onClick, role = Role.RadioButton)` | Makes the **whole row** tappable — not just the tiny circle. 👆 Much easier to use. (Chapter 9) |
| 4 | `RadioButton(..., onClick = null)` | The row already handles the tap, so the button itself does nothing extra. |
| 5 | `ButtonDefaults.buttonColors(containerColor = error ...)` | A **red** button for a **dangerous** action. 🟥 |
| 6 | `rememberSaveable { mutableStateOf(currentName) }` | The dialog **starts** with the current name, and the user edits a **local** copy. Only **Save** writes it to DataStore. **Cancel** → nothing changes. ✅ |

> 💡 **Why a dialog for the name, instead of a text field right on the Settings screen?** Remember Chapter 18: a text field's text should **not** come through a Flow (it would come from DataStore → Flow → `stateIn` → screen). The cursor can jump! ⌨️😖 Editing a **local** copy in a dialog avoids the problem completely. 😎

---

## 21.11 Step 5: Navigation, Theme, and MainActivity 🧭🎨

### `ui/navigation/Routes.kt`

```kotlin
package com.example.myspace.ui.navigation

import kotlinx.serialization.Serializable

@Serializable object Welcome
@Serializable object Home
@Serializable object Settings
```

(Several short declarations on separate lines are fine — each is its own `object`.)

### `ui/navigation/MySpaceNavHost.kt`

```kotlin
package com.example.myspace.ui.navigation

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.myspace.data.UserSettings
import com.example.myspace.ui.MainViewModel
import com.example.myspace.ui.home.HomeScreen
import com.example.myspace.ui.settings.SettingsScreen
import com.example.myspace.ui.welcome.WelcomeScreen

@Composable
fun MySpaceNavHost(
    settings: UserSettings,
    viewModel: MainViewModel
) {
    val navController = rememberNavController()

    val startDestination: Any = remember {                                    // (1)
        if (settings.hasSeenWelcome) Home else Welcome
    }

    NavHost(navController = navController, startDestination = startDestination) {

        composable<Welcome> {
            Scaffold { innerPadding ->
                WelcomeScreen(
                    onStartClick = { name ->
                        viewModel.onWelcomeFinished(name)
                        navController.navigate(Home) {
                            popUpTo<Welcome> { inclusive = true }              // (2)
                        }
                    },
                    modifier = Modifier.padding(innerPadding)
                )
            }
        }

        composable<Home> {
            HomeScreen(
                userName = settings.userName,
                openCount = settings.openCount,
                onSettingsClick = { navController.navigate(Settings) }
            )
        }

        composable<Settings> {
            SettingsScreen(
                userName = settings.userName,
                themeMode = settings.themeMode,
                onThemeModeChange = viewModel::onThemeModeChange,
                onNameChange = viewModel::onNameChange,
                onResetConfirmed = {
                    viewModel.onResetConfirmed()
                    navController.navigate(Welcome) {
                        popUpTo(navController.graph.id) { inclusive = true }  // (3)
                    }
                },
                onBackClick = { navController.popBackStack() }
            )
        }
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `val startDestination: Any = remember { ... }` | **Decide once** where the app starts: Welcome (first time) or Home. `remember` with no key → computed **one time** and kept. We **don't** want it to change while the app is running (changing a NavHost's start destination later can confuse it). `Any` = "any type" — `Home` and `Welcome` are different objects, so we need a type that fits both. |
| 2 | `popUpTo<Welcome> { inclusive = true }` | After "Let's go", **remove** Welcome from the back stack. Back on Home → leave the app, not back to Welcome. (Chapter 13 👋) |
| 3 | `popUpTo(navController.graph.id) { inclusive = true }` | After a reset: **remove every screen** from the back stack 🥞🗑️, then show Welcome. `graph.id` = "the whole graph — everything". Back on Welcome → leave the app. ✅ |

### `MainActivity.kt` — theme and loading

```kotlin
package com.example.myspace

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.myspace.data.ThemeMode
import com.example.myspace.ui.MainUiState
import com.example.myspace.ui.MainViewModel
import com.example.myspace.ui.navigation.MySpaceNavHost
import com.example.myspace.ui.theme.MySpaceTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            val viewModel: MainViewModel = viewModel(factory = MainViewModel.Factory)
            val uiState by viewModel.uiState.collectAsStateWithLifecycle()

            when (val state = uiState) {
                MainUiState.Loading -> {                                       // (1)
                    MySpaceTheme {
                        Surface(modifier = Modifier.fillMaxSize()) { }
                    }
                }

                is MainUiState.Ready -> {
                    val darkTheme = when (state.settings.themeMode) {          // (2)
                        ThemeMode.SYSTEM -> isSystemInDarkTheme()
                        ThemeMode.LIGHT -> false
                        ThemeMode.DARK -> true
                    }
                    MySpaceTheme(darkTheme = darkTheme) {                      // (3)
                        MySpaceNavHost(settings = state.settings, viewModel = viewModel)
                    }
                }
            }
        }
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `MainUiState.Loading -> { ... }` | While the settings file is being read (usually a few **milliseconds**), show an **empty** surface. Why not show Home or Welcome right away? Because we **don't know yet** which one is correct! Showing Welcome for a flash, then jumping to Home, looks broken. 😬 |
| 2 | `when (state.settings.themeMode)` | Turn the saved choice into "dark or not?". `isSystemInDarkTheme()` asks the **phone's** setting. |
| 3 | `MySpaceTheme(darkTheme = darkTheme)` | The theme function Android Studio made for you (Chapter 7) **already** has a `darkTheme` parameter! We just pass our value. Change the setting → new settings flow in → recomposition → the **whole app** changes color instantly. 🎨✨ |

> 💡 Real apps often show their **logo** during this tiny loading moment, using the **SplashScreen** library (`installSplashScreen()`). An empty surface is fine for now.

**Run the app!** ▶️

---

## 21.12 Test Checklist ✅

| Test | Expected | ✓ |
|---|---|---|
| First open | Welcome screen 👋 | ☐ |
| "Let's go" with an empty name | Button disabled | ☐ |
| Type "Sam" → Let's go | Home: "Hello, Sam! 👋" + first-visit message | ☐ |
| Back on Home | Leaves the app (Welcome is gone) | ☐ |
| **Swipe the app away** from Recents, reopen | **Home** directly — no Welcome! 💾 | ☐ |
| Reopen a few times | "You've opened My Space 3 times", 4, 5… | ☐ |
| Rotate on Home 🔄 | Count does **not** go up (ViewModel survives) | ☐ |
| Settings → Dark 🌙 | Whole app turns dark **immediately** | ☐ |
| Close and reopen | Still dark 💾 | ☐ |
| System + change the phone's dark mode | App follows the phone | ☐ |
| Change name → Cancel | Name unchanged | ☐ |
| Change name → "Mia" → Save | Home says "Hello, Mia! 👋" | ☐ |
| Reset → Cancel | Nothing happens | ☐ |
| Reset → Reset | Welcome screen; Back leaves the app | ☐ |
| After reset, close and reopen | Welcome again (everything cleared) | ☐ |

### Where is the file? 🔍 (optional)

Android Studio can show the phone's files: **View → Tool Windows → Device Explorer**. Open:

```
/data/data/com.example.myspace/files/datastore/settings.preferences_pb
```

That's your jar shelf! 🫙 (It's a special compact format, not easy to read — but now you know it's **really** there.)

> 🧹 **Want to start fresh while testing?** On the phone: **Settings → Apps → My Space → Storage → Clear storage**. Or **uninstall** the app. Both delete the DataStore file.

---

## 21.13 🏅 Upgrade the Quiz App: Best Scores!

Remember **Challenge 5** from Chapter 17? *"Show 'Best: 4/5' on each topic card."* We promised to come back. Let's do it now! 💪

Open your **Quiz** project (`com.example.quiz`). Add the **DataStore** library (21.4) and **Sync**.

```
┌──────────────────────────┐
│ ╭──────────────────────╮ │
│ │ 🚀 Space              │ │
│ │ 5 questions           │ │
│ │ Best: 4 / 5 🏅         │ │
│ ╰──────────────────────╯ │
│ ╭──────────────────────╮ │
│ │ 🐾 Animals            │ │
│ │ 5 questions           │ │
│ │ Not played yet        │ │
│ ╰──────────────────────╯ │
└──────────────────────────┘
```

### Step 1: `data/BestScoreRepository.kt` (new)

```kotlin
package com.example.quiz.data

import com.example.quiz.data.model.QuizCategory
import kotlinx.coroutines.flow.Flow

interface BestScoreRepository {
    val bestScores: Flow<Map<QuizCategory, Int>>                     // (1)
    suspend fun saveScore(category: QuizCategory, score: Int)        // (2)
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `Flow<Map<QuizCategory, Int>>` | A **map** 🗺️: topic → best score. A topic that was **never played** is simply **not** in the map. |
| 2 | `saveScore(...)` | "Here's a new score." The repository decides if it's a **new best**. |

### Step 2: `data/DataStoreBestScoreRepository.kt` (new)

```kotlin
package com.example.quiz.data

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.emptyPreferences
import androidx.datastore.preferences.core.intPreferencesKey
import com.example.quiz.data.model.QuizCategory
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import java.io.IOException

class DataStoreBestScoreRepository(
    private val dataStore: DataStore<Preferences>
) : BestScoreRepository {

    private fun keyFor(category: QuizCategory) =                              // (1)
        intPreferencesKey("best_score_${category.name}")

    override val bestScores: Flow<Map<QuizCategory, Int>> = dataStore.data
        .catch { error ->
            if (error is IOException) emit(emptyPreferences()) else throw error
        }
        .map { preferences ->
            QuizCategory.entries
                .mapNotNull { category ->                                     // (2)
                    val best = preferences[keyFor(category)]
                    if (best == null) null else category to best
                }
                .toMap()                                                      // (3)
        }

    override suspend fun saveScore(category: QuizCategory, score: Int) {
        dataStore.edit { preferences ->
            val oldBest = preferences[keyFor(category)] ?: -1                 // (4)
            if (score > oldBest) {
                preferences[keyFor(category)] = score                         // (5)
            }
        }
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `keyFor(category)` | **One key per topic**, made from its name: `"best_score_SPACE"`, `"best_score_ANIMALS"`, … Add a topic → it gets a key **automatically**. 😎 |
| 2 | `.mapNotNull { ... }` | For each topic: if there's a saved best, make a **pair** `category to best` (Chapter 3, `to`); if not, `null` → **skipped**. (`mapNotNull`: Chapter 17.) |
| 3 | `.toMap()` | A list of pairs → a `Map`. `[(SPACE, 4), (KOTLIN, 5)]` → `{SPACE=4, KOTLIN=5}` |
| 4 | `?: -1` | Never played → `-1`, so **any** score (even 0) is a "new best". |
| 5 | `if (score > oldBest)` | Only save if it's **better**. A worse score never replaces a good one. 🏅 Because this read-and-write happens **inside** `edit`, it's always correct, even if two saves happen at once (21.5). |

### Step 3: `di/AppContainer.kt` (changed)

```kotlin
package com.example.quiz.di

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.preferencesDataStore
import com.example.quiz.data.BestScoreRepository
import com.example.quiz.data.DataStoreBestScoreRepository
import com.example.quiz.data.InMemoryQuestionRepository
import com.example.quiz.data.QuestionRepository

private val Context.quizDataStore: DataStore<Preferences>
    by preferencesDataStore(name = "quiz_scores")                             // 👈 new

interface AppContainer {
    val questionRepository: QuestionRepository
    val bestScoreRepository: BestScoreRepository                              // 👈 new
}

class DefaultAppContainer(
    private val context: Context                                              // 👈 new
) : AppContainer {

    override val questionRepository: QuestionRepository by lazy {
        InMemoryQuestionRepository()
    }

    override val bestScoreRepository: BestScoreRepository by lazy {          // 👈 new
        DataStoreBestScoreRepository(context.quizDataStore)
    }
}
```

### Step 4: `QuizApplication.kt` (one change)

```kotlin
container = DefaultAppContainer(context = this)
```

### Step 5: Save the score — `QuizViewModel.kt` (changed)

The best moment to save is when the user **answers the last question** — the score is **final** then. Three changes:

**a) The constructor gets the new repository:**

```kotlin
class QuizViewModel(
    private val savedStateHandle: SavedStateHandle,
    private val repository: QuestionRepository,
    private val bestScoreRepository: BestScoreRepository                       // 👈 new
) : ViewModel() {
```

**b) `selectOption` saves after the last answer:**

```kotlin
private fun selectOption(index: Int) {
    val state = _uiState.value
    if (state.isAnswered) return
    val isCorrect = index == state.currentQuestion?.correctIndex
    updateState {
        it.copy(
            selectedOption = index,
            score = if (isCorrect) it.score + 1 else it.score
        )
    }

    if (state.isLastQuestion) {                                                // 👈 new
        val finalScore = _uiState.value.score
        viewModelScope.launch {
            bestScoreRepository.saveScore(category, finalScore)
        }
    }
}
```

**c) The factory passes it in:**

```kotlin
QuizViewModel(
    savedStateHandle = createSavedStateHandle(),
    repository = app.container.questionRepository,
    bestScoreRepository = app.container.bestScoreRepository                    // 👈 new
)
```

New imports: `androidx.lifecycle.viewModelScope`, `kotlinx.coroutines.launch`, `com.example.quiz.data.BestScoreRepository`.

| Code | Meaning |
|---|---|
| `if (state.isLastQuestion)` | `state` is the state **before** the answer — still on the last question. ✅ |
| `_uiState.value.score` | The score **after** this answer was counted. |
| `viewModelScope.launch { ... }` | Writing is `suspend` → start a coroutine. It's quick, and finishes while the user reads the explanation 💡. |

> 🤔 Why save **here** and not on the Result screen? The Result screen can be shown again by rotation or process death — and it would save again. Saving at the **moment** the quiz ends happens exactly **once**. 🎯 (And even if it did happen twice, `saveScore` only keeps the **best**, so nothing would break. Two safety nets! 🛡️🛡️)

### Step 6: Show the scores — `StartScreen.kt` (changed)

Add a parameter, and pass the best score to each card:

```kotlin
@Composable
fun StartScreen(
    questionCount: (QuizCategory) -> Int,
    bestScores: Map<QuizCategory, Int>,                                       // 👈 new
    onCategoryClick: (QuizCategory) -> Unit,
    modifier: Modifier = Modifier
) {
    // ... same as before, but in the loop:
        QuizCategory.entries.forEach { category ->
            CategoryCard(
                category = category,
                count = questionCount(category),
                best = bestScores[category],                                  // 👈 new (Int? — null if never played)
                onClick = { onCategoryClick(category) }
            )
        }
    // ...
}

@Composable
private fun CategoryCard(category: QuizCategory, count: Int, best: Int?, onClick: () -> Unit) {
    ElevatedCard(onClick = onClick, modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.padding(20.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(category.emoji, fontSize = 40.sp)
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(category.label, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Text(
                    text = "$count questions",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(                                                         // 👈 new
                    text = if (best == null) "Not played yet" else "Best: $best / $count 🏅",
                    style = MaterialTheme.typography.bodyMedium,
                    color = if (best == null) MaterialTheme.colorScheme.onSurfaceVariant
                            else MaterialTheme.colorScheme.primary
                )
            }
            Text("▶", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.primary)
        }
    }
}
```

Update the preview: `StartScreen(questionCount = { 5 }, bestScores = mapOf(QuizCategory.SPACE to 4), onCategoryClick = {})`.

| Code | Meaning |
|---|---|
| `bestScores[category]` | Reading a `Map` with `[ ]` gives `null` if the key isn't there (Chapter 3) → "Not played yet". |

### Step 7: Connect it — `QuizNavHost.kt` and `MainActivity.kt` (changed)

```kotlin
@Composable
fun QuizNavHost(
    repository: QuestionRepository,
    bestScoreRepository: BestScoreRepository                                  // 👈 new
) {
    val navController = rememberNavController()
    val bestScores by bestScoreRepository.bestScores
        .collectAsStateWithLifecycle(initialValue = emptyMap())               // 👈 new

    NavHost(navController = navController, startDestination = Start) {
        composable<Start> {
            Scaffold { innerPadding ->
                StartScreen(
                    questionCount = { category -> repository.countQuestions(category) },
                    bestScores = bestScores,                                  // 👈 new
                    onCategoryClick = { category ->
                        navController.navigate(Quiz(categoryName = category.name))
                    },
                    modifier = Modifier.padding(innerPadding)
                )
            }
        }
        // ... Quiz and Result stay the same ...
    }
}
```

New imports: `androidx.compose.runtime.getValue`, `androidx.lifecycle.compose.collectAsStateWithLifecycle`, `com.example.quiz.data.BestScoreRepository`.

And in `MainActivity`:

```kotlin
val container = (application as QuizApplication).container
setContent {
    QuizTheme {
        QuizNavHost(
            repository = container.questionRepository,
            bestScoreRepository = container.bestScoreRepository
        )
    }
}
```

> 💡 The Start screen still has **no ViewModel** (Chapter 17 said: not every screen needs one). We collect the flow right in the NavHost. If the Start screen grows, give it a `StartViewModel` with `stateIn` — you know how! 😉

**Run it!** ▶️ Play Space, get 3/5 → "Best: 3 / 5 🏅". Play again, get 2/5 → **still** 3/5. Get 5/5 → 5/5! 🏆 **Close the app completely**, reopen → the scores are **still there**! 💾🎉

---

## 21.14 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| Creating `preferencesDataStore` inside a class or function | 💥 *There are multiple DataStores active for the same file* | One **top-level** `val Context.xxx by preferencesDataStore(...)` per file name. |
| Two different names for the same data (`"settings"` here, `"Settings"` there) | Two separate files — data "disappears" | Create the DataStore in **one** place (the AppContainer file). |
| Renaming a key's label (`"user_name"` → `"username"`) | Old saved value is lost | Never change a label once the app is published. |
| `ThemeMode.valueOf(saved)` | 💥 Crash if the saved name no longer exists | `entries.find { it.name == saved } ?: default` |
| Reading `preferences[KEY]` without `?:` | It's nullable — red error | Give a default: `?: 0`, `?: ""`, `?: false`. |
| Calling `edit` outside a coroutine | *Suspend function … should be called only from a coroutine* | `viewModelScope.launch { ... }` |
| Counting with a value read **outside** `edit` | Fast taps get lost | Read the current value **inside** `edit { }`. |
| No `catch` on `dataStore.data` | 💥 Crash if the file is broken | `.catch { if (it is IOException) emit(emptyPreferences()) else throw it }` |
| Saving a `List` or a data class | Not supported by Preferences DataStore | Save simple values, or use **Room** (Chapter 22) for lists. |
| Text field reading straight from DataStore | Cursor jumps, letters lost ⌨️😖 | Edit a **local** copy; save on a button (or with a delay). |
| Showing Welcome before settings are loaded | Welcome flashes, then jumps to Home 😬 | A `Loading` state first; decide when `Ready`. |
| Keeping an **Activity** in the AppContainer | 💧 Memory leak | Use the **Application** context. |
| Data is still there after "testing from zero" | The file survives app updates | **Clear storage** or uninstall. |

---

## 21.15 Summary — What You Learned 🎓

✅ `remember`, `rememberSaveable`, `ViewModel`, and `SavedStateHandle` live in **memory** — closing the app wipes them. To **really** remember, save to **storage**. 💾

✅ **Preferences DataStore** = labeled **jars** 🫙: **keys** (`stringPreferencesKey`, `booleanPreferencesKey`, `intPreferencesKey`, …) and **values**. For **small** data. Lists of things → **Room** (next chapter).

✅ Create it **once**, at the top level: `val Context.dataStore by preferencesDataStore(name = "...")`. **One DataStore per file!**

✅ **Read** with `dataStore.data` — a **`Flow`** 🌊. Missing values are `null` → use `?:` defaults. Add `.catch { }` for `IOException`.

✅ **Write** with `dataStore.edit { it[KEY] = value }` — a `suspend` function, **main-safe**, and **atomic** (all changes in one `edit` are saved together). Read-then-write **inside** `edit`.

✅ Save **enums** as their `name`, and read them back **safely** with `entries.find { }`.

✅ **MVVM:** a `SettingsRepository` hides DataStore; the AppContainer creates the DataStore with the **Application** context; the ViewModel turns the Flow into `StateFlow` with `stateIn`.

✅ Show **Loading** until settings are read; decide the **start destination** once; switch the **theme** live with `MySpaceTheme(darkTheme = ...)`.

✅ You built **My Space** 🏠 and gave the **Quiz app** real **best scores** 🏅 that survive everything!

---

## 21.16 Practice Time 🏋️

**Task 1 — Which way? 🤔**
For each, choose: `remember`, `rememberSaveable`, `ViewModel`, **DataStore**, or **Room**:
a) Is a dropdown menu open right now?
b) The text the user is typing in a search box (should survive rotation).
c) "Notifications on/off" in the app's settings.
d) 500 notes the user wrote.
e) The list of jokes just downloaded from the internet (Chapter 19).
f) The user's chosen language.

**Task 2 — Keys ✍️:**
Write the keys for: a sound volume (`0.0` to `1.0`), the date of the last visit (milliseconds), a nickname, "has rated the app" (yes/no), and a set of favorite colors.

**Task 3 — Font size setting 🔠:**
Add a **"Big text"** switch to My Space's Settings. Save it in DataStore. When it's on, the "Hello, Sam!" text on Home uses `displaySmall` instead of `headlineMedium`.

**Task 4 — Last visit 📅:**
Show "**Last visit: 5 minutes ago**" on the Home screen of My Space. Save the time (with `System.currentTimeMillis()`) every time the app opens — but show the **previous** visit, not this one!
*Hint:* read the old value **before** you save the new one.

**Task 5 — Find the 3 bugs 🐛🐛🐛:**

```kotlin
class SettingsRepository(private val context: Context) {

    private val Context.dataStore by preferencesDataStore(name = "settings")

    private val DARK = booleanPreferencesKey("dark")

    val isDark: Flow<Boolean> = context.dataStore.data.map { it[DARK] }

    fun setDark(value: Boolean) {
        context.dataStore.edit { it[DARK] = value }
    }
}
```

**Task 6 — Quiz: "New best!" 🎉:**
On the Quiz app's **Result** screen, show "**🏅 New best score!**" when the user just beat (or set) their record.
*Hint:* make `saveScore` **return** a `Boolean` (`true` if it was a new best), keep it in the `QuizUiState` as `isNewBest`, and pass it to the Result route as one more argument.

---

### Answers

**Task 1:**

| | Answer | Why |
|---|---|---|
| a) | `remember` (or `rememberSaveable`) | Tiny UI detail; fine to forget. |
| b) | `rememberSaveable` (or a ViewModel + `SavedStateHandle`) | Survives rotation and process death, but not needed after closing the app. |
| c) | **DataStore** 📝 | A small setting that must be remembered forever. |
| d) | **Room** 🗃️ | Lots of items the user created. |
| e) | `ViewModel` | It can be downloaded again; just keep it while the screen is open. (Chapter 22 shows how to cache it in Room for offline use!) |
| f) | **DataStore** 📝 | A small setting. |

**Task 2:**

```kotlin
val VOLUME = floatPreferencesKey("volume")
val LAST_VISIT = longPreferencesKey("last_visit")
val NICKNAME = stringPreferencesKey("nickname")
val HAS_RATED = booleanPreferencesKey("has_rated")
val FAVORITE_COLORS = stringSetPreferencesKey("favorite_colors")
```

💡 Time in milliseconds is a **big** number (over 1.7 **trillion**!) → `Long`, not `Int`.

**Task 3:**

1. `UserSettings`: add `val bigText: Boolean = false`.
2. `SettingsRepository`: add `suspend fun setBigText(enabled: Boolean)`.
3. `DataStoreSettingsRepository`:

```kotlin
// in Keys:
val BIG_TEXT = booleanPreferencesKey("big_text")

// in map { }:
bigText = preferences[Keys.BIG_TEXT] ?: false,

override suspend fun setBigText(enabled: Boolean) {
    dataStore.edit { it[Keys.BIG_TEXT] = enabled }
}
```

4. `MainViewModel`:

```kotlin
fun onBigTextChange(enabled: Boolean) {
    viewModelScope.launch { settingsRepository.setBigText(enabled) }
}
```

5. `SettingsScreen` — new parameters `bigText: Boolean` and `onBigTextChange: (Boolean) -> Unit`, and a row:

```kotlin
Row(verticalAlignment = Alignment.CenterVertically) {
    Text("Big text 🔠", modifier = Modifier.weight(1f))
    Switch(checked = bigText, onCheckedChange = onBigTextChange)
}
```

6. `HomeScreen` — new parameter `bigText: Boolean`:

```kotlin
style = if (bigText) MaterialTheme.typography.displaySmall
        else MaterialTheme.typography.headlineMedium,
```

7. Pass the new values in `MySpaceNavHost`. ✅ Notice how **every layer** got one small change — that's MVVM: each piece has its **own job**. 🏗️

**Task 4:**

In the repository:

```kotlin
// Keys:
val LAST_VISIT = longPreferencesKey("last_visit")
val PREVIOUS_VISIT = longPreferencesKey("previous_visit")

// UserSettings gets: val previousVisit: Long? = null
// map { }:
previousVisit = preferences[Keys.PREVIOUS_VISIT],

override suspend fun recordVisit() {
    dataStore.edit { preferences ->
        val last = preferences[Keys.LAST_VISIT]                 // the old "now" ...
        if (last != null) preferences[Keys.PREVIOUS_VISIT] = last   // ... becomes "previous"
        preferences[Keys.LAST_VISIT] = System.currentTimeMillis()
    }
}
```

Call `recordVisit()` in `MainViewModel`'s `init`, next to `increaseOpenCount()`. On Home:

```kotlin
fun lastVisitText(previousVisit: Long?): String {
    if (previousVisit == null) return "First visit! 🎉"
    val minutes = (System.currentTimeMillis() - previousVisit) / 60_000
    return when {
        minutes < 1 -> "Last visit: just now"
        minutes < 60 -> "Last visit: $minutes minutes ago"
        minutes < 60 * 24 -> "Last visit: ${minutes / 60} hours ago"
        else -> "Last visit: ${minutes / (60 * 24)} days ago"
    }
}
```

💡 Why **two** keys? Because `init` saves "now" **immediately** when the app opens. If we only had one key, the Home screen would always show "just now" 😅. So we move the old value to `PREVIOUS_VISIT` first — all inside **one** `edit`, so it's atomic. ✅

**Task 5:**

| # | Bug | Fix |
|---|---|---|
| 1 | `preferencesDataStore` **inside a class** → a new DataStore for **each** repository object → *multiple DataStores active* 💥 | Move `val Context.dataStore by preferencesDataStore(...)` to the **top level** of a file. |
| 2 | `it[DARK]` is `Boolean?`, but the flow is `Flow<Boolean>` → red error | `it[DARK] ?: false` |
| 3 | `edit` is `suspend`, but `setDark` is a normal `fun` → red error | `suspend fun setDark(value: Boolean)` |

Bonus 🌟: no `.catch { }` for `IOException` on `data`, and keeping a `Context` is only OK if it's the **Application** context.

**Task 6:**

1. `BestScoreRepository`: `suspend fun saveScore(category: QuizCategory, score: Int): Boolean`
2. `DataStoreBestScoreRepository`:

```kotlin
override suspend fun saveScore(category: QuizCategory, score: Int): Boolean {
    var isNewBest = false
    dataStore.edit { preferences ->
        val oldBest = preferences[keyFor(category)] ?: -1
        if (score > oldBest) {
            preferences[keyFor(category)] = score
            isNewBest = true
        }
    }
    return isNewBest
}
```

3. `QuizUiState`: add `val isNewBest: Boolean = false`. In `selectOption`:

```kotlin
viewModelScope.launch {
    val newBest = bestScoreRepository.saveScore(category, finalScore)
    _uiState.update { it.copy(isNewBest = newBest) }
}
```

4. Routes: `data class Result(val categoryName: String, val score: Int, val total: Int, val isNewBest: Boolean)`.
5. `QuizRoute`'s `onFinished` passes `uiState.isNewBest` too, and the NavHost puts it in the `Result` route.
6. `ResultScreen` gets `isNewBest: Boolean` and shows:

```kotlin
if (isNewBest) {
    Text("🏅 New best score!", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.primary)
}
```

💡 `isNewBest` is saved in the **route**, so rotation and process death keep it. And `var isNewBest` inside `edit`'s lambda works because the lambda runs **before** `edit` returns.

---

## 21.17 Challenges 🚀

### Challenge 1: Recipe Book — skip the Welcome screen ⭐⭐
In the **Recipe Book** from **Chapter 13**, the Welcome screen appears **every** time the app opens. Use DataStore to show it **only the first time** — exactly like My Space.

### Challenge 2: Theme color choice 🎨 ⭐⭐
Let the user choose a **color**: 🟢 Green, 🔵 Blue, 🟣 Purple. Save it, and build the `colorScheme` from it in your theme.
*Hint:* add a parameter to `MySpaceTheme`, and use `lightColorScheme(primary = ...)` / `darkColorScheme(primary = ...)` (Chapter 7).

### Challenge 3: Reset the Quiz scores 🗑️ ⭐
Add a "**Reset scores**" button (with an "Are you sure?" dialog) on the Quiz Start screen.

### Challenge 4: Quiz timer, now with a saved setting ⏱️ ⭐⭐⭐
If you did Chapter 18's Challenge 1 (the timer), add a setting to turn the timer **on/off**, and save it in DataStore.

### Challenge 5: Daily streak 🔥 ⭐⭐⭐
Show "**🔥 3-day streak!**" when the user opens the app on several days **in a row**.
*Hint:* save the **day number** (`System.currentTimeMillis() / 86_400_000`) of the last visit and the streak length. Same day → nothing; next day → streak + 1; later → back to 1. (This simple day math uses UTC days — good enough for practice.)

---

## 21.18 What Is Next?

DataStore is perfect for **a few** small values. But what about **many** things — hundreds of **notes**, **recipes**, **contacts**, or **messages**? We need searching, sorting, editing, and deleting. 📚

In **Chapter 22: Saving Lots of Data — Room Database**, you will learn:

- What a **database** is — tables, rows, and columns 🗃️ (like a spreadsheet!)
- **Room**: Android's official database library
- **Entities** (tables), **DAOs** (the questions you ask), and the **Database** class
- A little **SQL** — the language of databases — in simple words 🗣️
- Room + **`Flow`**: the screen updates **by itself** when data changes 🌊🪄
- Adding, editing, and deleting items ✏️🗑️
- Upgrading the **Recipe Book**: a `RoomRecipeRepository` — swapped in by changing **one line** in the AppContainer, just like we promised in Chapter 16! 🔁

**Brilliant work finishing Chapter 21! 🎉 Your apps finally have a real memory! 🧠💾**
