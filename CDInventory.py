#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# CManzuk, 2022-03-06, updated starter code for Asgnmt6
# CManzuk, 2022-03-12, updated for Assignment 7
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of dicts to hold data
dicRow = {}  # dict of data row
strFileName = 'CDInventory'  # data storage filename root
strFileNameTxt = strFileName+'.txt'  # data storage text
strFileNameBin = strFileName+'.bin'  # data storage binary
objFile = None  # file object

import pickle


# Assign06 feedback:
# -Make sure you separate out your IO from your data processing. 
# this particularly comes in the case of TODO 3.3.1 which should have it's
# own IO function but you lumped it into the data processing class
# FIXED FOR ASG7

# ### Assignment 7
# Add structured error handling around the areas where there is 
#     user interaction, 
#     type casting (string to int) or 
#     file access operations.
    
# Modify the permanent data store to use binary data.


# -- PROCESSING -- #
class DataProcessor:

 # >>> MOVED def InputCD_LineItem()to 'class IO' per Asg6  feedback
    
    @staticmethod
    def addCD_LineItem (newRow, table):            # imput parameters as lists
        """Function to append new row of data to existing table

        Makes needed data type conversion, creates dict row from the input list,
        appends to existing table
        
        Args:
            newRow (list): line item elements as strings
            table (list of dict): 2D data structure that holds the data during runtime

        Returns:
            table (list of dict): (same)
        """
  
        # ASG7 - Add Error trap
        
        try:
            dicRow = {'ID': newRow[0], 'Title': newRow[1], 'Artist': newRow[2]} 
                # moved ID str-to-int conversion to IO Fn
        except:
            print("\n\tCheck Data Types\n")

        table.append(dicRow)
        
        return table


    @staticmethod
    def delCD_LineItem (IDselect, table):    # input parameters  int, list
        """Function to delete a selected row of data from existing table

        Takes user's ID selection, converts to list index number, identifies 
        the corresponding row in the table, and deletes it.

        Args:
            IDselect (integer): user selection for row to be deleted
            table (list of dict): 2D data structure that holds the data during runtime

        Returns:
            table (list of dict): 2D data structure that holds the data during runtime
        """
    
        intRowNr = -1
        blnCDRemoved = False

        for row in table:
            intRowNr += 1
            if row['ID'] == IDselect:
                del table[intRowNr]
                blnCDRemoved = True
                break

        if blnCDRemoved:
            print('The CD was removed\n')
        else:
            print('Could not find this CD!')
        
        return table  


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table, binFlag):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from TEXT or BINARY file identified by file_name into a 2D table
        (list of dicts); one line in the file represents one dictionary row in table.
        
        Initial read at startup is an existing text file; Later saves and reads 
        accomplished as binary. Selected by passing flag in function call from Main

        Args:
            file_name (string):     name of file used to read the data from
            table (list of dict):   2D data structure (list of dicts) that holds the data during runtime
            binFlag (bin):          indicates if file is saved as .txt or .bin

        Returns:
            None.
        """
        
        table.clear()  # this clears existing data to allow clean data load from file

    # ASG7 - Add Error trap
    # ASG7 - convert to reading binary >>> added bin capability rather than replace

# DEBUG - getting this mess straight was challenging, esp pickle.load

        try:    
            if binFlag == True:                 # execute read for binary file
            
                objFile = open(file_name , 'rb')     
     
                with open(strFileNameBin , 'rb')  as objFile:
                    table = pickle.load(objFile)   
                
                objFile.close()   
                print("\n\tLoaded " + file_name+" from binary\n")
  # table is actually loading - but the return didn't work for a gooid while
                
            else:                               # execute read for text file
                objFile = open(file_name, 'r')  
    
                for line in objFile:
                    data = line.strip().split(',')
                    dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                    table.append(dicRow)           
    
                objFile.close()            
                print("\n\tLoaded " + file_name+" as text")

        except TypeError:
            print("ERROR - Binary or Text file unclear - returning to main menu")
             
        except IOError:                     # covers both text & bin files
            print("ERROR - File doesn't exist, or points to wrong directory")

        return table            # return value to Main did not work for a while
                                # problem was actually in Main



    @staticmethod
    def write_file(file_name, table):
        """Function to manage data outout from the list of dictionaries to a file

        Writes the data from a 2D table (list of dicts) into a BINARY file
        identified by file_name; one line in the file represents one dictionary
        row in table.

        Args:
            file_name (string):     name of file used to read the data from BINARY file
            table (list of dict):   2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """

    # ASG7 - convert to writing binary
    # ASG7 - Add Error trap

        print("Saving to " + file_name + " as BINARY")
        objFile = open(file_name, 'wb')
            
        pickle.dump(table, objFile)        
    
        objFile.close()
            
        print("Saved")


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print(""" 
            \n\nMenu\n\n
            [l] Load Inventory from file\n
            [i] Display Current Inventory\n
            [a] Add CD\n
            [d] Delete CD from Inventory\n
            [s] Save Inventory to binary file\n
            [x] eXit\n
              """)


    @staticmethod
    def menu_choice():
        """Gets user input for Main Menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """

        choice = ' '
     
      # ASG7 - Add Error trap
     
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            try:
                choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
                print()  # Add extra space for layout
            except (TypeError, ValueError):
                print("\n\tMUST be [l, a, i, d, s or x]\n")
                
        return choice


    @staticmethod
    def InputCD_LineItem():
        """Function to collect new line item data

        Takes input strings and returns a list of the strings

        Args:
            None

        Returns:
            (list): List of line item input strings
            ID (integer): line item ID number     # Chgd: now_integer was_string
            strTitle (string): CD title
            stArtist (string): CD artist
        """

        # ASG7 - Add Error trap

        try:
            intID = int(input('Enter ID: ').strip())        # moved int conversion from function
            strTitle = input('What is the CD\'s title? ').strip()
            stArtist = input('What is the Artist\'s name? ').strip()
            print()
        except (TypeError, ValueError):
            print("\n\tNumbers for IDs, strings for CD/Artist")
        
        return[intID,strTitle,stArtist]     # return a List


    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        
        print('\n======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by: {})'.format(*row.values() ) )
        print('======================================\n\n')


##   M A I N 
# 1. When program starts, read in the currently saved Inventory

FileProcessor.read_file(strFileNameTxt, lstTbl, False)


# 2. start main loop
while True:
    
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()


    # 3. Process menu selection

    # 3.1 process exit first
    if strChoice == 'x':
        break


    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'y\' to continue and reload from file. otherwise reload will be canceled :')

        if strYesNo.lower() == 'y':
            print('\nreloading...\n')
            lstTbl=FileProcessor.read_file(strFileNameBin, lstTbl, True)
    # DEBUG - function call not capturing the return value from function call
    # DUUHHH - forgot "lstTbl=" assignment - return was not being assigned to anything

        else:
            input('\ncanceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.\n')

        print("\n\t\t Updated Table - for verification\n")
        IO.show_inventory(lstTbl)       # trying this - more efficient

        continue  # start loop back at top.


    # 3.3 process add a CD
    elif strChoice == 'a':
        
        # 3.3.1 Ask user for new ID, CD Title and Artist
        
        lstNewRow=[]
        lstNewRow = IO.InputCD_LineItem()

        # Updated InputCD_LineItem function call - has been moved
        # from 'class DataProcessing' per asg6 feedback

        # 3.3.2 Add item to the table

        lstTbl = DataProcessor.addCD_LineItem(lstNewRow,lstTbl)
        print()
        IO.show_inventory(lstTbl)
        
        continue  # start loop back at top.

 
   # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.


    # 3.5 process delete a CD
    elif strChoice == 'd':

        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)

        # 3.5.1.2 ask user which ID to remove

        # ASG7 - Add Error trap
        try:
            intIDdel = int(input('\nWhich ID would you like to delete? \n').strip() )
        except (TypeError, ValueError):
            print("\n\tERROR - Numbers for IDs - back to main menu")
            continue        # on error skip function call, restart menu

        # 3.5.2 search thru table and delete CD
        lstTbl = DataProcessor.delCD_LineItem (intIDdel, lstTbl)
        IO.show_inventory(lstTbl)

        continue  # start loop back at top.


    # 3.6 process save inventory to file
    elif strChoice == 's':
        
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('\nSave this inventory to BINARY file? [y/n] \n').strip().lower()

        # 3.6.2 Process choice
        if strYesNo == 'y':

            # 3.6.2.1 save data
            print("standby...")
            FileProcessor.write_file(strFileNameBin, lstTbl)

        elif strYesNo == 'n':
            input('\nThe inventory was NOT saved to file. Press [ENTER] to return to the menu.\n')

        else:
           input('\nChoose either y or n. Returning to Main Menu\n')

        continue  # start loop back at top.


    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('\nGeneral Error')




