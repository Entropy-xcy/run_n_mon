import csv
import io
import time

from rich.table import Table
from rich.syntax import Syntax
from rich.pretty import Pretty

from textual.app import App, ComposeResult
from textual import events
from textual.widgets import TextLog

import sys
import asyncio

from ui import RNMApp


app = RNMApp()
class StdOutWrapper():
    def __init__(self, app):
        self.app = app

    def write(self, data):
        self.app.write_stdout(data)
    
    def flush(self) -> None:
        pass

class StdErrWrapper():
    def __init__(self, app):
        self.app = app

    def write(self, data):
        self.app.write_stderr(data)
    
    def flush(self) -> None:
        pass

async def main():
    # run async code
    task = asyncio.create_task(app.run_async())

    # wait for the app to be ready
    while not app.ready:
        await asyncio.sleep(0.1)

    # redirect stdout and stderr
    sys.stdout = StdOutWrapper(app)
    sys.stderr = StdErrWrapper(app)

    while True:
        print("This is stdout")
        print("This is stderr", file=sys.stderr)
        await asyncio.sleep(1)

    await task

if __name__ == "__main__":
    asyncio.run(main())
