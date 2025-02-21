document.addEventListener('DOMContentLoaded', function() {
    // Show actions on hover
    const messages = document.querySelectorAll('.message');
    
    messages.forEach(message => {
        message.addEventListener('mouseenter', function() {
            this.querySelector('.message-actions').style.display = 'block';
        });
        
        message.addEventListener('mouseleave', function() {
            this.querySelector('.message-actions').style.display = 'none';
        });
        
        // Handle AI button click
        const aiBtn = message.querySelector('.ask-ai-btn');
        aiBtn.addEventListener('click', async function() {
            const messageId = message.dataset.messageId;
            const responseContainer = message.querySelector('.ai-response-container');
            const responseElement = responseContainer.querySelector('.ai-response');
            
            // Show loading state
            responseElement.textContent = 'Getting AI response...';
            responseContainer.style.display = 'block';
            
            try {
                const response = await fetch('/api/ai-response/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ message_id: messageId })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    responseElement.textContent = data.response;
                } else {
                    responseElement.textContent = 'Error getting AI response';
                }
            } catch (error) {
                responseElement.textContent = 'Error: Could not get AI response';
            }
        });
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 