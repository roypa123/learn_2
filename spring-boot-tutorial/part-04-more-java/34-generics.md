# Chapter 34 – Generics: The `<...>` Signs

[⬅ Previous chapter](33-exceptions.md) | [Table of Contents](../README.md) | [Next chapter ➡](35-lambdas.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- **Why** generics exist (type safety!)
- How to **read** generic types like `List<String>` and `Map<String, List<Integer>>`
- How to write your **own generic class**: `Box<T>`
- How to write **generic methods**: `<T> T firstOf(List<T> list)`
- **Bounded types**: `<T extends Number>`
- **Wildcards**: `<?>`, `<? extends T>`, `<? super T>` (just enough to read them)
- How to read Spring Boot code like `JpaRepository<Student, Long>` 🌱

> 💡 This chapter is a bit more **abstract**. The most important goal: be able to **read** and **use** generic types confidently. Writing complex generic code yourself is less common. Don't worry if wildcards feel strange at first! 😊

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Generic** | A class or method that works with **any type**, chosen later. Like a template with a blank for the type. |
| **Type parameter** | The **placeholder** for a type, like `T`. Written in `< >`. |
| **Type argument** | The **real type** you put in: `String` in `List<String>`. |
| **Type safety** | The compiler **checks** that you only put the right type in. Mistakes are caught early. |
| **Bounded type** | A type parameter with a **limit**: `<T extends Number>` = "T must be a Number". |
| **Wildcard** | The `?` sign: "some type, I don't know which". |
| **Raw type** | A generic class used **without** `< >` (old code — avoid!). |

---

## 📖 Story: The labeled lunch box 🍱

At school, every child has a **lunch box**. Some lunch boxes are **labeled**:

- 🍎 "**FRUIT ONLY**" — you can only put fruit in. If you try to put a sandwich in, the teacher stops you **at the door**.
- 🥪 "**SANDWICHES ONLY**"

It's the **same kind** of box. The **label** says what goes inside.

When you open a "FRUIT ONLY" box, you **know** you'll find fruit. No surprises — no worm 🐛, no sock 🧦.

**Generics** are the **labels** on your boxes:

```
 List<String>    → a list labeled "Strings only"
 List<Integer>   → a list labeled "Integers only"
 Box<Apple>      → a box labeled "Apples only"
```

---

## 😩 Part 1: Life before generics

Before Java 5 (2004), lists had **no labels**. A list could hold **any** `Object`:

```java
List list = new ArrayList();      // no <...> — a "raw type"
list.add("Sara");
list.add(42);                      // 😱 a number in a list of names!
list.add(new Dog("Rex"));          // 😱😱 a dog?!

String name = (String) list.get(0);   // you must CAST every time
String oops = (String) list.get(1);   // 💥 ClassCastException at RUN time!
```

Problems:
1. You can put **anything** in. Mistakes are **not caught** by the compiler.
2. You must **cast** every time you take something out.
3. Wrong casts **crash** while the program runs. 💥

### ✅ With generics

```java
List<String> names = new ArrayList<>();
names.add("Sara");
names.add(42);                     // ❌ COMPILE error: int cannot be converted to String

String name = names.get(0);        // ✅ no cast needed — Java KNOWS it's a String
```

| | Without generics | With generics |
|---|---|---|
| Wrong type added | 💥 crash later, at run time | ❌ error **now**, at compile time ✅ |
| Taking items out | needs a cast | no cast |
| Reading the code | "a list of... what?" 🤷 | "a list of Strings" 📖 |

👉 **Generics move errors from run time to compile time.** That's **type safety**. 🛡️

---

## 📖 Part 2: Reading generic types

You've used generics since Chapter 30! Let's learn to **read** them like sentences.

| Code | Read it as |
|---|---|
| `List<String>` | "a list **of** Strings" |
| `Set<Integer>` | "a set **of** Integers" |
| `Map<String, Double>` | "a map **from** String **to** Double" |
| `Map<Integer, List<String>>` | "a map from Integer to (a list of Strings)" |
| `List<List<Integer>>` | "a list of (lists of Integers)" — like a 2D table |
| `Comparable<Student>` | "comparable **with** Students" |
| `Optional<User>` | "maybe a User" (Chapter 37) |
| `JpaRepository<Student, Long>` | "a repository **for** Students, whose IDs are Longs" 🌱 |

> 💡 **Tip:** Read from the **outside in**, like opening Russian dolls 🪆: `Map<String, List<Integer>>` → a Map → whose keys are Strings → and whose values are Lists → of Integers.

### The diamond `<>`

```java
Map<String, List<Integer>> scores = new HashMap<>();
```

On the right side, `<>` (the **diamond** 💎) means: "Java, use the same types as on the left." You don't need to write them twice.

---

## 📦 Part 3: Your own generic class

Let's build a **box** that can hold **one** thing of **any** type.

### Without generics (one box per type 😩)

```java
class StringBox { private String item; ... }
class IntegerBox { private Integer item; ... }
class DogBox { private Dog item; ... }
// ... a new class for every type?! 😵
```

### With generics (one box for all types 🎉)

```java
public class Box<T> {
    private T item;

    public void put(T item) {
        this.item = item;
    }

    public T get() {
        return item;
    }

    public boolean isEmpty() {
        return item == null;
    }

    @Override
    public String toString() {
        return "Box[" + item + "]";
    }
}
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `class Box<T>` | "Box is a generic class. **`T`** is a **placeholder** for a type that will be chosen later." |
| `private T item;` | The field's type is "whatever T will be". |
| `void put(T item)` | Accepts a T. |
| `T get()` | Returns a T. |

### Using it

```java
Box<String> nameBox = new Box<>();
nameBox.put("Sara");
String name = nameBox.get();            // no cast!
System.out.println(name.toUpperCase()); // SARA

Box<Integer> numberBox = new Box<>();
numberBox.put(42);
int n = numberBox.get() + 8;            // 50

nameBox.put(42);                        // ❌ error: incompatible types: int cannot be converted to String
```

When you write `Box<String>`, Java **replaces** every `T` with `String` (in its head 🧠):

```
 class Box<T>              →     Box<String>
   T item                  →       String item
   void put(T item)        →       void put(String item)
   T get()                 →       String get()
```

**One** class, **any** type, **fully** type-safe. ✨

### 🔤 Names for type parameters

By tradition, type parameters are **one capital letter**:

| Letter | Usually means | Example |
|---|---|---|
| `T` | **T**ype | `Box<T>` |
| `E` | **E**lement (in collections) | `List<E>` |
| `K` | **K**ey | `Map<K, V>` |
| `V` | **V**alue | `Map<K, V>` |
| `R` | **R**esult / return | `Function<T, R>` |
| `ID` | an ID type (Spring) | `CrudRepository<T, ID>` |

### Many type parameters: a `Pair`

```java
public record Pair<A, B>(A first, B second) { }
```

Yes — **records can be generic** too!

```java
Pair<String, Integer> nameAndAge = new Pair<>("Sara", 12);
System.out.println(nameAndAge.first());    // Sara
System.out.println(nameAndAge.second());   // 12

Pair<String, Boolean> answer = new Pair<>("Is Java fun?", true);
System.out.println(answer);                // Pair[first=Is Java fun?, second=true]
```

Great for returning **two values** from a method! 🎁

---

## 🛠️ Part 4: Generic methods

A **method** can also be generic, even in a normal class:

```java
public class ListUtils {

    public static <T> T firstOrDefault(List<T> list, T defaultValue) {
        if (list.isEmpty()) {
            return defaultValue;
        }
        return list.get(0);
    }

    public static <T> List<T> repeat(T item, int times) {
        List<T> result = new ArrayList<>();
        for (int i = 0; i < times; i++) {
            result.add(item);
        }
        return result;
    }
}
```

### 🔍 Line by line

`public static <T> T firstOrDefault(List<T> list, T defaultValue)`

| Part | Meaning |
|---|---|
| `<T>` before the return type | "This **method** has its own type parameter `T`." ⚠️ It goes **before** the return type. |
| `T` (return type) | It returns a T. |
| `List<T> list, T defaultValue` | It takes a list of T and a T. |

### Using it — Java guesses `T`

```java
List<String> names = List.of("Ali", "Sara");
List<Integer> empty = List.of();

String first = ListUtils.firstOrDefault(names, "nobody");   // T = String → "Ali"
Integer num = ListUtils.firstOrDefault(empty, 0);           // T = Integer → 0

List<String> echo = ListUtils.repeat("hi", 3);              // [hi, hi, hi]
List<Character> stars = ListUtils.repeat('*', 5);           // [*, *, *, *, *]
```

You don't write the type — Java **figures it out** from the arguments. This is called **type inference**. 🧠

> 💡 You've used generic methods many times: `List.of(...)`, `Map.of(...)`, `Collections.max(...)`, `Arrays.asList(...)` are all generic methods!

---

## 🚧 Part 5: Bounded types — `<T extends Something>`

What if we want a method that adds up numbers?

```java
public static <T> double sum(List<T> list) {
    double total = 0;
    for (T item : list) {
        total += item.doubleValue();   // ❌ error: cannot find symbol — T could be ANYTHING (a Dog?)
    }
    return total;
}
```

Java doesn't know that `T` is a number. A `Dog` has no `doubleValue()`! 🐕

### ✅ Add a bound

```java
public static <T extends Number> double sum(List<T> list) {
    double total = 0;
    for (T item : list) {
        total += item.doubleValue();   // ✅ every Number has doubleValue()
    }
    return total;
}
```

| Part | Meaning |
|---|---|
| `<T extends Number>` | "T can be **any type**, as long as it **is a** `Number` (or a child of Number)." |

`Integer`, `Double`, `Long` are all children of `Number` (Chapter 22).

```java
System.out.println(sum(List.of(1, 2, 3)));          // 6.0   (T = Integer)
System.out.println(sum(List.of(1.5, 2.5)));         // 4.0   (T = Double)
System.out.println(sum(List.of("a", "b")));         // ❌ error — String is not a Number
```

> 💡 In generics, `extends` is used for **both** classes and interfaces. `<T extends Comparable<T>>` means "T must implement Comparable".

### Example: find the biggest of anything comparable

```java
public static <T extends Comparable<T>> T max(List<T> list) {
    T best = list.get(0);
    for (T item : list) {
        if (item.compareTo(best) > 0) {
            best = item;
        }
    }
    return best;
}
```

```java
System.out.println(max(List.of(3, 9, 2)));               // 9
System.out.println(max(List.of("pear", "apple", "fig"))); // pear  (alphabetically last)
```

It works for **any** type that can compare itself (Chapter 25)! 🎉

---

## ❓ Part 6: Wildcards — `?`

You'll **see** wildcards in Java and Spring code. Here's how to **read** them.

### The surprising problem

```java
List<Integer> ints = List.of(1, 2, 3);
List<Number> nums = ints;   // ❌ error: incompatible types
```

😮 But an `Integer` **is a** `Number`! Why isn't a list of Integers a list of Numbers?

📖 **Story:** A **basket of apples** 🍎 is **not** a "basket of fruit" that anyone can put **any** fruit into. If it were, someone could put a **banana** 🍌 into your apple basket! Java protects you from that.

### `<? extends T>` — "T or any child" (for **reading**)

```java
public static double total(List<? extends Number> numbers) {
    double sum = 0;
    for (Number n : numbers) {
        sum += n.doubleValue();
    }
    return sum;
}
```

```java
total(List.of(1, 2, 3));        // ✅ List<Integer>
total(List.of(1.5, 2.5));       // ✅ List<Double>
```

`List<? extends Number>` = "a list of **some kind** of Number". You can **read** Numbers from it. ✅ You **can't add** to it (Java doesn't know the exact type — maybe it's Integers, and you'd add a Double!).

### `<? super T>` — "T or any parent" (for **writing**)

```java
public static void addNumbers(List<? super Integer> list) {
    list.add(1);
    list.add(2);
}
```

```java
List<Number> nums = new ArrayList<>();
List<Object> objs = new ArrayList<>();
addNumbers(nums);   // ✅
addNumbers(objs);   // ✅
```

`List<? super Integer>` = "a list that can **hold** Integers". You can **add** Integers to it. ✅

### `<?>` — "any type"

```java
public static void printAll(List<?> list) {
    for (Object item : list) {
        System.out.println(item);
    }
}
```

"A list of **something**" — you can only read items as `Object`.

### 📋 Simple rule: **PECS** 🧠

| Wildcard | Memory trick | You can... |
|---|---|---|
| `<? extends T>` | **P**roducer **E**xtends — it **gives** you Ts | **read** ✅, not add ❌ |
| `<? super T>` | **C**onsumer **S**uper — it **takes** Ts | **add** ✅, read only as Object |
| `<?>` | anything | read as Object |

👉 **Beginner tip:** You don't need to write wildcards often. Just recognize them when you see them in documentation — for example `Collections.sort(List<T> list)` or `addAll(Collection<? extends E> c)`. Now you can read it: "add all items from a collection of E or any child of E". ✅

---

## ⚠️ Part 7: Limits of generics

### Only object types

```java
List<int> x;        // ❌ — use List<Integer>  (Chapter 30)
Box<double> b;      // ❌ — use Box<Double>
```

### Type erasure (just know it exists)

The type labels exist only for the **compiler**. At run time, `List<String>` and `List<Integer>` are both just `List`. This is called **type erasure**. Because of it:

```java
if (list instanceof List<String>) { }   // ❌ error: can't check generic type at run time
new T();                                 // ❌ error: can't create a T — Java doesn't know what T is at run time
```

You rarely hit these limits as a beginner. 😊

### Don't use raw types

```java
List list = new ArrayList();   // ⚠️ raw type — no type safety! IntelliJ shows a warning.
List<String> list = new ArrayList<>();   // ✅
```

---

## 🌱 Part 8: Generics in Spring Boot

Now you can **read** this Spring Boot code! 🎉

```java
public interface StudentRepository extends JpaRepository<Student, Long> {
}
```

| Part | Meaning |
|---|---|
| `interface StudentRepository` | Our own interface. |
| `extends JpaRepository<Student, Long>` | Spring's generic interface. It's declared like `JpaRepository<T, ID>`. Here: `T = Student` (what we store), `ID = Long` (the type of the ID). |

Because of generics, Spring gives you methods with the **right types**:

```java
Student s = studentRepository.findById(5L).orElseThrow();  // returns a Student, not an Object!
List<Student> all = studentRepository.findAll();           // a List of Students
studentRepository.save(new Student("Sara"));               // only accepts Students
```

And in web code:

```java
public ResponseEntity<List<StudentDto>> getAll() { ... }
```

Read it: "returns a **response** containing a **list of StudentDtos**". 📖

Generics make Spring's tools **reusable** for **your** classes — one `JpaRepository` works for Students, Courses, Teachers... just like our `Box<T>`. 📦

---

## 💻 Mini project: A generic cache 🗃️

A **cache** remembers results so you don't have to calculate them again. Let's make one that works for **any** key and value type:

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class Cache<K, V> {
    private final Map<K, V> storage = new LinkedHashMap<>();
    private final int maxSize;
    private int hits = 0;
    private int misses = 0;

    public Cache(int maxSize) {
        this.maxSize = maxSize;
    }

    public void put(K key, V value) {
        if (storage.size() >= maxSize && !storage.containsKey(key)) {
            K oldest = storage.keySet().iterator().next();
            storage.remove(oldest);
            System.out.println("   (removed oldest: " + oldest + ")");
        }
        storage.put(key, value);
    }

    public V get(K key) {
        if (storage.containsKey(key)) {
            hits++;
            return storage.get(key);
        }
        misses++;
        return null;
    }

    public String stats() {
        return "size=" + storage.size() + ", hits=" + hits + ", misses=" + misses;
    }
}
```

```java
public class CacheDemo {
    public static void main(String[] args) {
        Cache<String, Integer> wordLengths = new Cache<>(2);
        wordLengths.put("hello", 5);
        wordLengths.put("java", 4);
        wordLengths.put("spring", 6);           // too many → removes the oldest

        System.out.println(wordLengths.get("java"));    // 4
        System.out.println(wordLengths.get("hello"));   // null (was removed)
        System.out.println(wordLengths.stats());

        Cache<Integer, String> romanNumbers = new Cache<>(10);
        romanNumbers.put(4, "IV");
        romanNumbers.put(9, "IX");
        String nine = romanNumbers.get(9);              // no cast needed!
        System.out.println(nine + " — " + romanNumbers.stats());
    }
}
```

**Output:**

```
   (removed oldest: hello)
4
null
size=2, hits=1, misses=1
IX — size=2, hits=1, misses=0
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `class Cache<K, V>` | Two type parameters: key type and value type. |
| `Map<K, V> storage` | Inside, we use a generic Map with the same types. |
| `Cache<String, Integer>` | A cache from words to numbers. |
| `Cache<Integer, String>` | The **same class**, now from numbers to words. |
| `String nine = romanNumbers.get(9);` | Type-safe: Java knows it returns a String. |

> 🌱 Spring Boot has a real caching system (`@Cacheable`) that works on this idea — it remembers method results.

---

## ✋ Try it yourself

**Task 1:** Read these types out loud (in words):
1. `List<Double>`
2. `Map<String, Set<String>>`
3. `Pair<Integer, List<String>>`
4. `Box<Box<String>>`

<details>
<summary>Click to see the answers</summary>

1. A list of Doubles.
2. A map from String to (a set of Strings).
3. A pair of an Integer and (a list of Strings).
4. A box containing a box containing a String. 📦📦

</details>

**Task 2:** Write a generic record `Triple<A, B, C>(A first, B second, C third)`. Create a triple of a name, an age and a boolean.

**Task 3:** Write a generic method `<T> void swap(List<T> list, int i, int j)` that swaps two items in a list.

<details>
<summary>Click to see the answer</summary>

```java
public static <T> void swap(List<T> list, int i, int j) {
    T temp = list.get(i);
    list.set(i, list.get(j));
    list.set(j, temp);
}

// in main:
List<String> letters = new ArrayList<>(List.of("a", "b", "c"));
swap(letters, 0, 2);
System.out.println(letters);   // [c, b, a]
```

</details>

**Task 4:** Write a generic method `<T> int countMatches(List<T> list, T target)` that counts how many items are `equals` to `target`.

**Task 5:** Write `<T extends Comparable<T>> boolean isSorted(List<T> list)` that returns `true` if the list is in order.

<details>
<summary>Click to see the answer</summary>

```java
public static <T extends Comparable<T>> boolean isSorted(List<T> list) {
    for (int i = 1; i < list.size(); i++) {
        if (list.get(i - 1).compareTo(list.get(i)) > 0) {
            return false;
        }
    }
    return true;
}

// isSorted(List.of(1, 2, 3))       → true
// isSorted(List.of("b", "a"))      → false
```

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Primitives in `< >`

```java
Box<int> b;       // ❌
Box<Integer> b;   // ✅
```

### Mistake 2: Raw types

```java
List names = new ArrayList();   // ⚠️ no type safety
```

**Fix:** Always write the type: `List<String> names = new ArrayList<>();`

### Mistake 3: `<T>` in the wrong place for generic methods

```java
public static T first<T>(List<T> list)   // ❌
public static <T> T first(List<T> list)  // ✅  <T> goes BEFORE the return type
```

### Mistake 4: Expecting `List<Integer>` to be a `List<Number>`

```java
List<Number> nums = new ArrayList<Integer>();   // ❌ error
```

**Fix:** Use `List<? extends Number>` when you only need to read.

### Mistake 5: Calling methods that `T` might not have

```java
<T> void show(T x) { x.length(); }   // ❌ T could be anything
```

**Fix:** Add a bound: `<T extends CharSequence>`, or use a specific type.

---

## ✅ Summary

- **Generics** put a **type label** on classes and methods: `List<String>`, `Box<Apple>`. 🍱
- They give **type safety**: wrong types are caught at **compile time**, and you don't need casts.
- Read them like sentences: `Map<String, List<Integer>>` = "a map from String to a list of Integers".
- Generic class: `class Box<T> { private T item; ... }` → `Box<String>`, `Box<Integer>`.
- Records can be generic: `record Pair<A, B>(A first, B second)`.
- Generic method: `public static <T> T first(List<T> list)` — `<T>` before the return type. Java **infers** T.
- **Bounds**: `<T extends Number>` → T must be a Number (so you can use Number's methods).
- **Wildcards**: `<? extends T>` (read), `<? super T>` (write), `<?>` (anything). Mostly for **reading** library code.
- Only object types in `< >`. Avoid raw types.
- Spring: `JpaRepository<Student, Long>` = a repository for Students with Long IDs. 🌱

---

## ❓ Quiz

1. What problem do generics solve?
2. What does the `T` in `class Box<T>` mean?
3. Where does `<T>` go in a generic method?
4. What does `<T extends Number>` mean?
5. Can you write `List<int>`?
6. Is a `List<Integer>` a `List<Number>`?
7. Read this out loud: `JpaRepository<Product, Long>`.
8. What is a raw type, and why avoid it?

<details>
<summary>Click to see the answers</summary>

1. Type safety: wrong types are caught at compile time, and no casts are needed.
2. It's a placeholder for a type that will be chosen when the class is used.
3. Before the return type: `public static <T> T method(...)`.
4. T can be any type that is a `Number` (or a child of Number).
5. No — use `List<Integer>`.
6. No (but it is a `List<? extends Number>`).
7. "A repository for Products, whose IDs are Longs."
8. A generic class used without `< >` (like `List`). It has no type safety — mistakes crash at run time.

</details>

---

[⬅ Previous chapter](33-exceptions.md) | [Table of Contents](../README.md) | [Next chapter: Lambdas ➡](35-lambdas.md)
