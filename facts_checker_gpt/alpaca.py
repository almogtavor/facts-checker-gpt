import subprocess
import time
from pathlib import Path
from threading import Lock
from typing import Optional


class Alpaca:
    def __init__(self, alpaca_cli_path: Path, model_path: Path):
        self.alpaca_cli_path = alpaca_cli_path
        self.model_path = model_path
        self.process: Optional[subprocess.Popen] = None
        self.system_info: Optional[dict] = None
        self.lock = Lock()
        self.start()
        self._write("")

    def start(self):
        if self.process is not None:
            return
        with self.lock:
            self.process = subprocess.Popen(
                args=[str(self.alpaca_cli_path), "--model", str(self.model_path)],
                text=True,
                bufsize=1,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )

    def _write(self, message: str) -> None:
        self.process.stdin.write(f"{message.strip()}\n")
        self.process.stdin.flush()

    def _read_stdout(self) -> str:
        return self.process.stdout.readline().strip()

    def stop(self):
        with self.lock:
            self._write("quit();")
            time.sleep(3)
            self.process = None

    def run(self, prompt: str) -> str:
        with self.lock:
            self._write(prompt)
            time.sleep(2)
            response = self._read_stdout()
        return response
