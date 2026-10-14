# Chapter 11: Screen Frames and Pop-ups — Scaffold, Bars, Buttons, Dialogs, and Sheets

> **What you will learn in this chapter**
>
> 1. `Scaffold` — the frame of a screen, fully explained 🏗️
> 2. **Top app bars** — title, back arrow, action buttons 🔝
> 3. Top bars that **hide or shrink** when you scroll
> 4. The **⋮ "more" menu**
> 5. **Floating action buttons** (FAB) ➕
> 6. **Bottom app bars** and **navigation bars** (tabs) 🔽
> 7. **Snackbars** — short messages with an **Undo** button ↩️
> 8. **Dialogs** — "Are you sure?" pop-ups ❓
> 9. **Bottom sheets** — panels that slide up 📤
> 10. Building a **Notes app** that uses all of them 🗒️
>
> **Time needed:** about 4 to 5 hours.

---

## 11.1 `Scaffold` — The Frame of a Screen 🏗️

You've used `Scaffold` since Chapter 1:

```kotlin
Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
    MyScreen(modifier = Modifier.padding(innerPadding))
}
```

But we only used **one** of its powers. A `Scaffold` has **slots** (empty places) for the standard parts of a Material screen:

```
┌──────────────────────────────┐
│  topBar                      │  ← title, back arrow, actions
├──────────────────────────────┤
│                              │
│                              │
│  content                     │  ← your screen
│                              │
│                     ┌─────┐  │
│                     │ FAB │  │  ← floatingActionButton
│                     └─────┘  │
│ ┌──────────────────────────┐ │
│ │ snackbar                 │ │  ← snackbarHost
│ └──────────────────────────┘ │
├──────────────────────────────┤
│  bottomBar                   │  ← tabs or actions
└──────────────────────────────┘
```

```kotlin
Scaffold(
    topBar = { /* a top app bar */ },
    bottomBar = { /* a bottom bar */ },
    floatingActionButton = { /* a FAB */ },
    snackbarHost = { /* where snackbars appear */ },
    modifier = Modifier.fillMaxSize()
) { innerPadding ->
    /* your screen content */
}
```

| Slot | What goes there |
|---|---|
| `topBar` | A `TopAppBar` |
| `bottomBar` | A `NavigationBar` or `BottomAppBar` |
| `floatingActionButton` | A `FloatingActionButton` |
| `floatingActionButtonPosition` | `FabPosition.End` (default), `Center`, `Start`, `EndOverlay` |
| `snackbarHost` | A `SnackbarHost` |
| `containerColor` | Background color of the screen (default: `background`) |
| content `{ innerPadding -> }` | Your screen |

Each slot is a **lambda** (Chapter 3) — you can put **any** Composable in it, but Material has ready-made ones for each.

**Real-life example:** A **picture frame with labeled spaces** 🖼️: "*title goes here*", "*photo goes here*", "*caption goes here*". You just fill in the spaces; the frame keeps everything in the right place.

### `innerPadding` — very important! ⚠️

`innerPadding` tells your content **how much space** the bars take:

- **Top:** the status bar + the top app bar
- **Bottom:** the bottom bar + the navigation buttons of the phone

If you **forget** to use it, your content goes **under** the bars and gets hidden! 🙈

```kotlin
Scaffold(topBar = { ... }) { innerPadding ->
    LazyColumn(contentPadding = innerPadding) {      // ✅ for lazy lists
        ...
    }
}

Scaffold(topBar = { ... }) { innerPadding ->
    Column(modifier = Modifier.padding(innerPadding)) {   // ✅ for normal layouts
        ...
    }
}
```

> 💡 **For lazy lists, use `contentPadding = innerPadding`** (Chapter 10). Then the list can scroll **behind** the bars nicely, but the first and last items are never hidden. ✨

---

## 11.2 Top App Bars 🔝

### Your first top app bar

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SimpleTopBarScreen() {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("My App") }
            )
        }
    ) { innerPadding ->
        Text(
            text = "Hello!",
            modifier = Modifier.padding(innerPadding).padding(16.dp)
        )
    }
}
```

Imports:

```kotlin
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.TopAppBar
```

### About `@OptIn(ExperimentalMaterial3Api::class)` 🧪

Some Material 3 parts — like `TopAppBar`, bottom sheets, and date pickers — are still marked **experimental** ("new, may change a little in the future").

To use them, write **`@OptIn(ExperimentalMaterial3Api::class)`** above your function. It means: "*I know it's new. I want to use it anyway.*"

> 💡 Don't worry — "experimental" here does **not** mean "broken". Millions of apps use these every day. 👍

> 💡 **Tip:** Android Studio can add it for you: click the red/yellow warning and press **Alt + Enter** → **Opt in for 'ExperimentalMaterial3Api'**.

### A full top app bar: back arrow, title, actions

```kotlin
TopAppBar(
    title = { Text("Inbox") },
    navigationIcon = {
        IconButton(onClick = { /* go back */ }) {
            Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
        }
    },
    actions = {
        IconButton(onClick = { /* search */ }) {
            Icon(Icons.Filled.Search, contentDescription = "Search")
        }
        IconButton(onClick = { /* share */ }) {
            Icon(Icons.Filled.Share, contentDescription = "Share")
        }
    }
)
```

```
┌──────────────────────────────────────┐
│ ⬅️  Inbox                    🔍  🔗   │
└──────────────────────────────────────┘
```

| Input | Meaning |
|---|---|
| `title` | The screen's title. |
| `navigationIcon` | One icon at the **start**: usually **⬅️ Back** or **☰ Menu**. |
| `actions` | Icons at the **end**. It's a **`Row`**, so you can put several. |
| `colors` | Change the bar's colors (see below). |
| `scrollBehavior` | How it reacts to scrolling (see 11.3). |

Import for the back arrow: `androidx.compose.material.icons.automirrored.filled.ArrowBack`
(**AutoMirrored** = it flips for right-to-left languages like Arabic, Chapter 5.)

> 💡 **Design tip:** Show at most **2–3 action icons**. Put the rest in a **⋮ menu** (section 11.4).

### Four kinds of top app bars

| Bar | Looks like | Use for |
|---|---|---|
| `TopAppBar` | Small; title on the left | Most screens |
| `CenterAlignedTopAppBar` | Small; title in the **center** | Main/home screens |
| `MediumTopAppBar` | Taller; title on a **second line** | Important screens |
| `LargeTopAppBar` | Even taller; **big** title | Top-level screens (like Settings) |

```
TopAppBar               ⬅️ Title                  🔍
CenterAlignedTopAppBar  ☰        Title            🔍
MediumTopAppBar         ⬅️                        🔍
                        Title
LargeTopAppBar          ⬅️                        🔍

                        Title (big)
```

All four use the **same** inputs. Just change the name!

### Colored top bar

```kotlin
TopAppBar(
    title = { Text("My App") },
    colors = TopAppBarDefaults.topAppBarColors(
        containerColor = MaterialTheme.colorScheme.primaryContainer,
        titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer
    )
)
```

Import: `androidx.compose.material3.TopAppBarDefaults`

---

## 11.3 Top Bars That React to Scrolling 🎢

Modern apps make the top bar **hide**, **change color**, or **shrink** when you scroll — so there's more room for content.

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScrollingBarScreen() {
    val scrollBehavior = TopAppBarDefaults.enterAlwaysScrollBehavior()

    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            TopAppBar(
                title = { Text("Scroll me!") },
                scrollBehavior = scrollBehavior
            )
        }
    ) { innerPadding ->
        LazyColumn(contentPadding = innerPadding) {
            items(50) { i ->
                Text("Row $i", modifier = Modifier.padding(16.dp))
            }
        }
    }
}
```

Import: `androidx.compose.ui.input.nestedscroll.nestedScroll`

### Every bit explained

| Code | Meaning |
|---|---|
| `TopAppBarDefaults.enterAlwaysScrollBehavior()` | "**Hide** the bar when scrolling **down**, **show** it again as soon as scrolling **up**." |
| `scrollBehavior = scrollBehavior` | Give the behavior to the bar. |
| `Modifier.nestedScroll(scrollBehavior.nestedScrollConnection)` | ⚠️ **Don't forget!** This **connects** the list's scrolling to the bar, so the bar **knows** when you scroll. 🔌 |

**Real-life example:** The bar and the list are **two people**. `nestedScroll` is the **phone line** 📞 between them: "*Hey bar, the user is scrolling down — hide!*"

### The 3 scroll behaviors

| Behavior | What happens |
|---|---|
| `pinnedScrollBehavior()` | Bar **stays**, but changes color when content scrolls under it. |
| `enterAlwaysScrollBehavior()` | Bar **hides** on scroll down, **comes back** on scroll up. |
| `exitUntilCollapsedScrollBehavior()` | For `Medium`/`LargeTopAppBar`: the big bar **shrinks** to a small one as you scroll. ✨ |

**Try this:** Change `TopAppBar` to `LargeTopAppBar` and use `exitUntilCollapsedScrollBehavior()`. Scroll and watch the big title **shrink** smoothly — just like the Android Settings app! ⚙️

---

## 11.4 The ⋮ "More" Menu

When you have **more actions** than space, put them in a menu behind a **⋮** icon:

```kotlin
var menuOpen by remember { mutableStateOf(false) }

TopAppBar(
    title = { Text("Photos") },
    actions = {
        IconButton(onClick = { /* share */ }) {
            Icon(Icons.Filled.Share, contentDescription = "Share")
        }
        Box {
            IconButton(onClick = { menuOpen = true }) {
                Icon(Icons.Filled.MoreVert, contentDescription = "More options")
            }
            DropdownMenu(
                expanded = menuOpen,
                onDismissRequest = { menuOpen = false }
            ) {
                DropdownMenuItem(
                    text = { Text("Edit") },
                    leadingIcon = { Icon(Icons.Filled.Edit, contentDescription = null) },
                    onClick = {
                        menuOpen = false
                        /* edit */
                    }
                )
                DropdownMenuItem(
                    text = { Text("Settings") },
                    leadingIcon = { Icon(Icons.Filled.Settings, contentDescription = null) },
                    onClick = {
                        menuOpen = false
                        /* settings */
                    }
                )
                HorizontalDivider()
                DropdownMenuItem(
                    text = { Text("Delete", color = MaterialTheme.colorScheme.error) },
                    leadingIcon = {
                        Icon(Icons.Filled.Delete, contentDescription = null, tint = MaterialTheme.colorScheme.error)
                    },
                    onClick = {
                        menuOpen = false
                        /* delete */
                    }
                )
            }
        }
    }
)
```

- This is the same `DropdownMenu` from **Chapter 9**! 🎉
- `Icons.Filled.MoreVert` = the **⋮** icon ("more, vertical").
- `leadingIcon` → an icon next to each menu item.
- `HorizontalDivider()` → a line to separate **dangerous** actions (like Delete) from the others.
- The **red** color warns: "*be careful!*" ⚠️
- **Always** close the menu (`menuOpen = false`) when an item is tapped.

---

## 11.5 Floating Action Buttons (FAB) ➕

A **FAB** is a round (or rounded) button that **floats** above the content. It's for the **most important action** on the screen:

- ✉️ Gmail: **Compose** a new email
- 💬 WhatsApp: **Start** a new chat
- 📝 Notes: **Add** a new note

```kotlin
Scaffold(
    floatingActionButton = {
        FloatingActionButton(onClick = { /* add something */ }) {
            Icon(Icons.Filled.Add, contentDescription = "Add")
        }
    }
) { innerPadding -> ... }
```

### Kinds of FABs

| FAB | Looks like | Use for |
|---|---|---|
| `SmallFloatingActionButton` | Small (40 dp) | Small screens, extra actions (Chapter 10's ⬆️ button) |
| `FloatingActionButton` | Normal (56 dp) | Most cases ⭐ |
| `LargeFloatingActionButton` | Big (96 dp) | When the action is **very** important |
| `ExtendedFloatingActionButton` | Wide, with **text** | When an icon alone isn't clear enough |

### Extended FAB that shrinks when scrolling ✨

```kotlin
val listState = rememberLazyListState()
val expanded by remember { derivedStateOf { listState.firstVisibleItemIndex == 0 } }

Scaffold(
    floatingActionButton = {
        ExtendedFloatingActionButton(
            onClick = { /* compose */ },
            icon = { Icon(Icons.Filled.Edit, contentDescription = null) },
            text = { Text("Compose") },
            expanded = expanded
        )
    }
) { innerPadding ->
    LazyColumn(state = listState, contentPadding = innerPadding) { ... }
}
```

- At the **top** of the list → `[ ✏️ Compose ]` (wide, with text).
- **Scrolled down** → `[ ✏️ ]` (small, icon only). More room to read! 📖
- `derivedStateOf` → from Chapter 10. ✅

> 💡 **Rule:** Only **one** FAB per screen, for the **one** most important action.

---

## 11.6 Bottom Bars 🔽

There are **two** kinds of bottom bars, for **different** jobs:

| Bar | Job | Example |
|---|---|---|
| `NavigationBar` | Switch between the **main sections** of the app (tabs) | Instagram: 🏠 Home, 🔍 Search, ➕, 🎬 Reels, 👤 Profile |
| `BottomAppBar` | **Actions** for the current screen | A photo editor: ✂️ Crop, 🎨 Filter, 🔄 Rotate |

### `NavigationBar` — tabs at the bottom ⭐

```kotlin
@Composable
fun TabsDemo() {
    var selectedTab by rememberSaveable { mutableIntStateOf(0) }

    Scaffold(
        bottomBar = {
            NavigationBar {
                NavigationBarItem(
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 },
                    icon = { Icon(Icons.Filled.Home, contentDescription = null) },
                    label = { Text("Home") }
                )
                NavigationBarItem(
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 },
                    icon = { Icon(Icons.Filled.Favorite, contentDescription = null) },
                    label = { Text("Favorites") }
                )
                NavigationBarItem(
                    selected = selectedTab == 2,
                    onClick = { selectedTab = 2 },
                    icon = { Icon(Icons.Filled.Person, contentDescription = null) },
                    label = { Text("Profile") }
                )
            }
        }
    ) { innerPadding ->
        Box(
            modifier = Modifier.fillMaxSize().padding(innerPadding),
            contentAlignment = Alignment.Center
        ) {
            when (selectedTab) {
                0 -> Text("🏠 Home screen")
                1 -> Text("❤️ Favorites screen")
                else -> Text("👤 Profile screen")
            }
        }
    }
}
```

```
┌──────────────────────────────┐
│                              │
│        🏠 Home screen         │
│                              │
├──────────────────────────────┤
│   (🏠)       ❤️        👤     │   ← selected item has a colored "pill"
│   Home   Favorites  Profile  │
└──────────────────────────────┘
```

| Code | Meaning |
|---|---|
| `var selectedTab by rememberSaveable { mutableIntStateOf(0) }` | Which tab is chosen (0, 1, or 2). Saved on rotation. 🔄 |
| `NavigationBar { ... }` | The bar. It's a `Row` of items. |
| `NavigationBarItem(selected = ..., onClick = ...)` | One tab. The **selected** one gets a colored **pill** behind its icon. |
| `when (selectedTab) { ... }` | Show a **different screen** for each tab (Chapter 2: `when`). |

### A cleaner way: a list of tabs 🧹

Writing each item by hand repeats a lot. Use a **data class** and a **loop**:

```kotlin
data class TabItem(val label: String, val icon: ImageVector)

val tabs = listOf(
    TabItem("Home", Icons.Filled.Home),
    TabItem("Favorites", Icons.Filled.Favorite),
    TabItem("Profile", Icons.Filled.Person)
)

NavigationBar {
    tabs.forEachIndexed { index, tab ->
        NavigationBarItem(
            selected = selectedTab == index,
            onClick = { selectedTab = index },
            icon = { Icon(tab.icon, contentDescription = null) },
            label = { Text(tab.label) }
        )
    }
}
```

Adding a 4th tab is now **one line**! ✨

### A badge on a tab 🔴

```kotlin
icon = {
    BadgedBox(badge = { Badge { Text("3") } }) {
        Icon(Icons.Filled.Email, contentDescription = null)
    }
}
```

Shows a small red **"3"** on the icon — like unread messages. 📬

Imports: `androidx.compose.material3.Badge`, `androidx.compose.material3.BadgedBox`

> 💡 **Rules for `NavigationBar`:**
> - **3 to 5** tabs. (Fewer than 3? Use something else. More than 5? Too crowded.)
> - Each tab is a **main section** of the app.
> - Short labels (one word if possible).

> ℹ️ Switching tabs with `when` is fine for learning. In **Chapter 13** we learn **Navigation Compose**, the professional way to move between screens (with a back button that works!).

### `BottomAppBar` — actions at the bottom

```kotlin
Scaffold(
    bottomBar = {
        BottomAppBar(
            actions = {
                IconButton(onClick = { }) { Icon(Icons.Filled.Check, contentDescription = "Done") }
                IconButton(onClick = { }) { Icon(Icons.Filled.Edit, contentDescription = "Edit") }
                IconButton(onClick = { }) { Icon(Icons.Filled.Delete, contentDescription = "Delete") }
            },
            floatingActionButton = {
                FloatingActionButton(onClick = { }) {
                    Icon(Icons.Filled.Add, contentDescription = "Add")
                }
            }
        )
    }
) { innerPadding -> ... }
```

The FAB sits **inside** the bottom bar, on the right. Nice and compact! 👌

---

## 11.7 Snackbars — Short Messages With "Undo" ↩️

A **Snackbar** is a short message at the **bottom** of the screen. It can have **one action button**, like **Undo**.

```
┌──────────────────────────────────┐
│ Note deleted                UNDO │
└──────────────────────────────────┘
```

**Snackbar vs Toast (Chapter 5):**

| | Toast 🍞 | Snackbar 🍫 |
|---|---|---|
| Looks | Android's style | Your app's **Material** style |
| Action button | ❌ No | ✅ Yes ("Undo", "Retry"…) |
| User can swipe it away | ❌ | ✅ |
| Recommended for apps | Simple debug messages | ✅ Most user messages |

### How to show a Snackbar (4 steps)

```kotlin
@Composable
fun SnackbarDemo() {
    // 1. A "host state" — the manager of snackbars
    val snackbarHostState = remember { SnackbarHostState() }
    // 2. A coroutine scope — showSnackbar takes time (it waits for the user)
    val scope = rememberCoroutineScope()

    Scaffold(
        // 3. Tell the Scaffold where to show snackbars
        snackbarHost = { SnackbarHost(hostState = snackbarHostState) }
    ) { innerPadding ->
        Button(
            onClick = {
                // 4. Show it!
                scope.launch {
                    snackbarHostState.showSnackbar("Hello from a Snackbar! 👋")
                }
            },
            modifier = Modifier.padding(innerPadding).padding(16.dp)
        ) {
            Text("Show snackbar")
        }
    }
}
```

Imports:

```kotlin
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.runtime.rememberCoroutineScope
import kotlinx.coroutines.launch
```

| Step | Code | Meaning |
|---|---|---|
| 1 | `remember { SnackbarHostState() }` | The **manager** 🧑‍💼 that shows snackbars one at a time (in a queue). |
| 2 | `rememberCoroutineScope()` | A **worker** 👷 to run tasks that take time (Chapter 10). |
| 3 | `snackbarHost = { SnackbarHost(snackbarHostState) }` | The **place** where snackbars appear. |
| 4 | `scope.launch { snackbarHostState.showSnackbar("...") }` | **Show** a message. |

### Snackbar with an "Undo" action ⭐

```kotlin
scope.launch {
    val result = snackbarHostState.showSnackbar(
        message = "Photo deleted",
        actionLabel = "Undo",
        duration = SnackbarDuration.Short
    )
    if (result == SnackbarResult.ActionPerformed) {
        // The user tapped "Undo"! Put the photo back.
    }
}
```

Imports: `androidx.compose.material3.SnackbarDuration`, `androidx.compose.material3.SnackbarResult`

| Code | Meaning |
|---|---|
| `actionLabel = "Undo"` | Add a button with this text. |
| `duration = SnackbarDuration.Short` | How long: `Short` (~4 s), `Long` (~10 s), `Indefinite` (until tapped or dismissed). |
| `val result = showSnackbar(...)` | `showSnackbar` **waits** until the snackbar goes away, then **tells you** what happened. ⏳ |
| `SnackbarResult.ActionPerformed` | The user tapped **Undo**. |
| `SnackbarResult.Dismissed` | It disappeared (time ran out, or swiped away). |

> 💡 **This is why we need a coroutine:** `showSnackbar` **waits** for seconds. A coroutine can wait **without freezing** the app. ❄️🚫

**The "Delete + Undo" pattern** (very common!):
1. Delete the item **immediately** (the user sees it gone).
2. Show a Snackbar with **Undo**.
3. If they tap Undo → **put it back**.

This is friendlier than asking "*Are you sure?*" every time. 😊

---

## 11.8 Dialogs — "Are You Sure?" ❓

A **dialog** is a small window that appears **on top** of everything, and **blocks** the screen until the user answers.

Use dialogs for **important** decisions:
- "*Delete all notes? This can't be undone.*" 🗑️
- "*Log out?*"
- "*Discard your changes?*"

### `AlertDialog`

```kotlin
@Composable
fun DeleteAllButton(onConfirmDelete: () -> Unit) {
    var showDialog by remember { mutableStateOf(false) }

    Button(onClick = { showDialog = true }) {
        Text("Delete all")
    }

    if (showDialog) {
        AlertDialog(
            onDismissRequest = { showDialog = false },
            icon = { Icon(Icons.Filled.Warning, contentDescription = null) },
            title = { Text("Delete all notes?") },
            text = { Text("All your notes will be removed. This cannot be undone.") },
            confirmButton = {
                TextButton(onClick = {
                    showDialog = false
                    onConfirmDelete()
                }) {
                    Text("Delete")
                }
            },
            dismissButton = {
                TextButton(onClick = { showDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }
}
```

Import: `androidx.compose.material3.AlertDialog`

```
        ┌────────────────────────────────┐
        │              ⚠️                 │
        │       Delete all notes?        │
        │                                │
        │ All your notes will be removed.│
        │ This cannot be undone.         │
        │                                │
        │              Cancel   Delete   │
        └────────────────────────────────┘
```

### Every bit explained

| Code | Meaning |
|---|---|
| `var showDialog by remember { ... }` | Is the dialog **open**? A dialog is just **state**! |
| `if (showDialog) { AlertDialog(...) }` | Draw the dialog **only** when the state is `true`. |
| `onDismissRequest = { showDialog = false }` | The user tapped **outside** or pressed **Back** → close it. |
| `icon`, `title`, `text` | The picture, the question, and the explanation. |
| `confirmButton` | The "**yes, do it**" button. |
| `dismissButton` | The "**no, cancel**" button. |

> 🎉 **Big idea:** In Compose, **a dialog is just state + `if`**. No special "open dialog" command. Want it open? `showDialog = true`. Want it closed? `showDialog = false`. Simple! ✨

### Writing good dialogs ✍️

| ✅ Do | ❌ Don't |
|---|---|
| Ask a **clear question**: "*Delete all notes?*" | "*Are you sure?*" (sure about **what**?) |
| Use **action words** on buttons: "*Delete*", "*Log out*" | "*OK*" / "*Yes*" (unclear) |
| Explain **what will happen** | Leave the user guessing |
| Use dialogs **rarely** | Show a dialog for everything (annoying! 😤) |

### A custom dialog with your own content

For anything more complex, use `Dialog` with your own layout:

```kotlin
if (showRating) {
    Dialog(onDismissRequest = { showRating = false }) {
        Card(shape = MaterialTheme.shapes.extraLarge) {
            Column(
                modifier = Modifier.padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text("Enjoying the app? 😊", style = MaterialTheme.typography.titleLarge)
                Spacer(modifier = Modifier.height(16.dp))
                Row {
                    repeat(5) {
                        Icon(Icons.Filled.Star, contentDescription = null, tint = Color(0xFFFFB300))
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
                Button(onClick = { showRating = false }) { Text("Rate now") }
            }
        }
    }
}
```

Import: `androidx.compose.ui.window.Dialog`

`Dialog` gives you an **empty** pop-up window. You put **anything** inside. 🎨

---

## 11.9 Bottom Sheets 📤

A **bottom sheet** is a panel that **slides up** from the bottom. It shows **extra options** or a **small form**, without leaving the screen.

You've seen them in:
- 🗺️ Google Maps: details of a place
- 🔗 The **Share** panel
- 🎵 Music apps: "Add to playlist, Share, Download…"

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BottomSheetDemo() {
    var showSheet by remember { mutableStateOf(false) }
    val sheetState = rememberModalBottomSheetState()

    Button(onClick = { showSheet = true }, modifier = Modifier.padding(16.dp)) {
        Text("Open options")
    }

    if (showSheet) {
        ModalBottomSheet(
            onDismissRequest = { showSheet = false },
            sheetState = sheetState
        ) {
            Column(modifier = Modifier.padding(bottom = 32.dp)) {
                Text(
                    text = "Choose an option",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp)
                )
                SheetOption(Icons.Filled.Share, "Share") { showSheet = false }
                SheetOption(Icons.Filled.Edit, "Edit") { showSheet = false }
                SheetOption(Icons.Filled.Delete, "Delete") { showSheet = false }
            }
        }
    }
}

@Composable
fun SheetOption(icon: ImageVector, label: String, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(horizontal = 24.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null)
        Spacer(modifier = Modifier.width(16.dp))
        Text(label, style = MaterialTheme.typography.bodyLarge)
    }
}
```

Imports:

```kotlin
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.rememberModalBottomSheetState
```

```
┌──────────────────────────────┐
│     (screen is dimmed)       │
│                              │
├──────────────────────────────┤
│           ───                │  ← drag handle
│ Choose an option             │
│ 🔗  Share                    │
│ ✏️  Edit                     │
│ 🗑️  Delete                   │
└──────────────────────────────┘
```

| Code | Meaning |
|---|---|
| `var showSheet by remember { ... }` | Same idea as dialogs: **state + `if`**. |
| `rememberModalBottomSheetState()` | Remembers the sheet's **position** (open, half, hidden) and **animates** it. |
| `ModalBottomSheet(...)` | "Modal" = the rest of the screen is **dimmed** and blocked while it's open. |
| `onDismissRequest = { showSheet = false }` | User swiped it **down**, tapped **outside**, or pressed **Back**. |
| `Column(modifier = Modifier.padding(bottom = 32.dp))` | Extra space at the bottom, so the last option isn't too close to the edge. |

### Closing the sheet with a nice animation 🎬

Setting `showSheet = false` **removes** the sheet immediately (a little "jump"). To **slide it down** smoothly first:

```kotlin
val scope = rememberCoroutineScope()

SheetOption(Icons.Filled.Share, "Share") {
    scope.launch { sheetState.hide() }.invokeOnCompletion {
        if (!sheetState.isVisible) {
            showSheet = false
        }
    }
}
```

| Code | Meaning |
|---|---|
| `scope.launch { sheetState.hide() }` | **Animate** the sheet down (takes time → coroutine). |
| `.invokeOnCompletion { ... }` | "When that's **finished**, do this." |
| `if (!sheetState.isVisible) showSheet = false` | Now **remove** it from the screen. |

> 💡 This "hide, then remove" recipe is used a lot. Copy it when you need it. 📋

### Dialog vs Bottom sheet — which one?

| Use a **dialog** when… | Use a **bottom sheet** when… |
|---|---|
| You need a **decision** (yes/no) | You show **options** or a **small form** |
| It's **important** / dangerous | It's an **extra** step, not scary |
| Short text | A list of items, or more content |

---

## 11.10 Build It: A Notes App 🗒️

Let's build an app that uses **everything** from this chapter:

```
┌──────────────────────────────────┐
│ ☰  My Notes          🔍?    ⋮    │  ← TopAppBar + ⋮ menu (Sort, Delete all)
├──────────────────────────────────┤
│ ┌──────────────────────────────┐ │
│ │ Shopping 🛒             ☆  🗑 │ │  ← tap ☆ to favorite, 🗑 to delete
│ │ Milk, eggs, bread            │ │
│ └──────────────────────────────┘ │
│ ┌──────────────────────────────┐ │
│ │ Ideas 💡                ★  🗑 │ │
│ │ An app that waters plants    │ │
│ └──────────────────────────────┘ │
│                                  │
│ ┌──────────────────────┐         │
│ │ Note deleted    UNDO │  [✏️ New note]   ← Snackbar + Extended FAB
│ └──────────────────────┘         │
├──────────────────────────────────┤
│   (📝)       ★        ⚙️         │  ← NavigationBar
│   Notes  Favorites  Settings     │
└──────────────────────────────────┘

Tap the FAB → a bottom sheet slides up with a form to add a note.
Tap "Delete all" in the ⋮ menu → an AlertDialog asks to confirm.
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
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExtendedFloatingActionButton
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarDuration
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.SnackbarResult
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.myfirstapp.ui.theme.MyFirstAppTheme
import kotlinx.coroutines.launch

// ---------- Data ----------

data class Note(
    val id: Int,
    val title: String,
    val body: String,
    val isFavorite: Boolean = false
)

data class Tab(val label: String, val icon: ImageVector)

val appTabs = listOf(
    Tab("Notes", Icons.Filled.List),
    Tab("Favorites", Icons.Filled.Star),
    Tab("Settings", Icons.Filled.Settings)
)

val startNotes = listOf(
    Note(1, "Shopping 🛒", "Milk, eggs, bread, and bananas."),
    Note(2, "Ideas 💡", "An app that reminds me to water my plants.", isFavorite = true),
    Note(3, "Homework 📚", "Finish Chapter 11 and do all the practice tasks!"),
    Note(4, "Birthday 🎂", "Buy a gift for Asha before Friday.", isFavorite = true),
    Note(5, "Workout 🏃", "20 push-ups, 30 squats, 10 minutes of running.")
)

// ---------- Activity ----------

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyFirstAppTheme {
                NotesApp()
            }
        }
    }
}

// ---------- The app ----------

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NotesApp() {
    // ---- State ----
    var notes by remember { mutableStateOf(startNotes) }
    var nextId by remember { mutableIntStateOf(6) }
    var selectedTab by rememberSaveable { mutableIntStateOf(0) }
    var showAddSheet by rememberSaveable { mutableStateOf(false) }
    var showDeleteAllDialog by rememberSaveable { mutableStateOf(false) }
    var menuOpen by remember { mutableStateOf(false) }
    var confirmBeforeDelete by rememberSaveable { mutableStateOf(false) }
    var noteToDelete by remember { mutableStateOf<Note?>(null) }

    // ---- Helpers ----
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    val listState = rememberLazyListState()
    val scrollBehavior = TopAppBarDefaults.pinnedScrollBehavior()
    val fabExpanded by remember { derivedStateOf { listState.firstVisibleItemIndex == 0 } }

    // ---- Calculated ----
    val shownNotes = if (selectedTab == 1) notes.filter { it.isFavorite } else notes

    // ---- Events ----
    fun deleteNote(note: Note) {
        val position = notes.indexOf(note)
        notes = notes - note
        scope.launch {
            val result = snackbarHostState.showSnackbar(
                message = "\"${note.title}\" deleted",
                actionLabel = "Undo",
                duration = SnackbarDuration.Short
            )
            if (result == SnackbarResult.ActionPerformed) {
                notes = notes.toMutableList().apply {
                    add(position.coerceAtMost(size), note)
                }
            }
        }
    }

    fun toggleFavorite(note: Note) {
        notes = notes.map { if (it.id == note.id) it.copy(isFavorite = !it.isFavorite) else it }
    }

    fun addNote(title: String, body: String) {
        notes = listOf(Note(nextId, title, body)) + notes
        nextId++
        scope.launch { snackbarHostState.showSnackbar("Note added ✅") }
    }

    // ---- UI ----
    Scaffold(
        modifier = Modifier
            .fillMaxSize()
            .nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            TopAppBar(
                title = { Text(appTabs[selectedTab].label) },
                scrollBehavior = scrollBehavior,
                actions = {
                    if (selectedTab != 2) {
                        Box {
                            IconButton(onClick = { menuOpen = true }) {
                                Icon(Icons.Filled.MoreVert, contentDescription = "More options")
                            }
                            DropdownMenu(
                                expanded = menuOpen,
                                onDismissRequest = { menuOpen = false }
                            ) {
                                DropdownMenuItem(
                                    text = { Text("Sort A → Z") },
                                    onClick = {
                                        notes = notes.sortedBy { it.title }
                                        menuOpen = false
                                    }
                                )
                                HorizontalDivider()
                                DropdownMenuItem(
                                    text = { Text("Delete all", color = MaterialTheme.colorScheme.error) },
                                    leadingIcon = {
                                        Icon(
                                            Icons.Filled.Delete,
                                            contentDescription = null,
                                            tint = MaterialTheme.colorScheme.error
                                        )
                                    },
                                    enabled = notes.isNotEmpty(),
                                    onClick = {
                                        menuOpen = false
                                        showDeleteAllDialog = true
                                    }
                                )
                            }
                        }
                    }
                }
            )
        },
        bottomBar = {
            NavigationBar {
                appTabs.forEachIndexed { index, tab ->
                    NavigationBarItem(
                        selected = selectedTab == index,
                        onClick = { selectedTab = index },
                        icon = { Icon(tab.icon, contentDescription = null) },
                        label = { Text(tab.label) }
                    )
                }
            }
        },
        floatingActionButton = {
            if (selectedTab == 0) {
                ExtendedFloatingActionButton(
                    onClick = { showAddSheet = true },
                    icon = { Icon(Icons.Filled.Edit, contentDescription = null) },
                    text = { Text("New note") },
                    expanded = fabExpanded
                )
            }
        },
        snackbarHost = { SnackbarHost(hostState = snackbarHostState) }
    ) { innerPadding ->
        when (selectedTab) {
            0, 1 -> NotesList(
                notes = shownNotes,
                emptyText = if (selectedTab == 0) "No notes yet. Tap ✏️ to write one!" else "No favorites yet. Tap ☆ on a note.",
                listState = listState,
                contentPadding = innerPadding,
                onToggleFavorite = { toggleFavorite(it) },
                onDelete = { note ->
                    if (confirmBeforeDelete) noteToDelete = note else deleteNote(note)
                }
            )
            else -> SettingsPage(
                confirmBeforeDelete = confirmBeforeDelete,
                onConfirmBeforeDeleteChange = { confirmBeforeDelete = it },
                noteCount = notes.size,
                modifier = Modifier.padding(innerPadding)
            )
        }
    }

    // ---- Pop-ups (outside the Scaffold, drawn on top) ----

    if (showAddSheet) {
        AddNoteSheet(
            onDismiss = { showAddSheet = false },
            onSave = { title, body ->
                addNote(title, body)
                showAddSheet = false
            }
        )
    }

    if (showDeleteAllDialog) {
        AlertDialog(
            onDismissRequest = { showDeleteAllDialog = false },
            icon = { Icon(Icons.Filled.Warning, contentDescription = null) },
            title = { Text("Delete all notes?") },
            text = { Text("All ${notes.size} notes will be removed. This cannot be undone.") },
            confirmButton = {
                TextButton(onClick = {
                    notes = emptyList()
                    showDeleteAllDialog = false
                }) {
                    Text("Delete all")
                }
            },
            dismissButton = {
                TextButton(onClick = { showDeleteAllDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }

    noteToDelete?.let { note ->
        AlertDialog(
            onDismissRequest = { noteToDelete = null },
            title = { Text("Delete \"${note.title}\"?") },
            confirmButton = {
                TextButton(onClick = {
                    deleteNote(note)
                    noteToDelete = null
                }) { Text("Delete") }
            },
            dismissButton = {
                TextButton(onClick = { noteToDelete = null }) { Text("Cancel") }
            }
        )
    }
}

// ---------- Parts ----------

@Composable
fun NotesList(
    notes: List<Note>,
    emptyText: String,
    listState: LazyListState,
    contentPadding: PaddingValues,
    onToggleFavorite: (Note) -> Unit,
    onDelete: (Note) -> Unit
) {
    if (notes.isEmpty()) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(contentPadding)
                .padding(32.dp),
            contentAlignment = Alignment.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text("🗒️", fontSize = 64.sp)
                Text(emptyText, style = MaterialTheme.typography.titleMedium)
            }
        }
        return
    }

    LazyColumn(
        state = listState,
        contentPadding = PaddingValues(
            start = 16.dp,
            end = 16.dp,
            top = contentPadding.calculateTopPadding() + 8.dp,
            bottom = contentPadding.calculateBottomPadding() + 88.dp
        ),
        verticalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier.fillMaxSize()
    ) {
        items(notes, key = { it.id }) { note ->
            NoteCard(
                note = note,
                onToggleFavorite = { onToggleFavorite(note) },
                onDelete = { onDelete(note) },
                modifier = Modifier.animateItem()
            )
        }
    }
}

@Composable
fun NoteCard(
    note: Note,
    onToggleFavorite: () -> Unit,
    onDelete: () -> Unit,
    modifier: Modifier = Modifier
) {
    ElevatedCard(modifier = modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.padding(start = 16.dp, top = 12.dp, bottom = 12.dp, end = 4.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = note.title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = note.body,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis
                )
            }
            IconButton(onClick = onToggleFavorite) {
                Icon(
                    imageVector = Icons.Filled.Star,
                    contentDescription = if (note.isFavorite) "Remove from favorites" else "Add to favorites",
                    tint = if (note.isFavorite) Color(0xFFFFB300) else MaterialTheme.colorScheme.outlineVariant
                )
            }
            IconButton(onClick = onDelete) {
                Icon(Icons.Filled.Delete, contentDescription = "Delete ${note.title}")
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddNoteSheet(
    onDismiss: () -> Unit,
    onSave: (title: String, body: String) -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    var title by rememberSaveable { mutableStateOf("") }
    var body by rememberSaveable { mutableStateOf("") }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .imePadding()
                .padding(horizontal = 24.dp)
                .padding(bottom = 24.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Text("New note ✏️", style = MaterialTheme.typography.titleLarge)
            OutlinedTextField(
                value = title,
                onValueChange = { title = it.take(40) },
                label = { Text("Title") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
            OutlinedTextField(
                value = body,
                onValueChange = { body = it },
                label = { Text("Note") },
                minLines = 3,
                modifier = Modifier.fillMaxWidth()
            )
            Row(modifier = Modifier.align(Alignment.End)) {
                TextButton(onClick = onDismiss) { Text("Cancel") }
                Spacer(modifier = Modifier.padding(4.dp))
                Button(
                    onClick = { onSave(title.trim(), body.trim()) },
                    enabled = title.isNotBlank()
                ) {
                    Text("Save")
                }
            }
        }
    }
}

@Composable
fun SettingsPage(
    confirmBeforeDelete: Boolean,
    onConfirmBeforeDeleteChange: (Boolean) -> Unit,
    noteCount: Int,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.padding(16.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Column(modifier = Modifier.weight(1f)) {
                Text("Ask before deleting", style = MaterialTheme.typography.bodyLarge)
                Text(
                    "Show a dialog instead of Undo",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Switch(checked = confirmBeforeDelete, onCheckedChange = onConfirmBeforeDeleteChange)
        }
        Spacer(modifier = Modifier.height(16.dp))
        HorizontalDivider()
        Spacer(modifier = Modifier.height(16.dp))
        Text("You have $noteCount notes 🗒️", style = MaterialTheme.typography.bodyLarge)
    }
}

// ---------- Preview ----------

@Preview(showSystemUi = true)
@Composable
fun NotesAppPreview() {
    MyFirstAppTheme {
        NotesApp()
    }
}
```

> ⚠️ Keep **your own** `package` line and theme import.
> ℹ️ `Icons.Filled.List` may show a yellow warning saying it's deprecated and suggesting `Icons.AutoMirrored.Filled.List`. Both work; you can press Alt + Enter to switch to the new one.

### Every new part explained

#### Part 1: `setContent` — the Scaffold moved!

```kotlin
setContent {
    MyFirstAppTheme {
        NotesApp()
    }
}
```

Until now, the `Scaffold` was in `onCreate`. Now **`NotesApp` has its own `Scaffold`**, because it needs to fill the `topBar`, `bottomBar`, `floatingActionButton`, and `snackbarHost` slots. 🏗️

#### Part 2: The state

| State | Meaning |
|---|---|
| `notes`, `nextId` | The notes and the next id to use. |
| `selectedTab` | Which bottom tab: 0 = Notes, 1 = Favorites, 2 = Settings. |
| `showAddSheet`, `showDeleteAllDialog`, `menuOpen` | Is each pop-up **open**? (State + `if`!) |
| `confirmBeforeDelete` | A setting from the Settings tab. |
| `noteToDelete: Note?` | The note waiting for confirmation, or `null` (no dialog). |

```kotlin
    var noteToDelete by remember { mutableStateOf<Note?>(null) }
```

- `mutableStateOf<Note?>(null)` → we must say the type `<Note?>`, because Kotlin can't guess it from `null` alone.
- A **nullable** state is a neat trick: `null` = no dialog, a `Note` = show the dialog **for this note**. One state does two jobs! ✨

#### Part 3: Functions inside a Composable

```kotlin
    fun deleteNote(note: Note) { ... }
    fun toggleFavorite(note: Note) { ... }
    fun addNote(title: String, body: String) { ... }
```

- You can write **normal functions inside** a Composable! They can use the state around them.
- This keeps the UI part below **short and readable**: `onToggleFavorite = { toggleFavorite(it) }`.

#### Part 4: Delete with Undo ↩️

```kotlin
    fun deleteNote(note: Note) {
        val position = notes.indexOf(note)
        notes = notes - note
        scope.launch {
            val result = snackbarHostState.showSnackbar(
                message = "\"${note.title}\" deleted",
                actionLabel = "Undo",
                duration = SnackbarDuration.Short
            )
            if (result == SnackbarResult.ActionPerformed) {
                notes = notes.toMutableList().apply {
                    add(position.coerceAtMost(size), note)
                }
            }
        }
    }
```

| Step | Code | Meaning |
|---|---|---|
| 1 | `val position = notes.indexOf(note)` | Remember **where** the note was. |
| 2 | `notes = notes - note` | Remove it **now**. |
| 3 | `showSnackbar(..., actionLabel = "Undo")` | Show the message and **wait**. ⏳ |
| 4 | `if (result == ActionPerformed)` | The user tapped **Undo**… |
| 5 | `notes.toMutableList().apply { add(position..., note) }` | …make a changeable copy, put the note **back in the same place**, and save it as the new list. |

| Detail | Meaning |
|---|---|
| `toMutableList()` | A **new** list we can `add` to. (The original isn't changed — immutable state, Chapter 8.) |
| `.apply { add(...) }` | `apply` (Chapter 4): do things on the object, then give it back. |
| `position.coerceAtMost(size)` | "Use `position`, but **not more than** `size`." In case other notes were deleted in the meantime, so we never add at a position that doesn't exist (which would crash 💥). |

#### Part 5: The top bar

- `title = { Text(appTabs[selectedTab].label) }` → the title **changes** with the tab.
- `pinnedScrollBehavior()` + `nestedScroll(...)` → the bar **changes color** when notes scroll under it.
- The **⋮ menu** has "Sort A → Z" and a **red** "Delete all" (with `enabled = notes.isNotEmpty()` → greyed out when there's nothing to delete).
- `if (selectedTab != 2)` → no menu on the Settings tab.

#### Part 6: The FAB — only on the Notes tab

```kotlin
        floatingActionButton = {
            if (selectedTab == 0) {
                ExtendedFloatingActionButton(..., expanded = fabExpanded)
            }
        },
```

- Shown only on the **Notes** tab.
- Shrinks to an icon when you scroll (11.5).

#### Part 7: The content — `when` on the tab

```kotlin
        when (selectedTab) {
            0, 1 -> NotesList(notes = shownNotes, ...)
            else -> SettingsPage(...)
        }
```

- Tabs **0 and 1** both show a `NotesList` — with **all** notes or only **favorites** (`shownNotes` is calculated).
- The **same** `NotesList` Composable is reused with different data and empty texts. ♻️

#### Part 8: `NotesList` — using `innerPadding` with our own padding

```kotlin
        contentPadding = PaddingValues(
            start = 16.dp,
            end = 16.dp,
            top = contentPadding.calculateTopPadding() + 8.dp,
            bottom = contentPadding.calculateBottomPadding() + 88.dp
        ),
```

- We want the Scaffold's padding (for the bars) **plus** our own spacing.
- `calculateTopPadding()` / `calculateBottomPadding()` → read the numbers out of the `PaddingValues`.
- `+ 88.dp` at the bottom → room so the **last note** isn't hidden behind the FAB. 👌

#### Part 9: Pop-ups are drawn **after** the Scaffold

```kotlin
    if (showAddSheet) { AddNoteSheet(...) }
    if (showDeleteAllDialog) { AlertDialog(...) }
    noteToDelete?.let { note -> AlertDialog(...) }
```

- Dialogs and sheets appear **on top** of everything, wherever you write them. Putting them at the **end** keeps the code tidy. 🧹
- `noteToDelete?.let { note -> ... }` → "**If** there is a note to delete, show the dialog for it." (Chapter 3: `?.let`.)

#### Part 10: `AddNoteSheet` — a form in a bottom sheet

```kotlin
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
```

- `skipPartiallyExpanded = true` → the sheet opens **fully**, not half-way. Better for a form. 📝
- `.imePadding()` → the keyboard doesn't cover the fields (Chapter 9).
- `title` and `body` are **local state** of the sheet. When saved, the sheet calls `onSave(title, body)` → **events up** ⬆️.
- `enabled = title.isNotBlank()` → can't save a note without a title.
- `onSave: (title: String, body: String) -> Unit` → you can **name** the inputs in a lambda type. It's just for readability. 📖

#### Part 11: Settings change behavior

- The **Switch** in Settings changes `confirmBeforeDelete`.
- In `onDelete`: `if (confirmBeforeDelete) noteToDelete = note else deleteNote(note)` → **dialog** or **Undo snackbar**, depending on the setting. ⚙️

### Run it! ▶️

1. Tap ☆ on a note → it turns gold ★. Open **Favorites** → it's there!
2. Tap 🗑️ → **"deleted"** snackbar → tap **UNDO** → it's back in the same place. ↩️
3. Tap **✏️ New note** → a sheet slides up → write a note → **Save** → "Note added ✅".
4. Scroll the list → the FAB **shrinks**; the top bar changes color.
5. ⋮ → **Sort A → Z**.
6. ⋮ → **Delete all** → a dialog asks first. ⚠️
7. **Settings** → turn on "Ask before deleting" → now 🗑️ shows a **dialog** instead.

🎉 **This is a real app structure** — top bar, bottom tabs, FAB, snackbars, dialogs, and sheets. Professional apps are built exactly like this!

---

## 11.11 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| Not using `innerPadding` | Content hidden under the top/bottom bars | `Modifier.padding(innerPadding)` or `contentPadding = innerPadding`. |
| `TopAppBar` shows an "experimental" error | *This material API is experimental...* | Add `@OptIn(ExperimentalMaterial3Api::class)`. |
| Scroll behavior does nothing | Forgot to connect it | Add `Modifier.nestedScroll(scrollBehavior.nestedScrollConnection)` to the `Scaffold`. |
| `showSnackbar` in `onClick` | *Suspend function should be called only from a coroutine* | `scope.launch { ... }` |
| Snackbar never appears | No host | `snackbarHost = { SnackbarHost(snackbarHostState) }` |
| `SnackbarHostState()` without `remember` | Snackbars get lost on recomposition | `remember { SnackbarHostState() }` |
| Dialog can't be closed | `onDismissRequest` does nothing | `onDismissRequest = { showDialog = false }` |
| Menu stays open after tapping an item | Forgot to close it | Set `menuOpen = false` in each `onClick`. |
| Last list item hidden behind the FAB | No bottom space | Add extra bottom `contentPadding` (~88 dp). |
| Bottom sheet "jumps" away | Removed without animation | `scope.launch { sheetState.hide() }.invokeOnCompletion { ... }` |
| Too many top-bar icons | Crowded, confusing | Max 2–3 icons; the rest in a ⋮ menu. |
| Dialogs for everything | Annoying 😤 | Prefer **Undo** snackbars; use dialogs only for big decisions. |

---

## 11.12 Summary — What You Learned 🎓

✅ **`Scaffold`** has slots: `topBar`, `bottomBar`, `floatingActionButton`, `snackbarHost`, and content with **`innerPadding`** (always use it!).

✅ **Top app bars:** `TopAppBar`, `CenterAlignedTopAppBar`, `MediumTopAppBar`, `LargeTopAppBar`; `title`, `navigationIcon`, `actions`, `colors`. Needs `@OptIn(ExperimentalMaterial3Api::class)`.

✅ **Scroll behaviors:** `pinned`, `enterAlways`, `exitUntilCollapsed` + `Modifier.nestedScroll(...)`.

✅ **⋮ menu:** `IconButton` + `DropdownMenu` in a `Box`.

✅ **FABs:** Small, normal, Large, **Extended** (with `expanded`). One per screen.

✅ **Bottom bars:** `NavigationBar` + `NavigationBarItem` for 3–5 main tabs; `BottomAppBar` for actions; `BadgedBox` for badges.

✅ **Snackbars:** `SnackbarHostState` + `SnackbarHost` + `scope.launch { showSnackbar(...) }`; check `SnackbarResult.ActionPerformed` for **Undo**.

✅ **Dialogs:** `AlertDialog` / `Dialog` — **state + `if`**. Clear questions and action words.

✅ **Bottom sheets:** `ModalBottomSheet` + `rememberModalBottomSheetState()`; hide with animation.

✅ You built a full **Notes app** with tabs, menus, FAB, Undo, dialogs, and a sheet! 🗒️

---

## 11.13 Practice Time 🏋️

**Task 1 — Large collapsing bar:**
Make a screen with a `LargeTopAppBar` titled "Settings ⚙️" and `exitUntilCollapsedScrollBehavior()`, and a `LazyColumn` of 30 rows. Watch the title shrink as you scroll.

**Task 2 — Counter with snackbar:**
A screen with a FAB ➕. Each tap adds 1 to a counter shown in the middle. Every **5th** tap shows a snackbar: `"Wow, 5 taps! 🎉"` (then 10, 15…).

**Task 3 — Logout dialog:**
A top app bar with a ⋮ menu containing "Profile" and "Log out". Tapping "Log out" opens an `AlertDialog`: title "Log out?", text "You will need to sign in again.", buttons **Log out** / **Cancel**. Tapping **Log out** shows a snackbar "Logged out 👋".

**Task 4 — Color picker sheet:**
A button "Pick a color 🎨" opens a `ModalBottomSheet` with 5 colored circles in a `Row`. Tapping a circle closes the sheet (with the hide animation) and changes the **screen background** to that color.

**Task 5 — 4 tabs with a badge:**
A `NavigationBar` with 4 tabs (Home, Search, Inbox, Profile). The **Inbox** tab has a badge with the number `5`. When the user opens the Inbox tab, the badge disappears.

---

### Answers

**Task 1:**

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CollapsingSettings() {
    val scrollBehavior = TopAppBarDefaults.exitUntilCollapsedScrollBehavior()

    Scaffold(
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            LargeTopAppBar(
                title = { Text("Settings ⚙️") },
                scrollBehavior = scrollBehavior
            )
        }
    ) { innerPadding ->
        LazyColumn(contentPadding = innerPadding) {
            items(30) { i ->
                Text("Setting number ${i + 1}", modifier = Modifier.padding(16.dp))
            }
        }
    }
}
```

Import: `androidx.compose.material3.LargeTopAppBar`

**Task 2:**

```kotlin
@Composable
fun TapCounter() {
    var count by rememberSaveable { mutableIntStateOf(0) }
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()

    Scaffold(
        floatingActionButton = {
            FloatingActionButton(onClick = {
                count++
                if (count % 5 == 0) {
                    scope.launch { snackbarHostState.showSnackbar("Wow, $count taps! 🎉") }
                }
            }) {
                Icon(Icons.Filled.Add, contentDescription = "Add one")
            }
        },
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { innerPadding ->
        Box(
            modifier = Modifier.fillMaxSize().padding(innerPadding),
            contentAlignment = Alignment.Center
        ) {
            Text("$count", style = MaterialTheme.typography.displayLarge)
        }
    }
}
```

`count % 5 == 0` → every 5th tap (Chapter 2: remainder). 🔢

**Task 3:**

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LogoutDemo() {
    var menuOpen by remember { mutableStateOf(false) }
    var showLogout by remember { mutableStateOf(false) }
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Home") },
                actions = {
                    Box {
                        IconButton(onClick = { menuOpen = true }) {
                            Icon(Icons.Filled.MoreVert, contentDescription = "More options")
                        }
                        DropdownMenu(expanded = menuOpen, onDismissRequest = { menuOpen = false }) {
                            DropdownMenuItem(
                                text = { Text("Profile") },
                                onClick = { menuOpen = false }
                            )
                            DropdownMenuItem(
                                text = { Text("Log out") },
                                onClick = {
                                    menuOpen = false
                                    showLogout = true
                                }
                            )
                        }
                    }
                }
            )
        },
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { innerPadding ->
        Text("Welcome!", modifier = Modifier.padding(innerPadding).padding(16.dp))
    }

    if (showLogout) {
        AlertDialog(
            onDismissRequest = { showLogout = false },
            title = { Text("Log out?") },
            text = { Text("You will need to sign in again.") },
            confirmButton = {
                TextButton(onClick = {
                    showLogout = false
                    scope.launch { snackbarHostState.showSnackbar("Logged out 👋") }
                }) { Text("Log out") }
            },
            dismissButton = {
                TextButton(onClick = { showLogout = false }) { Text("Cancel") }
            }
        )
    }
}
```

**Task 4:**

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ColorPickerSheetDemo() {
    val colors = listOf(
        Color(0xFFFFCDD2), Color(0xFFC8E6C9), Color(0xFFBBDEFB),
        Color(0xFFFFF9C4), Color(0xFFE1BEE7)
    )
    var background by remember { mutableStateOf(Color.White) }
    var showSheet by remember { mutableStateOf(false) }
    val sheetState = rememberModalBottomSheetState()
    val scope = rememberCoroutineScope()

    Box(
        modifier = Modifier.fillMaxSize().background(background),
        contentAlignment = Alignment.Center
    ) {
        Button(onClick = { showSheet = true }) { Text("Pick a color 🎨") }
    }

    if (showSheet) {
        ModalBottomSheet(onDismissRequest = { showSheet = false }, sheetState = sheetState) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 32.dp),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                colors.forEach { color ->
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .background(color, CircleShape)
                            .clickable {
                                background = color
                                scope.launch { sheetState.hide() }.invokeOnCompletion {
                                    if (!sheetState.isVisible) showSheet = false
                                }
                            }
                    )
                }
            }
        }
    }
}
```

> 🌙 We used **light, fixed** colors on purpose here — it's a "paint the wall" demo, not theme text. (Chapter 7's rule is about **text and surfaces**.)

**Task 5:**

```kotlin
@Composable
fun FourTabs() {
    val tabs = listOf(
        Tab("Home", Icons.Filled.Home),
        Tab("Search", Icons.Filled.Search),
        Tab("Inbox", Icons.Filled.Email),
        Tab("Profile", Icons.Filled.Person)
    )
    var selected by rememberSaveable { mutableIntStateOf(0) }
    var unread by rememberSaveable { mutableIntStateOf(5) }

    Scaffold(
        bottomBar = {
            NavigationBar {
                tabs.forEachIndexed { index, tab ->
                    NavigationBarItem(
                        selected = selected == index,
                        onClick = {
                            selected = index
                            if (tab.label == "Inbox") unread = 0
                        },
                        icon = {
                            if (tab.label == "Inbox" && unread > 0) {
                                BadgedBox(badge = { Badge { Text("$unread") } }) {
                                    Icon(tab.icon, contentDescription = null)
                                }
                            } else {
                                Icon(tab.icon, contentDescription = null)
                            }
                        },
                        label = { Text(tab.label) }
                    )
                }
            }
        }
    ) { innerPadding ->
        Box(
            modifier = Modifier.fillMaxSize().padding(innerPadding),
            contentAlignment = Alignment.Center
        ) {
            Text("${tabs[selected].label} screen", style = MaterialTheme.typography.headlineSmall)
        }
    }
}
```

This reuses the `Tab` data class from the Notes app.

---

## 11.14 What Is Next?

You now know **all the building blocks** of a single screen! 🧱✅

In **Chapter 12: 🛠️ Mini Project — Tip Calculator App**, you will build a **complete, polished app** from start to finish, using everything from Chapters 1–11:

- Planning an app on paper first ✏️
- A custom theme 🎨
- Text fields with the right keyboards ⌨️
- Sliders and chips for the tip %
- Splitting the bill between friends 👥
- Rounding up 🔼
- State, hoisting, and clean, reusable Composables
- Previews for light and dark mode 🌙

**Great job finishing Chapter 11! 🎉 Your screens now look and feel like real apps!**
