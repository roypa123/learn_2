# Chapter 62 — Project: Weather App 🌤️

🍎 **Needs a Mac** (and internet)

---

## What you will build

A real **Weather app** that loads live data from the internet:

- 🌡️ Current temperature, wind and description
- 📅 A 7-day forecast
- 🏙️ Choose from a list of cities (and save your choice)
- 🎨 Background gradient that changes with the weather
- ⏳ Loading, error and pull-to-refresh

We use **Open-Meteo** (`open-meteo.com`) — a **free** weather API that needs **no API key** and no sign-up. 🎉

Skills used: networking (Ch 58), JSON (Ch 59), `@Observable` (Ch 53), `@AppStorage` (Ch 56), enums (Ch 23), stacks and gradients (Ch 43, 54), `async`/`await` (Ch 28).

```
 ┌─────────────────────────────┐
 │  Chennai ▾                  │
 │                             │
 │           ⛅                 │
 │          31°                │
 │     Partly cloudy           │
 │   💨 12 km/h                │
 │ ┌─────────────────────────┐ │
 │ │ Today   ☀️   34°  27°    │ │
 │ │ Wed     🌧️   30°  25°    │ │
 │ │ Thu     ⛈️   29°  24°    │ │
 │ │ ...                     │ │
 │ └─────────────────────────┘ │
 └─────────────────────────────┘
```

---

## Step 0: Look at the API first 🔎

Before writing code, **always look at the data**.

Open this URL in your browser (works on Windows too!):

```
https://api.open-meteo.com/v1/forecast?latitude=13.08&longitude=80.27&current=temperature_2m,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto
```

Let's read the URL:

| Part | Meaning |
|---|---|
| `latitude=13.08&longitude=80.27` | The location (Chennai). |
| `current=temperature_2m,weather_code,wind_speed_10m` | What we want **now**: temperature, weather type, wind speed. |
| `daily=weather_code,temperature_2m_max,temperature_2m_min` | What we want **per day**. |
| `timezone=auto` | Use the city's local time zone for days. |

> 📖 **New word: Latitude / Longitude**
> Two numbers that describe any place on Earth. Latitude = north/south, longitude = east/west. 🌍

You'll see JSON like this (shortened):

```json
{
  "latitude": 13.125,
  "longitude": 80.25,
  "timezone": "Asia/Kolkata",
  "current": {
    "time": "2026-10-14T15:30",
    "temperature_2m": 31.2,
    "weather_code": 2,
    "wind_speed_10m": 12.4
  },
  "daily": {
    "time": ["2026-10-14", "2026-10-15", "2026-10-16", "..."],
    "weather_code": [2, 61, 95, "..."],
    "temperature_2m_max": [34.1, 30.2, 29.0, "..."],
    "temperature_2m_min": [27.0, 25.3, 24.8, "..."]
  }
}
```

Notice:
- `current` is an **object**.
- `daily` has **arrays** — the first item of each array is today, the second is tomorrow, etc.
- Keys use **snake_case** → we'll use `.convertFromSnakeCase` (Ch 59).
- `weather_code` is a **number** that means a weather type (0 = clear sky, 61 = rain…).

⚠️ **Careful:** Always check the current documentation on **open-meteo.com** — APIs can change. If a field name is different, update your struct to match what you see in the browser.

---

## Step 1: Create the project and files

1. New project: `SkyCast`, SwiftUI, Storage: None.
2. Create files:

```
SkyCast/
 ├─ SkyCastApp.swift
 ├─ Models/
 │   ├─ City.swift
 │   ├─ WeatherResponse.swift
 │   └─ WeatherCondition.swift
 ├─ Services/
 │   └─ WeatherService.swift
 ├─ ViewModels/
 │   └─ WeatherViewModel.swift
 └─ Views/
     ├─ ContentView.swift
     └─ ForecastRow.swift
```

---

## Step 2: Cities — `City.swift`

```swift
import Foundation

struct City: Identifiable, Hashable, Codable {
    let name: String
    let latitude: Double
    let longitude: Double

    var id: String { name }

    static let all: [City] = [
        City(name: "Chennai", latitude: 13.08, longitude: 80.27),
        City(name: "Mumbai", latitude: 19.08, longitude: 72.88),
        City(name: "Delhi", latitude: 28.61, longitude: 77.21),
        City(name: "Bengaluru", latitude: 12.97, longitude: 77.59),
        City(name: "London", latitude: 51.51, longitude: -0.13),
        City(name: "New York", latitude: 40.71, longitude: -74.01),
        City(name: "Tokyo", latitude: 35.68, longitude: 139.69),
        City(name: "Sydney", latitude: -33.87, longitude: 151.21)
    ]
}
```

| Part | Meaning |
|---|---|
| `var id: String { name }` | The city name is the ID (names are unique in our list). |
| `static let all` | A list of cities, shared by the type (Ch 20). Add your own city! |

💡 **Tip:** To find a city's latitude and longitude, search "CITY latitude longitude" on the web.

---

## Step 3: Decoding the JSON — `WeatherResponse.swift`

Make structs that **match** the JSON shape:

```swift
import Foundation

struct WeatherResponse: Codable {
    let current: Current
    let daily: Daily

    struct Current: Codable {
        let time: String
        let temperature2m: Double
        let weatherCode: Int
        let windSpeed10m: Double
    }

    struct Daily: Codable {
        let time: [String]
        let weatherCode: [Int]
        let temperature2mMax: [Double]
        let temperature2mMin: [Double]
    }
}
```

| JSON key | `convertFromSnakeCase` makes | Our property |
|---|---|---|
| `temperature_2m` | `temperature2m` | ✅ `temperature2m` |
| `weather_code` | `weatherCode` | ✅ `weatherCode` |
| `wind_speed_10m` | `windSpeed10m` | ✅ `windSpeed10m` |
| `temperature_2m_max` | `temperature2mMax` | ✅ `temperature2mMax` |

| Part | Meaning |
|---|---|
| Nested `struct Current` / `struct Daily` | Each JSON object `{ }` → a struct (Ch 59). |
| `[String]`, `[Int]`, `[Double]` | Each JSON array → a Swift array. |
| We skip `latitude`, `timezone`… | Keys we don't need can be left out. |

### A friendlier "day" type

Arrays side by side are awkward to use. Let's turn them into a list of `DayForecast`:

```swift
struct DayForecast: Identifiable {
    let date: Date
    let code: Int
    let maxTemp: Double
    let minTemp: Double

    var id: Date { date }
}

extension WeatherResponse.Daily {
    var days: [DayForecast] {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"

        var result: [DayForecast] = []
        for index in time.indices {
            guard let date = formatter.date(from: time[index]),
                  index < weatherCode.count,
                  index < temperature2mMax.count,
                  index < temperature2mMin.count else { continue }

            result.append(DayForecast(date: date,
                                      code: weatherCode[index],
                                      maxTemp: temperature2mMax[index],
                                      minTemp: temperature2mMin[index]))
        }
        return result
    }
}
```

| Part | Meaning |
|---|---|
| `DateFormatter` with `"yyyy-MM-dd"` | Turns text like `"2026-10-14"` into a `Date`. |
| `time.indices` | All valid positions: 0, 1, 2… (safer than `0..<time.count`). |
| `guard ... else { continue }` | Skip a day if anything is wrong (bad date, arrays of different lengths). **No crashes** from "index out of range" (Ch 14)! |
| `continue` | Skip to the next loop round (Ch 12). |

```
 time:    ["10-14", "10-15", "10-16"]        DayForecast(10-14, code 2, 34, 27)
 code:    [  2,       61,      95   ]   →    DayForecast(10-15, code 61, 30, 25)
 max:     [ 34,       30,      29   ]        DayForecast(10-16, code 95, 29, 24)
 min:     [ 27,       25,      24   ]
```

---

## Step 4: Weather codes → words and icons — `WeatherCondition.swift`

Open-Meteo uses **WMO weather codes** (a world standard). Let's map them to friendly words, SF Symbols and colors:

```swift
import SwiftUI

enum WeatherCondition {
    case clear, partlyCloudy, cloudy, fog, drizzle, rain, snow, thunderstorm, unknown

    init(code: Int) {
        switch code {
        case 0: self = .clear
        case 1, 2: self = .partlyCloudy
        case 3: self = .cloudy
        case 45, 48: self = .fog
        case 51...57: self = .drizzle
        case 61...67, 80...82: self = .rain
        case 71...77, 85, 86: self = .snow
        case 95...99: self = .thunderstorm
        default: self = .unknown
        }
    }

    var description: String {
        switch self {
        case .clear: "Clear sky"
        case .partlyCloudy: "Partly cloudy"
        case .cloudy: "Cloudy"
        case .fog: "Foggy"
        case .drizzle: "Drizzle"
        case .rain: "Rain"
        case .snow: "Snow"
        case .thunderstorm: "Thunderstorm"
        case .unknown: "Unknown"
        }
    }

    var symbol: String {
        switch self {
        case .clear: "sun.max.fill"
        case .partlyCloudy: "cloud.sun.fill"
        case .cloudy: "cloud.fill"
        case .fog: "cloud.fog.fill"
        case .drizzle: "cloud.drizzle.fill"
        case .rain: "cloud.rain.fill"
        case .snow: "cloud.snow.fill"
        case .thunderstorm: "cloud.bolt.rain.fill"
        case .unknown: "questionmark.circle"
        }
    }

    var gradient: [Color] {
        switch self {
        case .clear: [.orange, .yellow]
        case .partlyCloudy: [.blue, .cyan]
        case .cloudy, .fog: [.gray, .blue.opacity(0.6)]
        case .drizzle, .rain: [.indigo, .gray]
        case .snow: [.cyan, .white]
        case .thunderstorm: [.black, .purple]
        case .unknown: [.gray, .secondary]
        }
    }
}
```

| Part | Meaning |
|---|---|
| `init(code: Int)` | Make a condition from a number. A custom `init` for an enum (Ch 29 did this too!). |
| `case 51...57:` | Ranges in `switch` (Ch 11). |
| `description`, `symbol`, `gradient` | Computed properties (Ch 23). |

> 📖 **New word: WMO code**
> A number from the World Meteorological Organization that describes weather. Open-Meteo's documentation lists them all.

---

## Step 5: The service — `WeatherService.swift`

```swift
import Foundation

enum WeatherError: LocalizedError {
    case badResponse(Int)

    var errorDescription: String? {
        switch self {
        case .badResponse(let code):
            "The weather server answered with code \(code). Please try again."
        }
    }
}

struct WeatherService {
    func fetchWeather(for city: City) async throws -> WeatherResponse {
        var components = URLComponents(string: "https://api.open-meteo.com/v1/forecast")!
        components.queryItems = [
            URLQueryItem(name: "latitude", value: String(city.latitude)),
            URLQueryItem(name: "longitude", value: String(city.longitude)),
            URLQueryItem(name: "current", value: "temperature_2m,weather_code,wind_speed_10m"),
            URLQueryItem(name: "daily", value: "weather_code,temperature_2m_max,temperature_2m_min"),
            URLQueryItem(name: "timezone", value: "auto")
        ]

        let (data, response) = try await URLSession.shared.data(from: components.url!)

        if let http = response as? HTTPURLResponse, !(200...299).contains(http.statusCode) {
            throw WeatherError.badResponse(http.statusCode)
        }

        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try decoder.decode(WeatherResponse.self, from: data)
    }
}
```

| Part | Meaning |
|---|---|
| `URLComponents` + `queryItems` | Build the URL safely (Ch 58). |
| Status code check | 2xx = success; otherwise throw (Ch 58). |
| `.convertFromSnakeCase` | `temperature_2m` → `temperature2m` (Ch 59). |

---

## Step 6: The view model — `WeatherViewModel.swift`

```swift
import SwiftUI

@MainActor
@Observable
class WeatherViewModel {
    enum State {
        case loading
        case loaded(WeatherResponse)
        case failed(String)
    }

    var state: State = .loading
    private let service = WeatherService()

    func load(city: City) async {
        if case .loaded = state {
            // keep showing old data while refreshing
        } else {
            state = .loading
        }

        do {
            let weather = try await service.fetchWeather(for: city)
            state = .loaded(weather)
        } catch is CancellationError {
            // the view went away or a new load started — ignore
        } catch {
            state = .failed(error.localizedDescription)
        }
    }
}
```

| Part | Meaning |
|---|---|
| `enum State` | Loading / loaded / failed — our favorite pattern (Ch 58)! |
| `if case .loaded = state` | "Is the state `.loaded`?" (Ch 23 `if case`). Keep old data visible during **pull-to-refresh** — no flashing spinner. |
| `catch is CancellationError` | When you switch cities quickly, the old request is **cancelled**. That's not a real error, so we ignore it. |

> 📖 **New word: CancellationError**
> Thrown when async work is **cancelled** (for example, the `.task` stops because the screen changed).

---

## Step 7: A forecast row — `ForecastRow.swift`

```swift
import SwiftUI

struct ForecastRow: View {
    let day: DayForecast

    var condition: WeatherCondition { WeatherCondition(code: day.code) }

    var dayName: String {
        Calendar.current.isDateInToday(day.date)
            ? "Today"
            : day.date.formatted(.dateTime.weekday(.abbreviated))
    }

    var body: some View {
        HStack {
            Text(dayName)
                .frame(width: 60, alignment: .leading)
            Spacer()
            Image(systemName: condition.symbol)
                .symbolRenderingMode(.multicolor)
                .font(.title3)
                .frame(width: 40)
            Spacer()
            Text("\(Int(day.maxTemp.rounded()))°")
                .bold()
                .frame(width: 44, alignment: .trailing)
            Text("\(Int(day.minTemp.rounded()))°")
                .foregroundStyle(.white.opacity(0.7))
                .frame(width: 44, alignment: .trailing)
        }
        .font(.body)
        .foregroundStyle(.white)
    }
}
```

| Part | Meaning |
|---|---|
| `Calendar.current.isDateInToday(...)` | Is this date today? |
| `.formatted(.dateTime.weekday(.abbreviated))` | Short day name like "Wed" — in the user's language! 🌍 |
| `Int(day.maxTemp.rounded())` | `33.6` → `34`. |
| Fixed `.frame(width:)` | Columns line up nicely in every row. |

---

## Step 8: The main screen — `ContentView.swift`

```swift
import SwiftUI

struct ContentView: View {
    @State private var viewModel = WeatherViewModel()
    @AppStorage("selectedCity") private var selectedCityName = City.all[0].name

    var selectedCity: City {
        City.all.first { $0.name == selectedCityName } ?? City.all[0]
    }

    var body: some View {
        ZStack {
            background
                .ignoresSafeArea()

            ScrollView {
                VStack(spacing: 24) {
                    cityPicker

                    switch viewModel.state {
                    case .loading:
                        ProgressView()
                            .tint(.white)
                            .controlSize(.large)
                            .padding(.top, 100)

                    case .loaded(let weather):
                        currentWeather(weather.current)
                        forecast(weather.daily.days)

                    case .failed(let message):
                        errorView(message)
                    }
                }
                .padding()
            }
            .refreshable {
                await viewModel.load(city: selectedCity)
            }
        }
        .task(id: selectedCityName) {
            await viewModel.load(city: selectedCity)
        }
    }

    // MARK: - Pieces

    private var background: some View {
        let colors: [Color]
        if case .loaded(let weather) = viewModel.state {
            colors = WeatherCondition(code: weather.current.weatherCode).gradient
        } else {
            colors = [.blue, .cyan]
        }
        return LinearGradient(colors: colors, startPoint: .top, endPoint: .bottom)
            .animation(.easeInOut(duration: 0.8), value: colors)
    }

    private var cityPicker: some View {
        Menu {
            Picker("City", selection: $selectedCityName) {
                ForEach(City.all) { city in
                    Text(city.name).tag(city.name)
                }
            }
        } label: {
            HStack(spacing: 6) {
                Image(systemName: "location.fill")
                Text(selectedCity.name)
                Image(systemName: "chevron.down")
                    .font(.caption)
            }
            .font(.title2.bold())
            .foregroundStyle(.white)
            .padding(.horizontal, 16)
            .padding(.vertical, 8)
            .background(.ultraThinMaterial, in: Capsule())
        }
    }

    private func currentWeather(_ current: WeatherResponse.Current) -> some View {
        let condition = WeatherCondition(code: current.weatherCode)
        return VStack(spacing: 8) {
            Image(systemName: condition.symbol)
                .symbolRenderingMode(.multicolor)
                .font(.system(size: 100))
                .shadow(radius: 10)

            Text("\(Int(current.temperature2m.rounded()))°")
                .font(.system(size: 90, weight: .thin))
                .contentTransition(.numericText())

            Text(condition.description)
                .font(.title2)

            Label("\(Int(current.windSpeed10m.rounded())) km/h", systemImage: "wind")
                .font(.headline)
                .opacity(0.9)
        }
        .foregroundStyle(.white)
        .padding(.top, 20)
    }

    private func forecast(_ days: [DayForecast]) -> some View {
        VStack(alignment: .leading, spacing: 14) {
            Label("7-DAY FORECAST", systemImage: "calendar")
                .font(.caption.bold())
                .foregroundStyle(.white.opacity(0.8))

            ForEach(days) { day in
                ForecastRow(day: day)
                if day.id != days.last?.id {
                    Divider().overlay(.white.opacity(0.3))
                }
            }
        }
        .padding()
        .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 20))
    }

    private func errorView(_ message: String) -> some View {
        VStack(spacing: 16) {
            Image(systemName: "wifi.exclamationmark")
                .font(.system(size: 60))
            Text("Couldn't load weather")
                .font(.title2.bold())
            Text(message)
                .multilineTextAlignment(.center)
                .opacity(0.8)
            Button("Try again") {
                Task { await viewModel.load(city: selectedCity) }
            }
            .buttonStyle(.borderedProminent)
            .tint(.white)
            .foregroundStyle(.blue)
        }
        .foregroundStyle(.white)
        .padding(.top, 60)
    }
}

#Preview {
    ContentView()
}
```

Important parts:

| Part | Meaning |
|---|---|
| `@AppStorage("selectedCity")` | The chosen city is **remembered** (Ch 56). |
| `City.all.first { ... } ?? City.all[0]` | Find the saved city; if not found, use the first. |
| `.task(id: selectedCityName)` | ⭐ Run when the screen appears **and again whenever the city changes**. The old task is cancelled automatically. |
| `Menu { Picker(...) }` | A tappable city name that opens a menu of cities. |
| `background` | The gradient depends on the weather; `.animation(..., value: colors)` makes it **fade** smoothly (Ch 55). |
| Private computed views and functions | Break the big screen into **small named pieces** — easier to read. |

> 📖 **New word: `.task(id:)`**
> Like `.task`, but **restarts** whenever the `id` value changes. Perfect for "reload when X changes".

---

## Step 9: Run it! 🚀

`Cmd + R`. You should see live weather for Chennai. 🌤️

| Test | Expected |
|---|---|
| Change the city | Loading → new weather. Background color changes. |
| Pull down | Refreshes (old data stays visible). |
| Turn off Wi-Fi, change city | Error screen with **Try again**. |
| Stop and re-run | Your last city is selected. 💾 |
| Dark mode | Still looks good (white text on gradients). |

### If it doesn't work 🔧

1. Print the raw JSON in `fetchWeather`: `print(String(decoding: data, as: UTF8.self))`.
2. Open the same URL in your browser. Compare keys with your structs.
3. Read the decoding error (Ch 59) — it tells you which key is wrong.

---

## 🏆 Challenges

1. **Hourly forecast:** add `&hourly=temperature_2m,weather_code` and show a horizontal `ScrollView` of the next 24 hours.
2. **More details:** add `relative_humidity_2m` and `apparent_temperature` ("feels like") to `current`.
3. **°C / °F switch:** add `&temperature_unit=fahrenheit` based on an `@AppStorage` setting.
4. **City search:** Open-Meteo has a free **geocoding** API (`geocoding-api.open-meteo.com/v1/search?name=Pune`). Let users search any city!
5. **Current location:** use **CoreLocation** to get the user's location (needs the location **privacy key** — Ch 37).
6. **Favorites:** let users save several cities and swipe between them with `TabView(.page)` (Ch 50).

---

## 🧠 What you practiced

- **Reading API docs and real JSON** before coding.
- Decoding **nested JSON with parallel arrays**, and turning it into friendly structs safely.
- Mapping codes to **words, icons and colors** with an enum.
- A clean structure: **Service** (network) → **ViewModel** (state) → **Views** (UI).
- `.task(id:)` to reload when something changes, cancellation handling, pull-to-refresh.
- Saving the user's choice with `@AppStorage`.
- Weather-based **animated gradients** and **materials**.

---

⬅️ **Back:** [Chapter 61 — Project: To-Do List App](61-project-todo.md)
➡️ **Next:** [Chapter 63 — Project: Notes App](63-project-notes.md)
