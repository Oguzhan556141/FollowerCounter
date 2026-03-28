let lastCelebratedMilestone = null;
let lastKnownCount = null;

// Initialize Socket.io
const socket = io();

socket.on('connect', () => {
    console.log('Connected to server via WebSocket');
    const soundStatus = document.getElementById('sound-status');
    if (soundStatus) {
        soundStatus.innerHTML = '● Çevrimiçi';
        soundStatus.style.color = '#00ff00';
    }
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    const soundStatus = document.getElementById('sound-status');
    if (soundStatus) {
        soundStatus.innerHTML = '○ Bağlantı Kesildi';
        soundStatus.style.color = '#ff0000';
    }
});

socket.on('follower_update', (data) => {
    console.log('Follower update received:', data);
    if (data.count !== undefined) {
        updateUI(data);
    }
});

function updateUI(data) {
    const counterElement = document.querySelector('#follower-counter .count');
    const updateElement = document.getElementById('last-update');
    const countdownElement = document.getElementById('update-countdown');

    // Animate counter
    animateValue(counterElement, parseInt(counterElement.innerText) || 0, data.count, 2000);
    
    // Update time
    const lastUpdatedTs = data.last_updated * 1000;
    const lastUpdate = new Date(lastUpdatedTs);
    updateElement.innerText = lastUpdate.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

    // Update Progress Bar
    updateProgressBar(data.count);

    // Single Follower Sound
    if (lastKnownCount !== null && data.count > lastKnownCount) {
        const milestone = Math.floor(data.count / 10) * 10;
        if (milestone <= (lastCelebratedMilestone || 0)) {
            playPop();
        }
    }
    lastKnownCount = data.count;

    // Milestone Celebration
    checkMilestones(data.count);

    // Reset countdown visual (since it's live now, we can just show "Canlı")
    if (countdownElement) {
        countdownElement.innerText = 'Canlı';
    }
}

function updateProgressBar(count) {
    const progressBar = document.getElementById('progress-bar');
    const progressPercent = document.getElementById('progress-percent');
    const target = 1000;
    
    const percentage = Math.min((count / target) * 100, 100).toFixed(1);
    
    if (progressBar) {
        progressBar.style.height = `${percentage}%`;
    }
    
    if (progressPercent) {
        const currentVal = parseFloat(progressPercent.innerText) || 0;
        animateValue(progressPercent, currentVal, parseFloat(percentage), 2000, true);
    }
}

function animateValue(obj, start, end, duration, isDecimal = false) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = progress * (end - start) + start;
        
        if (isDecimal) {
            obj.innerHTML = value.toFixed(1);
        } else {
            obj.innerHTML = Math.floor(value).toLocaleString();
        }
        
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Milestone Celebration
function checkMilestones(count) {
    const milestone = Math.floor(count / 10) * 10;
    
    // Initial load: just set the last milestone
    if (lastCelebratedMilestone === null) {
        lastCelebratedMilestone = milestone;
        return;
    }
    
    // If we crossed a new milestone
    if (milestone > lastCelebratedMilestone) {
        lastCelebratedMilestone = milestone;
        celebrate();
    }
}

// Sound status handling
const soundStatus = document.getElementById('sound-status');
let audioUnlocked = false;
let audioContext = null;

function unlockAudio() {
    if (audioUnlocked) return;
    
    try {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        
        if (audioContext.state === 'suspended') {
            audioContext.resume();
        }
        
        // Also try to unlock HTML5 Audio elements
        const horn = document.getElementById('celebration-sound');
        if (horn) { 
            horn.play().then(() => { horn.pause(); horn.currentTime = 0; })
                .catch(e => console.log('HTML5 Audio still locked:', e)); 
        }
        
        audioUnlocked = true;
        if (soundStatus) {
            soundStatus.innerText = '🔊 Sesler Hazır (Test Et)';
            soundStatus.style.color = '#00ff00';
        }
        console.log('Audio Context Unlocked. State:', audioContext.state);
        
        // Provide visual feedback for unlock
        pulseSoundStatus();
    } catch (e) {
        console.error('Audio Context failed:', e);
    }
}

function pulseSoundStatus() {
    if (!soundStatus) return;
    soundStatus.style.transform = 'scale(1.2)';
    setTimeout(() => {
        soundStatus.style.transform = 'scale(1)';
    }, 200);
}

function playPop() {
    if (!audioUnlocked || !audioContext) {
        console.log('Cannot play sound: Audio not unlocked.');
        return;
    }
    
    // 1. Try playing the HTML Clap MP3
    const chime = document.getElementById('follower-chime');
    if (chime) {
        chime.currentTime = 0;
        chime.play().catch(e => {
            console.log('Clap MP3 blocked, falling back to Web Audio');
            synthesizePop();
        });
    } else {
        synthesizePop();
    }
}

function synthesizePop() {
    if (!audioContext) return;
    if (audioContext.state === 'suspended') audioContext.resume();
    
    try {
        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();
        osc.type = 'sine';
        osc.connect(gain);
        gain.connect(audioContext.destination);
        const now = audioContext.currentTime;
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.1);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
        osc.start(now);
        osc.stop(now + 0.2);
        pulseSoundStatus();
    } catch (e) {
        console.error('Synthesized Pop failed:', e);
    }
}

// Unlock audio on FIRST interaction
['click', 'touchstart', 'keydown', 'mousedown'].forEach(evt => {
    document.addEventListener(evt, unlockAudio, { once: true });
});

if (soundStatus) {
    soundStatus.addEventListener('click', (e) => {
        e.stopPropagation();
        unlockAudio();
        console.log('Testing applause/clap...');
        playPop();
    });
}

function celebrate() {
    const sound = document.getElementById('celebration-sound');
    if (sound) {
        sound.currentTime = 0;
        sound.play().catch(e => {
            console.log('Celebration sound blocked');
            if (soundStatus) {
                soundStatus.innerText = '🔇 Sesleri Aktif Et (Tıkla)';
                soundStatus.style.color = '#ff0000';
            }
        });
    }

    const duration = 5 * 1000;
    const animationEnd = Date.now() + duration;
    const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

    function randomInRange(min, max) {
        return Math.random() * (max - min) + min;
    }

    const interval = setInterval(function() {
        const timeLeft = animationEnd - Date.now();

        if (timeLeft <= 0) {
            return clearInterval(interval);
        }

        const particleCount = 50 * (timeLeft / duration);
        confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } });
        confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } });
    }, 250);
}

// Add some interaction to the stars
document.addEventListener('mousemove', (e) => {
    const stars = document.querySelector('.stars');
    if (!stars) return;
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    stars.style.transform = `translate(${x * 10}px, ${y * 10}px)`;
});
