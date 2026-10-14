# Chapter 100 – Putting your app on the internet

[⬅ Previous chapter](99-docker.md) | [Table of Contents](../README.md)

---

## 🎯 Goal

The **last** chapter! 🎆 Your Library app is built, secured, tested, packed into a jar and into a Docker box. Only one step is left: putting it **on the internet**, so anyone in the world can use it. 🌍

At the end of this chapter you will know:

- Where an app can **live** on the internet: the main kinds of **hosting** 🏠
- How to put the app on a **server** with Docker Compose, step by step 🖥️
- What a **domain** and **DNS** are 🪧
- How to get **HTTPS** 🔒 — automatically and for free
- How to **update** the app, make **backups**, and watch its **health** 🩺
- A **checklist** before going live ✅
- What to learn **next** 🚀

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Hosting** | Renting a place on the internet where your app can run. 🏠 |
| **Server** / **VPS** | A computer in a data center that's always on. A **VPS** ("virtual private server") is a **piece** of a big computer, rented just for you. 🖥️ |
| **PaaS** | "Platform as a Service": a company runs your app **for** you — you just give them the code or the image. ☁️ |
| **SSH** | A safe way to type commands on a **faraway** computer. 🔑 |
| **Domain** | A **name** for your server, like `mylibrary.com`. 🪧 |
| **DNS** | The internet's **phone book**: it turns a domain name into the server's **IP address**. 📖 |
| **IP address** | The **number** of a computer on the internet, like `203.0.113.42`. |
| **Reverse proxy** | A program in **front** of your app that takes all requests first — for example, to add HTTPS. 🚪 |
| **Certificate** | A digital "ID card" that proves a website is really who it says it is — needed for HTTPS. 🪪 |
| **Backup** | A copy of your data, kept somewhere **safe**, in case something goes wrong. 💾 |

---

## 📖 Story: Opening a real shop 🏪

Sara has baked cookies at home for a year 🍪 — for family and friends. Now she wants to open a **real shop**. What does she need?

1. 🏠 A **place**: rent a shop on a street — or a stand inside a big market hall that handles the electricity and cleaning for her.
2. 🪧 A **sign** with a name, so people can **find** her: "Sara's Cookies".
3. 🔒 A **lock** on the door and a **safe** for the money.
4. 📋 A **plan** for every day: open in the morning, check the oven, count the money, buy new flour.

Putting an app on the internet is the **same**:

| Shop 🏪 | App 🌍 |
|---|---|
| Rent a shop | Rent a **server** (VPS) |
| A stand in a market hall | A **PaaS** that runs it for you |
| The sign with the name | A **domain** + **DNS** |
| Lock and safe | **HTTPS**, secrets, security rules |
| Daily plan | **Updates**, **backups**, **health checks** |

---

## 🏠 Part 1: Where can an app live?

There are three main kinds of homes for an app:

| Kind | You do | They do | Good for |
|---|---|---|---|
| ☁️ **PaaS** (Platform as a Service) | Give them your Docker image (or code) and the settings | Servers, HTTPS, restarts, often the database | Starting out, small apps — **easiest** |
| 🖥️ **VPS** (your own small server) | Everything: install Docker, start containers, HTTPS, backups | Only the computer and the internet connection | Learning how it **really** works, full control |
| 🏢 **Big cloud** (with Kubernetes and friends) | Lots of setup | Huge, automatic scaling | Big companies, millions of users |

Many companies offer PaaS and VPS hosting — some with a small **free** plan for learning. Their websites and buttons change often, so we won't click through one particular company here. Instead, we'll learn the steps that are the **same everywhere**. 🧭

### ☁️ Going live with a PaaS — the idea

Almost every PaaS works like this:

1. Put your code on **GitHub** (Chapter 42).
2. Create a new "app" or "service" at the PaaS and connect it to your GitHub repository.
3. Tell it to use your **`Dockerfile`** (the multi-stage one from Chapter 99 is perfect!).
4. Add a **PostgreSQL** database (most PaaS offer one with a click) and copy its address, user and password.
5. Set the **environment variables**: `SPRING_PROFILES_ACTIVE=prod`, `DB_URL`, `DB_USERNAME`, `DB_PASSWORD`, `JWT_SECRET`, `LIBRARIAN_PASSWORD`.
6. Tell it the app listens on port **8080**, and that the health check is **`/actuator/health`** (Chapter 94). 🩺
7. Click **Deploy**. The PaaS builds the image, starts the container, and gives you an address with **HTTPS** — like `https://library-sara.some-paas.app`. 🎉

That's it! Everything you built in this book fits **exactly**: Docker, profiles, environment variables, the health endpoint. 🧩

---

## 🖥️ Part 2: Going live on your own server

Let's do it the "real" way on a **VPS**, so you understand every step. You need: a VPS with **Ubuntu Linux** (rented from any hosting company), its **IP address**, and a login.

### Step 1: Connect with SSH 🔑

```bash
ssh root@203.0.113.42
```

| Part | Meaning |
|---|---|
| `ssh` | "Open a safe connection to a faraway computer." |
| `root@203.0.113.42` | User `root` (the boss of the server) at the server's IP address. (Use **your** server's IP!) |

Now every command you type runs on the **server**. 🖥️🌍

### Step 2: Install Docker 🐳

Docker's website has an install script for Ubuntu:

```bash
curl -fsSL https://get.docker.com | sh
docker --version
```

### Step 3: Get the code 📥

```bash
git clone https://github.com/your-name/library.git
cd library
```

### Step 4: Create the secrets 🔒

The `.env` file is **not** in Git (Chapter 99) — so we make it **on the server**:

```bash
nano .env
```

(**nano** is a simple text editor in the terminal. Type, then **Ctrl+O** to save, **Enter**, **Ctrl+X** to leave.)

```
DB_PASSWORD=a-really-long-random-database-password
JWT_SECRET=another-really-long-random-secret-with-more-than-32-characters
LIBRARIAN_PASSWORD=Novak-Strong-Pass-2026
```

💡 Good random secrets: `openssl rand -base64 48` makes one for you.

### Step 5: Start everything 🚀

With the **multi-stage** Dockerfile (Chapter 99's mini project), the server doesn't even need Java:

```bash
docker compose up -d --build
docker compose logs -f app
```

When you see `Started LibraryApplication`, press **Ctrl+C** (that only stops **watching** the log). Open **`http://203.0.113.42:8080/api/books`** in your browser... 📚 **Your app is on the internet!** 🌍🎉

But wait — three problems: 😟

1. Nobody remembers `203.0.113.42`. → a **domain**.
2. It's **`http://`** — passwords and tokens travel **readable** (Chapter 80!). → **HTTPS**.
3. `:8080` looks strange. → a **reverse proxy** on the normal ports 80 and 443.

---

## 🪧 Part 3: A domain name

Buy a domain (like `mylibrary.com`) from a **domain registrar** — a company that sells names (often a few euros or dollars per year). Then, in their **DNS** settings, add a record:

| Type | Name | Value |
|---|---|---|
| `A` | `library` | `203.0.113.42` |

| Part | Meaning |
|---|---|
| `A` record | "**A**ddress": this name → this IP address. |
| `library` | The part **before** your domain → `library.mylibrary.com`. (Use `@` for `mylibrary.com` itself.) |

After a few minutes (sometimes a few hours), the internet's **phone book** 📖 knows: `library.mylibrary.com` → `203.0.113.42`. Check with:

```bash
ping library.mylibrary.com
```

---

## 🔒 Part 4: HTTPS — with a reverse proxy

We put a small program **in front** of our app: **Caddy**. It's a web server that gets HTTPS **certificates** automatically and for **free** (from a project called **Let's Encrypt**) — and renews them by itself. 🪄

```
 Browser ──https://library.mylibrary.com──► 🚪 Caddy (ports 80 + 443, does HTTPS)
                                                │  plain http, inside Docker only
                                                ▼
                                            📚 app:8080 ──► 🐘 db:5432
```

Create a file **`Caddyfile`** next to `compose.yaml`:

```
library.mylibrary.com {
    reverse_proxy app:8080
}
```

| Line | Meaning |
|---|---|
| `library.mylibrary.com {` | "For requests to **this** name..." Caddy sees the name and gets a certificate for it **automatically**. 🪪 |
| `reverse_proxy app:8080` | "...pass them on to the service `app`, port 8080." (Service names again — Chapter 99!) |

Add Caddy to **`compose.yaml`**, and **remove** the `ports:` from `app` (only Caddy should talk to the outside world now):

```yaml
services:
  db:
    # ... as before ...

  app:
    build: .
    environment:
      SPRING_PROFILES_ACTIVE: prod
      SERVER_FORWARD_HEADERS_STRATEGY: framework
      DB_URL: jdbc:postgresql://db:5432/library
      DB_USERNAME: library
      DB_PASSWORD: ${DB_PASSWORD}
      JWT_SECRET: ${JWT_SECRET}
      LIBRARIAN_PASSWORD: ${LIBRARIAN_PASSWORD}
    depends_on:
      db:
        condition: service_healthy

  caddy:
    image: caddy:2
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy-data:/data
    depends_on:
      - app

volumes:
  library-data:
  caddy-data:
```

| Part | Meaning |
|---|---|
| (no `ports:` on `app`) | ⭐ The app is **only** reachable **through** Caddy. Nobody can skip HTTPS. 🔒 |
| `SERVER_FORWARD_HEADERS_STRATEGY: framework` | The app sees requests from Caddy as plain `http`. This setting tells Spring: "**trust** the headers Caddy adds (like `X-Forwarded-Proto: https`) to know the **real** address" — so links like the `Location` header say `https://...`. |
| `caddy:2` | The official Caddy image. |
| `"80:80"`, `"443:443"` | The normal ports for `http` and `https`. (Caddy sends `http` visitors to `https` automatically.) |
| `./Caddyfile:/etc/caddy/Caddyfile` | Put **our** Caddyfile into the container. |
| `caddy-data:/data` | A volume for the **certificates**, so they're kept after restarts. |

```bash
docker compose up -d --build
```

Open **https://library.mylibrary.com/api/books** — with a 🔒 lock in the address bar! 🎉🎉🎉

Your Library app is **live**, on its own name, with HTTPS, a real database, real secrets, and the security from Part 10. **You did it.** 🏆

---

## 🔄 Part 5: Living with a live app

Going live is not the end — it's the **start**. 🌱 Here's the "daily plan" of the shop:

### 🔄 Updates

You fixed a bug and pushed it to GitHub. On the server:

```bash
cd library
git pull
docker compose up -d --build
```

Compose rebuilds the app image and **replaces** the app container. The database (and its volume) keep running. A few seconds of "not available" — fine for a school library. (Big apps use tricks for **zero** downtime.)

⭐ And **before** every update: `./mvnw test` on your own computer — 🟢 or no update! (Part 11.)

### 💾 Backups

Servers break. People make mistakes (`docker compose down -v`! 😱). Make **backups** of the database:

```bash
docker compose exec db pg_dump -U library library > backup-2026-10-14.sql
```

| Part | Meaning |
|---|---|
| `docker compose exec db ...` | Run a command **inside** the `db` container. |
| `pg_dump -U library library` | PostgreSQL's tool to write the **whole** database as SQL (Chapter 68!). |
| `> backup-2026-10-14.sql` | Save it into a file. |

Do this **regularly** — a scheduled job is perfect (on the server, or like Chapter 91) — and keep copies **somewhere else** (not only on the same server!). 💾💾

A backup you've never **tried to restore** is just a hope. 🤞 Test it now and then!

### 🩺 Health and logs

- **Health**: many free "uptime" services can check `https://library.mylibrary.com/actuator/health` every minute, and send you an email when it's not `UP` (Chapter 94). 🚨
- **Logs**: `docker compose logs --tail 100 app` shows the last 100 lines (Chapter 88). Look at them when something feels strange. 🕵️

---

## ✅ Part 6: The go-live checklist

Before you tell the world your app's address, check **every** line:

| ✅ | Check | Chapter |
|---|---|---|
| ☐ | All tests are green (`./mvnw test`) | 84–87, 97 |
| ☐ | **HTTPS** only — no plain `http` to the app | 80, 100 |
| ☐ | All secrets come from **outside** (`.env` / PaaS settings), none in Git | 77, 83, 98, 99 |
| ☐ | `JWT_SECRET` is **long and random**, not the learning one | 83 |
| ☐ | The first librarian/admin has a **strong** password | 82, 97 |
| ☐ | The **H2 Console** is off (or H2 isn't used at all) | 69, 80 |
| ☐ | **Swagger UI** is off — or on purpose public | 93 |
| ☐ | **Actuator** shows only `health` publicly | 94 |
| ☐ | No passwords or tokens in the **logs** | 88 |
| ☐ | Upload limits are set, uploads are checked | 92 |
| ☐ | The database has a **volume** and **backups** | 99, 100 |
| ☐ | The health endpoint is watched | 94, 100 |
| ☐ | `ddl-auto` is safe for real data (`update` or — even better — `validate` with a migration tool) | 73 |

💡 About that last line: on a real server, letting Hibernate change tables by itself (`update`) is risky. Professionals use **database migration** tools like **Flyway**: you write each table change as a small numbered SQL file (`V1__create_books.sql`, `V2__add_reservations.sql`...), and Flyway runs them in order. A great **next** topic! 🚀

---

## 💻 Mini project: Your own go-live plan 📝

Take the **school app** from Parts 7–12 and write a go-live plan for it, **like an engineer**:

1. Which hosting would you choose — PaaS or VPS? Why?
2. Which **environment variables** does it need? (Look through all its `${...}` settings!)
3. Which items of the checklist are **not** done yet in the school app? What would you change?

<details>
<summary>Click to see one possible answer</summary>

1. A **PaaS** — it's a learning project, and the PaaS gives HTTPS, restarts and a database with a few clicks. (A VPS is a great **second** step, to learn more.)
2. `SPRING_PROFILES_ACTIVE=prod`, `DB_URL` / `DB_USERNAME` / `DB_PASSWORD` (Chapter 77's prod profile), `JWT_SECRET` (Chapter 83), `ADMIN_PASSWORD` (Chapter 82). Plus maybe `SCHOOL_HOMEWORK_BASE_URL` (Chapter 90) and `SCHOOL_UPLOAD_DIR` (Chapter 92 — with a **volume** for the photos!).
3. For example:
   - The **H2 Console** is on (`spring.h2.console.enabled=true`) and `permitAll()` — turn it off in `prod`!
   - `UserLoader` creates a `teacher` with the password `secret123` **from the code** — remove it in `prod`, or use a variable.
   - `management.endpoint.health.show-details=always` → `when-authorized`.
   - Uploaded photos live in a folder inside the container → they'd be lost; they need a **volume**.
   - `JWT_SECRET` and `ADMIN_PASSWORD` have learning **defaults** — the `prod` profile must override them **without** defaults (Chapter 98).
   - Swagger UI is public — switch it off in `prod`.

If you found at least four of these, you think like someone who runs real apps. 🏆

</details>

---

## ✋ Try it yourself

1. Run the **whole** Caddy setup on your own computer: use `localhost` instead of a domain in the `Caddyfile`. (Caddy makes a **local** certificate — your browser will warn, because it's not from Let's Encrypt.)
2. Make a backup with `pg_dump`, delete a book through the API, then restore the backup with `docker compose exec -T db psql -U library library < backup.sql`. Is the book back? (Hint: you may need to drop the old tables first — try it on a **test** database!)
3. Find out what **CORS** is. Why will you need it when a **web page** on another domain (for example, a Blazor app 😉) calls your API?

<details>
<summary>Click to see the answers</summary>

1. ```
   localhost {
       reverse_proxy app:8080
   }
   ```
   Then `https://localhost/api/books` works — with a browser warning about the certificate. (That's expected: it's only trusted on your computer.)
2. Restoring a full dump into a database that **already** has the same tables gives errors ("relation already exists"). In real life, you restore into an **empty** database. That's exactly why you should **practise** restoring before you need it! 🧯
3. **CORS** ("Cross-Origin Resource Sharing") is a browser rule: JavaScript on a page from `https://app.mylibrary.com` may **not** call `https://api.mylibrary.com` unless the API **allows** it with special headers. In Spring, you allow it with a `CorsConfigurationSource` bean and `.cors(Customizer.withDefaults())` in the `SecurityFilterChain`. You'll meet it in the **Blazor** book, when a web page talks to your API! 🌐

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Opening the app port to the world

`ports: "8080:8080"` on `app` **and** Caddy → people can skip HTTPS via `http://203.0.113.42:8080`. **Fix:** Only the reverse proxy has `ports:`.

### Mistake 2: The `.env` file in Git

**Fix:** `.gitignore` — and if it ever **was** committed: change **all** the secrets. Git never forgets! 🐘

### Mistake 3: No backups

"It won't happen to me." It will. 💥 **Fix:** Automatic backups, stored somewhere else, and a tested restore.

### Mistake 4: Updating without testing

**Fix:** `./mvnw test` → 🟢 → then update.

### Mistake 5: Using the learning passwords

`admin12345`, `secret123`, `librarian123` are in **this book** — so everyone knows them! 😅 **Fix:** Strong, random secrets for every real app.

---

## ✅ Summary

- Apps live on a **PaaS** ☁️ (easiest), a **VPS** 🖥️ (full control) or a **big cloud** 🏢.
- **PaaS**: connect GitHub, use your Dockerfile, add PostgreSQL, set environment variables, health check `/actuator/health`, deploy.
- **VPS**: `ssh` → install Docker → `git clone` → create `.env` → `docker compose up -d --build`.
- **Domain** + **DNS `A` record** 🪧 → the name points to your server's IP.
- **HTTPS** 🔒 with a **reverse proxy** like **Caddy**: automatic, free certificates. Only the proxy is open to the world. `SERVER_FORWARD_HEADERS_STRATEGY=framework` for the app.
- Live life: **updates** (`git pull` + `docker compose up -d --build`, tests first!), **backups** (`pg_dump`, tested!), **health** checks and **logs**.
- Go through the **checklist** ✅ before going live.

---

## ❓ Quiz

1. What's the difference between a PaaS and a VPS?
2. What does DNS do?
3. Why do we put Caddy in front of our app?
4. Why does the `app` service have no `ports:` anymore?
5. How do you update the app on the server?
6. Why should backups be stored somewhere else, and tested?
7. Name three items from the go-live checklist.

<details>
<summary>Click to see the answers</summary>

1. On a PaaS, a company runs your app for you (servers, HTTPS, restarts). On a VPS, you rent a computer and do everything yourself.
2. It turns a domain name (like `library.mylibrary.com`) into the server's IP address — the internet's phone book.
3. To get HTTPS automatically (free certificates), and to have one door (ports 80 and 443) in front of the app.
4. So nobody can reach the app directly with plain `http` — only through Caddy and HTTPS.
5. `git pull`, then `docker compose up -d --build` (after the tests were green).
6. If the server breaks, a backup on the same server is gone too. And an untested backup may not work when you need it.
7. For example: tests green, HTTPS only, secrets from outside, strong admin password, H2 Console off, Actuator limited, backups, health checks.

</details>

---

## 🎓 The book is complete! 🎉🎉🎉

**Congratulations!** 🏆 You started this book not knowing what a variable is. Look where you are now:

```
 Part 1  ✅ Getting ready            📦 Java, IntelliJ, Hello World
 Part 2  ✅ Java basics              🧮 variables, if, loops, methods
 Part 3  ✅ Objects                  🍪 classes, inheritance, interfaces, records
 Part 4  ✅ More Java                🧺 lists, maps, lambdas, streams, Optional
 Part 5  ✅ Tools                    🛠️ Maven, pom.xml, Git
 Part 6  ✅ How the web works        🌐 HTTP, JSON, REST, curl
 Part 7  ✅ Spring Boot basics       🌱 beans, dependency injection, properties
 Part 8  ✅ REST APIs                🎮 controllers, DTOs, validation, errors
 Part 9  ✅ Databases                🗄️ SQL, JPA, relationships, transactions
 Part 10 ✅ Security                 🔐 users, BCrypt, roles, JWT
 Part 11 ✅ Testing                  🧪 JUnit, Mockito, slices, integration
 Part 12 ✅ Useful extras            🧰 logging, Thymeleaf, scheduling, Swagger...
 Part 13 ✅ Final project            🏆 the Library app — built, tested, live!
```

You built **two** real applications. You know how to **plan**, **build**, **secure**, **test**, **pack** and **ship** software. That's what professional backend developers do every day. 💪

### 🚀 What's next?

A few great topics for your next steps:

| Topic | Why |
|---|---|
| **Flyway** | Safe database changes in production (Part 6 of this chapter). |
| **Optimistic locking** (`@Version`) | Two people borrowing the last copy at once (Chapter 96). |
| **Testcontainers** | Tests with a **real** PostgreSQL in Docker. |
| **Caching** (`@Cacheable`) | Make slow things fast. |
| **Messaging** (Kafka, RabbitMQ) | Apps that talk to each other with messages. |
| **A frontend!** | A beautiful user interface for your API. 🎨 |

### 🎨 Coming next: the Blazor book!

Our Library API has no **face** yet — people use it with curl and Swagger. 😅 In the **Blazor** book, you'll build **web pages** — with buttons, forms and lists — that talk to APIs like the ones you built here. Same easy steps, same little stories, a whole new world. 🌍✨

Thank you for learning with this book. Now go and build something **amazing**! 🚀👩‍💻👨‍💻

---

[⬅ Previous chapter](99-docker.md) | [Table of Contents](../README.md)
