# Chapter 18 — Functions: Reusable Blocks of Code

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What a **function** is and why we need it.
- Making and calling functions.
- Giving functions inputs (**parameters**).
- Getting outputs back (**return**).
- Argument labels, `_`, and default values.
- Returning many values at once.

---

## 1. Why functions?

Imagine you make tea ☕ every morning:

1. Boil water.
2. Add tea leaves.
3. Add milk.
4. Add sugar.

Instead of saying all 4 steps every time, you just say **"make tea"**.

A **function** is like that: a group of steps with a **name**. You write the steps **once**, then use the name **many times**.

> 📖 **New word: Function**
> A named block of code that does one job. You can use it again and again.

You already used functions: `print()`, `type(of:)`, `max()`!

---

## 2. Making your first function

```swift
func sayHello() {
    print("Hello!")
    print("Nice to meet you.")
}
```

**Output:**

*(nothing!)*

Why nothing? We only **made** (defined) the function. We didn't **use** (call) it yet.

| Part | Meaning |
|---|---|
| `func` | "I'm making a function." |
| `sayHello` | The function's name. Use camelCase. Usually a **verb** (action word). |
| `()` | Brackets for inputs. Empty here = no inputs. |
| `{` | Start of the function's code. |
| `print(...)` lines | The steps. |
| `}` | End. |

> 📖 **New word: Define**
> To **make** a function (write its steps).

---

## 3. Calling a function

```swift
func sayHello() {
    print("Hello!")
    print("Nice to meet you.")
}

sayHello()
sayHello()
```

**Output:**

```
Hello!
Nice to meet you.
Hello!
Nice to meet you.
```

| Part | Meaning |
|---|---|
| `sayHello()` | "Run the steps inside `sayHello` now." |

We called it **twice**, so the steps ran twice.

> 📖 **New word: Call**
> To **use** a function: write its name with `()`.

---

## 4. Parameters: giving input

What if we want to greet **different** people?

```swift
func greet(name: String) {
    print("Hello, \(name)!")
}

greet(name: "Ravi")
greet(name: "Meena")
```

**Output:**

```
Hello, Ravi!
Hello, Meena!
```

| Part | Meaning |
|---|---|
| `greet` | Function name. |
| `(name: String)` | One input. Its name is `name`, its type is `String`. |
| `\(name)` | Use the input inside the function. |
| `greet(name: "Ravi")` | Call it. Give `"Ravi"` as the `name`. |

> 📖 **New word: Parameter**
> An input **box** in the function definition: `name: String`.

> 📖 **New word: Argument**
> The actual **value** you give when calling: `"Ravi"`.

Think of a juice machine 🧃:
- **Parameter** = the slot that says "put fruit here".
- **Argument** = the actual mango you put in.

---

## 5. Many parameters

```swift
func introduce(name: String, age: Int) {
    print("I am \(name) and I am \(age) years old.")
}

introduce(name: "Arun", age: 14)
```

**Output:**

```
I am Arun and I am 14 years old.
```

| Part | Meaning |
|---|---|
| `name: String, age: Int` | Two parameters, separated by a comma. |
| `introduce(name: "Arun", age: 14)` | Give both, in the **same order**. |

⚠️ **Careful:** You must give the arguments in the **same order** and with the **labels**.

```swift
introduce(age: 14, name: "Arun")   // ❌ ERROR: wrong order
introduce("Arun", 14)              // ❌ ERROR: missing labels
```

---

## 6. Return: getting output back

So far, our functions only **print**. But often we want the function to **give back** an answer.

```swift
func square(number: Int) -> Int {
    return number * number
}

let result = square(number: 5)
print(result)
```

**Output:**

```
25
```

| Part | Meaning |
|---|---|
| `-> Int` | "This function **gives back** an `Int`." The arrow `->` is a minus and a greater-than. |
| `return number * number` | Calculate 5 × 5 = 25 and **give it back**. |
| `let result = square(number: 5)` | Call it. The answer (25) goes into `result`. |

> 📖 **New word: Return value**
> The answer a function **gives back** to whoever called it.

Think of a calculator 🧮: you press `5 x 5`, it **gives back** `25`. You can then use that `25` for something else.

### Print vs return

```swift
func printDouble(n: Int) {
    print(n * 2)          // just shows it
}

func double(n: Int) -> Int {
    return n * 2          // gives it back
}

printDouble(n: 4)                    // shows 8
let x = double(n: 4)                 // x is 8, nothing shown
print(double(n: 4) + double(n: 1))   // 8 + 2 = 10
```

**Output:**

```
8
10
```

| | `print` inside | `return` |
|---|---|---|
| Shows on screen? | Yes | No |
| Can you use the answer later? | No | Yes ✅ |

🧠 **Remember:** `return` is more useful. It lets you **use** the answer.

---

## 7. `return` ends the function

When Swift reaches `return`, it **leaves** the function immediately.

```swift
func checkAge(age: Int) -> String {
    if age < 0 {
        return "Invalid age"
    }
    if age >= 18 {
        return "Adult"
    }
    return "Child"
}

print(checkAge(age: -5))
print(checkAge(age: 30))
print(checkAge(age: 8))
```

**Output:**

```
Invalid age
Adult
Child
```

| Call | What happens |
|---|---|
| `checkAge(age: -5)` | `-5 < 0` → return `"Invalid age"`. Stop. |
| `checkAge(age: 30)` | Not < 0. `30 >= 18` → return `"Adult"`. Stop. |
| `checkAge(age: 8)` | Not < 0. Not >= 18. Reach the last line → return `"Child"`. |

### Short form: one line, no `return`

If the function has **only one expression**, you can leave out `return`:

```swift
func square(number: Int) -> Int {
    number * number
}
```

---

## 8. Argument labels

Sometimes the **outside** name and the **inside** name should be different, to read nicely.

```swift
func sayHi(to person: String) {
    print("Hi, \(person)!")
}

sayHi(to: "Priya")
```

**Output:**

```
Hi, Priya!
```

| Part | Meaning |
|---|---|
| `to` | **Argument label** — used when **calling**: `sayHi(to: ...)`. |
| `person` | **Parameter name** — used **inside** the function. |

Read it out loud: *"say hi to Priya"*. Sounds like English! 😊

### No label at all: `_`

```swift
func double(_ n: Int) -> Int {
    return n * 2
}

print(double(7))
```

**Output:**

```
14
```

| Part | Meaning |
|---|---|
| `_` | "No label when calling." |
| `double(7)` | Clean and short. |

This is why `print("Hi")` has no label — it uses `_`!

---

## 9. Default values

You can give a parameter a **default** value. Then the caller can skip it.

```swift
func orderCoffee(size: String = "medium", sugar: Int = 1) {
    print("One \(size) coffee with \(sugar) sugar.")
}

orderCoffee()
orderCoffee(size: "large")
orderCoffee(size: "small", sugar: 0)
```

**Output:**

```
One medium coffee with 1 sugar.
One large coffee with 1 sugar.
One small coffee with 0 sugar.
```

| Part | Meaning |
|---|---|
| `size: String = "medium"` | If nobody gives a size, use `"medium"`. |
| `orderCoffee()` | Uses both defaults. |
| `orderCoffee(size: "large")` | Gives size, uses default sugar. |

---

## 10. Returning many values: tuples

A function can give back **more than one** value using a **tuple**.

> 📖 **New word: Tuple**
> A small group of values in brackets, like `(3, "hello")`.

```swift
func minAndMax(numbers: [Int]) -> (smallest: Int, largest: Int) {
    var smallest = numbers[0]
    var largest = numbers[0]

    for n in numbers {
        if n < smallest { smallest = n }
        if n > largest { largest = n }
    }

    return (smallest, largest)
}

let result = minAndMax(numbers: [4, 9, 1, 7])
print("Smallest: \(result.smallest)")
print("Largest: \(result.largest)")
```

**Output:**

```
Smallest: 1
Largest: 9
```

| Part | Meaning |
|---|---|
| `-> (smallest: Int, largest: Int)` | Gives back two named `Int`s. |
| `return (smallest, largest)` | Give both back together. |
| `result.smallest` | Get one value from the tuple by name. |

⚠️ **Careful:** This function crashes if the array is empty (`numbers[0]` doesn't exist). A better version would return an Optional. Can you think how?

---

## 11. Functions calling functions

```swift
func square(_ n: Int) -> Int {
    n * n
}

func sumOfSquares(_ a: Int, _ b: Int) -> Int {
    square(a) + square(b)
}

print(sumOfSquares(3, 4))
```

**Output:**

```
25
```

`sumOfSquares` uses `square`: 3² + 4² = 9 + 16 = 25.

💡 **Tip:** Good functions are **small** and do **one** job. Then you combine them like LEGO bricks 🧱.

---

## 12. Variables inside functions (scope)

```swift
func makeGreeting() {
    let message = "Hi!"
    print(message)
}

makeGreeting()
print(message)   // ❌ ERROR
```

**Error:**

```
error: cannot find 'message' in scope
```

> 📖 **New word: Scope**
> The area of code where a name can be used.

`message` was made **inside** the function. It only lives there. Outside, it doesn't exist.

Think of it like a secret inside a room 🚪 — people outside can't hear it.

---

## 13. Parameters are constants

```swift
func addOne(n: Int) {
    n += 1   // ❌ ERROR: left side of mutating operator isn't mutable: 'n' is a 'let' constant
}
```

Parameters are like `let` — you **can't** change them inside the function.
Make a new variable instead:

```swift
func addOne(n: Int) -> Int {
    var result = n
    result += 1
    return result
}
```

---

## 14. Mini project: a tip calculator 💰

```swift
func calculateTip(bill: Double, percent: Double = 10) -> Double {
    return bill * percent / 100
}

func printReceipt(bill: Double, percent: Double = 10) {
    let tip = calculateTip(bill: bill, percent: percent)
    let total = bill + tip
    print("Bill:  \(bill)")
    print("Tip:   \(tip)  (\(percent)%)")
    print("Total: \(total)")
    print("----------")
}

printReceipt(bill: 500)
printReceipt(bill: 1200, percent: 15)
```

**Output:**

```
Bill:  500.0
Tip:   50.0  (10.0%)
Total: 550.0
----------
Bill:  1200.0
Tip:   180.0  (15.0%)
Total: 1380.0
----------
```

| Part | Meaning |
|---|---|
| `calculateTip` | Does **one** job: calculate the tip. Returns a `Double`. |
| `percent: Double = 10` | Default tip is 10%. |
| `printReceipt` | Uses `calculateTip`, then prints everything. |
| `printReceipt(bill: 500)` | Uses the default 10%. |

---

## 🏋️ Practice

1. Write `func sayGoodbye()` that prints `"Goodbye!"`. Call it 3 times.
2. Write `func greet(name: String, times: Int)` that prints `"Hi, NAME!"` `times` times. (Hint: a loop inside!)
3. Write `func add(_ a: Int, _ b: Int) -> Int`. Print `add(3, 4)`.
4. Write `func isEven(_ n: Int) -> Bool`. Print `isEven(10)` and `isEven(7)`.
5. Write `func area(width: Double, height: Double = 1.0) -> Double`. Call it with and without `height`.
6. Write `func average(_ numbers: [Double]) -> Double` that returns the average. If the array is empty, return `0`.

<details>
<summary>Click to see the answers</summary>

```swift
// 1
func sayGoodbye() {
    print("Goodbye!")
}
sayGoodbye()
sayGoodbye()
sayGoodbye()

// 2
func greet(name: String, times: Int) {
    for _ in 1...times {
        print("Hi, \(name)!")
    }
}
greet(name: "Meena", times: 3)

// 3
func add(_ a: Int, _ b: Int) -> Int {
    a + b
}
print(add(3, 4))   // 7

// 4
func isEven(_ n: Int) -> Bool {
    n % 2 == 0
}
print(isEven(10))  // true
print(isEven(7))   // false

// 5
func area(width: Double, height: Double = 1.0) -> Double {
    width * height
}
print(area(width: 5))              // 5.0
print(area(width: 5, height: 3))   // 15.0

// 6
func average(_ numbers: [Double]) -> Double {
    if numbers.isEmpty {
        return 0
    }
    var total = 0.0
    for n in numbers {
        total += n
    }
    return total / Double(numbers.count)
}
print(average([2, 4, 6]))   // 4.0
print(average([]))          // 0.0
```

</details>

---

## 🧠 Remember

- `func name() { }` **defines** a function. `name()` **calls** it.
- Parameters are inputs: `func greet(name: String)`.
- `-> Type` and `return` give back an answer.
- `return` ends the function right away.
- Argument labels: `func sayHi(to person: String)` → `sayHi(to: "X")`.
- `_` means no label: `func double(_ n: Int)` → `double(5)`.
- Default values: `size: String = "medium"`.
- Variables inside a function only live inside it (scope).

---

⬅️ **Back:** [Chapter 17 — Optionals](17-optionals.md)
➡️ **Next:** [Chapter 19 — Closures](19-closures.md)
