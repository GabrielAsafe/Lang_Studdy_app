document.addEventListener("click", async (e) => {
  if (!e.target.classList.contains("palavra")) return;

  const palavra = e.target.innerText;

  try {

    const [ortografia, definicao] = await Promise.all([
      verificarOrtografia(palavra),
      verificarDefinicao(palavra)
    ]);

    ler(palavra);

    escreverOrto(ortografia);
    escreverDef(definicao);

    console.log("DEFINICAO:", definicao);

    const dict_search = await buscarNoDicionario(definicao);

    console.log("DIC:", dict_search);

    escreverdicionario(dict_search);

  } catch (err) {
    console.error("Erro:", err);
  }
});


//--------------faz o fetch
const buscarNoDicionario = async (palavra) => {
  const resp = await fetch("/search_On_Dict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ palavra })
  });

  return resp.json();
};


const verificarOrtografia = async (palavra) => {
  const resp = await fetch("/verificar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ palavra })
  });

  console.log(resp)
  return resp.json();
};


const verificarDefinicao = async (palavra) => {
   // console.log(palavra);
  const resp = await fetch("/definitions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ palavra })
  });
  return resp.json();
};


const ler = async (palavra) => {
   // console.log(palavra);
  const resp = await fetch("/ler", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ palavra })
  });
  //return resp.json();
};

//------------ escreve os dados


const escreverOrto = (data) => {
  
  const div = document.querySelector(".Ortografia");
  const status = div.querySelector(".Ortografia_status");
  const sugestoes = div.querySelector(".Ortografia_sugestoes");

    //console.log(data)

    //may no exist on the payload
  if (data.correta) {
    status.textContent = `${data.palavra} está correta`;
    sugestoes.textContent = "";
  } else {
    status.textContent = `${data.palavra} está incorreta`;
    sugestoes.textContent =
      `Sugestões: ${(data.sugestoes || []).join(", ")}`;
  }

};


const escreverDef = (data) => {
  const div = document.querySelector(".definition");
  const status = div.querySelector(".definition_status");
  const sugestoes = div.querySelector(".definition_sugestoes");

  // Mostrar sinônimos
  if(data.sinonimos && data.sinonimos.length > 0){
    status.textContent = data.sinonimos.join(", ");
  } else {
    status.textContent = "";
  }

  // Mostrar definições
  if(data.definicoes_base && data.definicoes_base.length > 0){
    sugestoes.textContent = data.definicoes_base.join(", ");
  } else if(data.definicoes_target && data.definicoes_target.length > 0){
    sugestoes.textContent = data.definicoes_target.join(", ");
  } else {
    sugestoes.textContent = "Sem definições";
  }
};


const escreverdicionario = (data) => {

  const div = document.querySelector(".translation");
  const status = div.querySelector(".translation_status");
  const sugestoes = div.querySelector(".translation_sugestoes");

  if (!data.resultados || data.resultados.length === 0) {
    status.textContent = "Nada encontrado";
    sugestoes.textContent = "";
    return;
  }

  status.textContent = "Dicionário:";

  const textos = data.resultados.map(obj => {
    const palavra = Object.keys(obj)[0];
    return `${palavra}: ${obj[palavra]}`;
  });

  sugestoes.textContent = textos.join(" | ");
};


//--------------------------------------js da página

//painel lateral
const left = document.querySelector(".left");
const toggleBtn = document.getElementById("toggle_left");

toggleBtn.addEventListener("click", () => {
    left.classList.toggle("collapsed");

    // muda ícone da seta
    if(left.classList.contains("collapsed")){
        toggleBtn.innerHTML = "&#9654;"; // ►
    } else {
        toggleBtn.innerHTML = "&#9664;"; // ◄
    }
});



//ler arquivos
document.getElementById('fileInput').addEventListener('change', async (event) => {
  const file = event.target.files[0];

  const formData = new FormData();
  formData.append("file", file);

  const resp = await fetch("/parse_text", {
    method: "POST",
    body: formData
  });

  const text = await resp.text();
  //console.log(text);
});




//refletir config.json no frontend

document.addEventListener("DOMContentLoaded", () => {
    fetch("/static/conf.json")
        .then(response => response.json())
        .then(config => {

            const targetConfig = config.configurations.find(
                item => item.key === "TARGET_LANGUAGE"
            );

            const baseConfig = config.configurations.find(
                item => item.key === "BASE_LANGUAGE"
            );
            
            const choosenVoice = config.configurations.find(
                item => item.key === "CHOOSEN_VOICE"
            );


            if (targetConfig) {
                document.getElementById("target_lang_select").value = targetConfig.default;
            }

            if (baseConfig) {
                document.getElementById("base_lang_select").value = baseConfig.default;
            }

            if (choosenVoice) {
                document.getElementById("base_read_voice").value = choosenVoice.default;
            }


        })
        .catch(error => console.error("Erro ao carregar conf.json:", error));
});


//atualizar conf.js

document.getElementById("configForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const targetLang = document.getElementById("target_lang_select").value;
    const baseLang = document.getElementById("base_lang_select").value;
    const choosenVoice = document.getElementById("base_read_voice").value;


    fetch("/update-config", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            TARGET_LANGUAGE: targetLang,
            BASE_LANGUAGE: baseLang,
            CHOOSEN_VOICE:choosenVoice
        })
    })
    .then(res => res.json())
    .then(data => {
        alert("Configuração atualizada!");
    })
    .catch(err => console.error(err));
});
