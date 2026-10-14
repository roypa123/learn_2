# Chapter 95 – Final project: Library app – planning

[⬅ Previous chapter](../part-12-extras/94-actuator.md) | [Table of Contents](../README.md) | [Next chapter ➡](96-library-building.md)

---

## 🎯 Goal

This is it — the **final project**! 🎆 You'll build a **whole new app**, from an empty folder to a finished, tested, secured API: a **Library app** 📚.

But real programmers don't start by typing code. They start by **thinking** and **planning**. 🤔📝 A good plan makes the building fast — a missing plan makes it messy. Today: **only planning**, no Java at all!

At the end of this chapter you will have:

- A list of **what** the app must do (the **requirements**) 📋
- The **users** and their **roles** 🎭
- The **data**: tables and their relationships 🗄️
- The **business rules** — the "laws" of our library ⚖️
- A list of all **endpoints** 🌐
- The **package structure** 📁
- A **building plan** for the next two chapters 🗺️

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Requirement** | Something the app **must** do. "Members must be able to borrow books." ✅ |
| **User story** | A requirement written from a user's view: "**As a** member, **I want** to borrow a book, **so that** I can read it at home." 📖 |
| **Business rule** | A "law" of the real world that the app must follow: "Nobody may borrow more than 3 books at once." ⚖️ |
| **Domain** | The "world" your app is about — here: books, members, loans. 🌍 |
| **Loan** | Borrowing a book: **who** took **which** book, **when**, and **until when**. 📅 |
| **Overdue** | A book that should have been returned already, but wasn't. ⏰😬 |
| **Copy** | One **physical** book. A library can have 3 copies of "The Hobbit". 📚📚📚 |

---

## 📖 Story: The architect's drawing 🏗️

Before builders start on a house, the **architect** draws a plan: how many rooms, where the doors go, where the water pipes run. 📐

Building **without** a plan? You'd put the bathroom in the middle of the kitchen 🚽🍳, and halfway through, you'd notice there's no door to the garden. Tearing down walls is **expensive**! 💸

In software it's the same: changing a **plan** costs a pencil and an eraser ✏️. Changing **finished code** costs hours. So today, we are the **architects**. 👷

---

## 📋 Part 1: What must the app do?

Our school wants a library app. We talked to the school librarian, Mrs. Novak 👩‍🏫, and wrote down her wishes as **user stories**:

**As a visitor** (not logged in) 😶:

1. I want to **see all books** and **search** them by title, so that I know what the library has.
2. I want to **register**, so that I can borrow books.

**As a member** (a student) 🧒:

3. I want to **log in** and get a token.
4. I want to **borrow** a book, if a copy is free.
5. I want to **return** a book.
6. I want to see **my loans** (what I borrowed, and until when).

**As a librarian** 👩‍🏫:

7. I want to **add**, **change** and **delete** books.
8. I want to see **all overdue** loans, so that I can remind people.
9. I want to **return** a book **for** a member (when they bring it to my desk).

✋ **Not** in our first version (maybe later!): fines for late books 💰, reservations, emails, book covers. Saying **"not now"** is an important part of planning — otherwise a project never ends! 😅

---

## 🎭 Part 2: The users and their roles

| Role | Who | What they may do |
|---|---|---|
| (none) 😶 | Visitors | Read and search books, register, log in |
| `MEMBER` 🧒 | Students | + borrow, return their **own** loans, see their **own** loans |
| `LIBRARIAN` 👩‍🏫 | Mrs. Novak | + manage books, see overdue loans, return **any** loan |

Everyone who **registers** becomes a `MEMBER`. The first `LIBRARIAN` is made by the app at start, with a password from **outside** the code (like our admin in Chapter 82). 🔑

---

## 🗄️ Part 3: The data

What "things" does our library have? Look at the **nouns** in the user stories: **book**, **member**, **loan**. 🔍

```
 ┌──────────────────┐         ┌──────────────────────┐         ┌──────────────────┐
 │ books            │         │ loans                │         │ app_users        │
 ├──────────────────┤         ├──────────────────────┤         ├──────────────────┤
 │ id          PK   │◄────────│ book_id      FK      │         │ id          PK   │
 │ title            │  1    * │ member_id    FK      │────────►│ username (unique)│
 │ author           │         │ id           PK      │  *    1 │ password (hash)  │
 │ isbn    (unique) │         │ borrowed_on          │         │ role             │
 │ published_year   │         │ due_on               │         └──────────────────┘
 │ total_copies     │         │ returned_on (or null)│
 │ available_copies │         └──────────────────────┘
 └──────────────────┘
```

| Table | One row is... | Notes |
|---|---|---|
| `books` 📚 | one **title** (with all its copies) | `isbn` is the book's world-wide number (every book has one!) — unique. `available_copies` goes **down** when someone borrows, **up** when they return. |
| `app_users` 👤 | one person | Exactly like our school app (Chapter 81). `user` is reserved! |
| `loans` 📅 | one borrowing | Links **one** book and **one** member. `returned_on` is **empty** (`null`) while the book is still out. |

The relationships (Chapter 75):

- One book has **many** loans (over time). Each loan is for **one** book. → **Many-to-one** from `Loan` to `Book`.
- One member has **many** loans. Each loan belongs to **one** member. → **Many-to-one** from `Loan` to `AppUser`.

💡 Why keep old loans instead of deleting them when a book comes back? Because then we have a **history**: "Who borrowed this book last?", "How many books did Sara read this year?" 📈 We just fill in `returned_on`.

🤔 Why `published_year` and not `year`? Remember Chapter 68: `YEAR` is a **reserved word** in H2! 🙅

---

## ⚖️ Part 4: The business rules

These are the **laws** of our library. They're the most important part of the plan — and the most important part to **test** later! 🧪

| # | Rule | If broken |
|---|---|---|
| R1 | A loan lasts **14 days**. `due_on` = `borrowed_on` + 14. | — |
| R2 | You can only borrow a book if `available_copies` > 0. | **409** "No copies left" |
| R3 | A member may have at most **3** active loans (not yet returned). | **409** "Loan limit reached" |
| R4 | Only the member **who borrowed** a book (or a librarian) may return it. | **403** |
| R5 | A loan can only be returned **once**. | **409** "Already returned" |
| R6 | A loan is **overdue** if it's not returned and today is **after** `due_on`. | — |
| R7 | Two books can't have the same ISBN. | **409** "ISBN already used" |
| R8 | A book can only be deleted when **no** copy is borrowed right now. | **409** "Book is still borrowed" |
| R9 | `available_copies` is never below 0 and never above `total_copies`. | — |

⭐ The numbers **14** and **3** might change one day ("Mrs. Novak says 21 days in the summer!"). So they go into **settings**, not into the code:

```properties
library.loan.days=14
library.loan.max-active=3
```

---

## 🌐 Part 5: The endpoints

| Method | URL | Who | What | Success |
|---|---|---|---|---|
| `POST` | `/api/auth/register` | everyone | Register as `MEMBER` | 201 |
| `POST` | `/api/auth/login` | everyone | Get a token | 200 |
| `GET` | `/api/auth/me` | logged in | Who am I? | 200 |
| `GET` | `/api/books?search=hob` | everyone | All books (optional search) | 200 |
| `GET` | `/api/books/{id}` | everyone | One book | 200 |
| `POST` | `/api/books` | `LIBRARIAN` | Add a book | 201 |
| `PUT` | `/api/books/{id}` | `LIBRARIAN` | Change a book | 200 |
| `DELETE` | `/api/books/{id}` | `LIBRARIAN` | Delete a book (R8) | 204 |
| `POST` | `/api/loans` `{"bookId":1}` | `MEMBER` | Borrow a book (R1–R3) | 201 |
| `GET` | `/api/loans/mine` | `MEMBER` | My loans | 200 |
| `PUT` | `/api/loans/{id}/return` | `MEMBER` (own) or `LIBRARIAN` | Return (R4, R5) | 200 |
| `GET` | `/api/loans/overdue` | `LIBRARIAN` | All overdue loans (R6) | 200 |

And from Part 12: `GET /actuator/health` for everyone. 🩺

### 📦 What does a loan look like as JSON?

```json
{
  "id": 7,
  "bookId": 2,
  "bookTitle": "The Hobbit",
  "member": "sara",
  "borrowedOn": "2026-10-14",
  "dueOn": "2026-10-28",
  "returnedOn": null,
  "overdue": false
}
```

Notice: **no** passwords, **no** whole `AppUser` or `Book` objects — a flat, friendly **DTO** (Chapter 64). And `overdue` is **calculated**, not stored.

---

## 📁 Part 6: The package structure

The same layers as our school app (Chapter 63):

```
 com.example.library
 ├── LibraryApplication.java
 ├── config        SecurityConfig, JwtConfig, ClockConfig
 ├── controller    AuthController, BookController, LoanController
 ├── dto           BookRequest, BookResponse, LoanRequest, LoanResponse, ...
 ├── entity        Book, Loan, AppUser
 ├── exception     BookNotFoundException, NoCopiesLeftException, ..., GlobalExceptionHandler
 ├── repository    BookRepository, LoanRepository, AppUserRepository
 ├── security      LibraryUserDetailsService, TokenService, DataLoader
 └── service       BookService, LoanService, UserService
```

### ⏰ A special helper: the `Clock`

Rules R1 and R6 depend on **today's date**. But how do you **test** "this loan is overdue"? You can't wait 15 days! 😅

The trick: our code never asks `LocalDate.now()` directly. Instead, it asks a **`Clock`** bean: `LocalDate.now(clock)`. In the real app, the clock is the real time. In **tests**, we give it a **fixed** clock — "today is 1 March" — and we can travel in time! ⏰🚀 (You'll see it in Chapter 97.)

---

## 🗺️ Part 7: The building plan

We'll build in **small steps**, and test after each one:

| Step | Chapter | What |
|---|---|---|
| 1 | 96 | Create the project with Spring Initializr |
| 2 | 96 | Entities and repositories: `Book`, `Loan`, `AppUser` |
| 3 | 96 | DTOs, exceptions, `GlobalExceptionHandler` |
| 4 | 96 | `BookService` + `BookController` → test with curl 📚 |
| 5 | 96 | `LoanService` with **all** the business rules ⚖️ |
| 6 | 97 | Security: users, BCrypt, JWT, roles 🔐 |
| 7 | 97 | `LoanController` + the first librarian and some books |
| 8 | 97 | Tests: rules (Mockito + `Clock`), controller, the whole story 🧪 |
| 9 | 98–100 | `.jar`, Docker, the internet 🌍 |

### 🛠️ The Initializr settings (for Chapter 96)

| Setting | Value |
|---|---|
| Project | **Maven** |
| Language | **Java** |
| Spring Boot | **4.1.x** (the newest 4.x) |
| Group | `com.example` |
| Artifact | `library` |
| Java | **25** |
| Dependencies | **Spring Web**, **Validation**, **Spring Data JPA**, **H2 Database**, **Spring Security**, **OAuth2 Resource Server**, **Spring Boot Actuator** |

---

## 💻 Mini project: Plan a "reservation" feature 📝

Mrs. Novak asks: "When all copies of a book are out, can a member **reserve** it, so they get it next?" Plan it — **no code**, just like we did today:

1. Write the **user story**.
2. What new **table** do you need? Which columns?
3. Write at least **three business rules**.
4. Which **endpoints** would you add?

<details>
<summary>Click to see one possible answer</summary>

1. **As a** member, **I want** to reserve a book that has no free copies, **so that** I get it as soon as someone returns it.
2. A table **`reservations`**: `id`, `book_id` (FK), `member_id` (FK), `reserved_at` (date and time — the **order** matters!), `status` (`WAITING`, `READY`, `DONE`, `CANCELLED`).
3. Rules, for example:
   - You can only reserve a book that has **0** free copies (otherwise, just borrow it!).
   - A member can't reserve the **same** book twice.
   - When a copy comes back, the **oldest** waiting reservation becomes `READY`, and the copy is kept for that member for **3 days**.
   - A `READY` reservation that isn't picked up in 3 days becomes `CANCELLED`, and the next person's turn comes. (A **scheduled job**, Chapter 91! ⏰)
4. `POST /api/reservations` `{"bookId":1}`, `GET /api/reservations/mine`, `DELETE /api/reservations/{id}` (cancel), and for librarians `GET /api/reservations?bookId=1`.

There's no single "right" answer — but if you thought about the **order**, about **what happens when a book comes back**, and about **time limits**, you planned like a real developer. 🏆

</details>

---

## ✋ Try it yourself

1. Find the **nouns** and **verbs** in this story: "A member borrows a book. The librarian sees which loans are overdue." Which become **tables**, which become **endpoints**?
2. Why do we store `available_copies` in `books`, instead of counting the active loans every time?
3. Why does `PUT /api/loans/{id}/return` answer **403** (and not 404) when Tom tries to return Sara's loan?

<details>
<summary>Click to see the answers</summary>

1. Nouns: member, book, librarian, loan → tables (`app_users`, `books`, `loans`; "librarian" is a **role**, not a table). Verbs: borrows, sees → endpoints (`POST /api/loans`, `GET /api/loans/overdue`).
2. It's faster and simpler to read (one column instead of a count query every time). The price: we must keep it **correct** when borrowing and returning — that's what rule R9 and **transactions** (Chapter 79) are for. (Counting every time would also be a fine choice — both are OK designs!)
3. The loan **exists**, but Tom may not touch it — that's "I know you, but no" = **403** (Chapter 80). (Some apps answer 404 on purpose, so strangers can't even learn that the loan exists. Both are used in real life; we pick 403 because it's clearer for learning.)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Starting to code without a plan

You'll build the wrong thing, or the right thing the wrong way — and tear it down later. 🏚️ **Fix:** User stories, tables, rules, endpoints — **first**.

### Mistake 2: Planning too much

A 200-page plan that's never finished is as bad as no plan. **Fix:** Plan the **first version** well, write "not now" for the rest.

### Mistake 3: Forgetting the "unhappy paths"

"Borrow a book" is easy. But **what if** there's no copy? **What if** the member has 3 books? **Fix:** For every action, ask: "What can go wrong?" — and write it as a rule with a status code.

### Mistake 4: Magic numbers in the code

`if (activeLoans >= 3)` — what's 3? And who changes it next summer? **Fix:** Settings with clear names: `library.loan.max-active=3`.

---

## ✅ Summary

- **Plan before you build** 🏗️: changing a plan is cheap, changing code is expensive.
- **User stories**: "As a ..., I want ..., so that ...".
- **Roles**: visitors, `MEMBER`, `LIBRARIAN`.
- **Tables**: `books`, `app_users`, `loans` (two many-to-one relationships).
- **Business rules** ⚖️ R1–R9, each with its status code when broken. Numbers like 14 days and 3 loans go into **settings**.
- **Endpoints** table, **packages** like the school app, and a **`Clock`** bean to make dates testable ⏰.
- A **step-by-step building plan** — build a little, test a little.

---

## ❓ Quiz

1. Write a user story for "a librarian deletes a book".
2. Why do we keep loans after a book is returned?
3. Which rule stops a member from borrowing a fourth book, and which status code do they get?
4. What does `returned_on = null` mean?
5. Why do we put `14` and `3` into `application.properties`?
6. Why will our code use a `Clock` instead of `LocalDate.now()`?

<details>
<summary>Click to see the answers</summary>

1. "As a librarian, I want to delete a book, so that books we no longer have don't show up in the list."
2. To keep a history (who borrowed what and when).
3. Rule R3 (at most 3 active loans) → **409** "Loan limit reached".
4. The book of this loan hasn't been returned yet — the loan is still active.
5. So they can change without changing (and rebuilding) the code.
6. So tests can use a fixed, fake date and check time rules like "overdue" without waiting.

</details>

---

[⬅ Previous chapter](../part-12-extras/94-actuator.md) | [Table of Contents](../README.md) | [Next chapter: Final project: Library app – building ➡](96-library-building.md)
