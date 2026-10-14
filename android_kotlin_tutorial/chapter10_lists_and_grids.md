# Chapter 10: Lists and Grids — Showing Many Things Fast

> **What you will learn in this chapter**
>
> 1. Why `Column` + `forEach` is slow for long lists 🐢
> 2. `LazyColumn` — super-fast vertical lists ⚡
> 3. `item`, `items`, and `itemsIndexed`
> 4. Spacing, padding, and dividers in lists
> 5. **Keys** — helping Compose know which item is which 🔑
> 6. Tapping items, and changing the list (add, remove, update)
> 7. Headers and **sticky headers** 📌
> 8. `LazyRow` — horizontal lists ➡️
> 9. Grids: `LazyVerticalGrid` and staggered grids 🖼️
> 10. Controlling scrolling — the **"back to top"** button ⬆️
> 11. Empty lists, and mixing different content in one list
> 12. Building a **Contacts app** with search 🔍📇
>
> **Time needed:** about 4 to 5 hours.

---

## 10.1 The Problem: Long Lists Are Slow 🐢

In Chapter 6 and 8, we showed lists like this:

```kotlin
Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
    names.forEach { name ->
        Text(name)
    }
}
```

This is **fine for 10 or 20 items**. But imagine:

- A chat app with **5,000 messages** 💬
- A music app with **20,000 songs** 🎵
- A shop with **100,000 products** 🛍️

A `Column` draws **every single item** — even the ones far below the screen that nobody can see. That means:

- 🐢 The screen opens **slowly**.
- 🔋 It uses a lot of **battery** and **memory**.
- 💥 It might even **crash** with too many items.

### The solution: "lazy" lists

A **lazy** list only draws the items you can **see right now** (plus a few extra). When you scroll, it draws the new ones and **forgets** the ones that left the screen.

**Real-life example:** A **restaurant** 🍽️.
- `Column` = the chef cooks **every dish on the menu** before you even sit down. 😵 Huge waste!
- `LazyColumn` = the chef cooks **only what you order**, when you order it. 👨‍🍳 Smart!

| | `Column` + `forEach` | `LazyColumn` |
|---|---|---|
| Draws | **All** items | Only **visible** items |
| Good for | Small lists (up to ~30) | Any size, even 100,000+ ⚡ |
| Scrolling | Needs `verticalScroll` | Scrolls **by itself** |

> 💡 **Rule:** If a list can grow long, or comes from the internet or a database, use a **Lazy** list.

---

## 10.2 Your First `LazyColumn` ⚡

```kotlin
@Composable
fun NumberList(modifier: Modifier = Modifier) {
    LazyColumn(modifier = modifier.fillMaxSize()) {
        items(1000) { index ->
            Text(
                text = "Item number ${index + 1}",
                modifier = Modifier.padding(16.dp)
            )
        }
    }
}
```

Imports:

```kotlin
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
```

Run it and scroll. **1,000 items**, and it's smooth as butter! 🧈

### Every bit explained

| Piece | Meaning |
|---|---|
| `LazyColumn(...)` | A lazy, vertical list. **It scrolls by itself** — no `verticalScroll` needed! |
| `{ ... }` | ⚠️ **Not** normal Composable content! It's a special area where you **describe** the items (see below). |
| `items(1000) { index -> ... }` | "There are **1000** items. Here's how to draw item number `index`." `index` goes from 0 to 999. |
| `Text(...)` | What **one** item looks like. |

### ⚠️ The inside of `LazyColumn` is special

Inside `LazyColumn { }`, you **can't** call Composables directly:

```kotlin
LazyColumn {
    Text("Hello")      // ❌ ERROR: @Composable invocations can only happen
                       //    from the context of a @Composable function
}
```

Instead, you use **`item { }`** or **`items(...) { }`**. Inside **those**, you write normal Composables:

```kotlin
LazyColumn {
    item {
        Text("Hello")  // ✅
    }
}
```

**Why?** `LazyColumn` doesn't draw things right away. It **collects a list of recipes** 📝 ("here's how to draw item 1, item 2…"). Then it cooks only the ones on screen. `item { }` = "**here's one recipe**".

---

## 10.3 `item`, `items`, and `itemsIndexed` 📋

There are **4 ways** to add things to a lazy list:

### 1. `item { }` — one single item

```kotlin
LazyColumn {
    item {
        Text("My Shopping List", style = MaterialTheme.typography.headlineSmall)
    }
}
```

Good for a **title**, a **header**, a **button** at the end…

### 2. `items(count) { index -> }` — a number of items

```kotlin
items(50) { index ->
    Text("Row $index")
}
```

### 3. `items(list) { item -> }` — one for each thing in a list ⭐ (most common)

```kotlin
val fruits = listOf("Apple 🍎", "Banana 🍌", "Cherry 🍒", "Grape 🍇")

LazyColumn {
    items(fruits) { fruit ->
        Text(text = fruit, modifier = Modifier.padding(16.dp))
    }
}
```

> ⚠️ **Import alert!** For `items(list)`, you need `import androidx.compose.foundation.lazy.items`. If you see a red error like *"Type mismatch: inferred type is List<String> but Int was expected"*, this import is **missing**. Press Alt + Enter on `items` and choose the one from **`androidx.compose.foundation.lazy`**.

### 4. `itemsIndexed(list) { index, item -> }` — with the position

```kotlin
LazyColumn {
    itemsIndexed(fruits) { index, fruit ->
        Text("${index + 1}. $fruit", modifier = Modifier.padding(16.dp))
    }
}
```

Output:

```
1. Apple 🍎
2. Banana 🍌
3. Cherry 🍒
4. Grape 🍇
```

Import: `androidx.compose.foundation.lazy.itemsIndexed`

### Mix them all! 🥗

```kotlin
LazyColumn {
    item {
        Text("Fruits", style = MaterialTheme.typography.titleLarge)
    }
    items(fruits) { fruit ->
        Text(fruit)
    }
    item {
        Text("Vegetables", style = MaterialTheme.typography.titleLarge)
    }
    items(vegetables) { veg ->
        Text(veg)
    }
    item {
        Button(onClick = { }) { Text("Add more") }
    }
}
```

The list is **one long scroll**: title → fruits → title → vegetables → button. All lazy! ⚡

---

## 10.4 Spacing, Padding, and Dividers 📏

### Space between items: `verticalArrangement`

```kotlin
LazyColumn(
    verticalArrangement = Arrangement.spacedBy(8.dp)
) {
    items(fruits) { fruit -> FruitCard(fruit) }
}
```

Same as `Column` (Chapter 6)! 👍

### Space around the whole list: `contentPadding` ⭐

```kotlin
LazyColumn(
    contentPadding = PaddingValues(16.dp),
    verticalArrangement = Arrangement.spacedBy(8.dp)
) { ... }
```

Import: `androidx.compose.foundation.layout.PaddingValues`

**Why not `Modifier.padding(16.dp)`?** Look at the difference when you scroll:

| `Modifier.padding(16.dp)` | `contentPadding = PaddingValues(16.dp)` |
|---|---|
| The **list window** gets smaller. Items are **cut off** 16 dp before the edge. ✂️ | The list window stays **full size**. The padding is **inside** the scrolling area — items scroll **all the way** to the edge. ✨ |

> 💡 For lists, use **`contentPadding`**. It looks much nicer, especially at the bottom of the screen.

`PaddingValues` options:

```kotlin
PaddingValues(16.dp)                                   // all sides
PaddingValues(horizontal = 16.dp, vertical = 8.dp)     // left/right and top/bottom
PaddingValues(start = 16.dp, top = 8.dp, end = 16.dp, bottom = 80.dp)
```

> 💡 **Tip:** A big `bottom` padding (like `80.dp`) leaves room so the **last item** isn't hidden behind a floating button. 👌

### Dividers between items

```kotlin
LazyColumn {
    itemsIndexed(fruits) { index, fruit ->
        Text(fruit, modifier = Modifier.padding(16.dp))
        if (index < fruits.lastIndex) {
            HorizontalDivider()
        }
    }
}
```

Inside **one** item, you can put **several** Composables (here: a `Text` and a `HorizontalDivider`). They are stacked like a Column.
And `if (index < lastIndex)` — no divider after the **last** one (Chapter 6 trick). ✨

---

## 10.5 Lists of Data Classes — The Real World 🌍

Real apps show lists of **objects**, not just Strings.

```kotlin
data class Song(
    val id: Int,
    val title: String,
    val artist: String,
    val minutes: Int,
    val seconds: Int
)

val songs = listOf(
    Song(1, "Sunrise", "The Morning Band", 3, 45),
    Song(2, "Ocean Waves", "Blue Sea", 4, 12),
    Song(3, "City Lights", "Neon Kids", 2, 58),
    Song(4, "Mountain Air", "Peak Trio", 5, 3),
    Song(5, "Rainy Day", "Cloud Nine", 3, 21)
)
```

### A separate Composable for one row ⭐

```kotlin
@Composable
fun SongRow(song: Song, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text("🎵", fontSize = 28.sp)
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(song.title, style = MaterialTheme.typography.titleMedium)
            Text(
                song.artist,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Text(
            text = "${song.minutes}:${song.seconds.toString().padStart(2, '0')}",
            style = MaterialTheme.typography.labelLarge
        )
    }
}

@Composable
fun SongList(songs: List<Song>, modifier: Modifier = Modifier) {
    LazyColumn(modifier = modifier.fillMaxSize()) {
        items(songs) { song ->
            SongRow(song)
        }
    }
}
```

| Code | Meaning |
|---|---|
| `SongRow(song: Song)` | A Composable for **one** song. Easy to read, preview, and reuse. ♻️ |
| `SongList(songs: List<Song>)` | The list receives its data **from outside** (hoisting, Chapter 8). |
| `seconds.toString().padStart(2, '0')` | Make it at least 2 characters by adding `0` in front: `3` → `"03"`. So `5:3` becomes `5:03`. ⏱️ |

> 💡 **Always** make a separate Composable for one list item. The list code stays short, and you can preview one row by itself.

---

## 10.6 Keys — Which Item Is Which? 🔑

### The problem

Imagine a list of 3 songs. Each row has its own little `remember` state (like "*is this row expanded?*"). You expand **row 2**. Then you **delete row 1**.

Without keys, Compose only knows rows by their **position**: "the first row, the second row…". After the delete, the old row 3 moves to position 2… and **gets row 2's state!** The wrong song is now expanded. 😵

### The solution: give each item a **key**

```kotlin
LazyColumn {
    items(
        items = songs,
        key = { song -> song.id }
    ) { song ->
        SongRow(song)
    }
}
```

- `key = { song -> song.id }` → "Use the song's **id** to recognize it."
- Now Compose knows: "*This is song #7*", no matter **where** it is in the list. 🔑
- State stays with the **right** item when the list changes.

**Real-life example:** Students in a classroom 🧑‍🎓.
- Without keys = "*the student in seat 3*". If students change seats, you confuse them.
- With keys = "*Asha, student ID 1042*". Wherever she sits, you know it's her.

### Rules for keys

| Rule | Why |
|---|---|
| Must be **unique** — no two items with the same key | Otherwise: crash 💥 *"Key was already used"* |
| Must stay the **same** for the same item | So Compose can follow it |
| Use simple types: `Int`, `Long`, `String` | They can be saved |

> ⚠️ **Don't** use the **index** as a key (`key = { index }`) — that's the same as no key!
> ⚠️ **Don't** use the title as a key if two items could have the **same** title.

> 💡 **Best practice:** Give every data class an **`id`**, and **always** use it as the key when the list can **change** (add, remove, sort, filter). Data from databases and the internet almost always has an id already.

### Bonus: smooth animations with `animateItem()` ✨

Because Compose knows which item is which (thanks to keys!), it can **animate** them:

```kotlin
items(songs, key = { it.id }) { song ->
    SongRow(song, modifier = Modifier.animateItem())
}
```

Now when items are **added**, **removed**, or **moved**, they **slide** and **fade** smoothly instead of jumping. 🎬

> ℹ️ `Modifier.animateItem()` needs a **key**. In older Compose versions it was called `animateItemPlacement()`.

---

## 10.7 Tapping Items and Changing the List 👆

### Tapping an item

```kotlin
@Composable
fun SongList(
    songs: List<Song>,
    onSongClick: (Song) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyColumn(modifier = modifier) {
        items(songs, key = { it.id }) { song ->
            SongRow(
                song = song,
                modifier = Modifier.clickable { onSongClick(song) }
            )
        }
    }
}
```

- `onSongClick: (Song) -> Unit` → "**which** song was tapped" goes **up** to the parent (events up ⬆️, Chapter 8).
- `.clickable { }` on the row → the whole row is tappable, with a ripple 🌊.

### Changing the list: add, remove, update

The list lives in **state** (Chapter 8). When the state changes, the `LazyColumn` updates. ✨

```kotlin
@Composable
fun TodoScreen(modifier: Modifier = Modifier) {
    var todos by remember {
        mutableStateOf(
            listOf(
                Todo(1, "Learn LazyColumn", false),
                Todo(2, "Drink water 💧", true),
                Todo(3, "Call grandma ☎️", false)
            )
        )
    }
    var nextId by remember { mutableIntStateOf(4) }

    Column(modifier = modifier.fillMaxSize()) {
        Button(
            onClick = {
                todos = todos + Todo(nextId, "New task #$nextId", false)
                nextId++
            },
            modifier = Modifier.padding(16.dp)
        ) {
            Text("Add task")
        }

        LazyColumn(modifier = Modifier.weight(1f)) {
            items(todos, key = { it.id }) { todo ->
                TodoRow(
                    todo = todo,
                    onCheckedChange = { checked ->
                        todos = todos.map {
                            if (it.id == todo.id) it.copy(done = checked) else it
                        }
                    },
                    onDelete = {
                        todos = todos.filter { it.id != todo.id }
                    },
                    modifier = Modifier.animateItem()
                )
            }
        }
    }
}

data class Todo(val id: Int, val text: String, val done: Boolean)

@Composable
fun TodoRow(
    todo: Todo,
    onCheckedChange: (Boolean) -> Unit,
    onDelete: () -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Checkbox(checked = todo.done, onCheckedChange = onCheckedChange)
        Text(
            text = todo.text,
            style = MaterialTheme.typography.bodyLarge,
            textDecoration = if (todo.done) TextDecoration.LineThrough else null,
            modifier = Modifier.weight(1f)
        )
        IconButton(onClick = onDelete) {
            Icon(Icons.Filled.Delete, contentDescription = "Delete ${todo.text}")
        }
    }
}
```

### The 3 list operations (immutable style, Chapter 8)

| Operation | Code | Meaning |
|---|---|---|
| **Add** ➕ | `todos = todos + newTodo` | A new list with one more item at the end. |
| **Remove** ➖ | `todos = todos.filter { it.id != todo.id }` | A new list with **everything except** this one. |
| **Update** ✏️ | `todos = todos.map { if (it.id == todo.id) it.copy(done = checked) else it }` | A new list where **only** this one is changed. |

**The update, step by step:**
- `map` goes through **every** todo (Chapter 3).
- If it's the one we want (`it.id == todo.id`) → make a **copy** with the change.
- Otherwise → keep it **as it is** (`else it`).

> 💡 These **three patterns** (`+`, `filter`, `map` + `copy`) are used in **almost every** Android app. Learn them well! 🌟

| Other detail | Meaning |
|---|---|
| `LazyColumn(modifier = Modifier.weight(1f))` | The list takes all the space **below** the button (Chapter 6). |
| `textDecoration = if (todo.done) LineThrough else null` | Done tasks are ~~crossed out~~. `null` = no decoration. |
| `Modifier.animateItem()` | New tasks **slide in**, deleted ones **fade out**. ✨ |

---

## 10.8 Headers and Sticky Headers 📌

### Normal headers

Just use `item { }`:

```kotlin
LazyColumn {
    item { SectionHeader("Today") }
    items(todayMessages, key = { it.id }) { MessageRow(it) }

    item { SectionHeader("Yesterday") }
    items(yesterdayMessages, key = { it.id }) { MessageRow(it) }
}
```

### Sticky headers — they stay on top! 📌

A **sticky header** **sticks** to the top of the screen while you scroll through its section. When the next section arrives, the new header **pushes** the old one away.

You've seen this in **contact lists** (A, B, C…) and **chat apps** (Today, Yesterday…).

```kotlin
@OptIn(ExperimentalFoundationApi::class)
@Composable
fun GroupedNames(names: List<String>, modifier: Modifier = Modifier) {
    val grouped = names.sorted().groupBy { it.first().uppercaseChar() }

    LazyColumn(modifier = modifier.fillMaxSize()) {
        grouped.forEach { (letter, namesForLetter) ->
            stickyHeader(key = "header_$letter") {
                Text(
                    text = letter.toString(),
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(MaterialTheme.colorScheme.surfaceVariant)
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                )
            }
            items(namesForLetter, key = { it }) { name ->
                Text(name, modifier = Modifier.padding(16.dp))
            }
        }
    }
}
```

Imports:

```kotlin
import androidx.compose.foundation.ExperimentalFoundationApi
```

### Every bit explained

| Code | Meaning |
|---|---|
| `@OptIn(ExperimentalFoundationApi::class)` | `stickyHeader` was marked "**experimental**" (new) in many Compose versions. This line says "*I know, I want to use it.*" If your version doesn't need it, you'll just see a small grey warning — no problem. |
| `names.sorted()` | Sort A → Z. |
| `.groupBy { it.first().uppercaseChar() }` | Make a **Map** (Chapter 3): `'A' → [Asha, Ali]`, `'B' → [Ben]`… |
| `grouped.forEach { (letter, namesForLetter) -> ... }` | For each group… (`(letter, names)` takes the pair apart). |
| `stickyHeader(key = ...) { ... }` | A header that **sticks** to the top. |
| `.background(surfaceVariant)` | ⚠️ **Important!** A sticky header needs a **background**, or the items scrolling **under** it will show through. 👻 |
| `key = "header_$letter"` | Unique keys for headers too. We add `"header_"` so a header key can never be the same as an item key. |

> 💡 Yes — you **can** use `forEach` inside `LazyColumn { }`, as long as **inside the loop** you call `item`, `items`, or `stickyHeader`. You're just adding many recipes in a loop. 📝🔁

---

## 10.9 `LazyRow` — Horizontal Lists ➡️

Exactly like `LazyColumn`, but **sideways**:

```kotlin
@Composable
fun CategoryRow(categories: List<String>, modifier: Modifier = Modifier) {
    LazyRow(
        modifier = modifier,
        contentPadding = PaddingValues(horizontal = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(categories) { category ->
            AssistChip(onClick = { }, label = { Text(category) })
        }
    }
}
```

Import: `androidx.compose.foundation.lazy.LazyRow`

| `LazyColumn` | `LazyRow` |
|---|---|
| `verticalArrangement` | `horizontalArrangement` |
| `horizontalAlignment` | `verticalAlignment` |
| scrolls up/down ↕️ | scrolls left/right ↔️ |

### A very common design: rows inside a column 🎬

Netflix, YouTube, Spotify, Play Store… they all use a **`LazyColumn` of `LazyRow`s**:

```
LazyColumn  (scroll up/down)
 ├── item: Text("Trending 🔥")
 ├── item: LazyRow  [🎬][🎬][🎬][🎬] → → →
 ├── item: Text("For you ❤️")
 ├── item: LazyRow  [🎬][🎬][🎬][🎬] → → →
 └── ...
```

```kotlin
LazyColumn {
    item { Text("Trending 🔥", style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(16.dp)) }
    item { CategoryRow(trending) }
    item { Text("For you ❤️", style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(16.dp)) }
    item { CategoryRow(forYou) }
}
```

✅ This is **allowed** — the directions are **different** (vertical outside, horizontal inside).

---

## 10.10 Grids 🖼️

For **photos**, **products**, **apps**, **emojis** — use a **grid**.

### `LazyVerticalGrid` with a fixed number of columns

```kotlin
@Composable
fun EmojiGrid(emojis: List<String>, modifier: Modifier = Modifier) {
    LazyVerticalGrid(
        columns = GridCells.Fixed(3),
        modifier = modifier,
        contentPadding = PaddingValues(16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(emojis) { emoji ->
            Card(modifier = Modifier.aspectRatio(1f)) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text(emoji, fontSize = 40.sp)
                }
            }
        }
    }
}
```

Imports:

```kotlin
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
```

> ⚠️ **Import alert!** For grids, `items` comes from **`androidx.compose.foundation.lazy.grid.items`** — a **different** `items` than the one for `LazyColumn`!

| Code | Meaning |
|---|---|
| `columns = GridCells.Fixed(3)` | Always **3** columns. |
| `Modifier.aspectRatio(1f)` | Each card is a perfect **square** (Chapter 6). |

```
┌────┐ ┌────┐ ┌────┐
│ 🐶 │ │ 🐱 │ │ 🐭 │
└────┘ └────┘ └────┘
┌────┐ ┌────┐ ┌────┐
│ 🐹 │ │ 🐰 │ │ 🦊 │
└────┘ └────┘ └────┘
```

### `GridCells.Adaptive` — as many columns as fit ⭐

```kotlin
columns = GridCells.Adaptive(minSize = 100.dp)
```

- "Each cell is **at least 100 dp** wide. Fit **as many** as possible."
- Small phone → 3 columns. Big phone → 4. Tablet → 8! 📱💻
- **Great** for apps that work on every screen size.

| Columns setting | Meaning |
|---|---|
| `GridCells.Fixed(3)` | Exactly 3 columns, always |
| `GridCells.Adaptive(100.dp)` | As many as fit, each at least 100 dp |
| `GridCells.FixedSize(120.dp)` | Each column exactly 120 dp |

### A full-width header in a grid

```kotlin
LazyVerticalGrid(columns = GridCells.Fixed(3)) {
    item(span = { GridItemSpan(maxLineSpan) }) {
        Text("Animals 🐾", style = MaterialTheme.typography.titleLarge)
    }
    items(animals) { animal -> AnimalCell(animal) }
}
```

- `span = { GridItemSpan(maxLineSpan) }` → "This item takes the **whole row**."
- `maxLineSpan` = the number of columns.

Import: `androidx.compose.foundation.lazy.grid.GridItemSpan`

### Staggered grid — like Pinterest 📌

Items have **different heights**, and fill the gaps like bricks:

```kotlin
LazyVerticalStaggeredGrid(
    columns = StaggeredGridCells.Fixed(2),
    contentPadding = PaddingValues(16.dp),
    horizontalArrangement = Arrangement.spacedBy(8.dp),
    verticalItemSpacing = 8.dp
) {
    items(notes) { note ->
        Card { Text(note, modifier = Modifier.padding(12.dp)) }
    }
}
```

Imports:

```kotlin
import androidx.compose.foundation.lazy.staggeredgrid.LazyVerticalStaggeredGrid
import androidx.compose.foundation.lazy.staggeredgrid.StaggeredGridCells
import androidx.compose.foundation.lazy.staggeredgrid.items
```

```
┌──────┐ ┌──────┐
│short │ │a much│
└──────┘ │longer│
┌──────┐ │note  │
│medium│ │here  │
│note  │ └──────┘
└──────┘ ┌──────┐
         │ hi!  │
         └──────┘
```

Perfect for **notes** apps (like Google Keep 📝) and **photo** walls.

### All the lazy layouts

| Layout | Scrolls | Use for |
|---|---|---|
| `LazyColumn` | ↕️ | Most lists |
| `LazyRow` | ↔️ | Carousels, chips, stories |
| `LazyVerticalGrid` | ↕️ | Photos, products, emojis |
| `LazyHorizontalGrid` | ↔️ | Rare: horizontal grids |
| `LazyVerticalStaggeredGrid` | ↕️ | Notes, Pinterest-style walls |

---

## 10.11 Controlling Scrolling — "Back to Top" ⬆️

### The list state

```kotlin
val listState = rememberLazyListState()

LazyColumn(state = listState) { ... }
```

Import: `androidx.compose.foundation.lazy.rememberLazyListState`

`listState` **knows** about the scrolling, and can **control** it:

| Property / function | Meaning |
|---|---|
| `listState.firstVisibleItemIndex` | The index of the **top** item you can see now. |
| `listState.scrollToItem(0)` | **Jump** to the first item (instant). |
| `listState.animateScrollToItem(0)` | **Scroll smoothly** to the first item. 🎢 |

(For grids: `rememberLazyGridState()`.)

### A "back to top" button

```kotlin
@Composable
fun LongListWithTopButton(modifier: Modifier = Modifier) {
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()

    val showButton by remember {
        derivedStateOf { listState.firstVisibleItemIndex > 2 }
    }

    Box(modifier = modifier.fillMaxSize()) {
        LazyColumn(state = listState) {
            items(200) { i ->
                Text("Row $i", modifier = Modifier.padding(16.dp))
            }
        }

        if (showButton) {
            SmallFloatingActionButton(
                onClick = {
                    scope.launch { listState.animateScrollToItem(0) }
                },
                modifier = Modifier
                    .align(Alignment.BottomEnd)
                    .padding(16.dp)
            ) {
                Icon(Icons.Filled.KeyboardArrowUp, contentDescription = "Back to top")
            }
        }
    }
}
```

Imports:

```kotlin
import androidx.compose.material3.SmallFloatingActionButton
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.material.icons.filled.KeyboardArrowUp
import kotlinx.coroutines.launch
```

### Every new idea explained

**1. `derivedStateOf` — state calculated from other state**

```kotlin
    val showButton by remember {
        derivedStateOf { listState.firstVisibleItemIndex > 2 }
    }
```

- `firstVisibleItemIndex` changes **very often** while scrolling (0, 1, 2, 3, 4…).
- But `showButton` only changes **twice**: `false` → `true` when you pass item 2, and back.
- `derivedStateOf` makes Compose redraw **only when the answer (`true`/`false`) changes**, not on every tiny scroll. ⚡ Saves a lot of work!

> 💡 In Chapter 8 we said "*just calculate it*". That's still true! Use `derivedStateOf` only when the input changes **much more often** than the result — like scroll positions.

**2. `rememberCoroutineScope()` and `scope.launch { }`**

- `animateScrollToItem` takes **time** (it's an animation 🎢). In Kotlin, things that take time are called **`suspend`** functions.
- A `suspend` function can't run directly in `onClick`. It needs a **coroutine** — a task that can **wait** without freezing the app.
- `rememberCoroutineScope()` → a "**worker**" 👷 tied to this screen.
- `scope.launch { ... }` → "Worker, please **start** this task."

> ℹ️ Don't worry about coroutines now — we learn them properly in **Chapter 18**. For now, remember this recipe: **`scope.launch { listState.animateScrollToItem(0) }`**.

**3. `SmallFloatingActionButton`**

A small, round **floating** button 🔘 — it "floats" above the content. Aligned to the **bottom-right** of the `Box` (Chapter 6).

### Remember the scroll position across rotation?

`rememberLazyListState()` is already **saveable** — the scroll position survives rotation automatically! 🔄✅

---

## 10.12 Two Important Rules ⚠️

### Rule 1: Don't put a `LazyColumn` inside a scrolling `Column` ❌

```kotlin
Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
    Text("Header")
    LazyColumn { ... }      // 💥 CRASH!
}
```

Error:
> *Vertically scrollable component was measured with an infinity maximum height constraints, which is disallowed.*

**Why?** A scrolling Column says "*you can be as tall as you want*". A LazyColumn says "*I need to know how tall I am, so I know how many items to draw*". They can't agree! 🤷

**Fix ✅:** Put the header **inside** the LazyColumn as an `item`:

```kotlin
LazyColumn {
    item { Text("Header") }
    items(list) { ... }
}
```

> 💡 **One scroll, one LazyColumn.** Everything that scrolls together goes **inside** the same lazy list as `item { }`s.

### Rule 2: A `LazyColumn` needs a limited height

Inside a normal (non-scrolling) `Column`, give it `Modifier.weight(1f)` or `fillMaxSize()`, so it knows how much space it has:

```kotlin
Column(modifier = Modifier.fillMaxSize()) {
    SearchBox()                                     // fixed at the top
    LazyColumn(modifier = Modifier.weight(1f)) {    // takes the rest ✅
        items(results) { ... }
    }
}
```

This is how you make a **search box that stays on top** while the list scrolls below it. We'll use exactly this in the project! 🔍

---

## 10.13 Empty Lists 🫙

What if the list is **empty**? A blank screen is confusing: "*Is it loading? Is it broken?*" 😕

Always show a **friendly message**:

```kotlin
if (todos.isEmpty()) {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text("🎉", fontSize = 64.sp)
            Text("No tasks! Enjoy your day.", style = MaterialTheme.typography.titleMedium)
        }
    }
} else {
    LazyColumn { ... }
}
```

This is called an **empty state**. Good apps always have one. ✨

---

## 10.14 Build It: A Contacts App 📇🔍

Let's build a contacts app with:

- 🔍 A **search box** that filters as you type
- ⭐ A horizontal row of **favorites**
- 🔤 Contacts **grouped by letter** with **sticky headers**
- 👆 **Tap** a star to add/remove a favorite
- ⬆️ A **back-to-top** button
- 🫙 An **empty state** when nothing matches

```
┌──────────────────────────────────┐
│ Contacts                    (32) │
│ ┌ 🔍 Search ─────────────────┐   │  ← stays on top
│                                  │
│ Favorites ⭐                     │
│ (A) (B) (M) (Z) → →              │  ← LazyRow
│ ┌──────────────────────────────┐ │
│ │ A                            │ │  ← sticky header
│ ├──────────────────────────────┤ │
│ │ (A) Aarav Mehta          ☆   │ │
│ │     +91 98765 00001          │ │
│ │ (A) Amara Okafor         ★   │ │
│ │ B                            │ │
│ │ (B) Ben Carter           ☆   │ │
│ │ ...                     (⬆)  │ │  ← back to top
└──────────────────────────────────┘
```

### The full code

Replace **everything** in `MainActivity.kt` (keep your own `package` line and theme import):

```kotlin
package com.example.myfirstapp

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SmallFloatingActionButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.myfirstapp.ui.theme.MyFirstAppTheme
import kotlinx.coroutines.launch

// ---------- Data ----------

data class Contact(
    val id: Int,
    val name: String,
    val phone: String,
    val isFavorite: Boolean = false
)

private val sampleNames = listOf(
    "Aarav Mehta", "Amara Okafor", "Ana Souza", "Ben Carter", "Bianca Rossi",
    "Carlos Diaz", "Chen Wei", "Chloe Martin", "Daniel Kim", "Diya Sharma",
    "Elena Petrova", "Ethan Brooks", "Fatima Khan", "Felix Weber", "Grace Lee",
    "Hana Sato", "Hugo Dubois", "Isla Murphy", "Ivan Novak", "Jamal Ali",
    "Julia Santos", "Kenji Tanaka", "Lara Nguyen", "Leo Fischer", "Maya Patel",
    "Mohammed Hassan", "Nina Larsen", "Omar Farouk", "Priya Nair", "Rosa Garcia",
    "Sofia Rossi", "Zara Ahmed"
)

fun sampleContacts(): List<Contact> =
    sampleNames.mapIndexed { index, name ->
        Contact(
            id = index + 1,
            name = name,
            phone = "+1 555 01${(index + 1).toString().padStart(2, '0')}",
            isFavorite = index % 7 == 1
        )
    }

private val avatarColors = listOf(
    Color(0xFFE57373), Color(0xFF64B5F6), Color(0xFF81C784),
    Color(0xFFFFB74D), Color(0xFFBA68C8), Color(0xFF4DB6AC)
)

fun avatarColorFor(id: Int): Color = avatarColors[id % avatarColors.size]

// ---------- Activity ----------

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyFirstAppTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    ContactsScreen(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

// ---------- Screen ----------

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun ContactsScreen(modifier: Modifier = Modifier) {
    // State
    var contacts by remember { mutableStateOf(sampleContacts()) }
    var query by rememberSaveable { mutableStateOf("") }

    // Calculated from state
    val filtered = contacts.filter { it.name.contains(query.trim(), ignoreCase = true) }
    val favorites = contacts.filter { it.isFavorite }
    val grouped = filtered
        .sortedBy { it.name }
        .groupBy { it.name.first().uppercaseChar() }

    // Scrolling
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()
    val showTopButton by remember {
        derivedStateOf { listState.firstVisibleItemIndex > 3 }
    }

    val context = LocalContext.current

    // Events
    val toggleFavorite: (Contact) -> Unit = { contact ->
        contacts = contacts.map {
            if (it.id == contact.id) it.copy(isFavorite = !it.isFavorite) else it
        }
    }
    val openContact: (Contact) -> Unit = { contact ->
        Toast.makeText(context, "Calling ${contact.name}... 📞", Toast.LENGTH_SHORT).show()
    }

    Column(modifier = modifier.fillMaxSize()) {
        // ---- Fixed top part ----
        Row(
            modifier = Modifier.padding(start = 16.dp, end = 16.dp, top = 16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "Contacts",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.weight(1f)
            )
            Text(
                text = "${filtered.size}",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        SearchBox(
            query = query,
            onQueryChange = { query = it },
            modifier = Modifier.padding(16.dp)
        )

        // ---- Scrolling part ----
        Box(modifier = Modifier.weight(1f)) {
            if (filtered.isEmpty()) {
                EmptyResults(query = query)
            } else {
                LazyColumn(
                    state = listState,
                    contentPadding = PaddingValues(bottom = 80.dp),
                    modifier = Modifier.fillMaxSize()
                ) {
                    if (query.isBlank() && favorites.isNotEmpty()) {
                        item(key = "favorites") {
                            FavoritesRow(favorites = favorites, onClick = openContact)
                        }
                    }

                    grouped.forEach { (letter, contactsForLetter) ->
                        stickyHeader(key = "header_$letter") {
                            LetterHeader(letter)
                        }
                        items(contactsForLetter, key = { it.id }) { contact ->
                            ContactRow(
                                contact = contact,
                                onClick = { openContact(contact) },
                                onToggleFavorite = { toggleFavorite(contact) },
                                modifier = Modifier.animateItem()
                            )
                        }
                    }
                }
            }

            if (showTopButton && filtered.isNotEmpty()) {
                SmallFloatingActionButton(
                    onClick = { scope.launch { listState.animateScrollToItem(0) } },
                    modifier = Modifier
                        .align(Alignment.BottomEnd)
                        .padding(16.dp)
                ) {
                    Icon(Icons.Filled.KeyboardArrowUp, contentDescription = "Back to top")
                }
            }
        }
    }
}

// ---------- Parts ----------

@Composable
fun SearchBox(query: String, onQueryChange: (String) -> Unit, modifier: Modifier = Modifier) {
    OutlinedTextField(
        value = query,
        onValueChange = onQueryChange,
        placeholder = { Text("Search contacts") },
        leadingIcon = { Icon(Icons.Filled.Search, contentDescription = null) },
        trailingIcon = {
            if (query.isNotEmpty()) {
                IconButton(onClick = { onQueryChange("") }) {
                    Icon(Icons.Filled.Clear, contentDescription = "Clear search")
                }
            }
        },
        singleLine = true,
        shape = MaterialTheme.shapes.extraLarge,
        modifier = modifier.fillMaxWidth()
    )
}

@Composable
fun Avatar(name: String, color: Color, size: Int, modifier: Modifier = Modifier) {
    Box(
        modifier = modifier
            .size(size.dp)
            .background(color, CircleShape),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = name.first().uppercase(),
            color = Color.White,
            fontWeight = FontWeight.Bold,
            fontSize = (size / 2.4).sp
        )
    }
}

@Composable
fun FavoritesRow(
    favorites: List<Contact>,
    onClick: (Contact) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.padding(bottom = 8.dp)) {
        Text(
            text = "Favorites ⭐",
            style = MaterialTheme.typography.titleSmall,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
        )
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            items(favorites, key = { it.id }) { contact ->
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .widthIn(max = 72.dp)
                        .clickable { onClick(contact) }
                ) {
                    Avatar(contact.name, avatarColorFor(contact.id), size = 56)
                    Text(
                        text = contact.name.substringBefore(" "),
                        style = MaterialTheme.typography.labelMedium,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        textAlign = TextAlign.Center
                    )
                }
            }
        }
    }
}

@Composable
fun LetterHeader(letter: Char, modifier: Modifier = Modifier) {
    Text(
        text = letter.toString(),
        style = MaterialTheme.typography.titleSmall,
        fontWeight = FontWeight.Bold,
        color = MaterialTheme.colorScheme.primary,
        modifier = modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.surfaceContainerHighest)
            .padding(horizontal = 16.dp, vertical = 6.dp)
    )
}

@Composable
fun ContactRow(
    contact: Contact,
    onClick: () -> Unit,
    onToggleFavorite: () -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(start = 16.dp, top = 8.dp, bottom = 8.dp, end = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Avatar(contact.name, avatarColorFor(contact.id), size = 44)
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(contact.name, style = MaterialTheme.typography.bodyLarge)
            Text(
                text = contact.phone,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        IconButton(onClick = onToggleFavorite) {
            Icon(
                imageVector = Icons.Filled.Star,
                contentDescription = if (contact.isFavorite) "Remove from favorites" else "Add to favorites",
                tint = if (contact.isFavorite) Color(0xFFFFB300) else MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
fun EmptyResults(query: String, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(32.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("🔍", fontSize = 64.sp)
        Text(
            text = "No contacts found",
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold
        )
        Text(
            text = "Nobody matches \"$query\". Try another name.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center
        )
    }
}

// ---------- Preview ----------

@Preview(showBackground = true, showSystemUi = true)
@Composable
fun ContactsPreview() {
    MyFirstAppTheme {
        Surface {
            ContactsScreen()
        }
    }
}
```

> ⚠️ Keep **your own** `package` line and theme import.
> ℹ️ We use the same `Icons.Filled.Star` for both states and only change its **color**: gold ★ for favorites, grey for the others. (A hollow star ☆ icon, `Icons.Filled.StarBorder`, is only in the **extended** icon library.)

### Every part explained

#### Part 1: Making sample data with `mapIndexed`

```kotlin
fun sampleContacts(): List<Contact> =
    sampleNames.mapIndexed { index, name ->
        Contact(
            id = index + 1,
            name = name,
            phone = "+1 555 01${(index + 1).toString().padStart(2, '0')}",
            isFavorite = index % 7 == 1
        )
    }
```

| Code | Meaning |
|---|---|
| `mapIndexed { index, name -> }` | Like `map` (Chapter 3), but also gives the **position**. Turns 32 names into 32 `Contact` objects. |
| `id = index + 1` | Unique ids: 1, 2, 3… → perfect **keys** 🔑. |
| `padStart(2, '0')` | `7` → `"07"`, so phone numbers look neat: `+1 555 0107`. |
| `isFavorite = index % 7 == 1` | A few contacts start as favorites (every 7th one), just for the demo. |

```kotlin
fun avatarColorFor(id: Int): Color = avatarColors[id % avatarColors.size]
```

- `%` (remainder) **cycles** through 6 colors: id 1 → color 1, id 7 → color 1 again… 🎨 Each contact always gets the **same** color.

#### Part 2: State vs calculated values

```kotlin
    var contacts by remember { mutableStateOf(sampleContacts()) }
    var query by rememberSaveable { mutableStateOf("") }
```

Only **2** pieces of state: the contacts and the search text. **Everything else is calculated:**

```kotlin
    val filtered = contacts.filter { it.name.contains(query.trim(), ignoreCase = true) }
    val favorites = contacts.filter { it.isFavorite }
    val grouped = filtered
        .sortedBy { it.name }
        .groupBy { it.name.first().uppercaseChar() }
```

| Value | Meaning |
|---|---|
| `filtered` | Contacts whose name **contains** the search text. `ignoreCase = true` → "asha" finds "Asha". |
| `favorites` | Only the starred ones. |
| `grouped` | Sorted A→Z, then grouped by first letter: `{'A'=[...], 'B'=[...]}`. |

Type a letter → `query` changes → recomposition → `filtered` and `grouped` are recalculated → the list updates. **Live search with no extra code!** ✨🔍

#### Part 3: Events stored in `val`s

```kotlin
    val toggleFavorite: (Contact) -> Unit = { contact ->
        contacts = contacts.map {
            if (it.id == contact.id) it.copy(isFavorite = !it.isFavorite) else it
        }
    }
```

- A **lambda in a `val`** (Chapter 3), with the type `(Contact) -> Unit`.
- The **update pattern** from 10.7: `map` + `copy`.
- We give this lambda a name because **two** places use the same idea. Clean code! 🧹

#### Part 4: Fixed top + scrolling list (Rule 2!)

```kotlin
    Column(modifier = modifier.fillMaxSize()) {
        Row { /* title + count */ }
        SearchBox(...)                         // stays on top
        Box(modifier = Modifier.weight(1f)) {  // takes the rest
            LazyColumn(...) { ... }
            SmallFloatingActionButton(...)     // floats above the list
        }
    }
```

- The title and search box are **outside** the LazyColumn → they **don't** scroll away. 📌
- `Box(weight(1f))` → the list area takes all the space below (Rule 2 from 10.12).
- Inside the `Box`, the floating button sits **on top** of the list (Chapter 6: last child on top).

#### Part 5: Inside the LazyColumn

```kotlin
                    if (query.isBlank() && favorites.isNotEmpty()) {
                        item(key = "favorites") {
                            FavoritesRow(...)
                        }
                    }
```

- The **favorites row** is shown only when **not** searching. You can use `if` inside `LazyColumn { }` too!
- `FavoritesRow` contains a **`LazyRow`** → a horizontal list **inside** a vertical one. ✅ Allowed (different directions).

```kotlin
                    grouped.forEach { (letter, contactsForLetter) ->
                        stickyHeader(key = "header_$letter") { LetterHeader(letter) }
                        items(contactsForLetter, key = { it.id }) { contact ->
                            ContactRow(..., modifier = Modifier.animateItem())
                        }
                    }
```

- For each letter: a **sticky header** + the contacts for that letter.
- **Keys everywhere**: `"favorites"`, `"header_A"`, and the contact ids. All **unique**. 🔑
- `animateItem()` → when searching, rows **slide** nicely. ✨

#### Part 6: `Avatar` — initials in a colored circle

```kotlin
@Composable
fun Avatar(name: String, color: Color, size: Int, modifier: Modifier = Modifier) {
    Box(
        modifier = modifier.size(size.dp).background(color, CircleShape),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = name.first().uppercase(),
            fontSize = (size / 2.4).sp,
            ...
        )
    }
}
```

- Used **twice** with different sizes: 56 in favorites, 44 in rows. ♻️
- `size.dp` → turns an `Int` into `dp`. `(size / 2.4).sp` → the letter grows with the circle.
- `name.first().uppercase()` → `"Ben Carter"` → `"B"`.

#### Part 7: `FavoritesRow` details

```kotlin
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .widthIn(max = 72.dp)
                        .clickable { onClick(contact) }
                ) { ... }
```

- `widthIn(max = 72.dp)` → each favorite is at most 72 dp wide (Chapter 6).
- `contact.name.substringBefore(" ")` → only the **first name**: `"Amara Okafor"` → `"Amara"`.

#### Part 8: `LetterHeader` — a sticky header with a background

```kotlin
        modifier = modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.surfaceContainerHighest)
            .padding(...)
```

- The **background** stops rows from showing through when they scroll under it (10.8). 👻🚫
- `surfaceContainerHighest` → a theme color for a slightly stronger surface (Chapter 7).

#### Part 9: `EmptyResults` — the empty state

When the search finds **nothing**, we show 🔍 "No contacts found" with the search text. Friendly and clear. 😊

### Run it! ▶️

1. **Scroll** — watch the letters **stick** to the top. 📌
2. Tap a **☆** — it becomes **★**, and the contact appears in **Favorites**!
3. Type **"ro"** in search → only matching names, live. 🔍
4. Type **"xyz"** → the empty state appears.
5. Clear the search with **✖️**.
6. Scroll down a lot → tap **⬆️** → smooth scroll back to the top. 🎢
7. **Rotate** → the search text and scroll position are kept. 🔄

---

## 10.15 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| `Text(...)` directly inside `LazyColumn { }` | *@Composable invocations can only happen from the context of a @Composable function* | Wrap it: `item { Text(...) }`. |
| `items(myList)` shows a type error | *Type mismatch: inferred type is List<...> but Int was expected* | Import `androidx.compose.foundation.lazy.items`. |
| Using LazyColumn's `items` in a grid | Type error | Grids need `androidx.compose.foundation.lazy.grid.items`. |
| `LazyColumn` inside `verticalScroll` Column | 💥 *...infinity maximum height constraints...* | Put headers inside the LazyColumn as `item { }`. |
| `LazyColumn` in a `Column` takes no space / pushes things off | No height limit | Give it `Modifier.weight(1f)`. |
| Two items with the same key | 💥 *Key "x" was already used* | Make keys unique (use ids; prefix header keys). |
| Using the index as the key | State jumps to the wrong row | Use a stable `id`. |
| `Modifier.padding` on a LazyColumn | Items cut off at the edges when scrolling | Use `contentPadding = PaddingValues(...)`. |
| Sticky header is see-through | Rows show through it 👻 | Give the header a `background(...)`. |
| `animateScrollToItem` in `onClick` | *Suspend function should be called only from a coroutine* | `scope.launch { ... }` with `rememberCoroutineScope()`. |
| Changing a `mutableListOf` inside state | List doesn't update | Use `list + x`, `filter`, `map` + `copy`. |
| Blank screen when the list is empty | Users are confused | Show an **empty state**. |

---

## 10.16 Summary — What You Learned 🎓

✅ **Lazy lists** draw only what's visible → fast for any size. `Column` + `forEach` only for small lists.

✅ **`LazyColumn { }`** is a special area: use `item { }`, `items(count)`, `items(list)`, `itemsIndexed(list)`.

✅ **`contentPadding`** (not `Modifier.padding`) and **`verticalArrangement = spacedBy(...)`** for spacing.

✅ **Keys** (`key = { it.id }`) keep state with the right item, and enable **`Modifier.animateItem()`**.

✅ **List changes:** add with `+`, remove with `filter`, update with `map` + `copy`.

✅ **Headers:** `item { }`; **sticky headers:** `stickyHeader { }` with a background.

✅ **`LazyRow`** for horizontal lists; rows inside a column are fine.

✅ **Grids:** `LazyVerticalGrid` with `GridCells.Fixed` / `Adaptive`, full-width items with `GridItemSpan(maxLineSpan)`, and `LazyVerticalStaggeredGrid`.

✅ **Scroll control:** `rememberLazyListState()`, `firstVisibleItemIndex`, `animateScrollToItem` inside `scope.launch { }`, and `derivedStateOf`.

✅ **Rules:** no LazyColumn in a scrolling Column; give it `weight(1f)` in a Column; always have an **empty state**.

✅ You built a **Contacts app** with search, favorites, sticky headers, and back-to-top! 📇

---

## 10.17 Practice Time 🏋️

**Task 1 — Numbers:**
A `LazyColumn` showing `"1 × 7 = 7"` up to `"100 × 7 = 700"`, with 16 dp padding around the list (use `contentPadding`) and a divider between rows (none after the last).

**Task 2 — Movie cards:**
Make `data class Movie(val id: Int, val title: String, val year: Int, val emoji: String)`. Show 8 movies as `ElevatedCard`s in a `LazyColumn` with 12 dp between cards. Each card shows the emoji, title (bold), and year.

**Task 3 — Emoji grid:**
A `LazyVerticalGrid` with `GridCells.Adaptive(80.dp)` showing 40 emojis in square cards. Tapping one shows a Toast with that emoji.

**Task 4 — Remove on tap:**
A list of 10 fruits. Each row has a 🗑️ button that removes it (with `animateItem()`). Show `"All fruits eaten! 🍽️"` when the list is empty, and a **Reset** button.

**Task 5 — Netflix style:**
A `LazyColumn` with 3 sections ("Action 💥", "Comedy 😂", "Cartoons 🐭"). Each section has a title and a `LazyRow` of 10 colored boxes (120 × 80 dp) labelled `"Movie 1"` … `"Movie 10"`.

**Task 6 — Thinking question 🤔:**
In the Contacts app, why is `filtered` **not** a state with `remember`? What would go wrong if it were?

---

### Answers

**Task 1:**

```kotlin
@Composable
fun TimesSeven(modifier: Modifier = Modifier) {
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp)
    ) {
        items(100) { index ->
            val n = index + 1
            Text(
                text = "$n × 7 = ${n * 7}",
                modifier = Modifier.padding(vertical = 12.dp)
            )
            if (n < 100) {
                HorizontalDivider()
            }
        }
    }
}
```

**Task 2:**

```kotlin
data class Movie(val id: Int, val title: String, val year: Int, val emoji: String)

val movies = listOf(
    Movie(1, "Space Cats", 2021, "🐱"),
    Movie(2, "The Lost Map", 2019, "🗺️"),
    Movie(3, "Robot Friend", 2023, "🤖"),
    Movie(4, "Ocean Deep", 2018, "🌊"),
    Movie(5, "Dragon School", 2022, "🐉"),
    Movie(6, "Pizza Wars", 2020, "🍕"),
    Movie(7, "Mountain Run", 2017, "🏔️"),
    Movie(8, "Night Garden", 2024, "🌙")
)

@Composable
fun MovieList(modifier: Modifier = Modifier) {
    LazyColumn(
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        items(movies, key = { it.id }) { movie ->
            ElevatedCard(modifier = Modifier.fillMaxWidth()) {
                Row(
                    modifier = Modifier.padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(movie.emoji, fontSize = 36.sp)
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text(movie.title, fontWeight = FontWeight.Bold)
                        Text("${movie.year}", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
    }
}
```

**Task 3:**

```kotlin
@Composable
fun EmojiPicker(modifier: Modifier = Modifier) {
    val emojis = listOf(
        "😀", "😂", "😍", "🤔", "😎", "😴", "🥳", "😇", "🤖", "👻",
        "🐶", "🐱", "🦊", "🐼", "🐸", "🐵", "🦁", "🐯", "🐨", "🐷",
        "🍎", "🍌", "🍇", "🍓", "🍕", "🍔", "🍩", "🍪", "🍉", "🥑",
        "⚽", "🏀", "🎸", "🎮", "🚀", "🌈", "⭐", "🔥", "💧", "🌙"
    )
    val context = LocalContext.current

    LazyVerticalGrid(
        columns = GridCells.Adaptive(80.dp),
        modifier = modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(emojis) { emoji ->
            Card(
                onClick = { Toast.makeText(context, "You picked $emoji", Toast.LENGTH_SHORT).show() },
                modifier = Modifier.aspectRatio(1f)
            ) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text(emoji, fontSize = 36.sp)
                }
            }
        }
    }
}
```

Remember: `items` from **`androidx.compose.foundation.lazy.grid`**! (Each emoji is unique, so no key is needed — the list never changes.)

**Task 4:**

```kotlin
@Composable
fun FruitEater(modifier: Modifier = Modifier) {
    val startFruits = listOf(
        "Apple 🍎", "Banana 🍌", "Cherry 🍒", "Grape 🍇", "Kiwi 🥝",
        "Lemon 🍋", "Mango 🥭", "Orange 🍊", "Peach 🍑", "Pear 🍐"
    )
    var fruits by rememberSaveable { mutableStateOf(startFruits) }

    Column(modifier = modifier.fillMaxSize()) {
        TextButton(onClick = { fruits = startFruits }, modifier = Modifier.padding(8.dp)) {
            Text("Reset")
        }
        if (fruits.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("All fruits eaten! 🍽️", style = MaterialTheme.typography.titleLarge)
            }
        } else {
            LazyColumn(modifier = Modifier.weight(1f)) {
                items(fruits, key = { it }) { fruit ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .animateItem()
                            .padding(start = 16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(fruit, modifier = Modifier.weight(1f))
                        IconButton(onClick = { fruits = fruits - fruit }) {
                            Icon(Icons.Filled.Delete, contentDescription = "Eat $fruit")
                        }
                    }
                }
            }
        }
    }
}
```

Here the fruit **names** are unique, so `key = { it }` is fine. (A `List<String>` can be saved by `rememberSaveable`. ✅)

**Task 5:**

```kotlin
@Composable
fun StreamingHome(modifier: Modifier = Modifier) {
    val sections = listOf(
        "Action 💥" to Color(0xFFE53935),
        "Comedy 😂" to Color(0xFFFFB300),
        "Cartoons 🐭" to Color(0xFF1E88E5)
    )

    LazyColumn(modifier = modifier.fillMaxSize()) {
        sections.forEach { (title, color) ->
            item(key = title) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleLarge,
                    modifier = Modifier.padding(16.dp)
                )
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(10) { i ->
                        Box(
                            modifier = Modifier
                                .size(width = 120.dp, height = 80.dp)
                                .background(color, RoundedCornerShape(8.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("Movie ${i + 1}", color = Color.White)
                        }
                    }
                }
            }
        }
    }
}
```

`"Action 💥" to Color(...)` makes a **Pair** (Chapter 4), and `(title, color)` takes it apart.

**Task 6:**
`filtered` can be **calculated** from `contacts` and `query`. If it were its own state, we'd have to update it **by hand** every time the user types **and** every time a favorite changes. Forget once → the list shows **old** data. 🐛 Calculating it means it's **always right**. ✅

---

## 10.18 What Is Next?

In **Chapter 11: Screen Frames and Pop-ups**, you will learn the full power of **`Scaffold`**:

- **`TopAppBar`** — the bar at the top with a title and buttons 🔝
- **Bottom bars** and **navigation bars** 🔽
- **Floating action buttons** (FAB) ➕
- **Snackbars** — small messages with an "Undo" button ↩️
- **Dialogs** — "Are you sure?" pop-ups ❓
- **Bottom sheets** — panels that slide up from the bottom 📤
- **Menus** — the ⋮ "more options" menu

**Great job finishing Chapter 10! 🎉 Your apps can now handle thousands of items!**
