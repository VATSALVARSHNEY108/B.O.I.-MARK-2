// Modern GUI JavaScript

let socket;
let startTime = Date.now();

// Initialize WebSocket connection
function initSocket() {
    socket = io();
    
    socket.on('connect', () => {
        console.log('✓ Connected to server');
        updateStatusIndicator(true);
    });
    
    socket.on('disconnect', () => {
        console.log('✗ Disconnected from server');
        updateStatusIndicator(false);
    });
    
    socket.on('command_result', (data) => {
        handleCommandResult(data);
    });
    
    socket.on('command_started', (data) => {
        logToConsole(`> ${data.command}`, 'command');
        logToConsole('Processing...', 'normal');
    });
}

// Update clock
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    document.getElementById('clock').textContent = timeString;
}

// Update active time
function updateActiveTime() {
    const elapsed = Math.floor((Date.now() - startTime) / 60000);
    document.getElementById('activeTime').textContent = `${elapsed}m`;
}

// Update status indicator
function updateStatusIndicator(online) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-text');
    
    if (online) {
        statusDot.classList.add('online');
        statusDot.classList.remove('offline');
        statusText.textContent = 'Online';
    } else {
        statusDot.classList.remove('online');
        statusDot.classList.add('offline');
        statusText.textContent = 'Offline';
    }
}

// Log message to console
function logToConsole(message, type = 'normal') {
    const console = document.getElementById('console');
    const line = document.createElement('div');
    line.className = `console-line ${type}`;
    line.textContent = message;
    console.appendChild(line);
    console.scrollTop = console.scrollHeight;
}

// Execute command
function executeCommand() {
    const input = document.getElementById('commandInput');
    const command = input.value.trim();
    
    if (!command) {
        return;
    }
    
    input.value = '';
    
    // Log command
    logToConsole(`> ${command}`, 'command');
    
    // Execute via WebSocket
    if (socket && socket.connected) {
        socket.emit('execute_command', { command: command });
    } else {
        // Fallback to HTTP request
        fetch('/api/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ command: command })
        })
        .then(response => response.json())
        .then(data => handleCommandResult(data))
        .catch(error => {
            logToConsole(`❌ Error: ${error}`, 'error');
        });
    }
}

// Handle command result
function handleCommandResult(data) {
    if (data.success) {
        logToConsole(`✓ ${data.message}`, 'success');
    } else {
        logToConsole(`❌ ${data.message}`, 'error');
    }
    
    // Update stats
    if (data.stats) {
        document.getElementById('commandsRun').textContent = data.stats.commands_run;
        document.getElementById('successRate').textContent = `${data.stats.success_rate}%`;
    }
    
    // Update history
    if (data.history) {
        updateHistory(data.history);
    }
}

// Update history list
function updateHistory(history) {
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = '';
    
    if (history.length === 0) {
        historyList.innerHTML = '<li class="history-empty">No commands yet</li>';
        return;
    }
    
    history.reverse().forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.timestamp} - ${item.command.substring(0, 40)}${item.command.length > 40 ? '...' : ''}`;
        historyList.appendChild(li);
    });
}

// Set command in input
function setCommand(command) {
    const input = document.getElementById('commandInput');
    input.value = command;
    input.focus();
}

// Handle Enter key press
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        executeCommand();
    }
}

// Load stats on startup
function loadStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            if (data.stats) {
                document.getElementById('commandsRun').textContent = data.stats.commands_run;
                document.getElementById('successRate').textContent = `${data.stats.success_rate}%`;
            }
            if (data.history) {
                updateHistory(data.history);
            }
        })
        .catch(error => {
            console.error('Failed to load stats:', error);
        });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initSocket();
    updateClock();
    setInterval(updateClock, 1000);
    setInterval(updateActiveTime, 60000);
    loadStats();
    
    logToConsole('Welcome to VATSAL AI Assistant! 👋', 'success');
    logToConsole('Type a command to get started.', 'normal');
});
