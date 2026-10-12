from .atlogger import *
from .handlers.wandbhandler import WandbHandler
__all__ = [
  "log","logger",
  "PROD","STAGE","TEST","DEV","DEBUG",
  "WandbHandler"]

def main() -> None:
  print("Hello from atlog!")
