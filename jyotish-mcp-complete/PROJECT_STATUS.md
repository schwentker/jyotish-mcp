# Jyotish MCP Project Status

**Last Updated:** 2025-11-01  
**Phase:** Foundation (Week 1)

---

## ✅ Completed Components

### Documentation

1. **README.md** - Comprehensive project documentation
   - Executive summary for Fortune 50 leaders
   - Stakeholder-specific sections
   - Technical architecture
   - Complete Jyotish calculation standards
   - Ethical guidelines
   - Roadmap

2. **prompts/astrologer_system.md** - Master system prompt
   - Interpretation principles
   - Ethical guardrails
   - Cultural sensitivity guidelines
   - Response patterns
   - Special considerations for Her

### MCP Server (TypeScript)

3. **mcp-server/package.json** - Dependencies and scripts
4. **mcp-server/tsconfig.json** - TypeScript configuration
5. **mcp-server/src/index.ts** - Complete MCP server
   - 8 core tools defined
   - Parameter validation (Zod)
   - Python subprocess integration
   - Error handling

### Calculation Engine (Python)

6. **calculations/requirements.txt** - Python dependencies
7. **calculations/constants.py** - Complete Jyotish reference data
   - 12 rashis with lords, elements, qualities
   - 27 nakshatras with deities and lords
   - 9 planets with Swiss Ephemeris IDs
   - Vimshottari Dasha system (120-year cycle)
   - House significations
   - Aspect rules
   - Divisional chart definitions (D1-D60)
   - Exaltation/debilitation data
   - Utility functions

---

## 🔨 Next Priority: Core Calculation Modules

### Immediate Next Steps (Week 1 continued)

#### 1. Swiss Ephemeris Integration
**File:** `calculations/ephemeris.py`

```python
Key functions needed:
- init_ephemeris() - Set path and ayanamsa
- get_planet_position(jd, planet) -> longitude, latitude, speed
- get_ascendant(jd, lat, lon) -> ascendant_longitude
- is_retrograde(speed) -> bool
- julian_day(datetime, timezone) -> jd
```

**Status:** Not started  
**Priority:** CRITICAL - Foundation for all calculations

#### 2. Nakshatra Calculator
**File:** `calculations/nakshatras.py`

```python
Key functions needed:
- get_nakshatra(longitude) -> (name, pada, lord)
- get_dasha_balance(moon_longitude) -> (planet, years, months, days)
```

**Status:** Utility functions in constants.py, needs module  
**Priority:** HIGH - Needed for Dasha calculations

#### 3. House System
**File:** `calculations/houses.py`

```python
Key functions needed:
- calculate_houses(ascendant_long) -> dict of 12 house cusps
- get_planet_house(planet_long, asc_long) -> house_number
```

**Status:** Utility function in constants.py, needs module  
**Priority:** HIGH - Core interpretation element

#### 4. Dasha Calculator
**File:** `calculations/dashas.py`

```python
Key functions needed:
- calculate_vimshottari(moon_long, birth_jd) -> full dasha tree
- get_current_dasha(dasha_tree, target_jd) -> Maha/Antar/Pratyantar
- dasha_to_json(dasha_tree) -> JSONB format
```

**Status:** Constants defined, needs implementation  
**Priority:** HIGH - Critical timing system

#### 5. Divisional Charts
**File:** `calculations/vargas.py`

```python
Key functions needed:
- calculate_navamsa(longitude) -> D9 longitude
- calculate_varga(longitude, division) -> Dx longitude
- get_all_divisional_positions(planets, division) -> dict
```

**Status:** Not started  
**Priority:** MEDIUM - D9 essential, others can wait

#### 6. Aspect System
**File:** `calculations/aspects.py`

```python
Key functions needed:
- get_aspects(planet_positions, houses) -> list of aspects
- check_aspect(planet1, planet2, houses) -> bool
- aspect_strength(aspect_type) -> strength value
```

**Status:** Constants defined, needs implementation  
**Priority:** MEDIUM - Important for interpretation

#### 7. Main Chart Calculator
**File:** `calculations/chart_calculator.py`

```python
Key functions needed:
- calculate_chart(birth_data) -> complete chart JSON
- save_chart(chart_data) -> chart_id
- load_chart(chart_id) -> chart_data
```

**Status:** Not started  
**Priority:** CRITICAL - Orchestrates all calculations

### Database Layer

#### 8. Database Setup
**Files needed:**
- `calculations/database.py` - SQLAlchemy setup
- `calculations/models.py` - ORM models
- `calculations/schema.sql` - Initial schema

**Status:** Schema documented in README, needs implementation  
**Priority:** HIGH - Data persistence layer

#### 9. PostgreSQL Migration
**Files needed:**
- `migrations/001_initial_schema.sql`

**Status:** Not started  
**Priority:** HIGH - Required before any data storage

### Testing

#### 10. Test Suite
**Files needed:**
- `tests/test_ephemeris.py`
- `tests/test_nakshatras.py`
- `tests/test_dashas.py`
- `tests/test_chart_calculator.py`
- `tests/fixtures/known_charts.json`

**Status:** Not started  
**Priority:** HIGH - Validation essential

**Test Chart Data Available:**
- Date: Sep 27, 1953
- Time: 09:10:08 AM
- Location: Amritapuri, India (9°08'N, 76°48'E)
- Timezone: +5:30 (IST)

---

## 📦 Setup & Configuration Files Needed

### 11. Installation Scripts
- `scripts/setup.sh` - Automated setup
- `scripts/install_swisseph.sh` - Download ephemeris files
- `.env.example` - Environment variables template

### 12. Docker Configuration
- `docker-compose.yml` - Local development
- `Dockerfile.python` - Calculation engine
- `Dockerfile.mcp` - MCP server

### 13. GitHub Configuration
- `.github/workflows/ci.yml` - Continuous integration
- `.github/workflows/test.yml` - Automated testing
- `CONTRIBUTING.md` - Contribution guidelines
- `LICENSE` - MIT license file

---

## 🎯 Week 1 Goals (Revised)

**By end of Week 1, have:**
1. ✅ Complete documentation
2. ✅ MCP server structure
3. ✅ Constants and reference data
4. ⏳ Swiss Ephemeris integration (IN PROGRESS)
5. ⏳ Basic chart calculation (planets + houses)
6. ⏳ Nakshatra identification
7. ⏳ Database setup
8. ⏳ One working end-to-end test

**Minimum Viable Product (MVP):**
- User can provide birth data to Claude
- Claude calls chart_create tool
- MCP server invokes Python calculator
- Returns: planetary positions, rashis, nakshatras, houses
- Data stored in PostgreSQL
- Chart retrievable via chart_id

---

## 🚧 Known Blockers

1. **Swiss Ephemeris Data Files**
   - Need to download ephemeris files (~100MB)
   - Store in: `/calculations/ephemeris_data/`
   - URL: ftp://ftp.astro.com/pub/swisseph/ephe/

2. **PostgreSQL Setup**
   - Local vs Docker decision
   - Connection string configuration
   - Migration strategy

3. **Timezone Handling**
   - Complex timezone conversions
   - Historical timezone data
   - pytz vs dateutil.tz decision

---

## 💭 Design Decisions Made

### 1. User Data Storage
**Decision:** Both local and cloud options (1c)
- Default: Local PostgreSQL
- Optional: Cloud sync for chart sharing
- User controls what data leaves machine

### 2. Remedy Philosophy
**Decision:** Wait until explicitly asked (2b)
- Don't push remedies unprompted
- Provide when user asks
- Always frame as supportive tools, not magic

### 3. Monetization
**Decision:** Fully open source (3a)
- MIT license
- No premium tiers initially
- Community-driven development
- Potential consulting services later

### 4. Claude Access
**Decision:** Web version with Claude API (4b)
- Build web interface that calls Claude API
- Not restricted to Claude Pro users
- More accessible

### 5. Interpretation Style
**Decision:** Blend classical + modern psychology (5c - TBD)
- Will refine based on testing
- Start with classical principles
- Add psychological depth naturally
- User feedback will guide balance

---

## 📝 Notes for Development

### For Her's Chart
**Birth Data Provided:**
- Date: September 27, 1953
- Time: 09:10:08 AM
- Location: Amritapuri, India
- Coordinates: 9°08'N, 76°48'E
- Timezone: India Standard Time (UTC +5:30)

**Special Considerations:**
- High spiritual evolution likely
- Approach with deep respect
- Focus on dharma and service themes
- Avoid personal relationship speculation

### Validation Strategy
- Compare all calculations against JHora (free software)
- Tolerance: ±1 arc-minute for planets
- Test edge cases (retrograde, sign cusps, pole latitudes)
- Blind interpretation tests (AI vs human)

### Performance Targets
- Chart calculation: <2 seconds
- Database retrieval: <100ms
- MCP tool response: <3 seconds total
- Concurrent users: 10+ (initial)

---

## 🎨 Future Enhancements (Post-MVP)

### Phase 2 Features
- All 16 divisional charts (Shodasha Varga)
- Shadbala calculations
- Ashtakavarga system
- Advanced yoga identification
- Transit predictions
- PDF report generation

### Phase 3 Features
- Web UI (if MCP proves limiting)
- Birth time rectification
- Prashna (horary) module
- Muhurta (electional) system
- Relationship compatibility reports

### Phase 4 Features
- Mobile apps (iOS/Android)
- Multi-language support
- Research database (anonymized)
- Academic collaboration tools
- Teaching/learning modules

---

## 🤝 Collaboration Needs

**Seeking contributors for:**
1. Vedic astrology expertise (validation)
2. Python astronomy calculations (optimization)
3. PostgreSQL schema design (scalability)
4. UI/UX design (if web interface needed)
5. Technical writing (documentation)
6. Testing (edge cases, accuracy)

---

## 📊 Progress Tracking

**Overall Completion:** ~30%

- Documentation: 95%
- MCP Server: 80%
- Calculation Engine: 15%
- Database: 0%
- Testing: 0%
- Deployment: 0%

**Target for Week 1:** 60% overall completion

---

## 🔄 Next Immediate Actions

**TODAY:**
1. Create `ephemeris.py` with Swiss Ephemeris integration
2. Create `chart_calculator.py` main orchestrator
3. Create `database.py` setup
4. Create basic test with Her's chart data

**THIS WEEK:**
5. Complete Nakshatra and Dasha calculators
6. Implement house system
7. Create SQL schema and migrations
8. Write comprehensive tests
9. End-to-end integration test

**NEXT WEEK:**
10. Refine MCP tools based on testing
11. Enhance system prompts
12. Add divisional charts
13. Begin documentation for users
14. Prepare for early adopter testing

---

**Status:** Foundation solid, ready for core implementation phase.

*Last updated by: Development Team*  
*Next review: End of Week 1*
