const uploadForm = document.getElementById('upload-form');
const pdfFileInput = document.getElementById('pdf-file');
const uploadBtn = document.getElementById('upload-btn');
const questionInput = document.getElementById('question-input');
const askBtn = document.getElementById('ask-btn');
const answerContainer = document.getElementById('answer-container');

uploadBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const pdfFile = pdfFileInput.files[0];
    if (!pdfFile) {
        alert('Please select a PDF file to upload.');
        return;
    }
    const formData = new FormData();
    formData.append('pdf_file', pdfFile);
    fetch('http://127.0.0.1:5002/upload', {  
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        console.log(data);
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            alert('PDF uploaded successfully.');
        }
    })
    .catch((error) => {
        console.error(error);
        alert('An error occurred while uploading the PDF. Please try again.');
    });
});

askBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const question = questionInput.value.trim();
    if (!question) {
        alert('Please enter a question.');
        return;
    }
    fetch('http://127.0.0.1:5002/ask', {  
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        const answer = data.answer;
        answerContainer.innerHTML = <p>${answer}</p>;
    })
    .catch((error) => {
        console.error(error);
        alert('An error occurred while asking the question. Please try again.');
    });
});

