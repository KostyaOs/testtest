specdict = {'a': [2]}



try:
    specdict['a'].append(1)
except KeyError:
    specdict['a'] = [1]

print(specdict)