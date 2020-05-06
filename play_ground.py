import tkinter as tk

root = tk.Tk()
root.title("Thinter Test")
root.geometry("400x300")

def push1():
    textBox.delete(0, tk.END)
    textBox.insert(tk.END, "push1")
def push2():
  print("push2")
def push3():
  print("push3")

btn1 = tk.Button(root, text="Button1", width="20",command=push1)
btn1.place(x=10, y=10)
btn2 = tk.Button(root, text="Button2", width="20", command=push2)
btn2.place(x=10, y=40)
btn3 = tk.Button(root, text="Button3", width="20", command=push3)
btn3.place(x=10, y=70)

textBox = tk.Entry(root)
textBox.place(x=200, y=10)

root.mainloop()
