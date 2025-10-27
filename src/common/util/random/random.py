import random
import string
import time
from datetime import datetime


g_seed_num: int = 0


def get_random_string(length: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def new_id() -> str:
    global g_seed_num
    snum = g_seed_num % 100
    g_seed_num += 1
    rstr = get_random_string(2)
    # id: str = datetime.now().strftime("%y%m%d%H%M%S%f")
    # id = "%s%.2d" % (id[0:18], snum)
    return "%s%.2s%.2d" % (datetime.now().strftime("%y%m%d%H%M%S%f"), rstr, snum)

    """
    id = next(gen)
    str_id = str(id)

    sf = Snowflake.parse(id)  # , 1288834974657)
    print(f"{sf.timestamp = }")
    print(f"{sf.instance = }")
    print(f"{sf.epoch = }")
    print(f"{sf.seq = }")
    print(f"{sf.seconds = }")
    print(f"{sf.milliseconds = }")
    print(f"{sf.datetime = }")
    print(f"{int(sf) = }")

    return str_id
    """


def new_unique_id(prev_id: str) -> str:
    id: str = ""
    for i in range(100):
        id = new_id()
        if prev_id == id:
            time.sleep(0.001)
            continue
        break
    return id
