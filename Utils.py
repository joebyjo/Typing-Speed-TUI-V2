from time import sleep
from math import ceil, floor, isnan
from hashlib import sha256

def hash(password):
    """Hashes given password using sha256"""
    return sha256(password.encode('utf-8')).hexdigest()


def timer(seconds,quiet=False):
    """starts a timer for n seconds. no output is printed if quiet=True"""

    if not quiet:
        for i in range(seconds, 0, -1):
            print(f'{i}', end='')
            sleep(0.2)
            for j in range(4):
                print('.', end='')
                sleep(0.2)

        print('GO!')
        return

    else:
        sleep(seconds)


def clear(n=50):
    """clears the terminal with n newline characters"""
    print('\n'*n)


def average(lst):
    """returns average of elements of a provided list"""
    _sum = sum(lst)
    _len = len(lst)
    return round(_sum/_len,1)


def render_table(headers, data):
    """
    returns provided list() in the form of a clean and readable table
    headers = ("username","Net WPM","Accuracy")
    data = [{"username": "xyz", "Net WPM": 70,"Accuracy":100}]
    ┌───────────────────────────────┐
    │ USERNAME │ NET WPM │ ACCURACY │
    ├───────────────────────────────┤
    │   xyz    │   70    │    100   │
    └───────────────────────────────┘
    """

    num_of_columns = 0
    head = ''
    table_string = ''

    for header in headers:
        greatest_value = max([len(str(x[header])) for x in data])  # find cell in column with greatest length

        # print headers one-by-one
        head += '│ '
        header = header.center(greatest_value).upper()
        head += header + ' '

        num_of_columns += len(header) + 3
    head += '│'

    table_string += '┌' + ('─' * (num_of_columns - 2)) + '─┐' + '\n'
    table_string += head +'\n'
    table_string += '├' + ('─' * (num_of_columns - 2)) + '─┤' + '\n'

    # print data one-by-one
    for item in data:
        for header in headers:
            stats = str(item[header])
            greatest_value = max([len(str(x[header])) for x in data])

            greatest_value = greatest_value if greatest_value > len(header) else len(
                header)  # reassign greatest_value to longest value in entire column to center data

            table_string += '│ '
            table_string += stats.center(greatest_value) + ' '  # center data
        table_string +='│' + '\n'
    table_string +='└' + ('─' * (num_of_columns - 2)) + '─┘\n'

    table_string += '\n' * 3
    return table_string


def render_graph(series, cfg=None):
    """
    Renders a graph using given data in the form
    series = [2,4,3,1,5,3,4,5,2,3,3,3,2,4,4]

      5 ┤   ╭╮ ╭╮
      4 ┤╭╮ ││╭╯│    ╭─
      3 ┤│╰╮│╰╯ │╭──╮│
      2 ┼╯ ││   ╰╯  ╰╯
      1 ┤  ╰╯
        └────────────────────

    modified version of https://github.com/kroitor/asciichart/blob/master/asciichartpy/__init__.py
    """

    series = series[len(series) - 80:] if len(series) > 80 else series

    def _isnum(n):
        return not isnan(n)

    if len(series) == 0:
        return ''

    if not isinstance(series[0], list):
        if all(isnan(n) for n in series):
            return ''
        else:
            series = [series]

    cfg = cfg or {}

    colors = cfg.get('colors', [None])

    minimum = cfg.get('min', min(filter(_isnum, [j for i in series for j in i])))
    maximum = cfg.get('max', max(filter(_isnum, [j for i in series for j in i])))

    default_symbols = ['┼', '┤', '╶', '╴', '─', '╰', '╭', '╮', '╯', '│','└']
    symbols = cfg.get('symbols', default_symbols)

    if minimum > maximum:
        raise ValueError('The min value cannot exceed the max value.')

    interval = maximum - minimum
    offset = cfg.get('offset', 3)
    height = cfg.get('height', interval)
    ratio = height / interval if interval > 0 else 1

    min2 = int(floor(minimum * ratio))
    max2 = int(ceil(maximum * ratio))

    def clamp(n):
        return min(max(n, minimum), maximum)

    def scaled(y):
        return int(round(clamp(y) * ratio) - min2)

    rows = max2 - min2

    width = 0
    for i in range(0, len(series)):
        width = max(width, len(series[i]))
    width += offset

    placeholder = cfg.get('format', '{:3.0f}')

    result = [[' '] * width for i in range(rows + 1)]

    # axis and labels
    for y in range(min2, max2 + 1):
        label = placeholder.format(maximum - ((y - min2) * interval / (rows if rows else 1)))
        result[y - min2][max(offset - len(label), 0)] = label
        result[y - min2][offset - 1] = symbols[0] if y == 0 else symbols[1]  # zero tick mark

    # first value is a tick mark across the y-axis
    d0 = series[0][0]
    if _isnum(d0):
        result[rows - scaled(d0)][offset - 1] = symbols[0]

    for i in range(0, len(series)):

        color = colors[i % len(colors)]

        # plot the line
        for x in range(0, len(series[i]) - 1):
            d0 = series[i][x + 0]
            d1 = series[i][x + 1]

            if isnan(d0) and isnan(d1):
                continue

            if isnan(d0) and _isnum(d1):
                result[rows - scaled(d1)][x + offset] = symbols[2]
                continue

            if _isnum(d0) and isnan(d1):
                result[rows - scaled(d0)][x + offset] = symbols[3]
                continue

            y0 = scaled(d0)
            y1 = scaled(d1)
            if y0 == y1:
                result[rows - y0][x + offset] = symbols[4]
                continue

            result[rows - y1][x + offset] = symbols[5] if y0 > y1 else symbols[6]
            result[rows - y0][x + offset] = symbols[7] if y0 > y1 else symbols[8]

            start = min(y0, y1) + 1
            end = max(y0, y1)
            for y in range(start, end):
                result[rows - y][x + offset] = symbols[9]

    length_of_graph = (max([len(a) for a in result])-offset)
    x_axis = ' '*(offset+1) + symbols[10] + (symbols[4] * (length_of_graph if length_of_graph>20 else 20))

    result.append(x_axis)

    return '\n'.join([''.join(row).rstrip() for row in result])


if __name__ == '__main__':
    # -----Used during developement----- #
    #
    # headers = ('userInput', 'timeTaken', 'netWPM', 'grossWPM', 'Accuracy', 'Error')
    #
    # data = [{'String': 'premium hang capricious ancient mysterious', 'userInput': 'premium hang capricious ancient mysterious', 'timeTaken': 10.4, 'netWPM': 48, 'grossWPM': 48, 'Accuracy': 100, 'Error': 0},
    #         {'String': 'governor utter vacuous bulb test', 'userInput': 'governor utter vacous bulb test', 'timeTaken': 7.2, 'netWPM': 47, 'grossWPM': 52, 'Accuracy': 88, 'Error': 3},
    #         {'String': 'prevent education obese changeable fade', 'userInput': 'prevent education obese changeable fade', 'timeTaken': 7.5, 'netWPM': 62, 'grossWPM': 62, 'Accuracy': 100, 'Error': 0}]
    #
    # headers = ("username", 'time', 'netwpm', 'grosswpm','accuracy')
    # data = [
    #     {'username': 'joe', 'time': 4, 'netwpm': 70, 'grosswpm': 70,'accuracy':100},
    #     {'username': 'joe', 'time': 4, 'netwpm': 70, 'grosswpm': 70,'accuracy':100},
    #     {'username': 'joe', 'time': 4, 'netwpm': 70, 'grosswpm': 70,'accuracy':100},
    # ]
    #
    # render_table(headers, data)
    #
    # timer(3)
    # clear()

    data = [('joe', 20.0, 23.0, 2.3, 52.5, 3.5, 100.0), ('xyz', 20.0, 23.0, 2.3, 52.5, 3.5, 100.0)]
    headers = ('UserName', 'Highscore NWPM','Highscore GWPM','HighScore Time', 'AVG wpm', 'avg accuracy', 'avg time')
    data = [{headers[i]:attr for i, attr in enumerate(row)} for row in data]
    render_table(headers,data)