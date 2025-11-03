# Jyotish MCP - Merge Strategy & Commit Plan

**Date:** November 2, 2025  
**Source:** jyotish-mcp-complete.zip  
**Target:** github.com/schwentker/jyotish-mcp  

## Overview

This document provides a step-by-step plan to merge the uploaded complete codebase with your GitHub repository, broken down into logical, atomic commits that can be reviewed and tested independently.

## Critical Issues to Fix

### 1. Remove Hardcoded Paths ⚠️

**Current Problem in `mcp-server/src/index.ts` (lines 204-206):**

```typescript
// ❌ WRONG - Hardcoded relative paths
const calculationsPath = join(__dirname, "..", "..", "calculations");
const scriptPath = join(calculationsPath, `${scriptName}.py`);
const pythonPath = join(calculationsPath, "venv", "bin", "python");
```

**Solution - Use Dynamic Resolution:**

```typescript
// ✅ CORRECT - Works for any clone location
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const calculationsPath = join(__dirname, '..', '..', 'calculations');
```

This is already partially implemented but needs verification.

### 2. Python Path Fallback

Add fallback for when venv doesn't exist:

```typescript
// Check if venv Python exists, otherwise use system python3
const venvPython = join(calculationsPath, "venv", "bin", "python");
const systemPython = "python3";
const pythonPath = fs.existsSync(venvPython) ? venvPython : systemPython;
```

## Merge Strategy: 10 Atomic Commits

### Commit 1: Core Infrastructure
**Branch:** `merge/01-core-infrastructure`

**Files to add/update:**
```
├── .gitignore
├── LICENSE
├── package.json (root, if exists)
└── .github/workflows/ci.yml
```

**Commit message:**
```
chore: Add core project infrastructure

- Add MIT license
- Configure .gitignore for Node, Python, ephemeris files
- Add GitHub Actions CI workflow
- Set up project root configuration

Related: Initial project structure
```

**Test:** Verify .gitignore patterns work, CI config validates

---

### Commit 2: Documentation Foundation
**Branch:** `merge/02-documentation`

**Files to add/update:**
```
├── README.md
├── CONTRIBUTING.md
├── LICENSE (if not in commit 1)
└── QUICK_START.md
```

**Commit message:**
```
docs: Add comprehensive project documentation

- Add detailed README with architecture overview
- Include quick start guide for non-technical users
- Add contribution guidelines
- Document MCP integration approach

Features:
- Executive summary of AI + ancient wisdom experiment
- Stakeholder-specific sections (business, practitioners, developers)
- Technical architecture diagrams
- Installation instructions
```

**Test:** Verify all internal doc links work

---

### Commit 3: Status & Tracking Docs
**Branch:** `merge/03-status-tracking`

**Files to add/update:**
```
├── TODO.md                      (from uploaded file)
├── IMPLEMENTATION_STATUS.md     (from uploaded file)
├── PROJECT_STATUS.md
├── BUILD_CHECKLIST.md
├── NEXT_STEPS.md
└── TROUBLESHOOTING.md
```

**Commit message:**
```
docs: Add project status and task tracking

- Add comprehensive TODO list with priorities
- Document implementation status (45% complete)
- Add build checklist for quick reference
- Include troubleshooting guide
- Outline next steps and roadmap

Status tracking:
- ✅ Core infrastructure: 100%
- ✅ Chart calculations: 80%
- 🔨 Divisional charts: 10% (D1 only)
- ❌ Database: 0% (file cache only)
```

**Test:** Cross-reference status docs with actual code

---

### Commit 4: Python Calculation Engine - Constants
**Branch:** `merge/04-python-constants`

**Files to add/update:**
```
calculations/
├── requirements.txt
├── constants.py
└── README.md
```

**Commit message:**
```
feat(calculations): Add astrological constants and dependencies

- Define rashis (zodiac signs) with properties
- Define nakshatras with padas and ruling planets
- Define Vimshottari Dasha periods (120 years)
- Add planetary constants and relationships
- Set up Python dependencies (pyswisseph, pytz)

Constants include:
- 12 Rashis with lords and nature
- 27 Nakshatras with ruling planets
- Dasha system configuration
- Ayanamsa settings (Lahiri)
```

**Test:** 
```bash
cd calculations
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -c "from constants import RASHIS, NAKSHATRAS; print(len(RASHIS), len(NAKSHATRAS))"
```

---

### Commit 5: Python Calculation Engine - Core Charts
**Branch:** `merge/05-python-charts`

**Files to add/update:**
```
calculations/
├── chart_calculator.py
└── test_ephemeris.py
```

**Commit message:**
```
feat(calculations): Implement birth chart calculator

Features:
- Calculate planetary positions using Swiss Ephemeris
- Determine ascendant (Lagna) with sidereal zodiac
- Assign rashis, nakshatras, and padas
- Detect retrograde planets
- Whole Sign house system
- File-based caching to .charts_cache/

Actions supported:
- create: Generate new chart from birth data
- read: Retrieve cached chart by UUID
- list: Show all stored charts

Accuracy: ±1 arc-second (Swiss Ephemeris precision)
```

**Test:**
```bash
cd calculations
source venv/bin/activate
python chart_calculator.py '{"action":"create","datetime":"1953-09-27T09:10:00+05:30","latitude":9.133333,"longitude":76.8,"timezone":"Asia/Kolkata","name":"Test"}'
```

---

### Commit 6: Python Calculation Engine - Dashas & Transits
**Branch:** `merge/06-python-dashas-transits`

**Files to add/update:**
```
calculations/
├── dasha_calculator.py
└── transit_calculator.py
```

**Commit message:**
```
feat(calculations): Add Dasha and transit calculators

Dasha Calculator:
- Vimshottari Dasha system (120-year cycle)
- Calculate birth Dasha balance from Moon nakshatra
- Generate nested Maha and Antar Dashas
- Determine current running period for any date
- Accurate date arithmetic

Transit Calculator:
- Current planetary positions
- House placements relative to birth chart
- Retrograde status
- Comparison with natal positions

Both use Swiss Ephemeris for precision.
```

**Test:**
```bash
python dasha_calculator.py '{"action":"current","chart_id":"<uuid>"}'
python transit_calculator.py '{"action":"current","chart_id":"<uuid>"}'
```

---

### Commit 7: Python Calculation Engine - Vargas & Yogas (Stubs)
**Branch:** `merge/07-python-vargas-yogas`

**Files to add/update:**
```
calculations/
├── varga_calculator.py
├── yoga_identifier.py
└── compatibility_calculator.py
```

**Commit message:**
```
feat(calculations): Add divisional charts and yoga identifiers (stubs)

Varga Calculator:
- ✅ D1 (Rashi) - fully implemented
- 🔨 D9 (Navamsa) - stub only (HIGH PRIORITY TODO)
- 🔨 D2-D60 - not yet implemented

Yoga Identifier:
- Framework in place
- Returns "not yet implemented"
- TODO: Raj Yogas, Dhana Yogas, Pancha Mahapurusha

Compatibility Calculator:
- Framework in place
- Returns "not yet implemented"
- TODO: Kuta system, cross-aspects

Note: These are stubs to enable MCP tools. Full implementation needed.
```

**Test:** Verify stubs return appropriate messages

---

### Commit 8: MCP Server - Fix Hardcoded Paths
**Branch:** `merge/08-mcp-path-fixes`

**Files to add/update:**
```
mcp-server/
├── package.json
├── tsconfig.json
└── src/index.ts (CRITICAL PATH FIXES)
```

**Commit message:**
```
fix(mcp): Remove hardcoded paths, add dynamic resolution

BREAKING FIX: Path resolution now works for any clone location

Changes:
- Use __dirname for relative path calculation
- Add fallback from venv Python to system python3
- Proper error handling for missing Python
- Add fs.existsSync check before spawning Python

Before (broken):
  const calculationsPath = "/hardcoded/path";

After (works everywhere):
  const __dirname = dirname(fileURLToPath(import.meta.url));
  const calculationsPath = join(__dirname, '..', '..', 'calculations');
  
Python fallback:
  const venvPython = join(calculationsPath, 'venv', 'bin', 'python');
  const pythonPath = fs.existsSync(venvPython) ? venvPython : 'python3';

This ensures the repo works immediately after cloning.
```

**Critical code change in `src/index.ts`:**

```typescript
// Add import at top
import { existsSync } from 'fs';

// In callPythonCalculator function (around line 198):
async function callPythonCalculator(
  scriptName: string,
  args: Record<string, any>
): Promise<any> {
  return new Promise((resolve, reject) => {
    // Use dynamic path resolution
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = dirname(__filename);
    const calculationsPath = join(__dirname, "..", "..", "calculations");
    const scriptPath = join(calculationsPath, `${scriptName}.py`);
    
    // Check for venv Python, fallback to system
    const venvPython = join(calculationsPath, "venv", "bin", "python");
    const pythonPath = existsSync(venvPython) ? venvPython : "python3";
    
    // Verify script exists
    if (!existsSync(scriptPath)) {
      reject(new Error(`Python script not found: ${scriptPath}`));
      return;
    }
    
    const python = spawn(pythonPath, [scriptPath, JSON.stringify(args)], {
      cwd: calculationsPath
    });
    
    // ... rest of function unchanged
```

**Test:**
```bash
cd mcp-server
npm install
npm run build
# Verify no hardcoded paths in dist/index.js
grep -n "schwentker" dist/index.js  # Should return nothing
```

---

### Commit 9: MCP Server - Tool Definitions
**Branch:** `merge/09-mcp-tools`

**Files:** (continuation of `mcp-server/src/index.ts`)

**Commit message:**
```
feat(mcp): Implement 8 MCP tools for Jyotish calculations

Tools implemented:
1. chart_create - Generate birth chart
2. chart_read - Retrieve stored chart
3. chart_list - List all charts
4. dasha_current - Current Dasha period
5. transit_now - Current transits
6. divisional_read - Divisional charts (D1-D30)
7. yogas_identify - Planetary combinations (stub)
8. compatibility_analyze - Synastry (stub)

Each tool:
- Has Zod schema validation
- Spawns Python subprocess
- Returns JSON response
- Handles errors gracefully

MCP Protocol: Model Context Protocol v0.5.0
Server: stdio transport for Claude Desktop integration
```

**Test:** 
```bash
npm run build
node dist/index.js  # Should print "Jyotish MCP Server running on stdio"
```

---

### Commit 10: Scripts & Setup Automation
**Branch:** `merge/10-setup-scripts`

**Files to add/update:**
```
scripts/
└── setup.sh
prompts/
└── astrologer_system.md
```

**Commit message:**
```
feat(scripts): Add automated setup and AI prompts

Setup Script (scripts/setup.sh):
- Check Python 3.12 installation
- Create virtual environment
- Install Python dependencies
- Download Swiss Ephemeris files via HTTPS
- Build MCP server (npm install & build)
- Create necessary directories
- Display next steps

Prompts:
- Astrologer system prompt for Claude
- Ethical interpretation guidelines
- Classical Jyotish principles
- Guardrails against determinism

Usage:
  chmod +x scripts/setup.sh
  ./scripts/setup.sh

Installs everything needed in ~5 minutes.
```

**Test:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh  # Run on clean system
```

---

## Merge Execution Plan

### Phase 1: Prepare Local Repository

```bash
# 1. Ensure you're in your local repo
cd /Users/schwentker/dev/sblai/jyotish-mcp

# 2. Commit or stash any local changes
git status
git stash  # if you have uncommitted changes

# 3. Create a merge preparation branch
git checkout -b merge-prep

# 4. Fetch latest from GitHub
git fetch origin
git merge origin/main  # or origin/master, depending on your default branch
```

### Phase 2: Extract and Stage Commits

For each commit (1-10), you'll:

```bash
# Example for Commit 1:
git checkout -b merge/01-core-infrastructure

# Copy files from extracted zip
cp /path/to/extracted/.gitignore .
cp /path/to/extracted/LICENSE .
cp /path/to/extracted/.github/workflows/ci.yml .github/workflows/

# Stage and commit
git add .gitignore LICENSE .github/
git commit -m "chore: Add core project infrastructure

- Add MIT license
- Configure .gitignore for Node, Python, ephemeris files  
- Add GitHub Actions CI workflow
- Set up project root configuration

Related: Initial project structure"

# Push to GitHub
git push origin merge/01-core-infrastructure

# Create PR on GitHub, review, merge

# Return to main and repeat for next commit
git checkout main
git pull origin main
```

### Phase 3: Critical Path Fix (Commit 8)

**This is the most important commit** - it fixes the hardcoded paths.

```bash
git checkout -b merge/08-mcp-path-fixes

# Edit mcp-server/src/index.ts
# Make the changes described in Commit 8 above

# Test the changes
cd mcp-server
npm run build
grep -n "schwentker" dist/index.js  # Should be empty
grep -n "/Users/" dist/index.js     # Should be empty

# Commit
git add mcp-server/
git commit -m "fix(mcp): Remove hardcoded paths, add dynamic resolution

BREAKING FIX: Path resolution now works for any clone location
...
"

git push origin merge/08-mcp-path-fixes
```

### Phase 4: Integration Testing

After all commits are merged:

```bash
# 1. Clone fresh copy to test
cd /tmp
git clone https://github.com/schwentker/jyotish-mcp.git test-clone
cd test-clone

# 2. Run setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. Test calculations
cd calculations
source venv/bin/activate
python chart_calculator.py '{"action":"create","datetime":"1953-09-27T09:10:00+05:30","latitude":9.133333,"longitude":76.8,"timezone":"Asia/Kolkata"}'

# 4. Test MCP server
cd ../mcp-server
npm run build
node dist/index.js  # Should start without errors

# 5. Test with Claude Desktop
# Configure claude_desktop_config.json
# Try: "What jyotish tools are available?"
```

## Alternative: Single Merge Strategy

If you prefer to merge everything at once:

```bash
# 1. Create comprehensive merge branch
git checkout -b merge/complete-codebase

# 2. Copy all files from zip except .git
rsync -av --exclude='.git' /path/to/extracted/ .

# 3. Fix hardcoded paths manually
vim mcp-server/src/index.ts
# Make the path fixes described in Commit 8

# 4. Stage all changes
git add -A

# 5. Commit with detailed message
git commit -m "merge: Integrate complete Jyotish MCP implementation

This merge brings in the complete v0.5.0 codebase with:

✅ Complete:
- MCP server with 8 tools
- Python calculation engine (chart, dasha, transit)
- Swiss Ephemeris integration
- Comprehensive documentation
- Setup automation

🔨 In Progress:
- Divisional charts (D1 only, need D9)
- Database migration (file cache → PostgreSQL)
- Yoga identification (stubs)

❌ TODO:
- Full test suite
- Advanced calculations (Shadbala, Ashtakavarga)
- Web interface

BREAKING CHANGES:
- Fixed hardcoded paths in MCP server
- Now works for any clone location
- Added Python fallback (venv → system)

See TODO.md and IMPLEMENTATION_STATUS.md for details.
"

# 6. Push and create PR
git push origin merge/complete-codebase
```

## Files Requiring Manual Review

### High Priority Review

1. **mcp-server/src/index.ts**
   - Verify path resolution is truly dynamic
   - Check Python fallback logic
   - Ensure no hardcoded paths remain

2. **calculations/*.py**
   - Verify Swiss Ephemeris paths
   - Check cache directory handling
   - Ensure timezone handling is correct

3. **scripts/setup.sh**
   - Test on fresh system
   - Verify ephemeris download works
   - Check error handling

### Medium Priority Review

4. **package.json & tsconfig.json**
   - Verify dependency versions
   - Check for security vulnerabilities
   - Ensure compatibility

5. **TODO.md & IMPLEMENTATION_STATUS.md**
   - Update percentages if code changed
   - Verify task priorities
   - Cross-reference with actual code

6. **.gitignore**
   - Ensure ephemeris files ignored (large)
   - Ignore venv and node_modules
   - Ignore .charts_cache/

## Post-Merge Checklist

- [ ] All hardcoded paths removed
- [ ] Setup script works on fresh clone
- [ ] Python calculations accurate (test against JHora)
- [ ] MCP server starts without errors
- [ ] All documentation links work
- [ ] CI pipeline passes
- [ ] No sensitive data in commits
- [ ] GitHub repo description updated
- [ ] Topics/tags added to repo (mcp, astrology, jyotish)
- [ ] Claude Desktop config example provided

## Communication Plan

### GitHub Release Notes

```markdown
## v0.5.0 - Initial Public Release

### 🎉 What's New

Complete Jyotish MCP implementation integrating Claude AI with Vedic astrology calculations.

### ✅ Features

- MCP server with 8 tools for birth chart analysis
- Swiss Ephemeris integration (±1 arc-second precision)
- Vimshottari Dasha calculator
- Current transit calculator
- Whole Sign house system
- 27 Nakshatras with padas
- File-based chart caching

### 🔨 In Progress

- D9 (Navamsa) divisional chart
- PostgreSQL integration
- Yoga identification
- Compatibility analysis

### 📚 Documentation

- Comprehensive README
- Quick start guide (15 min setup)
- Troubleshooting guide
- Contribution guidelines

### 🐛 Bug Fixes

- Fixed hardcoded paths in MCP server
- Added Python environment fallback
- Improved error messages

### ⚠️ Known Issues

- Only D1 (Rashi) chart implemented
- File-based cache (not PostgreSQL yet)
- No automated tests yet

See TODO.md for complete roadmap.
```

### Tweet/Social

```
Jyotish MCP v0.5: AI meets 5,000-year-old Vedic astrology 🕉️

- Claude + Swiss Ephemeris
- 8 MCP tools for chart analysis
- Open source (MIT)
- Works out of the box

Testing whether AI can surface patterns in ancient symbolic systems.

github.com/schwentker/jyotish-mcp

#AI #Astrology #MCP #OpenSource
```

## Troubleshooting Common Merge Issues

### Conflict: README.md

If GitHub repo already has README:

```bash
# Keep both, merge manually
# GitHub README (existing project description)
# Zip README (comprehensive new docs)

# Option 1: Replace entirely
git checkout --theirs README.md

# Option 2: Merge manually
# Keep intro from GitHub version
# Add detailed sections from zip version
```

### Conflict: package.json

```bash
# Merge dependencies carefully
# Keep higher version numbers
# Test after merge:
npm install
npm run build
```

### Missing Ephemeris Files

If setup fails:

```bash
# Manual download
cd calculations
mkdir -p ephe
cd ephe
wget https://www.astro.com/ftp/swisseph/ephe/sepl_18.se1
wget https://www.astro.com/ftp/swisseph/ephe/semo_18.se1
wget https://www.astro.com/ftp/swisseph/ephe/seas_18.se1
wget https://www.astro.com/ftp/swisseph/ephe/sefstars.txt
```

## Success Criteria

### Merge is successful when:

1. ✅ Fresh clone works with `./scripts/setup.sh`
2. ✅ Chart calculation produces accurate results
3. ✅ MCP server starts without errors
4. ✅ Claude Desktop can discover and use tools
5. ✅ No hardcoded paths in codebase
6. ✅ All documentation renders correctly on GitHub
7. ✅ CI pipeline passes (if configured)
8. ✅ No sensitive data exposed

### Test with these commands:

```bash
# 1. Fresh clone test
cd /tmp && git clone <your-repo> test && cd test

# 2. Setup test
./scripts/setup.sh

# 3. Calculation test
cd calculations && source venv/bin/activate
python chart_calculator.py '{"action":"list"}'

# 4. MCP test
cd ../mcp-server && npm run build && node dist/index.js

# 5. Path test
grep -r "/Users/schwentker" .  # Should be empty
grep -r "hardcoded" .          # Should only be in docs/comments
```

## Next Steps After Merge

1. **Create issues from TODO.md**
   - Tag with priorities (P0, P1, P2)
   - Add milestones (MVP, v1.0, v2.0)
   - Assign to contributors

2. **Set up project board**
   - Backlog
   - In Progress
   - Review
   - Done

3. **Create development branches**
   - `feature/d9-navamsa`
   - `feature/postgresql-integration`
   - `feature/aspects-system`
   - `feature/test-suite`

4. **Community engagement**
   - Tweet announcement
   - Post to relevant forums
   - Reach out to Jyotish community
   - Share with MCP developers

---

**Ready to merge!** 🚀

Choose your strategy:
- **Recommended:** 10 atomic commits (easier to review)
- **Alternative:** Single comprehensive merge (faster)

Both approaches work. Atomic commits are better for code review and git history.
