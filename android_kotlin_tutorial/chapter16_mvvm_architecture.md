# Chapter 16: Clean App Structure — MVVM and the Repository 🏗️

> **What you will learn in this chapter**
>
> 1. Why apps need **architecture** (a plan for where code goes) 🗺️
> 2. **MVVM** — Model, View, ViewModel
> 3. The **layers** of an app: UI → ViewModel → Repository → Data sources 🏢
> 4. What a **Repository** is, and why every app needs one 🏪
> 5. **Single source of truth** — one place for each piece of data ✅
> 6. Using **interfaces** so you can swap fake data for real data 🔌
> 7. Organizing your project into **packages** (folders) 📁
> 8. Creating objects in one place: an **App Container** and the **Application** class 📦
> 9. Giving a ViewModel what it needs: **ViewModel factories** 🏭
> 10. Turning repository data into screen state: `map` + `stateIn`
> 11. Rebuilding the **Recipe Book** with MVVM 📖
>
> **Time needed:** about 5 hours.
>
> **Good news:** This chapter has **few new Compose things**. It's about **where** to put code. This is what separates a beginner from a professional! 💼

---

## 16.1 Why Do We Need Architecture? 🗺️

Imagine building a **house** 🏠 without a plan:
- The kitchen sink is in the bedroom. 🚰🛏️
- The electric wires go through the bathtub. ⚡🛁
- To fix a lamp, you have to break a wall. 🔨

It **works**… until you need to **change** something. 😱

Apps are the same. Without a plan:
- Code to **download** data is inside a **button**.
- The **same** data is copied in **five** places, and they don't agree. 🤷
- To change from **fake** data to **real** data, you must edit **every** screen.

**Architecture** is the **plan** for where each kind of code lives. 📐

A good architecture makes an app:

| Quality | Meaning |
|---|---|
| 📖 **Easy to read** | You know where to look for things. |
| 🔧 **Easy to change** | Change one part without breaking others. |
| 🧪 **Easy to test** | Test each part alone. |
| 👥 **Easy to share** | Many developers can work at the same time. |
| 📈 **Easy to grow** | Adding screen #50 is as easy as screen #2. |

---

## 16.2 MVVM — Model, View, ViewModel 🧩

**MVVM** is the architecture **Google recommends** for Android apps. It has 3 parts:

| Part | What it is | In our apps |
|---|---|---|
| **M**odel | The **data** and where it comes from (internet, database…) | Data classes + **Repository** |
| **V**iew | What the user **sees** | **Composables** 🎨 |
| **V**iew**M**odel | The **bridge**: gets data from the Model, prepares it for the View, handles events | **ViewModel** 🧠 (Chapter 15) |

```
   ┌───────────────┐    state ⬇️     ┌───────────────┐   asks for data ⬇️   ┌───────────────┐
   │   View 🎨      │ ◀──────────── │  ViewModel 🧠  │ ──────────────────▶ │   Model 📦     │
   │ (Composables) │ ─────────────▶ │               │ ◀────────────────── │ (Repository)  │
   └───────────────┘   events ⬆️     └───────────────┘     data ⬆️          └───────────────┘
```

**Real-life example:** A **restaurant** (again! 🍽️):

| Restaurant | MVVM |
|---|---|
| 🪑 **Dining room** — what customers see | **View** |
| 🧑‍🍳 **Chef** — takes orders, prepares dishes | **ViewModel** |
| 🏬 **Store room / suppliers** — where the ingredients come from | **Model** (Repository + data sources) |

The **dining room** never goes to the **supplier** directly. It asks the **chef**. The chef gets ingredients from the **store room**. Everyone has **one job**. ✅

You already know the **V** and the **VM** (Chapters 5–15). This chapter is about the **M** — especially the **Repository**.

---

## 16.3 The Layers of an App 🏢

Google's official guide splits an app into **layers** — like the **floors** of a building:

```
┌──────────────────────────────────────────────────────────┐
│  🎨 UI LAYER                                              │
│     • Composables (Screens)                               │
│     • ViewModels                                          │
├──────────────────────────────────────────────────────────┤
│  (⚙️ DOMAIN LAYER — optional, for big apps: "use cases")  │
├──────────────────────────────────────────────────────────┤
│  📦 DATA LAYER                                            │
│     • Repositories                                        │
│     • Data sources: 🌐 network (Retrofit), 🗄️ database     │
│       (Room), 💾 settings (DataStore), 📄 files            │
└──────────────────────────────────────────────────────────┘
```

### The 3 rules of layers

| # | Rule | Why |
|---|---|---|
| 1 | **Each layer only talks to the layer right below it.** UI → ViewModel → Repository → Data source. | No shortcuts = no spaghetti. 🍝🚫 |
| 2 | **Lower layers know nothing about upper layers.** The Repository has **no idea** there's a screen. | You can change the screen without touching the data code. |
| 3 | **Data flows up, events flow down.** | One-way flow (Chapter 8, 15) — easy to follow. 🔁 |

> ⚠️ **Never** call the internet or the database **directly** from a Composable or a ViewModel. Always go **through a Repository**.

> ℹ️ The **domain layer** (with "use cases") is **optional** — useful for big apps with complex rules. We won't need it in this book. 😊

---

## 16.4 The Repository — The Store Manager 🏪

### What is a Repository?

A **Repository** is a class that:

1. Is the **only** place the rest of the app gets a certain kind of data from (recipes, users, messages…).
2. **Hides** where the data really comes from: the internet? a database? a file? memory? The ViewModel **doesn't know and doesn't care**. 🙈
3. **Decides** things like: "*Use the saved copy, or download a new one?*"
4. Lets **many** ViewModels **share** the same data.

**Real-life example:** A **shop manager** 🧑‍💼 in a supermarket.
- You (the ViewModel) ask: "*Do you have milk?*" 🥛
- The manager checks the **shelf** (memory), the **back room** (database), or calls the **farm** (internet).
- You **just get milk**. You don't need to know where it was. ✅
- If the shop changes suppliers tomorrow, **you** don't have to change anything. 🎉

### A Repository has a clear set of functions

```kotlin
interface RecipeRepository {
    val recipes: StateFlow<List<Recipe>>
    fun getRecipe(id: Int): Recipe?
    fun toggleFavorite(id: Int)
}
```

That's the **promise** (an **interface**, Chapter 4!): "*Here's what you can ask me.*" **How** it's done is hidden. 🎁

### Naming conventions

| Name | Example |
|---|---|
| `XxxRepository` | `RecipeRepository`, `UserRepository`, `WeatherRepository` |
| Functions | `getRecipe(id)`, `getRecipes()`, `addRecipe(r)`, `deleteRecipe(id)`, `toggleFavorite(id)` |
| Flows | `recipes`, `favoriteIds`, `observeRecipes()` |

---

## 16.5 Single Source of Truth ✅

In Chapter 13's Recipe Book, the **favorites** lived in `RecipeBookApp`, and were passed down to three screens. It worked, but:

- What if a **4th** screen needs them? Pass them through **more** functions. 😩
- What if favorites should be **saved** to a database later? Change the **App** Composable. 😩

**Single source of truth (SSOT)** means:

> **Every piece of data has exactly ONE owner. Everyone else only reads it, and asks the owner to change it.**

For recipes and favorites, the owner is the **`RecipeRepository`**. 🏪

```
          ┌──────────────────────┐
          │  RecipeRepository 🏪  │  ← the ONE owner of recipes + favorites
          │  recipes: StateFlow   │
          └──────────┬───────────┘
        reads ⬆️     │     ⬆️ reads        ⬆️ reads
    ┌────────────────┼────────────────────────────┐
    ▼                ▼                            ▼
ListViewModel   FavoritesViewModel        DetailViewModel
    │                │                            │
    ▼                ▼                            ▼
 List screen    Favorites screen           Detail screen
                                          [♥ tap] → repository.toggleFavorite(id)
```

When the **Detail** screen toggles a favorite:
1. It asks the **repository** to change it.
2. The repository updates its **StateFlow**. 📢
3. **Every** ViewModel watching it gets the **new** data.
4. **Every** screen updates **automatically**. ✨

**No passing data around. No copies that disagree.** 🎉

**Real-life example:** A **family calendar** 📅 on the fridge. Everyone **reads** the same calendar. To add an event, you write it **on that calendar** — not on your own paper. So everybody always sees the **same** plan.

---

## 16.6 Interfaces — Swap Fake Data for Real Data 🔌

Why make `RecipeRepository` an **interface** instead of a normal class?

Because we can have **different versions** that keep the **same promise**:

```kotlin
interface RecipeRepository { ... }                               // 📜 the promise

class InMemoryRecipeRepository : RecipeRepository { ... }        // 🧠 data in memory (today)
class RoomRecipeRepository(...) : RecipeRepository { ... }       // 🗄️ data in a database (Chapter 22)
class NetworkRecipeRepository(...) : RecipeRepository { ... }    // 🌐 data from the internet (Chapter 19)
class FakeRecipeRepository : RecipeRepository { ... }            // 🧪 fixed data for tests & previews
```

The ViewModel only knows the **interface**:

```kotlin
class RecipeListViewModel(
    private val repository: RecipeRepository      // ← the interface, not a specific class!
) : ViewModel() { ... }
```

So we can give it **any** version:

| Situation | Give the ViewModel… |
|---|---|
| Learning (now) | `InMemoryRecipeRepository()` |
| Real app (later) | `RoomRecipeRepository(database)` |
| Tests (Chapter 27) | `FakeRecipeRepository()` |

**Change one line** in one place → the **whole app** uses the new data source. The ViewModels and screens **don't change at all**! 🤯

**Real-life example:** A **wall socket** 🔌. The socket is the **interface**. You can plug in a lamp, a phone charger, or a fan — the socket doesn't care, as long as the plug **fits** (keeps the promise).

### Passing what a class needs from outside = Dependency Injection 💉

Notice: the ViewModel **doesn't create** its repository. It **receives** it in the constructor:

```kotlin
class RecipeListViewModel(private val repository: RecipeRepository) : ViewModel()   // ✅ receives it
```

instead of:

```kotlin
class RecipeListViewModel : ViewModel() {
    private val repository = InMemoryRecipeRepository()    // ❌ creates it — glued forever
}
```

Giving a class what it needs **from outside** is called **Dependency Injection** (DI). A **dependency** is something a class **needs** to do its job.

**Real-life example:** A **chef** doesn't build their own oven. 🔥 The restaurant **gives** them one. Tomorrow it can be a **better** oven — the chef cooks the same way.

> 💡 In this chapter we do DI **by hand** (it's simple!). In **Chapter 23**, a library called **Hilt** will do it **automatically**.

---

## 16.7 Packages — Folders for Your Code 📁

So far, almost everything was in `MainActivity.kt`. For a real app, we split code into **files** and **packages** (folders).

### Two common ways to organize

**By layer** 🏢 (good for small apps):

```
com.example.recipebook
 ├── data/
 ├── ui/
 └── di/
```

**By feature** 🧩 (good for bigger apps) — each feature has its own folder **inside** `ui`:

```
com.example.recipebook
 ├── data/
 │    ├── model/
 │    │    └── Recipe.kt
 │    ├── RecipeRepository.kt
 │    └── InMemoryRecipeRepository.kt
 ├── di/
 │    └── AppContainer.kt
 ├── ui/
 │    ├── theme/                    (Color.kt, Theme.kt, Type.kt)
 │    ├── navigation/
 │    │    ├── Routes.kt
 │    │    └── RecipeBookNavHost.kt
 │    ├── list/
 │    │    ├── RecipeListScreen.kt
 │    │    └── RecipeListViewModel.kt
 │    ├── detail/
 │    │    ├── RecipeDetailScreen.kt
 │    │    └── RecipeDetailViewModel.kt
 │    ├── about/
 │    │    └── AboutScreen.kt
 │    └── components/
 │         └── RecipeCard.kt        (small parts used by many screens)
 ├── RecipeBookApplication.kt
 └── MainActivity.kt
```

We'll use **this mix** in our project: layers at the top, features inside `ui`. It's what most modern apps look like. 🏙️

### How to make a package in Android Studio

1. In the **Project** window, **right-click** your main package (`com.example.recipebook`).
2. **New → Package**.
3. Type the name, for example `data` → Enter. 📁
4. For a package **inside** a package: right-click `data` → **New → Package** → `model`.

### How to make a file inside a package

Right-click the package → **New → Kotlin Class/File** → choose **File** (or **Class**) → type the name.

### The `package` line changes!

A file in `ui/list` starts with:

```kotlin
package com.example.recipebook.ui.list
```

And to use something from another package, you **import** it:

```kotlin
import com.example.recipebook.data.RecipeRepository
import com.example.recipebook.data.model.Recipe
```

> 💡 **Alt + Enter** adds these imports for you. And when you **move** a file with drag and drop, Android Studio offers to **update** the package and imports automatically (**Refactor → Move**). 🪄

### Naming rules for packages

- All **small letters**: `ui.list`, not `UI.List`.
- No spaces, no dashes. Short words.

---

## 16.8 Creating Objects in One Place: the App Container 📦

Who **creates** the repository, and makes sure **everyone shares the same one**? 🤔

If each ViewModel did `InMemoryRecipeRepository()`, each would have its **own** copy — **not** a single source of truth! ❌

### The App Container

A simple class whose job is to **create and hold** the app's shared objects:

```kotlin
interface AppContainer {
    val recipeRepository: RecipeRepository
}

class DefaultAppContainer : AppContainer {
    override val recipeRepository: RecipeRepository by lazy {
        InMemoryRecipeRepository()
    }
}
```

| Code | Meaning |
|---|---|
| `interface AppContainer` | A promise: "*I can give you a recipe repository.*" (A fake container for tests can keep the same promise.) |
| `override val recipeRepository ... by lazy { ... }` | **`lazy`** = "Create it the **first time** someone asks, then **reuse** the same one forever." 😴➡️⚡ |
| `InMemoryRecipeRepository()` | **The one place** in the whole app where we choose **which** repository to use. Change it here → the whole app changes. 🔧 |

**Real-life example:** A **toolbox** 🧰 in the house. Everyone takes tools from the **same** toolbox. Nobody buys their own hammer.

### Where does the container live? The `Application` class 🏛️

Android has a special class called **`Application`**. It's created **once**, **before** any Activity, and lives as long as the **process**. Perfect for app-wide things!

```kotlin
class RecipeBookApplication : Application() {

    lateinit var container: AppContainer

    override fun onCreate() {
        super.onCreate()
        container = DefaultAppContainer()
    }
}
```

| Code | Meaning |
|---|---|
| `class RecipeBookApplication : Application()` | Our own Application class. |
| `lateinit var container: AppContainer` | **`lateinit`** = "I promise to give this a value **later**, before anyone uses it." It's not created in the constructor, but in `onCreate`. (If used before that → crash: *lateinit property has not been initialized*.) |
| `override fun onCreate()` | Called **once** when the app process starts (like the Activity's `onCreate`, but for the **whole** app). |

### Tell Android to use it: the manifest 📜

Open `AndroidManifest.xml` and add **`android:name`** to `<application>`:

```xml
<application
    android:name=".RecipeBookApplication"
    android:icon="@mipmap/ic_launcher"
    android:label="@string/app_name"
    ... >
```

- `android:name=".RecipeBookApplication"` → "Use **my** class as the Application." The `.` means "in my package".
- ⚠️ **Forget this**, and your class is **never** created → the app crashes when it tries to use the container. 💥

---

## 16.9 ViewModel Factories — Giving a ViewModel What It Needs 🏭

In Chapter 15, `viewModel()` created ViewModels with **no inputs** (or only a `SavedStateHandle`). But now our ViewModel needs a **repository**:

```kotlin
class RecipeListViewModel(private val repository: RecipeRepository) : ViewModel()
```

`viewModel()` doesn't know **where** to get a repository! 😕 We need a **factory** — a recipe for **how to build** this ViewModel.

```kotlin
class RecipeListViewModel(
    private val repository: RecipeRepository
) : ViewModel() {

    // ...

    companion object {
        val Factory: ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val app = this[APPLICATION_KEY] as RecipeBookApplication
                RecipeListViewModel(repository = app.container.recipeRepository)
            }
        }
    }
}
```

Imports:

```kotlin
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.ViewModelProvider.AndroidViewModelFactory.Companion.APPLICATION_KEY
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
```

### Every bit explained

| Code | Meaning |
|---|---|
| `companion object { val Factory ... }` | The factory belongs to the **class** (Chapter 4), so we can write `RecipeListViewModel.Factory`. |
| `viewModelFactory { initializer { ... } }` | "Here's **how to build** this ViewModel." |
| `this[APPLICATION_KEY]` | Inside `initializer`, get the **Application** object. 🏛️ |
| `as RecipeBookApplication` | We know it's **our** Application class, so we tell Kotlin (a **cast**, Chapter 4). |
| `app.container.recipeRepository` | Take the **shared** repository from the toolbox 🧰. |
| `RecipeListViewModel(repository = ...)` | Build the ViewModel with it. |

### Using the factory

```kotlin
@Composable
fun RecipeListRoute(
    viewModel: RecipeListViewModel = viewModel(factory = RecipeListViewModel.Factory)
) { ... }
```

`viewModel(factory = ...)` → "Build it **with this recipe** (only the first time; after rotation you still get the same one)." ✅

### A ViewModel that needs a repository **and** a `SavedStateHandle`

```kotlin
initializer {
    val app = this[APPLICATION_KEY] as RecipeBookApplication
    RecipeDetailViewModel(
        savedStateHandle = createSavedStateHandle(),
        repository = app.container.recipeRepository
    )
}
```

Import: `androidx.lifecycle.createSavedStateHandle`

`createSavedStateHandle()` → gives the ViewModel its `SavedStateHandle` (with the **navigation arguments** inside, Chapter 15). 🎁

> 💡 Yes, factories are a bit of **boilerplate** (repeated code). In **Chapter 23**, Hilt removes all of it — you'll just write `hiltViewModel()`. But knowing how it works **underneath** makes Hilt much easier to understand! 🧠

---

## 16.10 From Repository Data to Screen State: `map` + `stateIn` 🌊

The repository gives a `StateFlow<List<Recipe>>`. The **Favorites** screen wants **only** favorites, wrapped in a `UiState`. We need to **change** the flow.

```kotlin
class RecipeListViewModel(
    repository: RecipeRepository,
    private val onlyFavorites: Boolean
) : ViewModel() {

    val uiState: StateFlow<RecipeListUiState> = repository.recipes
        .map { all ->
            val shown = if (onlyFavorites) all.filter { it.isFavorite } else all
            RecipeListUiState(recipes = shown)
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = RecipeListUiState()
        )
}
```

Imports:

```kotlin
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
```

### Every bit explained

**`.map { ... }`** — change every value that flows through 🔄

```kotlin
    repository.recipes
        .map { all -> ... RecipeListUiState(recipes = shown) }
```

- Like `List.map` from Chapter 3, but for a **flow**: every time the repository sends a **new** list, this lambda turns it into a **new** `UiState`.
- **Real-life example:** A **water filter** 🚰. Water (data) flows in; clean water (UiState) flows out — **every time**.

**`.stateIn(...)`** — turn it back into a `StateFlow` the UI can watch

After `map`, we have a plain `Flow` (no current `.value`). `stateIn` makes it a `StateFlow` again:

| Input | Meaning |
|---|---|
| `scope = viewModelScope` | The flow lives as long as the **ViewModel**. When the ViewModel is cleared, it stops. 🧹 (We'll learn `viewModelScope` properly in Chapter 18.) |
| `started = SharingStarted.WhileSubscribed(5_000)` | Only **work** while the UI is **watching**. If the UI stops watching (app in the background) for more than **5 seconds**, pause. 🔋 The 5 s gives time for a **rotation** without restarting. |
| `initialValue = RecipeListUiState()` | What to show **before** the first value arrives. |

> 💡 `5_000` is just `5000` (milliseconds = 5 seconds). The `_` makes big numbers easy to read (Chapter 2).

> 📋 **Copy this recipe!** `.map { ... }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), initialValue)` is used in **thousands** of Android apps. In **Chapter 18** you'll understand every part of it deeply. For now, it's enough to know **what** it does: *"turn repository data into screen state, and keep it up to date."* ✅

---

## 16.11 Build It: Recipe Book with MVVM 📖🏗️

Let's rebuild the Recipe Book from Chapter 13 with:

- 📁 **Packages** by layer and feature
- 🏪 A **`RecipeRepository`** interface + an in-memory version — the **single source of truth** for recipes **and** favorites
- 🧰 An **AppContainer** in a custom **Application**
- 🏭 **ViewModels with factories**
- 🖼️ **Route + Screen** for every screen
- ♥ Toggle favorites from the **list** *and* the **details** — all screens update automatically

> 🛠️ **Use the Recipe Book project from Chapter 13** (it already has Navigation and Serialization), or a new project with the Chapter 13 setup **plus** the Chapter 15 libraries (`lifecycle-viewmodel-compose`, `lifecycle-runtime-compose`).
>
> In the code below, the package is `com.example.recipebook` and the theme is `RecipeBookTheme`. **Use yours!**

### The plan 🗺️

```
com.example.recipebook
 ├── RecipeBookApplication.kt
 ├── MainActivity.kt
 ├── data/
 │    ├── model/Recipe.kt
 │    ├── RecipeRepository.kt
 │    ├── InMemoryRecipeRepository.kt
 │    └── SampleRecipes.kt
 ├── di/
 │    └── AppContainer.kt
 └── ui/
      ├── theme/ (already exists)
      ├── navigation/
      │    ├── Routes.kt
      │    └── RecipeBookNavHost.kt
      ├── components/
      │    └── RecipeCard.kt
      ├── list/
      │    ├── RecipeListViewModel.kt
      │    └── RecipeListScreen.kt
      ├── detail/
      │    ├── RecipeDetailViewModel.kt
      │    └── RecipeDetailScreen.kt
      └── about/
           └── AboutScreen.kt
```

**Delete** the old `Recipe.kt` and `Routes.kt` from Chapter 13 (they move to new places), and **clear** `MainActivity.kt`. Then make the packages: `data`, `data.model`, `di`, `ui.navigation`, `ui.components`, `ui.list`, `ui.detail`, `ui.about`.

---

### 📦 DATA LAYER

#### `data/model/Recipe.kt`

```kotlin
package com.example.recipebook.data.model

data class Recipe(
    val id: Int,
    val name: String,
    val emoji: String,
    val minutes: Int,
    val ingredients: List<String>,
    val steps: List<String>,
    val isFavorite: Boolean = false
)
```

New: `isFavorite` is now **part of the recipe**. The repository keeps it up to date.

#### `data/RecipeRepository.kt` — the promise 📜

```kotlin
package com.example.recipebook.data

import com.example.recipebook.data.model.Recipe
import kotlinx.coroutines.flow.StateFlow

interface RecipeRepository {
    /** All recipes. Watch it: it updates when something changes. */
    val recipes: StateFlow<List<Recipe>>

    /** One recipe by id, or null if it doesn't exist. */
    fun getRecipe(id: Int): Recipe?

    /** Add or remove a recipe from the favorites. */
    fun toggleFavorite(id: Int)
}
```

> 💡 `/** ... */` is a **documentation comment** (a special comment). When you hover over `toggleFavorite` anywhere in your code, Android Studio **shows** this text. Great for interfaces! 📝

#### `data/SampleRecipes.kt` — the starting data

```kotlin
package com.example.recipebook.data

import com.example.recipebook.data.model.Recipe

val sampleRecipes = listOf(
    Recipe(
        id = 1, name = "Pizza", emoji = "🍕", minutes = 30, isFavorite = true,
        ingredients = listOf("Flour", "Water", "Yeast", "Tomato sauce", "Cheese"),
        steps = listOf(
            "Mix flour, water, and yeast to make the dough.",
            "Let the dough rest for 1 hour.",
            "Spread the dough, add sauce and cheese.",
            "Bake at 220°C for 12 minutes."
        )
    ),
    Recipe(
        id = 2, name = "Pasta", emoji = "🍝", minutes = 20,
        ingredients = listOf("Pasta", "Garlic", "Olive oil", "Tomatoes", "Basil"),
        steps = listOf(
            "Boil the pasta in salty water.",
            "Fry garlic in olive oil.",
            "Add tomatoes and cook for 5 minutes.",
            "Mix with the pasta and add basil."
        )
    ),
    Recipe(
        id = 3, name = "Pancakes", emoji = "🥞", minutes = 15, isFavorite = true,
        ingredients = listOf("Flour", "Milk", "Eggs", "Sugar", "Butter"),
        steps = listOf(
            "Mix flour, milk, eggs, and sugar.",
            "Heat butter in a pan.",
            "Pour a small cup of batter and cook both sides."
        )
    ),
    Recipe(
        id = 4, name = "Salad", emoji = "🥗", minutes = 10,
        ingredients = listOf("Lettuce", "Cucumber", "Tomato", "Olive oil", "Lemon"),
        steps = listOf(
            "Wash and cut the vegetables.",
            "Mix olive oil and lemon juice.",
            "Pour over the salad and mix."
        )
    ),
    Recipe(
        id = 5, name = "Soup", emoji = "🍲", minutes = 40,
        ingredients = listOf("Carrots", "Potatoes", "Onion", "Water", "Salt"),
        steps = listOf(
            "Cut all vegetables into small pieces.",
            "Boil them in water for 30 minutes.",
            "Add salt and blend until smooth."
        )
    ),
    Recipe(
        id = 6, name = "Smoothie", emoji = "🥤", minutes = 5,
        ingredients = listOf("Banana", "Strawberries", "Yogurt", "Honey"),
        steps = listOf(
            "Put everything in a blender.",
            "Blend for 1 minute.",
            "Pour into a glass and enjoy!"
        )
    )
)
```

#### `data/InMemoryRecipeRepository.kt` — keeping the promise 🧠

```kotlin
package com.example.recipebook.data

import com.example.recipebook.data.model.Recipe
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

class InMemoryRecipeRepository(
    initialRecipes: List<Recipe> = sampleRecipes
) : RecipeRepository {

    private val _recipes = MutableStateFlow(initialRecipes)
    override val recipes: StateFlow<List<Recipe>> = _recipes.asStateFlow()

    override fun getRecipe(id: Int): Recipe? =
        _recipes.value.find { it.id == id }

    override fun toggleFavorite(id: Int) {
        _recipes.update { list ->
            list.map { recipe ->
                if (recipe.id == id) recipe.copy(isFavorite = !recipe.isFavorite) else recipe
            }
        }
    }
}
```

| Code | Meaning |
|---|---|
| `: RecipeRepository` | This class **keeps the promise** (implements the interface). |
| `initialRecipes: List<Recipe> = sampleRecipes` | The starting data, with a default. For tests, we can give **different** data! 🧪 |
| `private val _recipes` + `override val recipes` | The **backing property** pattern (Chapter 15) — only the repository can change the data. 🔒 |
| `toggleFavorite` | The **update pattern** from Chapter 10: `map` + `copy`. Then `update` tells everyone watching. 📢 |

> ⚠️ "In memory" means the data is **lost** when the app closes. In **Chapter 22**, we'll write a `RoomRecipeRepository` that saves to a database — and **nothing else** in the app will need to change. That's the power of the interface! 🔌

---

### 🧰 DI: the container and the Application

#### `di/AppContainer.kt`

```kotlin
package com.example.recipebook.di

import com.example.recipebook.data.InMemoryRecipeRepository
import com.example.recipebook.data.RecipeRepository

interface AppContainer {
    val recipeRepository: RecipeRepository
}

class DefaultAppContainer : AppContainer {
    override val recipeRepository: RecipeRepository by lazy {
        InMemoryRecipeRepository()
    }
}
```

#### `RecipeBookApplication.kt` (in the main package)

```kotlin
package com.example.recipebook

import android.app.Application
import com.example.recipebook.di.AppContainer
import com.example.recipebook.di.DefaultAppContainer

class RecipeBookApplication : Application() {

    lateinit var container: AppContainer

    override fun onCreate() {
        super.onCreate()
        container = DefaultAppContainer()
    }
}
```

#### `AndroidManifest.xml` — add one attribute

```xml
<application
    android:name=".RecipeBookApplication"
    ... the rest stays the same ... >
```

---

### 🎨 UI LAYER

#### `ui/navigation/Routes.kt`

```kotlin
package com.example.recipebook.ui.navigation

import kotlinx.serialization.Serializable

@Serializable object RecipeList
@Serializable object Favorites
@Serializable object About
@Serializable data class RecipeDetail(val recipeId: Int)
```

(We skip the Welcome screen this time to keep the focus on architecture. 😊)

#### `ui/components/RecipeCard.kt` — shared by two screens

```kotlin
package com.example.recipebook.ui.components

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.recipebook.data.model.Recipe

@Composable
fun RecipeCard(
    recipe: Recipe,
    onClick: () -> Unit,
    onToggleFavorite: () -> Unit,
    modifier: Modifier = Modifier
) {
    ElevatedCard(onClick = onClick, modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.padding(start = 16.dp, top = 12.dp, bottom = 12.dp, end = 4.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(recipe.emoji, fontSize = 40.sp)
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(recipe.name, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                Text(
                    text = "⏱️ ${recipe.minutes} min · ${recipe.ingredients.size} ingredients",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            IconButton(onClick = onToggleFavorite) {
                Icon(
                    imageVector = Icons.Filled.Favorite,
                    contentDescription = if (recipe.isFavorite) "Remove from favorites" else "Add to favorites",
                    tint = if (recipe.isFavorite) Color(0xFFE53935) else MaterialTheme.colorScheme.outlineVariant
                )
            }
        }
    }
}
```

#### `ui/list/RecipeListViewModel.kt` 🧠

```kotlin
package com.example.recipebook.ui.list

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.ViewModelProvider.AndroidViewModelFactory.Companion.APPLICATION_KEY
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.example.recipebook.RecipeBookApplication
import com.example.recipebook.data.RecipeRepository
import com.example.recipebook.data.model.Recipe
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn

data class RecipeListUiState(
    val recipes: List<Recipe> = emptyList(),
    val isLoading: Boolean = true
)

class RecipeListViewModel(
    private val repository: RecipeRepository,
    private val onlyFavorites: Boolean
) : ViewModel() {

    val uiState: StateFlow<RecipeListUiState> = repository.recipes
        .map { all ->
            val shown = if (onlyFavorites) all.filter { it.isFavorite } else all
            RecipeListUiState(recipes = shown, isLoading = false)
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = RecipeListUiState()
        )

    fun onToggleFavorite(id: Int) {
        repository.toggleFavorite(id)
    }

    companion object {
        fun factory(onlyFavorites: Boolean): ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val app = this[APPLICATION_KEY] as RecipeBookApplication
                RecipeListViewModel(
                    repository = app.container.recipeRepository,
                    onlyFavorites = onlyFavorites
                )
            }
        }
    }
}
```

| New idea | Meaning |
|---|---|
| `isLoading: Boolean = true` | Before the first data arrives, the screen knows it's **loading**. (With the internet in Chapter 19, this will really matter! ⏳) |
| `onlyFavorites: Boolean` | The **same** ViewModel class works for **both** the Recipes tab and the Favorites tab. ♻️ |
| `fun factory(onlyFavorites: Boolean)` | A **function** that makes a factory — so we can pass the extra input. |
| `onToggleFavorite(id)` | The ViewModel **doesn't** change any list itself — it **asks the repository** (the single source of truth). Then the change **flows back** through `recipes` → `map` → `uiState`. 🔁 |

#### `ui/list/RecipeListScreen.kt` 🎨

```kotlin
package com.example.recipebook.ui.list

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.recipebook.data.sampleRecipes
import com.example.recipebook.ui.components.RecipeCard
import com.example.recipebook.ui.theme.RecipeBookTheme

@Composable
fun RecipeListRoute(
    title: String,
    emptyText: String,
    onlyFavorites: Boolean,
    onRecipeClick: (Int) -> Unit,
    viewModel: RecipeListViewModel = viewModel(
        key = if (onlyFavorites) "favorites" else "all",
        factory = RecipeListViewModel.factory(onlyFavorites)
    )
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    RecipeListScreen(
        title = title,
        emptyText = emptyText,
        uiState = uiState,
        onRecipeClick = onRecipeClick,
        onToggleFavorite = viewModel::onToggleFavorite
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RecipeListScreen(
    title: String,
    emptyText: String,
    uiState: RecipeListUiState,
    onRecipeClick: (Int) -> Unit,
    onToggleFavorite: (Int) -> Unit
) {
    Scaffold(topBar = { TopAppBar(title = { Text(title) }) }) { innerPadding ->
        when {
            uiState.isLoading -> {
                Box(Modifier.fillMaxSize().padding(innerPadding), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            }
            uiState.recipes.isEmpty() -> {
                Box(Modifier.fillMaxSize().padding(innerPadding), contentAlignment = Alignment.Center) {
                    Text(emptyText, textAlign = TextAlign.Center, style = MaterialTheme.typography.titleMedium)
                }
            }
            else -> {
                LazyColumn(
                    contentPadding = PaddingValues(
                        start = 16.dp,
                        end = 16.dp,
                        top = innerPadding.calculateTopPadding() + 8.dp,
                        bottom = innerPadding.calculateBottomPadding() + 16.dp
                    ),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    items(uiState.recipes, key = { it.id }) { recipe ->
                        RecipeCard(
                            recipe = recipe,
                            onClick = { onRecipeClick(recipe.id) },
                            onToggleFavorite = { onToggleFavorite(recipe.id) },
                            modifier = Modifier.animateItem()
                        )
                    }
                }
            }
        }
    }
}

@Preview(showSystemUi = true)
@Composable
fun RecipeListScreenPreview() {
    RecipeBookTheme {
        RecipeListScreen(
            title = "Recipes 🍳",
            emptyText = "",
            uiState = RecipeListUiState(recipes = sampleRecipes, isLoading = false),
            onRecipeClick = {},
            onToggleFavorite = {}
        )
    }
}
```

| New idea | Meaning |
|---|---|
| `viewModel(key = ..., factory = ...)` | ⚠️ **The `key`!** Both the Recipes and Favorites tabs use `RecipeListViewModel`. Inside **one** screen's back stack entry that's fine — but adding a **key** makes sure each version gets its **own** ViewModel and is never mixed up. 🔑 |
| `CircularProgressIndicator()` | A spinning circle ⏳ — shown while `isLoading` is true. |
| `when { isLoading -> ...; isEmpty -> ...; else -> ... }` | The **3 states** of almost every list screen: **loading**, **empty**, **content**. 🎯 |

#### `ui/detail/RecipeDetailViewModel.kt` 🧠

```kotlin
package com.example.recipebook.ui.detail

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.ViewModelProvider.AndroidViewModelFactory.Companion.APPLICATION_KEY
import androidx.lifecycle.createSavedStateHandle
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import androidx.navigation.toRoute
import com.example.recipebook.RecipeBookApplication
import com.example.recipebook.data.RecipeRepository
import com.example.recipebook.data.model.Recipe
import com.example.recipebook.ui.navigation.RecipeDetail
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn

data class RecipeDetailUiState(
    val recipe: Recipe? = null,
    val notFound: Boolean = false
)

class RecipeDetailViewModel(
    savedStateHandle: SavedStateHandle,
    private val repository: RecipeRepository
) : ViewModel() {

    private val recipeId: Int = savedStateHandle.toRoute<RecipeDetail>().recipeId

    val uiState: StateFlow<RecipeDetailUiState> = repository.recipes
        .map { all ->
            val recipe = all.find { it.id == recipeId }
            RecipeDetailUiState(recipe = recipe, notFound = recipe == null)
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = RecipeDetailUiState(recipe = repository.getRecipe(recipeId))
        )

    fun onToggleFavorite() {
        repository.toggleFavorite(recipeId)
    }

    companion object {
        val Factory: ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val app = this[APPLICATION_KEY] as RecipeBookApplication
                RecipeDetailViewModel(
                    savedStateHandle = createSavedStateHandle(),
                    repository = app.container.recipeRepository
                )
            }
        }
    }
}
```

| New idea | Meaning |
|---|---|
| `savedStateHandle.toRoute<RecipeDetail>().recipeId` | The ViewModel reads the **id** from the route itself (Chapter 15). |
| `.map { all -> all.find { it.id == recipeId } }` | Watch **all** recipes, pick **ours**. When its favorite changes (from **any** screen!), this screen updates. ✨ |
| `initialValue = ...getRecipe(recipeId)` | Show the recipe **immediately**, no flicker. |
| `notFound` | A clear flag for "*this id doesn't exist*". |

#### `ui/detail/RecipeDetailScreen.kt` 🎨

```kotlin
package com.example.recipebook.ui.detail

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.recipebook.data.sampleRecipes
import com.example.recipebook.ui.theme.RecipeBookTheme

@Composable
fun RecipeDetailRoute(
    onBack: () -> Unit,
    viewModel: RecipeDetailViewModel = viewModel(factory = RecipeDetailViewModel.Factory)
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    RecipeDetailScreen(
        uiState = uiState,
        onToggleFavorite = viewModel::onToggleFavorite,
        onBack = onBack
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RecipeDetailScreen(
    uiState: RecipeDetailUiState,
    onToggleFavorite: () -> Unit,
    onBack: () -> Unit
) {
    val recipe = uiState.recipe

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(recipe?.name ?: "Not found") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    if (recipe != null) {
                        IconButton(onClick = onToggleFavorite) {
                            Icon(
                                imageVector = Icons.Filled.Favorite,
                                contentDescription = if (recipe.isFavorite) "Remove from favorites" else "Add to favorites",
                                tint = if (recipe.isFavorite) Color(0xFFE53935) else MaterialTheme.colorScheme.outline
                            )
                        }
                    }
                }
            )
        }
    ) { innerPadding ->
        if (recipe == null) {
            Box(Modifier.fillMaxSize().padding(innerPadding), contentAlignment = Alignment.Center) {
                Text("😕 This recipe doesn't exist.")
            }
            return@Scaffold
        }

        LazyColumn(
            contentPadding = PaddingValues(
                start = 16.dp,
                end = 16.dp,
                top = innerPadding.calculateTopPadding(),
                bottom = innerPadding.calculateBottomPadding() + 24.dp
            )
        ) {
            item {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(recipe.emoji, fontSize = 72.sp)
                    Spacer(modifier = Modifier.width(16.dp))
                    Text("⏱️ ${recipe.minutes} minutes", style = MaterialTheme.typography.titleMedium)
                }
                Spacer(modifier = Modifier.height(16.dp))
                Text("Ingredients 🧺", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            }
            items(recipe.ingredients) { ingredient ->
                Text("• $ingredient", style = MaterialTheme.typography.bodyLarge, modifier = Modifier.padding(vertical = 4.dp))
            }
            item {
                Spacer(modifier = Modifier.height(16.dp))
                Text("Steps 👩‍🍳", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
            }
            itemsIndexed(recipe.steps) { index, step ->
                Row(modifier = Modifier.padding(vertical = 6.dp)) {
                    Text("${index + 1}.", fontWeight = FontWeight.Bold, modifier = Modifier.width(28.dp))
                    Text(step, style = MaterialTheme.typography.bodyLarge)
                }
            }
        }
    }
}

@Preview(showSystemUi = true)
@Composable
fun RecipeDetailScreenPreview() {
    RecipeBookTheme {
        RecipeDetailScreen(
            uiState = RecipeDetailUiState(recipe = sampleRecipes.first()),
            onToggleFavorite = {},
            onBack = {}
        )
    }
}
```

#### `ui/about/AboutScreen.kt`

```kotlin
package com.example.recipebook.ui.about

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AboutScreen() {
    Scaffold(topBar = { TopAppBar(title = { Text("About ℹ️") }) }) { innerPadding ->
        Column(
            modifier = Modifier.fillMaxSize().padding(innerPadding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text("Recipe Book 📖", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            Text("Version 2.0 — now with MVVM 🏗️")
            Text("Built with Kotlin, Jetpack Compose, Navigation, and ViewModels. 💚")
        }
    }
}
```

#### `ui/navigation/RecipeBookNavHost.kt` 🧭

```kotlin
package com.example.recipebook.ui.navigation

import androidx.compose.foundation.layout.consumeWindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.navigation.NavDestination.Companion.hasRoute
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.example.recipebook.ui.about.AboutScreen
import com.example.recipebook.ui.detail.RecipeDetailRoute
import com.example.recipebook.ui.list.RecipeListRoute

data class TopLevelRoute<T : Any>(val label: String, val icon: ImageVector, val route: T)

private val topLevelRoutes = listOf(
    TopLevelRoute("Recipes", Icons.Filled.Home, RecipeList),
    TopLevelRoute("Favorites", Icons.Filled.Favorite, Favorites),
    TopLevelRoute("About", Icons.Filled.Info, About)
)

@Composable
fun RecipeBookNavHost() {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination

    val showBottomBar = topLevelRoutes.any { currentDestination?.hasRoute(it.route::class) == true }

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        bottomBar = {
            if (showBottomBar) {
                NavigationBar {
                    topLevelRoutes.forEach { topLevel ->
                        NavigationBarItem(
                            selected = currentDestination?.hierarchy?.any { it.hasRoute(topLevel.route::class) } == true,
                            onClick = {
                                navController.navigate(topLevel.route) {
                                    popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            },
                            icon = { Icon(topLevel.icon, contentDescription = null) },
                            label = { Text(topLevel.label) }
                        )
                    }
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = RecipeList,
            modifier = Modifier.padding(innerPadding).consumeWindowInsets(innerPadding)
        ) {
            composable<RecipeList> {
                RecipeListRoute(
                    title = "Recipes 🍳",
                    emptyText = "No recipes yet.",
                    onlyFavorites = false,
                    onRecipeClick = { id -> navController.navigate(RecipeDetail(id)) }
                )
            }
            composable<Favorites> {
                RecipeListRoute(
                    title = "Favorites ♥",
                    emptyText = "No favorites yet.\nTap ♥ on a recipe.",
                    onlyFavorites = true,
                    onRecipeClick = { id -> navController.navigate(RecipeDetail(id)) }
                )
            }
            composable<About> {
                AboutScreen()
            }
            composable<RecipeDetail> {
                RecipeDetailRoute(onBack = { navController.navigateUp() })
            }
        }
    }
}
```

> ✅ This time `startDestination = RecipeList` (the first tab), so the **official** tab recipe with `findStartDestination()` works perfectly. (Remember the Welcome-screen problem from Chapter 13? 😉)

#### `MainActivity.kt` — tiny now! 🎉

```kotlin
package com.example.recipebook

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.recipebook.ui.navigation.RecipeBookNavHost
import com.example.recipebook.ui.theme.RecipeBookTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            RecipeBookTheme {
                RecipeBookNavHost()
            }
        }
    }
}
```

From **hundreds** of lines to **12**. The Activity is just the **door** 🚪 now.

---

### 🔁 Follow one tap through all the layers

Let's trace what happens when you tap ♥ on the **details** screen:

```
1. 👆 User taps ♥ in RecipeDetailScreen
        │  onToggleFavorite()                         (event ⬆️)
        ▼
2. 🧠 RecipeDetailViewModel.onToggleFavorite()
        │  repository.toggleFavorite(recipeId)        (asks the owner)
        ▼
3. 🏪 InMemoryRecipeRepository.toggleFavorite(id)
        │  _recipes.update { map + copy }             (the ONE change)
        ▼
4. 📢 repository.recipes sends a NEW list to everyone watching:
        ├──▶ RecipeDetailViewModel   .map → new uiState → ♥ turns red
        ├──▶ RecipeListViewModel (all)  .map → new uiState → ♥ on the card
        └──▶ RecipeListViewModel (favorites) .map → recipe appears in Favorites
        │
        ▼
5. 🎨 Every screen that's visible recomposes with its new state. ✨
```

**One** change, in **one** place → **every** screen is correct. That's the **single source of truth**. 🏆

### Run it! ▶️

1. Tap ♥ on **Pasta** in the list → it turns red. Open **Favorites** → Pasta is there!
2. Open **Salad** → tap ♥ in the top bar → go back → Salad's card has a red ♥.
3. On **Favorites**, tap ♥ on Pizza → it **slides away** (it's not a favorite anymore). ✨
4. **Rotate** anywhere → nothing is lost (ViewModels + repository survive).

> ⚠️ Close the app completely and reopen → favorites are **back to the start**. That's because the repository is **in memory**. In **Chapter 22**, we'll swap in a **database** repository — by changing **one line** in `AppContainer`. 🔌

---

## 16.12 Bonus: A Fake Repository for Previews and Tests 🧪

Because the ViewModel depends on the **interface**, we can write a **fake** one:

```kotlin
class FakeRecipeRepository(
    recipes: List<Recipe> = sampleRecipes.take(2)
) : RecipeRepository {

    private val _recipes = MutableStateFlow(recipes)
    override val recipes: StateFlow<List<Recipe>> = _recipes.asStateFlow()

    var toggleCalls = 0      // count how many times toggle was called (for tests)

    override fun getRecipe(id: Int): Recipe? = _recipes.value.find { it.id == id }

    override fun toggleFavorite(id: Int) {
        toggleCalls++
        _recipes.update { list ->
            list.map { if (it.id == id) it.copy(isFavorite = !it.isFavorite) else it }
        }
    }
}
```

Now a test (Chapter 27) can do:

```kotlin
val fakeRepo = FakeRecipeRepository()
val vm = RecipeListViewModel(repository = fakeRepo, onlyFavorites = false)
vm.onToggleFavorite(1)
// check: fakeRepo.toggleCalls == 1 ✅
```

No phone, no screen, no internet needed. ⚡

---

## 16.13 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| Forgot `android:name=".RecipeBookApplication"` in the manifest | 💥 *ClassCastException: android.app.Application cannot be cast to RecipeBookApplication* | Add `android:name` to `<application>`. |
| Each ViewModel creates its own repository | Data not shared; screens disagree | Create it **once** in the AppContainer; pass it in. |
| ViewModel depends on `InMemoryRecipeRepository` (the class) | Can't swap for a database or fake | Depend on the **interface** `RecipeRepository`. |
| `viewModel()` without a factory for a ViewModel with inputs | 💥 *Cannot create an instance of class RecipeListViewModel* | `viewModel(factory = RecipeListViewModel.Factory)` |
| Two uses of the same ViewModel class mixed up | Favorites tab shows all recipes (or the opposite) | Give each a different `key` in `viewModel(key = ..., factory = ...)`. |
| A Composable calls the repository directly | Layers are broken; hard to test | Composable → ViewModel → Repository. |
| Repository exposes a public `MutableStateFlow` | Anyone can change data → chaos | `private val _x` + `override val x = _x.asStateFlow()`. |
| ViewModel copies the list and changes its copy | Other screens don't see the change | Ask the repository to change it (single source of truth). |
| `lateinit property container has not been initialized` | Container used before `Application.onCreate` / manifest missing | Check the manifest; create the container in `onCreate`. |
| Wrong `package` line after moving a file | *Unresolved reference* everywhere | Use **Refactor → Move** in Android Studio, or fix the package and imports. |
| Everything in one giant file | Hard to read and change | Split into packages by layer and feature. |

---

## 16.14 Summary — What You Learned 🎓

✅ **Architecture** = a plan for where code lives → easy to read, change, test, and grow.

✅ **MVVM:** **Model** (data + repository), **View** (Composables), **ViewModel** (the bridge).

✅ **Layers:** UI (screens + ViewModels) → Data (repositories + data sources). Each layer only talks to the one below; data flows up, events flow down.

✅ **Repository** = the only door to a kind of data. Hides where the data comes from.

✅ **Single source of truth:** one owner per piece of data; everyone else reads and asks.

✅ **Interfaces** let you swap **in-memory**, **database**, **network**, and **fake** repositories without changing ViewModels.

✅ **Dependency Injection:** give a class what it needs **from outside** (constructor). Done by hand with an **AppContainer** in a custom **`Application`** class (+ manifest `android:name`).

✅ **ViewModel factories:** `viewModelFactory { initializer { ... } }`, `APPLICATION_KEY`, `createSavedStateHandle()`, and `viewModel(key, factory)`.

✅ **`map` + `stateIn(viewModelScope, WhileSubscribed(5_000), initial)`** turns repository data into screen state.

✅ **Packages:** `data`, `di`, `ui/feature`… with matching `package` lines and imports.

✅ You rebuilt the **Recipe Book** with real MVVM architecture! 📖🏗️

---

## 16.15 Practice Time 🏋️

**Task 1 — Draw the layers ✏️:**
For a **Weather app** that shows today's weather from the internet and saves the last result: list the **classes** you'd create in each layer (UI, ViewModel, Repository, data sources).

**Task 2 — Add a feature through all layers:**
In the MVVM Recipe Book, add a **"Clear all favorites"** button to the Favorites screen's top bar.
1. Add `fun clearFavorites()` to the **interface**.
2. Implement it in `InMemoryRecipeRepository`.
3. Add `onClearFavorites()` to `RecipeListViewModel`.
4. Add the button to the screen (only when `onlyFavorites` is true and the list isn't empty).

**Task 3 — A second repository:**
Make `ShuffledRecipeRepository` that keeps the same promise, but gives the recipes in **random order** at the start (`sampleRecipes.shuffled()`). Use it by changing **only** `AppContainer`. Did you need to change any screen or ViewModel?

**Task 4 — Search in the ViewModel:**
Add a search box to the Recipes tab. The **query** lives in the ViewModel (`MutableStateFlow("")`). The UiState shows only recipes whose name contains the query.
*Hint:* use `combine(repository.recipes, _query) { all, query -> ... }` instead of `map`, then the same `stateIn`. (Import `kotlinx.coroutines.flow.combine`.)

**Task 5 — Spot the problems 🔍:**
What's wrong with this code? (There are 3 architecture problems.)

```kotlin
@Composable
fun FavoritesScreen() {
    val repository = InMemoryRecipeRepository()
    val favorites = repository.recipes.value.filter { it.isFavorite }
    LazyColumn {
        items(favorites) { recipe -> Text(recipe.name) }
    }
}
```

---

### Answers

**Task 1:**

```
UI layer
 ├── WeatherScreen (Composable, stateless) + WeatherRoute
 └── WeatherViewModel  (WeatherUiState: loading / temperature / error)

Data layer
 ├── WeatherRepository (interface) + DefaultWeatherRepository
 │     "Give me today's weather" — decides: internet or saved copy?
 ├── WeatherNetworkDataSource  (talks to the internet — Retrofit, Chapter 19)
 └── WeatherLocalDataSource    (saves the last result — Room or DataStore, Chapters 21–22)

DI
 └── AppContainer: creates the data sources and the repository once
```

**Task 2:**

```kotlin
// RecipeRepository.kt
interface RecipeRepository {
    val recipes: StateFlow<List<Recipe>>
    fun getRecipe(id: Int): Recipe?
    fun toggleFavorite(id: Int)
    fun clearFavorites()
}

// InMemoryRecipeRepository.kt
override fun clearFavorites() {
    _recipes.update { list -> list.map { it.copy(isFavorite = false) } }
}

// RecipeListViewModel.kt
fun onClearFavorites() {
    repository.clearFavorites()
}

// RecipeListRoute: pass it down
//   onClearFavorites = viewModel::onClearFavorites,
//   showClearButton = onlyFavorites

// RecipeListScreen: in the TopAppBar
actions = {
    if (showClearButton && uiState.recipes.isNotEmpty()) {
        TextButton(onClick = onClearFavorites) { Text("Clear all") }
    }
}
```

The change went through **every layer**, top to bottom — and each layer stayed **clean**. 🏗️ (If you also made a `FakeRecipeRepository`, Kotlin will show an **error** there until you add `clearFavorites` — the interface makes sure **every** version keeps the promise! 🛡️)

**Task 3:**

```kotlin
class ShuffledRecipeRepository : RecipeRepository {
    private val _recipes = MutableStateFlow(sampleRecipes.shuffled())
    override val recipes: StateFlow<List<Recipe>> = _recipes.asStateFlow()

    override fun getRecipe(id: Int): Recipe? = _recipes.value.find { it.id == id }

    override fun toggleFavorite(id: Int) {
        _recipes.update { list ->
            list.map { if (it.id == id) it.copy(isFavorite = !it.isFavorite) else it }
        }
    }
}

// AppContainer.kt — the ONLY change in the app:
override val recipeRepository: RecipeRepository by lazy {
    ShuffledRecipeRepository()
}
```

**No** screen or ViewModel changed. 🔌✨ (Even shorter: `InMemoryRecipeRepository(sampleRecipes.shuffled())` — because we gave it a constructor input!)

**Task 4:**

```kotlin
class RecipeListViewModel(
    private val repository: RecipeRepository,
    private val onlyFavorites: Boolean
) : ViewModel() {

    private val _query = MutableStateFlow("")
    val query: StateFlow<String> = _query.asStateFlow()

    val uiState: StateFlow<RecipeListUiState> =
        combine(repository.recipes, _query) { all, query ->
            val shown = all
                .filter { !onlyFavorites || it.isFavorite }
                .filter { it.name.contains(query.trim(), ignoreCase = true) }
            RecipeListUiState(recipes = shown, isLoading = false)
        }.stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = RecipeListUiState()
        )

    fun onQueryChange(newQuery: String) {
        _query.value = newQuery
    }

    fun onToggleFavorite(id: Int) = repository.toggleFavorite(id)

    // companion object with factory(...) stays the same
}
```

- `combine(a, b) { valueA, valueB -> ... }` → runs whenever **either** flow changes. 🔀
- In the Route: `val query by viewModel.query.collectAsStateWithLifecycle()` and pass `query` + `viewModel::onQueryChange` to a `SearchBox` (Chapter 10) in the screen.

**Task 5:**

1. 🐛 **The Composable creates its own repository** → not shared, not the single source of truth. (And a **new** one on every recomposition!)
2. 🐛 **The Composable talks to the repository directly** → skips the ViewModel layer.
3. 🐛 **It reads `.value` once** → it doesn't **watch** the flow, so it **won't update** when favorites change. (The filtering logic also belongs in a ViewModel.)

Fix: a `FavoritesRoute` with `viewModel(factory = ...)` + `collectAsStateWithLifecycle()`, exactly like our `RecipeListRoute`. ✅

---

## 16.16 What Is Next?

🎉 **You now know how to structure a real app!** UI → ViewModel → Repository → Data.

Before the mini project, a quick look back: we used `viewModelScope`, `stateIn`, `Flow`, `scope.launch`… and said "**Chapter 18**" many times. 😄 That chapter will explain all of it.

But first — time to **practice**! In **Chapter 17: 🛠️ Mini Project — Quiz App**, you will build a complete **Quiz** app from scratch using **everything** from Part 4:

- 🧭 **Navigation**: Start → Question → Result screens
- 🧠 A **ViewModel** with `UiState`, events, and `SavedStateHandle`
- 🏪 A **QuestionRepository** with an interface
- 📁 **Packages** and an **AppContainer**
- ✅ Scoring, a progress bar, answer feedback, and "Play again"

**Amazing work finishing Chapter 16! 🎉 You're thinking like a professional Android developer now!**
