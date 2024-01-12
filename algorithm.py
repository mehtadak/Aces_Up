################################################################################
#   Computer Project #10
#
# import cards (provided file)
# init_game():
#   Calls methods from Cards to initialize a new game
#   Uses for loop to initialize tableau with the first 4 cards
# deal_to_tableau():
#   Uses for loop nested within if-else statement to deal new cards to tableau
# validate_move_to_foundation():
#   Uses nested for loops and if-else statements to check is the card move to
#   foundation is legal. Prints error messages if move is illegal
# move_to_foundation():
#   Calls the validate_move_to_foundation to move the requested card to the
#   foundation. Uses a if statement to check for validity of the move
# validated_move_within_tableau():
#   Uses nested if-else to check if card can be moved to an empty tableau column
# validate_move_within_tableau():
#   Calls the validate move_within_tableau to move the requested card to the
#   tableau column. If statement to check the validity of the move
# check_for_win():
#   Checks if the user has won using for loop and if-else statement
# display():
#   Given function
# get_option():
#   Uses nested if-else statement to get an option from user and display error
#   messages when recieving the incorrect input
# main():
#   Calls various functions based on user input and displays rules, menu and the
#   current state of the game
################################################################################

import cards  # required !!!

RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card 
     of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.
'''

MENU = '''     
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''
def init_game():
    '''
    Initializes the variables to be used in the program
    Returns: a Tuple
    '''
    deck = cards.Deck() # calls class Deck from cards file
    deck.shuffle() # calls the shuffle method from the class Deck
    tableau = []
    foundation = []
    for i in range(4):
        temp_list = [deck.deal()] # deals cards to each tableau
        tableau.append(temp_list)
    stock = deck
    return (stock, tableau, foundation)
    
def deal_to_tableau(tableau, stock):
    '''
    Deals one card to each column in the tableau
    Returns: Nothing
    '''
    if len(stock) >= 4:
        for x in tableau:
            x.append(stock.deal()) # appends the card to column in the tableau
    else:
        for i in range(len(stock)):
            tableau[i].append(stock.deal())
           
def validate_move_to_foundation( tableau, from_col ):
    '''Validates if the move is correct or not
    Returns: boolean True or False'''
    if tableau[from_col] == []:
        print("\nError, empty column: {:}".format(from_col))
        return False
    else:
        for col in tableau: #goes through each column in tableau
            if col != []:
                if col == from_col:
                    continue
                else:
                    if tableau[from_col][-1].rank() == 1:
                        #printing error message
                        print("\nError, cannot move {}."
                              .format(tableau[from_col][-1]))
                        return False
                    elif col[-1].suit() == tableau[from_col][-1].suit():
                        if col[-1].rank() > tableau[from_col][-1].rank() \
                            or col[-1].rank() == 1:
                            return True
                    else:
                        continue
        #printing error message
        print("\nError, cannot move {}.".format(tableau[from_col][-1]))
        return False
    
def move_to_foundation( tableau, foundation, from_col ):
    '''Moves the card from the tableau to the foundation
    Returns: Nothing'''
    boo = validate_move_to_foundation(tableau, from_col) #calls function
    if boo is True:
        temp = tableau[from_col].pop(-1) #pop method to remove the card
        foundation.append(temp)  

def validate_move_within_tableau( tableau, from_col, to_col ):
    '''Validates is the move is correct or not
    Returns: Boolean True or False'''
    if tableau[to_col] != []:
        #printing error message
        print("\nError, target column is not empty: {:}".format(int(to_col)+1))
        return False
    else:
        if tableau[from_col] == []:
            #printing error message
            print("\nError, no card in column: {:}".format(int(from_col)+1))
            return False
        else:
            return True

def move_within_tableau( tableau, from_col, to_col ):
    '''Moves the card to the column in tableau
    Returns: Nothing'''
    boo = validate_move_within_tableau(tableau, from_col, to_col)
    if boo == True:
        temp = tableau[from_col].pop(-1)#pop method the remove the card
        #appends the popped card to the empty column in tableau
        tableau[to_col].append(temp)  
    
def check_for_win( tableau, stock ):
    '''Checks if the user has won or not
    Returns: Boolean True or False'''
    n = 0
    i = 0
    for col in tableau:
        for x in col:
            if x.rank() == 1: #calls the rank method
                n+=1
            else:
                i+=1
    if stock.is_empty() == True and n == 4 and i == 0:#calls the is_empty method
        return True
    else:
        return False

def display( stock, tableau, foundation ):
    '''Provided: Display the stock, tableau, and foundation.'''
    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))
    maxm = 0
    for col in tableau:
        if len(col) > maxm:
            maxm = len(col)
    
    assert maxm > 0   # maxm == 0 should not happen in this game?
        
    for i in range(maxm):
        if i == 0:
            if stock.is_empty():
                print("{:<8s}".format(""),end='')
            else:
                print("{:<8s}".format(" XX"),end='')
        else:
            print("{:<8s}".format(""),end='')        
        
        #prior_ten = False  # indicate if prior card was a ten
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print( "{:4s}".format( str(col[i]) ), end='' )

        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')
                
        print()

def get_option():
    returned = []
    ans = input("\nInput an option (DFTRHQ): ")
    a = ans.lower().strip()
    a_list = a.split()
    if a == 'd':
        returned = ['D']
    elif len(a_list) == 2:
        if a_list[0] == 'f' and a_list[1].isdigit() == True:
            if int(a_list[1]) in range(1,5):
                returned = ['F', int(a_list[1])-1]
            else:
                print("\nError in option: {}".format(ans))
        else:
            print("\nError in option: {}".format(ans))
    elif len(a_list) == 3:
        if a_list[0] == 't' and a_list[1].isdigit() == True \
            and a_list[2].isdigit() == True:
            if int(a_list[1]) in range (1,5) and int(a_list[2]) in range(1,5):
                returned = ['T', int(a_list[1])-1, int(a_list[2])-1]
            else:
                print("\nError in option: {}".format(ans))
        else:
            print("\nError in option: {}".format(ans))
    elif a == 'r':
        returned = ['R']
    elif a == 'h':
        returned = ['H']
    elif a == 'q':
        returned = ['Q']
    else:
        print("\nError in option: {}".format(ans))
        returned = []
    return returned  

def main():
    print(RULES)
    print(MENU)
    game = init_game() #initializes a new game
    display(game[0], game[1], game[2])#display the game status
    while True:#Loops till the user wants to play
        ans = get_option()
        if ans == []:
            continue
        else:
            if ans == ['D']:
                deal_to_tableau(game[1], game[0])
            elif ans[0] == 'F':
                move_to_foundation(game[1], game[2], ans[1])
            elif ans[0] == 'T':
                move_within_tableau(game[1], ans[1], ans[2])
            elif ans == ['R']:
                print("\n=========== Restarting: new game ============")
                print(RULES)
                print(MENU)
                game = init_game()
                display(game[0], game[1], game[2])
                continue #skips the part below and loops again
            elif ans == ['H']:
                print(MENU)
            elif ans == ['Q']:
                print("\nYou have chosen to quit.")
                break #Exits the game when the user wants to quit
            if check_for_win(game[1], game[0]) == True:
                print("\nYou won!")
                # Exits the game  when the user wins the game
                break
            display(game[0], game[1], game[2])#display the game status


if __name__ == '__main__':
    main()