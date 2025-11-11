# Swagger API Documentation Setup

## Overview

The API includes comprehensive Swagger/OpenAPI documentation that allows you to:
- View all available endpoints
- Test API requests directly from the browser
- See request/response schemas
- View example requests and responses

## Accessing Swagger UI

Once the server is running, access the Swagger UI at:
```
http://localhost:3000/api-docs
```

You can also access the raw OpenAPI JSON specification at:
```
http://localhost:3000/api-docs.json
```

## Features

### 1. Interactive API Testing
- Click "Try it out" on any endpoint
- Fill in the request parameters
- Execute the request and see the response
- View request/response examples

### 2. Request Examples
Each endpoint includes multiple example requests:
- Basic examples with minimal required fields
- Complete examples with all optional fields
- Dry-run examples for testing

### 3. Response Schemas
All endpoints document their response schemas including:
- Success responses (200, 201)
- Error responses (400, 409, 500)
- Response examples

### 4. Server Selection
You can select from multiple server URLs:
- `http://localhost:3000` - Default development server
- `http://127.0.0.1:3000` - Alternative localhost address

## Testing Requests in Swagger UI

### Creating a Single Team

1. Navigate to `POST /api/v1/teams`
2. Click "Try it out"
3. Select an example from the dropdown or enter your own data:
```json
{
  "team": "Team Alpha",
  "uni": "University of Technology",
  "email": "team@example.com"
}
```
4. Click "Execute"
5. View the response with team ID, username, and password

### Creating Multiple Teams (Bulk)

1. Navigate to `POST /api/v1/teams/bulk`
2. Click "Try it out"
3. Enter team data:
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
      "uni": "University B"
    }
  ]
}
```
4. Click "Execute"
5. View the response with creation statistics

### Dry Run Mode

Test requests without actually creating teams:
1. Add `?dryRun=true` as a query parameter for single team creation
2. Or set `"dryRun": true` in the request body for bulk creation
3. The response will show what would be created without making actual API calls

## Configuration

### CORS Settings
The API is configured to allow requests from Swagger UI:
- All origins allowed (`*`)
- All HTTP methods supported
- Required headers allowed

### Helmet Security
Helmet is configured to allow Swagger UI resources:
- Content Security Policy disabled for Swagger
- Cross-Origin Embedder Policy disabled

### Request Limits
- JSON body limit: 10MB
- URL-encoded body limit: 10MB

## Troubleshooting

### Swagger UI Not Loading
1. Verify the server is running
2. Check that port 3000 is accessible
3. Clear browser cache
4. Check browser console for errors

### Requests Failing in Swagger UI
1. Verify DOMjudge API credentials in `.env`
2. Check server logs for errors
3. Verify network connectivity to DOMjudge API
4. Check CORS settings if accessing from different origin

### Response Not Showing
1. Check browser network tab for actual response
2. Verify server logs for errors
3. Check that DOMjudge API is accessible
4. Verify request body matches schema

## API Endpoints Documented

### Teams
- `POST /api/v1/teams` - Create a single team
- `POST /api/v1/teams/bulk` - Create multiple teams
- `GET /api/v1/teams` - Get all teams

### Organizations
- `GET /api/v1/organizations` - Get all organizations

### Users
- `GET /api/v1/users` - Get all users

### Health
- `GET /health` - Health check endpoint

## Swagger Options

The Swagger UI is configured with:
- **persistAuthorization**: true - Saves authorization tokens
- **displayRequestDuration**: true - Shows request timing
- **filter**: true - Enables endpoint filtering
- **tryItOutEnabled**: true - Enables "Try it out" by default
- **supportedSubmitMethods**: ['get', 'post', 'put', 'delete', 'patch']

## Customization

To customize Swagger UI, edit `src/server.mjs`:
```javascript
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec, {
  customCss: '.swagger-ui .topbar { display: none }',
  customSiteTitle: 'DOMjudge Automation API Documentation',
  swaggerOptions: {
    // Add your custom options here
  },
}));
```

## OpenAPI Specification

The OpenAPI 3.0 specification is generated from JSDoc comments in:
- `src/routes/*.mjs` - Route definitions with Swagger annotations
- `src/controllers/*.mjs` - Controller documentation
- `src/config/swagger.mjs` - Schema definitions

To modify the specification, edit these files and restart the server.

