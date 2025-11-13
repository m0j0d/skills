#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Sequential Thinking - Dynamic and Reflective Problem-Solving

This module provides a Python implementation of the Sequential Thinking MCP server,
enabling structured, step-by-step reasoning with revision and branching capabilities.

Originally from: @modelcontextprotocol/server-sequential-thinking
Converted to Python skill for Claude.ai
"""

import json
import sys
from typing import Dict, List, Any, Optional, TypedDict
from dataclasses import dataclass, asdict, field
from datetime import datetime
import os


class ThoughtData(TypedDict):
    """Structure for a single thought in the sequence."""
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


@dataclass
class SequentialThinkingState:
    """Maintains the state of the sequential thinking process."""
    thoughtHistory: List[ThoughtData] = field(default_factory=list)
    branches: Dict[str, List[ThoughtData]] = field(default_factory=dict)
    currentBranch: str = "main"
    sessionId: str = ""
    
    def __post_init__(self):
        if not self.sessionId:
            self.sessionId = datetime.now().strftime("%Y%m%d_%H%M%S")


# Global state management
_state_store: Dict[str, SequentialThinkingState] = {}


def get_state(session_id: Optional[str] = None) -> SequentialThinkingState:
    """Get or create a session state."""
    if session_id is None:
        session_id = "default"
    
    if session_id not in _state_store:
        _state_store[session_id] = SequentialThinkingState(sessionId=session_id)
    
    return _state_store[session_id]


def clear_history(session_id: Optional[str] = None) -> Dict[str, Any]:
    """Clear the thought history for a session."""
    if session_id is None:
        session_id = "default"
    
    if session_id in _state_store:
        del _state_store[session_id]
    
    return {
        "status": "success",
        "message": f"History cleared for session: {session_id}",
        "session_id": session_id
    }


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
) -> Dict[str, Any]:
    """
    Process a thought in a sequential thinking chain.
    
    This function enables dynamic and reflective problem-solving through a structured
    thinking process. It maintains a history of thoughts and supports:
    - Sequential step-by-step reasoning
    - Revision of previous thoughts
    - Branching to explore alternative approaches
    - Dynamic adjustment of total thought count
    
    Args:
        thought: Your current thinking step
        thoughtNumber: Current thought number (starting from 1)
        totalThoughts: Estimated total thoughts needed
        nextThoughtNeeded: Whether another thought step is needed (only false when done)
        isRevision: Whether this revises previous thinking
        revisesThought: Which thought number is being reconsidered
        branchFromThought: Which thought to branch from for alternatives
        branchId: Identifier for the new branch
        needsMoreThoughts: Whether more thoughts than initially planned are needed
        session_id: Optional session identifier for managing multiple thinking sessions
    
    Returns:
        Dictionary containing:
        - status: Operation status
        - thoughtNumber: Current thought number
        - totalThoughts: Total thoughts in sequence
        - thoughtsSoFar: Number of thoughts recorded
        - nextThoughtNeeded: Whether another thought is needed
        - isRevision: Whether this was a revision
        - branchInfo: Information about current branch (if applicable)
        - summary: Brief summary of the thinking process
    """
    
    # Get or create session state
    state = get_state(session_id)
    
    # Validate inputs
    if thoughtNumber < 1:
        return {
            "status": "error",
            "message": "thoughtNumber must be >= 1",
            "thoughtNumber": thoughtNumber
        }
    
    if totalThoughts < 1:
        return {
            "status": "error",
            "message": "totalThoughts must be >= 1",
            "totalThoughts": totalThoughts
        }
    
    if thoughtNumber > totalThoughts and not needsMoreThoughts:
        return {
            "status": "error",
            "message": f"thoughtNumber ({thoughtNumber}) exceeds totalThoughts ({totalThoughts}). Set needsMoreThoughts=true to expand the sequence.",
            "thoughtNumber": thoughtNumber,
            "totalThoughts": totalThoughts
        }
    
    # Handle dynamic thought expansion
    if needsMoreThoughts and thoughtNumber > totalThoughts:
        totalThoughts = thoughtNumber
    
    # Create thought data
    thought_data: ThoughtData = {
        "thought": thought,
        "thoughtNumber": thoughtNumber,
        "totalThoughts": totalThoughts,
        "nextThoughtNeeded": nextThoughtNeeded,
        "isRevision": isRevision if isRevision else None,
        "revisesThought": revisesThought,
        "branchFromThought": branchFromThought,
        "branchId": branchId,
        "needsMoreThoughts": needsMoreThoughts if needsMoreThoughts else None,
        "timestamp": datetime.now().isoformat()
    }
    
    # Handle branching
    if branchFromThought is not None and branchId:
        if branchId not in state.branches:
            state.branches[branchId] = []
        state.branches[branchId].append(thought_data)
        state.currentBranch = branchId
    else:
        state.thoughtHistory.append(thought_data)
        state.currentBranch = "main"
    
    # Prepare response
    thoughts_so_far = len(state.thoughtHistory)
    
    response = {
        "status": "success",
        "thoughtNumber": thoughtNumber,
        "totalThoughts": totalThoughts,
        "thoughtsSoFar": thoughts_so_far,
        "nextThoughtNeeded": nextThoughtNeeded,
        "progress": f"{thoughtNumber}/{totalThoughts}",
        "progressPercentage": round((thoughtNumber / totalThoughts) * 100, 1),
        "session_id": state.sessionId
    }
    
    # Add revision info
    if isRevision and revisesThought is not None:
        response["isRevision"] = True
        response["revisesThought"] = revisesThought
        response["revisionNote"] = f"Reconsidering thought #{revisesThought}"
    
    # Add branch info
    if branchId:
        response["branchInfo"] = {
            "branchId": branchId,
            "branchFromThought": branchFromThought,
            "branchLength": len(state.branches.get(branchId, []))
        }
        response["currentBranch"] = branchId
    else:
        response["currentBranch"] = "main"
    
    # Add summary if complete
    if not nextThoughtNeeded:
        response["summary"] = f"Completed sequential thinking with {thoughts_so_far} thoughts"
        response["complete"] = True
        
        # Count revisions and branches
        revisions = sum(1 for t in state.thoughtHistory if t.get("isRevision"))
        branches = len(state.branches)
        
        response["statistics"] = {
            "totalThoughts": thoughts_so_far,
            "revisions": revisions,
            "branches": branches,
            "finalThoughtNumber": thoughtNumber
        }
    else:
        response["complete"] = False
        response["nextAction"] = f"Continue with thought #{thoughtNumber + 1}"
    
    return response


def get_thought_history(
    session_id: Optional[str] = None,
    include_branches: bool = True
) -> Dict[str, Any]:
    """
    Retrieve the thought history for a session.
    
    Args:
        session_id: Optional session identifier
        include_branches: Whether to include branch information
    
    Returns:
        Dictionary containing the complete thought history
    """
    state = get_state(session_id)
    
    result = {
        "status": "success",
        "session_id": state.sessionId,
        "thoughtCount": len(state.thoughtHistory),
        "thoughts": state.thoughtHistory
    }
    
    if include_branches and state.branches:
        result["branches"] = state.branches
        result["branchCount"] = len(state.branches)
    
    return result


def export_thinking_session(
    session_id: Optional[str] = None,
    format: str = "json"
) -> str:
    """
    Export a thinking session to a file.
    
    Args:
        session_id: Optional session identifier
        format: Export format ('json' or 'markdown')
    
    Returns:
        Path to the exported file
    """
    state = get_state(session_id)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"thinking_session_{state.sessionId}_{timestamp}"
    
    if format == "json":
        filename += ".json"
        filepath = os.path.join("/tmp", filename)
        
        export_data = {
            "session_id": state.sessionId,
            "exported_at": datetime.now().isoformat(),
            "thought_history": state.thoughtHistory,
            "branches": state.branches
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    elif format == "markdown":
        filename += ".md"
        filepath = os.path.join("/tmp", filename)
        
        lines = [
            f"# Sequential Thinking Session",
            f"**Session ID:** {state.sessionId}",
            f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Thoughts:** {len(state.thoughtHistory)}",
            "",
            "## Thought Sequence",
            ""
        ]
        
        for i, thought_data in enumerate(state.thoughtHistory, 1):
            lines.append(f"### Thought {thought_data['thoughtNumber']}")
            lines.append(f"**Progress:** {thought_data['thoughtNumber']}/{thought_data['totalThoughts']}")
            
            if thought_data.get('isRevision'):
                lines.append(f"**Type:** Revision of thought #{thought_data.get('revisesThought')}")
            
            lines.append("")
            lines.append(thought_data['thought'])
            lines.append("")
        
        # Add branches
        if state.branches:
            lines.append("## Alternative Branches")
            lines.append("")
            for branch_id, branch_thoughts in state.branches.items():
                lines.append(f"### Branch: {branch_id}")
                lines.append(f"**Thoughts:** {len(branch_thoughts)}")
                lines.append("")
                for thought_data in branch_thoughts:
                    lines.append(f"- **Thought {thought_data['thoughtNumber']}:** {thought_data['thought'][:100]}...")
                lines.append("")
        
        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))
    
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    return filepath


# CLI interface
if __name__ == "__main__":
    """Command-line interface for Sequential Thinking tools."""
    
    if len(sys.argv) < 2:
        print("Sequential Thinking - Dynamic Problem-Solving Tool")
        print("=" * 50)
        print("\nUsage: python sequential_thinking.py <command> [options]")
        print("\nCommands:")
        print("  think        - Process a thought in the sequence")
        print("  history      - View thought history")
        print("  clear        - Clear thought history")
        print("  export       - Export thinking session")
        print("\nExample:")
        print('  python sequential_thinking.py think --thought "First step" --thoughtNumber 1 --totalThoughts 5 --nextThoughtNeeded true')
        sys.exit(1)
    
    command = sys.argv[1]
    
    # Parse parameters
    params = {}
    i = 2
    while i < len(sys.argv):
        if sys.argv[i].startswith('--'):
            param_name = sys.argv[i][2:]
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('--'):
                value = sys.argv[i + 1]
                # Type conversion
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.isdigit():
                    value = int(value)
                params[param_name] = value
                i += 2
            else:
                params[param_name] = True
                i += 1
        else:
            i += 1
    
    # Execute command
    try:
        if command == "think":
            result = sequential_thinking(**params)
        elif command == "history":
            result = get_thought_history(**params)
        elif command == "clear":
            result = clear_history(**params)
        elif command == "export":
            filepath = export_thinking_session(**params)
            result = {"status": "success", "filepath": filepath}
        else:
            print(f"Error: Unknown command '{command}'")
            sys.exit(1)
        
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
