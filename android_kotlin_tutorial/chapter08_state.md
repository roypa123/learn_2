# Chapter 8: State — Making Screens Change

> **What you will learn in this chapter**
>
> 1. What **state** is
> 2. Why a normal `var` does **not** update the screen
> 3. `mutableStateOf` — a box that Compose **watches** 👀
> 4. `remember` — giving your Composable a **memory** 🧠
> 5. The `by` keyword — a shorter way to write state
> 6. **Recomposition** — how Compose redraws the screen
> 7. `rememberSaveable` — surviving **screen rotation** 🔄
> 8. State with **lists** and **data classes**
> 9. **State hoisting** — who should own the state ⬆️
> 10. **"State down, events up"** — the one-way data flow
> 11. Building a **Coffee Order** app ☕ that really works
>
> **Time needed:** about 4 to 5 hours. This is **the most important chapter** for Compose. Go slowly! 🐢
>
> **Where to practice:** Android Studio, in your **MyFirstApp** project. **Run the app** or use **Interactive Mode** in the Preview — normal previews don't react to taps.

---

## 8.1 What Is State? 🤔

**State** is **any value that can change over time** and that the screen shows.

Look at any app, and you will find state everywhere:

| App | State |
|---|---|
| A counter app | The **number** |
| Instagram | Is the post **liked**? ❤️ / 🤍 |
| A to-do list | The **list of tasks**, which ones are **done** ✅ |
| Settings | Is **dark mode** on or off? |
| A login screen | What the user **typed** in the boxes |
| A music player | Is it **playing** or **paused**? Which **song**? |
| A shop | **How many** items are in the cart 🛒 |

**Real-life example:** A **light switch** 💡. Its state is **ON** or **OFF**. When the state changes, the room changes (bright or dark).

In Compose:

> **The screen = a picture of the current state.**
> **When the state changes → Compose draws a new picture.** 🖼️➡️🖼️

---

## 8.2 The Problem: A Normal `var` Doesn't Work ❌

Let's try to make a counter with what we know so far.

```kotlin
@Composable
fun BrokenCounter(modifier: Modifier = Modifier) {
    var count = 0

    Column(modifier = modifier.padding(16.dp)) {
        Text("You tapped $count times")
        Button(onClick = {
            count++
            Log.d("Counter", "count is now $count")
        }) {
            Text("Tap me")
        }
    }
}
```

**Run the app** and tap the button many times. What happens?

- 📱 The screen **always** says: `You tapped 0 times`. 😕
- 📝 But **Logcat** says: `count is now 1`, `2`, `3`…

**The number IS changing… but the screen does NOT update!** Why?

### Reason 1: Compose doesn't know the value changed

`count` is a **normal** variable. When it changes, **nobody tells Compose**. Compose has no idea it should redraw the screen.

**Real-life example:** You change the score on a **piece of paper in your pocket** 📝. The **scoreboard** in the stadium doesn't change, because nobody told the scoreboard operator.

We need a special box that **shouts** "*I changed!*" whenever its value changes. 📢

That box is called **`mutableStateOf`**.

---

## 8.3 `mutableStateOf` — A Box That Compose Watches 👀

```kotlin
val count = mutableStateOf(0)
```

| Piece | Meaning |
|---|---|
| `mutableStateOf(0)` | Make a special **state box**, with `0` inside. "Mutable" = can change. |
| `count` | The box. (It's a `val` — the **box** stays the same; the **value inside** changes.) |
| `count.value` | The value **inside** the box. |

```kotlin
Text("You tapped ${count.value} times")   // read the value
count.value++                              // change the value
```

When you **change** `count.value`, the box **tells Compose**: "*I changed! Redraw everyone who reads me!*" 📢

Let's try:

```kotlin
@Composable
fun StillBrokenCounter(modifier: Modifier = Modifier) {
    val count = mutableStateOf(0)

    Column(modifier = modifier.padding(16.dp)) {
        Text("You tapped ${count.value} times")
        Button(onClick = { count.value++ }) {
            Text("Tap me")
        }
    }
}
```

Run it and tap… Still `0`! 😩 Why??

### Reason 2: The Composable forgets everything when it runs again

Here's what happens, step by step:

1. Compose runs `StillBrokenCounter()`. It makes a new box with `0`. Shows "0 times".
2. You tap. `count.value` becomes `1`. The box shouts "*I changed!*" 📢
3. Compose **runs `StillBrokenCounter()` again** to draw the new picture.
4. The first line runs again: `val count = mutableStateOf(0)` → a **brand-new box** with `0`! 😱
5. Shows "0 times".

Every time the function runs, it **starts from zero** — like a **goldfish** 🐠 with a 3-second memory.

We need the Composable to **remember** the box between runs. That's what **`remember`** does. 🧠

---

## 8.4 `remember` — Giving Your Composable a Memory 🧠

```kotlin
val count = remember { mutableStateOf(0) }
```

| Piece | Meaning |
|---|---|
| `remember { ... }` | "The **first** time, run the code in `{ }` and **keep** the result. **Every next time**, give me the **same** kept thing — don't run the code again." |
| `mutableStateOf(0)` | The state box we want to keep. |

Now:

1. First run: `remember` makes the box with `0` and **keeps it**. Shows "0 times".
2. You tap. `count.value` becomes `1`. The box shouts 📢.
3. Compose runs the function again.
4. `remember { ... }` → "I already have a box!" → gives back the **same box** (with `1` inside). ✅
5. Shows "**1 times**". 🎉

### The working counter ✅

```kotlin
@Composable
fun Counter(modifier: Modifier = Modifier) {
    val count = remember { mutableStateOf(0) }

    Column(modifier = modifier.padding(16.dp)) {
        Text("You tapped ${count.value} times")
        Button(onClick = { count.value++ }) {
            Text("Tap me")
        }
    }
}
```

Imports:

```kotlin
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
```

Run it and tap. The number goes up: **1, 2, 3, 4…** 🎉🎉🎉

### You need BOTH ✌️

| You have… | What happens |
|---|---|
| Normal `var` only | Value changes, but Compose **doesn't know**. Screen never updates. ❌ |
| `mutableStateOf` only | Compose knows… but the value is **reset** every time. ❌ |
| `remember { mutableStateOf(...) }` | Compose knows **and** the value is kept. ✅✅ |

**Memory trick:**
- `mutableStateOf` = the **loudspeaker** 📢 ("I changed!")
- `remember` = the **memory** 🧠 ("Keep this between redraws.")

---

## 8.5 The `by` Keyword — A Shorter Way ✨

Writing `.value` everywhere is boring. Kotlin has a trick: **`by`**.

```kotlin
var count by remember { mutableStateOf(0) }
```

Now you use `count` like a **normal variable** — no `.value`!

```kotlin
@Composable
fun Counter(modifier: Modifier = Modifier) {
    var count by remember { mutableStateOf(0) }

    Column(modifier = modifier.padding(16.dp)) {
        Text("You tapped $count times")
        Button(onClick = { count++ }) {
            Text("Tap me")
        }
    }
}
```

### Every bit explained

| Piece | Meaning |
|---|---|
| `var` | Now it's `var`, because **we** change `count` directly. |
| `count` | Looks like a normal `Int`! |
| `by` | "**Hand over** reading and writing to the state box." When you read `count`, Kotlin secretly reads `box.value`. When you write `count++`, Kotlin secretly writes `box.value`. |

This is called a **delegated property** ("by" = "done by someone else"). You don't need to remember the name.

**Real-life example:** A **secretary** 👩‍💼. You say "*send this letter*", and the secretary does all the steps for you. `by` is the secretary for `.value`.

### ⚠️ Two imports needed for `by`

When you write `by remember`, Android Studio may show a **red error**:

> *Property delegate must have a 'getValue(Nothing?, KProperty<*>)' method*

Fix: add these two imports (Alt + Enter usually offers them):

```kotlin
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
```

- `getValue` → needed to **read** `count`.
- `setValue` → needed to **change** `count`.

> 💡 **From now on, this book uses `var x by remember { mutableStateOf(...) }`.** It's what most real apps use.

### Special versions for numbers

For `Int`, `Long`, `Float`, and `Double`, Compose has **faster** versions:

```kotlin
var count by remember { mutableIntStateOf(0) }       // for Int
var volume by remember { mutableFloatStateOf(0.5f) } // for Float
var price by remember { mutableDoubleStateOf(9.99) } // for Double
var bigNum by remember { mutableLongStateOf(0L) }    // for Long
```

Android Studio will even show a **yellow hint** if you use `mutableStateOf(0)`, suggesting `mutableIntStateOf(0)`. Both work; the special version is slightly faster. ⚡

---

## 8.6 Recomposition — How Compose Redraws 🔁

**Recomposition** is a big word for a simple idea:

> **When state changes, Compose runs the Composable functions that READ that state again, to make a new picture.**

### Step by step

```kotlin
@Composable
fun Counter() {
    var count by remember { mutableIntStateOf(0) }      // (1)
    Column {
        Text("Count: $count")                           // (2) reads count
        Button(onClick = { count++ }) {                 // (3)
            Text("Add")
        }
        Text("This text never changes")                 // (4)
    }
}
```

```
 ┌───────────────────────┐
 │ FIRST TIME (composition)
 │  - remember makes the box: count = 0
 │  - draws "Count: 0", the button, the other text
 └───────────────────────┘
            │
      user taps "Add"
            │
            ▼
 ┌───────────────────────┐
 │ onClick runs: count++  →  count = 1
 │ The box shouts: "I changed!" 📢
 └───────────────────────┘
            │
            ▼
 ┌───────────────────────┐
 │ RECOMPOSITION
 │  - Compose runs Counter() again
 │  - remember gives back the SAME box (count = 1)
 │  - "Count: 1" is drawn ✅
 │  - Parts that didn't change may be SKIPPED (smart!) ⚡
 └───────────────────────┘
```

### Smart skipping ⚡

Compose is **clever**: it tries to redraw **only** the parts that need it. If `Text("This text never changes")` has the same input as before, Compose can **skip** it. That's why Compose is fast, even with big screens.

### Important rules that come from recomposition

**Rule 1: Composables can run MANY times.** Maybe 60 times a second during an animation! So:
- Keep them **fast**. ⚡
- Don't do slow work (like downloading) directly in them. (We learn the right way in Chapter 18.)

**Rule 2: Don't change state while drawing.** ❌

```kotlin
@Composable
fun BadExample() {
    var count by remember { mutableIntStateOf(0) }
    count++                         // ❌ changes state while drawing!
    Text("Count: $count")
}
```

This causes an **endless loop**: draw → change → redraw → change → redraw… 🔄💥
✅ Change state **only in events**: `onClick = { ... }`, `onValueChange = { ... }`, etc.

**Rule 3: Values calculated from state update automatically.**

```kotlin
var count by remember { mutableIntStateOf(0) }
val isEven = count % 2 == 0          // ✅ calculated fresh every recomposition
val message = if (isEven) "Even 🟦" else "Odd 🟥"

Text(message)
```

You don't need a second state for `isEven`. Just **calculate it** from `count`. When `count` changes, the function runs again and `isEven` is recalculated. ✨

> 💡 **Golden rule:** Keep the **smallest** amount of state possible. Everything you can **calculate** from it, calculate it.

---

## 8.7 Small Examples You Can Try 🧪

### Example 1: Like button ❤️ (Boolean state)

```kotlin
@Composable
fun LikeButton(modifier: Modifier = Modifier) {
    var liked by remember { mutableStateOf(false) }

    IconButton(onClick = { liked = !liked }, modifier = modifier) {
        Icon(
            imageVector = if (liked) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
            contentDescription = if (liked) "Unlike" else "Like",
            tint = if (liked) Color.Red else MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
```

| Code | Meaning |
|---|---|
| `var liked by remember { mutableStateOf(false) }` | Starts **not** liked. |
| `liked = !liked` | **Flip** it: `false` → `true` → `false`… (Chapter 2: `!` = NOT) |
| `if (liked) ... else ...` | Choose the **icon**, **description**, and **color** from the state. |

Imports: `androidx.compose.material.icons.outlined.FavoriteBorder`

Tap → ❤️. Tap again → 🤍.

### Example 2: Light switch 💡

```kotlin
@Composable
fun LightRoom(modifier: Modifier = Modifier) {
    var isOn by remember { mutableStateOf(false) }

    Column(
        modifier = modifier
            .fillMaxWidth()
            .height(250.dp)
            .background(if (isOn) Color(0xFFFFF59D) else Color(0xFF263238)),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(text = if (isOn) "💡" else "🌑", fontSize = 64.sp)
        Spacer(modifier = Modifier.height(16.dp))
        Switch(
            checked = isOn,
            onCheckedChange = { newValue -> isOn = newValue }
        )
    }
}
```

| Code | Meaning |
|---|---|
| `.background(if (isOn) yellow else dark)` | The **room color** comes from the state. |
| `Switch(checked = isOn, ...)` | A Material **switch**. It shows the state we give it. |
| `onCheckedChange = { newValue -> isOn = newValue }` | When the user flips it, the switch **tells us** the new value. **We** update the state. |

👀 **Important idea:** The `Switch` does **not** change by itself! It only **shows** `checked`, and **tells us** when the user wants to change it. **We** decide. This is the pattern of **almost every input** in Compose (more in 8.10).

### Example 3: Show and hide (with `if`)

```kotlin
@Composable
fun SecretMessage(modifier: Modifier = Modifier) {
    var visible by remember { mutableStateOf(false) }

    Column(modifier = modifier.padding(16.dp)) {
        Button(onClick = { visible = !visible }) {
            Text(if (visible) "Hide secret" else "Show secret")
        }
        if (visible) {
            Text(
                text = "🤫 Kotlin was named after an island near St. Petersburg!",
                modifier = Modifier.padding(top = 8.dp)
            )
        }
    }
}
```

- When `visible` is `false`, the `Text` is **not drawn at all** — it's not in the picture.
- When it becomes `true`, recomposition **adds** it. ✨

### Example 4: A dice 🎲 (random state)

```kotlin
@Composable
fun Dice(modifier: Modifier = Modifier) {
    var number by remember { mutableIntStateOf(1) }
    val faces = listOf("⚀", "⚁", "⚂", "⚃", "⚄", "⚅")

    Column(
        modifier = modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(text = faces[number - 1], fontSize = 96.sp)
        Text("You rolled: $number")
        Spacer(modifier = Modifier.height(8.dp))
        Button(onClick = { number = (1..6).random() }) {
            Text("Roll 🎲")
        }
    }
}
```

- `(1..6).random()` → a random number from 1 to 6.
- `faces[number - 1]` → lists start at **0** (Chapter 3), so number 1 → index 0.

---

## 8.8 `rememberSaveable` — Surviving Rotation 🔄

### The problem

Run the `Counter`. Tap it until it shows **7**. Now **rotate** the phone (or emulator) 📱↪️.

The counter goes back to **0**! 😱

### Why?

When the phone rotates (or changes language, or dark mode), Android **destroys** the screen (the Activity) and **builds it again** from scratch. This is called a **configuration change**.

`remember` keeps values only **while the Composable lives**. When the whole screen is rebuilt, `remember`'s memory is **gone**. 🧠💨

> 🔄 **How to rotate the emulator:** click the **rotate** buttons ↺ ↻ on the emulator's side toolbar. Make sure **auto-rotate** is on in the emulator's quick settings.

### The fix: `rememberSaveable`

```kotlin
var count by rememberSaveable { mutableIntStateOf(0) }
```

Import: `androidx.compose.runtime.saveable.rememberSaveable`

- `rememberSaveable` = `remember` + **saves the value** in a safe place before the screen is destroyed, and **gives it back** after. 💾
- Rotate now → still **7**! ✅

**Real-life example:** Moving to a new house 🏠➡️🏠.
- `remember` = things on your desk. When you move, they're **lost**.
- `rememberSaveable` = things you **packed in a box** 📦. They arrive at the new house safely.

### `remember` vs `rememberSaveable`

| | `remember` | `rememberSaveable` |
|---|---|---|
| Survives recomposition | ✅ | ✅ |
| Survives rotation / dark mode / language change | ❌ | ✅ |
| Survives the app being killed by Android in the background | ❌ | ✅ (usually) |
| What can it hold? | **Anything** | **Simple types**: numbers, Strings, Booleans, enums, and some lists. (More needs extra work.) |

### When to use which?

| Use `rememberSaveable` for… | Use `remember` for… |
|---|---|
| What the **user typed** ⌨️ | Things that are cheap to **calculate again** |
| Which **tab** is selected | Your own objects that **can't be saved** easily |
| Counters, toggles, selections | Temporary UI details |

> 💡 **Simple rule for beginners:** If losing the value on rotation would **annoy the user**, use `rememberSaveable`.

> ℹ️ Later, in **Chapter 15**, we'll keep important state in a **ViewModel**, which also survives rotation, and is the professional way for screen data.

---

## 8.9 State With Lists and Data Classes 📋

### ⚠️ The trap: a normal mutable list inside state

```kotlin
var items by remember { mutableStateOf(mutableListOf("Apple")) }

Button(onClick = { items.add("Banana") }) { Text("Add") }   // ❌ screen does NOT update!
```

Why? `items.add(...)` changes **inside** the list, but the **state box** still holds the **same list object**. The box didn't get a **new value**, so it doesn't shout 📢. Compose doesn't know!

### ✅ Way 1: Use a read-only list and replace it

```kotlin
var items by remember { mutableStateOf(listOf("Apple")) }

Button(onClick = { items = items + "Banana" }) { Text("Add") }   // ✅
```

| Code | Meaning |
|---|---|
| `listOf("Apple")` | A **read-only** list. |
| `items + "Banana"` | Makes a **new** list: `["Apple", "Banana"]`. The old one is not changed. |
| `items = ...` | Put the **new list** in the box → the box shouts 📢 → screen updates. ✅ |

Removing works the same way:

```kotlin
items = items - "Apple"                       // remove by value
items = items.filter { it != "Apple" }        // remove with a rule (Chapter 3!)
```

### ✅ Way 2: `mutableStateListOf` — a list that shouts by itself

```kotlin
val items = remember { mutableStateListOf("Apple") }

Button(onClick = { items.add("Banana") }) { Text("Add") }   // ✅ works!
```

Import: `androidx.compose.runtime.mutableStateListOf`

- `mutableStateListOf` is a **special list** that tells Compose whenever you `add`, `remove`, or change an item.
- Notice: `val` (the list stays the same object) and **no** `by`.

| | Way 1: `mutableStateOf(listOf(...))` | Way 2: `mutableStateListOf(...)` |
|---|---|---|
| Change it | `items = items + x` (new list) | `items.add(x)` |
| Style | "Replace the whole thing" (safer, very common with ViewModels) | "Change in place" (easy for quick lists) |

### A small shopping list example 🛒

```kotlin
@Composable
fun ShoppingList(modifier: Modifier = Modifier) {
    var items by remember { mutableStateOf(listOf("Milk", "Bread")) }
    var counter by remember { mutableIntStateOf(1) }

    Column(modifier = modifier.padding(16.dp)) {
        Text("Items: ${items.size}", style = MaterialTheme.typography.titleMedium)

        items.forEach { item ->
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(text = "• $item", modifier = Modifier.weight(1f))
                TextButton(onClick = { items = items - item }) {
                    Text("Remove")
                }
            }
        }

        Button(onClick = {
            items = items + "New item $counter"
            counter++
        }) {
            Text("Add item")
        }
    }
}
```

- `items.forEach { ... }` draws **one row per item**. When the list changes, the rows change. ✨
- **Remove** creates a new list **without** that item.

> ℹ️ For **long** lists, we'll use `LazyColumn` in **Chapter 10**.

### State with a data class (use `copy`!)

```kotlin
data class Profile(val name: String, val age: Int, val isPremium: Boolean)

@Composable
fun ProfileEditor(modifier: Modifier = Modifier) {
    var profile by remember { mutableStateOf(Profile("Roy", 10, false)) }

    Column(modifier = modifier.padding(16.dp)) {
        Text("${profile.name}, ${profile.age} years ${if (profile.isPremium) "⭐" else ""}")

        Button(onClick = { profile = profile.copy(age = profile.age + 1) }) {
            Text("Birthday 🎂")
        }
        Button(onClick = { profile = profile.copy(isPremium = !profile.isPremium) }) {
            Text("Toggle premium")
        }
    }
}
```

- `profile.copy(age = ...)` makes a **new** Profile with one change (Chapter 3!) → we put it in the box → 📢 → screen updates.
- ❌ Don't use `var` properties inside the data class and change them directly (`profile.age++`) — Compose won't notice, same trap as the list.

> 💡 **Rule:** Inside state, use **`val`** properties and **read-only** lists. To change, make a **new** value (`copy`, `+`, `-`, `filter`, `map`). This is called **immutable state**, and it's the professional way. ✅

---

## 8.10 State Hoisting — Who Owns the State? ⬆️

### The problem

Look at our `Counter`. It **owns** its state **inside**. That's fine for small things, but:

- ❓ What if **another** part of the screen needs to know the count? (Like a "Total: 5" at the top.)
- ❓ What if we want to **reset** it from a different button?
- ❓ How do we **test** it, or show it in a preview with the number 42?

The state is **locked inside** the Composable. Nobody else can see or change it. 🔒

### The solution: move the state **up** (hoist it)

**Hoisting** = lifting something **up** (like a flag on a pole 🚩).

We move the state **out** of the Composable, **up** to its **parent**. The Composable gets:
1. The **value** to show (as an input).
2. A **lambda** to call when something should change (an **event**).

**Before (stateful — owns its state):**

```kotlin
@Composable
fun Counter() {
    var count by remember { mutableIntStateOf(0) }
    Button(onClick = { count++ }) {
        Text("Count: $count")
    }
}
```

**After (stateless — gets state from outside):**

```kotlin
@Composable
fun Counter(
    count: Int,                    // 1. the value to show ⬇️
    onIncrement: () -> Unit,       // 2. "please add one!" ⬆️
    modifier: Modifier = Modifier
) {
    Button(onClick = onIncrement, modifier = modifier) {
        Text("Count: $count")
    }
}
```

And the **parent** owns the state:

```kotlin
@Composable
fun CounterScreen() {
    var count by rememberSaveable { mutableIntStateOf(0) }

    Column {
        Text("Total taps: $count")
        Counter(
            count = count,
            onIncrement = { count++ }
        )
        TextButton(onClick = { count = 0 }) {
            Text("Reset")
        }
    }
}
```

### Every bit explained

| Code | Meaning |
|---|---|
| `count: Int` | The counter **receives** the number. It doesn't own it. |
| `onIncrement: () -> Unit` | A **lambda input** (Chapter 3): "a function with no inputs that gives nothing". The counter **calls** it when tapped. |
| `Button(onClick = onIncrement)` | We pass the lambda straight to the button. (Same as `onClick = { onIncrement() }`.) |
| In the parent: `onIncrement = { count++ }` | The **parent** decides **what happens**. |
| `TextButton(onClick = { count = 0 })` | Now **another** button can reset the count! ✅ |
| `Text("Total taps: $count")` | And **another** text can show it! ✅ |

**Real-life example:** A **TV remote** 📺.
- The **remote** (stateless Composable) doesn't know what channel is on. It just has buttons, and when you press one it **sends a signal** ("*channel up!*").
- The **TV** (parent) **owns** the state (the current channel) and **decides** what to do.
- Because of this, you can have **two** remotes for one TV! 📺📲📲

### "State down, events up" ⬇️⬆️

This is the **most important pattern** in Compose. It's called **unidirectional data flow** (one-way flow):

```
          ┌──────────────────────┐
          │   Parent (owns state) │
          │   count = 5           │
          └──────────────────────┘
             │              ▲
   STATE ⬇️  │ count = 5     │ onIncrement()  ⬆️ EVENTS
             ▼              │
          ┌──────────────────────┐
          │  Counter (stateless)  │
          │  shows "Count: 5"     │
          │  [button tapped!] ────┘
          └──────────────────────┘
```

1. **State flows DOWN** ⬇️ — the parent gives values to its children.
2. **Events flow UP** ⬆️ — children tell the parent "*something happened*" by calling lambdas.
3. The **parent** changes the state → recomposition → new values flow down again. 🔁

### You already used this pattern!

```kotlin
Switch(
    checked = isOn,                              // state ⬇️
    onCheckedChange = { newValue -> isOn = newValue }   // event ⬆️
)
```

The Material `Switch` is a **stateless** Composable! So are `Checkbox`, `Slider`, `TextField`… They all follow:

> **`value` + `onValueChange`**

### Naming the lambdas

By custom, event lambdas start with **`on`**:

| Name | Type | Meaning |
|---|---|---|
| `onClick` | `() -> Unit` | "Something was tapped." |
| `onIncrement` | `() -> Unit` | "Please add one." |
| `onCheckedChange` | `(Boolean) -> Unit` | "The user wants this new true/false value." |
| `onValueChange` | `(String) -> Unit` | "The user typed; here is the new text." |
| `onSizeSelected` | `(CoffeeSize) -> Unit` | "The user picked this size." |

### How high should state go?

> **Hoist the state to the lowest common parent of everyone who needs it.**

- Only the counter needs it? Keep it **inside** (stateful is fine). 👍
- The counter **and** a total text need it? Move it to their **shared parent**. ⬆️
- **Many screens** need it? Move it into a **ViewModel** (Chapter 15). ⬆️⬆️

### Why stateless Composables are great ✨

| Benefit | Why |
|---|---|
| **Reusable** ♻️ | Use the same `Counter` for apples, oranges, anything. |
| **Easy previews** 👀 | `Counter(count = 42, onIncrement = {})` — see any number instantly. |
| **Easy to test** 🧪 | Give inputs, check what is shown. |
| **One source of truth** ✅ | The state lives in **one** place. No two copies that disagree. |

> 💡 **A common pattern:** Make a **stateless** version for the real work, and a small **stateful** wrapper for convenience:
> ```kotlin
> @Composable
> fun Counter(modifier: Modifier = Modifier) {           // stateful wrapper
>     var count by rememberSaveable { mutableIntStateOf(0) }
>     Counter(count = count, onIncrement = { count++ }, modifier = modifier)
> }
> ```
> Two functions with the **same name** but **different inputs** is allowed in Kotlin. It's called **overloading**.

---

## 8.11 Build It: A Coffee Order App ☕

Let's build a real, working order screen. It uses **everything** from this chapter.

```
┌──────────────────────────────────┐
│ ☕ Coffee Order                   │
│                                  │
│ Choose your size                 │
│ [ Small ] [■Medium■] [ Large ]   │  ← one is selected (state)
│                                  │
│ Cups                             │
│        [ − ]   2   [ + ]         │  ← hoisted QuantitySelector
│                                  │
│ Extras                           │
│ Extra sugar 🍬           [  ●]   │  ← Switch
│ Whipped cream 🍦         [●  ]   │  ← Switch
│                                  │
│ ──────────────────────────────── │
│ Total                    $8.00   │  ← calculated from state
│                                  │
│ [        Place order        ]    │
│                                  │
│ ╭──────────────────────────────╮ │  ← appears only after ordering
│ │ ✅ Order placed!              │ │
│ │ 2 × Medium coffee, sugar      │ │
│ │              [New order]      │ │
│ ╰──────────────────────────────╯ │
└──────────────────────────────────┘
```

### The full code

Replace **everything** in `MainActivity.kt` (keep your own `package` line and theme import):

```kotlin
package com.example.myfirstapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.myfirstapp.ui.theme.MyFirstAppTheme

// ---------- Data ----------

enum class CoffeeSize(val label: String, val price: Double) {
    SMALL("Small", 2.50),
    MEDIUM("Medium", 3.50),
    LARGE("Large", 4.50)
}

const val SUGAR_PRICE = 0.25
const val CREAM_PRICE = 0.75

fun Double.toMoney(): String = "$" + String.format("%.2f", this)

// ---------- Activity ----------

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyFirstAppTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    CoffeeOrderScreen(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

// ---------- Screen (owns the state) ----------

@Composable
fun CoffeeOrderScreen(modifier: Modifier = Modifier) {
    // 1. STATE — the smallest set of values that can change
    var size by rememberSaveable { mutableStateOf(CoffeeSize.MEDIUM) }
    var cups by rememberSaveable { mutableIntStateOf(1) }
    var sugar by rememberSaveable { mutableStateOf(false) }
    var cream by rememberSaveable { mutableStateOf(false) }
    var orderPlaced by rememberSaveable { mutableStateOf(false) }

    // 2. CALCULATED from state (not state itself!)
    val pricePerCup = size.price +
        (if (sugar) SUGAR_PRICE else 0.0) +
        (if (cream) CREAM_PRICE else 0.0)
    val total = pricePerCup * cups

    // 3. UI — state flows down ⬇️, events flow up ⬆️
    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = "☕ Coffee Order",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold
        )

        SectionTitle("Choose your size")
        SizeSelector(
            selected = size,
            onSizeSelected = { newSize -> size = newSize }
        )

        SectionTitle("Cups")
        QuantitySelector(
            quantity = cups,
            onDecrease = { if (cups > 1) cups-- },
            onIncrease = { if (cups < 10) cups++ },
            modifier = Modifier.align(Alignment.CenterHorizontally)
        )

        SectionTitle("Extras")
        ExtraRow(
            label = "Extra sugar 🍬 (+${SUGAR_PRICE.toMoney()})",
            checked = sugar,
            onCheckedChange = { sugar = it }
        )
        ExtraRow(
            label = "Whipped cream 🍦 (+${CREAM_PRICE.toMoney()})",
            checked = cream,
            onCheckedChange = { cream = it }
        )

        HorizontalDivider()

        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Total", style = MaterialTheme.typography.titleLarge)
            Spacer(modifier = Modifier.weight(1f))
            Text(
                text = total.toMoney(),
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
        }

        Button(
            onClick = { orderPlaced = true },
            enabled = !orderPlaced,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Place order")
        }

        if (orderPlaced) {
            OrderSummary(
                cups = cups,
                size = size,
                sugar = sugar,
                cream = cream,
                total = total,
                onNewOrder = {
                    size = CoffeeSize.MEDIUM
                    cups = 1
                    sugar = false
                    cream = false
                    orderPlaced = false
                }
            )
        }
    }
}

// ---------- Stateless parts ----------

@Composable
fun SectionTitle(text: String, modifier: Modifier = Modifier) {
    Text(
        text = text,
        style = MaterialTheme.typography.titleMedium,
        fontWeight = FontWeight.Bold,
        modifier = modifier
    )
}

@Composable
fun SizeSelector(
    selected: CoffeeSize,
    onSizeSelected: (CoffeeSize) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        CoffeeSize.entries.forEach { coffeeSize ->
            val buttonModifier = Modifier.weight(1f)
            if (coffeeSize == selected) {
                Button(
                    onClick = { onSizeSelected(coffeeSize) },
                    modifier = buttonModifier
                ) {
                    Text(coffeeSize.label)
                }
            } else {
                OutlinedButton(
                    onClick = { onSizeSelected(coffeeSize) },
                    modifier = buttonModifier
                ) {
                    Text(coffeeSize.label)
                }
            }
        }
    }
}

@Composable
fun QuantitySelector(
    quantity: Int,
    onDecrease: () -> Unit,
    onIncrease: () -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier,
        verticalAlignment = Alignment.CenterVertically
    ) {
        FilledTonalButton(onClick = onDecrease, enabled = quantity > 1) {
            Text("−", style = MaterialTheme.typography.titleLarge)
        }
        Text(
            text = quantity.toString(),
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(horizontal = 24.dp)
        )
        FilledTonalButton(onClick = onIncrease, enabled = quantity < 10) {
            Text("+", style = MaterialTheme.typography.titleLarge)
        }
    }
}

@Composable
fun ExtraRow(
    label: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodyLarge,
            modifier = Modifier.weight(1f)
        )
        Spacer(modifier = Modifier.width(8.dp))
        Switch(checked = checked, onCheckedChange = onCheckedChange)
    }
}

@Composable
fun OrderSummary(
    cups: Int,
    size: CoffeeSize,
    sugar: Boolean,
    cream: Boolean,
    total: Double,
    onNewOrder: () -> Unit,
    modifier: Modifier = Modifier
) {
    val extras = buildList {
        if (sugar) add("sugar")
        if (cream) add("cream")
    }
    val extrasText = if (extras.isEmpty()) "no extras" else extras.joinToString(" and ")

    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        ),
        modifier = modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "✅ Order placed!",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )
            Text("$cups × ${size.label} coffee, $extrasText")
            Text("You paid ${total.toMoney()}")
            TextButton(
                onClick = onNewOrder,
                modifier = Modifier.align(Alignment.End)
            ) {
                Text("New order")
            }
        }
    }
}

// ---------- Previews ----------

@Preview(showBackground = true, showSystemUi = true)
@Composable
fun CoffeeOrderPreview() {
    MyFirstAppTheme {
        Surface {
            CoffeeOrderScreen()
        }
    }
}

@Preview(showBackground = true)
@Composable
fun QuantitySelectorPreview() {
    MyFirstAppTheme {
        QuantitySelector(quantity = 7, onDecrease = {}, onIncrease = {})
    }
}
```

### Every part explained

#### Part 1: The data

```kotlin
enum class CoffeeSize(val label: String, val price: Double) {
    SMALL("Small", 2.50),
    MEDIUM("Medium", 3.50),
    LARGE("Large", 4.50)
}
```

- An **enum** (Chapter 4) — exactly 3 sizes, each with a label and a price.
- Enums work with `rememberSaveable` out of the box. ✅

```kotlin
const val SUGAR_PRICE = 0.25
const val CREAM_PRICE = 0.75
```

- **Constants** (Chapter 4) — fixed prices. If the price changes, change it in **one** place.

```kotlin
fun Double.toMoney(): String = "$" + String.format("%.2f", this)
```

- An **extension function** (Chapter 4) on `Double`.
- `String.format("%.2f", this)` → show the number with **exactly 2 digits** after the dot: `8.0` → `"8.00"`, `3.5` → `"3.50"`.
- `"$" + ...` → add a dollar sign. Result: `8.0.toMoney()` → `"$8.00"`. 💵

#### Part 2: The state (in `CoffeeOrderScreen`)

```kotlin
    var size by rememberSaveable { mutableStateOf(CoffeeSize.MEDIUM) }
    var cups by rememberSaveable { mutableIntStateOf(1) }
    var sugar by rememberSaveable { mutableStateOf(false) }
    var cream by rememberSaveable { mutableStateOf(false) }
    var orderPlaced by rememberSaveable { mutableStateOf(false) }
```

- **5 pieces of state** — the **smallest** set of things that can change.
- All use `rememberSaveable` → rotate the phone, and your order is **still there**. 🔄✅
- The **screen** owns all the state. The small parts below are **stateless**.

#### Part 3: Calculated values (NOT state)

```kotlin
    val pricePerCup = size.price +
        (if (sugar) SUGAR_PRICE else 0.0) +
        (if (cream) CREAM_PRICE else 0.0)
    val total = pricePerCup * cups
```

- `total` is **not** a state! It's **calculated** from `size`, `sugar`, `cream`, and `cups`.
- When any of them changes → recomposition → `total` is calculated again **automatically**. ✨
- Example: Medium (3.50) + sugar (0.25) = 3.75 per cup × 2 cups = **$7.50**.

> 💡 If you made `total` a state too, you would have to **remember** to update it every time something changes. Easy to forget → bugs! 🐛 Calculating it is **always correct**.

#### Part 4: `SizeSelector` — hoisted selection

```kotlin
@Composable
fun SizeSelector(
    selected: CoffeeSize,                         // state ⬇️
    onSizeSelected: (CoffeeSize) -> Unit,         // event ⬆️
    modifier: Modifier = Modifier
) {
```

| Code | Meaning |
|---|---|
| `onSizeSelected: (CoffeeSize) -> Unit` | A lambda that **takes a size**. The selector says "*the user picked THIS one*". |
| `CoffeeSize.entries.forEach { ... }` | One button **for each** size (Chapter 4: `entries`). |
| `if (coffeeSize == selected) Button(...) else OutlinedButton(...)` | The **selected** size gets a filled button; the others get outlined buttons. |
| `onClick = { onSizeSelected(coffeeSize) }` | Tell the parent which size was tapped. |
| `Modifier.weight(1f)` | Three equal-width buttons (Chapter 6). |

And in the parent:

```kotlin
        SizeSelector(
            selected = size,
            onSizeSelected = { newSize -> size = newSize }
        )
```

The **parent** updates the state → recomposition → the selector gets the new `selected` → the right button is filled. 🔁

#### Part 5: `QuantitySelector` — two events

```kotlin
        QuantitySelector(
            quantity = cups,
            onDecrease = { if (cups > 1) cups-- },
            onIncrease = { if (cups < 10) cups++ },
            ...
        )
```

- The **parent** decides the **rules**: at least 1 cup, at most 10.
- Inside the selector, `enabled = quantity > 1` greys out the **−** button at 1. Nice! 👌
- Look at `QuantitySelectorPreview` — we show it with `quantity = 7` and **empty** lambdas `{}`. Easy previews: a benefit of stateless Composables!

#### Part 6: `ExtraRow` — passing the lambda straight through

```kotlin
        ExtraRow(
            label = "...",
            checked = sugar,
            onCheckedChange = { sugar = it }
        )
```

- `{ sugar = it }` → `it` is the new `Boolean` from the Switch (Chapter 3: `it` = the one input).
- Inside `ExtraRow`: `Switch(checked = checked, onCheckedChange = onCheckedChange)` → we give the Switch **our** lambda directly. The event goes up **two** levels: Switch → ExtraRow → Screen. ⬆️⬆️

#### Part 7: Placing the order

```kotlin
        Button(
            onClick = { orderPlaced = true },
            enabled = !orderPlaced,
            modifier = Modifier.fillMaxWidth()
        ) { Text("Place order") }

        if (orderPlaced) {
            OrderSummary(..., onNewOrder = { ... reset everything ... })
        }
```

- Tap → `orderPlaced = true` → the button becomes **disabled** and the **summary card appears**. ✨
- `onNewOrder` **resets** all 5 states → the card **disappears**, and everything is back to the start.

#### Part 8: `OrderSummary` — building text from state

```kotlin
    val extras = buildList {
        if (sugar) add("sugar")
        if (cream) add("cream")
    }
    val extrasText = if (extras.isEmpty()) "no extras" else extras.joinToString(" and ")
```

- `buildList` (Chapter 4) → a list of only the chosen extras.
- Result: `"no extras"`, `"sugar"`, `"cream"`, or `"sugar and cream"`. Nice English! 📝

### Run it! ▶️

1. Pick **Large**. The total changes.
2. Tap **+** a few times. The total changes.
3. Turn on **sugar** and **cream**. The total changes.
4. **Rotate** the phone 🔄 — everything is still there!
5. Tap **Place order** — the summary appears. ✅
6. Tap **New order** — everything resets.

🎉 **Your first truly interactive app!**

### Try Interactive Mode in the Preview 👆

At the top of `CoffeeOrderPreview`, click **Start Interactive Mode**. Now you can tap the buttons **inside the preview**, without running the app!

---

## 8.12 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| `var count = 0` in a Composable | Screen never updates | `var count by remember { mutableIntStateOf(0) }` |
| `mutableStateOf` without `remember` | Value resets to the start every time | Wrap it: `remember { mutableStateOf(...) }` |
| `by remember` shows a red error | *Property delegate must have a 'getValue'...* | Import `androidx.compose.runtime.getValue` and `setValue`. |
| `val x by remember { ... }` then `x = 5` | *Val cannot be reassigned* | Use `var` with `by`. |
| Value resets after rotation | `remember` forgets on configuration change | Use `rememberSaveable`. |
| `mutableListOf` inside state + `.add()` | Screen doesn't update | Use `items = items + x`, or `mutableStateListOf`. |
| Changing a `var` property inside a data class in state | Screen doesn't update | Use `val` properties and `state = state.copy(...)`. |
| Changing state directly in the Composable body | Endless recomposition loop 🔄💥 | Change state only inside events (`onClick`, …). |
| Two states that must agree (e.g., `count` and `isEven`) | They get out of sync → bugs | Keep one state, **calculate** the other. |
| A `Switch`/`Checkbox` doesn't move | You didn't update the state in `onCheckedChange` | `onCheckedChange = { isOn = it }` |
| `rememberSaveable` with your own class | Crash: *...cannot be saved using the current SaveableStateRegistry* | Use simple types, an enum, or `remember` (or a ViewModel later). |
| Normal Preview doesn't react to taps | Previews are pictures | Use **Interactive Mode** or run the app. |

---

## 8.13 Summary — What You Learned 🎓

✅ **State** = any value that changes and is shown on screen. **Screen = a picture of the state.**

✅ A normal `var` doesn't work: Compose doesn't know it changed, and it resets every run.

✅ **`mutableStateOf`** = a box that tells Compose when it changes 📢. **`remember`** = keeps it between runs 🧠. You need both.

✅ **`var x by remember { mutableStateOf(...) }`** — the short way (imports: `getValue`, `setValue`).
Special versions: `mutableIntStateOf`, `mutableFloatStateOf`, …

✅ **Recomposition** = Compose runs Composables again when the state they read changes. Keep them fast; change state only in events; calculate what you can.

✅ **`rememberSaveable`** survives rotation and other configuration changes.

✅ **Lists and data classes in state:** replace with a new value (`+`, `-`, `filter`, `copy`), or use `mutableStateListOf`.

✅ **State hoisting:** move state up; pass **value** ⬇️ and **event lambdas** ⬆️. Stateless Composables are reusable, previewable, and testable.

✅ **"State down, events up"** — the one-way data flow. `Switch`, `Checkbox`, `TextField` all work this way.

✅ You built a working **Coffee Order** app ☕!

---

## 8.14 Practice Time 🏋️

**Task 1 — Counter with minus:**
Make a counter with **−** and **+** buttons and a **Reset** button. The number can't go below 0.

**Task 2 — Color changer:**
A `Box` (200 × 200 dp) that changes color **each time it's tapped**: red → green → blue → red… (Hint: a list of colors and an index state.)

**Task 3 — Hoist it:**
Take your counter from Task 1 and make it **stateless**: `CounterControls(count: Int, onMinus: () -> Unit, onPlus: () -> Unit, onReset: () -> Unit)`. Then use **two** separate counters on one screen (for "Apples 🍎" and "Oranges 🍊") and show `"Total fruits: X"` at the top.

**Task 4 — Name list:**
A screen with a button "Add name". Each tap adds `"Person 1"`, `"Person 2"`, … to a list shown below. Each name has a "❌" button to remove it. Show `"No people yet"` when the list is empty.

**Task 5 — Find the bug 🐛:**
Why does this not work? Fix it.

```kotlin
@Composable
fun Mystery() {
    val clicks = remember { mutableStateOf(0) }
    Button(onClick = { clicks++ }) {
        Text("Clicked $clicks times")
    }
}
```

**Task 6 — Thinking question 🤔:**
In the Coffee app, why is `total` **not** a state with `remember`?

---

### Answers

**Task 1:**

```kotlin
@Composable
fun MinusPlusCounter(modifier: Modifier = Modifier) {
    var count by rememberSaveable { mutableIntStateOf(0) }

    Column(
        modifier = modifier.padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(text = "$count", style = MaterialTheme.typography.displayMedium)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = { if (count > 0) count-- }, enabled = count > 0) {
                Text("−")
            }
            Button(onClick = { count++ }) {
                Text("+")
            }
        }
        TextButton(onClick = { count = 0 }) {
            Text("Reset")
        }
    }
}
```

**Task 2:**

```kotlin
@Composable
fun ColorChanger(modifier: Modifier = Modifier) {
    val colors = listOf(Color.Red, Color.Green, Color.Blue)
    var index by remember { mutableIntStateOf(0) }

    Box(
        modifier = modifier
            .size(200.dp)
            .background(colors[index])
            .clickable { index = (index + 1) % colors.size }
    )
}
```

`(index + 1) % colors.size` → `0 → 1 → 2 → 0 → …` The **remainder** `%` (Chapter 2) makes it go back to 0. 🔁

**Task 3:**

```kotlin
@Composable
fun CounterControls(
    label: String,
    count: Int,
    onMinus: () -> Unit,
    onPlus: () -> Unit,
    onReset: () -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(text = "$label: $count", modifier = Modifier.weight(1f))
        TextButton(onClick = onMinus, enabled = count > 0) { Text("−") }
        TextButton(onClick = onPlus) { Text("+") }
        TextButton(onClick = onReset) { Text("Reset") }
    }
}

@Composable
fun FruitScreen(modifier: Modifier = Modifier) {
    var apples by rememberSaveable { mutableIntStateOf(0) }
    var oranges by rememberSaveable { mutableIntStateOf(0) }

    Column(modifier = modifier.padding(16.dp)) {
        Text(
            text = "Total fruits: ${apples + oranges}",
            style = MaterialTheme.typography.titleLarge
        )
        CounterControls(
            label = "Apples 🍎",
            count = apples,
            onMinus = { if (apples > 0) apples-- },
            onPlus = { apples++ },
            onReset = { apples = 0 }
        )
        CounterControls(
            label = "Oranges 🍊",
            count = oranges,
            onMinus = { if (oranges > 0) oranges-- },
            onPlus = { oranges++ },
            onReset = { oranges = 0 }
        )
    }
}
```

**One** stateless Composable, used **twice** with different state. And the total is **calculated**. ♻️✨

**Task 4:**

```kotlin
@Composable
fun NameList(modifier: Modifier = Modifier) {
    var names by remember { mutableStateOf(listOf<String>()) }
    var nextNumber by remember { mutableIntStateOf(1) }

    Column(modifier = modifier.padding(16.dp)) {
        Button(onClick = {
            names = names + "Person $nextNumber"
            nextNumber++
        }) {
            Text("Add name")
        }

        if (names.isEmpty()) {
            Text("No people yet", modifier = Modifier.padding(top = 8.dp))
        } else {
            names.forEach { name ->
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(text = name, modifier = Modifier.weight(1f))
                    TextButton(onClick = { names = names - name }) {
                        Text("❌")
                    }
                }
            }
        }
    }
}
```

`listOf<String>()` → an **empty** read-only list. We must say `<String>` because Kotlin can't guess the type of an empty list (Chapter 3).

**Task 5:**
`clicks` is a **state box** (`MutableState<Int>`), not a number — there's no `by`. So `clicks++` doesn't work, and `"$clicks"` prints the box, not the number.

**Fix A** (use `.value`):

```kotlin
val clicks = remember { mutableStateOf(0) }
Button(onClick = { clicks.value++ }) {
    Text("Clicked ${clicks.value} times")
}
```

**Fix B** (use `by` — better):

```kotlin
var clicks by remember { mutableIntStateOf(0) }
Button(onClick = { clicks++ }) {
    Text("Clicked $clicks times")
}
```

**Task 6:**
Because `total` can be **calculated** from other state (`size`, `cups`, `sugar`, `cream`). If it were its own state, we would have to update it by hand every time one of those changes — and if we forgot once, the total would be **wrong**. 🐛 Calculating it during recomposition means it is **always correct**. ✅

---

## 8.15 What Is Next?

In **Chapter 9: Getting Input From the User**, you will use state to build forms:

- **`TextField`** and **`OutlinedTextField`** — let the user **type** ⌨️
- Keyboard types: numbers, email, password 🔒
- Showing **errors** under a text field
- **`Checkbox`**, **`RadioButton`**, **`Switch`**, **`Slider`**
- **Chips** for choices
- Building a full **Sign-Up form** with checks ✅

**Great job finishing Chapter 8! 🎉 You learned the heart of Jetpack Compose!**
