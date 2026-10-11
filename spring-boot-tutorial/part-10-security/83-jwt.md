# Chapter 83 – JWT tokens

[⬅ Previous chapter](82-roles.md) | [Table of Contents](../README.md) | [Next chapter ➡](../part-11-testing/84-junit.md)

---

## 🎯 Goal

Until now, the client sent the **name and password** with **every** request (HTTP Basic). That works — but it's not how modern apps do it. 📱 When you log in to a game or a shopping app, you type your password **once**, and then the app uses a **token** 🎟️.

Today you'll build that! At the end of this chapter you will know:

- What a **token** is, and why it's better than sending the password every time 🎟️
- What a **JWT** looks like inside: **header**, **payload**, **signature** 🔍
- Why nobody can **fake** or **change** a JWT ✍️
- How to build **`POST /api/auth/login`**, which gives out tokens
- How to make Spring **check** tokens: the **resource server** 🛡️
- What happens when a token is **expired** or **changed** ⏰
- The **price** of tokens: you can't take them back 🤔

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Token** | A small piece of text that proves "I already logged in". Like a ticket. 🎟️ |
| **JWT** | **J**SON **W**eb **T**oken: a very popular kind of token. Say "jot". |
| **Claim** | One piece of information inside a JWT, like `"sub":"teacher"` ("the user is teacher"). |
| **Header** | The first part of a JWT: **how** the token is signed. |
| **Payload** | The second part of a JWT: the **claims** (who, which roles, until when). 📦 |
| **Signature** | The third part: a **seal** ✍️ made with a secret key. If anyone changes the token, the seal breaks. |
| **Secret key** | A long secret text that only the **server** knows. It makes and checks signatures. 🔑 |
| **HS256** | The recipe we use for the signature (HMAC with SHA-256). |
| **Bearer** | "The one who **carries** it." `Authorization: Bearer <token>` means "Let in whoever carries this token." |
| **Expire** | To stop working after some time. ⏰ |
| **Resource server** | A server that **checks tokens** before it gives out its data (its "resources"). Our app! |
| **Encode / decode** | Turn something **into** a coded form / turn it **back**. |

---

## 📖 Story: The wristband at the festival 🎪

Lina goes to a big music festival. 🎶 At the **entrance**, she shows her **ticket** and her **ID card**. The guard checks them carefully — that takes a minute. ⏳

Then the guard puts a **wristband** 🎟️ on her arm. On it is printed:

```
 ┌───────────────────────────────────────┐
 │ 🎪 SUMMER FEST                         │
 │ Name: Lina      Area: VIP ⭐           │
 │ Valid until: Saturday 23:59           │
 │ ✍️ official seal (can't be copied!)    │
 └───────────────────────────────────────┘
```

For the rest of the day, Lina **never** shows her ticket and ID again. At every stage, the guards just look at the **wristband**: 👀 "Seal OK? Still valid? VIP? → Come in!" That's **fast**.

- Could Lina **change** "Area: normal" into "Area: VIP" with a pen? 🖊️ No — the **seal** would break, and the guards would see it.
- On Sunday, the wristband is **expired** ⏰. Lina needs a new ticket.
- But: if Lina **loses** her wristband, whoever finds it can use it — **until Saturday 23:59**. 😟

That's **exactly** how a JWT works:

| Festival 🎪 | Our app 💻 |
|---|---|
| Ticket + ID at the entrance | `POST /api/auth/login` with name + password (**once**) |
| The wristband 🎟️ | The **JWT** |
| "Name: Lina, Area: VIP" | The **claims**: `"sub":"lina"`, `"roles":["TEACHER"]` |
| The official seal ✍️ | The **signature**, made with the secret key 🔑 |
| "Valid until Saturday 23:59" | The **`exp`** claim |
| Guards look at the wristband | Spring checks the token in **every** request |

---

## 🤔 Part 1: Why tokens?

With **HTTP Basic**, every single request carries the password:

```
 GET  /api/students      Authorization: Basic dGVhY2hlcjpzZWNyZXQxMjM=   🔑
 POST /api/students      Authorization: Basic dGVhY2hlcjpzZWNyZXQxMjM=   🔑
 GET  /api/courses       Authorization: Basic dGVhY2hlcjpzZWNyZXQxMjM=   🔑
 ...  100 more requests, 100 more times the password 😟
```

That has some problems:

| Problem with Basic | Why it's bad |
|---|---|
| The password travels **all the time** 🔑🔑🔑 | More chances for it to leak (a log file, a bug, a spy...). |
| The client must **keep** the password | A phone app would have to save your password somewhere. 😬 |
| The server checks the password **every** time | Remember? One BCrypt check takes about **0.2 seconds** on purpose 🐢 (Chapter 81) — for **every** request! |
| The password **never expires** | A stolen password works **forever** (until it's changed). |

With a **token**, it looks like this:

```
 1. POST /api/auth/login   {"username":"teacher","password":"secret123"}     🔑 ONCE
    ◄── 200  {"token":"eyJraWQi...","tokenType":"Bearer","expiresIn":3600}   🎟️

 2. GET  /api/students     Authorization: Bearer eyJraWQi...   🎟️ (no password!)
 3. POST /api/students     Authorization: Bearer eyJraWQi...   🎟️
 4. ...                    the token works for 1 hour ⏰
```

✅ The password travels **once**. ✅ The token **expires**. ✅ Checking a token is **fast** — no database, no BCrypt. 🚀

---

## 🔍 Part 2: What a JWT looks like

Here's a **real** token from our app (made when the teacher logged in):

```
eyJraWQiOiJzSloxTlVnVzBETGlnMkJ1VXhFQTQxNGtXNXNDYXhOOFI2Y3lhcWlZaEswIiwiYWxnIjoiSFMyNTYifQ.eyJpc3MiOiJzY2hvb2wiLCJzdWIiOiJ0ZWFjaGVyIiwiZXhwIjoxNzkxNzA1NTYyLCJpYXQiOjE3OTE3MDE5NjIsInJvbGVzIjpbIlRFQUNIRVIiXX0.gd7kkCWQh8YRSluOqwI_ctC61T83Pa0OrczveMPOvo0
```

😵 Looks like nonsense? Look closer: there are **two dots** `.` — they split the token into **three parts**:

```
 eyJraWQi...MEiJ9  .  eyJpc3Mi...XX0  .  gd7kkCWQ...Ovo0
 └──── header ───┘    └── payload ──┘    └─ signature ─┘
      🏷️ how              📦 what            ✍️ the seal
```

The header and the payload are just **JSON** written in **Base64** (like the Basic header in Chapter 80 — readable by anyone!). Let's decode the **payload** in Git Bash:

```bash
echo eyJpc3MiOiJzY2hvb2wiLCJzdWIiOiJ0ZWFjaGVyIiwiZXhwIjoxNzkxNzA1NTYyLCJpYXQiOjE3OTE3MDE5NjIsInJvbGVzIjpbIlRFQUNIRVIiXX0 | base64 -d
```

```
{"iss":"school","sub":"teacher","exp":1791705562,"iat":1791701962,"roles":["TEACHER"]}base64: invalid input
```

(The `base64: invalid input` at the end is harmless: JWTs leave out the `=` signs that `base64` expects at the end. The JSON is all there. 👍)

**The payload** — our **claims**:

| Claim | Value | Meaning |
|---|---|---|
| `iss` | `"school"` | **Iss**uer: **who** made this token. Our app! |
| `sub` | `"teacher"` | **Sub**ject: **who** the token is about — the username. |
| `iat` | `1791701962` | **I**ssued **at**: **when** it was made. |
| `exp` | `1791705562` | **Exp**ires: when it stops working. ⏰ |
| `roles` | `["TEACHER"]` | **Our own** claim: the user's roles. |

🤔 What are those big numbers? Computers often count time as **seconds since 1 January 1970**. `1791705562 - 1791701962 = 3600` seconds = **1 hour**. So this token lives for one hour. ⏰

**The header** — decode the first part the same way:

```
{"kid":"sJZ1NUgW0DLig2BuUxEA414kW5sCaxN8R6cyaqiYhK0","alg":"HS256"}
```

| Field | Meaning |
|---|---|
| `alg` | `"HS256"`: the signature was made with the **HS256** recipe and a secret key. |
| `kid` | **K**ey **id**: a "name" for the key that made the signature. Spring makes it from our key automatically. (Servers with **many** keys use it to know which one to use.) |

**The signature** ✍️ — this part is **not** JSON. It's a "fingerprint" made from the header + the payload + our **secret key**:

```
 signature = HS256( header + "." + payload , 🔑 secret key )
```

Only someone who knows the **secret key** can make the right signature. That's **our server** — and nobody else! 🔐

### ⚠️ Readable, but not changeable

| Can a stranger... | Answer |
|---|---|
| **read** the payload? | **Yes!** 👀 It's only Base64. So **never** put secrets (like passwords) into a token! |
| **change** the payload (`"TEACHER"` → `"ADMIN"`)? | They can change the text... but then the signature **doesn't fit** anymore → our server **rejects** it. ❌ (We'll try it in Part 7!) |
| **make** a new token? | **No** — without the secret key, they can't make a valid signature. ❌ |

Just like the festival wristband: everyone can **read** "VIP" on it — but nobody can **fake** the seal. 🎪✍️

---

## 📦 Part 3: The tools — dependency, settings and keys

Spring Security has everything for tokens in **one** starter. Add it to **`pom.xml`**, next to `spring-boot-starter-security`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security-oauth2-resource-server</artifactId>
</dependency>
```

| Code | Meaning |
|---|---|
| `spring-boot-starter-security-oauth2-resource-server` | The "**resource server**" starter: it can **check** JWTs in requests. It also brings **Nimbus**, a library that can **make** JWTs. ("OAuth2" is the name of a big standard for tokens; we only use the token part of it.) |

Next, two settings in **`application.properties`**:

```properties
# JWT tokens
school.jwt.secret=${JWT_SECRET:learning-only-secret-please-change-me-0123456789}
school.jwt.lifetime=1h
```

| Code | Meaning |
|---|---|
| `school.jwt.secret=${JWT_SECRET:...}` | 🔑 The **secret key**. From the environment variable `JWT_SECRET` — or, only for learning, the default text. |
| `learning-only-secret-please-change-me-0123456789` | ⚠️ It must be **long**: at least **32** letters (256 bits) for HS256. Ours has 48. (See "Common mistakes" for what happens with a short one!) |
| `school.jwt.lifetime=1h` | How long a token lives: **1 hour**. Spring understands `30s`, `15m`, `1h`, `2d`... |

⚠️ **The secret key is the most important secret of your app!** Whoever knows it can make tokens for **any** user — even an admin. 👑😈 In a real app, it **only** comes from outside (`JWT_SECRET`), and it's long and random.

Now a configuration class that makes **two** beans — a token **maker** and a token **checker**:

**`config/JwtConfig.java`**

```java
package com.example.school.config;

import java.nio.charset.StandardCharsets;

import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.NimbusJwtDecoder;
import org.springframework.security.oauth2.jwt.NimbusJwtEncoder;

@Configuration
public class JwtConfig {

    private final SecretKey secretKey;

    public JwtConfig(@Value("${school.jwt.secret}") String secret) {
        this.secretKey = new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
    }

    @Bean
    public JwtEncoder jwtEncoder() {
        return NimbusJwtEncoder.withSecretKey(secretKey).build();
    }

    @Bean
    public JwtDecoder jwtDecoder() {
        return NimbusJwtDecoder.withSecretKey(secretKey).build();
    }
}
```

| Code | Meaning |
|---|---|
| `@Value("${school.jwt.secret}") String secret` | Our secret text from the settings. |
| `secret.getBytes(StandardCharsets.UTF_8)` | Turn the text into **bytes** (the computer's raw numbers). A key is made of bytes. |
| `new SecretKeySpec(..., "HmacSHA256")` | Make a real Java **key** 🔑 from those bytes, for the HMAC-SHA256 recipe (= HS256). |
| `JwtEncoder` / `NimbusJwtEncoder.withSecretKey(secretKey).build()` | The token **maker** 🏭: it writes JWTs and **signs** them with our key. |
| `JwtDecoder` / `NimbusJwtDecoder.withSecretKey(secretKey).build()` | The token **checker** 🔍: it reads JWTs and checks the **signature** and the **expiry** time. |

⭐ Maker and checker use the **same** key. The checker can only accept tokens signed by the maker. 🤝

---

## 🏭 Part 4: The token maker — `TokenService`

Now a service that builds a token for a logged-in user:

**`security/TokenService.java`**

```java
package com.example.school.security;

import java.time.Duration;
import java.time.Instant;
import java.util.List;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.oauth2.jose.jws.MacAlgorithm;
import org.springframework.security.oauth2.jwt.JwsHeader;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;
import org.springframework.stereotype.Service;

import com.example.school.dto.TokenResponse;

@Service
public class TokenService {

    private final JwtEncoder jwtEncoder;
    private final Duration lifetime;

    public TokenService(JwtEncoder jwtEncoder, @Value("${school.jwt.lifetime}") Duration lifetime) {
        this.jwtEncoder = jwtEncoder;
        this.lifetime = lifetime;
    }

    public TokenResponse createToken(Authentication authentication) {
        Instant now = Instant.now();
        List<String> roles = authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .filter(authority -> authority.startsWith("ROLE_"))
                .map(authority -> authority.substring("ROLE_".length()))
                .toList();

        JwtClaimsSet claims = JwtClaimsSet.builder()
                .issuer("school")
                .issuedAt(now)
                .expiresAt(now.plus(lifetime))
                .subject(authentication.getName())
                .claim("roles", roles)
                .build();
        JwsHeader header = JwsHeader.with(MacAlgorithm.HS256).build();

        String token = jwtEncoder.encode(JwtEncoderParameters.from(header, claims)).getTokenValue();
        return new TokenResponse(token, "Bearer", lifetime.toSeconds());
    }
}
```

And the DTO for the answer:

**`dto/TokenResponse.java`**

```java
package com.example.school.dto;

public record TokenResponse(String token, String tokenType, long expiresIn) {
}
```

Let's go through `TokenService` slowly:

| Code | Meaning |
|---|---|
| `@Value("${school.jwt.lifetime}") Duration lifetime` | A **`Duration`** is "an amount of time" (Chapter 39). Spring turns `1h` into a `Duration` of one hour by itself. ⏳ |
| `Instant now = Instant.now();` | An **`Instant`** is one exact moment in time — here: **now**. |
| `authentication.getAuthorities().stream()...` | Take the user's authorities, like `ROLE_TEACHER` and `FACTOR_PASSWORD`... |
| `.filter(authority -> authority.startsWith("ROLE_"))` | ...keep only the **roles**... |
| `.map(authority -> authority.substring("ROLE_".length()))` | ...and cut off the `ROLE_` in front: `ROLE_TEACHER` → `TEACHER`. (`"ROLE_".length()` is 5, so `substring(5)` = "everything from letter 5 on", Chapter 9.) |
| `JwtClaimsSet.builder()` | A **builder** 🧱 for the claims (the payload). |
| `.issuer("school")` | → `"iss":"school"` |
| `.issuedAt(now)` | → `"iat":...` |
| `.expiresAt(now.plus(lifetime))` | → `"exp":...` — now **plus** 1 hour. ⏰ |
| `.subject(authentication.getName())` | → `"sub":"teacher"` |
| `.claim("roles", roles)` | → `"roles":["TEACHER"]` — our **own** claim. |
| `JwsHeader.with(MacAlgorithm.HS256).build()` | The header: "signed with **HS256**". |
| `jwtEncoder.encode(...).getTokenValue()` | 🏭 Make the token: header + payload + **signature** → the long text with two dots. |
| `new TokenResponse(token, "Bearer", lifetime.toSeconds())` | The answer: the token, its type, and its lifetime in seconds (3600). |

---

## 🚪 Part 5: The login endpoint

Now `POST /api/auth/login`: check the name and password **once** → give out a token.

**`dto/LoginRequest.java`**

```java
package com.example.school.dto;

import jakarta.validation.constraints.NotBlank;

public record LoginRequest(
        @NotBlank(message = "Username is required")
        String username,

        @NotBlank(message = "Password is required")
        String password) {
}
```

To **check** a name and password ourselves, we need Spring's **`AuthenticationManager`** — the "boss" who uses our `UserDetailsService` and `PasswordEncoder` (the login steps from Chapter 81). Add this bean to **`SecurityConfig`**:

```java
@Bean
public AuthenticationManager authenticationManager(UserDetailsService userDetailsService,
                                                   PasswordEncoder passwordEncoder) {
    DaoAuthenticationProvider provider = new DaoAuthenticationProvider(userDetailsService);
    provider.setPasswordEncoder(passwordEncoder);
    return new ProviderManager(provider);
}
```

(Imports: `org.springframework.security.authentication.AuthenticationManager`, `org.springframework.security.authentication.ProviderManager`, `org.springframework.security.authentication.dao.DaoAuthenticationProvider`, `org.springframework.security.core.userdetails.UserDetailsService`.)

| Code | Meaning |
|---|---|
| `UserDetailsService userDetailsService` | Spring gives us **our** `SchoolUserDetailsService` (it's the only one). |
| `new DaoAuthenticationProvider(userDetailsService)` | A helper that checks name + password: find the user (with our service), then `matches` the password. ("DAO" = "data access object": it gets users from **data**.) |
| `provider.setPasswordEncoder(passwordEncoder)` | Use **our** BCrypt encoder for checking. |
| `new ProviderManager(provider)` | The `AuthenticationManager` that uses this helper. |

Now **`AuthController`** gets two new helpers and the `login` method:

```java
private final UserService userService;
private final AuthenticationManager authenticationManager;
private final TokenService tokenService;

public AuthController(UserService userService, AuthenticationManager authenticationManager,
                      TokenService tokenService) {
    this.userService = userService;
    this.authenticationManager = authenticationManager;
    this.tokenService = tokenService;
}

@PostMapping("/login")
public TokenResponse login(@Valid @RequestBody LoginRequest request) {
    Authentication authentication = authenticationManager.authenticate(
            UsernamePasswordAuthenticationToken.unauthenticated(request.username(), request.password()));
    return tokenService.createToken(authentication);
}
```

(Imports: `org.springframework.security.authentication.AuthenticationManager`, `org.springframework.security.authentication.UsernamePasswordAuthenticationToken`, `com.example.school.dto.LoginRequest`, `com.example.school.dto.TokenResponse`, `com.example.school.security.TokenService`.)

| Code | Meaning |
|---|---|
| `UsernamePasswordAuthenticationToken.unauthenticated(name, password)` | A "login **request**" object: "This person **says** they're `teacher` with password `secret123`. Not checked yet!" (Don't mix it up with our JWT — Spring just calls many things "token".) |
| `authenticationManager.authenticate(...)` | ⭐ **Check** it! Correct → we get back a full `Authentication` with the user's authorities. Wrong → it **throws** an exception. |
| `tokenService.createToken(authentication)` | Make the JWT for this user. 🏭🎟️ |

---

## 🛡️ Part 6: Checking tokens — the resource server

Last step: Spring must **read** the token from every request. Change **`SecurityConfig`** like this:

```java
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(HttpMethod.POST, "/api/auth/register", "/api/auth/login").permitAll()
                .requestMatchers("/api/auth/**").authenticated()
                // ... the other rules stay the same ...
                .anyRequest().authenticated())
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthenticationConverter())))
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .headers(headers -> headers.frameOptions(frame -> frame.sameOrigin()));
```

And add this **private** helper method to `SecurityConfig`:

```java
private JwtAuthenticationConverter jwtAuthenticationConverter() {
    JwtGrantedAuthoritiesConverter rolesConverter = new JwtGrantedAuthoritiesConverter();
    rolesConverter.setAuthoritiesClaimName("roles");
    rolesConverter.setAuthorityPrefix("ROLE_");

    JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
    converter.setJwtGrantedAuthoritiesConverter(rolesConverter);
    return converter;
}
```

(Imports: `org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter` and `org.springframework.security.oauth2.server.resource.authentication.JwtGrantedAuthoritiesConverter`. You can **remove** the `Customizer` import.)

| Code | Meaning |
|---|---|
| `.requestMatchers(HttpMethod.POST, "/api/auth/register", "/api/auth/login")` | You can give **several** paths at once. Strangers must be able to **log in** — of course! 🚪 |
| ~~`.httpBasic(Customizer.withDefaults())`~~ | **Gone!** No more passwords in every request. From now on: **tokens only**. |
| `.oauth2ResourceServer(oauth2 -> oauth2.jwt(...))` | ⭐ "Our app is a **resource server**: look for `Authorization: Bearer <token>`, and check the JWT with our `JwtDecoder` bean." |
| `jwt.jwtAuthenticationConverter(...)` | "...and here's how to turn a checked JWT into the user's authorities." |
| `rolesConverter.setAuthoritiesClaimName("roles")` | "Find the roles in **our** claim called `roles`." (Normally, Spring looks in a claim called `scope` — our tokens don't have one.) |
| `rolesConverter.setAuthorityPrefix("ROLE_")` | "Put `ROLE_` in front": `TEACHER` → `ROLE_TEACHER`. Now `hasRole("TEACHER")` works again! 🧩 |

How it fits together, for every request:

```
 GET /api/auth/me   Authorization: Bearer eyJraWQi...
     │
     ▼
 💂 BearerTokenAuthenticationFilter: "There's a Bearer token!"
     │
     ▼
 🔍 JwtDecoder: signature OK? ✍️  not expired? ⏰
     │   ❌ no → 401
     ▼   ✅ yes
 🔄 JwtAuthenticationConverter: "roles":["TEACHER"] → ROLE_TEACHER
     │
     ▼
 🚪 AuthorizationFilter: our rules (hasRole, hasAnyRole...) → 200 / 403
```

⭐ Look: **no** database, **no** BCrypt! Everything Spring needs is **inside** the token. That's why tokens are so fast. 🚀

---

## 🧪 Part 7: Test it!

Restart. Here are our **real** results.

### 1. Log in 🚪

```bash
curl -i -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"teacher","password":"secret123"}'
```

```
HTTP/1.1 200 
Content-Type: application/json

{"token":"eyJraWQiOiJzSloxTlVnVzBETGlnMkJ1VXhFQTQxNGtXNXNDYXhOOFI2Y3lhcWlZaEswIiwiYWxnIjoiSFMyNTYifQ.eyJpc3MiOiJzY2hvb2wiLCJzdWIiOiJ0ZWFjaGVyIiwiZXhwIjoxNzkxNzA1NTYyLCJpYXQiOjE3OTE3MDE5NjIsInJvbGVzIjpbIlRFQUNIRVIiXX0.gd7kkCWQh8YRSluOqwI_ctC61T83Pa0OrczveMPOvo0","tokenType":"Bearer","expiresIn":3600}
```

🎟️ Our wristband! Copy the token (without the quotes). To make the next commands shorter, save it in a **shell variable** (in Git Bash):

```bash
TOKEN=eyJraWQiOiJzSloxTlVnVzBETGlnMkJ1VXhFQTQxNGtXNXNDYXhOOFI2Y3lhcWlZaEswIiwiYWxnIjoiSFMyNTYifQ.eyJpc3Mi...
```

(Paste **your** whole token. Now `$TOKEN` means "the token". In Postman: **Authorization** tab → Type **Bearer Token** → paste it.)

### 2. Use the token 🎟️

```bash
curl -i -H "Authorization: Bearer $TOKEN" http://localhost:8080/api/auth/me
```

```
HTTP/1.1 200 
Content-Type: application/json

{"username":"teacher","authorities":["FACTOR_BEARER","ROLE_TEACHER"]}
```

🎉 It works! And our `me` method didn't change **at all** — `authentication.getName()` now reads the `sub` claim of the token. (That's why we used `Authentication` in Chapter 81, and not something password-specific.)

| Authority | Meaning |
|---|---|
| `ROLE_TEACHER` | From our `roles` claim, thanks to the converter. |
| `FACTOR_BEARER` | Spring Security 7's stamp: "This person proved who they are with a **bearer token**." (Before, it was `FACTOR_PASSWORD`.) |

Adding a student with the token:

```bash
curl -i -H "Authorization: Bearer $TOKEN" -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Noah King","email":"noah@school.com","age":12}'
```

```
HTTP/1.1 201 
Location: /api/students/7
Content-Type: application/json

{"id":7,"name":"Noah King","email":"noah@school.com","age":12,"classroom":null}
```

✅ The roles work exactly like in Chapter 82.

### 3. Without a token, or with the wrong role

**No token** for `POST /api/students`:

```
HTTP/1.1 401 
WWW-Authenticate: Bearer resource_metadata="http://localhost:8080/.well-known/oauth-protected-resource"
Content-Length: 0
```

The header now says **`Bearer`** — "please bring a token". (The `resource_metadata` part is a hint for big token systems. We can ignore it.)

**The teacher tries to delete** (`DELETE /api/students/1`):

```
HTTP/1.1 403 
WWW-Authenticate: Bearer error="insufficient_scope", error_description="The request requires higher privileges than provided by the access token.", error_uri="https://tools.ietf.org/html/rfc6750#section-3.1"
Content-Length: 0
```

"**Insufficient** scope" = "your token doesn't give you **enough** power". 🚫 Still a 403, like before — just explained in the header now.

**Basic doesn't work anymore:** `curl -u teacher:secret123 .../api/auth/me` → **401**. Tokens only! 🎟️

### 4. A wrong password at login 🪤

```bash
curl -i -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"teacher","password":"nope"}'
```

```
HTTP/1.1 500 
Content-Type: application/problem+json

{"detail":"Something went wrong on our side. Please try again later.","instance":"/api/auth/login","status":500,"title":"Server error"}
```

😵 **500?!** The log tells us why:

```
ERROR ... c.e.s.exception.GlobalExceptionHandler   : Unexpected error
org.springframework.security.authentication.BadCredentialsException: Bad credentials
```

It's the **same trap** as in Chapter 82! `authenticate(...)` throws a **`BadCredentialsException`** inside **our controller** → our catch-all turns it into a 500. A wrong password is **not** a server error — it's the client's mistake → it should be **401**.

**The fix** — one more handler in **`GlobalExceptionHandler`**:

```java
@ExceptionHandler(AuthenticationException.class)
public ProblemDetail handleLoginFailed(AuthenticationException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.UNAUTHORIZED,
            "Wrong username or password");
    problem.setTitle("Login failed");
    return problem;
}
```

(Import `org.springframework.security.core.AuthenticationException`.)

| Code | Meaning |
|---|---|
| `AuthenticationException` | The **parent** of all login exceptions: `BadCredentialsException` (wrong password), `UsernameNotFoundException`, `DisabledException`... One handler catches them all. |
| `"Wrong username or password"` | ⭐ The **same** message for "wrong password" **and** "no such user" — don't tell strangers which names exist (Chapter 81)! |

Our real answers now:

```
HTTP/1.1 401 
Content-Type: application/problem+json

{"detail":"Wrong username or password","instance":"/api/auth/login","status":401,"title":"Login failed"}
```

...and **exactly** the same for `{"username":"nobody","password":"nope"}`. ✅ And with empty fields → **400** `"The request has 2 invalid field(s)"` from our validation. ✅

---

## 🦹 Part 8: Can a hacker cheat? Let's try!

### 🖊️ Changing the token

Our token says `"roles":["TEACHER"]`. A sneaky teacher thinks: "I'll just change it to `ADMIN`!" 😈 They decode the payload, change the word, encode it again in Base64, and put it back between the two dots — keeping the old signature:

```
{"iss":"school","sub":"teacher","exp":1791705611,"iat":1791702011,"roles":["ADMIN"]}
```

Then they call `GET /api/admin/users` with the changed token. Our real answer:

```
HTTP/1.1 401 
WWW-Authenticate: Bearer error="invalid_token", error_description="An error occurred while attempting to decode the Jwt: Signed JWT rejected: Invalid signature", error_uri="https://tools.ietf.org/html/rfc6750#section-3.1", resource_metadata="http://localhost:8080/.well-known/oauth-protected-resource"
Content-Length: 0
```

🎉 **"Invalid signature"!** The server calculated the seal for the **new** payload with its secret key — and it didn't fit the old one. ✍️❌ Without the secret key, the sneaky teacher can't make a fitting signature.

### 🗑️ A broken token

`Authorization: Bearer hello` → **401** with `error_description="An error occurred while attempting to decode the Jwt: Malformed token"`. ("Malformed" = "badly made".)

⚠️ Watch out: this happens even for **public** URLs! `GET /api/students/1` with a broken token → **401** too. When a request **brings** a token, Spring **must** check it — and a bad token is never ignored. (No token at all → the public URL works as usual.)

### ⏰ An expired token

To test this without waiting an hour, we set `school.jwt.lifetime=10s` for a moment. We logged in at 12:31:20 (the token was made to expire at 12:31:30), and then:

| Time | Result |
|---|---|
| 12:31:20 (just made) | **200** ✅ |
| 12:31:50 (20 seconds **after** it expired) | **200** 🤔 still OK?! |
| 12:32:36 (over a minute after) | **401** ⏰ |

The last answer:

```
HTTP/1.1 401 
WWW-Authenticate: Bearer error="invalid_token", error_description="An error occurred while attempting to decode the Jwt: Jwt expired at 2026-10-11T07:01:30Z", error_uri="https://tools.ietf.org/html/rfc6750#section-3.1", resource_metadata="http://localhost:8080/.well-known/oauth-protected-resource"
```

🤔 Why did it still work 20 seconds **after** `exp`? Spring gives **60 seconds** of extra time ("clock skew"), because the clocks of different computers are never **exactly** the same. ⏱️ (The time in the message is in **UTC**, world time — that's what the `Z` means. Our computer's clock was 5½ hours ahead of it.)

Put `school.jwt.lifetime=1h` back afterwards!

---

## 🤔 Part 9: The price of tokens

Tokens are great — but they have **one** big weakness. Let's test it:

1. The teacher logs in → gets a token with `"roles":["TEACHER"]`.
2. The **admin** changes the teacher's role to `USER` (`PUT /api/admin/users/1/role` — use the teacher's id from Chapter 82).
3. The teacher uses the **old** token to add a student...

Our real result: **201 Created**! 😱 The teacher is a `USER` now — but the old token still **says** `TEACHER`, and Spring **trusts** the token (it doesn't look in the database, remember?).

4. The teacher logs in **again** → the **new** token says `"roles":["USER"]` → adding a student → **403**. ✅

(Afterwards, let the admin make the teacher a `TEACHER` again — we'll need them!)

Remember Chapter 82? With **Basic**, a role change worked **right away**, because every request read the database. With **tokens**:

> 🎟️ **A token is like a wristband: once it's given out, you can't take it back — until it expires.**

The same goes for changing your **password**: old tokens keep working until they expire! That's why:

- ⏰ Tokens should live **short**: minutes or hours, not months. (We use 1 hour.)
- 🔑 If the **secret key** ever leaks, change it → **all** tokens become invalid at once (see "Try it yourself").
- 🏢 Big apps add more tricks: very short tokens plus a second "refresh token" to get new ones, or a "block list" of tokens. That's for later in your programming life! 🚀

| | HTTP Basic 🔑 | JWT 🎟️ |
|---|---|---|
| Password sent | every request | **once** |
| Server checks | the database + BCrypt, every time 🐢 | only the signature 🚀 |
| Role/password changes | work **at once** | only after the token **expires** |
| Expires | never | yes ⏰ |
| Good for | quick tests, small tools | real apps, phone apps, websites |

---

## 💻 Mini project: What's in my token? 🔎

Build **`GET /api/auth/token-info`**: it answers with the information **inside** the caller's token:

```json
{"username":"teacher","roles":["TEACHER"],"issuedAt":"...","expiresAt":"..."}
```

**Hints:**

- In a controller method, you can get the token itself with **`@AuthenticationPrincipal Jwt jwt`**.
- A `Jwt` object has `getSubject()`, `getIssuedAt()`, `getExpiresAt()` and `getClaimAsStringList("roles")`.
- Make a record `TokenInfoResponse`. What type do the two times have?
- Do you need a new rule in `SecurityConfig`?

<details>
<summary>Click to see the answer</summary>

**`dto/TokenInfoResponse.java`**

```java
package com.example.school.dto;

import java.time.Instant;
import java.util.List;

public record TokenInfoResponse(String username, List<String> roles, Instant issuedAt, Instant expiresAt) {
}
```

**In `AuthController`:**

```java
@GetMapping("/token-info")
public TokenInfoResponse tokenInfo(@AuthenticationPrincipal Jwt jwt) {
    return new TokenInfoResponse(jwt.getSubject(), jwt.getClaimAsStringList("roles"),
            jwt.getIssuedAt(), jwt.getExpiresAt());
}
```

(Imports: `org.springframework.security.core.annotation.AuthenticationPrincipal`, `org.springframework.security.oauth2.jwt.Jwt`, `com.example.school.dto.TokenInfoResponse`.)

| Code | Meaning |
|---|---|
| `@AuthenticationPrincipal Jwt jwt` | "Give me the **principal** — the main object about the logged-in user." With a resource server, that's the checked **`Jwt`** itself! |
| `jwt.getSubject()` | The `sub` claim: `"teacher"`. |
| `jwt.getClaimAsStringList("roles")` | Our own `roles` claim, as a `List<String>`. |
| `jwt.getIssuedAt()`, `jwt.getExpiresAt()` | The `iat` and `exp` claims, as `Instant`s. |

**No new rule:** `/api/auth/**` → `authenticated()` already covers it. ✅

Our real answer:

```
HTTP/1.1 200 
Content-Type: application/json

{"username":"teacher","roles":["TEACHER"],"issuedAt":"2026-10-11T07:08:09Z","expiresAt":"2026-10-11T08:08:09Z"}
```

Jackson writes `Instant`s as readable **UTC** times — much nicer than `1791705562`! 🕐

</details>

---

## ✋ Try it yourself

1. Log in, then **restart** the app. Does your token still work? Why?
2. Change `school.jwt.secret` to another long text and restart. Does your old token still work?
3. Send the token **without** the word `Bearer`: `-H "Authorization: $TOKEN"`. What happens?
4. Register `sara`, log in as `sara`, and try to add a student with her token.
5. Sara changes her password with `PUT /api/auth/password` (using her token). Does her token still work afterwards?

<details>
<summary>Click to see the answers</summary>

1. **Yes** — our real test: after the restart, the old token → **200**. The server doesn't **remember** tokens at all (stateless!). It only checks the signature with the secret key — and the key is the same. (We even tried it with a **brand-new** database: still 200, because the token alone is enough.)
2. **No** — our real answer was **401** with `error_description="An error occurred while attempting to decode the Jwt: Signed JWT rejected: Invalid signature"`. The new key makes different seals, so **every** old token is dead at once. That's the emergency button 🚨 if your secret key ever leaks. (Put the old secret back afterwards — or just log in again.)
3. **401**, with only `WWW-Authenticate: Bearer resource_metadata=...` — exactly like **no** token at all. Spring only looks at `Authorization` headers that start with **`Bearer `** (with a space!).
4. Sara can log in and gets a token with `"roles":["USER"]` — but adding a student → **403**. Tokens don't change the **rules**; they only carry the roles. 👍
5. **Yes!** Our real test: password change → **204**, and then the **old** token → still **200**. 😮 The token doesn't know anything about the password — it's valid until `exp`. (Part 9: tokens can't be taken back.)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: A secret key that's too short

```properties
school.jwt.secret=too-short   # ❌ only 9 letters
```

The app **doesn't start**. Our real error:

```
Caused by: org.springframework.beans.BeanInstantiationException: Failed to instantiate [org.springframework.security.oauth2.jwt.JwtEncoder]: Factory method 'jwtEncoder' threw exception with message: com.nimbusds.jose.KeyLengthException: The secret length must be at least 256 bits
```

**Fix:** At least **32** letters (32 × 8 bits = 256 bits). Even better: a long **random** text from `JWT_SECRET`.

### Mistake 2: Forgetting the roles converter

With `.jwt(Customizer.withDefaults())` instead of our converter, Spring looks for roles in a claim called `scope` — and ignores our `roles` claim. Our real `GET /api/auth/me` as teacher:

```
{"username":"teacher","authorities":["FACTOR_BEARER"]}
```

No `ROLE_TEACHER`! 😱 So adding a student → **403** `insufficient_scope`. **Fix:** Use the `JwtAuthenticationConverter` with `setAuthoritiesClaimName("roles")` and `setAuthorityPrefix("ROLE_")` (Part 6).

### Mistake 3: Forgetting to open `/api/auth/login`

Without `"/api/auth/login"` in the `permitAll()` rule, you need a token... to **get** a token! 🐔🥚 Our real answer to the login:

```
HTTP/1.1 401
WWW-Authenticate: Bearer resource_metadata="http://localhost:8080/.well-known/oauth-protected-resource"
```

**Fix:** `.requestMatchers(HttpMethod.POST, "/api/auth/register", "/api/auth/login").permitAll()`.

### Mistake 4: A wrong password gives 500

The `BadCredentialsException` from `authenticate(...)` lands in the catch-all handler. **Fix:** an `@ExceptionHandler(AuthenticationException.class)` → **401** (Part 7, test 4).

### Mistake 5: Forgetting `Bearer`

`Authorization: eyJraWQi...` → **401**, as if there were no token. **Fix:** `Authorization: Bearer eyJraWQi...` — the word `Bearer` and **one** space.

### Mistake 6: Secrets inside the token

```java
.claim("password", user.getPassword())   // ❌ anyone can read the payload!
```

**Fix:** Only put what the server **needs** and what may be **seen**: the username, the roles, the times.

### Mistake 7: The secret key in Git

If `school.jwt.secret=my-real-production-secret` is in `application.properties`, everyone who can see your code can make **admin tokens**. 👑😈 **Fix:** The real key only in the environment variable `JWT_SECRET` (Chapter 77). The default in the file is **only** for learning.

### Mistake 8: Tokens that live for months

`school.jwt.lifetime=365d` → a stolen token works for a **year**, and role changes take a year to work. **Fix:** Keep lifetimes **short** (minutes to hours).

---

## ✅ Summary

- A **token** 🎟️ proves "I already logged in". The password travels **once** (`POST /api/auth/login`), then every request sends **`Authorization: Bearer <token>`**.
- A **JWT** has three parts: **header**.**payload**.**signature**. Header and payload are **readable** Base64 JSON — never put secrets in them!
- **Claims**: `iss` (who made it), `sub` (who it's about), `iat` (made at), `exp` (expires at), and our own `roles`.
- The **signature** ✍️ is made with the **secret key** (HS256). Change one letter → **"Invalid signature"**. The secret key must be **long** (32+ letters) and come from **outside** (`JWT_SECRET`).
- `JwtEncoder` 🏭 makes tokens, `JwtDecoder` 🔍 checks them. **`oauth2ResourceServer(...jwt(...))`** makes Spring check every Bearer token. A **converter** turns our `roles` claim into `ROLE_...` authorities.
- `AuthenticationManager.authenticate(...)` checks a name and password in our own login endpoint. Handle **`AuthenticationException`** → **401**.
- Checking a token needs **no** database → fast 🚀. But a token **can't be taken back** until it expires ⏰ → keep lifetimes **short**.

---

## ❓ Quiz

1. Why are tokens better than sending the password with every request? Give two reasons.
2. What are the three parts of a JWT, and what's in each?
3. Can anybody read the payload of a JWT? What does that mean for what you put inside?
4. A hacker changes `"roles":["USER"]` to `"roles":["ADMIN"]` in a token. What happens, and why?
5. What does `exp` mean? What happens after it?
6. Why must the secret key never be in Git?
7. What does the `JwtAuthenticationConverter` in our `SecurityConfig` do?
8. The admin takes away a teacher's `TEACHER` role. Can the teacher still add students? For how long?

<details>
<summary>Click to see the answers</summary>

1. The password travels only once (fewer chances to leak), the client doesn't need to keep the password, checking a token is fast (no database, no BCrypt), and tokens expire.
2. **Header** (how it's signed: `alg`, `kid`), **payload** (the claims: `iss`, `sub`, `iat`, `exp`, `roles`), **signature** (the seal made with the secret key).
3. Yes — it's only Base64. So never put secrets like passwords in a token.
4. The server rejects it with **401** "Invalid signature", because the signature doesn't fit the changed payload, and the hacker can't make a new one without the secret key.
5. **Exp**ires: the moment the token stops working. After it (plus 60 seconds of extra time), the server answers 401 "Jwt expired".
6. Anyone who knows the secret key can make valid tokens for any user — even an admin.
7. It reads the roles from our `roles` claim and puts `ROLE_` in front, so `hasRole(...)` rules work with tokens.
8. Yes — with their **old** token, until it expires (up to 1 hour in our app). A new login gives a token with the new role.

</details>

---

## 🎉 Part 10 complete!

Your app is **safe** now! 🔐🎉 Look at everything you learned:

- ✅ **Authentication** (who are you? → 401) and **authorization** (what may you do? → 403)
- ✅ Spring Security's **filter chain** 💂💂💂, and your own **`SecurityFilterChain`** rules
- ✅ **HTTP Basic**, **CSRF**, **stateless** APIs
- ✅ **Users in the database**, with **BCrypt** password hashes 🧂🐢
- ✅ **Register**, **"who am I?"**, and **changing passwords**
- ✅ **Roles**: `USER`, `TEACHER`, `ADMIN`, with `hasRole`, `hasAnyRole` and **`@PreAuthorize`** 🎭
- ✅ **JWT tokens** 🎟️: login, signatures, expiry — and their limits

### 🏁 Where are we?

```
 Part 1 ✅ Getting ready          Part 7  ✅ Spring Boot basics
 Part 2 ✅ Java basics            Part 8  ✅ Building REST APIs
 Part 3 ✅ Objects (OOP)          Part 9  ✅ Databases
 Part 4 ✅ More Java              Part 10 ✅ Security          ← you are here! 🎉
 Part 5 ✅ Tools                  Part 11 ⏳ Testing           ← next!
 Part 6 ✅ How the web works
```

Our app has grown **big**: students, classrooms, courses, books, users, roles, tokens... 🏗️ Every time we changed something, we tested it **by hand** with curl — again and again. 😓 What if a change in Part 12 secretly breaks something from Part 8? Would we notice?

In **Part 11**, you'll teach the computer to **test your app for you** — hundreds of checks in a few seconds, every time you change something. 🤖✅ Let's go!

---

[⬅ Previous chapter](82-roles.md) | [Table of Contents](../README.md) | [Next chapter: Why we test, and JUnit ➡](../part-11-testing/84-junit.md)
