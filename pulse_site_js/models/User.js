// models/User.js
import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
    email: String,
    company_name: String,
    company_type: String,
    state: String,
});

export default mongoose.models.User || mongoose.model('User', userSchema);
