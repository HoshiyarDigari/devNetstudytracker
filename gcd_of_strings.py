import argparse
def isRepeatedPattern(pattern:str, word:str) -> bool:
    """
    checks if the word can be constructed by repeating the pattern
    Args:
        pattern (str): the substring to use as a repeating unit.
        word (str): the full string to test against the repeated pattern
    Returns:
        bool: True if word can be constructed by repeating the pattern, False otherwise
    """
    # a valid pattern must repeat itself to construct the word
    # the number of repetitions should make the repeated pattern match the word length.
    return pattern * (len(word)//len(pattern))==word 
    
def gcd(word1:str, word2:str)->str:
    """
    returns the gcd of the two input strings. The gcd is the longest string that can be repeated to construct the two input strings.
    Args:
        word1 (str): first string
        word2 (str): second string
    Returns:
        str: the gcd of the two strings
    """

    shorter = word1 if len(word1)<= len(word2) else word2
    longer = word2 if len(word2)>len(word1) else word1
    gcd_candidates = []
    # gcd can only be substrings of the shorter string, that can repeat to construct the shorter string. We test them from the longest to the shortest.
    for i in range(len(shorter),0,-1):
        if len(shorter)%i == 0:
            gcd_candidates.append(shorter[:i])
    
    for divisor in gcd_candidates:
        # the length of the candidate gcd should be a factor of the length of the longer string
        if len(longer)%len(divisor)!=0:
            continue

        if isRepeatedPattern(divisor, longer) and isRepeatedPattern(divisor, shorter):
            return divisor 
    return ''

if __name__ == "__main__":
    #create parser for arguments
    parser = argparse.ArgumentParser(description="Get the GCD of two strings")
    # create inputs/arguments
    parser.add_argument("word1", type=str, help="first input string")
    parser.add_argument("word2", type=str, help="second input string")

    # parse arguments
    args = parser.parse_args()

    # populate the varaibles
    word1 = args.word1
    word2 = args.word2

    # find the gcd
    result = gcd(word1, word2)
    print('the GCD of  ', word1, 'and', word2, 'is', result)



# assert gcd("abcabc", 'abc') == 'abc'
# assert gcd("ABABABAB","ABAB") == "ABAB"
# assert gcd("ABCABCABC","ABCAAA") == ''
# assert gcd("TAUXXTAUXXTAUXXTAUXXTAUXX","TAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXXTAUXX") == "TAUXX"