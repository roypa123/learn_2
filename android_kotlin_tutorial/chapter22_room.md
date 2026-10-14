# Chapter 22: Saving Lots of Data — Room Database 🗃️💾

> **What you will learn in this chapter**
>
> 1. When you need a **database** (and when DataStore is enough) 🤔
> 2. What a database is — **tables**, **rows**, and **columns** (like a spreadsheet!) 📊
> 3. A little **SQL** — the language of databases — in simple words 🗣️
> 4. **Room**: the three parts — **Entity**, **DAO**, and **Database** 🏛️
> 5. Setting up Room with **KSP** 📦
> 6. 🛠️ Building a **Shopping List** app 🛒 — add, check, delete, and clear items
> 7. Room + **`Flow`**: the screen updates **by itself** 🌊🪄
> 8. Looking **inside** your database with the **Database Inspector** 🔍
> 9. Changing the database later — **migrations** 🚚
> 10. 🔁 Keeping Chapter 16's promise: the **Recipe Book** with a `RoomRecipeRepository`!
>
> **Time needed:** about 6 hours. Take a break between Part A and Part B! ☕
>
> **What you need to know:** Chapters 1–21, especially 16 (MVVM), 18 (coroutines and Flow), and 21 (DataStore).

---

## 22.1 When Do You Need a Database? 🤔

In Chapter 21, DataStore saved **a few small values**: a name, a theme, a score. 📝

But imagine a **shopping list** 🛒:

- The user adds **many** items — 5, 50, maybe 500.
- Each item has **several** pieces of information: a name, "bought or not", when it was added…
- We want to **sort** them (not bought first), **find** them, **change** one, **delete** some.

DataStore's labeled jars 🫙 can't do that well. We need a **filing cabinet** 🗃️ — a **database**.

| | DataStore 📝 | Room database 🗃️ |
|---|---|---|
| How much data | A **few** values | **Lots** — thousands of items |
| Shape | Single values (`"Sam"`, `true`, `12`) | **Lists** of things, each with many fields |
| Sorting / searching | ❌ | ✅ |
| Changing one item in a list | ❌ (you'd rewrite everything) | ✅ |
| Examples | Theme, name, "seen welcome" | Notes, contacts, recipes, messages, to-dos |

> 🎯 **Simple rule (from Chapter 21):** A few settings → **DataStore**. Lists of things the user creates → **Room**.

---

## 22.2 What Is a Database? 📊

A **database** stores data in **tables**. A table looks just like a **spreadsheet** (like Excel or Google Sheets):

**Table: `shopping_items`**

| id | name | isBought | createdAt |
|---|---|---|---|
| 1 | Milk 🥛 | 1 | 1718000000000 |
| 2 | Bread 🍞 | 0 | 1718000100000 |
| 3 | Apples 🍎 | 0 | 1718000200000 |

| Word | Meaning | In the table above |
|---|---|---|
| **Table** | One "sheet" for one **kind** of thing | `shopping_items` |
| **Column** | One **piece of information**, with a **type** | `id`, `name`, `isBought`, `createdAt` |
| **Row** | One **thing** (one item) | "Bread 🍞" is one row |
| **Primary key** 🔑 | A column whose value is **different** for every row, so we can find **exactly one** row | `id` |

> 💡 Notice `isBought` shows `1` and `0`. Databases usually store **true** as **1** and **false** as **0**. Room converts them to `Boolean` for you. ✅

> 💡 **Kotlin connection:** a **table** is like a `List` of a **data class**. A **row** is one **object**. A **column** is one **property**. You already think this way! 😎

Android phones have a database engine built in, called **SQLite** (say: "**S-Q-L-light**"). It's small, fast, and free. Room is a friendly Kotlin layer **on top of** SQLite.

---

## 22.3 SQL in 10 Minutes 🗣️

To talk to SQLite, we use a language called **SQL** (say "**S-Q-L**" or "**sequel**"). It reads almost like English! Here are the sentences you'll need — all using the table above.

### Reading: `SELECT` 📖

```sql
SELECT * FROM shopping_items
```

"**Give me** all columns (`*` = everything) **from** the table `shopping_items`." → all 3 rows.

```sql
SELECT * FROM shopping_items WHERE isBought = 0
```

"…but **only** rows **where** `isBought` is 0 (not bought)." → Bread, Apples.

```sql
SELECT * FROM shopping_items ORDER BY name ASC
```

"…**sorted** by `name`, A → Z." (`ASC` = ascending ⬆️, `DESC` = descending ⬇️) → Apples, Bread, Milk.

```sql
SELECT * FROM shopping_items WHERE id = 2
```

→ Only Bread.

```sql
SELECT COUNT(*) FROM shopping_items
```

"**How many** rows?" → 3

### Writing: `INSERT`, `UPDATE`, `DELETE` ✍️

```sql
INSERT INTO shopping_items (name, isBought, createdAt) VALUES ('Eggs', 0, 1718000300000)
```

"**Add** a new row." (No `id` given → the database chooses the next one: **4**.)

```sql
UPDATE shopping_items SET isBought = 1 WHERE id = 2
```

"**Change** `isBought` to 1 for the row with id 2." → Bread is bought ✅.

```sql
DELETE FROM shopping_items WHERE isBought = 1
```

"**Remove** all rows where `isBought` is 1." → Milk and Bread are gone. 🗑️

### Cheat sheet 📋

| SQL | Meaning | Like in Kotlin… |
|---|---|---|
| `SELECT * FROM t` | Get all rows | `list` |
| `WHERE x = 5` | Only some rows | `.filter { it.x == 5 }` |
| `ORDER BY x ASC / DESC` | Sort | `.sortedBy { }` / `.sortedByDescending { }` |
| `SELECT COUNT(*)` | How many | `.size` |
| `INSERT INTO t ... VALUES ...` | Add a row | `list + item` |
| `UPDATE t SET x = 1 WHERE ...` | Change rows | `.map { if (...) it.copy(x = 1) else it }` |
| `DELETE FROM t WHERE ...` | Remove rows | `.filterNot { ... }` |

> ⚠️ **Don't panic!** 😌 With Room, you'll write **only small** SQL sentences like these, and Room **checks them while building** your app. A typo → a clear error in Android Studio, **not** a crash on the user's phone. 🛡️

---

## 22.4 Room — The Three Parts 🏛️

Room has **three** parts. Let's imagine a **library** 📚:

| Room part | What it is | Library version | Kotlin |
|---|---|---|---|
| **Entity** | One **table** (what a row looks like) | A **shelf** for one kind of book 📚 | A **data class** with `@Entity` |
| **DAO** (**D**ata **A**ccess **O**bject) | The **questions** you can ask: get, add, change, delete | The **librarian** 🧑‍🏫 — you ask, they fetch | An **interface** with `@Dao` |
| **Database** | Holds everything together; opens the file | The **library building** 🏛️ | An **abstract class** with `@Database` |

```
   🏛️ Database  ─────────────────▶  gives you  ─────▶  🧑‍🏫 DAO
        │                                                │
        └── knows about ──▶  📚 Entity (table)  ◀── reads/writes
```

**You write** small, simple pieces with **annotations** (`@Entity`, `@Dao`, `@Query`…). **Room writes** all the long, boring database code **for you** while building the app. 🪄 That's why we need a **code generator** called **KSP**.

---

## 22.5 Setting Up Room 📦

### What is KSP? 🤖

**KSP** (**K**otlin **S**ymbol **P**rocessing) is a tool that **reads your code while it's being built** and **writes more code**. Room uses it: it reads your `@Entity`, `@Dao`, and `@Database` and generates the real database code.

### The KSP version must fit your Kotlin version ⚠️

Open `gradle/libs.versions.toml` and look for the line `kotlin = "..."`. Then find your KSP version in this table:

| Your `kotlin = ` version | Use `ksp = ` |
|---|---|
| `"2.0.21"` | `"2.0.21-1.0.28"` |
| `"2.1.0"` | `"2.1.0-1.0.29"` |
| `"2.1.10"` | `"2.1.10-1.0.31"` |
| `"2.1.20"` | `"2.1.20-2.0.1"` |
| `"2.1.21"` | `"2.1.21-2.0.2"` |
| `"2.2.0"` | `"2.2.0-2.0.2"` |
| `"2.2.10"` | `"2.2.10-2.0.2"` |
| `"2.2.20"` | `"2.2.20-2.0.4"` |
| `"2.2.21"` | `"2.2.21-2.0.5"` |
| `"2.3.0"` or newer | the newest `"2.3.x"` (from KSP 2.3.0, the version no longer includes the Kotlin version) |

🔎 **The pattern** for older versions: KSP's version **starts with** your Kotlin version, then `-` and KSP's own number. For other versions, check **github.com/google/ksp/releases**.

> 😵 If the versions don't fit, the build fails with an error like *"ksp-2.0.21-1.0.28 is too old for kotlin-2.1.0"*. Just pick the right version from the table and **Sync** again.

### `gradle/libs.versions.toml`

```toml
[versions]
room = "2.7.1"
ksp = "2.0.21-1.0.28"            # 👈 choose from the table above!

[libraries]
androidx-room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
androidx-room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
androidx-room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }

[plugins]
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
```

### `build.gradle.kts (Project: ...)` — the **top-level** file

```kotlin
plugins {
    // ... existing lines ...
    alias(libs.plugins.ksp) apply false
}
```

### `build.gradle.kts (Module :app)`

```kotlin
plugins {
    // ... existing lines ...
    alias(libs.plugins.ksp)
}

dependencies {
    // ... existing lines ...
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    ksp(libs.androidx.room.compiler)
}
```

**Sync Now** 🔄 ✅

| Line | Meaning |
|---|---|
| `room-runtime` | Room itself — runs inside your app. |
| `room-ktx` | Kotlin extras: **coroutines** (`suspend`) and **`Flow`** support. 🌊 |
| `ksp(room-compiler)` | The **code writer**. `ksp(...)` instead of `implementation(...)` means: "use it **while building**, don't put it **inside** the app." |
| `apply false` (top-level file) | "Make the plugin **available** to modules, but don't use it here." Same as the other plugins already in that file. |

> ℹ️ There are **two** `build.gradle.kts` files! The **Project** one (top level) and the **Module :app** one. Both need a small change here. In the **Project** view, the top-level one is in the project's main folder; the app one is in the `app` folder.

---

# Part A: The Shopping List App 🛒

## 22.6 What Are We Building? 🎯

```
┌──────────────────────────────────┐
│ Shopping List 🛒    [Clear bought]│
├──────────────────────────────────┤
│ [ Eggs               ] [ Add ➕ ] │
│ 1 of 4 bought                    │
│ ☐  Eggs                     🗑️   │
│ ☐  Apples 🍎                 🗑️   │
│ ☐  Bread 🍞                  🗑️   │
│ ☑  M̶i̶l̶k̶ ̶🥛                  🗑️   │
└──────────────────────────────────┘
```

### Requirements 📋

1. Type an item and tap **Add** (or the keyboard's **Done** ✔️) → it appears at the **top**.
2. Tap the **checkbox** → the item is **bought**: crossed out and moved to the **bottom**.
3. Tap 🗑️ → the item is **deleted**.
4. **Clear bought** removes **all** bought items at once.
5. "**1 of 4 bought**" counter.
6. Everything is saved in a **Room database** — close the app, reopen, it's all there. 💾

### Create the project

1. **File → New → New Project… → Empty Activity**.
2. **Name:** `Shopping List` · **Package:** `com.example.shoppinglist` · **Finish**.
3. Your theme is **`ShoppingListTheme`**.

### Libraries

- **Room + KSP** (22.5)
- **Lifecycle** libraries (`lifecycle-viewmodel-compose`, `lifecycle-runtime-compose` — Chapter 15)

**Sync** 🔄 ✅

### The files 📁

```
com.example.shoppinglist
 ├── ShoppingApplication.kt
 ├── MainActivity.kt
 ├── data/
 │    ├── ShoppingItem.kt              (Entity 📚)
 │    ├── ShoppingItemDao.kt           (DAO 🧑‍🏫)
 │    ├── ShoppingDatabase.kt          (Database 🏛️)
 │    ├── ShoppingRepository.kt        (interface)
 │    └── RoomShoppingRepository.kt
 ├── di/
 │    └── AppContainer.kt
 └── ui/
      ├── theme/                       (already there)
      ├── ShoppingListViewModel.kt
      └── ShoppingListScreen.kt
```

---

## 22.7 Step 1: The Entity — What a Row Looks Like 📚

### `data/ShoppingItem.kt`

```kotlin
package com.example.shoppinglist.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "shopping_items")                       // (1)
data class ShoppingItem(
    @PrimaryKey(autoGenerate = true)                        // (2)
    val id: Long = 0,                                       // (3)
    val name: String,                                       // (4)
    val isBought: Boolean = false,
    val createdAt: Long = System.currentTimeMillis()        // (5)
)
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `@Entity(tableName = "shopping_items")` | "Room, make a **table** for this class, called `shopping_items`." Each **object** = one **row**. Each **property** = one **column**. |
| 2 | `@PrimaryKey(autoGenerate = true)` | This property is the **primary key** 🔑. `autoGenerate = true` → "**Database, you choose** the number" (1, 2, 3, …). |
| 3 | `val id: Long = 0` | `0` means "**no id yet**". When we insert an item with id 0, the database gives it a **real** id. `Long` because there could be many, many rows. |
| 4 | `val name: String` | A text column. No default → you **must** give a name. |
| 5 | `createdAt = System.currentTimeMillis()` | **When** the item was added (milliseconds since 1970 — a big `Long`). We'll use it to sort **newest first**. ⏰ |

So this class becomes this table:

| id (🔑 INTEGER) | name (TEXT) | isBought (INTEGER 0/1) | createdAt (INTEGER) |
|---|---|---|---|

> 💡 In this small app, the **Entity** is also the class the screens use. That's OK for simple apps. In **Part B**, you'll see why bigger apps often keep them **separate**.

---

## 22.8 Step 2: The DAO — The Questions You Can Ask 🧑‍🏫

### `data/ShoppingItemDao.kt`

```kotlin
package com.example.shoppinglist.data

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao                                                                        // (1)
interface ShoppingItemDao {

    @Query("SELECT * FROM shopping_items ORDER BY isBought ASC, createdAt DESC")   // (2)
    fun observeAll(): Flow<List<ShoppingItem>>                              // (3)

    @Insert                                                                 // (4)
    suspend fun insert(item: ShoppingItem): Long                            // (5)

    @Update                                                                 // (6)
    suspend fun update(item: ShoppingItem)

    @Delete                                                                 // (7)
    suspend fun delete(item: ShoppingItem)

    @Query("DELETE FROM shopping_items WHERE isBought = 1")                 // (8)
    suspend fun deleteBought(): Int                                         // (9)
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `@Dao interface ShoppingItemDao` | "Room, this is the **librarian** 🧑‍🏫." Only function **headers** — Room writes the bodies! |
| 2 | `@Query("SELECT ... ORDER BY isBought ASC, createdAt DESC")` | Your own SQL sentence. Sort by **two** things: first `isBought` (0 before 1 → **not bought first**), then, inside each group, `createdAt` **newest first**. |
| 3 | `fun observeAll(): Flow<List<ShoppingItem>>` | Returns a **`Flow`** 🌊 — **not** `suspend`! Room sends the list **now**, and **again every time the table changes**. That's the magic 🪄 — see 22.13. |
| 4 | `@Insert` | "**Add** this item as a new row." No SQL needed — Room writes it. |
| 5 | `suspend fun insert(...): Long` | `suspend` → it runs on a **background** thread (main-safe 🛡️). It returns the **new id** the database chose. |
| 6 | `@Update` | "Find the row with the **same id**, and **replace** its values." |
| 7 | `@Delete` | "Remove the row with the **same id**." |
| 8 | `@Query("DELETE FROM ... WHERE isBought = 1")` | `@Query` can also **change** data. `1` = true. |
| 9 | `: Int` | How many rows were deleted (useful for a message like "3 items cleared"). |

### Two kinds of DAO functions 🌊⚡

| Kind | Looks like | Use for |
|---|---|---|
| **Observe** 👀 | `fun x(): Flow<...>` (no `suspend`) | Data the screen **shows** — it updates **itself** |
| **One-time action** ⚡ | `suspend fun x(...)` | Insert, update, delete, or "get it once" |

> 🛡️ **Room checks your SQL while building!** Try writing `SELCT` (a typo) or a column that doesn't exist, then build. Android Studio shows an error with the problem, **before** the app ever runs. Many mistakes are caught early. 🎉

---

## 22.9 Step 3: The Database — Holding It All Together 🏛️

### `data/ShoppingDatabase.kt`

```kotlin
package com.example.shoppinglist.data

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(                                                  // (1)
    entities = [ShoppingItem::class],                       // (2)
    version = 1,                                            // (3)
    exportSchema = false                                    // (4)
)
abstract class ShoppingDatabase : RoomDatabase() {          // (5)
    abstract fun shoppingItemDao(): ShoppingItemDao         // (6)
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `@Database(...)` | "Room, this is the **library building** 🏛️." |
| 2 | `entities = [ShoppingItem::class]` | The list of **tables** in this database. `[ ]` here makes an array; `::class` means "the class itself". More tables later → `[A::class, B::class]`. |
| 3 | `version = 1` | The database's **version number**. When you **change** a table later, you must **increase** it (see 22.14). |
| 4 | `exportSchema = false` | Room can save a description of the tables to a file (useful for big projects). We turn it off to keep things simple — otherwise you get a **warning** while building. |
| 5 | `abstract class ... : RoomDatabase()` | **Abstract** = an **unfinished** class: we can't create it ourselves. **Room** finishes it (writes the missing code) while building. 🪄 |
| 6 | `abstract fun shoppingItemDao()` | "This building has a librarian." Room writes the code that gives you a `ShoppingItemDao`. |

### Creating the database (we'll do this in the AppContainer)

```kotlin
val database = Room.databaseBuilder(
    context,                              // the Application context
    ShoppingDatabase::class.java,         // which database class
    "shopping.db"                         // the file name on the phone 📁
).build()
```

> ⚠️ **Create the database only ONCE** in the whole app — opening it is slow, and two copies can fight over the file. That's exactly what the **AppContainer** 🧰 is for (with `by lazy`).

---

## 22.10 Step 4: Repository, AppContainer, Application 🏪🧰

### `data/ShoppingRepository.kt`

```kotlin
package com.example.shoppinglist.data

import kotlinx.coroutines.flow.Flow

interface ShoppingRepository {
    val items: Flow<List<ShoppingItem>>

    suspend fun addItem(name: String)
    suspend fun setBought(item: ShoppingItem, isBought: Boolean)
    suspend fun deleteItem(item: ShoppingItem)
    suspend fun clearBought(): Int
}
```

This time we designed the promise **for a database** from the start: a **`Flow`** to watch, and **`suspend`** functions for actions. (Compare with Chapter 16's interface in Part B! 👀)

### `data/RoomShoppingRepository.kt`

```kotlin
package com.example.shoppinglist.data

import kotlinx.coroutines.flow.Flow

class RoomShoppingRepository(
    private val dao: ShoppingItemDao
) : ShoppingRepository {

    override val items: Flow<List<ShoppingItem>> = dao.observeAll()

    override suspend fun addItem(name: String) {
        dao.insert(ShoppingItem(name = name))                         // (1)
    }

    override suspend fun setBought(item: ShoppingItem, isBought: Boolean) {
        dao.update(item.copy(isBought = isBought))                    // (2)
    }

    override suspend fun deleteItem(item: ShoppingItem) {
        dao.delete(item)
    }

    override suspend fun clearBought(): Int = dao.deleteBought()
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `ShoppingItem(name = name)` | A new item: `id = 0` (the database will choose), `isBought = false`, `createdAt = now`. All defaults! ✨ |
| 2 | `item.copy(isBought = isBought)` | Same item (same **id** 🔑), with one change → `@Update` finds the row by its id and saves it. |

> 💡 The repository looks almost **too** simple. That's fine! It's the **one** place that knows we use Room. If we later add internet sync ☁️, only **this** class grows.

### `di/AppContainer.kt`

```kotlin
package com.example.shoppinglist.di

import android.content.Context
import androidx.room.Room
import com.example.shoppinglist.data.RoomShoppingRepository
import com.example.shoppinglist.data.ShoppingDatabase
import com.example.shoppinglist.data.ShoppingRepository

interface AppContainer {
    val shoppingRepository: ShoppingRepository
}

class DefaultAppContainer(private val context: Context) : AppContainer {

    private val database: ShoppingDatabase by lazy {                   // (1)
        Room.databaseBuilder(
            context,
            ShoppingDatabase::class.java,
            "shopping.db"
        ).build()
    }

    override val shoppingRepository: ShoppingRepository by lazy {
        RoomShoppingRepository(database.shoppingItemDao())            // (2)
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `database by lazy { Room.databaseBuilder(...).build() }` | Build the database the **first** time it's needed, and only **once**. ✅ |
| 2 | `database.shoppingItemDao()` | Ask the building for its librarian, and hand it to the repository. |

### `ShoppingApplication.kt`

```kotlin
package com.example.shoppinglist

import android.app.Application
import com.example.shoppinglist.di.AppContainer
import com.example.shoppinglist.di.DefaultAppContainer

class ShoppingApplication : Application() {

    lateinit var container: AppContainer

    override fun onCreate() {
        super.onCreate()
        container = DefaultAppContainer(context = this)
    }
}
```

### `AndroidManifest.xml`

```xml
<application
    android:name=".ShoppingApplication"
    ... the rest stays the same ... >
```

---

## 22.11 Step 5: The ViewModel 🧠

### `ui/ShoppingListViewModel.kt`

```kotlin
package com.example.shoppinglist.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.ViewModelProvider.AndroidViewModelFactory.Companion.APPLICATION_KEY
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.example.shoppinglist.ShoppingApplication
import com.example.shoppinglist.data.ShoppingItem
import com.example.shoppinglist.data.ShoppingRepository
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

data class ShoppingUiState(
    val items: List<ShoppingItem> = emptyList(),
    val isLoading: Boolean = true
) {
    val boughtCount: Int get() = items.count { it.isBought }                  // (1)
    val totalCount: Int get() = items.size
}

class ShoppingListViewModel(
    private val repository: ShoppingRepository
) : ViewModel() {

    val uiState: StateFlow<ShoppingUiState> = repository.items
        .map { items -> ShoppingUiState(items = items, isLoading = false) }   // (2)
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = ShoppingUiState()
        )

    fun onAddItem(name: String) {
        val cleanName = name.trim()
        if (cleanName.isEmpty()) return                                       // (3)
        viewModelScope.launch {
            repository.addItem(cleanName)
        }
    }

    fun onBoughtChange(item: ShoppingItem, isBought: Boolean) {
        viewModelScope.launch { repository.setBought(item, isBought) }
    }

    fun onDeleteItem(item: ShoppingItem) {
        viewModelScope.launch { repository.deleteItem(item) }
    }

    fun onClearBought() {
        viewModelScope.launch { repository.clearBought() }
    }

    companion object {
        val Factory: ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val app = this[APPLICATION_KEY] as ShoppingApplication
                ShoppingListViewModel(repository = app.container.shoppingRepository)
            }
        }
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `items.count { it.isBought }` | How many items match the condition (Chapter 3). Calculated values — not stored. |
| 2 | `.map { ... }.stateIn(...)` | The Chapter 18 recipe: database Flow → screen state. Until the database answers, `isLoading = true`. |
| 3 | `if (cleanName.isEmpty()) return` | No empty items. The ViewModel **protects** the data. 🛡️ |

> 🎯 Look closely: **no function changes `uiState` by hand!** Every action **writes to the database**, and the database's Flow **brings the new list back** by itself. One source of truth: the **database**. 🗃️

---

## 22.12 Step 6: The Screen 🎨

### `ui/ShoppingListScreen.kt`

```kotlin
package com.example.shoppinglist.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
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
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.shoppinglist.data.ShoppingItem
import com.example.shoppinglist.ui.theme.ShoppingListTheme

@Composable
fun ShoppingListRoute(
    viewModel: ShoppingListViewModel = viewModel(factory = ShoppingListViewModel.Factory)
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    ShoppingListScreen(
        uiState = uiState,
        onAddItem = viewModel::onAddItem,
        onBoughtChange = viewModel::onBoughtChange,
        onDeleteItem = viewModel::onDeleteItem,
        onClearBought = viewModel::onClearBought
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ShoppingListScreen(
    uiState: ShoppingUiState,
    onAddItem: (String) -> Unit,
    onBoughtChange: (ShoppingItem, Boolean) -> Unit,
    onDeleteItem: (ShoppingItem) -> Unit,
    onClearBought: () -> Unit,
    modifier: Modifier = Modifier
) {
    var newItemText by rememberSaveable { mutableStateOf("") }                // (1)

    fun addItem() {                                                           // (2)
        onAddItem(newItemText)
        newItemText = ""
    }

    Scaffold(
        modifier = modifier,
        topBar = {
            TopAppBar(
                title = { Text("Shopping List 🛒") },
                actions = {
                    TextButton(
                        onClick = onClearBought,
                        enabled = uiState.boughtCount > 0
                    ) {
                        Text("Clear bought")
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .padding(innerPadding)
                .fillMaxSize()
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedTextField(
                    value = newItemText,
                    onValueChange = { newItemText = it },
                    label = { Text("New item") },
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(
                        capitalization = KeyboardCapitalization.Sentences,
                        imeAction = ImeAction.Done                            // (3)
                    ),
                    keyboardActions = KeyboardActions(onDone = { addItem() }),
                    modifier = Modifier.weight(1f)
                )
                Button(onClick = { addItem() }, enabled = newItemText.isNotBlank()) {
                    Text("Add ➕")
                }
            }

            if (uiState.totalCount > 0) {
                Text(
                    text = "${uiState.boughtCount} of ${uiState.totalCount} bought",
                    style = MaterialTheme.typography.labelLarge,
                    modifier = Modifier.padding(horizontal = 16.dp)
                )
            }

            when {                                                            // (4)
                uiState.isLoading -> {
                    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator()
                    }
                }
                uiState.items.isEmpty() -> {
                    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        Text("Your list is empty 🛒\nAdd something above!")
                    }
                }
                else -> {
                    LazyColumn(modifier = Modifier.fillMaxSize()) {
                        items(uiState.items, key = { item -> item.id }) { item ->   // (5)
                            ShoppingItemRow(
                                item = item,
                                onBoughtChange = { checked -> onBoughtChange(item, checked) },
                                onDelete = { onDeleteItem(item) },
                                modifier = Modifier.animateItem()                    // (6)
                            )
                            HorizontalDivider()
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ShoppingItemRow(
    item: ShoppingItem,
    onBoughtChange: (Boolean) -> Unit,
    onDelete: () -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Checkbox(checked = item.isBought, onCheckedChange = onBoughtChange)
        Text(
            text = item.name,
            style = MaterialTheme.typography.bodyLarge,
            textDecoration = if (item.isBought) TextDecoration.LineThrough else null,   // (7)
            color = if (item.isBought) MaterialTheme.colorScheme.onSurfaceVariant
                    else MaterialTheme.colorScheme.onSurface,
            modifier = Modifier.weight(1f)
        )
        IconButton(onClick = onDelete) {
            Icon(Icons.Filled.Delete, contentDescription = "Delete ${item.name}")
        }
    }
}

@Preview(showBackground = true)
@Composable
fun ShoppingListScreenPreview() {
    ShoppingListTheme {
        ShoppingListScreen(
            uiState = ShoppingUiState(
                items = listOf(
                    ShoppingItem(id = 1, name = "Eggs 🥚"),
                    ShoppingItem(id = 2, name = "Apples 🍎"),
                    ShoppingItem(id = 3, name = "Milk 🥛", isBought = true)
                ),
                isLoading = false
            ),
            onAddItem = {}, onBoughtChange = { _, _ -> }, onDeleteItem = {}, onClearBought = {}
        )
    }
}
```

**The important parts:**

| # | Code | Meaning |
|---|---|---|
| 1 | `newItemText` with `rememberSaveable` | What the user is **typing** is UI state (Chapter 18's text field rule ⌨️). It goes to the database only when **added**. |
| 2 | `fun addItem() { ... }` **inside** a Composable | A **local function** — a function inside a function! Used by **both** the button and the keyboard's Done key, so we don't repeat the code. ♻️ |
| 3 | `imeAction = ImeAction.Done` + `onDone = { addItem() }` | The keyboard shows a ✔️ key; pressing it **adds** the item (Chapter 9). Fast typing! ⌨️⚡ |
| 4 | `when { ... }` (no subject) | Three situations: loading ⏳, empty 📭, or the list 📋. The first matching condition wins. |
| 5 | `key = { item -> item.id }` | The database id is a **perfect** key — unique and stable. 🔑 |
| 6 | `Modifier.animateItem()` | When an item is checked, it **slides** to its new place at the bottom instead of jumping. ✨ (Chapter 10) |
| 7 | `TextDecoration.LineThrough` | ~~Crossed-out~~ text for bought items. |

> 💡 In the preview, `onBoughtChange = { _, _ -> }` — a lambda with **two** parameters we don't use (`_` = "ignore this").

### `MainActivity.kt`

```kotlin
package com.example.shoppinglist

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.shoppinglist.ui.ShoppingListRoute
import com.example.shoppinglist.ui.theme.ShoppingListTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            ShoppingListTheme {
                ShoppingListRoute()
            }
        }
    }
}
```

**Run it!** ▶️ Add "Milk 🥛", "Bread 🍞", "Apples 🍎". Check Milk → it slides to the bottom, crossed out. **Swipe the app away** and reopen → **everything is still there!** 💾🎉

---

## 22.13 The Magic: How Does the Screen Update by Itself? 🪄

Let's follow **one tap** on Milk's checkbox, step by step:

```
1. 👆 Tap the checkbox
2. 📱 Screen       → onBoughtChange(milk, true)
3. 🧠 ViewModel    → viewModelScope.launch { repository.setBought(milk, true) }
4. 🏪 Repository   → dao.update(milk.copy(isBought = true))
5. 🗃️ Room         → UPDATE shopping_items SET ... WHERE id = 1   (on a background thread)
6. 🗃️ Room         → "The shopping_items table changed! Who is watching it?"
7. 🌊 Room         → runs observeAll()'s SELECT again → sends a NEW list into the Flow
8. 🧠 ViewModel    → map { ShoppingUiState(...) } → stateIn → new uiState
9. 📱 Screen       → collectAsStateWithLifecycle → recomposition → Milk slides down ✨
```

**Nobody told the screen to refresh!** Room **knows** which tables each Flow query reads. When one of those tables changes, it **re-runs** the query and sends the new result. 🪄

This is the **single source of truth** idea at its best:

```
          writes ✍️                       reads 👀 (automatically)
📱 ──▶ 🧠 ──▶ 🏪 ──▶ 🗃️ DATABASE 🗃️ ──▶ 🌊 Flow ──▶ 🏪 ──▶ 🧠 ──▶ 📱
```

---

## 22.14 Look Inside: The Database Inspector 🔍

Android Studio can show your database **live**, while the app runs!

1. Run the app on an emulator or phone.
2. At the bottom of Android Studio, open **App Inspection** (or **View → Tool Windows → App Inspection**).
3. Choose the **Database Inspector** tab.
4. Open `shopping.db` → `shopping_items`.

You'll see your table: **id**, **name**, **isBought** (0/1), **createdAt**. 📊

**Try this:** tick ✅ **Live updates** at the top. Now check an item in the app → the table changes **instantly** in Android Studio! 🤯

You can even **run your own SQL**: click **New Query** (the SQL icon) and type:

```sql
SELECT * FROM shopping_items WHERE isBought = 0
```

…and press **Run**. Great for testing your queries before putting them in a DAO. 🧪

---

## 22.15 Changing the Database Later — Migrations 🚚

Your app is published. 1,000 people have shopping lists. 📱📱📱 Now you want to add a **quantity** to each item:

```kotlin
data class ShoppingItem(
    ...
    val quantity: Int = 1          // 👈 new column
)
```

But the users' phones have a database file with the **old** table (no `quantity` column)! 😱 If you just change the class and run, the app **crashes**:

```
Room cannot verify the data integrity. Looks like you've changed schema but forgot to update the version number.
```

Room is protecting your users' data. 🛡️ You must tell it **how** to move from the old shape to the new one. That's a **migration** (like moving house 🚚 — you need a plan to carry the furniture).

### Step 1: Increase the version

```kotlin
@Database(entities = [ShoppingItem::class], version = 2, exportSchema = false)   // 1 → 2
```

### Step 2a: While you're still learning/developing — throw the old data away 🗑️

```kotlin
Room.databaseBuilder(context, ShoppingDatabase::class.java, "shopping.db")
    .fallbackToDestructiveMigration(dropAllTables = true)       // ⚠️ deletes all old data!
    .build()
```

"If you don't know how to migrate, just **delete** everything and start fresh." Fine on **your** test phone — but **never** in a real published app (users would lose their lists! 😭).

### Step 2b: In a real app — write a migration ✍️

```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {                                // (1)
    override fun migrate(db: SupportSQLiteDatabase) {                          // (2)
        db.execSQL(
            "ALTER TABLE shopping_items ADD COLUMN quantity INTEGER NOT NULL DEFAULT 1"   // (3)
        )
    }
}

Room.databaseBuilder(context, ShoppingDatabase::class.java, "shopping.db")
    .addMigrations(MIGRATION_1_2)                                              // (4)
    .build()
```

| # | Code | Meaning |
|---|---|---|
| 1 | `object : Migration(1, 2)` | A plan for moving from version **1** to version **2**. (`object :` makes a one-off object from a class — like an anonymous helper.) |
| 2 | `migrate(db: SupportSQLiteDatabase)` | Room calls this **once**, on each phone that still has version 1. |
| 3 | `ALTER TABLE ... ADD COLUMN quantity INTEGER NOT NULL DEFAULT 1` | SQL: "**Change** the table: **add** a column `quantity`, a whole number, never empty, **1** for all existing rows." Everyone's old items get quantity 1. ✅ |
| 4 | `.addMigrations(MIGRATION_1_2)` | Tell Room about the plan. |

Imports: `androidx.room.migration.Migration`, `androidx.sqlite.db.SupportSQLiteDatabase`.

> 🎯 **Rules for later:**
> 1. Change an `@Entity` → **increase** `version`.
> 2. While learning → uninstalling the app, or `fallbackToDestructiveMigration(dropAllTables = true)`, is fine.
> 3. After publishing → **always** write a `Migration`. Your users' data is precious. 💎

> ℹ️ For a beginner-friendly shortcut: **uninstall** the app from your test phone/emulator after changing an entity. A fresh install creates the new table. (Your test data is lost, of course.)

---

# Part B: Keeping a Promise — The Recipe Book With Room 📖🗃️

## 22.16 The Promise From Chapter 16 🤝

In Chapter 16 we wrote:

> *"In Chapter 22, we'll write a `RoomRecipeRepository` that saves to a database — and nothing else in the app will need to change. That's the power of the interface!"*

Right now, the Recipe Book's favorites ♥ are **forgotten** when the app closes (they live in `InMemoryRecipeRepository`). Let's fix that — **without touching a single screen or ViewModel**. 😎

Open your **Recipe Book** project from Chapter 16 (`com.example.recipebook`). Add **Room + KSP** (22.5) and **Sync**. (It already has kotlinx.serialization from Chapter 13 — we'll need it!)

Here's the interface we must keep (from Chapter 16):

```kotlin
interface RecipeRepository {
    val recipes: StateFlow<List<Recipe>>
    fun getRecipe(id: Int): Recipe?
    fun toggleFavorite(id: Int)
}
```

Hmm. 🤔 Look carefully — there are **two** challenges:

| Challenge | Why it's tricky with Room |
|---|---|
| `recipes` is a **`StateFlow`** | Room gives a plain **`Flow`**. |
| `getRecipe` and `toggleFavorite` are **not** `suspend` | Room's actions **are** `suspend` (database work takes time). |

The interface was designed for **memory**, where everything is instant. We'll still keep our promise — let's see how! 💪

### The new files 📁

```
data/
 ├── model/Recipe.kt                     (unchanged ✅)
 ├── RecipeRepository.kt                 (unchanged ✅)
 ├── InMemoryRecipeRepository.kt         (unchanged — we keep it!)
 ├── SampleRecipes.kt                    (unchanged ✅)
 ├── RoomRecipeRepository.kt             🆕
 └── local/                              🆕 (make this package)
      ├── RecipeEntity.kt                🆕
      ├── Converters.kt                  🆕
      ├── RecipeDao.kt                   🆕
      └── RecipeDatabase.kt              🆕
```

---

## 22.17 Step 1: Storing a List in a Table — Type Converters 🔄

A `Recipe` has `ingredients: List<String>` and `steps: List<String>`. But a database **column** can only hold **simple** things: numbers and text. 😬 **Room doesn't know how to store a `List`.**

Solution: a **Type Converter** — a pair of functions that turn a `List<String>` into **text** (to save) and back into a list (to read).

What text? We already know a great format for lists… **JSON**! (Chapter 19) 📄

```
listOf("Flour", "Water", "Yeast")   ⇄   "[\"Flour\",\"Water\",\"Yeast\"]"
        Kotlin list                        text in the database column
```

### `data/local/Converters.kt`

```kotlin
package com.example.recipebook.data.local

import androidx.room.TypeConverter
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

class Converters {

    @TypeConverter                                                       // (1)
    fun fromStringList(list: List<String>): String =
        Json.encodeToString(list)                                        // (2)

    @TypeConverter
    fun toStringList(text: String): List<String> =
        Json.decodeFromString(text)                                      // (3)
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `@TypeConverter` | "Room, use this function when you meet this **type**." Room looks at the **parameter** and **return** types to know when to call it. |
| 2 | `Json.encodeToString(list)` | `List<String>` → JSON **text** (to **save**). 📦➡️📄 |
| 3 | `Json.decodeFromString(text)` | JSON text → `List<String>` (to **read**). Kotlin knows the result type from the function's return type. 📄➡️📦 |

(If the `decodeFromString` / `encodeToString` imports show as **unused** in grey, that's fine — you can remove them.)

---

## 22.18 Step 2: The Entity and the Mappers 📚↔️📦

### Why a separate `RecipeEntity`? 🤔

We **could** put `@Entity` on the `Recipe` class itself. But the screens use `Recipe` everywhere. If database details (`@Entity`, `@PrimaryKey`, table names…) are mixed into it, the **whole app** depends on Room. 😬

So, just like `DogImagesResponse` vs `DogPhoto` in Chapter 20, we keep **two** classes:

| Class | For | Knows about Room? |
|---|---|---|
| `RecipeEntity` | The **database** 🗃️ | ✅ Yes |
| `Recipe` | The **app** (ViewModels, screens) 📱 | ❌ No — and it stays that way |

### `data/local/RecipeEntity.kt`

```kotlin
package com.example.recipebook.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.recipebook.data.model.Recipe

@Entity(tableName = "recipes")
data class RecipeEntity(
    @PrimaryKey val id: Int,                                         // (1)
    val name: String,
    val emoji: String,
    val minutes: Int,
    val ingredients: List<String>,                                   // (2)
    val steps: List<String>,
    val isFavorite: Boolean
)

fun RecipeEntity.toRecipe(): Recipe = Recipe(                        // (3)
    id = id,
    name = name,
    emoji = emoji,
    minutes = minutes,
    ingredients = ingredients,
    steps = steps,
    isFavorite = isFavorite
)

fun Recipe.toEntity(): RecipeEntity = RecipeEntity(                  // (4)
    id = id,
    name = name,
    emoji = emoji,
    minutes = minutes,
    ingredients = ingredients,
    steps = steps,
    isFavorite = isFavorite
)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `@PrimaryKey val id: Int` | **No** `autoGenerate` here — our recipes **already** have ids (1 to 6), and the routes use them. |
| 2 | `val ingredients: List<String>` | Room will use our **Converters** for this column. 🔄 |
| 3 | `fun RecipeEntity.toRecipe()` | An **extension function** (Chapter 4): "Every `RecipeEntity` can turn itself into a `Recipe`." 📚➡️📦 |
| 4 | `fun Recipe.toEntity()` | And the other way around. 📦➡️📚 These are called **mappers**. |

> 💡 Yes, the mappers look repetitive. That's normal! In bigger apps, the two classes **differ** more (for example, the entity might store dates as `Long`, while the app model uses a nicer type). The mappers are where those differences are handled.

---

## 22.19 Step 3: The DAO and the Database 🧑‍🏫🏛️

### `data/local/RecipeDao.kt`

```kotlin
package com.example.recipebook.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface RecipeDao {

    @Query("SELECT * FROM recipes ORDER BY id ASC")
    fun observeAll(): Flow<List<RecipeEntity>>

    @Query("SELECT COUNT(*) FROM recipes")
    suspend fun count(): Int                                                  // (1)

    @Insert(onConflict = OnConflictStrategy.REPLACE)                          // (2)
    suspend fun insertAll(recipes: List<RecipeEntity>)

    @Query("UPDATE recipes SET isFavorite = NOT isFavorite WHERE id = :id")    // (3)
    suspend fun toggleFavorite(id: Int)
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `suspend fun count(): Int` | "How many recipes are saved?" — we'll use it to fill an **empty** database the first time. |
| 2 | `@Insert(onConflict = OnConflictStrategy.REPLACE)` | Insert a **whole list** at once. If a row with the same id **already exists** (a "conflict"), **replace** it instead of crashing. |
| 3 | `SET isFavorite = NOT isFavorite WHERE id = :id` | Flip the favorite **inside the database**: `NOT 1` = 0, `NOT 0` = 1. 🔁 **`:id`** is a **placeholder**: Room puts the function's `id` parameter there — **safely**. (Never build SQL by gluing strings together!) |

### `data/local/RecipeDatabase.kt`

```kotlin
package com.example.recipebook.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters

@Database(entities = [RecipeEntity::class], version = 1, exportSchema = false)
@TypeConverters(Converters::class)                                           // (1)
abstract class RecipeDatabase : RoomDatabase() {
    abstract fun recipeDao(): RecipeDao
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `@TypeConverters(Converters::class)` | "Room, use **these** converters for this database." Now `List<String>` columns work. ✅ (Forget this line → build error: *"Cannot figure out how to save this field into database"*.) |

---

## 22.20 Step 4: `RoomRecipeRepository` — Keeping the Promise 🤝

Now the clever part. We need a **`StateFlow`** and **non-suspend** functions… while Room wants coroutines. The solution: give the repository its **own** coroutine scope — one that lives as long as the **app**.

### `data/RoomRecipeRepository.kt`

```kotlin
package com.example.recipebook.data

import com.example.recipebook.data.local.RecipeDao
import com.example.recipebook.data.local.toEntity
import com.example.recipebook.data.local.toRecipe
import com.example.recipebook.data.model.Recipe
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class RoomRecipeRepository(
    private val recipeDao: RecipeDao,
    private val scope: CoroutineScope                                         // (1)
) : RecipeRepository {

    override val recipes: StateFlow<List<Recipe>> = recipeDao.observeAll()
        .map { entities -> entities.map { it.toRecipe() } }                   // (2)
        .stateIn(
            scope = scope,
            started = SharingStarted.Eagerly,                                 // (3)
            initialValue = emptyList()
        )

    init {
        scope.launch {                                                        // (4)
            if (recipeDao.count() == 0) {
                recipeDao.insertAll(sampleRecipes.map { it.toEntity() })
            }
        }
    }

    override fun getRecipe(id: Int): Recipe? =
        recipes.value.find { it.id == id }                                    // (5)

    override fun toggleFavorite(id: Int) {
        scope.launch {                                                        // (6)
            recipeDao.toggleFavorite(id)
        }
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `private val scope: CoroutineScope` | A coroutine **home** 🏠 that lives as long as the **app** (we create it in the AppContainer). The repository uses it for database work. |
| 2 | `.map { entities -> entities.map { it.toRecipe() } }` | Two different `map`s! The **outer** one is the Flow's `map` (each **new list** from the database); the **inner** one is the List's `map` (each **entity** → a `Recipe`). |
| 3 | `.stateIn(scope, SharingStarted.Eagerly, emptyList())` | Turn Room's `Flow` into the **`StateFlow`** the interface promised. ✅ `Eagerly` → start reading **right away** and **keep** the latest list in memory, so `recipes.value` is always ready. |
| 4 | `init { scope.launch { if (count() == 0) insertAll(...) } }` | The **very first** time, the database is **empty** → fill it with the 6 sample recipes. Every time after, `count()` is 6 → do nothing. This is called **seeding** (planting the first seeds 🌱). |
| 5 | `recipes.value.find { ... }` | Not `suspend`! We look in the **in-memory copy** that `stateIn` keeps up to date. ⚡ |
| 6 | `scope.launch { recipeDao.toggleFavorite(id) }` | Not `suspend` either — we **start** the database work in the app scope and return **immediately**. A moment later, Room's Flow sends the updated list → `recipes` → every screen. 🪄 |

> 🤔 **Why not `viewModelScope`?** The repository is shared by **all** screens and lives as long as the **app**. A ViewModel's scope dies when its screen is closed — a toggle started there could be **cancelled** halfway. The app scope is the right home. 🏠

---

## 22.21 Step 5: The One-Line Change 🔁

### `di/AppContainer.kt`

```kotlin
package com.example.recipebook.di

import android.content.Context
import androidx.room.Room
import com.example.recipebook.data.RecipeRepository
import com.example.recipebook.data.RoomRecipeRepository
import com.example.recipebook.data.local.RecipeDatabase
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob

interface AppContainer {
    val recipeRepository: RecipeRepository
}

class DefaultAppContainer(private val context: Context) : AppContainer {

    private val applicationScope = CoroutineScope(SupervisorJob() + Dispatchers.Default)   // (1)

    private val database: RecipeDatabase by lazy {                                       // (2)
        Room.databaseBuilder(context, RecipeDatabase::class.java, "recipe_book.db").build()
    }

    override val recipeRepository: RecipeRepository by lazy {
        RoomRecipeRepository(database.recipeDao(), applicationScope)                     // (3) 👈 THE line
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `CoroutineScope(SupervisorJob() + Dispatchers.Default)` | Make our **app-wide** coroutine home. `SupervisorJob()` → if **one** coroutine fails, the **others** keep running (a normal parent would cancel all its children — Chapter 18's family rules 👨‍👩‍👧). `Dispatchers.Default` → work happens off the main thread. |
| 2 | `database by lazy { ... }` | Build the database **once**. |
| 3 | `RoomRecipeRepository(...)` | **Before:** `InMemoryRecipeRepository()`. **After:** `RoomRecipeRepository(...)`. **That's the swap!** 🔁 |

### `RecipeBookApplication.kt` — pass the Context

```kotlin
container = DefaultAppContainer(context = this)
```

### What did NOT change? ✅

| File | Changed? |
|---|---|
| `Recipe.kt`, `RecipeRepository.kt` | ❌ No |
| `RecipeListViewModel.kt`, `RecipeDetailViewModel.kt` | ❌ **No** |
| `RecipeListScreen.kt`, `RecipeDetailScreen.kt`, `RecipeCard.kt`, `AboutScreen.kt` | ❌ **No** |
| `RecipeBookNavHost.kt`, `Routes.kt`, `MainActivity.kt` | ❌ **No** |

**Not one screen or ViewModel was touched.** 🎉 The container chose a different repository, and the whole app now saves to a database. **Promise kept!** 🤝

**Run it!** ▶️ Tap ♥ on Pasta and Salad. **Swipe the app away.** Reopen → **Pasta and Salad are still favorites!** 💾♥ Open the **Database Inspector** → `recipe_book.db` → `recipes` → you'll see the `isFavorite` column change as you tap. And look at the `ingredients` column: JSON text like `["Pasta","Garlic",...]` — your Type Converter at work! 🔄

> 🧪 **Bonus:** Want to see the power again? In `AppContainer`, change **(3)** back to `InMemoryRecipeRepository()`. Run → favorites are forgotten again. Switch back → saved. **One line** decides where the data lives. 🔌

---

## 22.22 An Honest Look: Was This the Best Design? 🧐

Our `RoomRecipeRepository` works well. But let's be honest about the **small compromises** we made to keep the old interface:

| Compromise | What can happen |
|---|---|
| `getRecipe(id)` reads `recipes.value` | In the first **milliseconds** after the app starts, the list may still be **empty** → `null`. (Our Detail ViewModel handles it, because it also **watches** the Flow.) |
| `toggleFavorite` returns before the database has saved | The caller can't **wait** for it, or know if it **failed**. |
| `SharingStarted.Eagerly` | All recipes stay in memory forever — fine for 6, not great for 60,000. |

**If we designed the interface for a database from the start**, it would look like the Shopping List's:

```kotlin
interface RecipeRepository {
    val recipes: Flow<List<Recipe>>                 // a Flow — the ViewModels use stateIn
    fun observeRecipe(id: Int): Flow<Recipe?>       // watch one recipe
    suspend fun toggleFavorite(id: Int)             // can be awaited
}
```

> 🎓 **The lesson:** interfaces protect you from change — but only as well as they are **designed**. A good habit for **any** data that might someday come from a database or the internet: use **`Flow`** for things you watch and **`suspend`** for actions — **even** in an in-memory version. Then **any** future repository fits perfectly. In **Chapter 24 (Notes App)**, we'll design it this way from day one. 💪

---

## 22.23 Test Checklist ✅

### Shopping List 🛒

| Test | Expected | ✓ |
|---|---|---|
| Add 3 items | Newest at the top | ☐ |
| Add with the keyboard's ✔️ key | Works, text field clears | ☐ |
| Add an empty / spaces-only item | Button disabled; nothing added | ☐ |
| Check an item | Crossed out, slides to the bottom ✨ | ☐ |
| Uncheck it | Goes back up | ☐ |
| Delete 🗑️ | Gone | ☐ |
| Clear bought | All checked items gone; button disabled when none are bought | ☐ |
| Swipe the app away, reopen | **Everything** is still there 💾 | ☐ |
| Rotate 🔄 while typing | Typed text and list stay | ☐ |
| Database Inspector with Live updates | Rows change as you tap | ☐ |

### Recipe Book 📖

| Test | Expected | ✓ |
|---|---|---|
| First start (fresh install) | 6 recipes appear (seeded 🌱) | ☐ |
| Toggle ♥ in the list | Favorites tab updates | ☐ |
| Toggle ♥ in the detail screen | List updates too | ☐ |
| Swipe the app away, reopen | Favorites **remembered** 💾 | ☐ |
| Database Inspector → `recipes` | `ingredients` column shows JSON text | ☐ |

---

## 22.24 Common Mistakes and Fixes 🔧

| Mistake | Error / Problem | Fix |
|---|---|---|
| KSP version doesn't fit Kotlin | Build fails (*"…too old for kotlin…"* or similar) | Use the table in 22.5. |
| Used `implementation` instead of `ksp` for `room-compiler` | 💥 Crash when opening the database: *"…ShoppingDatabase_Impl does not exist. Is Room annotation processor correctly configured?"* | `ksp(libs.androidx.room.compiler)` |
| Forgot `alias(libs.plugins.ksp)` in a `plugins { }` block | `ksp(...)` is red | Add it to **both** build files (`apply false` in the project one). |
| A `List` (or other complex type) in an `@Entity` without a converter | *"Cannot figure out how to save this field into database"* | A `@TypeConverter` + `@TypeConverters(...)` on the database. |
| Typo in a `@Query` | Build error pointing at the SQL | Fix the SQL — Room found it for you! 🛡️ |
| `suspend` on a function returning `Flow` | Works badly / confusing | Flow functions: **no** `suspend`. Actions: `suspend`. |
| Calling a DAO `suspend` function outside a coroutine | *Suspend function … should be called only from a coroutine* | `viewModelScope.launch { }` |
| Building the database in a ViewModel or Composable | Several copies, slow, errors | Build it **once** in the AppContainer (`by lazy`). |
| Changed an `@Entity`, didn't change `version` | 💥 *Room cannot verify the data integrity…* | Increase `version` + a `Migration` (or uninstall while learning). |
| `fallbackToDestructiveMigration` in a published app | Users **lose all data** 😭 | Write real migrations. |
| `@Update` / `@Delete` with an item whose `id` is 0 | Nothing happens (no row with id 0) | Use items that came **from** the database (they have real ids). |
| Two items with the same `@PrimaryKey` on `@Insert` | 💥 *UNIQUE constraint failed* | `autoGenerate = true`, or `onConflict = OnConflictStrategy.REPLACE`. |
| Building SQL with `"... WHERE name = '$name'"` | Breaks with `'` in names; unsafe | Use placeholders: `WHERE name = :name`. |

---

## 22.25 Summary — What You Learned 🎓

✅ **Room** is for **lots** of structured data; **DataStore** is for a few settings.

✅ A **database** has **tables** (like spreadsheets) with **columns** and **rows**. A **primary key** 🔑 identifies each row.

✅ **SQL** basics: `SELECT … FROM … WHERE … ORDER BY`, `COUNT(*)`, `INSERT`, `UPDATE … SET`, `DELETE`. Room **checks** your SQL while building. 🛡️

✅ Room's three parts: **`@Entity`** (a table 📚), **`@Dao`** (the questions 🧑‍🏫: `@Query`, `@Insert`, `@Update`, `@Delete`), **`@Database`** (the building 🏛️, an abstract class).

✅ Setup: `room-runtime`, `room-ktx`, and **`ksp(room-compiler)`**, with a **KSP version that fits your Kotlin**.

✅ DAO functions that return **`Flow`** update **by themselves** when the table changes 🪄; actions are **`suspend`** and main-safe.

✅ Build the database **once** (in the AppContainer). Use the **Database Inspector** to look inside. 🔍

✅ Changing an entity → increase **`version`** + a **`Migration`** (or destructive fallback **only** while learning).

✅ **Type Converters** store complex types (like `List<String>`) as text. Keep **entities** and **app models** separate with **mappers**.

✅ An **app-wide `CoroutineScope`** (`SupervisorJob() + Dispatchers.Default`) for repository work that outlives screens.

✅ You built a **Shopping List** 🛒 and swapped the Recipe Book to **Room** with **one line** in the AppContainer — **promise kept!** 🤝

---

## 22.26 Practice Time 🏋️

**Task 1 — Read the SQL 🗣️:**
What does each one do? (Table: `books` with columns `id`, `title`, `pages`, `isRead`.)
a) `SELECT * FROM books WHERE isRead = 0 ORDER BY pages ASC`
b) `SELECT COUNT(*) FROM books WHERE pages > 300`
c) `UPDATE books SET isRead = 1 WHERE id = 7`
d) `DELETE FROM books WHERE isRead = 1`

**Task 2 — Write the DAO ✍️:**
For an `@Entity(tableName = "books")` data class `Book(id: Long, title: String, pages: Int, isRead: Boolean)`, write a DAO with:
a) watch all books sorted by title (A → Z)
b) watch only **unread** books
c) get **one** book by id (once, nullable)
d) insert a book
e) delete all **read** books

**Task 3 — Quantity in the Shopping List 🔢:**
Add `quantity: Int = 1` to `ShoppingItem`, with **+** and **−** buttons on each row (not below 1). Show "Eggs × 3". Write a **real migration** from version 1 to 2.

**Task 4 — Undo delete ↩️:**
When an item is deleted in the Shopping List, show a **Snackbar** "Eggs deleted" with **Undo**. Undo puts it back.
*Hint:* Snackbar with action (Chapter 11). To put it back, **insert** the same `ShoppingItem` object again — it still has its old `id` and `createdAt`!

**Task 5 — Search 🔍:**
Add a DAO query that finds items whose name **contains** some text:
`@Query("SELECT * FROM shopping_items WHERE name LIKE '%' || :text || '%'")`
What do `LIKE`, `%`, and `||` mean? Use it to make a search box.

**Task 6 — Find the 3 bugs 🐛🐛🐛:**

```kotlin
@Entity
data class Note(
    val id: Long = 0,
    val text: String,
    val tags: List<String>
)

@Dao
interface NoteDao {
    @Query("SELECT * FROM note")
    suspend fun observeAll(): Flow<List<Note>>
}
```

---

### Answers

**Task 1:**

| | Meaning |
|---|---|
| a) | All **unread** books, **shortest first**. |
| b) | **How many** books have **more than 300** pages. |
| c) | Mark book number **7** as **read**. |
| d) | **Delete** all books that are **read**. |

**Task 2:**

```kotlin
@Dao
interface BookDao {

    @Query("SELECT * FROM books ORDER BY title ASC")
    fun observeAll(): Flow<List<Book>>

    @Query("SELECT * FROM books WHERE isRead = 0")
    fun observeUnread(): Flow<List<Book>>

    @Query("SELECT * FROM books WHERE id = :id")
    suspend fun getById(id: Long): Book?

    @Insert
    suspend fun insert(book: Book)

    @Query("DELETE FROM books WHERE isRead = 1")
    suspend fun deleteRead()
}
```

💡 c) returns `Book?` — `null` if there's no book with that id. "Once" → `suspend`; "watch" → `Flow`.

**Task 3:**

1. Entity: add `val quantity: Int = 1`.
2. Database: `version = 2`.
3. Migration:

```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE shopping_items ADD COLUMN quantity INTEGER NOT NULL DEFAULT 1")
    }
}
```

and `.addMigrations(MIGRATION_1_2)` in the AppContainer's `Room.databaseBuilder(...)`.

4. Repository: `suspend fun setQuantity(item: ShoppingItem, quantity: Int)` → `dao.update(item.copy(quantity = quantity.coerceAtLeast(1)))`.
5. ViewModel: `fun onQuantityChange(item: ShoppingItem, quantity: Int) { viewModelScope.launch { repository.setQuantity(item, quantity) } }`
6. Row: add

```kotlin
TextButton(onClick = { onQuantityChange(item.quantity - 1) }, enabled = item.quantity > 1) { Text("−") }
Text("× ${item.quantity}")
TextButton(onClick = { onQuantityChange(item.quantity + 1) }) { Text("+") }
```

…with a new `onQuantityChange: (Int) -> Unit` parameter, passed from the screen.

💡 Test the migration: install the **old** version, add items, then run the new version **without uninstalling** → old items show "× 1". ✅

**Task 4:**

In the ViewModel:

```kotlin
fun onUndoDelete(item: ShoppingItem) {
    viewModelScope.launch { repository.restoreItem(item) }
}
```

Repository: `suspend fun restoreItem(item: ShoppingItem)` → `dao.insert(item)` (the same object, with its **old id** → it comes back in the **same place**).

In the screen (with a `SnackbarHostState` in the Scaffold and `val scope = rememberCoroutineScope()`):

```kotlin
onDelete = {
    onDeleteItem(item)
    scope.launch {
        val result = snackbarHostState.showSnackbar(
            message = "${item.name} deleted",
            actionLabel = "Undo",
            duration = SnackbarDuration.Short
        )
        if (result == SnackbarResult.ActionPerformed) {
            onUndoDelete(item)
        }
    }
}
```

💡 This works because the **deleted** `item` object is still in our hands (in the lambda). Inserting it again with its old `id` and `createdAt` restores it **exactly**. ↩️

**Task 5:**

| Part | Meaning |
|---|---|
| `LIKE` | "Looks like this **pattern**" (not exactly equal). It ignores upper/lower case for normal letters. |
| `%` | "**Any** text here (even nothing)". `'%milk%'` = "has *milk* somewhere". |
| `\|\|` | **Glue** texts together in SQL (like `+` for Strings in Kotlin). `'%' \|\| :text \|\| '%'` → `'%milk%'`. |

```kotlin
@Query("SELECT * FROM shopping_items WHERE name LIKE '%' || :text || '%' ORDER BY isBought ASC, createdAt DESC")
fun search(text: String): Flow<List<ShoppingItem>>
```

Add `fun search(text: String): Flow<List<ShoppingItem>>` to the repository interface (and `= dao.search(text)` in `RoomShoppingRepository`). In the ViewModel, keep the search text in a `MutableStateFlow("")` and switch to the new query each time it changes:

```kotlin
private val _query = MutableStateFlow("")
val query: StateFlow<String> = _query.asStateFlow()

@OptIn(ExperimentalCoroutinesApi::class)
val uiState: StateFlow<ShoppingUiState> = _query
    .flatMapLatest { text -> repository.search(text) }        // 👈 new query for each text
    .map { items -> ShoppingUiState(items = items, isLoading = false) }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ShoppingUiState())

fun onQueryChange(text: String) { _query.value = text }
```

💡 **`flatMapLatest`** = "for each new search text, start the **new** query and **stop** the old one." (It's marked experimental, so it needs `@OptIn(ExperimentalCoroutinesApi::class)`.) An empty text gives `'%%'` → matches **everything**. 😎 (Remember: the search `TextField` reads `query` **directly**, not through `uiState` — Chapter 18.)

**Task 6:**

| # | Bug | Fix |
|---|---|---|
| 1 | **No `@PrimaryKey`** → build error *"An entity must have at least 1 field annotated with @PrimaryKey"*. | `@PrimaryKey(autoGenerate = true) val id: Long = 0` |
| 2 | **`tags: List<String>`** with no Type Converter → *"Cannot figure out how to save this field…"*. | Add `Converters` + `@TypeConverters(Converters::class)` on the database. |
| 3 | **`suspend` + `Flow`** — a watching query shouldn't be `suspend`. | `fun observeAll(): Flow<List<Note>>` |

Bonus 🌟: `@Entity` with no `tableName` → the table is named after the class: `Note`. SQL table names don't care about upper/lower case, so `FROM note` works — but writing `@Entity(tableName = "notes")` and `FROM notes` is **clearer**.

---

## 22.27 Challenges 🚀

### Challenge 1: Several shopping lists 🗂️ ⭐⭐⭐
Let the user have **several** lists (🏠 Home, 🎉 Party, 🏕️ Camping). Make a second entity `ShoppingList(id, name)` and give `ShoppingItem` a `listId` column. Query: `SELECT * FROM shopping_items WHERE listId = :listId`.

### Challenge 2: Recipe Book — your own recipes ✍️ ⭐⭐⭐
Add an "**Add recipe**" screen to the Recipe Book that **inserts** a new recipe. (You'll need to add a function to the interface — and implement it in **both** repositories. Or follow 22.22's advice and redesign the interface first!)

### Challenge 3: Sort options ↕️ ⭐⭐
Add a menu: "Newest first" / "A → Z". Save the choice in **DataStore** (Chapter 21!) and use a different DAO query for each.

### Challenge 4: Offline jokes 😂📴 ⭐⭐⭐
In the **Joke Machine** (Chapter 19), save every loaded joke in Room. When there's **no internet**, show the **saved** jokes instead of an error. This pattern — the database as a **cache** of the internet — is used by most big apps! 🌐➡️🗃️➡️📱

### Challenge 5: Statistics 📊 ⭐⭐
Show "**You've bought 37 things this month 🛍️**". Instead of deleting bought items, keep them with a `boughtAt: Long?` time, and count them with SQL: `SELECT COUNT(*) FROM shopping_items WHERE boughtAt > :since`.

---

## 22.28 What Is Next?

Look at our AppContainers. In every project, they grow: Retrofit, the database, DAOs, repositories, scopes… and every ViewModel needs a **factory** with `this[APPLICATION_KEY] as ...`. 😓 Writing all that wiring by hand gets **boring** — and in big apps with 50 screens, **very** messy.

In **Chapter 23: Connecting the Pieces — Dependency Injection with Hilt**, you will learn:

- What **dependency injection** (DI) really means — you've **already been doing it** by hand! 💉
- **Hilt**: Google's library that does the wiring **for you** 🤖
- `@HiltAndroidApp`, `@AndroidEntryPoint`, `@Inject`, `@HiltViewModel`
- **Modules** with `@Provides` and `@Binds` — telling Hilt how to build Retrofit, Room, and repositories 🏗️
- **Scopes** like `@Singleton` — "only one in the whole app"
- **`hiltViewModel()`** — goodbye, ViewModel factories! 👋🏭
- Converting the **Recipe Book** to Hilt, and seeing how much code **disappears** ✂️

**Excellent work finishing Chapter 22! 🎉 Your apps can now remember thousands of things! 🗃️💪**
