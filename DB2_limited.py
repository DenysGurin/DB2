import re

def handle_numbers(number1, number2, number3):
    
    if type(number1) != int and type(number2) != int:
            raise "Invalid input, function need number1(int), number2(int), number3 as parameters"
    
    try:
        why = ""
        count = 0
        
        for number in range(number1, number2+1):
            if number % number3 == 0:
                count += 1
                why += "%s, " % (number)
    
        if len(why) > 0:
            why = why[:-2]
        else:
            why = "no numbers"
        
        return "Result:\n{count}, because {why} are divisible by {number3}".format(count=count, why=why[:-2], number3=number3)
        
    except ZeroDivisionError:
        print("number3 can't be Zero") 
        
    except TypeError:
        print("function handle_numbers() need number1(int), number2(int), number3 as parameters") 
        
    
print(handle_numbers(1, 10, 2)) 
print(handle_numbers(1, 1, 2))   
#print(handle_numbers(3, 12, 2))
#print(handle_numbers(1, 10, 3))
#print(handle_numbers(1, 12, 3))
#print(handle_numbers(1, 12, 2.5))
#print(handle_numbers(1, 12, 0))


def hendle_string(value):
    
    try:
        
        if type(value) != str:
            raise "Invalid input, function need str as parameter"
        
        letters = 0
        digits = 0
        
        for s in value:
            if re.match(r'[a-zA-Z]', s):
                letters += 1
            elif re.match(r'\d', s):
                digits += 1
                
        return "Result:\nLetters -  {letters}\nDigits -  {digits}".format(letters=letters,digits=digits)
        
    except TypeError:
        print("function hendle_string() need str as parameter") 
        
    
print(hendle_string("Hello world! 123!"))


def handle_list_of_tuples(list_):
    
    sorted_list = sorted(list_, key=lambda x: (x[0], -int(x[1]), -int(x[2]), -int(x[3])))
    
    return sorted_list
    
print(handle_list_of_tuples([("Tom", "19", "167", "54"), 
                            ("Jony", "24", "180", "69"),
                            ("Json", "21", "185", "75"),
                            ("John", "27", "190", "87"), 
                            ("Jony", "24", "191", "98"), 
                            ]))