# Chapter 91 – Doing jobs on a timer (Scheduling)

[⬅ Previous chapter](90-calling-apis.md) | [Table of Contents](../README.md) | [Next chapter ➡](92-file-upload.md)

---

## 🎯 Goal

Until now, our app only did something when a **request** came in. 📨 But some jobs must happen **by themselves**, at a certain **time**:

- ⏰ Every morning at 7: send the daily report.
- 🧹 Every night: clean up old data.
- 🔁 Every minute: check if another service is still alive.

Today your app gets an **alarm clock**. ⏰

At the end of this chapter you will know:

- How to switch on scheduling with **`@EnableScheduling`**
- How to run a method **every few seconds**: **`fixedRate`** and **`fixedDelay`**
- How to run a method at an **exact time**: **cron expressions** 🕖
- How to put the timing into **settings**
- What to watch out for: errors, long jobs, and many servers 🤔

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Scheduling** | Planning jobs to run **at certain times**, automatically. 📅 |
| **Scheduled task** / **job** | A method that runs on a timer. |
| **`@Scheduled`** | The label that says "run this method on a timer". ⏰ |
| **Fixed rate** | "Start the job every X seconds" — like a clock ticking. |
| **Fixed delay** | "After the job **finishes**, wait X seconds, then start again." |
| **Cron expression** | A short code that describes **when** to run: "every weekday at 7:00". 🕖 |
| **Time zone** | Which country's clock to use (7:00 in London is not 7:00 in Tokyo!). 🌍 |

---

## 📖 Story: The school bell 🔔

Nobody at school presses a button to ring the bell. 🔔 It's on a **timer**:

```
 07:55  🔔 "School starts in 5 minutes!"
 08:00  🔔 First lesson
 10:00  🔔 Break
 ...    (every school day, Monday to Friday — not on weekends!)
```

The caretaker set it up **once**, and now it rings **by itself**, every day, at the right times. 🎉

That's **scheduling**: you tell Spring **once** "run this method at these times", and Spring rings the bell for you. 🔔

---

## ⏰ Part 1: Switch on the alarm clock

Scheduling is **off** by default. Switch it on with **one** annotation. Create:

**`config/SchedulingConfig.java`**

```java
package com.example.school.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;

@Configuration
@EnableScheduling
public class SchedulingConfig {
}
```

| Code | Meaning |
|---|---|
| `@EnableScheduling` | "Spring, please look for `@Scheduled` methods and run them on their timers." |
| (empty class) | That's OK! The class only exists to carry the annotation. (You could also put it on `SchoolApplication`.) |

No new dependency needed — scheduling is part of Spring itself. 👍

---

## 🔁 Part 2: Every few seconds — `fixedRate`

Let's make a **heartbeat** 💓: a log line every 10 seconds that says "I'm alive".

**`job/HeartbeatJob.java`** (a new package `job`)

```java
package com.example.school.job;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class HeartbeatJob {

    private static final Logger log = LoggerFactory.getLogger(HeartbeatJob.class);

    private int beats = 0;

    @Scheduled(fixedRate = 10_000)
    public void beat() {
        beats++;
        log.info("💓 Heartbeat number {}", beats);
    }
}
```

| Code | Meaning |
|---|---|
| `@Component` | The job class must be a **bean** — otherwise Spring never sees it (Chapter 54). |
| `@Scheduled(fixedRate = 10_000)` | ⭐ "Run this method every **10,000 milliseconds** = 10 seconds." (The `_` just makes big numbers easier to read: `10_000` = `10000`.) |
| `public void beat()` | A scheduled method takes **no** parameters and returns **nothing**. Nobody is there to give it values or read its answer! |
| `private int beats` | The bean lives as long as the app, so the counter keeps counting. |

Start the app and watch the log:

```
... INFO ... [   scheduling-1] c.example.school.job.HeartbeatJob       : 💓 Heartbeat number 1
... INFO ... [   scheduling-1] c.example.school.job.HeartbeatJob       : 💓 Heartbeat number 2
... INFO ... [   scheduling-1] c.example.school.job.HeartbeatJob       : 💓 Heartbeat number 3
```

...every 10 seconds, for ever. 💓 Look at the thread name: **`scheduling-1`**. Scheduled jobs run on their **own** worker thread, not on a web request's thread.

You can also write the time in a friendlier way:

```java
@Scheduled(fixedRate = 10, timeUnit = TimeUnit.SECONDS)
```

(Import `java.util.concurrent.TimeUnit`.)

### 🤔 `fixedRate` or `fixedDelay`?

Imagine a job that takes **4 seconds**, with a timer of 10 seconds:

```
 fixedRate = 10s   (start every 10 seconds, like a clock)
 0s ████ 10s ████ 20s ████ 30s
    job       job       job

 fixedDelay = 10s  (wait 10 seconds AFTER the job ends)
 0s ████ ·········· 14s ████ ·········· 28s ████
    job   10s pause     job   10s pause
```

| | `fixedRate` | `fixedDelay` |
|---|---|---|
| Counts from | the **start** of the last run | the **end** of the last run |
| Good for | "every minute, on the minute" | jobs whose length changes, where you always want a **rest** between them |

There's also **`initialDelay`**: wait a bit after the app starts before the **first** run:

```java
@Scheduled(fixedDelay = 60, initialDelay = 30, timeUnit = TimeUnit.SECONDS)
```

---

## 🕖 Part 3: At an exact time — cron

"Every 10 seconds" is easy. But "every school day at 7:00 in the morning"? For that, we use a **cron expression**. 🕖 (The name comes from **Chronos**, the Greek word for time.)

A Spring cron expression has **six** parts:

```
 ┌───────────── second       (0-59)
 │ ┌─────────── minute       (0-59)
 │ │ ┌───────── hour         (0-23)
 │ │ │ ┌─────── day of month (1-31)
 │ │ │ │ ┌───── month        (1-12 or JAN-DEC)
 │ │ │ │ │ ┌─── day of week  (0-7 or MON-SUN)
 │ │ │ │ │ │
 0 0 7 * * MON-FRI
```

| Sign | Meaning |
|---|---|
| a number | exactly this: `7` in the hour place = "at 7 o'clock" |
| `*` | **every** (every day, every month...) |
| `MON-FRI` | from Monday **to** Friday |
| `*/15` | **every 15** (in the minute place: 0, 15, 30, 45) |
| `1,15` | 1 **and** 15 |

Some examples:

| Cron | Means |
|---|---|
| `0 0 7 * * MON-FRI` | Every school day at 07:00:00 🏫 |
| `0 */15 * * * *` | Every 15 minutes (at :00, :15, :30, :45) |
| `0 0 0 * * *` | Every night at midnight 🌙 |
| `0 30 16 * * FRI` | Every Friday at 16:30 🎉 |
| `0 0 9 1 * *` | On the 1st of every month at 09:00 📅 |
| `*/5 * * * * *` | Every 5 seconds (good for testing!) |

⚠️ Spring's cron has **six** parts (it starts with **seconds**). Cron on Linux servers has only **five**. If you copy one from the internet, check! 👀

---

## 📊 Part 4: A real job — the daily school report

Every school day at 7:00, the principal wants a report in the log: how many students, and their average age.

**`job/DailyReportJob.java`**

```java
package com.example.school.job;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import com.example.school.repository.StudentRepository;

@Component
public class DailyReportJob {

    private static final Logger log = LoggerFactory.getLogger(DailyReportJob.class);

    private final StudentRepository studentRepository;

    public DailyReportJob(StudentRepository studentRepository) {
        this.studentRepository = studentRepository;
    }

    @Scheduled(cron = "${school.report.cron}", zone = "${school.report.zone}")
    public void writeReport() {
        long count = studentRepository.count();
        Double averageAge = studentRepository.averageAge();
        log.info("📊 Daily report: {} students, average age {}", count, averageAge);
    }
}
```

And in **`application.properties`**:

```properties
# The daily report: every school day at 7:00
school.report.cron=0 0 7 * * MON-FRI
school.report.zone=Europe/London
```

| Code | Meaning |
|---|---|
| `StudentRepository studentRepository` | A job is a normal bean — it can get **any** other bean injected. |
| `cron = "${school.report.cron}"` | ⭐ The timing comes from **settings** (Chapter 55). Change the time **without** changing code! |
| `zone = "${school.report.zone}"` | ⭐ **Whose** 7 o'clock? Without a zone, it's the **server's** clock — and servers often run on UTC (world time). Use your school's zone, like `Europe/London`, `Asia/Kolkata` or `America/New_York`. 🌍 |

🧪 **Testing tip:** Nobody wants to wait until tomorrow at 7:00! While you build the job, use a fast timer in a **dev** profile (Chapter 56) — for example `school.report.cron=*/20 * * * * *` (every 20 seconds). Then you see:

```
... INFO ... [   scheduling-1] c.e.school.job.DailyReportJob           : 📊 Daily report: 3 students, average age 12.0
```

---

## 🤔 Part 5: Things to watch out for

### 💥 When a job throws an exception

If `writeReport` crashes (for example, the database is down), Spring **logs** the error — and runs the job again at the **next** time as normal. The timer doesn't stop. 👍 But nobody **sees** the error unless they read the log! So for important jobs, catch errors and log them clearly:

```java
@Scheduled(cron = "${school.report.cron}", zone = "${school.report.zone}")
public void writeReport() {
    try {
        long count = studentRepository.count();
        Double averageAge = studentRepository.averageAge();
        log.info("📊 Daily report: {} students, average age {}", count, averageAge);
    } catch (RuntimeException ex) {
        log.error("The daily report failed", ex);
    }
}
```

### 🐢 One worker for all jobs

By default, Spring has **one** scheduling thread (`scheduling-1`). If one job takes 5 minutes, all **other** jobs must **wait**! 😴 For many or long jobs, give Spring more workers:

```properties
spring.task.scheduling.pool.size=3
```

### 🖥️🖥️ Many servers

A big app often runs on **several** servers at once (Chapter 100). Then **each** server runs the job → the principal gets **three** reports! 😅 Big apps use special tools to make sure only **one** server runs it (for example, a library called **ShedLock**). For our school app with one server, it's fine.

---

## 💻 Mini project: Is the homework service alive? 🌍💓

Combine Chapter 90 and today: every **minute**, check if the homework API (JSONPlaceholder) answers.

- If yes → `INFO`: `"Homework service is up"`.
- If not (any exception) → `WARN`: `"Homework service is DOWN: <message>"`.
- The first check should wait **10 seconds** after the app starts.

**Hint:** Inject the `HomeworkService` and call `getHomework(1L)`.

<details>
<summary>Click to see the answer</summary>

**`job/HomeworkHealthJob.java`**

```java
package com.example.school.job;

import java.util.concurrent.TimeUnit;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import com.example.school.service.HomeworkService;

@Component
public class HomeworkHealthJob {

    private static final Logger log = LoggerFactory.getLogger(HomeworkHealthJob.class);

    private final HomeworkService homeworkService;

    public HomeworkHealthJob(HomeworkService homeworkService) {
        this.homeworkService = homeworkService;
    }

    @Scheduled(fixedRate = 60, initialDelay = 10, timeUnit = TimeUnit.SECONDS)
    public void check() {
        try {
            homeworkService.getHomework(1L);
            log.info("Homework service is up");
        } catch (RuntimeException ex) {
            log.warn("Homework service is DOWN: {}", ex.getMessage());
        }
    }
}
```

| Code | Meaning |
|---|---|
| `fixedRate = 60, initialDelay = 10, timeUnit = TimeUnit.SECONDS` | First check 10 seconds after the start, then every 60 seconds. |
| `catch (RuntimeException ex)` | `RestClient` problems (no answer, timeouts, 5xx) are `RuntimeException`s. |
| `log.warn("...{}", ex.getMessage())` | Here a short message is enough — "down" is expected sometimes, it's not a bug in **our** code. |

Try the typo from Chapter 90 (`...typicode.co`) → after a minute: `WARN ... Homework service is DOWN: I/O error on GET request for ...`. 📵

</details>

---

## ✋ Try it yourself

1. Write the cron expression for "every day at 12:30".
2. Write the cron expression for "every Monday at 8:00".
3. Make the heartbeat use `fixedDelay` with a `Thread.sleep(3000)` inside (a job that takes 3 seconds). How far apart are the log lines now?
4. Turn the heartbeat **off** in tests. (Hint: `@Scheduled(fixedRateString = "${school.heartbeat.rate}")` and a different value... or think about profiles!)

<details>
<summary>Click to see the answers</summary>

1. `0 30 12 * * *`
2. `0 0 8 * * MON`
3. About **13** seconds apart: 3 seconds of work + 10 seconds of pause. (With `fixedRate`, they'd be 10 seconds apart.)
4. One simple way: put `@Profile("!test")` on the `HeartbeatJob` class (Chapter 56) — "this bean exists in every profile **except** `test`". (The `!` means "not".)

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `@EnableScheduling`

Nothing happens. No error, no log — the `@Scheduled` annotations are simply ignored. 😶 **Fix:** `@EnableScheduling` on a configuration class.

### Mistake 2: The job class isn't a bean

`@Scheduled` on a class without `@Component` (or `@Service`) → ignored. **Fix:** Make it a bean.

### Mistake 3: Five-part cron

`0 7 * * MON-FRI` (copied from a Linux example) → Spring refuses to start with an error like *"Cron expression must consist of 6 fields (found 5 in ...)"*. **Fix:** Add the **seconds** at the front: `0 0 7 * * MON-FRI`.

### Mistake 4: Forgetting the time zone

The report comes at 7:00 **UTC** — maybe 2:00 at night for your school. 🌙 **Fix:** `zone = "..."`.

### Mistake 5: Parameters on a scheduled method

`public void writeReport(String day)` → Spring can't call it (who would give the `day`?) and refuses to start. **Fix:** Scheduled methods have **no** parameters.

---

## ✅ Summary

- **`@EnableScheduling`** switches the alarm clock on ⏰. Jobs are **beans** with **`@Scheduled`** methods (no parameters, return `void`).
- **`fixedRate`**: start every X. **`fixedDelay`**: X after the last run **ended**. **`initialDelay`**: wait before the first run. `timeUnit` makes it readable.
- **Cron** (6 parts: second minute hour day month weekday): `0 0 7 * * MON-FRI` 🕖. Always set a **`zone`**.
- Put timings in **settings**: `cron = "${school.report.cron}"`.
- Jobs run on the `scheduling-1` thread. Catch and log errors. More workers: `spring.task.scheduling.pool.size`. Many servers → every server runs the job!

---

## ❓ Quiz

1. What must you add before any `@Scheduled` method runs?
2. What's the difference between `fixedRate` and `fixedDelay`?
3. Read this cron: `0 0 18 * * SUN`.
4. Why do Spring cron expressions have six parts, and Linux ones five?
5. Why should you set a `zone`?
6. What happens to the timer when a scheduled job throws an exception?
7. Why can a scheduled method not have parameters?

<details>
<summary>Click to see the answers</summary>

1. `@EnableScheduling` on a configuration class (and the job class must be a bean).
2. `fixedRate` counts from the **start** of the last run; `fixedDelay` counts from the **end** of the last run.
3. Every Sunday at 18:00:00.
4. Spring's cron starts with an extra field for **seconds**.
5. Otherwise the server's clock is used — often UTC, which may be hours away from your school's time.
6. Spring logs the error and keeps going: the job runs again at its next time.
7. Nobody calls it by hand — Spring calls it on a timer and has no values to give it.

</details>

---

[⬅ Previous chapter](90-calling-apis.md) | [Table of Contents](../README.md) | [Next chapter: Uploading files ➡](92-file-upload.md)
