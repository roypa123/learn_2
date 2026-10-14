# Chapter 23: Connecting the Pieces — Dependency Injection with Hilt 💉🤖

> **What you will learn in this chapter**
>
> 1. What a **dependency** is, and what **dependency injection** (DI) means 💉
> 2. Surprise: you've **already** been doing DI by hand! 🎁
> 3. The problems with hand-made wiring 😓
> 4. **Hilt** — a robot that does the wiring for you 🤖
> 5. The Hilt words: `@HiltAndroidApp`, `@AndroidEntryPoint`, `@Inject`, `@HiltViewModel`, `@Module`, `@Provides`, `@Binds`, `@Singleton` 🏷️
> 6. Setting up Hilt 📦
> 7. 🔁 Converting the **Recipe Book** to Hilt — and watching code **disappear** ✂️
> 8. **Assisted injection** — when a ViewModel needs a value from the screen
> 9. Hilt for **Retrofit** — converting the **Joke Machine** 😂
> 10. **Scopes** — "only one" vs "a new one every time" 🔢
> 11. Reading Hilt's **error messages** without fear 😌
>
> **Time needed:** about 4–5 hours.
>
> **What you need to know:** Chapters 1–22, especially 16 (MVVM, AppContainer, factories), 19 (Retrofit), and 22 (Room).

---

## 23.1 What Is a Dependency? 🔗

Look at this ViewModel from Chapter 16:

```kotlin
class RecipeDetailViewModel(
    savedStateHandle: SavedStateHandle,
    private val repository: RecipeRepository
) : ViewModel()
```

The ViewModel **can't work** without a `RecipeRepository`. It **depends** on it. So the repository is a **dependency** of the ViewModel. 🔗

Dependencies are everywhere:

```
RecipeDetailViewModel
   └── needs RecipeRepository
          └── needs RecipeDao  +  CoroutineScope
                   └── needs RecipeDatabase
                            └── needs Context
```

Like a **chain** ⛓️: each piece needs the piece below it.

### Two ways to get what you need 🍕

Imagine a **pizza chef** 👨‍🍳 who needs an **oven**.

**Way 1 — The chef builds the oven himself** 🔨

```kotlin
class Chef {
    private val oven = Oven()          // the chef MAKES his own oven
    fun bake() = oven.heat()
}
```

Problems:
- Every chef builds **his own** oven → 10 chefs, 10 ovens. 💸
- Want a **gas** oven instead of electric? You must **change the Chef** class.
- Testing the chef with a **toy** oven? Impossible — the real oven is built inside. 🧪❌

**Way 2 — The restaurant GIVES the chef an oven** 🎁

```kotlin
class Chef(private val oven: Oven) {   // the oven is GIVEN to the chef
    fun bake() = oven.heat()
}

val oven = Oven()
val chef = Chef(oven)                  // someone else decides which oven
```

Now:
- Many chefs can **share** one oven. ✅
- Gas or electric? **Whoever creates the chef** decides. The `Chef` class doesn't change. ✅
- Testing? Give the chef a **toy oven**. ✅

**Way 2 is dependency injection.** 💉 A fancy name for a simple idea:

> 🎯 **Dependency Injection (DI)** = a class **receives** the things it needs (usually through its **constructor**), instead of **creating** them itself.

"**Injection**" just means "**giving from outside**" — like a doctor's injection puts medicine **into** you from outside. 💉

---

## 23.2 Surprise — You're Already Doing It! 🎁

Since Chapter 16, every ViewModel **receives** its repository. Every repository **receives** its DAO or API service. And **who** creates everything and hands it out? The **AppContainer** 🧰:

```kotlin
class DefaultAppContainer(private val context: Context) : AppContainer {

    private val applicationScope = CoroutineScope(SupervisorJob() + Dispatchers.Default)

    private val database: RecipeDatabase by lazy {
        Room.databaseBuilder(context, RecipeDatabase::class.java, "recipe_book.db").build()
    }

    override val recipeRepository: RecipeRepository by lazy {
        RoomRecipeRepository(database.recipeDao(), applicationScope)
    }
}
```

That's **manual dependency injection**. You've been a DI expert for 7 chapters! 🎓😎

### So what's the problem? 😓

It works — but look at what we write again and again:

**1. A factory for every ViewModel** 🏭

```kotlin
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
```

10 screens = 10 of these. Boring, and easy to get wrong. 😴

**2. The container keeps growing** 📈 — every new repository, DAO, API, or helper must be added **by hand**, in the right **order**.

**3. Mistakes appear late** 💥 — forget `android:name` in the manifest, or a cast (`as RecipeBookApplication`) to the wrong class → the app **crashes** when it runs.

In a small app, that's fine. In a real app with **50 screens** and **30 repositories**… 😱 That's why most professional Android apps use a DI **library**.

---

## 23.3 Meet Hilt 🤖

**Hilt** is Google's DI library for Android. It's built on top of an older, very powerful library called **Dagger** 🗡️ (Hilt = the **handle** of the dagger — easier to hold! 😄).

Think of Hilt as a **robot** 🤖 that **builds your AppContainer for you**:

1. You put **labels** (annotations) on your classes: "*this can be built*", "*this needs that*".
2. While building your app, Hilt (using **KSP**, like Room!) **reads** the labels.
3. It **writes** all the wiring code: containers, factories, everything. 🪄
4. If something is **missing**, the **build fails** with a message — **before** the app runs. 🛡️

| | Manual DI (AppContainer) 🧰 | Hilt 🤖 |
|---|---|---|
| Who writes the wiring? | **You** | **Hilt** (generated code) |
| ViewModel factories | One per ViewModel 🏭 | **None!** `hiltViewModel()` |
| Missing dependency | 💥 Crash at **run** time (or a red error, if you're lucky) | ❌ **Build** error with a clear message |
| Good for | Small apps, learning | Real apps of any size |
| Learning curve | Easy | A few new words (this chapter!) |

> 💡 **Why did we learn manual DI first?** Because Hilt is **just** an automatic AppContainer. Now that you understand **what** it does, Hilt's labels will make sense instead of feeling like magic. 🧠

---

## 23.4 The Hilt Words 🏷️

Here are **all** the labels you'll use in this chapter. Don't memorize them now — just look back here when you need to. 📌

| Label | Goes on… | Meaning | Restaurant version 🍕 |
|---|---|---|---|
| **`@HiltAndroidApp`** | Your `Application` class | "Hilt, **start** here — build the app-wide container." | Opening the restaurant 🏪 |
| **`@AndroidEntryPoint`** | Your `Activity` | "Hilt, this Activity may **receive** things." | A door where deliveries arrive 🚪 |
| **`@Inject constructor(...)`** | A class's constructor | "Hilt, you **can build** this class — here's what it needs." | A recipe card: "chef needs: oven" 📋 |
| **`@HiltViewModel`** | A ViewModel | "Hilt, this ViewModel is yours to build." | — |
| **`hiltViewModel()`** | In a Composable | Get the ViewModel — **no factory**! | — |
| **`@Module`** + **`@InstallIn(...)`** | An `object` or abstract class | "Here are **instructions** for things you can't build alone." | The instruction **book** 📖 |
| **`@Provides`** | A function in a module | "To get **this**, run **this** function." | "To get pizza dough: mix flour + water" 🥣 |
| **`@Binds`** | An abstract function in a module | "When someone asks for the **interface**, give **this** class." | "When someone asks for 'an oven', give the **gas** oven" 🔥 |
| **`@Singleton`** | A class or `@Provides` function | "Make **only one** in the whole app, and share it." | **One** oven for the whole kitchen |
| **`@ApplicationContext`** | A `Context` parameter | "Give me the **Application** context (safe to keep)." | — |

---

## 23.5 Setting Up Hilt 📦

We'll convert the **Recipe Book** (with Room, from Chapter 22). Open it. It already has **KSP** (for Room) — Hilt uses KSP too. 🎉

### `gradle/libs.versions.toml`

```toml
[versions]
hilt = "2.56.2"
hiltNavigationCompose = "1.2.0"

[libraries]
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-android-compiler = { group = "com.google.dagger", name = "hilt-android-compiler", version.ref = "hilt" }
androidx-hilt-navigation-compose = { group = "androidx.hilt", name = "hilt-navigation-compose", version.ref = "hiltNavigationCompose" }

[plugins]
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
```

### `build.gradle.kts (Project: ...)` — the top-level file

```kotlin
plugins {
    // ... existing lines (including ksp from Chapter 22) ...
    alias(libs.plugins.hilt) apply false
}
```

### `build.gradle.kts (Module :app)`

```kotlin
plugins {
    // ... existing lines (including ksp) ...
    alias(libs.plugins.hilt)
}

dependencies {
    // ... existing lines ...
    implementation(libs.hilt.android)
    ksp(libs.hilt.android.compiler)
    implementation(libs.androidx.hilt.navigation.compose)
}
```

**Sync Now** 🔄 ✅

| Library | What it does |
|---|---|
| `hilt-android` | Hilt itself, inside your app. |
| `ksp(hilt-android-compiler)` | The **robot** 🤖 that writes the wiring code while building. |
| `hilt-navigation-compose` | Gives you **`hiltViewModel()`** for Compose (works with Navigation too). |
| plugin `com.google.dagger.hilt.android` | Connects Hilt to the Android build. |

> ⚠️ If the build fails with a strange KSP or Kotlin version error, check **two** things: (1) your KSP version fits your Kotlin version (Chapter 22's table); (2) try a **newer** Hilt version — Android Studio shows newer ones with a yellow hint.

---

## 23.6 Step 1: The Application — `@HiltAndroidApp` 🏪

### `RecipeBookApplication.kt` — before

```kotlin
class RecipeBookApplication : Application() {

    lateinit var container: AppContainer

    override fun onCreate() {
        super.onCreate()
        container = DefaultAppContainer(context = this)
    }
}
```

### After ✂️

```kotlin
package com.example.recipebook

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp                                         // (1)
class RecipeBookApplication : Application()             // (2)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `@HiltAndroidApp` | "Hilt, **start here**." Hilt creates the **app-wide container** (it calls it the `SingletonComponent`) when the Application starts. 🏪 |
| 2 | `class RecipeBookApplication : Application()` | Empty! No `container`, no `onCreate`. Hilt does it. ✨ |

The manifest **already** has `android:name=".RecipeBookApplication"` (Chapter 16). Keep it — Hilt needs it! ✅

---

## 23.7 Step 2: The Activity — `@AndroidEntryPoint` 🚪

### `MainActivity.kt`

```kotlin
package com.example.recipebook

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.recipebook.ui.navigation.RecipeBookNavHost
import com.example.recipebook.ui.theme.RecipeBookTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint                                      // 👈 the only change
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

`@AndroidEntryPoint` = "Hilt, this Activity is a **door** 🚪 — things (like ViewModels) may be delivered here." Without it, `hiltViewModel()` can't work in this Activity's screens.

---

## 23.8 Step 3: Teaching Hilt to Build Things 📋

Hilt needs to know **how to build** every piece in our chain:

```
ViewModels ──▶ RecipeRepository ──▶ RoomRecipeRepository ──▶ RecipeDao + CoroutineScope
                  (interface!)                                    │
                                                              RecipeDatabase ──▶ Context
```

There are **two ways** to teach Hilt:

| Way | When | Example |
|---|---|---|
| **`@Inject constructor`** on the class | It's **your** class, and Hilt can build everything it needs | `RoomRecipeRepository` |
| A **module** (`@Provides` / `@Binds`) | It's **not your** class, it's built with a **builder**, or it's an **interface** | `RecipeDatabase` (Room builds it), `CoroutineScope`, `RecipeRepository` (an interface) |

### Way 1: `@Inject constructor` — `data/RoomRecipeRepository.kt`

Only the **first lines** change:

```kotlin
package com.example.recipebook.data

import com.example.recipebook.data.local.RecipeDao
// ... the other imports stay ...
import javax.inject.Inject
import javax.inject.Singleton

@Singleton                                                              // (1)
class RoomRecipeRepository @Inject constructor(                         // (2)
    private val recipeDao: RecipeDao,                                   // (3)
    private val scope: CoroutineScope
) : RecipeRepository {

    // ... everything inside stays EXACTLY the same ...
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `@Singleton` | "Make **only one** `RoomRecipeRepository` for the whole app." Important: all screens must share the **same** repository (and the same `stateIn` list)! |
| 2 | `@Inject constructor(...)` | "Hilt, you **can build** this class with this constructor." In Kotlin, to put a label on the main constructor, we must write the word `constructor`. |
| 3 | `recipeDao`, `scope` | "To build me, you need a `RecipeDao` and a `CoroutineScope`." Hilt will find them — or **complain while building** if it can't. 🛡️ |

### Way 2a: `@Provides` — things Hilt can't build alone

Hilt can't build a `RecipeDatabase` by itself — **Room's builder** makes it. So we write the instructions in a **module**. Make a package **`di`** (it already exists — delete the old `AppContainer.kt` from it!) and create:

### `di/DatabaseModule.kt`

```kotlin
package com.example.recipebook.di

import android.content.Context
import androidx.room.Room
import com.example.recipebook.data.local.RecipeDao
import com.example.recipebook.data.local.RecipeDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module                                                                 // (1)
@InstallIn(SingletonComponent::class)                                   // (2)
object DatabaseModule {

    @Provides                                                           // (3)
    @Singleton                                                          // (4)
    fun provideRecipeDatabase(
        @ApplicationContext context: Context                            // (5)
    ): RecipeDatabase =
        Room.databaseBuilder(context, RecipeDatabase::class.java, "recipe_book.db").build()

    @Provides
    fun provideRecipeDao(database: RecipeDatabase): RecipeDao =         // (6)
        database.recipeDao()
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `@Module` | "This is an **instruction book** 📖 for Hilt." |
| 2 | `@InstallIn(SingletonComponent::class)` | "These instructions are for the **app-wide** container" (the one that lives as long as the app). |
| 3 | `@Provides` | "When someone needs a **`RecipeDatabase`** (the **return type**!), run this function." Hilt looks at the return type — the function **name** doesn't matter (but `provideXxx` is the habit). |
| 4 | `@Singleton` | Build the database **only once**. 🏛️ (Very important — Chapter 22!) |
| 5 | `@ApplicationContext context: Context` | "Hilt, give me the **Application** context." Hilt already knows how. ✅ |
| 6 | `provideRecipeDao(database: RecipeDatabase)` | To get a `RecipeDao`, Hilt needs a `RecipeDatabase` — which it knows from the function above! It **chains** them automatically. ⛓️ |

### `di/CoroutinesModule.kt`

```kotlin
package com.example.recipebook.di

import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object CoroutinesModule {

    @Provides
    @Singleton
    fun provideApplicationScope(): CoroutineScope =
        CoroutineScope(SupervisorJob() + Dispatchers.Default)
}
```

The **same** app-wide scope as the AppContainer had (Chapter 22) — now built by Hilt, **once**.

> ℹ️ Hilt finds things by their **type**. There's only **one** `CoroutineScope` in our app, so that's fine. If you ever need **two** different things of the **same** type (for example two scopes), Hilt needs extra labels called **qualifiers** — an advanced topic for later.

### Way 2b: `@Binds` — connecting an interface to a class 🔌

The ViewModels ask for a **`RecipeRepository`** — an **interface**. Hilt can't build an interface (it's just a promise!). We must say **which class** keeps the promise.

### `di/RepositoryModule.kt`

```kotlin
package com.example.recipebook.di

import com.example.recipebook.data.RecipeRepository
import com.example.recipebook.data.RoomRecipeRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {                                       // (1)

    @Binds                                                              // (2)
    abstract fun bindRecipeRepository(
        impl: RoomRecipeRepository                                      // (3)
    ): RecipeRepository                                                 // (4)
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `abstract class RepositoryModule` | `@Binds` functions have **no body**, so the module must be **abstract** (Chapter 22's "unfinished class" — Hilt finishes it). |
| 2 | `@Binds` | "When someone asks for the **return type**…" |
| 3 | `impl: RoomRecipeRepository` | "…give them **this** class." (Hilt knows how to build it — `@Inject constructor`!) |
| 4 | `: RecipeRepository` | The **interface** people ask for. |

🔁 **This is the new "one line"!** Remember Chapter 22: swapping `InMemoryRecipeRepository` ⇄ `RoomRecipeRepository` was **one line** in the AppContainer. Now it's **one line** here: the parameter type of `bindRecipeRepository`. The promise still holds! 🤝

> 🤔 **`@Provides` or `@Binds`?**
> - `@Binds` → "interface ➡️ class", when Hilt **can** build the class (it has `@Inject constructor`). Short and fast. ⚡
> - `@Provides` → anything that needs **your code** to build it (builders, `Room...build()`, `Retrofit.Builder()...`, scopes).

---

## 23.9 Step 4: ViewModels — `@HiltViewModel` 🧠

### `ui/detail/RecipeDetailViewModel.kt` — the easy one

**Before** (Chapter 16):

```kotlin
class RecipeDetailViewModel(
    savedStateHandle: SavedStateHandle,
    private val repository: RecipeRepository
) : ViewModel() {
    // ...
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

**After** ✂️:

```kotlin
package com.example.recipebook.ui.detail

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.navigation.toRoute
import com.example.recipebook.data.RecipeRepository
import com.example.recipebook.data.model.Recipe
import com.example.recipebook.ui.navigation.RecipeDetail
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import javax.inject.Inject

data class RecipeDetailUiState(
    val recipe: Recipe? = null,
    val notFound: Boolean = false
)

@HiltViewModel                                                       // (1)
class RecipeDetailViewModel @Inject constructor(                     // (2)
    savedStateHandle: SavedStateHandle,                              // (3)
    private val repository: RecipeRepository                         // (4)
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
}                                                                    // (5)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `@HiltViewModel` | "Hilt, this ViewModel is **yours** to build." |
| 2 | `@Inject constructor(...)` | "…and here's what it needs." |
| 3 | `savedStateHandle: SavedStateHandle` | Hilt gives **every** `@HiltViewModel` its `SavedStateHandle` **automatically** — with the route's arguments inside. `toRoute<RecipeDetail>()` still works! ✅ |
| 4 | `repository: RecipeRepository` | Hilt looks it up: "`RecipeRepository`? → `@Binds` says `RoomRecipeRepository` → needs `RecipeDao` + `CoroutineScope` → …" and builds the whole chain. 🤖⛓️ |
| 5 | (no `companion object`!) | **The factory is gone.** 🎉 ✂️ |

### `RecipeDetailRoute` — use `hiltViewModel()`

```kotlin
import androidx.hilt.navigation.compose.hiltViewModel

@Composable
fun RecipeDetailRoute(
    onBack: () -> Unit,
    viewModel: RecipeDetailViewModel = hiltViewModel()            // 👈 was viewModel(factory = ...)
) {
    // ... unchanged ...
}
```

`hiltViewModel()` works like `viewModel()` (Chapter 15): the **same** ViewModel after rotation, a new one for a new screen, cleared when the screen leaves the back stack. The only difference: **Hilt builds it**, so no factory is needed. 🏭❌

---

## 23.10 Step 5: Assisted Injection — Values From the Screen 🎁

Now the **list** ViewModel. It's trickier:

```kotlin
class RecipeListViewModel(
    private val repository: RecipeRepository,
    private val onlyFavorites: Boolean                    // 🤔 who gives this?
) : ViewModel()
```

The **repository** comes from Hilt. But **`onlyFavorites`**? Hilt has no idea! It's not something you "build" — it comes from the **screen**: the Recipes tab says `false`, the Favorites tab says `true`.

Some values come from **Hilt**, and one from **us**. This is called **assisted injection** — "Hilt does most of the work, and **we assist** with the rest." 🤝

### `ui/list/RecipeListViewModel.kt`

```kotlin
package com.example.recipebook.ui.list

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.recipebook.data.RecipeRepository
import com.example.recipebook.data.model.Recipe
import dagger.assisted.Assisted
import dagger.assisted.AssistedFactory
import dagger.assisted.AssistedInject
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn

data class RecipeListUiState(
    val recipes: List<Recipe> = emptyList(),
    val isLoading: Boolean = true
)

@HiltViewModel(assistedFactory = RecipeListViewModel.Factory::class)        // (1)
class RecipeListViewModel @AssistedInject constructor(                       // (2)
    private val repository: RecipeRepository,                                // (3) from Hilt
    @Assisted private val onlyFavorites: Boolean                             // (4) from us
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

    @AssistedFactory                                                         // (5)
    interface Factory {
        fun create(onlyFavorites: Boolean): RecipeListViewModel
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `@HiltViewModel(assistedFactory = RecipeListViewModel.Factory::class)` | "Hilt, you build this ViewModel — but use **this factory** to get the extra value." |
| 2 | `@AssistedInject constructor` | Like `@Inject`, but some values will be **given by us**. |
| 3 | `repository` (no label) | Hilt provides this one, like before. 🤖 |
| 4 | `@Assisted onlyFavorites` | "**We** will provide this one." 🙋 |
| 5 | `@AssistedFactory interface Factory` | A tiny **interface** with one function: "give me `onlyFavorites`, I give you the ViewModel." Hilt **writes** the code inside it. We only write the header. |

### `RecipeListRoute` — pass the value

```kotlin
import androidx.hilt.navigation.compose.hiltViewModel

@Composable
fun RecipeListRoute(
    title: String,
    emptyText: String,
    onlyFavorites: Boolean,
    onRecipeClick: (Int) -> Unit,
    viewModel: RecipeListViewModel =
        hiltViewModel<RecipeListViewModel, RecipeListViewModel.Factory>(       // (1)
            creationCallback = { factory -> factory.create(onlyFavorites) }    // (2)
        )
) {
    // ... unchanged ...
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `hiltViewModel<RecipeListViewModel, RecipeListViewModel.Factory>(...)` | Two types in `< >`: **which** ViewModel, and **which** assisted factory. |
| 2 | `creationCallback = { factory -> factory.create(onlyFavorites) }` | "When the ViewModel must be **created**, here's how: call `create` with **our** value." Used only the **first** time — after rotation you get the **same** ViewModel. ✅ |

> 💡 In Chapter 16 we also passed `key = ...` to keep the two tabs' ViewModels apart. Each tab is its **own** back-stack entry, so each one already gets its **own** ViewModel — the key isn't needed. (Adding `key = ...` is still allowed.)

> 💡 **When do you need assisted injection?** Only when a ViewModel needs a value that comes from the **UI** and **isn't** in the route. Values that **are** in the route → just read them from `SavedStateHandle` (like the Detail ViewModel). That's the more common case. 🙂

---

## 23.11 Step 6: Clean Up and Run 🧹

Delete what Hilt replaced:

| Delete | Why |
|---|---|
| `di/AppContainer.kt` (`AppContainer` + `DefaultAppContainer`) | Hilt **is** the container now 🤖 |
| `companion object { val Factory ... }` in every ViewModel | `hiltViewModel()` needs no factory |
| Unused imports (`APPLICATION_KEY`, `viewModelFactory`, `initializer`, …) | **Code → Optimize Imports** (Ctrl + Alt + O) cleans them all 🧽 |

**Build** (🔨 **Build → Make Project**). If something is missing, Hilt tells you **now** (see 23.15).

**Run it!** ▶️ The app works **exactly** like before — favorites, tabs, details, saved in Room. 🎉 But look at what disappeared:

| | Before (manual DI) | After (Hilt) |
|---|---|---|
| `AppContainer.kt` | ~25 lines | **deleted** ✂️ |
| `RecipeBookApplication` | ~10 lines | **2 lines** |
| ViewModel factories | ~12 lines each | **0** ✂️ |
| `as RecipeBookApplication` casts | in every factory | **0** |
| Missing dependency | crash at run time 💥 | **build** error 🛡️ |

And here's how Hilt sees our app — it built this **map** all by itself 🗺️:

```
@HiltAndroidApp RecipeBookApplication
   └── SingletonComponent (app-wide container) 🏪
         ├── RecipeDatabase      ◀── @Provides @Singleton (DatabaseModule)
         ├── RecipeDao           ◀── @Provides (needs RecipeDatabase)
         ├── CoroutineScope      ◀── @Provides @Singleton (CoroutinesModule)
         ├── RoomRecipeRepository◀── @Inject constructor, @Singleton (needs RecipeDao, CoroutineScope)
         └── RecipeRepository    ◀── @Binds → RoomRecipeRepository

@AndroidEntryPoint MainActivity 🚪
   └── screens ── hiltViewModel() ──▶ @HiltViewModel RecipeDetailViewModel (needs SavedStateHandle, RecipeRepository)
                                     @HiltViewModel RecipeListViewModel (needs RecipeRepository + @Assisted onlyFavorites)
```

---

## 23.12 Hilt for Retrofit — Converting the Joke Machine 😂📡

Let's practice once more with the **Joke Machine** (Chapter 19). Its AppContainer built `Json`, `Retrofit`, the API service, and the repository. Each becomes a Hilt instruction.

**Setup:** Hilt needs **KSP**. The Joke Machine doesn't have it yet → add KSP (Chapter 22, section 22.5 — but **without** the Room lines), then the Hilt setup (23.5). **Sync**. 🔄

### 1. Application and Activity

```kotlin
@HiltAndroidApp
class JokeMachineApplication : Application()
```

```kotlin
@AndroidEntryPoint
class MainActivity : ComponentActivity() { /* unchanged */ }
```

### 2. `di/NetworkModule.kt`

```kotlin
package com.example.jokemachine.di

import com.example.jokemachine.data.network.JokeApiService
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    private const val BASE_URL = "https://official-joke-api.appspot.com/"

    @Provides
    @Singleton
    fun provideJson(): Json = Json { ignoreUnknownKeys = true }                 // (1)

    @Provides
    @Singleton
    fun provideRetrofit(json: Json): Retrofit =                                 // (2)
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
            .build()

    @Provides
    @Singleton
    fun provideJokeApiService(retrofit: Retrofit): JokeApiService =             // (3)
        retrofit.create(JokeApiService::class.java)
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `provideJson()` | "To get a `Json`, run this." Only once. |
| 2 | `provideRetrofit(json: Json)` | Needs a `Json` → Hilt uses function **(1)**. ⛓️ |
| 3 | `provideJokeApiService(retrofit: Retrofit)` | Needs a `Retrofit` → Hilt uses function **(2)**. ⛓️ Retrofit itself is built **only once** (Chapter 19's rule ✅). |

### 3. The repository

```kotlin
@Singleton
class NetworkJokesRepository @Inject constructor(
    private val apiService: JokeApiService
) : JokesRepository {
    // ... unchanged ...
}
```

### 4. `di/RepositoryModule.kt`

```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    abstract fun bindJokesRepository(impl: NetworkJokesRepository): JokesRepository
}
```

### 5. The ViewModel

```kotlin
@HiltViewModel
class JokesViewModel @Inject constructor(
    private val repository: JokesRepository
) : ViewModel() {
    // ... unchanged, but DELETE the companion object Factory ...
}
```

### 6. The Route

```kotlin
@Composable
fun JokesRoute(
    viewModel: JokesViewModel = hiltViewModel()
) { /* unchanged */ }
```

Delete `AppContainer.kt`. **Run** → jokes! 😂 Same app, less wiring. 🎉

> 🎯 **The pattern is always the same:**
> 1. `@HiltAndroidApp` on the Application, `@AndroidEntryPoint` on the Activity.
> 2. Your own classes → `@Inject constructor` (+ `@Singleton` if there must be only one).
> 3. Builder-made things (Retrofit, Room, Json, scopes) → `@Provides` in a module.
> 4. Interfaces → `@Binds` in a module.
> 5. ViewModels → `@HiltViewModel` + `@Inject constructor`, and `hiltViewModel()` in the Route.

---

## 23.13 Scopes — "Only One" or "A New One Every Time"? 🔢

By default, Hilt builds a **new** object **every time** one is needed. A label like `@Singleton` changes that.

| Label | How many? | Lives as long as… | Use for |
|---|---|---|---|
| *(no label)* | A **new** one each time it's needed | whoever received it | Small, cheap helpers with no state (like a DAO — Room gives the same one anyway) |
| **`@Singleton`** | **One** for the whole app | the **app** | Database, Retrofit, `Json`, repositories, app scope ⭐ |
| `@ActivityRetainedScoped` | One per Activity (survives rotation) | the Activity's "logical" life | Rarely needed in Compose apps |
| `@ViewModelScoped` | One per ViewModel | that ViewModel | A helper shared by things inside **one** ViewModel |

> ⚠️ **The most common scope mistake:** forgetting `@Singleton` on a repository that **holds data** (like `InMemoryRecipeRepository` or our `stateIn` list). Without it, each ViewModel gets its **own** repository → tapping ♥ in the list doesn't update the detail screen! 😵 The "single source of truth" breaks. Rule: **repositories → `@Singleton`**.

> ⚠️ **The opposite mistake:** putting a short-lived thing (like an `Activity`) into a `@Singleton` → memory leak 💧. That's why we use **`@ApplicationContext`**, never an Activity, in app-wide modules.

---

## 23.14 What About Testing? 🧪

DI's biggest gift: you can **swap** pieces. 🔌 The ViewModel constructors **didn't change** — they still receive a `RecipeRepository`. So in a test (Chapter 27), you can still write:

```kotlin
val viewModel = RecipeDetailViewModel(
    savedStateHandle = SavedStateHandle(/* ... */),
    repository = FakeRecipeRepository()         // 🧪 a fake, no database needed
)
```

**No Hilt needed in simple tests** — just call the constructor! For bigger tests, Hilt also has tools to replace a whole module with a fake one (`@TestInstallIn`). We'll see testing in **Chapter 27**.

---

## 23.15 Reading Hilt's Error Messages 😌

Hilt errors appear when you **build**, in the **Build** window at the bottom. They look scary, but they're actually **helpful**. Find the line that starts with **`[Dagger/...]`** or **`error:`** and read it slowly.

### Error 1: Missing binding 🔍

```
error: [Dagger/MissingBinding] com.example.recipebook.data.RecipeRepository cannot be provided
without an @Provides-annotated method.
    com.example.recipebook.data.RecipeRepository is injected at
        com.example.recipebook.ui.detail.RecipeDetailViewModel(…, repository)
```

**In simple words:** "The `RecipeDetailViewModel` needs a `RecipeRepository`, but nobody told me how to make one!" 🤷

**Fix:** a `@Binds` (for an interface) or `@Provides` function, or `@Inject constructor` on the class. Here: the `RepositoryModule` is missing or has a typo.

> 💡 The bottom lines show the **path**: "*X is injected at Y*" → you can see **who** asked for the missing piece. 🗺️

### Error 2: The Application isn't a Hilt app 🏪

```
Hilt Activity must be attached to an @HiltAndroidApp Application.
```

**Fix:** add `@HiltAndroidApp` to your Application class, **and** check `android:name=".RecipeBookApplication"` is in the manifest.

### Error 3: The Activity isn't an entry point 🚪

The app crashes when a screen calls `hiltViewModel()`, with a message mentioning **`@AndroidEntryPoint`** or *"…does not implement interface dagger.hilt.internal.GeneratedComponent…"*.

**Fix:** add `@AndroidEntryPoint` to `MainActivity`.

### Error 4: Two ways to make the same thing 👯

```
error: [Dagger/DuplicateBindings] com.example.recipebook.data.RecipeRepository is bound multiple times
```

**In simple words:** "You gave me **two** instructions for `RecipeRepository`. Which one?!" 🤔

**Fix:** keep only **one** `@Binds`/`@Provides` for each type (for example, you left an old module behind).

### Error 5: A ViewModel created the old way 🏭

```
java.lang.RuntimeException: Cannot create an instance of class ...RecipeDetailViewModel
```

**Fix:** you used `viewModel()` for a `@HiltViewModel`. Use **`hiltViewModel()`**. (And for assisted ViewModels: `hiltViewModel<VM, VM.Factory>(creationCallback = ...)`.)

---

## 23.16 Test Checklist ✅

| Test | Expected | ✓ |
|---|---|---|
| **Build** the Recipe Book | No errors | ☐ |
| Run | Same app as before: 6 recipes, tabs work | ☐ |
| ♥ in the list | Favorites tab updates (one shared `@Singleton` repository ✅) | ☐ |
| ♥ in the detail | List updates | ☐ |
| Rotate on any screen 🔄 | Same ViewModels, nothing reloads | ☐ |
| Close and reopen the app | Favorites remembered (Room 💾) | ☐ |
| Remove `@Singleton` from `RoomRecipeRepository`, run | Still works? Try ♥ in list, then open details… (see Practice Task 1!) Then put it back. | ☐ |
| Remove the `@Binds` function, build | `[Dagger/MissingBinding]` error. Put it back. | ☐ |
| Joke Machine with Hilt | Jokes load, retry works | ☐ |

---

## 23.17 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| Forgot `@HiltAndroidApp` | Crash: *Hilt Activity must be attached to an @HiltAndroidApp Application* | Add it to the Application class. |
| Forgot `android:name` in the manifest | Same crash | `android:name=".YourApplication"` |
| Forgot `@AndroidEntryPoint` | Crash when using `hiltViewModel()` | Add it to the Activity. |
| `viewModel()` instead of `hiltViewModel()` | *Cannot create an instance of class …* | `hiltViewModel()` |
| Forgot `@HiltViewModel` or `@Inject constructor` on a ViewModel | Build or run error | Both are needed. |
| Missing `@Binds` / `@Provides` | `[Dagger/MissingBinding]` | Teach Hilt how to build it. |
| Two bindings for the same type | `[Dagger/DuplicateBindings]` | Keep one. |
| `@Binds` in an `object` | Error: @Binds methods must be abstract | Put `@Binds` in an **abstract class**. |
| `@Provides` in an abstract class without a body | Error | `@Provides` functions need a **body** → use an `object` module. |
| No `@Singleton` on a repository that holds data | Screens don't see each other's changes | `@Singleton` on the class. |
| Database or Retrofit not `@Singleton` | Many copies, slow, file conflicts | `@Singleton` on the `@Provides` function. |
| Injecting an Activity `Context` into a singleton | 💧 Memory leak | `@ApplicationContext` |
| `ksp(...)` vs `implementation(...)` mixed up | Generated code missing | `implementation(hilt-android)`, `ksp(hilt-android-compiler)` |
| Hilt + KSP version problems | Strange build errors | KSP fits Kotlin (Ch. 22 table); try a newer Hilt. |
| Assisted ViewModel with plain `hiltViewModel()` | Error about the assisted factory | `hiltViewModel<VM, VM.Factory>(creationCallback = { it.create(...) })` |

---

## 23.18 Summary — What You Learned 🎓

✅ A **dependency** is something a class **needs**. **Dependency injection** = **receiving** it from outside (usually through the constructor) instead of creating it. 💉

✅ The **AppContainer** was **manual DI**. It works, but needs factories, casts, and hand-wiring — and mistakes show up at **run** time.

✅ **Hilt** 🤖 writes the wiring for you at **build** time (with KSP) and reports missing pieces as **build errors**. 🛡️

✅ **Start:** `@HiltAndroidApp` on the Application, `@AndroidEntryPoint` on the Activity.

✅ **Your classes:** `@Inject constructor(...)`. **Builder-made things:** `@Provides` in an `@Module @InstallIn(SingletonComponent::class) object`. **Interfaces:** `@Binds` in an **abstract class** module.

✅ **`@Singleton`** = one for the whole app: database, Retrofit, `Json`, repositories, app scope. `@ApplicationContext` for a safe Context.

✅ **ViewModels:** `@HiltViewModel` + `@Inject constructor`; `SavedStateHandle` comes free; get them with **`hiltViewModel()`** — **no factories**. ✂️🏭

✅ **Assisted injection** (`@AssistedInject`, `@Assisted`, `@AssistedFactory`, `creationCallback`) for values that come from the **screen**.

✅ Read Hilt errors calmly: `[Dagger/MissingBinding]` = "I don't know how to build X" — and the path shows **who** needed it. 🗺️

✅ You converted the **Recipe Book** and the **Joke Machine** to Hilt — same apps, less code, safer wiring! 🎉

---

## 23.19 Practice Time 🏋️

**Task 1 — The missing `@Singleton` 🕵️:**
Remove `@Singleton` from `RoomRecipeRepository`. Run the Recipe Book, tap ♥ on a recipe in the list, then open its detail screen. Does it still work? Why — or why not? (Think carefully: where is the **real** data stored now?) Put `@Singleton` back afterwards.

**Task 2 — Back to memory 🧠:**
Make the Recipe Book use **`InMemoryRecipeRepository`** again — by changing only the `RepositoryModule` and the `InMemoryRecipeRepository` class.
*Hint:* Hilt can't use default parameter values. Give `InMemoryRecipeRepository` a **second** constructor with `@Inject`.

**Task 3 — Convert the Dog Gallery 🐶:**
Convert the **Dog Gallery** (Chapter 20) to Hilt. Write the `NetworkModule`. Careful: the base URL is different, and the Application class **also** implements `SingletonImageLoader.Factory` for Coil — does that still work with `@HiltAndroidApp`?

**Task 4 — Read the error 🔍:**
What's wrong, and how do you fix it?

```
error: [Dagger/MissingBinding] com.example.shoppinglist.data.ShoppingItemDao cannot be provided
without an @Provides-annotated method.
    com.example.shoppinglist.data.ShoppingItemDao is injected at
        com.example.shoppinglist.data.RoomShoppingRepository(dao)
```

**Task 5 — Find the 3 bugs 🐛🐛🐛:**

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Binds
    abstract fun bindNotesRepository(impl: RoomNotesRepository): NotesRepository

    @Provides
    fun provideDatabase(context: Context): NotesDatabase =
        Room.databaseBuilder(context, NotesDatabase::class.java, "notes.db").build()
}
```

**Task 6 — Convert the Shopping List 🛒:**
Convert the **Shopping List** (Chapter 22) to Hilt from start to finish. Write every file that changes.

---

### Answers

**Task 1:**

It **still works**! 😮 Why? Without `@Singleton`, each ViewModel gets its **own** `RoomRecipeRepository` object — but they all read and write the **same database** (the `RecipeDatabase` is still `@Singleton`). When the list toggles ♥, Room's Flow tells **every** repository's `observeAll()` → all screens update. 🪄

**But** there are hidden costs: each repository runs its **own** `stateIn(Eagerly)` (several copies of the list in memory, forever 🐘) and its own seeding check in `init`. So keep `@Singleton`.

And with **`InMemoryRecipeRepository`** (Task 2), forgetting `@Singleton` **would** break the app — each copy has its **own** list in memory, so a ♥ in one screen never reaches another. 😵 **Repositories → `@Singleton`**, always.

**Task 2:**

```kotlin
@Singleton
class InMemoryRecipeRepository(
    initialRecipes: List<Recipe>
) : RecipeRepository {

    @Inject constructor() : this(sampleRecipes)       // 👈 Hilt uses this one

    // ... everything else unchanged ...
}
```

```kotlin
@Binds
abstract fun bindRecipeRepository(impl: InMemoryRecipeRepository): RecipeRepository
```

⚠️ Notice we **removed** the default value `= sampleRecipes` from the main constructor. If we kept it, Kotlin would already make a no-parameter constructor, and the two would clash.

💡 `@Inject constructor() : this(sampleRecipes)` = a **secondary constructor** with **no** parameters (so Hilt needs nothing), which calls the main constructor with the sample data. Tests can still use the main one with their own list. 🧪

(Note: with the in-memory repository, the `RecipeDatabase`/`RecipeDao` instructions are simply **not used** — Hilt only builds what someone actually needs.)

**Task 3:**

```kotlin
@HiltAndroidApp
class DogGalleryApplication : Application(), SingletonImageLoader.Factory {
    override fun newImageLoader(context: PlatformContext): ImageLoader =
        ImageLoader.Builder(context).crossfade(true).build()
}
```

✅ Yes, it works: `@HiltAndroidApp` doesn't care what **else** your Application implements.

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides @Singleton
    fun provideJson(): Json = Json { ignoreUnknownKeys = true }

    @Provides @Singleton
    fun provideRetrofit(json: Json): Retrofit = Retrofit.Builder()
        .baseUrl("https://dog.ceo/api/")
        .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
        .build()

    @Provides @Singleton
    fun provideDogApiService(retrofit: Retrofit): DogApiService =
        retrofit.create(DogApiService::class.java)
}

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    abstract fun bindDogPhotosRepository(impl: NetworkDogPhotosRepository): DogPhotosRepository
}
```

Plus: `@Singleton class NetworkDogPhotosRepository @Inject constructor(private val apiService: DogApiService)`, `@AndroidEntryPoint` on `MainActivity`, `@HiltViewModel class GalleryViewModel @Inject constructor(...)` without the factory, and `hiltViewModel()` in `GalleryRoute`. 🐶

💡 `@Provides @Singleton` on **one** line is fine — labels can share a line.

**Task 4:**

"`RoomShoppingRepository` needs a `ShoppingItemDao`, but Hilt doesn't know how to make one." A DAO comes **from the database**, so add a `@Provides` function:

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides @Singleton
    fun provideDatabase(@ApplicationContext context: Context): ShoppingDatabase =
        Room.databaseBuilder(context, ShoppingDatabase::class.java, "shopping.db").build()

    @Provides
    fun provideShoppingItemDao(database: ShoppingDatabase): ShoppingItemDao =
        database.shoppingItemDao()
}
```

**Task 5:**

| # | Bug | Fix |
|---|---|---|
| 1 | **`@Binds` in an `object`** — `@Binds` functions must be **abstract**, and an `object` can't have abstract functions. | Move it to a separate `abstract class RepositoryModule`. |
| 2 | `context: Context` **without `@ApplicationContext`** → Hilt doesn't know which Context → `[Dagger/MissingBinding] android.content.Context…` | `@ApplicationContext context: Context` |
| 3 | The database has **no `@Singleton`** → a **new** database for every user of it! 💥 | `@Provides @Singleton` |

**Task 6:**

1. KSP is already there (Room). Add Hilt (23.5).
2. `@HiltAndroidApp class ShoppingApplication : Application()`
3. `@AndroidEntryPoint class MainActivity ...`
4. `di/DatabaseModule.kt` — exactly as in Task 4's answer.
5. `data/RoomShoppingRepository.kt`:

```kotlin
@Singleton
class RoomShoppingRepository @Inject constructor(
    private val dao: ShoppingItemDao
) : ShoppingRepository { /* unchanged */ }
```

6. `di/RepositoryModule.kt`:

```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    abstract fun bindShoppingRepository(impl: RoomShoppingRepository): ShoppingRepository
}
```

7. `ShoppingListViewModel`: `@HiltViewModel class ShoppingListViewModel @Inject constructor(private val repository: ShoppingRepository)` — delete the `companion object`.
8. `ShoppingListRoute(viewModel: ShoppingListViewModel = hiltViewModel())`
9. Delete `di/AppContainer.kt`. Build ✅ Run ✅ 🛒

---

## 23.20 Challenges 🚀

### Challenge 1: Convert My Space ⚙️ ⭐⭐
Convert **My Space** (Chapter 21) to Hilt. How do you provide the `DataStore<Preferences>`? (*Hint:* a `@Provides @Singleton` function that returns `context.settingsDataStore` — keep the top-level `preferencesDataStore` delegate!)

### Challenge 2: Convert the Quiz app 🧠 ⭐⭐⭐
Convert the **Quiz** app. The `QuizViewModel` needs a `SavedStateHandle` (free with Hilt!), the `QuestionRepository`, **and** the `BestScoreRepository` from Chapter 21. The `QuizNavHost` received repositories as **parameters** — how could the Start screen get best scores now? (*Idea:* a small `@HiltViewModel StartViewModel`.)

### Challenge 3: A dispatcher module 👷 ⭐⭐⭐
Instead of writing `Dispatchers.IO` inside classes, **inject** it, so tests can replace it. Search for "**Hilt qualifiers**" (`@Qualifier`) — you'll need them to tell `IO` and `Default` apart, because both have the same type (`CoroutineDispatcher`).

### Challenge 4: Draw the map 🗺️ ⭐
For the **Joke Machine**, draw (on paper!) the dependency map like the one in 23.11: which piece needs which?

---

## 23.21 What Is Next?

You now know **all** the big tools of modern Android development:

| Tool | Chapter |
|---|---|
| Jetpack Compose 🎨 | 5–11 |
| Navigation 🧭 | 13 |
| ViewModel + StateFlow 🧠 | 15 |
| MVVM + Repositories 🏗️ | 16 |
| Coroutines + Flow ⚡🌊 | 18 |
| Retrofit 📡 | 19 |
| Coil 🖼️ | 20 |
| DataStore 📝 | 21 |
| Room 🗃️ | 22 |
| Hilt 🤖 | 23 |

Time to put them **together** in one complete, real app! In **Chapter 24: 🛠️ Mini Project — Notes App**, you will:

- Plan a full app: notes list, note editor, search, colors, and pinning 📌
- Design the repository **for Room from day one** — `Flow` + `suspend` (the lesson from Chapter 22!) ✅
- Use **Room** for saving, **Hilt** for wiring, **Navigation** for screens, and **DataStore** for settings 🧩
- Add **swipe-to-delete** with **Undo** ↩️, **search** 🔍, and **sorting** ↕️
- Make it survive **everything**: rotation, process death, and closing the app 💾

**Fantastic work finishing Chapter 23! 🎉 You now wire apps like a professional! 🤖💪**
