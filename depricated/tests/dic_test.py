def naoseidireito():
    import bz2
    import xml.etree.ElementTree as ET

    filename = "ptwiki.xml.bz2"

    def get_text(elem, path):
        found = elem.find(path)
        return found.text if found is not None else None

    with bz2.open(filename, "rb") as f:
        context = ET.iterparse(f, events=("end",))

        for event, elem in context:
            if elem.tag.endswith("page"):

                title = get_text(elem, "{*}title")
                ns = get_text(elem, "{*}ns")

                # Apenas namespace principal (verbetes)
                if ns != "0":
                    elem.clear()
                    continue

                # Ignorar redirects
                if elem.find("{*}redirect") is not None:
                    elem.clear()
                    continue

                text = get_text(elem, "{*}revision/{*}text")

                if text:
                    print("Título:", title)
                    print("Tamanho texto:", len(text))
                    print("-" * 40)

                elem.clear()

def getFilenames():

    import gzip

    filename = "ptwiktionary-20250901-all-titles.gz"
    cnt = 0
    with gzip.open(filename, "rt", encoding="utf-8") as f:
        for line in f:
            cnt +=1


    print(cnt)


import bz2
import re
import sqlite3
import xml.etree.ElementTree as ET

DUMP_FILE = "ptwiki.xml.bz2"
DB_FILE = "wiktionary_pt.db"

# --- Criar base ---
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    pos TEXT,
    definition TEXT,
    translations TEXT
)
""")

conn.commit()

def clean_wiki(text):
    # remove templates {{...}}
    text = re.sub(r"\{\{.*?\}\}", "", text)
    # remove links [[...]]
    text = re.sub(r"\[\[(.*?)\]\]", r"\1", text)
    return text.strip()

with bz2.open(DUMP_FILE, "rb") as f:
    context = ET.iterparse(f, events=("end",))

    for event, elem in context:
        if not elem.tag.endswith("page"):
            continue

        ns = elem.find("{*}ns")
        if ns is None or ns.text != "0":
            elem.clear()
            continue

        title = elem.find("{*}title").text
        text_elem = elem.find("{*}revision/{*}text")

        if text_elem is None or text_elem.text is None:
            elem.clear()
            continue

        text = text_elem.text

        # --- pegar só seção Português ---
        if re.search(r"==\s*Português\s*==", text):

            elem.clear()
            continue

            
        match = re.search(r"==\s*Português\s*==(.+?)(?:\n==|$)", text, re.DOTALL)
        if match:
            section = match.group(1)
        else:
            # se não encontrou, pula a página
            elem.clear()
            continue

        pos = None

        for line in section.splitlines():
            line = line.strip()
            # detectar POS
            if line.startswith("==="):
                pos = line.strip("= ").strip()
            # pegar definições
            if line.startswith("#"):
                definition = re.sub(r"\{\{.*?\}\}", "", line.lstrip("#: ")).strip()
                cur.execute(
                    "INSERT INTO entries (word, pos, definition, translations) VALUES (?, ?, ?, ?)",
                    (title, pos, definition, None)
                )


        elem.clear()

conn.commit()
conn.close()

print("Base criada com sucesso.")
