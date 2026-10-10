# Chapter 47 – Testing APIs with Postman and curl

[⬅ Previous chapter](46-rest-api.md) | [Table of Contents](../README.md) | [Next chapter ➡](../part-07-spring-boot-basics/48-spring-and-spring-boot.md)

---

## 🎯 Goal

At the end of this chapter you will know:

- Why you need special **tools** to test APIs (the browser is not enough)
- How to use **curl** in the terminal: GET, POST, PUT, DELETE, headers, JSON bodies
- The **Windows PowerShell** traps with curl, and how to avoid them ⚠️
- How to use **Postman**: requests, JSON bodies, collections, variables
- How to practice on a **free test API** (JSONPlaceholder)
- How to test your **own** server (the Notes server from Chapter 44)

> 🌱 You'll use these tools **every day** when you build Spring Boot APIs in Part 8. They're like a **remote control** 🎮 for your server!

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **curl** | A small **terminal program** that sends HTTP requests. Installed on almost every computer. |
| **Postman** | A **desktop app** with buttons and forms for sending HTTP requests. |
| **Flag / option** | An extra setting for a terminal command, starting with `-`: `-X`, `-H`, `-d`. |
| **Collection** | In Postman: a **folder** of saved requests. 📁 |
| **Environment variable** | In Postman: a named value like `{{baseUrl}}` that you can reuse and change in one place. |
| **Test API** | A free public API made for **practice**. |

---

## 📖 Story: The remote control 🎮

You built a robot toy 🤖 (your server). How do you **test** it? You need a **remote control** with buttons: "walk forward", "turn left", "pick up the ball"...

- The **browser** is a remote control with only **one button**: GET. 😕
- **curl** is a remote control with **all** the buttons — but you type commands instead of pressing buttons. ⌨️
- **Postman** is a **fancy** remote control with a screen, buttons, and a memory for your favorite commands. 🎮✨

Professional developers use **both** curl and Postman (or similar tools).

---

## 🤔 Part 1: Why not just the browser?

The browser's address bar:

| Can | Can't |
|---|---|
| ✅ send **GET** requests | ❌ send POST, PUT, PATCH, DELETE |
| ✅ show JSON responses | ❌ add custom headers (like `Authorization`) |
| | ❌ send a JSON **body** |
| | ❌ easily show status codes and headers (you need F12) |

So for **reading** (GET), the browser is fine. For **everything else**, we need curl or Postman. 🧰

---

## 🧪 Part 2: A free test API — JSONPlaceholder

To practice **without** writing a server, we use a free fake API on the internet:

```
https://jsonplaceholder.typicode.com
```

It has fake **posts**, **comments**, **users**, **todos**... You can GET, POST, PUT, DELETE — it **answers** like a real API, but it **doesn't really save** your changes (it's fake! 😄).

| Endpoint | What |
|---|---|
| `GET /posts` | 100 posts |
| `GET /posts/1` | post number 1 |
| `GET /todos?userId=1` | to-dos of user 1 (a query filter!) |
| `GET /users/1/todos` | the same, as a nested resource |
| `POST /posts` | "create" a post (returns `201` and an `id`) |
| `PUT /posts/1` | "replace" post 1 |
| `DELETE /posts/1` | "delete" post 1 |

Try in your browser first: `https://jsonplaceholder.typicode.com/todos/1`

```json
{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

(The text is fake Latin — it's normal! 😊)

---

## ⌨️ Part 3: curl — the terminal remote control

**curl** (say "curl", like hair 💇) is already installed on **Windows 10/11**, **Mac** and **Linux**.

Check:

```
curl --version
```

```
curl 8.x.x (...)
```

### ⚠️ Windows users — read this first!

On Windows there are **3** terminals. curl works a bit differently in each:

| Terminal | Type the command as | JSON quotes |
|---|---|---|
| **Git Bash** (installed with Git — Chapter 42) ✅ **recommended** | `curl ...` | easy: `'{"title":"Hi"}'` |
| **Command Prompt** (cmd) | `curl ...` | escape inside: `"{\"title\":\"Hi\"}"` |
| **Windows PowerShell** | ⚠️ **`curl.exe`** ... (with `.exe`!) | tricky — use a **file** (Part 3.6) |

Why? In Windows PowerShell, the word `curl` is a **different** command (a shortcut for `Invoke-WebRequest`). Writing **`curl.exe`** uses the real curl. 😉

> 💡 **Easiest choice:** use **Git Bash** for curl. All the examples below work there exactly as written. In IntelliJ, you can open a Git Bash terminal: **Terminal** window → the **▾** arrow next to **+** → **Git Bash**.

### 3.1 GET — the simplest request

```
curl https://jsonplaceholder.typicode.com/todos/1
```

```json
{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

| Part | Meaning |
|---|---|
| `curl` | the program |
| `https://...` | the URL. Without other options, curl sends a **GET** and prints the **body**. |

### 3.2 `-i` — show the status and headers too

```
curl -i https://jsonplaceholder.typicode.com/todos/1
```

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
...more headers...

{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

`-i` = **i**nclude the response headers. Now you see the **status code** `200 OK`! ✅

### 3.3 Query parameters

```
curl "https://jsonplaceholder.typicode.com/todos?userId=1&completed=true"
```

⚠️ Put the URL in **quotes** when it contains `&` or `?`. Otherwise the terminal thinks `&` is a special command symbol! 😵

### 3.4 `-X` — choose the method

```
curl -i -X DELETE https://jsonplaceholder.typicode.com/posts/1
```

```
HTTP/1.1 200 OK
...
{}
```

| Option | Meaning |
|---|---|
| `-X DELETE` | use the method **DELETE** (`-X` = "request method") |

(A real API would often answer `204 No Content`. This fake API answers `200` with an empty object `{}`.)

### 3.5 POST with a JSON body: `-H` and `-d`

```
curl -i -X POST https://jsonplaceholder.typicode.com/posts \
     -H "Content-Type: application/json" \
     -d '{"title": "Hello", "body": "My first post", "userId": 1}'
```

```
HTTP/1.1 201 Created
location: https://jsonplaceholder.typicode.com/posts/101
...

{
  "title": "Hello",
  "body": "My first post",
  "userId": 1,
  "id": 101
}
```

### 🔍 Line by line

| Part | Meaning |
|---|---|
| `-X POST` | method POST (create). |
| `\` at the end of a line | "The command continues on the next line." (Just for readability. In cmd use `^`, in PowerShell use `` ` ``. Or write everything on **one** line.) |
| `-H "Content-Type: application/json"` | Add a **header**: "my body is JSON". (`-H` = header. You can use many `-H`.) ⚠️ Spring Boot **needs** this header to read JSON! |
| `-d '{...}'` | The **body** (data). `-d` also makes curl use POST automatically. |

Look at the answer: **201 Created**, a **`location`** header, and the new **`id: 101`**. Exactly the REST style from Chapter 46! 🎉

### 3.6 JSON from a file (best for Windows PowerShell!)

Quotes inside quotes are painful. 😩 Put the JSON in a **file** instead:

**File: `new-post.json`**

```json
{
  "title": "Hello",
  "body": "My first post",
  "userId": 1
}
```

```
curl -i -X POST https://jsonplaceholder.typicode.com/posts -H "Content-Type: application/json" -d "@new-post.json"
```

`-d "@new-post.json"` = "read the body **from this file**". 📄 This works the **same** in Git Bash, cmd and PowerShell (with `curl.exe`). ✅

### 3.7 PUT

```
curl -X PUT https://jsonplaceholder.typicode.com/posts/1 \
     -H "Content-Type: application/json" \
     -d '{"id": 1, "title": "New title", "body": "New body", "userId": 1}'
```

```json
{
  "id": 1,
  "title": "New title",
  "body": "New body",
  "userId": 1
}
```

### 3.8 `-v` — see EVERYTHING (verbose) 🔬

```
curl -v https://jsonplaceholder.typicode.com/todos/1
```

You see the **request** (lines starting with `>`) **and** the response (lines starting with `<`):

```
> GET /todos/1 HTTP/1.1
> Host: jsonplaceholder.typicode.com
> User-Agent: curl/8.x.x
> Accept: */*
>
< HTTP/1.1 200 OK
< Content-Type: application/json; charset=utf-8
< ...
```

Perfect for **debugging**: "What exactly did I send?" 🕵️

### 3.9 Sending a token

```
curl -H "Authorization: Bearer my-secret-token" http://localhost:8080/api/profile
```

(You'll use this with Spring Security in Chapter 83. 🔐)

### 📋 curl cheat sheet

| Option | Meaning | Example |
|---|---|---|
| (none) | GET, print body | `curl URL` |
| `-i` | show status + headers | `curl -i URL` |
| `-v` | show **everything** (request too) | `curl -v URL` |
| `-X METHOD` | choose the method | `-X POST`, `-X PUT`, `-X DELETE` |
| `-H "Name: value"` | add a header | `-H "Content-Type: application/json"` |
| `-d 'data'` | send a body | `-d '{"name":"Sara"}'` |
| `-d "@file.json"` | body from a file | `-d "@student.json"` |
| `-s` | silent (no progress bar) | `curl -s URL` |
| `-o file` | save the body to a file | `-o result.json` |

---

## 📮 Part 4: Postman — the friendly remote control

**Postman** is a free desktop app with a graphical window. Great for beginners and for saving your requests. 🎮

### Install

1. Go to `https://www.postman.com/downloads/`.
2. Download and install it for your system.
3. Open it. You can **create a free account** (to save your work online), or look for the option to continue without signing in (if your version offers it).

> 💡 Alternatives that work the same way: **Insomnia**, **Bruno**, **Hoppscotch** (in the browser), and the **HTTP Client** in some IntelliJ editions. Choose what you like — the ideas are the same!

### 4.1 Your first request

1. Click **New** → **HTTP** (or the **+** tab).
2. You see this:

```
 ┌───────────────────────────────────────────────────────────────────┐
 │ [GET ▾]  https://jsonplaceholder.typicode.com/todos/1   [ Send ]  │  ← method + URL
 ├───────────────────────────────────────────────────────────────────┤
 │ Params | Authorization | Headers | Body | ...                     │  ← request settings
 ├───────────────────────────────────────────────────────────────────┤
 │ Response:   Status: 200 OK   Time: 120 ms   Size: 350 B           │  ← result
 │ ┌───────────────────────────────────────────────────────────────┐ │
 │ │ {                                                             │ │
 │ │   "userId": 1,                                                │ │
 │ │   "id": 1,                                                    │ │
 │ │   "title": "delectus aut autem",                              │ │
 │ │   "completed": false                                          │ │
 │ │ }                                                             │ │
 │ └───────────────────────────────────────────────────────────────┘ │
 └───────────────────────────────────────────────────────────────────┘
```

3. Choose **GET**, paste the URL, click **Send**. 🚀
4. Look at the bottom: **Status 200 OK**, the **time**, the **size**, and the **JSON body** (nicely colored!). Click the **Headers** tab in the response to see the response headers.

### 4.2 Query parameters — the **Params** tab

Type the URL `https://jsonplaceholder.typicode.com/todos`, then open **Params**:

| Key | Value |
|---|---|
| userId | 1 |
| completed | true |

Postman builds the URL for you: `.../todos?userId=1&completed=true`. ✨ You can tick ☑️ / untick ☐ parameters to turn them on and off.

### 4.3 POST with a JSON body

1. Choose **POST**, URL: `https://jsonplaceholder.typicode.com/posts`
2. Open the **Body** tab → choose **raw** → choose **JSON** in the dropdown (on the right).
3. Type:

```json
{
  "title": "Hello from Postman",
  "body": "This is fun!",
  "userId": 1
}
```

4. **Send**.

Result: **201 Created** ✅ and the new `"id": 101`.

> 💡 Choosing **JSON** in the dropdown **automatically** adds the header `Content-Type: application/json`. Check it in the **Headers** tab (it may be hidden under "auto-generated headers"). 🪄

### 4.4 Headers and Authorization

- **Headers** tab → add any header: `Accept: application/json`.
- **Authorization** tab → choose **Bearer Token** → paste a token. Postman adds `Authorization: Bearer ...` for you. 🔐 (Chapter 83.)

### 4.5 Collections — save your requests 📁

You'll test the **same** requests many times. Save them!

1. Click **Save** (Ctrl + S).
2. Give it a name: "Get todo 1".
3. Create a **collection** (a folder): "JSONPlaceholder practice".

Later, your Spring Boot project gets its **own** collection: "Student API" with "List students", "Create student", "Delete student"... One click to run any of them! 🖱️

### 4.6 Variables — change the address in one place

Your API will run at `http://localhost:8080` during development, and somewhere else later (Chapter 100). Don't type the address in **every** request!

1. Click on the collection → **Variables** tab.
2. Add: `baseUrl` = `http://localhost:8080`
3. In requests, write: `{{baseUrl}}/api/students`

Change `baseUrl` once → **all** requests use the new address. 🎯 (Like a **constant** in Java — Chapter 17!)

---

## 🔬 Part 5: Test your OWN server

Remember the **Notes server** from Chapter 44? Let's test it with both tools!

1. Run `NotesServer` in IntelliJ.
2. Test with **curl** (Git Bash):

```
curl -i http://localhost:8080/notes
```
```
HTTP/1.1 200 OK
Content-type: text/plain; charset=utf-8
Content-length: 9

Notes: []
```

```
curl -i -X POST -d "Buy milk" http://localhost:8080/notes
```
```
HTTP/1.1 201 Created
...
Saved note number 1
```

```
curl -i -X DELETE http://localhost:8080/notes
```
```
HTTP/1.1 405 Method Not Allowed
...
Method DELETE is not allowed here
```

3. Test with **Postman**:
   - **GET** `http://localhost:8080/notes` → `200 OK`, `Notes: [Buy milk]`
   - **POST** `http://localhost:8080/notes`, Body → **raw** → **Text** → `Learn Postman` → `201 Created`
   - **POST** with an empty body → `400 Bad Request`

4. Look at IntelliJ's Run window — your server printed every request it received:

```
📨 GET /notes
📨 POST /notes
📨 DELETE /notes
📨 GET /notes
📨 POST /notes
📨 POST /notes
```

🎉 You're testing your own server like a professional! In Part 8, you'll do exactly this with your **Spring Boot** Student API.

---

## 🆚 Part 6: curl or Postman?

| | curl ⌨️ | Postman 🎮 |
|---|---|---|
| Install | already there | download an app |
| Style | type commands | click buttons and forms |
| Saving requests | in scripts / text files | collections, variables, history |
| Great for | quick checks, scripts, documentation, servers without a screen | exploring, many requests, teamwork, beginners |
| Seen in | tutorials, README files, Stack Overflow | team workspaces |

👉 **Learn both.** You'll read curl commands **everywhere** (documentation always shows them), and Postman makes daily work comfortable. 😊

> 💡 **Postman bonus:** Paste a curl command into Postman (**Import** → **Raw text**) → it becomes a Postman request automatically! And the **Code** button `</>` turns a Postman request into a curl command. 🔄

---

## ✋ Try it yourself

**Task 1 (curl):** Get **user number 3** from JSONPlaceholder. What is the user's name and city? (Hint: `/users/3`.)

**Task 2 (curl):** Get all **comments** of post 1. Try both styles: `/posts/1/comments` and `/comments?postId=1`. Are the results the same?

**Task 3 (curl):** Create a **todo** with `POST /todos` and the JSON body `{"title": "Learn curl", "completed": false, "userId": 1}`. Which status code and `id` do you get?

<details>
<summary>Click to see the command</summary>

```
curl -i -X POST https://jsonplaceholder.typicode.com/todos \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn curl", "completed": false, "userId": 1}'
```

You get `201 Created` and `"id": 201` (the fake API has 200 todos).

</details>

**Task 4 (Postman):** Make a collection "JSONPlaceholder practice" with **5 saved requests**: list posts, get one post, create a post, update a post (PUT), delete a post. Use a variable `{{baseUrl}}` = `https://jsonplaceholder.typicode.com`.

**Task 5:** Request `GET /posts/9999`. What status code do you get? What does it mean? (Chapter 44!)

<details>
<summary>Click to see the answer</summary>

`404 Not Found` — there is no post with id 9999. (The body is an empty object `{}`.)

</details>

**Task 6 (your server):** Start the Notes server. Add 3 notes with curl, and 2 with Postman. Then open `http://localhost:8080/notes` in the browser. Are all 5 there?

---

## ⚠️ Common mistakes

### Mistake 1: PowerShell's fake `curl`

```
PS> curl -X POST ...
Invoke-WebRequest : A parameter cannot be found that matches parameter name 'X'.
```

**Fix:** Type **`curl.exe`**, or use Git Bash / cmd.

### Mistake 2: JSON quotes broken in the terminal

```
curl: (3) URL rejected: Bad hostname
```
or the server says `400 Bad Request` because the JSON arrived broken.

**Fix:** Use single quotes `'...'` around JSON in Git Bash, or put the JSON in a **file** and use `-d "@file.json"`.

### Mistake 3: Forgetting `Content-Type: application/json`

The server can't read your JSON body → `415 Unsupported Media Type` (very common with Spring Boot!).
**Fix:** `-H "Content-Type: application/json"` in curl, or **raw + JSON** in Postman.

### Mistake 4: URL with `&` not in quotes

```
curl https://.../todos?userId=1&completed=true   ❌ the terminal cuts it at &
curl "https://.../todos?userId=1&completed=true" ✅
```

### Mistake 5: Server not running

```
curl: (7) Failed to connect to localhost port 8080: Connection refused
```

Postman shows "Could not send request — Error: connect ECONNREFUSED 127.0.0.1:8080".
**Fix:** Start your server first! ▶️

### Mistake 6: Expecting the fake API to really save data

JSONPlaceholder **pretends** to save. After `POST`, `GET /posts/101` returns `404`. That's normal for a fake test API. 😄 Your **own** Spring Boot API will really save (Part 9)!

---

## ✅ Summary

- The browser can only send **GET** — use **curl** or **Postman** for everything else. 🎮
- Practice on **JSONPlaceholder**: `https://jsonplaceholder.typicode.com`.
- **curl** essentials:
  - `curl URL` (GET) · `-i` (status + headers) · `-v` (everything)
  - `-X POST/PUT/DELETE` (method) · `-H "Name: value"` (header) · `-d '...'` or `-d "@file.json"` (body)
  - Quote URLs with `&`. On Windows: Git Bash ✅, or **`curl.exe`** in PowerShell.
- **Postman** essentials:
  - method + URL + **Send**; **Params** tab; **Body → raw → JSON**; **Headers**; **Authorization**
  - **Collections** 📁 to save requests; **variables** like `{{baseUrl}}`
- Always send `Content-Type: application/json` with JSON bodies.
- You tested your **own** server — the same way you'll test Spring Boot. 🌱

---

## ❓ Quiz

1. Why can't you test a POST request with the browser's address bar?
2. What does `curl -i` show that plain `curl` doesn't?
3. Which curl option chooses the HTTP method?
4. Which curl option adds a header? Which one sends a body?
5. Why do you type `curl.exe` in Windows PowerShell?
6. In Postman, how do you send a JSON body?
7. What is a Postman collection? What is a variable like `{{baseUrl}}` for?
8. You get "Connection refused" for `localhost:8080`. What's the most likely reason?

<details>
<summary>Click to see the answers</summary>

1. The address bar only sends GET requests.
2. The status line and the response headers.
3. `-X` (for example `-X POST`).
4. `-H` adds a header. `-d` sends a body.
5. Because in PowerShell, `curl` is a shortcut for a different command (`Invoke-WebRequest`).
6. Body tab → raw → choose JSON → type the JSON.
7. A collection is a folder of saved requests. A variable stores a value (like the server address) used in many requests, so you change it in one place.
8. The server is not running (or it runs on a different port).

</details>

---

## 🎉 Part 6 complete!

You now understand **how the web works**:

- ✅ Clients and servers, URLs, ports, localhost
- ✅ HTTP requests, responses, methods, status codes, headers
- ✅ JSON
- ✅ REST API design
- ✅ Testing APIs with curl and Postman
- ✅ You even built **two tiny web servers** in plain Java! 🚀

### 🏁 The foundation is complete!

Look how far you've come: 🏔️

```
 Part 1 ✅ Getting ready          Part 4 ✅ More Java (lists, streams...)
 Part 2 ✅ Java basics            Part 5 ✅ Tools (Maven, Git)
 Part 3 ✅ Objects (OOP)          Part 6 ✅ How the web works
```

**Now** you're truly ready. In **Part 7**, we finally start **Spring Boot**! 🌱🚀 You'll create your first project, understand every folder and file, and discover the **big idea** behind Spring: **Dependency Injection**.

Let's go! 🎉

---

[⬅ Previous chapter](46-rest-api.md) | [Table of Contents](../README.md) | [Next chapter: What are Spring and Spring Boot? ➡](../part-07-spring-boot-basics/48-spring-and-spring-boot.md)
