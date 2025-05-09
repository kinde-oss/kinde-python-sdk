# Kinde Flask Example

This is an example Flask application that demonstrates how to use the Kinde Flask integration.

## Setup

1. Install the required dependencies:
```bash
pip install flask python-dotenv
```

2. Configure your Kinde application:
   - Create a new application in your Kinde dashboard
   - Set the redirect URI to `http://localhost:5000/callback`
   - Copy your client ID and client secret

3. Create a `.env` file in the examples directory with the following variables:
```
KINDE_CLIENT_ID=your_client_id
KINDE_CLIENT_SECRET=your_client_secret
KINDE_REDIRECT_URI=http://localhost:5000/callback
KINDE_DOMAIN=your_kinde_domain
```

## Running the Example

Run the example application:
```bash
python example_app.py
```

The application will be available at `http://localhost:5000`.

## Features Demonstrated

1. **Authentication Flow**
   - Login with Kinde
   - OAuth callback handling
   - Session management
   - Logout

2. **Protected Routes**
   - Example of a protected route that requires authentication
   - Automatic redirection to login for unauthenticated users

3. **User Information**
   - Retrieving and displaying user information
   - Session-based user state management

## API Endpoints

- `/` - Home page (shows different content based on authentication status)
- `/login` - Redirects to Kinde login
- `/callback` - Handles OAuth callback from Kinde
- `/logout` - Logs out the user
- `/user` - Returns user information

## Security Considerations

1. Always use HTTPS in production
2. Use a secure session secret key
3. Implement proper state parameter validation
4. Handle OAuth errors appropriately
5. Implement proper session management
6. Consider implementing CSRF protection

## Next Steps

1. Add proper error handling
2. Implement state parameter validation
3. Add more security features
4. Use proper templates instead of inline HTML
5. Add user profile management 