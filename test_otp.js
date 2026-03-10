const axios = require('axios');

// Test OTP sending
async function testOTP() {
    try {
        console.log('Testing OTP email sending...\n');

        // Test email - you can change this to your email
        const testEmail = 'saikrishna@example.com'; // Change to your actual email to receive OTP

        console.log(`Sending OTP to: ${testEmail}`);

        const response = await axios.post('http://localhost:5000/api/auth/send-otp', {
            email: testEmail
        });

        console.log('\n✅ SUCCESS!');
        console.log('Response:', response.data);
        console.log('\n📧 Check your email inbox for the OTP!');
        console.log('(Also check spam/junk folder if you don\'t see it)\n');

    } catch (error) {
        console.log('\n❌ ERROR!');
        if (error.response) {
            console.log('Status:', error.response.status);
            console.log('Error:', error.response.data);
        } else {
            console.log('Error:', error.message);
        }
        console.log('\nTroubleshooting:');
        console.log('1. Make sure the backend server is running (node server/server.js)');
        console.log('2. Check that EMAIL_PASS in .env is correct');
        console.log('3. Verify Gmail app password is valid');
        console.log('4. Check server console for detailed error messages\n');
    }
}

testOTP();
