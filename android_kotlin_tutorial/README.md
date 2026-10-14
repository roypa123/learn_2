# Android App Development with Kotlin — A Beginner's Book 📱

Welcome! 👋
This book teaches you how to make **Android apps** with **Kotlin** and **Jetpack Compose**, step by step.

- ✅ For **complete beginners** — no coding knowledge needed
- ✅ **Simple English** — easy to read even if English is not your first language
- ✅ **Every line of code is explained**
- ✅ **Small examples** and **practice tasks with answers** in every chapter
- ✅ Uses the **modern way** Android apps are made today (Kotlin + Jetpack Compose)

---

## How to Use This Book

1. Read the chapters **in order**. Each chapter uses things from the chapters before it.
2. **Type every example yourself.** Don't just copy and paste. Your fingers learn too! ⌨️
3. Do the **Practice Time** tasks at the end of each chapter **before** you look at the answers.
4. If something is hard, **read it again slowly**. That is normal. Every developer did this.
5. Take breaks. ☕ One chapter per day is a good speed.

---

## How Many Chapters?

There are **28 chapters**, in **7 parts**.

**Status:** ✅ = ready to read  ⏳ = coming soon

### Part 1 — Getting Started 🚀

| # | Chapter | What you will learn | Status |
|---|---|---|---|
| 1 | [Getting Ready — Install Android Studio and Make Your First App](chapter01_setup.md) | Install Android Studio, make a project, every file and line explained, run on emulator and real phone | ✅ |

### Part 2 — The Kotlin Language 🗣️

| # | Chapter | What you will learn | Status |
|---|---|---|---|
| 2 | [Kotlin Basics — Talking to the Computer](chapter02_kotlin_basics.md) | Variables, types, math, Strings, `if`, `when`, loops, functions | ✅ |
| 3 | [Kotlin Next Steps — Nulls, Lists, Classes, and Lambdas](chapter03_kotlin_next_steps.md) | Null safety (`?`, `?.`, `?:`), Lists, Maps, Sets, classes, objects, data classes, lambdas | ✅ |
| 4 | [Kotlin Power Tools — Inheritance, Enums, Sealed Classes, and More](chapter04_kotlin_power_tools.md) | Inheritance, interfaces, enums, sealed classes, `object`, companion object, extension functions, scope functions (`let`, `apply`, `also`, `run`, `with`), generics | ✅ |

### Part 3 — Building Screens With Jetpack Compose 🎨

| # | Chapter | What you will learn | Status |
|---|---|---|---|
| 5 | [Your First Compose Screen — Text, Images, Buttons, and Modifiers](chapter05_first_compose_screen.md) | Composable functions, `Text`, `Image`, `Button`, `Icon`, Preview, Modifiers, Profile Card screen | ✅ |
| 6 | [Layouts — Putting Things in Place](chapter06_layouts.md) | `Column`, `Row`, `Box`, `Spacer`, alignment, arrangement, padding, size, weight, scrolling, Weather screen | ✅ |
| 7 | [Making It Beautiful — Material 3](chapter07_material3.md) | Themes, colors, color roles, dynamic color, dark mode, fonts, shapes, `Surface`, `Card`, Plant Shop screen | ✅ |
| 8 | [State — Making Screens Change](chapter08_state.md) | `remember`, `mutableStateOf`, recomposition, `rememberSaveable`, state hoisting, Coffee Order app | ✅ |
| 9 | [Getting Input From the User](chapter09_user_input.md) | `TextField`, keyboards, passwords, validation, `Checkbox`, `RadioButton`, `Switch`, `Slider`, chips, dropdowns, Sign-Up form | ✅ |
| 10 | [Lists and Grids](chapter10_lists_and_grids.md) | `LazyColumn`, `LazyRow`, `LazyVerticalGrid`, items, keys, sticky headers, scroll control, Contacts app | ✅ |
| 11 | Screen Frames and Pop-ups | `Scaffold`, `TopAppBar`, bottom bar, floating button, `Snackbar`, dialogs, bottom sheets | ⏳ |
| 12 | 🛠️ Mini Project: Tip Calculator App | Build a full small app using Parts 1–3 | ⏳ |

### Part 4 — Many Screens and App Structure 🏗️

| # | Chapter | What you will learn | Status |
|---|---|---|---|
| 13 | Moving Between Screens — Navigation | Navigation Compose, routes, passing data, back button, bottom navigation | ⏳ |
| 14 | The Life of an App — Activity Lifecycle | `onCreate`, `onStart`, `onResume`…, screen rotation, saving state | ⏳ |
| 15 | ViewModel — The Screen's Brain | `ViewModel`, why we need it, `UiState`, `StateFlow` | ⏳ |
| 16 | Clean App Structure — MVVM | Layers (UI, ViewModel, Repository, Data), one-way data flow | ⏳ |
| 17 | 🛠️ Mini Project: Quiz App | Build a quiz app with many screens and a ViewModel | ⏳ |

### Part 5 — Data, Internet, and Saving 🌐💾

| # | Chapter | What you will learn | Status |
|---|---|---|---|
| 18 | Doing Things in the Background — Coroutines and Flow | `suspend`, `launch`, `viewModelScope`, `Flow`, `collectAsState` | ⏳ |
| 19 | Getting Data From the Internet | Internet permission, Retrofit, JSON with kotlinx.serialization, loading and error states | ⏳ |
| 20 | Showing Pictures From the Internet | Coil, `AsyncImage`, placeholders, caching | ⏳ |
| 21 | Saving Small Settings — DataStore | Preferences DataStore, saving dark mode, user name, etc. | ⏳ |
| 22 | Saving Lots of Data — Room Database | Entities, DAO, database, queries, Room + Flow | ⏳ |
| 23 | Connecting the Pieces — Dependency Injection with Hilt | What DI is, Hilt setup, `@Inject`, modules, `hiltViewModel()` | ⏳ |
| 24 | 🛠️ Mini Project: Notes App | Full app with Room, ViewModel, Navigation, and Hilt | ⏳ |

### Part 6 — Phone Features and Polish ✨

| # | Chapter | What you will learn | Status |
|---|---|---|---|
| 25 | Using Phone Features | Permissions, camera, photo picker, location, notifications, WorkManager | ⏳ |
| 26 | Animations | `AnimatedVisibility`, `animate*AsState`, `Crossfade`, transitions | ⏳ |

### Part 7 — Testing and Sharing Your App 🏁

| # | Chapter | What you will learn | Status |
|---|---|---|---|
| 27 | Testing and Debugging | Logcat, breakpoints, unit tests, Compose UI tests, finding crashes | ⏳ |
| 28 | Publishing Your App on Google Play | App icon, signing, release build, App Bundle, Play Console, store listing | ⏳ |

---

## What You Need

- A computer with **Windows**, **macOS**, or **Linux** (this book shows Windows steps)
- At least **8 GB RAM** (16 GB is better)
- **Internet** for downloads
- An **Android phone** (optional, but nice for testing)
- **Patience and curiosity** 😊

---

## Folder Contents

```
android_kotlin_tutorial/
 ├── README.md                     ← you are here
 ├── chapter01_setup.md
 ├── chapter02_kotlin_basics.md
 ├── chapter03_kotlin_next_steps.md
 ├── chapter04_kotlin_power_tools.md
 ├── chapter05_first_compose_screen.md
 ├── chapter06_layouts.md
 ├── chapter07_material3.md
 ├── chapter08_state.md
 ├── chapter09_user_input.md
 ├── chapter10_lists_and_grids.md
 └── ... (more chapters coming)
```

**Happy learning! 🎉**
