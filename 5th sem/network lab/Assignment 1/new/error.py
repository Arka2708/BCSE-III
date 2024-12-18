import random
import os


def inject_single_bit_error(block):
    bit_to_flip = random.randint(0, len(block) * 8 - 1)
    byte_index = bit_to_flip // 8
    bit_index = bit_to_flip % 8
    byte = block[byte_index]
    block = block[:byte_index] + bytes([byte ^ (1 << bit_index)]) + block[byte_index+1:]
    return block

def inject_burst_error(block):
    start_index = random.randint(0, len(block) - 2)
    end_index = random.randint(start_index + 1, len(block))
    error_byte = os.urandom(1)
    return block[:start_index] + error_byte + block[end_index:]

def inject_two_isolated_single_bit_errors(block):
    error1 = inject_single_bit_error(block)
    error2 = inject_single_bit_error(error1)
    return error2

def inject_odd_number_of_errors(block):
    num_errors = random.randint(1, len(block) * 8 - 1)
    for _ in range(num_errors):
        block = inject_single_bit_error(block)
    return block
