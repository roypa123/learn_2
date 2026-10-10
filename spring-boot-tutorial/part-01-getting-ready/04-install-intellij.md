# Chapter 4 – Install a Code Editor (IntelliJ IDEA)

[⬅ Previous chapter](03-install-java.md) | [Table of Contents](../README.md) | [Next chapter ➡](05-hello-world.md)

---

## 🎯 Goal

At the end of this chapter:

- **IntelliJ IDEA** is installed on your computer.
- You know the **main parts** of the IntelliJ window.
- You created your **first empty Java project**.

⏱️ Time needed: about 20–30 minutes.

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Editor** | A program for writing text. A **code editor** is made for writing code. |
| **IDE** | *Integrated Development Environment.* A "super editor": it writes, checks, builds and runs your code — all in one place. |
| **IntelliJ IDEA** | A very popular IDE for Java. We just call it **IntelliJ**. |
| **Project** | A folder with all the files of one program. |
| **SDK** | *Software Development Kit.* For Java, the SDK is the **JDK**. IntelliJ uses this word. |
| **Syntax highlighting** | The editor shows different parts of code in **different colors**, so it is easier to read. |
| **Auto-complete** | You type a few letters, and the editor **suggests** the rest. |

---

## 📖 Story: Notepad vs. a smart kitchen

You can write Java code in **Notepad**. It works. But it is like cooking with **only a knife and a fire**. 🔪🔥

An **IDE** is like a **modern kitchen**: 🍳
- An oven with a timer (it **runs** your code with one click)
- A scale that warns you "too much salt!" (it **shows mistakes** in red while you type)
- A recipe book that opens by itself (it **suggests** code)
- Labels on every jar (it **colors** your code)

You *can* cook without it. But why make life hard? 😊

> 💡 In Chapter 5 we will write our first program **one time in Notepad**, so you understand what happens "under the hood". After that, we always use IntelliJ.

---

## 💾 Part 1: Download IntelliJ IDEA

1. Open your web browser.
2. Go to:

   ```
   https://www.jetbrains.com/idea/download/
   ```

3. Make sure **Windows** is selected at the top.
4. Download the **free** version.

> 💡 **Which version is free?**
> JetBrains (the company that makes IntelliJ) sometimes changes how the download page looks.
> - If you see **two** downloads — **Ultimate** and **Community Edition** — choose **Community Edition**. It is free forever and has everything we need for Java.
> - If you see **one** download — just download **IntelliJ IDEA**. The basic features are free. If it asks you about a paid trial or subscription, you can skip it and keep using the free features.

5. Wait until the `.exe` file is downloaded.

> 💡 **Mac users:** choose **macOS**, and choose **Apple Silicon** (M1/M2/M3/M4) or **Intel**. You get a `.dmg` file. Open it and drag IntelliJ into the **Applications** folder.

---

## 🛠️ Part 2: Install IntelliJ on Windows

1. Open your **Downloads** folder.
2. Double-click the file (its name looks like `ideaIC-....exe` or `idea-....exe`).
3. Windows asks *"Do you want to allow this app to make changes?"* → click **Yes**.
4. Click **Next**.
5. **Choose the install folder** → keep the normal folder → click **Next**.
6. **Installation Options** — you will see some checkboxes. We suggest:

   | Option | Check it? | Why |
   |---|---|---|
   | Create Desktop Shortcut | ✅ Yes | An icon on your desktop to open IntelliJ quickly. |
   | Add "Open Folder as Project" | ✅ Yes | You can right-click a folder and open it in IntelliJ. |
   | Add "bin" folder to the PATH | ✅ Yes | You can start IntelliJ from the terminal. |
   | Create Associations `.java` | ✅ Yes | Double-clicking a `.java` file opens IntelliJ. |

7. Click **Next**, then **Install**.
8. Wait. At the end it may ask to **reboot** (restart) the computer. Choose **Reboot now** or **later** — both are OK, but restart before you start working.
9. Click **Finish**. 🎉

---

## 🚪 Part 3: Open IntelliJ for the first time

1. Double-click the **IntelliJ IDEA** icon on your desktop.
2. It may ask you to **accept the user agreement**. Read it, check the box, and click **Continue**.
3. It may ask about **sending usage data**. Choose what you like ("Don't Send" is fine).
4. It may ask about **importing settings**. Choose **"Do not import settings"** (this is your first time).

Now you see the **Welcome screen**:

```
 ┌───────────────────────────────────────────────────────┐
 │  IntelliJ IDEA                                        │
 │                                                       │
 │   Projects        ┌─────────────┐ ┌──────┐ ┌───────┐ │
 │   Customize       │ New Project │ │ Open │ │ Clone │ │
 │   Plugins         └─────────────┘ └──────┘ └───────┘ │
 │   Learn                                               │
 │                                                       │
 └───────────────────────────────────────────────────────┘
```

| Button | Meaning |
|---|---|
| **New Project** | Create a new, empty project. |
| **Open** | Open a project folder that already exists. |
| **Clone Repository** | Download a project from the internet (with Git — Chapter 42). |
| **Customize** (left) | Change colors, font size, and more. |
| **Plugins** (left) | Add extra features. |

### 💡 Tip: Make the text bigger

If the text is too small for your eyes:
1. Click **Customize** on the left.
2. Find **IDE font** and choose a bigger number, like **16**.
3. You can also choose a **Color theme**: **Dark** or **Light**. Choose what is comfortable for your eyes. 👀

---

## 📁 Part 4: Create your first project

1. Click **New Project**.
2. You see a window with settings. Fill it like this:

```
 ┌────────────────────────────────────────────────────┐
 │ New Project                                        │
 │                                                    │
 │ Name:       my-first-java                          │
 │ Location:   C:\Users\YourName\IdeaProjects         │
 │                                                    │
 │ Language:   [Java]  Kotlin  Groovy                 │
 │ Build system: [IntelliJ]  Maven  Gradle            │
 │ JDK:        25  Eclipse Temurin                    │
 │                                                    │
 │ [✓] Add sample code                                │
 │                                                    │
 │                             [ Create ]             │
 └────────────────────────────────────────────────────┘
```

### 🔍 Every setting explained

| Setting | What to choose | What it means |
|---|---|---|
| **Name** | `my-first-java` | The name of your project. It is also the name of the folder. Use small letters and `-` instead of spaces. |
| **Location** | (keep it) | **Where** on your computer the project folder will be saved. |
| **Language** | **Java** | The programming language. |
| **Build system** | **IntelliJ** | Who "builds" the project. For now, IntelliJ itself — the simplest choice. Later (Chapter 40) we will use **Maven**. |
| **JDK** | **25 Eclipse Temurin** (or your version) | Which Java toolbox to use. IntelliJ usually **finds it automatically** (from Chapter 3). |
| **Add sample code** | ✅ Checked | IntelliJ writes a small example program for you. |

3. Click **Create**.

> ⚠️ **The JDK box is empty or says "No SDK"?**
> Click on the JDK box → choose **Add JDK...** (or **Add JDK from disk**) → find the folder where you installed Java in Chapter 3, for example
> `C:\Program Files\Eclipse Adoptium\jdk-25...`
> → click **OK**.
>
> You can also choose **Download JDK...** and let IntelliJ download one for you.

---

## 🖥️ Part 5: A tour of the IntelliJ window

After a few seconds your project opens. The window has **four main areas**:

```
 ┌──────────────────────────────────────────────────────────────┐
 │  Menu  ·  Toolbar                           ▶ Run   🐞 Debug │ ← (1)
 ├───────────────┬──────────────────────────────────────────────┤
 │ my-first-java │  Main.java                                   │
 │  ├─ .idea     │                                              │
 │  ├─ src       │   public class Main {                        │
 │  │  └─ Main   │       public static void main(String[] a) {  │
 │  └─ ...       │           System.out.println("Hello...");    │
 │               │       }                                      │
 │      (2)      │   }                       (3)                │
 ├───────────────┴──────────────────────────────────────────────┤
 │  Run:  Hello and welcome!                       (4)          │
 └──────────────────────────────────────────────────────────────┘
```

| Number | Name | What it does |
|---|---|---|
| **(1)** | **Toolbar** | Buttons at the top. The green **▶ Run** button starts your program. |
| **(2)** | **Project window** | Shows all the folders and files in your project. Like File Explorer. |
| **(3)** | **Editor** | The big area where you **write code**. |
| **(4)** | **Run window** | Appears at the bottom when you run a program. Shows the **output** (what your program prints). |

### 🔍 The folders in the Project window

| Folder / file | What it is |
|---|---|
| `my-first-java` | The main folder of your project. |
| `.idea` | IntelliJ's own settings for this project. **Don't touch it.** |
| `src` | Short for **source**. **Your code goes here.** Always. |
| `Main` (inside `src`) | The sample Java file IntelliJ made. Its full name is `Main.java`. |
| `my-first-java.iml` | Another IntelliJ settings file. **Don't touch it.** |

---

## ▶️ Part 6: Run the sample code

1. In the **Project window**, double-click **Main** inside `src`. The code opens in the editor.
2. Find the green **▶** triangle. You can click:
   - the **▶ Run** button at the top of the window, **or**
   - the small green **▶** next to the line `public class Main` (on the left side, near the line numbers).
3. If a small menu appears, choose **Run 'Main.main()'**.
4. Wait a few seconds. The **Run window** opens at the bottom.

You will see something like:

```
Hello and welcome!
i = 1
i = 2
i = 3
i = 4
i = 5

Process finished with exit code 0
```

(The sample code can be a little different in different IntelliJ versions. That's OK.)

### 🔍 What does the output mean?

| Line | Meaning |
|---|---|
| `Hello and welcome!` and `i = 1` ... | The text the program **printed**. You will understand this code soon. |
| `Process finished with exit code 0` | The program **ended**. `exit code 0` means "**everything was OK**". ✅ Any other number usually means an **error**. |

🎉 **Congratulations! You just ran a Java program!**

---

## ⌨️ Useful keyboard shortcuts

You don't need to remember these now. Come back to this table when you need it.

| Shortcut (Windows) | Shortcut (Mac) | What it does |
|---|---|---|
| `Shift + F10` | `Ctrl + R` | Run the program again |
| `Ctrl + S` | `Cmd + S` | Save (IntelliJ also saves automatically) |
| `Ctrl + Z` | `Cmd + Z` | Undo (go back one step) |
| `Ctrl + Shift + Z` | `Cmd + Shift + Z` | Redo |
| `Ctrl + Space` | `Ctrl + Space` | Show suggestions (auto-complete) |
| `Ctrl + Alt + L` | `Cmd + Option + L` | Make the code tidy (format code) |
| `Ctrl + /` | `Cmd + /` | Turn a line into a comment (or back) |
| `Shift` `Shift` (press 2 times fast) | `Shift` `Shift` | Search everything |

---

## 🆓 Other editors (optional)

IntelliJ is the most popular, but some people use others:

| Editor | Notes |
|---|---|
| **VS Code** | Free and light. Install the **"Extension Pack for Java"** and **"Spring Boot Extension Pack"**. |
| **Eclipse** | Free and old but still used by many companies. |

👉 This book uses **IntelliJ** in all screenshots and steps. If you are a beginner, please use IntelliJ too, so your screen looks like the book.

---

## ✋ Try it yourself

1. Open IntelliJ and open your project `my-first-java`.
2. Run the sample code. Look at the output.
3. In the code, find the text `"Hello and welcome!"`. Change it to `"Hello, my name is ...!"` with **your** name.
   - Be careful: keep the `"` quotes at the start and end!
4. Run again. Do you see your name? 🎉
5. Change the text size: **File → Settings → Editor → Font → Size**. (Mac: **IntelliJ IDEA → Settings**.)

---

## ⚠️ Common mistakes

### Problem 1: "Project JDK is not defined" / "No SDK"

**What it means:** IntelliJ does not know where Java is.

**How to fix:**
1. Click **File → Project Structure...**
2. Click **Project** on the left.
3. In **SDK**, choose your JDK (for example **25 Eclipse Temurin**).
   - If it's not there: **Add SDK → JDK...** → choose the Java folder from Chapter 3.
4. Click **OK**.

### Problem 2: The ▶ Run button is gray

**What it means:** IntelliJ is still **starting up** (indexing your files), or it doesn't know which file to run.

**How to fix:**
- Look at the **bottom right** of the window. If you see a progress bar ("Indexing..."), just **wait**.
- Or: right-click on `Main.java` in the Project window → choose **Run 'Main.main()'**.

### Problem 3: My code has red lines everywhere

**What it means:** There is a mistake in the code, **or** the JDK is not set.

**How to fix:**
- Did you delete a `"`, `;`, `{` or `}` by accident? Press `Ctrl + Z` to undo.
- Check Problem 1 (no JDK).

### Problem 4: I closed the Project window (or another window) by accident

**How to fix:** Click **View → Tool Windows → Project** (or press `Alt + 1`).

---

## ✅ Summary

- An **IDE** is a smart program for writing, checking and running code.
- We use **IntelliJ IDEA** (free version) from **jetbrains.com/idea**.
- To make a new project: **New Project** → Name → Language **Java** → Build system **IntelliJ** → JDK → **Create**.
- Your code always goes in the **`src`** folder.
- The green **▶** button runs your program. The output is shown in the **Run window** at the bottom.
- `Process finished with exit code 0` means everything was OK.

---

## ❓ Quiz

1. What does IDE mean?
2. In which folder do you put your Java code?
3. What does `exit code 0` mean?
4. Which button starts your program?
5. IntelliJ says "No SDK". What does this mean?
6. Which keyboard shortcut makes your code tidy?

<details>
<summary>Click to see the answers</summary>

1. Integrated Development Environment — a smart program to write, check and run code.
2. In the **`src`** folder.
3. The program finished **without errors**.
4. The green **▶ Run** button.
5. IntelliJ does not know where Java (the JDK) is. You must choose it in **File → Project Structure**.
6. `Ctrl + Alt + L` (Windows) or `Cmd + Option + L` (Mac).

</details>

---

[⬅ Previous chapter](03-install-java.md) | [Table of Contents](../README.md) | [Next chapter: Hello World ➡](05-hello-world.md)
