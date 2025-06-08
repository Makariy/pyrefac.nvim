import subprocess


class PyrefacFormatter:
    def __init__(self, format_command: str | None) -> None:
        self._format_command = format_command

    def is_format_enabled(self) -> bool:
        return self._format_command is not None

    def run_format_files(self, files: list[str], cwd: str) -> None:
        assert self._format_command is not None
        rendered_files = " ".join(files)

        result = subprocess.run(
            self._format_command.format(rendered_files).split(),
            text=True,
            capture_output=True,
            cwd=cwd,
        )
        output = result.stderr
        if output:
            raise RuntimeError(output)
