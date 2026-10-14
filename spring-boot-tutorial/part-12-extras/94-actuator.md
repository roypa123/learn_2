# Chapter 94 – Actuator: checking your app's health

[⬅ Previous chapter](93-swagger.md) | [Table of Contents](../README.md) | [Next chapter ➡](../part-13-final-project/95-library-planning.md)

---

## 🎯 Goal

Your app runs on a server, day and night. 🌙 How do you know it's **OK**? Is the database still connected? Is the disk full? How many requests came in today? 🤔

Spring Boot has a ready-made **doctor's kit** for your app: **Actuator**. 🩺

At the end of this chapter you will know:

- What **Actuator** is, and what **endpoints** it gives you
- How to check your app's **health**: `/actuator/health` 💚
- How to show **info** about your app: `/actuator/info` ℹ️
- How to look at **metrics** (numbers about your app): `/actuator/metrics` 📊
- Which endpoints to show — and how to **protect** them 🔒
- How to write your **own** health check 🩺

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Actuator** | A Spring Boot tool that adds **check-up** endpoints to your app. 🩺 (In machines, an actuator is a part that moves or controls something.) |
| **Health check** | A quick test: "Is the app OK?" → `UP` 💚 or `DOWN` 💔. |
| **Metric** | A **number** about your app: memory used, number of requests, time per request... 📊 |
| **Monitoring** | Watching those numbers all the time, often with graphs and alarms. 📈🚨 |
| **Expose** | Make an endpoint **reachable** over the web. |
| **Health indicator** | One small check inside the health check, for example "is the database OK?". |

---

## 📖 Story: The school nurse 🩺

Every school has a **nurse**. Once a year, she does a check-up with every student:

```
 🩺 Check-up: Tom Brown
    Heart:      ✅ OK
    Eyes:       ✅ OK
    Height:     152 cm  📏
    Weight:     41 kg   ⚖️
    → Overall:  HEALTHY 💚
```

She checks **parts** (heart, eyes), writes down **numbers** (height, weight), and gives an **overall** result. If **one** part is wrong, the overall result isn't "healthy" anymore.

Actuator is the school nurse for your app:

| Nurse 🩺 | Actuator |
|---|---|
| Heart OK? Eyes OK? | Database OK? Disk OK? — **health indicators** |
| Overall: HEALTHY | `/actuator/health` → `{"status":"UP"}` 💚 |
| Height, weight | `/actuator/metrics` — memory, requests... 📊 |
| Name, class, age | `/actuator/info` ℹ️ |

---

## 📦 Part 1: Add Actuator

Add to **`pom.xml`**:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

Restart. In the log, you'll see a new line like this:

```
... o.s.b.a.e.web.EndpointLinksResolver      : Exposing 1 endpoint beneath base path '/actuator'
```

**One** endpoint? Yes — by default, Actuator only shows **`health`** over the web. The others are hidden, because some of them show **secret** things about your app. 🔒 Safe by default — like Spring Security! 👍

### 🔓 The security rule

Our `SecurityConfig` locks everything that isn't listed. Add, near the other `permitAll` rules:

```java
                .requestMatchers("/actuator/health").permitAll()
                .requestMatchers("/actuator/**").hasRole("ADMIN")
```

| Code | Meaning |
|---|---|
| `/actuator/health` → `permitAll()` | Everyone may ask "are you OK?" — servers and monitoring tools need this **without** a login. |
| `/actuator/**` → `hasRole("ADMIN")` | ⭐ All **other** Actuator endpoints: admins only. (The specific rule is on top! Chapter 80. 📏) |

---

## 💚 Part 2: Health

```bash
curl -i http://localhost:8080/actuator/health
```

```
HTTP/1.1 200 
Content-Type: application/vnd.spring-boot.actuator.v3+json

{"status":"UP"}
```

💚 **UP** — the app is healthy! That's what big systems check every few seconds: if a server answers `DOWN` (or doesn't answer at all), they stop sending users to it and maybe restart it. 🔄

### 🔍 More details

`UP` alone doesn't say **why**. Let's see the parts. Add to **`application.properties`**:

```properties
# Actuator: show the details of the health check
management.endpoint.health.show-details=always
```

```bash
curl http://localhost:8080/actuator/health
```

Now you see something like this (the numbers depend on your computer):

```json
{
  "status": "UP",
  "components": {
    "db":        { "status": "UP", "details": { "database": "H2", "validationQuery": "isValid()" } },
    "diskSpace": { "status": "UP", "details": { "total": 511101063168, "free": 202517073920, "threshold": 10485760, "path": "...", "exists": true } },
    "ping":      { "status": "UP" }
  }
}
```

| Component | Checks |
|---|---|
| `db` 🗄️ | Can the app talk to the database? Spring Boot added this check **by itself**, because we use a database! |
| `diskSpace` 💾 | Is there enough free disk space? (`threshold`: below 10 MB free → `DOWN`.) |
| `ping` 🏓 | Always `UP` — "the app answers at all". |

⭐ The overall `status` is only `UP` if **all** components are `UP` — just like the nurse's "healthy". If the database stops, `db` → `DOWN`, and the whole answer becomes `{"status":"DOWN", ...}` with status code **503**. 💔

⚠️ `show-details=always` shows details to **everyone**. A safer choice for real apps:

```properties
management.endpoint.health.show-details=when-authorized
```

→ details only for **logged-in** users; strangers just see `{"status":"UP"}`.

---

## ℹ️ Part 3: Info

`/actuator/info` tells people **what** this app is. First, expose it (and two more endpoints for Part 4):

```properties
# Which Actuator endpoints are reachable over the web
management.endpoints.web.exposure.include=health,info,metrics

# Information shown at /actuator/info
management.info.env.enabled=true
info.app.name=School API
info.app.description=Students, classrooms, courses and books
info.app.version=1.0
```

| Code | Meaning |
|---|---|
| `management.endpoints.web.exposure.include=health,info,metrics` | ⭐ Make **these three** endpoints reachable. Never use `*` (all) on a real server! |
| `management.info.env.enabled=true` | "Show the `info.*` settings at `/actuator/info`." (Off by default.) |
| `info.app.name=...` | Anything that starts with `info.` appears in the answer. |

`/actuator/info` is under `/actuator/**` → admins only. Log in as admin (Chapter 83), then:

```bash
curl -H "Authorization: Bearer $ADMIN_TOKEN" http://localhost:8080/actuator/info
```

```json
{"app":{"name":"School API","description":"Students, classrooms, courses and books","version":"1.0"}}
```

---

## 📊 Part 4: Metrics

Actuator measures **hundreds** of things about your app — all the time, automatically. 📏⚖️

```bash
curl -H "Authorization: Bearer $ADMIN_TOKEN" http://localhost:8080/actuator/metrics
```

You get a long list of **names**:

```json
{"names":["application.ready.time","disk.free","hikaricp.connections.active","http.server.requests","jvm.memory.used","jvm.threads.live","process.uptime","system.cpu.usage", ...]}
```

Ask for **one** of them:

```bash
curl -H "Authorization: Bearer $ADMIN_TOKEN" http://localhost:8080/actuator/metrics/process.uptime
```

```json
{"name":"process.uptime","description":"The uptime of the Java virtual machine","baseUnit":"seconds","measurements":[{"statistic":"VALUE","value":1532.5}],"availableTags":[]}
```

The app has been running for about **1532 seconds** (25 minutes). ⏱️

Some useful metrics:

| Metric | Tells you |
|---|---|
| `http.server.requests` | How many requests came in, and how long they took. 📨 |
| `jvm.memory.used` | How much memory the app uses right now. 🧠 |
| `process.uptime` | How long the app has been running. ⏱️ |
| `hikaricp.connections.active` | How many database connections are busy. 🗄️ |
| `system.cpu.usage` | How busy the computer's processor is. 🔥 |

You can even ask about **one** URL with a **tag**:

```bash
curl -H "Authorization: Bearer $ADMIN_TOKEN" "http://localhost:8080/actuator/metrics/http.server.requests?tag=uri:/api/students/{id}"
```

→ how many times `GET /api/students/{id}` was called, the **total** time, and the **max** time. 📊

💡 In real life, nobody reads these with curl. A **monitoring** tool (like **Prometheus** + **Grafana**) collects them every few seconds and draws **graphs** 📈 — and rings an **alarm** 🚨 when something looks wrong.

---

## 🩺 Part 5: Your own health check

The `db` check was added automatically. But **our** app also needs the **homework API** (Chapter 90). Let's add a health check for it!

**`health/HomeworkHealthIndicator.java`** (a new package `health`)

```java
package com.example.school.health;

import org.springframework.boot.health.contributor.Health;
import org.springframework.boot.health.contributor.HealthIndicator;
import org.springframework.stereotype.Component;

import com.example.school.service.HomeworkService;

@Component
public class HomeworkHealthIndicator implements HealthIndicator {

    private final HomeworkService homeworkService;

    public HomeworkHealthIndicator(HomeworkService homeworkService) {
        this.homeworkService = homeworkService;
    }

    @Override
    public Health health() {
        try {
            homeworkService.getHomework(1L);
            return Health.up()
                    .withDetail("service", "jsonplaceholder")
                    .build();
        } catch (RuntimeException ex) {
            return Health.down()
                    .withDetail("service", "jsonplaceholder")
                    .withDetail("error", ex.getMessage())
                    .build();
        }
    }
}
```

| Code | Meaning |
|---|---|
| `implements HealthIndicator` | ⭐ "I am one health check." Actuator finds all beans like this. (In Spring Boot 4, health classes live in the package `org.springframework.boot.health.contributor`.) |
| `public Health health()` | Called every time someone asks `/actuator/health`. |
| `Health.up()` / `Health.down()` | The result: 💚 or 💔. |
| `.withDetail("error", ex.getMessage())` | Extra information shown in the details. |

The **name** of the check comes from the class name, without `HealthIndicator` → **`homework`**:

```json
{
  "status": "UP",
  "components": {
    "db":        { "status": "UP", ... },
    "diskSpace": { "status": "UP", ... },
    "homework":  { "status": "UP", "details": { "service": "jsonplaceholder" } },
    "ping":      { "status": "UP" }
  }
}
```

Now break the URL (the typo from Chapter 90) → `homework` becomes **DOWN**, and so does the **whole** app → **503**. 💔

🤔 **Hmm — is that right?** If the homework API is down, our school app still works fine for everything **else**! Marking the **whole** app `DOWN` could make a monitoring system **restart** it for nothing. Be careful which checks make your app "sick". (Big apps put such checks into a separate **group** that doesn't change the main status — a topic for later.)

---

## 💻 Mini project: A "students" health check 👩‍🎓

Write a `StudentsHealthIndicator`:

- `UP` with a detail `"count"` = the number of students.
- But if there are **0** students, the school is empty — return `Health.status("EMPTY")` with a detail `"message"`: `"There are no students"`. (A custom status! It's not `DOWN` — the app works, it's just strange.)

<details>
<summary>Click to see the answer</summary>

**`health/StudentsHealthIndicator.java`**

```java
package com.example.school.health;

import org.springframework.boot.health.contributor.Health;
import org.springframework.boot.health.contributor.HealthIndicator;
import org.springframework.stereotype.Component;

import com.example.school.repository.StudentRepository;

@Component
public class StudentsHealthIndicator implements HealthIndicator {

    private final StudentRepository studentRepository;

    public StudentsHealthIndicator(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    @Override
    public Health health() {
        long count = studentRepository.count();
        if (count == 0) {
            return Health.status("EMPTY")
                    .withDetail("message", "There are no students")
                    .build();
        }
        return Health.up()
                .withDetail("count", count)
                .build();
    }
}
```

| Code | Meaning |
|---|---|
| `Health.status("EMPTY")` | A status with **your own** name. |
| `.withDetail("count", count)` | Details can be numbers too. |

With our 3 students: `"students": {"status":"UP","details":{"count":3}}`. 👩‍🎓👨‍🎓👧

(Actuator doesn't know how "bad" `EMPTY` is, so it places unknown statuses **last** in its order — the overall status stays `UP`. You could change that with the setting `management.endpoint.health.status.order` if you wanted.)

</details>

---

## ✋ Try it yourself

1. Stop the H2 database... wait, it runs **inside** our app! Instead, change `spring.datasource.url` to a wrong value for a moment. Does the app even start?
2. Add `beans` to the exposed endpoints and open `/actuator/beans` as admin. How many beans can you find with `school` in the name?
3. Call `GET /api/students/1` five times, then look at `http.server.requests` with the tag `uri:/api/students/{id}`. What is `COUNT`?

<details>
<summary>Click to see the answers</summary>

1. With a wrong URL, Hibernate can't connect while starting → the app **doesn't start** at all. (Health checks help with problems that happen **while** the app is running — like a database server that goes down later.)
2. Every bean of the app, with its class and its dependencies. All our controllers, services, repositories, `SecurityConfig`, `TokenService`... — a few dozen with `school` in the name, and **hundreds** of Spring's own. It's like an X-ray 🩻 of Chapter 54! (Remove `beans` again afterwards — it shows a lot about your app.)
3. `COUNT` is **5** (or more, if you called it before). You also get `TOTAL_TIME` and `MAX`.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: `exposure.include=*` on a real server

That shows **everything**: all settings (`/actuator/env`), all beans, even a memory dump (`/actuator/heapdump`) that can contain **passwords**! 😱 **Fix:** Expose only what you need (`health,info,metrics`), and protect it with Spring Security.

### Mistake 2: Forgetting the security rules

Without them, `/actuator/health` answers **401** — and your monitoring thinks the app is broken. **Fix:** `permitAll()` for `/actuator/health`, `hasRole("ADMIN")` for the rest.

### Mistake 3: Expecting `/actuator/info` to show the `info.*` settings

They don't appear by default. **Fix:** `management.info.env.enabled=true`.

### Mistake 4: Slow health checks

Every `/actuator/health` call runs **all** checks. A check that waits 10 seconds for another API makes the health endpoint slow. **Fix:** Use short timeouts in such checks (Chapter 90).

### Mistake 5: Making the whole app `DOWN` for a small problem

**Fix:** Only things your app **really** can't live without (like its database) should make it `DOWN`.

---

## ✅ Summary

- **Actuator** 🩺 = check-up endpoints for your app. Add `spring-boot-starter-actuator`.
- **`/actuator/health`** → `{"status":"UP"}` 💚. Components like `db`, `diskSpace`, `ping` are added automatically. One part `DOWN` → all `DOWN` → **503**.
- Details: `management.endpoint.health.show-details=when-authorized` (or `always` for learning).
- Choose what's reachable: `management.endpoints.web.exposure.include=health,info,metrics`. **Never `*`** on a real server.
- **`/actuator/info`** with `info.*` settings (+ `management.info.env.enabled=true`). **`/actuator/metrics`** 📊 for numbers like `http.server.requests`.
- Protect it: health for everyone, everything else for admins.
- Your own check: a bean that **`implements HealthIndicator`** and returns `Health.up()` / `Health.down()`.

---

## ❓ Quiz

1. What does `/actuator/health` answer when everything is fine?
2. Why does Actuator only expose `health` by default?
3. The database stops working. What does `/actuator/health` answer?
4. What's the difference between `show-details=always` and `show-details=when-authorized`?
5. Name two metrics and what they measure.
6. How do you write your own health check?
7. Why should `/actuator/health` be reachable without a login?

<details>
<summary>Click to see the answers</summary>

1. `{"status":"UP"}` with status code 200.
2. Some endpoints show secret information about the app. Safe by default: you must choose what to show.
3. `{"status":"DOWN", ...}` with status code 503 (the `db` component is `DOWN`).
4. `always` shows the details to everyone; `when-authorized` shows them only to logged-in users.
5. For example: `http.server.requests` (number and time of requests), `jvm.memory.used` (memory), `process.uptime` (how long the app has run).
6. Make a bean that implements `HealthIndicator` and returns `Health.up()` or `Health.down()` (with details) from `health()`.
7. Servers and monitoring tools check it all the time, often without a user account.

</details>

---

## 🎉 Part 12 complete!

Your toolbox 🧰 is full! Look at everything you learned:

- ✅ **Logging** 📔: SLF4J, levels, files — and what never to log
- ✅ **Thymeleaf** 🌿: real HTML pages with `th:text`, `th:each`, `th:if`
- ✅ **Calling other APIs** 🌍: `RestClient`, errors, timeouts
- ✅ **Scheduling** ⏰: `fixedRate`, `fixedDelay`, cron
- ✅ **File uploads** 📸: `MultipartFile`, checks, safe saving, downloads
- ✅ **API docs** 📖: springdoc, Swagger UI, the Authorize button
- ✅ **Actuator** 🩺: health, info, metrics, your own health checks

### 🏁 Where are we?

```
 Part 1 ✅ Getting ready          Part 8  ✅ Building REST APIs
 Part 2 ✅ Java basics            Part 9  ✅ Databases
 Part 3 ✅ Objects (OOP)          Part 10 ✅ Security
 Part 4 ✅ More Java              Part 11 ✅ Testing
 Part 5 ✅ Tools                  Part 12 ✅ Useful extras     ← you are here! 🎉
 Part 6 ✅ How the web works      Part 13 ⏳ Final project     ← the last part!
 Part 7 ✅ Spring Boot basics
```

Now comes the **grand finale** 🎆: in **Part 13**, you'll build a **whole new app** from scratch — a **Library app** — using **everything** you've learned. Then you'll pack it into a `.jar`, put it into a **Docker** box, and put it **on the internet**. 🌍 Let's go!

---

[⬅ Previous chapter](93-swagger.md) | [Table of Contents](../README.md) | [Next chapter: Final project: Library app – planning ➡](../part-13-final-project/95-library-planning.md)
