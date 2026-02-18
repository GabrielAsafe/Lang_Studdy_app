import json
import sqlite3

# conn = sqlite3.connect("pt_dict.db")
# cur = conn.cursor()

# cur.execute("""
# CREATE TABLE IF NOT EXISTS entries (
#     word TEXT,
#     lang_code TEXT,
#     pos TEXT,
#     gloss TEXT
# )
# """)

# cur.execute("CREATE INDEX IF NOT EXISTS idx_word ON entries(word, lang_code)")



# with open("pt-extract.jsonl", encoding="utf-8") as f:
#     for linha in f:
#         entry = json.loads(linha)

#         word = entry.get("word")
#         lang = entry.get("lang_code")

#         for sense in entry.get("senses", []):
#             for gloss in sense.get("glosses", []):
#                 cur.execute(
#                     "INSERT INTO entries VALUES (?, ?, ?, ?)",
#                     (word, lang, entry.get("pos"), gloss)
#                 )

# conn.commit()
# conn.close()



# conn = sqlite3.connect("pt_dict.db")
# cur = conn.cursor()

# cur.execute("""
# SELECT gloss FROM entries
# WHERE word = ? AND lang_code = ?
# """, ("simples", "pt"))

# print(cur.fetchall())







# conn = sqlite3.connect("en_dict.db")
# cur = conn.cursor()

# cur.execute("""
# CREATE TABLE IF NOT EXISTS entries (
#     word TEXT,
#     lang_code TEXT,
#     pos TEXT,
#     gloss TEXT
# )
# """)

# cur.execute("CREATE INDEX IF NOT EXISTS idx_word ON entries(word, lang_code)")



# with open("simple-extract.jsonl", encoding="utf-8") as f:
#     for linha in f:
#         entry = json.loads(linha)

#         word = entry.get("word")
#         lang = entry.get("lang_code")

#         for sense in entry.get("senses", []):
#             for gloss in sense.get("glosses", []):
#                 cur.execute(
#                     "INSERT INTO entries VALUES (?, ?, ?, ?)",
#                     (word, lang, entry.get("pos"), gloss)
#                 )

# conn.commit()
# conn.close()



# conn = sqlite3.connect("en_dict.db")
# cur = conn.cursor()

# cur.execute("""
# SELECT gloss FROM entries
# WHERE word = ? AND lang_code = ?
# """, ("simple", "en"))

# print(cur.fetchall())





conn = sqlite3.connect("de_dict.db")
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



with open("de-extract.jsonl", encoding="utf-8") as f:
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



conn = sqlite3.connect("de_dict.db")
cur = conn.cursor()

cur.execute("""
SELECT gloss FROM entries
WHERE word = ? AND lang_code = ?
""", ("liebe", "de"))

#print(cur.fetchall())
