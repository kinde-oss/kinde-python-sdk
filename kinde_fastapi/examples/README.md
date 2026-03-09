# Kinde FastAPI Example

This is an example FastAPI application that demonstrates how to use the Kinde FastAPI integration.

## Setup

1. Install the required dependencies:
```bash
pip install fastapi uvicorn python-multipart python-dotenv
```

2. Configure your Kinde application:
   - Create a new application in your Kinde dashboard
   - Set the redirect URI to `http://localhost:8000/callback`
   - Copy your client ID and client secret

3. Create a `.env` file in the examples directory with the following variables:
```env
KINDE_CLIENT_ID=your_client_id
KINDE_CLIENT_SECRET=your_client_secret
KINDE_REDIRECT_URI=http://localhost:8000/callback
KINDE_HOST=https://your-domain.kinde.com
```

## Running the Example

Run the example application from the SDK root directory:
```bash
python -m uvicorn kinde_fastapi.examples.example_app:app --reload --port 8000
```

The application will be available at `http://localhost:8000`.

## Features Demonstrated

1. **Authentication Flow**
   - Login with Kinde
   - OAuth callback handling
   - Session management
   - Logout

2. **Automatic Route Registration**
   - The OAuth class automatically registers these routes:
     - `/login` - Redirects to Kinde login
     - `/callback` - Handles OAuth callback from Kinde
     - `/logout` - Logs out the user
     - `/register` - Redirects to Kinde registration
     - `/user` - Returns user information (JSON)

3. **Protected Routes**
   - Example of a protected route that requires authentication
   - Automatic redirection to login for unauthenticated users

4. **User Information**
   - Retrieving and displaying user information
   - Session-based user state management

## API Endpoints

- `/` - Home page (shows different content based on authentication status)
- `/login` - Redirects to Kinde login (auto-registered)
- `/callback` - Handles OAuth callback from Kinde (auto-registered)
- `/logout` - Logs out the user (auto-registered)
- `/register` - Redirects to Kinde registration (auto-registered)
- `/user` - Returns user information as JSON (auto-registered)
- `/protected` - Example protected route

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
6. Implement role-based access control
