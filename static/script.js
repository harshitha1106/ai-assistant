const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');

userInput.addEventListener('keypress', function(e) {
  if (e.key === 'Enter') sendMessage();
});

function addMessage(text, isUser) {
  const welcome = chatBox.querySelector('.welcome');
  if (welcome) welcome.remove();

  const div = document.createElement('div');
  div.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function showTyping() {
  const div = document.createElement('div');
  div.className = 'typing';
  div.id = 'typing';
  div.innerHTML = '<span></span><span></span><span></span>';
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
  const typing = document.getElementById('typing');
  if (typing) typing.remove();
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, true);
  userInput.value = '';
  showTyping();

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    removeTyping();
    addMessage(data.response, false);
  } catch (error) {
    removeTyping();
    addMessage('Something went wrong. Please try again.', false);
  }
}