# Chapter 19: Getting Data From the Internet 🌐📡

> **What you will learn in this chapter**
>
> 1. How apps talk to **servers** — requests and responses 💬
> 2. **URLs** — the addresses of the internet 🏠
> 3. **HTTP** — methods (`GET`, `POST`, …) and **status codes** (200, 404, 500…)
> 4. **JSON** — the language of data on the internet 📄
> 5. **APIs** — and trying one in your web browser 🔍
> 6. The **Internet permission** 🔑
> 7. **kotlinx.serialization** — turning JSON into Kotlin objects (and back) 🔄
> 8. **Retrofit** — calling the internet with a simple `suspend` function 🚀
> 9. What can **go wrong** — no internet, server errors, strange data ⚠️
> 10. **Loading**, **Success**, and **Error** states ⏳✅❌
> 11. 🛠️ Building the **Joke Machine** app 😂 — with categories, refresh, retry, and an MVVM structure
>
> **Time needed:** about 5 hours.
>
> **What you need to know:** Chapters 1–18, especially 15 (ViewModel), 16 (MVVM, AppContainer), and 18 (coroutines).

---

## 19.1 How Do Apps Get Data From the Internet? 🤔

Open a weather app. 🌦️ Where does "**21°C, sunny**" come from? It's not inside the app — the weather changes every hour! The app **asks** a computer far away, and that computer **answers**.

That faraway computer is called a **server**. 🖥️ Your app is the **client**. 📱

### The restaurant again 🍽️

| Restaurant | Internet |
|---|---|
| **You** (the customer) | The **app** (the client) 📱 |
| The **kitchen** | The **server** 🖥️ |
| Your **order**: "One pizza, please" 🍕 | A **request** 📤 |
| The **food** that comes back | A **response** 📥 |
| The **menu** — what you're allowed to order | The **API** 📜 |

```
   📱 App                                         🖥️ Server
     │                                               │
     │ ── Request: "Give me 10 jokes, please" ──▶    │
     │                                               │  (looks in its database...)
     │ ◀── Response: "OK! Here they are: [...]" ──   │
     │                                               │
```

Every time an app shows something **new** from the internet — posts, photos, prices, messages — it sends a **request** and gets a **response**. Usually in **less than a second**. ⚡

> 💡 **Remember Chapter 18?** "Less than a second" is **way too long** for the main thread (16 ms per frame!). That's why internet calls are always done in a **coroutine**. Now you know why we learned coroutines first! 😎

---

## 19.2 URLs — The Addresses of the Internet 🏠

Every request goes to an **address**, called a **URL**. You've seen thousands of them in your web browser.

Let's take apart the one we'll use in this chapter:

```
https://official-joke-api.appspot.com/jokes/programming/ten
└─┬─┘   └────────────┬──────────────┘└──────────┬─────────┘
scheme            domain                      path
```

| Part | Example | Meaning | Like a real address… |
|---|---|---|---|
| **Scheme** | `https://` | **How** to talk. `https` = **secure** (encrypted 🔒). | "By car" 🚗 |
| **Domain** | `official-joke-api.appspot.com` | **Which** server. | "123 Main Street" 🏠 |
| **Path** | `/jokes/programming/ten` | **What** you want from that server. | "Apartment 4, the red box on the table" 📦 |

Some URLs also have a **query** at the end, starting with `?`:

```
https://example.com/search?q=cats&page=2
                          └──────┬─────┘
                               query
```

| Part | Meaning |
|---|---|
| `?` | "Here come some **extra options**." |
| `q=cats` | An option named `q` (query) with the value `cats`. |
| `&` | "And another option…" |
| `page=2` | Option `page` = `2`. |

> 🔒 **Always `https`!** Android **blocks** plain `http://` by default (since Android 9), because anyone on the same Wi-Fi could read it. You'd get an error like *"CLEARTEXT communication … not permitted"*.

---

## 19.3 HTTP — The Rules for Talking 🗣️

**HTTP** is the "language" apps and servers use. Each request has a **method** — **what kind** of thing you want to do:

| Method | Meaning | Real-life example |
|---|---|---|
| **`GET`** ⭐ | "**Give** me something." (read) | Show me the weather 🌦️ |
| `POST` | "**Create** something new." | Post a new photo 📸 |
| `PUT` / `PATCH` | "**Change** something." | Edit my profile name ✏️ |
| `DELETE` | "**Remove** something." | Delete my comment 🗑️ |

In this chapter we only need **`GET`** — we just **read** jokes. 😄

### Status codes — how did it go? 🚦

Every response starts with a **number** that says how things went:

| Code | Name | Meaning | Feeling |
|---|---|---|---|
| **200** | OK | "Here you go!" Everything worked. | ✅😊 |
| 201 | Created | "I made the new thing you asked for." | ✅🎉 |
| 400 | Bad Request | "I don't understand your request." | ❌🤨 |
| 401 | Unauthorized | "Who are you? Log in first." | ❌🔑 |
| 403 | Forbidden | "I know who you are, but you're not allowed." | ❌🚫 |
| **404** | Not Found | "That doesn't exist here." | ❌🤷 |
| 429 | Too Many Requests | "Slow down! You ask too often." | ❌🐢 |
| **500** | Internal Server Error | "Oops, **I** (the server) broke." | ❌💥 |
| 503 | Service Unavailable | "I'm too busy or resting. Try later." | ❌😴 |

**Easy way to remember:**

- **2xx** (200–299) = ✅ **success**
- **4xx** (400–499) = ❌ **your** mistake (the app asked wrongly)
- **5xx** (500–599) = ❌ **the server's** mistake

> 💡 You have probably seen "**404 Not Found**" on a website. Now you know what it means! 🤓

---

## 19.4 JSON — The Language of Data 📄

When the server answers, the data is usually written in **JSON** (say: "**JAY-son**"). JSON is just **text**, written in a special, simple format that **both** humans and computers can read.

Here is a joke in JSON:

```json
{
  "id": 23,
  "type": "programming",
  "setup": "A SQL query walks into a bar, walks up to two tables and asks...",
  "punchline": "'Can I join you?'"
}
```

### The JSON building blocks 🧱

| JSON | Name | Example | Kotlin friend |
|---|---|---|---|
| `{ ... }` | **Object** — a group of named values | `{ "id": 23, "type": "general" }` | a **data class** 📦 |
| `"name": value` | A **key** (name) and its **value** | `"id": 23` | a **property** |
| `"text"` | **String** (always **double** quotes `"`) | `"programming"` | `String` |
| `23`, `3.14` | **Number** | `23` | `Int`, `Long`, `Double` |
| `true` / `false` | **Boolean** | `true` | `Boolean` |
| `null` | **Nothing** | `null` | a **nullable** type (`String?`) |
| `[ ... ]` | **Array** — a list | `[1, 2, 3]` | `List<...>` |

### A list of objects

When we ask for 10 jokes, the server answers with an **array** `[ ]` of **objects** `{ }`:

```json
[
  { "id": 371, "type": "programming", "setup": "What's the object-oriented way to become wealthy?", "punchline": "Inheritance." },
  { "id": 71, "type": "programming", "setup": "I was gonna tell you a joke about UDP...", "punchline": "...but you might not get it." }
]
```

In Kotlin, that's a **`List<Joke>`**. 🎯

### Objects inside objects 🪆

JSON objects can contain **other** objects and lists:

```json
{
  "name": "Mimi",
  "age": 3,
  "toys": ["ball", "mouse"],
  "owner": { "name": "Sam", "city": "Paris" }
}
```

```kotlin
data class Cat(
    val name: String,
    val age: Int,
    val toys: List<String>,     // [ ... ] of strings
    val owner: Owner            // { ... } inside → another data class
)

data class Owner(
    val name: String,
    val city: String
)
```

> 🎯 **The rule:** every `{ }` becomes a **data class**, every `[ ]` becomes a **`List`**, and every `"key"` becomes a **property** with the **same name**.

---

## 19.5 APIs — The Server's Menu 📜

An **API** (**A**pplication **P**rogramming **I**nterface) is the list of things a server lets apps ask for. Like a **menu**: you can only order what's on it.

We'll use a free, fun API: the **Official Joke API** 😂. It needs **no account** and **no key**.

| What you want | Path (add to `https://official-joke-api.appspot.com`) | Answer |
|---|---|---|
| One random joke | `/random_joke` | one joke `{ }` |
| Ten random jokes | `/jokes/ten` | a list `[ ]` |
| Up to ten jokes of one **type** | `/jokes/{type}/ten` | a list `[ ]` |
| All the types | `/types` | `["general", "knock-knock", "programming", "dad"]` |

`{type}` means "**put a type here**", for example `/jokes/programming/ten`.

### 🔍 Try it in your web browser!

Before writing **any** code, always **look** at the real data first. Open your browser (Chrome, Edge, …) and visit:

**https://official-joke-api.appspot.com/jokes/programming/ten**

You'll see a lot of JSON text. 🎉 That's **exactly** what your app will receive.

> 💡 **Tip:** In Chrome or Edge, tick the **"Pretty-print"** box at the top (if you see one) to make the JSON easier to read. Firefox shows it nicely by itself.

Now try these, and **notice** what happens:

| URL | What you see | Lesson |
|---|---|---|
| `.../jokes/knock-knock/ten` | Only **5** jokes | "ten" means "**up to** ten". Never assume the number! |
| `.../jokes/pirate/ten` | `[]` | An **empty list** — no pirate jokes. 🏴‍☠️ Your app must handle "nothing found" too. |
| `.../jokes/oops` | An error page (status **404**) | A path that's not on the menu. |

> ⚠️ This is a **free community** API. Sometimes it may be **slow** or **down** for a while. That's actually great practice — your app must handle it nicely! (And if it's down when you read this, the code works the same way with any other JSON API.)

---

## 19.6 Step 1: Create the Project 🆕

1. **File → New → New Project… → Empty Activity** → **Next**.
2. **Name:** `Joke Machine`
3. **Package name:** `com.example.jokemachine`
4. **Finish**.

Your theme is called **`JokeMachineTheme`**. (Different project name → different theme name.)

Here's what we'll build:

```
┌─────────────────────────────────┐
│ Joke Machine 😂              🔄  │
├─────────────────────────────────┤
│ [✓ General 😄] [Programming 💻]  │
│ [Knock-knock 🚪]                 │
│ ╭─────────────────────────────╮ │
│ │ Why was the font always     │ │
│ │ tired?                      │ │
│ │ 👆 Tap to see the answer     │ │
│ ╰─────────────────────────────╯ │
│ ╭─────────────────────────────╮ │
│ │ What's the object-oriented  │ │
│ │ way to become wealthy?      │ │
│ │ 😂 Inheritance.              │ │
│ ╰─────────────────────────────╯ │
│  ...                            │
└─────────────────────────────────┘
```

### Requirements 📋

1. When the app opens, it **loads** up to 10 jokes from the internet.
2. While loading, show a **spinner** ⏳.
3. **Chips** at the top choose the **type**: General, Programming, Knock-knock.
4. Each joke shows its **setup**. **Tap** the card to show (or hide) the **punchline**. 😂
5. A **Refresh** button 🔄 loads **new** jokes.
6. If there's **no internet** or the server has a problem, show a **friendly message** and a **Try again** button.
7. If the list is **empty**, say so.
8. **Rotation** doesn't load the jokes again (the ViewModel keeps them). 🔄

---

## 19.7 Step 2: Add the Libraries 📦

We need **three** new things:

| Library | What it does |
|---|---|
| **Retrofit** | Sends requests and receives responses. 📡 |
| **kotlinx.serialization** (+ its plugin) | Turns **JSON text** into **Kotlin objects**. 🔄 |
| **Retrofit's kotlinx.serialization converter** | The **bridge** 🌉 between Retrofit and kotlinx.serialization. |

…plus the lifecycle libraries from Chapter 15, as always.

### `gradle/libs.versions.toml`

Add to the matching sections (keep everything that's already there):

```toml
[versions]
retrofit = "2.11.0"
kotlinxSerializationJson = "1.7.3"

[libraries]
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
retrofit-kotlinx-serialization = { group = "com.squareup.retrofit2", name = "converter-kotlinx-serialization", version.ref = "retrofit" }
kotlinx-serialization-json = { group = "org.jetbrains.kotlinx", name = "kotlinx-serialization-json", version.ref = "kotlinxSerializationJson" }
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
    alias(libs.plugins.kotlin.serialization)          // 👈 new
}

// ... android { } unchanged ...

dependencies {
    // ... existing lines ...
    implementation(libs.retrofit)
    implementation(libs.retrofit.kotlinx.serialization)
    implementation(libs.kotlinx.serialization.json)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)
}
```

**Sync Now** 🔄 ✅

| Line | Meaning |
|---|---|
| `retrofit = "2.11.0"` | One version for **both** Retrofit libraries — they must always match. |
| `version.ref = "kotlin"` (plugin) | The serialization plugin must have the **same version as Kotlin** — so we reuse the `kotlin` version that's already in the file. |
| `alias(libs.plugins.kotlin.serialization)` | Turns on the plugin. It **writes code for you** at build time for every `@Serializable` class. 🪄 |

> ℹ️ Newer versions may exist when you read this. Android Studio shows a **yellow hint** on old versions — you can let it update them. Retrofit uses **OkHttp** inside (another library that does the real network work); it comes **automatically** with Retrofit.

> ℹ️ The names in your `plugins { }` block may look a little different in newer Android Studio versions. Keep **your** existing lines, and only **add** the serialization one.

---

## 19.8 Step 3: The Internet Permission 🔑

Android apps can't use the internet **unless they say so**. Open **`app/src/main/AndroidManifest.xml`** and add **one line** above `<application`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.INTERNET" />    <!-- 👈 new -->

    <application
        ... (everything else stays the same) ...
```

| Code | Meaning |
|---|---|
| `<uses-permission ... />` | "This app **needs** permission to…" |
| `android.permission.INTERNET` | "…use the internet." 🌐 |

> 💡 The Internet permission is a "**normal**" permission: the user is **not** asked with a pop-up. It's simply allowed. (Permissions like **camera** and **location** do need a pop-up — that's Chapter 25. 📸📍)

> ⚠️ **Forgetting this line** is the **#1 beginner mistake** with the internet! The app crashes with *"SecurityException: Permission denied (missing INTERNET permission?)"*. Now you know! 😉

---

## 19.9 kotlinx.serialization — From JSON Text to Kotlin Objects 🔄

The server sends **text**. Our app wants a **`Joke` object**. Changing one into the other has fancy names:

| Direction | Name | Picture |
|---|---|---|
| JSON text → Kotlin object | **Deserialization** (decoding) | 📄 ➡️ 📦 |
| Kotlin object → JSON text | **Serialization** (encoding) | 📦 ➡️ 📄 |

You met `@Serializable` in Chapter 13 for **navigation routes**. Same library, same idea! 😎

### The `Joke` model

Make the package **`data.model`** and the file **`Joke.kt`**:

```kotlin
package com.example.jokemachine.data.model

import kotlinx.serialization.Serializable

@Serializable                                       // (1)
data class Joke(
    val id: Int,                                    // (2)
    val type: String,
    val setup: String,
    val punchline: String
)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `@Serializable` | "Plugin, please write the code to turn this class into JSON and back." 🪄 |
| 2 | `val id: Int`, `val type: String`, … | The property **names** match the JSON **keys** **exactly**: `"id"`, `"type"`, `"setup"`, `"punchline"`. The **types** match too: `23` → `Int`, `"programming"` → `String`. |

### A tiny experiment 🧪 (you can delete it afterwards)

Let's decode JSON **by hand** to see it working. In `MainActivity.kt`, inside `onCreate`, **after** `super.onCreate(savedInstanceState)`, add:

```kotlin
val text = """{"id":23,"type":"programming","setup":"Why?","punchline":"Because!"}"""   // (1)
val joke = Json.decodeFromString<Joke>(text)                                          // (2)
Log.d("JokeTest", "Decoded: $joke")                                                    // (3)
```

Imports:

```kotlin
import android.util.Log
import com.example.jokemachine.data.model.Joke
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
```

(If Android Studio shows `decodeFromString` import in grey as "unused", that's fine — you can delete it.)

| # | Code | Meaning |
|---|---|---|
| 1 | `"""..."""` | A **raw string** (Chapter 2): inside it you can use `"` freely, no `\"` needed. Perfect for JSON! |
| 2 | `Json.decodeFromString<Joke>(text)` | "Read this JSON text and make a `Joke` from it." 📄➡️📦 |
| 3 | `Log.d("JokeTest", ...)` | Write a message into **Logcat**, Android Studio's **diary** 📔 for developers. Users never see it. |

**Run the app.** At the bottom of Android Studio, open **Logcat** (the tab with a 🐱 cat icon, or **View → Tool Windows → Logcat**). In its search box, type `JokeTest`. You'll see:

```
Decoded: Joke(id=23, type=programming, setup=Why?, punchline=Because!)
```

🎉 JSON text became a real Kotlin object! (`data class` gives this nice printing — Chapter 3.)

**Now delete these 3 lines** (and the imports) — Retrofit will do this for us automatically.

### What if the JSON doesn't match? 🤨

Real APIs are messy. Here's how to handle the common cases:

**1. The JSON has extra keys we don't need**

```json
{ "id": 23, "type": "general", "setup": "...", "punchline": "...", "rating": 4.5, "author": "Sam" }
```

By default, kotlinx.serialization **refuses** unknown keys and throws an error! 😱 Fix it by creating a `Json` that **ignores** them:

```kotlin
val json = Json { ignoreUnknownKeys = true }
```

> ✅ **Always use `ignoreUnknownKeys = true` for APIs.** Servers often **add** new keys later — your app shouldn't break because of that.

**2. The key name is ugly, or not how Kotlin names things**

```json
{ "first_name": "Sam", "fav_color": "blue" }
```

```kotlin
@Serializable
data class Person(
    @SerialName("first_name") val firstName: String,     // JSON "first_name" → Kotlin firstName
    @SerialName("fav_color") val favoriteColor: String
)
```

`@SerialName("...")` = "In the JSON, this property is called **this**." Now your Kotlin code can use nice names. ✨ (Import `kotlinx.serialization.SerialName`.)

**3. A key is sometimes missing**

```kotlin
@Serializable
data class Joke(
    val id: Int,
    val setup: String,
    val punchline: String,
    val type: String = "general"       // missing in the JSON? Use "general".
)
```

A **default value** is used when the key is **missing**.

**4. A value can be `null`**

```json
{ "id": 5, "setup": "...", "punchline": null }
```

```kotlin
val punchline: String?       // ? → null is allowed (Chapter 3)
```

Without the `?`, a `null` makes decoding **fail**.

### Summary table 📋

| JSON situation | Kotlin solution |
|---|---|
| Key names match | Just use the same names ✅ |
| Extra keys we don't need | `Json { ignoreUnknownKeys = true }` |
| Different / ugly key names | `@SerialName("json_name")` |
| Key sometimes missing | Default value `= ...` |
| Value can be `null` | Nullable type `String?` |
| `{ }` inside `{ }` | Another `@Serializable` data class |
| `[ ]` | `List<...>` |

---

## 19.10 Retrofit — Talking to the Server 📡

**Retrofit** is the most popular library for calling web APIs on Android. You describe the API as a **Kotlin interface**, and Retrofit writes all the hard networking code for you. 🪄

### Step A: Describe the API — an interface

Make the package **`data.network`** and the file **`JokeApiService.kt`**:

```kotlin
package com.example.jokemachine.data.network

import com.example.jokemachine.data.model.Joke
import retrofit2.http.GET
import retrofit2.http.Path

interface JokeApiService {                                       // (1)

    @GET("jokes/{type}/ten")                                     // (2)
    suspend fun getTenJokes(@Path("type") type: String): List<Joke>   // (3)

    @GET("random_joke")                                          // (4)
    suspend fun getRandomJoke(): Joke
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `interface JokeApiService` | A **list of requests** this app can make — our **menu** 📜. Just function **headers**, no bodies! Retrofit fills them in. (Interfaces: Chapter 4.) |
| 2 | `@GET("jokes/{type}/ten")` | "This is a **GET** request to this **path**." `{type}` is a **hole** 🕳️ to fill in. |
| 3 | `suspend fun getTenJokes(@Path("type") type: String): List<Joke>` | `suspend` → it's called from a coroutine and **doesn't block** (Chapter 18). `@Path("type")` → "put this parameter into the `{type}` hole". The result is a `List<Joke>` — Retrofit **decodes** the JSON for us! 🎉 |
| 4 | `@GET("random_joke")` | Another menu item: one random joke. (We'll use it in a practice task.) |

**So when we call** `getTenJokes("programming")`, Retrofit:

1. builds the URL `https://official-joke-api.appspot.com/jokes/programming/ten` 🔗
2. sends a **GET** request 📤
3. waits for the response (**without blocking** — it's main-safe! 🛡️) ⏳
4. checks the status code (200? ✅) 🚦
5. turns the JSON into a `List<Joke>` 🔄
6. **returns** it to us 📦

**Six steps — one line of code.** That's why everybody uses Retrofit. 😍

### Other Retrofit annotations you'll meet 🏷️

| Annotation | Example | Becomes |
|---|---|---|
| `@GET("path")` | `@GET("users")` | `GET .../users` |
| `@Path("x")` | `@GET("users/{id}")` + `@Path("id") id: Int` with `5` | `.../users/5` |
| `@Query("x")` | `@GET("search")` + `@Query("q") text: String` with `"cats"` | `.../search?q=cats` |
| `@POST("path")` + `@Body` | `@POST("notes")` + `@Body note: Note` | Sends `note` as JSON |
| `@DELETE("path")` | `@DELETE("notes/{id}")` | Deletes note `id` |

### Step B: Build Retrofit itself 🏗️

Retrofit needs to know **2 things**:

1. The **base URL** — the start of every address.
2. **How to read JSON** — a **converter**.

```kotlin
private val json = Json { ignoreUnknownKeys = true }                              // (1)

private val retrofit: Retrofit = Retrofit.Builder()                               // (2)
    .baseUrl("https://official-joke-api.appspot.com/")                            // (3)
    .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))   // (4)
    .build()                                                                       // (5)

val jokeApiService: JokeApiService = retrofit.create(JokeApiService::class.java)  // (6)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `Json { ignoreUnknownKeys = true }` | Our JSON reader, which **ignores** extra keys (19.9). |
| 2 | `Retrofit.Builder()` | A **builder**: set options one by one, then `.build()`. Like ordering a burger: "bun, cheese, no onions… done!" 🍔 |
| 3 | `.baseUrl("https://.../")` | The **start** of every URL. **Must end with `/`!** Otherwise: crash with *"baseUrl must end in /"*. |
| 4 | `.addConverterFactory(...)` | "Use **kotlinx.serialization** to read and write the bodies." `"application/json".toMediaType()` tells it the data type is **JSON**. |
| 5 | `.build()` | Make the Retrofit object. |
| 6 | `retrofit.create(JokeApiService::class.java)` | 🪄 **The magic line:** Retrofit **creates a real object** that implements our interface. `JokeApiService::class.java` = "the class of this interface" (Retrofit is a Java library, so it wants the **Java** class). |

**Base URL + path = full URL:**

```
"https://official-joke-api.appspot.com/"  +  "jokes/programming/ten"
= "https://official-joke-api.appspot.com/jokes/programming/ten"  ✅
```

> ⚠️ Notice: the base URL **ends** with `/`, and the path in `@GET` does **not start** with `/`. Keep this habit and URLs will always join correctly.

> 💡 **Build Retrofit only once!** Creating it is slow-ish. We'll put it in the **AppContainer** (Chapter 16), so the whole app shares **one**. 🧰

---

## 19.11 What Can Go Wrong? ⚠️

On your computer, the internet "just works". On a **phone**, it's very different: 🚇 tunnels, 🛗 elevators, ✈️ airplane mode, 📶 one bar of signal, a sleepy server…

A **good** app expects problems and handles them **kindly**. Here's what can happen when we call `getTenJokes(...)`:

| Problem | Example | Error (exception) type | Package |
|---|---|---|---|
| **No connection** 📶 | Airplane mode, no Wi-Fi, server unreachable, too slow (timeout) | **`IOException`** | `java.io` |
| **Server said no** 🚦 | Status 404, 500, 503… | **`HttpException`** (has `.code()`) | `retrofit2` |
| **Strange data** 🤔 | JSON doesn't match our data class | **`SerializationException`** | `kotlinx.serialization` |

If we **don't catch** these, the app **crashes**. 💥 If we **do**, we can show a friendly message:

| Exception | Friendly message for the user |
|---|---|
| `IOException` | "No internet connection 📶 Check your Wi-Fi or mobile data." |
| `HttpException` | "The joke server has a problem (error 503) 🛠️ Please try again later." |
| `SerializationException` | "The server sent something we don't understand 🤔" |

> 🎯 **Never** show raw errors like *"java.net.UnknownHostException: Unable to resolve host…"* to users. They're scary and unhelpful. 😱 Show a **simple sentence** and a **Try again** button. (You can still write the details to **Logcat** for yourself.)

---

## 19.12 Loading, Success, Error — The Three Faces of Internet Screens 🎭

Every screen that loads from the internet is **always** in **one** of these situations:

| State | What the user sees |
|---|---|
| ⏳ **Loading** | A spinner |
| ✅ **Success** | The data (or "nothing found" if the list is empty) |
| ❌ **Error** | A message + **Try again** |

"Always exactly one of a few cases" → a **sealed interface**! (Chapter 4 — and just like `DownloadStatus` in Chapter 18.)

```kotlin
sealed interface JokesLoadState {
    data object Loading : JokesLoadState
    data class Success(val jokes: List<Joke>) : JokesLoadState
    data class Error(val message: String) : JokesLoadState
}
```

```
        open app / refresh / retry
                  │
                  ▼
            ┌──────────┐
            │ Loading ⏳│
            └────┬─────┘
          worked │  failed
         ┌───────┴────────┐
         ▼                ▼
   ┌───────────┐    ┌───────────┐
   │ Success ✅ │    │  Error ❌  │──── Try again ───▶ Loading
   └───────────┘    └───────────┘
```

> 💡 Why not three Booleans (`isLoading`, `hasError`, `hasData`)? Because then **impossible** mixes can happen, like `isLoading = true` **and** `hasError = true` at once. 🤯 With a sealed interface, the screen is **always** in exactly **one** state. The compiler protects you. 🛡️

---

## 19.13 Step 4: Plan the Files 📁

We'll use the **MVVM** structure from Chapter 16:

```
com.example.jokemachine
 ├── JokeMachineApplication.kt
 ├── MainActivity.kt
 ├── data/
 │    ├── model/
 │    │    ├── Joke.kt                 (done ✅)
 │    │    └── JokeCategory.kt
 │    ├── network/
 │    │    └── JokeApiService.kt       (done ✅)
 │    ├── JokesRepository.kt           (interface)
 │    └── NetworkJokesRepository.kt
 ├── di/
 │    └── AppContainer.kt              (Retrofit lives here!)
 └── ui/
      ├── theme/                       (already there)
      └── jokes/
           ├── JokesUiState.kt
           ├── JokesViewModel.kt
           └── JokesScreen.kt
```

```
📱 JokesScreen ──events──▶ 🧠 JokesViewModel ──▶ 🏪 JokesRepository ──▶ 📡 JokeApiService ──▶ 🌐 Server
             ◀──UiState──                     ◀── List<Joke> ──       ◀── List<Joke> ──     ◀── JSON
```

Make the packages: right-click `com.example.jokemachine` → **New → Package** → `data.model`, `data.network`, `di`, `ui.jokes`.

---

## 19.14 Step 5: The Data Layer 🏪

### `data/model/JokeCategory.kt`

```kotlin
package com.example.jokemachine.data.model

enum class JokeCategory(val apiName: String, val label: String) {   // (1)
    GENERAL("general", "General 😄"),
    PROGRAMMING("programming", "Programming 💻"),
    KNOCK_KNOCK("knock-knock", "Knock-knock 🚪")
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `enum class JokeCategory(val apiName: String, val label: String)` | The 3 types we offer (enums with properties: Chapter 4). `apiName` is the word the **server** understands; `label` is what the **user** sees. Keeping them separate means we can change the label (or translate it! 🌍) without breaking the API call. |

### `data/JokesRepository.kt`

```kotlin
package com.example.jokemachine.data

import com.example.jokemachine.data.model.Joke
import com.example.jokemachine.data.model.JokeCategory

interface JokesRepository {
    suspend fun getJokes(category: JokeCategory): List<Joke>
}
```

The **promise** 🤝: "I can give you jokes of a category." The ViewModel only knows **this** — not Retrofit, not URLs, not JSON. (Chapter 16: the ViewModel shouldn't care **where** data comes from.)

### `data/NetworkJokesRepository.kt`

```kotlin
package com.example.jokemachine.data

import com.example.jokemachine.data.model.Joke
import com.example.jokemachine.data.model.JokeCategory
import com.example.jokemachine.data.network.JokeApiService

class NetworkJokesRepository(
    private val apiService: JokeApiService                           // (1)
) : JokesRepository {

    override suspend fun getJokes(category: JokeCategory): List<Joke> =
        apiService.getTenJokes(category.apiName)                     // (2)
            .map { joke -> joke.copy(setup = cleanLines(joke.setup)) }   // (3)

    private fun cleanLines(text: String): String =                   // (4)
        text.lines().joinToString("\n") { line -> line.trim() }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `private val apiService: JokeApiService` | The repository **receives** the API service (it doesn't build it — the AppContainer does). |
| 2 | `apiService.getTenJokes(category.apiName)` | The real internet call! 📡 `GENERAL` → `"general"`. It's a suspend call, so this function is `suspend` too. |
| 3 | `.map { joke -> joke.copy(setup = ...) }` | Knock-knock jokes come with messy spaces around the line breaks (`"Knock knock. \n Who's there? \n …"`). We **clean** each setup before giving it to the app. `copy` makes a new `Joke` with only `setup` changed (Chapter 3). |
| 4 | `cleanLines(text)` | `lines()` → split the text into a list of lines. `trim()` → remove spaces at the start and end of each line. `joinToString("\n")` → glue them back with line breaks. |

> 💡 **This is a repository's job:** take **raw** data from the server and give the app **clean, ready-to-use** data. 🧼 The screen never needs to know the server was messy.

---

## 19.15 Step 6: The AppContainer and Application 🧰

### `di/AppContainer.kt`

```kotlin
package com.example.jokemachine.di

import com.example.jokemachine.data.JokesRepository
import com.example.jokemachine.data.NetworkJokesRepository
import com.example.jokemachine.data.network.JokeApiService
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory

interface AppContainer {
    val jokesRepository: JokesRepository
}

class DefaultAppContainer : AppContainer {

    private val baseUrl = "https://official-joke-api.appspot.com/"         // (1)

    private val json = Json { ignoreUnknownKeys = true }                   // (2)

    private val retrofit: Retrofit = Retrofit.Builder()                    // (3)
        .baseUrl(baseUrl)
        .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
        .build()

    private val jokeApiService: JokeApiService by lazy {                   // (4)
        retrofit.create(JokeApiService::class.java)
    }

    override val jokesRepository: JokesRepository by lazy {                // (5)
        NetworkJokesRepository(jokeApiService)
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `baseUrl` | The **one** place the server's address is written. Ends with `/`! |
| 2 | `json` | Our JSON reader, ignoring unknown keys. |
| 3 | `retrofit` | Built **once** for the whole app (19.10). |
| 4 | `jokeApiService by lazy { ... }` | Created the **first time** someone needs it (Chapter 16), then reused. |
| 5 | `jokesRepository by lazy { ... }` | The repository, **given** the API service. This is the **one line** to change if we ever want a **different** repository — for example a fake one for tests (Chapter 27). 🔧 |

**The imports explained** (they look scary, but they're just addresses 🏠):

| Import | What it is |
|---|---|
| `kotlinx.serialization.json.Json` | The JSON reader. |
| `okhttp3.MediaType.Companion.toMediaType` | The `toMediaType()` function for `"application/json"`. From **OkHttp**, which comes with Retrofit. |
| `retrofit2.Retrofit` | Retrofit itself. |
| `retrofit2.converter.kotlinx.serialization.asConverterFactory` | The **bridge** 🌉: `json.asConverterFactory(...)`. |

> 💡 If `asConverterFactory` or `toMediaType` is red, place the cursor on it and press **Alt + Enter** → **Import**. If it's still red, check that you added **`converter-kotlinx-serialization`** and pressed **Sync**.

### `JokeMachineApplication.kt` (in the main package)

```kotlin
package com.example.jokemachine

import android.app.Application
import com.example.jokemachine.di.AppContainer
import com.example.jokemachine.di.DefaultAppContainer

class JokeMachineApplication : Application() {

    lateinit var container: AppContainer

    override fun onCreate() {
        super.onCreate()
        container = DefaultAppContainer()
    }
}
```

Exactly like Chapter 16. 🏛️

### `AndroidManifest.xml` — register it

```xml
<uses-permission android:name="android.permission.INTERNET" />

<application
    android:name=".JokeMachineApplication"
    ... the rest stays the same ... >
```

✅ Two changes in the manifest now: the **permission** and the **`android:name`**.

---

## 19.16 Step 7: The ViewModel 🧠

### `ui/jokes/JokesUiState.kt`

```kotlin
package com.example.jokemachine.ui.jokes

import com.example.jokemachine.data.model.Joke
import com.example.jokemachine.data.model.JokeCategory

sealed interface JokesLoadState {                                      // (1)
    data object Loading : JokesLoadState
    data class Success(val jokes: List<Joke>) : JokesLoadState
    data class Error(val message: String) : JokesLoadState
}

data class JokesUiState(                                               // (2)
    val category: JokeCategory = JokeCategory.GENERAL,
    val loadState: JokesLoadState = JokesLoadState.Loading,
    val revealedIds: Set<Int> = emptySet()                             // (3)
)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `JokesLoadState` | The three faces from 19.12. ⏳✅❌ |
| 2 | `JokesUiState` | **Everything** the screen needs: the chosen chip, the load state, and which punchlines are shown. |
| 3 | `revealedIds: Set<Int>` | The **ids** of jokes whose punchline is visible. A `Set` (Chapter 3) because each id is either **in** or **not in** — no duplicates. |

### `ui/jokes/JokesViewModel.kt`

```kotlin
package com.example.jokemachine.ui.jokes

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.ViewModelProvider.AndroidViewModelFactory.Companion.APPLICATION_KEY
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.example.jokemachine.JokeMachineApplication
import com.example.jokemachine.data.JokesRepository
import com.example.jokemachine.data.model.JokeCategory
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.serialization.SerializationException
import retrofit2.HttpException
import java.io.IOException

class JokesViewModel(
    private val repository: JokesRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(JokesUiState())
    val uiState: StateFlow<JokesUiState> = _uiState.asStateFlow()

    private var loadJob: Job? = null

    init {                                                             // (1)
        loadJokes()
    }

    fun onCategorySelected(category: JokeCategory) {
        if (category == _uiState.value.category) return                // (2)
        _uiState.update { it.copy(category = category) }
        loadJokes()
    }

    fun onRefreshClick() = loadJokes()

    fun onRetryClick() = loadJokes()

    fun onJokeClick(jokeId: Int) {                                     // (3)
        _uiState.update { state ->
            val newIds = if (jokeId in state.revealedIds) {
                state.revealedIds - jokeId
            } else {
                state.revealedIds + jokeId
            }
            state.copy(revealedIds = newIds)
        }
    }

    private fun loadJokes() {
        loadJob?.cancel()                                              // (4)
        val category = _uiState.value.category

        loadJob = viewModelScope.launch {
            _uiState.update {
                it.copy(loadState = JokesLoadState.Loading, revealedIds = emptySet())   // (5)
            }

            val newLoadState = try {                                   // (6)
                val jokes = repository.getJokes(category)              // (7) 📡
                JokesLoadState.Success(jokes)
            } catch (e: IOException) {                                 // (8)
                JokesLoadState.Error("No internet connection 📶\nCheck your Wi-Fi or mobile data.")
            } catch (e: HttpException) {
                JokesLoadState.Error("The joke server has a problem (error ${e.code()}) 🛠️\nPlease try again later.")
            } catch (e: SerializationException) {
                JokesLoadState.Error("The server sent something we don't understand 🤔")
            }

            _uiState.update { it.copy(loadState = newLoadState) }      // (9)
        }
    }

    companion object {
        val Factory: ViewModelProvider.Factory = viewModelFactory {    // (10)
            initializer {
                val app = this[APPLICATION_KEY] as JokeMachineApplication
                JokesViewModel(repository = app.container.jokesRepository)
            }
        }
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `init { loadJokes() }` | `init` runs **once**, when the ViewModel is **created** (Chapter 3). So jokes load when the screen first opens — but **not** again after rotation, because the ViewModel survives! 🔄✅ |
| 2 | `if (category == ...) return` | Tapping the chip that's **already** selected does nothing — no wasted request. |
| 3 | `onJokeClick(jokeId)` | Toggle: if the id is in the set, **remove** it (hide); if not, **add** it (show). `Set - x` and `Set + x` make **new** sets (immutable state, Chapter 15). |
| 4 | `loadJob?.cancel()` | If an **older** request is still running, cancel it! Imagine: tap "General", then quickly "Programming". Without this, the slow "General" answer might arrive **last** and show the **wrong** jokes under the "Programming" chip. 🏃‍♂️🏃 This is called a **race**. Cancelling the old job prevents it. ✅ |
| 5 | `loadState = Loading, revealedIds = emptySet()` | Show the spinner ⏳ and forget the old revealed punchlines. |
| 6 | `val newLoadState = try { ... } catch ...` | **`try` is an expression** in Kotlin — it **gives back a value**: the last line of `try` if everything worked, or the last line of the `catch` that ran. Very neat! ✨ |
| 7 | `repository.getJokes(category)` | 📡 **The internet call.** The coroutine **pauses** here (the screen stays smooth) until the answer comes. Main-safe thanks to Retrofit. 🛡️ |
| 8 | `catch (e: IOException)` etc. | One `catch` for each problem from 19.11, each with a **friendly** message. `\n` = new line. `e.code()` = the status number, like 404 or 503. We catch **specific** errors, so **cancellation** passes through correctly (Chapter 18). |
| 9 | `_uiState.update { it.copy(loadState = newLoadState) }` | Show the result: ✅ or ❌. |
| 10 | `Factory` | Builds the ViewModel with the repository from the AppContainer — the **same recipe** as Chapter 16. 🧰 |

> 🤔 **Why does the ViewModel import `HttpException` from Retrofit?** Good eye! 👀 Strictly, the ViewModel shouldn't know about Retrofit. A cleaner way is for the repository to turn errors into **its own** error types. For now, this simpler way is fine and very common. You'll see more ways later in the book.

---

## 19.17 Step 8: The Screen 📱

### `ui/jokes/JokesScreen.kt`

```kotlin
package com.example.jokemachine.ui.jokes

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.Button
import androidx.compose.material3.Card
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
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.jokemachine.data.model.Joke
import com.example.jokemachine.data.model.JokeCategory
import com.example.jokemachine.ui.theme.JokeMachineTheme

@Composable
fun JokesRoute(
    viewModel: JokesViewModel = viewModel(factory = JokesViewModel.Factory)
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    JokesScreen(
        uiState = uiState,
        onCategorySelected = viewModel::onCategorySelected,
        onRefreshClick = viewModel::onRefreshClick,
        onRetryClick = viewModel::onRetryClick,
        onJokeClick = viewModel::onJokeClick
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun JokesScreen(
    uiState: JokesUiState,
    onCategorySelected: (JokeCategory) -> Unit,
    onRefreshClick: () -> Unit,
    onRetryClick: () -> Unit,
    onJokeClick: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    Scaffold(
        modifier = modifier,
        topBar = {
            TopAppBar(
                title = { Text("Joke Machine 😂") },
                actions = {
                    IconButton(
                        onClick = onRefreshClick,
                        enabled = uiState.loadState !is JokesLoadState.Loading     // (1)
                    ) {
                        Icon(Icons.Filled.Refresh, contentDescription = "Load new jokes")
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(modifier = Modifier.padding(innerPadding)) {
            CategoryChips(
                selected = uiState.category,
                onCategorySelected = onCategorySelected
            )

            when (val loadState = uiState.loadState) {                             // (2)
                JokesLoadState.Loading -> LoadingContent()
                is JokesLoadState.Error -> ErrorContent(
                    message = loadState.message,
                    onRetryClick = onRetryClick
                )
                is JokesLoadState.Success -> JokesList(
                    jokes = loadState.jokes,
                    revealedIds = uiState.revealedIds,
                    onJokeClick = onJokeClick
                )
            }
        }
    }
}

@Composable
fun CategoryChips(
    selected: JokeCategory,
    onCategorySelected: (JokeCategory) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .horizontalScroll(rememberScrollState())                               // (3)
            .padding(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        JokeCategory.entries.forEach { category ->                                 // (4)
            FilterChip(
                selected = category == selected,
                onClick = { onCategorySelected(category) },
                label = { Text(category.label) }
            )
        }
    }
}

@Composable
fun LoadingContent(modifier: Modifier = Modifier) {
    Box(
        modifier = modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        CircularProgressIndicator()
    }
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
        Text("😵", style = MaterialTheme.typography.displayMedium)
        Text(message, textAlign = TextAlign.Center)
        Button(onClick = onRetryClick) {
            Text("Try again 🔁")
        }
    }
}

@Composable
fun JokesList(
    jokes: List<Joke>,
    revealedIds: Set<Int>,
    onJokeClick: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    if (jokes.isEmpty()) {                                                         // (5)
        Box(modifier = modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text("No jokes found 🤷")
        }
        return                                                                     // (6)
    }

    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        items(jokes, key = { joke -> joke.id }) { joke ->                          // (7)
            JokeCard(
                joke = joke,
                isRevealed = joke.id in revealedIds,
                onClick = { onJokeClick(joke.id) }
            )
        }
    }
}

@Composable
fun JokeCard(
    joke: Joke,
    isRevealed: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        onClick = onClick,                                                         // (8)
        modifier = modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(joke.setup, style = MaterialTheme.typography.titleMedium)
            if (isRevealed) {
                Text(
                    text = "😂 ${joke.punchline}",
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.primary
                )
            } else {
                Text(
                    text = "👆 Tap to see the answer",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}
```

**The important parts:**

| # | Code | Meaning |
|---|---|---|
| 1 | `enabled = uiState.loadState !is JokesLoadState.Loading` | `!is` = "is **not** of this type". No refreshing while already loading. |
| 2 | `when (val loadState = uiState.loadState)` | Show **one** of the three faces. Sealed → the compiler checks that we handled **all** of them. 🛡️ |
| 3 | `.horizontalScroll(rememberScrollState())` | If the chips don't fit on a small phone, the user can **swipe** them sideways (Chapter 6). |
| 4 | `JokeCategory.entries.forEach { ... }` | One chip per category. Add a 4th category to the enum → a 4th chip appears **by itself**. 😎 |
| 5 | `if (jokes.isEmpty())` | ✅ Success, but **nothing** came back (remember `/jokes/pirate/ten` → `[]`). Say so kindly. |
| 6 | `return` | Stop here — don't draw the empty list. (Yes, Composables can `return` early!) |
| 7 | `key = { joke -> joke.id }` | The server gives each joke a unique `id` — a **perfect** key (Chapter 10). |
| 8 | `Card(onClick = onClick)` | A **clickable** Card, with the ripple effect built in. Tap → show/hide the punchline. |

### Previews 🖼️ (add at the bottom of the file)

```kotlin
private val previewJokes = listOf(
    Joke(1, "programming", "Why do programmers prefer dark mode?", "Because light attracts bugs. 🐛"),
    Joke(2, "programming", "Why was the font always tired?", "It was working in bold.")
)

@Preview(showBackground = true)
@Composable
fun JokesScreenSuccessPreview() {
    JokeMachineTheme {
        JokesScreen(
            uiState = JokesUiState(
                category = JokeCategory.PROGRAMMING,
                loadState = JokesLoadState.Success(previewJokes),
                revealedIds = setOf(1)
            ),
            onCategorySelected = {}, onRefreshClick = {}, onRetryClick = {}, onJokeClick = {}
        )
    }
}

@Preview(showBackground = true)
@Composable
fun JokesScreenErrorPreview() {
    JokeMachineTheme {
        JokesScreen(
            uiState = JokesUiState(
                loadState = JokesLoadState.Error("No internet connection 📶\nCheck your Wi-Fi or mobile data.")
            ),
            onCategorySelected = {}, onRefreshClick = {}, onRetryClick = {}, onJokeClick = {}
        )
    }
}

@Preview(showBackground = true)
@Composable
fun JokesScreenLoadingPreview() {
    JokeMachineTheme {
        JokesScreen(
            uiState = JokesUiState(loadState = JokesLoadState.Loading),
            onCategorySelected = {}, onRefreshClick = {}, onRetryClick = {}, onJokeClick = {}
        )
    }
}
```

> ℹ️ If `Icons` or `Icons.Filled.Refresh` is red even after **Alt + Enter**, add the `material-icons-core` library (Chapter 5, section 5.8) and Sync.

🎉 **Thanks to the Route + Screen pattern (Chapter 15), you can see all three states in the preview — without any internet at all!** That's a huge time saver. ⏱️

> 💡 `Joke(1, "programming", ...)` — we pass the values **in order** (id, type, setup, punchline) without names. Fine for short previews; in real code, named arguments are clearer.

---

## 19.18 Step 9: `MainActivity.kt` 🔗

```kotlin
package com.example.jokemachine

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.jokemachine.ui.jokes.JokesRoute
import com.example.jokemachine.ui.theme.JokeMachineTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            JokeMachineTheme {
                JokesRoute()
            }
        }
    }
}
```

(Make sure the 3-line JSON experiment from 19.9 is **deleted**.)

**Run the app!** ▶️ After a moment… **jokes from the internet!** 🌐😂🎉

> 🐢 **Emulator has no internet?** Check that your **computer** is online. Then try: in the emulator, swipe down from the top and make sure **Wi-Fi** is on and **Airplane mode** is off. If it still fails, close the emulator and in **Device Manager** choose **⋮ → Cold Boot Now**.

---

## 19.19 Test Checklist ✅

| Test | How | Expected | ✓ |
|---|---|---|---|
| First load | Open the app | Spinner, then up to 10 General jokes | ☐ |
| Reveal | Tap a card | Punchline appears 😂; tap again → hides | ☐ |
| Category | Tap "Programming 💻" | Spinner, then programming jokes | ☐ |
| Fewer jokes | Tap "Knock-knock 🚪" | Only **5** jokes, with clean line breaks | ☐ |
| Same chip | Tap the selected chip again | Nothing happens (no reload) | ☐ |
| Refresh | Tap 🔄 | New random jokes, all punchlines hidden | ☐ |
| Rotation | Reveal 2 punchlines, rotate 🔄 | **Same** jokes, same punchlines shown — **no** reload | ☐ |
| No internet | Turn on **Airplane mode** ✈️ → tap 🔄 | "No internet connection 📶" + Try again | ☐ |
| Recover | Airplane mode **off** → Try again | Jokes load ✅ | ☐ |
| Fast taps | Tap General → Programming → Knock-knock quickly | You end with **Knock-knock** jokes (no race!) | ☐ |
| Dark mode | Turn on dark theme | Looks good 🌙 | ☐ |

### Make the server "fail" on purpose 🧪

To **see** the `HttpException` message, change the path in `JokeApiService` for a moment:

```kotlin
@GET("jokes/{type}/tenn")       // 👈 typo on purpose
```

Run → "The joke server has a problem (error **404**) 🛠️". ✅ Now **change it back**!

And to see the `SerializationException` message, temporarily **add** a property to `Joke`:

```kotlin
val rating: Int,                // 👈 no such key in the JSON, and no default value
```

Run → "The server sent something we don't understand 🤔" (the JSON has no `"rating"` key, so decoding fails). ✅ **Remove it again!** (Also remove it from the preview jokes if Android Studio complains there.)

> 💡 Testing the **sad paths** 😢 is just as important as testing the happy path. Real users **will** hit them!

---

## 19.20 Common Mistakes and Fixes 🔧

| Mistake | Error / Problem | Fix |
|---|---|---|
| No `INTERNET` permission | 💥 *SecurityException: Permission denied (missing INTERNET permission?)* | Add `<uses-permission android:name="android.permission.INTERNET" />`. |
| Base URL without `/` at the end | 💥 *IllegalArgumentException: baseUrl must end in /* | `"https://…appspot.com/"` |
| `http://` instead of `https://` | *CLEARTEXT communication … not permitted* | Use `https://`. |
| Forgot `@Serializable` | 💥 *Serializer for class 'Joke' is not found* | Add `@Serializable` to **every** data class in the JSON (also nested ones). |
| Forgot the serialization **plugin** | Same error, even with `@Serializable` | Add `alias(libs.plugins.kotlin.serialization)` and Sync. |
| Server added a new key | 💥 *Encountered an unknown key 'xyz'* | `Json { ignoreUnknownKeys = true }` |
| Property name ≠ JSON key | Decoding error | Same name, or `@SerialName("json_key")`. |
| JSON value is `null` | Decoding error | Make it nullable: `String?` |
| Calling the API without `suspend` / outside a coroutine | *Suspend function … should be called only from a coroutine* | Call it in `viewModelScope.launch { }`. |
| No `try`/`catch` | 💥 Crash when offline | Catch `IOException`, `HttpException`, `SerializationException`. |
| Building Retrofit in the ViewModel or Composable | Slow; many copies | Build it **once** in the AppContainer. |
| Loading in the Composable body | Loads again on every recomposition 🔁 | Load in the ViewModel's `init`. |
| Old request finishes after a new one | Wrong data on screen (race) | Cancel the old `Job` before starting a new one. |
| Showing `e.message` to users | Scary technical text 😱 | Show a friendly sentence. |
| `asConverterFactory` is red | Missing converter library | Add `converter-kotlinx-serialization` and Sync. |

---

## 19.21 Summary — What You Learned 🎓

✅ Apps are **clients** 📱 that send **requests** to **servers** 🖥️ and get **responses**.

✅ A **URL** = scheme (`https://`) + domain + path (+ `?query`). **Always `https`.** 🔒

✅ **HTTP methods:** `GET` (read), `POST` (create), `PUT`/`PATCH` (change), `DELETE` (remove).
**Status codes:** 2xx ✅ success, 4xx ❌ app's mistake, 5xx ❌ server's mistake.

✅ **JSON:** `{ }` → data class, `[ ]` → `List`, `"key"` → property. Always **look** at the real JSON in a browser first. 🔍

✅ **`INTERNET` permission** in the manifest — no pop-up needed.

✅ **kotlinx.serialization:** `@Serializable`, `Json { ignoreUnknownKeys = true }`, `@SerialName`, default values, nullable types.

✅ **Retrofit:** an **interface** with `@GET`, `@Path`, `@Query` and **`suspend`** functions. Build it **once** with a base URL (ending in `/`) and a converter, then `retrofit.create(...)`. Its calls are **main-safe**. 🛡️

✅ **Errors:** `IOException` 📶, `HttpException` 🚦, `SerializationException` 🤔 → friendly messages + **Try again**.

✅ **Loading / Success / Error** as a **sealed interface**, plus the **empty** case.

✅ **MVVM:** API service → Repository (cleans data 🧼) → ViewModel (loads in `init`, cancels old jobs) → Screen. Retrofit lives in the **AppContainer**. 🧰

✅ You built the **Joke Machine** 😂 — your first app with **real data from the internet**! 🌐🎉

---

## 19.22 Practice Time 🏋️

**Task 1 — JSON to Kotlin 📄➡️📦:**
Write the `@Serializable` data classes for this JSON:

```json
{
  "title": "Space Facts",
  "pageCount": 120,
  "isAvailable": true,
  "tags": ["space", "planets", "kids"],
  "author": { "name": "Mia", "country": "Kenya" },
  "rating": null
}
```

**Task 2 — Nicer names 🏷️:**
The server sends `{ "user_name": "sam99", "avatar_url": "https://...", "is_pro": false }`. Make a data class with the Kotlin names `userName`, `avatarUrl`, and `isPro`.

**Task 3 — Write the Retrofit functions ✍️:**
For an imaginary API at `https://api.example.com/`, write the interface functions for:
a) `GET /books` → a list of `Book`
b) `GET /books/42` (any id) → one `Book`
c) `GET /books/search?title=space&page=2` → a list of `Book`

**Task 4 — A random joke dialog 🎲:**
Add a **"Surprise me! 🎲"** button (for example in the top bar) to the Joke Machine. It calls `getRandomJoke()` and shows the joke in an `AlertDialog` (Chapter 11) with the setup as the title and the punchline as the text. If it fails, show nothing (keep it simple).

**Task 5 — Find the 3 bugs 🐛🐛🐛:**

```kotlin
data class Planet(
    val name: String,
    val moons: Int
)

interface PlanetApi {
    @GET("/planets")
    fun getPlanets(): List<Planet>
}

val retrofit = Retrofit.Builder()
    .baseUrl("https://api.example.com")
    .addConverterFactory(Json.asConverterFactory("application/json".toMediaType()))
    .build()
```

**Task 6 — A friendly error helper 🤝:**
Write a function `fun friendlyMessage(e: Exception): String` that returns the right friendly message for `IOException`, `HttpException` (with special text for 404: "We couldn't find that 🤷"), `SerializationException`, and anything else ("Something went wrong 😕"). Use `when` with `is`.

---

### Answers

**Task 1:**

```kotlin
@Serializable
data class Book(
    val title: String,
    val pageCount: Int,
    val isAvailable: Boolean,
    val tags: List<String>,
    val author: Author,
    val rating: Double?            // null in the JSON → must be nullable
)

@Serializable
data class Author(
    val name: String,
    val country: String
)
```

💡 `rating` is `null` here, so we can't see if it's normally a whole number or not. `Double?` is a safe guess for ratings like `4.5`. (When unsure, check the API's documentation 📚.)

**Task 2:**

```kotlin
@Serializable
data class User(
    @SerialName("user_name") val userName: String,
    @SerialName("avatar_url") val avatarUrl: String,
    @SerialName("is_pro") val isPro: Boolean
)
```

**Task 3:**

```kotlin
interface BookApiService {

    @GET("books")
    suspend fun getBooks(): List<Book>

    @GET("books/{id}")
    suspend fun getBook(@Path("id") id: Int): Book

    @GET("books/search")
    suspend fun searchBooks(
        @Query("title") title: String,
        @Query("page") page: Int
    ): List<Book>
}
```

With the base URL `https://api.example.com/`, `searchBooks("space", 2)` calls `https://api.example.com/books/search?title=space&page=2`. ✅ (`Query` import: `retrofit2.http.Query`.)

**Task 4:**

Add to `JokesRepository` and `NetworkJokesRepository`:

```kotlin
// JokesRepository
suspend fun getRandomJoke(): Joke

// NetworkJokesRepository
override suspend fun getRandomJoke(): Joke = apiService.getRandomJoke()
```

In `JokesUiState`, add:

```kotlin
val surpriseJoke: Joke? = null
```

In `JokesViewModel`:

```kotlin
fun onSurpriseClick() {
    viewModelScope.launch {
        try {
            val joke = repository.getRandomJoke()
            _uiState.update { it.copy(surpriseJoke = joke) }
        } catch (e: IOException) {
            // keep it simple: ignore
        } catch (e: HttpException) {
            // ignore
        }
    }
}

fun onSurpriseDismiss() {
    _uiState.update { it.copy(surpriseJoke = null) }
}
```

In `JokesScreen` (add the two new parameters `onSurpriseClick` and `onSurpriseDismiss`, and pass them from `JokesRoute`):

```kotlin
// in TopAppBar actions, before the refresh button:
TextButton(onClick = onSurpriseClick) { Text("🎲") }

// anywhere inside JokesScreen, e.g. right after Scaffold { ... }:
uiState.surpriseJoke?.let { joke ->
    AlertDialog(
        onDismissRequest = onSurpriseDismiss,
        title = { Text(joke.setup) },
        text = { Text("😂 ${joke.punchline}") },
        confirmButton = {
            TextButton(onClick = onSurpriseDismiss) { Text("Haha! 😆") }
        }
    )
}
```

💡 `uiState.surpriseJoke?.let { ... }` → "If there **is** a surprise joke, show the dialog with it" (Chapter 4). Closing the dialog sets it back to `null` → the dialog disappears. 🎲

**Task 5:**

| # | Bug | Fix |
|---|---|---|
| 1 | `Planet` has no **`@Serializable`** → *Serializer for class 'Planet' is not found*. | Add `@Serializable`. |
| 2 | `getPlanets()` is **not `suspend`** → 💥 *Unable to create call adapter for java.util.List…* (without `suspend`, Retrofit expects an old-style `Call<...>` return type). | `suspend fun getPlanets(): List<Planet>` |
| 3 | The base URL **doesn't end with `/`** → crash *"baseUrl must end in /"*. | `"https://api.example.com/"` |

Bonus 🌟: `@GET("/planets")` starts with `/` — it works, but a leading `/` means "start from the **domain**", which can **drop** part of a base URL like `https://example.com/api/`. Keep the habit: **no** leading `/` → `@GET("planets")`. And `Json.asConverterFactory(...)` uses the **default** `Json` (no `ignoreUnknownKeys`) — not a bug yet, but a future crash waiting to happen. 😉

**Task 6:**

```kotlin
fun friendlyMessage(e: Exception): String = when (e) {
    is IOException -> "No internet connection 📶"
    is HttpException -> if (e.code() == 404) {
        "We couldn't find that 🤷"
    } else {
        "The server has a problem (error ${e.code()}) 🛠️"
    }
    is SerializationException -> "The server sent something we don't understand 🤔"
    else -> "Something went wrong 😕"
}
```

💡 After `is HttpException ->`, Kotlin **knows** `e` is an `HttpException`, so `e.code()` works (smart cast). With this helper, the ViewModel's three `catch` blocks could become **one** — try it! (Remember Chapter 18: if you catch `Exception`, rethrow `CancellationException` first.)

---

## 19.23 Challenges 🚀

### Challenge 1: Keep the old jokes while refreshing ⭐⭐
Right now, Refresh **hides** the list and shows a big spinner. Instead, keep the old jokes visible and show a thin `LinearProgressIndicator` at the top while loading.
*Hint:* add `val isRefreshing: Boolean = false` to `JokesUiState`, and only use `Loading` for the **first** load.

### Challenge 2: Pull to refresh ⬇️🔄 ⭐⭐
Let the user **pull down** the list to refresh — like most apps.
*Hint:* look up **`PullToRefreshBox`** in Material 3 (it needs `@OptIn(ExperimentalMaterial3Api::class)`). Give it `isRefreshing` and `onRefresh`.

### Challenge 3: A "Dad" category 👨 ⭐
The API also has the type `"dad"`. Add it. How many jokes come back? (Only a few!) What did you have to change? (Hint: just **one line**. 😎)

### Challenge 4: Show the error to the developer 🔍 ⭐
In each `catch`, also write the real error into Logcat: `Log.e("JokesViewModel", "Loading failed", e)`. Turn on airplane mode and find the full error in **Logcat** (filter: `JokesViewModel`). Users see the friendly text; **you** see the details. 🕵️

### Challenge 5: Your own API 🌍 ⭐⭐⭐
Find another free API without a key (search for "**free public APIs list**"), look at its JSON in your browser, and make a small app for it with the same structure: model → API service → repository → AppContainer → ViewModel → Screen.

---

## 19.24 What Is Next?

Our jokes are just **text**. But most apps show **pictures** from the internet: profile photos, products, posts… 📸

In **Chapter 20: Showing Pictures From the Internet**, you will learn:

- Why pictures are **different** from text (big files, slow, memory-hungry 🐘)
- **Coil** — the modern image library for Compose 🖼️
- **`AsyncImage`** — show a picture from a URL in **one** line
- **Placeholders** ⏳ and **error images** ❌ while loading or when it fails
- **Caching** — why the second time is instant ⚡
- Cropping, rounding, and sizing pictures nicely ✂️
- Building a **photo gallery** app with a grid of pictures from a free API 🐶📸

**Awesome work finishing Chapter 19! 🎉 Your apps can now talk to the whole world! 🌍**
