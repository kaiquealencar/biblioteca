async function BuscaLeitor() {
    const termo = document.getElementById("busca-leitor").value.trim();
    const divResultado = document.getElementById("resultado-busca-leitor");
    const inputIdLeitor = document.getElementById("leitor-id");

    if (!termo) {
        alert("Por favor, insira um nome ou CPF para buscar.");
        return;
    }

    const formData = new FormData();
    formData.append("busca-leitor", termo);

    try {
        const response = await fetch("/buscar-leitor", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            divResultado.innerHTML = `
                <p><strong>Leitor Encontrado:</strong></p>
                <p><strong>Matrícula:</strong> ${formatarMatricula(data.matricula)}</p>
                <p><strong>Nome:</strong> ${data.nome}</p>
                <p><strong>CPF:</strong> ${data.cpf}</p>
            `;
            inputIdLeitor.value = data.id;
        } else {
            divResultado.innerHTML = `<p style="color: red;">${data.error}</p>`;
            inputIdLeitor.value = "";
        } 
    } catch (error) {
        console.error("Erro na busca do leitor:", error);
        divResultado.innerHTML = `<p style="color: red;">Erro ao buscar leitor. Tente novamente.</p>`;
        inputIdLeitor.value = "";
    }
    
}
async function BuscaLivro() {
    const termo = document.getElementById("busca-livro").value.trim();
    const divResultado = document.getElementById("resultado-busca-livro");
    const inputIdLivro = document.getElementById("livro-id");

    if (!termo) {
        alert("Por favor, insira um título ou ISBN para buscar.");
        return;
    }

    const formData = new FormData();
    formData.append("busca-livro", termo);

    try {
        const response = await fetch("/buscar-livro", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            divResultado.innerHTML = `
                <p><strong>Livro Encontrado:</strong></p>
                <p><strong>Título:</strong> ${data.titulo}</p>
                <p><strong>Autor:</strong> ${data.autor}</p>
                <p><strong>ISBN:</strong> ${data.isbn}</p>
            `;
            inputIdLivro.value = data.id;
        } else {
            divResultado.innerHTML = `<p style="color: red;">${data.error}</p>`;
            inputIdLivro.value = "";
        } 
    } catch (error) {
        console.error("Erro na busca do livro:", error);
        divResultado.innerHTML = `<p style="color: red;">Erro ao buscar livro. Tente novamente.</p>`;
        inputIdLivro.value = "";
    }
    
}

document.getElementById("busca-leitor").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); 
        BuscaLeitor();
    }
});
document.getElementById("busca-livro").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); 
        BuscaLivro();
    }
});

function formatarMatricula(valor) {
    if (!valor) return "N/A";

    const v = String(valor).trim().padStart(5, '0');
    
    return v;
}