let timer;
let timeRemaining;
let initialTime;
let isRunning = false;
const timerDisplay = document.getElementById('timer');
const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const stopBtn = document.getElementById('stopBtn');
const resetBtn = document.getElementById('resetBtn');
const tenMinBtn = document.getElementById('tenMinBtn');
const fifteenMinBtn = document.getElementById('fifteenMinBtn');
const buzzerInfo = document.getElementById('buzzerInfo');

const feetWeaponsGoSound = new Audio('feet_weapons_go.mp3');
const buzzerSound = new Audio('buzzer_sound.mp3');
const stopSound = new Audio('stop_sound.mp3');

function updateTimerDisplay(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function startTimer() {
    if (!isRunning) {
        feetWeaponsGoSound.play().then(() => {
            isRunning = true;
            timer = setInterval(() => {
                timeRemaining--;
                updateTimerDisplay(timeRemaining);
                if (timeRemaining <= 0) {
                    clearInterval(timer);
                    isRunning = false;
                    buzzerSound.play();
                }
            }, 1000);
        });
    }
}

function pauseTimer() {
    clearInterval(timer);
    isRunning = false;
}

function stopTimer() {
    clearInterval(timer);
    isRunning = false;
    stopSound.play();
    buzzerInfo.textContent = 'Timer Stopped';
}

function resetTimer() {
    clearInterval(timer);
    isRunning = false;
    timeRemaining = initialTime;
    updateTimerDisplay(timeRemaining);
    buzzerInfo.textContent = 'Buzzer: None';
}

function setTime(duration) {
    initialTime = duration;
    resetTimer();
}

startBtn.addEventListener('click', startTimer);
pauseBtn.addEventListener('click', pauseTimer);
stopBtn.addEventListener('click', stopTimer);
resetBtn.addEventListener('click', resetTimer);
tenMinBtn.addEventListener('click', () => setTime(600));
fifteenMinBtn.addEventListener('click', () => setTime(900));

// Simulating buzzer input (replace this with actual buzzer input logic)
document.addEventListener('keydown', (event) => {
    if (event.key === '1' || event.key === '2') {
        pauseTimer();
        buzzerSound.play();
        buzzerInfo.textContent = `Buzzer: Team ${event.key}`;
    }
});

// Initialize with 10 minutes
setTime(600);