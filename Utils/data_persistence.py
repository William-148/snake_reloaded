from Collections.queue import Queue


USERS_FILE = "local/usr.txt"
SCORE_HISTORY_FILE = "local/scr_h.txt"

def read_local_user_data(callbackFn):
    """Parameters: 
            callbackFn:
                file_line: str
    """
    if not callable(callbackFn): return
    try:
        with open(USERS_FILE, "r") as f:
            for line_readed in f:
                callbackFn(line_readed[:-1])
    except Exception as ex:
        print(ex)

def write_local_user(user: str):
    try:
        with open(USERS_FILE, "a") as f:
            f.write(user + '\n')
    except Exception as ex:
        print(ex)

def read_local_score_history(callbackFn):
    """Parameters: 
            callbackFn:
                user: str
                score: int
    """
    if not callable(callbackFn): return
    try:
        with open(SCORE_HISTORY_FILE, "r") as f:
            for line_readed in f:
                score = line_readed[:-1].split(',')
                callbackFn(score[0], int(score[1]))
    except Exception as ex:
        print(ex)

def write_local_score_to_history(score: tuple[str, int]):
    try:
        with open(SCORE_HISTORY_FILE, "a") as f:
            f.write("{0},{1}\n".format(score[0], score[1]))
    except Exception as ex:
        print(ex)

def write_local_score_history_queue(score_history: Queue):
    """Parameters:
            score_history: Queue of tuple[str, int]
    """
    try:
        with open(SCORE_HISTORY_FILE, "w") as f:
            def write_file(tuple, _):
                f.write("{0},{1}\n".format(tuple[0], tuple[1]))
            score_history.for_each(write_file)
    except Exception as ex:
        print(ex)