# Chapter 26: Animations — Making Apps Feel Alive ✨🎬

> **What you will learn in this chapter**
>
> 1. **Why** animations matter — and the rules for good ones 🎯
> 2. **`animate*AsState`** — the easiest animation: just change a value 🎨
> 3. **Animation specs** — `tween`, `spring`, `keyframes`, and **easing** 🏀
> 4. **`AnimatedVisibility`** — appearing and disappearing in style 👻
> 5. **`animateContentSize`** — smooth growing and shrinking 📏
> 6. **`Crossfade`** and **`AnimatedContent`** — smooth changes from one thing to another 🔀
> 7. **`updateTransition`** — animating many things together 🎭
> 8. **Infinite** animations — pulsing, breathing, loading dots 💓
> 9. **`Animatable`** — animations you control with coroutines (a "wrong!" shake 🫨)
> 10. **Gestures** — dragging, springing back, and double-tap ❤️ 👆
> 11. **Screen transitions** in Navigation 🧭
> 12. 🛠️ Polishing the **Quiz app** and the **Notes app** 💫
>
> **Time needed:** about 4–5 hours. This is a **fun** chapter! 🎉
>
> **What you need to know:** Chapters 1–25, especially 8 (state), 13 (Navigation), 17 (Quiz app), 18 (coroutines), and 24 (Notes app).

---

## 26.1 Why Animate? 🤔

Turn on a light switch 💡: the room is **instantly** bright. Fine. But when a **door** opens instantly — no swinging, just *pop*, open — it's **confusing**. Where did the door go? 🚪❓

Apps are the same. Without animation, things **jump**. With good animation, the user **understands** what happened.

| Animation helps to… | Example |
|---|---|
| **Explain** what changed 🧭 | A card **slides** away when deleted → "it went **there**" |
| **Guide the eye** 👀 | A new message **fades in** → you notice it |
| **Show** that something is working ⏳ | A **pulsing** dot while loading |
| **Give feedback** 👆 | A button **bounces** when tapped → "got it!" |
| **Delight** 😊 | A heart **pops** when you like a photo ❤️ |

### The rules of good animation 🏆

| Rule | Why |
|---|---|
| **Short** — usually **150–400 ms** | Longer feels **slow** and annoying 🐌 |
| **With a purpose** | Every animation should **explain** or **give feedback** — not just "look cool" |
| **Natural** — use easing or springs | Real things **speed up** and **slow down**; they don't move like robots 🤖 |
| **Respect the user's settings** | Some people get **dizzy** from motion and turn animations off (26.16) |

> 💡 Most Compose animations are **just one line**: "*When this value changes, change it smoothly instead of instantly.*" Let's see! 🎬

> 🛠️ Try each example in **MyFirstApp**: put the Composable in `setContent { MyFirstAppTheme { ... } }` and run.

---

## 26.2 `animate*AsState` — The Easiest Animation 🎨

You already know this pattern from Chapter 8:

```kotlin
var liked by remember { mutableStateOf(false) }
val color = if (liked) Color.Red else Color.Gray      // changes INSTANTLY 💥
```

Now with animation — just **wrap** the value:

```kotlin
val color by animateColorAsState(
    targetValue = if (liked) Color.Red else Color.Gray,   // changes SMOOTHLY ✨
    label = "heartColor"
)
```

**`animateColorAsState`** = "Here's the color I **want**. Please **travel** there smoothly from wherever you are now." 🚗

### A ❤️ Like button

```kotlin
@Composable
fun LikeButton() {
    var liked by remember { mutableStateOf(false) }

    val color by animateColorAsState(                                          // (1)
        targetValue = if (liked) Color(0xFFE53935) else Color.Gray,
        animationSpec = tween(durationMillis = 300),                           // (2)
        label = "heartColor"                                                   // (3)
    )
    val size by animateDpAsState(                                              // (4)
        targetValue = if (liked) 72.dp else 48.dp,
        animationSpec = spring(                                                // (5)
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessLow
        ),
        label = "heartSize"
    )

    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Icon(
            imageVector = Icons.Filled.Favorite,
            contentDescription = if (liked) "Unlike" else "Like",
            tint = color,                                                      // (6)
            modifier = Modifier
                .size(size)
                .clickable { liked = !liked }                                  // (7)
        )
    }
}
```

Imports:

```kotlin
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `val color by animateColorAsState(...)` | A **color** that moves smoothly towards `targetValue`. `by` → use it like a normal value (Chapter 8). |
| 2 | `animationSpec = tween(durationMillis = 300)` | **How** to animate: take **300 ms**. (More in 26.3.) |
| 3 | `label = "heartColor"` | A **name** for this animation. It shows up in Android Studio's **Animation Preview** tool (26.17). Not required — but a good habit. 🏷️ |
| 4 | `animateDpAsState(...)` | Same idea for a **size** in `dp`. |
| 5 | `spring(dampingRatio = ..., stiffness = ...)` | Move like a **spring** 🪀 — overshoot a bit, then settle. A **bouncy** feeling! |
| 6 | `tint = color` | Use the animated color. Every frame, it's a little **closer** to the target. |
| 7 | `liked = !liked` | We only change the **state**. The animations follow **by themselves**. 🪄 |

**Run it** and tap the heart: it turns **red** and **bounces** bigger. Tap again → grey and smaller. ❤️✨

### The whole family 👨‍👩‍👧‍👦

| Function | Animates a… | Example |
|---|---|---|
| `animateColorAsState` | `Color` 🎨 | Background color |
| `animateDpAsState` | `Dp` 📏 | Size, padding, corner radius |
| `animateFloatAsState` | `Float` 🔢 | Alpha (see-through), scale, rotation, progress |
| `animateIntAsState` | `Int` | A score counting up |
| `animateOffsetAsState` | `Offset` (x, y) | A position |

> 🎯 **Rule:** if a value changes because of **state**, and you want the change to look **smooth**, wrap it in `animate*AsState`. That covers **most** animations in real apps! 😎

### What happens if the target changes in the middle? 🔄

Tap the heart **very fast**, several times. The animation never "jumps" — it **turns around** smoothly from wherever it is. `animate*AsState` always continues from the **current** value. 🧠 That's why it feels so natural.

---

## 26.3 Animation Specs — *How* Things Move 🏀

The `animationSpec` decides the **style** of movement. Let's see three balls race! 🏁

```kotlin
@Composable
fun BallRace() {
    var moved by remember { mutableStateOf(false) }
    val target = if (moved) 220.dp else 0.dp

    val tweenX by animateDpAsState(target, tween(durationMillis = 1000), label = "tween")
    val linearX by animateDpAsState(target, tween(durationMillis = 1000, easing = LinearEasing), label = "linear")
    val springX by animateDpAsState(
        target,
        spring(dampingRatio = Spring.DampingRatioHighBouncy, stiffness = Spring.StiffnessVeryLow),
        label = "spring"
    )

    Column(
        modifier = Modifier.padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        Ball(label = "tween", offsetX = tweenX)
        Ball(label = "linear", offsetX = linearX)
        Ball(label = "spring", offsetX = springX)
        Button(onClick = { moved = !moved }) { Text("Go! 🏁") }
    }
}

@Composable
fun Ball(label: String, offsetX: Dp) {
    Column {
        Text(label, style = MaterialTheme.typography.labelMedium)
        Box(
            modifier = Modifier
                .offset(x = offsetX)                                // move to the right
                .size(40.dp)
                .background(MaterialTheme.colorScheme.primary, CircleShape)
        )
    }
}
```

**Run it** and tap **Go!** a few times. Watch closely 👀:

| Spec | What you see | Like… |
|---|---|---|
| `tween(1000)` | Starts **slowly**, speeds up, **slows down** at the end. Smooth. | A car 🚗 leaving and parking |
| `tween(1000, easing = LinearEasing)` | The **same speed** the whole way. Feels **robotic**. 🤖 | A conveyor belt |
| `spring(HighBouncy, VeryLow)` | **Shoots** past the end and **bounces** back and forth. | A ball on a rubber band 🪀 |

### `tween` — a fixed time ⏱️

```kotlin
tween(
    durationMillis = 300,                // how long
    delayMillis = 0,                     // wait before starting
    easing = FastOutSlowInEasing         // the "speed curve" (this is the default)
)
```

**Easing** = how the speed **changes** during the animation:

| Easing | Speed | Good for |
|---|---|---|
| `FastOutSlowInEasing` (default) | Quick start, gentle stop | Most movements ⭐ |
| `LinearEasing` | Always the same | Spinning loaders, progress |
| `FastOutLinearInEasing` | Slow start, fast end | Things **leaving** the screen 🚪➡️ |
| `LinearOutSlowInEasing` | Fast start, slow end | Things **entering** the screen ➡️🚪 |

### `spring` — physics, no fixed time 🪀

```kotlin
spring(
    dampingRatio = Spring.DampingRatioMediumBouncy,   // how BOUNCY
    stiffness = Spring.StiffnessMedium                // how FAST
)
```

| `dampingRatio` | Bounce |
|---|---|
| `Spring.DampingRatioNoBouncy` | None — just smooth (default) |
| `Spring.DampingRatioLowBouncy` | A little |
| `Spring.DampingRatioMediumBouncy` | Clear bounce ⭐ (fun buttons, hearts) |
| `Spring.DampingRatioHighBouncy` | Very bouncy 🤪 |

| `stiffness` | Speed |
|---|---|
| `Spring.StiffnessHigh` | Very fast, snappy |
| `Spring.StiffnessMedium` | Normal |
| `Spring.StiffnessLow` | Slow, soft ⭐ |
| `Spring.StiffnessVeryLow` | Very slow, floaty |

> 💡 **Springs** have no fixed duration — they move until they **settle**, like real objects. They're the **default** for many Compose animations, because they feel **natural** and handle interruptions beautifully. 🌿

### `keyframes` — a step-by-step plan 📋

```kotlin
animationSpec = keyframes {
    durationMillis = 1000
    0.dp at 0                   // at 0 ms:    0 dp
    250.dp at 300               // at 300 ms:  250 dp (fast!)
    200.dp at 600               // at 600 ms:  a little back
    220.dp at 1000              // at 1000 ms: the end
}
```

"At **this** time, be at **this** value." Compose fills in the moments between. Useful for special effects. ✨

---

## 26.4 `AnimatedVisibility` — Appear and Disappear in Style 👻

With a normal `if`, things **pop** in and out:

```kotlin
if (showDetails) {
    DetailsCard()          // 💥 pop!
}
```

With **`AnimatedVisibility`**, they **arrive** and **leave** smoothly:

```kotlin
@Composable
fun DetailsDemo() {
    var showDetails by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier.padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Button(onClick = { showDetails = !showDetails }) {
            Text(if (showDetails) "Hide details 🙈" else "Show details 👀")
        }

        AnimatedVisibility(                                                    // (1)
            visible = showDetails,                                             // (2)
            enter = fadeIn() + expandVertically(),                             // (3)
            exit = fadeOut() + shrinkVertically()                              // (4)
        ) {
            Card(modifier = Modifier.fillMaxWidth()) {
                Text(
                    "🦒 Giraffes have the same number of neck bones as people: seven!",
                    modifier = Modifier.padding(16.dp)
                )
            }
        }

        Text("This text moves down smoothly when the card appears. 👇")
    }
}
```

Imports: `androidx.compose.animation.AnimatedVisibility`, `androidx.compose.animation.fadeIn`, `fadeOut`, `expandVertically`, `shrinkVertically`.

| # | Code | Meaning |
|---|---|---|
| 1 | `AnimatedVisibility(...) { ... }` | "Show the content **with an animation**." |
| 2 | `visible = showDetails` | `true` → animate **in**. `false` → animate **out**, then remove it. |
| 3 | `enter = fadeIn() + expandVertically()` | How to **arrive**: fade in **and** grow taller — at the same time. `+` **combines** effects! |
| 4 | `exit = fadeOut() + shrinkVertically()` | How to **leave**. |

**Run it.** The card fades in **while** growing — and the text below **slides down** smoothly instead of jumping. ✨

### The enter and exit menu 🍽️

| Enter ➡️ | Exit ⬅️ | Effect |
|---|---|---|
| `fadeIn()` | `fadeOut()` | See-through ↔ visible 👻 |
| `slideInVertically()` | `slideOutVertically()` | Slide from/to top or bottom ↕️ |
| `slideInHorizontally()` | `slideOutHorizontally()` | Slide from/to the side ↔️ |
| `expandVertically()` | `shrinkVertically()` | Grow/shrink in height 📏 |
| `expandHorizontally()` | `shrinkHorizontally()` | Grow/shrink in width |
| `scaleIn()` | `scaleOut()` | Zoom in/out 🔍 |

**Slide direction** — you choose where it starts with a small lambda:

```kotlin
enter = slideInVertically { fullHeight -> fullHeight }       // from the BOTTOM (one full height below)
enter = slideInVertically { fullHeight -> -fullHeight }      // from the TOP
enter = slideInHorizontally { fullWidth -> fullWidth }       // from the RIGHT
```

> 💡 Without `enter`/`exit`, `AnimatedVisibility` uses a nice default (fade + expand/shrink). So `AnimatedVisibility(visible = x) { ... }` already looks good! 👍

---

## 26.5 `animateContentSize` — Smooth Growing 📏

Sometimes content **changes size** — like "Read more" on a long text. One modifier makes it smooth:

```kotlin
@Composable
fun ReadMoreCard() {
    var expanded by remember { mutableStateOf(false) }
    val story = "Once upon a time, a little robot 🤖 wanted to learn Kotlin. " +
        "Every day it read one chapter, typed every example, and asked many questions. " +
        "After a few months, it built its very own app — and everyone was amazed! 🎉"

    Card(
        onClick = { expanded = !expanded },
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            .animateContentSize()                                   // 👈 the magic line
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = story,
                maxLines = if (expanded) Int.MAX_VALUE else 2,       // 2 lines, or all
                overflow = TextOverflow.Ellipsis
            )
            Text(
                text = if (expanded) "Show less ⬆️" else "Read more ⬇️",
                color = MaterialTheme.colorScheme.primary,
                style = MaterialTheme.typography.labelLarge
            )
        }
    }
}
```

| Code | Meaning |
|---|---|
| `Modifier.animateContentSize()` | "Whenever my **size** changes, change it **smoothly**." Put it **before** `padding` inside the card… or anywhere on the thing that grows. |
| `maxLines = if (expanded) Int.MAX_VALUE else 2` | `Int.MAX_VALUE` = the biggest possible `Int` → "no limit". |

Tap the card: it **grows** smoothly to show the whole story, and **shrinks** back. 📖✨ (Import: `androidx.compose.animation.animateContentSize`.)

---

## 26.6 `Crossfade` and `AnimatedContent` — From One Thing to Another 🔀

`AnimatedVisibility` is for **one** thing appearing/disappearing. But what about **changing** from **A** to **B**?

### `Crossfade` — fade between two things 🌗

```kotlin
@Composable
fun DayNight() {
    var isDay by remember { mutableStateOf(true) }

    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Crossfade(targetState = isDay, label = "dayNight") { day ->              // (1)
            Text(if (day) "☀️" else "🌙", fontSize = 120.sp)                       // (2)
        }
        Button(onClick = { isDay = !isDay }) { Text("Switch 🔁") }
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `Crossfade(targetState = isDay) { day -> ... }` | When `isDay` changes, the **old** content fades **out** while the **new** fades **in**. |
| 2 | `day` (not `isDay`!) | ⚠️ Use the **lambda's** value. During the fade, **both** versions exist — the old one with `day = true`, the new one with `day = false`. If you used `isDay`, both would show the **new** emoji! |

### `AnimatedContent` — full control 🎛️

`AnimatedContent` is like `Crossfade`, but you choose **any** enter/exit. Let's make a counter where numbers **roll** like a slot machine 🎰 — **up** when increasing, **down** when decreasing:

```kotlin
@Composable
fun RollingCounter() {
    var count by remember { mutableIntStateOf(0) }

    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        AnimatedContent(
            targetState = count,
            transitionSpec = {                                                    // (1)
                if (targetState > initialState) {                                 // (2)
                    (slideInVertically { height -> height } + fadeIn()) togetherWith    // (3)
                        (slideOutVertically { height -> -height } + fadeOut())
                } else {
                    (slideInVertically { height -> -height } + fadeIn()) togetherWith
                        (slideOutVertically { height -> height } + fadeOut())
                }
            },
            label = "counter"
        ) { value ->                                                              // (4)
            Text("$value", style = MaterialTheme.typography.displayLarge)
        }

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedButton(onClick = { count-- }) { Text("−1") }
            Button(onClick = { count++ }) { Text("+1") }
        }
    }
}
```

Imports: `androidx.compose.animation.AnimatedContent`, `androidx.compose.animation.togetherWith`, `slideInVertically`, `slideOutVertically`, `fadeIn`, `fadeOut`.

| # | Code | Meaning |
|---|---|---|
| 1 | `transitionSpec = { ... }` | **How** to go from the old content to the new. |
| 2 | `targetState > initialState` | Inside `transitionSpec`, `initialState` = the **old** value, `targetState` = the **new** value. Going **up**? ⬆️ |
| 3 | `enter togetherWith exit` | "The new content enters **like this**, **together with** the old content leaving **like that**." New number comes from **below**, old one leaves to the **top**. 🎰 |
| 4 | `{ value -> ... }` | Again: use the **lambda's** value (like `Crossfade`). |

Tap **+1** → numbers roll **up**. Tap **−1** → they roll **down**. Satisfying! 😄

> 💡 **When to use which?**
> - Something appears/disappears → `AnimatedVisibility` 👻
> - A simple swap between states → `Crossfade` 🌗
> - A swap with **your own** movement → `AnimatedContent` 🎛️
> - Loading → Success → Error screens (Chapter 19!) → `AnimatedContent(targetState = loadState)` makes them flow nicely. ✨

---

## 26.7 `updateTransition` — Many Animations, One Conductor 🎭

Sometimes **several** things should change **together** when one state changes. For example, selecting a card changes its **border color**, **border width**, **elevation**, and shows a **check mark**. 🎻🎺🥁

You could write four `animate*AsState`… but **`updateTransition`** is like an orchestra **conductor** 🎼: one state, and every instrument follows **in sync**.

```kotlin
@Composable
fun SelectablePlanCard() {
    var selected by remember { mutableStateOf(false) }
    val transition = updateTransition(targetState = selected, label = "planCard")   // (1)

    val borderColor by transition.animateColor(label = "border") { isSelected ->   // (2)
        if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline
    }
    val borderWidth by transition.animateDp(label = "borderWidth") { isSelected ->
        if (isSelected) 4.dp else 1.dp
    }
    val elevation by transition.animateDp(label = "elevation") { isSelected ->
        if (isSelected) 8.dp else 0.dp
    }
    val checkScale by transition.animateFloat(                                      // (3)
        transitionSpec = { spring(dampingRatio = Spring.DampingRatioMediumBouncy) },
        label = "check"
    ) { isSelected ->
        if (isSelected) 1f else 0f
    }

    OutlinedCard(
        onClick = { selected = !selected },
        border = BorderStroke(borderWidth, borderColor),
        elevation = CardDefaults.outlinedCardElevation(defaultElevation = elevation),
        modifier = Modifier
            .fillMaxWidth()
            .padding(24.dp)
    ) {
        Row(
            modifier = Modifier.padding(20.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text("⭐ Super Plan", style = MaterialTheme.typography.titleLarge)
                Text("All features, forever!")
            }
            Text(
                "✅",
                fontSize = 32.sp,
                modifier = Modifier.graphicsLayer {                                 // (4)
                    scaleX = checkScale
                    scaleY = checkScale
                }
            )
        }
    }
}
```

Imports: `androidx.compose.animation.animateColor`, `androidx.compose.animation.core.animateDp`, `androidx.compose.animation.core.animateFloat`, `androidx.compose.animation.core.updateTransition`, `androidx.compose.ui.graphics.graphicsLayer`, `androidx.compose.foundation.BorderStroke`.

| # | Code | Meaning |
|---|---|---|
| 1 | `updateTransition(targetState = selected)` | The **conductor** 🎼, following `selected`. |
| 2 | `transition.animateColor { isSelected -> ... }` | "For each state, here's my color." All values follow the **same** transition, so they start and finish **together**. |
| 3 | `animateFloat(transitionSpec = { spring(...) })` | Each value can have its **own** spec — the ✅ bounces in! |
| 4 | `Modifier.graphicsLayer { scaleX = ...; scaleY = ... }` | **Scale** (zoom) the check mark. `0f` = invisible (zero size), `1f` = normal. See the box below. 👇 |

> ⚡ **`graphicsLayer { }` — the fast way to animate looks.** Changing `scaleX`, `scaleY`, `rotationZ`, `alpha`, `translationX`/`translationY` inside `graphicsLayer { }` **doesn't** make Compose measure the layout again — it just **redraws** the pixels. Perfect for smooth animations at 60+ frames per second! 🏎️ (`Modifier.scale(x)`, `Modifier.alpha(x)`, and `Modifier.rotate(x)` are short versions of the same idea.)

---

## 26.8 Infinite Animations — Forever and Ever 🔁💓

Some animations should **never stop**: a pulsing "recording" dot 🔴, a breathing heart, loading dots… For these, use **`rememberInfiniteTransition`**.

### A beating heart 💓

```kotlin
@Composable
fun BeatingHeart() {
    val infinite = rememberInfiniteTransition(label = "heartbeat")             // (1)
    val scale by infinite.animateFloat(                                       // (2)
        initialValue = 1f,
        targetValue = 1.25f,
        animationSpec = infiniteRepeatable(                                   // (3)
            animation = tween(durationMillis = 500),
            repeatMode = RepeatMode.Reverse                                   // (4)
        ),
        label = "scale"
    )

    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Text(
            "❤️",
            fontSize = 96.sp,
            modifier = Modifier.graphicsLayer {
                scaleX = scale
                scaleY = scale
            }
        )
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `rememberInfiniteTransition()` | An animation clock that runs **forever** (while the Composable is on screen). ⏰ |
| 2 | `infinite.animateFloat(initialValue, targetValue, ...)` | A value that moves between `1f` and `1.25f`… |
| 3 | `infiniteRepeatable(animation = tween(500))` | …taking 500 ms each time, **repeating forever**. |
| 4 | `RepeatMode.Reverse` | Go **there and back**: 1 → 1.25 → 1 → 1.25… 💓 (`RepeatMode.Restart` = jump back to the start each time — good for spinning 🔄.) |

### Loading dots ● ● ●

```kotlin
@Composable
fun LoadingDots() {
    val infinite = rememberInfiniteTransition(label = "dots")

    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        repeat(3) { index ->
            val offsetY by infinite.animateFloat(
                initialValue = 0f,
                targetValue = -20f,
                animationSpec = infiniteRepeatable(
                    animation = tween(durationMillis = 400),
                    repeatMode = RepeatMode.Reverse,
                    initialStartOffset = StartOffset(offsetMillis = index * 130)   // 👈 each dot starts a bit later
                ),
                label = "dot$index"
            )
            Box(
                modifier = Modifier
                    .graphicsLayer { translationY = offsetY }                      // move up/down
                    .size(16.dp)
                    .background(MaterialTheme.colorScheme.primary, CircleShape)
            )
        }
    }
}
```

`StartOffset(index * 130)` → dot 0 starts now, dot 1 after 130 ms, dot 2 after 260 ms → a **wave** 🌊: ● ● ● hopping one after another. `translationY` moves it **up** (negative = up).

> 🔋 Infinite animations **only run while visible**. When the Composable leaves the screen, they stop automatically. Still — use them **sparingly**: endless motion can be distracting.

---

## 26.9 `Animatable` — Animations You Control 🎮

`animate*AsState` follows a **state**. But sometimes you want to **command** an animation directly: "**Shake now!**" — not because a state changed, but because something **happened** (a wrong password ❌).

**`Animatable`** is a value you animate **step by step**, from a **coroutine** (Chapter 18):

### A "wrong PIN" shake 🫨

```kotlin
@Composable
fun PinInput() {
    var pin by remember { mutableStateOf("") }
    var message by remember { mutableStateOf("Enter the secret PIN (hint: 1234) 🔐") }
    val shakeOffset = remember { Animatable(0f) }                                 // (1)
    val scope = rememberCoroutineScope()

    fun shake() {
        scope.launch {                                                            // (2)
            for (x in listOf(-30f, 30f, -20f, 20f, -10f, 10f, 0f)) {              // (3)
                shakeOffset.animateTo(x, animationSpec = tween(durationMillis = 40))   // (4)
            }
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(message, textAlign = TextAlign.Center)
        OutlinedTextField(
            value = pin,
            onValueChange = { pin = it.take(4) },
            label = { Text("PIN") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.NumberPassword),
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier.graphicsLayer { translationX = shakeOffset.value }   // (5)
        )
        Button(onClick = {
            if (pin == "1234") {
                message = "Welcome! 🎉"
            } else {
                message = "Wrong PIN ❌ Try again."
                pin = ""
                shake()
            }
        }) {
            Text("Unlock 🔓")
        }
    }
}
```

Import: `androidx.compose.animation.core.Animatable`.

| # | Code | Meaning |
|---|---|---|
| 1 | `remember { Animatable(0f) }` | A number that can be animated, starting at `0f` (no shake). |
| 2 | `scope.launch { ... }` | `animateTo` is a **suspend** function (it waits until the animation ends) → it needs a coroutine. |
| 3 | `for (x in listOf(-30f, 30f, ...))` | Left, right, left, right… each time a bit **less**, then back to **0** — like a head shaking "no!" 🙅 |
| 4 | `animateTo(x, tween(40))` | Animate to `x` in 40 ms, and **wait** until done. Then the loop continues to the next `x`. Step by step! 👣 |
| 5 | `translationX = shakeOffset.value` | Move the text field left/right by that many **pixels**. |

Type `0000` and tap **Unlock** → the field **shakes** "no!" 🫨 Type `1234` → welcome! 🎉

| `Animatable` function | Meaning |
|---|---|
| `animateTo(target, spec)` | Animate to a value and **wait** until finished. |
| `snapTo(value)` | **Jump** to a value instantly (no animation). |
| `stop()` | Stop where it is. |
| `.value` | The current value. |

> 💡 **`animate*AsState` vs `Animatable`:**
> - "When the **state** is X, look like Y" → `animate*AsState` 🎨
> - "**Do** this animation **now**, in these steps" → `Animatable` 🎮

---

## 26.10 Gestures — Touch and Move 👆

### Drag a sticker, and watch it spring back 🐱🪀

```kotlin
@Composable
fun DraggableSticker() {
    val offset = remember { Animatable(Offset.Zero, Offset.VectorConverter) }    // (1)
    val scope = rememberCoroutineScope()

    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Text(
            text = "🐱",
            fontSize = 96.sp,
            modifier = Modifier
                .offset { IntOffset(offset.value.x.roundToInt(), offset.value.y.roundToInt()) }   // (2)
                .pointerInput(Unit) {                                            // (3)
                    detectDragGestures(                                          // (4)
                        onDragEnd = {
                            scope.launch {
                                offset.animateTo(                                // (5)
                                    targetValue = Offset.Zero,
                                    animationSpec = spring(
                                        dampingRatio = Spring.DampingRatioMediumBouncy,
                                        stiffness = Spring.StiffnessLow
                                    )
                                )
                            }
                        }
                    ) { change, dragAmount ->                                    // (6)
                        change.consume()
                        scope.launch { offset.snapTo(offset.value + dragAmount) }   // (7)
                    }
                }
        )
    }
}
```

Imports:

```kotlin
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.VectorConverter
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.unit.IntOffset
import kotlin.math.roundToInt
```

**Line by line:**

| # | Code | Meaning |
|---|---|---|
| 1 | `Animatable(Offset.Zero, Offset.VectorConverter)` | An animatable **position** (x and y together). `VectorConverter` tells Compose how to animate an `Offset` (two numbers). Starts at `(0, 0)`. |
| 2 | `.offset { IntOffset(...) }` | Move the cat by the current offset (in pixels, rounded to whole numbers). The `{ }` version is **fast** — no re-layout needed. |
| 3 | `.pointerInput(Unit) { ... }` | "I want to handle **touches** myself." 👆 |
| 4 | `detectDragGestures(...)` | Compose recognizes **dragging** for us. |
| 5 | `onDragEnd = { offset.animateTo(Offset.Zero, spring(...)) }` | When the finger **lets go**: spring back to the center, with a bounce! 🪀 |
| 6 | `{ change, dragAmount -> ... }` | Called **many** times while dragging. `dragAmount` = how far the finger moved **since last time**. |
| 7 | `offset.snapTo(offset.value + dragAmount)` | Follow the finger **exactly** (no animation while dragging). `change.consume()` = "I handled this touch — nobody else should." |

Drag the cat around… let go… **boing!** 🐱🪀 It flies back to the middle.

### Double-tap to like ❤️ (like Instagram!)

```kotlin
@Composable
fun DoubleTapLike() {
    var liked by remember { mutableStateOf(false) }
    var showBigHeart by remember { mutableStateOf(false) }

    val heartScale by animateFloatAsState(
        targetValue = if (showBigHeart) 1f else 0f,
        animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy),
        label = "bigHeart"
    )

    LaunchedEffect(showBigHeart) {                                            // (1)
        if (showBigHeart) {
            delay(700)
            showBigHeart = false
        }
    }

    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(12.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Box(
            modifier = Modifier
                .size(260.dp)
                .clip(RoundedCornerShape(24.dp))
                .background(MaterialTheme.colorScheme.secondaryContainer)
                .pointerInput(Unit) {
                    detectTapGestures(                                        // (2)
                        onDoubleTap = {
                            liked = true
                            showBigHeart = true
                        }
                    )
                },
            contentAlignment = Alignment.Center
        ) {
            Text("🐶", fontSize = 140.sp)
            Text(
                "❤️",
                fontSize = 110.sp,
                modifier = Modifier.graphicsLayer {
                    scaleX = heartScale
                    scaleY = heartScale
                    alpha = heartScale.coerceIn(0f, 1f)                       // (3)
                }
            )
        }
        Text(if (liked) "❤️ You liked this" else "Double-tap the photo 👆👆")
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `LaunchedEffect(showBigHeart)` | After the big heart appears, wait 0.7 s, then hide it again (Chapter 18). |
| 2 | `detectTapGestures(onDoubleTap = { ... })` | Recognize a **double tap**. (Also available: `onTap`, `onLongPress`, `onPress`.) |
| 3 | `alpha = heartScale.coerceIn(0f, 1f)` | The spring **overshoots** past `1f` (bouncy!), but `alpha` must stay between 0 and 1. `coerceIn` keeps it inside. |

Double-tap the dog → a big ❤️ **pops**, bounces, and **shrinks** away. 🐶❤️✨

| Gesture tool | Recognizes |
|---|---|
| `Modifier.clickable { }` | A simple tap (with ripple) |
| `detectTapGestures(onTap, onDoubleTap, onLongPress)` | Taps, double taps, long presses |
| `detectDragGestures` | Dragging in any direction |
| `detectHorizontalDragGestures` / `detectVerticalDragGestures` | Dragging in **one** direction |
| `detectTransformGestures` | Two-finger **pinch** (zoom) and **rotate** 🤏 |

---

## 26.11 Screen Transitions in Navigation 🧭✨

By default, Navigation (Chapter 13) **fades** between screens. You can choose your own — for **all** screens at once — right in the `NavHost`:

```kotlin
NavHost(
    navController = navController,
    startDestination = NotesList,
    enterTransition = {                                                        // (1)
        slideIntoContainer(AnimatedContentTransitionScope.SlideDirection.Start, tween(300))
    },
    exitTransition = {                                                         // (2)
        slideOutOfContainer(AnimatedContentTransitionScope.SlideDirection.Start, tween(300))
    },
    popEnterTransition = {                                                     // (3)
        slideIntoContainer(AnimatedContentTransitionScope.SlideDirection.End, tween(300))
    },
    popExitTransition = {                                                      // (4)
        slideOutOfContainer(AnimatedContentTransitionScope.SlideDirection.End, tween(300))
    }
) {
    // ... composable<...> { } as before ...
}
```

| # | Transition | When | Here |
|---|---|---|---|
| 1 | `enterTransition` | The **new** screen arrives (`navigate`) | Slides in from the **right** ➡️ |
| 2 | `exitTransition` | The **old** screen leaves (`navigate`) | Slides out to the **left** ⬅️ |
| 3 | `popEnterTransition` | The **previous** screen comes back (**Back**) | Slides in from the **left** |
| 4 | `popExitTransition` | The current screen leaves (**Back**) | Slides out to the **right** |

`SlideDirection.Start` / `End` follow the **reading direction** — in right-to-left languages (Arabic, Hebrew), they automatically **flip**. 🌍 Imports: `androidx.compose.animation.AnimatedContentTransitionScope`, `androidx.compose.animation.core.tween`.

> 💡 You can also give **one** screen its own transition: `composable<NoteEditor>(enterTransition = { ... }) { ... }`.

---

# 🛠️ Polishing Our Apps 💫

Now the best part: using what we learned to make **real apps** feel great!

## 26.12 Polishing the Quiz App 🧠✨

Open your **Quiz** project (Chapter 17). Five small upgrades:

| # | Upgrade | Tool |
|---|---|---|
| 1 | The progress bar **slides** forward | `animateFloatAsState` |
| 2 | Answer colors **fade** to green/red | `animateColorAsState` |
| 3 | A wrong answer **shakes** 🫨, a right one **pops** 🎉 | `Animatable` |
| 4 | The explanation **slides in** | `AnimatedVisibility` |
| 5 | The result stars appear **one by one** ⭐, and the trophy **pulses** 🏆 | `AnimatedVisibility` + infinite |

### 1. A smooth progress bar — in `QuizScreen`

```kotlin
val animatedProgress by animateFloatAsState(
    targetValue = uiState.progress,
    animationSpec = tween(durationMillis = 500),
    label = "progress"
)

LinearProgressIndicator(
    progress = { animatedProgress },                         // 👈 was uiState.progress
    modifier = Modifier.fillMaxWidth()
)
```

(Put the `val` right after `val question = ...`, inside the Scaffold content.)

### 2 + 3. Animated `OptionCard` — fades, shakes, and pops

Replace the `OptionCard` function:

```kotlin
@Composable
private fun OptionCard(
    text: String,
    state: OptionState,
    enabled: Boolean,
    onClick: () -> Unit
) {
    val (container, border, content) = when (state) {
        OptionState.NORMAL -> Triple(
            MaterialTheme.colorScheme.surface,
            MaterialTheme.colorScheme.outline,
            MaterialTheme.colorScheme.onSurface
        )
        OptionState.CORRECT -> Triple(CorrectColor, CorrectBorder, Color.Black)
        OptionState.WRONG -> Triple(WrongColor, WrongBorder, Color.Black)
        OptionState.FADED -> Triple(
            MaterialTheme.colorScheme.surface,
            MaterialTheme.colorScheme.outlineVariant,
            MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
        )
    }
    val mark = when (state) {
        OptionState.CORRECT -> "✅"
        OptionState.WRONG -> "❌"
        else -> ""
    }

    // ✨ NEW: smooth colors
    val containerColor by animateColorAsState(container, tween(300), label = "container")   // (1)
    val borderColor by animateColorAsState(border, tween(300), label = "border")
    val contentColor by animateColorAsState(content, tween(300), label = "content")

    // ✨ NEW: shake and pop
    val shakeX = remember { Animatable(0f) }                                                  // (2)
    val popScale = remember { Animatable(1f) }

    LaunchedEffect(state) {                                                                   // (3)
        when (state) {
            OptionState.WRONG -> {
                for (x in listOf(-24f, 24f, -16f, 16f, -8f, 8f, 0f)) {
                    shakeX.animateTo(x, tween(40))
                }
            }
            OptionState.CORRECT -> {
                popScale.animateTo(1.06f, tween(120))                                         // (4)
                popScale.animateTo(1f, spring(dampingRatio = Spring.DampingRatioMediumBouncy))
            }
            else -> Unit
        }
    }

    OutlinedCard(
        onClick = onClick,
        enabled = enabled,
        colors = CardDefaults.outlinedCardColors(
            containerColor = containerColor,
            contentColor = contentColor,
            disabledContainerColor = containerColor,
            disabledContentColor = contentColor
        ),
        border = BorderStroke(2.dp, borderColor),
        modifier = Modifier
            .fillMaxWidth()
            .graphicsLayer {                                                                  // (5)
                translationX = shakeX.value
                scaleX = popScale.value
                scaleY = popScale.value
            }
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(text, style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
            Text(mark)
        }
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `animateColorAsState(container, ...)` | Instead of **jumping** to green/red, the colors **fade** there in 300 ms. |
| 2 | Two `Animatable`s | One for the **shake** (left/right), one for the **pop** (size). |
| 3 | `LaunchedEffect(state)` | Runs every time **this option's** state changes. `WRONG` → shake. `CORRECT` → pop. |
| 4 | `animateTo(1.06f)` then `animateTo(1f, spring)` | Grow quickly to 106%, then **bounce** back to normal. 🎉 |
| 5 | `graphicsLayer { ... }` | Apply both — fast, no re-layout. ⚡ |

**What the user sees:** tap a wrong answer → it turns **red** and **shakes** 🫨, while the right answer turns **green** and **pops** 🎉. Tap the right answer → it turns green and pops. Much more fun! 😄

> 💡 After a rotation 🔄, the `LaunchedEffect` starts again with the **same** state — so the shake/pop **replays** once. That's harmless (even cute). To avoid it, you could remember "already played" with `rememberSaveable`.

### 4. The explanation slides in

Replace the `if (uiState.isAnswered) { ... }` block:

```kotlin
AnimatedVisibility(
    visible = uiState.isAnswered,
    enter = fadeIn(tween(300)) + expandVertically(),
    exit = ExitTransition.None                                                 // 👈 see below
) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        FeedbackCard(
            correct = uiState.answeredCorrectly,
            correctAnswer = question.correctAnswer,
            explanation = question.explanation
        )
        Button(onClick = onNextClick, modifier = Modifier.fillMaxWidth()) {
            Text(if (uiState.isLastQuestion) "See results 🏁" else "Next ➡️")
        }
    }
}
```

🤔 **Why `exit = ExitTransition.None`?** When you tap **Next**, `isAnswered` becomes `false` **and** the question changes **at the same moment**. A fade-out would show the **next** question's explanation for a split second while fading. 😬 So: **animate in, disappear instantly.** (Import `androidx.compose.animation.ExitTransition`.)

### 5. Stars one by one, and a pulsing trophy — in `ResultScreen.kt`

Add this Composable:

```kotlin
@Composable
private fun AnimatedStars(score: Int, total: Int) {
    var shownStars by rememberSaveable { mutableIntStateOf(0) }                // (1)

    LaunchedEffect(Unit) {
        while (shownStars < total) {                                           // (2)
            delay(250)
            shownStars++
        }
    }

    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
        repeat(total) { index ->
            AnimatedVisibility(
                visible = index < shownStars,                                  // (3)
                enter = scaleIn(spring(dampingRatio = Spring.DampingRatioMediumBouncy)) + fadeIn()
            ) {
                Text(if (index < score) "⭐" else "☆", fontSize = 36.sp)
            }
        }
    }
}
```

| # | Code | Meaning |
|---|---|---|
| 1 | `rememberSaveable { mutableIntStateOf(0) }` | How many stars are visible so far. **Saveable** → after rotation they don't start again from zero. |
| 2 | `while (shownStars < total) { delay(250); shownStars++ }` | Every 250 ms, show one more star. ⏱️⭐ |
| 3 | `visible = index < shownStars` | Star number `index` appears when its turn comes — **bouncing** in with `scaleIn` + a spring! |

In `ResultScreen`, replace the old `Text(stars, ...)` line with `AnimatedStars(score = score, total = total)` (and delete the `val stars = ...` line).

And make the big emoji **pulse** — replace `Text(message.emoji, fontSize = 96.sp)`:

```kotlin
val pulse = rememberInfiniteTransition(label = "trophy")
val emojiScale by pulse.animateFloat(
    initialValue = 1f,
    targetValue = 1.12f,
    animationSpec = infiniteRepeatable(tween(700), RepeatMode.Reverse),
    label = "emojiScale"
)
Text(
    message.emoji,
    fontSize = 96.sp,
    modifier = Modifier.graphicsLayer {
        scaleX = emojiScale
        scaleY = emojiScale
    }
)
```

**Run the Quiz!** ▶️ Shaking wrong answers 🫨, popping right ones 🎉, a gliding progress bar, sliding explanations, and stars that **pop in one by one** ⭐⭐⭐⭐☆ under a breathing trophy 🏆. It feels like a **real game** now! 🎮

---

## 26.13 Polishing the Notes App 📝✨

Open your **Notes** project (Chapters 24–25). Five upgrades:

### 1. Sliding screens — `NotesNavHost.kt`

Add the four transitions from **26.11** to the `NavHost`. Opening a note slides it in from the right; Back slides it out. ➡️⬅️

### 2. The editor's background color glides — `NoteEditorScreen.kt`

```kotlin
val backgroundColor by animateColorAsState(
    targetValue = uiState.color.toComposeColor(),
    animationSpec = tween(400),
    label = "noteBackground"
)

Scaffold(
    containerColor = backgroundColor,                 // 👈 was uiState.color.toComposeColor()
    // ...
)
```

Tap 🟡 then 🔵 → the whole page **flows** from yellow to blue. 🎨🌊

### 3. Bouncy color circles — `ColorPicker`

Inside the `forEach`, before the `Box`:

```kotlin
val borderWidth by animateDpAsState(
    targetValue = if (isSelected) 3.dp else 1.dp,
    label = "colorBorder"
)
val circleScale by animateFloatAsState(
    targetValue = if (isSelected) 1.15f else 1f,
    animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy),
    label = "colorScale"
)
```

…and in the `Box`'s modifier, add `.graphicsLayer { scaleX = circleScale; scaleY = circleScale }` **first** (before `.size`), and use `width = borderWidth` in the `.border(...)`.

The chosen circle now **grows** with a little bounce. 🔵✨

### 4. A gently fading pin 📌 — `NoteCard.kt` and the editor

```kotlin
val pinAlpha by animateFloatAsState(
    targetValue = if (note.isPinned) 1f else 0.25f,
    label = "pinAlpha"
)
Text("📌", modifier = Modifier.alpha(pinAlpha))           // 👈 was the if/else directly
```

(Same in the editor's top bar, with `uiState.isPinned`.) And the card **sliding** to the top when pinned? That's already done by `animateItem()` from Chapter 24! 🎉

### 5. A smart **+** button that shrinks while scrolling — `NotesListScreen.kt`

When the user scrolls down to read, a big "**+ New note**" button would cover the cards. Let's make it **expanded** at the top and **small** while scrolling:

```kotlin
val listState = rememberLazyListState()                                       // (1)
val isAtTop by remember {
    derivedStateOf { listState.firstVisibleItemIndex == 0 }                   // (2)
}

Scaffold(
    // ...
    floatingActionButton = {
        ExtendedFloatingActionButton(                                         // (3)
            onClick = onAddClick,
            expanded = isAtTop,
            icon = { Icon(Icons.Filled.Add, contentDescription = null) },
            text = { Text("New note") }
        )
    }
) { /* ... */ }

// ...and give the LazyColumn the state:
LazyColumn(
    state = listState,                                                        // 👈 new
    // ... the rest unchanged ...
)
```

| # | Code | Meaning |
|---|---|---|
| 1 | `rememberLazyListState()` | Lets us **read** the list's scroll position (Chapter 10). |
| 2 | `derivedStateOf { firstVisibleItemIndex == 0 }` | "Are we at the top?" — only recomposes when the **answer** changes, not on every scroll pixel (Chapter 10). ⚡ |
| 3 | `ExtendedFloatingActionButton(expanded = isAtTop, ...)` | A FAB with **text**. `expanded = false` → it **animates** into a small round **+** by itself! Material 3 does the animation for us. 🪄 |

**Run the Notes app!** ▶️ Screens slide, colors flow, circles bounce, pins fade, and the **+** button politely shrinks while you scroll. ✨📝

---

## 26.14 Seeing Animations in Slow Motion 🐢

Animations are **fast** — hard to check by eye. Two tools help:

### 1. Slow down the whole phone 🐌

On the emulator or phone, turn on **Developer options** (Chapter 1) → find **"Animator duration scale"** → choose **5x** or **10x**. Now **every** animation (including yours) is 5–10 times slower. Perfect for checking the details! 🔍 (Set it back to **1x** afterwards.)

### 2. Android Studio's Animation Preview 🎞️

In a `@Preview` with animations, look for the **"Start Animation Preview"** button (an icon with a play triangle) above the preview. It shows a **timeline** of each animation — that's where your **`label`**s appear! 🏷️ You can **scrub** back and forth, frame by frame. (It works with `updateTransition`, `AnimatedVisibility`, `animate*AsState`, `AnimatedContent`, `Crossfade`, and infinite transitions.)

---

## 26.15 Making Animations Fast ⚡

| Tip | Why |
|---|---|
| Animate **looks** (`alpha`, `scale`, `rotation`, `translation`) inside **`graphicsLayer { }`** | Only **redraws** — no measuring, no layout. Smoothest! 🏎️ |
| Use the **lambda** versions: `Modifier.offset { }`, `graphicsLayer { }` | The value is read **while drawing**, so Compose skips recomposition. |
| Animate **size** (with `animateContentSize`, `animateDpAsState` on `size`) only when needed | Size changes make Compose **measure and lay out** again — more work. |
| Use `derivedStateOf` for scroll-based effects | Avoids recomposing on every pixel of scrolling (26.13, #5). |
| Don't run **infinite** animations everywhere | They use the CPU/GPU all the time 🔋. |

---

## 26.16 Respecting the User: "Remove Animations" ♿

Some people feel **dizzy** or **sick** from motion on screens. Android has a setting for them: **Settings → Accessibility → Remove animations** (the name varies a little between phones).

Good news: Compose animations follow the phone's **animation speed** setting **automatically**. When animations are removed, most of them simply **jump** to the end. ✅

**Your part:**
- **Never** hide important information **only** in an animation. If a shake says "wrong!", also show a **text** message ("Wrong PIN ❌") — like we did! 📝
- Don't use fast **flashing** effects (they can be dangerous for some people).

---

## 26.17 Test Checklist ✅

| Test | Expected | ✓ |
|---|---|---|
| Like button ❤️ | Color fades, size bounces | ☐ |
| Ball race 🏁 | Three different movements; tap during the race → they turn around smoothly | ☐ |
| Details card 👀 | Fades + expands; text below slides down | ☐ |
| Read more 📖 | Card grows/shrinks smoothly | ☐ |
| Day/Night 🌗 | Crossfade between ☀️ and 🌙 | ☐ |
| Rolling counter 🎰 | Up rolls up, down rolls down | ☐ |
| Plan card ⭐ | Border, width, shadow, and ✅ animate together | ☐ |
| Heart 💓 and dots ●●● | Run forever, smoothly | ☐ |
| PIN 🔐 | Wrong → shake + message; right → welcome | ☐ |
| Sticker 🐱 | Follows the finger, springs back | ☐ |
| Double-tap 🐶 | Big heart pops and fades | ☐ |
| Quiz 🧠 | Progress slides, colors fade, wrong shakes, right pops, explanation slides in, stars pop one by one, trophy pulses | ☐ |
| Notes 📝 | Screens slide, background glides, circles bounce, pins fade, FAB shrinks on scroll | ☐ |
| Animator duration scale 10x | Everything in slow motion 🐢 — check that nothing looks broken | ☐ |
| Remove animations ON | Apps still work and make sense | ☐ |

---

## 26.18 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| Using the **outside** state inside `Crossfade`/`AnimatedContent` | Both old and new show the **new** data | Use the **lambda parameter** (`{ value -> ... }`). |
| `AnimatedVisibility` with content that changes while exiting | Wrong data flashes during the exit | Keep the data stable, or use `ExitTransition.None`. |
| `animateTo` without a coroutine | *Suspend function … should be called only from a coroutine* | `scope.launch { }` or `LaunchedEffect`. |
| `remember { Animatable(...) }` forgotten (just `Animatable(...)`) | A **new** Animatable every recomposition → no animation | Always `remember { }`. |
| Animating `size`/`padding` for a simple "pulse" | Janky, heavy | Use `graphicsLayer { scaleX/scaleY }`. |
| Very long animations (1–2 s) for normal actions | App feels **slow** 🐌 | Keep them **150–400 ms**. |
| `alpha` outside 0..1 (from a bouncy spring) | Crash or odd look | `coerceIn(0f, 1f)`. |
| Forgetting `change.consume()` in drag | Other things (like a scrolling list) also react | Consume the change. |
| Infinite animation in every list item | Battery drain 🔋 | Use sparingly. |
| Information **only** in an animation | Lost when animations are off ♿ | Also show text. |
| `with` instead of `togetherWith` (old tutorials) | Deprecated | `enter togetherWith exit` |

---

## 26.19 Summary — What You Learned 🎓

✅ Good animations **explain**, **guide**, and **give feedback**. Keep them **short** (150–400 ms), **natural**, and **purposeful**.

✅ **`animate*AsState`** (`Color`, `Dp`, `Float`, `Int`, `Offset`) — change the **target**, and the value travels there smoothly. Interruptions are handled for you. 🎨

✅ **Specs:** `tween(duration, easing)` ⏱️, `spring(dampingRatio, stiffness)` 🪀, `keyframes { }` 📋. Default easing: `FastOutSlowInEasing`.

✅ **`AnimatedVisibility(visible, enter, exit)`** with `fadeIn`, `slideIn…`, `expand…`, `scaleIn` — combined with `+`. 👻

✅ **`Modifier.animateContentSize()`** for smooth size changes. 📏

✅ **`Crossfade`** and **`AnimatedContent`** (with `transitionSpec`, `initialState`/`targetState`, `togetherWith`) — always use the **lambda's** value. 🔀

✅ **`updateTransition`** = one conductor for many animated values. 🎭

✅ **`rememberInfiniteTransition`** + `infiniteRepeatable` (`RepeatMode.Reverse`, `StartOffset`) for pulsing and loading. 💓

✅ **`Animatable`** + coroutines (`animateTo`, `snapTo`) for animations you **command** — like a shake. 🫨

✅ **Gestures:** `pointerInput` + `detectDragGestures`, `detectTapGestures(onDoubleTap)`; spring back with `Animatable`. 👆

✅ **Navigation transitions:** `enterTransition`, `exitTransition`, `popEnterTransition`, `popExitTransition` with `slideIntoContainer`/`slideOutOfContainer`. 🧭

✅ **Performance:** animate looks inside **`graphicsLayer { }`**. **Accessibility:** never rely **only** on animation. ♿

✅ You polished the **Quiz** 🧠 and **Notes** 📝 apps until they **sparkle**! ✨

---

## 26.20 Practice Time 🏋️

**Task 1 — A light switch 💡:**
A big round button. Tapping it toggles "on/off". When **on**: the background fades to **yellow**, the button **grows** a little with a bounce, and the emoji changes from 🌑 to 💡 with a **Crossfade**.

**Task 2 — Expandable FAQ ❓:**
Make a list of 3 questions. Tapping a question shows its answer below with `AnimatedVisibility` (fade + expand), and an arrow ▶️ next to the question **rotates** 90° to point down.
*Hint:* `animateFloatAsState(if (open) 90f else 0f)` + `Modifier.rotate(angle)`.

**Task 3 — Score counter 🔢:**
When a score changes from 0 to 120, make the number **count up** (0, 1, 2, … 120) instead of jumping.
*Hint:* `animateIntAsState(targetValue = score, animationSpec = tween(1000))`.

**Task 4 — Loading → Success → Error 🎭:**
Take the Joke Machine's (Chapter 19) `when (loadState)` and wrap it in `AnimatedContent(targetState = uiState.loadState)` so the three faces **fade** into each other.
*Hint:* inside, use the **lambda's** state! And because `Success` changes every time the list changes, think: should the key be the whole state, or just its **type**?

**Task 5 — Find the 3 bugs 🐛🐛🐛:**

```kotlin
@Composable
fun Shaker(isWrong: Boolean) {
    val offset = Animatable(0f)
    if (isWrong) {
        offset.animateTo(20f)
        offset.animateTo(0f)
    }
    Crossfade(targetState = isWrong, label = "x") {
        Text(if (isWrong) "❌" else "✅", modifier = Modifier.offset(x = offset.value.dp))
    }
}
```

**Task 6 — Spinning sun ☀️:**
Make a ☀️ that **rotates** slowly and forever (one full turn every 4 seconds, always the same speed).
*Hint:* `infiniteRepeatable(tween(4000, easing = LinearEasing), RepeatMode.Restart)` from `0f` to `360f`, and `graphicsLayer { rotationZ = angle }`.

---

### Answers

**Task 1:**

```kotlin
@Composable
fun LightSwitch() {
    var isOn by remember { mutableStateOf(false) }

    val background by animateColorAsState(
        targetValue = if (isOn) Color(0xFFFFF59D) else Color(0xFF263238),
        animationSpec = tween(400),
        label = "background"
    )
    val buttonScale by animateFloatAsState(
        targetValue = if (isOn) 1.15f else 1f,
        animationSpec = spring(dampingRatio = Spring.DampingRatioMediumBouncy),
        label = "buttonScale"
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(background),
        contentAlignment = Alignment.Center
    ) {
        Box(
            modifier = Modifier
                .graphicsLayer { scaleX = buttonScale; scaleY = buttonScale }
                .size(160.dp)
                .clip(CircleShape)
                .background(Color.White)
                .clickable { isOn = !isOn },
            contentAlignment = Alignment.Center
        ) {
            Crossfade(targetState = isOn, label = "emoji") { on ->
                Text(if (on) "💡" else "🌑", fontSize = 72.sp)
            }
        }
    }
}
```

💡 `scaleX = buttonScale; scaleY = buttonScale` — two short statements on **one line** with `;`.

**Task 2:**

```kotlin
@Composable
fun FaqItem(question: String, answer: String) {
    var open by remember { mutableStateOf(false) }
    val arrowAngle by animateFloatAsState(
        targetValue = if (open) 90f else 0f,
        label = "arrow"
    )

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { open = !open }
            .padding(16.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("▶️", modifier = Modifier.rotate(arrowAngle))
            Spacer(Modifier.width(12.dp))
            Text(question, style = MaterialTheme.typography.titleMedium)
        }
        AnimatedVisibility(visible = open) {
            Text(answer, modifier = Modifier.padding(start = 36.dp, top = 8.dp))
        }
    }
}

@Composable
fun Faq() {
    Column {
        FaqItem("Is Kotlin hard? 🤔", "Not at all! Step by step, anyone can learn it. 💪")
        HorizontalDivider()
        FaqItem("What is Compose? 🎨", "Android's modern way to build screens with Kotlin.")
        HorizontalDivider()
        FaqItem("Do I need a phone? 📱", "No — the emulator works great!")
    }
}
```

(Import `androidx.compose.ui.draw.rotate`.)

**Task 3:**

```kotlin
@Composable
fun CountingScore(score: Int) {
    val shownScore by animateIntAsState(
        targetValue = score,
        animationSpec = tween(durationMillis = 1000),
        label = "score"
    )
    Text("$shownScore points 🏆", style = MaterialTheme.typography.displaySmall)
}
```

Change `score` from 0 to 120 → the text counts **up** over one second. 🔢⬆️ (Import `androidx.compose.animation.core.animateIntAsState`.)

**Task 4:**

```kotlin
AnimatedContent(
    targetState = uiState.loadState,
    contentKey = { state -> state::class },                       // 👈 animate only when the TYPE changes
    transitionSpec = { fadeIn(tween(300)) togetherWith fadeOut(tween(300)) },
    label = "loadState"
) { state ->                                                      // 👈 the lambda's state!
    when (state) {
        JokesLoadState.Loading -> LoadingContent()
        is JokesLoadState.Error -> ErrorContent(message = state.message, onRetryClick = onRetryClick)
        is JokesLoadState.Success -> JokesList(
            jokes = state.jokes,
            revealedIds = uiState.revealedIds,
            onJokeClick = onJokeClick
        )
    }
}
```

💡 **`contentKey = { it::class }`** → only animate when the state changes **type** (Loading → Success). If the jokes list **inside** Success changes (a punchline is revealed), it updates **normally**, without a fade. 😎

**Task 5:**

| # | Bug | Fix |
|---|---|---|
| 1 | `Animatable(0f)` **without `remember`** → a new one on every recomposition, so the animation never continues. | `val offset = remember { Animatable(0f) }` |
| 2 | `animateTo` called directly in the Composable body → it's `suspend` (red error), and the body may run many times. | Put it in `LaunchedEffect(isWrong) { if (isWrong) { ... } }`. |
| 3 | Inside `Crossfade`, it uses **`isWrong`** instead of the lambda's value → during the fade, **both** sides show the new emoji. | `Crossfade(targetState = isWrong) { wrong -> Text(if (wrong) "❌" else "✅") }` |

Bonus 🌟: `Modifier.offset(x = offset.value.dp)` causes re-layout on every frame; `graphicsLayer { translationX = offset.value }` is faster.

**Task 6:**

```kotlin
@Composable
fun SpinningSun() {
    val infinite = rememberInfiniteTransition(label = "sun")
    val angle by infinite.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 4000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "angle"
    )
    Text("☀️", fontSize = 120.sp, modifier = Modifier.graphicsLayer { rotationZ = angle })
}
```

💡 `LinearEasing` → the **same** speed all the time (no slowing at the end of each turn). `Restart` → 360° is the same as 0°, so jumping back is invisible. A perfect, endless spin. 🔄☀️

---

## 26.21 Challenges 🚀

### Challenge 1: Swipe cards 🃏 ⭐⭐⭐
Make a "**Tinder-style**" card: drag it left or right; it **rotates** a little while dragging (`rotationZ = offsetX / 20`). Let go far enough → it **flies away** (`animateTo` a big offset); otherwise it springs back.

### Challenge 2: Confetti 🎊 ⭐⭐⭐
When the Quiz score is **perfect** (5/5), show 30 emoji 🎉🎊⭐ falling from the top with different speeds and positions.
*Hint:* `remember` a list of random start positions; one `Animatable` per piece, launched in `LaunchedEffect`.

### Challenge 3: Shared element — the note grows 📝🔍 ⭐⭐⭐
Look up **shared element transitions** in Compose (`SharedTransitionLayout`, `Modifier.sharedElement`). Make the note's **card** grow into the editor screen when tapped.

### Challenge 4: Pull-to-refresh with a bouncing dog 🐶 ⭐⭐
In the Dog Gallery (Chapter 20), show a **bouncing** 🐶 (infinite animation) instead of the spinner while loading.

### Challenge 5: Animated tab bar 🧭 ⭐⭐
In the Recipe Book's bottom bar (Chapter 16), make the **selected** icon bounce (`animateFloatAsState` with a spring) when its tab is chosen.

---

## 26.22 What Is Next?

🎉 **Part 6 complete!** Your apps now use the phone's features **and** feel smooth and delightful. ✨

But… how do you **know** your app really works? What if a change in one place **breaks** something in another? 😰 And when the app crashes, how do you find **why**?

In **Part 7 — Testing and Sharing Your App**, starting with **Chapter 27: Testing and Debugging**, you will learn:

- **Logcat** like a detective 🕵️ — reading crash messages (**stack traces**) calmly
- The **debugger**: breakpoints, stepping, and looking inside variables while the app runs 🔍
- **Unit tests** — checking small pieces of code automatically (`formatTime`, `breedNameFromUrl`, `sortedFor`…) ✅
- Testing **ViewModels** with **fake repositories** — the promise from Chapter 16! 🧪
- Testing **coroutines** and **Flows** ⏱️🌊
- **Compose UI tests** — a robot that taps your buttons for you 🤖👆
- Finding and fixing **common crashes** 💥🔧

**Wonderful work finishing Chapter 26! 🎉 Your apps don't just work — they feel alive! ✨🎬**
