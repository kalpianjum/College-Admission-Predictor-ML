const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const axios = require("axios");

const app = express();
const PORT = process.env.PORT || 4000;
const FLASK_API_URL = process.env.FLASK_API_URL || "http://127.0.0.1:5000";

app.use(cors({ origin: process.env.FRONTEND_URL || "http://localhost:3000" }));
app.use(bodyParser.json());

// Proxy route to Flask
app.post("/api/predict", async (req, res) => {
    console.log("🔹 Received request from React:", req.body);
    try {
        const response = await axios.post(`${FLASK_API_URL}/predict`, req.body);
        console.log("✅ Response from Flask:", response.data);
    
        res.json(response.data);
      } catch (err) {
        console.error("❌ Prediction error (Express → Flask):", err.message);
    
        // If Flask sent an error response, show that too
        if (err.response) {
          console.error("Flask responded with:", err.response.data);
          res.status(err.response.status).json(err.response.data);
        } else {
          res.status(500).json({ error: "Internal Server Error in Express" });
        }
      }
    });

app.listen(PORT, () => {
  console.log(`🔁 Express server running at http://localhost:${PORT}`);
});
