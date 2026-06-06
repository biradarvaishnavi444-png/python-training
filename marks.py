sub1=int(input("Enter subject 1 marks:"))
sub2=int(input("Enter subject 2 marks:"))
sub3=int(input("Enter subject 3 marks:"))
sub4=int(input("Enter subject 4 marks:"))
sub5=int(input("Enter subject 5 marks:"))

total=sub1+sub2+sub3+sub4+sub5
percentages=total/5
print("total marks=",total)
print("percentages=percentages")

if percentages>=75:
    print("Distinction")
elif percentages>=60:
    print("first class")
elif percentages>=45:
    print("pass")
else:
    print("fail")