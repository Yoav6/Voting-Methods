import string
from random import randint, seed, choice

def calc_weight(ballot, elected, ejected):
    return (1
            + len([candidate for candidate, vote in ballot.items() if candidate in elected and vote == 2])
            + len([candidate for candidate, vote in ballot.items() if candidate in ejected and vote == 0])
            )

def reweigh_ballots(ballots, elected, ejected):
    for ballot in ballots:
        ballot[0] = calc_weight(ballot[1], elected, ejected)
    return ballots

def count_votes(ballots, candidates):
    for candidate in candidates:
        candidates[candidate] = [0, 0, 0]
    for ballot in ballots:
        weight, ballot = ballot
        for candidate, vote in ballot.items():
            try:
                candidates[candidate][vote] += (1 / weight)
            except KeyError:
                pass
                # happens when a candidate is elected or ejected
    return candidates

def get_semifinalists(candidates):
    return dict(sorted(candidates.items(), key=lambda item: item[1][2], reverse=True)[0:3])

def get_finalists(semifinalists):
    x = sorted(semifinalists.items(), key=lambda item: item[1][0])
    return dict(x[0:2]), x[2][0]

def get_winner(ballots, finalists):
    finalist1, finalist2 = finalists.keys()
    finalist1_score = sum((ballot[finalist1] > ballot[finalist2]) * weight for weight, ballot in ballots)
    finalist2_score = sum((ballot[finalist2] > ballot[finalist1]) * weight for weight, ballot in ballots)
    if finalist1_score > finalist2_score:
        return finalist1
    elif finalist2_score > finalist1_score:
        return finalist2
    else:  # tiebreaker
        print("tiebreaker used")
        finalist1_score = sum(ballot[finalist1] * weight for weight, ballot in ballots)
        finalist2_score = sum(ballot[finalist2] * weight for weight, ballot in ballots)
        if finalist1_score > finalist2_score:
            return finalist1
        elif finalist2_score > finalist1_score:
            return finalist2
        else:
            print('winner chosen randomly')
            return choice([finalist1, finalist2])

if __name__ == '__main__':
    seed(10)  # makes the random number generator generate the same numbers each run

    elected = []
    ejected = []
    seats = 5  # setting to 1 implements single-winner 3-2-1 voting

    candidates = {candidate: [0, 0, 0] for candidate in list(string.ascii_uppercase)}
    #print(candidates)

    # first number is the weight
    ballots = [[1, {candidate: randint(0, 2) for candidate in candidates}] for i in range(10)]
    #print(*ballots, sep='\n')
    for seat in range(seats):
        print('\n', 'round', seat + 1, '\n')
        ballots = reweigh_ballots(ballots, elected, ejected)
        candidates = count_votes(ballots, candidates)
        print(f'{candidates=}')
        semifinalists = get_semifinalists(candidates)
        print(f'{semifinalists=}')
        finalists, to_eject = get_finalists(semifinalists)
        print(f'{finalists=}')
        ejected.append(to_eject)
        candidates.__delitem__(to_eject)  # can be disabled to make ejection non-final
        print(to_eject, 'was ejected')
        winner = get_winner(ballots, finalists)
        print(winner, 'was elected')
        elected.append(winner)
        candidates.__delitem__(winner)
    print(f'\n final result:\n')
    print(f'{elected=}')
    print(f'{ejected=}')


