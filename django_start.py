import sys
import socket

sys.argv.append("runserver")
ipPort = "%s:%d" % (socket.gethostbyname(socket.gethostname()), 8000)

sys.argv.append(ipPort)
sys.argv.append("--noreload")

from django.core.management import execute_manager

import settings # Assumed to be in the same directory.
execute_manager(settings)

# so we can see any error
raw_input()
