# Chapter 7 – Data Types: What Kind of Thing Is in the Box?

[⬅ Previous chapter](06-variables.md) | [Table of Contents](../README.md) | [Next chapter ➡](08-math-operators.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- The **8 basic types** in Java (called **primitive types**)
- When to use `int`, `long`, `double`, `char` and `boolean`
- Why `String` is a little different
- How to **change** a value from one type to another (**casting**)
- How to turn text into a number (`Integer.parseInt`)

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Data** | Information. Numbers, text, yes/no... |
| **Data type** | The **kind** of data: whole number, decimal number, letter, yes/no, text. |
| **Primitive type** | One of the 8 **basic** types built into Java. Small and simple. Written with **small** letters: `int`, `double`... |
| **Decimal number** | A number with a dot: `3.14`, `0.5`, `19.99`. |
| **Character** | **One** letter, number or symbol: `'A'`, `'7'`, `'?'`. |
| **Boolean** | A value that is only `true` or `false`. Yes or no. |
| **Casting** | Changing a value from one type to another. |
| **Overflow** | A number is too big for its box, and it "goes around" to a wrong value. |

---

## 📖 Story: Different containers in a kitchen

In a kitchen, you use different containers for different things: 🍳

- A **small cup** for coffee ☕
- A **big pot** for soup 🍲
- An **egg box** for eggs 🥚 (only eggs fit well)
- A **light switch** has only two states: **on** or **off** 💡

Java is the same. Every type is a container made for **one kind** of data, and some containers are **bigger** than others.

---

## 🗂️ The 8 primitive types

| Type | What it keeps | Example | Size |
|---|---|---|---|
| `byte` | very small whole number | `100` | tiny (−128 to 127) |
| `short` | small whole number | `20000` | small (−32,768 to 32,767) |
| **`int`** ⭐ | whole number | `25`, `-7`, `1000000` | normal (about −2.1 billion to 2.1 billion) |
| **`long`** ⭐ | **very big** whole number | `8000000000L` | big (about 9 quintillion!) |
| `float` | decimal number (less exact) | `3.14f` | normal |
| **`double`** ⭐ | decimal number (more exact) | `3.14`, `19.99` | big |
| **`char`** ⭐ | **one** character | `'A'`, `'z'`, `'5'` | small |
| **`boolean`** ⭐ | `true` or `false` | `true` | tiny |

⭐ = You will use these **most**. Don't worry about `byte`, `short` and `float` — you will rarely need them.

👉 **Easy rule for beginners:**
- Whole number? → `int` (if it's very big, `long`)
- Decimal number? → `double`
- One letter? → `char`
- Yes/no? → `boolean`
- Text? → `String`

---

## 🔢 Part 1: `int` — whole numbers

```java
public class IntExample {
    public static void main(String[] args) {
        int apples = 12;
        int temperature = -5;
        int population = 1_500_000;

        System.out.println(apples);
        System.out.println(temperature);
        System.out.println(population);
    }
}
```

**Output:**

```
12
-5
1500000
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `int apples = 12;` | A whole number. |
| `int temperature = -5;` | Whole numbers can be **negative** (with `-`). |
| `int population = 1_500_000;` | You can put `_` inside big numbers to make them **easier to read**. Java ignores the `_`. It's the same as `1500000`. |

> ⚠️ **Don't use commas** in numbers: `1,500,000` is an **error** in Java. Use `_` or nothing.

---

## 🔢 Part 2: `long` — very big whole numbers

An `int` can only go up to about **2.1 billion** (2,147,483,647).
The world has about **8 billion** people. That doesn't fit in an `int`! 😱

```java
long worldPopulation = 8_000_000_000L;
System.out.println(worldPopulation);
```

**Output:**

```
8000000000
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `long` | The type for **very big** whole numbers. |
| `8_000_000_000` | 8 billion. |
| `L` | ⚠️ **Important!** It tells Java: "This number is a `long`." Without `L`, Java thinks it's an `int` and says: `error: integer number too large`. Use a **capital** `L` (small `l` looks like the number `1`). |

### 💥 What is overflow?

What happens if an `int` gets **too big**?

```java
int big = 2_147_483_647;   // the biggest int
big = big + 1;
System.out.println(big);
```

**Output:**

```
-2147483648
```

😮 The number **jumped to the most negative** number! This is **overflow**. It's like a car's distance counter going from 999999 back to 000000. 🚗

👉 Java does **not** give an error here. It's a silent bug. So: if a number can be very big (money in cents, time in milliseconds, IDs in a big database), use `long`.

---

## 🔢 Part 3: `double` — decimal numbers

```java
public class DoubleExample {
    public static void main(String[] args) {
        double price = 19.99;
        double pi = 3.14159;
        double height = 1.75;
        double half = 0.5;

        System.out.println(price);
        System.out.println(pi);
        System.out.println(height);
        System.out.println(half);
    }
}
```

**Output:**

```
19.99
3.14159
1.75
0.5
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `double price = 19.99;` | A decimal number. Use a **dot** `.`, never a comma. |
| `double half = 0.5;` | Write the `0` before the dot. (`.5` also works, but `0.5` is clearer.) |

### 🤔 `int` or `double`?

```java
double a = 10;      // ✅ OK — Java makes it 10.0
int b = 10.5;       // ❌ error: possible lossy conversion from double to int
```

| | Why |
|---|---|
| `int` → `double` ✅ | A whole number fits easily in a decimal box. 10 becomes 10.0. Nothing is lost. |
| `double` → `int` ❌ | 10.5 doesn't fit in a whole-number box. The `.5` would be **lost**. Java stops you, to protect you. |

### ⚠️ Decimal numbers are not always exact

```java
System.out.println(0.1 + 0.2);
```

**Output:**

```
0.30000000000000004
```

😲 Not exactly `0.3`! The computer stores decimal numbers in a special way (with 0s and 1s), and some numbers can't be stored **perfectly**. It's like trying to write 1/3 as a decimal: 0.33333... — it never ends.

👉 For normal things (height, weight, temperature) this is fine. For **money** in real apps, programmers use a special class called `BigDecimal` (we'll see it later). For learning, `double` is OK.

### `float` — the smaller brother

```java
float temperature = 36.6f;
```

`float` is like `double`, but **less exact**. You must put `f` at the end. 👉 Just use `double`. It's the normal choice in Java.

---

## 🔤 Part 4: `char` — one character

```java
public class CharExample {
    public static void main(String[] args) {
        char grade = 'A';
        char firstLetter = 'S';
        char digit = '7';
        char symbol = '?';

        System.out.println(grade);
        System.out.println(firstLetter);
        System.out.println(digit);
        System.out.println(symbol);
    }
}
```

**Output:**

```
A
S
7
?
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `char` | The type for **one** character (letter, digit or symbol). |
| `'A'` | ⚠️ **Single** quotes `' '` for `char`. |

### `char` vs. `String` — very important!

| | `char` | `String` |
|---|---|---|
| Quotes | **single** `'A'` | **double** `"A"` |
| How many characters | exactly **one** | zero, one, or many |
| Example | `'S'` | `"Sara"` |

```java
char c = 'AB';     // ❌ error: unclosed character literal  (only ONE character allowed)
char d = "A";      // ❌ error: String cannot be converted to char  (wrong quotes)
String s = 'A';    // ❌ error: char cannot be converted to String
String t = "A";    // ✅
char e = 'A';      // ✅
```

> 💡 **Memory trick:** **One** quote mark `'` → **one** character. **Two** quote marks `"` → text (many characters).

---

## ✅ Part 5: `boolean` — true or false

```java
public class BooleanExample {
    public static void main(String[] args) {
        boolean isRaining = true;
        boolean hasHomework = false;

        System.out.println(isRaining);
        System.out.println(hasHomework);

        boolean isAdult = 20 >= 18;
        System.out.println(isAdult);
    }
}
```

**Output:**

```
true
false
true
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `boolean isRaining = true;` | A yes/no box. The answer is **yes** (`true`). |
| `boolean hasHomework = false;` | The answer is **no** (`false`). |
| `boolean isAdult = 20 >= 18;` | Java **checks**: "Is 20 bigger than or equal to 18?" Yes! So `isAdult` becomes `true`. (`>=` means "bigger than or equal to". More in Chapter 10.) |

> ⚠️ `true` and `false` are written in **small letters** and **without quotes**.
> `"true"` with quotes is a **String**, not a boolean!

> 💡 **Good names for booleans** sound like a yes/no question: `isRaining`, `hasHomework`, `canDrive`, `isLoggedIn`.

👉 Booleans are **very** important. In Chapter 10, we use them to make **decisions** (if it is raining, take an umbrella ☂️).

---

## 📜 Part 6: `String` — text (not primitive)

```java
String greeting = "Good morning!";
String empty = "";
```

`String` is **not** one of the 8 primitive types. How can you see it?

| | Primitive types | `String` |
|---|---|---|
| First letter | **small**: `int`, `double`, `char` | **Capital**: `String` |
| What it is | A simple value | A **class** (a "smart" type with many abilities) |

A String has **abilities** (methods). For example, it can tell you its length:

```java
String name = "Sara";
System.out.println(name.length());   // 4
```

We learn all about Strings in **Chapter 9**, and about classes in **Part 3**.

---

## 🔄 Part 7: Changing types (casting)

### Automatic (widening) — small box → big box ✅

Java does this **automatically**, because nothing is lost:

```java
int small = 100;
long bigger = small;      // int → long ✅
double decimal = small;   // int → double ✅

System.out.println(bigger);    // 100
System.out.println(decimal);   // 100.0
```

```
 byte → short → int → long → float → double
 small ──────────────────────────────► big
```

📦 → 📦📦 Pouring water from a **small** glass into a **big** bucket. No problem! 🥛→🪣

### By hand (narrowing) — big box → small box ⚠️

Java does **not** do this automatically, because something can be **lost**. You must say "I know, do it anyway" by writing the type in brackets:

```java
double price = 9.99;
int wholePrice = (int) price;
System.out.println(wholePrice);
```

**Output:**

```
9
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `(int)` | "**Cast** to int." "Change this into an int, I know data may be lost." |
| `price` | 9.99 |
| Result | `9` — the `.99` is **cut off**. ⚠️ It is **not rounded**! 9.99 becomes 9, not 10. |

🪣 → 🥛 Pouring a **bucket** into a small **glass**: some water spills. 💦

### `char` and `int` — a secret connection 🤫

Every character has a **number** inside the computer:

```java
char letter = 'A';
int code = letter;
System.out.println(code);    // 65

char next = (char) (code + 1);
System.out.println(next);    // B
```

| Line | Meaning |
|---|---|
| `int code = letter;` | `'A'` is stored as the number **65**. |
| `(char) (code + 1)` | 65 + 1 = 66 → cast to char → `'B'`. |

(This list of numbers is called **Unicode**. `'A'` = 65, `'B'` = 66, `'a'` = 97...) You don't need to remember this, just know it exists. 😊

---

## 🔄 Part 8: Text → number (`parseInt`, `parseDouble`)

Sometimes you have a number **as text**, for example `"25"`. You can't do math with text:

```java
String text = "25";
System.out.println(text + 5);   // 255   ← glued, not added! 😮
```

To change text into a real number:

```java
String text = "25";
int number = Integer.parseInt(text);
System.out.println(number + 5);      // 30 ✅

String priceText = "9.99";
double price = Double.parseDouble(priceText);
System.out.println(price * 2);       // 19.98
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `Integer` | A helper class for `int`. |
| `.parseInt(text)` | "**Read** this text and make an `int` from it." (*Parse* means "read and understand".) |
| `Double.parseDouble(...)` | The same, but for `double`. |

> ⚠️ If the text is **not** a number, the program **crashes**:
> ```java
> Integer.parseInt("hello");   // 💥 NumberFormatException: For input string: "hello"
> ```
> In Chapter 33 we learn how to handle this safely.

### Number → text

```java
int age = 25;
String ageText = String.valueOf(age);   // "25"
String alsoText = "" + age;             // "25" (short trick: glue to empty text)
```

---

## ✋ Try it yourself

**Task 1:** Choose the best type for each thing:

1. The number of students in a class
2. Your height in meters (like 1.65)
3. Is the door open?
4. The first letter of your name
5. Your full name
6. The number of stars in the galaxy (about 100,000,000,000)

<details>
<summary>Click to see the answers</summary>

1. `int`
2. `double`
3. `boolean`
4. `char`
5. `String`
6. `long` (too big for `int`)

</details>

**Task 2:** Write a program with **one variable of each** of these types: `int`, `long`, `double`, `char`, `boolean`, `String`. Print them all with a label, like:

```
Age: 30
Distance to sun (km): 150000000000
Height: 1.8
Grade: B
Is student: true
Name: Lina
```

<details>
<summary>Click to see one possible answer</summary>

```java
public class AllTypes {
    public static void main(String[] args) {
        int age = 30;
        long distanceToSun = 150_000_000_000L;
        double height = 1.8;
        char grade = 'B';
        boolean isStudent = true;
        String name = "Lina";

        System.out.println("Age: " + age);
        System.out.println("Distance to sun (km): " + distanceToSun);
        System.out.println("Height: " + height);
        System.out.println("Grade: " + grade);
        System.out.println("Is student: " + isStudent);
        System.out.println("Name: " + name);
    }
}
```

(Real distance to the sun is about 150,000,000 km — but the number is just for practice! 😉)

</details>

**Task 3:** What does each line print?

```java
System.out.println((int) 7.9);
System.out.println((double) 7);
System.out.println("7" + 3);
System.out.println(Integer.parseInt("7") + 3);
```

<details>
<summary>Click to see the answers</summary>

```
7
7.0
73
10
```

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Big number without `L`

```java
long x = 5000000000;   // ❌ error: integer number too large
long x = 5000000000L;  // ✅
```

### Mistake 2: Decimal into `int`

```java
int price = 4.5;        // ❌ error: possible lossy conversion from double to int
double price = 4.5;     // ✅
```

### Mistake 3: Comma in numbers

```java
double price = 4,5;     // ❌ error
double price = 4.5;     // ✅ use a dot
int big = 1,000;        // ❌ error
int big = 1_000;        // ✅
```

### Mistake 4: Wrong quotes for `char`

```java
char c = "A";   // ❌
char c = 'A';   // ✅
```

### Mistake 5: `True` with a capital letter, or `"true"` in quotes

```java
boolean b = True;     // ❌ error: cannot find symbol
boolean b = "true";   // ❌ error: String cannot be converted to boolean
boolean b = true;     // ✅
```

### Mistake 6: Thinking casting rounds the number

```java
int x = (int) 2.99;   // x is 2, NOT 3!
```

If you want to **round**, use `Math.round` (Chapter 8):
```java
long x = Math.round(2.99);   // 3
```

---

## ✅ Summary

- Java has **8 primitive types**. The important ones: `int`, `long`, `double`, `char`, `boolean`.
- `int` → whole numbers (up to ~2.1 billion). `long` → very big whole numbers (add `L`).
- `double` → decimal numbers (use a **dot**). Not always 100% exact.
- `char` → **one** character in **single** quotes `'A'`.
- `boolean` → only `true` or `false` (small letters, no quotes).
- `String` → text in **double** quotes. It's a **class**, not a primitive (capital S).
- Small → big type: automatic. Big → small type: needs **casting** `(int)` and may lose data. Casting **cuts**, it does not round.
- Text → number: `Integer.parseInt("25")`, `Double.parseDouble("9.99")`.

---

## ❓ Quiz

1. Which type would you use for a price like 4.99?
2. What is wrong? `long distance = 9000000000;`
3. What is the difference between `'A'` and `"A"`?
4. What does `(int) 5.8` give?
5. What are the only two values a `boolean` can have?
6. Why does `String` start with a capital letter?
7. What does `"10" + 5` give? And `Integer.parseInt("10") + 5`?
8. What happens if you add 1 to the biggest `int`?

<details>
<summary>Click to see the answers</summary>

1. `double`
2. The `L` is missing at the end: `9000000000L`.
3. `'A'` is a `char` (one character). `"A"` is a `String` (text).
4. `5` (the decimal part is cut off).
5. `true` and `false`.
6. Because `String` is a **class**, not a primitive type. Class names start with a capital letter.
7. `"105"` (text glued) and `15` (real addition).
8. Overflow: it becomes the most negative `int` (−2,147,483,648).

</details>

---

[⬅ Previous chapter](06-variables.md) | [Table of Contents](../README.md) | [Next chapter: Math in Java ➡](08-math-operators.md)
