# Chapter 7: Making It Beautiful — Material 3 Themes, Colors, Fonts, and Cards

> **What you will learn in this chapter**
>
> 1. What Material Design 3 is
> 2. Your three theme files — `Color.kt`, `Theme.kt`, `Type.kt` — every line explained
> 3. Color **roles**: `primary`, `onPrimary`, `primaryContainer`… what each one is for
> 4. Making your **own color scheme** (by hand and with the Material Theme Builder)
> 5. **Dynamic color** — colors from the user's wallpaper 🎨
> 6. **Dark mode** done right 🌙
> 7. `Surface` — the "paper" of your app
> 8. `Card`, `OutlinedCard`, `ElevatedCard`
> 9. **Typography** — your app's text styles and **custom fonts**
> 10. **Shapes** — round corners for the whole app
> 11. Building a themed **Plant Shop** screen 🌿
>
> **Time needed:** about 4 hours.
>
> **Where to practice:** Android Studio, in your **MyFirstApp** project.

---

## 7.1 What Is Material Design 3? 🎨

**Material Design** is a **design system** made by Google. It is a big book of rules and ready-made parts that say:

- Which **colors** go well together
- How big **text** should be
- How **buttons**, **cards**, and **menus** should look and behave
- How much **space** to leave
- How things should **move** (animations)

**Material 3** (also called **Material You**) is the **newest** version. It is used in Android 12 and newer, and in Google's own apps (Gmail, Photos, Settings…).

**Real-life example:** A **school uniform** rule book 👔. It says which colors, which shirt, which shoes. Every student looks neat and **matching**, but each school can choose **its own colors**.

In the same way:
- Material 3 gives you **the rules and the parts**.
- **Your theme** chooses **your app's colors, fonts, and shapes**.

> 💡 **Why use it?** Your app will look **professional**, **modern**, and **familiar** to users — without being a designer! ✨

The official website: **https://m3.material.io** (lots of pictures and examples).

---

## 7.2 Where Is the Theme? 📁

When you made your project in Chapter 1, Android Studio made **three theme files** for you:

```
app
 └── kotlin+java
      └── com.example.myfirstapp
           └── ui.theme
                ├── Color.kt    ← the colors 🎨
                ├── Theme.kt    ← puts everything together 🧩
                └── Type.kt     ← the text styles 🔤
```

And in `MainActivity.kt`, you have been using the theme all along:

```kotlin
setContent {
    MyFirstAppTheme {          // ← this is your theme!
        Scaffold(...) { ... }
    }
}
```

Everything **inside** `MyFirstAppTheme { }` uses your app's colors, fonts, and shapes.

Let's open each file and understand **every line**.

> ℹ️ The exact color names and numbers in your files may be a little different, depending on your Android Studio version. The ideas are the same.

---

## 7.3 `Color.kt` — The Paint Box 🎨

Open `ui/theme/Color.kt`. You will see something like:

```kotlin
package com.example.myfirstapp.ui.theme

import androidx.compose.ui.graphics.Color

val Purple80 = Color(0xFFD0BCFF)
val PurpleGrey80 = Color(0xFFCCC2DC)
val Pink80 = Color(0xFFEFB8C8)

val Purple40 = Color(0xFF6650a4)
val PurpleGrey40 = Color(0xFF625b71)
val Pink40 = Color(0xFF7D5260)
```

### Every bit explained

| Line | Meaning |
|---|---|
| `package ...ui.theme` | This file lives in the `ui.theme` folder. |
| `import ...Color` | We use the `Color` class. |
| `val Purple80 = Color(0xFFD0BCFF)` | A **color** with a name. `0xFF` + `D0BCFF` (hex, from Chapter 5). |

**What do `80` and `40` mean?**
They describe **how light** the color is:

- **`40`** → a **darker** color → used in **light mode** (dark color on a light background = easy to read).
- **`80`** → a **lighter** color → used in **dark mode** (light color on a dark background = easy to read).

This file is just a **paint box** — a list of named colors. It doesn't decide **where** each color goes. That happens in `Theme.kt`. 👇

---

## 7.4 `Theme.kt` — Putting It All Together 🧩

Open `ui/theme/Theme.kt`. You will see something like:

```kotlin
package com.example.myfirstapp.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext

private val DarkColorScheme = darkColorScheme(
    primary = Purple80,
    secondary = PurpleGrey80,
    tertiary = Pink80
)

private val LightColorScheme = lightColorScheme(
    primary = Purple40,
    secondary = PurpleGrey40,
    tertiary = Pink40
)

@Composable
fun MyFirstAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    // Dynamic color is available on Android 12+
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }

        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
```

This looks big, but you already know **every Kotlin idea** in it! Let's go slowly. 🐢

### Part 1: The two color schemes

```kotlin
private val DarkColorScheme = darkColorScheme(
    primary = Purple80,
    secondary = PurpleGrey80,
    tertiary = Pink80
)
```

| Piece | Meaning |
|---|---|
| `private` | Only this file can use it (Chapter 3). |
| `val DarkColorScheme` | A box holding the **set of colors for dark mode**. |
| `darkColorScheme(...)` | A Material function that makes a **full** dark color set. |
| `primary = Purple80` | "The **main** color is `Purple80`." (Named arguments!) |
| `secondary`, `tertiary` | The second and third accent colors. |

**What about all the other colors** (background, surface, error…)?
`darkColorScheme(...)` has **default values** for all of them (Chapter 2: default values!). You only change the ones you want.

`LightColorScheme` is the same idea, for **light mode**.

### Part 2: The theme function

```kotlin
@Composable
fun MyFirstAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
```

It's a **Composable function** with **3 inputs**:

| Input | Meaning |
|---|---|
| `darkTheme: Boolean = isSystemInDarkTheme()` | Use dark mode? By default: **ask the phone** — "*Is the phone in dark mode?*" |
| `dynamicColor: Boolean = true` | Use colors from the **wallpaper**? By default: **yes**. (See 7.7.) |
| `content: @Composable () -> Unit` | A **lambda** (Chapter 3) — the **screen** to show inside the theme. The `@Composable` label means this lambda can draw UI. |

> 🎉 **Now you understand `MyFirstAppTheme { ... }`!** The `{ ... }` is a **trailing lambda** that becomes the `content` input!

### Part 3: Choosing the colors

```kotlin
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }

        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }
```

A `when` without a value (Chapter 2) — it checks from top to bottom:

| Check | Meaning | Result |
|---|---|---|
| `dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S` | "Dynamic color is ON **and** the phone has Android 12 (API 31, code name **S**) or newer?" | Use **wallpaper** colors (dark or light). |
| `darkTheme` | "Is it dark mode?" | Use **our** `DarkColorScheme`. |
| `else` | Otherwise… | Use **our** `LightColorScheme`. |

| Code | Meaning |
|---|---|
| `Build.VERSION.SDK_INT` | The **API level** of the phone the app is running on (Chapter 1). |
| `Build.VERSION_CODES.S` | The number **31** (Android 12). Android versions used to have dessert names; `S` is "Snow Cone" 🍧. |
| `dynamicDarkColorScheme(context)` | "Make a dark color set **from the wallpaper**." It needs the `context` to ask the phone. |

### Part 4: Giving everything to `MaterialTheme`

```kotlin
    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
```

- `MaterialTheme` is the **real** theme from the Material library.
- We give it our **colors**, our **text styles** (`Typography`, from `Type.kt`), and the **screen** (`content`).
- Now everything inside can use `MaterialTheme.colorScheme.primary`, `MaterialTheme.typography.bodyLarge`, etc. ✅

**Real-life example:** `MyFirstAppTheme` is like a **costume shop** 👗. It looks at the weather (dark mode?) and the user's taste (wallpaper?), picks the right outfit, and **dresses** the whole screen.

### 🤔 "Why is my app not purple?"

If your phone or emulator has **Android 12 or newer**, `dynamicColor = true` means your app uses **colors from the wallpaper** — not the purple from `Color.kt`! This surprises many beginners.

To always use **your own** colors, set it to `false` (see 7.7).

---

## 7.5 `Type.kt` — The Text Styles 🔤

Open `ui/theme/Type.kt`:

```kotlin
package com.example.myfirstapp.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

// Set of Material typography styles to start with
val Typography = Typography(
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    )
    /* Other default text styles to override
    titleLarge = TextStyle(...),
    labelSmall = TextStyle(...)
    */
)
```

| Piece | Meaning |
|---|---|
| `val Typography = Typography(...)` | A box named `Typography` holding a **set of text styles**. |
| `bodyLarge = TextStyle(...)` | **Change** the `bodyLarge` style. |
| `TextStyle(...)` | One text style: font, weight, size, line height, letter spacing. |
| `/* ... */` | A comment with ideas — other styles you **could** change. |

All the other styles (`headlineLarge`, `titleMedium`, `labelSmall`, … — the table from Chapter 5) use Material's **default** values.

We'll change these and add a **custom font** in section 7.11.

---

## 7.6 Color Roles — Which Color Goes Where? 🧭

A Material 3 color scheme is not just "a few colors". It's a set of **roles**. Each role has a **job**.

### The main idea: pairs

Most colors come in **pairs**:

| Color | Its partner | Rule |
|---|---|---|
| `primary` | `onPrimary` | Text/icons **on top of** `primary` use `onPrimary`. |
| `primaryContainer` | `onPrimaryContainer` | Text/icons on top of `primaryContainer` use `onPrimaryContainer`. |
| `surface` | `onSurface` | Text/icons on top of `surface` use `onSurface`. |

**`on` = "on top of"**. The pair is chosen so the text is **always easy to read**. 👓

### The full list of roles

| Role | Job | Example |
|---|---|---|
| **`primary`** | Main brand color. The **most important** things. | Main button, active tab, switch "on" |
| `onPrimary` | Text/icons on `primary` | Text on the main button |
| **`primaryContainer`** | A **softer** version of primary, for bigger areas | A highlighted card, a selected chip |
| `onPrimaryContainer` | Text/icons on `primaryContainer` | |
| **`secondary`** | Second accent, **less** important | Filter chips |
| `onSecondary`, `secondaryContainer`, `onSecondaryContainer` | Same pattern as primary | Tonal button (`FilledTonalButton`) |
| **`tertiary`** | Third accent, for **contrast** / balance | A special badge |
| `onTertiary`, `tertiaryContainer`, `onTertiaryContainer` | Same pattern | |
| **`error`** | Errors and warnings ❌ | Error text, "Delete" button |
| `onError`, `errorContainer`, `onErrorContainer` | Same pattern | |
| **`background`** | The screen behind everything | |
| `onBackground` | Text on the background | |
| **`surface`** | "Paper": cards, sheets, menus, top bars | |
| `onSurface` | Main text on surfaces | Most of your text! |
| **`surfaceVariant`** | A slightly different surface | Text field background |
| `onSurfaceVariant` | **Softer** text, icons | Subtitles, hints, grey icons |
| `surfaceContainerLowest` … `surfaceContainerHighest` | 5 surface tones, from lightest to strongest | Card backgrounds, navigation bars |
| **`outline`** | Borders | Outlined button, text field border |
| `outlineVariant` | Soft borders, dividers | `HorizontalDivider` |
| `inverseSurface`, `inverseOnSurface`, `inversePrimary` | Opposite colors | Snackbar (a dark bar in light mode) |

> 😮 **That's a lot!** Don't try to remember all of them. In practice, you'll mostly use:
> `primary`, `onPrimary`, `primaryContainer`, `onPrimaryContainer`, `surface`, `onSurface`, `onSurfaceVariant`, `error`, `outline`.

### See all your theme colors 👀

Paste this **helper** into `MainActivity.kt` and look at its preview. It shows your real colors:

```kotlin
@Composable
fun ColorSwatch(name: String, color: Color, onColor: Color) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .background(color)
            .padding(12.dp)
    ) {
        Text(text = name, color = onColor)
    }
}

@Composable
fun ColorRolesPreviewContent() {
    val c = MaterialTheme.colorScheme
    Column {
        ColorSwatch("primary", c.primary, c.onPrimary)
        ColorSwatch("primaryContainer", c.primaryContainer, c.onPrimaryContainer)
        ColorSwatch("secondary", c.secondary, c.onSecondary)
        ColorSwatch("secondaryContainer", c.secondaryContainer, c.onSecondaryContainer)
        ColorSwatch("tertiary", c.tertiary, c.onTertiary)
        ColorSwatch("tertiaryContainer", c.tertiaryContainer, c.onTertiaryContainer)
        ColorSwatch("error", c.error, c.onError)
        ColorSwatch("surface", c.surface, c.onSurface)
        ColorSwatch("surfaceVariant", c.surfaceVariant, c.onSurfaceVariant)
    }
}

@Preview(name = "Light", widthDp = 300)
@Preview(name = "Dark", widthDp = 300, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun ColorRolesPreview() {
    MyFirstAppTheme(dynamicColor = false) {
        ColorRolesPreviewContent()
    }
}
```

| Code | Meaning |
|---|---|
| `val c = MaterialTheme.colorScheme` | A **short name** so we don't type `MaterialTheme.colorScheme` many times. |
| `MyFirstAppTheme(dynamicColor = false)` | Use **our** colors, not the wallpaper's. |
| Two `@Preview`s | See light **and** dark side by side. 🌞🌙 |

---

## 7.7 Dynamic Color — Colors From the Wallpaper 🖼️

On **Android 12+**, the phone picks colors from the user's **wallpaper**, and apps can use them. If the wallpaper is a beach 🏖️, apps become sandy and blue. If it's a forest 🌲, apps become green.

This is **dynamic color**.

### Should I use it?

| Use dynamic color ✅ | Don't use it ❌ |
|---|---|
| Tools and utility apps (notes, calculator, settings) | Apps with a **brand** color (a bank, a shop, a game) |
| You want the app to feel **personal** | You want the **same** look for every user |

### Turning it off — for the whole app

**Option A:** In `Theme.kt`, change the default:

```kotlin
    dynamicColor: Boolean = false,
```

**Option B:** In `MainActivity.kt`, pass it when you use the theme:

```kotlin
setContent {
    MyFirstAppTheme(dynamicColor = false) {
        ...
    }
}
```

> 💡 In this book we'll use **Option A** in the project below, so **our** colors always show — easier for learning.

### How to test dynamic color

1. On the emulator or your phone (Android 12+), **long-press** the home screen.
2. Tap **Wallpaper & style**.
3. Choose a different wallpaper or color.
4. Open your app (with `dynamicColor = true`). The colors changed! 🎨

---

## 7.8 Dark Mode Done Right 🌙

### How to switch the phone to dark mode

- **Emulator / phone:** swipe down from the top twice → tap **Dark theme** in Quick Settings.
- Or: **Settings → Display → Dark theme**.

Your app follows automatically, because of `darkTheme: Boolean = isSystemInDarkTheme()`. ✨

### The golden rules of dark mode

**Rule 1: Don't hard-code black and white for text and backgrounds.** ❌

```kotlin
// ❌ BAD: black text on a dark background in dark mode = invisible!
Text("Hello", color = Color.Black)

// ✅ GOOD: changes automatically
Text("Hello", color = MaterialTheme.colorScheme.onSurface)
```

**Rule 2: Even better — don't set a color at all.** Put your content on a `Surface` (next section). It gives the **right** text color automatically. ✅

**Rule 3: Use theme colors for backgrounds.**

```kotlin
// ❌ BAD
Modifier.background(Color.White)

// ✅ GOOD
Modifier.background(MaterialTheme.colorScheme.surface)
```

**Rule 4: Always check your screens in a dark preview.**

```kotlin
@Preview(name = "Light")
@Preview(name = "Dark", uiMode = Configuration.UI_MODE_NIGHT_YES)
```

> 💡 **When is a fixed color OK?** For things that should look the **same** in both modes: a brand logo, a red "LIVE" badge, emoji, photos.

---

## 7.9 `Surface` — The Paper of Your App 📄

### What is a `Surface`?

A **`Surface`** is a piece of "**paper**" in your app. It does three things:

1. Paints a **background color** (by default: `surface`).
2. Sets the **right text/icon color** for everything inside (by default: `onSurface`). ✨
3. Can have a **shape**, **border**, **shadow**, and be **clickable**.

```kotlin
Surface(
    color = MaterialTheme.colorScheme.primaryContainer,
    shape = RoundedCornerShape(16.dp),
    modifier = Modifier.padding(16.dp)
) {
    Text(
        text = "I am on a surface!",
        modifier = Modifier.padding(16.dp)
    )
}
```

Notice: we **didn't** give the `Text` a color. The `Surface` saw `color = primaryContainer` and **automatically** gave its children `onPrimaryContainer`. In dark mode, both change together. 🪄

### Surface inputs

| Input | Meaning |
|---|---|
| `color` | Background color (default `MaterialTheme.colorScheme.surface`) |
| `contentColor` | Text/icon color inside (default: the matching `on` color) |
| `shape` | `RoundedCornerShape(16.dp)`, `CircleShape`, … |
| `border` | `BorderStroke(1.dp, MaterialTheme.colorScheme.outline)` |
| `shadowElevation` | A **shadow** below it (like paper lifted off the table) |
| `tonalElevation` | Makes the color a little **tinted** with primary, instead of a shadow |
| `onClick` | Makes the whole surface **tappable** |

### Fixing the dark preview problem from Chapter 5 🌙

In Chapter 5, the dark preview still had a **light** background. That's because `@Preview(showBackground = true)` draws a **fixed** background.

**The fix:** wrap your screen in a `Surface` in the preview:

```kotlin
@Preview(name = "Dark", uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun MyScreenDarkPreview() {
    MyFirstAppTheme {
        Surface {
            MyScreen()
        }
    }
}
```

Now the background is the **theme's** surface color — dark in dark mode. ✅

> 💡 In the real app, `Scaffold` (from Chapter 1) already works like a Surface for the whole screen. That's why the running app looks right.

---

## 7.10 Cards 🃏

A **Card** is a Surface made for showing **one piece of content**: a product, a post, a recipe, a contact…

Material 3 has **three** card styles:

```kotlin
Column(
    modifier = Modifier.padding(16.dp),
    verticalArrangement = Arrangement.spacedBy(16.dp)
) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Text("Filled card", modifier = Modifier.padding(16.dp))
    }

    ElevatedCard(modifier = Modifier.fillMaxWidth()) {
        Text("Elevated card", modifier = Modifier.padding(16.dp))
    }

    OutlinedCard(modifier = Modifier.fillMaxWidth()) {
        Text("Outlined card", modifier = Modifier.padding(16.dp))
    }
}
```

| Card | Looks like | Use when |
|---|---|---|
| `Card` | Soft **filled** color, no shadow | Most cases — a calm look |
| `ElevatedCard` | Has a **shadow**, looks lifted | It must **stand out** from the background |
| `OutlinedCard` | A thin **border**, no fill | Lots of cards together, a clean look |

### Inside a card: add a `Column` with padding

A Card puts its children **one under another** (its inside works like a `Column`), but it adds **no padding**, so text would touch the edges. The usual way is to add your own `Column` with padding:

```kotlin
Card(modifier = Modifier.fillMaxWidth()) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text("Title", style = MaterialTheme.typography.titleMedium)
        Text("Some description here.", style = MaterialTheme.typography.bodyMedium)
    }
}
```

### Card colors

```kotlin
Card(
    colors = CardDefaults.cardColors(
        containerColor = MaterialTheme.colorScheme.tertiaryContainer
    )
) {
    Text("A tertiary card", modifier = Modifier.padding(16.dp))
}
```

- `CardDefaults.cardColors(...)` → change the card's colors.
- The text color changes **automatically** to match (`onTertiaryContainer`). ✨

### A tappable card

```kotlin
val context = LocalContext.current

ElevatedCard(
    onClick = {
        Toast.makeText(context, "Card tapped!", Toast.LENGTH_SHORT).show()
    },
    modifier = Modifier.fillMaxWidth()
) {
    Text("Tap me", modifier = Modifier.padding(16.dp))
}
```

Cards with `onClick` show a nice **ripple** (a wave of color 🌊) when tapped. Better than `Modifier.clickable` on a card, because it also handles the rounded corners correctly.

### Card shapes and shadow

```kotlin
ElevatedCard(
    shape = RoundedCornerShape(24.dp),
    elevation = CardDefaults.elevatedCardElevation(defaultElevation = 8.dp)
) { ... }
```

### A real card: photo on top, text below

```kotlin
@Composable
fun ArticleCard(title: String, summary: String, modifier: Modifier = Modifier) {
    ElevatedCard(modifier = modifier.fillMaxWidth()) {
        Image(
            painter = painterResource(R.drawable.ic_launcher_foreground),
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .fillMaxWidth()
                .height(140.dp)
                .background(MaterialTheme.colorScheme.secondaryContainer)
        )
        Column(modifier = Modifier.padding(16.dp)) {
            Text(title, style = MaterialTheme.typography.titleLarge)
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = summary,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}
```

- The image **touches the edges** of the card (no padding), and the card's **rounded corners cut it** automatically. ✂️
- The text part has its **own** padding.

---

## 7.11 Typography and Custom Fonts 🔤

### Changing the type scale

In `Type.kt`, you can change **any** of the 15 styles. Example: make titles bolder and headlines bigger:

```kotlin
val Typography = Typography(
    headlineMedium = TextStyle(
        fontWeight = FontWeight.Bold,
        fontSize = 30.sp,
        lineHeight = 36.sp
    ),
    titleLarge = TextStyle(
        fontWeight = FontWeight.SemiBold,
        fontSize = 22.sp,
        lineHeight = 28.sp
    ),
    bodyLarge = TextStyle(
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    )
)
```

Now **every** `Text(style = MaterialTheme.typography.titleLarge)` in the whole app changes. Change once, update everywhere! 🔁

| TextStyle input | Meaning |
|---|---|
| `fontFamily` | Which font |
| `fontWeight` | Thickness: `Light`, `Normal`, `Medium`, `SemiBold`, `Bold` |
| `fontSize` | Size (in `sp`) |
| `lineHeight` | Height of each line (space between lines) |
| `letterSpacing` | Space between letters |

### Adding a custom font (step by step) 🖋️

Let's use a free Google Font, for example **Poppins** or **Nunito**.

**Step 1: Download the font**

1. Go to **https://fonts.google.com**
2. Search for **Nunito**.
3. Click **Get font** → **Download all**.
4. Unzip the file. Inside the `static` folder, find:
   - `Nunito-Regular.ttf`
   - `Nunito-Bold.ttf`

**Step 2: Make a `font` folder**

1. In Android Studio's Project window, **right-click `res`**.
2. Click **New → Android Resource Directory**.
3. **Resource type:** choose **font**. Click **OK**.
4. Now you have `res/font/`.

**Step 3: Rename and copy the files**

Remember the **file name rules** from Chapter 5 (small letters, `_`, no `-`):

| Old name | New name |
|---|---|
| `Nunito-Regular.ttf` | `nunito_regular.ttf` |
| `Nunito-Bold.ttf` | `nunito_bold.ttf` |

Copy them into `res/font/`.

**Step 4: Make a FontFamily in `Type.kt`**

```kotlin
import androidx.compose.ui.text.font.Font
import com.example.myfirstapp.R

val Nunito = FontFamily(
    Font(R.font.nunito_regular, FontWeight.Normal),
    Font(R.font.nunito_bold, FontWeight.Bold)
)
```

| Code | Meaning |
|---|---|
| `FontFamily(...)` | A **family** — one font in different weights. |
| `Font(R.font.nunito_regular, FontWeight.Normal)` | "Use this file for **normal** weight." |
| `Font(R.font.nunito_bold, FontWeight.Bold)` | "Use this file for **bold**." |
| `import com.example.myfirstapp.R` | `Type.kt` is in a different folder, so we import `R`. |

**Step 5: Use it in the Typography**

```kotlin
val Typography = Typography(
    titleLarge = TextStyle(
        fontFamily = Nunito,
        fontWeight = FontWeight.Bold,
        fontSize = 22.sp,
        lineHeight = 28.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = Nunito,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    )
)
```

### Use the font for ALL styles (a shortcut) ⭐

Changing 15 styles by hand is a lot of work. Here's a trick using `copy` (Chapter 3!):

```kotlin
private val defaultTypography = Typography()

val Typography = Typography(
    displayLarge = defaultTypography.displayLarge.copy(fontFamily = Nunito),
    displayMedium = defaultTypography.displayMedium.copy(fontFamily = Nunito),
    displaySmall = defaultTypography.displaySmall.copy(fontFamily = Nunito),
    headlineLarge = defaultTypography.headlineLarge.copy(fontFamily = Nunito),
    headlineMedium = defaultTypography.headlineMedium.copy(fontFamily = Nunito),
    headlineSmall = defaultTypography.headlineSmall.copy(fontFamily = Nunito),
    titleLarge = defaultTypography.titleLarge.copy(fontFamily = Nunito),
    titleMedium = defaultTypography.titleMedium.copy(fontFamily = Nunito),
    titleSmall = defaultTypography.titleSmall.copy(fontFamily = Nunito),
    bodyLarge = defaultTypography.bodyLarge.copy(fontFamily = Nunito),
    bodyMedium = defaultTypography.bodyMedium.copy(fontFamily = Nunito),
    bodySmall = defaultTypography.bodySmall.copy(fontFamily = Nunito),
    labelLarge = defaultTypography.labelLarge.copy(fontFamily = Nunito),
    labelMedium = defaultTypography.labelMedium.copy(fontFamily = Nunito),
    labelSmall = defaultTypography.labelSmall.copy(fontFamily = Nunito)
)
```

- `Typography()` with **no inputs** → all Material **default** styles.
- `.copy(fontFamily = Nunito)` → "the same style, but with **our** font."

> ℹ️ **Another way:** Google also offers **downloadable fonts** (the library `ui-text-google-fonts`), which download the font when the app runs instead of putting the file in your app. Putting the `.ttf` in `res/font` (what we did) is simpler and works offline. 👍

---

## 7.12 Shapes 🔷

Material 3 has **5 shape sizes**. Components use them automatically:

| Shape | Default corner | Used by |
|---|---|---|
| `extraSmall` | 4 dp | Text fields, menus |
| `small` | 8 dp | Chips, Snackbars |
| `medium` | 12 dp | **Cards** |
| `large` | 16 dp | Navigation drawers, floating buttons |
| `extraLarge` | 28 dp | Dialogs, bottom sheets |

### Change the shapes for the whole app

Add this to `Theme.kt` (above the theme function):

```kotlin
val AppShapes = Shapes(
    small = RoundedCornerShape(12.dp),
    medium = RoundedCornerShape(20.dp),
    large = RoundedCornerShape(28.dp)
)
```

And give it to `MaterialTheme`:

```kotlin
    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        shapes = AppShapes,
        content = content
    )
```

Now **all cards** in your app have 20 dp corners — rounder and friendlier. 😊

### Use theme shapes in your own code

```kotlin
Modifier.background(MaterialTheme.colorScheme.primaryContainer, MaterialTheme.shapes.medium)
```

Use `MaterialTheme.shapes.medium` instead of `RoundedCornerShape(12.dp)`, so your own boxes **match** the rest of the app.

---

## 7.13 Making Your Own Color Scheme 🎨

### Way 1: Material Theme Builder ⭐ (easiest and best)

1. Go to **https://material-foundation.github.io/material-theme-builder/**
2. On the left, under **Core colors**, click **Primary** and pick your main color (for example, a green 🌿).
3. The tool makes a **full** light and dark scheme — all the roles — that go well together and are **easy to read**.
4. Click **Export** (top right) → **Jetpack Compose (Theme.kt)**.
5. You get a zip with `Color.kt` and `Theme.kt`.
6. Copy the **colors** from its `Color.kt` into your `Color.kt`, and the **schemes** from its `Theme.kt` into your `Theme.kt`.

> ⚠️ The exported file uses its own theme function name (like `AppTheme`). Keep **your** function name `MyFirstAppTheme`, and only copy the color parts.

### Way 2: By hand (to understand it)

We will do this in the project below: write the main roles ourselves for a green **Plant Shop** theme.

---

## 7.14 Build It: A Plant Shop Screen 🌿

We'll make a custom **green theme**, turn off dynamic color, set rounder shapes, and build a screen with a `Surface` banner and `ElevatedCard`s.

```
┌──────────────────────────────────┐
│ Hello, Roy 👋                    │
│ Find your new green friend       │
│                                  │
│ ╭──────────────────────────────╮ │  ← Surface (primaryContainer)
│ │ 🌱 Spring Sale!               │ │
│ │ 20% off all succulents       │ │
│ │                  [Shop now]  │ │
│ ╰──────────────────────────────╯ │
│                                  │
│ Popular plants                   │
│ ╭──────────────────────────────╮ │  ← ElevatedCard (tappable)
│ │ 🪴  Monstera         $25     │ │
│ │     Easy care · Indoor        │ │
│ ╰──────────────────────────────╯ │
│ ╭──────────────────────────────╮ │
│ │ 🌵  Cactus           $12     │ │
│ ╰──────────────────────────────╯ │
│ ...                              │
│ ┌──────────────────────────────┐ │  ← OutlinedCard
│ │ 💡 Tip: Water less in winter │ │
│ └──────────────────────────────┘ │
└──────────────────────────────────┘
```

### Step 1: `Color.kt` — our green paint box

Replace **everything** in `ui/theme/Color.kt` (keep your own `package` line):

```kotlin
package com.example.myfirstapp.ui.theme

import androidx.compose.ui.graphics.Color

// ----- Light mode -----
val GreenPrimaryLight = Color(0xFF386A20)
val GreenOnPrimaryLight = Color(0xFFFFFFFF)
val GreenPrimaryContainerLight = Color(0xFFB8F397)
val GreenOnPrimaryContainerLight = Color(0xFF042100)

val GreenSecondaryLight = Color(0xFF55624C)
val GreenOnSecondaryLight = Color(0xFFFFFFFF)
val GreenSecondaryContainerLight = Color(0xFFD9E7CB)
val GreenOnSecondaryContainerLight = Color(0xFF131F0D)

val GreenTertiaryLight = Color(0xFF386666)
val GreenOnTertiaryLight = Color(0xFFFFFFFF)
val GreenTertiaryContainerLight = Color(0xFFBBEBEB)
val GreenOnTertiaryContainerLight = Color(0xFF002020)

val GreenBackgroundLight = Color(0xFFFDFDF6)
val GreenOnBackgroundLight = Color(0xFF1A1C18)
val GreenSurfaceLight = Color(0xFFFDFDF6)
val GreenOnSurfaceLight = Color(0xFF1A1C18)
val GreenSurfaceVariantLight = Color(0xFFDFE4D7)
val GreenOnSurfaceVariantLight = Color(0xFF43483F)

// ----- Dark mode -----
val GreenPrimaryDark = Color(0xFF9DD67D)
val GreenOnPrimaryDark = Color(0xFF0B3900)
val GreenPrimaryContainerDark = Color(0xFF205107)
val GreenOnPrimaryContainerDark = Color(0xFFB8F397)

val GreenSecondaryDark = Color(0xFFBDCBB0)
val GreenOnSecondaryDark = Color(0xFF283420)
val GreenSecondaryContainerDark = Color(0xFF3E4A36)
val GreenOnSecondaryContainerDark = Color(0xFFD9E7CB)

val GreenTertiaryDark = Color(0xFFA0CFCF)
val GreenOnTertiaryDark = Color(0xFF003737)
val GreenTertiaryContainerDark = Color(0xFF1E4E4E)
val GreenOnTertiaryContainerDark = Color(0xFFBBEBEB)

val GreenBackgroundDark = Color(0xFF1A1C18)
val GreenOnBackgroundDark = Color(0xFFE3E3DC)
val GreenSurfaceDark = Color(0xFF1A1C18)
val GreenOnSurfaceDark = Color(0xFFE3E3DC)
val GreenSurfaceVariantDark = Color(0xFF43483F)
val GreenOnSurfaceVariantDark = Color(0xFFC3C8BC)
```

👀 Notice the pattern:
- **Light** mode: `primary` is **dark** green (`386A20`), `primaryContainer` is **light** green.
- **Dark** mode: the **opposite** — `primary` is **light** green, `primaryContainer` is **dark** green.
- Every `on...` color is chosen to be **easy to read** on its partner.

### Step 2: `Theme.kt` — the green theme

Replace **everything** in `ui/theme/Theme.kt` (keep your own `package` line):

```kotlin
package com.example.myfirstapp.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Shapes
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp

private val LightColorScheme = lightColorScheme(
    primary = GreenPrimaryLight,
    onPrimary = GreenOnPrimaryLight,
    primaryContainer = GreenPrimaryContainerLight,
    onPrimaryContainer = GreenOnPrimaryContainerLight,
    secondary = GreenSecondaryLight,
    onSecondary = GreenOnSecondaryLight,
    secondaryContainer = GreenSecondaryContainerLight,
    onSecondaryContainer = GreenOnSecondaryContainerLight,
    tertiary = GreenTertiaryLight,
    onTertiary = GreenOnTertiaryLight,
    tertiaryContainer = GreenTertiaryContainerLight,
    onTertiaryContainer = GreenOnTertiaryContainerLight,
    background = GreenBackgroundLight,
    onBackground = GreenOnBackgroundLight,
    surface = GreenSurfaceLight,
    onSurface = GreenOnSurfaceLight,
    surfaceVariant = GreenSurfaceVariantLight,
    onSurfaceVariant = GreenOnSurfaceVariantLight
)

private val DarkColorScheme = darkColorScheme(
    primary = GreenPrimaryDark,
    onPrimary = GreenOnPrimaryDark,
    primaryContainer = GreenPrimaryContainerDark,
    onPrimaryContainer = GreenOnPrimaryContainerDark,
    secondary = GreenSecondaryDark,
    onSecondary = GreenOnSecondaryDark,
    secondaryContainer = GreenSecondaryContainerDark,
    onSecondaryContainer = GreenOnSecondaryContainerDark,
    tertiary = GreenTertiaryDark,
    onTertiary = GreenOnTertiaryDark,
    tertiaryContainer = GreenTertiaryContainerDark,
    onTertiaryContainer = GreenOnTertiaryContainerDark,
    background = GreenBackgroundDark,
    onBackground = GreenOnBackgroundDark,
    surface = GreenSurfaceDark,
    onSurface = GreenOnSurfaceDark,
    surfaceVariant = GreenSurfaceVariantDark,
    onSurfaceVariant = GreenOnSurfaceVariantDark
)

val AppShapes = Shapes(
    small = RoundedCornerShape(12.dp),
    medium = RoundedCornerShape(20.dp),
    large = RoundedCornerShape(28.dp)
)

@Composable
fun MyFirstAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false,   // ← OFF: always use our green colors
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }

        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        shapes = AppShapes,
        content = content
    )
}
```

**What changed** from the original `Theme.kt`:

| Change | Why |
|---|---|
| Both schemes now set **18 roles** (not just 3) | Full control over our green look. |
| `dynamicColor: Boolean = false` | Always use **our** colors, not the wallpaper's. |
| New `AppShapes` | Rounder corners for the whole app. |
| `shapes = AppShapes` in `MaterialTheme` | Give the shapes to the theme. |

> 💡 If you added the **Nunito font** in 7.11, your `Type.kt` already uses it — the Plant Shop will use it too! If not, it just uses the normal font. Both are fine.

### Step 3: `MainActivity.kt` — the Plant Shop screen

Replace **everything** in `MainActivity.kt` (keep your own `package` line and theme import):

```kotlin
package com.example.myfirstapp

import android.content.res.Configuration
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.myfirstapp.ui.theme.MyFirstAppTheme

// ---------- Data ----------

data class Plant(
    val name: String,
    val emoji: String,
    val price: Int,
    val tags: List<String>
)

val popularPlants = listOf(
    Plant("Monstera", "🪴", 25, listOf("Easy care", "Indoor")),
    Plant("Cactus", "🌵", 12, listOf("Little water", "Sunny")),
    Plant("Sunflower", "🌻", 8, listOf("Outdoor", "Fast growing")),
    Plant("Bonsai", "🌳", 60, listOf("Expert", "Indoor")),
    Plant("Tulip", "🌷", 10, listOf("Outdoor", "Spring"))
)

// ---------- Activity ----------

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyFirstAppTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    PlantShopScreen(
                        userName = "Roy",
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }
}

// ---------- Screen ----------

@Composable
fun PlantShopScreen(userName: String, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Greeting(userName)
        SaleBanner()
        Text(
            text = "Popular plants",
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.Bold
        )
        popularPlants.forEach { plant ->
            PlantCard(plant)
        }
        TipCard("Water your plants less in winter. They grow slower when it's cold! ❄️")
    }
}

// ---------- Parts ----------

@Composable
fun Greeting(userName: String, modifier: Modifier = Modifier) {
    Column(modifier = modifier) {
        Text(
            text = "Hello, $userName 👋",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold
        )
        Text(
            text = "Find your new green friend",
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun SaleBanner(modifier: Modifier = Modifier) {
    val context = LocalContext.current

    Surface(
        color = MaterialTheme.colorScheme.primaryContainer,
        shape = MaterialTheme.shapes.large,
        modifier = modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Text(
                text = "🌱 Spring Sale!",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = "20% off all succulents",
                style = MaterialTheme.typography.bodyLarge
            )
            Spacer(modifier = Modifier.height(12.dp))
            Button(
                onClick = {
                    Toast.makeText(context, "Opening the sale... 🛍️", Toast.LENGTH_SHORT).show()
                },
                modifier = Modifier.align(Alignment.End)
            ) {
                Text("Shop now")
            }
        }
    }
}

@Composable
fun PlantCard(plant: Plant, modifier: Modifier = Modifier) {
    val context = LocalContext.current

    ElevatedCard(
        onClick = {
            Toast.makeText(context, "${plant.name} costs \$${plant.price}", Toast.LENGTH_SHORT).show()
        },
        modifier = modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .background(
                        MaterialTheme.colorScheme.secondaryContainer,
                        MaterialTheme.shapes.medium
                    ),
                contentAlignment = Alignment.Center
            ) {
                Text(text = plant.emoji, fontSize = 30.sp)
            }

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = plant.name,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = plant.tags.joinToString(" · "),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            Text(
                text = "\$${plant.price}",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

@Composable
fun TipCard(tip: String, modifier: Modifier = Modifier) {
    OutlinedCard(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(text = "💡", fontSize = 24.sp)
            Spacer(modifier = Modifier.width(12.dp))
            Text(text = tip, style = MaterialTheme.typography.bodyMedium)
        }
    }
}

// ---------- Previews ----------

@Preview(name = "Light", showSystemUi = true)
@Preview(name = "Dark", showSystemUi = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun PlantShopPreview() {
    MyFirstAppTheme {
        Surface {
            PlantShopScreen(userName = "Roy")
        }
    }
}
```

### Every new part explained

#### The data

```kotlin
data class Plant(val name: String, val emoji: String, val price: Int, val tags: List<String>)
```

- A data class can hold a **list** inside it! `tags` is a `List<String>`.
- Later we show the tags with `plant.tags.joinToString(" · ")` → `"Easy care · Indoor"`.

#### The `SaleBanner` — a Surface

```kotlin
    Surface(
        color = MaterialTheme.colorScheme.primaryContainer,
        shape = MaterialTheme.shapes.large,
        modifier = modifier.fillMaxWidth()
    ) {
```

| Code | Meaning |
|---|---|
| `color = primaryContainer` | Soft green background. Text inside **automatically** becomes `onPrimaryContainer` — no `color` needed on the Texts! ✨ |
| `shape = MaterialTheme.shapes.large` | Our **theme's** large shape (28 dp corners). |

```kotlin
            Button(
                onClick = { ... },
                modifier = Modifier.align(Alignment.End)
            )
```

- `Modifier.align(Alignment.End)` (Chapter 6) → only the button goes to the **right**.

#### The `PlantCard` — a tappable ElevatedCard

```kotlin
    ElevatedCard(
        onClick = {
            Toast.makeText(context, "${plant.name} costs \$${plant.price}", Toast.LENGTH_SHORT).show()
        },
        modifier = modifier.fillMaxWidth()
    ) {
```

| Code | Meaning |
|---|---|
| `ElevatedCard(onClick = ...)` | A card with a shadow that can be **tapped** (with a ripple 🌊). |
| `\$${plant.price}` | `\$` → a real dollar sign. `${plant.price}` → the price. Result: `$25`. (Chapter 2: special characters.) |

```kotlin
            Box(
                modifier = Modifier
                    .size(56.dp)
                    .background(
                        MaterialTheme.colorScheme.secondaryContainer,
                        MaterialTheme.shapes.medium
                    ),
                contentAlignment = Alignment.Center
            ) {
                Text(text = plant.emoji, fontSize = 30.sp)
            }
```

- A 56 dp rounded square with a **soft color**, and the emoji in the center. 🪴
- Uses the **theme's** medium shape, so it matches the card corners.

The rest is the **chat-item pattern** from Chapter 6: picture → text with `weight(1f)` → price at the end.

#### The previews

```kotlin
@Preview(name = "Light", showSystemUi = true)
@Preview(name = "Dark", showSystemUi = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun PlantShopPreview() {
    MyFirstAppTheme {
        Surface {
            PlantShopScreen(userName = "Roy")
        }
    }
}
```

- **Two** previews: light 🌞 and dark 🌙.
- `Surface { }` gives the **right background** in both modes (the fix from 7.9).

### Run it! ▶️

1. Run the app — you see a **green** plant shop. 🌿
2. Tap a plant card → a Toast shows its price.
3. Turn on **dark mode** on the phone → the whole app switches to a dark green look. 🌙
4. Look at the **two previews** side by side in Android Studio.

### Make it yours ✏️

1. Go to the **Material Theme Builder**, pick **your favorite color**, export, and copy the colors into `Color.kt`. Your whole app changes color! 🎨
2. Change `dynamicColor` back to `true` and try different wallpapers.
3. Change `AppShapes.medium` to `RoundedCornerShape(4.dp)` — see how all the cards become **sharper**.
4. Add the **Nunito** font (7.11) and see the difference.

---

## 7.15 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| "My app isn't using my colors!" | Dynamic color is ON (Android 12+) | Set `dynamicColor = false` in `Theme.kt`. |
| `Color.Black` text | Invisible in dark mode 🌑 | Use `MaterialTheme.colorScheme.onSurface`, or no color inside a `Surface`. |
| `Modifier.background(Color.White)` | A bright white box in dark mode | Use `MaterialTheme.colorScheme.surface`. |
| Dark preview has a light background | `showBackground` uses a fixed color | Wrap the preview content in `Surface { }`. |
| Font file name `Nunito-Bold.ttf` | *'Nunito-Bold' is not a valid file-based resource name* | Rename to `nunito_bold.ttf`. |
| `Unresolved reference: R` in `Type.kt` | `R` is in a different package | `import com.example.myfirstapp.R` |
| Font file in `drawable` or `assets` | `R.font.xxx` not found | Make a `res/font` folder (resource type **font**). |
| Wrong pair (e.g. `onPrimary` text on `primaryContainer`) | Hard to read | Always match: `X` ↔ `onX`, `XContainer` ↔ `onXContainer`. |
| Card content has no space | Text touches the card edges | Add `Modifier.padding(16.dp)` to the content inside. |
| `Card` + `Modifier.clickable` | Ripple goes outside the rounded corners | Use the card's own `onClick = { }` input. |

---

## 7.16 Summary — What You Learned 🎓

✅ **Material 3** = Google's design system. Your **theme** sets your app's colors, fonts, and shapes.

✅ **Theme files:**
- `Color.kt` → named colors (a paint box)
- `Theme.kt` → light/dark **color schemes**, dynamic color, and `MaterialTheme(...)`
- `Type.kt` → `Typography` (15 text styles)

✅ **Color roles** come in pairs: `primary`/`onPrimary`, `primaryContainer`/`onPrimaryContainer`, `surface`/`onSurface`…

✅ **Dynamic color** = colors from the wallpaper (Android 12+). Turn off with `dynamicColor = false`.

✅ **Dark mode rules:** use theme colors, not `Color.Black`/`White`; check dark previews.

✅ **`Surface`** paints a background **and** sets the right content color automatically.

✅ **Cards:** `Card` (filled), `ElevatedCard` (shadow), `OutlinedCard` (border). `onClick`, `CardDefaults.cardColors`.

✅ **Typography:** change styles in `Type.kt`; add fonts in `res/font` with `FontFamily(Font(...))`.

✅ **Shapes:** `Shapes(small, medium, large)`; use `MaterialTheme.shapes.medium`.

✅ **Material Theme Builder** makes beautiful, readable color schemes for you.

✅ You built a themed, dark-mode-ready **Plant Shop** screen! 🌿

---

## 7.17 Practice Time 🏋️

**Task 1 — Read the roles:**
Without running code, answer: on a `Button` (filled), which color role is the **background**, and which is the **text**?

**Task 2 — Surface magic:**
Make a `Surface` with `color = MaterialTheme.colorScheme.errorContainer` and rounded corners, containing a `Text("Something went wrong")` with **no** color set. Check it in light and dark previews. What color is the text?

**Task 3 — Three cards:**
Make a `Column` with one `Card`, one `ElevatedCard`, and one `OutlinedCard`. Each holds a title and a one-line description. Use `spacedBy(12.dp)`.

**Task 4 — Tertiary card:**
Make a `Card` that uses `tertiaryContainer` as its background color.

**Task 5 — New theme color:**
Change the `primary` color in the **light** scheme to `Color(0xFFD84315)` (deep orange). What changes in the Plant Shop? (Look at the "Shop now" button and the prices.)

**Task 6 — Your own type style:**
In `Type.kt`, change `headlineMedium` to be `FontWeight.ExtraBold` and `32.sp`. Look at the "Hello, Roy 👋" text.

---

### Answers

**Task 1:**
Background = **`primary`**, text = **`onPrimary`**. (That's why the button text is always readable.)

**Task 2:**

```kotlin
@Composable
fun ErrorBox(modifier: Modifier = Modifier) {
    Surface(
        color = MaterialTheme.colorScheme.errorContainer,
        shape = RoundedCornerShape(12.dp),
        modifier = modifier
    ) {
        Text(
            text = "Something went wrong",
            modifier = Modifier.padding(16.dp)
        )
    }
}

@Preview(name = "Light")
@Preview(name = "Dark", uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun ErrorBoxPreview() {
    MyFirstAppTheme {
        ErrorBox(modifier = Modifier.padding(16.dp))
    }
}
```

The text is **`onErrorContainer`** — a dark red in light mode and a light pink in dark mode. The `Surface` chose it **automatically**. 🪄

**Task 3:**

```kotlin
@Composable
fun ThreeCards(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Filled", style = MaterialTheme.typography.titleMedium)
                Text("A calm, soft card.")
            }
        }
        ElevatedCard(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Elevated", style = MaterialTheme.typography.titleMedium)
                Text("This one has a shadow.")
            }
        }
        OutlinedCard(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Outlined", style = MaterialTheme.typography.titleMedium)
                Text("Clean, with a thin border.")
            }
        }
    }
}
```

**Task 4:**

```kotlin
Card(
    colors = CardDefaults.cardColors(
        containerColor = MaterialTheme.colorScheme.tertiaryContainer
    ),
    modifier = Modifier.fillMaxWidth()
) {
    Text("I am a tertiary card!", modifier = Modifier.padding(16.dp))
}
```

Import: `androidx.compose.material3.CardDefaults`.

**Task 5:**
In `Color.kt`: `val GreenPrimaryLight = Color(0xFFD84315)`.
The **"Shop now" button** and the **prices** become **orange**, because they use `primary`. Everything else stays green. This shows how **one** role change updates many places at once. 🔁
(Change it back to green after trying!)

**Task 6:**

```kotlin
val Typography = Typography(
    headlineMedium = TextStyle(
        fontWeight = FontWeight.ExtraBold,
        fontSize = 32.sp,
        lineHeight = 40.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    )
)
```

The greeting becomes **bigger and heavier**. Every other `headlineMedium` in the app changes too.

---

## 7.18 What Is Next?

Until now, our screens could **not change**. Buttons only showed Toasts. 😴

In **Chapter 8: State — Making Screens Change**, you will learn the **most important idea in Compose**:

- What **state** is
- `remember` and `mutableStateOf` — giving your screen a **memory** 🧠
- **Recomposition** — how Compose redraws the screen when state changes
- `rememberSaveable` — keeping state when the phone **rotates**
- **State hoisting** — who should own the state
- Building a **counter**, a **like button** ❤️, and a **light switch** 💡 that really work!

**Great job finishing Chapter 7! 🎉 Your apps now look professional!**
