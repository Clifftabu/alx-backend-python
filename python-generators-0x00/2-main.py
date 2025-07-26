#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')

# Print processed users in a batch of 50
try:
    users = processing.batch_processing(50)
    for user in users:
        print(f"User {user['user_id']} is over 25 years old.")
except BrokenPipeError:
    sys.stderr.close()
