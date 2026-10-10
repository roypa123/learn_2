# Chapter 15 – Methods: Giving a Name to a Job

[⬅ Previous chapter](14-arrays.md) | [Table of Contents](../README.md) | [Next chapter ➡](16-scanner-input.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **method** is and **why** we use methods
- How to **write** your own method and **call** it
- How to give **inputs** to a method (**parameters**)
- How to get an **answer** back from a method (**return**)
- What `void` really means
- **Overloading**: many methods with the same name
- **Scope**: where a variable lives
- How to pass **arrays** to methods

> 🌱 **Why this chapter is VERY important for Spring Boot:** In Spring Boot, almost **everything** you write is a method. A web page answer? A method. Saving a student? A method. Understand this chapter well!

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Method** | A block of code with a **name** that does **one job**. |
| **Call** | **Use** a method — tell it "do your job now!" |
| **Parameter** | An **input** variable of the method. Written in the method's brackets. |
| **Argument** | The **real value** you give to a parameter when you call the method. |
| **Return** | Give an **answer back** to the place that called the method. |
| **Return type** | The **type** of the answer (`int`, `String`, ...). `void` = no answer. |
| **Signature** | The name of the method + the types of its parameters. |
| **Overloading** | Many methods with the **same name** but **different** parameters. |
| **Scope** | The area of code where a variable **exists**. |

---

## 📖 Story: The coffee machine ☕

A coffee machine is like a **method**:

```
            INPUT                    THE JOB                 OUTPUT
       (parameters)               (method body)             (return)
 ┌──────────────────────┐     ┌─────────────────────┐    ┌────────────┐
 │ water 💧, coffee 🫘,  │ ──► │  makeCoffee         │ ──►│  a cup ☕   │
 │ sugar: 2 spoons      │     │  (heat, mix, pour)  │    │            │
 └──────────────────────┘     └─────────────────────┘    └────────────┘
```

- It has a **name**: "makeCoffee".
- You give it **inputs**: water, coffee, how much sugar.
- It does a **job** inside. You don't need to know **how** — you just press the button.
- It gives you something **back**: a cup of coffee.

And the best part: you can use it **again and again**, every morning, without building a new machine! 🔁

---

## 🤔 Part 1: Why do we need methods?

Look at this code:

```java
System.out.println("====================");
System.out.println("  Welcome, Sara!");
System.out.println("====================");

// ... some other code ...

System.out.println("====================");
System.out.println("  Welcome, Tom!");
System.out.println("====================");

// ... some other code ...

System.out.println("====================");
System.out.println("  Welcome, Lina!");
System.out.println("====================");
```

The same 3 lines, **again and again**. 😩 Problems:

1. **Long** and boring to write.
2. If you want to change `=` to `*`, you must change it in **many** places. You will forget one!
3. It's **hard to read**. What is this code doing?

**With a method:**

```java
welcome("Sara");
welcome("Tom");
welcome("Lina");
```

Short, clear, easy to change. 😍 Here's how to make it.

> 💡 **Programmer's rule: DRY — Don't Repeat Yourself.** If you copy the same code 2–3 times, make a method.

---

## ✍️ Part 2: Your first method

```java
public class FirstMethod {

    public static void main(String[] args) {
        System.out.println("Start");
        sayHello();
        sayHello();
        System.out.println("End");
    }

    public static void sayHello() {
        System.out.println("Hello! 👋");
    }
}
```

**Output:**

```
Start
Hello! 👋
Hello! 👋
End
```

### 🔍 Line by line — the method

`public static void sayHello() {`

| Part | Meaning |
|---|---|
| `public` | Everyone can use this method. (More about this in Part 3 of the book.) |
| `static` | The method belongs to the class. For now: use `static` because `main` is `static`. (Chapter 27 explains it fully.) |
| `void` | The method gives **nothing back**. It just does its job. |
| `sayHello` | The **name** we choose. Methods use **camelCase** and usually start with a **verb** (an action word): `sayHello`, `calculateTotal`, `printReport`. |
| `()` | The brackets for inputs. **Empty** = no inputs. |
| `{ ... }` | The **body**: the code that runs when the method is called. |

### 🔍 Line by line — calling it

`sayHello();`

| Part | Meaning |
|---|---|
| `sayHello` | "Find the method with this name..." |
| `()` | "...and **run** it now." The brackets are **needed** to call it. |
| `;` | End of the statement. |

### 🎬 What happens — step by step

```
 main starts
   │
   ├─ print "Start"
   │
   ├─ sayHello(); ───────────► jump into sayHello
   │                             print "Hello! 👋"
   │  ◄──────────────────────── method ends, jump BACK
   │
   ├─ sayHello(); ───────────► jump into sayHello again
   │                             print "Hello! 👋"
   │  ◄──────────────────────── jump BACK
   │
   ├─ print "End"
   │
 main ends
```

👉 When you call a method, Java **jumps** into it, runs all its lines, then **jumps back** to the exact place where it was called, and continues.

### 📍 Where do methods go?

Methods are written **inside the class**, but **outside** other methods. They are **neighbors** of `main`, not **inside** `main`.

```java
public class MyProgram {

    public static void main(String[] args) {   // method 1
        ...
    }

    public static void sayHello() {            // method 2 (a neighbor of main)
        ...
    }
}
```

The **order** of methods in the class does not matter. `sayHello` can be above or below `main`.

---

## 📥 Part 3: Parameters — giving inputs to a method

A method is more useful if it can work with **different** values:

```java
public class Greeting {

    public static void main(String[] args) {
        welcome("Sara");
        welcome("Tom");
    }

    public static void welcome(String name) {
        System.out.println("====================");
        System.out.println("  Welcome, " + name + "!");
        System.out.println("====================");
    }
}
```

**Output:**

```
====================
  Welcome, Sara!
====================
====================
  Welcome, Tom!
====================
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `welcome(String name)` | The method has **one parameter**: a `String` named `name`. It's like a variable that is created when the method starts. |
| `welcome("Sara");` | Call the method. The **argument** `"Sara"` is put into the parameter `name`. |
| Inside the method | `name` is `"Sara"` on the first call, and `"Tom"` on the second call. |

### Parameter vs. argument

```
 Definition:     public static void welcome(String name)
                                            ───────────
                                            PARAMETER (the empty box)

 Call:           welcome("Sara");
                         ──────
                         ARGUMENT (the value put in the box)
```

📖 Think of a **form** with an empty field "Name: ____". The **field** is the parameter. What you **write** in it is the argument. 📝

### Many parameters

Separate them with commas. Each one needs its **own type**:

```java
public static void printRectangle(int width, int height, char symbol) {
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            System.out.print(symbol);
        }
        System.out.println();
    }
}
```

Call it:

```java
printRectangle(5, 3, '#');
```

**Output:**

```
#####
#####
#####
```

| Parameter | Argument |
|---|---|
| `width` | `5` |
| `height` | `3` |
| `symbol` | `'#'` |

⚠️ The arguments must come in the **same order** and have the **same types** as the parameters:

```java
printRectangle('#', 5, 3);   // ❌ error: wrong order (3 is not a char)
printRectangle(5, 3);        // ❌ error: method needs 3 arguments, you gave 2
```

---

## 📤 Part 4: Return — getting an answer back

Some methods **calculate** something and give the result **back**:

```java
public class AddNumbers {

    public static void main(String[] args) {
        int result = add(3, 4);
        System.out.println("3 + 4 = " + result);

        System.out.println("10 + 20 = " + add(10, 20));

        int total = add(add(1, 2), add(3, 4));
        System.out.println("Total: " + total);
    }

    public static int add(int a, int b) {
        int sum = a + b;
        return sum;
    }
}
```

**Output:**

```
3 + 4 = 7
10 + 20 = 30
Total: 10
```

### 🔍 Line by line — the method

| Part | Meaning |
|---|---|
| `public static int add(...)` | ⚠️ `int` instead of `void`! This is the **return type**: "This method gives back an `int`." |
| `(int a, int b)` | Two inputs. |
| `int sum = a + b;` | Do the job. |
| `return sum;` | "**Give** the value of `sum` **back** to the caller, and **end** the method." |

### 🔍 Line by line — the calls

| Call | What happens |
|---|---|
| `int result = add(3, 4);` | Java runs `add` with a=3, b=4. It returns 7. The call `add(3, 4)` is **replaced** by `7`. So: `int result = 7;` |
| `"10 + 20 = " + add(10, 20)` | You can use the call **directly** in an expression. It becomes `"10 + 20 = " + 30`. |
| `add(add(1, 2), add(3, 4))` | Inside first: `add(1, 2)` → 3, `add(3, 4)` → 7. Then `add(3, 7)` → **10**. |

👉 **Think of it this way:** a method call with a return value is **replaced by its answer**. 🔄

### Shorter

You don't always need the extra variable:

```java
public static int add(int a, int b) {
    return a + b;
}
```

### More examples of returning methods

```java
public static double circleArea(double radius) {
    return Math.PI * radius * radius;
}

public static boolean isEven(int number) {
    return number % 2 == 0;
}

public static String fullName(String first, String last) {
    return first + " " + last;
}

public static char firstLetter(String word) {
    return word.charAt(0);
}
```

Using them:

```java
System.out.println(circleArea(2));             // 12.566370614359172
System.out.println(isEven(7));                 // false
System.out.println(fullName("Sara", "Ali"));   // Sara Ali
System.out.println(firstLetter("Java"));       // J

if (isEven(10)) {
    System.out.println("10 is even!");
}
```

> 💡 Look at `isEven`: `number % 2 == 0` is already `true` or `false`. So we can **return it directly**. No need for `if`!
> ```java
> // ❌ too long
> if (number % 2 == 0) {
>     return true;
> } else {
>     return false;
> }
> // ✅ short and clear
> return number % 2 == 0;
> ```

---

## 🧩 Part 5: `void` vs. returning a value

| | `void` method | Method with a return type |
|---|---|---|
| Gives back | **nothing** | a value (`int`, `String`, ...) |
| Has `return value;` | no | **yes** (required!) |
| Example | `printReport()` — prints something | `calculateTotal()` — gives a number |
| Use the call in an expression? | ❌ `int x = sayHello();` → error | ✅ `int x = add(1, 2);` |

📖 **Story:**
- A `void` method is like **"Please clean your room."** 🧹 — The job is done. Nothing is given back to you.
- A returning method is like **"Please tell me the time."** ⌚ — You get an **answer** back.

### 👍 Good habit: calculate OR print — not both

```java
// 👎 Less useful: it calculates AND prints
public static void printSum(int a, int b) {
    System.out.println(a + b);
}

// 👍 More useful: it only calculates. The caller decides what to do with the answer.
public static int sum(int a, int b) {
    return a + b;
}
```

With `sum`, you can print the result, save it, compare it, use it in another calculation... With `printSum`, you can **only** print. 🤷

---

## 🚪 Part 6: More about `return`

### `return` ends the method immediately

```java
public static String checkAge(int age) {
    if (age < 0) {
        return "Invalid age";      // ← method ends here if age < 0
    }
    if (age < 18) {
        return "Child";            // ← or here
    }
    return "Adult";                // ← or here
}
```

Lines after a `return` (in the same path) are **never** reached.

```java
System.out.println(checkAge(-5));   // Invalid age
System.out.println(checkAge(10));   // Child
System.out.println(checkAge(30));   // Adult
```

### Every path must return a value

```java
public static String sign(int n) {
    if (n > 0) {
        return "positive";
    } else if (n < 0) {
        return "negative";
    }
    // ❌ error: missing return statement  (what if n == 0?)
}
```

**Fix:** Make sure **every** possible road ends with a `return`:

```java
    return "zero";   // ✅ add this at the end
}
```

### `return;` in a `void` method

A `void` method can use `return;` (without a value) to **stop early**:

```java
public static void divide(int a, int b) {
    if (b == 0) {
        System.out.println("Can't divide by zero!");
        return;   // stop here
    }
    System.out.println(a / b);
}
```

---

## 🔁 Part 7: Overloading — same name, different inputs

You can have **many methods with the same name**, if their **parameters are different**:

```java
public static int add(int a, int b) {
    return a + b;
}

public static int add(int a, int b, int c) {
    return a + b + c;
}

public static double add(double a, double b) {
    return a + b;
}
```

```java
System.out.println(add(1, 2));        // 3      → uses the first method
System.out.println(add(1, 2, 3));     // 6      → uses the second method
System.out.println(add(1.5, 2.5));    // 4.0    → uses the third method
```

Java looks at the **number** and **types** of the arguments and picks the matching method. 🎯

👉 You already used overloading! `System.out.println` has many versions: `println(int)`, `println(String)`, `println(double)`, `println()`...

> ⚠️ Changing **only** the return type is **not** enough:
> ```java
> public static int calc(int a) { ... }
> public static double calc(int a) { ... }   // ❌ error: method calc(int) is already defined
> ```

---

## 🏠 Part 8: Scope — where variables live

Every method is like a **separate house**. 🏠 🏠 Variables made inside a method live **only in that house**.

```java
public class ScopeExample {

    public static void main(String[] args) {
        int x = 10;
        changeIt(x);
        System.out.println("In main, x = " + x);
    }

    public static void changeIt(int x) {
        x = 99;
        System.out.println("In changeIt, x = " + x);
    }
}
```

**Output:**

```
In changeIt, x = 99
In main, x = 10
```

😮 `x` in `main` is **still 10**! Why?

| | Meaning |
|---|---|
| `changeIt(x)` | Java gives the method a **copy** of the value 10. |
| `int x` in `changeIt` | This is a **different** box, in a **different** house, that just has the same name. |
| `x = 99` | Changes only the box in `changeIt`'s house. |

🏠 **Story:** Two houses each have a dog named "Max". 🐕 🐕 If you give a bath to Max in house 1, Max in house 2 stays dirty! Same name, different dogs.

👉 **Rule:** For `int`, `double`, `char`, `boolean` and `String`, the method gets a **copy**. It can't change the caller's variable. If you want a new value, **return** it:

```java
public static int doubleIt(int x) {
    return x * 2;
}

int x = 10;
x = doubleIt(x);   // x is now 20 ✅
```

### Variables can't be seen in other methods

```java
public static void main(String[] args) {
    int secret = 42;
    showSecret();
}

public static void showSecret() {
    System.out.println(secret);   // ❌ error: cannot find symbol
}
```

`secret` lives in `main`'s house. `showSecret` can't see it. **Fix:** Pass it as a parameter:

```java
public static void showSecret(int secret) {
    System.out.println(secret);
}
```

---

## 📦 Part 9: Arrays and methods

### Passing an array to a method

```java
public static int sumArray(int[] numbers) {
    int sum = 0;
    for (int n : numbers) {
        sum += n;
    }
    return sum;
}
```

```java
int[] scores = {80, 95, 70};
System.out.println(sumArray(scores));   // 245
```

### ⚠️ A method CAN change an array!

Remember Chapter 14, Part 7: an array variable holds an **address** (a note pointing to the egg box). The method gets a copy of the **note** — but it points to the **same** egg box!

```java
public static void addBonus(int[] numbers) {
    for (int i = 0; i < numbers.length; i++) {
        numbers[i] += 5;
    }
}
```

```java
int[] scores = {80, 95, 70};
addBonus(scores);
System.out.println(Arrays.toString(scores));   // [85, 100, 75] ← changed!
```

| Type | Can the method change the caller's value? |
|---|---|
| `int`, `double`, `boolean`, `char` | ❌ No (gets a copy of the value) |
| `String` | ❌ No (Strings can't change at all — immutable) |
| Arrays (and objects — Part 3) | ✅ **Yes**, the elements inside (gets a copy of the address) |

### Returning an array

```java
public static int[] makeRange(int start, int end) {
    int[] result = new int[end - start + 1];
    for (int i = 0; i < result.length; i++) {
        result[i] = start + i;
    }
    return result;
}
```

```java
int[] r = makeRange(3, 7);
System.out.println(Arrays.toString(r));   // [3, 4, 5, 6, 7]
```

---

## 🧱 Part 10: Methods calling methods

Methods can call **other** methods. This lets you build big programs from **small pieces**, like LEGO 🧱:

```java
public class Shop {

    public static void main(String[] args) {
        double[] prices = {12.50, 8.00, 3.75};
        printReceipt(prices);
    }

    public static double subtotal(double[] prices) {
        double sum = 0;
        for (double p : prices) {
            sum += p;
        }
        return sum;
    }

    public static double tax(double amount) {
        return amount * 0.10;
    }

    public static double roundMoney(double amount) {
        return Math.round(amount * 100) / 100.0;
    }

    public static void printReceipt(double[] prices) {
        double sub = subtotal(prices);
        double t = tax(sub);
        double total = sub + t;

        System.out.println("--- RECEIPT ---");
        System.out.println("Subtotal: " + roundMoney(sub));
        System.out.println("Tax 10%:  " + roundMoney(t));
        System.out.println("Total:    " + roundMoney(total));
    }
}
```

**Output:**

```
--- RECEIPT ---
Subtotal: 24.25
Tax 10%:  2.43
Total:    26.68
```

### 🔍 Who calls whom?

```
 main
  └─► printReceipt
        ├─► subtotal   → returns 24.25
        ├─► tax        → returns about 2.425
        └─► roundMoney (3 times)
```

👉 Each method does **one small job** and has a **clear name**. You can read `printReceipt` almost like English: "subtotal of prices, tax of sub, total is sub plus tax". 📖 That's **clean code**!

---

## ✋ Try it yourself

**Task 1:** Write a method `square(int n)` that returns `n * n`. Test it with 5 (answer: 25).

<details>
<summary>Click to see the answer</summary>

```java
public static int square(int n) {
    return n * n;
}

// in main:
System.out.println(square(5));   // 25
```

</details>

**Task 2:** Write a method `max(int a, int b)` that returns the bigger number **without** using `Math.max`.

<details>
<summary>Click to see the answer</summary>

```java
public static int max(int a, int b) {
    if (a > b) {
        return a;
    }
    return b;
}

// or with the ternary operator:
public static int max(int a, int b) {
    return a > b ? a : b;
}
```

</details>

**Task 3:** Write a method `countVowels(String text)` that returns how many vowels the text has.

<details>
<summary>Click to see the answer</summary>

```java
public static int countVowels(String text) {
    int count = 0;
    String lower = text.toLowerCase();
    for (int i = 0; i < lower.length(); i++) {
        char c = lower.charAt(i);
        if ("aeiou".indexOf(c) != -1) {
            count++;
        }
    }
    return count;
}
```

Trick: `"aeiou".indexOf(c) != -1` means "c is one of these letters".

</details>

**Task 4:** Write a method `isPrime(int n)` that returns `true` if `n` is a prime number. Then use it in a loop to print all prime numbers from 1 to 50.

<details>
<summary>Click to see the answer</summary>

```java
public static boolean isPrime(int n) {
    if (n < 2) {
        return false;
    }
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}

// in main:
for (int i = 1; i <= 50; i++) {
    if (isPrime(i)) {
        System.out.print(i + " ");
    }
}
// 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47
```

`i * i <= n` is a speed trick: you only need to check up to the square root.

</details>

**Task 5:** Write a method `average(int[] numbers)` that returns a `double`. Test with `{4, 8, 15, 16, 23, 42}` (answer: 18.0).

**Task 6:** Overload a method `describe`: `describe(int)` prints "Number: 5", `describe(String)` prints "Text: hello", `describe(boolean)` prints "Yes/No: true".

---

## ⚠️ Common mistakes

### Mistake 1: Writing a method inside `main`

```java
public static void main(String[] args) {
    public static void hello() { }   // ❌ error: illegal start of expression
}
```

**Fix:** Methods go **next to** `main`, inside the class.

### Mistake 2: Forgetting `()` when calling

```java
sayHello;     // ❌ error: not a statement
sayHello();   // ✅
```

### Mistake 3: Missing `return` in a non-void method

```java
public static int twice(int n) {
    int r = n * 2;
}   // ❌ error: missing return statement
```

### Mistake 4: Returning a value from a `void` method

```java
public static void twice(int n) {
    return n * 2;   // ❌ error: incompatible types: unexpected return value
}
```

**Fix:** Change `void` to `int`.

### Mistake 5: Ignoring the returned value

```java
add(3, 4);                  // ⚠️ no error, but the answer 7 is thrown away! 🗑️
int r = add(3, 4);          // ✅ keep it
System.out.println(add(3, 4));  // ✅ or use it
```

### Mistake 6: Wrong number or type of arguments

```java
public static int add(int a, int b) { ... }

add(1);            // ❌ error: method add cannot be applied to given types
add("1", "2");     // ❌ error: incompatible types
```

### Mistake 7: `static` missing

```java
public static void main(String[] args) {
    hello();       // ❌ error: non-static method hello() cannot be referenced from a static context
}
public void hello() { }
```

**Fix (for now):** Add `static`: `public static void hello()`. In Part 3, you'll learn when **not** to use `static`.

### Mistake 8: Expecting a method to change an `int`

```java
public static void addOne(int x) { x++; }

int n = 5;
addOne(n);
System.out.println(n);   // 5, not 6! (the method changed only its own copy)
```

**Fix:** Return the new value: `n = addOne(n);` with `public static int addOne(int x) { return x + 1; }`.

---

## ✅ Summary

- A **method** is a named block of code that does **one job**. Write it once, use it many times. (**DRY!**)
- Define: `public static returnType name(parameters) { body }`
- Call: `name(arguments);` — Java jumps in, runs the body, and jumps back.
- **Parameters** are the inputs (the empty fields). **Arguments** are the values you give.
- `void` = gives nothing back. Any other return type = **must** `return` a value.
- `return` gives the answer back **and ends** the method.
- A call like `add(3, 4)` is **replaced** by its answer.
- **Overloading**: same name, different parameters.
- **Scope**: each method is a separate house. Variables live only in their own method.
- Methods get **copies** of primitive values. But arrays are **shared** — the method can change their elements.
- Good method names are **verbs** in camelCase: `calculateTotal`, `isEven`, `printReport`.

---

## ❓ Quiz

1. What does `void` mean?
2. What is the difference between a parameter and an argument?
3. What does this print?
   ```java
   public static int triple(int n) { return n * 3; }
   // in main:
   System.out.println(triple(triple(2)));
   ```
4. What is wrong? `public static int getAge() { System.out.println(25); }`
5. Can two methods have the same name? When?
6. After `int a = 5; change(a);` where `change` sets its parameter to 100 — what is `a`?
7. After `int[] a = {5}; change(a);` where `change` sets `arr[0] = 100` — what is `a[0]`?
8. Why is it often better to `return` a result instead of printing it inside the method?

<details>
<summary>Click to see the answers</summary>

1. The method gives **nothing** back.
2. A **parameter** is the variable in the method's definition. An **argument** is the real value you give when you call it.
3. `18` (`triple(2)` = 6, `triple(6)` = 18).
4. It says it returns an `int`, but there's no `return` statement. Fix: `return 25;`
5. Yes, if they have **different parameters** (number or types). This is overloading.
6. `5` — the method got a copy.
7. `100` — arrays are shared.
8. Because the caller can then decide what to do with the result: print it, save it, compare it, use it in another calculation.

</details>

---

[⬅ Previous chapter](14-arrays.md) | [Table of Contents](../README.md) | [Next chapter: Reading user input ➡](16-scanner-input.md)
