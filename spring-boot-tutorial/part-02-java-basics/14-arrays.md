# Chapter 14 – Arrays: Many Boxes in a Row

[⬅ Previous chapter](13-while-loop.md) | [Table of Contents](../README.md) | [Next chapter ➡](15-methods.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What an **array** is, and why we need it
- How to **create** an array (two ways)
- How to **read** and **change** values with an **index**
- How to go through an array with a `for` loop and a **for-each** loop
- Common jobs: **sum**, **average**, **biggest**, **search**, **count**
- The **`Arrays`** helper class: `toString`, `sort`, `fill`, `copyOf`
- **2D arrays** (tables with rows and columns)

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Array** | A row of boxes, all of the **same type**, under **one name**. |
| **Element** | One box (one value) inside the array. |
| **Index** | The position number of an element. Starts at **0**. |
| **Length** | How many elements the array has. It can **never change** after the array is made. |
| **for-each loop** | A short loop that visits **each** element, one by one. |
| **2D array** | An array of arrays — like a table with **rows** and **columns**. |
| **Default value** | The value Java puts in new boxes automatically (`0`, `false`, `null`). |

---

## 📖 Story: The egg box 🥚

You want to save the scores of 5 students. With what you know now, you write:

```java
int score1 = 80;
int score2 = 95;
int score3 = 70;
int score4 = 88;
int score5 = 60;
```

What if you have **500** students? 500 variables?! 😱

An **array** is like an **egg box**: one box with many places, all in a row. Each place has a **number**.

```
 int[] scores = {80, 95, 70, 88, 60};

   ┌────┬────┬────┬────┬────┐
   │ 80 │ 95 │ 70 │ 88 │ 60 │      ← values (elements)
   └────┴────┴────┴────┴────┘
     0    1    2    3    4         ← index
                                   ← name: scores
                                   ← length: 5
```

- **One** name: `scores`
- **Five** values
- Each value has an **index**: 0, 1, 2, 3, 4 (yes, starting at 0 — just like Strings!)

---

## 🛠️ Part 1: Creating an array

### Way 1: With the values you already know

```java
int[] scores = {80, 95, 70, 88, 60};
String[] names = {"Ali", "Sara", "Tom"};
double[] prices = {1.99, 5.50, 3.25};
char[] vowels = {'a', 'e', 'i', 'o', 'u'};
boolean[] answers = {true, false, true};
```

### 🔍 Line by line: `int[] scores = {80, 95, 70, 88, 60};`

| Part | Meaning |
|---|---|
| `int` | The type of **every** element. All elements must be `int`. |
| `[]` | "This is an **array**" (many boxes, not just one). |
| `scores` | The name of the array. Use a **plural** name (`scores`, `names`), because there are many! |
| `=` | Put into. |
| `{80, 95, 70, 88, 60}` | The values, separated by commas, inside `{ }`. |
| `;` | End. |

### Way 2: Empty array with a size

When you know **how many** boxes, but **not** the values yet:

```java
int[] scores = new int[5];
```

| Part | Meaning |
|---|---|
| `new` | "Make a **new** array." |
| `int[5]` | An array of `int` with **5** places. |

What's inside the boxes now? Java fills them with **default values**:

```
   ┌───┬───┬───┬───┬───┐
   │ 0 │ 0 │ 0 │ 0 │ 0 │
   └───┴───┴───┴───┴───┘
     0   1   2   3   4
```

| Type | Default value |
|---|---|
| `int`, `long`, `double`... | `0` (or `0.0`) |
| `boolean` | `false` |
| `char` | an invisible "empty" character |
| `String` (and other objects) | `null` (= "nothing here") |

> ⚠️ **The size is fixed!** An array of 5 boxes stays 5 boxes **forever**. You can't add a 6th. (In Chapter 30 we learn **ArrayList**, which **can** grow.)

---

## 📖 Part 2: Reading and changing elements

### Reading

```java
int[] scores = {80, 95, 70, 88, 60};

System.out.println(scores[0]);   // 80  (first)
System.out.println(scores[2]);   // 70
System.out.println(scores[4]);   // 60  (last)
```

`scores[2]` means "the box at **index 2**" in `scores`. Say it: "scores **at** 2".

### Changing

```java
scores[1] = 100;     // change index 1 from 95 to 100
scores[4] += 5;      // add 5 to index 4 → 65

System.out.println(scores[1]);   // 100
System.out.println(scores[4]);   // 65
```

Each element works **just like a normal variable**. You can use `=`, `+=`, `++` on it.

### Length

```java
System.out.println(scores.length);   // 5
```

> ⚠️ For arrays: `length` with **no** brackets. For Strings: `length()` **with** brackets.

| | Write |
|---|---|
| Array | `scores.length` |
| String | `name.length()` |

### The last element

```java
int last = scores[scores.length - 1];   // scores[4]
```

Same trick as with Strings: the last index is always **length − 1**.

### 💥 Going outside the array

```java
scores[5] = 99;   // 💥 ArrayIndexOutOfBoundsException: Index 5 out of bounds for length 5
```

There is no box number 5! The program crashes. This is one of the **most common** errors. 🐛

---

## 🔁 Part 3: Going through an array with a `for` loop

```java
public class PrintScores {
    public static void main(String[] args) {
        int[] scores = {80, 95, 70, 88, 60};

        for (int i = 0; i < scores.length; i++) {
            System.out.println("Student " + (i + 1) + ": " + scores[i]);
        }
    }
}
```

**Output:**

```
Student 1: 80
Student 2: 95
Student 3: 70
Student 4: 88
Student 5: 60
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `int i = 0` | Start at the first index. |
| `i < scores.length` | Go while `i` is less than 5 → i = 0, 1, 2, 3, 4. ⚠️ `<`, not `<=`! |
| `scores[i]` | The element at position `i`. |
| `(i + 1)` | Humans count from 1, so we show `i + 1` as the student number. |

👉 **This loop is the most important pattern for arrays.** Learn it by heart:

```java
for (int i = 0; i < array.length; i++) {
    // use array[i]
}
```

---

## ✨ Part 4: The for-each loop (shorter!)

When you only need to **read** each element (and you don't need the index), there's a shorter loop:

```java
String[] fruits = {"apple", "banana", "cherry"};

for (String fruit : fruits) {
    System.out.println("I like " + fruit);
}
```

**Output:**

```
I like apple
I like banana
I like cherry
```

### 🔍 Line by line

```
 for ( String   fruit   :   fruits ) {
       ──────   ─────   ─   ──────
         ①        ②     ③     ④
```

| Part | Meaning |
|---|---|
| ① `String` | The type of each element. |
| ② `fruit` | A name for "the current element". Usually the **singular** of the array name: `fruits` → `fruit`. |
| ③ `:` | Read it as "**in**". |
| ④ `fruits` | The array to go through. |

Read the whole line as: "**For each** `fruit` **in** `fruits`..."

### 🆚 Which loop?

| Use the normal `for` when... | Use for-each when... |
|---|---|
| you need the **index** (`i`) | you only need the **values** |
| you want to **change** elements | you only want to **read** |
| you want to go **backwards** or skip some | you go from first to last |

> ⚠️ Changing `fruit` in a for-each loop does **not** change the array:
> ```java
> for (String fruit : fruits) {
>     fruit = "mango";   // only changes the local copy, not the array!
> }
> ```

---

## 🧮 Part 5: Common jobs with arrays

These patterns are used **everywhere**. Practice them! 💪

### Job 1: Sum and average

```java
int[] scores = {80, 95, 70, 88, 60};
int sum = 0;

for (int score : scores) {
    sum += score;
}

double average = (double) sum / scores.length;

System.out.println("Sum: " + sum);           // Sum: 393
System.out.println("Average: " + average);   // Average: 78.6
```

### Job 2: Find the biggest (maximum)

```java
int[] scores = {80, 95, 70, 88, 60};
int max = scores[0];   // start with the FIRST element

for (int i = 1; i < scores.length; i++) {
    if (scores[i] > max) {
        max = scores[i];
    }
}

System.out.println("Highest: " + max);   // Highest: 95
```

### 🔍 Why start with `scores[0]`?

📖 **Story:** You want to find the tallest person in a line. You stand next to the **first** person and say, "You're the tallest so far." Then you walk down the line. Every time you see someone taller, **they** become "the tallest so far". At the end, you have the real tallest. 🧍🧍‍♂️🧍‍♀️

| i | `scores[i]` | `> max`? | `max` |
|---|---|---|---|
| start | | | 80 |
| 1 | 95 | yes | **95** |
| 2 | 70 | no | 95 |
| 3 | 88 | no | 95 |
| 4 | 60 | no | 95 |

> ⚠️ Don't start with `max = 0`. If all numbers are negative (like temperatures `{-5, -2, -9}`), the answer would be 0, which is wrong!

The **smallest** works the same way, with `<` instead of `>`.

### Job 3: Search — is a value in the array?

```java
String[] names = {"Ali", "Sara", "Tom", "Lina"};
String target = "Tom";
int foundAt = -1;   // -1 means "not found" (like indexOf!)

for (int i = 0; i < names.length; i++) {
    if (names[i].equals(target)) {
        foundAt = i;
        break;   // found it, stop looking
    }
}

if (foundAt != -1) {
    System.out.println(target + " found at index " + foundAt);
} else {
    System.out.println(target + " not found");
}
```

**Output:**

```
Tom found at index 2
```

(Remember: Strings → `.equals()`!)

### Job 4: Count

How many scores are 80 or more?

```java
int[] scores = {80, 95, 70, 88, 60};
int count = 0;

for (int score : scores) {
    if (score >= 80) {
        count++;
    }
}

System.out.println(count + " students got 80 or more.");   // 3 students got 80 or more.
```

### Job 5: Change every element

Give every student 5 bonus points:

```java
for (int i = 0; i < scores.length; i++) {
    scores[i] += 5;
}
```

(Here we need the normal `for` loop, because we **change** the array.)

---

## 🧰 Part 6: The `Arrays` helper class

Java has a ready-made helper called `Arrays`. To use it, write this line at the **very top** of your file (before `public class`):

```java
import java.util.Arrays;
```

| Part | Meaning |
|---|---|
| `import` | "I want to use something from Java's library." |
| `java.util.Arrays` | The full "address" of the `Arrays` class. (`java.util` is a **package** — a folder of classes. More in Chapter 26.) |

### Print the whole array

```java
int[] numbers = {5, 3, 9, 1};

System.out.println(numbers);                    // [I@1b6d3586  😵 (strange!)
System.out.println(Arrays.toString(numbers));   // [5, 3, 9, 1] ✅
```

Printing an array directly shows a strange code (its "address" in memory). Always use `Arrays.toString(...)`.

### Sort

```java
int[] numbers = {5, 3, 9, 1};
Arrays.sort(numbers);
System.out.println(Arrays.toString(numbers));   // [1, 3, 5, 9]

String[] names = {"Tom", "Ali", "Sara"};
Arrays.sort(names);
System.out.println(Arrays.toString(names));     // [Ali, Sara, Tom]
```

`Arrays.sort` changes the array itself into order (small → big, or A → Z).

### Fill

```java
int[] board = new int[5];
Arrays.fill(board, 7);
System.out.println(Arrays.toString(board));   // [7, 7, 7, 7, 7]
```

### Copy (and make bigger)

```java
int[] original = {1, 2, 3};
int[] bigger = Arrays.copyOf(original, 5);
System.out.println(Arrays.toString(bigger));   // [1, 2, 3, 0, 0]
```

`copyOf` makes a **new** array with a new length. (This is how you "grow" an array — you make a new, bigger one.)

### Compare

```java
int[] a = {1, 2, 3};
int[] b = {1, 2, 3};

System.out.println(a == b);               // false  (two different arrays)
System.out.println(Arrays.equals(a, b));  // true   (same values)
```

Just like Strings: `==` asks "same object?", `Arrays.equals` asks "same values?".

---

## ⚠️ Part 7: Arrays are shared, not copied!

This surprises everyone. 😮

```java
int[] a = {1, 2, 3};
int[] b = a;        // b is NOT a copy!
b[0] = 99;

System.out.println(a[0]);   // 99 😱
```

### Why?

For `int` variables (Chapter 6), `b = a` **copies the value**.
But an array variable does **not** hold the boxes themselves. It holds an **address** — like a note that says "the egg box is on the kitchen table".

```
   a ──────┐
           ├────►  ┌────┬───┬───┐
   b ──────┘       │ 99 │ 2 │ 3 │    (only ONE array!)
                   └────┴───┴───┘
```

`b = a` copies the **note**, not the egg box. Now both notes point to the **same** box. If you change it through `b`, you see the change through `a` too.

**To make a real copy:**

```java
int[] b = Arrays.copyOf(a, a.length);   // or: int[] b = a.clone();
```

> 💡 This idea is called a **reference**. It's very important for objects in Part 3. Keep it in mind!

---

## 🗺️ Part 8: 2D arrays (tables)

A **2D array** is an array of arrays. Think of a **table** or a **chessboard** ♟️ with rows and columns.

```java
int[][] grid = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};
```

```
            col 0  col 1  col 2
          ┌──────┬──────┬──────┐
   row 0  │  1   │  2   │  3   │
          ├──────┼──────┼──────┤
   row 1  │  4   │  5   │  6   │
          ├──────┼──────┼──────┤
   row 2  │  7   │  8   │  9   │
          └──────┴──────┴──────┘
```

### 🔍 Reading

| Code | Meaning | Value |
|---|---|---|
| `grid[0][0]` | row 0, column 0 | `1` |
| `grid[1][2]` | row 1, column 2 | `6` |
| `grid[2][1]` | row 2, column 1 | `8` |
| `grid.length` | number of **rows** | `3` |
| `grid[0].length` | number of **columns** (in row 0) | `3` |

👉 Always **[row][column]**. Like a cinema seat: first the **row**, then the **seat number**. 🎬

### Go through all elements (nested loops!)

```java
for (int row = 0; row < grid.length; row++) {
    for (int col = 0; col < grid[row].length; col++) {
        System.out.print(grid[row][col] + " ");
    }
    System.out.println();
}
```

**Output:**

```
1 2 3
4 5 6
7 8 9
```

### Empty 2D array

```java
int[][] seats = new int[3][4];   // 3 rows, 4 columns, all 0
seats[1][2] = 1;                 // book the seat at row 1, column 2
```

---

## 💻 Mini project: Weekly temperatures 🌡️

```java
import java.util.Arrays;

public class Temperatures {
    public static void main(String[] args) {
        String[] days = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"};
        double[] temps = {21.5, 23.0, 19.8, 25.4, 27.1, 24.6, 20.3};

        double sum = 0;
        int hottestIndex = 0;
        int coldestIndex = 0;

        for (int i = 0; i < temps.length; i++) {
            sum += temps[i];

            if (temps[i] > temps[hottestIndex]) {
                hottestIndex = i;
            }
            if (temps[i] < temps[coldestIndex]) {
                coldestIndex = i;
            }
        }

        double average = sum / temps.length;

        System.out.println("=== Weekly Report ===");
        for (int i = 0; i < days.length; i++) {
            String mark = temps[i] > average ? " ☀️ above average" : "";
            System.out.printf("%s: %.1f°C%s%n", days[i], temps[i], mark);
        }
        System.out.printf("Average: %.1f°C%n", average);
        System.out.println("Hottest: " + days[hottestIndex] + " (" + temps[hottestIndex] + "°C)");
        System.out.println("Coldest: " + days[coldestIndex] + " (" + temps[coldestIndex] + "°C)");

        double[] sorted = Arrays.copyOf(temps, temps.length);
        Arrays.sort(sorted);
        System.out.println("Sorted: " + Arrays.toString(sorted));
    }
}
```

**Output:**

```
=== Weekly Report ===
Mon: 21.5°C
Tue: 23.0°C
Wed: 19.8°C
Thu: 25.4°C ☀️ above average
Fri: 27.1°C ☀️ above average
Sat: 24.6°C ☀️ above average
Sun: 20.3°C
Average: 23.1°C
Hottest: Fri (27.1°C)
Coldest: Wed (19.8°C)
Sorted: [19.8, 20.3, 21.5, 23.0, 24.6, 25.4, 27.1]
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `days` and `temps` | Two arrays that "match": `days[3]` and `temps[3]` are about the same day (Thursday). These are called **parallel arrays**. |
| `hottestIndex` | We remember the **index** (not just the value), so we can also find the day name. |
| `Arrays.copyOf(...)` then `sort` | We sort a **copy**, so the original order (Mon–Sun) is kept. |

---

## ✋ Try it yourself

**Task 1:** Make an array with 5 of your favorite foods. Print them with a for-each loop, like `1. Pizza`, `2. Rice`... (Hint: you need a counter, or use a normal `for`.)

**Task 2:** Find the **smallest** number in `{42, 7, 19, 3, 88, 25}`.

<details>
<summary>Click to see the answer</summary>

```java
int[] numbers = {42, 7, 19, 3, 88, 25};
int min = numbers[0];

for (int n : numbers) {
    if (n < min) {
        min = n;
    }
}

System.out.println("Smallest: " + min);   // 3
```

</details>

**Task 3:** Print an array **backwards**: `{1, 2, 3, 4, 5}` → `5 4 3 2 1`.

<details>
<summary>Click to see the answer</summary>

```java
int[] numbers = {1, 2, 3, 4, 5};
for (int i = numbers.length - 1; i >= 0; i--) {
    System.out.print(numbers[i] + " ");
}
```

</details>

**Task 4:** Count how many **even** numbers are in `{3, 8, 12, 5, 7, 10, 1}`. (Answer: 3)

**Task 5:** Make a 3×3 tic-tac-toe board ❌⭕ as a `char[][]`, filled with `'-'`. Put an `'X'` in the middle and an `'O'` in the top-left corner. Print the board.

<details>
<summary>Click to see the answer</summary>

```java
char[][] board = new char[3][3];

for (int r = 0; r < 3; r++) {
    for (int c = 0; c < 3; c++) {
        board[r][c] = '-';
    }
}

board[1][1] = 'X';
board[0][0] = 'O';

for (int r = 0; r < 3; r++) {
    for (int c = 0; c < 3; c++) {
        System.out.print(board[r][c] + " ");
    }
    System.out.println();
}
```

Output:
```
O - -
- X -
- - -
```

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Index out of bounds

```java
int[] a = new int[3];
a[3] = 10;   // 💥 ArrayIndexOutOfBoundsException: Index 3 out of bounds for length 3
```

Valid indexes are **0 to length − 1** (here: 0, 1, 2).

### Mistake 2: `<=` in the loop

```java
for (int i = 0; i <= a.length; i++)   // ❌ crashes at the last round
for (int i = 0; i < a.length; i++)    // ✅
```

### Mistake 3: `length()` on an array

```java
a.length()   // ❌ error: cannot find symbol
a.length     // ✅
```

### Mistake 4: Printing an array directly

```java
System.out.println(a);                    // [I@6d06d69c ❌
System.out.println(Arrays.toString(a));   // [0, 0, 0] ✅
```

### Mistake 5: Forgetting `import java.util.Arrays;`

```java
Arrays.sort(a);   // ❌ error: cannot find symbol  (symbol: variable Arrays)
```

**Fix:** Add `import java.util.Arrays;` at the top of the file.
(In IntelliJ: click on the red word and press **Alt + Enter** → **Import class**. 🪄)

### Mistake 6: Mixing types

```java
int[] numbers = {1, 2, "three"};   // ❌ error: String cannot be converted to int
```

All elements must be the **same** type.

### Mistake 7: Thinking `b = a` makes a copy

See Part 7. Use `Arrays.copyOf` or `.clone()`.

### Mistake 8: Using a `null` element

```java
String[] names = new String[3];
System.out.println(names[0].length());   // 💥 NullPointerException
```

`names[0]` is `null` (empty). Put a String in it first: `names[0] = "Ali";`

---

## ✅ Summary

- An **array** keeps many values of the **same type** under one name.
- Create: `int[] a = {1, 2, 3};` or `int[] a = new int[5];` (filled with default values).
- Read/change: `a[0]`, `a[2] = 10;`. The index goes from **0** to **length − 1**.
- Length: `a.length` (no brackets). The size **never changes**.
- Loop: `for (int i = 0; i < a.length; i++)` or for-each: `for (int x : a)`.
- Patterns: sum, average, max/min (start with `a[0]`), search (use `-1` for "not found"), count.
- `Arrays.toString`, `Arrays.sort`, `Arrays.fill`, `Arrays.copyOf`, `Arrays.equals` — need `import java.util.Arrays;`
- `b = a` does **not** copy an array — both names point to the **same** array.
- 2D array: `int[][] grid`, use `grid[row][col]`, loop with nested loops.

---

## ❓ Quiz

1. What is the index of the first element of an array?
2. `int[] a = new int[4];` — What is in `a[2]`?
3. How do you get the number of elements in array `a`?
4. `int[] a = {10, 20, 30};` — What is `a[a.length - 1]`?
5. What happens with `a[3]` for the array in question 4?
6. How do you print an array nicely?
7. What does this print? `int[] a = {1, 2}; int[] b = a; b[1] = 5; System.out.println(a[1]);`
8. In `int[][] m = new int[2][5];`, how many rows and columns are there?
9. When should you **not** use a for-each loop?

<details>
<summary>Click to see the answers</summary>

1. `0`
2. `0` (the default value for `int`).
3. `a.length`
4. `30`
5. The program crashes with `ArrayIndexOutOfBoundsException`.
6. `System.out.println(Arrays.toString(a));` (with `import java.util.Arrays;`)
7. `5` — `a` and `b` point to the same array.
8. 2 rows and 5 columns.
9. When you need the index, when you want to change the elements, or when you want to go backwards.

</details>

---

[⬅ Previous chapter](13-while-loop.md) | [Table of Contents](../README.md) | [Next chapter: Methods ➡](15-methods.md)
