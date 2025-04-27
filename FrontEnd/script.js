async function sendMessage() {
    const userInput = document.getElementById("userInput");
    const message = userInput.value.trim();
    if (message === "") return;

    addMessage(message, 'd-flex justify-content-end');
    userInput.value = "";

    const response = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: message })
    });

    const data = await response.json();
    addMessage(data.reply, 'd-flex justify-content-start');
}

function addMessage(text, alignmentClass) {
    const chatContainer = document.getElementById("chatContainer");
    const wrapperDiv = document.createElement("div");
    wrapperDiv.className = `${alignmentClass} mb-2`;

    const messageDiv = document.createElement("div");
    messageDiv.className = `p-2 rounded bg-primary bg-opacity-25 text-light`;
    messageDiv.style.maxWidth = '75%';
    messageDiv.textContent = text;

    wrapperDiv.appendChild(messageDiv);
    chatContainer.appendChild(wrapperDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.start();
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById("userInput").value = transcript;
    };
}