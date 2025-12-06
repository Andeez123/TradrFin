// Vercel Serverless Function for /api/sentiment
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
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'GET') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

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
};

