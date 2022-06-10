import PySimpleGUI as sg

# Buttons Setting
title = {'size': (25, 1),
         'justification':  'left',
         'background_color': '#272533', 
         'text_color': 'white', 
         'font': ('DK Lemon Yellow Sun',  16, 'bold')
        }

display = {'size': (25, 1),
         'justification':  'right',
         'background_color': 'white', 
         'text_color': 'black', 
         'font': ('Calculator',  48, 'bold'),
         'relief': 'sunken',
         'key': '_display_'
        }

oper = {'size': (7, 2), 
        'font': ('Calculator', 24), 
        'button_color': ("black","#F8F8F8")
        }

num = {'size': (7, 2),  
        'font': ('Calculator', 24), 
        'button_color': ("black","#F1EABC")
        }

equals = {'size': (50, 1), 
        'font': ('Calculator', 24), 
        'button_color': ("black","#ECA527"),
        'focus': True,
        'bind_return_key': True
        }

# Overall Layout
layout = [
    [sg.Text('computandi', **title)],
    [sg.Text('0.0000', **display)],
    [sg.Button('7',**num), sg.Button('8',**num), sg.Button('9',**num), sg.Button('C',**oper), sg.Button('CE',**oper)],
    [sg.Button('4',**num), sg.Button('5',**num), sg.Button('6',**num), sg.Button('^',**oper), sg.Button("//",**oper)],
    [sg.Button('1',**num), sg.Button('2',**num), sg.Button('3',**num), sg.Button("*",**oper), sg.Button("/",**oper)],    
    [sg.Button('0',**num), sg.Button('.',**num), sg.Button('%',**oper), sg.Button("+",**oper), sg.Button("-",**oper)],
    [sg.Button('=',**equals)]
]

window = sg.Window('Computandi', size=(560, 600), layout=layout, 
                   background_color="#272533", return_keyboard_events=True)

# Functionality
class Calculator():
        def __init__(self):
                self.current_display = {'whole_number': [], 'fractional_part': [],
                                        'decimal': False, 'x_val': 0.0, 
                                        'y_val': 0.0, 'result':0.0, 'operator': ''}

        def format_number(self):
                """ formats the number to combine both whole number 
                    and fractional part of a number """
                formatted_number = float(f"{''.join(self.current_display['whole_number'])}.{''.join(self.current_display['fractional_part'])}")
                return formatted_number

        def update_display(self, display_value):
                """ updates the calculator display """
                try:
                        window['_display_'].update(value='{:,.4f}'.format(display_value))
                except:
                        window['_display_'].update(value=display_value)

        def number_func(self, event):
                """ functionality of the number buttons """
                if self.current_display['decimal']:
                        self.current_display['fractional_part'].append(event)
                else:
                        self.current_display['whole_number'].append(event)
                self.update_display(self.format_number())

        def operator_func(self, event):
                """ operator button functionality """
                self.current_display['operator'] = event
                try:
                        self.current_display['x_val'] = self.format_number()
                except:
                        self.current_display['x_val'] = self.current_display['result']
                self.clear_func()
                
        def clear_func(self):
                """ clear button events """
                self.current_display['whole_number'].clear()
                self.current_display['fractional_part'].clear()
                self.current_display['decimal'] = False 

        def equal_func(self):   
                """ equals button functionality """
                self.current_display['y_val'] = self.format_number()
                try:
                        if self.current_display['operator'] != '^':
                                self.current_display['result'] = eval(str(self.current_display['x_val']) 
                                                                      + self.current_display['operator'] 
                                                                      + str(self.current_display['y_val']))
                        else:
                                self.current_display['result'] = eval(str(self.current_display['x_val']) 
                                                                      + '**' 
                                                                      + str(self.current_display['y_val']))
                        self.update_display(self.current_display['result'])
                        self.clear_func()
                except:
                        self.update_display("Math ERROR")
                        self.clear_func()

# Main Event
calc = Calculator()
while True:
    event, values = window.read()
    if event is None:
        break
    if event in ['0','1','2','3','4','5','6','7','8','9']:
        calc.number_func(event)
    if event in ['+','-','*', '^', '/', '//', '%']:
        calc.operator_func(event)
    if event in ['Escape:27','C','CE']: # 'Escape:27 is for keyboard control
        calc.clear_func()
        calc.update_display(0.0)
        calc.current_display['result'] = 0.0
    if event == '.':
        calc.current_display['decimal'] = True
    if event == '%':
        calc.update_display(calc.current_display['result'] / 100.0)
    if event == '=':
        calc.equal_func()