import React, { useState } from 'react';
import axios from 'axios';

function OpenAIChat() {
  const [inputText, setInputText] = useState('');
  const [response, setResponse] = useState('');

  const apiKey = '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'; // Replace with your OpenAI API key

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        'https://api.openai.com/v1/engines/davinci/completions',
        {
          prompt: inputText,
          max_tokens: 50,
        },
        {
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
          },
        }
      );

      setResponse(response.data.choices[0].text);
    } catch (error) {
      console.error('Error fetching response:', error);
    }
  };

  return (
    <div>
      <h1>OpenAI Chat</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          rows="4"
          cols="50"
          value={inputText}
          onChange={handleInputChange}
          placeholder="Enter your message..."
        />
        <br />
        <button type="submit">Submit</button>
      </form>
      {response && (
        <div>
          <h2>Response:</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default OpenAIChat;
