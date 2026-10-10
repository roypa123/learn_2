# Chapter 17 – Comments, Clean Code and the Debugger

[⬅ Previous chapter](16-scanner-input.md) | [Table of Contents](../README.md) | [Next chapter ➡](../part-03-objects/18-classes-and-objects.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- The **3 kinds of comments** in Java: `//`, `/* */`, `/** */`
- **When** to write a comment, and when **not** to
- Java's **naming rules** for classes, methods, variables and constants
- How to make code **clean**: good names, no "magic numbers", small methods
- IntelliJ's helpers: **reformat**, **rename**, **extract method**
- How to use the **debugger** to watch your program step by step 🔍
- A big **Part 2 review project** 🎓

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Comment** | A note for **humans** inside the code. Java ignores it. |
| **Javadoc** | Special comments `/** */` that describe a class or method. Tools can turn them into web pages. |
| **Clean code** | Code that is **easy to read** and **easy to change**. |
| **Magic number** | A number in the code with **no explanation**, like `0.19` or `86400`. |
| **Constant** | A `final` variable whose value never changes. |
| **Refactoring** | Making code **cleaner** without changing what it does. |
| **Debugger** | A tool that lets you **pause** the program and look inside. |
| **Breakpoint** | A **stop sign** 🛑 you put on a line. The debugger pauses there. |

---

## 📖 Story: The messy kitchen 🍳

Two cooks make the **same** soup. 🍲

- **Cook A** throws everything everywhere. No labels on the jars. Dirty pots on the floor. The soup tastes fine — but **nobody else** can work in that kitchen. Even Cook A gets lost the next day!
- **Cook B** labels every jar, cleans as they go, and keeps a recipe card. Anyone can come in and help.

Code is the same. The computer doesn't care if your code is messy. But **humans** do — your teammates, and **you in 3 months**. 😅

> 💬 "Any fool can write code that a computer can understand. Good programmers write code that **humans** can understand." — Martin Fowler

---

## 💬 Part 1: Three kinds of comments

### 1️⃣ Single-line comment `//`

Everything after `//` until the end of the line is ignored by Java:

```java
// Calculate the price with tax
double total = price * 1.2;

int age = 25;   // a comment can also be at the end of a line
```

### 2️⃣ Multi-line comment `/* ... */`

Everything between `/*` and `*/` is ignored, even over many lines:

```java
/*
   This program calculates the monthly
   payment for a loan.
   Written by: Sara, 2025
*/
```

### 3️⃣ Javadoc comment `/** ... */`

A special comment for **describing** classes and methods. It starts with **two** stars `/**`:

```java
/**
 * Calculates the area of a rectangle.
 *
 * @param width  the width of the rectangle
 * @param height the height of the rectangle
 * @return the area (width times height)
 */
public static double area(double width, double height) {
    return width * height;
}
```

| Part | Meaning |
|---|---|
| `/**` | Start of a Javadoc comment. |
| First sentence | A short description of **what** the method does. |
| `@param width ...` | Describes a **parameter**. |
| `@return ...` | Describes what the method **returns**. |
| `*/` | End. |

💡 **IntelliJ bonus:** Type `/**` above a method and press **Enter**. IntelliJ writes the `@param` and `@return` lines for you! And when you **hover** your mouse over a method call anywhere, IntelliJ shows its Javadoc in a little popup. 🪄

👉 When you hover over `System.out.println` or `String.substring` in IntelliJ, the help you see **is** Javadoc, written by the Java team!

### 🔇 Using comments to turn code off

A comment can **temporarily** switch off code, for testing:

```java
System.out.println("Line 1");
// System.out.println("Line 2");   ← this line won't run
System.out.println("Line 3");
```

⌨️ **Shortcut:** Select lines and press **Ctrl + /** (Mac: **Cmd + /**) to comment them on/off.

---

## 🤔 Part 2: Good comments vs. bad comments

### ❌ Bad: saying **what** the code already says

```java
i++;              // add 1 to i
int age = 25;     // set age to 25
```

These comments are **useless**. The code already says it clearly. They just add noise. 📢

### ✅ Good: explaining **why**

```java
// Use 7 tries because binary search finds any number 1–100 in at most 7 guesses.
int maxTries = 7;

// The bank's API counts months from 0 (January = 0), so we add 1.
int month = apiMonth + 1;
```

These comments explain things the code **can't** say: the **reason**, a warning, a strange rule.

### ❌ Bad: a comment instead of a good name

```java
int d;   // number of days since the start
```

### ✅ Good: a good name — no comment needed

```java
int daysSinceStart;
```

### ❌ Bad: old, wrong comments

```java
// Give 10% discount
double price = original * 0.8;   // 😱 the code gives 20%! Which one is true?
```

A wrong comment is **worse** than no comment. When you change code, update the comment too!

### 📋 Rules for comments

| ✅ Write a comment when... | ❌ Don't write a comment when... |
|---|---|
| you explain **why** something is done | it just repeats **what** the code says |
| there's a **warning** ("don't change this, because...") | a better **name** would explain it |
| there's a strange **business rule** | the code is messy — clean the code instead! |
| you describe a public method (Javadoc) | |

---

## 🏷️ Part 3: Naming rules in Java

Java programmers all over the world follow the **same** naming style. If you follow it too, everyone can read your code easily. 🌍

| What | Style | Examples |
|---|---|---|
| **Class** | **P**ascalCase — every word starts big | `Student`, `BankAccount`, `HelloWorld` |
| **Method** | **c**amelCase — first word small, then big. Usually a **verb**. | `calculateTotal()`, `printReport()`, `isEmpty()` |
| **Variable** | camelCase. Usually a **noun**. | `age`, `firstName`, `totalPrice` |
| **Constant** (`static final`) | UPPER_SNAKE_CASE — all big, `_` between words | `MAX_SIZE`, `TAX_RATE`, `PI` |
| **Package** | all small, often with dots | `com.example.shop` |
| **boolean** | sounds like a yes/no question | `isActive`, `hasChildren`, `canEdit` |

### ✅ Good names vs. 👎 bad names

| 👎 Bad | ✅ Good | Why |
|---|---|---|
| `x` | `price` | says **what** it is |
| `n` | `numberOfStudents` | clear meaning |
| `data` | `customerList` | `data` could be anything |
| `doIt()` | `sendEmail()` | says **what** it does |
| `flag` | `isLoggedIn` | says what the yes/no is about |
| `tmp2` | `previousScore` | |
| `calc()` | `calculateTax()` | no unclear short forms |
| `strName` | `name` | don't put the type in the name |

> 💡 Short names like `i`, `j` are **OK** for small loop counters. Everyone knows what they mean.

---

## 🧹 Part 4: Clean code rules

### Rule 1: No magic numbers 🪄❌

```java
// 👎 What is 0.19? What is 3? Nobody knows!
double total = price + price * 0.19;
if (tries > 3) { ... }
```

```java
// ✅ Give the numbers names
static final double TAX_RATE = 0.19;
static final int MAX_LOGIN_TRIES = 3;

double total = price + price * TAX_RATE;
if (tries > MAX_LOGIN_TRIES) { ... }
```

Now:
1. The code **explains itself**.
2. If the tax changes, you change **one line**.

Constants are usually written at the **top of the class**:

```java
public class Shop {
    static final double TAX_RATE = 0.19;
    static final int MAX_ITEMS = 50;

    public static void main(String[] args) {
        ...
    }
}
```

| Part | Meaning |
|---|---|
| `static` | belongs to the class, so all methods can use it (Chapter 27) |
| `final` | can never change |
| `TAX_RATE` | UPPER_SNAKE_CASE for constants |

### Rule 2: One method = one job

```java
// 👎 One giant method that does everything
public static void main(String[] args) {
    // 80 lines: read input, check input, calculate, print report...
}
```

```java
// ✅ Small methods with clear names
public static void main(String[] args) {
    int[] scores = readScores();
    double average = calculateAverage(scores);
    printReport(scores, average);
}
```

The `main` method now reads like a **table of contents**. 📖 If there's a bug in the average, you know exactly where to look.

👉 **Tip:** If a method doesn't fit on your screen, it's probably too long. Try to keep methods **short** (often under ~20 lines).

### Rule 3: Indent and format

```java
// 👎
public static int max(int a,int b){if(a>b){return a;}
else{return b;}}

// ✅
public static int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

⌨️ **IntelliJ does it for you:** **Ctrl + Alt + L** (Mac: **Cmd + Option + L**). Use it often!

### Rule 4: Avoid deep nesting

```java
// 👎 Hard to follow — like a staircase going right ➡️➡️➡️
if (user != null) {
    if (user.isActive()) {
        if (user.hasPermission()) {
            doTheWork();
        }
    }
}
```

```java
// ✅ "Early return" — check the problems first, then do the work
if (user == null) return;
if (!user.isActive()) return;
if (!user.hasPermission()) return;
doTheWork();
```

### Rule 5: Don't repeat yourself (DRY)

If you see the same 3+ lines in more than one place → make a **method** (Chapter 15).

---

## 🛠️ Part 5: IntelliJ helpers for clean code

| What | Shortcut (Windows) | Shortcut (Mac) | What it does |
|---|---|---|---|
| **Reformat** | `Ctrl + Alt + L` | `Cmd + Option + L` | Fixes spaces and indentation |
| **Rename** | `Shift + F6` | `Shift + F6` | Renames a variable/method **everywhere** it is used. Much safer than doing it by hand! |
| **Extract method** | `Ctrl + Alt + M` | `Cmd + Option + M` | Select some lines → IntelliJ makes them into a new method |
| **Extract constant** | `Ctrl + Alt + C` | `Cmd + Option + C` | Select a magic number → IntelliJ makes it a constant |
| **Extract variable** | `Ctrl + Alt + V` | `Cmd + Option + V` | Select an expression → IntelliJ puts it into a new variable |
| **Show fixes** | `Alt + Enter` | `Option + Enter` | On a red or yellow line: shows quick fixes (add import, etc.) |
| **Optimize imports** | `Ctrl + Alt + O` | `Ctrl + Option + O` | Removes unused `import` lines |

### Try "Rename"

1. Write: `int x = 5; System.out.println(x * 2);`
2. Click on `x`.
3. Press **Shift + F6**.
4. Type `quantity` and press **Enter**.
5. ✨ Every `x` became `quantity`!

### Yellow and gray hints

IntelliJ also **warns** you:

- **Gray** text → "This is not used." (A variable or import you don't need.)
- **Yellow** underline → "This could be better." Hover your mouse to see why.
- **Red** underline → "This is an error." Must fix.

👉 Read these hints. They are like a free teacher sitting next to you! 👩‍🏫

---

## 🐞 Part 6: The debugger — see inside your program

Sometimes the program runs, but the answer is **wrong**, and you don't know why. 🤔

**Beginner way:** Add `System.out.println` everywhere to see the values. It works, but it's messy.

**Pro way:** Use the **debugger**. It lets you **pause** the program and **watch every variable** change, line by line. 🔍

### A program with a bug

```java
public class BuggyAverage {
    public static void main(String[] args) {
        int[] scores = {80, 90, 100};
        int sum = 0;

        for (int i = 1; i < scores.length; i++) {
            sum += scores[i];
        }

        double average = (double) sum / scores.length;
        System.out.println("Average: " + average);
    }
}
```

**Output:**

```
Average: 63.333333333333336
```

The average of 80, 90, 100 should be **90**! Where's the bug? Let's use the debugger.

### Step 1: Set a breakpoint 🛑

Click in the **gray area** to the left of the line `int sum = 0;` (next to the line number).
A **red dot** 🔴 appears. This is a **breakpoint**: "Stop here!"

### Step 2: Start debugging 🐞

Instead of the green ▶ Run, click the **bug icon 🐞** (Debug) — or right-click → **Debug 'BuggyAverage.main()'**.

The program starts and **pauses** at your red dot. The line is highlighted in blue.

### Step 3: Look at the variables 👀

At the bottom, the **Debug window** opens. In the **Variables** area you see:

```
 args = {String[0]}
 scores = {int[3]} [80, 90, 100]
```

### Step 4: Step through the code ⏭️

Press **F8** (**Step Over**) to run **one line** and pause again. Watch the variables change:

| Press F8 | Line about to run | `i` | `sum` |
|---|---|---|---|
| 1 | `for (int i = 1; ...` | — | 0 |
| 2 | `sum += scores[i];` | **1** | 0 |
| 3 | (back to the loop) | 1 | **90** |
| ... | | | |

😮 Look! The first time we're inside the loop, `i` is **1**, not 0. So `scores[0]` (80) is **never added**! We found the bug: `int i = 1` should be `int i = 0`.

### 🎮 Debugger buttons

| Button / key | Name | What it does |
|---|---|---|
| **F8** | Step Over | Run this line, stop at the next line. |
| **F7** | Step Into | If the line calls **your** method, go **inside** that method. |
| **Shift + F8** | Step Out | Finish this method and go back to the caller. |
| **F9** | Resume | Continue running until the next breakpoint (or the end). |
| **Ctrl + F2** | Stop | Stop the program. |

👉 **Learn the debugger now.** In Spring Boot, programs are big, and the debugger is your **best friend**. 🐞❤️

---

## 🎓 Part 7: Part 2 review project — Student Grade Manager

This project uses **everything** from Part 2. Read it slowly, and look for each concept.

```java
import java.util.Arrays;
import java.util.Scanner;

/**
 * A small program to enter student grades and show a report.
 */
public class GradeManager {

    static final int PASS_MARK = 50;
    static final int MAX_SCORE = 100;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int count = readIntInRange(scanner, "How many students? ", 1, 30);
        String[] names = new String[count];
        int[] scores = new int[count];

        for (int i = 0; i < count; i++) {
            System.out.print("Name of student " + (i + 1) + ": ");
            names[i] = scanner.nextLine().strip();
            scores[i] = readIntInRange(scanner, "Score of " + names[i] + ": ", 0, MAX_SCORE);
        }

        printReport(names, scores);
        scanner.close();
    }

    /**
     * Reads a whole number from the user. Asks again until the number
     * is a valid int between min and max (both included).
     */
    public static int readIntInRange(Scanner scanner, String prompt, int min, int max) {
        while (true) {
            System.out.print(prompt);
            String line = scanner.nextLine().strip();

            if (!isWholeNumber(line)) {
                System.out.println("❗ Please type a whole number.");
                continue;
            }

            int value = Integer.parseInt(line);
            if (value < min || value > max) {
                System.out.println("❗ Please type a number from " + min + " to " + max + ".");
                continue;
            }

            return value;
        }
    }

    /** Returns true if the text is not empty and has only digits. */
    public static boolean isWholeNumber(String text) {
        if (text.isEmpty() || text.length() > 9) {
            return false;
        }
        for (int i = 0; i < text.length(); i++) {
            if (!Character.isDigit(text.charAt(i))) {
                return false;
            }
        }
        return true;
    }

    /** Returns a letter grade for a score. */
    public static char letterGrade(int score) {
        if (score >= 90) return 'A';
        if (score >= 80) return 'B';
        if (score >= 70) return 'C';
        if (score >= PASS_MARK) return 'D';
        return 'F';
    }

    public static double average(int[] numbers) {
        int sum = 0;
        for (int n : numbers) {
            sum += n;
        }
        return (double) sum / numbers.length;
    }

    /** Returns the index of the highest score. */
    public static int indexOfMax(int[] numbers) {
        int best = 0;
        for (int i = 1; i < numbers.length; i++) {
            if (numbers[i] > numbers[best]) {
                best = i;
            }
        }
        return best;
    }

    public static void printReport(String[] names, int[] scores) {
        System.out.println();
        System.out.println("========== REPORT ==========");
        System.out.printf("%-12s %5s %6s %s%n", "Name", "Score", "Grade", "Result");

        int passed = 0;
        for (int i = 0; i < names.length; i++) {
            boolean pass = scores[i] >= PASS_MARK;
            if (pass) {
                passed++;
            }
            System.out.printf("%-12s %5d %6c %s%n",
                    names[i], scores[i], letterGrade(scores[i]), pass ? "✅ pass" : "❌ fail");
        }

        int best = indexOfMax(scores);
        int[] sorted = Arrays.copyOf(scores, scores.length);
        Arrays.sort(sorted);

        System.out.println("----------------------------");
        System.out.printf("Average:  %.1f%n", average(scores));
        System.out.println("Best:     " + names[best] + " (" + scores[best] + ")");
        System.out.println("Passed:   " + passed + " of " + names.length);
        System.out.println("Sorted:   " + Arrays.toString(sorted));
    }
}
```

**Example run:**

```
How many students? 3
Name of student 1: Sara
Score of Sara: 92
Name of student 2: Tom
Score of Tom: abc
❗ Please type a whole number.
Score of Tom: 150
❗ Please type a number from 0 to 100.
Score of Tom: 45
Name of student 3: Lina
Score of Lina: 78

========== REPORT ==========
Name         Score  Grade Result
Sara            92      A ✅ pass
Tom             45      F ❌ fail
Lina            78      C ✅ pass
----------------------------
Average:  71.7
Best:     Sara (92)
Passed:   2 of 3
Sorted:   [45, 78, 92]
```

### 🔍 Find the concepts! 🕵️

| Concept | Where in the code | Chapter |
|---|---|---|
| Javadoc comments | `/** ... */` above methods | 17 |
| Constants | `PASS_MARK`, `MAX_SCORE` | 6, 17 |
| Variables and types | `int count`, `String line`, `char`, `boolean pass` | 6, 7 |
| Math, integer division fix | `(double) sum / numbers.length` | 8 |
| String methods | `strip()`, `isEmpty()`, `charAt()`, `length()` | 9 |
| `if`, `else`, `&&`, `\|\|`, `!`, ternary | `pass ? "✅ pass" : "❌ fail"` | 10 |
| Early `return` (no deep nesting) | `letterGrade` | 10, 17 |
| `for` loop, for-each | everywhere | 12 |
| `while (true)` + `continue` + `return` | `readIntInRange` | 13 |
| Arrays, parallel arrays, `Arrays.sort` | `names`, `scores` | 14 |
| Methods with parameters and return values | all methods | 15 |
| Scanner, safe input | `readIntInRange` | 16 |
| `printf` formatting | `printReport` | 9 |
| `Character.isDigit` | `isWholeNumber` — checks if a char is `'0'`–`'9'` | new! |

> 💡 Why `text.length() > 9` in `isWholeNumber`? A number with 10+ digits might be **too big** for an `int` (overflow, Chapter 7). `parseInt` would crash. This check keeps us safe.

---

## ✋ Try it yourself

**Task 1:** Clean this code. Give good names, add a constant, format it, and remove useless comments.

```java
public class X {
public static void main(String[] args){
double a=50; // a
double b=a*0.08; // multiply a by 0.08
double c=a+b;
System.out.println(c);}}
```

<details>
<summary>Click to see one possible answer</summary>

```java
public class PriceCalculator {
    static final double SALES_TAX_RATE = 0.08;

    public static void main(String[] args) {
        double price = 50;
        double tax = price * SALES_TAX_RATE;
        double totalPrice = price + tax;
        System.out.println(totalPrice);
    }
}
```

</details>

**Task 2:** In the `GradeManager`, add a method `countGrade(int[] scores, char grade)` that returns how many students got that letter grade. Print how many got `A`.

**Task 3:** Use the **debugger** on the `GradeManager`. Put a breakpoint in `letterGrade`, use **F7** to step **into** it, and watch the `score` variable.

**Task 4:** Write a Javadoc comment for a method `public static boolean isLeapYear(int year)`. Then hover over a call to it in IntelliJ and see your comment appear! ✨

---

## ⚠️ Common mistakes

### Mistake 1: Nested multi-line comments

```java
/* outer
   /* inner */
   this line is NOT a comment anymore! ❌
*/
```

The first `*/` ends the comment. Use `//` for each line instead (Ctrl + /).

### Mistake 2: Forgetting to close `/*`

```java
/* This comment never ends...
public static void main(String[] args) { }   // ❌ all of this is now a comment!
```

### Mistake 3: Comments that lie

Code changes, comments don't. Always **update** comments when you change code — or delete them.

### Mistake 4: Renaming by hand

You rename a variable in 5 places but forget the 6th → error. **Fix:** Use **Shift + F6** in IntelliJ.

### Mistake 5: Running instead of debugging

Breakpoints only work with the **Debug** button 🐞, not the normal **Run** button ▶.

---

## ✅ Summary

- Comments: `//` (one line), `/* */` (many lines), `/** */` (Javadoc for classes and methods).
- Good comments explain **why**. Bad comments repeat **what** the code says.
- A **good name** is better than a comment.
- Naming: `PascalCase` for classes, `camelCase` for methods and variables, `UPPER_SNAKE_CASE` for constants.
- Clean code: no magic numbers (use constants), small methods, one job per method, good formatting, avoid deep nesting, DRY.
- IntelliJ: **Ctrl+Alt+L** (format), **Shift+F6** (rename), **Ctrl+Alt+M** (extract method), **Alt+Enter** (quick fix).
- **Debugger:** set a breakpoint 🔴, click Debug 🐞, step with **F8** / **F7**, watch the variables.

---

## ❓ Quiz

1. Which comment style is used for Javadoc?
2. Is this a good comment? `count++; // add one to count`
3. How should a constant for the maximum number of players be named?
4. What is a magic number? How do you fix it?
5. Which IntelliJ shortcut renames a variable everywhere?
6. What is a breakpoint?
7. What is the difference between **F8** and **F7** in the debugger?
8. Which name is best for a boolean: `status`, `active`, `isActive`?

<details>
<summary>Click to see the answers</summary>

1. `/** ... */`
2. No. It only repeats what the code already says.
3. `MAX_PLAYERS` (as `static final int MAX_PLAYERS = ...;`)
4. A number in the code with no explanation. Fix: put it in a named constant.
5. **Shift + F6**
6. A "stop sign" on a line. When you debug, the program pauses there so you can look at the variables.
7. **F8** (Step Over) runs the line and goes to the next one. **F7** (Step Into) goes **inside** a method that is called on that line.
8. `isActive`

</details>

---

## 🎉 Part 2 complete!

You now know the **basics of Java**:

- ✅ Variables and data types
- ✅ Math and Strings
- ✅ Decisions (`if`, `switch`)
- ✅ Loops (`for`, `while`)
- ✅ Arrays
- ✅ Methods
- ✅ User input
- ✅ Clean code and debugging

This is a **huge** step! 🏔️ Many people give up before here. You didn't. 💪

In **Part 3**, we learn the **most important idea in Java**: **objects and classes**. This is what Spring Boot is built on. Let's go! 🚀

---

[⬅ Previous chapter](16-scanner-input.md) | [Table of Contents](../README.md) | [Next chapter: Classes and objects ➡](../part-03-objects/18-classes-and-objects.md)
