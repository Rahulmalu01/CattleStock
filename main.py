class Solution(object):
    def longestValidParentheses(self, s):
        stack = []
        count = 0
        for i in s:
            if stack and ord(i) - ord(stack[-1]) in (1, 2):
                stack.pop()
                count += 2
            else:
                stack.append(i)
        return count

if __name__ == "__main__":
    s = "(()"
    print(Solution().longestValidParentheses(s))