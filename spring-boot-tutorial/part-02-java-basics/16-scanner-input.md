# Chapter 16 – Reading What the User Types (`Scanner`)

[⬅ Previous chapter](15-methods.md) | [Table of Contents](../README.md) | [Next chapter ➡](17-comments-clean-code.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- How to read what the user **types** on the keyboard with **`Scanner`**
- How to read **text** (`nextLine`), **whole numbers** (`nextInt`) and **decimals** (`nextDouble`)
- The famous **"skipped input" bug** and how to fix it
- How to check that the user typed a **valid** number
- How to build **interactive programs**: a menu, a quiz, a guessing game 🎮

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Input** | Information that goes **into** the program (for example, from the keyboard). |
| **Output** | Information that comes **out** of the program (for example, on the screen). |
| **Scanner** | A ready-made Java class that **reads** input. |
| **`System.in`** | The **keyboard** (the standard input). The opposite of `System.out` (the screen). |
| **Prompt** | A message that tells the user **what to type**: "Enter your name: " |
| **Object** | A "thing" made from a class with `new`. Our Scanner is an object. (Part 3 explains objects fully.) |
| **Validation** | Checking that the input is **correct** before using it. |

---

## 📖 Story: A conversation 💬

Until now, our programs were like a **TV** 📺: they talk, but you can't answer.

With `Scanner`, the program becomes like a **phone call** 📞: it asks a question, **waits** for your answer, and then continues using what you said.

```
 Program: What is your name?
 You:     Sara             ⌨️
 Program: Hello, Sara! How old are you?
 You:     12               ⌨️
 Program: In 10 years you will be 22.
```

---

## ⌨️ Part 1: Your first Scanner program

```java
import java.util.Scanner;

public class AskName {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("What is your name? ");
        String name = scanner.nextLine();

        System.out.println("Hello, " + name + "! 👋");

        scanner.close();
    }
}
```

**Run it.** The program prints the question and **waits**. ⏳

**In IntelliJ:** click inside the **Run window** at the bottom, type your name, and press **Enter**.

```
What is your name? Sara
Hello, Sara! 👋
```

(Here `Sara` is what **you** typed.)

### 🔍 Line by line

**Line 1:** `import java.util.Scanner;`

| Part | Meaning |
|---|---|
| `import` | "I want to use a class from Java's library." |
| `java.util.Scanner` | The full address of the `Scanner` class. It lives in the package `java.util`. |

Without this line, Java says `cannot find symbol: class Scanner`.

**Line 5:** `Scanner scanner = new Scanner(System.in);`

This line makes a **reading machine** connected to the keyboard.

| Part | Meaning |
|---|---|
| `Scanner` | The **type** of the variable (a class). |
| `scanner` | The **name** of our variable. (Small `s`. You can choose another name, like `input` or `sc`.) |
| `=` | Put into. |
| `new` | "**Make** a new object." 🏭 |
| `Scanner(System.in)` | "...a new Scanner that reads from `System.in` (the keyboard)." |

> 💡 This is the first time we use `new` to make an **object**. Think of the `Scanner` class as a **plan** for a reading machine, and `new Scanner(...)` as **building** one machine from that plan. Part 3 explains this fully. For now, just copy this line. 😊

**Line 7:** `System.out.print("What is your name? ");`

The **prompt**. We use `print` (not `println`) so the user types on the **same line**, right after the question. The space at the end makes it look nice.

**Line 8:** `String name = scanner.nextLine();`

| Part | Meaning |
|---|---|
| `scanner.nextLine()` | "**Wait** until the user types something and presses Enter. Then give me the **whole line** as a String." |
| `String name = ...` | Save what the user typed in `name`. |

**Line 12:** `scanner.close();`

"I'm finished reading. Turn off the machine." 🔌 It's good practice to close it at the end.

---

## 🔢 Part 2: Reading numbers

`nextLine()` always gives a **String**. To get numbers, use:

| Method | Reads | Returns |
|---|---|---|
| `nextLine()` | a whole line of text | `String` |
| `next()` | **one word** (until a space) | `String` |
| `nextInt()` | a whole number | `int` |
| `nextDouble()` | a decimal number | `double` |
| `nextLong()` | a big whole number | `long` |
| `nextBoolean()` | `true` or `false` | `boolean` |

```java
import java.util.Scanner;

public class AgeCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("How old are you? ");
        int age = scanner.nextInt();

        System.out.print("How tall are you (in meters)? ");
        double height = scanner.nextDouble();

        System.out.println("In 10 years you will be " + (age + 10) + " years old.");
        System.out.println("Your height in cm: " + (height * 100));

        scanner.close();
    }
}
```

**Example run:**

```
How old are you? 12
How tall are you (in meters)? 1.52
In 10 years you will be 22 years old.
Your height in cm: 152.0
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `int age = scanner.nextInt();` | Wait for the user to type a whole number. Give it back as an `int`. Now we can do **math** with it! |
| `double height = scanner.nextDouble();` | Same, but for a decimal number. |

> ⚠️ **Comma or dot?** In some countries, computers use a **comma** for decimals (`1,52`). Then `nextDouble()` might expect `1,52` and crash on `1.52`! If this happens, make the scanner always use a dot:
> ```java
> Scanner scanner = new Scanner(System.in).useLocale(java.util.Locale.US);
> ```

---

## 🐛 Part 3: The famous "skipped input" bug

This is the **#1 problem** beginners have with Scanner. Look:

```java
Scanner scanner = new Scanner(System.in);

System.out.print("Enter your age: ");
int age = scanner.nextInt();

System.out.print("Enter your name: ");
String name = scanner.nextLine();

System.out.println("Age: " + age + ", Name: [" + name + "]");
```

**What happens:**

```
Enter your age: 12
Enter your name: Age: 12, Name: []
```

😱 The program **didn't wait** for the name! The name is **empty**!

### 🤔 Why?

When you type `12` and press **Enter**, the keyboard sends: `1`, `2`, and an invisible **Enter** character (`\n`).

```
 What you sent:    [ 1 ][ 2 ][ \n ]
                   └──────┘
 nextInt() takes:    12          ← it takes ONLY the number
                              [ \n ]  ← the Enter stays behind! 😈
```

Then `nextLine()` comes. It reads "everything until the next Enter". But an Enter is **already waiting**! So it reads an **empty** line `""` immediately and doesn't wait for you.

📖 **Story:** You order a pizza 🍕 and a drink 🥤. The waiter brings the pizza but leaves the drink on the counter. The next customer asks for "whatever is on the counter" and gets... your drink, not what they wanted!

### ✅ Fix 1: Eat the leftover Enter

After `nextInt()` (or `nextDouble()`), add an extra `nextLine()` to **clean up**:

```java
System.out.print("Enter your age: ");
int age = scanner.nextInt();
scanner.nextLine();                 // 🧹 eat the leftover Enter

System.out.print("Enter your name: ");
String name = scanner.nextLine();   // ✅ now it waits
```

### ✅ Fix 2 (recommended): Always use `nextLine()` and convert

Read **everything** as a line, then change it into a number yourself (Chapter 7):

```java
System.out.print("Enter your age: ");
int age = Integer.parseInt(scanner.nextLine().strip());

System.out.print("Enter your name: ");
String name = scanner.nextLine();
```

| Part | Meaning |
|---|---|
| `scanner.nextLine()` | Read the whole line, including the Enter. Nothing is left behind. ✅ |
| `.strip()` | Remove extra spaces (if the user typed `" 12 "`). |
| `Integer.parseInt(...)` | Change the text `"12"` into the number `12`. |

👉 In this book we mostly use **Fix 2**. It's simple and you never get the bug.

---

## 🛡️ Part 4: What if the user types something wrong?

What if the program asks for a number, and the user types `hello`? 🙈

```java
int age = scanner.nextInt();   // user types: hello
```

```
Exception in thread "main" java.util.InputMismatchException
```

💥 The program **crashes**. Not nice! Users make mistakes all the time. Let's **check** first.

### Check with `hasNextInt()`

```java
import java.util.Scanner;

public class SafeNumber {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter a number: ");

        while (!scanner.hasNextInt()) {
            String wrong = scanner.nextLine();
            System.out.print("'" + wrong + "' is not a number. Try again: ");
        }

        int number = scanner.nextInt();
        scanner.nextLine();   // eat the Enter

        System.out.println("Thank you! Your number times 2 is " + (number * 2));
        scanner.close();
    }
}
```

**Example run:**

```
Enter a number: hello
'hello' is not a number. Try again: 12abc
'12abc' is not a number. Try again: 21
Thank you! Your number times 2 is 42
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `scanner.hasNextInt()` | "**Look** at what the user typed (but don't take it yet). Is it a whole number?" Returns `true` or `false`. |
| `while (!scanner.hasNextInt())` | "**As long as** it is **not** a number..." |
| `String wrong = scanner.nextLine();` | ...take the wrong input away (throw it out), so we can look at the **next** input. |
| `System.out.print("... Try again: ");` | Ask again. |
| `int number = scanner.nextInt();` | Now we **know** it's a number. Safe to read! ✅ |

There's also `hasNextDouble()`, `hasNextLine()`, `hasNext()`.

> 💡 In Chapter 33 you'll learn another way: `try` / `catch` — "try to do this; if it crashes, do that instead."

### A reusable method for safe numbers

Remember Chapter 15? Let's put this in a **method** so we can use it again and again:

```java
public static int readInt(Scanner scanner, String prompt) {
    System.out.print(prompt);
    while (!scanner.hasNextInt()) {
        scanner.nextLine();
        System.out.print("Please enter a whole number: ");
    }
    int value = scanner.nextInt();
    scanner.nextLine();
    return value;
}
```

Use it:

```java
int age = readInt(scanner, "How old are you? ");
int year = readInt(scanner, "What year is it? ");
```

Clean and safe! 😎

---

## 📋 Part 5: A menu program (with `do ... while`)

Remember the menu from Chapter 13? Now with **real** input:

```java
import java.util.Scanner;

public class MenuProgram {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String choice;

        do {
            System.out.println();
            System.out.println("===== MENU =====");
            System.out.println("1. Say hello");
            System.out.println("2. Tell a joke");
            System.out.println("3. Show the time of day");
            System.out.println("0. Exit");
            System.out.print("Your choice: ");

            choice = scanner.nextLine().strip();

            switch (choice) {
                case "1" -> System.out.println("Hello there! 👋");
                case "2" -> System.out.println("Why do Java developers wear glasses? Because they don't C#! 😄");
                case "3" -> System.out.println("It's always a good time to learn Java! ⏰");
                case "0" -> System.out.println("Goodbye! 👋");
                default -> System.out.println("❗ Unknown choice: " + choice);
            }
        } while (!choice.equals("0"));

        scanner.close();
    }
}
```

**Example run:**

```
===== MENU =====
1. Say hello
2. Tell a joke
3. Show the time of day
0. Exit
Your choice: 2
Why do Java developers wear glasses? Because they don't C#! 😄

===== MENU =====
1. Say hello
2. Tell a joke
3. Show the time of day
0. Exit
Your choice: 0
Goodbye! 👋
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `do { ... } while (...)` | The menu must be shown **at least once**. Perfect for `do ... while`! |
| `choice = scanner.nextLine().strip();` | Read the choice as **text**. Even if the user types `abc`, nothing crashes. |
| `switch (choice)` with `case "1"` | Compare Strings in a switch. |
| `while (!choice.equals("0"))` | Repeat until the user types `0`. |

---

## 💻 Mini project 1: The guessing game (you play!) 🎯

```java
import java.util.Scanner;

public class GuessTheNumber {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int secret = (int) (Math.random() * 100) + 1;
        int tries = 0;
        int guess = 0;

        System.out.println("🎲 I'm thinking of a number between 1 and 100.");

        while (guess != secret) {
            guess = readInt(scanner, "Your guess: ");
            tries++;

            if (guess < 1 || guess > 100) {
                System.out.println("Please choose a number from 1 to 100.");
            } else if (guess < secret) {
                System.out.println("Too low! ⬆️");
            } else if (guess > secret) {
                System.out.println("Too high! ⬇️");
            } else {
                System.out.println("🎉 Correct! You found it in " + tries + " tries.");
            }
        }

        if (tries <= 7) {
            System.out.println("🏆 Great job! You're a binary search master!");
        }

        scanner.close();
    }

    public static int readInt(Scanner scanner, String prompt) {
        System.out.print(prompt);
        while (!scanner.hasNextInt()) {
            scanner.nextLine();
            System.out.print("Please enter a whole number: ");
        }
        int value = scanner.nextInt();
        scanner.nextLine();
        return value;
    }
}
```

**Example run:**

```
🎲 I'm thinking of a number between 1 and 100.
Your guess: 50
Too high! ⬇️
Your guess: 25
Too low! ⬆️
Your guess: 37
Too low! ⬆️
Your guess: 43
Too high! ⬇️
Your guess: 40
🎉 Correct! You found it in 5 tries.
🏆 Great job! You're a binary search master!
```

### 🔍 What we used

| Concept | Chapter |
|---|---|
| Variables, `int` | 6, 7 |
| `Math.random()` | 8 |
| `if / else if` | 10 |
| `while` loop | 13 |
| A method (`readInt`) | 15 |
| `Scanner` | 16 (this one!) |

🎉 Look how much you can already do!

---

## 💻 Mini project 2: Shopping list 🛒

```java
import java.util.Scanner;

public class ShoppingList {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("How many items do you want to buy? ");
        int count = Integer.parseInt(scanner.nextLine().strip());

        String[] items = new String[count];
        double[] prices = new double[count];

        for (int i = 0; i < count; i++) {
            System.out.print("Item " + (i + 1) + " name: ");
            items[i] = scanner.nextLine().strip();

            System.out.print("Item " + (i + 1) + " price: ");
            prices[i] = Double.parseDouble(scanner.nextLine().strip());
        }

        double total = 0;
        System.out.println();
        System.out.println("===== YOUR LIST =====");
        for (int i = 0; i < count; i++) {
            System.out.printf("%-10s %6.2f%n", items[i], prices[i]);
            total += prices[i];
        }
        System.out.println("---------------------");
        System.out.printf("%-10s %6.2f%n", "TOTAL", total);

        scanner.close();
    }
}
```

**Example run:**

```
How many items do you want to buy? 3
Item 1 name: Milk
Item 1 price: 1.2
Item 2 name: Bread
Item 2 price: 2.5
Item 3 name: Eggs
Item 3 price: 3.99

===== YOUR LIST =====
Milk         1.20
Bread        2.50
Eggs         3.99
---------------------
TOTAL        7.69
```

### 🔍 New formatting tricks

| Placeholder | Meaning |
|---|---|
| `%-10s` | A String in a space **10** characters wide, pushed to the **left** (`-`). Makes a neat column. |
| `%6.2f` | A decimal number in a space **6** characters wide, with **2** decimals, pushed to the **right**. |

---

## 🖥️ Part 6: Running Scanner programs in the terminal

Scanner programs also work in the terminal (Chapter 5):

```
javac AskName.java
java AskName
What is your name? Sara
Hello, Sara! 👋
```

Or in one step:

```
java AskName.java
```

> 💡 If emojis show as `?` or strange symbols in the Windows terminal, that's only a display problem. The program is fine. IntelliJ's Run window usually shows them correctly.

---

## ✋ Try it yourself

**Task 1:** Ask for two numbers and print their sum, difference, product and quotient (as a decimal).

<details>
<summary>Click to see the answer</summary>

```java
import java.util.Scanner;

public class TwoNumbers {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("First number: ");
        double a = Double.parseDouble(scanner.nextLine().strip());
        System.out.print("Second number: ");
        double b = Double.parseDouble(scanner.nextLine().strip());

        System.out.println("Sum:        " + (a + b));
        System.out.println("Difference: " + (a - b));
        System.out.println("Product:    " + (a * b));
        if (b != 0) {
            System.out.println("Quotient:   " + (a / b));
        } else {
            System.out.println("Quotient:   can't divide by zero");
        }

        scanner.close();
    }
}
```

</details>

**Task 2:** Ask for the user's name and birth year. Print: `Hi Sara, you will be 30 in the year 2043.`

**Task 3:** Make a **quiz** with 3 questions. Count the correct answers and print the score at the end, like `You got 2 out of 3!`. Use `equalsIgnoreCase` so `"paris"` and `"Paris"` are both correct.

<details>
<summary>Click to see one possible answer</summary>

```java
import java.util.Scanner;

public class Quiz {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int score = 0;

        System.out.print("1. What is the capital of France? ");
        if (scanner.nextLine().strip().equalsIgnoreCase("Paris")) {
            System.out.println("✅ Correct!");
            score++;
        } else {
            System.out.println("❌ The answer is Paris.");
        }

        System.out.print("2. How many legs does a spider have? ");
        if (scanner.nextLine().strip().equals("8")) {
            System.out.println("✅ Correct!");
            score++;
        } else {
            System.out.println("❌ The answer is 8.");
        }

        System.out.print("3. What color do you get by mixing blue and yellow? ");
        if (scanner.nextLine().strip().equalsIgnoreCase("green")) {
            System.out.println("✅ Correct!");
            score++;
        } else {
            System.out.println("❌ The answer is green.");
        }

        System.out.println("You got " + score + " out of 3!");
        scanner.close();
    }
}
```

**Bonus:** Can you put the questions and answers in two **arrays** and use a **loop**? Then adding a 4th question is just one more item in each array!

</details>

**Task 4:** Ask the user to type numbers, one per line. When they type `0`, stop and print the **sum** and the **average** of the numbers (not counting the 0).

**Task 5:** Make a simple calculator: ask for a number, an operator (`+ - * /`) and another number. Use a `switch` to print the result. Repeat until the user types `q` as the operator.

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting the import

```java
Scanner scanner = new Scanner(System.in);   // ❌ error: cannot find symbol  class Scanner
```

**Fix:** `import java.util.Scanner;` at the top. (IntelliJ: **Alt + Enter** on the red word.)

### Mistake 2: The skipped `nextLine()` after `nextInt()`

See Part 3. **Fix:** Add `scanner.nextLine();` after `nextInt()`, or always use `nextLine()` + `parseInt`.

### Mistake 3: Typing text when a number is expected

```
InputMismatchException     (from nextInt)
NumberFormatException      (from Integer.parseInt)
```

**Fix:** Check with `hasNextInt()` (Part 4), or use `try/catch` (Chapter 33).

### Mistake 4: Comparing the input with `==`

```java
String answer = scanner.nextLine();
if (answer == "yes") { }          // ❌ almost never true!
if (answer.equals("yes")) { }     // ✅
```

### Mistake 5: Forgetting to click in the Run window

The program seems "frozen" 🥶 — but it's just **waiting** for you to type! In IntelliJ, click in the Run window at the bottom and type.

### Mistake 6: Making many Scanners

```java
Scanner s1 = new Scanner(System.in);
Scanner s2 = new Scanner(System.in);   // ⚠️ can cause strange problems
```

**Fix:** Make **one** Scanner at the start, and use it everywhere. Pass it to methods as a parameter (like `readInt(scanner, ...)`).

### Mistake 7: Using the Scanner after `close()`

```java
scanner.close();
scanner.nextLine();   // 💥 IllegalStateException: Scanner closed
```

Close it only at the **very end**.

---

## ✅ Summary

- `import java.util.Scanner;` then `Scanner scanner = new Scanner(System.in);`
- Print a **prompt** with `print`, then read:
  - `nextLine()` → whole line (String)
  - `next()` → one word
  - `nextInt()`, `nextDouble()` → numbers
- ⚠️ After `nextInt()`/`nextDouble()`, the **Enter** stays behind. The next `nextLine()` reads it as an empty line.
  - Fix: add an extra `scanner.nextLine();` — **or** always read with `nextLine()` and use `Integer.parseInt(...)`.
- Check input with `hasNextInt()` / `hasNextDouble()` before reading, so wrong input doesn't crash the program.
- Use **one** Scanner for the whole program. `close()` it at the end.
- `do ... while` is perfect for menus.

---

## ❓ Quiz

1. Which line must you write at the top of the file to use Scanner?
2. What is `System.in`?
3. What does `nextLine()` return?
4. A user types `42` and presses Enter. Then the program calls `nextInt()` and then `nextLine()`. What does `nextLine()` return?
5. How can you avoid the problem in question 4? (Give two ways.)
6. What does `hasNextInt()` do?
7. Why is `do ... while` good for a menu?
8. How do you compare the user's answer with `"yes"`?

<details>
<summary>Click to see the answers</summary>

1. `import java.util.Scanner;`
2. The keyboard (standard input).
3. The whole line the user typed, as a `String` (without the Enter).
4. An **empty** String `""` (it reads the Enter that `nextInt()` left behind).
5. (a) Add an extra `scanner.nextLine();` after `nextInt()`. (b) Read everything with `nextLine()` and convert with `Integer.parseInt(...)`.
6. It checks (without reading) if the next input is a whole number. Returns `true` or `false`.
7. Because the menu must be shown **at least once** before we can check the user's choice.
8. `answer.equals("yes")` (or `equalsIgnoreCase` to ignore big/small letters).

</details>

---

[⬅ Previous chapter](15-methods.md) | [Table of Contents](../README.md) | [Next chapter: Comments and clean code ➡](17-comments-clean-code.md)
