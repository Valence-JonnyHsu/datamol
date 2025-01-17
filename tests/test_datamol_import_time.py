import multiprocessing
import platform

DATAMOL_MAX_IMPORT_DURATION = {}  # in seconds
DATAMOL_MAX_IMPORT_DURATION["default"] = 3
DATAMOL_MAX_IMPORT_DURATION["linux"] = 3
DATAMOL_MAX_IMPORT_DURATION["osx"] = 20
DATAMOL_MAX_IMPORT_DURATION["windows"] = 6


def _get_max_import_duration():
    if platform.system() == "Windows":
        return DATAMOL_MAX_IMPORT_DURATION["windows"]
    elif platform.system() == "Linux":
        return DATAMOL_MAX_IMPORT_DURATION["linux"]
    elif platform.system() == "Darwin":
        return DATAMOL_MAX_IMPORT_DURATION["osx"]
    else:
        return DATAMOL_MAX_IMPORT_DURATION["default"]


def _import_datamol_fn(queue):
    import datetime

    start = datetime.datetime.now()
    import datamol

    duration = datetime.datetime.now() - start
    duration = duration.total_seconds()
    queue.put(duration)


def test_datamol_import():

    context = multiprocessing.get_context(method="spawn")

    queue = context.Queue()
    p = context.Process(target=_import_datamol_fn, args=(queue,))
    p.start()
    duration = queue.get()
    p.join()
    p.close()

    print(duration)

    # Check datamol wasn't too fast to load
    # That should never happen and it's a simple sanity check
    # whether the `spawn` process worked correctly.
    assert duration > 1e-2, "datamol loaded too fast, something is wrong with the test."

    # Check datamol wasn't too long to load
    assert duration < _get_max_import_duration(), "datamol tooks too long to load."
