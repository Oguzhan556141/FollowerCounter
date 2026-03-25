async function fetchFollowers() {
    const counterElement = document.querySelector('#follower-counter .count');
    const updateElement = document.getElementById('last-update');

    try {
        const response = await fetch('/api/followers');
        const data = await response.json();

        if (data.count !== undefined) {
            animateValue(counterElement, parseInt(counterElement.innerText), data.count, 2000);
            
            const lastUpdatedTs = data.last_updated * 1000;
            const lastUpdate = new Date(lastUpdatedTs);
            updateElement.innerText = lastUpdate.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        }
    } catch (error) {
        console.error('Error fetching followers:', error);
    }
}

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start).toLocaleString();
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Initial fetch
fetchFollowers();

let countdown = 30;
const countdownElement = document.getElementById('update-countdown');

setInterval(() => {
    countdown--;
    if (countdown <= 0) {
        countdown = 30;
        fetchFollowers();
    }
    if (countdownElement) {
        countdownElement.innerText = countdown;
    }
}, 1000);

// Add some interaction to the stars
document.addEventListener('mousemove', (e) => {
    const stars = document.querySelector('.stars');
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    stars.style.transform = `translate(${x * 10}px, ${y * 10}px)`;
});
