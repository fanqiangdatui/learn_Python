def func():
    strlist = input().strip().split()
    strlist = "".join(strlist)
    strN = input().strip()
    countN = 0
    for i in strlist:
        if i == strN or i.upper() == strN or i.lower() == strN:
            countN = countN + 1
    print(countN)
if __name__ == "__main__":
    func()
