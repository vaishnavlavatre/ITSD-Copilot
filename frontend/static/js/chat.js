class ChatApp {
    constructor() {
        this.token = localStorage.getItem('authToken');
        this.conversationHistory = [];
        
        this.initializeEventListeners();
        this.checkAuthentication();
        this.updateCurrentTime();
    }

    initializeEventListeners() {
        // Login form
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.login();
            });
        }

        // Chat functionality
        const sendBtn = document.getElementById('sendBtn');
        const userInput = document.getElementById('userInput');
        
        if (sendBtn) {
            sendBtn.addEventListener('click', () => this.sendMessage());
        }
        
        if (userInput) {
            userInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.sendMessage();
            });
        }

        // Quick actions
        document.querySelectorAll('.quick-action').forEach(button => {
            button.addEventListener('click', (e) => {
                const query = e.target.getAttribute('data-query');
                document.getElementById('userInput').value = query;
                this.sendMessage();
            });
        });

        // Logout
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.logout());
        }
    }

    updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
        });
        const currentTimeElement = document.getElementById('currentTime');
        if (currentTimeElement) {
            currentTimeElement.textContent = timeString;
        }
    }

    async login() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const errorDiv = document.getElementById('loginError');

        // Clear previous errors
        errorDiv.textContent = '';
        
        // Add loading state
        const loginBtn = document.querySelector('.login-btn');
        const originalText = loginBtn.innerHTML;
        loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing In...';
        loginBtn.disabled = true;

        try {
            const response = await fetch('http://localhost:5000/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.token = data.access_token;
                localStorage.setItem('authToken', this.token);
                this.showChatInterface(data.user);
            } else {
                errorDiv.textContent = data.error || 'Login failed. Please check your credentials.';
            }
        } catch (error) {
            errorDiv.textContent = 'Network error. Please make sure the backend server is running on http://localhost:5000';
            console.error('Login error:', error);
        } finally {
            // Restore button state
            loginBtn.innerHTML = originalText;
            loginBtn.disabled = false;
        }
    }

    showChatInterface(user) {
        console.log('Showing chat interface for user:', user);
        
        const loginScreen = document.getElementById('loginScreen');
        const chatInterface = document.getElementById('chatInterface');
        
        if (loginScreen) loginScreen.style.display = 'none';
        if (chatInterface) chatInterface.style.display = 'flex';
        
        // Update user info
        const userDisplayName = document.getElementById('userDisplayName');
        const userRole = document.getElementById('userRole');
        
        if (userDisplayName) userDisplayName.textContent = user.name;
        if (userRole) {
            userRole.textContent = user.role;
            userRole.style.background = user.role === 'admin' ? 
                'linear-gradient(135deg, #ef4444, #dc2626)' : 
                'linear-gradient(135deg, #10b981, #059669)';
        }
        
        this.updateCurrentTime();
    }

    async sendMessage() {
        const userInput = document.getElementById('userInput');
        const message = userInput.value.trim();
        
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        userInput.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        try {
            const response = await this.queryCopilot(message);
            this.removeTypingIndicator();
            this.addMessage(response.response, 'bot');
            
            // Add to conversation history
            this.addToHistory(message);
            
        } catch (error) {
            this.removeTypingIndicator();
            this.addMessage('Sorry, I encountered an error while processing your request. Please try again.', 'bot');
            console.error('Error:', error);
        }
    }

    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.id = 'typingIndicator';
        
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        
        if (chatMessages) {
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    async queryCopilot(message) {
        if (!this.token) {
            throw new Error('Not authenticated');
        }

        const response = await fetch('http://localhost:5000/chat/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify({ query: message })
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        return await response.json();
    }

    addMessage(content, sender) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const headerDiv = document.createElement('div');
        headerDiv.className = 'message-header';
        
        const timeDiv = document.createElement('span');
        timeDiv.className = 'message-time';
        
        // Set avatar and header
        if (sender === 'user') {
            avatarDiv.innerHTML = '<i class="fas fa-user"></i>';
            headerDiv.innerHTML = `<strong>You</strong>`;
            timeDiv.textContent = new Date().toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit',
                hour12: true 
            });
        } else {
            avatarDiv.innerHTML = '<i class="fas fa-robot"></i>';
            headerDiv.innerHTML = `<strong>ITSD Copilot</strong>`;
            timeDiv.textContent = new Date().toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit',
                hour12: true 
            });
        }
        
        headerDiv.appendChild(timeDiv);
        contentDiv.appendChild(headerDiv);
        
        // Create message text container
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        
        // Enhanced content formatting
        this.formatMessageContent(content, messageText, sender);
        
        contentDiv.appendChild(messageText);
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    formatMessageContent(content, container, sender) {
        // Split content by lines and process each line
        const lines = content.split('\n');
        
        lines.forEach(line => {
            if (line.trim() === '') return;
            
            // Check for article sections
            if (line.includes('📖 **') && line.includes('**')) {
                this.createArticleSection(line, container, sender);
                return;
            }
            
            // Check for command help sections
            if (line.startsWith('- `') && line.includes('`:')) {
                this.createCommandHelp(line, container, sender);
                return;
            }
            
            // Check for troubleshooting sections
            if (line.startsWith('- **') && line.includes('**:')) {
                this.createTroubleshootingItem(line, container, sender);
                return;
            }
            
            // Check for automation steps
            if (line.startsWith('  Command: `')) {
                this.createAutomationStep(line, container, sender);
                return;
            }
            
            // Check for section headers
            if (line.startsWith('**') && line.endsWith('**') && !line.includes('📖')) {
                this.createSectionHeader(line, container, sender);
                return;
            }
            
            // Regular text with basic formatting
            this.createRegularText(line, container, sender);
        });
    }

    createArticleSection(line, container, sender) {
        const articleDiv = document.createElement('div');
        articleDiv.className = 'article-item';
        
        // Extract title and content
        const titleMatch = line.match(/📖 \*\*(.*?)\*\*/);
        const contentText = line.replace(/📖 \*\*(.*?)\*\*/, '').trim();
        
        if (titleMatch) {
            const titleDiv = document.createElement('div');
            titleDiv.className = 'article-title';
            titleDiv.innerHTML = `<i class="fas fa-book-open"></i>${titleMatch[1]}`;
            articleDiv.appendChild(titleDiv);
        }
        
        if (contentText) {
            const contentDiv = document.createElement('div');
            contentDiv.className = 'article-content';
            contentDiv.textContent = contentText;
            articleDiv.appendChild(contentDiv);
        }
        
        container.appendChild(articleDiv);
    }

    createCommandHelp(line, container, sender) {
        const commandDiv = document.createElement('div');
        commandDiv.className = 'command-help';
        
        // Extract command and description
        const commandMatch = line.match(/- `(.*?)`:(.*)/);
        if (commandMatch) {
            const syntaxDiv = document.createElement('div');
            syntaxDiv.className = 'command-syntax';
            syntaxDiv.textContent = commandMatch[1].trim();
            
            const descDiv = document.createElement('div');
            descDiv.className = 'command-description';
            descDiv.textContent = commandMatch[2].trim();
            
            commandDiv.appendChild(syntaxDiv);
            commandDiv.appendChild(descDiv);
        } else {
            // Fallback to regular text
            this.createRegularText(line, container, sender);
            return;
        }
        
        container.appendChild(commandDiv);
    }

    createTroubleshootingItem(line, container, sender) {
        const troubleDiv = document.createElement('div');
        troubleDiv.className = 'troubleshooting-item';
        
        // Extract error and solution
        const errorMatch = line.match(/- \*\*(.*?)\*\*:(.*)/);
        if (errorMatch) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'troubleshooting-error';
            errorDiv.textContent = errorMatch[1].trim();
            
            const solutionDiv = document.createElement('div');
            solutionDiv.className = 'troubleshooting-solution';
            solutionDiv.textContent = errorMatch[2].trim();
            
            troubleDiv.appendChild(errorDiv);
            troubleDiv.appendChild(solutionDiv);
        } else {
            // Fallback to regular text
            this.createRegularText(line, container, sender);
            return;
        }
        
        container.appendChild(troubleDiv);
    }

    createAutomationStep(line, container, sender) {
        // Find the previous step description
        const lastChild = container.lastChild;
        if (lastChild && lastChild.classList.contains('step-item')) {
            const commandDiv = document.createElement('div');
            commandDiv.className = 'step-command';
            
            // Extract command
            const commandMatch = line.match(/Command: `(.*?)`/);
            if (commandMatch) {
                commandDiv.textContent = commandMatch[1];
                lastChild.appendChild(commandDiv);
            }
        }
    }

    createSectionHeader(line, container, sender) {
        const header = document.createElement('div');
        header.className = 'section-header';
        header.style.cssText = 'font-weight: 700; color: #1e293b; margin: 15px 0 10px 0; padding-bottom: 5px; border-bottom: 2px solid #667eea;';
        
        // Remove ** from the line
        const cleanText = line.replace(/\*\*/g, '');
        header.textContent = cleanText;
        
        container.appendChild(header);
    }

    createRegularText(line, container, sender) {
        const textDiv = document.createElement('div');
        textDiv.style.marginBottom = '8px';
        
        // Basic formatting
        let formattedText = line
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/`(.*?)`/g, '<code>$1</code>');
        
        // Check if this is a step description for automation
        if (line.startsWith('- ') && !line.startsWith('- **') && !line.startsWith('- `')) {
            const stepDiv = document.createElement('div');
            stepDiv.className = 'step-item';
            
            const descDiv = document.createElement('div');
            descDiv.className = 'step-description';
            descDiv.innerHTML = line.replace('- ', '');
            
            stepDiv.appendChild(descDiv);
            container.appendChild(stepDiv);
            return;
        }
        
        textDiv.innerHTML = formattedText;
        container.appendChild(textDiv);
    }

    addToHistory(message) {
        this.conversationHistory.push({
            query: message,
            timestamp: new Date().toLocaleTimeString()
        });

        this.updateHistoryUI();
    }

    updateHistoryUI() {
        const historyContainer = document.getElementById('conversationHistory');
        if (!historyContainer) return;
        
        // Clear existing history except the "no history" message
        while (historyContainer.firstChild) {
            historyContainer.removeChild(historyContainer.firstChild);
        }

        // Show last 5 conversations
        const recentHistory = this.conversationHistory.slice(-5).reverse();
        
        if (recentHistory.length === 0) {
            const noHistory = document.createElement('div');
            noHistory.className = 'no-history';
            noHistory.textContent = 'No conversations yet';
            historyContainer.appendChild(noHistory);
            return;
        }
        
        recentHistory.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.textContent = item.query.substring(0, 40) + (item.query.length > 40 ? '...' : '');
            historyItem.title = item.query;
            historyItem.addEventListener('click', () => {
                document.getElementById('userInput').value = item.query;
                document.getElementById('userInput').focus();
            });
            historyContainer.appendChild(historyItem);
        });
    }

    checkAuthentication() {
        if (this.token) {
            // Verify token is still valid
            this.verifyToken();
        } else {
            // Show login screen
            const loginScreen = document.getElementById('loginScreen');
            if (loginScreen) loginScreen.style.display = 'flex';
        }
    }

    async verifyToken() {
        try {
            const response = await fetch('http://localhost:5000/auth/profile', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const userData = await response.json();
                this.showChatInterface(userData);
            } else {
                this.logout();
            }
        } catch (error) {
            console.error('Token verification error:', error);
            this.logout();
        }
    }

    logout() {
        localStorage.removeItem('authToken');
        this.token = null;
        
        const chatInterface = document.getElementById('chatInterface');
        const loginScreen = document.getElementById('loginScreen');
        
        if (chatInterface) chatInterface.style.display = 'none';
        if (loginScreen) loginScreen.style.display = 'flex';
        
        // Clear forms and errors
        const loginError = document.getElementById('loginError');
        const loginForm = document.getElementById('loginForm');
        
        if (loginError) loginError.textContent = '';
        if (loginForm) loginForm.reset();
        
        // Clear conversation
        this.conversationHistory = [];
        const chatMessages = document.getElementById('chatMessages');
        if (chatMessages) {
            chatMessages.innerHTML = `
                <div class="message bot-message welcome-message">
                    <div class="message-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-content">
                        <div class="message-header">
                            <strong>ITSD Copilot</strong>
                            <span class="message-time" id="currentTime"></span>
                        </div>
                        <div class="message-text">
                            <p>Hello! I'm your AI-powered IT Service Desk Assistant. I can help you with:</p>
                            <ul>
                                <li>Unix command syntax and troubleshooting</li>
                                <li>System monitoring and status checks</li>
                                <li>Ford-specific procedures and KB articles</li>
                                <li>Automated task guidance</li>
                            </ul>
                            <p>How can I assist you today?</p>
                        </div>
                    </div>
                </div>
            `;
        }
        this.updateCurrentTime();
    }
}

// Initialize chat app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing ChatApp...');
    new ChatApp();
});