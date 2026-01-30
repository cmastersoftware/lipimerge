from rich.console import Console
from rich.progress import track as rich_track

_console = Console()

def print(*args, **kwargs):
    _console.print(*args, **kwargs)

def track(iterable, description: str):
    return rich_track(iterable, description.ljust(30))