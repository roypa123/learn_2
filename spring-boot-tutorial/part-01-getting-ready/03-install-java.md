# Chapter 3 – Install Java on Your Computer

[⬅ Previous chapter](02-what-are-java-and-spring-boot.md) | [Table of Contents](../README.md) | [Next chapter ➡](04-install-intellij.md)

---

## 🎯 Goal

At the end of this chapter:

- The **JDK** (Java toolbox) is installed on your computer.
- You know how to open the **terminal** (the black window where you type commands).
- You can check that Java works with the commands `java -version` and `javac -version`.

⏱️ Time needed: about 15–20 minutes.

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Download** | Copy a file from the internet to your computer. |
| **Install** | Put a program on your computer so you can use it. |
| **Installer** | The file that installs a program. On Windows it often ends with `.msi` or `.exe`. |
| **Version** | The number of a program's edition, like `25`. Bigger number = newer. |
| **LTS** | *Long Term Support.* A version that gets fixes for many years. Best for learning and for work. |
| **Terminal** | A window where you type commands instead of clicking. On Windows it is called **Command Prompt**, **PowerShell** or **Terminal**. |
| **Command** | An instruction you type in the terminal, then press **Enter**. |
| **PATH** | A list of folders where Windows looks for programs. If Java is in PATH, you can type `java` from anywhere. |
| **JAVA_HOME** | A setting that tells other programs (like Maven) where Java is installed. |

---

## 📖 Story: Getting a toolbox

Before a carpenter can build a table, they need a **toolbox**: a hammer, a saw, nails. 🧰

Before **you** can write Java, you need **your** toolbox. That toolbox is the **JDK**.

There are many companies that make a JDK. They all work the same way. In this book we use **Eclipse Temurin**, because:

- It is **free** for everyone, also for work.
- It is made by a trusted group (the Eclipse Foundation / Adoptium).
- It has an easy installer.

---

## 🪟 Part 1: Install Java on Windows

### Step 1 – Open the download website

1. Open your web browser (Chrome, Edge, Firefox...).
2. Go to this address:

   ```
   https://adoptium.net
   ```

3. You will see a big button to download the **latest LTS** version of Temurin.

> 💡 **Which version?** Choose the newest **LTS** version. At the time this book was written, that is **Java 25**. Java 21 is also fine. Everything in this book works with **Java 21 or newer**.

### Step 2 – Download the installer

1. Make sure the website shows **Windows** and **x64**.
   (Most Windows computers are **x64**. If your computer has an "ARM" processor, choose **aarch64**.)
2. Choose the **`.msi`** file. This is the easy installer.
3. Click **Download**. Wait until it finishes.

> 💡 **How do I know if my computer is x64?**
> Press the **Windows key**, type `About your PC`, and press Enter.
> Look at **System type**. It says something like *"64-bit operating system, x64-based processor"*.

### Step 3 – Run the installer

1. Open your **Downloads** folder.
2. Double-click the file. Its name looks like `OpenJDK25U-jdk_x64_windows_hotspot_....msi`.
3. Click **Next**.

### Step 4 – ⚠️ The important screen: Custom Setup

Now you see a screen called **Custom Setup** with a list of features. This screen is **very important**.

You will see something like this:

```
 ┌─────────────────────────────────────────────┐
 │ Custom Setup                                │
 │                                             │
 │  [💾] Add to PATH                           │
 │  [💾] Associate .jar                        │
 │  [❌] Set JAVA_HOME variable    ◄── change! │
 │  [❌] JavaSoft (Oracle) registry keys       │
 │                                             │
 └─────────────────────────────────────────────┘
```

- **Add to PATH** — should already be ON (💾 icon). ✅ Keep it.
- **Set JAVA_HOME variable** — is often OFF (red ❌). **Turn it ON:**
  1. Click on the small icon next to **Set JAVA_HOME variable**.
  2. A small menu opens. Choose **"Will be installed on local hard drive"**.
  3. Now the icon is not red any more. ✅

👉 **Why?** Later, tools like **Maven** and **Spring Boot** look at **JAVA_HOME** to find Java. If it is not set, they may not work.

### Step 5 – Finish

1. Click **Next**.
2. Click **Install**.
3. Windows may ask *"Do you want to allow this app to make changes?"* Click **Yes**.
4. Wait. Then click **Finish**. 🎉

---

## 💻 Part 2: Open the terminal

Now we check if Java works. For this, we use the **terminal**.

### How to open it on Windows

1. Press the **Windows key** ⊞ on your keyboard.
2. Type: `cmd`
3. Press **Enter**.

A black window opens. It looks like this:

```
Microsoft Windows [Version 10.0.22621]
(c) Microsoft Corporation. All rights reserved.

C:\Users\YourName>
```

### 🔍 What do we see?

| Part | Meaning |
|---|---|
| `C:\Users\YourName` | The **folder** you are "standing in" right now. |
| `>` | The terminal is **waiting** for you to type a command. |
| The blinking line `_` | The cursor. Your typing appears here. |

> ⚠️ **Important:** If the terminal was **already open before** you installed Java, **close it and open a new one.** An old terminal does not know about the new PATH.

---

## ✅ Part 3: Check that Java works

### Command 1: `java -version`

Type this and press **Enter**:

```
java -version
```

You should see something like this:

```
openjdk version "25" 2025-09-16 LTS
OpenJDK Runtime Environment Temurin-25+36 (build 25+36-LTS)
OpenJDK 64-Bit Server VM Temurin-25+36 (build 25+36-LTS, mixed mode, sharing)
```

(Your numbers may be a little different. That is OK.)

#### 🔍 Line by line

**The command:**

| Part | Meaning |
|---|---|
| `java` | Start the program called **java** (the JVM, the program runner). |
| (space) | Separates the program name from the option. |
| `-version` | An **option**. It means: "Don't run any program. Just tell me your version." The `-` (minus sign) shows that this is an option. |

**The answer:**

| Line | Meaning |
|---|---|
| `openjdk version "25" ... LTS` | You have **Java 25**, and it is an **LTS** version. 🎉 |
| `OpenJDK Runtime Environment Temurin-25...` | The company that made this JDK is **Temurin** (Adoptium). |
| `OpenJDK 64-Bit Server VM ...` | The **JVM** (VM = Virtual Machine) is ready. It is **64-bit**. |

### Command 2: `javac -version`

Now type this and press **Enter**:

```
javac -version
```

You should see:

```
javac 25
```

#### 🔍 Line by line

| Part | Meaning |
|---|---|
| `javac` | The **Java Compiler**. The "c" means **compiler**. It changes your `.java` files into `.class` files. |
| `-version` | "Tell me your version." |
| `javac 25` | The answer: the compiler is version 25. |

👉 **Why check both?** `java` runs programs, `javac` builds them. You need **both**. If `javac` works, you know you installed the full **JDK** (and not only a small "runtime").

### Command 3: Check JAVA_HOME

Type this and press **Enter**:

```
echo %JAVA_HOME%
```

You should see a folder, for example:

```
C:\Program Files\Eclipse Adoptium\jdk-25.0.0.36-hotspot\
```

#### 🔍 Line by line

| Part | Meaning |
|---|---|
| `echo` | "Repeat back to me" / "show me". |
| `%JAVA_HOME%` | In Command Prompt, a name between `%` signs means: "the **value** of this setting". |

So the command means: **"Show me the value of JAVA_HOME."**

If you see a folder path → ✅ Perfect!
If you see just `%JAVA_HOME%` (the same text you typed) → ❌ JAVA_HOME is not set. See "Common mistakes" below.

> 💡 **Using PowerShell instead of cmd?** In PowerShell the command is different:
> ```
> echo $env:JAVA_HOME
> ```

---

## 🍎 🐧 For Mac and Linux users (short)

**Mac:**
1. Go to `https://adoptium.net`, choose **macOS**, download the **`.pkg`** file.
   (New Macs with M1/M2/M3/M4 chips use **aarch64**. Older Intel Macs use **x64**.)
2. Double-click it and follow the steps.
3. Open **Terminal** (press `Cmd + Space`, type `Terminal`, press Enter).
4. Type `java -version` and `javac -version`.

**Linux (Ubuntu):**
The Adoptium website explains how to add their package source. After that:
```
sudo apt install temurin-25-jdk
```
Then check with `java -version` and `javac -version`.

---

## ✋ Try it yourself

1. Open a **new** terminal.
2. Type `java -version`. Write down the version number you see.
3. Type `javac -version`. Is it the same number?
4. Type `java --help` (two minus signs). You will see a long list of options. Don't read all of it! Just see that Java answers you. 😊
5. Type `exit` and press Enter. What happens?

<details>
<summary>Answer for number 5</summary>

The terminal window **closes**. `exit` is the command to close the terminal.

</details>

---

## ⚠️ Common mistakes

### Problem 1: `'java' is not recognized as an internal or external command`

Full message:
```
'java' is not recognized as an internal or external command,
operable program or batch file.
```

**What it means:** Windows cannot find Java. It is not in the **PATH**.

**How to fix:**
1. **First, close the terminal and open a new one.** This fixes the problem most of the time!
2. Still not working? **Restart your computer.**
3. Still not working? Run the installer again. On the **Custom Setup** screen, make sure **Add to PATH** is ON.

### Problem 2: `java` works, but `javac` does not

**What it means:** You installed a **JRE** (only the runner), not the **JDK** (the full toolbox).

**How to fix:** Go back to adoptium.net. Make sure you choose **JDK**, not **JRE**. Install again.

### Problem 3: `echo %JAVA_HOME%` shows `%JAVA_HOME%`

**What it means:** JAVA_HOME is not set.

**How to fix (easy way):**
Run the installer again. Choose **Change** (or **Modify**). Turn ON **Set JAVA_HOME variable**. Finish. Open a **new** terminal.

**How to fix (by hand):**
1. Press the **Windows key**, type `environment`, and choose **"Edit the system environment variables"**.
2. Click the button **Environment Variables...**
3. Under **System variables**, click **New...**
4. **Variable name:** `JAVA_HOME`
5. **Variable value:** the folder where Java is installed, for example
   `C:\Program Files\Eclipse Adoptium\jdk-25.0.0.36-hotspot`
   (Open this folder in File Explorer to check the exact name on your computer.)
6. Click **OK**, **OK**, **OK**.
7. Open a **new** terminal and try `echo %JAVA_HOME%` again.

### Problem 4: I see an **old** version (like `1.8` or `11`)

**What it means:** An older Java was already on your computer, and Windows finds it first.

**How to fix:**
- **Easy way:** Uninstall the old Java. (Windows key → type `Add or remove programs` → find the old Java → **Uninstall**.) Open a new terminal.
- **Or:** Open Environment Variables (see Problem 3). In **Path**, move the new Java folder to the **top** of the list.

### Problem 5: I typed `Java -Version` with capital letters

On Windows this sometimes works, but on Mac and Linux it does **not**. Java and its commands **care about big and small letters**.
👉 Always type commands **exactly** as shown: `java -version`.

---

## ✅ Summary

- The **JDK** is the Java toolbox. We use the free **Eclipse Temurin** JDK from **adoptium.net**.
- Choose an **LTS** version (Java 21 or newer, best: the newest LTS).
- In the installer, turn ON **Add to PATH** and **Set JAVA_HOME variable**.
- Open the terminal with **Windows key → `cmd` → Enter**.
- Check your installation:
  - `java -version` → the runner works
  - `javac -version` → the compiler works
  - `echo %JAVA_HOME%` → JAVA_HOME is set
- If a command is "not recognized": **open a new terminal** or **restart** the computer.

---

## ❓ Quiz

1. What is the name of the free JDK we use in this book?
2. What does **LTS** mean?
3. Which two settings must be ON in the installer?
4. What is the difference between `java` and `javac`?
5. You installed Java, but the terminal says `'java' is not recognized`. What is the **first** thing you should try?
6. What does the `-` in `-version` show?

<details>
<summary>Click to see the answers</summary>

1. Eclipse Temurin (from adoptium.net).
2. Long Term Support. The version gets fixes for many years.
3. **Add to PATH** and **Set JAVA_HOME variable**.
4. `java` **runs** Java programs (it starts the JVM). `javac` **compiles** Java code (turns `.java` into `.class`).
5. Close the terminal and open a **new** one.
6. It shows that `version` is an **option** for the command, not a file or a program.

</details>

---

[⬅ Previous chapter](02-what-are-java-and-spring-boot.md) | [Table of Contents](../README.md) | [Next chapter: Install IntelliJ IDEA ➡](04-install-intellij.md)
