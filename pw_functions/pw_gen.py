from random import randint, choices
import string
doc_string = """
This program is configured to use 3 positional arguments
1 for Number of Letters in the password
2 for Amount of numbers that the password should contain
3 for Number of symbols in the password
The script gets the length of these 3 elements and combines it to set the total password length

"""

"""
Generating number of special symbols using the string punctuation function
"""


def generate_symbols(number_of_symbols:int):
	symbols = "!@#$%^&*()+="
	# number_of_symbols = int(input("Enter Number of symbols to use: "))
	
	return choices(symbols, k=number_of_symbols)


# print(generate_symbols())
"""
Generating random list of numbers with the string library ascii characters lower and upper
"""


def generate_random_letters(number_of_letters:int):
	letters = string.ascii_lowercase + string.ascii_uppercase
	# number_of_letters = int(input('Enter number of letters: '))
	return (choices(letters, k=number_of_letters))


def random_number():
	return randint(1, 9)




# def random_numbers_list(n:int):
# 	while n!=0:
# 		list_of_numbers.append(random_number())
# 		n -= 1
# 	return map(str, list_of_numbers)
def random_numbers_list(n=5):
    list_of_numbers = []

    global new_list
    new_list = []
    while n!=0:
        list_of_numbers.append(random_number())
        n -= 1
        new_list = [str(x) for x in list_of_numbers]
    return ''.join(new_list)


""" Using while loop in a function to set the amount of numbers to be taken from
A list of numbers between 1 and 100
"""

# symbols = ''.join(generate_symbols(5))
# letters = ''.join(generate_random_letters(12))
# numbers = ''.join(random_numbers_list(3))
# # total_length = len(symbols) + len(letters) + len(numbers)
# final_password = symbols + letters + numbers
# random_password = [ele for ele in final_password]
#
# shuffle(random_password)
# def display_password():
# 	retu
# # print(f"{Fore.CYAN}The Generated Password is:{Fore.RESET} "
# #       f"\n{Fore.RED}{''.join((random_password))}{Fore.RESET}")



