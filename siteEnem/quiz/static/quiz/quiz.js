document.getElementById('form-pergunta').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    fetch('/responder/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        const resultado = document.getElementById('resultado');
        if (data.correta) {
            resultado.innerHTML = `<p>Parabéns! Resposta correta.</p><p>${data.explicacao}</p>`;
        } else {
            resultado.innerHTML = `<p>Resposta errada. ${data.explicacao}</p>`;
        }
    });
});
