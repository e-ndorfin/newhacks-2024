// server/server.js
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const mongoose = require('mongoose');

const app = express();
const PORT = 8000; // You can choose any port that is available

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect('mongodb+srv://zacharytang24:zDTAalcoWz5Ock7Z@pulse.2x4ku.mongodb.net/pulse_db', { 
    useNewUrlParser: true, 
    useUnifiedTopology: true 
})
.then(() => console.log("MongoDB connected"))
.catch(err => console.error("MongoDB connection error:", err));

// Define the Schema and Model
const userSchema = new mongoose.Schema({
    email: String,
    company_name: String,
    company_type: String,
    state: String,
});

const User = mongoose.model('User', userSchema);

// POST route to submit data
app.post('/api/usermodel/submit', async (req, res) => {
    try {
        const user = new User(req.body);
        await user.save();
        res.status(201).json({ message: 'User created successfully', user });
    } catch (error) {
        console.error('Error saving user:', error);
        res.status(500).json({ message: 'Error saving user' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
