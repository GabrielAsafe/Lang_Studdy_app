document.addEventListener("click", async (e) => {
  if (!e.target.classList.contains("palavra")) return;

  const palavra = e.target.innerText;

  try {
    const [ortografia, definicao, voz] = await Promise.all([
    verificarOrtografia(palavra),
    verificarDefinicao(palavra),
    ler(palavra)

    ]);


    escreverOrto(ortografia, ".Ortografia");
    escreverDef(definicao, ".definition");


  } catch (err) {
    //console.error("Erro:", err);
    //return err.json()
  }
});

//--------------faz o fetch
const verificarOrtografia = async (palavra) => {
  const resp = await fetch("/verificar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ palavra })
  });

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


const escreverOrto = (data, container) => {
  const div = document.querySelector(container);
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
const div = document.querySelector(".definition"); // container
const status = div.querySelector(".definition_status"); // classe
const sugestoes = div.querySelector(".definition_sugestoes"); // classe

  console.log(data);

  if(data.sinonimos && data.sinonimos.length > 0){
    status.textContent = data.sinonimos.join(", ");
  }

  if(!data.definicoes || data.definicoes.every(d => d.trim() === "")){
    sugestoes.textContent = data.definicoesEN.join(", ");
  }else{
    sugestoes.textContent = data.definicoes.join(", ");
  }
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

document.getElementById('fileInput').addEventListener('change', (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    console.log(file),
    console.log(reader);
    // reader.onload = function () {
    //     const content = reader.result;
    //     console.log(content);
    // };

    // reader.onerror = function () {
    //     console.error('Error reading the file');
    // };

    // reader.readAsText(file, 'utf-8');
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
