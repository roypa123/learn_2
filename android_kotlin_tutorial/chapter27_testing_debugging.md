# Chapter 27: Testing and Debugging — Being a Bug Detective 🧪🔍

> **What you will learn in this chapter**
>
> 1. What a **bug** is, and the two big jobs: **debugging** 🕵️ and **testing** 🤖
> 2. **Logcat** — the app's diary 📔
> 3. **Crashes** and **stack traces** — reading the "crash letter" calmly 💥📜
> 4. The **debugger** — pausing time and looking inside your app ⏸️🔍
> 5. **Unit tests** — small robots that check your code in milliseconds ⚡
> 6. Testing **real code** from our apps: `formatTime`, `breedNameFromUrl`, `sortedFor` ✅
> 7. Testing **coroutines** and **Flows** with `runTest` and **virtual time** ⏱️
> 8. Testing **ViewModels** with **fake repositories** — the promise from Chapter 16! 🎭
> 9. **Compose UI tests** — a robot that taps your buttons 🤖👆
> 10. A peek at **big tests with Hilt** (`@TestInstallIn`) 🔭
> 11. The **most common crashes** and how to fix them 💥🔧
>
> **Time needed:** about 5–6 hours. Take breaks! ☕
>
> **What you need to know:** Chapters 1–26, especially 15 (ViewModel), 16 (repositories), 18 (coroutines and Flow), 23 (Hilt), and 24 (Notes app).

---

## 27.1 Bugs Happen to Everyone 🐛

A **bug** is a mistake in a program: the app does something you **didn't** want. It shows the wrong number, a button does nothing, or the app **crashes** (closes suddenly). 💥

> 📜 **A true story:** in 1947, engineers working on a giant computer (the Harvard Mark II) found a real **moth** 🦋 stuck inside it, causing problems. They taped it into their notebook with the words *"First actual case of bug being found."* Since then, finding and fixing mistakes is called **debugging**.

**Every** programmer writes bugs — beginners **and** experts with 20 years of experience. The difference is that experts are good at **finding** them quickly. That's what this chapter teaches. 💪

### Two jobs 🕵️🤖

| Job | Question | Tools | Like… |
|---|---|---|---|
| **Debugging** 🕵️ | "Something is wrong. **Why?**" | Logcat, stack traces, the debugger | A **detective** looking for clues |
| **Testing** 🤖 | "Does it work? Will it **still** work tomorrow?" | Unit tests, UI tests | A **robot** that checks everything, again and again |

The first half of this chapter is the **detective** part. The second half builds the **robots**. Let's go! 🚀

> 🛠️ The small examples go in **MyFirstApp**: put the Composable in `setContent { MyFirstAppTheme { ... } }` and run, like in the earlier chapters.

---

## 27.2 Logcat — The App's Diary 📔

You met **Logcat** briefly in earlier chapters. Now let's really learn it.

**Logcat** is a window in Android Studio that shows **messages** from the phone: from Android itself, from libraries, and from **your** app. It's like a **diary** 📔 the app writes while it runs.

You can write in this diary yourself with the **`Log`** class:

```kotlin
import android.util.Log

Log.d("MyTag", "Hello from my app! 👋")
```

| Part | Meaning |
|---|---|
| `Log` | Android's diary-writing class. |
| `.d` | The **level** — how important the message is (table below). |
| `"MyTag"` | A **tag** — a short label, so you can **find** your messages among thousands. 🏷️ |
| `"Hello…"` | The message itself. |

### The five levels 🎚️

| Function | Level | Use it for | Color in Logcat |
|---|---|---|---|
| `Log.v(...)` | **V**erbose | Tiny details (rarely used) | gray |
| `Log.d(...)` | **D**ebug | "I'm here, and x = 5" — messages for **you** while building | blue |
| `Log.i(...)` | **I**nfo | Normal important events: "User logged in" | green |
| `Log.w(...)` | **W**arning | "Something is strange, but I can continue" | yellow/orange |
| `Log.e(...)` | **E**rror | "Something went wrong!" | red |

> 💡 The level is **your** choice. It helps you **filter**: when things go badly, you can show only warnings and errors.

### A small example: the click diary 🖱️

```kotlin
import android.util.Log
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

private const val TAG = "ClickDiary"                                   // (1)

@Composable
fun ClickDiary() {
    var clicks by remember { mutableIntStateOf(0) }

    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("Clicks: $clicks")
        Button(onClick = {
            clicks++
            Log.d(TAG, "Button clicked. clicks = $clicks")             // (2)
            if (clicks == 5) {
                Log.w(TAG, "Wow, 5 clicks! Is everything OK? 🤔")      // (3)
            }
            if (clicks > 10) {
                Log.e(TAG, "Too many clicks! clicks = $clicks 😱")     // (4)
            }
        }) {
            Text("Click me")
        }
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `private const val TAG = "ClickDiary"` | One **constant** for the tag (Chapter 20). Then all messages from this file have the **same** tag, and you can't make a typo. ✅ Tags should be **short** (Android may cut very long ones). |
| 2 | `Log.d(TAG, "... $clicks")` | A **debug** message with the current value inside (string templates, Chapter 2). |
| 3 | `Log.w(...)` | A **warning** at exactly 5 clicks. |
| 4 | `Log.e(...)` | An **error** message after 10 clicks. (Nothing really breaks — it's just practice. 😉) |

**Run it** ▶️ and click the button 12 times. Now open Logcat: **View → Tool Windows → Logcat** (or the **Logcat** tab at the bottom of Android Studio).

You'll see **many** lines — Android talks a lot! 🗣️ Let's find **ours**.

### Filtering — finding your needle in the haystack 🪡

At the top of the Logcat window there's a **filter box**. Type special words into it:

| Filter | Shows |
|---|---|
| `package:mine` | Only messages from **your** app (this is usually there by default ✅) |
| `tag:ClickDiary` | Only messages with **this tag** |
| `level:warn` | Only warnings **and** more important (warn + error) |
| `is:crash` | Only **crashes** 💥 |
| `ClickDiary` | Any line that **contains** this text |
| `package:mine level:error` | Combine filters with a space: your app **and** errors only |

Try `package:mine tag:ClickDiary`. Now you see only your 12 click messages — blue for debug, then the yellow warning at 5, then red errors after 10. 🎉

```
D  Button clicked. clicks = 4
D  Button clicked. clicks = 5
W  Wow, 5 clicks! Is everything OK? 🤔
D  Button clicked. clicks = 6
...
D  Button clicked. clicks = 11
E  Too many clicks! clicks = 11 😱
```

> 💡 **More Logcat tricks:**
> - The 🗑️ **Clear** button at the side empties the window — great before you try something, so you see only **new** messages.
> - Logcat **keeps** working when the app crashes — that's where you'll find the crash letter (next section).
> - `println("...")` also appears in Logcat, with the tag `System.out`. It works, but `Log` with a tag is **much** easier to filter. Use `Log`. 👍

### Logging rules 📏

| Rule | Why |
|---|---|
| **Never** log passwords, tokens, or private user data 🔐 | Logs can be read with a cable, and some tools collect them. |
| Use **one tag per file** (or per feature) | Easy filtering. |
| Remove "I am here!!!" messages when you've found the bug 🧹 | A diary full of noise helps nobody. Chapter 28 also shows how to make a clean release. |

---

## 27.3 Crashes and Stack Traces — The Crash Letter 💥📜

When an app crashes, the user sees the app **close** (sometimes with a message like *"MyFirstApp keeps stopping"*). 😢 But **you**, the developer, get a gift 🎁: a **letter** in Logcat that says **what** went wrong and **where**. This letter is called a **stack trace**.

Many beginners see the big red wall of text and panic. 😱 Don't! Once you know **where to look**, it's usually just **three lines** that matter.

### Let's crash on purpose: the Crash Lab 🧪💥

```kotlin
import android.util.Log
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

private const val TAG = "CrashLab"

@Composable
fun CrashLab() {
    val numbers = listOf(10, 20, 30)                                     // (1)
    val nickname by remember { mutableStateOf<String?>(null) }           // (2)

    Column(
        modifier = Modifier.fillMaxSize().padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("💥 Crash Lab", style = MaterialTheme.typography.headlineMedium)

        Button(onClick = {
            Log.d(TAG, "Turning \"abc\" into a number…")
            val age = "abc".toInt()                                      // (3)
            Log.d(TAG, "Age is $age")
        }) { Text("1. Bad number") }

        Button(onClick = {
            Log.d(TAG, "Item: ${numbers[5]}")                            // (4)
        }) { Text("2. Wrong index") }

        Button(onClick = {
            Log.d(TAG, "Nickname length: ${nickname!!.length}")          // (5)
        }) { Text("3. Null with !!") }

        Button(onClick = {
            error("The oven is not hot yet 🔥")                          // (6)
        }) { Text("4. My own error") }
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `listOf(10, 20, 30)` | A list with **3** items — positions **0, 1, 2** (Chapter 3). |
| 2 | `mutableStateOf<String?>(null)` | A nickname the user **never typed** — it's `null`. |
| 3 | `"abc".toInt()` | Turn text into a number… but "abc" is **not** a number! 💥 (Chapter 2 warned us: use `toIntOrNull()` for user input.) |
| 4 | `numbers[5]` | Ask for position **5** in a list with only 0–2. 💥 |
| 5 | `nickname!!` | `!!` means "*I promise this is not null!*" (Chapter 3). We **broke** the promise. 💥 |
| 6 | `error("...")` | A Kotlin function that **crashes on purpose** with your message. Useful for "this should **never** happen" places. |

**Run it** ▶️, clear Logcat 🗑️, and tap **"1. Bad number"**. The app closes. 💥 Now look at Logcat (try the filter `is:crash`):

```
FATAL EXCEPTION: main                                                   ← (A)
Process: com.example.myfirstapp, PID: 14523
java.lang.NumberFormatException: For input string: "abc"                ← (B)
    at java.lang.Integer.parseInt(Integer.java:797)
    at java.lang.Integer.parseInt(Integer.java:915)
    at com.example.myfirstapp.CrashLabKt.CrashLab$lambda$3$lambda$2(CrashLab.kt:35)   ← (C)
    at androidx.compose.foundation.ClickableNode$clickPointerInput$3.invoke(Clickable.kt:639)
    at androidx.compose.foundation.gestures.TapGestureDetectorKt$detectTapAndPress$2$1.invokeSuspend(...)
    ... (many more lines) ...
    at android.os.Looper.loop(Looper.java:288)
    at android.app.ActivityThread.main(ActivityThread.java:7872)
```

> 📝 Your numbers (PID, line numbers, lambda names) will be **different**. That's normal.

### How to read it — the three important lines 👀

| Line | What it tells you |
|---|---|
| **(A)** `FATAL EXCEPTION: main` | "The app **crashed** 💀 on the **main** thread." (`FATAL` = deadly.) |
| **(B)** `java.lang.NumberFormatException: For input string: "abc"` | **WHAT** happened: the **type** of problem (before the `:`) and a **message** (after it). This is the most important line! |
| **(C)** The **first** line with **your package** (`com.example.myfirstapp`) | **WHERE** it happened in **your** code: file `CrashLab.kt`, line **35**. |

The lines **under** (C) are the "path" that led there — Compose's click handling, then Android's main loop. They're **Android's** code, not yours. You can usually **ignore** them. 🙈

> 🖱️ **The magic trick:** in Logcat, `CrashLab.kt:35` is a **blue link**. **Click it** → Android Studio jumps **straight** to the guilty line! 🎯

### Why is it called a "stack" trace? 📚

Think of a **stack of plates**. 🍽️ Each time a function calls another function, a new plate goes **on top**. The trace lists the plates from **top** (where the crash happened) to **bottom** (where everything started: `ActivityThread.main`, the very first function of every Android app).

```
  Integer.parseInt          ← top: the crash happened here 💥
  CrashLab (your click)     ← your code called it
  Compose click handling    ← Compose called your click
  ...
  ActivityThread.main       ← bottom: where the app started
```

So you read **from the top**, and stop at the **first line that is yours**. That's where you can fix something.

### Try the other buttons 🔬

Run again and tap each button. Here's what you'll see (line (B)):

| Button | Line (B) | In simple words | The fix |
|---|---|---|---|
| 1 | `NumberFormatException: For input string: "abc"` | "This text is not a number." | `toIntOrNull()` and handle `null` (Chapter 9) |
| 2 | `ArrayIndexOutOfBoundsException: length=3; index=5` | "You asked for item 5, but there are only 3." | Check the size, or use `getOrNull(5)` (Chapter 3) |
| 3 | `NullPointerException` | "Something was `null`, and you used it anyway." | Don't use `!!` — use `?.`, `?:`, or `if (x != null)` (Chapter 3) |
| 4 | `IllegalStateException: The oven is not hot yet 🔥` | Your **own** message! | — (you did it on purpose 😄) |

### "Caused by" — a crash inside a crash 🪆

Sometimes the stack trace has **several** parts, like this:

```
java.lang.RuntimeException: Unable to start activity ComponentInfo{...MainActivity}
    at android.app.ActivityThread.performLaunchActivity(...)
    ...
Caused by: java.lang.IllegalStateException: Room cannot verify the data integrity...
    at androidx.room.RoomOpenHelper.checkIdentity(...)
    ...
    at com.example.notes.data.RoomNotesRepository...(RoomNotesRepository.kt:31)
```

Like Russian dolls 🪆: the **outer** error says "*I couldn't start the screen*", but the **real** reason is **inside**. **Rule:** scroll down to the **last** `Caused by:` — that's the **root** problem. (This one is Chapter 22's "you changed the database but forgot the version/migration". 😉)

### The detective's 5 steps 🕵️‍♀️

When your app crashes:

1. **Don't panic.** 😌 A crash is information, not a disaster.
2. Open Logcat, filter with **`is:crash`** (or `level:error`).
3. Find the **last `Caused by:`** (if there is one) and read **WHAT**: the exception type + message.
4. Find the **first line with your package** → click the blue link → **WHERE**.
5. Think: "*What value was different from what I expected?*" If you don't know → use the **debugger** (next section!) or add a `Log.d` before that line.

> 💡 **Copy the message into a search engine.** Exception messages like `"Cannot access database on the main thread"` are shared by millions of developers. Someone has almost certainly asked about it before. 🌍 Leave out **your** names (package, file) and search for the **Android** part.

---

## 27.4 The Debugger — Pausing Time ⏸️🔍

`Log.d` is great, but you must guess **beforehand** what to print, then run again, and again… 🔁 The **debugger** is a superpower: it **freezes** your app at any line you choose, and lets you look at **every** variable — and then move forward **one line at a time**. ⏸️ ▶️

### A bug to catch 🐛

Create a new file **`ScoreMath.kt`** in MyFirstApp (right-click the `com.example.myfirstapp` package → **New → Kotlin Class/File → File**):

```kotlin
package com.example.myfirstapp

fun averageScore(scores: List<Int>): Double {
    val total = scores.sum()                                  // (1)
    val average = total / scores.size                         // (2)
    return average.toDouble()                                 // (3)
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `scores.sum()` | Add all scores together. |
| 2 | `total / scores.size` | Divide by how many there are — the **average**. |
| 3 | `.toDouble()` | Turn the result into a `Double` (a number with decimals). |

And a small screen to show it:

```kotlin
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun ScoreBoard() {
    val scores = listOf(2, 3)
    Column(modifier = Modifier.padding(24.dp)) {
        Text("Scores: ${scores.joinToString()}")
        Text(
            text = "Average: ${averageScore(scores)}",
            style = MaterialTheme.typography.headlineSmall
        )
    }
}
```

**Run it** ▶️. The screen says:

```
Scores: 2, 3
Average: 2.0
```

Hmm. 🤔 (2 + 3) ÷ 2 = **2.5**, not 2.0! There's a bug. Maybe you can already see it — but let's **pretend** we can't, and use the debugger like a pro. 🕵️

### Step 1: Set a breakpoint 🔴

A **breakpoint** is a **stop sign** 🛑 for the app: "*When you reach this line, freeze!*"

Open `ScoreMath.kt` and **click in the gray area** just to the right of the line number of `val total = scores.sum()`. A **red dot** 🔴 appears. That's your breakpoint! (Click it again to remove it.)

### Step 2: Run in debug mode 🐞

Don't use the normal ▶️ Run button. Use the **Debug** button — the green **bug** icon 🐞 next to it (or **Run → Debug 'app'**, or **Shift + F9** on Windows).

The app starts (maybe a little slower) and… **freezes**! ⏸️ The line with the red dot is highlighted in **blue**, and the **Debug** window opens at the bottom.

> 📝 The app **stops before** running the highlighted line. The blue line is "**the next line to run**".

### Step 3: Look around 👀

The Debug window has two important parts:

| Part | What it shows |
|---|---|
| **Frames** (left) | The **stack** — the same "pile of plates" as a stack trace! The top is where you are now (`averageScore`), under it is who called it (`ScoreBoard`). Click a frame to look at **its** variables. |
| **Variables** (right) | **Every** variable that exists right now, with its **value**. You'll see something like `scores = {Arrays$ArrayList@...} size = 2` — click the ▸ arrow to open it: `0 = 2`, `1 = 3`. ✅ |

> 💡 You can also simply **hover the mouse** over a variable in the code — a small box shows its value. 🖱️

### Step 4: Step through the code 👣

Now move forward **one line at a time**. These are the buttons at the top of the Debug window (the keys are for **Windows**; on a Mac they're different, so use the buttons):

| Button | Key | What it does |
|---|---|---|
| **Step Over** ⤵️ | **F8** | Run this line, go to the **next** one. (If the line calls a function, run the whole function **without** going inside.) |
| **Step Into** ⬇️ | **F7** | If this line calls a function, go **inside** it. |
| **Step Out** ⬆️ | **Shift + F8** | Finish the current function and go back to the one that called it. |
| **Resume** ▶️ | **F9** | Continue running normally until the **next** breakpoint (or forever). |
| **Evaluate Expression** 🧮 | **Alt + F8** | Type **any** Kotlin expression and see its value **right now**. |

Press **F8** (Step Over). The line `val total = scores.sum()` runs. In Variables, a new one appears: **`total = 5`**. ✅ Correct.

Press **F8** again. `val average = total / scores.size` runs. In Variables: **`average = 2`**. ❌ **There!** We expected 2.5!

Why? 🤔 `total` is an `Int` (5), `scores.size` is an `Int` (2). **`Int / Int` gives an `Int`** — the `.5` is thrown away (Chapter 2: "integer division drops the rest")! Then `.toDouble()` on line 3 turns 2 into 2.0 — **too late**, the `.5` is already gone. 🥲

Try **Evaluate Expression** (Alt + F8): type `total.toDouble() / scores.size` → **2.5**. 🎉 That's the fix!

Press **F9** (Resume) to let the app continue. Then stop the app (the red ■ square).

### Step 5: Fix it 🔧

```kotlin
fun averageScore(scores: List<Int>): Double {
    val total = scores.sum()
    return total.toDouble() / scores.size                     // 👈 Double / Int = Double ✅
}
```

Run again → **"Average: 2.5"** 🎉. Bug caught! 🐛🔨

### More breakpoint superpowers 🦸

**Right-click** a red dot to open its settings:

| Setting | What it does | When it's useful |
|---|---|---|
| **Condition** | Only stop if this is **true**, for example `score > 100` | A loop that runs 1000 times, but the problem is only at one item. 🎯 |
| **Suspend** (uncheck) + **Evaluate and log** | **Don't** stop — just **print** something to the Debug console | Like a `Log.d` — but **without** changing your code and running again! 📝 (This is called a **logpoint**.) |
| **Disable** | Keep the dot, but ignore it for now (it turns into an empty circle ⭕) | You may need it again later. |

To see **all** breakpoints: **Run → View Breakpoints…** (Ctrl + Shift + F8). Remove the ones you don't need anymore — forgotten breakpoints can surprise you later! 😅

### The app is already running? Attach! 🔗

Sometimes a bug appears **after** you started the app normally with ▶️, and you don't want to restart (the bug might be hard to repeat). No problem:

**Run → Attach Debugger to Android Process** → choose your app → **OK**. Now your breakpoints work, without restarting! 🪄

### Debugging Compose and coroutines 🧩

- Breakpoints work **inside** `onClick = { ... }` lambdas, inside `viewModelScope.launch { ... }`, and inside `suspend` functions. ✅
- A breakpoint **directly** inside a Composable function stops **every time** it recomposes — which can be very often (and it's even more often during animations). Put breakpoints in **event lambdas** and **ViewModel functions** instead. 💡
- Paused at a breakpoint, the app is **frozen** — if you wait too long, Android may show *"App isn't responding"* (ANR). Just click **Wait**. ⏳

---

## 27.5 More Detective Tools 🧰

Android Studio has a whole **detective kit**. You've already met some of these:

| Tool | Where | What it shows | Chapter |
|---|---|---|---|
| **Logcat** 📔 | View → Tool Windows → Logcat | Messages and crashes | 27 |
| **Debugger** 🐞 | Debug button | Pause, look inside, step | 27 |
| **Layout Inspector** 🔬 | View → Tool Windows → Layout Inspector | The **Compose tree** of the running app: every Composable, its size, its parameters, and **how many times it recomposed** | 26 (performance) |
| **Database Inspector** 🗄️ | View → Tool Windows → **App Inspection** → Database Inspector | The **live** Room database — you can even run SQL | 22 |
| **Background Task Inspector** ⚙️ | App Inspection → Background Task Inspector | WorkManager jobs | 25 |
| **Network Inspector** 🌐 | App Inspection → Network Inspector | Every internet request and its answer (works with OkHttp/Retrofit) | 19 |
| **Profiler** 📈 | View → Tool Windows → Profiler | CPU, memory, and energy use over time — for "it's **slow**" bugs | — |

> 🎯 **Which tool when?**
> - The app **crashes** → Logcat (stack trace).
> - The app shows a **wrong value** → the debugger.
> - The screen **looks** wrong (sizes, padding, something missing) → Layout Inspector.
> - The **data** is wrong → Database Inspector / Network Inspector.
> - The app is **slow** → Layout Inspector (recompositions) and Profiler.

---

## 27.6 Why Write Tests? 🤖✅

Every time you change your app, you should check that **everything** still works. Tap every button, try every screen, rotate, type wrong things… 😩 With 5 screens, that's 20 minutes. With 50 screens? Impossible. And one day you **forget** to check something — and the bug goes to your users. 🐛📱

A **test** is a small piece of code that **checks** other code **automatically**:

```
"Robot, check that averageScore(listOf(2, 3)) gives 2.5."
🤖 ... ✅ Yes!
```

You write it **once**, and the robot checks it **forever** — in **milliseconds**, as often as you want. 🔁

### What tests give you 🎁

| Gift | Meaning |
|---|---|
| **Safety net** 🕸️ | Change code without fear: if you break something, a test turns **red** immediately. |
| **Fast checking** ⚡ | Hundreds of checks in a few seconds. |
| **Living notes** 📝 | A test like `formatTime_oneHour_showsSixtyMinutes` **explains** how the code behaves. |
| **Better design** 🏗️ | Code that's easy to test is usually **well organized**: small functions, interfaces, ViewModels. (Everything we did in Chapters 15–23 makes testing easy now! 🎉) |

### Two kinds of tests 🧪📱

| | **Local unit tests** | **Instrumented tests** |
|---|---|---|
| Folder | `app/src/test/` | `app/src/androidTest/` |
| Runs on | **Your computer** (in the JVM — Java's engine) | A **phone or emulator** 📱 |
| Speed | ⚡ Very fast (milliseconds) | 🐢 Slower (seconds — it must install the app) |
| Can use Android things (`Context`, screens)? | ❌ No | ✅ Yes |
| Good for | Functions, ViewModels, repositories with fakes | **UI tests** (Compose), databases, the whole app |

Every new project already has **both** folders, with one example test in each. In the **Android** view of the Project window, look for the packages marked **`(test)`** and **`(androidTest)`**:

```
app
 └── kotlin+java
      ├── com.example.myfirstapp                 ← your app code (main)
      ├── com.example.myfirstapp (androidTest)   ← tests on a phone 📱
      │    └── ExampleInstrumentedTest
      └── com.example.myfirstapp (test)          ← tests on your computer 💻
           └── ExampleUnitTest
```

### The testing pyramid 🔺

```
          /\
         /UI\          ← few: slow, but test what the user sees 📱
        /----\
       / Inte-\        ← some: several pieces together
      / gration\
     /----------\
    / Unit tests \     ← MANY: fast, small, precise ⚡
   /--------------\
```

Write **many** small, fast unit tests, **some** bigger ones, and a **few** UI tests. Like a pyramid: a wide, strong base. 💪

---

## 27.7 Your First Unit Test 🧪

Open **`ExampleUnitTest`** in the **`(test)`** package of MyFirstApp. Android Studio wrote it for you:

```kotlin
package com.example.myfirstapp

import org.junit.Test                                          // (1)

import org.junit.Assert.*                                      // (2)

/**
 * Example local unit test, which will execute on the development machine (host).
 *
 * See [testing documentation](http://d.android.com/tools/testing).
 */
class ExampleUnitTest {                                        // (3)
    @Test                                                      // (4)
    fun addition_isCorrect() {                                 // (5)
        assertEquals(4, 2 + 2)                                 // (6)
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `import org.junit.Test` | **JUnit** is the most famous testing library for Java and Kotlin. Every new project already includes it (`testImplementation(libs.junit)` in `build.gradle.kts`). ✅ |
| 2 | `import org.junit.Assert.*` | Imports **all** the "check" functions (`assertEquals`, `assertTrue`, …). The `*` means "everything". |
| 3 | `class ExampleUnitTest` | A test class — just a normal class holding tests. |
| 4 | `@Test` | The magic label: "**This function is a test.** Robot, run it!" 🏷️ Without it, the function is ignored. |
| 5 | `fun addition_isCorrect()` | The test's **name**. It should say **what** is checked. |
| 6 | `assertEquals(4, 2 + 2)` | "**I expect** 4. **Check** that `2 + 2` really is 4." If yes → ✅ pass. If not → ❌ fail. ⚠️ The order is **(expected, actual)** — what you **want** first, what the code **gives** second. |

### Run it ▶️

See the small green **▶** arrows in the gray area next to `class ExampleUnitTest` and `fun addition_isCorrect`? Click the one next to the **class** → **Run 'ExampleUnitTest'**.

A few seconds later (the first time is slower, it must build), the **Run** window shows:

```
✅ ExampleUnitTest
   ✅ addition_isCorrect          2 ms
Tests passed: 1 of 1 test
```

🎉 Your first passing test! Notice: **no emulator** started. It ran on your computer, in **2 milliseconds**. ⚡

### Make it fail on purpose ❌

Change the line to `assertEquals(5, 2 + 2)` and run again:

```
❌ addition_isCorrect
java.lang.AssertionError:
Expected :5
Actual   :4
```

Very clear: "**You expected 5, but the code gave 4.**" A failing test **always** tells you the **expected** and the **actual** value. That's why the order (expected, actual) matters — swap them, and the message lies to you! 🤥

Change it back to `4`. ✅

### Testing our `averageScore` 🧮

Now a **real** test. Right-click the **`com.example.myfirstapp (test)`** package → **New → Kotlin Class/File** → **Class** → name it **`ScoreMathTest`**:

```kotlin
package com.example.myfirstapp

import org.junit.Assert.assertEquals
import org.junit.Test

class ScoreMathTest {

    @Test
    fun averageScore_twoAndThree_isTwoPointFive() {
        // Arrange — prepare the inputs                         (1)
        val scores = listOf(2, 3)

        // Act — call the code we are testing                   (2)
        val result = averageScore(scores)

        // Assert — check the result                            (3)
        assertEquals(2.5, result, 0.0001)                       // (4)
    }

    @Test
    fun averageScore_oneScore_isThatScore() {
        assertEquals(7.0, averageScore(listOf(7)), 0.0001)     // (5)
    }

    @Test
    fun averageScore_emptyList_isZero() {
        assertEquals(0.0, averageScore(emptyList()), 0.0001)   // (6)
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | **Arrange** | Get everything ready: the input values. |
| 2 | **Act** | Do **one** thing: call the function. |
| 3 | **Assert** | Check the answer. These three steps — **Arrange, Act, Assert** (the "**AAA**" pattern 🅰️🅰️🅰️) — make every test easy to read. |
| 4 | `assertEquals(2.5, result, 0.0001)` | For `Double`s there's a **third** value: the **tolerance**. Computers store decimals **almost** exactly (`0.1 + 0.2` is `0.30000000000000004`! 😮). So we say: "*Equal if they differ by less than 0.0001.*" |
| 5 | Short version | For simple tests, Arrange/Act/Assert can fit in **one** line. |
| 6 | `emptyList()` | What if there are **no** scores yet? We decide: the average should be **0.0**. |

**Test names** follow a simple pattern: **`whatIsTested_situation_expectedResult`**. When a test fails, its name alone tells you what broke. 📛

> 💡 In local unit tests you can also use **backticks** for names with spaces: ``fun `average of 2 and 3 is 2,5`()``. It reads nicely — but it does **not** work in `androidTest` on older phones, so in this book we use the underscore style everywhere.

**Run `ScoreMathTest`** ▶️:

```
✅ averageScore_twoAndThree_isTwoPointFive
✅ averageScore_oneScore_isThatScore
❌ averageScore_emptyList_isZero
   Expected :0.0
   Actual   :NaN
```

😮 The test found a bug we **didn't** see with the debugger! For an empty list, the code calculates `0.0 / 0` → **`NaN`** ("**N**ot **a** **N**umber"). The screen would show *"Average: NaN"*. 🙈

> 🧠 **Think:** if you had tested the **old** buggy version (Int division), the first test would have failed with *Expected 2.5, Actual 2.0* — **without** even opening the app. That's the power of tests. ⚡

Fix `averageScore`:

```kotlin
fun averageScore(scores: List<Int>): Double {
    if (scores.isEmpty()) return 0.0                          // 👈 the empty case
    return scores.sum().toDouble() / scores.size
}
```

Run the tests again → **all green** ✅✅✅. 🎉

> 🎯 **Test the edges!** Bugs love to hide at the **edges**: an **empty** list, **zero**, **one** item, the **last** item, a **very big** number, text with **spaces**. When you write tests, always ask: "*What's the weirdest input this could get?*" 🧱

### The check functions 🧰

All from `org.junit.Assert`:

| Function | Passes when… | Example |
|---|---|---|
| `assertEquals(expected, actual)` | the two are **equal** | `assertEquals("Pug", name)` |
| `assertEquals(expected, actual, delta)` | two `Double`s are **close enough** | `assertEquals(2.5, avg, 0.0001)` |
| `assertNotEquals(a, b)` | they are **different** | `assertNotEquals(0, list.size)` |
| `assertTrue(condition)` | the condition is `true` | `assertTrue(state.isLoading)` |
| `assertFalse(condition)` | the condition is `false` | `assertFalse(state.canReset)` |
| `assertNull(value)` | the value is `null` | `assertNull(state.recentlyDeleted)` |
| `assertNotNull(value)` | the value is **not** `null` | `assertNotNull(repo.getNote(1))` |
| `assertThrows(Type::class.java) { ... }` | the code inside **crashes** with that exception | `assertThrows(NumberFormatException::class.java) { "abc".toInt() }` |

> 💡 Every function can also take a **message** as the **first** value, shown when it fails: `assertEquals("Pizza should be first", "Pizza", list.first())`.

### Running many tests at once 🏃‍♀️🏃‍♂️🏃

| How | Runs |
|---|---|
| ▶ next to a `fun` | That **one** test |
| ▶ next to a `class` | All tests in that class |
| Right-click the **`(test)`** package → **Run 'Tests in …'** | **All** local unit tests |
| In the **Terminal** tab: `.\gradlew test` | All unit tests, without the buttons (a report is saved in `app/build/reports/tests/`) |

> 💡 After a test run, the **Run** window has a 🔁 **Rerun Failed Tests** button — very handy while you fix bugs.

---

## 27.8 Testing Real Code from Our Apps ✅

Now let's test the functions we **promised** to test in earlier chapters. Each one is a normal, **top-level** function with no Android in it — the **easiest** kind of code to test. 🍰

### 1. `formatTime` — Background Lab (Chapter 18) ⏱️

Open the **Background Lab** project. In the **`com.example.backgroundlab (test)`** package, create **`FormatTimeTest`**:

```kotlin
package com.example.backgroundlab

import com.example.backgroundlab.ui.stopwatch.formatTime              // (1)
import org.junit.Assert.assertEquals
import org.junit.Test

class FormatTimeTest {

    @Test
    fun formatTime_zero_isAllZeros() {
        assertEquals("00:00.00", formatTime(0L))
    }

    @Test
    fun formatTime_exampleFromChapter18() {
        assertEquals("01:23.45", formatTime(83_456L))                 // (2)
    }

    @Test
    fun formatTime_justBeforeOneMinute() {
        assertEquals("00:59.99", formatTime(59_999L))                 // (3)
    }

    @Test
    fun formatTime_exactlyOneMinute() {
        assertEquals("01:00.00", formatTime(60_000L))
    }

    @Test
    fun formatTime_oneHour_showsSixtyMinutes() {
        assertEquals("60:00.00", formatTime(3_600_000L))              // (4)
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `import ...ui.stopwatch.formatTime` | The test lives in a **different** package, so we import the function. (If you put the test in the **same** package, no import is needed — both ways are fine.) |
| 2 | `83_456L` → `"01:23.45"` | The exact example we calculated **by hand** in Chapter 18. Now a robot checks it **forever**. 🤖 |
| 3 | `59_999L` → `"00:59.99"` | An **edge**: one millisecond before a full minute. |
| 4 | `3_600_000L` → `"60:00.00"` | One **hour**. Our stopwatch has no hours, so it shows **60 minutes**. Is that a bug? 🤔 Not really — it's a **decision**. This test **documents** it: if someone adds hours one day, the test reminds them to update it. 📝 |

Run ▶️ → **5 green checks**. ✅

### 2. `breedNameFromUrl` — Dog Gallery (Chapter 20) 🐶

Open **Dog Gallery**. In **`com.example.doggallery (test)`**, create **`BreedNameTest`**:

```kotlin
package com.example.doggallery

import com.example.doggallery.data.breedNameFromUrl
import org.junit.Assert.assertEquals
import org.junit.Test

class BreedNameTest {

    @Test
    fun breedName_twoWords_areReversedAndCapitalized() {
        val url = "https://images.dog.ceo/breeds/retriever-golden/n02099601_100.jpg"
        assertEquals("Golden Retriever", breedNameFromUrl(url))
    }

    @Test
    fun breedName_oneWord_isCapitalized() {
        val url = "https://images.dog.ceo/breeds/pug/n02110958_1975.jpg"
        assertEquals("Pug", breedNameFromUrl(url))
    }

    @Test
    fun breedName_notADogUrl_isUnknown() {
        val url = "https://example.com/cat.jpg"                         // (1)
        assertEquals("Unknown breed", breedNameFromUrl(url))
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | A URL **without** `/breeds/` | An **edge**: what if the API sends something strange one day? We **decide** the answer should be `"Unknown breed"`. |

Run ▶️:

```
✅ breedName_twoWords_areReversedAndCapitalized
✅ breedName_oneWord_isCapitalized
❌ breedName_notADogUrl_isUnknown
   Expected :Unknown breed
   Actual   :Https:
```

😂 **"Https:"**! Let's see why. `substringAfter("/breeds/")` can't find `/breeds/`, so it returns the **whole** text. `substringBefore("/")` then cuts at the first `/` → `"https:"`. Capitalized → `"Https:"`. A strange dog breed! 🐕‍🦺

Fix it in `data/NetworkDogPhotosRepository.kt` (the file where `breedNameFromUrl` lives):

```kotlin
fun breedNameFromUrl(url: String): String {
    if (!url.contains("/breeds/")) return "Unknown breed"                 // 👈 new
    val folder = url.substringAfter("/breeds/").substringBefore("/")
    return folder
        .split("-")
        .reversed()
        .joinToString(" ") { word -> word.replaceFirstChar { it.uppercase() } }
}
```

Run again → **all green** ✅✅✅.

### Red ➡️ Green ➡️ Clean 🚦

Look at what we just did:

1. 🔴 **Red** — write a test for what you **want**. Run it. It **fails** (the code doesn't do it yet).
2. 🟢 **Green** — change the code, just enough to make the test **pass**.
3. 🧹 **Clean** — now that the tests protect you, make the code **nicer** if needed — and run the tests again.

Many professional developers **always** work like this. It's called **Test-Driven Development** (**TDD**). You don't have to — but try it sometimes. It feels great to watch red turn green! 🚦😊

### 3. `sortedFor` — the Notes app (Chapter 24) 📝

The Notes app will get **many** tests in this chapter, and many of them need `Note` objects. A `Note` has **8** values — writing all of them in every test would be long and boring. 😴 So first, a **helper**.

In **`com.example.notes (test)`**, create a **file** (not a class) **`TestNotes.kt`**:

```kotlin
package com.example.notes

import com.example.notes.data.model.Note
import com.example.notes.data.model.NoteColor

fun testNote(                                                          // (1)
    id: Long,
    title: String = "Note $id",                                        // (2)
    content: String = "",
    isPinned: Boolean = false,
    createdAt: Long = 0L,
    updatedAt: Long = 0L
): Note = Note(
    id = id,
    title = title,
    content = content,
    color = NoteColor.DEFAULT,
    isPinned = isPinned,
    createdAt = createdAt,
    updatedAt = updatedAt                                              // (3)
)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `fun testNote(...)` | A tiny **factory** for notes — only in the **test** folder, so the real app never sees it. |
| 2 | Default values | Every value except `id` has a default (Chapter 4). A test only writes what **matters** for it: `testNote(1, isPinned = true)`. Short and clear! ✂️ |
| 3 | `photoPath` not given | It has a default (`null`) since Chapter 25. |

Now **`SortedForTest`**:

```kotlin
package com.example.notes

import com.example.notes.data.model.Note
import com.example.notes.data.model.SortOrder
import com.example.notes.data.model.sortedFor
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class SortedForTest {

    @Test
    fun lastEdited_newestEditFirst() {
        val notes = listOf(
            testNote(1, updatedAt = 100),
            testNote(2, updatedAt = 300),
            testNote(3, updatedAt = 200)
        )

        val sorted = notes.sortedFor(SortOrder.LAST_EDITED)

        assertEquals(listOf(2L, 3L, 1L), sorted.map { it.id })               // (1)
    }

    @Test
    fun pinnedNotes_alwaysComeFirst() {
        val notes = listOf(
            testNote(1, updatedAt = 300),
            testNote(2, updatedAt = 100, isPinned = true)                     // (2)
        )

        val sorted = notes.sortedFor(SortOrder.LAST_EDITED)

        assertEquals(listOf(2L, 1L), sorted.map { it.id })
    }

    @Test
    fun dateCreated_newestCreatedFirst() {
        val notes = listOf(
            testNote(1, createdAt = 100, updatedAt = 900),
            testNote(2, createdAt = 200, updatedAt = 100)
        )

        val sorted = notes.sortedFor(SortOrder.DATE_CREATED)

        assertEquals(listOf(2L, 1L), sorted.map { it.id })                   // (3)
    }

    @Test
    fun title_ignoresUpperAndLowerCase() {
        val notes = listOf(
            testNote(1, title = "banana"),
            testNote(2, title = "Cherry"),
            testNote(3, title = "apple")
        )

        val sorted = notes.sortedFor(SortOrder.TITLE)

        assertEquals(listOf("apple", "banana", "Cherry"), sorted.map { it.title })   // (4)
    }

    @Test
    fun emptyList_staysEmpty() {
        val notes = emptyList<Note>()                                         // (5)

        val sorted = notes.sortedFor(SortOrder.TITLE)

        assertTrue(sorted.isEmpty())
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `sorted.map { it.id }` | Compare only the **ids**: `[2, 3, 1]`. If the test fails, the message is **short and readable** — instead of three huge `Note(...)` texts. 👓 (`2L` = a `Long`, because `id` is a `Long`.) |
| 2 | Note 2 is **older** but **pinned** | It must still come **first**. 📌 This test protects our most important sorting rule. |
| 3 | `DATE_CREATED` | Note 1 was **edited** later, but note 2 was **created** later → 2 first. The `updatedAt` values are there to make sure the code really uses `createdAt`. 🕵️ |
| 4 | `"banana"`, `"Cherry"`, `"apple"` | Without `CASE_INSENSITIVE_ORDER`, computers put **all** capital letters first (`"Cherry"` before `"apple"`!). This test proves our sort is **human-friendly**. 🔤 |
| 5 | `emptyList<Note>()` | The edge case: an empty list. No crash, empty result. `<Note>` tells Kotlin **what kind** of empty list (it can't guess from nothing). |

Run ▶️ → **5 green checks**. ✅

> 🧪 **Experiment:** in `Note.kt`, remove `String.CASE_INSENSITIVE_ORDER` from the `TITLE` line, and run the tests. `title_ignoresUpperAndLowerCase` turns **red**. Put it back → green. Now you **know** the tests are really watching! 👀 (A test that **never** fails is worth nothing — it's good to see each test fail **once**.)

---

## 27.9 Testing Coroutines: `runTest` and Virtual Time ⏱️

### A problem: tests can't wait 🐌

Background Lab's `FakeDownloader.download()` (Chapter 18) is a **Flow** with `delay(200L)` × 20 = **4 seconds**. And it's a `suspend`-world thing — you can't call `collect` from a normal test function:

```kotlin
@Test
fun download_works() {
    downloader.download(badInternet = false).toList()   // ❌ red: "Suspend function can only be called from a coroutine"
}
```

Even if we could, should a test **really** wait 4 seconds? With 100 tests like this, you'd wait **7 minutes**. 😴

### The solution: `kotlinx-coroutines-test` 🧰

The coroutines team made a **testing library**. It gives us:

| Tool | What it does |
|---|---|
| **`runTest { ... }`** | Runs `suspend` code inside a test. 🏃 |
| **Virtual time** ⏩ | Inside `runTest`, `delay` **doesn't really wait** — the robot's clock **jumps** forward instead. 4 "seconds" pass in **a few milliseconds**! |
| **Test dispatchers** | Replacements for `Dispatchers.Main` (next section). |

### Add it — `gradle/libs.versions.toml`

Do this in **every** project where you test coroutines (Background Lab, MyFirstApp, Recipe Book, and Notes in this chapter):

```toml
[versions]
kotlinxCoroutinesTest = "1.9.0"

[libraries]
kotlinx-coroutines-test = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-test", version.ref = "kotlinxCoroutinesTest" }
```

### `build.gradle.kts (Module :app)`

```kotlin
dependencies {
    // ... existing lines ...
    testImplementation(libs.kotlinx.coroutines.test)          // 👈 test folder only
}
```

**Sync Now** 🔄

> 💡 **`testImplementation`** means: "*only for the `test` folder*". This library is **not** put inside your real app — users never download it. (For the `androidTest` folder, it would be `androidTestImplementation`.)

### Testing the `FakeDownloader` 📥

In **`com.example.backgroundlab (test)`**, create **`FakeDownloaderTest`**:

```kotlin
package com.example.backgroundlab

import com.example.backgroundlab.data.FakeDownloader
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.toList
import kotlinx.coroutines.test.currentTime
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.IOException

@OptIn(ExperimentalCoroutinesApi::class)                                  // (1)
class FakeDownloaderTest {

    private val downloader = FakeDownloader()                               // (2)

    @Test
    fun download_goodInternet_sendsAllPercentsInOrder() = runTest {        // (3)
        val percents = downloader.download(badInternet = false).toList()    // (4)

        assertEquals((5..100 step 5).toList(), percents)                    // (5)
        assertEquals(4_000L, currentTime)                                   // (6)
    }

    @Test
    fun download_badInternet_stopsAfter55WithError() = runTest {
        val received = mutableListOf<Int>()

        val result = runCatching {                                          // (7)
            downloader.download(badInternet = true).collect { percent ->
                received += percent
            }
        }

        assertTrue(result.exceptionOrNull() is IOException)                 // (8)
        assertEquals(55, received.last())                                   // (9)
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `@OptIn(ExperimentalCoroutinesApi::class)` | Some test tools (like `currentTime`) are still marked "**experimental**" — they work fine, but their name or shape might change in the future. This line says "*I know, I accept.*" (Like `@OptIn` in Chapters 11 and 18.) |
| 2 | `private val downloader = FakeDownloader()` | JUnit creates a **brand-new** test class object for **every** test. So each test gets a **fresh** downloader — tests never disturb each other. 🧼 |
| 3 | `= runTest { ... }` | The test's body is a **coroutine** now. We can call `suspend` functions and collect Flows! The `=` means the function **returns** what `runTest` gives (that's how JUnit knows when the test is finished). |
| 4 | `.toList()` | Collect the **whole** Flow into a `List` (Chapter 18). This is a `suspend` function — it waits until the Flow ends. |
| 5 | `(5..100 step 5).toList()` | The list we **expect**: `[5, 10, 15, … 100]`. |
| 6 | `currentTime` | The **virtual** clock ⏰. 20 delays × 200 ms = **4 000 ms** "passed" — but the test really took only a few **milliseconds**. ⏩ This also **proves** that the timing is right! |
| 7 | `runCatching { ... }` | A Kotlin helper: "**try** this code, and give me the result **or** the error" — instead of crashing the test. It's a short form of `try { ... } catch { ... }` (Chapter 19). |
| 8 | `result.exceptionOrNull() is IOException` | Did it fail with an **IOException**, like we wanted? ✅ |
| 9 | `received.last() == 55` | The last percent **before** the error. At 60%, the downloader threw instead of sending 60. |

Run ▶️ → green ✅✅. Look at the time: both tests together take **milliseconds**, even though they "waited" 6.4 seconds. 🤯

> 🎬 **Virtual time** is like a movie where you can **skip** the boring parts. ⏩ The story (the order of events) is **exactly** the same — the waiting is just skipped.

---

## 27.10 The Main Dispatcher Problem — and `MainDispatcherRule` 🧩

ViewModels use **`viewModelScope`**, and `viewModelScope` runs on **`Dispatchers.Main`** — the phone's **main thread** (Chapter 18). 🧵

But local unit tests run on your **computer**, not a phone. There's **no** Android main thread! 😱 Depending on the library versions, a ViewModel test without preparation either **crashes** with an error like:

```
java.lang.IllegalStateException: Module with the Main dispatcher had failed to initialize.
For tests Dispatchers.setMain from kotlinx-coroutines-test module can be used
```

…or, even worse, **sometimes passes and sometimes fails** (the coroutines run on some random background thread). 🎲

The error message even tells us the solution: **`Dispatchers.setMain`** — "for this test, **replace** the main thread with a **test** dispatcher".

### `MainDispatcherRule.kt` — write it once, use it everywhere 📏

In the **`(test)`** package of **each** project with ViewModel tests, create **`MainDispatcherRule.kt`** (change the `package` line to match the project):

```kotlin
package com.example.myfirstapp

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.TestDispatcher
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.setMain
import org.junit.rules.TestWatcher
import org.junit.runner.Description

@OptIn(ExperimentalCoroutinesApi::class)
class MainDispatcherRule(
    private val testDispatcher: TestDispatcher = UnconfinedTestDispatcher()  // (1)
) : TestWatcher() {                                                           // (2)

    override fun starting(description: Description) {                        // (3)
        Dispatchers.setMain(testDispatcher)
    }

    override fun finished(description: Description) {                        // (4)
        Dispatchers.resetMain()
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `UnconfinedTestDispatcher()` | The **test** dispatcher that will play the role of "Main". (Explained below. 👇) |
| 2 | `: TestWatcher()` | A JUnit **rule** — a helper that does something **before** and **after** every test, automatically. 📏 |
| 3 | `starting(...)` | **Before** each test: "Main is now our test dispatcher." |
| 4 | `finished(...)` | **After** each test: put the normal Main back, so the next test starts clean. 🧹 |

And this is how a test class uses it:

```kotlin
class SomeViewModelTest {

    @get:Rule                                                    // (1)
    val mainDispatcherRule = MainDispatcherRule()

    // ... tests ...
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `@get:Rule` | "JUnit, this property is a **rule** — use it for every test in this class." (`get:` is needed because of how Kotlin properties work inside; just always write it like this. 😉) |

### Two kinds of test dispatchers 🚦

| Dispatcher | How it runs a new coroutine | Like… |
|---|---|---|
| **`UnconfinedTestDispatcher`** | **Immediately**, right where you call `launch` — until the first `delay` or waiting point | A waiter who brings your food **right now** 🏃 |
| **`StandardTestDispatcher`** | Puts it in a **queue**. It runs only when you say "go!" (`advanceUntilIdle()`, `runCurrent()`) | A waiter who writes your order down and waits for the kitchen bell 🔔 |

We use **`UnconfinedTestDispatcher`** for Main: when the test calls `viewModel.onSomething()`, the ViewModel's `launch` runs **right away**, and we can check the result on the **next line**. Simple! 😊 (`runTest` itself uses a `StandardTestDispatcher` — and both share **one** virtual clock ⏰, so `delay`s in the ViewModel are skipped too.)

### Controlling virtual time ⏩

Inside `runTest`, you can move the virtual clock yourself:

| Function | What it does |
|---|---|
| `advanceTimeBy(1_000)` | Move the clock forward 1 000 ms, running everything planned **before** that moment. |
| `advanceUntilIdle()` | Run **everything** that's waiting, until nothing is left. (Skips **all** the waiting.) |
| `runCurrent()` | Run what's waiting **right now**, without moving the clock. |
| `currentTime` | What time is it on the virtual clock? |

---

## 27.11 Testing a ViewModel: Download (Background Lab) 📥

Remember `DownloadViewModel` (Chapter 18)? It has states: Idle → Downloading → Checking → Done, or Failed. Let's test it. Create **`MainDispatcherRule.kt`** in `com.example.backgroundlab (test)` (as above, with `package com.example.backgroundlab`), then **`DownloadViewModelTest`**:

```kotlin
package com.example.backgroundlab

import com.example.backgroundlab.ui.download.DownloadStatus
import com.example.backgroundlab.ui.download.DownloadViewModel
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.advanceTimeBy
import kotlinx.coroutines.test.advanceUntilIdle
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class DownloadViewModelTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    @Test
    fun download_showsProgress_andCancelGoesBackToIdle() = runTest {
        val viewModel = DownloadViewModel()                                     // (1)

        viewModel.onDownloadClick()                                             // (2)
        assertEquals(DownloadStatus.Downloading(percent = 0), viewModel.uiState.value.status)
        assertTrue(viewModel.uiState.value.isBusy)

        advanceTimeBy(1_100)                                                    // (3)
        assertEquals(DownloadStatus.Downloading(percent = 25), viewModel.uiState.value.status)

        viewModel.onCancelClick()                                               // (4)
        assertEquals(DownloadStatus.Idle, viewModel.uiState.value.status)
        assertFalse(viewModel.uiState.value.isBusy)
    }

    @Test
    fun download_badInternet_failsWithMessage() = runTest {
        val viewModel = DownloadViewModel()
        viewModel.onBadInternetChange(true)

        viewModel.onDownloadClick()
        advanceUntilIdle()                                                      // (5)

        assertEquals(
            DownloadStatus.Failed("Connection lost at 60% 📶"),                 // (6)
            viewModel.uiState.value.status
        )
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `val viewModel = DownloadViewModel()` | Just **call the constructor** — a ViewModel is a normal class! 🎉 Create it **inside** the test (after the rule set up Main), never as a property at the top of the class. |
| 2 | `onDownloadClick()` | Thanks to `UnconfinedTestDispatcher`, the `launch` starts **immediately**: status → `Downloading(0)`, then it reaches the first `delay(200)` and waits. |
| 3 | `advanceTimeBy(1_100)` | ⏩ Jump 1.1 virtual seconds. Delays finished at 200, 400, 600, 800, 1000 ms → **5** steps → **25%**. (Why 1 100 and not 1 000? `advanceTimeBy` runs what's planned **before** the new time — something planned at **exactly** 1 000 waits for the next nudge. A little extra makes it clear. 😉) |
| 4 | `onCancelClick()` | Cancel → `Idle`. And the download coroutine is really stopped — nothing changes the status anymore. |
| 5 | `advanceUntilIdle()` | Skip **all** the waiting: the download runs until the error at 60%. |
| 6 | `DownloadStatus.Failed("...")` | `Failed` is a **data class** (Chapter 4), so `assertEquals` compares the **message** inside. 💌 |

Run ▶️ → ✅✅.

> 🤔 **What about the "Done" path?** After 100%, `checkFile()` runs on **`Dispatchers.Default`** — a **real** background thread, **outside** the robot's virtual clock. ⏰🚫 The test can't control it. That's a hint from the code: "*the dispatcher should be **given** to me, not hard-coded!*" Remember Chapter 23: the Recipe Book's repository **receives** its coroutine scope from outside (Hilt's `CoroutinesModule`) instead of creating it itself. Dispatchers work the same way: pass the dispatcher **into** the class, and a test can pass a **test** dispatcher instead. You'll do this in **Challenge 2**. 💪

> 💡 Notice: `DownloadViewModel.uiState` is a **`MutableStateFlow`** underneath (`asStateFlow()`), so `uiState.value` is **always** up to date. With **`stateIn`**, it's different… 👇

---

## 27.12 Testing `stateIn` ViewModels: The Fruit Finder 🍎

Remember the **Fruit Finder** in MyFirstApp (Chapter 18)? Its `uiState` is made with **`combine` + `stateIn(WhileSubscribed(5_000))`**.

`WhileSubscribed` means: "*Only work while **someone is watching**.*" 👀 On the phone, the screen watches with `collectAsStateWithLifecycle()`. But in a test… **nobody** is watching! So the ViewModel never does the work, and `uiState.value` stays the **initial value** forever. 😴

**The fix:** in the test, start a small **watcher** that collects in the background. 🕵️

First, add `kotlinx-coroutines-test` to MyFirstApp (27.9) and create its `MainDispatcherRule.kt` (27.10). Then **`FruitViewModelTest`**:

```kotlin
package com.example.myfirstapp

import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class FruitViewModelTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    @Test
    fun start_showsAllThirteenFruits() = runTest {
        val viewModel = FruitViewModel()
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {        // (1)
            viewModel.uiState.collect()                                         // (2)
        }

        assertEquals(13, viewModel.uiState.value.fruits.size)
    }

    @Test
    fun search_an_findsThreeFruitsInOrder() = runTest {
        val viewModel = FruitViewModel()
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
            viewModel.uiState.collect()
        }

        viewModel.onQueryChange("an")                                           // (3)

        assertEquals(
            listOf("Banana 🍌", "Mango 🥭", "Orange 🍊"),
            viewModel.uiState.value.fruits
        )
    }

    @Test
    fun search_ignoresSpacesAndCase() = runTest {
        val viewModel = FruitViewModel()
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
            viewModel.uiState.collect()
        }

        viewModel.onQueryChange("  KIWI ")                                      // (4)

        assertEquals(listOf("Kiwi 🥝"), viewModel.uiState.value.fruits)
    }

    @Test
    fun sortZtoA_putsWatermelonFirst() = runTest {
        val viewModel = FruitViewModel()
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
            viewModel.uiState.collect()
        }

        viewModel.onSortChange(zToA = true)

        assertEquals("Watermelon 🍉", viewModel.uiState.value.fruits.first())
        assertTrue(viewModel.uiState.value.sortZtoA)
    }

    @Test
    fun search_noMatch_givesEmptyList() = runTest {
        val viewModel = FruitViewModel()
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
            viewModel.uiState.collect()
        }

        viewModel.onQueryChange("pizza")                                        // (5)

        assertTrue(viewModel.uiState.value.fruits.isEmpty())
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `backgroundScope.launch(UnconfinedTestDispatcher(testScheduler))` | Start a **watcher** coroutine. **`backgroundScope`** is a special scope inside `runTest`: its coroutines are **cancelled automatically** when the test ends (a normal `launch` that collects forever would make the test **never** finish!). `UnconfinedTestDispatcher(testScheduler)` = start **immediately**, on the **same** virtual clock. |
| 2 | `.collect()` | Collect **without** doing anything with the values. We only want the ViewModel to **feel watched**, so `WhileSubscribed` starts working. 👀 (This `collect()` with **no** braces needs `import kotlinx.coroutines.flow.collect`.) |
| 3 | `onQueryChange("an")` | Same as typing "an" on the screen. `combine` runs again **immediately** (Unconfined), so on the next line `uiState.value` is already updated. |
| 4 | `"  KIWI "` | Spaces **and** capital letters — two edges at once. `trim()` and `ignoreCase = true` should handle both. |
| 5 | `"pizza"` | Not a fruit 🍕 → an empty list, no crash. |

Run ▶️ → **5 green checks**. ✅

### See the problem with your own eyes 👀

In `search_an_findsThreeFruitsInOrder`, **delete** the three lines of `backgroundScope.launch { ... }` and run that test:

```
❌ search_an_findsThreeFruitsInOrder
Expected :[Banana 🍌, Mango 🥭, Orange 🍊]
Actual   :[Apple 🍎, Banana 🍌, Cherry 🍒, Grapes 🍇, Kiwi 🥝, … ]
```

Nobody watched → `WhileSubscribed` never started → still the initial value (all fruits). Put the lines back. ✅

> 🎯 **Rule:** a ViewModel with **`stateIn(WhileSubscribed(...))`** needs a **watcher** in the test: `backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) { viewModel.uiState.collect() }`. A ViewModel with a plain **`MutableStateFlow`** doesn't.

> 🧰 **Bonus — Turbine:** many teams use a small library called **Turbine** (`app.cash.turbine`) for testing Flows. It lets you write `flow.test { assertEquals(5, awaitItem()) }` — checking **every** value the Flow sends, one by one. It's great, but the tools in this chapter are **enough** for everything we do. Look it up when you're curious! 🐢

---

## 27.13 Fakes — Pretend Helpers for Tests 🎭

A ViewModel **needs** a repository. But in a test, we don't want a **real** one:

| Real repository | Problem in a test |
|---|---|
| Room database 🗄️ | Needs a phone (Context), slow, and data from one test stays for the next. |
| Internet 🌐 | Slow, needs a connection, and the answers change every day. |
| WorkManager ⚙️ | Needs a phone, and really schedules things! |

So we use a **fake**: a small, simple class that keeps the **same promise** (the same **interface**) but does everything **in memory**. 🧠 Like a **stunt double** in a movie 🎬: it looks the same from the outside, but it's much easier to work with.

```
                 RecipeRepository (the promise 📜)
                 /                  \
RoomRecipeRepository 🗄️      FakeRecipeRepository 🎭
   (the real app)               (the tests)
```

The ViewModel **can't tell** the difference — it only knows the interface. That's the gift of Chapters 16 and 23! 🎁

> 💡 **Fakes can also spy** 🕵️: they can count calls or remember values, so the test can ask "*Did the ViewModel really call `toggleFavorite`?*"

---

## 27.14 Testing the Recipe Book — The Chapter 16 Promise 🍕🧪

In Chapter 16 (section 16.12) we promised: *"Now a test (Chapter 27) can do: `vm.onToggleFavorite(1)` … check: `fakeRepo.toggleCalls == 1` ✅"*. Time to keep that promise! 🤝

Open the **Recipe Book**. Add **`kotlinx-coroutines-test`** (27.9) and create **`MainDispatcherRule.kt`** (27.10, with `package com.example.recipebook`) in the **`(test)`** package.

### `FakeRecipeRepository.kt` (in the test folder)

```kotlin
package com.example.recipebook

import com.example.recipebook.data.RecipeRepository
import com.example.recipebook.data.model.Recipe
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

val testRecipes = listOf(                                                    // (1)
    Recipe(id = 1, name = "Pizza", emoji = "🍕", minutes = 30,
        ingredients = emptyList(), steps = emptyList(), isFavorite = true),
    Recipe(id = 2, name = "Pasta", emoji = "🍝", minutes = 20,
        ingredients = emptyList(), steps = emptyList()),
    Recipe(id = 3, name = "Salad", emoji = "🥗", minutes = 10,
        ingredients = emptyList(), steps = emptyList())
)

class FakeRecipeRepository(
    recipes: List<Recipe> = testRecipes
) : RecipeRepository {                                                       // (2)

    private val _recipes = MutableStateFlow(recipes)
    override val recipes: StateFlow<List<Recipe>> = _recipes.asStateFlow()

    var toggleCalls = 0                                                      // (3)
        private set

    override fun getRecipe(id: Int): Recipe? = _recipes.value.find { it.id == id }

    override fun toggleFavorite(id: Int) {
        toggleCalls++
        _recipes.update { list ->
            list.map { if (it.id == id) it.copy(isFavorite = !it.isFavorite) else it }
        }
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `testRecipes` | Our **own** small test data: 3 recipes, only Pizza is a favorite. ⭐ We don't use the app's `sampleRecipes` — if someone changes those one day, our tests shouldn't break. Test data belongs to the **tests**. |
| 2 | `: RecipeRepository` | The **same** promise as the real repository. ✅ (If your interface has more functions — for example from a challenge — Android Studio underlines the class in red. Press **Alt + Enter → Implement members**.) |
| 3 | `var toggleCalls = 0` + `private set` | The **spy** counter 🕵️. Tests can **read** it, but only the fake can **change** it. |

> 📝 If you created a `FakeRecipeRepository` in the **main** code in Chapter 16 and nothing uses it there, delete that one. A fake that only tests need lives in the **test** folder. (If a Preview uses it, you can keep it — the two live in different packages, so they don't clash.)

### `RecipeListViewModelTest.kt`

```kotlin
package com.example.recipebook

import com.example.recipebook.ui.list.RecipeListViewModel
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class RecipeListViewModelTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private val fakeRepository = FakeRecipeRepository()                        // (1)

    @Test
    fun beforeAnyoneWatches_isLoading() {
        val viewModel = RecipeListViewModel(repository = fakeRepository, onlyFavorites = false)

        assertTrue(viewModel.uiState.value.isLoading)                           // (2)
    }

    @Test
    fun allRecipesTab_showsAllThree() = runTest {
        val viewModel = RecipeListViewModel(repository = fakeRepository, onlyFavorites = false)
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
            viewModel.uiState.collect()
        }

        val state = viewModel.uiState.value
        assertFalse(state.isLoading)
        assertEquals(listOf("Pizza", "Pasta", "Salad"), state.recipes.map { it.name })
    }

    @Test
    fun favoritesTab_showsOnlyFavorites() = runTest {
        val viewModel = RecipeListViewModel(repository = fakeRepository, onlyFavorites = true)   // (3)
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
            viewModel.uiState.collect()
        }

        assertEquals(listOf("Pizza"), viewModel.uiState.value.recipes.map { it.name })
    }

    @Test
    fun toggleFavorite_callsRepository_andFavoritesUpdate() = runTest {
        val viewModel = RecipeListViewModel(repository = fakeRepository, onlyFavorites = true)
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
            viewModel.uiState.collect()
        }

        viewModel.onToggleFavorite(2)                                           // (4)

        assertEquals(1, fakeRepository.toggleCalls)                             // (5)
        assertEquals(listOf("Pizza", "Pasta"), viewModel.uiState.value.recipes.map { it.name })   // (6)
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `private val fakeRepository = FakeRecipeRepository()` | A fresh fake for **every** test (JUnit makes a new test object each time). Creating a **fake** at the top is fine — only the **ViewModel** must be created inside the test. |
| 2 | `isLoading` before watching | Nobody watches yet → still the initial value (`isLoading = true`). This test **documents** how `WhileSubscribed` behaves. 📝 |
| 3 | `RecipeListViewModel(repository = ..., onlyFavorites = true)` | 🎉 **No Hilt needed!** The ViewModel is `@HiltViewModel` with `@AssistedInject`, but in a test we just call the **constructor** ourselves — exactly what Chapter 23 promised. |
| 4 | `onToggleFavorite(2)` | Like tapping ♥ on Pasta. |
| 5 | `toggleCalls == 1` | The spy says: "*Yes, the ViewModel asked me exactly once.*" ✅ **Promise kept!** 🤝 |
| 6 | `["Pizza", "Pasta"]` | And the Favorites list **updated by itself**, because the fake's `StateFlow` changed — the same reactive chain as in the real app. 🔁 |

Run ▶️ → **4 green checks**. ✅

---

## 27.15 Testing the Notes App 📝🧪

Now the **big** one: `NotesListViewModel` — search, sorting, delete with Undo, and the reminder. Let's look at its constructor (from Chapter 25):

```kotlin
class NotesListViewModel @Inject constructor(
    private val notesRepository: NotesRepository,                 // interface ✅ → fake it
    private val preferencesRepository: UserPreferencesRepository, // interface ✅ → fake it
    private val reminderScheduler: ReminderScheduler              // a CLASS ❌ — uses WorkManager!
) : ViewModel()
```

Two interfaces — easy to fake. But **`ReminderScheduler`** is a **class** that talks to WorkManager, which needs a real phone. 📱 We **can't** use it in a local test.

> 🧠 **A big lesson:** when code is **hard to test**, it's often telling you something about its **design**. The fix is the same trick we used for repositories: put an **interface** in front of it. Then the real app uses the real class, and tests use a fake. 🎭

### Step 1: Make `ReminderScheduler` an interface 🔌

Replace **`notifications/ReminderScheduler.kt`** with this (the inside of the class is the **same** as in Chapter 25 — only the top lines and the `override` words are new):

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

interface ReminderScheduler {                                                        // (1)
    fun scheduleDaily(hour: Int = 20)
    fun cancel()
    fun showPreviewNow()
}

@Singleton
class WorkManagerReminderScheduler @Inject constructor(                              // (2)
    @ApplicationContext private val context: Context
) : ReminderScheduler {

    private val workManager: WorkManager
        get() = WorkManager.getInstance(context)

    override fun scheduleDaily(hour: Int) {                                          // (3)
        val request = PeriodicWorkRequestBuilder<ReminderWorker>(1, TimeUnit.DAYS)
            .setInitialDelay(millisUntilNext(hour), TimeUnit.MILLISECONDS)
            .build()

        workManager.enqueueUniquePeriodicWork(
            DAILY_REMINDER_WORK,
            ExistingPeriodicWorkPolicy.UPDATE,
            request
        )
    }

    override fun cancel() {
        workManager.cancelUniqueWork(DAILY_REMINDER_WORK)
    }

    override fun showPreviewNow() {
        workManager.enqueue(OneTimeWorkRequestBuilder<ReminderWorker>().build())
    }

    private fun millisUntilNext(hour: Int): Long {
        val now = Calendar.getInstance()
        val next = Calendar.getInstance().apply {
            set(Calendar.HOUR_OF_DAY, hour)
            set(Calendar.MINUTE, 0)
            set(Calendar.SECOND, 0)
            set(Calendar.MILLISECOND, 0)
            if (before(now)) add(Calendar.DAY_OF_MONTH, 1)
        }
        return next.timeInMillis - now.timeInMillis
    }

    private companion object {
        const val DAILY_REMINDER_WORK = "daily_reminder"
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `interface ReminderScheduler` | The **promise** 📜: three things anyone can ask. It keeps the **old name**, so `NotesListViewModel` doesn't change at all! The default `hour = 20` lives here, in the interface. |
| 2 | `class WorkManagerReminderScheduler ... : ReminderScheduler` | The **real** worker, named after **how** it works (like `RoomNotesRepository`). Still `@Singleton` with `@Inject constructor`. |
| 3 | `override fun scheduleDaily(hour: Int)` | `override` = "this is how I keep the promise". ⚠️ **No** `= 20` here: Kotlin doesn't allow an `override` to repeat a default value — it's taken from the interface automatically. |

### Step 2: Tell Hilt which class keeps the promise — `di/RepositoryModule.kt`

Hilt can't build an **interface** (Chapter 23). Add one `@Binds` line:

```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    abstract fun bindNotesRepository(impl: RoomNotesRepository): NotesRepository

    @Binds
    abstract fun bindUserPreferencesRepository(
        impl: DataStoreUserPreferencesRepository
    ): UserPreferencesRepository

    @Binds                                                                     // 👈 new
    abstract fun bindReminderScheduler(
        impl: WorkManagerReminderScheduler
    ): ReminderScheduler
}
```

(Add the imports for `ReminderScheduler` and `WorkManagerReminderScheduler` from `com.example.notes.notifications` — **Alt + Enter**.)

**Run the app** ▶️ — the 🔔 button works **exactly** as before. ✅ Nothing changed for the user; we only made the code **testable**. 🧪

> 💡 Changing code to make it **better inside**, without changing what it **does**, is called **refactoring** 🧹. Tests make refactoring safe — and here, refactoring made tests possible!

### Step 3: The fakes — `NotesFakes.kt` (in the test folder)

Add **`kotlinx-coroutines-test`** (27.9) and **`MainDispatcherRule.kt`** (27.10, `package com.example.notes`) to the Notes app. Then, in **`com.example.notes (test)`**, create the file **`NotesFakes.kt`** — three fakes in one file:

> 🧩 Did you do **Chapter 24, Challenge 7**? Compare your `FakeNotesRepository` with this one!

```kotlin
package com.example.notes

import com.example.notes.data.NotesRepository
import com.example.notes.data.UserPreferencesRepository
import com.example.notes.data.model.Note
import com.example.notes.data.model.NoteColor
import com.example.notes.data.model.SortOrder
import com.example.notes.notifications.ReminderScheduler
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.update

class FakeNotesRepository(
    initialNotes: List<Note> = emptyList()
) : NotesRepository {

    private val notes = MutableStateFlow(initialNotes)                          // (1)
    private var nextId = (initialNotes.maxOfOrNull { it.id } ?: 0L) + 1         // (2)

    val allNotes: List<Note>                                                    // (3)
        get() = notes.value

    override fun observeNotes(query: String): Flow<List<Note>> =
        notes.map { list ->
            list.filter { note ->
                note.title.contains(query, ignoreCase = true) ||
                    note.content.contains(query, ignoreCase = true)             // (4)
            }
        }

    override suspend fun getNote(id: Long): Note? =
        notes.value.find { it.id == id }

    override suspend fun addNote(
        title: String,
        content: String,
        color: NoteColor,
        isPinned: Boolean,
        photoPath: String?
    ): Long {
        val id = nextId++                                                       // (5)
        val now = System.currentTimeMillis()
        val note = Note(
            id = id, title = title, content = content, color = color, isPinned = isPinned,
            createdAt = now, updatedAt = now, photoPath = photoPath
        )
        notes.update { it + note }
        return id
    }

    override suspend fun updateNote(note: Note) {
        notes.update { list -> list.map { if (it.id == note.id) note else it } }
    }

    override suspend fun deleteNote(note: Note) {
        notes.update { list -> list.filterNot { it.id == note.id } }
    }

    override suspend fun restoreNote(note: Note) {
        notes.update { list -> list.filterNot { it.id == note.id } + note }      // (6)
    }

    override suspend fun setPinned(id: Long, isPinned: Boolean) {
        notes.update { list -> list.map { if (it.id == id) it.copy(isPinned = isPinned) else it } }
    }
}

class FakeUserPreferencesRepository : UserPreferencesRepository {

    private val _sortOrder = MutableStateFlow(SortOrder.LAST_EDITED)            // (7)
    private val _reminderEnabled = MutableStateFlow(false)

    override val sortOrder: Flow<SortOrder> = _sortOrder
    override val reminderEnabled: Flow<Boolean> = _reminderEnabled

    override suspend fun setSortOrder(sortOrder: SortOrder) {
        _sortOrder.value = sortOrder
    }

    override suspend fun setReminderEnabled(enabled: Boolean) {
        _reminderEnabled.value = enabled
    }
}

class FakeReminderScheduler : ReminderScheduler {                               // (8)

    var scheduledHour: Int? = null
        private set
    var previewCount = 0
        private set
    var cancelCount = 0
        private set

    override fun scheduleDaily(hour: Int) {
        scheduledHour = hour
    }

    override fun cancel() {
        cancelCount++
        scheduledHour = null
    }

    override fun showPreviewNow() {
        previewCount++
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `MutableStateFlow(initialNotes)` | Our "database" 🗄️ — just a list in a `StateFlow`. When it changes, everyone watching gets the new list, **like Room**. 🔁 |
| 2 | `nextId` | The next free id, like Room's `autoGenerate`. `maxOfOrNull` gives the biggest id, or `null` for an empty list → then we start at 1. |
| 3 | `allNotes` | A **spy** property 🕵️: tests can look at **everything** inside, including notes hidden by a search. |
| 4 | `contains(query, ignoreCase = true)` in title **or** content | The **same** behavior as our Room query (`LIKE '%' || :query || '%'`, which also ignores upper/lower case). A good fake behaves like the real thing! An empty query matches everything. |
| 5 | `nextId++` | Use the id, **then** add 1 for next time (Chapter 2). |
| 6 | `filterNot { ... } + note` | Restore = put the note back (and never twice — like Room's `REPLACE`, Chapter 24). |
| 7 | Two `MutableStateFlow`s | Settings in memory instead of DataStore. They start with the **same** defaults as the real app. |
| 8 | `FakeReminderScheduler` | It schedules **nothing** — it only **remembers** what it was asked. 📝 |

### Step 4: `NotesListViewModelTest.kt` 🧪

```kotlin
package com.example.notes

import com.example.notes.data.model.SortOrder
import com.example.notes.ui.list.NotesListViewModel
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.TestScope
import kotlinx.coroutines.test.UnconfinedTestDispatcher
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Rule
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class NotesListViewModelTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private val shopping = testNote(1, title = "Shopping 🛒", content = "Milk, eggs", updatedAt = 300)   // (1)
    private val ideas = testNote(2, title = "Ideas 💡", content = "An app for my cat", updatedAt = 100)
    private val trip = testNote(3, title = "Trip ✈️", content = "Buy milk for the road",
        updatedAt = 200, isPinned = true)

    private lateinit var notesRepository: FakeNotesRepository                   // (2)
    private lateinit var preferences: FakeUserPreferencesRepository
    private lateinit var scheduler: FakeReminderScheduler
    private lateinit var viewModel: NotesListViewModel

    @Before                                                                     // (3)
    fun setUp() {
        notesRepository = FakeNotesRepository(listOf(shopping, ideas, trip))
        preferences = FakeUserPreferencesRepository()
        scheduler = FakeReminderScheduler()
        viewModel = NotesListViewModel(
            notesRepository = notesRepository,
            preferencesRepository = preferences,
            reminderScheduler = scheduler
        )
    }

    private fun TestScope.watchUiState() {                                      // (4)
        backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
            viewModel.uiState.collect()
        }
    }

    private fun shownIds(): List<Long> = viewModel.uiState.value.notes.map { it.id }   // (5)

    @Test
    fun start_pinnedFirst_thenNewestEdit() = runTest {
        watchUiState()

        assertFalse(viewModel.uiState.value.isLoading)
        assertEquals(listOf(3L, 1L, 2L), shownIds())                            // (6)
    }

    @Test
    fun search_findsTitleAndContent_ignoringCase() = runTest {
        watchUiState()

        viewModel.onQueryChange("MILK")                                         // (7)

        assertEquals(listOf(3L, 1L), shownIds())
        assertTrue(viewModel.uiState.value.isSearching)
    }

    @Test
    fun sortByTitle_isSaved_andUsed() = runTest {
        watchUiState()

        viewModel.onSortOrderChange(SortOrder.TITLE)

        assertEquals(SortOrder.TITLE, viewModel.uiState.value.sortOrder)
        assertEquals(listOf(3L, 2L, 1L), shownIds())                            // (8)
    }

    @Test
    fun delete_removesNote_andRemembersItForUndo() = runTest {
        watchUiState()

        viewModel.onDeleteNote(shopping)

        assertEquals(listOf(3L, 2L), shownIds())
        assertEquals(shopping, viewModel.uiState.value.recentlyDeleted)        // (9)
    }

    @Test
    fun undo_bringsTheNoteBack() = runTest {
        watchUiState()
        viewModel.onDeleteNote(shopping)

        viewModel.onUndoDelete()

        assertEquals(listOf(3L, 1L, 2L), shownIds())
        assertNull(viewModel.uiState.value.recentlyDeleted)
    }

    @Test
    fun undoTimeout_forgetsTheNote_andItStaysDeleted() = runTest {
        watchUiState()
        viewModel.onDeleteNote(shopping)

        viewModel.onUndoTimeout()

        assertNull(viewModel.uiState.value.recentlyDeleted)
        assertEquals(2, notesRepository.allNotes.size)                          // (10)
    }

    @Test
    fun pinClick_movesNoteToTheTop() = runTest {
        watchUiState()

        viewModel.onPinClick(ideas)

        assertEquals(listOf(3L, 2L, 1L), shownIds())                            // (11)
    }

    @Test
    fun reminderOn_schedulesAt8pm_andShowsPreview() = runTest {
        watchUiState()

        viewModel.onReminderToggle(true)

        assertTrue(viewModel.uiState.value.reminderEnabled)
        assertEquals(20, scheduler.scheduledHour)                               // (12)
        assertEquals(1, scheduler.previewCount)
    }

    @Test
    fun reminderOff_cancels() = runTest {
        watchUiState()
        viewModel.onReminderToggle(true)

        viewModel.onReminderToggle(false)

        assertFalse(viewModel.uiState.value.reminderEnabled)
        assertEquals(1, scheduler.cancelCount)
        assertNull(scheduler.scheduledHour)
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | Three test notes | Made with our `testNote` helper (27.8). **Trip** is pinned 📌. **Shopping** was edited last (300), **Ideas** first (100). Both Shopping and Trip contain "milk" 🥛 — useful for the search test. |
| 2 | `lateinit var` | "*I'll give this a value later, before using it*" (Chapter 14). They're filled in `setUp()`. |
| 3 | `@Before fun setUp()` | JUnit runs this **before every test** — after the rule has set up Main. ✅ Every test gets **fresh** fakes and a **fresh** ViewModel, so tests never disturb each other. 🧼 |
| 4 | `private fun TestScope.watchUiState()` | A small **helper** with the "watcher" lines from 27.12, so we don't repeat them 9 times. ✂️ It's an **extension function** on `TestScope` (Chapter 4), so it can use `backgroundScope` and `testScheduler`. |
| 5 | `shownIds()` | Another helper: the ids of the notes the screen would show, in order. |
| 6 | `[3, 1, 2]` | Trip first (📌), then Shopping (edited at 300), then Ideas (100). ✅ |
| 7 | `"MILK"` | In capital letters! It should still find "Milk, eggs" (Shopping) **and** "Buy milk…" (Trip, in the **content**). Trip is pinned → first. |
| 8 | `[3, 2, 1]` by title | Trip (📌) first, then **I**deas before **S**hopping. And `sortOrder` in the state is `TITLE` → the fake preferences really saved it. |
| 9 | `recentlyDeleted == shopping` | The screen needs this to show the "Undo" Snackbar. `Note` is a data class, so `assertEquals` compares all its values. |
| 10 | `notesRepository.allNotes.size == 2` | Using the **spy** property: the note is **really** gone from the "database". |
| 11 | Pin Ideas → `[3, 2, 1]` | Two pinned notes now: Trip (edited at 200) and Ideas (100) — both on top, newest edit first. Then Shopping. |
| 12 | `scheduledHour == 20` | The ViewModel called `scheduleDaily()` **without** an hour → the interface's default **20** (8 PM) was used. And one preview was shown. 🔔 |

Run ▶️ → **9 green checks**. ✅🎉

That's the **whole** list screen's logic — search, sorting, delete, Undo, pins, and reminders — tested in about **one second**, without a phone, a database, or WorkManager. 🚀

> 🧪 **Make one fail on purpose:** in `NotesListViewModel.onUndoDelete()`, comment out the line `viewModelScope.launch { notesRepository.restoreNote(note) }` (put `//` in front). Run the tests → `undo_bringsTheNoteBack` turns **red**: *Expected [3, 1, 2], Actual [3, 2]*. Remove the `//` → green. The robot is watching! 🤖👀

> 💡 **Tip — let Android Studio create test files:** put the cursor on a class name (for example `NotesListViewModel`), press **Ctrl + Shift + T** → **Create New Test…** → choose **JUnit4** and the **test** folder (not androidTest). Android Studio creates the file in the matching package for you.

---

## 27.16 Compose UI Tests — A Robot That Taps Your Buttons 🤖👆

Unit tests check the **logic**. But what about the **screen**? Does the button really appear? Is it disabled at the right moment? Does tapping it really change the text?

A **Compose UI test** is a robot that **looks** at your screen and **taps** it — **thousands** of times faster than you, and it never gets bored. 🤖

### How does the robot "see"? 👀 The semantics tree

The robot can't look at **pixels** like you. Instead, it reads the **semantics tree** 🌳: a description of the screen that Compose builds anyway — **the same one TalkBack uses** to read the screen aloud for blind users (Chapter 26's accessibility notes!).

```
Screen
 ├── Text: "Cookies: 0"           (tag: cookieCount)
 ├── Button (clickable, enabled)
 │     └── Text: "Add cookie 🍪"
 └── Button (clickable, enabled)
       └── Text: "Reset"
```

So the robot asks things like: "*Find the node with the text 'Reset' and click it.*" 🎯

> 💡 **Bonus:** if the robot can find your things, TalkBack can too. Good UI tests and good **accessibility** go together. ♿

### Where do UI tests live? 📱

UI tests need a **real** screen → they go in the **`androidTest`** folder and run on an **emulator or phone**. Good news: every new project **already** has everything they need in `build.gradle.kts`:

```kotlin
androidTestImplementation(platform(libs.androidx.compose.bom))
androidTestImplementation(libs.androidx.ui.test.junit4)          // the robot 🤖
debugImplementation(libs.androidx.ui.test.manifest)              // a tiny empty screen for tests
```

✅ Nothing to add!

### A screen to test: the Cookie Counter 🍪

In **MyFirstApp**, create **`CookieCounter.kt`** (in the **main** code):

```kotlin
package com.example.myfirstapp

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp

const val MAX_COOKIES = 5

@Composable
fun CookieCounter(modifier: Modifier = Modifier) {
    var cookies by rememberSaveable { mutableIntStateOf(0) }
    val isFull = cookies >= MAX_COOKIES

    Column(
        modifier = modifier.padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(
            text = "Cookies: $cookies",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.testTag("cookieCount")                    // (1)
        )
        if (isFull) {
            Text("That's enough cookies! 🛑")                              // (2)
        }
        Button(onClick = { cookies++ }, enabled = !isFull) {               // (3)
            Text("Add cookie 🍪")
        }
        OutlinedButton(onClick = { cookies = 0 }) {
            Text("Reset")
        }
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `Modifier.testTag("cookieCount")` | A **name tag** 🏷️ only for tests. The user never sees it. It lets the robot find this exact `Text`, even when its words change ("Cookies: 0", "Cookies: 1"…). |
| 2 | The "enough" message | Appears only when there are 5 cookies. |
| 3 | `enabled = !isFull` | The button turns **off** at 5 cookies. |

### The test: `CookieCounterTest.kt` (in `androidTest`!)

Right-click **`com.example.myfirstapp (androidTest)`** → **New → Kotlin Class/File → Class** → **`CookieCounterTest`**:

```kotlin
package com.example.myfirstapp

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertIsNotEnabled
import androidx.compose.ui.test.assertTextEquals
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import com.example.myfirstapp.ui.theme.MyFirstAppTheme
import org.junit.Rule
import org.junit.Test

class CookieCounterTest {

    @get:Rule
    val composeTestRule = createComposeRule()                                  // (1)

    private fun showCounter() {
        composeTestRule.setContent {                                           // (2)
            MyFirstAppTheme {
                CookieCounter()
            }
        }
    }

    @Test
    fun start_showsZeroCookies() {
        showCounter()

        composeTestRule.onNodeWithTag("cookieCount")                           // (3)
            .assertTextEquals("Cookies: 0")                                    // (4)
    }

    @Test
    fun clickAdd_countsUp() {
        showCounter()

        composeTestRule.onNodeWithText("Add cookie 🍪").performClick()        // (5)

        composeTestRule.onNodeWithTag("cookieCount").assertTextEquals("Cookies: 1")
    }

    @Test
    fun fiveCookies_disablesButton_andShowsMessage() {
        showCounter()

        repeat(MAX_COOKIES) {                                                  // (6)
            composeTestRule.onNodeWithText("Add cookie 🍪").performClick()
        }

        composeTestRule.onNodeWithText("Add cookie 🍪").assertIsNotEnabled()  // (7)
        composeTestRule.onNodeWithText("That's enough cookies! 🛑").assertIsDisplayed()
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `createComposeRule()` | The robot's **rule** 🤖: before each test, it opens an empty test screen; after, it closes it. |
| 2 | `setContent { ... }` | Like `setContent` in `MainActivity` — put **any** Composable on the test screen. |
| 3 | `onNodeWithTag("cookieCount")` | **Find** the node with this test tag. 🔍 |
| 4 | `assertTextEquals("Cookies: 0")` | **Check** its text is exactly this. ✅ |
| 5 | `onNodeWithText("Add cookie 🍪").performClick()` | Find the button by its text and **tap** it. 👆 The robot then **waits** automatically until the screen has updated (recomposition, animations…) before the next line. ⏳ |
| 6 | `repeat(MAX_COOKIES) { ... }` | Tap 5 times (`repeat`, Chapter 2). We use the **constant** — if the limit changes to 10, the test still works. |
| 7 | `assertIsNotEnabled()` | The button must be **disabled** now. 🚫 |

### Run it 📱

1. **Start the emulator** (or connect your phone).
2. Click the ▶ next to `class CookieCounterTest` → **Run 'CookieCounterTest'**.

It takes longer than unit tests (it builds and installs a test app 📦). Watch the emulator: screens **flash** by for a moment — that's the robot working! 🤖⚡ Then:

```
✅ CookieCounterTest
   ✅ start_showsZeroCookies
   ✅ clickAdd_countsUp
   ✅ fiveCookies_disablesButton_andShowsMessage
Tests passed: 3 of 3 tests
```

🎉 Your first UI tests!

### The robot's toolbox 🧰

**1. Finders** — "*find…*" 🔍

| Finder | Finds the node… |
|---|---|
| `onNodeWithText("Reset")` | with this text (`substring = true` → text **containing** it) |
| `onNodeWithTag("cookieCount")` | with this `testTag` |
| `onNodeWithContentDescription("Pin note")` | with this description (icons! 🖼️) |
| `onAllNodesWithText("Delete")` | **all** matching nodes → then `.assertCountEquals(3)` or `[0]` for the first |
| `onRoot()` | the whole screen |

> ⚠️ `onNodeWith...` expects **exactly one** match. If there are **two** nodes with the same text, the test fails with *"Expected exactly '1' node but found '2'"*. Use a `testTag` or `onAllNodesWithText(...)[0]`.

**2. Actions** — "*do…*" 👆

| Action | Does |
|---|---|
| `performClick()` | Tap |
| `performTextInput("hello")` | Type into a text field ⌨️ |
| `performTextClearance()` | Delete all text in a field |
| `performScrollTo()` | Scroll until this node is visible (in a scrollable `Column`) |
| `performTouchInput { swipeLeft() }` | Gestures: swipe, long-press, double-click… |

**3. Assertions** — "*check…*" ✅

| Assertion | Checks that the node… |
|---|---|
| `assertIsDisplayed()` | is **visible** on the screen |
| `assertDoesNotExist()` | is **not** there at all |
| `assertIsEnabled()` / `assertIsNotEnabled()` | can / can't be tapped |
| `assertTextEquals("...")` | has **exactly** this text |
| `assertTextContains("...")` | has text **containing** this |
| `assertIsOn()` / `assertIsOff()` | a `Switch` or `Checkbox` is on / off |
| `assertIsSelected()` | is selected (tabs, chips) |

### Lost? Print the tree! 🌳🖨️

If the robot can't find something, ask it to **print** what it sees:

```kotlin
import androidx.compose.ui.test.onRoot
import androidx.compose.ui.test.printToLog

composeTestRule.onRoot().printToLog("TREE")
```

Run the test, then look in **Logcat** for the tag `TREE`:

```
Node #1 at (l=0.0, t=0.0, r=1080.0, b=2400.0)px
 |-Node #3 at (...)px, Tag: 'cookieCount'
 |  Text = '[Cookies: 0]'
 |-Node #5 at (...)px
 |  Role = 'Button'
 |  Focused = 'false'
 |  Text = '[Add cookie 🍪]'
 |  Actions = [OnClick, RequestFocus]
 |  MergeDescendants = 'true'
```

Notice **`MergeDescendants = 'true'`** on the button: Compose **merges** the button and its `Text` into **one** node — just like TalkBack reads "Add cookie, button" as **one** thing. That's why `onNodeWithText("Add cookie 🍪")` finds the **button** (which we can click), not only the text. 🔗

> 💡 Need the separate, **unmerged** pieces? Most finders take `useUnmergedTree = true`: `onNodeWithText("Add cookie 🍪", useUnmergedTree = true)`.

---

## 27.17 UI Tests for the Notes App 📝🤖

Our Notes screens follow the **Route + Screen** pattern (Chapter 15): the **Screen** gets everything as **parameters** — the state and the event lambdas. That makes it **perfect** for UI tests: we can show **any** state we like, and **record** which events fire. No ViewModel, no database, no Hilt needed! 🎉

### Testing `NoteCard` 🃏

In **`com.example.notes (androidTest)`**, create **`NoteCardTest`**:

```kotlin
package com.example.notes

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import com.example.notes.data.model.Note
import com.example.notes.data.model.NoteColor
import com.example.notes.ui.list.NoteCard
import com.example.notes.ui.theme.NotesTheme
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test

class NoteCardTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    private fun note(title: String, content: String = "", isPinned: Boolean = false): Note {   // (1)
        val now = System.currentTimeMillis()
        return Note(
            id = 1, title = title, content = content, color = NoteColor.YELLOW,
            isPinned = isPinned, createdAt = now, updatedAt = now
        )
    }

    @Test
    fun showsTitleContentAndTime() {
        composeTestRule.setContent {
            NotesTheme {
                NoteCard(note = note("Shopping 🛒", "Milk, eggs"), onClick = {}, onPinClick = {})
            }
        }

        composeTestRule.onNodeWithText("Shopping 🛒").assertIsDisplayed()
        composeTestRule.onNodeWithText("Milk, eggs").assertIsDisplayed()
        composeTestRule.onNodeWithText("Edited just now").assertIsDisplayed()      // (2)
    }

    @Test
    fun blankTitle_showsUntitled() {
        composeTestRule.setContent {
            NotesTheme {
                NoteCard(note = note(title = ""), onClick = {}, onPinClick = {})
            }
        }

        composeTestRule.onNodeWithText("Untitled").assertIsDisplayed()
    }

    @Test
    fun tapPin_callsOnPinClick() {
        var pinClicks = 0                                                          // (3)
        composeTestRule.setContent {
            NotesTheme {
                NoteCard(note = note("Ideas 💡"), onClick = {}, onPinClick = { pinClicks++ })
            }
        }

        composeTestRule.onNodeWithContentDescription("Pin note").performClick()    // (4)

        assertEquals(1, pinClicks)
    }

    @Test
    fun pinnedNote_offersUnpin() {
        composeTestRule.setContent {
            NotesTheme {
                NoteCard(note = note("Trip ✈️", isPinned = true), onClick = {}, onPinClick = {})
            }
        }

        composeTestRule.onNodeWithContentDescription("Unpin note").assertIsDisplayed()   // (5)
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `private fun note(...)` | A small helper, like `testNote` — but that one lives in the `test` folder, and **`androidTest` can't see `test`** (they're two separate worlds 🌍🌎). So we make a little one here. |
| 2 | `"Edited just now"` | From `editedText()` (Chapter 24) — `updatedAt` is **now**. This uses Android's `DateUtils`, which works here because UI tests run on a **real** Android. 📱 |
| 3 | `var pinClicks = 0` | A **spy** inside the test: our lambda counts the taps. |
| 4 | `onNodeWithContentDescription("Pin note")` | The pin button has no text a robot can rely on (just 📌), but it has a **description** — the one we added for TalkBack in Chapter 24. Accessibility pays off **twice**! ♿🤖 |
| 5 | `"Unpin note"` | A pinned note offers the **opposite** action. ✅ |

### Testing `NotesListScreen` 📋

First, give the search field a **test tag**. In **`NotesListScreen.kt`**, add one line to the `OutlinedTextField`'s modifier:

```kotlin
modifier = Modifier
    .fillMaxWidth()
    .padding(horizontal = 16.dp, vertical = 8.dp)
    .testTag("searchField")                                                    // 👈 new
```

(Import `androidx.compose.ui.platform.testTag`.)

Now **`NotesListScreenTest`** (in `androidTest`):

```kotlin
package com.example.notes

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performTextInput
import com.example.notes.data.model.Note
import com.example.notes.data.model.NoteColor
import com.example.notes.ui.list.NotesListScreen
import com.example.notes.ui.list.NotesListUiState
import com.example.notes.ui.theme.NotesTheme
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test

class NotesListScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    private fun showScreen(                                                    // (1)
        uiState: NotesListUiState,
        query: String = "",
        onQueryChange: (String) -> Unit = {},
        onAddClick: () -> Unit = {}
    ) {
        composeTestRule.setContent {
            NotesTheme {
                NotesListScreen(
                    uiState = uiState,
                    query = query,
                    onQueryChange = onQueryChange,
                    onSortOrderChange = {},
                    onNoteClick = {},
                    onPinClick = {},
                    onDeleteNote = {},
                    onUndoDelete = {},
                    onUndoTimeout = {},
                    onAddClick = onAddClick,
                    onReminderClick = {}
                )
            }
        }
    }

    private fun note(id: Long, title: String): Note {
        val now = System.currentTimeMillis()
        return Note(id, title, "", NoteColor.DEFAULT, false, now, now)
    }

    @Test
    fun noNotes_showsFriendlyEmptyMessage() {
        showScreen(NotesListUiState(isLoading = false))                       // (2)

        composeTestRule.onNodeWithText("No notes yet", substring = true).assertIsDisplayed()
    }

    @Test
    fun loading_doesNotShowEmptyMessage() {
        showScreen(NotesListUiState())                                         // (3)

        composeTestRule.onNodeWithText("No notes yet", substring = true).assertDoesNotExist()
    }

    @Test
    fun withNotes_showsTheirTitles() {
        showScreen(
            NotesListUiState(
                notes = listOf(note(1, "Shopping 🛒"), note(2, "Ideas 💡")),
                isLoading = false
            )
        )

        composeTestRule.onNodeWithText("Shopping 🛒").assertIsDisplayed()
        composeTestRule.onNodeWithText("Ideas 💡").assertIsDisplayed()
    }

    @Test
    fun searchWithoutResults_showsNoMatchMessage() {
        showScreen(
            uiState = NotesListUiState(isSearching = true, isLoading = false),
            query = "pizza"
        )

        composeTestRule.onNodeWithText("No notes match \"pizza\"", substring = true).assertIsDisplayed()
    }

    @Test
    fun typingInSearch_sendsTheText() {
        var lastQuery = ""
        showScreen(NotesListUiState(isLoading = false), onQueryChange = { lastQuery = it })

        composeTestRule.onNodeWithTag("searchField").performTextInput("milk")  // (4)

        assertEquals("milk", lastQuery)
    }

    @Test
    fun tapNewNote_callsOnAddClick() {
        var addClicks = 0
        showScreen(NotesListUiState(isLoading = false), onAddClick = { addClicks++ })

        composeTestRule.onNodeWithText("New note").performClick()              // (5)

        assertEquals(1, addClicks)
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `showScreen(...)` | A helper: shows the screen with the state we choose. Only the lambdas a test **cares** about are parameters; the rest do nothing (`{}`). (`snackbarHostState` has a default since Chapter 25, so we can leave it out.) |
| 2 | `NotesListUiState(isLoading = false)` | Loaded, but **no** notes → the friendly empty message. `substring = true` because the full text also has "Tap + to write…" on a second line. |
| 3 | `NotesListUiState()` | The **default** state has `isLoading = true` → a spinner, **not** the empty message. This protects against a classic bug: showing "No notes yet!" for a split second while the notes are still loading. 😬 |
| 4 | `performTextInput("milk")` | The robot **types** "milk". The field calls `onQueryChange("milk")` → our spy saves it. |
| 5 | `onNodeWithText("New note")` | The **Extended** FAB from Chapter 26 shows the text "New note" at the top of the list. 👆 |

Run ▶️ (emulator on!) → **6 green checks**. ✅

> 💡 We tested `NotesListViewModel` (local tests) **and** `NotesListScreen` (UI tests) **separately**. Together they cover the whole list feature. That's the beauty of the Route + Screen split from Chapter 15! ✂️

---

## 27.18 A Peek at Big Tests with Hilt 🔭 (optional ⭐)

So far, each test checked **one piece**. Sometimes you also want to test the **whole app** — real screens, real navigation, real ViewModels made by Hilt — but with **fake** data. In Chapter 23 we mentioned **`@TestInstallIn`**: it **replaces** a Hilt module with a test module. Here's how it looks. You don't have to do this now — it's a preview of what professional teams do. 👀

**1. Add Hilt's testing library** (`libs.versions.toml` → `[libraries]`):

```toml
hilt-android-testing = { group = "com.google.dagger", name = "hilt-android-testing", version.ref = "hilt" }
```

…and in `build.gradle.kts (Module :app)`:

```kotlin
androidTestImplementation(libs.hilt.android.testing)
kspAndroidTest(libs.hilt.android.compiler)                 // Hilt writes code for the androidTest folder too
```

**2. A special test runner** — `HiltTestRunner.kt` in `androidTest`:

```kotlin
package com.example.notes

import android.app.Application
import android.content.Context
import androidx.test.runner.AndroidJUnitRunner
import dagger.hilt.android.testing.HiltTestApplication

class HiltTestRunner : AndroidJUnitRunner() {
    override fun newApplication(cl: ClassLoader?, className: String?, context: Context?): Application =
        super.newApplication(cl, HiltTestApplication::class.java.name, context)
}
```

It says: "*During tests, don't use `NotesApplication` — use Hilt's special **test** application.*" Then, in `build.gradle.kts`, inside `defaultConfig { }`, change the runner line:

```kotlin
testInstrumentationRunner = "com.example.notes.HiltTestRunner"
```

**3. Replace the real module with a fake one** — `FakeRepositoryModule.kt` in `androidTest`:

```kotlin
package com.example.notes

import com.example.notes.data.NotesRepository
import com.example.notes.data.UserPreferencesRepository
import com.example.notes.di.RepositoryModule
import com.example.notes.notifications.ReminderScheduler
import dagger.Module
import dagger.Provides
import dagger.hilt.components.SingletonComponent
import dagger.hilt.testing.TestInstallIn
import javax.inject.Singleton

@Module
@TestInstallIn(
    components = [SingletonComponent::class],
    replaces = [RepositoryModule::class]                                     // 👈 "use me INSTEAD of that one"
)
object FakeRepositoryModule {

    @Provides
    @Singleton
    fun provideNotesRepository(): NotesRepository {
        val now = System.currentTimeMillis()
        return FakeNotesRepository(
            listOf(testNote(1, title = "Shopping 🛒", content = "Milk, eggs", updatedAt = now))
        )
    }

    @Provides
    @Singleton
    fun providePreferences(): UserPreferencesRepository = FakeUserPreferencesRepository()

    @Provides
    @Singleton
    fun provideReminderScheduler(): ReminderScheduler = FakeReminderScheduler()
}
```

> ⚠️ The `androidTest` folder **can't see** the `test` folder. For this to work, **copy** `NotesFakes.kt` and `TestNotes.kt` into `androidTest` too. (Big projects put shared test code in its own module — a topic for later.)

**4. The test — the whole app, with fake data:**

```kotlin
package com.example.notes

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import dagger.hilt.android.testing.HiltAndroidRule
import dagger.hilt.android.testing.HiltAndroidTest
import org.junit.Before
import org.junit.Rule
import org.junit.Test

@HiltAndroidTest                                                             // (1)
class NotesAppTest {

    @get:Rule(order = 0)
    val hiltRule = HiltAndroidRule(this)                                     // (2)

    @get:Rule(order = 1)
    val composeTestRule = createAndroidComposeRule<MainActivity>()           // (3)

    @Before
    fun setUp() {
        hiltRule.inject()
    }

    @Test
    fun tapNote_opensItInTheEditor() {
        composeTestRule.onNodeWithText("Shopping 🛒").performClick()          // (4)

        composeTestRule.onNodeWithText("Milk, eggs").assertIsDisplayed()     // (5)
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `@HiltAndroidTest` | "Hilt, build things for **this** test." |
| 2 | `HiltAndroidRule(this)`, `order = 0` | Hilt's rule must start **first** (before the Activity), so `order = 0`. |
| 3 | `createAndroidComposeRule<MainActivity>()` | Unlike `createComposeRule()`, this starts our **real** `MainActivity` — the real app, with real navigation! |
| 4 | Tap the note | The list shows the note from the **fake** repository. |
| 5 | `"Milk, eggs"` visible | We're in the **editor** now — navigation, the editor's ViewModel, and Hilt all worked together. 🎉 |

That's an **end-to-end** test: the top of the testing pyramid 🔺. Powerful, but slower and more work to set up — that's why we write **fewer** of them.

---

## 27.19 The Most Common Crashes — and Their Fixes 💥🔧

Keep this table close! 📌 Most crashes you'll ever see are on this list. Search for the **exception name** from line (B) of the stack trace:

| Exception (line B) | What it means | Fix | Chapter |
|---|---|---|---|
| `NullPointerException` | Something was `null` and you used it (often after `!!`) | Use `?.`, `?:`, or check for `null` | 3 |
| `UninitializedPropertyAccessException: lateinit property x has not been initialized` | You used a `lateinit var` before giving it a value | Give it a value first, or use a nullable type | 14 |
| `NumberFormatException: For input string: "..."` | `toInt()` / `toDouble()` on text that isn't a number | `toIntOrNull()` and handle `null` | 2, 9 |
| `IndexOutOfBoundsException` / `ArrayIndexOutOfBoundsException` | Asked for a position that doesn't exist | Check `size`, use `getOrNull(i)` | 3 |
| `IllegalArgumentException: Key "…" was already used` | Two items in a `LazyColumn`/grid have the **same** `key` | Make keys unique (`distinct()`, real ids) | 10, 20 |
| `NetworkOnMainThreadException` | Internet work on the main thread | `suspend` Retrofit functions, `withContext(Dispatchers.IO)` | 18, 19 |
| `SecurityException: Permission denied (missing INTERNET permission?)` | Forgot the INTERNET permission | Add `<uses-permission android:name="android.permission.INTERNET" />` to the manifest | 19 |
| `SerializationException: Serializer for class '…' is not found` | Forgot `@Serializable` (or the serialization plugin) | Add `@Serializable` / the plugin | 13, 19 |
| `IllegalStateException: Cannot access database on the main thread` | A Room function that isn't `suspend`/`Flow`, called on Main | Make DAO functions `suspend` or return `Flow` | 22 |
| `IllegalStateException: Room cannot verify the data integrity…` | You changed an `@Entity` but not the version / migration | Increase `version`, add a `Migration` | 22, 25 |
| `RuntimeException: Cannot find implementation for …Database. …_Impl does not exist` | Room's code generator (KSP) didn't run | Add `ksp(libs.androidx.room.compiler)`; check the KSP version | 22 |
| `IllegalStateException: Given component holder class MainActivity does not implement interface dagger.hilt.internal.GeneratedComponent…` | Forgot `@AndroidEntryPoint` (or `@HiltAndroidApp`) | Add the label to the Activity / Application | 23 |
| `IllegalArgumentException: Navigation destination that matches route … cannot be found` | Navigated to a route that's not in the `NavHost` | Add `composable<YourRoute> { ... }` | 13 |
| `ActivityNotFoundException: No Activity found to handle Intent` | No app on the phone can open this (Maps, email…) | Wrap `startActivity` in `try`/`catch` | 25 |
| `FileUriExposedException` | Gave a `file://` path to another app | Use a `FileProvider` (`content://`) | 25 |
| `OutOfMemoryError` | Too much memory — usually huge images | Let **Coil** load images (it resizes them) | 20 |
| **ANR** — *"App isn't responding"* (not a crash, a freeze 🥶) | The main thread was busy for ~5 seconds | Move heavy work to `Dispatchers.Default` / `IO` | 18 |

> 💡 **ANRs** don't create a normal stack trace in Logcat. Look for lines with **`ANR in com.example...`** (filter `level:error`), and think: "*What heavy work did I do on the main thread?*"

---

## 27.20 Good Testing Habits 🏆

### What to test ✅ and what not ❌

| ✅ Test this | ❌ Don't bother |
|---|---|
| Your **logic**: calculations, formatting, sorting, filtering | Simple `data class`es with no logic |
| **ViewModels**: "when the user does X, the state becomes Y" | **Libraries** themselves (Room, Retrofit, Compose are already tested by their makers) |
| **Edges**: empty, zero, one, huge, `null`, spaces, capital letters | `private` functions directly — test them **through** the public functions that use them |
| **Bugs you fixed** (so they never come back) | The exact colors and pixel sizes |
| Important **screens**: does the right thing appear, do buttons call the right lambdas | Every tiny detail of every screen |

### Good tests are… 🌟

| Quality | Meaning | Our trick |
|---|---|---|
| **Fast** ⚡ | Milliseconds, so you run them often | Local tests, fakes, virtual time |
| **Independent** 🧍 | No test depends on another test | Fresh objects in every test (`@Before`, new fakes) |
| **Repeatable** 🔁 | Same result every time — no real clock, no internet, no randomness | Fakes, `runTest`, test dispatchers |
| **Clear** 📖 | The name and the AAA steps tell the story | `subject_situation_result`, Arrange/Act/Assert |

### The bug-fixing recipe 🐛➡️🧪➡️🔧

When you find a bug:

1. Write a test that **shows** the bug → it's **red** 🔴.
2. Fix the code → the test turns **green** 🟢.
3. Keep the test **forever** — the bug can **never** come back unnoticed. 🛡️

### When to run tests ⏰

- **Before every commit** (Git) — a habit that saves you many times. 💾
- After **every big change** (refactoring, a new library version).
- Unit tests: **all the time** (they're fast!). UI tests: before a release (Chapter 28!).

### Code coverage 📊

Right-click the `(test)` package → **More Run/Debug → Run 'Tests in …' with Coverage**. Android Studio colors your code: **green** lines were run by tests, **red** lines never were. 🟩🟥

It's a nice way to find **forgotten** code. But don't chase **100%**: it's better to have **good** tests for the **important** code than silly tests for everything. 🎯

---

## 27.21 Test Checklist ✅

| What to check | Expected | ✅ |
|---|---|---|
| Logcat: `package:mine tag:ClickDiary` | Only your click messages, in 3 colors | ☐ |
| Crash Lab: each button | A different exception; the blue link jumps to the right line | ☐ |
| Debugger: breakpoint in `averageScore` | App pauses, `total = 5`, `average = 2` (before the fix) | ☐ |
| `ScoreMathTest` | 3 green (after both fixes) | ☐ |
| `FormatTimeTest`, `BreedNameTest`, `SortedForTest` | All green | ☐ |
| `FakeDownloaderTest` | Green, in milliseconds, `currentTime == 4000` | ☐ |
| `DownloadViewModelTest` | 2 green | ☐ |
| `FruitViewModelTest` | 5 green; red when you remove the watcher | ☐ |
| `RecipeListViewModelTest` | 4 green; `toggleCalls == 1` | ☐ |
| Notes: `ReminderScheduler` is an interface; app still works | 🔔 button schedules and shows a preview | ☐ |
| `NotesListViewModelTest` | 9 green | ☐ |
| `CookieCounterTest` (emulator) | 3 green | ☐ |
| `NoteCardTest` + `NotesListScreenTest` (emulator) | 10 green | ☐ |
| Break something on purpose | The right test turns red ❌, then green again ✅ | ☐ |

---

## 27.22 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| `assertEquals(actual, expected)` (wrong order) | The fail message says "expected" for the **wrong** value — confusing! | Always `assertEquals(expected, actual)` |
| `assertEquals(2.5, result)` for `Double`s | Fails or warns: decimals are never perfectly exact | Add a tolerance: `assertEquals(2.5, result, 0.0001)` |
| Forgot `@Test` | The function is silently **ignored** — "0 tests" | Add `@Test` above every test function |
| A UI test in the `test` folder (or a unit test in `androidTest`) | Won't compile / can't find Compose test classes | UI and Android tests → `androidTest`; pure Kotlin tests → `test` |
| `Log.d(...)` inside code tested by a local unit test | *"Method d in android.util.Log not mocked"* | Keep logic free of Android classes, or wrap the log; or add `testOptions { unitTests.isReturnDefaultValues = true }` in `build.gradle.kts` |
| No `MainDispatcherRule` in a ViewModel test | *"Module with the Main dispatcher had failed to initialize"*, or random results | Add `@get:Rule val mainDispatcherRule = MainDispatcherRule()` |
| Creating the ViewModel as a **property** of the test class | It's built **before** the rule sets up Main → strange failures | Create it **inside** the test or in `@Before` |
| `stateIn(WhileSubscribed)` test without a watcher | `uiState.value` never changes from the initial value | `backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) { viewModel.uiState.collect() }` |
| Collecting forever with a normal `launch` inside `runTest` | The test **never ends** (or fails after a long wait) | Use **`backgroundScope.launch`** — it's cancelled when the test ends |
| Testing with real `delay`s outside `runTest` | Slow tests 🐌 | Put the test body in `runTest { }` — virtual time ⏩ |
| Hard-coded `Dispatchers.Default`/`IO` in the code under test | The test can't control that work | Pass the dispatcher in through the constructor (Challenge 2) |
| Tests that depend on each other (shared objects, order) | Pass alone, fail together (or the opposite) | Fresh objects for **every** test |
| `onNodeWithText(...)` finds 2 nodes | *"Expected exactly '1' node but found '2'"* | Use a `testTag`, or `onAllNodesWithText(...)[0]` |
| A UI test can't find something | *"Failed: assertExists. Reason: Expected exactly '1' node but could not find any"* | `onRoot().printToLog("TREE")` and read the tree; try `useUnmergedTree = true` |
| Instrumented tests won't start | *"No connected devices"* | Start the emulator first 📱 |
| Forgot breakpoints after debugging | The app keeps stopping in debug mode | Run → View Breakpoints → remove them |

---

## 27.23 Summary — What You Learned 🎓

| Topic | Key points |
|---|---|
| **Logcat** 📔 | `Log.d/i/w/e(TAG, message)`; filters `package:mine`, `tag:`, `level:`, `is:crash` |
| **Stack traces** 📜 | Line (B) = **what**; first line with **your** package = **where**; read the last `Caused by:` |
| **Debugger** 🐞 | Breakpoints 🔴, Debug (Shift+F9), Step Over F8 / Into F7 / Out Shift+F8, Resume F9, Evaluate Alt+F8; conditional breakpoints, logpoints, Attach |
| **Detective tools** 🧰 | Layout Inspector, Database/Network/Background Task Inspectors, Profiler |
| **Unit tests** 🧪 | `test` folder, JUnit, `@Test`, `assertEquals(expected, actual)`, AAA, test the **edges**, Red → Green → Clean |
| **Coroutine tests** ⏱️ | `kotlinx-coroutines-test`, `runTest`, virtual time, `advanceTimeBy`, `advanceUntilIdle`, `currentTime` |
| **ViewModel tests** 🧠 | `MainDispatcherRule`, call the constructor yourself (no Hilt!), a **watcher** for `stateIn(WhileSubscribed)` |
| **Fakes** 🎭 | Same interface, in memory, can **spy**; hard-to-test code → add an **interface** (`ReminderScheduler`) |
| **Compose UI tests** 🤖 | `androidTest`, `createComposeRule`, `setContent`, finders/actions/assertions, `testTag`, the semantics tree, `printToLog` |
| **Hilt tests** 🔭 | `@HiltAndroidTest`, `HiltAndroidRule`, `HiltTestRunner`, `@TestInstallIn(replaces = …)` |
| **Crashes** 💥 | The big table in 27.19 |

🎉 You're now a **bug detective** 🕵️ **and** a **robot builder** 🤖. Most beginner developers skip testing — you didn't. That makes you **stand out**! ⭐

---

## 27.24 Practice Time 🏋️

### Task 1: Search diary 📔
In MyFirstApp's `FruitViewModel.onQueryChange`, write a `Log.d` with the new text. Type "app" in the Fruit Finder. Filter Logcat so you see **only** these messages.

### Task 2: PIN rules 🔢
Write a function `isValidPin(pin: String): Boolean` in MyFirstApp: a valid PIN has **exactly 4** characters, and **all** are digits. Then write a test class with **at least 5** tests — think about the **edges**!

### Task 3: Stopwatch buttons ⏱️
In Background Lab, `StopwatchUiState` has `canLap` and `canReset`. Write tests for them: a running stopwatch can lap but not reset; a paused one with time can reset; a fresh one can do neither.

### Task 4: A favorite on the "All" tab 🍝
In `RecipeListViewModelTest`, write a test: on the **All** tab (`onlyFavorites = false`), toggling Pasta (id 2) makes Pasta's `isFavorite` **true**, and the list still has 3 recipes.

### Task 5: Nothing found 🔍
In `NotesListViewModelTest`, write a test: searching for `"pizza"` gives **no** notes, `isSearching` is `true`, but the repository still has **3** notes.

### Task 6: Reset the cookies 🍪
In `CookieCounterTest`, write a test: add 5 cookies, tap **Reset**, then check the count is 0, the button is **enabled** again, and the "enough" message is **gone**.

---

### Answers

**Task 1:**

```kotlin
import android.util.Log

fun onQueryChange(newQuery: String) {
    Log.d("FruitFinder", "Search text: \"$newQuery\"")
    _query.value = newQuery
}
```

Filter: **`package:mine tag:FruitFinder`**. You'll see `"a"`, `"ap"`, `"app"` — one message per letter. ⌨️

> ⚠️ Now `FruitViewModelTest` (a **local** test) **fails** with *"Method d in android.util.Log not mocked"*! 😮 This is the mistake from 27.22. Remove the `Log.d` line when you're done with the task — or add `testOptions { unitTests.isReturnDefaultValues = true }` inside `android { }` in `build.gradle.kts`.

**Task 2:**

```kotlin
// ScoreMath.kt (or a new file)
fun isValidPin(pin: String): Boolean =
    pin.length == 4 && pin.all { it.isDigit() }
```

```kotlin
package com.example.myfirstapp

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class PinTest {

    @Test
    fun fourDigits_isValid() {
        assertTrue(isValidPin("1234"))
    }

    @Test
    fun zeros_areValid() {
        assertTrue(isValidPin("0000"))
    }

    @Test
    fun threeDigits_isNotValid() {
        assertFalse(isValidPin("123"))
    }

    @Test
    fun fiveDigits_isNotValid() {
        assertFalse(isValidPin("12345"))
    }

    @Test
    fun letters_areNotValid() {
        assertFalse(isValidPin("12a4"))
    }

    @Test
    fun empty_isNotValid() {
        assertFalse(isValidPin(""))
    }

    @Test
    fun spaces_areNotValid() {
        assertFalse(isValidPin("12 4"))
    }
}
```

`all { ... }` is `true` only if **every** character passes (Chapter 3). The edges: empty, too short, too long, letters, spaces, and zeros (a number that "looks small" but is a fine PIN).

**Task 3:**

```kotlin
package com.example.backgroundlab

import com.example.backgroundlab.ui.stopwatch.StopwatchUiState
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class StopwatchUiStateTest {

    @Test
    fun fresh_cannotLapOrReset() {
        val state = StopwatchUiState()

        assertFalse(state.canLap)
        assertFalse(state.canReset)
    }

    @Test
    fun running_canLap_butNotReset() {
        val state = StopwatchUiState(elapsedMillis = 5_000L, isRunning = true)

        assertTrue(state.canLap)
        assertFalse(state.canReset)
    }

    @Test
    fun pausedWithTime_canReset_butNotLap() {
        val state = StopwatchUiState(elapsedMillis = 5_000L, isRunning = false)

        assertFalse(state.canLap)
        assertTrue(state.canReset)
    }
}
```

No coroutines and no ViewModel needed — `StopwatchUiState` is a plain data class with calculated values. The **easiest** kind of test! 🍰

**Task 4:**

```kotlin
@Test
fun allTab_toggleFavorite_marksPastaAsFavorite() = runTest {
    val viewModel = RecipeListViewModel(repository = fakeRepository, onlyFavorites = false)
    backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
        viewModel.uiState.collect()
    }

    viewModel.onToggleFavorite(2)

    val recipes = viewModel.uiState.value.recipes
    assertEquals(3, recipes.size)
    assertTrue(recipes.first { it.id == 2 }.isFavorite)
}
```

`first { ... }` finds the first recipe that matches (Chapter 3).

**Task 5:**

```kotlin
@Test
fun search_noMatch_showsNothing_butKeepsNotes() = runTest {
    watchUiState()

    viewModel.onQueryChange("pizza")

    assertTrue(viewModel.uiState.value.notes.isEmpty())
    assertTrue(viewModel.uiState.value.isSearching)
    assertEquals(3, notesRepository.allNotes.size)
}
```

The screen uses `isSearching` to choose *"No notes match…"* instead of *"No notes yet"* — and the spy proves no note was lost. 🕵️

**Task 6:**

```kotlin
import androidx.compose.ui.test.assertIsEnabled

@Test
fun reset_goesBackToZero() {
    showCounter()
    repeat(MAX_COOKIES) {
        composeTestRule.onNodeWithText("Add cookie 🍪").performClick()
    }

    composeTestRule.onNodeWithText("Reset").performClick()

    composeTestRule.onNodeWithTag("cookieCount").assertTextEquals("Cookies: 0")
    composeTestRule.onNodeWithText("Add cookie 🍪").assertIsEnabled()
    composeTestRule.onNodeWithText("That's enough cookies! 🛑").assertDoesNotExist()
}
```

Only `assertIsEnabled` needs a new import. `assertDoesNotExist()` is built into the node object, so it needs none.

---

## 27.25 Challenges 🚀

### Challenge 1: Test the note editor 📝 ⭐⭐⭐
`NoteEditorViewModel` needs a `PhotoStorage` (a class that uses files and a `Context`). Make `PhotoStorage` an **interface** with a real class behind it (exactly like `ReminderScheduler` in 27.15), write a `FakePhotoStorage`, and test: a new note is **not** saved when it's empty; a note with a title **is** saved; editing an existing note updates it. Give the ViewModel a `SavedStateHandle(mapOf(...))` with the keys it reads. (If your ViewModel reads the route with `toRoute()`, a local test may need Android's `Bundle` — then run this test in `androidTest` instead.)

### Challenge 2: Test the "Done" path ✅ ⭐⭐⭐
In Background Lab, give `FakeDownloader` a constructor parameter `private val workDispatcher: CoroutineDispatcher = Dispatchers.Default`, use it in `checkFile()`, and let `DownloadViewModel` receive the downloader in its constructor (with a default, so the app doesn't change). In the test, pass `StandardTestDispatcher(testScheduler)` and check that the status finally becomes `Done`. (Hint: make the loop shorter in tests with another parameter, for example `checkLoops: Int = 30_000_000`.)

### Challenge 3: Test the Quiz 🧠 ⭐⭐⭐
Write a fake for the Quiz app's best-score repository (Chapter 21) and test `QuizViewModel`: answering everything correctly gives the full score, and the best score is saved **only** when it's better than the old one.

### Challenge 4: Test the database itself 🗄️ ⭐⭐⭐
In the Notes app's `androidTest`, create a **real** Room database that lives only in memory:
`Room.inMemoryDatabaseBuilder(context, NotesDatabase::class.java).build()` (get `context` with `ApplicationProvider.getApplicationContext()`). Test `NoteDao`: insert 3 notes, then check that the search query finds the right ones (`.first()` on the `Flow`). Close the database in `@After`.

### Challenge 5: Bug hunt 🐛 ⭐⭐
Pick **any** app from this book. Use it like a **naughty** user 😈: type emojis, very long text, empty fields, rotate during loading, turn off the internet, tap buttons super fast. When you find a bug: write a test that shows it (🔴), fix it (🟢), and keep the test.

---

## 27.26 What Is Next?

🎉 Your apps now have **robot guards** 🤖🛡️ — and you know how to find bugs like a **detective** 🕵️ when something goes wrong.

There's only **one** step left: sharing your app with the **world**! 🌍 In the **last chapter**, **Chapter 28: Publishing Your App on Google Play**, you will learn:

- Making a beautiful **app icon** 🎨 (adaptive icons)
- **Version numbers** — `versionCode` and `versionName` 🔢
- Making a **release build**: smaller and faster with **R8**, and without your debug logs 📦
- **Signing** your app with your own **key** 🔑 — and why you must **never lose it**
- The **Android App Bundle** (`.aab`) 🎁
- The **Google Play Console**: creating your app, the **store listing** (screenshots, description), the privacy policy, and content rating 🏪
- **Testing tracks** — sharing with friends before everyone 👫
- Sending **updates** 🔁

**Fantastic work finishing Chapter 27! 🎉 You don't just build apps — you build apps you can TRUST. 🧪🔍✅**
