def isFactor(factor, word):
    multiple = factor
    count=1
    while len(multiple)<=len(word):
        multiple=factor*count
        if multiple == word:
            return True
        else:
            count+=1
    return False
def gcd(word1, word2):
    shorter = word1 if len(word1)<= len(word2) else word2
    longer = word2 if len(word2)>len(word1) else word1
    gcd_candidates = []
    for i in range(len(shorter),0,-1):
        if len(shorter)%i == 0:
            gcd_candidates.append(shorter[:i])
    for divisor in gcd_candidates:
        # early exit if the divisior length can't be repeated to get the wordings
        if len(longer)%len(divisor)!=0:
            continue

        if isFactor(divisor, longer) and isFactor(divisor, shorter):
            return divisor 
    return ''

assert gcd("abcabc", 'abc') == 'abc'
assert gcd("ABABABAB","ABAB") == "ABAB"
assert gcd("ABCABCABC","ABCAAA") == ''
assert gcd("TAUXXTAUXXTAUXXTAUXXTAUXX","TAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXX") == "TAUXX"