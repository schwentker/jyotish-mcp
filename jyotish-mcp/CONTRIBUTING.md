# Contributing to Jyotish MCP

Thank you for your interest in contributing! This project combines ancient wisdom with modern AI, and we welcome contributions from various backgrounds.

## Who Can Contribute

- **Jyotish Experts:** Validate calculations, refine interpretations
- **Developers:** Improve code, add features, fix bugs
- **UX Researchers:** Study user interactions, suggest improvements
- **Technical Writers:** Enhance documentation
- **Testers:** Find edge cases, validate accuracy
- **Ethicists:** Review AI safety guardrails

## Getting Started

1. **Read the documentation:**
   - [README.md](README.md) - Project overview
   - [QUICK_START.md](QUICK_START.md) - Setup guide
   - [PROJECT_STATUS.md](PROJECT_STATUS.md) - Current state

2. **Set up your environment:**
   ```bash
   git clone https://github.com/yourusername/jyotish-mcp.git
   cd jyotish-mcp
   # Follow QUICK_START.md
   ```

3. **Find an issue or create one:**
   - Check [GitHub Issues](https://github.com/yourusername/jyotish-mcp/issues)
   - Comment on an issue to claim it
   - Create new issue for bugs or features

## Contribution Guidelines

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes:**
   - Follow code style (see below)
   - Add tests for new features
   - Update documentation

4. **Test thoroughly:**
   ```bash
   # Python tests
   cd calculations
   pytest -v
   
   # TypeScript tests
   cd mcp-server
   npm test
   ```

5. **Submit a pull request:**
   - Clear description of changes
   - Reference related issues
   - Include test results

### Code Style

**Python:**
```bash
# Format with Black
black calculations/

# Lint with Ruff
ruff check calculations/

# Type check
mypy calculations/
```

**TypeScript:**
```bash
# Format and lint
npm run format
npm run lint
```

### Calculation Contributions

If adding or modifying Jyotish calculations:

1. **Provide classical reference:**
   - Cite source text (BPHS, Jataka Parijata, etc.)
   - Explain traditional principle

2. **Validate against known charts:**
   - Test with minimum 10 charts
   - Compare with established software (JHora, etc.)
   - Document any deviations from tradition

3. **Add tests:**
   ```python
   def test_new_calculation():
       result = your_function(test_data)
       expected = known_correct_value
       assert abs(result - expected) < tolerance
   ```

### Interpretation Prompt Contributions

If refining AI interpretation prompts:

1. **Test with diverse examples:**
   - Different chart types
   - Various user questions
   - Edge cases

2. **Maintain ethical guidelines:**
   - No fatalistic language
   - No fear-mongering
   - Emphasize free will
   - Check against guidelines in `prompts/astrologer_system.md`

3. **Document reasoning:**
   - Why this change improves interpretations
   - Example before/after responses

### Documentation Contributions

- Clear, concise writing
- Examples where helpful
- Accessible to varied audiences
- Proofread for typos

## Reporting Issues

### Bug Reports

Include:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Birth data if calculation-related (or use test data)
- Screenshots if UI-related
- System info (OS, Python version, Node version)

### Feature Requests

Include:
- Clear description
- Use case / why it's needed
- Traditional source if Jyotish-related
- Mockups if UI-related

### Calculation Errors

Include:
- Birth data used
- What was calculated
- Expected result (with reference)
- Comparison with other software

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Honor traditional knowledge
- Prioritize user safety and ethics

### Unacceptable Behavior

- Harassment or discrimination
- Disrespectful comments about beliefs
- Pushing personal spiritual/religious views
- Sharing private user data
- Encouraging harmful use of astrology

### Reporting

Contact maintainers privately for Code of Conduct issues.

## Testing Requirements

### For New Features

1. **Unit tests:** Test individual functions
2. **Integration tests:** Test feature end-to-end
3. **Validation tests:** Compare with known correct results

### For Bug Fixes

1. **Reproduction test:** Fails before fix, passes after
2. **Regression test:** Ensure fix doesn't break other features

### Test Data

Use test charts from `tests/fixtures/known_charts.json`

**Do not commit real user data to the repository.**

## Review Process

1. Maintainer reviews PR within 1 week
2. Feedback provided if changes needed
3. Once approved, PR is merged
4. Contributor added to CONTRIBUTORS.md

## Questions?

- **Technical questions:** GitHub Discussions
- **Jyotish questions:** Tag with `jyotish` label
- **Urgent issues:** Tag with `urgent` label

## Recognition

All contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Thanked profusely! 🙏

---

**Thank you for helping preserve and evolve Vedic wisdom with modern technology!**

*Om Tat Sat* 🕉️
