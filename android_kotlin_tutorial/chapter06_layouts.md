# Chapter 6: Layouts — Putting Things in Place

> **What you will learn in this chapter**
>
> 1. The three basic layouts: `Column`, `Row`, and `Box`
> 2. Arrangement — how children **share the space** (start, center, space between…)
> 3. Alignment — how children **line up** (top, center, bottom…)
> 4. `Box` — putting things **on top of** each other
> 5. `weight` — sharing space fairly
> 6. Sizes: wrap, fill, fixed, min/max, and aspect ratio
> 7. `Spacer`, dividers, and the "push to the end" trick
> 8. Scrolling a screen
> 9. `FlowRow` — rows that wrap to the next line
> 10. How to look at any app screen and break it into layouts 🔍
> 11. Building a **Weather screen** 🌤️
>
> **Time needed:** about 4 to 5 hours.
>
> **Where to practice:** Android Studio, in your **MyFirstApp** project. Use the **Preview** a lot!

---

## 6.1 The Three Basic Layouts 📐

Almost **every** Android screen is built from just **three** layout blocks:

| Layout | Puts children… | Picture | Real-life example |
|---|---|---|---|
| **`Column`** | one **under** another ⬇️ | `▭`<br>`▭`<br>`▭` | A **shopping list** on paper |
| **`Row`** | **side by side** ➡️ | `▭ ▭ ▭` | **Books on a shelf** |
| **`Box`** | **on top of** each other 🥞 | `▣` | A **sticker on a photo** |

You **put layouts inside layouts** to build any screen:

```
Column                       ← the whole screen, top to bottom
 ├── Row                     ← a header: picture + name side by side
 │    ├── Image
 │    └── Column             ← name above the subtitle
 │         ├── Text
 │         └── Text
 ├── Box                     ← a big photo with a "NEW" label on it
 │    ├── Image
 │    └── Text ("NEW")
 └── Row                     ← buttons side by side
      ├── Button
      └── Button
```

> 💡 **Remember:** Without a layout, Compose draws all children **on the same spot** (top-left), one on top of another. That's why we always wrap many items in a `Column`, `Row`, or `Box`.

### Two directions: main axis and cross axis

Every `Column` and `Row` has **two directions**:

| | **Main direction** (the way children are lined up) | **Cross direction** (the other way) |
|---|---|---|
| `Column` | ⬇️ **Vertical** (top to bottom) | ↔️ Horizontal |
| `Row` | ➡️ **Horizontal** (left to right) | ↕️ Vertical |

And there are **two settings**, one for each direction:

| Setting | Controls | Question it answers |
|---|---|---|
| **Arrangement** | the **main** direction | "*How do the children **share the space** along the line?*" |
| **Alignment** | the **cross** direction | "*How do the children **line up** across the line?*" |

So:

| Layout | Arrangement setting | Alignment setting |
|---|---|---|
| `Column` | `verticalArrangement` | `horizontalAlignment` |
| `Row` | `horizontalArrangement` | `verticalAlignment` |

Don't worry if this sounds hard — the pictures below make it very clear! 👇

---

## 6.2 A Practice Helper 🧪

To see layouts clearly, we need **colored boxes**. Add this small helper Composable to `MainActivity.kt` (at the bottom, outside other `{ }`):

```kotlin
@Composable
fun ColorBox(
    text: String,
    color: Color,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .background(color)
            .padding(12.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(text = text, color = Color.White, fontWeight = FontWeight.Bold)
    }
}
```

- A colored rectangle with a word in the middle.
- We use `Box` here (learn it fully in 6.5) just to center the text.

We will use `ColorBox("A", Color.Red)`, `ColorBox("B", Color.Blue)`, etc. in all examples.

And a preview to try things:

```kotlin
@Preview(showBackground = true, widthDp = 320, heightDp = 400)
@Composable
fun LayoutPreview() {
    MyFirstAppTheme {
        // We will put examples here
    }
}
```

`widthDp = 320, heightDp = 400` gives a fixed-size preview area, so we can see how space is shared.

---

## 6.3 `Column` — One Under Another ⬇️

### The simplest Column

```kotlin
Column {
    ColorBox("A", Color(0xFFE53935))
    ColorBox("B", Color(0xFF1E88E5))
    ColorBox("C", Color(0xFF43A047))
}
```

```
┌──────────────┐
│[A]           │
│[B]           │
│[C]           │
│              │
│              │
└──────────────┘
```

By default:
- Children start at the **top**.
- Children line up on the **left** (the **start**).
- The Column is only as big as its children (**wrap content**).

### `horizontalAlignment` — line up left, center, or right

```kotlin
Column(
    modifier = Modifier.fillMaxWidth(),
    horizontalAlignment = Alignment.CenterHorizontally
) {
    ColorBox("A", Color(0xFFE53935))
    ColorBox("BBBB", Color(0xFF1E88E5))
    ColorBox("C", Color(0xFF43A047))
}
```

| Value | Picture |
|---|---|
| `Alignment.Start` (default) | `[A]`<br>`[BBBB]`<br>`[C]` — all on the left |
| `Alignment.CenterHorizontally` | `   [A]   `<br>` [BBBB] `<br>`   [C]   ` — all in the middle |
| `Alignment.End` | `     [A]`<br>`  [BBBB]`<br>`     [C]` — all on the right |

> ⚠️ **Important:** The Column must be **wider** than its children, or there's no room to move! That's why we added `Modifier.fillMaxWidth()`.

### `verticalArrangement` — share the space top to bottom

```kotlin
Column(
    modifier = Modifier.fillMaxSize(),
    verticalArrangement = Arrangement.SpaceBetween
) {
    ColorBox("A", Color(0xFFE53935))
    ColorBox("B", Color(0xFF1E88E5))
    ColorBox("C", Color(0xFF43A047))
}
```

Again: the Column must be **taller** than its children (`fillMaxSize()`), or there's no extra space to share.

### All the arrangements (Column, from top ⬇️ to bottom)

```
 Top          Center       Bottom       SpaceBetween  SpaceAround   SpaceEvenly  spacedBy(8.dp)
┌─────┐      ┌─────┐      ┌─────┐      ┌─────┐       ┌─────┐       ┌─────┐      ┌─────┐
│ A   │      │     │      │     │      │ A   │       │     │       │     │      │ A   │
│ B   │      │     │      │     │      │     │       │ A   │       │ A   │      │     │
│ C   │      │ A   │      │     │      │     │       │     │       │     │      │ B   │
│     │      │ B   │      │     │      │ B   │       │     │       │ B   │      │     │
│     │      │ C   │      │ A   │      │     │       │ B   │       │     │      │ C   │
│     │      │     │      │ B   │      │     │       │     │       │ C   │      │     │
│     │      │     │      │ C   │      │ C   │       │ C   │       │     │      │     │
└─────┘      └─────┘      └─────┘      └─────┘       └─────┘       └─────┘      └─────┘
```

| Arrangement | Meaning | Real-life example |
|---|---|---|
| `Arrangement.Top` (default) | All at the top, together | Books pushed to the top of a box |
| `Arrangement.Center` | All in the middle, together | A group photo in the middle of the frame |
| `Arrangement.Bottom` | All at the bottom, together | Things fallen to the bottom of a bag |
| `Arrangement.SpaceBetween` | First at top, last at bottom, equal gaps **between** | Fence posts: one at each end |
| `Arrangement.SpaceAround` | Equal space **around** each (edges get **half** a gap) | People standing with arms out |
| `Arrangement.SpaceEvenly` | **All** gaps equal, including edges | Perfectly spaced trees 🌳 🌳 🌳 |
| `Arrangement.spacedBy(8.dp)` | A **fixed** gap of 8 dp between each | Tiles with grout lines |

> 💡 **`spacedBy` is the most used one!** It's easier than putting a `Spacer` between every child.

> ⚠️ Notice: `SpaceBetween` starts with a **BIG** letter (it's a ready-made value). `spacedBy(...)` starts with a **small** letter (it's a function you call with a number).

---

## 6.4 `Row` — Side by Side ➡️

`Row` is like `Column`, but **sideways**.

```kotlin
Row {
    ColorBox("A", Color(0xFFE53935))
    ColorBox("B", Color(0xFF1E88E5))
    ColorBox("C", Color(0xFF43A047))
}
```

```
┌──────────────────────┐
│[A][B][C]             │
└──────────────────────┘
```

### `horizontalArrangement` — share the space left to right

```kotlin
Row(
    modifier = Modifier.fillMaxWidth(),
    horizontalArrangement = Arrangement.SpaceEvenly
) {
    ColorBox("A", Color(0xFFE53935))
    ColorBox("B", Color(0xFF1E88E5))
    ColorBox("C", Color(0xFF43A047))
}
```

```
Start         │[A][B][C]               │
Center        │       [A][B][C]        │
End           │               [A][B][C]│
SpaceBetween  │[A]        [B]        [C]│
SpaceAround   │  [A]     [B]     [C]  │
SpaceEvenly   │   [A]    [B]    [C]   │
spacedBy(8dp) │[A] [B] [C]             │
```

| Value | Meaning |
|---|---|
| `Arrangement.Start` (default) | All on the left (start) |
| `Arrangement.Center` | All in the middle |
| `Arrangement.End` | All on the right (end) |
| `Arrangement.SpaceBetween` / `SpaceAround` / `SpaceEvenly` / `spacedBy(...)` | Same as in Column, but sideways |

### `verticalAlignment` — line up top, center, or bottom

When children have **different heights**:

```kotlin
Row(
    modifier = Modifier.height(100.dp),
    verticalAlignment = Alignment.CenterVertically
) {
    ColorBox("Small", Color(0xFFE53935))
    ColorBox("Tall", Color(0xFF1E88E5), Modifier.height(80.dp))
    ColorBox("Mid", Color(0xFF43A047), Modifier.height(50.dp))
}
```

| Value | Picture |
|---|---|
| `Alignment.Top` (default) | `▀ █ ▀` — all touch the top |
| `Alignment.CenterVertically` | `▬ █ ▬` — all in the middle |
| `Alignment.Bottom` | `▄ █ ▄` — all touch the bottom |

> 💡 **The most common combination** for an icon next to text: `Row(verticalAlignment = Alignment.CenterVertically)`. You used it in Chapter 5's `InfoLine`!

### Quick memory table 🧠

| | Main direction → **Arrangement** | Cross direction → **Alignment** |
|---|---|---|
| **Column** ⬇️ | `verticalArrangement = Arrangement.____` | `horizontalAlignment = Alignment.____` |
| **Row** ➡️ | `horizontalArrangement = Arrangement.____` | `verticalAlignment = Alignment.____` |

**Trick:** Arrangement follows the **direction of the layout** (Column = vertical, Row = horizontal). Alignment is **the other one**.

---

## 6.5 Aligning Just One Child: `Modifier.align` 🎯

Sometimes you want **one** child to be different.

```kotlin
Column(modifier = Modifier.fillMaxWidth()) {
    ColorBox("Left (normal)", Color(0xFFE53935))
    ColorBox("Center", Color(0xFF1E88E5), Modifier.align(Alignment.CenterHorizontally))
    ColorBox("Right", Color(0xFF43A047), Modifier.align(Alignment.End))
}
```

```
┌────────────────────────┐
│[Left (normal)]         │
│       [Center]         │
│                 [Right]│
└────────────────────────┘
```

- `Modifier.align(...)` is set **on the child**, not on the Column.
- It **only works inside** a `Column`, `Row`, or `Box` (the parent gives it this power).

| Inside a… | `align` can use |
|---|---|
| `Column` | `Alignment.Start`, `CenterHorizontally`, `End` |
| `Row` | `Alignment.Top`, `CenterVertically`, `Bottom` |
| `Box` | 9 positions — see next section |

> 🎉 **Why does `align` only work inside a parent?** Because `Column { ... }` gives its children a special **scope** (`ColumnScope`) — like a **room with special tools** 🧰. Only children in that room can use those tools. This uses the **lambda with receiver** idea, like `apply` from Chapter 4!

---

## 6.6 `Box` — On Top of Each Other 🥞

In a `Box`, children are drawn **in layers**. The **first** child is at the **bottom**, the **last** child is on **top**.

**Real-life example:** A stack of **pancakes** 🥞, or **stickers** on a notebook. The last one you put down is on top.

### Basic Box

```kotlin
Box {
    ColorBox("BIG BOTTOM", Color(0xFFE53935), Modifier.size(150.dp))
    ColorBox("Top", Color(0xFF1E88E5))
}
```

```
┌───────────────┐
│[Top]          │   ← blue "Top" is drawn ON the red box
│               │
│  BIG BOTTOM   │
│               │
└───────────────┘
```

By default, children go to the **top-left** (top-start).

### `contentAlignment` — where all children go

```kotlin
Box(
    modifier = Modifier.size(200.dp),
    contentAlignment = Alignment.Center
) {
    ColorBox("Middle", Color(0xFF1E88E5))
}
```

A `Box` can put things in **9 positions**:

```
┌──────────────────────────────────┐
│ TopStart     TopCenter    TopEnd │
│                                  │
│ CenterStart   Center   CenterEnd │
│                                  │
│ BottomStart BottomCenter BottomEnd│
└──────────────────────────────────┘
```

All are written `Alignment.TopStart`, `Alignment.Center`, `Alignment.BottomEnd`, etc.

### Each child in its own place

```kotlin
Box(modifier = Modifier.size(250.dp).background(Color.LightGray)) {
    ColorBox("1", Color(0xFFE53935), Modifier.align(Alignment.TopStart))
    ColorBox("2", Color(0xFF1E88E5), Modifier.align(Alignment.TopEnd))
    ColorBox("3", Color(0xFF43A047), Modifier.align(Alignment.Center))
    ColorBox("4", Color(0xFFFB8C00), Modifier.align(Alignment.BottomStart))
    ColorBox("5", Color(0xFF8E24AA), Modifier.align(Alignment.BottomEnd))
}
```

```
┌──────────────────┐
│[1]            [2]│
│                  │
│       [3]        │
│                  │
│[4]            [5]│
└──────────────────┘
```

### Real use 1: A photo with a label on it 🏷️

```kotlin
Box {
    Image(
        painter = painterResource(R.drawable.ic_launcher_foreground),
        contentDescription = "Product photo",
        modifier = Modifier
            .size(200.dp)
            .background(Color(0xFFBBDEFB))
    )
    Text(
        text = "NEW",
        color = Color.White,
        fontWeight = FontWeight.Bold,
        modifier = Modifier
            .align(Alignment.TopEnd)
            .padding(8.dp)
            .background(Color(0xFFE53935), RoundedCornerShape(4.dp))
            .padding(horizontal = 8.dp, vertical = 2.dp)
    )
}
```

- The **Image** is first → bottom layer.
- The **"NEW" label** is second → on top, in the **top-right corner**.
- Notice the **padding–background–padding** trick from Chapter 5: space outside, red background, space inside.

### Real use 2: Text on a dark shade over a photo 🌄

```kotlin
Box(modifier = Modifier.size(width = 300.dp, height = 180.dp)) {
    Image(
        painter = painterResource(R.drawable.ic_launcher_foreground),
        contentDescription = null,
        contentScale = ContentScale.Crop,
        modifier = Modifier
            .matchParentSize()
            .background(Color(0xFF90CAF9))
    )
    Box(
        modifier = Modifier
            .matchParentSize()
            .background(
                Brush.verticalGradient(
                    listOf(Color.Transparent, Color.Black.copy(alpha = 0.7f))
                )
            )
    )
    Text(
        text = "Beautiful Mountains",
        color = Color.White,
        style = MaterialTheme.typography.titleLarge,
        modifier = Modifier
            .align(Alignment.BottomStart)
            .padding(16.dp)
    )
}
```

| Code | Meaning |
|---|---|
| `Modifier.matchParentSize()` | "Be **exactly** as big as the Box." (Only inside a `Box`.) |
| `Brush.verticalGradient(listOf(...))` | A color that **slowly changes** from top to bottom. Here: from see-through to dark. |
| 3 layers | Photo → dark shade → white text. The shade makes the text **easy to read** on any photo. 👓 |

Import: `androidx.compose.ui.graphics.Brush`

> 💡 You see this design in **many** apps: Netflix, YouTube, news apps, travel apps…

### Moving a child a little: `offset`

```kotlin
ColorBox("Moved", Color(0xFF1E88E5), Modifier.offset(x = 20.dp, y = 10.dp))
```

`offset` moves a child **20 dp to the right** and **10 dp down** from where it would be. Good for small adjustments, like a notification dot 🔴 on an icon.

---

## 6.7 `weight` — Sharing Space Fairly ⚖️

### The problem

You want two boxes in a row that **share the full width**: each gets **half**.

### The solution: `Modifier.weight`

```kotlin
Row(modifier = Modifier.fillMaxWidth()) {
    ColorBox("Left", Color(0xFFE53935), Modifier.weight(1f))
    ColorBox("Right", Color(0xFF1E88E5), Modifier.weight(1f))
}
```

```
┌───────────────────────────────┐
│[    Left     ][    Right     ]│
└───────────────────────────────┘
          50%           50%
```

- `weight(1f)` → "Take **1 share** of the free space."
- Both have `1f`, so they get **equal** shares.

**Real-life example:** Sharing a **pizza** 🍕. If Roy gets 1 share and Asha gets 1 share, each gets half. If Roy gets 2 shares and Asha gets 1, Roy gets 2/3 and Asha gets 1/3.

### Different shares

```kotlin
Row(modifier = Modifier.fillMaxWidth()) {
    ColorBox("1", Color(0xFFE53935), Modifier.weight(1f))
    ColorBox("2", Color(0xFF1E88E5), Modifier.weight(2f))
    ColorBox("1", Color(0xFF43A047), Modifier.weight(1f))
}
```

```
┌───────────────────────────────┐
│[  1  ][     2      ][  1  ]   │
└───────────────────────────────┘
   25%       50%         25%
```

Total shares = 1 + 2 + 1 = **4**. So: `1/4`, `2/4`, `1/4`.

### Mixing fixed size and weight ⭐ (very common!)

```kotlin
Row(
    modifier = Modifier.fillMaxWidth(),
    verticalAlignment = Alignment.CenterVertically
) {
    ColorBox("📷", Color(0xFF8E24AA), Modifier.size(56.dp))   // fixed
    ColorBox("Name and text — takes ALL the rest", Color(0xFF1E88E5), Modifier.weight(1f))
    ColorBox("⋮", Color(0xFF757575))                          // wraps its content
}
```

```
┌──────────────────────────────────────────┐
│[📷][Name and text — takes ALL the rest][⋮]│
└──────────────────────────────────────────┘
```

How Compose shares space:

1. **First**, children **without** weight get their size (📷 = 56 dp, ⋮ = small).
2. **Then**, the **leftover** space is shared among children **with** weight.

This is how **every list item** in a chat or contact app is built: a picture, a text that takes the rest, and a small button at the end. 📱

### `weight` in a Column

Same idea, vertically:

```kotlin
Column(modifier = Modifier.fillMaxSize()) {
    ColorBox("Header", Color(0xFF1E88E5), Modifier.fillMaxWidth())
    ColorBox("Content (takes the rest)", Color(0xFF43A047), Modifier.fillMaxWidth().weight(1f))
    ColorBox("Footer", Color(0xFFE53935), Modifier.fillMaxWidth())
}
```

```
┌────────────────┐
│[    Header    ]│
│[              ]│
│[   Content    ]│
│[ (takes the   ]│
│[    rest)     ]│
│[              ]│
│[    Footer    ]│
└────────────────┘
```

The footer is **always at the bottom**, no matter the screen size. 👍

> ⚠️ `weight` only works **inside** a `Row` or `Column`. In a `Box`, it gives an error.

---

## 6.8 The "Push to the End" Trick 🫸

A `Spacer` with `weight(1f)` **eats all the free space**, pushing the next children to the **end**.

```kotlin
Row(
    modifier = Modifier.fillMaxWidth(),
    verticalAlignment = Alignment.CenterVertically
) {
    Text("Notifications")
    Spacer(modifier = Modifier.weight(1f))
    Text("ON ✅")
}
```

```
┌────────────────────────────────────┐
│Notifications                  ON ✅│
└────────────────────────────────────┘
```

Same in a Column — push a button to the **bottom** of the screen:

```kotlin
Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
    Text("Welcome!", style = MaterialTheme.typography.headlineMedium)
    Text("This is a sign-up screen.")
    Spacer(modifier = Modifier.weight(1f))
    Button(onClick = { }, modifier = Modifier.fillMaxWidth()) {
        Text("Continue")
    }
}
```

The **Continue** button sits at the **bottom** of the screen. 👇

> 💡 This gives the same result as `Arrangement.SpaceBetween` with two children, but the Spacer trick lets you choose **exactly where** the gap goes.

---

## 6.9 Sizes — How Big Is Each Thing? 📏

### The 4 kinds of size

| Kind | Code | Meaning |
|---|---|---|
| **Wrap content** (default) | (nothing) | "Be just big enough for what's inside." |
| **Fixed** | `.size(100.dp)`, `.width(200.dp)`, `.height(50.dp)` | "Be exactly this big." |
| **Fill** | `.fillMaxWidth()`, `.fillMaxHeight()`, `.fillMaxSize()` | "Be as big as the parent allows." |
| **Share** | `.weight(1f)` | "Take a share of the leftover space." (Row/Column only) |

### Fill a part

```kotlin
ColorBox("Half", Color(0xFF1E88E5), Modifier.fillMaxWidth(0.5f))   // 50% of the width
ColorBox("80%", Color(0xFF43A047), Modifier.fillMaxWidth(0.8f))    // 80%
```

### Minimum and maximum sizes

```kotlin
Text(
    text = "Hi",
    modifier = Modifier
        .widthIn(min = 100.dp, max = 250.dp)
        .background(Color.Yellow)
)
```

| Code | Meaning |
|---|---|
| `.widthIn(min = 100.dp)` | At least 100 dp wide (can be bigger). |
| `.widthIn(max = 250.dp)` | At most 250 dp wide (long text goes to a new line). |
| `.heightIn(min = 48.dp)` | At least 48 dp tall — great for things you tap 👆. |
| `.defaultMinSize(minWidth = ..., minHeight = ...)` | A minimum size the child can still override. |

**Real-life example:** A **chat bubble** 💬 — short messages are small, long messages grow, but never wider than 250 dp.

### `aspectRatio` — keep the shape

```kotlin
ColorBox(
    "16:9 video",
    Color(0xFF212121),
    Modifier
        .fillMaxWidth()
        .aspectRatio(16f / 9f)
)
```

- `aspectRatio(16f / 9f)` → "Height = width × 9 ÷ 16." The shape of a **YouTube video** 📺.
- `aspectRatio(1f)` → a perfect **square**.

> 💡 Combine `fillMaxWidth()` + `aspectRatio(...)` so pictures look right on **every** phone size.

---

## 6.10 Spacers and Dividers ➖

### `Spacer` (from Chapter 5)

```kotlin
Spacer(modifier = Modifier.height(16.dp))   // in a Column: vertical space
Spacer(modifier = Modifier.width(16.dp))    // in a Row: horizontal space
Spacer(modifier = Modifier.weight(1f))      // eat all free space
```

### Dividers — a thin line

```kotlin
Column {
    Text("Item 1", modifier = Modifier.padding(16.dp))
    HorizontalDivider()
    Text("Item 2", modifier = Modifier.padding(16.dp))
    HorizontalDivider(thickness = 2.dp, color = Color.LightGray)
    Text("Item 3", modifier = Modifier.padding(16.dp))
}
```

```
Item 1
─────────────────
Item 2
━━━━━━━━━━━━━━━━━
Item 3
```

| Composable | Draws |
|---|---|
| `HorizontalDivider()` | A thin line **across** (use in a Column) |
| `VerticalDivider()` | A thin line **up and down** (use in a Row with a fixed height) |

Import: `androidx.compose.material3.HorizontalDivider`

### `spacedBy` vs `Spacer` vs `padding` — which one?

| You want… | Use |
|---|---|
| The **same** gap between **all** children | `Arrangement.spacedBy(8.dp)` ⭐ |
| A **different** gap in one place | `Spacer(Modifier.height(24.dp))` |
| Space **around** the whole layout | `Modifier.padding(16.dp)` on the layout |
| Push things apart | `Spacer(Modifier.weight(1f))` |

---

## 6.11 Scrolling 📜

What if the content is **taller than the screen**? By default, the extra part is **cut off** and you can't see it. 😱

### Vertical scroll

```kotlin
Column(
    modifier = Modifier
        .fillMaxSize()
        .verticalScroll(rememberScrollState())
) {
    repeat(30) { number ->
        Text(
            text = "Line number ${number + 1}",
            modifier = Modifier.padding(16.dp)
        )
    }
}
```

Imports:

```kotlin
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
```

| Code | Meaning |
|---|---|
| `.verticalScroll(...)` | "Let the user **swipe up and down** to see everything." |
| `rememberScrollState()` | Remembers **how far** the user has scrolled. (We learn about `remember` in Chapter 8.) |
| `repeat(30) { number -> ... }` | Makes 30 Texts. `number` goes from 0 to 29, so we show `number + 1`. |

### Horizontal scroll

```kotlin
Row(
    modifier = Modifier.horizontalScroll(rememberScrollState()),
    horizontalArrangement = Arrangement.spacedBy(8.dp)
) {
    repeat(10) { i ->
        ColorBox("Card ${i + 1}", Color(0xFF1E88E5), Modifier.size(100.dp))
    }
}
```

Swipe **left and right**. Like a row of movie posters 🎬.

### ⚠️ Important warning about long lists

`verticalScroll` draws **every** child, even the ones you can't see.
- **10–50 items?** ✅ Fine.
- **Hundreds or thousands of items** (like contacts or messages)? ❌ Slow! Use **`LazyColumn`** instead — it only draws what is on the screen. We learn it in **Chapter 10**.

> ⚠️ Don't put `.weight(...)` children or `fillMaxHeight()` inside a `verticalScroll` Column — a scrolling column has **no end**, so "fill the rest" makes no sense there.

---

## 6.12 `FlowRow` — Rows That Wrap 🌊

A normal `Row` puts everything on **one line** — if there's too much, it gets **cut off**.
A **`FlowRow`** goes to the **next line** when there's no more room. Like words in a book! 📖

```kotlin
FlowRow(
    horizontalArrangement = Arrangement.spacedBy(8.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp)
) {
    listOf("Kotlin", "Android", "Compose", "Material", "Coroutines", "Room", "Retrofit", "Hilt")
        .forEach { tag ->
            ColorBox(tag, Color(0xFF00897B))
        }
}
```

```
[Kotlin] [Android] [Compose]
[Material] [Coroutines] [Room]
[Retrofit] [Hilt]
```

Import: `androidx.compose.foundation.layout.FlowRow`

- Perfect for **tags**, **chips**, **filters** 🏷️.
- There is also **`FlowColumn`** (goes to the next column when there's no room).

> ⚠️ **If you see an error** like *"This foundation API is experimental"*, your Compose version is a bit older. Add this line **above** your Composable function:
> ```kotlin
> @OptIn(ExperimentalLayoutApi::class)
> ```
> It means: "*I know this is new, I want to use it anyway.*"

---

## 6.13 How to Break Any Screen Into Layouts 🔍

This is the **most important skill** in this chapter. Before you write code, **look at the design** and find the Rows, Columns, and Boxes.

### The method (4 steps)

1. **Find the big parts** from top to bottom → that is usually a **`Column`**.
2. Inside each part, are things **side by side**? → **`Row`**.
3. Are things **on top of** each other (text on a photo, a badge on an icon)? → **`Box`**.
4. Repeat for smaller parts until you reach `Text`, `Image`, `Icon`, `Button`.

### Example: a chat list item 💬

```
┌──────────────────────────────────────────┐
│ ┌────┐  Asha Sharma               10:42  │
│ │ 👩 │  Are we still meeting today?  (2) │
│ └────┘                                    │
└──────────────────────────────────────────┘
```

Let's break it down:

```
Row (verticalAlignment = CenterVertically)
 ├── Image (round photo, size 56.dp)
 ├── Spacer (width 12.dp)
 ├── Column (weight 1f)                ← takes all the middle space
 │    ├── Text ("Asha Sharma", bold)
 │    └── Text ("Are we still...", maxLines = 1, Ellipsis)
 └── Column (horizontalAlignment = End)
      ├── Text ("10:42", small)
      └── Box (round, primary color)   ← the unread badge
           └── Text ("2")
```

And the code:

```kotlin
@Composable
fun ChatItem(
    name: String,
    message: String,
    time: String,
    unread: Int,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Photo
        Image(
            painter = painterResource(R.drawable.ic_launcher_foreground),
            contentDescription = "Photo of $name",
            modifier = Modifier
                .size(56.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primaryContainer)
        )

        Spacer(modifier = Modifier.width(12.dp))

        // Name and last message
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = name,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = message,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }

        Spacer(modifier = Modifier.width(8.dp))

        // Time and unread badge
        Column(horizontalAlignment = Alignment.End) {
            Text(
                text = time,
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(modifier = Modifier.height(4.dp))
            if (unread > 0) {
                Box(
                    modifier = Modifier
                        .size(22.dp)
                        .background(MaterialTheme.colorScheme.primary, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = unread.toString(),
                        color = MaterialTheme.colorScheme.onPrimary,
                        style = MaterialTheme.typography.labelSmall
                    )
                }
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun ChatItemPreview() {
    MyFirstAppTheme {
        Column {
            ChatItem("Asha Sharma", "Are we still meeting today? I can bring the notes.", "10:42", 2)
            HorizontalDivider()
            ChatItem("Ben", "Thanks! 👍", "Yesterday", 0)
        }
    }
}
```

### New things in this code

| Code | Meaning |
|---|---|
| `Column(modifier = Modifier.weight(1f))` | The middle part takes **all leftover** width. So long names/messages don't push the time off the screen. |
| `maxLines = 1, overflow = TextOverflow.Ellipsis` | Long message → `Are we still meeting tod...` |
| `if (unread > 0) { Box(...) }` | ⭐ **You can use `if` inside Composables!** The badge is shown **only** when there are unread messages. |
| `unread.toString()` | `Text` needs a `String`, so we change the `Int` into text (Chapter 2). |
| `onSurfaceVariant` | A softer text color from the theme, for less important text. |

> 🎉 **This is a real, professional design!** Apps like WhatsApp and Telegram use almost exactly this layout.

---

## 6.14 Build It: A Weather Screen 🌤️

Let's build a full, scrollable weather screen using **everything** from this chapter.

```
┌──────────────────────────────────┐
│ Mumbai                    ⚙️      │  ← Row + Spacer weight trick
│ Monday, 14 October               │
│                                  │
│              ☀️                  │  ← Column, centered
│             32°                  │
│            Sunny                 │
│       H: 34°   L: 26°            │
│                                  │
│ ┌────────┐┌────────┐┌────────┐   │  ← Row with 3 × weight(1f)
│ │💧 70%  ││💨 12km ││🌧️ 10% │   │
│ │Humidity││ Wind   ││ Rain   │   │
│ └────────┘└────────┘└────────┘   │
│                                  │
│ Today                            │
│ [Now][1PM][2PM][3PM][4PM] → →    │  ← horizontal scroll
│                                  │
│ Next 5 days                      │
│ Tue   🌤️          33° / 26°      │  ← Rows with weight
│ Wed   ⛅          31° / 25°      │
│ ...                              │
└──────────────────────────────────┘
```

We use **emojis** for weather pictures, so you don't need any image files. 😊

### The full code

Replace **everything** in `MainActivity.kt` with this:

```kotlin
package com.example.myfirstapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.myfirstapp.ui.theme.MyFirstAppTheme

// ---------- Data ----------

data class HourForecast(val time: String, val emoji: String, val temperature: Int)

data class DayForecast(val day: String, val emoji: String, val high: Int, val low: Int)

val hourlyForecast = listOf(
    HourForecast("Now", "☀️", 32),
    HourForecast("1 PM", "☀️", 33),
    HourForecast("2 PM", "🌤️", 34),
    HourForecast("3 PM", "⛅", 33),
    HourForecast("4 PM", "⛅", 31),
    HourForecast("5 PM", "🌥️", 30),
    HourForecast("6 PM", "🌧️", 28),
    HourForecast("7 PM", "🌧️", 27)
)

val dailyForecast = listOf(
    DayForecast("Tuesday", "🌤️", 33, 26),
    DayForecast("Wednesday", "⛅", 31, 25),
    DayForecast("Thursday", "🌧️", 29, 24),
    DayForecast("Friday", "⛈️", 28, 24),
    DayForecast("Saturday", "☀️", 32, 25)
)

// ---------- Activity ----------

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyFirstAppTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    WeatherScreen(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

// ---------- Screen ----------

@Composable
fun WeatherScreen(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        WeatherHeader(city = "Mumbai", date = "Monday, 14 October")

        Spacer(modifier = Modifier.height(24.dp))

        CurrentWeather(
            emoji = "☀️",
            temperature = 32,
            description = "Sunny",
            high = 34,
            low = 26,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(24.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            InfoTile(emoji = "💧", value = "70%", label = "Humidity", modifier = Modifier.weight(1f))
            InfoTile(emoji = "💨", value = "12 km/h", label = "Wind", modifier = Modifier.weight(1f))
            InfoTile(emoji = "🌧️", value = "10%", label = "Rain", modifier = Modifier.weight(1f))
        }

        Spacer(modifier = Modifier.height(24.dp))

        SectionTitle("Today")
        Row(
            modifier = Modifier.horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            hourlyForecast.forEach { hour ->
                HourItem(hour)
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        SectionTitle("Next 5 days")
        dailyForecast.forEachIndexed { index, day ->
            DayRow(day)
            if (index < dailyForecast.lastIndex) {
                HorizontalDivider()
            }
        }
    }
}

// ---------- Small parts ----------

@Composable
fun WeatherHeader(city: String, date: String, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column {
            Text(
                text = city,
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = date,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Spacer(modifier = Modifier.weight(1f))
        Text(text = "⚙️", fontSize = 24.sp)
    }
}

@Composable
fun CurrentWeather(
    emoji: String,
    temperature: Int,
    description: String,
    high: Int,
    low: Int,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(text = emoji, fontSize = 80.sp)
        Text(
            text = "$temperature°",
            fontSize = 72.sp,
            fontWeight = FontWeight.Light
        )
        Text(text = description, style = MaterialTheme.typography.titleLarge)
        Spacer(modifier = Modifier.height(4.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            Text("H: $high°", style = MaterialTheme.typography.bodyLarge)
            Text("L: $low°", style = MaterialTheme.typography.bodyLarge)
        }
    }
}

@Composable
fun InfoTile(emoji: String, value: String, label: String, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .background(MaterialTheme.colorScheme.secondaryContainer, RoundedCornerShape(16.dp))
            .padding(vertical = 12.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(text = emoji, fontSize = 24.sp)
        Text(
            text = value,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold
        )
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.onSecondaryContainer
        )
    }
}

@Composable
fun SectionTitle(text: String, modifier: Modifier = Modifier) {
    Text(
        text = text,
        style = MaterialTheme.typography.titleMedium,
        fontWeight = FontWeight.Bold,
        modifier = modifier.padding(bottom = 8.dp)
    )
}

@Composable
fun HourItem(hour: HourForecast, modifier: Modifier = Modifier) {
    val isNow = hour.time == "Now"
    val background = if (isNow) {
        MaterialTheme.colorScheme.primary
    } else {
        MaterialTheme.colorScheme.surfaceVariant
    }
    val textColor = if (isNow) {
        MaterialTheme.colorScheme.onPrimary
    } else {
        MaterialTheme.colorScheme.onSurfaceVariant
    }

    Column(
        modifier = modifier
            .width(64.dp)
            .background(background, RoundedCornerShape(32.dp))
            .padding(vertical = 12.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(6.dp)
    ) {
        Text(text = hour.time, color = textColor, style = MaterialTheme.typography.labelMedium)
        Text(text = hour.emoji, fontSize = 22.sp)
        Text(
            text = "${hour.temperature}°",
            color = textColor,
            fontWeight = FontWeight.Bold
        )
    }
}

@Composable
fun DayRow(day: DayForecast, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = day.day,
            style = MaterialTheme.typography.bodyLarge,
            modifier = Modifier.weight(1f)
        )
        Text(
            text = day.emoji,
            fontSize = 22.sp,
            textAlign = TextAlign.Center,
            modifier = Modifier.weight(1f)
        )
        Text(
            text = "${day.high}° / ${day.low}°",
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.End,
            modifier = Modifier.weight(1f)
        )
    }
}

// ---------- Preview ----------

@Preview(showBackground = true, showSystemUi = true)
@Composable
fun WeatherScreenPreview() {
    MyFirstAppTheme {
        WeatherScreen()
    }
}
```

> ⚠️ Keep **your own** `package` line and theme import if they are different.
> ℹ️ If you try the "Make it yours" ideas below and `Color` turns red, press **Alt + Enter** to import it.

### Every part explained

#### Part 1: The data

```kotlin
data class HourForecast(val time: String, val emoji: String, val temperature: Int)
data class DayForecast(val day: String, val emoji: String, val high: Int, val low: Int)
```

- Two **data classes** (Chapter 3) describe **one hour** and **one day** of weather.

```kotlin
val hourlyForecast = listOf(
    HourForecast("Now", "☀️", 32),
    ...
)
```

- Lists of example data, written **outside** any function (at the "top level" of the file), so every Composable can use them.
- Later (Chapter 19), this data will come from the **internet**! 🌐

#### Part 2: `WeatherScreen` — the big Column

```kotlin
    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
```

| Code | Meaning |
|---|---|
| `.fillMaxSize()` | Use the whole screen. |
| `.verticalScroll(rememberScrollState())` | The screen can **scroll** if it's taller than the phone. |
| `.padding(16.dp)` | Keep content away from the edges. It's **after** the scroll, so the padding scrolls **with** the content. |

The screen is built from **small, named parts**: `WeatherHeader`, `CurrentWeather`, `InfoTile`, `SectionTitle`, `HourItem`, `DayRow`. The main function reads like a **table of contents**. 📖

#### Part 3: Three equal tiles with `weight`

```kotlin
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            InfoTile(..., modifier = Modifier.weight(1f))
            InfoTile(..., modifier = Modifier.weight(1f))
            InfoTile(..., modifier = Modifier.weight(1f))
        }
```

- Each tile gets **1 share** → three **equal** tiles, on **any** screen size.
- `spacedBy(8.dp)` → 8 dp gap between them.
- We pass `Modifier.weight(1f)` **from outside** into each `InfoTile`'s `modifier` input. That's why every Composable should accept a `modifier`! ✅

#### Part 4: Horizontal scrolling hours

```kotlin
        Row(
            modifier = Modifier.horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            hourlyForecast.forEach { hour ->
                HourItem(hour)
            }
        }
```

- `forEach` (Chapter 3) inside a Composable → one `HourItem` **for each** hour in the list. 🔁
- `horizontalScroll` → swipe left/right to see later hours.

#### Part 5: The daily list with dividers

```kotlin
        dailyForecast.forEachIndexed { index, day ->
            DayRow(day)
            if (index < dailyForecast.lastIndex) {
                HorizontalDivider()
            }
        }
```

| Code | Meaning |
|---|---|
| `forEachIndexed { index, day -> }` | Like `forEach`, but also gives the **position** (0, 1, 2…). |
| `dailyForecast.lastIndex` | The position of the **last** item (`size - 1` = 4). |
| `if (index < lastIndex)` | Draw a divider **between** rows, but **not after the last one**. A small detail that looks professional ✨. |

#### Part 6: `WeatherHeader` — the push-to-end trick

```kotlin
    Row(...) {
        Column { /* city and date */ }
        Spacer(modifier = Modifier.weight(1f))
        Text(text = "⚙️", fontSize = 24.sp)
    }
```

The Spacer eats the middle space, pushing ⚙️ to the **right edge**.

#### Part 7: `HourItem` — choosing colors with `if`

```kotlin
    val isNow = hour.time == "Now"
    val background = if (isNow) {
        MaterialTheme.colorScheme.primary
    } else {
        MaterialTheme.colorScheme.surfaceVariant
    }
```

- `if` **gives back a value** (Chapter 2). The "Now" item gets the **main color**; the others get a soft color.
- `RoundedCornerShape(32.dp)` on a 64 dp wide item → a **pill** shape 💊.

#### Part 8: `DayRow` — three equal columns

```kotlin
        Text(text = day.day, modifier = Modifier.weight(1f))
        Text(text = day.emoji, textAlign = TextAlign.Center, modifier = Modifier.weight(1f))
        Text(text = "...", textAlign = TextAlign.End, modifier = Modifier.weight(1f))
```

- Each text gets **1/3** of the width.
- `textAlign` puts the text **inside** its third: left, center, right.
- Because all rows use the same weights, the emojis and temperatures line up **perfectly** in columns, like a table. 📊

### Run it! ▶️

You will see a beautiful weather screen. Scroll down to see the 5-day forecast. Swipe the hourly row left and right. 🎉

### Make it yours ✏️

1. Change the city to **your** city.
2. Add more hours to `hourlyForecast`.
3. Change the `InfoTile` background to `Color(0xFFE3F2FD)` (light blue).
4. Add a 4th `InfoTile` for "UV index" — see how `weight` shares the space between 4 tiles automatically!

---

## 6.15 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| Arrangement does nothing | The Column/Row is only as big as its children — no extra space | Add `fillMaxSize()` / `fillMaxWidth()` to the layout. |
| Mixing up arrangement and alignment | *No parameter with name 'verticalAlignment' found* (in a Column) | Column: `verticalArrangement` + `horizontalAlignment`. Row: the opposite. |
| `Alignment.CenterVertically` in a Column | *Type mismatch* | Column needs a **horizontal** alignment: `Alignment.CenterHorizontally`. |
| `weight` outside Row/Column | *Unresolved reference: weight* | Use `weight` only on direct children of a `Row` or `Column`. |
| `align` in the wrong place | *Unresolved reference: align* | Use `Modifier.align` only on direct children of `Column`/`Row`/`Box`. |
| Content cut off at the bottom | No scrolling | Add `.verticalScroll(rememberScrollState())`. |
| `weight` or `fillMaxHeight` inside a scrolling Column | Error: *Vertically scrollable component was measured with an infinity maximum height constraint* | A scrolling Column has no end. Use fixed heights inside it. |
| Long text pushes other items off the screen | The text takes all the width | Give the text `Modifier.weight(1f)` and `maxLines` + `overflow`. |
| Box children in the wrong order | The photo covers the text | In a `Box`, the **last** child is on top. Put the text **after** the image. |
| Hundreds of items with `verticalScroll` | The app is slow | Use `LazyColumn` (Chapter 10). |

---

## 6.16 Summary — What You Learned 🎓

✅ **Three layouts:** `Column` ⬇️ (under), `Row` ➡️ (side by side), `Box` 🥞 (on top).

✅ **Arrangement** = main direction (sharing space): `Top/Start`, `Center`, `Bottom/End`, `SpaceBetween`, `SpaceAround`, `SpaceEvenly`, `spacedBy(...)`.

✅ **Alignment** = cross direction (lining up): Column → `Start / CenterHorizontally / End`; Row → `Top / CenterVertically / Bottom`.

✅ **`Modifier.align`** — one child is different.

✅ **`Box`:** `contentAlignment`, 9 positions, `matchParentSize`, layers (last is on top), gradients, `offset`.

✅ **`weight`:** share leftover space. Fixed sizes first, then shares.

✅ **Spacer + weight** pushes things to the end.

✅ **Sizes:** wrap, fixed, fill, share; `widthIn`/`heightIn`; `aspectRatio`.

✅ **Dividers:** `HorizontalDivider`, `VerticalDivider`.

✅ **Scrolling:** `verticalScroll` / `horizontalScroll` with `rememberScrollState()`. Long lists → `LazyColumn` (Chapter 10).

✅ **`FlowRow`:** wraps to the next line.

✅ **Breaking a design into layouts** — the most important skill.

✅ You built a **Chat item** and a full **Weather screen**!

---

## 6.17 Practice Time 🏋️

Use the **Preview** for all tasks. Answers are below!

**Task 1 — Centered login title:**
Make a full-screen `Column` where the title `"Welcome Back!"` and a `Button` `"Log in"` are both in the **exact center** of the screen (up/down and left/right), with 16 dp between them.

**Task 2 — Settings row:**
Make `SettingRow(title: String, value: String)`. The title is on the left, the value is on the right edge (grey). Show three rows: `Language — English`, `Theme — Dark`, `Version — 1.0`, with dividers between them.

**Task 3 — Traffic light 🚦:**
Draw a traffic light: a dark grey rounded rectangle with three circles (red, yellow, green) one under another, centered, with space between them.

**Task 4 — Profile picture with online dot:**
Make a 80 dp round picture (any image) with a small 18 dp **green dot** with a white border at the **bottom-right** corner. (Hint: `Box`.)

**Task 5 — 3-part screen:**
Make a full screen: a header (blue, 64 dp tall), a content area that takes **all the rest** (light grey, with the text "Content" in the center), and a footer (blue, 56 dp tall).

**Task 6 — Break it down 🔍:**
Write (as a comment, no code needed) the layout tree for this design:

```
┌────────────────────────────────────┐
│ ┌──────────────────────────────┐   │
│ │      [ big photo ]     ❤️    │   │  ← heart in the top-right of the photo
│ └──────────────────────────────┘   │
│ Cozy Apartment          ⭐ 4.8     │
│ Lisbon, Portugal                   │
│ $120 / night                       │
└────────────────────────────────────┘
```

---

### Answers

**Task 1:**

```kotlin
@Composable
fun LoginCenter(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.fillMaxSize(),
        verticalArrangement = Arrangement.spacedBy(16.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Welcome Back!", style = MaterialTheme.typography.headlineMedium)
        Button(onClick = { }) {
            Text("Log in")
        }
    }
}
```

💡 **New trick:** `Arrangement.spacedBy(16.dp, Alignment.CenterVertically)` → "16 dp between children, **and** put the whole group in the center." Two settings in one!

**Task 2:**

```kotlin
@Composable
fun SettingRow(title: String, value: String, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(text = title, style = MaterialTheme.typography.bodyLarge)
        Spacer(modifier = Modifier.weight(1f))
        Text(
            text = value,
            style = MaterialTheme.typography.bodyLarge,
            color = Color.Gray
        )
    }
}

@Preview(showBackground = true)
@Composable
fun SettingsPreview() {
    MyFirstAppTheme {
        Column {
            SettingRow("Language", "English")
            HorizontalDivider()
            SettingRow("Theme", "Dark")
            HorizontalDivider()
            SettingRow("Version", "1.0")
        }
    }
}
```

**Task 3:**

```kotlin
@Composable
fun TrafficLight(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .background(Color(0xFF424242), RoundedCornerShape(24.dp))
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Box(Modifier.size(60.dp).background(Color.Red, CircleShape))
        Box(Modifier.size(60.dp).background(Color.Yellow, CircleShape))
        Box(Modifier.size(60.dp).background(Color.Green, CircleShape))
    }
}
```

An **empty** `Box` with a size and a background is a simple way to draw a colored shape! 🔴🟡🟢

**Task 4:**

```kotlin
@Composable
fun AvatarWithStatus(modifier: Modifier = Modifier) {
    Box(modifier = modifier) {
        Image(
            painter = painterResource(R.drawable.ic_launcher_foreground),
            contentDescription = "Profile picture",
            modifier = Modifier
                .size(80.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primaryContainer)
        )
        Box(
            modifier = Modifier
                .align(Alignment.BottomEnd)
                .size(18.dp)
                .background(Color.White, CircleShape)
                .padding(3.dp)
                .background(Color(0xFF4CAF50), CircleShape)
        )
    }
}
```

The dot uses the **background–padding–background** trick: a white circle, then 3 dp of space, then a green circle inside → a green dot with a **white ring**. ✨

**Task 5:**

```kotlin
@Composable
fun ThreePartScreen(modifier: Modifier = Modifier) {
    Column(modifier = modifier.fillMaxSize()) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(64.dp)
                .background(Color(0xFF1E88E5))
        )
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .background(Color(0xFFEEEEEE)),
            contentAlignment = Alignment.Center
        ) {
            Text("Content")
        }
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp)
                .background(Color(0xFF1E88E5))
        )
    }
}
```

**Task 6:**

```kotlin
// Column
//  ├── Box  (fillMaxWidth, aspectRatio, rounded corners)
//  │    ├── Image (matchParentSize, ContentScale.Crop)
//  │    └── Icon ❤️ (align = TopEnd, padding)
//  ├── Row (verticalAlignment = CenterVertically)
//  │    ├── Text "Cozy Apartment" (weight 1f)
//  │    └── Text "⭐ 4.8"
//  ├── Text "Lisbon, Portugal" (grey)
//  └── Text "$120 / night" (bold)
```

> 💡 Try to build this design in code too! It's a great extra practice. (Hint: inside a Kotlin String, write `\$120` to show a real dollar sign — Chapter 2.)

---

## 6.18 What Is Next?

In **Chapter 7: Making It Beautiful — Material 3**, you will learn:

- What **Material Design 3** is
- Your app's **theme** files: `Color.kt`, `Theme.kt`, `Type.kt` — explained line by line
- Making your **own color scheme** (and using the Material Theme Builder)
- **Dynamic color** — colors from the user's wallpaper 🎨
- **Dark mode** done right 🌙
- Custom **fonts** (like Google Fonts)
- **Shapes**
- `Surface` and `Card` (filled, outlined, elevated)

**Great job finishing Chapter 6! 🎉 You can now build almost any screen layout!**
