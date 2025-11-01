# Quick Start Guide

Get the Jyotish MCP server running in 15 minutes.

---

## Prerequisites

Install these first:

```bash
# Python 3.11+
python3 --version

# Node.js 18+
node --version

# PostgreSQL 15+
psql --version

# Git
git --version
```

---

## Setup Steps

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/jyotish-mcp.git
cd jyotish-mcp
```

### 2. Setup Python Environment

```bash
cd calculations

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download Swiss Ephemeris data files
mkdir -p ephemeris_data
cd ephemeris_data
wget ftp://ftp.astro.com/pub/swisseph/ephe/sepl_18.se1
wget ftp://ftp.astro.com/pub/swisseph/ephe/semo_18.se1
wget ftp://ftp.astro.com/pub/swisseph/ephe/seas_18.se1
cd ..
```

### 3. Setup Database

```bash
# Create database
createdb jyotish

# Set environment variable
export DATABASE_URL="postgresql://localhost/jyotish"

# Run migrations (once available)
# python migrations/run_migrations.py
```

### 4. Setup MCP Server

```bash
cd ../mcp-server

# Install dependencies
npm install

# Build TypeScript
npm run build
```

### 5. Configure Claude Desktop

Add to your Claude Desktop MCP settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "jyotish": {
      "command": "node",
      "args": ["/path/to/jyotish-mcp/mcp-server/dist/index.js"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/jyotish",
        "EPHEMERIS_PATH": "/path/to/jyotish-mcp/calculations/ephemeris_data"
      }
    }
  }
}
```

### 6. Test It

Restart Claude Desktop, then try:

```
You: "Calculate a birth chart for September 27, 1953, 9:10 AM 
     in Amritapuri, India (9°08'N, 76°48'E)"

Claude: [Should call chart_create tool and return results]
```

---

## Development Workflow

### Running Tests

```bash
# Python tests
cd calculations
pytest -v

# With coverage
pytest --cov=. --cov-report=html
```

### Watching for Changes

```bash
# MCP server (auto-rebuild on changes)
cd mcp-server
npm run watch
```

### Code Formatting

```bash
# Python
cd calculations
black .
ruff check .

# TypeScript
cd mcp-server
npm run format
npm run lint
```

---

## Troubleshooting

### Swiss Ephemeris files not found

```bash
# Verify files exist
ls calculations/ephemeris_data/*.se1

# If missing, download manually:
cd calculations/ephemeris_data
# Download from: https://www.astro.com/ftp/swisseph/ephe/
```

### PostgreSQL connection error

```bash
# Check PostgreSQL is running
pg_isready

# Check database exists
psql -l | grep jyotish

# Recreate if needed
dropdb jyotish
createdb jyotish
```

### MCP server not appearing in Claude

1. Check config file path is correct
2. Verify node can execute: `node /path/to/dist/index.js`
3. Check Claude Desktop logs: `~/Library/Logs/Claude/`
4. Restart Claude Desktop completely

### Python import errors

```bash
# Ensure virtual environment active
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Quick Test

Test calculation engine directly:

```bash
cd calculations
python3 << EOF
import swisseph as swe
swe.set_ephe_path('./ephemeris_data')
swe.set_sid_mode(swe.SIDM_LAHIRI)
jd = swe.julday(1953, 9, 27, 9.169)  # 9:10 AM
sun = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0]
print(f"Sun at {sun:.2f}° sidereal")
EOF
```

Expected output: Sun at ~169-171° (Virgo)

---

## Next Steps

1. Read [README.md](README.md) for full architecture
2. Check [PROJECT_STATUS.md](PROJECT_STATUS.md) for current progress
3. See [prompts/astrologer_system.md](prompts/astrologer_system.md) for interpretation guidelines
4. Join discussions to contribute

---

## Getting Help

- **Issues:** GitHub Issues for bugs
- **Discussions:** GitHub Discussions for questions
- **Documentation:** Check `/docs` folder
- **System Prompt:** Read `prompts/astrologer_system.md`

---

**You're ready to contribute! 🚀**
