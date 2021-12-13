import random
names=["we","i","they","he","she","jack","jim"]
verbs=["was","is","are","were"]
nouns=["playing a game","watching television","talking","dancing","speaking", "playing football", "chilling", "having fun"]
f = open("big_test.txt", "w")
for i, _ in enumerate(range(700002)):
    a = (random.choice(names))
    b = (random.choice(verbs))
    c = (random.choice(nouns))
    f.write(f"{a} {b} {c}")
    if i != len(range(700002)) -1:
        f.write("\n")
