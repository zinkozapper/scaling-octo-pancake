'''colby seeley
this funcion is to add'''

def add_2_num(iNum1,iNum2):
    return round(iNum1 + iNum2,2)

while True:
    try:
        iNum1 = float(input("Pick a number. "))
        iNum2 = float(input("Pick another number. "))
        break
    except:
        print("Invalid input. Try again.")

print(add_2_num(iNum1, iNum2))