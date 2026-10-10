# Chapter 36 – Streams: Working with Lists Easily

[⬅ Previous chapter](35-lambdas.md) | [Table of Contents](../README.md) | [Next chapter ➡](37-optional.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **Stream** is: a **conveyor belt** for your data 🏭
- How to **filter**, **map** (transform), **sort** and **limit**
- How to **collect** the result into a List, Set or Map
- How to **count**, **sum**, **average**, find **min/max**
- `anyMatch`, `allMatch`, `findFirst`
- **Grouping** with `Collectors.groupingBy` — in one line!
- Number streams: `IntStream.range(...)`
- When to use a stream — and when a normal loop is better

> 🌱 **Spring Boot note:** In Spring Boot, you'll use streams **all the time** — for example, to turn a list of database entities into a list of DTOs: `students.stream().map(StudentDto::from).toList()`. This chapter is very practical!

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Stream** | A **flow** of items, one after another, that you can process step by step. |
| **Pipeline** | A chain of steps: source → steps → result. |
| **Intermediate operation** | A step in the middle that gives back **another stream**: `filter`, `map`, `sorted`... |
| **Terminal operation** | The **last** step that gives a **result**: `toList`, `count`, `sum`... |
| **Lazy** | Nothing happens until the terminal operation is called. |
| **Collector** | A recipe for **collecting** stream items into something (a List, a Map...). |

---

## 📖 Story: The juice factory 🍊🏭

Imagine a **juice factory** with a **conveyor belt**:

```
  🍊🍋🍊🍎🍊🍋🍊  →  [ keep only oranges ]  →  [ squeeze each ]  →  [ pour into bottles ]  →  🧃🧃🧃🧃
   SOURCE            FILTER                     MAP                  COLLECT                 RESULT
```

1. **Source:** a pile of fruit is put on the belt.
2. **Filter:** a worker **removes** everything that isn't an orange. 🍋🍎❌
3. **Map:** a machine **turns** each orange into juice. 🍊 → 🥤
4. **Collect:** the juice is put into **bottles**. 🧃

A **Stream** is this conveyor belt for your data. Each **step** does **one** small job. 🏭

---

## 🆚 Part 1: Loop vs. Stream

**Task:** From a list of names, get the names that are **longer than 3 letters**, in **CAPITAL letters**, **sorted**.

### The loop way (Chapters 12 & 30)

```java
List<String> names = List.of("Sara", "Tom", "Benjamin", "Al", "Lina", "Max");

List<String> result = new ArrayList<>();
for (String name : names) {
    if (name.length() > 3) {
        result.add(name.toUpperCase());
    }
}
Collections.sort(result);
System.out.println(result);   // [BENJAMIN, LINA, SARA]
```

### The stream way ✨

```java
List<String> result = names.stream()
        .filter(name -> name.length() > 3)
        .map(String::toUpperCase)
        .sorted()
        .toList();

System.out.println(result);   // [BENJAMIN, LINA, SARA]
```

### 🔍 Line by line

| Line | Meaning | Items on the belt |
|---|---|---|
| `names.stream()` | Put the list on the conveyor belt. (**Source**) | Sara, Tom, Benjamin, Al, Lina, Max |
| `.filter(name -> name.length() > 3)` | Keep only names **longer than 3**. | Sara, Benjamin, Lina |
| `.map(String::toUpperCase)` | **Turn** each name into capitals. | SARA, BENJAMIN, LINA |
| `.sorted()` | Sort A → Z. | BENJAMIN, LINA, SARA |
| `.toList()` | Put the result in a **List**. (**Terminal**) | → `[BENJAMIN, LINA, SARA]` |

👉 The stream code reads like a **recipe**: "Take the names, keep the long ones, make them uppercase, sort them, give me a list." 📖 You say **what** you want, not **how** to loop.

> 💡 **Formatting tip:** Put each step on its **own line**, starting with `.` — it's much easier to read.

---

## 🏗️ Part 2: The 3 parts of every stream

```
   SOURCE          INTERMEDIATE OPERATIONS (0 or more)         TERMINAL OPERATION (exactly 1)
 ┌─────────┐    ┌──────────┐   ┌──────────┐   ┌──────────┐    ┌─────────────┐
 │ .stream()│ → │ .filter()│ → │  .map()  │ → │ .sorted()│ →  │  .toList()  │ → result
 └─────────┘    └──────────┘   └──────────┘   └──────────┘    └─────────────┘
```

| Part | Examples | Returns |
|---|---|---|
| **Source** | `list.stream()`, `set.stream()`, `Arrays.stream(array)`, `Stream.of(1, 2, 3)` | a Stream |
| **Intermediate** | `filter`, `map`, `sorted`, `distinct`, `limit`, `skip`, `peek` | **another** Stream (so you can chain more) |
| **Terminal** | `toList`, `collect`, `count`, `forEach`, `sum`, `min`, `max`, `anyMatch`, `findFirst`, `reduce` | a **result** (or nothing) |

### ⚠️ Two important rules

**Rule 1: Streams are lazy.** 😴 Nothing happens until a **terminal** operation is called.

```java
names.stream().filter(n -> {
    System.out.println("checking " + n);
    return n.length() > 3;
});
// prints NOTHING! There's no terminal operation, so the belt never starts.
```

**Rule 2: A stream can be used only once.** 🔥

```java
Stream<String> s = names.stream();
s.count();
s.count();   // 💥 IllegalStateException: stream has already been operated upon or closed
```

Just call `.stream()` again for a new one.

**Bonus rule:** A stream **never changes** the original list. It creates **new** results. 🛡️

---

## 🔍 Part 3: `filter` — keep only some items

`filter` takes a **Predicate** (a yes/no question — Chapter 35) and keeps the items where the answer is **yes**.

```java
List<Integer> numbers = List.of(5, 12, 8, 21, 3, 16, 9);

List<Integer> even = numbers.stream()
        .filter(n -> n % 2 == 0)
        .toList();
System.out.println(even);   // [12, 8, 16]

List<Integer> bigAndOdd = numbers.stream()
        .filter(n -> n > 5)
        .filter(n -> n % 2 == 1)
        .toList();
System.out.println(bigAndOdd);   // [21, 9]
```

You can use **many** filters in a row (or combine conditions with `&&`).

---

## 🔄 Part 4: `map` — transform each item

`map` takes a **Function** (Chapter 35) and **turns** each item into something else.

```java
List<String> words = List.of("apple", "kiwi", "banana");

List<Integer> lengths = words.stream()
        .map(String::length)
        .toList();
System.out.println(lengths);   // [5, 4, 6]

List<String> shouted = words.stream()
        .map(w -> w.toUpperCase() + "!")
        .toList();
System.out.println(shouted);   // [APPLE!, KIWI!, BANANA!]
```

Notice: `map(String::length)` changed a stream of **Strings** into a stream of **Integers**. The type can change! 🔀

### Map objects to one of their fields

```java
record Student(String name, int grade, String className) { }

List<Student> students = List.of(
    new Student("Sara", 92, "5A"),
    new Student("Tom", 58, "5B"),
    new Student("Ali", 75, "5A"),
    new Student("Lina", 88, "5B"),
    new Student("Ben", 45, "5A")
);

List<String> names = students.stream()
        .map(Student::name)
        .toList();
System.out.println(names);   // [Sara, Tom, Ali, Lina, Ben]
```

### 🌱 The #1 Spring Boot use: entity → DTO

```java
record StudentDto(String name, boolean passed) {
    static StudentDto from(Student s) {
        return new StudentDto(s.name(), s.grade() >= 60);
    }
}

List<StudentDto> dtos = students.stream()
        .map(StudentDto::from)
        .toList();
```

You'll write lines like this **very often** in Spring Boot! 🎉

---

## 🔢 Part 5: Sorting, distinct, limit, skip

```java
List<Integer> nums = List.of(5, 3, 9, 3, 1, 9, 7);

nums.stream().sorted().toList();                              // [1, 3, 3, 5, 7, 9, 9]
nums.stream().sorted(Comparator.reverseOrder()).toList();     // [9, 9, 7, 5, 3, 3, 1]
nums.stream().distinct().toList();                            // [5, 3, 9, 1, 7]  (no duplicates)
nums.stream().limit(3).toList();                              // [5, 3, 9]  (first 3)
nums.stream().skip(4).toList();                               // [1, 9, 7]  (skip first 4)
```

| Operation | Meaning |
|---|---|
| `sorted()` | natural order |
| `sorted(comparator)` | your order (Chapter 35) |
| `distinct()` | remove duplicates (uses `equals`) |
| `limit(n)` | keep only the **first** n |
| `skip(n)` | throw away the first n |

### Example: Top 3 students 🏆

```java
List<String> top3 = students.stream()
        .sorted(Comparator.comparing(Student::grade).reversed())
        .limit(3)
        .map(s -> s.name() + " (" + s.grade() + ")")
        .toList();

System.out.println(top3);   // [Sara (92), Lina (88), Ali (75)]
```

> 💡 `skip` + `limit` together = **pagination** (page 2 = skip 10, limit 10). Spring Boot does this with databases in Chapter 78!

---

## 🏁 Part 6: Terminal operations — getting results

### Collect into a List

```java
List<String> list = stream.toList();   // Java 16+, unchangeable list ✅
```

(Older code uses `.collect(Collectors.toList())` — same idea, you'll see it a lot.)

### Count

```java
long passed = students.stream()
        .filter(s -> s.grade() >= 60)
        .count();
System.out.println(passed + " students passed");   // 3 students passed
```

### Check: `anyMatch`, `allMatch`, `noneMatch`

```java
boolean someoneFailed = students.stream().anyMatch(s -> s.grade() < 60);    // true
boolean allPassed     = students.stream().allMatch(s -> s.grade() >= 60);   // false
boolean nobodyPerfect = students.stream().noneMatch(s -> s.grade() == 100); // true
```

| Method | Question |
|---|---|
| `anyMatch` | Is it true for **at least one**? |
| `allMatch` | Is it true for **all**? |
| `noneMatch` | Is it true for **none**? |

They **stop early** as soon as they know the answer. ⚡

### Find one: `findFirst`

```java
Optional<Student> firstFrom5B = students.stream()
        .filter(s -> s.className().equals("5B"))
        .findFirst();

System.out.println(firstFrom5B.get().name());   // Tom
```

`findFirst()` returns an **`Optional`** — a box that **might be empty** (if nothing matches). Next chapter is all about `Optional`! 📦

### Min and max

```java
Optional<Student> best = students.stream()
        .max(Comparator.comparing(Student::grade));
System.out.println(best.get().name());   // Sara
```

### `forEach` — do something with each

```java
students.stream()
        .filter(s -> s.grade() < 60)
        .forEach(s -> System.out.println("📢 " + s.name() + " needs help"));
```

**Output:**

```
📢 Tom needs help
📢 Ben needs help
```

---

## 🔢 Part 7: Number streams — sum, average, statistics

For numbers, there are special streams: **`IntStream`**, **`DoubleStream`**, **`LongStream`**. They have math methods!

```java
int total = students.stream()
        .mapToInt(Student::grade)
        .sum();
System.out.println("Total: " + total);   // Total: 358

double average = students.stream()
        .mapToInt(Student::grade)
        .average()
        .orElse(0);
System.out.println("Average: " + average);   // Average: 71.6
```

| Code | Meaning |
|---|---|
| `mapToInt(Student::grade)` | Turn the stream of Students into an **IntStream** of grades. |
| `.sum()` | Add them all up. |
| `.average()` | The average — returns an `OptionalDouble` (empty if there are no items). |
| `.orElse(0)` | "If empty, use 0." (Chapter 37.) |

### All statistics at once

```java
IntSummaryStatistics stats = students.stream()
        .mapToInt(Student::grade)
        .summaryStatistics();

System.out.println(stats);
// IntSummaryStatistics{count=5, sum=358, min=45, average=71.600000, max=92}
System.out.println("Highest: " + stats.getMax());   // Highest: 92
```

### `IntStream.range` — a stream of numbers (instead of a `for` loop!)

```java
IntStream.range(1, 6).forEach(i -> System.out.print(i + " "));        // 1 2 3 4 5
System.out.println();
IntStream.rangeClosed(1, 5).map(i -> i * i).forEach(i -> System.out.print(i + " "));   // 1 4 9 16 25
System.out.println();

int sum1to100 = IntStream.rangeClosed(1, 100).sum();
System.out.println(sum1to100);   // 5050  (remember Chapter 12? 😉)
```

| Method | Numbers |
|---|---|
| `IntStream.range(1, 6)` | 1, 2, 3, 4, 5 (6 **not** included — like `i < 6`) |
| `IntStream.rangeClosed(1, 5)` | 1, 2, 3, 4, 5 (5 **included** — like `i <= 5`) |

### From an array

```java
int[] scores = { 80, 95, 70 };
int max = Arrays.stream(scores).max().getAsInt();   // 95
```

---

## 🧺 Part 8: Collectors — joining, grouping, counting

`collect(...)` with a **Collector** can build almost anything. Import: `java.util.stream.Collectors`.

### Join Strings

```java
String allNames = students.stream()
        .map(Student::name)
        .collect(Collectors.joining(", "));
System.out.println(allNames);   // Sara, Tom, Ali, Lina, Ben

String fancy = students.stream()
        .map(Student::name)
        .collect(Collectors.joining(" | ", "[ ", " ]"));
System.out.println(fancy);   // [ Sara | Tom | Ali | Lina | Ben ]
```

### Into a Set

```java
Set<String> classes = students.stream()
        .map(Student::className)
        .collect(Collectors.toSet());   // [5A, 5B] — no duplicates
```

### Into a Map

```java
Map<String, Integer> gradeByName = students.stream()
        .collect(Collectors.toMap(Student::name, Student::grade));
System.out.println(gradeByName.get("Lina"));   // 88
```

`toMap(keyFunction, valueFunction)` — "the name is the key, the grade is the value".

> ⚠️ If two items have the **same key**, `toMap` throws an exception (`Duplicate key`). Use `groupingBy` instead, or give a merge function.

### ⭐ Group by — the superstar

Remember grouping in Chapter 31 (with `computeIfAbsent`)? Now it's **one line**:

```java
Map<String, List<Student>> byClass = students.stream()
        .collect(Collectors.groupingBy(Student::className));

byClass.forEach((className, list) ->
        System.out.println(className + ": " + list.stream().map(Student::name).toList()));
```

**Output:**

```
5A: [Sara, Ali, Ben]
5B: [Tom, Lina]
```

### Group and count / average

```java
Map<String, Long> countPerClass = students.stream()
        .collect(Collectors.groupingBy(Student::className, Collectors.counting()));
System.out.println(countPerClass);   // {5A=3, 5B=2}

Map<String, Double> averagePerClass = students.stream()
        .collect(Collectors.groupingBy(Student::className,
                 Collectors.averagingInt(Student::grade)));
System.out.println(averagePerClass);   // {5A=70.66666666666667, 5B=73.0}
```

### Split in two: `partitioningBy`

```java
Map<Boolean, List<String>> passFail = students.stream()
        .collect(Collectors.partitioningBy(
                s -> s.grade() >= 60,
                Collectors.mapping(Student::name, Collectors.toList())));

System.out.println("Passed: " + passFail.get(true));    // Passed: [Sara, Ali, Lina]
System.out.println("Failed: " + passFail.get(false));   // Failed: [Tom, Ben]
```

### Count words — the counting pattern in one line

```java
String text = "the cat and the dog and the bird";
Map<String, Long> wordCount = Arrays.stream(text.split(" "))
        .collect(Collectors.groupingBy(w -> w, TreeMap::new, Collectors.counting()));
System.out.println(wordCount);   // {and=2, bird=1, cat=1, dog=1, the=3}
```

(Compare with Chapter 31 — same result! `TreeMap::new` tells it to use a sorted map.)

### 📋 Collectors cheat sheet

| Collector | Result |
|---|---|
| `Collectors.toList()` / `.toList()` | `List` |
| `Collectors.toSet()` | `Set` |
| `Collectors.toMap(k, v)` | `Map` (unique keys!) |
| `Collectors.joining(", ")` | one `String` |
| `Collectors.groupingBy(key)` | `Map<Key, List<T>>` |
| `Collectors.groupingBy(key, Collectors.counting())` | `Map<Key, Long>` |
| `Collectors.partitioningBy(predicate)` | `Map<Boolean, List<T>>` |
| `Collectors.averagingInt(...)`, `summingInt(...)` | numbers |

---

## 🧮 Part 9: `reduce` — combine everything into one

`reduce` combines all items into **one** value, step by step:

```java
int product = Stream.of(1, 2, 3, 4, 5)
        .reduce(1, (a, b) -> a * b);
System.out.println(product);   // 120  (1 × 1 × 2 × 3 × 4 × 5)
```

| Part | Meaning |
|---|---|
| `1` | The **starting value** (for multiplying, start with 1 — Chapter 12!). |
| `(a, b) -> a * b` | How to combine "the result so far" (`a`) with the next item (`b`). |

```
 start: 1
 1 × 1 = 1
 1 × 2 = 2
 2 × 3 = 6
 6 × 4 = 24
 24 × 5 = 120 ✅
```

> 💡 For sums, `mapToInt(...).sum()` is simpler. Use `reduce` for special combinations.

---

## 🤔 Part 10: Stream or loop?

Streams are great — but not **always** better.

| Use a **stream** when... | Use a **loop** when... |
|---|---|
| you **filter**, **transform**, **group**, **count** a collection | you need to **change** outside variables |
| the steps read like a recipe | you need `break` in a complicated way |
| you want a **new** collection as the result | the logic has many `if/else` branches |
| | you need the **index** a lot |
| | a beginner on your team must read it 😊 |

```java
// 👍 stream: clear
long adults = people.stream().filter(p -> p.age() >= 18).count();

// 👎 stream: hard to read
var x = list.stream().flatMap(a -> a.items().stream().filter(i -> i.p() > 3)
        .map(i -> Map.entry(a.id(), i))).collect(Collectors.groupingBy(...));
```

👉 **Rule:** If a stream is hard to read, use a loop — or break it into small, well-named methods. **Readable code wins.** 📖

---

## 💻 Mini project: Movie analyzer 🎬

```java
import java.util.*;
import java.util.stream.Collectors;

public class MovieAnalyzer {

    enum Genre { ACTION, COMEDY, DRAMA, ANIMATION }

    record Movie(String title, Genre genre, int year, double rating, int minutes) { }

    public static void main(String[] args) {
        List<Movie> movies = List.of(
            new Movie("Space Race", Genre.ACTION, 2019, 7.8, 132),
            new Movie("Funny Farm", Genre.COMEDY, 2021, 6.5, 95),
            new Movie("Ocean Heart", Genre.DRAMA, 2018, 8.4, 141),
            new Movie("Robo Pals", Genre.ANIMATION, 2022, 8.1, 88),
            new Movie("Speed Zone", Genre.ACTION, 2023, 6.9, 118),
            new Movie("Laugh Out", Genre.COMEDY, 2020, 7.2, 101),
            new Movie("Little Dragon", Genre.ANIMATION, 2019, 7.5, 92)
        );

        // 1. Top 3 by rating
        System.out.println("🏆 Top 3:");
        movies.stream()
                .sorted(Comparator.comparing(Movie::rating).reversed())
                .limit(3)
                .forEach(m -> System.out.println("   " + m.rating() + " ⭐ " + m.title()));

        // 2. Average rating
        double avg = movies.stream().mapToDouble(Movie::rating).average().orElse(0);
        System.out.printf("📊 Average rating: %.2f%n", avg);

        // 3. Short movies (under 100 minutes), sorted by title
        List<String> shortOnes = movies.stream()
                .filter(m -> m.minutes() < 100)
                .map(Movie::title)
                .sorted()
                .toList();
        System.out.println("⏱️ Short movies: " + shortOnes);

        // 4. How many movies per genre
        Map<Genre, Long> perGenre = movies.stream()
                .collect(Collectors.groupingBy(Movie::genre, TreeMap::new, Collectors.counting()));
        System.out.println("🎭 Per genre: " + perGenre);

        // 5. Best movie in each genre
        System.out.println("🥇 Best per genre:");
        movies.stream()
                .collect(Collectors.groupingBy(Movie::genre, TreeMap::new,
                         Collectors.maxBy(Comparator.comparing(Movie::rating))))
                .forEach((genre, best) ->
                        System.out.println("   " + genre + ": " + best.get().title()));

        // 6. Any movie from before 2019?
        boolean anyOld = movies.stream().anyMatch(m -> m.year() < 2019);
        System.out.println("📅 Any movie before 2019? " + anyOld);

        // 7. Total watch time
        int totalMinutes = movies.stream().mapToInt(Movie::minutes).sum();
        System.out.println("🍿 Watch them all: " + totalMinutes / 60 + "h " + totalMinutes % 60 + "min");
    }
}
```

**Output:**

```
🏆 Top 3:
   8.4 ⭐ Ocean Heart
   8.1 ⭐ Robo Pals
   7.8 ⭐ Space Race
📊 Average rating: 7.49
⏱️ Short movies: [Funny Farm, Little Dragon, Robo Pals]
🎭 Per genre: {ACTION=2, COMEDY=2, DRAMA=1, ANIMATION=2}
🥇 Best per genre:
   ACTION: Space Race
   COMEDY: Laugh Out
   DRAMA: Ocean Heart
   ANIMATION: Robo Pals
📅 Any movie before 2019? true
🍿 Watch them all: 12h 47min
```

### 🔍 What we used

| # | Operations |
|---|---|
| 1 | `sorted` + `reversed` + `limit` + `forEach` |
| 2 | `mapToDouble` + `average` + `orElse` |
| 3 | `filter` + `map` + `sorted` + `toList` |
| 4 | `groupingBy` + `counting` (with a `TreeMap` → enum order) |
| 5 | `groupingBy` + `maxBy` |
| 6 | `anyMatch` |
| 7 | `mapToInt` + `sum` |

Imagine writing all of this with loops! 😅

---

## ✋ Try it yourself

Use this list for the tasks:

```java
List<String> fruits = List.of("apple", "banana", "cherry", "date", "fig", "grape", "kiwi", "banana");
```

**Task 1:** Get all fruits with **more than 4** letters, in capitals, without duplicates.

<details>
<summary>Click to see the answer</summary>

```java
List<String> result = fruits.stream()
        .filter(f -> f.length() > 4)
        .map(String::toUpperCase)
        .distinct()
        .toList();
// [APPLE, BANANA, CHERRY, GRAPE]
```

</details>

**Task 2:** Count how many fruits contain the letter `"a"`.

**Task 3:** Join all fruits into one String, sorted, separated by `" - "`.

<details>
<summary>Click to see the answer</summary>

```java
String joined = fruits.stream()
        .distinct()
        .sorted()
        .collect(Collectors.joining(" - "));
// apple - banana - cherry - date - fig - grape - kiwi
```

</details>

**Task 4:** Group the fruits by their **length**: `{3=[fig], 4=[date, kiwi], 5=[apple, grape], 6=[banana, cherry, banana]}`.

<details>
<summary>Click to see the answer</summary>

```java
Map<Integer, List<String>> byLength = fruits.stream()
        .collect(Collectors.groupingBy(String::length));
```

</details>

**Task 5:** Use `IntStream.rangeClosed` to get a list of all numbers from 1 to 50 that can be divided by 7.

**Task 6:** Rewrite the **Grade Book** mini project from Chapter 30 using streams. How many lines did you save? 😉

---

## ⚠️ Common mistakes

### Mistake 1: No terminal operation

```java
names.stream().filter(n -> n.length() > 3).map(String::toUpperCase);   // does NOTHING
```

**Fix:** End with `.toList()`, `.forEach(...)`, `.count()`...

### Mistake 2: Reusing a stream

```
💥 IllegalStateException: stream has already been operated upon or closed
```

**Fix:** Call `.stream()` again.

### Mistake 3: Expecting the original list to change

```java
names.stream().map(String::toUpperCase).toList();
System.out.println(names);   // still lowercase! The result was thrown away.
```

**Fix:** Save the result: `List<String> upper = names.stream()...toList();`

### Mistake 4: Changing the result of `toList()`

```java
List<String> l = stream.toList();
l.add("x");   // 💥 UnsupportedOperationException — toList() is unchangeable
```

**Fix:** `new ArrayList<>(stream.toList())` or `.collect(Collectors.toList())`.

### Mistake 5: `toMap` with duplicate keys

```
💥 IllegalStateException: Duplicate key Sara (attempted merging values 92 and 88)
```

**Fix:** Use `groupingBy`, or `toMap(k, v, (a, b) -> a)` to keep the first.

### Mistake 6: Calling `.get()` on an empty Optional

```java
students.stream().filter(s -> s.grade() > 100).findFirst().get();   // 💥 NoSuchElementException
```

**Fix:** Next chapter — `Optional`! 📦

---

## ✅ Summary

- A **stream** is a conveyor belt 🏭: **source** → **intermediate steps** → **terminal** result.
- Source: `list.stream()`, `Arrays.stream(arr)`, `Stream.of(...)`, `IntStream.range(a, b)`.
- Intermediate: `filter` (keep), `map` (transform), `sorted`, `distinct`, `limit`, `skip`.
- Terminal: `toList`, `count`, `forEach`, `anyMatch`/`allMatch`/`noneMatch`, `findFirst`, `min`/`max`, `reduce`, `collect`.
- Numbers: `mapToInt(...)` → `sum()`, `average()`, `max()`, `summaryStatistics()`.
- Collectors: `joining`, `toSet`, `toMap`, **`groupingBy`**, `counting`, `partitioningBy`.
- Streams are **lazy**, **one-use**, and **don't change** the original.
- Use streams when they make code **clearer**; use loops when they don't.
- Spring Boot: `entities.stream().map(Dto::from).toList()` — you'll write this a lot! 🌱

---

## ❓ Quiz

1. What are the 3 parts of a stream pipeline?
2. What's the difference between `filter` and `map`?
3. What happens if a stream has no terminal operation?
4. Does `list.stream().sorted().toList()` change `list`?
5. How do you get the sum of all grades from a list of students?
6. What does `IntStream.range(0, 3)` produce?
7. Which collector groups items into a `Map<Key, List<Item>>`?
8. What does `findFirst()` return, and why?

<details>
<summary>Click to see the answers</summary>

1. Source, intermediate operations, terminal operation.
2. `filter` keeps or removes items (yes/no). `map` transforms each item into something else.
3. Nothing happens — streams are lazy.
4. No — it creates a new sorted list.
5. `students.stream().mapToInt(Student::grade).sum()`
6. 0, 1, 2
7. `Collectors.groupingBy(...)`
8. An `Optional`, because there might be no matching item.

</details>

---

[⬅ Previous chapter](35-lambdas.md) | [Table of Contents](../README.md) | [Next chapter: Optional ➡](37-optional.md)
