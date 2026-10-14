# Chapter 50 — Tabs

🍎 **Needs a Mac** (or iPad Swift Playgrounds)

---

## What you will learn

- `TabView` — the tab bar at the bottom of many apps.
- Adding tabs with icons and titles.
- Two ways to write tabs (older `.tabItem` and newer `Tab`).
- Badges 🔴.
- Switching tabs with code.
- Combining tabs with navigation.
- Page-style swiping (onboarding screens).

---

## 1. What is a tab bar?

Many apps have **buttons at the bottom** to switch between main sections:

```
 ┌──────────────────────────┐
 │                          │
 │     (current screen)     │
 │                          │
 ├──────────────────────────┤
 │  🏠      🔍      👤      │
 │ Home   Search  Profile   │  ← tab bar
 └──────────────────────────┘
```

Examples: the App Store, Music, Phone and Clock apps.

> 📖 **New word: Tab**
> One main section of an app, chosen with a button in the tab bar.

---

## 2. Your first `TabView`

```swift
struct ContentView: View {
    var body: some View {
        TabView {
            Text("🏠 Home screen")
                .tabItem {
                    Label("Home", systemImage: "house.fill")
                }

            Text("🔍 Search screen")
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }

            Text("👤 Profile screen")
                .tabItem {
                    Label("Profile", systemImage: "person.fill")
                }
        }
    }
}
```

**Try it:** Tap each tab at the bottom. The screen changes! ✨

| Part | Meaning |
|---|---|
| `TabView { }` | The container with a tab bar. Each view inside = one tab. |
| `.tabItem { Label(...) }` | The **icon and title** for that tab in the bar. |

💡 **Tip:** Use **3 to 5** tabs. More than 5 and iPhone shows a "More" tab — not great.

---

## 3. The newer `Tab` syntax (iOS 18 and later)

New iOS versions have a cleaner way to write tabs:

```swift
TabView {
    Tab("Home", systemImage: "house.fill") {
        Text("🏠 Home screen")
    }
    Tab("Search", systemImage: "magnifyingglass") {
        Text("🔍 Search screen")
    }
    Tab("Profile", systemImage: "person.fill") {
        Text("👤 Profile screen")
    }
}
```

| Part | Meaning |
|---|---|
| `Tab("Home", systemImage: "house.fill") { ... }` | Title, icon, and the content — all in one place. |

| | `.tabItem { }` (older) | `Tab(...) { }` (newer) |
|---|---|---|
| Works on | iOS 13+ | iOS 18+ |
| Style | modifier on the content | wrapper around the content |

🧠 **Remember:** If your **Minimum Deployment** (Chapter 36) is iOS 18 or newer, use `Tab`. Otherwise use `.tabItem`. Both work the same way for users.

The rest of this chapter uses `.tabItem` so it works on more iOS versions, but you can switch to `Tab` easily.

---

## 4. Each tab as its own view

Real apps put each tab in a **separate view struct**:

```swift
struct ContentView: View {
    var body: some View {
        TabView {
            HomeView()
                .tabItem { Label("Home", systemImage: "house.fill") }

            FavoritesView()
                .tabItem { Label("Favorites", systemImage: "heart.fill") }

            SettingsView()
                .tabItem { Label("Settings", systemImage: "gearshape.fill") }
        }
    }
}

struct HomeView: View {
    var body: some View {
        Text("Welcome home! 🏠").font(.title)
    }
}

struct FavoritesView: View {
    var body: some View {
        Text("Your favorites ❤️").font(.title)
    }
}

struct SettingsView: View {
    var body: some View {
        Text("Settings ⚙️").font(.title)
    }
}
```

💡 **Tip:** Put each tab view in its **own file** (File → New → File → SwiftUI View). Your project stays tidy. 🧹

---

## 5. Tabs with navigation ⭐

Each tab usually has its **own** `NavigationStack`:

```swift
struct ContentView: View {
    var body: some View {
        TabView {
            NavigationStack {
                List(1...20, id: \.self) { n in
                    NavigationLink("Item \(n)") {
                        Text("Details for item \(n)")
                            .navigationTitle("Item \(n)")
                    }
                }
                .navigationTitle("Home")
            }
            .tabItem { Label("Home", systemImage: "house.fill") }

            NavigationStack {
                Text("Settings go here")
                    .navigationTitle("Settings")
            }
            .tabItem { Label("Settings", systemImage: "gearshape.fill") }
        }
    }
}
```

```
 TabView
  ├── NavigationStack  →  Home list → Item details
  └── NavigationStack  →  Settings
```

| Part | Why |
|---|---|
| `NavigationStack` **inside** each tab | Each tab remembers its own screens. Go deep in Home, switch to Settings, come back — you're still deep in Home! |

⚠️ **Careful:** Put `NavigationStack` **inside** each tab — **not** around the `TabView`. Otherwise the tab bar disappears when you navigate, or titles act strangely.

---

## 6. Badges 🔴

Show a small number or text on a tab:

```swift
TabView {
    Text("Inbox")
        .tabItem { Label("Inbox", systemImage: "tray.fill") }
        .badge(3)

    Text("Updates")
        .tabItem { Label("Updates", systemImage: "bell.fill") }
        .badge("New")
}
```

| Modifier | Shows |
|---|---|
| `.badge(3)` | A red circle with **3**. (`.badge(0)` shows nothing.) |
| `.badge("New")` | A red label with text. |

With the newer syntax: `Tab("Inbox", systemImage: "tray.fill") { ... }.badge(3)`.

---

## 7. Changing tabs with code

Sometimes a button should **switch** tabs. Give each tab a **tag** and bind the selection:

```swift
enum AppTab {
    case home, cart, profile
}

struct ContentView: View {
    @State private var selectedTab: AppTab = .home
    @State private var cartCount = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            VStack(spacing: 20) {
                Text("🛍️ Shop").font(.largeTitle)
                Button("Add to cart") {
                    cartCount += 1
                }
                .buttonStyle(.bordered)
                Button("Go to cart →") {
                    selectedTab = .cart
                }
                .buttonStyle(.borderedProminent)
            }
            .tabItem { Label("Home", systemImage: "house.fill") }
            .tag(AppTab.home)

            Text("🛒 \(cartCount) items in your cart")
                .font(.title)
                .tabItem { Label("Cart", systemImage: "cart.fill") }
                .badge(cartCount)
                .tag(AppTab.cart)

            Text("👤 Profile")
                .tabItem { Label("Profile", systemImage: "person.fill") }
                .tag(AppTab.profile)
        }
    }
}
```

| Part | Meaning |
|---|---|
| `enum AppTab` | The list of tabs — no typos possible (Chapter 23). |
| `@State private var selectedTab` | Which tab is showing. |
| `TabView(selection: $selectedTab)` | Bind the tab view to it. |
| `.tag(AppTab.cart)` | "This tab's value is `.cart`." |
| `selectedTab = .cart` | Switch to the Cart tab! |

With the newer syntax: `Tab("Cart", systemImage: "cart.fill", value: AppTab.cart) { ... }` — the `value:` replaces `.tag`.

---

## 8. Tab bar color

```swift
TabView { ... }
    .tint(.orange)
```

`.tint` sets the color of the **selected** tab icon and title.

---

## 9. Page style: swipe between screens 👆

`TabView` can also make **swipeable pages** — great for **onboarding** (the welcome screens new users see).

```swift
struct ContentView: View {
    var body: some View {
        TabView {
            OnboardingPage(emoji: "👋", title: "Welcome!", text: "Thanks for downloading our app.")
            OnboardingPage(emoji: "📸", title: "Take photos", text: "Capture your best moments.")
            OnboardingPage(emoji: "🚀", title: "Get started", text: "Let's go!")
        }
        .tabViewStyle(.page)
        .indexViewStyle(.page(backgroundDisplayMode: .always))
    }
}

struct OnboardingPage: View {
    let emoji: String
    let title: String
    let text: String

    var body: some View {
        VStack(spacing: 20) {
            Text(emoji).font(.system(size: 100))
            Text(title).font(.largeTitle.bold())
            Text(text)
                .font(.title3)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal)
        }
    }
}
```

| Part | Meaning |
|---|---|
| `.tabViewStyle(.page)` | No tab bar — swipe left/right between pages. Dots show at the bottom. |
| `.indexViewStyle(.page(backgroundDisplayMode: .always))` | Show a background behind the dots so they're visible on any color. |

> 📖 **New word: Onboarding**
> The first screens a new user sees, explaining the app.

---

## 10. Mini project: a small app with 3 tabs 📱

```swift
struct ContentView: View {
    @State private var favorites: [String] = []

    var body: some View {
        TabView {
            NavigationStack {
                ExploreView(favorites: $favorites)
            }
            .tabItem { Label("Explore", systemImage: "safari.fill") }

            NavigationStack {
                FavoritesListView(favorites: favorites)
            }
            .tabItem { Label("Favorites", systemImage: "heart.fill") }
            .badge(favorites.count)

            NavigationStack {
                Text("Version 1.0 ✨")
                    .navigationTitle("About")
            }
            .tabItem { Label("About", systemImage: "info.circle.fill") }
        }
        .tint(.pink)
    }
}

struct ExploreView: View {
    @Binding var favorites: [String]
    let places = ["🗼 Paris", "🗽 New York", "🏯 Kyoto", "🕌 Agra", "🏝️ Maldives"]

    var body: some View {
        List(places, id: \.self) { place in
            HStack {
                Text(place)
                Spacer()
                Button {
                    if favorites.contains(place) {
                        favorites.removeAll { $0 == place }
                    } else {
                        favorites.append(place)
                    }
                } label: {
                    Image(systemName: favorites.contains(place) ? "heart.fill" : "heart")
                        .foregroundStyle(.pink)
                }
                .buttonStyle(.borderless)
            }
        }
        .navigationTitle("Explore")
    }
}

struct FavoritesListView: View {
    let favorites: [String]

    var body: some View {
        List(favorites, id: \.self) { place in
            Text(place)
        }
        .navigationTitle("Favorites")
        .overlay {
            if favorites.isEmpty {
                ContentUnavailableView("No favorites yet",
                                       systemImage: "heart",
                                       description: Text("Tap ♡ on a place to save it."))
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `@State private var favorites` in `ContentView` | The **shared** list lives in the parent. |
| `ExploreView(favorites: $favorites)` | Pass a **binding** so Explore can **change** it. (`@Binding` — Chapter 52.) |
| `FavoritesListView(favorites: favorites)` | Pass the value — Favorites only **reads** it. |
| `.badge(favorites.count)` | The badge updates automatically. |
| `.buttonStyle(.borderless)` | Inside a List row, this makes only the heart tappable (not the whole row). |

Tap ♡ in Explore → the badge on Favorites goes up → open Favorites → the place is there! 🎉

---

## 🏋️ Practice

1. Make a `TabView` with 4 tabs: Home, Search, Messages, Profile — each with an SF Symbol.
2. Rewrite it using the newer `Tab` syntax (if your Xcode supports it).
3. Add a badge with the number 5 on Messages.
4. Put a `NavigationStack` with a list inside the Home tab.
5. Add a button on Home that switches to the Profile tab with code.
6. Make 3 onboarding pages with `.tabViewStyle(.page)`.

---

## 🧠 Remember

- `TabView { }` + `.tabItem { Label(...) }` (or `Tab(...) { }` on iOS 18+) makes a tab bar.
- Use 3–5 tabs. Put each tab in its own view (and file).
- Put a `NavigationStack` **inside** each tab.
- `.badge(n)` shows a red number.
- `TabView(selection: $tab)` + `.tag(value)` → switch tabs with code.
- `.tabViewStyle(.page)` → swipeable pages.

---

⬅️ **Back:** [Chapter 49 — Navigation](49-navigation.md)
➡️ **Next:** [Chapter 51 — Sheets and Alerts](51-sheets-alerts.md)
