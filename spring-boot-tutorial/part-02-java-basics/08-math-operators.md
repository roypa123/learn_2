# Chapter 8 – Math in Java (Operators)

[⬅ Previous chapter](07-data-types.md) | [Table of Contents](../README.md) | [Next chapter ➡](09-strings.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- How to **add, subtract, multiply and divide** in Java
- The big surprise: **`7 / 2` is `3`**, not `3.5` 😮
- What the **remainder** operator `%` is, and why it's so useful
- Short ways to change a variable: `+=`, `-=`, `++`, `--`
- In which **order** Java calculates
- Useful helpers from the **`Math`** class: round, power, square root, random...

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Operator** | A symbol that does something, like `+` or `*`. |
| **Operand** | The values the operator works on. In `3 + 4`, the operands are `3` and `4`. |
| **Expression** | A piece of code that gives a value: `3 + 4`, `price * 2`. |
| **Remainder** | What is **left over** after dividing. 7 ÷ 2 = 3, and **1** is left over. |
| **Increment** | Make bigger by 1. |
| **Decrement** | Make smaller by 1. |
| **Precedence** | Which operator Java calculates **first**. |

---

## 📖 Story: Sharing candy 🍬

You have **7 candies** and **2 friends**.
You give each friend the **same number** of candies.

- Each friend gets **3** candies. → this is **division** `7 / 2 = 3` (in whole numbers)
- **1** candy is left over. → this is the **remainder** `7 % 2 = 1`

Keep this story in mind. It explains the two most surprising operators in Java!

---

## ➕ Part 1: The basic operators

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | add | `5 + 3` | `8` |
| `-` | subtract | `5 - 3` | `2` |
| `*` | multiply | `5 * 3` | `15` |
| `/` | divide | `6 / 3` | `2` |
| `%` | remainder | `7 % 3` | `1` |

> 💡 On a keyboard there is no `×` or `÷`. So Java uses `*` (star) for multiply and `/` (slash) for divide.

```java
public class BasicMath {
    public static void main(String[] args) {
        int a = 10;
        int b = 3;

        System.out.println("a + b = " + (a + b));
        System.out.println("a - b = " + (a - b));
        System.out.println("a * b = " + (a * b));
        System.out.println("a / b = " + (a / b));
        System.out.println("a % b = " + (a % b));
    }
}
```

**Output:**

```
a + b = 13
a - b = 7
a * b = 30
a / b = 3
a % b = 1
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `int a = 10;` `int b = 3;` | Two number boxes. |
| `"a + b = " + (a + b)` | First, Java calculates **inside the brackets**: 10 + 3 = 13. Then it glues the text `"a + b = "` and `13`. |
| `(a / b)` | 10 / 3 → **3**. Not 3.333! (See Part 2.) |
| `(a % b)` | 10 % 3 → **1**. 3 goes into 10 three times (9), and 1 is left. |

### ⚠️ Why the brackets `( )`?

Look what happens **without** brackets:

```java
System.out.println("a + b = " + a + b);
```

**Output:**

```
a + b = 103
```

😱 Why? Java reads **left to right**:
1. `"a + b = " + a` → text + number → glue → `"a + b = 10"`
2. `"a + b = 10" + b` → text + number → glue → `"a + b = 103"`

Once there is **text** on the left, `+` means **glue**, not add.

👉 **Rule:** When you mix text and math, put the math **in brackets**: `"Sum: " + (a + b)`.

---

## ➗ Part 2: The big surprise — integer division

```java
System.out.println(7 / 2);
```

**Output:**

```
3
```

Not `3.5`! 😮

### Why?

`7` is an `int`. `2` is an `int`. When **both** sides are `int`, Java gives an `int` answer. An `int` can't have a decimal part, so Java **cuts it off** (remember the candy story: each friend gets 3 whole candies).

| Calculation | Result | Why |
|---|---|---|
| `7 / 2` | `3` | int / int → int (cut) |
| `7.0 / 2` | `3.5` | double / int → double |
| `7 / 2.0` | `3.5` | int / double → double |
| `7.0 / 2.0` | `3.5` | double / double → double |

👉 **Rule:** If **at least one** side is a `double`, the answer is a `double`.

### How to get `3.5` from two `int` variables

```java
int total = 7;
int people = 2;

double wrong = total / people;           // 3.0  ❌ (cut first, then made double)
double right = (double) total / people;  // 3.5  ✅

System.out.println(wrong);
System.out.println(right);
```

**Output:**

```
3.0
3.5
```

### 🔍 Line by line

| Line | What happens |
|---|---|
| `double wrong = total / people;` | Step 1: `7 / 2` → both int → `3`. Step 2: put 3 into a double box → `3.0`. **Too late!** The .5 is already gone. |
| `double right = (double) total / people;` | Step 1: `(double) total` → `7.0`. Step 2: `7.0 / 2` → double → `3.5`. ✅ |

> ⚠️ This is one of the **most common bugs** in Java, even for experienced programmers. Remember it! 🧠

### Dividing by zero

```java
System.out.println(10 / 0);     // 💥 ArithmeticException: / by zero  (program crashes)
System.out.println(10.0 / 0);   // Infinity  (no crash, but a strange value)
```

👉 Never divide by zero. Check first (Chapter 10 shows how).

---

## 🍬 Part 3: The remainder operator `%`

`%` gives what is **left over** after division. (It is also called **modulo** or **mod**.)

| Calculation | Think | Result |
|---|---|---|
| `7 % 2` | 7 = 2×3 + **1** | `1` |
| `10 % 3` | 10 = 3×3 + **1** | `1` |
| `12 % 4` | 12 = 4×3 + **0** | `0` |
| `5 % 7` | 5 = 7×0 + **5** | `5` |
| `17 % 5` | 17 = 5×3 + **2** | `2` |

### Why is `%` so useful? 🤩

**Use 1: Is a number even or odd?**

```java
int number = 14;
System.out.println(number % 2);   // 0 → even
number = 15;
System.out.println(number % 2);   // 1 → odd
```

If `number % 2` is `0`, the number is **even**. If it's `1`, it's **odd**.

**Use 2: Change minutes into hours and minutes**

```java
int totalMinutes = 135;
int hours = totalMinutes / 60;     // 2
int minutes = totalMinutes % 60;   // 15

System.out.println(totalMinutes + " minutes = " + hours + " hours and " + minutes + " minutes");
```

**Output:**

```
135 minutes = 2 hours and 15 minutes
```

### 🔍 Line by line

| Line | Calculation | Value |
|---|---|---|
| `int hours = totalMinutes / 60;` | 135 / 60 → int division | `2` |
| `int minutes = totalMinutes % 60;` | 135 % 60 → 135 − 120 | `15` |

**Use 3: Get the last digit of a number**

```java
int n = 4729;
System.out.println(n % 10);    // 9  (last digit)
System.out.println(n / 10);    // 472  (number without the last digit)
```

---

## ✏️ Part 4: Short ways to change a variable

You already know this:

```java
score = score + 10;
```

This is so common that Java has a **shorter** way:

```java
score += 10;
```

Both lines do **exactly the same**: "add 10 to score".

| Short form | Long form | Meaning |
|---|---|---|
| `x += 5;` | `x = x + 5;` | add 5 |
| `x -= 5;` | `x = x - 5;` | subtract 5 |
| `x *= 5;` | `x = x * 5;` | multiply by 5 |
| `x /= 5;` | `x = x / 5;` | divide by 5 |
| `x %= 5;` | `x = x % 5;` | remainder after dividing by 5 |

```java
public class ShortForms {
    public static void main(String[] args) {
        int money = 100;
        System.out.println("Start: " + money);

        money += 50;
        System.out.println("After += 50: " + money);

        money -= 30;
        System.out.println("After -= 30: " + money);

        money *= 2;
        System.out.println("After *= 2: " + money);

        money /= 4;
        System.out.println("After /= 4: " + money);
    }
}
```

**Output:**

```
Start: 100
After += 50: 150
After -= 30: 120
After *= 2: 240
After /= 4: 60
```

`+=` also works with text:

```java
String message = "Hello";
message += " World";
System.out.println(message);   // Hello World
```

---

## ⬆️ Part 5: `++` and `--` (add 1, subtract 1)

Adding **1** is **so** common that it has an even shorter form:

| Short | Same as | Meaning |
|---|---|---|
| `x++;` | `x = x + 1;` | increment (make bigger by 1) |
| `x--;` | `x = x - 1;` | decrement (make smaller by 1) |

```java
int steps = 0;
steps++;
steps++;
steps++;
System.out.println(steps);   // 3

int lives = 3;
lives--;
System.out.println(lives);   // 2
```

### `x++` vs. `++x` (advanced, but good to know)

Both add 1. The difference is only **when** you use them **inside** another expression:

```java
int a = 5;
int b = a++;   // b gets the OLD value (5), THEN a becomes 6

int c = 5;
int d = ++c;   // c becomes 6 FIRST, THEN d gets the new value (6)

System.out.println(a + " " + b);   // 6 5
System.out.println(c + " " + d);   // 6 6
```

| | Name | Order |
|---|---|---|
| `a++` | post-increment | **use** first, **then** add 1 |
| `++a` | pre-increment | **add 1** first, **then** use |

👉 **Beginner tip:** To keep things simple, write `x++;` **alone on its own line**. Then there's no difference and no confusion. 😊

---

## 🧮 Part 6: Order of calculation (precedence)

What is `2 + 3 * 4`?

- If you go left to right: (2 + 3) × 4 = **20** ❌
- Java's answer: 2 + (3 × 4) = **14** ✅

Java follows the same rules as math class:

| Order | Operators | Example |
|---|---|---|
| 1️⃣ First | `( )` brackets | `(2 + 3) * 4` = 20 |
| 2️⃣ Then | `*` `/` `%` (left to right) | `10 - 6 / 2` = 7 |
| 3️⃣ Last | `+` `-` (left to right) | `10 - 3 + 2` = 9 |

```java
System.out.println(2 + 3 * 4);       // 14
System.out.println((2 + 3) * 4);     // 20
System.out.println(10 - 6 / 2);      // 7
System.out.println(20 / 4 * 2);      // 10   (left to right: 5 * 2)
System.out.println(10 % 3 + 1);      // 2    (1 + 1)
```

👉 **Tip:** If you're not sure, **use brackets**. They make your code clearer for humans too.

```java
// Average of 3 numbers
double average = (a + b + c) / 3.0;    // ✅ brackets needed!
double wrong   = a + b + c / 3.0;      // ❌ only c is divided
```

---

## 🧰 Part 7: The `Math` helper class

Java has a ready-made class called `Math` with many useful methods. You don't need to install anything.

| Method | What it does | Example | Result |
|---|---|---|---|
| `Math.max(a, b)` | the **bigger** of two numbers | `Math.max(4, 9)` | `9` |
| `Math.min(a, b)` | the **smaller** of two numbers | `Math.min(4, 9)` | `4` |
| `Math.abs(x)` | remove the minus (**absolute value**) | `Math.abs(-7)` | `7` |
| `Math.pow(a, b)` | a to the **power** of b (a×a×a...) | `Math.pow(2, 3)` | `8.0` |
| `Math.sqrt(x)` | **square root** | `Math.sqrt(25)` | `5.0` |
| `Math.round(x)` | round to the **nearest** whole number | `Math.round(2.5)` | `3` |
| `Math.floor(x)` | round **down** | `Math.floor(2.9)` | `2.0` |
| `Math.ceil(x)` | round **up** | `Math.ceil(2.1)` | `3.0` |
| `Math.random()` | a random decimal from 0.0 up to (not including) 1.0 | `Math.random()` | e.g. `0.7134...` |
| `Math.PI` | the number π | `Math.PI` | `3.141592653589793` |

> 💡 *floor* = the floor of a room (down ⬇️). *ceil* = ceiling (up ⬆️).

### Example: area of a circle ⭕

```java
public class Circle {
    public static void main(String[] args) {
        double radius = 3;
        double area = Math.PI * Math.pow(radius, 2);

        System.out.println("Radius: " + radius);
        System.out.println("Area: " + area);
        System.out.println("Area (rounded): " + Math.round(area));
    }
}
```

**Output:**

```
Radius: 3.0
Area: 28.274333882308138
Area (rounded): 28
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `double radius = 3;` | The radius. The `int` 3 becomes `3.0` automatically. |
| `Math.pow(radius, 2)` | radius × radius = 9.0 |
| `Math.PI * ...` | π × 9.0 = 28.27... |
| `Math.round(area)` | 28.27... → nearest whole number → `28` |

### Example: roll a dice 🎲

```java
int dice = (int) (Math.random() * 6) + 1;
System.out.println("You rolled: " + dice);
```

### 🔍 Step by step

| Step | Code | Possible values |
|---|---|---|
| 1 | `Math.random()` | 0.0 ... 0.999 |
| 2 | `Math.random() * 6` | 0.0 ... 5.999 |
| 3 | `(int) (...)` | 0, 1, 2, 3, 4, 5 (cut the decimals) |
| 4 | `+ 1` | 1, 2, 3, 4, 5, 6 🎲 |

Run it many times. You get a different number each time!

### Round to 2 decimal places (money style)

```java
double price = 12.3456;
double rounded = Math.round(price * 100) / 100.0;
System.out.println(rounded);   // 12.35
```

| Step | Value |
|---|---|
| `price * 100` | 1234.56 |
| `Math.round(...)` | 1235 |
| `/ 100.0` | 12.35 (use `100.0`, not `100`, to avoid integer division!) |

---

## 💻 Mini project: Restaurant bill 🍽️

```java
public class RestaurantBill {
    public static void main(String[] args) {
        double foodPrice = 45.50;
        double drinkPrice = 8.00;
        int tipPercent = 10;
        int people = 3;

        double subtotal = foodPrice + drinkPrice;
        double tip = subtotal * tipPercent / 100;
        double total = subtotal + tip;
        double perPerson = total / people;

        System.out.println("Subtotal:   " + subtotal);
        System.out.println("Tip (" + tipPercent + "%): " + tip);
        System.out.println("Total:      " + total);
        System.out.println("Per person: " + Math.round(perPerson * 100) / 100.0);
    }
}
```

**Output:**

```
Subtotal:   53.5
Tip (10%): 5.35
Total:      58.85
Per person: 19.62
```

### 🔍 Line by line

| Line | Calculation | Value |
|---|---|---|
| `double subtotal = foodPrice + drinkPrice;` | 45.50 + 8.00 | 53.5 |
| `double tip = subtotal * tipPercent / 100;` | 53.5 × 10 = 535.0, then / 100 | 5.35 |
| `double total = subtotal + tip;` | 53.5 + 5.35 | 58.85 |
| `double perPerson = total / people;` | 58.85 / 3 | 19.6166... |
| `Math.round(perPerson * 100) / 100.0` | round to 2 decimals | 19.62 |

> 💡 Why is `tip` correct even though `tipPercent` and `100` are `int`? Because Java goes left to right: `subtotal * tipPercent` is **double** × int = **double** (535.0). Then `535.0 / 100` is double / int = **double**. ✅

---

## ✋ Try it yourself

**Task 1:** What does each line print? Think first, then test.

```java
System.out.println(9 / 2);
System.out.println(9 % 2);
System.out.println(9.0 / 2);
System.out.println(2 + 2 * 2);
System.out.println((2 + 2) * 2);
System.out.println(1 + 2 + "3");
System.out.println("1" + 2 + 3);
```

<details>
<summary>Click to see the answers</summary>

```
4
1
4.5
6
8
33
123
```

The last two: `1 + 2` = 3 (numbers), then `3 + "3"` = `"33"`. But `"1" + 2` = `"12"` (text first!), then `"12" + 3` = `"123"`.

</details>

**Task 2:** Change **seconds** into hours, minutes and seconds. Example: `3725` seconds → `1 hours, 2 minutes, 5 seconds`.

<details>
<summary>Click to see the answer</summary>

```java
public class TimeConverter {
    public static void main(String[] args) {
        int totalSeconds = 3725;

        int hours = totalSeconds / 3600;
        int rest = totalSeconds % 3600;
        int minutes = rest / 60;
        int seconds = rest % 60;

        System.out.println(hours + " hours, " + minutes + " minutes, " + seconds + " seconds");
    }
}
```

`3725 / 3600 = 1`, `3725 % 3600 = 125`, `125 / 60 = 2`, `125 % 60 = 5`.

</details>

**Task 3:** Temperature converter. Change `30` degrees Celsius to Fahrenheit. Formula: **F = C × 9 / 5 + 32**. (Answer: 86.0)

<details>
<summary>Click to see the answer</summary>

```java
double celsius = 30;
double fahrenheit = celsius * 9 / 5 + 32;
System.out.println(celsius + " C = " + fahrenheit + " F");
```

Output: `30.0 C = 86.0 F`

</details>

**Task 4:** Make a program that rolls **two** dice and prints both numbers and the sum.

---

## ⚠️ Common mistakes

### Mistake 1: Integer division

```java
double half = 1 / 2;      // 0.0 ❌
double half = 1.0 / 2;    // 0.5 ✅
```

### Mistake 2: Forgetting brackets with text

```java
System.out.println("Total: " + 5 + 5);     // Total: 55 ❌
System.out.println("Total: " + (5 + 5));   // Total: 10 ✅
```

### Mistake 3: Wrong order of calculation

```java
double avg = 80 + 90 / 2;      // 125.0 ❌ (only 90 is divided)
double avg = (80 + 90) / 2.0;  // 85.0 ✅
```

### Mistake 4: Using `^` for power

```java
int x = 2 ^ 3;              // 1 ❌ (^ means something else in Java!)
double x = Math.pow(2, 3);  // 8.0 ✅
```

### Mistake 5: `Math.pow` gives a `double`

```java
int x = Math.pow(2, 3);         // ❌ error: possible lossy conversion from double to int
int x = (int) Math.pow(2, 3);   // ✅ 8
```

### Mistake 6: Dividing by zero

```java
int people = 0;
int each = 10 / people;   // 💥 ArithmeticException: / by zero
```

Check that `people` is not 0 before dividing (Chapter 10).

---

## ✅ Summary

- Operators: `+` add, `-` subtract, `*` multiply, `/` divide, `%` remainder.
- **int / int = int** — the decimal part is cut: `7 / 2` is `3`. Use `7.0 / 2` or `(double)` to get `3.5`.
- `%` gives the **remainder**: `7 % 2` is `1`. Great for even/odd, time conversion, last digit.
- Short forms: `x += 5`, `x -= 5`, `x *= 5`, `x /= 5`, `x++`, `x--`.
- Order: **brackets** → `* / %` → `+ -`. When in doubt, use brackets.
- With text, `+` **glues**. Put math in brackets: `"Sum: " + (a + b)`.
- `Math` helps: `max`, `min`, `abs`, `pow`, `sqrt`, `round`, `floor`, `ceil`, `random`, `PI`.

---

## ❓ Quiz

1. What is `17 / 5`? What is `17 % 5`?
2. What is `17.0 / 5`?
3. How can you check if a number is even?
4. What is the short form of `count = count + 1;`?
5. What does `3 + 4 * 2` give?
6. How do you calculate 5 to the power of 3 in Java?
7. What is printed? `System.out.println("Age: " + 10 + 2);`
8. What is the difference between `Math.floor(4.7)` and `Math.round(4.7)`?

<details>
<summary>Click to see the answers</summary>

1. `3` and `2`.
2. `3.4`
3. `number % 2 == 0` (if the remainder is 0, it's even). We learn `==` in Chapter 10.
4. `count++;` (or `count += 1;`)
5. `11` (multiplication first: 4 × 2 = 8, then 3 + 8).
6. `Math.pow(5, 3)` → `125.0`
7. `Age: 102`
8. `Math.floor(4.7)` rounds **down** → `4.0`. `Math.round(4.7)` rounds to the **nearest** → `5`.

</details>

---

[⬅ Previous chapter](07-data-types.md) | [Table of Contents](../README.md) | [Next chapter: Strings ➡](09-strings.md)
