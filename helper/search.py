def match(key, field) -> bool:
    key = key.lower()
    field = field.lower()
    if key in field:
        return True
    cnt = 0
    j = 0
    for i in range(len(key)):
        while j < len(field) and key[i] != field[j]:
            j += 1

        if j < len(field):
            j += 1
            cnt += 1

    return cnt > (0.7 * len(key))

def search(key, fields) -> dict:
    if not key:
        return {}
    matched = {}
    cnt = 1
    for field in fields:
        if match(key, field):
            matched[cnt] = field
            cnt += 1

    return matched
