const startButton = document.getElementById('start-button');
const nextButton = document.getElementById('next-button');
const restartButton = document.getElementById('restart-button');
const reviewButton = document.getElementById('review-button');
const reviewPrevButton = document.getElementById('review-prev');
const reviewNextButton = document.getElementById('review-next');
const reviewExitButton = document.getElementById('review-exit');
const startScreen = document.getElementById('start-screen');
const quizScreen = document.getElementById('quiz-screen');
const resultScreen = document.getElementById('result-screen');
const reviewScreen = document.getElementById('review-screen');
const questionContainerElement = document.getElementById('question-container');
const questionElement = document.getElementById('question');
const answerButtonsElement = document.getElementById('answer-buttons');
const scoreElement = document.getElementById('score');
const reviewQuestionElement = document.getElementById('review-question');
const reviewAnswersElement = document.getElementById('review-answers');
const reviewCounterElement = document.getElementById('review-counter');

let allQuestions = [];
let selectedQuestions = []; // Nuovo array per le domande selezionate
let currentQuestionIndex;
let score = 0;
let userAnswers = []; // Array per tracciare le risposte dell'utente
let reviewIndex = 0; // Indice per la modalità revisione

// Funzione per selezionare casualemente 10 domande dal pool completo
function selectRandomQuestions(questions, count = 10) {
    const shuffled = [...questions].sort(() => Math.random() - 0.5);
    return shuffled.slice(0, count);
}

// Carica le domande dal file JSON
fetch('questions.json')
    .then(res => res.json())
    .then(data => {
        allQuestions = data;
        startButton.disabled = false; // Abilita il pulsante solo dopo aver caricato le domande
        startButton.innerText = 'Inizia';
    })
    .catch(err => {
        console.error("Errore nel caricamento delle domande:", err);
        questionElement.innerText = "Impossibile caricare le domande. Controlla il file questions.json e ricarica la pagina.";
    });


startButton.addEventListener('click', startGame);
nextButton.addEventListener('click', () => {
    currentQuestionIndex++;
    setNextQuestion();
});
restartButton.addEventListener('click', startGame);
reviewButton.addEventListener('click', startReview);
reviewPrevButton.addEventListener('click', () => {
    if (reviewIndex > 0) {
        reviewIndex--;
        showReviewQuestion();
    }
});
reviewNextButton.addEventListener('click', () => {
    if (reviewIndex < userAnswers.length - 1) {
        reviewIndex++;
        showReviewQuestion();
    }
});
reviewExitButton.addEventListener('click', () => {
    reviewScreen.classList.add('hidden');
    resultScreen.classList.remove('hidden');
});

function startGame() {
    score = 0;
    userAnswers = []; // Reset delle risposte utente
    startScreen.classList.add('hidden');
    resultScreen.classList.add('hidden');
    reviewScreen.classList.add('hidden');
    quizScreen.classList.remove('hidden');
    
    // Seleziona 10 domande casuali ogni volta che inizia una nuova partita
    selectedQuestions = selectRandomQuestions(allQuestions, 10);
    currentQuestionIndex = 0;
    setNextQuestion();
}

function setNextQuestion() {
    resetState();
    if (selectedQuestions.length > currentQuestionIndex) {
        showQuestion(selectedQuestions[currentQuestionIndex]);
    } else {
        showResult();
    }
}

function showQuestion(question) {
    questionElement.innerText = question.question;
    question.answers.forEach(answer => {
        const button = document.createElement('button');
        button.innerText = answer.text;
        button.classList.add('btn');
        if (answer.correct) {
            button.dataset.correct = answer.correct;
        }
        button.addEventListener('click', selectAnswer);
        answerButtonsElement.appendChild(button);
    });
}

function resetState() {
    clearStatusClass(document.body);
    nextButton.classList.add('hidden');
    while (answerButtonsElement.firstChild) {
        answerButtonsElement.removeChild(answerButtonsElement.firstChild);
    }
}

function selectAnswer(e) {
    const selectedButton = e.target;
    const correct = selectedButton.dataset.correct === 'true';
    
    // Salva la risposta dell'utente con tutti i dettagli della domanda
    userAnswers.push({
        question: selectedQuestions[currentQuestionIndex].question,
        answers: selectedQuestions[currentQuestionIndex].answers,
        userAnswer: selectedButton.innerText,
        userAnswerIndex: Array.from(answerButtonsElement.children).indexOf(selectedButton),
        correctAnswer: selectedQuestions[currentQuestionIndex].answers.find(ans => ans.correct).text,
        isCorrect: correct
    });
    
    if (correct) {
        score++;
    }
    setStatusClass(selectedButton, correct);
    Array.from(answerButtonsElement.children).forEach(button => {
        setStatusClass(button, button.dataset.correct === 'true');
        button.disabled = true;
    });
    nextButton.classList.remove('hidden');
}

function setStatusClass(element, correct) {
    clearStatusClass(element);
    if (correct) {
        element.classList.add('correct');
    } else {
        element.classList.add('wrong');
    }
}

function clearStatusClass(element) {
    element.classList.remove('correct');
    element.classList.remove('wrong');
}

function showResult() {
    quizScreen.classList.add('hidden');
    resultScreen.classList.remove('hidden');
    scoreElement.innerText = score + ' su 10'; // Ora sempre su 10 domande
    
    // Crea il riepilogo delle risposte
    const summaryContainer = document.getElementById('answers-summary');
    summaryContainer.innerHTML = '';
    
    userAnswers.forEach((answer, index) => {
        const summaryItem = document.createElement('div');
        summaryItem.className = 'summary-item';
        
        const questionText = document.createElement('div');
        questionText.className = 'summary-question';
        questionText.innerText = answer.question.replace(/\n/g, ' ');
        
        const userAnswerDiv = document.createElement('div');
        userAnswerDiv.className = `summary-answer user-answer ${answer.isCorrect ? 'correct' : 'wrong'}`;
        userAnswerDiv.innerHTML = `<strong>La tua risposta:</strong> ${answer.userAnswer}`;
        
        summaryItem.appendChild(questionText);
        summaryItem.appendChild(userAnswerDiv);
        
        // Se la risposta era sbagliata, mostra anche quella corretta
        if (!answer.isCorrect) {
            const correctAnswerDiv = document.createElement('div');
            correctAnswerDiv.className = 'summary-answer correct-answer';
            correctAnswerDiv.innerHTML = `<strong>Risposta corretta:</strong> ${answer.correctAnswer}`;
            summaryItem.appendChild(correctAnswerDiv);
        }
        
        summaryContainer.appendChild(summaryItem);
    });
}

function startReview() {
    reviewIndex = 0;
    resultScreen.classList.add('hidden');
    reviewScreen.classList.remove('hidden');
    showReviewQuestion();
}

function showReviewQuestion() {
    const currentAnswer = userAnswers[reviewIndex];
    
    // Aggiorna il contatore
    reviewCounterElement.innerText = `${reviewIndex + 1} di ${userAnswers.length}`;
    
    // Mostra la domanda
    reviewQuestionElement.innerText = currentAnswer.question;
    
    // Pulisce le risposte precedenti
    reviewAnswersElement.innerHTML = '';
    
    // Crea i pulsanti delle risposte
    currentAnswer.answers.forEach((answer, index) => {
        const button = document.createElement('button');
        button.innerText = answer.text;
        button.classList.add('btn');
        button.disabled = true; // Non cliccabili in modalità revisione
        
        // Evidenzia la risposta dell'utente e quella corretta
        if (index === currentAnswer.userAnswerIndex) {
            // Risposta selezionata dall'utente
            if (currentAnswer.isCorrect) {
                button.classList.add('correct');
            } else {
                button.classList.add('wrong');
            }
        } else if (answer.correct) {
            // Risposta corretta (se diversa da quella dell'utente)
            button.classList.add('correct');
        }
        
        reviewAnswersElement.appendChild(button);
    });
    
    // Gestisce i pulsanti di navigazione
    reviewPrevButton.disabled = (reviewIndex === 0);
    reviewNextButton.disabled = (reviewIndex === userAnswers.length - 1);
}
