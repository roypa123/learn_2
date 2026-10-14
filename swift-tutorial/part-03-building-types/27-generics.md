# Chapter 27 — Generics (Simple Introduction)

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What **generics** are and why they're useful.
- Writing a generic function with `<T>`.
- Generic types (your own generic struct).
- Constraints: `<T: Comparable>`.
- How you've **already** been using generics!

---

## 1. The problem: copy-paste code

Let's write a function that prints an array of `Int`s with a title:

```swift
func printInts(_ items: [Int]) {
    for item in items {
        print("- \(item)")
    }
}
```

Now we need the same for `String`s:

```swift
func printStrings(_ items: [String]) {
    for item in items {
        print("- \(item)")
    }
}
```

And for `Double`s… 😩 The code is **exactly the same**. Only the **type** changes!

---

## 2. The solution: generics

> 📖 **New word: Generic**
> Code that works with **any type**. You write it once, and it works for `Int`, `String`, `Double`, your own structs…

```swift
func printList<T>(_ items: [T]) {
    for item in items {
        print("- \(item)")
    }
}

printList([1, 2, 3])
printList(["apple", "banana"])
printList([true, false])
```

**Output:**

```
- 1
- 2
- 3
- apple
- banana
- true
- false
```

| Part | Meaning |
|---|---|
| `<T>` | "This function has a **placeholder type** called `T`." |
| `_ items: [T]` | "An array of `T` — whatever `T` turns out to be." |
| `printList([1, 2, 3])` | Swift sees `Int`s, so `T` becomes `Int`. |
| `printList(["apple", ...])` | Here `T` becomes `String`. |

> 📖 **New word: Type parameter**
> A placeholder for a type, like `T`. It's filled in when you use the function.

Think of a **cookie cutter** 🍪: the shape is the same, but you can use it with chocolate dough, vanilla dough, or ginger dough.

💡 **Tip:** `T` is just a name (short for "Type"). You could write `<Item>` or `<Element>`. Short names like `T` are common, but clear names are fine too!

---

## 3. Generic function that returns a value

```swift
func firstItem<T>(of items: [T]) -> T? {
    items.first
}

let n = firstItem(of: [10, 20, 30])
let s = firstItem(of: ["x", "y"])

print(n ?? 0)
print(s ?? "none")
```

**Output:**

```
10
x
```

| Part | Meaning |
|---|---|
| `-> T?` | Returns an Optional of the **same** type `T`. |
| `n` | Swift knows it's `Int?`. |
| `s` | Swift knows it's `String?`. |

---

## 4. Two values of the same type

```swift
func makePair<T>(_ a: T, _ b: T) -> [T] {
    [a, b]
}

print(makePair(1, 2))
print(makePair("hi", "bye"))
// print(makePair(1, "hi"))   // ❌ ERROR — both must be the SAME type T
```

**Output:**

```
[1, 2]
["hi", "bye"]
```

### Two different types

Use two placeholders:

```swift
func describePair<A, B>(_ a: A, _ b: B) {
    print("First: \(a), Second: \(b)")
}

describePair(1, "one")
describePair("pi", 3.14)
```

**Output:**

```
First: 1, Second: one
First: pi, Second: 3.14
```

---

## 5. Constraints: "any type that can…"

What if we want to find the **biggest** item?

```swift
func biggest<T>(_ items: [T]) -> T? {
    var best = items.first
    for item in items {
        if item > best! { best = item }   // ❌ ERROR
    }
    return best
}
```

**Error:**

```
error: binary operator '>' cannot be applied to two 'T' operands
```

Swift says: *"`T` could be **anything**. Not everything can be compared with `>`!"*

Fix: add a **constraint**:

```swift
func biggest<T: Comparable>(_ items: [T]) -> T? {
    guard var best = items.first else { return nil }
    for item in items {
        if item > best {
            best = item
        }
    }
    return best
}

print(biggest([3, 9, 2]) ?? 0)
print(biggest(["cat", "zebra", "ant"]) ?? "")
```

**Output:**

```
9
zebra
```

| Part | Meaning |
|---|---|
| `<T: Comparable>` | "`T` can be any type — **but** it must follow `Comparable`." |
| `item > best` | Now allowed, because `Comparable` types support `>`. |
| `guard var best = items.first else { return nil }` | If the array is empty, return `nil`. Otherwise, start with the first item. |

> 📖 **New word: Constraint**
> A rule for a type parameter: "`T` must follow this protocol."

Common constraints:

| Constraint | Allows |
|---|---|
| `T: Equatable` | `==`, `!=` |
| `T: Comparable` | `<`, `>`, sorting |
| `T: Hashable` | putting in a `Set`, dictionary keys |
| `T: Numeric` | `+`, `-`, `*` |
| `T: YourProtocol` | anything your protocol requires |

### Example: adding numbers of any number type

```swift
func sum<T: Numeric>(_ numbers: [T]) -> T {
    var total: T = 0
    for n in numbers {
        total += n
    }
    return total
}

print(sum([1, 2, 3]))
print(sum([1.5, 2.5]))
```

**Output:**

```
6
4.0
```

---

## 6. Generic types: your own generic struct

Let's make a **Box** that can hold any one type:

```swift
struct Box<T> {
    var item: T

    func show() {
        print("📦 The box contains: \(item)")
    }
}

let numberBox = Box(item: 42)
let textBox = Box(item: "Hello")
let boolBox = Box<Bool>(item: true)

numberBox.show()
textBox.show()
boolBox.show()
```

**Output:**

```
📦 The box contains: 42
📦 The box contains: Hello
📦 The box contains: true
```

| Part | Meaning |
|---|---|
| `struct Box<T>` | A generic struct. `T` is the type of the item inside. |
| `var item: T` | The item has type `T`. |
| `Box(item: 42)` | Swift figures out `T` = `Int`. |
| `Box<Bool>(item: true)` | You can also write the type yourself in `< >`. |

### A generic Stack 📚

A **stack** is like a pile of plates: you add to the top and take from the top.

```swift
struct Stack<Element> {
    private var items: [Element] = []

    mutating func push(_ item: Element) {
        items.append(item)
    }

    mutating func pop() -> Element? {
        items.popLast()
    }

    var top: Element? {
        items.last
    }

    var isEmpty: Bool {
        items.isEmpty
    }
}

var plates = Stack<String>()
plates.push("🍽️ Plate 1")
plates.push("🍽️ Plate 2")
plates.push("🍽️ Plate 3")

print("Top:", plates.top ?? "none")
print("Took:", plates.pop() ?? "none")
print("Took:", plates.pop() ?? "none")
print("Top now:", plates.top ?? "none")
```

**Output:**

```
Top: 🍽️ Plate 3
Took: 🍽️ Plate 3
Took: 🍽️ Plate 2
Top now: 🍽️ Plate 1
```

| Part | Meaning |
|---|---|
| `struct Stack<Element>` | Works for any type of element. |
| `private var items` | `private` = only code **inside** `Stack` can use it. Outside code must use `push`/`pop`. |
| `items.popLast()` | Remove and return the last item (Optional — the array might be empty). |
| `Stack<String>()` | A stack of strings. |

> 📖 **New word: private**
> Hides a property or method so only code inside the type can use it. It protects data from mistakes.

---

## 7. You've already used generics! 😮

| You wrote | It's really |
|---|---|
| `[Int]` | `Array<Int>` |
| `[String: Int]` | `Dictionary<String, Int>` |
| `Set<String>` | `Set<String>` |
| `Int?` | `Optional<Int>` |

`Array`, `Dictionary`, `Set` and `Optional` are all **generic types** made by Apple!

```swift
let a: Array<Int> = [1, 2, 3]       // same as [Int]
let o: Optional<String> = "hi"      // same as String?
print(a, o ?? "")
```

And functions like `map`, `filter`, `max` are **generic functions**. That's why they work with any type.

---

## 8. Mini project: a generic "find" function 🔍

```swift
func findIndex<T: Equatable>(of target: T, in items: [T]) -> Int? {
    for (index, item) in items.enumerated() {
        if item == target {
            return index
        }
    }
    return nil
}

struct Color: Equatable {
    var name: String
}

let numbers = [5, 8, 13, 21]
let fruits = ["apple", "mango", "kiwi"]
let colors = [Color(name: "red"), Color(name: "blue")]

if let i = findIndex(of: 13, in: numbers) {
    print("13 is at index \(i)")
}
if let i = findIndex(of: "kiwi", in: fruits) {
    print("kiwi is at index \(i)")
}
if let i = findIndex(of: Color(name: "blue"), in: colors) {
    print("blue is at index \(i)")
}
if findIndex(of: "grape", in: fruits) == nil {
    print("grape not found")
}
```

**Output:**

```
13 is at index 2
kiwi is at index 2
blue is at index 1
grape not found
```

**One** function works for `Int`, `String`, **and** our own `Color` struct — because they're all `Equatable`. ✨

---

## 🏋️ Practice

1. Write `func repeatItem<T>(_ item: T, times: Int) -> [T]` that returns an array with `item` repeated. Test with `5` and `"hi"`.
2. Write `func smallest<T: Comparable>(_ a: T, _ b: T) -> T`. Test with numbers and strings.
3. Make `struct Pair<T>` with `first: T` and `second: T`, and a method `swapped() -> Pair<T>`.
4. Make a generic `struct Queue<Element>` (first in, first out — like a line at a shop 🧍🧍🧍) with `enqueue(_:)` to add at the end and `dequeue() -> Element?` to remove from the front. (Hint: `items.isEmpty ? nil : items.removeFirst()`)

<details>
<summary>Click to see the answers</summary>

```swift
// 1
func repeatItem<T>(_ item: T, times: Int) -> [T] {
    Array(repeating: item, count: times)
}
print(repeatItem(5, times: 3))       // [5, 5, 5]
print(repeatItem("hi", times: 2))    // ["hi", "hi"]

// 2
func smallest<T: Comparable>(_ a: T, _ b: T) -> T {
    a < b ? a : b
}
print(smallest(4, 9))           // 4
print(smallest("pear", "fig"))  // fig

// 3
struct Pair<T> {
    var first: T
    var second: T
    func swapped() -> Pair<T> {
        Pair(first: second, second: first)
    }
}
let p = Pair(first: "left", second: "right").swapped()
print(p.first, p.second)   // right left

// 4
struct Queue<Element> {
    private var items: [Element] = []
    mutating func enqueue(_ item: Element) {
        items.append(item)
    }
    mutating func dequeue() -> Element? {
        items.isEmpty ? nil : items.removeFirst()
    }
}
var line = Queue<String>()
line.enqueue("Ravi")
line.enqueue("Meena")
print(line.dequeue() ?? "")   // Ravi
print(line.dequeue() ?? "")   // Meena
print(line.dequeue() ?? "empty")   // empty
```

</details>

---

## 🧠 Remember

- **Generics** let you write code once for **any type**.
- Generic function: `func name<T>(_ x: T) -> T`.
- Generic type: `struct Box<T> { var item: T }`.
- **Constraints** limit `T`: `<T: Comparable>`, `<T: Equatable>`.
- `Array`, `Dictionary`, `Set`, `Optional` are all generics.
- `private` hides things inside a type.

---

⬅️ **Back:** [Chapter 26 — Error Handling](26-error-handling.md)
➡️ **Next:** [Chapter 28 — `async` and `await`](28-async-await.md)
