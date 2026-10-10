# Chapter 33 – Errors and Exceptions (`try` and `catch`)

[⬅ Previous chapter](32-sets.md) | [Table of Contents](../README.md) | [Next chapter ➡](34-generics.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What an **exception** is
- How to **read a stack trace** (the red error text) 🔍
- How to **catch** exceptions with **`try` / `catch`**
- What **`finally`** and **try-with-resources** do
- How to **throw** your own exceptions with **`throw`**
- **Checked** vs. **unchecked** exceptions, and the word **`throws`**
- How to make your **own exception classes**
- **Good habits** for handling errors
- How Spring Boot turns exceptions into **web error messages** 🌱

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Exception** | A **problem** that happens while the program runs. It stops the normal flow. |
| **Throw** | **Create** and **send** an exception: "Something is wrong! 🚨" |
| **Catch** | **Receive** an exception and **handle** it, so the program doesn't crash. |
| **Stack trace** | The red text that shows **where** the exception happened, and the path the program took to get there. |
| **Checked exception** | An exception Java **forces** you to handle (or declare). |
| **Unchecked exception** | An exception Java does **not** force you to handle. Usually a **bug**. |
| **`throws`** | A word in a method's header that **warns**: "This method might throw this exception." |
| **Resource** | Something that must be **closed** after use: a file, a Scanner, a database connection. |

---

## 📖 Story: The fire alarm 🚨

You're in a school. Suddenly — **fire!** 🔥

1. Someone **pulls the fire alarm**. 🚨 → **throw** an exception
2. Everyone **stops** what they're doing. Lessons are not finished. → normal flow **stops**
3. The alarm goes up to the **fire department**. → the exception goes **up** to whoever can handle it
4. The firefighters **handle** it. 🧑‍🚒 → **catch**
5. If **nobody** handles it... the building burns down. 🔥🏚️ → the program **crashes**

And **no matter what** happens, at the end, someone **locks the doors**. 🔒 → **finally**

---

## 💥 Part 1: You've already seen exceptions!

In earlier chapters, you saw many of these:

| Exception | When | Chapter |
|---|---|---|
| `ArithmeticException` | divide by zero | 8 |
| `StringIndexOutOfBoundsException` | `"hi".charAt(5)` | 9 |
| `NumberFormatException` | `Integer.parseInt("hello")` | 7 |
| `ArrayIndexOutOfBoundsException` | `arr[10]` on a small array | 14 |
| `InputMismatchException` | `scanner.nextInt()` but the user typed text | 16 |
| `NullPointerException` | calling a method on `null` | 18 |
| `ClassCastException` | wrong downcast | 23 |
| `IllegalArgumentException` | a bad value (we threw it in records!) | 29 |
| `ConcurrentModificationException` | remove in a for-each loop | 30 |
| `UnsupportedOperationException` | `List.of(...).add(...)` | 30 |

Every one of these is an **object** — an instance of a class that extends `Exception`. And every one, until now, **crashed** our program. 😢 Let's learn to handle them!

---

## 🔍 Part 2: Reading a stack trace

Here's a program with a bug:

```java
public class Crash {
    public static void main(String[] args) {
        System.out.println("Start");
        int result = calculate(10, 0);
        System.out.println("Result: " + result);
    }

    static int calculate(int a, int b) {
        return divide(a, b) * 2;
    }

    static int divide(int a, int b) {
        return a / b;
    }
}
```

**Output:**

```
Start
Exception in thread "main" java.lang.ArithmeticException: / by zero
	at Crash.divide(Crash.java:13)
	at Crash.calculate(Crash.java:9)
	at Crash.main(Crash.java:4)
```

😱 Scary? Let's read it slowly — it's actually **very helpful**!

| Line | Meaning |
|---|---|
| `Exception in thread "main"` | A problem happened in the main program. |
| `java.lang.ArithmeticException` | **What kind** of problem: a math problem. |
| `: / by zero` | The **message**: what exactly went wrong. |
| `at Crash.divide(Crash.java:13)` | 🎯 **Where** it happened: in the method `divide`, file `Crash.java`, **line 13**. |
| `at Crash.calculate(Crash.java:9)` | Who **called** `divide`: `calculate`, line 9. |
| `at Crash.main(Crash.java:4)` | Who called `calculate`: `main`, line 4. |

### 🥞 Read it like a stack of pancakes

The list is called a **stack trace** because it shows the "stack" of method calls — the **newest on top**:

```
   divide    (line 13)   ← 💥 the problem is HERE (top)
   calculate (line 9)    ← called divide
   main      (line 4)    ← called calculate (bottom, where it all started)
```

👉 **How to read any stack trace:**
1. Read the **first line**: **what** went wrong.
2. Look at the **first `at` line in YOUR code**: **where** it went wrong. (In IntelliJ, it's a **blue link** — click it to jump to the line! 🪄)
3. Go down the list to see **how** the program got there.

> 💡 In big Spring Boot programs, stack traces can be **100 lines long** — most of them are Spring's own code. Look for lines with **your** package name (`com.example...`). That's where your bug is! 🎯

Also notice: `Result:` was **never printed**. When an exception is thrown and not caught, the program **stops immediately**.

---

## 🛟 Part 3: `try` and `catch`

```java
public class SafeDivide {
    public static void main(String[] args) {
        System.out.println("Start");

        try {
            int result = 10 / 0;
            System.out.println("Result: " + result);
        } catch (ArithmeticException e) {
            System.out.println("⚠️ Oops: " + e.getMessage());
        }

        System.out.println("The program continues! 🎉");
    }
}
```

**Output:**

```
Start
⚠️ Oops: / by zero
The program continues! 🎉
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `try {` | "**Try** to run this code. It might fail." |
| `int result = 10 / 0;` | 💥 An exception is thrown here! |
| `System.out.println("Result: ...")` | **Skipped** — Java jumps straight to `catch`. |
| `} catch (ArithmeticException e) {` | "If an `ArithmeticException` happens, **catch** it, and call it `e`." |
| `e.getMessage()` | The exception's message: `"/ by zero"`. |
| After the `catch` block | The program **continues normally**. No crash! 🛟 |

### 🗺️ The flow

```
 try {
     line 1   ✅
     line 2   💥 exception!  ──────┐
     line 3   (skipped)            │
 }                                 │
 catch (...) {   ◄─────────────────┘
     handle it 🛟
 }
 next line   ✅ continues
```

If **no** exception happens, the `catch` block is **skipped**.

### A real example: safe number input

```java
import java.util.Scanner;

public class AskAge {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.print("How old are you? ");
            String input = scanner.nextLine();
            try {
                int age = Integer.parseInt(input.strip());
                System.out.println("In 10 years you'll be " + (age + 10) + "!");
                break;
            } catch (NumberFormatException e) {
                System.out.println("❌ '" + input + "' is not a number. Try again.");
            }
        }
    }
}
```

**Example run:**

```
How old are you? twelve
❌ 'twelve' is not a number. Try again.
How old are you? 12
In 10 years you'll be 22!
```

👉 This is the `try/catch` way to do what we did with `hasNextInt()` in Chapter 16. It's very common!

### Useful methods on an exception

| Method | Gives |
|---|---|
| `e.getMessage()` | the message text: `"/ by zero"` |
| `e.getClass().getSimpleName()` | the exception type: `"ArithmeticException"` |
| `e.printStackTrace()` | prints the full stack trace (for debugging) |
| `e.toString()` | type + message |

---

## 🎣 Part 4: Catching different exceptions

### Many `catch` blocks

```java
String[] data = { "10", "abc", null };

for (int i = 0; i <= data.length; i++) {
    try {
        int n = Integer.parseInt(data[i].strip());
        System.out.println("Number: " + n);
    } catch (NumberFormatException e) {
        System.out.println("❌ Not a number: " + data[i]);
    } catch (NullPointerException e) {
        System.out.println("❌ Missing value at index " + i);
    } catch (ArrayIndexOutOfBoundsException e) {
        System.out.println("❌ No index " + i + " in the array");
    }
}
```

**Output:**

```
Number: 10
❌ Not a number: abc
❌ Missing value at index 2
❌ No index 3 in the array
```

Java checks the `catch` blocks **from top to bottom**, and uses the **first one that matches**.

### One `catch` for many types: `|`

```java
try {
    ...
} catch (NumberFormatException | NullPointerException e) {
    System.out.println("❌ Bad input");
}
```

### Catching the parent type

Exceptions form a **family tree** (inheritance — Chapter 22!):

```
                        Throwable
                       /         \
                  Error           Exception
          (very serious,         /          \
           don't catch!)   IOException   RuntimeException
           OutOfMemoryError  (checked)    (unchecked)
                                          /     |      \
                     ArithmeticException  NullPointer  IllegalArgumentException
                                          Exception          |
                                                     NumberFormatException
```

Because of **polymorphism** (Chapter 23), `catch (RuntimeException e)` catches **all** its children:

```java
try {
    ...
} catch (NumberFormatException e) {
    System.out.println("Not a number");          // specific first
} catch (RuntimeException e) {
    System.out.println("Something else went wrong: " + e.getMessage());   // general last
}
```

> ⚠️ Put **specific** exceptions **first**, general ones **last**. Otherwise the general one catches everything, and Java gives an error: `exception NumberFormatException has already been caught`.

> ⚠️ Don't catch `Exception` or `Throwable` everywhere "just to be safe". You'll hide real bugs! 🙈 (See Part 10.)

---

## 🔒 Part 5: `finally` — always runs

`finally` is a block that runs **no matter what**: exception or not, caught or not.

```java
public static void process(String text) {
    System.out.println("🔓 Open the door");
    try {
        int n = Integer.parseInt(text);
        System.out.println("Number: " + n);
    } catch (NumberFormatException e) {
        System.out.println("❌ Not a number");
    } finally {
        System.out.println("🔒 Lock the door");
    }
}
```

```java
process("42");
process("abc");
```

**Output:**

```
🔓 Open the door
Number: 42
🔒 Lock the door
🔓 Open the door
❌ Not a number
🔒 Lock the door
```

👉 Use `finally` for **cleanup**: closing files, releasing connections, stopping timers... Things that **must** happen. 🧹

Even a `return` inside `try` doesn't stop `finally`:

```java
static String test() {
    try {
        return "from try";
    } finally {
        System.out.println("finally still runs!");
    }
}
```

---

## 📂 Part 6: try-with-resources — automatic closing

Some objects must be **closed** after use (a `Scanner`, a file, a database connection). If you forget, or if an exception happens before `close()`, the resource stays open. 🚰💧 (Like leaving the tap running!)

The old way:

```java
Scanner scanner = new Scanner(System.in);
try {
    String line = scanner.nextLine();
    ...
} finally {
    scanner.close();
}
```

The modern way — **try-with-resources**:

```java
try (Scanner scanner = new Scanner(System.in)) {
    String line = scanner.nextLine();
    ...
}   // ← scanner.close() is called AUTOMATICALLY here, even if an exception happens! ✨
```

| Part | Meaning |
|---|---|
| `try (` ... `)` | Create the resource **inside the brackets** after `try`. |
| `}` at the end | Java **automatically** calls `close()`. |

It works with any class that implements the interface **`AutoCloseable`** (Chapter 25!). Files, Scanners, database connections — they all do.

### Example: reading a file

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class ReadFile {
    public static void main(String[] args) {
        try {
            List<String> lines = Files.readAllLines(Path.of("notes.txt"));
            for (String line : lines) {
                System.out.println("📄 " + line);
            }
        } catch (IOException e) {
            System.out.println("❌ Could not read the file: " + e.getMessage());
        }
    }
}
```

If `notes.txt` doesn't exist:

```
❌ Could not read the file: notes.txt
```

> 💡 `Files.readAllLines` opens and closes the file **for you**. For big files you'd use `Files.lines(...)` inside try-with-resources.

---

## 🚨 Part 7: `throw` — throwing your own exceptions

You can **throw** an exception yourself when something is wrong. We already did it in records (Chapter 29):

```java
public class BankAccount {
    private double balance;

    public void withdraw(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive, but was: " + amount);
        }
        if (amount > balance) {
            throw new IllegalStateException("Not enough money. Balance: " + balance);
        }
        balance -= amount;
    }
}
```

### 🔍 Line by line

`throw new IllegalArgumentException("Amount must be positive, but was: " + amount);`

| Part | Meaning |
|---|---|
| `throw` | "Pull the fire alarm! 🚨" — stop this method **immediately**. |
| `new IllegalArgumentException(...)` | Create an exception **object** (it's a normal class!). |
| `"Amount must be..."` | The **message**. Make it helpful: say **what** was wrong and **what the value was**. |

After `throw`, **no more lines** in the method run. The exception goes **up** to the caller.

### Which exception should I throw?

Java has good ready-made exceptions. Use them!

| Exception | Use when... | Example |
|---|---|---|
| `IllegalArgumentException` | a **parameter** has a bad value | negative age, empty name |
| `IllegalStateException` | the object is in the **wrong state** for this action | withdraw from a closed account |
| `NullPointerException` (via `Objects.requireNonNull`) | a value must not be `null` | `Objects.requireNonNull(name, "name")` |
| `UnsupportedOperationException` | this action is **not supported** | changing an immutable list |
| `IndexOutOfBoundsException` | an index is out of range | |

### 🤔 Why throw instead of printing?

In earlier chapters we did this:

```java
if (age < 0) {
    System.out.println("❌ Invalid age");   // 👎
    return;
}
```

**Problem:** The **caller** doesn't know anything went wrong! It continues as if everything was fine. 😶

With `throw`, the caller **must** react — or the program stops and shows **exactly** where and why. Much safer! 🛡️

```java
try {
    account.withdraw(500);
    System.out.println("✅ Here is your money");
} catch (IllegalStateException e) {
    System.out.println("❌ " + e.getMessage());
}
```

> 🌱 In Spring Boot, `System.out.println` messages are invisible to the user anyway (they appear on the **server**, not in the browser). Exceptions, however, can be turned into **proper error responses** (Part 11).

---

## ✅❌ Part 8: Checked vs. unchecked exceptions

Java has **two kinds** of exceptions:

| | **Unchecked** | **Checked** |
|---|---|---|
| Parent class | `RuntimeException` | `Exception` (but **not** `RuntimeException`) |
| Must you handle it? | ❌ No — Java doesn't force you | ✅ **Yes** — Java **forces** you to catch it or declare it |
| Usually means | a **bug** in the code (your fault) 🐛 | a problem **outside** your control (not your fault) 🌧️ |
| Examples | `NullPointerException`, `IllegalArgumentException`, `ArithmeticException` | `IOException` (file missing), `SQLException` (database down) |

📖 **Story:**
- **Unchecked** = you trip over your own shoelaces. 👟 Fix your shoelaces (fix the bug)!
- **Checked** = it starts raining. 🌧️ Not your fault — but you **must** have a plan (umbrella ☂️).

### Checked: Java forces you

```java
import java.nio.file.Files;
import java.nio.file.Path;

public static String readNote() {
    return Files.readString(Path.of("note.txt"));
    // ❌ error: unreported exception IOException; must be caught or declared to be thrown
}
```

Java says: "**Reading a file can fail** (the file may not exist). You must decide what to do!" Two choices:

**Choice 1: Catch it** (handle it here)

```java
public static String readNote() {
    try {
        return Files.readString(Path.of("note.txt"));
    } catch (IOException e) {
        return "(no note found)";
    }
}
```

**Choice 2: Declare it with `throws`** (pass it to the caller)

```java
public static String readNote() throws IOException {
    return Files.readString(Path.of("note.txt"));
}
```

| Part | Meaning |
|---|---|
| `throws IOException` | A **warning label** ⚠️ on the method: "I might throw an IOException. **You** (the caller) must deal with it." |

Now the **caller** must catch it (or declare it too). It's like passing the hot potato 🥔🔥 up until someone handles it.

### ⚠️ `throw` vs. `throws`

| | `throw` | `throws` |
|---|---|---|
| Where | **inside** a method | in the method **header** |
| What it does | **actually throws** an exception now | **warns** that the method **might** throw |
| Example | `throw new IOException("x");` | `void read() throws IOException` |

> 🌱 **Modern Java and Spring Boot mostly use unchecked exceptions.** Spring even **wraps** checked database exceptions into unchecked ones, so your code stays clean. When you make your own exceptions, usually extend **`RuntimeException`**.

---

## 🏗️ Part 9: Your own exception classes

Ready-made exceptions are good, but sometimes a **specific** name is much clearer:

```java
public class InsufficientFundsException extends RuntimeException {
    private final double balance;
    private final double requested;

    public InsufficientFundsException(double balance, double requested) {
        super("Not enough money: balance is " + balance + ", but " + requested + " was requested");
        this.balance = balance;
        this.requested = requested;
    }

    public double getMissingAmount() {
        return requested - balance;
    }
}
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `extends RuntimeException` | It's an **unchecked** exception (a child of RuntimeException). |
| `super("Not enough money: ...")` | Pass the **message** to the parent's constructor (Chapter 22). `getMessage()` will return it. |
| extra fields and methods | A custom exception can carry **extra information**! |

Using it:

```java
public class BankAccount {
    private final String owner;
    private double balance;

    public BankAccount(String owner, double balance) {
        this.owner = owner;
        this.balance = balance;
    }

    public void withdraw(double amount) {
        if (amount > balance) {
            throw new InsufficientFundsException(balance, amount);
        }
        balance -= amount;
    }
}
```

```java
BankAccount acc = new BankAccount("Sara", 100);
try {
    acc.withdraw(150);
} catch (InsufficientFundsException e) {
    System.out.println("❌ " + e.getMessage());
    System.out.println("💡 You need " + e.getMissingAmount() + " more.");
}
```

**Output:**

```
❌ Not enough money: balance is 100.0, but 150.0 was requested
💡 You need 50.0 more.
```

> 🌱 **In Spring Boot** you'll write exceptions like `StudentNotFoundException`, `EmailAlreadyUsedException`... and Spring will turn them into the right **HTTP error** (like `404 Not Found`). (Part 11 and Chapter 66.)

### Wrapping an exception (the "cause")

Sometimes you catch a technical exception and throw a clearer one, but **keep** the original as the **cause**:

```java
try {
    String text = Files.readString(Path.of("config.txt"));
} catch (IOException e) {
    throw new IllegalStateException("Could not load the settings", e);   // e = the cause
}
```

The stack trace will show **both**: "Could not load the settings" ... **Caused by**: `java.nio.file.NoSuchFileException: config.txt`. Very helpful when debugging! 🔍

---

## 👍👎 Part 10: Good habits

### ❌ Never swallow exceptions

```java
try {
    doSomething();
} catch (Exception e) {
    // nothing here 🙈
}
```

This is the **worst** thing you can do. The problem **disappears silently**. Later, something strange happens, and you have **no idea why**. 😱

**At least** log it:

```java
} catch (Exception e) {
    e.printStackTrace();   // or, in Spring Boot: log.error("Something failed", e);  (Chapter 88)
}
```

### ❌ Don't catch `Exception` everywhere

```java
try {
    ... 100 lines ...
} catch (Exception e) {
    System.out.println("Error");   // which error? where? why? 🤷
}
```

Catch **specific** exceptions you **know how to handle**.

### ✅ Catch only where you can **do something** useful

If you can't fix the problem, **don't catch it**. Let it go up to someone who can (or let it crash and show the stack trace while developing).

| Situation | What to do |
|---|---|
| User typed a wrong number | catch `NumberFormatException` → ask again ✅ |
| A file is missing, but there's a default | catch `IOException` → use the default ✅ |
| A bug: `NullPointerException` | **don't catch** → **fix the bug** 🐛 |
| You can't do anything useful here | **don't catch** → let it go up |

### ✅ Fail fast, with a clear message

Check values **early** (in constructors and at the start of methods) and throw with a **helpful** message:

```java
throw new IllegalArgumentException("age must be between 0 and 150, but was " + age);   // 👍
throw new IllegalArgumentException("error");                                             // 👎
```

### ✅ Don't use exceptions for normal flow

```java
// 👎 using an exception as an "if"
try {
    return list.get(0);
} catch (IndexOutOfBoundsException e) {
    return null;
}

// 👍 just check
return list.isEmpty() ? null : list.get(0);
```

Exceptions are for **exceptional** situations, not for normal decisions.

---

## 🌱 Part 11: Exceptions in Spring Boot (a preview)

In a web application, if your code throws an exception, Spring **catches** it and sends an **error response** to the browser instead of crashing the whole server.

You'll write things like:

```java
@ResponseStatus(HttpStatus.NOT_FOUND)
public class StudentNotFoundException extends RuntimeException {
    public StudentNotFoundException(Long id) {
        super("Student with id " + id + " was not found");
    }
}
```

```java
public Student findById(Long id) {
    return repository.findById(id)
            .orElseThrow(() -> new StudentNotFoundException(id));
}
```

And the user of your API gets a clean answer:

```json
{
  "status": 404,
  "error": "Not Found",
  "message": "Student with id 42 was not found"
}
```

We'll build this properly in **Chapter 66** (`@ControllerAdvice`). For now: **custom unchecked exceptions with clear messages** are exactly what Spring Boot wants! 🎉

---

## 💻 Mini project: A safe calculator 🧮

```java
import java.util.Scanner;

public class SafeCalculator {

    static class UnknownOperatorException extends RuntimeException {
        UnknownOperatorException(String op) {
            super("Unknown operator: '" + op + "'. Use + - * /");
        }
    }

    static double calculate(double a, String op, double b) {
        return switch (op) {
            case "+" -> a + b;
            case "-" -> a - b;
            case "*" -> a * b;
            case "/" -> {
                if (b == 0) {
                    throw new ArithmeticException("Cannot divide by zero");
                }
                yield a / b;
            }
            default -> throw new UnknownOperatorException(op);
        };
    }

    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            System.out.println("Type a calculation like: 12 * 3   (or 'quit')");

            while (true) {
                System.out.print("> ");
                String line = scanner.nextLine().strip();
                if (line.equalsIgnoreCase("quit")) {
                    break;
                }

                try {
                    String[] parts = line.split("\\s+");
                    if (parts.length != 3) {
                        throw new IllegalArgumentException("Please write: number operator number");
                    }
                    double a = Double.parseDouble(parts[0]);
                    double b = Double.parseDouble(parts[2]);
                    double result = calculate(a, parts[1], b);
                    System.out.println("= " + result);
                } catch (NumberFormatException e) {
                    System.out.println("❌ That's not a valid number.");
                } catch (ArithmeticException | IllegalArgumentException e) {
                    System.out.println("❌ " + e.getMessage());
                }
            }
        }
        System.out.println("Bye! 👋");
    }
}
```

**Example run:**

```
Type a calculation like: 12 * 3   (or 'quit')
> 12 * 3
= 36.0
> 10 / 0
❌ Cannot divide by zero
> 5 % 2
❌ Unknown operator: '%'. Use + - * /
> ten + 2
❌ That's not a valid number.
> 7 +
❌ Please write: number operator number
> quit
Bye! 👋
```

### 🔍 What we used

| Code | Concept |
|---|---|
| `try (Scanner scanner = ...)` | try-with-resources: the Scanner is closed automatically |
| `throw new ArithmeticException(...)` | throw a ready-made exception with a clear message |
| `default -> throw new UnknownOperatorException(op);` | a custom exception — even inside a switch expression! |
| `catch (NumberFormatException e)` **before** `IllegalArgumentException` | specific first: `NumberFormatException` is a **child** of `IllegalArgumentException`! |
| `catch (A \| B e)` | one catch for two types |
| The loop continues after an error | the user can try again 🔁 |

---

## ✋ Try it yourself

**Task 1:** Read this stack trace. What went wrong, and on which line of **your** code?

```
Exception in thread "main" java.lang.NullPointerException: Cannot invoke "String.length()" because "name" is null
	at com.example.Greeter.greet(Greeter.java:12)
	at com.example.App.main(App.java:7)
```

<details>
<summary>Click to see the answer</summary>

`name` was `null`, and the code called `name.length()`. It happened in `Greeter.java` line 12, in the method `greet`, which was called from `App.java` line 7.

</details>

**Task 2:** Write a method `int safeParse(String text, int defaultValue)` that returns the number, or `defaultValue` if the text is not a number.

<details>
<summary>Click to see the answer</summary>

```java
public static int safeParse(String text, int defaultValue) {
    try {
        return Integer.parseInt(text.strip());
    } catch (NumberFormatException | NullPointerException e) {
        return defaultValue;
    }
}
```

</details>

**Task 3:** Add checks to the `Person` constructor: throw `IllegalArgumentException` if the name is empty or the age is not between 0 and 150. Test it with `try/catch` in `main`.

**Task 4:** Make a custom exception `ProductNotFoundException(String name)`. Write a method `double findPrice(Map<String, Double> prices, String name)` that throws it when the product is missing.

<details>
<summary>Click to see the answer</summary>

```java
public class ProductNotFoundException extends RuntimeException {
    public ProductNotFoundException(String name) {
        super("No product called '" + name + "'");
    }
}

public static double findPrice(Map<String, Double> prices, String name) {
    Double price = prices.get(name);
    if (price == null) {
        throw new ProductNotFoundException(name);
    }
    return price;
}
```

</details>

**Task 5:** What does this print? Think carefully about `finally`!

```java
try {
    System.out.println("A");
    int x = 5 / 0;
    System.out.println("B");
} catch (ArithmeticException e) {
    System.out.println("C");
} finally {
    System.out.println("D");
}
System.out.println("E");
```

<details>
<summary>Click to see the answer</summary>

```
A
C
D
E
```

`B` is skipped because the exception happens before it.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Empty catch block

```java
catch (Exception e) { }   // 🙈 the error disappears
```

**Fix:** Handle it, log it, or don't catch it.

### Mistake 2: General catch before specific catch

```java
catch (Exception e) { ... }
catch (NumberFormatException e) { ... }   // ❌ error: exception NumberFormatException has already been caught
```

**Fix:** Specific first.

### Mistake 3: Ignoring a checked exception

```
error: unreported exception IOException; must be caught or declared to be thrown
```

**Fix:** `try/catch` it, or add `throws IOException` to the method.

### Mistake 4: Mixing up `throw` and `throws`

```java
void read() throw IOException { }      // ❌
void read() throws IOException { }     // ✅
throws new IOException("x");           // ❌
throw new IOException("x");            // ✅
```

### Mistake 5: Using a variable from `try` outside it

```java
try {
    int n = Integer.parseInt(text);
} catch (NumberFormatException e) { }
System.out.println(n);   // ❌ error: cannot find symbol — n only lives inside try { }
```

**Fix:** Declare `n` before the `try`.

### Mistake 6: Catching `NullPointerException` instead of fixing the bug

A NPE is almost always a **bug**. Find out **why** the value is `null`, and fix that.

---

## ✅ Summary

- An **exception** is a problem at run time. It **stops** the normal flow and goes **up** the call stack. 🚨
- **Stack trace**: first line = **what**; first `at` in your code = **where**. Click the blue links in IntelliJ.
- `try { ... } catch (SomeException e) { ... }` → handle it, the program continues.
- Many catches: **specific first**. One catch for many: `catch (A | B e)`.
- `finally { ... }` **always** runs → cleanup.
- **try-with-resources** `try (Scanner s = ...) { }` closes things **automatically**.
- `throw new IllegalArgumentException("clear message");` → throw your own.
- **Unchecked** (`RuntimeException`) = usually bugs, not forced. **Checked** (`IOException`) = outside problems, **must** catch or declare with `throws`.
- Make **custom exceptions** by extending `RuntimeException`.
- Good habits: never swallow exceptions, catch only what you can handle, fail fast with clear messages.
- Spring Boot turns exceptions into **HTTP error responses**. 🌱

---

## ❓ Quiz

1. What happens to the program when an exception is thrown and not caught?
2. In a stack trace, which line tells you **where** the problem happened?
3. When does a `finally` block run?
4. What does try-with-resources do?
5. What is the difference between `throw` and `throws`?
6. Is `NullPointerException` checked or unchecked? And `IOException`?
7. Which class should your own exceptions usually extend?
8. Why is an empty `catch` block dangerous?
9. Which exception should you throw if someone passes a negative age to a method?

<details>
<summary>Click to see the answers</summary>

1. It stops (crashes) and prints a stack trace.
2. The first `at ...` line that points to **your** code (file name and line number).
3. Always — whether an exception happened or not, caught or not.
4. It automatically closes the resource (Scanner, file...) at the end of the `try` block.
5. `throw` actually throws an exception (inside a method). `throws` in the method header warns that it might throw.
6. `NullPointerException`: unchecked. `IOException`: checked.
7. `RuntimeException`
8. The error disappears silently, and you won't know something went wrong.
9. `IllegalArgumentException`

</details>

---

[⬅ Previous chapter](32-sets.md) | [Table of Contents](../README.md) | [Next chapter: Generics ➡](34-generics.md)
