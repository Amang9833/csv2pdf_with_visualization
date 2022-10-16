from multiprocessing.sharedctypes import Value
from optparse import Values
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
from fpdf import FPDF

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
    plt.savefig("img.png")
    img = plt.imread("./img.png")
    di["img1"] = img
    plt.clf()
    return di


def fn2(df):
    di = {}
    di["mean"] = df.mean()
    di["median"] = df.median()
    di["range"] = str(df.min()) + " - " + str(df.max())
    img = plt.hist(df)
    plt.title("HIST")
    plt.savefig("img.png")
    img = plt.imread("./img.png")
    di["img1"] = img
    plt.clf()
    return di


def fn3(df1, df2, x, y):
    di = {}
    img = plt.scatter(df1, df2)
    plt.title("PLOT")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.savefig("img.png")
    img = plt.imread("./img.png")
    di["img1"] = img
    plt.clf()
    return di


res = fn(data)
res1 = res.values()
# res1 = pd.DataFrame(res)
# print(res1)
with open("data.csv", newline="") as f:
    reader = csv.reader(f)
    pdf = FPDF()

    pdf.add_page()
    page_width = pdf.w - 2 * pdf.l_margin
    # print(res)
    pdf.set_font("Times", "B", 14.0)
    pdf.cell(page_width, 0.0, "TASK 2", align="C")
    pdf.ln(10)

    pdf.set_font("Courier", "", 12)

    col_width = page_width / 4

    pdf.ln(1)

    th = pdf.font_size
    # for row in res1:

    #     pdf.cell(col_width, th, res1, border=1)

    #     pdf.ln(th)
    for i in res:
        for col_name in res.keys():
            print(col_name)
            pdf.cell(page_width, 0.0, col_name, align="C")
            pdf.ln(10)
            pdf.cell(col_width, th,, border=1)

    pdf.ln(10)

    pdf.set_font("Times", "", 10.0)
    pdf.cell(page_width, 0.0, "- end of report -", align="C")

    pdf.output("student.pdf", "F")
