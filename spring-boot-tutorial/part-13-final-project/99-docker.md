# Chapter 99 – Docker basics

[⬅ Previous chapter](98-making-a-jar.md) | [Table of Contents](../README.md) | [Next chapter ➡](100-going-live.md)

---

## 🎯 Goal

Our jar needs **Java 25** on the server. And a **PostgreSQL** database. And the right settings. 😓 "But it works on **my** computer!" — every programmer has said that, when the app didn't work on another one. 🤷

**Docker** puts your app **and everything it needs** into a box that runs the **same** way everywhere. 🐳📦

At the end of this chapter you will know:

- What **images** and **containers** are 🐳
- How to write a **`Dockerfile`** for the Library app
- How to **build** an image and **run** a container
- How to start **PostgreSQL** with **one** command
- How to start the app **and** the database together with **Docker Compose** 🎼
- Where to put **secrets** 🔒

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Docker** | A tool that runs apps in **containers**. 🐳 |
| **Image** | A **frozen** package: an operating system (a small Linux), Java, your jar, and how to start it. Like a **recipe + all ingredients**, frozen. 🧊 |
| **Container** | A **running** copy of an image. You can start many containers from one image. 📦 |
| **Dockerfile** | The **recipe** for building an image, step by step. 📜 |
| **Base image** | The image you **start** from — for us: "Linux + Java 25". |
| **Port mapping** | Connecting a port of **your** computer to a port **inside** the container: `-p 8080:8080`. 🔌 |
| **Volume** | A storage place **outside** the container, so data survives when the container is deleted. 💾 |
| **Docker Compose** | A tool that starts **several** containers together, from one file. 🎼 |
| **Registry** | An online "library" of images, like **Docker Hub**. 📚 |

---

## 📖 Story: Shipping containers 🚢

Long ago, ships carried goods in sacks, barrels and boxes of every size. 🛢️📦🧺 Loading a ship took **days**, things broke, and every port needed different cranes.

Then someone invented the **shipping container** 🚢: a **standard** steel box. Inside: anything — bananas, cars, toys. Outside: always the **same** size and shape. Now **every** ship, train and truck in the world can carry **every** container, and the cranes don't care what's inside. 🎉

Docker does the same for software:

| Shipping 🚢 | Docker 🐳 |
|---|---|
| The standard steel box | A **container** |
| The packing list + goods | An **image** |
| Bananas, cars, toys | Java apps, Python apps, databases... |
| Any ship, train, truck | Any computer with Docker: your laptop, a server, the cloud ☁️ |

"Works on my computer" → "works in the box" → **works everywhere**. 📦✅

### 🤔 Image vs container

```
 📜 Dockerfile ──docker build──► 🧊 Image ──docker run──► 📦 Container (running!)
    (recipe)                     (frozen cake)            📦 Container (another one)
                                                          📦 ...
```

Like a **cookie cutter** and **cookies** (Chapter 18!): the image is the cutter, containers are the cookies. 🍪

---

## 🛠️ Part 1: Install Docker

1. Download **Docker Desktop** from **https://www.docker.com/products/docker-desktop** (Windows, Mac or Linux).
2. Install it and start it. (On Windows, it may ask to install **WSL 2** — say yes and restart.)
3. Open a terminal and check:

```bash
docker --version
```

```
Docker version 28.x.x, build ...
```

4. Your very first container:

```bash
docker run hello-world
```

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

🎉 Docker downloaded a tiny image from **Docker Hub**, made a container from it, ran it — and the container printed this message.

---

## 📜 Part 2: A Dockerfile for the library

In the **`library`** project folder (next to `pom.xml`), create a file called exactly **`Dockerfile`** (no extension!):

```dockerfile
FROM eclipse-temurin:25-jre
WORKDIR /app
COPY target/library-1.0.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Five lines! Each one is a **step** of the recipe:

| Line | Meaning |
|---|---|
| `FROM eclipse-temurin:25-jre` | ⭐ Start from a **base image**: a small Linux with **Java 25** already installed. ("Temurin" is a free Java made by the Eclipse foundation. **JRE** = only what's needed to **run** Java, not to build it — smaller!) |
| `WORKDIR /app` | "Inside the box, work in the folder `/app`." (It's made if it doesn't exist.) |
| `COPY target/library-1.0.0.jar app.jar` | ⭐ Copy **our** jar (from Chapter 98) into the box, and call it `app.jar`. |
| `EXPOSE 8080` | A **note**: "this app listens on port 8080". (It doesn't open anything by itself — that's `-p`, below.) |
| `ENTRYPOINT ["java", "-jar", "app.jar"]` | ⭐ The command to run when a container **starts**: our good old `java -jar`! |

And a **`.dockerignore`** file (like `.gitignore`, Chapter 42) — so Docker doesn't send unneeded folders into the build:

```
data/
logs/
uploads/
.idea/
.git/
```

---

## 🧊 Part 3: Build the image

First the jar (Chapter 98), then the image:

```bash
./mvnw clean package
docker build -t library:1.0.0 .
```

| Part | Meaning |
|---|---|
| `docker build` | "Follow the `Dockerfile` and make an image." |
| `-t library:1.0.0` | The image's **name** (`library`) and **tag** (`1.0.0` — a version label 🏷️). |
| `.` | ⚠️ Don't forget the dot! It means "the Dockerfile and files are **here**, in this folder". |

The first build downloads the Java base image (a few hundred MB — once!). Then:

```
 => [1/3] FROM docker.io/library/eclipse-temurin:25-jre
 => [2/3] WORKDIR /app
 => [3/3] COPY target/library-1.0.0.jar app.jar
 => exporting to image
 => => naming to docker.io/library/library:1.0.0
```

Check your images:

```bash
docker images
```

```
REPOSITORY   TAG      IMAGE ID       CREATED          SIZE
library      1.0.0    3f2a9c1d8e7b   10 seconds ago   ~350MB
```

🧊 Your app is frozen into an image — Linux + Java + jar, all in one.

---

## 📦 Part 4: Run a container

```bash
docker run -p 8080:8080 --name library library:1.0.0
```

| Part | Meaning |
|---|---|
| `docker run` | Make a **container** from an image and start it. |
| `-p 8080:8080` | ⭐ **Port mapping** 🔌: "port 8080 of **my** computer → port 8080 **inside** the box". Without it, the app runs, but nobody can reach it! (The left number is yours: `-p 9000:8080` would make it `localhost:9000`.) |
| `--name library` | A friendly name for the container. |
| `library:1.0.0` | Which image. |

The Spring Boot log appears — from **inside** the box! 🐳 In another terminal: `curl http://localhost:8080/api/books` → the books. 📚

### 🎮 Useful Docker commands

| Command | Does |
|---|---|
| `docker ps` | Show **running** containers. |
| `docker ps -a` | Show **all** containers, also stopped ones. |
| `docker logs library` | Show the log of the container `library`. (`-f` = keep following it.) |
| `docker stop library` | Stop it nicely (graceful shutdown, Chapter 98). |
| `docker start library` | Start it again. |
| `docker rm library` | Delete the (stopped) container. |
| `docker run -d ...` | **Detached**: run in the background, give the terminal back. |

🤔 Where's the data? Our app uses the H2 **file** `./data/library` — **inside** the container. Delete the container (`docker rm`) → the data is **gone**! 😱 Containers are meant to be **thrown away**. Real data belongs in a **database** with a **volume**. Let's do that!

---

## 🐘 Part 5: PostgreSQL in one command

Remember installing PostgreSQL in Chapter 77? With Docker:

```bash
docker run -d --name library-db \
  -e POSTGRES_DB=library \
  -e POSTGRES_USER=library \
  -e POSTGRES_PASSWORD=change-me \
  -p 5432:5432 \
  -v library-data:/var/lib/postgresql/data \
  postgres:17
```

| Part | Meaning |
|---|---|
| `-d` | In the background. |
| `-e POSTGRES_DB=library` | ⭐ `-e` sets an **environment variable** inside the container. The official PostgreSQL image reads these to create a database, a user and a password. |
| `-v library-data:/var/lib/postgresql/data` | ⭐ A **volume** 💾 called `library-data` for the database files. Delete the container → the volume (and your data) **stays**. |
| `postgres:17` | The official PostgreSQL 17 image from Docker Hub. |

That's a whole database server, in **seconds**. 🤯 (If you already have PostgreSQL installed on port 5432, use `-p 5433:5432` instead.)

---

## 🎼 Part 6: Docker Compose — everything together

Starting two containers with long commands, in the right order, with the right settings... 😩 **Docker Compose** does it from **one** file.

Create **`compose.yaml`** next to the `Dockerfile`:

```yaml
services:
  db:
    image: postgres:17
    environment:
      POSTGRES_DB: library
      POSTGRES_USER: library
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - library-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U library -d library"]
      interval: 5s
      retries: 10

  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      SPRING_PROFILES_ACTIVE: prod
      DB_URL: jdbc:postgresql://db:5432/library
      DB_USERNAME: library
      DB_PASSWORD: ${DB_PASSWORD}
      JWT_SECRET: ${JWT_SECRET}
      LIBRARIAN_PASSWORD: ${LIBRARIAN_PASSWORD}
    depends_on:
      db:
        condition: service_healthy

volumes:
  library-data:
```

This is **YAML** — a settings format where **indentation** (spaces!) shows what belongs to what. 📏

| Part | Meaning |
|---|---|
| `services:` | The containers: **`db`** and **`app`**. |
| `image: postgres:17` | `db` uses a ready-made image. |
| `build: .` | ⭐ `app` is **built** from **our** `Dockerfile` in this folder. |
| `${DB_PASSWORD}` | Taken from **your** environment — or from a **`.env`** file (below). |
| `healthcheck:` | "Every 5 seconds, ask PostgreSQL `pg_isready` — is it ready?" |
| `DB_URL: jdbc:postgresql://db:5432/library` | ⭐ Look: the host is **`db`** — the **service name**! Inside Compose, containers find each other **by name**. 🏷️ |
| `depends_on: db: condition: service_healthy` | ⭐ "Start `app` only **after** `db` is **healthy**." Otherwise the app might start first and fail to connect. |
| `volumes: library-data:` | The volume for the database, so data survives. 💾 |

### 🔒 The `.env` file

Compose automatically reads a file called **`.env`** in the same folder:

```
DB_PASSWORD=change-me-to-something-long
JWT_SECRET=a-long-random-production-secret-at-least-32-characters
LIBRARIAN_PASSWORD=Novak-Strong-Pass-2026
```

⚠️ **Add `.env` to `.gitignore` right now!** It holds real secrets. 🔒 (A common trick: commit a file **`.env.example`** with the **names** but fake values, so others know what to fill in.)

### 🚀 Start everything

```bash
./mvnw clean package
docker compose up --build
```

| Part | Meaning |
|---|---|
| `docker compose up` | Start **all** services from `compose.yaml`. |
| `--build` | Build our app image first (fresh jar → fresh image). |

You'll see the logs of **both** containers, with their names in front:

```
db-1   | ... database system is ready to accept connections
app-1  | ... The following 1 profile is active: "prod"
app-1  | ... Database JDBC URL [jdbc:postgresql://db:5432/library]
app-1  | ... Added the librarian novak
app-1  | ... Added 3 books
app-1  | ... Started LibraryApplication in 6.1 seconds
```

🎉 The library, with a real PostgreSQL database, the `prod` profile and real secrets — started with **one** command! Test: `curl http://localhost:8080/api/books`. 📚🐘

| Command | Does |
|---|---|
| `docker compose up -d` | Start in the background. |
| `docker compose logs -f app` | Follow the app's log. |
| `docker compose down` | Stop and remove the containers (the **volume** stays!). |
| `docker compose down -v` | ⚠️ ...and **delete** the volume — all data gone! |

Stop with `docker compose down`, start again with `docker compose up -d` → your books, users and loans are **still there**. 💾 That's the volume.

---

## 💻 Mini project: Build the jar inside Docker 🏭🐳

Right now, you must run `./mvnw clean package` **before** `docker build`. What if the server has no Java and no Maven at all? Let Docker build the jar **too**, with a **multi-stage** Dockerfile:

- **Stage 1** ("build"): start from `eclipse-temurin:25-jdk` (the **JDK** can build Java), copy the project, run `./mvnw clean package`.
- **Stage 2**: start from `eclipse-temurin:25-jre` and copy **only** the jar from stage 1.

<details>
<summary>Click to see the answer</summary>

**`Dockerfile`**

```dockerfile
# Stage 1: build the jar
FROM eclipse-temurin:25-jdk AS build
WORKDIR /workspace
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN ./mvnw dependency:go-offline
COPY src src
RUN ./mvnw clean package

# Stage 2: only what's needed to run
FROM eclipse-temurin:25-jre
WORKDIR /app
COPY --from=build /workspace/target/library-1.0.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

| Code | Meaning |
|---|---|
| `FROM ... AS build` | The first stage gets a **name**: `build`. |
| `RUN ...` | Run a command **while building** the image. |
| `COPY mvnw pom.xml ./` then `RUN ./mvnw dependency:go-offline` | ⭐ Download all libraries **first**. Docker **remembers** (caches) each step — if only your Java code changes, the slow download step is **reused**. 🚀 |
| `COPY src src` then `RUN ./mvnw clean package` | Copy the code and build the jar (with tests!). |
| `COPY --from=build ...` | ⭐ Take **only** the jar from the `build` stage. The JDK, Maven and the source code are **left behind** → a small final image. 🎒 |

Now `docker compose up --build` works on a computer with **only** Docker — no Java, no Maven. 🐳✨ (If `./mvnw` says "Permission denied" on Linux, add `RUN chmod +x mvnw` after copying it.)

💡 Spring Boot can even make an image **without** a Dockerfile: `./mvnw spring-boot:build-image`. It uses "buildpacks" to choose everything for you. Worth trying!

</details>

---

## ✋ Try it yourself

1. Run the library image **twice**, on ports 8080 and 8081 (`-p 8081:8080 --name library2`). Do they share data?
2. Run `docker exec -it library-db psql -U library` and type `SELECT title, available_copies FROM books;`. (Type `\q` to leave.)
3. Change `library.loan.days` for the Compose app **without** rebuilding. Where would you put it?

<details>
<summary>Click to see the answers</summary>

1. Both run. With the H2 file inside each container, **each** has its **own** data — they don't share. With Compose and PostgreSQL, both could point to the **same** database.
2. `docker exec` runs a command **inside** a running container. `psql` is PostgreSQL's command-line tool — you see the three books with their copies. 🐘
3. Add `LIBRARY_LOAN_DAYS: 21` under `environment:` of `app` in `compose.yaml`, then `docker compose up -d`. Environment variables beat `application.properties` (Chapter 98). 🥈

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Forgetting the `.` in `docker build`

`docker build -t library:1.0.0` → *"requires 1 argument"*. **Fix:** `docker build -t library:1.0.0 .`

### Mistake 2: Forgetting `-p`

The app runs, but `localhost:8080` doesn't answer. **Fix:** `-p 8080:8080`.

### Mistake 3: `localhost` inside a container

`DB_URL=jdbc:postgresql://localhost:5432/library` inside the app container → *"Connection refused"*. Inside a container, `localhost` means **the container itself**, not your computer! **Fix:** In Compose, use the **service name**: `db`.

### Mistake 4: The jar is old

You changed code, but forgot `./mvnw clean package` before `docker build` → the image has the **old** jar. **Fix:** Build the jar first — or use the multi-stage Dockerfile.

### Mistake 5: Secrets in `compose.yaml` or the Dockerfile

`POSTGRES_PASSWORD: mypassword123` in a file that goes into Git. 😱 **Fix:** `${DB_PASSWORD}` + a `.env` file in `.gitignore`.

### Mistake 6: `docker compose down -v` by accident

The `-v` deletes your volumes — all database data is gone. **Fix:** Use plain `docker compose down`. Make **backups** of real data!

---

## ✅ Summary

- **Docker** 🐳 packs your app and everything it needs into a **container** — it runs the same everywhere. 🚢
- **Dockerfile** 📜 → `docker build -t name:tag .` → **image** 🧊 → `docker run -p 8080:8080 name:tag` → **container** 📦.
- Our Dockerfile: `FROM eclipse-temurin:25-jre`, `COPY` the jar, `ENTRYPOINT ["java", "-jar", "app.jar"]`.
- Containers are thrown away — keep data in a **database** with a **volume** 💾.
- **Docker Compose** 🎼 (`compose.yaml`): app + PostgreSQL together, `depends_on` + `healthcheck`, containers find each other **by service name**. `docker compose up --build` / `down`.
- Secrets in **`.env`** (in `.gitignore`!) → `${VARIABLE}` in `compose.yaml`.

---

## ❓ Quiz

1. What's the difference between an image and a container?
2. What does `FROM eclipse-temurin:25-jre` do?
3. What does `-p 9000:8080` mean?
4. Why does deleting a container delete the H2 file data, but not the PostgreSQL data in our Compose setup?
5. Why is the database host `db` and not `localhost` in `compose.yaml`?
6. What does `depends_on` with `condition: service_healthy` do?
7. Where do the secrets for Compose live, and what must you do with that file?

<details>
<summary>Click to see the answers</summary>

1. An image is a frozen package (the recipe and ingredients). A container is a running copy made from an image.
2. It starts our image from a small Linux that already has Java 25 (the runtime) installed.
3. Port 9000 on my computer is connected to port 8080 inside the container.
4. The H2 file lives inside the container. The PostgreSQL data lives in a volume, which is kept outside the container.
5. Inside Compose, containers reach each other by their service name. `localhost` would mean the app's own container.
6. It starts the app only after the database's health check says it's ready.
7. In a `.env` file next to `compose.yaml` — and that file must be in `.gitignore`.

</details>

---

[⬅ Previous chapter](98-making-a-jar.md) | [Table of Contents](../README.md) | [Next chapter: Putting your app on the internet ➡](100-going-live.md)
