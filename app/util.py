import hashlib
import datetime
import asyncio
import logging


def get_ram_space(ram: str) -> int:
    units = {'MB': 1e6, 'GB': 1e9}
    return int(float(ram[:-2]) * units[ram[-2:]])


def convert_storage(storage: str) -> str:
    return storage[:-1]


async def run_command(cmd):
    # Start a subprocess
    process = await asyncio.create_subprocess_shell(
        cmd=cmd,  # Replace this with your command and arguments
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Read stdout and stderr
    stdout, stderr = await process.communicate()

    # Print the output
    logging.info(f"[stdout]\n{stdout.decode()}")
    if stderr:
        logging.info(f"[stderr]\n{stderr.decode()}")


def get_random_str():
    hashlib.sha1().update(str(datetime.datetime.now().timestamp()).encode("utf-8"))
    return hashlib.sha1().hexdigest()[:20]
