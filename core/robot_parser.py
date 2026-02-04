NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3,
    "four": 4, "five": 5, "six": 6
}

MOVE_VERBS = {"move", "go", "advance", "fly", "ascend", "descend"}
DIRECTIONS = {"forward", "backward", "up", "down"}
NEGATIONS = {"no", "not", "dont", "never"}

def is_robot_intent(tokens):
    if any(n in tokens for n in NEGATIONS):
        return False
    return any(t in MOVE_VERBS for t in tokens)

def extract_commands(tokens):
    commands = []
    i = 0

    while i < len(tokens):
        if tokens[i] in MOVE_VERBS:
            cmd = {"action": tokens[i], "direction": None, "distance": None}

            if i+1 < len(tokens) and tokens[i+1] in DIRECTIONS:
                cmd["direction"] = tokens[i+1]
                i += 1

            if i+2 < len(tokens) and tokens[i+1] == "by":
                val = tokens[i+2]
                if val.isdigit():
                    cmd["distance"] = int(val)
                elif val in NUMBER_WORDS:
                    cmd["distance"] = NUMBER_WORDS[val]
                i += 2

            commands.append(cmd)
        i += 1

    return commands
