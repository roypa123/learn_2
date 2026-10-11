# Chapter 84 – Why we test, and JUnit

[⬅ Previous chapter](../part-10-security/83-jwt.md) | [Table of Contents](../README.md) | [Next chapter ➡](85-mockito.md)

---

## 🎯 Goal

Since Part 8, you've tested your app **by hand**: start it, type a curl command, read the answer, think "yes, that's right" 🤔, and do it again... and again... and **again** after every change. 😓

Today you'll teach the **computer** to do the checking. 🤖✅

At the end of this chapter you will know:

- **Why** programmers write tests — and what a test **is**
- How to write tests with **JUnit**: `@Test`, `assertEquals`, `assertThrows`
- How to run tests in **IntelliJ** and with **Maven** — and how to read a **red** result 🔴
- How a test **catches a real bug** 🐛
- How to test **many values** with **one** test: `@ParameterizedTest` 🔁
- A second, friendlier way to check things: **AssertJ** (`assertThat`)

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Test** | A small piece of code that **runs your code** and **checks** the answer. ✅❌ |
| **Unit test** | A test for **one small part** (one class, one method), all alone. 🧩 |
| **JUnit** | The most popular tool for writing and running tests in Java. |
| **Assertion** | A check inside a test: "I **say** the answer must be `A`." If it isn't, the test **fails**. |
| **Pass / fail** | A test **passes** ✅ (green) when all checks are OK, and **fails** ❌ (red) when one isn't. |
| **Bug** | A mistake in the code that makes it do the wrong thing. 🐛 |
| **Regression** | A bug in something that **used to work**. ("It worked yesterday!") 😩 |
| **Border value** | A value right at the **edge** of a rule, like `90` in "90 and more is an A". Bugs love edges! |
| **Parameterized test** | **One** test that runs with **many** different values. 🔁 |
| **AssertJ** | A library for assertions that read like English: `assertThat(letter).isEqualTo("A")`. |

---

## 📖 Story: The bakery's taste tester 🧁

Mrs. Baker makes **500** cupcakes every morning. 🧁🧁🧁 One day she changes the recipe a tiny bit — "a little less sugar". Did she break something? 🤔

She could taste **every** cupcake herself... that would take all day (and she'd feel sick 🤢).

So she hires a **taste tester** 👩‍🔬 with a **checklist**:

```
 📋 Every morning, check:
   ✅ Is it sweet?          (but not TOO sweet)
   ✅ Is it soft inside?
   ✅ Is the icing pink?
   ✅ Does it weigh 80 grams?
```

Now, after **every** change to the recipe, the tester runs the **same** checklist in **one minute**. If something is wrong, she knows **at once** — before any customer bites into a bad cupcake. 🎉

**Tests** are your app's taste tester:

| Bakery 🧁 | Your app 💻 |
|---|---|
| The checklist 📋 | Your **tests** |
| One line on the list | One **assertion** |
| Tasting takes 1 minute instead of all day | Tests run in **seconds** instead of an hour of curl |
| "The new recipe broke the icing!" | "The new code broke the grades!" — a **regression**, caught early 🐛 |

---

## 🤔 Part 1: Why test?

Testing by hand has big problems:

| Testing by hand 🖐️ | Automatic tests 🤖 |
|---|---|
| Slow: start the app, type, read, think... | Hundreds of checks in **seconds** |
| You **forget** to check old things | The tests check **everything**, every time |
| Boring → you skip it 😴 | The computer never gets bored |
| "It worked last week" — did it? | Proof, **right now**: green ✅ |

And there's one more big reason: **courage**. 🦁 With good tests, you can change and clean up your code **without fear**. If you break something, a test turns **red** and tells you **where**.

### 🧪 What does a test do?

Every test has the same **three steps**. Programmers call them **Arrange – Act – Assert** (or, more simply: **Given – When – Then**):

```
 1. Arrange 🧱  Prepare everything:          "Take a grade calculator."
 2. Act     🎬  Do the ONE thing you test:   "Ask it for the letter of 95."
 3. Assert  ✅  Check the answer:            "It must say A!"
```

That's all a test is! 🎉

---

## 🧮 Part 2: Something to test — `GradeCalculator`

Our school needs **report cards**. 📝 A score from 0 to 100 becomes a **letter**:

| Score | Letter |
|---|---|
| 90 – 100 | **A** 🌟 |
| 80 – 89 | **B** |
| 70 – 79 | **C** |
| 60 – 69 | **D** |
| 0 – 59 | **F** |
| below 0 or above 100 | not allowed ❌ |

Create a new package **`util`** (for "utilities", small helpers) with this class:

**`util/GradeCalculator.java`**

```java
package com.example.school.util;

import java.util.List;

public class GradeCalculator {

    public String letterFor(int score) {
        if (score < 0 || score > 100) {
            throw new IllegalArgumentException("Score must be between 0 and 100, but was " + score);
        }
        if (score > 90) {
            return "A";
        }
        if (score >= 80) {
            return "B";
        }
        if (score >= 70) {
            return "C";
        }
        if (score >= 60) {
            return "D";
        }
        return "F";
    }

    public double average(List<Integer> scores) {
        if (scores.isEmpty()) {
            throw new IllegalArgumentException("Cannot make an average of no scores");
        }
        int sum = 0;
        for (int score : scores) {
            sum = sum + score;
        }
        return (double) sum / scores.size();
    }
}
```

| Code | Meaning |
|---|---|
| `public class GradeCalculator` | A **normal** Java class — no `@Service`, no Spring. Just logic. 🧮 |
| `throw new IllegalArgumentException(...)` | A score like `-5` or `150` makes no sense → stop with an exception (Chapter 33). |
| `if (score > 90) return "A";` and so on | Check from the **top** grade down. The first `if` that fits decides. |
| `average(List<Integer> scores)` | The average of many scores: add them up, divide by how many. |
| `(double) sum / scores.size()` | Turn `sum` into a `double` **first**, so `7 / 2` gives `3.5` and not `3` (Chapter 8). |

👀 **Look closely.** There's a **bug** 🐛 hidden in this class! Can you find it? Don't worry if you can't — our tests will find it for us. 😉

---

## ✍️ Part 3: Your first JUnit test

Tests live in a **separate** folder: **`src/test/java`** (Chapter 50). They're **not** part of the finished app — they're only for checking.

⭐ **The rule:** the test for a class goes into the **same package**, in the **test** folder, with **`Test`** at the end of the name:

```
 src/main/java/com/example/school/util/GradeCalculator.java       ← the code
 src/test/java/com/example/school/util/GradeCalculatorTest.java   ← its test
```

💡 **IntelliJ shortcut:** click on the class name `GradeCalculator`, press **Ctrl+Shift+T** (Mac: **⌘+Shift+T**) → **Create New Test...** → OK. IntelliJ makes the file in the right place!

**`src/test/java/com/example/school/util/GradeCalculatorTest.java`**

```java
package com.example.school.util;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class GradeCalculatorTest {

    private GradeCalculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new GradeCalculator();
    }

    @Test
    void scoreOf95IsAnA() {
        String letter = calculator.letterFor(95);
        assertEquals("A", letter);
    }

    @Test
    void scoreOf85IsAB() {
        assertEquals("B", calculator.letterFor(85));
    }

    @Test
    void scoreOf30IsAnF() {
        assertEquals("F", calculator.letterFor(30));
    }

    @Test
    @DisplayName("90 is the lowest A")
    void scoreOf90IsAnA() {
        assertEquals("A", calculator.letterFor(90));
    }

    @Test
    void negativeScoreIsNotAllowed() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class,
                () -> calculator.letterFor(-5));
        assertEquals("Score must be between 0 and 100, but was -5", exception.getMessage());
    }
}
```

Let's go through it slowly:

| Code | Meaning |
|---|---|
| `import static org.junit.jupiter.api.Assertions.assertEquals;` | A **static import**: now we can write `assertEquals(...)` instead of `Assertions.assertEquals(...)` (Chapter 27). ("Jupiter" is just the name of the newest JUnit engine. 🪐) |
| `class GradeCalculatorTest` | The test class. No `public` needed — JUnit finds it anyway. |
| `private GradeCalculator calculator;` | The thing we test. |
| `@BeforeEach void setUp()` | ⭐ Runs **before each** test. Every test gets a **fresh** calculator — no test can mess things up for another one. 🧼 |
| `@Test` | ⭐ "This method **is a test**. JUnit, run it!" |
| `void scoreOf95IsAnA()` | The name says **what** we check. A good name is like a sentence. Tests return nothing (`void`). |
| `String letter = calculator.letterFor(95);` | **Act** 🎬: do the one thing. |
| `assertEquals("A", letter);` | **Assert** ✅: "The answer must **equal** `"A"`." ⚠️ The **expected** value comes **first**, the real one **second**. |
| `@DisplayName("90 is the lowest A")` | A nicer name to **show** in the results (spaces allowed!). |
| `assertThrows(IllegalArgumentException.class, () -> calculator.letterFor(-5))` | "Running this code **must throw** an `IllegalArgumentException`." The code is given as a **lambda** (Chapter 35), so JUnit can run it **inside** a safe box and catch the exception. 📦 |
| `exception.getMessage()` | `assertThrows` gives us the exception → we can check its **message** too. |

🤔 Where's the **Arrange** step? In `setUp()` — it's the same for every test, so we wrote it **once**. 👍

---

## ▶️ Part 4: Run the tests — and meet the bug 🐛

**In IntelliJ:** next to `class GradeCalculatorTest`, there's a green ▶️ (two arrows). Click it → **Run 'GradeCalculatorTest'**. The **Run** window shows each test with a ✅ or ❌.

**With Maven** (Chapter 50), in the project folder:

```bash
./mvnw test -Dtest=GradeCalculatorTest
```

| Part | Meaning |
|---|---|
| `./mvnw test` | Compile everything and run **all** tests. |
| `-Dtest=GradeCalculatorTest` | ...but only **this** test class. (Faster while you work on it.) |

Our real result (the important part):

```
[INFO] Running com.example.school.util.GradeCalculatorTest
[ERROR] Tests run: 5, Failures: 1, Errors: 0, Skipped: 0, Time elapsed: 0.231 s <<< FAILURE! -- in com.example.school.util.GradeCalculatorTest
[ERROR] com.example.school.util.GradeCalculatorTest.scoreOf90IsAnA -- Time elapsed: 0.031 s <<< FAILURE!
org.opentest4j.AssertionFailedError: expected: <A> but was: <B>
	at org.junit.jupiter.api.AssertionFailureBuilder.build(AssertionFailureBuilder.java:158)
	...
	at com.example.school.util.GradeCalculatorTest.scoreOf90IsAnA(GradeCalculatorTest.java:38)

[INFO] Results:
[ERROR] Failures: 
[ERROR]   GradeCalculatorTest.scoreOf90IsAnA:38 expected: <A> but was: <B>
[ERROR] Tests run: 5, Failures: 1, Errors: 0, Skipped: 0
[ERROR] BUILD FAILURE
```

🔴 **One test failed!** Let's read it like a detective 🕵️:

| Line | Meaning |
|---|---|
| `Tests run: 5, Failures: 1` | 5 tests ran, **4** passed, **1** failed. |
| `GradeCalculatorTest.scoreOf90IsAnA:38` | **Which** test, and the **line** in the test file. |
| `expected: <A> but was: <B>` | ⭐ The most important line: we **expected** `A`, but the code **gave** `B`. |
| `BUILD FAILURE` | Maven stops: "Don't use this code — it has a problem!" |

So: a score of **90** gives a **B**. But our table says 90 is an **A**! 🐛 Look at the code again:

```java
if (score > 90) {      // ❌ "more than 90" — 90 itself is NOT included!
```

It must be **"90 or more"**:

```java
if (score >= 90) {     // ✅
```

Fix it and run the tests again:

```
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

🟢 **All green!** 🎉

🤔 Notice: the tests for 95, 85 and 30 all **passed** — even with the bug! Only the test for **90**, the **border value**, found it. That's the big lesson:

> 🐛 **Bugs love borders.** Always test the values right at the **edge** of a rule: 89 and 90, 59 and 60, 0 and 100.

This kind of mistake (`>` instead of `>=`) is so common it has a name: an **off-by-one** error. ☝️

---

## 🔁 Part 5: Many values, one test — `@ParameterizedTest`

To test all the borders, we'd need **ten** almost identical tests: 100, 90, 89, 80, 79... 😩 JUnit has a better way:

```java
@ParameterizedTest
@CsvSource({
        "100, A",
        "90,  A",
        "89,  B",
        "80,  B",
        "79,  C",
        "70,  C",
        "69,  D",
        "60,  D",
        "59,  F",
        "0,   F"
})
void letterForBorderScores(int score, String expectedLetter) {
    assertEquals(expectedLetter, calculator.letterFor(score));
}
```

(Imports: `org.junit.jupiter.params.ParameterizedTest` and `org.junit.jupiter.params.provider.CsvSource`.)

| Code | Meaning |
|---|---|
| `@ParameterizedTest` | "This test runs **many times**, with different values." (Use it **instead** of `@Test`.) |
| `@CsvSource({ "100, A", ... })` | The values. **CSV** = "comma-separated values": each text is **one run**. `"90,  A"` → `score = 90`, `expectedLetter = "A"`. Extra spaces are ignored. |
| `void letterForBorderScores(int score, String expectedLetter)` | The test method gets the values as **parameters**. JUnit even turns the text `"90"` into the `int` 90. |

And for "not allowed" values, there's an even simpler one:

```java
@ParameterizedTest
@ValueSource(ints = {-1, 101, 500})
void scoresOutside0To100AreNotAllowed(int score) {
    assertThrows(IllegalArgumentException.class, () -> calculator.letterFor(score));
}
```

(Import `org.junit.jupiter.params.provider.ValueSource`.)

| Code | Meaning |
|---|---|
| `@ValueSource(ints = {-1, 101, 500})` | **One** value per run: three runs, with `-1`, `101` and `500`. |

In IntelliJ, every run shows up **separately**: `[1] score=100, expectedLetter=A`, `[2] score=90, expectedLetter=A`... And if we put the bug back in, our real Maven output names the exact run:

```
[ERROR] com.example.school.util.GradeCalculatorTest.letterForBorderScores(int, String)[2] -- Time elapsed: 0.014 s <<< FAILURE!
org.opentest4j.AssertionFailedError: expected: <A> but was: <B>
```

`[2]` = the **second** line of our `@CsvSource`: `"90, A"`. 🎯

---

## 🗣️ Part 6: AssertJ — tests that read like English

JUnit's `assertEquals` works fine. But Spring projects usually use another library for checks: **AssertJ**. It's already in your project (it comes with `spring-boot-starter-webmvc-test`). Compare:

```java
assertEquals("C", calculator.letterFor(75));                 // JUnit

assertThat(calculator.letterFor(75)).isEqualTo("C");          // AssertJ 🗣️ "assert that ... is equal to C"
```

With AssertJ, you **can't** mix up "expected" and "actual": the real value always goes into `assertThat(...)`, and the expected one comes after. 👍

Two AssertJ tests for our calculator:

```java
@Test
void scoreOf75IsAC_withAssertJ() {
    assertThat(calculator.letterFor(75)).isEqualTo("C");
}

@Test
void scoreOf150IsNotAllowed_withAssertJ() {
    assertThatThrownBy(() -> calculator.letterFor(150))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessage("Score must be between 0 and 100, but was 150");
}
```

(Imports: `import static org.assertj.core.api.Assertions.assertThat;` and `import static org.assertj.core.api.Assertions.assertThatThrownBy;`)

| Code | Meaning |
|---|---|
| `assertThat(x).isEqualTo(y)` | "x must equal y." |
| `assertThatThrownBy(() -> ...)` | "This code must throw something..." |
| `.isInstanceOf(IllegalArgumentException.class)` | "...of **this** kind..." |
| `.hasMessage("...")` | "...with **this** message." All in **one** sentence! 🗣️ |

AssertJ has **hundreds** of checks that read like English. A few you'll use a lot:

| AssertJ | Checks that... |
|---|---|
| `assertThat(name).isEqualTo("Sara")` | it's equal |
| `assertThat(age).isGreaterThan(10)` | it's bigger |
| `assertThat(email).contains("@")` | the text contains something |
| `assertThat(list).hasSize(3)` | the list has 3 items |
| `assertThat(list).contains("Sara", "Tom")` | the list contains these |
| `assertThat(optional).isEmpty()` | there's nothing inside |
| `assertThat(note).isNull()` | it's `null` |

And when an AssertJ check fails, the message is very clear. Our real one for `assertThat(calculator.letterFor(85)).isEqualTo("A")`:

```
org.opentest4j.AssertionFailedError: 

expected: "A"
 but was: "B"
```

🎯 **From now on, we'll use AssertJ** — it's what most Spring projects use, and it's what Spring's own test tools use (Chapter 86).

---

## 🟢 Part 7: Run ALL the tests

Run **every** test in the project:

```bash
./mvnw test
```

Our real result (shortened):

```
[INFO] Running com.example.school.SchoolApplicationTests
...
UserLoader: added the user admin with the role ADMIN
UserLoader: added the user teacher with the role TEACHER
DataLoader: added 2 classrooms, 3 courses and 3 students
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 19.48 s -- in com.example.school.SchoolApplicationTests
[INFO] Running com.example.school.util.GradeCalculatorTest
[INFO] Tests run: 24, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.628 s -- in com.example.school.util.GradeCalculatorTest
[INFO] Tests run: 25, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

(24 = our tests **plus** the mini project below. Each run of a parameterized test counts as one test.)

👀 Two things to notice:

1. **`SchoolApplicationTests`** — the `contextLoads()` test that Spring Initializr made in Chapter 49! It starts the **whole** app (look: the loaders ran!) and checks that it **can** start. It took **19 seconds**. 🐢
2. **`GradeCalculatorTest`**: 24 tests in **0.6 seconds**. 🚀 Why so fast? Because a **unit test** doesn't start Spring, Tomcat or a database — it only creates **one** object and calls it.

💡 Also important: `./mvnw package` (which builds your `.jar` file, Chapter 98) runs the tests **first**. If a test fails → **no jar**. Broken code can't be shipped! 🚫📦

🤔 Hmm, `contextLoads()` used our **real** database file (`./data/school`) — a test changing real data isn't great. We'll fix that in Chapter 87.

---

## 💻 Mini project: Test the average 📊

`GradeCalculator` has a second method: `average(List<Integer> scores)`. Write tests for it:

1. The average of `70, 80, 90` is `80.0`.
2. The average of `1, 1, 2` is about `1.33` (careful! 🤔).
3. The average of just `42` is `42.0`. (Use AssertJ.)
4. The average of **no** scores throws an `IllegalArgumentException` with the message `"Cannot make an average of no scores"`. (Use AssertJ.)

**Hint:** `List.of(70, 80, 90)` makes a list quickly (Chapter 30).

<details>
<summary>Click to see the answer</summary>

Add to `GradeCalculatorTest` (plus `import java.util.List;`):

```java
@Test
void averageOfThreeScores() {
    assertEquals(80.0, calculator.average(List.of(70, 80, 90)));
}

@Test
void averageCanHaveDecimals() {
    assertEquals(1.33, calculator.average(List.of(1, 1, 2)), 0.01);
}

@Test
void averageOfOneScoreIsThatScore() {
    assertThat(calculator.average(List.of(42))).isEqualTo(42.0);
}

@Test
void averageOfNoScoresIsNotAllowed() {
    assertThatThrownBy(() -> calculator.average(List.of()))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessage("Cannot make an average of no scores");
}
```

| Code | Meaning |
|---|---|
| `assertEquals(1.33, ..., 0.01)` | ⭐ The **third** value is the allowed **difference** ("delta"): "1.33, give or take 0.01". The real average is `1.3333333333333333` — it goes on forever, so we can never write it **exactly**. |
| `List.of()` | An **empty** list. |

Why the delta? Without it, our real result was:

```
org.opentest4j.AssertionFailedError: expected: <1.33> but was: <1.3333333333333333>
```

(With AssertJ, the same check is `assertThat(result).isCloseTo(1.33, within(0.01))` — `within` comes from `org.assertj.core.api.Assertions` too.)

All 24 tests: **green** ✅.

</details>

---

## ✋ Try it yourself

1. Change `if (score >= 80)` into `if (score > 80)`. Which tests turn red? Change it back.
2. Write a test that checks `letterFor(100)` is `"A"` — with `@DisplayName("100 is the best score")`. Find the display name in IntelliJ's results.
3. Write a test that calls `calculator.letterFor(150)` and expects `"A"` (without `assertThrows`). Run it. What does Maven say — **failure** or **error**?
4. Remove the `@Test` above `scoreOf85IsAB`. How many tests run now?

<details>
<summary>Click to see the answers</summary>

1. Only the tests that use **80**: the parameterized run `[4]` (`"80, B"`) fails with `expected: <B> but was: <C>`. Another border bug caught! 🐛
2. ```java
   @Test
   @DisplayName("100 is the best score")
   void scoreOf100IsAnA() {
       assertThat(calculator.letterFor(100)).isEqualTo("A");
   }
   ```
   IntelliJ shows "100 is the best score" instead of the method name.
3. An **error**, not a failure! Our real output: `Tests run: ..., Failures: ..., Errors: 1` and `<<< ERROR!` with `java.lang.IllegalArgumentException: Score must be between 0 and 100, but was 150`. **Failure** = a check said "wrong answer". **Error** = the test **crashed** with an exception nobody expected.
4. One test **less**. Without `@Test`, the method is just a normal method — JUnit **silently** skips it. No warning! 😱

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting `@Test`

The test simply **doesn't run** — and "no failures" looks like success. 🙈 **Fix:** Every test method needs `@Test` (or `@ParameterizedTest`). Watch the **number** of tests run.

### Mistake 2: Expected and actual swapped

```java
assertEquals(calculator.letterFor(90), "A");   // ❌ real value first
```

When it fails, the message says `expected: <B> but was: <A>` — the **opposite** of the truth! 😵 **Fix:** `assertEquals(expected, actual)` — or use AssertJ, where this can't happen.

### Mistake 3: Comparing decimals exactly

`assertEquals(1.33, 1.3333333333333333)` fails. **Fix:** Use a delta: `assertEquals(1.33, result, 0.01)`.

### Mistake 4: Only testing "easy" values

Our first three tests (95, 85, 30) all passed **with the bug**. **Fix:** Always test the **borders**: the smallest and biggest value of each rule.

### Mistake 5: A test file in the wrong folder

A test in `src/main/java` becomes part of the app — and can't even find JUnit (it's only there for tests). **Fix:** Tests go in **`src/test/java`**, same package as the class they test.

### Mistake 6: Tests that need each other

If test B only works after test A has run, you're in trouble: JUnit does **not** promise any order! **Fix:** Every test prepares its **own** things (with `@BeforeEach`).

---

## ✅ Summary

- A **test** runs your code and **checks** the answer. Tests are fast, never forget, and give you **courage** to change code. 🦁
- Every test: **Arrange** 🧱 → **Act** 🎬 → **Assert** ✅.
- **JUnit**: `@Test`, `@BeforeEach`, `@DisplayName`, `assertEquals(expected, actual)`, `assertThrows(...)`.
- Tests live in **`src/test/java`**, in the same package, named **`...Test`**.
- Run them with the green ▶️ in IntelliJ, or **`./mvnw test`** (`-Dtest=...` for one class). Read the red: **`expected: <A> but was: <B>`**.
- 🐛 **Bugs love borders**: test 89 **and** 90!
- **`@ParameterizedTest`** + **`@CsvSource`** / **`@ValueSource`**: one test, many values. 🔁
- **AssertJ**: `assertThat(x).isEqualTo(y)`, `assertThatThrownBy(...)` — reads like English. We use it from now on.
- **Failure** = wrong answer. **Error** = unexpected exception.

---

## ❓ Quiz

1. Give two reasons why automatic tests are better than testing by hand.
2. What are the three steps of a test?
3. What does `@BeforeEach` do, and why is it useful?
4. In `assertEquals(a, b)`, which one is the expected value?
5. The tests for 95, 85 and 30 passed, but the code had a bug. Why didn't they find it?
6. What does `@CsvSource({"90, A", "89, B"})` do?
7. Write the AssertJ version of `assertEquals("F", calculator.letterFor(10));`.
8. What's the difference between a **failure** and an **error**?

<details>
<summary>Click to see the answers</summary>

1. They're much faster, they check everything every time (they don't forget), they never get bored, and they give you courage to change code.
2. Arrange (prepare), Act (do the one thing), Assert (check the answer).
3. It runs before **each** test, so every test starts fresh (for example, with a new calculator). Tests can't disturb each other.
4. The **first** one (`a`).
5. The bug was at the **border** (`> 90` instead of `>= 90`), and none of those tests used the value 90.
6. It runs the parameterized test **twice**: once with `90` and `"A"`, once with `89` and `"B"`.
7. `assertThat(calculator.letterFor(10)).isEqualTo("F");`
8. A failure: an assertion found a wrong answer. An error: the test crashed with an exception nobody expected.

</details>

---

[⬅ Previous chapter](../part-10-security/83-jwt.md) | [Table of Contents](../README.md) | [Next chapter: Mockito: fake helpers for tests ➡](85-mockito.md)
