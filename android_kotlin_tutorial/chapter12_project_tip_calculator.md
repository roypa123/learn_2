# Chapter 12: 🛠️ Mini Project — Tip Calculator App

> **What you will do in this chapter**
>
> 1. **Plan** an app before writing code ✏️
> 2. Break the design into small **Composables** 🧱
> 3. Write the **math** as plain Kotlin functions 🧮
> 4. Build the app **step by step**, testing as you go
> 5. Show money the **right way** for every country 💵💶💴
> 6. Polish: previews, dark mode, reset button, keyboard comfort ✨
> 7. Test your app with a **checklist** ✅
> 8. Ideas to make it even better 🚀
>
> **Time needed:** about 3 to 4 hours.
>
> **What you need to know:** Chapters 1–11. This chapter has **no new big ideas** — it puts everything **together**. That is how you become a real developer! 💪

---

## 12.1 What Are We Building? 🍽️

When friends eat at a restaurant, they often ask:

- "*How much tip should we leave?*" 🤔
- "*How much does each person pay?*" 👥

Our app answers both questions **instantly**.

### The finished app

```
┌──────────────────────────────────┐
│        💰 Tip Calculator     ↻   │  ← CenterAlignedTopAppBar + Reset
├──────────────────────────────────┤
│ ╭──────────────────────────────╮ │
│ │      Each person pays        │ │  ← Result card (big number)
│ │          $18.40              │ │
│ │  Tip: $9.20   Total: $55.20  │ │
│ ╰──────────────────────────────╯ │
│                                  │
│ ┌ Bill amount ───────────────┐   │  ← Decimal keyboard
│ │ $  46.00                    │   │
│ └────────────────────────────┘   │
│                                  │
│ Tip                              │
│ [10%] [15%] [■20%■] [25%] [Custom]  ← FilterChips
│                                  │
│ Split between                    │
│        [ − ]   3 people  [ + ]   │  ← Stepper
│                                  │
│ Round up per person    [  ●]     │  ← Switch
└──────────────────────────────────┘
```

### What the app must do (the "requirements") 📋

Writing a list like this **before** coding is what professionals do. It keeps you focused. 🎯

1. The user types the **bill amount** (with decimals, like `46.50`).
2. The user picks a **tip %**: 10, 15, 18, 20, 25, or **Custom** (a slider from 0 to 30%).
3. The user chooses **how many people** split the bill (1 to 20).
4. The user can **round up** what each person pays to a whole number (no coins! 🪙🚫).
5. The app shows **per person**, **tip**, and **total** — and updates **live**.
6. A **Reset** button starts over.
7. Rotating the phone keeps everything. 🔄
8. Works in **light and dark** mode. 🌙
9. Money looks right in **any country** ($46.00, 46,00 €, ₹46.00…).

---

## 12.2 Step 0: Plan on Paper ✏️📄

Before writing code, **draw** the screen and **break it into blocks** (the skill from Chapter 6).

```
TipCalculatorApp
 └── Scaffold
      ├── topBar: CenterAlignedTopAppBar ("💰 Tip Calculator", Reset button)
      └── content: TipCalculatorScreen (Column, scrollable)
           ├── ResultCard          ← shows per person, tip, total
           ├── BillInput           ← OutlinedTextField
           ├── TipSelector         ← FilterChips + optional Slider
           ├── PeopleStepper       ← − number +
           └── RoundUpRow          ← text + Switch
```

### Decide: where does the state live? 🧠

Ask: "*What can change?*" (Chapter 8)

| State | Type | Starts as |
|---|---|---|
| The bill text | `String` | `""` |
| The tip percent | `Int` | `15` |
| Is "Custom" chosen? | `Boolean` | `false` |
| Number of people | `Int` | `1` |
| Round up? | `Boolean` | `false` |

Ask: "*Who needs it?*" → The **result card** needs **all** of them. So the state lives in the **parent** (`TipCalculatorScreen`), and the small blocks are **stateless** (hoisting, Chapter 8). ⬆️

Ask: "*What can be calculated?*" → **Tip**, **total**, and **per person**. These are **not** state! ✅

> 💡 **These 3 questions** — *What changes? Who needs it? What can be calculated?* — work for **every** app you'll ever build. Write them down! 📝

---

## 12.3 Step 1: A Fresh Project (or Clean Up) 🧹

You can keep using **MyFirstApp**, or make a **new project** for this app (good practice!):

1. **File → New → New Project…**
2. Choose **Empty Activity** → **Next**.
3. **Name:** `Tip Calculator`
4. **Package name:** `com.example.tipcalculator`
5. **Minimum SDK:** keep the default.
6. **Finish**, and wait for Gradle. ☕

> ⚠️ **If you make a new project:** in all the code below, use **`com.example.tipcalculator`** as the package and **`TipCalculatorTheme`** as the theme name (Android Studio names the theme after your app). If you keep **MyFirstApp**, use your old package and `MyFirstAppTheme`.

> 💡 **Icons:** we use `Icons.Filled.Refresh`. If `Icons` is red, add the icons library (Chapter 5, section 5.8).

### Change the app name

Open `res/values/strings.xml`:

```xml
<resources>
    <string name="app_name">Tip Calculator</string>
</resources>
```

This is the name under the app icon on the phone. 📱

---

## 12.4 Step 2: The Math First (Plain Kotlin) 🧮

**Good habit:** Write the **logic** (math) **separately** from the **UI**. Then:

- It's **easy to read** — no buttons or colors mixed in.
- It's **easy to test** (Chapter 27). 🧪
- You can **reuse** it anywhere.

Make a **new Kotlin file** for it:

1. In the Project window, **right-click** your package folder (`com.example.tipcalculator`).
2. **New → Kotlin Class/File**.
3. Choose **File**, name it **`TipMath`**, press Enter.

Put this inside `TipMath.kt` (keep the `package` line Android Studio wrote):

```kotlin
package com.example.tipcalculator

import java.text.NumberFormat
import kotlin.math.ceil

data class TipResult(
    val tip: Double,
    val total: Double,
    val perPerson: Double
)

fun calculateTip(
    bill: Double,
    tipPercent: Int,
    people: Int,
    roundUp: Boolean
): TipResult {
    val safePeople = people.coerceAtLeast(1)
    val tip = bill * tipPercent / 100.0
    val total = bill + tip
    val perPerson = total / safePeople

    if (!roundUp) {
        return TipResult(tip = tip, total = total, perPerson = perPerson)
    }

    val roundedPerPerson = ceil(perPerson)
    val roundedTotal = roundedPerPerson * safePeople
    return TipResult(
        tip = roundedTotal - bill,
        total = roundedTotal,
        perPerson = roundedPerPerson
    )
}

fun Double.toMoney(): String = NumberFormat.getCurrencyInstance().format(this)

fun isValidBillText(text: String): Boolean {
    if (text.isEmpty()) return true
    if (!text.all { it.isDigit() || it == '.' }) return false
    if (text.count { it == '.' } > 1) return false
    val decimals = text.substringAfter('.', missingDelimiterValue = "")
    return decimals.length <= 2 && text.length <= 9
}
```

### Every bit explained

#### The result: a data class

```kotlin
data class TipResult(
    val tip: Double,
    val total: Double,
    val perPerson: Double
)
```

- A function can only `return` **one** thing. To give back **three** numbers, we put them in **one data class** (Chapter 3). 📦

#### `calculateTip` — the main math

```kotlin
    val safePeople = people.coerceAtLeast(1)
```

- `coerceAtLeast(1)` → "**At least** 1." If someone passes `0`, we use `1`. **Dividing by zero** would give a broken result (`Infinity`)! 💥 Safety first. 🛡️

```kotlin
    val tip = bill * tipPercent / 100.0
    val total = bill + tip
    val perPerson = total / safePeople
```

**Example:** bill = 46.00, tip = 20%, people = 3

| Step | Math | Result |
|---|---|---|
| tip | 46 × 20 ÷ 100 | **9.20** |
| total | 46 + 9.20 | **55.20** |
| perPerson | 55.20 ÷ 3 | **18.40** |

> ⚠️ **Why `100.0` and not `100`?** Remember Chapter 2: `Int / Int` cuts off decimals! `bill` is a `Double`, so here it's safe anyway — but writing `100.0` makes it **clear** we want decimals. 👍

```kotlin
    if (!roundUp) {
        return TipResult(tip = tip, total = total, perPerson = perPerson)
    }
```

- If the user doesn't want rounding → give back the normal result and **stop** here (**early return**).

```kotlin
    val roundedPerPerson = ceil(perPerson)
    val roundedTotal = roundedPerPerson * safePeople
    return TipResult(
        tip = roundedTotal - bill,
        total = roundedTotal,
        perPerson = roundedPerPerson
    )
```

**Rounding up**, with the same example:

| Step | Math | Result |
|---|---|---|
| `ceil(18.40)` | Round **up** to the next whole number | **19.00** |
| roundedTotal | 19 × 3 | **57.00** |
| tip | 57 − 46 | **11.00** (the extra goes to the tip! 😊) |

| Function | Meaning | Examples |
|---|---|---|
| `ceil(x)` | Round **up** (ceiling ⬆️) | `ceil(18.01)` = 19.0, `ceil(18.0)` = 18.0 |
| `floor(x)` | Round **down** (floor ⬇️) | `floor(18.99)` = 18.0 |
| `round(x)` | Round to the **nearest** | `round(18.4)` = 18.0, `round(18.5)` = 19.0 (in Kotlin, .5 goes to the nearest **even** number: `round(19.5)` = 20.0, `round(18.5)` = 18.0!) |

Import: `kotlin.math.ceil`

#### `toMoney` — money for every country 🌍

```kotlin
fun Double.toMoney(): String = NumberFormat.getCurrencyInstance().format(this)
```

- An **extension function** on `Double` (Chapter 4).
- `NumberFormat.getCurrencyInstance()` → a **money formatter** that follows the **phone's language and country** settings.

| Phone set to… | `55.2.toMoney()` shows |
|---|---|
| English (US) | `$55.20` |
| English (India) | `₹55.20` |
| German (Germany) | `55,20 €` |
| Japanese (Japan) | `￥55` |
| French (France) | `55,20 €` |

✨ One line, and your app is **international**! Much better than writing `"$" + ...` by hand (like we did in Chapter 8).

#### `isValidBillText` — what can be typed in the bill box

```kotlin
fun isValidBillText(text: String): Boolean {
    if (text.isEmpty()) return true                                   // 1
    if (!text.all { it.isDigit() || it == '.' }) return false         // 2
    if (text.count { it == '.' } > 1) return false                    // 3
    val decimals = text.substringAfter('.', missingDelimiterValue = "")
    return decimals.length <= 2 && text.length <= 9                   // 4
}
```

| Rule | Allows | Blocks |
|---|---|---|
| 1. Empty is OK | `""` (so the user can delete everything) | — |
| 2. Only digits and dots | `46.50` | `46a`, `-5`, `4 6` |
| 3. At most one dot | `46.5` | `46.5.0` |
| 4. At most 2 decimals, max 9 characters | `46.25`, `123456.78` | `46.257`, `1234567890` |

- `text.count { it == '.' }` → how many dots (Chapter 3: `count`).
- `substringAfter('.', missingDelimiterValue = "")` → the part **after** the dot. If there's **no** dot, give `""`.
  - `"46.25"` → `"25"` (2 decimals ✅)
  - `"46"` → `""` (0 decimals ✅)

> 💡 This uses **early returns** to check rules one by one. Very readable! 📖

> ℹ️ **About commas:** Some countries write `46,50` instead of `46.50`. Our app always uses a **dot** for typing (that's what the Decimal keyboard gives on most phones). Supporting commas is a nice extra challenge — see 12.11! 🌍

---

## 12.5 Step 3: Build the Screen Piece by Piece 🧱

Now the UI. We'll write **each block** separately, and **preview** each one. Building and checking small pieces is **much easier** than writing everything at once and hoping it works! 🙏

Put all the following code into **`MainActivity.kt`**. The complete file is in section 12.7 — but please **type each part** as you read. ⌨️

### Block 1: `ResultCard` 💳

```kotlin
@Composable
fun ResultCard(
    result: TipResult,
    people: Int,
    modifier: Modifier = Modifier
) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        ),
        shape = MaterialTheme.shapes.extraLarge,
        modifier = modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = if (people == 1) "You pay" else "Each person pays",
                style = MaterialTheme.typography.titleMedium
            )
            Text(
                text = result.perPerson.toMoney(),
                style = MaterialTheme.typography.displayMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(8.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(24.dp)) {
                LabeledAmount(label = "Tip", amount = result.tip)
                LabeledAmount(label = "Total", amount = result.total)
            }
        }
    }
}

@Composable
fun LabeledAmount(label: String, amount: Double, modifier: Modifier = Modifier) {
    Column(modifier = modifier, horizontalAlignment = Alignment.CenterHorizontally) {
        Text(text = label, style = MaterialTheme.typography.labelMedium)
        Text(
            text = amount.toMoney(),
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.SemiBold
        )
    }
}

@Preview(showBackground = true)
@Composable
fun ResultCardPreview() {
    TipCalculatorTheme {
        ResultCard(
            result = TipResult(tip = 9.2, total = 55.2, perPerson = 18.4),
            people = 3,
            modifier = Modifier.padding(16.dp)
        )
    }
}
```

| Code | Meaning |
|---|---|
| `result: TipResult` | The card gets **all three** numbers in one object. |
| `if (people == 1) "You pay" else "Each person pays"` | Nice, correct English for one person. 😊 |
| `displayMedium` | A **big** text style (Chapter 5) for the most important number. |
| `LabeledAmount` | A tiny reusable block: a label above an amount. Used **twice**. ♻️ |
| `ResultCardPreview` | Check the card **alone**, with fake numbers. 👀 |

> 🎯 **Design idea:** The **most important** number (per person) is the **biggest**. The others are smaller. This is called **visual hierarchy** — the eye goes to the big thing first. 👁️

### Block 2: `BillInput` 💵

```kotlin
@Composable
fun BillInput(
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val focusManager = LocalFocusManager.current

    OutlinedTextField(
        value = value,
        onValueChange = { newText ->
            if (isValidBillText(newText)) {
                onValueChange(newText)
            }
        },
        label = { Text("Bill amount") },
        placeholder = { Text("0.00") },
        leadingIcon = { Text("💵", fontSize = 20.sp) },
        singleLine = true,
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Decimal,
            imeAction = ImeAction.Done
        ),
        keyboardActions = KeyboardActions(onDone = { focusManager.clearFocus() }),
        modifier = modifier.fillMaxWidth()
    )
}
```

| Code | Meaning |
|---|---|
| `if (isValidBillText(newText)) onValueChange(newText)` | Only pass **good** text up. Bad text is **ignored** (Chapter 9). 🛂 |
| `leadingIcon = { Text("💵") }` | An emoji works as an icon too! (Any Composable can go in the slot.) |
| `KeyboardType.Decimal` | Digits + a dot. |
| `ImeAction.Done` + `clearFocus()` | The ✅ key closes the keyboard so the user sees the result. |

### Block 3: `TipSelector` 🏷️

```kotlin
val tipPresets = listOf(10, 15, 18, 20, 25)

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun TipSelector(
    tipPercent: Int,
    isCustom: Boolean,
    onPresetSelected: (Int) -> Unit,
    onCustomSelected: () -> Unit,
    onCustomChange: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier) {
        SectionTitle("Tip")
        FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            tipPresets.forEach { percent ->
                FilterChip(
                    selected = !isCustom && tipPercent == percent,
                    onClick = { onPresetSelected(percent) },
                    label = { Text("$percent%") }
                )
            }
            FilterChip(
                selected = isCustom,
                onClick = onCustomSelected,
                label = { Text("Custom") }
            )
        }

        if (isCustom) {
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "Custom tip: $tipPercent%",
                style = MaterialTheme.typography.bodyMedium
            )
            Slider(
                value = tipPercent.toFloat(),
                onValueChange = { onCustomChange(it.roundToInt()) },
                valueRange = 0f..30f,
                steps = 29
            )
        }
    }
}
```

| Code | Meaning |
|---|---|
| `val tipPresets = listOf(10, 15, 18, 20, 25)` | The quick choices. Want to add 12%? Change **one** line. ✨ |
| `selected = !isCustom && tipPercent == percent` | A preset chip is selected only if we're **not** in custom mode **and** its % matches. |
| `if (isCustom) { Slider(...) }` | The slider **appears** only in custom mode (state + `if`, Chapter 8). |
| `tipPercent.toFloat()` | The slider needs a `Float` (Chapter 9). |
| `it.roundToInt()` | Turn the slider's `Float` back into a whole `Int`. Import `kotlin.math.roundToInt`. |
| `steps = 29` | 0 to 30 = 31 values − 2 ends = **29** steps → whole percents only. ✅ |
| **5 inputs**, all hoisted | The selector **owns nothing**. The screen decides everything. |

### Block 4: `PeopleStepper` 👥

```kotlin
@Composable
fun PeopleStepper(
    people: Int,
    onPeopleChange: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier) {
        SectionTitle("Split between")
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center
        ) {
            FilledTonalIconButton(
                onClick = { onPeopleChange(people - 1) },
                enabled = people > MIN_PEOPLE
            ) {
                Text("−", style = MaterialTheme.typography.titleLarge)
            }
            Text(
                text = if (people == 1) "1 person" else "$people people",
                style = MaterialTheme.typography.titleLarge,
                modifier = Modifier
                    .padding(horizontal = 24.dp)
                    .widthIn(min = 110.dp),
                textAlign = TextAlign.Center
            )
            FilledTonalIconButton(
                onClick = { onPeopleChange(people + 1) },
                enabled = people < MAX_PEOPLE
            ) {
                Text("+", style = MaterialTheme.typography.titleLarge)
            }
        }
    }
}

const val MIN_PEOPLE = 1
const val MAX_PEOPLE = 20
```

| Code | Meaning |
|---|---|
| `FilledTonalIconButton` | A **round** button with a soft color. Good for small `−` / `+` buttons. |
| `enabled = people > MIN_PEOPLE` | The `−` button turns **grey** at 1 person. Can't go to 0! 🚫 |
| `"1 person"` / `"$people people"` | Correct singular and plural. Details matter! ✨ |
| `widthIn(min = 110.dp)` | The text **always** has the same minimum width, so the buttons **don't jump** around when the number changes from `9` to `10`. 🎯 |
| `const val MIN_PEOPLE / MAX_PEOPLE` | Limits in **one** place (Chapter 4). |

### Block 5: `RoundUpRow` and `SectionTitle`

```kotlin
@Composable
fun RoundUpRow(
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .toggleable(value = checked, onValueChange = onCheckedChange, role = Role.Switch),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text("Round up per person", style = MaterialTheme.typography.bodyLarge)
            Text(
                text = "No coins needed 🪙",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Switch(checked = checked, onCheckedChange = null)
    }
}

@Composable
fun SectionTitle(text: String, modifier: Modifier = Modifier) {
    Text(
        text = text,
        style = MaterialTheme.typography.titleSmall,
        fontWeight = FontWeight.Bold,
        modifier = modifier.padding(bottom = 8.dp)
    )
}
```

- The **whole row** is tappable (`toggleable`, Chapter 9), with `role = Role.Switch` for screen readers. ♿
- `Switch(onCheckedChange = null)` → the row handles the tap.

---

## 12.6 Step 4: Connect Everything — The Screen 🔌

Now the **parent** that owns the state and connects the blocks:

```kotlin
@Composable
fun TipCalculatorScreen(
    billText: String,
    onBillTextChange: (String) -> Unit,
    tipPercent: Int,
    isCustomTip: Boolean,
    onPresetSelected: (Int) -> Unit,
    onCustomSelected: () -> Unit,
    onCustomChange: (Int) -> Unit,
    people: Int,
    onPeopleChange: (Int) -> Unit,
    roundUp: Boolean,
    onRoundUpChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    val bill = billText.toDoubleOrNull() ?: 0.0
    val result = calculateTip(bill, tipPercent, people, roundUp)

    Column(
        modifier = modifier
            .fillMaxSize()
            .imePadding()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        ResultCard(result = result, people = people)
        BillInput(value = billText, onValueChange = onBillTextChange)
        TipSelector(
            tipPercent = tipPercent,
            isCustom = isCustomTip,
            onPresetSelected = onPresetSelected,
            onCustomSelected = onCustomSelected,
            onCustomChange = onCustomChange
        )
        PeopleStepper(people = people, onPeopleChange = onPeopleChange)
        RoundUpRow(checked = roundUp, onCheckedChange = onRoundUpChange)
    }
}
```

| Code | Meaning |
|---|---|
| `billText.toDoubleOrNull() ?: 0.0` | Text → number. Empty or `"."` → `null` → use **0.0** (Chapter 3: Elvis). No crash! 🛡️ |
| `val result = calculateTip(...)` | **Calculated**, not state. Every recomposition → fresh, correct numbers. ✨ |
| `.imePadding().verticalScroll(...)` | The keyboard never hides anything (Chapter 9). |
| `spacedBy(24.dp)` | Nice, even space between the sections. |

> 🤔 **Why does this screen get its state from outside too?** So we can **preview** it with **any** values (see 12.8), and so the **app** level can **reset** everything easily. The state goes **one more level up** — into `TipCalculatorApp`. ⬆️

### The app: state + Scaffold + top bar

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TipCalculatorApp() {
    var billText by rememberSaveable { mutableStateOf("") }
    var tipPercent by rememberSaveable { mutableIntStateOf(15) }
    var isCustomTip by rememberSaveable { mutableStateOf(false) }
    var people by rememberSaveable { mutableIntStateOf(1) }
    var roundUp by rememberSaveable { mutableStateOf(false) }

    val focusManager = LocalFocusManager.current

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("💰 Tip Calculator") },
                actions = {
                    IconButton(onClick = {
                        billText = ""
                        tipPercent = 15
                        isCustomTip = false
                        people = 1
                        roundUp = false
                        focusManager.clearFocus()
                    }) {
                        Icon(Icons.Filled.Refresh, contentDescription = "Reset")
                    }
                }
            )
        },
        modifier = Modifier.fillMaxSize()
    ) { innerPadding ->
        TipCalculatorScreen(
            billText = billText,
            onBillTextChange = { billText = it },
            tipPercent = tipPercent,
            isCustomTip = isCustomTip,
            onPresetSelected = { percent ->
                tipPercent = percent
                isCustomTip = false
            },
            onCustomSelected = { isCustomTip = true },
            onCustomChange = { tipPercent = it },
            people = people,
            onPeopleChange = { people = it.coerceIn(MIN_PEOPLE, MAX_PEOPLE) },
            roundUp = roundUp,
            onRoundUpChange = { roundUp = it },
            modifier = Modifier.padding(innerPadding)
        )
    }
}
```

| Code | Meaning |
|---|---|
| 5 × `rememberSaveable` | All state survives rotation. 🔄 |
| `CenterAlignedTopAppBar` | Title in the middle — nice for a one-screen app (Chapter 11). |
| Reset `IconButton` | Puts **every** state back to the start, and closes the keyboard. ↻ |
| `onPresetSelected = { tipPercent = percent; isCustomTip = false }` | Picking 20% **leaves** custom mode. |
| `onCustomSelected = { isCustomTip = true }` | Show the slider. The slider **starts** at the current %, so nothing jumps. 👌 |
| `it.coerceIn(MIN_PEOPLE, MAX_PEOPLE)` | **Double safety:** even if a button is pressed too fast, the number stays between 1 and 20. 🛡️ |

**The flow of data** in this app:

```
TipCalculatorApp (owns 5 states)
     │  ⬇️ values                  ⬆️ events (lambdas)
     ▼
TipCalculatorScreen (calculates result)
     │  ⬇️                         ⬆️
     ▼
ResultCard · BillInput · TipSelector · PeopleStepper · RoundUpRow
     (all stateless — they only show and report)
```

This is **"state down, events up"** (Chapter 8) in a real app. 🎉

---

## 12.7 The Complete Code 📄

### `TipMath.kt`

(From section 12.4 — no changes.)

### `MainActivity.kt`

Replace **everything** in `MainActivity.kt` with this. Use **your** package name and theme name!

```kotlin
package com.example.tipcalculator

import android.content.res.Configuration
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.selection.toggleable
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilledTonalIconButton
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Slider
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.tipcalculator.ui.theme.TipCalculatorTheme
import kotlin.math.roundToInt

// ---------- Constants ----------

const val MIN_PEOPLE = 1
const val MAX_PEOPLE = 20
val tipPresets = listOf(10, 15, 18, 20, 25)

// ---------- Activity ----------

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            TipCalculatorTheme {
                TipCalculatorApp()
            }
        }
    }
}

// ---------- App (owns the state) ----------

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TipCalculatorApp() {
    var billText by rememberSaveable { mutableStateOf("") }
    var tipPercent by rememberSaveable { mutableIntStateOf(15) }
    var isCustomTip by rememberSaveable { mutableStateOf(false) }
    var people by rememberSaveable { mutableIntStateOf(1) }
    var roundUp by rememberSaveable { mutableStateOf(false) }

    val focusManager = LocalFocusManager.current

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("💰 Tip Calculator") },
                actions = {
                    IconButton(onClick = {
                        billText = ""
                        tipPercent = 15
                        isCustomTip = false
                        people = 1
                        roundUp = false
                        focusManager.clearFocus()
                    }) {
                        Icon(Icons.Filled.Refresh, contentDescription = "Reset")
                    }
                }
            )
        },
        modifier = Modifier.fillMaxSize()
    ) { innerPadding ->
        TipCalculatorScreen(
            billText = billText,
            onBillTextChange = { billText = it },
            tipPercent = tipPercent,
            isCustomTip = isCustomTip,
            onPresetSelected = { percent ->
                tipPercent = percent
                isCustomTip = false
            },
            onCustomSelected = { isCustomTip = true },
            onCustomChange = { tipPercent = it },
            people = people,
            onPeopleChange = { people = it.coerceIn(MIN_PEOPLE, MAX_PEOPLE) },
            roundUp = roundUp,
            onRoundUpChange = { roundUp = it },
            modifier = Modifier.padding(innerPadding)
        )
    }
}

// ---------- Screen (calculates, connects) ----------

@Composable
fun TipCalculatorScreen(
    billText: String,
    onBillTextChange: (String) -> Unit,
    tipPercent: Int,
    isCustomTip: Boolean,
    onPresetSelected: (Int) -> Unit,
    onCustomSelected: () -> Unit,
    onCustomChange: (Int) -> Unit,
    people: Int,
    onPeopleChange: (Int) -> Unit,
    roundUp: Boolean,
    onRoundUpChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    val bill = billText.toDoubleOrNull() ?: 0.0
    val result = calculateTip(bill, tipPercent, people, roundUp)

    Column(
        modifier = modifier
            .fillMaxSize()
            .imePadding()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        ResultCard(result = result, people = people)
        BillInput(value = billText, onValueChange = onBillTextChange)
        TipSelector(
            tipPercent = tipPercent,
            isCustom = isCustomTip,
            onPresetSelected = onPresetSelected,
            onCustomSelected = onCustomSelected,
            onCustomChange = onCustomChange
        )
        PeopleStepper(people = people, onPeopleChange = onPeopleChange)
        RoundUpRow(checked = roundUp, onCheckedChange = onRoundUpChange)
    }
}

// ---------- Blocks (stateless) ----------

@Composable
fun ResultCard(
    result: TipResult,
    people: Int,
    modifier: Modifier = Modifier
) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        ),
        shape = MaterialTheme.shapes.extraLarge,
        modifier = modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = if (people == 1) "You pay" else "Each person pays",
                style = MaterialTheme.typography.titleMedium
            )
            Text(
                text = result.perPerson.toMoney(),
                style = MaterialTheme.typography.displayMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(8.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(24.dp)) {
                LabeledAmount(label = "Tip", amount = result.tip)
                LabeledAmount(label = "Total", amount = result.total)
            }
        }
    }
}

@Composable
fun LabeledAmount(label: String, amount: Double, modifier: Modifier = Modifier) {
    Column(modifier = modifier, horizontalAlignment = Alignment.CenterHorizontally) {
        Text(text = label, style = MaterialTheme.typography.labelMedium)
        Text(
            text = amount.toMoney(),
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.SemiBold
        )
    }
}

@Composable
fun BillInput(
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val focusManager = LocalFocusManager.current

    OutlinedTextField(
        value = value,
        onValueChange = { newText ->
            if (isValidBillText(newText)) {
                onValueChange(newText)
            }
        },
        label = { Text("Bill amount") },
        placeholder = { Text("0.00") },
        leadingIcon = { Text("💵", fontSize = 20.sp) },
        singleLine = true,
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Decimal,
            imeAction = ImeAction.Done
        ),
        keyboardActions = KeyboardActions(onDone = { focusManager.clearFocus() }),
        modifier = modifier.fillMaxWidth()
    )
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun TipSelector(
    tipPercent: Int,
    isCustom: Boolean,
    onPresetSelected: (Int) -> Unit,
    onCustomSelected: () -> Unit,
    onCustomChange: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier) {
        SectionTitle("Tip")
        FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            tipPresets.forEach { percent ->
                FilterChip(
                    selected = !isCustom && tipPercent == percent,
                    onClick = { onPresetSelected(percent) },
                    label = { Text("$percent%") }
                )
            }
            FilterChip(
                selected = isCustom,
                onClick = onCustomSelected,
                label = { Text("Custom") }
            )
        }

        if (isCustom) {
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "Custom tip: $tipPercent%",
                style = MaterialTheme.typography.bodyMedium
            )
            Slider(
                value = tipPercent.toFloat(),
                onValueChange = { onCustomChange(it.roundToInt()) },
                valueRange = 0f..30f,
                steps = 29
            )
        }
    }
}

@Composable
fun PeopleStepper(
    people: Int,
    onPeopleChange: (Int) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier) {
        SectionTitle("Split between")
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center
        ) {
            FilledTonalIconButton(
                onClick = { onPeopleChange(people - 1) },
                enabled = people > MIN_PEOPLE
            ) {
                Text("−", style = MaterialTheme.typography.titleLarge)
            }
            Text(
                text = if (people == 1) "1 person" else "$people people",
                style = MaterialTheme.typography.titleLarge,
                textAlign = TextAlign.Center,
                modifier = Modifier
                    .padding(horizontal = 24.dp)
                    .widthIn(min = 110.dp)
            )
            FilledTonalIconButton(
                onClick = { onPeopleChange(people + 1) },
                enabled = people < MAX_PEOPLE
            ) {
                Text("+", style = MaterialTheme.typography.titleLarge)
            }
        }
    }
}

@Composable
fun RoundUpRow(
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .toggleable(value = checked, onValueChange = onCheckedChange, role = Role.Switch),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text("Round up per person", style = MaterialTheme.typography.bodyLarge)
            Text(
                text = "No coins needed 🪙",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        Switch(checked = checked, onCheckedChange = null)
    }
}

@Composable
fun SectionTitle(text: String, modifier: Modifier = Modifier) {
    Text(
        text = text,
        style = MaterialTheme.typography.titleSmall,
        fontWeight = FontWeight.Bold,
        modifier = modifier.padding(bottom = 8.dp)
    )
}

// ---------- Previews ----------

@Preview(name = "Light", showSystemUi = true)
@Preview(name = "Dark", showSystemUi = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun TipCalculatorAppPreview() {
    TipCalculatorTheme {
        TipCalculatorApp()
    }
}

@Preview(name = "Filled in", showBackground = true, heightDp = 800)
@Composable
fun TipCalculatorScreenFilledPreview() {
    TipCalculatorTheme {
        Surface {
            TipCalculatorScreen(
                billText = "46.00",
                onBillTextChange = {},
                tipPercent = 20,
                isCustomTip = false,
                onPresetSelected = {},
                onCustomSelected = {},
                onCustomChange = {},
                people = 3,
                onPeopleChange = {},
                roundUp = false,
                onRoundUpChange = {}
            )
        }
    }
}

@Preview(name = "Custom tip, rounded", showBackground = true, heightDp = 800)
@Composable
fun TipCalculatorScreenCustomPreview() {
    TipCalculatorTheme {
        Surface {
            TipCalculatorScreen(
                billText = "123.45",
                onBillTextChange = {},
                tipPercent = 12,
                isCustomTip = true,
                onPresetSelected = {},
                onCustomSelected = {},
                onCustomChange = {},
                people = 4,
                onPeopleChange = {},
                roundUp = true,
                onRoundUpChange = {}
            )
        }
    }
}

@Preview(showBackground = true)
@Composable
fun ResultCardPreview() {
    TipCalculatorTheme {
        ResultCard(
            result = TipResult(tip = 9.2, total = 55.2, perPerson = 18.4),
            people = 3,
            modifier = Modifier.padding(16.dp)
        )
    }
}
```

> ⚠️ If you used **MyFirstApp**: change the first line to your package, and use `MyFirstAppTheme` (and its import) instead of `TipCalculatorTheme`.

---

## 12.8 The Power of Previews 👀

Look at the previews you get:

| Preview | What it shows |
|---|---|
| **Light** / **Dark** | The whole app, empty, in both modes 🌞🌙 |
| **Filled in** | $46.00, 20%, 3 people — check the numbers! |
| **Custom tip, rounded** | The slider is visible, rounding is on |
| **ResultCard** | Just the card, alone |

**Why is this so great?** You can see the app in **4 different situations** at once, **without running it** and **without tapping anything**. This is **only possible** because our Composables are **stateless** — they show whatever values you give them. 🎉

> 💡 **Professional habit:** For every important screen, make previews for: **empty**, **filled**, **special cases** (very long text, big numbers), and **dark mode**.

---

## 12.9 Test Your App — The Checklist ✅

Run the app and check **every** line. Testing like this is what real developers do before releasing an app. 🧪

### The math

| Bill | Tip | People | Round up | Expected per person | Expected tip | Expected total | ✅? |
|---|---|---|---|---|---|---|---|
| 46.00 | 20% | 3 | No | 18.40 | 9.20 | 55.20 | ☐ |
| 46.00 | 20% | 3 | Yes | 19.00 | 11.00 | 57.00 | ☐ |
| 100 | 15% | 1 | No | 115.00 | 15.00 | 115.00 | ☐ |
| 100 | 10% | 4 | No | 27.50 | 10.00 | 110.00 | ☐ |
| 100 | 10% | 4 | Yes | 28.00 | 12.00 | 112.00 | ☐ |
| 0 (empty) | 15% | 1 | No | 0.00 | 0.00 | 0.00 | ☐ |
| 50 | Custom 0% | 2 | No | 25.00 | 0.00 | 50.00 | ☐ |

### The inputs

| Check | ✅? |
|---|---|
| Typing letters in the bill does **nothing** | ☐ |
| Typing a second `.` does nothing | ☐ |
| A 3rd decimal (`46.257`) is blocked | ☐ |
| Typing just `.` doesn't crash (shows 0.00) | ☐ |
| The keyboard's ✅ key closes the keyboard | ☐ |
| `−` is grey at 1 person; `+` is grey at 20 | ☐ |
| Tapping **Custom** shows the slider; tapping **20%** hides it | ☐ |
| Tapping the **text** "Round up per person" flips the switch | ☐ |

### The app

| Check | ✅? |
|---|---|
| **Rotate** the phone — everything stays 🔄 | ☐ |
| Switch to **dark mode** — everything is readable 🌙 | ☐ |
| **Reset** ↻ clears everything and closes the keyboard | ☐ |
| On a **small** screen, you can scroll to everything | ☐ |
| Change the phone's **language/region** (e.g. to Germany) — money shows `€` | ☐ |
| Make the phone's **font** bigger (Settings → Display → Font size) — still looks OK | ☐ |

> 🌍 **To test another country:** Settings → System → Languages → add **Deutsch (Deutschland)** and move it to the top. Open the app: `18,40 €`! Don't forget to switch back. 😉

If something doesn't match, **debug** it:
1. Add `Log.d("TipCalc", "bill=$bill tip=$tipPercent people=$people result=$result")` in `TipCalculatorScreen`.
2. Look in **Logcat**. Thanks to the **data class**, `result` prints nicely: `TipResult(tip=9.2, total=55.2, perPerson=18.4)`. 🔍

---

## 12.10 What You Practiced 🎓

Look at everything you used in **one** app:

| Chapter | Skill used in the Tip Calculator |
|---|---|
| 2 | Math, `if`, functions, early `return` |
| 3 | Data class (`TipResult`), null safety (`toDoubleOrNull() ?: 0.0`), lambdas, `count`, `all` |
| 4 | Extension function (`toMoney`), `const val` |
| 5 | `Text` styles, `Icon`, `IconButton`, Modifiers |
| 6 | `Column`, `Row`, `FlowRow`, `weight`, `spacedBy`, `widthIn`, scrolling |
| 7 | `Card`, theme colors, shapes, dark mode |
| 8 | `rememberSaveable`, state hoisting, calculated values, one-way data flow |
| 9 | `OutlinedTextField`, Decimal keyboard, input filtering, `FilterChip`, `Slider`, `Switch`, `toggleable` |
| 11 | `Scaffold`, `CenterAlignedTopAppBar`, actions |

🎉 **You built a complete, polished, international app!** Be proud — this is real developer work.

---

## 12.11 Make It Even Better 🚀 (Challenges)

Try these on your own. There are hints, but no full answers — you've got this! 💪

### Challenge 1: A bigger choice of people ⭐
Change `MAX_PEOPLE` to `50`. What else do you need to change? (Hint: nothing! That's the power of constants. 😎)

### Challenge 2: "Service was…" 😊😐😞 ⭐
Add a row of three chips: **Great** (20%), **OK** (15%), **Bad** (10%). Tapping one sets the tip.
*Hint:* make a `List<Pair<String, Int>>` and loop over it with `FilterChip`s.

### Challenge 3: Show the tip as words ⭐⭐
Under the result card, show a small message:
- 0% → "*No tip 😶*"
- 1–14% → "*A small thank-you 🙂*"
- 15–19% → "*A good tip 😊*"
- 20%+ → "*Very generous! 🤩*"

*Hint:* a `when` with ranges (Chapter 2), calculated from `tipPercent`.

### Challenge 4: Accept commas too 🌍 ⭐⭐
Allow the user to type `46,50`.
*Hint:* in `onValueChange`, replace `,` with `.` **before** checking: `newText.replace(',', '.')`.

### Challenge 5: Copy the result 📋 ⭐⭐
Add a "Copy" button to the result card that copies `"Each person pays $18.40"` to the clipboard and shows a Snackbar "Copied! ✅".
*Hint:* `val clipboard = LocalClipboardManager.current` and `clipboard.setText(AnnotatedString("..."))`. You'll need a `SnackbarHostState` in the Scaffold (Chapter 11).

### Challenge 6: Share 📤 ⭐⭐⭐
Add a **Share** icon to the top bar that opens Android's share panel with the result text.
*Hint:*
```kotlin
val context = LocalContext.current
val intent = Intent(Intent.ACTION_SEND).apply {
    type = "text/plain"
    putExtra(Intent.EXTRA_TEXT, "Each person pays ${result.perPerson.toMoney()} 💰")
}
context.startActivity(Intent.createChooser(intent, "Share result"))
```
(We'll learn about **Intents** properly in Chapter 25.)

### Challenge 7: Your own theme 🎨 ⭐⭐
Use the **Material Theme Builder** (Chapter 7) to give the app a money-green or gold theme. Turn off dynamic color.

---

## 12.12 What Is Next?

🎉 **You finished Part 3 — Building Screens With Jetpack Compose!**

So far, every app had **one screen**. Real apps have **many**: a list, a details page, a settings page, a profile… 📱📱📱

In **Chapter 13: Moving Between Screens — Navigation**, you will learn:

- **Navigation Compose** — the official way to move between screens 🧭
- **Routes** — the "address" of each screen
- **Passing data** to a screen (like *which* note to open)
- The **Back button** — making it work correctly ⬅️
- **Bottom navigation** with real screens (better than the `when` from Chapter 11)
- **Type-safe** navigation with Kotlin

**Amazing work finishing Chapter 12! 🎉 You are now officially building real Android apps!**
