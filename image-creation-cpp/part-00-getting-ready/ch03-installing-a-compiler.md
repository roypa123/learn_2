# Chapter 03 — Installing a C++ Compiler

> Part 0 — Getting Ready · Chapter 03 of 90 · about 9 pages

---

## What you will learn

- What a **compiler** is, and why C++ needs one.
- The difference between **source code** and a **program you can run**.
- How to install the free **g++** compiler on Windows, Mac or Linux.
- How to check that the compiler works.
- How to set up a way to **look at** the pictures we make.

---

## Words you need

| Word | Simple meaning |
|---|---|
| **compiler** | A program that turns your C++ code into a program the computer can run. |
| **source code** | The code you write, in a `.cpp` file. People can read it. |
| **machine code** | Instructions for the processor, as numbers. Hard for people to read. |
| **executable** | A file you can run as a program. On Windows it ends in `.exe`. |
| **compile** | To use the compiler to turn source code into an executable. |
| **g++** | A free and very popular C++ compiler. |
| **install** | To put a program on your computer so you can use it. |
| **PATH** | A list of folders where the terminal looks for commands. |
| **version** | Which edition of a program you have, like `13.2.0`. |
| **image viewer** | A program that opens a picture file and shows it on the screen. |

---

## 1. The big idea

Imagine you write a recipe in **English**. But your cook only understands **Japanese**.
You need a **translator**. The translator reads your whole English recipe, and writes a new recipe in Japanese. Now the cook can follow it.

```
  Your recipe          Translator          Recipe the cook
  (English)                                can follow
                                           (Japanese)
 ┌───────────┐       ┌───────────┐       ┌───────────┐
 │ Mix flour │  ──►  │           │  ──►  │ 小麦粉を   │
 │ and water │       │ translate │       │ 水と混ぜる │
 └───────────┘       └───────────┘       └───────────┘
```

Programming in C++ is the same:

- You write instructions in **C++**. People can read C++. This is the **source code**.
- The **processor** cannot read C++. It only understands **machine code**: long lists of numbers.
- The **compiler** is the translator. It reads your C++ and writes machine code into a new file: the **executable**.

```
   hello.cpp            g++             hello.exe
 (source code)      (compiler)        (executable)
 ┌───────────┐     ┌───────────┐     ┌───────────┐
 │ int main()│ ──► │           │ ──► │ 01001000  │ ──► the processor
 │ { ... }   │     │  compile  │     │ 11100101  │     runs it
 └───────────┘     └───────────┘     └───────────┘
  you write this                      the computer
                                      runs this
```

🧠 **Remember:** You write `.cpp` files. The compiler makes `.exe` files. You run the `.exe` file.

---

## 2. Why do we need to compile?

Some languages (like Python) use a different helper, called an **interpreter**. An interpreter reads your code **while** it runs, one line at a time. That is like a translator who stands next to the cook and translates each sentence as the cook works. It is easy, but slower.

C++ uses a **compiler**. The compiler translates **everything once, before** the program runs. Then the processor runs the machine code directly, with no translator in the middle. That is why C++ programs are **very fast**. This is good for pictures, because a picture can have millions of pixels.

| | Interpreter (like Python) | Compiler (like C++) |
|---|---|---|
| When does it translate? | While the program runs | Before the program runs |
| Speed of the program | Slower | Faster |
| Extra step for you? | No | Yes: you compile first |
| What you run | The source code file | The executable file |

### What does the compiler do inside?

You do not need to know all of this. But it is nice to know the three main steps:

1. **Preprocessing.** The compiler reads lines that start with `#`, such as `#include <iostream>`. These lines say: "copy in some tools from the standard library."
2. **Compiling.** The compiler checks your code for mistakes and translates it into machine code.
3. **Linking.** The compiler joins your machine code with the machine code of the standard library tools you used. The result is one executable file.

If there is a mistake in your code, the compiler **stops** and prints an **error message**. It tells you the file, the line number, and what is wrong. Chapter 4 shows you how to read these messages.

---

## 3. Which compiler will we use?

We will use **g++**. It is free, it works on every computer, and it follows the C++ standard closely.

| Your computer | What we install | Size of the download |
|---|---|---|
| Windows 10/11 | **MSYS2**, then g++ inside it | about 500 MB in total |
| Mac | **Xcode Command Line Tools** (has `g++`, which is really `clang++`) | about 1 GB |
| Linux (Ubuntu, Debian, Mint) | the `g++` package | about 100 MB |

💡 **Tip:** A compiler is not a "package" for our code. It is the **tool** that every C++ programmer needs. Our rule "no extra packages" means our **code** only uses the C++ standard library, and the standard library **comes with** the compiler.

Follow **only** the section for your computer.

---

## 4. Installing on Windows

We install **MSYS2**. MSYS2 is a free collection of programming tools for Windows. We use it to get g++.

### Step 1 — Download MSYS2

1. Open your web browser.
2. Go to **https://www.msys2.org**
3. Under "Installation", click the link to download the installer. The file name looks like `msys2-x86_64-2026xxxx.exe` (the numbers are the date).

### Step 2 — Run the installer

1. Open the file you downloaded (double-click it).
2. Click **Next**.
3. The installer asks for a folder. Keep the normal choice: **`C:\msys64`**. Click **Next**.
4. Click **Next** and **Install**. Wait until it finishes.
5. Keep the box "Run MSYS2 now" ticked. Click **Finish**.

A terminal window opens. Its title says **MSYS2 UCRT64** (or similar). This is a special terminal that comes with MSYS2.

### Step 3 — Update MSYS2

In the MSYS2 window, type this command and press **Enter**:

```
pacman -Syu
```

📖 **New word: pacman** — the program MSYS2 uses to install tools. (It has nothing to do with the video game, except the name.)

- It asks `Proceed with installation? [Y/n]`. Type `Y` and press **Enter**.
- The window may close by itself when it finishes. That is normal.
- If it closed: open the Start menu, type **MSYS2 UCRT64**, and open it again. Run `pacman -Syu` one more time.

### Step 4 — Install g++

In the **MSYS2 UCRT64** window, type:

```
pacman -S mingw-w64-ucrt-x86_64-gcc
```

- When it asks `Proceed with installation? [Y/n]`, type `Y` and press **Enter**.
- Wait until it finishes.

Let us understand this long name:

| Part | Meaning |
|---|---|
| `pacman -S` | "Install this." |
| `mingw-w64` | The tools are for Windows. |
| `ucrt` | They use a modern Windows system library (the "Universal C Runtime"). |
| `x86_64` | They are for 64-bit processors (almost all computers today). |
| `gcc` | The **GNU Compiler Collection**. It includes **g++**. |

### Step 5 — Let PowerShell find g++ (the PATH)

g++ is now in the folder `C:\msys64\ucrt64\bin`. But PowerShell does not know that yet.
When you type a command, the terminal looks in a list of folders called the **PATH**. We must add our folder to that list.

📖 **New word: PATH** — a list of folders. When you type a command like `g++`, the terminal searches these folders for a program called `g++`.

1. Press the **Windows key**. Type `environment`. Click **Edit the system environment variables**.
2. In the window, click the button **Environment Variables…**
3. In the top box ("User variables"), click the line **Path**. Click **Edit…**
4. Click **New**. Type exactly: `C:\msys64\ucrt64\bin`
5. Click **OK**, **OK**, and **OK** to close all three windows.
6. **Close all PowerShell windows** and **close VS Code** if it is open. They only read the PATH when they start.

### Step 6 — Check that it works

Open a **new** PowerShell window. Type:

```
g++ --version
```

You should see something like:

```
g++.exe (Rev2, Built by MSYS2 project) 14.2.0
Copyright (C) 2024 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.
```

The numbers may be different on your computer. That is fine. **If you see a version number, g++ is ready.** 🎉

⚠️ **Careful:** If you see `g++ : The term 'g++' is not recognized...`, the PATH is not right. Check:
1. Did you type `C:\msys64\ucrt64\bin` exactly, with no spaces?
2. Did you close and open PowerShell again?
3. Does the folder really exist? Type `ls C:\msys64\ucrt64\bin\g++.exe`. If it says "cannot find path", Step 4 did not finish. Do Step 4 again.

---

## 5. Installing on Mac

1. Open the **Terminal** (Command + Space, type `Terminal`, Enter).
2. Type this command and press **Enter**:

```
xcode-select --install
```

3. A window appears and asks if you want to install the command line developer tools. Click **Install**. Then **Agree**.
4. Wait until it finishes. It can take 10 to 30 minutes.
5. Check it. Type:

```
g++ --version
```

You should see something like `Apple clang version 16.0.0`. On a Mac, the command `g++` really runs a compiler called **clang++**. It understands the same C++, so everything in this book works. 🎉

💡 **Tip:** If it says the tools are "already installed", that is good. You can go to step 5.

---

## 6. Installing on Linux

For Ubuntu, Debian, Linux Mint and similar systems:

1. Open the **Terminal** (Ctrl + Alt + T).
2. Type:

```
sudo apt update
sudo apt install g++
```

3. Type your password when it asks. (You will not see the letters while you type. That is normal, for safety.)
4. Type `Y` if it asks to continue.
5. Check it:

```
g++ --version
```

You should see something like `g++ (Ubuntu 13.2.0-23ubuntu4) 13.2.0`. 🎉

📖 **New word: sudo** — "do this as the boss of the computer". Installing programs needs permission, so we put `sudo` in front.

For Fedora, use `sudo dnf install gcc-c++` instead.

---

## 7. How will we see our pictures?

Our programs will write image **files**. To look at them, we need an **image viewer**. This is only for **looking**; our code does not use it.

We will write two kinds of image files in this book:

| File type | First chapter | Can the normal viewer open it? |
|---|---|---|
| `.ppm` | Chapter 23 | Mac: ✅ Preview. Linux: ✅ most viewers. Windows: ❌ the Photos app cannot. |
| `.bmp` | Chapter 28 | ✅ On every computer, with the normal viewer. |

So on **Mac** and **Linux**, you are ready.

On **Windows**, the normal Photos app cannot open `.ppm` files. You have three choices:

1. **Wait until Chapter 28.** From Chapter 28 on, we save `.bmp` files. They open with a double-click in Windows Photos. Until then, you can also open the text kind of `.ppm` file in a text editor and read the numbers.
2. **Install a free image viewer that knows PPM**, for example **IrfanView** (irfanview.com) or **GIMP** (gimp.org). This is only for looking at pictures. It does not change our code.
3. **Use VS Code.** Some free VS Code extensions can show PPM pictures. Search for "PPM" in the VS Code Extensions panel.

💡 **Tip:** Choice 1 is enough to learn everything. Choice 2 is nice because you can zoom in and see each pixel.

---

## 8. Small examples

### Example 03.1 — Check the compiler version

**Goal:** Make sure g++ is installed.

**Command:**

```
g++ --version
```

**Explanation:** `--version` is an **option**. Options start with `-` or `--`. They change what a command does. This option says: "do not compile anything; just tell me your version."

**Result:** A line with a version number, like `14.2.0`.

📖 **New word: option** (also **flag**) — extra words after a command that change what it does. They usually start with `-` or `--`.

### Example 03.2 — Find where g++ lives

**Goal:** See which folder the terminal found g++ in.

**Command (Windows PowerShell):**

```
where.exe g++
```

**Command (Mac/Linux):**

```
which g++
```

**Explanation:** These commands search the PATH (section 4, step 5) for `g++`, and print where it is.

**Result (Windows):** `C:\msys64\ucrt64\bin\g++.exe`. **(Mac):** `/usr/bin/g++`. **(Linux):** `/usr/bin/g++`.

### Example 03.3 — Run g++ with nothing to do

**Goal:** See what happens when you forget to give g++ a file.

**Command:**

```
g++
```

**Explanation:** We did not tell g++ which file to compile.

**Result:**

```
g++: fatal error: no input files
compilation terminated.
```

"Fatal error" sounds scary, but it only means "I cannot continue". "No input files" means "you did not give me a `.cpp` file." Nothing is broken.

### Example 03.4 — Ask g++ for help

**Goal:** See the list of options g++ understands.

**Command:**

```
g++ --help
```

**Result:** A long list of options. You do not need to read it all. In this book we only use a few options, shown in the next example.

### Example 03.5 — The options we will use in this book

**Goal:** Learn the compile command we will type many times.

**The command (you will use it from Chapter 4):**

```
g++ -std=c++17 -Wall -O2 hello.cpp -o hello.exe
```

**Explanation, part by part:**

| Part | Meaning |
|---|---|
| `g++` | Run the compiler. |
| `-std=c++17` | Use the 2017 version of the C++ rules ("C++17"). Everything in this book uses C++17. |
| `-Wall` | "**W**arnings: **all**". Tell me about code that is allowed but probably a mistake. Very helpful for beginners! |
| `-O2` | "**O**ptimize, level **2**". Make the program faster. (This is the capital letter O, not the number zero.) Our picture programs will run much faster. |
| `hello.cpp` | The source code file to compile. |
| `-o hello.exe` | "**O**utput": name the new executable `hello.exe`. (A small letter o.) |

**Result:** If the code has no mistakes, a new file `hello.exe` appears in the folder. We try it in Chapter 4.

💡 **Tip:** On Mac and Linux you can name the output `hello` instead of `hello.exe`. The `.exe` ending is a Windows custom. But `hello.exe` also works on Mac and Linux, so you can use the same commands as Windows readers.

### Example 03.6 — Make the folder for the next chapter

**Goal:** Get ready for Chapter 4.

**Commands (Windows):**

```
cd C:\pictures-code
mkdir ch04
cd ch04
```

**(Mac/Linux):** `cd ~/pictures-code`, then `mkdir ch04`, then `cd ch04`.

**Result:** You are in an empty folder `ch04`, ready for your first program.

---

## 9. Common mistakes

⚠️ **Typing commands in the wrong window (Windows).** The `pacman` commands go in the **MSYS2 UCRT64** window. The `g++` commands (from Chapter 4 on) go in **PowerShell** (or the VS Code terminal). Both work for `g++` once the PATH is set.

⚠️ **Not closing the terminal after changing the PATH.** The terminal reads the PATH only when it opens. Close it and open a new one.

⚠️ **Installing the wrong gcc package (Windows).** If you install just `gcc` (without the long name), you get a version for the MSYS2 system itself, not for normal Windows programs. Use `mingw-w64-ucrt-x86_64-gcc`.

⚠️ **Mixing up `-O2` and `-o`.** Capital `-O2` means "make it fast". Small `-o` means "name of the output file". They are different.

⚠️ **Writing `-std=c++17` with spaces.** It must be one word with no spaces: `-std=c++17`.

---

## 10. Try it yourself

🏋️ **Practice 1.** Run `g++ --version`. Write down the version number you see.

🏋️ **Practice 2.** In your own words: what is the difference between `hello.cpp` and `hello.exe`?

🏋️ **Practice 3.** In the command `g++ -std=c++17 -Wall -O2 sky.cpp -o sky.exe`:
(a) Which file is the source code?
(b) Which file will the compiler make?
(c) Which part asks for warnings?

🏋️ **Practice 4.** Why is a C++ program usually faster than a program that uses an interpreter?

🏋️ **Practice 5.** You type `g++ --version` and see "not recognized". Write two things you should check.

---

## 11. Answers

**Answer 1.** Your own number, for example `14.2.0` (Windows), `16.0.0` (Mac), or `13.2.0` (Linux). Any number means it works.

**Answer 2.** `hello.cpp` is the **source code**: text that you write and people can read. `hello.exe` is the **executable**: machine code made by the compiler, which the computer can run.

**Answer 3.** (a) `sky.cpp` (b) `sky.exe` (c) `-Wall`

**Answer 4.** The compiler translates the whole program into machine code **before** it runs. So when it runs, the processor follows machine code directly, without a translator working at the same time.

**Answer 5.** (1) Is the folder `C:\msys64\ucrt64\bin` in the PATH, spelled exactly? (2) Did you close and open the terminal again after you changed the PATH? Also: (3) Did the install in Step 4 finish? Check that `C:\msys64\ucrt64\bin\g++.exe` exists.

---

## Summary

🧠 A **compiler** translates your C++ **source code** (`.cpp`) into an **executable** (`.exe`).

🧠 C++ is fast because it is compiled **before** it runs.

🧠 We use the free compiler **g++**. Windows: MSYS2. Mac: Xcode Command Line Tools. Linux: `apt install g++`.

🧠 `g++ --version` checks that the compiler is ready.

🧠 Our compile command is: `g++ -std=c++17 -Wall -O2 file.cpp -o file.exe`

🧠 To **see** pictures: `.ppm` files open on Mac and Linux. On Windows, wait for `.bmp` files (Chapter 28) or use a free viewer.

---

## What comes next

Everything is ready. Now we write, compile and run our very first C++ program, and we look at every single line of it.

➡️ Next: [Chapter 04 — Your First C++ Program](ch04-your-first-program.md)
