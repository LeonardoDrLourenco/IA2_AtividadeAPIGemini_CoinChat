document.getElementById('chat-button').addEventListener('click', async () => {
    const userInput = document.getElementById('chat-input').value;
    const messagesDiv = document.getElementById('chat-output');

    if (!userInput.trim()) {
        return;
    }

    messagesDiv.innerHTML += `<div><strong>Você:</strong> ${userInput}</div>`;
    document.getElementById('chat-input').value = '';

    const lowerInput = userInput.toLowerCase();

    try {
        if (lowerInput.includes('preço do bitcoin')) {
            const response = await fetch('/api/bitcoin-price');
            const data = await response.json();
            if (data.price_usd) {
                messagesDiv.innerHTML += `<div><strong>Chatbot:</strong> O preço atual do Bitcoin é: $${data.price_usd.toFixed(2)}</div>`;
            } else {
                messagesDiv.innerHTML += `<div><strong>Chatbot:</strong> Desculpe, não foi possível obter o preço do Bitcoin.</div>`;
            }
        } else if (lowerInput.includes('converter bitcoin para')) {
            const currency = lowerInput.split('para')[1].trim().toUpperCase(); 
            const response = await fetch(`/api/convert?currency=${currency}`);
            const data = await response.json();
            if (data.price) {
                messagesDiv.innerHTML += `<div><strong>Chatbot:</strong> O preço do Bitcoin em ${currency} é: ${data.price.toFixed(2)} ${currency}</div>`;
            } else {
                messagesDiv.innerHTML += `<div><strong>Chatbot:</strong> Desculpe, não foi possível converter para ${currency}.</div>`;
            }
        } else {
            messagesDiv.innerHTML += `<div><strong>Chatbot:</strong> Desculpe, não entendi sua pergunta.</div>`;
        }
    } catch (error) {
        console.error('Erro ao processar a requisição:', error);
        messagesDiv.innerHTML += `<div><strong>Chatbot:</strong> Ocorreu um erro ao processar sua solicitação.</div>`;
    }

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});
