# Chapter 31 – Maps (`HashMap`)

[⬅ Previous chapter](30-lists.md) | [Table of Contents](../README.md) | [Next chapter ➡](32-sets.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **Map** is: **keys** and **values**
- How to **put**, **get**, **change** and **remove** entries
- How to check if a key exists, and use **`getOrDefault`**
- How to **loop** over a map (keys, values, or both)
- The **counting** pattern: "how many times does each word appear?"
- **`HashMap`**, **`LinkedHashMap`** and **`TreeMap`** — and the order of items
- Maps with **lists** inside (grouping)

> 🌱 **Spring Boot note:** Maps are everywhere: settings (`key=value`), JSON objects (`{"name": "Sara"}`), HTTP headers, caches... A JSON object is basically a Map!

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Map** | A collection of **pairs**: each **key** points to a **value**. |
| **Key** | The thing you **look up** with. Like a word in a dictionary. Keys are **unique**. |
| **Value** | The thing you **find**. Like the meaning of the word. |
| **Entry** | One key–value pair. |
| **`HashMap`** | The most common Map. Very fast, but **no order**. |
| **`LinkedHashMap`** | A Map that remembers the order you **added** things. |
| **`TreeMap`** | A Map that keeps the keys **sorted**. |

---

## 📖 Story: The dictionary 📖 and the phone book ☎️

In a **dictionary**, you don't look for a word by its **page number** (index). You look it up by the **word itself**:

```
  "apple"   →  a round fruit 🍎
  "banana"  →  a long yellow fruit 🍌
  "cherry"  →  a small red fruit 🍒
    KEY            VALUE
```

In a **phone book**, you look up a **name** and find a **number**:

```
  "Sara"  →  "555-1234"
  "Tom"   →  "555-9876"
```

That's a **Map**: you give it a **key**, it gives you the **value**. ⚡ Very fast — no searching through a list!

### List vs. Map

| | List | Map |
|---|---|---|
| Find an item by... | **position** (index 0, 1, 2) | **key** ("Sara", "apple") |
| Example | `names.get(2)` | `phoneBook.get("Sara")` |
| Picture | 🚂 a train with numbered wagons | 🗄️ a cabinet with **labeled** drawers |

---

## 🗄️ Part 1: Your first `HashMap`

```java
import java.util.HashMap;
import java.util.Map;

public class PhoneBook {
    public static void main(String[] args) {
        Map<String, String> phones = new HashMap<>();

        phones.put("Sara", "555-1234");
        phones.put("Tom", "555-9876");
        phones.put("Lina", "555-4444");

        System.out.println(phones.get("Tom"));
        System.out.println(phones.get("Ben"));
        System.out.println("Entries: " + phones.size());
    }
}
```

**Output:**

```
555-9876
null
Entries: 3
```

### 🔍 Line by line

`Map<String, String> phones = new HashMap<>();`

| Part | Meaning |
|---|---|
| `Map` | The interface (like `List` in Chapter 30). |
| `<String, String>` | **Two** types: `<KeyType, ValueType>`. Here: the key is a String (name), and the value is a String (phone number). |
| `new HashMap<>()` | Create an empty `HashMap`. |

| Other lines | Meaning |
|---|---|
| `phones.put("Sara", "555-1234");` | **Put** a pair in: key `"Sara"` → value `"555-1234"`. |
| `phones.get("Tom")` | **Get** the value for key `"Tom"` → `"555-9876"`. |
| `phones.get("Ben")` | `"Ben"` is not in the map → returns **`null`**. ⚠️ |
| `phones.size()` | The number of **pairs**: 3. |

### Different types

Keys and values can be **any** object type:

```java
Map<String, Integer> ages = new HashMap<>();          // name → age
Map<Integer, String> studentsById = new HashMap<>();  // id → name
Map<String, Double> prices = new HashMap<>();         // product → price
Map<Character, Integer> letterCount = new HashMap<>(); // letter → how many
Map<String, List<String>> groups = new HashMap<>();   // group name → list of members
```

(Remember: use wrapper classes like `Integer`, not `int` — Chapter 30.)

---

## 🔑 Part 2: Keys are unique

What if you `put` the **same key** two times?

```java
Map<String, Integer> ages = new HashMap<>();
ages.put("Sara", 12);
ages.put("Sara", 13);   // Sara had a birthday 🎂

System.out.println(ages.get("Sara"));   // 13
System.out.println(ages.size());        // 1
```

The **new** value **replaces** the old one. There's still only **one** `"Sara"`.

📖 In a dictionary, each word appears **once**. If you write a new meaning, the old one is crossed out. ✏️

But **values** can repeat:

```java
ages.put("Tom", 13);    // ✅ Sara and Tom can both be 13
```

| | Unique? |
|---|---|
| Keys | ✅ **yes** — each key only once |
| Values | ❌ no — the same value can appear many times |

---

## 🧰 Part 3: The most useful Map methods

```java
Map<String, Integer> stock = new HashMap<>();
stock.put("apple", 10);
stock.put("banana", 5);
stock.put("cherry", 0);
```

### Checking

```java
stock.containsKey("apple");     // true  — is there a key "apple"?
stock.containsKey("mango");     // false
stock.containsValue(5);         // true  — is any value equal to 5?
stock.isEmpty();                // false
```

### Getting safely: `getOrDefault`

```java
int mangos = stock.get("mango");   // 💥 NullPointerException! (null can't become an int)
```

`get` returns `null` for a missing key. Unboxing `null` into an `int` crashes! 😱 Use `getOrDefault`:

```java
int mangos = stock.getOrDefault("mango", 0);   // 0 ✅ — "give me 0 if mango is not there"
int apples = stock.getOrDefault("apple", 0);   // 10
```

### Removing

```java
stock.remove("cherry");         // removes the pair with key "cherry"
```

### Only add if missing: `putIfAbsent`

```java
stock.putIfAbsent("apple", 99);   // apple already exists → nothing changes (still 10)
stock.putIfAbsent("kiwi", 7);     // kiwi is new → added
```

### Updating a value: `merge`

```java
stock.merge("apple", 3, Integer::sum);   // apple: 10 + 3 = 13
stock.merge("grape", 3, Integer::sum);   // grape doesn't exist → put 3
```

`merge(key, value, howToCombine)`: "If the key exists, **combine** the old and new value (here: add them). If not, just **put** the value." Perfect for counting! (Part 5)

### 📋 Cheat sheet

| Method | What it does |
|---|---|
| `put(key, value)` | add or **replace** |
| `get(key)` | get the value, or `null` |
| `getOrDefault(key, def)` | get the value, or `def` if missing |
| `containsKey(key)` | is this key there? |
| `containsValue(value)` | is this value there? |
| `remove(key)` | remove the pair |
| `size()` | number of pairs |
| `isEmpty()` | is it empty? |
| `putIfAbsent(key, value)` | add only if the key is missing |
| `merge(key, value, fn)` | add, or combine with the old value |
| `keySet()` | all keys |
| `values()` | all values |
| `entrySet()` | all pairs |
| `clear()` | remove everything |

---

## 🔁 Part 4: Looping over a map

```java
Map<String, Integer> scores = new HashMap<>();
scores.put("Sara", 92);
scores.put("Tom", 75);
scores.put("Lina", 88);
```

### Loop over the keys

```java
for (String name : scores.keySet()) {
    System.out.println(name);
}
```

### Loop over the values

```java
int total = 0;
for (int score : scores.values()) {
    total += score;
}
System.out.println("Total: " + total);   // Total: 255
```

### Loop over both (entries) ✅ — the most useful

```java
for (Map.Entry<String, Integer> entry : scores.entrySet()) {
    System.out.println(entry.getKey() + " → " + entry.getValue());
}
```

**Output:**

```
Tom → 75
Lina → 88
Sara → 92
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `scores.entrySet()` | All the **pairs** in the map. |
| `Map.Entry<String, Integer>` | The type of **one pair**. |
| `entry.getKey()` | The key of this pair (`"Tom"`). |
| `entry.getValue()` | The value of this pair (`75`). |

> 💡 **Shorter with `var`** (Chapter 6): `for (var entry : scores.entrySet()) { ... }`

### Or with `forEach` and a lambda (Chapter 35)

```java
scores.forEach((name, score) -> System.out.println(name + " → " + score));
```

### 😮 Wait — why is the order strange?

We added Sara, Tom, Lina. But it printed **Tom, Lina, Sara**!

A `HashMap` does **not** keep any order. It stores items in a special way (by **hash code** — Chapter 20!) to be **super fast**. The order can look random, and it can even change when you add more items. 🎲

Next part shows how to get an order when you need one.

---

## 📚 Part 5: The order — `HashMap`, `LinkedHashMap`, `TreeMap`

All three implement the `Map` interface. Only the **order** is different:

```java
Map<String, Integer> hash   = new HashMap<>();
Map<String, Integer> linked = new LinkedHashMap<>();
Map<String, Integer> tree   = new TreeMap<>();

for (Map<String, Integer> m : List.of(hash, linked, tree)) {
    m.put("banana", 2);
    m.put("cherry", 3);
    m.put("apple", 1);
}

System.out.println("HashMap:       " + hash);
System.out.println("LinkedHashMap: " + linked);
System.out.println("TreeMap:       " + tree);
```

**Output:**

```
HashMap:       {banana=2, cherry=3, apple=1}
LinkedHashMap: {banana=2, cherry=3, apple=1}
TreeMap:       {apple=1, banana=2, cherry=3}
```

(The `HashMap` order happens to look like the insertion order here — but that's **luck**! Don't depend on it.)

| Class | Order | Speed | Use it when... |
|---|---|---|---|
| `HashMap` | ❓ no order | ⚡ fastest | order doesn't matter (most of the time) |
| `LinkedHashMap` | 📝 the order you **added** | ⚡ fast | you want to keep the order of insertion |
| `TreeMap` | 🔤 **sorted** by key | 🐢 a bit slower | you want keys sorted (A→Z, 1→9) |

👉 Because we write `Map<...> m = new XxxMap<>()`, switching is **one word**. Loose coupling again! 🔌

> 💡 Maps print nicely: `{key=value, key=value}` — curly braces `{ }`, while lists use `[ ]`.

---

## 🔢 Part 6: The counting pattern ⭐

This is one of the **most common** uses of a Map. **Learn it well!**

**Question:** How many times does each word appear?

```java
import java.util.Map;
import java.util.TreeMap;

public class WordCount {
    public static void main(String[] args) {
        String text = "the cat and the dog and the bird";
        String[] words = text.split(" ");

        Map<String, Integer> counts = new TreeMap<>();

        for (String word : words) {
            if (counts.containsKey(word)) {
                counts.put(word, counts.get(word) + 1);   // seen before → add 1
            } else {
                counts.put(word, 1);                      // first time → 1
            }
        }

        System.out.println(counts);
    }
}
```

**Output:**

```
{and=2, bird=1, cat=1, dog=1, the=3}
```

### 🎬 Step by step

| Word | In map? | Action | Map after |
|---|---|---|---|
| the | no | put 1 | {the=1} |
| cat | no | put 1 | {cat=1, the=1} |
| and | no | put 1 | {and=1, cat=1, the=1} |
| the | **yes** (1) | put 1+1 | {..., the=**2**} |
| dog | no | put 1 | ... |
| and | **yes** (1) | put 1+1 | {and=**2**, ...} |
| the | **yes** (2) | put 2+1 | {..., the=**3**} |
| bird | no | put 1 | ... |

### ✨ Shorter versions

```java
// With getOrDefault
counts.put(word, counts.getOrDefault(word, 0) + 1);

// With merge (shortest!)
counts.merge(word, 1, Integer::sum);
```

All three do the same thing. `merge(word, 1, Integer::sum)` means: "put 1 for this word; if it's already there, **add** 1 to the old number."

### Count letters

```java
Map<Character, Integer> letters = new TreeMap<>();
for (char c : "hello".toCharArray()) {
    letters.merge(c, 1, Integer::sum);
}
System.out.println(letters);   // {e=1, h=1, l=2, o=1}
```

`"hello".toCharArray()` turns a String into a `char[]` array, so we can use for-each.

---

## 🗂️ Part 7: Maps with lists inside (grouping)

A value can be a **list**! Example: group students by their class.

```java
import java.util.*;

public class Groups {
    record Student(String name, String className) { }

    public static void main(String[] args) {
        List<Student> students = List.of(
            new Student("Sara", "5A"),
            new Student("Tom", "5B"),
            new Student("Lina", "5A"),
            new Student("Ben", "5C"),
            new Student("Ali", "5B")
        );

        Map<String, List<String>> byClass = new TreeMap<>();

        for (Student s : students) {
            byClass.computeIfAbsent(s.className(), k -> new ArrayList<>())
                   .add(s.name());
        }

        for (var entry : byClass.entrySet()) {
            System.out.println("Class " + entry.getKey() + ": " + entry.getValue());
        }
    }
}
```

**Output:**

```
Class 5A: [Sara, Lina]
Class 5B: [Tom, Ali]
Class 5C: [Ben]
```

### 🔍 The magic line

```java
byClass.computeIfAbsent(s.className(), k -> new ArrayList<>()).add(s.name());
```

| Step | Meaning |
|---|---|
| `computeIfAbsent(s.className(), ...)` | "Look for the list of this class. If there is **no list yet**..." |
| `k -> new ArrayList<>()` | "...**make** a new empty list and put it in the map." |
| (returns the list) | Either the old list or the new one. |
| `.add(s.name())` | Add the student's name to that list. |

Without `computeIfAbsent`, you'd write:

```java
List<String> list = byClass.get(s.className());
if (list == null) {
    list = new ArrayList<>();
    byClass.put(s.className(), list);
}
list.add(s.name());
```

Same result — the one-liner is just shorter. 😊

> 🚀 In Chapter 36 (**Streams**), grouping becomes **one line**: `Collectors.groupingBy(...)`.

---

## 🔑 Part 8: Good keys

### Keys need `equals()` and `hashCode()`

A HashMap uses `hashCode()` to find the right "drawer" quickly, and `equals()` to check the key. Strings, Integers, enums and **records** have both. ✅

If you use your **own class** as a key, it **must** have `equals()` and `hashCode()` (Chapter 20) — or be a **record**:

```java
record Point(int x, int y) { }

Map<Point, String> board = new HashMap<>();
board.put(new Point(0, 0), "♜ rook");
board.put(new Point(4, 0), "♚ king");

System.out.println(board.get(new Point(4, 0)));   // ♚ king ✅
```

A **new** `Point(4, 0)` finds the value, because records compare by **content**. 🎉

### Don't change a key after putting it in

If the key object changes, its hash code changes, and the map **can't find it anymore**! 😱 That's another reason to use **immutable** keys (Strings, records, enums).

### Enums as keys: `EnumMap`

```java
enum Day { MON, TUE, WED }

Map<Day, String> plans = new EnumMap<>(Day.class);
plans.put(Day.WED, "Swimming 🏊");
plans.put(Day.MON, "Football ⚽");
System.out.println(plans);   // {MON=Football ⚽, WED=Swimming 🏊}  ← enum order!
```

`EnumMap` is a very fast map for enum keys, sorted in the enum's order.

---

## 🏗️ Part 9: Creating maps quickly

```java
// Immutable map (can't change)
Map<String, Integer> romanNumbers = Map.of(
    "I", 1,
    "V", 5,
    "X", 10
);

// Changeable copy
Map<String, Integer> copy = new HashMap<>(romanNumbers);
copy.put("L", 50);   // ✅
```

> ⚠️ `Map.of(...)` can take up to **10** pairs, and it **can't** be changed: `romanNumbers.put(...)` → 💥 `UnsupportedOperationException`.

---

## 💻 Mini project: A tiny shop inventory 🏪

```java
import java.util.Map;
import java.util.TreeMap;

public class Inventory {
    private final Map<String, Integer> stock = new TreeMap<>();
    private final Map<String, Double> prices = new TreeMap<>();

    public void addProduct(String name, double price, int amount) {
        prices.put(name, price);
        stock.merge(name, amount, Integer::sum);
    }

    public boolean sell(String name, int amount) {
        int available = stock.getOrDefault(name, 0);
        if (amount > available) {
            System.out.println("❌ Not enough " + name + " (have " + available + ")");
            return false;
        }
        stock.put(name, available - amount);
        System.out.printf("✅ Sold %d %s for %.2f%n", amount, name, amount * prices.get(name));
        return true;
    }

    public double totalValue() {
        double total = 0;
        for (var entry : stock.entrySet()) {
            total += entry.getValue() * prices.get(entry.getKey());
        }
        return total;
    }

    public void report() {
        System.out.println("=== Stock ===");
        for (var entry : stock.entrySet()) {
            String warning = entry.getValue() < 3 ? "  ⚠️ low!" : "";
            System.out.printf("%-8s %3d x %5.2f%s%n",
                    entry.getKey(), entry.getValue(), prices.get(entry.getKey()), warning);
        }
        System.out.printf("Total value: %.2f%n", totalValue());
    }

    public static void main(String[] args) {
        Inventory shop = new Inventory();
        shop.addProduct("apple", 0.50, 40);
        shop.addProduct("milk", 1.20, 10);
        shop.addProduct("bread", 2.50, 5);
        shop.addProduct("apple", 0.50, 10);   // more apples arrive

        shop.sell("milk", 8);
        shop.sell("bread", 6);
        shop.sell("banana", 1);
        shop.sell("apple", 20);

        shop.report();
    }
}
```

**Output:**

```
✅ Sold 8 milk for 9.60
❌ Not enough bread (have 5)
❌ Not enough banana (have 0)
✅ Sold 20 apple for 10.00
=== Stock ===
apple     30 x  0.50
bread      5 x  2.50
milk       2 x  1.20  ⚠️ low!
Total value: 29.90
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `stock.merge(name, amount, Integer::sum)` | New product → put. Existing → add to the old amount. |
| `stock.getOrDefault(name, 0)` | Unknown product (banana) → 0, no crash. |
| `TreeMap` | The report is sorted A → Z. |
| Two maps with the same keys | Works, but a **record** `Product(name, price, amount)` in **one** map would be cleaner. Try it in Task 5! |

---

## ✋ Try it yourself

**Task 1:** Make a `Map<String, String>` of 5 countries → capitals. Ask the user for a country with `Scanner` and print the capital, or "I don't know" if it's missing.

**Task 2:** Count how many times each **letter** appears in your name. Ignore big/small letters and spaces.

<details>
<summary>Click to see the answer</summary>

```java
String name = "Sara Ahmed";
Map<Character, Integer> counts = new TreeMap<>();

for (char c : name.toLowerCase().toCharArray()) {
    if (c != ' ') {
        counts.merge(c, 1, Integer::sum);
    }
}
System.out.println(counts);   // {a=3, d=1, e=1, h=1, m=1, r=1, s=1}
```

</details>

**Task 3:** You have `Map<String, Integer> scores`. Find the name with the **highest** score.

<details>
<summary>Click to see the answer</summary>

```java
String best = null;
int bestScore = Integer.MIN_VALUE;

for (var entry : scores.entrySet()) {
    if (entry.getValue() > bestScore) {
        bestScore = entry.getValue();
        best = entry.getKey();
    }
}
System.out.println(best + " has the highest score: " + bestScore);
```

</details>

**Task 4:** Group words by their **first letter**: `["apple", "avocado", "banana", "blueberry", "cherry"]` → `{a=[apple, avocado], b=[banana, blueberry], c=[cherry]}`.

**Task 5:** Rewrite the `Inventory` with **one** map: `Map<String, Product>` where `record Product(String name, double price, int amount)`. (Remember: records are immutable — to change the amount, put a **new** Product.)

---

## ⚠️ Common mistakes

### Mistake 1: Unboxing `null` from `get`

```java
int age = ages.get("Unknown");   // 💥 NullPointerException
```

**Fix:** `ages.getOrDefault("Unknown", 0)` or check `containsKey` first.

### Mistake 2: Expecting `HashMap` to keep the order

**Fix:** Use `LinkedHashMap` (insertion order) or `TreeMap` (sorted).

### Mistake 3: Thinking `put` adds a second value for the same key

`put` **replaces**. For many values per key, use `Map<K, List<V>>` (Part 7).

### Mistake 4: Your own class as a key without `equals`/`hashCode`

`get` returns `null` even though you "put the same thing". **Fix:** Use a record, or generate `equals`/`hashCode`.

### Mistake 5: Changing a map while looping over it

```java
for (String key : map.keySet()) {
    map.remove(key);   // 💥 ConcurrentModificationException
}
```

**Fix:** `map.keySet().removeIf(key -> ...)` or `map.entrySet().removeIf(e -> ...)`.

### Mistake 6: Primitive types in `< >`

```java
Map<String, int> m;       // ❌
Map<String, Integer> m;   // ✅
```

---

## ✅ Summary

- A **Map** stores **key → value** pairs. Look up by **key**, super fast. 🗄️
- `Map<String, Integer> m = new HashMap<>();`
- `put` (add/replace), `get` (or `null`), `getOrDefault`, `containsKey`, `remove`, `size`.
- **Keys are unique**; values can repeat.
- Loop with `keySet()`, `values()`, or `entrySet()` (`getKey()` / `getValue()`).
- `HashMap` → no order. `LinkedHashMap` → insertion order. `TreeMap` → sorted keys.
- **Counting pattern:** `counts.merge(word, 1, Integer::sum);`
- **Grouping pattern:** `map.computeIfAbsent(key, k -> new ArrayList<>()).add(value);`
- Keys need `equals()` and `hashCode()` → Strings, enums and **records** are perfect keys.
- `Map.of(...)` is immutable.

---

## ❓ Quiz

1. What is the difference between a List and a Map?
2. What does `map.get("x")` return if `"x"` is not a key?
3. What happens if you `put` the same key twice?
4. Which Map keeps the keys sorted?
5. How do you loop over both keys and values?
6. Write the one-line counting pattern with `merge`.
7. Why are records good map keys?
8. What's wrong? `int n = map.get("missing");`

<details>
<summary>Click to see the answers</summary>

1. A List finds items by **position** (index). A Map finds values by **key**.
2. `null`
3. The new value replaces the old one. The size doesn't change.
4. `TreeMap`
5. `for (Map.Entry<K, V> e : map.entrySet()) { e.getKey(); e.getValue(); }`
6. `counts.merge(word, 1, Integer::sum);`
7. They have `equals()` and `hashCode()` automatically, and they are immutable.
8. `get` returns `null`, and unboxing `null` into an `int` throws a `NullPointerException`. Use `getOrDefault`.

</details>

---

[⬅ Previous chapter](30-lists.md) | [Table of Contents](../README.md) | [Next chapter: Sets ➡](32-sets.md)
