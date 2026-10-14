# Chapter 22 — Struct vs Class: When to Use Which

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- A side-by-side comparison of structs and classes.
- A simple rule to choose.
- Common bugs that happen when you choose wrong.

This chapter is short, but **very important**. Many beginners get confused here.

---

## 1. Side by side

| Feature | `struct` | `class` |
|---|---|---|
| Assigning (`b = a`) | **Copies** 📄📄 | **Shares** the same object 🌐 |
| Type kind | Value type | Reference type |
| Automatic `init` | ✅ Yes | ❌ No — you write it |
| Inheritance | ❌ No | ✅ Yes |
| `let` instance can change `var` properties? | ❌ No | ✅ Yes |
| Methods that change properties | need `mutating` | no keyword needed |
| `deinit` | ❌ No | ✅ Yes |
| Compare identity with `===` | ❌ No | ✅ Yes |

---

## 2. The same code, two results

### With a struct

```swift
struct PlayerS {
    var score = 0
}

var p1 = PlayerS()
var p2 = p1
p2.score = 50

print("p1:", p1.score)
print("p2:", p2.score)
```

**Output:**

```
p1: 0
p2: 50
```

### With a class

```swift
class PlayerC {
    var score = 0
}

let q1 = PlayerC()
let q2 = q1
q2.score = 50

print("q1:", q1.score)
print("q2:", q2.score)
```

**Output:**

```
q1: 50
q2: 50
```

| | Struct | Class |
|---|---|---|
| After `p2 = p1` | two separate players | one player, two names |
| Changing one | the other stays the same | both see the change |

---

## 3. The simple rule 🧭

🧠 **Remember:** **Use a struct by default.** Use a class only when you need something a struct can't do.

Apple itself recommends this. Most Swift types are structs: `Int`, `String`, `Array`, `Dictionary` — and all SwiftUI views!

### Use a `struct` when…

- The thing is just **data**: a point, a color, a student record, a settings value.
- Each copy should be **independent**.
- You want **safety**: nobody can change your copy by surprise.

### Use a `class` when…

- Many parts of the app must **share and see the same** thing. (Example: one shopping cart that every screen uses.)
- You need **inheritance**.
- You need `deinit`, or the **identity** of the object matters ("is this the *same* one?").
- Apple's tools ask for a class. (In SwiftUI, shared data models with `@Observable` are classes — Chapter 53.)

---

## 4. A real-life way to think 🌍

| Real life | Best match | Why |
|---|---|---|
| A **photo** you send to a friend | struct | They get a **copy**. If they draw on it, your photo stays the same. |
| A **shared family calendar** | class | Everyone sees the **same** calendar. One change, everyone sees it. |
| A **birthday** (a date) | struct | Just a value. |
| A **bank account** used by an app and a website | class | Both must see the same balance. |

---

## 5. Bug example: accidental sharing 🐛

```swift
class Settings {
    var volume = 5
}

let mySettings = Settings()
let friendSettings = mySettings     // oops — meant to make a copy!

friendSettings.volume = 0           // friend mutes their sound

print("My volume:", mySettings.volume)
```

**Output:**

```
My volume: 0
```

😱 The friend changed **your** volume! Because a class is shared.

If `Settings` were a `struct`, `friendSettings` would be a **copy**, and your volume would stay 5. ✅

---

## 6. Bug example: changes "disappear" 🐛

The opposite problem — you wanted sharing, but used a struct:

```swift
struct Cart {
    var items: [String] = []
}

var mainCart = Cart()
var checkoutCart = mainCart        // a COPY

checkoutCart.items.append("Book")

print("Main cart:", mainCart.items)
```

**Output:**

```
Main cart: []
```

The book was added to the **copy**, not the main cart. If the whole app should share **one** cart, a class (or a single shared source) is the right choice.

---

## 7. A mixed example: struct inside a class

You can use **both** together. This is very common.

```swift
struct Item {
    let name: String
    let price: Double
}

final class ShoppingCart {
    var items: [Item] = []

    var total: Double {
        items.reduce(0) { $0 + $1.price }
    }

    func add(_ item: Item) {
        items.append(item)
    }
}

let cart = ShoppingCart()        // one shared cart
let screenA = cart
let screenB = cart

screenA.add(Item(name: "Pen", price: 10))
screenB.add(Item(name: "Book", price: 120))

print("Items:", cart.items.count)
print("Total:", cart.total)
```

**Output:**

```
Items: 2
Total: 130.0
```

| Part | Why |
|---|---|
| `struct Item` | An item is just data. Copies are fine. |
| `final class ShoppingCart` | The cart must be **shared** between screens. |
| `screenA`, `screenB` | Both point to the same cart. |

---

## 🏋️ Practice

Decide: **struct** or **class**? Write your answer and a short reason.

1. A `Color` with red, green and blue values.
2. A `MusicPlayer` that the whole app uses to play songs.
3. A `Location` with latitude and longitude.
4. A `GameCharacter` base type with `Warrior` and `Wizard` types that inherit from it.
5. A `Message` in a chat (text, sender, time).

<details>
<summary>Click to see the answers</summary>

1. **struct** — it's just data (three numbers).
2. **class** — one player must be shared by the whole app.
3. **struct** — just two numbers.
4. **class** — needs inheritance. (Later you'll learn protocols can also solve this — Chapter 24!)
5. **struct** — a message is data. Copies are safe.

</details>

---

## 🧠 Remember

- **Struct** = copy. **Class** = shared.
- **Start with a struct.** Switch to a class only when you need sharing, inheritance or identity.
- Wrong choice → bugs: unexpected sharing (class) or lost changes (struct).

---

⬅️ **Back:** [Chapter 21 — Classes](21-classes.md)
➡️ **Next:** [Chapter 23 — Enums](23-enums.md)
