# Chapter 77 – Using MySQL or PostgreSQL

[⬅ Previous chapter](76-many-to-many.md) | [Table of Contents](../README.md) | [Next chapter ➡](78-paging-sorting.md)

---

## 🎯 Goal

H2 is a wonderful **learning** database 🧪. But real apps on real servers use a **database server** like **PostgreSQL** 🐘 or **MySQL** 🐬. Today you'll switch — and you'll be amazed how **little** changes!

At the end of this chapter you will know:

- Why real apps use a **database server**
- How to get **PostgreSQL** or **MySQL** running (installer or Docker)
- How to create a **database** and a **user** for your app
- Which **driver** dependency to add
- How to use **profiles** (Chapter 56): **H2 on your laptop**, **PostgreSQL/MySQL on the server** 🎭
- How to keep the **password** out of your code 🔒
- The most common **connection errors** and how to fix them

> 🌱 We tested everything in this chapter with a real **PostgreSQL 14** server and a real **MariaDB 10.11** server (MariaDB is MySQL's twin — Chapter 67 — and works with the MySQL driver). Our app ran on **both** with **zero** changes to the Java code. 🤯

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **Database server** | A separate program that runs the database (Chapter 67). |
| **Host** | The computer where the server runs: `localhost` = your own computer. |
| **Port** | The "door number" (Chapter 43): PostgreSQL **5432**, MySQL **3306**. |
| **Driver** | The library that lets Java talk to **one** kind of database (Chapter 70). |
| **Dialect** | Hibernate's knowledge of **one** database's way of speaking SQL. 🗣️ |
| **`psql`** | PostgreSQL's command-line tool for typing SQL. |
| **Docker** | A tool that runs programs (like databases) in ready-made boxes called **containers**. 🐳 (Chapter 99) |
| **Migration tool** | A tool (Flyway, Liquibase) that changes tables **step by step** on real servers. |

---

## 📖 Story: Moving from the kitchen fridge to the big warehouse 🏭

Our little fridge (H2 🧊) was great for cooking at home. But now our school app is getting **famous**: hundreds of students, several apps using the same data, and the head teacher wants **backups** every night. 💾

So we move the food to a **big, professional warehouse** (PostgreSQL / MySQL 🏭):

- Many trucks (apps) can deliver and pick up at the same time. 🚚🚚
- It has guards, alarms and backups. 🛡️
- It can hold **millions** of boxes.

And the best part: our cooks (the Java code) **don't change how they work**. They still say "save this student!" — only the **address** of the storage is different. 📍

---

## 🤔 Part 1: Why switch from H2?

| | H2 (embedded) 🧊 | PostgreSQL / MySQL (server) 🏭 |
|---|---|---|
| Installation | ✅ None — it's a dependency | ❌ Install a server (or Docker) |
| Runs | Inside your app | As a separate program |
| Several apps share the data | ❌ | ✅ |
| Size | Small to medium | Huge |
| Backups, users, permissions, monitoring | Basic | ✅ Professional tools |
| Used on real servers | ❌ Rarely | ✅ Almost always |
| Best for | Learning, quick tests | Real apps |

**The plan:** keep **H2** for development on your laptop (fast, no setup), and use **PostgreSQL** (or MySQL) on real servers. Profiles (Chapter 56) make this easy! 🎭

---

## 🐘 Part 2: Get PostgreSQL running

You need a PostgreSQL **server** on your computer. Two ways:

### Way 1: The installer

1. Go to **https://www.postgresql.org/download/** and choose your system (Windows, Mac, Linux).
2. Run the installer. Keep the defaults. It asks for a password for the **`postgres`** user (the boss of the database) — **remember it**! 🔑
3. The default **port** is **5432**. Keep it.
4. The installer also installs **pgAdmin** (a graphical tool) and **`psql`** (the command-line tool).

### Way 2: Docker 🐳

If you have Docker (you'll learn it in **Chapter 99**), **one** command starts PostgreSQL:

```
docker run --name school-postgres -e POSTGRES_DB=school -e POSTGRES_USER=school_user -e POSTGRES_PASSWORD=secret123 -p 5432:5432 -d postgres:17
```

| Part | Meaning |
|---|---|
| `--name school-postgres` | A name for this container. |
| `-e POSTGRES_DB=school` | Create a database called `school`. |
| `-e POSTGRES_USER=school_user` / `-e POSTGRES_PASSWORD=secret123` | Create this user with this password. |
| `-p 5432:5432` | Open door 5432 on your computer → door 5432 in the container. |
| `-d postgres:17` | Run (in the background) the official PostgreSQL 17 image. |

With Docker, the database and user are ready — skip Part 3! 🎉

### Part 3: Create a database and a user (installer only)

Your app should **not** use the all-powerful `postgres` user. Create its **own** user. Open **`psql`** (or the "Query Tool" in pgAdmin), log in as `postgres`, and type:

```sql
CREATE DATABASE school;
CREATE USER school_user WITH PASSWORD 'secret123';
ALTER DATABASE school OWNER TO school_user;
```

| SQL | Meaning |
|---|---|
| `CREATE DATABASE school;` | A new, empty database for our app. |
| `CREATE USER school_user WITH PASSWORD 'secret123';` | A user just for our app. (Use a **better** password! 🔒) |
| `ALTER DATABASE school OWNER TO school_user;` | `school_user` owns the database → it may create tables in it. |

> 💡 One PostgreSQL server can hold **many** databases — one per app. 🗄️🗄️🗄️

---

## 📦 Part 4: Add the driver

Java needs the **PostgreSQL driver** (Chapter 70). Add to **`pom.xml`**:

```xml
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

Click **Maven reload** 🔄. (Like H2, it's `runtime`: your code never uses its classes directly.)

**Keep the H2 dependency!** We still use H2 on the laptop. Both drivers can be in the project — the **URL** decides which one is used. 🔌

---

## 🎭 Part 5: Profiles — H2 for dev, PostgreSQL for prod

Remember **profiles** (Chapter 56)? `application.properties` is **always** read; `application-prod.properties` is read **only** when the `prod` profile is active, and **wins**.

**`application.properties`** stays as it is — H2 for your laptop:

```properties
spring.application.name=school

# The database: a FILE in the folder "data" of the project
spring.datasource.url=jdbc:h2:file:./data/school
spring.datasource.username=sa
spring.datasource.password=

# The H2 console (a web page to look inside the database)
spring.h2.console.enabled=true

# JPA / Hibernate
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.open-in-view=false
```

Create **`src/main/resources/application-prod.properties`**:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/school
spring.datasource.username=school_user
spring.datasource.password=${DB_PASSWORD}
spring.jpa.hibernate.ddl-auto=update
spring.h2.console.enabled=false
```

### 🔍 Line by line

| Setting | Meaning |
|---|---|
| `jdbc:postgresql://localhost:5432/school` | ⭐ The address: **PostgreSQL**, on **this computer**, door **5432**, database **`school`**. |
| `spring.datasource.username=school_user` | Our app's own user. |
| `spring.datasource.password=${DB_PASSWORD}` | ⭐ **No password in the file!** 🔒 It comes from the **environment variable** `DB_PASSWORD` (Chapter 55). |
| `spring.jpa.hibernate.ddl-auto=update` | Let Hibernate create the tables (fine for learning — see Part 8!). |
| `spring.h2.console.enabled=false` | ⭐ The H2 Console must **never** be open on a real server! 🔒 |

The **JDBC URL** has the same shape for every database:

```
 jdbc:postgresql://localhost:5432/school
 └┬─┘ └───┬────┘   └───┬───┘ └┬─┘ └─┬──┘
 JDBC  database    host     port  database
       type                       name
```

---

## ▶️ Part 6: Run it with PostgreSQL

Start the app with the `prod` profile **and** the password (Chapter 55–56):

**Git Bash / Mac / Linux:**

```bash
DB_PASSWORD=secret123 java -jar target/school-0.0.1-SNAPSHOT.jar --spring.profiles.active=prod
```

**Windows PowerShell:**

```powershell
$env:DB_PASSWORD="secret123"; java -jar target/school-0.0.1-SNAPSHOT.jar --spring.profiles.active=prod
```

**In IntelliJ:** Run → Edit Configurations → **Program arguments**: `--spring.profiles.active=prod`, and **Environment variables**: `DB_PASSWORD=secret123` (Chapter 56).

The log (real, from our test — we used port 5433 on our test computer):

```
... The following 1 profile is active: "prod"
... HikariPool-1 - Added connection org.postgresql.jdbc.PgConnection@500ec769
	Database JDBC URL [jdbc:postgresql://localhost:5433/school]
	Database driver: PostgreSQL JDBC Driver
	Database dialect: PostgreSQLDialect
	Database version: 14.15
... Started SchoolApplication in 10.972 seconds
DataLoader: added 2 classrooms, 3 courses and 3 students
```

| Log | Meaning |
|---|---|
| `profile is active: "prod"` | The prod settings are used. 🎭 |
| `PgConnection` / `PostgreSQL JDBC Driver` | Connected with the **PostgreSQL** driver. 🐘 |
| `Database dialect: PostgreSQLDialect` | ⭐ Hibernate now speaks **PostgreSQL's** SQL. 🗣️ |
| `DataLoader: added ...` | A new, empty database → our seed data was added. 🌱 |

And Hibernate's `CREATE TABLE` for PostgreSQL (real):

```sql
create table students (
    id bigint generated by default as identity,
    age integer not null,
    created_at timestamp(6) not null,
    email varchar(100) not null,
    name varchar(50) not null,
    teacher_note varchar(255),
    classroom_id bigint,
    primary key (id)
)
```

### ✅ Test the API

Exactly the same requests as before (real answers from PostgreSQL):

`GET /api/students`

```json
[{"id":1,"name":"Sara Ahmed","email":"sara@school.com","age":12,"classroom":"5A"},{"id":2,"name":"Tom Brown","email":"tom@school.com","age":13,"classroom":"6B"},{"id":3,"name":"Lina Haddad","email":"lina@school.com","age":11,"classroom":"5A"}]
```

`POST /api/students` with Omar → **201** `{"id":4,"name":"Omar Ali","email":"omar@school.com","age":12,"classroom":null}`

`GET /api/classrooms/1` → `{"id":1,"name":"5A","teacher":"Mrs. Khan","students":["Sara Ahmed","Lina Haddad"]}`

🎉🎉🎉 **The same API, the same answers, a real database server — and not ONE line of Java changed!** Only a dependency and a settings file. That's the power of JPA + Spring Boot. 🔌✨

---

## 🐬 Part 7: The same with MySQL

MySQL works the **same** way. Only three things are different:

**1. Start MySQL** (installer from **https://dev.mysql.com/downloads/**, or Docker):

```
docker run --name school-mysql -e MYSQL_DATABASE=school -e MYSQL_USER=school_user -e MYSQL_PASSWORD=secret123 -e MYSQL_ROOT_PASSWORD=rootsecret -p 3306:3306 -d mysql:8.4
```

(With the installer, create the database and user in the MySQL command-line tool:)

```sql
CREATE DATABASE school;
CREATE USER 'school_user'@'localhost' IDENTIFIED BY 'secret123';
GRANT ALL ON school.* TO 'school_user'@'localhost';
```

**2. The driver** in `pom.xml`:

```xml
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
    <scope>runtime</scope>
</dependency>
```

**3. The URL** (port **3306**):

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/school
spring.datasource.username=school_user
spring.datasource.password=${DB_PASSWORD}
spring.jpa.hibernate.ddl-auto=update
spring.h2.console.enabled=false
```

We tested this with **MariaDB** and the MySQL driver. The log said:

```
	Database driver: MySQL Connector/J
	Database dialect: MySQLDialect
```

and Hibernate wrote **MySQL-style** SQL — look at the differences:

```sql
create table students (
    id bigint not null auto_increment,
    age integer not null,
    created_at datetime(6) not null,
    ...
    primary key (id)
) engine=InnoDB
```

| PostgreSQL / H2 | MySQL |
|---|---|
| `generated by default as identity` | `auto_increment` |
| `timestamp(6)` | `datetime(6)` |
| — | `engine=InnoDB` |

**You** didn't write any of that — the **dialect** did. 🗣️ And the API answers were, again, **exactly** the same. 🎉

---

## 🏗️ Part 8: `ddl-auto` on real servers

On your laptop, `ddl-auto=update` is handy. On a **real** server with **real** data, professionals are more careful:

| Setting | Use it... |
|---|---|
| `update` | 💻 Learning, your laptop. It **adds** tables and columns — but it **never** removes or renames them, and big changes can go wrong. |
| `validate` | 🌍 Real servers: "**check** that the tables match the entities — and **refuse to start** if not." Safe! 🛡️ |
| `none` | 🌍 Real servers: Hibernate does nothing with the tables. |
| `create` / `create-drop` | ❌ **Never** on a real server — they **delete** all data! 😱 |

But then **who** creates and changes the tables on a real server? 🤔 A **migration tool** like **Flyway** or **Liquibase**: you write numbered SQL files (`V1__create_students.sql`, `V2__add_classrooms.sql`...), and the tool runs each one **once**, in order. Every change is planned, tested and saved in Git. 📜 (That's a topic for after this book — just remember the names!)

---

## 🔥 Part 9: Connection errors — and how to fix them

### 🚫 "Connection refused" — the server isn't running

We stopped our test PostgreSQL and started the app. It **didn't start** (our test server used port 5433 — with 5432 you'll see 5432 here):

```
Caused by: org.postgresql.util.PSQLException: Connection to localhost:5433 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
```

(Further down: `Unable to determine Dialect without JDBC metadata` — Hibernate couldn't even ask the database what kind it is.)

| Check | How |
|---|---|
| Is the database **running**? | Start the PostgreSQL service / the Docker container. |
| Is the **port** right? | 5432 (PostgreSQL), 3306 (MySQL). |
| Is the **host** right? | `localhost` if it's on your computer. |

("postmaster" is an old name for the PostgreSQL server program. 😄)

### 🔑 Wrong password or user

You'll see a message like:

```
FATAL: password authentication failed for user "school_user"
```

**Fix:** Check `spring.datasource.username` and the **`DB_PASSWORD`** environment variable. (Did you forget to set it? Then `${DB_PASSWORD}` can't be resolved, and Spring tells you that too — Chapter 55.)

### 🗄️ The database doesn't exist

PostgreSQL says something like `database "school" does not exist`. **Fix:** `CREATE DATABASE school;` (Part 3).

### 🧩 Missing driver

If you forget the driver dependency, Spring Boot can't find a driver for `jdbc:postgresql:...` and refuses to start. **Fix:** Add the driver (Part 4) and **reload Maven**.

---

## 💻 Mini project: Your own database settings 📝

You have a MySQL server on the computer `db.myschool.org`, on door **3307**. The database is called `library`, the user is `library_app`, and the password must come from an environment variable called `LIBRARY_DB_PASSWORD`.

1. Write the file **`application-library.properties`**.
2. Write the command to start the app with that profile (Git Bash).
3. Does the Book API (Chapter 73) need any **Java** changes to work with it?

<details>
<summary>Click to see the answer</summary>

1. **`application-library.properties`**:

```properties
spring.datasource.url=jdbc:mysql://db.myschool.org:3307/library
spring.datasource.username=library_app
spring.datasource.password=${LIBRARY_DB_PASSWORD}
spring.jpa.hibernate.ddl-auto=update
spring.h2.console.enabled=false
```

2. ```bash
LIBRARY_DB_PASSWORD=theRealPassword java -jar target/school-0.0.1-SNAPSHOT.jar --spring.profiles.active=library
```

(and the MySQL driver must be in `pom.xml`).

3. **No!** The `Book` entity, the repository and the service stay exactly the same. Hibernate creates the `books` table with MySQL's dialect. (And the column is still called `published`, thanks to `@Column(name = "published")` from Chapter 71. 😉)

</details>

---

## ✋ Try it yourself

**Task 1:** Take apart this URL: `jdbc:postgresql://192.168.1.50:5433/shop`

<details>
<summary>Click to see the answer</summary>

Database type: **PostgreSQL**. Host: **192.168.1.50** (another computer in the network). Port: **5433**. Database name: **shop**.

</details>

**Task 2:** Why do we write `spring.datasource.password=${DB_PASSWORD}` instead of the real password?

<details>
<summary>Click to see the answer</summary>

So the password is **never** in the code or in Git (Chapter 55). It's given from **outside** (an environment variable) when the app starts. 🔒

</details>

**Task 3:** You start the app **without** `--spring.profiles.active=prod`. Which database does it use?

<details>
<summary>Click to see the answer</summary>

**H2** (the file database from `application.properties`). The PostgreSQL settings are only used when the `prod` profile is active. That's exactly what we want on the laptop. 🎭

</details>

---

## ⚠️ Common mistakes

### Mistake 1: The password in `application.properties`

It ends up in Git → on GitHub → everybody can read it. 😱 **Fix:** `${DB_PASSWORD}` + an environment variable.

### Mistake 2: `ddl-auto=create` or `create-drop` on a real server

**All data deleted** at the next restart. 💥 **Fix:** `update` only for learning; `validate` or `none` (+ Flyway/Liquibase) for real servers.

### Mistake 3: The H2 Console open on a real server

**Fix:** `spring.h2.console.enabled=false` in the prod profile (or remove the console dependency for production builds).

### Mistake 4: Using the `postgres` / `root` user in the app

If the app is hacked, the attacker gets **full** control of **all** databases. **Fix:** A separate user with rights only for **its** database.

### Mistake 5: Native queries that only work on H2

A native SQL query (Chapter 74) with an H2-only feature breaks on PostgreSQL. **Fix:** Prefer query methods and JPQL; test native queries on the **real** database type.

### Mistake 6: Forgetting to start the database

"Connection refused" 🚫. **Fix:** Start PostgreSQL/MySQL **before** the app.

---

## ✅ Summary

- Real apps use a **database server**: **PostgreSQL** 🐘 (port **5432**) or **MySQL** 🐬 (port **3306**).
- Get one with the **installer** or **Docker** 🐳; create a **database** and an **app user**.
- Add the **driver** (`org.postgresql:postgresql` or `com.mysql:mysql-connector-j`, scope `runtime`).
- **Profiles** 🎭: H2 in `application.properties` (laptop), the real database in **`application-prod.properties`** (`--spring.profiles.active=prod`).
- JDBC URL: `jdbc:postgresql://host:port/database` (or `jdbc:mysql://...`).
- Password from outside: **`${DB_PASSWORD}`**. H2 Console **off** in prod. 🔒
- **No Java changes!** The **dialect** writes the right SQL for each database. 🗣️
- `ddl-auto`: `update` for learning; `validate`/`none` + **Flyway/Liquibase** on real servers.
- "Connection refused" = the server isn't running (or wrong host/port).

---

## ❓ Quiz

1. Why do real apps usually use PostgreSQL or MySQL instead of H2?
2. What are the default ports of PostgreSQL and MySQL?
3. Which dependency do you need for PostgreSQL?
4. Write the JDBC URL for a PostgreSQL database `shop` on your own computer, default port.
5. How does the app use H2 on your laptop, but PostgreSQL on the server?
6. Why should the app have its own database user?
7. Which `ddl-auto` values should you use on a real server?
8. You see `Connection to localhost:5432 refused`. What do you check first?
9. Which part of Hibernate makes sure the SQL fits each database?

<details>
<summary>Click to see the answers</summary>

1. They're separate servers: many apps can share them, they handle huge data, and they have professional tools for backups, users and monitoring.
2. PostgreSQL: **5432**. MySQL: **3306**.
3. `org.postgresql:postgresql` (scope `runtime`).
4. `jdbc:postgresql://localhost:5432/shop`
5. With profiles: H2 in `application.properties`, PostgreSQL in `application-prod.properties`, and `--spring.profiles.active=prod` on the server.
6. So that a hacked app can only reach its own database, not everything.
7. `validate` or `none` (with a migration tool like Flyway or Liquibase).
8. Is the PostgreSQL server running? (And are the host and port right?)
9. The **dialect** (for example `PostgreSQLDialect`, `MySQLDialect`).

</details>

---

[⬅ Previous chapter](76-many-to-many.md) | [Table of Contents](../README.md) | [Next chapter: Pages and sorting ➡](78-paging-sorting.md)
