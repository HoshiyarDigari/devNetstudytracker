class Solution:

    def merge_strings(word1, word2):
        merged_list = []
        # Interleave characters from word1 and word2 up to the length of word1
        for index in range(len(word1)):
            merged_list.append(word1[index])
            
            # Append character from word2 if it exists at this index
            if index < len(word2):
                merged_list.append(word2[index])
            else:
                # word2 is exhausted; append remaining characters from word1
                merged_list.append(word1[index+1:])
                return ''.join(merged_list)

        # word1 is exhausted; append remaining characters from word2
        if len(word2) > len(word1):
            merged_list.append(word2[len(word1):])

        return ''.join(merged_list)




solution = Solution
assert solution.merge_strings("", "") == ''
assert solution.merge_strings("abc", "12") == "a1b2c"
assert solution.merge_strings("abc", "1234") == "a1b2c34"
assert solution.merge_strings("abcdef", "12") == "a1b2cdef"



