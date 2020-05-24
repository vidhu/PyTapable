import sys
if sys.version_info[0] < 3:
    from mock import *
else:
    from unittest.mock import *
