# Chapter 4: Kotlin Power Tools — Inheritance, Enums, Sealed Classes, and More

> **What you will learn in this chapter**
>
> 1. Inheritance — a class that is "a kind of" another class
> 2. Abstract classes — plans that are not finished
> 3. Interfaces — promises a class must keep
> 4. Checking types with `is` and `as?`
> 5. Enums — a fixed list of choices
> 6. Sealed classes — perfect for *Loading / Success / Error*
> 7. `object` and `companion object` — one-of-a-kind objects
> 8. Extension functions — new powers for old types
> 9. Scope functions — `let`, `apply`, `also`, `run`, `with`
> 10. Generics — what `<T>` means
> 11. Using all of this in your Android app
>
> **Time needed:** about 4 to 5 hours.
>
> **Where to practice:** Kotlin Playground — **https://play.kotlinlang.org**

> 💡 **Good news:** After this chapter, you know **all the Kotlin you need** to start building real Android screens. From Chapter 5, we build apps! 🚀

---

## 4.1 Inheritance — "Is a Kind Of" 👨‍👧

### The idea

In real life, things come in **families**:

- A **cat** is a kind of **animal**.
- A **car** is a kind of **vehicle**.
- A **button** is a kind of **screen part**.

All animals have something in common: a name, they eat, they make a sound.
But each kind of animal is also a bit **different**: a cat says "Meow", a dog says "Woof".

**Inheritance** lets one class (the **child**) get everything from another class (the **parent**), and then **add or change** things.

```
           Animal          ← parent (also called "superclass")
          /      \
       Cat        Dog      ← children (also called "subclasses")
```

### Step 1: The parent must be `open`

In Kotlin, classes are **closed** by default. Nobody can inherit from them.
To allow children, write **`open`** in front:

```kotlin
open class Animal(val name: String) {
    fun eat() {
        println("$name is eating. 🍽️")
    }
}
```

**Why closed by default?** Safety. The person who writes a class decides if others may extend it. 🔒

### Step 2: Make a child class

```kotlin
class Cat(name: String) : Animal(name)

fun main() {
    val cat = Cat("Kitty")
    cat.eat()           // Kitty is eating. 🍽️
    println(cat.name)   // Kitty
}
```

### Every bit explained

```kotlin
class Cat(name: String) : Animal(name)
```

| Piece | Meaning |
|---|---|
| `class Cat` | A new class called `Cat`. |
| `(name: String)` | To build a Cat, give a name. ⚠️ No `val` here — the parent already has the `name` property. |
| `:` | "**is a kind of**" (you saw this in Chapter 1!). |
| `Animal(name)` | "Build the Animal part, and pass the name to it." |

`Cat` did not write `eat()`, but it **has** it — it **inherited** it from `Animal`. 🎁

> 🎉 **Remember Chapter 1?** `class MainActivity : ComponentActivity()` — this is inheritance! Your screen **is a kind of** `ComponentActivity`, and it gets hundreds of features from it for free.

### Step 3: Changing behavior — `open` and `override`

```kotlin
open class Animal(val name: String) {
    open fun sound() {
        println("$name makes a sound.")
    }
}

class Cat(name: String) : Animal(name) {
    override fun sound() {
        println("$name says Meow! 🐱")
    }
}

class Dog(name: String) : Animal(name) {
    override fun sound() {
        println("$name says Woof! 🐶")
    }
}

class Fish(name: String) : Animal(name)   // does not override

fun main() {
    Cat("Kitty").sound()   // Kitty says Meow! 🐱
    Dog("Rex").sound()     // Rex says Woof! 🐶
    Fish("Nemo").sound()   // Nemo makes a sound.
}
```

| Word | Where | Meaning |
|---|---|---|
| `open fun` | in the **parent** | "Children are **allowed** to change this function." |
| `override fun` | in the **child** | "I am **replacing** my parent's version." |

`Fish` did not override, so it uses the parent's version.

> 🎉 **Remember `override fun onCreate(...)` from Chapter 1?** Now you know: `ComponentActivity` has an `open fun onCreate`, and **we override it** with our own steps!

### Step 4: Calling the parent's version with `super`

```kotlin
class Puppy(name: String) : Animal(name) {
    override fun sound() {
        super.sound()                        // first, do the parent's version
        println("$name also says Yip! 🐕")   // then add our own
    }
}

fun main() {
    Puppy("Bobo").sound()
}
```

Output:

```
Bobo makes a sound.
Bobo also says Yip! 🐕
```

- `super` = "my **parent**".
- `super.sound()` = "run my parent's `sound()`".

> 🎉 This is exactly `super.onCreate(savedInstanceState)` from Chapter 1!

### One list, many kinds (polymorphism)

A child **is a kind of** parent. So you can put **different children in one list**:

```kotlin
fun main() {
    val zoo: List<Animal> = listOf(Cat("Kitty"), Dog("Rex"), Fish("Nemo"))

    for (animal in zoo) {
        animal.sound()
    }
}
```

Output:

```
Kitty says Meow! 🐱
Rex says Woof! 🐶
Nemo makes a sound.
```

- The list type is `List<Animal>`.
- Each animal uses **its own** version of `sound()`.

This has a long name: **polymorphism** ("many shapes"). You don't need to remember the word. Just remember the idea: **same command, each one does it its own way.** 🎭

### `Any` — the grandparent of everything

Every class in Kotlin secretly inherits from a class called **`Any`**. That is why **every** object has `toString()`, `equals()` (used by `==`), and `hashCode()`.

---

## 4.2 Abstract Classes — Unfinished Plans 📐

Sometimes a parent class is **too general** to make real objects from.

What does a "**Shape**" look like? You can't draw a "shape" — you draw a **circle**, a **square**…
But every shape **has an area**.

```kotlin
abstract class Shape(val name: String) {
    abstract fun area(): Double      // no body! Children MUST write it.

    fun describe() {
        println("$name has an area of ${area()}")
    }
}

class Square(val side: Double) : Shape("Square") {
    override fun area(): Double = side * side
}

class Circle(val radius: Double) : Shape("Circle") {
    override fun area(): Double = 3.14 * radius * radius
}

fun main() {
    Square(4.0).describe()   // Square has an area of 16.0
    Circle(2.0).describe()   // Circle has an area of 12.56

    // val s = Shape("Blob")  ❌ ERROR: Cannot create an instance of an abstract class
}
```

| Word | Meaning |
|---|---|
| `abstract class` | An **unfinished plan**. You **cannot** build objects from it directly. Only children can be built. |
| `abstract fun area(): Double` | "Every child **must** write this function." There is no `{ }` body here. |

**Real-life example:** A **form** with blank spaces 📄. The form says "*Write your name here: _____*". Every person **must** fill in the blank.

> 💡 An abstract class is automatically `open`. You don't need to write `open`.

---

## 4.3 Interfaces — Promises 🤝

An **interface** is a **list of promises**: *"Any class that uses me **promises** to have these functions."*

```kotlin
interface Swimmer {
    fun swim()
}

interface Flyer {
    fun fly()
}

class Duck(val name: String) : Swimmer, Flyer {
    override fun swim() {
        println("$name is swimming. 🦆💦")
    }

    override fun fly() {
        println("$name is flying. 🦆☁️")
    }
}

class Penguin(val name: String) : Swimmer {
    override fun swim() {
        println("$name is swimming fast! 🐧")
    }
}

fun main() {
    val duck = Duck("Donald")
    duck.swim()
    duck.fly()

    val penguin = Penguin("Pingu")
    penguin.swim()
    // penguin.fly()  ❌ penguins can't fly — no promise was made!
}
```

### Every bit explained

| Piece | Meaning |
|---|---|
| `interface Swimmer` | A list of promises called `Swimmer`. |
| `fun swim()` | The promise: "I can swim." No body. |
| `class Duck(...) : Swimmer, Flyer` | Duck **keeps two promises**. Separate them with commas. |
| `override fun swim()` | Duck **keeps** the promise by writing the function. |

**Real-life example:** A **driving license** 🪪. It promises "*This person can drive.*" Anyone with a license can drive — a teacher, a doctor, a chef. They are very different people, but they all keep the same promise.

### Interface vs abstract class

| | Abstract class | Interface |
|---|---|---|
| How many can a class use? | Only **one** parent | **Many** interfaces |
| Can it hold values (state) like `var count = 0`? | ✅ Yes | ❌ No (only promises) |
| Has a constructor `( )`? | ✅ Yes | ❌ No |
| Main idea | "**is a kind of**" | "**can do**" |

> 💡 A class can have **one** parent class **and many** interfaces:
> `class Duck(name: String) : Bird(name), Swimmer, Flyer`

### Interfaces can have ready-made functions

```kotlin
interface Greeter {
    val name: String                   // promise: you must have a name

    fun greet() {                      // a ready-made function (has a body)
        println("Hi, I am $name! 👋")
    }
}

class Robot(override val name: String) : Greeter

fun main() {
    Robot("Zippy").greet()   // Hi, I am Zippy! 👋
}
```

- `val name: String` in the interface → a **property promise**. The class keeps it with `override val name`.
- `greet()` has a body → classes get it **for free** (they can still override it).

### Why are interfaces important in Android?

You will see them a lot. For example, in **Chapter 22 (Room database)** you write an interface, and **Room writes the code for you**! And in **Chapter 16** we use interfaces to keep the app's parts clean and testable.

---

## 4.4 Checking Types: `is`, Smart Cast, and `as?` 🔍

Sometimes you have an `Animal`, and you want to know: *"Is it a Cat?"*

### `is` — "Is it a kind of…?"

```kotlin
fun describe(animal: Animal) {
    if (animal is Cat) {
        println("${animal.name} is a cat.")
    } else if (animal is Dog) {
        println("${animal.name} is a dog.")
    } else {
        println("${animal.name} is some other animal.")
    }
}
```

- `animal is Cat` → `true` if it is a `Cat`, otherwise `false`.
- `!is` means "is **not**": `animal !is Cat`.

### Smart cast (again!) 🧠

After checking with `is`, Kotlin **treats** the value as that type:

```kotlin
open class Animal(val name: String)
class Bird(name: String, val wingSpan: Int) : Animal(name)

fun show(animal: Animal) {
    if (animal is Bird) {
        println("Wings: ${animal.wingSpan} cm")   // ✅ Kotlin knows it's a Bird here
    }
}
```

`wingSpan` exists only in `Bird`. Because we checked with `is`, Kotlin lets us use it.

### `is` inside `when` ⭐ (very common)

```kotlin
fun describe(x: Any) {
    when (x) {
        is Int -> println("A number: ${x + 1}")
        is String -> println("Text with ${x.length} letters")
        is Boolean -> println("A yes/no value: $x")
        else -> println("Something else")
    }
}

fun main() {
    describe(41)        // A number: 42
    describe("Hello")   // Text with 5 letters
    describe(true)      // A yes/no value: true
    describe(3.5)       // Something else
}
```

### `as?` — "Try to treat it as…"

```kotlin
val thing: Any = "Hello"
val text: String? = thing as? String   // "Hello"
val number: Int? = thing as? Int       // null (it's not an Int)
```

- `as?` = "**try** to use this as that type. If it isn't, give `null`." Safe! ✅
- `as` (without `?`) = "**force** it." If wrong → 💥 crash. Avoid it.

---

## 4.5 Enums — A Fixed List of Choices 🚦

Some things have only a **few possible values**, and the list **never changes**:

- Traffic light: **RED**, **YELLOW**, **GREEN**
- Days of the week: **MONDAY** … **SUNDAY**
- T-shirt size: **SMALL**, **MEDIUM**, **LARGE**

You **could** use Strings like `"red"`. But what if someone types `"redd"` or `"Red"`? 🐛
An **enum** (short for **enumeration** = "a counted list") stops these mistakes.

### Your first enum

```kotlin
enum class TrafficLight {
    RED, YELLOW, GREEN
}

fun main() {
    val light = TrafficLight.RED
    println(light)   // RED
}
```

| Piece | Meaning |
|---|---|
| `enum class TrafficLight` | A type with a **fixed list** of values. |
| `RED, YELLOW, GREEN` | The **only** possible values. By custom, written in **BIG letters**. |
| `TrafficLight.RED` | Use one value: "the RED of TrafficLight". |

Now `TrafficLight.REDD` is an **error** right away. Typos are caught! ✅

### `when` with enums ⭐

```kotlin
fun action(light: TrafficLight): String {
    return when (light) {
        TrafficLight.RED -> "Stop 🛑"
        TrafficLight.YELLOW -> "Get ready ⚠️"
        TrafficLight.GREEN -> "Go 🟢"
    }
}
```

👀 Notice: **no `else`!**
Kotlin knows the list has **only 3** values, and we covered all 3. This is called an **exhaustive** `when` ("covers everything").

And if someone later adds `BLUE` to the enum, Kotlin will show an **error** here: *"you forgot BLUE!"*. That's very helpful. 🙌

### Enums with properties

Each enum value can carry **data**:

```kotlin
enum class Planet(val emoji: String, val order: Int) {
    MERCURY("☿️", 1),
    VENUS("♀️", 2),
    EARTH("🌍", 3),
    MARS("🔴", 4);              // ← a semicolon is needed when you add more below

    fun describe() = "$emoji $name is planet number $order"
}

fun main() {
    println(Planet.EARTH.emoji)       // 🌍
    println(Planet.EARTH.describe())  // 🌍 EARTH is planet number 3
}
```

### Free things every enum has

```kotlin
fun main() {
    val p = Planet.MARS
    println(p.name)      // MARS          → the name as a String
    println(p.ordinal)   // 3             → position in the list (starts at 0!)

    for (planet in Planet.entries) {      // all values, in order
        println(planet.describe())
    }
}
```

| Thing | Meaning |
|---|---|
| `.name` | The value's name as text |
| `.ordinal` | Its position (0, 1, 2…) |
| `Planet.entries` | A list of **all** values |
| `Planet.valueOf("MARS")` | Turn text into the enum value (crashes if wrong!) |

---

## 4.6 Sealed Classes — A Fixed List of *Kinds* ⭐⭐

### The problem

An app loads the weather from the internet. The screen can be in **three situations**:

1. ⏳ **Loading** — still waiting
2. ✅ **Success** — we have the temperature (needs **data**: a number!)
3. ❌ **Error** — something went wrong (needs **data**: an error message!)

An enum is **not enough**, because each choice needs **different data**.
A normal class hierarchy is **not safe enough**, because anyone could add a 4th kind anywhere.

### The solution: `sealed`

```kotlin
sealed interface WeatherState {
    data object Loading : WeatherState
    data class Success(val temperature: Int) : WeatherState
    data class Error(val message: String) : WeatherState
}
```

### Every bit explained

| Piece | Meaning |
|---|---|
| `sealed interface WeatherState` | A **closed family**. All its kinds must be written **right here** (in the same file/package). Nobody else can add more. 🔒 |
| `data object Loading` | Loading needs **no data**, so it's an **`object`** (only one exists — see 4.7). `data` gives it nice printing. |
| `data class Success(val temperature: Int)` | Success **carries a temperature**. |
| `data class Error(val message: String)` | Error **carries a message**. |
| `: WeatherState` | Each one **is a kind of** `WeatherState`. |

**Real-life example:** A **parcel tracking** 📦 page. The parcel is **either**:
- "Being packed" (no extra info),
- "On the way" (with the city it is in now),
- "Delivered" (with the time and who signed).

Always exactly **one** of these. Each has **its own** information.

### Using a sealed type with `when`

```kotlin
fun showWeather(state: WeatherState): String {
    return when (state) {
        WeatherState.Loading -> "Loading... ⏳"
        is WeatherState.Success -> "It is ${state.temperature}°C ☀️"
        is WeatherState.Error -> "Oops: ${state.message} ❌"
    }
}

fun main() {
    println(showWeather(WeatherState.Loading))
    println(showWeather(WeatherState.Success(28)))
    println(showWeather(WeatherState.Error("No internet")))
}
```

Output:

```
Loading... ⏳
It is 28°C ☀️
Oops: No internet ❌
```

Look carefully:

| Line | Why written like this |
|---|---|
| `WeatherState.Loading ->` | `Loading` is **one single object**, so we compare to it directly. |
| `is WeatherState.Success ->` | `Success` is a **class** (many possible objects), so we use `is`. Then **smart cast** lets us use `state.temperature`! |
| No `else` | The family is **sealed**, Kotlin knows all 3 kinds. Exhaustive! ✅ |

> 💡 **This pattern is used in almost every modern Android app.** In Chapters 15–19 you will write `sealed interface UiState { Loading, Success, Error }` again and again, and show a different screen for each one.

### `sealed class` or `sealed interface`?

Both work. `sealed interface` is a bit more flexible, and is common in modern code. You will also see `sealed class` in many tutorials — it is the same idea.

### Enum vs sealed — which one?

| Use an **enum** when… | Use a **sealed** type when… |
|---|---|
| Every choice is **simple** with the **same** shape of data. | Each choice needs **different** data. |
| Example: `SMALL`, `MEDIUM`, `LARGE` | Example: `Loading`, `Success(data)`, `Error(message)` |

---

## 4.7 `object` and `companion object` — One of a Kind ☝️

### `object` — exactly one, forever

Sometimes you need **only one** of something in the whole app. For example: the app's **settings**.

```kotlin
object AppSettings {
    var darkMode = false
    val appVersion = "1.0"

    fun toggleDarkMode() {
        darkMode = !darkMode
        println("Dark mode is now $darkMode")
    }
}

fun main() {
    println(AppSettings.appVersion)   // 1.0
    AppSettings.toggleDarkMode()      // Dark mode is now true
    AppSettings.toggleDarkMode()      // Dark mode is now false
}
```

| Piece | Meaning |
|---|---|
| `object AppSettings` | Make a class **and** its one single object, at the same time. |
| `AppSettings.appVersion` | Use it **by its name**. No `( )` — you don't build it; it already exists. |

**Real-life example:** The **sun** ☀️. There is only one. Everyone talks about "**the** sun". Nobody builds a new sun.

The big word for this is **singleton** ("only one").

### `companion object` — things that belong to the class itself

Sometimes a value belongs to the **whole class**, not to each object.

```kotlin
class Player(val name: String) {
    var lives = MAX_LIVES

    companion object {
        const val MAX_LIVES = 3

        fun guest(): Player {
            return Player("Guest")
        }
    }
}

fun main() {
    println(Player.MAX_LIVES)    // 3        ← used with the CLASS name
    val p = Player.guest()
    println(p.name)              // Guest
    println(p.lives)             // 3
}
```

| Piece | Meaning |
|---|---|
| `companion object { ... }` | A "**helper**" that lives inside the class. One for the whole class. |
| `const val MAX_LIVES = 3` | A **constant**: a value fixed forever, known before the app even runs. By custom, written in `BIG_LETTERS_WITH_UNDERSCORES`. |
| `Player.MAX_LIVES` | Used with the **class name**, not an object. |
| `fun guest()` | A helper that **builds** a Player for you. This kind of function is called a **factory**. 🏭 |

**Real-life example:** A **school**. Each student has their own name (object property). But the **school's address** belongs to the whole school (companion).

> 💡 In Android you'll often see `companion object { const val TAG = "MainActivity" }` used for Logcat tags.

---

## 4.8 Extension Functions — New Powers for Old Types 🦸‍♂️

What if you want `String` to have a new function, like `shout()`?
You can't change Kotlin's `String` class… but you **can** add an **extension**!

```kotlin
fun String.shout(): String {
    return this.uppercase() + "!!!"
}

fun main() {
    println("hello".shout())     // HELLO!!!
    println("kotlin".shout())    // KOTLIN!!!
}
```

### Every bit explained

| Piece | Meaning |
|---|---|
| `fun String.shout()` | "Add a function called `shout` **to every String**." |
| `this` | "The String this was called on." For `"hello".shout()`, `this` is `"hello"`. |

You can skip `this.` — it is understood:

```kotlin
fun String.shout() = uppercase() + "!!!"
```

**Real-life example:** Putting a **phone case with a stand** on your phone 📱. You didn't change the phone itself, but now it has a new power: it can stand up!

### More examples

```kotlin
fun Int.isEven() = this % 2 == 0

fun Int.minutesToText(): String {
    val hours = this / 60
    val minutes = this % 60
    return "${hours}h ${minutes}m"
}

fun List<Int>.secondOrNull(): Int? = this.getOrNull(1)

fun main() {
    println(7.isEven())              // false
    println(135.minutesToText())     // 2h 15m
    println(listOf(5, 9, 2).secondOrNull())   // 9
}
```

### Extension properties

```kotlin
val String.wordCount: Int
    get() = this.split(" ").size

fun main() {
    println("I love learning Kotlin".wordCount)   // 4
}
```

- `get() = ...` → "**calculate** the value each time someone asks."

> 🎉 **You've been using extensions already!** `Modifier.padding(...)`, `Modifier.fillMaxSize()` in Chapter 1 — these are **extension functions** on `Modifier`. Jetpack Compose uses extensions **everywhere**.

---

## 4.9 Scope Functions — `let`, `apply`, `also`, `run`, `with` 🧰

These five small functions are used **everywhere** in Kotlin code. They all do one thing:
> *"Run a small block of code **on an object**."*

They differ in only **two** ways:

1. Inside the `{ }`, do you call the object **`it`** or **`this`**?
2. What do they **give back**: the **object itself**, or the **last line** of the block?

### `let` — "with this value, do…" (uses `it`, gives back the last line)

```kotlin
fun main() {
    val name: String? = "roy"

    val greeting = name?.let {
        val big = it.replaceFirstChar { c -> c.uppercase() }
        "Hello, $big!"
    }

    println(greeting)   // Hello, Roy!
}
```

**Most common use:** together with `?.` — "**if not null**, do this" (you saw it in Chapter 3).

### `apply` — "set up this object" (uses `this`, gives back the object)

```kotlin
class Pizza {
    var size = "Medium"
    var cheese = false
    var toppings = mutableListOf<String>()
}

fun main() {
    val myPizza = Pizza().apply {
        size = "Large"
        cheese = true
        toppings.add("Mushroom")
        toppings.add("Olive")
    }

    println("${myPizza.size}, cheese=${myPizza.cheese}, ${myPizza.toppings}")
    // Large, cheese=true, [Mushroom, Olive]
}
```

- Inside `apply { }`, `this` is the pizza, so you can write `size` instead of `myPizza.size`.
- It gives back **the pizza itself**.

**Most common use:** **setting up** a new object.

**Real-life example:** You order a pizza 🍕 and say: "*Apply these settings: large, extra cheese, mushrooms.*" You get back **the pizza**.

### `also` — "and also do this" (uses `it`, gives back the object)

```kotlin
fun main() {
    val numbers = mutableListOf(1, 2, 3)
        .also { println("List made: $it") }
        .also { it.add(4) }

    println(numbers)   // [1, 2, 3, 4]
}
```

Output:

```
List made: [1, 2, 3]
[1, 2, 3, 4]
```

**Most common use:** doing an **extra side job** like printing a log, without changing the flow.

### `run` — "run these steps on this object" (uses `this`, gives back the last line)

```kotlin
fun main() {
    val message = "Kotlin".run {
        val count = length          // this.length
        "The word has $count letters"
    }
    println(message)   // The word has 6 letters
}
```

**Most common use:** **calculate something** from an object.

### `with` — like `run`, but written differently

```kotlin
fun main() {
    val pizza = Pizza()
    val info = with(pizza) {
        "Size: $size, Cheese: $cheese"
    }
    println(info)   // Size: Medium, Cheese: false
}
```

- `with(object) { ... }` instead of `object.run { ... }`.
- Read it as: "**With** this pizza, do…"

### The big comparison table 📊

| Function | Inside the block, the object is called | Gives back | Most common use |
|---|---|---|---|
| `let` | `it` | the **last line** | `x?.let { }` — do something if not null |
| `run` | `this` | the **last line** | calculate a result from an object |
| `with` | `this` | the **last line** | do many things with one object |
| `apply` | `this` | the **object** | set up / configure an object |
| `also` | `it` | the **object** | extra side job (logging, checking) |

**A simple memory trick:**

- `apply` and `also` → give back **the object** ("**A**lways the object" 🅰️)
- `let`, `run`, `with` → give back **the result** of the block

> 💡 **Don't worry** if this feels like a lot. In real code you'll mostly see `?.let { }` and `.apply { }`. The others will become clear with practice.

### Bonus: `buildString` and `buildList`

Kotlin has helpers that work like `apply`:

```kotlin
fun main() {
    val text = buildString {
        append("Hello")
        append(", ")
        appendLine("world!")
        append("Bye!")
    }
    println(text)

    val list = buildList {
        add(1)
        add(2)
        if (true) add(3)
    }
    println(list)   // [1, 2, 3]
}
```

Output:

```
Hello, world!
Bye!
[1, 2, 3]
```

- `append(x)` → add text.
- `appendLine(x)` → add text **and** a new line.

---

## 4.10 Generics — What Does `<T>` Mean? 🎁

### You have already used generics!

```kotlin
val names: List<String> = listOf("Roy", "Asha")
val ages: Map<String, Int> = mapOf("Roy" to 10)
val items = mutableListOf<Int>()
```

The `< >` part tells **what type is inside**. `List` is **one** class, but it can hold **any** type. That is **generics**.

**Real-life example:** A **lunch box** 🍱. The box is the same. Today it holds **rice**, tomorrow **sandwiches**. You write on the lid what is inside: `LunchBox<Rice>`, `LunchBox<Sandwich>`.

### Making your own generic class

```kotlin
class Box<T>(val item: T) {
    fun open(): T {
        println("Opening the box... 🎁")
        return item
    }
}

fun main() {
    val toyBox = Box("Teddy bear")     // Box<String>
    val numberBox = Box(42)            // Box<Int>

    val toy: String = toyBox.open()
    val number: Int = numberBox.open()

    println(toy)      // Teddy bear
    println(number)   // 42
}
```

| Piece | Meaning |
|---|---|
| `class Box<T>` | "`Box` has a **type placeholder** called `T`." `T` stands for "**T**ype". |
| `val item: T` | "The item is of type `T` — whatever type you choose." |
| `fun open(): T` | "Gives back something of type `T`." |
| `Box("Teddy bear")` | Kotlin sees a String, so here `T` = `String`. |

### Making your own generic function

```kotlin
fun <T> pickRandom(a: T, b: T): T {
    return if ((0..1).random() == 0) a else b
}

fun main() {
    println(pickRandom("Tea", "Coffee"))   // Tea or Coffee
    println(pickRandom(1, 100))            // 1 or 100
}
```

- `fun <T>` → "This function works with **any** type `T`."
- `(0..1).random()` → a random number, 0 or 1. 🎲

### Built-in generic helpers: `Pair` and `Triple`

```kotlin
fun main() {
    val point: Pair<Int, Int> = Pair(3, 5)
    println(point.first)    // 3
    println(point.second)   // 5

    val quick = "Roy" to 10        // "to" makes a Pair! (you used this in mapOf)
    val (name, age) = quick
    println("$name is $age")       // Roy is 10
}
```

> 💡 You don't need to write many generic classes yourself as a beginner. But you **must be able to read** `List<T>`, `Map<K, V>`, `StateFlow<T>`, etc. You will see these types **all the time** in Android.

---

## 4.11 Use It in Your Android App! 📱

Let us use an **enum**, a **sealed interface**, **extension functions**, and **`buildString`** in our app.

### Step 1: Open the project

Open **MyFirstApp** in Android Studio. Open `MainActivity.kt`.

### Step 2: Add new types and functions

Add this at the **very bottom** of the file (outside of every other `{ }`). You can delete the `ShopItem` class from Chapter 3 or keep it — both are fine.

```kotlin
enum class Mood(val emoji: String) {
    HAPPY("😊"),
    SLEEPY("😴"),
    HUNGRY("😋")
}

sealed interface WeatherState {
    data object Loading : WeatherState
    data class Ready(val city: String, val temperature: Int) : WeatherState
    data class Failed(val reason: String) : WeatherState
}

fun Int.toFeeling(): String = when {
    this < 15 -> "cold 🥶"
    this < 30 -> "nice 😊"
    else -> "hot 🥵"
}

fun WeatherState.toMessage(): String = when (this) {
    WeatherState.Loading -> "Loading the weather... ⏳"
    is WeatherState.Ready -> "In $city it is $temperature°C — ${temperature.toFeeling()}"
    is WeatherState.Failed -> "Sorry! $reason ❌"
}
```

### Every bit explained

**The enum:**

```kotlin
enum class Mood(val emoji: String) {
    HAPPY("😊"),
    ...
}
```

- 3 fixed moods. Each carries an `emoji`.

**The sealed interface:**

```kotlin
sealed interface WeatherState {
    data object Loading : WeatherState
    data class Ready(val city: String, val temperature: Int) : WeatherState
    data class Failed(val reason: String) : WeatherState
}
```

- The weather is **either** Loading, **or** Ready (with a city and temperature), **or** Failed (with a reason).

**Extension function on `Int`:**

```kotlin
fun Int.toFeeling(): String = when {
    this < 15 -> "cold 🥶"
    ...
}
```

- Every `Int` now has `.toFeeling()`. Example: `32.toFeeling()` → `"hot 🥵"`.
- `this` is the number.

**Extension function on `WeatherState`:**

```kotlin
fun WeatherState.toMessage(): String = when (this) {
    WeatherState.Loading -> "..."
    is WeatherState.Ready -> "In $city it is $temperature°C — ${temperature.toFeeling()}"
    is WeatherState.Failed -> "Sorry! $reason ❌"
}
```

- Every `WeatherState` now has `.toMessage()`.
- `when (this)` checks **which kind** it is.
- After `is WeatherState.Ready`, **smart cast** lets us use `city` and `temperature` directly (they are `this.city` and `this.temperature`).
- No `else` needed — sealed! ✅

### Step 3: Change the `Greeting` function

```kotlin
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    val myMood = Mood.HAPPY

    val weatherExamples = listOf(
        WeatherState.Loading,
        WeatherState.Ready(city = "Mumbai", temperature = 32),
        WeatherState.Ready(city = "Oslo", temperature = 4),
        WeatherState.Failed(reason = "No internet")
    )

    val text = buildString {
        appendLine("Hello $name! ${myMood.emoji}")
        appendLine("Today I feel ${myMood.name.lowercase()}.")
        appendLine()
        appendLine("All moods: ${Mood.entries.joinToString(" ") { it.emoji }}")
        appendLine()
        appendLine("Weather examples:")
        weatherExamples.forEach { state ->
            appendLine("• ${state.toMessage()}")
        }
    }

    Text(
        text = text,
        modifier = modifier
    )
}
```

### Every bit explained

| Code | Meaning |
|---|---|
| `val myMood = Mood.HAPPY` | Pick one value from the enum. |
| `listOf(WeatherState.Loading, ...)` | A `List<WeatherState>` with **different kinds** inside (polymorphism!). |
| `WeatherState.Ready(city = "Mumbai", ...)` | Named arguments make it easy to read. |
| `buildString { ... }` | Build one big text, step by step. |
| `appendLine()` (empty) | Adds an empty line. |
| `myMood.name.lowercase()` | `"HAPPY"` → `"happy"`. |
| `Mood.entries.joinToString(" ") { it.emoji }` | All moods → `"😊 😴 😋"`. |
| `weatherExamples.forEach { state -> ... }` | For each weather state… |
| `state.toMessage()` | …use our extension function to get the right message. |

### Step 4: Run it

Click **▶ Run** or look at the **Preview**. You will see:

```
Hello Roy! 😊
Today I feel happy.

All moods: 😊 😴 😋

Weather examples:
• Loading the weather... ⏳
• In Mumbai it is 32°C — hot 🥵
• In Oslo it is 4°C — cold 🥶
• Sorry! No internet ❌
```

🎉 You used **enums**, **sealed interfaces**, **smart casts**, **extension functions**, **lambdas**, and **`buildString`** in a real app!

> 💡 **Try this:** add a new kind to the sealed interface:
> ```kotlin
> data object Offline : WeatherState
> ```
> Android Studio will show a **red error** in `toMessage()`: *"'when' expression must be exhaustive, add necessary 'Offline' branch"*. Kotlin protects you from forgetting a case! Add the missing line to fix it:
> ```kotlin
> WeatherState.Offline -> "You are offline 📴"
> ```

---

## 4.12 Common Mistakes and Fixes 🔧

| Mistake | Example | Error / Problem | Fix |
|---|---|---|---|
| Inheriting from a closed class | `class Cat : Animal()` when Animal is not `open` | *This type is final, so it cannot be inherited from* | Add `open` to the parent class. |
| Overriding a closed function | `override fun sound()` when parent's isn't `open` | *'sound' in 'Animal' is final and cannot be overridden* | Add `open` to the parent's function. |
| Forgetting `override` | `fun sound()` in the child | *'sound' hides member of supertype and needs 'override' modifier* | Add `override`. |
| `val` in child constructor | `class Cat(val name: String) : Animal(name)` | *'name' hides member of supertype 'Animal' and needs 'override' modifier* | Remove `val`: `class Cat(name: String)`. |
| Building an abstract class | `Shape("x")` | *Cannot create an instance of an abstract class* | Build a child (`Square`) instead. |
| Not keeping an interface promise | Class misses `swim()` | *Class 'Duck' is not abstract and does not implement abstract member* | Write `override fun swim()`. |
| Missing branch in `when` | Forgot one enum/sealed value | *'when' expression must be exhaustive* | Add the missing branch. |
| `()` after an object | `AppSettings()` | *Expression 'AppSettings' of type 'AppSettings' cannot be invoked as a function* | Use `AppSettings.something` (no `()`). |
| `is` with a data object | `is WeatherState.Loading` | Works, but not needed | `WeatherState.Loading ->` is enough. |
| Using `as` without `?` | `x as Int` | 💥 *ClassCastException* if wrong | Use `x as? Int` (safe). |

---

## 4.13 Summary — What You Learned 🎓

✅ **Inheritance:** `open class Parent`, `class Child : Parent()`, `open fun` + `override fun`, `super.function()`.
You now fully understand `class MainActivity : ComponentActivity()` and `override fun onCreate`.

✅ **Abstract classes:** unfinished plans with `abstract fun`. Can't build them directly.

✅ **Interfaces:** promises. A class can keep **many** interfaces.

✅ **Type checks:** `is`, `!is`, smart cast, `as?`.

✅ **Enums:** a fixed list of simple choices. `entries`, `name`, `ordinal`. `when` without `else`.

✅ **Sealed types:** a closed family of kinds, each with its own data. Perfect for `Loading / Success / Error`.

✅ **`object`:** one single object (singleton). **`companion object`:** things that belong to the class; `const val`.

✅ **Extension functions:** `fun String.shout()`. `Modifier.padding()` is one!

✅ **Scope functions:**
- `let` (it → result), `run` (this → result), `with` (this → result)
- `apply` (this → object), `also` (it → object)

✅ **Generics:** `<T>` is a type placeholder. `List<T>`, `Box<T>`, `Pair<A, B>`.

---

## 4.14 Practice Time 🏋️

Use the **Kotlin Playground**. Try first, then check the answers! 💪

**Task 1 — Inheritance:**
Make an `open class Vehicle(val name: String)` with an `open fun move()` that prints `"<name> is moving."`.
Make `Car` and `Bicycle` children. `Car` prints `"<name> drives on the road 🚗"`. `Bicycle` prints `"<name> is pedaling 🚲"`. Put them in a `List<Vehicle>` and call `move()` on each.

**Task 2 — Abstract class:**
Make `abstract class Shape` with `abstract fun area(): Double`. Make `Rectangle(width, height)` and `Triangle(base, height)` (triangle area = base × height ÷ 2). Print the area of each.

**Task 3 — Interface:**
Make `interface Playable { fun play() }`. Make `Song(title)` and `Video(title)` that keep the promise. Play both.

**Task 4 — Enum:**
Make `enum class Size(val price: Int) { SMALL(100), MEDIUM(150), LARGE(200) }`. Print every size and its price using `entries`.

**Task 5 — Sealed:**
Make a sealed interface `LoginResult` with:
- `data object Success`
- `data class WrongPassword(val triesLeft: Int)`
- `data class Blocked(val minutes: Int)`

Write `fun message(result: LoginResult): String` using `when`. Test all three.

**Task 6 — Extension:**
Write `fun String.isPalindrome(): Boolean` — `true` if the word is the same backwards (ignore BIG/small letters). Test with `"Level"`, `"racecar"`, and `"kotlin"`.

**Task 7 — Scope functions:**
Use `apply` to make and set up a `Pizza` object (from 4.9) with size `"Small"` and cheese `true`. Then use `also` to print it.

**Task 8 — Companion object:**
Make `class Temperature(val celsius: Double)` with a companion object that has `fun fromFahrenheit(f: Double): Temperature` (formula: C = (F − 32) × 5 ÷ 9). Make one from `212.0` and print its `celsius`.

---

### Answers

**Task 1:**

```kotlin
open class Vehicle(val name: String) {
    open fun move() {
        println("$name is moving.")
    }
}

class Car(name: String) : Vehicle(name) {
    override fun move() {
        println("$name drives on the road 🚗")
    }
}

class Bicycle(name: String) : Vehicle(name) {
    override fun move() {
        println("$name is pedaling 🚲")
    }
}

fun main() {
    val garage: List<Vehicle> = listOf(Car("Tesla"), Bicycle("BMX"), Vehicle("Cart"))
    for (v in garage) {
        v.move()
    }
}
```

Output:

```
Tesla drives on the road 🚗
BMX is pedaling 🚲
Cart is moving.
```

**Task 2:**

```kotlin
abstract class Shape {
    abstract fun area(): Double
}

class Rectangle(val width: Double, val height: Double) : Shape() {
    override fun area() = width * height
}

class Triangle(val base: Double, val height: Double) : Shape() {
    override fun area() = base * height / 2
}

fun main() {
    println(Rectangle(4.0, 5.0).area())   // 20.0
    println(Triangle(6.0, 3.0).area())    // 9.0
}
```

`Shape()` has empty brackets, because `Shape` has no inputs.

**Task 3:**

```kotlin
interface Playable {
    fun play()
}

class Song(val title: String) : Playable {
    override fun play() {
        println("🎵 Playing song: $title")
    }
}

class Video(val title: String) : Playable {
    override fun play() {
        println("🎬 Playing video: $title")
    }
}

fun main() {
    val playlist: List<Playable> = listOf(Song("Happy"), Video("Cute Cats"))
    playlist.forEach { it.play() }
}
```

Note: interfaces have **no** `()` after them: `: Playable`, not `: Playable()`.

**Task 4:**

```kotlin
enum class Size(val price: Int) {
    SMALL(100), MEDIUM(150), LARGE(200)
}

fun main() {
    for (size in Size.entries) {
        println("${size.name}: ${size.price}")
    }
}
```

Output:

```
SMALL: 100
MEDIUM: 150
LARGE: 200
```

**Task 5:**

```kotlin
sealed interface LoginResult {
    data object Success : LoginResult
    data class WrongPassword(val triesLeft: Int) : LoginResult
    data class Blocked(val minutes: Int) : LoginResult
}

fun message(result: LoginResult): String = when (result) {
    LoginResult.Success -> "Welcome! ✅"
    is LoginResult.WrongPassword -> "Wrong password. ${result.triesLeft} tries left."
    is LoginResult.Blocked -> "Too many tries. Wait ${result.minutes} minutes. ⛔"
}

fun main() {
    println(message(LoginResult.Success))
    println(message(LoginResult.WrongPassword(2)))
    println(message(LoginResult.Blocked(15)))
}
```

Output:

```
Welcome! ✅
Wrong password. 2 tries left.
Too many tries. Wait 15 minutes. ⛔
```

**Task 6:**

```kotlin
fun String.isPalindrome(): Boolean {
    val small = this.lowercase()
    return small == small.reversed()
}

fun main() {
    println("Level".isPalindrome())    // true
    println("racecar".isPalindrome())  // true
    println("kotlin".isPalindrome())   // false
}
```

**Task 7:**

```kotlin
class Pizza {
    var size = "Medium"
    var cheese = false
}

fun main() {
    val pizza = Pizza()
        .apply {
            size = "Small"
            cheese = true
        }
        .also {
            println("Pizza ready: size=${it.size}, cheese=${it.cheese} 🍕")
        }
}
```

Output: `Pizza ready: size=Small, cheese=true 🍕`

**Task 8:**

```kotlin
class Temperature(val celsius: Double) {
    companion object {
        fun fromFahrenheit(f: Double): Temperature {
            return Temperature((f - 32) * 5 / 9)
        }
    }
}

fun main() {
    val boiling = Temperature.fromFahrenheit(212.0)
    println(boiling.celsius)   // 100.0
}
```

---

## 4.15 What Is Next?

🎉 **You finished the Kotlin part of the book!** You now know more Kotlin than you need to start.

In **Chapter 5: Your First Compose Screen**, we start building **real screens**:

- What a **Composable function** really is
- Showing text with **`Text`** (sizes, colors, bold)
- Showing pictures with **`Image`** and **`Icon`**
- Making **`Button`s** that do something when tapped
- Using the **Preview** like a pro
- **Modifiers** — changing size, padding, background, borders, and more

No more one big `Text` — time to make apps that **look** like apps! 🎨📱

**Great job finishing Chapter 4! 🎉 You are now a Kotlin programmer!**
