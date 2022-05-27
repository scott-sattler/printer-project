import math
import queue
import random
import string
import time
from itertools import combinations


# # print(type(time.time() - time_initial))
#
# # queue_timeout = 1
# # time_initial = time.time()
# #
# # time_box = 0
# # time_to_print_at = math.inf
# # while time_to_print_at > time.time():
# #     time_to_print_at = queue_timeout * 3 + time_initial
# #     print(time_to_print_at, time.time())
# #     time_box += 1
# #
# # print(time_box)
#
# # x = [['d', 1], ['c', 3], ['b', 2], ['a', 4]]
# # # x = [[2342.2, 1], [2.2, 3], [132.2, 2], [342.2, 4]]
# # # x.sort(key=lambda y: y[1])
# # # print(x)
# # # x.sort()
# # # print(x)
# # print(sum([i[1] for i in x]))
#
#
# # minimize wasted label paper
# # max_size = 0
# # agenda = []
# # open_set = []
# # closed_set = []
# # best_fit = []
# # label_queue = [(342.2, 'ytntev'), (2342.2, 'sad'), (2.2, 've'), (132.2, 'seve')]
# #
# # big_list = []
# # new_item = []
# # for i, seed in enumerate(label_queue):
# #     new_item = ([seed], [])
# #     for j, remaining in enumerate(label_queue):
# #         if i != j:
# #             new_item[1].append(remaining)
# #     big_list.append(new_item)
# #
# # print(big_list)
#
# # agenda.append(new_item)
#
# # print(agenda)
#
#
#
# """
#         List<NodeData> exploredNodes = new List<NodeData>();    // closed set.
#         List<NodeData> evaluatedNodes = new List<NodeData>();   // open set.
#         List<NodeData> discoveredNodes = new List<NodeData>();
#         List<Vector2Int> bestPathFound = new List<Vector2Int>();
#         NodeData currentNode = new NodeData();
#
# """
#
#
# # x = [[[[[342.2, 'ytntev']], [[2342.2, 'sad'], [2.2, 've'], [132.2, 'seve']]], [[[2342.2, 'sad']], [[342.2, 'ytntev'], [2.2, 've'], [132.2, 'seve']]], [[[2.2, 've']], [[342.2, 'ytntev'], [2342.2, 'sad'], [132.2, 'seve']]], [[[132.2, 'seve']], [[342.2, 'ytntev'], [2342.2, 'sad'], [2.2, 've']]]]]
#
#
#
# # z = [[[[132.2, 'seve']], [[342.2, 'ytntev'], [2342.2, 'sad'], [2.2, 've']]]]
# # print(z[0][0])
#
#
# # buff_capacity = 12
# # font_width = 1
# #
# # k = lambda: random.randint(1, int(buff_capacity // font_width))  # bad practice var = lambda
# # generate_string = lambda max_len: ''.join(random.choices(string.ascii_letters, k=k()))
# # out = [generate_string(buff_capacity) for i in range(10)]
# # print(out)
# #
# # # out = ['xAssQOAT', 'xAssQOAT', 'xAssQOAT', 'xAssQOAT', 'pNDmsG']
# # # print(out)
# #
# # # convert to numeric value hash table
# # hash_lookup = {}
# # for each in out:
# #     size = len(each)
# #     if hash_lookup.get(size) is None:
# #         hash_lookup[size] = [1, each]
# #     else:
# #         hash_lookup[size].append(each)
# #         hash_lookup[size][0] += 1
# #
# # print(hash_lookup)
#
#
# # label_queue = queue.SimpleQueue()
# #
# # label_queue.put((3, 'abc'))
# # label_queue.put((3, 'sfe'))
# # print(' '.join([label_queue.get()[1] for i in range(label_queue.qsize())]))
# # label_queue.put('abc')
# # print(label_queue.get())
# # print(list(label_queue))
#
#
# # foo = '1234235'
# # bar = '1'
# #
# # list1 = [foo, bar]
# # fn_list = map(lambda x: len(x), list1)
# # # print(sum(map(lambda x: len(x), list1)))
# #
# # len_fn = lambda x: sum(map(lambda y: len(y), x))  # bad practice
# # print(len_fn(list1))
#
# expr_time = lambda: random.randint(1, 99)
# label_text = lambda: ''.join([random.choice(string.ascii_letters) for j in range(random.randint(1, 13))])
#
# foo = [(expr_time(), label_text()) for i in range(20)]
# # print(foo)
#
# test_case_1 = [3, 2, 9, 9, 5, 3, 2, 4, 8, 8]
# test_case_2 = [8, 7, 3, 9, 7, 6, 3, 6, 1, 8, 9, 8, 8, 7, 7, 8, 8, 4, 9, 8]
# test_case_3 = [(80, 'NkroxdTbenoeY'), (98, 'mL'), (66, 'T'), (17, 'rPNwLpieD'), (46, 'vrBmlXSYffj'), (14, 'kwlJjvmZPmXik'), (23, 'OieJoiIEfynk'), (56, 'PEmsQxW'), (72, 'HxMkRQ'), (30, 'VXyDxOqHo'), (47, 'hZylONzrDHX'), (29, 'pmRkCmRbtyk'), (40, 'JMJEbZTymuZ'), (25, 'zcYeOovJOQk'), (9, 'zq'), (37, 'jcgJOUxSq'), (50, 'XzwwCLovN'), (30, 'iqVbVTYf'), (61, 'zZJhT'), (49, 'LJnpRoSoUw')]
#
#
# bin = []
# remaining = test_case_2
# current_time = time.time()
# current_time = 30
# buffer_capacity = 12
# def bin_packer(queue_list):
#     # since a print must occur under the temporal constraint
#     # printing all pending jobs satisfies label usage minimization
#     if sum([len(i[1]) for i in queue_list]) <= buffer_capacity:
#         return queue_list
#
#     # job expiration
#
#
#
#     # the corner case for optimization occurs when
#     # the buffer overflows with >0 unexpired print jobs
#
#
#
#     # get expired
#     remaining = []
#     expired_seeds = []
#     # expired_seeds = [j for j in [i if current_time >= i[0] else remaining.append(i) for i in queue_list] if j is not None]
#     for i in queue_list:
#         if current_time >= i[0]:
#             expired_seeds.append(i)
#         else:
#             remaining.append(i)
#
#     print("remaining:", remaining)
#     print("expired_seeds:", expired_seeds)
#
#     # sort
#     # rem_srt = lambda x: x[0]
#     # exp_srt = lambda x: x[1]
#     remaining = sorted(remaining, key=lambda x: x[0])
#     expired_seeds = sorted(expired_seeds, key=lambda x: x[1], reverse=True)
#
#     print("remaining sorted:", remaining)
#     print("expired_seeds sorted:", expired_seeds)
#
#     push_bins = []
#     for expired_seed in expired_seeds:
#         push_bin = [expired_seed]
#         for each_remaining in remaining:
#             pass
#
#
#
#
#     # for each expired seed
#     # test existing bins for space
#     # place into existing bin if space
#     # else return to remaining (warning infinite loop)
#
#
#
# # runtime O(2^n * n)
# # memory O(n)
#
# # operations research: subset sum / partition / problem
#
# bin_packer(test_case_3)
#
#
# # x = ['a', 'b', 'c', 'd']
# # y = ['z']
# #
# # for each in x:
# #     print(y[0] + each)
#
# nums = [8, 7, 3, 9, 7, 6, 3, 6, 1, 8, 9, 8, 8, 7, 7, 8, 8, 4, 9, 8]
#
# # for each in nums:
# #     print(nums[0] + each)
#
# # for i, x in enumerate(nums):
# #     for j, y in enumerate(nums):
# #         if i != j:
# #             for k, z in enumerate(nums):
# #                 if j != k and i != k:
# #                     print(x + y + z)
#
# # print(len(nums)**3)
#
# nums.sort(reverse=True)
# print(nums)
#
# base = 3
# goal = 17
# total = base
# indices = []
# for i, num in enumerate(nums):
#     if total + num <= goal:
#         total += num
#         indices.append(i)
# print(total, indices)
#
#
# test_nums = [1, 2, 3, 4, 5]
# list_combinations = list()
# # print(list_combinations)
# # for i in range(1, len(test_nums)):
# #     for j in [list(combinations(test_nums, r=i))]:
# #         for k in j:
# #             list_combinations.append(sum(k))
#
# # combinations of each size 1 to n
# n = len(test_nums)
# for i in range(1, n):
#     list_combinations.append(list(combinations(test_nums, r=i)))
#
#
# for j in list_combinations:
#     print(j)
#
# # com
# # for i in list_combinations:
#
#
# # print(list_combinations)
#
# # unique_sums = list()
# # for each in list_combinations:
# #     print(each)
#
#
#
# lst = []
# print(len(lst))
# lst.append('a')
# print(lst)




k = lambda: random.randint(1, int(buff_capacity // font_width))  # bad practice var = lambda
generate_string = lambda max_len: ''.join(random.choices(string.ascii_letters, k=k()))
out = [generate_string(buff_capacity) for i in range(10)]
print(out)


