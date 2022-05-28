from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

def first_com():
    img = Image.open('1.jpg')
    img_arr = np.asarray(img)
    plt.axis('off')
    plt.imshow(img_arr)
    plt.show()

def second_com():
    img = Image.open('2.jpg')
    img_arr = np.asarray(img)
    plt.axis('off')
    plt.imshow(img_arr)
    plt.show()

def third_com():
    img = Image.open('3.jpg')
    img_arr = np.asarray(img)
    plt.axis('off')
    plt.imshow(img_arr)
    plt.show()

root = Tk()
root.title("3 лаба")
root.configure(bg="#FFFFFF")
root.geometry('570x125')

lbl=Label(root, text="1) Исходное изображение", font= 20, fg="#000000", bg="#FFFFFF", width = 30)
lbl.grid(row=0, column = 0, columnspan=5)
bttn = Button(root, text="Показать", font= 20, width = 20, bg="#008000", command = first_com)
bttn.grid(row=0, column = 5, columnspan=5)

lbl1=Label(root, text="2) Изображение с шумами", font= 20, fg="#000000", bg="#FFFFFF", width = 30)
lbl1.grid(row=2, column = 0, columnspan=5)
bttn1 = Button(root, text="Показать", font= 20, command = second_com, bg="#008000", width = 20)
bttn1.grid(row=2, column = 5, columnspan=5)

lbl2=Label(root, text="3) Исправленное изображение", font= 20, fg="#000000", bg="#FFFFFF", width = 30)
lbl2.grid(row=4, column = 0, columnspan=5)
bttn2 = Button(root, text="Показать", font= 20, command = third_com, bg="#008000", width = 20)
bttn2.grid(row=4, column = 5, columnspan=5)



root.mainloop()