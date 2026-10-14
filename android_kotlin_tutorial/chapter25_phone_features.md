# Chapter 25: Using Phone Features 📱🔑📸📍🔔

> **What you will learn in this chapter**
>
> 1. How apps live in their own **safe room** — and why they must **ask** 🏠🔑
> 2. **Permissions**: normal vs. runtime, the asking flow, and the golden rules 🙋
> 3. The **Activity Result API** — "go somewhere, then come back with an answer" ↩️
> 4. 📍 **Location**: a small "**Where Am I?**" app
> 5. 🖼️ The **Photo Picker** — choosing pictures **without** any permission
> 6. 📸 The **camera** — taking a photo with **FileProvider**
> 7. 💾 Saving photos in the app's **own storage**
> 8. 🔔 **Notifications** — channels, permission, and building a notification
> 9. ⏰ **WorkManager** — work that runs even when the app is **closed**
> 10. 🛠️ Upgrading the **Notes app**: a **photo** in each note and a **daily reminder**!
>
> **Time needed:** about 6 hours. Two parts — take a break in between! ☕
>
> **What you need to know:** Chapters 1–24, especially 14 (lifecycle), 22 (Room migrations), 23 (Hilt), and 24 (Notes app).

---

## 25.1 Your App Lives in a Safe Room 🏠

Every Android app lives in its **own private room** — called a **sandbox** 🏖️. Inside its room, an app can do what it wants: save files, use its database, draw its screens.

But some things are **outside** the room, and they belong to the **user**:

- 📸 The **camera** (it could secretly take pictures!)
- 📍 The **location** (it could follow you everywhere!)
- 🖼️ The user's **photos**
- 🎤 The **microphone**
- 👥 The **contacts**
- 🔔 Sending **notifications** (it could spam you!)

To use these, an app must **ask for permission** — just like a guest knocks 🚪✊ before entering someone's bedroom.

> 🛡️ This protects **everyone** — including **you**, as a phone user. Good apps ask **only** for what they really need, and only **when** they need it.

---

## 25.2 Permissions — Two Kinds 🔑

| Kind | Asked how? | Examples | What you do |
|---|---|---|---|
| **Normal** (install-time) | **Never** — allowed automatically 🟢 | Internet, vibrate, set alarms | Just write it in the **manifest** |
| **Runtime** (dangerous) | A **pop-up** ❓ while the app runs | Location, camera, microphone, contacts, notifications (Android 13+) | Manifest **and** ask in code |

You already used a **normal** permission: `INTERNET` (Chapter 19) — no pop-up. 👍

**Runtime** permissions need **two** steps:

1. **Declare** it in `AndroidManifest.xml`: "*My app might need this.*" 📜
2. **Ask** the user in code, at the right moment: "*May I use it now?*" 🙋

### The asking flow 🔁

```
User taps "Find my location 📍"
        │
        ▼
Do we already have permission? ──YES──▶ ✅ Use the feature
        │ NO
        ▼
Show Android's pop-up:  "Allow My App to access this device's location?"
        │                    [While using the app]  [Only this time]  [Don't allow]
        ▼
   ┌────┴─────┐
 Allowed ✅   Denied ❌
   │            │
 Use it      Explain kindly and keep working without it 🙂
             (and offer a way to open Settings later)
```

> ⚠️ **After the user says "Don't allow" twice**, Android **stops showing** the pop-up for that permission. Asking again does **nothing** — the answer comes back as "denied" immediately. The only way left: send the user to the app's page in **Settings** ⚙️.

### The golden rules of asking 🏆

| Rule | ✅ Good | ❌ Bad |
|---|---|---|
| **Ask in context** | Ask for location when the user taps "Find my location 📍" | Ask for everything the moment the app opens |
| **Explain why** | "We need your location to show the weather where you are" | No explanation |
| **Ask only for what you need** | Approximate location for weather | Precise location for a weather app |
| **Accept "no"** | The app still works; the feature is just off | Closing the app or asking again and again 😤 |

---

## 25.3 The Activity Result API — "Go and Come Back" ↩️

Asking for a permission, picking a photo, taking a picture… they all work the **same** way:

1. Your app **opens** something else (a pop-up, the photo picker, the camera app). 🚀
2. The user does something there.
3. Your app **gets an answer back**. 📬

Like sending a friend to the shop 🏪: "Please buy bread and **tell me** if they had it."

In Compose, you prepare this with **`rememberLauncherForActivityResult`**:

```kotlin
val launcher = rememberLauncherForActivityResult(           // (1)
    contract = ActivityResultContracts.RequestPermission()   // (2)
) { isGranted: Boolean ->                                    // (3)
    // the answer arrives here
}

Button(onClick = { launcher.launch(Manifest.permission.CAMERA) }) {   // (4)
    Text("Ask")
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `rememberLauncherForActivityResult(...)` | Prepare a **launcher** 🚀 — the "go and come back" tool. Remembered across recompositions (and even process death!). |
| 2 | `contract = ...` | **What** kind of trip: ask a permission? pick a photo? take a picture? |
| 3 | `{ answer -> ... }` | What to do with the **answer** when it comes back. |
| 4 | `launcher.launch(input)` | **Go!** The input depends on the contract (here: which permission). |

### The contracts you'll use in this chapter 📜

| Contract | Input (`launch(...)`) | Answer | For |
|---|---|---|---|
| `RequestPermission()` | one permission name | `Boolean` (granted?) | One permission |
| `RequestMultiplePermissions()` | an **array** of names | `Map<String, Boolean>` | Several at once |
| `PickVisualMedia()` | `PickVisualMediaRequest(...)` | `Uri?` (the photo, or `null`) | Photo Picker 🖼️ |
| `TakePicture()` | a `Uri` where to **save** the photo | `Boolean` (photo taken?) | Camera 📸 |

> ⚠️ Create launchers **at the top** of a Composable (like `remember`), **not** inside `onClick`. Then call `.launch(...)` inside `onClick`.

---

# Part A: 📍 Where Am I?

## 25.4 A Small Location App 🗺️

Let's build a tiny screen in **MyFirstApp**: tap a button → see your location → open it in a map.

```
┌──────────────────────────────┐
│            📍                 │
│         Where Am I?           │
│                               │
│  Latitude:   48.8584          │
│  Longitude:  2.2945           │
│  (accuracy: about 20 m)       │
│                               │
│   [ Find my location 📍 ]      │
│   [ Open in Maps 🗺️ ]          │
└──────────────────────────────┘
```

### Latitude and longitude? 🌍

Every place on Earth has **two numbers**:

| Number | Meaning | Range |
|---|---|---|
| **Latitude** | How far **north** (+) or **south** (−) of the equator | −90 to 90 |
| **Longitude** | How far **east** (+) or **west** (−) of London (Greenwich) | −180 to 180 |

The Eiffel Tower 🗼 is at latitude **48.8584**, longitude **2.2945**.

### Step 1: Libraries 📦

Google's **Fused Location Provider** is the best way to get the location. "Fused" = it **mixes** GPS 🛰️, Wi-Fi 📶, and phone towers 📡 to get a good answer **fast**, while saving battery 🔋.

**`gradle/libs.versions.toml`**:

```toml
[versions]
playServicesLocation = "21.3.0"
coroutinesPlayServices = "1.9.0"

[libraries]
play-services-location = { group = "com.google.android.gms", name = "play-services-location", version.ref = "playServicesLocation" }
kotlinx-coroutines-play-services = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-play-services", version.ref = "coroutinesPlayServices" }
```

**`build.gradle.kts (Module :app)`**:

```kotlin
implementation(libs.play.services.location)
implementation(libs.kotlinx.coroutines.play.services)
```

**Sync** 🔄 ✅

| Library | Why |
|---|---|
| `play-services-location` | The Fused Location Provider. |
| `kotlinx-coroutines-play-services` | Google's location library uses an older "callback" style called **`Task`**. This library adds **`.await()`**, so we can use it like a `suspend` function. 😎 |

### Step 2: Declare the permissions 📜

In `AndroidManifest.xml`, above `<application`:

```xml
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

| Permission | Accuracy | Like… |
|---|---|---|
| `ACCESS_COARSE_LOCATION` | **Approximate** — about 1–3 km | "I'm somewhere in this neighborhood" 🏘️ |
| `ACCESS_FINE_LOCATION` | **Precise** — a few meters | "I'm at this exact door" 🚪 |

> 💡 Since Android 12, you must ask for **both** together, and the **user chooses**: the pop-up has a "**Precise**" / "**Approximate**" option. Your app must work with **either**!

### Step 3: Get the location (a suspend function) 📍

Make a new file **`LocationHelper.kt`** in MyFirstApp:

```kotlin
package com.example.myfirstapp

import android.Manifest
import android.annotation.SuppressLint
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import androidx.core.content.ContextCompat
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import kotlinx.coroutines.tasks.await

fun hasLocationPermission(context: Context): Boolean =                        // (1)
    ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_COARSE_LOCATION) ==
        PackageManager.PERMISSION_GRANTED

@SuppressLint("MissingPermission")                                            // (2)
suspend fun getCurrentLocation(context: Context): Location? {
    if (!hasLocationPermission(context)) return null                          // (3)
    val client = LocationServices.getFusedLocationProviderClient(context)     // (4)
    return client
        .getCurrentLocation(Priority.PRIORITY_BALANCED_POWER_ACCURACY, null)  // (5)
        .await()                                                              // (6)
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `ContextCompat.checkSelfPermission(...) == PERMISSION_GRANTED` | "Do we **already** have this permission?" We check **coarse** — if the user allowed precise, coarse is allowed too. |
| 2 | `@SuppressLint("MissingPermission")` | Android Studio can't see that we check the permission (in another function), so it warns. This label says "**I know, I checked.**" Use it only when you **really** check! |
| 3 | `if (!hasLocationPermission(context)) return null` | Safety first: no permission → no location. 🛡️ |
| 4 | `getFusedLocationProviderClient(context)` | Get the location "**helper**". |
| 5 | `getCurrentLocation(PRIORITY_BALANCED_POWER_ACCURACY, null)` | "Find where we are **now**." `BALANCED` = good accuracy, kind to the battery 🔋 (good for most apps). `HIGH_ACCURACY` uses GPS 🛰️ more. The `null` means "no way to cancel" (we don't need one). |
| 6 | `.await()` | Wait for the answer **without blocking** (thanks to `kotlinx-coroutines-play-services`). The result can be **`null`** — for example if location is **turned off** in the phone's settings. |

### Step 4: The screen, with the permission flow 🙋

```kotlin
@Composable
fun WhereAmIScreen() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var location by remember { mutableStateOf<Location?>(null) }
    var message by remember { mutableStateOf("Tap the button to find your location.") }

    fun findLocation() {                                                        // (1)
        scope.launch {
            message = "Looking… 🛰️"
            val result = getCurrentLocation(context)
            location = result
            message = if (result == null) {
                "Couldn't find your location. Is Location turned on in Settings? 📍"
            } else {
                "Found you! 🎉"
            }
        }
    }

    val permissionLauncher = rememberLauncherForActivityResult(                 // (2)
        contract = ActivityResultContracts.RequestMultiplePermissions()
    ) { answers: Map<String, Boolean> ->
        val anyGranted = answers.values.any { it }                              // (3)
        if (anyGranted) {
            findLocation()
        } else {
            message = "No problem! 🙂 Without location, I can't show where you are. " +
                "You can allow it later in Settings."
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("📍", style = MaterialTheme.typography.displayLarge)
        Text("Where Am I?", style = MaterialTheme.typography.headlineMedium)

        location?.let { loc ->                                                  // (4)
            Text("Latitude:  ${"%.4f".format(loc.latitude)}")
            Text("Longitude: ${"%.4f".format(loc.longitude)}")
            Text("(accuracy: about ${loc.accuracy.toInt()} m)", style = MaterialTheme.typography.labelMedium)
        }
        Text(message, textAlign = TextAlign.Center)

        Button(onClick = {
            if (hasLocationPermission(context)) {                               // (5)
                findLocation()
            } else {
                permissionLauncher.launch(                                      // (6)
                    arrayOf(
                        Manifest.permission.ACCESS_FINE_LOCATION,
                        Manifest.permission.ACCESS_COARSE_LOCATION
                    )
                )
            }
        }) {
            Text("Find my location 📍")
        }

        location?.let { loc ->
            OutlinedButton(onClick = {
                val uri = Uri.parse("geo:${loc.latitude},${loc.longitude}?q=${loc.latitude},${loc.longitude}")   // (7)
                try {
                    context.startActivity(Intent(Intent.ACTION_VIEW, uri))
                } catch (e: ActivityNotFoundException) {                        // (8)
                    message = "No map app found on this phone 🗺️❌"
                }
            }) {
                Text("Open in Maps 🗺️")
            }
        }
    }
}
```

Imports (press **Alt + Enter** on red words, or add these):

```kotlin
import android.Manifest
import android.content.ActivityNotFoundException
import android.content.Intent
import android.location.Location
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.platform.LocalContext
import kotlinx.coroutines.launch
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `fun findLocation()` (local function) | Used in **two** places: when we already have permission, and right after the user allows it. ♻️ |
| 2 | `rememberLauncherForActivityResult(RequestMultiplePermissions())` | A launcher for asking **several** permissions in **one** pop-up. |
| 3 | `answers.values.any { it }` | The answer is a **map**: permission → allowed? If **either** coarse **or** fine was allowed, we can continue. (The user may pick "Approximate" → only coarse is `true`.) |
| 4 | `location?.let { ... }` | Show the numbers only when we **have** a location. `"%.4f".format(...)` → 4 digits after the dot: `48.8584`. |
| 5 | `if (hasLocationPermission(context))` | Already allowed? Don't ask again — just go. ✅ |
| 6 | `permissionLauncher.launch(arrayOf(FINE, COARSE))` | Show Android's pop-up. (Ask for both — Android 12+ requires it.) |
| 7 | `"geo:lat,lng?q=lat,lng"` | A special **geo** link. Any map app knows how to open it. 🗺️ `q=` puts a **pin** there. |
| 8 | `catch (e: ActivityNotFoundException)` | Some phones (and many emulators) have **no** map app → `startActivity` would **crash**. Always protect "open another app" calls. 🛡️ |

### Try it! 🧪

**On the emulator:** the emulator has a **fake** location. Click **⋮ (Extended controls) → Location**, search a place (try "Eiffel Tower"), and click **Set location**. Then tap the button in your app. 🗼

| Try this | What happens |
|---|---|
| First tap | Android's pop-up: **Precise** / **Approximate**, and **While using the app** / **Only this time** / **Don't allow** |
| Choose Approximate | Works — the numbers are less exact |
| Choose Don't allow | Our kind message 🙂 — the app keeps working |
| Tap again, Don't allow again | Next time, **no pop-up** appears at all (Android remembers the "no") |
| Turn Location off in the phone's quick settings | "Couldn't find your location…" |

> 🔧 **Reset permissions while testing:** long-press your app icon → **App info → Permissions** → change them. Or uninstall and reinstall the app.

### Sending the user to Settings ⚙️

After two "no"s, the only way is the app's **Settings** page. You can open it for the user:

```kotlin
val intent = Intent(
    Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
    Uri.fromParts("package", context.packageName, null)
)
context.startActivity(intent)
```

(Import: `android.provider.Settings`.) Show it as a button like "**Open Settings ⚙️**" after a denial — never automatically.

---

# Part B: Upgrading the Notes App 📝📸🔔

## 25.5 The Plan ✏️

Open your **Notes** project from Chapter 24. We'll add **two** features:

| Feature | Uses | Permission needed? |
|---|---|---|
| 🖼️ **Add a photo from the gallery** | Photo Picker | ❌ **None!** |
| 📸 **Take a photo** | Camera app + FileProvider | ❌ **None!** (we use the camera **app**, not the camera itself) |
| 🔔 **Daily reminder** "Time to write a note! ✍️" at 8 PM | Notifications + WorkManager | ✅ `POST_NOTIFICATIONS` (Android 13+) |

```
NOTE EDITOR                                 NOTES LIST
┌──────────────────────────────────┐       ┌──────────────────────────────────┐
│ ⬅️              🖼️  📸  📌  🗑️    │       │ My Notes 📝               🔔  ↕️  │
├──────────────────────────────────┤       ├──────────────────────────────────┤
│ ⚪ 🟡 🟢 🔵 🩷 🟣                  │       │ ╭──────────────────────────────╮ │
│ ┌──────────────────────────✖️┐   │       │ │ [photo] Trip 🏔️            📌 │ │
│ │                            │   │       │ │         Amazing view…        │ │
│ │       (the photo)          │   │       │ ╰──────────────────────────────╯ │
│ └────────────────────────────┘   │       └──────────────────────────────────┘
│ Trip 🏔️                          │
│ Amazing view from the top…       │       🔔 8:00 PM  "Time to write a note! ✍️"
└──────────────────────────────────┘
```

### New and changed files 📁

```
data/
 ├── model/Note.kt                     ✏️ + photoPath
 ├── local/NoteEntity.kt               ✏️ + photoPath
 ├── local/NotesDatabase.kt            ✏️ version 2 + migration
 ├── NotesRepository.kt                ✏️ addNote(… photoPath)
 ├── RoomNotesRepository.kt            ✏️
 ├── PhotoStorage.kt                   🆕
 ├── UserPreferencesRepository.kt      ✏️ + reminderEnabled
 └── DataStoreUserPreferencesRepository.kt  ✏️
di/DatabaseModule.kt                   ✏️ addMigrations
notifications/                         🆕
 ├── NotificationHelper.kt             🆕
 ├── ReminderWorker.kt                 🆕
 └── ReminderScheduler.kt              🆕
NotesApplication.kt                    ✏️ create the channel
ui/editor/…                            ✏️ photo buttons + photo
ui/list/…                              ✏️ thumbnail + 🔔 button
res/xml/file_paths.xml                 🆕
res/drawable/ic_notification.xml       🆕
AndroidManifest.xml                    ✏️ provider + permission
```

### New libraries 📦

```toml
[versions]
coil = "3.1.0"
work = "2.10.1"

[libraries]
coil-compose = { group = "io.coil-kt.coil3", name = "coil-compose", version.ref = "coil" }
androidx-work-runtime-ktx = { group = "androidx.work", name = "work-runtime-ktx", version.ref = "work" }
```

```kotlin
implementation(libs.coil.compose)
implementation(libs.androidx.work.runtime.ktx)
```

**Sync** 🔄 ✅

> 💡 Coil **without** `coil-network-okhttp` this time! We only show photos from **files on the phone**, not from the internet. 📁 (Chapter 20)

---

## 25.6 Step 1: A Photo Column — Database Version 2 🗃️🚚

Each note can have **one** photo (or none). We'll save the photo **file's path** (like `/data/user/0/com.example.notes/files/note_photos/photo_1718.jpg`) in a new column.

Changing a table → **migration** time (Chapter 22)! 🚚

### `data/model/Note.kt` — add one property

```kotlin
data class Note(
    val id: Long,
    val title: String,
    val content: String,
    val color: NoteColor,
    val isPinned: Boolean,
    val createdAt: Long,
    val updatedAt: Long,
    val photoPath: String? = null                         // 👈 new (null = no photo)
)
```

### `data/local/NoteEntity.kt`

```kotlin
@Entity(tableName = "notes")
data class NoteEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val title: String,
    val content: String,
    val color: String,
    val isPinned: Boolean,
    val createdAt: Long,
    val updatedAt: Long,
    val photoPath: String? = null                         // 👈 new
)
```

…and add `photoPath = photoPath` to **both** mappers (`toNote()` and `toEntity()`).

### `data/local/NotesDatabase.kt`

```kotlin
package com.example.notes.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase

@Database(entities = [NoteEntity::class], version = 2, exportSchema = false)   // 👈 1 → 2
abstract class NotesDatabase : RoomDatabase() {
    abstract fun noteDao(): NoteDao
}

val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE notes ADD COLUMN photoPath TEXT")            // (1)
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `ADD COLUMN photoPath TEXT` | A **text** column that **may be empty** (no `NOT NULL`) — matches `String?` in Kotlin. Old notes get `NULL` = no photo. ✅ |

### `di/DatabaseModule.kt` — use the migration

```kotlin
Room.databaseBuilder(context, NotesDatabase::class.java, "notes.db")
    .addMigrations(MIGRATION_1_2)                         // 👈 new
    .build()
```

### `data/NotesRepository.kt` and `RoomNotesRepository.kt`

Add a `photoPath` parameter to `addNote`:

```kotlin
// NotesRepository
suspend fun addNote(
    title: String, content: String, color: NoteColor, isPinned: Boolean, photoPath: String?
): Long

// RoomNotesRepository — inside addNote, in the NoteEntity(...):
photoPath = photoPath,
```

(`updateNote` needs no change — it saves the whole `Note`, which now includes `photoPath`.)

> 🧪 **Test the migration:** your phone still has notes from Chapter 24 (version 1). Run the app **without uninstalling** → all old notes are still there ✅. If it crashes with *"Room cannot verify the data integrity"*, check that `version = 2` **and** `.addMigrations(...)` are both there.

---

## 25.7 Step 2: Where Do Photos Live? 💾📁

### Why copy the photo into our app? 🤔

When the user picks a photo from the gallery, we get a **`Uri`** — an **address** of the photo, like `content://media/picker/0/...`. 📬

We **could** just save that address. But:

- The user might **delete** the photo from the gallery → our note shows a broken picture 💔
- Our **permission** to read that address may **expire** after the app restarts 🔑⏰

So we **copy** the photo into our app's **own private folder**. Now it's **ours** — safe forever (until the note is deleted). 🏠✅

### The app's own storage 📂

Every app has a **private folder**, reached with **`context.filesDir`**. No permission needed — it's inside our safe room. 🏠 Other apps can't see it, and it's deleted when the app is uninstalled.

```
/data/user/0/com.example.notes/files/          ← context.filesDir
 └── note_photos/                               ← our folder
      ├── photo_1718000000000.jpg
      └── photo_1718000555000.jpg
```

### `data/PhotoStorage.kt`

```kotlin
package com.example.notes.data

import android.content.Context
import android.net.Uri
import androidx.core.content.FileProvider
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.io.IOException
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class PhotoStorage @Inject constructor(
    @ApplicationContext private val context: Context                          // (1)
) {

    private val photosDir: File
        get() = File(context.filesDir, "note_photos").apply { mkdirs() }      // (2)

    fun createPhotoFile(): File =
        File(photosDir, "photo_${System.currentTimeMillis()}.jpg")            // (3)

    fun uriForFile(file: File): Uri =
        FileProvider.getUriForFile(context, "${context.packageName}.fileprovider", file)   // (4)

    suspend fun copyToAppStorage(source: Uri): String? = withContext(Dispatchers.IO) {   // (5)
        try {
            val target = createPhotoFile()
            val input = context.contentResolver.openInputStream(source)       // (6)
                ?: return@withContext null
            input.use { inputStream ->                                        // (7)
                target.outputStream().use { outputStream ->
                    inputStream.copyTo(outputStream)                          // (8)
                }
            }
            target.absolutePath                                               // (9)
        } catch (e: IOException) {
            null
        }
    }

    fun delete(path: String) {
        File(path).delete()
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `@ApplicationContext context` | Hilt gives us the safe Application context (Chapter 23). |
| 2 | `File(context.filesDir, "note_photos").apply { mkdirs() }` | The folder `note_photos` inside our private folder. `mkdirs()` **creates** it if it doesn't exist yet (and does nothing if it does). `apply` (Chapter 4) runs that, then gives back the `File`. |
| 3 | `"photo_${System.currentTimeMillis()}.jpg"` | A **unique** file name, using the current time. |
| 4 | `FileProvider.getUriForFile(...)` | Makes a **shareable** address for our private file, so the **camera app** can write into it. More in 25.9! 📸 |
| 5 | `withContext(Dispatchers.IO)` | Copying a file is slow **waiting** work → the **IO** team (Chapter 18). Main-safe! 🛡️ |
| 6 | `contentResolver.openInputStream(source)` | **Open** the picked photo for reading — like opening a tap 🚰. It can be `null` → give up. |
| 7 | `.use { ... }` | **Automatically closes** the stream when done — even if an error happens. Always close files! (Forgetting to close = a "leak" 💧.) |
| 8 | `inputStream.copyTo(outputStream)` | Pour everything from the source into our new file. 🚰➡️🪣 |
| 9 | `target.absolutePath` | The full path as text — that's what we save in the database. |

---

## 25.8 Step 3: The Photo Picker 🖼️

Android's **Photo Picker** is a ready-made, beautiful screen for choosing photos. The best part: **no permission needed!** 🎉 The user picks **exactly** the photo they want to share — your app sees **only** that one photo, nothing else. 🛡️

```kotlin
val pickPhotoLauncher = rememberLauncherForActivityResult(
    contract = ActivityResultContracts.PickVisualMedia()                      // (1)
) { uri: Uri? ->                                                              // (2)
    if (uri != null) viewModel.onPhotoPicked(uri)
}

// later, in an onClick:
pickPhotoLauncher.launch(
    PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)  // (3)
)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `PickVisualMedia()` | The Photo Picker contract. (`PickMultipleVisualMedia(5)` lets the user choose up to 5.) |
| 2 | `uri: Uri?` | The chosen photo's address — or `null` if the user **cancelled** (pressed Back). |
| 3 | `PickVisualMedia.ImageOnly` | Show **only photos** (no videos). Other options: `VideoOnly`, `ImageAndVideo`. |

> ℹ️ On new phones, this shows Android's own picker. On older phones (back to our minimum, Android 7), it automatically uses a fallback picker. Either way — **one** line of code. 😎

---

## 25.9 Step 4: The Camera 📸

The simplest way to take a photo: ask the phone's **camera app** to do it, and save the picture **into a file we choose**.

```
Our app ──"please take a photo and save it HERE ➡️ (an address)"──▶ 📸 Camera app
Our app ◀──────────────── "done! ✅" (true) or "cancelled ❌" (false) ──── 📸
```

But there's a problem: our files are **private** 🏠🔒 — the camera app **can't** write into our folder! The solution is a **FileProvider**: a "**mail slot**" 📮 in our door. We create a special address for **one** file, and the camera app may write **only** that file.

### Step 4a: Declare the FileProvider in `AndroidManifest.xml`

Inside `<application ...>`, next to `<activity ...>`:

```xml
<provider
    android:name="androidx.core.content.FileProvider"
    android:authorities="${applicationId}.fileprovider"
    android:exported="false"
    android:grantUriPermissions="true">
    <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/file_paths" />
</provider>
```

| Line | Meaning |
|---|---|
| `android:name="androidx.core.content.FileProvider"` | Use AndroidX's ready-made FileProvider. |
| `android:authorities="${applicationId}.fileprovider"` | Its **unique name**: `com.example.notes.fileprovider`. `${applicationId}` is filled in automatically. It must **match** the text in `PhotoStorage.uriForFile` (`"${context.packageName}.fileprovider"`). |
| `android:exported="false"` | Other apps can't use it freely… |
| `android:grantUriPermissions="true"` | …only when **we** give them permission for **one** file. 🔑 |
| `<meta-data ... @xml/file_paths />` | **Which** folders the mail slot may share → the file below. |

### Step 4b: `res/xml/file_paths.xml`

Right-click **`res`** → **New → Android Resource Directory** → Resource type: **xml** → OK. Then right-click the new `xml` folder → **New → XML Resource File** → name: `file_paths`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<paths>
    <files-path name="note_photos" path="note_photos/" />
</paths>
```

| Part | Meaning |
|---|---|
| `<files-path ...>` | A folder inside `context.filesDir`. |
| `path="note_photos/"` | **Only** our photos folder can be shared — nothing else. 🔒 |
| `name="note_photos"` | A short name used inside the shareable address. |

### Step 4c: The camera launcher

```kotlin
val takePhotoLauncher = rememberLauncherForActivityResult(
    contract = ActivityResultContracts.TakePicture()                          // (1)
) { success: Boolean ->
    viewModel.onCameraResult(success)                                         // (2)
}

// later, in an onClick:
takePhotoLauncher.launch(viewModel.prepareCameraPhoto())                      // (3)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `TakePicture()` | Open the camera app. The input is a `Uri`: **where** to save. |
| 2 | `success: Boolean` | `true` = a photo was saved into our file. `false` = cancelled. |
| 3 | `viewModel.prepareCameraPhoto()` | Creates an empty file, remembers it, and returns its FileProvider address. |

> 💡 **No CAMERA permission needed!** We're not using the camera ourselves — the **camera app** is. ⚠️ But careful: if your manifest **declares** `android.permission.CAMERA` (for some other feature), Android then **requires** it to be granted even for this. So don't declare it unless you need it.

### 💀 The process-death trap with the camera

Here's a sneaky problem that happens in **real** apps:

1. Our app opens the camera app 📸. Our app goes to the **background**.
2. The camera app uses **lots** of memory → Android **kills** our app 💀 (process death, Chapter 14).
3. The user takes the photo → Android **restarts** our app and gives it the answer: "`true`, done!"
4. But… **which file** was it? Our ViewModel was destroyed. If we kept the file path in a normal variable, it's **gone**! 😱

**The fix:** remember the waiting file's path in the **`SavedStateHandle`** (Chapter 15) — it survives process death. 💾✅ You'll see it in the ViewModel below.

---

## 25.10 Step 5: The Editor ViewModel — Photo Edition 🧠📸

Here are **all** the changes to `NoteEditorViewModel.kt` (from Chapter 24):

### The state gets a photo

```kotlin
data class NoteEditorUiState(
    val title: String = "",
    val content: String = "",
    val color: NoteColor = NoteColor.DEFAULT,
    val isPinned: Boolean = false,
    val photoPath: String? = null,                                            // 👈 new
    val isLoading: Boolean = true,
    val isFinished: Boolean = false
)

private const val KEY_SAVED_NOTE_ID = "saved_note_id"
private const val KEY_PENDING_CAMERA_PATH = "pending_camera_path"            // 👈 new
```

### The constructor gets `PhotoStorage`

```kotlin
@HiltViewModel
class NoteEditorViewModel @Inject constructor(
    private val savedStateHandle: SavedStateHandle,
    private val notesRepository: NotesRepository,
    private val photoStorage: PhotoStorage                                    // 👈 new — Hilt brings it!
) : ViewModel() {
```

### Loading: keep a photo that arrived early

In `init`, when the note is loaded:

```kotlin
it.copy(
    title = note.title,
    content = note.content,
    color = note.color,
    isPinned = note.isPinned,
    photoPath = it.photoPath ?: note.photoPath,                               // 👈 new
    isLoading = false
)
```

🤔 **Why `it.photoPath ?: note.photoPath`?** After process death (25.9), the camera's answer may arrive **before** the note has finished loading from the database. If we simply wrote `note.photoPath`, we'd **overwrite** the new photo with the old one! So: if a photo is **already** in the state, keep it. 🛡️

### The new events

```kotlin
fun onPhotoPicked(uri: Uri) {                                                 // (1)
    viewModelScope.launch {
        val path = photoStorage.copyToAppStorage(uri)
        if (path != null) {
            _uiState.update { it.copy(photoPath = path) }
        }
    }
}

fun prepareCameraPhoto(): Uri {                                               // (2)
    val file = photoStorage.createPhotoFile()
    savedStateHandle[KEY_PENDING_CAMERA_PATH] = file.absolutePath             // 💾 survives process death
    return photoStorage.uriForFile(file)
}

fun onCameraResult(success: Boolean) {                                        // (3)
    val path: String = savedStateHandle[KEY_PENDING_CAMERA_PATH] ?: return
    savedStateHandle.remove<String>(KEY_PENDING_CAMERA_PATH)
    if (success) {
        _uiState.update { it.copy(photoPath = path) }
    } else {
        photoStorage.delete(path)                                             // (4)
    }
}

fun onRemovePhoto() = _uiState.update { it.copy(photoPath = null) }          // (5)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `onPhotoPicked(uri)` | Copy the picked photo into our folder (in the background), then show it. |
| 2 | `prepareCameraPhoto()` | Make an empty file, **remember** its path in `SavedStateHandle`, give the camera its address. |
| 3 | `onCameraResult(success)` | Read the remembered path — **even after process death** ✅ — and forget it (`remove`). |
| 4 | `photoStorage.delete(path)` | Cancelled? Delete the empty file — no junk left behind. 🧹 |
| 5 | `onRemovePhoto()` | ✖️ Remove the photo from the note. (The file stays for now — see Challenge 3!) |

Import: `android.net.Uri`, `com.example.notes.data.PhotoStorage`.

### Saving includes the photo

In `saveNow()`, three small changes:

```kotlin
val isEmpty = state.title.isBlank() && state.content.isBlank() && state.photoPath == null   // 👈 a photo-only note is not empty!

// "new + text" branch:
val newId = notesRepository.addNote(
    title = state.title,
    content = state.content,
    color = state.color,
    isPinned = state.isPinned,
    photoPath = state.photoPath                                              // 👈 new
)

// "existing" branch:
val edited = current.copy(
    title = state.title,
    content = state.content,
    color = state.color,
    isPinned = state.isPinned,
    photoPath = state.photoPath                                              // 👈 new
)
```

> 💡 Opening the photo picker or the camera puts our app in the **background** → `ON_STOP` → **auto-save** (Chapter 24)! Your note is safe even if Android kills the app while you're taking a picture. 💾🛡️

---

## 25.11 Step 6: The Editor Screen — Photo Edition 🎨📸

### `NoteEditorRoute` — add the two launchers

```kotlin
@Composable
fun NoteEditorRoute(
    onNavigateBack: () -> Unit,
    viewModel: NoteEditorViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val context = LocalContext.current

    val pickPhotoLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia()
    ) { uri ->
        if (uri != null) viewModel.onPhotoPicked(uri)
    }

    val takePhotoLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.TakePicture()
    ) { success ->
        viewModel.onCameraResult(success)
    }

    // ... LaunchedEffect(isFinished), LifecycleEventEffect(ON_STOP), BackHandler — unchanged ...

    NoteEditorScreen(
        uiState = uiState,
        // ... the old parameters ...
        onGalleryClick = {
            pickPhotoLauncher.launch(
                PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
            )
        },
        onCameraClick = {
            try {
                takePhotoLauncher.launch(viewModel.prepareCameraPhoto())
            } catch (e: ActivityNotFoundException) {                                    // (1)
                viewModel.onCameraResult(false)
                Toast.makeText(context, "No camera app found 📸❌", Toast.LENGTH_SHORT).show()
            }
        },
        onRemovePhoto = viewModel::onRemovePhoto
    )
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `catch (e: ActivityNotFoundException)` | A phone (or emulator) without a camera app → no crash; clean up the empty file and show a short **Toast** message. (A `Toast` is a small grey message at the bottom that disappears by itself 🍞.) |

Imports: `android.content.ActivityNotFoundException`, `android.widget.Toast`, `androidx.activity.compose.rememberLauncherForActivityResult`, `androidx.activity.result.PickVisualMediaRequest`, `androidx.activity.result.contract.ActivityResultContracts`, `androidx.compose.ui.platform.LocalContext`.

### `NoteEditorScreen` — new parameters, buttons, and the photo

Add three parameters:

```kotlin
onGalleryClick: () -> Unit,
onCameraClick: () -> Unit,
onRemovePhoto: () -> Unit,
```

In the `TopAppBar`'s `actions`, **before** the pin button:

```kotlin
IconButton(onClick = onGalleryClick) {
    Text("🖼️", modifier = Modifier.semantics { contentDescription = "Add photo from gallery" })
}
IconButton(onClick = onCameraClick) {
    Text("📸", modifier = Modifier.semantics { contentDescription = "Take a photo" })
}
```

In the `Column`, right **after** the `ColorPicker`:

```kotlin
uiState.photoPath?.let { path ->                                                        // (1)
    Box(
        modifier = Modifier
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .fillMaxWidth()
    ) {
        AsyncImage(
            model = File(path),                                                         // (2)
            contentDescription = "Note photo",
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(max = 220.dp)                                                 // (3)
                .clip(RoundedCornerShape(16.dp))
        )
        IconButton(
            onClick = onRemovePhoto,
            modifier = Modifier
                .align(Alignment.TopEnd)                                                // (4)
                .padding(8.dp)
                .background(Color.Black.copy(alpha = 0.5f), CircleShape)
        ) {
            Icon(Icons.Filled.Close, contentDescription = "Remove photo", tint = Color.White)
        }
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `uiState.photoPath?.let { path -> ... }` | Only show this part when the note **has** a photo. |
| 2 | `model = File(path)` | Coil can load a **file** too, not only URLs (Chapter 20). 📁 Shrinking, caching, crossfade — all free. |
| 3 | `.heightIn(max = 220.dp)` | At most 220 dp tall, so there's room left for writing. |
| 4 | `.align(Alignment.TopEnd)` | The ✖️ button sits in the **top-right corner**, on a half-transparent black circle so it's visible on any photo. |

Imports: `coil3.compose.AsyncImage`, `java.io.File`, `androidx.compose.foundation.layout.heightIn`, `androidx.compose.foundation.shape.RoundedCornerShape`, `androidx.compose.ui.layout.ContentScale`, `androidx.compose.ui.Alignment`, `androidx.compose.material.icons.filled.Close`.

### `NoteCard` — a small thumbnail in the list

In `NoteCard.kt`, at the **start** of the `Card`'s content (before the `Column`), wrap everything in a `Column` and add:

```kotlin
Card(/* ... unchanged ... */) {
    note.photoPath?.let { path ->
        AsyncImage(
            model = File(path),
            contentDescription = null,                                    // decorative here
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .fillMaxWidth()
                .height(120.dp)
        )
    }
    Column(/* ... the old title/text/edited Column ... */) { /* unchanged */ }
}
```

(The `Card`'s content is already a `Column`, so the photo simply appears **above** the text. The card's rounded corners clip it automatically. ✨)

> ⚠️ Don't forget `contentDescription = null` is OK **here** because the card already says the title — but in the **editor**, the photo is the main content, so we described it.

**Run it!** ▶️ Open a note → 🖼️ → pick a photo → it appears! 📸 → take a picture (the emulator shows a fake 3D room — you can "walk" with Alt + W/A/S/D) → it appears! Go back → the list shows the thumbnail. 🎉

---

## 25.12 Notifications — Messages From Your App 🔔

A **notification** is a message that appears at the **top** of the phone, even when your app is **closed**. Tapping it usually **opens** the app.

```
┌─────────────────────────────────────────┐
│ 📝 Notes · now                          │
│ Time to write! ✍️                        │
│ What happened today? Write it in a note 📝│
└─────────────────────────────────────────┘
```

Three things to know:

| Thing | What it is | Like… |
|---|---|---|
| **Channel** 📺 | A **category** of notifications. Users can turn each channel on/off in Settings. Required since Android 8. | TV channels — you can mute the news but keep cartoons |
| **Permission** 🔑 | `POST_NOTIFICATIONS` — a **runtime** permission since **Android 13**. (Older phones: allowed by default.) | Knocking before you can talk |
| **The notification** ✉️ | Built with `NotificationCompat.Builder`: icon, title, text, what happens on tap | The letter itself |

### Step 1: A small notification icon 🎨

Notification icons must be **simple**, **one color** (white shapes on transparent). Let's make one:

1. Right-click **`res/drawable`** → **New → Vector Asset**.
2. Click the **Clip art** icon → search **"notifications"** → pick the bell 🔔 → **OK**.
3. **Name:** `ic_notification` → **Next → Finish**.

> ⚠️ Don't use your colorful **app icon** as the small icon — Android paints it as a **white blob** ⬜ in the status bar.

### Step 2: The permission in `AndroidManifest.xml`

```xml
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
```

### Step 3: `notifications/NotificationHelper.kt`

Make a package **`notifications`** and create:

```kotlin
package com.example.notes.notifications

import android.Manifest
import android.annotation.SuppressLint
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.provider.Settings
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import com.example.notes.MainActivity
import com.example.notes.R

object NotificationHelper {

    private const val REMINDER_CHANNEL_ID = "reminders"
    private const val REMINDER_NOTIFICATION_ID = 1

    fun createChannels(context: Context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {                       // (1)
            val channel = NotificationChannel(
                REMINDER_CHANNEL_ID,                                                // (2)
                "Daily reminders",                                                  // (3)
                NotificationManager.IMPORTANCE_DEFAULT                              // (4)
            ).apply {
                description = "A friendly daily nudge to write a note"
            }
            val manager = context.getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)                              // (5)
        }
    }

    fun canPostNotifications(context: Context): Boolean =                           // (6)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            ContextCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS) ==
                PackageManager.PERMISSION_GRANTED
        } else {
            NotificationManagerCompat.from(context).areNotificationsEnabled()
        }

    @SuppressLint("MissingPermission")                                              // (7)
    fun showReminder(context: Context) {
        if (!canPostNotifications(context)) return

        val openApp = Intent(context, MainActivity::class.java).apply {             // (8)
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        val pendingIntent = PendingIntent.getActivity(                              // (9)
            context, 0, openApp,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )

        val notification = NotificationCompat.Builder(context, REMINDER_CHANNEL_ID)   // (10)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle("Time to write! ✍️")
            .setContentText("What happened today? Write it in a note 📝")
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)                                                    // (11)
            .build()

        NotificationManagerCompat.from(context).notify(REMINDER_NOTIFICATION_ID, notification)   // (12)
    }

    fun appNotificationSettingsIntent(context: Context): Intent =                   // (13)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS)
                .putExtra(Settings.EXTRA_APP_PACKAGE, context.packageName)
        } else {
            Intent(
                Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
                Uri.fromParts("package", context.packageName, null)
            )
        }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)` | Channels exist since Android **8** ("O" = Oreo 🍪). Our app supports Android 7 too, so we **check** the version first. `SDK_INT` = the phone's Android version number. |
| 2 | `REMINDER_CHANNEL_ID` | The channel's **id** — never change it once published. |
| 3 | `"Daily reminders"` | The **name** the user sees in Settings. |
| 4 | `IMPORTANCE_DEFAULT` | Makes a sound, shows in the status bar — but doesn't pop up over other apps. (`HIGH` = pops up; save that for **important** things like messages.) |
| 5 | `createNotificationChannel(channel)` | Create it. Safe to call many times — if it exists, nothing changes. |
| 6 | `canPostNotifications(context)` | Android **13+** ("Tiramisu" 🍰): check the runtime permission. Older: check that the user didn't **turn off** our notifications in Settings. |
| 7 | `@SuppressLint("MissingPermission")` | We check in `canPostNotifications`, but Android Studio can't see it across functions. We **did** check. ✅ |
| 8 | `Intent(context, MainActivity::class.java)` | "Open **our** app." The flags start it **fresh** on the notes list. |
| 9 | `PendingIntent.getActivity(...)` | A **"ticket for later"** 🎫: Android will use it **when the user taps** — even if our app isn't running. `FLAG_IMMUTABLE` = nobody can change the ticket (required on new Android). |
| 10 | `NotificationCompat.Builder(context, CHANNEL_ID)` | Build the notification, in **our** channel. A builder again! 🍔 |
| 11 | `.setAutoCancel(true)` | Tapping the notification also **removes** it. |
| 12 | `notify(REMINDER_NOTIFICATION_ID, notification)` | **Show** it! Using the **same** id again **replaces** the old one instead of stacking up. |
| 13 | `appNotificationSettingsIntent(context)` | Opens **our** app's notification settings page — for when the user said "no" twice. ⚙️ |

### Step 4: Create the channel when the app starts — `NotesApplication.kt`

```kotlin
@HiltAndroidApp
class NotesApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        NotificationHelper.createChannels(this)              // 👈 once, at app start
    }
}
```

---

## 25.13 WorkManager — Work That Runs Even When the App Is Closed ⏰

How do we show a notification **every day at 8 PM**, when the app is probably **closed**? 🤔

- A coroutine with `delay(24 hours)`? ❌ When the app closes, the coroutine dies.
- **WorkManager** ✅ — Android's tool for **background work that must happen**, even if the app is closed or the phone **restarts**. 🔁📴

| WorkManager is great for | Not for |
|---|---|
| Daily reminders 🔔 | Work that must happen at an **exact** second (alarm clocks ⏰ → `AlarmManager`) |
| Uploading photos when Wi-Fi is available ☁️ | Work while the user watches (→ coroutines) |
| Cleaning up old files 🧹 | |
| Syncing data every few hours 🔄 | |

> 💡 WorkManager runs work at a **good** time, not always an **exact** time. Android may wait a bit to save battery 🔋 (for example, when the phone is sleeping). "Around 8 PM" is perfect for a reminder.

### The three pieces 🧩

| Piece | What it is | Like… |
|---|---|---|
| **Worker** 👷 | A class with the **job**: `doWork()` | A worker who knows **how** to do one task |
| **WorkRequest** 📝 | **When** and **how often**: once, or every day; delays; conditions | A job ticket: "every day, starting at 8 PM" |
| **WorkManager** 🏢 | Takes the ticket and makes sure the job happens | The office that schedules all workers |

### Step 1: The Worker — `notifications/ReminderWorker.kt`

```kotlin
package com.example.notes.notifications

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters

class ReminderWorker(
    appContext: Context,
    params: WorkerParameters
) : CoroutineWorker(appContext, params) {                       // (1)

    override suspend fun doWork(): Result {                     // (2)
        NotificationHelper.showReminder(applicationContext)     // (3)
        return Result.success()                                 // (4)
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `: CoroutineWorker(appContext, params)` | A worker that can use **coroutines** — `doWork` is `suspend`. WorkManager creates it for us (so the constructor must look **exactly** like this). |
| 2 | `override suspend fun doWork(): Result` | **The job.** It already runs in the **background** — no `withContext` needed. |
| 3 | `showReminder(applicationContext)` | Our job: show the notification. 🔔 |
| 4 | `Result.success()` | "Done! ✅" Other answers: `Result.retry()` (try again later 🔁) or `Result.failure()` (give up ❌). |

### Step 2: Scheduling — `notifications/ReminderScheduler.kt`

```kotlin
package com.example.notes.notifications

import android.content.Context
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import dagger.hilt.android.qualifiers.ApplicationContext
import java.util.Calendar
import java.util.concurrent.TimeUnit
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class ReminderScheduler @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val workManager: WorkManager
        get() = WorkManager.getInstance(context)                                     // (1)

    fun scheduleDaily(hour: Int = 20) {
        val request = PeriodicWorkRequestBuilder<ReminderWorker>(1, TimeUnit.DAYS)   // (2)
            .setInitialDelay(millisUntilNext(hour), TimeUnit.MILLISECONDS)           // (3)
            .build()

        workManager.enqueueUniquePeriodicWork(                                       // (4)
            DAILY_REMINDER_WORK,
            ExistingPeriodicWorkPolicy.UPDATE,                                       // (5)
            request
        )
    }

    fun cancel() {
        workManager.cancelUniqueWork(DAILY_REMINDER_WORK)                            // (6)
    }

    fun showPreviewNow() {
        workManager.enqueue(OneTimeWorkRequestBuilder<ReminderWorker>().build())     // (7)
    }

    private fun millisUntilNext(hour: Int): Long {                                   // (8)
        val now = Calendar.getInstance()
        val next = Calendar.getInstance().apply {
            set(Calendar.HOUR_OF_DAY, hour)
            set(Calendar.MINUTE, 0)
            set(Calendar.SECOND, 0)
            set(Calendar.MILLISECOND, 0)
            if (before(now)) add(Calendar.DAY_OF_MONTH, 1)                           // (9)
        }
        return next.timeInMillis - now.timeInMillis
    }

    private companion object {
        const val DAILY_REMINDER_WORK = "daily_reminder"
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `WorkManager.getInstance(context)` | The **office** 🏢. There's one for the whole app. |
| 2 | `PeriodicWorkRequestBuilder<ReminderWorker>(1, TimeUnit.DAYS)` | A ticket: "do `ReminderWorker` **every 1 day**." (The shortest allowed period is **15 minutes**.) |
| 3 | `.setInitialDelay(...)` | "…but **start** after this long" — the time until the next 8 PM. |
| 4 | `enqueueUniquePeriodicWork(name, ...)` | Give the ticket to the office, with a **name**. "**Unique**" → there's only **one** job with this name — turning the reminder on twice doesn't create two reminders! 🛡️ |
| 5 | `ExistingPeriodicWorkPolicy.UPDATE` | If a job with this name already exists, **update** it with the new ticket. |
| 6 | `cancelUniqueWork(name)` | Stop the daily reminder. 🔕 |
| 7 | `OneTimeWorkRequestBuilder<ReminderWorker>()` | A **one-time** job, **right now** — a **preview** so the user sees what the reminder looks like (and great for testing! 🧪). |
| 8 | `millisUntilNext(hour)` | How many milliseconds until the next `hour:00`? We use **`Calendar`** (a date/time tool that works on all Android versions we support). |
| 9 | `if (before(now)) add(DAY_OF_MONTH, 1)` | It's 9 PM and we want 8 PM? Today's 8 PM is **past** → use **tomorrow's**. 📅 |

> 💡 **WorkManager remembers jobs!** They're saved in its own small database. Close the app, **restart the phone** 📴 — the daily reminder still comes. 🔁 That's why we don't need to schedule it again at every app start.

---

## 25.14 Step 7: The Reminder Switch 🔔🔕

### Save the choice — `UserPreferencesRepository`

```kotlin
interface UserPreferencesRepository {
    val sortOrder: Flow<SortOrder>
    val reminderEnabled: Flow<Boolean>                                       // 👈 new
    suspend fun setSortOrder(sortOrder: SortOrder)
    suspend fun setReminderEnabled(enabled: Boolean)                         // 👈 new
}
```

In `DataStoreUserPreferencesRepository`:

```kotlin
private val reminderKey = booleanPreferencesKey("reminder_enabled")

override val reminderEnabled: Flow<Boolean> = dataStore.data
    .catch { error -> if (error is IOException) emit(emptyPreferences()) else throw error }
    .map { preferences -> preferences[reminderKey] ?: false }

override suspend fun setReminderEnabled(enabled: Boolean) {
    dataStore.edit { it[reminderKey] = enabled }
}
```

### `NotesListViewModel` — two small changes

```kotlin
data class NotesListUiState(
    // ... the old fields ...
    val reminderEnabled: Boolean = false                                      // 👈 new
)

@OptIn(ExperimentalCoroutinesApi::class)
@HiltViewModel
class NotesListViewModel @Inject constructor(
    private val notesRepository: NotesRepository,
    private val preferencesRepository: UserPreferencesRepository,
    private val reminderScheduler: ReminderScheduler                          // 👈 new
) : ViewModel() {

    // ... _query, _recentlyDeleted, notesForQuery unchanged ...

    val uiState: StateFlow<NotesListUiState> = combine(
        notesForQuery,
        preferencesRepository.sortOrder,
        _query,
        _recentlyDeleted,
        preferencesRepository.reminderEnabled                                 // 👈 a 5th flow
    ) { notes, sortOrder, query, recentlyDeleted, reminderEnabled ->
        NotesListUiState(
            notes = notes.sortedFor(sortOrder),
            sortOrder = sortOrder,
            isSearching = query.isNotBlank(),
            isLoading = false,
            recentlyDeleted = recentlyDeleted,
            reminderEnabled = reminderEnabled
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), NotesListUiState())

    fun onReminderToggle(enabled: Boolean) {                                  // 👈 new
        viewModelScope.launch {
            preferencesRepository.setReminderEnabled(enabled)
            if (enabled) {
                reminderScheduler.scheduleDaily()
                reminderScheduler.showPreviewNow()
            } else {
                reminderScheduler.cancel()
            }
        }
    }

    // ... the other functions unchanged ...
}
```

> 💡 `combine` works with up to **5** flows like this (with named parameters). For more, you'd group some flows first.

### `NotesListRoute` — the permission dance 💃🔑

The **permission launcher** must live in the **Route** (it needs a real Activity — previews can't show it). We also move the `SnackbarHostState` up to the Route, so **both** the Route and the Screen can show messages.

```kotlin
@Composable
fun NotesListRoute(
    onNoteClick: (Long) -> Unit,
    onAddClick: () -> Unit,
    viewModel: NotesListViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val query by viewModel.query.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val snackbarHostState = remember { SnackbarHostState() }                 // (1)

    fun turnReminderOn() {
        viewModel.onReminderToggle(true)
        scope.launch { snackbarHostState.showSnackbar("Daily reminder on — every day at 8 PM 🔔") }
    }

    fun showBlockedMessage() {                                               // (2)
        scope.launch {
            val result = snackbarHostState.showSnackbar(
                message = "Notifications are blocked 🔕",
                actionLabel = "Settings",
                duration = SnackbarDuration.Long
            )
            if (result == SnackbarResult.ActionPerformed) {
                context.startActivity(NotificationHelper.appNotificationSettingsIntent(context))
            }
        }
    }

    val notificationPermissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (granted) turnReminderOn() else showBlockedMessage()
    }

    NotesListScreen(
        uiState = uiState,
        query = query,
        snackbarHostState = snackbarHostState,                                // 👈 new
        onReminderClick = {                                                   // 👈 new
            when {
                uiState.reminderEnabled -> viewModel.onReminderToggle(false)                  // (3)
                NotificationHelper.canPostNotifications(context) -> turnReminderOn()          // (4)
                Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU ->
                    notificationPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)   // (5)
                else -> showBlockedMessage()                                                  // (6)
            }
        },
        // ... all the old parameters unchanged ...
    )
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `snackbarHostState` in the Route | Created here and **passed down** to the Screen (hoisting, Chapter 8). |
| 2 | `showBlockedMessage()` | A Snackbar with a **Settings** button → opens our notification settings. ⚙️ |
| 3 | Already on → turn **off** | No permission needed to turn things off! 🔕 |
| 4 | Already allowed → turn **on** | No pop-up needed. |
| 5 | Android 13+ and not allowed yet → **ask** | Show Android's pop-up. The answer goes to the launcher's lambda. |
| 6 | Older Android, notifications switched off in Settings | We can't ask with a pop-up → explain + Settings button. |

Imports: `android.Manifest`, `android.os.Build`, `androidx.activity.compose.rememberLauncherForActivityResult`, `androidx.activity.result.contract.ActivityResultContracts`, `androidx.compose.runtime.rememberCoroutineScope`, `androidx.compose.ui.platform.LocalContext`, `kotlinx.coroutines.launch`, `com.example.notes.notifications.NotificationHelper`, plus the Snackbar ones.

### `NotesListScreen` — the 🔔 button

Add two parameters, and use the passed-in `snackbarHostState` (delete the old `val snackbarHostState = remember { ... }` line inside the Screen):

```kotlin
fun NotesListScreen(
    uiState: NotesListUiState,
    query: String,
    onReminderClick: () -> Unit,                                         // 👈 new
    // ... the other parameters ...
    modifier: Modifier = Modifier,
    snackbarHostState: SnackbarHostState = remember { SnackbarHostState() }   // 👈 new (with a default for previews)
)
```

In the `TopAppBar`'s `actions`, **before** the sort `Box`:

```kotlin
IconButton(
    onClick = onReminderClick,
    modifier = Modifier.semantics {
        contentDescription = if (uiState.reminderEnabled) "Turn off daily reminder" else "Turn on daily reminder"
    }
) {
    Text(if (uiState.reminderEnabled) "🔔" else "🔕")
}
```

**Run it!** ▶️ Tap 🔕:

- **Android 13+:** the pop-up *"Allow Notes to send you notifications?"* → **Allow** → the icon becomes 🔔, a Snackbar confirms, and a **preview** notification appears at the top! 📬
- Tap the notification → the app opens. ✅
- Tap 🔔 → 🔕 — reminder off.

---

## 25.15 Testing Background Work 🧪🔍

You don't want to wait until 8 PM to test! 😄

### The Background Task Inspector 🕵️

1. Run the app, turn the reminder **on**.
2. **View → Tool Windows → App Inspection** → **Background Task Inspector** tab.
3. You'll see `ReminderWorker` twice: the **one-time** preview (✅ *Succeeded*) and the **periodic** one (⏳ *Enqueued*), with its next run time!

### Quick trick for testing: a short delay ⏱️

While testing, change `scheduleDaily` temporarily:

```kotlin
PeriodicWorkRequestBuilder<ReminderWorker>(15, TimeUnit.MINUTES)     // the shortest period
    .setInitialDelay(10, TimeUnit.SECONDS)                           // start soon
```

Turn the reminder off and on → wait 10 seconds → 🔔! Then **change it back** to the daily version.

### Test closing and restarting 📴

| Test | Expected |
|---|---|
| Reminder on → swipe the app away → wait (with the short test delay) | Notification still comes ✅ |
| Reminder on → **restart** the emulator (⋮ → Cold boot / or power off and on) | The job is **still** in the Background Task Inspector ✅ |

---

## 25.16 Test Checklist ✅

### Where Am I? 📍

| Test | Expected | ✓ |
|---|---|---|
| First tap | Location pop-up with Precise/Approximate | ☐ |
| Allow → set a location in the emulator | Latitude/longitude shown | ☐ |
| Open in Maps | Map opens — or a friendly "No map app" message | ☐ |
| Deny | Kind message; the app keeps working | ☐ |
| Location turned off | "Couldn't find your location…" | ☐ |

### Notes: photos 🖼️📸

| Test | Expected | ✓ |
|---|---|---|
| Upgrade from Chapter 24 without uninstalling | Old notes still there (migration ✅) | ☐ |
| 🖼️ → pick a photo | It appears in the editor | ☐ |
| 🖼️ → press Back in the picker | Nothing changes | ☐ |
| 📸 → take a photo | It appears in the editor | ☐ |
| 📸 → cancel | Nothing changes (and no empty file left) | ☐ |
| ✖️ on the photo | Photo removed | ☐ |
| A note with **only** a photo (no text) → Back | Saved (not treated as empty) | ☐ |
| List | The card shows a thumbnail on top | ☐ |
| Close and reopen the app | Photos still there 💾 | ☐ |
| Delete the original photo from the gallery | Our note still shows it (we made a copy ✅) | ☐ |

### Notes: reminder 🔔

| Test | Expected | ✓ |
|---|---|---|
| 🔕 → Allow | 🔔 + Snackbar + a preview notification | ☐ |
| Tap the notification | The app opens | ☐ |
| 🔔 → 🔕 | Reminder off; Background Task Inspector shows it **cancelled** | ☐ |
| 🔕 → Don't allow | "Notifications are blocked 🔕 — Settings" | ☐ |
| Tap Settings | Our app's notification settings open | ☐ |
| Settings → Notifications → Daily reminders | Our **channel** is listed and can be switched off | ☐ |
| Close and reopen the app | 🔔 is remembered (DataStore) | ☐ |

---

## 25.17 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| Runtime permission only in the manifest | Feature never works (always "denied") | Also **ask** in code with a launcher. |
| Asking for permissions at app start | Users say "no" — they don't know why 🤨 | Ask **in context**, when the feature is used. |
| `rememberLauncherForActivityResult` inside `onClick` | Error: launchers must be registered while composing | Create it at the **top** of the Composable. |
| Launcher in a Screen with a Preview | Preview crashes (*No ActivityResultRegistryOwner*) | Keep launchers in the **Route**. |
| Only `ACCESS_FINE_LOCATION` requested | Android 12+ users can't choose approximate | Ask for **both** fine and coarse. |
| Not handling a `null` location | Crash 💥 | Location can be `null` (location off) — check it. |
| Opening another app without `try`/`catch` | 💥 *ActivityNotFoundException* | Catch it and explain. |
| Saving the picker's `Uri` instead of copying | Broken photo later 💔 | Copy the file into `filesDir`. |
| FileProvider `authorities` ≠ the text in `getUriForFile` | 💥 *Couldn't find meta-data for provider* | Same `"${applicationId}.fileprovider"` / `"${packageName}.fileprovider"`. |
| Folder missing in `file_paths.xml` | 💥 *Failed to find configured root* | Add the matching `<files-path path="note_photos/" />`. |
| Camera file path in a normal variable | Lost after process death 💀 | Keep it in `SavedStateHandle`. |
| Declaring `CAMERA` permission but using the camera **app** | 💥 SecurityException | Don't declare it — or request it first. |
| Notification without a channel (Android 8+) | Nothing appears 😶 | Create the channel at app start. |
| Colorful small icon | A white blob ⬜ in the status bar | A simple **vector asset**. |
| Missing `FLAG_IMMUTABLE` on `PendingIntent` | 💥 Crash on Android 12+ | Add `PendingIntent.FLAG_IMMUTABLE`. |
| `enqueue` instead of `enqueueUniquePeriodicWork` for daily work | Reminders **pile up** — 2, 3, 4 per day 🔔🔔🔔 | Use **unique** work with a name. |
| Periodic work shorter than 15 minutes | Silently becomes 15 minutes | That's the minimum. |
| Expecting WorkManager at an exact second | It's a bit late sometimes | That's normal (battery saving). Exact alarms → `AlarmManager`. |

---

## 25.18 Summary — What You Learned 🎓

✅ Apps live in a **sandbox** 🏠. To touch the user's things, they need **permissions**: **normal** (manifest only) or **runtime** (manifest **+** a pop-up).

✅ **Golden rules:** ask **in context**, explain **why**, ask for the **minimum**, and **accept "no"**. After two "no"s, only **Settings** can change it.

✅ The **Activity Result API**: `rememberLauncherForActivityResult(contract) { answer -> }` + `launcher.launch(input)`. Contracts: `RequestPermission`, `RequestMultiplePermissions`, `PickVisualMedia`, `TakePicture`.

✅ **Location:** coarse + fine permissions, the **Fused Location Provider**, `getCurrentLocation(...).await()` — and the result can be `null`.

✅ **Photo Picker:** no permission needed; you get a `Uri`. **Copy** it into `filesDir` with `contentResolver.openInputStream` + `copyTo` on `Dispatchers.IO`.

✅ **Camera:** `TakePicture` + a **FileProvider** address (manifest `<provider>` + `res/xml/file_paths.xml`). Keep the waiting file path in **`SavedStateHandle`** for process death. 💀🛡️

✅ **Notifications:** a **channel** (Android 8+), the **`POST_NOTIFICATIONS`** permission (Android 13+), `NotificationCompat.Builder`, a `PendingIntent` for taps, a simple **vector** small icon.

✅ **WorkManager:** a `CoroutineWorker` (the job), a `PeriodicWorkRequest`/`OneTimeWorkRequest` (the ticket), and **unique** work names. Survives app closing **and** phone restarts. 🔁

✅ The **Notes app** now has **photos** 🖼️📸 and a **daily reminder** 🔔 — with a database **migration**, Hilt-injected helpers, and careful permission handling!

---

## 25.19 Practice Time 🏋️

**Task 1 — Which permission? 🔑**
For each feature, answer: no permission / normal (manifest only) / runtime (manifest + ask)?
a) Loading jokes from the internet 😂
b) Choosing a profile photo with the Photo Picker 🖼️
c) Showing a weather notification on Android 14 🔔
d) Showing the user's city 📍
e) Taking a photo with the camera **app** (`TakePicture`) 📸
f) Reading the user's contacts 👥

**Task 2 — Three photos 🖼️🖼️🖼️:**
In MyFirstApp, let the user pick **up to 3** photos at once and show them in a row.
*Hint:* `ActivityResultContracts.PickMultipleVisualMedia(3)` → the answer is a `List<Uri>`. Coil can show a `Uri` directly with `AsyncImage(model = uri)` (for showing right now — no copying needed).

**Task 3 — A longer notification 📜:**
Make the reminder show a **longer** text that expands when the user pulls it down.
*Hint:* `.setStyle(NotificationCompat.BigTextStyle().bigText("..."))`.

**Task 4 — Only while charging 🔌:**
Make the daily reminder job run only when the phone is **not low on battery**.
*Hint:* `Constraints.Builder().setRequiresBatteryNotLow(true).build()` and `.setConstraints(...)` on the request builder.

**Task 5 — Find the 3 bugs 🐛🐛🐛:**

```kotlin
@Composable
fun CameraButton(viewModel: MyViewModel) {
    Button(onClick = {
        val launcher = rememberLauncherForActivityResult(ActivityResultContracts.TakePicture()) { }
        val file = File(LocalContext.current.filesDir, "pic.jpg")
        launcher.launch(Uri.fromFile(file))
    }) {
        Text("Take photo 📸")
    }
}
```

**Task 6 — Reminder time ⏰:**
Let the user choose the reminder **hour** (for example with a row of chips: 8 AM, 12 PM, 6 PM, 8 PM). Save it in DataStore and pass it to `scheduleDaily(hour)`.

---

### Answers

**Task 1:**

| | Answer | Why |
|---|---|---|
| a) | **Normal** (`INTERNET` in the manifest) | No pop-up for internet. |
| b) | **No permission** | The Photo Picker shares only what the user picks. 🛡️ |
| c) | **Runtime** (`POST_NOTIFICATIONS`) | Required on Android 13+. |
| d) | **Runtime** (`ACCESS_COARSE_LOCATION` is enough for a city!) | Ask for the **minimum**. |
| e) | **No permission** (as long as you don't declare `CAMERA`) | The camera **app** takes the photo. |
| f) | **Runtime** (`READ_CONTACTS`) | Contacts are private. |

**Task 2:**

```kotlin
@Composable
fun ThreePhotos() {
    var photos by remember { mutableStateOf<List<Uri>>(emptyList()) }

    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickMultipleVisualMedia(3)
    ) { uris: List<Uri> ->
        photos = uris
    }

    Column(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Button(onClick = {
            launcher.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
        }) {
            Text("Pick up to 3 photos 🖼️")
        }
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            photos.forEach { uri ->
                AsyncImage(
                    model = uri,
                    contentDescription = "Picked photo",
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .size(100.dp)
                        .clip(RoundedCornerShape(12.dp))
                )
            }
        }
    }
}
```

💡 Cancelled → an **empty** list (not `null`). Add **Coil** (`coil-compose`) to MyFirstApp first.

**Task 3:**

```kotlin
.setContentText("What happened today? Write it in a note 📝")
.setStyle(
    NotificationCompat.BigTextStyle().bigText(
        "What happened today? 🌞 Something funny, something new, or something you learned? " +
        "Write it down in a note before you forget! 📝✨"
    )
)
```

Collapsed → the short text. Expanded → the long one. 📜

**Task 4:**

```kotlin
val constraints = Constraints.Builder()
    .setRequiresBatteryNotLow(true)
    .build()

val request = PeriodicWorkRequestBuilder<ReminderWorker>(1, TimeUnit.DAYS)
    .setInitialDelay(millisUntilNext(hour), TimeUnit.MILLISECONDS)
    .setConstraints(constraints)
    .build()
```

(Import `androidx.work.Constraints`.) Other useful constraints: `setRequiredNetworkType(NetworkType.UNMETERED)` (Wi-Fi only 📶), `setRequiresCharging(true)` (🔌).

**Task 5:**

| # | Bug | Fix |
|---|---|---|
| 1 | **`rememberLauncherForActivityResult` inside `onClick`** — it's a Composable function; it must be called while **composing**, at the top. | Move it out, above the `Button`. |
| 2 | **`LocalContext.current` inside `onClick`** — also a Composable thing, not allowed in a click lambda. | `val context = LocalContext.current` at the top. |
| 3 | **`Uri.fromFile(file)`** — a plain `file://` address → the camera app can't write into our private folder (💥 *FileUriExposedException*). | Use a **FileProvider** address: `FileProvider.getUriForFile(context, "${context.packageName}.fileprovider", file)`. |

Bonus 🌟: the file path should be kept in `SavedStateHandle` (process death 💀), and the result lambda `{ }` ignores whether the photo was taken!

**Task 6:**

1. Preferences: `val reminderHour: Flow<Int>` (default `20`) + `suspend fun setReminderHour(hour: Int)` with an `intPreferencesKey("reminder_hour")`.
2. ViewModel: add `reminderHour` to the state; `onReminderHourChange(hour)` saves it **and**, if the reminder is on, calls `reminderScheduler.scheduleDaily(hour)` again (`UPDATE` replaces the old job ✅).
3. When turning the reminder on: `scheduleDaily(uiState.value.reminderHour)`.
4. UI: chips (Chapter 9):

```kotlin
listOf(8 to "8 AM", 12 to "12 PM", 18 to "6 PM", 20 to "8 PM").forEach { (hour, label) ->
    FilterChip(
        selected = uiState.reminderHour == hour,
        onClick = { onReminderHourChange(hour) },
        label = { Text(label) }
    )
}
```

💡 `(hour, label)` — **destructuring** a `Pair` (Chapter 17). 😎

---

## 25.20 Challenges 🚀

### Challenge 1: "Written in Paris 📍" ⭐⭐⭐
Save the **place** where each note was created. Ask for **coarse** location when creating a note (only if the user turns on a setting!), and turn the coordinates into a city name with Android's `Geocoder`. Another database **migration**! 🚚

### Challenge 2: Several photos per note 🖼️🖼️ ⭐⭐⭐
Let a note have **many** photos. You'll need a **second table** (`note_photos` with `noteId` and `path`) — a real "one-to-many" database design.

### Challenge 3: Clean up old photo files 🧹 ⭐⭐⭐
When a photo is removed or a note is deleted, the **file** stays in `note_photos/`. Write a **`CleanupWorker`** that runs once a week: list all files in the folder, ask the database which paths are still used, and delete the others.
*Hint:* the worker needs the database → look up **`@HiltWorker`** and the `hilt-work` library (it lets Hilt inject into workers).

### Challenge 4: Share the note with its photo 📤 ⭐⭐
Share the note's text **and** its photo with other apps: `Intent.ACTION_SEND`, `type = "image/*"`, `putExtra(Intent.EXTRA_STREAM, fileProviderUri)`, and `addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)`. The FileProvider from this chapter makes it possible! 📮

### Challenge 5: Smart reminder 🧠🔔 ⭐⭐⭐
Only send the daily reminder if the user **hasn't** written a note today. (The worker needs to check the database → `@HiltWorker` again.)

---

## 25.21 What Is Next?

Our apps can now do **everything**: show screens, save data, talk to the internet, and use the phone's camera, location, and notifications. 🎉 But some parts still feel a bit **stiff** — things just **appear** and **disappear** instantly.

In **Chapter 26: Animations**, you will learn to make your apps feel **alive** ✨:

- **`AnimatedVisibility`** — things that slide and fade in and out 👻
- **`animate*AsState`** — smoothly changing colors, sizes, and positions 🎨
- **`Crossfade`** and **`AnimatedContent`** — smooth changes between screens and states 🔀
- **`updateTransition`** — animating several things together 🎭
- **Infinite** animations — pulsing, spinning, breathing 💓
- **Gestures** — dragging and flinging things around 👆
- Polishing the **Notes app** and the **Quiz app** with delightful animations 💫

**Amazing work finishing Chapter 25! 🎉 Your apps can now see 📸, find 📍, and remind 🔔 — like real phone apps! 📱✨**
