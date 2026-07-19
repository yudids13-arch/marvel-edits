// JARVIS Web Interface Script

const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const commandsModal = document.getElementById('commandsModal');

// Send message on button click
sendBtn.addEventListener('click', sendMessage);

// Send message on Enter key
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addMessage(message, 'user');
    userInput.value = '';

    // Send to backend
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        addMessage(data.response, 'jarvis');
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('Error communicating with JARVIS', 'jarvis');
    });
}

function sendCommand(cmd) {
    userInput.value = cmd;
    sendMessage();
}

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const p = document.createElement('p');
    p.textContent = content;
    
    messageDiv.appendChild(p);
    chatBox.appendChild(messageDiv);
    
    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

function loadCommands() {
    fetch('/api/commands')
    .then(response => response.json())
    .then(data => {
        let html = '';
        for (const [category, commands] of Object.entries(data)) {
            html += `<div class="command-group">`;
            html += `<h3>${category.replace(/_/g, ' ').toUpperCase()}</h3>`;
            commands.forEach(cmd => {
                html += `
                    <div class="command-item">
                        <div class="cmd">${cmd.cmd}</div>
                        <div class="desc">${cmd.desc}</div>
                    </div>
                `;
            });
            html += `</div>`;
        }
        document.getElementById('commandsList').innerHTML = html;
        commandsModal.style.display = 'block';
    });
}

function closeModal() {
    commandsModal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target === commandsModal) {
        commandsModal.style.display = 'none';
    }
}

// Load system info
function loadSystemInfo() {
    fetch('/api/system/info')
    .then(response => response.json())
    .then(data => {
        let html = `
            <p><strong>Name:</strong> ${data.name}</p>
            <p><strong>Version:</strong> ${data.version}</p>
            <p><strong>Status:</strong> <span style="color: var(--success-color);">${data.status}</span></p>
            <p><strong>Mode:</strong> ${data.mode}</p>
        `;
        document.getElementById('systemInfo').innerHTML = html;
    });
}

// Load knowledge base info
function loadKnowledgeInfo() {
    fetch('/api/knowledge')
    .then(response => response.json())
    .then(data => {
        let html = `
            <p><strong>Items:</strong> ${data.total_items}</p>
            <p><strong>Categories:</strong> ${data.categories.length}</p>
        `;
        if (data.categories.length > 0) {
            html += `<p><strong>Tags:</strong> ${data.categories.slice(0, 3).join(', ')}${data.categories.length > 3 ? '...' : ''}</p>`;
        }
        document.getElementById('knowledgeInfo').innerHTML = html;
    });
}

// Initial load
window.addEventListener('load', () => {
    loadSystemInfo();
    loadKnowledgeInfo();
    userInput.focus();
});

// Refresh info periodically
setInterval(() => {
    loadSystemInfo();
    loadKnowledgeInfo();
}, 30000); // Every 30 seconds
