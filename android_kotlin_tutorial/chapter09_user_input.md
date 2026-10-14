# Chapter 9: Getting Input From the User — Text Fields, Checkboxes, Sliders, and Forms

> **What you will learn in this chapter**
>
> 1. `TextField` and `OutlinedTextField` — letting the user **type** ⌨️
> 2. Labels, placeholders, icons, and helper text
> 3. Choosing the right **keyboard** (numbers, email, phone…)
> 4. The keyboard's action button: **Next** ➡️ and **Done** ✅
> 5. **Password** fields with show/hide 🔒
> 6. Checking input and showing **errors** ❌
> 7. Allowing only certain characters (like digits only)
> 8. `Checkbox`, `RadioButton`, `Switch`, `Slider`
> 9. **Chips** — small choice buttons 🏷️
> 10. **Dropdown menus** — pick one from a list
> 11. Making the keyboard **not cover** your fields
> 12. Building a full **Sign-Up form** 📝
>
> **Time needed:** about 4 to 5 hours.
>
> **Before you start:** This chapter uses **state** and **hoisting** from Chapter 8 everywhere. If something feels unclear, look back at sections 8.5 and 8.10. 👀

---

## 9.1 Your First Text Field ⌨️

A **text field** is a box where the user can **type** text: a name, an email, a message, a search word…

```kotlin
@Composable
fun NameInput(modifier: Modifier = Modifier) {
    var name by remember { mutableStateOf("") }

    Column(modifier = modifier.padding(16.dp)) {
        TextField(
            value = name,
            onValueChange = { newText -> name = newText },
            label = { Text("Your name") }
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text("Hello, $name! 👋")
    }
}
```

Imports:

```kotlin
import androidx.compose.material3.TextField
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
```

**Run the app** and type. The "Hello" text updates **with every letter**! ✨

### Every bit explained

| Piece | Meaning |
|---|---|
| `var name by remember { mutableStateOf("") }` | The **state**: what the user typed. Starts **empty** (`""`). |
| `TextField(` | A Material text field. |
| `value = name` | **Show** this text in the box. (state ⬇️) |
| `onValueChange = { newText -> name = newText }` | When the user types, the field **tells us** the new full text. **We** save it. (event ⬆️) |
| `label = { Text("Your name") }` | A small title for the field. It's a **lambda** (it can hold any Composable). |

### 🤔 Why doesn't the text field remember the text by itself?

Remember the `Switch` in Chapter 8? `TextField` works **the same way**: it's **stateless**. It only **shows** `value` and **reports** changes.

**Try this experiment** — forget to save the text:

```kotlin
TextField(
    value = name,
    onValueChange = { }     // ❌ we ignore the new text
)
```

Now when you type… **nothing appears!** 😮 The field asked "*Can I change to 'R'?*", we said nothing, so it keeps showing the old `value`.

This is actually **powerful**: **we** are in control. We can **change**, **limit**, or **reject** what the user types (see 9.7). 💪

### Shorter: use `it`

```kotlin
onValueChange = { name = it }
```

`it` = the new text (one input → `it`, Chapter 3). You'll see this style everywhere.

---

## 9.2 `TextField` vs `OutlinedTextField` 🔲

Material 3 has **two** styles:

```kotlin
TextField(
    value = text1,
    onValueChange = { text1 = it },
    label = { Text("Filled") }
)

OutlinedTextField(
    value = text2,
    onValueChange = { text2 = it },
    label = { Text("Outlined") }
)
```

| Style | Looks like | Use when |
|---|---|---|
| `TextField` | A **filled** box with a line at the bottom | Forms with few fields; strong look |
| `OutlinedTextField` | A **border** all around | Long forms; a cleaner, lighter look |

Both have **exactly the same inputs**. Pick one style and **use it everywhere** in your app for a neat look. In this book we'll mostly use `OutlinedTextField`.

---

## 9.3 Making Text Fields Better ✨

Text fields have **many** optional inputs. Here are the most useful ones:

```kotlin
OutlinedTextField(
    value = email,
    onValueChange = { email = it },
    label = { Text("Email") },
    placeholder = { Text("example@mail.com") },
    leadingIcon = { Icon(Icons.Filled.Email, contentDescription = null) },
    supportingText = { Text("We'll never share your email.") },
    singleLine = true,
    modifier = Modifier.fillMaxWidth()
)
```

```
 ┌ Email ─────────────────────────┐
 │ ✉️  example@mail.com            │   ← placeholder (grey, disappears when typing)
 └────────────────────────────────┘
   We'll never share your email.      ← supporting text
```

### All the useful inputs

| Input | Example | What it does |
|---|---|---|
| `label` | `{ Text("Email") }` | Title. It **moves up** to the border when the user taps the field. ✨ |
| `placeholder` | `{ Text("example@mail.com") }` | Grey **hint** text, shown only when the field is **empty** and focused. |
| `leadingIcon` | `{ Icon(Icons.Filled.Email, null) }` | An icon at the **start** (left). |
| `trailingIcon` | `{ IconButton(...) { Icon(...) } }` | An icon or button at the **end** (right). |
| `prefix` | `{ Text("$") }` | Fixed text **before** the input: `$ 25` |
| `suffix` | `{ Text("kg") }` | Fixed text **after** the input: `70 kg` |
| `supportingText` | `{ Text("Help text") }` | Small text **under** the field (help or error). |
| `isError` | `true` | Makes the field **red** ❌. |
| `singleLine` | `true` | Only **one** line. The Enter key won't add a new line. |
| `maxLines` | `4` | For longer text, like a message. Grows up to 4 lines, then scrolls. |
| `minLines` | `3` | Starts at least 3 lines tall. |
| `enabled` | `false` | Greyed out, can't type. |
| `readOnly` | `true` | Can select and copy, but not change. |
| `textStyle` | `MaterialTheme.typography.titleLarge` | Style of the typed text. |

### A clear button ✖️ (trailing icon)

```kotlin
OutlinedTextField(
    value = search,
    onValueChange = { search = it },
    label = { Text("Search") },
    leadingIcon = { Icon(Icons.Filled.Search, contentDescription = null) },
    trailingIcon = {
        if (search.isNotEmpty()) {
            IconButton(onClick = { search = "" }) {
                Icon(Icons.Filled.Clear, contentDescription = "Clear text")
            }
        }
    },
    singleLine = true,
    modifier = Modifier.fillMaxWidth()
)
```

- The ✖️ button appears **only** when there is text (`if (search.isNotEmpty())`).
- Tapping it sets `search = ""` → the field is **empty** again. Because **we** own the state, clearing is **one line**! 🎉

### A message box (many lines)

```kotlin
OutlinedTextField(
    value = message,
    onValueChange = { message = it },
    label = { Text("Your message") },
    minLines = 3,
    maxLines = 6,
    supportingText = { Text("${message.length} / 200") },
    modifier = Modifier.fillMaxWidth()
)
```

- `supportingText` shows a **live counter**: `42 / 200`. It's calculated from the state! ✨

---

## 9.4 Choosing the Right Keyboard 📱⌨️

When the user taps a field, a keyboard appears. You can choose **which kind** of keyboard!

```kotlin
OutlinedTextField(
    value = phone,
    onValueChange = { phone = it },
    label = { Text("Phone number") },
    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone),
    singleLine = true
)
```

Imports:

```kotlin
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.text.input.KeyboardType
```

### Keyboard types

| `KeyboardType` | Keyboard shows | Use for |
|---|---|---|
| `Text` (default) | Normal letters | Names, messages |
| `Number` | Only **digits** 0–9 | Age, quantity, PIN |
| `Decimal` | Digits **and** a dot | Price, weight (`72.5`) |
| `Phone` | A phone keypad 📞 | Phone numbers |
| `Email` | Letters **and** an easy `@` key | Email addresses |
| `Password` | Letters, no suggestions | Passwords |
| `NumberPassword` | Digits, hidden | PIN codes |
| `Uri` | Letters with `/` and `.com` keys | Website addresses |

> 💡 The right keyboard makes your app **much** easier to use. Nobody likes searching for `@` on a keyboard! 😅

### Capital letters automatically

```kotlin
keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Words)
```

| `KeyboardCapitalization` | Result |
|---|---|
| `None` | no automatic capitals |
| `Characters` | ALL CAPITALS |
| `Words` | Every New Word (good for **names**) |
| `Sentences` | First letter of each sentence (good for **messages**) |

Import: `androidx.compose.ui.text.input.KeyboardCapitalization`

---

## 9.5 The Keyboard's Action Button: Next and Done ➡️✅

The bottom-right key of the keyboard can change! It's called the **IME action** (IME = **I**nput **M**ethod **E**ditor = the keyboard).

```kotlin
OutlinedTextField(
    value = firstName,
    onValueChange = { firstName = it },
    label = { Text("First name") },
    singleLine = true,
    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next)
)
```

Import: `androidx.compose.ui.text.input.ImeAction`

| `ImeAction` | Key shows | Normal use |
|---|---|---|
| `ImeAction.Next` | ➡️ | Go to the **next** field |
| `ImeAction.Done` | ✅ | Finished — **close** the keyboard |
| `ImeAction.Search` | 🔍 | Start a search |
| `ImeAction.Send` | ➤ | Send a message |
| `ImeAction.Go` | Go | Go to a website |

### What happens when the user presses it?

- With `singleLine = true`, **Next** automatically moves to the **next** field, and **Done** closes the keyboard. 👍
- To do **your own** thing, use `keyboardActions`:

```kotlin
val focusManager = LocalFocusManager.current

OutlinedTextField(
    value = searchText,
    onValueChange = { searchText = it },
    label = { Text("Search") },
    singleLine = true,
    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
    keyboardActions = KeyboardActions(
        onSearch = {
            Log.d("Search", "Searching for: $searchText")
            focusManager.clearFocus()        // hide the keyboard
        }
    )
)
```

Imports:

```kotlin
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.ui.platform.LocalFocusManager
```

| Code | Meaning |
|---|---|
| `LocalFocusManager.current` | A helper that controls **focus** — which field is "active" (has the blinking cursor). |
| `KeyboardActions(onSearch = { ... })` | What to do when the 🔍 key is pressed. Also: `onDone`, `onNext`, `onSend`, `onGo`. |
| `focusManager.clearFocus()` | "No field is active anymore" → the **keyboard closes**. ⌨️⬇️ |

### Combine many keyboard options

```kotlin
keyboardOptions = KeyboardOptions(
    keyboardType = KeyboardType.Email,
    imeAction = ImeAction.Next
)
```

---

## 9.6 Password Fields 🔒

A password should be **hidden**: `••••••••`.

```kotlin
@Composable
fun PasswordField(
    password: String,
    onPasswordChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    var visible by remember { mutableStateOf(false) }

    OutlinedTextField(
        value = password,
        onValueChange = onPasswordChange,
        label = { Text("Password") },
        leadingIcon = { Icon(Icons.Filled.Lock, contentDescription = null) },
        trailingIcon = {
            TextButton(onClick = { visible = !visible }) {
                Text(if (visible) "Hide" else "Show")
            }
        },
        visualTransformation = if (visible) {
            VisualTransformation.None
        } else {
            PasswordVisualTransformation()
        },
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
        singleLine = true,
        modifier = modifier.fillMaxWidth()
    )
}
```

Imports:

```kotlin
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
```

### Every bit explained

| Code | Meaning |
|---|---|
| `password: String, onPasswordChange: (String) -> Unit` | **Hoisted**! The parent owns the password (it needs it to sign up). |
| `var visible by remember { ... }` | **Local** state — only this field cares whether the password is shown. It's OK to keep it inside. |
| `onValueChange = onPasswordChange` | Pass the parent's lambda straight to the field. |
| `visualTransformation` | Changes **how the text looks**, **not** the real text. |
| `PasswordVisualTransformation()` | Shows every letter as `•`. |
| `VisualTransformation.None` | Shows the real letters. |
| `TextButton(...) { Text(if (visible) "Hide" else "Show") }` | A small button at the end to switch. 👁️ |

> 💡 **The real value doesn't change** — `password` is still `"secret123"`. Only the **display** is `•••••••••`. Like dark sunglasses 🕶️: the world is the same, it just looks different.

> ℹ️ **Want an eye icon 👁️ instead of "Show"?** The eye icons (`Icons.Filled.Visibility`, `VisibilityOff`) are in the **extended** icon library (`material-icons-extended`, Chapter 5). Text works just as well and keeps your app small.

---

## 9.7 Controlling What the User Can Type 🛂

Because **we** decide what goes into the state, we can **filter** the input.

### Only digits

```kotlin
OutlinedTextField(
    value = age,
    onValueChange = { newText ->
        if (newText.all { it.isDigit() }) {
            age = newText
        }
    },
    label = { Text("Age") },
    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
    singleLine = true
)
```

| Code | Meaning |
|---|---|
| `newText.all { it.isDigit() }` | "Is **every** character a digit (0–9)?" (Chapter 3: `all`) |
| `if (...) { age = newText }` | Only **accept** the new text if it's all digits. Otherwise, **ignore** it — the field stays the same. 🚫 |

> 💡 **Why filter if we already use the Number keyboard?** Because users can still **paste** text, or use a different keyboard app. Always filter important fields! 🛡️

> ℹ️ An **empty** string `""` passes `all { }` (there's nothing to fail!), so the user can still **delete** everything. 👍

### Maximum length

```kotlin
onValueChange = { newText ->
    if (newText.length <= 20) {
        username = newText
    }
}
```

Or **cut** it instead of rejecting:

```kotlin
onValueChange = { username = it.take(20) }
```

`take(20)` → only the **first 20** characters.

### Both rules together

```kotlin
onValueChange = { newText ->
    if (newText.length <= 4 && newText.all { it.isDigit() }) {
        pin = newText
    }
}
```

A **4-digit PIN** only. 🔢

### Change while typing

```kotlin
onValueChange = { username = it.lowercase().replace(" ", "") }
```

The username is always **small letters with no spaces**, no matter what the user types. ✨

### Turning text into a number

The field always gives a **String**. To do math, convert it (Chapter 2):

```kotlin
val ageNumber: Int? = age.toIntOrNull()     // null if empty or not a number
```

> ⚠️ Keep the **state** as a `String`. Don't make the state an `Int` — then the user couldn't have an **empty** field while typing. Convert only when you **use** it.

---

## 9.8 Checking Input and Showing Errors ❌

### The tools: `isError` and `supportingText`

```kotlin
val emailError = email.isNotEmpty() && !email.contains("@")

OutlinedTextField(
    value = email,
    onValueChange = { email = it },
    label = { Text("Email") },
    isError = emailError,
    supportingText = {
        if (emailError) {
            Text("Please enter a valid email")
        }
    },
    singleLine = true
)
```

```
 ┌ Email ─────────────────────────┐   ← RED border and label
 │ roy.example.com                 │
 └────────────────────────────────┘
   Please enter a valid email         ← RED message
```

| Code | Meaning |
|---|---|
| `val emailError = ...` | **Calculated** from state (Chapter 8: don't make it a separate state!). |
| `email.isNotEmpty() && ...` | Don't show an error on an **empty** field — the user hasn't typed yet. 😊 |
| `isError = emailError` | When `true`, the field turns **red** (the theme's `error` color). |
| `supportingText = { if (emailError) Text(...) }` | Show the **message** only when there's an error. |

### When should errors appear? ⏰

Showing an error **while** the user is still typing feels rude: you type `r` and immediately see "*Invalid email!*" 😠

**A friendly approach used by many apps:**

1. **Don't** show errors at first.
2. When the user taps **Submit**, check **all** fields.
3. From then on, show errors **live** as they fix them.

```kotlin
var submitted by remember { mutableStateOf(false) }

val emailError = submitted && !isValidEmail(email)

Button(onClick = { submitted = true }) { Text("Sign up") }
```

- `submitted` starts `false` → no errors shown.
- After tapping, `submitted = true` → errors appear for any wrong fields.
- As the user fixes a field, its error **disappears** right away (it's calculated every recomposition). ✨

### Validation functions (plain Kotlin!)

Put the **rules** in normal Kotlin functions, outside any Composable:

```kotlin
fun isValidEmail(email: String): Boolean {
    val at = email.indexOf('@')
    val lastDot = email.lastIndexOf('.')
    return at > 0 && lastDot > at + 1 && lastDot < email.length - 1
}

fun isValidPassword(password: String): Boolean {
    return password.length >= 8 && password.any { it.isDigit() }
}
```

**`isValidEmail`, step by step**, for `"roy@mail.com"`:

| Check | Value | OK? |
|---|---|---|
| `at = indexOf('@')` | 3 | |
| `lastDot = lastIndexOf('.')` | 8 | |
| `at > 0` — something **before** `@` | 3 > 0 | ✅ |
| `lastDot > at + 1` — something between `@` and `.` | 8 > 4 | ✅ |
| `lastDot < length - 1` — something **after** the dot | 8 < 11 | ✅ |

**`isValidPassword`:** at least **8** characters **and** at least **one digit** (`any`, Chapter 3).

> 💡 **Why separate functions?**
> - The Composable stays **short** and easy to read.
> - The rules can be **reused** and **tested** (Chapter 27).
> - Later (Chapter 15), they'll move into a **ViewModel**.

> ℹ️ Android also has a ready-made email checker: `android.util.Patterns.EMAIL_ADDRESS.matcher(email).matches()`. Our own function is simpler to understand while learning.

---

## 9.9 `Checkbox` ☑️

A **checkbox** is for **yes/no** choices, especially when there are **many independent** choices ("*Which toppings do you want?*").

### Basic checkbox

```kotlin
var agreed by remember { mutableStateOf(false) }

Checkbox(
    checked = agreed,
    onCheckedChange = { agreed = it }
)
```

Same pattern as `Switch`: `checked` ⬇️ + `onCheckedChange` ⬆️.

### Checkbox with a label — the right way ✅

A checkbox alone is **tiny** and hard to tap. Users expect to tap the **text** too!

```kotlin
@Composable
fun LabeledCheckbox(
    label: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .toggleable(
                value = checked,
                onValueChange = onCheckedChange,
                role = Role.Checkbox
            )
            .padding(vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Checkbox(
            checked = checked,
            onCheckedChange = null
        )
        Spacer(modifier = Modifier.width(8.dp))
        Text(text = label, style = MaterialTheme.typography.bodyLarge)
    }
}
```

Imports:

```kotlin
import androidx.compose.foundation.selection.toggleable
import androidx.compose.ui.semantics.Role
```

| Code | Meaning |
|---|---|
| `Modifier.toggleable(...)` | Makes the **whole row** tappable, and flips the value. |
| `role = Role.Checkbox` | Tells **screen readers** (TalkBack) "*this is a checkbox*". ♿ |
| `Checkbox(onCheckedChange = null)` | The checkbox itself does **nothing** on tap — the **row** handles it. (Otherwise a tap could be counted twice.) |

> 💡 This pattern — **the whole row is tappable** — is what good apps do. Bigger target = happier users. 👆😊

### Many checkboxes (a list of choices)

```kotlin
@Composable
fun ToppingsPicker(modifier: Modifier = Modifier) {
    val allToppings = listOf("Cheese 🧀", "Mushroom 🍄", "Olive 🫒", "Pepper 🌶️")
    var chosen by remember { mutableStateOf(setOf<String>()) }

    Column(modifier = modifier.padding(16.dp)) {
        allToppings.forEach { topping ->
            LabeledCheckbox(
                label = topping,
                checked = topping in chosen,
                onCheckedChange = { isChecked ->
                    chosen = if (isChecked) chosen + topping else chosen - topping
                }
            )
        }
        Text("You chose: ${chosen.joinToString().ifEmpty { "nothing yet" }}")
    }
}
```

| Code | Meaning |
|---|---|
| `setOf<String>()` | A **Set** (Chapter 3) — no repeats, perfect for "which ones are chosen". |
| `topping in chosen` | Is this topping in the set? → `true`/`false`. |
| `chosen + topping` / `chosen - topping` | A **new** set with / without it (immutable state, Chapter 8). |
| `.ifEmpty { "nothing yet" }` | If the text is empty, use this instead. |

---

## 9.10 `RadioButton` 🔘

**Radio buttons** are for choosing **exactly one** from a small list ("*Pick a size: S, M, L*"). When you pick one, the others turn **off** — like old car radio buttons. 📻

```kotlin
@Composable
fun SizePicker(modifier: Modifier = Modifier) {
    val sizes = listOf("Small", "Medium", "Large")
    var selected by remember { mutableStateOf(sizes[1]) }

    Column(modifier = modifier.selectableGroup()) {
        sizes.forEach { size ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .selectable(
                        selected = (size == selected),
                        onClick = { selected = size },
                        role = Role.RadioButton
                    )
                    .padding(vertical = 8.dp, horizontal = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                RadioButton(
                    selected = (size == selected),
                    onClick = null
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(size)
            }
        }
    }
}
```

Imports:

```kotlin
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.material3.RadioButton
```

| Code | Meaning |
|---|---|
| `var selected by remember { mutableStateOf(sizes[1]) }` | **One** state for the **whole group**: which size is chosen. Starts with "Medium". |
| `Modifier.selectableGroup()` | Tells screen readers: "*these options belong together*". ♿ |
| `Modifier.selectable(...)` | Like `toggleable`, but for "pick one". The whole row is tappable. |
| `selected = (size == selected)` | This row is selected **if** its size is the chosen one. |
| `onClick = { selected = size }` | Choose this size. The others turn off **automatically** — because they're calculated from the same state! ✨ |
| `RadioButton(onClick = null)` | The row handles the tap. |

### Checkbox vs Radio vs Switch — which one?

| Control | Use when | Example |
|---|---|---|
| ☑️ **Checkbox** | Pick **any number** (0, 1, or many) from a list | Toppings, "I agree to the terms" |
| 🔘 **Radio button** | Pick **exactly one** from a **small** list (2–5) | Size, delivery method |
| 🔛 **Switch** | Turn **one setting** on/off, takes effect **immediately** | Dark mode, notifications |

---

## 9.11 `Slider` 🎚️

A **slider** lets the user pick a number by **dragging**. Great for volume, brightness, price range…

```kotlin
@Composable
fun VolumeSlider(modifier: Modifier = Modifier) {
    var volume by remember { mutableFloatStateOf(0.5f) }

    Column(modifier = modifier.padding(16.dp)) {
        Text("Volume: ${(volume * 100).toInt()}% 🔊")
        Slider(
            value = volume,
            onValueChange = { volume = it }
        )
    }
}
```

Imports:

```kotlin
import androidx.compose.material3.Slider
import androidx.compose.runtime.mutableFloatStateOf
```

| Code | Meaning |
|---|---|
| `mutableFloatStateOf(0.5f)` | A slider uses a **`Float`**. Default range: `0f` to `1f`. |
| `value = volume` | Where the handle is. |
| `onValueChange = { volume = it }` | The user dragged → save the new value. |
| `(volume * 100).toInt()` | `0.5` → `50` → show "50%". |

### Your own range and steps

```kotlin
var stars by remember { mutableFloatStateOf(3f) }

Slider(
    value = stars,
    onValueChange = { stars = it },
    valueRange = 1f..5f,
    steps = 3
)
Text("Rating: ${stars.toInt()} ⭐")
```

| Input | Meaning |
|---|---|
| `valueRange = 1f..5f` | The slider goes from **1** to **5**. |
| `steps = 3` | **3 stop points between** the ends → the handle can only be at **1, 2, 3, 4, 5**. |

> 🧮 **How to count steps:** for values 1, 2, 3, 4, 5, there are **5** positions. Minus the **2 ends** = **3** steps. Formula: `steps = (number of values) - 2`.

### `RangeSlider` — pick a range (two handles)

```kotlin
var priceRange by remember { mutableStateOf(20f..80f) }

RangeSlider(
    value = priceRange,
    onValueChange = { priceRange = it },
    valueRange = 0f..100f
)
Text("From \$${priceRange.start.toInt()} to \$${priceRange.endInclusive.toInt()}")
```

Perfect for shop filters: "*Show prices from $20 to $80.*" 🛍️

---

## 9.12 Chips 🏷️

**Chips** are small, rounded buttons for **choices**, **filters**, and **tags**.

### `FilterChip` — select / unselect

```kotlin
var vegetarian by remember { mutableStateOf(false) }

FilterChip(
    selected = vegetarian,
    onClick = { vegetarian = !vegetarian },
    label = { Text("Vegetarian") },
    leadingIcon = if (vegetarian) {
        { Icon(Icons.Filled.Check, contentDescription = null, modifier = Modifier.size(18.dp)) }
    } else {
        null
    }
)
```

| Code | Meaning |
|---|---|
| `selected` | Is it on? Selected chips get a **filled** color. |
| `onClick` | Flip it. |
| `leadingIcon = if (...) { { Icon(...) } } else { null }` | Show a ✔️ **only** when selected. Notice the **double** `{ { } }`: the outer is the `if`, the inner is the **lambda** for the icon. |

### Many filter chips in a `FlowRow` (multi-select)

```kotlin
@Composable
fun InterestChips(
    allInterests: List<String>,
    selected: Set<String>,
    onToggle: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    FlowRow(
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        allInterests.forEach { interest ->
            FilterChip(
                selected = interest in selected,
                onClick = { onToggle(interest) },
                label = { Text(interest) }
            )
        }
    }
}
```

- `FlowRow` (Chapter 6) — chips **wrap** to the next line. 🌊
- Fully **hoisted**: the parent owns the `Set` of selected interests.

### Other chip types

| Chip | Use for |
|---|---|
| `FilterChip` | Turning a **filter** on/off ("Vegetarian", "Under $10") |
| `AssistChip` | A **smart action** ("📅 Add to calendar", "📍 Directions") |
| `InputChip` | Something the **user entered**, often with an ✖️ to remove ("roy@mail.com ✖️") |
| `SuggestionChip` | A **suggestion** ("Try: pizza", "Try: pasta") |

---

## 9.13 Dropdown Menus 🔽

When there are **many** options (like a list of countries 🌍), radio buttons take too much space. Use a **dropdown menu**.

```kotlin
@Composable
fun CountryPicker(
    selected: String,
    onSelected: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val countries = listOf("India", "Japan", "Brazil", "Germany", "Kenya", "Canada")
    var expanded by remember { mutableStateOf(false) }

    Box(modifier = modifier) {
        OutlinedButton(onClick = { expanded = true }) {
            Text(if (selected.isEmpty()) "Choose a country" else selected)
            Spacer(modifier = Modifier.width(8.dp))
            Icon(Icons.Filled.ArrowDropDown, contentDescription = null)
        }

        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            countries.forEach { country ->
                DropdownMenuItem(
                    text = { Text(country) },
                    onClick = {
                        onSelected(country)
                        expanded = false
                    }
                )
            }
        }
    }
}
```

Imports:

```kotlin
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material.icons.filled.ArrowDropDown
```

### Every bit explained

| Code | Meaning |
|---|---|
| `var expanded by remember { ... }` | Is the menu **open**? Local state — only this picker cares. |
| `Box { ... }` | The menu opens **next to** the things in this Box (the button). |
| `OutlinedButton(onClick = { expanded = true })` | Tap → **open** the menu. |
| `DropdownMenu(expanded = expanded, ...)` | The menu is shown when `expanded` is `true`. |
| `onDismissRequest = { expanded = false }` | The user tapped **outside** the menu → **close** it. |
| `DropdownMenuItem(text = ..., onClick = ...)` | One option. On tap: tell the parent, then close. |

> ℹ️ Material 3 also has `ExposedDropdownMenuBox`, which looks like a **text field** with a menu. It's a bit more complex, and its code has changed between versions, so we use the simpler `DropdownMenu` here. Both are fine!

---

## 9.14 Don't Let the Keyboard Cover Your Fields ⌨️🙈

On a small phone, when the keyboard opens, it can **cover** the field you're typing in — or the **Submit** button! 😩

Because our app uses `enableEdgeToEdge()` (Chapter 1), we tell Compose to make room for the keyboard with **`imePadding()`**:

```kotlin
Column(
    modifier = modifier
        .fillMaxSize()
        .imePadding()
        .verticalScroll(rememberScrollState())
        .padding(16.dp)
) {
    // ... many text fields ...
}
```

Import: `androidx.compose.foundation.layout.imePadding`

| Modifier | Meaning |
|---|---|
| `.imePadding()` | "Add space at the bottom **equal to the keyboard's height**." When the keyboard opens, the content **shrinks** above it. |
| `.verticalScroll(...)` | So the user can **scroll** to every field while the keyboard is open. |

> 💡 **Always** use `imePadding()` + `verticalScroll` on screens with text fields. Your users will thank you! 🙏

### Close the keyboard by tapping outside

A nice touch: tapping empty space hides the keyboard.

```kotlin
val focusManager = LocalFocusManager.current

Column(
    modifier = Modifier
        .fillMaxSize()
        .pointerInput(Unit) {
            detectTapGestures(onTap = { focusManager.clearFocus() })
        }
) { ... }
```

Imports:

```kotlin
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
```

- `pointerInput` + `detectTapGestures` → listen for taps on the **empty** parts of the screen.
- `clearFocus()` → the keyboard closes.

---

## 9.15 Build It: A Sign-Up Form 📝

Let's build a **real** sign-up form with **all** the inputs from this chapter.

```
┌──────────────────────────────────┐
│ Create account 🚀                │
│                                  │
│ ┌ 👤 Full name ──────────────┐   │  ← Words capitalization, Next
│ ┌ ✉️ Email ──────────────────┐   │  ← Email keyboard, error
│ ┌ 🔒 Password ───────[Show]──┐   │  ← hidden, Show/Hide
│   At least 8 characters and 1 digit
│ ┌ Age ──────────────── years ┐   │  ← digits only, Done
│                                  │
│ Country    [ India  ▾ ]          │  ← dropdown
│                                  │
│ Experience                       │  ← radio buttons
│ (•) Beginner  ( ) Some  ( ) Expert
│                                  │
│ Interests                        │  ← filter chips
│ [Games] [✓Music] [Art] [Sports]  │
│                                  │
│ Daily study goal: 30 min         │  ← slider
│ ──────●────────────              │
│                                  │
│ Email me tips          [  ●]     │  ← switch
│ ☑ I agree to the terms           │  ← checkbox
│                                  │
│ [      Create account      ]     │
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
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.selection.selectableGroup
import androidx.compose.foundation.selection.toggleable
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.RadioButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Slider
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.myfirstapp.ui.theme.MyFirstAppTheme

// ---------- Data and rules (plain Kotlin) ----------

enum class Experience(val label: String) {
    BEGINNER("Beginner"),
    SOME("Some"),
    EXPERT("Expert")
}

val allCountries = listOf("India", "Japan", "Brazil", "Germany", "Kenya", "Canada", "Mexico")
val allInterests = listOf("Games 🎮", "Music 🎵", "Art 🎨", "Sports ⚽", "Science 🔬", "Travel ✈️")

fun isValidName(name: String): Boolean = name.trim().length >= 2

fun isValidEmail(email: String): Boolean {
    val at = email.indexOf('@')
    val lastDot = email.lastIndexOf('.')
    return at > 0 && lastDot > at + 1 && lastDot < email.length - 1
}

fun isValidPassword(password: String): Boolean =
    password.length >= 8 && password.any { it.isDigit() }

fun isValidAge(age: String): Boolean {
    val number = age.toIntOrNull() ?: return false
    return number in 5..120
}

// ---------- Activity ----------

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyFirstAppTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    SignUpScreen(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}

// ---------- Screen (owns the state) ----------

@Composable
fun SignUpScreen(modifier: Modifier = Modifier) {
    // 1. State
    var name by rememberSaveable { mutableStateOf("") }
    var email by rememberSaveable { mutableStateOf("") }
    var password by rememberSaveable { mutableStateOf("") }
    var age by rememberSaveable { mutableStateOf("") }
    var country by rememberSaveable { mutableStateOf("") }
    var experience by rememberSaveable { mutableStateOf(Experience.BEGINNER) }
    var interests by remember { mutableStateOf(setOf<String>()) }
    var studyMinutes by rememberSaveable { mutableFloatStateOf(30f) }
    var emailTips by rememberSaveable { mutableStateOf(true) }
    var agreed by rememberSaveable { mutableStateOf(false) }
    var submitted by rememberSaveable { mutableStateOf(false) }
    var success by rememberSaveable { mutableStateOf(false) }

    // 2. Calculated errors (shown only after the first submit)
    val nameError = submitted && !isValidName(name)
    val emailError = submitted && !isValidEmail(email)
    val passwordError = submitted && !isValidPassword(password)
    val ageError = submitted && !isValidAge(age)
    val countryError = submitted && country.isEmpty()
    val termsError = submitted && !agreed

    val formIsValid = isValidName(name) && isValidEmail(email) &&
        isValidPassword(password) && isValidAge(age) &&
        country.isNotEmpty() && agreed

    val focusManager = LocalFocusManager.current

    if (success) {
        SuccessCard(
            name = name.trim(),
            onStartOver = {
                name = ""; email = ""; password = ""; age = ""; country = ""
                experience = Experience.BEGINNER; interests = emptySet()
                studyMinutes = 30f; emailTips = true; agreed = false
                submitted = false; success = false
            },
            modifier = modifier.padding(16.dp)
        )
        return
    }

    // 3. UI
    Column(
        modifier = modifier
            .fillMaxSize()
            .imePadding()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(
            text = "Create account 🚀",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold
        )

        // Name
        OutlinedTextField(
            value = name,
            onValueChange = { name = it.take(40) },
            label = { Text("Full name") },
            leadingIcon = { Icon(Icons.Filled.Person, contentDescription = null) },
            isError = nameError,
            supportingText = { if (nameError) Text("Please enter your name") },
            singleLine = true,
            keyboardOptions = KeyboardOptions(
                capitalization = KeyboardCapitalization.Words,
                imeAction = ImeAction.Next
            ),
            modifier = Modifier.fillMaxWidth()
        )

        // Email
        OutlinedTextField(
            value = email,
            onValueChange = { email = it.trim() },
            label = { Text("Email") },
            placeholder = { Text("you@example.com") },
            leadingIcon = { Icon(Icons.Filled.Email, contentDescription = null) },
            isError = emailError,
            supportingText = { if (emailError) Text("Please enter a valid email") },
            singleLine = true,
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Email,
                imeAction = ImeAction.Next
            ),
            modifier = Modifier.fillMaxWidth()
        )

        // Password
        PasswordField(
            password = password,
            onPasswordChange = { password = it },
            isError = passwordError
        )

        // Age
        OutlinedTextField(
            value = age,
            onValueChange = { newText ->
                if (newText.length <= 3 && newText.all { it.isDigit() }) {
                    age = newText
                }
            },
            label = { Text("Age") },
            suffix = { Text("years") },
            isError = ageError,
            supportingText = { if (ageError) Text("Please enter an age from 5 to 120") },
            singleLine = true,
            keyboardOptions = KeyboardOptions(
                keyboardType = KeyboardType.Number,
                imeAction = ImeAction.Done
            ),
            keyboardActions = KeyboardActions(onDone = { focusManager.clearFocus() }),
            modifier = Modifier.fillMaxWidth()
        )

        // Country
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Country", style = MaterialTheme.typography.titleSmall, modifier = Modifier.weight(1f))
            CountryPicker(selected = country, onSelected = { country = it })
        }
        if (countryError) {
            Text(
                text = "Please choose a country",
                color = MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodySmall
            )
        }

        // Experience
        SectionLabel("Experience")
        ExperiencePicker(selected = experience, onSelected = { experience = it })

        // Interests
        SectionLabel("Interests")
        FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            allInterests.forEach { interest ->
                FilterChip(
                    selected = interest in interests,
                    onClick = {
                        interests = if (interest in interests) interests - interest else interests + interest
                    },
                    label = { Text(interest) }
                )
            }
        }

        // Study goal
        SectionLabel("Daily study goal: ${studyMinutes.toInt()} min ⏱️")
        Slider(
            value = studyMinutes,
            onValueChange = { studyMinutes = it },
            valueRange = 10f..120f,
            steps = 10
        )

        // Email tips
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Email me learning tips", modifier = Modifier.weight(1f))
            Switch(checked = emailTips, onCheckedChange = { emailTips = it })
        }

        // Terms
        LabeledCheckbox(
            label = "I agree to the terms and conditions",
            checked = agreed,
            onCheckedChange = { agreed = it }
        )
        if (termsError) {
            Text(
                text = "You must agree to continue",
                color = MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodySmall
            )
        }

        // Submit
        Button(
            onClick = {
                submitted = true
                focusManager.clearFocus()
                if (formIsValid) {
                    success = true
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Create account")
        }
    }
}

// ---------- Reusable, stateless parts ----------

@Composable
fun SectionLabel(text: String, modifier: Modifier = Modifier) {
    Text(
        text = text,
        style = MaterialTheme.typography.titleSmall,
        fontWeight = FontWeight.Bold,
        modifier = modifier
    )
}

@Composable
fun PasswordField(
    password: String,
    onPasswordChange: (String) -> Unit,
    isError: Boolean,
    modifier: Modifier = Modifier
) {
    var visible by remember { mutableStateOf(false) }

    OutlinedTextField(
        value = password,
        onValueChange = onPasswordChange,
        label = { Text("Password") },
        leadingIcon = { Icon(Icons.Filled.Lock, contentDescription = null) },
        trailingIcon = {
            TextButton(onClick = { visible = !visible }) {
                Text(if (visible) "Hide" else "Show")
            }
        },
        visualTransformation = if (visible) VisualTransformation.None else PasswordVisualTransformation(),
        isError = isError,
        supportingText = { Text("At least 8 characters and 1 digit") },
        singleLine = true,
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Password,
            imeAction = ImeAction.Next
        ),
        modifier = modifier.fillMaxWidth()
    )
}

@Composable
fun CountryPicker(
    selected: String,
    onSelected: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    var expanded by remember { mutableStateOf(false) }

    Box(modifier = modifier) {
        OutlinedButton(onClick = { expanded = true }) {
            Text(if (selected.isEmpty()) "Choose" else selected)
            Spacer(modifier = Modifier.width(4.dp))
            Icon(Icons.Filled.ArrowDropDown, contentDescription = null)
        }
        DropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false }
        ) {
            allCountries.forEach { country ->
                DropdownMenuItem(
                    text = { Text(country) },
                    onClick = {
                        onSelected(country)
                        expanded = false
                    }
                )
            }
        }
    }
}

@Composable
fun ExperiencePicker(
    selected: Experience,
    onSelected: (Experience) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(modifier = modifier.selectableGroup()) {
        Experience.entries.forEach { level ->
            Row(
                modifier = Modifier
                    .weight(1f)
                    .selectable(
                        selected = level == selected,
                        onClick = { onSelected(level) },
                        role = Role.RadioButton
                    )
                    .padding(vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                RadioButton(selected = level == selected, onClick = null)
                Spacer(modifier = Modifier.width(4.dp))
                Text(level.label)
            }
        }
    }
}

@Composable
fun LabeledCheckbox(
    label: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .toggleable(value = checked, onValueChange = onCheckedChange, role = Role.Checkbox)
            .padding(vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Checkbox(checked = checked, onCheckedChange = null)
        Spacer(modifier = Modifier.width(8.dp))
        Text(label)
    }
}

@Composable
fun SuccessCard(name: String, onStartOver: () -> Unit, modifier: Modifier = Modifier) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer),
        modifier = modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(24.dp)) {
            Text("🎉", style = MaterialTheme.typography.displayMedium)
            Text(
                text = "Welcome, $name!",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
            Text("Your account was created.")
            TextButton(onClick = onStartOver, modifier = Modifier.align(Alignment.End)) {
                Text("Start over")
            }
        }
    }
}

// ---------- Preview ----------

@Preview(showBackground = true, showSystemUi = true)
@Composable
fun SignUpPreview() {
    MyFirstAppTheme {
        Surface {
            SignUpScreen()
        }
    }
}
```

> ⚠️ Keep **your own** `package` line and theme import.
> ⚠️ If `FlowRow` shows an "experimental" error, add `@OptIn(ExperimentalLayoutApi::class)` above `fun SignUpScreen` (Chapter 6).

### Every new part explained

#### Part 1: Rules as plain Kotlin functions

```kotlin
fun isValidAge(age: String): Boolean {
    val number = age.toIntOrNull() ?: return false
    return number in 5..120
}
```

| Code | Meaning |
|---|---|
| `age.toIntOrNull()` | Turn the text into a number, or `null` (Chapter 2). |
| `?: return false` | **Elvis + return** (Chapter 3): "If it's `null`, stop right here and answer `false`." A very common Kotlin trick! ⭐ |
| `number in 5..120` | Is it between 5 and 120? (Chapter 2: ranges) |

```kotlin
fun isValidName(name: String): Boolean = name.trim().length >= 2
```

- `trim()` removes spaces at the **start and end**. So `"   "` (only spaces) is **not** a valid name. 👍

#### Part 2: The state

- **12 pieces of state**, one for each input + `submitted` + `success`.
- Most use `rememberSaveable` → rotate the phone and nothing is lost. 🔄
- `interests` uses `remember` — a `Set` is a more complex type, so to stay safe we use `remember`. (In Chapter 15, a **ViewModel** will keep **all** of this safely.)

#### Part 3: Calculated errors

```kotlin
    val emailError = submitted && !isValidEmail(email)
```

- **No** error before the first submit (friendly 😊).
- **After** submit, errors are **live**: fix the email and the red goes away **immediately**. ✨

```kotlin
    val formIsValid = isValidName(name) && isValidEmail(email) && ...
```

- One value that says "*is everything OK?*". Used when the button is tapped.

#### Part 4: Showing a different screen with `if` + `return`

```kotlin
    if (success) {
        SuccessCard(...)
        return
    }
```

- If the account was created, show the **success card** and **stop** (`return`) — don't draw the form.
- Yes, a Composable can `return` early! ↩️
- `onStartOver` resets **all** the state → the form comes back, empty.

> 💡 `name = ""; email = ""; ...` — the **semicolon** `;` lets you put several statements on **one line**. Handy for a long reset.

#### Part 5: The text fields

Each field uses **the right tools**:

| Field | Special settings |
|---|---|
| Name | `take(40)` max length, `KeyboardCapitalization.Words`, `ImeAction.Next` |
| Email | `trim()` removes spaces, `KeyboardType.Email`, placeholder |
| Password | Our hoisted `PasswordField`: hidden, Show/Hide, help text |
| Age | Digits only, max 3, `suffix = "years"`, `ImeAction.Done` closes the keyboard |

Notice the **Next** ➡️ key moves smoothly from Name → Email → Password → Age, and **Done** ✅ closes the keyboard. Small details, big comfort! 🛋️

#### Part 6: The other inputs

| Input | Pattern |
|---|---|
| `CountryPicker` | Dropdown, **hoisted**: `selected` + `onSelected`. Has its own `expanded` state inside. |
| `ExperiencePicker` | Radio buttons in a **Row**, each taking `weight(1f)`. Uses the `Experience` **enum**. |
| `FilterChip`s in a `FlowRow` | Multi-select with a `Set`. |
| `Slider` | 10 to 120 minutes, `steps = 10` → stops at 10, 20, 30… 120. (12 values − 2 ends = 10 steps ✅) |
| `Switch` | Email tips on/off. |
| `LabeledCheckbox` | The whole row is tappable. |

#### Part 7: The submit button

```kotlin
        Button(
            onClick = {
                submitted = true
                focusManager.clearFocus()
                if (formIsValid) {
                    success = true
                }
            },
            ...
        )
```

1. `submitted = true` → errors may now appear.
2. `clearFocus()` → close the keyboard so the user can **see** the errors.
3. If everything is valid → `success = true` → the **success card** appears! 🎉

### Run it! ▶️

1. Tap **Create account** right away → see **all the errors** in red. ❌
2. Fill in each field — watch each error **disappear** as you fix it. ✅
3. Try typing letters in **Age** — they're **blocked**. 🛂
4. Try a password with no digits — error. Add a digit — fixed!
5. **Rotate** the phone — your typed text is still there. 🔄
6. Fill everything correctly → **🎉 Welcome, Roy!**

---

## 9.16 Common Mistakes and Fixes 🔧

| Mistake | Problem | Fix |
|---|---|---|
| `onValueChange = { }` (empty) | Typing does **nothing** | Save the text: `onValueChange = { text = it }`. |
| `var text = ""` (no state) | Typing does nothing / resets | `var text by remember { mutableStateOf("") }` |
| Keeping a number field's state as `Int` | Can't have an empty field; crashes on bad input | Keep a `String`; convert with `toIntOrNull()` when used. |
| `label = Text("Name")` | *Type mismatch: expected @Composable () -> Unit* | It's a lambda: `label = { Text("Name") }` |
| Errors show while the user is still typing | Feels rude 😠 | Show errors after submit (`submitted && ...`). |
| Keyboard covers fields or the button | Can't see what you type | Add `.imePadding()` and `.verticalScroll(...)`. |
| Tiny checkbox is hard to tap | Users miss it | Make the whole row `toggleable` / `selectable`. |
| `Checkbox(onCheckedChange = { ... })` **and** a `toggleable` row | Tap counted twice → nothing seems to happen | Inside a toggleable row, use `onCheckedChange = null`. |
| Wrong `steps` on a Slider | Stops at strange numbers | `steps = (number of values) - 2`. |
| `DropdownMenu` doesn't close | Forgot `onDismissRequest` / `expanded = false` | Close it in both places. |
| Password visible in plain text | Not secure 😱 | `visualTransformation = PasswordVisualTransformation()` |
| Users paste letters into a Number field | Bad data | Filter in `onValueChange` (`all { it.isDigit() }`). |

---

## 9.17 Summary — What You Learned 🎓

✅ **`TextField` / `OutlinedTextField`** are **stateless**: `value` ⬇️ + `onValueChange` ⬆️. We control what is saved.

✅ **Options:** `label`, `placeholder`, `leadingIcon`, `trailingIcon`, `prefix`, `suffix`, `supportingText`, `isError`, `singleLine`, `minLines`/`maxLines`.

✅ **Keyboard:** `KeyboardOptions(keyboardType, imeAction, capitalization)` and `KeyboardActions(onDone = ...)`. `LocalFocusManager` + `clearFocus()` hides the keyboard.

✅ **Passwords:** `PasswordVisualTransformation()` with a Show/Hide toggle.

✅ **Filtering:** `all { it.isDigit() }`, `take(n)`, `lowercase()` in `onValueChange`.

✅ **Validation:** rules in plain functions; errors calculated from state; show after submit.

✅ **Checkbox** (many), **RadioButton** (one of few), **Switch** (one setting), **Slider** / **RangeSlider** (a number), **FilterChip** (filters/tags), **DropdownMenu** (one of many).

✅ **Accessibility:** whole rows tappable with `toggleable` / `selectable` and a `Role`.

✅ **`imePadding()`** keeps fields visible above the keyboard.

✅ You built a complete **Sign-Up form** with validation! 📝

---

## 9.18 Practice Time 🏋️

**Task 1 — Live greeting:**
A text field for a name. Below it, show `"Hello, <name>!"` — but if the field is empty, show `"Hello, stranger!"`.

**Task 2 — Tip calculator preview:**
Two fields: **Bill amount** (decimal keyboard) and **Tip %** (number keyboard). Show the tip and total below, like `Tip: $4.50 — Total: $34.50`. If a field is empty or wrong, show `—`.

**Task 3 — Character limit:**
A "Bio" field with `minLines = 3`, max **100** characters, and a live counter `57 / 100` in the supporting text. When the user reaches 100, the counter turns **red** (use `isError`).

**Task 4 — Pizza builder:**
- Radio buttons for size: Small / Medium / Large.
- Checkboxes for toppings: Cheese, Mushroom, Olive.
- Show the order text: `"Large pizza with Cheese, Olive"`.

**Task 5 — Brightness:**
A `Slider` from 0 to 100 (whole numbers only). A `Box` below gets **lighter** as the slider goes up. (Hint: `Color.Yellow.copy(alpha = value / 100f)`.)

**Task 6 — Username rules:**
A username field that **automatically** turns every letter to lowercase, removes spaces, and allows at most 15 characters.

---

### Answers

**Task 1:**

```kotlin
@Composable
fun LiveGreeting(modifier: Modifier = Modifier) {
    var name by rememberSaveable { mutableStateOf("") }

    Column(modifier = modifier.padding(16.dp)) {
        OutlinedTextField(
            value = name,
            onValueChange = { name = it },
            label = { Text("Your name") },
            singleLine = true
        )
        Text("Hello, ${name.ifBlank { "stranger" }}!")
    }
}
```

`ifBlank { }` → if the text is empty **or only spaces**, use `"stranger"`.

**Task 2:**

```kotlin
@Composable
fun TipPreviewCalc(modifier: Modifier = Modifier) {
    var bill by rememberSaveable { mutableStateOf("") }
    var tipPercent by rememberSaveable { mutableStateOf("15") }

    val billNumber = bill.toDoubleOrNull()
    val tipNumber = tipPercent.toDoubleOrNull()

    val resultText = if (billNumber != null && tipNumber != null) {
        val tip = billNumber * tipNumber / 100
        val total = billNumber + tip
        "Tip: \$${"%.2f".format(tip)} — Total: \$${"%.2f".format(total)}"
    } else {
        "—"
    }

    Column(
        modifier = modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        OutlinedTextField(
            value = bill,
            onValueChange = { bill = it },
            label = { Text("Bill amount") },
            prefix = { Text("$") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
            singleLine = true
        )
        OutlinedTextField(
            value = tipPercent,
            onValueChange = { new -> if (new.all { it.isDigit() }) tipPercent = new },
            label = { Text("Tip") },
            suffix = { Text("%") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            singleLine = true
        )
        Text(resultText, style = MaterialTheme.typography.titleMedium)
    }
}
```

`"%.2f".format(tip)` → 2 digits after the dot. (Same idea as `String.format` in Chapter 8.)
💡 You'll build a full, beautiful **Tip Calculator** app in **Chapter 12**!

**Task 3:**

```kotlin
@Composable
fun BioField(modifier: Modifier = Modifier) {
    var bio by rememberSaveable { mutableStateOf("") }
    val max = 100
    val atLimit = bio.length >= max

    OutlinedTextField(
        value = bio,
        onValueChange = { bio = it.take(max) },
        label = { Text("Bio") },
        minLines = 3,
        isError = atLimit,
        supportingText = { Text("${bio.length} / $max") },
        modifier = modifier.fillMaxWidth().padding(16.dp)
    )
}
```

**Task 4:**

```kotlin
@Composable
fun PizzaBuilder(modifier: Modifier = Modifier) {
    val sizes = listOf("Small", "Medium", "Large")
    val toppings = listOf("Cheese", "Mushroom", "Olive")

    var size by rememberSaveable { mutableStateOf("Medium") }
    var chosen by remember { mutableStateOf(setOf<String>()) }

    Column(modifier = modifier.padding(16.dp)) {
        Text("Size", fontWeight = FontWeight.Bold)
        Column(modifier = Modifier.selectableGroup()) {
            sizes.forEach { s ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .selectable(selected = s == size, onClick = { size = s }, role = Role.RadioButton)
                        .padding(vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    RadioButton(selected = s == size, onClick = null)
                    Text(s, modifier = Modifier.padding(start = 8.dp))
                }
            }
        }

        Text("Toppings", fontWeight = FontWeight.Bold)
        toppings.forEach { t ->
            LabeledCheckbox(
                label = t,
                checked = t in chosen,
                onCheckedChange = { isOn -> chosen = if (isOn) chosen + t else chosen - t }
            )
        }

        val toppingText = if (chosen.isEmpty()) "no toppings" else chosen.joinToString(", ")
        Text("$size pizza with $toppingText 🍕", style = MaterialTheme.typography.titleMedium)
    }
}
```

**Task 5:**

```kotlin
@Composable
fun BrightnessDemo(modifier: Modifier = Modifier) {
    var value by rememberSaveable { mutableFloatStateOf(50f) }

    Column(modifier = modifier.padding(16.dp)) {
        Text("Brightness: ${value.toInt()}%")
        Slider(
            value = value,
            onValueChange = { value = it },
            valueRange = 0f..100f,
            steps = 99
        )
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(120.dp)
                .background(Color.Yellow.copy(alpha = value / 100f))
        )
    }
}
```

`steps = 99` → 101 values (0 to 100) − 2 ends = 99. Whole numbers only. ✅

**Task 6:**

```kotlin
@Composable
fun UsernameField(modifier: Modifier = Modifier) {
    var username by rememberSaveable { mutableStateOf("") }

    OutlinedTextField(
        value = username,
        onValueChange = { username = it.lowercase().replace(" ", "").take(15) },
        label = { Text("Username") },
        prefix = { Text("@") },
        supportingText = { Text("Small letters, no spaces, max 15") },
        singleLine = true,
        modifier = modifier.padding(16.dp)
    )
}
```

Three rules **chained** together (Chapter 3: chaining). ⛓️

---

## 9.19 What Is Next?

Until now, we showed lists with `forEach` inside a scrolling `Column`. That's fine for 10 items… but what about **1,000** messages or **10,000** songs? 🐢

In **Chapter 10: Lists and Grids**, you will learn:

- **`LazyColumn`** — super-fast lists that only draw what's on screen ⚡
- **`LazyRow`** — horizontal lists
- **`LazyVerticalGrid`** — photo-gallery grids 🖼️
- `items`, `itemsIndexed`, and **keys**
- Headers, dividers, and **sticky headers** 📌
- Scrolling to the top with a button ⬆️
- A **Contacts** app with search 🔍

**Great job finishing Chapter 9! 🎉 Your apps can now listen to the user!**
