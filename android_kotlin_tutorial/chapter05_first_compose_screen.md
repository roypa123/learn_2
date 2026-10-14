# Chapter 5: Your First Compose Screen — Text, Images, Buttons, and Modifiers

> **What you will learn in this chapter**
>
> 1. What Jetpack Compose really is, and how it thinks
> 2. The rules of Composable functions
> 3. Showing and styling text with `Text`
> 4. Sizes in Android: `dp` and `sp`
> 5. Colors
> 6. Showing pictures with `Image`
> 7. Showing small symbols with `Icon`
> 8. Making `Button`s that do something
> 9. Modifiers — changing size, space, color, shape, and more
> 10. Using the Preview like a pro
> 11. Building a **Profile Card** screen 🪪
>
> **Time needed:** about 4 to 5 hours.
>
> **Where to practice:** Android Studio, in your **MyFirstApp** project (from Chapter 1). From now on, we work in Android Studio, not in the Kotlin Playground.

---

## 5.1 What Is Jetpack Compose? 🧱

### The old way vs the new way

There are two ways to tell a computer how to make a screen.

**The old way (imperative = "giving orders step by step"):**

> *"Make a text box. Now set its words to 'Hello'. Now the user tapped — find the text box, change its words to 'Bye'. Now make it red…"*

You must **remember** every part of the screen and **change** it by hand. Easy to forget something. 🐛

**The new way — Compose (declarative = "describing what you want"):**

> *"The screen shows a text. If the user tapped, the text says 'Bye' in red. Otherwise, it says 'Hello'."*

You **describe** what the screen should look like **for the current data**. When the data changes, Compose **redraws** the parts that need it, **automatically**. ✨

**Real-life example:**

- **Old way:** You tell a painter: "*Paint a bit of blue here. Now erase that corner. Now add a little red…*"
- **New way:** You show the painter a **photo**: "*Make it look like this.*" When you want a change, you show a **new photo**. The painter figures out what to change.

### Compose is LEGO 🧱

In Compose, a screen is made of small blocks. Each block is a **Composable function**.

```
Screen
 └── Column (puts things one under another)
      ├── Image   (a photo)
      ├── Text    (a name)
      ├── Text    (a job title)
      └── Button  (a "Follow" button)
           └── Text ("Follow")
```

You **put blocks inside blocks** to make the whole screen. Small blocks → bigger blocks → the whole app.

---

## 5.2 The Rules of Composable Functions 📏

You met your first Composable in Chapter 1:

```kotlin
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}
```

Here are the **rules**:

| # | Rule | Why |
|---|---|---|
| 1 | Must have **`@Composable`** above it. | This label tells Compose: "*This function draws UI.*" |
| 2 | Name starts with a **BIG letter**: `Greeting`, `ProfileCard`. | It's a **thing on the screen** (a noun), not an action. Normal functions start small: `calculateTotal()`. |
| 3 | Usually **returns nothing** (no `: String`, no `return`). | It **draws**, it doesn't give back a value. |
| 4 | Can only be **called from another Composable** (or from `setContent { }`). | Compose needs to **track** where each block is on the screen. |
| 5 | Should have a **`modifier: Modifier = Modifier`** input. | So the **caller** can change its size, spacing, etc. (See 5.9.) |
| 6 | Should be **fast** and **have no side effects**. | Compose may run it **many times** (every time something changes). Don't do slow work in it. |

**Rule 4 example:**

```kotlin
fun normalFunction() {
    Text("Hi")   // ❌ ERROR: @Composable invocations can only happen
                 //    from the context of a @Composable function
}
```

### How to make your own Composable

```kotlin
@Composable
fun WelcomeMessage() {
    Text("Welcome to my app! 🎉")
}
```

And use it like any other block:

```kotlin
setContent {
    MyFirstAppTheme {
        WelcomeMessage()
    }
}
```

---

## 5.3 Starting Fresh 🧹

Let's clean `MainActivity.kt` so we have a simple place to practice.

Replace **everything** in `MainActivity.kt` with this:

```kotlin
package com.example.myfirstapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.myfirstapp.ui.theme.MyFirstAppTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyFirstAppTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    PracticeScreen(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

@Composable
fun PracticeScreen(modifier: Modifier = Modifier) {
    Text(
        text = "Let's practice! 🚀",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun PracticeScreenPreview() {
    MyFirstAppTheme {
        PracticeScreen()
    }
}
```

> ⚠️ If your package name is different (not `com.example.myfirstapp`), keep **your** first line and **your** theme import. Only change the rest.

What changed from Chapter 1:
- `Greeting` is now called **`PracticeScreen`**.
- The preview shows `PracticeScreen`.

Click **Split** (top right of the editor) to see the Preview. You should see: **Let's practice! 🚀**

In this chapter, you will change the inside of `PracticeScreen` again and again to try new things.

> 💡 **Missing import?** When a word turns **red**, click it and press **Alt + Enter** → **Import**. You will do this many times in this chapter. It is normal!

---

## 5.4 The `Text` Composable — Showing Words 📝

`Text` shows words on the screen. It has **many** optional inputs to change how the words look.

### Basic text

```kotlin
Text(text = "Hello!")
Text("Hello!")          // same thing — "text" is the first input, so the name can be skipped
```

### Making text bigger, bolder, colorful

```kotlin
@Composable
fun PracticeScreen(modifier: Modifier = Modifier) {
    Text(
        text = "Big Red Bold Text",
        fontSize = 32.sp,
        color = Color.Red,
        fontWeight = FontWeight.Bold,
        modifier = modifier
    )
}
```

Imports you will need (Alt + Enter will add them):

```kotlin
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
```

### Every bit explained

| Input | Meaning |
|---|---|
| `text = "..."` | The words to show. |
| `fontSize = 32.sp` | How **big** the letters are. `sp` is a size unit for text (see 5.5). |
| `color = Color.Red` | The **color** of the letters. |
| `fontWeight = FontWeight.Bold` | How **thick** the letters are. |
| `modifier = modifier` | Size/space changes from outside (see 5.9). |

### All the useful `Text` inputs

| Input | Example | What it does |
|---|---|---|
| `fontSize` | `24.sp` | Letter size |
| `color` | `Color.Blue` | Letter color |
| `fontWeight` | `FontWeight.Bold`, `FontWeight.Light`, `FontWeight.Black` | Thickness |
| `fontStyle` | `FontStyle.Italic` | *Slanted* letters |
| `fontFamily` | `FontFamily.Serif`, `FontFamily.Monospace`, `FontFamily.Cursive` | Kind of letters |
| `textAlign` | `TextAlign.Center` | Left / center / right |
| `textDecoration` | `TextDecoration.Underline`, `TextDecoration.LineThrough` | Underline or ~~strike~~ |
| `letterSpacing` | `2.sp` | Space between letters |
| `lineHeight` | `28.sp` | Space between lines |
| `maxLines` | `1` | Most lines to show |
| `overflow` | `TextOverflow.Ellipsis` | What to do if text is too long (`...`) |
| `style` | `MaterialTheme.typography.titleLarge` | Use a ready-made text style |

### Example: many styles

```kotlin
@Composable
fun PracticeScreen(modifier: Modifier = Modifier) {
    Column(modifier = modifier) {
        Text("Normal text")
        Text("Bold text", fontWeight = FontWeight.Bold)
        Text("Italic text", fontStyle = FontStyle.Italic)
        Text("Big text", fontSize = 30.sp)
        Text("Blue text", color = Color.Blue)
        Text("Underlined", textDecoration = TextDecoration.Underline)
        Text("Crossed out", textDecoration = TextDecoration.LineThrough)
        Text("Monospace font", fontFamily = FontFamily.Monospace)
        Text("S P A C E D", letterSpacing = 4.sp)
    }
}
```

> 📦 **What is `Column`?** It puts its children **one under another** (in a column). Without it, all texts would be drawn **on top of each other** in one spot! We learn `Column` fully in **Chapter 6**. For now, just wrap many items in `Column { ... }`.

### Long text: `maxLines` and `overflow`

```kotlin
Text(
    text = "This is a very very very long sentence that will not fit in one line on a small phone screen",
    maxLines = 1,
    overflow = TextOverflow.Ellipsis
)
```

Shows: `This is a very very very long sente...`

- `maxLines = 1` → only **one** line.
- `overflow = TextOverflow.Ellipsis` → cut it and add **`...`** at the end.

Great for long titles in lists (song names, email subjects…).

### Ready-made styles from the theme ⭐ (the recommended way)

Your app's theme has a set of **ready-made text styles**. Using them makes your app **look consistent and professional**.

```kotlin
Text("Big headline", style = MaterialTheme.typography.headlineLarge)
Text("Title", style = MaterialTheme.typography.titleMedium)
Text("Normal body text", style = MaterialTheme.typography.bodyLarge)
Text("Small label", style = MaterialTheme.typography.labelSmall)
```

The styles, from biggest to smallest:

| Group | Sizes | Use for |
|---|---|---|
| `display` | Large, Medium, Small | Very big numbers or words (like a clock) |
| `headline` | Large, Medium, Small | Screen headings |
| `title` | Large, Medium, Small | Titles of cards, sections |
| `body` | Large, Medium, Small | Normal reading text |
| `label` | Large, Medium, Small | Small text on buttons, tags |

> 💡 **Tip:** Use `style = MaterialTheme.typography...` first. Only add `fontSize`, `color`, etc. if you need something special. We learn more about themes in **Chapter 7**.

### Text from `strings.xml` (best practice)

Remember `strings.xml` from Chapter 1? Let's use it!

1. Open `res/values/strings.xml`.
2. Add a new line:

```xml
<resources>
    <string name="app_name">My First App</string>
    <string name="welcome">Welcome to my app!</string>
</resources>
```

3. In Kotlin:

```kotlin
Text(text = stringResource(R.string.welcome))
```

| Piece | Meaning |
|---|---|
| `stringResource(...)` | "Get a text from `strings.xml`." (import `androidx.compose.ui.res.stringResource`) |
| `R` | A class Android **makes for you automatically**. It has an ID for every resource (text, image, color…). |
| `R.string.welcome` | "The ID of the text named `welcome`." |

**Why?** So you can **translate** your app later without changing code. 🌍

> 💡 In this book we often write text directly in code to keep examples short. In real apps, put user-visible text in `strings.xml`.

---

## 5.5 Sizes: `dp` and `sp` 📏

Phones have different screens. Some have **many tiny dots** (pixels), some have **fewer, bigger dots**.

If you said "*make this button 100 pixels wide*", it would look **big** on one phone and **tiny** on another. 😕

So Android uses special units:

| Unit | Name | Use it for | Example |
|---|---|---|---|
| **`dp`** | Density-independent pixel | **Everything except text**: sizes, spacing, borders | `16.dp`, `100.dp` |
| **`sp`** | Scale-independent pixel | **Text size only** | `16.sp`, `24.sp` |

- **`dp`** looks about the **same physical size** on every phone. ✅
- **`sp`** is like `dp`, **but** it also grows when the user makes the font bigger in phone settings (for people who can't see small text well). ♿

> ⚠️ **Rule:** Text size → `sp`. Everything else → `dp`. Never use `sp` for a box size, and never use `dp` for text.

**Imports:**

```kotlin
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
```

**Common sizes designers use:**

| Size | Used for |
|---|---|
| `4.dp`, `8.dp` | Small spaces |
| `16.dp` | Normal padding around the screen edge |
| `24.dp`, `32.dp` | Bigger spaces between sections |
| `48.dp` | Minimum size of something you can tap 👆 |
| `14.sp` – `16.sp` | Normal text |
| `20.sp` – `32.sp` | Titles |

---

## 5.6 Colors 🎨

### Ready-made colors

```kotlin
Color.Red
Color.Green
Color.Blue
Color.Black
Color.White
Color.Gray
Color.LightGray
Color.DarkGray
Color.Yellow
Color.Cyan
Color.Magenta
Color.Transparent   // invisible
```

### Your own color with a hex code

```kotlin
val skyBlue = Color(0xFF87CEEB)
val sunsetOrange = Color(0xFFFF7043)
```

What does `0xFF87CEEB` mean?

```
0x  FF  87  CE  EB
│   │   │   │   └── Blue  amount (00 to FF)
│   │   │   └────── Green amount
│   │   └────────── Red   amount
│   └────────────── Alpha = how see-through (FF = solid, 00 = invisible)
└────────────────── "This is a hex number"
```

- Hex numbers use `0–9` and `A–F`. `00` is the smallest, `FF` is the biggest (255).
- You can find colors on websites like **https://m3.material.io** or by searching "**color picker**" on Google. Copy the 6-letter code (like `87CEEB`) and put `0xFF` in front.

### See-through colors

```kotlin
Color.Black.copy(alpha = 0.5f)   // black, half see-through
```

`alpha` goes from `0f` (invisible) to `1f` (solid).

### Theme colors ⭐ (the recommended way)

```kotlin
Text("Hi", color = MaterialTheme.colorScheme.primary)
```

Your theme has a **set of colors that go well together**, and they **change automatically in dark mode** 🌙. Use them first:

| Theme color | Use for |
|---|---|
| `MaterialTheme.colorScheme.primary` | Main brand color: important buttons, highlights |
| `MaterialTheme.colorScheme.secondary` | Second accent color |
| `MaterialTheme.colorScheme.background` | Screen background |
| `MaterialTheme.colorScheme.surface` | Cards, sheets |
| `MaterialTheme.colorScheme.onPrimary` | Text/icons **on top of** primary |
| `MaterialTheme.colorScheme.onSurface` | Text/icons on top of surface |
| `MaterialTheme.colorScheme.error` | Errors ❌ |

> 💡 `onSomething` means "the color to use **on top of** something". Example: white text **on** a blue button → `onPrimary`.

---

## 5.7 The `Image` Composable — Showing Pictures 🖼️

### Step 1: Add a picture to your project

1. Find a picture on your computer (a `.png` or `.jpg`). For example, a photo of yourself or a pet.
2. **Rename** the file. Android has strict rules for file names:

| Rule | ✅ Good | ❌ Bad |
|---|---|---|
| Only **small** letters | `my_cat.png` | `My_Cat.png` |
| Only letters, numbers, `_` | `cat_photo_2.png` | `cat-photo.png`, `cat photo.png` |
| Must **start with a letter** | `photo1.png` | `1photo.png` |

3. In Android Studio, in the **Project** window, find **`res → drawable`**.
4. **Copy** your file (Ctrl + C) in File Explorer.
5. **Right-click** the `drawable` folder → **Paste** (Ctrl + V).
6. A box may ask about the folder: choose **`drawable`** (not `drawable-v24`). Click **OK**.

Now you will see `my_cat.png` inside `drawable`. 🎉

**Another way:** **View → Tool Windows → Resource Manager** → click **+** → **Import Drawables**.

### Step 2: Show it

```kotlin
@Composable
fun PracticeScreen(modifier: Modifier = Modifier) {
    Image(
        painter = painterResource(id = R.drawable.my_cat),
        contentDescription = "My cat sitting on a sofa",
        modifier = modifier
    )
}
```

Imports:

```kotlin
import androidx.compose.foundation.Image
import androidx.compose.ui.res.painterResource
```

### Every bit explained

| Input | Meaning |
|---|---|
| `painter = painterResource(id = R.drawable.my_cat)` | "Load the picture named `my_cat` from the `drawable` folder." Notice: **no** `.png` at the end. |
| `contentDescription = "..."` | A **description** for people who **can't see** the screen. Phone apps called **screen readers** (like TalkBack) read this aloud. ♿ |
| `modifier = modifier` | Size, shape, etc. |

> 💡 **About `contentDescription`:** Always describe **important** pictures. If a picture is **only decoration** (like a background pattern), write `contentDescription = null` — the screen reader will skip it.

### No picture? Use one that is already there

Every new project has a built-in picture: the Android robot from the app icon.

```kotlin
Image(
    painter = painterResource(id = R.drawable.ic_launcher_foreground),
    contentDescription = "Android robot"
)
```

### Size and shape

```kotlin
Image(
    painter = painterResource(id = R.drawable.my_cat),
    contentDescription = "My cat",
    contentScale = ContentScale.Crop,
    modifier = Modifier
        .size(150.dp)
        .clip(CircleShape)
)
```

Imports:

```kotlin
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
```

| Code | Meaning |
|---|---|
| `Modifier.size(150.dp)` | Make the image **150 × 150 dp**. |
| `.clip(CircleShape)` | **Cut** it into a **circle** ⭕. (Like a profile photo!) |
| `contentScale = ContentScale.Crop` | If the picture is not square, **fill** the space and cut off the extra edges. |

### `contentScale` options

| Option | What happens | Like… |
|---|---|---|
| `ContentScale.Fit` (default) | The whole picture fits inside. There may be **empty space**. | A photo in a frame that's too big |
| `ContentScale.Crop` | Fills **all** the space. Edges may be **cut off**. | Zooming in on a photo |
| `ContentScale.FillBounds` | Stretches to fill. Picture may look **squished**. 😬 | Pulling a rubber sheet |
| `ContentScale.Inside` | Like Fit, but never makes it **bigger** than the real size. | — |

### Other shapes

```kotlin
.clip(RoundedCornerShape(16.dp))   // rectangle with round corners ▢
.clip(CircleShape)                 // circle ⭕
.clip(RectangleShape)              // normal square corners ⬜
```

Import: `androidx.compose.foundation.shape.RoundedCornerShape`

> ℹ️ **Pictures from the internet** (like a URL) need an extra library. We learn that in **Chapter 20**.

---

## 5.8 The `Icon` Composable — Small Symbols ⭐❤️🏠

Icons are small, simple pictures: a heart, a star, a home, a search glass…
Material Design gives you **hundreds** of ready-made icons.

```kotlin
@Composable
fun PracticeScreen(modifier: Modifier = Modifier) {
    Icon(
        imageVector = Icons.Filled.Favorite,
        contentDescription = "Favorite",
        tint = Color.Red,
        modifier = modifier.size(48.dp)
    )
}
```

Imports:

```kotlin
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material3.Icon
```

### Every bit explained

| Input | Meaning |
|---|---|
| `imageVector = Icons.Filled.Favorite` | Which icon. `Filled` = solid style. `Favorite` = a heart ❤️. |
| `contentDescription` | What it means (for screen readers). |
| `tint = Color.Red` | The icon's color. |
| `modifier.size(48.dp)` | The icon's size (default is 24 dp). |

### ⚠️ If `Icons` is red and Alt + Enter doesn't help

In some newer projects, the icons library is **not included** by default. Add it:

1. Open **`build.gradle.kts (Module :app)`**.
2. In `dependencies { ... }`, add this line:

```kotlin
    implementation("androidx.compose.material:material-icons-core")
```

3. Click **Sync Now** (the yellow bar at the top).

There is no version number because the **Compose BOM** (from Chapter 1) chooses the right one.

> 💡 **Want even more icons?** Use `material-icons-extended` instead of `material-icons-core`. It has **thousands** of icons, but it makes your app bigger.

### Some useful icons in `material-icons-core`

| Code | Icon |
|---|---|
| `Icons.Filled.Home` | 🏠 Home |
| `Icons.Filled.Favorite` | ❤️ Heart |
| `Icons.Filled.Star` | ⭐ Star |
| `Icons.Filled.Search` | 🔍 Search |
| `Icons.Filled.Settings` | ⚙️ Settings |
| `Icons.Filled.Person` | 👤 Person |
| `Icons.Filled.Email` | ✉️ Email |
| `Icons.Filled.Phone` | 📞 Phone |
| `Icons.Filled.Add` | ➕ Add |
| `Icons.Filled.Delete` | 🗑️ Delete |
| `Icons.Filled.Share` | 🔗 Share |
| `Icons.Filled.LocationOn` | 📍 Location |
| `Icons.Filled.Check` | ✔️ Check |
| `Icons.Filled.Close` | ✖️ Close |
| `Icons.AutoMirrored.Filled.ArrowBack` | ⬅️ Back arrow |

### Icon styles

The same icon comes in different **styles**:

| Style | Look |
|---|---|
| `Icons.Filled.Favorite` | Solid ❤️ |
| `Icons.Outlined.FavoriteBorder` | Only the outline 🤍 |
| `Icons.Rounded.Favorite` | Rounded corners |

> 💡 `Icons.Default` is the same as `Icons.Filled`.

> ℹ️ **`AutoMirrored`?** Some icons, like arrows, should **flip** for languages written right-to-left (like Arabic). `AutoMirrored` icons do this automatically.

### `Icon` vs `Image`

| | `Icon` | `Image` |
|---|---|---|
| For | Small, one-color symbols | Photos and colorful pictures |
| Color | Can change with `tint` | Shows the real colors |
| Default size | 24 dp | Real picture size |

---

## 5.9 Modifiers — The Magic Changers ✨

A **Modifier** changes **how** a Composable looks or behaves: its size, spacing, background, border, shape, what happens when you tap it…

Almost **every** Composable has a `modifier` input.

### How to write modifiers

You start with `Modifier` (big M) and add changes with dots `.`:

```kotlin
Text(
    text = "Hello",
    modifier = Modifier
        .background(Color.Yellow)
        .padding(16.dp)
)
```

This is a **chain** — like the list chains from Chapter 3. Each `.something()` adds one more change.

> 🎉 These are **extension functions** on `Modifier` (Chapter 4)!

### The most useful modifiers

| Modifier | What it does | Example |
|---|---|---|
| `.padding(16.dp)` | Space **around** (inside the edge) | all sides 16 |
| `.padding(horizontal = 16.dp, vertical = 8.dp)` | Different space left/right and top/bottom | |
| `.padding(start = 8.dp, top = 4.dp)` | Space on chosen sides | `start`, `end`, `top`, `bottom` |
| `.size(100.dp)` | Width **and** height | 100 × 100 |
| `.size(width = 200.dp, height = 50.dp)` | Different width and height | |
| `.width(200.dp)` / `.height(50.dp)` | Only one direction | |
| `.fillMaxWidth()` | As **wide** as possible | full width |
| `.fillMaxHeight()` | As **tall** as possible | |
| `.fillMaxSize()` | Fill **everything** | |
| `.fillMaxWidth(0.5f)` | **Half** the width | 50% |
| `.background(Color.Yellow)` | Background color | |
| `.background(Color.Yellow, RoundedCornerShape(8.dp))` | Background with round corners | |
| `.border(2.dp, Color.Black)` | A line around it | |
| `.border(2.dp, Color.Black, CircleShape)` | A round line | |
| `.clip(CircleShape)` | Cut into a shape | |
| `.clickable { ... }` | Do something when **tapped** 👆 | |
| `.alpha(0.5f)` | Half see-through | |
| `.rotate(45f)` | Turn by 45 degrees | |

> 💡 **`start` and `end` instead of `left` and `right`:** In right-to-left languages (Arabic, Hebrew), `start` is on the **right**. Using `start`/`end` makes your app work for everyone. 🌍

### ⚠️ ORDER MATTERS! (very important)

Modifiers are applied **one after another, in order**. Changing the order changes the result!

**Example A: background, then padding**

```kotlin
Text(
    text = "Hello",
    modifier = Modifier
        .background(Color.Yellow)
        .padding(16.dp)
)
```

```
┌──────────────────────┐
│ 🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨 │
│ 🟨🟨  Hello   🟨🟨 │  ← yellow is BIG: includes the padding
│ 🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨 │
└──────────────────────┘
```

**Example B: padding, then background**

```kotlin
Text(
    text = "Hello",
    modifier = Modifier
        .padding(16.dp)
        .background(Color.Yellow)
)
```

```
┌──────────────────────┐
│                      │
│      🟨Hello🟨        │  ← yellow is SMALL: only behind the text
│                      │
└──────────────────────┘
```

**How to think about it:** Read the chain **from top to bottom**, like wrapping a gift 🎁:

- **A:** "Paint it yellow. **Then** add space inside." → the space is yellow too.
- **B:** "Add space around. **Then** paint yellow." → only the inner part is yellow.

### Padding **outside** and **inside** a border

```kotlin
Text(
    text = "Framed",
    modifier = Modifier
        .padding(16.dp)                                         // 1. space OUTSIDE the border
        .border(2.dp, Color.Blue, RoundedCornerShape(8.dp))     // 2. the border
        .padding(12.dp)                                         // 3. space INSIDE the border
)
```

One modifier used **twice** — once for outside space, once for inside space. This is a very common trick!

### `clickable` — make anything tappable 👆

```kotlin
Text(
    text = "Tap me!",
    modifier = Modifier
        .clickable { Log.d("Practice", "The text was tapped!") }
        .padding(16.dp)
)
```

- `.clickable { ... }` → a **lambda** that runs when the user taps.
- Open **Logcat** (bottom of Android Studio), search `Practice`, and tap the text in the app. You'll see your message!
- Put `clickable` **before** `padding`, so the padding area is tappable too (a bigger, easier target 👍).

### Why every Composable should take a `modifier` input

Look at our `PracticeScreen`:

```kotlin
@Composable
fun PracticeScreen(modifier: Modifier = Modifier) {
    Text(text = "...", modifier = modifier)
}
```

- The **caller** decides the outside things (padding, size, position).
- The Composable passes it to its **outermost** block.
- `= Modifier` → if the caller gives nothing, use an empty modifier (no changes).

This makes your Composables **reusable** — like a LEGO block that can fit in many places. 🧱

> ⚠️ Use the `modifier` input **only once**, on the **outermost** block. Inside, use a fresh `Modifier`.

---

## 5.10 Buttons — Making Things Happen 🔘

### A simple button

```kotlin
@Composable
fun PracticeScreen(modifier: Modifier = Modifier) {
    Button(
        onClick = { Log.d("Practice", "Button clicked!") },
        modifier = modifier
    ) {
        Text("Click me")
    }
}
```

Imports:

```kotlin
import android.util.Log
import androidx.compose.material3.Button
```

### Every bit explained

| Piece | Meaning |
|---|---|
| `Button(` | A ready-made Material button. |
| `onClick = { ... }` | A **lambda**: what to do when tapped. |
| `modifier = modifier` | Size and spacing. |
| `) { Text("Click me") }` | A **trailing lambda** (Chapter 3!): what to show **inside** the button. |

**Why is the text inside `{ }` and not just `text = "..."`?**
Because a button can hold **anything**: text, an icon, or both! Very flexible.

### A button with an icon and text

```kotlin
Button(onClick = { /* do something */ }) {
    Icon(
        imageVector = Icons.Filled.Favorite,
        contentDescription = null,
        modifier = Modifier.size(18.dp)
    )
    Spacer(modifier = Modifier.width(8.dp))
    Text("Like")
}
```

- Inside a `Button`, items are placed **side by side** (in a row) automatically.
- `Spacer(...)` → an **empty space**. Here, 8 dp between the icon and the text.
- `contentDescription = null` for the icon, because the text "Like" already explains it.

> 💡 `/* do something */` is a **comment** (Chapter 1). The lambda is empty for now, so nothing happens on tap.

### Different button styles

Material 3 has **5 kinds** of buttons. Use them to show **how important** an action is.

```kotlin
Column {
    Button(onClick = { }) { Text("Filled") }
    FilledTonalButton(onClick = { }) { Text("Tonal") }
    ElevatedButton(onClick = { }) { Text("Elevated") }
    OutlinedButton(onClick = { }) { Text("Outlined") }
    TextButton(onClick = { }) { Text("Text") }
}
```

| Button | Looks like | Use for | Importance |
|---|---|---|---|
| `Button` | Solid color | The **main** action: "Save", "Buy" | ⭐⭐⭐⭐⭐ |
| `FilledTonalButton` | Soft color | Important, but not the main one | ⭐⭐⭐⭐ |
| `ElevatedButton` | With a shadow | Stands out from a busy background | ⭐⭐⭐ |
| `OutlinedButton` | Only a border | Second choice: "Cancel", "Back" | ⭐⭐ |
| `TextButton` | Only text | Small actions: "Learn more", "Skip" | ⭐ |

> 💡 **Design tip:** Use only **one** `Button` (filled) per screen area, for the **most important** action.

### `IconButton` — a tappable icon

```kotlin
IconButton(onClick = { Log.d("Practice", "Settings tapped") }) {
    Icon(Icons.Filled.Settings, contentDescription = "Settings")
}
```

Used in top bars: back arrow ⬅️, search 🔍, menu ⋮…

### Disabled button

```kotlin
Button(onClick = { }, enabled = false) {
    Text("Can't tap me")
}
```

`enabled = false` → the button is **grey** and **does nothing** when tapped. Useful when, for example, a form is not filled in yet.

### Custom button colors

```kotlin
Button(
    onClick = { },
    colors = ButtonDefaults.buttonColors(
        containerColor = Color(0xFF4CAF50),   // background: green
        contentColor = Color.White            // text/icon: white
    )
) {
    Text("Green button")
}
```

### Show a pop-up message: `Toast` 🍞

Logcat is for **you** (the developer). To show a short message to the **user**, use a **Toast** — a small message that pops up at the bottom of the screen and disappears.

```kotlin
@Composable
fun PracticeScreen(modifier: Modifier = Modifier) {
    val context = LocalContext.current

    Button(
        onClick = {
            Toast.makeText(context, "Hello from the button! 👋", Toast.LENGTH_SHORT).show()
        },
        modifier = modifier
    ) {
        Text("Show a Toast")
    }
}
```

Imports:

```kotlin
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext
```

### Every bit explained

| Piece | Meaning |
|---|---|
| `val context = LocalContext.current` | Get the **context**. The context is like the app's "**ID badge**" 🪪 — many Android features need it to know which app is asking. |
| `Toast.makeText(...)` | Make a Toast message. |
| `context` | Who is showing it. |
| `"Hello..."` | The message. |
| `Toast.LENGTH_SHORT` | Show for a **short** time (~2 seconds). `LENGTH_LONG` = ~3.5 seconds. |
| `.show()` | Actually **show** it! (Easy to forget! 😅) |

> ℹ️ The Preview can't show Toasts. **Run the app** to see them.

### "But how do I change the text on the screen when I click?" 🤔

Great question! For that, the screen must **remember** a changing value. This is called **state**, and it is the **most important idea in Compose**. We learn it fully in **Chapter 8**. For now, we use **Logcat** and **Toast** to see that buttons work.

---

## 5.11 Using the Preview Like a Pro 👀

The Preview lets you see your design **without running** the app. ⚡

### Preview options

```kotlin
@Preview(
    name = "My preview",
    showBackground = true,
    backgroundColor = 0xFFF0F0F0,
    showSystemUi = true,
    widthDp = 320,
    heightDp = 200
)
@Composable
fun PracticeScreenPreview() {
    MyFirstAppTheme {
        PracticeScreen()
    }
}
```

| Option | Meaning |
|---|---|
| `name = "..."` | A label above the preview. |
| `showBackground = true` | Draw a background (otherwise it's see-through). |
| `backgroundColor = 0xFF...` | Background color. |
| `showSystemUi = true` | Show a **full phone** with the status bar. 📱 |
| `widthDp`, `heightDp` | Size of the preview area. |
| `fontScale = 1.5f` | Pretend the user chose **bigger** fonts. |
| `uiMode = Configuration.UI_MODE_NIGHT_YES` | Show in **dark mode** 🌙. |

### Many previews at once

You can stack `@Preview` labels:

```kotlin
@Preview(name = "Light", showBackground = true)
@Preview(
    name = "Dark",
    showBackground = true,
    uiMode = Configuration.UI_MODE_NIGHT_YES
)
@Preview(name = "Big font", showBackground = true, fontScale = 1.5f)
@Composable
fun PracticeScreenPreview() {
    MyFirstAppTheme {
        PracticeScreen()
    }
}
```

Import: `android.content.res.Configuration`

Now you see **three** previews side by side: light, dark, and big font. Great for checking that your design works for everyone! ✅

### Interactive mode and run on device

At the top of each preview, there are small buttons:

| Button | What it does |
|---|---|
| 👆 **Interactive Mode** (Start Interactive Mode) | You can **click** things in the preview, like a mini app. |
| 📱 **Run Preview** (Deploy Preview) | Runs **just this one Composable** on your phone or emulator. |

### Preview tips

- Previews are **only for you**. Users never see them.
- A preview function must have **no inputs** (or only inputs with default values).
- Always wrap it in your **theme** (`MyFirstAppTheme { }`) so colors and fonts look right.
- If the preview says "**out of date**", click **Build & Refresh** (or press **Ctrl + Shift + F5**).

---

## 5.12 Build It: A Profile Card 🪪

Let's put **everything** together and build a nice profile card screen!

```
┌─────────────────────────────┐
│                             │
│          ┌──────┐           │
│          │ 🤖   │  ← round photo with a border
│          └──────┘           │
│                             │
│        Roy Paul             │  ← name (big)
│   Android Developer 📱      │  ← job (colored)
│                             │
│   ✉️ roy@example.com        │  ← icon + text
│   📍 Mumbai, India          │  ← icon + text
│                             │
│   [ ❤️ Follow ]  [ Message ] │  ← two buttons
│                             │
└─────────────────────────────┘
```

### The full code

Replace **everything** in `MainActivity.kt` with this:

```kotlin
package com.example.myfirstapp

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.myfirstapp.ui.theme.MyFirstAppTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyFirstAppTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    ProfileCard(
                        name = "Roy Paul",
                        job = "Android Developer 📱",
                        email = "roy@example.com",
                        city = "Mumbai, India",
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }
}

@Composable
fun ProfileCard(
    name: String,
    job: String,
    email: String,
    city: String,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(32.dp))

        // 1. The round profile picture
        Image(
            painter = painterResource(id = R.drawable.ic_launcher_foreground),
            contentDescription = "Profile picture of $name",
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .size(140.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primaryContainer)
                .border(4.dp, MaterialTheme.colorScheme.primary, CircleShape)
        )

        Spacer(modifier = Modifier.height(16.dp))

        // 2. Name and job
        Text(
            text = name,
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold
        )
        Text(
            text = job,
            style = MaterialTheme.typography.titleMedium,
            color = MaterialTheme.colorScheme.primary
        )

        Spacer(modifier = Modifier.height(24.dp))

        // 3. Contact info
        InfoLine(icon = Icons.Filled.Email, text = email)
        Spacer(modifier = Modifier.height(8.dp))
        InfoLine(icon = Icons.Filled.LocationOn, text = city)

        Spacer(modifier = Modifier.height(32.dp))

        // 4. Buttons
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Button(
                onClick = {
                    Toast.makeText(context, "You followed $name! 🎉", Toast.LENGTH_SHORT).show()
                }
            ) {
                Icon(
                    imageVector = Icons.Filled.Favorite,
                    contentDescription = null,
                    modifier = Modifier.size(18.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text("Follow")
            }

            OutlinedButton(
                onClick = {
                    Toast.makeText(context, "Messages are coming soon ✉️", Toast.LENGTH_SHORT).show()
                }
            ) {
                Text("Message")
            }
        }
    }
}

@Composable
fun InfoLine(icon: ImageVector, text: String, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.secondary,
            modifier = Modifier.size(20.dp)
        )
        Spacer(modifier = Modifier.width(8.dp))
        Text(
            text = text,
            style = MaterialTheme.typography.bodyLarge
        )
    }
}

@Preview(showBackground = true, showSystemUi = true)
@Composable
fun ProfileCardPreview() {
    MyFirstAppTheme {
        ProfileCard(
            name = "Roy Paul",
            job = "Android Developer 📱",
            email = "roy@example.com",
            city = "Mumbai, India"
        )
    }
}
```

> ⚠️ Remember: keep **your own** `package` line and theme import if they are different.
> ⚠️ If `Icons` is red, add the icons library (see section 5.8).

### Every part explained

#### Part 1: `onCreate` — showing the card

```kotlin
ProfileCard(
    name = "Roy Paul",
    job = "Android Developer 📱",
    ...
    modifier = Modifier.padding(innerPadding)
)
```

- We **call** our own Composable `ProfileCard` with **named arguments**.
- We give it the safe space `innerPadding` from the Scaffold (Chapter 1).

#### Part 2: `ProfileCard` — the inputs

```kotlin
@Composable
fun ProfileCard(
    name: String,
    job: String,
    email: String,
    city: String,
    modifier: Modifier = Modifier
) {
```

- The card gets **all its data from outside**. It doesn't "know" who Roy is.
- This makes it **reusable**: you can show **anyone's** card by giving different inputs! ♻️
- When a function has many inputs, put **each one on its own line**. Easier to read.

#### Part 3: The `Column`

```kotlin
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
```

| Code | Meaning |
|---|---|
| `Column(...)` | Put the children **one under another**. |
| `modifier = modifier` | Start from the modifier we got from outside (with the safe space). Note: small `m` — the **input**, not a new `Modifier`. |
| `.fillMaxSize()` | Use the whole screen. |
| `.padding(24.dp)` | Keep 24 dp away from the edges. |
| `horizontalAlignment = Alignment.CenterHorizontally` | Put all children in the **center** (left–right). |

#### Part 4: The round picture

```kotlin
        Image(
            painter = painterResource(id = R.drawable.ic_launcher_foreground),
            contentDescription = "Profile picture of $name",
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .size(140.dp)
                .clip(CircleShape)
                .background(MaterialTheme.colorScheme.primaryContainer)
                .border(4.dp, MaterialTheme.colorScheme.primary, CircleShape)
        )
```

| Code | Meaning |
|---|---|
| `R.drawable.ic_launcher_foreground` | The Android robot picture. 🤖 **Change it** to your own photo (`R.drawable.my_photo`) if you added one! |
| `"Profile picture of $name"` | A good description, with a String template. |
| `.size(140.dp)` | 140 × 140. |
| `.clip(CircleShape)` | Cut into a circle. |
| `.background(...primaryContainer)` | A soft color behind the picture (the robot picture is see-through). |
| `.border(4.dp, ...primary, CircleShape)` | A **round** colored ring around it. |

#### Part 5: Name and job

```kotlin
        Text(
            text = name,
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold
        )
```

- Uses a **theme style** and makes it **bold**.
- The job text uses `color = MaterialTheme.colorScheme.primary` — the app's main color.

#### Part 6: `Spacer` — empty space

```kotlin
        Spacer(modifier = Modifier.height(16.dp))
```

- An **invisible** block that only takes space.
- In a `Column`, use `.height(...)`. In a `Row`, use `.width(...)`.

#### Part 7: `InfoLine` — our own small, reusable block

```kotlin
@Composable
fun InfoLine(icon: ImageVector, text: String, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(...)
        Spacer(modifier = Modifier.width(8.dp))
        Text(...)
    }
}
```

| Code | Meaning |
|---|---|
| `icon: ImageVector` | An input that is an **icon** (the type of `Icons.Filled.Email`). |
| `Row(...)` | Put children **side by side** (left to right). |
| `verticalAlignment = Alignment.CenterVertically` | Line up the icon and text in the **middle** (top–bottom). |

We used `InfoLine` **twice** — once for email, once for city. **Write once, use many times.** That is the power of Composables! 🧱

> 💡 **When to make a new Composable?** When you **repeat** the same design, or when a part of the screen gets **long**. Small, named blocks make code easy to read.

#### Part 8: The buttons

```kotlin
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Button(onClick = { Toast... }) { ... }
            OutlinedButton(onClick = { Toast... }) { ... }
        }
```

| Code | Meaning |
|---|---|
| `Row(...)` | Buttons side by side. |
| `horizontalArrangement = Arrangement.spacedBy(12.dp)` | Put **12 dp of space between** the children. (No need for a Spacer!) |
| `Button` | The **main** action (Follow) — filled. |
| `OutlinedButton` | The **second** action (Message) — outlined. |
| `Toast.makeText(...)` | Shows a pop-up. Uses `context` from the top of the function. |

#### Part 9: The preview

```kotlin
@Preview(showBackground = true, showSystemUi = true)
```

- `showSystemUi = true` → see the card on a **full phone** frame.
- We give **example data** to the card. You can make another preview with **different** data to test long names, etc.

### Run it! ▶️

Click **Run**. You will see your profile card. Tap **Follow** → a Toast says "*You followed Roy Paul! 🎉*". 🎉

### Make it yours ✏️

1. Change the name, job, email, and city to **your** information.
2. Add your own photo to `drawable` and use it instead of `ic_launcher_foreground`.
3. Add a third `InfoLine` with `Icons.Filled.Phone` and a phone number.
4. Change the border color to `Color(0xFFFF9800)` (orange).

---

## 5.13 Common Mistakes and Fixes 🔧

| Mistake | Error / Problem | Fix |
|---|---|---|
| Calling a Composable from a normal function | *@Composable invocations can only happen from the context of a @Composable function* | Add `@Composable` to the calling function, or call it from `setContent`. |
| Many items without `Column` / `Row` | All items are drawn **on top of each other** 😵 | Wrap them in `Column { }` or `Row { }`. |
| `sp` for sizes, `dp` for text | Works, but looks wrong when the user changes font size | Text → `sp`. Everything else → `dp`. |
| Image file name with BIG letters, spaces, or `-` | *'My-Photo' is not a valid file-based resource name* | Rename: `my_photo.png`. |
| Writing `.png` in code | `R.drawable.my_photo.png` → error | Just `R.drawable.my_photo`. |
| `Unresolved reference: R` | The project didn't build yet, or a resource file has an error | **Build → Rebuild Project**. Check file names in `res`. |
| `Icons` is red | The icons library is missing | Add `material-icons-core` (section 5.8) and **Sync**. |
| Forgot `.show()` on Toast | Nothing appears | `Toast.makeText(...).show()` |
| Wrong modifier order | Background or click area is the wrong size | Remember: order matters. Read the chain top to bottom. |
| Used `modifier` (input) on many children | Strange spacing everywhere | Use the input `modifier` only on the **outermost** block. Use `Modifier` inside. |
| Preview is blank or old | — | Click **Build & Refresh**. Check that the preview function has no required inputs. |

---

## 5.14 Summary — What You Learned 🎓

✅ **Compose is declarative:** you describe the screen; Compose redraws it when data changes.

✅ **Composable rules:** `@Composable`, BIG first letter, returns nothing, called from other Composables, takes a `modifier`.

✅ **`Text`:** `fontSize`, `color`, `fontWeight`, `textAlign`, `maxLines`, `overflow`, and theme `style`s. Text from `strings.xml` with `stringResource`.

✅ **Units:** `dp` for sizes, `sp` for text.

✅ **Colors:** `Color.Red`, `Color(0xFF...)`, and **theme colors** `MaterialTheme.colorScheme...`.

✅ **`Image`:** add pictures to `res/drawable`, `painterResource`, `contentDescription`, `contentScale`, `clip(CircleShape)`.

✅ **`Icon`:** `Icons.Filled.Favorite`, `tint`, size.

✅ **Modifiers:** `padding`, `size`, `fillMaxWidth`, `background`, `border`, `clip`, `clickable`. **Order matters!**

✅ **Buttons:** `Button`, `FilledTonalButton`, `ElevatedButton`, `OutlinedButton`, `TextButton`, `IconButton`. `onClick`, `enabled`, `colors`. **Toast** messages.

✅ **Preview:** `showSystemUi`, dark mode, font scale, many previews, interactive mode.

✅ You built a **Profile Card** with your own reusable `InfoLine` Composable.

---

## 5.15 Practice Time 🏋️

Do these in Android Studio. Use the **Preview** to check your work. Answers are below!

**Task 1 — Styled text:**
Make a Composable `StyledTitle()` that shows `"Kotlin is fun!"` in size `28.sp`, bold, italic, and the color `Color(0xFF6A1B9A)` (purple).

**Task 2 — Modifier order:**
Make a `Text("Badge")` that has:
- a green background with round corners (`RoundedCornerShape(50)`),
- white text,
- 12 dp of space **inside** (left/right) and 4 dp (top/bottom).

**Task 3 — Icon row:**
Make a Composable `RatingStars()` that shows **5 yellow stars** in a row. (Hint: use `Row` and a `repeat(5) { ... }` loop!)

**Task 4 — Buttons:**
Make a Composable with a `Column` holding a filled `Button` "Save" and a `TextButton` "Cancel". When tapped, each shows a Toast: `"Saved!"` / `"Cancelled"`.

**Task 5 — Reusable Composable:**
Make a Composable `Tag(text: String, color: Color)` that shows the text with a colored rounded background. Show three tags: `"Kotlin"` (blue), `"Android"` (green), `"Compose"` (purple), side by side with 8 dp between them.

**Task 6 — Dark mode preview:**
Add a second preview to your `ProfileCard` that shows it in **dark mode**.

---

### Answers

**Task 1:**

```kotlin
@Composable
fun StyledTitle(modifier: Modifier = Modifier) {
    Text(
        text = "Kotlin is fun!",
        fontSize = 28.sp,
        fontWeight = FontWeight.Bold,
        fontStyle = FontStyle.Italic,
        color = Color(0xFF6A1B9A),
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun StyledTitlePreview() {
    MyFirstAppTheme {
        StyledTitle()
    }
}
```

**Task 2:**

```kotlin
@Composable
fun PillBadge(modifier: Modifier = Modifier) {
    Text(
        text = "Badge",
        color = Color.White,
        modifier = modifier
            .background(Color(0xFF4CAF50), RoundedCornerShape(50))
            .padding(horizontal = 12.dp, vertical = 4.dp)
    )
}
```

`background` comes **first**, so the green covers the padding too. `RoundedCornerShape(50)` means 50% round corners → a "pill" shape 💊.

**Task 3:**

```kotlin
@Composable
fun RatingStars(modifier: Modifier = Modifier) {
    Row(modifier = modifier) {
        repeat(5) {
            Icon(
                imageVector = Icons.Filled.Star,
                contentDescription = null,
                tint = Color(0xFFFFC107)
            )
        }
    }
}
```

Imports: `androidx.compose.material.icons.filled.Star`.
Yes — you can use **loops** inside Composables! `repeat(5)` draws 5 icons.

> ♿ For screen readers, it would be even better to add a `contentDescription = "5 stars"` to the `Row` (we learn how in a later chapter). For now, `null` on each star is OK.

**Task 4:**

```kotlin
@Composable
fun SaveCancel(modifier: Modifier = Modifier) {
    val context = LocalContext.current

    Column(modifier = modifier) {
        Button(onClick = {
            Toast.makeText(context, "Saved!", Toast.LENGTH_SHORT).show()
        }) {
            Text("Save")
        }
        TextButton(onClick = {
            Toast.makeText(context, "Cancelled", Toast.LENGTH_SHORT).show()
        }) {
            Text("Cancel")
        }
    }
}
```

Import: `androidx.compose.material3.TextButton`.

**Task 5:**

```kotlin
@Composable
fun Tag(text: String, color: Color, modifier: Modifier = Modifier) {
    Text(
        text = text,
        color = Color.White,
        style = MaterialTheme.typography.labelLarge,
        modifier = modifier
            .background(color, RoundedCornerShape(8.dp))
            .padding(horizontal = 10.dp, vertical = 4.dp)
    )
}

@Composable
fun TagList(modifier: Modifier = Modifier) {
    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Tag("Kotlin", Color(0xFF1E88E5))
        Tag("Android", Color(0xFF43A047))
        Tag("Compose", Color(0xFF8E24AA))
    }
}

@Preview(showBackground = true)
@Composable
fun TagListPreview() {
    MyFirstAppTheme {
        TagList(modifier = Modifier.padding(16.dp))
    }
}
```

**Task 6:**

```kotlin
@Preview(
    name = "Dark",
    showBackground = true,
    showSystemUi = true,
    uiMode = Configuration.UI_MODE_NIGHT_YES
)
@Composable
fun ProfileCardDarkPreview() {
    MyFirstAppTheme {
        ProfileCard(
            name = "Roy Paul",
            job = "Android Developer 📱",
            email = "roy@example.com",
            city = "Mumbai, India"
        )
    }
}
```

Import: `android.content.res.Configuration`.

> ℹ️ In the dark preview, the background may still look light. That's because `showBackground` draws a fixed background. In **Chapter 7** we learn `Surface`, which uses the theme's background color properly in dark mode.

---

## 5.16 What Is Next?

In **Chapter 6: Layouts — Putting Things in Place**, you will master:

- **`Column`** — things one under another
- **`Row`** — things side by side
- **`Box`** — things **on top of** each other (like a photo with a label on it)
- **Alignment** and **Arrangement** — center, start, end, space between…
- **`weight`** — share space fairly (like 1/3 and 2/3)
- **`Spacer`**, sizes, and scrolling
- How to look at **any app screen** and break it into Rows, Columns, and Boxes 🔍

**Great job finishing Chapter 5! 🎉 You built your first real-looking screen!**
