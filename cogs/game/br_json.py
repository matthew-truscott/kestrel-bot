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
            r_iter += 1
            rresult -= (p[r_iter] / p_total)
    return element
