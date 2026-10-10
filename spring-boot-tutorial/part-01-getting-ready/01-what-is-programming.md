# Chapter 1 – What is Programming?

[⬅ Back to Table of Contents](../README.md) | [Next chapter ➡](02-what-are-java-and-spring-boot.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What a **computer program** is
- What **programming** is
- What a **programming language** is
- Why a computer needs **very exact** instructions

There is **no code to install** in this chapter. We only learn the ideas. Relax and read. ☕

---

## 📖 Story: Making tea

Imagine you have a robot friend. The robot is very strong and very fast.
But the robot is **not smart**. It does **exactly** what you say. Nothing more. Nothing less.

You say to the robot:

> "Make tea."

The robot does nothing. 🤖❓
It does not know what "make tea" means.

So you try again. This time you give **small steps**:

1. Take the cup.
2. Put the tea bag in the cup.
3. Fill the kettle with water.
4. Turn on the kettle.
5. Wait until the water is hot.
6. Pour the hot water into the cup.
7. Wait 3 minutes.
8. Take out the tea bag.

Now the robot can make tea! ✅

But look carefully. What if you **forget step 4**?
The robot waits forever, because the water never gets hot. 😅

**This is programming.**

- The **robot** is the **computer**.
- The **list of steps** is the **program**.
- **You**, writing the steps, are the **programmer**.

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Computer** | A machine that follows instructions very fast. |
| **Instruction** | One small order, like "Turn on the kettle." |
| **Program** | A list of instructions, in the correct order. |
| **Programming** | Writing programs. |
| **Programmer** | A person who writes programs. (Soon, this is you!) |
| **Programming language** | A special language that computers can understand. Java is one. |
| **Code** | The text of a program. "Write code" = "write a program". |
| **Bug** | A mistake in a program. |
| **Debugging** | Finding and fixing bugs. |

---

## 🧠 Idea 1: A computer is fast, but not smart

A computer can do **billions** of small jobs in one second.
But it cannot **guess** what you want.

A human understands this:

> "Put the milk in the fridge, please."

A human knows which milk, which fridge, and to open the door first.

A computer needs every small step:

1. Go to the table.
2. Pick up the milk.
3. Go to the fridge.
4. Open the fridge door.
5. Put the milk inside.
6. Close the fridge door.

👉 **Remember:** The computer only does what you write. If you write something wrong, the computer does the wrong thing.

---

## 🧠 Idea 2: Order is important

Look at these two lists.

**List A**
1. Open the door.
2. Walk outside.

**List B**
1. Walk outside.
2. Open the door.

List B is a problem. You walk into the closed door! 🚪💥

A computer reads instructions **from top to bottom**, one by one.
So the order of your instructions is very important.

---

## 🧠 Idea 3: Why do we need a programming language?

A computer inside understands only **numbers**: `0` and `1`.

Something like this:

```
01001000 01100101 01101100 01101100 01101111
```

This is very hard for humans to read or write. 😵

English is easy for humans, but it is hard for computers.
Why? Because English words can have **many meanings**.

> "I saw her duck."

Did she have a duck (the bird 🦆)? Or did she bend down quickly?
Humans guess from the situation. Computers cannot guess.

So people made **programming languages**.
A programming language is in the **middle**:

```
Human language   →   Programming language   →   Computer language (0 and 1)
  (English)              (Java)                  (machine code)
   too unclear         clear AND readable         too hard for us
```

- It looks a little like English, so **humans can read it**.
- It has **strict rules**, so there is only **one meaning**.
- A special tool changes it into 0 and 1, so the **computer can run it**.

---

## 💻 A first look at code

You do not need to understand this yet. Just look at it.
This is a tiny program in **Java**:

```java
System.out.println("Hello!");
```

When the computer runs it, it shows this on the screen:

```
Hello!
```

### 🔍 Line by line (very simple for now)

| Part | Meaning |
|---|---|
| `System.out` | "The screen" (the place where text is shown) |
| `.println` | "Print a line" = show some text and go to a new line |
| `( ... )` | Inside the brackets we put **what** to show |
| `"Hello!"` | The text to show. Text is always inside `" "` quotes |
| `;` | The end of the instruction. Like a full stop `.` in English |

In Chapter 5 you will run this code yourself, and we will explain every word again in more detail.

---

## 🧠 Idea 4: From code to a running program

Here is what happens, step by step:

```
 ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
 │  1. You      │      │  2. A tool   │      │  3. The      │
 │  write code  │ ───► │  translates  │ ───► │  computer    │
 │  (Java)      │      │  the code    │      │  runs it     │
 └──────────────┘      └──────────────┘      └──────────────┘
```

1. **You write code.** It is just text in a file, like a letter.
2. **A tool translates it.** This tool is called a **compiler**. It changes your code into something the computer understands.
3. **The computer runs it.** "Run" means "do the instructions".

---

## 🧠 Idea 5: Bugs are normal

Every programmer makes mistakes. **Every single one.** Even experts with 30 years of experience.

A mistake in code is called a **bug** 🐛.
Finding and fixing it is called **debugging**.

There are two common kinds of bugs:

| Kind | Example in real life | Example in code |
|---|---|---|
| **Spelling / grammar mistake** | "I goed to school." | You forget the `;` at the end. The computer says: "I don't understand!" |
| **Logic mistake** | You forgot to turn on the kettle. The steps are "correct English", but the tea is cold. | The program runs, but the answer is wrong. |

👉 When you see an error message, **don't be sad**. The computer is trying to **help you**. It tells you where the problem is.

---

## ✋ Try it yourself

No computer needed. Take a paper and a pen. ✏️

**Task 1:** Write the steps to **brush your teeth**.
Write them so that a robot who knows *nothing* can follow them.
Use small steps and number them.

**Task 2:** Give your list to a friend or family member. Ask them to act like a stupid robot.
They must do **exactly** what you wrote, nothing more.
Did it work? Did you forget a step? (Most people forget "open the toothpaste"! 😄)

**Task 3:** Look at this list. Find the bug.

1. Put on your shoes.
2. Put on your socks.
3. Walk to school.

<details>
<summary>Click to see the answer</summary>

The order is wrong. You must put on socks **before** shoes. Steps 1 and 2 must swap places.

</details>

---

## ⚠️ Common mistakes (in thinking)

| Wrong idea | The truth |
|---|---|
| "Programming is only for very smart people." | No. Programming is a skill, like cooking or riding a bike. Everyone can learn with practice. |
| "I need to be good at math." | For most programs, simple math (+, −, ×, ÷) is enough. |
| "I need perfect English." | No. Java uses only a few English words, and you will learn them one by one. |
| "If I get an error, I am bad at this." | No. Errors are normal. They help you learn. |
| "I must remember everything." | No. Programmers look things up every day. Understanding is more important than remembering. |

---

## ✅ Summary

- A **program** is a list of instructions for a computer.
- **Programming** means writing these instructions.
- A computer is **fast but not smart**. It does exactly what you say.
- The **order** of instructions is important. The computer reads from top to bottom.
- A **programming language** (like Java) is clear for computers and readable for humans.
- A **compiler** translates your code so the computer can run it.
- A **bug** is a mistake. Fixing it is **debugging**. Bugs are normal.

---

## ❓ Quiz

1. What is a program?
2. Why can't we just write programs in normal English?
3. What does the computer do if your instructions are in the wrong order?
4. What is a bug?
5. In the code `System.out.println("Hello!");` — what is the `;` for?

<details>
<summary>Click to see the answers</summary>

1. A list of instructions, in the correct order, that a computer follows.
2. Because English words can have many meanings. The computer cannot guess which meaning you want.
3. It still follows them in that order, so the result is wrong.
4. A mistake in a program.
5. It shows the **end** of the instruction, like a full stop `.` in an English sentence.

</details>

---

[⬅ Back to Table of Contents](../README.md) | [Next chapter: What are Java and Spring Boot? ➡](02-what-are-java-and-spring-boot.md)
