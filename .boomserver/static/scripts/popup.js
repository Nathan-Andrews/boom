createChannelConnectionOnPopup();

buildDropdown();

async function buildDropdown() {
    fetch('/static/styles/themes/theme-metadata.json')
    .then(response => response.text())
    .then(data => {
      console.log(data)
    })
    .catch(error => console.error('Error loading text file:', error));

}