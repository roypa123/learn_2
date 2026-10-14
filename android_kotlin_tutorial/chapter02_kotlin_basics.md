# Chapter 2: Kotlin Basics — Talking to the Computer

> **What you will learn in this chapter**
>
> 1. Where to practice Kotlin code
> 2. How to show messages with `println`
> 3. Variables — boxes that hold values (`val` and `var`)
> 4. Types — numbers, text, true/false
> 5. Math in code
> 6. Working with text (Strings)
> 7. Changing one type into another
> 8. Comparing things (`==`, `>`, `<`) and logic (`&&`, `||`, `!`)
> 9. Making decisions with `if` and `when`
> 10. Repeating things with loops (`for`, `while`)
> 11. Writing your own functions
> 12. Using what you learned inside your Android app
>
> **Time needed:** about 3 to 4 hours. Go slowly. Type every example yourself!

---

## 2.1 Where Do I Practice?

In this chapter we learn **only the Kotlin language**. No phone screens yet.
So we want a place where we can type code and see the result **fast**.

You have two good choices:

### Choice A: Kotlin Playground (in your web browser) ⭐ easiest

1. Open your browser.
2. Go to: **https://play.kotlinlang.org**
3. You see some code already there. Delete it.
4. Type your code.
5. Click the **▶ Run** button (top right).
6. The result appears **below** the code.

✅ Nothing to install. Very fast. Great for this chapter.

### Choice B: A Scratch File in Android Studio

1. Open Android Studio (any project).
2. Click the menu **File → New → Scratch File**.
3. Choose **Kotlin**.
4. Type your code.
5. Click the green **▶** button at the top of the scratch file.
6. The result appears in a panel on the right or bottom.

> 💡 **Tip:** Use the **Kotlin Playground** for this chapter. It is simpler. In section 2.14 we will go back to Android Studio and use our new skills in the app.

---

## 2.2 Your First Kotlin Program

Type this in the Kotlin Playground:

```kotlin
fun main() {
    println("Hello, Kotlin!")
}
```

Click **Run**. You will see:

```
Hello, Kotlin!
```

🎉 You wrote your first Kotlin program!

### Every bit explained

| Piece | Meaning |
|---|---|
| `fun` | "Here is a **function**." (A function is a named list of steps.) |
| `main` | The name of the function. `main` is **special**: the computer **starts** here. |
| `()` | Brackets for inputs. This function has no inputs, so they are empty. |
| `{` | "The steps start here." |
| `println(...)` | "**Print** a **line**." It shows something on the screen, then goes to a new line. |
| `"Hello, Kotlin!"` | The text to show. Text is always inside double quotes `" "`. |
| `}` | "The steps end here." |

**Real-life example:**
`main` is like the **front door** of a house. When you visit, you always come in through the front door first. 🚪

> ⚠️ **In Android apps there is no `main` function you write.** Android has its own front door (`onCreate`, from Chapter 1). We use `main` only to practice.

### Many lines

```kotlin
fun main() {
    println("Line one")
    println("Line two")
    println("Line three")
}
```

Output:

```
Line one
Line two
Line three
```

The computer runs the code **from top to bottom**, one line at a time. Like reading a book. 📖

### `print` vs `println`

```kotlin
fun main() {
    print("A")
    print("B")
    println("C")
    println("D")
}
```

Output:

```
ABC
D
```

| Command | What it does |
|---|---|
| `print(...)` | Shows the text. **Stays on the same line.** |
| `println(...)` | Shows the text, **then moves to a new line.** |

---

## 2.3 Variables — Boxes That Hold Values 📦

A **variable** is like a **box with a name label**. You put a value inside. Later you can look inside the box.

```kotlin
fun main() {
    val name = "Roy"
    println(name)
}
```

Output:

```
Roy
```

### Every bit explained

```kotlin
    val name = "Roy"
```

| Piece | Meaning |
|---|---|
| `val` | "Make a new box." (`val` comes from the word **value**.) |
| `name` | The **label** on the box. |
| `=` | "Put this inside." (In code, `=` does **not** mean "equals". It means "**put into**".) |
| `"Roy"` | The value we put inside the box. |

Then:

```kotlin
    println(name)
```

- We did **not** use quotes here.
- Without quotes, Kotlin thinks: *"`name` is a box. Show what is **inside** the box."*

**Compare:**

```kotlin
fun main() {
    val name = "Roy"
    println(name)     // shows: Roy
    println("name")   // shows: name
}
```

| Code | Shows | Why |
|---|---|---|
| `println(name)` | `Roy` | No quotes → look inside the box called `name`. |
| `println("name")` | `name` | Quotes → show these exact letters. |

### `val` vs `var` — locked box vs open box

There are **two kinds** of boxes:

| Keyword | Kind of box | Can you change what is inside? |
|---|---|---|
| `val` | 🔒 **Locked box** | ❌ No. Once you put something in, it stays. |
| `var` | 🔓 **Open box** | ✅ Yes. You can put a new value in later. (`var` comes from **variable** = "can change".) |

**Example with `var`:**

```kotlin
fun main() {
    var score = 0
    println(score)   // 0

    score = 10
    println(score)   // 10

    score = 25
    println(score)   // 25
}
```

Output:

```
0
10
25
```

- The first time we write `var score = 0` → we **make** the box.
- After that, we write just `score = 10` → we **change** what is inside. (No `var` again!)

**Example with `val` — this is an error:**

```kotlin
fun main() {
    val birthYear = 2015
    birthYear = 2016   // ❌ ERROR: Val cannot be reassigned
}
```

Kotlin says: **"Val cannot be reassigned."** This means: *"You locked this box. You cannot change it."*

### Which one should I use?

> 💡 **Golden rule:** Always use `val` first. Change to `var` **only** if you really need to change the value later.

**Why?** Locked boxes are **safer**. Nobody can change them by mistake. Professional Kotlin developers use `val` most of the time.

**Real-life examples:**

| Thing | `val` or `var`? | Why |
|---|---|---|
| Your birthday | `val` | It never changes. |
| Your age | `var` | It changes every year. |
| Number of days in a week | `val` | Always 7. |
| Score in a game | `var` | It goes up while you play. |
| Your name | `val` | It (usually) does not change. |
| Battery level of a phone | `var` | It goes down and up. |

---

## 2.4 Types — What Kind of Value Is in the Box?

Every value has a **type**. The type says **what kind** of thing it is.

**Real-life example:** In a kitchen, you have a **water bottle**, a **rice jar**, and a **egg box**. You don't put eggs in the water bottle! 🥚💧 Each box is for one **type** of thing.

### The most common types

| Type | What it holds | Examples |
|---|---|---|
| `Int` | Whole numbers (no dot) | `0`, `7`, `-3`, `2025` |
| `Long` | Very big whole numbers | `8000000000L` |
| `Double` | Numbers with a dot (decimals) | `3.14`, `-0.5`, `99.99` |
| `Float` | Decimals, less exact (used for sizes in Android) | `1.5f` |
| `Boolean` | Only `true` or `false` | `true`, `false` |
| `Char` | **One** letter or symbol, in single quotes | `'A'`, `'z'`, `'7'`, `'?'` |
| `String` | Text (any number of letters), in double quotes | `"Hello"`, `"Roy"`, `""` |

### Writing the type yourself

You can **tell** Kotlin the type with a colon `:`:

```kotlin
fun main() {
    val age: Int = 10
    val price: Double = 49.99
    val isStudent: Boolean = true
    val firstLetter: Char = 'R'
    val city: String = "Mumbai"

    println(age)
    println(price)
    println(isStudent)
    println(firstLetter)
    println(city)
}
```

Output:

```
10
49.99
true
R
Mumbai
```

Read `val age: Int = 10` like this:
> *"Make a locked box named `age`. It **holds an Int**. Put `10` inside."*

### Kotlin can guess the type (type inference)

Most of the time, you **don't need** to write the type. Kotlin looks at the value and **guesses** correctly.

```kotlin
val age = 10          // Kotlin knows: Int
val price = 49.99     // Kotlin knows: Double
val isStudent = true  // Kotlin knows: Boolean
val city = "Mumbai"   // Kotlin knows: String
```

This is called **type inference** ("Kotlin figures out the type by itself").

> 💡 **Tip:** In Android Studio, click on a variable name and press **Ctrl + Shift + P**. It shows you the type Kotlin guessed.

### A box can only hold its own type

```kotlin
fun main() {
    var age = 10
    age = 11            // ✅ OK: still an Int
    age = "eleven"      // ❌ ERROR: Type mismatch
}
```

`age` is an **Int box**. You cannot put **text** in it. Kotlin says **"Type mismatch"** (the types do not match).

### When do you **need** to write the type?

When you make a box **without** a value yet:

```kotlin
fun main() {
    val answer: Int     // the type is needed: there is no value to guess from
    answer = 42
    println(answer)
}
```

### Little details about numbers

```kotlin
val small = 100           // Int
val big = 8_000_000_000L  // Long — notice the L at the end
val pi = 3.14             // Double
val width = 1.5f          // Float — notice the f at the end
```

- The underscore `_` in `8_000_000_000` is only to make it **easy to read**. Kotlin ignores it. Like writing `8,000,000,000`.
- `Int` can hold numbers up to about **2 billion** (2,147,483,647). For bigger numbers, use `Long`.

---

## 2.5 Naming Your Boxes — The Rules

### Rules (you **must** follow)

1. Names can have **letters**, **numbers**, and **underscore** `_`.
2. Names **cannot start** with a number.
3. Names **cannot have spaces**.
4. Names **cannot be special Kotlin words** like `val`, `var`, `fun`, `if`, `class`.
5. **BIG and small letters matter.** `score` and `Score` are two **different** boxes.

| Name | OK? | Why |
|---|---|---|
| `score` | ✅ | Good |
| `playerName` | ✅ | Good |
| `level2` | ✅ | Number is not at the start |
| `2level` | ❌ | Starts with a number |
| `player name` | ❌ | Has a space |
| `fun` | ❌ | Special Kotlin word |

### Style (you **should** follow)

Kotlin developers use **camelCase**:

- Start with a **small** letter.
- Each new word starts with a **BIG** letter.
- Like the humps of a camel 🐫: `myFavoriteColor`

| ❌ Not nice | ✅ Nice (camelCase) |
|---|---|
| `myfavoritecolor` | `myFavoriteColor` |
| `My_Favorite_Color` | `myFavoriteColor` |
| `x` (what is x?) | `totalPrice` |

> 💡 **Use names that explain themselves.** `totalPrice` is better than `tp`. Your code becomes easy to read, like a story.

---

## 2.6 Math in Code ➕➖✖️➗

Computers are very good at math.

### The math signs

| Sign | Meaning | Example | Result |
|---|---|---|---|
| `+` | Add | `5 + 3` | `8` |
| `-` | Subtract | `5 - 3` | `2` |
| `*` | Multiply (not `x`!) | `5 * 3` | `15` |
| `/` | Divide | `6 / 3` | `2` |
| `%` | Remainder (what is left over) | `7 % 3` | `1` |

```kotlin
fun main() {
    val a = 10
    val b = 3

    println(a + b)   // 13
    println(a - b)   // 7
    println(a * b)   // 30
    println(a / b)   // 3   ← surprise!
    println(a % b)   // 1
}
```

### ⚠️ Surprise: `10 / 3` is `3`, not `3.33`

When **both** numbers are `Int` (whole numbers), the answer is also an `Int`.
Kotlin **cuts off** the part after the dot. It does **not** round.

```kotlin
println(7 / 2)      // 3   (not 3.5!)
println(9 / 10)     // 0   (not 0.9!)
```

**How to get the decimal answer?** Make at least one number a `Double` (add `.0`):

```kotlin
println(7.0 / 2)    // 3.5
println(7 / 2.0)    // 3.5
println(9.0 / 10)   // 0.9
```

**Real-life example:** You have 7 cookies 🍪 and 2 friends. Each friend gets **3 whole cookies** (`7 / 2 = 3`). **1 cookie is left over** (`7 % 2 = 1`).

### What is `%` good for?

The remainder sign `%` is very useful:

```kotlin
fun main() {
    println(10 % 2)   // 0 → 10 is EVEN (no remainder)
    println(7 % 2)    // 1 → 7 is ODD
    println(125 % 60) // 5 → 125 seconds = 2 minutes and 5 seconds
}
```

> 💡 If `number % 2` is `0`, the number is **even**. If it is `1`, the number is **odd**.

### Order of math (like in school)

Kotlin follows school rules: **`*` `/` `%` first**, then **`+` `-`**.

```kotlin
println(2 + 3 * 4)     // 14  (3 * 4 first = 12, then 2 + 12)
println((2 + 3) * 4)   // 20  (brackets first = 5, then 5 * 4)
```

> 💡 **When unsure, use brackets `( )`.** They make the order clear for you and for the computer.

### Short ways to change a number

```kotlin
fun main() {
    var coins = 10

    coins = coins + 5   // long way: coins is now 15
    coins += 5          // short way: coins is now 20

    coins -= 3          // coins is now 17
    coins *= 2          // coins is now 34
    coins /= 2          // coins is now 17

    coins++             // add 1: coins is now 18
    coins--             // subtract 1: coins is now 17

    println(coins)      // 17
}
```

| Short | Long | Meaning |
|---|---|---|
| `x += 5` | `x = x + 5` | Add 5 to x |
| `x -= 5` | `x = x - 5` | Subtract 5 from x |
| `x *= 2` | `x = x * 2` | Multiply x by 2 |
| `x /= 2` | `x = x / 2` | Divide x by 2 |
| `x++` | `x = x + 1` | Add 1 |
| `x--` | `x = x - 1` | Subtract 1 |

**About `coins = coins + 5`:**
In school, this looks wrong! But remember: `=` means "**put into**". So it reads:
> *"Take what is in `coins`, add 5, and put the answer back into `coins`."*

> ⚠️ These only work with `var` (open box). A `val` cannot change.

### Mini example: shopping 🛒

```kotlin
fun main() {
    val applePrice = 30
    val appleCount = 4
    val milkPrice = 55

    val total = applePrice * appleCount + milkPrice

    println(total)   // 175
}
```

`30 * 4 = 120`, then `120 + 55 = 175`.

---

## 2.7 Working With Text (Strings) 📝

A `String` is **text**. It always goes inside **double quotes** `" "`.

### Joining text with `+`

```kotlin
fun main() {
    val firstName = "Roy"
    val lastName = "Paul"
    val fullName = firstName + " " + lastName
    println(fullName)   // Roy Paul
}
```

- `+` with Strings **joins** them together (it does not do math).
- `" "` is a String with just **one space** in it. Without it, we get `RoyPaul`.

### String templates with `$` ⭐ (the better way)

You saw this in Chapter 1: `"Hello $name!"`.

```kotlin
fun main() {
    val name = "Roy"
    val age = 10
    println("My name is $name and I am $age years old.")
}
```

Output:

```
My name is Roy and I am 10 years old.
```

- `$name` → "Put the value of `name` here."
- `$age` → "Put the value of `age` here." (It works with numbers too!)

### `${ }` — for more than one simple name

When you want to do **math** or something more inside the text, use `${ ... }` with curly brackets:

```kotlin
fun main() {
    val apples = 3
    val oranges = 5
    println("Total fruits: ${apples + oranges}")   // Total fruits: 8
    println("Total fruits: $apples + $oranges")    // Total fruits: 3 + 5
}
```

| Code | Result | Why |
|---|---|---|
| `"${apples + oranges}"` | `8` | Everything inside `${ }` is calculated first. |
| `"$apples + $oranges"` | `3 + 5` | Only the names are replaced. `+` stays as text. |

### Useful things a String can do

```kotlin
fun main() {
    val word = "Kotlin"

    println(word.length)        // 6        → how many letters
    println(word.uppercase())   // KOTLIN   → all BIG letters
    println(word.lowercase())   // kotlin   → all small letters
    println(word[0])            // K        → the first letter
    println(word[1])            // o        → the second letter
    println(word.first())       // K
    println(word.last())        // n
    println(word.reversed())    // niltoK
    println(word.contains("lin"))   // true
}
```

**The dot `.`** means: *"Ask this thing to do something."*
`word.uppercase()` = *"Hey `word`, give me your BIG-letter version."*

### ⚠️ Counting starts at 0!

```
 Letter:   K   o   t   l   i   n
 Number:   0   1   2   3   4   5
```

- `word[0]` is the **first** letter (`K`).
- `word[5]` is the **last** letter (`n`).
- `word[6]` → ❌ **crash!** There is no letter number 6.

> 💡 In programming, counting almost always starts at **0**, not 1. This feels strange at first. You will get used to it!

### Special characters

| Code | Meaning |
|---|---|
| `\n` | New line |
| `\t` | Tab (a big space) |
| `\"` | A double quote inside a String |
| `\$` | A real dollar sign |
| `\\` | A real backslash |

```kotlin
fun main() {
    println("Line 1\nLine 2")
    println("She said \"Hi!\"")
    println("Price: \$5")
}
```

Output:

```
Line 1
Line 2
She said "Hi!"
Price: $5
```

### Text with many lines: `"""`

```kotlin
fun main() {
    val poem = """
        Roses are red,
        Violets are blue,
        Kotlin is fun,
        And so are you!
    """.trimIndent()

    println(poem)
}
```

- Three quotes `"""` let you write **many lines** easily.
- `.trimIndent()` removes the extra spaces at the start of each line.

---

## 2.8 Changing One Type Into Another 🔄

Sometimes you have a value of one type, but you need another type.

```kotlin
fun main() {
    val text = "25"
    val number = text.toInt()
    println(number + 5)   // 30
}
```

- `"25"` is **text** (a String). You can't do math with text.
- `.toInt()` changes it into a **number**.

**Why does this matter in apps?** When a user types in a text box (for example their age), you always get **text**. You must change it to a number before doing math.

### The common changers

| Code | From → To | Example | Result |
|---|---|---|---|
| `.toInt()` | String/Double → Int | `"42".toInt()` | `42` |
| `.toDouble()` | String/Int → Double | `"3.5".toDouble()` | `3.5` |
| `.toString()` | anything → String | `42.toString()` | `"42"` |
| `.toLong()` | → Long | `"9".toLong()` | `9L` |
| `.toFloat()` | → Float | `2.toFloat()` | `2.0` |

```kotlin
fun main() {
    val price = 9.99
    println(price.toInt())     // 9   ← cuts off, does not round

    val count = 7
    println(count.toDouble())  // 7.0
}
```

### ⚠️ What if the text is not a number?

```kotlin
val bad = "hello".toInt()   // ❌ CRASH! (NumberFormatException)
```

The app **crashes**. 💥 To be safe, use **`toIntOrNull()`**:

```kotlin
fun main() {
    val a = "42".toIntOrNull()
    val b = "hello".toIntOrNull()

    println(a)   // 42
    println(b)   // null
}
```

- If it works → you get the number.
- If it does not work → you get **`null`** (which means "**nothing**", an empty box) instead of a crash.

We will learn all about `null` in Chapter 3. For now, remember: **`toIntOrNull()` is the safe way.**

---

## 2.9 Comparing Things and Logic ⚖️

### Comparing — the answer is always `true` or `false`

| Sign | Meaning | Example | Result |
|---|---|---|---|
| `==` | Is equal to? | `5 == 5` | `true` |
| `!=` | Is NOT equal to? | `5 != 3` | `true` |
| `>` | Is bigger than? | `5 > 3` | `true` |
| `<` | Is smaller than? | `5 < 3` | `false` |
| `>=` | Bigger **or** equal? | `5 >= 5` | `true` |
| `<=` | Smaller **or** equal? | `4 <= 3` | `false` |

```kotlin
fun main() {
    val age = 12
    println(age > 10)    // true
    println(age == 13)   // false
    println(age != 13)   // true

    val name = "Roy"
    println(name == "Roy")   // true
    println(name == "roy")   // false  ← BIG and small letters matter
}
```

> ⚠️ **Do not mix up `=` and `==`!**
> - `=` → "**put into**" a box.
> - `==` → "**are they the same?**" (asks a question)

### Logic: AND, OR, NOT

Sometimes you need to check **more than one thing**.

| Sign | Name | Meaning |
|---|---|---|
| `&&` | AND | `true` only if **both** sides are true |
| `\|\|` | OR | `true` if **at least one** side is true |
| `!` | NOT | Flips it: `true` → `false`, `false` → `true` |

**Real-life examples:**

- **AND:** *"You can play outside if your homework is done **AND** it is not raining."* Both must be true.
- **OR:** *"You can have juice **OR** milk."* One is enough.
- **NOT:** *"It is **NOT** raining."*

```kotlin
fun main() {
    val homeworkDone = true
    val isRaining = false

    val canPlay = homeworkDone && !isRaining
    println(canPlay)   // true

    val hasJuice = false
    val hasMilk = true
    val hasDrink = hasJuice || hasMilk
    println(hasDrink)  // true
}
```

Let's read `homeworkDone && !isRaining` slowly:

1. `homeworkDone` → `true`
2. `!isRaining` → NOT `false` → `true`
3. `true && true` → `true` ✅

### Truth tables (the full picture)

**AND `&&`:**

| A | B | A && B |
|---|---|---|
| true | true | **true** |
| true | false | false |
| false | true | false |
| false | false | false |

**OR `||`:**

| A | B | A \|\| B |
|---|---|---|
| true | true | **true** |
| true | false | **true** |
| false | true | **true** |
| false | false | false |

---

## 2.10 Making Decisions With `if` 🤔

Programs often need to **choose**: *"If this is true, do that."*

### Simple `if`

```kotlin
fun main() {
    val temperature = 35

    if (temperature > 30) {
        println("It is hot! Drink water. 💧")
    }

    println("Have a nice day!")
}
```

Output:

```
It is hot! Drink water. 💧
Have a nice day!
```

| Piece | Meaning |
|---|---|
| `if` | "Check this:" |
| `(temperature > 30)` | The **question**. It must give `true` or `false`. |
| `{ ... }` | Steps to do **only if** the answer is `true`. |

If `temperature` was `20`, the question is `false`. Kotlin **skips** the `{ }` part. Only `Have a nice day!` is shown.

### `if` ... `else`

```kotlin
fun main() {
    val age = 15

    if (age >= 18) {
        println("You can vote.")
    } else {
        println("You are too young to vote.")
    }
}
```

Output:

```
You are too young to vote.
```

- `else` means "**otherwise**".
- **Exactly one** of the two parts runs. Never both.

### `if` ... `else if` ... `else` — many choices

```kotlin
fun main() {
    val marks = 72

    if (marks >= 90) {
        println("Grade A ⭐")
    } else if (marks >= 75) {
        println("Grade B")
    } else if (marks >= 50) {
        println("Grade C")
    } else {
        println("Try again")
    }
}
```

Output:

```
Grade C
```

How Kotlin thinks, step by step:

1. Is `72 >= 90`? No. ➡️ go on.
2. Is `72 >= 75`? No. ➡️ go on.
3. Is `72 >= 50`? **Yes!** ➡️ print `Grade C` and **stop checking**.

> 💡 Kotlin checks from **top to bottom** and stops at the **first** `true`.

### `if` can give back a value ⭐ (Kotlin special)

In Kotlin, `if` can **produce an answer** and you can put it in a box:

```kotlin
fun main() {
    val number = 7
    val kind = if (number % 2 == 0) "even" else "odd"
    println("$number is $kind")   // 7 is odd
}
```

Read it as:
> *"`kind` is: if `number % 2 == 0` then `"even"`, else `"odd"`."*

This is short and clean. You will see it often in Android code.

---

## 2.11 Making Decisions With `when` 🎯

When you have **many choices**, `if ... else if ... else if ...` gets long. Kotlin has a cleaner tool: **`when`**.

```kotlin
fun main() {
    val day = 3

    when (day) {
        1 -> println("Monday")
        2 -> println("Tuesday")
        3 -> println("Wednesday")
        4 -> println("Thursday")
        5 -> println("Friday")
        6, 7 -> println("Weekend! 🎉")
        else -> println("Not a real day")
    }
}
```

Output:

```
Wednesday
```

| Piece | Meaning |
|---|---|
| `when (day)` | "Look at the value of `day`." |
| `1 -> ...` | "If it is `1`, do this." The arrow `->` means "**then do**". |
| `6, 7 -> ...` | "If it is `6` **or** `7`, do this." |
| `else -> ...` | "If **nothing** above matched, do this." |

**Real-life example:** A lift (elevator) 🛗. You press a number → it goes to that floor.

### `when` with ranges

```kotlin
fun main() {
    val marks = 85

    when (marks) {
        in 90..100 -> println("Grade A")
        in 75..89 -> println("Grade B")
        in 50..74 -> println("Grade C")
        else -> println("Try again")
    }
}
```

Output: `Grade B`

- `90..100` means "**all numbers from 90 to 100**" (including both). This is called a **range**.
- `in` means "**is inside**".

### `when` without a value (like many `if`s)

```kotlin
fun main() {
    val temperature = 8

    when {
        temperature < 0 -> println("Freezing! 🥶")
        temperature < 15 -> println("Cold. Wear a jacket.")
        temperature < 30 -> println("Nice weather. 😊")
        else -> println("Hot! 🥵")
    }
}
```

Output: `Cold. Wear a jacket.`

Here `when` has **no** `( )` after it. Each line has its own full question.

### `when` gives back a value too

```kotlin
fun main() {
    val light = "red"

    val action = when (light) {
        "red" -> "Stop 🛑"
        "yellow" -> "Get ready"
        "green" -> "Go 🟢"
        else -> "Be careful"
    }

    println(action)   // Stop 🛑
}
```

> 💡 **When to use what?**
> - **1 or 2 choices** → `if` / `else`
> - **3 or more choices** → `when`

---

## 2.12 Repeating Things With Loops 🔁

Imagine you must print "Hello" **100 times**. You don't want to write `println` 100 times! A **loop** repeats code for you.

### `for` loop with a range

```kotlin
fun main() {
    for (i in 1..5) {
        println("Hello number $i")
    }
}
```

Output:

```
Hello number 1
Hello number 2
Hello number 3
Hello number 4
Hello number 5
```

| Piece | Meaning |
|---|---|
| `for` | "Repeat for each..." |
| `i` | A box that holds the **current number**. It changes every round. (You can name it anything.) |
| `in 1..5` | "...number from 1 to 5." |
| `{ ... }` | The steps to repeat. |

**What happens, round by round:**

| Round | `i` is | Prints |
|---|---|---|
| 1 | 1 | Hello number 1 |
| 2 | 2 | Hello number 2 |
| 3 | 3 | Hello number 3 |
| 4 | 4 | Hello number 4 |
| 5 | 5 | Hello number 5 |

### Different kinds of ranges

| Code | Numbers you get | Meaning |
|---|---|---|
| `1..5` | 1, 2, 3, 4, 5 | 1 **to** 5 (5 included) |
| `1..<5` | 1, 2, 3, 4 | 1 **up to but not** 5 |
| `1 until 5` | 1, 2, 3, 4 | Same as `1..<5` (older style) |
| `5 downTo 1` | 5, 4, 3, 2, 1 | Counting **down** |
| `0..10 step 2` | 0, 2, 4, 6, 8, 10 | Jump by 2 |
| `10 downTo 0 step 5` | 10, 5, 0 | Down, jump by 5 |

**Rocket countdown 🚀:**

```kotlin
fun main() {
    for (i in 5 downTo 1) {
        println(i)
    }
    println("Blast off! 🚀")
}
```

Output:

```
5
4
3
2
1
Blast off! 🚀
```

### `for` loop over the letters of a String

```kotlin
fun main() {
    for (letter in "Kotlin") {
        println(letter)
    }
}
```

Output:

```
K
o
t
l
i
n
```

### `repeat` — the simplest loop

When you just want to do something **N times**:

```kotlin
fun main() {
    repeat(3) {
        println("Hip hip hooray! 🎉")
    }
}
```

Output:

```
Hip hip hooray! 🎉
Hip hip hooray! 🎉
Hip hip hooray! 🎉
```

### `while` loop — repeat **while** something is true

```kotlin
fun main() {
    var water = 0

    while (water < 5) {
        water++
        println("Glasses of water: $water")
    }

    println("Done for today! 💧")
}
```

Output:

```
Glasses of water: 1
Glasses of water: 2
Glasses of water: 3
Glasses of water: 4
Glasses of water: 5
Done for today! 💧
```

How it works:

1. Check: is `water < 5`? → yes → do the steps.
2. Check again → ... → repeat.
3. When `water` becomes `5`, the check is `false` → **stop**.

> 💡 **`for` or `while`?**
> - You **know** how many times → `for`
> - You repeat **until something happens** → `while`

> ⚠️ **Danger: never-ending loop!**
> ```kotlin
> var x = 0
> while (x < 5) {
>     println(x)   // ❌ we forgot x++
> }
> ```
> `x` is **always** 0. `0 < 5` is **always** true. The loop never stops! 😱
> If this happens, press the **Stop ■** button.

### `do ... while` — do it at least once

```kotlin
fun main() {
    var count = 10
    do {
        println("Count is $count")
        count++
    } while (count < 3)
}
```

Output:

```
Count is 10
```

`do ... while` runs the steps **first**, then checks. So it always runs **at least once**, even if the check is `false`.

### `break` and `continue` — controlling the loop

| Word | Meaning |
|---|---|
| `break` | **Stop the loop now.** Jump out completely. |
| `continue` | **Skip the rest of this round.** Go to the next round. |

```kotlin
fun main() {
    for (i in 1..10) {
        if (i == 3) continue   // skip 3
        if (i == 6) break      // stop at 6
        println(i)
    }
}
```

Output:

```
1
2
4
5
```

**Real-life example:** You eat grapes one by one 🍇.
- A grape is bad → **`continue`** (throw it away, take the next one).
- You are full → **`break`** (stop eating).

---

## 2.13 Writing Your Own Functions 🛠️

A **function** is a **named list of steps**. You write it once. Then you can **use (call) it many times**.

**Real-life example:** A recipe called "**Make Tea**" ☕. You write the steps once. Every time you want tea, you just say "Make Tea!" — you don't explain every step again.

### A simple function

```kotlin
fun sayHello() {
    println("Hello!")
    println("Welcome to Kotlin.")
}

fun main() {
    sayHello()
    sayHello()
}
```

Output:

```
Hello!
Welcome to Kotlin.
Hello!
Welcome to Kotlin.
```

| Piece | Meaning |
|---|---|
| `fun sayHello() { ... }` | **Making** (defining) the function. Like writing the recipe. |
| `sayHello()` | **Using** (calling) the function. Like following the recipe. The `()` are needed! |

### Functions with inputs (parameters)

```kotlin
fun greet(name: String) {
    println("Hello, $name! 👋")
}

fun main() {
    greet("Roy")
    greet("Asha")
    greet("Ben")
}
```

Output:

```
Hello, Roy! 👋
Hello, Asha! 👋
Hello, Ben! 👋
```

- `name: String` → this function needs an **input** called `name`, and it must be a `String`.
- The input is called a **parameter**.
- When we call `greet("Roy")`, the value `"Roy"` goes into `name`.

### Many inputs

```kotlin
fun introduce(name: String, age: Int) {
    println("I am $name. I am $age years old.")
}

fun main() {
    introduce("Roy", 10)
    introduce("Asha", 12)
}
```

- Inputs are separated by a **comma** `,`.
- The **order** matters: first a `String`, then an `Int`.

### Functions that give back an answer (return)

Some functions **calculate something** and **give the answer back**.

```kotlin
fun add(a: Int, b: Int): Int {
    return a + b
}

fun main() {
    val result = add(3, 4)
    println(result)            // 7
    println(add(10, 20))       // 30
}
```

| Piece | Meaning |
|---|---|
| `(a: Int, b: Int)` | Two inputs, both `Int`. |
| `: Int` after the `)` | "This function **gives back** an `Int`." This is the **return type**. |
| `return a + b` | "Calculate `a + b` and **give it back**." |
| `val result = add(3, 4)` | Call the function and put the answer in a box. |

**Real-life example:** A **juice machine** 🧃. You put in fruits (inputs). The machine gives back juice (return value).

> ⚠️ After `return`, the function **stops**. Lines after `return` do not run.

### Short functions — one line

If the function only returns **one thing**, you can write it shorter:

```kotlin
fun add(a: Int, b: Int): Int = a + b

fun square(n: Int) = n * n      // Kotlin guesses the return type: Int

fun isEven(n: Int) = n % 2 == 0 // returns a Boolean

fun main() {
    println(add(2, 3))     // 5
    println(square(4))     // 16
    println(isEven(7))     // false
}
```

### Default values

You can give an input a **default** value. Then the caller can **skip** it.

```kotlin
fun orderPizza(size: String = "Medium", cheese: Boolean = true) {
    println("Pizza: $size, extra cheese: $cheese 🍕")
}

fun main() {
    orderPizza()                    // Pizza: Medium, extra cheese: true
    orderPizza("Large")             // Pizza: Large, extra cheese: true
    orderPizza("Small", false)      // Pizza: Small, extra cheese: false
}
```

### Named arguments ⭐ (very common in Compose!)

You can write the **name** of the input when you call the function:

```kotlin
fun main() {
    orderPizza(cheese = false)                  // Pizza: Medium, extra cheese: false
    orderPizza(cheese = true, size = "Large")   // order does not matter with names
}
```

- `cheese = false` → "Put `false` into the input named `cheese`."
- With names, the **order does not matter**, and the code is **easier to read**.

> 💡 **Remember Chapter 1?**
> ```kotlin
> Greeting(
>     name = "Android",
>     modifier = Modifier.padding(innerPadding)
> )
> ```
> These are **named arguments**! And in `fun Greeting(name: String, modifier: Modifier = Modifier)`, the `= Modifier` is a **default value**. Now you understand it fully! 🎉

### Functions that return nothing: `Unit`

`sayHello()` gives nothing back. In Kotlin, "nothing back" is called **`Unit`**. You don't need to write it:

```kotlin
fun sayHello(): Unit {    // you CAN write : Unit
    println("Hello!")
}

fun sayHello2() {         // but usually we don't. Same thing.
    println("Hello!")
}
```

### Variables live inside their `{ }` (scope)

```kotlin
fun makeTea() {
    val sugar = 2
    println("Tea with $sugar spoons of sugar")
}

fun main() {
    makeTea()
    println(sugar)   // ❌ ERROR: Unresolved reference: sugar
}
```

- `sugar` was made **inside** `makeTea`. It only lives **inside** those `{ }`.
- Outside, nobody knows it. This is called **scope**.

**Real-life example:** A toy in **your room** 🧸. People in the kitchen can't see it.

---

## 2.14 Use It in Your Android App! 📱

Let us use our new skills in the app from Chapter 1.

### Step 1: Open the project

Open **MyFirstApp** in Android Studio. Open `MainActivity.kt`.

### Step 2: Add a helper function

Add this function **below** the `Greeting` function (outside of any other `{ }`):

```kotlin
fun ageMessage(age: Int): String {
    return when {
        age < 13 -> "You are a kid. Have fun learning! 🧒"
        age < 20 -> "You are a teenager. Great time to start coding! 🧑"
        else -> "It is never too late to learn! 👍"
    }
}
```

- Input: `age` (an `Int`).
- Output: a `String` message.
- It uses `when` to choose the message.

### Step 3: Use it in `Greeting`

Change the `Greeting` function to this:

```kotlin
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    val age = 10
    val nextYearAge = age + 1

    Text(
        text = "Hello $name!\n" +
            "You are $age years old.\n" +
            "Next year you will be $nextYearAge.\n" +
            ageMessage(age),
        modifier = modifier
    )
}
```

### Every bit explained

| Line | Meaning |
|---|---|
| `val age = 10` | A locked box with the age. |
| `val nextYearAge = age + 1` | Math! `10 + 1 = 11`. |
| `"Hello $name!\n"` | String template + new line `\n`. |
| `+` at the end of lines | **Joins** the Strings together. We split it over many lines only to make it easy to read. |
| `ageMessage(age)` | **Calls** our function. It gives back a message String. |

### Step 4: Run it

Click **▶ Run** (or look at the **Preview**). You will see:

```
Hello Roy!
You are 10 years old.
Next year you will be 11.
You are a kid. Have fun learning! 🧒
```

🎉 You used **variables**, **math**, **String templates**, **when**, and **your own function** — in a **real Android app**!

### Bonus: Print messages to Logcat

`println` does not show on the phone screen. But Android has a message window called **Logcat**. Developers use it to check what the app is doing.

Add this inside `onCreate`, after `super.onCreate(savedInstanceState)`:

```kotlin
        for (i in 1..3) {
            Log.d("MyFirstApp", "Loop round number $i")
        }
```

- When the word `Log` turns red, click it and press **Alt + Enter** → **Import**. It adds `import android.util.Log`.
- `Log.d(...)` → "write a **debug** message".
- `"MyFirstApp"` → a **tag** (a label) so you can find your messages.
- The second part is the message.

Run the app. At the bottom, open **Logcat**. In its search box, type `MyFirstApp`. You will see:

```
Loop round number 1
Loop round number 2
Loop round number 3
```

> 💡 **Logcat is your best friend** when something goes wrong. You will use it a lot.

---

## 2.15 Common Mistakes and Fixes 🔧

| Mistake | Example | Error message | Fix |
|---|---|---|---|
| Changing a `val` | `val x = 1` then `x = 2` | *Val cannot be reassigned* | Use `var`, or don't change it. |
| Wrong type | `var age = 10` then `age = "ten"` | *Type mismatch* | Put the right type in the box. |
| Forgot quotes | `println(Hello)` | *Unresolved reference: Hello* | `println("Hello")` |
| Single quotes for text | `val s = 'Hello'` | *Too many characters in a character literal* | Use **double** quotes for Strings: `"Hello"`. |
| `=` instead of `==` | `if (x = 5)` | *Assignments are not expressions...* | Use `==` to compare. |
| Wrong letter size | `Println("Hi")` | *Unresolved reference: Println* | `println` with a small `p`. |
| Missing bracket | `fun main() { println("Hi")` | *Expecting '}'* | Every `{` needs a `}`. |
| Integer division | `7 / 2` gives `3` | (no error, wrong answer!) | Use `7.0 / 2` for `3.5`. |
| Counting from 1 | `"Cat"[3]` | *StringIndexOutOfBoundsException* (crash) | Counting starts at `0`. Last is `[2]`. |
| Text to number crash | `"abc".toInt()` | *NumberFormatException* (crash) | Use `toIntOrNull()`. |

---

## 2.16 Summary — What You Learned 🎓

✅ **`println`** shows text. **`main`** is where a Kotlin practice program starts.

✅ **Variables** are named boxes:
- `val` = 🔒 locked (can't change) — **use this first**
- `var` = 🔓 open (can change)

✅ **Types:** `Int`, `Long`, `Double`, `Float`, `Boolean`, `Char`, `String`. Kotlin can **guess** the type.

✅ **Names** use **camelCase**: `myFavoriteColor`.

✅ **Math:** `+ - * / %`. `Int / Int` cuts off decimals. `%` gives the remainder.

✅ **Strings:** `"Hello $name"`, `"${a + b}"`, `.length`, `.uppercase()`, counting starts at **0**.

✅ **Convert:** `.toInt()`, `.toDouble()`, `.toString()`, safe: `.toIntOrNull()`.

✅ **Compare:** `== != > < >= <=`. **Logic:** `&&` (and), `||` (or), `!` (not).

✅ **Decisions:** `if / else if / else`, and `when` for many choices. Both can **give back a value**.

✅ **Loops:** `for (i in 1..5)`, `downTo`, `step`, `..<`, `repeat(n)`, `while`, `do-while`, `break`, `continue`.

✅ **Functions:** inputs (parameters), `return`, one-line `=` functions, **default values**, **named arguments**.

✅ You used all of this inside your **Android app**, and printed messages to **Logcat**.

---

## 2.17 Practice Time 🏋️

Try each task in the **Kotlin Playground**. Answers are below — try first! 💪

**Task 1 — About me:**
Make variables for your name, age, and favorite food. Print:
`My name is Roy. I am 10. I love pizza.`

**Task 2 — Rectangle:**
A rectangle has width `8` and height `5`. Print its **area** (width × height) and **perimeter** (2 × (width + height)).

**Task 3 — Even or odd:**
Make a variable `number = 17`. Use `if` to print `17 is even` or `17 is odd`.

**Task 4 — Times table:**
Use a `for` loop to print the 5 times table, from `5 x 1 = 5` to `5 x 10 = 50`.

**Task 5 — Sum:**
Use a loop to add all numbers from 1 to 100. Print the total.

**Task 6 — Weather with `when`:**
Make `val weather = "rainy"`. Use `when` to print:
- `"sunny"` → `Wear sunglasses 😎`
- `"rainy"` → `Take an umbrella ☂️`
- `"snowy"` → `Wear a warm coat 🧥`
- anything else → `Have a good day!`

**Task 7 — Function:**
Write a function `celsiusToFahrenheit(c: Double): Double`.
The formula is: `F = C × 9 / 5 + 32`.
Print the answer for `0.0`, `37.0`, and `100.0`.

**Task 8 — FizzBuzz (a famous puzzle!) 🧩:**
Print the numbers from 1 to 15. But:
- If the number can be divided by **3** → print `Fizz` instead.
- If it can be divided by **5** → print `Buzz` instead.
- If by **both 3 and 5** → print `FizzBuzz` instead.

---

### Answers

**Task 1:**

```kotlin
fun main() {
    val name = "Roy"
    val age = 10
    val food = "pizza"
    println("My name is $name. I am $age. I love $food.")
}
```

**Task 2:**

```kotlin
fun main() {
    val width = 8
    val height = 5
    val area = width * height
    val perimeter = 2 * (width + height)
    println("Area: $area")            // Area: 40
    println("Perimeter: $perimeter")  // Perimeter: 26
}
```

**Task 3:**

```kotlin
fun main() {
    val number = 17
    if (number % 2 == 0) {
        println("$number is even")
    } else {
        println("$number is odd")
    }
}
```

Output: `17 is odd`

**Task 4:**

```kotlin
fun main() {
    for (i in 1..10) {
        println("5 x $i = ${5 * i}")
    }
}
```

**Task 5:**

```kotlin
fun main() {
    var total = 0
    for (i in 1..100) {
        total += i
    }
    println(total)   // 5050
}
```

`total` must be a `var`, because it changes in every round.

**Task 6:**

```kotlin
fun main() {
    val weather = "rainy"
    when (weather) {
        "sunny" -> println("Wear sunglasses 😎")
        "rainy" -> println("Take an umbrella ☂️")
        "snowy" -> println("Wear a warm coat 🧥")
        else -> println("Have a good day!")
    }
}
```

**Task 7:**

```kotlin
fun celsiusToFahrenheit(c: Double): Double {
    return c * 9 / 5 + 32
}

fun main() {
    println(celsiusToFahrenheit(0.0))    // 32.0
    println(celsiusToFahrenheit(37.0))   // 98.6
    println(celsiusToFahrenheit(100.0))  // 212.0
}
```

> ℹ️ For `37.0` you may see `98.60000000000001`. This is normal! Computers store decimals in a way that is sometimes a tiny bit off.

**Task 8:**

```kotlin
fun main() {
    for (i in 1..15) {
        when {
            i % 15 == 0 -> println("FizzBuzz")
            i % 3 == 0 -> println("Fizz")
            i % 5 == 0 -> println("Buzz")
            else -> println(i)
        }
    }
}
```

**Why check `15` first?** `when` stops at the **first** true line. If `% 3` was first, `15` would print `Fizz` and never reach `FizzBuzz`. A number divisible by both 3 and 5 is divisible by 15.

Output:

```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
```

---

## 2.18 What Is Next?

In **Chapter 3: Kotlin Next Steps**, you will learn:

- **Null safety** — what `null` is, and how Kotlin protects you from crashes (`?`, `?.`, `?:`, `!!`)
- **Lists** — many values in one box 📋
- **Maps** — pairs like a dictionary 📖
- **Classes and objects** — make your own types (like `Student`, `Car`)
- **Data classes** — the most-used kind of class in Android
- **Lambdas** — small functions you can pass around (Compose uses them everywhere!)

**Great job finishing Chapter 2! 🎉 You can now speak basic Kotlin!**
