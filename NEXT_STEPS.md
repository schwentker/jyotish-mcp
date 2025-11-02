# Next Steps: Building & Running the MCP Server

You've successfully set up Python 3.12 and PostgreSQL 14. Here's what to do next.

---

## ✅ Completed

- [x] Python 3.12 installed (`brew install python@3.12`)
- [x] PostgreSQL 14 installed (`brew install postgresql@14`)
- [x] Virtual environment created with Python 3.12
- [x] Dependencies installed (`pip install -r requirements.txt`)
- [x] Documentation updated
- [x] Repository ready to push to GitHub

---

## 🚀 Next: Build & Run MCP Server

### 1. Install Node.js Dependencies

```bash
cd mcp-server

# Install dependencies (use --legacy-peer-deps for compatibility)
npm install --legacy-peer-deps

# Build TypeScript
npm run build

# Verify build succeeded
ls dist/index.js  # Should exist
```

### 2. Start PostgreSQL & Create Database

```bash
# Start PostgreSQL service
brew services start postgresql@14

# Create database
createdb jyotish

# Verify connection
psql -d jyotish -c "SELECT version();"
```

### 3. Download Swiss Ephemeris Data

```bash
cd calculations/ephemeris_data

# Download ephemeris files (~2MB total, covers 1800-2399 AD)
# Using HTTPS (faster and more reliable than FTP)
wget https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1
wget https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/semo_18.se1  
wget https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1
wget https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sefstars.txt

# Or use curl if wget not available:
# curl -LO https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1
# curl -LO https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/semo_18.se1
# curl -LO https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1
# curl -LO https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sefstars.txt

cd ../..
```

### 4. Test MCP Server (Before Claude Integration)

```bash
# Test that server starts without errors
cd mcp-server
node dist/index.js

# It should start and wait for input
# Press Ctrl+C to exit
```

### 5. Configure Claude Desktop

**Find your absolute paths first:**
```bash
# Get project directory path
pwd

# Should show something like:
# /Users/YOUR_USERNAME/jyotish-mcp
# or /home/YOUR_USERNAME/jyotish-mcp
```

**Edit Claude Desktop config:**

**macOS:**
```bash
# Open config file in editor
code ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Or use nano:
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Add this configuration (replace paths with YOUR absolute paths):**
```json
{
  "mcpServers": {
    "jyotish": {
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/jyotish-mcp/mcp-server/dist/index.js"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/jyotish",
        "EPHEMERIS_PATH": "/ABSOLUTE/PATH/TO/jyotish-mcp/calculations/ephemeris_data"
      }
    }
  }
}
```

**Important:** Replace `/ABSOLUTE/PATH/TO/` with your actual project path from `pwd` above!

### 6. Restart Claude Desktop

1. Quit Claude Desktop completely
2. Reopen Claude Desktop
3. Look for MCP server indicator (should show "jyotish" available)

### 7. Test with Claude

In Claude, try:

```
Can you test the jyotish MCP tools? List what tools are available.
```

If working, Claude should see:
- chart_create
- chart_read
- chart_list
- dasha_current
- transit_now
- divisional_read
- yogas_identify
- compatibility_analyze

Then try a real calculation:
```
Calculate a birth chart for September 27, 1953, 9:10 AM 
in Amritapuri, India (9°08'N, 76°48'E)
```

---

## 🔧 If Issues Occur

**Server won't start:**
```bash
# Check Node version
node --version  # Should be 18+

# Rebuild
cd mcp-server
rm -rf node_modules dist
npm install
npm run build
```

**Database connection fails:**
```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Start if needed
brew services start postgresql@14

# Recreate database
dropdb jyotish
createdb jyotish
```

**Claude doesn't see server:**
1. Check Claude Desktop config has absolute paths
2. Verify server can start: `node mcp-server/dist/index.js`
3. Check Claude Desktop logs: `~/Library/Logs/Claude/`
4. Restart Claude Desktop completely

**See full troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📝 Meanwhile: Push to GitHub

While testing MCP, also push your updates:

```bash
# Make sure you're in project root
cd ~/jyotish-mcp  # or wherever your project is

# Check status
git status

# Push to GitHub
git push origin main
```

If you get authentication errors, use a Personal Access Token:
https://github.com/settings/tokens

---

## 🎯 Once MCP Server Works

**Priority: Build Core Calculations**

The MCP server is ready, but it needs the Python calculation engine. Next priorities:

1. **ephemeris.py** - Swiss Ephemeris wrapper
2. **chart_calculator.py** - Main orchestrator  
3. **nakshatras.py** - Nakshatra calculator
4. **dashas.py** - Vimshottari Dasha
5. **database.py** - PostgreSQL interface
6. **houses.py** - Whole Sign houses

See [PROJECT_STATUS.md](PROJECT_STATUS.md) for detailed next steps.

---

## 📊 Current Status

```
✅ Documentation (100%)
✅ MCP Server Structure (100%)
✅ Python Environment (100%)
✅ PostgreSQL Setup (100%)
⏳ Ephemeris Data (~50% - need to download)
⏳ MCP Integration (pending test)
❌ Calculation Engine (0% - next phase)
❌ Database Schema (0% - next phase)
```

---

## 🎉 You're Making Great Progress!

Your Scorpio depth + Sagittarius wisdom is showing - methodical setup with the bigger vision in mind.

**Questions? Check:**
- [QUICK_START.md](QUICK_START.md) - Setup guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Development roadmap

*Let's get this MCP server talking to Claude!* 🚀
