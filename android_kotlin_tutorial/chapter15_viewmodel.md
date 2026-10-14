# Chapter 15: ViewModel — The Screen's Brain 🧠

> **What you will learn in this chapter**
>
> 1. The problem with keeping everything in Composables 😵
> 2. What a **ViewModel** is, and how long it **lives** ⏳
> 3. Adding the ViewModel library
> 4. Your first ViewModel
> 5. **`StateFlow`** — state the UI can watch 👀
> 6. **`UiState`** — one data class for the whole screen 📦
> 7. **Events** — telling the ViewModel what happened (with a **sealed interface**!)
> 8. `collectAsStateWithLifecycle()` — watching safely
> 9. The **Route + Screen** pattern — easy previews 🖼️
> 10. ViewModels and **Navigation** (one per screen, arguments with `SavedStateHandle`)
> 11. Surviving **process death** with `SavedStateHandle` 💾
> 12. The **rules** of ViewModels (what NOT to put inside) ⚠️
> 13. Rebuilding the **Coffee Order** app the professional way ☕
>
> **Time needed:** about 5 hours. This is a **very important** chapter for real apps.

---

## 15.1 The Problem 😵

Look back at the **Coffee Order** app (Chapter 8) and the **Sign-Up form** (Chapter 9). The top Composable had:

- 5–12 `rememberSaveable` lines of **state**
- **calculations** (total price, form validation)
- **logic** (reset the order, check rules, place the order)
- **AND** all the **UI** (Columns, Buttons, Texts…)

All mixed together in **one big function**. 🍝 For a small app that's OK, but as apps grow:

| Problem | Why it hurts |
|---|---|
| 📏 Huge, hard-to-read functions | Logic and UI are tangled like spaghetti |
| 🔄 State lost or awkward | `rememberSaveable` only handles small, simple types |
| 🌐 Where do I load data from the internet? | Not inside a Composable that runs 60 times a second! |
| 🧪 Hard to test | You can't test the logic without drawing the UI |
| 🔁 Lost work on rotation | A download started in a Composable is **restarted** after rotation |

We need a **separate place** for a screen's **data** and **logic**. That place is the **ViewModel**. 🏡

---

## 15.2 What Is a ViewModel? 🧠

A **ViewModel** is a Kotlin class that:

1. **Holds the state** of a screen (the data it shows). 📦
2. **Contains the logic** (what happens when the user taps something). ⚙️
3. **Survives configuration changes** (rotation, dark mode, language…). 🔄✅
4. Knows **nothing** about how the screen **looks**. 🙈

The **Composable** becomes simple: it just **shows** the state and **reports** user actions.

```
┌───────────────────────────┐            ┌───────────────────────────┐
│        ViewModel 🧠        │  state ⬇️   │      Composable UI 🎨      │
│                           │ ─────────▶ │                           │
│  • holds the state        │            │  • shows the state        │
│  • does the logic         │ ◀───────── │  • reports clicks/typing  │
│  • survives rotation      │  events ⬆️  │  • recreated on rotation  │
└───────────────────────────┘            └───────────────────────────┘
```

**Real-life example:** A **restaurant** 🍽️.

| Restaurant | App |
|---|---|
| The **kitchen** 👨‍🍳 — keeps the food, does the cooking, follows the recipes | **ViewModel** — keeps the state, does the logic |
| The **dining room** 🪑 — shows the food nicely, takes orders | **Composable UI** — shows the state, takes clicks |
| Repainting the dining room 🎨 doesn't throw away the food in the kitchen | **Rotation** recreates the UI, but the ViewModel (and its state) **stays** |

> 💡 This is called **separation of concerns**: each part has **one job**. It's the most important idea in app architecture. 🏗️

### How long does a ViewModel live? ⏳

```
Activity:   created ── rotate ──▶ destroyed + created ── rotate ──▶ destroyed + created ── finished ──▶ gone
                         🔄                               🔄                                   🏁
ViewModel:  created ─────────────────────────────────────────────────────────────────────────▶ cleared 🧹
            (one ViewModel the whole time!)
```

| Event | The ViewModel… |
|---|---|
| Rotation / dark mode / language 🔄 | **Survives** ✅ — the **same** object is given to the new screen |
| Press Home 🏠 and come back | **Survives** ✅ |
| Leave the screen for good (Back, or `popBackStack`) | Is **cleared** 🧹 (`onCleared()` is called) |
| **Process death** 💀 | **Lost** ❌ — unless you use `SavedStateHandle` (15.11) |

**Real-life example:** A **backpack** 🎒 you carry from room to room. When a room is **repainted** (rotation), you still have your backpack. When you **leave the building** (finish the screen), you put the backpack away.

---

## 15.3 Step 1: Add the Libraries 📦

We need **`lifecycle-viewmodel-compose`** (for the `viewModel()` function) and **`lifecycle-runtime-compose`** (for `collectAsStateWithLifecycle()`, from Chapter 14).

### `gradle/libs.versions.toml`

Under `[libraries]` (the version `lifecycleRuntimeKtx` already exists in new projects):

```toml
androidx-lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycleRuntimeKtx" }
androidx-lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycleRuntimeKtx" }
```

(If you already added `lifecycle-runtime-compose` in Chapter 14, don't add it twice.)

### `build.gradle.kts (Module :app)`

```kotlin
dependencies {
    // ... existing lines ...
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)
}
```

Click **Sync Now**. 🔄 ✅

> ℹ️ All lifecycle libraries should use the **same version** — that's why we use `version.ref = "lifecycleRuntimeKtx"` for both.

---

## 15.4 Your First ViewModel 👶

Let's make a counter **with a ViewModel**. Make a new file **`CounterViewModel.kt`**:

```kotlin
package com.example.myfirstapp

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel

class CounterViewModel : ViewModel() {

    var count by mutableIntStateOf(0)
        private set

    fun increase() {
        count++
    }

    fun reset() {
        count = 0
    }
}
```

### Every bit explained

| Code | Meaning |
|---|---|
| `class CounterViewModel : ViewModel()` | Our class **is a kind of** `ViewModel` (inheritance, Chapter 4). It gets the "survive rotation" power. 🦸 |
| `var count by mutableIntStateOf(0)` | The state — a Compose state box (Chapter 8). **No `remember`** needed: the ViewModel **itself** is what's remembered. |
| `private set` | ⭐ **Important!** Anyone can **read** `count`, but only the ViewModel can **change** it. 🔒 |
| `fun increase()` / `fun reset()` | The **logic**. The UI calls these. |

**Why `private set`?** 🤔
Without it, any Composable could write `viewModel.count = 9999`. With it, the **only** way to change the count is through `increase()` or `reset()`. The ViewModel is **in control** — like a bank 🏦: you can see your balance, but you can't just write a new number; you must use **deposit** or **withdraw** (Chapter 3's `private`!).

### Using it in a Composable

```kotlin
@Composable
fun CounterScreen(viewModel: CounterViewModel = viewModel()) {
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("${viewModel.count}", style = MaterialTheme.typography.displayLarge)
        Button(onClick = { viewModel.increase() }) { Text("+1") }
        TextButton(onClick = { viewModel.reset() }) { Text("Reset") }
    }
}
```

Import: `androidx.lifecycle.viewmodel.compose.viewModel`

| Code | Meaning |
|---|---|
| `viewModel: CounterViewModel = viewModel()` | **Get** the ViewModel. The first time, it's **created**. After rotation, you get the **same one** back! 🎁 |
| `viewModel.count` | Read the state. Because it's a Compose state, the screen **recomposes** when it changes. ✨ |
| `viewModel.increase()` | Tell the ViewModel what happened (an **event** ⬆️). |

**Run it** → tap +1 a few times → **rotate** 🔄 → the number is **still there**! No `rememberSaveable` needed. 🎉

> ⚠️ **Never** create a ViewModel yourself with `CounterViewModel()`. That makes a **new** one every recomposition, and it **won't** survive rotation. Always use **`viewModel()`**. Android keeps track of it for you. 🗂️

---

## 15.5 `StateFlow` — The Standard Way to Share State 🌊

Using `mutableIntStateOf` inside a ViewModel **works** (and it's fine for simple cases!). But most professional Android apps use **`StateFlow`**. Why?

- It's **pure Kotlin** — it doesn't depend on Compose. The ViewModel stays **independent** of the UI. 🧱
- It works great with **coroutines** (Chapter 18) — for loading data from the internet and databases.
- Room (Chapter 22) and many libraries give you **Flows** directly.

### What is a `StateFlow`?

A **`StateFlow`** is a box that:
1. **Always** has a current value (`.value`).
2. **Tells** everyone watching when the value **changes**. 📢

It's very similar to `mutableStateOf` — but from the Kotlin coroutines library.

**Real-life example:** A **live scoreboard** 🏟️. It always shows the current score, and everyone watching sees it update immediately.

### The pattern: private `MutableStateFlow`, public `StateFlow` 🔒

```kotlin
class CounterViewModel : ViewModel() {

    private val _count = MutableStateFlow(0)
    val count: StateFlow<Int> = _count.asStateFlow()

    fun increase() {
        _count.value++
    }

    fun reset() {
        _count.value = 0
    }
}
```

Imports:

```kotlin
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
```

| Code | Meaning |
|---|---|
| `private val _count = MutableStateFlow(0)` | A **changeable** flow, starting at 0. `private` → only the ViewModel can change it. The `_` (underscore) at the start is a custom: "*this is the private, changeable one*". |
| `val count: StateFlow<Int> = _count.asStateFlow()` | A **read-only** view of the same flow, for the UI. 👀 The UI can **watch** but not **change**. |
| `_count.value++` | Change the value → everyone watching is told. 📢 |

**Real-life example:** A **TV studio** 📺. Only the studio (`_count`, private) can change what's broadcast. Viewers at home (`count`, public) can only **watch**.

> 💡 This "**private `_x` + public `x`**" pattern is called a **backing property**. You'll see it in **almost every** Android project! 🌟

### Watching a StateFlow in Compose

```kotlin
@Composable
fun CounterScreen(viewModel: CounterViewModel = viewModel()) {
    val count by viewModel.count.collectAsStateWithLifecycle()

    Text("$count")
    ...
}
```

Import: `androidx.lifecycle.compose.collectAsStateWithLifecycle`

| Code | Meaning |
|---|---|
| `.collectAsStateWithLifecycle()` | Turn the `StateFlow` into Compose **state** → the screen **recomposes** when it changes. |
| `by` | Same `by` as Chapter 8 → use `count` like a normal `Int`. |
| `WithLifecycle` | ⭐ It **stops** watching when the app goes to the **background** (`onStop`, Chapter 14), and **starts** again when it comes back. Saves battery! 🔋 |

> ℹ️ There's also `collectAsState()` (without "WithLifecycle"). It keeps watching even in the background. On Android, **prefer `collectAsStateWithLifecycle()`**.

---

## 15.6 `UiState` — One Data Class for the Whole Screen 📦

A real screen has **many** pieces of state. Instead of 10 separate flows, we put them **all** in **one data class**:

```kotlin
data class ProfileUiState(
    val name: String = "",
    val age: String = "",
    val isPremium: Boolean = false,
    val isSaving: Boolean = false,
    val errorMessage: String? = null
)
```

- **One** object describes **everything** the screen shows. 📸
- **Default values** (Chapter 2) → `ProfileUiState()` is the **starting** state.
- All properties are **`val`** → we **never** change it; we make a **new copy** (Chapter 8: immutable state).

**Real-life example:** A **photograph** 📸 of the screen. To change the screen, you don't draw on the old photo — you take a **new** photo.

### Updating it with `update { it.copy(...) }` ⭐

```kotlin
class ProfileViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(ProfileUiState())
    val uiState: StateFlow<ProfileUiState> = _uiState.asStateFlow()

    fun onNameChange(newName: String) {
        _uiState.update { it.copy(name = newName) }
    }

    fun onPremiumToggle() {
        _uiState.update { it.copy(isPremium = !it.isPremium) }
    }
}
```

Import: `kotlinx.coroutines.flow.update`

| Code | Meaning |
|---|---|
| `_uiState.update { ... }` | "Take the **current** state, and replace it with what the lambda gives back." |
| `it` | The **current** `ProfileUiState`. |
| `it.copy(name = newName)` | A **new** state, same as before, but with the new name (Chapter 3: `copy`). |

> 💡 **Why `update { }` instead of `_uiState.value = _uiState.value.copy(...)`?** Both work, but `update` is **safe** even if two changes happen at the **same time** (from different coroutines — Chapter 18). Always use `update`. ✅

### Calculated values inside the UiState ✨

Values that can be **calculated** (Chapter 8's golden rule!) can be **properties** of the data class:

```kotlin
data class CartUiState(
    val items: List<CartItem> = emptyList(),
    val discountPercent: Int = 0
) {
    val subtotal: Double get() = items.sumOf { it.price * it.quantity }
    val total: Double get() = subtotal * (100 - discountPercent) / 100
    val isEmpty: Boolean get() = items.isEmpty()
}
```

- `val subtotal: Double get() = ...` → a property that is **calculated every time** you read it (Chapter 4: `get()`).
- It's **not** in the `( )`, so it's **not** stored and **not** part of `copy`. It's always **correct**. ✅
- The UI just reads `uiState.total` — no math in the UI! 🎉

---

## 15.7 Events — Telling the ViewModel What Happened ⬆️

### Way 1: One function per event (simple)

```kotlin
viewModel.onNameChange("Roy")
viewModel.onPremiumToggle()
viewModel.onSaveClick()
```

Clear and simple. ✅ Function names usually start with **`on`**: "*on name change*", "*on save click*".

### Way 2: A sealed interface of events (tidy for big screens) ⭐

When a screen has **many** events, passing many lambdas to the UI gets long. Instead, describe **all** events with a **sealed interface** (Chapter 4!):

```kotlin
sealed interface ProfileEvent {
    data class NameChanged(val name: String) : ProfileEvent
    data class AgeChanged(val age: String) : ProfileEvent
    data object PremiumToggled : ProfileEvent
    data object SaveClicked : ProfileEvent
}
```

And **one** function in the ViewModel handles them all:

```kotlin
fun onEvent(event: ProfileEvent) {
    when (event) {
        is ProfileEvent.NameChanged -> _uiState.update { it.copy(name = event.name) }
        is ProfileEvent.AgeChanged -> _uiState.update { it.copy(age = event.age) }
        ProfileEvent.PremiumToggled -> _uiState.update { it.copy(isPremium = !it.isPremium) }
        ProfileEvent.SaveClicked -> save()
    }
}
```

- The UI gets **one** lambda: `onEvent: (ProfileEvent) -> Unit`. 🎯
- `when` covers **every** event — if you add a new one and forget it, Kotlin shows an **error**. 🛡️

**Real-life example:** Instead of a **separate phone number** for every department 📞📞📞, a company has **one** number and you say "*I want sales*" or "*I want support*". ☎️

> 💡 Both ways are used in real projects. Use **Way 1** for small screens; **Way 2** when there are many events.

### The full one-way data flow 🔁

```
          ┌─────────────────────────────────────────┐
          │              ViewModel 🧠                │
          │                                         │
          │   _uiState ──▶ uiState (StateFlow)       │
          │       ▲              │                  │
          │       │ update{}     │                  │
          │   onEvent(event)     │                  │
          └───────▲──────────────┼──────────────────┘
                  │              │
       EVENTS ⬆️  │              │  STATE ⬇️
   (NameChanged,  │              │  collectAsStateWithLifecycle()
    SaveClicked…) │              ▼
          ┌───────┴─────────────────────────────────┐
          │           Composable UI 🎨               │
          │   shows uiState · calls onEvent(...)     │
          └─────────────────────────────────────────┘
```

This is **"state down, events up"** (Chapter 8) — now with a ViewModel at the top. It's called **UDF: Unidirectional Data Flow**. Google recommends it for **all** Android apps. 🌟

---

## 15.8 The Route + Screen Pattern 🖼️

There's a problem with this:

```kotlin
@Composable
fun ProfileScreen(viewModel: ProfileViewModel = viewModel()) { ... }

@Preview
@Composable
fun ProfileScreenPreview() {
    ProfileScreen()   // 😕 makes a real ViewModel… hard to control what it shows
}
```

**The solution:** split into **two** Composables:

```kotlin
// 1. The ROUTE: connects the ViewModel to the screen. Small. No UI.
@Composable
fun ProfileRoute(viewModel: ProfileViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    ProfileScreen(
        uiState = uiState,
        onEvent = viewModel::onEvent
    )
}

// 2. The SCREEN: only UI. Gets everything as inputs. Easy to preview! ✅
@Composable
fun ProfileScreen(
    uiState: ProfileUiState,
    onEvent: (ProfileEvent) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.padding(16.dp)) {
        OutlinedTextField(
            value = uiState.name,
            onValueChange = { onEvent(ProfileEvent.NameChanged(it)) },
            label = { Text("Name") }
        )
        ...
    }
}

// 3. PREVIEW with any state you like 🎨
@Preview(showBackground = true)
@Composable
fun ProfileScreenPreview() {
    ProfileScreen(
        uiState = ProfileUiState(name = "Roy", age = "10", isPremium = true),
        onEvent = {}
    )
}
```

### New syntax: `viewModel::onEvent` 🔗

```kotlin
onEvent = viewModel::onEvent
```

- `::` makes a **function reference** — "*use this function as a lambda*".
- It's the same as `onEvent = { event -> viewModel.onEvent(event) }`, just shorter. ✂️

| Composable | Knows about the ViewModel? | Previewable? | Job |
|---|---|---|---|
| `ProfileRoute` | ✅ Yes | ❌ | Connect: get state, pass events |
| `ProfileScreen` | ❌ No | ✅ Yes | Draw the UI |

> 💡 This is the **same idea** as Chapter 13's rule "*don't pass the NavController into screens*" — **screens** should only get **data and lambdas**. 🧼

---

## 15.9 ViewModels and Navigation 🧭

### One ViewModel per screen

When you call `viewModel()` **inside** a `composable<Route> { }` in a NavHost, the ViewModel belongs to **that screen's back stack entry** (its "plate" 🍽️, Chapter 13):

```kotlin
NavHost(navController, startDestination = RecipeList) {
    composable<RecipeList> {
        RecipeListRoute()            // gets its own RecipeListViewModel
    }
    composable<RecipeDetail> {
        RecipeDetailRoute(onBack = { navController.navigateUp() })   // gets its own RecipeDetailViewModel
    }
}
```

| Event | ViewModel of that screen |
|---|---|
| You **go to** another screen (the plate stays in the stack) | **Kept** ✅ |
| You **come back** to it | The **same** ViewModel — state is still there ✅ |
| The screen is **popped** (Back) | **Cleared** 🧹 |
| You open the **same** route again later | A **new** ViewModel |

Each screen has its **own brain**. 🧠🧠🧠

### Getting navigation arguments in the ViewModel: `SavedStateHandle` 📦

The details screen needs the **recipe id** from the route. The ViewModel can get it **directly**:

```kotlin
class RecipeDetailViewModel(
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val recipeId: Int = savedStateHandle.toRoute<RecipeDetail>().recipeId

    val recipe: Recipe? = RecipeData.findById(recipeId)
}
```

Imports:

```kotlin
import androidx.lifecycle.SavedStateHandle
import androidx.navigation.toRoute
```

| Code | Meaning |
|---|---|
| `(savedStateHandle: SavedStateHandle)` | The ViewModel **asks** for a `SavedStateHandle` in its constructor. `viewModel()` **gives it automatically**. 🎁 |
| `savedStateHandle.toRoute<RecipeDetail>()` | Read the **route object** — same `toRoute` as Chapter 13! — with the `recipeId` inside. |

Now the Route doesn't need to pass the id at all:

```kotlin
composable<RecipeDetail> {
    RecipeDetailRoute(onBack = { navController.navigateUp() })
}
```

✨ Clean!

### Sharing one ViewModel between screens

Sometimes two screens need the **same** data (like favorites in the Recipe Book). Options:

1. **Pass it down** from a parent: create it **above** the NavHost with `viewModel()` and pass its state/events to the screens.
2. Better, for real apps: keep the shared data in a **repository** (Chapter 16) that **both** ViewModels use. 🏪

We'll see option 2 in **Chapter 16**.

---

## 15.10 Rules of the ViewModel ⚠️

### ❌ Rule 1: Never keep a `Context`, Activity, or View in a ViewModel

```kotlin
class BadViewModel(private val activity: Activity) : ViewModel()   // ❌❌❌
```

**Why?** The ViewModel **lives longer** than the Activity (it survives rotation). After rotation, the **old** Activity is destroyed — but the ViewModel still **holds** it, so it can't be cleaned from memory. This is a **memory leak** 💧 — the app slowly uses more and more memory until it crashes. 💥

**Real-life example:** Keeping the **key** of a house that was **demolished** 🏚️🔑. Useless, and it fills your pocket.

> ℹ️ If you **really** need app-level things (like files), there's `AndroidViewModel(application)`, which holds the **Application** (it lives as long as the app, so it's safe). Later, **Hilt** (Chapter 23) will give us a cleaner way.

### ❌ Rule 2: No Compose UI in the ViewModel

- No `@Composable` functions, no `Color`, no `Modifier`, no `Text` in a ViewModel.
- The ViewModel gives **data** (`isError = true`); the **UI** decides **how** to show it (red color). 🎨

### ❌ Rule 3: No Toasts, no navigation directly from the ViewModel

- The ViewModel doesn't know about the screen. It can't call `navController.navigate(...)` or `Toast.makeText(...)`.
- Instead, put something in the **UiState** (like `orderPlaced = true` or `message = "Saved!"`), and let the **UI** react. ✅

### ✅ Rule 4: Expose **read-only** state

- `private val _uiState = MutableStateFlow(...)` + `val uiState = _uiState.asStateFlow()`
- Or `var x by mutableStateOf(...)` with **`private set`**.

### ✅ Rule 5: Clean up in `onCleared()` (if needed)

```kotlin
override fun onCleared() {
    super.onCleared()
    Log.d("VM", "🧹 ViewModel cleared — goodbye!")
}
```

Called once, when the ViewModel is thrown away for good. Most ViewModels don't need it — **`viewModelScope`** (Chapter 18) cleans up coroutines automatically. 🧹

---

## 15.11 Surviving Process Death With `SavedStateHandle` 💾

Remember Chapter 14's table: a ViewModel survives **rotation** ✅ but **not** process death ❌.

For **small**, important values (what the user typed, selections), use the ViewModel's **`SavedStateHandle`** — it's saved in the same **Bundle** as `rememberSaveable` (Chapter 14: "the note" 📝).

```kotlin
class NoteEditorViewModel(
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    val text: StateFlow<String> = savedStateHandle.getStateFlow("text", "")

    fun onTextChange(newText: String) {
        savedStateHandle["text"] = newText
    }
}
```

| Code | Meaning |
|---|---|
| `savedStateHandle.getStateFlow("text", "")` | A `StateFlow` that reads the saved value with the key `"text"`. If nothing is saved yet → `""`. |
| `savedStateHandle["text"] = newText` | **Save** a new value. The `StateFlow` above updates **automatically**. ✨ |

Now the text survives **rotation** ✅ **and** process death ✅.

> 💡 `SavedStateHandle` is a **Map** (Chapter 3) of keys → values. The same rules as Chapter 14: only **small, simple** values (numbers, Strings, Booleans, enums as names…). 🎒

### Updated survival table

| Where | Rotation 🔄 | Process death 💀 |
|---|---|---|
| `remember` | ❌ | ❌ |
| `rememberSaveable` | ✅ | ✅ |
| ViewModel (normal property) | ✅ | ❌ |
| ViewModel + `SavedStateHandle` | ✅ | ✅ |
| Database / DataStore | ✅ | ✅ |

---

## 15.12 Build It: Coffee Order — The Professional Way ☕🏗️

Let's rebuild the **Coffee Order** app from Chapter 8 with:

- ✅ A **ViewModel** holding all logic
- ✅ A **UiState** data class with **calculated** prices
- ✅ **Events** as a **sealed interface**
- ✅ **`SavedStateHandle`** so the order survives **process death**
- ✅ The **Route + Screen** pattern with **previews**

The screen looks **exactly** like Chapter 8. Only the **inside** changes. 🔧

### File 1: `CoffeeOrderState.kt` — data, state, events

```kotlin
package com.example.myfirstapp

enum class CoffeeSize(val label: String, val price: Double) {
    SMALL("Small", 2.50),
    MEDIUM("Medium", 3.50),
    LARGE("Large", 4.50)
}

const val SUGAR_PRICE = 0.25
const val CREAM_PRICE = 0.75
const val MIN_CUPS = 1
const val MAX_CUPS = 10

data class CoffeeUiState(
    val size: CoffeeSize = CoffeeSize.MEDIUM,
    val cups: Int = 1,
    val sugar: Boolean = false,
    val cream: Boolean = false,
    val orderPlaced: Boolean = false
) {
    val pricePerCup: Double
        get() = size.price + (if (sugar) SUGAR_PRICE else 0.0) + (if (cream) CREAM_PRICE else 0.0)

    val total: Double
        get() = pricePerCup * cups

    val canDecrease: Boolean
        get() = cups > MIN_CUPS && !orderPlaced

    val canIncrease: Boolean
        get() = cups < MAX_CUPS && !orderPlaced

    val extrasText: String
        get() {
            val extras = buildList {
                if (sugar) add("sugar")
                if (cream) add("cream")
            }
            return if (extras.isEmpty()) "no extras" else extras.joinToString(" and ")
        }
}

sealed interface CoffeeEvent {
    data class SizeSelected(val size: CoffeeSize) : CoffeeEvent
    data object IncreaseCups : CoffeeEvent
    data object DecreaseCups : CoffeeEvent
    data class SugarChanged(val checked: Boolean) : CoffeeEvent
    data class CreamChanged(val checked: Boolean) : CoffeeEvent
    data object PlaceOrder : CoffeeEvent
    data object NewOrder : CoffeeEvent
}
```

### File 2: `CoffeeOrderViewModel.kt` — the brain 🧠

```kotlin
package com.example.myfirstapp

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

class CoffeeOrderViewModel(
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _uiState = MutableStateFlow(restoreState())
    val uiState: StateFlow<CoffeeUiState> = _uiState.asStateFlow()

    fun onEvent(event: CoffeeEvent) {
        when (event) {
            is CoffeeEvent.SizeSelected -> updateState { it.copy(size = event.size) }
            CoffeeEvent.IncreaseCups -> updateState { it.copy(cups = (it.cups + 1).coerceAtMost(MAX_CUPS)) }
            CoffeeEvent.DecreaseCups -> updateState { it.copy(cups = (it.cups - 1).coerceAtLeast(MIN_CUPS)) }
            is CoffeeEvent.SugarChanged -> updateState { it.copy(sugar = event.checked) }
            is CoffeeEvent.CreamChanged -> updateState { it.copy(cream = event.checked) }
            CoffeeEvent.PlaceOrder -> updateState { it.copy(orderPlaced = true) }
            CoffeeEvent.NewOrder -> updateState { CoffeeUiState() }
        }
    }

    // Change the state AND save it, in one place.
    private fun updateState(change: (CoffeeUiState) -> CoffeeUiState) {
        _uiState.update(change)
        saveState(_uiState.value)
    }

    private fun saveState(state: CoffeeUiState) {
        savedStateHandle[KEY_SIZE] = state.size.name
        savedStateHandle[KEY_CUPS] = state.cups
        savedStateHandle[KEY_SUGAR] = state.sugar
        savedStateHandle[KEY_CREAM] = state.cream
        savedStateHandle[KEY_PLACED] = state.orderPlaced
    }

    private fun restoreState(): CoffeeUiState {
        val default = CoffeeUiState()
        return CoffeeUiState(
            size = savedStateHandle.get<String>(KEY_SIZE)?.let { CoffeeSize.valueOf(it) } ?: default.size,
            cups = savedStateHandle[KEY_CUPS] ?: default.cups,
            sugar = savedStateHandle[KEY_SUGAR] ?: default.sugar,
            cream = savedStateHandle[KEY_CREAM] ?: default.cream,
            orderPlaced = savedStateHandle[KEY_PLACED] ?: default.orderPlaced
        )
    }

    private companion object {
        const val KEY_SIZE = "size"
        const val KEY_CUPS = "cups"
        const val KEY_SUGAR = "sugar"
        const val KEY_CREAM = "cream"
        const val KEY_PLACED = "placed"
    }
}
```

### File 3: `MainActivity.kt` — Route + Screen

```kotlin
package com.example.myfirstapp

import android.content.res.Configuration
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.selection.toggleable
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.myfirstapp.ui.theme.MyFirstAppTheme
import java.text.NumberFormat

fun Double.toMoney(): String = NumberFormat.getCurrencyInstance().format(this)

// ---------- Activity ----------

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyFirstAppTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    CoffeeOrderRoute(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

// ---------- Route: connects ViewModel ↔ Screen ----------

@Composable
fun CoffeeOrderRoute(
    modifier: Modifier = Modifier,
    viewModel: CoffeeOrderViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    CoffeeOrderScreen(
        uiState = uiState,
        onEvent = viewModel::onEvent,
        modifier = modifier
    )
}

// ---------- Screen: only UI ----------

@Composable
fun CoffeeOrderScreen(
    uiState: CoffeeUiState,
    onEvent: (CoffeeEvent) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("☕ Coffee Order", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)

        SectionTitle("Choose your size")
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            CoffeeSize.entries.forEach { size ->
                val buttonModifier = Modifier.weight(1f)
                if (size == uiState.size) {
                    Button(
                        onClick = { onEvent(CoffeeEvent.SizeSelected(size)) },
                        enabled = !uiState.orderPlaced,
                        modifier = buttonModifier
                    ) { Text(size.label) }
                } else {
                    OutlinedButton(
                        onClick = { onEvent(CoffeeEvent.SizeSelected(size)) },
                        enabled = !uiState.orderPlaced,
                        modifier = buttonModifier
                    ) { Text(size.label) }
                }
            }
        }

        SectionTitle("Cups")
        Row(
            modifier = Modifier.align(Alignment.CenterHorizontally),
            verticalAlignment = Alignment.CenterVertically
        ) {
            FilledTonalButton(
                onClick = { onEvent(CoffeeEvent.DecreaseCups) },
                enabled = uiState.canDecrease
            ) { Text("−", style = MaterialTheme.typography.titleLarge) }
            Text(
                text = "${uiState.cups}",
                style = MaterialTheme.typography.headlineMedium,
                modifier = Modifier.padding(horizontal = 24.dp)
            )
            FilledTonalButton(
                onClick = { onEvent(CoffeeEvent.IncreaseCups) },
                enabled = uiState.canIncrease
            ) { Text("+", style = MaterialTheme.typography.titleLarge) }
        }

        SectionTitle("Extras")
        ExtraRow(
            label = "Extra sugar 🍬 (+${SUGAR_PRICE.toMoney()})",
            checked = uiState.sugar,
            enabled = !uiState.orderPlaced,
            onCheckedChange = { onEvent(CoffeeEvent.SugarChanged(it)) }
        )
        ExtraRow(
            label = "Whipped cream 🍦 (+${CREAM_PRICE.toMoney()})",
            checked = uiState.cream,
            enabled = !uiState.orderPlaced,
            onCheckedChange = { onEvent(CoffeeEvent.CreamChanged(it)) }
        )

        HorizontalDivider()

        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Total", style = MaterialTheme.typography.titleLarge)
            Spacer(modifier = Modifier.weight(1f))
            Text(
                text = uiState.total.toMoney(),
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
        }

        if (uiState.orderPlaced) {
            OrderSummaryCard(uiState = uiState, onNewOrder = { onEvent(CoffeeEvent.NewOrder) })
        } else {
            Button(
                onClick = { onEvent(CoffeeEvent.PlaceOrder) },
                modifier = Modifier.fillMaxWidth()
            ) { Text("Place order") }
        }
    }
}

@Composable
fun SectionTitle(text: String) {
    Text(text, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
}

@Composable
fun ExtraRow(
    label: String,
    checked: Boolean,
    enabled: Boolean,
    onCheckedChange: (Boolean) -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .toggleable(value = checked, enabled = enabled, onValueChange = onCheckedChange, role = Role.Switch),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(label, style = MaterialTheme.typography.bodyLarge, modifier = Modifier.weight(1f))
        Switch(checked = checked, onCheckedChange = null, enabled = enabled)
    }
}

@Composable
fun OrderSummaryCard(uiState: CoffeeUiState, onNewOrder: () -> Unit) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text("✅ Order placed!", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            Text("${uiState.cups} × ${uiState.size.label} coffee, ${uiState.extrasText}")
            Text("You paid ${uiState.total.toMoney()}")
            TextButton(onClick = onNewOrder, modifier = Modifier.align(Alignment.End)) {
                Text("New order")
            }
        }
    }
}

// ---------- Previews: any state, no ViewModel needed! ----------

@Preview(name = "Empty order", showSystemUi = true)
@Composable
fun CoffeeEmptyPreview() {
    MyFirstAppTheme {
        Surface { CoffeeOrderScreen(uiState = CoffeeUiState(), onEvent = {}) }
    }
}

@Preview(name = "Placed order", showSystemUi = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun CoffeePlacedPreview() {
    MyFirstAppTheme {
        Surface {
            CoffeeOrderScreen(
                uiState = CoffeeUiState(
                    size = CoffeeSize.LARGE,
                    cups = 3,
                    sugar = true,
                    cream = true,
                    orderPlaced = true
                ),
                onEvent = {}
            )
        }
    }
}
```

> ⚠️ Keep **your own** package and theme names. If you still have the Chapter 8 code in the same project, **delete** the old Coffee functions first, or you'll get "conflicting declarations" errors (two things with the same name).

### Every important part explained

#### Part 1: `CoffeeUiState` — the photo 📸 with calculated values

```kotlin
data class CoffeeUiState(
    val size: CoffeeSize = CoffeeSize.MEDIUM,
    val cups: Int = 1,
    ...
) {
    val total: Double
        get() = pricePerCup * cups

    val canDecrease: Boolean
        get() = cups > MIN_CUPS && !orderPlaced
    ...
}
```

- **5 stored** values (in the `( )`).
- **5 calculated** values (`get()`): `pricePerCup`, `total`, `canDecrease`, `canIncrease`, `extrasText`.
- The UI just **reads** them: `uiState.total`, `uiState.canDecrease`. **No logic in the UI!** 🎉
- Compare with Chapter 8, where the Composable did all this math itself. 🍝➡️🍱

#### Part 2: `CoffeeEvent` — every user action

```kotlin
sealed interface CoffeeEvent {
    data class SizeSelected(val size: CoffeeSize) : CoffeeEvent
    data object IncreaseCups : CoffeeEvent
    ...
}
```

- Events **with** data → `data class` (`SizeSelected` needs to know **which** size).
- Events **without** data → `data object` (`IncreaseCups` is just "+1").
- Reading this list, you know **everything** the user can do on this screen. 📋

#### Part 3: `onEvent` — one door for all actions 🚪

```kotlin
    fun onEvent(event: CoffeeEvent) {
        when (event) {
            is CoffeeEvent.SizeSelected -> updateState { it.copy(size = event.size) }
            CoffeeEvent.IncreaseCups -> updateState { it.copy(cups = (it.cups + 1).coerceAtMost(MAX_CUPS)) }
            ...
            CoffeeEvent.NewOrder -> updateState { CoffeeUiState() }
        }
    }
```

| Code | Meaning |
|---|---|
| `is CoffeeEvent.SizeSelected ->` | A data class → use `is` → smart cast → `event.size` works (Chapter 4). |
| `CoffeeEvent.IncreaseCups ->` | A data object → compare directly. |
| `.coerceAtMost(MAX_CUPS)` | Never more than 10 — even if the button is tapped very fast. 🛡️ The **rules** live in the ViewModel. |
| `updateState { CoffeeUiState() }` | A **brand-new**, default state → reset everything in **one** line! ✨ |

#### Part 4: `updateState` — change **and** save

```kotlin
    private fun updateState(change: (CoffeeUiState) -> CoffeeUiState) {
        _uiState.update(change)
        saveState(_uiState.value)
    }
```

- A **helper** that takes a **lambda** (Chapter 3: a function as input). 🧩
- Every change goes through **here** → we **never forget** to save. ✅
- `_uiState.update(change)` → we pass our lambda straight to `update`.

#### Part 5: Saving and restoring with `SavedStateHandle` 💾

```kotlin
    private fun saveState(state: CoffeeUiState) {
        savedStateHandle[KEY_SIZE] = state.size.name
        savedStateHandle[KEY_CUPS] = state.cups
        ...
    }
```

- We save each value with a **key** (like a Map, Chapter 3).
- `state.size.name` → the enum as **text** (`"LARGE"`) — simple types are safest to save.

```kotlin
    private fun restoreState(): CoffeeUiState {
        val default = CoffeeUiState()
        return CoffeeUiState(
            size = savedStateHandle.get<String>(KEY_SIZE)?.let { CoffeeSize.valueOf(it) } ?: default.size,
            cups = savedStateHandle[KEY_CUPS] ?: default.cups,
            ...
        )
    }
```

| Code | Meaning |
|---|---|
| `savedStateHandle.get<String>(KEY_SIZE)` | Read the saved size text, or `null` if nothing is saved (fresh start). |
| `?.let { CoffeeSize.valueOf(it) }` | Text → enum (Chapter 4: `valueOf`). Only if not null (Chapter 3: `?.let`). |
| `?: default.size` | Nothing saved → use the default (Elvis!). |
| `savedStateHandle[KEY_CUPS] ?: default.cups` | Kotlin **guesses** the type (`Int`) from `cups`. |

- On a **fresh** start: nothing saved → **defaults**.
- After **process death**: values come back from the "note" 📝 → the **same order**! ✨

#### Part 6: `private companion object` — the keys

```kotlin
    private companion object {
        const val KEY_SIZE = "size"
        ...
    }
```

- **Constants** for the keys (Chapter 4: companion object). A typo like `"sise"` can't happen in one place but not the other. 🛡️
- `private` → only this ViewModel uses them.

#### Part 7: The Route — 4 lines of glue 🔌

```kotlin
@Composable
fun CoffeeOrderRoute(
    modifier: Modifier = Modifier,
    viewModel: CoffeeOrderViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    CoffeeOrderScreen(uiState = uiState, onEvent = viewModel::onEvent, modifier = modifier)
}
```

- `viewModel()` → creates the ViewModel **and** gives it a `SavedStateHandle` automatically. 🎁
- `collectAsStateWithLifecycle()` → watches the state safely (stops in the background). 🔋
- `viewModel::onEvent` → a function reference (15.8).

#### Part 8: The Screen — pure UI 🎨

- Gets **one** state object and **one** event lambda. That's it!
- Every button just **sends an event**: `onEvent(CoffeeEvent.IncreaseCups)`.
- When the order is placed, the controls are **disabled** (`enabled = !uiState.orderPlaced`) — so the user can't change a paid order. 💳

#### Part 9: Previews for **any** situation

- `CoffeeUiState()` → an empty order.
- `CoffeeUiState(size = LARGE, cups = 3, ..., orderPlaced = true)` → a placed order, in **dark** mode. 🌙
- No ViewModel, no clicking — just **give a state** and look! 👀

### Run it! ▶️ — the 3 survival tests

| Test | Result |
|---|---|
| Choose Large, 3 cups, sugar → **rotate** 🔄 | ✅ All kept (the ViewModel survived) |
| Same → turn on **dark mode** 🌙 | ✅ All kept |
| Same → press **Home** → `adb shell am kill com.example.myfirstapp` → reopen from Recents 💀 | ✅ All kept (thanks to `SavedStateHandle`!) |

### Before and after 📊

| | Chapter 8 version | Chapter 15 version |
|---|---|---|
| State lives in | The Composable (`rememberSaveable` × 5) | The ViewModel (one `UiState`) |
| Price math lives in | The Composable | `CoffeeUiState` (`get()`) |
| Rules (1–10 cups) live in | Lambdas in the Composable | The ViewModel |
| Screen inputs | 10+ values and lambdas | `uiState` + `onEvent` |
| Previews | Only the default state | **Any** state you want |
| Testable without UI? | ❌ | ✅ (Chapter 27) |

> 🎉 The app looks **the same** to the user, but inside it's **clean, safe, and ready to grow**. That's professional Android development!

### A quick taste of testing 🧪

Because the logic is in a normal class, you can check it **without any UI**:

```kotlin
val vm = CoffeeOrderViewModel(SavedStateHandle())
vm.onEvent(CoffeeEvent.SizeSelected(CoffeeSize.LARGE))
vm.onEvent(CoffeeEvent.IncreaseCups)
vm.onEvent(CoffeeEvent.SugarChanged(true))
println(vm.uiState.value.total)   // (4.50 + 0.25) × 2 = 9.5
```

We'll write real tests like this in **Chapter 27**. ✅

---

## 15.13 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| `val vm = CoffeeOrderViewModel(...)` in a Composable | A new ViewModel every time; lost on rotation | Use `viewModel()`. |
| `viewModel()` is red | Library missing | Add `lifecycle-viewmodel-compose` and Sync. |
| `collectAsStateWithLifecycle` is red | Library missing | Add `lifecycle-runtime-compose`. |
| Public `MutableStateFlow` | The UI can change state directly → messy bugs | `private val _uiState` + `val uiState = _uiState.asStateFlow()`. |
| `var` properties in `UiState` and changing them | Screen doesn't update | Use `val` + `update { it.copy(...) }`. |
| Keeping an `Activity` / `Context` in the ViewModel | 💧 Memory leak | Never. Use `AndroidViewModel` or Hilt (Chapter 23) if needed. |
| Calling `Toast` / `navController` from the ViewModel | Can't — and shouldn't | Put a flag/message in `UiState`; let the UI react. |
| Doing math in the Composable | Logic spread everywhere | Put it in `UiState` (`get()`) or the ViewModel. |
| ViewModel state lost after process death | Normal properties don't survive | Save small values in `SavedStateHandle`. |
| Saving big lists in `SavedStateHandle` | 💥 *TransactionTooLargeException* | Save only ids/small values. |
| Previewing a screen that calls `viewModel()` | Preview fails or shows nothing useful | Use the **Route + Screen** pattern; preview the Screen. |
| Two Coffee files with the same names | *Conflicting declarations* | Delete or rename the old code. |

---

## 15.14 Summary — What You Learned 🎓

✅ A **ViewModel** holds a screen's **state and logic**, survives **configuration changes**, and is **cleared** when the screen is gone.

✅ **Get it with `viewModel()`** — never with a constructor call.

✅ **Expose read-only state:** `private val _uiState = MutableStateFlow(...)` + `val uiState = _uiState.asStateFlow()` (or `mutableStateOf` with `private set`).

✅ **`UiState`** = one immutable data class for the whole screen; **calculated** values with `get()`.

✅ **Update** with `_uiState.update { it.copy(...) }`.

✅ **Events** go up: functions like `onSaveClick()`, or a **sealed interface** + `onEvent(event)`.

✅ **Watch** with `collectAsStateWithLifecycle()`.

✅ **Route + Screen:** the Route connects the ViewModel; the Screen is pure UI and easy to **preview**.

✅ **Navigation:** each screen gets its own ViewModel; read route arguments with `savedStateHandle.toRoute<T>()`.

✅ **`SavedStateHandle`** saves small values through **process death**.

✅ **Rules:** no Context/Activity, no Compose UI, no Toasts/navigation inside the ViewModel.

✅ You rebuilt the **Coffee Order** app the professional way! ☕🏗️

---

## 15.15 Practice Time 🏋️

**Task 1 — Counter ViewModel with StateFlow:**
Make `ScoreViewModel` with a `StateFlow<Int>` score, and functions `addPoint()`, `removePoint()` (not below 0), and `reset()`. Show it with a Route + Screen.

**Task 2 — Light switch UiState:**
Make `data class RoomUiState(val lightOn: Boolean = false, val brightness: Float = 1f)` with a calculated `val description: String` → `"Off 🌑"`, `"Dim 🔅"` (brightness < 0.5), or `"Bright 💡"`. Make a ViewModel with `onToggle()` and `onBrightnessChange(value: Float)`. The slider is **disabled** when the light is off.

**Task 3 — Events as a sealed interface:**
Rewrite Task 1 using `sealed interface ScoreEvent { AddPoint, RemovePoint, Reset }` and one `onEvent` function.

**Task 4 — Survive process death:**
Make `NameViewModel(savedStateHandle)` with a `StateFlow<String>` name using `savedStateHandle.getStateFlow("name", "")`, and `onNameChange(...)`. Show it in a text field. Test with `adb shell am kill`.

**Task 5 — Find the 3 bugs 🐛🐛🐛:**

```kotlin
class TodoViewModel(private val context: Context) : ViewModel() {
    val todos = MutableStateFlow(listOf<String>())

    fun add(text: String) {
        todos.value.toMutableList().add(text)
    }
}
```

---

### Answers

**Task 1:**

```kotlin
class ScoreViewModel : ViewModel() {
    private val _score = MutableStateFlow(0)
    val score: StateFlow<Int> = _score.asStateFlow()

    fun addPoint() = _score.update { it + 1 }
    fun removePoint() = _score.update { (it - 1).coerceAtLeast(0) }
    fun reset() { _score.value = 0 }
}

@Composable
fun ScoreRoute(viewModel: ScoreViewModel = viewModel()) {
    val score by viewModel.score.collectAsStateWithLifecycle()
    ScoreScreen(
        score = score,
        onAdd = viewModel::addPoint,
        onRemove = viewModel::removePoint,
        onReset = viewModel::reset
    )
}

@Composable
fun ScoreScreen(score: Int, onAdd: () -> Unit, onRemove: () -> Unit, onReset: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(12.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("$score", style = MaterialTheme.typography.displayLarge)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = onRemove, enabled = score > 0) { Text("−1") }
            Button(onClick = onAdd) { Text("+1") }
        }
        TextButton(onClick = onReset) { Text("Reset") }
    }
}
```

💡 `fun addPoint() = _score.update { it + 1 }` — a one-line function (Chapter 2).

**Task 2:**

```kotlin
data class RoomUiState(
    val lightOn: Boolean = false,
    val brightness: Float = 1f
) {
    val description: String
        get() = when {
            !lightOn -> "Off 🌑"
            brightness < 0.5f -> "Dim 🔅"
            else -> "Bright 💡"
        }
}

class RoomViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(RoomUiState())
    val uiState: StateFlow<RoomUiState> = _uiState.asStateFlow()

    fun onToggle() = _uiState.update { it.copy(lightOn = !it.lightOn) }
    fun onBrightnessChange(value: Float) = _uiState.update { it.copy(brightness = value) }
}

@Composable
fun RoomRoute(viewModel: RoomViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    RoomScreen(uiState, viewModel::onToggle, viewModel::onBrightnessChange)
}

@Composable
fun RoomScreen(uiState: RoomUiState, onToggle: () -> Unit, onBrightnessChange: (Float) -> Unit) {
    Column(modifier = Modifier.padding(24.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Text(uiState.description, style = MaterialTheme.typography.headlineMedium)
        Switch(checked = uiState.lightOn, onCheckedChange = { onToggle() })
        Slider(
            value = uiState.brightness,
            onValueChange = onBrightnessChange,
            enabled = uiState.lightOn
        )
    }
}
```

**Task 3:**

```kotlin
sealed interface ScoreEvent {
    data object AddPoint : ScoreEvent
    data object RemovePoint : ScoreEvent
    data object Reset : ScoreEvent
}

class ScoreViewModel : ViewModel() {
    private val _score = MutableStateFlow(0)
    val score: StateFlow<Int> = _score.asStateFlow()

    fun onEvent(event: ScoreEvent) {
        when (event) {
            ScoreEvent.AddPoint -> _score.update { it + 1 }
            ScoreEvent.RemovePoint -> _score.update { (it - 1).coerceAtLeast(0) }
            ScoreEvent.Reset -> _score.value = 0
        }
    }
}
```

In the Screen: `Button(onClick = { onEvent(ScoreEvent.AddPoint) }) { ... }`.

**Task 4:**

```kotlin
class NameViewModel(private val savedStateHandle: SavedStateHandle) : ViewModel() {
    val name: StateFlow<String> = savedStateHandle.getStateFlow("name", "")

    fun onNameChange(newName: String) {
        savedStateHandle["name"] = newName
    }
}

@Composable
fun NameRoute(viewModel: NameViewModel = viewModel()) {
    val name by viewModel.name.collectAsStateWithLifecycle()
    OutlinedTextField(
        value = name,
        onValueChange = viewModel::onNameChange,
        label = { Text("Your name") },
        modifier = Modifier.padding(16.dp)
    )
}
```

**Task 5:**

1. 🐛 **Keeps a `Context`** → memory leak. Remove it: `class TodoViewModel : ViewModel()`.
2. 🐛 **Public `MutableStateFlow`** → the UI could change it. Use `private val _todos` + `val todos = _todos.asStateFlow()`.
3. 🐛 **`add` changes a temporary copy**, not the state! `toMutableList()` makes a **new** list, `add` changes **that**, and then it's thrown away. The state **never** changes.

Fixed:

```kotlin
class TodoViewModel : ViewModel() {
    private val _todos = MutableStateFlow(listOf<String>())
    val todos: StateFlow<List<String>> = _todos.asStateFlow()

    fun add(text: String) {
        _todos.update { it + text }
    }
}
```

---

## 15.16 What Is Next?

Our ViewModel now has the **state** and **logic** — but where does the **data** come from? Right now, it's written in the code (`RecipeData`). Real apps get data from the **internet** 🌐 and a **database** 🗄️.

Should the ViewModel talk to the internet **directly**? 🤔 No! In **Chapter 16: Clean App Structure — MVVM**, you will learn:

- The **layers** of a good app: **UI → ViewModel → Repository → Data sources** 🏗️
- What a **Repository** is, and why every app needs one 🏪
- Sharing data between screens through a repository
- **Interfaces** for data sources (Chapter 4 comes back!) — swap fake data for real data easily
- Organizing your project into **packages** (folders) 📁
- Rebuilding the **Recipe Book** with MVVM

**Great job finishing Chapter 15! 🎉 Your screens now have a real brain!**
