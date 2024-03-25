import re
import json





#The last dictionary, overwrites the previous dictionary
list_of_dictionaries = ["Plover_main_without_compound_words", #Lowest priority
                        "Lapwing",
                        "Lapwing_UK",
                        "Harri_additions_with_Lapwing_logic",
                        "Jos+Mir-Plover",
                        "Harri_additions_with_Josiah_logic",
                        "Harri_additions_with_Lapwing&Josiah_logic",
                        "Harri_additions_with_Jeff_logic",
                        "Harri_personal_titles",
                        "Harri_personal_biology",
                        "Harri_personal_one_handed_fingerspelling",
                        "Harri_personal_subscript",
                        "st_ft_switching",
                        "make_z_use_asterisk-Z",
                        "Harri_personal_user"
                        ] #Highest priority











LONGEST_KEY = 4


import os
cwd = os.getcwd()

numbers_to_letters = {
    "1": "S",
    "2": "T",
    "3": "P",
    "4": "H",
    "5": "A",
    "6": "F",
    "7": "P",
    "8": "L",
    "9": "T",
    "0": "O"
    }

def aericks_denumberizer(old_outline):

    old_strokes = old_outline.split("/")
    new_strokes = []

    for stroke in old_strokes:

        new_strokes.append(stroke)

        for match in numbers_to_letters.keys():

            if match in stroke:

                if new_strokes[-1][0] != "#":
                    new_strokes[-1] = "#" + new_strokes[-1]

                new_strokes[-1] = new_strokes[-1].replace(match, numbers_to_letters[match])

        if new_strokes == []:
            new_strokes = old_strokes

    return "/".join(new_strokes)




def collapse_outlines(dictionary_file, collapsed_dictionary = {}, force_cap=False):
    #The latest addition overwrites the previous entry at that location
    with (open(dictionary_file, "r", encoding="utf-8")) as temp_dictionary:                                        #debug
    #with (open('C:\\Users\\harrry\\AppData\\Local\\plover\\plover\\' + dictionary_file, "r", encoding="utf-8")) as temp_dictionary: #Windows
    #with (open("Library/Application Support/plover/"+ dictionary_file, "r", encoding="utf-8")) as temp_dictionary: #Macintosh
    #with (open(".config/plover/"+ dictionary_file, "r", encoding="utf-8")) as temp_dictionary:                      #Linux
        temp_dictionary = json.load(temp_dictionary)
        for outline in temp_dictionary:
            translated_phrase = temp_dictionary[outline]
            if force_cap:
                if translated_phrase[0] == "{":
                    translated_phrase = "{" + translated_phrase[1].upper() + translated_phrase[2:]
                else:
                    translated_phrase = translated_phrase[0].upper() + translated_phrase[1:]
            
            outline = aericks_denumberizer(outline)



            unchecked_outlines_to_add = [str(outline)]
            checked_outlines_to_add = []
            while unchecked_outlines_to_add:
                working_outline =  unchecked_outlines_to_add.pop()


                match = re.fullmatch(r'([#^STKPWHRAO\-\*EUFRPBLGTSDZ]+)/([#^STKPWHRAO\-\*EUFRPBLGTSDZ]+).*', working_outline)


                if match:
                    if match[1] == str(match[2]).replace("*",""):
                        print(match[1]+" is the same as "+match[2])
                        unchecked_outlines_to_add.append('&'+working_outline)


                checked_outlines_to_add.append(working_outline)
                ###########check for duplicates
                unchecked_outlines_to_add =  list(set(unchecked_outlines_to_add) - set(checked_outlines_to_add))

            #checked_outlines_to_add.pop(0) #The original outline is valid but like, obviously I've already got it
            for um_outline in checked_outlines_to_add:
                if not um_outline == checked_outlines_to_add[0]:
                    collapsed_dictionary[str(um_outline.replace("X",''))] = translated_phrase

    return collapsed_dictionary




collapsed_dictionary = {}
reverse_lookup_dictionary = {}

#Send everything through capped and add #
for dictionary in list_of_dictionaries:
    collapsed_dictionary = collapse_outlines(dictionary + ".json", collapsed_dictionary, True)
#Send everything through normally
for dictionary in list_of_dictionaries:
    collapsed_dictionary = collapse_outlines(dictionary + ".json", collapsed_dictionary)




#reverse_dictionary = {translated_phrase:outline for outline,translated_phrase in collapsed_dictionary.items()} 

#collapsed_dictionary['-PG'] = str(len(collapsed_dictionary))


def lookup(strokes):

    outline = "/".join(strokes)
    outline = aericks_denumberizer(outline)

    return collapsed_dictionary[outline]

with open("Doubles.json", "w") as outfile:
    json.dump(collapsed_dictionary, outfile, indent=0)




"""
#def reverse_lookup(translated_phrase):

    This don't work cause you can't alter what goes in, only what comes out
    outline = "/".join(strokes)

    return {key for key,value in collapsed_dictionary.items() if value==outline }
    
    #return reverse_dictionary
"""


#print(lookup(("^PHAOE","TPHOE")))
#print(lookup(("#TPHOS","KOEPL","KWRAL")))
#print(lookup("^SKWRABGS")) Nos comb amino acid

#print(reverse_lookup(("reverse"))) okay huh
