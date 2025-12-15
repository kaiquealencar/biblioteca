function buscaCep() {
  const cep = document.getElementById("cep").value.replace(/\D/g, "");
  const numeroEndereco = document.getElementById("numero_endereco")

  if (cep.length !== 8) return;

  const url = `https://www.republicavirtual.com.br/web_cep.php?cep=${cep}&formato=json`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      if (data.resultado === "1") {
        const logradouro = 
          (data.tipo_logradouro ? data.tipo_logradouro + " " : "") + data.logradouro;

        document.getElementById("logradouro").value = logradouro;
        document.getElementById("bairro").value = data.bairro;
        document.getElementById("cidade").value = data.cidade;
        document.getElementById("uf").value = data.uf;
        numeroEndereco.focus();
      } else {
        alert("CEP não encontrado");
        limparEndereco();
      }


    })
    .catch(() => {
      alert("Erro ao buscar o CEP");
    });
}

function limparEndereco() {
  document.getElementById("logradouro").value = "";
  document.getElementById("bairro").value = "";
  document.getElementById("cidade").value = "";
  document.getElementById("uf").value = "";
}

