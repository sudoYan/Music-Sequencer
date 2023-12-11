from time import sleep
import music_sequencer as ms
from musicpy import *
from IPython.display import Audio, display, FileLink
import random

def take_user_input(statement, acceptable_inputs, notation_bool = False):
  """Validates user input with customisable notation option.

  Parameters
  ----------
  statement : str
    Output to print for user requesting input
  acceptable_inputs : list
    List of valid inputs
  notation_bool : bool, default=False
    Whether input is musical notation

  Returns
  ----------
  var
    Valid user input
  """
  unacceptable_bool = True #Initialise invalid user input as True

  #Loop until user input is valid
  while unacceptable_bool == True:

    var = input(statement) #Take user input

    #Loop over list of valid inputs
    for x in acceptable_inputs:

      #Conditional to check whether user input matches valid input
      if var == x:
        unacceptable_bool = False
        break
      #Checks whether notation is sharpened or flattened version of valid inputs
      elif notation_bool == True and (var == (x + '#') or var == (x + 'b')):
        unacceptable_bool = False
        break

    #Conditional to print warning when user input is invalid
    if unacceptable_bool == True:
      print("I wrote this sad little ballad, \nbecause your input is invalid." +
            "\nPlease try again with a proper input.")

  return var #Returns valid user input

def user_interface(list_pieces):
  """Provides normal user interface.

  Returns
  ----------
  music_piece, output : Genre instance
    Built instance of a Genre subclass based on user preferences

  Notes
  ----------
    Generates prototype sequence through sequence() method
  """
  print('This is a music theory based algorithm that can (as of this moment)' +
        ' generate music in 3 genres - Jazz, Country and Pop. If you wish to quit type Q')
  print('Would you like to begin the algorithm or open advanced settings for' +
        'music composition (Choose the first option for first-use)?')

  #Conditional to change from normal interface to advanced interface
  menu_pref = take_user_input('First/Normal Use or Advanced Settings? Press Q to Quit. [N/A/Q]: ', ['N', 'A', 'Q']) 
  if menu_pref == 'A':
    output = advanced_interface(list_pieces)
    if output != None:
      return output
    return None
  #To exit loop if preference is Q
  elif menu_pref == 'Q':
    return False
  else:
    print('To begin, Please select your genre')
    input_genre = take_user_input('Jazz, Country or Pop? [J/C/P]: ', ['J', 'C', 'P'])

    #User input for key chord
    print('Excellent choice. In music theory, there is an alphabetically-ordered' +
          'roster of notes, going from letters A to G, with semitonal variations' +
          ' described by sharps (#) and flats (b).')
    print('This algorithm similarly uses an alphabetically-ordered roster. ' +
          'A diagram can be found here -> https://fireinsidemusic.com/evolution-of-the-piano/.')
    print('A key chord is utilised to decide the scale of a piece. ' +
          'Please choose a note to form the key chord.')
    input_chord = take_user_input('What note is your key chord in: ',
     ['A','B','C', 'D', 'E', 'F', 'G'], True)

    #Conditional to choose path of function based on chosen genre
    if input_genre == 'J':
      print('A chord can be in either major or minor. In jazz music,' +
            'the key scale may be in either major or minor.')
      input_add_chord = take_user_input('Major or minor? [M/m]: ', ['M', 'm'])
      #Conditional to choose add_chord
      if input_add_chord == 'm':
        input_add_chord = 'minor'
      else:
        input_add_chord = 'major'
    else:
      input_add_chord = 'major'

    #Conditional to change wording based on genre chosen to input number of variations
    if input_genre == 'J' or input_genre == 'C':
      print('This genre can have multiple variations in chord progressions over time.' +
            ' How many variations (and correlationally, bars) would you prefer?')
      input_num = int(input('Number of variations: '))
    elif input_genre == 'P':
      print('This genre can have multiple repetitions of the same chord sequence.' +
            ' How many repetitions would you prefer?')
      input_num = int(input('Number of variations: '))

    #Choose name for musical instance
    print('Thank you for your inputs. What would you like to name this creation?')
    input_name = input('Name: ')

    #Conditional to create musical instance based on genre
    if input_genre == 'J':
      music_piece = ms.Jazz(input_name, input_chord, input_add_chord, input_num)
    elif input_genre == 'P':
      music_piece = ms.Pop(input_name, input_chord, input_add_chord, input_num)
    else:
      music_piece = ms.Country(input_name, input_chord, input_add_chord, input_num)

    #Sequence the musical piece to generate prototype audio playback
    music_piece.sequence()

    return music_piece #Returns Genre instance

def advanced_interface(list_pieces):
  """Provides advanced interface for user.

    Parameters
    ----------
    list_pieces : dictionary
      Dictionary of musical instances

    Returns
    ----------
    piece_to_add : Genre instance
      Instance of mixed pieces
    Notes
    ----------
    Generates audio playback for all options
  """
  #Conditional to check whether list_pieces is empty
  if list_pieces == {}:
    print('Sorry, please return to normal settings and create a musical piece first!')
    return None
  else:

    #Set list of piece names
    music_list = list(list_pieces.keys())
    print(f'Welcome to advanced settings! You currently have {len(music_list)} piece(s)' +
          'in your current session. The music list is as follows - ')
    print(music_list)
    print('This algorithm can rerun sequencing on any of these pieces, generate ' +
          'multi-instrumental symphonies and mix pieces together.' +
          ' What would you like to do today?')

    #Conditional to decide which advanced function to run on musical instances
    user_choice = take_user_input('Rerun Sequencing, Generate Symphonies or Mix Pieces together. [R/S/M]: ',
                                  ['R', 'S', 'M'])
    if user_choice == 'R' or user_choice == 'S':
      print('Excellent Idea! Which piece would you like to run this on?')
      user_piece = take_user_input('Enter piece name: ', music_list)

      if user_choice == 'R':
        list_pieces[user_piece].sequence(rerun = True) #Run sequencing
      else:
        list_pieces[user_piece].generate_symph() #Generate symphony

      return None

    else:
      print('Excellent Idea! Which pieces would you like to try this on?')
      print('Would you wish to the harmonize the pieces to a singular key chord, or not?')

      #Boolean regarding transposition of pieces
      if take_user_input('Y/N? ', ['Y', 'N']) == 'Y':
        change_key = True
      else:
        change_key = False

      #Mix pieces
      print('Time to choose your pieces! Note that the key chord will be defined' +
            'by the first piece unless specified!')
      user_piece1 = take_user_input('Enter piece 1 name: ', music_list)
      user_piece2 = take_user_input('Enter piece 2 name: ', music_list)
      piece_to_add = ms.mix_pieces(list_pieces[user_piece1], list_pieces[user_piece2],
                                change_key)

      return piece_to_add #Return Genre instance
