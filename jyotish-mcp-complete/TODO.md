# TODO - Jyotish MCP Implementation

## ✅ Completed

- [x] MCP server structure with 8 tools
- [x] Python 3.12 environment setup
- [x] Swiss Ephemeris integration
- [x] Constants and reference data (rashis, nakshatras, etc.)
- [x] chart_calculator.py (create, read, list charts)
- [x] dasha_calculator.py (Vimshottari Dasha with balance)
- [x] transit_calculator.py (current planetary transits)
- [x] varga_calculator.py (D1 only, stubs for others)
- [x] Path resolution fixes in MCP server
- [x] Documentation and setup scripts
- [x] Ephemeris download via HTTPS

## 🔨 High Priority (Needed for MVP)

### Python Calculation Scripts

- [ ] **Divisional Charts (vargas.py)**
  - [ ] D9 (Navamsa) - CRITICAL for complete readings
  - [ ] D10 (Dasamsa) - Career analysis
  - [ ] D2, D3, D7, D12, D30 - Standard divisions
  - [ ] Full Shodashavargas (16 divisions)

- [ ] **House System (houses.py)**
  - [ ] Whole Sign house calculation (currently inline)
  - [ ] House cusps generation
  - [ ] Bhava Madhya (house midpoints)
  - [ ] House lordships

- [ ] **Aspects System (aspects.py)**
  - [ ] Traditional full aspects (7th for all)
  - [ ] Special aspects (Mars 4/8, Jupiter 5/9, Saturn 3/10)
  - [ ] Aspect strength calculations
  - [ ] Mutual aspects identification

- [ ] **Yoga Identification (yoga_identifier.py)**
  - [ ] Raj Yogas (power/status combinations)
  - [ ] Dhana Yogas (wealth combinations)
  - [ ] Pancha Mahapurusha Yogas (great personality)
  - [ ] Debilitation cancellation (Neecha Bhanga)
  - [ ] Exchange yogas (Parivartana)

- [ ] **Compatibility Analysis (compatibility_calculator.py)**
  - [ ] Kuta system (Ashtakoota)
  - [ ] Cross-aspects between charts
  - [ ] 7th house and Venus analysis
  - [ ] Composite chart generation

### Database Integration

- [ ] **PostgreSQL Schema**
  - [ ] Create tables (charts, planets, houses, dashas)
  - [ ] Migration from file-based cache
  - [ ] Database connection module
  - [ ] SQLAlchemy models

- [ ] **Data Persistence**
  - [ ] Replace `.charts_cache/` with PostgreSQL
  - [ ] Chart CRUD operations
  - [ ] Transaction handling
  - [ ] Connection pooling

### Testing

- [ ] **Unit Tests**
  - [ ] Test chart calculations against known charts
  - [ ] Test nakshatra calculations
  - [ ] Test Dasha period generation
  - [ ] Test transit calculations
  - [ ] Validate against JHora/commercial software

- [ ] **Integration Tests**
  - [ ] End-to-end MCP → Python → Response
  - [ ] Claude Desktop integration test
  - [ ] Multi-chart scenarios
  - [ ] Error handling

- [ ] **Test Data**
  - [ ] Her's chart (Sep 27, 1953, 9:10 AM, Amritapuri)
  - [ ] 10+ additional known charts
  - [ ] Edge cases (retrograde, sign cusps, poles)

## 🎯 Medium Priority

### Advanced Calculations

- [ ] **Shadbala (Six-fold strength)**
  - [ ] Positional strength (Sthanabala)
  - [ ] Directional strength (Digbala)
  - [ ] Temporal strength (Kalabala)
  - [ ] Natural strength (Naisargikabala)
  - [ ] Combined strength scores

- [ ] **Ashtakavarga**
  - [ ] Bindus calculation
  - [ ] House-wise scores
  - [ ] Transit predictions using Ashtakavarga

- [ ] **Bhava Bala (House strength)**
  - [ ] Bhavadhipati Bala
  - [ ] Bhava Digbala
  - [ ] Bhava Drishti Bala

- [ ] **Special Lagnas**
  - [ ] Bhava Lagna
  - [ ] Hora Lagna
  - [ ] Ghati Lagna

### Enhanced Features

- [ ] **Prashna (Horary Astrology)**
  - [ ] Question chart calculation
  - [ ] Interpretation guidelines
  - [ ] Integration with birth chart

- [ ] **Muhurta (Electional Astrology)**
  - [ ] Find auspicious times
  - [ ] Activity-specific considerations
  - [ ] Tarabala and other factors

- [ ] **Transit Predictions**
  - [ ] Sade Sati calculation
  - [ ] Transit of slow planets (Jupiter, Saturn)
  - [ ] Gochara Phala (transit results)

- [ ] **Panchanga**
  - [ ] Tithi (lunar day)
  - [ ] Vara (weekday)
  - [ ] Nakshatra
  - [ ] Yoga
  - [ ] Karana

## 📊 Lower Priority (Future)

### Visualization

- [ ] **Chart Rendering**
  - [ ] South Indian style SVG
  - [ ] North Indian style SVG
  - [ ] East Indian style SVG
  - [ ] PDF generation

- [ ] **Ephemeris Display**
  - [ ] Monthly ephemeris tables
  - [ ] Planetary positions graph
  - [ ] Retrograde periods visualization

### Analysis Tools

- [ ] **Birth Time Rectification**
  - [ ] Reverse engineering from life events
  - [ ] Multiple algorithm support
  - [ ] Confidence scoring

- [ ] **Research Database**
  - [ ] Anonymized chart storage
  - [ ] Pattern analysis
  - [ ] Statistical correlations
  - [ ] Privacy-preserving queries

- [ ] **AI Integration**
  - [ ] Enhanced interpretation prompts
  - [ ] Pattern recognition
  - [ ] Predictive modeling
  - [ ] Natural language queries

### User Experience

- [ ] **Web Interface**
  - [ ] React dashboard
  - [ ] Chart input forms
  - [ ] Visual chart display
  - [ ] Report generation

- [ ] **API Enhancements**
  - [ ] REST API endpoints
  - [ ] GraphQL support
  - [ ] Webhooks for events
  - [ ] Rate limiting

- [ ] **Multi-User Support**
  - [ ] User authentication
  - [ ] Chart sharing
  - [ ] Permissions system
  - [ ] User preferences

## 🐛 Known Issues

### Critical

- [ ] **Path Resolution**
  - [x] Fixed: MCP server now uses relative paths
  - [ ] Test on Windows (path separators)
  - [ ] Test when installed in different locations

- [ ] **Python Environment**
  - [x] Fixed: Now uses venv Python
  - [ ] Add fallback to system Python if venv missing
  - [ ] Check Python version at runtime

- [ ] **Error Handling**
  - [ ] Better error messages for missing ephemeris files
  - [ ] Validation of input dates (valid ranges)
  - [ ] Graceful degradation if calculations fail

### Non-Critical

- [ ] **Performance**
  - [ ] Cache frequently accessed calculations
  - [ ] Optimize Dasha generation (currently generates all 120 years)
  - [ ] Batch processing for multiple charts

- [ ] **Documentation**
  - [ ] API examples for each tool
  - [ ] Video walkthrough
  - [ ] Architecture diagrams
  - [ ] Calculation algorithm explanations

## 📝 Notes

### Implementation Order Recommendation

1. **Phase 1** (Week 1-2): Core MVP
   - D9 (Navamsa) calculation
   - Aspects system
   - PostgreSQL integration
   - Basic tests

2. **Phase 2** (Week 3-4): Enhanced Accuracy
   - More divisional charts (D2, D3, D7, D10, D12, D30)
   - Yoga identification
   - Compatibility analysis
   - Comprehensive test suite

3. **Phase 3** (Month 2): Advanced Features
   - Shadbala and strength calculations
   - Ashtakavarga
   - Prashna and Muhurta
   - Chart visualization

4. **Phase 4** (Month 3+): Polish
   - Web interface
   - Multi-user support
   - Birth time rectification
   - Research database

### Testing Strategy

- Use Her's chart as primary validation
- Cross-reference with JHora (free software)
- Compare with 3+ commercial software packages
- Test edge cases (retrograde, combustion, etc.)
- Validate classical text examples

### Performance Targets

- Chart calculation: <2 seconds
- Dasha generation: <1 second
- Transit calculation: <500ms
- Database queries: <100ms
- API response: <3 seconds total

---

**Current Status:** ~40% complete (infrastructure + basic calculations)

**Next Immediate Task:** Implement D9 (Navamsa) calculation

**Contributors:** See [CONTRIBUTING.md](CONTRIBUTING.md)
