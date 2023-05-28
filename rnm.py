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
    def __init__(self, stdout=sys.stdout):
        super().__init__()
        self.stdout = stdout

    def compose(self) -> ComposeResult:
        yield TextLog(highlight=True, markup=True)
    
    def write(self, s):
        self.text_log.write(Syntax(s, "python", indent_guides=True))
    
    def flush(self):
        # we need this method to ensure compatibility with certain environments (like Jupyter)
        pass
         

    def on_ready(self) -> None:
        """Called  when the DOM is ready."""
        self.text_log = self.query_one(TextLog)

        # text_log.write(Syntax(CODE, "python", indent_guides=True))

        # rows = iter(csv.reader(io.StringIO(CSV)))
        # table = Table(*next(rows))
        # for row in rows:
        #     table.add_row(*row)

        # text_log.write(table)
        # text_log.write("[bold magenta]Write text or any Rich renderable!")

    def on_key(self, event: events.Key) -> None:
        """Write Key events to log."""
        text_log = self.query_one(TextLog)
        text_log.write(event)


async def main():
    app = TextLogApp()
    # run async code
    task = asyncio.create_task(app.run_async())

    # wait for the app to be ready
    await asyncio.sleep(0.1)
    original_stdout = sys.stdout
    sys.stdout = app

    while True:
        print("Hello World")
        await asyncio.sleep(1)

    await task

if __name__ == "__main__":
    asyncio.run(main())
