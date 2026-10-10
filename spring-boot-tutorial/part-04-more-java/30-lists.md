# Chapter 30 – Lists (`ArrayList`)

[⬅ Previous chapter](../part-03-objects/29-records.md) | [Table of Contents](../README.md) | [Next chapter ➡](31-maps.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- Why arrays are sometimes **not enough**
- What a **`List`** is, and how **`ArrayList`** works
- How to **add**, **get**, **change**, **remove** and **search** items
- How to **loop** over a list (3 ways)
- **Wrapper classes** (`Integer`, `Double`...) and **autoboxing**
- How to **sort** a list
- **Immutable lists** with `List.of(...)`
- The famous error when you remove items **inside a loop**

> 🌱 **Spring Boot note:** Lists are **everywhere** in Spring Boot. "Give me all students" returns a `List<Student>`. A JSON array `[...]` becomes a `List`. You'll use lists every day!

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Collection** | An object that holds **many** other objects. Lists, sets and maps are collections. |
| **List** | A collection that keeps items **in order**, with an **index**. It can **grow** and **shrink**. Duplicates are allowed. |
| **`ArrayList`** | The most common kind of List. |
| **`<Type>`** | The **type** of the items in the list, like `<String>`. This is called a **generic** (Chapter 34). |
| **Wrapper class** | A class that "wraps" a primitive into an object: `int` → `Integer`. |
| **Autoboxing** | Java **automatically** changes `int` ↔ `Integer` for you. |
| **Immutable list** | A list that **cannot** be changed. |

---

## 📖 Story: The egg box vs. the shopping bag 🥚🛍️

In Chapter 14, an **array** was like an **egg box**: it has a **fixed** number of places. A box for 6 eggs can never hold 7. If you need more, you must buy a **new, bigger box** and move all the eggs. 😩

A **list** is like a **shopping bag** 🛍️:
- Put in **one** more thing? No problem — it **grows**.
- Take something out? It **shrinks**.
- You never have to think about the size. ✨

```
 Array (fixed):    [🥚][🥚][🥚][  ][  ][  ]      ← always 6 places

 List (flexible):  [🍎][🍌][🥛]                  ← 3 items
       add 🧀 →    [🍎][🍌][🥛][🧀]              ← 4 items
    remove 🍌 →    [🍎][🥛][🧀]                  ← 3 items (the others move left!)
```

---

## 😩 Part 1: The problem with arrays

```java
String[] names = new String[3];
names[0] = "Ali";
names[1] = "Sara";
names[2] = "Tom";
names[3] = "Lina";   // 💥 ArrayIndexOutOfBoundsException — no room!
```

Arrays can't grow. And **removing** an item from the middle? You have to move everything by hand. And how many items are **really** used? You need an extra `count` variable (like in our `TodoList` in Chapter 20). 😩

`ArrayList` does all of this **for you**.

---

## 🛍️ Part 2: Your first `ArrayList`

```java
import java.util.ArrayList;
import java.util.List;

public class FirstList {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();

        names.add("Ali");
        names.add("Sara");
        names.add("Tom");
        names.add("Lina");      // no problem — it grows! 🎉

        System.out.println(names);
        System.out.println("Size: " + names.size());
        System.out.println("First: " + names.get(0));
    }
}
```

**Output:**

```
[Ali, Sara, Tom, Lina]
Size: 4
First: Ali
```

### 🔍 Line by line

`List<String> names = new ArrayList<>();`

| Part | Meaning |
|---|---|
| `List` | The **type** of the variable: "a list". `List` is an **interface** (Chapter 25)! |
| `<String>` | "...a list of **Strings**." Only Strings can go in. |
| `names` | The variable name (plural — it holds many!). |
| `new ArrayList<>()` | Create a new, **empty** `ArrayList`. `ArrayList` is a **class** that **implements** the `List` interface. |
| `<>` | The "diamond" 💎. Java **guesses** the type (`String`) from the left side. |

👉 **Why `List` on the left and `ArrayList` on the right?** This is **loose coupling** (Chapter 25)! Your code only depends on the **interface** `List`. If you later want a different kind of list, you change **one** word. Professional Java code almost always looks like this.

| Other lines | Meaning |
|---|---|
| `names.add("Ali");` | Put `"Ali"` at the **end** of the list. |
| `System.out.println(names);` | Lists have a nice `toString()`: `[Ali, Sara, Tom, Lina]`. (No `Arrays.toString` needed!) |
| `names.size()` | How many items. (Arrays: `.length`. Strings: `.length()`. Lists: **`.size()`**. 😅) |
| `names.get(0)` | The item at index 0. (Arrays: `names[0]`. Lists: **`names.get(0)`**.) |

### 📋 Array vs. List — the syntax

| | Array | List |
|---|---|---|
| Create | `String[] a = new String[3];` | `List<String> l = new ArrayList<>();` |
| Add | `a[i] = "x";` (must manage the index) | `l.add("x");` |
| Get | `a[0]` | `l.get(0)` |
| Change | `a[0] = "y";` | `l.set(0, "y");` |
| Size | `a.length` | `l.size()` |
| Print | `Arrays.toString(a)` | `l` (just print it!) |
| Grows? | ❌ no | ✅ yes |

---

## 🧰 Part 3: The most useful List methods

```java
List<String> fruits = new ArrayList<>();
fruits.add("apple");
fruits.add("banana");
fruits.add("cherry");
// fruits = [apple, banana, cherry]
```

### Adding

```java
fruits.add("date");            // at the end       → [apple, banana, cherry, date]
fruits.add(1, "avocado");      // at index 1       → [apple, avocado, banana, cherry, date]
```

`add(index, item)` puts the item **at** that position, and moves the others **to the right**. ➡️

### Getting and changing

```java
String f = fruits.get(2);      // "banana"
fruits.set(0, "apricot");      // replace index 0  → [apricot, avocado, banana, cherry, date]
```

### Removing

```java
fruits.remove("banana");       // remove by VALUE  → [apricot, avocado, cherry, date]
fruits.remove(0);              // remove by INDEX  → [avocado, cherry, date]
```

When you remove, the items after it move **to the left**. ⬅️

### Searching

```java
fruits.contains("cherry");     // true
fruits.indexOf("date");        // 2
fruits.indexOf("mango");       // -1 (not found)
fruits.isEmpty();              // false
```

### Everything else

```java
fruits.size();                 // 3
fruits.clear();                // remove EVERYTHING → []
fruits.isEmpty();              // true
```

### 📋 Cheat sheet

| Method | What it does | Returns |
|---|---|---|
| `add(item)` | add at the end | `true` |
| `add(index, item)` | insert at a position | — |
| `get(index)` | get the item at a position | the item |
| `set(index, item)` | replace the item at a position | the **old** item |
| `remove(index)` | remove at a position | the removed item |
| `remove(item)` | remove the first matching item | `true` if found |
| `size()` | number of items | `int` |
| `isEmpty()` | is it empty? | `boolean` |
| `contains(item)` | is it in the list? | `boolean` |
| `indexOf(item)` | where is it? (−1 = not found) | `int` |
| `clear()` | remove everything | — |
| `addAll(otherList)` | add all items of another list | `boolean` |

> 💡 `contains`, `indexOf` and `remove(item)` use **`equals()`** to find the item (Chapter 20). For your own classes, write `equals()` — or use a **record**, which has it for free!

---

## 🔁 Part 4: Looping over a list

```java
List<String> names = new ArrayList<>(List.of("Ali", "Sara", "Tom"));
```

### Way 1: for-each (most common ✅)

```java
for (String name : names) {
    System.out.println("Hello, " + name);
}
```

### Way 2: normal `for` with index (when you need the position)

```java
for (int i = 0; i < names.size(); i++) {
    System.out.println((i + 1) + ". " + names.get(i));
}
```

**Output:**

```
1. Ali
2. Sara
3. Tom
```

### Way 3: `forEach` with a lambda (a sneak peek — Chapter 35)

```java
names.forEach(name -> System.out.println(name));
```

Short and modern! You'll understand `name -> ...` in Chapter 35. 😊

---

## 📦 Part 5: Lists of numbers — wrapper classes

Try this:

```java
List<int> numbers = new ArrayList<>();   // ❌ error: unexpected type — required: reference, found: int
```

😮 **Lists can only hold objects, not primitives!** (`int`, `double`, `boolean`, `char` are primitives — Chapter 7.)

The fix: every primitive has a **wrapper class** — an object version of it:

| Primitive | Wrapper class |
|---|---|
| `int` | **`Integer`** ⚠️ |
| `double` | `Double` |
| `long` | `Long` |
| `boolean` | `Boolean` |
| `char` | **`Character`** ⚠️ |

```java
List<Integer> numbers = new ArrayList<>();
numbers.add(10);     // Java turns 10 (int) into an Integer automatically
numbers.add(20);
numbers.add(30);

int first = numbers.get(0);   // Java turns the Integer back into an int automatically
int sum = 0;
for (int n : numbers) {
    sum += n;
}
System.out.println("Sum: " + sum);   // Sum: 60
```

### 🎁 Autoboxing

Java **automatically** converts between `int` and `Integer`:

| Direction | Name | Example |
|---|---|---|
| `int` → `Integer` | **autoboxing** 📦 (put it in a box) | `numbers.add(10);` |
| `Integer` → `int` | **unboxing** 📭 (take it out of the box) | `int x = numbers.get(0);` |

You rarely need to think about it. Just remember: **in `< >`, use the wrapper class name**.

### ⚠️ Trap: `remove` with Integer lists

```java
List<Integer> nums = new ArrayList<>(List.of(10, 20, 30));
nums.remove(1);                     // removes INDEX 1 → [10, 30]
nums.remove(Integer.valueOf(10));   // removes the VALUE 10 → [30]
```

`remove(1)` with an `int` means "remove at index 1". To remove the **value**, wrap it: `Integer.valueOf(10)`.

### ⚠️ Trap: comparing Integers with `==`

```java
Integer a = 1000;
Integer b = 1000;
System.out.println(a == b);        // false 😱 (two different objects!)
System.out.println(a.equals(b));   // true ✅
```

`Integer` is an **object**, so `==` compares **references** (Chapter 18). Use `.equals()` — or unbox to `int` first.

---

## 🏗️ Part 6: Creating lists quickly

### `List.of(...)` — an **immutable** list

```java
List<String> colors = List.of("red", "green", "blue");
System.out.println(colors);   // [red, green, blue]

colors.add("yellow");         // 💥 UnsupportedOperationException
```

`List.of` makes a list that **can't change** (immutable — like records!). Great for **fixed** data.

### A changeable copy

```java
List<String> colors = new ArrayList<>(List.of("red", "green", "blue"));
colors.add("yellow");   // ✅ works
```

`new ArrayList<>(otherList)` makes a **new, changeable** list with the same items.

### From an array

```java
String[] array = { "a", "b", "c" };
List<String> list = new ArrayList<>(Arrays.asList(array));
// or: new ArrayList<>(List.of(array));
```

### Back to an array (sometimes needed)

```java
String[] back = list.toArray(new String[0]);
```

### 📋 Which one?

| Code | Can change? | Use it for |
|---|---|---|
| `new ArrayList<>()` | ✅ | an empty list you will fill |
| `new ArrayList<>(List.of(...))` | ✅ | a changeable list with starting items |
| `List.of(...)` | ❌ | fixed data, constants, return values |
| `List.copyOf(list)` | ❌ | a safe, unchangeable **copy** (great in records! — Chapter 29) |

---

## 🔢 Part 7: Sorting

### Natural order (numbers small → big, Strings A → Z)

```java
List<String> names = new ArrayList<>(List.of("Tom", "Ali", "Sara", "Ben"));
Collections.sort(names);
System.out.println(names);   // [Ali, Ben, Sara, Tom]

List<Integer> nums = new ArrayList<>(List.of(5, 3, 9, 1));
nums.sort(null);             // null = "use the natural order"
System.out.println(nums);    // [1, 3, 5, 9]
```

`Collections` (with an **s**) is a **utility class** (Chapter 27) full of helpers for collections. Import: `java.util.Collections`.

### Reverse order

```java
nums.sort(Comparator.reverseOrder());
System.out.println(nums);   // [9, 5, 3, 1]
```

### Sorting your own objects — with a `Comparator`

```java
public record Student(String name, int grade) { }
```

```java
List<Student> students = new ArrayList<>(List.of(
    new Student("Sara", 92),
    new Student("Tom", 75),
    new Student("Ali", 88)
));

students.sort(Comparator.comparing(Student::name));
System.out.println(students);
// [Student[name=Ali, grade=88], Student[name=Sara, grade=92], Student[name=Tom, grade=75]]

students.sort(Comparator.comparing(Student::grade).reversed());
System.out.println(students);
// [Student[name=Sara, grade=92], Student[name=Ali, grade=88], Student[name=Tom, grade=75]]
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `Comparator` | An object that knows **how to compare** two things. Import `java.util.Comparator`. |
| `Comparator.comparing(Student::name)` | "Compare students **by their name**." |
| `Student::name` | A **method reference**: "the `name()` method of Student". (Chapter 35 explains it. For now: read it as "**by name**".) |
| `.reversed()` | Turn the order around: big → small. |

👉 This is much easier than implementing `Comparable` (Chapter 25), and you can sort **in many different ways**.

### Other useful `Collections` helpers

```java
Collections.reverse(list);     // reverse the order
Collections.shuffle(list);     // random order 🎲
Collections.max(nums);         // biggest
Collections.min(nums);         // smallest
Collections.frequency(list, "x");   // how many times "x" appears
```

---

## 💥 Part 8: Removing inside a loop — the famous error

You want to remove all short names:

```java
List<String> names = new ArrayList<>(List.of("Al", "Sara", "Bo", "Tom", "Lina"));

for (String name : names) {
    if (name.length() < 3) {
        names.remove(name);   // 💥
    }
}
```

```
Exception in thread "main" java.util.ConcurrentModificationException
```

😱 You **can't change a list while a for-each loop is walking through it**. 🚶‍♀️ It's like pulling a rug while someone is walking on it!

### ✅ Fix 1: `removeIf` (best, short and clear)

```java
names.removeIf(name -> name.length() < 3);
System.out.println(names);   // [Sara, Tom, Lina]
```

"Remove every name **if** its length is less than 3." (Another lambda — Chapter 35.)

### ✅ Fix 2: an `Iterator`

```java
Iterator<String> it = names.iterator();
while (it.hasNext()) {
    String name = it.next();
    if (name.length() < 3) {
        it.remove();   // safe: the iterator removes it
    }
}
```

An **Iterator** is the "walker" 🚶 that a for-each loop uses secretly. If **it** removes the item, everything stays in order.

### ✅ Fix 3: loop backwards with an index

```java
for (int i = names.size() - 1; i >= 0; i--) {
    if (names.get(i).length() < 3) {
        names.remove(i);
    }
}
```

Going backwards, removing an item doesn't change the indexes of the items you haven't checked yet.

👉 **Use `removeIf`.** It's the modern way.

---

## 🧩 Part 9: Lists of objects, and lists in classes

```java
public record Task(String title, boolean done) { }
```

```java
public class TodoList {
    private final List<Task> tasks = new ArrayList<>();

    public void add(String title) {
        tasks.add(new Task(title, false));
    }

    public void complete(String title) {
        for (int i = 0; i < tasks.size(); i++) {
            Task t = tasks.get(i);
            if (t.title().equalsIgnoreCase(title)) {
                tasks.set(i, new Task(t.title(), true));   // records are immutable → replace
                return;
            }
        }
    }

    public List<Task> getTasks() {
        return List.copyOf(tasks);   // give a read-only copy, not our private list!
    }

    public int countOpen() {
        int count = 0;
        for (Task t : tasks) {
            if (!t.done()) {
                count++;
            }
        }
        return count;
    }
}
```

```java
TodoList todo = new TodoList();
todo.add("Learn lists");
todo.add("Buy milk");
todo.add("Call grandma");
todo.complete("buy milk");

for (Task t : todo.getTasks()) {
    System.out.println((t.done() ? "[x] " : "[ ] ") + t.title());
}
System.out.println(todo.countOpen() + " tasks left");
```

**Output:**

```
[ ] Learn lists
[x] Buy milk
[ ] Call grandma
2 tasks left
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `private final List<Task> tasks = new ArrayList<>();` | The list is `final` (the **variable** can't point to another list), but you **can** add and remove items. |
| `return List.copyOf(tasks);` | **Encapsulation** (Chapter 21): give a **read-only copy**, so nobody outside can change our private list. |
| No `count` variable, no fixed size | Compare with Chapter 20's `TodoList` — so much simpler! 🎉 |

---

## 💻 Mini project: Class grade book 📊

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class GradeBook {

    record Student(String name, int score) { }

    public static void main(String[] args) {
        List<Student> students = new ArrayList<>();
        students.add(new Student("Sara", 92));
        students.add(new Student("Tom", 58));
        students.add(new Student("Ali", 75));
        students.add(new Student("Lina", 88));
        students.add(new Student("Ben", 45));

        // 1. Average
        int sum = 0;
        for (Student s : students) {
            sum += s.score();
        }
        double average = (double) sum / students.size();
        System.out.printf("Average: %.1f%n", average);

        // 2. Who passed?
        List<String> passed = new ArrayList<>();
        for (Student s : students) {
            if (s.score() >= 60) {
                passed.add(s.name());
            }
        }
        System.out.println("Passed: " + passed);

        // 3. Ranking
        students.sort(Comparator.comparing(Student::score).reversed());
        System.out.println("Ranking:");
        for (int i = 0; i < students.size(); i++) {
            Student s = students.get(i);
            System.out.println("  " + (i + 1) + ". " + s.name() + " (" + s.score() + ")");
        }

        // 4. Remove the failed students
        students.removeIf(s -> s.score() < 60);
        System.out.println("Still in class: " + students.size());

        // 5. Names in alphabetical order
        List<String> names = new ArrayList<>();
        for (Student s : students) {
            names.add(s.name());
        }
        Collections.sort(names);
        System.out.println("Alphabetical: " + names);
    }
}
```

**Output:**

```
Average: 71.6
Passed: [Sara, Ali, Lina]
Ranking:
  1. Sara (92)
  2. Lina (88)
  3. Ali (75)
  4. Tom (58)
  5. Ben (45)
Still in class: 3
Alphabetical: [Ali, Lina, Sara]
```

> 💡 `record Student(...)` is written **inside** the `GradeBook` class. This is called a **nested** record — handy for small helper types that only one class uses.

In Chapter 36 (**Streams**), you'll learn to write steps 1, 2 and 5 in **one line each**! 🚀

---

## ✋ Try it yourself

**Task 1:** Make a `List<String>` of 5 cities. Add one at the beginning, remove the third one, and print the list and its size.

**Task 2:** Make a `List<Integer>` with the numbers 1 to 20 (use a loop). Then remove all **even** numbers with `removeIf`. Print the list.

<details>
<summary>Click to see the answer</summary>

```java
List<Integer> numbers = new ArrayList<>();
for (int i = 1; i <= 20; i++) {
    numbers.add(i);
}
numbers.removeIf(n -> n % 2 == 0);
System.out.println(numbers);   // [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
```

</details>

**Task 3:** Write a method `List<String> longWords(List<String> words, int minLength)` that returns a **new** list with only the words that have at least `minLength` letters.

<details>
<summary>Click to see the answer</summary>

```java
public static List<String> longWords(List<String> words, int minLength) {
    List<String> result = new ArrayList<>();
    for (String w : words) {
        if (w.length() >= minLength) {
            result.add(w);
        }
    }
    return result;
}
```

</details>

**Task 4:** Ask the user (with `Scanner`) to type names, one per line, until they type `done`. Store them in a list. Then print them **sorted**, with a number in front.

**Task 5:** Write a method that removes **duplicates** from a list while keeping the order: `[a, b, a, c, b]` → `[a, b, c]`. (Hint: build a new list, and only add an item if the new list doesn't `contains` it yet. In Chapter 32 you'll learn a faster way!)

---

## ⚠️ Common mistakes

### Mistake 1: Primitives in `< >`

```java
List<int> nums;       // ❌ error: unexpected type
List<Integer> nums;   // ✅
```

### Mistake 2: Using array syntax on a list

```java
names[0]          // ❌ error: array required, but List<String> found
names.get(0)      // ✅
names.length      // ❌
names.size()      // ✅
```

### Mistake 3: Index out of bounds

```java
List<String> l = new ArrayList<>();
l.get(0);   // 💥 IndexOutOfBoundsException: Index 0 out of bounds for length 0
```

Check `isEmpty()` or `size()` first.

### Mistake 4: Changing a `List.of(...)` list

```java
List<String> l = List.of("a", "b");
l.add("c");   // 💥 UnsupportedOperationException
```

**Fix:** `new ArrayList<>(List.of("a", "b"))`.

### Mistake 5: Removing in a for-each loop

`ConcurrentModificationException` — use `removeIf` (Part 8).

### Mistake 6: Forgetting the imports

```java
import java.util.ArrayList;
import java.util.List;
```

(IntelliJ: **Alt + Enter**.)

### Mistake 7: `contains` doesn't find your object

```java
class Book { String title; ... }   // no equals()!
list.contains(new Book("Java"));   // false 😕
```

**Fix:** Write `equals()`/`hashCode()` — or use a **record**.

---

## ✅ Summary

- A **List** keeps items **in order**, can **grow** and **shrink**, and allows duplicates.
- Create: `List<String> names = new ArrayList<>();` — the interface `List` on the left, the class `ArrayList` on the right.
- Methods: `add`, `get`, `set`, `remove`, `size`, `isEmpty`, `contains`, `indexOf`, `clear`.
- Lists hold **objects** only → use **wrapper classes**: `Integer`, `Double`, `Boolean`, `Character`. **Autoboxing** converts automatically.
- `List.of(...)` → **immutable**. `new ArrayList<>(List.of(...))` → changeable.
- Sort: `Collections.sort(list)`, `list.sort(Comparator.comparing(Student::name))`, `.reversed()`.
- **Don't remove inside a for-each loop** → use `removeIf(...)`.
- Return `List.copyOf(...)` from getters to protect private lists.

---

## ❓ Quiz

1. What is the main advantage of a List over an array?
2. How do you get the number of items in a List?
3. Why can't you write `List<int>`?
4. What does `list.add(0, "x")` do?
5. What's the difference between `List.of("a")` and `new ArrayList<>(List.of("a"))`?
6. What happens if you remove items from a list inside a for-each loop over it?
7. How do you sort a list of `Student` records by grade, highest first?
8. `List<Integer> l = new ArrayList<>(List.of(5, 6, 7)); l.remove(1);` — what is `l` now?

<details>
<summary>Click to see the answers</summary>

1. It can grow and shrink automatically.
2. `list.size()`
3. Lists can only hold objects. Use the wrapper class `Integer`.
4. It inserts `"x"` at index 0 (the beginning) and moves the other items to the right.
5. The first can't be changed (immutable). The second can.
6. `ConcurrentModificationException`. Use `removeIf` instead.
7. `students.sort(Comparator.comparing(Student::grade).reversed());`
8. `[5, 7]` — `remove(1)` removes **index** 1.

</details>

---

[⬅ Previous chapter](../part-03-objects/29-records.md) | [Table of Contents](../README.md) | [Next chapter: Maps ➡](31-maps.md)
