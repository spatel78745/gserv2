'''
Created on Jan 30, 2016

@author: spatel78745
'''
from _functools import reduce

A1 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

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

print('size 1:', subarraysOfSize(A1, 1))
print('size', len(A1), ':', subarraysOfSize(A1, len(A1)))
print('size 2:', subarraysOfSize(A1, 2))

subsOfA1 = subarrays(A1)
print('all:', subsOfA1)
print('max:', maxSequence(subsOfA1))
