const msgInput = document.getElementById('msgInput');
const sendBtn = document.getElementById('sendBtn');
const messagesBox = document.getElementById('messagesBox');

// الاتصال بالسيرفر
const ws = new WebSocket(`ws://${window.location.host}/ws`);

ws.onmessage = function(event) {
    addMessage(event.data, 'incoming'); // رسالة من شخص آخر (أصفر)
};

function sendMessage() {
    const text = msgInput.value;
    if (text.trim() === "") return;

    ws.send(text); // إرسال للسيرفر
    addMessage(text, 'outgoing'); // إظهار عندي (أحمر)
    msgInput.value = "";
}

function addMessage(text, type) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', type);

    const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    msgDiv.innerHTML = `<p>${text}</p><span class="time">${time}</span>`;

    messagesBox.appendChild(msgDiv);
    messagesBox.scrollTop = messagesBox.scrollHeight;
}

sendBtn.addEventListener('click', sendMessage);
msgInput.addEventListener('keypress', (e) => { if(e.key === 'Enter') sendMessage(); });