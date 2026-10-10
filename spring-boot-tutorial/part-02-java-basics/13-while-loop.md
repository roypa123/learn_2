# Chapter 13 – The `while` Loop

[⬅ Previous chapter](12-for-loop.md) | [Table of Contents](../README.md) | [Next chapter ➡](14-arrays.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- How the **`while`** loop works
- How the **`do ... while`** loop works, and how it is different
- **When** to use `for`, `while` or `do-while`
- How to use `while (true)` with `break`
- How to avoid **infinite loops**

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **while** | "As long as..." — repeat **as long as** the condition is true. |
| **do ... while** | "Do it first, **then** check." The body runs **at least once**. |
| **Sentinel** | A special value that means "stop", like `0` or `"quit"`. |
| **Flag** | A `boolean` variable that remembers if something happened, like `found = true`. |

---

## 📖 Story: Eating soup 🍲

Your mom gives you a bowl of soup. You don't know **how many** spoons it will take.

You just do this:

> **As long as** there is soup in the bowl → take one more spoon. 🥄

You don't count. You just **check** before each spoon: "Is there still soup?"

That's a `while` loop!

- `for` loop: "Do it **10 times**." → you **know** the number.
- `while` loop: "Do it **as long as** something is true." → you **don't know** the number.

---

## 🔁 Part 1: The `while` loop

```java
public class WhileExample {
    public static void main(String[] args) {
        int count = 1;

        while (count <= 5) {
            System.out.println("Count is " + count);
            count++;
        }

        System.out.println("Finished!");
    }
}
```

**Output:**

```
Count is 1
Count is 2
Count is 3
Count is 4
Count is 5
Finished!
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `int count = 1;` | Make the counter **before** the loop. |
| `while (count <= 5) {` | "**As long as** `count` is 5 or less, repeat the block." Checked **before** every round. |
| `System.out.println(...)` | The work. |
| `count++;` | ⚠️ **Very important!** Change the counter. Without this, `count` stays 1 forever → infinite loop! |
| `}` | Go back up to the `while` and check again. |

### 🗺️ The flow

```
          ┌───────────────────┐   false
    ┌────►│ count <= 5 ?      ├───────────► (leave the loop)
    │     └─────────┬─────────┘
    │               │ true
    │               ▼
    │     ┌───────────────────┐
    │     │ print, count++    │
    │     └─────────┬─────────┘
    └───────────────┘
```

### `for` vs. `while` — the same loop

These two loops do **exactly** the same thing:

```java
// for loop                       // while loop
for (int i = 1; i <= 5; i++) {    int i = 1;               // start
    System.out.println(i);        while (i <= 5) {         // check
}                                     System.out.println(i);
                                      i++;                 // update
                                  }
```

The `for` loop puts the 3 parts **on one line**. The `while` loop **spreads** them out.
👉 When you **count**, `for` is cleaner. When you **don't know** how many times, `while` is better.

---

## 🤷 Part 2: When you don't know how many times

### Example 1: Saving money 💰

You save 15 dollars every week. How many weeks until you have 100 dollars?

```java
public class Savings {
    public static void main(String[] args) {
        int money = 0;
        int weeks = 0;
        int goal = 100;

        while (money < goal) {
            money += 15;
            weeks++;
            System.out.println("Week " + weeks + ": " + money + " dollars");
        }

        System.out.println("You reached your goal in " + weeks + " weeks! 🎉");
    }
}
```

**Output:**

```
Week 1: 15 dollars
Week 2: 30 dollars
Week 3: 45 dollars
Week 4: 60 dollars
Week 5: 75 dollars
Week 6: 90 dollars
Week 7: 105 dollars
You reached your goal in 7 weeks! 🎉
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `while (money < goal)` | As long as we have **less** than the goal, keep saving. |
| `money += 15;` | Save 15 more. |
| `weeks++;` | One more week passed. |
| After week 7 | money = 105. Check `105 < 100` → false → **stop**. |

👉 We didn't know "7" before. The loop **found** it for us!

### Example 2: Count the digits of a number

How many digits does `48213` have?

```java
int number = 48213;
int digits = 0;

while (number > 0) {
    number = number / 10;   // remove the last digit
    digits++;
}

System.out.println("Digits: " + digits);   // Digits: 5
```

| Round | `number` before | `number / 10` | `digits` |
|---|---|---|---|
| 1 | 48213 | 4821 | 1 |
| 2 | 4821 | 482 | 2 |
| 3 | 482 | 48 | 3 |
| 4 | 48 | 4 | 4 |
| 5 | 4 | 0 | 5 |
| check | 0 | `0 > 0` false → stop | |

(Integer division cuts the last digit each time. Remember Chapter 8!)

### Example 3: Roll a dice until you get a 6 🎲

```java
int roll = 0;
int tries = 0;

while (roll != 6) {
    roll = (int) (Math.random() * 6) + 1;
    tries++;
    System.out.println("Try " + tries + ": rolled " + roll);
}

System.out.println("Got a 6 after " + tries + " tries!");
```

**Output (different every time!):**

```
Try 1: rolled 3
Try 2: rolled 1
Try 3: rolled 6
Got a 6 after 3 tries!
```

👉 Nobody knows how many tries it will take — maybe 1, maybe 20. A perfect job for `while`!

---

## 🔂 Part 3: The `do ... while` loop

In a `while` loop, the check is at the **start**. If the condition is false from the beginning, the body **never** runs.

In a `do ... while` loop, the check is at the **end**. The body **always runs at least once**.

```java
int number = 10;

do {
    System.out.println("Number is " + number);
    number++;
} while (number < 5);

System.out.println("Done");
```

**Output:**

```
Number is 10
Done
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `do {` | "**Do** this first..." |
| `System.out.println(...)` | Runs once — **without** any check. |
| `number++;` | number becomes 11. |
| `} while (number < 5);` | "...then repeat **while** number < 5." 11 < 5 → false → stop. ⚠️ Notice the `;` at the end! |

The condition was false from the start, but the body still ran **once**.

### 🆚 `while` vs. `do ... while`

```
       while                         do ... while
 ┌─────────────────┐            ┌─────────────────┐
 │ CHECK first     │            │ DO the body     │
 │   ↓ true        │            │   ↓             │
 │ DO the body     │            │ CHECK after     │
 │   ↓             │            │   ↓ true        │
 │ go back up      │            │ go back up      │
 └─────────────────┘            └─────────────────┘
  may run 0 times                runs at least 1 time
```

📖 **Story:**
- `while` = "Look in the fridge. **If** there's food, eat." 🧊 (Maybe you eat nothing.)
- `do ... while` = "**Taste** the soup, **then** decide if you want more." 🍲 (You always taste once.)

### When is `do ... while` useful?

When you **must** do something once **before** you can check. The classic example is a **menu**: show it first, then ask "again?". In Chapter 16 we'll use it with real keyboard input.

```java
int choice;
int round = 0;

do {
    round++;
    System.out.println("=== MENU (round " + round + ") ===");
    System.out.println("1. Play");
    System.out.println("2. Settings");
    System.out.println("0. Exit");

    // Here we fake the user's choice. In Chapter 16 we read it from the keyboard!
    choice = (round < 3) ? 1 : 0;
    System.out.println("You chose: " + choice);
} while (choice != 0);

System.out.println("Goodbye! 👋");
```

---

## ♾️ Part 4: `while (true)` with `break`

Sometimes the "stop" decision is in the **middle** of the loop. Then you can write a loop that runs "forever", and use `break` to get out:

```java
int number = 1;

while (true) {
    number *= 2;
    System.out.println(number);

    if (number > 100) {
        break;
    }
}

System.out.println("Stopped at " + number);
```

**Output:**

```
2
4
8
16
32
64
128
Stopped at 128
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `while (true)` | The condition is **always** true → this loop would never stop by itself. |
| `number *= 2;` | Double the number. |
| `if (number > 100) { break; }` | The **exit door** 🚪. When the number is bigger than 100, leave the loop. |

> ⚠️ With `while (true)`, you **must** have a `break` that will surely happen. Otherwise: infinite loop!

👉 This style is common for **programs that wait for commands** — like a game loop 🎮, or a **server** that waits for requests forever (Spring Boot's server does something like this inside!).

---

## 🚩 Part 5: Using a flag

A **flag** is a `boolean` that remembers something. 🚩

```java
String text = "Hello World";
boolean foundSpace = false;
int i = 0;

while (i < text.length() && !foundSpace) {
    if (text.charAt(i) == ' ') {
        foundSpace = true;
        System.out.println("Found a space at index " + i);
    }
    i++;
}
```

**Output:**

```
Found a space at index 5
```

| Part | Meaning |
|---|---|
| `boolean foundSpace = false;` | The flag starts **down** (false). |
| `while (i < text.length() && !foundSpace)` | Continue **while** there are more characters **and** we have **not** found a space yet. |
| `foundSpace = true;` | Raise the flag! 🚩 The loop will stop at the next check. |

---

## 🤔 Part 6: Which loop should I use?

| Situation | Best loop | Example |
|---|---|---|
| I know **how many** times | `for` | Print 10 lines. Go through a String. |
| I **don't know** how many times. Maybe 0 times. | `while` | Save money until the goal. Read until the file ends. |
| I don't know how many times, but **at least once** | `do ... while` | Show a menu, then ask again. |
| The stop decision is in the **middle** | `while (true)` + `break` | Game loop. Server loop. |

👉 Don't worry too much. Any loop can do the job of the others. Choose the one that is **easiest to read**.

---

## 💻 Mini project: Number guessing game (computer vs. computer) 🎯

The computer picks a secret number from 1 to 100. Another "player" (also the computer 😄) guesses in a smart way: always the **middle** of the possible range.

```java
public class GuessingGame {
    public static void main(String[] args) {
        int secret = (int) (Math.random() * 100) + 1;
        int low = 1;
        int high = 100;
        int tries = 0;
        boolean found = false;

        System.out.println("(Secret number is " + secret + ")");

        while (!found) {
            int guess = (low + high) / 2;
            tries++;
            System.out.print("Try " + tries + ": guess " + guess + " → ");

            if (guess == secret) {
                System.out.println("Correct! 🎉");
                found = true;
            } else if (guess < secret) {
                System.out.println("Too low ⬆️");
                low = guess + 1;
            } else {
                System.out.println("Too high ⬇️");
                high = guess - 1;
            }
        }

        System.out.println("Found it in " + tries + " tries.");
    }
}
```

**Output (example with secret = 73):**

```
(Secret number is 73)
Try 1: guess 50 → Too low ⬆️
Try 2: guess 75 → Too high ⬇️
Try 3: guess 62 → Too low ⬆️
Try 4: guess 68 → Too low ⬆️
Try 5: guess 71 → Too low ⬆️
Try 6: guess 73 → Correct! 🎉
Found it in 6 tries.
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `int secret = (int) (Math.random() * 100) + 1;` | A random number 1–100. |
| `int low = 1; int high = 100;` | The secret is somewhere between `low` and `high`. |
| `boolean found = false;` | A flag 🚩. |
| `while (!found)` | Keep guessing **as long as** we haven't found it. |
| `int guess = (low + high) / 2;` | Guess the **middle**. |
| `low = guess + 1;` | Too low → the secret is **above** the guess. Move `low` up. |
| `high = guess - 1;` | Too high → the secret is **below** the guess. Move `high` down. |

🤯 This smart strategy **always** finds the number in **7 tries or fewer** — for any number 1 to 100! It's called **binary search**. Each guess cuts the possible numbers in **half**.

In Chapter 16, you'll make a version where **you** play by typing on the keyboard! ⌨️

---

## ✋ Try it yourself

**Task 1:** Use a `while` loop to print the numbers 10, 20, 30 ... 100.

<details>
<summary>Click to see the answer</summary>

```java
int n = 10;
while (n <= 100) {
    System.out.print(n + " ");
    n += 10;
}
```

</details>

**Task 2:** A ball is dropped from 100 meters. Every bounce, it goes back up to **half** the height. How many bounces until the height is less than 1 meter?

<details>
<summary>Click to see the answer</summary>

```java
double height = 100;
int bounces = 0;

while (height >= 1) {
    height = height / 2;
    bounces++;
    System.out.println("Bounce " + bounces + ": " + height + " m");
}

System.out.println("Total bounces: " + bounces);   // 7
```

</details>

**Task 3:** Add up the digits of a number. For example `4721` → 4 + 7 + 2 + 1 = **14**.
Hint: `number % 10` gives the last digit. `number / 10` removes it.

<details>
<summary>Click to see the answer</summary>

```java
int number = 4721;
int sum = 0;

while (number > 0) {
    int lastDigit = number % 10;
    sum += lastDigit;
    number /= 10;
}

System.out.println("Sum of digits: " + sum);   // 14
```

</details>

**Task 4:** Reverse the digits of a number: `1234` → `4321`.
Hint: `reversed = reversed * 10 + lastDigit;`

<details>
<summary>Click to see the answer</summary>

```java
int number = 1234;
int reversed = 0;

while (number > 0) {
    int lastDigit = number % 10;
    reversed = reversed * 10 + lastDigit;
    number /= 10;
}

System.out.println(reversed);   // 4321
```

| number | lastDigit | reversed |
|---|---|---|
| 1234 | 4 | 0×10+4 = 4 |
| 123 | 3 | 4×10+3 = 43 |
| 12 | 2 | 43×10+2 = 432 |
| 1 | 1 | 432×10+1 = 4321 |

</details>

**Task 5:** What does this print? Why?

```java
int x = 5;
while (x < 5) {
    System.out.println("while");
}
do {
    System.out.println("do-while");
} while (x < 5);
```

<details>
<summary>Click to see the answer</summary>

```
do-while
```

The `while` loop checks first: 5 < 5 is false → never runs.
The `do-while` runs once **before** checking.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting to update the variable → infinite loop ♾️

```java
int i = 0;
while (i < 5) {
    System.out.println(i);
    // ❌ forgot i++ → prints 0 forever!
}
```

**Stop it:** red **■ Stop** button in IntelliJ, or **Ctrl + C** in the terminal.
**Fix:** Make sure something **inside** the loop moves toward making the condition `false`.

### Mistake 2: `;` after `while (...)`

```java
while (i < 5);      // ❌ an empty loop that runs forever (i never changes)
{
    i++;
}
```

### Mistake 3: Forgetting `;` after `do ... while`

```java
do {
    ...
} while (x < 5)     // ❌ error: ';' expected
} while (x < 5);    // ✅
```

### Mistake 4: The condition is the wrong way around

```java
// Goal: keep saving until we have 100
while (money > 100) { ... }   // ❌ never runs (money starts at 0)
while (money < 100) { ... }   // ✅
```

👉 Read the condition aloud: "**As long as** money is less than 100, keep going."

### Mistake 5: Declaring the variable inside the loop

```java
while (count < 5) {
    int count = 0;   // ❌ error: count isn't known in the condition, and it would reset every round
    count++;
}
```

**Fix:** Declare it **before** the loop.

---

## ✅ Summary

- `while (condition) { ... }` repeats **as long as** the condition is true. It checks **first** — it may run **0** times.
- `do { ... } while (condition);` runs the body **first**, then checks — it runs **at least once**. Don't forget the `;`!
- Use `for` when you **know** how many times. Use `while` when you **don't**.
- `while (true)` + `break` is good when the stop decision is in the middle.
- A **flag** is a `boolean` that remembers if something happened.
- Always change something inside the loop, so the condition becomes **false** one day. Otherwise: **infinite loop**!

---

## ❓ Quiz

1. What is the main difference between `while` and `do ... while`?
2. When is `while` better than `for`?
3. What is wrong here? `int i = 0; while (i < 3) { System.out.println(i); }`
4. How many times does the body run? `int x = 10; while (x < 10) { x++; }`
5. How many times does the body run? `int x = 10; do { x++; } while (x < 10);`
6. What must every `while (true)` loop have?
7. What does `number % 10` give? And `number / 10`? (for `number = 365`)

<details>
<summary>Click to see the answers</summary>

1. `while` checks **before** the body (may run 0 times). `do ... while` checks **after** the body (runs at least once).
2. When you **don't know** how many times the loop must run.
3. `i` never changes → infinite loop. Add `i++;` inside.
4. **0** times.
5. **1** time.
6. A `break` (an exit) that will surely be reached.
7. `5` (the last digit) and `36` (the number without the last digit).

</details>

---

[⬅ Previous chapter](12-for-loop.md) | [Table of Contents](../README.md) | [Next chapter: Arrays ➡](14-arrays.md)
