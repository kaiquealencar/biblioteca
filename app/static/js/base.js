/**
 * Cria um preview genérico para qualquer formulário
 *
 * @param {string} formId - ID do formulário
 * @param {Object} fieldMap - Mapeamento dos campos do formulário para os elementos do preview
 *   Ex: { titulo: 'previewTitle', autor: 'previewAuthor', descricao: 'previewDesc' }
 * @param {Object} defaultValues - Valores padrão para o preview se o campo estiver vazio
 */
function setupPreview(formId, fieldMap, defaultValues = {}) {
  const form = document.getElementById(formId);
  if (!form) return;

  const previewElements = {};
  for (const key in fieldMap) {
    previewElements[key] = document.getElementById(fieldMap[key]);
    const input = document.getElementById(key);
    if (input) {
      input.addEventListener('input', updatePreview);
    }
  }

  function updatePreview() {
    for (const key in previewElements) {
      const input = document.getElementById(key);
      const value = input ? input.value : '';
      previewElements[key].textContent = value || (defaultValues[key] || '');
    }
  }

  function resetPreview() {
    for (const key in previewElements) {
      previewElements[key].textContent = defaultValues[key] || '';
    }
  }

  const fileInputs = form.querySelectorAll('input[type="file"]');
  fileInputs.forEach(fileInput => {
    const fileNameEl = document.getElementById('fileName');
    const previewImgEl = document.getElementById('previewImg');
    const placeholderEl = document.getElementById('previewPlaceholder');

    fileInput.addEventListener('change', (event) => {
      const file = event.target.files[0];
      if (!file) return;
      if(fileNameEl) fileNameEl.textContent = file.name;
      if(previewImgEl && placeholderEl){
        const reader = new FileReader();
        reader.onload = (ev) => {
          previewImgEl.src = ev.target.result;
          previewImgEl.style.display = "block";
          placeholderEl.style.display = "none";
        };
        reader.readAsDataURL(file);
      }
    });
  });

  return { updatePreview, resetPreview };
}
