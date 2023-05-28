import csv
import io

from rich.table import Table
from rich.syntax import Syntax

from textual.app import App, ComposeResult
from textual import events
from textual.widgets import TextLog

from contextlib import redirect_stdout

import sys
import asyncio


class TextLogApp(App):
    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Table.grid(expand=True)

        # yield TextLog(highlight=True, markup=True)
    
    def write(self, s):
        self.text_log.write(Syntax(s, "python", indent_guides=True))
    
    def flush(self):
        # we need this method to ensure compatibility with certain environments (like Jupyter)
        pass
         
    def on_ready(self) -> None:
        self.text_log = self.query_one(TextLog)

    def on_key(self, event: events.Key) -> None:
        """Write Key events to log."""
        pass


async def main():
    app = TextLogApp()
    # run async code
    task = asyncio.create_task(app.run_async())

    # wait for the app to be ready
    await asyncio.sleep(0.1)

    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = app
    sys.stderr = app

    while True:
        print("You entered")
        print("DUMMY Error", file=sys.stderr)
        await asyncio.sleep(1)

    await task

if __name__ == "__main__":
    asyncio.run(main())
