#!/usr/bin/env python3
"""
Import wait_random and write an async routine called wait_n
"""
import asyncio
from importlib import import_module as a


wait_random = a('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> float:
    """
    """