def count_votes(ballots, candidates):
    for ballot in ballots:
        for candidate, vote in ballot.items():
            candidates[candidate][vote] += 1
    return candidates

def get_semifinalists(candidates):
    return dict(sorted(candidates.items(), key=lambda item: item[1][2], reverse=True)[0:3])

def get_finalists(semifinalists):
    return dict(sorted(semifinalists.items(), key=lambda item: item[1][0])[0:2])

def get_winner(ballots, finalists):
    finalist1, finalist2 = finalists.keys()
    finalist1_score = sum(ballot[finalist1] > ballot[finalist2] for ballot in ballots)
    finalist2_score = sum(ballot[finalist2] > ballot[finalist1] for ballot in ballots)
    if finalist1_score > finalist2_score:
        return finalist1
    elif finalist2_score > finalist1_score:
        return finalist2
    else:
        return "tie"

if __name__ == '__main__':
    # dict of candidates and how much of each vote they got
    candidates = {'Red': [0, 0, 0], 'Green': [0, 0, 0], 'Yellow': [0, 0, 0], 'Blue': [0, 0, 0]}

    ballots = [
        {"Red": 2, "Green": 1, "Yellow": 0, "Blue": 2},
        {"Red": 0, "Green": 2, "Yellow": 1, "Blue": 2},
        {"Red": 2, "Green": 0, "Yellow": 2, "Blue": 1},
        {"Red": 2, "Green": 1, "Yellow": 2, "Blue": 2},
        {"Red": 1, "Green": 2, "Yellow": 0, "Blue": 2},
        {"Red": 2, "Green": 1, "Yellow": 2, "Blue": 2},
        {"Red": 2, "Green": 2, "Yellow": 1, "Blue": 2},
        {"Red": 1, "Green": 2, "Yellow": 0, "Blue": 2},
        {"Red": 2, "Green": 0, "Yellow": 1, "Blue": 2},
    ]  # 0=bad, 1=ok, 2=good. used for index in candidates dict

    candidates = count_votes(ballots, candidates)
    print(candidates)

    semifinalists = get_semifinalists(candidates)
    print(semifinalists)

    finalists = get_finalists(semifinalists)
    print(finalists)

    winner = get_winner(ballots, finalists)
    print(f'The winner is {winner}')


