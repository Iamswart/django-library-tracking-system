# Complete the following Python tasks in the core_skills.py file.
# Create a list of 10 random numbers between 1 and 20.
# Filter Numbers Below 10 (List Comprehension)
# Filter Numbers Below 10 (Using filter)

import random

rand_list = [random.randint(1, 20) for _ in range(10)]

list_comprehension_below_10 = [num for num in rand_list if num < 10]

filter_below_10 = list(filter(lambda x:x < 10, rand_list))


print("Random list:", rand_list)
print("List comprehension result:", list_comprehension_below_10)
print("Filter result:", filter_below_10 )