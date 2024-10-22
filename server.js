const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcrypt'); // Add bcrypt for password hashing
const app = express();
const db = new sqlite3.Database('users.db');

app.use(express.json()); // Use built-in middleware
app.use(express.static('public')); // Serve HTML files

// Create users table
db.serialize(() => {
    db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)");
});

// Serve the login page
app.get('/login', (req, res) => {
    res.sendFile(__dirname + '/templates/login.html'); // Adjust the path as necessary
});

// Serve the signup page
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/templates/signup.html'); // Adjust the path as necessary
});

// Serve the index page
app.get('/index', (req, res) => {
    res.sendFile(__dirname + '/templates/index.html'); // Adjust the path as necessary
});

// Signup route
app.post('/signup', async (req, res) => {
    const { username, password } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10); // Hashing the password

    db.run("INSERT INTO users (username, password) VALUES (?, ?)", [username, hashedPassword], (err) => {
        if (err) {
            res.status(400).send("Error inserting user or username already exists");
        } else {
            res.send("User registered successfully");
        }
    });
});

// Login route
app.post('/login', (req, res) => {
    const { username, password } = req.body;

    db.get("SELECT * FROM users WHERE username = ?", [username], async (err, row) => {
        if (row && await bcrypt.compare(password, row.password)) { // Compare hashed password
            res.send("Login successful");
        } else {
            res.status(401).send("Invalid credentials");
        }
    });
});

// Start server
app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
