// Load environment variables
require('dotenv').config();

const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');


const app = express();
app.use(cors()); // Allows React to talk to this server
app.use(express.json());

// Cloud Database Connection Pool
const pool = mysql.createPool({
    host: process.env.DB_HOST || 'your-cloud-db-host',
    user: process.env.DB_USER || 'your-db-username',
    password: process.env.DB_PASSWORD || 'your-db-password',
    database: process.env.DB_NAME || 'your-database-name',
    port: parseInt(process.env.DB_PORT) || 3306,
    ssl: process.env.DB_SSL === 'true' ? {
        rejectUnauthorized: true
    } : false,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// Test database connection
pool.getConnection((err, connection) => {
    if (err) {
        console.error('Database connection failed:', err);
        return;
    }
    console.log('Connected to cloud database successfully!');
    connection.release();
});

// API Endpoint: Get Sentiment Data
app.get('/api/sentiment', (req, res) => {
    const query = 'SELECT * FROM sentiment_agent ORDER BY id DESC LIMIT 50';
    pool.query(query, (err, results) => {
        if (err) {
            console.error('Error fetching sentiment data:', err);
            return res.status(500).json({
                error: err.message,
                message: 'Failed to fetch sentiment data from cloud database'
            });
        }
        res.json(results);
    });
});

// API Endpoint: Get Market Data
app.get('/api/market-data', (req, res) => {
    const query = 'SELECT * FROM market_data_agent ORDER BY date DESC LIMIT 100';
    pool.query(query, (err, results) => {
        if (err) {
            console.error('Error fetching market data:', err);
            return res.status(500).json({
                error: err.message,
                message: 'Failed to fetch market data from cloud database'
            });
        }
        res.json(results);
    });
});

// API Endpoint: Get Transaction History
app.get('/api/transactions', (req, res) => {
    const query = 'SELECT * FROM asset_movement_agent ORDER BY crosscheck_id DESC LIMIT 100';
    pool.query(query, (err, results) => {
        if (err) {
            console.error('Error fetching transactions:', err);
            return res.status(500).json({
                error: err.message,
                message: 'Failed to fetch transaction data from cloud database'
            });
        }
        res.json(results);
    });
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({
        status: 'ok',
        message: 'Backend server is running and connected to cloud database',
        timestamp: new Date().toISOString()
    });
});

const PORT = parseInt(process.env.PORT) || 5000;
app.listen(PORT, () => {
    console.log(`Backend Server running on port ${PORT}`);
    console.log('Make sure to set your cloud database environment variables in .env file');
});

// AI Logic Endpoint
app.post('/api/chat', (req, res) => {
    const { message } = req.body;
    const lowerMsg = message.toLowerCase();

    // 1. If user asks about SENTIMENT
    if (lowerMsg.includes('sentiment') || lowerMsg.includes('news')) {
        const query = 'SELECT summary, sentiment FROM sentiment_agent ORDER BY id DESC LIMIT 1';
        pool.query(query, (err, results) => {
            if (err || results.length === 0) return res.json({ reply: "I'm having trouble accessing the news feed right now." });

            const row = results[0];
            const reply = `Based on the latest analysis, market sentiment is currently **${row.sentiment.toUpperCase()}**. The key driver is: "${row.summary}"`;
            res.json({ reply });
        });
        return;
    }

    // 2. If user asks about TSLA (Example of specific ticker check)
    if (lowerMsg.includes('tsla') || lowerMsg.includes('tesla')) {
        const query = "SELECT price, rsi, summary FROM market_data_agent WHERE ticker = 'TSLA' ORDER BY date DESC LIMIT 1";
        pool.query(query, (err, results) => {
            if (err || results.length === 0) return res.json({ reply: "I don't have recent data for Tesla at the moment." });

            const row = results[0];
            const reply = `Tesla (TSLA) is trading at **$${row.price}**. The RSI is ${row.rsi.toFixed(1)}. My technical analysis suggests: "${row.summary}"`;
            res.json({ reply });
        });
        return;
    }

    // 3. Default / General Fallback
    setTimeout(() => {
        res.json({
            reply: "I am your Financial AI Copilot. You can ask me about **Market Sentiment**, specific stocks like **TSLA** or **MSFT**, or review your **Trade History**."
        });
    }, 500); // Fake delay for realism
});