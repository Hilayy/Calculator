import tkinter as tk


# changes the color of a button that is being hovered on
def hover_on(event):
    event.widget.configure(bg='#2f2f39')


# returns the button to its original color once it stops being hovered on
def hover_off(event):
    event.widget.configure(bg='#33333d')


def superscript(exponent):
    exponent_ss = ''
    # converts each digit of the exponent into its superscript form
    for char in str(exponent):
        if char == '1':
            exponent_ss += chr(0x00B9)
        elif char >= '4' or char == '0':
            exponent_ss += chr(0x2070 + int(char))
        elif char != '-':
            exponent_ss += chr(0x00B0 + int(char))
        else:
            exponent_ss += chr(0x207B)
    return exponent_ss


# solves the input from the calc line and presents it
def convert_to(visual_answer, answer_value):
    global calc_line_text
    global answer
    global error

    # replaces the unicode symbols of the operators with their correspondent python symbol
    visual_answer = visual_answer.replace('\u00F7', '/')
    visual_answer = visual_answer.replace('\u2212', '-')
    visual_answer = visual_answer.replace('\u002B', '+')
    visual_answer = visual_answer.replace('\u00D7', '*')
    visual_answer = '/100*'.join(visual_answer.split('%'))

    # turns implicit multiplication to explicit multiplication and checks for syntax errors such as 'Ans2'
    temp = ''
    for i in range(len(visual_answer)):
        if visual_answer[i:i + 3] == 'Ans':
            if i > 0 and visual_answer[i - 1] not in '+-*/%':
                temp += '*'
            if len(visual_answer) > i + 3 and visual_answer[i + 3].isdigit():
                error = 'Syntax ERROR'
        temp += visual_answer[i]
    visual_answer = temp
    # checks if their are '**' or '//' combinations, that have a function in python but shouldn't work in a
    # calculator, calculation string
    for i in range(len(visual_answer)):
        if (visual_answer[i] == '*' or visual_answer[i] == '/') and visual_answer[i - 1] == visual_answer[i]:
            error = 'Syntax ERROR'

    visual_answer = visual_answer.replace('Ans',
                                          str(answer_value))  # replaces all the 'Ans' instances in the string with
    # their string representation

    visual_answer = eval(visual_answer)
    answer_value = visual_answer

    if float(answer_value) >= 10 ** 100:
        error = 'math'
        return None, None
    if float(answer_value) <= 10 ** -100:
        return '0', 0

    exponent = 0
    # if the number is greater than 10 to the power of 10, stores the power notation of the number and divides the
    # number by it, for later use
    if visual_answer >= 10 ** 10:
        visual_answer /= 10 ** 10
        exponent = 10
        while visual_answer >= 10:
            visual_answer /= 10
            exponent += 1
    visual_answer = str(visual_answer)

    visual_answer = (str(int(float(visual_answer[0:10]))) if float(visual_answer) % 1 == 0 else visual_answer[0:11]
    if 'e' not in visual_answer else visual_answer.split('e')[0][0:11].rstrip('0').rstrip('.') + 'e' +
                                     visual_answer.split('e')[1])
    # cuts the string so there are at most 10 characters in the string not including '.', like in other calculators

    # if the number is greater than 10^10, the answer string shows the number as its scientific notation, using the
    # already divided number and a 'x10^' string
    if exponent != 0:
        visual_answer += f'x10{superscript(exponent)}'
        answer = str(visual_answer)

    if 'e' in visual_answer:
        temp = visual_answer.split('e')
        visual_answer = temp[0] + 'x10' + superscript(temp[1])

    if round(answer_value, 9) % 1 == 0 and 'x' not in visual_answer:
        answer_value = int(answer_value)
        visual_answer = str(answer_value)

    return visual_answer, answer_value


# handles the event of a button being pushed, additionally handles all kinds of errors
def button_click(text):
    global on
    global calc_line_text
    global answer_text
    global answer
    global answer_num
    global error
    error = ''
    if text == 'ON' or (text == 'CE' and on):  # clears the answer and the calculation labels, and if the button clicked
        # is 'ON', also resets the value of 'Ans'
        on = True
        calc_line_text = ""
        answer_text = ""
        if text == 'ON':
            answer = ''
            answer_text = ''
    # if the 'ON' button has already been pushed
    elif on:
        if answer_text != '':  # clears the calc and answer labels when a new expression comes is typed
            calc_line_text = ""
            answer_text = ""
        if text == '=':
            try:
                answer_text, answer_num = convert_to(calc_line_text, answer_num)
                answer = str(answer_text)
            except Exception as e:
                error = e
            if error != '':  # if there is an error
                on = False
                if 'EOF' in str(error) or 'Syntax' in str(error) or 'modulo' in str(error):
                    error = 'Syntax Error'
                else:
                    error = 'Math ERROR'
                calc_line_text = error
                answer_text = "[ON]    : Cancel        "

        else:
            if text in {'\u00F7', '\u00D7', '\u2212', '\u002B',
                        '%'} and answer != '' and calc_line_text == '':  # places
                # 'Ans' before operators in a clear line
                calc_line_text = "Ans"
            if len(calc_line_text + text) <= 17:
                calc_line_text += text

    # updates the strings of the labels
    calc_line_text = str(calc_line_text)
    calc_line.config(text=calc_line_text)
    answer_text = str(answer_text)
    answer_line.config(text=answer_text)


# create window
root = tk.Tk()
root.title('Calculator')
root.iconbitmap(r"C:\Users\User\Pictures\תמונות בשביל עבודות\calc_icon.ico")
root.minsize(500, 800)
root.maxsize(500, 800)

# background
img = tk.PhotoImage(file=r"C:\Users\User\Pictures\תמונות בשביל עבודות\Calculator.png")
label = tk.Label(root, image=img)
label.pack()

# some colors
light_blue = '#80d9d3'
light_red = '#db3550'
white = 'white'

# it could be simpler but i wanted to make everything clear in the code
buttons = [{'text': 'ON', 'color': light_blue}, {'text': 'CE', 'color': light_blue}, {'text': '%', 'color': light_red},
           {'text': '\u00F7', 'color': '#db3550', 'font': ("Helvetica", 28)}, {'text': '7', 'color': white},
           {'text': '8', 'color': white}, {'text': '9', 'color': white}, {'text': '\u00D7', 'color': light_red},
           {'text': '4', 'color': white}, {'text': '5', 'color': white}, {'text': '6', 'color': white},
           {'text': '\u2212', 'color': light_red}, {'text': '1', 'color': white}, {'text': '2', 'color': white}
    , {'text': '3', 'color': white}, {'text': '\u002B', 'color': light_red}, {'text': '0', 'color': white},
           {'text': '.', 'color': white}, {'text': 'Ans', 'color': light_blue}, {'text': '=', 'color': light_red}]

font = ('Helvetica', 28)

# creates a 5x4 matrix of buttons with different text and text color, using the buttons[] list
for i in range(5):
    for j in range(4):
        button = tk.Button(root, text=buttons[0]['text'], width=3, height=1, bg='#33333d',
                           fg=buttons[0]['color'], font=font,
                           command=lambda text=buttons[0]['text']: button_click(text), activebackground='#2f2f39',
                           activeforeground=buttons[0]['color'], borderwidth=8)
        button.bind('<Enter>', hover_on)
        button.bind('<Leave>', hover_off)
        del buttons[0]
        button.place(x=25 + j * 120, y=350 + i * 90)

calc_line_text = ""  # the text that the upper 'calc' label will present
answer_text = ""  # the text that the lower 'answer' label will present
answer_num = None  # the actual value of the text that is shown in the 'answer' label

calc_line = tk.Label(root, text=calc_line_text, width=20, anchor='w', font=('Segue UI', 40), fg='#d7d7d9', bg='#22252d')
answer_line = tk.Label(root, text=answer_text, width=16, anchor='e', font=('Segue UI', 40), fg='#d7d7d9',
                       bg='#22252d')
calc_line.place(y=60, x=0)
answer_line.place(y=220, x=0)
answer = ''
on = False

root.mainloop()
