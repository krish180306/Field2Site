# OTP Email Verification - Testing Guide

## Current Status

✅ **Backend Code**: OTP endpoints added to `server/server.js`
- `/api/auth/send-otp` - Sends OTP to email
- `/api/auth/verify-otp` - Verifies OTP code

✅ **Frontend Code**: SignUp page updated with 3-step OTP flow
- Step 1: Enter email
- Step 2: Verify OTP
- Step 3: Complete signup form

✅ **Email Configuration**: Set up in `.env`
- Sender: filed2site@gmail.com
- SMTP: Gmail (smtp.gmail.com:587)

⚠️ **Email Password**: Needs to be verified in `.env`
- Current value in file: `your-app-password-here`
- You mentioned you added it, but it may not be saved yet

⚠️ **Server Status**: Running but needs restart
- Server was started 3+ hours ago (before OTP code was added)
- New OTP endpoints won't be available until server restarts

---

## How to Test OTP Functionality

### Step 1: Verify Email Password

1. Open `server/.env` file
2. Make sure `EMAIL_PASS` has your actual Gmail app password (not the placeholder)
3. Save the file

### Step 2: Restart Backend Server

**Stop the current server:**
- Go to the terminal running `node server/server.js`
- Press `Ctrl+C` to stop it

**Start the server again:**
```bash
cd server
node server.js
```

Or from the root directory:
```bash
node server/server.js
```

### Step 3: Test via Frontend

1. Open browser to http://localhost:5173/signup
2. Enter your email address
3. Click "Send OTP"
4. Check your email inbox (and spam folder) for the OTP
5. Enter the 4-digit OTP code
6. Click "Verify OTP"
7. Complete the signup form

### Step 4: Test via API (Optional)

Using PowerShell:
```powershell
$body = @{email='your-email@gmail.com'} | ConvertTo-Json
$response = Invoke-RestMethod -Uri 'http://localhost:5000/api/auth/send-otp' -Method Post -Body $body -ContentType 'application/json'
Write-Host "Response: $($response | ConvertTo-Json)"
```

---

## Expected Behavior

### Successful OTP Send:
- **Frontend**: Shows "OTP sent successfully" message
- **Backend Console**: Logs `OTP sent to {email}: {otp_code}`
- **Email**: Receives styled email with 4-digit OTP

### Successful OTP Verification:
- **Frontend**: Proceeds to signup form (Step 3)
- **Backend**: Returns `{success: true, message: 'OTP verified successfully'}`

---

## Troubleshooting

### "Cannot POST /api/auth/send-otp"
- **Cause**: Server needs restart
- **Fix**: Stop and restart the backend server

### "Failed to send OTP email"
- **Cause**: Invalid Gmail app password or network issue
- **Fix**: 
  1. Verify EMAIL_PASS in .env is correct
  2. Make sure 2-Step Verification is enabled on Gmail
  3. Generate a new app password if needed

### Email not received
- Check spam/junk folder
- Verify the email address is correct
- Check backend console for error messages
- Verify EMAIL_USER in .env is filed2site@gmail.com

### "Invalid login" error in backend
- Gmail app password is incorrect
- Using regular password instead of app password
- 2-Step Verification not enabled

---

## Quick Checklist

- [ ] Email password added to `server/.env`
- [ ] Backend server restarted
- [ ] Frontend dev server running (http://localhost:5173)
- [ ] Navigate to signup page
- [ ] Test OTP sending
- [ ] Check email inbox
- [ ] Test OTP verification
- [ ] Complete signup flow
