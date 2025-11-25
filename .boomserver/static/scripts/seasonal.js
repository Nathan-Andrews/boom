let holiday = "";

function getHoliday() {
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear()
    const currentMonth = currentDate.getMonth();
    const currentDay = currentDate.getDate();
    
    if (currentMonth === 11 && currentDay != 31) {
        holiday = "CHRISTMAS"
    }

    const firstDayOfNov = new Date(`11-1-${currentYear}`).getDay();
    const firstThursOfNov = (11 - firstDayOfNov) % 7 + 1;

    if (currentMonth === 10 && currentDay >= (firstThursOfNov + 11) && currentDay <= (firstThursOfNov + 21)) {
        holiday = "THANKSGIVING"
    }
}

getHoliday();
setInterval(getHoliday, 24 * 60 * 60 * 1000); // check holiday every 24 hrs


function randomEvent() {
    // 1/10 random event chance every 10 mins

    if (Math.floor(Math.random() * 10) % 10 === 0) {
        seasonalFlurry();
    }
}
setInterval(randomEvent,300000);

function seasonalFlurry() {
    if (holiday === "THANKSGIVING")
        startSeasonalSnowEffect("🍁",{sizeMin: 32,sizeMax: 64});
    
    if (holiday === "CHRISTMAS")
        startSeasonalSnowEffect("❄️");
}

// trigger a flurry seasonal effect
function ensureSnowStyles() {
    if (document.getElementById("snow-flurry-style")) return;

    const style = document.createElement("style");
    style.id = "snow-flurry-style";
    style.textContent = `
@keyframes snow-fall {
0% {
    transform: translate3d(var(--snow-x-start), -10vh, 0) rotate(0deg);
    opacity: 0;
}
10% {
    opacity: 1;
}
100% {
    transform: translate3d(calc(var(--snow-x-start) + var(--snow-x-drift)), 110vh, 0) rotate(720deg);
    opacity: 0;
}
}`;
    document.head.appendChild(style);
}

// startSnow({ sizeMin: 18, sizeMax: 40, duration: 3000, fallTime: 3500, spawnInterval: 60 })
window.startSeasonalSnowEffect = function startSeasonalSnowEffect(emoji,options = {}) {
    ensureSnowStyles();

    const duration = options.duration ?? 2500;       // ms to keep spawning flakes
    const fallTime = options.fallTime ?? 3000;       // ms each flake spends falling
    const spawnInterval = options.spawnInterval ?? 80;
    const sizeMin = options.sizeMin ?? 16;           // minimum font size (px)
    const sizeMax = options.sizeMax ?? 32;           // maximum font size (px)

    const container = document.createElement("div");
    container.style.position = "fixed";
    container.style.left = 0;
    container.style.top = 0;
    container.style.width = "100vw";
    container.style.height = "100vh";
    container.style.pointerEvents = "none";
    container.style.zIndex = 999999;
    container.style.overflow = "hidden";
    document.body.appendChild(container);

    const spawn = setInterval(() => {
        const flake = document.createElement("div");
        flake.textContent = emoji;
        flake.style.position = "absolute";

        const startX = Math.random() * 100;              // vw
        const drift = (Math.random() * 2 - 1) * 20;      // -20vw to 20vw

        flake.style.setProperty("--snow-x-start", startX + "vw");
        flake.style.setProperty("--snow-x-drift", drift + "vw");

        const size = sizeMin + Math.random() * (sizeMax - sizeMin);
        flake.style.fontSize = size + "px";
        flake.style.opacity = "0.9";
        flake.style.animation = `snow-fall ${fallTime}ms linear forwards`;

        container.appendChild(flake);

        setTimeout(() => flake.remove(), fallTime);
    }, spawnInterval);

    setTimeout(() => {
        clearInterval(spawn);
        setTimeout(() => container.remove(), fallTime);
    }, duration);
};

