# API Testing Guide

## Quick Start

### 1. Start the Server
```bash
cd backend
npm install
npm start
```

### 2. Access Swagger UI
Open your browser and go to:
```
http://localhost:3000/api-docs
```

## Testing Steps in Swagger UI

### Step 1: Test Health Check
1. Find the **Health** section
2. Expand `GET /health`
3. Click **"Try it out"**
4. Click **"Execute"**
5. Expected Response:
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "service": "domjudge-automation-api"
}
```

### Step 2: Create a Single Team
1. Find the **Teams** section
2. Expand `POST /api/v1/teams`
3. Click **"Try it out"**
4. In the request body, use the example or enter:
```json
{
  "team": "Test Team",
  "uni": "Test University"
}
```
5. Click **"Execute"**
6. Check the response for:
   - `teamId`: The created team ID
   - `userId`: The created user ID
   - `username`: Generated username (e.g., T12345)
   - `password`: Generated password

### Step 3: Test Dry Run Mode
1. In `POST /api/v1/teams`
2. Set the `dryRun` query parameter to `true`
3. Enter the same request body
4. Click **"Execute"**
5. Response will show what would be created without actually creating it

### Step 4: Create Multiple Teams (Bulk)
1. Expand `POST /api/v1/teams/bulk`
2. Click **"Try it out"**
3. Use the example or enter:
```json
{
  "dryRun": false,
  "teams": [
    {
      "team": "Team Alpha",
      "uni": "University A"
    },
    {
      "team": "Team Beta",
      "uni": "University B",
      "email": "teambeta@example.com"
    }
  ]
}
```
4. Click **"Execute"**
5. Review the response:
   - `total`: Total teams in request
   - `created`: Successfully created
   - `skipped`: Already existing teams
   - `failed`: Failed creations
   - `createdUsers`: Array with credentials

### Step 5: View Existing Data
1. **Get All Teams**: `GET /api/v1/teams`
2. **Get All Organizations**: `GET /api/v1/organizations`
3. **Get All Users**: `GET /api/v1/users`

For each:
- Click "Try it out"
- Click "Execute"
- View the response array

## Request Examples

### Minimal Team Creation
```json
{
  "team": "Team Name",
  "uni": "University Name"
}
```

### Complete Team Creation
```json
{
  "team": "Team Name",
  "uni": "University Name",
  "username": "T12345",
  "password": "mypassword",
  "email": "team@example.com",
  "names": "Member1, Member2, Member3",
  "phone": "1234567890"
}
```

### Bulk Team Creation
```json
{
  "dryRun": false,
  "teams": [
    {
      "team": "Team 1",
      "uni": "University A"
    },
    {
      "team": "Team 2",
      "uni": "University B",
      "email": "team2@example.com"
    }
  ]
}
```

## Response Examples

### Success Response (201)
```json
{
  "success": true,
  "teamId": 12345,
  "userId": 12345,
  "username": "T12345",
  "password": "abc123xyz"
}
```

### Error Response (400)
```json
{
  "errors": [
    {
      "msg": "Team name is required",
      "param": "team",
      "location": "body"
    }
  ]
}
```

### Conflict Response (409)
```json
{
  "success": false,
  "error": "Team 'Team Alpha' already exists"
}
```

## Testing Tips

1. **Always start with Health Check**: Verify the server is running
2. **Use Dry Run First**: Test with `dryRun=true` before creating actual teams
3. **Check Responses**: Always review the response for success/error messages
4. **Save Credentials**: Save the `createdUsers` array for credential distribution
5. **Test Error Cases**: Try invalid data to see error responses
6. **Use Examples**: Swagger UI includes pre-configured examples you can use

## Common Testing Scenarios

### Scenario 1: Create a Team
1. Use `POST /api/v1/teams`
2. Enter team name and university
3. Execute and save the credentials

### Scenario 2: Create Multiple Teams
1. Use `POST /api/v1/teams/bulk`
2. Enter array of teams
3. Review creation statistics
4. Save all credentials from `createdUsers`

### Scenario 3: Test Validation
1. Try creating a team without required fields
2. Check the 400 error response
3. Verify validation messages

### Scenario 4: Test Duplicate Prevention
1. Create a team with a specific name
2. Try to create the same team again
3. Verify 409 conflict response

## Troubleshooting

### Server Not Responding
- Check if server is running: `npm start`
- Verify port 3000 is available
- Check server logs for errors

### Request Fails
- Verify DOMjudge API credentials in `.env`
- Check network connectivity
- Review error response for details

### Swagger UI Not Loading
- Clear browser cache
- Try different browser
- Check server is running on correct port

## Next Steps

After testing:
1. Review the created teams in DOMjudge
2. Verify user accounts are created
3. Test login with generated credentials
4. Use the API in your automation scripts

## Additional Resources

- Swagger UI: `http://localhost:3000/api-docs`
- API Documentation: See `SWAGGER_YAML_GUIDE.md`
- Installation Guide: See `INSTALL.md`
- Main README: See `README.md`

