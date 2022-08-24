def range_sum(numbers, start, end):
    summ = 0
    start = int(start)
    end = int(end)
    for number in numbers:
        if start <= int(number) <= end:
            summ += int(number)
    return summ


input_numbers =  input().split()
a, b =  input().split()
print(range_sum(input_numbers, a, b))