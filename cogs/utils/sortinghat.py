import gspread
import random
from oauth2client.service_account import ServiceAccountCredentials
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
UTIL_DIR = os.path.join(ROOT_DIR, 'cogs/utils')
CREDENTIALS_DIR = os.path.join(ROOT_DIR, '.credentials')

A1 = 'A1'
A2 = 'A2'
A3 = 'A3'
A4 = 'A4'

A1_TYPES = ["INTJ", "ENTP", "INFJ", "ENFP"]
A2_TYPES = ["INTP", "ENTJ", "ENFJ", "INFP"]
A3_TYPES = ["ISTJ", "ISFJ", "ESTP", "ESFP"]
A4_TYPES = ["ESTJ", "ESFJ", "ISTP", "ISFP"]


def sorting_sleeve(t_type):
    if t_type in A1_TYPES:
        return A1
    elif t_type in A2_TYPES:
        return A2
    elif t_type in A3_TYPES:
        return A3
    elif t_type in A4_TYPES:
        return A4
    else:
        return 'Invalid Type'


def scoring_personality(answers):

    q0 = answers['What is the perfect size group for a night out? ']
    q1 = answers['How much time do you spend socializing? ']
    q2 = answers['How neat do you keep your workspace?']
    q3 = answers['Do you prefer novelty or stability to be more common in situations surrounding you?']
    q4 = answers['Do you express your emotions or thoughts more?']
    q5 = answers['Are you better at improvising or planning out a given task?']

    # # First - What is the perfect size group for a night out?
    # if q1 in (3,4):
    #     first = 'I'
    # elif q1 in (6,7,8):
    #     first = 'E'
    # elif q1 == 5:
    #     if random.random() > .48:
    #         first = 'I'
    # else:
    #     first = 'error'

    # First - How much time do you spend socializing? What is the perfect size group for a night out?
    if q1 in (1,2):
        first = 'I'
    elif q1 in (4,5):
        first = 'E'
    elif q1 == 3:
        if q0 is 3:
            first = 'I'
        elif q0 is 4:
            if random.random() > .25:
                first = 'I'
            else:
                first = 'E'
        elif q0 is 5:
            if random.random() > .25:
                first = 'E'
            else:
                first = 'I'
        elif q0 in [6, 7, 8]:
            first = 'E'
    else:
        first = 'error'

    # Second - How neat do you keep your workspace? Do you prefer novelty or stability to be more common in situations surrounding you?
    if q2 is 1:
        second = 'S'
    elif q2 is 5:
        second = 'N'
    elif q2 is 3:
        if q3.lower() is 'novelty':
            second = 'N'
        else:
            second = 'S'
    elif q2 is 2:
        if q3.lower() is 'stability':
            second = 'S'
        else:
            if random.random() > .3:
                second = 'N'
            else:
                second = 'S'
    elif q2 is 4:
        if q3.lower() is 'novelty':
            second = 'N'
        else:
            if random.random() > .3:
                second = 'S'
            else:
                second = 'N'

    # Third - Do you express emotions or thoughts more?
    if q4 == 'Thoughts':
        third = 'T'
    elif q4 == 'Emotions':
        third = 'F'
    else:
        third = 'error'

    # Fourth - Are you better at improvising or planning out a given task?
    if q5 == 'Improvising':
        fourth = 'P'
    elif q5 == 'Planning':
        fourth = 'J'
    else:
        fourth = 'error'

    personality_score = first + second + third + fourth
    return personality_score


def check_accuracy(resp):
    # read in Welcome question about type
    mbtype = resp['Myers Briggs Personality Type?']
    personality_score = scoring_personality(resp)
    print('given:', mbtype, 'scored:', personality_score)
    if mbtype == personality_score:
        compat = sorting_sleeve(mbtype)
    elif mbtype != personality_score:
        if "N" in mbtype and "N" in personality_score:
            if random.random() > .5:
                compat = A1
            else:
                compat = A2
        elif "S" in mbtype and "S" in personality_score:
            if random.random() > .5:
                compat = A3
            else:
                compat = A4
        else:
            scores = {A1: 0,
                      A2: 0,
                      A3: 0,
                      A4: 0}
            # pull in data about alignment, HP house, and morals
            alignment1 = resp['What is your Alignment:1?']
            alignment2 = resp['What is your Alignment:2?']
            hp = resp['What Harry Potter house are you in?']
            morals = resp['Are you strongly driven by your morals?']

            if "chaotic" in alignment1.lower():
                scores[A1] += 1
                scores[A2] += 1
            elif "lawful" in alignment1.lower():
                scores[A3] += 1
                scores[A4] += 1

            if "Ravenclaw" == hp:
                scores[A1] += 1
            elif "Slytherin" == hp:
                scores[A2] += 1
            elif "Gryfindor" == hp:
                scores[A3] += 1
            elif "Hufflepuff" == hp:
                scores[A4] += 1

            if "Yes" == morals:
                scores[A1] += 1
                scores[A3] += 1
            elif "No" == morals:
                scores[A2] += 1
                scores[A4] += 1

            max_key = ''
            max_score = 0
            for k in scores.keys():
                if scores[k] > max_score:
                    max_key = k
                    max_score = scores[k]

            compat = max_key
    return compat


def read_sorted():
    with open(os.path.join(DATA_DIR, 'sorted'), 'r') as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    return content


def append_sorted(uid):
    with open(os.path.join(DATA_DIR, 'sorted'), 'a+') as f:
        f.write(uid+'\n')


def main():

    # Retrieve already sorted #
    sorted_uids = read_sorted()

    # Retrieve Survey Results #
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(CREDENTIALS_DIR, 'client_secret_survey.json'), scope)
    client = gspread.authorize(creds)

    sheet_sort = client.open("Quick_Sort_Responses").sheet1
    responses = sheet_sort.get_all_records()
    for r in responses:
        if r['Timestamp'] is '':
            responses.remove(r)

    for r in responses:
        uid = r['What is your Discord Name? Answer in the form of: Username#1234']
        if uid not in sorted_uids:
            try:
                print(uid, check_accuracy(r))
                append_sorted(uid)
            except:
                print("ERROR")

if __name__ == '__main__':
    sys.exit(main())
