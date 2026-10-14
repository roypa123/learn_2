# Chapter 29 — Mini Project: Text Adventure Game 🏰

✅ **Works in browser** — use https://swiftfiddle.com

---

## What you will build

A small **text adventure game**. The hero explores a castle, picks up items, opens a locked door, and finds the treasure! 💎

We will use **everything** from Parts 2 and 3:

| Feature | Where we use it |
|---|---|
| `enum` + raw values + `CaseIterable` | Directions and items |
| `enum` with associated values | Player commands |
| `struct` | Rooms |
| `class` | The game (shared state) |
| `protocol` + `extension` | Things that can be described |
| Dictionaries, Sets, Arrays | Map, inventory, command list |
| Optionals | "Is there a door that way?" |
| `throws` / `catch` | Invalid moves |
| Closures | Parsing and filtering |

We build it **step by step**. At each step, you can run the code and see it work.

💡 **Tip:** SwiftFiddle can't read keyboard input easily, so the player's commands will come from an **array of strings**. It's like the player typed them in advance. In a real app, they'd come from a text field or buttons.

---

## Step 1: Directions

```swift
enum Direction: String, CaseIterable {
    case north, south, east, west
}
```

| Part | Meaning |
|---|---|
| `enum Direction` | Only 4 possible directions. No typos. |
| `: String` | Each case has a String raw value (`"north"`, etc.). We'll use this to read commands like `"go north"`. |
| `CaseIterable` | Gives us `Direction.allCases` — handy for listing exits. |

Test it:

```swift
print(Direction(rawValue: "east") ?? "unknown")   // east
print(Direction(rawValue: "up") == nil)          // true — "up" is not a direction
```

---

## Step 2: Items

```swift
enum Item: String, CaseIterable {
    case key, torch, sword, treasure

    var emoji: String {
        switch self {
        case .key: "🔑"
        case .torch: "🔦"
        case .sword: "🗡️"
        case .treasure: "💎"
        }
    }
}
```

| Part | Meaning |
|---|---|
| `case key, torch, sword, treasure` | The four items in our game. |
| `var emoji` | A computed property. Each item gets a picture. |

---

## Step 3: A protocol for describing things

```swift
protocol Describable {
    var name: String { get }
    var details: String { get }
}

extension Describable {
    func describe() -> String {
        "📍 \(name)\n   \(details)"
    }
}
```

| Part | Meaning |
|---|---|
| `protocol Describable` | Anything with a `name` and `details`. |
| `extension Describable` | Everyone who follows it gets `describe()` for free. |
| `\n` | New line. `"   "` = a little indent. |

---

## Step 4: Rooms

```swift
struct Room: Describable {
    let name: String
    let details: String
    var exits: [Direction: String]     // direction → name of the next room
    var items: Set<Item>
    var lockedExit: Direction? = nil   // an exit that needs the key
}
```

| Part | Meaning |
|---|---|
| `struct Room: Describable` | A room follows `Describable` because it has `name` and `details`. |
| `exits: [Direction: String]` | A **dictionary**. Example: `[.north: "Hall"]` = "go north to reach the Hall". |
| `items: Set<Item>` | A **set** of items lying in the room. No duplicates. |
| `lockedExit: Direction?` | An **Optional**. Most rooms have no locked exit (`nil`). |

Test it:

```swift
let test = Room(name: "Test Room", details: "Just a test.", exits: [.north: "Hall"], items: [.key])
print(test.describe())
```

**Output:**

```
📍 Test Room
   Just a test.
```

---

## Step 5: Commands

```swift
enum Command {
    case go(Direction)
    case take(Item)
    case look
    case inventory
    case unknown(String)
}
```

Each command can carry **different data** (associated values):

| Command | Carries |
|---|---|
| `.go(.north)` | a direction |
| `.take(.key)` | an item |
| `.look` | nothing |
| `.inventory` | nothing |
| `.unknown("dance")` | the text we didn't understand |

### Turning text into a command

```swift
extension Command {
    init(text: String) {
        let words = text.lowercased().split(separator: " ").map { String($0) }

        guard let verb = words.first else {
            self = .unknown(text)
            return
        }
        let noun = words.count > 1 ? words[1] : ""

        switch verb {
        case "go":
            if let dir = Direction(rawValue: noun) {
                self = .go(dir)
            } else {
                self = .unknown(text)
            }
        case "take":
            if let item = Item(rawValue: noun) {
                self = .take(item)
            } else {
                self = .unknown(text)
            }
        case "look":
            self = .look
        case "inventory", "inv":
            self = .inventory
        default:
            self = .unknown(text)
        }
    }
}
```

Line by line:

| Line | Meaning |
|---|---|
| `extension Command { init(text:) }` | A new way to create a `Command` from text. |
| `text.lowercased()` | `"Go NORTH"` → `"go north"`. |
| `.split(separator: " ")` | Cut at spaces → `["go", "north"]`. |
| `.map { String($0) }` | `split` gives pieces of text called `Substring`. We turn each into a normal `String`. |
| `guard let verb = words.first else {...}` | If the text was empty, it's unknown. |
| `let noun = words.count > 1 ? words[1] : ""` | The second word, or `""` if there isn't one. |
| `switch verb` | Decide what kind of command it is. |
| `Direction(rawValue: noun)` | Turn `"north"` into `.north`. Gives `nil` for a bad direction. |
| `self = .go(dir)` | In an enum `init`, we set `self` to a case. |
| `case "inventory", "inv"` | Two words mean the same command. |

Test it:

```swift
print(Command(text: "go north"))
print(Command(text: "TAKE key"))
print(Command(text: "fly away"))
```

**Output** (something like):

```
go(Direction.north)
take(Item.key)
unknown("fly away")
```

(Some versions add a module name, like `go(main.Direction.north)`. That's fine.)

---

## Step 6: Game errors

```swift
enum GameError: Error, CustomStringConvertible {
    case noExit(Direction)
    case doorLocked
    case itemNotHere(Item)

    var description: String {
        switch self {
        case .noExit(let dir): "You can't go \(dir.rawValue). There's a wall. 🧱"
        case .doorLocked: "The door is locked. 🔒 You need a key."
        case .itemNotHere(let item): "There is no \(item.rawValue) here."
        }
    }
}
```

| Part | Meaning |
|---|---|
| `: Error` | Can be thrown. |
| `CustomStringConvertible` | Gives a friendly message when printed. |
| Associated values | `noExit` remembers **which** direction. `itemNotHere` remembers **which** item. |

---

## Step 7: The game (a class)

We use a **class** here, because the game's state (where the player is, what they carry) is **one shared thing** that changes over time.

```swift
final class Game {
    private var rooms: [String: Room]
    private var currentRoomName: String
    private var inventory: Set<Item> = []
    private(set) var isWon = false
    private(set) var moves = 0

    init() {
        rooms = [
            "Gate": Room(
                name: "Gate",
                details: "A huge castle gate. The air is cold.",
                exits: [.north: "Hall"],
                items: [.torch]
            ),
            "Hall": Room(
                name: "Hall",
                details: "A big hall with old paintings. Doors lead everywhere.",
                exits: [.south: "Gate", .east: "Kitchen", .west: "Armory", .north: "Treasury"],
                items: [],
                lockedExit: .north
            ),
            "Kitchen": Room(
                name: "Kitchen",
                details: "Smells like old soup. Something shiny is under the table.",
                exits: [.west: "Hall"],
                items: [.key]
            ),
            "Armory": Room(
                name: "Armory",
                details: "Shields and swords hang on the walls.",
                exits: [.east: "Hall"],
                items: [.sword]
            ),
            "Treasury": Room(
                name: "Treasury",
                details: "Gold everywhere! A glowing chest sits in the middle.",
                exits: [.south: "Hall"],
                items: [.treasure]
            )
        ]
        currentRoomName = "Gate"
    }

    private var currentRoom: Room {
        rooms[currentRoomName]!
    }
}
```

| Part | Meaning |
|---|---|
| `final class Game` | A class nobody inherits from. |
| `private var rooms` | The map: room name → room. `private` = only `Game` can touch it. |
| `currentRoomName` | Where the player is now. |
| `inventory: Set<Item>` | What the player carries. Starts empty. |
| `private(set) var isWon` | **Anyone can read** it, but **only `Game` can change** it. |
| `init()` | Build the castle map. |
| `lockedExit: .north` | In the Hall, the north door is locked. |
| `rooms[currentRoomName]!` | We use `!` because we control the map and know the room exists. (One of the rare safe uses!) |

> 📖 **New word: private(set)**
> "Everyone can **read** this, but only code inside the type can **change** it."

Here is our castle map:

```
              ┌──────────┐
              │ Treasury │ 💎
              └────┬─────┘
                   │ (locked 🔒)
┌────────┐    ┌────┴────┐    ┌─────────┐
│ Armory │────│  Hall   │────│ Kitchen │
│   🗡️   │    │         │    │   🔑    │
└────────┘    └────┬────┘    └─────────┘
                   │
              ┌────┴────┐
              │  Gate   │ 🔦  ← start
              └─────────┘
```

---

## Step 8: Game actions

Add these methods **inside** the `Game` class (or in an extension — let's use an extension to keep it tidy):

```swift
extension Game {
    func look() -> String {
        let room = currentRoom
        var text = room.describe()

        let exitNames = Direction.allCases
            .filter { room.exits[$0] != nil }
            .map { $0.rawValue }
        text += "\n   Exits: \(exitNames.joined(separator: ", "))"

        if !room.items.isEmpty {
            let itemList = room.items
                .sorted { $0.rawValue < $1.rawValue }
                .map { "\($0.emoji) \($0.rawValue)" }
            text += "\n   You see: \(itemList.joined(separator: ", "))"
        }
        return text
    }

    func go(_ direction: Direction) throws -> String {
        guard let nextName = currentRoom.exits[direction] else {
            throw GameError.noExit(direction)
        }
        if currentRoom.lockedExit == direction {
            guard inventory.contains(.key) else {
                throw GameError.doorLocked
            }
            rooms[currentRoomName]?.lockedExit = nil
            print("🔓 You unlock the door with the key!")
        }
        currentRoomName = nextName
        moves += 1
        return look()
    }

    func take(_ item: Item) throws -> String {
        guard currentRoom.items.contains(item) else {
            throw GameError.itemNotHere(item)
        }
        rooms[currentRoomName]?.items.remove(item)
        inventory.insert(item)

        if item == .treasure {
            isWon = true
        }
        return "You take the \(item.emoji) \(item.rawValue)."
    }

    func showInventory() -> String {
        if inventory.isEmpty {
            return "🎒 Your bag is empty."
        }
        let list = inventory
            .sorted { $0.rawValue < $1.rawValue }
            .map { "\($0.emoji) \($0.rawValue)" }
        return "🎒 You carry: \(list.joined(separator: ", "))"
    }
}
```

Let's explain the important parts:

### `look()`

| Line | Meaning |
|---|---|
| `Direction.allCases.filter { room.exits[$0] != nil }` | Keep only the directions that have an exit. |
| `.map { $0.rawValue }` | Turn them into text: `["north", "south"]`. |
| `.joined(separator: ", ")` | Join an array of strings into one: `"north, south"`. |
| `room.items.sorted { ... }` | Sets have no order, so we sort them to always show the same order. |

### `go(_:)`

| Line | Meaning |
|---|---|
| `func go(...) throws -> String` | Can fail (wall or locked door). |
| `guard let nextName = currentRoom.exits[direction] else { throw ... }` | No exit that way? Throw `noExit`. |
| `if currentRoom.lockedExit == direction` | Is this the locked door? |
| `guard inventory.contains(.key) else { throw ... }` | No key? Throw `doorLocked`. |
| `rooms[currentRoomName]?.lockedExit = nil` | Unlock it for good. `?.` because the dictionary gives an Optional. |
| `currentRoomName = nextName` | Move the player. |

### `take(_:)`

| Line | Meaning |
|---|---|
| `guard currentRoom.items.contains(item)` | Is the item really here? |
| `rooms[currentRoomName]?.items.remove(item)` | Remove it from the room. |
| `inventory.insert(item)` | Put it in the bag. |
| `if item == .treasure { isWon = true }` | You win! 🏆 |

---

## Step 9: Running a command

```swift
extension Game {
    func run(_ text: String) {
        print("\n> \(text)")
        let command = Command(text: text)

        do {
            switch command {
            case .go(let direction):
                print(try go(direction))
            case .take(let item):
                print(try take(item))
            case .look:
                print(look())
            case .inventory:
                print(showInventory())
            case .unknown(let words):
                print("🤔 I don't understand \"\(words)\". Try: go, take, look, inventory.")
            }
        } catch {
            print("⚠️ \(error)")
        }
    }
}
```

| Part | Meaning |
|---|---|
| `print("\n> \(text)")` | Show what the player "typed", with an empty line before it. |
| `Command(text: text)` | Turn text into a `Command` (Step 5). |
| `switch command` | Do the right action. No `default` needed — all cases covered! |
| `case .go(let direction)` | Take the direction out of the command. |
| `try go(direction)` | Might throw. |
| `catch { print("⚠️ \(error)") }` | Show the friendly error message (from `CustomStringConvertible`). |

---

## Step 10: Play! 🎮

```swift
let game = Game()

print("🏰 Welcome to the Castle Adventure!")
print(game.look())

let commands = [
    "take torch",
    "go north",
    "go north",
    "go east",
    "look",
    "take key",
    "take sword",
    "go west",
    "go west",
    "take sword",
    "inv",
    "go east",
    "dance",
    "go north",
    "take treasure"
]

for command in commands {
    game.run(command)
    if game.isWon {
        break
    }
}

if game.isWon {
    print("\n🏆 YOU WIN! You found the treasure in \(game.moves) moves!")
} else {
    print("\nThe adventure continues...")
}
```

| Part | Meaning |
|---|---|
| `let game = Game()` | Create the game. |
| `commands` | The player's "typed" commands, in order. |
| `for command in commands` | Run each one. |
| `if game.isWon { break }` | Stop early if the player wins. |

**Output:**

```
🏰 Welcome to the Castle Adventure!
📍 Gate
   A huge castle gate. The air is cold.
   Exits: north
   You see: 🔦 torch

> take torch
You take the 🔦 torch.

> go north
📍 Hall
   A big hall with old paintings. Doors lead everywhere.
   Exits: north, south, east, west

> go north
⚠️ The door is locked. 🔒 You need a key.

> go east
📍 Kitchen
   Smells like old soup. Something shiny is under the table.
   Exits: west
   You see: 🔑 key

> look
📍 Kitchen
   Smells like old soup. Something shiny is under the table.
   Exits: west
   You see: 🔑 key

> take key
You take the 🔑 key.

> take sword
⚠️ There is no sword here.

> go west
📍 Hall
   A big hall with old paintings. Doors lead everywhere.
   Exits: north, south, east, west

> go west
📍 Armory
   Shields and swords hang on the walls.
   Exits: east
   You see: 🗡️ sword

> take sword
You take the 🗡️ sword.

> inv
🎒 You carry: 🔑 key, 🗡️ sword, 🔦 torch

> go east
📍 Hall
   A big hall with old paintings. Doors lead everywhere.
   Exits: north, south, east, west

> dance
🤔 I don't understand "dance". Try: go, take, look, inventory.

> go north
🔓 You unlock the door with the key!
📍 Treasury
   Gold everywhere! A glowing chest sits in the middle.
   Exits: south
   You see: 💎 treasure

> take treasure
You take the 💎 treasure.

🏆 YOU WIN! You found the treasure in 6 moves!
```

🎉 **Congratulations!** You built a real game using structs, classes, enums, protocols, extensions, optionals, errors and closures!

---

## Step 11: How to run the full game

Put **all the code** from Steps 1–10 into SwiftFiddle **in this order**:

1. `enum Direction`
2. `enum Item`
3. `protocol Describable` + its `extension`
4. `struct Room`
5. `enum Command` + its `extension` (the `init(text:)`)
6. `enum GameError`
7. `final class Game` (with `init` and `currentRoom`)
8. `extension Game` with `look`, `go`, `take`, `showInventory`
9. `extension Game` with `run`
10. The "Play!" code

Skip the small "Test it" snippets — they were just for checking each step.

---

## 🏋️ Challenges (make it your own!)

Try these one by one. There are no answers — be creative! 🎨

1. **New room:** Add a `"Garden"` east of the Gate with a `.flower` item. (Add `flower` to `Item` too, and give it an emoji.)
2. **Drop command:** Add `case drop(Item)` to `Command`. Remove the item from the inventory and add it to the current room.
3. **Dark room:** Make the Armory dark. If the player doesn't have the `.torch`, `look()` should say `"It's too dark to see! 🌑"`.
4. **Monster:** Put a dragon 🐉 in the Treasury. The player can only take the treasure if they have the `.sword`. Throw a new `GameError.dragonBlocks` otherwise.
5. **Help command:** Add `case help` that lists all commands.
6. **Short directions:** Let the player type `"n"`, `"s"`, `"e"`, `"w"` as well as `"go north"` and so on.

---

## 🧠 What you practiced

- `enum` with raw values, `CaseIterable`, computed properties and associated values.
- `struct` for simple data (`Room`).
- `class` for shared, changing state (`Game`).
- `protocol` + `extension` for shared behavior (`Describable`).
- `Dictionary`, `Set`, `Array` together.
- `Optional` (`lockedExit`, `rawValue` inits).
- `throws` / `do` / `catch` with friendly messages.
- Closures: `filter`, `map`, `sorted`, `joined`.
- `private` and `private(set)` to protect data.

---

## 🎉 Part 3 complete!

You can now **design your own types** — that's how real apps are built.

**Parts 1–3 are all of Swift you need to start building apps.** 🏆

Next is **Part 4**: getting access to a Mac, installing **Xcode**, and learning every important Xcode setting. After that, **SwiftUI** — where you'll build real iPhone screens!

---

⬅️ **Back:** [Chapter 28 — `async` and `await`](28-async-await.md)
➡️ **Next:** Chapter 30 — Options When You Don't Own a Mac *(coming soon)*
