// app/api/usermodel/submit/route.js
import dbConnect from '@/lib/mongodb'; // Adjust the import path as necessary
import User from '@/models/User'; // Adjust the import path as necessary

export async function POST(req) {
    await dbConnect(); // Ensure the database is connected

    const body = await req.json(); // Parse the request body

    console.log('Request body:', body);

    try {
        const user = new User(body);
        await user.save();
        return new Response(JSON.stringify({ message: 'User created successfully', user }), {
            status: 201,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    } catch (error) {
        console.error('Error saving user:', error);
        return new Response(JSON.stringify({ message: 'Error saving user' }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }
}
