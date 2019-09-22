import logging
import sys
from moar_dots import Wipe

log = logging.getLogger()

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(logging.Formatter("%(message)s"))
stdout_handler.setLevel(logging.DEBUG)

log.addHandler(stdout_handler)

log.setLevel(logging.DEBUG)

log.info("Testing a wipe!")
my_wipe = Wipe(
    "KeyError", "This is supposed to tell me wtf went wrong.", "This, too. Supposedly."
)
