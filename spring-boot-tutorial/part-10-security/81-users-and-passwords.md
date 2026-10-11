# Chapter 81 – Users and passwords

[⬅ Previous chapter](80-spring-security.md) | [Table of Contents](../README.md) | [Next chapter ➡](82-roles.md)

---

## 🎯 Goal

In the last chapter, our app had **one** user, written in `application.properties`. 😬 A real school has **hundreds** of users, and new ones every day. Today, users move into the **database** — with their passwords stored the **safe** way. 🔐

At the end of this chapter you will know:

- Why you must **never** save a password as plain text 😱
- What **hashing** is (the smoothie trick 🥤), and what a **salt** is 🧂
- How **BCrypt** and the **`PasswordEncoder`** work
- How Spring Security finds a user: the **`UserDetailsService`** 🔎
- How to build a **register** endpoint: `POST /api/auth/register` 📝
- How your code knows **who** is calling: `GET /api/auth/me` 🙋

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Plain text** | Text exactly as it is, readable by anyone: `secret123`. |
| **Hash** | A "fingerprint" made from a text by a **one-way** recipe. You can't turn it back into the text. 🥤 |
| **Hashing** | Making a hash from a text. |
| **Salt** | A **random** extra bit mixed in before hashing, so two equal passwords get **different** hashes. 🧂 |
| **BCrypt** | A hashing recipe made **for passwords**: salted and **slow on purpose**. 🐢 |
| **`PasswordEncoder`** | Spring's helper that **hashes** passwords and **checks** them. |
| **`UserDetails`** | Spring Security's "user card": name, password hash, and what the user may do. 🪪 |
| **`UserDetailsService`** | The helper Spring asks: "Please **find** the user called `sara`." 🔎 |
| **Register** | Making a new user account ("sign up"). |
| **Data leak** | When secret data gets out — for example, a bad person copies the whole database. 💧 |

---

## 📖 Story: The diary in the school bag 📔

Lina writes her secrets in a diary 📔. One day, her school bag is **stolen**.

- If the diary is written in **normal** letters → the thief reads **everything**. 😱
- If the diary is written in a **secret code** that **nobody** can turn back → the thief sees only gibberish: `$2a$10$dOIboiyrIvCT...` 🤷

Databases get stolen too — it happens to big companies every year. 💧 So we follow one **golden rule**:

> 🏆 **Never store passwords. Store only their hashes.**

But wait... if we can't turn a hash back into the password, how do we **check** a login? 🤔 That's the clever part — let's see!

---

## 😱 Part 1: Why not just save the password?

Imagine our `app_users` table **with** plain passwords:

```
 ID | USERNAME | PASSWORD
  1 | teacher  | secret123
  2 | sara     | sunflower7
```

If a bad person **ever** gets this table (a stolen backup, a bug, a curious worker 👀):

1. They can log in as **every** user. 😱
2. Even worse: many people use the **same** password on **many** websites. Now the bad person tries `sara` / `sunflower7` on Sara's **email**, her **games**... 🎮📧

So even **you**, the programmer, must **not** be able to read the passwords. Only the **user** knows their password. 🤫

---

## 🥤 Part 2: Hashing — the smoothie trick

A **hash** is like a **smoothie** 🥤:

```
 🍓🍌 strawberry + banana  ──► 🌀 blender ──►  🥤 pink smoothie
```

| Smoothie fact | Hash fact |
|---|---|
| Same fruit → **always** the same smoothie. | Same text → **always** the same hash. |
| You **can't** un-blend a smoothie back into a strawberry. 🍓❌ | You **can't** turn a hash back into the password. |
| Different fruit → a different smoothie. | Different text → a totally different hash. |

So how do we **check** a password? We don't un-blend! We **blend again** and **compare**:

```
 Register:  "sunflower7"  ──► 🌀 ──► $2a$10$.CVT91... → save in the database 💾

 Login:     "sunflower7"  ──► 🌀 ──► same result?  ✅ → correct password!
 Login:     "sunflower8"  ──► 🌀 ──► different!     ❌ → wrong password!
```

The server **never** needs the real password again. 🎉

### 🧂 The problem with "same text, same hash" — and the salt

Bad people have **giant lists** of popular passwords and their hashes: `123456` → `e10adc...`, `password` → `5f4dcc...`. They just **look up** your hash in the list. 📖 And if Tom and Lina **both** use `football1`, their hashes look **the same** — so cracking one cracks both!

The fix is a **salt** 🧂: before blending, add a **random** extra ingredient — **different** for every user — and keep it **next to** the hash:

```
 Tom:  "football1" + 🧂 salt "x8Kq..."  ──► 🌀 ──► $2a$10$x8Kq...8fJ2...
 Lina: "football1" + 🧂 salt "Pz3w..."  ──► 🌀 ──► $2a$10$Pz3w...Ab91...
                                                      ▲ totally different! ✅
```

Now the giant lists are **useless** (they don't have the salts), and nobody can see that Tom and Lina have the same password. 🛡️

### 🐢 Slow on purpose

A computer can try **billions** of guesses per second with simple hashes. So password hashes should be **slow** — not slow for **one** login (a fraction of a second is fine), but **way** too slow for **billions** of guesses. 🐢

**BCrypt** does **all** of this: salt 🧂 + slow 🐢. It's the default in Spring Security. 👍

---

## 🔬 Part 3: BCrypt in Java

Let's try it! Create a small class with a `main` method in **`com.example.school`** (we'll delete it afterwards):

**`PasswordDemo.java`**

```java
package com.example.school;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

public class PasswordDemo {

    public static void main(String[] args) {
        PasswordEncoder encoder = new BCryptPasswordEncoder();

        long start = System.currentTimeMillis();
        String hash1 = encoder.encode("secret123");
        long time = System.currentTimeMillis() - start;
        String hash2 = encoder.encode("secret123");

        System.out.println("Hash 1: " + hash1);
        System.out.println("Hash 2: " + hash2);
        System.out.println("Same hash?            " + hash1.equals(hash2));
        System.out.println("secret123 matches?    " + encoder.matches("secret123", hash1));
        System.out.println("Secret123 matches?    " + encoder.matches("Secret123", hash1));
        System.out.println("Time for one hash:    " + time + " ms");
    }
}
```

| Code | Meaning |
|---|---|
| `PasswordEncoder encoder = new BCryptPasswordEncoder();` | A `PasswordEncoder` (an **interface**, Chapter 25) that uses the BCrypt recipe. |
| `encoder.encode("secret123")` | **Hash** the password: new random salt 🧂 + slow blending 🐢. |
| `System.currentTimeMillis()` | The time now, in milliseconds. "After minus before" = how long it took. ⏱️ |
| `hash1.equals(hash2)` | Are the two hashes of the **same** password equal? |
| `encoder.matches("secret123", hash1)` | ⭐ "Does this **password** fit this **hash**?" It takes the salt **out of** the hash, blends again, and compares. |

Click the green ▶️ next to `main`. Our real output:

```
Hash 1: $2a$10$.QGfQshi3pExWohjowagLuw6EB7piyVUOaudeHcSxG7GvRt34YIIq
Hash 2: $2a$10$j0JoyvLWUHs8dqtPO9iiSugixvPG7Qh9B/Xm23QoshIRsQcMVOAHW
Same hash?            false
secret123 matches?    true
Secret123 matches?    false
Time for one hash:    182 ms
```

Your hashes will look **different** (new random salts!), but the `true`/`false` answers will be the same. Look at what happened:

- 🧂 The **same** password gave **two different** hashes — thanks to the salt.
- ✅ `matches` still knows `secret123` is correct for hash 1.
- ❌ `Secret123` (big **S**) doesn't match. Passwords are **case-sensitive**.
- 🐢 One hash took about **0.2 seconds** — nothing for one login, but **forever** for a billion guesses.

### 🔍 Inside a BCrypt hash

```
 $2a$10$.QGfQshi3pExWohjowagLu w6EB7piyVUOaudeHcSxG7GvRt34YIIq
 └┬┘└┬┘ └──────────┬─────────┘ └──────────────┬──────────────┘
  │  │            salt 🧂 (22 letters)         the real hash (31 letters)
  │  └─ cost 10: how slow (bigger = slower 🐢)
  └─ "this is BCrypt, version 2a"
```

The salt is **stored inside** the hash — that's how `matches` can find it again. 🤓 A salt doesn't need to be secret; it only needs to be **different** for every password.

Delete `PasswordDemo.java` when you're done. 🗑️

---

## 🔧 Part 4: The `PasswordEncoder` bean

Our app needs **one** `PasswordEncoder` that everybody can use. Add a `@Bean` method to **`SecurityConfig`**:

```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();
}
```

(Imports: `org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder` and `org.springframework.security.crypto.password.PasswordEncoder`.)

| Code | Meaning |
|---|---|
| `@Bean` | Spring keeps this object and **injects** it wherever someone asks for a `PasswordEncoder` (Chapter 54). |
| `return new BCryptPasswordEncoder();` | Our choice: BCrypt. |

Spring Security uses this bean **automatically** to check passwords at login. And **we** will use it to hash new passwords at **register**. Same bean, same recipe. 🤝

---

## 🗄️ Part 5: A table for users

A user needs: an **id**, a **username**, a **password hash**, and a **role** (what kind of user: we'll use `"USER"` for now — roles are the next chapter's big topic).

**`entity/AppUser.java`**

```java
package com.example.school.entity;

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

    public void setPassword(String password) {
        this.password = password;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }
}
```

| Code | Meaning |
|---|---|
| `class AppUser` | Why not just `User`? Because Spring Security **already** has a class called `User` — two `User`s in one file would be confusing. 😵 |
| `@Table(name = "app_users")` | ⚠️ **Not** `user`! `USER` is a **reserved word** in H2 (and in PostgreSQL) — just like `YEAR` in Chapter 68. |
| `unique = true` on `username` | Two users can't have the same name. 🚫👯 |
| `private String password;` | ⚠️ The name says "password", but we'll **only** ever put a **hash** in it. |
| `@Column(nullable = false)` on `password` | No length: a BCrypt hash is always 60 letters, and the default (255) is plenty. |
| `protected AppUser() { }` | The empty constructor that JPA needs (Chapter 71). |
| `setPassword`, `setRole` | For changing a password (mini project) and a role (next chapter). No `setUsername` — names don't change. |

And the repository:

**`repository/AppUserRepository.java`**

```java
package com.example.school.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.school.entity.AppUser;

public interface AppUserRepository extends JpaRepository<AppUser, Long> {

    Optional<AppUser> findByUsername(String username);

    boolean existsByUsername(String username);
}
```

| Code | Meaning |
|---|---|
| `Optional<AppUser> findByUsername(String username)` | A **query method** (Chapter 74): `SELECT ... WHERE username = ?`. `Optional`, because maybe nobody has that name (Chapter 37). |
| `boolean existsByUsername(String username)` | "Is this name already taken?" → `true`/`false`. |

Start the app: Hibernate makes the new table for us (`ddl-auto=update`). From the log:

```sql
    create table app_users (
        id bigint generated by default as identity,
        password varchar(255) not null,
        role varchar(20) not null,
        username varchar(30) not null,
        primary key (id)
    )
```

---

## 🔎 Part 6: `UserDetailsService` — how Spring finds a user

When someone logs in, Spring Security has a name and a password — but it doesn't know about **our** `app_users` table! 🤷 We must give it a helper that **finds** users. That helper is a **`UserDetailsService`**: an interface with **one** method.

Create a new package **`security`** and this class in it:

**`security/SchoolUserDetailsService.java`**

```java
package com.example.school.security;

import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import com.example.school.entity.AppUser;
import com.example.school.repository.AppUserRepository;

@Service
public class SchoolUserDetailsService implements UserDetailsService {

    private final AppUserRepository appUserRepository;

    public SchoolUserDetailsService(AppUserRepository appUserRepository) {
        this.appUserRepository = appUserRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String username) {
        AppUser appUser = appUserRepository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("No user with the name " + username));
        return User.withUsername(appUser.getUsername())
                .password(appUser.getPassword())
                .roles(appUser.getRole())
                .build();
    }
}
```

| Code | Meaning |
|---|---|
| `implements UserDetailsService` | "I keep the promise (Chapter 25): I can **find** users." Spring Security looks for a bean like this. |
| `loadUserByUsername(String username)` | Spring calls this at **every** login with the name the user typed. |
| `findByUsername(username).orElseThrow(...)` | Find the user — or throw **`UsernameNotFoundException`** if there's nobody with that name. Spring knows this exception → login fails → **401**. |
| `User.withUsername(...)` | ⭐ Spring Security's **own** `User` class (not ours!). We copy our `AppUser` into Spring's "user card" 🪪. |
| `.password(appUser.getPassword())` | The **hash** from the database. Spring will check the typed password against it with our `PasswordEncoder`. |
| `.roles(appUser.getRole())` | What the user may do — `"USER"` for now. (Next chapter!) |
| `.build()` | Make the finished `UserDetails` object. |

Notice: **we** never compare passwords! We only **find** the user. Spring does the checking. Here's the whole login, step by step:

```
 curl -u sara:sunflower7 ...
    │
    ▼
 💂 BasicAuthenticationFilter: "Name: sara, password: sunflower7"
    │
    ▼
 🧠 Spring Security asks our SchoolUserDetailsService: loadUserByUsername("sara")
    │                                         └─► SELECT ... FROM app_users WHERE username='sara'
    ▼
 🪪 UserDetails { name: sara, password: $2a$10$.CVT91..., roles: USER }
    │
    ▼
 🔐 passwordEncoder.matches("sunflower7", "$2a$10$.CVT91...")
    │
    ├── true  ✅ → logged in! → on to the next filters and the controller
    └── false ❌ → 401
```

When the app starts, the log confirms that Spring found our helper:

```
Global AuthenticationManager configured with UserDetailsService bean with name schoolUserDetailsService
```

And there's **no** "Using generated security password" message anymore — Spring Boot only makes its `user` when **we** don't give it a `UserDetailsService`. So **remove** these two lines from `application.properties` — they do nothing now:

```properties
# One fixed user (only for learning!)
spring.security.user.name=teacher
spring.security.user.password=secret123
```

---

## 👩‍🏫 Part 7: Our first user from the database

The `app_users` table is **empty** — nobody can log in! 😅 Let's add the teacher automatically at start, like the `DataLoader` adds students (Chapter 73). We make a **separate** loader for users:

**`security/UserLoader.java`**

```java
package com.example.school.security;

import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import com.example.school.entity.AppUser;
import com.example.school.repository.AppUserRepository;

@Component
public class UserLoader implements CommandLineRunner {

    private final AppUserRepository appUserRepository;
    private final PasswordEncoder passwordEncoder;

    public UserLoader(AppUserRepository appUserRepository, PasswordEncoder passwordEncoder) {
        this.appUserRepository = appUserRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public void run(String... args) {
        if (!appUserRepository.existsByUsername("teacher")) {
            appUserRepository.save(new AppUser("teacher", passwordEncoder.encode("secret123"), "USER"));
            System.out.println("UserLoader: added the user teacher");
        }
    }
}
```

| Code | Meaning |
|---|---|
| `implements CommandLineRunner` | `run` is called **once**, right after the app has started (Chapter 73). |
| `PasswordEncoder passwordEncoder` | We get **our** BCrypt bean injected. |
| `if (!appUserRepository.existsByUsername("teacher"))` | Only if the teacher doesn't exist yet → no duplicate at the next start. |
| `passwordEncoder.encode("secret123")` | ⭐ Hash **before** saving. The database only ever sees `$2a$10$...`. |

🤔 **Why not put this in `DataLoader`?** Because `DataLoader` stops early (`return`) when there are already students — and your database **has** students from Part 9! A separate loader keeps things simple. 👍

Restart. The log says:

```
UserLoader: added the user teacher
```

And `curl -u teacher:secret123 ...` works exactly like before — but now the teacher lives in the **database**. 🎉

⚠️ Yes, `"secret123"` is still written in the Java code. That's OK for a **learning** project. In Chapter 82, you'll learn to take such passwords from **outside** the code.

---

## 📝 Part 8: Register — making new users

Now anyone should be able to **sign up**: `POST /api/auth/register` with a name and a password. Let's build it, layer by layer (Chapter 63).

**1. The DTOs** — what comes in, and what goes out (Chapter 64):

**`dto/RegisterRequest.java`**

```java
package com.example.school.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record RegisterRequest(
        @NotBlank(message = "Username is required")
        @Size(min = 3, max = 30, message = "Username must have 3 to 30 characters")
        String username,

        @NotBlank(message = "Password is required")
        @Size(min = 8, max = 100, message = "Password must have at least 8 characters")
        String password) {
}
```

**`dto/UserResponse.java`**

```java
package com.example.school.dto;

import com.example.school.entity.AppUser;

public record UserResponse(Long id, String username, String role) {

    public static UserResponse from(AppUser appUser) {
        return new UserResponse(appUser.getId(), appUser.getUsername(), appUser.getRole());
    }
}
```

| Code | Meaning |
|---|---|
| `@Size(min = 8, ...)` on `password` | Short passwords are easy to guess. 8 is the minimum many websites use. |
| `record UserResponse(Long id, String username, String role)` | ⭐ What we send **back**. Look: **no password field!** Not even the hash ever leaves the server. 🔒 |

**2. A new exception** for a name that's already taken:

**`exception/UsernameTakenException.java`**

```java
package com.example.school.exception;

public class UsernameTakenException extends RuntimeException {

    public UsernameTakenException(String username) {
        super("The username " + username + " is already taken");
    }
}
```

And its handler in **`GlobalExceptionHandler`** (409 Conflict, like `EmailAlreadyUsedException`):

```java
@ExceptionHandler(UsernameTakenException.class)
public ProblemDetail handleUsernameTaken(UsernameTakenException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, ex.getMessage());
    problem.setTitle("Username taken");
    return problem;
}
```

**3. The service:**

**`service/UserService.java`**

```java
package com.example.school.service;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.school.dto.RegisterRequest;
import com.example.school.dto.UserResponse;
import com.example.school.entity.AppUser;
import com.example.school.exception.UsernameTakenException;
import com.example.school.repository.AppUserRepository;

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
        AppUser saved = appUserRepository.save(new AppUser(request.username(), hash, "USER"));
        return UserResponse.from(saved);
    }
}
```

| Code | Meaning |
|---|---|
| `existsByUsername(...)` → `throw` | Name taken? → **409**. |
| `passwordEncoder.encode(request.password())` | ⭐ Hash it **right away**. The plain password is never saved. |
| `new AppUser(..., hash, "USER")` | Every new user gets the role `"USER"`. Nobody can register as something more powerful! |
| `@Transactional` | The check and the save are one job (Chapter 79). |

**4. The controller:**

**`controller/AuthController.java`**

```java
package com.example.school.controller;

import jakarta.validation.Valid;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.school.dto.RegisterRequest;
import com.example.school.dto.UserResponse;
import com.example.school.service.UserService;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserService userService;

    public AuthController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping("/register")
    public ResponseEntity<UserResponse> register(@Valid @RequestBody RegisterRequest request) {
        UserResponse created = userService.register(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

| Code | Meaning |
|---|---|
| `@RequestMapping("/api/auth")` | Everything about logging in lives under `/api/auth`. |
| `ResponseEntity.status(HttpStatus.CREATED).body(created)` | **201 Created**, with the new user in the body (Chapter 62). |

**5. Open the door!** 🚪 Strangers must be able to register — that's the whole point. But `POST` needs a login right now (`anyRequest().authenticated()`). Add a rule at the **top** in `SecurityConfig`:

```java
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(HttpMethod.POST, "/api/auth/register").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/students/search").authenticated()
                .requestMatchers(HttpMethod.GET, "/api/**").permitAll()
                .requestMatchers("/h2-console/**").permitAll()
                .requestMatchers("/error").permitAll()
                .anyRequest().authenticated())
```

### 🧪 Test it

```bash
curl -i -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"sara","password":"sunflower7"}'
```

```
HTTP/1.1 201 
Content-Type: application/json

{"id":2,"username":"sara","role":"USER"}
```

🎉 Sara has an account — and no password in the answer. Now Sara can log in:

```bash
curl -i -u sara:sunflower7 -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Omar Ali","email":"omar@school.com","age":12}'
```

That works (**201**) — hmm, wait... 😟 Sara is a **student**, and she can add students. She could **delete** them too (we tried: `DELETE` as `sara` → **204**)! **Any** new user can do **everything**?! We'll fix that with **roles** in the next chapter. For now, our real tests of the other cases:

**The same name again:**

```bash
curl -i -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"sara","password":"other1234"}'
```

```
HTTP/1.1 409 
Content-Type: application/problem+json

{"detail":"The username sara is already taken","instance":"/api/auth/register","status":409,"title":"Username taken"}
```

**Too short:**

```bash
curl -i -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"x","password":"123"}'
```

```
HTTP/1.1 400 
Content-Type: application/problem+json

{"detail":"The request has 2 invalid field(s)","instance":"/api/auth/register","status":400,"title":"Invalid data","errors":{"password":"Password must have at least 8 characters","username":"Username must have 3 to 30 characters"}}
```

✅ All our Part 8 skills work here too: validation, ProblemDetail, the 409.

### 👀 Look inside the database

Open the H2 Console and run `SELECT * FROM APP_USERS;`. Our real result:

```
ID | PASSWORD                                                     | ROLE | USERNAME
 1 | $2a$10$dOIboiyrIvCTbc48iDDKruFP8SXeE8ar0ZqgMpRwG1shN2TcvjocW | USER | teacher
 2 | $2a$10$.CVT91t0He3k.tEX73fqee2frlpBy/nKExQ2sctEEOUMuSCOaRTw. | USER | sara
```

🎉 **No** readable passwords. Even **you** can't tell what Sara's password is. That's exactly how it should be! 🔒

---

## 🙋 Part 9: Who am I? — `GET /api/auth/me`

Inside a controller, how do you know **who** is calling? Just ask Spring for an **`Authentication`** — add it as a method parameter, and Spring fills it in! 🪄

Add this method to **`AuthController`**, plus a small DTO:

**`dto/CurrentUserResponse.java`**

```java
package com.example.school.dto;

import java.util.List;

public record CurrentUserResponse(String username, List<String> authorities) {
}
```

**In `AuthController`:**

```java
@GetMapping("/me")
public CurrentUserResponse me(Authentication authentication) {
    List<String> authorities = authentication.getAuthorities().stream()
            .map(GrantedAuthority::getAuthority)
            .toList();
    return new CurrentUserResponse(authentication.getName(), authorities);
}
```

(Imports: `java.util.List`, `org.springframework.security.core.Authentication`, `org.springframework.security.core.GrantedAuthority`, `org.springframework.web.bind.annotation.GetMapping`, `com.example.school.dto.CurrentUserResponse`.)

| Code | Meaning |
|---|---|
| `Authentication authentication` | ⭐ Spring Security's note about the **logged-in** user: the name, the **authorities** (what they may do), and more. |
| `authentication.getName()` | The username: `"sara"`. |
| `authentication.getAuthorities()` | A collection of `GrantedAuthority` objects: the user's "permission stamps". 🏷️ |
| `.stream().map(GrantedAuthority::getAuthority).toList()` | Turn each stamp into its text (Chapter 36). `GrantedAuthority::getAuthority` is a **method reference**: a short way to write `a -> a.getAuthority()`. |

One more rule in `SecurityConfig`, because `/me` is a `GET /api/...` — and those are open to strangers. But a stranger has **no** "me"! So, near the top:

```java
                .requestMatchers(HttpMethod.GET, "/api/auth/me").authenticated()
```

(It must come **before** `GET /api/**`. You'll see in "Common mistakes" what happens without it. 💥)

```bash
curl -i -u sara:sunflower7 http://localhost:8080/api/auth/me
```

Our real answer:

```
HTTP/1.1 200 
Content-Type: application/json

{"username":"sara","authorities":["ROLE_USER","FACTOR_PASSWORD"]}
```

| Authority | Meaning |
|---|---|
| `ROLE_USER` | Sara has the role `USER`. `.roles("USER")` in our `UserDetailsService` added the prefix `ROLE_` (more in the next chapter). |
| `FACTOR_PASSWORD` | A stamp that Spring Security 7 adds by itself: "This person proved who they are with a **password**." (Big apps use this for **two-step** logins — password **and** a code from your phone 📱. We won't need it.) |

And **without** a login → **401**, like every locked URL. ✅

---

## 💻 Mini project: Change your password 🔑

Users should be able to change their own password:

```
PUT /api/auth/password
{"currentPassword":"sunflower7","newPassword":"rainbow42"}
```

**Rules:**

1. Only for **logged-in** users (they change **their own** password).
2. The **current** password must be right — otherwise **400** with the title `"Wrong password"`. (Why ask again? If Sara forgets to log out at a library computer, a stranger can't lock her out! 🔐)
3. The new password must have at least 8 characters.
4. Answer: **204 No Content**.
5. After the change, the **old** password must **stop** working.

**Hints:** a `ChangePasswordRequest` record, a `WrongPasswordException`, a `changePassword(String username, ChangePasswordRequest request)` method in `UserService`, and `authentication.getName()` in the controller. Do you need a new rule in `SecurityConfig`? 🤔

<details>
<summary>Click to see the answer</summary>

**`dto/ChangePasswordRequest.java`**

```java
package com.example.school.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record ChangePasswordRequest(
        @NotBlank(message = "Current password is required")
        String currentPassword,

        @NotBlank(message = "New password is required")
        @Size(min = 8, max = 100, message = "Password must have at least 8 characters")
        String newPassword) {
}
```

**`exception/WrongPasswordException.java`**

```java
package com.example.school.exception;

public class WrongPasswordException extends RuntimeException {

    public WrongPasswordException() {
        super("The current password is wrong");
    }
}
```

**In `GlobalExceptionHandler`:**

```java
@ExceptionHandler(WrongPasswordException.class)
public ProblemDetail handleWrongPassword(WrongPasswordException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, ex.getMessage());
    problem.setTitle("Wrong password");
    return problem;
}
```

**In `UserService`:**

```java
@Transactional
public void changePassword(String username, ChangePasswordRequest request) {
    AppUser appUser = appUserRepository.findByUsername(username).orElseThrow();
    if (!passwordEncoder.matches(request.currentPassword(), appUser.getPassword())) {
        throw new WrongPasswordException();
    }
    appUser.setPassword(passwordEncoder.encode(request.newPassword()));
}
```

| Code | Meaning |
|---|---|
| `findByUsername(username).orElseThrow()` | The user **is** logged in, so they **must** exist. `orElseThrow()` without arguments throws `NoSuchElementException` — it should never happen. |
| `passwordEncoder.matches(current, hash)` | Check the **current** password, exactly like a login does. |
| `appUser.setPassword(passwordEncoder.encode(...))` | Save the **hash** of the new password. No `save` call needed: **dirty checking** writes it at the end of the transaction (Chapter 79)! 🧹 |

**In `AuthController`:**

```java
@PutMapping("/password")
@ResponseStatus(HttpStatus.NO_CONTENT)
public void changePassword(Authentication authentication, @Valid @RequestBody ChangePasswordRequest request) {
    userService.changePassword(authentication.getName(), request);
}
```

| Code | Meaning |
|---|---|
| `authentication.getName()` | ⭐ The name comes from the **login**, not from the request body. So Sara can only change **Sara's** password — never Tom's! 🛡️ |

**No new rule needed:** `PUT /api/auth/password` falls under `anyRequest().authenticated()`. ✅

Our real tests:

```bash
curl -i -u sara:sunflower7 -X PUT http://localhost:8080/api/auth/password \
  -H "Content-Type: application/json" \
  -d '{"currentPassword":"nope","newPassword":"rainbow42"}'
```

```
HTTP/1.1 400 
Content-Type: application/problem+json

{"detail":"The current password is wrong","instance":"/api/auth/password","status":400,"title":"Wrong password"}
```

```bash
curl -i -u sara:sunflower7 -X PUT http://localhost:8080/api/auth/password \
  -H "Content-Type: application/json" \
  -d '{"currentPassword":"sunflower7","newPassword":"rainbow42"}'
```

```
HTTP/1.1 204 
```

Then `curl -i -u sara:sunflower7 .../api/auth/me` → **401** (the old password is dead ☠️), and `curl -i -u sara:rainbow42 .../api/auth/me` → **200** ✅. Without a login, `PUT /api/auth/password` → **401**.

</details>

---

## ✋ Try it yourself

1. Register **two** users with the **same** password (for example `tom` and `lina`, both `football1`). Look at their hashes in the H2 Console. Are they the same?
2. Try to log in with a **wrong password** for `sara`, and with a name that **doesn't exist**, like `nobody`. Compare the two answers.
3. In `PasswordDemo`, use `new BCryptPasswordEncoder(14)` instead. What changes in the hash, and in the time?
4. Register a user called `Sara` (big S). Does it work? Can `Sara` log in as `sara`?

<details>
<summary>Click to see the answers</summary>

1. No — they're totally different, thanks to the **salt** 🧂. Nobody looking at the table can see that Tom and Lina share a password.
2. Both give exactly the same **401** answer. That's **on purpose**: if the answer for "this name doesn't exist" were different, a bad person could find out **which** usernames exist. 🕵️ (Inside, Spring even does fake password work for unknown names, so the time is about the same too.)
3. The hash starts with `$2a$14$` — cost 14. Each step up **doubles** the work, so 14 is 2×2×2×2 = **16 times** slower than 10. (On our computer: `Time for one hash: 1303 ms` instead of 182 ms. The very first hash also includes some warm-up time, so the numbers aren't exactly 16 times apart.) A higher cost is safer, but every login gets slower too. ⚖️ The default, 10, is a good choice for us.
4. It works: `existsByUsername("Sara")` is `false`, because `Sara` and `sara` are different texts in our H2 database. `Sara` logs in with **her own** password. (Real apps often turn names into small letters before saving, so `Sara` and `sara` can't **both** exist. You could do that with `request.username().toLowerCase()`.)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Saving the password without hashing it

```java
appUserRepository.save(new AppUser("teacher", "secret123", "USER"));   // ❌ plain text!
```

Not only is it unsafe — the login **doesn't work** either! The `PasswordEncoder` expects a BCrypt hash. Our real result: `curl -u teacher:secret123 ...` → **401**, and the log says:

```
WARN ... o.s.s.c.bcrypt.BCryptPasswordEncoder     : Encoded password does not look like BCrypt
```

**Fix:** **Always** `passwordEncoder.encode(...)` before saving.

### Mistake 2: Forgetting the `PasswordEncoder` bean

The app doesn't start. Our real error:

```
***************************
APPLICATION FAILED TO START
***************************

Description:

Parameter 1 of constructor in com.example.school.service.UserService required a bean of type 'org.springframework.security.crypto.password.PasswordEncoder' that could not be found.


Action:

Consider defining a bean of type 'org.springframework.security.crypto.password.PasswordEncoder' in your configuration.
```

**Fix:** Add the `@Bean public PasswordEncoder passwordEncoder()` method to `SecurityConfig` (Part 4).

### Mistake 3: A table called `user`

With `@Table(name = "user")`, Hibernate can't even make the table. Our real log:

```
WARN ... GenerationTarget encountered exception accepting command : Error executing DDL "
    create table [*]user ( ... )"; expected "identifier";
```

...and then the app crashes when `UserLoader` runs: `Syntax error in SQL statement "select au1_0.id from [*]user au1_0 ..."`. The `[*]` points at the problem: `user` is a **reserved word**. **Fix:** `@Table(name = "app_users")`.

### Mistake 4: `/me` without its rule

Without `.requestMatchers(HttpMethod.GET, "/api/auth/me").authenticated()`, the request matches `GET /api/**` → **open to strangers**. A stranger has no `Authentication`, so the parameter is **`null`**. Our real answer:

```
HTTP/1.1 500 
Content-Type: application/problem+json

{"detail":"Something went wrong on our side. Please try again later.","instance":"/api/auth/me","status":500,"title":"Server error"}
```

And the log: `NullPointerException: Cannot invoke "org.springframework.security.core.Authentication.getAuthorities()" because "authentication" is null`. **Fix:** Every endpoint that **needs** to know the user must be **locked**.

### Mistake 5: Sending the entity back

```java
public AppUser register(...)   // ❌ returns the entity
```

The JSON would contain `"password":"$2a$10$..."`. Even a hash should **never** leave the server. **Fix:** Always answer with a **DTO** like `UserResponse` (Chapter 64).

### Mistake 6: Telling strangers too much

```java
throw new RuntimeException("Wrong password for sara");   // ❌ now they know sara exists!
```

**Fix:** Login errors should always say the same thing, whatever went wrong. Spring Security already does this for you (Try it 2).

---

## ✅ Summary

- 🏆 **Never** store passwords — store **hashes**. A hash is **one-way** 🥤: you check a password by hashing it again and comparing.
- A **salt** 🧂 makes equal passwords get different hashes. **BCrypt** = salt + slow on purpose 🐢. A BCrypt hash looks like `$2a$10$<salt><hash>`.
- **`PasswordEncoder`**: `encode(password)` to hash, `matches(password, hash)` to check. Make **one** `@Bean` with `new BCryptPasswordEncoder()`.
- Users live in our own entity **`AppUser`** (table **`app_users`** — `user` is reserved!).
- A **`UserDetailsService`** **finds** users for Spring Security. It returns a `UserDetails` card 🪪; Spring checks the password itself.
- **Register**: validate, check the name, **hash**, save, and answer with a **DTO** without the password. Open the URL with `permitAll()`.
- Add an **`Authentication`** parameter to a controller method to know **who** is calling. Lock such URLs!

---

## ❓ Quiz

1. Why must we never store passwords as plain text?
2. If a hash can't be turned back into a password, how does a login check work?
3. What does a salt do?
4. Why is BCrypt slow on purpose?
5. What does `loadUserByUsername` do? Does it check the password?
6. Why is our entity called `AppUser` and our table `app_users`?
7. Why does `UserResponse` have no `password` field?
8. In the mini project, why does the username come from `authentication.getName()` and not from the request body?

<details>
<summary>Click to see the answers</summary>

1. If the database ever leaks, everyone could read the passwords and log in as any user — and try the same passwords on other websites.
2. The login hashes the typed password again (with the same salt, which is stored in the hash) and compares the result with the saved hash.
3. It adds a random extra ingredient before hashing, so equal passwords get different hashes. Ready-made lists of hashes become useless.
4. So that guessing billions of passwords takes far too long. One login is still fast enough.
5. It finds a user by name and returns a `UserDetails` (name, hash, roles) — or throws `UsernameNotFoundException`. It does **not** check the password; Spring does that with the `PasswordEncoder`.
6. Spring Security already has a class `User`, and `user` is a reserved word in H2 and PostgreSQL.
7. Not even a hash should ever leave the server. The DTO decides exactly what the client sees.
8. So users can only change **their own** password. The login proves who they are; a body could contain anybody's name.

</details>

---

[⬅ Previous chapter](80-spring-security.md) | [Table of Contents](../README.md) | [Next chapter: Roles: admin and user ➡](82-roles.md)
