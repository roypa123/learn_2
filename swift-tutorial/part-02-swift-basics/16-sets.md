# Chapter 16 — No Duplicates: Sets

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What a **set** is.
- How sets remove duplicates automatically.
- Adding, removing and checking items.
- Comparing sets: union, intersection, difference.

---

## 1. What is a set?

Imagine a sticker collection 🌟. You only want **one** of each sticker.
If a friend gives you a sticker you already have, you don't add it again.

> 📖 **New word: Set**
> A collection of **unique** values (no duplicates) with **no order**.

| | Array | Set | Dictionary |
|---|---|---|---|
| Has order? | ✅ Yes | ❌ No | ❌ No |
| Duplicates allowed? | ✅ Yes | ❌ No | Keys: ❌ No |
| Find by | position | the value itself | key |

---

## 2. Making a set

```swift
let colors: Set = ["red", "green", "blue", "red"]
print(colors)
print(colors.count)
```

**Output** (order may be different):

```
["green", "red", "blue"]
3
```

| Part | Meaning |
|---|---|
| `: Set` | "Make this a **set**, not an array." Without this, Swift would make an array! |
| `["red", "green", "blue", "red"]` | We wrote `"red"` twice… |
| `count` is 3 | …but the set keeps only **one** `"red"`. |

You can also write the full type:

```swift
let numbers: Set<Int> = [1, 2, 3]
```

`Set<Int>` means "a set of Int".

⚠️ **Careful:** Without `: Set`, square brackets make an **array**.

```swift
let a = [1, 2, 2]         // Array: [1, 2, 2]
let b: Set = [1, 2, 2]    // Set: [1, 2]
```

---

## 3. Removing duplicates from an array

A very useful trick:

```swift
let visitors = ["Ravi", "Meena", "Ravi", "Arun", "Meena"]
let uniqueVisitors = Set(visitors)

print(uniqueVisitors.count)
```

**Output:**

```
3
```

| Part | Meaning |
|---|---|
| `Set(visitors)` | Make a set from the array. Duplicates disappear. |

Want an array back (sorted)?

```swift
let sortedVisitors = uniqueVisitors.sorted()
print(sortedVisitors)
```

**Output:**

```
["Arun", "Meena", "Ravi"]
```

---

## 4. Empty set and adding items

```swift
var stickers = Set<String>()

stickers.insert("⭐")
stickers.insert("🌙")
stickers.insert("⭐")   // already there — ignored

print(stickers.count)
```

**Output:**

```
2
```

| Part | Meaning |
|---|---|
| `Set<String>()` | An empty set of strings. |
| `.insert("⭐")` | Add an item. Sets use `insert`, not `append` (there is no "end" in a set!). |
| Second `"⭐"` | Already there, so nothing changes. |

---

## 5. Removing and checking

```swift
var stickers: Set = ["⭐", "🌙", "☀️"]

stickers.remove("🌙")
print(stickers.contains("🌙"))
print(stickers.contains("⭐"))
```

**Output:**

```
false
true
```

| Method | Meaning |
|---|---|
| `.remove(x)` | Remove `x` from the set. |
| `.contains(x)` | Is `x` in the set? |

💡 **Tip:** `contains` is **super fast** on a set — much faster than on a big array. If you check "is this in the list?" many times, a set is a great choice.

---

## 6. Looping through a set

```swift
let fruits: Set = ["apple", "mango", "kiwi"]

for fruit in fruits.sorted() {
    print(fruit)
}
```

**Output:**

```
apple
kiwi
mango
```

We used `.sorted()` so the order is always the same (A to Z).

---

## 7. Set math 🧮

Two friends and the games they like:

```swift
let ravi: Set = ["chess", "cricket", "football"]
let meena: Set = ["chess", "tennis", "football"]
```

```
      ravi                 meena
  ┌───────────┐       ┌───────────┐
  │ cricket ┌─┼───────┼─┐ tennis  │
  │         │ chess   │ │         │
  │         │ football│ │         │
  │         └─┼───────┼─┘         │
  └───────────┘       └───────────┘
```

### Union — everything from both

```swift
print(ravi.union(meena).sorted())
```

**Output:**

```
["chess", "cricket", "football", "tennis"]
```

All games that **either** friend likes.

### Intersection — only the shared ones

```swift
print(ravi.intersection(meena).sorted())
```

**Output:**

```
["chess", "football"]
```

Games that **both** like. They can play these together! 🎮

### Subtracting — only in the first

```swift
print(ravi.subtracting(meena).sorted())
```

**Output:**

```
["cricket"]
```

Games **only Ravi** likes.

### Symmetric difference — in one but not both

```swift
print(ravi.symmetricDifference(meena).sorted())
```

**Output:**

```
["cricket", "tennis"]
```

| Method | Meaning | Result |
|---|---|---|
| `a.union(b)` | in a **or** b | chess, cricket, football, tennis |
| `a.intersection(b)` | in a **and** b | chess, football |
| `a.subtracting(b)` | in a but **not** b | cricket |
| `a.symmetricDifference(b)` | in one, but **not both** | cricket, tennis |

---

## 8. Mini project: who hasn't submitted homework? 📚

```swift
let allStudents: Set = ["Ravi", "Meena", "Arun", "Priya", "John"]
let submitted: Set = ["Meena", "John", "Ravi"]

let missing = allStudents.subtracting(submitted)

print("Not submitted yet:")
for name in missing.sorted() {
    print("- \(name)")
}
```

**Output:**

```
Not submitted yet:
- Arun
- Priya
```

| Line | Meaning |
|---|---|
| `allStudents.subtracting(submitted)` | Everyone in the class, minus those who submitted. |
| `missing.sorted()` | Sort A to Z so the list is neat. |

---

## 🏋️ Practice

1. Make a set from `[1, 2, 2, 3, 3, 3, 4]`. Print its count.
2. Make an empty `Set<String>`. Insert `"cat"`, `"dog"`, `"cat"`. Print the count.
3. Check if your set from exercise 2 contains `"dog"`.
4. Set A = `[1, 2, 3, 4]` and Set B = `[3, 4, 5, 6]`. Print their union, intersection and A subtracting B (all sorted).

<details>
<summary>Click to see the answers</summary>

```swift
// 1
let numbers = Set([1, 2, 2, 3, 3, 3, 4])
print(numbers.count)   // 4

// 2
var pets = Set<String>()
pets.insert("cat")
pets.insert("dog")
pets.insert("cat")
print(pets.count)   // 2

// 3
print(pets.contains("dog"))   // true

// 4
let a: Set = [1, 2, 3, 4]
let b: Set = [3, 4, 5, 6]
print(a.union(b).sorted())          // [1, 2, 3, 4, 5, 6]
print(a.intersection(b).sorted())   // [3, 4]
print(a.subtracting(b).sorted())    // [1, 2]
```

</details>

---

## 🧠 Remember

- A **set** holds **unique** values with **no order**.
- Make one with `let x: Set = [...]` or `Set<Type>()`.
- `insert`, `remove`, `contains` — and `contains` is very fast.
- `Set(array)` removes duplicates.
- `union`, `intersection`, `subtracting` compare two sets.

---

⬅️ **Back:** [Chapter 15 — Dictionaries](15-dictionaries.md)
➡️ **Next:** [Chapter 17 — Optionals](17-optionals.md)
