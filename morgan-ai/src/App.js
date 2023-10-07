import React, { useState } from 'react';

function App() {
  // State to store the user input
  const [inputText, setInputText] = useState('');
  // State to store the submitted text for display
  const [submittedText, setSubmittedText] = useState('');

  // Function to handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // Set the submitted text to the input text
    setSubmittedText(inputText);
  };

  return (
    <div className="App">
      <h1>React Form Example</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Enter Text:
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
        </label>
        <button type="submit">Submit</button>
      </form>
      {submittedText && (
        <div>
          <h2>Submitted Text:</h2>
          <p>{submittedText}</p>
        </div>
      )}
    </div>
  );
}

export default App;