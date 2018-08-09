import sys
from pathlib import Path
from user import UserFactory
from user import User
from user import Comment
import os

# basic platform that is used directly by user or tester.

def validate_cmdline_args(nargs, msg):
    if len(sys.argv) != nargs:
        print(msg)
        sys.exit(1)

validate_cmdline_args(2, "Should provide only one argument, <input file name>")

users = UserFactory().getUsers(sys.argv[1])

for user in users:
	thisUser = users.get(user)
	thisUser.calculateCommentSentiments()
	thisUser.getUserSentiment()

for user in users:
	haha = users.get(user)
	print(user+": "+str(haha.sentiment))
