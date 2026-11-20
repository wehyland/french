# Assimil French — Lesson 004: L’heure

Import [french_time.apkg](french_time.apkg) into Anki with **File → Import**. The deck is **Assimil French::Lesson 004**, divided into Speaking, Comprehension, Vocabulary, and Patterns. All audio files are inside the package; no separate copying is needed. Enable Anki’s audio autoplay to hear the French when you reveal each answer.

There are **21 cards**: 7 speaking phrases, 3 comprehension prompts, 8 vocabulary prompts, and 3 focused gap cards. Read the Speaking answers and explanations before trying Patterns. Learn the supplied phrases as chunks; unfamiliar conjugations, inversion, and possessives are not separate production requirements. Accept equivalent grammatical phrases and translations. You can add the groups gradually at your own pace.

Audio is **synthesized**, using Apple’s installed **Thomas, French (France)** voice at **140 words per minute**. Complete French answers are spoken, including for the gap cards. Audio appears only on the answer side. The written notes highlight useful pronunciation points: the linking z in *vous avez*, the silent x in *dix minutes*, the final s sound in standalone *dix*, and the pronunciation of *femme*.

The build verifies that all 21 recordings contain audio, have measurable non-silent signal without significant clipping, are embedded intact, and match their cards’ answer-side references. These are technical audio checks, not a claim of human listening review. [audio_validation.json](audio_validation.json) records the voice, rate, and recording durations.

Inspect every card in [cards.md](cards.md). This is a flashcard reference with answers, separate from graded grammar exercises. No lesson completion or mastery has been recorded.

Source: Assimil French **Lesson 004**, identified by the learner, dialogue titled **L’heure** and three vocabulary screenshots supplied 2026-11-20 (11:37:56, 11:38:11, 11:38:24, and 11:38:36). Cards select useful chunks rather than converting every glossary line. Clarifications: *retard* is a masculine noun meaning delay/lateness; *de* in *pas de montre* belongs to the negative noun construction; *le* in *le savez-vous* is a pronoun. These adaptations are not a replacement for the original lesson audio.

Canonical vocabulary: [entries.md](../../vocabulary/entries.md), source `assimil-04`, IDs `fr-0147`–`fr-0162`. Existing vocabulary IDs and other decks are untouched.

To rebuild on macOS, use Python with `genanki==0.13.1`, `say`, `afconvert`, and the installed Thomas voice: `python build.py`. Existing valid recordings are reused. Stable note GUIDs and model/deck IDs allow later updates to these notes without intentionally creating duplicates; retain this package’s identity when modifying it. No CSV is generated.
