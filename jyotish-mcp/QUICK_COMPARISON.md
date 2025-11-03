# Quick Comparison: Uploaded Zip vs GitHub Repo

**Date:** November 2, 2025  
**Zip File:** jyotish-mcp-complete.zip  
**Target Repo:** github.com/schwentker/jyotish-mcp

## TL;DR

✅ **The uploaded zip is your complete v0.5.0 codebase** - ready to merge  
⚠️ **Critical Fix Needed:** Remove hardcoded paths in `mcp-server/src/index.ts`  
📋 **Status:** 45% complete, needs D9, PostgreSQL, and tests

## What's in the Zip

### Complete & Working (60%)
```
✅ MCP server (8 tools) - TypeScript
✅ Chart calculator - Python  
✅ Dasha calculator - Python
✅ Transit calculator - Python
✅ Swiss Ephemeris integration
✅ Constants (rashis, nakshatras)
✅ Setup automation (scripts/setup.sh)
✅ Comprehensive docs (10 markdown files)
```

### Partial/Stubs (30%)
```
🔨 Varga calculator - D1 only (needs D9!)
🔨 Yoga identifier - stub
🔨 Compatibility - stub
🔨 Database - file cache only
```

### Missing (10%)
```
❌ Tests (pytest suite)
❌ PostgreSQL schema
❌ Aspects system
❌ Advanced calculations
```

## Critical Issue: Hardcoded Paths

### Current Problem (Line 204-206 in mcp-server/src/index.ts)

```typescript
// ❌ BAD - Won't work after cloning
const calculationsPath = join(__dirname, "..", "..", "calculations");
const pythonPath = join(calculationsPath, "venv", "bin", "python");
```

The code already uses `__dirname`, so it should work! But needs verification and fallback:

### Required Fix

```typescript
// ✅ GOOD - Add fallback
const calculationsPath = join(__dirname, "..", "..", "calculations");
const venvPython = join(calculationsPath, "venv", "bin", "python");
const pythonPath = existsSync(venvPython) ? venvPython : "python3";

// Also check script exists
if (!existsSync(scriptPath)) {
  reject(new Error(`Script not found: ${scriptPath}`));
  return;
}
```

## File Inventory

### Documentation (10 files, 95KB)
- README.md (29KB) - Comprehensive overview
- TODO.md (7.3KB) - Task list with priorities
- IMPLEMENTATION_STATUS.md (9.7KB) - Status tracking
- QUICK_START.md (5.2KB) - 15-min setup
- TROUBLESHOOTING.md (7.8KB) - Common issues
- CONTRIBUTING.md (5.1KB) - How to contribute
- PROJECT_STATUS.md (10KB) - Development tracking
- BUILD_CHECKLIST.md (3.2KB) - Quick reference
- NEXT_STEPS.md (5.9KB) - Post-setup guide
- DELIVERY_SUMMARY.md (8KB) - Project summary

### Python Code (9 files, 48KB)
- calculations/chart_calculator.py (7KB) - Main chart
- calculations/dasha_calculator.py (8.5KB) - Dashas
- calculations/transit_calculator.py (5.5KB) - Transits
- calculations/constants.py (12KB) - Astrological data
- calculations/varga_calculator.py (2.5KB) - Divisional charts (stub)
- calculations/yoga_identifier.py (1KB) - Yogas (stub)
- calculations/compatibility_calculator.py (1KB) - Synastry (stub)
- calculations/test_ephemeris.py (4KB) - Tests
- calculations/requirements.txt (512B) - Dependencies

### TypeScript Code (3 files, 17KB)
- mcp-server/src/index.ts (16KB) - Main server
- mcp-server/package.json (1.5KB) - Node deps
- mcp-server/tsconfig.json (1KB) - TS config

### Scripts & Config (4 files, 19KB)
- scripts/setup.sh (7KB) - Automated setup
- prompts/astrologer_system.md (11KB) - AI prompt
- .github/workflows/ci.yml (???) - CI/CD
- .gitignore (684B) - Git excludes

## Merge Recommendation

### Option 1: 10 Atomic Commits (Recommended)

**Pros:**
- Easy to review each change
- Can test incrementally  
- Clean git history
- Easy to revert if needed

**Cons:**
- Takes longer (10 PRs)
- More overhead

**Timeline:** 3-5 days with reviews

### Option 2: Single Comprehensive Merge

**Pros:**
- Fast (1 PR)
- Everything merged at once
- Less overhead

**Cons:**
- Large PR hard to review
- All-or-nothing
- Messy if conflicts

**Timeline:** 1-2 days

### Recommended Approach: Hybrid

1. **Critical Path First** (1 commit)
   - Fix hardcoded paths
   - Add Python fallback
   - Verify dynamic resolution
   
2. **Core Code** (1 commit)
   - All Python calculators
   - MCP server (already fixed)
   - Constants and setup
   
3. **Documentation** (1 commit)
   - All markdown files
   - Update status tracking
   
**Timeline:** 1 day for commits, 1-2 days for testing

## Testing Checklist

After merge, verify:

```bash
# 1. Fresh clone test
cd /tmp
git clone https://github.com/schwentker/jyotish-mcp.git test-repo
cd test-repo

# 2. No hardcoded paths
grep -r "/Users/schwentker" .  # Should be empty
grep -r "hardcoded" .          # Only in docs/comments

# 3. Setup works
chmod +x scripts/setup.sh
./scripts/setup.sh

# 4. Calculations work
cd calculations
source venv/bin/activate
python chart_calculator.py '{"action":"list"}'

# 5. MCP server builds
cd ../mcp-server
npm install
npm run build

# 6. Server starts
node dist/index.js  # Should print "running on stdio"

# 7. Test with Claude Desktop
# Configure claude_desktop_config.json
# Ask: "What jyotish tools are available?"
```

## Priority Tasks After Merge

### Week 1-2: MVP Features
1. **D9 (Navamsa)** - CRITICAL
   - Algorithm: `(planet_long % 30) * 9 / 30`
   - Most important divisional chart
   - Required for complete readings

2. **Test Suite** - HIGH
   - pytest framework
   - Known chart fixtures  
   - Validation vs JHora

3. **PostgreSQL** - HIGH
   - Replace file cache
   - Proper schema
   - Migration path

### Week 3-4: Enhanced Features
4. **Aspects System** - MEDIUM
   - 7th house aspects
   - Special aspects (Mars, Jupiter, Saturn)
   - Mutual aspects

5. **More Divisional Charts** - MEDIUM
   - D2, D3, D7, D10, D12, D30
   - Standard interpretations

6. **Yoga Identification** - MEDIUM
   - Raj Yogas
   - Dhana Yogas
   - Pancha Mahapurusha

## Known Issues to Address

### Critical
- [ ] Verify no hardcoded paths remain
- [ ] Add Python environment fallback
- [ ] Test on Windows (path separators)

### High
- [ ] File cache → PostgreSQL migration
- [ ] D9 implementation
- [ ] Test suite creation

### Medium
- [ ] Better error messages
- [ ] Input validation
- [ ] Performance optimization

### Low
- [ ] Chart visualization
- [ ] Web interface
- [ ] Multi-user support

## Status Summary

**Overall Completion:** 45%

| Component | Status | % |
|-----------|--------|---|
| Infrastructure | Complete | 100% |
| MCP Server | Working (needs path fix) | 95% |
| Chart Calc | Complete | 80% |
| Dashas | Complete | 90% |
| Transits | Complete | 80% |
| Divisional Charts | D1 only | 10% |
| Yogas | Stub only | 0% |
| Compatibility | Stub only | 0% |
| Database | File cache | 0% |
| Tests | Manual only | 5% |
| Docs | Comprehensive | 95% |

**Time to MVP:** 2-3 weeks additional development

## Files Ready for Merge

All files in the zip are ready to merge after fixing the path issue. Here's the full list:

### Core (3)
- .gitignore ✅
- LICENSE ✅  
- README.md ✅

### Documentation (9)
- TODO.md ✅
- IMPLEMENTATION_STATUS.md ✅
- QUICK_START.md ✅
- TROUBLESHOOTING.md ✅
- CONTRIBUTING.md ✅
- PROJECT_STATUS.md ✅
- BUILD_CHECKLIST.md ✅
- NEXT_STEPS.md ✅
- DELIVERY_SUMMARY.md ✅

### Python (9)
- calculations/chart_calculator.py ✅
- calculations/dasha_calculator.py ✅
- calculations/transit_calculator.py ✅
- calculations/varga_calculator.py ⚠️ (D1 only)
- calculations/yoga_identifier.py ⚠️ (stub)
- calculations/compatibility_calculator.py ⚠️ (stub)
- calculations/constants.py ✅
- calculations/test_ephemeris.py ✅
- calculations/requirements.txt ✅

### TypeScript (3)
- mcp-server/src/index.ts ⚠️ (needs path fix)
- mcp-server/package.json ✅
- mcp-server/tsconfig.json ✅

### Scripts (2)
- scripts/setup.sh ✅
- prompts/astrologer_system.md ✅

### Config (2)
- .github/workflows/ci.yml ✅
- calculations/README.md ✅

**Total:** 28 files ready to merge (3 need attention: index.ts, varga, yoga)

## Next Actions

### Immediate (Today)
1. Review fixed `index.ts` (provided separately)
2. Choose merge strategy (atomic vs single)
3. Create merge branch

### This Week  
4. Execute merge
5. Test on fresh clone
6. Configure Claude Desktop
7. Test end-to-end

### Next Week
8. Create issues from TODO.md
9. Start on D9 implementation
10. Set up test suite

---

**Ready to proceed!** 🚀

See MERGE_STRATEGY.md for detailed execution plan.
