const form = document.getElementById('bookForm');
const previewTitle = document.getElementById('previewTitle');
const previewAuthor = document.getElementById('previewAuthor');
const previewDesc = document.getElementById('previewDesc');
const previewCover = document.getElementById('previewCover');
const previewImg = document.getElementById('previewImg');
const previewPlaceholder = document.getElementById('previewPlaceholder');
const fileName = document.getElementById('fileName');

['titulo','autor','editora','ano_pub','descricao'].forEach(id => {
  const el = document.getElementById(id);
  if(!el) return;
  el.addEventListener('input', updatePreview);
});

function updatePreview(){
  const title = document.getElementById('titulo').value || 'Título do livro';
  const author = document.getElementById('autor').value || '';
  const publisher = document.getElementById('editora').value || '';
  const year = document.getElementById('ano_pub').value || '';
  previewTitle.textContent = title;
  const parts = [author, publisher, year].filter(Boolean).join(' • ');
  previewAuthor.textContent = parts || 'Autor • Editora • Ano';
  const desc = document.getElementById('descricao').value || 'Descrição curta do livro aparecerá aqui.';
  previewDesc.textContent = desc;
}

function handleFile(event) {
  const file = event.target.files[0];
  if (!file) return;

  fileName.textContent = file.name;

  const reader = new FileReader();
  reader.onload = (ev) => {
    previewImg.src = ev.target.result;
    previewImg.style.display = "block";
    previewPlaceholder.style.display = "none";
  };
  reader.readAsDataURL(file);
}

function resetPreview(){
  fileName.textContent = 'Nenhum arquivo selecionado';
  previewImg.src = '';
  previewImg.style.display = 'none';
  previewPlaceholder.style.display = 'block';
  previewTitle.textContent = 'Título do livro';
  previewAuthor.textContent = 'Autor • Editora • Ano';
  previewDesc.textContent = 'Descrição curta do livro aparecerá aqui.';
}

function handleSubmit(e){
  e.preventDefault();
  const data = new FormData(form);
  const obj = {};
  data.forEach((v,k) => {
    obj[k] = v;
  });

  console.log('Dados do livro:', obj);
  alert('Livro salvo (simulação). Abra o console para ver o objeto gerado.');
  form.reset();
  resetPreview();
}
