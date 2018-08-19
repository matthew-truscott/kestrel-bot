import random

def get_random_element(dict, tag):
    rval = dict[tag]
    rcont = rval["content"]
    rresult = random.random()
    element = None
    r_iter = 0
    p = rval["p"]
    p_total = sum(rval["p"])
    while rresult > 0.0:
        if rresult < (p[r_iter] / p_total):
            rresult = -1
            element = rcont[r_iter]
        else:
            rresult -= (p[r_iter] / p_total)
            r_iter += 1
    return element

if __name__ == '__main__':
    testdict = {
        "id": 1,
        "name": "wasteland",
        "p_event": 30,
        "forage": {
          "content": [1, 7],
          "p": [10, 5]
        },
        "event": {
          "content": [1],
          "p": [10]
        }
    }
    tag = "forage"
    e = get_random_element(testdict, tag)
    print(e)
