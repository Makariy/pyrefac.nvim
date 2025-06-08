from pynvim import Nvim


class NvimFileUpdater:
    def __init__(self, nvim: Nvim) -> None:
        self._nvim = nvim

    def reopen_files(self, files: list[str]) -> None:
        for filename in files:
            self.reopen_file(filename)

    def reopen_file(self, filename: str) -> None:
        buff = self._nvim.eval(f"bufadd('{filename}')")
        if buff == -1:
            self._nvim.out_write(f"\nCould not open {filename}\n")
            return

        self._nvim.command(f"buffer {buff}")
        self._nvim.command("e!")
