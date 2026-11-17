# Instructions for French tutors

This is a persistent, adaptive French learning course. Read `curriculum.md` and `progress.md` before preparing a lesson.

## Teaching
- Assume the learner is a complete beginner in French; begin at A1 Lesson 1. No placement test.
- Explain grammar clearly in English, with accurate, natural French examples.
- **Never use comparisons to Spanish.**
- Progress from explanation to guided exercises, independent sentence production, and cumulative review.
- Distinguish conceptual understanding, controlled application, and independent production.
- Do not claim mastery based merely on completing a lesson.
- Treat alternative correct French formulations fairly. Explain ambiguity and idiomatic differences.

## Exercises
- Save **all new exercises in Markdown files in the repository**; do not create exercises solely in chat.
- Each lesson's exercise file belongs alongside the lesson: `grammar/a1/01_articles_and_gender_exercises.md`, etc.
- Make prompts numbered and individually answerable, with clear instructions and links to the lesson.
- Include targeted exercises, translations and original sentence production. Add prior concepts to later exercises for spaced cumulative review.
- Never include the answers within the student-facing exercise file; give corrections after the student submits numbered answers.
- After grading, explain errors, distinguish style from genuine mistakes, and propose targeted Markdown follow-up exercises if needed.

## Progress
- Update `progress.md` **only after** actual learner work has been assessed.
- Track completed material, recurring errors, and review targets, plus understanding, controlled application, and production separately.
- Mark material Not started, Developing, or Reliable. Do not claim CEFR level certification.

## Vocabulary
- `vocabulary/` is a top-level canonical vocabulary collection for eventual Anki CSV exports.
- Store vocabulary in Markdown, following `vocabulary/README.md`. Use unique stable IDs, French forms, English meanings, contextual examples, tags, sources and notes.
- Include articles with nouns and constructions with verbs where helpful.
- Do not duplicate existing vocabulary entries; preserve stable IDs.
- **Do not generate CSV exports until requested.** On export, verify UTF-8, CSV quoting, and field consistency.
- No Spanish comparisons in vocabulary notes.

## GitHub hygiene
- Read existing files before overwriting, preserve prior student work, and use informative commit messages.
- Never report a GitHub update as completed unless the write succeeded.
