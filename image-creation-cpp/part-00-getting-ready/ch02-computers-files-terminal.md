# Chapter 02 — Computers, Files, Folders and the Terminal

> Part 0 — Getting Ready · Chapter 02 of 90 · about 9 pages

---

## What you will learn

- The three main parts of a computer: the **processor**, the **memory**, and the **storage**.
- What a **file** is, and what the **file extension** (like `.cpp` or `.bmp`) tells you.
- What a **folder** and a **path** are.
- How to open the **terminal** and type commands.
- Six commands you will use all the time: `pwd`, `ls`, `cd`, `mkdir`, `cat`, `clear`.
- How to make the folder where all your picture programs will live.

---

## Words you need

| Word | Simple meaning |
|---|---|
| **processor (CPU)** | The "brain" of the computer. It follows instructions very fast. |
| **memory (RAM)** | The computer's short-time memory. Fast, but forgets everything when the power goes off. |
| **storage (disk)** | The computer's long-time memory. Slower, but keeps files when the power is off. |
| **file** | A named piece of information kept in storage. |
| **file extension** | The last part of a file name, after the dot. `photo.bmp` has the extension `.bmp`. |
| **folder** (also **directory**) | A container for files and other folders. |
| **path** | The "address" of a file or folder. It tells you how to find it. |
| **terminal** | A window where you type commands to the computer, using words instead of the mouse. |
| **command** | One instruction that you type in the terminal. |
| **text editor** | A program for writing plain text, such as code. |

---

## 1. The big idea

Think about a **kitchen**.

- The **cook** does the work: cuts, mixes, cooks. → This is the **processor**.
- The **table** is where the cook puts the things they are using right now. It is close and quick to reach, but small. When the kitchen closes, the table is cleaned. → This is the **memory**.
- The **cupboard** keeps food for a long time. It is bigger, but it takes longer to get things from it. → This is the **storage**.
- A **recipe** tells the cook what to do, step by step. → This is a **program**.

```
   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
   │   STORAGE    │     │    MEMORY    │     │  PROCESSOR   │
   │  (cupboard)  │ ──► │   (table)    │ ──► │    (cook)    │
   │ keeps files  │     │ holds what   │     │ does the     │
   │ for a long   │ ◄── │ we use now   │ ◄── │ work         │
   │ time         │     │              │     │              │
   └──────────────┘     └──────────────┘     └──────────────┘
```

When our picture program runs, this is what happens:

1. The program is loaded from **storage** into **memory**.
2. The **processor** follows the program. It works out the colour of every pixel.
3. The colours are kept in **memory** while the program works.
4. At the end, the program writes the colours into an image **file** in **storage**.
5. Now the picture is saved. You can open it any time, even after you turn the computer off.

🧠 **Remember:** Memory is fast but forgets. Storage is slow but remembers. Our program makes the picture in memory, then saves it to storage as a file.

---

## 2. Files

A **file** is a named piece of information in storage.
A photo is a file. A song is a file. A letter you wrote is a file. A program is a file.

Inside, **every file is just a long list of numbers**. Each number is between 0 and 255. (Chapter 20 explains why.)
The numbers mean different things in different kinds of files.
In a photo file, the numbers are colours. In a text file, each number stands for a letter.

### File names and extensions

Most file names have two parts, separated by a dot:

```
     red_square . bmp
     └───┬────┘   └┬┘
       name    extension
```

The **extension** tells you (and the computer) **what kind of file** it is.
Here are the extensions you will see in this book:

| Extension | What kind of file | Example |
|---|---|---|
| `.cpp` | C++ code that **you** write | `hello.cpp` |
| `.h` | A C++ "header" file (Chapter 16) | `image.h` |
| `.exe` | A program you can run (on Windows) | `hello.exe` |
| `.txt` | Plain text | `notes.txt` |
| `.ppm` | A simple image file (Chapter 23) | `sunset.ppm` |
| `.bmp` | A Windows "bitmap" image file (Chapter 27) | `sunset.bmp` |

⚠️ **Careful (Windows):** Windows often **hides** extensions. You may see `hello` when the real name is `hello.cpp`. Please make extensions visible:

1. Open **File Explorer** (the yellow folder icon).
2. Click **View** at the top.
3. On Windows 11: click **Show → File name extensions**. On Windows 10: tick the box **File name extensions**.

Now you will see the full names, like `hello.cpp`. This helps a lot.

### Plain text files

Code files (`.cpp`) are **plain text**. That means they hold only letters, numbers and symbols. No bold, no colours, no pictures.

⚠️ **Careful:** Do **not** write code in Microsoft Word or a similar program. Word adds hidden information to the file (fonts, sizes, styles). The C++ compiler cannot understand it. Use a **text editor** (see section 6).

---

## 3. Folders and paths

A **folder** is a container. It can hold files and other folders.
Folders inside folders make a **tree**:

```
C:\                         ← the top of the disk (called the "root")
├── Users\
│   └── Sam\
│       ├── Documents\
│       └── Pictures\
└── pictures-code\          ← we will make this folder
    ├── ch04\
    │   ├── hello.cpp
    │   └── hello.exe
    └── ch24\
        ├── red_image.cpp
        └── red_image.ppm
```

📖 **New word: directory** — another word for folder. Programmers often say "directory".

### Paths

A **path** is the address of a file. It lists the folders you walk through to reach it.

On **Windows**, the parts are separated with a backslash `\`:

```
C:\pictures-code\ch04\hello.cpp
│  │             │    │
│  │             │    └─ the file
│  │             └─ the folder "ch04"
│  └─ the folder "pictures-code"
└─ the disk "C:"
```

On **Mac and Linux**, the parts are separated with a forward slash `/`:

```
/home/sam/pictures-code/ch04/hello.cpp
```

💡 **Tip:** Windows PowerShell also understands `/`. So `C:/pictures-code/ch04` works too.

### Full paths and short paths

- A **full path** starts from the top of the disk: `C:\pictures-code\ch04\hello.cpp`.
- A **short path** (programmers say **relative path**) starts from the folder you are in now. If you are already in `C:\pictures-code`, then the short path `ch04\hello.cpp` points to the same file.

Two special short names:

| Name | Meaning |
|---|---|
| `.` (one dot) | "This folder, the one I am in now." |
| `..` (two dots) | "The folder one step **up**", the folder that holds this one. |

⚠️ **Careful:** Spaces in folder names make life harder in the terminal. Use names like `pictures-code` or `pictures_code`, **not** `my pictures code`.

---

## 4. The terminal

You usually use a computer with the **mouse**: you click on icons.
The **terminal** is another way. You **type** commands with the keyboard.

📖 **New word: terminal** — a window where you type commands. Other names for it: **command line**, **console**, **shell**, **PowerShell** (on Windows).

Why use the terminal? Because the C++ compiler is a **command**. We run it by typing in the terminal. Also, the terminal shows us the text our programs print.

### How to open the terminal

| Computer | How to open it |
|---|---|
| **Windows 10/11** | Press the **Windows key**, type `PowerShell`, press **Enter**. (Or: right-click the Start button → **Terminal**.) |
| **Mac** | Press **Command + Space**, type `Terminal`, press **Enter**. |
| **Linux** | Press **Ctrl + Alt + T** (on most Linux systems). |

You will see a window with some text and a blinking line. It looks something like this:

```
PS C:\Users\Sam>
```

This text is called the **prompt**. It means: "I am ready. Type a command."
The prompt shows **which folder you are in now**. Here it is `C:\Users\Sam`.

📖 **New word: prompt** — the text the terminal shows when it waits for your command.

On Mac or Linux the prompt may look like `sam@laptop ~ %` or `sam@pc:~$`. The `~` sign means "my home folder".

### How to type a command

1. Click inside the terminal window.
2. Type the command.
3. Press **Enter**.
4. The computer does the command and maybe prints an answer.
5. A new prompt appears. You can type the next command.

---

## 5. Six commands you will use all the time

Good news: these six commands work in **Windows PowerShell**, on **Mac**, and on **Linux**.

### Command 1: `pwd` — "Where am I?"

`pwd` means **p**rint **w**orking **d**irectory. It shows the folder you are in now.

```
PS C:\Users\Sam> pwd

Path
----
C:\Users\Sam
```

### Command 2: `ls` — "What is in this folder?"

`ls` means **l**i**s**t. It shows the files and folders in the folder you are in.

```
PS C:\Users\Sam> ls

    Directory: C:\Users\Sam

Mode          LastWriteTime   Length Name
----          -------------   ------ ----
d-----     10/17/2026  9:00          Documents
d-----     10/17/2026  9:00          Pictures
```

A `d` at the start means it is a **directory** (folder).

### Command 3: `cd` — "Go to another folder."

`cd` means **c**hange **d**irectory. You type `cd`, a space, and the folder name.

```
PS C:\Users\Sam> cd Documents
PS C:\Users\Sam\Documents>
```

Look at the prompt. It changed! Now you are in `Documents`.

To go **up** one folder, use `..`:

```
PS C:\Users\Sam\Documents> cd ..
PS C:\Users\Sam>
```

To go to a full path, type the full path:

```
PS C:\Users\Sam> cd C:\
PS C:\>
```

### Command 4: `mkdir` — "Make a new folder."

`mkdir` means **m**a**k**e **dir**ectory.

```
PS C:\> mkdir pictures-code
```

Now there is a new, empty folder called `pictures-code`.

### Command 5: `cat` — "Show me what is inside this text file."

`cat` prints the text inside a file. (The name comes from "con**cat**enate", which means "join together", but we use it just to look at a file.)

```
PS C:\pictures-code> cat notes.txt
Today I learned about the terminal.
```

⚠️ **Careful:** Only use `cat` on text files (like `.cpp`, `.txt`, or the text kind of `.ppm`). On other files, such as `.exe` or `.bmp`, it prints strange symbols, because those files are not text.

### Command 6: `clear` — "Clean the screen."

`clear` removes all the old text from the terminal window. Your files are **not** changed. It only cleans the window.

### Summary table

| Command | Meaning | Example |
|---|---|---|
| `pwd` | Where am I? | `pwd` |
| `ls` | What is here? | `ls` |
| `cd folder` | Go into a folder | `cd ch04` |
| `cd ..` | Go up one folder | `cd ..` |
| `mkdir name` | Make a new folder | `mkdir ch04` |
| `cat file` | Show a text file | `cat hello.cpp` |
| `clear` | Clean the window | `clear` |

### Two keys that save time

1. **Tab key (⇥) — finish the name for me.** Type the first few letters of a folder or file name, then press **Tab**. The terminal finishes the name for you. Example: type `cd Doc` and press Tab → it becomes `cd .\Documents\`.
2. **Up arrow (↑) — show my last command again.** Press ↑ to see the command you typed before. Press ↑ again to go further back. Press Enter to run it again. This is very useful: we will compile and run the same program many times.

---

## 6. A text editor for writing code

You need a program to **write** your `.cpp` files. This is a **text editor**.

| Editor | Good for | Cost |
|---|---|---|
| **Visual Studio Code** (VS Code) | Best choice. Colours the code to make it easy to read. Has a terminal inside it. | Free |
| **Notepad** (Windows) | Simple. Already on every Windows computer. | Free |
| **TextEdit** (Mac) | Simple. Use **Format → Make Plain Text** first! | Free |
| **gedit**, **Kate** (Linux) | Simple. | Free |

💡 **Tip:** VS Code is a text editor, not a code library. It does not add anything to your program. Our rule "no extra packages" is still true. You can use any editor you like — even Notepad.

⚠️ **Careful (Notepad):** When you save, Notepad may add `.txt` to the end, so `hello.cpp` becomes `hello.cpp.txt`. To stop this: in the **Save as** window, set **Save as type** to **All files (\*.\*)**, then type the name `hello.cpp`.

### The terminal inside VS Code

In VS Code, click the menu **Terminal → New Terminal**. A terminal opens at the bottom of the window. It is the same terminal (PowerShell on Windows). Now you can write code at the top and run commands at the bottom, in one window.

---

## 7. Making your work folder

Let us make the folder for **all** the programs in this book. Follow these steps exactly.

**On Windows (PowerShell):**

```
cd C:\
mkdir pictures-code
cd pictures-code
pwd
```

The last command should print `C:\pictures-code`.

**On Mac or Linux:**

```
cd ~
mkdir pictures-code
cd pictures-code
pwd
```

The last command prints something like `/Users/sam/pictures-code` or `/home/sam/pictures-code`.

From now on, for each chapter with code, we make a small folder inside `pictures-code`, like `ch04`, `ch24`, and so on. This keeps things tidy.

---

## 8. Small examples

All these examples are typed in the terminal. Try each one.

### Example 02.1 — Where am I?

**Goal:** See which folder you are in.

**Command:**

```
pwd
```

**Explanation:** `pwd` prints the full path of the folder you are in now. When you first open the terminal, you are usually in your **home folder** (for example `C:\Users\Sam`).

**Result:** You see a path like `C:\Users\Sam`.

### Example 02.2 — Make a folder and go inside

**Goal:** Make a folder for Chapter 4 and go into it.

**Commands:**

```
cd C:\pictures-code
mkdir ch04
cd ch04
pwd
```

**Explanation:**
- Line 1 goes to the `pictures-code` folder (use `cd ~/pictures-code` on Mac or Linux).
- Line 2 makes a new folder `ch04` inside it.
- Line 3 goes into the new folder.
- Line 4 shows where you are.

**Result:** `pwd` prints `C:\pictures-code\ch04`.

### Example 02.3 — Go up and look around

**Goal:** Use `..` and `ls`.

**Commands:**

```
cd ..
ls
```

**Explanation:** `cd ..` goes up one step, from `ch04` back to `pictures-code`. `ls` lists what is inside `pictures-code`.

**Result:** You see the folder `ch04` in the list.

### Example 02.4 — Make a text file and look inside it

**Goal:** Make a small text file and read it with `cat`.

**Steps:**
1. Open your text editor.
2. Type: `I am learning to make pictures.`
3. Save it in `C:\pictures-code` with the name `notes.txt`.
4. In the terminal, type:

```
cd C:\pictures-code
cat notes.txt
```

**Explanation:** `cat` opens the file and prints its text into the terminal.

**Result:**

```
I am learning to make pictures.
```

### Example 02.5 — Use Tab to finish a name

**Goal:** Let the terminal type for you.

**Steps:** Go to `C:\pictures-code`. Type `cat no` and press **Tab**.

**Explanation:** The terminal looks for a file whose name starts with `no`. It finds `notes.txt` and finishes the name.

**Result:** The command becomes `cat .\notes.txt` (on Windows) or `cat notes.txt` (on Mac/Linux). Press Enter to run it.

### Example 02.6 — Use the up arrow

**Goal:** Run a command again without typing it.

**Steps:** Press the **↑** key once. Then press **Enter**.

**Explanation:** The ↑ key brings back the last command (`cat notes.txt`). Enter runs it again.

**Result:** The text of `notes.txt` is printed again. Later, you will use this trick to compile and run your programs again and again.

### Example 02.7 — What happens with a wrong name?

**Goal:** See an error message, so you are not afraid of it later.

**Command:**

```
cd folder-that-does-not-exist
```

**Explanation:** There is no folder with this name. The terminal cannot go there.

**Result:** You see a red error message, something like `Cannot find path ... because it does not exist.` Nothing bad happened. The terminal just tells you it could not do it. Read error messages calmly: they usually tell you exactly what is wrong.

---

## 9. Common mistakes

⚠️ **Forgetting the space after `cd`.** `cdDocuments` is wrong. `cd Documents` is right.

⚠️ **Spelling mistakes in names.** `cd Documnets` does not work. Use the **Tab** key to avoid this.

⚠️ **Being in the wrong folder.** Many problems happen because you are not in the folder you think. Type `pwd` to check, and `ls` to see the files.

⚠️ **Hidden extensions on Windows.** Your file might be called `hello.cpp.txt`. Turn on "File name extensions" in File Explorer (section 2).

⚠️ **Spaces in folder names.** If you must use a folder with a space, put the path in quotes: `cd "my folder"`.

⚠️ **Writing code in Word.** Always use a plain text editor.

---

## 10. Try it yourself

🏋️ **Practice 1.** Open the terminal. Type `pwd`. Write down the folder you are in.

🏋️ **Practice 2.** In `pictures-code`, make three folders: `test1`, `test2`, `test3`. Use `ls` to check they exist.

🏋️ **Practice 3.** Go into `test2`. Then, with **one** command, go back up to `pictures-code`. Which command did you use?

🏋️ **Practice 4.** What is the extension of each file? (a) `circle.cpp` (b) `circle.exe` (c) `sky.bmp` (d) `my.notes.txt`

🏋️ **Practice 5.** You are in `C:\pictures-code\ch04`. What is the full path of the folder `..`?

🏋️ **Practice 6.** Write the full path of a file called `star.bmp` that is in the folder `ch59`, which is inside `C:\pictures-code`.

---

## 11. Answers

**Answer 1.** It depends on your computer. Usually it is your home folder, like `C:\Users\YourName` on Windows, or `/Users/yourname` on Mac.

**Answer 2.**

```
cd C:\pictures-code
mkdir test1
mkdir test2
mkdir test3
ls
```

You see `test1`, `test2` and `test3` in the list.

**Answer 3.** First `cd test2`. Then `cd ..` takes you up one step, back to `pictures-code`.

**Answer 4.** (a) `.cpp` (b) `.exe` (c) `.bmp` (d) `.txt` — only the part after the **last** dot is the extension.

**Answer 5.** `..` means "one step up". One step up from `C:\pictures-code\ch04` is `C:\pictures-code`.

**Answer 6.** `C:\pictures-code\ch59\star.bmp`

---

## Summary

🧠 A computer has a **processor** (does the work), **memory** (fast, forgets) and **storage** (slow, remembers).

🧠 A **file** is a named list of numbers in storage. The **extension** tells you what kind of file it is.

🧠 **Folders** hold files and other folders. A **path** is the address of a file.

🧠 The **terminal** lets you type commands. You will use `pwd`, `ls`, `cd`, `mkdir`, `cat` and `clear`.

🧠 Write code in a **plain text editor** (VS Code is best). Never in Word.

🧠 All your programs go in the folder `pictures-code`, one small folder for each chapter.

---

## What comes next

Now you can move around your computer with the terminal. Next, we install the **C++ compiler**: the tool that turns your code into a program the computer can run.

➡️ Next: [Chapter 03 — Installing a C++ Compiler](ch03-installing-a-compiler.md)
