# Master Plan

This file explains **how** the course is designed. Learners do not need to read it. It is for anyone writing or checking the course.

---

## 1. The main idea

> Do not just teach a rule and give an example. Explain the example itself, explain the grammar inside it, explain how the rules connect, remind the learner of anything they may have forgotten, and show how to use the same knowledge in new situations.

## 2. Writing rules for every file

1. Use simple English. Short sentences. Common words.
2. Explain a grammar word **before** using it. Add new terms to [GLOSSARY.md](GLOSSARY.md).
3. Never assume the learner remembers an earlier lesson. Give a short reminder and a link.
4. Explain **why**, not only **what**.
5. Every wrong sentence is clearly marked with ❌. Every correct sentence used as a contrast is marked with ✅.
6. Use natural English. No strange sentences made only to show a rule.
7. Do not repeat an example with only a new name. Each example must teach something new (new context, new form, new difficulty).
8. When more than one form is correct, say so. Explain differences between formal / informal, spoken / written, and British / American where it matters.
9. Do not invent rules that do not exist.

## 3. The 10 levels

| Level | Name | Approx. CEFR | Folder(s) |
|---|---|---|---|
| L0 | Absolute beginner (foundations) | Pre-A1 | `00-foundations` |
| L1 | Basic words and sentences | A1 | `01-beginner-grammar` |
| L2 | Beginner grammar | A1–A2 | `01-beginner-grammar` |
| L3 | Elementary English | A2 | `02-intermediate-grammar` |
| L4 | Pre-intermediate | A2–B1 | `02-intermediate-grammar` |
| L5 | Intermediate | B1 | `02-intermediate-grammar`, `04-grammar-combinations` |
| L6 | Upper-intermediate | B2 | `03-advanced-grammar`, `04-grammar-combinations` |
| L7 | Advanced grammar and communication | C1 | `03-advanced-grammar` |
| L8 | Natural and fluent English | C1 | `06-spoken-english`, `09-vocabulary` |
| L9 | Advanced writing, reading and style | C1–C2 | `10-writing`, `07-reading-and-stories` |

CEFR is used only as a guide. Topic coverage is controlled by [CURRICULUM_MAP.md](CURRICULUM_MAP.md).

Every level contains: grammar, vocabulary, reading, writing, listening, speaking, pronunciation, revision and tests.

## 4. Identifiers (IDs)

Every item gets a stable ID that never changes.

| Item | Format | Example |
|---|---|---|
| Lesson | `L-###` | `L-001` |
| Example sentence | `EX-<lesson>-<number>` | `EX-005-012` |
| Integrated (cross-topic) example | `IX-#####` | `IX-00001` |
| Grammar combination | `C-###` | `C-001` |
| Story | `S-###` | `S-001` |
| Dialogue | `D-###` | `D-001` |
| Exercise set | `E-###` (answers `A-###`) | `E-001` |
| Review | `R-###` | `R-001` |
| Vocabulary entry | `V-####` | `V-0001` |

File names: `lesson-001-what-is-a-language.md`, `combination-001-either-or-with-modal-verbs.md`, `story-001-a-day-at-school.md`, `exercise-001-...md`, `answers-001-...md`, `review-001-...md`.

## 5. Lesson structure (every major lesson)

1. Lesson number and title
2. Level and prerequisites
3. Learning objectives
4. Why this topic matters
5. Simple introduction
6. Definition in easy English
7. Key words (terminology)
8. Detailed explanation
9. Basic sentence patterns
10. Rules and exceptions
11. Positive examples
12. Negative examples
13. Questions and answers
14. Detailed sentence analysis
15. Common mistakes
16. Related grammar points
17. Grammar combinations
18. Conversation examples
19. Story examples
20. Pronunciation and listening notes
21. Vocabulary connections
22. Guided practice
23. Your own practice (exercises)
24. Answer key with explanations
25. Quick revision sheet
26. Memory tricks and patterns
27. Self-check list
28. What you need for the next lesson
29. When to review
30. Links to related lessons

Small foundation lessons (L0) may merge some sections, but must never skip explanations.

## 6. Example teaching template (major examples)

```
### EX-###-### — "<sentence>"
- Meaning in simple English:
- Situation:
- Main lesson:
- Grammar in this sentence:
- Sentence structure (parts):
- Subject: (and how to find it)
- Verb: (form and job)
- Helping verbs:
- Object / complements / modifiers:
- Word by word:
- How the rules work together here:
- Remember from before: (short reminders + links)
- Why this is correct:
- Other versions: (change tense / pronoun / etc.)
- Wrong versions ❌ and corrections ✅:
- In natural speech:
- Writing and punctuation:
- Pronunciation:
- Pattern you can reuse:
- More examples with the same pattern:
- Quick check question:
```

Fields may be left out only if they truly do not apply (for example, "helping verbs" in a one-word sentence). Smaller examples still get a short explanation.

## 7. Example production strategy

- Target: **100+ examples** for every major grammar topic and every important combination; **10,000+ integrated examples** across the course.
- Each topic's 100 examples follow the difficulty ladder:
  1. One rule, very short sentence
  2. Same rule, new nouns and verbs
  3. Same rule, with pronouns
  4. Questions and negatives
  5. Different tenses (only tenses already taught)
  6. Two topics combined
  7. Three topics combined
  8. Long sentences
  9. Conversations
  10. Stories
  11. Real writing tasks
  12. Telling similar structures apart
- Variety checklist per topic: different subjects, names, pronouns, singular/plural, countable/uncountable, contexts (home, school, work, shop, travel, health, technology, feelings, opinions, formal, informal).
- Only use grammar the learner has already met, **or** explain the new piece right there in simple words and mark it "(you will learn this fully in Lesson X)".
- Full template for roughly the first 20–30 examples of a topic and every integrated example; shorter explanations for the rest — but every example has some explanation.
- Every example is logged in [EXAMPLE_CATALOG.md](EXAMPLE_CATALOG.md) to stop duplicates.

## 8. Grammar combination system

See [GRAMMAR_COMBINATION_MATRIX.md](GRAMMAR_COMBINATION_MATRIX.md). A combination is only taught after **all** its parts are taught. Each combination file follows the 20-step method in that file.

## 9. Revision system

See [REVISION_SCHEDULE.md](REVISION_SCHEDULE.md). Every lesson ends with a review plan (same day, +1, +3, +7, +14, +30 days, then cumulative). Every review item links back to the lesson and example IDs.

## 10. Skills plan

| Skill | How it is taught |
|---|---|
| Speaking | Every lesson has "say it aloud" tasks; `06-spoken-english` has functions (greeting, asking, apologizing…), role-plays and dialogues D-###. |
| Listening | Written transcripts with pronunciation marks in `08-pronunciation-and-listening`. **No real audio is included**; learners can use a text-to-speech tool or a teacher to read the scripts. |
| Pronunciation | Sounds, IPA explained simply, minimal pairs, stress, rhythm, linking, reductions. Notes appear inside lessons too. |
| Reading | Stories S-### at each level, with full analysis. |
| Writing | From single sentences (L1) to emails, paragraphs and essays (L5–L9) in `10-writing`. |
| Vocabulary | Taught inside lessons; collected in [VOCABULARY_INDEX.md](VOCABULARY_INDEX.md) and `09-vocabulary`. |

## 11. Quality control (after every batch)

1. Grammar check: every correct sentence is really correct and natural.
2. Order check: no lesson uses grammar not yet taught without explaining it.
3. Simplicity check: explanations use easy words; new terms are in the glossary.
4. Duplicate check: new examples compared with the catalog.
5. Link check: all relative links point to real files.
6. Completeness check: a lesson is "complete" only when explanation + examples (target met) + exercises + answers + revision are done.
7. Update [PROGRESS.md](PROGRESS.md) honestly.

## 12. Production stages

1. Design ✅ (this file and the index files)
2. Validate curriculum ✅ (first pass; repeat at the start of each level)
3. Generate lessons — in progress
4. Integrate topics (combinations)
5. Communication materials (dialogues, stories, listening)
6. Revision materials
7. Quality review
8. Continue batch by batch until complete

## 13. Size estimate

| Item | Estimate |
|---|---|
| Core lessons | ~420 |
| Grammar combinations | ~250 |
| Stories | ~120 |
| Dialogues | ~200 |
| Exercise sets + answer keys | ~450 each |
| Reviews / tests | ~150 |
| Example sentences (all) | 50,000+ (including 10,000+ integrated) |

These numbers are a plan, not a promise. Quality is more important than size.
