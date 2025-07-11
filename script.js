    // server.js (Node.js + Express + sqlite3)
    const express = require('express');
    const sqlite3 = require('sqlite3').verbose();
    const bodyParser = require('body-parser');
    const app = express();
    app.use(bodyParser.json());
    app.use(bodyParser.urlencoded({ extended: true }));

    // Initialize SQLite DB
    const db = new sqlite3.Database('./accounts.db');
    db.run('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)');

    // Login endpoint
    app.post('/login', (req, res) => {
        const { username, password } = req.body;
        db.get('SELECT * FROM users WHERE username = ? AND password = ?', [username, password], (err, row) => {
            if (row) {
                res.json({ success: true });
            } else {
                res.json({ success: false });
            }
        });
    });

    // Sign up endpoint
    app.post('/signup', (req, res) => {
        const { username, password } = req.body;
        db.run('INSERT INTO users (username, password) VALUES (?, ?)', [username, password], (err) => {
            if (err) {
                res.json({ success: false });
            } else {
                res.json({ success: true });
            }
        });
    });

    app.listen(3000, () => console.log('Server running on port 3000'));
