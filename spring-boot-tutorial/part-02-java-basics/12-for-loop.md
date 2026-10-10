# Chapter 12 – Doing Things Again and Again: The `for` Loop

[⬅ Previous chapter](11-switch.md) | [Table of Contents](../README.md) | [Next chapter ➡](13-while-loop.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **loop** is and why we need it
- How the **`for` loop** works — every part of it
- How to count **up**, **down**, and in **steps**
- How to **add up** numbers with a loop
- How to use `break` (stop the loop) and `continue` (skip one round)
- **Nested loops** (a loop inside a loop)

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Loop** | Code that **repeats** many times. |
| **Iteration** | **One** round of the loop. |
| **Counter** | A variable that counts the rounds. Usually called `i`. |
| **Condition** | The question "Should we do one more round?" |
| **Update** | The change to the counter after each round (usually `i++`). |
| **`break`** | Stop the loop **now**. |
| **`continue`** | Skip the rest of **this** round, go to the next round. |
| **Nested loop** | A loop inside another loop. |
| **Infinite loop** | A loop that **never stops**. Usually a bug. |

---

## 📖 Story: The teacher's punishment ✏️

A teacher says: "Write **'I will not talk in class'** 100 times!" 😩

Without a loop, you write:

```java
System.out.println("I will not talk in class");
System.out.println("I will not talk in class");
System.out.println("I will not talk in class");
// ... 97 more times 😵
```

With a loop:

```java
for (int i = 1; i <= 100; i++) {
    System.out.println("I will not talk in class");
}
```

**Three lines** instead of 100! 🎉 And if the teacher says 1000 times, you change **one number**.

Computers are **great** at repeating things. They never get tired or bored. 🤖

---

## 🔁 Part 1: Your first `for` loop

```java
public class FirstLoop {
    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) {
            System.out.println("Hello number " + i);
        }
        System.out.println("Done!");
    }
}
```

**Output:**

```
Hello number 1
Hello number 2
Hello number 3
Hello number 4
Hello number 5
Done!
```

### 🔍 The `for` line has 3 parts

```
 for ( int i = 1 ;   i <= 5   ;   i++   ) {
       ──────────    ────────     ─────
          ①             ②           ③
        START         CHECK      AFTER EACH
       (one time)   (every time)   ROUND
```

| Part | Code | Meaning |
|---|---|---|
| ① **Start** | `int i = 1` | Make a counter `i` and start at 1. This happens **only once**, at the very beginning. |
| ② **Check** | `i <= 5` | "Is `i` still 5 or less?" If **yes** → do one more round. If **no** → stop the loop. Checked **before every** round. |
| ③ **Update** | `i++` | After each round, add 1 to `i`. |
| `{ ... }` | the body | The code that is repeated. |

The three parts are separated by `;` (semicolons).

### 🎬 Step by step — slow motion

| Step | `i` | Check `i <= 5` | What happens |
|---|---|---|---|
| Start | 1 | | `i` is created with 1 |
| Round 1 | 1 | 1 <= 5 ✅ | print "Hello number 1", then `i++` → 2 |
| Round 2 | 2 | 2 <= 5 ✅ | print "Hello number 2", then `i++` → 3 |
| Round 3 | 3 | 3 <= 5 ✅ | print "Hello number 3", then `i++` → 4 |
| Round 4 | 4 | 4 <= 5 ✅ | print "Hello number 4", then `i++` → 5 |
| Round 5 | 5 | 5 <= 5 ✅ | print "Hello number 5", then `i++` → 6 |
| End | 6 | 6 <= 5 ❌ | **stop**. Go to the line after the loop → "Done!" |

### 🗺️ The flow

```
        ┌──────────────┐
        │ ① int i = 1  │
        └──────┬───────┘
               ▼
        ┌──────────────┐   false
  ┌────►│ ② i <= 5 ?   ├───────────► (leave the loop)
  │     └──────┬───────┘
  │            │ true
  │            ▼
  │     ┌──────────────┐
  │     │   { body }   │
  │     └──────┬───────┘
  │            ▼
  │     ┌──────────────┐
  └─────┤ ③ i++        │
        └──────────────┘
```

> 💡 **Why `i`?** It's a tradition from math (*i* for *index*). You can use any name: `count`, `round`, `n`... But `i` is what everyone uses for simple loops.

---

## 🔢 Part 2: Different ways to count

### Count from 0 (very common!)

```java
for (int i = 0; i < 5; i++) {
    System.out.print(i + " ");
}
```

**Output:**

```
0 1 2 3 4
```

👉 `i = 0; i < 5` → runs **5 times** (0, 1, 2, 3, 4). Programmers love this style because indexes start at 0 (remember Strings!).

| Style | Values of i | Rounds |
|---|---|---|
| `i = 1; i <= 5` | 1, 2, 3, 4, 5 | 5 |
| `i = 0; i < 5` | 0, 1, 2, 3, 4 | 5 |

### Count down (rocket launch 🚀)

```java
for (int i = 10; i >= 1; i--) {
    System.out.print(i + " ");
}
System.out.println("🚀 Lift off!");
```

**Output:**

```
10 9 8 7 6 5 4 3 2 1 🚀 Lift off!
```

| Part | Meaning |
|---|---|
| `int i = 10` | Start at 10. |
| `i >= 1` | Continue while `i` is 1 or more. |
| `i--` | Subtract 1 after each round. |

### Count in steps

```java
// Even numbers from 0 to 20
for (int i = 0; i <= 20; i += 2) {
    System.out.print(i + " ");
}
```

**Output:**

```
0 2 4 6 8 10 12 14 16 18 20
```

`i += 2` adds **2** each round, not 1.

```java
// Count by 5 (like a clock's minutes)
for (int minute = 0; minute < 60; minute += 5) {
    System.out.print(minute + " ");
}
```

**Output:**

```
0 5 10 15 20 25 30 35 40 45 50 55
```

---

## ➕ Part 3: Adding up with a loop

This is one of the most important patterns. Learn it well! 🧠

**Question:** What is 1 + 2 + 3 + ... + 100?

```java
public class SumNumbers {
    public static void main(String[] args) {
        int sum = 0;

        for (int i = 1; i <= 100; i++) {
            sum = sum + i;
        }

        System.out.println("The sum is: " + sum);
    }
}
```

**Output:**

```
The sum is: 5050
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `int sum = 0;` | A box to collect the total. Start with **0** (empty). It's made **before** the loop, so it survives after the loop. |
| `for (int i = 1; i <= 100; i++)` | `i` goes from 1 to 100. |
| `sum = sum + i;` | Add the current `i` to the total. (Short form: `sum += i;`) |
| `System.out.println(...)` | After the loop: print the total. |

### 🎬 The first rounds

| Round | `i` | `sum` before | `sum` after |
|---|---|---|---|
| 1 | 1 | 0 | 0 + 1 = **1** |
| 2 | 2 | 1 | 1 + 2 = **3** |
| 3 | 3 | 3 | 3 + 3 = **6** |
| 4 | 4 | 6 | 6 + 4 = **10** |
| ... | ... | ... | ... |
| 100 | 100 | 4950 | 4950 + 100 = **5050** |

🪣 Think of `sum` as a **bucket**. Every round, you pour `i` into the bucket.

### Same pattern: multiply (factorial)

5! ("5 factorial") = 5 × 4 × 3 × 2 × 1 = 120

```java
int result = 1;   // start with 1 for multiplying! (0 × anything = 0)

for (int i = 1; i <= 5; i++) {
    result *= i;
}

System.out.println("5! = " + result);   // 5! = 120
```

> ⚠️ For **adding**, start with `0`. For **multiplying**, start with `1`.

### Same pattern: counting

How many numbers between 1 and 50 can be divided by 7?

```java
int count = 0;

for (int i = 1; i <= 50; i++) {
    if (i % 7 == 0) {
        count++;
    }
}

System.out.println("Count: " + count);   // Count: 7  (7, 14, 21, 28, 35, 42, 49)
```

👉 Loops + `if` are best friends! 🤝

---

## 📋 Part 4: Multiplication table

```java
public class TimesTable {
    public static void main(String[] args) {
        int number = 7;

        for (int i = 1; i <= 10; i++) {
            System.out.println(number + " x " + i + " = " + (number * i));
        }
    }
}
```

**Output:**

```
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
```

---

## 🔤 Part 5: Looping over a String

Remember: a String is a train of characters with indexes 0 to length − 1. A loop can visit **every wagon**! 🚂

```java
String word = "JAVA";

for (int i = 0; i < word.length(); i++) {
    System.out.println("Index " + i + ": " + word.charAt(i));
}
```

**Output:**

```
Index 0: J
Index 1: A
Index 2: V
Index 3: A
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `int i = 0` | Start at the first index. |
| `i < word.length()` | `length()` is 4 → `i` goes 0, 1, 2, 3. ⚠️ Use `<`, **not** `<=`! Index 4 doesn't exist. |
| `word.charAt(i)` | The character at position `i`. |

### Example: count the vowels

```java
String text = "Programming is fun";
int vowels = 0;

for (int i = 0; i < text.length(); i++) {
    char c = Character.toLowerCase(text.charAt(i));
    if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
        vowels++;
    }
}

System.out.println("Vowels: " + vowels);   // Vowels: 5
```

| Line | Meaning |
|---|---|
| `Character.toLowerCase(...)` | Make the char small, so `'A'` and `'a'` are both counted. |
| `c == 'a' \|\| ...` | Is it a vowel? (`char` can use `==` because it's a primitive.) |

### Example: reverse a word

```java
String word = "hello";
String reversed = "";

for (int i = word.length() - 1; i >= 0; i--) {
    reversed += word.charAt(i);
}

System.out.println(reversed);   // olleh
```

Start at the **last** index (4) and go **down** to 0.

---

## 🛑 Part 6: `break` — stop the loop early

```java
for (int i = 1; i <= 10; i++) {
    if (i == 5) {
        System.out.println("Found 5! Stopping.");
        break;
    }
    System.out.println(i);
}
System.out.println("After the loop");
```

**Output:**

```
1
2
3
4
Found 5! Stopping.
After the loop
```

| Part | Meaning |
|---|---|
| `break;` | **Leave the loop immediately.** Jump to the first line **after** the loop. |

👉 Use it when you **found** what you were looking for, and there's no need to continue. 🔍

### Example: find the first number divisible by 13

```java
for (int i = 100; i <= 200; i++) {
    if (i % 13 == 0) {
        System.out.println("First: " + i);   // First: 104
        break;
    }
}
```

---

## ⏭️ Part 7: `continue` — skip this round

```java
for (int i = 1; i <= 10; i++) {
    if (i % 3 == 0) {
        continue;
    }
    System.out.print(i + " ");
}
```

**Output:**

```
1 2 4 5 7 8 10
```

| Part | Meaning |
|---|---|
| `continue;` | **Skip the rest of this round.** Go directly to the update (`i++`) and the next round. |

3, 6 and 9 are skipped, because `i % 3 == 0` is true for them.

### 🆚 `break` vs. `continue`

| | `break` | `continue` |
|---|---|---|
| What it does | **Stops** the whole loop | **Skips** one round |
| Story | 🏃 You leave the race. | 🦘 You jump over one hurdle and keep running. |

---

## 🪆 Part 8: Nested loops (a loop inside a loop)

```java
for (int row = 1; row <= 3; row++) {
    for (int col = 1; col <= 4; col++) {
        System.out.print("* ");
    }
    System.out.println();
}
```

**Output:**

```
* * * *
* * * *
* * * *
```

### 🔍 How it works

| Part | Meaning |
|---|---|
| Outer loop `row` | Runs **3** times (one time per row). |
| Inner loop `col` | For **each** row, it runs **4** times (prints 4 stars). |
| `System.out.println();` | After the inner loop finishes, go to a new line. |

Total stars: 3 × 4 = **12**.

🕐 Think of a **clock**: the minute hand (inner loop) goes all the way around (60 times) for **every one** step of the hour hand (outer loop).

### Example: a triangle 🔺

```java
for (int row = 1; row <= 5; row++) {
    for (int col = 1; col <= row; col++) {
        System.out.print("* ");
    }
    System.out.println();
}
```

**Output:**

```
*
* *
* * *
* * * *
* * * * *
```

The trick: `col <= row`. Row 1 → 1 star. Row 2 → 2 stars. Row 5 → 5 stars.

### Example: full multiplication table

```java
for (int a = 1; a <= 5; a++) {
    for (int b = 1; b <= 5; b++) {
        System.out.print((a * b) + "\t");
    }
    System.out.println();
}
```

**Output:**

```
1	2	3	4	5
2	4	6	8	10
3	6	9	12	15
4	8	12	16	20
5	10	15	20	25
```

`\t` is a **tab** — it makes nice columns.

---

## 💻 Mini project: FizzBuzz 🐝

A famous programming puzzle (often used in job interviews!):

Print the numbers 1 to 20. But:
- If the number can be divided by **3**, print `Fizz` instead.
- If it can be divided by **5**, print `Buzz` instead.
- If it can be divided by **both 3 and 5**, print `FizzBuzz`.

```java
public class FizzBuzz {
    public static void main(String[] args) {
        for (int i = 1; i <= 20; i++) {
            if (i % 3 == 0 && i % 5 == 0) {
                System.out.println("FizzBuzz");
            } else if (i % 3 == 0) {
                System.out.println("Fizz");
            } else if (i % 5 == 0) {
                System.out.println("Buzz");
            } else {
                System.out.println(i);
            }
        }
    }
}
```

**Output:**

```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
Buzz
```

### 🔍 Why is the "both" check **first**?

If we checked `i % 3 == 0` first, then 15 would print `Fizz` and **stop** (remember: `else if` stops at the first true). The `FizzBuzz` case would never be reached. Most specific condition first! (Chapter 10.)

---

## ✋ Try it yourself

**Task 1:** Print all numbers from 1 to 30 that are **odd**.

<details>
<summary>Click to see two possible answers</summary>

```java
// Way 1: check with if
for (int i = 1; i <= 30; i++) {
    if (i % 2 != 0) {
        System.out.print(i + " ");
    }
}

// Way 2: jump by 2
for (int i = 1; i <= 30; i += 2) {
    System.out.print(i + " ");
}
```

</details>

**Task 2:** Calculate the **average** of the numbers 1 to 10. (Answer: 5.5)

<details>
<summary>Click to see the answer</summary>

```java
int sum = 0;
int count = 0;

for (int i = 1; i <= 10; i++) {
    sum += i;
    count++;
}

double average = (double) sum / count;
System.out.println("Average: " + average);
```

Remember the `(double)` — otherwise 55 / 10 = 5! (Chapter 8.)

</details>

**Task 3:** Check if a word is a **palindrome** (the same forwards and backwards), like `"level"` or `"racecar"`.

<details>
<summary>Click to see the answer</summary>

```java
String word = "racecar";
String reversed = "";

for (int i = word.length() - 1; i >= 0; i--) {
    reversed += word.charAt(i);
}

if (word.equals(reversed)) {
    System.out.println(word + " is a palindrome!");
} else {
    System.out.println(word + " is not a palindrome.");
}
```

</details>

**Task 4:** Print this upside-down triangle:

```
* * * * *
* * * *
* * *
* *
*
```

<details>
<summary>Click to see the answer</summary>

```java
for (int row = 5; row >= 1; row--) {
    for (int col = 1; col <= row; col++) {
        System.out.print("* ");
    }
    System.out.println();
}
```

</details>

**Task 5:** Is a number **prime**? (A prime number can only be divided by 1 and itself: 2, 3, 5, 7, 11, 13...) Check `number = 29`.

<details>
<summary>Click to see the answer</summary>

```java
int number = 29;
boolean isPrime = number > 1;

for (int i = 2; i < number; i++) {
    if (number % i == 0) {
        isPrime = false;
        break;   // found a divider, no need to check more
    }
}

System.out.println(number + (isPrime ? " is prime" : " is not prime"));
```

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Off-by-one (one too many or one too few)

```java
for (int i = 0; i <= 5; i++)   // runs 6 times (0..5), not 5!
for (int i = 1; i < 5; i++)    // runs 4 times (1..4), not 5!
```

👉 For 5 rounds: `i = 0; i < 5` **or** `i = 1; i <= 5`.

### Mistake 2: `<=` with `length()`

```java
for (int i = 0; i <= word.length(); i++) {
    word.charAt(i);    // 💥 StringIndexOutOfBoundsException at the last round
}
```

**Fix:** `i < word.length()`.

### Mistake 3: Infinite loop ♾️

```java
for (int i = 1; i <= 10; i--) {   // i goes 1, 0, -1, -2... never > 10!
    System.out.println(i);
}
```

The program **never stops**. 😱 In IntelliJ, click the red **■ Stop** button. In the terminal, press **Ctrl + C**.
**Fix:** Make sure the update moves `i` **towards** the end (`i++` here).

### Mistake 4: `;` after the `for` brackets

```java
for (int i = 0; i < 5; i++);   // ❌ the ; is an empty body! The loop does nothing 5 times.
{
    System.out.println(i);      // ❌ error: cannot find symbol i
}
```

### Mistake 5: Using `i` after the loop

```java
for (int i = 0; i < 5; i++) { }
System.out.println(i);   // ❌ error: cannot find symbol
```

`i` only lives **inside** the loop (scope!).

### Mistake 6: Making the sum variable inside the loop

```java
for (int i = 1; i <= 5; i++) {
    int sum = 0;      // ❌ reset to 0 every round!
    sum += i;
}
```

**Fix:** Make `sum` **before** the loop.

### Mistake 7: Commas instead of semicolons

```java
for (int i = 0, i < 5, i++)   // ❌ error
for (int i = 0; i < 5; i++)   // ✅
```

---

## ✅ Summary

- A **loop** repeats code. The `for` loop is best when you know **how many times**.
- `for (start; check; update) { body }`
  - **start** runs once
  - **check** runs before every round — if false, the loop ends
  - **update** runs after every round
- `i = 0; i < n` → n rounds (0 to n−1). `i = 1; i <= n` → n rounds (1 to n).
- Count down with `i--`, count in steps with `i += 2`.
- **Sum pattern:** `int sum = 0;` before the loop, `sum += i;` inside.
- Loop over a String: `for (int i = 0; i < s.length(); i++) { s.charAt(i) }`
- `break` → stop the loop. `continue` → skip to the next round.
- Nested loops: the inner loop runs **completely** for each round of the outer loop.
- Watch out for **off-by-one** errors and **infinite loops**.

---

## ❓ Quiz

1. What are the three parts inside `for ( ... )`?
2. How many times does `for (int i = 0; i < 10; i++)` run?
3. What does `for (int i = 10; i > 0; i -= 3)` print if the body is `System.out.print(i + " ");`?
4. What is the difference between `break` and `continue`?
5. Why should `sum` be created **before** the loop?
6. An outer loop runs 4 times and an inner loop runs 3 times. How many times does the inner body run in total?
7. How do you stop an infinite loop in IntelliJ?

<details>
<summary>Click to see the answers</summary>

1. Start (`int i = 0`), check (`i < 10`), update (`i++`).
2. 10 times.
3. `10 7 4 1`
4. `break` stops the whole loop. `continue` skips only the current round.
5. If it's created inside, it becomes 0 again in every round, and it doesn't exist after the loop.
6. 4 × 3 = **12** times.
7. Click the red **■ Stop** button (or Ctrl + C in the terminal).

</details>

---

[⬅ Previous chapter](11-switch.md) | [Table of Contents](../README.md) | [Next chapter: The while loop ➡](13-while-loop.md)
