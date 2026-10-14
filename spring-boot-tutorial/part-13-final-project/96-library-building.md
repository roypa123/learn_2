# Chapter 96 – Final project: Library app – building

[⬅ Previous chapter](95-library-planning.md) | [Table of Contents](../README.md) | [Next chapter ➡](97-library-security-tests.md)

---

## 🎯 Goal

Time to build! 🏗️ We follow the plan from Chapter 95, step by step. You've seen **every** tool before — today you'll put them together **on your own**, in a fresh project.

At the end of this chapter you will have:

- A new project **`library`** ✨
- The entities **`Book`**, **`AppUser`** and **`Loan`**, with their repositories 🗄️
- Clean **DTOs** and a smart **exception** family 🧯
- A working **Book API** 📚 (tested with curl)
- A **`LoanService`** with **all** the business rules from the plan ⚖️

💡 This chapter is **long** and has **lots** of code — that's normal for a real project! Take breaks. ☕ Each part ends with something that **works**.

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Domain logic** | The code that follows the business rules (borrow, return, limits...). ⚖️ |
| **Exception family** | Several exceptions with **one** common parent class, so **one** handler can treat them all. 👨‍👩‍👧‍👦 |
| **`Clock`** | A Java object that tells the time. Our code asks **it**, instead of asking the computer directly — so tests can use a **fake** clock. ⏰ |
| **Derived delete** | A repository method like `deleteByBookId(...)` that Spring writes for you (Chapter 74). |

---

## 🛠️ Part 1: Create the project

Go to **https://start.spring.io** (Chapter 49) and use the settings from Chapter 95:

| Setting | Value |
|---|---|
| Project / Language | Maven / Java |
| Spring Boot | the newest **4.1.x** |
| Group / Artifact | `com.example` / `library` |
| Java | **25** |
| Dependencies | Spring Web, Validation, Spring Data JPA, H2 Database, Spring Security, OAuth2 Resource Server, Spring Boot Actuator |

**Generate**, unzip, open in IntelliJ (Chapter 49). 🎉

### ⚙️ Settings

Replace **`src/main/resources/application.properties`** with:

```properties
spring.application.name=library

# The database: a file in the folder "data"
spring.datasource.url=jdbc:h2:file:./data/library
spring.datasource.username=sa
spring.datasource.password=

# JPA / Hibernate
spring.jpa.hibernate.ddl-auto=update
spring.jpa.open-in-view=false

# The library's rules (Chapter 95)
library.loan.days=14
library.loan.max-active=3
```

Every line is an old friend: the file database (Chapter 73), `ddl-auto=update` (Chapter 73), no open-in-view (Chapter 75), and our **own** settings for the rules (Chapter 55).

### 🚪 A temporary open door

Spring Security is in the project → **everything** is locked (Chapter 80). We'll lock things **properly** in Chapter 97. For now, while we build, we open the door:

**`config/SecurityConfig.java`**

```java
package com.example.library.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    // ⚠️ TEMPORARY: everything is open while we build. Chapter 97 locks it!
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth.anyRequest().permitAll());
        return http.build();
    }
}
```

⚠️ The comment is important: a door that's open "for now" is easy to **forget**. 😬

### ⏰ The clock

**`config/ClockConfig.java`**

```java
package com.example.library.config;

import java.time.Clock;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ClockConfig {

    @Bean
    public Clock clock() {
        return Clock.systemDefaultZone();
    }
}
```

| Code | Meaning |
|---|---|
| `Clock.systemDefaultZone()` | The **real** clock of the computer, in its time zone. In tests, we'll use a **fixed** clock instead (Chapter 97). ⏰ |

---

## 🗄️ Part 2: The entities

### 📚 `Book`

**`entity/Book.java`**

```java
package com.example.library.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "books")
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String title;

    @Column(nullable = false, length = 100)
    private String author;

    @Column(nullable = false, unique = true, length = 20)
    private String isbn;

    private int publishedYear;

    private int totalCopies;

    private int availableCopies;

    protected Book() {
    }

    public Book(String title, String author, String isbn, int publishedYear, int totalCopies) {
        this.title = title;
        this.author = author;
        this.isbn = isbn;
        this.publishedYear = publishedYear;
        this.totalCopies = totalCopies;
        this.availableCopies = totalCopies;
    }

    public void update(String title, String author, String isbn, int publishedYear, int totalCopies) {
        int borrowed = getBorrowedCopies();
        this.title = title;
        this.author = author;
        this.isbn = isbn;
        this.publishedYear = publishedYear;
        this.totalCopies = totalCopies;
        this.availableCopies = totalCopies - borrowed;
    }

    public void borrowOneCopy() {
        if (availableCopies == 0) {
            throw new IllegalStateException("No copies left of " + title);
        }
        availableCopies--;
    }

    public void returnOneCopy() {
        if (availableCopies == totalCopies) {
            throw new IllegalStateException("All copies of " + title + " are already here");
        }
        availableCopies++;
    }

    public int getBorrowedCopies() {
        return totalCopies - availableCopies;
    }

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getAuthor() {
        return author;
    }

    public String getIsbn() {
        return isbn;
    }

    public int getPublishedYear() {
        return publishedYear;
    }

    public int getTotalCopies() {
        return totalCopies;
    }

    public int getAvailableCopies() {
        return availableCopies;
    }
}
```

| Code | Meaning |
|---|---|
| `this.availableCopies = totalCopies;` | A new book: **all** copies are on the shelf. |
| `update(...)` | Change everything at once. ⭐ The **borrowed** copies stay borrowed: 5 copies with 2 out → change to 6 → **4** available. |
| `borrowOneCopy()` / `returnOneCopy()` | ⭐ The **only** ways to change `availableCopies`. They guard rule **R9** (never below 0, never above the total) — a last safety net. If something is wrong, they throw. |
| `getBorrowedCopies()` | Calculated, not stored. |
| No setters! | ⭐ Nobody can write `book.setAvailableCopies(-5)`. The entity **protects itself** (encapsulation, Chapter 21). 🛡️ |

### 👤 `AppUser`

Exactly like the school app (Chapter 81) — copy it into **`entity/AppUser.java`** with the new package name:

```java
package com.example.library.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "app_users")
public class AppUser {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 30)
    private String username;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false, length = 20)
    private String role;

    protected AppUser() {
    }

    public AppUser(String username, String password, String role) {
        this.username = username;
        this.password = password;
        this.role = role;
    }

    public Long getId() {
        return id;
    }

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }

    public String getRole() {
        return role;
    }
}
```

### 📅 `Loan`

**`entity/Loan.java`**

```java
package com.example.library.entity;

import java.time.LocalDate;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "loans")
public class Loan {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "book_id", nullable = false)
    private Book book;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "member_id", nullable = false)
    private AppUser member;

    @Column(nullable = false)
    private LocalDate borrowedOn;

    @Column(nullable = false)
    private LocalDate dueOn;

    private LocalDate returnedOn;

    protected Loan() {
    }

    public Loan(Book book, AppUser member, LocalDate borrowedOn, LocalDate dueOn) {
        this.book = book;
        this.member = member;
        this.borrowedOn = borrowedOn;
        this.dueOn = dueOn;
    }

    public boolean isReturned() {
        return returnedOn != null;
    }

    public boolean isOverdue(LocalDate today) {
        return !isReturned() && today.isAfter(dueOn);
    }

    public void markReturned(LocalDate today) {
        this.returnedOn = today;
    }

    public Long getId() {
        return id;
    }

    public Book getBook() {
        return book;
    }

    public AppUser getMember() {
        return member;
    }

    public LocalDate getBorrowedOn() {
        return borrowedOn;
    }

    public LocalDate getDueOn() {
        return dueOn;
    }

    public LocalDate getReturnedOn() {
        return returnedOn;
    }
}
```

| Code | Meaning |
|---|---|
| `@ManyToOne(fetch = FetchType.LAZY, optional = false)` | Many loans → one book (Chapter 75). `LAZY`: load the book only when needed. `optional = false`: a loan **always** has a book. |
| `@JoinColumn(name = "member_id", nullable = false)` | The foreign key column. We call it `member_id` (not `app_user_id`) because that's what it **means**. |
| `LocalDate` | A date without a time: `2026-10-14` (Chapter 39). |
| `returnedOn` (no `@Column(nullable = false)`) | May be `null` = "not returned yet". |
| `isOverdue(LocalDate today)` | ⭐ Rule **R6**. Notice: **today** comes in as a parameter — the entity never asks the computer's clock. Easy to test! |
| `today.isAfter(dueOn)` | `true` only if today is **later** than the due date. On the due date itself, it's not overdue yet. |

---

## 🔎 Part 3: The repositories

**`repository/BookRepository.java`**

```java
package com.example.library.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.library.entity.Book;

public interface BookRepository extends JpaRepository<Book, Long> {

    List<Book> findAllByOrderByTitle();

    List<Book> findByTitleContainingIgnoreCaseOrderByTitle(String text);

    boolean existsByIsbn(String isbn);

    boolean existsByIsbnAndIdNot(String isbn, Long id);
}
```

**`repository/AppUserRepository.java`**

```java
package com.example.library.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.library.entity.AppUser;

public interface AppUserRepository extends JpaRepository<AppUser, Long> {

    Optional<AppUser> findByUsername(String username);

    boolean existsByUsername(String username);
}
```

**`repository/LoanRepository.java`**

```java
package com.example.library.repository;

import java.time.LocalDate;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.library.entity.Loan;

public interface LoanRepository extends JpaRepository<Loan, Long> {

    long countByMemberUsernameAndReturnedOnIsNull(String username);

    List<Loan> findByMemberUsernameOrderByBorrowedOnDesc(String username);

    List<Loan> findByReturnedOnIsNullAndDueOnBeforeOrderByDueOn(LocalDate date);

    void deleteByBookId(Long bookId);
}
```

Read the method names like sentences (Chapter 74): 🗣️

| Method | Means |
|---|---|
| `findAllByOrderByTitle()` | All books, sorted by title. |
| `existsByIsbnAndIdNot(isbn, id)` | "Is there **another** book (not this id) with this ISBN?" — for updates (rule R7). |
| `countByMemberUsernameAndReturnedOnIsNull(username)` | ⭐ "How many loans does **this member** have that are **not returned**?" → rule R3. `MemberUsername` walks **through** the relationship: `loan.member.username`! |
| `findByMemberUsernameOrderByBorrowedOnDesc(username)` | A member's loans, newest first. |
| `findByReturnedOnIsNullAndDueOnBeforeOrderByDueOn(date)` | ⭐ Not returned **and** due **before** today → **overdue** (R6), the most overdue first. |
| `deleteByBookId(bookId)` | Delete all loans of a book (we'll need it for deleting books). |

---

## 🧯 Part 4: DTOs and an exception family

### 📦 DTOs

**`dto/BookRequest.java`**

```java
package com.example.library.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

public record BookRequest(
        @NotBlank(message = "Title is required")
        @Size(max = 100, message = "Title can have at most 100 characters")
        String title,

        @NotBlank(message = "Author is required")
        @Size(max = 100, message = "Author can have at most 100 characters")
        String author,

        @NotBlank(message = "ISBN is required")
        @Pattern(regexp = "[0-9-]{10,17}", message = "ISBN must have 10 to 17 digits or dashes")
        String isbn,

        @NotNull(message = "Published year is required")
        @Min(value = 1450, message = "Published year must be 1450 or later")
        @Max(value = 2100, message = "Published year must be 2100 or earlier")
        Integer publishedYear,

        @NotNull(message = "Total copies is required")
        @Min(value = 1, message = "A book needs at least 1 copy")
        @Max(value = 100, message = "A book can have at most 100 copies")
        Integer totalCopies) {
}
```

| Code | Meaning |
|---|---|
| `@Pattern(regexp = "[0-9-]{10,17}", ...)` | Only digits and dashes, 10 to 17 of them — like `978-0-261-10221-7`. |
| `@Min(1450)` | The printing press was invented around 1450 — no printed books before that! 📜 |

**`dto/BookResponse.java`**

```java
package com.example.library.dto;

import com.example.library.entity.Book;

public record BookResponse(Long id, String title, String author, String isbn, int publishedYear,
                           int totalCopies, int availableCopies) {

    public static BookResponse from(Book book) {
        return new BookResponse(book.getId(), book.getTitle(), book.getAuthor(), book.getIsbn(),
                book.getPublishedYear(), book.getTotalCopies(), book.getAvailableCopies());
    }
}
```

**`dto/LoanRequest.java`**

```java
package com.example.library.dto;

import jakarta.validation.constraints.NotNull;

public record LoanRequest(
        @NotNull(message = "Book id is required")
        Long bookId) {
}
```

**`dto/LoanResponse.java`**

```java
package com.example.library.dto;

import java.time.LocalDate;

import com.example.library.entity.Loan;

public record LoanResponse(Long id, Long bookId, String bookTitle, String member, LocalDate borrowedOn,
                           LocalDate dueOn, LocalDate returnedOn, boolean overdue) {

    public static LoanResponse from(Loan loan, LocalDate today) {
        return new LoanResponse(loan.getId(), loan.getBook().getId(), loan.getBook().getTitle(),
                loan.getMember().getUsername(), loan.getBorrowedOn(), loan.getDueOn(),
                loan.getReturnedOn(), loan.isOverdue(today));
    }
}
```

| Code | Meaning |
|---|---|
| `from(Loan loan, LocalDate today)` | ⭐ Needs **today** to calculate `overdue`. |
| `loan.getBook().getTitle()` | The book is `LAZY` — this loads it. So `from` must be called **inside** a transaction (in the service), never in the controller (Chapter 75's lazy-loading error!). |

### 👨‍👩‍👧‍👦 The exception family

The plan has **nine** ways for things to go wrong. In the school app, every exception had its **own** handler method — lots of copy-paste. 😩 Let's be smarter: **one** parent class that **knows** its status code and title.

**`exception/LibraryException.java`**

```java
package com.example.library.exception;

import org.springframework.http.HttpStatus;

public abstract class LibraryException extends RuntimeException {

    private final HttpStatus status;
    private final String title;

    protected LibraryException(HttpStatus status, String title, String message) {
        super(message);
        this.status = status;
        this.title = title;
    }

    public HttpStatus getStatus() {
        return status;
    }

    public String getTitle() {
        return title;
    }
}
```

| Code | Meaning |
|---|---|
| `abstract class` | Nobody throws a plain `LibraryException` — only its **children** (Chapter 24). |
| `HttpStatus status`, `String title` | ⭐ Every child **carries** its own status and title. |

Now each child is **tiny**:

**`exception/BookNotFoundException.java`**

```java
package com.example.library.exception;

import org.springframework.http.HttpStatus;

public class BookNotFoundException extends LibraryException {

    public BookNotFoundException(Long id) {
        super(HttpStatus.NOT_FOUND, "Book not found", "Book with id " + id + " was not found");
    }
}
```

Make the others the same way — each in its own file in `exception`:

| Class | Constructor | Status | Title | Message |
|---|---|---|---|---|
| `LoanNotFoundException` | `(Long id)` | `NOT_FOUND` | `"Loan not found"` | `"Loan with id " + id + " was not found"` |
| `IsbnAlreadyUsedException` | `(String isbn)` | `CONFLICT` | `"ISBN already used"` | `"Another book already has the ISBN " + isbn` |
| `InvalidBookException` | `(String message)` | `BAD_REQUEST` | `"Invalid book"` | `message` |
| `BookStillBorrowedException` | `(String title)` | `CONFLICT` | `"Book is still borrowed"` | `"Some copies of " + title + " are still borrowed"` |
| `NoCopiesLeftException` | `(String title)` | `CONFLICT` | `"No copies left"` | `"All copies of " + title + " are borrowed right now"` |
| `LoanLimitReachedException` | `(int max)` | `CONFLICT` | `"Loan limit reached"` | `"You already have " + max + " books. Please return one first."` |
| `LoanAlreadyReturnedException` | `(Long id)` | `CONFLICT` | `"Already returned"` | `"Loan " + id + " was already returned"` |
| `NotYourLoanException` | `(Long id)` | `FORBIDDEN` | `"Not your loan"` | `"Loan " + id + " belongs to another member"` |

For example, **`NoCopiesLeftException.java`**:

```java
package com.example.library.exception;

import org.springframework.http.HttpStatus;

public class NoCopiesLeftException extends LibraryException {

    public NoCopiesLeftException(String title) {
        super(HttpStatus.CONFLICT, "No copies left", "All copies of " + title + " are borrowed right now");
    }
}
```

And the handler — **one** method for the whole family:

**`exception/GlobalExceptionHandler.java`**

```java
package com.example.library.exception;

import java.util.Map;
import java.util.TreeMap;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ProblemDetail;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(LibraryException.class)
    public ProblemDetail handleLibraryException(LibraryException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(ex.getStatus(), ex.getMessage());
        problem.setTitle(ex.getTitle());
        return problem;
    }

    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(MethodArgumentNotValidException ex,
            HttpHeaders headers, HttpStatusCode status, WebRequest request) {
        Map<String, String> errors = new TreeMap<>();
        for (FieldError fieldError : ex.getBindingResult().getFieldErrors()) {
            errors.put(fieldError.getField(), fieldError.getDefaultMessage());
        }
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST,
                "The request has " + errors.size() + " invalid field(s)");
        problem.setTitle("Invalid data");
        problem.setProperty("errors", errors);
        return ResponseEntity.badRequest().body(problem);
    }

    @ExceptionHandler(Exception.class)
    public ProblemDetail handleEverythingElse(Exception ex) {
        logger.error("Unexpected error", ex);
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.INTERNAL_SERVER_ERROR,
                "Something went wrong on our side. Please try again later.");
        problem.setTitle("Server error");
        return problem;
    }
}
```

| Code | Meaning |
|---|---|
| `@ExceptionHandler(LibraryException.class)` | ⭐ Catches **every** child: `BookNotFoundException`, `NoCopiesLeftException`... (Chapter 23: a child **is** a parent!) |
| `ex.getStatus()`, `ex.getTitle()` | Each exception tells the handler **its own** status and title. 🎯 |
| the other two methods | Exactly like the school app (Chapter 66). |

Nine exceptions, **one** handler method. Adding a tenth one later? Just a tiny new class — the handler **doesn't change**. 🎉 (This is polymorphism — Chapter 23 — doing real work!)

---

## 📚 Part 5: The Book API

**`service/BookService.java`**

```java
package com.example.library.service;

import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.library.dto.BookRequest;
import com.example.library.dto.BookResponse;
import com.example.library.entity.Book;
import com.example.library.exception.BookNotFoundException;
import com.example.library.exception.BookStillBorrowedException;
import com.example.library.exception.InvalidBookException;
import com.example.library.exception.IsbnAlreadyUsedException;
import com.example.library.repository.BookRepository;
import com.example.library.repository.LoanRepository;

@Service
@Transactional(readOnly = true)
public class BookService {

    private final BookRepository bookRepository;
    private final LoanRepository loanRepository;

    public BookService(BookRepository bookRepository, LoanRepository loanRepository) {
        this.bookRepository = bookRepository;
        this.loanRepository = loanRepository;
    }

    public List<BookResponse> getAll(String search) {
        List<Book> books = (search == null || search.isBlank())
                ? bookRepository.findAllByOrderByTitle()
                : bookRepository.findByTitleContainingIgnoreCaseOrderByTitle(search);
        return books.stream()
                .map(BookResponse::from)
                .toList();
    }

    public BookResponse getById(Long id) {
        return BookResponse.from(findBook(id));
    }

    @Transactional
    public BookResponse create(BookRequest request) {
        if (bookRepository.existsByIsbn(request.isbn())) {
            throw new IsbnAlreadyUsedException(request.isbn());
        }
        Book book = new Book(request.title(), request.author(), request.isbn(),
                request.publishedYear(), request.totalCopies());
        return BookResponse.from(bookRepository.save(book));
    }

    @Transactional
    public BookResponse update(Long id, BookRequest request) {
        Book book = findBook(id);
        if (bookRepository.existsByIsbnAndIdNot(request.isbn(), id)) {
            throw new IsbnAlreadyUsedException(request.isbn());
        }
        if (request.totalCopies() < book.getBorrowedCopies()) {
            throw new InvalidBookException(book.getBorrowedCopies() + " copies are borrowed right now, so the book needs at least "
                    + book.getBorrowedCopies() + " copies");
        }
        book.update(request.title(), request.author(), request.isbn(),
                request.publishedYear(), request.totalCopies());
        return BookResponse.from(book);
    }

    @Transactional
    public void delete(Long id) {
        Book book = findBook(id);
        if (book.getBorrowedCopies() > 0) {
            throw new BookStillBorrowedException(book.getTitle());
        }
        loanRepository.deleteByBookId(id);
        bookRepository.delete(book);
    }

    private Book findBook(Long id) {
        return bookRepository.findById(id)
                .orElseThrow(() -> new BookNotFoundException(id));
    }
}
```

| Code | Meaning |
|---|---|
| `condition ? a : b` | The **ternary** operator (Chapter 10): no search → all books; else → search. |
| `existsByIsbnAndIdNot(request.isbn(), id)` | Rule **R7** for updates: keeping your **own** ISBN is fine, taking **another** book's isn't. |
| `request.totalCopies() < book.getBorrowedCopies()` | You can't have **5** copies borrowed but only **3** copies in total! |
| `book.update(...)` | No `save` — dirty checking (Chapter 79). 🧹 |
| `if (book.getBorrowedCopies() > 0)` | Rule **R8**. |
| `loanRepository.deleteByBookId(id)` | ⭐ The book's **old** (returned) loans point to it with a foreign key → the database would refuse to delete the book. So we delete its loan history first. (A **choice**! Another library might rather keep the history and mark the book "removed" instead. 🤔) |

**`controller/BookController.java`**

```java
package com.example.library.controller;

import java.net.URI;
import java.util.List;

import jakarta.validation.Valid;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.example.library.dto.BookRequest;
import com.example.library.dto.BookResponse;
import com.example.library.service.BookService;

@RestController
@RequestMapping("/api/books")
public class BookController {

    private final BookService bookService;

    public BookController(BookService bookService) {
        this.bookService = bookService;
    }

    @GetMapping
    public List<BookResponse> getAll(@RequestParam(required = false) String search) {
        return bookService.getAll(search);
    }

    @GetMapping("/{id}")
    public BookResponse getById(@PathVariable Long id) {
        return bookService.getById(id);
    }

    @PostMapping
    public ResponseEntity<BookResponse> create(@Valid @RequestBody BookRequest request) {
        BookResponse created = bookService.create(request);
        return ResponseEntity.created(URI.create("/api/books/" + created.id())).body(created);
    }

    @PutMapping("/{id}")
    public BookResponse update(@PathVariable Long id, @Valid @RequestBody BookRequest request) {
        return bookService.update(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        bookService.delete(id);
    }
}
```

Nothing new here — it's the Part 8 pattern you know by heart now. 💪

### 🧪 Try the Book API

Start the app (the door is still open). Add a book:

```bash
curl -i -X POST http://localhost:8080/api/books \
  -H "Content-Type: application/json" \
  -d '{"title":"The Hobbit","author":"J.R.R. Tolkien","isbn":"978-0-261-10221-7","publishedYear":1937,"totalCopies":2}'
```

```
HTTP/1.1 201 
Location: /api/books/1
Content-Type: application/json

{"id":1,"title":"The Hobbit","author":"J.R.R. Tolkien","isbn":"978-0-261-10221-7","publishedYear":1937,"totalCopies":2,"availableCopies":2}
```

The same ISBN again → **409**:

```json
{"detail":"Another book already has the ISBN 978-0-261-10221-7","instance":"/api/books","status":409,"title":"ISBN already used"}
```

Our exception family works! 👨‍👩‍👧‍👦 And `curl "http://localhost:8080/api/books?search=hob"` finds The Hobbit. 🔎

---

## ⚖️ Part 6: `LoanService` — the heart of the library

Now the **business rules** R1–R6. This is the most important class of the app. ❤️

**`service/LoanService.java`**

```java
package com.example.library.service;

import java.time.Clock;
import java.time.LocalDate;
import java.util.List;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.library.dto.LoanResponse;
import com.example.library.entity.AppUser;
import com.example.library.entity.Book;
import com.example.library.entity.Loan;
import com.example.library.exception.BookNotFoundException;
import com.example.library.exception.LoanAlreadyReturnedException;
import com.example.library.exception.LoanLimitReachedException;
import com.example.library.exception.LoanNotFoundException;
import com.example.library.exception.NoCopiesLeftException;
import com.example.library.exception.NotYourLoanException;
import com.example.library.repository.AppUserRepository;
import com.example.library.repository.BookRepository;
import com.example.library.repository.LoanRepository;

@Service
@Transactional(readOnly = true)
public class LoanService {

    private final LoanRepository loanRepository;
    private final BookRepository bookRepository;
    private final AppUserRepository appUserRepository;
    private final Clock clock;
    private final int loanDays;
    private final int maxActiveLoans;

    public LoanService(LoanRepository loanRepository, BookRepository bookRepository,
                       AppUserRepository appUserRepository, Clock clock,
                       @Value("${library.loan.days}") int loanDays,
                       @Value("${library.loan.max-active}") int maxActiveLoans) {
        this.loanRepository = loanRepository;
        this.bookRepository = bookRepository;
        this.appUserRepository = appUserRepository;
        this.clock = clock;
        this.loanDays = loanDays;
        this.maxActiveLoans = maxActiveLoans;
    }

    @Transactional
    public LoanResponse borrow(Long bookId, String username) {
        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new BookNotFoundException(bookId));
        if (book.getAvailableCopies() == 0) {
            throw new NoCopiesLeftException(book.getTitle());
        }
        long activeLoans = loanRepository.countByMemberUsernameAndReturnedOnIsNull(username);
        if (activeLoans >= maxActiveLoans) {
            throw new LoanLimitReachedException(maxActiveLoans);
        }
        AppUser member = appUserRepository.findByUsername(username).orElseThrow();

        LocalDate today = LocalDate.now(clock);
        book.borrowOneCopy();
        Loan loan = loanRepository.save(new Loan(book, member, today, today.plusDays(loanDays)));
        return LoanResponse.from(loan, today);
    }

    @Transactional
    public LoanResponse returnLoan(Long loanId, String username, boolean isLibrarian) {
        Loan loan = loanRepository.findById(loanId)
                .orElseThrow(() -> new LoanNotFoundException(loanId));
        if (!isLibrarian && !loan.getMember().getUsername().equals(username)) {
            throw new NotYourLoanException(loanId);
        }
        if (loan.isReturned()) {
            throw new LoanAlreadyReturnedException(loanId);
        }
        LocalDate today = LocalDate.now(clock);
        loan.markReturned(today);
        loan.getBook().returnOneCopy();
        return LoanResponse.from(loan, today);
    }

    public List<LoanResponse> getMyLoans(String username) {
        LocalDate today = LocalDate.now(clock);
        return loanRepository.findByMemberUsernameOrderByBorrowedOnDesc(username).stream()
                .map(loan -> LoanResponse.from(loan, today))
                .toList();
    }

    public List<LoanResponse> getOverdue() {
        LocalDate today = LocalDate.now(clock);
        return loanRepository.findByReturnedOnIsNullAndDueOnBeforeOrderByDueOn(today).stream()
                .map(loan -> LoanResponse.from(loan, today))
                .toList();
    }
}
```

Let's walk through **`borrow`** — rule by rule:

| Step | Code | Rule |
|---|---|---|
| 1 | `bookRepository.findById(bookId).orElseThrow(...)` | The book must exist → else **404**. |
| 2 | `if (book.getAvailableCopies() == 0) throw new NoCopiesLeftException(...)` | **R2**: a free copy? → else **409**. |
| 3 | `countByMemberUsernameAndReturnedOnIsNull(username)` + `>= maxActiveLoans` | **R3**: fewer than 3 active loans? → else **409**. |
| 4 | `appUserRepository.findByUsername(username).orElseThrow()` | The member — they're logged in, so they exist. |
| 5 | `LocalDate today = LocalDate.now(clock);` | ⭐ "Today" — from **our** `Clock` bean. ⏰ |
| 6 | `book.borrowOneCopy();` | One copy **less** on the shelf (R9 guards it). |
| 7 | `new Loan(book, member, today, today.plusDays(loanDays))` | **R1**: due in 14 days. `plusDays` = "add days" to a date. |
| 8 | `@Transactional` | ⭐ Steps 6 and 7 happen **together or not at all** (Chapter 79). We never get "a copy is gone but no loan exists"! ⚛️ |

And **`returnLoan`**:

| Step | Code | Rule |
|---|---|---|
| 1 | `findById(...)` → `LoanNotFoundException` | The loan must exist → **404**. |
| 2 | `!isLibrarian && !...equals(username)` | **R4**: only the member who borrowed it — or a librarian → else **403**. |
| 3 | `if (loan.isReturned())` | **R5**: not twice → **409**. |
| 4 | `loan.markReturned(today)` + `loan.getBook().returnOneCopy()` | Fill in `returned_on`, and put the copy back on the shelf. Both in **one** transaction. ⚛️ |

🤔 Notice what `LoanService` **doesn't** know: nothing about HTTP, tokens or JSON. It gets a **username** (a `String`) and an `isLibrarian` (a `boolean`). **Who** these come from — that's the controller's job, in Chapter 97. Clean layers = easy to test! 🧪

---

## 💻 Mini project: How many books does each member have? 📊

Mrs. Novak wants a small statistic: **`GET /api/books/{id}/borrowers`** — the usernames of everyone who has this book **right now**.

1. Add a repository method to `LoanRepository` that finds the **active** loans of **one book**.
2. Add `getCurrentBorrowers(Long bookId)` to `BookService` → `List<String>`.
3. Add the endpoint to `BookController`.
4. Unknown book → **404**.

<details>
<summary>Click to see the answer</summary>

**In `LoanRepository`:**

```java
List<Loan> findByBookIdAndReturnedOnIsNull(Long bookId);
```

**In `BookService`:**

```java
public List<String> getCurrentBorrowers(Long bookId) {
    findBook(bookId);
    return loanRepository.findByBookIdAndReturnedOnIsNull(bookId).stream()
            .map(loan -> loan.getMember().getUsername())
            .toList();
}
```

(Import `com.example.library.entity.Loan` is not even needed — the stream works without it. 😉)

| Code | Meaning |
|---|---|
| `findBook(bookId);` | We don't need the book — we call it only for its **check**: unknown id → `BookNotFoundException` → 404. |
| `loan.getMember().getUsername()` | `LAZY` member → loaded here, inside the `readOnly` transaction of the class. ✅ |

**In `BookController`:**

```java
@GetMapping("/{id}/borrowers")
public List<String> getCurrentBorrowers(@PathVariable Long id) {
    return bookService.getCurrentBorrowers(id);
}
```

Right now, nobody can borrow yet (no users, no loan endpoint), so the answer is `[]`. After Chapter 97, it'll show names like `["sara","tom"]`. (And in Chapter 97, think about it: should **everyone** see who borrowed a book? 🤔 Probably only librarians!)

</details>

---

## ✋ Try it yourself

1. Add a second book with `totalCopies` 0. What happens?
2. Change The Hobbit with `PUT` to `"totalCopies":5`. What is `availableCopies` afterwards?
3. Why does `Loan.isOverdue` get `today` as a parameter, instead of calling `LocalDate.now()` itself?
4. Two members click "borrow" on the **last** copy at the **exact** same moment. Could both get it? 🤔

<details>
<summary>Click to see the answers</summary>

1. **400** — `"totalCopies":"A book needs at least 1 copy"` from `@Min(1)`.
2. **5** — nobody has borrowed it yet. (If 1 copy were out, it would be 4.)
3. So it can be tested with **any** date, and so the whole app uses **one** "today" from the `Clock` bean. No hidden clocks! ⏰
4. Sadly, **yes, maybe**: both transactions could read "1 available" at the same time, before either one saves. 😬 Real apps solve this with **locking**. The easiest way in JPA: add a field `@Version private long version;` to `Book`. Then Hibernate notices that the row changed in between, and the **second** transaction fails (with an `ObjectOptimisticLockingFailureException`) instead of giving away a copy that doesn't exist. This is called **optimistic locking** — a great next topic after this book! 🚀

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Setters for everything

`book.setAvailableCopies(...)` from anywhere → sooner or later, someone breaks rule R9. **Fix:** Only meaningful methods like `borrowOneCopy()` that **check** the rules.

### Mistake 2: `LocalDate.now()` everywhere

Then tests can't control "today". **Fix:** Inject a `Clock` and use `LocalDate.now(clock)`.

### Mistake 3: Converting `Loan` to JSON in the controller

`LoanResponse.from(loan, ...)` touches the `LAZY` book and member → outside a transaction, that's the `LazyInitializationException` (Chapter 75). **Fix:** Convert to DTOs **inside** the service.

### Mistake 4: Forgetting `@Transactional` on `borrow`

Without it, `borrowOneCopy()` (with dirty checking) might never be saved, while the loan **is** saved — or the other way round. **Fix:** Every method that changes data gets `@Transactional`.

### Mistake 5: Forgetting the temporary open door

Shipping the "permit all" `SecurityConfig` would be a disaster. **Fix:** Chapter 97 — right now! 🔐

---

## ✅ Summary

- A new project, built **layer by layer** from the plan 🏗️.
- **Entities** protect their own rules (`borrowOneCopy`, `returnOneCopy`, no setters) 🛡️. `Loan` has two `LAZY` many-to-one links and a nullable `returnedOn`.
- **Query methods** can walk through relationships: `countByMemberUsernameAndReturnedOnIsNull`.
- An **exception family** 👨‍👩‍👧‍👦: one abstract parent with status + title → **one** handler for all.
- **`LoanService`** checks every business rule, uses a **`Clock`** for "today", and changes the book and the loan in **one transaction** ⚛️.
- The settings `library.loan.days` and `library.loan.max-active` come in with `@Value`.

---

## ❓ Quiz

1. Why does `Book` have `borrowOneCopy()` instead of `setAvailableCopies(...)`?
2. What does `countByMemberUsernameAndReturnedOnIsNull("sara")` count?
3. How does one `@ExceptionHandler` method handle nine different exceptions?
4. Which rules does `borrow` check, and in which order?
5. Why is `borrow` marked `@Transactional`?
6. Why does `LoanService` get a `String username` instead of an `Authentication`?
7. When is a loan overdue?

<details>
<summary>Click to see the answers</summary>

1. So nobody can set a wrong number: the method checks rule R9 and only ever changes it by one.
2. Sara's loans that are not returned yet (her active loans).
3. All nine extend `LibraryException`, and each one carries its own status and title. The handler catches the parent class and uses those values.
4. The book exists (404), a copy is free (R2, 409), the member has fewer than 3 active loans (R3, 409) — then the loan is made with a due date 14 days later (R1).
5. So taking a copy from the shelf and saving the loan happen together — or not at all.
6. To keep the service independent of HTTP and security. That makes it simpler and easy to test.
7. When it isn't returned and today is after its due date.

</details>

---

[⬅ Previous chapter](95-library-planning.md) | [Table of Contents](../README.md) | [Next chapter: Final project: Library app – security and tests ➡](97-library-security-tests.md)
