# Chapter 60 — Showing Images From the Internet

🍎 **Needs a Mac** (and internet)

---

## What you will learn

- `AsyncImage` — load an image from a URL with one line.
- Showing a **placeholder** while loading.
- Handling **errors** (broken images).
- Resizing and styling downloaded images.
- Images in **lists** and **grids**.
- Caching (a short explanation).
- Letting the user **pick photos** with `PhotosPicker`.

---

## 1. `AsyncImage` — the simplest way

```swift
struct ContentView: View {
    var body: some View {
        AsyncImage(url: URL(string: "https://picsum.photos/300"))
    }
}
```

**Run it:** after a moment, a **random photo** appears! 🖼️

| Part | Meaning |
|---|---|
| `AsyncImage` | A view that **downloads** and shows an image from the internet. |
| `url: URL(string: ...)` | The image's web address. (An Optional URL is fine here.) |
| `picsum.photos/300` | A free service that gives a random 300×300 photo — great for practice. |

> 📖 **New word: AsyncImage**
> A SwiftUI view that loads an image **asynchronously** (in the background — Chapter 28) and shows it when ready.

While loading, it shows a **gray box**. Then the image appears.

⚠️ **Careful:** By default the image shows at its **original size** — maybe too big! Let's fix that.

---

## 2. Resizing: the `content` / `placeholder` form

```swift
AsyncImage(url: URL(string: "https://picsum.photos/600/400")) { image in
    image
        .resizable()
        .scaledToFill()
} placeholder: {
    ProgressView()
}
.frame(width: 300, height: 200)
.clipShape(RoundedRectangle(cornerRadius: 16))
```

| Part | Meaning |
|---|---|
| `{ image in ... }` | When loaded, you get an `Image`. Style it like any image (Chapter 42). |
| `.resizable().scaledToFill()` | Fill the frame, keep its shape. |
| `placeholder: { ProgressView() }` | What to show **while loading**: a spinner ⏳. |
| `.frame(...)` and `.clipShape(...)` | On the **AsyncImage** itself: size and rounded corners for all states. |

🧠 **Remember:** Use the `{ image in } placeholder: { }` form so you can call `.resizable()`.

### Nice placeholders

```swift
placeholder: {
    ZStack {
        Color.gray.opacity(0.2)
        Image(systemName: "photo")
            .font(.largeTitle)
            .foregroundStyle(.gray)
    }
}
```

---

## 3. Handling errors: the `phase` form

The image might **fail** (no internet, broken URL, 404). Use **phases**:

```swift
AsyncImage(url: URL(string: "https://picsum.photos/400")) { phase in
    switch phase {
    case .empty:
        ProgressView()
    case .success(let image):
        image
            .resizable()
            .scaledToFit()
    case .failure:
        VStack {
            Image(systemName: "exclamationmark.triangle")
                .font(.largeTitle)
            Text("Couldn't load image")
                .font(.caption)
        }
        .foregroundStyle(.secondary)
    @unknown default:
        EmptyView()
    }
}
.frame(width: 250, height: 250)
```

| Phase | Meaning |
|---|---|
| `.empty` | Still loading (or no URL). |
| `.success(let image)` | Loaded! Here's the image. |
| `.failure` | Something went wrong. |
| `@unknown default` | For possible **future** phases Apple might add. Swift asks for it. |

> 📖 **New word: `@unknown default`**
> A `default` case for enums that might get **new cases in the future**. It keeps your `switch` working if Apple adds something.

This is the **same idea** as our `LoadState` enum in Chapter 58! 🎉

**Test the failure:** use a broken URL like `"https://picsum.photos/doesnotexist"`.

---

## 4. Fade-in animation ✨

```swift
AsyncImage(url: url, transaction: Transaction(animation: .easeIn(duration: 0.4))) { phase in
    switch phase {
    case .success(let image):
        image.resizable().scaledToFill()
            .transition(.opacity)
    case .failure:
        Image(systemName: "photo")
    default:
        ProgressView()
    }
}
```

| Part | Meaning |
|---|---|
| `transaction: Transaction(animation: ...)` | Animate the change between phases. |
| `.transition(.opacity)` | The image **fades in** (Chapter 55). |

---

## 5. Round profile pictures from the internet 👤

```swift
struct Avatar: View {
    let url: URL?
    var size: CGFloat = 60

    var body: some View {
        AsyncImage(url: url) { image in
            image.resizable().scaledToFill()
        } placeholder: {
            Image(systemName: "person.fill")
                .font(.system(size: size * 0.5))
                .foregroundStyle(.white)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(.gray.opacity(0.4))
        }
        .frame(width: size, height: size)
        .clipShape(Circle())
    }
}

// Use it:
Avatar(url: URL(string: "https://i.pravatar.cc/150?img=5"), size: 100)
```

| Part | Meaning |
|---|---|
| `struct Avatar` | A reusable view (Chapter 41). |
| `i.pravatar.cc/150?img=5` | A free service for sample face pictures. `img=1` to `img=70` give different faces. |
| `.clipShape(Circle())` | Round! |

---

## 6. Images in a list 📋

```swift
struct Photo: Identifiable {
    let id: Int
    var url: URL? { URL(string: "https://picsum.photos/id/\(id)/200") }
    var title: String { "Photo #\(id)" }
}

struct ContentView: View {
    let photos = (10...40).map { Photo(id: $0) }

    var body: some View {
        NavigationStack {
            List(photos) { photo in
                HStack(spacing: 12) {
                    AsyncImage(url: photo.url) { image in
                        image.resizable().scaledToFill()
                    } placeholder: {
                        Color.gray.opacity(0.2)
                    }
                    .frame(width: 70, height: 70)
                    .clipShape(RoundedRectangle(cornerRadius: 10))

                    Text(photo.title)
                        .font(.headline)
                }
            }
            .navigationTitle("Photos 📷")
        }
    }
}
```

| Part | Meaning |
|---|---|
| `(10...40).map { Photo(id: $0) }` | Make 31 photos from a range (`map` — Chapter 19). |
| `picsum.photos/id/\(id)/200` | A **specific** photo by id (always the same image). |
| `var url: URL? { ... }` | A computed property (Chapter 20). |

`List` is **lazy** — images load only when rows scroll into view. 🚀

---

## 7. A photo grid 🔲

```swift
struct ContentView: View {
    let ids = Array(100...160)
    let columns = [GridItem(.adaptive(minimum: 100), spacing: 4)]

    var body: some View {
        NavigationStack {
            ScrollView {
                LazyVGrid(columns: columns, spacing: 4) {
                    ForEach(ids, id: \.self) { id in
                        AsyncImage(url: URL(string: "https://picsum.photos/id/\(id)/300")) { image in
                            image.resizable().scaledToFill()
                        } placeholder: {
                            Color.gray.opacity(0.15)
                        }
                        .frame(minWidth: 0, maxWidth: .infinity)
                        .frame(height: 110)
                        .clipped()
                    }
                }
            }
            .navigationTitle("Gallery")
        }
    }
}
```

| Part | Meaning |
|---|---|
| `GridItem(.adaptive(minimum: 100))` | "Fit as many columns as possible, each at least 100 wide." More columns on iPad automatically! |
| `.clipped()` | Cut off parts of the image outside the frame. |

---

## 8. Caching (what you should know)

> 📖 **New word: Cache**
> A place where downloaded things are **kept** for a while, so they don't need to be downloaded again.

- `AsyncImage` uses the system's basic URL cache. Images **may** be reused, but not always.
- In long lists, scrolling back up can **re-download** images.
- For big photo apps, developers often use a **caching library** (like **Kingfisher** or **Nuke**) or write their own image cache.

💡 **Tip:** For learning and small apps, `AsyncImage` is perfect. 👍

> 📖 **New word: Library (package)**
> Code written by other developers that you can add to your app. In Xcode: **File → Add Package Dependencies…** (Swift Package Manager).

---

## 9. Letting the user pick a photo: `PhotosPicker` 🖼️

Not from the internet, but very useful: let the user choose a photo from **their** library.

```swift
import SwiftUI
import PhotosUI

struct ContentView: View {
    @State private var selectedItem: PhotosPickerItem?
    @State private var selectedImage: Image?

    var body: some View {
        VStack(spacing: 20) {
            if let selectedImage {
                selectedImage
                    .resizable()
                    .scaledToFill()
                    .frame(width: 200, height: 200)
                    .clipShape(Circle())
            } else {
                Image(systemName: "person.crop.circle.badge.plus")
                    .font(.system(size: 100))
                    .foregroundStyle(.gray)
            }

            PhotosPicker("Choose photo", selection: $selectedItem, matching: .images)
                .buttonStyle(.borderedProminent)
        }
        .onChange(of: selectedItem) {
            Task {
                if let data = try? await selectedItem?.loadTransferable(type: Data.self),
                   let uiImage = UIImage(data: data) {
                    selectedImage = Image(uiImage: uiImage)
                }
            }
        }
    }
}
```

| Part | Meaning |
|---|---|
| `import PhotosUI` | The framework for the photo picker. |
| `PhotosPicker(..., selection: $selectedItem, matching: .images)` | A button that opens the system photo picker. Only images. |
| `PhotosPickerItem?` | The chosen item (not the image yet!). |
| `.loadTransferable(type: Data.self)` | Load the photo's data (async — it might be large or in iCloud). |
| `UIImage(data:)` | Turn the data into an image (UIKit type). |
| `Image(uiImage:)` | Turn it into a SwiftUI `Image`. |

> 📖 **New word: UIImage**
> The image type from **UIKit** (Apple's older UI framework). SwiftUI can show it with `Image(uiImage:)`.

💡 **Tip:** `PhotosPicker` does **not** need a privacy permission key (Chapter 37), because the user picks photos in a safe system window. 🔐

In the Simulator: **drag** photos from your Mac onto the Simulator to add them to its Photos app (Chapter 34).

---

## 10. Mini project: a team directory 👥

Combining Chapters 58, 59 and 60: load users from JSON, show their avatars.

```swift
import SwiftUI

struct Member: Codable, Identifiable {
    let id: Int
    let name: String
    let email: String
    let company: Company

    struct Company: Codable {
        let name: String
    }

    var avatarURL: URL? {
        URL(string: "https://i.pravatar.cc/150?img=\(id + 10)")
    }
}

@MainActor
@Observable
class DirectoryModel {
    var members: [Member] = []
    var errorMessage: String?

    func load() async {
        do {
            let url = URL(string: "https://jsonplaceholder.typicode.com/users")!
            let (data, _) = try await URLSession.shared.data(from: url)
            members = try JSONDecoder().decode([Member].self, from: data)
            errorMessage = nil
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}

struct ContentView: View {
    @State private var model = DirectoryModel()

    var body: some View {
        NavigationStack {
            List(model.members) { member in
                NavigationLink {
                    MemberDetail(member: member)
                } label: {
                    HStack(spacing: 14) {
                        Avatar(url: member.avatarURL, size: 50)
                        VStack(alignment: .leading) {
                            Text(member.name).font(.headline)
                            Text(member.company.name)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
            }
            .navigationTitle("Team 👥")
            .overlay {
                if model.members.isEmpty {
                    if let message = model.errorMessage {
                        ContentUnavailableView("Error", systemImage: "wifi.slash",
                                               description: Text(message))
                    } else {
                        ProgressView("Loading team...")
                    }
                }
            }
            .task { await model.load() }
            .refreshable { await model.load() }
        }
    }
}

struct MemberDetail: View {
    let member: Member

    var body: some View {
        VStack(spacing: 16) {
            Avatar(url: member.avatarURL, size: 140)
                .shadow(radius: 10)
            Text(member.name)
                .font(.title.bold())
            Label(member.email, systemImage: "envelope")
            Label(member.company.name, systemImage: "building.2")
                .foregroundStyle(.secondary)
            Spacer()
        }
        .padding(.top, 40)
        .navigationTitle(member.name)
        .navigationBarTitleDisplayMode(.inline)
    }
}

// Avatar view from section 5
```

| Part | Meaning |
|---|---|
| `struct Company: Codable` inside `Member` | A **nested type** for the nested JSON object `"company": { "name": ... }`. |
| `avatarURL` | A computed property that makes a picture URL from the id. |
| `.overlay { ... }` | Loading spinner or error on top of the empty list. |

---

## 🏋️ Practice

1. Show a random photo from `https://picsum.photos/400` with a spinner placeholder and rounded corners.
2. Use the `phase` form and show a nice error view for a broken URL.
3. Make a reusable `Avatar` view and show 5 different faces in an `HStack`.
4. Make a list of 20 photos with titles.
5. Make an adaptive photo grid.
6. Add a `PhotosPicker` to choose a profile picture.
7. Add a "shuffle" button that reloads a random image (hint: add `?random=\(Int.random(in: 1...1000))` to the URL so it changes).

---

## 🧠 Remember

- `AsyncImage(url:)` downloads and shows an image.
- Use `{ image in image.resizable()... } placeholder: { ... }` to style it.
- Use the `phase` form (`.empty`, `.success`, `.failure`) to handle errors.
- Put `.frame` and `.clipShape` on the `AsyncImage` itself.
- In lists and grids, images load lazily as you scroll.
- `PhotosPicker` lets users choose their own photos — no permission key needed.

---

⬅️ **Back:** [Chapter 59 — Reading JSON](59-json-codable.md)
➡️ **Next:** [Chapter 61 — Project: To-Do List App](61-project-todo.md)
