import os
from pathlib import Path
from agent.tools import Tool

# Safety: all paths must resolve within user's home directory
HOME_DIR = str(Path.home())


def _safe_path(path: str) -> str:
    """Resolve path and ensure it's within the user's home directory."""
    resolved = os.path.realpath(os.path.expanduser(path))
    if not resolved.startswith(HOME_DIR):
        raise PermissionError(f"Access denied: path must be within {HOME_DIR}")
    return resolved


class ReadFileTool(Tool):
    def __init__(self):
        super().__init__(
            name='read_file',
            description='Read the contents of a file. Path must be within your home directory.',
            parameters={
                'path': {'type': 'string', 'description': 'File path (absolute or ~/ relative)'},
                'max_lines': {'type': 'integer', 'default': 100},
            }
        )

    def execute(self, path='', max_lines=100, **kwargs) -> str:
        try:
            safe = _safe_path(path)
            with open(safe, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()[:max_lines]
            content = ''.join(lines)
            total = len(lines)
            if total == max_lines:
                content += f"\n... (showing first {max_lines} lines)"
            return content if content.strip() else '(empty file)'
        except PermissionError as e:
            return str(e)
        except Exception as e:
            return f"Error reading file: {e}"


class WriteFileTool(Tool):
    def __init__(self):
        super().__init__(
            name='write_file',
            description='Write content to a file. Creates parent directories if needed. Path must be within home directory.',
            parameters={
                'path': {'type': 'string', 'description': 'File path (absolute or ~/ relative)'},
                'content': {'type': 'string', 'description': 'Content to write'},
            }
        )

    def execute(self, path='', content='', **kwargs) -> str:
        try:
            safe = _safe_path(path)
            os.makedirs(os.path.dirname(safe), exist_ok=True)
            with open(safe, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"File written: {safe} ({len(content)} chars)"
        except PermissionError as e:
            return str(e)
        except Exception as e:
            return f"Error writing file: {e}"


class ListFilesTool(Tool):
    def __init__(self):
        super().__init__(
            name='list_files',
            description='List files and directories at a given path. Path must be within home directory.',
            parameters={
                'path': {'type': 'string', 'description': 'Directory path (absolute or ~/ relative)'},
                'max_items': {'type': 'integer', 'default': 50},
            }
        )

    def execute(self, path='', max_items=50, **kwargs) -> str:
        try:
            safe = _safe_path(path)
            if not os.path.isdir(safe):
                return f"Not a directory: {safe}"
            entries = sorted(os.listdir(safe))[:max_items]
            lines = []
            for entry in entries:
                full = os.path.join(safe, entry)
                marker = '/' if os.path.isdir(full) else ''
                lines.append(f"  {entry}{marker}")
            header = f"Contents of {safe} ({len(entries)} items):"
            return header + '\n' + '\n'.join(lines)
        except PermissionError as e:
            return str(e)
        except Exception as e:
            return f"Error listing files: {e}"
