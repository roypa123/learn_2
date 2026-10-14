# Chapter 18: Doing Things in the Background — Coroutines and Flow ⚡🌊

> **What you will learn in this chapter**
>
> 1. Why long tasks **freeze** an app 🥶 (and see it happen!)
> 2. **Threads** — the workers inside your app 👷
> 3. **Coroutines** — tasks that can **pause** and **continue** ⏸️▶️
> 4. **`suspend`** functions — what that word really means
> 5. `launch`, `delay`, `async`, `await` — doing things **in order** or **at the same time**
> 6. **Jobs** and **cancelling** 🛑
> 7. **Dispatchers** — choosing the right worker (`Main`, `IO`, `Default`) and `withContext`
> 8. **Errors** in coroutines (`try` / `catch`) ⚠️
> 9. Coroutines in Android: `viewModelScope`, `rememberCoroutineScope`, **`LaunchedEffect`**
> 10. **`Flow`** — a stream of values over time 🌊
> 11. Flow **operators**: `map`, `filter`, `take`, `onEach`, `catch`, **`combine`**
> 12. `StateFlow` vs `Flow`, and **`stateIn`** — fully explained at last!
> 13. 🛠️ Two projects: a **Stopwatch** ⏱️ and a **fake download** with a progress bar ⬇️
>
> **Time needed:** about 5–6 hours. Take breaks! ☕ This chapter has **new ideas**, not just new code.
>
> **What you need to know:** Chapters 1–17, especially 8 (State), 15 (ViewModel), and 16 (`map` + `stateIn`).

---

## 18.1 The Problem: A Frozen App 🥶

Since Chapter 10 we wrote some strange code without really explaining it:

```kotlin
scope.launch { listState.animateScrollToItem(0) }        // Chapter 10
scope.launch { snackbarHostState.showSnackbar("Saved") } // Chapter 11
.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ...) // Chapter 16
```

We always said "**Chapter 18** will explain this." 😄 **This is Chapter 18!** Let's start with **why** all this exists.

### Let's freeze an app on purpose 🧪

Open your practice project **MyFirstApp**. Put this Composable in `MainActivity.kt` and call it inside `setContent { MyFirstAppTheme { ... } }`:

```kotlin
@Composable
fun FreezeDemo() {
    var message by remember { mutableStateOf("Tap a button") }   // (1)
    var taps by remember { mutableIntStateOf(0) }                 // (2)

    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(message, style = MaterialTheme.typography.headlineMedium)
        Text("Taps: $taps")

        Button(onClick = { taps++ }) {                              // (3)
            Text("Tap me 👆")
        }

        Button(onClick = {
            message = "Loading… ⏳"                                  // (4)
            Thread.sleep(5_000L)                                     // (5) ❌
            message = "Done! ✅"                                     // (6)
        }) {
            Text("Load (the WRONG way) 🥶")
        }
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `message` | A text that changes (Chapter 8). |
| 2 | `taps` | Counts taps, so we can see if the app **answers** us. |
| 3 | `taps++` | Each tap adds 1. A **quick** job. |
| 4 | `message = "Loading… ⏳"` | We **want** the screen to say "Loading…". |
| 5 | `Thread.sleep(5_000L)` | "**Stop everything** and wait 5 seconds." 😴 This pretends to be a slow job, like downloading. `5_000L` = 5000 milliseconds = 5 seconds. (`_` makes big numbers easier to read; `L` means `Long`.) |
| 6 | `message = "Done! ✅"` | After waiting, say "Done!". |

**Run it** and try this:

1. Tap **"Tap me"** a few times. The number goes up. 👍
2. Tap **"Load (the WRONG way)"**.
3. Quickly tap **"Tap me"** again many times.

**What happens?** 😱

- The screen **never** shows "Loading… ⏳"!
- The app is **frozen** for 5 seconds. Your taps do **nothing**. The button ripple doesn't even move.
- After 5 seconds, it suddenly shows "Done! ✅" (and maybe your taps are counted all at once).
- If you tapped during the freeze, Android may show a scary box: **"MyFirstApp isn't responding"** with **Close app** / **Wait**. This is called an **ANR** (**A**pplication **N**ot **R**esponding). 💀

> 💡 If you don't see the ANR box, change `5_000L` to `10_000L` and tap many times while it's frozen.

Real users **hate** this. Many will **uninstall** the app. And Google Play **counts** ANRs — too many, and your app is shown to fewer people. 📉

So **why** did it freeze? To understand, we need to meet the **workers** inside your app.

---

## 18.2 Threads — The Workers Inside Your App 👷

Imagine a small **restaurant** 🍽️ with only **one waiter**.

The waiter does **everything** in the dining room:
- takes orders 📝
- brings food 🍝
- cleans tables 🧽
- answers customers' questions 🙋

As long as every job is **quick**, the restaurant works fine.

But what if the waiter goes to the kitchen and **stands there for 5 minutes** waiting for a cake to bake? 🎂
Nobody takes orders. Nobody brings food. Customers wave their hands… nothing. The restaurant is **frozen**. 🥶

In your app:

| Restaurant | App |
|---|---|
| The restaurant | Your app |
| A worker | A **thread** |
| The one waiter in the dining room | The **main thread** (also called the **UI thread**) |
| Taking orders, bringing food | Drawing the screen, answering taps |
| Standing in the kitchen waiting for a cake | `Thread.sleep(5_000)` — or a slow download |

**A thread** = a worker that does jobs **one after another**.

**The main thread** = the special worker that **draws the screen** and **handles taps**. There is only **one**.

### How busy is the main thread? ⏱️

The screen is redrawn about **60 times per second** (on some phones 90 or 120). That means the main thread has about **16 milliseconds** to prepare each picture. 16 ms is **very** short!

```
Main thread:  [draw][tap][draw][draw][tap][draw] ...   ← quick jobs, smooth app 😊
Main thread:  [draw][ 😴😴😴 sleeping 5 seconds 😴😴😴 ][draw] ← frozen app 🥶
```

> 🎯 **The Golden Rule of Android:**
> **Never** make the main thread **wait** for anything slow.
> Slow things = internet ⬇️, database 🗄️, big files 📁, big calculations 🧮, timers ⏱️.

### The old way: more threads 🧵

Long ago, Android developers created **extra threads** by hand (a second waiter for the kitchen). It worked, but:

- Threads are **expensive** (each one uses a lot of memory). 💸
- Passing results **back** to the main thread was complicated. 🤯
- Forgetting to **stop** threads caused crashes and memory leaks. 💧

Today we use something **much** better: **coroutines**. 🎉

---

## 18.3 Coroutines — Tasks That Can Pause ⏸️▶️

A **coroutine** is a **task** that can **pause** in the middle, and **continue later** — **without** blocking its worker.

### The bookmark idea 📖

You are reading a book. Your mom calls: "Come and eat!" 🍲

- ❌ **Blocking** way: you keep holding the book open and **stand there** without moving until… forever. You can't eat.
- ✅ **Coroutine** way: you put a **bookmark** 🔖 in the book, close it, go eat, and later **continue from the bookmark**.

A coroutine does the same:

1. It runs until it must **wait** (for the internet, a timer, …).
2. It puts in a **bookmark** 🔖 and **steps aside**.
3. The worker (thread) is now **free** to do other jobs — like drawing the screen! 🎨
4. When the waiting is over, the coroutine **continues from the bookmark**.

### The waiter with a buzzer 📟

Back to our restaurant. This time, the waiter gives the cake order to the kitchen and gets a **buzzer**. 📟
The waiter goes back to serving customers. When the cake is ready, the buzzer **beeps** and the waiter brings the cake.

**One waiter, many tasks, nobody waits. 😎** That's coroutines.

| Word | Meaning |
|---|---|
| **Coroutine** | A task that can **pause** (without blocking) and **continue** later. |
| **Suspend** | To **pause** a coroutine (put in the bookmark 🔖). |
| **Resume** | To **continue** a coroutine from where it paused. |
| **Block** | To make the **whole worker** wait. ❌ Bad on the main thread. |

> 💡 Coroutines are **cheap**. You can start **100,000** coroutines on a phone easily. 100,000 threads would crash it. 💥

---

## 18.4 Your First Coroutine 👶

Let's play with coroutines in the **Kotlin Playground** first (from Chapter 2): go to **play.kotlinlang.org**. The Playground already includes the coroutines library. ✅

Type this:

```kotlin
import kotlinx.coroutines.*                         // (1)

fun main() = runBlocking {                          // (2)
    println("1. Start")

    launch {                                        // (3)
        delay(1_000L)                               // (4)
        println("3. Hello from the coroutine! 👋")
    }

    println("2. Main keeps going")                  // (5)
}
```

**Output:**

```
1. Start
2. Main keeps going
3. Hello from the coroutine! 👋      ← after 1 second
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `import kotlinx.coroutines.*` | Bring in **all** the coroutine tools. `*` means "everything in this package". |
| 2 | `fun main() = runBlocking { ... }` | `runBlocking` makes a **coroutine world** 🌍 and **waits** until every coroutine inside it finishes. We use it **only** in the Playground and in tests. **Never** in an app — it **blocks** (that's in its name!). |
| 3 | `launch { ... }` | **Start a new coroutine**. "Do this task — and don't wait for it, I'll keep going." 🚀 |
| 4 | `delay(1_000L)` | **Pause this coroutine** for 1 second 🔖. The worker is **free** in the meantime. |
| 5 | `println("2. ...")` | Runs **right away** — `launch` didn't wait! |

**Why is "2" printed before "3"?** 🤔

Because `launch` says "start this task" and **immediately** goes to the next line. The new coroutine waits 1 second, and then prints "3".

### `delay` vs `Thread.sleep` — the big difference 😴 vs 🔖

| | `Thread.sleep(1000)` | `delay(1000)` |
|---|---|---|
| What waits? | The **whole thread** (worker) | Only **this coroutine** |
| Can the thread do other work? | ❌ No — it's asleep | ✅ Yes! |
| On the main thread | 🥶 Frozen app | 😊 Smooth app |
| Can be used | Anywhere | Only inside a **coroutine** |

### Many coroutines, one worker 🤹

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    launch {
        delay(300L)
        println("🐢 Turtle arrives (300 ms)")
    }
    launch {
        delay(100L)
        println("🐇 Rabbit arrives (100 ms)")
    }
    launch {
        delay(200L)
        println("🐕 Dog arrives (200 ms)")
    }
    println("🏁 The race started!")
}
```

**Output:**

```
🏁 The race started!
🐇 Rabbit arrives (100 ms)
🐕 Dog arrives (200 ms)
🐢 Turtle arrives (300 ms)
```

All three coroutines wait **at the same time**, on **one** thread. The whole program takes about **300 ms**, not 600 ms. ⚡

---

## 18.5 `suspend` Functions — "This Might Pause" ⏸️

`delay` is a special kind of function: a **suspend function**. It **can pause** the coroutine that calls it.

You can write your own with the word **`suspend`**:

```kotlin
import kotlinx.coroutines.*

suspend fun makeTea(): String {                     // (1)
    println("Boiling water... 💧")
    delay(2_000L)                                   // (2)
    println("Adding tea leaves... 🍃")
    delay(1_000L)
    return "a cup of tea ☕"                         // (3)
}

fun main() = runBlocking {
    println("I want tea!")
    val tea = makeTea()                             // (4)
    println("Here is $tea")
}
```

**Output:**

```
I want tea!
Boiling water... 💧
Adding tea leaves... 🍃      ← after 2 seconds
Here is a cup of tea ☕       ← after 1 more second
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `suspend fun makeTea(): String` | A function that **may pause** while it works. It still **returns** a value at the end, like a normal function. |
| 2 | `delay(2_000L)` | Pause **here** for 2 seconds. Only allowed because `makeTea` is `suspend`. |
| 3 | `return "a cup of tea ☕"` | Give back the result. |
| 4 | `val tea = makeTea()` | Call it **like a normal function**! The coroutine pauses inside, and when `makeTea` is done, `tea` gets the result. 😍 |

> 😍 **The magic:** The code **looks** simple and step-by-step, like normal code. But it **never blocks** the thread. No buzzers, no callbacks — just normal-looking code.

### The one rule of `suspend` 📏

> A `suspend` function can **only** be called from:
> - **another `suspend` function**, or
> - **inside a coroutine** (`launch { }`, `runBlocking { }`, `LaunchedEffect { }`, …).

If you break this rule, Android Studio shows a red error:

```
Suspend function 'makeTea' should be called only from a coroutine or another suspend function
```

**You saw this before!** In Chapter 10, `animateScrollToItem` is a suspend function (scrolling **takes time** ⏳). That's why we needed `scope.launch { ... }` around it. And in Chapter 11, `showSnackbar` is a suspend function — it **waits** until the Snackbar disappears and then **returns** whether the user tapped "Undo". 🤯 Now it all makes sense!

### How to recognise suspend calls in Android Studio 👀

Look at the **left edge** of the code (the "gutter"). Next to each line that calls a suspend function, Android Studio shows a small **arrow-with-a-wave icon** ⤵️. It means: "**this line may pause**".

### Think of `suspend` as a label 🏷️

| Function | Label |
|---|---|
| `fun add(a: Int, b: Int)` | "I finish **immediately**." ⚡ |
| `suspend fun download()` | "I **might take a while**. Call me from a coroutine." ⏳ |

> ⚠️ `suspend` does **not** make code run in the background by itself! It only means "**can pause**". Where the code runs is decided by **Dispatchers** (section 18.8).

---

## 18.6 In Order, or At the Same Time? 🔢 vs 🤹

### In order (one after another)

Inside one coroutine, code runs **in order**, top to bottom — even with suspend functions.

```kotlin
import kotlinx.coroutines.*
import kotlin.system.measureTimeMillis             // (1)

suspend fun boilWater(): String {
    delay(2_000L)
    return "hot water 💧"
}

suspend fun toastBread(): String {
    delay(1_000L)
    return "toast 🍞"
}

fun main() = runBlocking {
    val time = measureTimeMillis {                  // (2)
        val water = boilWater()                     // 2 seconds...
        val bread = toastBread()                    // ...then 1 more second
        println("Breakfast: $water and $bread")
    }
    println("It took $time ms")
}
```

**Output:**

```
Breakfast: hot water 💧 and toast 🍞
It took 3015 ms
```

(Your number will be **a little** different, like 3008 or 3021. That's normal.)

| # | Code | Meaning |
|---|---|---|
| 1 | `import kotlin.system.measureTimeMillis` | A helper that **measures** how long some code takes. ⏱️ |
| 2 | `measureTimeMillis { ... }` | Runs the code in `{ }` and **returns** the time in milliseconds. |

2 seconds + 1 second = **3 seconds**. But wait… a real person would put the **bread in the toaster while the water is boiling**! 🧠

### At the same time: `async` and `await` 🤹

```kotlin
fun main() = runBlocking {
    val time = measureTimeMillis {
        val water = async { boilWater() }           // (1) start boiling
        val bread = async { toastBread() }          // (2) start toasting — right away!
        println("Breakfast: ${water.await()} and ${bread.await()}")   // (3)
    }
    println("It took $time ms")
}
```

**Output:**

```
Breakfast: hot water 💧 and toast 🍞
It took 2012 ms
```

| # | Code | Meaning |
|---|---|---|
| 1 | `async { boilWater() }` | **Start** a coroutine that will **give back a result** later. It returns a "**promise**" box 📦 (its type is `Deferred<String>`). |
| 2 | `async { toastBread() }` | Start the toast **now**, while the water is still boiling. |
| 3 | `water.await()` | "**Wait** for the result in this box, and give it to me." ⏳ Pauses (doesn't block!) until it's ready. |

Only **2 seconds** now — the longest job. ⚡

### `launch` vs `async` — which one? 🤔

| | `launch { }` | `async { }` |
|---|---|---|
| Gives back a **result**? | ❌ No | ✅ Yes — get it with `.await()` |
| Returns | a `Job` 🎫 | a `Deferred<T>` 📦 (a `Job` with a result) |
| Use it for | "Go **do** this." (save, update, animate) | "Go **get** this, I need the answer." (two downloads at once) |
| How often in apps | **Very** often ⭐ | Sometimes |

> 💡 **Beginner tip:** Use **`launch`** almost always. Use **`async`** only when you need **two or more results at the same time**.

---

## 18.7 Jobs and Cancelling 🛑

`launch` gives back a **`Job`** 🎫 — like a ticket for that task. With the ticket you can **check** on the task or **cancel** it.

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    val job = launch {                              // (1)
        repeat(10) { i ->                           // (2)
            println("Working... $i 🔨")
            delay(500L)
        }
        println("All 10 done!")                     // (3)
    }

    delay(1_300L)                                   // (4)
    println("Stop! 🛑")
    job.cancel()                                    // (5)
    job.join()                                      // (6)
    println("The job is cancelled: ${job.isCancelled}")   // (7)
}
```

**Output:**

```
Working... 0 🔨
Working... 1 🔨
Working... 2 🔨
Stop! 🛑
The job is cancelled: true
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `val job = launch { ... }` | Start a task and **keep its ticket** 🎫 in `job`. |
| 2 | `repeat(10) { i -> ... }` | Do this 10 times; `i` is 0, 1, 2, … 9 (Chapter 2). |
| 3 | `println("All 10 done!")` | Never printed — we cancel before! |
| 4 | `delay(1_300L)` | The main code waits 1.3 seconds. Meanwhile the job prints 0 (at 0 s), 1 (0.5 s), 2 (1.0 s). |
| 5 | `job.cancel()` | "**Stop** that task, please." The job is **paused** in `delay`, so it stops **there**. |
| 6 | `job.join()` | **Wait** until the job has really finished stopping. (Like waiting for the door to close.) |
| 7 | `job.isCancelled` | `true` — it was cancelled. |

### Useful things on a `Job` 🎫

| Code | Meaning |
|---|---|
| `job.cancel()` | Stop it. 🛑 |
| `job.join()` | Wait (suspend) until it is finished. |
| `job.isActive` | `true` while it is still running. 🏃 |
| `job.isCompleted` | `true` when it is finished (normally **or** cancelled). 🏁 |
| `job.isCancelled` | `true` if it was cancelled. |

### How does cancelling actually work? 🤔

Cancelling is **polite**. 🙇 It doesn't kill the coroutine instantly. It puts up a **sign** 🪧 "Please stop". The coroutine sees the sign **the next time it pauses** — for example in `delay()`. Then it stops.

All the suspend functions from `kotlinx.coroutines` (`delay`, `await`, `join`, …) **check the sign**. ✅

But what if your code **never pauses**? 🤨

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    val job = launch(Dispatchers.Default) {         // (1)
        var count = 0L
        while (isActive) {                          // (2)
            count++                                 // counting very fast, never pausing
        }
        println("I counted to $count before I was stopped")
    }

    delay(100L)
    job.cancelAndJoin()                             // (3)
    println("Finished")
}
```

**Output** (your number will be different):

```
I counted to 187340212 before I was stopped
Finished
```

| # | Code | Meaning |
|---|---|---|
| 1 | `launch(Dispatchers.Default)` | Run on a **background** worker (section 18.8 explains). |
| 2 | `while (isActive)` | `isActive` = "has nobody asked me to stop?" We **check the sign** 🪧 ourselves on every loop. |
| 3 | `job.cancelAndJoin()` | `cancel()` + `join()` in one call. |

> ⚠️ If you write `while (true)` instead of `while (isActive)`, the loop **never** checks the sign and **never stops**. The program runs forever! 😱 (Press the stop button in the Playground.)
>
> **Rule:** In a long loop with **no** suspend calls, check **`isActive`** (or call **`ensureActive()`**, which stops the coroutine if it was cancelled).

### The coroutine family 👨‍👩‍👧 — "structured concurrency"

Coroutines started **inside** another coroutine are its **children**.

```kotlin
val parent = launch {
    launch { /* child 1 */ }
    launch { /* child 2 */ }
}
```

Family rules:

1. 👨‍👩‍👧 A parent **waits** for all its children before it is finished.
2. 🛑 **Cancel the parent → all children are cancelled** too.
3. 💥 If a child **fails** (crashes), the parent and the other children are cancelled.

This sounds like a small detail, but it is **super** important for Android:

> 🧠 `viewModelScope` is the **parent** of every coroutine your ViewModel starts. When the ViewModel is **cleared** (the screen is gone for good), `viewModelScope` is **cancelled** — and **all** its coroutines stop **automatically**. No forgotten tasks, no leaks, no crashes! 🎉

This "family" idea has a fancy name: **structured concurrency**. You don't need to remember the name — just the rules.

---

## 18.8 Dispatchers — Choosing the Right Worker 👷

Remember: **`suspend` doesn't decide WHERE code runs.** A **dispatcher** decides **which thread(s)** a coroutine uses.

Think of three teams of workers in our restaurant:

| Dispatcher | Restaurant team | Use it for | Examples |
|---|---|---|---|
| **`Dispatchers.Main`** | 🤵 The **one waiter** in the dining room | Updating the **screen** and **quick** work | Changing state, showing a Snackbar |
| **`Dispatchers.IO`** | 📦 **Delivery** people — lots of them, mostly **waiting** | **Waiting** for things outside the app | Internet, database, reading/writing files |
| **`Dispatchers.Default`** | 👨‍🍳 **Cooks** — a few, always **busy** with their hands | **Heavy calculations** | Sorting 100,000 items, image filters, checking big files |

> 💡 `IO` has **many** workers (because they spend most of their time **waiting**). `Default` has about **as many workers as the phone has CPU cores** (because they are always **working hard**).

### Switching workers: `withContext` 🔀

`withContext(dispatcher) { ... }` = "Run **this block** on that team, then **come back** with the result."

```kotlin
import kotlinx.coroutines.*

fun isPrime(n: Int): Boolean {                      // (1)
    if (n < 2) return false
    var divisor = 2
    while (divisor * divisor <= n) {
        if (n % divisor == 0) return false
        divisor++
    }
    return true
}

suspend fun countPrimes(upTo: Int): Int = withContext(Dispatchers.Default) {   // (2)
    var count = 0
    for (n in 2..upTo) {
        if (isPrime(n)) count++
    }
    count                                           // (3)
}

fun main() = runBlocking {
    println("Counting... 🧮")
    val primes = countPrimes(2_000_000)             // (4)
    println("There are $primes prime numbers up to 2 million!")
}
```

**Output** (after a second or so):

```
Counting... 🧮
There are 148933 prime numbers up to 2 million!
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `fun isPrime(n: Int)` | A normal function: is `n` a prime number? (A prime can only be divided by 1 and itself: 2, 3, 5, 7, 11, …) It's just math — **heavy** math when called 2 million times. |
| 2 | `= withContext(Dispatchers.Default) { ... }` | Do the counting on the **cooks** 👨‍🍳 team, not on the waiter. |
| 3 | `count` | The **last line** of the block is its **result** (like a lambda, Chapter 3). `withContext` returns it. |
| 4 | `val primes = countPrimes(...)` | The caller just calls it. It pauses until the cooks are done, then continues. |

### "Main-safe" functions — a very important habit 🛡️

Look at `countPrimes` again. The **function itself** chooses `Dispatchers.Default`. So **anyone** can call it from **anywhere** — even from the main thread — and the app **never freezes**.

This kind of function is called **main-safe**. ✅

> 🎯 **Rule:** A suspend function that does slow work should switch to the right dispatcher **inside itself** with `withContext`. The caller (often the ViewModel) should **not** have to worry about it.

Good news: **Retrofit** (internet, Chapter 19) and **Room** (database, Chapter 22) suspend functions are **already main-safe**. You'll just call them from `viewModelScope.launch { }`. 😎

### Which dispatcher does what by default?

| Where you launch | Default dispatcher |
|---|---|
| `viewModelScope.launch { }` | `Dispatchers.Main` 🤵 |
| `rememberCoroutineScope()` + `launch` | `Dispatchers.Main` 🤵 |
| `LaunchedEffect { }` | `Dispatchers.Main` 🤵 |
| `runBlocking { }` (Playground) | The thread that called it |

Starting on **Main** is good: you can **update the state** directly. Then use `withContext` only for the slow parts.

> 🤔 "Wait — if `viewModelScope` runs on the main thread, how can `delay(5000)` there not freeze the app?"
> Because `delay` **suspends** (bookmark 🔖), it doesn't **block**. The waiter is free while waiting. Only **blocking** code (`Thread.sleep`, heavy loops, old-style file reading) freezes it. That's why heavy work goes to `Default` or `IO`.

---

## 18.9 When Things Go Wrong — Errors in Coroutines ⚠️

The internet can fail. 📶❌ Files can be missing. Inside a coroutine, you handle errors with the normal **`try` / `catch`** (Chapter 3):

```kotlin
import kotlinx.coroutines.*

suspend fun loadHighScore(): Int {
    delay(500L)
    throw IllegalStateException("The server is sleeping 😴")   // (1)
}

fun main() = runBlocking {
    try {                                           // (2)
        val score = loadHighScore()
        println("High score: $score")               // (3)
    } catch (e: IllegalStateException) {            // (4)
        println("Oops! ${e.message}")
    }
    println("The app keeps running 👍")
}
```

**Output:**

```
Oops! The server is sleeping 😴
The app keeps running 👍
```

| # | Code | Meaning |
|---|---|---|
| 1 | `throw IllegalStateException(...)` | Pretend something went wrong. 💥 |
| 2 | `try { ... }` | "Try this code…" |
| 3 | `println("High score: ...")` | **Skipped** — the error jumped straight to `catch`. |
| 4 | `catch (e: IllegalStateException)` | "…and if **this kind** of error happens, do this instead." |

### ⚠️ A sneaky trap: catching cancellation

Remember: **cancelling** works by putting up a sign 🪧. Technically, the sign is a special error called **`CancellationException`**.

If you write `catch (e: Exception)`, you catch **every** error — **including** the "please stop" sign! 😱 The coroutine might then **keep running** after it was cancelled.

```kotlin
// ❌ Risky: catches cancellation too
try {
    downloadSomething()
} catch (e: Exception) {
    showError()
}

// ✅ Better: catch only the errors you expect
try {
    downloadSomething()
} catch (e: IOException) {          // internet/file problems
    showError()
}
```

> 🎯 **Rule:** Catch **specific** errors (`IOException`, `HttpException`, …). If you really must catch `Exception`, put this **first**:
> ```kotlin
> } catch (e: CancellationException) {
>     throw e                       // let cancellation do its job
> } catch (e: Exception) {
>     showError()
> }
> ```

### What if you don't catch an error?

An uncaught error in `launch` **crashes the app** 💥 (just like an error anywhere else). So always think: "**What can go wrong here?**" — and catch it.

---

## 18.10 Coroutines in Android — The Scopes 🏠

In the Playground we used `runBlocking`. In an app, **never**. Instead, every coroutine is started from a **scope**.

**A scope** = a **home** 🏠 for coroutines. When the home is **destroyed**, all coroutines living in it are **cancelled** automatically (the family rules from 18.7).

Android gives you ready-made scopes:

| Scope | Lives as long as… | Use it for |
|---|---|---|
| **`viewModelScope`** ⭐ | the **ViewModel** (survives rotation ✅) | Loading data, saving, timers — **most** work |
| **`rememberCoroutineScope()`** | the **Composable** is on the screen | UI actions after a tap: scroll, Snackbar, bottom sheet |
| **`LaunchedEffect(key) { }`** | the Composable is on the screen (restarts when `key` changes) | Work that should start **by itself** when something **appears** |
| `lifecycleScope` | the **Activity** | Rarely needed in Compose apps |

> ❌ **Never** use `GlobalScope`. It's a home that is **never** destroyed — coroutines there are never cancelled automatically. Android Studio even shows a warning. ⚠️

### Fixing the frozen app — version 1: `rememberCoroutineScope` 🔧

Go back to `FreezeDemo` from 18.1 and change the "Load" button:

```kotlin
@Composable
fun FreezeDemo() {
    var message by remember { mutableStateOf("Tap a button") }
    var taps by remember { mutableIntStateOf(0) }
    val scope = rememberCoroutineScope()                   // (1)

    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(message, style = MaterialTheme.typography.headlineMedium)
        Text("Taps: $taps")

        Button(onClick = { taps++ }) {
            Text("Tap me 👆")
        }

        Button(onClick = {
            scope.launch {                                 // (2)
                message = "Loading… ⏳"
                delay(5_000L)                              // (3) ✅
                message = "Done! ✅"
            }
        }) {
            Text("Load (the RIGHT way) 😊")
        }
    }
}
```

New imports:

```kotlin
import androidx.compose.runtime.rememberCoroutineScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
```

| # | Code | Meaning |
|---|---|---|
| 1 | `val scope = rememberCoroutineScope()` | Get a **home** for coroutines that belongs to this Composable. |
| 2 | `scope.launch { ... }` | Start a coroutine in that home. `onClick` is a normal function (not `suspend`), so we need `launch` to be allowed to call `delay`. |
| 3 | `delay(5_000L)` | **Pauses** the coroutine. The main thread is **free**! |

**Run it.** Now:
- "Loading… ⏳" **appears** right away. ✅
- "Tap me" **still works** during the 5 seconds. ✅
- After 5 seconds: "Done! ✅". No ANR. 🎉

**But there's a problem left.** Tap "Load", then **rotate** the phone. 🔄 The message goes back to "Tap a button" and "Done!" never comes! 😢

Why? Rotation **destroys** the Composable (Chapter 14). Its scope is destroyed → the coroutine is **cancelled**. And `remember` forgot the message.

### Fixing it properly — version 2: the ViewModel 🧠

Work that must **survive rotation** belongs in the **ViewModel** — in **`viewModelScope`**.

```kotlin
class LoadViewModel : ViewModel() {

    private val _message = MutableStateFlow("Tap the button")
    val message: StateFlow<String> = _message.asStateFlow()

    fun onLoadClick() {
        viewModelScope.launch {                            // (1)
            _message.value = "Loading… ⏳"
            delay(5_000L)                                  // (2)
            _message.value = "Done! ✅"
        }
    }
}

@Composable
fun LoadDemo(viewModel: LoadViewModel = viewModel()) {
    val message by viewModel.message.collectAsStateWithLifecycle()

    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(message, style = MaterialTheme.typography.headlineMedium)
        Button(onClick = viewModel::onLoadClick) {
            Text("Load 😊")
        }
    }
}
```

New imports:

```kotlin
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
```

| # | Code | Meaning |
|---|---|---|
| 1 | `viewModelScope.launch { ... }` | Start a coroutine that lives as long as the **ViewModel**. Rotation doesn't stop it! 🔄✅ |
| 2 | `delay(5_000L)` | Pretend loading. The coroutine pauses; the UI stays smooth. |

**Run it, tap Load, rotate during the 5 seconds.** "Loading… ⏳" stays, and "Done! ✅" still arrives. 🎉

And when the user **leaves** the screen for good (presses Back), the ViewModel is cleared → `viewModelScope` is cancelled → the coroutine stops. No wasted work. 🔋

### Which scope should I use? 🤔

```
Should the work survive rotation, or change the screen's data?
 ├── YES → viewModelScope.launch { }                     ⭐ (most of the time)
 └── NO, it's a pure UI action:
       ├── after a TAP (scroll, snackbar, sheet)  → rememberCoroutineScope()
       └── by ITSELF when something appears      → LaunchedEffect(key) { }
```

---

## 18.11 `LaunchedEffect` — Start Work When Something Appears 🎬

Sometimes work should start **by itself**, without a tap. For example: "Show the screen, then after 2 seconds show a tip." You **can't** call `launch` directly in the body of a Composable — the body runs again on **every** recomposition, so you would start **hundreds** of coroutines! 😱

`LaunchedEffect` solves this:

```kotlin
@Composable
fun TipDemo() {
    var showTip by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {                          // (1)
        delay(2_000L)                               // (2)
        showTip = true
    }

    Column(modifier = Modifier.padding(24.dp)) {
        Text("Welcome! 👋", style = MaterialTheme.typography.headlineMedium)
        if (showTip) {
            Text("💡 Tip: swipe left to delete.")
        }
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `LaunchedEffect(Unit) { ... }` | When this Composable **first appears**, start a coroutine with this code. It runs **once**, even if the screen recomposes 100 times. `Unit` is a key that **never changes** → "run once". |
| 2 | `delay(2_000L)` | We're **inside a coroutine**, so suspend functions are allowed. ✅ |

**Rules of `LaunchedEffect`:**

1. 🎬 **Starts** when the Composable **enters** the screen.
2. 🛑 **Cancelled** when the Composable **leaves** the screen.
3. 🔁 **Restarted** (old one cancelled, new one started) when the **key** changes.

### Using the key: a countdown 🚀

```kotlin
@Composable
fun Countdown() {
    var seconds by remember { mutableIntStateOf(10) }

    LaunchedEffect(seconds) {                       // (1)
        if (seconds > 0) {
            delay(1_000L)
            seconds--                               // (2)
        }
    }

    Text(
        text = if (seconds > 0) "$seconds" else "🚀 Lift off!",
        style = MaterialTheme.typography.displayLarge
    )
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `LaunchedEffect(seconds)` | The key is `seconds`. Every time `seconds` **changes**, the effect **restarts**. |
| 2 | `seconds--` | Changing `seconds` (10 → 9) changes the key → the effect restarts → waits 1 second → 9 → 8 → … → 0. At 0 the `if` is false, so it stops. |

It's like a line of dominoes: each one knocks over the next. 🁢🁢🁢

> 💡 **Choosing the key:** ask "**When should this work start again?**"
> - Never → `Unit` (or `true`)
> - When the user id changes → `LaunchedEffect(userId)`
> - When the message changes → `LaunchedEffect(message)`

### Real use: show a Snackbar when the ViewModel says so 📢

A very common pattern (remember Chapter 15: the ViewModel can't show Snackbars itself, it puts a **message** in the state):

```kotlin
LaunchedEffect(uiState.errorMessage) {
    val message = uiState.errorMessage
    if (message != null) {
        snackbarHostState.showSnackbar(message)     // suspend — fine here!
        viewModel.onErrorShown()                    // tell the ViewModel: "done, clear it"
    }
}
```

Every time a **new** error message arrives, the effect restarts and shows it. ✅

---

## 18.12 `Flow` — A Stream of Values Over Time 🌊

A `suspend` function gives back **one** value, **one time**:

```kotlin
suspend fun getTemperature(): Int    // "It's 21°C." Done.
```

But some things give **many** values **over time**:

- 🌡️ The temperature **every minute**
- ⬇️ Download progress: 10%… 20%… 30%…
- 🗄️ Your notes in the database — a **new list** every time you add one
- ⏱️ A stopwatch: 00:01… 00:02…

For that we use a **`Flow`**: a **stream** of values that arrive **one by one**, over time. 🌊

### Picture it 🖼️

```
suspend fun:   ──────────────▶ 📦                 (one box, then done)

Flow:          ──📦────📦──────📦──📦────▶ ✅      (many boxes over time, then maybe done)
```

Think of a **conveyor belt** in a sushi restaurant 🍣: plates arrive one by one. You **take** each plate as it comes.

- The kitchen putting plates on the belt = **emitting** values (`emit`)
- You taking plates = **collecting** values (`collect`)

### Your first Flow (Playground)

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*                   // (1)

fun countdown(): Flow<Int> = flow {                 // (2)
    for (i in 3 downTo 1) {
        delay(1_000L)
        emit(i)                                     // (3)
    }
}

fun main() = runBlocking {
    println("Get ready...")
    countdown().collect { number ->                 // (4)
        println("$number ⏳")
    }
    println("Go! 🚀")                                // (5)
}
```

**Output:**

```
Get ready...
3 ⏳      ← after 1 second
2 ⏳      ← after 2 seconds
1 ⏳      ← after 3 seconds
Go! 🚀
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `import kotlinx.coroutines.flow.*` | All the Flow tools. |
| 2 | `fun countdown(): Flow<Int> = flow { ... }` | A function that returns a **Flow of Ints**. `flow { }` is the **builder** — the "kitchen" 🧑‍🍳 code that produces values. Notice: `countdown` is **not** a `suspend` function! It only **describes** the stream. |
| 3 | `emit(i)` | "Put this value on the belt." 🍣 |
| 4 | `.collect { number -> ... }` | "**Start** the flow, and run this code for **every** value." `collect` is a suspend function — it pauses until the flow is **finished**. |
| 5 | `println("Go! 🚀")` | Runs only **after** the flow has ended (after 3 seconds). |

### Flows are "cold" 🧊 — nothing happens until you collect

```kotlin
fun main() = runBlocking {
    val myFlow = countdown()       // Nothing happens! No waiting, no numbers.
    println("I made a flow, but nobody is collecting it.")
}
```

**Output:**

```
I made a flow, but nobody is collecting it.
```

A `flow { }` is like a **recipe** 📜. Writing down a recipe doesn't cook any food. The cooking starts only when someone calls **`collect`**. And **every** collector gets its **own** fresh cooking from the start. 🍳

(Android Studio and the Playground may show a yellow warning "*Variable 'myFlow' is never used*". That's fine here.)

---

## 18.13 Flow Operators — Changing the Stream 🔧

**Operators** are functions that take a flow and make a **new**, changed flow. They look **just like** the list functions from Chapter 3! 😍

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

fun main() = runBlocking {
    (1..10).asFlow()                                // (1)
        .filter { it % 2 == 0 }                     // (2)
        .map { it * it }                            // (3)
        .take(3)                                    // (4)
        .collect { println(it) }                    // (5)
}
```

**Output:**

```
4
16
36
```

| # | Code | What comes out | Meaning |
|---|---|---|---|
| 1 | `(1..10).asFlow()` | 1, 2, 3, … 10 | Turn a range into a flow (a quick way to make test flows). |
| 2 | `.filter { it % 2 == 0 }` | 2, 4, 6, 8, 10 | Keep only **even** numbers. |
| 3 | `.map { it * it }` | 4, 16, 36, 64, 100 | **Change** each value (square it). |
| 4 | `.take(3)` | 4, 16, 36 | Only the **first 3**, then **stop** the flow. ✂️ |
| 5 | `.collect { ... }` | — | **Start** everything and print. |

Like a factory line 🏭: each operator is one machine on the belt.

```
1..10 ──▶ [filter even] ──▶ [map square] ──▶ [take 3] ──▶ collect 🖨️
```

> 💡 Operators like `map` and `filter` are **cold** too — they don't do anything until `collect`.

### The most useful operators 🧰

| Operator | Meaning | Example |
|---|---|---|
| `map { }` | Change each value | `.map { "$it°C" }` |
| `filter { }` | Keep only some values | `.filter { it > 0 }` |
| `take(n)` | Only the first `n` values, then stop | `.take(5)` |
| `onEach { }` | **Do something** with each value, but pass it on **unchanged** (great for checking 🔍) | `.onEach { println("Got $it") }` |
| `distinctUntilChanged()` | Skip a value if it's the **same** as the one before | 1, 1, 2, 2, 1 → 1, 2, 1 |
| `catch { }` | **Handle errors** from the flow **above** it | see below |
| `onStart { }` / `onCompletion { }` | Do something at the start / end | Show and hide a loading spinner |
| `flowOn(dispatcher)` | Run the flow **above** it on another dispatcher | `.flowOn(Dispatchers.Default)` |

### `onEach` — peeking at the belt 👀

```kotlin
fun main() = runBlocking {
    flowOf("🍎", "🍌", "🍒")                         // a flow of 3 fixed values
        .onEach { println("Checking $it") }
        .map { "$it is yummy!" }
        .collect { println(it) }
}
```

**Output:**

```
Checking 🍎
🍎 is yummy!
Checking 🍌
🍌 is yummy!
Checking 🍒
🍒 is yummy!
```

Notice the order: each value goes through the **whole** line before the next one starts. 🍎 → 🍎 → 🍌 → 🍌 …

### `catch` — when the kitchen catches fire 🔥

```kotlin
fun riskyFlow(): Flow<Int> = flow {
    emit(1)
    emit(2)
    throw IllegalStateException("The machine broke! 💥")
}

fun main() = runBlocking {
    riskyFlow()
        .catch { error ->                           // (1)
            println("Problem: ${error.message}")
            emit(-1)                                // (2)
        }
        .collect { println("Value: $it") }
    println("Still alive 👍")
}
```

**Output:**

```
Value: 1
Value: 2
Problem: The machine broke! 💥
Value: -1
Still alive 👍
```

| # | Code | Meaning |
|---|---|---|
| 1 | `.catch { error -> ... }` | If the flow **above** throws an error, run this instead of crashing. (And `catch` lets **cancellation** pass through — good! ✅) |
| 2 | `emit(-1)` | Inside `catch` you may even send a **replacement** value. |

### `flowOn` — making a flow main-safe 🛡️

```kotlin
fun primeNumbers(): Flow<Int> = flow {
    for (n in 2..2_000_000) {
        if (isPrime(n)) emit(n)                     // heavy work!
    }
}.flowOn(Dispatchers.Default)                       // all the code ABOVE runs on the cooks 👨‍🍳
```

`flowOn` is to flows what `withContext` is to suspend functions: it moves the **producing** work to another dispatcher. The **collector** still runs where it was (for example on Main, so it can update the screen). ✅

> ⚠️ Don't use `withContext` **inside** `flow { }` around `emit` — you'll get an error. Use `flowOn` instead.

---

## 18.14 `combine` — Mixing Two Flows 🍹

`combine` takes **two (or more) flows** and makes **one** flow. Every time **any** of them sends a new value, `combine` builds a new result from the **latest value of each**.

Like a smoothie blender 🍹: whenever you change the fruit **or** the milk, you get a new smoothie.

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

fun main() = runBlocking {
    val name = MutableStateFlow("Sam")              // (1)
    val age = MutableStateFlow(10)

    val job = launch {
        combine(name, age) { n, a ->                // (2)
            "$n is $a years old"
        }.collect { println(it) }
    }

    delay(100L)
    age.value = 11                                  // (3)
    delay(100L)
    name.value = "Mia"                              // (4)
    delay(100L)
    job.cancel()                                    // (5)
}
```

**Output:**

```
Sam is 10 years old
Sam is 11 years old
Mia is 11 years old
```

| # | Code | Meaning |
|---|---|---|
| 1 | `MutableStateFlow("Sam")` | A flow that **holds a value** (Chapter 15). We compare it to normal flows in 18.15. |
| 2 | `combine(name, age) { n, a -> ... }` | Whenever `name` **or** `age` changes, run this with the **newest** of both. |
| 3 | `age.value = 11` | Age changed → new sentence, with the **latest** name ("Sam"). |
| 4 | `name.value = "Mia"` | Name changed → new sentence, with the **latest** age (11). |
| 5 | `job.cancel()` | StateFlows **never end** by themselves, so this `collect` would wait forever. We cancel it to finish the program. |

> 🎯 In apps, `combine` is **perfect** for screens that depend on **several** things: the search text **and** the sort order **and** the list from the database. You'll use it in 18.16!

---

## 18.15 `StateFlow` vs `Flow`, and `stateIn` — Fully Explained 🧠

You've used `StateFlow` since Chapter 15. Now let's see how it's **different** from a normal `Flow`.

| | `Flow` (from `flow { }`) | `StateFlow` |
|---|---|---|
| Picture | A **recipe** 📜 — cooked fresh for each collector | A **scoreboard** 🏟️ — everyone sees the same current score |
| Has a **current value**? | ❌ No | ✅ Always — read it with `.value` |
| Works when nobody collects? | ❌ No ("cold" 🧊) | ✅ Yes, it always holds its value ("hot" 🔥) |
| Ends? | Can end (like `countdown()`) | **Never** ends |
| Same value twice in a row? | Sent twice | Sent **once** (equal values are **skipped**) |
| Used for | Streams of data: database results, progress | **Screen state** in a ViewModel ⭐ |

### StateFlow skips repeated values 🔁

```kotlin
fun main() = runBlocking {
    val score = MutableStateFlow(0)

    val job = launch {
        score.collect { println("Score: $it") }
    }

    delay(100L); score.value = 5
    delay(100L); score.value = 5        // same as before → nobody is told
    delay(100L); score.value = 7
    delay(100L); job.cancel()
}
```

(`;` lets you put two short statements on one line.)

**Output:**

```
Score: 0
Score: 5
Score: 7
```

The second `5` was **skipped** — nothing changed, so the screen doesn't need to redraw. Smart! 🧠

> 💡 A StateFlow also **only keeps the latest** value. If it changes very fast (5 → 6 → 7 in one moment), a slow collector may only see 7. For **screen state**, that's exactly what we want: the screen only needs to show **the newest** state.

### From `Flow` to `StateFlow`: `stateIn` 🔄

Here's the problem: databases usually give us a **normal `Flow`** (Room does — Chapter 22). And `map` and `combine` **also** produce a normal `Flow`. But the UI wants a **`StateFlow`** — something with a current value that's always ready.

**`stateIn`** turns a `Flow` into a `StateFlow`. Here's the recipe from Chapter 16 again:

```kotlin
val uiState: StateFlow<RecipeListUiState> = repository.recipes
    .map { list -> RecipeListUiState(recipes = list.filter { it.isFavorite }) }
    .stateIn(
        scope = viewModelScope,                                   // (1)
        started = SharingStarted.WhileSubscribed(5_000),          // (2)
        initialValue = RecipeListUiState()                        // (3)
    )
```

Now we can understand **every** part! 🎉

**(1) `scope = viewModelScope`** — collecting a flow needs a **coroutine**. `stateIn` starts one for you, living in this **home**. When the ViewModel is cleared, it stops. 🏠

**(2) `started = ...`** — **when** should that coroutine run? Three choices:

| Choice | Starts… | Stops… | Good for |
|---|---|---|---|
| `SharingStarted.Eagerly` | **Immediately** | Never (until the scope ends) | Rare |
| `SharingStarted.Lazily` | When the **first** collector arrives | Never (until the scope ends) | Rare |
| `SharingStarted.WhileSubscribed(5_000)` ⭐ | When the **first** collector arrives | **5 seconds** after the **last** collector leaves | **Screen state** — use this |

Why `WhileSubscribed(5_000)`? Think of **lights with a timer** 💡⏲️:

- Someone enters the room (the screen starts collecting) → lights **on**.
- Everyone leaves (the app goes to the background → `collectAsStateWithLifecycle` stops collecting) → after **5 seconds**, lights **off**. Saves battery. 🔋
- **Rotation** takes about 1 second: the old screen leaves, the new one arrives. The 5-second timer **hasn't finished**, so the lights stay on — **no restart**, no flicker. ✅

**(3) `initialValue = ...`** — a `StateFlow` **must always have a value**. But the database may need a moment to answer. What should the screen show **until** the first real value arrives? This! Often an empty state, or a state with `isLoading = true`. ⏳

### The full picture 🖼️

```
Repository (Flow) ──▶ map / combine ──▶ stateIn ──▶ StateFlow ──▶ collectAsStateWithLifecycle() ──▶ 📱 UI
   🗄️ data             🔧 change it      🔄 hold it    🏟️ scoreboard       👀 watch it safely
```

---

## 18.16 Putting It Together: Fruit Finder 🍎🔍

Let's use `combine` + `stateIn` in a small screen, in **MyFirstApp**: a search box and a sort switch for a list of fruits.

```
┌────────────────────────────┐
│ 🔍 [ an              ]      │
│ Sort Z → A        [  ⚪ ]   │
│ 3 fruits found              │
│ Banana 🍌                   │
│ Mango 🥭                    │
│ Orange 🍊                   │
└────────────────────────────┘
```

### The ViewModel

```kotlin
data class FruitListUiState(                               // (1)
    val fruits: List<String> = emptyList(),
    val sortZtoA: Boolean = false
)

class FruitViewModel : ViewModel() {

    private val allFruits = listOf(                         // (2)
        "Apple 🍎", "Banana 🍌", "Cherry 🍒", "Grapes 🍇", "Kiwi 🥝",
        "Lemon 🍋", "Mango 🥭", "Orange 🍊", "Peach 🍑", "Pear 🍐",
        "Pineapple 🍍", "Strawberry 🍓", "Watermelon 🍉"
    )

    private val _query = MutableStateFlow("")               // (3)
    val query: StateFlow<String> = _query.asStateFlow()

    private val _sortZtoA = MutableStateFlow(false)         // (4)

    val uiState: StateFlow<FruitListUiState> =
        combine(_query, _sortZtoA) { query, zToA ->         // (5)
            val found = allFruits.filter { it.contains(query.trim(), ignoreCase = true) }
            val sorted = if (zToA) found.sortedDescending() else found.sorted()
            FruitListUiState(fruits = sorted, sortZtoA = zToA)
        }.stateIn(                                          // (6)
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = FruitListUiState(fruits = allFruits)
        )

    fun onQueryChange(newQuery: String) {                   // (7)
        _query.value = newQuery
    }

    fun onSortChange(zToA: Boolean) {
        _sortZtoA.value = zToA
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `FruitListUiState` | What the **list part** of the screen needs: the fruits to show and the switch position. |
| 2 | `allFruits` | Our pretend "database" 🗄️. (In Chapter 22 we'll use a real one!) |
| 3 | `_query` / `query` | The search text. **Private** writable + **public** read-only (Chapter 15). |
| 4 | `_sortZtoA` | The switch: `false` = A → Z, `true` = Z → A. |
| 5 | `combine(_query, _sortZtoA) { query, zToA -> ... }` | Whenever the text **or** the switch changes: filter, sort, and build a new `FruitListUiState`. `contains(..., ignoreCase = true)` → "AN" finds "Banana". `trim()` removes extra spaces. |
| 6 | `.stateIn(...)` | `combine` gives a normal `Flow` → turn it into a `StateFlow` for the UI, exactly as in 18.15. Before the first result, show **all** fruits. |
| 7 | `onQueryChange` / `onSortChange` | **Events** from the UI (Chapter 15). We only change the **inputs** — `combine` does the rest **automatically**. 🪄 |

> 🤔 **Why is `query` a separate StateFlow, and not inside `FruitListUiState`?**
> The `combine` + `stateIn` path is **not instant** — the new value arrives a tiny moment later. For a **list**, nobody notices. But a **text field** must get its text **immediately**, or the cursor can jump and letters can get lost while typing fast. ⌨️😖 So the text field reads `query` **directly**.
> 🎯 **Rule:** a `TextField`'s text should come **straight** from a `MutableStateFlow` (or `mutableStateOf`), not through `combine` / `map` / `stateIn`.

### The screen

```kotlin
@Composable
fun FruitFinder(viewModel: FruitViewModel = viewModel()) {
    val query by viewModel.query.collectAsStateWithLifecycle()
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        OutlinedTextField(
            value = query,
            onValueChange = viewModel::onQueryChange,
            label = { Text("Search fruits 🔍") },
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )

        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)
        ) {
            Text("Sort Z → A", modifier = Modifier.weight(1f))
            Switch(checked = uiState.sortZtoA, onCheckedChange = viewModel::onSortChange)
        }

        Text(
            text = "${uiState.fruits.size} fruits found",
            style = MaterialTheme.typography.labelLarge
        )

        LazyColumn {
            items(uiState.fruits, key = { it }) { fruit ->
                Text(fruit, modifier = Modifier.padding(vertical = 8.dp))
            }
        }
    }
}
```

Everything on this screen is from earlier chapters: `OutlinedTextField` and `Switch` (9), `weight` (6), `LazyColumn` with keys (10), `collectAsStateWithLifecycle` (15). 😎 (We kept it as one Composable to stay short. In a real app, split it into a Route + Screen, like Chapter 15.)

New imports for the ViewModel part:

```kotlin
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
```

(Press **Alt + Enter** on anything else that turns red.)

**Run it:** type "an" → Banana, Mango, Orange. Turn on the switch → the order flips. Rotate → everything stays. ✅

> 💡 **Bonus — waiting for the user to stop typing:** for a **real** internet search, you don't want to search after **every** letter. The `debounce(300)` operator waits until the text hasn't changed for 300 ms:
> ```kotlin
> _query.debounce(300).map { text -> search(text) } ...
> ```
> `debounce` is still marked as a "preview" feature, so Android Studio asks you to add `@OptIn(FlowPreview::class)` above the class or function. That's normal.

---

## 18.17 🛠️ Project Time: The "Background Lab" App 🧪

Now let's build a real app with **two** tabs:

```
┌────────────────────────┐        ┌────────────────────────┐
│                        │        │          🐱             │
│       01:23.45         │        │     cute_cat.jpg       │
│                        │        │                        │
│ Reset  Pause ⏸️  Lap 🏁 │        │ ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░   │
│                        │        │          45%           │
│ Lap 2        01:01.20  │        │     [ Cancel ✖️ ]       │
│ ────────────────────── │        │                        │
│ Lap 1        00:30.05  │        │                        │
│                        │        │ Simulate bad internet ⚪│
├───────────┬────────────┤        ├───────────┬────────────┤
│ ⏱️ Stopwatch │  ⬇️ Download │        │ ⏱️ Stopwatch │  ⬇️ Download │
└───────────┴────────────┘        └───────────┴────────────┘
```

| Tab | What it practices |
|---|---|
| ⏱️ **Stopwatch** | `viewModelScope.launch`, a **loop** with `delay`, keeping a **`Job`** to **pause** (cancel) it |
| ⬇️ **Download** | A **`Flow`** of progress, `collect`, `withContext(Dispatchers.Default)`, **cancelling**, **errors** with `try` / `catch`, a **sealed** status |

### Step 1: Create the project

1. **File → New → New Project… → Empty Activity** → **Next**.
2. **Name:** `Background Lab`
3. **Package name:** `com.example.backgroundlab`
4. **Minimum SDK:** API 24 (like before) → **Finish**.

Android Studio makes the theme for you: **`BackgroundLabTheme`**. (If your project name is different, your theme name is different too — use yours.)

### Step 2: Add the libraries 📦

The same two lifecycle libraries as in Chapter 15. **No new libraries** — coroutines and Flow are **already included** with them. 🎉

**`gradle/libs.versions.toml`**, under `[libraries]`:

```toml
androidx-lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycleRuntimeKtx" }
androidx-lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycleRuntimeKtx" }
```

**`build.gradle.kts (Module :app)`**:

```kotlin
dependencies {
    // ... existing lines ...
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)
}
```

Click **Sync Now**. 🔄 ✅

> ℹ️ Where do coroutines come from? The `kotlinx-coroutines` library is a **dependency of** the lifecycle libraries, so you get it **for free**. In a plain Kotlin project (no Android), you would add `org.jetbrains.kotlinx:kotlinx-coroutines-core` yourself.

### Step 3: The folders 📁

Right-click the `com.example.backgroundlab` package → **New → Package** to make them (Chapter 16):

```
com.example.backgroundlab
 ├── MainActivity.kt
 ├── data/
 │    └── FakeDownloader.kt
 └── ui/
      ├── theme/                    (already there)
      ├── stopwatch/
      │    ├── StopwatchUiState.kt
      │    ├── StopwatchViewModel.kt
      │    └── StopwatchScreen.kt
      └── download/
           ├── DownloadUiState.kt
           ├── DownloadViewModel.kt
           └── DownloadScreen.kt
```

---

## 18.18 Project Part 1: The Stopwatch ⏱️

### How does a stopwatch work? 🤔

**Idea 1 (❌ wrong):** "Every 10 ms, add 10 to the time."

```kotlin
while (true) {
    delay(10L)
    elapsed += 10      // ❌
}
```

The problem: `delay(10)` means "wait **at least** 10 ms". Sometimes it's 11, sometimes 13, plus the time to update the screen. After one minute, this stopwatch could be **seconds** too slow! 🐌

**Idea 2 (✅ right):** Remember **when** we started. Then, every few milliseconds, **calculate**: `now − start`. Even if one update comes a bit late, the **time shown is always correct**. ✅

```
started at:   1000 ms  (the phone's clock)
now:          4250 ms
elapsed:      4250 − 1000 = 3250 ms  →  "00:03.25"
```

We read "now" with **`SystemClock.elapsedRealtime()`**: the number of milliseconds since the phone was **turned on**. 📱

> 🤔 Why not the normal clock (`System.currentTimeMillis()`)? Because the normal clock can **jump**: the user can change the time, or the phone updates it from the network. `elapsedRealtime()` **never jumps** — perfect for measuring time. ✅

**Pausing** = **cancel** the loop's `Job`. **Continuing** = start a new loop, and pretend we started `elapsed` milliseconds **ago**.

### `StopwatchUiState.kt`

```kotlin
package com.example.backgroundlab.ui.stopwatch

data class StopwatchUiState(
    val elapsedMillis: Long = 0L,                         // (1)
    val isRunning: Boolean = false,                       // (2)
    val laps: List<Long> = emptyList()                    // (3)
) {
    val timeText: String                                  // (4)
        get() = formatTime(elapsedMillis)

    val canLap: Boolean
        get() = isRunning

    val canReset: Boolean
        get() = !isRunning && elapsedMillis > 0L
}

fun formatTime(millis: Long): String {                    // (5)
    val minutes = millis / 60_000
    val seconds = (millis / 1_000) % 60
    val hundredths = (millis / 10) % 100
    return "${twoDigits(minutes)}:${twoDigits(seconds)}.${twoDigits(hundredths)}"
}

private fun twoDigits(number: Long): String =             // (6)
    number.toString().padStart(2, '0')
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `elapsedMillis` | How much time has passed, in milliseconds. `Long` because it can get big. |
| 2 | `isRunning` | Is the stopwatch counting right now? |
| 3 | `laps` | Saved lap times, **newest first**. |
| 4 | `timeText`, `canLap`, `canReset` | **Calculated** values (Chapter 15) — the screen just reads them. You can only press Lap while running, and Reset while paused with some time on it. |
| 5 | `formatTime(...)` | Turns milliseconds into `"01:23.45"`. It's **outside** the class because the lap list needs it too. |
| 6 | `padStart(2, '0')` | Makes the text at least 2 characters long by adding `'0'` at the **start**: `"5"` → `"05"`, `"23"` → `"23"`. |

**Let's check `formatTime(83_456)`** with real numbers 🧮:

| Step | Math | Result |
|---|---|---|
| minutes | 83 456 / 60 000 | **1** (Int division drops the rest, Chapter 2) |
| seconds | 83 456 / 1 000 = 83 → 83 % 60 | **23** |
| hundredths | 83 456 / 10 = 8 345 → 8 345 % 100 | **45** |
| text | | **"01:23.45"** ✅ |

### `StopwatchViewModel.kt`

```kotlin
package com.example.backgroundlab.ui.stopwatch

import android.os.SystemClock
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch

class StopwatchViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(StopwatchUiState())
    val uiState: StateFlow<StopwatchUiState> = _uiState.asStateFlow()

    private var tickJob: Job? = null                                  // (1)
    private var startedAt = 0L                                        // (2)

    fun onStartPauseClick() {                                         // (3)
        if (_uiState.value.isRunning) pause() else start()
    }

    fun onLapClick() {
        if (!_uiState.value.isRunning) return                         // (4)
        val lapTime = now() - startedAt
        _uiState.update {
            it.copy(elapsedMillis = lapTime, laps = listOf(lapTime) + it.laps)   // (5)
        }
    }

    fun onResetClick() {
        tickJob?.cancel()
        tickJob = null
        _uiState.value = StopwatchUiState()                           // (6)
    }

    private fun start() {
        startedAt = now() - _uiState.value.elapsedMillis              // (7)
        _uiState.update { it.copy(isRunning = true) }

        tickJob = viewModelScope.launch {                             // (8)
            while (isActive) {                                        // (9)
                _uiState.update { it.copy(elapsedMillis = now() - startedAt) }
                delay(10L)                                            // (10)
            }
        }
    }

    private fun pause() {
        tickJob?.cancel()                                             // (11)
        tickJob = null
        _uiState.update { it.copy(isRunning = false, elapsedMillis = now() - startedAt) }   // (12)
    }

    private fun now(): Long = SystemClock.elapsedRealtime()           // (13)
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `private var tickJob: Job? = null` | The **ticket** 🎫 of the counting coroutine, so we can **cancel** it later. `null` = not counting. |
| 2 | `private var startedAt = 0L` | The phone's time when we (pretend we) started. Not part of the UI, so it's a normal private property. |
| 3 | `onStartPauseClick()` | **One** button for both: running → pause, not running → start. |
| 4 | `if (!...isRunning) return` | Laps only while running. (The button is also disabled — but the ViewModel should **protect itself** too. 🛡️) |
| 5 | `listOf(lapTime) + it.laps` | A **new** list: the new lap **first**, then the old ones. (`+` joins two lists, Chapter 3.) We also update `elapsedMillis`, so the big time and the lap match exactly. |
| 6 | `_uiState.value = StopwatchUiState()` | Back to the **default** state: 0, not running, no laps. |
| 7 | `startedAt = now() - elapsedMillis` | The trick for **continuing** after a pause! If 3 seconds were already counted, pretend we started 3 seconds **ago**. On the first start, `elapsedMillis` is 0, so `startedAt = now()`. |
| 8 | `tickJob = viewModelScope.launch { ... }` | Start the counting coroutine in the ViewModel's home, and **keep its ticket**. |
| 9 | `while (isActive)` | Repeat until cancelled. (`delay` also checks for cancelling, so `while (true)` would work too — but `isActive` makes the **meaning** clear: "while nobody stopped me".) |
| 10 | `delay(10L)` | Pause 10 ms 🔖 → about 100 updates per second, enough for the hundredths. The main thread is free between updates. 😊 |
| 11 | `tickJob?.cancel()` | **Stop** the loop. `?.` because it might be `null`. |
| 12 | `elapsedMillis = now() - startedAt` | Save the **exact** time at the moment of pausing (the last tick could be up to 10 ms old). |
| 13 | `SystemClock.elapsedRealtime()` | "Milliseconds since the phone was turned on." Never jumps. ✅ |

### `StopwatchScreen.kt`

```kotlin
package com.example.backgroundlab.ui.stopwatch

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material3.Button
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.backgroundlab.ui.theme.BackgroundLabTheme

@Composable
fun StopwatchRoute(
    modifier: Modifier = Modifier,
    viewModel: StopwatchViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    StopwatchScreen(
        uiState = uiState,
        onStartPauseClick = viewModel::onStartPauseClick,
        onLapClick = viewModel::onLapClick,
        onResetClick = viewModel::onResetClick,
        modifier = modifier
    )
}

@Composable
fun StopwatchScreen(
    uiState: StopwatchUiState,
    onStartPauseClick: () -> Unit,
    onLapClick: () -> Unit,
    onResetClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(Modifier.height(32.dp))

        Text(
            text = uiState.timeText,
            style = MaterialTheme.typography.displayLarge,
            fontFamily = FontFamily.Monospace                         // (1)
        )

        Spacer(Modifier.height(32.dp))

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedButton(onClick = onResetClick, enabled = uiState.canReset) {
                Text("Reset")
            }
            Button(onClick = onStartPauseClick) {
                Text(if (uiState.isRunning) "Pause ⏸️" else "Start ▶️")   // (2)
            }
            OutlinedButton(onClick = onLapClick, enabled = uiState.canLap) {
                Text("Lap 🏁")
            }
        }

        Spacer(Modifier.height(24.dp))

        LazyColumn(modifier = Modifier.fillMaxWidth()) {
            itemsIndexed(
                items = uiState.laps,
                key = { index, _ -> uiState.laps.size - index }       // (3)
            ) { index, lapMillis ->
                val lapNumber = uiState.laps.size - index             // (4)
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 12.dp)
                ) {
                    Text("Lap $lapNumber", modifier = Modifier.weight(1f))
                    Text(formatTime(lapMillis), fontFamily = FontFamily.Monospace)
                }
                HorizontalDivider()
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun StopwatchScreenPreview() {
    BackgroundLabTheme {
        StopwatchScreen(
            uiState = StopwatchUiState(
                elapsedMillis = 83_450L,
                isRunning = true,
                laps = listOf(61_200L, 30_050L)
            ),
            onStartPauseClick = {},
            onLapClick = {},
            onResetClick = {}
        )
    }
}
```

**The new parts:**

| # | Code | Meaning |
|---|---|---|
| 1 | `fontFamily = FontFamily.Monospace` | A font where **every** digit has the **same width**. Without it, the time **wiggles** left and right as the digits change ("1" is thinner than "8"). Try removing it and see! 👀 |
| 2 | `if (uiState.isRunning) "Pause ⏸️" else "Start ▶️"` | One button, two labels. |
| 3 | `key = { index, _ -> uiState.laps.size - index }` | Each lap's **number** is its key (Chapter 10). The newest lap is at index 0, so the key is calculated the same way as the number. `_` = "I don't need the lap value here." |
| 4 | `uiState.laps.size - index` | With 3 laps: index 0 → "Lap 3", index 1 → "Lap 2", index 2 → "Lap 1". Newest on top. ✅ |

---

## 18.19 Project Part 2: The Fake Download ⬇️

We don't have the internet yet (that's Chapter 19!), so we'll **pretend**: a `Flow` that sends progress numbers 5, 10, 15, … 100 — slowly, like a real download.

### `data/FakeDownloader.kt`

```kotlin
package com.example.backgroundlab.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.withContext
import java.io.IOException

class FakeDownloader {

    fun download(badInternet: Boolean): Flow<Int> = flow {            // (1)
        for (percent in 5..100 step 5) {                              // (2)
            delay(200L)                                               // (3)
            if (badInternet && percent == 60) {
                throw IOException("Connection lost at 60% 📶")        // (4)
            }
            emit(percent)                                             // (5)
        }
    }

    suspend fun checkFile(): Boolean = withContext(Dispatchers.Default) {   // (6)
        var checksum = 0L
        for (i in 1..30_000_000) {                                    // (7)
            checksum += i % 7
            if (i % 1_000_000 == 0) ensureActive()                    // (8)
        }
        delay(1_000L)                                                 // (9)
        checksum > 0                                                  // (10)
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `fun download(...): Flow<Int> = flow { ... }` | Returns a **Flow** of percentages. Remember: nothing happens until someone **collects**. 🧊 |
| 2 | `for (percent in 5..100 step 5)` | 5, 10, 15, … 100 → 20 steps. (`step`, Chapter 2.) |
| 3 | `delay(200L)` | Each step "takes" 200 ms → the whole download takes 20 × 200 = **4 seconds**. |
| 4 | `throw IOException(...)` | When "bad internet" is on, fail at 60%. `IOException` is the **real** error type for internet and file problems. |
| 5 | `emit(percent)` | Send the progress to whoever is collecting. 🍣 |
| 6 | `suspend fun checkFile() = withContext(Dispatchers.Default) { ... }` | A **main-safe** function (18.8): it moves its own heavy work to the **cooks** 👨‍🍳. |
| 7 | `for (i in 1..30_000_000)` | 30 million little calculations — **heavy** work, pretending to check the file. |
| 8 | `if (i % 1_000_000 == 0) ensureActive()` | Every million loops, check for the "please stop" sign 🪧 (18.7). Without this, **Cancel** would have to wait until the loop ends. |
| 9 | `delay(1_000L)` | Modern phones finish the loop very fast, so we wait 1 more second — just so you can **see** the "Checking" step. 😉 |
| 10 | `checksum > 0` | The last line = the result (`true` → the file is OK). |

### `ui/download/DownloadUiState.kt`

```kotlin
package com.example.backgroundlab.ui.download

sealed interface DownloadStatus {                                     // (1)
    data object Idle : DownloadStatus
    data class Downloading(val percent: Int) : DownloadStatus
    data object Checking : DownloadStatus
    data object Done : DownloadStatus
    data class Failed(val message: String) : DownloadStatus
}

data class DownloadUiState(
    val status: DownloadStatus = DownloadStatus.Idle,                 // (2)
    val badInternet: Boolean = false
) {
    val isBusy: Boolean                                               // (3)
        get() = status is DownloadStatus.Downloading || status is DownloadStatus.Checking
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `sealed interface DownloadStatus` | The download is **always** in exactly **one** of these 5 situations (Chapter 4). Only `Downloading` and `Failed` carry extra data, so they are `data class`es; the others are `data object`s. |
| 2 | `status = DownloadStatus.Idle` | At the start: nothing happening. |
| 3 | `isBusy` | `true` while downloading or checking. We use it to **lock** the switch during work. 🔒 |

### Picture the states 🗺️

```
[Idle] ──Download──▶ [Downloading 5%…100%] ──▶ [Checking 🔍] ──▶ [Done ✅]
                           │ IOException 📶          │ broken file 💔
                           ▼                         ▼
                       [Failed ❌] ◀─────────────────┘

Cancel ✖️ (while Downloading or Checking)        ──▶ [Idle]
Try again / Download again (from Failed or Done) ──▶ [Downloading]
```

Every arrow is one `setStatus(...)` call in the ViewModel below. 👇

### `ui/download/DownloadViewModel.kt`

```kotlin
package com.example.backgroundlab.ui.download

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.backgroundlab.data.FakeDownloader
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.io.IOException

class DownloadViewModel : ViewModel() {

    private val downloader = FakeDownloader()                         // (1)

    private val _uiState = MutableStateFlow(DownloadUiState())
    val uiState: StateFlow<DownloadUiState> = _uiState.asStateFlow()

    private var downloadJob: Job? = null                              // (2)

    fun onBadInternetChange(value: Boolean) {
        _uiState.update { it.copy(badInternet = value) }
    }

    fun onDownloadClick() {
        if (downloadJob?.isActive == true) return                     // (3)
        val badInternet = _uiState.value.badInternet

        downloadJob = viewModelScope.launch {
            try {                                                     // (4)
                setStatus(DownloadStatus.Downloading(percent = 0))
                downloader.download(badInternet).collect { percent -> // (5)
                    setStatus(DownloadStatus.Downloading(percent))
                }

                setStatus(DownloadStatus.Checking)                    // (6)
                val fileIsOk = downloader.checkFile()                 // (7)

                setStatus(
                    if (fileIsOk) DownloadStatus.Done
                    else DownloadStatus.Failed("The file is broken 💔")
                )
            } catch (e: IOException) {                                // (8)
                setStatus(DownloadStatus.Failed(e.message ?: "Something went wrong"))
            }
        }
    }

    fun onCancelClick() {
        downloadJob?.cancel()                                         // (9)
        downloadJob = null
        setStatus(DownloadStatus.Idle)
    }

    private fun setStatus(status: DownloadStatus) {                   // (10)
        _uiState.update { it.copy(status = status) }
    }
}
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `private val downloader = FakeDownloader()` | Our "data source". (In a bigger app it would come from the **AppContainer**, Chapter 16 — or Hilt, Chapter 23.) |
| 2 | `downloadJob` | The ticket 🎫 of the running download, for **Cancel**. |
| 3 | `if (downloadJob?.isActive == true) return` | Already downloading? Don't start a **second** one! (Double-taps happen. 👆👆) `== true` because `?.` can give `null`. |
| 4 | `try { ... }` | Everything that can fail goes inside. |
| 5 | `.collect { percent -> ... }` | **Start** the Flow and update the status for **every** percent. This line **pauses** here until the flow is finished (4 seconds) — then the code continues to the next line. In order, like a story. 📖 |
| 6 | `setStatus(DownloadStatus.Checking)` | Download finished → now "checking". |
| 7 | `downloader.checkFile()` | A **main-safe** suspend function. We're on the main thread, but it moves itself to `Default`. We don't need to care! 😎 |
| 8 | `catch (e: IOException)` | Catch **only** internet/file errors. ✅ This does **not** catch cancellation (18.9), so **Cancel** still works properly. `e.message ?: "..."` — the message might be `null` (Chapter 3). |
| 9 | `downloadJob?.cancel()` | Stop the coroutine. Whatever it's doing — waiting in `delay`, collecting, or checking — it stops at the next check. 🛑 |
| 10 | `setStatus(...)` | A tiny helper so we don't repeat `_uiState.update { it.copy(status = ...) }` six times. ✂️ |

### `ui/download/DownloadScreen.kt`

```kotlin
package com.example.backgroundlab.ui.download

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.backgroundlab.ui.theme.BackgroundLabTheme

@Composable
fun DownloadRoute(
    modifier: Modifier = Modifier,
    viewModel: DownloadViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    DownloadScreen(
        uiState = uiState,
        onDownloadClick = viewModel::onDownloadClick,
        onCancelClick = viewModel::onCancelClick,
        onBadInternetChange = viewModel::onBadInternetChange,
        modifier = modifier
    )
}

@Composable
fun DownloadScreen(
    uiState: DownloadUiState,
    onDownloadClick: () -> Unit,
    onCancelClick: () -> Unit,
    onBadInternetChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("🐱", style = MaterialTheme.typography.displayLarge)
        Text("cute_cat.jpg", style = MaterialTheme.typography.titleLarge)

        when (val status = uiState.status) {                          // (1)
            DownloadStatus.Idle -> {
                Text("Ready to download.")
                Button(onClick = onDownloadClick) { Text("Download ⬇️") }
            }

            is DownloadStatus.Downloading -> {                        // (2)
                LinearProgressIndicator(
                    progress = { status.percent / 100f },             // (3)
                    modifier = Modifier.fillMaxWidth()
                )
                Text("${status.percent}%")
                OutlinedButton(onClick = onCancelClick) { Text("Cancel ✖️") }
            }

            DownloadStatus.Checking -> {
                CircularProgressIndicator()                           // (4)
                Text("Checking the file… 🔍")
                OutlinedButton(onClick = onCancelClick) { Text("Cancel ✖️") }
            }

            DownloadStatus.Done -> {
                Text(
                    "Download complete! ✅",
                    color = MaterialTheme.colorScheme.primary
                )
                Button(onClick = onDownloadClick) { Text("Download again 🔁") }
            }

            is DownloadStatus.Failed -> {
                Text(
                    "❌ ${status.message}",
                    color = MaterialTheme.colorScheme.error
                )
                Button(onClick = onDownloadClick) { Text("Try again 🔁") }
            }
        }

        Spacer(Modifier.weight(1f))                                   // (5)

        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Simulate bad internet 📶", modifier = Modifier.weight(1f))
            Switch(
                checked = uiState.badInternet,
                onCheckedChange = onBadInternetChange,
                enabled = !uiState.isBusy                             // (6)
            )
        }
    }
}

@Preview(showBackground = true)
@Composable
fun DownloadScreenPreview() {
    BackgroundLabTheme {
        DownloadScreen(
            uiState = DownloadUiState(status = DownloadStatus.Downloading(45)),
            onDownloadClick = {},
            onCancelClick = {},
            onBadInternetChange = {}
        )
    }
}
```

**The new parts:**

| # | Code | Meaning |
|---|---|---|
| 1 | `when (val status = uiState.status)` | Save the status in a short local name **and** check its type. Because it's a `sealed interface`, `when` knows all 5 cases — forget one and you get an error. 🛡️ |
| 2 | `is DownloadStatus.Downloading ->` | `is` for **classes** (they carry data). Inside, Kotlin **knows** `status` is `Downloading`, so `status.percent` works (smart cast, Chapter 4). The `data object`s don't need `is`. |
| 3 | `progress = { status.percent / 100f }` | The bar wants a number from **0.0** to **1.0**. 45 / 100f = 0.45. The `f` makes it a `Float` division (Int division would give **0**! Remember Chapter 17's trap? 😉) |
| 4 | `CircularProgressIndicator()` | A spinning circle **without** a percentage — for "working, but we don't know how long". |
| 5 | `Spacer(Modifier.weight(1f))` | Takes all the free space → pushes the switch row to the **bottom**. |
| 6 | `enabled = !uiState.isBusy` | You can't change "bad internet" in the middle of a download. 🔒 |

---

## 18.20 Connecting the Tabs: `MainActivity.kt` 🔗

Replace everything in `MainActivity.kt`:

```kotlin
package com.example.backgroundlab

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import com.example.backgroundlab.ui.download.DownloadRoute
import com.example.backgroundlab.ui.stopwatch.StopwatchRoute
import com.example.backgroundlab.ui.theme.BackgroundLabTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            BackgroundLabTheme {
                BackgroundLabApp()
            }
        }
    }
}

@Composable
fun BackgroundLabApp() {
    var selectedTab by rememberSaveable { mutableIntStateOf(0) }      // (1)

    Scaffold(
        bottomBar = {
            NavigationBar {
                NavigationBarItem(
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 },
                    icon = { Text("⏱️") },                            // (2)
                    label = { Text("Stopwatch") }
                )
                NavigationBarItem(
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 },
                    icon = { Text("⬇️") },
                    label = { Text("Download") }
                )
            }
        }
    ) { innerPadding ->
        val contentModifier = Modifier.padding(innerPadding)          // (3)
        when (selectedTab) {
            0 -> StopwatchRoute(modifier = contentModifier)
            else -> DownloadRoute(modifier = contentModifier)
        }
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `rememberSaveable { mutableIntStateOf(0) }` | Which tab is selected: 0 or 1. **Saveable**, so it survives rotation (Chapter 8). |
| 2 | `icon = { Text("⏱️") }` | An emoji as the icon — simple, no icon library needed. |
| 3 | `Modifier.padding(innerPadding)` | Keep the content away from the bottom bar and the status bar (Chapter 11). |

> 🧠 **Interesting:** there's no NavHost here, so `viewModel()` gives ViewModels that belong to the **Activity**. Both ViewModels stay alive when you **switch tabs** — so the stopwatch **keeps running** while you look at the Download tab, and the download keeps going while you look at the stopwatch! Try it. ⏱️⬇️

**Run the app!** ▶️ 🎉

---

## 18.21 Test Checklist ✅

| Test | Expected | ✓ |
|---|---|---|
| **Stopwatch:** tap Start | Time counts smoothly: 00:00.01, 00:00.02, … | ☐ |
| The digits don't wiggle | (Monospace font) | ☐ |
| Tap Lap 3 times | Lap 3, Lap 2, Lap 1 — newest on top | ☐ |
| Tap Pause, wait 5 seconds, tap Start | Continues from the **paused** time (not +5 s!) | ☐ |
| Reset while running | Disabled | ☐ |
| Pause → Reset | 00:00.00, laps gone | ☐ |
| Run for 1 minute next to your phone's clock app | Same time ✅ (no drift) | ☐ |
| Rotate while running 🔄 | Keeps counting, laps stay | ☐ |
| Switch to Download tab and back | Still counting | ☐ |
| **Download:** tap Download | Bar fills 5% … 100% in about 4 s, then "Checking…", then "Download complete! ✅" | ☐ |
| Cancel during download | Back to "Ready to download." immediately | ☐ |
| Cancel during "Checking" | Back to Ready immediately | ☐ |
| Turn on bad internet → Download | Stops at 55%, shows "❌ Connection lost at 60% 📶" | ☐ |
| Try again (bad internet still on) | Fails again at the same place | ☐ |
| Switch during download | Disabled 🔒 | ☐ |
| Tap Download, then rotate | Download continues, no restart | ☐ |
| Tap the Download button very fast twice | Only **one** download | ☐ |
| Switch tabs during "Checking" | App stays smooth — the heavy work is on `Default` 👨‍🍳 | ☐ |

> 💡 **Why does it stop at 55% and not 60%?** Look at `FakeDownloader`: the error is thrown **before** `emit(60)`. So the last value that arrived was 55. Code does exactly what you write! 🤓

> ⚠️ **What about process death** (Chapter 14)? Both screens start again from zero — the `Job`s are gone. For a stopwatch, a challenge below fixes it. For **real** long downloads that must finish even if the app is closed, Android has **WorkManager** — **Chapter 25**. 📦

---

## 18.22 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| `Thread.sleep(...)` in app code | 🥶 Frozen app, ANR | `delay(...)` inside a coroutine. |
| Calling a suspend function in `onClick` | *Suspend function should be called only from a coroutine…* | `viewModel.doIt()` + `viewModelScope.launch` inside, or `scope.launch { }`. |
| `runBlocking` in an app | Blocks the main thread → frozen | Only in the Playground and tests. |
| `GlobalScope.launch` | Never cancelled → leaks, crashes | `viewModelScope`, `rememberCoroutineScope()`, `LaunchedEffect`. |
| `scope.launch` directly in a Composable's body | Starts again on **every** recomposition 💥 | `LaunchedEffect(key) { }`. |
| Long work in `rememberCoroutineScope` | Cancelled on rotation | Move it to the ViewModel (`viewModelScope`). |
| Heavy loop on Main | Frozen even though it's a coroutine! | `withContext(Dispatchers.Default) { }`. |
| `while (true)` with **no** suspend call inside | Can't be cancelled | `while (isActive)` or `ensureActive()`. |
| `catch (e: Exception)` around suspend calls | Also catches cancellation | Catch specific errors, or rethrow `CancellationException`. |
| Starting a 2nd job while the 1st runs | Two downloads/timers at once | Check `job?.isActive == true` first. |
| Forgetting `collect` | The flow does **nothing** (it's cold 🧊) | Collect it (or use `stateIn`). |
| `collect` on a StateFlow, then more code below | The code below **never runs** (StateFlow never ends) | Collect in its **own** `launch { }`. |
| `withContext` around `emit` inside `flow { }` | *Flow invariant is violated* error | Use `.flowOn(...)` after the flow. |
| Counting time with `elapsed += 10` | Clock drifts slower and slower | Calculate `now - startedAt`. |
| TextField text coming through `combine`/`stateIn` | Cursor jumps, letters get lost | Give the TextField its own `MutableStateFlow`. |
| `percent / 100` for a progress bar | Always 0 (Int division) | `percent / 100f`. |

---

## 18.23 Summary — What You Learned 🎓

✅ The **main thread** draws the screen and handles taps. **Never block it** — or the app freezes and Android shows an **ANR**. 🥶

✅ A **coroutine** is a task that can **pause** (suspend 🔖) and **continue** later **without blocking** the thread. They're **cheap** — use as many as you want.

✅ **`suspend fun`** = "this function might pause." Call it only from a coroutine or another suspend function. `suspend` alone does **not** move work to the background.

✅ **`launch { }`** starts a coroutine and returns a **`Job`** 🎫 (`cancel()`, `join()`, `isActive`). **`async { }` + `await()`** run things **at the same time** and give back results.

✅ **Cancelling** is polite 🙇: coroutines stop at the next suspend point. In long loops, check **`isActive`** or call **`ensureActive()`**.

✅ **Structured concurrency** 👨‍👩‍👧: cancel the parent → children are cancelled. That's why **`viewModelScope`** cleans up everything automatically.

✅ **Dispatchers:** `Main` 🤵 (UI), `IO` 📦 (waiting: internet, files, database), `Default` 👨‍🍳 (heavy math). Switch with **`withContext`**. Make slow functions **main-safe**.

✅ **Errors:** `try` / `catch` **specific** errors (like `IOException`) — don't swallow cancellation.

✅ **Android scopes:** `viewModelScope` ⭐ (most work), `rememberCoroutineScope()` (UI actions after taps), **`LaunchedEffect(key)`** (start when something appears; restart when the key changes).

✅ **`Flow`** 🌊 = many values over time. `flow { emit(x) }` to make, `collect { }` to receive. Flows are **cold** 🧊.

✅ **Operators:** `map`, `filter`, `take`, `onEach`, `catch`, `flowOn`, and **`combine`** for mixing flows.

✅ **`StateFlow`** = a scoreboard 🏟️: always has a value, skips repeats, never ends. **`stateIn(viewModelScope, WhileSubscribed(5_000), initialValue)`** turns any Flow into a StateFlow for the UI.

✅ You built a **Stopwatch** ⏱️ and a **fake download** ⬇️ with progress, cancel, errors, and a heavy background step! 🎉

---

## 18.24 Practice Time 🏋️

Tasks 1–3 go in the **Kotlin Playground**. Tasks 4–6 go in **MyFirstApp**.

**Task 1 — Weather and news at the same time 🌦️📰:**
Write `suspend fun fetchWeather(): String` (waits 1500 ms, returns `"Sunny ☀️"`) and `suspend fun fetchNews(): String` (waits 1000 ms, returns `"Cats are great 🐱"`). In `main`, get **both at the same time** and print them, plus how long it took. It should be about **1500 ms**.

**Task 2 — Tick, tick, stop ⏰:**
Launch a coroutine that prints `"Tick N"` every 300 ms, forever. Cancel it after 1 second. Before writing the code, **guess** the output. Then check.

**Task 3 — Cookie factory 🍪:**
Make a flow that emits the numbers 1 to 20, with a 100 ms delay between them. Keep only the **multiples of 3**, turn each into `"🍪 x N"`, and take only the first **4**. What's printed?

**Task 4 — Traffic light 🚦:**
A Composable that shows "🔴 Stop" for 3 seconds, "🟢 Go" for 3 seconds, "🟡 Slow down" for 1 second, and repeats **forever**. Use `LaunchedEffect`.

**Task 5 — Find the 3 bugs 🐛🐛🐛:**

```kotlin
class WeatherViewModel : ViewModel() {
    val temperature = MutableStateFlow(0)

    fun refresh() {
        GlobalScope.launch {
            Thread.sleep(2_000L)
            temperature.value = 21
        }
    }
}
```

**Task 6 — Shopping cart total 🛒:**
Make `CartViewModel` with a price of **25 coins** per item and a quantity (starting at 1) that the user changes with **−** and **+** buttons (not below 1). Show `"Total: 75 coins 🪙"`. Calculate the total text with **`combine`** of a price flow and a quantity flow, and **`stateIn`**.

---

### Answers

**Task 1:**

```kotlin
import kotlinx.coroutines.*
import kotlin.system.measureTimeMillis

suspend fun fetchWeather(): String {
    delay(1_500L)
    return "Sunny ☀️"
}

suspend fun fetchNews(): String {
    delay(1_000L)
    return "Cats are great 🐱"
}

fun main() = runBlocking {
    val time = measureTimeMillis {
        val weather = async { fetchWeather() }
        val news = async { fetchNews() }
        println("Weather: ${weather.await()}")
        println("News: ${news.await()}")
    }
    println("It took $time ms")
}
```

**Output:**

```
Weather: Sunny ☀️
News: Cats are great 🐱
It took 1512 ms
```

Both start at once, so the total is the **longest** one (1500 ms), not 1500 + 1000. ⚡ Without `async` (just `val weather = fetchWeather()` and `val news = fetchNews()`), it would take about 2500 ms.

**Task 2:**

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    val job = launch {
        var n = 1
        while (true) {
            println("Tick $n")
            n++
            delay(300L)
        }
    }
    delay(1_000L)
    job.cancel()
    println("Stopped 🛑")
}
```

**Output:**

```
Tick 1      ← at 0 ms
Tick 2      ← at 300 ms
Tick 3      ← at 600 ms
Tick 4      ← at 900 ms
Stopped 🛑   ← at 1000 ms
```

💡 Here `while (true)` is OK: the loop has a `delay`, and `delay` checks the "please stop" sign. 🪧

**Task 3:**

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

fun main() = runBlocking {
    flow {
        for (i in 1..20) {
            delay(100L)
            emit(i)
        }
    }
        .filter { it % 3 == 0 }
        .map { "🍪 x $it" }
        .take(4)
        .collect { println(it) }
}
```

**Output:**

```
🍪 x 3
🍪 x 6
🍪 x 9
🍪 x 12
```

After the 4th cookie, `take(4)` **stops** the flow — numbers 13 to 20 are never even made. ✂️ (So it takes about 1.2 seconds, not 2.)

**Task 4:**

```kotlin
@Composable
fun TrafficLight() {
    var light by remember { mutableStateOf("🔴 Stop") }

    LaunchedEffect(Unit) {
        while (true) {
            light = "🔴 Stop"
            delay(3_000L)
            light = "🟢 Go"
            delay(3_000L)
            light = "🟡 Slow down"
            delay(1_000L)
        }
    }

    Text(light, style = MaterialTheme.typography.displayMedium)
}
```

💡 `LaunchedEffect(Unit)` starts **once**. The `while (true)` loop runs forever — but it's **safe**: when the Composable leaves the screen, the effect is cancelled, and `delay` sees the sign and stops. ✅

**Task 5:**

| # | Bug | Fix |
|---|---|---|
| 1 | `val temperature = MutableStateFlow(0)` is **public** and writable — the UI could change it. | `private val _temperature` + `val temperature = _temperature.asStateFlow()` |
| 2 | **`GlobalScope`** — never cancelled, even when the ViewModel is cleared. 💧 | `viewModelScope.launch` |
| 3 | **`Thread.sleep`** — blocks the thread. | `delay(2_000L)` |

```kotlin
class WeatherViewModel : ViewModel() {
    private val _temperature = MutableStateFlow(0)
    val temperature: StateFlow<Int> = _temperature.asStateFlow()

    fun refresh() {
        viewModelScope.launch {
            delay(2_000L)
            _temperature.value = 21
        }
    }
}
```

**Task 6:**

```kotlin
class CartViewModel : ViewModel() {

    private val price = MutableStateFlow(25)                    // coins per item

    private val _quantity = MutableStateFlow(1)
    val quantity: StateFlow<Int> = _quantity.asStateFlow()

    val totalText: StateFlow<String> =
        combine(price, _quantity) { p, q -> "Total: ${p * q} coins 🪙" }
            .stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5_000),
                initialValue = ""
            )

    fun onPlusClick() {
        _quantity.update { it + 1 }
    }

    fun onMinusClick() {
        _quantity.update { (it - 1).coerceAtLeast(1) }
    }
}

@Composable
fun Cart(viewModel: CartViewModel = viewModel()) {
    val quantity by viewModel.quantity.collectAsStateWithLifecycle()
    val totalText by viewModel.totalText.collectAsStateWithLifecycle()

    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            OutlinedButton(onClick = viewModel::onMinusClick, enabled = quantity > 1) { Text("−") }
            Text("$quantity", style = MaterialTheme.typography.headlineMedium)
            OutlinedButton(onClick = viewModel::onPlusClick) { Text("+") }
        }
        Text(totalText, style = MaterialTheme.typography.titleLarge)
    }
}
```

💡 The price never changes here, so `combine` might feel like too much. But imagine the price comes from the **internet** and can change (a sale! 🏷️). With `combine`, the total updates **automatically** when **either** one changes. That's the power of flows. 🌊

---

## 18.25 Challenges 🚀

### Challenge 1: The Quiz timer ⏱️ ⭐⭐⭐
Go back to the **Quiz app** (Chapter 17, Challenge 4). Give each question 15 seconds.
*Hint:* in `QuizViewModel`, keep a `timerJob: Job?`. When a question is shown, cancel the old job and `launch` a new one that counts down from 15 with `delay(1_000L)`, putting `secondsLeft` in the `UiState`. At 0, treat it as a wrong answer. When the user answers, **cancel** the timer.

### Challenge 2: Stopwatch that survives process death 💀 ⭐⭐
*Hint:* save `startedAt`, `isRunning`, and the paused `elapsedMillis` in a `SavedStateHandle` (Chapter 15). `elapsedRealtime()` keeps counting while the app is dead, so if it was running, just start the loop again with the saved `startedAt`! (Note: it resets if the phone **restarts**.)

### Challenge 3: Don't tick in the background 🔋 ⭐⭐
The stopwatch updates its state 100 times per second even when the app is in the background — nobody is looking! Make `uiState` stop ticking when nobody collects it.
*Hint:* keep only `startedAt`, `isRunning`, and `laps` in a `MutableStateFlow`, and build the ticking time as a `flow { while (true) { emit(now()); delay(10) } }`. `combine` them and use `stateIn(viewModelScope, WhileSubscribed(5_000), ...)`. 💡⏲️

### Challenge 4: Download speed 📈 ⭐⭐
Show "**1.2 MB/s**" under the progress bar. Pretend the file is 5 MB. Use the time between two progress values to calculate the speed.

### Challenge 5: Two downloads at once 🐱🐶 ⭐⭐⭐
Download `cute_cat.jpg` **and** `happy_dog.jpg` at the same time, each with its own progress bar. Cancel cancels **both**.
*Hint:* one parent `launch`, two child `launch`es inside it. Cancel the parent → both children stop (the family rules! 👨‍👩‍👧).

---

## 18.26 What Is Next?

You now understand the **engine** under every modern Android app: **coroutines** and **flows**. ⚡🌊 Every chapter from here uses them.

In **Chapter 19: Getting Data From the Internet**, we finally go **online**! 🌐 You will learn:

- How to ask for the **Internet permission** 🔑
- What an **API** and **JSON** are — in simple words 📄
- **Retrofit** — calling the internet with a simple **suspend function** (main-safe, of course! 🛡️)
- **kotlinx.serialization** — turning JSON text into Kotlin data classes (you already know the `@Serializable` word from Navigation!)
- **Loading**, **Success**, and **Error** states with a sealed interface — just like the download you built today ⏳✅❌
- **Retry** buttons and handling "no internet" nicely 📶
- Building an app that shows **real data** from a free web API

**Great work finishing Chapter 18! 🎉 This was one of the hardest chapters in the book — and you did it! 💪**
