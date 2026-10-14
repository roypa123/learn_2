# Chapter 65 — Putting Your App on the App Store 🚀

🍎 **Needs a Mac** and a **paid Apple Developer Program** membership.

---

## What you will learn

- The full journey from Xcode to the App Store.
- Joining the **Apple Developer Program**.
- Preparing your app (checklist).
- Creating your app in **App Store Connect**.
- **Archiving** and **uploading** a build.
- **TestFlight** — testing with real people.
- Screenshots, description, privacy information.
- **App Review** — and what to do if you're rejected.
- Updates after launch.

⚠️ **Careful:** Apple changes App Store Connect screens and rules often. The **steps** here stay the same, but button names and details can change. Always check Apple's current help pages (search "App Store Connect Help") and the **App Review Guidelines**.

---

## 1. The big picture 🗺️

```
  1. Join Apple Developer Program (yearly fee)
          │
          ▼
  2. Prepare the app (icon, version, test on device, privacy texts)
          │
          ▼
  3. Create the app record in App Store Connect
          │
          ▼
  4. Archive in Xcode  ──►  Upload the build
          │
          ▼
  5. TestFlight (optional but recommended)
          │
          ▼
  6. Fill in the store page (screenshots, description, privacy, price)
          │
          ▼
  7. Submit for App Review  ──►  ✅ Approved  ──►  🎉 On the App Store!
                               └► ❌ Rejected  ──►  fix and resubmit
```

> 📖 **New word: App Store Connect**
> Apple's website (`appstoreconnect.apple.com`) where you manage your apps: store pages, builds, TestFlight, sales, reviews.

---

## 2. Step 1: Join the Apple Developer Program 💳

1. Go to **developer.apple.com/programs** and click **Enroll**.
2. Sign in with your Apple ID (turn on **two-factor authentication** if asked).
3. Choose:

| Type | For | Needs |
|---|---|---|
| **Individual** | Just you | Your legal name. Your **name** appears as the seller. |
| **Organization** | A company | A legal company and a **D-U-N-S number** (a free business ID). The **company name** appears as the seller. |

4. Pay the **yearly fee** (check the current price for your country).
5. Wait for approval — from a few hours to a few days.

> 📖 **New word: D-U-N-S number**
> A unique number for businesses, used by Apple to check that a company is real.

💡 **Tip:** Some countries and organizations (like non-profits and schools) can ask for a **fee waiver**. Check Apple's website.

---

## 3. Step 2: Prepare your app ✅

Go through this **checklist** before uploading:

| ✅ | Item | Chapter |
|---|---|---|
| ☐ | **App icon**: 1024×1024 PNG, no transparency | 37 |
| ☐ | **Display name** is correct | 36 |
| ☐ | **Bundle ID** is final (it can't be changed after release!) | 33, 38 |
| ☐ | **Version** (e.g. `1.0`) and **Build** (e.g. `1`) are set | 36 |
| ☐ | **Privacy usage descriptions** for camera, photos, location… | 37 |
| ☐ | **Signing**: your **paid** team is selected, automatic signing ✅ | 38 |
| ☐ | Tested on a **real iPhone** | 39 |
| ☐ | Tested on **small and big** screens, **dark mode**, **big text** | 34, 54 |
| ☐ | No crashes. No placeholder text like "Lorem ipsum" or "TODO". | 40 |
| ☐ | Debug-only code is inside `#if DEBUG` | 35 |
| ☐ | Tests pass (`Cmd + U`) | 64 |
| ☐ | Launch screen looks good | 37 |
| ☐ | You have a **privacy policy** web page (required for all apps) | below |
| ☐ | You have a **support** web page or email | below |

> 📖 **New word: Privacy policy**
> A web page that explains what data your app collects and how you use it. **Every** app needs one, even if it collects nothing.

💡 **Tip:** If your app collects **no** data, your privacy policy can be short: "This app does not collect, store or share any personal data." You can host it for free (for example, with GitHub Pages or a simple website builder).

---

## 4. Step 3: Create the app in App Store Connect

1. Go to **appstoreconnect.apple.com** and sign in.
2. Click **Apps** → the **+** button → **New App**.

```
┌────────────────────────────────────────────┐
│ New App                                    │
│                                            │
│ Platforms:   ☑ iOS                         │
│ Name:        [ TaskMaster - Simple To-Do ] │
│ Primary Language: [ English (U.S.) ▾ ]     │
│ Bundle ID:   [ com.ravikumar.TaskMaster ▾ ]│
│ SKU:         [ taskmaster001 ]             │
│ User Access: (•) Full Access               │
│                                            │
│                         [ Cancel ] [Create]│
└────────────────────────────────────────────┘
```

| Field | Meaning |
|---|---|
| **Name** | The name on the App Store (up to 30 characters). Must be unique on the store. |
| **Primary Language** | The main language of your store page. |
| **Bundle ID** | Choose your app's Bundle ID. (If it's not in the list, build and run once with automatic signing — Xcode registers it — or register it on developer.apple.com.) |
| **SKU** | Your own private code for the app. Anything unique, like `taskmaster001`. Users never see it. |

> 📖 **New word: SKU**
> **S**tock **K**eeping **U**nit. A private ID for your own records.

3. Click **Create**. Your app now has a page in App Store Connect! 🎉

---

## 5. Step 4: Archive and upload 📦

### Archive

1. In Xcode, set the **run destination** to **Any iOS Device (arm64)** — not a Simulator!
2. **Product → Archive**.
3. Wait. Xcode builds a **Release** version (Chapter 35).
4. The **Organizer** window opens with your archive.

> 📖 **New word: Archive**
> A packaged **Release** build of your app, ready to upload (Chapter 35).

> 📖 **New word: Organizer**
> An Xcode window (**Window → Organizer**) that shows your archives, crash reports and more.

⚠️ **Careful:** If **Archive** is gray (disabled), your run destination is a **Simulator**. Choose **Any iOS Device**.

### Upload

1. In the Organizer, select your archive.
2. Click **Distribute App**.
3. Choose **App Store Connect** (sometimes shown as "TestFlight & App Store") → **Distribute** / **Upload**.
4. Keep the default options (automatic signing). Click **Next** / **Upload**.
5. Wait for "Upload Successful" ✅.

```
 Xcode                Apple                     You
  │ Archive             │                        │
  │ Distribute ───────► │ Processing (10–30 min) │
  │                     │ ──── email: "ready" ──►│
```

After upload, Apple **processes** the build (usually 10–30 minutes). You'll get an email. Then the build appears in App Store Connect under **TestFlight**.

### Common upload problems 🔧

| Problem | Fix |
|---|---|
| "No accounts with App Store Connect access" | Add your paid account in **Xcode → Settings → Accounts** (Ch 31). |
| "Redundant binary upload / build number already used" | Increase the **Build** number (Ch 36). Every upload needs a **new** build number. |
| "Missing app icon" | Add the 1024×1024 icon to **AppIcon** (Ch 37). |
| "Missing purpose string in Info.plist" | Add the missing **Privacy - … Usage Description** (Ch 37). |
| "Invalid bundle / unsupported SDK" | Update Xcode — Apple requires recent SDK versions. |

---

## 6. Step 5: TestFlight 🛫

**TestFlight** lets real people test your app **before** it's public.

> 📖 **New word: TestFlight**
> Apple's free service and app for sending test builds to testers (Ch 38).

| Testers | Who | Review needed? |
|---|---|---|
| **Internal** | Up to 100 people on your App Store Connect team | No — test right away |
| **External** | Up to 10,000 people, by email or a **public link** | A short **Beta App Review** for the first build |

### Steps

1. App Store Connect → your app → **TestFlight** tab.
2. Your build appears (after processing). Answer any **export compliance** question (most simple apps: "uses standard encryption only" / "none").
3. **Internal testing**: add yourself and team members.
4. **External testing**: create a group, add testers or create a **public link**, add "What to Test" notes, submit for Beta Review.
5. Testers install the **TestFlight** app from the App Store, then install your app.

> 📖 **New word: Export compliance**
> A legal question about encryption. If your app only uses Apple's standard HTTPS, the answer is usually simple. You can add `ITSAppUsesNonExemptEncryption = NO` to Info.plist to skip this question each time (only if that's true for your app).

💡 **Tip:** Testers can send **screenshots and feedback** directly from TestFlight. Ask friends and family to try your app and tell you what's confusing! 🙋

---

## 7. Step 6: The store page 🛍️

In App Store Connect → your app → the **App Store** tab → your version (e.g. **1.0 Prepare for Submission**).

### Screenshots 📸

- Required for the **iPhone** sizes Apple currently asks for (usually the largest iPhone display size; check App Store Connect for the exact sizes).
- Add iPad screenshots if your app supports iPad.
- **How:** run your app in the matching Simulator, then **File → Save Screen** (`Cmd + S`) in the Simulator (Ch 34).
- Use up to 10 screenshots. Show the **best** features first.

💡 **Tip:** Fill your app with **nice sample data** before taking screenshots. Empty screens don't sell! 😄

### Text

| Field | Tips |
|---|---|
| **Name** | Clear and short. |
| **Subtitle** | One short line under the name (up to 30 characters): "Simple tasks, done fast". |
| **Promotional Text** | Can be changed any time without a new version. |
| **Description** | What the app does and why it's great. First lines matter most. Simple sentences! |
| **Keywords** | Words people search for, separated by commas (up to 100 characters total). Don't repeat the app name. |
| **Support URL** | A web page (or page with an email) where users can get help. |
| **Marketing URL** | Optional: your app's website. |
| **Version / What's New** | For updates: what changed. |

### Other required info

| Section | What to do |
|---|---|
| **App Information** | Category (e.g. Productivity), content rights, age rating questionnaire. |
| **Age Rating** | Answer questions about content (violence, etc.). Apple calculates the rating. |
| **Pricing and Availability** | **Free** or a price. Choose countries. |
| **App Privacy** ("privacy nutrition label") | Tell Apple what data your app collects. If none: choose **"Data Not Collected"**. Add your **privacy policy URL**. |
| **Build** | Choose the build you uploaded (click **+** next to Build). |
| **App Review Information** | Your contact info. If the app needs a **login**, give Apple a **demo account**! Add notes to help the reviewer. |

> 📖 **New word: Privacy nutrition label**
> A section on your App Store page that shows users what data the app collects — like the nutrition label on food. 🥫

⚠️ **Careful:** Be **honest** in the privacy section. If you use analytics or ads libraries, they may collect data — you must declare it.

---

## 8. Step 7: Submit for review 📤

1. When everything is filled in, click **Add for Review** / **Submit for Review** (the button name varies).
2. Status changes to **Waiting for Review** → **In Review** → result.
3. Review often takes **about a day or two** (sometimes faster, sometimes longer).

### Release options

| Option | Meaning |
|---|---|
| **Automatically release** | Goes live as soon as it's approved. |
| **Manually release** | You click "Release" when you're ready (good for planned launches). |
| **Phased release** (updates) | The update reaches users gradually over 7 days. |

---

## 9. If your app is rejected ❌ (it happens to everyone!)

Don't worry — rejections are **normal**, especially the first time. Apple tells you **why** in **App Store Connect → Resolution Center** (or the app's messages).

### Common reasons

| Reason | Meaning | Fix |
|---|---|---|
| **Crashes / bugs** (Guideline 2.1) | The reviewer found a crash or something broken. | Test more on real devices. Fix and resubmit. |
| **Incomplete information** | Missing demo login, broken links. | Add a demo account and working URLs. |
| **Minimum functionality** (4.2) | The app is too simple (e.g. just a web page or one button). | Add real, useful features. |
| **Privacy** (5.1) | Missing privacy policy, unclear permission messages, collecting data without saying so. | Clear usage descriptions (Ch 37), a privacy policy, honest privacy label. |
| **Misleading metadata** (2.3) | Screenshots or description don't match the app. | Use real screenshots. Describe the real features. |
| **Placeholder content** | "Lorem ipsum", test data, "coming soon" buttons. | Remove it. |
| **Copying / trademarks** | Using another company's name or logo. | Use your own name and design. |

### What to do

1. **Read** the message carefully.
2. **Fix** the problem (or explain politely if you think it's a misunderstanding — you can reply in the Resolution Center).
3. Increase the **Build** number, archive, upload again (if you changed code).
4. **Resubmit**.

🧠 **Remember:** Read the **App Review Guidelines** (search "App Review Guidelines") **before** you submit. It saves a lot of time.

---

## 10. 🎉 Approved! Now what?

Your app is **on the App Store**! Share the link with everyone. 🥳

After launch:

| Task | Where |
|---|---|
| See downloads and sales | App Store Connect → **Analytics** / **Sales and Trends** |
| Read and reply to **ratings & reviews** | App Store Connect → your app → **Ratings and Reviews** |
| See **crash reports** | Xcode → **Window → Organizer → Crashes** |
| Ask for ratings politely | SwiftUI's `@Environment(\.requestReview)` (iOS shows the rating pop-up — not too often!) |

### Releasing an update 🔄

1. Make your changes in Xcode.
2. Increase the **Version** (e.g. `1.0` → `1.1`) **and** the **Build** number.
3. **Archive** → **Upload**.
4. App Store Connect → **+ Version** → fill in **What's New** → choose the build → **Submit**.

```
 Version 1.0 (Build 1, 2, 3...) ──► Version 1.1 (Build 4, 5...) ──► ...
```

---

## 11. Your launch checklist 📋

Copy this and tick it off! ✅

```
BEFORE UPLOAD
☐ Paid Apple Developer Program account
☐ Final Bundle ID
☐ App icon 1024×1024 (no transparency)
☐ Version + new Build number
☐ All privacy usage descriptions
☐ Tested on a real device, small & big screens, dark mode, big text
☐ No crashes, no placeholder text, debug code behind #if DEBUG

APP STORE CONNECT
☐ App record created (name, bundle ID, SKU)
☐ Build archived (Any iOS Device) and uploaded
☐ TestFlight tested with real people
☐ Screenshots for required sizes
☐ Name, subtitle, description, keywords
☐ Support URL + privacy policy URL
☐ Category, age rating, price, countries
☐ App Privacy ("nutrition label") answered honestly
☐ Demo account + review notes (if login needed)
☐ Build selected → Submit for Review

AFTER
☐ Reply to reviews
☐ Check crash reports
☐ Plan the next update 🚀
```

---

## 🏋️ Practice

(You can do 1–4 without paying.)

1. Make a privacy policy page for one of your apps (a simple web page).
2. Write the App Store **name**, **subtitle**, **description** and **keywords** for your To-Do app.
3. Take 5 nice **screenshots** of your app in the Simulator (with good sample data).
4. Go through the "Before upload" checklist for your Weather or Notes app. Fix anything missing.
5. (With a paid account) Archive and upload a build. Install it with **TestFlight**.
6. (With a paid account) Submit your app for review! 🚀

---

## 🧠 Remember

- Join the **Apple Developer Program** to publish.
- Prepare: icon, version/build, privacy texts, real-device testing, privacy policy.
- **App Store Connect**: create the app (name, Bundle ID, SKU).
- Xcode: **Any iOS Device** → **Product → Archive** → **Distribute App** → upload.
- **TestFlight** to test with real people.
- Store page: screenshots, description, keywords, privacy label, age rating, price.
- **Submit for Review**. Rejected? Read why, fix, resubmit — it's normal!
- Every new upload needs a **higher build number**.

---

## 🎓 Congratulations — you finished the tutorial! 🎉🏆

Look how far you've come:

| Part | You learned |
|---|---|
| **1** | What programming is, running Swift in the browser |
| **2** | All the Swift basics: variables, types, decisions, loops, collections, optionals, functions, closures |
| **3** | Structs, classes, enums, protocols, extensions, errors, generics, async/await |
| **4** | Xcode: every area, Simulator, **configurations**, targets, schemes, signing, debugging |
| **5** | SwiftUI: layouts, controls, state, lists, navigation, sheets, data flow, colors, animations |
| **6** | Saving data, networking, JSON, images, three real apps, testing, and the App Store |

You started not knowing what a variable was. Now you can build and publish a real iPhone app. **That's amazing.** 💙

### What next?

- 🔨 **Build your own app idea** — the best way to learn is to make something you care about.
- 📚 Read **Apple's documentation** and watch **WWDC videos** (Apple's yearly developer conference — free online).
- 🧩 Learn more: **Charts**, **MapKit** (maps), **WidgetKit** (widgets), **CoreLocation** (location), **notifications**, **accessibility**.
- 🤝 Join a community: Swift forums, local meetups, coding clubs.
- 🔁 Come back to any chapter when you need it — this tutorial is your reference.

Keep coding, keep making mistakes, keep learning. 🚀

**Happy coding!** 👩‍💻👨‍💻

---

⬅️ **Back:** [Chapter 64 — Testing Your App](64-testing.md)
📖 **Extra:** [Glossary](../extras/glossary.md) • [Common Errors and How to Fix Them](../extras/common-errors.md)
🏠 **Home:** [Table of Contents](../README.md)
