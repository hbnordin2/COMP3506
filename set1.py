#Find out if n is even
def q1(n):
    div = n//2
    remainder = n-div*2
    if(remainder!=0):
        return False
    return True

# Find n%m
def q2(n, m):
    div = n//m
    remainder = n-div*m
    return remainder

"""
This works because after you start checking integers
that are greater than sqrt(n), the only integers that
m>sqrt(n) can be multiplied with to equal n are less than
sqrt(n), which have already been checked.
"""
# Find out if n is prime
def q3(n):
    x = 2
    stopper = x*x
    while(stopper<n):
        if(q2(n, x) == 0):
            return False
        x += 1
        stopper = x*x
    return True

#Find out m^n where n=2^x where x is an integer
def q4(m,n):
    if (n == 1):
        return m
    else:
        result = powerer(m,n//2)
        return(result * result)

"""
This works by iterating through the unsorted list, and searching
for each element in the sorted list using binary search
"""
#Find out if a there is an element in a sorted list that is an element
#of an unsorted list

def binary_search(element, array):
    if(len(array)==1):
        if(array[0] == element):
            return True
        return False
    left=0
    right=len(array)
    middle=right//2
    if(array[middle]==element):
        return True
    elif(array[middle]>element):
        return binary_search(element, array[0:middle])
    else:
        return binary_search(element, array[middle: right])

def q5(sorted_list, unsorted_list):
    if(len(unsorted_list)==1):
        return binary_search(unsorted_list[0], sorted_list)
    return(q5(sorted_list, unsorted_list[1:]) or q5(sorted_list, [unsorted_list[0]]))
