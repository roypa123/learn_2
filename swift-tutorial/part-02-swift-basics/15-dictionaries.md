# Chapter 15 — Labels and Values: Dictionaries

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What a **dictionary** is.
- What **keys** and **values** are.
- Reading, adding, changing and removing.
- Using a **default** value.
- Looping through a dictionary.

---

## 1. Why dictionaries?

Think of a real dictionary 📖:

- You look up a **word** → you find its **meaning**.

Or a phone contact list 📱:

- You look up a **name** → you find the **phone number**.

With an array, you find things by **position** (0, 1, 2…).
With a dictionary, you find things by a **label**.

> 📖 **New word: Dictionary**
> A collection of **key–value pairs**. You use the **key** to find the **value**.

> 📖 **New word: Key**
> The label you look up. Like a word in a dictionary. Each key is **unique** (only once).

> 📖 **New word: Value**
> The thing stored for a key. Like the meaning of a word.

---

## 2. Making a dictionary

```swift
let ages = ["Ravi": 12, "Meena": 10, "Arun": 14]
print(ages)
```

**Output** (the order may be different!):

```
["Meena": 10, "Ravi": 12, "Arun": 14]
```

| Part | Meaning |
|---|---|
| `[` | Start. |
| `"Ravi": 12` | One pair: key `"Ravi"`, value `12`. The `:` connects them. |
| `,` | Separates the pairs. |
| `]` | End. |

The type is **`[String: Int]`** — keys are `String`, values are `Int`.

```
   KEY         VALUE
┌─────────┬─────────┐
│ "Ravi"  │   12    │
│ "Meena" │   10    │
│ "Arun"  │   14    │
└─────────┴─────────┘
```

⚠️ **Careful:** A dictionary has **no order**. When you print it, the order can change every time you run. That's normal!

---

## 3. Reading a value

```swift
let ages = ["Ravi": 12, "Meena": 10, "Arun": 14]
print(ages["Ravi"])
```

**Output:**

```
Optional(12)
```

Why `Optional`? Because the key might **not exist**:

```swift
print(ages["Zara"])
```

**Output:**

```
nil
```

> 📖 **New word: nil**
> Means **nothing** — no value. Like an empty box.

So Swift says: *"Maybe I found a value, maybe not."* That's an **Optional**. We learn all about them in **Chapter 17**.

### The easy way: a default value ⭐

```swift
let ages = ["Ravi": 12, "Meena": 10, "Arun": 14]

print(ages["Ravi", default: 0])
print(ages["Zara", default: 0])
```

**Output:**

```
12
0
```

| Part | Meaning |
|---|---|
| `ages["Ravi", default: 0]` | "Give me Ravi's value. If Ravi is not there, give me `0`." |

Now we always get a real `Int`, never `nil`. 😊

---

## 4. Empty dictionary

```swift
var scores: [String: Int] = [:]
print(scores.count)
```

**Output:**

```
0
```

| Part | Meaning |
|---|---|
| `: [String: Int]` | Keys are `String`, values are `Int`. |
| `= [:]` | Empty dictionary. Note the colon inside! |

| Empty array | Empty dictionary |
|---|---|
| `[]` | `[:]` |

---

## 5. Adding and changing

The same code does both!

```swift
var scores: [String: Int] = [:]

scores["Ravi"] = 50      // add (Ravi is new)
scores["Meena"] = 80     // add (Meena is new)
scores["Ravi"] = 65      // change (Ravi already exists)

print(scores["Ravi", default: 0])
print(scores.count)
```

**Output:**

```
65
2
```

| Line | What happens |
|---|---|
| `scores["Ravi"] = 50` | Key `"Ravi"` doesn't exist → **add** it with 50. |
| `scores["Meena"] = 80` | Key `"Meena"` doesn't exist → **add** it. |
| `scores["Ravi"] = 65` | Key `"Ravi"` already exists → **replace** 50 with 65. |
| `scores.count` | 2 keys. (Ravi is only counted once.) |

🧠 **Remember:** Keys are **unique**. One key can't appear twice.

---

## 6. Removing

```swift
var scores = ["Ravi": 65, "Meena": 80]

scores["Ravi"] = nil
print(scores)
```

**Output:**

```
["Meena": 80]
```

| Part | Meaning |
|---|---|
| `scores["Ravi"] = nil` | Set Ravi's value to "nothing" → **removes** the key. |

Another way: `scores.removeValue(forKey: "Ravi")`

---

## 7. Checking if a key exists

```swift
let capitals = ["India": "New Delhi", "Japan": "Tokyo"]

if capitals["Japan"] != nil {
    print("We know Japan's capital.")
}

print(capitals.keys.contains("France"))
```

**Output:**

```
We know Japan's capital.
false
```

| Part | Meaning |
|---|---|
| `capitals["Japan"] != nil` | Is the value **not** nothing? → the key exists. |
| `capitals.keys` | All the keys. |
| `.contains("France")` | Is `"France"` one of them? |

---

## 8. Looping through a dictionary

```swift
let capitals = ["India": "New Delhi", "Japan": "Tokyo", "France": "Paris"]

for (country, city) in capitals {
    print("The capital of \(country) is \(city).")
}
```

**Output** (order may be different):

```
The capital of Japan is Tokyo.
The capital of India is New Delhi.
The capital of France is Paris.
```

| Part | Meaning |
|---|---|
| `for (country, city) in capitals` | Each round, put the **key** in `country` and the **value** in `city`. |

### In order (sorted by key)

```swift
for (country, city) in capitals.sorted(by: { $0.key < $1.key }) {
    print("\(country): \(city)")
}
```

**Output:**

```
France: Paris
India: New Delhi
Japan: Tokyo
```

The `{ $0.key < $1.key }` part is a **closure**. We learn closures in **Chapter 19**. For now, just know it means "sort by key, A to Z".

### Only keys or only values

```swift
let prices = ["pen": 10, "book": 50]

for item in prices.keys {
    print(item)
}

for price in prices.values {
    print(price)
}
```

---

## 9. Counting things — a classic! 🔢

Count how many times each fruit appears:

```swift
let basket = ["apple", "banana", "apple", "mango", "apple", "banana"]
var counts: [String: Int] = [:]

for fruit in basket {
    counts[fruit, default: 0] += 1
}

print(counts["apple", default: 0])
print(counts["banana", default: 0])
print(counts["mango", default: 0])
```

**Output:**

```
3
2
1
```

The key line: `counts[fruit, default: 0] += 1`

| Step | Meaning |
|---|---|
| `counts[fruit, default: 0]` | Get the current count. If it's a new fruit, start at 0. |
| `+= 1` | Add one and store it back. |

Step by step:

| Fruit | Before | After |
|---|---|---|
| apple | apple: 0 (new) | apple: 1 |
| banana | banana: 0 (new) | banana: 1 |
| apple | apple: 1 | apple: 2 |
| mango | mango: 0 (new) | mango: 1 |
| apple | apple: 2 | apple: 3 |
| banana | banana: 1 | banana: 2 |

---

## 10. Array or dictionary?

| Use an **array** when… | Use a **dictionary** when… |
|---|---|
| Order matters. | You look things up by a label. |
| You find items by position. | Each item has a unique name/ID. |
| Example: a to-do list, a playlist. | Example: contacts, prices, settings. |

---

## 11. Mini project: a tiny shop 🛒

```swift
let prices = ["pen": 10, "notebook": 45, "eraser": 5]
let cart = ["pen", "notebook", "pen", "eraser", "ruler"]

var total = 0

for item in cart {
    if let price = prices[item] {
        print("\(item): \(price)")
        total += price
    } else {
        print("\(item): not sold here")
    }
}

print("Total: \(total)")
```

**Output:**

```
pen: 10
notebook: 45
pen: 10
eraser: 5
ruler: not sold here
Total: 70
```

| Line | Meaning |
|---|---|
| `for item in cart` | Go through each item in the cart. |
| `if let price = prices[item]` | "If this item has a price, call it `price`…" (an Optional trick — Chapter 17) |
| `total += price` | Add the price to the total. |
| `else` | The item is not in `prices` (like `"ruler"`). |

---

## 🏋️ Practice

1. Make a dictionary of 3 countries and their capitals. Print one capital using `default: "Unknown"`.
2. Make an empty `[String: Int]` called `stock`. Add `"apples": 10` and `"bananas": 5`. Change apples to 8. Print the count of keys.
3. Remove `"bananas"` from `stock`.
4. Loop through `["red": "🍎", "yellow": "🍌", "green": "🥝"]` and print `red → 🍎` and so on.
5. Count the letters in `"banana"` using a dictionary. (Hint: `for letter in "banana"` and use `String(letter)` as the key.)

<details>
<summary>Click to see the answers</summary>

```swift
// 1
let capitals = ["India": "New Delhi", "Japan": "Tokyo", "Kenya": "Nairobi"]
print(capitals["Japan", default: "Unknown"])

// 2
var stock: [String: Int] = [:]
stock["apples"] = 10
stock["bananas"] = 5
stock["apples"] = 8
print(stock.count)   // 2

// 3
stock["bananas"] = nil

// 4
let colors = ["red": "🍎", "yellow": "🍌", "green": "🥝"]
for (color, emoji) in colors {
    print("\(color) → \(emoji)")
}

// 5
var letterCounts: [String: Int] = [:]
for letter in "banana" {
    letterCounts[String(letter), default: 0] += 1
}
print(letterCounts)   // b: 1, a: 3, n: 2 (order may vary)
```

</details>

---

## 🧠 Remember

- A dictionary stores **key: value** pairs: `["Ravi": 12]`.
- Keys are **unique**. A dictionary has **no order**.
- `dict[key]` gives an Optional. Use `dict[key, default: x]` for a safe value.
- `dict[key] = value` adds or changes. `dict[key] = nil` removes.
- `for (key, value) in dict { }` loops through all pairs.

---

⬅️ **Back:** [Chapter 14 — Arrays](14-arrays.md)
➡️ **Next:** [Chapter 16 — No Duplicates: Sets](16-sets.md)
