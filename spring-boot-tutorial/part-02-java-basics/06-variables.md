# Chapter 6 – Variables: Boxes That Keep Information

[⬅ Previous chapter](../part-01-getting-ready/05-hello-world.md) | [Table of Contents](../README.md) | [Next chapter ➡](07-data-types.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **variable** is
- How to **create** a variable (declare it)
- How to **put a value** in it and **change** the value
- How to **use** a variable in your program
- The **rules** for good variable names

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Variable** | A **box** with a **name**. It keeps one piece of information. |
| **Value** | The thing **inside** the box. For example `25` or `"Sara"`. |
| **Declare** | **Make** a new box and give it a name and a type. |
| **Assign** | **Put** a value into the box. We use the `=` sign. |
| **Initialize** | Put the **first** value into a box. |
| **Type** | What **kind** of thing the box can keep: a whole number, text, etc. |
| **`int`** | The type for **whole numbers**: `1`, `25`, `-7`. |
| **`String`** | The type for **text**: `"Hello"`, `"Sara"`. |

---

## 📖 Story: Boxes in your room

Imagine your room has many boxes. 📦📦📦

On every box you write a **label**:
- One box says **"Toys"**.
- One box says **"Books"**.
- One box says **"Shoes"**.

When you want your shoes, you don't search everywhere. You go to the box with the label **"Shoes"**.

A **variable** is the same:

```
   ┌──────────┐      ┌──────────┐      ┌──────────┐
   │    25    │      │  "Sara"  │      │   170    │
   └──────────┘      └──────────┘      └──────────┘
       age               name             height
```

- The **label** is the variable's **name** (`age`).
- The **thing inside** is the **value** (`25`).
- The **kind of box** is the **type**. A box for numbers can't keep text — like a shoe box isn't made for water. 💧

---

## 💻 Your first variable

```java
public class FirstVariable {
    public static void main(String[] args) {
        int age = 25;
        System.out.println(age);
    }
}
```

**Output:**

```
25
```

### 🔍 Line by line

Line 3 is the new part: `int age = 25;`

| Part | Meaning |
|---|---|
| `int` | The **type**. "This box keeps a **whole number**." (`int` comes from *integer*, which means whole number.) |
| `age` | The **name** of the box. We choose it. |
| `=` | "**Put** the value on the right **into** the box on the left." ⚠️ In Java, `=` does **not** mean "is equal". It means "**put into**". |
| `25` | The **value**. |
| `;` | End of the statement. |

Line 4: `System.out.println(age);`

| Part | Meaning |
|---|---|
| `age` | **No quotes!** So Java looks for a box named `age`, opens it, and takes out the value `25`. |

👉 Compare:

```java
System.out.println(age);     // prints: 25    (the value inside the box)
System.out.println("age");   // prints: age   (just the text "age")
```

---

## 🧠 Idea 1: Declare first, then assign

You can make the box **first**, and put something in it **later**:

```java
public class TwoSteps {
    public static void main(String[] args) {
        int score;          // 1. make an empty box called score
        score = 100;        // 2. put 100 into the box
        System.out.println(score);
    }
}
```

**Output:**

```
100
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `int score;` | **Declare**: make a box named `score` for whole numbers. It is **empty** now. |
| `score = 100;` | **Assign**: put `100` into the box. Notice: **no `int`** here — the box already exists! |
| `System.out.println(score);` | Show what is in the box. |

> ⚠️ You can't **use** an empty box. This gives an error:
> ```java
> int score;
> System.out.println(score);   // ❌ error: variable score might not have been initialized
> ```

---

## 🧠 Idea 2: Change the value

A variable can **change**. That's why it's called a **vari**-able (it can **vary** = change).

```java
public class ChangeValue {
    public static void main(String[] args) {
        int lives = 3;
        System.out.println(lives);

        lives = 2;
        System.out.println(lives);

        lives = 1;
        System.out.println(lives);
    }
}
```

**Output:**

```
3
2
1
```

### 🔍 Line by line

| Line | What's in the box `lives` | Printed |
|---|---|---|
| `int lives = 3;` | 3 | |
| `System.out.println(lives);` | 3 | `3` |
| `lives = 2;` | 2 (the old 3 is **thrown away**) | |
| `System.out.println(lives);` | 2 | `2` |
| `lives = 1;` | 1 | |
| `System.out.println(lives);` | 1 | `1` |

👉 A box keeps only **one** value at a time. When you put a new value in, the old one is **gone**. 🗑️

---

## 🧠 Idea 3: Use a variable to change itself

This looks strange, but it's very common:

```java
int coins = 10;
coins = coins + 5;
System.out.println(coins);
```

**Output:**

```
15
```

### 🔍 How Java reads `coins = coins + 5;`

Java always does the **right side first**, then puts the result into the **left side**.

```
 coins = coins + 5;

 Step 1: Look at the right side:      coins + 5
 Step 2: Open the box coins:            10  + 5
 Step 3: Calculate:                       15
 Step 4: Put 15 into the box coins:   coins = 15
```

👉 In math class, `coins = coins + 5` is impossible. But in Java, `=` means "**put into**", so it makes sense: "Take coins, add 5, and put the result back into coins."

---

## 🧠 Idea 4: Text variables (`String`)

```java
public class TextVariable {
    public static void main(String[] args) {
        String name = "Sara";
        String city = "Lagos";

        System.out.println(name);
        System.out.println(city);
    }
}
```

**Output:**

```
Sara
Lagos
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `String` | The type for **text**. ⚠️ Capital **S**! (`string` with small s is an error.) |
| `name` | The name of the box. |
| `"Sara"` | The text value. Always in double quotes. |

---

## 🧠 Idea 5: Join text and variables with `+`

You can **join** text and variables together with `+`:

```java
public class Greeting {
    public static void main(String[] args) {
        String name = "Sara";
        int age = 12;

        System.out.println("My name is " + name);
        System.out.println("I am " + age + " years old.");
    }
}
```

**Output:**

```
My name is Sara
I am 12 years old.
```

### 🔍 Line by line

`"My name is " + name`

| Step | Result |
|---|---|
| Open the box `name` | `"Sara"` |
| Join `"My name is "` and `"Sara"` | `"My name is Sara"` |

`"I am " + age + " years old."`

| Step | Result |
|---|---|
| Open the box `age` | `12` |
| Join `"I am "` + `12` | `"I am 12"` |
| Join `"I am 12"` + `" years old."` | `"I am 12 years old."` |

> 💡 **Spaces!** Look at the space at the end of `"My name is "` and at the start of `" years old."`. Without them you get `My name isSara` and `I am 12years old.` Java adds **no** spaces by itself.

Joining text like this is called **concatenation** (con-cat-e-NAY-shun). Just remember: **`+` with text = glue**. 🧴

---

## 🧠 Idea 6: Many variables, one program

```java
public class Shop {
    public static void main(String[] args) {
        String product = "Apple";
        int price = 2;
        int amount = 6;
        int total = price * amount;

        System.out.println("Product: " + product);
        System.out.println("Price: " + price);
        System.out.println("Amount: " + amount);
        System.out.println("Total: " + total);
    }
}
```

**Output:**

```
Product: Apple
Price: 2
Amount: 6
Total: 12
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `String product = "Apple";` | A text box `product` with the value `"Apple"`. |
| `int price = 2;` | A number box `price` with the value `2`. |
| `int amount = 6;` | A number box `amount` with the value `6`. |
| `int total = price * amount;` | Open `price` (2) and `amount` (6). Multiply: `2 * 6 = 12`. Put 12 into a new box `total`. (`*` means multiply.) |
| The 4 `println` lines | Print a label and the value of each box. |

👉 **Why use variables here?** If the price changes to 3, you change **only one line** (`int price = 3;`), and `total` is correct automatically. 🎉

---

## 🧠 Idea 7: Copy one variable into another

```java
int a = 5;
int b = a;     // copy the VALUE of a into b
a = 100;       // change a

System.out.println(a);   // 100
System.out.println(b);   // 5
```

### 🔍 Line by line

| Line | a | b |
|---|---|---|
| `int a = 5;` | 5 | — |
| `int b = a;` | 5 | 5 (a **copy** of the value) |
| `a = 100;` | 100 | 5 (b **does not change**!) |

👉 `b = a` **copies** the value at that moment. The boxes are not "connected" after that.

---

## 🧠 Idea 8: `final` — a box you can't change

Sometimes a value should **never** change. For example, the number of days in a week. Use `final`:

```java
final int DAYS_IN_WEEK = 7;
DAYS_IN_WEEK = 8;   // ❌ error: cannot assign a value to final variable DAYS_IN_WEEK
```

| Part | Meaning |
|---|---|
| `final` | "This is the **final** value. Nobody can change it." Like a box that is **locked** 🔒. |
| `DAYS_IN_WEEK` | Names of `final` values (constants) are written in **CAPITAL letters** with `_` between words. This is a tradition, so everyone can see "this is fixed". |

---

## 🧠 Idea 9: `var` — let Java guess the type

Since Java 10, you can write `var` instead of the type. Java **looks at the value** and chooses the type:

```java
var age = 25;          // Java sees 25 → it chooses int
var name = "Sara";     // Java sees "Sara" → it chooses String
```

This is the **same** as:

```java
int age = 25;
String name = "Sara";
```

> ⚠️ The type is still **fixed**. After `var age = 25;`, `age` is an `int` forever. `age = "hello";` is an error.
>
> 👉 **In this book**, we usually write the type (`int`, `String`), because it helps you **learn** the types. You will see `var` in real projects.

---

## 📏 Rules for variable names

### ✅ Must-follow rules (or you get an error)

| Rule | ✅ Good | ❌ Bad |
|---|---|---|
| Start with a **letter** (or `_` or `$`) | `age`, `name1` | `1name` |
| Only letters, numbers, `_`, `$` | `my_age`, `total2` | `my-age`, `my age`, `total!` |
| No **spaces** | `firstName` | `first name` |
| Not a Java **keyword** | `myClass` | `class`, `int`, `public` |
| Big/small letters matter | `age` and `Age` are **different** variables | |

### 👍 Good habits (no error, but please follow)

| Habit | ✅ Good | 👎 Bad |
|---|---|---|
| Use **camelCase**: start small, every new word starts with a capital letter | `firstName`, `totalPrice`, `numberOfStudents` | `firstname`, `FirstName`, `first_name` |
| Use **clear** names that say what is inside | `price`, `studentName` | `x`, `a1`, `thing` |
| Use **English** words | `age` | `edad`, `umur` |

> 🐫 **Why "camelCase"?** The capital letters look like the humps of a camel: first**N**ame, total**P**rice.

---

## ✋ Try it yourself

**Task 1:** Make variables for your **name**, **age** and **favorite color**. Print:

```
Hi! I am Omar.
I am 15 years old.
My favorite color is blue.
```

<details>
<summary>Click to see one possible answer</summary>

```java
public class AboutMe {
    public static void main(String[] args) {
        String name = "Omar";
        int age = 15;
        String color = "blue";

        System.out.println("Hi! I am " + name + ".");
        System.out.println("I am " + age + " years old.");
        System.out.println("My favorite color is " + color + ".");
    }
}
```

</details>

**Task 2:** What does this print? Think first!

```java
int x = 4;
int y = x;
x = x + 10;
y = y + 1;
System.out.println(x);
System.out.println(y);
```

<details>
<summary>Click to see the answer</summary>

```
14
5
```

`x`: 4 → 14. `y` got a copy (4), then 4 + 1 = 5.

</details>

**Task 3:** Swap two boxes! You have `int a = 1;` and `int b = 2;`. Make `a` become `2` and `b` become `1`.
Hint: you need a **third** box. Think about swapping the water in two glasses — you need an empty glass! 🥛🥛🥛

<details>
<summary>Click to see the answer</summary>

```java
int a = 1;
int b = 2;

int temp = a;   // temp = 1   (save a)
a = b;          // a = 2
b = temp;       // b = 1

System.out.println(a);   // 2
System.out.println(b);   // 1
```

</details>

**Task 4:** Which names are **allowed** in Java? `myName`, `2fast`, `total_price`, `class`, `first name`, `$money`, `numberOfCats`

<details>
<summary>Click to see the answer</summary>

Allowed: `myName`, `total_price`, `$money`, `numberOfCats`
Not allowed: `2fast` (starts with a number), `class` (keyword), `first name` (space)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Using a variable before it exists

```java
System.out.println(age);   // ❌ error: cannot find symbol
int age = 25;
```

Java reads **top to bottom**. On line 1, the box `age` does not exist yet.
**Fix:** Declare the variable **before** you use it.

### Mistake 2: Declaring the same name two times

```java
int age = 25;
int age = 30;   // ❌ error: variable age is already defined
```

**Fix:** To **change** the value, don't write `int` again:
```java
int age = 25;
age = 30;       // ✅
```

### Mistake 3: Wrong type

```java
int age = "twenty";   // ❌ error: incompatible types: String cannot be converted to int
```

An `int` box only takes whole numbers. **Fix:** `int age = 20;`

### Mistake 4: Small `s` in `string`

```java
string name = "Sara";   // ❌ error: cannot find symbol
```

**Fix:** `String` with a capital **S**.

### Mistake 5: Quotes around a variable name

```java
String name = "Sara";
System.out.println("name");   // prints: name   (not Sara!)
```

**Fix:** No quotes when you want the **value**: `System.out.println(name);`

### Mistake 6: Using a variable with different capital letters

```java
int studentAge = 12;
System.out.println(studentage);   // ❌ error: cannot find symbol
```

`studentAge` and `studentage` are **different** names for Java. **Fix:** Use the exact same spelling.

---

## ✅ Summary

- A **variable** is a box with a **name**, a **type** and a **value**.
- Create it: `int age = 25;` → type, name, `=`, value, `;`.
- `=` means "**put into**", not "is equal".
- Java does the **right side first**, then puts the result into the left side.
- A box keeps **one** value. A new value **replaces** the old one.
- `int` = whole numbers. `String` = text (in `" "`).
- `+` with text **joins** (glues) text together. Don't forget spaces!
- `final` makes a value that can **never change**.
- `var` lets Java choose the type from the value.
- Name variables in **camelCase** with clear English words: `totalPrice`.

---

## ❓ Quiz

1. What are the three parts of a variable?
2. What does `=` mean in Java?
3. What is printed? `int a = 3; a = a * 2; System.out.println(a);`
4. What is the difference between `System.out.println(city);` and `System.out.println("city");`?
5. Why is `int 2cars = 2;` wrong?
6. Which is the best name for a variable that keeps the number of students: `n`, `NumberOfStudents`, `numberOfStudents`, `number_of_students`?
7. What does `final` do?
8. What is printed? `String s = "Hi"; System.out.println(s + s + "!");`

<details>
<summary>Click to see the answers</summary>

1. Type, name, value.
2. "Put the value on the right into the variable on the left."
3. `6`
4. The first prints the **value** inside the variable `city`. The second prints the word `city`.
5. A variable name cannot start with a number.
6. `numberOfStudents` (camelCase, clear).
7. The variable cannot be changed after it gets its value.
8. `HiHi!`

</details>

---

[⬅ Previous chapter](../part-01-getting-ready/05-hello-world.md) | [Table of Contents](../README.md) | [Next chapter: Data types ➡](07-data-types.md)
