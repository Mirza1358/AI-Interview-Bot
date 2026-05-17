document.addEventListener('DOMContentLoaded', () => {
    const setupForm = document.getElementById('setup-form');
    const setupScreen = document.getElementById('setup-screen');
    const chatScreen = document.getElementById('chat-screen');
    const chatBox = document.getElementById('chat-box');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const inputArea = document.getElementById('input-area');

    setupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const submitBtn = setupForm.querySelector('button');
        
        submitBtn.textContent = 'Connecting to AI...';
        submitBtn.disabled = true;

        try {
            const response = await fetch('/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, phone })
            });
            
            const data = await response.json();
            
            if (data.status === 'error') {
                alert(data.reply);
                submitBtn.textContent = 'Start Interview';
                submitBtn.disabled = false;
                return;
            }
            
            // Switch screens
            setupScreen.classList.add('hidden');
            chatScreen.classList.remove('hidden');
            
            // Show initial AI message
            appendMessage('bot', data.reply);
            inputArea.classList.remove('hidden');
            chatInput.focus();
            
        } catch (error) {
            alert('Failed to start interview. Please check your connection.');
            submitBtn.textContent = 'Start Interview';
            submitBtn.disabled = false;
        }
    });

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        appendMessage('user', text);
        chatInput.value = '';
        chatInput.disabled = true;
        sendBtn.disabled = true;

        const typingIndicator = showTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            
            const data = await response.json();
            
            chatBox.removeChild(typingIndicator);
            
            if (data.error) {
                alert("Error: " + data.error + ". Please refresh the page to start a new session.");
                chatInput.disabled = false;
                sendBtn.disabled = false;
                return;
            }
            
            appendMessage('bot', data.reply);
            
            if (data.status === 'completed') {
                inputArea.classList.add('hidden');
                // The congratulations message is already appended by the server.
            } else {
                chatInput.disabled = false;
                sendBtn.disabled = false;
                chatInput.focus();
            }
            
        } catch (error) {
            chatBox.removeChild(typingIndicator);
            appendMessage('bot', "Network error. Please try sending again.");
            chatInput.disabled = false;
            sendBtn.disabled = false;
        }
    }

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender === 'user' ? 'user-msg' : 'bot-msg');
        msgDiv.textContent = text;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('typing-indicator');
        typingDiv.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        chatBox.appendChild(typingDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        return typingDiv;
    }
});
