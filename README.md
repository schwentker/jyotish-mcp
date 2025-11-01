# Jyotish MCP - AI Meets Ancient Wisdom

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue.svg)](https://modelcontextprotocol.io)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**An experiment in synthesizing modern AI pattern recognition with 5,000-year-old Vedic predictive systems.**

---

## 🎯 Executive Summary

### The Experiment

Can we combine:
- **Ancient System:** Jyotish (Vedic astrology) - mathematical predictive framework used for millennia
- **Modern System:** Large Language Models - pattern recognition trained on humanity's collective knowledge

To create something more insightful than either alone?

### Why This Matters

**For Skeptics:** This isn't about "believing in astrology." It's about:
- Testing whether AI can surface patterns humans miss when interpreting complex multi-variable systems
- Exploring symbolic frameworks as lenses for decision-making (similar to scenario planning)
- Examining if ancient mathematical models contain signal worth extracting with modern tools

**For Practitioners:** This isn't replacing human astrologers. It's:
- Democratizing access to interpretive depth
- Preserving traditional calculation methods with precision
- Enabling conversational exploration of chart dynamics

**For Technologists:** This demonstrates:
- Model Context Protocol (MCP) for domain expertise
- AI as interpretive layer over precise calculations
- Ethical AI for sensitive personal insights

### What Makes This Different

Traditional astrology software: Calculator with fixed interpretations  
This project: Conversational AI consultant backed by precise astronomical math

**Status:** Early experimental phase. Architecture may evolve significantly based on findings.

---

## 🔬 Nature of the Experiment

### Hypothesis

Vedic astrology's mathematical precision (planetary positions, timing systems, harmonic divisions) combined with Claude's contextual reasoning creates emergent interpretive capabilities beyond:
- Pure calculation engines
- Static interpretation databases  
- Human astrologers working in isolation

### Variables Being Tested

1. **Calculation Accuracy:** Swiss Ephemeris (±1 arc-second) vs traditional hand calculations
2. **Interpretation Depth:** AI synthesis vs rule-based systems
3. **User Experience:** Conversational interface vs form-based software
4. **Ethical Boundaries:** AI guardrails for psychological safety

### Success Metrics (TBD)

- Interpretation consistency across chart re-readings
- User-reported insight quality (qualitative)
- Calculation validation against established software
- Adoption by practitioners as complementary tool

### Known Limitations

- AI cannot predict specific events (nor should it)
- System reflects training data biases
- Requires user discernment and free will
- Not a substitute for professional guidance (medical, legal, financial)

**This is research-grade software, not production divination.**

---

## 👥 For Different Stakeholders

### 🏢 Business Leaders & Strategists

**Why pay attention:**
- **Decision Frameworks:** Many executives use personality assessments (MBTI, Enneagram) for team dynamics. This explores whether ancient frameworks + AI offer complementary insights.
- **Pattern Recognition:** If AI can find signal in complex multi-variable symbolic systems, applications extend to market analysis, scenario planning, risk modeling.
- **Innovation Methodology:** Demonstrates how to revive ancient knowledge systems with modern tech responsibly.

**Analogies you know:**
- Like using AI to analyze chess positions (ancient game + modern compute)
- Or applying ML to Traditional Chinese Medicine diagnosis patterns
- Or using LLMs to interpret I Ching hexagrams for strategic questions

**The bet:** Some signal exists in systems that survived millennia of selection pressure. Worth extracting scientifically.

### 🔮 Astrology Practitioners

**Why contribute:**
- Preserves traditional calculations with open-source transparency
- Augments (not replaces) human interpretation
- Enables exploration of chart nuances conversationally
- Documents reasoning chains for learning

**What's respected:**
- Traditional Parashari methods (Whole Sign houses, classical aspects)
- Lahiri ayanamsa (standard)
- No Western/modern planet additions without explicit request
- Ethical interpretation guidelines built-in

**What's new:**
- AI synthesizes D1 + D9 + Dashas + transits simultaneously
- Natural language exploration of yogas and patterns
- Learns from conversation to refine responses

### 💻 Developers & Data Scientists

**Technical innovation:**
- **MCP Architecture:** Domain expertise via tool-calling protocol
- **Hybrid System:** Precise calculations (Python/Swiss Ephemeris) + interpretive reasoning (Claude)
- **Prompt Engineering:** System prompts encode classical Jyotish principles
- **Ethical AI:** Guardrails against fatalism, fear-mongering, dependency

**Skills demonstrated:**
- Real-time astronomical calculations
- Complex data synthesis across temporal dimensions
- Conversational AI for sensitive domains
- Open-source scientific software

### 🧘 Spiritual Seekers & Users

**What you get:**
- Conversational exploration of your birth chart
- Synthesis of timing (Dashas), current energy (transits), life domains (divisional charts)
- Psychological framing without determinism
- Privacy-respecting (charts stored locally if preferred)

**What you don't get:**
- Specific predictions ("you will marry on X date")
- Fear-based interpretations
- Dependency-creating language
- Medical/legal/financial advice

**Philosophy:** Charts show tendencies, not fate. You have free will. This is a mirror for self-reflection, not a script for your life.

---

## 🗺️ Quick Start (For Non-Technical Users)

### What You'll Need

1. **Claude Desktop App** with Claude Pro subscription (for MCP support)
2. **Python 3.11+** installed on your computer
3. **10 minutes** for setup

### Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/jyotish-mcp.git
cd jyotish-mcp

# Run setup script
./scripts/setup.sh

# The script will:
# - Install Python dependencies
# - Download Swiss Ephemeris data files
# - Set up local database
# - Configure MCP server
```

### Usage

1. Open Claude Desktop
2. Say: "Calculate my birth chart: [date] [time] [location]"
3. Claude will use the MCP tools to calculate and interpret

**Example:**
```
You: "Can you read my chart? Born September 27, 1953, 9:10 AM 
     in Amritapuri, India (9°08'N, 76°48'E)"

Claude: [Uses chart_create tool]
        [Uses dasha_current tool]
        [Uses transit_now tool]
        
        "I've calculated your chart. You're a Libra rising..."
        [Provides interpretation]
```

---

## 🏗️ Architecture Overview

### The MCP Approach

**Why not build another astrology app?**

Traditional approach:
```
User → Web Form → Database → Calculation → Display Chart
(Rigid, one-size-fits-all interpretation)
```

MCP approach:
```
User → Conversational AI → MCP Tools → Calculations → Dynamic Interpretation
(Flexible, context-aware, exploratory)
```

### System Components

```
┌─────────────────────────────────────────┐
│         Claude (AI Astrologer)          │
│  - Interprets charts conversationally   │
│  - Synthesizes multiple data sources    │
│  - Provides psychological context       │
└───────────────┬─────────────────────────┘
                │ MCP Protocol
┌───────────────▼─────────────────────────┐
│         MCP Server (TypeScript)         │
│  Tools: chart_create, dasha_current,    │
│         transit_now, divisional_read... │
└───────────────┬─────────────────────────┘
                │ Subprocess/API
┌───────────────▼─────────────────────────┐
│    Calculation Engine (Python)          │
│  - Swiss Ephemeris integration          │
│  - Nakshatra, Dasha, Varga algorithms   │
│  - House systems, aspects               │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│      PostgreSQL Database (Local)        │
│  - Chart storage                        │
│  - User data (optional)                 │
│  - Calculation cache                    │
└─────────────────────────────────────────┘
```

### Data Privacy Options

**Option A: Local Storage (Default)**
- All data stored on your machine
- No cloud dependencies after setup
- Full privacy

**Option B: Cloud + Local Hybrid**
- Calculations local
- Optional chart sharing via cloud
- You control what syncs

**Option C: Fully Open Source Self-Host**
- Deploy your own instance
- Complete data sovereignty
- For enterprises/institutions

---

## 🛠️ Technical Architecture

### MCP Tools Specification

#### Core Chart Tools

```typescript
chart_create(birth_data: BirthData) -> ChartID
/**
 * Calculates complete birth chart
 * Input: date, time, location, timezone
 * Output: chart_id for future reference
 * Stores: D1, D9, all planetary positions, houses, nakshatras
 */

chart_read(chart_id: string) -> FullChart
/**
 * Retrieves complete chart data
 * Includes: all calculations, metadata, previous interpretations
 */

chart_list() -> ChartSummary[]
/**
 * Lists all stored charts
 * For multi-chart comparison
 */
```

#### Temporal Analysis Tools

```typescript
dasha_current(chart_id: string, date?: Date) -> DashaPeriods
/**
 * Returns current/specified Maha, Antar, Pratyantar Dashas
 * Includes: ruling planets, start/end dates, remaining balance
 */

dasha_timeline(chart_id: string, start: Date, end: Date) -> Timeline
/**
 * Maps Dasha periods across date range
 * Useful for: life review, future planning
 */

transit_now(chart_id: string, date?: Date) -> TransitPositions
/**
 * Current planetary positions relative to birth chart
 * Identifies: house transits, aspects to natal planets
 */
```

#### Divisional Chart Tools

```typescript
divisional_read(chart_id: string, varga: string) -> DivisionalChart
/**
 * Retrieves specific divisional chart
 * Supported: D1-D60 (configurable)
 * Phase 1: D1, D9
 * Phase 2: D2, D3, D7, D10, D12, D30
 */

divisional_compare(chart_id: string, vargas: string[]) -> Comparison
/**
 * Cross-references multiple divisional charts
 * Identifies: repeating patterns, confirmation of themes
 */
```

#### Analysis Tools

```typescript
yogas_identify(chart_id: string) -> Yoga[]
/**
 * Identifies classical yogas (planetary combinations)
 * Examples: Raj Yoga, Dhana Yoga, Pancha Mahapurusha
 */

strength_analysis(chart_id: string) -> StrengthScores
/**
 * Calculates Shadbala (six-fold strength)
 * Includes: positional, directional, temporal, natural
 */

compatibility_analyze(chart_id_1: string, chart_id_2: string) -> Synastry
/**
 * Relationship compatibility analysis
 * Includes: Kuta system, cross-aspects, composite chart
 */
```

#### Predictive Tools

```typescript
question_analyze(chart_id: string, question: string, ask_time: Date) -> Prashna
/**
 * Horary astrology (Prashna)
 * Analyzes question chart relative to birth chart
 */

timing_find(chart_id: string, activity: string, timeframe: DateRange) -> Muhurta[]
/**
 * Electional astrology
 * Finds auspicious timings for activities
 */
```

### Calculation Engine Design

#### Python Backend Structure

```python
# Core calculation modules
calculations/
├── ephemeris.py          # Swiss Ephemeris wrapper
│   └── get_planet_position(jd, planet, flags)
├── houses.py             # Whole Sign house system
│   └── calculate_houses(jd, lat, lon)
├── nakshatras.py         # 27 nakshatra system
│   └── get_nakshatra(longitude) -> (name, pada, ruler)
├── dashas.py             # Vimshottari Dasha
│   └── calculate_vimshottari(moon_longitude, birth_jd)
├── vargas.py             # Divisional charts
│   └── calculate_divisional(longitude, division)
└── aspects.py            # Traditional aspects
    └── get_aspects(planets, houses)
```

#### Swiss Ephemeris Integration

```python
import swisseph as swe

# Configuration
swe.set_ephe_path('/path/to/ephemeris/data')
swe.set_sid_mode(swe.SIDM_LAHIRI)  # Lahiri ayanamsa

# Calculate planet position
jd = swe.julday(year, month, day, hour_decimal)
result = swe.calc_ut(jd, planet_id, swe.FLG_SIDEREAL)
longitude = result[0]  # Sidereal longitude

# Example: Sun position
sun_long = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)[0]
```

### Database Schema

```sql
-- Charts
CREATE TABLE charts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255),
    datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    ayanamsa VARCHAR(20) DEFAULT 'LAHIRI',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Planetary Positions (D1)
CREATE TABLE planet_positions (
    chart_id UUID REFERENCES charts(id) ON DELETE CASCADE,
    planet VARCHAR(20) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    rashi VARCHAR(20) NOT NULL,
    nakshatra VARCHAR(30) NOT NULL,
    nakshatra_pada INTEGER CHECK (nakshatra_pada BETWEEN 1 AND 4),
    house_number INTEGER CHECK (house_number BETWEEN 1 AND 12),
    is_retrograde BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (chart_id, planet)
);

-- House Cusps
CREATE TABLE house_cusps (
    chart_id UUID REFERENCES charts(id) ON DELETE CASCADE,
    house_number INTEGER CHECK (house_number BETWEEN 1 AND 12),
    cusp_longitude DECIMAL(10, 6) NOT NULL,
    rashi VARCHAR(20) NOT NULL,
    PRIMARY KEY (chart_id, house_number)
);

-- Dasha Periods (nested JSONB)
CREATE TABLE dasha_periods (
    chart_id UUID REFERENCES charts(id) ON DELETE CASCADE PRIMARY KEY,
    dasha_tree JSONB NOT NULL,  -- Full Maha > Antar > Pratyantar tree
    created_at TIMESTAMP DEFAULT NOW()
);

-- Divisional Charts
CREATE TABLE divisional_charts (
    chart_id UUID REFERENCES charts(id) ON DELETE CASCADE,
    division_type VARCHAR(10) NOT NULL,  -- 'D1', 'D9', etc.
    planet_positions JSONB NOT NULL,
    PRIMARY KEY (chart_id, division_type)
);
```

---

## 🕉️ Jyotish Calculation Standards

All calculations follow **traditional Parashari Vedic astrology principles**. This section documents every interpretive decision for transparency and reproducibility.

### 1. Ayanamsa System

**Decision: Lahiri (Chitrapaksha)**

- Most widely accepted in Indian Vedic astrology
- Value ~24°11' (2025)
- Swiss Ephemeris flag: `SIDM_LAHIRI`

**Rationale:** Standard for consistency. User-selectable ayanamsa in Phase 2.

### 2. House System

**Decision: Whole Sign Houses**

Each house occupies an entire zodiac sign starting from ascendant rashi.

```
Example: Ascendant at 15° Libra
- 1st House: 0°-30° Libra (entire sign)
- 2nd House: 0°-30° Scorpio
- 3rd House: 0°-30° Sagittarius
... continuing through zodiac
```

**Rationale:**
- Traditional Vedic approach (classical texts)
- Simplifies divisional calculations
- Avoids intercepted houses
- Clear for algorithmic implementation

**Ascendant Definition:**
- Exact degree stored
- Houses extend from 0° of each sign

### 3. Planetary Aspects (Graha Drishti)

**Decision: Traditional full aspects only**

**All Planets:**
- 7th house aspect (opposition)

**Mars (Kuja):**
- 4th, 7th, 8th house aspects

**Jupiter (Guru):**
- 5th, 7th, 9th house aspects

**Saturn (Shani):**
- 3rd, 7th, 10th house aspects

**Implementation:**
- Aspects counted by house position (whole sign)
- 100% strength (no degree-based gradation in v1)

**Rationale:** Classical Parashari system, unambiguous interpretation

### 4. Vimshottari Dasha System

**Decision: Moon nakshatra-based with birth balance**

**Algorithm:**
```
1. Find Moon's exact longitude at birth
2. Determine nakshatra and ruling planet
3. Calculate Moon's progress through nakshatra
4. Determine remaining balance of birth Dasha
5. Generate 120-year cycle from that point
6. Calculate nested periods:
   - Maha Dasha (major period)
   - Antar Dasha (sub-period)  
   - Pratyantar Dasha (sub-sub-period)
```

**Dasha Sequence & Durations:**
```
Ketu    → 7 years
Venus   → 20 years
Sun     → 6 years
Moon    → 10 years
Mars    → 7 years
Rahu    → 18 years
Jupiter → 16 years
Saturn  → 19 years
Mercury → 17 years
─────────────────
Total: 120 years
```

**Birth Balance Example:**
```
If Moon at 18°20' in Rohini nakshatra (ruled by Moon):
- Rohini spans: 10°00' to 23°20' Taurus
- Moon has traveled: 8°20' into nakshatra
- Remaining: 5°00' (of 13°20' total)
- Birth balance: Moon Dasha with ~3.75 years remaining
```

**Rationale:** Standard Parashari timing system, universally applicable

### 5. Nakshatra System

**Decision: 27 nakshatras (Abhijit excluded)**

Each nakshatra:
- Span: 13°20' (360° ÷ 27)
- 4 padas: 3°20' each
- Ruling planet (for Dasha)
- Associated deity, qualities

**Nakshatra List:**
```
1. Ashwini     (0°00'-13°20' Aries)      - Ketu
2. Bharani     (13°20'-26°40' Aries)     - Venus
3. Krittika    (26°40' Aries-10°00' Tau) - Sun
4. Rohini      (10°00'-23°20' Taurus)    - Moon
... (27 total)
27. Revati     (16°40'-30°00' Pisces)    - Mercury
```

**Rationale:** Standard modern Vedic system, Vimshottari-compatible

### 6. Divisional Charts (Vargas)

**Phase 1: D1 and D9 only**

**D1 (Rashi):**
- Birth chart
- Physical life, personality, events

**D9 (Navamsa):**
- 9th harmonic (each sign ÷ 9)
- Marriage, dharma, spiritual evolution
- Confirms D1 promises

**Calculation (Navamsa):**
```python
navamsa_position = ((planet_long % 30) * 9) // 30
navamsa_sign = (navamsa_position + sign_number) % 12
```

**Phase 2 Additions:**
- D2 (Hora) - Wealth
- D3 (Drekkana) - Siblings  
- D7 (Saptamsa) - Children
- D10 (Dasamsa) - Career
- D12 (Dwadasamsa) - Parents
- D30 (Trimsamsa) - Misfortunes

**Rationale:** D9 essential, others added based on user demand

### 7. Planet Set

**Traditional 9 Grahas:**
```
1. Sun (Surya)     - Soul, authority
2. Moon (Chandra)  - Mind, emotions
3. Mars (Mangala)  - Energy, action
4. Mercury (Budha) - Intellect, communication
5. Jupiter (Guru)  - Wisdom, expansion
6. Venus (Shukra)  - Desire, relationships
7. Saturn (Shani)  - Karma, discipline
8. Rahu            - North Node, obsession
9. Ketu            - South Node, liberation
```

**Calculation Details:**
- True positions (not mean)
- Rahu/Ketu: True node calculations
- Retrograde detection
- Daily motion (speed)

**Not included (v1):** Uranus, Neptune, Pluto, Upagrahas

### 8. Chart Visualization Priority

**Phase 1: South Indian style (data format)**

Chart rendering handled by Claude's interpretation, not visual output initially.

**Future:** SVG generation for South/North/East Indian styles

---

## 🤖 AI Interpretation Framework

### Master System Prompt

The MCP server includes a comprehensive system prompt that guides Claude's interpretations. Key principles:

**Interpretive Philosophy:**
```markdown
1. Holistic Synthesis
   - Cross-reference D1, D9, Dashas, transits simultaneously
   - Look for confirming/denying patterns
   - Present integrated narrative

2. Psychological Framing
   - Planets = archetypal energies, not literal predictors
   - Houses = life domains, not fixed outcomes
   - Dashas = timing for themes to ripen
   - Free will always emphasized

3. Ethical Boundaries
   - No fatalistic predictions
   - No medical/legal/financial advice
   - No death predictions
   - No fear-mongering language
   - Acknowledge uncertainty

4. Traditional Accuracy
   - Follow classical principles
   - Cite source texts when relevant
   - Don't mix Western methods without disclosure
   - Honor lineage of knowledge
```

**Interpretation Workflow:**
```
User provides birth data
    ↓
Claude calls chart_create
    ↓
Claude calls dasha_current + transit_now
    ↓
Claude synthesizes:
- Ascendant/Moon = soul's journey
- Planet placements = resources/challenges
- Current Dasha = active theme
- Transits = immediate catalysts
    ↓
Claude presents interpretation conversationally
    ↓
User asks follow-up questions
    ↓
Claude calls additional tools as needed
(divisional_read, yogas_identify, etc.)
    ↓
Iterative refinement of understanding
```

### Response Guidelines

**Structure:**
```
1. Acknowledge chart calculation
2. Core identity (Ascendant, Moon, Sun)
3. Current life phase (Dasha period)
4. Present influences (transits)
5. Specific area user asked about
6. Open-ended question for exploration
```

**Tone:**
- Warm, non-dogmatic
- Psychological sophistication
- Cultural sensitivity
- Empowering language

**Examples of Good/Bad Framing:**

❌ Bad: "You will lose your job in Saturn Dasha"
✅ Good: "Saturn periods often bring career restructuring. Your chart suggests you're being asked to build something more sustainable. What feels misaligned right now?"

❌ Bad: "Mars in 7th means divorce"
✅ Good: "Mars in 7th can bring intensity to partnerships. You may be attracted to dynamic, assertive partners. Healthy channels for this energy include shared activities and honest communication about needs."

❌ Bad: "Your 8th house Saturn will cause suffering"
✅ Good: "8th house Saturn gives you depth and resilience. You may face transformative experiences, but these ultimately build psychological strength. Many great researchers and healers have this placement."

---

## 📋 Project Roadmap

### Phase 1: MCP Foundation (Current)

**Week 1-2:**
- [x] Project architecture documentation
- [x] Calculation engine design
- [ ] Swiss Ephemeris Python integration
- [ ] Basic MCP server (TypeScript)
- [ ] 5 core tools: chart_create, chart_read, dasha_current, transit_now, divisional_read
- [ ] PostgreSQL schema setup
- [ ] Test with 10+ known charts

**Deliverable:** Working MCP server that Claude can use for basic chart reading

### Phase 2: Enhanced Tools

**Week 3-4:**
- [ ] Additional divisional charts (D2-D30)
- [ ] Yoga identification algorithm
- [ ] Shadbala calculations
- [ ] Compatibility tools (synastry)
- [ ] Transit prediction
- [ ] Refined system prompts
- [ ] Expanded test suite (50+ charts)

**Deliverable:** Comprehensive interpretive toolkit

### Phase 3: User Experience

**Week 5-6:**
- [ ] Onboarding documentation
- [ ] Installation scripts
- [ ] Chart storage/retrieval optimization
- [ ] Error handling and edge cases
- [ ] Privacy controls
- [ ] Export features (PDF reports)

**Deliverable:** Production-ready for early adopters

### Phase 4: Community & Iteration

**Month 2-3:**
- [ ] Gather user feedback
- [ ] Refine interpretation prompts based on usage
- [ ] Add requested features
- [ ] Documentation for contributors
- [ ] Case studies and validation
- [ ] Academic/practitioner collaboration

**Deliverable:** Community-validated system

### Future Exploration (TBD based on Phase 4 findings)

**Optional additions:**
- Web interface (if MCP-only proves limiting)
- Mobile app
- API for third-party integration
- Advanced calculations (Ashtakavarga, various Bala systems)
- Birth time rectification module
- Research database (anonymized charts for pattern analysis)
- Multi-language support

**Decision point:** Does MCP + Claude provide sufficient interface, or do users need visual/web components?

---

## 🧪 Validation Methodology

### Calculation Validation

**Against established software:**
- JHora (free Windows software)
- Jagannatha Hora
- Kala (commercial)
- Parashara's Light

**Test cases:**
- 50 charts with known positions
- Edge cases (near poles, cusp times, retrograde planets)
- Historical charts with verified events

**Acceptance criteria:**
- Planetary positions: ±1 arc-minute
- House cusps: ±10 arc-minutes (whole sign = full rashi)
- Nakshatra: 100% accuracy
- Dasha dates: ±1 day

### Interpretation Validation

**Qualitative assessment:**
- User reports on insight quality
- Practitioner peer review
- Blind tests (AI vs human interpretations)

**Metrics tracked:**
- Consistency (same chart, different sessions)
- Relevance (does interpretation address query)
- Safety (no harmful language detected)
- User satisfaction scores

**Not measured (intentionally):**
- Predictive accuracy of specific events
- "Correctness" of interpretations
(Jyotish is interpretive art, not deterministic science)

---

## 🤝 Contributing

### Who Should Contribute

**Jyotish Experts:**
- Validate calculations
- Refine interpretation prompts
- Suggest classical text references
- Test edge cases

**Developers:**
- Improve calculation efficiency
- Add features
- Fix bugs
- Enhance MCP tools

**UX Researchers:**
- Study how users interact with AI astrologer
- Identify friction points
- Suggest interface improvements

**Ethicists:**
- Review AI safety guardrails
- Flag problematic interpretations
- Improve consent/disclosure language

### How to Contribute

```bash
# Fork repository
git clone https://github.com/yourusername/jyotish-mcp.git
cd jyotish-mcp

# Create branch
git checkout -b feature/your-feature

# Make changes, test thoroughly

# Submit PR with:
- Clear description
- Test results (if calculations)
- Validation against known charts
- Documentation updates
```

### Code Standards

**Python:**
```bash
# Format
black calculations/

# Lint
ruff check calculations/

# Type check
mypy calculations/

# Test
pytest tests/
```

**TypeScript:**
```bash
npm run lint
npm run format
npm run test
```

### Contribution Guidelines

**For calculation changes:**
- Provide classical text reference if applicable
- Test against minimum 10 known charts
- Document any deviations from tradition

**For interpretation prompt changes:**
- Test with diverse chart examples
- Ensure ethical guidelines maintained
- No deterministic/fear-based language

**For new features:**
- Discuss in GitHub Issues first
- Align with project philosophy
- Consider MCP tool design patterns

---

## 📄 License & Legal

### MIT License

This project uses the MIT License, allowing:
- Commercial use
- Modification
- Distribution
- Private use

**Requirements:**
- Include original copyright notice
- Include license text

**Limitations:**
- No warranty
- No liability

See [LICENSE](LICENSE) file for details.

### Swiss Ephemeris License

This project uses Swiss Ephemeris for astronomical calculations:
- Free for non-commercial use
- Requires separate license for commercial deployment
- See: https://www.astro.com/swisseph/

**For commercial users:** Contact Astrodienst for licensing.

### Ethical Use Policy

**This software must not be used for:**
- Medical diagnosis or treatment
- Legal advice or proceedings
- Financial investment recommendations
- Coercing or manipulating vulnerable individuals
- Any purpose causing psychological harm

**Users acknowledge:**
- Interpretations are for self-reflection
- No guaranteed accuracy
- Professional consultation recommended for serious matters
- Free will supersedes chart indications

---

## 🙏 Acknowledgments

### Sources

**Astronomical Calculations:**
- Swiss Ephemeris by Astrodienst AG

**Classical Texts:**
- Brihat Parashara Hora Shastra (BPHS)
- Jataka Parijata
- Phaladeepika
- Saravali

**Modern References:**
- B.V. Raman
- K.N. Rao
- James Braha
- Komilla Sutton

**Technology:**
- Anthropic (Claude & MCP)
- PostgreSQL community
- Python astronomy community

### Philosophy

This project stands at the intersection of:
- Ancient wisdom preservation
- Modern AI capabilities  
- Open source collaboration
- Ethical technology development

We honor the lineage of Jyotish masters while exploring how AI can democratize access to this profound system.

*"The stars incline, they do not compel."*

---

## 📞 Support & Community

### Getting Help

**Technical Issues:**
- GitHub Issues: Bug reports, feature requests
- Discussions: Questions, ideas, general help

**Jyotish Questions:**
- Not a substitute for professional consultation
- Community discussion forum (coming soon)
- Practitioner directory (for human guidance)

**Privacy Concerns:**
- Data handling documentation
- Self-hosting guide
- Contact: privacy@jyotish-mcp.org

### Stay Updated

- **GitHub:** Star the repository for updates
- **Newsletter:** [Coming soon]
- **Blog:** Development updates and insights

---

**Built with precision. Guided by tradition. Empowered by AI.**

*Om Tat Sat* 🕉️
