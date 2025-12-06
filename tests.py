"""
Tests for your Drafter website.
"""

from drafter import *
from bakery import assert_equal

# do_not_start_server(): Prevent the server from starting during tests
get_main_server().configuration.skip = True

from main import *

## You can add your tests below this line

#assert_equal(index(State()), Page(State(), ["Hello World!"]))
