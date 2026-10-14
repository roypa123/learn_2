# Chapter 13: Moving Between Screens — Navigation 🧭

> **What you will learn in this chapter**
>
> 1. What **navigation** is, and the **back stack** 🥞
> 2. Adding **Navigation Compose** to your project
> 3. **Routes** — the "address" of each screen 🏠
> 4. `NavHost` and `NavController` — the map and the driver 🗺️🚗
> 5. Going to a screen, and going **back** ⬅️
> 6. **Passing data** to a screen (like *which* recipe to open)
> 7. The golden rule: **don't pass the NavController around**
> 8. Controlling the back stack: `popUpTo`, `inclusive`, `launchSingleTop`
> 9. **Bottom navigation** with real screens
> 10. Hiding the bottom bar on some screens
> 11. Building a **Recipe Book** app 📖🍳
>
> **Time needed:** about 5 hours.

---

## 13.1 What Is Navigation? 🧭

Almost every app has **many screens**:

```
📋 List of recipes  ──tap──▶  📄 Recipe details  ──tap──▶  🛒 Shopping list
        ▲                            │
        └────────── Back ⬅️ ─────────┘
```

**Navigation** means:
1. **Moving** from one screen to another.
2. **Remembering** where you came from, so the **Back** button works.
3. **Passing information** between screens ("*open recipe number 7*").

### The back stack 🥞

Android remembers your screens in a **stack** — like a **pile of plates** 🍽️ or **pancakes** 🥞:

```
 Open the app         Tap a recipe          Tap "Shopping list"     Press Back ⬅️
                                            ┌───────────────┐
                      ┌───────────────┐     │ Shopping list │       ┌───────────────┐
                      │ Recipe detail │     ├───────────────┤       │ Recipe detail │
┌───────────────┐     ├───────────────┤     │ Recipe detail │       ├───────────────┤
│ Recipe list   │     │ Recipe list   │     ├───────────────┤       │ Recipe list   │
└───────────────┘     └───────────────┘     │ Recipe list   │       └───────────────┘
                                            └───────────────┘
```

| Action | What happens to the stack |
|---|---|
| **Go to** a new screen | Put a new plate **on top** (push) ⬆️ |
| Press **Back** | Take the **top** plate off (pop) ⬇️ |
| Back on the **last** plate | The app **closes** 👋 |

You always see the screen on **top** of the pile.

> 💡 Remember this picture! Everything in this chapter is about **adding** and **removing** plates. 🍽️

### Why not just use `when` like in Chapter 11?

In Chapter 11 we switched tabs with `when (selectedTab)`. That's fine for tabs, but it has **no back stack**:
- Press Back → the app **closes**, instead of going to the previous screen. 😕
- No easy way to **pass data** to a screen.
- No **deep links** (opening a screen from a notification or website link).

**Navigation Compose** solves all of this. ✅

> ℹ️ Google is also building a newer library called **Navigation 3**. **Navigation Compose** (this chapter) is the most used, fully supported, and what you'll see in most projects and tutorials today. The ideas (routes, back stack) are the same in both.

---

## 13.2 Step 1: Add Navigation to Your Project 📦

Navigation is **not** included in a new project. We need to add **two** things:

1. The **Navigation Compose** library.
2. The **Kotlin Serialization** plugin — so routes can be normal Kotlin classes (more in 13.3).

Use **MyFirstApp**, or make a new project called **Recipe Book** (package `com.example.recipebook`) — good practice! 😊

### 1. Open `gradle/libs.versions.toml`

In the **Project** window (Android view): **Gradle Scripts → libs.versions.toml**.

Add these lines in the right sections (**don't delete** what's already there):

```toml
[versions]
# ... the existing lines stay ...
navigationCompose = "2.8.9"
kotlinxSerializationJson = "1.7.3"

[libraries]
# ... the existing lines stay ...
androidx-navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigationCompose" }
kotlinx-serialization-json = { group = "org.jetbrains.kotlinx", name = "kotlinx-serialization-json", version.ref = "kotlinxSerializationJson" }

[plugins]
# ... the existing lines stay ...
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
```

| Line | Meaning |
|---|---|
| `navigationCompose = "2.8.9"` | The version of Navigation Compose. |
| `androidx-navigation-compose = {...}` | The library itself. |
| `kotlinx-serialization-json` | A Kotlin library that turns objects into text and back (we'll use it again for the internet in Chapter 19!). |
| `kotlin-serialization = {...}` | A **plugin** (an extra power for the Kotlin compiler). `version.ref = "kotlin"` → it uses the **same** version as your Kotlin. |

> ⚠️ **About version numbers:** Libraries get updates often. Newer versions are fine (and better!). Android Studio shows a **yellow highlight** when a newer version exists — you can hover and update. You can check the latest version at **https://developer.android.com/jetpack/androidx/releases/navigation**. Type-safe navigation (what we use) needs **2.8.0 or newer**.

> ⚠️ **Check your Kotlin version name:** In the `[versions]` section, find the line for Kotlin. It's usually `kotlin = "2.x.x"`. If it has a different name, use that name in `version.ref`.

### 2. Open `build.gradle.kts (Module :app)`

Add the plugin at the top and the libraries at the bottom:

```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.serialization)      // ← NEW
}

// ... android { ... } stays the same ...

dependencies {
    // ... the existing lines stay ...
    implementation(libs.androidx.navigation.compose)      // ← NEW
    implementation(libs.kotlinx.serialization.json)       // ← NEW
}
```

Remember from Chapter 1: in Gradle files, the dashes `-` in the TOML names become dots `.`.

### 3. Sync! 🔄

Click **Sync Now** in the yellow bar at the top. Wait until it finishes without red errors. ✅

> 💡 **If sync fails:** read the red message in the **Build** window. The most common problems: a typo in a name, a missing quote `"`, or a line in the wrong `[section]`.

---

## 13.3 Routes — The Address of Each Screen 🏠

Each screen needs an **address**, so we can say "*go there!*". In Navigation Compose, an address is called a **route**.

Modern Navigation uses **Kotlin classes** as routes:

```kotlin
import kotlinx.serialization.Serializable

@Serializable
object Home

@Serializable
object Settings

@Serializable
data class Profile(val userId: Int)
```

### Every bit explained

| Code | Meaning |
|---|---|
| `@Serializable` | A label that lets Navigation **save** the route (as text) — for example when the phone rotates or the app goes to the background. **Every route needs it.** |
| `object Home` | A screen that needs **no** extra information. An `object` (Chapter 4) — there's only one "Home". |
| `data class Profile(val userId: Int)` | A screen that **needs** information: **which** user? The route **carries** the data. 📦 |

**Real-life example:** Addresses for **houses** 🏠.
- `Home` = "*the town hall*" — there's only one, no number needed.
- `Profile(userId = 42)` = "*house number 42 on Profile Street*" — you must say **which** one.

> 💡 **Why classes instead of text like `"profile/42"`?** Older Navigation used **text** routes. A typo like `"profle/42"` would only crash when the app runs. 💥 With classes, Kotlin checks everything **before** the app runs — `Profle(42)` is a red error right away. This is called **type-safe** navigation. 🛡️

---

## 13.4 `NavController` and `NavHost` 🚗🗺️

Two main parts:

| Part | Job | Real-life example |
|---|---|---|
| **`NavController`** | **Drives** between screens. Knows the back stack. You tell it "*go to X*" or "*go back*". | The **driver** 🚗 |
| **`NavHost`** | The **map**: lists every route and **which Composable** to show for it. It's also the **area** on screen where the current screen is drawn. | The **map** 🗺️ (and the window you look through) |

### Your first navigation: two screens

```kotlin
@Serializable
object Home

@Serializable
object About

@Composable
fun SimpleNavApp() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Home
    ) {
        composable<Home> {
            HomeScreen(
                onAboutClick = { navController.navigate(About) }
            )
        }
        composable<About> {
            AboutScreen(
                onBackClick = { navController.popBackStack() }
            )
        }
    }
}

@Composable
fun HomeScreen(onAboutClick: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("🏠 Home", style = MaterialTheme.typography.headlineLarge)
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = onAboutClick) {
            Text("Go to About")
        }
    }
}

@Composable
fun AboutScreen(onBackClick: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("ℹ️ About", style = MaterialTheme.typography.headlineLarge)
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = onBackClick) {
            Text("Go back")
        }
    }
}
```

Imports:

```kotlin
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import kotlinx.serialization.Serializable
```

And in `MainActivity`:

```kotlin
setContent {
    MyFirstAppTheme {
        SimpleNavApp()
    }
}
```

**Run it!** Tap "Go to About" → About screen. Tap "Go back" **or** press the phone's **Back** button → Home. Press Back again → the app closes. 🎉

### Every bit explained

| Code | Meaning |
|---|---|
| `val navController = rememberNavController()` | Make the **driver** 🚗, and **remember** it (like `remember`, Chapter 8). It also survives rotation. |
| `NavHost(navController = ..., startDestination = Home)` | The **map** 🗺️. `startDestination` = the **first** screen when the app opens. |
| `composable<Home> { ... }` | "When the route is **`Home`**, show **this**." The `<Home>` (generics, Chapter 4!) says **which** route. |
| `navController.navigate(About)` | **Go to** About — put a new plate on the stack. ⬆️ |
| `navController.popBackStack()` | **Go back** — take the top plate off. ⬇️ |

> 🎉 **The phone's Back button works automatically!** The NavHost handles it. You don't have to write anything.

### ⚠️ Import alert: `composable`

There are **two** things called "composable": the `@Composable` label, and the `composable<...> { }` function in a NavHost. For the NavHost, you need:

```kotlin
import androidx.navigation.compose.composable
```

If `composable<Home>` is red, press **Alt + Enter** and choose **this** import.

---

## 13.5 Passing Data to a Screen 📦

### The route carries the data

```kotlin
@Serializable
data class RecipeDetail(val recipeId: Int)
```

### Going there with data

```kotlin
navController.navigate(RecipeDetail(recipeId = 7))
```

"*Go to the RecipeDetail screen, for recipe **7**.*"

### Reading the data on the other side

```kotlin
composable<RecipeDetail> { backStackEntry ->
    val route: RecipeDetail = backStackEntry.toRoute()
    RecipeDetailScreen(recipeId = route.recipeId)
}
```

Import: `androidx.navigation.toRoute`

| Code | Meaning |
|---|---|
| `{ backStackEntry -> ... }` | The lambda gets a **back stack entry** — the "**plate**" 🍽️ for this screen. It has the route's data. |
| `backStackEntry.toRoute()` | "Give me the **route object** back" — a `RecipeDetail` with the `recipeId` inside. |
| `val route: RecipeDetail = ...` | We write the type so Kotlin knows **which** route to make. (Or: `backStackEntry.toRoute<RecipeDetail>()`.) |

### The full flow

```
RecipeListScreen                      NavHost                         RecipeDetailScreen
 user taps recipe 7  ──▶  navigate(RecipeDetail(7))  ──▶  toRoute() → recipeId = 7  ──▶  shows recipe 7
```

### 🔑 Golden rule: pass the **ID**, not the whole object

```kotlin
navController.navigate(RecipeDetail(recipeId = 7))       // ✅ GOOD: just a number

navController.navigate(RecipeDetail(recipe = myRecipe))  // ❌ BAD: a whole object
```

**Why?**
- Routes are **saved as text**. Big objects are slow and can even be too big to save. 🐘
- The details screen should **load** the recipe itself using the ID (from a list, a database, or the internet). Then it always shows the **newest** data. ✅

**Real-life example:** At a library 📚, you don't carry the whole **book** to the desk — you give the **book number**, and the librarian fetches it.

### Several pieces of data

```kotlin
@Serializable
data class Search(val query: String, val page: Int = 1, val onlyFavorites: Boolean = false)

navController.navigate(Search(query = "pizza"))
navController.navigate(Search(query = "cake", page = 2, onlyFavorites = true))
```

- Simple types: `Int`, `Long`, `String`, `Boolean`, `Float`, `Double`… ✅
- **Default values** work (Chapter 2) — you can skip them.
- **Nullable** types work too: `val color: String? = null`.

---

## 13.6 The Golden Rule: Don't Pass the NavController Around 🚫🚗

It's tempting to give the `navController` to every screen:

```kotlin
// ❌ BAD
@Composable
fun HomeScreen(navController: NavController) {
    Button(onClick = { navController.navigate(About) }) { ... }
}
```

**Problems:**
- 🔍 You **can't preview** `HomeScreen` easily (a preview has no real NavController).
- 🧪 Hard to **test**.
- 🔗 The screen is **glued** to navigation. You can't reuse it in another place.

### ✅ The right way: pass **lambdas** (events up! ⬆️)

```kotlin
// ✅ GOOD
@Composable
fun HomeScreen(onAboutClick: () -> Unit) {
    Button(onClick = onAboutClick) { ... }
}

// In the NavHost:
composable<Home> {
    HomeScreen(onAboutClick = { navController.navigate(About) })
}
```

- The screen only says "*the About button was clicked*". It **doesn't know** about navigation. 🙈
- The **NavHost** decides **where** to go.
- This is **state hoisting / events up** from Chapter 8 — again! 🎉

```kotlin
@Preview
@Composable
fun HomeScreenPreview() {
    HomeScreen(onAboutClick = {})      // ✅ easy!
}
```

> 💡 **Rule:** Only the **NavHost** (and the code right around it) touches the `navController`. Screens get **lambdas** like `onRecipeClick: (Int) -> Unit` and `onBack: () -> Unit`.

---

## 13.7 Going Back ⬅️

### 3 ways to go back

| Code | Meaning |
|---|---|
| Phone's **Back** button / gesture | Handled **automatically** by NavHost. ✅ |
| `navController.popBackStack()` | Remove the top screen. |
| `navController.navigateUp()` | "Go **up**" — used for the **⬅️ arrow** in the top app bar. |

> 💡 For the top bar's ⬅️ arrow, use **`navigateUp()`**. In normal apps, it does the same as `popBackStack()`. (They are different only in special cases, like when another app opened yours with a deep link.)

### A screen with a top-bar back arrow

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DetailScreen(title: String, onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(title) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { innerPadding ->
        Text("Details here", modifier = Modifier.padding(innerPadding).padding(16.dp))
    }
}

// In the NavHost:
composable<Detail> {
    DetailScreen(title = "Pizza", onBack = { navController.navigateUp() })
}
```

### Doing something special when Back is pressed: `BackHandler`

Sometimes you want to **stop** the Back button, for example: "*You have unsaved changes. Discard?*"

```kotlin
var showDiscardDialog by remember { mutableStateOf(false) }

BackHandler(enabled = hasUnsavedChanges) {
    showDiscardDialog = true     // instead of going back, ask first
}
```

Import: `androidx.activity.compose.BackHandler`

- When `enabled` is `true`, **your** code runs instead of the normal Back.
- When `enabled` is `false`, Back works normally.

---

## 13.8 Controlling the Back Stack 🥞🎛️

Sometimes the normal "push a plate" is **not** what you want.

### Problem 1: The Welcome / Login screen 👋

```
Welcome  ──"Get started"──▶  Home
```

After tapping "Get started", the user is on **Home**. If they press **Back**… they go **back to Welcome**! 😕 That's wrong — Welcome should be **gone**.

**Fix: `popUpTo` + `inclusive`**

```kotlin
navController.navigate(Home) {
    popUpTo(Welcome) { inclusive = true }
}
```

| Code | Meaning |
|---|---|
| `navigate(Home) { ... }` | Go to Home, with **extra options** in the `{ }` (a lambda with receiver, like `apply` — Chapter 4). |
| `popUpTo(Welcome)` | **Before** going, remove plates from the top **down to** Welcome. |
| `inclusive = true` | …and remove **Welcome itself** too. |

```
Before:  [Welcome]                After:  [Home]
                                  Back → app closes ✅
```

**Real-life example:** After you **enter** a building, you throw away your **ticket** 🎫. You can't go "back" through the ticket gate.

### Problem 2: Tapping the same button twice 👆👆

If the user taps "Settings" **twice** quickly, you get **two** Settings screens on the stack! Back → Settings again. 😵

**Fix: `launchSingleTop`**

```kotlin
navController.navigate(Settings) {
    launchSingleTop = true
}
```

"If Settings is **already on top**, don't add another one." ✅

### Problem 3: Going "home" from deep inside 🏠

```
[Home] [List] [Detail] [Edit] [Done]    →  tap "Back to home"  →  [Home]
```

```kotlin
navController.navigate(Home) {
    popUpTo(Home) { inclusive = false }
    launchSingleTop = true
}
```

Or simply:

```kotlin
navController.popBackStack(route = Home, inclusive = false)
```

"Pop plates until **Home** is on top." 🍽️

### Summary of options

| Option | Meaning | Typical use |
|---|---|---|
| `popUpTo(X)` | Remove screens above X | Clearing a flow |
| `popUpTo(X) { inclusive = true }` | …and remove X too | Welcome/Login → Home |
| `launchSingleTop = true` | Don't add a copy if it's already on top | Menu items, tabs |
| `popUpTo(...) { saveState = true }` + `restoreState = true` | Remember each tab's screens | Bottom navigation (next!) |

---

## 13.9 Bottom Navigation With Real Screens 🔽

In Chapter 11 we used `when (selectedTab)`. Now let's do it the **real** way, with a NavHost. Each tab is a **route**.

### Step 1: A list of top-level tabs

```kotlin
data class TopLevelRoute<T : Any>(val label: String, val icon: ImageVector, val route: T)

val topLevelRoutes = listOf(
    TopLevelRoute("Recipes", Icons.Filled.Home, RecipeList),
    TopLevelRoute("Favorites", Icons.Filled.Favorite, Favorites),
    TopLevelRoute("About", Icons.Filled.Info, About)
)
```

- `<T : Any>` → generics (Chapter 4): `route` can be **any** route object.

### Step 2: Know which screen is showing

```kotlin
val navBackStackEntry by navController.currentBackStackEntryAsState()
val currentDestination = navBackStackEntry?.destination
```

Import: `androidx.navigation.compose.currentBackStackEntryAsState`

| Code | Meaning |
|---|---|
| `currentBackStackEntryAsState()` | The **top plate** 🍽️, as **state** (Chapter 8) → when you navigate, the bar **recomposes** automatically. ✨ |
| `?.destination` | Info about that screen. Can be `null` at the very start, so we use `?.` (Chapter 3). |

### Step 3: The NavigationBar

```kotlin
NavigationBar {
    topLevelRoutes.forEach { topLevel ->
        val selected = currentDestination?.hierarchy?.any {
            it.hasRoute(topLevel.route::class)
        } == true

        NavigationBarItem(
            selected = selected,
            onClick = {
                navController.navigate(topLevel.route) {
                    popUpTo(navController.graph.findStartDestination().id) {
                        saveState = true
                    }
                    launchSingleTop = true
                    restoreState = true
                }
            },
            icon = { Icon(topLevel.icon, contentDescription = null) },
            label = { Text(topLevel.label) }
        )
    }
}
```

Imports:

```kotlin
import androidx.navigation.NavDestination.Companion.hasRoute
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
```

### Every bit explained

**Which tab is selected?**

```kotlin
        val selected = currentDestination?.hierarchy?.any {
            it.hasRoute(topLevel.route::class)
        } == true
```

| Code | Meaning |
|---|---|
| `hierarchy` | The current screen **and its parents** (useful with nested graphs, 13.11). |
| `.any { ... }` | Is **any** of them… (Chapter 3) |
| `it.hasRoute(topLevel.route::class)` | …this tab's route? `::class` → "the **class** of this object". |
| `== true` | The whole thing could be `null` (because of `?.`). `== true` turns `null` into `false`. 👍 |

**This is the official recipe for tabs** 📋 — copy it as it is:

```kotlin
                navController.navigate(topLevel.route) {
                    popUpTo(navController.graph.findStartDestination().id) {
                        saveState = true
                    }
                    launchSingleTop = true
                    restoreState = true
                }
```

| Line | Why |
|---|---|
| `popUpTo(start) { saveState = true }` | Remove other tabs' screens from the stack, but **save** them (like putting a bookmark 🔖). This stops the stack from growing forever as you switch tabs. |
| `launchSingleTop = true` | Tapping the **same** tab again doesn't add a copy. |
| `restoreState = true` | Coming back to a tab → **restore** what it had (its screens, scroll position…). 🔖➡️📖 |

**Result:** Each tab **remembers** where you were, just like in Instagram or YouTube. 🎉

### Step 4: Hide the bottom bar on some screens

The bottom bar should show on the **tabs**, but **not** on a details screen:

```kotlin
val showBottomBar = topLevelRoutes.any { topLevel ->
    currentDestination?.hasRoute(topLevel.route::class) == true
}

Scaffold(
    bottomBar = {
        if (showBottomBar) {
            NavigationBar { ... }
        }
    }
) { ... }
```

---

## 13.10 Screens With Their Own Top Bars (Scaffold Inside Scaffold) 🏗️🏗️

Usually:
- The **app** has one `Scaffold` with the **bottom bar** (shared by all tabs).
- **Each screen** has its own `Scaffold` with **its own top bar** (different titles, different buttons).

```kotlin
Scaffold(bottomBar = { ... }) { innerPadding ->
    NavHost(
        navController = navController,
        startDestination = RecipeList,
        modifier = Modifier
            .padding(innerPadding)
            .consumeWindowInsets(innerPadding)
    ) {
        composable<RecipeList> { RecipeListScreen(...) }   // has its own Scaffold + TopAppBar
        ...
    }
}
```

Import: `androidx.compose.foundation.layout.consumeWindowInsets`

| Code | Meaning |
|---|---|
| `.padding(innerPadding)` | Leave room for the outer Scaffold's bottom bar (Chapter 11). |
| `.consumeWindowInsets(innerPadding)` | Tell the **inner** Scaffolds: "*this space is already taken care of*". Without it, the inner Scaffold would add the **same** space **again** → a big empty gap. 📏📏 |

> 💡 **Window insets** = the parts of the screen used by the **system**: the status bar 🔋 at the top and the navigation bar at the bottom. Scaffolds add padding for them automatically. `consumeWindowInsets` stops them from being added **twice**.

---

## 13.11 Nested Graphs (a Quick Look) 📂

When an app gets big, you can **group** screens. For example, all **sign-in** screens together:

```kotlin
@Serializable object AuthGraph
@Serializable object Login
@Serializable object Register

NavHost(navController, startDestination = AuthGraph) {
    navigation<AuthGraph>(startDestination = Login) {
        composable<Login> { ... }
        composable<Register> { ... }
    }
    composable<Home> { ... }
}
```

Import: `androidx.navigation.compose.navigation`

- `navigation<AuthGraph>(...)` → a **folder** 📂 of screens with its own start screen.
- After signing in: `navController.navigate(Home) { popUpTo(AuthGraph) { inclusive = true } }` → the **whole** sign-in folder is removed from the stack. ✅

You don't need this for small apps. Just know it exists! 😊

---

## 13.12 Build It: A Recipe Book App 📖🍳

Let's build an app with **5 screens**:

```
┌───────────────┐   Get started   ┌──────────────────────────┐
│  👋 Welcome    │ ──────────────▶ │ 🍳 Recipes  (tab 1)      │
│  (only once)  │  (popUpTo,      │  🍕 Pizza          ♥     │
└───────────────┘   inclusive)     │  🍝 Pasta                │
                                  │  🥞 Pancakes       ♥     │
                                  ├──────────────────────────┤
                                  │ (🏠)     ♥      ℹ️        │  ← bottom bar
                                  └──────────────────────────┘
                                         │ tap a recipe
                                         ▼
                                  ┌──────────────────────────┐
                                  │ ⬅️  Pizza            ♥    │  ← own top bar, no bottom bar
                                  │ 🍕   ⏱️ 30 min            │
                                  │ Ingredients              │
                                  │ • Flour ...              │
                                  │ Steps                    │
                                  │ 1. Make the dough ...    │
                                  └──────────────────────────┘

Tab 2: ♥ Favorites (same list, only favorites)   Tab 3: ℹ️ About
```

### File 1: `Recipe.kt` — the data

Make a new Kotlin **file** called `Recipe.kt`:

```kotlin
package com.example.recipebook

data class Recipe(
    val id: Int,
    val name: String,
    val emoji: String,
    val minutes: Int,
    val ingredients: List<String>,
    val steps: List<String>
)

object RecipeData {
    val recipes = listOf(
        Recipe(
            id = 1, name = "Pizza", emoji = "🍕", minutes = 30,
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
            id = 3, name = "Pancakes", emoji = "🥞", minutes = 15,
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

    fun findById(id: Int): Recipe? = recipes.find { it.id == id }
}
```

| Code | Meaning |
|---|---|
| `object RecipeData` | One single "store" of recipes (Chapter 4: `object`). In Chapter 22, this will become a real **database**! 🗄️ |
| `fun findById(id: Int): Recipe?` | Find a recipe by its id. Returns `null` if not found (Chapter 3: `find`). This is how the details screen **loads** its recipe from just an **ID** (13.5's golden rule). |

### File 2: `Routes.kt` — all the addresses

Make a new Kotlin **file** called `Routes.kt`:

```kotlin
package com.example.recipebook

import kotlinx.serialization.Serializable

@Serializable
object Welcome

@Serializable
object RecipeList

@Serializable
object Favorites

@Serializable
object About

@Serializable
data class RecipeDetail(val recipeId: Int)
```

> 💡 Keeping all routes in **one file** makes it easy to see **every screen** of your app at a glance. 👀

### File 3: `MainActivity.kt` — the app and screens

Replace **everything** in `MainActivity.kt` (use **your** package and theme names):

```kotlin
package com.example.recipebook

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.consumeWindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.Button
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavDestination.Companion.hasRoute
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.toRoute
import com.example.recipebook.ui.theme.RecipeBookTheme

// ---------- Activity ----------

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            RecipeBookTheme {
                RecipeBookApp()
            }
        }
    }
}

// ---------- Tabs ----------

data class TopLevelRoute<T : Any>(val label: String, val icon: ImageVector, val route: T)

val topLevelRoutes = listOf(
    TopLevelRoute("Recipes", Icons.Filled.Home, RecipeList),
    TopLevelRoute("Favorites", Icons.Filled.Favorite, Favorites),
    TopLevelRoute("About", Icons.Filled.Info, About)
)

// ---------- The app: NavController + NavHost ----------

@Composable
fun RecipeBookApp() {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination

    // Shared state: which recipes are favorites (a set of ids)
    var favoriteIds by rememberSaveable { mutableStateOf(listOf(1, 3)) }
    val toggleFavorite: (Int) -> Unit = { id ->
        favoriteIds = if (id in favoriteIds) favoriteIds - id else favoriteIds + id
    }

    val showBottomBar = topLevelRoutes.any { topLevel ->
        currentDestination?.hasRoute(topLevel.route::class) == true
    }

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        bottomBar = {
            if (showBottomBar) {
                NavigationBar {
                    topLevelRoutes.forEach { topLevel ->
                        val selected = currentDestination?.hierarchy?.any {
                            it.hasRoute(topLevel.route::class)
                        } == true

                        NavigationBarItem(
                            selected = selected,
                            onClick = {
                                navController.navigate(topLevel.route) {
                                    // Not the graph's start (that's Welcome, already removed),
                                    // but our first tab, which is always at the bottom of the stack.
                                    popUpTo(RecipeList) {
                                        saveState = true
                                    }
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
            startDestination = Welcome,
            modifier = Modifier
                .padding(innerPadding)
                .consumeWindowInsets(innerPadding)
        ) {
            composable<Welcome> {
                WelcomeScreen(
                    onGetStarted = {
                        navController.navigate(RecipeList) {
                            popUpTo(Welcome) { inclusive = true }
                        }
                    }
                )
            }

            composable<RecipeList> {
                RecipeListScreen(
                    title = "Recipes 🍳",
                    recipes = RecipeData.recipes,
                    favoriteIds = favoriteIds,
                    emptyText = "No recipes yet.",
                    onRecipeClick = { id -> navController.navigate(RecipeDetail(recipeId = id)) }
                )
            }

            composable<Favorites> {
                RecipeListScreen(
                    title = "Favorites ♥",
                    recipes = RecipeData.recipes.filter { it.id in favoriteIds },
                    favoriteIds = favoriteIds,
                    emptyText = "No favorites yet.\nOpen a recipe and tap ♥.",
                    onRecipeClick = { id -> navController.navigate(RecipeDetail(recipeId = id)) }
                )
            }

            composable<About> {
                AboutScreen()
            }

            composable<RecipeDetail> { backStackEntry ->
                val route: RecipeDetail = backStackEntry.toRoute()
                val recipe = RecipeData.findById(route.recipeId)

                RecipeDetailScreen(
                    recipe = recipe,
                    isFavorite = route.recipeId in favoriteIds,
                    onToggleFavorite = { toggleFavorite(route.recipeId) },
                    onBack = { navController.navigateUp() }
                )
            }
        }
    }
}

// ---------- Screens ----------

@Composable
fun WelcomeScreen(onGetStarted: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("📖", fontSize = 96.sp)
        Text(
            text = "Recipe Book",
            style = MaterialTheme.typography.headlineLarge,
            fontWeight = FontWeight.Bold
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "Simple recipes for every day. Cook, learn, and enjoy! 🍳",
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center
        )
        Spacer(modifier = Modifier.height(32.dp))
        Button(onClick = onGetStarted, modifier = Modifier.fillMaxWidth()) {
            Text("Get started")
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RecipeListScreen(
    title: String,
    recipes: List<Recipe>,
    favoriteIds: List<Int>,
    emptyText: String,
    onRecipeClick: (Int) -> Unit
) {
    Scaffold(
        topBar = { TopAppBar(title = { Text(title) }) }
    ) { innerPadding ->
        if (recipes.isEmpty()) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding),
                contentAlignment = Alignment.Center
            ) {
                Text(emptyText, textAlign = TextAlign.Center, style = MaterialTheme.typography.titleMedium)
            }
        } else {
            LazyColumn(
                contentPadding = PaddingValues(
                    start = 16.dp,
                    end = 16.dp,
                    top = innerPadding.calculateTopPadding() + 8.dp,
                    bottom = innerPadding.calculateBottomPadding() + 16.dp
                ),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(recipes, key = { it.id }) { recipe ->
                    RecipeCard(
                        recipe = recipe,
                        isFavorite = recipe.id in favoriteIds,
                        onClick = { onRecipeClick(recipe.id) }
                    )
                }
            }
        }
    }
}

@Composable
fun RecipeCard(recipe: Recipe, isFavorite: Boolean, onClick: () -> Unit) {
    ElevatedCard(onClick = onClick, modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.padding(16.dp),
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
            if (isFavorite) {
                Icon(Icons.Filled.Favorite, contentDescription = "Favorite", tint = Color(0xFFE53935))
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RecipeDetailScreen(
    recipe: Recipe?,
    isFavorite: Boolean,
    onToggleFavorite: () -> Unit,
    onBack: () -> Unit
) {
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
                                contentDescription = if (isFavorite) "Remove from favorites" else "Add to favorites",
                                tint = if (isFavorite) Color(0xFFE53935) else MaterialTheme.colorScheme.outline
                            )
                        }
                    }
                }
            )
        }
    ) { innerPadding ->
        if (recipe == null) {
            Box(
                modifier = Modifier.fillMaxSize().padding(innerPadding),
                contentAlignment = Alignment.Center
            ) {
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
                SectionHeader("Ingredients 🧺")
            }
            items(recipe.ingredients) { ingredient ->
                Text("• $ingredient", style = MaterialTheme.typography.bodyLarge, modifier = Modifier.padding(vertical = 4.dp))
            }
            item {
                Spacer(modifier = Modifier.height(16.dp))
                SectionHeader("Steps 👩‍🍳")
            }
            itemsIndexed(recipe.steps) { index, step ->
                Row(modifier = Modifier.padding(vertical = 6.dp)) {
                    Text(
                        text = "${index + 1}.",
                        style = MaterialTheme.typography.bodyLarge,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.width(28.dp)
                    )
                    Text(step, style = MaterialTheme.typography.bodyLarge)
                }
            }
        }
    }
}

@Composable
fun SectionHeader(text: String) {
    Text(
        text = text,
        style = MaterialTheme.typography.titleLarge,
        fontWeight = FontWeight.Bold,
        modifier = Modifier.padding(vertical = 8.dp)
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AboutScreen() {
    Scaffold(
        topBar = { TopAppBar(title = { Text("About ℹ️") }) }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text("Recipe Book 📖", style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
            Text("Version 1.0")
            Text("Made while learning Android with Kotlin and Jetpack Compose. 💚")
            Text("Recipes: ${RecipeData.recipes.size}")
        }
    }
}

// ---------- Previews (easy, because screens don't know about navigation!) ----------

@Preview(showSystemUi = true)
@Composable
fun RecipeListPreview() {
    RecipeBookTheme {
        RecipeListScreen(
            title = "Recipes 🍳",
            recipes = RecipeData.recipes,
            favoriteIds = listOf(1, 3),
            emptyText = "",
            onRecipeClick = {}
        )
    }
}

@Preview(showSystemUi = true)
@Composable
fun RecipeDetailPreview() {
    RecipeBookTheme {
        RecipeDetailScreen(
            recipe = RecipeData.recipes.first(),
            isFavorite = true,
            onToggleFavorite = {},
            onBack = {}
        )
    }
}
```

> ⚠️ Use **your** package name and theme name (`MyFirstAppTheme` if you kept the old project).

### Every important part explained

#### Part 1: Shared state lives **above** the NavHost

```kotlin
    var favoriteIds by rememberSaveable { mutableStateOf(listOf(1, 3)) }
    val toggleFavorite: (Int) -> Unit = { id ->
        favoriteIds = if (id in favoriteIds) favoriteIds - id else favoriteIds + id
    }
```

- **Three** screens need the favorites: Recipes (♥ icons), Favorites (the filtered list), and Details (the ♥ button).
- So the state lives in their **common parent**: `RecipeBookApp` (Chapter 8: hoist to the lowest common parent). ⬆️
- `List<Int>` can be saved by `rememberSaveable`. ✅

> ℹ️ In **Chapter 15**, this shared state will move into a **ViewModel** — the professional place for it.

#### Part 2: The Welcome screen disappears

```kotlin
            composable<Welcome> {
                WelcomeScreen(
                    onGetStarted = {
                        navController.navigate(RecipeList) {
                            popUpTo(Welcome) { inclusive = true }
                        }
                    }
                )
            }
```

After "Get started", Welcome is **removed** from the stack. Press Back on Recipes → the app closes, instead of showing Welcome again. ✅ (13.8, Problem 1)

> ℹ️ The Welcome screen shows **every time** the app starts. In **Chapter 21** (DataStore) we'll **remember** that the user already saw it, and skip it next time. 💾

#### Part 3: The tab recipe, with one small change

In 13.9, the tab recipe used `popUpTo(navController.graph.findStartDestination().id)` — "*pop up to the **first screen** of the app*". But in this app, the first screen is **Welcome**, and we **removed** it from the stack! `popUpTo` a screen that isn't on the stack does **nothing**, so the stack would grow forever. 😵

So here we pop up to **`RecipeList`** — our **first tab**, which is always at the bottom of the stack after Welcome is gone. ✅

> 💡 **Rule:** `popUpTo` the screen that is **really at the bottom** of your back stack — usually your first tab.

#### Part 4: The same screen, used twice

```kotlin
            composable<RecipeList> {
                RecipeListScreen(title = "Recipes 🍳", recipes = RecipeData.recipes, ...)
            }
            composable<Favorites> {
                RecipeListScreen(title = "Favorites ♥", recipes = RecipeData.recipes.filter { it.id in favoriteIds }, ...)
            }
```

- **One** `RecipeListScreen` Composable, **two** routes, **different** data. ♻️
- Possible **only** because the screen gets everything as **inputs** (no NavController inside!).

#### Part 5: The details route — ID in, recipe loaded

```kotlin
            composable<RecipeDetail> { backStackEntry ->
                val route: RecipeDetail = backStackEntry.toRoute()
                val recipe = RecipeData.findById(route.recipeId)
                RecipeDetailScreen(recipe = recipe, ...)
            }
```

1. Read the **ID** from the route.
2. **Find** the recipe by ID (could be `null`!).
3. Show it.

The screen **handles `null`** — "*😕 This recipe doesn't exist.*" — so a wrong ID never crashes the app. 🛡️

#### Part 6: `return@Scaffold` — leaving a lambda early

```kotlin
    ) { innerPadding ->
        if (recipe == null) {
            Box(...) { Text("😕 This recipe doesn't exist.") }
            return@Scaffold
        }
        LazyColumn { ... }    // here, Kotlin knows recipe is NOT null (smart cast!)
    }
```

| Code | Meaning |
|---|---|
| `return@Scaffold` | Leave **this lambda** (the Scaffold's content) — not the whole function. The `@Scaffold` is a **label** that says **which** lambda. 🏷️ |
| After the `if` | Kotlin **knows** `recipe` isn't `null` → we can write `recipe.name` without `?.`. **Smart cast** (Chapter 3)! 🧠 |

> 💡 A plain `return` inside a lambda isn't allowed here. Use `return@NameOfTheFunction` to leave just the lambda.

#### Part 7: The details screen mixes item types in one LazyColumn

```kotlin
            item { /* emoji, time, "Ingredients" header */ }
            items(recipe.ingredients) { ... }
            item { /* "Steps" header */ }
            itemsIndexed(recipe.steps) { index, step -> ... }
```

One scroll, many kinds of items (Chapter 10). The numbers `1.`, `2.`, `3.` come from `index + 1`. 🔢

#### Part 8: Bottom bar only on the tabs

```kotlin
    val showBottomBar = topLevelRoutes.any { topLevel ->
        currentDestination?.hasRoute(topLevel.route::class) == true
    }
```

- On **Recipes**, **Favorites**, **About** → bar visible.
- On **Welcome** and **RecipeDetail** → bar hidden. More room for content! 📐

### Run it! ▶️

1. 👋 **Welcome** → tap **Get started**.
2. 🍳 **Recipes** → tap **Pizza** → the **details** screen (no bottom bar).
3. Tap ♥ in the top bar → red. Press **⬅️** → Pizza has a ♥ in the list.
4. Open the **Favorites** tab → Pizza and Pancakes are there.
5. Open Pasta's details **from Recipes**, then switch to the **About** tab, then back to **Recipes** → you're **back on Pasta's details**! The tab **remembered** (`saveState` / `restoreState`). 🔖
6. Press **Back** until the app closes — Welcome **never** comes back. ✅
7. **Rotate** on the details screen → still there, favorites kept. 🔄

---

## 13.13 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| Forgot `@Serializable` on a route | 💥 Crash: *Serializer for class 'X' is not found* | Add `@Serializable` above every route. |
| Serialization plugin not added | `@Serializable` is red / crash at runtime | Add `alias(libs.plugins.kotlin.serialization)` and Sync. |
| `composable<Home>` is red | Wrong import | `import androidx.navigation.compose.composable` |
| Navigating to a route not in the NavHost | 💥 *Navigation destination that matches route X cannot be found* | Add `composable<X> { }` to the NavHost. |
| Passing whole objects in routes | Slow, may crash; old data | Pass the **ID**, load the object on the screen. |
| Passing `navController` into screens | Hard to preview and reuse | Pass lambdas like `onItemClick: (Int) -> Unit`. |
| Back goes to the Welcome/Login screen | Old screen still on the stack | `popUpTo(Welcome) { inclusive = true }` |
| Tapping twice opens two copies | Duplicate screens | `launchSingleTop = true` |
| Tabs forget where you were / stack grows | Missing tab options | Use the full recipe: `popUpTo(start) { saveState = true }`, `launchSingleTop`, `restoreState`. |
| Big empty gap at the top or bottom | Insets added twice (Scaffold in Scaffold) | `.padding(innerPadding).consumeWindowInsets(innerPadding)` on the NavHost. |
| `return` inside a Scaffold lambda | *'return' is not allowed here* | Use `return@Scaffold`. |
| Shared state lost between screens | State was inside one screen | Hoist it above the NavHost (or into a ViewModel, Chapter 15). |

---

## 13.14 Summary — What You Learned 🎓

✅ **Navigation** = moving between screens + a **back stack** 🥞 (push to go, pop to go back).

✅ **Setup:** `navigation-compose` + `kotlinx-serialization-json` + the **Kotlin serialization plugin**.

✅ **Routes** are `@Serializable` objects (no data) or data classes (with data). Type-safe! 🛡️

✅ **`rememberNavController()`** = the driver 🚗. **`NavHost { composable<Route> { } }`** = the map 🗺️.

✅ **Go:** `navController.navigate(Route)`. **Back:** `popBackStack()` / `navigateUp()`; the system Back works automatically. **`BackHandler`** for special cases.

✅ **Data:** `navigate(Detail(id = 7))` → `backStackEntry.toRoute<Detail>()`. Pass **IDs**, not objects.

✅ **Golden rule:** screens get **lambdas**, not the NavController → easy previews and reuse.

✅ **Back stack control:** `popUpTo`, `inclusive`, `launchSingleTop`, `saveState`/`restoreState`.

✅ **Bottom navigation:** `currentBackStackEntryAsState()`, `hierarchy.any { it.hasRoute(...) }`, and the official tab recipe. Hide the bar on non-tab screens.

✅ **Scaffold in Scaffold:** `padding(innerPadding).consumeWindowInsets(innerPadding)`.

✅ You built a 5-screen **Recipe Book** app! 📖🍳

---

## 13.15 Practice Time 🏋️

**Task 1 — Three screens in a row:**
Make screens **A → B → C**. A has a button "Go to B", B has "Go to C", C has two buttons: "Back" (one step) and "Back to A" (all the way). Use routes `ScreenA`, `ScreenB`, `ScreenC`.

**Task 2 — Pass a name:**
Make a `GreetInput` screen with a text field and a button "Say hello". It navigates to a `Greeting(val name: String)` route that shows `"Hello, <name>! 👋"` big in the center.

**Task 3 — Number game:**
A `Pick` screen shows buttons 1 to 5. Tapping one navigates to `Result(val number: Int)`, which shows `"You picked 3!"` and whether it's even or odd.

**Task 4 — Login that can't go back:**
Make `Login` and `Home` routes. Login has a "Log in" button. After logging in, Back on Home must **close the app** (not return to Login). Home has a "Log out" button that goes back to Login and also **clears** Home from the stack.

**Task 5 — Add a 4th tab:**
In the Recipe Book, add a **"Quick"** tab (icon: `Icons.Filled.Star`) that shows only recipes that take **15 minutes or less**. (Hint: a new route object, a new `TopLevelRoute`, and a new `composable<...>` that reuses `RecipeListScreen`.)

---

### Answers

**Task 1:**

```kotlin
@Serializable object ScreenA
@Serializable object ScreenB
@Serializable object ScreenC

@Composable
fun AbcApp() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = ScreenA) {
        composable<ScreenA> {
            SimpleScreen(title = "Screen A 🅰️") {
                Button(onClick = { navController.navigate(ScreenB) }) { Text("Go to B") }
            }
        }
        composable<ScreenB> {
            SimpleScreen(title = "Screen B 🅱️") {
                Button(onClick = { navController.navigate(ScreenC) }) { Text("Go to C") }
            }
        }
        composable<ScreenC> {
            SimpleScreen(title = "Screen C ©️") {
                Button(onClick = { navController.popBackStack() }) { Text("Back") }
                Button(onClick = { navController.popBackStack(route = ScreenA, inclusive = false) }) {
                    Text("Back to A")
                }
            }
        }
    }
}

@Composable
fun SimpleScreen(title: String, content: @Composable () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(title, style = MaterialTheme.typography.headlineLarge)
        content()
    }
}
```

💡 `content: @Composable () -> Unit` — your **own** Composable with a content slot, just like `Card { }` or `Scaffold { }`! (Chapter 7's theme did this too.)

**Task 2:**

```kotlin
@Serializable object GreetInput
@Serializable data class Greeting(val name: String)

@Composable
fun GreetApp() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = GreetInput) {
        composable<GreetInput> {
            var name by rememberSaveable { mutableStateOf("") }
            Column(
                modifier = Modifier.fillMaxSize().padding(24.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically)
            ) {
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Your name") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                Button(
                    onClick = { navController.navigate(Greeting(name = name.trim())) },
                    enabled = name.isNotBlank(),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Say hello")
                }
            }
        }
        composable<Greeting> { backStackEntry ->
            val route: Greeting = backStackEntry.toRoute()
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("Hello, ${route.name}! 👋", style = MaterialTheme.typography.headlineLarge)
            }
        }
    }
}
```

**Task 3:**

```kotlin
@Serializable object Pick
@Serializable data class Result(val number: Int)

@Composable
fun NumberGameApp() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = Pick) {
        composable<Pick> {
            Row(
                modifier = Modifier.fillMaxSize(),
                horizontalArrangement = Arrangement.spacedBy(8.dp, Alignment.CenterHorizontally),
                verticalAlignment = Alignment.CenterVertically
            ) {
                (1..5).forEach { n ->
                    Button(onClick = { navController.navigate(Result(number = n)) }) {
                        Text("$n")
                    }
                }
            }
        }
        composable<Result> { backStackEntry ->
            val number = backStackEntry.toRoute<Result>().number
            val kind = if (number % 2 == 0) "even" else "odd"
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("You picked $number! It's $kind.", style = MaterialTheme.typography.headlineSmall)
            }
        }
    }
}
```

> ⚠️ `Result` is also the name of a class in Kotlin's standard library. Ours is in **your** package, so it's fine — but if you see confusing errors, rename it to `PickResult`. 😉

**Task 4:**

```kotlin
@Serializable object Login
@Serializable object Home

@Composable
fun LoginFlowApp() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = Login) {
        composable<Login> {
            SimpleScreen(title = "🔐 Login") {
                Button(onClick = {
                    navController.navigate(Home) {
                        popUpTo(Login) { inclusive = true }
                    }
                }) { Text("Log in") }
            }
        }
        composable<Home> {
            SimpleScreen(title = "🏠 Home") {
                Button(onClick = {
                    navController.navigate(Login) {
                        popUpTo(Home) { inclusive = true }
                    }
                }) { Text("Log out") }
            }
        }
    }
}
```

Both directions use `popUpTo(...) { inclusive = true }`, so the stack **always** has just **one** screen. Back closes the app. ✅

**Task 5:**

In `Routes.kt`:

```kotlin
@Serializable
object Quick
```

In `MainActivity.kt`, add to `topLevelRoutes`:

```kotlin
val topLevelRoutes = listOf(
    TopLevelRoute("Recipes", Icons.Filled.Home, RecipeList),
    TopLevelRoute("Quick", Icons.Filled.Star, Quick),
    TopLevelRoute("Favorites", Icons.Filled.Favorite, Favorites),
    TopLevelRoute("About", Icons.Filled.Info, About)
)
```

And in the `NavHost`:

```kotlin
            composable<Quick> {
                RecipeListScreen(
                    title = "Quick ⚡ (15 min or less)",
                    recipes = RecipeData.recipes.filter { it.minutes <= 15 },
                    favoriteIds = favoriteIds,
                    emptyText = "No quick recipes.",
                    onRecipeClick = { id -> navController.navigate(RecipeDetail(recipeId = id)) }
                )
            }
```

The bottom bar shows the new tab **automatically**, because it's built from the list. ✨ (Import `androidx.compose.material.icons.filled.Star`.)

---

## 13.16 What Is Next?

You may have noticed something: in the Recipe Book, the **favorites** state lives in `RecipeBookApp`. And when the phone **rotates**, every screen's state must be saved with `rememberSaveable`… As apps grow, this gets messy. 😵

But first, we need to understand **what really happens** to a screen when you rotate the phone, switch apps, or get a phone call. 📞

In **Chapter 14: The Life of an App — Activity Lifecycle**, you will learn:

- The **lifecycle**: `onCreate`, `onStart`, `onResume`, `onPause`, `onStop`, `onDestroy` 🔄
- What happens when you **rotate** the phone, **switch apps**, or **lock the screen** 📱
- **Configuration changes** and why state gets lost
- Watching the lifecycle in **Logcat** 🔍
- Lifecycle-aware code in Compose

**Great job finishing Chapter 13! 🎉 Your apps now have many screens!**
