
function setTheme(themeName) {
    document.getElementById("theme-style").href = `static/styles/themes/${themeName}.css`;
}

let userSettingsJson = {};

function getUserSettings() {
    const storedSettings = localStorage.getItem("userSettings");

    if (storedSettings !== null) {
        userSettingsJson = JSON.parse(storedSettings);
    }
}

function setInitalTheme() {
    getUserSettings();
    
    if (userSettingsJson.theme !== null && userSettingsJson.theme !== undefined) {
        if (userSettingsJson.theme.type == "CUSTOM") {
            // apply custom theme
        }
        else if (userSettingsJson.theme.type == "SAVED") {
            setTheme(userSettingsJson.theme.id);
        }
    }
    else {
        setTheme("palenight");
    }
}

setInitalTheme();

function saveTheme(theme) {
    userSettingsJson.theme = theme;

    localStorage.setItem("userSettings",JSON.stringify(userSettingsJson));
}