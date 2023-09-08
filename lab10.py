str = input("enter the numbers ")
nums = set()
for num in str.split(' '):
    if num in nums:
        print("YES")
    else:
        print("NO")
        nums.add(num)
