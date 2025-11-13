#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Memory knowledge graph implementation for Claude Code skills.
Auto-generated from @modelcontextprotocol/server-memory MCP server.

Provides persistent memory using a local knowledge graph stored in JSONL format.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


# Default storage location
DEFAULT_MEMORY_FILE = Path.home() / ".claude" / "memory" / "graph.jsonl"
MEMORY_FILE = Path(os.environ.get("MEMORY_FILE_PATH", str(DEFAULT_MEMORY_FILE)))


class KnowledgeGraph:
    """Knowledge graph for storing entities, relations, and observations."""

    def __init__(self, file_path: Path = MEMORY_FILE):
        self.file_path = file_path
        self.entities = {}
        self.relations = []
        self._load()

    def _load(self):
        """Load graph from JSONL file."""
        if not self.file_path.exists():
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        if data['type'] == 'entity':
                            self.entities[data['name']] = {
                                'entityType': data['entityType'],
                                'observations': data['observations']
                            }
                        elif data['type'] == 'relation':
                            self.relations.append({
                                'from': data['from'],
                                'to': data['to'],
                                'relationType': data['relationType']
                            })
        except Exception as e:
            print(f"Warning: Could not load memory file: {e}", file=sys.stderr)

    def _save(self):
        """Save graph to JSONL file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                # Write entities
                for name, data in self.entities.items():
                    f.write(json.dumps({
                        'type': 'entity',
                        'name': name,
                        'entityType': data['entityType'],
                        'observations': data['observations']
                    }) + '\n')

                # Write relations
                for relation in self.relations:
                    f.write(json.dumps({
                        'type': 'relation',
                        'from': relation['from'],
                        'to': relation['to'],
                        'relationType': relation['relationType']
                    }) + '\n')
        except Exception as e:
            raise Exception(f"Failed to save memory: {e}")

    def create_entities(self, entities: List[Dict[str, Any]]):
        """Create new entities."""
        for entity in entities:
            name = entity['name']
            if name in self.entities:
                raise ValueError(f"Entity already exists: {name}")
            self.entities[name] = {
                'entityType': entity['entityType'],
                'observations': entity.get('observations', [])
            }
        self._save()

    def create_relations(self, relations: List[Dict[str, str]]):
        """Create new relations."""
        for relation in relations:
            # Verify entities exist
            if relation['from'] not in self.entities:
                raise ValueError(f"Entity not found: {relation['from']}")
            if relation['to'] not in self.entities:
                raise ValueError(f"Entity not found: {relation['to']}")

            # Check for duplicate
            exists = any(
                r['from'] == relation['from'] and
                r['to'] == relation['to'] and
                r['relationType'] == relation['relationType']
                for r in self.relations
            )
            if exists:
                raise ValueError(f"Relation already exists: {relation}")

            self.relations.append(relation)
        self._save()

    def add_observations(self, entity_name: str, observations: List[str]):
        """Add observations to an entity."""
        if entity_name not in self.entities:
            raise ValueError(f"Entity not found: {entity_name}")

        self.entities[entity_name]['observations'].extend(observations)
        self._save()

    def delete_entities(self, entity_names: List[str]):
        """Delete entities and their relations."""
        for name in entity_names:
            if name in self.entities:
                del self.entities[name]

                # Remove relations involving this entity
                self.relations = [
                    r for r in self.relations
                    if r['from'] != name and r['to'] != name
                ]
        self._save()

    def delete_observations(self, entity_name: str, observations: List[str]):
        """Delete specific observations from an entity."""
        if entity_name not in self.entities:
            raise ValueError(f"Entity not found: {entity_name}")

        entity = self.entities[entity_name]
        entity['observations'] = [
            obs for obs in entity['observations']
            if obs not in observations
        ]
        self._save()

    def delete_relations(self, relations: List[Dict[str, str]]):
        """Delete specific relations."""
        for relation in relations:
            self.relations = [
                r for r in self.relations
                if not (r['from'] == relation['from'] and
                       r['to'] == relation['to'] and
                       r['relationType'] == relation['relationType'])
            ]
        self._save()

    def read_graph(self) -> Dict[str, Any]:
        """Get complete graph structure."""
        return {
            'entities': [
                {'name': name, **data}
                for name, data in self.entities.items()
            ],
            'relations': self.relations
        }

    def search_nodes(self, query: str) -> List[Dict[str, Any]]:
        """Search for entities by query string."""
        query_lower = query.lower()
        results = []

        for name, data in self.entities.items():
            # Search in name
            if query_lower in name.lower():
                results.append({'name': name, **data, 'match': 'name'})
                continue

            # Search in entity type
            if query_lower in data['entityType'].lower():
                results.append({'name': name, **data, 'match': 'type'})
                continue

            # Search in observations
            for obs in data['observations']:
                if query_lower in obs.lower():
                    results.append({'name': name, **data, 'match': 'observation'})
                    break

        return results

    def open_nodes(self, names: List[str]) -> List[Dict[str, Any]]:
        """Get detailed information about specific entities."""
        results = []

        for name in names:
            if name not in self.entities:
                continue

            entity = {'name': name, **self.entities[name]}

            # Add relations
            entity['relations_from'] = [
                r for r in self.relations if r['from'] == name
            ]
            entity['relations_to'] = [
                r for r in self.relations if r['to'] == name
            ]

            results.append(entity)

        return results


# Tool implementations

def create_entities(entities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create new entities in the knowledge graph.

    Args:
        entities: List of entities with name, entityType, and observations

    Returns:
        Result of the operation
    """
    try:
        graph = KnowledgeGraph()
        graph.create_entities(entities)

        return {
            'status': 'success',
            'tool': 'create_entities',
            'created': len(entities),
            'entities': [e['name'] for e in entities]
        }
    except Exception as e:
        return {
            'status': 'error',
            'tool': 'create_entities',
            'message': str(e)
        }


def create_relations(relations: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Create relations between existing entities.

    Args:
        relations: List of relations with from, to, and relationType

    Returns:
        Result of the operation
    """
    try:
        graph = KnowledgeGraph()
        graph.create_relations(relations)

        return {
            'status': 'success',
            'tool': 'create_relations',
            'created': len(relations),
            'relations': relations
        }
    except Exception as e:
        return {
            'status': 'error',
            'tool': 'create_relations',
            'message': str(e)
        }


def add_observations(entity_name: str, observations: List[str]) -> Dict[str, Any]:
    """
    Add observations to an existing entity.

    Args:
        entity_name: Name of the entity
        observations: List of observation strings to add

    Returns:
        Result of the operation
    """
    try:
        graph = KnowledgeGraph()
        graph.add_observations(entity_name, observations)

        return {
            'status': 'success',
            'tool': 'add_observations',
            'entity': entity_name,
            'added': len(observations)
        }
    except Exception as e:
        return {
            'status': 'error',
            'tool': 'add_observations',
            'message': str(e)
        }


def delete_entities(entity_names: List[str]) -> Dict[str, Any]:
    """
    Delete entities and their relations.

    Args:
        entity_names: List of entity names to delete

    Returns:
        Result of the operation
    """
    try:
        graph = KnowledgeGraph()
        graph.delete_entities(entity_names)

        return {
            'status': 'success',
            'tool': 'delete_entities',
            'deleted': len(entity_names),
            'entities': entity_names
        }
    except Exception as e:
        return {
            'status': 'error',
            'tool': 'delete_entities',
            'message': str(e)
        }


def delete_observations(entity_name: str, observations: List[str]) -> Dict[str, Any]:
    """
    Delete specific observations from an entity.

    Args:
        entity_name: Name of the entity
        observations: List of observation strings to remove

    Returns:
        Result of the operation
    """
    try:
        graph = KnowledgeGraph()
        graph.delete_observations(entity_name, observations)

        return {
            'status': 'success',
            'tool': 'delete_observations',
            'entity': entity_name,
            'deleted': len(observations)
        }
    except Exception as e:
        return {
            'status': 'error',
            'tool': 'delete_observations',
            'message': str(e)
        }


def delete_relations(relations: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Delete specific relations.

    Args:
        relations: List of relations to delete

    Returns:
        Result of the operation
    """
    try:
        graph = KnowledgeGraph()
        graph.delete_relations(relations)

        return {
            'status': 'success',
            'tool': 'delete_relations',
            'deleted': len(relations),
            'relations': relations
        }
    except Exception as e:
        return {
            'status': 'error',
            'tool': 'delete_relations',
            'message': str(e)
        }


def read_graph() -> Dict[str, Any]:
    """
    Read the complete knowledge graph.

    Returns:
        Complete graph structure
    """
    try:
        graph = KnowledgeGraph()
        data = graph.read_graph()

        return {
            'status': 'success',
            'tool': 'read_graph',
            'entity_count': len(data['entities']),
            'relation_count': len(data['relations']),
            'graph': data
        }
    except Exception as e:
        return {
            'status': 'error',
            'tool': 'read_graph',
            'message': str(e)
        }


def search_nodes(query: str) -> Dict[str, Any]:
    """
    Search for entities matching a query.

    Args:
        query: Search term

    Returns:
        Matching entities
    """
    try:
        graph = KnowledgeGraph()
        results = graph.search_nodes(query)

        return {
            'status': 'success',
            'tool': 'search_nodes',
            'query': query,
            'count': len(results),
            'results': results
        }
    except Exception as e:
        return {
            'status': 'error',
            'tool': 'search_nodes',
            'message': str(e)
        }


def open_nodes(names: List[str]) -> Dict[str, Any]:
    """
    Get detailed information about specific entities.

    Args:
        names: List of entity names to retrieve

    Returns:
        Entity details with relations
    """
    try:
        graph = KnowledgeGraph()
        results = graph.open_nodes(names)

        return {
            'status': 'success',
            'tool': 'open_nodes',
            'requested': len(names),
            'found': len(results),
            'nodes': results
        }
    except Exception as e:
        return {
            'status': 'error',
            'tool': 'open_nodes',
            'message': str(e)
        }


# CLI interface for testing
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python memory_tools.py <tool_name> [args...]")
        sys.exit(1)

    tool_name = sys.argv[1].replace('-', '_')
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    # Map CLI tools to functions
    tools = {
        'create_entities': create_entities,
        'create_relations': create_relations,
        'add_observations': add_observations,
        'delete_entities': delete_entities,
        'delete_observations': delete_observations,
        'delete_relations': delete_relations,
        'read_graph': read_graph,
        'search_nodes': search_nodes,
        'open_nodes': open_nodes,
    }

    if tool_name not in tools:
        print(f"Unknown tool: {tool_name}")
        print(f"Available tools: {', '.join(tools.keys())}")
        sys.exit(1)

    # Parse JSON args if provided
    if args:
        try:
            parsed_args = [json.loads(arg) for arg in args]
            result = tools[tool_name](*parsed_args)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            sys.exit(1)
    else:
        result = tools[tool_name]()

    print(json.dumps(result, indent=2))
