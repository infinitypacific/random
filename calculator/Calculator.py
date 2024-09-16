import tkinter as tk

window = tk.Tk()
window.title("Calculator")
window.geometry("300x300")

operator = ""
lastnum = ""
num1 = ""
eq = ""


def updateRes():
  global operator, lastnum, num1
  lastnum = int(lastnum)
  if operator == "+":
    num1 += lastnum
    updateText(num1)
  elif operator == "-":
    num1 -= lastnum
    updateText(num1)
  elif operator == "*":
    num1 *= lastnum
    updateText(num1)
  elif operator == "/":
    num1 /= lastnum
    updateText(num1)
  operator = ""
  lastnum = str(num1)
  num1 = ""


def clrlast():
  global lastnum
  lastnum = ""
  updateText(0)


def buttonChoice(num):
  global lastnum, eq, num1, operator
  lastnum += str(num)
  eq = f"{num1}{operator}{lastnum}"
  updateText(eq)


def operatorChoice(choice):
  global lastnum, num1, operator, eq
  num1 = int(lastnum)
  lastnum = ""
  eq = f"{num1}{choice}"
  operator = choice
  updateText(eq)


def updateText(var):
  result["text"] = var


result = tk.Label(text=0)
result.grid(row=0, column=1)

one = tk.Button(text="1", command=lambda: buttonChoice(1)).grid(row=1,
                                                                column=0)
two = tk.Button(text="2", command=lambda: buttonChoice(2)).grid(row=1,
                                                                column=1)
three = tk.Button(text="3", command=lambda: buttonChoice(3)).grid(row=1,
                                                                  column=2)
four = tk.Button(text="4", command=lambda: buttonChoice(4)).grid(row=2,
                                                                 column=0)
five = tk.Button(text="5", command=lambda: buttonChoice(5)).grid(row=2,
                                                                 column=1)
six = tk.Button(text="6", command=lambda: buttonChoice(6)).grid(row=2,
                                                                column=2)
seven = tk.Button(text="7", command=lambda: buttonChoice(7)).grid(row=3,
                                                                  column=0)
eight = tk.Button(text="8", command=lambda: buttonChoice(8)).grid(row=3,
                                                                  column=1)
nine = tk.Button(text="9", command=lambda: buttonChoice(9)).grid(row=3,
                                                                 column=2)
zero = tk.Button(text="0", command=lambda: buttonChoice(0)).grid(row=4,
                                                                 column=1)

plus = tk.Button(text="+", command=lambda: operatorChoice("+")).grid(row=1,
                                                                     column=3)
minus = tk.Button(text="-", command=lambda: operatorChoice("-")).grid(row=1,
                                                                      column=4)
clr = tk.Button(text="AC", command=clrlast).grid(row=1, column=5)
mult = tk.Button(text="*", command=lambda: operatorChoice("*")).grid(row=2,
                                                                     column=3)
div = tk.Button(text="/", command=lambda: operatorChoice("/")).grid(row=2,
                                                                    column=4)
equals = tk.Button(text="=", command=updateRes).grid(row=4, column=3)
tk.mainloop()