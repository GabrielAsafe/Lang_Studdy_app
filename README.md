# ImageApp

![Python](https://img.shields.io/badge/python-3.10+-blue) ![Flask](https://img.shields.io/badge/flask-2.3+-green)

**ImageApp** é uma aplicação Python/Flask para manipulação de PDFs, textos e dicionários multilíngues, com suporte a leitura de texto, conversão para voz e processamento de arquivos.

---

## Estrutura do Projeto

```
imageApp/
├── app/                     # Código principal da aplicação
│   ├── config_loader.py     # Carregamento de configuração
│   ├── extensions.py        # Extensões Flask
│   ├── routes.py            # Endpoints Flask
│   ├── utils/               # Utilitários de processamento
│   │   ├── dic.py
│   │   ├── parse.py
│   │   ├── pdf.py
│   │   ├── text.py
│   │   ├── tts.py
│   │   └── wordnet.py
│   ├── static/              # CSS, JS e arquivos de configuração
│   │   ├── style.css
│   │   ├── script.js
│   │   └── conf.json
│   └── templates/           # Templates HTML
│       ├── index.html
│       └── gerados/         # PDFs gerados
├── depricated/              # Código legado / testes antigos
├── parser/                  # Arquivos PDF e scripts de parsing
├── en_dict.db               # Dicionário Inglês
├── pt_dict.db               # Dicionário Português
├── run.py                   # Script principal para rodar o app
├── requirements.txt         # Dependências do Python
└── README.md
```

---

## Funcionalidades

- Upload e parsing de PDFs e textos.
- Conversão de texto para voz (TTS).
- Consulta e manipulação de dicionários multilíngues (`en_dict.db`, `pt_dict.db`).
- Geração de arquivos HTML/PDF processados.
- Interface web com Flask para interação do usuário.

---

## Pré-requisitos

- Python 3.10+  
- Flask 2.3+  
- Dependências listadas em `requirements.txt`

Instalação de dependências:

```bash
pip install -r requirements.txt
```

---

## Executando a Aplicação

1. Certifique-se de estar na pasta raiz do projeto (`imageApp`).
2. Execute o servidor Flask:

```bash
python run.py
```

3. Acesse a aplicação pelo navegador:

```
http://127.0.0.1:5000/
```

---

## Estrutura de Utilitários

- **pdf.py**: funções para manipulação de PDFs.
- **text.py**: manipulação de textos e limpeza.
- **tts.py**: conversão de texto para fala.
- **parse.py**: parsing de arquivos e extração de informações.
- **dic.py / wordnet.py**: manipulação de dicionários e consultas.

---

## Docker (Opcional)

Você pode rodar a aplicação via Docker:

```bash
docker build -t imageapp .
docker run -p 5000:5000 imageapp
```

---

## Observações

- Arquivos gerados ficam em `app/templates/gerados/`.
- Configurações do app podem ser ajustadas em `app/static/conf.json`.
- Código legado e testes antigos estão em `depricated/`.

---

## Contato

Gabriel – Desenvolvedor Principal  
Projeto criado para estudos e automação de manipulação de textos e PDFs.

