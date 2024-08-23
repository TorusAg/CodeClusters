const socket = io.connect('http://localhost:5000');
let currentRoom = null;

function findSpecialists() {
    navigator.geolocation.getCurrentPosition(function(position) {
        fetch('/find_specialists', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location: {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                }
            })
        })
        .then(response => response.json())
        .then(data => {
            let specialistList = document.getElementById('specialist-list');
            specialistList.innerHTML = data.specialists.map(specialist => `
                <p>${specialist.name} - ${specialist.specialization}
                <button onclick="startChat(${specialist.id}, '${specialist.name}')">Chat</button></p>`).join('');
        });
    });
}

function startChat(doctorId, doctorName) {
    currentRoom = doctorId;
    socket.emit('join', { room: doctorId, username: 'Patient' });

    socket.on('message', function(msg) {
        const messageContainer = document.getElementById('messages');
        const messageElement = document.createElement('div');
        messageElement.textContent = msg;
        messageContainer.appendChild(messageElement);
    });
}

function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value;
    socket.emit('message', { room: currentRoom, msg: `Patient: ${message}` });
    input.value = '';
}

function startVideoCall() {
    const peer = new SimplePeer({ initiator: true, trickle: false });
    
    peer.on('signal', data => {
        socket.emit('signal', { room: currentRoom, signalData: data });
    });
    
    socket.on('signal', signal => {
        peer.signal(signal.signalData);
    });
    
    peer.on('stream', stream => {
        const video = document.getElementById('remoteVideo');
        video.srcObject = stream;
    });
}
