from datetime import datetime, timezone
import os
import re
import threading
import time
import uuid


def _format_ts_micro(dt: datetime) -> str:
    """Return YYMMDDHHMMSS + 6-digit microseconds in UTC."""
    return dt.strftime("%y%m%d%H%M%S") + f"{dt.microsecond:06d}"


def _clean_worker_str(s: str, target_len: int = 2) -> str:
    """Normalize a worker string: remove separators, lowercase, and fit to length.

    - Removes any non-alphanumeric characters
    - Lowercases the result
    - If shorter than target_len, left-pads with '0'
    - If longer, keeps the rightmost target_len characters
    """
    s = re.sub(r"[^0-9A-Za-z]", "", s or "").lower()
    if len(s) < target_len:
        s = ("0" * (target_len - len(s))) + s
    elif len(s) > target_len:
        s = s[-target_len:]
    return s


def _default_worker_str() -> str:
    """Derive a stable worker identifier, preferring MAC address.

    Order:
    1) WORKER_ID or WORKER_STR env (sanitized)
    2) MAC address from uuid.getnode() (12 hex chars)
    """
    env = os.getenv("WORKER_ID") or os.getenv("WORKER_STR")
    if env:
        return _clean_worker_str(env)

    node = uuid.getnode()
    # uuid.getnode() returns a 48-bit int; format to 12 hex chars
    mac_hex = f"{node:012x}"
    return _clean_worker_str(mac_hex)


class TimeOrderedIDGenerator:
    """
    Snowflake-like generator with microsecond precision and MAC-based worker ID.

    ID format (concatenated string):
      - YYMMDDHHMMSS + microseconds (18 digits)
      - worker (3 chars, default = MAC hex)
      - sequence (configurable width, digits; default 3)

    Example: 250101123456123456ab07
    """

    def __init__(self, worker_str: str | None = None, seq_digits: int = 2):
        if seq_digits < 1:
            raise ValueError("seq_digits must be >= 1")
        self.worker = (
            _clean_worker_str(worker_str, 12) if worker_str else _default_worker_str()
        )
        self.seq_digits = seq_digits
        self.max_seq = 10**seq_digits - 1
        self._lock = threading.Lock()
        self._last_us = -1
        self._seq = 0

    @staticmethod
    def _now_utc() -> datetime:
        return datetime.now(timezone.utc)

    def next_id(self) -> str:
        with self._lock:
            while True:
                now_dt = self._now_utc()
                curr_us = int(now_dt.timestamp() * 1_000_000)

                if curr_us == self._last_us:
                    if self._seq < self.max_seq:
                        self._seq += 1
                    else:
                        # Exhausted this microsecond; wait for the next one
                        time.sleep(0.000001)  # 1 microsecond
                        continue
                else:
                    self._last_us = curr_us
                    self._seq = 0

                ts = _format_ts_micro(now_dt)
                seq = f"{self._seq:0{self.seq_digits}d}"
                return ts + self.worker + seq


# Module-level singleton with sensible defaults
_ID_GEN = TimeOrderedIDGenerator()


def configure_id_generator(
    worker_str: str | None = None, seq_digits: int | None = None
):
    """Configure the module-level generator.

    - worker_str: custom worker identifier (string). If None, keep current.
    - seq_digits: number of digits for the sequence. If None, keep current.
    """
    global _ID_GEN
    if worker_str is None:
        worker_str = _ID_GEN.worker
    if seq_digits is None:
        seq_digits = _ID_GEN.seq_digits
    _ID_GEN = TimeOrderedIDGenerator(worker_str=worker_str, seq_digits=seq_digits)


def get_id() -> str:
    """Generate a new unique ID: YYMMDDHHMMSS + microseconds(6) + worker(2) + seq."""
    return _ID_GEN.next_id()


def get_unique_id(prev_id: str | None = None) -> str:
    """Generate a new ID, ensuring it differs from prev_id (if provided)."""
    if prev_id is None:
        return get_id()
    for _ in range(100):
        nid = get_id()
        if nid != prev_id:
            return nid
        time.sleep(0.0005)
    return get_id()
