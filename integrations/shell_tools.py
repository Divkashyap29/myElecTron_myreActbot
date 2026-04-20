import subprocess
from agent.tools import Tool

BLOCKED_COMMANDS = [
    'rm', 'rmdir', 'del', 'format', 'shutdown', 'reboot',
    'kill', 'taskkill', 'mkfs', 'dd', 'fdisk',
    'reg delete', 'net user', 'passwd',
]


class RunCommandTool(Tool):
    def __init__(self):
        super().__init__(
            name='run_command',
            description='Run a shell command and return its output. Dangerous commands are blocked.',
            parameters={
                'command': {'type': 'string', 'description': 'Shell command to execute'},
                'timeout': {'type': 'integer', 'default': 30, 'description': 'Timeout in seconds'},
            }
        )

    def execute(self, command='', timeout=30, **kwargs) -> str:
        # Safety check
        cmd_lower = command.lower().strip()
        for blocked in BLOCKED_COMMANDS:
            if cmd_lower.startswith(blocked) or f' {blocked} ' in f' {cmd_lower} ':
                return f"Blocked: '{blocked}' commands are not allowed for safety."

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            output = result.stdout or ''
            if result.stderr:
                output += f"\n[stderr]: {result.stderr}"
            if result.returncode != 0:
                output += f"\n[exit code: {result.returncode}]"
            # Truncate long output
            if len(output) > 3000:
                output = output[:3000] + '\n... (output truncated at 3000 chars)'
            return output.strip() if output.strip() else '(no output)'
        except subprocess.TimeoutExpired:
            return f"Command timed out after {timeout} seconds."
        except Exception as e:
            return f"Error running command: {e}"
