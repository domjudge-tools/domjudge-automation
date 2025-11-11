# Installation Guide

## Prerequisites

- **Node.js** version 18.0.0 or higher
- **npm** version 9.0.0 or higher (or **yarn**)
- DOMjudge instance with API access
- DOMjudge admin credentials

## Quick Start

1. **Navigate to the backend directory:**
```bash
cd backend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create environment file:**
```bash
cp .env.example .env
```

4. **Configure environment variables:**
Edit the `.env` file with your DOMjudge credentials:
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

5. **Start the server:**
```bash
# Development mode (with auto-reload)
npm run dev

# Production mode
npm start
```

6. **Access the API:**
- API Base URL: `http://localhost:3000`
- Swagger Documentation: `http://localhost:3000/api-docs`
- Health Check: `http://localhost:3000/health`

## Detailed Installation

### Step 1: Verify Node.js Version

Check your Node.js version:
```bash
node --version
```

Should be 18.0.0 or higher. If not, install a newer version from [nodejs.org](https://nodejs.org/).

### Step 2: Install Dependencies

All dependencies are listed in `package.json`. Install them with:
```bash
npm install
```

This will install:
- **express** - Web framework
- **dotenv** - Environment variable management
- **axios** - HTTP client for DOMjudge API
- **cors** - Cross-origin resource sharing
- **helmet** - Security headers
- **express-validator** - Request validation
- **winston** - Logging
- **swagger-ui-express** - Swagger UI for API documentation
- **swagger-jsdoc** - Swagger documentation generator

### Step 3: Configure Environment Variables

Create a `.env` file in the backend directory:

```env
# DOMjudge API Configuration
DOMJUDGE_API_BASE=https://bircpc.ir
DOMJUDGE_USERNAME=admin
DOMJUDGE_PASSWORD=your_password_here
DOMJUDGE_CONTEST_ID=1

# Server Configuration
PORT=3000
NODE_ENV=development

# Contest Configuration
CONTEST_BASE_DIR=./data
CONTEST_STATE_NAME=contest

# Logging
LOG_LEVEL=info
```

### Step 4: Verify Installation

Test the installation:
```bash
# Check if all dependencies are installed
npm list --depth=0

# Start the server
npm start
```

You should see:
```
Server started on port 3000
Swagger documentation available at http://localhost:3000/api-docs
```

## Troubleshooting

### Issue: Module not found errors

**Solution:**
```bash
# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall dependencies
npm install
```

### Issue: Port already in use

**Solution:**
Change the `PORT` in `.env` file to a different port (e.g., 3001, 3002).

### Issue: Cannot connect to DOMjudge API

**Solution:**
1. Verify `DOMJUDGE_API_BASE` is correct
2. Check network connectivity
3. Verify DOMjudge credentials
4. Ensure DOMjudge API is accessible

### Issue: Swagger documentation not loading

**Solution:**
1. Ensure server is running
2. Check that port is correct
3. Verify Swagger dependencies are installed:
```bash
npm list swagger-ui-express swagger-jsdoc
```

### Issue: ES Module errors

**Solution:**
Ensure `package.json` has `"type": "module"` and you're using Node.js 18+.

## Production Deployment

### Build for Production

1. Set `NODE_ENV=production` in `.env`
2. Ensure all environment variables are set
3. Start the server:
```bash
npm start
```

### Using PM2 (Process Manager)

```bash
# Install PM2 globally
npm install -g pm2

# Start the application
pm2 start src/server.mjs --name domjudge-api

# Save PM2 configuration
pm2 save

# Setup PM2 to start on system boot
pm2 startup
```

### Using Docker

Create a `Dockerfile`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "src/server.mjs"]
```

Build and run:
```bash
docker build -t domjudge-api .
docker run -p 3000:3000 --env-file .env domjudge-api
```

## Verifying Installation

After installation, verify everything works:

1. **Health Check:**
```bash
curl http://localhost:3000/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "service": "domjudge-automation-api"
}
```

2. **Swagger Documentation:**
Open `http://localhost:3000/api-docs` in your browser.

3. **List Teams:**
```bash
curl http://localhost:3000/api/v1/teams
```

## Next Steps

- Read the [README.md](./README.md) for API usage
- Check [API Documentation](./README.md#api-endpoints) for endpoints
- Explore [Swagger UI](http://localhost:3000/api-docs) for interactive documentation

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the logs in `error.log` and `combined.log`
3. Verify all environment variables are set correctly
4. Ensure Node.js version is 18+

