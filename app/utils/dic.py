import json
import sqlite3

def createDictionaty(name, filepath):
    conn = sqlite3.connect(name)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS entries (
        word TEXT,
        lang_code TEXT,
        pos TEXT,
        gloss TEXT
    )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_word ON entries(word, lang_code)")



    with open(filepath, encoding="utf-8") as f:
        for linha in f:
            entry = json.loads(linha)

            word = entry.get("word")
            lang = entry.get("lang_code")

            for sense in entry.get("senses", []):
                for gloss in sense.get("glosses", []):
                    cur.execute(
                        "INSERT INTO entries VALUES (?, ?, ?, ?)",
                        (word, lang, entry.get("pos"), gloss)
                    )

    conn.commit()
    conn.close()




def searchEntry(name, langAbrev, wordToSearch):
    conn = sqlite3.connect(name)
    cur = conn.cursor()

    cur.execute("""
    SELECT gloss FROM entries
    WHERE word = ? AND lang_code = ?
    """, (wordToSearch, langAbrev))

    print(cur.fetchall())

name = "en_dict.db"
filepath = "de-extract.jsonl"
langAbrev = 'en'
wordToSearch = "love"
#searchEntry(name,langAbrev,wordToSearch)