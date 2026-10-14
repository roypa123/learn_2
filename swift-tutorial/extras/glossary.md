# 📖 Glossary — All New Words in One Place

Every **📖 New word** from the tutorial, in **A–Z** order, with a simple meaning and the chapter where it was first explained.

💡 **Tip:** Use your editor's search (`Ctrl + F` on Windows, `Cmd + F` on Mac) to find a word quickly.

---

## Symbols

| Word | Meaning | Ch |
|---|---|---|
| `$` (binding) | Put before a state property to create a **binding** — a two-way link a control can change: `$name`. | 47 |
| `@main` | Marks where the app **starts**. | 33 |
| `\( )` | **String interpolation**: put a value inside text: `"Hi \(name)"`. | 9 |
| `\.self` | A key path meaning "the item itself". Used in `ForEach(..., id: \.self)`. | 48 |
| `??` | **Nil-coalescing**: use a default if an Optional is empty: `name ?? "Guest"`. | 17 |
| `?.` | **Optional chaining**: do something only if the Optional has a value. | 17 |
| `!` (after a value) | **Force unwrap**: "I'm sure it's not nil." Crashes if it is. | 17 |
| `!` (before a Bool) | **NOT**: flips true ↔ false. | 10 |
| `&&` / `\|\|` | **AND** / **OR**. | 10 |
| `...` / `..<` | **Ranges**: `1...5` includes 5, `1..<5` stops before 5. | 11 |
| `->` | "This function returns…" | 18 |
| `===` | "Are these the **same object**?" (classes). | 21 |
| `#if DEBUG` | Code included only in Debug builds. | 35 |

---

## A

| Word | Meaning | Ch |
|---|---|---|
| **Accessibility** | Making apps usable by everyone, including people with disabilities. ♿ | 42 |
| **Action** | The code that runs when a button is tapped. | 45 |
| **Actor** | A type that lets only one task change its data at a time. | 28 |
| **API** | A set of web addresses a server offers for apps to ask for data. Like a menu. | 58 |
| **API key** | A secret code some APIs need. Keep it secret. | 58 |
| **Append** | Add to the end (of an array). | 14 |
| **Apple ID** | Your free Apple account. | 30 |
| **Archive** | A packaged Release build, ready to upload to the App Store. | 35 |
| **Argument** | The actual value you give when calling a function. | 18 |
| **Array** | An ordered list of values of the same type: `[1, 2, 3]`. | 14 |
| **`as?`** | Try to treat a value as another type; gives `nil` if it can't. | 58 |
| **Assert** | To check that something is true (in tests). | 64 |
| **Asset / Asset Catalog** | Non-code files (images, colors, icons) / the folder that organizes them. | 33, 37 |
| **Associated value** | Extra data attached to one enum case: `case cash(amount: Double)`. | 23 |
| **async / Asynchronous** | Work that takes time and finishes later. | 28 |
| **AsyncImage** | A view that downloads and shows an image from the internet. | 60 |
| **Autocomplete** | The editor suggests code as you type. | 32 |
| **`await`** | Wait for an async result without freezing the app. | 28 |

## B

| Word | Meaning | Ch |
|---|---|---|
| **Baseline** | The invisible line letters sit on. | 43 |
| **Beta** | An unfinished test version. | 31 |
| **Binding** | A two-way connection to someone's state. | 47 |
| **`@Binding`** | A property wrapper for a value another view owns. | 52 |
| **`@Bindable`** | Lets you make `$` bindings from an observable object you received. | 53 |
| **Bool** | A type that is only `true` or `false`. | 7 |
| **`break`** | Stop a loop (or leave a switch). | 11, 12 |
| **Breakpoint** | A marker that pauses the app on a line so you can look inside. | 40 |
| **Bug / Debugging** | A mistake in a program / finding and fixing it. | 1 |
| **Build** | Turning code into an app the device can run. | 32 |
| **Build configuration** | A named set of build settings (Debug, Release…). | 35 |
| **Build number** | An internal number that must increase on every upload. | 36 |
| **Build setting** | One rule for building (like optimization level). | 35 |
| **Bundle Identifier (Bundle ID)** | The app's unique ID, like `com.name.App`. | 33 |

## C

| Word | Meaning | Ch |
|---|---|---|
| **Cache** | A place where downloaded things are kept to reuse later. | 60 |
| **Call** | To use (run) a function: `greet()`. | 4, 18 |
| **Call stack (backtrace)** | The list of functions that led to the current line. | 40 |
| **CancellationError** | Thrown when async work is cancelled. | 62 |
| **Capture** | When a closure remembers a variable from outside. | 19 |
| **Case-sensitive** | Big and small letters are different: `print` ≠ `Print`. | 3 |
| **`case`** | One choice in a `switch` or an enum. | 11, 23 |
| **Certificate** | A digital ID proving you're a registered developer. | 38 |
| **Class** | A type that is shared (reference type) and can inherit. | 21 |
| **Closure** | A block of code without a name that you can store or pass. | 19 |
| **Cloud** | Computers elsewhere that you use over the internet. | 30 |
| **Codable** | A protocol to convert a type to/from JSON. | 59 |
| **Code signing** | A digital stamp proving who made an app. | 38 |
| **Comment** | A note in code for humans; Swift ignores it. | 5 |
| **Comparison** | Checking two values (`>`, `==`…). The answer is a Bool. | 8 |
| **Compiler** | The program that turns Swift into device instructions. | 35 |
| **Compiler directive** | A `#` line for the compiler, like `#if`. | 35 |
| **Component** | Extra software Xcode needs (like Simulators). | 31 |
| **Computed property** | A property that calculates its value each time. | 20 |
| **Concatenation** | Joining strings together. | 9 |
| **Concurrency** | Doing several things at the same time. | 28 |
| **Condition** | The true/false question an `if` checks. | 10 |
| **Conform** | When a type follows a protocol. | 24 |
| **Constant** | A named box whose value can't change (`let`). | 6 |
| **Constraint** | A rule for a generic type: `<T: Comparable>`. | 27 |
| **`continue`** | Skip the rest of this loop round. | 12 |

## D

| Word | Meaning | Ch |
|---|---|---|
| **D-U-N-S number** | A business ID needed for organization developer accounts. | 65 |
| **Data** | Raw bytes. | 58 |
| **Database** | Organized storage for lots of records. | 57 |
| **Debugger** | A tool to pause a running app and look inside. | 40 |
| **Declarative** | Describe *what* you want; the system figures out *how*. | 41 |
| **Decode / Encode** | JSON → Swift value / Swift value → JSON. | 59 |
| **`default`** | The choice when no `case` matches. | 11 |
| **Define** | To make (write) a function. | 18 |
| **`deinit`** | Code that runs when a class object is destroyed. | 21 |
| **Dependency injection** | Giving an object what it needs from outside (good for testing). | 64 |
| **Deployment target** | The oldest iOS your app supports. | 36 |
| **Deprecated** | Still works, but there's a newer recommended way. | 42 |
| **Detent** | A height where a sheet stops when dragged. | 51 |
| **Developer Mode** | An iPhone setting that allows apps from Xcode. | 39 |
| **Dictionary** | A collection of key–value pairs: `["Ravi": 12]`. | 15 |
| **Double** | A number with a decimal point. | 7 |
| **Dynamic Type** | iPhone feature that makes all text bigger/smaller. | 42 |

## E

| Word | Meaning | Ch |
|---|---|---|
| **Editor** | Where you type code. | 3 |
| **Entitlements** | A file listing your app's special permissions. | 38 |
| **Enum** | A type with a fixed list of choices. | 23 |
| **Environment** | Values SwiftUI gives to all views (color scheme, dismiss…). | 49 |
| **Error** | A message that something is wrong (or a thrown error). | 3, 26 |
| **Escape character** | A `\` before a character to give it special meaning: `\n`. | 9 |
| **Exhaustive** | Covering every possible value. | 11 |
| **Explicit / Implicit animation** | Animation with `withAnimation` / with `.animation(_:value:)`. | 55 |
| **Export compliance** | A legal question about encryption when uploading. | 65 |
| **Extension** | Adding features to an existing type. | 25 |

## F – G

| Word | Meaning | Ch |
|---|---|---|
| **Focus** | The field currently receiving typed text. | 47 |
| **Function** | A named block of code that does one job. | 4, 18 |
| **Generic** | Code that works with any type. | 27 |
| **Gesture** | A touch action: tap, swipe, drag, pinch. | 45 |
| **Git** | A tool that remembers every version of your code. | 33 |
| **`guard let`** | Unwrap an Optional or leave early. | 17 |

## H – I

| Word | Meaning | Ch |
|---|---|---|
| **Header** | Extra information sent with a web request. | 58 |
| **Hex code** | A color written as 6 characters: `#FF6B00`. | 54 |
| **HTTP / HTTPS** | The language of the web / its secure version. | 37, 58 |
| **ID (identifier)** | A value that's different for every item. | 48 |
| **`if let`** | Unwrap an Optional if it has a value. | 17 |
| **Imperative** | Writing every step of how to do something. | 41 |
| **Import** | Bring in extra tools: `import SwiftUI`. | 9 |
| **Index** | Position of an item in an array (starts at 0). | 14 |
| **IndexSet** | A set of positions. | 48 |
| **Infinite loop** | A loop that never stops. | 13 |
| **Info.plist** | The app's information card read by iOS. | 37 |
| **Inheritance** | A class taking everything from another class. | 21 |
| **Initializer (`init`)** | Code that runs when an instance is created. | 20 |
| **Instance** | One real value made from a type. | 20 |
| **Instruction** | One small order for the computer. | 1 |
| **Int** | A whole number. | 7 |
| **ISO 8601** | A standard way to write dates as text. | 59 |
| **Iteration** | One round of a loop. | 12 |

## J – L

| Word | Meaning | Ch |
|---|---|---|
| **JSON** | A simple text format for data. | 59 |
| **Key** | The label used to find a value (dictionaries, JSON, Info.plist). | 15, 37 |
| **Keychain** | The Mac/iPhone safe for passwords and certificates. | 38 |
| **Latitude / Longitude** | Two numbers that describe a place on Earth. | 62 |
| **Launch screen** | The simple screen shown while the app starts. | 37 |
| **Lazy** | Creates views only when needed on screen. | 43 |
| **leading / trailing** | Where reading starts / ends (left / right in English). | 42 |
| **Library (package)** | Code from others you can add to your app. | 60 |
| **LLDB** | The debugger engine; you can type commands into it. | 40 |
| **Loop** | Code that repeats. | 12 |

## M

| Word | Meaning | Ch |
|---|---|---|
| **Macro** | A word with `@` or `#` that writes extra code for you. | 53 |
| **`@MainActor`** | Run on the main thread (where the screen updates). | 53 |
| **Markdown** | Simple text styling with symbols like `**bold**`. | 42 |
| **Memory (RAM)** | Fast, temporary storage; cleared when the app closes. | 56 |
| **Memory leak** | Objects that are never removed from memory. | 40 |
| **Method** | A function that belongs to a type. | 9, 20 |
| **Migration** | Upgrading saved data to a new model design. | 57 |
| **Model** | A type that holds data and logic, separate from views. | 53, 57 |
| **Model container / context** | The SwiftData database / your workspace to change it. | 57 |
| **Modifier** | A method that returns a changed view: `.padding()`. | 33, 41 |
| **Mutate / `mutating`** | To change / a method that changes a struct. | 20 |

## N – O

| Word | Meaning | Ch |
|---|---|---|
| **NavigationPath** | The list of screens on a navigation stack. | 49 |
| **`nil`** | Nothing — an empty Optional. | 15, 17 |
| **Object** | An instance of a class. | 21 |
| **Observable** | Something that can be watched for changes. | 53 |
| **Onboarding** | The first screens explaining an app to new users. | 50 |
| **Operating system (OS)** | The main software of a device (iOS, macOS, Windows). | 30 |
| **Operator** | A sign that does something with values: `+`, `==`. | 8 |
| **Optimize** | Make code faster or smaller. | 35 |
| **Optional** | A box that might have a value or be empty: `String?`. | 17 |
| **Organization Identifier** | The first part of a Bundle ID: `com.yourname`. | 33 |
| **Organizer** | Xcode window for archives and crash reports. | 65 |
| **Output** | What a program shows after it runs. | 3 |
| **Override** | Replace a parent class's method. | 21 |

## P

| Word | Meaning | Ch |
|---|---|---|
| **Parameter** | An input box in a function definition. | 18 |
| **Persist / Persistent storage** | To save data / storage that stays after the app closes. | 56 |
| **Pixel / Point** | One tiny dot on a screen / SwiftUI's size unit. | 34, 37 |
| **Placeholder** | Gray hint text in an empty field. | 47 |
| **Platform** | A type of Apple device (iOS, macOS, watchOS…). | 31 |
| **Portrait / Landscape** | Phone standing up / on its side. | 36 |
| **Predicate** | A true/false rule to filter data (`#Predicate`). | 57 |
| **`private` / `private(set)`** | Only usable inside the type / readable outside but changeable only inside. | 27, 29 |
| **Production** | The real version customers use. | 35 |
| **Profile** | Running the app with Instruments to measure speed and memory. | 35 |
| **Program / Programming** | A list of instructions / writing them. | 1 |
| **Programming language** | A clear language for computer instructions. | 1 |
| **Prominent** | Easy to notice. | 45 |
| **Property** | A variable or constant inside a type. | 9, 20 |
| **Property wrapper** | A word like `@State` that adds behavior to a property. | 46 |
| **Protocol** | A list of requirements a type promises to have. | 24 |
| **Provisioning profile** | A permission slip: which app, developer and devices. | 38 |
| **Push / Pop** | Open a new screen / go back. | 49 |

## Q – R

| Word | Meaning | Ch |
|---|---|---|
| **Query** | A question to a database (`@Query`). | 57 |
| **Random** | Picked by chance. | 13 |
| **Range** | Numbers between two ends: `1...10`. | 11 |
| **Raw value** | A fixed value behind each enum case. | 23 |
| **Record** | One saved item in a database. | 57 |
| **Reference / Reference type** | A pointer to a shared object / types that share (classes). | 21 |
| **Refurbished** | A used product, checked and sold again. | 30 |
| **Remote desktop** | Seeing and controlling another computer's screen. | 30 |
| **Request / Response** | The app's question / the server's answer. | 58 |
| **Role** | What kind of action a button does (`.destructive`, `.cancel`). | 45 |
| **Run** | Tell the computer to do the instructions now. | 3 |
| **Run destination** | Where the app runs: a Simulator or real device. | 32 |

## S

| Word | Meaning | Ch |
|---|---|---|
| **Safe area** | The part of the screen not covered by the notch or home bar. | 44 |
| **Scene** | A part of the app's UI the system shows, like a window. | 33 |
| **Scheme** | Instructions for building/running a target. | 36 |
| **Scope** | The area of code where a name can be used. | 18 |
| **Semantic color** | A color named by purpose that adapts to dark mode. | 54 |
| **Server** | A computer on the internet that answers requests. | 58 |
| **Service** | A type whose job is to talk to an API. | 59 |
| **Set** | A collection of unique values with no order. | 16 |
| **ShareLink** | A view that opens the iOS share sheet. | 63 |
| **Simulator** | A pretend iPhone/iPad on your Mac. | 34 |
| **SKU** | A private ID for your app in App Store Connect. | 65 |
| **snake_case** | Words joined with underscores: `first_name`. | 59 |
| **Source of truth** | The one place where a piece of data lives. | 52 |
| **Spacer** | An invisible view that takes all free space. | 43 |
| **Specifier** | A format code like `"%.2f"`. | 46 |
| **Stack** | A container arranging views in one direction. | 43 |
| **State** | Data that changes and affects the screen. | 46 |
| **Step (debugging)** | Running code one small piece at a time while paused. | 40 |
| **String** | Text, inside double quotes. | 4 |
| **String interpolation** | Putting values inside a string with `\( )`. | 9 |
| **Stroke** | Drawing only the outline of a shape. | 44 |
| **Struct** | Your own value type that groups related values. | 20 |
| **Superclass / Subclass** | The parent class / the child class. | 21 |
| **Swift / SwiftUI / SwiftData** | The language / the UI framework / the database framework. | 2, 41, 57 |
| **Swift 6 language mode** | A stricter mode that catches data races. | 36 |

## T

| Word | Meaning | Ch |
|---|---|---|
| **Tab** | One main section of an app, chosen in the tab bar. | 50 |
| **Tag** | The value a Picker option (or tab) represents. | 47 |
| **Target** | One product Xcode builds (app, widget, tests). | 36 |
| **Task** | A unit of async work; `Task { }` starts it. | 28 |
| **`.task` / `.task(id:)`** | Run async work when a view appears / and again when the id changes. | 58, 62 |
| **Team** | The account that owns your apps in Xcode. | 31 |
| **Template** | A ready-made starting point for a project. | 33 |
| **Terminal** | An app where you type text commands. | 31 |
| **Test / Unit test / Test suite / Test target** | Code that checks code / for one small unit / a group of tests / a target with tests. | 64 |
| **TestFlight** | Apple's service for sending test builds to testers. | 38, 65 |
| **Text style** | A named font size like `.title` that supports Dynamic Type. | 42 |
| **`throw` / `throws`** | Report an error / mark a function that can fail. | 26 |
| **Transition** | How a view enters or leaves the screen. | 55 |
| **Trailing closure** | A closure written after the function's brackets. | 19 |
| **Trust (a computer)** | Allow your Mac to talk to your iPhone. | 39 |
| **Tuple** | A small group of values: `(3, "hi")`. | 18 |
| **Type / Type annotation / Type inference** | The kind of a value / writing it yourself / Swift guessing it. | 7 |
| **Type parameter** | A placeholder type like `T` in generics. | 27 |

## U – Z

| Word | Meaning | Ch |
|---|---|---|
| **UI** | User Interface — everything you see and touch. | 2 |
| **UIImage** | UIKit's image type. | 60 |
| **Unwrap** | Open an Optional and take out the value. | 17 |
| **URL** | A web address. | 58 |
| **URLSession** | Apple's class for internet requests. | 58 |
| **Usage description** | The message explaining why your app needs a permission. | 37 |
| **UserDefaults** | Small storage for app settings. | 56 |
| **UUID** | A random unique ID. | 48 |
| **Value / Value type** | What's inside a box / types that copy (structs, Int, String). | 6, 20 |
| **Variable** | A named box whose value can change (`var`). | 6 |
| **Version** | The version users see (1.0, 1.1). | 36 |
| **View** | Anything on screen in SwiftUI. | 33, 41 |
| **`@ViewBuilder`** | Lets a function/property build views with `if`/`switch`. | 61 |
| **ViewModel** | A model made for one screen (MVVM pattern). | 59 |
| **Void** | "Nothing" — a function that returns nothing. | 19 |
| **WMO code** | A number describing weather type. | 62 |

---

🏠 **Home:** [Table of Contents](../README.md) • **Also see:** [Common Errors](common-errors.md)
