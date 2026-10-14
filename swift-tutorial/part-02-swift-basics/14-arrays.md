# Chapter 14 — Lists of Things: Arrays

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What an **array** is.
- How to get an item by its **index** (position).
- Adding, changing and removing items.
- Looping through an array.
- Useful tools: `count`, `isEmpty`, `contains`, `first`, `last`, `sorted()`.

---

## 1. Why arrays?

Imagine you want to store 5 friends' names:

```swift
let friend1 = "Ravi"
let friend2 = "Meena"
let friend3 = "Arun"
let friend4 = "Priya"
let friend5 = "John"
```

What if you have 100 friends? 😵 That's 100 boxes!

An **array** is **one box with many compartments** — like an egg tray 🥚🥚🥚 or a train 🚃🚃🚃.

> 📖 **New word: Array**
> An **ordered list** of values, all of the **same type**.

---

## 2. Making an array

```swift
let friends = ["Ravi", "Meena", "Arun"]
print(friends)
```

**Output:**

```
["Ravi", "Meena", "Arun"]
```

| Part | Meaning |
|---|---|
| `let friends` | A constant called `friends`. |
| `[` | Start of the array. Square bracket. |
| `"Ravi", "Meena", "Arun"` | The items, separated by commas. |
| `]` | End of the array. |

Swift sees all items are `String`, so the type is **`[String]`** (read: "array of String").

More examples:

```swift
let scores = [90, 85, 72]           // [Int]
let prices = [9.99, 4.50, 12.0]     // [Double]
let answers = [true, false, true]   // [Bool]
```

⚠️ **Careful:** All items must be the **same type**.

```swift
let mixed = ["Ravi", 25]   // ❌ ERROR: Strings and Ints mixed
```

---

## 3. Index: the position of an item

Every item has a **position number**, called the **index**.

⚠️ **Very important:** Counting starts at **0**, not 1!

```
    index:    0        1        2
          ┌────────┬────────┬────────┐
friends:  │ "Ravi" │"Meena" │ "Arun" │
          └────────┴────────┴────────┘
```

> 📖 **New word: Index**
> The position number of an item in an array. The first item is at index **0**.

### Getting an item

```swift
let friends = ["Ravi", "Meena", "Arun"]
print(friends[0])
print(friends[1])
print(friends[2])
```

**Output:**

```
Ravi
Meena
Arun
```

| Part | Meaning |
|---|---|
| `friends` | The array. |
| `[0]` | "Give me the item at index 0" → the **first** item. |

💡 **Tip:** Think of floors in some buildings: the ground floor is 0, then 1, 2… The first item is on "floor 0".

### ⚠️ Index out of range

```swift
let friends = ["Ravi", "Meena", "Arun"]
print(friends[3])   // ❌ CRASH!
```

**Error:**

```
Fatal error: Index out of range
```

There are 3 items: indexes 0, 1, 2. Index **3 does not exist**. The program **crashes**.

🧠 **Remember:** The last index is always **count − 1**.

---

## 4. Counting items

```swift
let friends = ["Ravi", "Meena", "Arun"]
print(friends.count)
print(friends.isEmpty)
```

**Output:**

```
3
false
```

| Part | Meaning |
|---|---|
| `.count` | How many items. |
| `.isEmpty` | `true` if there are no items. |

---

## 5. First and last

```swift
let friends = ["Ravi", "Meena", "Arun"]
print(friends.first!)
print(friends.last!)
```

**Output:**

```
Ravi
Arun
```

What is the `!`? An empty array has **no** first item. So `first` gives an **Optional** (maybe a value, maybe nothing). The `!` says "I'm sure it has a value". We explain this properly in **Chapter 17**. For now, use it only when you are sure the array is not empty.

---

## 6. Making an empty array

To add things later, start with an **empty** array. You must say the type.

```swift
var shoppingList: [String] = []
print(shoppingList.count)
```

**Output:**

```
0
```

| Part | Meaning |
|---|---|
| `var` | `var`, because we will change it. |
| `: [String]` | Type: an array of strings. |
| `= []` | Empty array — nothing inside yet. |

Another way to write the same thing:

```swift
var shoppingList = [String]()
```

---

## 7. Adding items

```swift
var shoppingList: [String] = []

shoppingList.append("Milk")
shoppingList.append("Bread")
shoppingList.append("Eggs")

print(shoppingList)
```

**Output:**

```
["Milk", "Bread", "Eggs"]
```

| Part | Meaning |
|---|---|
| `.append("Milk")` | Add `"Milk"` at the **end** of the array. |

> 📖 **New word: Append**
> Add to the end.

### Adding with `+=`

```swift
var numbers = [1, 2]
numbers += [3, 4]
print(numbers)
```

**Output:**

```
[1, 2, 3, 4]
```

### Inserting at a position

```swift
var letters = ["A", "C"]
letters.insert("B", at: 1)
print(letters)
```

**Output:**

```
["A", "B", "C"]
```

| Part | Meaning |
|---|---|
| `insert("B", at: 1)` | Put `"B"` at index 1. Everything after moves right. |

⚠️ **Careful:** You can only change an array made with `var`. With `let`, you get an error.

---

## 8. Changing an item

```swift
var colors = ["red", "green", "blue"]
colors[1] = "yellow"
print(colors)
```

**Output:**

```
["red", "yellow", "blue"]
```

| Part | Meaning |
|---|---|
| `colors[1] = "yellow"` | Replace the item at index 1 (`"green"`) with `"yellow"`. |

---

## 9. Removing items

```swift
var fruits = ["apple", "banana", "cherry", "mango"]

fruits.remove(at: 1)
print(fruits)

fruits.removeLast()
print(fruits)

fruits.removeAll()
print(fruits)
```

**Output:**

```
["apple", "cherry", "mango"]
["apple", "cherry"]
[]
```

| Line | Meaning |
|---|---|
| `remove(at: 1)` | Remove the item at index 1 (`"banana"`). Items after it move left. |
| `removeLast()` | Remove the last item (`"mango"`). |
| `removeAll()` | Remove everything. |

---

## 10. Looping through an array ⭐

This is where arrays and loops become best friends.

```swift
let friends = ["Ravi", "Meena", "Arun"]

for friend in friends {
    print("Hello, \(friend)!")
}
```

**Output:**

```
Hello, Ravi!
Hello, Meena!
Hello, Arun!
```

| Part | Meaning |
|---|---|
| `for friend in friends` | For **each** item in `friends`, put it in the box `friend`. |
| `print("Hello, \(friend)!")` | Use the current item. |

💡 **Tip:** Use a **plural** name for the array (`friends`) and a **singular** name for one item (`friend`). It reads like English!

### Loop with index and item: `enumerated()`

```swift
let friends = ["Ravi", "Meena", "Arun"]

for (index, friend) in friends.enumerated() {
    print("\(index): \(friend)")
}
```

**Output:**

```
0: Ravi
1: Meena
2: Arun
```

| Part | Meaning |
|---|---|
| `friends.enumerated()` | Gives pairs: (0, "Ravi"), (1, "Meena"), (2, "Arun"). |
| `(index, friend)` | Put the number in `index` and the name in `friend`. |

---

## 11. Searching

```swift
let pets = ["cat", "dog", "fish"]

print(pets.contains("dog"))
print(pets.contains("lion"))
```

**Output:**

```
true
false
```

### Finding the position

```swift
let pets = ["cat", "dog", "fish"]

if let position = pets.firstIndex(of: "dog") {
    print("dog is at index \(position)")
}
```

**Output:**

```
dog is at index 1
```

`if let` is part of **Optionals** (Chapter 17). Here it means: *"If you found it, call the position `position` and run this code."*

---

## 12. Sorting and reversing

```swift
let numbers = [5, 2, 9, 1]

print(numbers.sorted())
print(numbers.reversed())
print(numbers)
```

**Output:**

```
[1, 2, 5, 9]
ReversedCollection<Array<Int>>(...)
[5, 2, 9, 1]
```

Hmm, `reversed()` prints something strange. To get a normal array, wrap it: `Array(numbers.reversed())` → `[1, 9, 2, 5]`.

| Method | Gives back |
|---|---|
| `.sorted()` | A **new** array, small to big. |
| `.sorted(by: >)` | A **new** array, big to small. |
| `Array(x.reversed())` | A **new** array, backwards. |

Notice: `numbers` itself did **not** change.

To change the array itself, use `sort()` (no "-ed"):

```swift
var numbers = [5, 2, 9, 1]
numbers.sort()
print(numbers)
```

**Output:**

```
[1, 2, 5, 9]
```

| | `sorted()` | `sort()` |
|---|---|---|
| Changes the original? | No | Yes |
| Needs `var`? | No | Yes |

---

## 13. Math helpers

```swift
let scores = [70, 95, 82]

print(scores.min()!)
print(scores.max()!)

var total = 0
for s in scores {
    total += s
}
print("Total: \(total)")
print("Average: \(Double(total) / Double(scores.count))")
```

**Output:**

```
70
95
Total: 247
Average: 82.33333333333333
```

(`min()` and `max()` give Optionals because an empty array has no min or max — so we use `!` here.)

---

## 14. Mini project: class report card 📋

```swift
let students = ["Ravi", "Meena", "Arun", "Priya"]
let marks = [78, 92, 45, 66]

for i in 0..<students.count {
    let name = students[i]
    let mark = marks[i]
    let result = mark >= 50 ? "Pass ✅" : "Fail ❌"
    print("\(name): \(mark) — \(result)")
}
```

**Output:**

```
Ravi: 78 — Pass ✅
Meena: 92 — Pass ✅
Arun: 45 — Fail ❌
Priya: 66 — Pass ✅
```

| Line | Meaning |
|---|---|
| `for i in 0..<students.count` | `i` goes 0, 1, 2, 3 (count is 4, so stop before 4). |
| `students[i]` | The name at position `i`. |
| `marks[i]` | The mark at the same position. |
| `mark >= 50 ? ... : ...` | Choose the result text. |

---

## 🏋️ Practice

1. Make an array of 5 of your favorite foods. Print the first and the third one.
2. Print how many items are in your food array.
3. Start with an empty `[Int]` array. Append 10, 20 and 30. Print it.
4. Make `var animals = ["cat", "dog", "cow"]`. Change `"dog"` to `"lion"`. Remove `"cat"`. Print it.
5. Loop through `[3, 6, 9, 12]` and print each number times 2.
6. Find the sum of `[4, 8, 15, 16, 23, 42]` using a loop.
7. What happens if you print `[1, 2, 3][5]`? Why?

<details>
<summary>Click to see the answers</summary>

```swift
// 1
let foods = ["dosa", "pizza", "biryani", "pasta", "idli"]
print(foods[0])   // dosa
print(foods[2])   // biryani

// 2
print(foods.count)   // 5

// 3
var numbers: [Int] = []
numbers.append(10)
numbers.append(20)
numbers.append(30)
print(numbers)

// 4
var animals = ["cat", "dog", "cow"]
animals[1] = "lion"
animals.remove(at: 0)
print(animals)   // ["lion", "cow"]

// 5
for n in [3, 6, 9, 12] {
    print(n * 2)
}

// 6
var sum = 0
for n in [4, 8, 15, 16, 23, 42] {
    sum += n
}
print(sum)   // 108
```

7. The program crashes with `Index out of range`. The array has only indexes 0, 1, 2.

</details>

---

## 🧠 Remember

- An array is an **ordered list** of the **same type**: `[1, 2, 3]`.
- Index starts at **0**. The last index is `count - 1`.
- `.append()` adds, `.remove(at:)` removes, `array[i] = x` changes.
- To change an array, it must be `var`.
- `for item in array { }` goes through every item.

---

⬅️ **Back:** [Chapter 13 — `while` Loops](13-while-loops.md)
➡️ **Next:** [Chapter 15 — Labels and Values: Dictionaries](15-dictionaries.md)
