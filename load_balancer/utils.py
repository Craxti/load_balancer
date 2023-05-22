import os
import time


def create_directory(directory):
    os.makedirs(directory, exist_ok=True)


def get_timestamp():
    return int(time.time())


def format_bytes(size):
    power = 2 ** 10
    n = 0
    size_labels = {0: '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}

    while size > power:
        size /= power
        n += 1

    return f"{size:.2f} {size_labels[n]}"
