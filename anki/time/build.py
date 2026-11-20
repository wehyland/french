"""Build Lesson 004 with genanki 0.13.1 and macOS Thomas fr_FR speech."""
from pathlib import Path
from collections import Counter
import array
import html
import io
import json
import sqlite3
import subprocess
import tempfile
import wave
import zipfile
import genanki

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = 'assimil-04'
# Stable vocabulary ID, French, meaning, example, example meaning, tags, notes.
ENTRIES = [
('fr-0147', 'Pardon, est-ce que vous avez l’heure ?', 'Excuse me, do you have the time?', 'Pardon, est-ce que vous avez l’heure ?', 'Excuse me, do you have the time?', 'a1,time,question', 'Learn this polite question as a chunk. The s in vous links to avez with a z sound; the h in heure is silent.'),
('fr-0148', 'Je n’ai pas de montre.', 'I do not have a watch.', 'Je n’ai pas de montre.', 'I do not have a watch.', 'a1,time,negation', 'Ne…pas makes the statement negative; ne becomes n’ before ai. In this negative construction, une montre becomes pas de montre.'),
('fr-0149', 'Je pense que…', 'I think that…', 'Je pense qu’il est midi dix.', 'I think it is ten past noon.', 'a1,verb,expression', 'Penser que + statement. Que becomes qu’ before il. Learn the supplied forms as chunks; no conjugation table is required.'),
('fr-0150', 'Il est midi dix.', 'It is ten past noon.', 'Il est midi dix.', 'It is ten past noon.', 'a1,time,expression', 'Midi dix = 12:10 at midday. Il is an impersonal subject here. At the end of midi dix, the x in dix sounds like s.'),
('fr-0151', 'J’ai rendez-vous à midi.', 'I have an appointment at noon.', 'J’ai rendez-vous à midi.', 'I have an appointment at noon.', 'a1,time,expression', 'Avoir rendez-vous = to have an appointment; à midi = at noon. This expression has no article before rendez-vous.'),
('fr-0152', 'J’ai rendez-vous avec ma femme.', 'I have an appointment with my wife.', 'J’ai rendez-vous avec ma femme à midi.', 'I have an appointment with my wife at noon.', 'a1,time,expression', 'Avoir rendez-vous avec + person. Ma femme means my wife here; learn the supplied possessive as part of the phrase. Femme sounds like fam.'),
('fr-0153', 'Elle a toujours dix minutes de retard.', 'She is always ten minutes late.', 'Elle a toujours dix minutes de retard.', 'She is always ten minutes late.', 'a1,time,expression', 'Avoir + duration + de retard = to be that much late. Retard is a masculine noun, delay/lateness. Before minutes, dix is pronounced di, without a final s.'),
('fr-0154', 'Mais comment le savez-vous ?', 'But how do you know?', 'Mais comment le savez-vous ?', 'But how do you know?', 'a1,time,recognition', 'Recognition chunk. Savez comes from savoir, to know; le refers to the information just mentioned, not the article the. Inversion is not a production requirement.'),
('fr-0155', 'une heure', 'an hour; time (in telling the time)', 'Vous avez l’heure ?', 'Do you have the time?', 'a1,noun,time', 'Feminine noun; definite form l’heure. Learn the gender with une; the h is silent.'),
('fr-0156', 'une montre', 'a watch', 'Je n’ai pas de montre.', 'I do not have a watch.', 'a1,noun,time', 'Feminine noun. The example means I do not have a watch; negative pas de is explained on the phrase card.'),
('fr-0157', 'une femme', 'a woman; a wife', 'J’ai rendez-vous avec ma femme.', 'I have an appointment with my wife.', 'a1,noun,people', 'Feminine noun. Ma femme means my wife in the dialogue. Femme sounds like fam.'),
('fr-0158', 'un rendez-vous', 'an appointment; a meeting', 'J’ai rendez-vous à midi.', 'I have an appointment at noon.', 'a1,noun,time', 'Masculine noun. In avoir rendez-vous, omit the article. The final s in rendez-vous is silent.'),
('fr-0159', 'une minute', 'a minute', 'Elle a dix minutes de retard.', 'She is ten minutes late.', 'a1,noun,time', 'Feminine noun. In dix minutes, the x in dix is silent.'),
('fr-0160', 'midi', 'noon; midday', 'Il est midi.', 'It is noon.', 'a1,noun,time', 'Masculine noun, normally without an article in il est midi and à midi.'),
('fr-0161', 'parce que', 'because', 'Parce que j’ai rendez-vous à midi.', 'Because I have an appointment at noon.', 'a1,connector', 'Gives a reason. Que becomes qu’ before a vowel, as in parce qu’il…; before j’ai it remains parce que.'),
('fr-0162', 'toujours', 'always (in this dialogue)', 'Elle a toujours dix minutes de retard.', 'She is always ten minutes late.', 'a1,adverb,time', 'Can also mean still in other contexts. The final s is silent.'),
]
# Stable key, group, vocabulary ID, front, complete spoken French answer, meaning, extra explanation.
CARDS = [
('ask-time', 'Speaking', 'fr-0147', 'Ask politely: “Excuse me, do you have the time?”', 'Pardon, est-ce que vous avez l’heure ?', 'Excuse me, do you have the time?', 'Accept equivalent polite questions; this is the lesson’s model.'),
('no-watch', 'Speaking', 'fr-0148', 'Say: “I don’t have a watch.”', 'Je n’ai pas de montre.', 'I don’t have a watch.', ''),
('think', 'Speaking', 'fr-0149', 'Say the opening phrase: “I think that…”', 'Je pense que…', 'I think that…', 'Only the opening phrase is required.'),
('time', 'Speaking', 'fr-0150', 'Say: “It’s ten past noon.”', 'Il est midi dix.', 'It’s ten past noon.', ''),
('appointment', 'Speaking', 'fr-0151', 'Say: “I have an appointment at noon.”', 'J’ai rendez-vous à midi.', 'I have an appointment at noon.', ''),
('wife', 'Speaking', 'fr-0152', 'Say: “I have an appointment with my wife.”', 'J’ai rendez-vous avec ma femme.', 'I have an appointment with my wife.', ''),
('late', 'Speaking', 'fr-0153', 'Say: “She is always ten minutes late.”', 'Elle a toujours dix minutes de retard.', 'She is always ten minutes late.', ''),
('reply', 'Comprehension', 'fr-0148', 'Je n’ai pas de montre mais je pense qu’il est midi dix.', 'Je n’ai pas de montre mais je pense qu’il est midi dix.', 'I don’t have a watch, but I think it’s ten past noon.', 'Mais = but; je pense qu’il est… = I think it is… Give the meaning; do not reproduce the sentence.'),
('know', 'Comprehension', 'fr-0154', 'Mais comment le savez-vous ?', 'Mais comment le savez-vous ?', 'But how do you know?', 'Equivalent English translations are fine.'),
('reason', 'Comprehension', 'fr-0152', 'Parce que j’ai rendez-vous avec ma femme à midi.', 'Parce que j’ai rendez-vous avec ma femme à midi.', 'Because I have an appointment with my wife at noon.', 'Parce que = because. Give the meaning; you are not being tested on constructing this longer sentence.'),
('hour', 'Vocabulary', 'fr-0155', 'Say: “an hour”. Include the indefinite article.', 'une heure', 'an hour', ''),
('watch', 'Vocabulary', 'fr-0156', 'Say: “a watch”. Include the indefinite article.', 'une montre', 'a watch', ''),
('woman', 'Vocabulary', 'fr-0157', 'Say: “a woman / a wife”. Include the indefinite article.', 'une femme', 'a woman; a wife', ''),
('meeting', 'Vocabulary', 'fr-0158', 'Say: “an appointment / a meeting”. Include the indefinite article.', 'un rendez-vous', 'an appointment; a meeting', ''),
('minute', 'Vocabulary', 'fr-0159', 'Say: “a minute”. Include the indefinite article.', 'une minute', 'a minute', ''),
('noon', 'Vocabulary', 'fr-0160', 'Say: “noon”.', 'midi', 'noon', ''),
('because', 'Vocabulary', 'fr-0161', 'Say: “because”.', 'parce que', 'because', ''),
('always', 'Vocabulary', 'fr-0162', 'Say: “always”.', 'toujours', 'always', ''),
('gap-de', 'Patterns', 'fr-0148', 'Complete with one word: Je n’ai pas ___ montre.\nMeaning: I don’t have a watch.', 'Je n’ai pas de montre.', 'I don’t have a watch.', 'Missing word: de. Read the short rule on the back of the no-watch phrase card before trying this pattern.'),
('gap-at', 'Patterns', 'fr-0151', 'Complete with one word: J’ai rendez-vous ___ midi.\nMeaning: I have an appointment at noon.', 'J’ai rendez-vous à midi.', 'I have an appointment at noon.', 'Missing word: à. Learn à midi as a chunk.'),
('gap-delay', 'Patterns', 'fr-0153', 'Complete with one word: Elle a dix minutes de ___.\nMeaning: She is ten minutes late.', 'Elle a dix minutes de retard.', 'She is ten minutes late.', 'Missing word: retard. Learn avoir dix minutes de retard as a chunk.'),
]


def audio_stats(data):
    with wave.open(io.BytesIO(data)) as wav:
        assert wav.getsampwidth() == 2 and wav.getnchannels() == 1
        duration = wav.getnframes() / wav.getframerate()
        samples = array.array('h', wav.readframes(wav.getnframes()))
    assert duration > .35 and len(samples) > 1000
    peak = max(abs(s) for s in samples)
    rms = (sum(s*s for s in samples) / len(samples)) ** .5
    assert peak > 300 and rms > 50, (duration, peak, rms)
    assert sum(abs(s) >= 32760 for s in samples) / len(samples) < .001
    return round(duration, 3)


def build():
    assert len(CARDS) == len({c[0] for c in CARDS}) == 21
    entries = {e[0]: e for e in ENTRIES}
    canonical = (ROOT / 'vocabulary/entries.md').read_text()
    for ident in entries:
        assert canonical.count('| ' + ident + ' |') == 1, ident
    model = genanki.Model(1863312401, 'French time — single direction v1',
        fields=[{'name': n} for n in ['ID', 'Front', 'French', 'Meaning', 'Notes', 'Audio', 'Mode']],
        templates=[{'name': 'Recall', 'qfmt': '<div class="mode">{{Mode}}</div><div class="prompt">{{Front}}</div>',
        'afmt': '{{FrontSide}}<hr id="answer"><div lang="fr">{{French}}</div><div class="meaning">{{Meaning}}</div>{{Audio}}<div class="notes">{{Notes}}</div><div class="credit">Synthesized audio · Thomas · French (France) · 140 wpm</div>'}],
        css='.card {font-family: Arial; font-size: 25px; text-align: center; padding: 20px; line-height: 1.5;} .mode,.credit {font-size: 13px; color: #777;} .prompt {white-space: pre-line;} .meaning {margin-top: 12px;} .notes {font-size: 18px; margin-top: 20px;}')
    groups = ['Speaking', 'Comprehension', 'Vocabulary', 'Patterns']
    decks = {g: genanki.Deck(1863312411+i, 'Assimil French::Lesson 004::'+g) for i,g in enumerate(groups)}
    media, report = {}, {}
    preview = ['# Assimil French — Lesson 004: L’heure', '', 'Source: learner-supplied dialogue and three glossary screenshots, 2026-11-20. These are flashcard references with answers, separate from graded grammar exercises.', '', 'Say the French for Speaking and Vocabulary; give the English meaning for Comprehension; supply one missing word for Patterns. Equivalent grammatical responses are acceptable. Learn the phrases as chunks. Study Speaking answers and notes before Patterns; new grammar is explained there.', '', '| # | Type | Front | French answer | Meaning | Notes |', '| --- | --- | --- | --- | --- | --- |']
    for i,(key, group, ident, front, french, meaning, extra) in enumerate(CARDS, 1):
        filename = f'fr-time-{key}-thomas.wav'
        target = HERE / 'audio' / filename
        target.parent.mkdir(exist_ok=True)
        if not target.exists():
            with tempfile.TemporaryDirectory() as tmp:
                aiff = Path(tmp) / 'speech.aiff'
                subprocess.run(['say', '-v', 'Thomas', '-r', '140', '-o', str(aiff), french.replace('…', '.')], check=True)
                subprocess.run(['afconvert', '-f', 'WAVE', '-d', 'LEI16', str(aiff), str(target)], check=True)
        report[filename] = audio_stats(target.read_bytes())
        media[filename] = str(target)
        notes = ' '.join(filter(None, [entries[ident][6], extra]))
        decks[group].add_note(genanki.Note(model=model, guid=genanki.guid_for('french-time-v1', key),
            fields=[html.escape(x) for x in [ident, front, french, meaning, notes]] + [f'[sound:{filename}]', group],
            tags=[SOURCE, 'time', group.lower(), 'fr_fr']))
        preview.append('| ' + ' | '.join(str(x).replace('\n', '<br>') for x in [i,group,front,french,meaning,notes]) + ' |')
    output = HERE / 'french_time.apkg'
    package = genanki.Package(list(decks.values()))
    package.media_files = list(media.values())
    package.write_to_file(str(output))
    with zipfile.ZipFile(output) as z, tempfile.TemporaryDirectory() as tmp:
        mapping = json.loads(z.read('media'))
        assert set(mapping.values()) == set(media)
        for archive, filename in mapping.items():
            assert z.read(archive) == Path(media[filename]).read_bytes()
            audio_stats(z.read(archive))
        db = Path(tmp) / 'collection.anki2'
        db.write_bytes(z.read('collection.anki2'))
        with sqlite3.connect(db) as conn:
            assert conn.execute('select count(*) from notes').fetchone()[0] == 21
            assert conn.execute('select count(*) from cards').fetchone()[0] == 21
            assert len(set(r[0] for r in conn.execute('select guid from notes'))) == 21
            models = json.loads(conn.execute('select models from col').fetchone()[0])
            t = models[str(model.model_id)]['tmpls'][0]
            assert '{{Audio}}' not in t['qfmt'] and '{{Audio}}' in t['afmt']
            stored_decks = json.loads(conn.execute('select decks from col').fetchone()[0])
            for d in decks.values():
                assert stored_decks[str(d.deck_id)]['name'] == d.name
            for (flds,) in conn.execute('select flds from notes'):
                assert flds.split('\x1f')[5][7:-1] in media
    (HERE / 'cards.md').write_text('\n'.join(preview)+'\n')
    (HERE / 'audio_validation.json').write_text(json.dumps({'voice':'Thomas', 'locale':'fr_FR', 'rate_wpm':140, 'duration_seconds':report}, indent=2)+'\n')
    print('Validated 21 cards:', dict(Counter(c[1] for c in CARDS)))
    print('21 non-silent embedded WAV files; no significant clipping; correct answer-side references; stable unique note GUIDs.')

if __name__ == '__main__':
    build()
