from multiprocessing.sharedctypes import Value
from optparse import Values
from tkinter import font
from turtle import fillcolor
from click import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
from fpdf import FPDF
from PIL import Image


p = "data.csv"
data = pd.read_csv(p)


def fn(data):
    li = []
    di = {}
    for x in data.columns:
        df = data[x]
        if df.dtype == "O":
            di[x] = fn1(df)
        else:
            li.append(x)
            di[x] = fn2(df)
    for i in range(len(li)):
        for j in range(i + 1, len(li)):
            di[li[i] + "-" + li[j]] = fn3(data[li[i]], data[li[j]], li[i], li[j])
    return di


def fn1(df):
    di = {}
    vc = df.value_counts()
    di["Value-count"] = ""
    for i in range(len(vc)):
        di["Value-count"] += str(vc.index[i]) + " " + str(vc[i]) + "\n"

    img = plt.hist(df)
    plt.title("HIST")
    plt.savefig("img1.png")
    img = plt.imread("./img1.png")
    di["img1"] = img
    plt.clf()
    return di


def fn2(df):
    di = {}
    di["Mean"] = df.mean()
    di["Median"] = df.median()
    di["Range"] = str(df.min()) + " - " + str(df.max())
    img = plt.hist(df)
    plt.title("HIST")
    plt.savefig("img2.png")
    img = plt.imread("./img2.png")
    di["img2"] = img
    plt.clf()
    return di


def fn3(df1, df2, x, y):
    di = {}
    img = plt.scatter(df1, df2)
    plt.title("PLOT")
    plt.xlabel(x)
    plt.ylabel
    plt.savefig("img3.png")
    img = plt.imread("./img3.png")
    di["img3"] = img
    plt.clf()
    return di


res = fn(data)
res1 = res.values()
# res1 = pd.DataFrame(res)
with open("data.csv", newline="") as f:
    reader = csv.reader(f)
    pdf = FPDF()

    pdf.add_page()
    pdf.set_font("Times", "B", 20.0)
    pdf.cell(200, 10, "TASK 2", align="C")
    pdf.ln(10)

    pdf.set_font("Courier", "", 12)
    pdf.ln(1)

    th = pdf.font_size
    for i in res:
        pdf.set_author("Teccrown Software")
        pdf.set_font("Times", "I", 22.0)
        # print(res[i])
        pdf.cell(200, 10, i, align="C")
        for col_name in res[i]:

            pdf.set_font("Times", "B", 12.0)
            pdf.ln(10)

            if col_name == "img1":
                pdf.image("img1.png", w=90, h=70, x=60)
            if col_name == "img2" and i == "AGE":
                pdf.image("img2.png", w=90, h=70, x=60)
            if col_name == "img3":
                pdf.image("img3.png", w=90, h=70, x=60)
                continue
            if col_name == "Value-count":
                pdf.multi_cell(
                    200,
                    6,
                    "{}\n \n{}".format(col_name, res[i][col_name]),
                    align="L",
                )

            if col_name == "Mean":
                pdf.multi_cell(
                    200,
                    2,
                    "{}: {}".format(col_name, res[i][col_name]),
                    align="L",
                )

            if col_name == "Median":
                pdf.multi_cell(
                    200,
                    2,
                    "{}: {}".format(col_name, res[i][col_name]),
                    align="L",
                )

            if col_name == "Range":
                pdf.multi_cell(
                    200,
                    2,
                    "{}: {}".format(col_name, res[i][col_name]),
                    align="L",
                )
    pdf.ln(10)
    pdf.cell(200, 0.0, "-------------end of report----------", align="C")

    pdf.output("student.pdf", "F")
