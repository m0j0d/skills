# Sequential Thinking API Reference

Complete API documentation for all Sequential Thinking functions.

## Core Functions

### sequential_thinking()

Process a thought in a sequential thinking chain with full state management.

#### Signature
```python
def sequential_thinking(
    thought: str,
    thoughtNumber: int,
    totalThoughts: int,
    nextThoughtNeeded: bool,
    isRevision: bool = False,
    revisesThought: Optional[int] = None,
    branchFromThought: Optional[int] = None,
    branchId: Optional[str] = None,
    needsMoreThoughts: bool = False,
    session_id: Optional[str] = None
) -> Dict[str, Any]
```

#### Parameters

**Required:**
- `thought` (str): The current thinking step
- `thoughtNumber` (int): Current thought number (>= 1)
- `totalThoughts` (int): Estimated total thoughts needed (>= 1)
- `nextThoughtNeeded` (bool): Whether another thought is needed

**Optional:**
- `isRevision` (bool): Whether this revises previous thinking
- `revisesThought` (int): Which thought number is being reconsidered
- `branchFromThought` (int): Which thought to branch from
- `branchId` (str): Identifier for the new branch
- `needsMoreThoughts` (bool): Expand beyond initial estimate
- `session_id` (str): Session identifier

#### Returns

Dictionary with status, progress, and metadata about the thinking process.

#### Example Usage

```python
# Basic sequence
result = sequential_thinking(
    thought="Understanding the core requirements",
    thoughtNumber=1,
    totalThoughts=5,
    nextThoughtNeeded=True
)

# With revision
result = sequential_thinking(
    thought="Actually, we need to reconsider the database choice",
    thoughtNumber=4,
    totalThoughts=5,
    nextThoughtNeeded=True,
    isRevision=True,
    revisesThought=2
)
```

### get_thought_history()

Retrieve the complete thought history for a session.

#### Signature
```python
def get_thought_history(
    session_id: Optional[str] = None,
    include_branches: bool = True
) -> Dict[str, Any]
```

### clear_history()

Clear the thought history for a session.

#### Signature
```python
def clear_history(session_id: Optional[str] = None) -> Dict[str, Any]
```

### export_thinking_session()

Export a thinking session to a file.

#### Signature
```python
def export_thinking_session(
    session_id: Optional[str] = None,
    format: str = "json"
) -> str
```

#### Parameters
- `format`: "json" or "markdown"

#### Returns
Path to the exported file.

## Data Structures

### ThoughtData

```python
class ThoughtData(TypedDict):
    thought: str
    thoughtNumber: int
    totalThoughts: int
    nextThoughtNeeded: bool
    isRevision: Optional[bool]
    revisesThought: Optional[int]
    branchFromThought: Optional[int]
    branchId: Optional[str]
    needsMoreThoughts: Optional[bool]
    timestamp: str
```

## Command-Line Interface

```bash
# Process a thought
python sequential_thinking.py think \
    --thought "Analyzing requirements" \
    --thoughtNumber 1 \
    --totalThoughts 5 \
    --nextThoughtNeeded true

# View history
python sequential_thinking.py history --session_id my_session

# Clear history
python sequential_thinking.py clear --session_id my_session

# Export session
python sequential_thinking.py export --format markdown
```
