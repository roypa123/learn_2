# Chapter 24: 🛠️ Mini Project — Notes App 📝✨

> **What you will do in this chapter**
>
> 1. **Plan** a complete, real app: requirements, screens, data, layers ✏️
> 2. Set up **all** the libraries from Part 5 at once 📦
> 3. Design a repository **for Room from day one** — `Flow` + `suspend` ✅
> 4. Build the **data layer**: Room (notes) + DataStore (settings) 🗃️📝
> 5. Wire everything with **Hilt** 🤖
> 6. Build the **notes list**: search 🔍, sort ↕️, pin 📌, colors 🎨, **swipe to delete with Undo** ↩️
> 7. Build the **note editor** with **auto-save** 💾 — even when the app goes to the background
> 8. Connect with **Navigation** 🧭
> 9. Test it with a big **checklist** ✅ — including process death 💀
> 10. Challenges to go further 🚀
>
> **Time needed:** about 6–8 hours. Spread it over a few days! 📅
>
> **What you need to know:** Chapters 1–23. This project uses almost **everything**.

---

## 24.1 What Are We Building? 🎯

A **notes app** — like Google Keep or Apple Notes, but made by **you**! 💪

```
 NOTES LIST                                       NOTE EDITOR
┌────────────────────────────────────┐           ┌────────────────────────────────────┐
│ My Notes 📝                     ↕️  │           │ ⬅️                        📌   🗑️   │
├────────────────────────────────────┤           ├────────────────────────────────────┤
│ 🔍 [ Search notes…            ✖️ ] │           │  ⚪ 🟡 🟢 🔵 🩷 🟣                   │
│ ╭────────────────────────────────╮ │   tap     │                                    │
│ │ Shopping 🛒                  📌 │ │ ───────▶  │  Shopping 🛒                        │
│ │ Milk, eggs, bread…             │ │           │                                    │
│ │ Edited 5 minutes ago           │ │           │  Milk, eggs, bread,                │
│ ╰────────────────────────────────╯ │           │  apples, cheese 🧀                  │
│ ╭────────────────────────────────╮ │  ◀── swipe│                                    │
│ │ Ideas 💡                     📌 │ │   left =  │                                    │
│ │ An app for my cat…             │ │   delete  │                                    │
│ │ Edited yesterday               │ │           │                                    │
│ ╰────────────────────────────────╯ │           │                                    │
│                              [ + ] │           │                                    │
│ ┌───────────────────────────────┐  │           │                                    │
│ │ "Ideas 💡" deleted      UNDO   │  │           │                                    │
│ └───────────────────────────────┘  │           │                                    │
└────────────────────────────────────┘           └────────────────────────────────────┘
```

### Requirements 📋

**Notes list:**
1. Shows all notes as **colored cards**: title, the start of the text, and "Edited 5 minutes ago". 🎨
2. **Pinned** notes 📌 are always at the **top**. Tap the pin to pin/unpin.
3. A **search box** 🔍 filters by title **or** text, while you type.
4. A **sort menu** ↕️: Last edited, Date created, or Title A → Z. The choice is **remembered** (DataStore).
5. **Swipe left** ⬅️ to delete, with an **Undo** ↩️ Snackbar.
6. A **+** button creates a new note.
7. Friendly messages when there are **no notes**, or **no search results**.

**Note editor:**
8. Edit the **title** and the **text**. Choose a **color**. **Pin** it. **Delete** it (with "Are you sure?").
9. **Auto-save** 💾: no Save button! The note is saved when you go **back**, and when the app goes to the **background**.
10. A **new** note that you leave **empty** is simply **not** saved (no empty junk notes).
11. Opening a note **without** changing it does **not** change its "Edited" time.

**Everywhere:**
12. Survives **rotation** 🔄, **process death** 💀, and **closing** the app 📴.

---

## 24.2 The Plan ✏️

### Screens and routes 🧭

| Screen | Route | Data it needs |
|---|---|---|
| Notes list | `NotesList` (object) | — |
| Note editor | `NoteEditor(noteId: Long = 0)` | **Which** note. `0` = a **new** note. |

> 💡 Why `0` for "new"? Room's `autoGenerate` ids start at **1**, so `0` is never a real note. Using a **special value** like this is simpler than a nullable route argument. We'll name it `NEW_NOTE_ID` so the code is easy to read.

### Where does each piece of data live? 🗺️

| Data | Where | Why |
|---|---|---|
| The **notes** | **Room** 🗃️ | Lots of items; search; must survive everything |
| The **sort order** | **DataStore** 📝 | One small setting |
| The **search text** | `ViewModel` (`MutableStateFlow`) | Only while the screen is open |
| "Just deleted" note (for Undo) | `ViewModel` | Only a few seconds |
| Title/text **while typing** | `ViewModel` (`MutableStateFlow`) → saved to **Room** on back / background | Fast typing ⌨️ + safe saving 💾 |
| Is a dialog/menu open? | `rememberSaveable` | Pure UI |

### The layers 🏗️

```
                 📱 UI LAYER                                🏪 DATA LAYER
┌──────────────────────────────────────┐     ┌──────────────────────────────────────────┐
│ NotesListScreen ⇄ NotesListViewModel ├──┬─▶│ NotesRepository ──▶ RoomNotesRepository  │──▶ 🗃️ Room
│ NoteEditorScreen ⇄ NoteEditorViewModel├──┤  │                                          │
└──────────────────────────────────────┘  └─▶│ UserPreferencesRepository ──▶ DataStore… │──▶ 📝 DataStore
                                              └──────────────────────────────────────────┘
                        🤖 Hilt builds and connects everything
```

### The files 📁

```
com.example.notes
 ├── NotesApplication.kt
 ├── MainActivity.kt
 ├── data/
 │    ├── model/
 │    │    └── Note.kt                         (Note, NoteColor, SortOrder, sorting)
 │    ├── local/
 │    │    ├── NoteEntity.kt                   (+ mappers)
 │    │    ├── NoteDao.kt
 │    │    └── NotesDatabase.kt
 │    ├── NotesRepository.kt                   (interface)
 │    ├── RoomNotesRepository.kt
 │    ├── UserPreferencesRepository.kt         (interface)
 │    └── DataStoreUserPreferencesRepository.kt
 ├── di/
 │    ├── DatabaseModule.kt
 │    ├── DataStoreModule.kt
 │    └── RepositoryModule.kt
 └── ui/
      ├── theme/                               (already there)
      ├── components/
      │    └── NoteColors.kt
      ├── navigation/
      │    ├── Routes.kt
      │    └── NotesNavHost.kt
      ├── list/
      │    ├── NotesListViewModel.kt
      │    ├── NotesListScreen.kt
      │    └── NoteCard.kt
      └── editor/
           ├── NoteEditorViewModel.kt
           └── NoteEditorScreen.kt
```

20 files — a **real** app! Don't worry: each one is small and has **one job**. 🧩

---

## 24.3 Step 1: Create the Project and Add Everything 📦

1. **File → New → New Project… → Empty Activity**.
2. **Name:** `Notes` · **Package:** `com.example.notes` · **Finish**.
3. Your theme is **`NotesTheme`**.

### `gradle/libs.versions.toml` — the complete Part 5 starter set 🧰

Add to the matching sections (keep everything that's already there):

```toml
[versions]
navigationCompose = "2.8.9"
kotlinxSerializationJson = "1.7.3"
room = "2.7.1"
ksp = "2.0.21-1.0.28"              # 👈 must fit YOUR Kotlin version (Chapter 22's table!)
hilt = "2.56.2"
hiltNavigationCompose = "1.2.0"
datastore = "1.1.4"

[libraries]
androidx-navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigationCompose" }
kotlinx-serialization-json = { group = "org.jetbrains.kotlinx", name = "kotlinx-serialization-json", version.ref = "kotlinxSerializationJson" }
androidx-lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycleRuntimeKtx" }
androidx-lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycleRuntimeKtx" }
androidx-room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
androidx-room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
androidx-room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-android-compiler = { group = "com.google.dagger", name = "hilt-android-compiler", version.ref = "hilt" }
androidx-hilt-navigation-compose = { group = "androidx.hilt", name = "hilt-navigation-compose", version.ref = "hiltNavigationCompose" }
androidx-datastore-preferences = { group = "androidx.datastore", name = "datastore-preferences", version.ref = "datastore" }

[plugins]
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
```

### `build.gradle.kts (Project: Notes)` — top level

```kotlin
plugins {
    // ... existing lines ...
    alias(libs.plugins.ksp) apply false
    alias(libs.plugins.hilt) apply false
}
```

### `build.gradle.kts (Module :app)`

```kotlin
plugins {
    // ... existing lines ...
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.ksp)
    alias(libs.plugins.hilt)
}

// ... android { } unchanged ...

dependencies {
    // ... existing lines ...
    implementation(libs.androidx.navigation.compose)
    implementation(libs.kotlinx.serialization.json)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    ksp(libs.androidx.room.compiler)
    implementation(libs.hilt.android)
    ksp(libs.hilt.android.compiler)
    implementation(libs.androidx.hilt.navigation.compose)
    implementation(libs.androidx.datastore.preferences)
}
```

**Sync Now** 🔄 ✅

> 📋 **Save this setup!** This is what a modern Android app uses: Compose + Navigation + ViewModel + Room + DataStore + Hilt. Add **Retrofit** (Chapter 19) and **Coil** (Chapter 20) when you need the internet, and you have the **full** toolbox. 🧰

### Make the packages

Right-click `com.example.notes` → **New → Package**: `data.model`, `data.local`, `di`, `ui.components`, `ui.navigation`, `ui.list`, `ui.editor`.

---

## 24.4 Step 2: The App Model 📦

### `data/model/Note.kt`

```kotlin
package com.example.notes.data.model

data class Note(                                                         // (1)
    val id: Long,
    val title: String,
    val content: String,
    val color: NoteColor,
    val isPinned: Boolean,
    val createdAt: Long,
    val updatedAt: Long
)

enum class NoteColor(val label: String) {                                // (2)
    DEFAULT("Default"),
    YELLOW("Yellow"),
    GREEN("Green"),
    BLUE("Blue"),
    PINK("Pink"),
    PURPLE("Purple")
}

enum class SortOrder(val label: String) {                                // (3)
    LAST_EDITED("Last edited ✏️"),
    DATE_CREATED("Date created 🗓️"),
    TITLE("Title A → Z 🔤")
}

fun List<Note>.sortedFor(order: SortOrder): List<Note> {                 // (4)
    val byOrder: Comparator<Note> = when (order) {
        SortOrder.LAST_EDITED -> compareByDescending { it.updatedAt }
        SortOrder.DATE_CREATED -> compareByDescending { it.createdAt }
        SortOrder.TITLE -> compareBy(String.CASE_INSENSITIVE_ORDER) { it.title }
    }
    return sortedWith(compareByDescending<Note> { it.isPinned }.then(byOrder))   // (5)
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `data class Note` | The **app model** — what screens and ViewModels use. No Room labels here (Chapter 22's lesson ✅). |
| 2 | `enum class NoteColor` | The 6 note colors. The **real** colors (`Color(...)`) live in the **UI** layer, because they depend on light/dark mode. The data layer only knows the **names**. |
| 3 | `enum class SortOrder` | The 3 ways to sort, with labels for the menu. |
| 4 | `fun List<Note>.sortedFor(order)` | An **extension function** (Chapter 4): every `List<Note>` can now sort itself: `notes.sortedFor(SortOrder.TITLE)`. |
| 5 | `compareByDescending<Note> { it.isPinned }.then(byOrder)` | Sort by **two** rules: first **pinned** (true before false — "descending", because `true` counts as bigger), **then** by the chosen order. 📌 always on top! |

### Comparators in simple words ⚖️

A **`Comparator`** is a rule that says which of two things comes **first**.

| Code | Rule |
|---|---|
| `compareBy { it.title }` | Smaller first (A → Z, 1 → 9) |
| `compareByDescending { it.updatedAt }` | **Bigger** first (newest time first) |
| `compareBy(String.CASE_INSENSITIVE_ORDER) { it.title }` | A → Z, **ignoring** upper/lower case ("apple" next to "Avocado", not after "Zebra") |
| `ruleA.then(ruleB)` | Use `ruleA`; if two items are **equal** by it, use `ruleB` to decide |

> 💡 **Why sort in Kotlin, not in SQL?** SQL can sort too (`ORDER BY`, Chapter 22) — but sorting by a **changing** setting needs complicated SQL. For a few hundred notes, sorting a list in Kotlin takes **less than a millisecond**. Simple code wins! 😎

---

## 24.5 Step 3: The Room Layer 🗃️

### `data/local/NoteEntity.kt`

```kotlin
package com.example.notes.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.notes.data.model.Note
import com.example.notes.data.model.NoteColor

@Entity(tableName = "notes")
data class NoteEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val title: String,
    val content: String,
    val color: String,                                                  // (1)
    val isPinned: Boolean,
    val createdAt: Long,
    val updatedAt: Long
)

fun NoteEntity.toNote(): Note = Note(
    id = id,
    title = title,
    content = content,
    color = NoteColor.entries.find { it.name == color } ?: NoteColor.DEFAULT,   // (2)
    isPinned = isPinned,
    createdAt = createdAt,
    updatedAt = updatedAt
)

fun Note.toEntity(): NoteEntity = NoteEntity(
    id = id,
    title = title,
    content = content,
    color = color.name,                                                 // (3)
    isPinned = isPinned,
    createdAt = createdAt,
    updatedAt = updatedAt
)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `val color: String` | The database stores the color's **name** (`"YELLOW"`), not an enum. |
| 2 | `entries.find { it.name == color } ?: NoteColor.DEFAULT` | The **safe** way back (Chapter 21): if a name is unknown, use the default — never crash. 🛡️ |
| 3 | `color.name` | Enum → text, for saving. |

### `data/local/NoteDao.kt`

```kotlin
package com.example.notes.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao
interface NoteDao {

    @Query(
        "SELECT * FROM notes " +
        "WHERE title LIKE '%' || :query || '%' OR content LIKE '%' || :query || '%'"   // (1)
    )
    fun observeNotes(query: String): Flow<List<NoteEntity>>

    @Query("SELECT * FROM notes WHERE id = :id")
    suspend fun getNote(id: Long): NoteEntity?                                         // (2)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(note: NoteEntity): Long                                         // (3)

    @Update
    suspend fun update(note: NoteEntity)

    @Query("DELETE FROM notes WHERE id = :id")
    suspend fun deleteById(id: Long)

    @Query("UPDATE notes SET isPinned = :isPinned WHERE id = :id")
    suspend fun setPinned(id: Long, isPinned: Boolean)                                 // (4)
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `WHERE title LIKE '%' \|\| :query \|\| '%' OR content LIKE ...` | Search in the title **or** the text (Chapter 22, Task 5). An **empty** query → `'%%'` → **all** notes. 🔍 The SQL is split over two lines with `+` just to keep it readable. |
| 2 | `suspend fun getNote(id): NoteEntity?` | Get **one** note, **once** (for the editor). `null` if it doesn't exist. |
| 3 | `insert(...): Long` with `REPLACE` | Returns the **new id**. `REPLACE` also lets **Undo** put a deleted note back with its **old** id. ↩️ |
| 4 | `setPinned(id, isPinned)` | Pin/unpin **without** touching `updatedAt` — pinning isn't "editing". |

### `data/local/NotesDatabase.kt`

```kotlin
package com.example.notes.data.local

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(entities = [NoteEntity::class], version = 1, exportSchema = false)
abstract class NotesDatabase : RoomDatabase() {
    abstract fun noteDao(): NoteDao
}
```

---

## 24.6 Step 4: The Repositories — Designed for Room From Day One ✅

Remember Chapter 22's lesson? 🎓 *"Use **`Flow`** for things you watch and **`suspend`** for actions."* Here it is:

### `data/NotesRepository.kt`

```kotlin
package com.example.notes.data

import com.example.notes.data.model.Note
import com.example.notes.data.model.NoteColor
import kotlinx.coroutines.flow.Flow

interface NotesRepository {
    fun observeNotes(query: String): Flow<List<Note>>                       // 👀 watch
    suspend fun getNote(id: Long): Note?                                    // ⚡ once
    suspend fun addNote(title: String, content: String, color: NoteColor, isPinned: Boolean): Long
    suspend fun updateNote(note: Note)
    suspend fun deleteNote(note: Note)
    suspend fun restoreNote(note: Note)
    suspend fun setPinned(id: Long, isPinned: Boolean)
}
```

Every action can be **awaited**, every list can be **watched**. Any future repository (in-memory for tests 🧪, or one that syncs to the internet ☁️) fits perfectly.

### `data/RoomNotesRepository.kt`

```kotlin
package com.example.notes.data

import com.example.notes.data.local.NoteDao
import com.example.notes.data.local.NoteEntity
import com.example.notes.data.local.toEntity
import com.example.notes.data.local.toNote
import com.example.notes.data.model.Note
import com.example.notes.data.model.NoteColor
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class RoomNotesRepository @Inject constructor(
    private val noteDao: NoteDao
) : NotesRepository {

    override fun observeNotes(query: String): Flow<List<Note>> =
        noteDao.observeNotes(query.trim())
            .map { entities -> entities.map { it.toNote() } }

    override suspend fun getNote(id: Long): Note? =
        noteDao.getNote(id)?.toNote()                                           // (1)

    override suspend fun addNote(
        title: String,
        content: String,
        color: NoteColor,
        isPinned: Boolean
    ): Long {
        val now = System.currentTimeMillis()
        return noteDao.insert(
            NoteEntity(
                title = title,
                content = content,
                color = color.name,
                isPinned = isPinned,
                createdAt = now,                                                 // (2)
                updatedAt = now
            )
        )
    }

    override suspend fun updateNote(note: Note) {
        noteDao.update(note.copy(updatedAt = System.currentTimeMillis()).toEntity())   // (3)
    }

    override suspend fun deleteNote(note: Note) {
        noteDao.deleteById(note.id)
    }

    override suspend fun restoreNote(note: Note) {
        noteDao.insert(note.toEntity())                                          // (4)
    }

    override suspend fun setPinned(id: Long, isPinned: Boolean) {
        noteDao.setPinned(id, isPinned)
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `noteDao.getNote(id)?.toNote()` | `?.` — if there's no such note, the result is `null` (Chapter 3). |
| 2 | `createdAt = now`, `updatedAt = now` | A new note is "created" and "edited" at the same moment. ⏰ |
| 3 | `note.copy(updatedAt = now)` | **The repository** sets the "edited" time — so **no** screen can forget it. 🛡️ |
| 4 | `noteDao.insert(note.toEntity())` | Undo: put the **exact** old note back, with its old id and times. ↩️ |

### `data/UserPreferencesRepository.kt`

```kotlin
package com.example.notes.data

import com.example.notes.data.model.SortOrder
import kotlinx.coroutines.flow.Flow

interface UserPreferencesRepository {
    val sortOrder: Flow<SortOrder>
    suspend fun setSortOrder(sortOrder: SortOrder)
}
```

### `data/DataStoreUserPreferencesRepository.kt`

```kotlin
package com.example.notes.data

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.emptyPreferences
import androidx.datastore.preferences.core.stringPreferencesKey
import com.example.notes.data.model.SortOrder
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import java.io.IOException
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class DataStoreUserPreferencesRepository @Inject constructor(
    private val dataStore: DataStore<Preferences>
) : UserPreferencesRepository {

    private val sortOrderKey = stringPreferencesKey("sort_order")

    override val sortOrder: Flow<SortOrder> = dataStore.data
        .catch { error -> if (error is IOException) emit(emptyPreferences()) else throw error }
        .map { preferences ->
            val savedName = preferences[sortOrderKey]
            SortOrder.entries.find { it.name == savedName } ?: SortOrder.LAST_EDITED
        }

    override suspend fun setSortOrder(sortOrder: SortOrder) {
        dataStore.edit { it[sortOrderKey] = sortOrder.name }
    }
}
```

Everything here is from **Chapter 21** — the same safe patterns: `catch` for `IOException`, enums saved by **name**, read back with `find`. 📝

---

## 24.7 Step 5: Hilt — Wiring It All 🤖

### `NotesApplication.kt`

```kotlin
package com.example.notes

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class NotesApplication : Application()
```

### `AndroidManifest.xml`

```xml
<application
    android:name=".NotesApplication"
    ... the rest stays the same ... >
```

### `di/DatabaseModule.kt`

```kotlin
package com.example.notes.di

import android.content.Context
import androidx.room.Room
import com.example.notes.data.local.NoteDao
import com.example.notes.data.local.NotesDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideNotesDatabase(@ApplicationContext context: Context): NotesDatabase =
        Room.databaseBuilder(context, NotesDatabase::class.java, "notes.db").build()

    @Provides
    fun provideNoteDao(database: NotesDatabase): NoteDao = database.noteDao()
}
```

### `di/DataStoreModule.kt`

```kotlin
package com.example.notes.di

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.preferencesDataStore
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

private val Context.userPreferencesDataStore: DataStore<Preferences>
    by preferencesDataStore(name = "user_preferences")                        // (1)

@Module
@InstallIn(SingletonComponent::class)
object DataStoreModule {

    @Provides
    @Singleton
    fun provideUserPreferencesDataStore(
        @ApplicationContext context: Context
    ): DataStore<Preferences> = context.userPreferencesDataStore              // (2)
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | Top-level `preferencesDataStore` delegate | Still the **one-per-file** rule from Chapter 21! The delegate guarantees **one** DataStore. 🫙 |
| 2 | `@Provides ... = context.userPreferencesDataStore` | Hand that **one** DataStore to whoever asks for a `DataStore<Preferences>`. |

### `di/RepositoryModule.kt`

```kotlin
package com.example.notes.di

import com.example.notes.data.DataStoreUserPreferencesRepository
import com.example.notes.data.NotesRepository
import com.example.notes.data.RoomNotesRepository
import com.example.notes.data.UserPreferencesRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent

@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    abstract fun bindNotesRepository(impl: RoomNotesRepository): NotesRepository

    @Binds
    abstract fun bindUserPreferencesRepository(
        impl: DataStoreUserPreferencesRepository
    ): UserPreferencesRepository
}
```

Exactly the **Chapter 23 pattern**: builder-made things → `@Provides`; interfaces → `@Binds`; our classes → `@Inject constructor` + `@Singleton`. ✅

> 🔨 **Build now!** (**Build → Make Project**.) Room and Hilt check everything **before** we write any screen. Fix any errors now — it's much easier while the app is small. 🛡️

---

## 24.8 Step 6: Note Colors and Routes 🎨🧭

### `ui/components/NoteColors.kt`

```kotlin
package com.example.notes.ui.components

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import com.example.notes.data.model.NoteColor

@Composable
fun NoteColor.toComposeColor(): Color {                                   // (1)
    val dark = isSystemInDarkTheme()                                      // (2)
    return when (this) {
        NoteColor.DEFAULT -> MaterialTheme.colorScheme.surfaceContainerHigh   // (3)
        NoteColor.YELLOW -> if (dark) Color(0xFF5C4B00) else Color(0xFFFFF59D)
        NoteColor.GREEN -> if (dark) Color(0xFF1E4D2B) else Color(0xFFC8E6C9)
        NoteColor.BLUE -> if (dark) Color(0xFF1A3A5C) else Color(0xFFBBDEFB)
        NoteColor.PINK -> if (dark) Color(0xFF5C1F3A) else Color(0xFFF8BBD0)
        NoteColor.PURPLE -> if (dark) Color(0xFF3F2A5C) else Color(0xFFE1BEE7)
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `@Composable fun NoteColor.toComposeColor()` | An extension function that is **also** a Composable — because it reads the **theme**. Usage: `note.color.toComposeColor()`. |
| 2 | `isSystemInDarkTheme()` | Is the phone in dark mode? 🌙 |
| 3 | `surfaceContainerHigh` | "Default" = a soft theme color that works in **both** modes. |

**Light** mode → light **pastel** colors with dark text. **Dark** mode → deep colors with light text. The text color (`onSurface`) flips **automatically** with the theme, so it's always readable. 👀✅ (`Color(0xFF...)` — Chapter 7.)

### `ui/navigation/Routes.kt`

```kotlin
package com.example.notes.ui.navigation

import kotlinx.serialization.Serializable

const val NEW_NOTE_ID = 0L

@Serializable
object NotesList

@Serializable
data class NoteEditor(val noteId: Long = NEW_NOTE_ID)
```

`NoteEditor()` → a **new** note. `NoteEditor(noteId = 5)` → edit note 5. ✨

---

## 24.9 Step 7: The Notes List ViewModel 🧠

### `ui/list/NotesListViewModel.kt`

```kotlin
package com.example.notes.ui.list

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.notes.data.NotesRepository
import com.example.notes.data.UserPreferencesRepository
import com.example.notes.data.model.Note
import com.example.notes.data.model.SortOrder
import com.example.notes.data.model.sortedFor
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

data class NotesListUiState(
    val notes: List<Note> = emptyList(),
    val sortOrder: SortOrder = SortOrder.LAST_EDITED,
    val isSearching: Boolean = false,
    val isLoading: Boolean = true,
    val recentlyDeleted: Note? = null                                       // (1)
)

@OptIn(ExperimentalCoroutinesApi::class)
@HiltViewModel
class NotesListViewModel @Inject constructor(
    private val notesRepository: NotesRepository,
    private val preferencesRepository: UserPreferencesRepository
) : ViewModel() {

    private val _query = MutableStateFlow("")
    val query: StateFlow<String> = _query.asStateFlow()                     // (2)

    private val _recentlyDeleted = MutableStateFlow<Note?>(null)

    private val notesForQuery = _query
        .flatMapLatest { query -> notesRepository.observeNotes(query) }     // (3)

    val uiState: StateFlow<NotesListUiState> = combine(                     // (4)
        notesForQuery,
        preferencesRepository.sortOrder,
        _query,
        _recentlyDeleted
    ) { notes, sortOrder, query, recentlyDeleted ->
        NotesListUiState(
            notes = notes.sortedFor(sortOrder),                             // (5)
            sortOrder = sortOrder,
            isSearching = query.isNotBlank(),
            isLoading = false,
            recentlyDeleted = recentlyDeleted
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = NotesListUiState()
    )

    fun onQueryChange(newQuery: String) {
        _query.value = newQuery
    }

    fun onSortOrderChange(sortOrder: SortOrder) {
        viewModelScope.launch { preferencesRepository.setSortOrder(sortOrder) }
    }

    fun onPinClick(note: Note) {
        viewModelScope.launch { notesRepository.setPinned(note.id, !note.isPinned) }
    }

    fun onDeleteNote(note: Note) {
        viewModelScope.launch {
            notesRepository.deleteNote(note)
            _recentlyDeleted.value = note                                   // (6)
        }
    }

    fun onUndoDelete() {
        val note = _recentlyDeleted.value ?: return                         // (7)
        _recentlyDeleted.value = null
        viewModelScope.launch { notesRepository.restoreNote(note) }
    }

    fun onUndoTimeout() {
        _recentlyDeleted.value = null                                       // (8)
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `recentlyDeleted: Note?` | The note that was **just** deleted — kept for a few seconds so **Undo** can bring it back. `null` = nothing to undo. |
| 2 | `query` (separate) | The search text, read **directly** by the text field (Chapter 18's rule ⌨️). |
| 3 | `_query.flatMapLatest { ... }` | For **every** new search text, start watching a **new** Room query and **stop** the old one (Chapter 22, Task 5). Type "sho" → only notes containing "sho". 🔍 |
| 4 | `combine(4 flows) { ... }` | Whenever **any** of the four changes — notes, sort order, search text, deleted note — build a **new** `NotesListUiState`. 🍹 (Chapter 18) |
| 5 | `notes.sortedFor(sortOrder)` | Our sorting function: pinned first, then the chosen order. |
| 6 | `_recentlyDeleted.value = note` | **After** deleting, remember the note. The screen sees it and shows the Snackbar. 📢 |
| 7 | `?: return` | Nothing to undo? Then do nothing. |
| 8 | `onUndoTimeout()` | The Snackbar disappeared without Undo → forget the note. It's **really** gone now. 👋 |

> 🎯 **The "message in the state" pattern again:** the ViewModel can't show a Snackbar (Chapter 15's rule). So it puts `recentlyDeleted` into the state, the **screen** shows the Snackbar, and then tells the ViewModel what happened (`onUndoDelete` or `onUndoTimeout`).

---

## 24.10 Step 8: The Note Card and Swipe to Delete 🃏⬅️

### `ui/list/NoteCard.kt`

```kotlin
package com.example.notes.ui.list

import android.text.format.DateUtils
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.SwipeToDismissBox
import androidx.compose.material3.SwipeToDismissBoxValue
import androidx.compose.material3.Text
import androidx.compose.material3.rememberSwipeToDismissBoxState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.example.notes.data.model.Note
import com.example.notes.ui.components.toComposeColor

@Composable
fun NoteCard(
    note: Note,
    onClick: () -> Unit,
    onPinClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        onClick = onClick,
        colors = CardDefaults.cardColors(containerColor = note.color.toComposeColor()),   // (1)
        modifier = modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(start = 16.dp, end = 4.dp, bottom = 16.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = note.title.ifBlank { "Untitled" },                     // (2)
                    style = MaterialTheme.typography.titleMedium,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,                             // (3)
                    modifier = Modifier.weight(1f)
                )
                IconButton(
                    onClick = onPinClick,
                    modifier = Modifier.semantics {                               // (4)
                        contentDescription = if (note.isPinned) "Unpin note" else "Pin note"
                    }
                ) {
                    Text("📌", modifier = Modifier.alpha(if (note.isPinned) 1f else 0.25f))   // (5)
                }
            }
            if (note.content.isNotBlank()) {
                Text(
                    text = note.content,
                    style = MaterialTheme.typography.bodyMedium,
                    maxLines = 4,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.padding(end = 12.dp)
                )
            }
            Text(
                text = editedText(note.updatedAt),
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

fun editedText(updatedAt: Long): String {                                         // (6)
    val now = System.currentTimeMillis()
    if (now - updatedAt < DateUtils.MINUTE_IN_MILLIS) return "Edited just now"
    val relative = DateUtils.getRelativeTimeSpanString(updatedAt, now, DateUtils.MINUTE_IN_MILLIS)
    return "Edited $relative"
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SwipeToDelete(
    onDelete: () -> Unit,
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit                                               // (7)
) {
    val currentOnDelete by rememberUpdatedState(onDelete)                         // (8)
    val dismissState = rememberSwipeToDismissBoxState(
        confirmValueChange = { value ->                                           // (9)
            if (value == SwipeToDismissBoxValue.EndToStart) {
                currentOnDelete()
                true
            } else {
                false
            }
        }
    )

    SwipeToDismissBox(
        state = dismissState,
        enableDismissFromStartToEnd = false,                                      // (10)
        backgroundContent = {                                                     // (11)
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .clip(CardDefaults.shape)
                    .background(MaterialTheme.colorScheme.errorContainer)
                    .padding(horizontal = 24.dp),
                contentAlignment = Alignment.CenterEnd
            ) {
                Icon(
                    Icons.Filled.Delete,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onErrorContainer
                )
            }
        },
        modifier = modifier
    ) {
        content()
    }
}
```

**The important parts:**

| # | Code | Meaning |
|---|---|---|
| 1 | `CardDefaults.cardColors(containerColor = ...)` | The card's background = the note's color. 🎨 |
| 2 | `note.title.ifBlank { "Untitled" }` | A note can have **no** title — show "Untitled" instead of an empty line. |
| 3 | `maxLines = 1`, `overflow = TextOverflow.Ellipsis` | Too long? Cut it and add **"…"** at the end. ✂️ |
| 4 | `Modifier.semantics { contentDescription = ... }` | Our "icon" is an emoji, so we tell **screen readers** ♿ what the button does: "Pin note" / "Unpin note". |
| 5 | `Modifier.alpha(if (note.isPinned) 1f else 0.25f)` | Pinned → a bright 📌. Not pinned → a faded, see-through one. (`alpha` = how **visible**: 1 = fully, 0 = invisible.) |
| 6 | `editedText(updatedAt)` | Android's **`DateUtils.getRelativeTimeSpanString`** turns a time into friendly words: "5 minutes ago", "Yesterday", "3 days ago"… **in the phone's language!** 🌍 Under one minute → "just now". |
| 7 | `content: @Composable () -> Unit` | A **slot** (Chapter 11): whatever goes **inside** the swipe box (our card). |
| 8 | `rememberUpdatedState(onDelete)` | The swipe state is **remembered**, but `onDelete` may change (for example, after pinning, it holds the **new** note). This keeps a **fresh** copy of the latest `onDelete`, so the remembered state always calls the newest one. 🔄 |
| 9 | `confirmValueChange = { value -> ... }` | Called when a swipe **finishes**. `EndToStart` = swiped **right to left** ⬅️ → delete and say `true` ("yes, let it go"). Anything else → `false` (snap back). |
| 10 | `enableDismissFromStartToEnd = false` | Only **left** swipes are allowed. |
| 11 | `backgroundContent = { ... }` | What's **behind** the card as it slides away: a red area with a 🗑️ icon on the right. |

> ℹ️ `SwipeToDismissBox` is still changing between Material 3 versions. If Android Studio shows `confirmValueChange` as **deprecated** (crossed out), it still works. Newer versions also offer an `onDismiss` parameter on `SwipeToDismissBox` itself.

---

## 24.11 Step 9: The Notes List Screen 📋

### `ui/list/NotesListScreen.kt`

```kotlin
package com.example.notes.ui.list

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarDuration
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.SnackbarResult
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.notes.data.model.Note
import com.example.notes.data.model.NoteColor
import com.example.notes.data.model.SortOrder
import com.example.notes.ui.theme.NotesTheme

@Composable
fun NotesListRoute(
    onNoteClick: (Long) -> Unit,
    onAddClick: () -> Unit,
    viewModel: NotesListViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val query by viewModel.query.collectAsStateWithLifecycle()

    NotesListScreen(
        uiState = uiState,
        query = query,
        onQueryChange = viewModel::onQueryChange,
        onSortOrderChange = viewModel::onSortOrderChange,
        onNoteClick = onNoteClick,
        onPinClick = viewModel::onPinClick,
        onDeleteNote = viewModel::onDeleteNote,
        onUndoDelete = viewModel::onUndoDelete,
        onUndoTimeout = viewModel::onUndoTimeout,
        onAddClick = onAddClick
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NotesListScreen(
    uiState: NotesListUiState,
    query: String,
    onQueryChange: (String) -> Unit,
    onSortOrderChange: (SortOrder) -> Unit,
    onNoteClick: (Long) -> Unit,
    onPinClick: (Note) -> Unit,
    onDeleteNote: (Note) -> Unit,
    onUndoDelete: () -> Unit,
    onUndoTimeout: () -> Unit,
    onAddClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val snackbarHostState = remember { SnackbarHostState() }
    var showSortMenu by rememberSaveable { mutableStateOf(false) }

    LaunchedEffect(uiState.recentlyDeleted) {                                     // (1)
        val deleted = uiState.recentlyDeleted ?: return@LaunchedEffect            // (2)
        val result = snackbarHostState.showSnackbar(
            message = "\"${deleted.title.ifBlank { "Untitled" }}\" deleted 🗑️",
            actionLabel = "Undo",
            duration = SnackbarDuration.Short
        )
        if (result == SnackbarResult.ActionPerformed) onUndoDelete() else onUndoTimeout()   // (3)
    }

    Scaffold(
        modifier = modifier,
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {
            TopAppBar(
                title = { Text("My Notes 📝") },
                actions = {
                    Box {                                                         // (4)
                        IconButton(onClick = { showSortMenu = true }) {
                            Text("↕️")
                        }
                        DropdownMenu(
                            expanded = showSortMenu,
                            onDismissRequest = { showSortMenu = false }
                        ) {
                            SortOrder.entries.forEach { order ->
                                DropdownMenuItem(
                                    text = { Text(order.label) },
                                    onClick = {
                                        onSortOrderChange(order)
                                        showSortMenu = false
                                    },
                                    trailingIcon = {
                                        if (order == uiState.sortOrder) {         // (5)
                                            Icon(Icons.Filled.Check, contentDescription = "Selected")
                                        }
                                    }
                                )
                            }
                        }
                    }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = onAddClick) {
                Icon(Icons.Filled.Add, contentDescription = "New note")
            }
        }
    ) { innerPadding ->
        Column(modifier = Modifier.padding(innerPadding)) {
            OutlinedTextField(
                value = query,
                onValueChange = onQueryChange,
                placeholder = { Text("Search notes…") },
                leadingIcon = { Icon(Icons.Filled.Search, contentDescription = null) },
                trailingIcon = {
                    if (query.isNotEmpty()) {                                     // (6)
                        IconButton(onClick = { onQueryChange("") }) {
                            Icon(Icons.Filled.Clear, contentDescription = "Clear search")
                        }
                    }
                },
                singleLine = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp)
            )

            when {
                uiState.isLoading -> CenteredBox { CircularProgressIndicator() }
                uiState.notes.isEmpty() && uiState.isSearching ->                 // (7)
                    CenteredBox { Text("No notes match \"$query\" 🔍", textAlign = TextAlign.Center) }
                uiState.notes.isEmpty() ->
                    CenteredBox { Text("No notes yet 📝\nTap + to write your first one!", textAlign = TextAlign.Center) }
                else -> LazyColumn(
                    contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 88.dp),   // (8)
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                    modifier = Modifier.fillMaxSize()
                ) {
                    items(uiState.notes, key = { note -> note.id }) { note ->
                        SwipeToDelete(
                            onDelete = { onDeleteNote(note) },
                            modifier = Modifier.animateItem()                     // (9)
                        ) {
                            NoteCard(
                                note = note,
                                onClick = { onNoteClick(note.id) },
                                onPinClick = { onPinClick(note) }
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun CenteredBox(content: @Composable () -> Unit) {                       // (10)
    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(32.dp),
        contentAlignment = Alignment.Center
    ) {
        content()
    }
}

@Preview(showBackground = true)
@Composable
fun NotesListScreenPreview() {
    val now = System.currentTimeMillis()
    NotesTheme {
        NotesListScreen(
            uiState = NotesListUiState(
                notes = listOf(
                    Note(1, "Shopping 🛒", "Milk, eggs, bread, apples", NoteColor.YELLOW, true, now, now),
                    Note(2, "Ideas 💡", "An app for my cat that…", NoteColor.BLUE, false, now, now - 3_600_000),
                    Note(3, "", "A note without a title", NoteColor.DEFAULT, false, now, now - 86_400_000)
                ),
                isLoading = false
            ),
            query = "",
            onQueryChange = {}, onSortOrderChange = {}, onNoteClick = {}, onPinClick = {},
            onDeleteNote = {}, onUndoDelete = {}, onUndoTimeout = {}, onAddClick = {}
        )
    }
}
```

**The important parts:**

| # | Code | Meaning |
|---|---|---|
| 1 | `LaunchedEffect(uiState.recentlyDeleted)` | Every time a **new** note is deleted, this restarts and shows a Snackbar (Chapter 18's pattern). |
| 2 | `?: return@LaunchedEffect` | Nothing deleted (`null`)? Leave the effect early. `return@LaunchedEffect` = "return from **this** lambda". |
| 3 | `if (result == ActionPerformed) onUndoDelete() else onUndoTimeout()` | `showSnackbar` **waits** until the Snackbar is gone, then tells us **why**: Undo tapped ↩️, or time ran out ⏰. |
| 4 | `Box { IconButton; DropdownMenu }` | The menu opens **next to** its button because they share a `Box` (Chapter 11). |
| 5 | `if (order == uiState.sortOrder) Icon(Check)` | A ✓ next to the **current** choice. |
| 6 | `if (query.isNotEmpty())` | The ✖️ clear button only appears when there's text to clear. |
| 7 | `isEmpty() && isSearching` | Two **different** empty messages: "no results for your search" vs "no notes at all". Small details make apps feel **smart**. 🧠 |
| 8 | `bottom = 88.dp` | Extra space at the end, so the **+** button never covers the last card. |
| 9 | `Modifier.animateItem()` | Cards **slide** smoothly when the order changes (pinning!) or a card is deleted. ✨ |
| 10 | `private fun CenteredBox(content)` | A tiny helper — **one** place for "centered message" layout, used **three** times. ♻️ |

---

## 24.12 Step 10: The Editor ViewModel — With Auto-Save 💾

This is the **smartest** class in the app. Let's think first. 🤔

**When should we save?** There's no Save button, so:

| Moment | Why |
|---|---|
| The user goes **back** ⬅️ | They're done. Save, **then** leave. |
| The app goes to the **background** 📲 (Home button, a phone call…) | Android **may kill** the app later (process death 💀). Saving to Room **now** means nothing is lost. |

**What should "save" do?** It depends:

| Situation | Action |
|---|---|
| **New** note, still **empty** | Nothing — no junk notes 🗑️ |
| **New** note with text | **Insert** it, and remember its new **id** |
| **Existing** note, now **empty** | **Delete** it |
| **Existing** note, **changed** | **Update** it (new "Edited" time) |
| **Existing** note, **not changed** | Nothing — keep its "Edited" time ✅ |

### `ui/editor/NoteEditorViewModel.kt`

```kotlin
package com.example.notes.ui.editor

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.navigation.toRoute
import com.example.notes.data.NotesRepository
import com.example.notes.data.model.Note
import com.example.notes.data.model.NoteColor
import com.example.notes.ui.navigation.NEW_NOTE_ID
import com.example.notes.ui.navigation.NoteEditor
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import javax.inject.Inject

data class NoteEditorUiState(
    val title: String = "",
    val content: String = "",
    val color: NoteColor = NoteColor.DEFAULT,
    val isPinned: Boolean = false,
    val isLoading: Boolean = true,
    val isFinished: Boolean = false                                            // (1)
)

private const val KEY_SAVED_NOTE_ID = "saved_note_id"

@HiltViewModel
class NoteEditorViewModel @Inject constructor(
    private val savedStateHandle: SavedStateHandle,
    private val notesRepository: NotesRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(NoteEditorUiState())
    val uiState: StateFlow<NoteEditorUiState> = _uiState.asStateFlow()

    private var savedNote: Note? = null                                        // (2)
    private val saveMutex = Mutex()                                            // (3)

    init {
        val noteId: Long = savedStateHandle[KEY_SAVED_NOTE_ID]                 // (4)
            ?: savedStateHandle.toRoute<NoteEditor>().noteId

        if (noteId == NEW_NOTE_ID) {
            _uiState.update { it.copy(isLoading = false) }
        } else {
            viewModelScope.launch {
                val note = notesRepository.getNote(noteId)
                savedNote = note
                _uiState.update {
                    if (note == null) {
                        it.copy(isLoading = false, isFinished = true)          // (5)
                    } else {
                        it.copy(
                            title = note.title,
                            content = note.content,
                            color = note.color,
                            isPinned = note.isPinned,
                            isLoading = false
                        )
                    }
                }
            }
        }
    }

    // ---------- Events from the screen ----------

    fun onTitleChange(title: String) = _uiState.update { it.copy(title = title) }

    fun onContentChange(content: String) = _uiState.update { it.copy(content = content) }

    fun onColorChange(color: NoteColor) = _uiState.update { it.copy(color = color) }

    fun onPinToggle() = _uiState.update { it.copy(isPinned = !it.isPinned) }

    fun onBackClick() {                                                        // (6)
        viewModelScope.launch {
            saveNow()
            _uiState.update { it.copy(isFinished = true) }
        }
    }

    fun onAppInBackground() {                                                  // (7)
        viewModelScope.launch { saveNow() }
    }

    fun onDeleteConfirmed() {
        viewModelScope.launch {
            saveMutex.withLock {
                savedNote?.let { notesRepository.deleteNote(it) }
                savedNote = null
                _uiState.update { it.copy(isFinished = true) }
            }
        }
    }

    // ---------- Saving ----------

    private suspend fun saveNow() = saveMutex.withLock {                       // (8)
        val state = _uiState.value
        if (state.isLoading || state.isFinished) return@withLock               // (9)

        val isEmpty = state.title.isBlank() && state.content.isBlank()
        val current = savedNote

        when {
            current == null && isEmpty -> Unit                                 // (10) new + empty

            current == null -> {                                               // (11) new + text
                val newId = notesRepository.addNote(
                    title = state.title,
                    content = state.content,
                    color = state.color,
                    isPinned = state.isPinned
                )
                savedStateHandle[KEY_SAVED_NOTE_ID] = newId
                savedNote = notesRepository.getNote(newId)
            }

            isEmpty -> {                                                       // (12) existing + empty
                notesRepository.deleteNote(current)
                savedStateHandle[KEY_SAVED_NOTE_ID] = NEW_NOTE_ID
                savedNote = null
            }

            else -> {                                                          // (13) existing
                val edited = current.copy(
                    title = state.title,
                    content = state.content,
                    color = state.color,
                    isPinned = state.isPinned
                )
                if (edited != current) {                                       // (14)
                    notesRepository.updateNote(edited)
                    savedNote = notesRepository.getNote(current.id)
                }
            }
        }
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `isFinished` | "The editor is done — please go back." The **screen** watches this and navigates (the ViewModel can't navigate itself — Chapter 15). |
| 2 | `savedNote: Note?` | The version that's **in the database** right now. `null` = not saved yet. We compare against it to know if anything **changed**. |
| 3 | `private val saveMutex = Mutex()` | A **lock** 🔒. See the box below! |
| 4 | `savedStateHandle[KEY_SAVED_NOTE_ID] ?: ...toRoute<NoteEditor>().noteId` | Which note? Normally the one from the **route**. But if a **new** note was already saved and then the app died 💀, we stored its **new id** in the `SavedStateHandle` — use **that**, so we don't create a **second** copy! 🛡️ |
| 5 | `note == null → isFinished = true` | The note doesn't exist (maybe deleted elsewhere) → just go back. |
| 6 | `onBackClick()` | Save **first**, **then** say "finished". The order matters: if we navigated away first, the ViewModel would be cleared and its coroutines **cancelled** — maybe in the middle of saving! 😱 |
| 7 | `onAppInBackground()` | Save, but **stay** on the screen. |
| 8 | `saveMutex.withLock { ... }` | Only **one** save at a time. |
| 9 | `if (isLoading \|\| isFinished) return@withLock` | Don't save before the note is **loaded** (we'd save an empty note over it!), or after we're done (for example, after **deleting**). |
| 10–13 | `when { ... }` | Exactly the 5 situations from the table above. ✅ |
| 11 | `savedStateHandle[KEY_SAVED_NOTE_ID] = newId` | Remember the new id — survives process death 💾 (point 4). |
| 14 | `if (edited != current)` | `data class` `!=` compares **all** the values (Chapter 3). Nothing changed → no update → the "Edited" time stays the same. ✅ |

> 🔒 **What is a `Mutex`?** Imagine a bathroom with **one key** 🔑. Whoever has the key goes in; everyone else **waits** for the key. `saveMutex.withLock { ... }` = "take the key, do this, give the key back."
>
> **Why do we need it?** The user presses **Back** at the exact moment the app goes to the background. Two saves start at the same time! Both see `savedNote == null`… and both **insert** → **two** copies of the note! 👯 With the mutex, the second save **waits**; by then `savedNote` is set, so it **updates** instead. ✅ (`Mutex` comes from `kotlinx.coroutines.sync`; it **suspends** while waiting — it doesn't block the thread.)

> 💡 `fun onTitleChange(title: String) = _uiState.update { ... }` — a **one-line function** (Chapter 2). The text goes **straight** into a `MutableStateFlow` — fast and safe for typing ⌨️ (Chapter 18's rule).

---

## 24.13 Step 11: The Editor Screen ✍️

### `ui/editor/NoteEditorScreen.kt`

```kotlin
package com.example.notes.ui.editor

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LifecycleEventEffect
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.notes.data.model.NoteColor
import com.example.notes.ui.components.toComposeColor
import com.example.notes.ui.theme.NotesTheme

@Composable
fun NoteEditorRoute(
    onNavigateBack: () -> Unit,
    viewModel: NoteEditorViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(uiState.isFinished) {                                         // (1)
        if (uiState.isFinished) onNavigateBack()
    }

    LifecycleEventEffect(Lifecycle.Event.ON_STOP) {                              // (2)
        viewModel.onAppInBackground()
    }

    BackHandler {                                                                // (3)
        viewModel.onBackClick()
    }

    NoteEditorScreen(
        uiState = uiState,
        onTitleChange = viewModel::onTitleChange,
        onContentChange = viewModel::onContentChange,
        onColorChange = viewModel::onColorChange,
        onPinToggle = viewModel::onPinToggle,
        onBackClick = viewModel::onBackClick,
        onDeleteConfirmed = viewModel::onDeleteConfirmed
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NoteEditorScreen(
    uiState: NoteEditorUiState,
    onTitleChange: (String) -> Unit,
    onContentChange: (String) -> Unit,
    onColorChange: (NoteColor) -> Unit,
    onPinToggle: () -> Unit,
    onBackClick: () -> Unit,
    onDeleteConfirmed: () -> Unit,
    modifier: Modifier = Modifier
) {
    var showDeleteDialog by rememberSaveable { mutableStateOf(false) }

    Scaffold(
        modifier = modifier,
        containerColor = uiState.color.toComposeColor(),                         // (4)
        topBar = {
            TopAppBar(
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent),
                title = { },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(
                        onClick = onPinToggle,
                        modifier = Modifier.semantics {
                            contentDescription = if (uiState.isPinned) "Unpin note" else "Pin note"
                        }
                    ) {
                        Text("📌", modifier = Modifier.alpha(if (uiState.isPinned) 1f else 0.25f))
                    }
                    IconButton(onClick = { showDeleteDialog = true }) {
                        Icon(Icons.Filled.Delete, contentDescription = "Delete note")
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .padding(innerPadding)
                .fillMaxSize()
                .imePadding()                                                    // (5)
        ) {
            ColorPicker(
                selected = uiState.color,
                onColorChange = onColorChange,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
            )

            val transparentColors = TextFieldDefaults.colors(                    // (6)
                focusedContainerColor = Color.Transparent,
                unfocusedContainerColor = Color.Transparent,
                focusedIndicatorColor = Color.Transparent,
                unfocusedIndicatorColor = Color.Transparent
            )

            TextField(
                value = uiState.title,
                onValueChange = onTitleChange,
                placeholder = { Text("Title", style = MaterialTheme.typography.headlineSmall) },
                textStyle = MaterialTheme.typography.headlineSmall,
                singleLine = true,
                keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Sentences),
                colors = transparentColors,
                enabled = !uiState.isLoading,
                modifier = Modifier.fillMaxWidth()
            )
            TextField(
                value = uiState.content,
                onValueChange = onContentChange,
                placeholder = { Text("Write something… ✍️") },
                textStyle = MaterialTheme.typography.bodyLarge,
                keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Sentences),
                colors = transparentColors,
                enabled = !uiState.isLoading,
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)                                                  // (7)
            )
        }
    }

    if (showDeleteDialog) {
        AlertDialog(
            onDismissRequest = { showDeleteDialog = false },
            title = { Text("Delete this note?") },
            text = { Text("This can't be undone.") },
            confirmButton = {
                TextButton(onClick = {
                    showDeleteDialog = false
                    onDeleteConfirmed()
                }) {
                    Text("Delete", color = MaterialTheme.colorScheme.error)
                }
            },
            dismissButton = {
                TextButton(onClick = { showDeleteDialog = false }) { Text("Cancel") }
            }
        )
    }
}

@Composable
fun ColorPicker(
    selected: NoteColor,
    onColorChange: (NoteColor) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        NoteColor.entries.forEach { color ->
            val isSelected = color == selected
            Box(
                modifier = Modifier
                    .size(36.dp)
                    .clip(CircleShape)
                    .background(color.toComposeColor())
                    .border(                                                     // (8)
                        width = if (isSelected) 3.dp else 1.dp,
                        color = if (isSelected) MaterialTheme.colorScheme.primary
                                else MaterialTheme.colorScheme.outline,
                        shape = CircleShape
                    )
                    .clickable(role = Role.RadioButton) { onColorChange(color) }
                    .semantics {
                        contentDescription = color.label + if (isSelected) ", selected" else ""
                    }
            )
        }
    }
}

@Preview(showBackground = true)
@Composable
fun NoteEditorScreenPreview() {
    NotesTheme {
        NoteEditorScreen(
            uiState = NoteEditorUiState(
                title = "Shopping 🛒",
                content = "Milk, eggs, bread,\napples, cheese 🧀",
                color = NoteColor.YELLOW,
                isPinned = true,
                isLoading = false
            ),
            onTitleChange = {}, onContentChange = {}, onColorChange = {},
            onPinToggle = {}, onBackClick = {}, onDeleteConfirmed = {}
        )
    }
}
```

**The important parts:**

| # | Code | Meaning |
|---|---|---|
| 1 | `LaunchedEffect(uiState.isFinished) { if (...) onNavigateBack() }` | When the ViewModel says "finished", go back. This happens **after** saving is done. ✅ |
| 2 | `LifecycleEventEffect(Lifecycle.Event.ON_STOP) { ... }` | Runs every time the screen gets **`ON_STOP`** — the app went to the **background** (Chapter 14). → Save! 💾 Android stops an app **before** it may kill it, so this save always comes in time. |
| 3 | `BackHandler { viewModel.onBackClick() }` | The phone's **Back** gesture/button would normally just leave. We **catch** it (Chapter 13) and save first. Both the ⬅️ arrow **and** the system Back now do the same thing. |
| 4 | `containerColor = uiState.color.toComposeColor()` | The **whole** editor takes the note's color. Change the color → the background changes **instantly**. 🎨 The top bar is `Transparent`, so the color shows through. |
| 5 | `.imePadding()` | When the **keyboard** ⌨️ opens, add space at the bottom so the text you're typing isn't hidden **behind** it. (IME = the on-screen keyboard.) |
| 6 | `TextFieldDefaults.colors(... Color.Transparent ...)` | Text fields with **no** box and **no** underline — it looks like writing on **paper** 📄. |
| 7 | `.weight(1f)` on the content field | The text area fills **all** the remaining height — tap anywhere below the title to start typing. |
| 8 | `.border(...)` | The **selected** color gets a thick, colored ring; the others a thin grey one. `Role.RadioButton` tells screen readers ♿ "pick one of these". |

---

## 24.14 Step 12: Navigation and MainActivity 🧭

### `ui/navigation/NotesNavHost.kt`

```kotlin
package com.example.notes.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.notes.ui.editor.NoteEditorRoute
import com.example.notes.ui.list.NotesListRoute

@Composable
fun NotesNavHost() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = NotesList) {

        composable<NotesList> {
            NotesListRoute(
                onNoteClick = { id -> navController.navigate(NoteEditor(noteId = id)) },
                onAddClick = { navController.navigate(NoteEditor()) }
            )
        }

        composable<NoteEditor> {
            NoteEditorRoute(
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}
```

The editor's ViewModel reads `noteId` from its **own** `SavedStateHandle` (Hilt gives it for free — Chapter 23), so the NavHost doesn't pass it. ✅

### `MainActivity.kt`

```kotlin
package com.example.notes

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.notes.ui.navigation.NotesNavHost
import com.example.notes.ui.theme.NotesTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            NotesTheme {
                NotesNavHost()
            }
        }
    }
}
```

**Run it!** ▶️ 🎉 Write a few notes, give them colors, pin one, search, sort, swipe one away and **Undo** it. **You built a real notes app!** 📝✨

---

## 24.15 Follow a Note Through the Whole App 🔍

Let's follow **one** note from birth to deletion, to see every layer work together:

```
1. 👆 Tap +                     → navigate(NoteEditor())   → noteId = 0 (NEW_NOTE_ID)
2. 🧠 NoteEditorViewModel       → new note: isLoading = false, empty fields
3. ⌨️ Type "Shopping 🛒"         → onTitleChange → MutableStateFlow → screen (instantly)
4. 🎨 Tap 🟡                     → onColorChange → the whole screen turns yellow
5. ⬅️ Press Back                 → BackHandler → onBackClick()
6. 💾 saveNow()                  → savedNote == null + not empty → addNote(...) → Room INSERT → id = 7
7. ✅ isFinished = true          → LaunchedEffect → popBackStack()
8. 🌊 Room                       → "notes table changed!" → observeNotes("") sends a new list
9. 🧠 NotesListViewModel         → combine → sortedFor(LAST_EDITED) → new uiState
10. 📋 List                      → the yellow "Shopping 🛒" card appears at the top ✨
11. ⬅️ Swipe it left             → onDeleteNote → Room DELETE → recentlyDeleted = note
12. 📢 LaunchedEffect            → Snackbar "Shopping 🛒" deleted — UNDO
13. ↩️ Tap UNDO                  → onUndoDelete → restoreNote → Room INSERT (id 7 again)
14. 🌊 Room → list               → the card slides back in ✨
```

**Fourteen steps — and you wrote every one of them.** 🏆

---

## 24.16 Test Checklist ✅

### The list 📋

| Test | Expected | ✓ |
|---|---|---|
| First start | "No notes yet 📝 Tap + to write your first one!" | ☐ |
| Create 4 notes with different colors | 4 colored cards, newest first | ☐ |
| Card text | Long titles end with "…"; text shows max 4 lines | ☐ |
| "Edited …" | "Edited just now"; after a few minutes: "Edited 3 minutes ago" | ☐ |
| Pin a note 📌 | It slides to the **top**; the pin is bright | ☐ |
| Pin 2 notes | Both on top, in the chosen order between them | ☐ |
| Search "sho" | Only notes with "sho" in the title **or** text | ☐ |
| Search "zzz" | "No notes match "zzz" 🔍" | ☐ |
| Clear search ✖️ | All notes back | ☐ |
| Sort ↕️ → Title A → Z | Sorted by title (pinned still first); ✓ next to the choice | ☐ |
| Close and reopen the app | Sort order **remembered** (DataStore 📝) | ☐ |
| Swipe a card left | Red background + 🗑️, card disappears, Snackbar with UNDO | ☐ |
| Tap UNDO | The note comes back, **same** place, same color, same "Edited" time | ☐ |
| Swipe, wait for the Snackbar to go | The note is gone for good | ☐ |
| Swipe right | Nothing happens (only left is allowed) | ☐ |

### The editor ✍️

| Test | Expected | ✓ |
|---|---|---|
| + → type nothing → Back | **No** new note in the list | ☐ |
| + → type a title → Back (arrow) | Note saved ✅ | ☐ |
| + → type → **system** Back gesture | Also saved ✅ (BackHandler) | ☐ |
| Open a note → Back without changes | Its "Edited" time does **not** change | ☐ |
| Change the color | The whole editor changes color 🎨 | ☐ |
| Open a note, delete all text → Back | The note is **deleted** | ☐ |
| Delete 🗑️ → Cancel | Nothing happens | ☐ |
| Delete 🗑️ → Delete | Back to the list; note gone | ☐ |
| Long text + keyboard open | You can always see what you type (`imePadding`) | ☐ |

### Survival 🔄💀📴

| Test | Expected | ✓ |
|---|---|---|
| Rotate while typing | Text, color, pin all stay | ☐ |
| Type in a **new** note → **Home** → reopen from Recents | Text still there (and already saved!) | ☐ |
| Type in a **new** note → Home → `adb shell am kill com.example.notes` → reopen | Same note, **one** copy only (not two!) 💾 (`KEY_SAVED_NOTE_ID`) | ☐ |
| Edit an existing note → Home → kill → reopen | Changes are there | ☐ |
| Swipe the app away from Recents, reopen | All notes, pins, colors, sort order ✅ | ☐ |
| Dark mode 🌙 | Deep note colors, light text, everything readable | ☐ |

> 💡 **The process-death test** is the one most apps fail! 💀 Remember from Chapter 14: `adb shell am kill` only works while the app is in the **background**. Your app passes because it **saves on `ON_STOP`** and remembers the new id in **`SavedStateHandle`**. 🏆

---

## 24.17 What You Practiced 🎓

| Chapter | Used in the Notes app |
|---|---|
| 3–4 | Data classes and `copy`, `!=` on data classes, enums, extension functions, `?.let`, `?:`, comparators |
| 6–7 | Layouts, `weight`, `imePadding`, colors for light/dark mode, `CircleShape`, `border`, `alpha` |
| 9 | Text fields (transparent style, capitalization), `Role.RadioButton` |
| 10 | `LazyColumn`, keys, `animateItem`, `contentPadding` |
| 11 | `Scaffold`, `TopAppBar`, FAB, `DropdownMenu`, Snackbar with action, `AlertDialog` |
| 13 | Type-safe routes with a default argument, `BackHandler`, `popBackStack` |
| 14 | `LifecycleEventEffect(ON_STOP)`, process death testing |
| 15 | `@HiltViewModel` ViewModels, `UiState`, events, `SavedStateHandle`, Route + Screen, previews |
| 16 | Layers, repository interfaces, app models |
| 18 | `combine`, `flatMapLatest`, `stateIn`, `LaunchedEffect`, `Mutex`, `viewModelScope` |
| 21 | DataStore for the sort order, safe enum reading |
| 22 | Room: entity, DAO, `LIKE` search, `REPLACE` for Undo, mappers |
| 23 | Hilt: `@HiltAndroidApp`, `@AndroidEntryPoint`, `@Provides`, `@Binds`, `@Singleton`, `hiltViewModel()` |

🎉 **You finished Part 5!** You can now build **real, data-driven** Android apps — the same way professional teams do. That's a **huge** achievement! 🏔️🏆

---

## 24.18 Troubleshooting 🔧

| Problem | Likely cause | Fix |
|---|---|---|
| Build fails mentioning KSP/Kotlin versions | KSP doesn't fit Kotlin | Chapter 22's table. |
| `[Dagger/MissingBinding] …DataStore<Preferences>…` | `DataStoreModule` missing or not `@InstallIn` | Check the module (24.7). |
| Crash: *Hilt Activity must be attached to an @HiltAndroidApp Application* | Manifest `android:name` missing | `android:name=".NotesApplication"` |
| New note saved **twice** after process death | `KEY_SAVED_NOTE_ID` not saved/read | Check `init` and the "new + text" branch in `saveNow`. |
| Opening a note changes its "Edited" time | Saving even when nothing changed | The `if (edited != current)` check. |
| Empty notes appear in the list | Saving new empty notes | The "new + empty → Unit" branch. |
| The note isn't saved when pressing the **system** Back | No `BackHandler` | Add it in `NoteEditorRoute`. |
| Swipe deletes, but Undo brings back an **old** version | Missing `rememberUpdatedState` | See 24.10, point 8. |
| Search doesn't update while typing | Not using `flatMapLatest` | See 24.9, point 3. |
| `SwipeToDismissBox` or `confirmValueChange` is red/crossed out | Different Material 3 version | Add `@OptIn(ExperimentalMaterial3Api::class)`; deprecated still works. |
| Text hidden behind the keyboard | Missing `imePadding()` | Add it to the editor's `Column`. |

---

## 24.19 Challenges 🚀

### Challenge 1: Grid view 🔲 ⭐⭐
Add a button to switch between a **list** and a **2-column grid** (`LazyVerticalStaggeredGrid` — cards of different heights, like Google Keep!). Save the choice in **DataStore**.

### Challenge 2: Undo in the editor ↩️ ⭐⭐
When a note is deleted from the **editor**, show the "deleted — UNDO" Snackbar on the **list** screen too.
*Hint:* the list ViewModel can't see the editor's ViewModel. One idea: give the repository a `MutableStateFlow<Note?>` of "recently deleted" notes that both screens can use.

### Challenge 3: Checklists ☑️ ⭐⭐⭐
Let a note be a **checklist**: each line starts with ☐ or ☑, and tapping a line toggles it.
*Hint:* keep it as text! `content.lines()` gives the lines; `"☐ Milk"` ↔ `"☑ Milk"`. No database change needed. 😎

### Challenge 4: Labels 🏷️ ⭐⭐⭐
Add labels like "Work", "Home", "Ideas". Each note can have **one** label. Show label chips above the list to filter.
*Hint:* a new column in `NoteEntity` → **version 2** + a **migration** (Chapter 22)!

### Challenge 5: Share a note 📤 ⭐⭐
Add a **Share** button in the editor that sends the note's title and text to other apps (Chapter 20, Challenge 4's `ACTION_SEND` idea).

### Challenge 6: Auto-save while typing ⏱️ ⭐⭐⭐
Also save **2 seconds after the user stops typing** — not only on Back and background.
*Hint:* in the ViewModel's `init`, collect `_uiState` with `.debounce(2_000)` (Chapter 18) and call `saveNow()`. Think: does the `Mutex` still protect you? (Yes! 🔒)

### Challenge 7: Tests 🧪 ⭐⭐⭐
Write a `FakeNotesRepository` (in memory, `Flow` + `suspend` — easy, thanks to our interface!). We'll use it in **Chapter 27** to test the ViewModels without a database.

---

## 24.20 What Is Next?

🎉 **Part 5 complete!** Our apps can show screens, talk to the internet, and remember everything. Now let's make them use the **phone itself**! 📱✨

In **Part 6 — Phone Features and Polish**, starting with **Chapter 25: Using Phone Features**, you will learn:

- **Permissions** — asking the user nicely for camera, location, notifications 🔑
- The **Photo Picker** — choosing pictures from the gallery 🖼️ (no permission needed!)
- The **camera** — taking a photo 📸
- **Location** — where am I? 📍
- **Notifications** — sending messages to the user 🔔
- **WorkManager** — doing work in the background, even after the app is closed ⏰
- Adding a **photo** to your notes, and a **daily reminder** notification 🔔📝

**Incredible work finishing Chapter 24! 🎉 You built a complete, professional app — from an empty project to a polished notes app. Be proud! 🏆📝**
