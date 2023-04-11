const socket = io();
const questionInput = document.getElementById('questionInput');
const submitQuestion = document.getElementById('submitQuestion');
const responseTable = document.getElementById('responseTable');
const errorContainer = document.getElementById('errorContainer');

submitQuestion.addEventListener('click', () => {
  const question = questionInput.value;
  if (question.trim() !== '') {
    socket.emit('submitQuestion', { question });
    questionInput.value = '';
  }
});

questionInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    event.preventDefault();
    submitQuestion.click();
  }
});


socket.on('response', (response) => {
  errorContainer.innerHTML = '';
  responseTable.innerHTML = '';

  if (response.error) {
    errorContainer.innerHTML = `<div class="alert alert-danger">${JSON.stringify(response)}</div>`;
  } else {
    const tableBody = document.createElement('tbody');
    response.symbols.forEach((item, index) => {
      const tableRow = document.createElement('tr');
      tableRow.innerHTML = `
        <th scope="row">${index + 1}</th>
        <td>${item}</td>
      `;
      tableBody.appendChild(tableRow);
    });
    responseTable.appendChild(tableBody);
  }
});
