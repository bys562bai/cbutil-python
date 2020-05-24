from container import SignSet

a = SignSet('abcdefg')
b = SignSet('efghijk')


results = [
    [a|b,a&b,a-b,a^b],
    [-a|b,-a&b,a-b,-a^b],
    [-a|-b,-a&-b,a-b,-a^-b],
    [a|-b,a& -b,a- -b,a^-b]
] 

from pprint import pprint

pprint(results)