def isRepeatedPattern(pattern:str, word:str) -> bool:
    """
    checks if the word can be constructed by repeating the pattern
    Args:
        pattern (str): the substring to use as a repeating unit.
        word (str): the full string to test against the repeated pattern
        bool: True if word can be constructed by repeating the pattern, False otherwise
    """
    # a valid pattern must repeat itself to construct the word
    # the number of repetitions should make the repeated pattern match the word length.
    return pattern * (len(word)//len(pattern))==word 
    
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

        if isRepeatedPattern(divisor, longer) and isRepeatedPattern(divisor, shorter):
            return divisor 
    return ''

assert gcd("abcabc", 'abc') == 'abc'
assert gcd("ABABABAB","ABAB") == "ABAB"
assert gcd("ABCABCABC","ABCAAA") == ''
assert gcd("TAUXXTAUXXTAUXXTAUXXTAUXX","TAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXX") == "TAUXX"