const socket = io();
const questionInput = document.getElementById('questionInput');
const submitQuestion = document.getElementById('submitQuestion');
const exploreButton = document.getElementById('explore');
const responseTable = document.getElementById('responseTable');
const errorContainer = document.getElementById('errorContainer');
const infoContainer = document.getElementById('infoContainer');
const disclaimer = document.getElementById('disclaimer');

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
    //table header 
    const tableHeader = document.createElement('thead');
    const headerRow = document.createElement('tr');
    headerRow.innerHTML = `
    <th> </th>
    <th>Ticker</th>
    `;
    tableHeader.appendChild(headerRow);
    responseTable.appendChild(tableHeader);
    //
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

disclaimer.addEventListener('click', () => {
  infoContainer.innerHTML = `<div class="alert alert-secondary"><b>Natural Language Stock Picker</b><br><br> This is a pet project where you can pick stocks using natural language description. Keep clicking on "Explore" to see some examples. <br><br> <small>DISCLAIMER: The information provided on this website is for educational and informational purposes only and should not be considered as investment advice. The website does not make any representation or warranty as to the accuracy, completeness, or timeliness of the information on this site. Any reliance you place on such information is therefore strictly at your own risk. The website shall not be liable for any investment loss, including without limitation, indirect or consequential loss or damage, or any loss or damage whatsoever arising from the use of this website.</small></div>`;
});
