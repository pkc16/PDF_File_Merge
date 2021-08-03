# Simple app which takes two pdf files and combines them into a single pdf file

from tkinter import *
from tkinter import filedialog, messagebox
import os
import PyPDF2

class SimpleWindow(object):

    def __init__(self, window):
        self.window = window
        self.window.wm_title("PDF Merge Application")
        self.filepath1 = ""
        self.filepath2 = ""
        self.directory = ""
        self.status = Label(self.window, text="")
        self.outputFileName = "merged_file.pdf"
        self.lblFilePath1 = Label(self.window, text="")
        self.lblFilePath2 = Label(self.window, text="")
        self.lblOutputDir = Label(self.window, text="", width=80)

        self.create_fields(window)


    def create_fields(self, window):

        self.lblFiller1 = Label(self.window, width=5, text="")
        self.lblFiller1.grid(row=0, column=0)

        btnBrowseOutputDir = Button(window, text="Output Location", width=14, command=self.getDirectory)
        btnBrowseOutputDir.grid(row=1, column=1)

        self.lblOutputFile = Label(self.window, text="Output Filename: ", width=14, anchor=E)
        self.lblOutputFile.grid(row=2, column=1, pady=5, sticky=W)
        self.outputFileName = StringVar(window)
        self.entOutput = Entry(window, textvariable=self.outputFileName)
        self.entOutput.grid(row=2, column=2, padx=10, sticky=W)  # sticky=W aligns field to left side of grid cell

        btnBrowseFile1 = Button(window, text="Select File 1", width=14, command=lambda: self.getFile("1"))
        btnBrowseFile1.grid(row=3, column=1, sticky=W)

        btnBrowseFile2 = Button(window, text="Select File 2", width=14, command=lambda: self.getFile("2"))
        btnBrowseFile2.grid(row=4, column=1, sticky=W)

        btnMerge = Button(window, text="Merge Files", width=14, command=self.mergeFiles)
        btnMerge.grid(row=5, column=1, pady=10)

        btnExit = Button(window, text="Exit", width=14, command=self.window.destroy)
        btnExit.grid(row=6, column=1)


    def getFile(self, filenum):
        # file selection
        os.chdir("C:\\")
        path = filedialog.askopenfilename(initialdir="C:", title="Select a PDF file", filetypes=[("pdf",".pdf")])

        if filenum == "1":
            self.filepath1 = path
            self.lblFilePath1.grid_forget()
            self.lblFilePath1 = Label(self.window, text=self.filepath1, width=80, anchor=W)
            self.lblFilePath1.grid(row=3, column=2, padx=10, sticky=W)

        else:
            self.filepath2 = path
            self.lblFilePath2.grid_forget()
            self.lblFilePath2 = Label(self.window, text=self.filepath2, width=80, anchor=W)
            self.lblFilePath2.grid(row=4, column=2, padx=10, sticky=W)

        self.status.grid_forget()


    def getDirectory(self):
        # directory selection for output
        os.chdir("C:\\")
        path = filedialog.askdirectory(initialdir="C:", title="Select a directory to put merged file")
        self.directory = path
        self.lblOutputDir.grid_forget()
        self.lblOutputDir = Label(self.window, text=self.directory, width=80, anchor=W)
        self.lblOutputDir.grid(row=1, column=2, padx=10, sticky=W)
        self.status.grid_forget()


    def mergeFiles(self):
        # merge the files
        # first validate fields
        if not self.directory:
            messagebox.showerror("Directory not specified", "Please specify the directory to save merged file to.")
            self.lblOutputDir.grid_forget()

        elif not self.filepath1:
            messagebox.showerror("File not specified", "Please specify File 1.")
            self.lblFilePath1.grid_forget()

        elif not self.filepath2:
            messagebox.showerror("File not specified", "Please specify File 2.")
            self.lblFilePath2.grid_forget()

        else:
            # set default output filename if nothing was specified
            self.outputFileName = self.entOutput.get()
            if not self.outputFileName:
                messagebox.showinfo("Output File not specified", 'Since the Output Filename was not specified, \nthe merged file will be named "merged_file.pdf".' )
                self.outputFileName = "merged_file.pdf"

            # now do the merge
            try:
                pdf1File = open(self.filepath1, 'rb')
                pdf2File = open(self.filepath2, 'rb')

                reader1 = PyPDF2.PdfFileReader(pdf1File)
                reader2 = PyPDF2.PdfFileReader(pdf2File)

                writer = PyPDF2.PdfFileWriter()
                for pageNum in range(reader1.numPages):
                    page = reader1.getPage(pageNum)
                    writer.addPage(page)

                for pageNum in range(reader2.numPages):
                    page = reader2.getPage(pageNum)
                    writer.addPage(page)

                outputFile = open(self.directory + "\\" + self.outputFileName, 'wb')
                writer.write(outputFile)
                outputFile.close()
                pdf1File.close()
                pdf2File.close()

                self.status = Label(self.window, text="Done!", width=10, anchor=W)
                self.status.grid(row=5, column=2, padx=10, sticky=W)

            except Exception as e:
                messagebox.showerror("Error", str(e))
                outputFile.close()
                pdf1File.close()
                pdf2File.close()


window = Tk()
simple_app = SimpleWindow(window)
window.geometry("800x300+300+300")  #(window width x window height + position right + position down)

window.mainloop()