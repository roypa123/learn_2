# Chapter 42 – Git: Saving the History of Your Code

[⬅ Previous chapter](41-pom-xml.md) | [Table of Contents](../README.md) | [Next chapter ➡](../part-06-web/43-client-and-server.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- What **version control** is, and why **every** programmer uses it
- How to **install** and **set up** Git
- The 3 places: **working folder**, **staging area**, **repository**
- The daily commands: `init`, `status`, `add`, `commit`, `log`, `diff`
- How to **undo** mistakes
- What **`.gitignore`** is
- **Branches**: working on new ideas safely, and **merging**
- How to fix a **merge conflict**
- **GitHub**: `push`, `pull`, `clone`
- How to use Git **inside IntelliJ** 🖱️

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Version control** | A system that **remembers every version** of your files. |
| **Git** | The most popular version control tool in the world. |
| **Repository (repo)** | A project folder that Git is watching, with its **whole history**. |
| **Commit** | A **saved snapshot** 📸 of your project at one moment, with a message. |
| **Staging area** | A "waiting room" for changes you **want** to put in the next commit. |
| **Branch** | A separate **line of work** — a copy where you can try ideas safely. |
| **Merge** | Joining the work from one branch into another. |
| **Conflict** | Two branches changed the **same line** differently. Git needs **you** to choose. |
| **Remote** | A copy of the repo on another computer (like **GitHub**). |
| **Push / Pull** | Send your commits **to** the remote / get new commits **from** the remote. |
| **Clone** | Download a full copy of a remote repo. |

---

## 📖 Story: The video game save points 🎮

When you play a video game, you **save** your progress at **save points**:

```
  💾 Save 1          💾 Save 2           💾 Save 3              💀 Oh no!
  "Level 1 done"     "Got the sword"     "Beat the dragon"      (you fell in lava)
```

When you fall in the lava 🌋, you don't start the **whole game** again. You go back to **Save 3**! 😌

And sometimes you make a **second save file** to try something risky: "What if I fight the boss without armor?" 🤔 If it goes badly, your main save file is still safe.

**Git is save points for your code:**

| Game | Git |
|---|---|
| 💾 Save point | **commit** |
| The list of all saves | **log** (history) |
| Load an old save | go back to an old commit |
| A second save file for risky ideas | **branch** |
| Cloud save (play on another device) | **GitHub** (remote) |

---

## 🤔 Part 1: Why use Git?

Without Git, people do this: 😅

```
 my-project.zip
 my-project-final.zip
 my-project-final-v2.zip
 my-project-final-v2-REALLY-FINAL.zip
 my-project-final-v2-REALLY-FINAL-fixed.zip
```

Problems:
- Which one is the newest? 🤷
- What changed between them? 🤷
- You broke something yesterday — what was the **working** version? 😱
- Two people changed the same file — whose version wins? 😱😱

**With Git:**
- ✅ **Every** change is saved with a **date**, an **author** and a **message**.
- ✅ You can see **exactly** what changed, line by line.
- ✅ You can go **back** to any old version.
- ✅ Many people can work on the **same** project at the same time.
- ✅ Your code is **backed up** on GitHub. ☁️

👉 **Every** software company uses Git. Knowing Git is as important as knowing Java! 💼

---

## 🛠️ Part 2: Install and set up Git

### Install

**Windows:**
1. Go to `https://git-scm.com/downloads`.
2. Download **Git for Windows** and run the installer.
3. Click **Next** on every screen — the default settings are fine. 👍

**Mac:** Open Terminal and type `git --version`. If Git is missing, the Mac offers to install it. Click **Install**.

**Linux (Ubuntu):** `sudo apt install git`

### Check it

Open a **new** terminal (Chapter 3) and type:

```
git --version
```

```
git version 2.47.1.windows.1
```

(Your number may be different.) ✅

### Tell Git who you are (once per computer)

Every commit records **who** made it. Tell Git your name and email:

```
git config --global user.name "Sara Ahmed"
git config --global user.email "sara@example.com"
git config --global init.defaultBranch main
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `git config` | "Change a Git setting." |
| `--global` | "For **all** my projects on this computer." |
| `user.name "Sara Ahmed"` | Your name, shown in every commit. |
| `user.email "..."` | Your email. (Use the **same** email as your GitHub account later.) |
| `init.defaultBranch main` | Call the main branch `main` (the modern name). |

> 💡 **On Windows**, you can use **Git Bash** (installed with Git) or PowerShell / cmd. The Git commands are the **same** everywhere.

---

## 📦 Part 3: The 3 places — working folder, staging, repository

This is the **most important idea** in Git. Understand this, and everything else is easy! 🧠

```
  📁 WORKING FOLDER          📋 STAGING AREA             🗄️ REPOSITORY (.git)
  (your files,               (the "waiting room":        (the history: all
   as you edit them)          what goes in the            saved commits)
                              NEXT commit)
        │                          │                           │
        │ ─────── git add ───────► │                           │
        │                          │ ─────── git commit ─────► │
        │                          │                           │
```

📸 **Story: Taking a class photo**
1. **Working folder** = the whole classroom. Kids are everywhere, moving, playing. 🏃
2. **Staging area** = you call some kids to **stand in front of the camera**. "Sara, Tom, Lina — come here!" (`git add`)
3. **Commit** = **click!** 📸 The photo is taken and put in the **album** forever. (`git commit`)

You choose **who** is in the photo. Not every change must go into every commit!

---

## 🚀 Part 4: Your first repository

Let's practice in the terminal. Make a new folder and go into it:

```
mkdir my-diary
cd my-diary
```

### `git init` — start watching this folder

```
git init
```

```
Initialized empty Git repository in C:/Users/Sara/projects/my-diary/.git/
```

Git created a **hidden** folder called **`.git`**. This is where the whole history lives. 🗄️

> ⚠️ **Never delete or edit the `.git` folder** by hand. If you delete it, the history is **gone**!

### `git status` — "what's going on?" 🔍

```
git status
```

```
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

👉 **`git status` is your best friend.** Run it **all the time**. It tells you what's happening and even suggests the next command!

### Create a file

Create `Hello.java` in the folder:

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello!");
    }
}
```

```
git status
```

```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	Hello.java

nothing added to commit but untracked files present (use "git add" to track)
```

**Untracked** = "Git sees a new file, but isn't saving it yet." 👀

### `git add` — put it in the staging area 📋

```
git add Hello.java
git status
```

```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   Hello.java
```

Now `Hello.java` is "standing in front of the camera". 📸

> 💡 `git add .` (with a dot) adds **all** changed files in the folder. Very common!

### `git commit` — take the snapshot 📸

```
git commit -m "Add Hello program"
```

```
[main (root-commit) d53964f] Add Hello program
 1 file changed, 5 insertions(+)
 create mode 100644 Hello.java
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `git commit` | Save a snapshot of everything in the staging area. |
| `-m "Add Hello program"` | The **message**: what this commit does. (`-m` = message) |
| `d53964f` | The commit's **ID** (called a **hash**). Every commit has a unique one. |
| `1 file changed, 5 insertions(+)` | 1 file, 5 new lines. |

🎉 Your first save point! 💾

---

## 🔁 Part 5: The daily cycle

Change the greeting in `Hello.java`:

```java
System.out.println("Hello, Git!");
```

```
git status
```

```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   Hello.java

no changes added to commit (use "git add" and/or "git commit -a")
```

### `git diff` — what exactly changed? 🔎

```
git diff
```

```
diff --git a/Hello.java b/Hello.java
index b4d21b9..0aac7f3 100644
--- a/Hello.java
+++ b/Hello.java
@@ -1,5 +1,5 @@
 public class Hello {
     public static void main(String[] args) {
-        System.out.println("Hello!");
+        System.out.println("Hello, Git!");
     }
 }
```

| Symbol | Meaning |
|---|---|
| `-` (red) | a line that was **removed** |
| `+` (green) | a line that was **added** |
| no symbol | unchanged lines (for context) |

A change of one line = one line removed + one line added.

### Add and commit again

```
git add Hello.java
git commit -m "Change the greeting"
```

```
[main ac87848] Change the greeting
 1 file changed, 1 insertion(+), 1 deletion(-)
```

> 💡 **Shortcut:** `git commit -am "message"` = add **all already-tracked** files + commit, in one step. (New files still need `git add` first.)

### 🔄 The cycle you'll do every day

```
   ✏️ edit files
        ↓
   🔍 git status        (what changed?)
        ↓
   🔎 git diff          (show me the details)
        ↓
   📋 git add .         (put changes in staging)
        ↓
   📸 git commit -m "..." (save the snapshot)
        ↓
   (repeat)
```

---

## 📜 Part 6: Looking at history — `git log`

```
git log
```

```
commit ac87848277f652b680df9f86d4e5a772a2f8ba3e
Author: Sara Ahmed <sara@example.com>
Date:   Sat Oct 10 21:48:21 2026 +0530

    Change the greeting

commit d53964fc4caf919bb70b35cf386109da04d4a742
Author: Sara Ahmed <sara@example.com>
Date:   Sat Oct 10 21:48:20 2026 +0530

    Add Hello program
```

Newest at the **top**. Each commit shows its **hash**, **author**, **date** and **message**.

(If the list is long, Git shows it page by page. Press **Space** for the next page, **q** to quit.)

### Short version

```
git log --oneline
```

```
ac87848 Change the greeting
d53964f Add Hello program
```

The short hash (first 7 characters) is enough to identify a commit. 👍

---

## ✍️ Part 7: Good commit messages

Your messages are **notes for the future** (for you and your team). 📝

| 👎 Bad | 👍 Good |
|---|---|
| `fix` | `Fix crash when the name is empty` |
| `changes` | `Add discount for members` |
| `asdf` | `Rename Student.getAge to calculateAge` |
| `stuff from friday` | `Add tests for the BankAccount withdraw rules` |

**Tips:**
- Start with a **verb**: Add, Fix, Change, Remove, Rename, Update.
- Say **what** and (if not obvious) **why**.
- Keep the first line **short** (about 50 characters).
- **One idea per commit.** Fix a bug → commit. Add a feature → another commit. Small commits are easy to understand and easy to undo. 🧩

---

## ↩️ Part 8: Undoing mistakes

### "I changed a file and want to throw away my changes" 🗑️

```
git restore Hello.java
```

The file goes back to the version of the **last commit**. ⚠️ Your uncommitted changes are **lost** forever!

### "I added a file to staging by mistake" 📋→📁

```
git restore --staged Hello.java
```

The file leaves the staging area. Your changes stay in the file. ✅

### "My last commit message has a typo" ✏️

```
git commit --amend -m "Fix the correct message"
```

(Only do this if you haven't **pushed** the commit yet — Part 13.)

### "I want to undo a commit" ⏪

```
git revert ac87848
```

This makes a **new** commit that does the **opposite** of `ac87848`. The history stays complete and honest. ✅ This is the **safe** way.

### "I want to see an old version"

```
git switch --detach d53964f      # look around in the old version (read-only feel)
git switch main                   # go back to the newest
```

> ⚠️ You may see `git reset --hard` on the internet. It can **delete** work permanently. Avoid it until you really understand Git! 💣

---

## 🙈 Part 9: `.gitignore` — files Git should NOT save

Some files should **never** go into Git:

| Don't commit | Why |
|---|---|
| `target/` | Maven's output — can be rebuilt any time (Chapter 40). |
| `.idea/`, `*.iml` | IntelliJ's personal settings. |
| `*.class` | Compiled files. |
| `.env`, passwords, API keys 🔑 | **Secrets!** Never put them in Git. 🚨 |
| `*.log` | Log files. |

Create a file named **`.gitignore`** (with the dot!) in the project folder:

```
# Build output
target/
*.class

# IntelliJ
.idea/
*.iml

# Logs
*.log

# Secrets
.env
```

| Line | Meaning |
|---|---|
| `# ...` | a comment |
| `target/` | ignore the whole `target` folder |
| `*.class` | ignore all files ending with `.class` (`*` = anything) |

Now `git status` doesn't show these files anymore. 🙈

🌱 **Good news:** Spring Initializr gives you a ready `.gitignore`. And IntelliJ also creates one for new projects!

> 🚨 **Important:** If you accidentally commit a password, removing it in a new commit is **not enough** — it's still in the history! Change the password immediately. Prevention is best: add secrets to `.gitignore` **before** your first commit.

---

## 🌿 Part 10: Branches — try ideas safely

A **branch** is a separate line of work. 🌳 The main line is called **`main`**.

```
 main:        ●───●───●
                       \
 new-feature:           ●───●   ← try something new here
```

📖 **Story:** You're writing a story 📖. You want to try a different ending — but you're not sure it's good. So you make a **photocopy** of your story and write the new ending on the copy. If you like it → you put it in the real story. If not → you throw the copy away. Your original is **always safe**. 😌

### Create and switch to a branch

```
git switch -c add-goodbye
```

```
Switched to a new branch 'add-goodbye'
```

| Part | Meaning |
|---|---|
| `git switch` | Go to another branch. |
| `-c` | **Create** it first. |
| `add-goodbye` | The branch name (describe the work, use `-` between words). |

### See all branches

```
git branch
```

```
* add-goodbye
  main
```

The `*` shows the branch you're **on** now.

### Work on the branch

Create `Goodbye.java`, then:

```
git add .
git commit -m "Add Goodbye program"
```

```
[add-goodbye 1cdfb2e] Add Goodbye program
 1 file changed, 5 insertions(+)
 create mode 100644 Goodbye.java
```

### Switch back to main

```
git switch main
```

Look at your folder — **`Goodbye.java` is gone!** 😮 Don't worry: it's safe on the other branch. Git changes your folder to match the branch you're on. 🪄

### Merge the branch into main

You're happy with the work. Bring it into `main`:

```
git switch main
git merge add-goodbye
```

```
Updating ac87848..1cdfb2e
Fast-forward
 Goodbye.java | 5 +++++
 1 file changed, 5 insertions(+)
 create mode 100644 Goodbye.java
```

✅ Now `main` has `Goodbye.java` too!

```
git log --oneline --graph
```

```
* 1cdfb2e Add Goodbye program
* ac87848 Change the greeting
* d53964f Add Hello program
```

### Delete the branch (it's done)

```
git branch -d add-goodbye
```

### 💼 How teams use branches

```
 main:     ●────●──────────●──────────●   ← always working, always safe ✅
             \            /  \        /
 feature-A:   ●───●───●──    \      /
                               ●───●      ← feature-B
```

1. Everyone keeps `main` **working**.
2. For each new feature or bug fix → a **new branch**.
3. When it's done and tested → **merge** it into `main` (on GitHub, through a **Pull Request** — Part 13).

---

## 💥 Part 11: Merge conflicts — when Git needs your help

If two branches change the **same line** differently, Git can't decide which one is right. 🤷

```
 main changed line 3 to:       System.out.println("Hi from main");
 branch b1 changed line 3 to:  System.out.println("Hi from branch b1");
```

```
git merge b1
```

```
Auto-merging Hello.java
CONFLICT (content): Merge conflict in Hello.java
Automatic merge failed; fix conflicts and then commit the result.
```

Don't panic! 😌 Open `Hello.java`:

```java
public class Hello {
    public static void main(String[] args) {
<<<<<<< HEAD
        System.out.println("Hi from main");
=======
        System.out.println("Hi from branch b1");
>>>>>>> b1
    }
}
```

### 🔍 Reading the conflict markers

| Marker | Meaning |
|---|---|
| `<<<<<<< HEAD` | Start: **your** version (the branch you're on — `main`). |
| `=======` | The line between the two versions. |
| `>>>>>>> b1` | End: the **other** version (from branch `b1`). |

### How to fix it

1. **Choose** what the code should be. Keep one version, the other, or **combine** them. **Delete the markers**:

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hi from main and b1!");
    }
}
```

2. Tell Git it's fixed, and commit:

```
git add Hello.java
git commit -m "Merge b1 and combine the greetings"
```

✅ Done!

> 💡 **IntelliJ makes this much easier:** it shows a window with **3 columns** — your version, the result, their version — and buttons `>>` and `<<` to pick changes. 🖱️ (Git → Resolve Conflicts...)

> 💡 Changed your mind? `git merge --abort` cancels the merge and goes back to how things were.

---

## ☁️ Part 12: GitHub — your code in the cloud

**GitHub** (`https://github.com`) is a website that stores Git repositories online. ☁️ (Others: GitLab, Bitbucket.)

| Why GitHub? | |
|---|---|
| 💾 **Backup** | Your computer breaks? Your code is safe. |
| 👥 **Teamwork** | Everyone pushes and pulls from the same place. |
| 🌍 **Portfolio** | Show your projects to employers! |
| 🔍 **Code review** | Teammates check your code before it's merged. |

### Create a repository on GitHub

1. Make a free account on `https://github.com`.
2. Click **+** (top right) → **New repository**.
3. Name it `my-diary`. Leave it **empty** (no README) for now. Click **Create repository**.

GitHub shows you the commands. They look like this:

```
git remote add origin https://github.com/sara-ahmed/my-diary.git
git push -u origin main
```

### 🔍 Line by line

| Command | Meaning |
|---|---|
| `git remote add origin <url>` | "Connect my local repo to this GitHub repo, and call it **`origin`**." (*origin* is the traditional name.) |
| `git push -u origin main` | "**Send** my `main` branch to `origin`." `-u` remembers this, so next time just `git push` is enough. |

The first time, Git asks you to **log in** to GitHub (a browser window opens). ✅

Refresh the GitHub page — your code is online! 🎉☁️

---

## 🔄 Part 13: Push, pull, clone

| Command | Direction | Meaning |
|---|---|---|
| `git push` | 💻 → ☁️ | **Send** your new commits to GitHub. |
| `git pull` | ☁️ → 💻 | **Get** new commits from GitHub (for example, from your teammates). |
| `git clone <url>` | ☁️ → 💻 | **Download** a whole repository for the first time. |

```
 Your computer 💻                            GitHub ☁️                       Teammate's computer 💻
 ┌──────────────┐     git push       ┌──────────────────┐     git pull     ┌──────────────┐
 │  local repo  │ ─────────────────► │   remote repo    │ ───────────────► │  local repo  │
 │              │ ◄───────────────── │    (origin)      │ ◄─────────────── │              │
 └──────────────┘     git pull       └──────────────────┘     git push     └──────────────┘
```

### Clone an existing project

```
git clone https://github.com/spring-projects/spring-petclinic.git
```

This downloads **Spring PetClinic** — a famous example Spring Boot app 🐶🐱 — with its **whole history**. Try it later! 😉

### 💼 A day of teamwork

```
git switch main
git pull                              # 1. get the newest code
git switch -c fix-login-bug           # 2. new branch for your work
# ... edit, test ...
git add .
git commit -m "Fix login when the email has capital letters"   # 3. commit
git push -u origin fix-login-bug      # 4. send the branch to GitHub
# 5. On GitHub: open a "Pull Request" → teammates review → merge into main ✅
```

A **Pull Request** (PR) is a request: "Please look at my branch and **pull** it into main." Teammates can comment, suggest changes, and approve. 👍 This is how almost **all** professional teams work.

---

## 🖱️ Part 14: Git in IntelliJ

You don't **have** to type commands. IntelliJ has excellent Git support!

| What | Where in IntelliJ |
|---|---|
| Start using Git | **VCS → Enable Version Control Integration → Git** (or **Git → Create Git Repository**) |
| See changed files | **Commit** window (left side, or **Alt + 0**) |
| Commit | **Ctrl + K** → check files → write message → **Commit** |
| Push | **Ctrl + Shift + K** |
| Pull | **Git → Pull...** |
| History | **Git** window at the bottom (**Alt + 9**) → **Log** tab |
| Branches | bottom-right corner: click the branch name (`main`) → New Branch / Checkout / Merge |
| See what changed in a file | right-click → **Git → Show Diff** |
| Who wrote this line? | right-click the line numbers → **Annotate with Git Blame** |
| Get a project from GitHub | **File → New → Project from Version Control** → paste the URL |

### 🎨 File colors in the Project window

| Color | Meaning |
|---|---|
| ⬜ white/normal | not changed |
| 🟦 blue | **modified** since the last commit |
| 🟩 green | **new**, added to Git |
| 🟥 red | **new**, not added to Git (untracked) |
| 🟫 gray/olive | **ignored** (in `.gitignore`) |

> 💡 **Learn both!** Use IntelliJ's buttons for daily work — but understand the commands, because you'll see them in documentation, in error messages, and in job interviews. 💼

---

## ✋ Try it yourself

**Task 1:** Set up Git (`user.name`, `user.email`). Create a folder `git-practice`, run `git init`, create a file `notes.txt` with one line, and make your first commit. Check with `git log --oneline`.

**Task 2:** Change `notes.txt` three times, with **one commit each time** and good messages. Then look at the history. Use `git diff` before each commit.

**Task 3:** Create a branch `new-idea`, add a file `idea.txt`, commit, switch back to `main` (the file disappears!), then merge `new-idea` into `main`.

**Task 4:** Create a **conflict on purpose**:
1. On `main`, change line 1 of `notes.txt` and commit.
2. Create a branch from the **previous** commit... (easier: create branch `b2` **before** step 1, change line 1 differently there, commit.)
3. Merge `b2` into `main`. Fix the conflict by hand. Commit.

**Task 5:** Put your `hello-maven` project (Chapter 40) into Git:
1. Check that `.gitignore` contains `target/` and `.idea/`.
2. `git init`, `git add .`, `git commit -m "First version of hello-maven"`.
3. Create a GitHub repository and push it. 🚀

**Task 6:** Which command?
1. See what changed (line by line) before committing
2. Throw away changes in a file
3. Send commits to GitHub
4. Download a project from GitHub
5. Create and switch to a new branch called `login`

<details>
<summary>Click to see the answers</summary>

1. `git diff`
2. `git restore <file>`
3. `git push`
4. `git clone <url>`
5. `git switch -c login`

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `git add`

```
git commit -m "Update"
```
```
nothing added to commit but untracked files present (use "git add" to track)
```

**Fix:** `git add .` first (or `git commit -am` for files Git already knows).

### Mistake 2: "Please tell me who you are"

```
*** Please tell me who you are.
Run
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
```

**Fix:** Do Part 2's setup.

### Mistake 3: Committing `target/`, `.idea/` or secrets

**Fix:** Add a `.gitignore` **before** the first commit. For already-committed files: `git rm -r --cached target` + commit.

### Mistake 4: "Your local changes would be overwritten"

```
error: Your local changes to the following files would be overwritten by checkout
```

You tried to switch branches with uncommitted changes. **Fix:** Commit them first (or `git stash` to put them aside temporarily, and `git stash pop` to get them back).

### Mistake 5: Push rejected

```
! [rejected]        main -> main (fetch first)
hint: Updates were rejected because the remote contains work that you do not have locally.
```

Someone pushed before you. **Fix:** `git pull` first, fix any conflicts, then `git push`.

### Mistake 6: Leaving conflict markers in the code

Code with `<<<<<<<` and `>>>>>>>` won't compile! **Fix:** Search for `<<<<<<<` and remove **all** markers.

### Mistake 7: "LF will be replaced by CRLF" warnings on Windows

```
warning: in the working copy of 'Hello.java', LF will be replaced by CRLF the next time Git touches it
```

This is just about invisible **line-ending** characters (Windows and Mac/Linux use different ones). It's **harmless** — you can ignore it. 😊

---

## ✅ Summary

- **Git** saves the **history** of your project: every change, who made it, when, and why. 🎮💾
- Setup once: `git config --global user.name / user.email`.
- **3 places:** working folder → (`git add`) → staging area → (`git commit`) → repository.
- Daily: `git status` 🔍, `git diff` 🔎, `git add .` 📋, `git commit -m "..."` 📸, `git log --oneline` 📜.
- Undo: `git restore <file>`, `git restore --staged <file>`, `git revert <hash>`.
- **`.gitignore`**: never commit `target/`, `.idea/`, passwords. 🙈
- **Branches**: `git switch -c name`, `git merge name`. Keep `main` working. 🌿
- **Conflicts**: edit the file, remove `<<<<<<<` `=======` `>>>>>>>`, `git add`, `git commit`.
- **GitHub**: `git remote add origin <url>`, `git push`, `git pull`, `git clone`. Teams use **Pull Requests**. ☁️
- IntelliJ: **Ctrl + K** (commit), **Ctrl + Shift + K** (push), branch name in the bottom-right corner.

---

## ❓ Quiz

1. What is a commit?
2. What are the 3 places in Git?
3. Which command shows the current situation (changed files, branch...)?
4. What's the difference between `git add` and `git commit`?
5. What is a branch? Why use one?
6. What should go into `.gitignore` in a Maven project?
7. What do `<<<<<<<`, `=======` and `>>>>>>>` mean in a file?
8. What's the difference between `git push` and `git pull`?
9. What is a Pull Request?

<details>
<summary>Click to see the answers</summary>

1. A saved snapshot of the project at one moment, with a message, author and date.
2. Working folder, staging area, repository.
3. `git status`
4. `git add` puts changes in the staging area. `git commit` saves the staged changes as a snapshot in the history.
5. A separate line of work. To try ideas or build features safely without breaking `main`.
6. `target/`, `.idea/`, `*.iml`, `*.class`, log files, and secrets like `.env`.
7. Conflict markers: the start of your version, the separator, and the end of the other branch's version.
8. `push` sends your commits to GitHub; `pull` gets new commits from GitHub.
9. A request on GitHub to merge your branch into main, so teammates can review it first.

</details>

---

## 🎉 Part 5 complete!

You now know the **tools** every professional Java developer uses:

- ✅ **Maven** — libraries and builds
- ✅ **pom.xml** — your project's ID card
- ✅ **Git** and **GitHub** — history, branches, teamwork

In **Part 6**, we learn **how the web works**: clients and servers, HTTP, JSON and REST APIs. This is the **world** that Spring Boot lives in. Then — finally — **Spring Boot**! 🌱🚀

---

[⬅ Previous chapter](41-pom-xml.md) | [Table of Contents](../README.md) | [Next chapter: Client and server ➡](../part-06-web/43-client-and-server.md)
