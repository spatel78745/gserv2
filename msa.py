'''
Created on Jan 30, 2016

@author: spatel78745
'''
from _functools import reduce

A1 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
A2 = [3, -1, 4, -3]

def subarraysOfSize(A, n):
    result = []
    for i in range(0, len(A)-n+1):
        j = i + n
        result.append(A[i:j])
    
    return result

def subarrays(A):    
    result = []
    for n in range(1, len(A) + 1):
        result += subarraysOfSize(A, n)
    return result

def maxSequence(sequences):
    maxSum = sum(sequences[0])
    maxSeq = sequences[0]
    
    for seq in sequences:
        testSum = sum(seq)
        if testSum > maxSum:
            maxSum = testSum
            maxSeq = seq
            
    return (maxSeq, maxSum) 

def kadane(A):
    max_ending_here = max_so_far = 0
    for x in A:
        max_ending_here_plus_x = max_ending_here + x
        old_max_ending_here = max_ending_here
        max_ending_here = max(0, max_ending_here + x)
        print('x', x, 'max_ending_here', old_max_ending_here, 'max_ending_here+x', max_ending_here_plus_x, '_max_ending_here', max_ending_here)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far 

print('size 1:', subarraysOfSize(A1, 1))
print('size', len(A1), ':', subarraysOfSize(A1, len(A1)))
print('size 2:', subarraysOfSize(A1, 2))

subsOfA1 = subarrays(A1)
print('all:', subsOfA1)
print('max:', maxSequence(subsOfA1))

subsOfA2 = subarrays(A2)
print('max:', maxSequence(subsOfA2))

print('kadane', kadane(A1))