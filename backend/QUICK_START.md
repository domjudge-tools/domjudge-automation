# Quick Start Guide - Interactive Swagger UI

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd backend
npm install
```

### Step 2: Configure Environment
Create a `.env` file:
```env
DOMJUDGE_API_BASE=https://bircpc.ir
DOMJUDGE_USERNAME=admin
DOMJUDGE_PASSWORD=your_password
DOMJUDGE_CONTEST_ID=1
PORT=3000
NODE_ENV=development
```

### Step 3: Start Server
```bash
npm start
```

## 📖 Using Swagger UI

### Access Swagger UI
Open your browser and go to:
```
http://localhost:3000/api-docs
```

### Test the API (Start Here!)

1. **Test GET Request:**
   - Find `GET /api/v1/test` in the Health section
   - Click **"Try it out"** button
   - Click **"Execute"** button
   - You should see a success response!

2. **Test POST Request:**
   - Find `POST /api/v1/test` in the Health section
   - Click **"Try it out"** button
   - Enter JSON in the request body (or use the example)
   - Click **"Execute"** button
   - Check the response!

3. **Test Health Check:**
   - Find `GET /health` in the Health section
   - Click **"Try it out"** → **"Execute"**
   - Verify server is running

### Create a Team

1. Find `POST /api/v1/teams` in the Teams section
2. Click **"Try it out"**
3. Select an example from the dropdown or enter:
```json
{
  "team": "My Test Team",
  "uni": "My University"
}
```
4. Click **"Execute"**
5. View the response with team ID, username, and password

## ✅ Verification Checklist

- [ ] Server starts without errors
- [ ] Swagger UI loads at `http://localhost:3000/api-docs`
- [ ] "Try it out" buttons are visible and clickable
- [ ] Test GET endpoint works (`GET /api/v1/test`)
- [ ] Test POST endpoint works (`POST /api/v1/test`)
- [ ] Health check works (`GET /health`)
- [ ] Can send requests and see responses

## 🔧 Troubleshooting

### Swagger UI Not Loading
- Check server is running: `npm start`
- Verify port 3000 is available
- Clear browser cache
- Try different browser

### "Try it out" Button Not Working
- Check browser console for errors
- Verify server is running
- Check CORS configuration
- Try the test endpoints first

### Requests Failing
- Check server logs for errors
- Verify DOMjudge API credentials in `.env`
- Check network connectivity
- Verify request format matches examples

### Cannot See Response
- Check browser network tab
- Verify server is processing requests
- Check server logs
- Try test endpoints first

## 📝 Next Steps

Once test endpoints work:
1. Test health check endpoint
2. Try creating a team (start with dryRun=true)
3. View existing teams
4. Create multiple teams in bulk

## 🎯 Quick Test Commands

Test with cURL:
```bash
# Test GET
curl http://localhost:3000/api/v1/test

# Test POST
curl -X POST http://localhost:3000/api/v1/test \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Test Health
curl http://localhost:3000/health
```

## 💡 Tips

1. **Always start with test endpoints** to verify Swagger UI is working
2. **Use dryRun=true** when testing team creation
3. **Check responses** for success/error messages
4. **Save credentials** from created users
5. **Use examples** provided in Swagger UI

## 📚 More Help

- Full Testing Guide: See `TESTING_GUIDE.md`
- API Documentation: See `README.md`
- Swagger YAML Guide: See `SWAGGER_YAML_GUIDE.md`

