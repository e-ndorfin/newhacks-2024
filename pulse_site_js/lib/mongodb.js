// lib/mongodb.js
import mongoose from 'mongoose';

const connection = {}; // Store the connection state

async function dbConnect() {
    if (connection.isConnected) {
        return;
    }

    const db = await mongoose.connect('mongodb+srv://zacharytang24:zDTAalcoWz5Ock7Z@pulse.2x4ku.mongodb.net/pulse_db', { 
        useNewUrlParser: true, 
        useUnifiedTopology: true 
    });

    connection.isConnected = db.connections[0].readyState;
}

export default dbConnect;
