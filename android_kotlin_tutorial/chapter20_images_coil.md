# Chapter 20: Showing Pictures From the Internet 🖼️🐶

> **What you will learn in this chapter**
>
> 1. Why pictures are **different** from text (big, slow, memory-hungry 🐘)
> 2. What an **image library** does for you — and meet **Coil** 🖼️
> 3. **`AsyncImage`** — a picture from a URL in **one** call
> 4. Making pictures look good: **`contentScale`**, size, **round** corners, **circles** ⭕
> 5. **Placeholders** ⏳, **error** pictures ❌, and **fallbacks**
> 6. **Crossfade** ✨ and setting up Coil **once** for the whole app
> 7. **`SubcomposeAsyncImage`** — a spinner while loading
> 8. **Caching** — why the second time is instant ⚡ (memory 🧠 and disk 💾)
> 9. 🛠️ Building the **Dog Gallery** app 🐶📸 — a grid of photos, breed filters, and a detail screen
>
> **Time needed:** about 4 hours.
>
> **What you need to know:** Chapters 1–19, especially 5 (`Image`), 10 (grids), 13 (Navigation), and 19 (Retrofit).

---

## 20.1 Why Are Pictures Different? 🤔

In Chapter 19, a joke was about **100 bytes** of text. Tiny! 🐜

A photo is **much** bigger:

| Thing | Size to download | Like… |
|---|---|---|
| A joke (text) | ~100 bytes | a grain of rice 🍚 |
| A small photo (thumbnail) | ~20,000 bytes (20 KB) | a spoon of rice 🥄 |
| A phone camera photo | ~4,000,000 bytes (4 MB) | a **bag** of rice 🛍️ |

But the download is only **half** the problem. To **show** a picture, the phone must **unpack** it (**decode** it) into **pixels** — every tiny dot of color. Each pixel needs **4 bytes** of memory.

Let's do the math for a normal 12-megapixel camera photo 🧮:

```
4000 pixels wide × 3000 pixels high = 12,000,000 pixels
12,000,000 pixels × 4 bytes        = 48,000,000 bytes  ≈ 48 MB of memory! 😱
```

A grid of 20 photos like that = **almost 1 GB**. The app would **crash** with an *OutOfMemoryError*. 💥

But wait — on the screen, a grid cell is only about **120 × 120 dp** (around 400 × 400 pixels). We don't need 4000 × 3000! A **smaller** copy uses:

```
400 × 400 × 4 bytes = 640,000 bytes ≈ 0.6 MB   ✅ (75 times less!)
```

So showing pictures well means a lot of work:

1. **Download** the file — in the background (Chapter 18!) 📡
2. **Shrink** it to the size it will really be shown 📏
3. **Decode** it into pixels — also in the background 🧮
4. **Remember** it, so we don't download it again 🧠
5. **Cancel** the work if the user scrolls away before it's finished 🛑
6. Show something **nice** while waiting, and if it fails ⏳❌

Writing all that yourself would take **weeks**. 😵 Luckily…

---

## 20.2 Meet Coil 🖼️

**Coil** (**Co**routine **I**mage **L**oader) is an **image library** that does **all six jobs** for you. It's built with **Kotlin coroutines** and made for **Compose**. It's the most popular choice for new Android apps. ⭐

With Coil, showing a picture from the internet is this simple:

```kotlin
AsyncImage(
    model = "https://images.dog.ceo/breeds/shiba/shiba-2.jpg",
    contentDescription = "A Shiba dog"
)
```

That's it! 🤯 "**Async**" means "**not right now — when it's ready**". The picture appears as soon as it has been downloaded and decoded, and the app stays **smooth** the whole time.

> ℹ️ You might also hear about **Glide** and **Picasso** — older image libraries from before Compose. They do the same job. In this book we use **Coil**.

---

## 20.3 Step 1: Create the Project 🆕

1. **File → New → New Project… → Empty Activity** → **Next**.
2. **Name:** `Dog Gallery`
3. **Package name:** `com.example.doggallery`
4. **Finish**.

Your theme is **`DogGalleryTheme`**.

Here's what we'll build:

```
┌──────────────────────────────────┐          ┌──────────────────────────────────┐
│ Dog Gallery 🐶                🔄  │          │ ⬅️  Golden Retriever               │
├──────────────────────────────────┤          ├──────────────────────────────────┤
│ [✓ All 🐾] [Shiba] [Husky] [Pug]→ │          │                                  │
│ ┌────────┐┌────────┐┌────────┐   │   tap    │   ┌──────────────────────────┐   │
│ │  🐕     ││  🐩     ││  🐕‍🦺    │   │  ─────▶  │   │                          │   │
│ │        ││        ││        │   │          │   │        🐕 (big)          │   │
│ └────────┘└────────┘└────────┘   │          │   │                          │   │
│ ┌────────┐┌────────┐┌────────┐   │          │   └──────────────────────────┘   │
│ │  🐶     ││ ⏳grey  ││  🐕     │   │          │                                  │
│ │        ││        ││        │   │          │   Photo from dog.ceo 📸           │
│ └────────┘└────────┘└────────┘   │          │                                  │
└──────────────────────────────────┘          └──────────────────────────────────┘
          Gallery screen                                  Detail screen
```

### Requirements 📋

1. The **Gallery** loads **20** random dog photos in a **grid**.
2. **Chips** filter by breed: All, Shiba, Husky, Pug, Beagle, Samoyed, Corgi, Golden Retriever.
3. While a photo downloads, its cell shows a **grey box**; if it fails, a **reddish box**.
4. Photos **fade in** smoothly ✨.
5. **Tap** a photo → the **Detail** screen shows it **big**, with the breed name.
6. **Refresh** 🔄 loads new photos. No internet → friendly error + **Try again** (Chapter 19 again!).

---

## 20.4 Step 2: Add the Libraries 📦

This project uses **everything** from Part 4 and Chapter 19, **plus** Coil.

### `gradle/libs.versions.toml`

Add to the matching sections (keep what's already there):

```toml
[versions]
coil = "3.1.0"
retrofit = "2.11.0"
navigationCompose = "2.8.9"
kotlinxSerializationJson = "1.7.3"

[libraries]
coil-compose = { group = "io.coil-kt.coil3", name = "coil-compose", version.ref = "coil" }
coil-network-okhttp = { group = "io.coil-kt.coil3", name = "coil-network-okhttp", version.ref = "coil" }
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
retrofit-kotlinx-serialization = { group = "com.squareup.retrofit2", name = "converter-kotlinx-serialization", version.ref = "retrofit" }
kotlinx-serialization-json = { group = "org.jetbrains.kotlinx", name = "kotlinx-serialization-json", version.ref = "kotlinxSerializationJson" }
androidx-navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigationCompose" }
androidx-lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycleRuntimeKtx" }
androidx-lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycleRuntimeKtx" }

[plugins]
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
```

### `build.gradle.kts (Module :app)`

```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.serialization)
}

// ... android { } unchanged ...

dependencies {
    // ... existing lines ...
    implementation(libs.coil.compose)
    implementation(libs.coil.network.okhttp)
    implementation(libs.retrofit)
    implementation(libs.retrofit.kotlinx.serialization)
    implementation(libs.kotlinx.serialization.json)
    implementation(libs.androidx.navigation.compose)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)
}
```

**Sync Now** 🔄 ✅

| Library | Why |
|---|---|
| **`coil-compose`** | Coil itself + `AsyncImage` for Compose. 🖼️ |
| **`coil-network-okhttp`** | Lets Coil **download** from the internet (using OkHttp, the same engine Retrofit uses). |

> ⚠️ **Very important:** Coil 3 does **not** download from the internet **unless** you add **`coil-network-okhttp`**! Without it, there's **no** crash and **no** clear message — your pictures just **never appear**. 😶 This trips up many developers. Now you know!

> ℹ️ Notice the group name: **`io.coil-kt.coil3`** — with a **3**. Old tutorials use `io.coil-kt` (Coil **2**), whose imports start with `coil.` instead of `coil3.`. Don't mix them!

### `AndroidManifest.xml` — the Internet permission 🔑

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

(Above `<application`, exactly like Chapter 19.)

---

## 20.5 Your First `AsyncImage` 🐕

Let's try Coil **before** building the whole app. Replace the `setContent { ... }` content in `MainActivity.kt` for a moment:

```kotlin
setContent {
    DogGalleryTheme {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            AsyncImage(                                                          // (1)
                model = "https://images.dog.ceo/breeds/shiba/shiba-2.jpg",       // (2)
                contentDescription = "A Shiba dog",                              // (3)
                modifier = Modifier.size(300.dp)                                 // (4)
            )
        }
    }
}
```

Imports:

```kotlin
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.size
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import coil3.compose.AsyncImage
```

| # | Code | Meaning |
|---|---|---|
| 1 | `AsyncImage(...)` | Coil's Composable: "Load this picture **in the background**, and show it when it's ready." |
| 2 | `model = "https://..."` | **What** to load. Usually a URL `String`. (It's called `model` because it can also be other things — a file, a resource…) |
| 3 | `contentDescription = "A Shiba dog"` | For **screen readers** ♿ — exactly like `Image` in Chapter 5. Use `null` only for decoration pictures. |
| 4 | `Modifier.size(300.dp)` | How big to show it. Coil **reads** this size and **shrinks** the photo to it (20.1!). 📏 |

**Run it.** ▶️ For a split second the screen is empty… then a **Shiba** appears! 🐕🎉

> 💡 **`Image` vs `AsyncImage`:**
> - **`Image`** (Chapter 5) shows a picture that's **inside** the app (`R.drawable.…`). Instant.
> - **`AsyncImage`** shows a picture from **somewhere else** (internet, files). Takes time ⏳.

---

## 20.6 Making Pictures Look Good 💅

### `contentScale` — how to fit the picture in its box 📐

You know these from Chapter 5. They work the same way with `AsyncImage`:

| `contentScale` | Result | Use it for |
|---|---|---|
| `ContentScale.Fit` (default) | Whole picture visible, maybe empty space at the sides | Detail screens, where you want to see **everything** |
| `ContentScale.Crop` ⭐ | Fills the box, edges **cut off** | **Grids**, profile photos, cards |
| `ContentScale.FillBounds` | Stretched to fill — may look **squished** 😬 | Almost never |

```kotlin
AsyncImage(
    model = "https://images.dog.ceo/breeds/shiba/shiba-2.jpg",
    contentDescription = "A Shiba dog",
    contentScale = ContentScale.Crop,                   // fill the square, cut the edges
    modifier = Modifier.size(200.dp)
)
```

### Round corners and circles ⭕

Use **`Modifier.clip(shape)`** — it cuts the picture into a shape:

```kotlin
// Rounded corners — great for cards and grids
AsyncImage(
    model = url,
    contentDescription = "A dog",
    contentScale = ContentScale.Crop,
    modifier = Modifier
        .size(160.dp)
        .clip(RoundedCornerShape(16.dp))                // (1)
)

// A circle — perfect for profile pictures 👤
AsyncImage(
    model = url,
    contentDescription = "Profile photo",
    contentScale = ContentScale.Crop,                   // (2)
    modifier = Modifier
        .size(96.dp)
        .clip(CircleShape)                              // (3)
        .border(3.dp, MaterialTheme.colorScheme.primary, CircleShape)   // (4)
)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `.clip(RoundedCornerShape(16.dp))` | Cut the corners round. ✂️ |
| 2 | `ContentScale.Crop` | **Needed** for a nice circle: the photo must **fill** the square first. With `Fit`, you'd get an oval photo inside a circle. 🥚 |
| 3 | `.clip(CircleShape)` | Cut into a circle. A square box + `CircleShape` = a perfect circle. ⭕ |
| 4 | `.border(3.dp, color, CircleShape)` | A colored ring around it. Use the **same** shape as the clip. |

Imports: `androidx.compose.ui.draw.clip`, `androidx.compose.foundation.border`, `androidx.compose.foundation.shape.CircleShape`, `androidx.compose.foundation.shape.RoundedCornerShape`, `androidx.compose.ui.layout.ContentScale`.

> ⚠️ **Modifier order matters** (Chapter 5)! `size` → `clip` → `border`. If you put `clip` **after** `border`, the border's outside part gets cut off.

### Square cells in a grid ⬛

In a grid we don't know the exact width (it depends on the phone), but we want **squares**:

```kotlin
modifier = Modifier
    .fillMaxWidth()          // as wide as the cell
    .aspectRatio(1f)         // height = width → square (Chapter 6)
```

---

## 20.7 Placeholders, Errors, and Fallbacks ⏳❌🤷

While the picture downloads, `AsyncImage` shows **nothing**. On a slow connection, that's a blank hole for seconds. 🕳️ Let's show something **while waiting** and **if it fails**:

```kotlin
AsyncImage(
    model = url,
    contentDescription = "A dog",
    contentScale = ContentScale.Crop,
    placeholder = ColorPainter(MaterialTheme.colorScheme.surfaceVariant),   // (1)
    error = ColorPainter(MaterialTheme.colorScheme.errorContainer),         // (2)
    fallback = ColorPainter(MaterialTheme.colorScheme.outlineVariant),      // (3)
    modifier = Modifier.size(160.dp)
)
```

| # | Parameter | Shown when… | Like… |
|---|---|---|---|
| 1 | `placeholder` | the picture is still **loading** ⏳ | an empty frame on the wall 🖼️ |
| 2 | `error` | loading **failed** ❌ (no internet, wrong URL, 404…) | a "broken" sign 🚧 |
| 3 | `fallback` | the `model` is **`null`** 🤷 (for example, a user without a profile photo) | a default avatar 👤 |

**`ColorPainter(color)`** = a **painter** (something that can draw) that just fills the space with **one color**. Simple and fast — no picture file needed! (Import: `androidx.compose.ui.graphics.painter.ColorPainter`.)

> 💡 If `error` is not set, Coil uses the `placeholder` for errors too. If `fallback` is not set, it uses `error`.

### Using your own drawing as a placeholder 🎨

You can also use a picture from your project, with `painterResource` (Chapter 5):

```kotlin
placeholder = painterResource(R.drawable.dog_placeholder),
error = painterResource(R.drawable.broken_image),
```

To make simple icon pictures, right-click **`res/drawable` → New → Vector Asset**, pick a **Clip art** icon, give it a name, and click **Finish**. 🎨

> ⚠️ The placeholder and error pictures are drawn with the **same** `contentScale` as the photo. With `ContentScale.Crop`, a small icon would be **blown up** huge. That's why plain colors (`ColorPainter`) are a great choice for grids.

### Doing something on success or error 📣

`AsyncImage` can also **tell you** what happened:

```kotlin
AsyncImage(
    model = url,
    contentDescription = "A dog",
    onSuccess = { Log.d("Images", "Loaded! ✅") },
    onError = { state -> Log.e("Images", "Failed ❌", state.result.throwable) }
)
```

Very useful for **finding problems**: if a picture doesn't appear, look in **Logcat** for the reason. 🔍

---

## 20.8 Crossfade ✨ — and Setting Up Coil Once

By default, the picture just **pops** in. 💥 A **crossfade** makes it fade in smoothly over a short moment. Much nicer! ✨

### For one picture: `ImageRequest`

Instead of just a URL, give `model` an **`ImageRequest`** — a URL **plus options**:

```kotlin
AsyncImage(
    model = ImageRequest.Builder(LocalContext.current)    // (1)
        .data(url)                                         // (2)
        .crossfade(true)                                   // (3)
        .build(),                                          // (4)
    contentDescription = "A dog"
)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `ImageRequest.Builder(LocalContext.current)` | Start building a request (a builder again, like Retrofit's 🍔). Coil needs the **Context** — `LocalContext.current` gives it inside a Composable. |
| 2 | `.data(url)` | **What** to load. |
| 3 | `.crossfade(true)` | Fade in when ready ✨. You can give a time instead: `.crossfade(500)` = half a second. |
| 4 | `.build()` | Done. |

Imports: `coil3.request.ImageRequest`, `coil3.request.crossfade`, `androidx.compose.ui.platform.LocalContext`.

### For the whole app: a custom `ImageLoader` 🏭

Writing a builder for **every** picture is boring. 😴 Better: tell Coil **once**, for the **whole app**, "always crossfade".

Coil has one shared **`ImageLoader`** (the "picture factory" 🏭 that does all the work). We can **create it ourselves** in our `Application` class (Chapter 16):

```kotlin
class DogGalleryApplication : Application(), SingletonImageLoader.Factory {    // (1)

    override fun newImageLoader(context: PlatformContext): ImageLoader {     // (2)
        return ImageLoader.Builder(context)
            .crossfade(true)                                                 // (3)
            .build()
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `: Application(), SingletonImageLoader.Factory` | Our Application **is** an Application **and** promises "I know how to build Coil's image loader" (implementing an interface, Chapter 4). |
| 2 | `override fun newImageLoader(...)` | Coil calls this **once**, the first time it needs to load a picture. |
| 3 | `.crossfade(true)` | Now **every** `AsyncImage` in the app fades in. ✨ No `ImageRequest` needed! |

We'll add this to the real app in section 20.13. 📌

---

## 20.9 `SubcomposeAsyncImage` — A Spinner While Loading ⏳

A grey box is fine for small grid cells. But for **one big picture** (like our Detail screen), a **spinner** looks better. `ColorPainter` can't spin… so Coil has another Composable where the loading and error parts are **Composables** — anything you want!

```kotlin
SubcomposeAsyncImage(
    model = url,
    contentDescription = "A dog",
    loading = {                                          // (1)
        Box(contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
    },
    error = {                                            // (2)
        Text("😢 This picture couldn't load")
    },
    modifier = Modifier.fillMaxWidth()
)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `loading = { ... }` | **Any Composable** to show while loading — here a spinner. ⏳ |
| 2 | `error = { ... }` | **Any Composable** if it fails — here a sad message. |

Import: `coil3.compose.SubcomposeAsyncImage`.

> ⚠️ **Don't use `SubcomposeAsyncImage` in big lists or grids.** It's **slower** than `AsyncImage` (it has to build extra Composables for every picture), and scrolling can stutter. 🐌
> 🎯 **Rule:** grids and lists → **`AsyncImage`** + `placeholder`. One big picture → `SubcomposeAsyncImage` is fine.

---

## 20.10 Caching — Why the Second Time Is Instant ⚡

Open a photo, go back, open it again — the second time it appears **immediately**. Why? Because Coil **remembers** pictures. This is called a **cache** (say: "**cash**").

Think about getting **milk** 🥛:

| Where Coil looks | Kitchen version | Speed | Survives closing the app? |
|---|---|---|---|
| 1. **Memory cache** 🧠 | The **fridge** — already open, right in front of you | ⚡ Instant | ❌ No |
| 2. **Disk cache** 💾 | The **cupboard** — a few steps away | 🏃 Very fast | ✅ Yes |
| 3. **Network** 🌐 | The **shop** — you have to go out | 🐢 Slow | — |

Every time a picture is needed:

```
Is it in the fridge (memory)? ──yes──▶ show it ⚡
      │ no
      ▼
Is it in the cupboard (disk)? ──yes──▶ decode, put in fridge, show it 🏃
      │ no
      ▼
Go to the shop (download) 🐢 ──▶ put in cupboard + fridge, show it
```

Both caches are **turned on by default**. You don't have to do anything! 🎉

- The **memory** cache is a part of the app's memory (about 20% by default). Old pictures are **thrown out** when it's full.
- The **disk** cache is a folder in the app's storage (up to about 2% of the free space, but at most a few hundred MB).

> 🧪 **See it yourself (in the finished app):**
> 1. Scroll through the gallery and open one photo. Go back.
> 2. Turn on **Airplane mode** ✈️.
> 3. Tap the **same** photo again → it still appears! 💾 (From the cache — no internet needed.)
> 4. Now tap **Refresh** 🔄 → error 📶. A **new** list of photos needs the internet.

> ℹ️ Caches belong to the app. **Settings → Apps → Dog Gallery → Storage → Clear cache** empties the disk cache.

---

## 20.11 Our API: Dog CEO 🐶

We'll use the free **Dog CEO API** (dog.ceo) — thousands of dog photos, no key needed.

| What you want | Path (add to `https://dog.ceo/api/`) |
|---|---|
| 20 random dog photos | `breeds/image/random/20` |
| 20 photos of **one** breed | `breed/{breed}/images/random/20` |
| …of a **sub-breed** (like *golden* retriever) | `breed/retriever/golden/images/random/20` |

### 🔍 Look at the JSON first!

Open **https://dog.ceo/api/breed/shiba/images/random/3** in your browser:

```json
{
  "message": [
    "https://images.dog.ceo/breeds/shiba/shiba-2.jpg",
    "https://images.dog.ceo/breeds/shiba/shiba-3i.jpg",
    "https://images.dog.ceo/breeds/shiba/shiba-11.jpg"
  ],
  "status": "success"
}
```

Interesting! 🤓

- The answer is an **object** `{ }` with two keys.
- The photo **URLs** are in a **list** called `"message"` (a strange name, but that's what this API uses — we'll handle it).
- There is **no breed name** in the JSON… but look closely at the URLs: **`/breeds/shiba/`**. The breed is **hidden inside the URL**! 🕵️

Try a few more:

| URL | What you notice |
|---|---|
| `.../breed/retriever/golden/images/random/2` | Folder name **`retriever-golden`** → we want to show "**Golden Retriever**". |
| `.../breeds/image/random/20` (try it several times!) | Sometimes the **same** photo appears **twice** in one list! 😮 |
| `.../breed/pirate/images/random/2` | Status **404**, `"Breed not found"`. |

Those two discoveries are **important** — we'll fix both in the **repository** (20.12). This is why we **always** look at real data first. 🔍

---

## 20.12 Step 3: The Data Layer 🏪

The files (make the packages first: `data.model`, `data.network`, `di`, `ui.navigation`, `ui.gallery`, `ui.detail`):

```
com.example.doggallery
 ├── DogGalleryApplication.kt
 ├── MainActivity.kt
 ├── data/
 │    ├── model/
 │    │    ├── DogPhoto.kt
 │    │    └── DogBreed.kt
 │    ├── network/
 │    │    ├── DogImagesResponse.kt
 │    │    └── DogApiService.kt
 │    ├── DogPhotosRepository.kt
 │    └── NetworkDogPhotosRepository.kt
 ├── di/
 │    └── AppContainer.kt
 └── ui/
      ├── theme/                    (already there)
      ├── navigation/
      │    ├── Routes.kt
      │    └── DogGalleryNavHost.kt
      ├── gallery/
      │    ├── GalleryUiState.kt
      │    ├── GalleryViewModel.kt
      │    └── GalleryScreen.kt
      └── detail/
           └── PhotoDetailScreen.kt
```

### Two kinds of models 📦📦

In Chapter 19, the `Joke` class matched the JSON **and** was used by the screen. Here, the JSON (`{"message": [...], "status": "..."}`) is **ugly** for our app. So we'll have **two** classes:

| Class | Matches… | Used by |
|---|---|---|
| `DogImagesResponse` | the **JSON** exactly (network model 📡) | Retrofit only |
| `DogPhoto` | what the **app** needs (app model 📱) | ViewModel and screens |

The **repository** turns one into the other. 🔄 This is very common in real apps: the server's format can change, but the rest of your app doesn't care.

### `data/network/DogImagesResponse.kt`

```kotlin
package com.example.doggallery.data.network

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class DogImagesResponse(
    @SerialName("message") val imageUrls: List<String>,      // (1)
    val status: String
)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `@SerialName("message") val imageUrls` | In the JSON it's called `"message"`, but in Kotlin we use a **clear** name: `imageUrls`. (Chapter 19 🏷️) |

### `data/model/DogPhoto.kt`

```kotlin
package com.example.doggallery.data.model

data class DogPhoto(
    val url: String,
    val breedName: String
)
```

Just what the app needs. No `@Serializable` — it never touches JSON. ✅

### `data/model/DogBreed.kt`

```kotlin
package com.example.doggallery.data.model

enum class DogBreed(val apiPath: String?, val label: String) {    // (1)
    ALL(null, "All 🐾"),                                           // (2)
    SHIBA("shiba", "Shiba"),
    HUSKY("husky", "Husky"),
    PUG("pug", "Pug"),
    BEAGLE("beagle", "Beagle"),
    SAMOYED("samoyed", "Samoyed"),
    CORGI("corgi", "Corgi"),
    GOLDEN("retriever/golden", "Golden Retriever")                 // (3)
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `apiPath: String?` | The breed's part of the URL. **Nullable**… |
| 2 | `ALL(null, ...)` | …because "All" has **no** breed path — it uses a different URL. |
| 3 | `"retriever/golden"` | A **sub-breed**: breed + `/` + sub-breed. (This `/` will need special care — see below! 👀) |

### `data/network/DogApiService.kt`

```kotlin
package com.example.doggallery.data.network

import retrofit2.http.GET
import retrofit2.http.Path

interface DogApiService {

    @GET("breeds/image/random/{count}")
    suspend fun getRandomImages(@Path("count") count: Int): DogImagesResponse

    @GET("breed/{breed}/images/random/{count}")
    suspend fun getBreedImages(
        @Path("breed", encoded = true) breed: String,                 // (1)
        @Path("count") count: Int                                     // (2)
    ): DogImagesResponse
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `@Path("breed", encoded = true)` | ⚠️ **The tricky part!** Normally Retrofit makes path values **safe** by changing special characters: `/` becomes **`%2F`**. Then `"retriever/golden"` would become `breed/retriever%2Fgolden/...` → **404**! `encoded = true` means "**I promise this value is already safe — put it in as it is.**" Then the `/` stays a `/`. ✅ |
| 2 | `@Path("count") count: Int` | Numbers work too — `20` becomes `"20"` in the URL. |

### `data/DogPhotosRepository.kt`

```kotlin
package com.example.doggallery.data

import com.example.doggallery.data.model.DogBreed
import com.example.doggallery.data.model.DogPhoto

interface DogPhotosRepository {
    suspend fun getPhotos(breed: DogBreed): List<DogPhoto>
}
```

### `data/NetworkDogPhotosRepository.kt`

```kotlin
package com.example.doggallery.data

import com.example.doggallery.data.model.DogBreed
import com.example.doggallery.data.model.DogPhoto
import com.example.doggallery.data.network.DogApiService

private const val PHOTO_COUNT = 20                                         // (1)

class NetworkDogPhotosRepository(
    private val apiService: DogApiService
) : DogPhotosRepository {

    override suspend fun getPhotos(breed: DogBreed): List<DogPhoto> {
        val response = if (breed.apiPath == null) {                         // (2)
            apiService.getRandomImages(PHOTO_COUNT)
        } else {
            apiService.getBreedImages(breed.apiPath, PHOTO_COUNT)
        }

        return response.imageUrls
            .distinct()                                                     // (3)
            .map { url -> DogPhoto(url = url, breedName = breedNameFromUrl(url)) }   // (4)
    }
}

fun breedNameFromUrl(url: String): String {                                 // (5)
    val folder = url.substringAfter("/breeds/").substringBefore("/")        // (6)
    return folder
        .split("-")                                                         // (7)
        .reversed()                                                         // (8)
        .joinToString(" ") { word -> word.replaceFirstChar { it.uppercase() } }   // (9)
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `private const val PHOTO_COUNT = 20` | A **constant**: a value fixed **forever**, known when the app is built. `const` only works for simple types (numbers, Strings). Written in `UPPER_CASE` by tradition. Outside the class, `private` = only this file can see it. |
| 2 | `if (breed.apiPath == null)` | "All" → the random-images URL. Otherwise → the breed URL. After the check, Kotlin **knows** `apiPath` isn't null in the `else` (smart cast). |
| 3 | `.distinct()` | **Remove duplicates!** Remember: the API sometimes sends the **same** URL twice. We use the URL as the grid **key** — and two items with the **same key** **crash** a lazy grid 💥 (*"Key … was already used"*). `distinct()` keeps only the **first** of each. (Chapter 3) |
| 4 | `.map { url -> DogPhoto(...) }` | Turn each **network** URL into an **app** model with a nice breed name. 📡➡️📱 |
| 5 | `fun breedNameFromUrl(url)` | A normal, **public** function (outside the class), so we can test it easily later (Chapter 27). |
| 6 | `substringAfter("/breeds/").substringBefore("/")` | Cut the folder name out of the URL — see the example below. ✂️ |
| 7 | `.split("-")` | `"retriever-golden"` → `["retriever", "golden"]` |
| 8 | `.reversed()` | → `["golden", "retriever"]` (the API puts the main breed **first**; English puts it **last**) |
| 9 | `.joinToString(" ") { ... }` | Capitalize each word and join with spaces → `"Golden Retriever"`. `replaceFirstChar { it.uppercase() }` makes only the **first** letter big. |

**Let's follow one URL step by step** 🔍:

```
url  = "https://images.dog.ceo/breeds/retriever-golden/n02099601_118.jpg"

substringAfter("/breeds/")  → "retriever-golden/n02099601_118.jpg"
substringBefore("/")        → "retriever-golden"
split("-")                  → ["retriever", "golden"]
reversed()                  → ["golden", "retriever"]
capitalize + join           → "Golden Retriever"   ✅
```

And a simple one: `".../breeds/shiba/shiba-2.jpg"` → `"shiba"` → `["shiba"]` → `"Shiba"`. ✅

> 💡 Again, this cleaning is the **repository's** job 🧼. The screens get **ready-to-use** `DogPhoto`s and never see the messy server format.

---

## 20.13 Step 4: AppContainer and Application 🧰

### `di/AppContainer.kt`

```kotlin
package com.example.doggallery.di

import com.example.doggallery.data.DogPhotosRepository
import com.example.doggallery.data.NetworkDogPhotosRepository
import com.example.doggallery.data.network.DogApiService
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory

interface AppContainer {
    val dogPhotosRepository: DogPhotosRepository
}

class DefaultAppContainer : AppContainer {

    private val baseUrl = "https://dog.ceo/api/"

    private val json = Json { ignoreUnknownKeys = true }

    private val retrofit: Retrofit = Retrofit.Builder()
        .baseUrl(baseUrl)
        .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
        .build()

    private val dogApiService: DogApiService by lazy {
        retrofit.create(DogApiService::class.java)
    }

    override val dogPhotosRepository: DogPhotosRepository by lazy {
        NetworkDogPhotosRepository(dogApiService)
    }
}
```

The **same** shape as Chapter 19 — only the names and the base URL changed. You're getting good at this! 💪

> 🤔 Notice the base URL `https://dog.ceo/api/` has a **path** (`api/`) in it. That's another reason the paths in `@GET` must **not** start with `/` — `@GET("/breeds/...")` would **skip** the `api/` part and break everything. (Chapter 19, Task 5 bonus 🌟)

### `DogGalleryApplication.kt` (in the main package)

```kotlin
package com.example.doggallery

import android.app.Application
import coil3.ImageLoader
import coil3.PlatformContext
import coil3.SingletonImageLoader
import coil3.request.crossfade
import com.example.doggallery.di.AppContainer
import com.example.doggallery.di.DefaultAppContainer

class DogGalleryApplication : Application(), SingletonImageLoader.Factory {

    lateinit var container: AppContainer

    override fun onCreate() {
        super.onCreate()
        container = DefaultAppContainer()                           // (1)
    }

    override fun newImageLoader(context: PlatformContext): ImageLoader {   // (2)
        return ImageLoader.Builder(context)
            .crossfade(true)
            .build()
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `container = DefaultAppContainer()` | Our toolbox 🧰, like always. |
| 2 | `newImageLoader(...)` | Coil's picture factory 🏭 for the whole app — with **crossfade** everywhere ✨ (20.8). `PlatformContext` is just Coil's name for Android's `Context`. |

### `AndroidManifest.xml`

```xml
<uses-permission android:name="android.permission.INTERNET" />

<application
    android:name=".DogGalleryApplication"
    ... the rest stays the same ... >
```

---

## 20.14 Step 5: The Gallery ViewModel 🧠

This is **almost the same** as the Joke Machine's ViewModel (Chapter 19). Compare them side by side — that's how you learn patterns! 🔁

### `ui/gallery/GalleryUiState.kt`

```kotlin
package com.example.doggallery.ui.gallery

import com.example.doggallery.data.model.DogBreed
import com.example.doggallery.data.model.DogPhoto

sealed interface GalleryLoadState {
    data object Loading : GalleryLoadState
    data class Success(val photos: List<DogPhoto>) : GalleryLoadState
    data class Error(val message: String) : GalleryLoadState
}

data class GalleryUiState(
    val breed: DogBreed = DogBreed.ALL,
    val loadState: GalleryLoadState = GalleryLoadState.Loading
)
```

### `ui/gallery/GalleryViewModel.kt`

```kotlin
package com.example.doggallery.ui.gallery

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.ViewModelProvider.AndroidViewModelFactory.Companion.APPLICATION_KEY
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.example.doggallery.DogGalleryApplication
import com.example.doggallery.data.DogPhotosRepository
import com.example.doggallery.data.model.DogBreed
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.serialization.SerializationException
import retrofit2.HttpException
import java.io.IOException

class GalleryViewModel(
    private val repository: DogPhotosRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(GalleryUiState())
    val uiState: StateFlow<GalleryUiState> = _uiState.asStateFlow()

    private var loadJob: Job? = null

    init {
        loadPhotos()
    }

    fun onBreedSelected(breed: DogBreed) {
        if (breed == _uiState.value.breed) return
        _uiState.update { it.copy(breed = breed) }
        loadPhotos()
    }

    fun onRefreshClick() = loadPhotos()

    fun onRetryClick() = loadPhotos()

    private fun loadPhotos() {
        loadJob?.cancel()
        val breed = _uiState.value.breed

        loadJob = viewModelScope.launch {
            _uiState.update { it.copy(loadState = GalleryLoadState.Loading) }

            val newLoadState = try {
                GalleryLoadState.Success(repository.getPhotos(breed))
            } catch (e: IOException) {
                GalleryLoadState.Error("No internet connection 📶\nCheck your Wi-Fi or mobile data.")
            } catch (e: HttpException) {
                GalleryLoadState.Error("The dog server has a problem (error ${e.code()}) 🛠️\nPlease try again later.")
            } catch (e: SerializationException) {
                GalleryLoadState.Error("The server sent something we don't understand 🤔")
            }

            _uiState.update { it.copy(loadState = newLoadState) }
        }
    }

    companion object {
        val Factory: ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val app = this[APPLICATION_KEY] as DogGalleryApplication
                GalleryViewModel(repository = app.container.dogPhotosRepository)
            }
        }
    }
}
```

Every line here was explained in Chapter 19 (19.16). 😎 Quick reminders:

| Code | Why |
|---|---|
| `init { loadPhotos() }` | Load once when the ViewModel is born — not again after rotation. |
| `loadJob?.cancel()` | No **races** when chips are tapped quickly. 🏃 |
| `val newLoadState = try { ... } catch ...` | `try` gives back a value. |
| Three `catch` blocks | Friendly messages; cancellation still works. |

> 🤔 **Where do the pictures get loaded?** Not here! The ViewModel only loads the **list of URLs** (text). Each picture is loaded by **Coil**, inside `AsyncImage`, when its cell appears on the screen. Cells you never scroll to are **never** downloaded. 🔋 Smart!

---

## 20.15 Step 6: The Gallery Screen 📱

### `ui/gallery/GalleryScreen.kt`

```kotlin
package com.example.doggallery.ui.gallery

import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.painter.ColorPainter
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import coil3.compose.AsyncImage
import com.example.doggallery.data.model.DogBreed
import com.example.doggallery.data.model.DogPhoto
import com.example.doggallery.ui.theme.DogGalleryTheme

@Composable
fun GalleryRoute(
    onPhotoClick: (DogPhoto) -> Unit,                                         // (1)
    viewModel: GalleryViewModel = viewModel(factory = GalleryViewModel.Factory)
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    GalleryScreen(
        uiState = uiState,
        onBreedSelected = viewModel::onBreedSelected,
        onRefreshClick = viewModel::onRefreshClick,
        onRetryClick = viewModel::onRetryClick,
        onPhotoClick = onPhotoClick
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GalleryScreen(
    uiState: GalleryUiState,
    onBreedSelected: (DogBreed) -> Unit,
    onRefreshClick: () -> Unit,
    onRetryClick: () -> Unit,
    onPhotoClick: (DogPhoto) -> Unit,
    modifier: Modifier = Modifier
) {
    Scaffold(
        modifier = modifier,
        topBar = {
            TopAppBar(
                title = { Text("Dog Gallery 🐶") },
                actions = {
                    IconButton(
                        onClick = onRefreshClick,
                        enabled = uiState.loadState !is GalleryLoadState.Loading
                    ) {
                        Icon(Icons.Filled.Refresh, contentDescription = "Load new photos")
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(modifier = Modifier.padding(innerPadding)) {
            BreedChips(selected = uiState.breed, onBreedSelected = onBreedSelected)

            when (val loadState = uiState.loadState) {
                GalleryLoadState.Loading -> {
                    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator()
                    }
                }
                is GalleryLoadState.Error -> ErrorContent(
                    message = loadState.message,
                    onRetryClick = onRetryClick
                )
                is GalleryLoadState.Success -> PhotoGrid(
                    photos = loadState.photos,
                    onPhotoClick = onPhotoClick
                )
            }
        }
    }
}

@Composable
fun BreedChips(
    selected: DogBreed,
    onBreedSelected: (DogBreed) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState())
            .padding(horizontal = 12.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        DogBreed.entries.forEach { breed ->
            FilterChip(
                selected = breed == selected,
                onClick = { onBreedSelected(breed) },
                label = { Text(breed.label) }
            )
        }
    }
}

@Composable
fun PhotoGrid(
    photos: List<DogPhoto>,
    onPhotoClick: (DogPhoto) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyVerticalGrid(
        columns = GridCells.Adaptive(minSize = 120.dp),                       // (2)
        contentPadding = PaddingValues(12.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
        modifier = modifier.fillMaxSize()
    ) {
        items(photos, key = { photo -> photo.url }) { photo ->                 // (3)
            DogPhotoCell(photo = photo, onClick = { onPhotoClick(photo) })
        }
    }
}

@Composable
fun DogPhotoCell(
    photo: DogPhoto,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    AsyncImage(
        model = photo.url,                                                    // (4)
        contentDescription = photo.breedName,                                 // (5)
        contentScale = ContentScale.Crop,                                     // (6)
        placeholder = ColorPainter(MaterialTheme.colorScheme.surfaceVariant), // (7)
        error = ColorPainter(MaterialTheme.colorScheme.errorContainer),
        modifier = modifier
            .fillMaxWidth()
            .aspectRatio(1f)                                                  // (8)
            .clip(RoundedCornerShape(12.dp))
            .clickable(onClick = onClick)                                     // (9)
    )
}

@Composable
fun ErrorContent(
    message: String,
    onRetryClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(32.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("🐕‍🦺😵", style = MaterialTheme.typography.displayMedium)
        Text(message, textAlign = TextAlign.Center)
        Button(onClick = onRetryClick) { Text("Try again 🔁") }
    }
}

@Preview(showBackground = true)
@Composable
fun GalleryScreenPreview() {
    DogGalleryTheme {
        GalleryScreen(
            uiState = GalleryUiState(
                breed = DogBreed.SHIBA,
                loadState = GalleryLoadState.Success(
                    List(6) { i -> DogPhoto(url = "https://example.com/$i.jpg", breedName = "Shiba") }   // (10)
                )
            ),
            onBreedSelected = {}, onRefreshClick = {}, onRetryClick = {}, onPhotoClick = {}
        )
    }
}
```

**The important parts:**

| # | Code | Meaning |
|---|---|---|
| 1 | `onPhotoClick: (DogPhoto) -> Unit` | The Route doesn't navigate itself — it **tells** the NavHost "this photo was tapped" (event up ⬆️, Chapter 13). |
| 2 | `GridCells.Adaptive(minSize = 120.dp)` | "As many columns as fit, each **at least** 120 dp wide." Small phone → 3 columns, tablet or landscape → 6 or more. 📱↔️💻 (Chapter 10) |
| 3 | `key = { photo -> photo.url }` | Each URL is **unique** — because the repository used `distinct()`! 🛡️ |
| 4 | `model = photo.url` | Coil downloads this URL — only when the cell is **visible**. |
| 5 | `contentDescription = photo.breedName` | Screen readers ♿ say "Golden Retriever". |
| 6 | `ContentScale.Crop` | Fill the square; cut the edges. Dog photos come in all shapes — Crop makes the grid **neat**. |
| 7 | `placeholder` / `error` | Grey while loading, reddish if it fails (20.7). |
| 8 | `.fillMaxWidth().aspectRatio(1f)` | A **square** as wide as its column. ⬛ |
| 9 | `.clickable(onClick = onClick)` **after** `.clip(...)` | The tap **ripple** is also clipped to the rounded shape. (Modifier order, again! 🔁) |
| 10 | `List(6) { i -> DogPhoto(...) }` | Makes a list of 6 items; `i` is 0 to 5 (Chapter 3). |

> 🖼️ **In the Preview, you'll see 6 grey squares** — previews **can't** go on the internet, so Coil shows the **placeholder**. That's normal and actually useful: you can check the **layout** without any photos. Run the app to see real dogs. 🐶

> ℹ️ If `Icons.Filled.Refresh` is red, add `material-icons-core` (Chapter 5, section 5.8).

---

## 20.16 Step 7: The Detail Screen 🔍

### `ui/detail/PhotoDetailScreen.kt`

```kotlin
package com.example.doggallery.ui.detail

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.CircularProgressIndicator
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
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import coil3.compose.SubcomposeAsyncImage

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PhotoDetailScreen(
    imageUrl: String,
    breedName: String,
    onBackClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Scaffold(
        modifier = modifier,
        topBar = {
            TopAppBar(
                title = { Text(breedName) },
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
            verticalArrangement = Arrangement.spacedBy(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            SubcomposeAsyncImage(                                            // (1)
                model = imageUrl,
                contentDescription = breedName,
                contentScale = ContentScale.Fit,                             // (2)
                loading = {
                    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator()
                    }
                },
                error = {
                    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        Text("😢 This picture couldn't load")
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)                                              // (3)
            )
            Text("Photo from dog.ceo 📸", style = MaterialTheme.typography.labelLarge)
        }
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `SubcomposeAsyncImage` | **One** big picture → a spinner is OK here (20.9). |
| 2 | `ContentScale.Fit` | Show the **whole** dog, nothing cut off. 🐕 |
| 3 | `.weight(1f)` | Take all the height that's left after the text (Chapter 6). |

> 🤔 **Do you even see the spinner?** Usually **not** — because the photo is already in the **cache** from the grid! ⚡ (Coil may load a bigger version from the **disk** cache, which is very fast.) You'll see the spinner when the photo was **never** loaded before — for example, tap a **red** (failed) cell: the Detail screen tries again, with a spinner ⏳, and shows the sad message if it fails again. 😢

---

## 20.17 Step 8: Navigation and MainActivity 🧭

### `ui/navigation/Routes.kt`

```kotlin
package com.example.doggallery.ui.navigation

import kotlinx.serialization.Serializable

@Serializable
object Gallery

@Serializable
data class PhotoDetail(
    val imageUrl: String,
    val breedName: String
)
```

We pass the **URL** and the **breed name** as route arguments (Chapter 13). They're small Strings — perfect for routes. ✅

### `ui/navigation/DogGalleryNavHost.kt`

```kotlin
package com.example.doggallery.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.toRoute
import com.example.doggallery.ui.detail.PhotoDetailScreen
import com.example.doggallery.ui.gallery.GalleryRoute

@Composable
fun DogGalleryNavHost(
    navController: NavHostController = rememberNavController()
) {
    NavHost(navController = navController, startDestination = Gallery) {

        composable<Gallery> {
            GalleryRoute(
                onPhotoClick = { photo ->
                    navController.navigate(
                        PhotoDetail(imageUrl = photo.url, breedName = photo.breedName)
                    )
                }
            )
        }

        composable<PhotoDetail> { backStackEntry ->
            val route: PhotoDetail = backStackEntry.toRoute()
            PhotoDetailScreen(
                imageUrl = route.imageUrl,
                breedName = route.breedName,
                onBackClick = { navController.popBackStack() }
            )
        }
    }
}
```

All from Chapter 13. 🧭 The **Gallery's ViewModel** stays alive while the Detail screen is open (its screen is still on the back stack 🥞), so going **back** shows the **same** photos — no reload. ✅

### `MainActivity.kt`

```kotlin
package com.example.doggallery

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.doggallery.ui.navigation.DogGalleryNavHost
import com.example.doggallery.ui.theme.DogGalleryTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            DogGalleryTheme {
                DogGalleryNavHost()
            }
        }
    }
}
```

(Remove the Shiba test from 20.5 if it's still there.)

**Run the app!** ▶️ A grid full of dogs fading in! 🐶🐕🐩✨🎉

---

## 20.18 Test Checklist ✅

| Test | Expected | ✓ |
|---|---|---|
| Open the app | Spinner, then a grid; photos **fade in** one by one ✨ | ☐ |
| Grey squares | Visible for a moment before each photo appears | ☐ |
| Scroll fast | Smooth; new photos load as they appear | ☐ |
| Tap "Golden Retriever" | Only golden retrievers 🐕 (the `/` worked — `encoded = true`!) | ☐ |
| Tap "All 🐾" many times with Refresh | Never crashes, even if the API sends a duplicate (`distinct()`) | ☐ |
| Tap a photo | Detail screen with the **big** photo and the breed name as the title | ☐ |
| Back | Same grid, same photos (no reload) | ☐ |
| Rotate on the Gallery 🔄 | More columns in landscape; same photos | ☐ |
| Airplane mode ✈️ → open a photo you already saw | Still shows (cache 💾) | ☐ |
| Airplane mode → Refresh | Friendly error + Try again | ☐ |
| Airplane mode **off** → Try again | Photos load | ☐ |
| Remove `coil-network-okhttp` (then put it back!) | Grid stays **grey/red** — no photos, no crash 😶 | ☐ |
| Dark mode 🌙 | Placeholders use dark colors | ☐ |

---

## 20.19 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| Forgot **`coil-network-okhttp`** | Pictures never appear, no crash 😶 | Add it and Sync. |
| Forgot the `INTERNET` permission | Pictures never appear (and Retrofit crashes) | Add it to the manifest. |
| Mixing Coil 2 and Coil 3 | Imports `coil.` vs `coil3.` don't work | Use `io.coil-kt.coil3` and `coil3.` imports everywhere. |
| `http://` image URLs | Blocked (cleartext) → error image | Use `https://` URLs. |
| `SubcomposeAsyncImage` in a big grid/list | Stuttering scroll 🐌 | `AsyncImage` + `placeholder`. |
| Circle photo looks like an oval | `ContentScale.Fit` | `ContentScale.Crop` for circles and grids. |
| `clip` after `border` | Border cut off | `size` → `clip` → `border`. |
| Ripple not rounded | `clickable` before `clip` | `clip` first, then `clickable`. |
| Same URL twice in a lazy grid | 💥 *Key … was already used* | `distinct()` in the repository (or a different unique key). |
| `/` in a `@Path` value | Becomes `%2F` → 404 | `@Path("name", encoded = true)` |
| `@GET("/path")` with a base URL that has a path | The base path (`api/`) is dropped → 404 | No leading `/`: `@GET("path")`. |
| `contentDescription = null` for meaningful photos | Screen readers say nothing ♿ | Describe the photo. Use `null` only for decoration. |
| Big icon as placeholder with `Crop` | The icon is blown up huge | Use `ColorPainter`, or a picture that looks fine when cropped. |
| A photo doesn't load and you don't know why | — | Add `onError = { Log.e(...) }` and read **Logcat**. 🔍 |

---

## 20.20 Summary — What You Learned 🎓

✅ Pictures are **big**: downloading, **shrinking**, decoding, and **caching** them is a lot of work. A big photo can use **48 MB** of memory! 🐘

✅ **Coil** (`io.coil-kt.coil3`) does it all. **Don't forget `coil-network-okhttp`** for internet pictures!

✅ **`AsyncImage(model = url, contentDescription = ...)`** — a picture from the internet in one call. Coil shrinks it to the Composable's **size**.

✅ **Looks:** `contentScale` (`Crop` for grids and circles, `Fit` for full views), `Modifier.clip(RoundedCornerShape/CircleShape)`, `border`, `aspectRatio(1f)`.

✅ **`placeholder`** ⏳ while loading, **`error`** ❌ when it fails, **`fallback`** 🤷 when the model is `null`. `ColorPainter` is simple and fast.

✅ **Crossfade** ✨: per picture with `ImageRequest.Builder(...).crossfade(true)`, or for the **whole app** with `SingletonImageLoader.Factory` in the Application.

✅ **`SubcomposeAsyncImage`** = Composable `loading`/`error` slots (spinners!) — only for **single** big pictures.

✅ **Caching:** memory 🧠 (fridge) → disk 💾 (cupboard) → network 🌐 (shop). On by default.

✅ **Network model vs app model:** `DogImagesResponse` matches the JSON; `DogPhoto` is what the app needs; the **repository** converts and cleans (`distinct()`, breed names from URLs). 🧼

✅ You built the **Dog Gallery** 🐶📸 — an adaptive photo grid with filters, crossfade, and a detail screen!

---

## 20.21 Practice Time 🏋️

**Task 1 — Profile avatar 👤:**
Make `@Composable fun Avatar(photoUrl: String?, name: String)`: a **96 dp circle** with a 2 dp **primary-colored border**. Grey while loading, and a **different** color if `photoUrl` is `null` (use `fallback`). Show it with a real URL **and** with `null`.

**Task 2 — Breed name on the photo 🏷️:**
Change `DogPhotoCell` so the **breed name** appears at the **bottom** of each square, in white text on a half-transparent black strip.
*Hint:* a `Box` with the `AsyncImage` and a `Text` with `Modifier.align(Alignment.BottomCenter)` and a background color like `Color.Black.copy(alpha = 0.5f)`.

**Task 3 — Memory math 🧮:**
a) How much memory does a **2000 × 1500** pixel photo need after decoding?
b) And if Coil shrinks it to **500 × 375**?
c) How many times less is that?

**Task 4 — Count in the title 🔢:**
Show the number of photos in the top bar: "**Dog Gallery 🐶 (20)**" — but only when the load state is **Success**. Otherwise just "Dog Gallery 🐶".

**Task 5 — Find the 3 problems 🐛🐛🐛:**

```kotlin
LazyVerticalGrid(columns = GridCells.Fixed(3)) {
    items(dogUrls) { url ->
        SubcomposeAsyncImage(
            model = url,
            contentDescription = null,
            loading = { CircularProgressIndicator() },
            modifier = Modifier
                .size(100.dp)
                .clip(CircleShape)
        )
    }
}
```

**Task 6 — Add a breed 🐕:**
Add the **Dalmatian** (API name `"dalmatian"`) and the **French Bulldog** (a sub-breed: `"bulldog/french"`) to the chips. What will `breedNameFromUrl` show for the French Bulldog? (Look at a real URL in your browser first!)

---

### Answers

**Task 1:**

```kotlin
@Composable
fun Avatar(photoUrl: String?, name: String, modifier: Modifier = Modifier) {
    AsyncImage(
        model = photoUrl,
        contentDescription = "Profile photo of $name",
        contentScale = ContentScale.Crop,
        placeholder = ColorPainter(MaterialTheme.colorScheme.surfaceVariant),
        error = ColorPainter(MaterialTheme.colorScheme.errorContainer),
        fallback = ColorPainter(MaterialTheme.colorScheme.primaryContainer),
        modifier = modifier
            .size(96.dp)
            .clip(CircleShape)
            .border(2.dp, MaterialTheme.colorScheme.primary, CircleShape)
    )
}

// Try both:
Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
    Avatar(photoUrl = "https://images.dog.ceo/breeds/pug/n02110958_11675.jpg", name = "Pugsley")
    Avatar(photoUrl = null, name = "Mystery dog")
}
```

💡 `model = photoUrl` is fine even when `photoUrl` is `null` — that's exactly when Coil shows the **fallback**. 🤷

**Task 2:**

```kotlin
@Composable
fun DogPhotoCell(
    photo: DogPhoto,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .aspectRatio(1f)
            .clip(RoundedCornerShape(12.dp))
            .clickable(onClick = onClick)
    ) {
        AsyncImage(
            model = photo.url,
            contentDescription = photo.breedName,
            contentScale = ContentScale.Crop,
            placeholder = ColorPainter(MaterialTheme.colorScheme.surfaceVariant),
            error = ColorPainter(MaterialTheme.colorScheme.errorContainer),
            modifier = Modifier.fillMaxSize()
        )
        Text(
            text = photo.breedName,
            color = Color.White,
            style = MaterialTheme.typography.labelMedium,
            maxLines = 1,
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .background(Color.Black.copy(alpha = 0.5f))
                .padding(horizontal = 8.dp, vertical = 4.dp)
        )
    }
}
```

💡 The **`Box`** now gets the size, clip, and click — and the picture just fills it. Things in a `Box` are stacked **on top of each other** (Chapter 6), so the text sits **over** the photo. `Color.Black.copy(alpha = 0.5f)` = black, **50% see-through**. (Imports: `androidx.compose.foundation.background`, `androidx.compose.ui.graphics.Color`.)

**Task 3:**

```
a) 2000 × 1500 × 4 bytes = 12,000,000 bytes ≈ 12 MB
b)  500 ×  375 × 4 bytes =    750,000 bytes ≈ 0.75 MB
c) 12,000,000 / 750,000  = 16 times less! 🎉
```

Making it 4 times **narrower** and 4 times **shorter** = 4 × 4 = **16** times less memory.

**Task 4:**

In `GalleryScreen`, change the title:

```kotlin
title = {
    val loadState = uiState.loadState
    val text = if (loadState is GalleryLoadState.Success) {
        "Dog Gallery 🐶 (${loadState.photos.size})"
    } else {
        "Dog Gallery 🐶"
    }
    Text(text)
}
```

💡 We copy `uiState.loadState` into a local `val` first, so the smart cast works and we can use `loadState.photos`.

**Task 5:**

| # | Problem | Fix |
|---|---|---|
| 1 | **`SubcomposeAsyncImage` in a grid** → slow, stuttering scroll. | `AsyncImage` with a `placeholder`. |
| 2 | **No `contentScale = ContentScale.Crop`** → with the default `Fit`, the photo doesn't fill the circle; you get an oval or a small picture inside the circle. | Add `contentScale = ContentScale.Crop`. |
| 3 | **`contentDescription = null`** for real photos → screen readers ♿ say nothing. | A real description, like `"A dog"` or the breed name. |

Bonus 🌟: `items(dogUrls)` has **no key** — fine here, but if the list changes, a key (`key = { it }`) helps Compose. And with the dog.ceo API, remember `distinct()` first!

**Task 6:**

```kotlin
DALMATIAN("dalmatian", "Dalmatian"),
FRENCH_BULLDOG("bulldog/french", "French Bulldog"),
```

The URLs look like `https://images.dog.ceo/breeds/bulldog-french/n02108915_1234.jpg`. So:

```
"bulldog-french" → ["bulldog", "french"] → reversed → ["french", "bulldog"] → "French Bulldog" ✅
```

Our function works for **all** sub-breeds automatically. 😎 And the new chips appear by themselves, because `BreedChips` loops over `DogBreed.entries`.

---

## 20.22 Challenges 🚀

### Challenge 1: Favorites ❤️ ⭐⭐
Add a heart button on the Detail screen. Show favorite photos in a new **"Favorites ❤️"** chip.
*Hint:* keep the favorites in a `FavoritesRepository` with a `MutableStateFlow<List<DogPhoto>>` in the AppContainer. (They'll be lost when the app closes — **Chapter 22** (Room) fixes that! 💾)

### Challenge 2: Load more when you reach the end ♾️ ⭐⭐⭐
When the user scrolls to the **last** row, load 20 **more** photos and **add** them to the list ("infinite scroll").
*Hint:* `rememberLazyGridState()` + `derivedStateOf { lastVisibleItemIndex >= photos.size - 3 }` (Chapter 10) + a `LaunchedEffect` that calls `viewModel.onLoadMore()`. Don't forget `distinct()` across **both** lists!

### Challenge 3: Pinch to zoom 🔍 ⭐⭐⭐
On the Detail screen, let the user zoom with two fingers.
*Hint:* look up `Modifier.transformable` and `rememberTransformableState`, and use `graphicsLayer(scaleX = scale, scaleY = scale)`.

### Challenge 4: Share the photo 📤 ⭐⭐
Add a **Share** button on the Detail screen that shares the **URL** with other apps.
*Hint:* an `Intent(Intent.ACTION_SEND)` with `type = "text/plain"` and `putExtra(Intent.EXTRA_TEXT, url)`, then `context.startActivity(Intent.createChooser(intent, null))`. Get `context` with `LocalContext.current`.

### Challenge 5: The breed list from the API 📋 ⭐⭐⭐
Instead of a fixed enum, load **all** breeds from `https://dog.ceo/api/breeds/list/all`. Look at its JSON first — it's a **map** (`{ "hound": ["afghan", "basset", ...], ... }`). In Kotlin: `Map<String, List<String>>`. 🗺️

---

## 20.23 What Is Next?

Our apps can now get **text** and **pictures** from the internet. 🌐🖼️ But they **forget everything** when they're closed! 😢 The Quiz app forgets your best score. The Recipe Book shows the Welcome screen **every** time.

In **Chapter 21: Saving Small Settings — DataStore**, you will learn:

- **Where** an app can keep data on the phone 💾
- **Preferences DataStore** — saving small things like settings ⚙️
- Saving and reading **dark mode**, the **user's name**, and **"already seen the Welcome screen"** ✅
- Why DataStore uses **`Flow`** — your Chapter 18 skills pay off again! 🌊
- Putting DataStore behind a **repository** (the MVVM way) 🏪
- Finally saving the **best scores** for the **Quiz app** 🏅 (Chapter 17's Challenge 5!)

**Wonderful work finishing Chapter 20! 🎉 Your apps can now show the world in pictures! 🌍📸**
