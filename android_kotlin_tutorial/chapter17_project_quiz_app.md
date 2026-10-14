# Chapter 17: 🛠️ Mini Project — Quiz App 🧠❓

> **What you will do in this chapter**
>
> 1. Plan a **multi-screen** app: requirements, screens, data, state ✏️
> 2. Set up a project with **all** the libraries from Part 4 📦
> 3. Build the **data layer**: model, repository interface, sample questions 🏪
> 4. Build an **AppContainer** and an **Application** class 🧰
> 5. Build a **QuizViewModel** with `UiState`, events, and **process-death safety** 💾
> 6. Build **3 screens**: Start → Quiz → Result 📱📱📱
> 7. Connect them with **type-safe Navigation** 🧭
> 8. Polish: progress bar, answer feedback, "Leave quiz?" dialog, previews ✨
> 9. Test with a **checklist** ✅
> 10. Challenges to go further 🚀
>
> **Time needed:** about 5 hours.
>
> **What you need to know:** Chapters 1–16, especially 13 (Navigation), 15 (ViewModel), and 16 (MVVM).

---

## 17.1 What Are We Building? 🎯

A **quiz app** with three topics: **🚀 Space**, **🐾 Animals**, and **💜 Kotlin**.

```
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│  🧠 Quiz Time!        │      │ ⬅️  🚀 Space    2/5   │      │                      │
│                      │      │ ▓▓▓▓▓▓▓░░░░░░░░░░░░  │      │        🏆             │
│  Choose a topic:     │      │                      │      │    Great job!        │
│ ╭──────────────────╮ │      │ How many planets are │      │                      │
│ │ 🚀 Space   5 Q's  │ │ ──▶  │ in our solar system? │ ──▶  │     4 / 5            │
│ ╰──────────────────╯ │ tap  │                      │ last │    ⭐⭐⭐⭐☆            │
│ ╭──────────────────╮ │      │ ╭──────────────────╮ │ Next │                      │
│ │ 🐾 Animals 5 Q's  │ │      │ │ 7                │ │      │ [   Play again   ]   │
│ ╰──────────────────╯ │      │ ╰──────────────────╯ │      │ [  Choose topic  ]   │
│ ╭──────────────────╮ │      │ ╭──────────────────╮ │      │                      │
│ │ 💜 Kotlin  5 Q's  │ │      │ │ 8            ✅   │ │      └──────────────────────┘
│ ╰──────────────────╯ │      │ ╰──────────────────╯ │
└──────────────────────┘      │ ...                  │
                              │ 💡 Mercury, Venus,…   │
                              │ [       Next       ] │
                              └──────────────────────┘
```

### Requirements 📋

1. The **Start** screen shows the topics. Tapping one starts its quiz.
2. Each quiz has **5 questions** in a **random order**.
3. Each question has **4 answers**. The user taps **one**.
4. After answering: the **correct** answer turns **green** ✅, a **wrong** choice turns **red** ❌, and a short **explanation** 💡 appears. Answers can't be changed.
5. A **Next** button goes to the next question. On the **last** question it says **See results**.
6. A **progress bar** and **"2 / 5"** show where you are.
7. Pressing **Back** during a quiz asks: **"Leave the quiz?"** ❓
8. The **Result** screen shows the **score**, **stars** ⭐, a **message**, and buttons **Play again** / **Choose topic**.
9. From the Result screen, Back goes to **Start** (not back into the finished quiz!).
10. **Rotation** and **process death** never lose your progress. 🔄💀

---

## 17.2 The Plan ✏️

### Screens and routes 🧭

| Screen | Route | Data it needs |
|---|---|---|
| Start | `Start` (object) | — |
| Quiz | `Quiz(categoryName: String)` | **Which** topic |
| Result | `Result(categoryName: String, score: Int, total: Int)` | Topic, score, total |

### The back stack 🥞

```
[Start]  ──tap topic──▶  [Start][Quiz]  ──See results──▶  [Start][Result]
                                         (popUpTo Quiz, inclusive)
[Start][Result]  ──Play again──▶  [Start][Quiz]     (popUpTo Start)
[Start][Result]  ──Choose topic / Back──▶  [Start]
```

The finished Quiz is **removed** when we go to Result — so Back never returns into an old quiz. ✅

### Layers and files 📁

```
com.example.quiz
 ├── QuizApplication.kt
 ├── MainActivity.kt
 ├── data/
 │    ├── model/Question.kt          (Question + QuizCategory)
 │    ├── QuestionRepository.kt      (interface)
 │    ├── InMemoryQuestionRepository.kt
 │    └── SampleQuestions.kt
 ├── di/
 │    └── AppContainer.kt
 └── ui/
      ├── theme/                     (already there)
      ├── navigation/
      │    ├── Routes.kt
      │    └── QuizNavHost.kt
      ├── start/StartScreen.kt
      ├── quiz/
      │    ├── QuizViewModel.kt
      │    └── QuizScreen.kt
      └── result/ResultScreen.kt
```

### The Quiz screen's state 🧠

Ask the 3 questions from Chapter 12:

**What changes?** → the questions (in random order), which question we're on, the answer picked, the score.
**Who needs it?** → only the Quiz screen → it lives in the **QuizViewModel**.
**What can be calculated?** → the current question, progress, "is it answered?", "is it the last one?".

| State | Type |
|---|---|
| `questions` | `List<Question>` (shuffled once) |
| `currentIndex` | `Int` |
| `selectedOption` | `Int?` (`null` = not answered yet) |
| `score` | `Int` |

---

## 17.3 Step 1: Create the Project and Add Libraries 📦

1. **File → New → New Project → Empty Activity**.
2. **Name:** `Quiz` · **Package:** `com.example.quiz` · **Finish**.
3. Your theme is called **`QuizTheme`**.

### `gradle/libs.versions.toml`

Add to the matching sections (keep everything that's already there):

```toml
[versions]
navigationCompose = "2.8.9"
kotlinxSerializationJson = "1.7.3"

[libraries]
androidx-navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigationCompose" }
kotlinx-serialization-json = { group = "org.jetbrains.kotlinx", name = "kotlinx-serialization-json", version.ref = "kotlinxSerializationJson" }
androidx-lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycleRuntimeKtx" }
androidx-lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycleRuntimeKtx" }

[plugins]
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
```

### `build.gradle.kts (Module :app)`

```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.kotlin.serialization)
}

// ... android { } unchanged ...

dependencies {
    // ... existing lines ...
    implementation(libs.androidx.navigation.compose)
    implementation(libs.kotlinx.serialization.json)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)
}
```

**Sync Now** 🔄 ✅

> 💡 This is the **standard starter set** for a modern Compose app. Save it somewhere — you'll use it in almost every project! 📋

### Make the packages

Right-click `com.example.quiz` → **New → Package**, and make: `data`, `data.model`, `di`, `ui.navigation`, `ui.start`, `ui.quiz`, `ui.result`.

---

## 17.4 Step 2: The Data Layer 🏪

### `data/model/Question.kt`

```kotlin
package com.example.quiz.data.model

enum class QuizCategory(val label: String, val emoji: String) {
    SPACE("Space", "🚀"),
    ANIMALS("Animals", "🐾"),
    KOTLIN("Kotlin", "💜")
}

data class Question(
    val id: Int,
    val category: QuizCategory,
    val text: String,
    val options: List<String>,
    val correctIndex: Int,
    val explanation: String
) {
    val correctAnswer: String get() = options[correctIndex]
}
```

| Code | Meaning |
|---|---|
| `enum class QuizCategory` | Exactly **3** topics, each with a label and an emoji (Chapter 4). |
| `options: List<String>` | The 4 possible answers. |
| `correctIndex: Int` | **Which** option is right — remember, counting starts at **0**! (Chapter 3) |
| `val correctAnswer get() = ...` | A **calculated** property (Chapter 15) — handy for showing the right answer. |

### `data/QuestionRepository.kt` — the promise 📜

```kotlin
package com.example.quiz.data

import com.example.quiz.data.model.Question
import com.example.quiz.data.model.QuizCategory

interface QuestionRepository {
    /** All questions for one topic (in their original order). */
    fun getQuestions(category: QuizCategory): List<Question>

    /** One question by its id, or null. */
    fun getQuestion(id: Int): Question?

    /** How many questions a topic has. */
    fun countQuestions(category: QuizCategory): Int
}
```

> ℹ️ No `StateFlow` this time: quiz questions **don't change** while the app runs, so simple functions are enough. Choose the **simplest** tool that does the job! 🧰

### `data/SampleQuestions.kt` — 15 questions

```kotlin
package com.example.quiz.data

import com.example.quiz.data.model.Question
import com.example.quiz.data.model.QuizCategory

val sampleQuestions = listOf(
    // ---------- 🚀 SPACE ----------
    Question(
        id = 1, category = QuizCategory.SPACE,
        text = "Which planet is closest to the Sun?",
        options = listOf("Venus", "Mercury", "Mars", "Earth"),
        correctIndex = 1,
        explanation = "Mercury is the closest planet to the Sun, and also the smallest planet."
    ),
    Question(
        id = 2, category = QuizCategory.SPACE,
        text = "How many planets are in our solar system?",
        options = listOf("7", "8", "9", "10"),
        correctIndex = 1,
        explanation = "There are 8 planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune."
    ),
    Question(
        id = 3, category = QuizCategory.SPACE,
        text = "What is the name of our galaxy?",
        options = listOf("Andromeda", "Whirlpool", "Milky Way", "Sombrero"),
        correctIndex = 2,
        explanation = "We live in the Milky Way, a spiral galaxy with billions of stars."
    ),
    Question(
        id = 4, category = QuizCategory.SPACE,
        text = "Which planet is famous for its big, bright rings?",
        options = listOf("Saturn", "Mars", "Mercury", "Venus"),
        correctIndex = 0,
        explanation = "Saturn's rings are made of ice and rock. They are the biggest and brightest rings in our solar system."
    ),
    Question(
        id = 5, category = QuizCategory.SPACE,
        text = "What does the Moon travel around?",
        options = listOf("The Sun", "Mars", "Jupiter", "The Earth"),
        correctIndex = 3,
        explanation = "The Moon goes around the Earth about once every 27 days."
    ),

    // ---------- 🐾 ANIMALS ----------
    Question(
        id = 6, category = QuizCategory.ANIMALS,
        text = "What is the largest animal on Earth?",
        options = listOf("African elephant", "Blue whale", "Giraffe", "Great white shark"),
        correctIndex = 1,
        explanation = "The blue whale is the largest animal that has ever lived — bigger than any dinosaur!"
    ),
    Question(
        id = 7, category = QuizCategory.ANIMALS,
        text = "How many legs does a spider have?",
        options = listOf("6", "8", "10", "12"),
        correctIndex = 1,
        explanation = "Spiders have 8 legs. Insects, like ants, have 6."
    ),
    Question(
        id = 8, category = QuizCategory.ANIMALS,
        text = "Which bird cannot fly?",
        options = listOf("Eagle", "Parrot", "Penguin", "Sparrow"),
        correctIndex = 2,
        explanation = "Penguins cannot fly, but they are excellent swimmers."
    ),
    Question(
        id = 9, category = QuizCategory.ANIMALS,
        text = "What do bees make?",
        options = listOf("Milk", "Honey", "Silk", "Butter"),
        correctIndex = 1,
        explanation = "Bees make honey from the nectar of flowers."
    ),
    Question(
        id = 10, category = QuizCategory.ANIMALS,
        text = "Which animal is often called the \"King of the Jungle\"?",
        options = listOf("Tiger", "Gorilla", "Elephant", "Lion"),
        correctIndex = 3,
        explanation = "The lion is called the King of the Jungle, even though most lions live in grasslands."
    ),

    // ---------- 💜 KOTLIN ----------
    Question(
        id = 11, category = QuizCategory.KOTLIN,
        text = "Which keyword makes a variable that cannot be changed?",
        options = listOf("var", "val", "fun", "set"),
        correctIndex = 1,
        explanation = "val is a locked box 🔒. Use var only when the value must change."
    ),
    Question(
        id = 12, category = QuizCategory.KOTLIN,
        text = "What does the ? mean in the type String? ",
        options = listOf("It is a list", "It is private", "It can be null", "It is a number"),
        correctIndex = 2,
        explanation = "String? means \"a String or nothing (null)\". This is Kotlin's null safety."
    ),
    Question(
        id = 13, category = QuizCategory.KOTLIN,
        text = "In Kotlin, what is the result of 7 / 2 (both are Int)?",
        options = listOf("3.5", "4", "3", "2"),
        correctIndex = 2,
        explanation = "Int divided by Int gives an Int. The part after the dot is cut off: 7 / 2 = 3."
    ),
    Question(
        id = 14, category = QuizCategory.KOTLIN,
        text = "Which kind of class gives you copy() and a nice toString() for free?",
        options = listOf("open class", "data class", "enum class", "abstract class"),
        correctIndex = 1,
        explanation = "A data class gives you toString(), equals(), copy(), and more — for free!"
    ),
    Question(
        id = 15, category = QuizCategory.KOTLIN,
        text = "Which function prints text and then moves to a new line?",
        options = listOf("print", "echo", "write", "println"),
        correctIndex = 3,
        explanation = "println = print line. It shows the text and then goes to a new line."
    )
)
```

> ✏️ **Notice:** the right answer is in **different** positions (0, 1, 2, 3). If it were always first, the quiz would be too easy! 😄

### `data/InMemoryQuestionRepository.kt`

```kotlin
package com.example.quiz.data

import com.example.quiz.data.model.Question
import com.example.quiz.data.model.QuizCategory

class InMemoryQuestionRepository(
    private val allQuestions: List<Question> = sampleQuestions
) : QuestionRepository {

    override fun getQuestions(category: QuizCategory): List<Question> =
        allQuestions.filter { it.category == category }

    override fun getQuestion(id: Int): Question? =
        allQuestions.find { it.id == id }

    override fun countQuestions(category: QuizCategory): Int =
        allQuestions.count { it.category == category }
}
```

Short and simple: `filter`, `find`, `count` (Chapter 3). ✅

---

## 17.5 Step 3: DI — Container and Application 🧰

### `di/AppContainer.kt`

```kotlin
package com.example.quiz.di

import com.example.quiz.data.InMemoryQuestionRepository
import com.example.quiz.data.QuestionRepository

interface AppContainer {
    val questionRepository: QuestionRepository
}

class DefaultAppContainer : AppContainer {
    override val questionRepository: QuestionRepository by lazy {
        InMemoryQuestionRepository()
    }
}
```

### `QuizApplication.kt` (in `com.example.quiz`)

```kotlin
package com.example.quiz

import android.app.Application
import com.example.quiz.di.AppContainer
import com.example.quiz.di.DefaultAppContainer

class QuizApplication : Application() {
    lateinit var container: AppContainer

    override fun onCreate() {
        super.onCreate()
        container = DefaultAppContainer()
    }
}
```

### `AndroidManifest.xml`

```xml
<application
    android:name=".QuizApplication"
    ... >
```

⚠️ Don't forget this line! (Chapter 16) 💥

---

## 17.6 Step 4: Routes 🧭

### `ui/navigation/Routes.kt`

```kotlin
package com.example.quiz.ui.navigation

import kotlinx.serialization.Serializable

@Serializable
object Start

@Serializable
data class Quiz(val categoryName: String)

@Serializable
data class Result(val categoryName: String, val score: Int, val total: Int)
```

**Why `categoryName: String` and not `category: QuizCategory`?** Routes are saved as **text**, and simple types are the **safest** to pass. We send the enum's **name** (`"SPACE"`) and turn it back with `QuizCategory.valueOf(...)`. (Same trick as Chapter 15's `SavedStateHandle`!) 🔤↔️🔠

---

## 17.7 Step 5: The QuizViewModel — The Brain 🧠

### `ui/quiz/QuizViewModel.kt`

```kotlin
package com.example.quiz.ui.quiz

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.ViewModelProvider.AndroidViewModelFactory.Companion.APPLICATION_KEY
import androidx.lifecycle.createSavedStateHandle
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import androidx.navigation.toRoute
import com.example.quiz.QuizApplication
import com.example.quiz.data.QuestionRepository
import com.example.quiz.data.model.Question
import com.example.quiz.data.model.QuizCategory
import com.example.quiz.ui.navigation.Quiz
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

// ---------- State ----------

data class QuizUiState(
    val category: QuizCategory = QuizCategory.SPACE,
    val questions: List<Question> = emptyList(),
    val currentIndex: Int = 0,
    val selectedOption: Int? = null,
    val score: Int = 0
) {
    val total: Int get() = questions.size
    val currentQuestion: Question? get() = questions.getOrNull(currentIndex)
    val questionNumber: Int get() = currentIndex + 1
    val isAnswered: Boolean get() = selectedOption != null
    val isLastQuestion: Boolean get() = currentIndex == questions.lastIndex
    val progress: Float get() = if (total == 0) 0f else questionNumber.toFloat() / total
    val answeredCorrectly: Boolean
        get() = selectedOption != null && selectedOption == currentQuestion?.correctIndex
}

// ---------- Events ----------

sealed interface QuizEvent {
    data class OptionSelected(val index: Int) : QuizEvent
    data object NextQuestion : QuizEvent
}

// ---------- ViewModel ----------

class QuizViewModel(
    private val savedStateHandle: SavedStateHandle,
    private val repository: QuestionRepository
) : ViewModel() {

    private val category: QuizCategory =
        QuizCategory.valueOf(savedStateHandle.toRoute<Quiz>().categoryName)

    private val _uiState = MutableStateFlow(createStartState())
    val uiState: StateFlow<QuizUiState> = _uiState.asStateFlow()

    fun onEvent(event: QuizEvent) {
        when (event) {
            is QuizEvent.OptionSelected -> selectOption(event.index)
            QuizEvent.NextQuestion -> goToNextQuestion()
        }
    }

    private fun selectOption(index: Int) {
        val state = _uiState.value
        if (state.isAnswered) return                       // answers can't be changed
        val isCorrect = index == state.currentQuestion?.correctIndex
        updateState {
            it.copy(
                selectedOption = index,
                score = if (isCorrect) it.score + 1 else it.score
            )
        }
    }

    private fun goToNextQuestion() {
        val state = _uiState.value
        if (!state.isAnswered || state.isLastQuestion) return
        updateState { it.copy(currentIndex = it.currentIndex + 1, selectedOption = null) }
    }

    // ---------- Saving and restoring (for process death) ----------

    private fun updateState(change: (QuizUiState) -> QuizUiState) {
        _uiState.update(change)
        val s = _uiState.value
        savedStateHandle[KEY_QUESTION_IDS] = s.questions.map { it.id }.toIntArray()
        savedStateHandle[KEY_INDEX] = s.currentIndex
        savedStateHandle[KEY_SELECTED] = s.selectedOption ?: NO_SELECTION
        savedStateHandle[KEY_SCORE] = s.score
    }

    private fun createStartState(): QuizUiState {
        val savedIds: IntArray? = savedStateHandle[KEY_QUESTION_IDS]

        if (savedIds != null) {
            // 💾 Restoring after process death
            val questions = savedIds.mapNotNull { repository.getQuestion(it) }
            val savedSelected: Int = savedStateHandle[KEY_SELECTED] ?: NO_SELECTION
            return QuizUiState(
                category = category,
                questions = questions,
                currentIndex = savedStateHandle[KEY_INDEX] ?: 0,
                selectedOption = if (savedSelected == NO_SELECTION) null else savedSelected,
                score = savedStateHandle[KEY_SCORE] ?: 0
            )
        }

        // 🆕 A brand-new quiz: shuffle the questions once
        val questions = repository.getQuestions(category).shuffled()
        savedStateHandle[KEY_QUESTION_IDS] = questions.map { it.id }.toIntArray()
        return QuizUiState(category = category, questions = questions)
    }

    companion object {
        private const val KEY_QUESTION_IDS = "question_ids"
        private const val KEY_INDEX = "index"
        private const val KEY_SELECTED = "selected"
        private const val KEY_SCORE = "score"
        private const val NO_SELECTION = -1

        val Factory: ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val app = this[APPLICATION_KEY] as QuizApplication
                QuizViewModel(
                    savedStateHandle = createSavedStateHandle(),
                    repository = app.container.questionRepository
                )
            }
        }
    }
}
```

### Every important part explained

#### Part 1: `QuizUiState` — 5 stored, 7 calculated

```kotlin
data class QuizUiState(
    val category: QuizCategory = QuizCategory.SPACE,
    val questions: List<Question> = emptyList(),
    val currentIndex: Int = 0,
    val selectedOption: Int? = null,
    val score: Int = 0
) {
    val currentQuestion: Question? get() = questions.getOrNull(currentIndex)
    val isAnswered: Boolean get() = selectedOption != null
    val progress: Float get() = if (total == 0) 0f else questionNumber.toFloat() / total
    ...
}
```

| Calculated value | Meaning | Example (question 2 of 5) |
|---|---|---|
| `total` | Number of questions | 5 |
| `currentQuestion` | The question to show (`getOrNull` → never crashes, Chapter 3) | the planets question |
| `questionNumber` | For people, counting starts at **1** 🙂 | 2 |
| `isAnswered` | Did the user pick something? | `true` / `false` |
| `isLastQuestion` | Is this the final one? | `false` |
| `progress` | For the progress bar, from 0.0 to 1.0 | 2 ÷ 5 = **0.4** |
| `answeredCorrectly` | Was the pick right? | |

> 💡 `selectedOption: Int?` — **`null` means "not answered yet"**. A nullable value that does two jobs, like `noteToDelete` in Chapter 11. ✨

> ⚠️ `questionNumber.toFloat() / total` — we turn one number into a `Float` **first**, so the division keeps decimals (Chapter 2: `2 / 5` would be `0`!).

#### Part 2: Reading the topic from the route

```kotlin
    private val category: QuizCategory =
        QuizCategory.valueOf(savedStateHandle.toRoute<Quiz>().categoryName)
```

1. `toRoute<Quiz>()` → the route object (Chapter 15).
2. `.categoryName` → `"SPACE"`.
3. `QuizCategory.valueOf("SPACE")` → `QuizCategory.SPACE` (Chapter 4).

#### Part 3: The rules live in the ViewModel 📏

```kotlin
    private fun selectOption(index: Int) {
        val state = _uiState.value
        if (state.isAnswered) return                       // answers can't be changed
        val isCorrect = index == state.currentQuestion?.correctIndex
        updateState {
            it.copy(
                selectedOption = index,
                score = if (isCorrect) it.score + 1 else it.score
            )
        }
    }
```

| Rule | How |
|---|---|
| You can't change your answer | `if (state.isAnswered) return` — early return (Chapter 12). Even if the UI forgot to disable the buttons, the **ViewModel** protects the score. 🛡️ |
| A right answer gives +1 | `score = if (isCorrect) it.score + 1 else it.score` |

```kotlin
    private fun goToNextQuestion() {
        val state = _uiState.value
        if (!state.isAnswered || state.isLastQuestion) return
        updateState { it.copy(currentIndex = it.currentIndex + 1, selectedOption = null) }
    }
```

- You can only go **next** after answering, and **not** past the last question.
- Moving on: index **+1** and `selectedOption = null` (the new question isn't answered yet).

> 💡 **"Defensive" code:** The UI already hides the Next button until you answer. But the ViewModel **checks again**. If someone (or a future you 😅) changes the UI, the rules **still** hold. That's what a **brain** is for. 🧠

#### Part 4: Saving everything for process death 💾

```kotlin
    private fun updateState(change: (QuizUiState) -> QuizUiState) {
        _uiState.update(change)
        val s = _uiState.value
        savedStateHandle[KEY_QUESTION_IDS] = s.questions.map { it.id }.toIntArray()
        savedStateHandle[KEY_INDEX] = s.currentIndex
        savedStateHandle[KEY_SELECTED] = s.selectedOption ?: NO_SELECTION
        savedStateHandle[KEY_SCORE] = s.score
    }
```

The same **"change and save in one place"** pattern as Chapter 15. ☕

| Saved | How | Why like this? |
|---|---|---|
| The shuffled **order** | `questions.map { it.id }.toIntArray()` → e.g. `[3, 1, 5, 2, 4]` | Save **ids**, not whole questions (keep it small! Chapter 14). `IntArray` is a simple array of numbers that the Bundle can store. |
| The index, score | plain `Int`s | simple ✅ |
| The selected option | `selectedOption ?: NO_SELECTION` → `-1` means "none" | Saving `null` in a Bundle is awkward, so we use a **special number** instead. |

#### Part 5: Starting fresh or restoring

```kotlin
    private fun createStartState(): QuizUiState {
        val savedIds: IntArray? = savedStateHandle[KEY_QUESTION_IDS]

        if (savedIds != null) {
            val questions = savedIds.mapNotNull { repository.getQuestion(it) }
            ...
            return QuizUiState(...)          // 💾 restored
        }

        val questions = repository.getQuestions(category).shuffled()
        savedStateHandle[KEY_QUESTION_IDS] = questions.map { it.id }.toIntArray()
        return QuizUiState(category = category, questions = questions)   // 🆕 fresh
    }
```

| Code | Meaning |
|---|---|
| `savedIds != null` | Something was saved → we're **coming back** after process death. |
| `savedIds.mapNotNull { repository.getQuestion(it) }` | Turn ids back into questions. `mapNotNull` = `map`, but **skip** any `null` results (in case a question disappeared). 🧹 |
| `.shuffled()` | A **new** list in **random** order (Chapter 3). Done **once** — so rotation doesn't reshuffle! 🔀 |

> 🤔 **Why does order matter?** Without saving the order, after process death the questions would be shuffled **again**, and "question 3" would be a **different** question. The user's score wouldn't make sense! 😵

---

## 17.8 Step 6: The Screens 🎨

### `ui/start/StartScreen.kt`

```kotlin
package com.example.quiz.ui.start

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.quiz.data.model.QuizCategory
import com.example.quiz.ui.theme.QuizTheme

@Composable
fun StartScreen(
    questionCount: (QuizCategory) -> Int,
    onCategoryClick: (QuizCategory) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Spacer(modifier = Modifier.height(16.dp))
        Text("🧠", fontSize = 64.sp, modifier = Modifier.align(Alignment.CenterHorizontally))
        Text(
            text = "Quiz Time!",
            style = MaterialTheme.typography.headlineLarge,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.align(Alignment.CenterHorizontally)
        )
        Text(
            text = "Choose a topic to start:",
            style = MaterialTheme.typography.titleMedium,
            modifier = Modifier.align(Alignment.CenterHorizontally)
        )
        Spacer(modifier = Modifier.height(8.dp))

        QuizCategory.entries.forEach { category ->
            CategoryCard(
                category = category,
                count = questionCount(category),
                onClick = { onCategoryClick(category) }
            )
        }
    }
}

@Composable
private fun CategoryCard(category: QuizCategory, count: Int, onClick: () -> Unit) {
    ElevatedCard(onClick = onClick, modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.padding(20.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(category.emoji, fontSize = 40.sp)
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(category.label, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Text(
                    text = "$count questions",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
            Text("▶", style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.primary)
        }
    }
}

@Preview(showSystemUi = true)
@Composable
private fun StartScreenPreview() {
    QuizTheme {
        Surface { StartScreen(questionCount = { 5 }, onCategoryClick = {}) }
    }
}
```

| New idea | Meaning |
|---|---|
| `questionCount: (QuizCategory) -> Int` | A **lambda that gives back a value**! The screen asks "*how many questions for this topic?*" without knowing about the repository. In the preview we just say `{ 5 }`. 🎯 |
| `private fun CategoryCard` | `private` → only **this file** can use it. It's a helper for the Start screen only. 🔒 |
| `private fun StartScreenPreview` | Previews can be private too — keeps the "public" list of functions clean. |

> 💡 The Start screen needs **no ViewModel** — it has no state of its own. Not every screen needs one! Keep it simple. 😊

### `ui/quiz/QuizScreen.kt`

```kotlin
package com.example.quiz.ui.quiz

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.quiz.data.model.Question
import com.example.quiz.data.model.QuizCategory
import com.example.quiz.data.sampleQuestions
import com.example.quiz.ui.theme.QuizTheme

// Fixed feedback colors (with black text) — readable in light AND dark mode
private val CorrectColor = Color(0xFFC8E6C9)
private val CorrectBorder = Color(0xFF2E7D32)
private val WrongColor = Color(0xFFFFCDD2)
private val WrongBorder = Color(0xFFC62828)

// ---------- Route ----------

@Composable
fun QuizRoute(
    onFinished: (score: Int, total: Int) -> Unit,
    onLeave: () -> Unit,
    viewModel: QuizViewModel = viewModel(factory = QuizViewModel.Factory)
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    QuizScreen(
        uiState = uiState,
        onOptionClick = { index -> viewModel.onEvent(QuizEvent.OptionSelected(index)) },
        onNextClick = {
            if (uiState.isLastQuestion) {
                onFinished(uiState.score, uiState.total)
            } else {
                viewModel.onEvent(QuizEvent.NextQuestion)
            }
        },
        onLeave = onLeave
    )
}

// ---------- Screen ----------

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QuizScreen(
    uiState: QuizUiState,
    onOptionClick: (Int) -> Unit,
    onNextClick: () -> Unit,
    onLeave: () -> Unit
) {
    var showLeaveDialog by rememberSaveable { mutableStateOf(false) }

    BackHandler { showLeaveDialog = true }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("${uiState.category.emoji} ${uiState.category.label}") },
                navigationIcon = {
                    IconButton(onClick = { showLeaveDialog = true }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Leave quiz")
                    }
                },
                actions = {
                    Text(
                        text = "${uiState.questionNumber} / ${uiState.total}",
                        style = MaterialTheme.typography.titleMedium,
                        modifier = Modifier.padding(end = 16.dp)
                    )
                }
            )
        }
    ) { innerPadding ->
        val question = uiState.currentQuestion ?: return@Scaffold

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            LinearProgressIndicator(
                progress = { uiState.progress },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = question.text,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(8.dp))

            question.options.forEachIndexed { index, option ->
                OptionCard(
                    text = option,
                    state = optionState(index, question, uiState.selectedOption),
                    enabled = !uiState.isAnswered,
                    onClick = { onOptionClick(index) }
                )
            }

            if (uiState.isAnswered) {
                FeedbackCard(
                    correct = uiState.answeredCorrectly,
                    correctAnswer = question.correctAnswer,
                    explanation = question.explanation
                )
                Button(onClick = onNextClick, modifier = Modifier.fillMaxWidth()) {
                    Text(if (uiState.isLastQuestion) "See results 🏁" else "Next ➡️")
                }
            }
        }
    }

    if (showLeaveDialog) {
        AlertDialog(
            onDismissRequest = { showLeaveDialog = false },
            title = { Text("Leave the quiz?") },
            text = { Text("Your progress in this quiz will be lost.") },
            confirmButton = {
                TextButton(onClick = {
                    showLeaveDialog = false
                    onLeave()
                }) { Text("Leave") }
            },
            dismissButton = {
                TextButton(onClick = { showLeaveDialog = false }) { Text("Keep playing") }
            }
        )
    }
}

// ---------- Option look ----------

enum class OptionState { NORMAL, CORRECT, WRONG, FADED }

fun optionState(index: Int, question: Question, selected: Int?): OptionState = when {
    selected == null -> OptionState.NORMAL
    index == question.correctIndex -> OptionState.CORRECT
    index == selected -> OptionState.WRONG
    else -> OptionState.FADED
}

@Composable
private fun OptionCard(
    text: String,
    state: OptionState,
    enabled: Boolean,
    onClick: () -> Unit
) {
    val (container, border, content) = when (state) {
        OptionState.NORMAL -> Triple(
            MaterialTheme.colorScheme.surface,
            MaterialTheme.colorScheme.outline,
            MaterialTheme.colorScheme.onSurface
        )
        OptionState.CORRECT -> Triple(CorrectColor, CorrectBorder, Color.Black)
        OptionState.WRONG -> Triple(WrongColor, WrongBorder, Color.Black)
        OptionState.FADED -> Triple(
            MaterialTheme.colorScheme.surface,
            MaterialTheme.colorScheme.outlineVariant,
            MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
        )
    }
    val mark = when (state) {
        OptionState.CORRECT -> "✅"
        OptionState.WRONG -> "❌"
        else -> ""
    }

    OutlinedCard(
        onClick = onClick,
        enabled = enabled,
        colors = CardDefaults.outlinedCardColors(
            containerColor = container,
            contentColor = content,
            disabledContainerColor = container,
            disabledContentColor = content
        ),
        border = BorderStroke(2.dp, border),
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(text, style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
            Text(mark)
        }
    }
}

@Composable
private fun FeedbackCard(correct: Boolean, correctAnswer: String, explanation: String) {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.secondaryContainer
        ),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = if (correct) "🎉 Correct!" else "😅 Not quite. The answer is: $correctAnswer",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text("💡 $explanation", style = MaterialTheme.typography.bodyMedium)
        }
    }
}

// ---------- Previews ----------

@Preview(name = "Not answered", showSystemUi = true)
@Composable
private fun QuizNotAnsweredPreview() {
    QuizTheme {
        QuizScreen(
            uiState = QuizUiState(
                category = QuizCategory.SPACE,
                questions = sampleQuestions.take(5),
                currentIndex = 1
            ),
            onOptionClick = {}, onNextClick = {}, onLeave = {}
        )
    }
}

@Preview(name = "Wrong answer", showSystemUi = true)
@Composable
private fun QuizWrongPreview() {
    QuizTheme {
        QuizScreen(
            uiState = QuizUiState(
                category = QuizCategory.SPACE,
                questions = sampleQuestions.take(5),
                currentIndex = 1,
                selectedOption = 2,
                score = 1
            ),
            onOptionClick = {}, onNextClick = {}, onLeave = {}
        )
    }
}
```

### Every important part explained

#### Part 1: The Route decides **where to go** 🧭

```kotlin
        onNextClick = {
            if (uiState.isLastQuestion) {
                onFinished(uiState.score, uiState.total)
            } else {
                viewModel.onEvent(QuizEvent.NextQuestion)
            }
        },
```

- Not the last question → tell the **ViewModel** (next question).
- Last question → tell the **NavHost** (go to results) via `onFinished`.
- The ViewModel stays free of navigation (Chapter 15, Rule 3). ✅
- `onFinished: (score: Int, total: Int) -> Unit` — named inputs in a lambda type, for readability (Chapter 11).

#### Part 2: `BackHandler` + a dialog ❓

```kotlin
    var showLeaveDialog by rememberSaveable { mutableStateOf(false) }

    BackHandler { showLeaveDialog = true }
```

- The phone's **Back** button now **asks first**, instead of leaving (Chapter 13). 🛑
- The ⬅️ in the top bar does the **same**.
- `showLeaveDialog` is **UI-only** state (a dialog is open or not), so it's fine to keep it in the Composable with `rememberSaveable`. Not everything needs to be in the ViewModel! 😊

#### Part 3: `?: return@Scaffold`

```kotlin
        val question = uiState.currentQuestion ?: return@Scaffold
```

- **Elvis + return** (Chapter 12, 13): if there's **no** question (shouldn't happen, but just in case), stop drawing the content.
- After this line, `question` is a normal, **non-null** `Question`. 👍

#### Part 4: The progress bar 📊

```kotlin
            LinearProgressIndicator(
                progress = { uiState.progress },
                modifier = Modifier.fillMaxWidth()
            )
```

- A horizontal bar that fills from **0.0** (empty) to **1.0** (full). Question 2 of 5 → **40%** filled. ▓▓░░░
- `progress = { ... }` is a **lambda** — Compose reads it only when drawing, which is fast. ⚡
- Without `progress`, `LinearProgressIndicator()` shows a **moving** "loading" bar instead (you'll use that in Chapter 19!).

#### Part 5: Deciding how each answer looks 🎨

```kotlin
enum class OptionState { NORMAL, CORRECT, WRONG, FADED }

fun optionState(index: Int, question: Question, selected: Int?): OptionState = when {
    selected == null -> OptionState.NORMAL
    index == question.correctIndex -> OptionState.CORRECT
    index == selected -> OptionState.WRONG
    else -> OptionState.FADED
}
```

| Situation | Look |
|---|---|
| Not answered yet | **NORMAL** — all the same |
| This is the **right** answer | **CORRECT** 🟩 ✅ (shown even if you picked wrong — so you learn!) |
| You picked this, and it's wrong | **WRONG** 🟥 ❌ |
| Any other option | **FADED** — grey, less important |

- A **plain Kotlin function** (not a Composable!) — easy to understand and **test**. 🧪
- `when` checks **in order** — "correct" is checked **before** "selected", so if you picked the right one, it's **green**, not red. 🎯

#### Part 6: `Triple` and destructuring 📦📦📦

```kotlin
    val (container, border, content) = when (state) {
        OptionState.CORRECT -> Triple(CorrectColor, CorrectBorder, Color.Black)
        ...
    }
```

- `Triple(a, b, c)` holds **three** values (like `Pair` from Chapter 4, but three).
- `val (container, border, content) = ...` → take it **apart** into three boxes (destructuring, Chapter 3). ✨
- So `when` can choose **three** colors at once.

#### Part 7: `OutlinedCard` with disabled colors

```kotlin
    OutlinedCard(
        onClick = onClick,
        enabled = enabled,
        colors = CardDefaults.outlinedCardColors(
            containerColor = container,
            contentColor = content,
            disabledContainerColor = container,
            disabledContentColor = content
        ),
        border = BorderStroke(2.dp, border),
        ...
    )
```

- After answering, cards are **disabled** (`enabled = false`) → can't tap again. 🚫
- Normally, disabled cards turn **grey**. We set `disabledContainerColor` / `disabledContentColor` to **our** colors, so green and red **stay visible**. 🟩🟥
- `BorderStroke(2.dp, border)` → a 2 dp colored outline. Import `androidx.compose.foundation.BorderStroke`.

> 🎨 Why fixed green/red with **black** text? Feedback colors should mean the **same** thing in light **and** dark mode, and black on light green/red is always easy to read. ✅

### `ui/result/ResultScreen.kt`

```kotlin
package com.example.quiz.ui.result

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.quiz.data.model.QuizCategory
import com.example.quiz.ui.theme.QuizTheme

data class ResultMessage(val emoji: String, val title: String, val text: String)

fun resultMessageFor(score: Int, total: Int): ResultMessage {
    val percent = if (total == 0) 0 else score * 100 / total
    return when {
        percent == 100 -> ResultMessage("🏆", "Perfect score!", "Wow, you got everything right!")
        percent >= 80 -> ResultMessage("🎉", "Great job!", "You really know this topic.")
        percent >= 50 -> ResultMessage("🙂", "Good work!", "A little more practice and you'll be a star.")
        else -> ResultMessage("💪", "Keep going!", "Every expert was once a beginner. Try again!")
    }
}

@Composable
fun ResultScreen(
    category: QuizCategory,
    score: Int,
    total: Int,
    onPlayAgain: () -> Unit,
    onChooseTopic: () -> Unit,
    modifier: Modifier = Modifier
) {
    val message = resultMessageFor(score, total)
    val stars = "⭐".repeat(score) + "☆".repeat(total - score)

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(message.emoji, fontSize = 96.sp)
        Text(message.title, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
        Text("${category.emoji} ${category.label}", style = MaterialTheme.typography.titleMedium)
        Text(
            text = "$score / $total",
            style = MaterialTheme.typography.displayMedium,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )
        Text(stars, fontSize = 28.sp)
        Text(message.text, style = MaterialTheme.typography.bodyLarge, textAlign = TextAlign.Center)

        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = onPlayAgain, modifier = Modifier.fillMaxWidth()) {
            Text("Play again 🔁")
        }
        OutlinedButton(onClick = onChooseTopic, modifier = Modifier.fillMaxWidth()) {
            Text("Choose another topic")
        }
    }
}

@Preview(showSystemUi = true)
@Composable
private fun ResultScreenPreview() {
    QuizTheme {
        Surface {
            ResultScreen(QuizCategory.ANIMALS, score = 4, total = 5, onPlayAgain = {}, onChooseTopic = {})
        }
    }
}
```

| New idea | Meaning |
|---|---|
| `resultMessageFor(score, total)` | A **plain function** with the rules for the message. Easy to test! 🧪 |
| `score * 100 / total` | Multiply **first**, then divide → `4 * 100 / 5 = 80`. (If you divided first: `4 / 5 = 0` → `0 * 100 = 0`! 😱 Chapter 2's Int division.) |
| `"⭐".repeat(score)` | Repeat a String: `"⭐".repeat(3)` → `"⭐⭐⭐"`. |
| `"☆".repeat(total - score)` | Empty stars for the wrong ones: `⭐⭐⭐⭐☆`. |
| `spacedBy(12.dp, Alignment.CenterVertically)` | Space between items **and** centered (Chapter 6 practice trick). |

> 💡 The Result screen needs **no ViewModel** either: everything it shows comes from the **route** (`score`, `total`, `categoryName`). 🎁

---

## 17.9 Step 7: Connect Everything — `QuizNavHost` 🧭

### `ui/navigation/QuizNavHost.kt`

```kotlin
package com.example.quiz.ui.navigation

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.toRoute
import com.example.quiz.data.QuestionRepository
import com.example.quiz.data.model.QuizCategory
import com.example.quiz.ui.quiz.QuizRoute
import com.example.quiz.ui.result.ResultScreen
import com.example.quiz.ui.start.StartScreen

@Composable
fun QuizNavHost(repository: QuestionRepository) {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = Start) {

        composable<Start> {
            Scaffold { innerPadding ->
                StartScreen(
                    questionCount = { category -> repository.countQuestions(category) },
                    onCategoryClick = { category ->
                        navController.navigate(Quiz(categoryName = category.name))
                    },
                    modifier = Modifier.padding(innerPadding)
                )
            }
        }

        composable<Quiz> { backStackEntry ->
            val route: Quiz = backStackEntry.toRoute()
            QuizRoute(
                onFinished = { score, total ->
                    navController.navigate(
                        Result(categoryName = route.categoryName, score = score, total = total)
                    ) {
                        popUpTo<Quiz> { inclusive = true }
                    }
                },
                onLeave = { navController.popBackStack() }
            )
        }

        composable<Result> { backStackEntry ->
            val route: Result = backStackEntry.toRoute()
            Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                ResultScreen(
                    category = QuizCategory.valueOf(route.categoryName),
                    score = route.score,
                    total = route.total,
                    onPlayAgain = {
                        navController.navigate(Quiz(categoryName = route.categoryName)) {
                            popUpTo<Start> { inclusive = false }
                        }
                    },
                    onChooseTopic = { navController.popBackStack() },
                    modifier = Modifier.padding(innerPadding)
                )
            }
        }
    }
}
```

### Every important part explained

| Code | Meaning |
|---|---|
| `QuizNavHost(repository: QuestionRepository)` | The NavHost **receives** the repository (DI!), only to count questions for the Start screen. |
| `navigate(Quiz(categoryName = category.name))` | `category.name` → `"SPACE"` (enum → text). |
| `popUpTo<Quiz> { inclusive = true }` | **New, shorter form:** `popUpTo<Route>` with the route **type** in `< >`. Removes the finished Quiz → stack is `[Start][Result]`. ✅ |
| Play again: `popUpTo<Start> { inclusive = false }` | Remove everything **above** Start (the Result), then add a new Quiz → `[Start][Quiz]`. A **fresh** ViewModel → a **new** shuffle! 🔀 |
| Choose topic: `popBackStack()` | Result is on top of Start → just pop it → `[Start]`. |
| `Scaffold { innerPadding -> }` around Start and Result | Gives them proper space around the status bar (edge-to-edge, Chapter 11). The Quiz screen has its **own** Scaffold with a top bar. |

> 💡 **Why does Play again give a new shuffle?** Because the old Quiz entry was **removed**, its ViewModel was **cleared** 🧹. The new Quiz entry gets a **brand-new** ViewModel with an empty `SavedStateHandle` → `createStartState()` shuffles again. The lifecycle of ViewModels (Chapter 15) working **for** you! 🎉

### `MainActivity.kt`

```kotlin
package com.example.quiz

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.quiz.ui.navigation.QuizNavHost
import com.example.quiz.ui.theme.QuizTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val repository = (application as QuizApplication).container.questionRepository
        setContent {
            QuizTheme {
                QuizNavHost(repository = repository)
            }
        }
    }
}
```

- `application as QuizApplication` → the Activity can reach the **Application** object directly, and take the repository from the container. 🧰

---

## 17.10 Run It! ▶️ — and Test With the Checklist ✅

### The quiz flow

| Check | ✅? |
|---|---|
| Start screen shows 3 topics, each with "5 questions" | ☐ |
| Tapping a topic opens its quiz; the title shows the emoji and name | ☐ |
| "1 / 5" and the progress bar at 20% | ☐ |
| Tapping an answer: correct → green ✅; wrong → red ❌ **and** the right one green | ☐ |
| Other answers fade; tapping again does **nothing** | ☐ |
| The feedback card shows 🎉/😅 and the 💡 explanation | ☐ |
| "Next ➡️" appears only after answering | ☐ |
| On question 5 the button says "See results 🏁" | ☐ |
| Questions come in a **different order** each new game | ☐ |

### Navigation

| Check | ✅? |
|---|---|
| Back (phone or ⬅️) during a quiz → "Leave the quiz?" dialog | ☐ |
| "Keep playing" closes the dialog; "Leave" goes to Start | ☐ |
| On the Result screen, Back goes to **Start** (not the old quiz) | ☐ |
| "Play again" → a **new**, reshuffled quiz of the same topic | ☐ |
| "Choose another topic" → Start | ☐ |

### Results

| Score | Expected | ✅? |
|---|---|---|
| 5 / 5 | 🏆 Perfect score! ⭐⭐⭐⭐⭐ | ☐ |
| 4 / 5 | 🎉 Great job! ⭐⭐⭐⭐☆ | ☐ |
| 3 / 5 | 🙂 Good work! ⭐⭐⭐☆☆ | ☐ |
| 0 / 5 | 💪 Keep going! ☆☆☆☆☆ | ☐ |

### Survival 🔄💀

| Check | ✅? |
|---|---|
| Rotate on question 3 (answered) → same question, same colors, same score | ☐ |
| Dark mode on/off → same | ☐ |
| Home → `adb shell am kill com.example.quiz` → reopen → same question, same order, same score! 💾 | ☐ |
| Rotate while the "Leave?" dialog is open → the dialog is still open | ☐ |

---

## 17.11 What You Practiced 🎓

| Chapter | Used in the Quiz app |
|---|---|
| 3–4 | Data classes, enums (`valueOf`, `entries`, `name`), sealed interface, `Triple` + destructuring, `mapNotNull`, `shuffled`, `repeat` |
| 6–7 | Layouts, `OutlinedCard` with custom colors, `BorderStroke`, theme colors |
| 8 | Calculated values, hoisting, UI-only state (`showLeaveDialog`) |
| 11 | `Scaffold`, `TopAppBar`, `AlertDialog` |
| 13 | Type-safe routes with data, `popUpTo<T>`, `BackHandler` |
| 14 | Testing rotation and process death |
| 15 | `ViewModel`, `UiState`, events, `SavedStateHandle`, Route + Screen, previews of every state |
| 16 | Repository interface, AppContainer, Application, ViewModel factory, packages |

🎉 **You finished Part 4!** You can now build **multi-screen, well-structured** Android apps. That's a **huge** milestone! 🏔️

---

## 17.12 Challenges 🚀

### Challenge 1: Add a 4th topic ⭐
Add `FOOD("Food", "🍕")` to `QuizCategory` and write 5 questions. What else must change? (Hint: **nothing** — the Start screen loops over `entries`! 😎)

### Challenge 2: Shuffle the answers too ⭐⭐
Shuffle the **4 options** of each question when the quiz starts.
*Hint:* make a new `Question` with `options = shuffledOptions` and `correctIndex = shuffledOptions.indexOf(question.correctAnswer)`. Remember to **save** the order (for process death) — or keep it simple and skip that part.

### Challenge 3: A review list ⭐⭐
On the Result screen, show every question with the user's answer and ✅/❌.
*Hint:* the ViewModel keeps a `List<Int>` of answers; pass a short summary to Result… or (better!) keep finished games in the **repository** and give Result just a **game id**. (Single source of truth! 🏪)

### Challenge 4: A timer ⏱️ ⭐⭐⭐
Give 15 seconds per question. If time runs out, it counts as wrong.
*Hint:* this needs **coroutines** (`delay`, `viewModelScope.launch`) — the topic of **Chapter 18**. Come back to this challenge after it! 😉

### Challenge 5: Best score 🏅 ⭐⭐⭐
Show "Best: 4/5" on each topic card on the Start screen.
*Hint:* this needs data that survives **closing the app** — **DataStore**, in **Chapter 21**. Another one to come back to! 💾

---

## 17.13 What Is Next?

🎉 **Part 4 complete!** Now we enter **Part 5 — Data, Internet, and Saving**. 🌐💾

Throughout the book we said "**Chapter 18**" for `viewModelScope`, `stateIn`, `scope.launch`, `suspend`, `Flow`… Now it's time! In **Chapter 18: Doing Things in the Background — Coroutines and Flow**, you will learn:

- Why long tasks **freeze** the app, and how to avoid it 🥶
- **`suspend`** functions and **coroutines** — doing work **without blocking** ⚡
- `launch`, `delay`, `viewModelScope`, `LaunchedEffect`
- **Dispatchers** — choosing the right "worker" (Main, IO, Default) 👷
- **`Flow`** — streams of values over time 🌊
- `map`, `filter`, `combine`, `stateIn` — fully explained at last!
- Building a **Stopwatch** ⏱️ and a fake "download" with a progress bar

**Fantastic work finishing Chapter 17! 🎉 You built a real, professional, multi-screen app!**
