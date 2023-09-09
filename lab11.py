candidates = {}
num = int(input())
for i in range(num):
    name, votes = input().split()
    if name in candidates:
        candidates[name]+=int(votes)
    else:
        candidates[name]=int(votes)
print(sorted(candidates.items()))
