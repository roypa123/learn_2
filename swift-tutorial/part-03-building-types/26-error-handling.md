# Chapter 26 — Error Handling (`throws`, `try`, `catch`)

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will learn

- What an **error** is (in running code, not typing mistakes).
- Making your own error types.
- `throw` — saying "something went wrong".
- `throws` — marking a function that can fail.
- `do`, `try`, `catch` — handling errors.
- `try?` and `try!`.
- `defer`.

---

## 1. Two kinds of "errors"

| Kind | When | Example |
|---|---|---|
| **Compile error** | When you write code. Swift won't run it. | Typo: `pirnt("hi")` |
| **Runtime error** | While the program runs. Something goes wrong. | No internet, wrong password, file not found |

This chapter is about the **second** kind: problems that happen while the app runs.

Optionals (Chapter 17) say: "maybe there's no value."
Errors say: "something went wrong — and **here's why**."

---

## 2. Real-life example 🏧

You go to an ATM to take out money. Many things can go wrong:

- Wrong PIN ❌
- Not enough money in your account ❌
- ATM is out of cash ❌

The ATM doesn't just say "No." It tells you **what** went wrong. That's what Swift errors do.

---

## 3. Making an error type

```swift
enum ATMError: Error {
    case wrongPIN
    case notEnoughMoney
    case machineEmpty
}
```

| Part | Meaning |
|---|---|
| `enum ATMError` | An enum with possible problems. |
| `: Error` | Follows the `Error` protocol. This makes it an error type. |
| `case wrongPIN` | One kind of problem. |

💡 **Tip:** Enums are perfect for errors: a fixed list of things that can go wrong.

---

## 4. `throws` and `throw`

```swift
enum ATMError: Error {
    case wrongPIN
    case notEnoughMoney
}

func withdraw(amount: Int, pin: Int, balance: Int) throws -> Int {
    if pin != 1234 {
        throw ATMError.wrongPIN
    }
    if amount > balance {
        throw ATMError.notEnoughMoney
    }
    return balance - amount
}
```

| Part | Meaning |
|---|---|
| `throws` | Written **before** `->`. "This function **might fail**." |
| `throw ATMError.wrongPIN` | "Stop! Something went wrong: wrong PIN." The function ends immediately. |
| `return balance - amount` | If nothing went wrong, give back the new balance. |

> 📖 **New word: throw**
> To **report** an error. Like throwing a red flag 🚩 in a game.

> 📖 **New word: throws**
> A label on a function that says: "I might throw an error."

---

## 5. Calling a throwing function: `do`, `try`, `catch`

```swift
do {
    let newBalance = try withdraw(amount: 500, pin: 1234, balance: 2000)
    print("Success! New balance: \(newBalance)")
} catch {
    print("Something went wrong: \(error)")
}
```

**Output:**

```
Success! New balance: 1500
```

| Part | Meaning |
|---|---|
| `do { ... }` | "Try to do this…" |
| `try` | Must be written before any call that can throw. "I know this might fail." |
| `catch { ... }` | "…and if an error is thrown, run this instead." |
| `error` | Inside `catch`, Swift gives you the error automatically in a constant called `error`. |

Now with a wrong PIN:

```swift
do {
    let newBalance = try withdraw(amount: 500, pin: 9999, balance: 2000)
    print("Success! New balance: \(newBalance)")
} catch {
    print("Something went wrong: \(error)")
}
```

**Output:**

```
Something went wrong: wrongPIN
```

The `print("Success!...")` line was **skipped**. As soon as `withdraw` threw, Swift jumped to `catch`.

```
 do {
    try withdraw(...)  ──── error! ────┐
    print("Success")   ← skipped       │
 } catch {                             │
    print("wrong...")  ◄───────────────┘
 }
```

⚠️ **Careful:** If you forget `try`:

```swift
let b = withdraw(amount: 1, pin: 1234, balance: 5)
// ❌ ERROR: call can throw but is not marked with 'try'
```

---

## 6. Catching specific errors

You can handle each error **differently**:

```swift
func tryWithdraw(_ amount: Int, pin: Int) {
    do {
        let left = try withdraw(amount: amount, pin: pin, balance: 1000)
        print("✅ Take your cash. Balance left: \(left)")
    } catch ATMError.wrongPIN {
        print("❌ Wrong PIN. Please try again.")
    } catch ATMError.notEnoughMoney {
        print("❌ Not enough money in your account.")
    } catch {
        print("❌ Unknown error: \(error)")
    }
}

tryWithdraw(200, pin: 1234)
tryWithdraw(200, pin: 1111)
tryWithdraw(5000, pin: 1234)
```

**Output:**

```
✅ Take your cash. Balance left: 800
❌ Wrong PIN. Please try again.
❌ Not enough money in your account.
```

| Part | Meaning |
|---|---|
| `catch ATMError.wrongPIN` | Only catches this one error. |
| `catch ATMError.notEnoughMoney` | Only catches this one. |
| last `catch` | Catches **anything else**. Swift needs it to be sure every error is handled. |

---

## 7. Errors with extra information

Use **associated values** (Chapter 23) to give more details:

```swift
enum ShopError: Error {
    case outOfStock(item: String)
    case notEnoughMoney(needed: Double)
}

func buy(_ item: String, money: Double) throws {
    let prices = ["pen": 10.0, "book": 150.0]
    let stock = ["pen": 5, "book": 0]

    guard let price = prices[item] else {
        throw ShopError.outOfStock(item: item)
    }
    if stock[item, default: 0] == 0 {
        throw ShopError.outOfStock(item: item)
    }
    if money < price {
        throw ShopError.notEnoughMoney(needed: price - money)
    }
    print("You bought a \(item)! 🛍️")
}

for (item, money) in [("pen", 20.0), ("book", 500.0), ("pen", 3.0)] {
    do {
        try buy(item, money: money)
    } catch ShopError.outOfStock(let item) {
        print("Sorry, \(item) is out of stock.")
    } catch ShopError.notEnoughMoney(let needed) {
        print("You need \(needed) more.")
    } catch {
        print("Error: \(error)")
    }
}
```

**Output:**

```
You bought a pen! 🛍️
Sorry, book is out of stock.
You need 7.0 more.
```

---

## 8. `try?` — turn an error into `nil`

If you don't care **why** it failed, use `try?`. The result becomes an **Optional**.

```swift
let result1 = try? withdraw(amount: 100, pin: 1234, balance: 500)
let result2 = try? withdraw(amount: 100, pin: 0000, balance: 500)

print(result1)
print(result2)
```

**Output:**

```
Optional(400)
nil
```

| Part | Meaning |
|---|---|
| `try?` | "Try it. If it fails, just give me `nil`." |

Combine with `if let` or `??`:

```swift
let balance = (try? withdraw(amount: 100, pin: 0, balance: 500)) ?? 500
print(balance)   // 500
```

---

## 9. `try!` — "it will never fail" ⚠️

```swift
let sure = try! withdraw(amount: 100, pin: 1234, balance: 500)
print(sure)   // 400
```

If it **does** fail, the app **crashes** 💥 (just like `!` with Optionals).

🧠 **Remember:** Avoid `try!`. Use `do`/`catch` or `try?`.

| Way | If it fails | Use when |
|---|---|---|
| `do { try } catch { }` | You handle it | You want to know **why** and react. |
| `try?` | Gives `nil` | You don't care why. |
| `try!` | 💥 Crash | Almost never! |

---

## 10. Passing errors up

A throwing function can call another throwing function **without** catching. The error just goes **up** to whoever called it.

```swift
enum LoginError: Error {
    case emptyName
    case shortPassword
}

func checkName(_ name: String) throws {
    if name.isEmpty { throw LoginError.emptyName }
}

func checkPassword(_ password: String) throws {
    if password.count < 6 { throw LoginError.shortPassword }
}

func login(name: String, password: String) throws {
    try checkName(name)          // if this throws, login stops and passes it up
    try checkPassword(password)  // same here
    print("Welcome, \(name)! 🎉")
}

do {
    try login(name: "Meena", password: "abc")
} catch {
    print("Login failed: \(error)")
}
```

**Output:**

```
Login failed: shortPassword
```

| Part | Meaning |
|---|---|
| `func login(...) throws` | `login` can throw too. |
| `try checkName(name)` | No `do`/`catch` here — if it throws, the error goes **up** to the caller of `login`. |

Think of a hot potato 🥔🔥: each function can either **handle** it (catch) or **pass it up** (throws).

---

## 11. Nice error messages: `LocalizedError`

```swift
import Foundation

enum PasswordError: LocalizedError {
    case tooShort
    case noNumber

    var errorDescription: String? {
        switch self {
        case .tooShort: "Password must be at least 8 characters."
        case .noNumber: "Password must contain a number."
        }
    }
}

func validate(_ p: String) throws {
    if p.count < 8 { throw PasswordError.tooShort }
    if !p.contains(where: { $0.isNumber }) { throw PasswordError.noNumber }
}

do {
    try validate("helloworld")
} catch {
    print(error.localizedDescription)
}
```

**Output:**

```
Password must contain a number.
```

| Part | Meaning |
|---|---|
| `import Foundation` | `LocalizedError` lives in Foundation. |
| `LocalizedError` | A protocol for errors with human-friendly messages. |
| `errorDescription` | The message to show. |
| `error.localizedDescription` | Read that message. |

💡 **Look ahead:** In an app, you'll show `error.localizedDescription` in an alert to the user.

---

## 12. `defer` — always run this at the end

```swift
func doWork() {
    print("1. Start")
    defer {
        print("3. Clean up (always runs!)")
    }
    print("2. Working...")
}

doWork()
```

**Output:**

```
1. Start
2. Working...
3. Clean up (always runs!)
```

| Part | Meaning |
|---|---|
| `defer { ... }` | "Run this when the function ends — no matter how it ends." |

It runs even if the function **throws** or **returns early**. Useful for clean-up, like closing a file or hiding a loading spinner.

---

## 13. Mini project: a sign-up form checker 📝

```swift
enum SignUpError: Error, CustomStringConvertible {
    case nameTooShort
    case invalidEmail(String)
    case tooYoung(age: Int)

    var description: String {
        switch self {
        case .nameTooShort:
            "Name must be at least 2 letters."
        case .invalidEmail(let email):
            "'\(email)' is not a valid email."
        case .tooYoung(let age):
            "You are \(age). You must be 13 or older."
        }
    }
}

struct SignUpForm {
    var name: String
    var email: String
    var age: Int

    func validate() throws {
        if name.count < 2 { throw SignUpError.nameTooShort }
        if !email.contains("@") || !email.contains(".") {
            throw SignUpError.invalidEmail(email)
        }
        if age < 13 { throw SignUpError.tooYoung(age: age) }
    }
}

let forms = [
    SignUpForm(name: "Ravi", email: "ravi@mail.com", age: 15),
    SignUpForm(name: "A", email: "a@mail.com", age: 20),
    SignUpForm(name: "Meena", email: "meena-mail", age: 14),
    SignUpForm(name: "Arun", email: "arun@mail.com", age: 9)
]

for form in forms {
    do {
        try form.validate()
        print("✅ \(form.name) signed up!")
    } catch {
        print("❌ \(form.name): \(error)")
    }
}
```

**Output:**

```
✅ Ravi signed up!
❌ A: Name must be at least 2 letters.
❌ Meena: 'meena-mail' is not a valid email.
❌ Arun: You are 9. You must be 13 or older.
```

---

## 🏋️ Practice

1. Make `enum DivisionError: Error { case divideByZero }`. Write `func divide(_ a: Int, _ b: Int) throws -> Int` that throws if `b` is 0.
2. Call `divide(10, 2)` and `divide(10, 0)` with `do`/`catch`. Print the result or an error message.
3. Call `divide(8, 0)` with `try?` and `?? 0`. Print the result.
4. Make `enum AgeError: Error { case negative, tooOld }`. Write `func setAge(_ age: Int) throws` that throws `negative` if age < 0 and `tooOld` if age > 150. Catch each error separately.
5. Write a function with `defer` and an early `return`. Check that `defer` still runs.

<details>
<summary>Click to see the answers</summary>

```swift
// 1 & 2
enum DivisionError: Error {
    case divideByZero
}

func divide(_ a: Int, _ b: Int) throws -> Int {
    if b == 0 { throw DivisionError.divideByZero }
    return a / b
}

do {
    print(try divide(10, 2))   // 5
    print(try divide(10, 0))   // throws — this line doesn't print
} catch {
    print("Error: \(error)")   // Error: divideByZero
}

// 3
let r = (try? divide(8, 0)) ?? 0
print(r)   // 0

// 4
enum AgeError: Error { case negative, tooOld }

func setAge(_ age: Int) throws {
    if age < 0 { throw AgeError.negative }
    if age > 150 { throw AgeError.tooOld }
    print("Age set to \(age)")
}

for a in [25, -3, 200] {
    do {
        try setAge(a)
    } catch AgeError.negative {
        print("Age can't be negative")
    } catch AgeError.tooOld {
        print("That's too old!")
    } catch {
        print("Other error")
    }
}

// 5
func check(_ n: Int) {
    defer { print("defer ran for \(n)") }
    if n < 0 {
        print("negative, leaving early")
        return
    }
    print("positive")
}
check(-1)
check(5)
```

</details>

---

## 🧠 Remember

- Make error types with `enum MyError: Error { case ... }`.
- `func f() throws` marks a function that can fail. `throw MyError.x` reports a problem.
- Call it with `try` inside `do { } catch { }`.
- `catch MyError.x` handles one error. A plain `catch` handles the rest (`error` holds it).
- `try?` → Optional (`nil` on error). `try!` → crash on error (avoid).
- `defer { }` always runs when the function ends.

---

⬅️ **Back:** [Chapter 25 — Extensions](25-extensions.md)
➡️ **Next:** [Chapter 27 — Generics](27-generics.md)
