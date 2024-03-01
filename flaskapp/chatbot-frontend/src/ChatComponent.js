import React, { useState } from 'react';

const ChatComponent = () => {
    const [userInput, setUserInput] = useState('');
    const [response, setResponse] = useState('');

    const handleInputChange = (e) => {
        setUserInput(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        // Using Fetch API to send data to Flask server
        fetch('http://127.0.0.1:5000/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: userInput }),
        })
        .then(response => response.json())
        .then(data => setResponse(data.response))
        .catch(error => {
            console.error('Error:', error);
            setResponse('Error getting response from the server.');
        });
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={userInput}
                    onChange={handleInputChange}
                    placeholder="Say something..."
                />
                <button type="submit">Send</button>
            </form>
            {response && <p>{response}</p>}
        </div>
    );
};

export default ChatComponent;
