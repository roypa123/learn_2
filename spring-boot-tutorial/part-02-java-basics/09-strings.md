# Chapter 9 – Text in Java (Strings)

[⬅ Previous chapter](08-math-operators.md) | [Table of Contents](../README.md) | [Next chapter ➡](10-if-else.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **String** really is (a row of characters)
- What an **index** is, and why counting starts at **0**
- The most useful String **methods**: `length`, `toUpperCase`, `charAt`, `indexOf`, `substring`, `replace`, `contains`, `trim`, `split`...
- How to **compare** two Strings correctly (`equals`, not `==`!)
- How to build nice text with `String.format` and **text blocks**

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **String** | Text. A row of characters. |
| **Character** | One letter, number, space or symbol. |
| **Index** | The **position number** of a character. The first one is **0**. |
| **Method** | A "job" that a String can do, like `toUpperCase()`. We call it with a **dot**: `name.toUpperCase()`. |
| **Return** | What a method **gives back**. `name.length()` returns a number. |
| **Immutable** | **Cannot be changed.** A String never changes; methods make a **new** String. |
| **Empty String** | A String with **no** characters: `""`. |

---

## 📖 Story: A train of letters 🚂

Think of a String as a **train**. Every wagon carries **one** character.
Every wagon has a **number** — but the numbering starts at **0**, not 1!

```
 String word = "HELLO";

   ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐
   │ H │-│ E │-│ L │-│ L │-│ O │
   └───┘ └───┘ └───┘ └───┘ └───┘
     0     1     2     3     4      ← index (position)
```

- The train has **5** wagons. → `length` is **5**.
- The **first** wagon is number **0**.
- The **last** wagon is number **4** (that's length − 1).

> 🤔 **Why start at 0?** Think of it as "how many steps from the start". The first wagon is **0 steps** from the start. The second is 1 step away. Almost all programming languages count this way. You'll get used to it! 😊

---

## 📏 Part 1: `length()` — how long is it?

```java
String name = "Sara";
System.out.println(name.length());   // 4

String sentence = "I like Java!";
System.out.println(sentence.length());   // 12

String empty = "";
System.out.println(empty.length());   // 0
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `name` | The String variable. |
| `.` | "Go into" — use an ability of this String. |
| `length` | The method name: "tell me how many characters". |
| `()` | Brackets are **needed** to call a method, even when they are empty. |

> 💡 **Spaces and symbols count too!** `"I like Java!"` has 12 characters: 9 letters, 2 spaces and 1 `!`.

---

## 🔠 Part 2: Big and small letters

```java
String city = "London";

System.out.println(city.toUpperCase());   // LONDON
System.out.println(city.toLowerCase());   // london
System.out.println(city);                 // London  ← not changed!
```

### 🔍 Line by line

| Method | What it returns |
|---|---|
| `toUpperCase()` | A **new** String, all CAPITAL letters. |
| `toLowerCase()` | A **new** String, all small letters. |

### ⚠️ Strings never change (immutable)

Look at the last line: `city` is **still** `"London"`. The methods did **not** change it. They made a **new** String.

If you want to keep the new one, you must **save** it:

```java
String city = "London";
city = city.toUpperCase();     // put the new String back into the box
System.out.println(city);      // LONDON
```

🖨️ Think of it like a photocopy machine. You put in a page, and you get a **new** copy in capital letters. The original page doesn't change.

---

## 🔍 Part 3: `charAt()` — get one character

```java
String word = "HELLO";

System.out.println(word.charAt(0));   // H
System.out.println(word.charAt(1));   // E
System.out.println(word.charAt(4));   // O

char last = word.charAt(word.length() - 1);
System.out.println(last);             // O
```

### 🔍 Line by line

| Line | Meaning |
|---|---|
| `word.charAt(0)` | "Give me the character at **index 0**" → `'H'`. It returns a `char`. |
| `word.charAt(4)` | Index 4 → the 5th character → `'O'`. |
| `word.length() - 1` | 5 − 1 = **4**. The index of the **last** character. This trick works for **any** String! |

### 💥 Going outside the train

```java
word.charAt(5);   // 💥 StringIndexOutOfBoundsException: index 5, length 5
```

There is no wagon number 5! The program crashes. Remember: the last index is **length − 1**.

---

## 🔎 Part 4: Searching in a String

### `indexOf()` — where is it?

```java
String text = "banana";

System.out.println(text.indexOf("n"));      // 2   (the first "n")
System.out.println(text.indexOf("nan"));    // 2
System.out.println(text.indexOf("x"));      // -1  (not found!)
System.out.println(text.lastIndexOf("a"));  // 5   (the last "a")
```

```
   b   a   n   a   n   a
   0   1   2   3   4   5
           ▲
           first "n" is at 2
```

| Method | Returns |
|---|---|
| `indexOf("n")` | The index of the **first** place where `"n"` is found. |
| `lastIndexOf("a")` | The index of the **last** place where `"a"` is found. |
| If not found | **`-1`** (because −1 can never be a real index). |

### `contains()`, `startsWith()`, `endsWith()` — yes or no?

These return a **boolean** (`true` / `false`):

```java
String email = "sara@mail.com";

System.out.println(email.contains("@"));         // true
System.out.println(email.startsWith("sara"));    // true
System.out.println(email.endsWith(".com"));      // true
System.out.println(email.endsWith(".org"));      // false
```

| Method | Question it answers |
|---|---|
| `contains("@")` | Is `"@"` **anywhere** inside? |
| `startsWith("sara")` | Does it **begin** with `"sara"`? |
| `endsWith(".com")` | Does it **end** with `".com"`? |

---

## ✂️ Part 5: `substring()` — cut a piece

```java
String text = "Hello World";

System.out.println(text.substring(6));      // World
System.out.println(text.substring(0, 5));   // Hello
System.out.println(text.substring(3, 8));   // lo Wo
```

```
   H   e   l   l   o       W   o   r   l   d
   0   1   2   3   4   5   6   7   8   9   10
```

### 🔍 Line by line

| Call | Meaning | Result |
|---|---|---|
| `substring(6)` | From index **6** to the **end**. | `"World"` |
| `substring(0, 5)` | From index **0**, **up to but not including** index **5**. So: 0, 1, 2, 3, 4. | `"Hello"` |
| `substring(3, 8)` | Index 3, 4, 5, 6, 7 (not 8). | `"lo Wo"` |

> 💡 **Easy trick:** In `substring(start, end)`, the number of characters you get is **end − start**. `substring(0, 5)` → 5 characters.

### Example: get the user name from an email

```java
String email = "sara@mail.com";
int at = email.indexOf("@");              // 4
String user = email.substring(0, at);     // "sara"
String domain = email.substring(at + 1);  // "mail.com"

System.out.println("User: " + user);
System.out.println("Domain: " + domain);
```

**Output:**

```
User: sara
Domain: mail.com
```

| Line | Value |
|---|---|
| `email.indexOf("@")` | `4` |
| `email.substring(0, 4)` | index 0–3 → `"sara"` |
| `email.substring(5)` | from index 5 → `"mail.com"` (we skip the `@` with `+ 1`) |

---

## 🔁 Part 6: `replace()` — change parts

```java
String sentence = "I like cats. Cats are cute.";

System.out.println(sentence.replace("cats", "dogs"));
System.out.println(sentence.replace("a", "@"));
```

**Output:**

```
I like dogs. Cats are cute.
I like c@ts. C@ts @re cute.
```

### 🔍 Line by line

| Call | Meaning |
|---|---|
| `replace("cats", "dogs")` | Change **every** `"cats"` into `"dogs"`. ⚠️ `"Cats"` (capital C) is **not** changed — it's a different word for Java! |
| `replace("a", "@")` | Change **every** `"a"` into `"@"`. |

---

## 🧹 Part 7: `trim()` and `strip()` — remove extra spaces

Users often type extra spaces by mistake:

```java
String input = "   Sara   ";

System.out.println("[" + input + "]");          // [   Sara   ]
System.out.println("[" + input.trim() + "]");   // [Sara]
System.out.println("[" + input.strip() + "]");  // [Sara]
```

| Method | Meaning |
|---|---|
| `trim()` | Remove spaces at the **start** and **end**. (Spaces in the middle stay.) |
| `strip()` | Same idea, but newer and better with special spaces from other languages. |

> 💡 We put `[` `]` around the text so you can **see** the spaces.

### `isEmpty()` and `isBlank()`

```java
System.out.println("".isEmpty());       // true   (no characters)
System.out.println("   ".isEmpty());    // false  (3 spaces are 3 characters)
System.out.println("   ".isBlank());    // true   (only spaces = blank)
System.out.println("Hi".isBlank());     // false
```

| Method | `true` when... |
|---|---|
| `isEmpty()` | length is 0 |
| `isBlank()` | empty **or** only spaces |

👉 `isBlank()` is great for checking forms: "Did the user really type a name?"

---

## ✂️ Part 8: `split()` — cut into many pieces

```java
String fruits = "apple,banana,cherry";
String[] parts = fruits.split(",");

System.out.println(parts[0]);       // apple
System.out.println(parts[1]);       // banana
System.out.println(parts[2]);       // cherry
System.out.println(parts.length);   // 3
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `fruits.split(",")` | Cut the String at every `,`. |
| `String[]` | The result is a **list** of Strings (an **array**). We learn arrays in Chapter 14. |
| `parts[0]` | The **first** piece. (Yes, index 0 again!) |
| `parts.length` | How many pieces. ⚠️ For arrays there are **no** brackets: `length`, not `length()`. |

Split a sentence into words:

```java
String sentence = "Java is fun";
String[] words = sentence.split(" ");
System.out.println(words.length);   // 3
```

---

## 🔗 Part 9: Joining Strings

You already know `+`. Here are more ways:

```java
String first = "Sara";
String last = "Ali";

String a = first + " " + last;              // "Sara Ali"
String b = first.concat(" ").concat(last);  // "Sara Ali"
String c = String.join("-", "2025", "01", "15");  // "2025-01-15"
String d = "ha".repeat(3);                  // "hahaha"
```

| Way | Meaning |
|---|---|
| `+` | Glue. The most common. |
| `concat(...)` | Glue (method version). |
| `String.join("-", ...)` | Glue many Strings with `"-"` **between** them. |
| `repeat(3)` | Repeat the String 3 times. |

---

## ⚖️ Part 10: Comparing Strings — VERY IMPORTANT ⚠️

### ✅ Use `equals()`

```java
String a = "hello";
String b = "hello";
String c = "Hello";

System.out.println(a.equals(b));            // true
System.out.println(a.equals(c));            // false  (H vs h)
System.out.println(a.equalsIgnoreCase(c));  // true   (ignore big/small)
```

| Method | Meaning |
|---|---|
| `a.equals(b)` | Do `a` and `b` have **exactly the same** characters? |
| `a.equalsIgnoreCase(c)` | Same characters, but **don't care** about big and small letters. |

### ❌ Don't use `==` for Strings

```java
String x = "hi";
String y = new String("hi");

System.out.println(x == y);        // false 😱
System.out.println(x.equals(y));   // true ✅
```

### 🤔 Why?

📖 **Story:** Two people each have a book called *"Harry Potter"*.
- `equals` asks: "Do the books have the **same text**?" → **Yes**.
- `==` asks: "Is it the **same physical book**?" → **No**, there are two books!

For Strings, `==` checks if it is the **same object in memory**, not the same text. Sometimes it works by luck, sometimes not. That makes **very confusing bugs**.

👉 **Golden rule:**
- Numbers (`int`, `double`, `char`, `boolean`) → compare with `==`
- **Strings** → compare with **`.equals()`**

### `compareTo()` — alphabetical order

```java
System.out.println("apple".compareTo("banana"));   // negative number → apple comes first
System.out.println("banana".compareTo("apple"));   // positive number → banana comes later
System.out.println("apple".compareTo("apple"));    // 0 → the same
```

You only need to look at the **sign**: negative, zero or positive. This is used for **sorting** (Chapter 14).

---

## 🎨 Part 11: Nice formatting with `String.format`

Gluing with `+` can get messy:

```java
String name = "Sara";
int age = 12;
double height = 1.456;

System.out.println("Name: " + name + ", Age: " + age + ", Height: " + height);
```

`String.format` is cleaner. You write the text with **placeholders**, then the values:

```java
String text = String.format("Name: %s, Age: %d, Height: %.2f", name, age, height);
System.out.println(text);
```

**Output:**

```
Name: Sara, Age: 12, Height: 1.46
```

### 🔍 Placeholders

| Placeholder | For | Example |
|---|---|---|
| `%s` | **S**tring (any text) | `name` → `Sara` |
| `%d` | whole number (**d**ecimal integer) | `age` → `12` |
| `%f` | decimal number (**f**loat/double) | `height` → `1.456000` |
| `%.2f` | decimal number with **2** digits after the dot (rounded) | `height` → `1.46` |
| `%n` | a new line | |
| `%%` | a real `%` sign | |

The values are used **in order**: first `%s` ← `name`, then `%d` ← `age`, then `%.2f` ← `height`.

### Shortcuts

```java
// printf = print + format, in one step (add %n for a new line!)
System.out.printf("Price: %.2f%n", 9.5);          // Price: 9.50

// .formatted() — a newer, shorter way
String msg = "Hello %s!".formatted("Sara");       // "Hello Sara!"
```

---

## 📜 Part 12: Special characters and text blocks

### Escape characters (from Chapter 5)

| Write | Meaning |
|---|---|
| `\n` | new line |
| `\t` | tab (a big space, to make columns) |
| `\"` | a `"` inside the text |
| `\\` | one `\` |

```java
System.out.println("Name:\tSara\nAge:\t12");
```

**Output:**

```
Name:	Sara
Age:	12
```

### Text blocks `"""` — for long text

Since Java 15, you can write text on **many lines** easily:

```java
String poem = """
        Roses are red,
        Violets are blue,
        Java is fun,
        And so are you!
        """;
System.out.println(poem);
```

**Output:**

```
Roses are red,
Violets are blue,
Java is fun,
And so are you!
```

| Part | Meaning |
|---|---|
| `"""` + new line | Start of the text block. |
| The lines | The text, exactly as you see it. Java removes the common spaces on the left. |
| `"""` | End of the text block. |

👉 Text blocks are very useful later for **JSON** and **SQL** in Spring Boot! 🌱

---

## 💻 Mini project: Name card 🪪

```java
public class NameCard {
    public static void main(String[] args) {
        String fullName = "  sara ahmed ali  ";

        // 1. Clean the spaces
        String clean = fullName.strip();

        // 2. Split into words
        String[] names = clean.split(" ");
        String first = names[0];
        String last = names[names.length - 1];

        // 3. First letter big, rest small
        String niceFirst = first.substring(0, 1).toUpperCase() + first.substring(1);
        String niceLast = last.substring(0, 1).toUpperCase() + last.substring(1);

        // 4. Initials
        char initial1 = niceFirst.charAt(0);
        char initial2 = niceLast.charAt(0);

        System.out.println("Full name:  " + clean);
        System.out.println("Nice name:  " + niceFirst + " " + niceLast);
        System.out.println("Initials:   " + initial1 + "." + initial2 + ".");
        System.out.println("Characters: " + clean.length());
    }
}
```

**Output:**

```
Full name:  sara ahmed ali
Nice name:  Sara Ali
Initials:   S.A.
Characters: 14
```

### 🔍 Line by line

| Line | Value |
|---|---|
| `fullName.strip()` | `"sara ahmed ali"` (spaces at the start and end removed) |
| `clean.split(" ")` | `["sara", "ahmed", "ali"]` |
| `names[0]` | `"sara"` |
| `names[names.length - 1]` | `names[2]` → `"ali"` (the **last** word) |
| `first.substring(0, 1)` | `"s"` (the first letter) |
| `.toUpperCase()` | `"S"` |
| `first.substring(1)` | `"ara"` (the rest) |
| `"S" + "ara"` | `"Sara"` |
| `niceFirst.charAt(0)` | `'S'` |
| `initial1 + "." + initial2 + "."` | `"S.A."` |

> 💡 Why `initial1 + "." + ...` and not `initial1 + initial2`? Because two `char`s added together become a **number** (remember: chars are numbers inside!). `'S' + 'A'` = 83 + 65 = **148** 😮. With a String `"."` in the middle, everything is glued as text.

---

## 📋 Cheat sheet: String methods

| Method | Returns | Example | Result |
|---|---|---|---|
| `length()` | int | `"Java".length()` | `4` |
| `charAt(i)` | char | `"Java".charAt(0)` | `'J'` |
| `toUpperCase()` | String | `"Java".toUpperCase()` | `"JAVA"` |
| `toLowerCase()` | String | `"Java".toLowerCase()` | `"java"` |
| `indexOf(s)` | int | `"Java".indexOf("v")` | `2` |
| `contains(s)` | boolean | `"Java".contains("av")` | `true` |
| `startsWith(s)` | boolean | `"Java".startsWith("J")` | `true` |
| `endsWith(s)` | boolean | `"Java".endsWith("a")` | `true` |
| `substring(a)` | String | `"Java".substring(2)` | `"va"` |
| `substring(a, b)` | String | `"Java".substring(1, 3)` | `"av"` |
| `replace(a, b)` | String | `"Java".replace("a", "o")` | `"Jovo"` |
| `strip()` / `trim()` | String | `" Hi ".strip()` | `"Hi"` |
| `isEmpty()` | boolean | `"".isEmpty()` | `true` |
| `isBlank()` | boolean | `"  ".isBlank()` | `true` |
| `split(s)` | String[] | `"a,b".split(",")` | `["a", "b"]` |
| `repeat(n)` | String | `"ab".repeat(2)` | `"abab"` |
| `equals(s)` | boolean | `"Java".equals("java")` | `false` |
| `equalsIgnoreCase(s)` | boolean | `"Java".equalsIgnoreCase("java")` | `true` |

---

## ✋ Try it yourself

**Task 1:** You have `String word = "Programming";`. Print:
1. The length
2. The first character
3. The last character
4. The word in capital letters
5. The first 7 letters (`Program`)

<details>
<summary>Click to see the answer</summary>

```java
String word = "Programming";
System.out.println(word.length());                    // 11
System.out.println(word.charAt(0));                   // P
System.out.println(word.charAt(word.length() - 1));   // g
System.out.println(word.toUpperCase());               // PROGRAMMING
System.out.println(word.substring(0, 7));             // Program
```

</details>

**Task 2:** You have `String date = "2025-03-15";`. Use `split` to print:

```
Year: 2025
Month: 03
Day: 15
```

<details>
<summary>Click to see the answer</summary>

```java
String date = "2025-03-15";
String[] parts = date.split("-");
System.out.println("Year: " + parts[0]);
System.out.println("Month: " + parts[1]);
System.out.println("Day: " + parts[2]);
```

</details>

**Task 3:** Check a password. Print `true` or `false` for each rule:
- Is it at least 8 characters long?
- Does it contain `"@"`?
- Is it **not** equal to `"password"`? (ignore big/small letters)

Test with `"Secret@123"` and `"PASSWORD"`.

<details>
<summary>Click to see the answer</summary>

```java
String pw = "Secret@123";
System.out.println(pw.length() >= 8);                    // true
System.out.println(pw.contains("@"));                    // true
System.out.println(!pw.equalsIgnoreCase("password"));    // true
```

The `!` means "**not**" — it turns `true` into `false` and `false` into `true`. More in Chapter 10.

</details>

**Task 4:** Use `String.format` (or `printf`) to print a price list where the prices always have 2 decimals:

```
Apple:  1.50
Bread:  2.25
Milk:   0.99
```

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `()` on methods

```java
int n = name.length;     // ❌ error: cannot find symbol
int n = name.length();   // ✅
```

(But for **arrays** it's `array.length` without `()`. Confusing, we know! 😅)

### Mistake 2: Comparing Strings with `==`

```java
if (input == "yes")        // ❌ may be false even when input is "yes"
if (input.equals("yes"))   // ✅
```

### Mistake 3: Thinking the String changed

```java
String s = "hello";
s.toUpperCase();
System.out.println(s);       // hello ❌ (not saved!)

s = s.toUpperCase();
System.out.println(s);       // HELLO ✅
```

### Mistake 4: Index out of range

```java
"Hi".charAt(2);         // 💥 StringIndexOutOfBoundsException
"Hello".substring(2, 10);  // 💥 end index 10 > length 5
```

The last valid index is `length() - 1`.

### Mistake 5: Calling a method on `null`

```java
String name = null;      // null = "no String at all, the box is empty"
name.length();           // 💥 NullPointerException
```

`null` means there is **no** String. You can't ask "nothing" for its length. We learn more about `null` in Part 3.

---

## ✅ Summary

- A String is a row of characters. The **index** starts at **0**. The last index is **length − 1**.
- Call methods with a dot and brackets: `text.length()`.
- Strings are **immutable**: methods return a **new** String. Save it: `s = s.toUpperCase();`
- Search: `indexOf` (−1 = not found), `contains`, `startsWith`, `endsWith`.
- Cut: `substring(start, end)` — `end` is **not** included.
- Clean: `strip()`, `trim()`. Check: `isEmpty()`, `isBlank()`.
- Split: `split(",")` gives an array.
- **Compare Strings with `equals()`**, never `==`.
- Format nicely: `String.format("%s is %d", name, age)`, `printf`, `%.2f` for 2 decimals.
- Text blocks `"""` for long text over many lines.

---

## ❓ Quiz

1. What is the index of the first character in a String?
2. What does `"Coffee".length()` return?
3. What does `"Coffee".charAt(2)` return?
4. What does `"Coffee".indexOf("z")` return?
5. What does `"Coffee".substring(1, 4)` return?
6. How should you compare two Strings?
7. What is printed? `String s = "abc"; s.toUpperCase(); System.out.println(s);`
8. Which placeholder prints a decimal number with 2 digits after the dot?
9. What is the difference between `isEmpty()` and `isBlank()`?

<details>
<summary>Click to see the answers</summary>

1. `0`
2. `6`
3. `'f'`
4. `-1` (not found)
5. `"off"` (index 1, 2, 3)
6. With `.equals()` (or `.equalsIgnoreCase()`).
7. `abc` — the result of `toUpperCase()` was not saved.
8. `%.2f`
9. `isEmpty()` is true only when there are 0 characters. `isBlank()` is also true when there are only spaces.

</details>

---

[⬅ Previous chapter](08-math-operators.md) | [Table of Contents](../README.md) | [Next chapter: if and else ➡](10-if-else.md)
