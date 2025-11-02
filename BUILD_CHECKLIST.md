# Build Checklist

Quick reference for building and running Jyotish MCP.

---

## ✅ Prerequisites (DONE)

- [x] Python 3.12 installed
- [x] PostgreSQL 14 installed
- [x] Virtual environment created
- [x] Python dependencies installed
- [x] Repository updated

---

## 📋 Next Steps

### Phase 1: MCP Server Setup

- [ ] Install Node dependencies: `cd mcp-server && npm install`
- [ ] Build TypeScript: `npm run build`
- [ ] Verify build: `ls dist/index.js`

### Phase 2: Database Setup

- [ ] Start PostgreSQL: `brew services start postgresql@14`
- [ ] Create database: `createdb jyotish`
- [ ] Test connection: `psql -d jyotish -c "SELECT version();"`

### Phase 3: Ephemeris Data

- [ ] Download sepl_18.se1 (planetary ephemeris)
- [ ] Download semo_18.se1 (moon ephemeris)
- [ ] Download seas_18.se1 (asteroid ephemeris)
- [ ] Verify files in: `calculations/ephemeris_data/`

### Phase 4: Claude Integration

- [ ] Get absolute project path: `pwd`
- [ ] Edit Claude config: `~/Library/Application Support/Claude/claude_desktop_config.json`
- [ ] Add MCP server configuration (use absolute paths!)
- [ ] Restart Claude Desktop
- [ ] Test: Ask Claude to list jyotish tools

### Phase 5: GitHub Push

- [ ] Review changes: `git status`
- [ ] Push updates: `git push origin main`
- [ ] Verify on GitHub: https://github.com/schwentker/jyotish-mcp

---

## 🧪 Testing

Once MCP server is connected:

```
Test 1: List tools
"What jyotish MCP tools are available?"

Test 2: Calculate chart (will fail - calculations not built yet)
"Calculate chart for Sep 27, 1953, 9:10 AM, Amritapuri, India"
```

Expected: Tools list works, calculations fail (need to build calculation engine)

---

## 🔨 Next Build Phase

After MCP server works, build calculation engine:

1. [ ] Create `calculations/ephemeris.py`
2. [ ] Create `calculations/chart_calculator.py`
3. [ ] Create `calculations/nakshatras.py`
4. [ ] Create `calculations/dashas.py`
5. [ ] Create `calculations/database.py`
6. [ ] Create `calculations/houses.py`
7. [ ] Write tests
8. [ ] End-to-end integration test

---

## 📝 Commands Quick Reference

```bash
# Build MCP server
cd mcp-server && npm install && npm run build

# Start PostgreSQL
brew services start postgresql@14

# Create database
createdb jyotish

# Download ephemeris (in calculations/ephemeris_data/)
wget ftp://ftp.astro.com/pub/swisseph/ephe/sepl_18.se1
wget ftp://ftp.astro.com/pub/swisseph/ephe/semo_18.se1
wget ftp://ftp.astro.com/pub/swisseph/ephe/seas_18.se1

# Test MCP server
node mcp-server/dist/index.js

# Push to GitHub
git push origin main
```

---

## 🆘 If Stuck

See:
- [NEXT_STEPS.md](NEXT_STEPS.md) - Detailed instructions
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [QUICK_START.md](QUICK_START.md) - Full setup guide

---

**Current Status:** Ready to build MCP server → Test integration → Build calculations

**Track progress by checking off items above!** ✓
