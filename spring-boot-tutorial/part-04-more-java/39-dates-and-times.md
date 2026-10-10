# Chapter 39 – Dates and Times

[⬅ Previous chapter](38-annotations.md) | [Table of Contents](../README.md) | [Next chapter ➡](../part-05-tools/40-maven.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- The modern date and time classes in **`java.time`**
- **`LocalDate`** (a date), **`LocalTime`** (a time), **`LocalDateTime`** (both)
- How to create dates: `now()`, `of(...)`, `parse(...)`
- How to **add** and **subtract** days, months, years
- How to **compare** dates: `isBefore`, `isAfter`
- How to measure **differences**: `Period`, `Duration`, `ChronoUnit.DAYS.between`
- How to **format** dates nicely with `DateTimeFormatter`
- Time zones (`ZonedDateTime`, `Instant`) — just the basics
- A big **Part 4 review project** 🎓

> 🌱 **Spring Boot note:** Almost every app has dates: when a user signed up, when an order was placed, when a book must be returned. Spring Boot and databases work perfectly with `java.time` classes.

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **`LocalDate`** | A date **without** a time: 2025-03-15. Like a page in a calendar 📅. |
| **`LocalTime`** | A time **without** a date: 14:30. Like a clock 🕐. |
| **`LocalDateTime`** | A date **and** a time: 2025-03-15T14:30. |
| **"Local"** | **No time zone.** Just "the date/time on the wall calendar here". |
| **Time zone** | A region with the same clock time: Europe/Paris, Asia/Tokyo... 🌍 |
| **`Instant`** | One exact moment on the world's timeline (the same everywhere). |
| **`Period`** | An amount of time in **years, months, days** ("2 years and 3 months"). |
| **`Duration`** | An amount of time in **hours, minutes, seconds** ("1 hour 30 minutes"). |
| **ISO format** | The international way to write dates: `YYYY-MM-DD` → `2025-03-15`. |
| **Format** | Turn a date into **text** in a certain style: `15/03/2025` or `March 15, 2025`. |

---

## 📖 Story: The calendar and the clock 📅🕐

On your wall, there's a **calendar** 📅 and a **clock** 🕐.

- The **calendar** tells you the **date**: "Saturday, March 15, 2025". → `LocalDate`
- The **clock** tells you the **time**: "2:30 in the afternoon". → `LocalTime`
- Together: "March 15, 2025, at 2:30 PM". → `LocalDateTime`

But your friend in **Japan** looks at **their** clock at the **same moment** — and it says 10:30 at night! 🌙 That's because of **time zones**. When people in different countries need to agree on an **exact moment**, we use `Instant` or `ZonedDateTime`.

---

## ⚠️ Part 0: Old classes — don't use them

Java has **old** date classes: `java.util.Date`, `java.util.Calendar`, `SimpleDateFormat`. They are **confusing** and full of traps (for example, months start at **0** — January = 0! 😱).

Since **Java 8** (2014), we have the new, clean **`java.time`** package. **Always use `java.time`.** 👍

| ❌ Old (avoid) | ✅ New (use) |
|---|---|
| `java.util.Date` | `LocalDate`, `LocalDateTime`, `Instant` |
| `java.util.Calendar` | `LocalDate`, `ZonedDateTime` |
| `SimpleDateFormat` | `DateTimeFormatter` |

> 💡 All `java.time` classes are **immutable** (like `String` — Chapter 9). Methods like `plusDays` return a **new** object. You must **save** the result!

---

## 📅 Part 1: `LocalDate` — a date

```java
import java.time.LocalDate;
import java.time.Month;

public class Dates {
    public static void main(String[] args) {
        LocalDate today = LocalDate.now();
        LocalDate birthday = LocalDate.of(2012, 5, 20);
        LocalDate newYear = LocalDate.of(2026, Month.JANUARY, 1);
        LocalDate fromText = LocalDate.parse("2025-03-15");

        System.out.println(today);      // e.g. 2026-10-10 (the date when you run it)
        System.out.println(birthday);   // 2012-05-20
        System.out.println(newYear);    // 2026-01-01
        System.out.println(fromText);   // 2025-03-15
    }
}
```

### 🔍 Line by line

| Code | Meaning |
|---|---|
| `LocalDate.now()` | **Today's** date, from your computer's clock. |
| `LocalDate.of(2012, 5, 20)` | A specific date: year, **month (1–12)** ✅, day. May = 5. (Unlike the old classes, January = **1**!) |
| `LocalDate.of(2026, Month.JANUARY, 1)` | The same, with the **enum** `Month` (Chapter 28) — even clearer. |
| `LocalDate.parse("2025-03-15")` | Read a date from **text** in ISO format `YYYY-MM-DD`. |
| `println(date)` | Prints in ISO format: `2025-03-15`. |

> ⚠️ `LocalDate.of(2025, 2, 30)` → 💥 `DateTimeException: Invalid date 'FEBRUARY 30'`. Java checks that the date is real! 🛡️

### Reading the parts of a date

```java
LocalDate date = LocalDate.of(2025, 3, 15);

System.out.println(date.getYear());         // 2025
System.out.println(date.getMonth());        // MARCH  (a Month enum)
System.out.println(date.getMonthValue());   // 3
System.out.println(date.getDayOfMonth());   // 15
System.out.println(date.getDayOfWeek());    // SATURDAY  (a DayOfWeek enum)
System.out.println(date.getDayOfYear());    // 74
System.out.println(date.isLeapYear());      // false
System.out.println(date.lengthOfMonth());   // 31
```

`DayOfWeek` and `Month` are **enums** — so you can use them in a `switch` (Chapter 28)!

```java
String plan = switch (date.getDayOfWeek()) {
    case SATURDAY, SUNDAY -> "Weekend! 🎉";
    default -> "School day 🏫";
};
System.out.println(plan);   // Weekend! 🎉
```

---

## ➕ Part 2: Adding and subtracting

```java
LocalDate start = LocalDate.of(2025, 1, 31);

System.out.println(start.plusDays(1));     // 2025-02-01
System.out.println(start.plusWeeks(2));    // 2025-02-14
System.out.println(start.plusMonths(1));   // 2025-02-28  ← smart! February has no 31st
System.out.println(start.plusYears(1));    // 2026-01-31
System.out.println(start.minusDays(31));   // 2024-12-31
```

| Method | Meaning |
|---|---|
| `plusDays(n)`, `minusDays(n)` | add / subtract days |
| `plusWeeks(n)`, `minusWeeks(n)` | weeks |
| `plusMonths(n)`, `minusMonths(n)` | months (handles short months smartly 🧠) |
| `plusYears(n)`, `minusYears(n)` | years |

### ⚠️ Remember: immutable!

```java
LocalDate d = LocalDate.of(2025, 1, 1);
d.plusDays(10);                 // ❌ the result is thrown away!
System.out.println(d);          // 2025-01-01  (unchanged)

d = d.plusDays(10);             // ✅ save it
System.out.println(d);          // 2025-01-11
```

### Changing one part: `with...`

```java
LocalDate d = LocalDate.of(2025, 3, 15);
System.out.println(d.withDayOfMonth(1));   // 2025-03-01  (first day of the month)
System.out.println(d.withYear(2030));      // 2030-03-15
```

---

## ⚖️ Part 3: Comparing dates

```java
LocalDate today = LocalDate.of(2025, 3, 15);
LocalDate deadline = LocalDate.of(2025, 3, 20);

System.out.println(today.isBefore(deadline));   // true
System.out.println(today.isAfter(deadline));    // false
System.out.println(today.isEqual(deadline));    // false
System.out.println(today.equals(LocalDate.of(2025, 3, 15)));   // true
```

| Method | Question |
|---|---|
| `a.isBefore(b)` | Is a **earlier** than b? |
| `a.isAfter(b)` | Is a **later** than b? |
| `a.isEqual(b)` / `a.equals(b)` | Same date? |
| `a.compareTo(b)` | negative / 0 / positive (for sorting) |

Dates are `Comparable` (Chapter 25), so you can **sort** them:

```java
List<LocalDate> dates = new ArrayList<>(List.of(
    LocalDate.of(2025, 12, 25),
    LocalDate.of(2025, 1, 1),
    LocalDate.of(2025, 7, 4)
));
Collections.sort(dates);
System.out.println(dates);   // [2025-01-01, 2025-07-04, 2025-12-25]
```

> ⚠️ Don't use `<` or `>` with dates: `today < deadline` → ❌ error. Use `isBefore` / `isAfter`.

---

## 📏 Part 4: How long between two dates?

### Count days, weeks, months... — `ChronoUnit`

```java
import java.time.temporal.ChronoUnit;

LocalDate start = LocalDate.of(2025, 3, 1);
LocalDate end = LocalDate.of(2025, 12, 25);

long days = ChronoUnit.DAYS.between(start, end);
long weeks = ChronoUnit.WEEKS.between(start, end);
long months = ChronoUnit.MONTHS.between(start, end);

System.out.println(days + " days");       // 299 days
System.out.println(weeks + " weeks");     // 42 weeks
System.out.println(months + " months");   // 9 months
```

`ChronoUnit.DAYS.between(a, b)` = "how many **whole** days from a to b?" 🗓️

### Years, months and days together — `Period`

```java
import java.time.Period;

LocalDate birthday = LocalDate.of(2012, 5, 20);
LocalDate today = LocalDate.of(2025, 3, 15);

Period age = Period.between(birthday, today);
System.out.println(age);   // P12Y9M23D
System.out.println("You are " + age.getYears() + " years, "
        + age.getMonths() + " months and " + age.getDays() + " days old.");
// You are 12 years, 9 months and 23 days old.
```

| Code | Meaning |
|---|---|
| `Period.between(a, b)` | the difference as years + months + days |
| `P12Y9M23D` | ISO format: **P**eriod of 12 **Y**ears, 9 **M**onths, 23 **D**ays |
| `getYears()`, `getMonths()`, `getDays()` | the parts |

You can also **create** a Period and add it:

```java
LocalDate due = LocalDate.of(2025, 3, 15).plus(Period.ofWeeks(3));   // 2025-04-05
```

---

## 🕐 Part 5: `LocalTime` and `LocalDateTime`

### `LocalTime` — just a time

```java
import java.time.LocalTime;

LocalTime lunch = LocalTime.of(12, 30);
LocalTime alarm = LocalTime.parse("07:15");
LocalTime now = LocalTime.now();

System.out.println(lunch);                  // 12:30
System.out.println(lunch.plusMinutes(45));  // 13:15
System.out.println(alarm.isBefore(lunch));  // true
System.out.println(lunch.getHour());        // 12
```

### `LocalDateTime` — date + time

```java
import java.time.LocalDateTime;

LocalDateTime meeting = LocalDateTime.of(2025, 3, 15, 14, 30);
LocalDateTime fromText = LocalDateTime.parse("2025-03-15T14:30:00");

System.out.println(meeting);                // 2025-03-15T14:30
System.out.println(meeting.plusHours(3));   // 2025-03-15T17:30
System.out.println(meeting.toLocalDate());  // 2025-03-15
System.out.println(meeting.toLocalTime());  // 14:30
```

> 💡 The **`T`** in `2025-03-15T14:30` separates the date from the time. It's the ISO standard.

### Combine a date and a time

```java
LocalDateTime party = LocalDate.of(2025, 12, 31).atTime(20, 0);   // 2025-12-31T20:00
```

### `Duration` — hours, minutes, seconds

```java
import java.time.Duration;

LocalTime start = LocalTime.of(9, 0);
LocalTime end = LocalTime.of(17, 45);

Duration workDay = Duration.between(start, end);
System.out.println(workDay);                // PT8H45M
System.out.println(workDay.toMinutes());    // 525
System.out.println(workDay.toHours() + "h " + workDay.toMinutesPart() + "min");   // 8h 45min
```

| | `Period` | `Duration` |
|---|---|---|
| Measures | years, months, days | hours, minutes, seconds |
| Used with | `LocalDate` | `LocalTime`, `LocalDateTime`, `Instant` |
| Example | "2 years and 3 months" | "1 hour 30 minutes" |
| ISO text | `P2Y3M` | `PT1H30M` (**T** = time part) |

---

## 🎨 Part 6: Formatting — dates as nice text

ISO format (`2025-03-15`) is great for computers 🤖, but humans like other styles. Use **`DateTimeFormatter`**:

```java
import java.time.format.DateTimeFormatter;

LocalDate date = LocalDate.of(2025, 3, 15);

DateTimeFormatter f1 = DateTimeFormatter.ofPattern("dd/MM/yyyy");
DateTimeFormatter f2 = DateTimeFormatter.ofPattern("MMMM d, yyyy", Locale.ENGLISH);
DateTimeFormatter f3 = DateTimeFormatter.ofPattern("EEEE, d MMM yyyy", Locale.ENGLISH);

System.out.println(date.format(f1));   // 15/03/2025
System.out.println(date.format(f2));   // March 15, 2025
System.out.println(date.format(f3));   // Saturday, 15 Mar 2025
```

### 🔤 Pattern letters

| Letter(s) | Meaning | Example |
|---|---|---|
| `yyyy` | year | 2025 |
| `MM` | month as 2 digits | 03 |
| `M` | month number | 3 |
| `MMM` | short month name | Mar |
| `MMMM` | full month name | March |
| `dd` | day as 2 digits | 05 |
| `d` | day | 5 |
| `EEE` | short day name | Sat |
| `EEEE` | full day name | Saturday |
| `HH` | hour (00–23) | 14 |
| `hh` | hour (01–12) | 02 |
| `mm` | minutes | 30 |
| `ss` | seconds | 05 |
| `a` | AM / PM | PM |

> ⚠️ **Big `MM` = month, small `mm` = minutes!** A very common mistake. 😅

```java
LocalDateTime dt = LocalDateTime.of(2025, 3, 15, 14, 5);
DateTimeFormatter f = DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm", Locale.ENGLISH);
System.out.println(dt.format(f));   // 15.03.2025 14:05

DateTimeFormatter us = DateTimeFormatter.ofPattern("MM/dd/yyyy hh:mm a", Locale.ENGLISH);
System.out.println(dt.format(us));  // 03/15/2025 02:05 PM
```

> 💡 `Locale.ENGLISH` makes sure month and day **names** are in English. Without it, Java uses your computer's language (maybe "März" or "mars" 🌍).

### Reading text in your own format

```java
DateTimeFormatter f = DateTimeFormatter.ofPattern("dd/MM/yyyy");
LocalDate d = LocalDate.parse("25/12/2025", f);
System.out.println(d);   // 2025-12-25
```

If the text doesn't match → 💥 `DateTimeParseException`. Catch it when the text comes from a user (Chapter 33)!

---

## 🌍 Part 7: Time zones (the basics)

`LocalDateTime` has **no time zone**. "2025-03-15 14:30" — but **where**? In Paris? In Tokyo? 🤔

For **exact moments** that people in different places must agree on (a video call, a flight, when an order was paid), use:

### `ZonedDateTime` — date + time + zone

```java
import java.time.ZoneId;
import java.time.ZonedDateTime;

ZonedDateTime callInParis = ZonedDateTime.of(
        LocalDateTime.of(2025, 3, 15, 14, 0), ZoneId.of("Europe/Paris"));

ZonedDateTime sameMomentInTokyo = callInParis.withZoneSameInstant(ZoneId.of("Asia/Tokyo"));
ZonedDateTime sameMomentInNewYork = callInParis.withZoneSameInstant(ZoneId.of("America/New_York"));

System.out.println("Paris:    " + callInParis.toLocalTime());          // 14:00
System.out.println("Tokyo:    " + sameMomentInTokyo.toLocalTime());    // 22:00
System.out.println("New York: " + sameMomentInNewYork.toLocalTime());  // 09:00
```

📞 One video call — three different clock times! 🌍

### `Instant` — a moment on the world timeline

```java
import java.time.Instant;

Instant now = Instant.now();
System.out.println(now);   // e.g. 2026-10-10T08:15:30.123Z   (Z = UTC, the world's reference time)
```

An `Instant` is the **same** everywhere in the world. It's great for **timestamps** ("when was this created?").

### 🤔 Which one should I use?

| Situation | Use |
|---|---|
| A birthday, a holiday, a due date 📅 | `LocalDate` |
| Opening hours of a shop 🕘 | `LocalTime` |
| A school timetable, an appointment in **one** city | `LocalDateTime` |
| A flight, a meeting across countries ✈️ | `ZonedDateTime` |
| "When was this record created / changed?" (server timestamps) | `Instant` |

> 🌱 **Spring Boot tip:** For "created at" / "updated at" fields, many teams use `Instant` (or `LocalDateTime` in UTC). Spring and the database handle them automatically. JSON shows them in ISO format: `"2025-03-15T14:30:00Z"`.

---

## 🌱 Part 8: Dates in Spring Boot (a preview)

```java
@Entity
public class Order {
    @Id @GeneratedValue
    private Long id;

    private LocalDate deliveryDate;        // stored as a DATE column
    private Instant createdAt;             // stored as a TIMESTAMP column
}
```

```java
public record CreateEventRequest(
        String title,
        @Future LocalDate date,            // validation: must be in the future!
        LocalTime startTime
) { }
```

The JSON looks like:

```json
{
  "title": "Science Fair",
  "date": "2025-06-01",
  "startTime": "10:00"
}
```

Spring turns `"2025-06-01"` into a `LocalDate` **automatically**, because it's ISO format. 🎉

---

## 🎓 Part 9: Part 4 review project — Library loans 📚

This project uses **everything** from Part 4: lists, maps, sets, exceptions, generics, lambdas, streams, Optional, (annotations) and dates!

```java
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.Collectors;

public class LibraryLoans {

    // ----- data (records — Chapter 29) -----
    record Book(String isbn, String title, String author) { }

    record Loan(Book book, String member, LocalDate borrowed, LocalDate due, LocalDate returned) {
        boolean isOpen() {
            return returned == null;
        }

        boolean isLate(LocalDate today) {
            LocalDate end = isOpen() ? today : returned;
            return end.isAfter(due);
        }

        long daysLate(LocalDate today) {
            LocalDate end = isOpen() ? today : returned;
            return Math.max(0, ChronoUnit.DAYS.between(due, end));
        }

        Loan returnOn(LocalDate date) {
            return new Loan(book, member, borrowed, due, date);
        }
    }

    // ----- exceptions (Chapter 33) -----
    static class LibraryException extends RuntimeException {
        LibraryException(String message) {
            super(message);
        }
    }

    // ----- state -----
    private static final int LOAN_DAYS = 14;
    private static final double FINE_PER_DAY = 0.25;
    private static final DateTimeFormatter NICE = DateTimeFormatter.ofPattern("dd MMM yyyy", Locale.ENGLISH);

    private final Map<String, Book> books = new LinkedHashMap<>();   // Map (Chapter 31)
    private final List<Loan> loans = new ArrayList<>();              // List (Chapter 30)
    private final Set<String> members = new TreeSet<>();             // Set (Chapter 32)

    void addBook(Book book) {
        books.put(book.isbn(), book);
    }

    void addMember(String name) {
        if (!members.add(name)) {
            throw new LibraryException("Member already exists: " + name);
        }
    }

    // Optional (Chapter 37)
    Optional<Loan> openLoanFor(String isbn) {
        return loans.stream()
                .filter(l -> l.book().isbn().equals(isbn) && l.isOpen())
                .findFirst();
    }

    void borrow(String isbn, String member, LocalDate date) {
        if (!members.contains(member)) {
            throw new LibraryException("Unknown member: " + member);
        }
        Book book = Optional.ofNullable(books.get(isbn))
                .orElseThrow(() -> new LibraryException("Unknown book: " + isbn));
        openLoanFor(isbn).ifPresent(l -> {
            throw new LibraryException("'" + book.title() + "' is already borrowed by " + l.member());
        });
        loans.add(new Loan(book, member, date, date.plusDays(LOAN_DAYS), null));
        System.out.println("📖 " + member + " borrowed '" + book.title() + "' — due " + date.plusDays(LOAN_DAYS).format(NICE));
    }

    void giveBack(String isbn, LocalDate date) {
        Loan loan = openLoanFor(isbn)
                .orElseThrow(() -> new LibraryException("No open loan for " + isbn));
        loans.set(loans.indexOf(loan), loan.returnOn(date));
        System.out.println("📥 '" + loan.book().title() + "' returned on " + date.format(NICE));
    }

    void report(LocalDate today) {
        System.out.println("\n===== REPORT for " + today.format(NICE) + " =====");

        // Streams + lambdas (Chapters 35–36)
        List<Loan> late = loans.stream()
                .filter(l -> l.isLate(today))
                .sorted(Comparator.comparing((Loan l) -> l.daysLate(today)).reversed())
                .toList();

        System.out.println("⏰ Late loans:");
        late.forEach(l -> System.out.printf("   %-22s %-5s %2d days late, fine %.2f%n",
                l.book().title(), l.member(), l.daysLate(today), l.daysLate(today) * FINE_PER_DAY));

        Map<String, Long> loansPerMember = loans.stream()
                .collect(Collectors.groupingBy(Loan::member, TreeMap::new, Collectors.counting()));
        System.out.println("👥 Loans per member: " + loansPerMember);

        List<String> available = books.values().stream()
                .filter(b -> openLoanFor(b.isbn()).isEmpty())
                .map(Book::title)
                .sorted()
                .toList();
        System.out.println("✅ Available now: " + available);

        double totalFines = loans.stream()
                .mapToDouble(l -> l.daysLate(today) * FINE_PER_DAY)
                .sum();
        System.out.printf("💰 Total fines: %.2f%n", totalFines);
    }

    public static void main(String[] args) {
        LibraryLoans lib = new LibraryLoans();
        lib.addBook(new Book("111", "The Hobbit", "Tolkien"));
        lib.addBook(new Book("222", "Charlotte's Web", "White"));
        lib.addBook(new Book("333", "Matilda", "Dahl"));
        lib.addBook(new Book("444", "Wonder", "Palacio"));
        lib.addMember("Sara");
        lib.addMember("Tom");

        LocalDate day1 = LocalDate.of(2025, 3, 1);
        lib.borrow("111", "Sara", day1);
        lib.borrow("222", "Tom", day1.plusDays(2));
        lib.borrow("333", "Sara", day1.plusDays(5));

        // Exceptions in action
        List<Runnable> badActions = List.of(
                () -> lib.borrow("111", "Tom", day1.plusDays(3)),
                () -> lib.borrow("999", "Tom", day1),
                () -> lib.borrow("444", "Zoe", day1),
                () -> lib.addMember("Sara")
        );
        for (Runnable action : badActions) {
            try {
                action.run();
            } catch (LibraryException e) {
                System.out.println("❌ " + e.getMessage());
            }
        }

        lib.giveBack("222", day1.plusDays(20));

        lib.report(LocalDate.of(2025, 3, 25));
    }
}
```

**Output:**

```
📖 Sara borrowed 'The Hobbit' — due 15 Mar 2025
📖 Tom borrowed 'Charlotte's Web' — due 17 Mar 2025
📖 Sara borrowed 'Matilda' — due 20 Mar 2025
❌ 'The Hobbit' is already borrowed by Sara
❌ Unknown book: 999
❌ Unknown member: Zoe
❌ Member already exists: Sara
📥 'Charlotte's Web' returned on 21 Mar 2025

===== REPORT for 25 Mar 2025 =====
⏰ Late loans:
   The Hobbit             Sara  10 days late, fine 2.50
   Matilda                Sara   5 days late, fine 1.25
   Charlotte's Web        Tom    4 days late, fine 1.00
👥 Loans per member: {Sara=2, Tom=1}
✅ Available now: [Charlotte's Web, Wonder]
💰 Total fines: 4.75
```

### 🔍 Find the concepts! 🕵️

| Concept | Where | Chapter |
|---|---|---|
| `List` | `loans` | 30 |
| `Map` (`LinkedHashMap`, `TreeMap`) | `books`, `loansPerMember` | 31 |
| `Set` (`TreeSet`), `add` returns false | `members`, `addMember` | 32 |
| Custom exception, `try/catch` | `LibraryException`, the `badActions` loop | 33 |
| Generics | `Map<String, Book>`, `Optional<Loan>`, `List<Runnable>` | 34 |
| Lambdas, method references, `Runnable` | `() -> lib.borrow(...)`, `Book::title`, `Loan::member` | 35 |
| Streams: filter, sorted, map, groupingBy, mapToDouble | `report()` | 36 |
| `Optional`: `ofNullable`, `orElseThrow`, `ifPresent`, `isEmpty` | `borrow`, `giveBack`, `openLoanFor` | 37 |
| Records with methods, "wither" | `Loan.returnOn(...)` | 29 |
| Dates: `plusDays`, `isAfter`, `ChronoUnit.DAYS.between`, formatting | `Loan`, `NICE` | 39 |

> 💡 `Comparator.comparing((Loan l) -> l.daysLate(today))` — here we wrote the type `(Loan l)` because Java sometimes can't guess it when `.reversed()` comes after. A small trick worth knowing!

---

## ✋ Try it yourself

**Task 1:** Calculate how many days are left until your next birthday. (Hint: make this year's birthday date; if it's already passed, use next year's.)

<details>
<summary>Click to see one possible answer</summary>

```java
LocalDate today = LocalDate.now();
LocalDate birthday = LocalDate.of(today.getYear(), 5, 20);   // your birthday: May 20

if (!birthday.isAfter(today)) {
    birthday = birthday.plusYears(1);
}

long days = ChronoUnit.DAYS.between(today, birthday);
System.out.println(days + " days until your birthday! 🎂");
```

</details>

**Task 2:** Print the dates of all **Mondays** in March 2025.

<details>
<summary>Click to see the answer</summary>

```java
LocalDate d = LocalDate.of(2025, 3, 1);
while (d.getMonthValue() == 3) {
    if (d.getDayOfWeek() == DayOfWeek.MONDAY) {
        System.out.println(d);
    }
    d = d.plusDays(1);
}
// 2025-03-03, 2025-03-10, 2025-03-17, 2025-03-24, 2025-03-31
```

</details>

**Task 3:** Ask the user for their birth date in the format `dd/MM/yyyy`. Print their age in years. If the text is wrong, catch `DateTimeParseException` and ask again.

**Task 4:** A movie starts at 19:45 and is 2 hours 17 minutes long. When does it end? (Answer: 22:02)

<details>
<summary>Click to see the answer</summary>

```java
LocalTime start = LocalTime.of(19, 45);
LocalTime end = start.plus(Duration.ofMinutes(137));
System.out.println(end);   // 22:02
```

</details>

**Task 5:** In the library project, add a method `List<Book> booksBorrowedBy(String member)` using a stream. Then add a rule: a member with more than **2** open loans can't borrow another book.

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting that dates are immutable

```java
date.plusDays(5);          // ❌ result thrown away
date = date.plusDays(5);   // ✅
```

### Mistake 2: `MM` vs. `mm`

```java
DateTimeFormatter.ofPattern("dd/mm/yyyy")   // ❌ mm = MINUTES!
DateTimeFormatter.ofPattern("dd/MM/yyyy")   // ✅ MM = month
```

### Mistake 3: Invalid dates

```java
LocalDate.of(2025, 13, 1);   // 💥 DateTimeException: Invalid value for MonthOfYear
LocalDate.of(2025, 2, 29);   // 💥 2025 is not a leap year
```

### Mistake 4: Parsing text in the wrong format

```java
LocalDate.parse("15/03/2025");   // 💥 DateTimeParseException — parse() expects 2025-03-15
```

**Fix:** Give a formatter: `LocalDate.parse("15/03/2025", DateTimeFormatter.ofPattern("dd/MM/yyyy"))`.

### Mistake 5: Comparing with `<` or `==`

```java
if (a < b)       // ❌ error
if (a == b)      // ⚠️ compares objects, not dates
if (a.isBefore(b))   // ✅
if (a.equals(b))     // ✅
```

### Mistake 6: Using the old `Date` class

Old tutorials use `new Date()` and `SimpleDateFormat`. **Use `java.time`** instead. 👍

---

## ✅ Summary

- Use **`java.time`** — never the old `Date`/`Calendar`.
- `LocalDate` (date 📅), `LocalTime` (time 🕐), `LocalDateTime` (both). No time zone.
- Create: `now()`, `of(2025, 3, 15)` (months 1–12!), `parse("2025-03-15")`.
- Change: `plusDays`, `minusMonths`, `withDayOfMonth`... — they return **new** objects (immutable!).
- Compare: `isBefore`, `isAfter`, `equals`. Sort with `Collections.sort`.
- Differences: `ChronoUnit.DAYS.between(a, b)`, `Period.between(a, b)` (years/months/days), `Duration.between(t1, t2)` (hours/minutes).
- Format: `date.format(DateTimeFormatter.ofPattern("dd/MM/yyyy"))`. **`MM` = month, `mm` = minutes!**
- Time zones: `ZonedDateTime` for exact moments in a place, `Instant` for timestamps.
- Spring Boot works with these classes automatically, using ISO format in JSON. 🌱

---

## ❓ Quiz

1. Which class would you use for a birthday?
2. What does `LocalDate.of(2025, 1, 31).plusMonths(1)` give?
3. Why must you write `d = d.plusDays(1);` and not just `d.plusDays(1);`?
4. How do you count the days between two dates?
5. What's the difference between `Period` and `Duration`?
6. What's the difference between `MM` and `mm` in a pattern?
7. What does the `T` in `2025-03-15T14:30` mean?
8. Which class is best for "when was this order created" on a server?

<details>
<summary>Click to see the answers</summary>

1. `LocalDate`
2. `2025-02-28` (February has no 31st day).
3. Because dates are immutable — `plusDays` returns a new date, it doesn't change `d`.
4. `ChronoUnit.DAYS.between(a, b)`
5. `Period` is in years, months and days (for dates). `Duration` is in hours, minutes and seconds (for times).
6. `MM` = month, `mm` = minutes.
7. It separates the date from the time (ISO format).
8. `Instant` (an exact moment, the same everywhere).

</details>

---

## 🎉 Part 4 complete!

You now know the Java tools that **every** Spring Boot program uses:

- ✅ Lists, Maps, Sets
- ✅ Exceptions
- ✅ Generics
- ✅ Lambdas and Streams
- ✅ Optional
- ✅ Annotations
- ✅ Dates and times

**Your Java foundation is complete!** 🏗️ You know more Java now than many people who start Spring Boot. 💪

In **Part 5**, we learn the **tools** that professional Java developers use every day: **Maven** (to download libraries and build your project) and **Git** (to save the history of your code). Then, **Spring Boot** is very close! 🚀🌱

---

[⬅ Previous chapter](38-annotations.md) | [Table of Contents](../README.md) | [Next chapter: Maven ➡](../part-05-tools/40-maven.md)
