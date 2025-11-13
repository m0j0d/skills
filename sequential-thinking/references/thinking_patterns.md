# Sequential Thinking Patterns

This guide documents common thinking patterns and strategies when using the Sequential Thinking skill.

## Pattern 1: The Linear Problem Solver

**When to use:** Straightforward problems with a clear path from start to finish.

**Structure:**
1. **Understand** - Frame the problem clearly
2. **Analyze** - Break down components
3. **Strategize** - Plan the approach
4. **Execute** - Work through the solution
5. **Verify** - Check the result

**Example:**
```python
# Thought 1: Understanding the requirements
# Thought 2: Identifying the data structure needed
# Thought 3: Designing the algorithm
# Thought 4: Implementing the solution
# Thought 5: Testing edge cases
```

## Pattern 2: The Iterative Refiner

**When to use:** Problems where initial understanding evolves significantly.

**Structure:**
1. **First pass** - Initial attempt at understanding
2. **Revision** - Refine based on new insights
3. **Second pass** - Improved approach
4. **Revision** - Further refinement
5. **Synthesis** - Final integrated understanding

**Example:**
```python
# Thought 1: Initial problem analysis
# Thought 2: Design approach A
# Thought 3 (Revision of 2): Wait, approach B is better
# Thought 4: Implement approach B
# Thought 5 (Revision of 1): Actually, the problem is different than I thought
# Thought 6: Adjusted solution
```

## Pattern 3: The Multi-Path Explorer

**When to use:** Multiple viable approaches exist and comparison is valuable.

**Structure:**
1. **Common analysis** - Shared understanding
2. **Branch A** - First alternative
3. **Branch B** - Second alternative
4. **Branch C** - Third alternative (if needed)
5. **Comparison** - Evaluate trade-offs
6. **Decision** - Select best approach

**Example:**
```python
# Thought 1: Problem requirements
# Thought 2: Key constraints
# Thought 3 (Branch A): Database solution
# Thought 3 (Branch B): Cache solution
# Thought 3 (Branch C): Hybrid solution
# Thought 4: Compare performance/complexity/cost
# Thought 5: Decision and rationale
```

## Pattern 4: The Hypothesis Tester

**When to use:** Debugging or investigating uncertain situations.

**Structure:**
1. **Observation** - Describe the symptoms
2. **Hypothesis 1** - First theory
3. **Test 1** - Evaluate hypothesis
4. **Hypothesis 2** - Alternative theory (if needed)
5. **Test 2** - Evaluate alternative
6. **Conclusion** - Confirmed understanding

**Example:**
```python
# Thought 1: Bug manifests as timeout errors
# Thought 2: Hypothesis - database query is slow
# Thought 3: Checked query time - not the issue
# Thought 4: Hypothesis - network latency
# Thought 5: Confirmed network issue with diagnostics
# Thought 6: Solution approach
```

## Pattern 5: The Layered Analyzer

**When to use:** Complex systems requiring analysis at multiple levels.

**Structure:**
1. **High-level** - System overview
2. **Mid-level** - Component analysis
3. **Low-level** - Implementation details
4. **Integration** - How layers connect
5. **Synthesis** - Complete understanding

**Example:**
```python
# Thought 1: Business requirements (high level)
# Thought 2: Architecture components (mid level)
# Thought 3: Database schema design (low level)
# Thought 4: API design (low level)
# Thought 5: How components interact (integration)
# Thought 6: Complete system design (synthesis)
```

## Pattern 6: The Constraint-Driven Designer

**When to use:** Problems with significant constraints that shape the solution.

**Structure:**
1. **Requirements** - What needs to be achieved
2. **Constraints** - Limitations and boundaries
3. **Design 1** - First attempt
4. **Constraint check** - Identify violations
5. **Design 2** - Adjusted for constraints
6. **Validation** - Confirm all constraints met

**Example:**
```python
# Thought 1: Need real-time data processing
# Thought 2: Constraints - budget, latency, scale
# Thought 3: Initial design - fancy ML pipeline
# Thought 4: Exceeds budget constraint
# Thought 5: Simplified design - rule-based system
# Thought 6: Meets all constraints
```

## Pattern 7: The Research Synthesizer

**When to use:** Integrating information from multiple sources.

**Structure:**
1. **Research question** - What to investigate
2. **Source 1** - First perspective
3. **Source 2** - Second perspective
4. **Source 3** - Additional perspectives
5. **Synthesis** - Integrate findings
6. **Conclusions** - Answer research question

**Example:**
```python
# Thought 1: How should we implement caching?
# Thought 2: Review Redis documentation
# Thought 3: Study Memcached alternatives
# Thought 4: Examine case studies
# Thought 5: Synthesize pros/cons of each
# Thought 6: Recommendation with rationale
```

## Pattern 8: The Progressive Decomposer

**When to use:** Very large problems that need incremental breakdown.

**Structure:**
1. **Mega-problem** - The whole challenge
2. **Major divisions** - Break into big pieces
3. **Sub-divisions** - Break pieces into tasks
4. **Micro-tasks** - Break tasks into steps
5. **Dependencies** - Identify relationships
6. **Roadmap** - Sequenced execution plan

**Example:**
```python
# Thought 1: Build e-commerce platform
# Thought 2: Major components - user, product, payment, order
# Thought 3: User component - auth, profile, preferences
# Thought 4: Auth - registration, login, password reset, 2FA
# Thought 5: Dependencies - auth before profile
# Thought 6: Implementation sequence
```

## Combining Patterns

Real-world problems often benefit from combining patterns:

### Example: Complex Feature Development

```python
# Phase 1: High-level decomposition (Progressive Decomposer)
# Thought 1: Break down feature into components

# Phase 2: Constraint analysis (Constraint-Driven)
# Thought 2: Identify technical and business constraints

# Phase 3: Multi-path exploration (Multi-Path Explorer)
# Thought 3 (Branch A): Implementation approach 1
# Thought 3 (Branch B): Implementation approach 2

# Phase 4: Iterative refinement (Iterative Refiner)
# Thought 4: Initial design
# Thought 5 (Revision): Refined design after constraint check

# Phase 5: Verification (Linear Problem Solver)
# Thought 6: Final validation
```

## Tips for Pattern Selection

1. **Start simple** - Begin with Linear Problem Solver for most problems
2. **Adapt as needed** - Switch to Iterative Refiner when understanding evolves
3. **Branch deliberately** - Use Multi-Path Explorer when genuinely uncertain
4. **Layer for complexity** - Use Layered Analyzer for system-level problems
5. **Constrain early** - Apply Constraint-Driven when limitations are critical
6. **Research systematically** - Use Research Synthesizer for information integration
7. **Decompose progressively** - Use Progressive Decomposer for large projects
8. **Test hypotheses** - Use Hypothesis Tester for debugging and investigation

## Anti-Patterns to Avoid

### 1. Over-Branching
**Problem:** Creating too many branches for minor variations
**Solution:** Use branches only for substantially different approaches

### 2. Under-Estimation
**Problem:** Setting totalThoughts too low and constantly needing more
**Solution:** Start with a generous estimate, easier to finish early

### 3. Revision Overload
**Problem:** Revising every thought multiple times
**Solution:** Let ideas develop, revise only when truly necessary

### 4. Missing Context
**Problem:** Vague thoughts that don't capture reasoning
**Solution:** Include enough detail that thoughts are self-explanatory

### 5. Premature Completion
**Problem:** Marking nextThoughtNeeded=false before thorough analysis
**Solution:** Ensure the problem is actually solved before completing

## Measuring Thinking Effectiveness

Good sequential thinking sessions typically show:

- **Clear progression** - Each thought builds on previous ones
- **Judicious revision** - 10-30% of thoughts are revisions
- **Selective branching** - 0-3 branches per session
- **Appropriate length** - 5-15 thoughts for most problems
- **Definitive conclusion** - Clear endpoint with solution or decision

## Session Analysis

After completing a thinking session, export it and review:

```python
# Export the session
export_thinking_session(session_id="my_analysis", format="markdown")

# Review the exported file to identify:
# - Were thoughts at the right granularity?
# - Did revisions add value?
# - Were branches necessary?
# - Was the sequence logical?
# - Could any steps be skipped?
```

Use these insights to improve future thinking patterns!
