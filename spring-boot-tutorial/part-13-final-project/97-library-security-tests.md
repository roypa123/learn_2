# Chapter 97 – Final project: Library app – security and tests

[⬅ Previous chapter](96-library-building.md) | [Table of Contents](../README.md) | [Next chapter ➡](98-making-a-jar.md)

---

## 🎯 Goal

Our library works — but the door is **wide open** 🚪 and nothing is **tested**. Today we finish the app:

- 🔐 Users, BCrypt, JWT tokens and the roles **`MEMBER`** and **`LIBRARIAN`**
- 📅 The **`LoanController`**: borrow, return, my loans, overdue
- 👩‍🏫 The first librarian and some books at start
- 🧪 Tests for the **business rules** — with a **time machine** ⏰🚀
- 🍰 A controller test and 🎂 an end-to-end test

You've done **all** of this before in the school app. That's the point of a final project: now you do it **alone**, faster, and you **see** how the pieces fit. 💪

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Fixed clock** | A `Clock` that always says the **same** time. Perfect for tests: "today is 1 March, forever". ⏰📌 |
| **Time travel** (in tests) | Making the code believe it's another day, to test rules like "overdue". 🚀 |
| **End-to-end test** | A test that walks through a **whole** user story, from the first request to the last. 🎂 |

---

## 📖 Story: The opening day 🎀

The library building is finished. 🏛️ But before the doors open to the public, two things must happen:

1. 🔑 **Locks and keys**: who gets which key? Members get a library card, Mrs. Novak gets the librarian's key.
2. 🧪 **The test run**: friends of the school pretend to be visitors. They borrow books, return them, try to borrow a fourth book, try to return someone else's book... Only when **everything** works correctly do the doors open. ✂️🎀

Today we do both!

---

## 🔐 Part 1: Users and tokens — copied and adapted

These classes are almost the same as in the school app (Chapters 81–83). Copy them, change the **package** to `com.example.library...`, and look at the **few** differences:

| Copy from school | Into library | Changes |
|---|---|---|
| `dto/RegisterRequest`, `LoginRequest`, `TokenResponse`, `UserResponse`, `CurrentUserResponse` | `dto/` | only the package |
| `security/SchoolUserDetailsService` | `security/LibraryUserDetailsService` | the name and the package |
| `security/TokenService` | `security/TokenService` | `.issuer("library")` |
| `config/JwtConfig` | `config/JwtConfig` | the setting `${library.jwt.secret}` |
| `exception/UsernameTakenException` | `exception/UsernameTakenException` | ⭐ now a **`LibraryException`**: `super(HttpStatus.CONFLICT, "Username taken", "The username " + username + " is already taken")` |

And `pom.xml` already has `spring-boot-starter-security` **and** `spring-boot-starter-security-oauth2-resource-server` — Spring Initializr added them when we chose "Spring Security" and "OAuth2 Resource Server". 👍

New settings in **`application.properties`**:

```properties
# JWT tokens
library.jwt.secret=${JWT_SECRET:learning-only-library-secret-change-me-0123456789}
library.jwt.lifetime=1h

# The first librarian
library.librarian.password=${LIBRARIAN_PASSWORD:librarian123}
```

### 👤 `UserService` — register as `MEMBER`

**`service/UserService.java`**

```java
package com.example.library.service;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.library.dto.RegisterRequest;
import com.example.library.dto.UserResponse;
import com.example.library.entity.AppUser;
import com.example.library.exception.UsernameTakenException;
import com.example.library.repository.AppUserRepository;

@Service
public class UserService {

    private final AppUserRepository appUserRepository;
    private final PasswordEncoder passwordEncoder;

    public UserService(AppUserRepository appUserRepository, PasswordEncoder passwordEncoder) {
        this.appUserRepository = appUserRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Transactional
    public UserResponse register(RegisterRequest request) {
        if (appUserRepository.existsByUsername(request.username())) {
            throw new UsernameTakenException(request.username());
        }
        String hash = passwordEncoder.encode(request.password());
        AppUser saved = appUserRepository.save(new AppUser(request.username(), hash, "MEMBER"));
        return UserResponse.from(saved);
    }
}
```

The only difference to Chapter 81: new users get the role **`"MEMBER"`**. 🧒

### 🚪 `AuthController`

Copy it from Chapter 83, **without** the change-password method (not in our plan — "not now"!): `register`, `login` and `me`.

### 🧯 Two more handlers

Add to **`GlobalExceptionHandler`** (Chapters 82 and 83 taught us why — the 500 traps!):

```java
@ExceptionHandler(AuthenticationException.class)
public ProblemDetail handleLoginFailed(AuthenticationException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.UNAUTHORIZED,
            "Wrong username or password");
    problem.setTitle("Login failed");
    return problem;
}

@ExceptionHandler(AccessDeniedException.class)
public ProblemDetail handleAccessDenied(AccessDeniedException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.FORBIDDEN,
            "You are not allowed to do this");
    problem.setTitle("Access denied");
    return problem;
}
```

(Imports: `org.springframework.security.core.AuthenticationException`, `org.springframework.security.access.AccessDeniedException`.)

---

## 🔒 Part 2: Locking the doors — the real `SecurityConfig`

Replace the temporary one. The rules come **straight** from the endpoint table in Chapter 95:

**`config/SecurityConfig.java`**

```java
package com.example.library.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.ProviderManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
import org.springframework.security.oauth2.server.resource.authentication.JwtGrantedAuthoritiesConverter;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(HttpMethod.POST, "/api/auth/register", "/api/auth/login").permitAll()
                .requestMatchers("/api/auth/**").authenticated()
                .requestMatchers(HttpMethod.GET, "/api/books/*/borrowers").hasRole("LIBRARIAN")
                .requestMatchers(HttpMethod.GET, "/api/books/**").permitAll()
                .requestMatchers("/api/books/**").hasRole("LIBRARIAN")
                .requestMatchers(HttpMethod.POST, "/api/loans").hasRole("MEMBER")
                .requestMatchers(HttpMethod.GET, "/api/loans/mine").hasRole("MEMBER")
                .requestMatchers(HttpMethod.PUT, "/api/loans/*/return").hasAnyRole("MEMBER", "LIBRARIAN")
                .requestMatchers(HttpMethod.GET, "/api/loans/overdue").hasRole("LIBRARIAN")
                .requestMatchers("/actuator/health").permitAll()
                .requestMatchers("/error").permitAll()
                .anyRequest().authenticated())
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthenticationConverter())))
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
        return http.build();
    }

    private JwtAuthenticationConverter jwtAuthenticationConverter() {
        JwtGrantedAuthoritiesConverter rolesConverter = new JwtGrantedAuthoritiesConverter();
        rolesConverter.setAuthoritiesClaimName("roles");
        rolesConverter.setAuthorityPrefix("ROLE_");

        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(rolesConverter);
        return converter;
    }

    @Bean
    public AuthenticationManager authenticationManager(UserDetailsService userDetailsService,
                                                       PasswordEncoder passwordEncoder) {
        DaoAuthenticationProvider provider = new DaoAuthenticationProvider(userDetailsService);
        provider.setPasswordEncoder(passwordEncoder);
        return new ProviderManager(provider);
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

The new things:

| Rule | Meaning |
|---|---|
| `GET /api/books/*/borrowers` → `LIBRARIAN` | The mini project of Chapter 96: **who** has a book is private. ⭐ It must come **before** `GET /api/books/**` → `permitAll`! (Chapter 80's lesson: specific first! 📏) |
| `/api/books/*/borrowers` | The `*` matches **one** part of the path: `/api/books/1/borrowers`, `/api/books/42/borrowers`... |
| `/api/books/**` → `LIBRARIAN` | All **other** book methods (POST, PUT, DELETE). |
| `PUT /api/loans/*/return` → `MEMBER` or `LIBRARIAN` | Both may return. **Whose** loan — that's checked in `LoanService` (rule R4), because the URL rule can't know who owns loan 7. 🤔 |

---

## 📅 Part 3: The `LoanController`

**`controller/LoanController.java`**

```java
package com.example.library.controller;

import java.net.URI;
import java.util.List;

import jakarta.validation.Valid;

import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.library.dto.LoanRequest;
import com.example.library.dto.LoanResponse;
import com.example.library.service.LoanService;

@RestController
@RequestMapping("/api/loans")
public class LoanController {

    private final LoanService loanService;

    public LoanController(LoanService loanService) {
        this.loanService = loanService;
    }

    @PostMapping
    public ResponseEntity<LoanResponse> borrow(@Valid @RequestBody LoanRequest request,
                                               Authentication authentication) {
        LoanResponse loan = loanService.borrow(request.bookId(), authentication.getName());
        return ResponseEntity.created(URI.create("/api/loans/" + loan.id())).body(loan);
    }

    @GetMapping("/mine")
    public List<LoanResponse> getMyLoans(Authentication authentication) {
        return loanService.getMyLoans(authentication.getName());
    }

    @PutMapping("/{id}/return")
    public LoanResponse returnLoan(@PathVariable Long id, Authentication authentication) {
        boolean isLibrarian = authentication.getAuthorities().stream()
                .anyMatch(authority -> authority.getAuthority().equals("ROLE_LIBRARIAN"));
        return loanService.returnLoan(id, authentication.getName(), isLibrarian);
    }

    @GetMapping("/overdue")
    public List<LoanResponse> getOverdue() {
        return loanService.getOverdue();
    }
}
```

| Code | Meaning |
|---|---|
| `authentication.getName()` | ⭐ The member comes from the **token**, never from the body. Sara can't borrow "as Tom". 🛡️ |
| `.anyMatch(authority -> ...equals("ROLE_LIBRARIAN"))` | "Does **any** of the user's authorities equal `ROLE_LIBRARIAN`?" (Chapter 36) → `true`/`false` for the service. |

See how **thin** the controller is? Just "read who's calling → call the service". All the thinking happens in `LoanService`. 🧠

---

## 👩‍🏫 Part 4: Opening day — the first librarian and some books

**`security/DataLoader.java`**

```java
package com.example.library.security;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import com.example.library.entity.AppUser;
import com.example.library.entity.Book;
import com.example.library.repository.AppUserRepository;
import com.example.library.repository.BookRepository;

@Component
public class DataLoader implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(DataLoader.class);

    private final AppUserRepository appUserRepository;
    private final BookRepository bookRepository;
    private final PasswordEncoder passwordEncoder;
    private final String librarianPassword;

    public DataLoader(AppUserRepository appUserRepository, BookRepository bookRepository,
                      PasswordEncoder passwordEncoder,
                      @Value("${library.librarian.password}") String librarianPassword) {
        this.appUserRepository = appUserRepository;
        this.bookRepository = bookRepository;
        this.passwordEncoder = passwordEncoder;
        this.librarianPassword = librarianPassword;
    }

    @Override
    public void run(String... args) {
        if (!appUserRepository.existsByUsername("novak")) {
            appUserRepository.save(new AppUser("novak", passwordEncoder.encode(librarianPassword), "LIBRARIAN"));
            log.info("Added the librarian novak");
        }
        if (bookRepository.count() == 0) {
            bookRepository.saveAll(List.of(
                    new Book("The Hobbit", "J.R.R. Tolkien", "978-0-261-10221-7", 1937, 2),
                    new Book("Matilda", "Roald Dahl", "978-0-14-241037-1", 1988, 1),
                    new Book("Charlotte's Web", "E.B. White", "978-0-06-440055-8", 1952, 3)));
            log.info("Added 3 books");
        }
    }
}
```

Everything here is from earlier chapters: a `CommandLineRunner` (Chapter 73), a password from **outside** (Chapter 82), BCrypt (Chapter 81), and a real **logger** (Chapter 88) instead of `System.out`. 📔

(If you added The Hobbit by hand in Chapter 96, the books part is skipped — `count()` isn't 0. No problem!)

---

## 🎬 Part 5: The test run — by hand

Restart. Let's play the opening day with curl. (In Git Bash, `TOKEN=...` saves a token — Chapter 83.)

**1. Sara registers and logs in:**

```bash
curl -X POST http://localhost:8080/api/auth/register -H "Content-Type: application/json" \
  -d '{"username":"sara","password":"sunflower7"}'
curl -X POST http://localhost:8080/api/auth/login -H "Content-Type: application/json" \
  -d '{"username":"sara","password":"sunflower7"}'
```

→ `{"id":2,"username":"sara","role":"MEMBER"}` and `{"token":"eyJ...","tokenType":"Bearer","expiresIn":3600}`. Save it: `SARA=eyJ...`

**2. Sara borrows Matilda (book 2, only 1 copy):**

```bash
curl -i -X POST http://localhost:8080/api/loans -H "Authorization: Bearer $SARA" \
  -H "Content-Type: application/json" -d '{"bookId":2}'
```

```
HTTP/1.1 201 
Location: /api/loans/1
Content-Type: application/json

{"id":1,"bookId":2,"bookTitle":"Matilda","member":"sara","borrowedOn":"2026-10-14","dueOn":"2026-10-28","returnedOn":null,"overdue":false}
```

📅 Due in 14 days (R1)! And `GET /api/books/2` now shows `"availableCopies":0`.

**3. Tom registers, logs in, and also wants Matilda:**

```
HTTP/1.1 409 
Content-Type: application/problem+json

{"detail":"All copies of Matilda are borrowed right now","instance":"/api/loans","status":409,"title":"No copies left"}
```

🚫 Rule R2!

**4. Tom tries to return Sara's loan** (`PUT /api/loans/1/return` with Tom's token):

```
HTTP/1.1 403 
Content-Type: application/problem+json

{"detail":"Loan 1 belongs to another member","instance":"/api/loans/1/return","status":403,"title":"Not your loan"}
```

🛡️ Rule R4!

**5. Sara returns it** → `200` with `"returnedOn":"2026-10-14"`. Again → **409** `"Already returned"` (R5). ✅

**6. Mrs. Novak** logs in (`novak` / `librarian123`) and checks `GET /api/loans/overdue` → `[]` (nobody is late — yet!). And if Sara tries `GET /api/loans/overdue` → **403**. 🔐

Everything works. But we can't check **every** rule by hand after **every** change — and how would we test "overdue" without waiting 15 days? 🤔 Tests!

---

## ⏰ Part 6: Testing the rules — with a time machine

The business rules are the **heart** of the app → they get the **most** tests. Unit tests with Mockito (Chapter 85) — plus a **fixed clock**.

**`src/test/java/com/example/library/service/LoanServiceTest.java`**

```java
package com.example.library.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.example.library.dto.LoanResponse;
import com.example.library.entity.AppUser;
import com.example.library.entity.Book;
import com.example.library.entity.Loan;
import com.example.library.exception.LoanAlreadyReturnedException;
import com.example.library.exception.LoanLimitReachedException;
import com.example.library.exception.NoCopiesLeftException;
import com.example.library.exception.NotYourLoanException;
import com.example.library.repository.AppUserRepository;
import com.example.library.repository.BookRepository;
import com.example.library.repository.LoanRepository;

@ExtendWith(MockitoExtension.class)
class LoanServiceTest {

    private static final LocalDate TODAY = LocalDate.of(2026, 3, 1);

    @Mock
    private LoanRepository loanRepository;

    @Mock
    private BookRepository bookRepository;

    @Mock
    private AppUserRepository appUserRepository;

    private LoanService loanService;

    private final AppUser sara = new AppUser("sara", "hash", "MEMBER");

    @BeforeEach
    void setUp() {
        Clock fixedClock = Clock.fixed(Instant.parse("2026-03-01T10:00:00Z"), ZoneOffset.UTC);
        loanService = new LoanService(loanRepository, bookRepository, appUserRepository, fixedClock, 14, 3);
    }

    @Test
    void borrowGivesALoanDueIn14Days() {
        Book hobbit = new Book("The Hobbit", "J.R.R. Tolkien", "978-0-261-10221-7", 1937, 2);
        when(bookRepository.findById(1L)).thenReturn(Optional.of(hobbit));
        when(loanRepository.countByMemberUsernameAndReturnedOnIsNull("sara")).thenReturn(0L);
        when(appUserRepository.findByUsername("sara")).thenReturn(Optional.of(sara));
        when(loanRepository.save(any(Loan.class))).thenAnswer(invocation -> invocation.getArgument(0));

        LoanResponse loan = loanService.borrow(1L, "sara");

        assertThat(loan.borrowedOn()).isEqualTo(TODAY);
        assertThat(loan.dueOn()).isEqualTo(LocalDate.of(2026, 3, 15));
        assertThat(loan.overdue()).isFalse();
        assertThat(hobbit.getAvailableCopies()).isEqualTo(1);
    }

    @Test
    void borrowRefusesWhenNoCopyIsLeft() {
        Book matilda = new Book("Matilda", "Roald Dahl", "978-0-14-241037-1", 1988, 1);
        matilda.borrowOneCopy();
        when(bookRepository.findById(2L)).thenReturn(Optional.of(matilda));

        assertThatThrownBy(() -> loanService.borrow(2L, "sara"))
                .isInstanceOf(NoCopiesLeftException.class)
                .hasMessage("All copies of Matilda are borrowed right now");
        verify(loanRepository, never()).save(any());
    }

    @Test
    void borrowRefusesAFourthBook() {
        Book hobbit = new Book("The Hobbit", "J.R.R. Tolkien", "978-0-261-10221-7", 1937, 2);
        when(bookRepository.findById(1L)).thenReturn(Optional.of(hobbit));
        when(loanRepository.countByMemberUsernameAndReturnedOnIsNull("sara")).thenReturn(3L);

        assertThatThrownBy(() -> loanService.borrow(1L, "sara"))
                .isInstanceOf(LoanLimitReachedException.class);
        assertThat(hobbit.getAvailableCopies()).isEqualTo(2);
    }

    @Test
    void aMemberCannotReturnSomeoneElsesLoan() {
        Loan saraLoan = borrowedLoan();
        when(loanRepository.findById(7L)).thenReturn(Optional.of(saraLoan));

        assertThatThrownBy(() -> loanService.returnLoan(7L, "tom", false))
                .isInstanceOf(NotYourLoanException.class);
        assertThat(saraLoan.isReturned()).isFalse();
    }

    @Test
    void aLibrarianCanReturnAnyLoan() {
        Loan saraLoan = borrowedLoan();
        when(loanRepository.findById(7L)).thenReturn(Optional.of(saraLoan));

        LoanResponse returned = loanService.returnLoan(7L, "novak", true);

        assertThat(returned.returnedOn()).isEqualTo(TODAY);
        assertThat(saraLoan.getBook().getAvailableCopies()).isEqualTo(2);
    }

    @Test
    void aLoanCannotBeReturnedTwice() {
        Loan saraLoan = borrowedLoan();
        saraLoan.markReturned(TODAY);
        when(loanRepository.findById(7L)).thenReturn(Optional.of(saraLoan));

        assertThatThrownBy(() -> loanService.returnLoan(7L, "sara", false))
                .isInstanceOf(LoanAlreadyReturnedException.class);
    }

    private Loan borrowedLoan() {
        Book hobbit = new Book("The Hobbit", "J.R.R. Tolkien", "978-0-261-10221-7", 1937, 2);
        hobbit.borrowOneCopy();
        return new Loan(hobbit, sara, TODAY.minusDays(3), TODAY.plusDays(11));
    }
}
```

The important new parts:

| Code | Meaning |
|---|---|
| `Clock.fixed(Instant.parse("2026-03-01T10:00:00Z"), ZoneOffset.UTC)` | ⭐ The **time machine** ⏰🚀: a clock that **always** says "1 March 2026, 10:00, UTC". `LocalDate.now(fixedClock)` → `2026-03-01`. Every time. On every computer. |
| `new LoanService(..., fixedClock, 14, 3)` | ⭐ We build the service **ourselves** — plain Java! `@InjectMocks` can't guess the numbers `14` and `3`. (And look: the constructor makes this easy. That's one more reason why constructor injection is great — Chapter 53.) |
| `LocalDate.of(2026, 3, 15)` | 1 March + 14 days = **15 March** (R1). |
| `hobbit.getAvailableCopies()).isEqualTo(1)` | The **real** `Book` object lost a copy. (We don't mock entities — Chapter 85's "mock the neighbours, test the house"!) |
| `matilda.borrowOneCopy();` | **Arrange**: the only copy is already out. |
| `...thenReturn(3L)` | Sara already has 3 loans → the fourth must fail (R3). And the Hobbit keeps **both** copies. |
| `borrowedLoan()` | A small helper that makes "Sara borrowed The Hobbit 3 days ago". `TODAY.minusDays(3)` = 26 February. |

### ⏰ Testing "overdue" — the real time travel

`Loan.isOverdue` gets today as a parameter → we can test **any** day, no clock needed:

**`src/test/java/com/example/library/entity/LoanTest.java`**

```java
package com.example.library.entity;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.LocalDate;

import org.junit.jupiter.api.Test;

class LoanTest {

    private final LocalDate dueOn = LocalDate.of(2026, 3, 15);
    private final Loan loan = new Loan(
            new Book("Matilda", "Roald Dahl", "978-0-14-241037-1", 1988, 1),
            new AppUser("sara", "hash", "MEMBER"),
            LocalDate.of(2026, 3, 1), dueOn);

    @Test
    void notOverdueBeforeTheDueDate() {
        assertThat(loan.isOverdue(LocalDate.of(2026, 3, 10))).isFalse();
    }

    @Test
    void notOverdueOnTheDueDate() {
        assertThat(loan.isOverdue(dueOn)).isFalse();
    }

    @Test
    void overdueTheDayAfter() {
        assertThat(loan.isOverdue(dueOn.plusDays(1))).isTrue();
    }

    @Test
    void neverOverdueWhenReturned() {
        loan.markReturned(LocalDate.of(2026, 3, 14));
        assertThat(loan.isOverdue(LocalDate.of(2026, 6, 1))).isFalse();
    }
}
```

| Test | Checks |
|---|---|
| `notOverdueOnTheDueDate` | ⭐ The **border** (Chapter 84 — bugs love borders!): on the due date itself, you're still on time. |
| `overdueTheDayAfter` | One day later → overdue. ⏰ |
| `neverOverdueWhenReturned` | A returned book is never "late" — even months later. |

We just tested the 15th of March, the 16th of March **and** June — in **milliseconds**. 🚀 That's the power of keeping "today" **out** of the logic.

---

## 🍰 Part 7: A controller test — the security rules

**`src/test/java/com/example/library/controller/LoanControllerTest.java`**

```java
package com.example.library.controller;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.jwt;

import java.time.LocalDate;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.assertj.MockMvcTester;
import org.springframework.test.web.servlet.request.RequestPostProcessor;

import com.example.library.config.JwtConfig;
import com.example.library.config.SecurityConfig;
import com.example.library.dto.LoanResponse;
import com.example.library.service.LoanService;

@WebMvcTest(LoanController.class)
@Import({SecurityConfig.class, JwtConfig.class})
class LoanControllerTest {

    @Autowired
    private MockMvcTester mvc;

    @MockitoBean
    private LoanService loanService;

    @MockitoBean
    private UserDetailsService userDetailsService;

    private static RequestPostProcessor user(String name, String role) {
        return jwt().jwt(token -> token.subject(name))
                .authorities(new SimpleGrantedAuthority("ROLE_" + role));
    }

    @Test
    void aMemberCanBorrow() {
        when(loanService.borrow(2L, "sara")).thenReturn(new LoanResponse(1L, 2L, "Matilda", "sara",
                LocalDate.of(2026, 3, 1), LocalDate.of(2026, 3, 15), null, false));

        assertThat(mvc.post().uri("/api/loans")
                .with(user("sara", "MEMBER"))
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                        {"bookId":2}
                        """))
                .hasStatus(HttpStatus.CREATED)
                .hasHeader("Location", "/api/loans/1")
                .bodyJson()
                .extractingPath("$.dueOn").isEqualTo("2026-03-15");
    }

    @Test
    void aLibrarianCannotBorrow() {
        assertThat(mvc.post().uri("/api/loans")
                .with(user("novak", "LIBRARIAN"))
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                        {"bookId":2}
                        """))
                .hasStatus(HttpStatus.FORBIDDEN);
        verify(loanService, never()).borrow(any(), any());
    }

    @Test
    void strangersCannotBorrow() {
        assertThat(mvc.post().uri("/api/loans")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                        {"bookId":2}
                        """))
                .hasStatus(HttpStatus.UNAUTHORIZED);
    }

    @Test
    void theControllerTellsTheServiceWhoIsALibrarian() {
        mvc.put().uri("/api/loans/7/return").with(user("novak", "LIBRARIAN")).exchange();

        verify(loanService).returnLoan(eq(7L), eq("novak"), eq(true));
    }

    @Test
    void onlyLibrariansSeeOverdueLoans() {
        assertThat(mvc.get().uri("/api/loans/overdue").with(user("sara", "MEMBER")))
                .hasStatus(HttpStatus.FORBIDDEN);
    }
}
```

| Code | Meaning |
|---|---|
| `jwt().jwt(token -> token.subject(name))` | ⭐ A pretend token **with a username** (`sub`), so `authentication.getName()` says `"sara"` — Chapter 86 didn't need that. |
| `.extractingPath("$.dueOn").isEqualTo("2026-03-15")` | Dates are written as text in JSON. |
| `verify(loanService).returnLoan(eq(7L), eq("novak"), eq(true))` | ⭐ The controller worked out `isLibrarian = true` from the token. `eq(...)` = "exactly this value" (needed when you mix matchers). |
| `mvc.put()...exchange()` | Send it — we don't care about the answer here, only about what reached the service. |

---

## 🎂 Part 8: The whole story — an end-to-end test

First, the test profile (Chapter 87): **`src/test/resources/application-test.properties`**

```properties
spring.datasource.url=jdbc:h2:mem:librarytest
spring.jpa.hibernate.ddl-auto=create-drop
```

**`src/test/java/com/example/library/LibraryFlowTest.java`**

```java
package com.example.library;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.assertj.MockMvcTester;
import org.springframework.test.web.servlet.assertj.MvcTestResult;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class LibraryFlowTest {

    @Autowired
    private MockMvcTester mvc;

    @Test
    void aMemberRegistersBorrowsAndReturnsABook() throws Exception {
        // 1. Register and log in
        assertThat(post("/api/auth/register", "{\"username\":\"lina\",\"password\":\"lina-reads-1\"}", null))
                .hasStatus(HttpStatus.CREATED);
        String token = tokenFrom(post("/api/auth/login", "{\"username\":\"lina\",\"password\":\"lina-reads-1\"}", null));

        // 2. Borrow Charlotte's Web (book 3, 3 copies)
        MvcTestResult borrowed = post("/api/loans", "{\"bookId\":3}", token);
        assertThat(borrowed).hasStatus(HttpStatus.CREATED);
        assertThat(mvc.get().uri("/api/books/3")).bodyJson()
                .extractingPath("$.availableCopies").isEqualTo(2);

        // 3. My loans shows it
        assertThat(mvc.get().uri("/api/loans/mine").header(HttpHeaders.AUTHORIZATION, "Bearer " + token))
                .hasStatusOk()
                .bodyJson()
                .extractingPath("$[0].bookTitle").isEqualTo("Charlotte's Web");

        // 4. Return it
        String location = borrowed.getResponse().getHeader(HttpHeaders.LOCATION);
        assertThat(mvc.put().uri(location + "/return").header(HttpHeaders.AUTHORIZATION, "Bearer " + token))
                .hasStatusOk();
        assertThat(mvc.get().uri("/api/books/3")).bodyJson()
                .extractingPath("$.availableCopies").isEqualTo(3);
    }

    private MvcTestResult post(String uri, String json, String token) {
        var request = mvc.post().uri(uri).contentType(MediaType.APPLICATION_JSON).content(json);
        if (token != null) {
            request.header(HttpHeaders.AUTHORIZATION, "Bearer " + token);
        }
        return request.exchange();
    }

    private static String tokenFrom(MvcTestResult result) throws Exception {
        String json = result.getResponse().getContentAsString();
        String start = "\"token\":\"";
        int from = json.indexOf(start) + start.length();
        return json.substring(from, json.indexOf("\"", from));
    }
}
```

| Code | Meaning |
|---|---|
| `@SpringBootTest` + `@AutoConfigureMockMvc` + `@ActiveProfiles("test")` | The whole app, with an in-memory database (Chapter 87). The `DataLoader` adds the 3 books and `novak`. |
| `var request = ...` | **`var`** lets Java work out the type by itself — handy for long builder types. |
| `post(...)` helper | Saves us from writing the same 4 lines again and again. |
| the four steps | ⭐ **One** test walks through the **whole** user story: register → login → borrow → see → return — and checks that the copies go **down** and **up** again. 🎂 |

### ▶️ Run everything

```bash
./mvnw test
```

You should see all test classes — `LoanServiceTest`, `LoanTest`, `LoanControllerTest`, `LibraryFlowTest`, and the generated `LibraryApplicationTests` (give it `@ActiveProfiles("test")` too!) — and:

```
[INFO] BUILD SUCCESS
```

🟢 The doors can open! ✂️🎀

---

## 💻 Mini project: A test for the book rules 📚

Write **`BookServiceTest`** (Mockito, like `LoanServiceTest`) with three tests:

1. `create` with a used ISBN → `IsbnAlreadyUsedException`, and nothing saved.
2. `update` to **1** copy while **2** are borrowed → `InvalidBookException`.
3. `delete` while a copy is borrowed → `BookStillBorrowedException`, and `deleteByBookId` was **never** called.

<details>
<summary>Click to see the answer</summary>

**`src/test/java/com/example/library/service/BookServiceTest.java`**

```java
package com.example.library.service;

import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Optional;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.example.library.dto.BookRequest;
import com.example.library.entity.Book;
import com.example.library.exception.BookStillBorrowedException;
import com.example.library.exception.InvalidBookException;
import com.example.library.exception.IsbnAlreadyUsedException;
import com.example.library.repository.BookRepository;
import com.example.library.repository.LoanRepository;

@ExtendWith(MockitoExtension.class)
class BookServiceTest {

    @Mock
    private BookRepository bookRepository;

    @Mock
    private LoanRepository loanRepository;

    @InjectMocks
    private BookService bookService;

    @Test
    void createRefusesAUsedIsbn() {
        when(bookRepository.existsByIsbn("978-0-261-10221-7")).thenReturn(true);

        assertThatThrownBy(() -> bookService.create(
                new BookRequest("The Hobbit", "J.R.R. Tolkien", "978-0-261-10221-7", 1937, 2)))
                .isInstanceOf(IsbnAlreadyUsedException.class);
        verify(bookRepository, never()).save(any());
    }

    @Test
    void updateNeedsEnoughCopiesForTheBorrowedOnes() {
        Book hobbit = new Book("The Hobbit", "J.R.R. Tolkien", "978-0-261-10221-7", 1937, 3);
        hobbit.borrowOneCopy();
        hobbit.borrowOneCopy();
        when(bookRepository.findById(1L)).thenReturn(Optional.of(hobbit));
        when(bookRepository.existsByIsbnAndIdNot("978-0-261-10221-7", 1L)).thenReturn(false);

        assertThatThrownBy(() -> bookService.update(1L,
                new BookRequest("The Hobbit", "J.R.R. Tolkien", "978-0-261-10221-7", 1937, 1)))
                .isInstanceOf(InvalidBookException.class);
    }

    @Test
    void deleteRefusesABorrowedBook() {
        Book matilda = new Book("Matilda", "Roald Dahl", "978-0-14-241037-1", 1988, 1);
        matilda.borrowOneCopy();
        when(bookRepository.findById(2L)).thenReturn(Optional.of(matilda));

        assertThatThrownBy(() -> bookService.delete(2L))
                .isInstanceOf(BookStillBorrowedException.class);
        verify(loanRepository, never()).deleteByBookId(any());
    }
}
```

| Code | Meaning |
|---|---|
| `@InjectMocks` works here | `BookService` only needs two repositories — no numbers, no clock. |
| two `borrowOneCopy()` calls | **Arrange**: 2 of 3 copies are out → asking for 1 copy in total must fail. |

</details>

---

## ✋ Try it yourself

1. Use the **time machine** to test `getOverdue()`: stub `findByReturnedOnIsNullAndDueOnBeforeOrderByDueOn(TODAY)` to return one loan with `dueOn` = 20 February, and check that its `overdue` is `true`.
2. Set `library.loan.max-active=1` in `application-test.properties`, and add a step to `LibraryFlowTest`: borrowing a **second** book → 409. Then put the setting back.
3. Look at the rule list R1–R9 from Chapter 95. Which rules have a test now? Which one doesn't?

<details>
<summary>Click to see the answers</summary>

1. ```java
   @Test
   void overdueLoansAreMarked() {
       Loan late = new Loan(new Book("Matilda", "Roald Dahl", "978-0-14-241037-1", 1988, 1), sara,
               LocalDate.of(2026, 2, 6), LocalDate.of(2026, 2, 20));
       when(loanRepository.findByReturnedOnIsNullAndDueOnBeforeOrderByDueOn(TODAY)).thenReturn(List.of(late));

       assertThat(loanService.getOverdue()).extracting(LoanResponse::overdue).containsExactly(true);
   }
   ```
   (Import `java.util.List`.)
2. After the first borrow, `post("/api/loans", "{\"bookId\":1}", token)` → `assertThat(...).hasStatus(HttpStatus.CONFLICT)`. The **setting** changes the **rule** — without changing any Java code! ⚙️
3. R1 ✅, R2 ✅, R3 ✅, R4 ✅, R5 ✅, R6 ✅ (`LoanTest`), R7 ✅ and R8 ✅ (mini project), R9 — partly: `borrowOneCopy`/`returnOneCopy` guard it, but there's no test that they **throw**. Write one! (`assertThatThrownBy(() -> book.returnOneCopy())` on a book with all copies at home.) 🧪

</details>

---

## ⚠️ Common mistakes

### Mistake 1: The specific URL rule after the general one

`GET /api/books/**` → `permitAll` **above** `GET /api/books/*/borrowers` → everyone sees the borrowers. **Fix:** Specific first — and **test** it (like `onlyLibrariansSeeOverdueLoans`).

### Mistake 2: Taking the member from the request body

`{"bookId":2,"member":"tom"}` → Sara could borrow in Tom's name. **Fix:** Always `authentication.getName()`.

### Mistake 3: Tests that depend on today's date

`assertThat(loan.dueOn()).isEqualTo(LocalDate.now().plusDays(14))` works... until a test runs at 23:59:59 and the date changes in between. 😅 **Fix:** A **fixed** `Clock`.

### Mistake 4: `@InjectMocks` with numbers in the constructor

Mockito can't guess `14` and `3`. **Fix:** Build the object yourself with `new`.

### Mistake 5: Only testing the happy path

The happy path is **one** test; the rules are **nine**. **Fix:** At least one test per business rule — every 409, 403 and 404 from the plan.

---

## ✅ Summary

- Security for the library = the school app's security, adapted: `MEMBER`/`LIBRARIAN`, BCrypt, JWT, URL rules **from the plan** 🔐.
- Ownership (rule R4) is checked in the **service** — URL rules can't know who owns loan 7.
- A **thin** `LoanController`: `authentication.getName()` + "is librarian?" → the service.
- **`Clock.fixed(...)`** ⏰📌 makes "today" a fixed day → time rules are testable in milliseconds.
- Build services with **`new`** in tests when the constructor needs values like `14` and `3`.
- **`jwt().jwt(token -> token.subject("sara"))`** gives the pretend user a name.
- The pyramid 🔺: many rule tests, a few controller tests, **one** end-to-end story — and `./mvnw test` → 🟢.

---

## ❓ Quiz

1. Why is rule R4 ("only your own loan") checked in `LoanService` and not in `SecurityConfig`?
2. What does `Clock.fixed(Instant.parse("2026-03-01T10:00:00Z"), ZoneOffset.UTC)` do?
3. Why do we create `LoanService` with `new` in `LoanServiceTest`?
4. How do you give a pretend JWT a username in a `@WebMvcTest`?
5. What does `LibraryFlowTest` check that the other tests can't?
6. Why is `notOverdueOnTheDueDate` an important test?

<details>
<summary>Click to see the answers</summary>

1. A URL rule only sees the URL and the roles. Who owns loan 7 is only known from the database, in the service.
2. It makes a clock that always says 1 March 2026, 10:00 UTC — so "today" is always the same in tests.
3. Its constructor needs the numbers 14 and 3 (and a clock), which `@InjectMocks` can't guess.
4. `jwt().jwt(token -> token.subject("sara"))`.
5. That all the real parts work together: login with a real token, the real database, the real rules — and that the copy counts go down and up again.
6. It's a **border** value: the day where "on time" turns into "late". Off-by-one bugs (`>=` instead of `>`) hide there.

</details>

---

[⬅ Previous chapter](96-library-building.md) | [Table of Contents](../README.md) | [Next chapter: Making a .jar file ➡](98-making-a-jar.md)
