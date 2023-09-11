import subprocess


def move_file(src, dst):
    subprocess.run(['mv', src, dst], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def strfdelta(tdelta):
    "Convert timedelta to string"
    d = {}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return "{hours}:{minutes:02d}:{seconds:02d}".format(**d)

def ask_question(question) -> bool:
    resp = input(question)
    while True:
        if resp.lower() in ["y", "yes"]:
            return True
        elif resp.lower() in ["n", "no"]:
            return False
        print("Invalid input")
        resp = input(question)
