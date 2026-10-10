# Chapter 11 – Many Choices: `switch`

[⬅ Previous chapter](10-if-else.md) | [Table of Contents](../README.md) | [Next chapter ➡](12-for-loop.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- When `switch` is **better** than many `else if`s
- The **modern** `switch` with arrows `->` (recommended ✅)
- How a `switch` can **give back a value** (switch expression)
- The **old** `switch` with `case:` and `break` (you will see it in old code)
- The famous **fall-through** bug, and how to avoid it

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **switch** | A statement that picks **one** road from many, based on **one** value. |
| **case** | One possible value, and what to do for it. |
| **default** | What to do when **no** case matches. Like `else`. |
| **break** | "Stop here and leave the switch." (Old style.) |
| **Fall-through** | In the old style, if you forget `break`, Java **falls** into the next case too. A bug! |
| **Switch expression** | A `switch` that **gives back** a value. |

---

## 📖 Story: The elevator 🛗

You are in an elevator. There is **one** panel with many buttons:

```
 ┌─────────────────────┐
 │   [1] Shop 🛒        │
 │   [2] Restaurant 🍔  │
 │   [3] Cinema 🎬      │
 │   [4] Gym 🏋️         │
 └─────────────────────┘
```

You press **one** number, and the elevator goes **directly** to that floor. It doesn't stop at floor 1 to ask "Is this floor 3?", then floor 2 to ask again...

`switch` works like this: you give it **one value**, and it jumps **directly** to the matching `case`.

---

## 🤔 Part 1: The problem with many `else if`s

```java
int day = 3;

if (day == 1) {
    System.out.println("Monday");
} else if (day == 2) {
    System.out.println("Tuesday");
} else if (day == 3) {
    System.out.println("Wednesday");
} else if (day == 4) {
    System.out.println("Thursday");
} else if (day == 5) {
    System.out.println("Friday");
} else if (day == 6) {
    System.out.println("Saturday");
} else if (day == 7) {
    System.out.println("Sunday");
} else {
    System.out.println("Invalid day");
}
```

It works... but we write `day ==` **seven** times. 😩 It's long and boring. `switch` is cleaner.

---

## ➡️ Part 2: The modern `switch` (with arrows) ✅

Since Java 14, this is the **recommended** way:

```java
public class DayName {
    public static void main(String[] args) {
        int day = 3;

        switch (day) {
            case 1 -> System.out.println("Monday");
            case 2 -> System.out.println("Tuesday");
            case 3 -> System.out.println("Wednesday");
            case 4 -> System.out.println("Thursday");
            case 5 -> System.out.println("Friday");
            case 6 -> System.out.println("Saturday");
            case 7 -> System.out.println("Sunday");
            default -> System.out.println("Invalid day");
        }
    }
}
```

**Output:**

```
Wednesday
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `switch (day)` | "Look at the value of `day`." The value in brackets is what we check. |
| `{` | Start of the switch. |
| `case 1 ->` | "**If** day is `1`, **do** this:" The arrow `->` means "do". |
| `System.out.println("Monday");` | The action for case 1. |
| `case 3 -> ...` | day is 3 → this one runs → prints "Wednesday". Then the switch **ends** automatically. |
| `default ->` | "If **no** case matches, do this." Like the last `else`. |
| `}` | End of the switch. |

👉 With arrows `->`, **only one** case runs. No `break` needed. Simple and safe! 😊

---

## 🧩 Part 3: Many values in one case

Use a **comma** to give many values to one case:

```java
int day = 6;

switch (day) {
    case 1, 2, 3, 4, 5 -> System.out.println("Work day 💼");
    case 6, 7 -> System.out.println("Weekend 🎉");
    default -> System.out.println("Invalid day");
}
```

**Output:**

```
Weekend 🎉
```

`case 6, 7 ->` means: "If day is **6 or 7**, do this."

---

## 📦 Part 4: Many lines in one case

If you need **more than one line**, use `{ }`:

```java
int choice = 2;

switch (choice) {
    case 1 -> {
        System.out.println("You chose: Pizza 🍕");
        System.out.println("Price: 10 dollars");
    }
    case 2 -> {
        System.out.println("You chose: Burger 🍔");
        System.out.println("Price: 8 dollars");
    }
    default -> System.out.println("Unknown choice");
}
```

**Output:**

```
You chose: Burger 🍔
Price: 8 dollars
```

---

## 🔤 Part 5: `switch` with Strings and chars

`switch` works with `int`, `char`, `String`, and **enums** (Chapter 28). It does **not** work with `double`, `long` or `boolean`.

### With a String

```java
String command = "stop";

switch (command) {
    case "start" -> System.out.println("Starting the engine... 🚗");
    case "stop" -> System.out.println("Stopping. 🛑");
    case "pause" -> System.out.println("Pausing. ⏸️");
    default -> System.out.println("Unknown command: " + command);
}
```

**Output:**

```
Stopping. 🛑
```

> 💡 Good news: `switch` compares Strings **correctly** (like `.equals()`). But it **is** case-sensitive: `"STOP"` does not match `"stop"`. Tip: use `switch (command.toLowerCase())`.

### With a char

```java
char grade = 'B';

switch (grade) {
    case 'A' -> System.out.println("Excellent!");
    case 'B' -> System.out.println("Good job!");
    case 'C' -> System.out.println("OK.");
    default -> System.out.println("Keep trying!");
}
```

**Output:**

```
Good job!
```

---

## 🎁 Part 6: Switch **expression** — a switch that gives back a value

This is the **best** part of the modern switch. A switch can **return** a value, and you can put it straight into a variable:

```java
public class Season {
    public static void main(String[] args) {
        int month = 7;

        String season = switch (month) {
            case 12, 1, 2 -> "Winter ❄️";
            case 3, 4, 5 -> "Spring 🌸";
            case 6, 7, 8 -> "Summer ☀️";
            case 9, 10, 11 -> "Autumn 🍂";
            default -> "Unknown";
        };

        System.out.println("Month " + month + " is in " + season);
    }
}
```

**Output:**

```
Month 7 is in Summer ☀️
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `String season = switch (month) {` | "The value of `season` will be **whatever this switch gives back**." |
| `case 6, 7, 8 -> "Summer ☀️";` | If month is 6, 7 or 8, the switch **gives back** `"Summer ☀️"`. |
| `default -> "Unknown";` | ⚠️ A switch expression **must** cover every possible value. For an `int`, that means you **need** `default`. |
| `};` | ⚠️ Notice the **`;`** after `}`. The whole thing is one long statement: `String season = ...;` |

### `yield` — giving back a value from a `{ }` block

If a case needs **many lines** before giving the value, use `yield`:

```java
int score = 85;

String result = switch (score / 10) {
    case 10, 9 -> "A";
    case 8 -> {
        System.out.println("Almost an A!");
        yield "B";
    }
    case 7 -> "C";
    default -> "F";
};

System.out.println("Grade: " + result);
```

**Output:**

```
Almost an A!
Grade: B
```

| Part | Meaning |
|---|---|
| `score / 10` | 85 / 10 = **8** (integer division — a smart trick to group scores!) |
| `case 8 -> { ... }` | A block with many lines. |
| `yield "B";` | "**Give back** `"B"` as the value of the switch." (*Yield* means "give".) |

---

## 🏚️ Part 7: The old `switch` (with `case:` and `break`)

You **will** see this style in older code, in books and on the internet. So you need to **understand** it, even if you use the new style.

```java
int day = 2;

switch (day) {
    case 1:
        System.out.println("Monday");
        break;
    case 2:
        System.out.println("Tuesday");
        break;
    case 3:
        System.out.println("Wednesday");
        break;
    default:
        System.out.println("Other day");
}
```

**Output:**

```
Tuesday
```

### 🔍 Differences

| Old style | New style |
|---|---|
| `case 2:` (colon) | `case 2 ->` (arrow) |
| needs `break;` at the end of each case | no `break` needed |
| can "fall through" by mistake 🐛 | never falls through ✅ |

### 🐛 The fall-through bug

What if you **forget** `break`?

```java
int day = 2;

switch (day) {
    case 1:
        System.out.println("Monday");
    case 2:
        System.out.println("Tuesday");
    case 3:
        System.out.println("Wednesday");
    default:
        System.out.println("Other day");
}
```

**Output:**

```
Tuesday
Wednesday
Other day
```

😱 **Three** lines! Why?

In the old style, `case 2:` is just a **starting point**. Java starts there and keeps going **down**, line by line, until it finds a `break` or the end of the switch. It **falls through** the other cases like water down stairs. 💧🪜

```
 case 1:  Monday        (skipped — start is at case 2)
 case 2:  Tuesday       ◄── START HERE
     ⬇  (no break!)
 case 3:  Wednesday     ◄── falls in
     ⬇  (no break!)
 default: Other day     ◄── falls in
 }                      ◄── finally stops
```

👉 This is a **very common bug**. That's why we use the **new arrow style** `->` in this book. ✅

---

## 🆚 `switch` or `if`?

| Use `switch` when... | Use `if` / `else if` when... |
|---|---|
| You check **one** variable against many **exact** values | You check **ranges**: `age > 18`, `score >= 90` |
| Values like `1, 2, 3` or `"start", "stop"` | You combine conditions with `&&` / `\|\|` |
| You want to **pick a value** (switch expression) | Different variables in each check |

---

## 💻 Mini project: Calculator 🧮

```java
public class Calculator {
    public static void main(String[] args) {
        double a = 12;
        double b = 4;
        char operator = '/';

        double result = switch (operator) {
            case '+' -> a + b;
            case '-' -> a - b;
            case '*' -> a * b;
            case '/' -> {
                if (b == 0) {
                    System.out.println("⚠️ Can't divide by zero!");
                    yield 0;
                }
                yield a / b;
            }
            default -> {
                System.out.println("⚠️ Unknown operator: " + operator);
                yield 0;
            }
        };

        System.out.println(a + " " + operator + " " + b + " = " + result);
    }
}
```

**Output:**

```
12.0 / 4.0 = 3.0
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `char operator = '/';` | Which math to do. |
| `double result = switch (operator) {` | The switch gives back a `double`. |
| `case '+' -> a + b;` | For `+`, the value is `a + b`. |
| `case '/' -> { ... }` | For `/`, we need extra checks, so we use a block. |
| `if (b == 0) { ...; yield 0; }` | If b is zero, warn and give back `0`. |
| `yield a / b;` | Otherwise give back `a / b` = 3.0. |
| `default -> { ...; yield 0; }` | Unknown operator → warn and give back 0. |

Try changing `operator` to `'*'`, `'%'`, and `b` to `0`!

---

## ✋ Try it yourself

**Task 1:** Make a switch for traffic lights 🚦. A `String light` can be `"red"`, `"yellow"` or `"green"`. Print `"Stop"`, `"Get ready"` or `"Go"`. For anything else print `"Broken light"`.

<details>
<summary>Click to see the answer</summary>

```java
String light = "yellow";

switch (light) {
    case "red" -> System.out.println("Stop");
    case "yellow" -> System.out.println("Get ready");
    case "green" -> System.out.println("Go");
    default -> System.out.println("Broken light");
}
```

</details>

**Task 2:** Use a **switch expression** to get the number of days in a month (ignore leap years). `int month` → `int days`.

<details>
<summary>Click to see the answer</summary>

```java
int month = 4;

int days = switch (month) {
    case 2 -> 28;
    case 4, 6, 9, 11 -> 30;
    case 1, 3, 5, 7, 8, 10, 12 -> 31;
    default -> 0;
};

System.out.println("Month " + month + " has " + days + " days.");
```

</details>

**Task 3:** What does this **old-style** switch print when `x = 1`? Think first!

```java
switch (x) {
    case 1:
        System.out.println("one");
    case 2:
        System.out.println("two");
        break;
    case 3:
        System.out.println("three");
}
```

<details>
<summary>Click to see the answer</summary>

```
one
two
```

No `break` after case 1 → it falls into case 2. Case 2 has `break` → stop.

</details>

**Task 4:** Rewrite Task 3 in the **new arrow style** so that `x = 1` prints only `one`.

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `break` in the old style

See Part 7. **Fix:** Use the arrow style `->`.

### Mistake 2: Forgetting `;` after a switch expression

```java
String s = switch (x) {
    case 1 -> "one";
    default -> "other";
}       // ❌ error: ';' expected
};      // ✅
```

### Mistake 3: Missing `default` in a switch expression

```java
String s = switch (x) {
    case 1 -> "one";
    case 2 -> "two";
};   // ❌ error: the switch expression does not cover all possible input values
```

**Fix:** Add `default -> ...;`

### Mistake 4: Using ranges or conditions in `case`

```java
case x > 10 -> ...     // ❌ not allowed (in simple switches)
```

**Fix:** Use `if` / `else if` for ranges.

### Mistake 5: Switching on a `double` or `boolean`

```java
double price = 9.99;
switch (price) { ... }   // ❌ error
```

**Fix:** Use `if` / `else if`.

### Mistake 6: Two cases with the same value

```java
case 1 -> ...
case 1 -> ...   // ❌ error: duplicate case label
```

### Mistake 7: Mixing `->` and `:` in one switch

```java
switch (x) {
    case 1 -> System.out.println("a");
    case 2: System.out.println("b");   // ❌ error: different case kinds used in the switch
}
```

**Fix:** Use **only** arrows (recommended), or **only** colons.

---

## ✅ Summary

- `switch` picks **one** road based on **one** value. Cleaner than many `else if`s.
- **Modern style:** `case value -> action;` — no `break`, no fall-through. ✅ Use this.
- Many values: `case 6, 7 -> ...`. Many lines: `case 1 -> { ... }`.
- `default` runs when no case matches.
- Works with `int`, `char`, `String`, enums. Not with `double`, `long`, `boolean`.
- **Switch expression:** `String s = switch (x) { case 1 -> "one"; default -> "?"; };` — needs `default` and a `;` at the end.
- `yield` gives back a value from a `{ }` block in a switch expression.
- **Old style:** `case 1: ... break;` — forgetting `break` causes **fall-through**.
- Use `if` for **ranges** and complex conditions; `switch` for **exact** values.

---

## ❓ Quiz

1. What does `default` do in a switch?
2. In the arrow style, do you need `break`?
3. What is fall-through?
4. How do you write one case for the values 1, 2 and 3?
5. Can you use `switch` with a `double`?
6. What does `yield` do?
7. What is wrong?
   ```java
   int n = switch (x) { case 1 -> 10; case 2 -> 20; }
   ```
8. Would you use `switch` or `if` to check if `temperature > 30`?

<details>
<summary>Click to see the answers</summary>

1. It runs when **no** case matches (like `else`).
2. No.
3. In the old style, without `break`, Java keeps running the **next** cases too.
4. `case 1, 2, 3 -> ...`
5. No.
6. It gives back a value from a `{ }` block inside a switch expression.
7. Two things: `default` is missing, and the `;` after `}` is missing.
8. `if` — because it's a range, not an exact value.

</details>

---

[⬅ Previous chapter](10-if-else.md) | [Table of Contents](../README.md) | [Next chapter: The for loop ➡](12-for-loop.md)
