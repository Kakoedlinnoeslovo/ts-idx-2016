
VAR = [1, 2, 3, 4, 5, 7, 9, 14, 28]

def _fill_bin(num, size):
    tmp = bin(num)[2:]
    return '0' * (size - len(tmp)) + tmp

def compress(nums):
    final_result = []
    diff_nums = [nums[0]] + [nums[i] - nums[i-1] for i in xrange(1, len(nums))]
    max_size = 0
    max_num = 8
    while len(diff_nums) > 0:
        if (len(diff_nums) >= VAR[max_num]) and \
                all(num < 2 ** VAR[max_size] for num in diff_nums[:VAR[max_num]]):
            result = _fill_bin(max_size, 4)
            for num in diff_nums[:VAR[max_num]]:
                result += _fill_bin(num, VAR[max_size])
            while len(result) > 0:
                if len(result) < 8:
                    result += '0' * (8 - len(result))
                final_result.append(chr(int(result[:8], 2)))
                result = result[8:]
            diff_nums = diff_nums[VAR[max_num]:]
            max_size = 0
            max_num = 8
        else:
            max_size += 1
            max_num -= 1
    return ''.join(final_result)

def decompress(encoded):
    final_result = []
    last_num = 0
    for i in xrange(0, len(encoded), 4):
        bitstring = ''.join([_fill_bin(ord(encoded[j]), 8) for j in xrange(i, i + 4)])
        max_size = VAR[int(bitstring[:4], 2)]
        for j in xrange(4, 33 - max_size, max_size):
            current = int(bitstring[j:j+max_size], 2)
            last_num += current
            final_result.append(last_num)
    return final_result