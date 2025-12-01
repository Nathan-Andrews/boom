document.addEventListener('keydown', function(event) {
    if (event.key === ' ' && fullyLoaded) {
        incrementStateContentRender();
    }

    if (event.key === 'Escape') {
        hideAlert();
    }

    if (event.key === 'l' && fullyLoaded) {
        if (holiday === "THANKSGIVING")
            startSeasonalSnowEffect("🍁",{sizeMin: 32, sizeMax: 64});
        
        if (holiday === "CHRISTMAS")
            startSeasonalSnowEffect("❄️");
    }

    if (event.key === "p"  && fullyLoaded) {
        window.open("popup.html", "_blank", "width=600,height=400");
    }
});

// alert system for showing errors, and in the future maybe other messages like announcements
function showAlert(headerContent, bodyContent) {
    const alertElement = document.getElementById('alertContainer');
    const alertHeaderElement = document.getElementById('alertHeader');
    const alertBodyElement = document.getElementById('alertBody');

    alertHeaderElement.textContent = headerContent;
    alertBodyElement.textContent = bodyContent;
    alertElement.style.display = 'flex';
}

function hideAlert() {
    const alertElement = document.getElementById('alertContainer');

    alertElement.style.display = 'none';
}

