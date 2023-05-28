from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, TextLog, Input, Label, ProgressBar, DataTable
from textual.widget import Widget
from rich.text import Text

    
class CPUMonitorWidget(Widget):
    DEFAULT_CSS = """
    CPUMonitorWidget {
        layout: grid;
        grid-size: 2 3;
        grid-rows: 1fr;
        grid-columns: 1fr 2fr;
        height: auto;
    }
    CPUMonitorWidget Label {
        padding: 0;
        width: 100%;
        content-align: center middle;
    }
    CPUMonitorWidget ProgressBar {
        padding: 0;
        content-align: center middle;
    }
    """

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:  
        yield Label("CPU Usage")
        yield ProgressBar(total=100, show_percentage=True, id="cpu_usage")
        yield Label("Mem Usage")
        yield ProgressBar(total=256, show_percentage=True, id="mem_usage")
        yield Label("Swap Usage")
        yield ProgressBar(total=2560, show_percentage=True, id="swap_usage")
    
    def update(self) -> None:
        self.query_one("#cpu_usage", ProgressBar).advance(1)
        self.query_one("#mem_usage", ProgressBar).advance(1)
        self.query_one("#swap_usage", ProgressBar).advance(1)

    def on_mount(self) -> None:
        self.set_interval(1.0, self.update)


class GPUMonitorWidget(Widget):
    DEFAULT_CSS = """
    GPUMonitorWidget {
        layout: vertical;
    }
    GPUMonitorWidget Label {
        padding-left: 1;
        align: center middle;
        width: 50%;
    }
    GPUMonitorWidget ProgressBar {
        padding-left: 1;
        padding-right: 1;
        align: center middle;
        width: 50%;
    }
    """

    def __init__(self, num_gpus: int) -> None:
        super().__init__()
        self.num_gpus = num_gpus

    def compose(self) -> ComposeResult:  
        yield Horizontal(
            Label("GPU Util"),
            Label("VRAM"),
        )
        for i in range(self.num_gpus):
            yield Horizontal(
                ProgressBar(total=100, id=f"gpu{i}"),
                ProgressBar(total=256, id=f"vram{i}"),
            )
    
    def update(self) -> None:
        for i in range(self.num_gpus):
            self.query_one(f"#gpu{i}", ProgressBar).advance(1)
            self.query_one(f"#vram{i}", ProgressBar).advance(1)

    def on_mount(self) -> None:
        self.set_interval(1.0, self.update)


ROWS = [
    ("", "/dev/sda1", "/dev/nvme0n1", "eth0", "lo"),
    ("R/s", "312M/s", "4.8G/s", "10M/s", "1T/s"),
    ("W/s", "1.3K/s", "0.0B/s", "3.0K/s", "1T/s"),
    ("#RX", "10G", "0.2T", "1.2G", "1.2T"),
    ("#TX", "1.2G", "0.1T", "10G", "1.2T"),
    ("Ltc.", "1ms", "8us", "45ms", "100ns"),
]

class IOStatsWidget(Widget):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:  
        yield DataTable()
    
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])
        for row in ROWS[1:]:
            # Adding styled and justified `Text` objects instead of plain strings.
            styled_row = [
                Text(str(cell), style="italic #03AC13", justify="right") for cell in row
            ]
            table.add_row(*styled_row)
    

class RNMApp(App):
    CSS = """
    CPUMonitorWidget {
        content-align: center middle;
        border: solid blue;
        height: 2fr;
    }

    #terminal {
        border: solid green;
    }

    GPUMonitorWidget {
        height: 3fr;
        border: solid red;
    }

    IOStatsWidget {
        height: 2fr;
        border: solid yellow;
    }

    .box {
        height: 100%;
        width: 1fr;
        border: solid green;
    }
    """
    def __init__(self) -> None:
        super().__init__()
        self.ready = False

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                CPUMonitorWidget(),
                GPUMonitorWidget(8),
                IOStatsWidget(),
                classes="column",
            ),
            Vertical(
                TextLog(id="terminal"),
                classes="column",
            ),
        )
    
    def on_ready(self) -> None:
        self.text_log = self.query_one("#terminal", TextLog)
        self.ready = True
    
    def write_stdout(self, data: str) -> None:
        # block until ready
        while not self._ready:
            pass
        self.text_log.write(data)
    
    def write_stderr(self, data: str) -> None:
        while not self._ready:
            pass
        # Write Red text to stderr
        self.text_log.write(data)
    
    # def on_mount(self) -> None:
    #     self.set_interval(1.0, self.update)
    
    # def update(self) -> None:
    #     self.write_stderr("This is stderr\n")
    #     self.write_stdout("This is stdout\n")


if __name__ == "__main__":
    app = RNMApp()
    app.run()
