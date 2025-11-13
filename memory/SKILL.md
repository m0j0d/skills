---
name: memory
description: Knowledge graph-based persistent memory for retaining information across conversations. Store entities, relations, and observations to remember context, preferences, and facts.
---

# Memory - Knowledge Graph Persistence

Persistent memory system using a local knowledge graph. Enables AI to remember information about users, projects, preferences, and relationships across conversations.

**Based on:** Official MCP memory server (@modelcontextprotocol/server-memory)

## When to Use

- Remember user preferences and context
- Track project information and relationships
- Store facts about people, organizations, events
- Build persistent knowledge over time
- Recall information from previous conversations

## Tools

### Knowledge Graph Structure

The memory system uses three core concepts:

**Entities**: Primary nodes with names, types, and observations
- Example: "John_Smith" (type: "person")

**Relations**: Directed connections between entities (active voice)
- Example: John_Smith → Anthropic (relation: "works_at")

**Observations**: Atomic facts attached to entities
- Example: ["Prefers Python", "Lives in San Francisco"]

### create_entities

Create new entities in the knowledge graph.

**Parameters:**
- `entities` (array, required): List of entities to create
  - `name` (string, required): Unique identifier
  - `entityType` (string, required): Classification (person, organization, event, etc.)
  - `observations` (array, required): List of fact strings

**Example:**
```python
create_entities(entities=[
    {
        "name": "User_Example",
        "entityType": "person",
        "observations": [
            "Works on MCP-to-skills project",
            "Prefers evidence-based development",
            "Uses Claude Code for development"
        ]
    }
])
```

### create_relations

Establish directed connections between existing entities.

**Parameters:**
- `relations` (array, required): List of relations to create
  - `from` (string, required): Source entity name
  - `to` (string, required): Target entity name
  - `relationType` (string, required): Relationship type (active voice)

**Example:**
```python
create_relations(relations=[
    {
        "from": "User_Example",
        "to": "mcp-to-skills",
        "relationType": "develops"
    }
])
```

### add_observations

Add new facts to existing entities.

**Parameters:**
- `entityName` (string, required): Target entity
- `observations` (array, required): List of fact strings to add

**Example:**
```python
add_observations(
    entityName="User_Example",
    observations=["Completed MCP protocol research", "Built containerized test infrastructure"]
)
```

### delete_entities

Remove entities and their associated relations.

**Parameters:**
- `entityNames` (array, required): List of entity names to delete

**Example:**
```python
delete_entities(entityNames=["Old_Project", "Deprecated_Tool"])
```

### delete_observations

Remove specific facts from entities.

**Parameters:**
- `entityName` (string, required): Target entity
- `observations` (array, required): Exact fact strings to remove

**Example:**
```python
delete_observations(
    entityName="User_Example",
    observations=["Old preference"]
)
```

### delete_relations

Remove specific connections between entities.

**Parameters:**
- `relations` (array, required): Relations to delete
  - `from` (string, required): Source entity
  - `to` (string, required): Target entity
  - `relationType` (string, required): Relationship type

**Example:**
```python
delete_relations(relations=[
    {
        "from": "User_Example",
        "to": "old_project",
        "relationType": "worked_on"
    }
])
```

### read_graph

Export the complete knowledge graph structure.

**Parameters:** None

**Returns:** Complete graph with all entities, relations, and observations

**Example:**
```python
graph = read_graph()
# Returns: {"entities": [...], "relations": [...]}
```

### search_nodes

Query entities by name, type, or observation content.

**Parameters:**
- `query` (string, required): Search term

**Returns:** Entities matching the search criteria

**Example:**
```python
search_nodes(query="Python")
# Returns entities with "Python" in name, type, or observations
```

### open_nodes

Retrieve specific entities with their full context and connections.

**Parameters:**
- `names` (array, required): Entity names to retrieve

**Returns:** Entities with their observations and relations

**Example:**
```python
open_nodes(names=["User_Example", "mcp-to-skills"])
# Returns full details and interconnections
```

## Usage Patterns

### Starting Conversations

Begin by retrieving relevant context:
```python
# Search for relevant information
results = search_nodes(query="user preferences")

# Open specific entities
context = open_nodes(names=["Current_Project"])
```

### Storing New Information

Monitor conversations for facts to remember:
```python
# Create new entity
create_entities(entities=[{
    "name": "New_Feature",
    "entityType": "feature",
    "observations": ["Requested by user", "High priority"]
}])

# Link to existing entities
create_relations(relations=[{
    "from": "Current_Project",
    "to": "New_Feature",
    "relationType": "includes"
}])
```

### Updating Information

Add or remove facts as context evolves:
```python
# Add new observations
add_observations(
    entityName="User",
    observations=["Prefers detailed commit messages"]
)

# Remove outdated facts
delete_observations(
    entityName="User",
    observations=["Old preference"]
)
```

## Best Practices

### Entity Naming
- Use underscores for multi-word names: `John_Smith`, `Project_X`
- Keep names unique and descriptive
- Avoid special characters

### Entity Types
- Use consistent classifications: "person", "organization", "project", "feature", "tool"
- Keep types generic for flexibility

### Relations
- Always use active voice: "works_at", "develops", "includes", "uses"
- Be specific: "manages" vs "works_on"
- Avoid passive voice: "managed_by" ❌ → "manages" ✅

### Observations
- Keep facts atomic (one fact per observation)
- Use complete sentences or clear phrases
- Be specific: "Prefers Python 3.11+" vs "Likes Python"
- Include context: "Completed MCP research on 2025-10-23"

### Search Strategy
- Start with broad search, then refine
- Use `search_nodes` for discovery
- Use `open_nodes` for detailed retrieval
- Regularly prune outdated information

## Configuration

The memory server stores data in a local JSONL file. Default location can be customized via `MEMORY_FILE_PATH` environment variable.

**Storage location:**
- Default: `~/.mcp/memory/graph.jsonl`
- Custom: Set via environment variable

## License

MIT (matches official MCP server license)

## Related

- **filesystem** - File operations for local data
- **sequential-thinking** - Structured problem-solving
- **fetch** - Web research and content retrieval
