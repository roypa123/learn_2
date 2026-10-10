# Chapter 32 – Sets (`HashSet`)

[⬅ Previous chapter](31-maps.md) | [Table of Contents](../README.md) | [Next chapter ➡](33-exceptions.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **Set** is: a collection with **no duplicates**
- How to **add**, **remove** and **check** items
- How to **remove duplicates** from a list in one line
- **Set math**: union, intersection, difference
- **`HashSet`**, **`LinkedHashSet`** and **`TreeSet`** — and their order
- When to use a **List**, a **Set** or a **Map**

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Set** | A collection where every item appears **only once**. No duplicates. |
| **Duplicate** | The **same** item two (or more) times. |
| **Union** | All items from **both** sets together. (A **or** B) |
| **Intersection** | Only the items that are in **both** sets. (A **and** B) |
| **Difference** | Items in A that are **not** in B. (A **minus** B) |

---

## 📖 Story: The sticker album 📒

You collect football stickers. Your album has **one place** for each player.

- You get Messi → put him in the album ✅
- You get Ronaldo → put him in ✅
- You get Messi **again** → he's **already** in the album! You can't add him twice. ❌ (You give him to your friend. 😄)

The album is a **Set**: every sticker appears **only once**. You don't care about the order — you only care: "**Do I have this one or not?**"

---

## 🎯 Part 1: Your first `HashSet`

```java
import java.util.HashSet;
import java.util.Set;

public class Stickers {
    public static void main(String[] args) {
        Set<String> album = new HashSet<>();

        System.out.println(album.add("Messi"));     // true  — added
        System.out.println(album.add("Ronaldo"));   // true  — added
        System.out.println(album.add("Messi"));     // false — already there!
        album.add("Salah");

        System.out.println(album);
        System.out.println("Size: " + album.size());
        System.out.println("Have Salah? " + album.contains("Salah"));
        System.out.println("Have Neymar? " + album.contains("Neymar"));
    }
}
```

**Output:**

```
true
true
false
[Ronaldo, Salah, Messi]
Size: 3
Have Salah? true
Have Neymar? false
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `Set<String> album = new HashSet<>();` | A set of Strings. `Set` is the interface, `HashSet` is the class. |
| `album.add("Messi")` | Add. Returns `true` if it was **new**, `false` if it was **already there**. |
| `album.add("Messi")` (again) | Already there → **not added**, returns `false`. No error! |
| `album.size()` | 3 — Messi counts **once**. |
| `album.contains("Salah")` | Is it in the set? ⚡ **Very fast**, even with millions of items. |

> 💡 Again, `HashSet` has **no order** (like `HashMap`). We added Messi, Ronaldo, Salah — it printed Ronaldo, Salah, Messi.

### 🚫 No index!

```java
album.get(0);   // ❌ error: cannot find symbol
```

A set has **no positions**. There's no "first" or "second" sticker. You can only ask "is it in?" or loop over all of them:

```java
for (String player : album) {
    System.out.println("⚽ " + player);
}
```

---

## 🧰 Part 2: Set methods

| Method | What it does | Returns |
|---|---|---|
| `add(x)` | add (if not already there) | `true` if added |
| `remove(x)` | remove | `true` if it was there |
| `contains(x)` | is it in? ⚡ fast | `boolean` |
| `size()` | how many | `int` |
| `isEmpty()` | empty? | `boolean` |
| `clear()` | remove all | — |
| `addAll(other)` | add all items of another collection | `true` if something changed |
| `retainAll(other)` | keep only items that are **also** in `other` | |
| `removeAll(other)` | remove all items that are in `other` | |

### ⚡ Why is `contains` so fast?

| | `list.contains(x)` | `set.contains(x)` |
|---|---|---|
| How it works | checks item 1, item 2, item 3... one by one 🐢 | jumps **directly** to the right "drawer" using the hash code ⚡ |
| 1,000,000 items | up to 1,000,000 checks | about 1 check |

👉 If you often ask "**is X in here?**", use a **Set**.

---

## 🧹 Part 3: Remove duplicates — in one line!

Remember Task 5 in Chapter 30 (remove duplicates from a list)? With a Set, it's **easy**:

```java
List<String> names = List.of("Ali", "Sara", "Ali", "Tom", "Sara", "Ali");

Set<String> unique = new HashSet<>(names);
System.out.println(unique);         // [Tom, Sara, Ali]   (no order)
System.out.println(unique.size());  // 3
```

`new HashSet<>(names)` puts all the names in a set → duplicates **disappear automatically**. ✨

### Keep the original order: `LinkedHashSet`

```java
Set<String> uniqueInOrder = new LinkedHashSet<>(names);
System.out.println(uniqueInOrder);   // [Ali, Sara, Tom]  ← first-seen order ✅
```

### Back to a list

```java
List<String> cleanList = new ArrayList<>(new LinkedHashSet<>(names));
```

---

## 📚 Part 4: `HashSet`, `LinkedHashSet`, `TreeSet`

Exactly like the maps in Chapter 31:

```java
List<String> fruits = List.of("cherry", "apple", "banana", "apple");

Set<String> hash   = new HashSet<>(fruits);
Set<String> linked = new LinkedHashSet<>(fruits);
Set<String> tree   = new TreeSet<>(fruits);

System.out.println("HashSet:       " + hash);
System.out.println("LinkedHashSet: " + linked);
System.out.println("TreeSet:       " + tree);
```

**Output:**

```
HashSet:       [banana, cherry, apple]
LinkedHashSet: [cherry, apple, banana]
TreeSet:       [apple, banana, cherry]
```

| Class | Order | Speed |
|---|---|---|
| `HashSet` | ❓ no order | ⚡ fastest |
| `LinkedHashSet` | 📝 the order you added | ⚡ fast |
| `TreeSet` | 🔤 sorted | 🐢 a bit slower |

### `TreeSet` extras — because it's sorted

```java
TreeSet<Integer> scores = new TreeSet<>(List.of(55, 92, 78, 61, 85));

System.out.println(scores);              // [55, 61, 78, 85, 92]
System.out.println(scores.first());      // 55  — smallest
System.out.println(scores.last());       // 92  — biggest
System.out.println(scores.headSet(70));  // [55, 61]  — everything below 70
System.out.println(scores.ceiling(80));  // 85  — the smallest one >= 80
```

(Here the variable type is `TreeSet`, not `Set`, because `first()`, `last()` etc. only exist in `TreeSet`.)

---

## ➕ Part 5: Set math 🧮

Two friends, two sticker albums:

```java
Set<String> sara = new TreeSet<>(Set.of("Messi", "Ronaldo", "Salah", "Mbappe"));
Set<String> tom  = new TreeSet<>(Set.of("Messi", "Kane", "Salah", "Neymar"));
```

```
        Sara                       Tom
   ┌──────────────┐          ┌──────────────┐
   │  Ronaldo  ┌──┼──────────┼──┐  Kane     │
   │  Mbappe   │  │ Messi    │  │  Neymar   │
   │           │  │ Salah    │  │           │
   │           └──┼──────────┼──┘           │
   └──────────────┘          └──────────────┘
```

### Union — all stickers they have together (A ∪ B)

```java
Set<String> all = new TreeSet<>(sara);
all.addAll(tom);
System.out.println(all);   // [Kane, Mbappe, Messi, Neymar, Ronaldo, Salah]
```

### Intersection — stickers they **both** have (A ∩ B)

```java
Set<String> both = new TreeSet<>(sara);
both.retainAll(tom);
System.out.println(both);   // [Messi, Salah]
```

### Difference — Sara has, Tom doesn't (A − B)

```java
Set<String> onlySara = new TreeSet<>(sara);
onlySara.removeAll(tom);
System.out.println(onlySara);   // [Mbappe, Ronaldo]  → Sara can trade these! 🔄
```

> ⚠️ `addAll`, `retainAll` and `removeAll` **change** the set. That's why we make a **copy** first (`new TreeSet<>(sara)`), so the original stays the same.

### 📋 Summary

| Math | Java | Story |
|---|---|---|
| A ∪ B (union) | `copyOfA.addAll(B)` | everything |
| A ∩ B (intersection) | `copyOfA.retainAll(B)` | what we **both** have |
| A − B (difference) | `copyOfA.removeAll(B)` | what **only A** has |

---

## 🔑 Part 6: Sets of your own objects

Like Map keys (Chapter 31), set items need **`equals()`** and **`hashCode()`** to detect duplicates. Records have them for free:

```java
record Point(int x, int y) { }

Set<Point> visited = new HashSet<>();
visited.add(new Point(1, 2));
visited.add(new Point(3, 4));
visited.add(new Point(1, 2));   // same content → duplicate!

System.out.println(visited.size());                     // 2 ✅
System.out.println(visited.contains(new Point(3, 4)));  // true ✅
```

With a normal class **without** `equals`/`hashCode`:

```java
class Spot {
    int x, y;
    Spot(int x, int y) { this.x = x; this.y = y; }
}

Set<Spot> spots = new HashSet<>();
spots.add(new Spot(1, 2));
spots.add(new Spot(1, 2));
System.out.println(spots.size());   // 2 😱 — Java thinks they're different!
```

👉 **Rule:** For Sets and Map keys, use **records**, Strings, numbers, enums — or write `equals` + `hashCode`.

### `EnumSet` — a set of enum values

```java
enum Topping { CHEESE, HAM, MUSHROOM, OLIVE, PINEAPPLE }

Set<Topping> myPizza = EnumSet.of(Topping.CHEESE, Topping.MUSHROOM);
myPizza.add(Topping.OLIVE);
System.out.println(myPizza);   // [CHEESE, MUSHROOM, OLIVE]

Set<Topping> notOnMyPizza = EnumSet.complementOf(EnumSet.copyOf(myPizza));
System.out.println(notOnMyPizza);   // [HAM, PINEAPPLE]
```

Super fast and kept in enum order. 🍕

---

## 🤔 Part 7: List, Set or Map?

| Question | Use |
|---|---|
| Do I need items **in order**, maybe with **duplicates**? Access by **position**? | **List** 🚂 |
| Do I need **unique** items? Mostly ask "**is it in there?**" | **Set** 📒 |
| Do I need to **look up** a value by a **key**? | **Map** 🗄️ |

### Examples

| Data | Best choice | Why |
|---|---|---|
| Songs in a playlist 🎵 | `List<Song>` | order matters, the same song can appear twice |
| Usernames already taken 👤 | `Set<String>` | unique, fast "is it taken?" check |
| Student ID → Student 🎓 | `Map<Integer, Student>` | look up by ID |
| Words in a book, counted 📖 | `Map<String, Integer>` | word → count |
| Tags on a blog post 🏷️ | `Set<String>` | no duplicate tags |
| Moves in a chess game ♟️ | `List<Move>` | order matters |

### The family tree 🌳

```
                    Collection
                    /        \
                 List        Set               Map (separate family)
                  │        /  │   \           /   │    \
            ArrayList HashSet │  TreeSet  HashMap │  TreeMap
                       LinkedHashSet          LinkedHashMap
```

> 🌱 **Spring Boot note:** In databases, a student's courses are often a `Set<Course>` (no duplicates), and in JSON a list becomes `[...]`. You'll choose between `List` and `Set` many times in Part 9!

---

## 💻 Mini project: Username checker 👤

```java
import java.util.*;

public class SignUp {
    private final Set<String> takenNames = new HashSet<>();
    private static final Set<String> FORBIDDEN = Set.of("admin", "root", "support");

    public boolean register(String username) {
        String name = username.strip().toLowerCase();

        if (name.length() < 3) {
            System.out.println("❌ '" + username + "' is too short.");
            return false;
        }
        if (FORBIDDEN.contains(name)) {
            System.out.println("❌ '" + username + "' is not allowed.");
            return false;
        }
        if (!takenNames.add(name)) {      // add returns false if it was already there!
            System.out.println("❌ '" + username + "' is already taken. Try: " + suggest(name));
            return false;
        }
        System.out.println("✅ Welcome, " + name + "!");
        return true;
    }

    private String suggest(String name) {
        int n = 1;
        while (takenNames.contains(name + n)) {
            n++;
        }
        return name + n;
    }

    public static void main(String[] args) {
        SignUp app = new SignUp();
        app.register("sara");
        app.register("Tom");
        app.register("SARA");
        app.register("sara1");
        app.register("Sara");
        app.register("Admin");
        app.register("al");
        System.out.println("Users: " + new TreeSet<>(app.takenNames));
    }
}
```

**Output:**

```
✅ Welcome, sara!
✅ Welcome, tom!
❌ 'SARA' is already taken. Try: sara1
✅ Welcome, sara1!
❌ 'Sara' is already taken. Try: sara2
❌ 'Admin' is not allowed.
❌ 'al' is too short.
Users: [sara, sara1, tom]
```

### 🔍 Key ideas

| Code | Idea |
|---|---|
| `toLowerCase()` before adding | "SARA" and "sara" count as the **same** name. |
| `Set.of("admin", ...)` | An immutable set of forbidden names. Fast `contains` check. |
| `if (!takenNames.add(name))` | A neat trick: `add` **tries** to add and tells you if it was **new**. One step instead of two! |
| `new TreeSet<>(app.takenNames)` | Print the users **sorted**. |

---

## ✋ Try it yourself

**Task 1:** Make a `Set<Integer>` and add the numbers `5, 3, 5, 1, 3, 9`. Print the set and its size. Then try `TreeSet` instead. What's different?

**Task 2:** Count how many **different** words are in this sentence: `"the cat saw the dog and the dog saw the cat"`. (Answer: 5)

<details>
<summary>Click to see the answer</summary>

```java
String text = "the cat saw the dog and the dog saw the cat";
Set<String> words = new HashSet<>(Arrays.asList(text.split(" ")));
System.out.println(words.size());   // 5
```

</details>

**Task 3:** Two classes have lists of students who like football:
- 5A: Sara, Tom, Ali, Lina
- 5B: Tom, Ben, Lina, Zoe

Print: everyone who likes football, students in **both** lists, and students **only** in 5A.

**Task 4:** Write a method `boolean hasDuplicates(List<Integer> numbers)`. Hint: compare `numbers.size()` with the size of a set made from it.

<details>
<summary>Click to see the answer</summary>

```java
public static boolean hasDuplicates(List<Integer> numbers) {
    return new HashSet<>(numbers).size() < numbers.size();
}
```

</details>

**Task 5:** Find the **first** repeated character in a word: `"programming"` → `'r'`. (Hint: loop over the characters, and use `seen.add(c)` — when it returns `false`, you found it!)

<details>
<summary>Click to see the answer</summary>

```java
String word = "programming";
Set<Character> seen = new HashSet<>();
for (char c : word.toCharArray()) {
    if (!seen.add(c)) {
        System.out.println("First repeat: " + c);   // r
        break;
    }
}
```

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Trying to get by index

```java
set.get(0);   // ❌ sets have no index
```

**Fix:** Loop over it, or convert: `new ArrayList<>(set).get(0)`.

### Mistake 2: Expecting an order from `HashSet`

**Fix:** `LinkedHashSet` (insertion order) or `TreeSet` (sorted).

### Mistake 3: Own class without `equals`/`hashCode`

Duplicates are not detected. **Fix:** Use a record (or generate the methods).

### Mistake 4: Changing the original by accident

```java
Set<String> both = sara;   // ⚠️ NOT a copy — the same set!
both.retainAll(tom);       // 😱 sara is changed too
```

**Fix:** `Set<String> both = new HashSet<>(sara);`

### Mistake 5: `Set.of` with duplicates

```java
Set.of("a", "b", "a");   // 💥 IllegalArgumentException: duplicate element: a
```

`Set.of` refuses duplicates. Use `new HashSet<>(List.of("a", "b", "a"))` if your data may have them.

### Mistake 6: `TreeSet` with objects that can't be compared

```java
new TreeSet<Spot>().add(new Spot(1, 2));   // 💥 ClassCastException: Spot cannot be cast to Comparable
```

A `TreeSet` must **sort**, so items need `Comparable` (Chapter 25) — or give it a `Comparator`: `new TreeSet<>(Comparator.comparing(...))`.

---

## ✅ Summary

- A **Set** holds **unique** items — no duplicates, no index. 📒
- `Set<String> s = new HashSet<>();` → `add` (returns `false` for duplicates), `remove`, `contains` (⚡ fast), `size`.
- Remove duplicates: `new HashSet<>(list)` — or `new LinkedHashSet<>(list)` to keep the order.
- `HashSet` → no order. `LinkedHashSet` → insertion order. `TreeSet` → sorted (with `first`, `last`, ...).
- Set math on **copies**: `addAll` (union), `retainAll` (intersection), `removeAll` (difference).
- Items need `equals()` and `hashCode()` → use records, Strings, numbers, enums.
- **List** = order + duplicates. **Set** = unique + fast "contains". **Map** = look up by key.

---

## ❓ Quiz

1. What is special about a Set?
2. What does `set.add("x")` return if `"x"` is already there?
3. How do you remove duplicates from a list?
4. Which set keeps items sorted?
5. How do you find the items that are in **both** set A and set B?
6. Can you write `set.get(2)`?
7. Why is `set.contains(x)` faster than `list.contains(x)`?
8. Usernames must be unique and checked quickly. List, Set or Map?

<details>
<summary>Click to see the answers</summary>

1. Every item appears only once (no duplicates).
2. `false`
3. `new HashSet<>(list)` (or `new LinkedHashSet<>(list)` to keep the order).
4. `TreeSet`
5. Copy A, then `copy.retainAll(B)`.
6. No — sets have no index.
7. A HashSet uses the hash code to jump directly to the right place. A list checks items one by one.
8. A Set.

</details>

---

[⬅ Previous chapter](31-maps.md) | [Table of Contents](../README.md) | [Next chapter: Exceptions ➡](33-exceptions.md)
