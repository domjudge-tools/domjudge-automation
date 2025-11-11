# Complete Explanation of `create_teams.py`

## Overview
The `create_teams.py` script is a Python automation tool that creates teams, users, and organizations (universities) in a DOMjudge contest management system. It reads team data from a TSV file and creates corresponding entries in DOMjudge via its REST API.

## Purpose
This script automates the bulk creation of:
1. **Organizations** (Universities/Affiliations) - Educational institutions
2. **Teams** - Contest teams with unique IDs
3. **Users** - User accounts linked to teams with credentials

## How It Works

### 1. **Initialization & Configuration**
```python
load_dotenv()  # Loads environment variables from .env file
```
- Loads configuration from environment variables:
  - `DOMJUDGE_API_BASE`: Base URL of DOMjudge API (e.g., `https://bircpc.ir`)
  - `DOMJUDGE_USERNAME`: Admin username for API authentication
  - `DOMJUDGE_PASSWORD`: Admin password for API authentication
  - `DOMJUDGE_CONTEST_ID`: The contest ID to create teams for
  - `CONTEST_BASE_DIR`: Directory path for storing output files
  - `CONTEST_STATE_NAME`: Name prefix for output files

- Sets up HTTP session with Basic Authentication for API calls

### 2. **Data Source: TSV File Reading**
```python
get_users_from_source("tsv", f"{CONTEST_BASE_DIR}/{CONTEST_STATE_NAME}_credentials.tsv")
```

**TSV Format:**
```
TeamName    Username    Password    UniName
Team1       T12345      abc12       University A
Team2       T12346      xyz34       University B
```

The script reads a TSV file with 4 columns:
- `TeamName`: Name of the team
- `Username`: Username for the user account (optional, can be auto-generated)
- `Password`: Password for the user account (optional, can be auto-generated)
- `UniName`: University/Organization name

### 3. **Fetching Existing Data**
Before creating new entries, the script fetches existing data to avoid duplicates:

- **Organizations** (`get_existing_unis_and_ids()`):
  - GET `/api/v4/contests/{contest_id}/organizations`
  - Returns a dictionary mapping organization names to their IDs

- **Teams** (`get_existing_teams_and_ids()`):
  - GET `/api/v4/contests/{contest_id}/teams`
  - Returns a dictionary mapping team names to their IDs

- **Users** (`get_existing_users_and_ids()`):
  - GET `/api/v4/users`
  - Returns a dictionary mapping usernames to their user IDs

### 4. **ID Generation**
```python
generate_unique_id(existing_ids, lower=10000, upper=99999)
```
- Generates a unique numeric ID between 10000 and 99999
- Ensures the ID doesn't conflict with existing team or user IDs
- This ID is used for both the team and the associated user

### 5. **Organization Creation**
```python
create_or_ignore_uni(entry)
```

**Process:**
1. Checks if the organization already exists
2. If it exists, returns the existing organization ID
3. If not, creates a new organization with:
   - `id`: Organization name (used as ID)
   - `shortname`: Short name (same as name)
   - `name`: Full organization name
   - `formal_name`: Formal name (same as name)
   - `country`: Set to "IRN" (Iran)

**API Call:**
- POST `/api/v4/contests/{contest_id}/organizations`
- Payload: Organization data

### 6. **Team Creation**
For each team in the TSV file that doesn't already exist:

**Team Payload:**
```json
{
  "id": 12345,                    // Unique numeric ID
  "name": "Team Name",            // Team name from TSV
  "display_name": "Team Name",    // Display name
  "description": "Names | Phone", // Optional: names and phone
  "organization_id": "Uni Name",  // Organization ID (name)
  "group_ids": ["3"]              // Group ID (usually 3 for teams)
}
```

**API Call:**
- POST `/api/v4/contests/{contest_id}/teams`
- Returns the created team ID

### 7. **User Creation**
After creating a team, a user account is created:

**User Payload:**
```json
{
  "id": 12345,                    // Same ID as team
  "username": "T12345",           // Generated or from TSV
  "name": "Team Name",            // Team name
  "email": "team@example.com",    // Email from TSV (optional)
  "password": "random10chars",    // Generated or from TSV
  "enabled": true,                // User is enabled
  "team_id": 12345,               // Link to team ID
  "roles": ["team"]               // User role is "team"
}
```

**Username Generation:**
- If provided in TSV, uses that username
- Otherwise, generates `T{unique_id}` (e.g., `T12345`)
- Ensures uniqueness by checking existing usernames

**Password Generation:**
- If provided in TSV, uses that password
- Otherwise, generates a random 10-character alphanumeric string

**API Call:**
- POST `/api/v4/users`
- Returns the created user ID

### 8. **Output Files**
The script generates two JSON files:

1. **`{CONTEST_STATE_NAME}_teams_to_create.json`**:
   - List of teams that will be created (before confirmation)
   - Used for verification before actual creation

2. **`{CONTEST_STATE_NAME}_created_users.json`**:
   - List of all successfully created users with their credentials
   - Contains: team name, user ID, username, names, email, phone, password
   - Can be used for sending credentials via email

### 9. **User Confirmation**
Before creating teams, the script:
1. Shows how many teams will be created
2. Saves a preview file
3. Asks for user confirmation (y/n)
4. Only proceeds if user confirms

### 10. **Error Handling**
- Skips malformed TSV lines
- Handles API errors (non-201 status codes)
- Continues processing even if one team/user fails
- Logs all errors with descriptive messages

## Key Features

1. **Idempotency**: Checks for existing teams/users before creating
2. **Uniqueness**: Ensures unique IDs and usernames
3. **Dry Run Support**: Has a `DRY` flag (currently set to `False`)
4. **Comprehensive Logging**: Prints progress for each operation
5. **Error Recovery**: Continues processing even if individual operations fail
6. **Data Persistence**: Saves created user data for later use (e.g., email sending)

## Workflow Summary

```
1. Load environment variables
2. Read TSV file with team data
3. Fetch existing organizations, teams, and users
4. Filter out teams that already exist
5. Save preview of teams to create
6. Ask user for confirmation
7. For each new team:
   a. Generate unique ID
   b. Create or get organization
   c. Create team with the ID
   d. Create user with the same ID
   e. Link user to team
8. Save created users to JSON file
```

## DOMjudge API Endpoints Used

1. `GET /api/v4/contests/{contest_id}/organizations` - List organizations
2. `POST /api/v4/contests/{contest_id}/organizations` - Create organization
3. `GET /api/v4/contests/{contest_id}/teams` - List teams
4. `POST /api/v4/contests/{contest_id}/teams` - Create team
5. `GET /api/v4/users` - List users
6. `POST /api/v4/users` - Create user

## Authentication
Uses HTTP Basic Authentication with admin credentials:
```python
session.auth = (DOMJUDGE_USERNAME, DOMJUDGE_PASSWORD)
```

## Dependencies
- `requests`: HTTP client for API calls
- `python-dotenv`: Environment variable management
- Standard library: `json`, `os`, `random`, `string`, `typing`

## Usage Example

1. Prepare TSV file: `{CONTEST_STATE_NAME}_credentials.tsv`
2. Set environment variables in `.env` file
3. Run script: `python create_teams.py`
4. Review preview file
5. Confirm creation (y/n)
6. Check output file for created users

## Output Format

**Created Users JSON:**
```json
[
  {
    "team": "Team Name",
    "id": 12345,
    "username": "T12345",
    "names": "Member1, Member2, Member3",
    "email": "team@example.com",
    "phone": "1234567890",
    "password": "abc123xyz"
  }
]
```

## Notes
- The script creates one user per team
- Team ID and User ID are the same (shared)
- Organization ID is the organization name (string)
- Usernames are prefixed with "T" followed by the numeric ID
- Passwords are auto-generated if not provided (10 characters)
- The script skips teams that already exist (idempotent)

