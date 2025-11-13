class VATSALWebGUI {
    constructor() {
        this.consoleElement = document.getElementById('output-console');
        this.commandInput = document.getElementById('command-input');
        this.executeBtn = document.getElementById('execute-btn');
        this.clearBtnTop = document.getElementById('clear-btn-top');
        this.clearBtnBottom = document.getElementById('clear-btn-bottom');
        this.themeBtn = document.getElementById('theme-btn');
        this.vatsalToggle = document.getElementById('vatsal-toggle');
        this.selfOperatingToggle = document.getElementById('self-operating-toggle');
        
        this.isDarkTheme = false;
        this.isVatsalOn = true;
        this.isSelfOperatingOn = true;
        
        this.init();
    }
    
    init() {
        this.updateDateTime();
        setInterval(() => this.updateDateTime(), 1000);
        
        this.executeBtn.addEventListener('click', () => this.executeCommand());
        this.commandInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.executeCommand();
            }
        });
        
        this.clearBtnTop.addEventListener('click', () => this.clearConsole());
        this.clearBtnBottom.addEventListener('click', () => this.clearConsole());
        
        this.themeBtn.addEventListener('click', () => this.toggleTheme());
        
        this.vatsalToggle.addEventListener('click', () => this.toggleVatsal());
        this.selfOperatingToggle.addEventListener('click', () => this.toggleSelfOperating());
        
        document.getElementById('settings-btn').addEventListener('click', () => {
            this.addConsoleMessage('Settings panel coming soon...', 'system-message');
        });
        
        document.getElementById('volume-btn').addEventListener('click', () => {
            this.addConsoleMessage('Volume controls coming soon...', 'system-message');
        });
        
        document.getElementById('power-btn').addEventListener('click', () => {
            this.addConsoleMessage('Power options coming soon...', 'system-message');
        });
        
        this.addConsoleMessage('VATSAL Web GUI Initialized Successfully! 🚀', 'system-message');
        this.addConsoleMessage('Ready to assist you, Boss!', 'response-message');
    }
    
    updateDateTime() {
        const now = new Date();
        
        const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        const dateStr = now.toLocaleDateString('en-US', dateOptions);
        
        const timeStr = now.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit',
            hour12: true 
        });
        
        document.getElementById('current-date').textContent = dateStr;
        document.getElementById('current-time').textContent = timeStr;
    }
    
    async executeCommand() {
        const command = this.commandInput.value.trim();
        
        if (!command) {
            this.addConsoleMessage('Please enter a command first!', 'system-message');
            return;
        }
        
        this.addConsoleMessage(`User Command: ${command}`, 'query-message');
        
        this.commandInput.value = '';
        
        this.addConsoleMessage('Processing your request...', 'system-message');
        
        try {
            const response = await fetch('/api/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.addConsoleMessage(`VATSAL: ${data.response}`, 'response-message');
                
                if (data.technical_details) {
                    this.addConsoleMessage(`⚙ Technical Details:\n${data.technical_details}`, 'technical-message');
                }
            } else {
                this.addConsoleMessage(`Error: ${data.message}`, 'system-message');
            }
        } catch (error) {
            this.addConsoleMessage(`Connection Error: ${error.message}`, 'system-message');
            this.addConsoleMessage('This is a demo interface. Backend API connection will be established when integrated with VATSAL core.', 'suggestion-message');
        }
    }
    
    addConsoleMessage(message, className = 'console-message') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `console-message ${className}`;
        messageDiv.innerHTML = message.replace(/\n/g, '<br>');
        
        this.consoleElement.appendChild(messageDiv);
        
        this.consoleElement.scrollTop = this.consoleElement.scrollHeight;
    }
    
    clearConsole() {
        const confirmClear = confirm('Are you sure you want to clear the console output?');
        if (confirmClear) {
            this.consoleElement.innerHTML = '';
            this.addConsoleMessage('Console cleared successfully!', 'system-message');
            this.addConsoleMessage('Ready for new commands...', 'response-message');
        }
    }
    
    toggleTheme() {
        this.isDarkTheme = !this.isDarkTheme;
        document.body.classList.toggle('dark-theme');
        
        this.addConsoleMessage(
            `Theme switched to ${this.isDarkTheme ? 'Dark' : 'Light'} mode! 🎨`, 
            'system-message'
        );
    }
    
    toggleVatsal() {
        this.isVatsalOn = !this.isVatsalOn;
        this.vatsalToggle.classList.toggle('active');
        this.vatsalToggle.textContent = `VATSAL: ${this.isVatsalOn ? 'ON' : 'OFF'}`;
        
        const dot = document.createElement('span');
        dot.className = 'toggle-dot';
        this.vatsalToggle.insertBefore(dot, this.vatsalToggle.firstChild);
        
        this.addConsoleMessage(
            `VATSAL System ${this.isVatsalOn ? 'Activated' : 'Deactivated'}!`, 
            'system-message'
        );
    }
    
    toggleSelfOperating() {
        this.isSelfOperatingOn = !this.isSelfOperatingOn;
        this.selfOperatingToggle.classList.toggle('active');
        this.selfOperatingToggle.innerHTML = `
            <span class="toggle-icon">🤖</span>
            Self-Operating: ${this.isSelfOperatingOn ? 'ON' : 'OFF'}
        `;
        
        this.addConsoleMessage(
            `Self-Operating Mode ${this.isSelfOperatingOn ? 'Enabled' : 'Disabled'}!`, 
            'system-message'
        );
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new VATSALWebGUI();
});
