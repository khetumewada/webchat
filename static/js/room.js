let chatSocket;
let typingTimer;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

// Update connection status
function updateConnectionStatus(status) {
    const statusElement = document.getElementById('connectionStatus');
    const sendBtn = document.getElementById('sendBtn');
    const messageInput = document.getElementById('messageInput');
    statusElement.className = `connection-status ${status}`;

    switch (status) {
        case 'connected':
            statusElement.textContent = 'Connected';
            statusElement.style.display = 'none';
            sendBtn.disabled = false;
            messageInput.disabled = false;
            reconnectAttempts = 0;
            break;
        case 'connecting':
            statusElement.textContent = 'Connecting...';
            statusElement.style.display = 'block';
            sendBtn.disabled = true;
            messageInput.disabled = true;
            break;
        case 'disconnected':
            statusElement.textContent = 'Disconnected - Trying to reconnect...';
            statusElement.style.display = 'block';
            sendBtn.disabled = true;
            messageInput.disabled = true;
            break;
    }
}

// Format timestamp to show correct time (5:49 format)
function formatTimestamp(timestamp) {
    const messageTime = new Date(timestamp);
    return messageTime.toLocaleTimeString([], {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

// Update all message timestamps to show correct time
function updateTimestamps() {
    const messages = document.querySelectorAll('.message[data-timestamp]');
    messages.forEach(message => {
        const timestamp = message.getAttribute('data-timestamp');
        const timeElement = message.querySelector('.message-time');
        if (timeElement && timestamp) {
            timeElement.textContent = formatTimestamp(timestamp);
        }
    });
}

// Initialize WebSocket connection
function initWebSocket() {
    updateConnectionStatus('connecting');

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/chat/${chatId}/`;

    chatSocket = new WebSocket(wsUrl);

    chatSocket.onopen = function (e) {
        console.log('WebSocket connection established');
        updateConnectionStatus('connected');
    };

    chatSocket.onmessage = function (e) {
        try {
            const data = JSON.parse(e.data);

            if (data.type === 'chat_message') {
                addMessageToChat(data.message, data.sender, data.timestamp, data.sender_id);
            } else if (data.type === 'typing_indicator') {
                handleTypingIndicator(data.user, data.is_typing);
            }
        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
        }
    };

    chatSocket.onclose = function (e) {
        console.log('WebSocket connection closed');
        updateConnectionStatus('disconnected');

        if (reconnectAttempts < maxReconnectAttempts) {
            reconnectAttempts++;
            setTimeout(initWebSocket, 3000 * reconnectAttempts);
        }
    };

    chatSocket.onerror = function (e) {
        console.error('WebSocket error:', e);
        updateConnectionStatus('disconnected');
    };
}

// Add message to chat with correct timestamp
function addMessageToChat(message, sender, timestamp, senderId) {
    const messagesContainer = document.getElementById('messagesContainer');
    const messageDiv = document.createElement('div');
    const isOwn = senderId === currentUserId;
    const now = new Date().toISOString();
    const currentTime = new Date().toLocaleTimeString([], {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });

    messageDiv.className = `message ${isOwn ? 'sent' : 'received'}`;
    messageDiv.setAttribute('data-timestamp', now);
    messageDiv.innerHTML = `
        <div class="message-text">${escapeHtml(message)}</div>
        <div class="message-time">${currentTime}</div>
    `;

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Send message
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();

    if (!message) return;

    if (chatSocket.readyState !== WebSocket.OPEN) {
        alert('Connection lost. Please wait for reconnection.');
        return;
    }

    try {
        chatSocket.send(JSON.stringify({
            'type': 'chat_message',
            'message': message
        }));
        messageInput.value = '';

        // Stop typing indicator
        chatSocket.send(JSON.stringify({
            'type': 'typing',
            'is_typing': false
        }));

    } catch (error) {
        console.error('Error sending message:', error);
    }
}

// Handle typing indicator
function handleTypingIndicator(user, isTyping) {
    const typingIndicator = document.getElementById('typingIndicator');

    if (isTyping) {
        typingIndicator.textContent = `${user} is typing...`;
        typingIndicator.style.display = 'block';
    } else {
        typingIndicator.style.display = 'none';
    }
}

// Send typing indicator
function sendTypingIndicator(isTyping) {
    if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
        try {
            chatSocket.send(JSON.stringify({
                'type': 'typing',
                'is_typing': isTyping
            }));
        } catch (error) {
            console.error('Error sending typing indicator:', error);
        }
    }
}

// Event listeners
document.getElementById('sendBtn').addEventListener('click', sendMessage);

document.getElementById('messageInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
});

// Typing indicator
document.getElementById('messageInput').addEventListener('input', function () {
    sendTypingIndicator(true);

    clearTimeout(typingTimer);
    typingTimer = setTimeout(() => {
        sendTypingIndicator(false);
    }, 1000);
});

// Dropdown functionality
let dropdownVisible = false;

function toggleChatDropdown() {
    const menu = document.getElementById('chatDropdownMenu');
    const toggleBtn = document.getElementById('dropdownToggleBtn');

    if (!menu) {
        console.error('Chat dropdown menu element not found');
        return;
    }

    dropdownVisible = !dropdownVisible;

    if (dropdownVisible) {
        menu.classList.add('show');
        toggleBtn.style.background = 'rgba(255,255,255,0.2)';
    } else {
        menu.classList.remove('show');
        toggleBtn.style.background = 'transparent';
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function () {
    initWebSocket();

    // Scroll to bottom
    const messagesContainer = document.getElementById('messagesContainer');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Update all existing timestamps to show correct format
    updateTimestamps();

    // Setup dropdown functionality
    const dropdownToggleBtn = document.getElementById('dropdownToggleBtn');
    if (dropdownToggleBtn) {
        dropdownToggleBtn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            toggleChatDropdown();
        });
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', function (e) {
        const menu = document.getElementById('chatDropdownMenu');
        const toggleBtn = document.getElementById('dropdownToggleBtn');

        if (menu && toggleBtn && !menu.contains(e.target) && !toggleBtn.contains(e.target) && dropdownVisible) {
            menu.classList.remove('show');
            toggleBtn.style.background = 'transparent';
            dropdownVisible = false;
        }
    });

    // Close dropdown with Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && dropdownVisible) {
            const menu = document.getElementById('chatDropdownMenu');
            const toggleBtn = document.getElementById('dropdownToggleBtn');
            if (menu) {
                menu.classList.remove('show');
                toggleBtn.style.background = 'transparent';
                dropdownVisible = false;
            }
        }
    });
});

// Clean up on page unload
window.addEventListener('beforeunload', function () {
    if (chatSocket) {
        chatSocket.close();
    }
});

// -- Message Search bar--
document.getElementById('chatSearchInput').addEventListener('input', function () {
    const query = this.value.trim().toLowerCase();
    const resultsDiv = document.getElementById('chatSearchResults');
    const messages = document.querySelectorAll('.message');
    resultsDiv.innerHTML = '';

    if (query.length > 0) {
        let matchingMessages = [];
        messages.forEach((message, index) => {
            const messageText = message.querySelector('.message-text');
            const messageTime = message.querySelector('.message-time');
            if (messageText && messageText.textContent.toLowerCase().includes(query)) {
                matchingMessages.push({
                    txt: messageText.textContent,
                    time: messageTime ? messageTime.textContent : '',
                    el: message,
                    idx: index
                });
            }
        });

        if (matchingMessages.length > 0) {
            matchingMessages.slice(0, 5).forEach(match => {
                const div = document.createElement('div');
                div.style.cssText = 'display: flex; flex-direction: column; align-items: flex-start; padding: 12px 16px; cursor: pointer; border-bottom: 1px solid var(--border-color); transition: var(--transition); background: transparent;';
                // highlight query
                const txtMarked = match.txt.replace(new RegExp(query, "gi"),
                    str => `<mark style="background: #ffeb3b; padding: 1px 2px; border-radius: 2px;">${str}</mark>`);
                div.innerHTML = `
                        <div style="font-size: 13px; color: var(--text-primary); margin-bottom: 3px; font-weight: 500;">${txtMarked}</div>
                        <div style="font-size: 11px; color: var(--text-secondary);">${match.time}</div>
                    `;
                div.addEventListener('mouseenter', () => {
                    div.style.backgroundColor = 'var(--hover-color)';
                });
                div.addEventListener('mouseleave', () => {
                    div.style.backgroundColor = 'transparent';
                });
                div.addEventListener('click', () => {
                    match.el.scrollIntoView({behavior: 'smooth', block: 'center'});
                    match.el.style.backgroundColor = '#fff3cd';
                    setTimeout(() => {
                        match.el.style.backgroundColor = '';
                    }, 1500);
                    resultsDiv.style.display = 'none';
                    document.getElementById('chatSearchInput').value = '';
                });
                resultsDiv.appendChild(div);
            });
            if (matchingMessages.length > 5) {
                const moreDiv = document.createElement('div');
                moreDiv.style.cssText = 'padding: 8px 12px; text-align: center; color: var(--text-secondary); font-size: 11px; font-style: italic;';
                moreDiv.textContent = `+${matchingMessages.length - 5} more results`;
                resultsDiv.appendChild(moreDiv);
            }
            resultsDiv.style.display = 'block';
        } else {
            resultsDiv.innerHTML = '<div style="padding: 24px; text-align: center; color: var(--text-secondary); font-size: 12px;">No messages found</div>';
            resultsDiv.style.display = 'block';
        }
    } else {
        resultsDiv.style.display = 'none';
    }
});

// Hide chat search results when clicking outside
document.addEventListener('click', function (e) {
    const chatSearchInput = document.getElementById('chatSearchInput');
    const chatSearchResults = document.getElementById('chatSearchResults');
    if (!chatSearchInput.contains(e.target) && !chatSearchResults.contains(e.target)) {
        chatSearchResults.style.display = 'none';
    }
});

// Clear search when pressing Escape
document.getElementById('chatSearchInput').addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        this.value = '';
        document.getElementById('chatSearchResults').style.display = 'none';
    }
});
