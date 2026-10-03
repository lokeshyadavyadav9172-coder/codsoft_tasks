const questions = [
    {
        question: "You receive an email saying your bank account will be closed in 30 minutes unless you verify your details. What should you do?",
        answers: [
            "Click the link immediately",
            "Reply with your password",
            "Contact the bank through its official website or phone number",
            "Forward the email to friends"
        ],
        correct: 2
    },

    {
        question: "Which is a strong warning sign of a phishing email?",
        answers: [
            "A message you were expecting",
            "A suspicious sender address and urgent request",
            "A normal company newsletter",
            "An email from a known contact that you verified"
        ],
        correct: 1
    },

    {
        question: "What should you check before entering your password on a website?",
        answers: [
            "The website's domain name",
            "How many images are on the page",
            "The background color",
            "The number of buttons"
        ],
        correct: 0
    },

    {
        question: "An unexpected message asks you to share a one-time verification code. What should you do?",
        answers: [
            "Share it if the person sounds trustworthy",
            "Share only half of the code",
            "Never share it and verify the request independently",
            "Post it online to ask for help"
        ],
        correct: 2
    },

    {
        question: "Which technique involves pretending to be a trusted authority such as a manager, bank employee, or IT administrator?",
        answers: [
            "Authority impersonation",
            "Data compression",
            "Encryption",
            "Firewall filtering"
        ],
        correct: 0
    }
];


let currentQuestion = 0;
let score = 0;
let answered = false;


const questionNumber = document.getElementById("question-number");
const progress = document.getElementById("progress");
const questionElement = document.getElementById("question");
const answersElement = document.getElementById("answers");
const nextButton = document.getElementById("next-btn");

const quizContainer = document.getElementById("quiz-container");
const resultContainer = document.getElementById("result");
const scoreElement = document.getElementById("score");
const resultMessage = document.getElementById("result-message");


function loadQuestion() {

    answered = false;

    const current = questions[currentQuestion];

    questionNumber.textContent =
        `Question ${currentQuestion + 1} of ${questions.length}`;

    progress.style.width =
        `${((currentQuestion + 1) / questions.length) * 100}%`;

    questionElement.textContent = current.question;

    answersElement.innerHTML = "";

    nextButton.style.display = "none";


    current.answers.forEach((answer, index) => {

        const button = document.createElement("button");

        button.className = "answer-btn";
        button.textContent = answer;

        button.addEventListener("click", () => {
            selectAnswer(index, button);
        });

        answersElement.appendChild(button);
    });
}


function selectAnswer(selectedIndex, selectedButton) {

    if (answered) {
        return;
    }

    answered = true;

    const correctIndex = questions[currentQuestion].correct;

    const answerButtons =
        document.querySelectorAll(".answer-btn");


    answerButtons.forEach((button, index) => {

        button.disabled = true;

        if (index === correctIndex) {
            button.classList.add("correct");
        }

    });


    if (selectedIndex === correctIndex) {

        score++;

    } else {

        selectedButton.classList.add("wrong");

    }


    if (currentQuestion < questions.length - 1) {

        nextButton.textContent = "Next Question →";

    } else {

        nextButton.textContent = "View Results →";

    }

    nextButton.style.display = "inline-flex";
}


nextButton.addEventListener("click", () => {

    currentQuestion++;

    if (currentQuestion < questions.length) {

        loadQuestion();

    } else {

        showResults();

    }

});


function showResults() {

    quizContainer.classList.add("hidden");
    resultContainer.classList.remove("hidden");

    const percentage =
        Math.round((score / questions.length) * 100);

    scoreElement.textContent =
        `${score}/${questions.length} (${percentage}%)`;


    if (percentage === 100) {

        resultMessage.textContent =
            "Excellent! You have a strong understanding of phishing threats.";

    } else if (percentage >= 70) {

        resultMessage.textContent =
            "Great job! You know the major phishing warning signs. Stay alert.";

    } else if (percentage >= 50) {

        resultMessage.textContent =
            "Good start! Review the warning signs and try the quiz again.";

    } else {

        resultMessage.textContent =
            "Keep learning! Review the training sections before clicking suspicious links.";

    }
}


function restartQuiz() {

    currentQuestion = 0;
    score = 0;

    resultContainer.classList.add("hidden");
    quizContainer.classList.remove("hidden");

    loadQuestion();

    document
        .getElementById("quiz")
        .scrollIntoView({
            behavior: "smooth"
        });
}


loadQuestion();