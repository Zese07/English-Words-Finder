import PySimpleGUI as sg
import json

# reads the words_dictionary.json
with open('words_dictionary.json') as file:
    data = json.load(file)


left_layout = [[(sg.Text('English Words Finder\n', font=('', 25, 'bold')))],
               [sg.Text('Words by Length:', font=('', 10, 'bold')),
                (sg.Combo(values=[num for num in range(0, 26)], default_value="0", key='LENGTH', enable_events=True))],
               [(sg.Text('Word:', font=('', 10, 'bold'))),
                (sg.Input(key='INPUT', size=(25, 1), justification='center', enable_events=True))]]

right_layout = [[(sg.Listbox(values=[], enable_events=True, size=(25, 15), key='WORDS'))],
                [(sg.Button('<', key='PREVIOUS')), (sg.Button('>', key='NEXT'))]]

layout = [[sg.Column(left_layout, element_justification='center'), sg.Column(right_layout, element_justification='center')]]

window = sg.Window('English Words Finder', layout, size=(600, 310), element_justification='c', finalize=True)
window.set_icon('icon.ico')

words_list = []
move = False
set = 1

# function for clearing the list
def clear_list():
    words_list.clear()
    window['WORDS'].update(values=words_list)

# function when the length is changed
def words_length():
    if values['LENGTH'] == 0:  # if length is 0
        if values['INPUT'] == '':  # if input is empty and chose 0 then print all words
            for word in data.keys():
                words_list.append(word)

        else:  # if input is not empty and chose 0 then print words that starts with the input
            for word in data.keys():
                if word.startswith(values['INPUT']):
                    words_list.append(word)

    else:  # if length is not 0 then print words that starts with the input with equivalent length
        for word in data.keys():
            if word.startswith(values['INPUT']) and len(word) == values['LENGTH']:
                words_list.append(word)
            else:
                pass

# function for searching the words
def words_search():
    if not values['INPUT'] == '':  # if input is not empty
        if not values['LENGTH'] == 0:  # if length is not 0 then print words that starts with the input with equivalent length
            for word in data.keys():
                if word.startswith(values['INPUT']) and len(word) == values['LENGTH']:
                    words_list.append(word)
                else:
                    pass

        else:  # if length is 0 then print words that starts with the input
            for word in data.keys():
                if word.startswith(values['INPUT']):
                    words_list.append(word)

    else:  # if input is empty
        if values['LENGTH'] == 0:  # if length is 0 then print all words
            for word in data.keys():
                words_list.append(word)

        else:  # if length is not 0 then print words that is equivalent to length
            for word in data.keys():
                if word.startswith(values['INPUT']) and len(word) == values['LENGTH']:
                    words_list.append(word)

# function when previous or next is clicked
def previous_and_next(sign, totalset):
    global set

    if sign == '<':  # if previous
        if not set == 1:
            set -= 1
            window['WORDS'].update(values=words_list[(set * 100) - 100:set * 100])
        else:
            pass

    else:  # if next
        if set < totalset:
            set += 1
            window['WORDS'].update(values=words_list[(set * 100) - 100:set * 100])
        else:
            pass

# function for checking the set of words
def check_set():
    length = len(words_list)
    quotient = length / 100
    remainder = length % 100

    if not remainder == 0:
        remainder = 1
    else:
        pass

    return int(quotient + remainder)


while True:
    move = False
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    elif event == 'LENGTH':  # if length is changed
        clear_list()
        words_length()
        set = 1

    elif event == 'INPUT':  # if search button is clicked
        clear_list()
        words_search()
        set = 1

    elif event == 'PREVIOUS':  # if previous button is clicked
        previous_and_next('<', check_set())
        move = True

    elif event == 'NEXT':  # if next button is clicked
        previous_and_next('>', check_set())
        move = True

    if not move:
        if len(words_list) <= 100:  # if words below 100
            window['WORDS'].update(values=words_list)
        else:  # if words greater than 100 then only prints the first 100
            window['WORDS'].update(values=words_list[:100])


window.close()
