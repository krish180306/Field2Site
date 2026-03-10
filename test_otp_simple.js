// Simple test to verify OTP endpoint is working
const testEmail = 'sai.krish6081@gmail.com'; // Change this to your actual email

console.log(`Testing OTP endpoint with email: ${testEmail}\n`);

fetch('http://localhost:5000/api/auth/send-otp', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email: testEmail })
})
    .then(response => response.json())
    .then(data => {
        console.log('✅ SUCCESS!');
        console.log('Response:', data);
        console.log('\n📧 Check your email inbox for the OTP!');
        console.log('(Also check spam/junk folder)\n');
    })
    .catch(error => {
        console.log('❌ ERROR!');
        console.log('Error:', error.message);
        console.log('\nMake sure:');
        console.log('1. Backend server is running (node server/server.js)');
        console.log('2. EMAIL_PASS in .env is correct');
        console.log('3. Check server console for detailed error messages\n');
    });
