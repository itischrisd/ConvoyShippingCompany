class RightTriangle:
    def __init__(self, hyp, leg_1, leg_2):
        self.c = hyp
        self.a = leg_1
        self.b = leg_2
        self.area = leg_1 * leg_2 * 0.5

# triangle from the input
input_c, input_a, input_b = [int(x) for x in input().split()]

# write your code here
if input_c ** 2 == input_a ** 2 + input_b ** 2:
    right_triangle = RightTriangle(input_c, input_a, input_b)
    print(right_triangle.area)
else:
    print("Not right")