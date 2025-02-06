from random import choice


def get_words(hard=False, count=7):
    """
    Get words from word_list_hard.txt/word_list_easy.txt depending on specified mode
    file which returns a random selection of words in the form of a list
    """
    hard_mode = "word_list_hard.txt"
    easy_mode = "word_list_easy.txt"

    word_list_file = hard_mode if hard else easy_mode
    count = count-2 if hard else count

    # get words from word_list_hard.txt
    with open(word_list_file, "r") as f:
        word_list = f.read()
        word_list = word_list.split("\n")

    words = []
    # choose 5 random words from word_list and append to words if its not there
    for i in range(count):
        word = choice(word_list)
        if word not in words:
            words.append(word)

    return words


def accuracy(input_text, text):
    """
    calculates accuracy of typing speed by comparing
    input_text and text on the basis of number of errors
    """

    # remove anti-cheat char from text
    text = text.replace("\u200e ", " ")
    error = 0

    text_lst = text.split()
    inp_lst = input_text.split()

    for i, c in enumerate(text_lst):
        for itr, cont in enumerate(c):
            try:
                if inp_lst[i][itr] == cont:
                    continue

                elif inp_lst[i][itr] != cont:
                    error += 1

            except IndexError:
                pass

    if len(input_text) > len(text):
        error += 2 * (len(input_text) - len(text))

    accuracy = ((len(input_text) - error) / len(text)) * 100

    if accuracy < 0:
        accuracy = 0.0

    return round(accuracy), error


def gross_wpm(input_text, total_time):
    """
    returns gross_wpm(wpm without accounting for errors)
    formula:

        length of input_text x 60
        —————————————————————————
             5  x  time_taken

    """
    wpm = len(input_text) * 60 / (5 * total_time)
    return round(wpm)


def net_wpm(input_text, text, total_time):
    """
    returns net_wpm(wpm accounting for errors)
    formula:

        (length of input_text - errors) x 60
        ————————————————————————————————————
                 5   x   time_taken

    """

    errors = (accuracy(input_text, text))[1]
    wpm = ((len(input_text) - errors) * 60) / (total_time * 5)
    if wpm > 0:
        return round(wpm)
    else:
        return 0


if __name__ == '__main__':
    # -----Used during developement----- #

    # print(get_words())

    inputText = 'album blade future farm high camel rulinggg'
    text = 'album blade future farm high camel ruling'

    print(accuracy(inputText, text))


    # word_list_file = "word_list_hard.txt"
    #
    # # get words from word_list_hard.txt
    # with open(word_list_file, "r") as f:
    #     word_list = f.read()
    #     word_list = word_list.split("\n")
    #
    # word_list.sort(key=len)
    # print(word_list)

    # print(net_wpm("puzzling bear employ flame entertain","puzzling bear employ flame entertain",5.5))

