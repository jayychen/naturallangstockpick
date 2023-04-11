const socket = io();
const questionInput = document.getElementById('questionInput');
const submitQuestion = document.getElementById('submitQuestion');
const exploreButton = document.getElementById('explore');
const responseTable = document.getElementById('responseTable');
const errorContainer = document.getElementById('errorContainer');
const infoContainer = document.getElementById('infoContainer');

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

exploreButton.addEventListener('click', () => {
  socket.emit('submitQuestion', { question: 'explore' });
});


socket.on('response', (response) => {
  infoContainer.innerHTML = '';
  errorContainer.innerHTML = '';
  responseTable.innerHTML = '';
  if (response.info) {
    infoContainer.innerHTML = `<div class="alert alert-secondary">` + response.info + `</div>`;
  }

  if (response.result === 'error') {
    errorContainer.innerHTML = `<div class="alert alert-danger">` + response.err_msg + `</div>`;
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
