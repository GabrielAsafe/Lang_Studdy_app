import re

def txt_para_blockspan(texto):
    texto = texto.strip()
    blocos = texto.split("\n\n")
    html_paragrafos = []

    for bloco in blocos:
        linhas = bloco.strip().split("\n")
        linhas_html = []

        for linha in linhas:
            # Regex para separar palavras e pontuação
            palavras = re.findall(r'\w+|[.,;!?]', linha)
            palavras_span = [f'<span class="palavra">{p}</span>' for p in palavras]
            linha_html = " ".join(palavras_span)
            linhas_html.append(linha_html)

        conteudo = "<br>\n".join(linhas_html)
        html_paragrafos.append(f"<p>{conteudo}</p>")

    return "\n".join(html_paragrafos)


def gerar_html_completo(texto_txt):
    blockspan_content = txt_para_blockspan(texto_txt)

    html_completo = f"""

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Reading app</title>
    <link rel="stylesheet" href="{{{{ url_for('static', filename='style.css') }}}}">
</head>
<body>  
<div class="bd">
    <div class="left">
        <div id="toggle_left">&#9664;</div>
        <h2>Configurações</h2>
        <form id="configForm">
            <label for="target_lang_select">Estou a estudar:</label>
            <select id="target_lang_select">
                <option value="pt_BR">Português</option>
                <option value="en_US">Inglês</option>
                <option value="de_DE">Alemão</option>
            </select>

            <label for="base_lang_select">Meu idioma nativo é:</label>
            <select id="base_lang_select">
                <option value="pt_BR">Português</option>
                <option value="en_US">Inglês</option>
                <option value="de_DE">Alemão</option>
            </select>

            <label for="base_read_voice">A voz de leitura será:</label> <!--vou martelar mas tem que adicionar dinamicamente depois-->
            <select id="base_read_voice">
                <option value="pt-br">Português</option>
                <option value="en-us">Inglês</option>
                <option value="de">Alemão</option>
            </select>
            
            <input type="submit" value="Mudar definições">
        </form>

        <label for="fileInput">seleciona um arquivo para leitura</label>
        <input type="file" id="fileInput" />

    </div>

    <div class="middle">
        {blockspan_content}
    </div>

       <div class="right">
        <div class="actions">
            <h1>Ações</h1>
            <p class="actions_status"></p>
            <p class="actions_sugestoes"></p>
        </div>
        <div class="Ortografia">
            <h1>Ortografia</h1>
            <p class="Ortografia_status"></p>
            <p class="Ortografia_sugestoes"></p>
        </div>
        <div class="translation">
            <h1>Traduções</h1>
            <p class="translation_status"></p>
            <p class="translation_sugestoes"></p>
        </div>
        <div class="definition">
            <h1>Sinônimo(s)</h1>
            <p class="definition_status"></p>
            <h2>Definição(oes)</h2>
            <p class="definition_sugestoes"></p>
        </div>
    </div>
</div>


<script src="{{{{ url_for('static', filename='script.js') }}}}"></script>
</body>
</html>

"""
    return html_completo


# Leitura do arquivo TXT
with open("parser/texto.txt", encoding="utf-8") as f:
    texto = f.read()

html_final = gerar_html_completo(texto)

# Salva ou imprime
with open("app/templates/index.html", "w", encoding="utf-8") as f:
    f.write(html_final)

print("HTML gerado com sucesso!")
