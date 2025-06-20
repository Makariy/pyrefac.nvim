from typing import Any, cast
import pynvim
import move_executor


@pynvim.plugin
class PyrefacPlugin:
    def __init__(self, nvim: pynvim.Nvim):
        self._nvim = nvim
        self._config: dict[str, str] = cast(
            dict[str, Any],
            self._nvim.vars.get("pyrefac_config") or {"pyrefac_command": "pyrefac"},
        )

    @pynvim.command("PyrefacMove", range=True, sync=True)
    def process_selected_code_command(
        self,
        selection: tuple[int, int],
    ):
        try:
            move_executor.PyrefacMoveExecutor(
                nvim=self._nvim,
                pyrefac_command=self._config["pyrefac_command"],
                format_command=self._config.get("format_command"),
            ).execute(selection)
        except Exception as e:
            self._nvim.err_write(f"\nAn error occured performing move: {e}\n")
