# Chapter 35 – Lambdas: Small Functions

[⬅ Previous chapter](34-generics.md) | [Table of Contents](../README.md) | [Next chapter ➡](36-streams.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **lambda** is: a small function **without a name**
- The **arrow** `->` syntax, in all its forms
- What a **functional interface** is
- The most important built-in ones: **`Predicate`**, **`Function`**, **`Consumer`**, **`Supplier`**, **`Comparator`**
- **Method references**: `String::toUpperCase`, `System.out::println`
- How to **pass behavior** to a method
- How lambdas make your code **shorter** (and prepare you for **Streams**!)

> 🌱 **Spring Boot note:** Modern Spring code is **full** of lambdas: `.orElseThrow(() -> new NotFoundException(id))`, security configuration, streams over database results... After this chapter, you'll read them easily!

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Lambda** | A short, **nameless** function you can store in a variable or pass to a method. |
| **Arrow** `->` | Separates the **inputs** (left) from the **work** (right). |
| **Functional interface** | An interface with **exactly one** abstract method. A lambda is a quick way to implement it. |
| **Method reference** | An even shorter lambda that points to an existing method: `String::length`. |
| **Predicate** | A function that answers **yes/no** (returns a `boolean`). |
| **Higher-order method** | A method that **takes a function** as a parameter. |

---

## 📖 Story: The sticky note for the babysitter 📝

You leave your little brother with a babysitter. You could write a **whole letter** with a title, an introduction, your signature... 📜

Or you could write a **sticky note**:

> 🟨 "If he cries → give him the teddy bear."

Short. Clear. Exactly the instruction needed, nothing more.

A **lambda** is a **sticky note of code**: a small instruction you **give** to someone else (a method), so they can use it **when they need it**.

```
   cries  →  give teddy bear
   ─────     ───────────────
   input        what to do
```

---

## 😩 Part 1: The problem — so much code for a small job

Remember sorting with a `Comparator` (Chapter 30)? Here's the **old way**, with an **anonymous class**:

```java
List<String> names = new ArrayList<>(List.of("Sara", "Al", "Benjamin", "Tom"));

names.sort(new Comparator<String>() {
    @Override
    public int compare(String a, String b) {
        return a.length() - b.length();
    }
});

System.out.println(names);   // [Al, Tom, Sara, Benjamin]
```

😵 **Six lines** of "ceremony" for one tiny idea: "compare by length".

### ✨ With a lambda

```java
names.sort((a, b) -> a.length() - b.length());
```

**One line.** Same result! 🎉

The lambda `(a, b) -> a.length() - b.length()` **is** the `compare` method — without all the wrapping paper. 🎁

---

## ➡️ Part 2: Lambda syntax

```
     (a, b)     ->     a.length() - b.length()
     ──────     ──     ───────────────────────
    PARAMETERS ARROW        BODY (the work)
```

Read `->` as "**goes to**" or "**becomes**": "a and b **become** a.length() minus b.length()".

### All the forms

| Form | Example | When |
|---|---|---|
| No parameters | `() -> System.out.println("Hi")` | nothing goes in |
| One parameter | `x -> x * 2` | brackets are **optional** with one parameter |
| One parameter, with brackets | `(x) -> x * 2` | also OK |
| Two parameters | `(a, b) -> a + b` | brackets **needed** |
| With types (rarely needed) | `(String s) -> s.length()` | Java usually guesses the types |
| Many lines | `x -> { int y = x * 2; return y + 1; }` | use `{ }` and `return` |

### One line vs. many lines

```java
// One expression: no { }, no return, no ; inside
x -> x * x

// Many statements: { }, return, and ; like a normal method
x -> {
    int squared = x * x;
    System.out.println("Squaring " + x);
    return squared;
}
```

### A lambda compared with a method

```java
// Normal method
static int square(int x) {
    return x * x;
}

// The same as a lambda
x -> x * x
```

The lambda has **no name**, **no return type**, **no `return`** (for one expression). Java figures it all out. 🧠

---

## 🔌 Part 3: Functional interfaces — where lambdas "plug in"

A lambda can't live alone. It must have a **type**. That type is a **functional interface**: an interface with **exactly one** abstract method.

```java
@FunctionalInterface
public interface Calculator {
    int calculate(int a, int b);
}
```

| Part | Meaning |
|---|---|
| `@FunctionalInterface` | A label (optional) that asks Java to check: "this interface has exactly one abstract method". |
| `int calculate(int a, int b);` | The **one** method. A lambda will **be** this method. |

```java
Calculator add      = (a, b) -> a + b;
Calculator multiply = (a, b) -> a * b;
Calculator power    = (a, b) -> (int) Math.pow(a, b);

System.out.println(add.calculate(3, 4));        // 7
System.out.println(multiply.calculate(3, 4));   // 12
System.out.println(power.calculate(3, 4));      // 81
```

### 🔍 What happens?

`Calculator add = (a, b) -> a + b;`

Java thinks: "The variable is a `Calculator`. Calculator has one method: `int calculate(int a, int b)`. So this lambda **is** the body of `calculate`: `a` and `b` are ints, and it returns `a + b`."

It's like a very short **class that implements the interface** (Chapter 25) — written in one line! 🪄

```
   Calculator add = (a, b) -> a + b;

   is the same as:

   class Adder implements Calculator {
       public int calculate(int a, int b) {
           return a + b;
       }
   }
   Calculator add = new Adder();
```

### You already know some functional interfaces!

| Interface | Its one method | Used in |
|---|---|---|
| `Comparator<T>` | `int compare(T a, T b)` | sorting (Chapter 30) |
| `Runnable` | `void run()` | tasks (Chapter 25) |
| `Comparable<T>` | `int compareTo(T other)` | sorting (Chapter 25) |

---

## 🧰 Part 4: Java's built-in functional interfaces

You don't need to write your own interface every time. Java has ready-made ones in **`java.util.function`**. Learn these **four** — they're used **everywhere**:

| Interface | Method | Input → Output | Think of it as... |
|---|---|---|---|
| **`Predicate<T>`** | `boolean test(T t)` | T → **yes/no** | a **question** ❓ "Is it...?" |
| **`Function<T, R>`** | `R apply(T t)` | T → R | a **machine** 🏭 that turns one thing into another |
| **`Consumer<T>`** | `void accept(T t)` | T → nothing | a **worker** 👷 that **does** something with it |
| **`Supplier<T>`** | `T get()` | nothing → T | a **vending machine** 🥤 that **gives** you something |

### ❓ `Predicate<T>` — a yes/no question

```java
import java.util.function.Predicate;

Predicate<Integer> isEven = n -> n % 2 == 0;
Predicate<String> isLong = s -> s.length() > 5;

System.out.println(isEven.test(4));         // true
System.out.println(isEven.test(7));         // false
System.out.println(isLong.test("banana"));  // true
```

You've already used one! `list.removeIf(...)` takes a **Predicate** (Chapter 30):

```java
names.removeIf(name -> name.length() < 3);   // "remove if this question is true"
```

Predicates can be **combined**:

```java
Predicate<Integer> isPositive = n -> n > 0;
Predicate<Integer> isPositiveEven = isPositive.and(isEven);
Predicate<Integer> isOdd = isEven.negate();

System.out.println(isPositiveEven.test(6));    // true
System.out.println(isPositiveEven.test(-4));   // false
System.out.println(isOdd.test(7));             // true
```

### 🏭 `Function<T, R>` — turns T into R

```java
import java.util.function.Function;

Function<String, Integer> length = s -> s.length();
Function<Integer, Integer> doubleIt = n -> n * 2;
Function<String, String> shout = s -> s.toUpperCase() + "!";

System.out.println(length.apply("hello"));   // 5
System.out.println(doubleIt.apply(21));      // 42
System.out.println(shout.apply("hi"));       // HI!
```

`Function<String, Integer>` = "takes a String, gives back an Integer".

Functions can be **chained** like a factory line 🏭→🏭:

```java
Function<String, Integer> lengthTimesTwo = length.andThen(doubleIt);
System.out.println(lengthTimesTwo.apply("hello"));   // 10  ("hello" → 5 → 10)
```

### 👷 `Consumer<T>` — does something, returns nothing

```java
import java.util.function.Consumer;

Consumer<String> greet = name -> System.out.println("Hello, " + name + "! 👋");
greet.accept("Sara");   // Hello, Sara! 👋
```

You've used it too! `list.forEach(...)` takes a **Consumer**:

```java
List.of("Ali", "Tom").forEach(name -> System.out.println("Hi " + name));
```

### 🥤 `Supplier<T>` — gives something, takes nothing

```java
import java.util.function.Supplier;

Supplier<Double> randomNumber = () -> Math.random();
Supplier<String> greeting = () -> "Good morning! ☀️";

System.out.println(randomNumber.get());   // 0.7342... (different every time)
System.out.println(greeting.get());       // Good morning! ☀️
```

A Supplier is great for **"create it only when needed"** (lazy):

```java
// 🌱 Spring Boot style — the exception is only created IF the student is missing:
Student s = repository.findById(id)
        .orElseThrow(() -> new StudentNotFoundException(id));
//                    └─── a Supplier<Exception>!
```

### More useful ones

| Interface | Method | Example |
|---|---|---|
| `BiFunction<T, U, R>` | `R apply(T t, U u)` | `(a, b) -> a + b` — two inputs |
| `UnaryOperator<T>` | `T apply(T t)` | `s -> s.trim()` — same type in and out |
| `BinaryOperator<T>` | `T apply(T a, T b)` | `(a, b) -> a * b` — like `Integer::sum` in `merge` (Chapter 31)! |
| `BiConsumer<T, U>` | `void accept(T t, U u)` | `(k, v) -> ...` in `map.forEach` (Chapter 31) |
| `IntPredicate`, `ToIntFunction<T>`... | | versions for primitives (faster, no boxing) |

---

## 📦 Part 5: Passing behavior to methods

This is the **real power** of lambdas: you can write a method that takes **behavior** (a function) as a parameter!

```java
import java.util.ArrayList;
import java.util.List;
import java.util.function.Predicate;

public class Filter {

    public static <T> List<T> filter(List<T> items, Predicate<T> rule) {
        List<T> result = new ArrayList<>();
        for (T item : items) {
            if (rule.test(item)) {
                result.add(item);
            }
        }
        return result;
    }

    public static void main(String[] args) {
        List<Integer> numbers = List.of(3, 8, 15, 22, 7, 40, 1);

        System.out.println(filter(numbers, n -> n % 2 == 0));   // [8, 22, 40]
        System.out.println(filter(numbers, n -> n > 10));       // [15, 22, 40]
        System.out.println(filter(numbers, n -> n < 5));        // [3, 1]

        List<String> words = List.of("sun", "rainbow", "sky", "thunder");
        System.out.println(filter(words, w -> w.length() > 3)); // [rainbow, thunder]
        System.out.println(filter(words, w -> w.startsWith("s"))); // [sun, sky]
    }
}
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `Predicate<T> rule` | The method receives a **rule** (a yes/no question). |
| `rule.test(item)` | Ask the question for each item. |
| `filter(numbers, n -> n % 2 == 0)` | **We** decide the rule when we **call** the method. |

👉 **One** `filter` method, **endless** rules. Without lambdas, you'd need a different method for each rule: `filterEven`, `filterBig`, `filterSmall`... 😩

📖 **Story:** A **sieve** 🥣 in the kitchen. The sieve (the `filter` method) is always the same. But you can **change the net** (the lambda) — big holes for pasta, small holes for flour.

> 🚀 You just built a tiny version of **Streams** — Java's built-in tool for this. Next chapter! Streams have `filter`, `map`, `sorted` and much more, ready to use.

---

## 🎯 Part 6: Method references — `::`

When a lambda **only calls one existing method**, you can make it **even shorter** with `::`:

| Lambda | Method reference | Read it as |
|---|---|---|
| `s -> s.toUpperCase()` | `String::toUpperCase` | "call `toUpperCase` on each String" |
| `s -> s.length()` | `String::length` | "the length of each String" |
| `x -> System.out.println(x)` | `System.out::println` | "print each one" |
| `s -> Integer.parseInt(s)` | `Integer::parseInt` | "parse each one" |
| `(a, b) -> Integer.sum(a, b)` | `Integer::sum` | "add them" |
| `name -> new Student(name)` | `Student::new` | "make a new Student from each" |
| `st -> st.name()` | `Student::name` | "the name of each Student" (records!) |

```java
List<String> names = List.of("sara", "tom", "lina");

names.forEach(System.out::println);
// sara
// tom
// lina

Function<String, String> upper = String::toUpperCase;
System.out.println(upper.apply("hello"));   // HELLO
```

### The 4 kinds (just so you recognize them)

| Kind | Example | Means |
|---|---|---|
| Static method | `Integer::parseInt` | `x -> Integer.parseInt(x)` |
| Method of **each** object | `String::length` | `s -> s.length()` |
| Method of **one specific** object | `System.out::println` | `x -> System.out.println(x)` |
| Constructor | `ArrayList::new` | `() -> new ArrayList<>()` |

👉 Now you understand `Comparator.comparing(Student::name)` from Chapter 30: "compare by `name()`"! And `Integer::sum` in `map.merge(word, 1, Integer::sum)` from Chapter 31! 🎉

> 💡 **IntelliJ helps:** When a lambda can be a method reference, IntelliJ shows a gray hint. Press **Alt + Enter** → *Replace lambda with method reference*. ✨

---

## 🔢 Part 7: Comparators with lambdas — sorting made easy

Sorting is where you'll use lambdas **most**:

```java
record Student(String name, int grade, int age) { }

List<Student> students = new ArrayList<>(List.of(
    new Student("Sara", 92, 12),
    new Student("Tom", 75, 13),
    new Student("Ali", 92, 11),
    new Student("Lina", 88, 12)
));
```

```java
// By name (A → Z)
students.sort(Comparator.comparing(Student::name));

// By grade, highest first
students.sort(Comparator.comparing(Student::grade).reversed());

// By grade (highest first), and if equal, by name (A → Z)
students.sort(Comparator.comparing(Student::grade).reversed()
                        .thenComparing(Student::name));

students.forEach(System.out::println);
```

**Output (last sort):**

```
Student[name=Ali, grade=92, age=11]
Student[name=Sara, grade=92, age=12]
Student[name=Lina, grade=88, age=12]
Student[name=Tom, grade=75, age=13]
```

| Method | Meaning |
|---|---|
| `Comparator.comparing(Student::grade)` | sort by grade |
| `.reversed()` | big → small |
| `.thenComparing(Student::name)` | if two grades are equal, sort those by name |
| `Comparator.comparingInt(Student::age)` | a faster version for `int` values |

It reads almost like English! 📖

---

## 🔒 Part 8: Lambdas and outside variables

A lambda can **use** variables from outside it:

```java
int minimum = 50;
List<Integer> scores = List.of(30, 70, 45, 90);
scores.forEach(s -> {
    if (s >= minimum) {
        System.out.println(s + " passed ✅");
    }
});
```

**Output:**

```
70 passed ✅
90 passed ✅
```

### ⚠️ But it can't **change** them

```java
int count = 0;
scores.forEach(s -> count++);   // ❌ error: local variables referenced from a lambda expression must be final or effectively final
```

The outside variable must be **"effectively final"** — it must **never change** after it gets its value. (It doesn't need the word `final`, it just must **behave** like it.)

📖 **Story:** The babysitter can **read** your sticky note 📝 and look at things in the house, but they're **not allowed** to rewrite your diary. 📔

**Fix:** Use a normal loop, or (better!) a Stream: `long count = scores.stream().filter(...).count();` (next chapter).

---

## 💻 Mini project: A tiny rule engine 🎛️

Let's build a discount system where the **rules** are lambdas. Adding a new rule = adding **one line**!

```java
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import java.util.function.Predicate;

public class DiscountRules {

    record Order(String customer, double total, int items, boolean isMember) { }

    record Rule(String name, Predicate<Order> when, Function<Double, Double> discount) { }

    public static void main(String[] args) {
        List<Rule> rules = new ArrayList<>();
        rules.add(new Rule("Members save 10%",   o -> o.isMember(),        t -> t * 0.10));
        rules.add(new Rule("Big order: 5 off",   o -> o.total() > 100,     t -> 5.0));
        rules.add(new Rule("Bulk: 2% per item over 10",
                                                 o -> o.items() > 10,      t -> t * 0.02));

        List<Order> orders = List.of(
            new Order("Sara", 120.0, 3, true),
            new Order("Tom", 40.0, 12, false),
            new Order("Lina", 80.0, 2, false)
        );

        for (Order order : orders) {
            double discount = 0;
            System.out.println("🛒 " + order.customer() + " (" + order.total() + ")");
            for (Rule rule : rules) {
                if (rule.when().test(order)) {
                    double amount = rule.discount().apply(order.total());
                    discount += amount;
                    System.out.printf("   ✅ %-28s -%.2f%n", rule.name(), amount);
                }
            }
            System.out.printf("   💰 Pay: %.2f%n", order.total() - discount);
        }
    }
}
```

**Output:**

```
🛒 Sara (120.0)
   ✅ Members save 10%             -12.00
   ✅ Big order: 5 off             -5.00
   💰 Pay: 103.00
🛒 Tom (40.0)
   ✅ Bulk: 2% per item over 10    -0.80
   💰 Pay: 39.20
🛒 Lina (80.0)
   💰 Pay: 80.00
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `record Rule(String name, Predicate<Order> when, Function<Double, Double> discount)` | A rule **stores two functions** as data! |
| `o -> o.isMember()` | The "when" question (a Predicate). |
| `t -> t * 0.10` | The "how much" calculation (a Function). |
| `rule.when().test(order)` | Ask the question. |
| `rule.discount().apply(order.total())` | Run the calculation. |

👉 **Functions are data** now! You can store them in lists, records and maps, and pass them around. This style is called **functional programming**. 🧠

(Note: the "bulk" rule is simplified — it gives 2% of the total, not per item. Can you fix it in Task 5? 😉)

---

## ✋ Try it yourself

**Task 1:** Write lambdas for these, and test them:
1. A `Predicate<String>` that checks if a String is empty.
2. A `Function<Integer, String>` that turns 5 into `"*****"` (hint: `"*".repeat(n)`).
3. A `Consumer<String>` that prints a String inside a box: `[ hello ]`.
4. A `Supplier<Integer>` that returns a random dice roll 1–6.

<details>
<summary>Click to see the answers</summary>

```java
Predicate<String> isEmpty = s -> s.isEmpty();               // or String::isEmpty
Function<Integer, String> stars = n -> "*".repeat(n);
Consumer<String> boxed = s -> System.out.println("[ " + s + " ]");
Supplier<Integer> dice = () -> (int) (Math.random() * 6) + 1;

System.out.println(isEmpty.test(""));   // true
System.out.println(stars.apply(5));     // *****
boxed.accept("hello");                  // [ hello ]
System.out.println(dice.get());         // 1..6
```

</details>

**Task 2:** Rewrite these lambdas as method references:
1. `s -> s.trim()`
2. `x -> System.out.println(x)`
3. `s -> Double.parseDouble(s)`
4. `p -> p.name()` (for a record `Person`)

<details>
<summary>Click to see the answers</summary>

1. `String::trim`
2. `System.out::println`
3. `Double::parseDouble`
4. `Person::name`

</details>

**Task 3:** Write a method `static void repeat(int times, Runnable action)` that runs the action `times` times. Call it: `repeat(3, () -> System.out.println("Hip hip hooray! 🎉"));`

**Task 4:** Write a generic method `<T, R> List<R> transform(List<T> items, Function<T, R> fn)` that applies `fn` to every item and returns a new list. Test: `transform(List.of("a", "bb", "ccc"), String::length)` → `[1, 2, 3]`.

<details>
<summary>Click to see the answer</summary>

```java
public static <T, R> List<R> transform(List<T> items, Function<T, R> fn) {
    List<R> result = new ArrayList<>();
    for (T item : items) {
        result.add(fn.apply(item));
    }
    return result;
}
```

This is exactly what `stream().map(...)` does — next chapter!

</details>

**Task 5:** In the mini project, add a new rule: "Weekend special: 3 off for orders over 30". Only **one** line in `main` should change!

---

## ⚠️ Common mistakes

### Mistake 1: Using a lambda where no functional interface is expected

```java
var f = x -> x * 2;   // ❌ error: cannot infer type for local variable f (lambda expression needs an explicit target-type)
```

**Fix:** Give it a type: `Function<Integer, Integer> f = x -> x * 2;`

### Mistake 2: Changing an outside variable

```java
int total = 0;
list.forEach(n -> total += n);   // ❌ error: ... must be final or effectively final
```

**Fix:** Use a normal for-each loop, or a stream: `list.stream().mapToInt(n -> n).sum()`.

### Mistake 3: Forgetting `return` in a block lambda

```java
Function<Integer, Integer> f = x -> { x * 2; };          // ❌ error: not a statement
Function<Integer, Integer> f = x -> { return x * 2; };   // ✅
Function<Integer, Integer> f = x -> x * 2;               // ✅ (shortest)
```

### Mistake 4: Brackets with two parameters

```java
a, b -> a + b       // ❌
(a, b) -> a + b     // ✅
```

### Mistake 5: Calling the lambda like a method

```java
Predicate<Integer> isEven = n -> n % 2 == 0;
isEven(4);          // ❌ error: cannot find symbol
isEven.test(4);     // ✅ call the interface's method
```

Remember: `Predicate` → `.test()`, `Function` → `.apply()`, `Consumer` → `.accept()`, `Supplier` → `.get()`.

### Mistake 6: Huge lambdas

A lambda with 20 lines is hard to read. 😵 **Fix:** Move the code into a normal method and use a **method reference**: `list.forEach(this::processItem);`

---

## ✅ Summary

- A **lambda** is a short, nameless function: `(a, b) -> a + b`. 📝
- Forms: `() -> ...`, `x -> ...`, `(a, b) -> ...`, `x -> { ...; return ...; }`.
- Lambdas implement **functional interfaces** (exactly one abstract method).
- Built-in interfaces (`java.util.function`):
  - `Predicate<T>` → `test` → yes/no ❓
  - `Function<T, R>` → `apply` → turns T into R 🏭
  - `Consumer<T>` → `accept` → does something 👷
  - `Supplier<T>` → `get` → gives something 🥤
- **Pass behavior** to methods: `filter(list, n -> n > 10)`.
- **Method references** `::` are shorter lambdas: `String::length`, `System.out::println`, `Student::new`.
- Sort easily: `Comparator.comparing(Student::grade).reversed().thenComparing(Student::name)`.
- Lambdas can **read** outside variables, but not **change** them (effectively final).

---

## ❓ Quiz

1. What is a lambda?
2. What is a functional interface?
3. Which functional interface would you use for "is this number positive?"
4. Which method do you call on a `Function`? On a `Consumer`?
5. Write a lambda that takes two numbers and returns the bigger one.
6. Write `s -> s.toLowerCase()` as a method reference.
7. Why does `list.forEach(n -> count++)` not compile?
8. What does `() -> new ArrayList<>()` take and return? Which interface fits?

<details>
<summary>Click to see the answers</summary>

1. A short function without a name, written with `->`.
2. An interface with exactly one abstract method.
3. `Predicate<Integer>`
4. `apply()` and `accept()`.
5. `(a, b) -> a > b ? a : b` (or `Math::max`)
6. `String::toLowerCase`
7. Lambdas can't change outside local variables — they must be (effectively) final.
8. It takes nothing and returns a new list → `Supplier<List<...>>` (or `ArrayList::new`).

</details>

---

[⬅ Previous chapter](34-generics.md) | [Table of Contents](../README.md) | [Next chapter: Streams ➡](36-streams.md)
