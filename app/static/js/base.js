const form = document.getElementById('bookForm');
    const previewTitle = document.getElementById('previewTitle');
    const previewAuthor = document.getElementById('previewAuthor');
    const previewDesc = document.getElementById('previewDesc');
    const previewCover = document.getElementById('previewCover');
    const fileName = document.getElementById('fileName');

    // live preview
    ['title','author','publisher','year','description'].forEach(id => {
      const el = document.getElementById(id);
      if(!el) return;
      el.addEventListener('input', updatePreview);
    });

    function updatePreview(){
      const title = document.getElementById('title').value || 'Título do livro';
      const author = document.getElementById('author').value || '';
      const publisher = document.getElementById('publisher').value || '';
      const year = document.getElementById('year').value || '';
      previewTitle.textContent = title;
      const parts = [author, publisher, year].filter(Boolean).join(' • ');
      previewAuthor.textContent = parts || 'Autor • Editora • Ano';
      const desc = document.getElementById('description').value || 'Descrição curta do livro aparecerá aqui. Use a seção de descrição para resumir o conteúdo.';
      previewDesc.textContent = desc;
    }

    function handleFile(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (ev) => {
        previewImg.src = ev.target.result;
        previewImg.style.display = "block";
        previewPlaceholder.style.display = "none";
      };
      reader.readAsDataURL(file);
    }
    function resetPreview(){
      previewCover.style.background = '';
      previewCover.textContent = 'Capa';
      fileName.textContent = 'Nenhum arquivo selecionado';
      previewTitle.textContent = 'Título do livro';
      previewAuthor.textContent = 'Autor • Editora • Ano';
      previewDesc.textContent = 'Descrição curta do livro aparecerá aqui. Use a seção de descrição para resumir o conteúdo.';
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