document.addEventListener('DOMContentLoaded', function () {
    loadChatHistory();
});

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const model = document.querySelector('input[name="model"]:checked').value;
    
    if (userInput.trim() === '') return;
    
    const chatHistory = document.getElementById('chat-history');
    const userMessage = document.createElement('div');
    userMessage.className = 'message user';
    userMessage.textContent = userInput;
    chatHistory.appendChild(userMessage);
    
    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user_input: userInput, model: model})
    })
    .then(response => response.json())
    .then(data => {
        const aiMessage = document.createElement('div');
        aiMessage.className = 'message ai';
        aiMessage.textContent = data.response;
        chatHistory.appendChild(aiMessage);
        saveChatHistory();
    });
    
    document.getElementById('user-input').value = '';
    saveChatHistory();
}

function saveChatHistory() {
    localStorage.setItem('chatHistory', document.getElementById('chat-history').innerHTML);
}

function loadChatHistory() {
    const chatHistory = localStorage.getItem('chatHistory');
    if (chatHistory) {
        document.getElementById('chat-history').innerHTML = chatHistory;
    }
}
