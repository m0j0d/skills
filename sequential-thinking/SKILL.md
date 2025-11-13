---
name: sequential-thinking
description: Dynamic and reflective problem-solving through structured thought sequences. Break down complex problems into manageable steps with revision and branching capabilities. Based on the popular @modelcontextprotocol/server-sequential-thinking MCP server.
license: MIT
---

# Sequential Thinking

A powerful skill for dynamic and reflective problem-solving that enables Claude to work through complex problems step-by-step. This skill provides a structured approach to reasoning with the ability to revise previous thoughts and explore alternative solution paths.

**Originally based on:** `@modelcontextprotocol/server-sequential-thinking` (5,550+ uses on Smithery.ai)

## When to Use This Skill

Use Sequential Thinking when:

- **Breaking down complex problems** - Multi-step challenges that need systematic analysis
- **Iterative reasoning** - Problems where understanding evolves as you work through them
- **Exploring alternatives** - Situations requiring evaluation of different approaches
- **Planning with uncertainty** - When the full solution path isn't immediately clear
- **Refining analysis** - Cases where initial thoughts need revision based on new insights
- **Decision-making** - Evaluating options through structured comparison

## Core Capabilities

### 1. Sequential Reasoning
Process thoughts in a structured sequence, tracking progress through complex problems.

### 2. Dynamic Adjustment
Adapt the total number of thoughts as understanding deepens - no rigid planning required.

### 3. Thought Revision
Reconsider and refine previous thinking steps when new insights emerge.

### 4. Branch Exploration
Fork reasoning paths to explore alternative approaches in parallel.

### 5. Session Management
Maintain separate thinking sessions for different problems or contexts.

## Available Tools

### `sequential_thinking()`

Process a thought in a sequential thinking chain.

**Required Parameters:**
- `thought` (string) - Your current thinking step
- `thoughtNumber` (integer) - Current thought number (starting from 1)
- `totalThoughts` (integer) - Estimated total thoughts needed
- `nextThoughtNeeded` (boolean) - Whether another thought step is needed

**Optional Parameters:**
- `isRevision` (boolean) - Whether this revises previous thinking
- `revisesThought` (integer) - Which thought number is being reconsidered
- `branchFromThought` (integer) - Which thought to branch from
- `branchId` (string) - Identifier for the new branch
- `needsMoreThoughts` (boolean) - Expand beyond initial estimate
- `session_id` (string) - Session identifier for multiple thinking processes

**Returns:** Status, progress, and metadata about the thinking process

**Example:**
```python
# Start a thinking sequence
result = sequential_thinking(
    thought="First, I need to understand the problem requirements",
    thoughtNumber=1,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# Continue the sequence
result = sequential_thinking(
    thought="Now let's identify the key constraints",
    thoughtNumber=2,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# Revise a previous thought
result = sequential_thinking(
    thought="Actually, I need to reconsider the requirements more carefully",
    thoughtNumber=3,
    totalThoughts=5,
    nextThoughtNeeded=True,
    isRevision=True,
    revisesThought=1
)
```

### `get_thought_history()`

Retrieve the complete thought history for a session.

**Parameters:**
- `session_id` (string, optional) - Session identifier
- `include_branches` (boolean) - Include branch information (default: true)

**Returns:** Complete thought history with metadata

### `clear_history()`

Clear the thought history for a session (useful for starting fresh).

**Parameters:**
- `session_id` (string, optional) - Session identifier to clear

### `export_thinking_session()`

Export a thinking session to a file for review or documentation.

**Parameters:**
- `session_id` (string, optional) - Session identifier
- `format` (string) - Export format: 'json' or 'markdown' (default: 'json')

**Returns:** Path to the exported file

## Common Workflows

### Basic Sequential Thinking

```python
# Thought 1
sequential_thinking(
    thought="Understanding the problem scope",
    thoughtNumber=1,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# Thought 2
sequential_thinking(
    thought="Identifying key requirements",
    thoughtNumber=2,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# ... continue through thoughts 3-4 ...

# Final thought
sequential_thinking(
    thought="Synthesizing the solution",
    thoughtNumber=5,
    totalThoughts=5,
    nextThoughtNeeded=False  # Done!
)
```

### Dynamic Expansion

```python
# Start with initial estimate
sequential_thinking(
    thought="Analyzing the data structure",
    thoughtNumber=1,
    totalThoughts=3,
    nextThoughtNeeded=True
)

# Realize more thoughts are needed
sequential_thinking(
    thought="Wait, this is more complex than expected",
    thoughtNumber=4,
    totalThoughts=6,  # Expanded estimate
    nextThoughtNeeded=True,
    needsMoreThoughts=True
)
```

### Revision and Refinement

```python
# Original thought
sequential_thinking(
    thought="The solution requires approach A",
    thoughtNumber=3,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# Later, revise it
sequential_thinking(
    thought="Actually, approach B is better because...",
    thoughtNumber=4,
    totalThoughts=5,
    nextThoughtNeeded=True,
    isRevision=True,
    revisesThought=3
)
```

### Exploring Alternatives

```python
# Main thinking path
sequential_thinking(
    thought="Primary solution using method X",
    thoughtNumber=3,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# Explore alternative branch
sequential_thinking(
    thought="Alternative solution using method Y",
    thoughtNumber=3,
    totalThoughts=5,
    nextThoughtNeeded=True,
    branchFromThought=2,
    branchId="alternative-approach"
)
```

### Multiple Sessions

```python
# Session for problem A
sequential_thinking(
    thought="Analyzing problem A",
    thoughtNumber=1,
    totalThoughts=3,
    nextThoughtNeeded=True,
    session_id="problem_a"
)

# Separate session for problem B
sequential_thinking(
    thought="Analyzing problem B",
    thoughtNumber=1,
    totalThoughts=4,
    nextThoughtNeeded=True,
    session_id="problem_b"
)
```

## Best Practices

1. **Start with a reasonable estimate** - Don't worry about perfection, you can adjust with `needsMoreThoughts`

2. **Use descriptive thoughts** - Clear reasoning steps help track your logic

3. **Embrace revision** - Don't hesitate to revise when you gain new insights

4. **Branch thoughtfully** - Use branches for genuinely different approaches, not minor variations

5. **Session management** - Use different session IDs for unrelated problems

6. **Export important sessions** - Save significant thinking processes for documentation

7. **Progress tracking** - Pay attention to the progress percentage to gauge how far along you are

## Implementation Notes

- **State Management:** Thoughts are stored in memory per session
- **Thread-Safe:** Safe for concurrent use across different sessions
- **Export Formats:** Supports JSON (for data) and Markdown (for readability)
- **Automatic Cleanup:** Old sessions can be cleared with `clear_history()`
- **Branching:** Unlimited branches supported, each tracked independently

## Example Use Cases

### Software Architecture Design
```python
# Thought 1: Understand requirements
# Thought 2: Consider scalability needs
# Thought 3: Evaluate database options
# Thought 4: Design API structure
# Thought 5 (Branch A): Microservices approach
# Thought 5 (Branch B): Monolithic approach
# Thought 6: Compare trade-offs and decide
```

### Research Analysis
```python
# Thought 1: Frame the research question
# Thought 2: Identify relevant literature
# Thought 3: Analyze methodology
# Thought 4 (Revision of 2): Expand literature search
# Thought 5: Synthesize findings
# Thought 6: Draw conclusions
```

### Problem Debugging
```python
# Thought 1: Identify the bug symptoms
# Thought 2: Analyze recent changes
# Thought 3: Hypothesis about root cause
# Thought 4: Test hypothesis
# Thought 5 (Revision of 3): Alternative hypothesis
# Thought 6: Implement fix
```

## Bundled Scripts

- `scripts/sequential_thinking.py` - Main implementation with full Sequential Thinking functionality
- Command-line interface for direct tool invocation

## Differences from Original MCP Server

This skill replicates the functionality of the original MCP server with these enhancements:

1. **Session Management** - Multiple concurrent thinking sessions
2. **Export Capabilities** - Save sessions as JSON or Markdown
3. **History Retrieval** - Query thought history programmatically
4. **Enhanced Metadata** - Progress percentages and statistics
5. **Python Native** - No Node.js/npm dependencies required

## Tips for Effective Use

- **Think out loud** - Use the tool to externalize your reasoning process
- **Iterate freely** - Don't aim for perfection on the first pass
- **Branch strategically** - Explore major alternatives, not every tiny variation
- **Document decisions** - Export important thinking sessions for team review
- **Pattern recognition** - Review exported sessions to identify your thinking patterns

## Limitations

- Thoughts are stored in memory only (not persisted between Claude sessions)
- No built-in visualization of thought trees (use export to Markdown for readable format)
- Branch comparisons require manual review of exported data

## Further Reading

- Original MCP Server: https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking
- Model Context Protocol: https://modelcontextprotocol.io
- Sequential Thinking Patterns: See `references/thinking_patterns.md`
