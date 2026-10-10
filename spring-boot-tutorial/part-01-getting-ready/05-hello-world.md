# Chapter 5 – Your First Java Program: Hello World

[⬅ Previous chapter](04-install-intellij.md) | [Table of Contents](../README.md) | [Next chapter ➡](../part-02-java-basics/06-variables.md)

---

## 🎯 Goal

At the end of this chapter:

- You wrote your **first Java program** by yourself. ✍️
- You **compiled** and **ran** it in the terminal (the "by hand" way).
- You ran it in **IntelliJ** (the easy way).
- You understand **every single word** of the program.
- You know what to do when you see the most common **errors**.

⏱️ Time needed: about 45 minutes. Take your time. This chapter is **very important**.

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Hello World** | The traditional first program in every language. It just shows "Hello, World!" on the screen. |
| **Source file** | The file with your code. In Java it ends with `.java`. |
| **Class** | A "container" for code. In Java, **all** code lives inside a class. |
| **Method** | A named "job" inside a class. It has a list of instructions. |
| **`main` method** | The **starting point** of a Java program. The JVM always starts here. |
| **Statement** | One instruction. In Java, it usually ends with `;`. |
| **Output** | What the program shows (prints) on the screen. |
| **Keyword** | A special word that Java already knows, like `public`, `class`, `static`, `void`. You cannot use them as names. |
| **Curly braces** `{ }` | They show where a block of code **starts** `{` and **ends** `}`. |
| **Error** | A message that says something is wrong. |

---

## 📖 Story: A letter with an envelope

Imagine you send a letter. ✉️

- The **envelope** has a name on it: who is it for?
- Inside the envelope is the **letter**.
- The letter has **sentences**.

A Java program is the same:

```
 ┌───────────────────────────────────────────┐
 │ ✉️ ENVELOPE  =  class Hello               │
 │                                           │
 │   ┌───────────────────────────────────┐   │
 │   │ 📄 LETTER  =  main method          │   │
 │   │                                   │   │
 │   │   ✏️ SENTENCE = println("Hello")  │   │
 │   │                                   │   │
 │   └───────────────────────────────────┘   │
 └───────────────────────────────────────────┘
```

- The **class** is the envelope.
- The **main method** is the letter.
- The **statements** are the sentences.

Keep this picture in your mind. 🧠

---

## 💻 The program

Here is the full program. It is only **5 lines**:

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

When you run it, you see:

```
Hello, World!
```

It looks strange at first. There are many words just to print one sentence! 😅
Don't worry. Now we explain **every word**, one by one.

---

## 🔍 Line by line — very slowly

### Line 1: `public class Hello {`

| Word | Meaning |
|---|---|
| `public` | "Everyone can see and use this." Like a **public** park — open for all. |
| `class` | "Here I make a class." A class is the **envelope** for our code. |
| `Hello` | The **name** of the class. We choose this name. |
| `{` | "The class **starts** here." Everything until the matching `}` is inside the class. |

> ⚠️ **Rule:** If a class is `public`, the **file name must be the same** as the class name.
> Class `Hello` → file name **`Hello.java`**.
> Big and small letters must also match! `hello.java` is **wrong**.

> 💡 **Naming rule for classes:** Class names start with a **capital letter**: `Hello`, `Student`, `BankAccount`. If there are many words, every word starts with a capital letter, and there are **no spaces**. This style is called **PascalCase**.

---

### Line 2: `public static void main(String[] args) {`

This is the longest line. It is the **door** where your program begins. 🚪
The JVM looks for **exactly** this line. If it is a little different, the JVM cannot find the door.

| Word | Meaning |
|---|---|
| `public` | "Everyone can use this method." The JVM must be able to call it, so it must be public. |
| `static` | "This method belongs to the **class itself**. You don't need to create anything first." The JVM can start it immediately. (We explain `static` fully in Chapter 27.) |
| `void` | "This method **gives nothing back**." It does its job, but it does not return an answer. *Void* means "empty". |
| `main` | The **name** of the method. `main` is special: it is **always** the starting point of a Java program. |
| `(` `)` | Inside the round brackets are the **inputs** of the method (things we can give to it). |
| `String[] args` | The input: a list of texts. `String` = text. `[]` = a list. `args` = the name (short for *arguments*). You can give extra words to the program when you start it. We don't use this now. |
| `{` | "The main method **starts** here." |

👉 **Beginner tip:** You don't need to understand `public static void` 100% now. For the next chapters, just remember:

> **"`public static void main(String[] args)` is the door where the program starts."**

You will understand each word better and better as you continue the book. That's normal. 😊

---

### Line 3: `System.out.println("Hello, World!");`

This is the line that **does the work**. It prints the text.

Let's break it into small pieces:

```
System . out . println ( "Hello, World!" ) ;
  │       │      │     │        │        │ │
  │       │      │     │        │        │ └─ end of statement
  │       │      │     │        │        └─── end of input
  │       │      │     │        └──────────── the text to show
  │       │      │     └───────────────────── start of input
  │       │      └─────────────────────────── the job: print a line
  │       └────────────────────────────────── the output (screen)
  └────────────────────────────────────────── the system (your computer)
```

| Part | Meaning |
|---|---|
| `System` | A ready-made class from Java. It is about **your computer system**. |
| `.` | The dot means "**inside of**" / "**go into**". `System.out` = "the `out` that is inside `System`". |
| `out` | The **output** — normally the screen / terminal. |
| `.` | Again: "go into". |
| `println` | A method that **prints a line**. Say it like *"print line"*. It shows the text, then moves to a **new line**. |
| `(` | Start of the input to `println`. |
| `"Hello, World!"` | The text we want to show. Text in Java is called a **String**. A String is always between **double quotes** `" "`. The quotes are **not** printed. |
| `)` | End of the input. |
| `;` | **End of the statement.** Like a full stop `.` in English. Almost every statement in Java ends with `;`. |

So the whole line means:

> "Computer system → output → print this line: **Hello, World!**"

---

### Line 4: `}`

"The **main method ends** here." This `}` closes the `{` from line 2.

### Line 5: `}`

"The **class ends** here." This `}` closes the `{` from line 1.

---

### 🧩 Braces always come in pairs

Every `{` needs a `}`. Look at the colors:

```java
public class Hello {                            // 🟦 class opens
    public static void main(String[] args) {    // 🟩 main opens
        System.out.println("Hello, World!");    //    the work
    }                                           // 🟩 main closes
}                                               // 🟦 class closes
```

- The **blue** pair is the envelope (class).
- The **green** pair is the letter (main method). It is **inside** the blue pair.

> 💡 The text after `//` is a **comment**. Java ignores it. It's a note for humans. We learn more about comments in Chapter 17.

### 📏 Why the spaces at the start of lines?

Look: line 2 has 4 spaces in front. Line 3 has 8 spaces.
This is called **indentation**.

- Java **does not care** about these spaces. The program works without them.
- But **humans** care! Indentation shows what is **inside** what, like the steps of a stair. 🪜

```java
// ✅ Easy to read
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

// ❌ Works, but terrible to read
public class Hello { public static void main(String[] args) { System.out.println("Hello, World!"); } }
```

👉 Always indent your code. In IntelliJ, `Ctrl + Alt + L` does it for you.

---

## 🛠️ Part A: The "by hand" way (Notepad + terminal)

We do it this way **one time**, so you see what really happens. After this, IntelliJ does these steps for you.

### Step 1 – Make a folder

1. Open **File Explorer**.
2. Go to your **Documents** folder.
3. Make a new folder: right-click → **New** → **Folder**. Name it `java-practice`.

### Step 2 – Write the code in Notepad

1. Press the **Windows key**, type `notepad`, press **Enter**.
2. Type the program. **Type it yourself, don't copy!** Be careful with every symbol:

   ```java
   public class Hello {
       public static void main(String[] args) {
           System.out.println("Hello, World!");
       }
   }
   ```

3. Click **File → Save As...**
4. Go to your folder `Documents\java-practice`.
5. **File name:** `Hello.java`
6. **Save as type:** choose **All Files (\*.\*)** ⚠️ (very important — otherwise Notepad saves it as `Hello.java.txt`!)
7. Click **Save**.

### Step 3 – Open the terminal in your folder

1. Open the folder `java-practice` in File Explorer.
2. Click on the **address bar** at the top (where it shows the folder path).
3. Type `cmd` and press **Enter**.

A terminal opens, already "standing" in your folder:

```
C:\Users\YourName\Documents\java-practice>
```

### Step 4 – Look at the files

Type:

```
dir
```

`dir` means "**dir**ectory" = "show me the files in this folder".
You should see `Hello.java` in the list. ✅

### Step 5 – Compile

Type:

```
javac Hello.java
```

#### 🔍 Line by line

| Part | Meaning |
|---|---|
| `javac` | The Java **compiler**. |
| `Hello.java` | The file to compile. |

If everything is correct, you see **nothing**. No message = **success**! 🎉
(In programming, "no news is good news.")

Now type `dir` again. You see a **new file**: `Hello.class`. This is the **bytecode** (remember Chapter 2).

```
Hello.class    ← new! made by javac (bytecode, for the JVM)
Hello.java     ← your code (for humans)
```

### Step 6 – Run

Type:

```
java Hello
```

You see:

```
Hello, World!
```

🎉🎉🎉 **You did it! You wrote, compiled and ran a Java program!**

#### 🔍 Line by line

| Part | Meaning |
|---|---|
| `java` | Start the **JVM** (the program runner). |
| `Hello` | The **class name** to run. ⚠️ **No** `.java` and **no** `.class` at the end! Just the class name. |

The JVM finds `Hello.class`, opens it, looks for the door `public static void main(String[] args)`, and runs the statements inside.

### 🗺️ What happened — the full picture

```
  You type          javac              java
 ┌──────────┐    ┌──────────┐      ┌──────────┐      ┌────────────────┐
 │Hello.java│───►│ compiler │─────►│Hello.class│────►│ JVM runs main()│──► Hello, World!
 └──────────┘    └──────────┘      └──────────┘      └────────────────┘
   source code                       bytecode
```

> 💡 **Shortcut:** Since Java 11, you can also run a single file **directly**, without `javac`:
> ```
> java Hello.java
> ```
> Java compiles it in memory and runs it. Nice for small tests! But it's good to know the two-step way, because that's what really happens.

---

## 🛠️ Part B: The easy way (IntelliJ)

1. Open **IntelliJ** and open your project `my-first-java` from Chapter 4.
2. In the Project window, **right-click** the `src` folder.
3. Choose **New → Java Class**.
4. Type the name: `Hello` (no `.java` — IntelliJ adds it). Press **Enter**.

IntelliJ makes the file `Hello.java` and writes the envelope for you:

```java
public class Hello {
}
```

5. Click **between** `{` and `}`. Now type the main method.

> 💡 **Magic shortcut:** Type `main` and press **Enter** (or **Tab**). IntelliJ writes the whole line `public static void main(String[] args) { }` for you! 🪄
>
> **Another one:** Type `sout` and press **Enter**. IntelliJ writes `System.out.println();` for you!

6. Write the full program:

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

7. Click the green **▶** next to `public class Hello` → **Run 'Hello.main()'**.

Output in the Run window:

```
Hello, World!

Process finished with exit code 0
```

✅ The same result — but IntelliJ did `javac` and `java` for you, in one click.

---

## 💻 More small examples

### Example 1: Many lines

```java
public class AboutMe {
    public static void main(String[] args) {
        System.out.println("My name is Sara.");
        System.out.println("I am learning Java.");
        System.out.println("This is fun!");
    }
}
```

**Output:**

```
My name is Sara.
I am learning Java.
This is fun!
```

#### 🔍 Line by line

| Line | Meaning |
|---|---|
| `public class AboutMe {` | A new class called `AboutMe`. The file must be named `AboutMe.java`. |
| `public static void main(String[] args) {` | The starting door. |
| `System.out.println("My name is Sara.");` | Print the first line. |
| `System.out.println("I am learning Java.");` | Print the second line. |
| `System.out.println("This is fun!");` | Print the third line. |
| `}` | End of main. |
| `}` | End of class. |

👉 The statements run **from top to bottom**, one after another (remember Chapter 1!).

---

### Example 2: `print` vs. `println`

```java
public class PrintTest {
    public static void main(String[] args) {
        System.out.print("Hello ");
        System.out.print("there! ");
        System.out.println("How are you?");
        System.out.println("I am fine.");
    }
}
```

**Output:**

```
Hello there! How are you?
I am fine.
```

#### 🔍 Line by line

| Line | What it prints | Then the cursor... |
|---|---|---|
| `System.out.print("Hello ");` | `Hello ` | ...**stays** on the same line. |
| `System.out.print("there! ");` | `there! ` | ...**stays** on the same line. |
| `System.out.println("How are you?");` | `How are you?` | ...**goes to a new line**. |
| `System.out.println("I am fine.");` | `I am fine.` | ...goes to a new line. |

| Method | Meaning |
|---|---|
| `print` | Print the text. **Stay** on the same line. |
| `println` | Print the text. Then **go to a new line**. (`ln` = **l**i**n**e) |

> 💡 Notice the **space** inside `"Hello "`. Without it, the output would be `Hellothere!`. Java prints **exactly** what is inside the quotes — nothing more.

---

### Example 3: An empty line

```java
public class EmptyLine {
    public static void main(String[] args) {
        System.out.println("Line one");
        System.out.println();
        System.out.println("Line three");
    }
}
```

**Output:**

```
Line one

Line three
```

#### 🔍 Line by line

| Line | Meaning |
|---|---|
| `System.out.println("Line one");` | Print "Line one" and go to a new line. |
| `System.out.println();` | **Nothing** inside the brackets → print nothing, just go to a new line. This makes an **empty line**. |
| `System.out.println("Line three");` | Print "Line three". |

---

### Example 4: Printing numbers

```java
public class Numbers {
    public static void main(String[] args) {
        System.out.println(7);
        System.out.println(3 + 4);
        System.out.println("3 + 4");
    }
}
```

**Output:**

```
7
7
3 + 4
```

#### 🔍 Line by line

| Line | Output | Why |
|---|---|---|
| `System.out.println(7);` | `7` | Numbers do **not** need quotes. |
| `System.out.println(3 + 4);` | `7` | **No quotes** → Java **calculates** 3 + 4 = 7, and prints the answer. |
| `System.out.println("3 + 4");` | `3 + 4` | **With quotes** → it is **text**. Java prints it exactly, without calculating. |

👉 **Very important idea:** Quotes `" "` mean "this is **text**, don't touch it". No quotes means "this is something Java should **understand** or **calculate**". We learn much more about this in Chapters 7–9.

---

### Example 5: A small drawing 🎨

```java
public class House {
    public static void main(String[] args) {
        System.out.println("   /\\   ");
        System.out.println("  /  \\  ");
        System.out.println(" /____\\ ");
        System.out.println(" |    | ");
        System.out.println(" | [] | ");
        System.out.println(" |____| ");
    }
}
```

**Output:**

```
   /\
  /  \
 /____\
 |    |
 | [] |
 |____|
```

#### 🔍 Why `\\` instead of `\`?

Inside a String, the backslash `\` is **special**. It's used for special characters (for example `\n` means "new line").
So, to print **one** real backslash, you must write **two**: `\\`.

| You write | Java prints |
|---|---|
| `\\` | `\` |
| `\"` | `"` (a quote inside the text) |
| `\n` | a new line |

Example:

```java
System.out.println("She said \"Hi!\"");
```

Output:

```
She said "Hi!"
```

---

## 🆕 Good to know: the short form (Java 25+)

Since **Java 25**, you can write a very small program **without** the class "envelope":

```java
void main() {
    IO.println("Hello, World!");
}
```

This is nice for tiny tests. **But** in real projects — and in **Spring Boot** — all code is inside classes, and almost all examples on the internet use the **full form**.

👉 So in this book we **always use the full form**:

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

---

## ✋ Try it yourself

**Task 1:** Write a program called `MyInfo` that prints:

```
Name: (your name)
City: (your city)
Favorite food: (your food)
```

<details>
<summary>Click to see one possible answer</summary>

```java
public class MyInfo {
    public static void main(String[] args) {
        System.out.println("Name: Ali");
        System.out.println("City: Cairo");
        System.out.println("Favorite food: Pizza");
    }
}
```

Remember: the file must be named `MyInfo.java`.

</details>

**Task 2:** Use **only `print`** (not `println`) to print `I love Java` with three separate statements: `"I "`, `"love "`, `"Java"`.

<details>
<summary>Click to see the answer</summary>

```java
public class Love {
    public static void main(String[] args) {
        System.out.print("I ");
        System.out.print("love ");
        System.out.print("Java");
    }
}
```

</details>

**Task 3:** What will this print? First **think**, then run it to check.

```java
System.out.println(10 + 5);
System.out.println("10 + 5");
System.out.println(10 * 2);
```

<details>
<summary>Click to see the answer</summary>

```
15
10 + 5
20
```

`*` means "multiply" (×) in Java.

</details>

**Task 4:** Draw a small tree 🌲 or a cat 🐱 with `println`.

**Task 5 (break it on purpose! 🔨):** Take your working `Hello` program. Make **one** of these mistakes, run it, and **read the error message**. Then fix it. Do each one separately:
- Remove the `;`
- Change `println` to `printn`
- Change `System` to `system`
- Remove the last `}`

👉 This is a great way to learn. Now you know what these errors look like, so they won't scare you later!

---

## ⚠️ Common mistakes

### Mistake 1: Forgot the `;`

```java
System.out.println("Hello, World!")     // ❌ no ; at the end
```

**Error:**
```
Hello.java:3: error: ';' expected
        System.out.println("Hello, World!")
                                           ^
1 error
```

#### 🔍 How to read the error

| Part | Meaning |
|---|---|
| `Hello.java` | In which **file** is the problem. |
| `:3` | On which **line** (line 3). |
| `error: ';' expected` | What is wrong: "I expected a `;` here." |
| `^` | The arrow points to **where** the problem is. |
| `1 error` | How many errors. |

**Fix:** Add `;` at the end.

---

### Mistake 2: Wrong big/small letters

```java
system.out.println("Hello");     // ❌ small 's'
System.out.PrintLn("Hello");     // ❌ big 'P' and 'L'
```

**Error:**
```
error: package system does not exist
```
or
```
error: cannot find symbol
  symbol:   method PrintLn(String)
```

**Why:** Java is **case-sensitive**. That means `System` and `system` are **two different words** for Java.

**Fix:** Write it exactly: `System.out.println`. Capital **S** in `System`, everything else small.

---

### Mistake 3: File name and class name are different

Your file is `hello.java` (small h), but the class is `Hello` (big H).

**Error:**
```
error: class Hello is public, should be declared in a file named Hello.java
```

**Fix:** Rename the file to **exactly** the class name + `.java`.

---

### Mistake 4: Forgot a quote `"`

```java
System.out.println("Hello, World!);     // ❌ missing " at the end
```

**Error:**
```
error: unclosed string literal
```

**Meaning:** "You started a text with `"`, but you never closed it."
**Fix:** Add the missing `"`.

---

### Mistake 5: Missing `}`

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
                                             // ❌ the last } is missing
```

**Error:**
```
error: reached end of file while parsing
```

**Meaning:** "I read the whole file, but a `{` was never closed."
**Fix:** Count your `{` and `}`. The numbers must be **equal**.

---

### Mistake 6: Using smart quotes “ ” instead of " "

If you copy code from Word or a website, sometimes the quotes become curly: `“Hello”`.

**Error:**
```
error: illegal character: '\u201c'
```

**Fix:** Delete them and type normal quotes `"` with your keyboard.

---

### Mistake 7: `java Hello.class` (with .class)

```
java Hello.class        ❌
```

**Error:**
```
Error: Could not find or load main class Hello.class
```

**Fix:** Run with the **class name only**:
```
java Hello              ✅
```

---

### Mistake 8: Wrong `main` line

```java
public static void Main(String[] args)    // ❌ capital M
public void main(String[] args)           // ❌ no static
```

**Error (when running):**
```
Error: Main method not found in class Hello, please define the main method as:
   public static void main(String[] args)
```

**Fix:** Write the door **exactly**: `public static void main(String[] args)`.
Or in IntelliJ, just type `main` + **Enter**.

---

### 💡 Golden rules for errors

1. **Read the error message.** Really read it. It usually tells you the **line** and the **problem**.
2. **Look at the first error first.** One mistake can cause many errors. Fix the first, then compile again.
3. **Look at the line before, too.** A missing `;` on line 3 sometimes shows as an error on line 4.
4. **Copy the error into Google.** Thousands of people had the same error. 😊

---

## ✅ Summary

- Every Java program needs a **class** (the envelope) and a **`main` method** (the starting door).
- The file name must be the **same as the class name** + `.java`.
- `public static void main(String[] args)` — the JVM always starts here.
- `System.out.println("...")` prints text and goes to a new line. `print` stays on the same line.
- Text (a **String**) is always in **double quotes** `" "`.
- Statements end with `;`. Blocks are inside `{ }`. Every `{` needs a `}`.
- Java is **case-sensitive**: `System` ≠ `system`.
- By hand: `javac Hello.java` (compile) → `java Hello` (run).
- In IntelliJ: click the green **▶**.
- IntelliJ shortcuts: `main` + Enter, `sout` + Enter.
- Error messages are your **friends**. Read them!

---

## ❓ Quiz

1. What must the file name be for `public class Robot`?
2. What is the starting point of every Java program?
3. What is the difference between `print` and `println`?
4. What does `System.out.println(2 + 2);` print? And `System.out.println("2 + 2");`?
5. Which command compiles `Hello.java`? Which command runs it?
6. You see `error: ';' expected`. What is the problem?
7. Is `system.out.println("Hi");` correct? Why?
8. How do you print a `"` inside a String?
9. What does `void` mean?
10. In IntelliJ, what do you type to quickly get `System.out.println();`?

<details>
<summary>Click to see the answers</summary>

1. `Robot.java`
2. The `main` method: `public static void main(String[] args)`.
3. `print` stays on the same line. `println` moves to a new line after printing.
4. `4` — and `2 + 2` (because it is text in quotes).
5. Compile: `javac Hello.java`. Run: `java Hello`.
6. A semicolon `;` is missing at the end of a statement.
7. No. `System` must start with a capital `S`. Java is case-sensitive.
8. With a backslash: `\"`. Example: `"She said \"Hi\""`.
9. The method gives **nothing back** (it returns nothing).
10. `sout` and then press Enter.

</details>

---

## 🎉 Part 1 complete!

You now have:
- ✅ Java installed
- ✅ IntelliJ installed
- ✅ Your first program running

In **Part 2**, we start learning real Java. First stop: **Variables** — boxes that keep information. 📦

---

[⬅ Previous chapter](04-install-intellij.md) | [Table of Contents](../README.md) | [Next chapter: Variables ➡](../part-02-java-basics/06-variables.md)
