// App.js
import React, { useState } from 'react';

function App() {
  const [rank, setRank] = useState('');
  const [category, setCategory] = useState('');
  const [branchCode, setBranchCode] = useState('');
  const [instReg, setInstReg] = useState('');
  const [predictions, setPredictions] = useState([]);
  const [error, setError] = useState('');

  const handlePredict = async () => {
    setError('');
    setPredictions([]);

    // Basic field validation
    if (!rank || !category || !branchCode || !instReg) {
      setError('⚠ All fields are required.');
      return;
    }

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:4000';
      const response = await fetch(`${apiUrl}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rank: rank.trim(),
          category_gender: category.trim().toUpperCase(),
          branch_code: branchCode.trim().toUpperCase(),
          inst_reg: instReg.trim().toUpperCase()
        })
      });

      const result = await response.json();
      console.log("✅ Received result:", result);

      if (!response.ok) {
        setError(result.error || '❌ Unexpected error from server.');
      } else if (!Array.isArray(result.result)) {
        setError('❌ Invalid response format.');
      } else {
        setPredictions(result.result);
      }
    } catch (err) {
      console.error("❌ Network error:", err);
      setError('🚫 Could not connect to server. Please try again later.');
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>🎓 College Admission Predictor</h1>

      <input
        placeholder="Enter Rank"
        type="number"
        value={rank}
        onChange={(e) => setRank(e.target.value)}
      /><br /><br />

      <input
        placeholder="Enter Category (e.g. BCE_GIRLS)"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
      /><br /><br />

      <input
        placeholder="Enter Branch Code (e.g. CSE)"
        value={branchCode}
        onChange={(e) => setBranchCode(e.target.value)}
      /><br /><br />

      <input
        placeholder="Enter Region (e.g. AU)"
        value={instReg}
        onChange={(e) => setInstReg(e.target.value)}
      /><br /><br />

      <button onClick={handlePredict}>🔍 Predict</button>

      <hr />

      {error && (
        <div style={{ color: 'red', marginTop: '10px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {predictions.length > 0 && (
        <div>
          <h2>🎯 Top Eligible Colleges:</h2>
          {predictions.map((college, index) => (
            <div key={index} style={{ marginBottom: '10px' }}>
              <strong>{college.NAME}</strong><br />
              Code: {college.INSTCODE} <br />
              Fee: ₹{college.FEE} <br />
              Type: {college.TYPE}
              <hr />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
