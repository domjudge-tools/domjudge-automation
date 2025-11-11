# DOMjudge Automation API

A Node.js/Express backend API for automating team and user creation in DOMjudge contest management system. Built with ES modules and Swagger documentation.

## Features

- ✅ Create teams in DOMjudge
- ✅ Create users linked to teams
- ✅ Create organizations (universities/affiliations)
- ✅ Bulk team creation
- ✅ Dry-run mode for testing
- ✅ Automatic ID generation
- ✅ Username and password generation
- ✅ Duplicate detection
- ✅ Comprehensive error handling
- ✅ Request validation
- ✅ Logging
- ✅ **Swagger/OpenAPI documentation**
- ✅ **ES Modules (.mjs) support**

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- DOMjudge instance with API access
- DOMjudge admin credentials

## Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Configure environment variables in `.env`:
```env
DOMJUDGE_API_BASE=https://bircpc.ir
DOMJUDGE_USERNAME=admin
DOMJUDGE_PASSWORD=your_password_here
DOMJUDGE_CONTEST_ID=1
PORT=3000
NODE_ENV=development
CONTEST_BASE_DIR=./data
CONTEST_STATE_NAME=contest
LOG_LEVEL=info
```

## Running

### Development Mode
```bash
npm run dev
```

### Production Mode
```bash
npm start
```

The server will start on port 3000 (or the port specified in `.env`).

## API Documentation (Swagger)

Once the server is running, access the Swagger UI at:
```
http://localhost:3000/api-docs
```

The Swagger UI provides:
- Interactive API documentation
- Try-it-out functionality
- Request/response schemas
- Example requests and responses

## API Endpoints

### Health Check
```
GET /health
```
Returns server status and timestamp.

### Create Single Team
```
POST /api/v1/teams
Content-Type: application/json

{
  "team": "Team Name",
  "uni": "University Name",
  "username": "T12345",  // Optional, auto-generated if not provided
  "password": "password123",  // Optional, auto-generated if not provided
  "email": "team@example.com",  // Optional
  "names": "Member1, Member2",  // Optional
  "phone": "1234567890"  // Optional
}

Query Parameters:
- dryRun=true  // Optional, for testing without creating
```

**Response:**
```json
{
  "success": true,
  "teamId": 12345,
  "userId": 12345,
  "username": "T12345",
  "password": "abc123xyz"
}
```

### Create Multiple Teams (Bulk)
```
POST /api/v1/teams/bulk
Content-Type: application/json

{
  "dryRun": false,  // Optional
  "teams": [
    {
      "team": "Team 1",
      "uni": "University A",
      "username": "T12345",  // Optional
      "password": "password1",  // Optional
      "email": "team1@example.com",  // Optional
      "names": "Member1, Member2",  // Optional
      "phone": "1234567890"  // Optional
    },
    {
      "team": "Team 2",
      "uni": "University B"
    }
  ]
}
```

**Response:**
```json
{
  "total": 2,
  "created": 2,
  "skipped": 0,
  "failed": 0,
  "results": [
    {
      "success": true,
      "teamId": 12345,
      "userId": 12345,
      "username": "T12345",
      "password": "abc123xyz"
    }
  ],
  "createdUsers": [
    {
      "team": "Team 1",
      "id": 12345,
      "username": "T12345",
      "names": "Member1, Member2",
      "email": "team1@example.com",
      "phone": "1234567890",
      "password": "abc123xyz"
    }
  ]
}
```

### Get All Teams
```
GET /api/v1/teams
```

**Response:**
```json
[
  {
    "name": "Team 1",
    "id": 12345
  }
]
```

### Get All Organizations
```
GET /api/v1/organizations
```

**Response:**
```json
[
  {
    "name": "University A",
    "id": "University A"
  }
]
```

### Get All Users
```
GET /api/v1/users
```

**Response:**
```json
[
  {
    "username": "T12345",
    "id": 12345
  }
]
```

## How It Works

1. **ID Generation**: Generates unique numeric IDs between 10000-99999 for teams and users
2. **Username Generation**: Auto-generates usernames as `T{id}` (e.g., `T12345`) if not provided
3. **Password Generation**: Auto-generates 10-character alphanumeric passwords if not provided
4. **Organization Handling**: Creates organizations if they don't exist, reuses existing ones
5. **Duplicate Detection**: Checks for existing teams, users, and organizations before creating
6. **Team-User Linking**: Creates a user account linked to each team with the same ID

## Example Usage

### Using cURL

Create a single team:
```bash
curl -X POST http://localhost:3000/api/v1/teams \
  -H "Content-Type: application/json" \
  -d '{
    "team": "Team Alpha",
    "uni": "University of Technology",
    "email": "teamalpha@example.com"
  }'
```

Create multiple teams:
```bash
curl -X POST http://localhost:3000/api/v1/teams/bulk \
  -H "Content-Type: application/json" \
  -d '{
    "teams": [
      {
        "team": "Team Alpha",
        "uni": "University of Technology"
      },
      {
        "team": "Team Beta",
        "uni": "University of Science"
      }
    ]
  }'
```

Dry run (test without creating):
```bash
curl -X POST "http://localhost:3000/api/v1/teams?dryRun=true" \
  -H "Content-Type: application/json" \
  -d '{
    "team": "Test Team",
    "uni": "Test University"
  }'
```

### Using JavaScript/TypeScript

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:3000/api/v1',
});

// Create a single team
const createTeam = async () => {
  try {
    const response = await api.post('/teams', {
      team: 'Team Alpha',
      uni: 'University of Technology',
      email: 'teamalpha@example.com',
    });
    console.log('Team created:', response.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};

// Create multiple teams
const createTeamsBulk = async () => {
  try {
    const response = await api.post('/teams/bulk', {
      teams: [
        { team: 'Team Alpha', uni: 'University A' },
        { team: 'Team Beta', uni: 'University B' },
      ],
    });
    console.log('Teams created:', response.data);
  } catch (error) {
    console.error('Error:', error.response?.data);
  }
};
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `409` - Conflict (team/user already exists)
- `500` - Internal Server Error

Error response format:
```json
{
  "error": "Error message",
  "errors": [
    {
      "msg": "Validation error message",
      "param": "team",
      "location": "body"
    }
  ]
}
```

## Logging

Logs are written to:
- `error.log` - Error level logs
- `combined.log` - All logs

In development mode, logs are also displayed in the console.

## Project Structure

```
backend/
├── src/
│   ├── config/          # Configuration (including Swagger)
│   ├── controllers/     # Request handlers
│   ├── middleware/      # Express middleware
│   ├── routes/          # API routes
│   ├── services/        # Business logic (DOMjudge API)
│   ├── utils/           # Utility functions
│   └── server.mjs       # Express server
├── package.json
└── README.md
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DOMJUDGE_API_BASE` | DOMjudge API base URL | Yes | - |
| `DOMJUDGE_USERNAME` | DOMjudge admin username | Yes | - |
| `DOMJUDGE_PASSWORD` | DOMjudge admin password | Yes | - |
| `DOMJUDGE_CONTEST_ID` | Contest ID | Yes | - |
| `PORT` | Server port | No | 3000 |
| `NODE_ENV` | Environment | No | development |
| `CONTEST_BASE_DIR` | Contest data directory | No | ./data |
| `CONTEST_STATE_NAME` | Contest state name | No | contest |
| `LOG_LEVEL` | Logging level | No | info |

## Technology Stack

- **Node.js** - Runtime environment
- **Express** - Web framework
- **ES Modules** - Modern JavaScript module system
- **Swagger/OpenAPI** - API documentation
- **Axios** - HTTP client
- **Winston** - Logging
- **Express Validator** - Request validation
- **Helmet** - Security headers
- **CORS** - Cross-origin resource sharing

## Security

- Uses Helmet.js for security headers
- Validates all input data
- Uses environment variables for sensitive data
- Implements proper error handling
- Logs security-relevant events

## Limitations

- Organization IDs are currently set to the organization name (string)
- Team and user IDs must be unique and numeric (10000-99999)
- One user per team
- Country is hardcoded to "IRN" (Iran)

## Troubleshooting

### Connection Errors
- Verify DOMjudge API URL is correct
- Check network connectivity
- Verify credentials are correct

### Authentication Errors
- Verify DOMjudge username and password
- Check if user has admin permissions
- Verify API endpoint is accessible

### Validation Errors
- Check request body format
- Verify all required fields are present
- Check data types match expected format

### Swagger Documentation Not Loading
- Ensure server is running
- Check that `/api-docs` endpoint is accessible
- Verify Swagger dependencies are installed

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
