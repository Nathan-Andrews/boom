function createChannelConnection() {
    const channel = new BroadcastChannel("customization_popup_channel");

    channel.addEventListener('message', (event) => {
        console.log('Received message:', event.data);
    });
}

function createChannelConnectionOnPopup() {
    const channel = new BroadcastChannel("customization_popup_channel");

    channel.addEventListener('message', (event) => {
        console.log('Received message:', event.data);
    });
}