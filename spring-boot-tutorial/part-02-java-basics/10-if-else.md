# Chapter 10 – Making Decisions: `if` and `else`

[⬅ Previous chapter](09-strings.md) | [Table of Contents](../README.md) | [Next chapter ➡](11-switch.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- How to **compare** values: `==`, `!=`, `>`, `<`, `>=`, `<=`
- How to make the program **choose** what to do with `if`, `else` and `else if`
- How to **combine** conditions with `&&` (and), `||` (or), `!` (not)
- How to put an `if` inside another `if`
- A short form: the **ternary operator** `? :`

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Condition** | A question with a **yes/no** answer: "Is age 18 or more?" In Java, it gives a `boolean`. |
| **Comparison operator** | A symbol that compares two values: `>`, `<`, `==`... |
| **Logical operator** | A symbol that combines conditions: `&&` (and), `\|\|` (or), `!` (not). |
| **Block** | Code between `{` and `}`. |
| **Branch** | One of the possible "roads" the program can take. |
| **Nested** | One thing inside another (an `if` inside an `if`). |

---

## 📖 Story: The road with two ways 🛣️

You walk to school. You come to a sign:

```
                    ┌──────────────────┐
                    │ Is it raining? 🌧️ │
                    └────────┬─────────┘
                    yes      │       no
              ┌──────────────┴──────────────┐
              ▼                             ▼
     ┌─────────────────┐           ┌─────────────────┐
     │ Take umbrella ☂️ │           │ Wear sunglasses 😎│
     └─────────────────┘           └─────────────────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
                     ┌───────────────┐
                     │ Go to school 🏫│
                     └───────────────┘
```

Until now, our programs did **every** line, top to bottom. Now the program can **choose** a road. That's what `if` does!

---

## ⚖️ Part 1: Comparison operators

To make decisions, we first need **questions**. Comparison operators make yes/no questions. The answer is always a `boolean`: `true` or `false`.

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `==` | is equal to | `5 == 5` | `true` |
| `!=` | is **not** equal to | `5 != 3` | `true` |
| `>` | is bigger than | `7 > 3` | `true` |
| `<` | is smaller than | `7 < 3` | `false` |
| `>=` | is bigger than **or** equal to | `5 >= 5` | `true` |
| `<=` | is smaller than **or** equal to | `4 <= 3` | `false` |

```java
int age = 15;

System.out.println(age == 15);   // true
System.out.println(age != 15);   // false
System.out.println(age > 18);    // false
System.out.println(age < 18);    // true
System.out.println(age >= 15);   // true
System.out.println(age <= 10);   // false
```

### ⚠️ `=` vs. `==` — don't mix them up!

| | Meaning | Example |
|---|---|---|
| `=` | **Put into** (assign) | `age = 15;` → "put 15 into age" |
| `==` | **Is equal?** (compare) | `age == 15` → "is age equal to 15?" |

> 💡 **Memory trick:** One `=` **gives**. Two `==` **ask**. 🤔

### Remember: Strings use `.equals()`

```java
String color = "red";
System.out.println(color.equals("red"));   // ✅ true
System.out.println(color == "red");        // ❌ don't do this (Chapter 9)
```

---

## 🚦 Part 2: The `if` statement

```java
public class IfExample {
    public static void main(String[] args) {
        int temperature = 35;

        if (temperature > 30) {
            System.out.println("It is hot! Drink water. 💧");
        }

        System.out.println("Have a nice day!");
    }
}
```

**Output:**

```
It is hot! Drink water. 💧
Have a nice day!
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `if` | "**If**..." — the start of a decision. |
| `(temperature > 30)` | The **condition**, always inside round brackets. Java checks it: 35 > 30 → `true`. |
| `{` | Start of the block that runs **only if** the condition is `true`. |
| `System.out.println("It is hot!...");` | This line runs, because the condition was `true`. |
| `}` | End of the `if` block. |
| `System.out.println("Have a nice day!");` | **Outside** the `if`. It runs **always**. |

Now change `temperature` to `20` and run again:

**Output:**

```
Have a nice day!
```

The condition `20 > 30` is `false`, so Java **skips** the whole block `{ ... }`.

### 🗺️ How Java reads an `if`

```
          ┌──────────────────────┐
          │ temperature > 30 ?   │
          └──────────┬───────────┘
            true     │     false
         ┌───────────┘         │
         ▼                     │
  ┌──────────────────┐         │
  │ "It is hot!..."  │         │  (skip)
  └────────┬─────────┘         │
           └──────────┬────────┘
                      ▼
          ┌──────────────────────┐
          │ "Have a nice day!"   │
          └──────────────────────┘
```

---

## 🔀 Part 3: `if` ... `else`

`else` means "**otherwise**". It gives a second road for when the condition is `false`.

```java
public class IfElseExample {
    public static void main(String[] args) {
        int age = 15;

        if (age >= 18) {
            System.out.println("You can vote. 🗳️");
        } else {
            System.out.println("You are too young to vote.");
        }
    }
}
```

**Output:**

```
You are too young to vote.
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `if (age >= 18) {` | Is age 18 or more? 15 >= 18 → `false`. |
| `System.out.println("You can vote. 🗳️");` | **Skipped**, because the condition is false. |
| `} else {` | "Otherwise..." — this block runs when the condition is `false`. |
| `System.out.println("You are too young to vote.");` | **Runs**. |
| `}` | End. |

👉 With `if ... else`, **exactly one** of the two blocks runs. Never both. Never none.

### Example: even or odd?

```java
int number = 7;

if (number % 2 == 0) {
    System.out.println(number + " is even.");
} else {
    System.out.println(number + " is odd.");
}
```

**Output:**

```
7 is odd.
```

| Step | Value |
|---|---|
| `number % 2` | 7 % 2 = `1` |
| `1 == 0` | `false` |
| → go to `else` | prints "7 is odd." |

---

## 🪜 Part 4: `else if` — many choices

What if there are **more than two** roads? Use `else if`:

```java
public class Grades {
    public static void main(String[] args) {
        int score = 78;

        if (score >= 90) {
            System.out.println("Grade: A 🌟");
        } else if (score >= 80) {
            System.out.println("Grade: B 😀");
        } else if (score >= 70) {
            System.out.println("Grade: C 🙂");
        } else if (score >= 60) {
            System.out.println("Grade: D 😐");
        } else {
            System.out.println("Grade: F 😢");
        }
    }
}
```

**Output:**

```
Grade: C 🙂
```

### 🔍 How Java checks (score = 78)

| Check | Result | What happens |
|---|---|---|
| `78 >= 90` ? | false | go to the next check |
| `78 >= 80` ? | false | go to the next check |
| `78 >= 70` ? | **true** | print "Grade: C" → **STOP**. Skip everything else. |
| `78 >= 60` ? | (not checked) | |
| `else` | (not checked) | |

👉 Java checks **from top to bottom** and stops at the **first** `true`. Only **one** block runs.

### ⚠️ Order matters!

```java
// ❌ WRONG ORDER
if (score >= 60) {
    System.out.println("D");
} else if (score >= 90) {
    System.out.println("A");
}
```

With `score = 95`, the first check `95 >= 60` is already `true` → prints **"D"**! 😱
The "A" check is never reached.

👉 Put the **most specific** (strictest) condition **first**.

---

## 🔗 Part 5: Combining conditions — `&&`, `||`, `!`

### `&&` — AND (both must be true)

📖 "You can ride the roller coaster 🎢 if you are **at least 10 years old AND at least 140 cm tall**."

```java
int age = 12;
int height = 135;

if (age >= 10 && height >= 140) {
    System.out.println("You can ride! 🎢");
} else {
    System.out.println("Sorry, you can't ride.");
}
```

**Output:**

```
Sorry, you can't ride.
```

| Condition | Value |
|---|---|
| `age >= 10` | `true` |
| `height >= 140` | `false` |
| `true && false` | **`false`** — both must be true! |

### `||` — OR (at least one must be true)

📖 "You get a discount if you are **a student OR older than 65**."

```java
boolean isStudent = false;
int age = 70;

if (isStudent || age > 65) {
    System.out.println("You get a discount! 🎉");
}
```

**Output:**

```
You get a discount! 🎉
```

| Condition | Value |
|---|---|
| `isStudent` | `false` |
| `age > 65` | `true` |
| `false \|\| true` | **`true`** — one is enough! |

> ⌨️ The `|` key is usually above **Enter**, with **Shift** + `\`.

### `!` — NOT (turn it around)

```java
boolean isRaining = false;

if (!isRaining) {
    System.out.println("Let's go to the park! 🌳");
}
```

`!isRaining` → `!false` → `true`. So it prints. `!` turns `true` into `false`, and `false` into `true`.

### 📋 Truth table

| A | B | `A && B` | `A \|\| B` | `!A` |
|---|---|---|---|---|
| true | true | **true** | **true** | false |
| true | false | false | **true** | false |
| false | true | false | **true** | **true** |
| false | false | false | false | **true** |

👉 Simple:
- `&&` → true only if **all** are true.
- `||` → true if **at least one** is true.
- `!` → the opposite.

### ⚡ Short-circuit (Java is lazy — in a good way)

- With `&&`: if the **first** part is `false`, Java **doesn't check** the second part. (The answer is already `false`.)
- With `||`: if the **first** part is `true`, Java **doesn't check** the second part. (The answer is already `true`.)

This is useful to avoid crashes:

```java
int people = 0;
int cake = 10;

if (people != 0 && cake / people > 2) {
    System.out.println("Everyone gets more than 2 pieces.");
}
```

If `people` is 0, the first part is `false`, so Java **never** does `cake / people`. No "divide by zero" crash! 🛡️

### Using brackets with `&&` and `||`

`&&` is calculated **before** `||` (like `*` before `+`). Use brackets to be clear:

```java
// "Weekend AND (sunny OR warm)"
if (isWeekend && (isSunny || isWarm)) {
    System.out.println("Beach day! 🏖️");
}
```

---

## 🪆 Part 6: Nested `if` (an `if` inside an `if`)

```java
public class Cinema {
    public static void main(String[] args) {
        int age = 16;
        boolean hasTicket = true;

        if (hasTicket) {
            if (age >= 18) {
                System.out.println("Enjoy any movie! 🎬");
            } else {
                System.out.println("You can watch family movies. 🧸");
            }
        } else {
            System.out.println("Please buy a ticket first. 🎟️");
        }
    }
}
```

**Output:**

```
You can watch family movies. 🧸
```

### 🔍 How Java reads it

| Step | Check | Result |
|---|---|---|
| 1 | `hasTicket`? | true → go **inside** the first block |
| 2 | `age >= 18`? | 16 >= 18 → false → go to the **inner** `else` |
| 3 | print | "You can watch family movies." |

👉 **Indentation** (the spaces on the left) makes it easy to see which `else` belongs to which `if`. Always indent!

> 💡 **Tip:** Too many nested `if`s make code hard to read (like a Russian doll 🪆 with 10 dolls inside). Try to keep at most 2–3 levels. Often, `&&` can help:
> ```java
> if (hasTicket && age >= 18) { ... }
> ```

---

## ❓ Part 7: The ternary operator `? :` (short if-else)

For a **simple** choice between two **values**, there's a short form:

```java
int age = 20;
String status = (age >= 18) ? "adult" : "child";
System.out.println(status);   // adult
```

### 🔍 How to read it

```
   condition    ?   value if true   :   value if false
 (age >= 18)    ?     "adult"       :      "child"
```

Read it like a question: "**Is age >= 18? If yes → "adult". If no → "child".**"

It's the same as:

```java
String status;
if (age >= 18) {
    status = "adult";
} else {
    status = "child";
}
```

👉 Use it only for **short, simple** choices. For anything bigger, use normal `if`/`else` — it's easier to read.

---

## 📦 Part 8: Variables inside blocks (scope)

A variable made **inside** `{ }` lives **only** inside those braces:

```java
int age = 20;

if (age >= 18) {
    String message = "Welcome!";
    System.out.println(message);   // ✅ works
}

System.out.println(message);       // ❌ error: cannot find symbol
```

📖 Think of `{ }` as a **room**. A box (variable) you put in the room **stays** in the room. Outside the room, nobody can see it.

**Fix:** Declare the variable **before** the `if`:

```java
String message = "";
if (age >= 18) {
    message = "Welcome!";
}
System.out.println(message);   // ✅
```

---

## 💻 Mini project: Login check 🔐

```java
public class Login {
    public static void main(String[] args) {
        String correctUser = "admin";
        String correctPassword = "java123";

        String user = "admin";
        String password = "java12";

        if (user.isBlank() || password.isBlank()) {
            System.out.println("❗ Please fill in both fields.");
        } else if (!user.equals(correctUser)) {
            System.out.println("❌ Unknown user.");
        } else if (!password.equals(correctPassword)) {
            System.out.println("❌ Wrong password.");
        } else {
            System.out.println("✅ Welcome, " + user + "!");
        }
    }
}
```

**Output:**

```
❌ Wrong password.
```

### 🔍 Line by line

| Line | Check | Result |
|---|---|---|
| `if (user.isBlank() \|\| password.isBlank())` | Is one of the fields empty? | false → next |
| `else if (!user.equals(correctUser))` | Is the user **not** "admin"? `!true` → false | next |
| `else if (!password.equals(correctPassword))` | Is the password **not** "java123"? `"java12"` ≠ `"java123"` → `!false` → **true** | print "Wrong password." **STOP** |
| `else` | | not reached |

Try changing `password` to `"java123"` → you get `✅ Welcome, admin!`.

> 🌱 **In Spring Boot**, you will write checks like this **a lot** — but Spring Security will do the password part for you (Chapter 80).

---

## ✋ Try it yourself

**Task 1:** Make a variable `number`. Print `"positive"`, `"negative"` or `"zero"`.

<details>
<summary>Click to see the answer</summary>

```java
int number = -4;

if (number > 0) {
    System.out.println("positive");
} else if (number < 0) {
    System.out.println("negative");
} else {
    System.out.println("zero");
}
```

</details>

**Task 2:** Find the **biggest** of three numbers `a`, `b`, `c` using `if` (not `Math.max`).

<details>
<summary>Click to see the answer</summary>

```java
int a = 7, b = 12, c = 9;
int biggest;

if (a >= b && a >= c) {
    biggest = a;
} else if (b >= a && b >= c) {
    biggest = b;
} else {
    biggest = c;
}

System.out.println("Biggest: " + biggest);   // Biggest: 12
```

`int a = 7, b = 12, c = 9;` makes three `int` variables in one line.

</details>

**Task 3:** A year is a **leap year** if:
- it can be divided by 4, **and**
- it can **not** be divided by 100, **unless** it can also be divided by 400.

Check the years 2024 (yes), 1900 (no), 2000 (yes), 2023 (no).

<details>
<summary>Click to see the answer</summary>

```java
int year = 2024;

boolean isLeap = (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);

if (isLeap) {
    System.out.println(year + " is a leap year.");
} else {
    System.out.println(year + " is not a leap year.");
}
```

</details>

**Task 4:** Ticket price 🎟️:
- Under 5 years: free
- 5 to 17: 5 dollars
- 18 to 64: 12 dollars
- 65 and older: 6 dollars

Print the price for a given `age`.

**Task 5:** Use the ternary operator to print `"pass"` if `score >= 50`, otherwise `"fail"`.

<details>
<summary>Click to see the answer</summary>

```java
int score = 64;
System.out.println(score >= 50 ? "pass" : "fail");
```

</details>

---

## ⚠️ Common mistakes

### Mistake 1: `=` instead of `==`

```java
if (age = 18) { }    // ❌ error: incompatible types: int cannot be converted to boolean
if (age == 18) { }   // ✅
```

### Mistake 2: `;` after the `if` brackets

```java
if (age >= 18);      // ❌ this ; ENDS the if! The block below ALWAYS runs.
{
    System.out.println("Adult");
}
```

There is **no** error message — it just does the wrong thing. 😱 Never put `;` right after `if (...)`.

### Mistake 3: No braces `{ }`

```java
if (age >= 18)
    System.out.println("Adult");
    System.out.println("Can vote");   // ⚠️ this line is NOT part of the if! It always runs.
```

Without `{ }`, only the **first** line belongs to the `if`. The indentation lies!
👉 **Always use `{ }`**, even for one line.

### Mistake 4: Writing a range like in math

```java
if (10 < age < 20) { }             // ❌ error: bad operand types for binary operator '<'
if (age > 10 && age < 20) { }      // ✅
```

### Mistake 5: `else` with a condition

```java
} else (age < 18) {      // ❌ error
} else if (age < 18) {   // ✅
```

`else` never has a condition. If you need one, use `else if`.

### Mistake 6: Using `&` and `|` (single)

```java
if (a > 0 & b > 0)    // works, but no short-circuit — use &&
if (a > 0 && b > 0)   // ✅
```

---

## ✅ Summary

- Comparison operators: `==`, `!=`, `>`, `<`, `>=`, `<=`. They give `true` or `false`.
- `=` **puts**, `==` **asks**. Strings use `.equals()`.
- `if (condition) { ... }` runs the block only when the condition is `true`.
- `else { ... }` runs when the condition is `false`.
- `else if` gives many choices. Java stops at the **first** `true`. Order matters!
- `&&` = and (all true), `||` = or (at least one true), `!` = not (opposite).
- `&&` and `||` are lazy (short-circuit): they can protect you from crashes.
- A variable made inside `{ }` exists only inside those `{ }`.
- Ternary: `condition ? valueIfTrue : valueIfFalse`.
- **Always use `{ }`** and never put `;` after `if (...)`.

---

## ❓ Quiz

1. What is the difference between `=` and `==`?
2. What does `5 != 5` give?
3. What is `true && false`? And `true || false`?
4. What does `!true` give?
5. `int x = 10;` — Which block runs?
   ```java
   if (x > 20) { A } else if (x > 5) { B } else if (x > 0) { C } else { D }
   ```
6. Why is `if (age > 18);` dangerous?
7. Rewrite with the ternary operator: `if (n > 0) { s = "yes"; } else { s = "no"; }`
8. How do you check that `age` is between 13 and 19 (both included)?

<details>
<summary>Click to see the answers</summary>

1. `=` puts a value into a variable. `==` compares two values.
2. `false`
3. `false` and `true`.
4. `false`
5. `B` (the first true condition is `x > 5`).
6. The `;` ends the `if`, so the block after it **always** runs.
7. `s = (n > 0) ? "yes" : "no";`
8. `age >= 13 && age <= 19`

</details>

---

[⬅ Previous chapter](09-strings.md) | [Table of Contents](../README.md) | [Next chapter: switch ➡](11-switch.md)
