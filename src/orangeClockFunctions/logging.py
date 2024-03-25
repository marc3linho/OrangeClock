import uio
import usys
from phew import logging

def log_exception(exception):
    tmp_string = uio.StringIO()
    usys.print_exception(exception, tmp_string)
    logging.exception("> {}".format(
        tmp_string.getvalue().replace("\n", "\\n")
    ))
