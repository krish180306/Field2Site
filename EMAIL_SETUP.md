# Email OTP Setup Guide

## Gmail Configuration for OTP Emails

The application is configured to send OTP emails from **filed2site@gmail.com**.

### Step 1: Enable 2-Step Verification

1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** in the left sidebar
3. Under "Signing in to Google", click **2-Step Verification**
4. Follow the steps to enable 2-Step Verification

### Step 2: Generate App Password

1. After enabling 2-Step Verification, go back to **Security**
2. Under "Signing in to Google", click **App passwords**
3. You may need to sign in again
4. In the "Select app" dropdown, choose **Mail**
5. In the "Select device" dropdown, choose **Other (Custom name)**
6. Enter "Field2Site Backend" as the name
7. Click **Generate**
8. Google will show you a 16-character password (e.g., `abcd efgh ijkl mnop`)
9. **Copy this password** - you won't be able to see it again!

### Step 3: Update .env File

1. Open `server/.env` file
2. Replace `your-app-password-here` with the app password you just generated
3. Remove any spaces from the password

Example:
```env
EMAIL_PASS=abcdefghijklmnop
```

### Step 4: Restart the Server

After updating the .env file, restart the backend server:

```bash
# Stop the current server (Ctrl+C in the terminal)
# Then restart it
npm run server
```

### Step 5: Test OTP Email

1. Go to http://localhost:5173/signup
2. Enter an email address
3. Click "Send OTP"
4. Check the email inbox for the OTP

---

## Current Configuration

- **Sender Email**: filed2site@gmail.com
- **SMTP Host**: smtp.gmail.com
- **SMTP Port**: 587
- **Security**: TLS

---

## Troubleshooting

### "Invalid login" error
- Make sure you've enabled 2-Step Verification
- Make sure you're using an App Password, not your regular Gmail password
- Check that there are no spaces in the password in .env file

### "Connection timeout" error
- Check your internet connection
- Make sure port 587 is not blocked by your firewall

### Email not received
- Check spam/junk folder
- Verify the recipient email address is correct
- Check server console for any error messages

---

## Security Notes

⚠️ **Important:**
- Never commit the .env file to Git
- The .env file is already in .gitignore
- Keep your app password secure
- Don't share your app password with anyone
