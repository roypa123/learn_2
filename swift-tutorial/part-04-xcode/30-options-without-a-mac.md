# Chapter 30 — Options When You Don't Own a Mac

✅ **Works in browser** — this chapter is just reading and planning.
From the next chapter on, you need one of the options below. 🍎

---

## What you will learn

- Why iPhone apps need a Mac.
- 5 ways to get access to a Mac (or something like it).
- The good and bad sides of each.
- Which one to choose for **your** situation.

---

## 1. Why do I need a Mac?

To build iPhone apps the normal way, you need **Xcode**.
Xcode is made by Apple and **only runs on macOS** (the Mac operating system).

> 📖 **New word: macOS**
> The operating system on Mac computers. Like Windows, but made by Apple.

> 📖 **New word: Operating system (OS)**
> The main software that runs a computer. Windows, macOS, Linux, iOS and Android are operating systems.

You **already learned Swift** without a Mac (Parts 1–3). 🎉
Now, to build **screens** and **real apps**, you need one of the options below.

---

## 2. Option A: Rent a Mac in the cloud ☁️

Some companies have many Macs in their buildings. You **rent** one and control it **from your Windows computer** over the internet.

```
 Your Windows PC  ─── internet ───►  A Mac in a data center
 (you see its screen                 (Xcode runs here)
  in a window)
```

> 📖 **New word: Cloud**
> Computers in another place that you use over the internet.

> 📖 **New word: Remote desktop**
> A program that shows another computer's screen on your computer. You use your mouse and keyboard to control it.

**Examples of services** (search for them online):
- **MacinCloud**
- **MacStadium**
- **AWS EC2 Mac** (Amazon — more for companies, usually more expensive)

| 👍 Good | 👎 Bad |
|---|---|
| Start today, no big purchase. | Monthly (or hourly) cost. |
| Works from Windows. | Needs a fast, stable internet connection. |
| You can stop any time. | Can feel slow or laggy. |
| | Connecting a real iPhone is hard or impossible. Use the Simulator instead. |

💡 **Tip:** Prices and plans change often. Compare a few services. Look for: a recent macOS version, enough storage (Xcode needs **a lot** — 40 GB or more free), and permission to install Xcode.

⚠️ **Careful:** Never type your bank card details on a website you don't trust. Use well-known services.

---

## 3. Option B: An iPad with Swift Playgrounds 📱

**Swift Playgrounds** is a free Apple app for the **iPad** (and Mac). It can build **real SwiftUI apps** — and even send them to the App Store!

| 👍 Good | 👎 Bad |
|---|---|
| An iPad usually costs less than a Mac. | Not the full Xcode. Fewer settings and tools. |
| Live preview of SwiftUI screens. | Most Xcode chapters (32–40) won't match exactly. |
| Great for learning SwiftUI (Part 5). | Big, professional apps are harder. |
| Free app. | Needs a fairly recent iPad. |

💡 **Tip:** If you use an iPad, you can still follow **Part 5 (SwiftUI)** almost completely. For Part 4 (Xcode), read the chapters to understand the ideas — you'll use them when you get a Mac later.

---

## 4. Option C: Buy a Mac (new or used) 💻

The **Mac mini** is the cheapest Mac. A **used** or **refurbished** one can cost much less.

> 📖 **New word: Refurbished**
> A used product that was checked and repaired, and is sold again — often with a warranty.

What to look for:

| Thing | Recommendation |
|---|---|
| Chip | **Apple Silicon** (M1, M2, M3, M4 or newer). Avoid old Intel Macs — new Xcode versions may not support them. |
| Memory (RAM) | **16 GB** is comfortable. 8 GB works but can be slow. |
| Storage | **256 GB minimum**, 512 GB better. Xcode and Simulators use a lot of space. |
| macOS version | Must be able to run the **latest** macOS, because new Xcode needs a new macOS. |

| 👍 Good | 👎 Bad |
|---|---|
| Best experience. Everything works. | Costs the most at the start. |
| Fast. Works offline. | |
| Easy to connect a real iPhone. | |

💡 **Tip:** Apple's official **refurbished store** sells Macs with a full warranty. It's often a safe way to save money.

---

## 5. Option D: Borrow a Mac 🤝

- A friend or family member.
- A school, college or library computer lab.
- A coding club or co-working space.

| 👍 Good | 👎 Bad |
|---|---|
| Free. | Limited time. |
| | You may not be allowed to install Xcode. |
| | Your projects aren't always with you (save them online — see Tip). |

💡 **Tip:** Save your project on **GitHub** or a USB drive, so you can continue on any Mac.

---

## 6. Option E (avoid): "Hackintosh" or macOS in a virtual machine on Windows ❌

You may read online about installing macOS on a normal PC.

⚠️ **Careful:** We **do not** recommend this:
- Apple's license only allows macOS on **Apple** computers.
- It is complicated, often breaks after updates, and can waste many days.
- Xcode and the Simulator may not work properly.

Choose one of the options A–D instead.

---

## 7. Which one should I choose? 🧭

```
          Do you have money to buy a Mac now?
                 /                    \
               YES                     NO
                |                       |
       Buy a Mac mini (C)      Can you borrow one? (D)
                                  /          \
                                YES          NO
                                 |            |
                            Use it        Do you have / can you get an iPad?
                                             /            \
                                           YES            NO
                                            |              |
                                   Swift Playgrounds (B)   Rent a cloud Mac (A)
```

| Your situation | Best choice |
|---|---|
| Just trying, small budget, good internet | **A — Cloud Mac** (1 month) |
| Have an iPad | **B — Swift Playgrounds** for SwiftUI, then a Mac later |
| Serious about making apps | **C — Buy a (used) Mac mini** |
| Have a friend / school with a Mac | **D — Borrow** |

---

## 8. What about the App Store?

To put an app on the **App Store**, you need an **Apple Developer Program** membership. It has a **yearly fee** (check Apple's website for the current price in your country).

You do **NOT** need to pay to:
- Learn.
- Use Xcode.
- Run apps in the Simulator.
- Run apps on **your own** iPhone (with a free Apple ID — with some limits, see Chapter 38).

So: **don't pay anything until you're ready to publish.** 😊

---

## 9. What you need in every case

| Thing | Why |
|---|---|
| An **Apple ID** (free) | To download Xcode and sign in. Make one at appleid.apple.com. |
| About **40 GB+** free space | Xcode + Simulators are big. |
| Patience 😊 | The first Xcode download can take an hour or more. |

> 📖 **New word: Apple ID**
> Your free Apple account. An email and password you use for all Apple services.

---

## 🏋️ Practice

1. Write down which option (A, B, C or D) fits you best, and **why**.
2. If you don't have one yet, create a free **Apple ID**.
3. If you choose option A: search for 2–3 cloud Mac services and compare their price, macOS version and storage.

---

## 🧠 Remember

- Xcode only runs on **macOS**.
- Options: **rent** a cloud Mac, use an **iPad** with Swift Playgrounds, **buy** a (used) Mac, or **borrow** one.
- Avoid Hackintosh / macOS on a PC.
- You only need to **pay Apple** when you want to publish on the App Store.

---

⬅️ **Back:** [Chapter 29 — Text Adventure Game](../part-03-building-types/29-project-text-adventure.md)
➡️ **Next:** [Chapter 31 — Installing Xcode](31-installing-xcode.md)
