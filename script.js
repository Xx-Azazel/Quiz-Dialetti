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

// Funzioni per la gestione del localStorage
const QuizState = {
    save: function() {
        try {
            const state = {
                selectedQuestions,
                currentQuestionIndex,
                score,
                userAnswers,
                timestamp: Date.now()
            };
            localStorage.setItem('quiz-dialetti-state', JSON.stringify(state));
        } catch (e) {
            console.warn('Impossibile salvare lo stato del quiz:', e);
        }
    },
    
    load: function() {
        try {
            const saved = localStorage.getItem('quiz-dialetti-state');
            if (saved) {
                const state = JSON.parse(saved);
                // Controlla se lo stato è recente (max 1 ora)
                if (Date.now() - state.timestamp < 3600000) {
                    return state;
                }
            }
        } catch (e) {
            console.warn('Impossibile caricare lo stato del quiz:', e);
        }
        return null;
    },
    
    clear: function() {
        try {
            localStorage.removeItem('quiz-dialetti-state');
        } catch (e) {
            console.warn('Impossibile cancellare lo stato del quiz:', e);
        }
    }
};

// Funzione per mostrare notifiche
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" aria-label="Chiudi notifica">×</button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-rimozione dopo 5 secondi
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Funzione per selezionare casualemente 10 domande dal pool completo
function selectRandomQuestions(questions, count = 10) {
    const shuffled = [...questions].sort(() => Math.random() - 0.5);
    return shuffled.slice(0, count);
}

// Funzione per caricare le domande con retry mechanism
async function loadQuestions(retries = 3) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch('questions.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            // Validazione dei dati JSON
            if (!Array.isArray(data) || data.length === 0) {
                throw new Error('Dati del quiz non validi');
            }
            
            // Validazione struttura domande
            const validQuestions = data.filter(q => 
                q.question && 
                Array.isArray(q.answers) && 
                q.answers.length >= 2 &&
                q.answers.some(a => a.correct === true)
            );
            
            if (validQuestions.length < 10) {
                throw new Error('Numero insufficiente di domande valide');
            }
            
            allQuestions = validQuestions;
            startButton.disabled = false;
            startButton.innerText = 'Inizia';
            return;
            
        } catch (err) {
            console.error(`Tentativo ${i + 1} fallito:`, err);
            if (i === retries - 1) {
                // Ultimo tentativo fallito - mostra errore con opzione retry
                startButton.innerText = 'Riprova';
                startButton.disabled = false;
                startButton.onclick = () => {
                    startButton.disabled = true;
                    startButton.innerText = 'Caricamento...';
                    loadQuestions();
                };
                
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-message';
                errorDiv.innerHTML = `
                    <h3>⚠️ Errore di Caricamento</h3>
                    <p>Impossibile caricare le domande del quiz.</p>
                    <p><strong>Dettagli:</strong> ${err.message}</p>
                    <button onclick="location.reload()" class="btn error-retry-btn">🔄 Ricarica Pagina</button>
                `;
                
                const container = document.getElementById('start-screen');
                container.appendChild(errorDiv);
                return;
            }
            // Attendi prima del prossimo tentativo
            await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
        }
    }
}

// Carica le domande al caricamento della pagina
loadQuestions();

// Gestione della navigazione da tastiera
document.addEventListener('keydown', function(e) {
    // Durante il quiz
    if (!quizScreen.classList.contains('hidden')) {
        const buttons = Array.from(answerButtonsElement.children);
        const activeElement = document.activeElement;
        const currentIndex = buttons.indexOf(activeElement);
        
        switch(e.key) {
            case 'ArrowDown':
            case 'ArrowRight':
                e.preventDefault();
                if (currentIndex < buttons.length - 1) {
                    buttons[currentIndex + 1].focus();
                } else {
                    buttons[0].focus();
                }
                break;
            case 'ArrowUp':
            case 'ArrowLeft':
                e.preventDefault();
                if (currentIndex > 0) {
                    buttons[currentIndex - 1].focus();
                } else {
                    buttons[buttons.length - 1].focus();
                }
                break;
            case 'Enter':
            case ' ':
                e.preventDefault();
                if (buttons.includes(activeElement) && !activeElement.disabled) {
                    activeElement.click();
                }
                break;
            case 'Escape':
                if (confirm('Vuoi davvero uscire dal quiz? Il progresso andrà perso.')) {
                    startGame(); // Ricomincia
                }
                break;
        }
    }
    
    // Durante la revisione
    if (!reviewScreen.classList.contains('hidden')) {
        switch(e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                if (!reviewPrevButton.disabled) {
                    reviewPrevButton.click();
                }
                break;
            case 'ArrowRight':
                e.preventDefault();
                if (!reviewNextButton.disabled) {
                    reviewNextButton.click();
                }
                break;
            case 'Escape':
                reviewExitButton.click();
                break;
        }
    }
});

startButton.addEventListener('click', startGame);
nextButton.addEventListener('click', () => {
    currentQuestionIndex++;
    setNextQuestion();
});
restartButton.addEventListener('click', () => {
    if (confirm('Sei sicuro di voler ricominciare? Il progresso attuale andrà perso.')) {
        QuizState.clear();
        startGame();
    }
});
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
    // Focus sul pulsante restart quando si torna ai risultati
    setTimeout(() => restartButton.focus(), 100);
});

// Gestione dell'uscita dalla pagina durante il quiz
window.addEventListener('beforeunload', function(e) {
    // Avvisa solo se il quiz è in corso
    if (!quizScreen.classList.contains('hidden') && currentQuestionIndex > 0) {
        e.preventDefault();
        e.returnValue = 'Hai un quiz in corso. Sei sicuro di voler uscire?';
        return e.returnValue;
    }
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
    QuizState.clear(); // Pulisce stato precedente
    setNextQuestion();
    
    // Focus sul primo pulsante disponibile
    setTimeout(() => {
        const firstButton = answerButtonsElement.querySelector('.btn');
        if (firstButton) firstButton.focus();
    }, 100);
    
    showNotification('Quiz avviato! Usa le frecce per navigare tra le risposte.', 'success');
}

function setNextQuestion() {
    resetState();
    if (selectedQuestions.length > currentQuestionIndex) {
        showQuestion(selectedQuestions[currentQuestionIndex]);
    } else {
        showResult();
    }
}

// Funzione per sanitizzare il testo e prevenire XSS
function sanitizeText(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showQuestion(question) {
    questionElement.textContent = question.question; // Usa textContent per sicurezza
    question.answers.forEach(answer => {
        const button = document.createElement('button');
        const span = document.createElement('span');
        span.textContent = sanitizeText(answer.text); // Sanitizza il testo
        button.appendChild(span);
        button.classList.add('btn');
        button.setAttribute('role', 'button');
        button.setAttribute('aria-label', `Risposta: ${answer.text}`);
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
    
    // Pulisce gli effetti LED e tutti i pulsanti precedenti
    while (answerButtonsElement.firstChild) {
        const button = answerButtonsElement.firstChild;
        if (button && button.classList) {
            button.classList.remove('selected-answer', 'correct', 'wrong');
        }
        answerButtonsElement.removeChild(button);
    }
}

function selectAnswer(e) {
    const selectedButton = e.target.closest('button'); // Usa closest per gestire il click su span
    const correct = selectedButton.dataset.correct === 'true';
    
    // Aggiungi effetto LED alla risposta selezionata
    selectedButton.classList.add('selected-answer');
    
    // Salva la risposta dell'utente con tutti i dettagli della domanda
    userAnswers.push({
        question: selectedQuestions[currentQuestionIndex].question,
        answers: selectedQuestions[currentQuestionIndex].answers,
        userAnswer: selectedButton.querySelector('span').textContent, // Prendi il testo dallo span
        userAnswerIndex: Array.from(answerButtonsElement.children).indexOf(selectedButton),
        correctAnswer: selectedQuestions[currentQuestionIndex].answers.find(ans => ans.correct).text,
        isCorrect: correct
    });
    
    if (correct) {
        score++;
        showNotification('Risposta corretta! 🎉', 'success');
    } else {
        showNotification('Risposta sbagliata 😔', 'error');
    }
    
    setStatusClass(selectedButton, correct);
    Array.from(answerButtonsElement.children).forEach(button => {
        setStatusClass(button, button.dataset.correct === 'true');
        button.disabled = true;
    });
    
    // Salva lo stato dopo ogni risposta
    QuizState.save();
    
    nextButton.classList.remove('hidden');
    nextButton.focus(); // Focus sul pulsante "Prossima"
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
    scoreElement.textContent = score + ' su 10'; // Ora sempre su 10 domande
    
    // Annuncio del risultato per screen reader
    const announcement = score >= 7 ? 
        `Complimenti! Hai ottenuto ${score} punti su 10. Ottimo risultato!` :
        score >= 5 ?
        `Hai ottenuto ${score} punti su 10. Buon risultato!` :
        `Hai ottenuto ${score} punti su 10. Puoi migliorare!`;
    
    showNotification(announcement, score >= 7 ? 'success' : score >= 5 ? 'info' : 'error');
    
    // Pulisce lo stato salvato
    QuizState.clear();
    
    // Crea il riepilogo delle risposte
    const summaryContainer = document.getElementById('answers-summary');
    summaryContainer.innerHTML = '';
    
    userAnswers.forEach((answer, index) => {
        const summaryItem = document.createElement('div');
        summaryItem.className = 'summary-item';
        
        const questionText = document.createElement('div');
        questionText.className = 'summary-question';
        questionText.textContent = answer.question.replace(/\n/g, ' ');
        
        const userAnswerDiv = document.createElement('div');
        userAnswerDiv.className = `summary-answer user-answer ${answer.isCorrect ? 'correct' : 'wrong'}`;
        userAnswerDiv.innerHTML = `<strong>La tua risposta:</strong> ${sanitizeText(answer.userAnswer)}`;
        
        summaryItem.appendChild(questionText);
        summaryItem.appendChild(userAnswerDiv);
        
        // Se la risposta era sbagliata, mostra anche quella corretta
        if (!answer.isCorrect) {
            const correctAnswerDiv = document.createElement('div');
            correctAnswerDiv.className = 'summary-answer correct-answer';
            correctAnswerDiv.innerHTML = `<strong>Risposta corretta:</strong> ${sanitizeText(answer.correctAnswer)}`;
            summaryItem.appendChild(correctAnswerDiv);
        }
        
        summaryContainer.appendChild(summaryItem);
    });
    
    // Focus sul pulsante restart per accessibilità
    setTimeout(() => restartButton.focus(), 100);
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
    reviewCounterElement.textContent = `${reviewIndex + 1} di ${userAnswers.length}`;
    
    // Mostra la domanda
    reviewQuestionElement.textContent = currentAnswer.question;
    
    // Pulisce le risposte precedenti
    reviewAnswersElement.innerHTML = '';
    
    // Crea i pulsanti delle risposte
    currentAnswer.answers.forEach((answer, index) => {
        const button = document.createElement('button');
        const span = document.createElement('span');
        span.textContent = sanitizeText(answer.text); // Sanitizza il testo
        button.appendChild(span);
        button.classList.add('btn');
        button.disabled = true; // Non cliccabili in modalità revisione
        button.setAttribute('role', 'button');
        button.setAttribute('aria-label', `Risposta ${index + 1}: ${answer.text}`);
        
        // Evidenzia la risposta dell'utente e quella corretta
        if (index === currentAnswer.userAnswerIndex) {
            // Risposta selezionata dall'utente
            button.classList.add('user-selected');
            button.setAttribute('aria-label', `La tua risposta: ${answer.text}`);
            if (currentAnswer.isCorrect) {
                button.classList.add('correct');
                button.setAttribute('aria-label', `La tua risposta corretta: ${answer.text}`);
            } else {
                button.classList.add('wrong');
                button.setAttribute('aria-label', `La tua risposta sbagliata: ${answer.text}`);
            }
        } else if (answer.correct) {
            // Risposta corretta (se diversa da quella dell'utente)
            button.classList.add('correct');
            button.setAttribute('aria-label', `Risposta corretta: ${answer.text}`);
        }
        
        reviewAnswersElement.appendChild(button);
    });
    
    // Gestisce i pulsanti di navigazione
    reviewPrevButton.disabled = (reviewIndex === 0);
    reviewNextButton.disabled = (reviewIndex === userAnswers.length - 1);
}
