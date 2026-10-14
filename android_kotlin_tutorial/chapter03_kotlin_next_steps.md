# Chapter 3: Kotlin Next Steps — Nulls, Lists, Classes, and Lambdas

> **What you will learn in this chapter**
>
> 1. What `null` is, and how Kotlin protects you from crashes (null safety)
> 2. Lists — many values in one box 📋
> 3. Sets — lists with no repeats
> 4. Maps — pairs, like a dictionary 📖
> 5. Classes and objects — making your own types
> 6. Data classes — the most-used kind of class in Android
> 7. Lambdas — small functions you can pass around
> 8. Super-powers for lists: `filter`, `map`, `sortedBy`, and more
> 9. Using all of this inside your Android app
>
> **Time needed:** about 4 to 5 hours. This chapter is very important. Take your time! 🐢
>
> **Where to practice:** Kotlin Playground — **https://play.kotlinlang.org** (same as Chapter 2).

---

## 3.1 Null — The Empty Box 📦❓

### What is `null`?

In Chapter 2, every box had something inside.
But sometimes, a box is **empty**. There is **nothing** in it.

In Kotlin, "**nothing**" is called **`null`**.

**Real-life examples:**

| Question | Answer could be `null` because… |
|---|---|
| What is your middle name? | Many people **don't have** one. |
| What is your phone number? | A small child may **not have** a phone. |
| What did the user type in the search box? | They may not have typed **anything yet**. |
| Which photo did the user pick? | They may have **cancelled**. |

### Why is `null` dangerous?

Imagine you ask a box: *"How many letters do you have?"*
But the box is **empty** (`null`). There are no letters. There is no word at all!
In many older languages, the app would **crash** 💥. This crash is so famous it has a name: **NullPointerException** (NPE).

The person who invented `null` (Tony Hoare) called it his "**billion-dollar mistake**" because it caused so many crashes.

### Kotlin's solution: null safety 🛡️

Kotlin has a simple rule:

> **A normal box can NEVER be empty.**
> **If a box is allowed to be empty, you must add a `?` to its type.**

```kotlin
fun main() {
    val name: String = "Roy"       // normal box: can never be null
    val middleName: String? = null // "?" box: can be null

    println(name)        // Roy
    println(middleName)  // null
}
```

| Type | Can it be `null`? | Read it as |
|---|---|---|
| `String` | ❌ No | "always a String" |
| `String?` | ✅ Yes | "a String **or** nothing" |
| `Int` | ❌ No | "always an Int" |
| `Int?` | ✅ Yes | "an Int **or** nothing" |

**Try to put `null` in a normal box:**

```kotlin
val name: String = null   // ❌ ERROR: Null can not be a value of a non-null type String
```

Kotlin stops you **before** the app even runs. That is the magic! ✨

### You can't use a `?` box directly

```kotlin
fun main() {
    val middleName: String? = "Kumar"
    println(middleName.length)   // ❌ ERROR
}
```

Error:
> *Only safe (?.) or non-null asserted (!!.) calls are allowed on a nullable receiver of type String?*

In simple words: *"This box **might** be empty. I won't let you ask it for `length` without being careful."*

Kotlin gives you **4 careful ways**. Let's learn each one.

---

### Way 1: Check with `if` (smart cast)

```kotlin
fun main() {
    val middleName: String? = "Kumar"

    if (middleName != null) {
        println(middleName.length)   // ✅ 5
    } else {
        println("No middle name")
    }
}
```

- Inside `if (middleName != null) { ... }`, Kotlin **knows** the box is not empty.
- So it treats `middleName` as a normal `String`. This is called a **smart cast** (Kotlin is smart 🧠).

---

### Way 2: The safe call `?.` ⭐

```kotlin
fun main() {
    val a: String? = "Kumar"
    val b: String? = null

    println(a?.length)   // 5
    println(b?.length)   // null   (no crash!)
}
```

`?.` means:
> *"**If** the box has something, do this. **If** it is empty, just give back `null` and don't crash."*

**Real-life example:** *"If there is milk in the fridge, pour me a glass."* 🥛
If there is no milk, nothing happens. Nobody gets hurt.

You can make a **chain**:

```kotlin
val shout: String? = b?.uppercase()?.reversed()
```

If any step is `null`, the whole answer is `null`.

---

### Way 3: The Elvis operator `?:` ⭐ (give a backup value)

```kotlin
fun main() {
    val nickname: String? = null

    val shownName = nickname ?: "Friend"
    println("Hello, $shownName!")   // Hello, Friend!
}
```

`?:` means:
> *"Use the left side. **If it is `null`**, use the right side instead."*

**Why "Elvis"?** Turn your head to the left and look at `?:` — it looks like the hair and eyes of the singer Elvis Presley! 🕺

**Very common together with `?.`:**

```kotlin
fun main() {
    val word: String? = null
    val letters = word?.length ?: 0
    println(letters)   // 0
}
```

Read it as: *"Give me the length of `word`. If `word` is empty, give me `0`."*

**Remember `toIntOrNull()` from Chapter 2?** Now we can use it nicely:

```kotlin
fun main() {
    val typed = "abc"
    val age = typed.toIntOrNull() ?: 0
    println(age)   // 0   (no crash!)
}
```

---

### Way 4: The "I promise" operator `!!` ⚠️ (use almost never)

```kotlin
fun main() {
    val a: String? = "Kumar"
    println(a!!.length)   // 5

    val b: String? = null
    println(b!!.length)   // 💥 CRASH: NullPointerException
}
```

`!!` means:
> *"Trust me, Kotlin! This box is **not** empty. If I'm wrong, crash the app."*

> ⚠️ **Rule:** Avoid `!!`. If you write `!!`, you are turning off Kotlin's protection. Use `?.`, `?:`, or `if` instead.

---

### Way 5 (bonus): `?.let { }` — do something only if not null

```kotlin
fun main() {
    val email: String? = "roy@mail.com"

    email?.let {
        println("Sending a message to $it")
    }
}
```

- `?.let { ... }` → "If `email` is not `null`, run the steps inside `{ }`."
- Inside the `{ }`, the word **`it`** means "the value" (here, the email).
- If `email` was `null`, nothing happens.

We will learn more about `let` and `it` in this chapter (lambdas) and in Chapter 4.

---

### Null safety summary table

| Code | Meaning | If `null`… |
|---|---|---|
| `String?` | This box may be empty | — |
| `if (x != null) { }` | Check first | the `else` part runs |
| `x?.length` | Safe call | gives `null` |
| `x ?: "backup"` | Elvis — backup value | gives `"backup"` |
| `x!!.length` | "I promise it's not null" | 💥 crash |
| `x?.let { }` | Run only if not null | nothing happens |

---

## 3.2 Lists — Many Values in One Box 📋

So far, one box held **one** value. But what about **all** your friends' names? Or **all** items in a shopping cart?

You use a **List**. A list is like a **train** 🚂 with many wagons. Each wagon holds one value, and the wagons are **in order**.

### Making a list

```kotlin
fun main() {
    val fruits = listOf("Apple", "Banana", "Mango")
    println(fruits)   // [Apple, Banana, Mango]
}
```

| Piece | Meaning |
|---|---|
| `listOf(...)` | "Make a list of these things." |
| `"Apple", "Banana", "Mango"` | The items, separated by commas. |
| `[Apple, Banana, Mango]` | How Kotlin prints a list — square brackets. |

Kotlin guesses the type: **`List<String>`** — read it as "**a List of Strings**".
The `< >` angle brackets say **what kind of things** are in the list.

```kotlin
val numbers: List<Int> = listOf(4, 8, 15, 16, 23, 42)
val answers: List<Boolean> = listOf(true, false, true)
```

### Getting items by their number (index)

Just like letters in a String, **counting starts at 0**:

```
 Item:    "Apple"   "Banana"   "Mango"
 Index:      0          1          2
```

```kotlin
fun main() {
    val fruits = listOf("Apple", "Banana", "Mango")

    println(fruits[0])        // Apple
    println(fruits[2])        // Mango
    println(fruits.first())   // Apple
    println(fruits.last())    // Mango
    println(fruits.size)      // 3  ← how many items
}
```

> ⚠️ `fruits[3]` → 💥 **crash** (`IndexOutOfBoundsException`). There is no item number 3.
> Safe way: `fruits.getOrNull(3)` → gives `null` instead of crashing.

### Asking questions about a list

```kotlin
fun main() {
    val fruits = listOf("Apple", "Banana", "Mango")

    println(fruits.contains("Mango"))   // true
    println("Grape" in fruits)          // false  ← same thing, shorter
    println(fruits.indexOf("Banana"))   // 1
    println(fruits.isEmpty())           // false
    println(fruits.isNotEmpty())        // true
}
```

### Going through every item with `for`

```kotlin
fun main() {
    val fruits = listOf("Apple", "Banana", "Mango")

    for (fruit in fruits) {
        println("I like $fruit")
    }
}
```

Output:

```
I like Apple
I like Banana
I like Mango
```

- In each round, `fruit` holds **one** item.
- Round 1: `"Apple"`. Round 2: `"Banana"`. Round 3: `"Mango"`.

**With the number too (`withIndex`):**

```kotlin
fun main() {
    val fruits = listOf("Apple", "Banana", "Mango")

    for ((index, fruit) in fruits.withIndex()) {
        println("$index: $fruit")
    }
}
```

Output:

```
0: Apple
1: Banana
2: Mango
```

`(index, fruit)` takes **two** values each round: the number and the item.

---

### Changing a list: `MutableList`

A list from `listOf` is **read-only**. You **cannot** add or remove items. 🔒

To change a list, use **`mutableListOf`**. ("Mutable" means "**can change**".)

```kotlin
fun main() {
    val cart = mutableListOf("Bread", "Milk")
    println(cart)              // [Bread, Milk]

    cart.add("Eggs")           // add at the end
    println(cart)              // [Bread, Milk, Eggs]

    cart.add(0, "Butter")      // add at position 0 (the start)
    println(cart)              // [Butter, Bread, Milk, Eggs]

    cart.remove("Milk")        // remove by value
    println(cart)              // [Butter, Bread, Eggs]

    cart.removeAt(0)           // remove by position
    println(cart)              // [Bread, Eggs]

    cart[1] = "Cheese"         // replace the item at position 1
    println(cart)              // [Bread, Cheese]

    cart.clear()               // remove everything
    println(cart)              // []
}
```

| Command | What it does |
|---|---|
| `add(x)` | Add `x` at the end |
| `add(i, x)` | Add `x` at position `i` |
| `remove(x)` | Remove the first `x` |
| `removeAt(i)` | Remove the item at position `i` |
| `list[i] = x` | Replace the item at position `i` |
| `clear()` | Remove all items |

### 🤔 Wait — `val cart`, but we changed it?

Good question! Look carefully:

- `val` means the **label is glued to this list**. You can't make `cart` point to a **different** list.
- `mutableListOf` means the **list itself** can get new items.

**Real-life example:** Your school bag 🎒 is **yours forever** (`val`). But you can still **put books in and take books out** (mutable).

```kotlin
val cart = mutableListOf("Bread")
cart.add("Milk")                 // ✅ OK: changing what is IN the bag
cart = mutableListOf("Rice")     // ❌ ERROR: Val cannot be reassigned (new bag)
```

### Making an empty list

When the list is empty, Kotlin can't guess the type. You must tell it:

```kotlin
val names = mutableListOf<String>()   // an empty list for Strings
names.add("Roy")
```

### `List` vs `MutableList` — which to use?

> 💡 **Same rule as `val`:** Use `listOf` (read-only) first. Use `mutableListOf` only if you need to change it.

---

## 3.3 Sets — No Repeats Allowed 🎟️

A **Set** is like a list, but:

1. **No duplicates.** Each value is there only **once**.
2. **No index.** You can't ask for `set[0]`.

```kotlin
fun main() {
    val colors = setOf("Red", "Blue", "Red", "Green", "Blue")
    println(colors)        // [Red, Blue, Green]
    println(colors.size)   // 3
}
```

The extra `"Red"` and `"Blue"` were **thrown away** automatically.

**Real-life example:** A **guest list** for a party 🎉. Each person is on it once — writing someone's name twice doesn't bring two of them!

```kotlin
fun main() {
    val visitors = mutableSetOf<String>()
    visitors.add("Roy")
    visitors.add("Asha")
    visitors.add("Roy")    // already there — ignored

    println(visitors)      // [Roy, Asha]
    println("Asha" in visitors)   // true
}
```

**Turn a list into a set to remove repeats:**

```kotlin
val numbers = listOf(1, 2, 2, 3, 3, 3)
println(numbers.toSet())   // [1, 2, 3]
```

---

## 3.4 Maps — Pairs Like a Dictionary 📖

A **Map** holds **pairs**: a **key** and a **value**.

**Real-life example:** A **dictionary**. You look up a **word** (key) and find its **meaning** (value).
Or a **phone book** ☎️: name (key) → phone number (value).

### Making a map

```kotlin
fun main() {
    val ages = mapOf(
        "Roy" to 10,
        "Asha" to 12,
        "Ben" to 9
    )

    println(ages)   // {Roy=10, Asha=12, Ben=9}
}
```

| Piece | Meaning |
|---|---|
| `mapOf(...)` | "Make a map." |
| `"Roy" to 10` | A **pair**: key `"Roy"`, value `10`. The word `to` joins them. |
| `{Roy=10, ...}` | How Kotlin prints a map — curly brackets, `key=value`. |

The type is **`Map<String, Int>`** — "a Map **from** String **to** Int".

### Looking up a value

```kotlin
fun main() {
    val ages = mapOf("Roy" to 10, "Asha" to 12)

    println(ages["Roy"])      // 10
    println(ages["Zara"])     // null  ← Zara is not in the map
}
```

> 💡 `ages["Roy"]` gives back an **`Int?`** (it might be `null`!), because the key might not exist.
> Use Elvis for a backup: `ages["Zara"] ?: 0` → `0`.

### Keys must be unique

```kotlin
val scores = mapOf("Roy" to 10, "Roy" to 50)
println(scores)   // {Roy=50}   ← the last one wins
```

Each **key** can appear only **once**. (Values can repeat.)

### Going through a map

```kotlin
fun main() {
    val capitals = mapOf(
        "India" to "New Delhi",
        "Japan" to "Tokyo",
        "France" to "Paris"
    )

    for ((country, city) in capitals) {
        println("The capital of $country is $city.")
    }
}
```

Output:

```
The capital of India is New Delhi.
The capital of Japan is Tokyo.
The capital of France is Paris.
```

Other useful things:

```kotlin
println(capitals.keys)              // [India, Japan, France]
println(capitals.values)            // [New Delhi, Tokyo, Paris]
println(capitals.size)              // 3
println(capitals.containsKey("Japan"))  // true
```

### Changing a map: `mutableMapOf`

```kotlin
fun main() {
    val stock = mutableMapOf("Apple" to 5, "Banana" to 3)

    stock["Mango"] = 8        // add a new pair
    stock["Apple"] = 10       // change an existing value
    stock.remove("Banana")    // remove a pair

    println(stock)            // {Apple=10, Mango=8}
}
```

### List vs Set vs Map — which one?

| You want to… | Use | Example |
|---|---|---|
| Keep things **in order**, repeats OK | **List** | Messages in a chat |
| Keep **unique** things | **Set** | Tags on a photo |
| **Look up** a value by a key | **Map** | Word → meaning, Name → score |

---

## 3.5 Classes and Objects — Making Your Own Types 🏭

So far we used types Kotlin gives us: `Int`, `String`, `List`…
But an app needs **its own** types: a `Student`, a `Product`, a `Message`, a `Song`…

### Class = blueprint. Object = the real thing.

| Word | Meaning | Real-life example |
|---|---|---|
| **Class** | A **plan** / **blueprint** that describes a kind of thing. | The **plan** of a house, drawn on paper. 📝 |
| **Object** | A **real thing** made from the class. | A **real house** built from that plan. 🏠 |

From **one** plan, you can build **many** houses. Each house can have a different color, but they all follow the same plan.

### Your first class

```kotlin
class Dog(val name: String, var age: Int)

fun main() {
    val dog1 = Dog("Rex", 3)
    val dog2 = Dog("Bella", 5)

    println(dog1.name)   // Rex
    println(dog2.name)   // Bella
    println(dog2.age)    // 5
}
```

### Every bit explained

```kotlin
class Dog(val name: String, var age: Int)
```

| Piece | Meaning |
|---|---|
| `class` | "I am making a new **type** (a blueprint)." |
| `Dog` | Its name. **Class names start with a BIG letter.** |
| `( ... )` | The **constructor** — what you must give when you **build** a Dog. |
| `val name: String` | Every Dog has a `name`. It can't change (`val`). |
| `var age: Int` | Every Dog has an `age`. It can change (`var`). |

These `name` and `age` are called **properties** (the things an object **has**).

```kotlin
    val dog1 = Dog("Rex", 3)
```

- `Dog("Rex", 3)` → "**Build** a new Dog object with name `Rex` and age `3`."
- We put the new Dog into the box `dog1`.
- (In some other languages you write `new Dog(...)`. In Kotlin, there is **no `new`**.)

```kotlin
    println(dog1.name)
```

- The **dot `.`** means "**the thing that belongs to**".
- `dog1.name` → "the name **of** dog1".

### Changing a property

```kotlin
fun main() {
    val dog = Dog("Rex", 3)
    dog.age = 4          // ✅ age is var
    // dog.name = "Max"  // ❌ ERROR: name is val
    println("${dog.name} is now ${dog.age}")   // Rex is now 4
}
```

> 💡 Notice we used `${dog.name}` with curly brackets. When there is a **dot**, you need `${ }`. Without it, `"$dog.name"` would print the dog object and then the letters `.name`.

### Adding actions (functions inside a class)

A class can also **do things**. Functions inside a class are called **methods**.

```kotlin
class Dog(val name: String, var age: Int) {

    fun bark() {
        println("$name says: Woof! 🐶")
    }

    fun haveBirthday() {
        age++
        println("Happy birthday, $name! You are now $age. 🎂")
    }
}

fun main() {
    val dog = Dog("Rex", 3)
    dog.bark()
    dog.haveBirthday()
}
```

Output:

```
Rex says: Woof! 🐶
Happy birthday, Rex! You are now 4. 🎂
```

- Inside the class, you can use `name` and `age` directly. They belong to **this** dog.
- `dog.bark()` → "Hey `dog`, **bark**!"

**So a class has two parts:**

| Part | Meaning | Dog example |
|---|---|---|
| **Properties** | What it **has** (nouns) | `name`, `age` |
| **Methods** | What it **does** (verbs) | `bark()`, `haveBirthday()` |

### Default values in the constructor

```kotlin
class Player(val name: String, var level: Int = 1, var lives: Int = 3)

fun main() {
    val p1 = Player("Roy")
    val p2 = Player("Asha", level = 5)

    println("${p1.name}: level ${p1.level}, lives ${p1.lives}")   // Roy: level 1, lives 3
    println("${p2.name}: level ${p2.level}, lives ${p2.lives}")   // Asha: level 5, lives 3
}
```

Same as functions: **default values** and **named arguments** work here too.

### Properties inside the class body

Not every property needs to be in the constructor:

```kotlin
class Phone(val brand: String) {
    var battery = 100            // every new phone starts at 100

    fun use(minutes: Int) {
        battery -= minutes / 2
        if (battery < 0) battery = 0
        println("$brand battery: $battery%")
    }
}

fun main() {
    val phone = Phone("Pixel")
    phone.use(30)   // Pixel battery: 85%
    phone.use(100)  // Pixel battery: 35%
}
```

### `init` — steps that run when the object is born

```kotlin
class Robot(val name: String) {
    init {
        println("🤖 Robot $name is switched ON!")
    }
}

fun main() {
    val r = Robot("Zippy")   // 🤖 Robot Zippy is switched ON!
}
```

The `init { }` block runs **automatically**, once, when the object is built.
(Like `onCreate` from Chapter 1 runs when a screen is born!)

### `private` — keep it secret 🔐

```kotlin
class BankAccount(val owner: String) {
    private var balance = 0

    fun deposit(amount: Int) {
        if (amount > 0) balance += amount
    }

    fun showBalance() {
        println("$owner has $balance coins.")
    }
}

fun main() {
    val account = BankAccount("Roy")
    account.deposit(50)
    account.showBalance()        // Roy has 50 coins.

    // account.balance = 1000000   ❌ ERROR: Cannot access 'balance': it is private
}
```

- `private` means "**only code inside this class** can see or change this."
- Nobody outside can cheat and set `balance` to a million! 💰
- They **must** use `deposit`, which checks that the amount is positive.

> 💡 This idea — hiding the inside and giving safe buttons to the outside — is called **encapsulation**. Think of a TV 📺: you use the remote's buttons; you don't open the TV and touch the wires.

---

## 3.6 Data Classes — Classes for Holding Data ⭐

In Android apps, most classes just **hold information**: a user, a product, a message, a weather report.
Kotlin has a special, super-useful kind for this: the **data class**.

### Normal class vs data class

```kotlin
class NormalStudent(val name: String, val age: Int)
data class Student(val name: String, val age: Int)

fun main() {
    val a = NormalStudent("Roy", 10)
    val b = Student("Roy", 10)

    println(a)   // NormalStudent@1b6d3586   ← not helpful 😕
    println(b)   // Student(name=Roy, age=10) ← nice! 😊
}
```

Just add the word **`data`** in front of `class`. Kotlin then gives you **free extra powers**:

### Power 1: Nice printing (`toString`)

As you saw: `Student(name=Roy, age=10)`. Very helpful in Logcat!

### Power 2: Comparing by content (`==`)

```kotlin
fun main() {
    val n1 = NormalStudent("Roy", 10)
    val n2 = NormalStudent("Roy", 10)
    println(n1 == n2)   // false  😕 (two different objects)

    val s1 = Student("Roy", 10)
    val s2 = Student("Roy", 10)
    println(s1 == s2)   // true   😊 (same data inside)
}
```

- Normal class: `==` asks "**Are these the very same object?**"
- Data class: `==` asks "**Do they have the same data inside?**"

**Real-life example:** Two copies of the same book 📚📚. They are two different objects, but the **content** is the same. A data class says they are equal.

### Power 3: `copy` — make a copy with small changes

```kotlin
fun main() {
    val roy = Student("Roy", 10)
    val olderRoy = roy.copy(age = 11)

    println(roy)       // Student(name=Roy, age=10)
    println(olderRoy)  // Student(name=Roy, age=11)
}
```

- `copy(age = 11)` → "Make a copy, but change `age` to 11."
- The original **does not change**.

> 💡 **This is VERY important in Jetpack Compose!** In Compose we usually keep data **unchanged** (`val`) and make a new copy when something changes. You will use `copy` a lot in Chapters 8 and 15.

### Power 4: Taking it apart (destructuring)

```kotlin
fun main() {
    val student = Student("Asha", 12)
    val (name, age) = student

    println(name)   // Asha
    println(age)    // 12
}
```

`val (name, age) = student` takes the data class **apart** into two boxes, **in order**.

### Rules for data classes

1. Must have **at least one** property in the `( )`.
2. Properties in `( )` must have `val` or `var`.
3. 💡 Best practice: use **`val`** for all properties. Use `copy()` to make changes.

### A list of data class objects 🌟 (very common!)

```kotlin
data class Product(val name: String, val price: Int, val inStock: Boolean)

fun main() {
    val products = listOf(
        Product("Pen", 10, true),
        Product("Notebook", 50, true),
        Product("Bag", 700, false)
    )

    for (p in products) {
        val status = if (p.inStock) "✅ in stock" else "❌ sold out"
        println("${p.name} — ${p.price} coins — $status")
    }
}
```

Output:

```
Pen — 10 coins — ✅ in stock
Notebook — 50 coins — ✅ in stock
Bag — 700 coins — ❌ sold out
```

This pattern — **a list of data class objects** — is in almost **every** Android app:
a list of messages, a list of songs, a list of products, a list of contacts…

---

## 3.7 Lambdas — Small Functions Without a Name 🐑

### What is a lambda?

In Chapter 2, every function had a **name**:

```kotlin
fun double(x: Int): Int {
    return x * 2
}
```

A **lambda** is a **small function with no name**, that you can **put in a box** or **give to another function**.

```kotlin
val double = { x: Int -> x * 2 }
```

**Real-life example:** A **sticky note with instructions** 📝: *"Multiply by 2."* You can keep the note, give it to a friend, and they can follow it whenever they want.

### Every bit explained

```kotlin
val double = { x: Int -> x * 2 }
```

| Piece | Meaning |
|---|---|
| `{ ... }` | Curly brackets = **this is a lambda**. |
| `x: Int` | The input. |
| `->` | Arrow: "**gives**" / "then do". Separates the input from the steps. |
| `x * 2` | The steps. The **last line** is automatically the answer (no `return` needed). |

**Using it:**

```kotlin
fun main() {
    val double = { x: Int -> x * 2 }
    println(double(5))    // 10
    println(double(21))   // 42
}
```

### More lambda examples

```kotlin
fun main() {
    // No input:
    val sayHi = { println("Hi! 👋") }
    sayHi()

    // Two inputs:
    val add = { a: Int, b: Int -> a + b }
    println(add(3, 4))   // 7

    // Many lines — the LAST line is the answer:
    val describe = { n: Int ->
        val kind = if (n % 2 == 0) "even" else "odd"
        "$n is $kind"
    }
    println(describe(7))  // 7 is odd
}
```

### The type of a lambda

A lambda's type looks like this: **`(inputs) -> output`**

| Lambda | Its type | Read it as |
|---|---|---|
| `{ println("Hi") }` | `() -> Unit` | "no input, gives nothing" |
| `{ x: Int -> x * 2 }` | `(Int) -> Int` | "takes an Int, gives an Int" |
| `{ a: Int, b: Int -> a + b }` | `(Int, Int) -> Int` | "takes two Ints, gives an Int" |
| `{ s: String -> s.length > 3 }` | `(String) -> Boolean` | "takes a String, gives true/false" |

```kotlin
val double: (Int) -> Int = { x -> x * 2 }
```

When you write the type on the left, you **don't need** to write `x: Int` again.

### `it` — the magic word for one input ✨

If a lambda has **exactly one** input, you can skip naming it. Kotlin calls it **`it`** automatically.

```kotlin
val double: (Int) -> Int = { it * 2 }
```

Same as `{ x -> x * 2 }`. Shorter! You will see `it` **everywhere** in Kotlin.

### Giving a lambda to a function ⭐

This is the **real power** of lambdas. A function can **take another function as input**.

```kotlin
fun doTwice(action: () -> Unit) {
    action()
    action()
}

fun main() {
    doTwice({ println("Clap! 👏") })
}
```

Output:

```
Clap! 👏
Clap! 👏
```

- `action: () -> Unit` → "My input is **a function** with no inputs that gives nothing."
- `action()` → "**Run** that function."

### Trailing lambda — the special short style ⭐⭐

If the **last** input of a function is a lambda, you can move it **outside** the `( )`:

```kotlin
doTwice({ println("Clap! 👏") })   // normal
doTwice() { println("Clap! 👏") }  // lambda moved outside
doTwice { println("Clap! 👏") }    // and the empty () can be removed!
```

All three do the same thing. The **last one** is the normal Kotlin style.

> 🎉 **Now you understand code from earlier chapters!**
>
> ```kotlin
> repeat(3) {                // Chapter 2: repeat takes a number AND a lambda!
>     println("Hooray!")
> }
>
> setContent {               // Chapter 1: setContent takes a lambda!
>     MyFirstAppTheme {      // MyFirstAppTheme takes a lambda too!
>         ...
>     }
> }
>
> Scaffold(...) { innerPadding ->   // a lambda with one input called innerPadding
>     ...
> }
> ```
>
> **Jetpack Compose is built on trailing lambdas.** Every `{ }` after a Compose function is a lambda that says *"put this inside me"*.

### Lambda with an input, passed to a function

```kotlin
fun forEachNumber(from: Int, to: Int, action: (Int) -> Unit) {
    for (i in from..to) {
        action(i)
    }
}

fun main() {
    forEachNumber(1, 3) { number ->
        println("Number $number")
    }

    forEachNumber(1, 3) {
        println("Square: ${it * it}")   // using "it"
    }
}
```

Output:

```
Number 1
Number 2
Number 3
Square: 1
Square: 4
Square: 9
```

---

## 3.8 Super-Powers for Lists 🦸

Kotlin lists have many built-in functions that take **lambdas**. They make your code **short** and **easy to read**.

We will use this list for the examples:

```kotlin
val numbers = listOf(5, 12, 3, 8, 20, 1)
```

### `forEach` — do something with each item

```kotlin
numbers.forEach { println(it) }
```

Same as a `for` loop. `it` is each number, one by one.

### `filter` — keep only some items 🔍

```kotlin
val big = numbers.filter { it > 6 }
println(big)   // [12, 8, 20]
```

- The lambda answers **true or false** for each item.
- `filter` **keeps** the items where the answer is `true`.

**Real-life example:** A **sieve** in the kitchen. Only the good things pass through.

### `map` — change every item 🔄

```kotlin
val doubled = numbers.map { it * 2 }
println(doubled)   // [10, 24, 6, 16, 40, 2]
```

- The lambda says **how to change** each item.
- `map` gives back a **new list** with the changed items. (The old list does not change.)

> ⚠️ Don't mix up this `map` (a list function that **changes items**) with a **Map** (the dictionary type from 3.4). Same word, different things!

### Counting and checking

```kotlin
println(numbers.count { it > 6 })     // 3     → how many are > 6
println(numbers.any { it > 15 })      // true  → is at least ONE > 15?
println(numbers.all { it > 0 })       // true  → are ALL > 0?
println(numbers.none { it > 100 })    // true  → is NONE > 100?
```

### Finding

```kotlin
println(numbers.find { it > 10 })     // 12    → the FIRST one > 10
println(numbers.find { it > 100 })    // null  → none found
```

`find` gives a **nullable** answer (`Int?`), because maybe nothing matches.

### Math on lists

```kotlin
println(numbers.sum())        // 49
println(numbers.average())    // 8.166666666666666
println(numbers.maxOrNull())  // 20
println(numbers.minOrNull())  // 1
```

`maxOrNull` gives `null` if the list is empty (safe!).

### Sorting

```kotlin
println(numbers.sorted())             // [1, 3, 5, 8, 12, 20]
println(numbers.sortedDescending())   // [20, 12, 8, 5, 3, 1]
```

### Joining into one String

```kotlin
println(numbers.joinToString(", "))           // 5, 12, 3, 8, 20, 1
println(numbers.joinToString(" + "))          // 5 + 12 + 3 + 8 + 20 + 1
println(numbers.joinToString(", ") { "#$it" })  // #5, #12, #3, #8, #20, #1
```

### Chaining — one after another ⛓️

You can join these functions together like a **factory line** 🏭:

```kotlin
val result = numbers
    .filter { it % 2 == 0 }   // keep even:  [12, 8, 20]
    .map { it * 10 }          // times 10:   [120, 80, 200]
    .sorted()                 // sort:       [80, 120, 200]

println(result)   // [80, 120, 200]
```

Read it from top to bottom like a recipe. Each step takes the result of the step before.

### With data classes — the real-world way 🌍

```kotlin
data class Product(val name: String, val price: Int, val inStock: Boolean)

fun main() {
    val products = listOf(
        Product("Pen", 10, true),
        Product("Notebook", 50, true),
        Product("Bag", 700, false),
        Product("Eraser", 5, true)
    )

    // Names of products in stock:
    val available = products.filter { it.inStock }.map { it.name }
    println(available)   // [Pen, Notebook, Eraser]

    // Total price of everything:
    println(products.sumOf { it.price })   // 765

    // Cheapest first:
    val cheapFirst = products.sortedBy { it.price }
    println(cheapFirst.map { it.name })    // [Eraser, Pen, Notebook, Bag]

    // Most expensive:
    val priciest = products.maxByOrNull { it.price }
    println(priciest?.name)                // Bag

    // Is anything sold out?
    println(products.any { !it.inStock })  // true
}
```

| Function | What it does |
|---|---|
| `sumOf { }` | Adds up a number from each item |
| `sortedBy { }` | Sorts by something (small to big) |
| `sortedByDescending { }` | Sorts by something (big to small) |
| `maxByOrNull { }` | Item with the biggest value |
| `minByOrNull { }` | Item with the smallest value |
| `groupBy { }` | Makes a Map of groups |

**`groupBy` example:**

```kotlin
val byStock = products.groupBy { it.inStock }
println(byStock[true]?.map { it.name })    // [Pen, Notebook, Eraser]
println(byStock[false]?.map { it.name })   // [Bag]
```

> 💡 You will use `filter`, `map`, `sortedBy`, `sumOf` and `find` **all the time** in Android apps. For example: *"Show only unread messages"* → `messages.filter { !it.isRead }`.

---

## 3.9 Use It in Your Android App! 📱

Let us show a **shopping list** in the app from Chapter 1, using data classes, a list, lambdas, and null safety.

### Step 1: Open the project

Open **MyFirstApp** in Android Studio. Open `MainActivity.kt`.

### Step 2: Add a data class

Add this at the **very bottom** of the file (outside of every other `{ }`):

```kotlin
data class ShopItem(
    val name: String,
    val emoji: String,
    val price: Int,
    val note: String? = null
)
```

| Line | Meaning |
|---|---|
| `data class ShopItem(` | A new data type for one item in the shop. |
| `val name: String` | The item's name. |
| `val emoji: String` | A small picture, like 🍎. |
| `val price: Int` | The price. |
| `val note: String? = null` | An **optional** note. It can be `null`. By default, it **is** `null`. |

### Step 3: Change the `Greeting` function

Replace your `Greeting` function with this:

```kotlin
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    val items = listOf(
        ShopItem("Apple", "🍎", 30),
        ShopItem("Bread", "🍞", 40, note = "whole wheat"),
        ShopItem("Milk", "🥛", 55),
        ShopItem("Cheese", "🧀", 120, note = "only if on sale")
    )

    val total = items.sumOf { it.price }
    val cheap = items.filter { it.price < 50 }.map { it.name }

    val listText = items.joinToString("\n") { item ->
        val noteText = item.note?.let { " ($it)" } ?: ""
        "${item.emoji} ${item.name} — ${item.price}$noteText"
    }

    Text(
        text = "Hello $name! Here is your shopping list:\n\n" +
            listText +
            "\n\nTotal: $total" +
            "\nCheap items: ${cheap.joinToString(", ")}",
        modifier = modifier
    )
}
```

### Every bit explained

**The list:**

```kotlin
    val items = listOf(
        ShopItem("Apple", "🍎", 30),
        ShopItem("Bread", "🍞", 40, note = "whole wheat"),
        ...
    )
```

- A `List<ShopItem>` with 4 objects.
- Apple and Milk have **no** note → `note` is `null` (the default).
- Bread and Cheese **have** a note. We use a **named argument** `note = ...`.

**The total:**

```kotlin
    val total = items.sumOf { it.price }
```

- For each item (`it`), take its `price`. Add them all. → `30 + 40 + 55 + 120 = 245`.

**The cheap items:**

```kotlin
    val cheap = items.filter { it.price < 50 }.map { it.name }
```

1. `filter { it.price < 50 }` → keep Apple (30) and Bread (40).
2. `map { it.name }` → change each item into just its name → `["Apple", "Bread"]`.

**Turning the list into text:**

```kotlin
    val listText = items.joinToString("\n") { item ->
        val noteText = item.note?.let { " ($it)" } ?: ""
        "${item.emoji} ${item.name} — ${item.price}$noteText"
    }
```

- `joinToString("\n")` → join all items, with a **new line** between them.
- `{ item -> ... }` → a lambda: **how** to turn each item into text. (We named the input `item` instead of `it`, because we use another `it` inside.)
- `item.note?.let { " ($it)" } ?: ""` → this is **null safety in action**:
  - If `note` is **not** null → make `" (whole wheat)"`. (Here `it` is the note.)
  - If `note` **is** null → `?.let` gives `null` → Elvis `?:` gives `""` (empty text).
- The last line of the lambda is the **answer**: for example `"🍞 Bread — 40 (whole wheat)"`.

### Step 4: Run it

Click **▶ Run** or look at the **Preview**. You will see:

```
Hello Roy! Here is your shopping list:

🍎 Apple — 30
🍞 Bread — 40 (whole wheat)
🥛 Milk — 55
🧀 Cheese — 120 (only if on sale)

Total: 245
Cheap items: Apple, Bread
```

🎉 You used **data classes**, **lists**, **lambdas**, **filter**, **map**, **sumOf**, **joinToString**, and **null safety** in a real app!

> ℹ️ Right now, everything is one big `Text`. In **Chapter 5 and 6** you will learn to show each item **nicely** in its own row, with real layouts. And in **Chapter 10** you will show long, scrollable lists. This chapter's skills are the **foundation** for that.

---

## 3.10 Common Mistakes and Fixes 🔧

| Mistake | Example | Error / Problem | Fix |
|---|---|---|---|
| Using a `?` value directly | `name.length` when `name: String?` | *Only safe (?.) or non-null asserted (!!.) calls are allowed...* | Use `name?.length`, `?:`, or `if (name != null)`. |
| Putting `null` in a normal type | `val s: String = null` | *Null can not be a value of a non-null type* | Use `String?`. |
| Using `!!` too much | `user!!.name` | 💥 crash if `user` is null | Use `user?.name ?: "Guest"`. |
| Adding to a read-only list | `listOf(1).add(2)` | *Unresolved reference: add* | Use `mutableListOf`. |
| Index too big | `list[list.size]` | 💥 *IndexOutOfBoundsException* | Last index is `size - 1`. Or use `getOrNull`. |
| Empty list with no type | `val x = mutableListOf()` | *Not enough information to infer type variable* | `mutableListOf<String>()` |
| Forgetting `${ }` with a dot | `"$dog.name"` | Prints `Dog@1a2b.name` | `"${dog.name}"` |
| Map value assumed not null | `val a: Int = ages["Roy"]` | *Type mismatch: inferred type is Int? but Int was expected* | `ages["Roy"] ?: 0` |
| Printing a normal class | `println(myObj)` | Shows `MyClass@1b6d3586` | Use a **data class**. |
| `it` with two inputs | `{ it + it }` for `(Int, Int) -> Int` | *Unresolved reference: it* | `it` works only with **one** input. Name them: `{ a, b -> a + b }`. |

---

## 3.11 Summary — What You Learned 🎓

✅ **Null safety:**
- `String?` = may be `null`. `String` = never `null`.
- `?.` safe call, `?:` Elvis backup, `if (x != null)` smart cast, `?.let { }`.
- Avoid `!!`.

✅ **Collections:**
- **List** — ordered, repeats OK: `listOf`, `mutableListOf`, `[index]`, `size`, `add`, `remove`.
- **Set** — no repeats: `setOf`, `mutableSetOf`.
- **Map** — key → value: `mapOf("a" to 1)`, `map["a"]`, `mutableMapOf`.

✅ **Classes:**
- Class = blueprint, object = real thing.
- Properties (what it **has**) and methods (what it **does**).
- `init { }`, default values, `private`.

✅ **Data classes:** `data class` gives nice printing, `==` by content, `copy()`, and destructuring.

✅ **Lambdas:**
- `{ x: Int -> x * 2 }`, type `(Int) -> Int`.
- `it` for one input.
- **Trailing lambda**: `doTwice { ... }` — this is how Compose works!

✅ **List super-powers:** `forEach`, `filter`, `map`, `find`, `count`, `any`, `all`, `sum`, `sumOf`, `sortedBy`, `maxByOrNull`, `groupBy`, `joinToString`.

✅ You built a **shopping list** in your Android app.

---

## 3.12 Practice Time 🏋️

Use the **Kotlin Playground**. Try first, then check the answers! 💪

**Task 1 — Null safety:**
Make `val city: String? = null`. Print `City: Unknown` using the Elvis operator. Then change `city` to `"Paris"` and check that it prints `City: Paris`.

**Task 2 — Safe length:**
Write a function `safeLength(text: String?): Int` that returns the length of the text, or `0` if it is `null`.

**Task 3 — Shopping cart:**
Make a mutable list of Strings. Add `"Rice"`, `"Oil"`, `"Salt"`. Remove `"Oil"`. Print the list and its size.

**Task 4 — Unique words:**
You have `listOf("cat", "dog", "cat", "bird", "dog", "cat")`. Print the unique words and how many there are.

**Task 5 — Phone book:**
Make a mutable map of names to phone numbers (as Strings) with 2 people. Add a third person. Then print each person in the form `Roy: 98765`.

**Task 6 — Class:**
Make a class `Counter` with a `private var count = 0`, and methods `increase()`, `reset()`, and `show()` (prints the count). Use it: increase 3 times, show, reset, show.

**Task 7 — Data class and copy:**
Make `data class Book(val title: String, val author: String, val pages: Int)`. Make one book. Make a copy with 50 more pages. Print both. Check with `==` if they are equal.

**Task 8 — Lambdas:**
Make a lambda `isLong` of type `(String) -> Boolean` that is `true` if a word has more than 5 letters. Test it with `"cat"` and `"elephant"`.

**Task 9 — List super-powers:**
You have:

```kotlin
data class Student(val name: String, val marks: Int)

val students = listOf(
    Student("Roy", 82),
    Student("Asha", 95),
    Student("Ben", 47),
    Student("Zara", 68)
)
```

Print:
1. Names of students who passed (marks ≥ 50).
2. The average marks.
3. The name of the top student.
4. All names sorted by marks, highest first.

---

### Answers

**Task 1:**

```kotlin
fun main() {
    val city: String? = null
    println("City: ${city ?: "Unknown"}")   // City: Unknown
}
```

Change `null` to `"Paris"` → `City: Paris`.

**Task 2:**

```kotlin
fun safeLength(text: String?): Int {
    return text?.length ?: 0
}

fun main() {
    println(safeLength("Hello"))  // 5
    println(safeLength(null))     // 0
}
```

Short version: `fun safeLength(text: String?) = text?.length ?: 0`

**Task 3:**

```kotlin
fun main() {
    val cart = mutableListOf<String>()
    cart.add("Rice")
    cart.add("Oil")
    cart.add("Salt")
    cart.remove("Oil")
    println(cart)        // [Rice, Salt]
    println(cart.size)   // 2
}
```

**Task 4:**

```kotlin
fun main() {
    val words = listOf("cat", "dog", "cat", "bird", "dog", "cat")
    val unique = words.toSet()
    println(unique)        // [cat, dog, bird]
    println(unique.size)   // 3
}
```

**Task 5:**

```kotlin
fun main() {
    val phoneBook = mutableMapOf(
        "Roy" to "98765",
        "Asha" to "91234"
    )
    phoneBook["Ben"] = "90000"

    for ((name, number) in phoneBook) {
        println("$name: $number")
    }
}
```

Output:

```
Roy: 98765
Asha: 91234
Ben: 90000
```

**Task 6:**

```kotlin
class Counter {
    private var count = 0

    fun increase() {
        count++
    }

    fun reset() {
        count = 0
    }

    fun show() {
        println("Count: $count")
    }
}

fun main() {
    val counter = Counter()
    counter.increase()
    counter.increase()
    counter.increase()
    counter.show()    // Count: 3
    counter.reset()
    counter.show()    // Count: 0
}
```

`class Counter` has no `( )` because it needs no inputs to be built. We still build it with `Counter()`.

**Task 7:**

```kotlin
data class Book(val title: String, val author: String, val pages: Int)

fun main() {
    val book = Book("Kotlin for Kids", "Roy", 200)
    val bigger = book.copy(pages = book.pages + 50)

    println(book)            // Book(title=Kotlin for Kids, author=Roy, pages=200)
    println(bigger)          // Book(title=Kotlin for Kids, author=Roy, pages=250)
    println(book == bigger)  // false (pages are different)
}
```

**Task 8:**

```kotlin
fun main() {
    val isLong: (String) -> Boolean = { it.length > 5 }
    println(isLong("cat"))       // false
    println(isLong("elephant"))  // true
}
```

**Task 9:**

```kotlin
data class Student(val name: String, val marks: Int)

fun main() {
    val students = listOf(
        Student("Roy", 82),
        Student("Asha", 95),
        Student("Ben", 47),
        Student("Zara", 68)
    )

    // 1. Passed
    val passed = students.filter { it.marks >= 50 }.map { it.name }
    println("Passed: $passed")          // Passed: [Roy, Asha, Zara]

    // 2. Average
    val average = students.map { it.marks }.average()
    println("Average: $average")        // Average: 73.0

    // 3. Top student
    val top = students.maxByOrNull { it.marks }
    println("Top: ${top?.name}")        // Top: Asha

    // 4. Sorted, highest first
    val ranking = students.sortedByDescending { it.marks }.map { it.name }
    println("Ranking: $ranking")        // Ranking: [Asha, Roy, Zara, Ben]
}
```

Check the average: `(82 + 95 + 47 + 68) / 4 = 292 / 4 = 73.0` ✅

---

## 3.13 What Is Next?

In **Chapter 4: Kotlin Power Tools**, you will learn:

- **Inheritance** — a class that is "a kind of" another class (like `MainActivity : ComponentActivity`!)
- **Interfaces** — promises a class must keep
- **Enums** — a fixed list of choices (like `RED`, `YELLOW`, `GREEN`)
- **Sealed classes** — perfect for screen states like *Loading*, *Success*, *Error*
- **`object`** and **companion object** — one-of-a-kind objects
- **Extension functions** — add new powers to existing types
- **Scope functions** — `let`, `apply`, `also`, `run`, `with`
- **Generics** — the meaning of `<T>` in `List<T>`

After Chapter 4, you will know all the Kotlin you need to build real Android apps! 🚀

**Great job finishing Chapter 3! 🎉 This was a big one. Be proud of yourself!**
