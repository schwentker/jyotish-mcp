# Troubleshooting Guide

Common issues and solutions for Jyotish MCP setup.

---

## Python Version Issues

### Error: `pydantic-core` requires Rust compiler

**Symptom:**
```
error: can't find Rust compiler
Building wheel for pydantic-core (pyproject.toml) ... error
```

**Cause:** Python 3.13 is too new - some dependencies don't have pre-built wheels yet.

**Solution:** Use Python 3.12 instead

```bash
# Install Python 3.12
brew install python@3.12

# Remove old virtual environment
rm -rf calculations/venv

# Create new venv with Python 3.12
cd calculations
/opt/homebrew/bin/python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify Python version:**
```bash
python --version  # Should show Python 3.12.x
```

---

## PostgreSQL Issues

### Error: PostgreSQL connection refused

**Symptom:**
```
psycopg2.OperationalError: could not connect to server: Connection refused
```

**Solutions:**

**1. Start PostgreSQL service:**
```bash
# macOS with Homebrew
brew services start postgresql@14

# Check if running
brew services list | grep postgresql
```

**2. Create database:**
```bash
createdb jyotish
```

**3. Check connection:**
```bash
psql -d jyotish -c "SELECT version();"
```

### PostgreSQL not found

**Install PostgreSQL 14:**
```bash
brew install postgresql@14
brew services start postgresql@14
```

---

## Swiss Ephemeris Issues

### Error: Ephemeris files not found

**Symptom:**
```
SwissEphException: ephemeris file not found
```

**Solution:** Download ephemeris data files

```bash
mkdir -p calculations/ephemeris_data
cd calculations/ephemeris_data

# Download required files (using HTTPS - faster than FTP)
wget https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1
wget https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/semo_18.se1
wget https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1
wget https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sefstars.txt
```

Or use curl if wget not available:
```bash
curl -LO https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1
curl -LO https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/semo_18.se1
curl -LO https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1
curl -LO https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sefstars.txt
```

**Verify files exist:**
```bash
ls -lh calculations/ephemeris_data/*.se1
```

---

## MCP Server Issues

### MCP Server Not Finding Python Scripts

**Symptom:**
```
Error in logs: can't open file '//calculations/chart_calculator.py'
Python: can't open file: [Errno 2] No such file or directory
```

**Cause:** Path resolution issue in MCP server

**Solution:**
1. Verify calculation scripts exist:
   ```bash
   ls -la calculations/*.py
   ```

2. Check MCP server logs:
   ```bash
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```

3. Test Python scripts directly:
   ```bash
   cd calculations
   source venv/bin/activate
   python chart_calculator.py '{"datetime":"1990-06-15T14:30:00Z","latitude":40.7128,"longitude":-74.0060,"timezone":"America/New_York","action":"create"}'
   ```

4. Rebuild MCP server:
   ```bash
   cd mcp-server
   npm run build
   ```

**Note:** The latest version uses proper path resolution from the script location, not `process.cwd()`.

### Claude Desktop doesn't see MCP server

**Check configuration file location:**

**macOS:**
```bash
# Configuration file location
~/Library/Application\ Support/Claude/claude_desktop_config.json

# View current config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Verify configuration:**
```json
{
  "mcpServers": {
    "jyotish": {
      "command": "node",
      "args": ["/absolute/path/to/jyotish-mcp/mcp-server/dist/index.js"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/jyotish",
        "EPHEMERIS_PATH": "/absolute/path/to/jyotish-mcp/calculations/ephemeris_data"
      }
    }
  }
}
```

**Important:** Use absolute paths, not relative!

**Test MCP server manually:**
```bash
cd mcp-server
node dist/index.js
# Should start without errors
```

### MCP server not building

**Error:** `Cannot find module '@modelcontextprotocol/sdk'` or peer dependency warnings

**Solution:**
```bash
cd mcp-server
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npm run build
```

**Why `--legacy-peer-deps`?** 
Some MCP SDK dependencies may have peer dependency conflicts. This flag allows npm to proceed with installation despite warnings.

---

## Node.js Issues

### Wrong Node version

**Check version:**
```bash
node --version  # Need 18+
```

**Update Node.js:**
```bash
# macOS
brew install node

# Or use nvm
nvm install 18
nvm use 18
```

---

## Git Issues

### Remote already exists

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/jyotish-mcp.git
```

### Permission denied (publickey)

**Use HTTPS instead of SSH:**
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/jyotish-mcp.git
```

**Or set up SSH key:**
```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub
# Copy public key
cat ~/.ssh/id_ed25519.pub

# Go to GitHub Settings → SSH Keys → Add new key
```

---

## Import Errors

### ModuleNotFoundError

**Symptom:**
```python
ModuleNotFoundError: No module named 'swisseph'
```

**Solution:**
```bash
# Make sure virtual environment is activated
source calculations/venv/bin/activate

# Reinstall dependencies
pip install -r calculations/requirements.txt

# Verify installation
python -c "import swisseph; print(swisseph.__version__)"
```

---

## Path Issues

### Command not found: python3.12

**macOS with Homebrew:**
```bash
# Add Homebrew to PATH
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
which python3.12
```

### Command not found: createdb

**PostgreSQL not in PATH:**
```bash
# Add PostgreSQL to PATH (macOS)
echo 'export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## Performance Issues

### Slow ephemeris calculations

**Solution:** Ensure ephemeris files are downloaded (see above)

**Cache calculations:**
The system is designed to cache calculations in PostgreSQL for repeated queries.

---

## Testing Issues

### Tests fail with database errors

**Create test database:**
```bash
createdb jyotish_test
export DATABASE_URL="postgresql://localhost/jyotish_test"
```

### Tests fail with ephemeris errors

**Set ephemeris path:**
```bash
export EPHEMERIS_PATH="$(pwd)/calculations/ephemeris_data"
```

---

## Still Having Issues?

1. **Check logs:**
   - Claude Desktop logs: `~/Library/Logs/Claude/`
   - MCP server: Run manually to see errors

2. **Verify all prerequisites:**
   ```bash
   python3.12 --version
   node --version
   psql --version
   ```

3. **Clean install:**
   ```bash
   # Remove everything
   rm -rf calculations/venv
   rm -rf mcp-server/node_modules
   rm -rf mcp-server/dist
   
   # Run setup again
   ./scripts/setup.sh
   ```

4. **Create GitHub issue:**
   - Include error messages
   - Include system info (OS, versions)
   - Include steps to reproduce

---

## System Info

**Get your system info for bug reports:**

```bash
echo "=== System Info ==="
echo "OS: $(uname -s)"
echo "Python: $(python3 --version 2>&1)"
echo "Python 3.12: $(/opt/homebrew/bin/python3.12 --version 2>&1 || echo 'Not found')"
echo "Node: $(node --version 2>&1 || echo 'Not found')"
echo "PostgreSQL: $(psql --version 2>&1 || echo 'Not found')"
echo "Git: $(git --version 2>&1 || echo 'Not found')"
```

---

**If none of these solve your issue, please create a GitHub issue with details!**
