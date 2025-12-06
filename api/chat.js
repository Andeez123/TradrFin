// Vercel Serverless Function for /api/chat
const mysql = require('mysql2');

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

module.exports = async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    let body;
    try {
        body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
    } catch (e) {
        return res.status(400).json({ error: 'Invalid JSON' });
    }
    
    const { message } = body;
    if (!message) {
        return res.status(400).json({ error: 'Message is required' });
    }
    
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
    res.json({ 
        reply: "I am your Financial AI Copilot. You can ask me about **Market Sentiment**, specific stocks like **TSLA** or **MSFT**, or review your **Trade History**." 
    });
};

