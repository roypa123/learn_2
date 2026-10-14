# Chapter 90 – Calling other APIs

[⬅ Previous chapter](89-thymeleaf.md) | [Table of Contents](../README.md) | [Next chapter ➡](91-scheduling.md)

---

## 🎯 Goal

So far, **others** called **our** API. But apps also call **other** apps! 🌍 A weather app asks a weather service for today's weather ☀️. A shop asks a bank if a payment worked 💳. Today **our** app becomes the **client**.

At the end of this chapter you will know:

- How our server can be a **client** too 🔄
- How to call another API with Spring's **`RestClient`**
- How to turn the other API's JSON into a Java **record** automatically 🪄
- How to put the other API's address into **settings**
- What to do when the other API answers **404** — or doesn't answer at all 😱
- How to get a **list** back

---

## 📝 New words

| Word | Simple meaning |
|---|---|
| **External API** | An API that belongs to **someone else**, somewhere on the internet. 🌍 |
| **`RestClient`** | Spring's tool for **sending** HTTP requests and reading the answers. 📞 |
| **Base URL** | The beginning of all addresses of an API, like `https://jsonplaceholder.typicode.com`. |
| **Deserialize** | Turn JSON **into** Java objects. (Serialize = Java → JSON, Chapter 45.) |
| **Timeout** | "If there's no answer after X seconds, give up." ⏱️ |
| **`ParameterizedTypeReference`** | A small trick to tell Java "I want a **`List` of** something" back. |

---

## 📖 Story: The school kitchen calls the bakery 🥖

The school kitchen 🍳 makes lunch for 300 students. It's great at soup and pasta — but **bread**? The kitchen doesn't bake bread. It **calls the bakery** 📞:

```
 🍳 Kitchen: "Hello, bakery! I need bread for 300 students, please."
 🥖 Bakery:  "Here are 30 loaves!"
 🍳 Kitchen: (puts the bread on the lunch plates and serves the students) 🍽️
```

For the **students**, the kitchen is the **server** (it serves them lunch). But for the **bakery**, the kitchen is a **client** (it orders bread). The same kitchen plays **both** roles! 🔄

```
 Students ──► 🍳 our app (server) ──► 🥖 other API (server)
   client          ...and client!
```

And the kitchen must be ready for problems: what if the bakery is **closed**? What if it takes **two hours**? The students still need lunch! 😱

---

## 🌍 Part 1: The other API

We need an API to call. We'll use **JSONPlaceholder** — a free, fake API made for learning. Open this in your browser:

**https://jsonplaceholder.typicode.com/todos/1**

```json
{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

It's a "to-do" item: a task with a **title** and whether it's **completed**. (The titles are in fake Latin — that's normal for test data. 😄) In our school, we'll call them **homework** tasks. 📝

---

## 📞 Part 2: The `RestClient`

`RestClient` is already in your project — it's part of Spring's web tools. We make **one** `RestClient` for the homework API, as a **bean**.

First, the address goes into **`application.properties`**:

```properties
# The external homework API
school.homework.base-url=https://jsonplaceholder.typicode.com
```

Then a configuration class:

**`config/HomeworkClientConfig.java`**

```java
package com.example.school.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestClient;

@Configuration
public class HomeworkClientConfig {

    @Bean
    public RestClient homeworkRestClient(@Value("${school.homework.base-url}") String baseUrl) {
        return RestClient.builder()
                .baseUrl(baseUrl)
                .build();
    }
}
```

| Code | Meaning |
|---|---|
| `@Value("${school.homework.base-url}") String baseUrl` | The address from our settings. Why not write it in the code? Because tests (or a different server) may need a **different** address. 👍 |
| `RestClient.builder()` | A **builder** 🧱 for a `RestClient`. |
| `.baseUrl(baseUrl)` | Every request will **start** with this address. Later we only write the end, like `/todos/1`. |
| `.build()` | Make the finished client. |

---

## 📦 Part 3: A record for the answer

What does the other API send? `userId`, `id`, `title`, `completed`. We make a **record** with the fields **we** need:

**`dto/HomeworkResponse.java`**

```java
package com.example.school.dto;

public record HomeworkResponse(Long id, String title, boolean completed) {
}
```

| Code | Meaning |
|---|---|
| `Long id, String title, boolean completed` | The **names** must match the JSON names exactly. Jackson fills them in. 🪄 |
| (no `userId`) | We don't need it — and that's fine! Spring Boot's Jackson simply **ignores** JSON fields that the record doesn't have. |

---

## 🔧 Part 4: The client service

Now a service that **calls** the other API:

**`service/HomeworkService.java`**

```java
package com.example.school.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import com.example.school.dto.HomeworkResponse;

@Service
public class HomeworkService {

    private final RestClient homeworkRestClient;

    public HomeworkService(RestClient homeworkRestClient) {
        this.homeworkRestClient = homeworkRestClient;
    }

    public HomeworkResponse getHomework(Long id) {
        return homeworkRestClient.get()
                .uri("/todos/{id}", id)
                .retrieve()
                .body(HomeworkResponse.class);
    }
}
```

Read it like a sentence: "**get** the **uri** `/todos/1`, **retrieve** the answer, and give me the **body** as a `HomeworkResponse`." 🗣️

| Code | Meaning |
|---|---|
| `homeworkRestClient.get()` | ⭐ A **GET** request. (There are also `.post()`, `.put()`, `.delete()`.) |
| `.uri("/todos/{id}", id)` | The address after the base URL. `{id}` is filled with our `id` → `/todos/1`. |
| `.retrieve()` | ⭐ **Send** the request and get the answer. |
| `.body(HomeworkResponse.class)` | Turn the JSON body into a `HomeworkResponse` — **deserialize**. 🪄 |

And a controller, so we can try it:

**`controller/HomeworkController.java`**

```java
package com.example.school.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.school.dto.HomeworkResponse;
import com.example.school.service.HomeworkService;

@RestController
@RequestMapping("/api/homework")
public class HomeworkController {

    private final HomeworkService homeworkService;

    public HomeworkController(HomeworkService homeworkService) {
        this.homeworkService = homeworkService;
    }

    @GetMapping("/{id}")
    public HomeworkResponse getHomework(@PathVariable Long id) {
        return homeworkService.getHomework(id);
    }
}
```

Restart and try it (it's a `GET /api/...`, so no login needed):

```bash
curl -i http://localhost:8080/api/homework/1
```

```
HTTP/1.1 200 
Content-Type: application/json

{"id":1,"title":"delectus aut autem","completed":false}
```

🎉 Our app called the internet, got the JSON, turned it into a record — and served it to **our** client, **without** `userId`:

```
 curl ──GET /api/homework/1──► 🏫 our app ──GET /todos/1──► 🌍 jsonplaceholder
      ◄── {"id":1,"title":...} ◄─────── {"userId":1,"id":1,...} ◄──
```

---

## 😱 Part 5: When things go wrong

### 🔍 The other API says 404

JSONPlaceholder has only 200 to-dos. Try `curl -i http://localhost:8080/api/homework/999`:

```
HTTP/1.1 500 
Content-Type: application/problem+json

{"detail":"Something went wrong on our side. Please try again later.","instance":"/api/homework/999","status":500,"title":"Server error"}
```

And our log (shortened):

```
ERROR ... c.e.s.exception.GlobalExceptionHandler   : Unexpected error
org.springframework.web.client.HttpClientErrorException$NotFound: 404 Not Found: "{}"
```

`retrieve()` **throws** an exception for every 4xx or 5xx answer. Our catch-all makes it a **500**. But it's not **our** fault — the homework simply doesn't exist. It should be a **404**! 🤔

The fix: tell `RestClient` what to do with a 404, using **`.onStatus(...)`**:

```java
public HomeworkResponse getHomework(Long id) {
    return homeworkRestClient.get()
            .uri("/todos/{id}", id)
            .retrieve()
            .onStatus(status -> status.value() == 404, (request, response) -> {
                throw new HomeworkNotFoundException(id);
            })
            .body(HomeworkResponse.class);
}
```

**`exception/HomeworkNotFoundException.java`**

```java
package com.example.school.exception;

public class HomeworkNotFoundException extends RuntimeException {

    public HomeworkNotFoundException(Long id) {
        super("Homework with id " + id + " was not found");
    }
}
```

**In `GlobalExceptionHandler`:**

```java
@ExceptionHandler(HomeworkNotFoundException.class)
public ProblemDetail handleHomeworkNotFound(HomeworkNotFoundException ex) {
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
    problem.setTitle("Homework not found");
    return problem;
}
```

| Code | Meaning |
|---|---|
| `.onStatus(status -> status.value() == 404, ...)` | ⭐ "**If** the answer's status is 404..." (The first lambda is the **question**.) |
| `(request, response) -> { throw new HomeworkNotFoundException(id); }` | "...**then** throw **our** exception." (The second lambda is the **action**.) |

Now `/api/homework/999` answers:

```
HTTP/1.1 404 
Content-Type: application/problem+json

{"detail":"Homework with id 999 was not found","instance":"/api/homework/999","status":404,"title":"Homework not found"}
```

✅ Much better!

### 🐢 The other API is slow — or down

What if the bakery is **closed**, or takes **forever**? Without a limit, our app would wait... and wait... and our **own** clients would wait too. 😴 Always set **timeouts**:

```java
@Bean
public RestClient homeworkRestClient(@Value("${school.homework.base-url}") String baseUrl) {
    SimpleClientHttpRequestFactory requestFactory = new SimpleClientHttpRequestFactory();
    requestFactory.setConnectTimeout(Duration.ofSeconds(2));
    requestFactory.setReadTimeout(Duration.ofSeconds(5));

    return RestClient.builder()
            .baseUrl(baseUrl)
            .requestFactory(requestFactory)
            .build();
}
```

(Imports: `java.time.Duration`, `org.springframework.http.client.SimpleClientHttpRequestFactory`.)

| Code | Meaning |
|---|---|
| `setConnectTimeout(Duration.ofSeconds(2))` | "If you can't even **reach** the other server in 2 seconds, give up." 📵 |
| `setReadTimeout(Duration.ofSeconds(5))` | "If the answer doesn't **arrive** within 5 seconds, give up." ⏱️ |
| `.requestFactory(requestFactory)` | Use these settings for all requests of this client. |

When a timeout happens, `RestClient` throws a **`ResourceAccessException`**. You could catch it and answer **503 Service Unavailable** ("the homework service isn't available right now") — see "Try it yourself".

⭐ **The golden rule:** never trust another API to be fast, correct or even **there**. Your app must survive when it isn't. 🛡️

---

## 💻 Mini project: All homework of one student 📋

JSONPlaceholder can also give a **list**: **https://jsonplaceholder.typicode.com/todos?userId=1** (all 20 to-dos of user 1).

Build **`GET /api/homework?userId=1`** that answers with a **summary**:

```json
{"userId":1,"total":20,"completed":11,"titles":["delectus aut autem", ...]}
```

**Hints:**

- `.uri(uriBuilder -> uriBuilder.path("/todos").queryParam("userId", userId).build())` builds `/todos?userId=1`.
- For a **list**, use `.body(new ParameterizedTypeReference<List<HomeworkResponse>>() {})`.
- Count the completed ones with a stream (Chapter 36).

<details>
<summary>Click to see the answer</summary>

**`dto/HomeworkSummaryResponse.java`**

```java
package com.example.school.dto;

import java.util.List;

public record HomeworkSummaryResponse(Long userId, int total, long completed, List<String> titles) {
}
```

**In `HomeworkService`:**

```java
public HomeworkSummaryResponse getSummary(Long userId) {
    List<HomeworkResponse> tasks = homeworkRestClient.get()
            .uri(uriBuilder -> uriBuilder.path("/todos").queryParam("userId", userId).build())
            .retrieve()
            .body(new ParameterizedTypeReference<List<HomeworkResponse>>() {});

    long completed = tasks.stream()
            .filter(HomeworkResponse::completed)
            .count();
    List<String> titles = tasks.stream()
            .map(HomeworkResponse::title)
            .toList();
    return new HomeworkSummaryResponse(userId, tasks.size(), completed, titles);
}
```

(Imports: `java.util.List`, `org.springframework.core.ParameterizedTypeReference`, `com.example.school.dto.HomeworkSummaryResponse`.)

| Code | Meaning |
|---|---|
| `uriBuilder -> uriBuilder.path("/todos").queryParam("userId", userId).build()` | Build the address **with** a request parameter → `/todos?userId=1`. |
| `new ParameterizedTypeReference<List<HomeworkResponse>>() {}` | ⭐ Java "forgets" the `<HomeworkResponse>` part of a `List` at runtime. This little trick (with `{}` at the end!) keeps it, so Jackson knows **what** to put in the list. |
| `.filter(HomeworkResponse::completed)` | Keep only tasks where `completed()` is `true`. |
| `.count()` | How many are left → a `long`. |

**In `HomeworkController`:**

```java
@GetMapping
public HomeworkSummaryResponse getSummary(@RequestParam Long userId) {
    return homeworkService.getSummary(userId);
}
```

(Import `org.springframework.web.bind.annotation.RequestParam`.)

`curl "http://localhost:8080/api/homework?userId=1"` → `{"userId":1,"total":20,"completed":11,"titles":["delectus aut autem","quis ut nam facilis et officia qui",...]}`. (The numbers come from JSONPlaceholder's test data; if they ever change it, yours may differ.)

</details>

---

## ✋ Try it yourself

1. Change `school.homework.base-url` to `https://jsonplaceholder.typicode.co` (a missing `m`). What happens when you call `/api/homework/1`?
2. Catch `ResourceAccessException` in `GlobalExceptionHandler` and answer **503** with the title `"Service unavailable"`.
3. JSONPlaceholder also has **users**: `https://jsonplaceholder.typicode.com/users/1`. Make a record with `name` and `email`, and an endpoint `/api/homework/users/1`.

<details>
<summary>Click to see the answers</summary>

1. The address can't be found → `RestClient` throws a `ResourceAccessException` ("I/O error on GET request...") → our catch-all → **500**. That's the "bakery is closed" case.
2. ```java
   @ExceptionHandler(ResourceAccessException.class)
   public ProblemDetail handleServiceUnavailable(ResourceAccessException ex) {
       logger.warn("An external service could not be reached", ex);
       ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.SERVICE_UNAVAILABLE,
               "The homework service is not available right now. Please try again later.");
       problem.setTitle("Service unavailable");
       return problem;
   }
   ```
   (Import `org.springframework.web.client.ResourceAccessException`.) Now the typo from task 1 gives **503** — an honest answer: "it's not your fault, and not really ours — someone else is down".
3. `public record HomeworkUserResponse(Long id, String name, String email) { }`, then `homeworkRestClient.get().uri("/users/{id}", id).retrieve().body(HomeworkUserResponse.class)`. For user 1 → `{"id":1,"name":"Leanne Graham","email":"Sincere@april.biz"}`.

</details>

---

## ⚠️ Common mistakes

### Mistake 1: Field names that don't match the JSON

`record HomeworkResponse(Long id, String name, boolean done)` → `name` and `done` stay `null`/`false`, because the JSON says `title` and `completed`. **No error!** 😱 **Fix:** Use the **exact** JSON names (or `@JsonProperty("title")` on the field).

### Mistake 2: No timeouts

One slow external API can make **your whole app** slow. **Fix:** Always set connect and read timeouts.

### Mistake 3: Every external error becomes a 500

**Fix:** Use `.onStatus(...)` for answers you expect (like 404), and handle `ResourceAccessException` (→ 503).

### Mistake 4: The URL written inside the code

**Fix:** Put base URLs in `application.properties` — then tests and other servers can use a different address.

### Mistake 5: `List.class` for a list

`.body(List.class)` gives you a list of **maps**, not of records. **Fix:** `new ParameterizedTypeReference<List<HomeworkResponse>>() {}`.

---

## ✅ Summary

- Our app can be a **client** too 🔄: it calls other APIs with **`RestClient`**.
- Make one `RestClient` bean per external API: `RestClient.builder().baseUrl(...).build()`, with the URL from **settings**.
- `client.get().uri("/todos/{id}", id).retrieve().body(MyRecord.class)` — Jackson turns the JSON into a record 🪄. Unknown JSON fields are ignored.
- For lists: `.body(new ParameterizedTypeReference<List<MyRecord>>() {})`.
- Errors: `retrieve()` throws for 4xx/5xx → use **`.onStatus(...)`** to throw your own exceptions. No answer → `ResourceAccessException` → **503**.
- Always set **timeouts** ⏱️. Never trust another API to be fast or even there. 🛡️

---

## ❓ Quiz

1. In the kitchen story, why is the kitchen both a server and a client?
2. What do `.get()`, `.uri(...)`, `.retrieve()` and `.body(...)` do?
3. The JSON has a field `userId`, but our record doesn't. What happens?
4. Why did `/api/homework/999` first answer 500?
5. What's the difference between the connect timeout and the read timeout?
6. Why do we need `ParameterizedTypeReference` for a list?
7. Which status code fits best when an external API is down?

<details>
<summary>Click to see the answers</summary>

1. It serves lunch to the students (server) and orders bread from the bakery (client).
2. `get()`: make a GET request. `uri(...)`: the address. `retrieve()`: send it and get the answer. `body(...)`: turn the body into a Java object.
3. Nothing bad — Jackson ignores fields the record doesn't have.
4. `retrieve()` threw `HttpClientErrorException.NotFound`, and our catch-all handler turned it into a 500.
5. Connect timeout: how long to wait to **reach** the server. Read timeout: how long to wait for the **answer**.
6. Java forgets the type inside `List<...>` at runtime; `ParameterizedTypeReference` keeps it so Jackson knows what to create.
7. **503 Service Unavailable**.

</details>

---

[⬅ Previous chapter](89-thymeleaf.md) | [Table of Contents](../README.md) | [Next chapter: Scheduling ➡](91-scheduling.md)
