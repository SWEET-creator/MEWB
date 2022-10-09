import tkinter as tk
import datetime

word_dict = {}
correct_count = {}
retest_date = {}
dt_now = datetime.datetime.now()


def readFILE():
    with open('word_dict.csv', 'r') as f:
        for line in f:
            data = line.split(', ')
            word_dict[data[0]] = data[1]
            correct_count[data[0]] = int(data[2])
            temp_str = data[3].rstrip()
            retest_date[data[0]] = datetime.datetime.strptime(temp_str, '%Y-%m-%d %H:%M:%S.%f')
    f.close()

def backup():
    output = [k for k in word_dict.keys()]
    with open('word_dict_backup.csv', 'w') as f:
        for key in output:
            f.write(str(key)+", "+str(word_dict[key])+", "+str(correct_count[key])+", "+str(retest_date[key])+"\n")
    f.close()

def writeFILE():
    output = [k for k in word_dict.keys()]
    with open('word_dict.csv', 'w') as f:
        for key in output:
            f.write(str(key)+", "+str(word_dict[key])+", "+str(correct_count[key])+", "+str(retest_date[key])+"\n")
    f.close()
    return

class Application(tk.Frame):
    def __init__(self,master = None):
        super().__init__(master)
        # self.pack()
        HEIGHT = 300
        WIDTH = 420


        master.title("my English word test")
        master.geometry(str(WIDTH)+"x"+str(HEIGHT))
        master.configure(bg='black')

        #-----------------------------#

        self.main_frame = tk.Frame(master, width=WIDTH, height=HEIGHT) 
        self.main_frame.propagate(False)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.configure(bg='turquoise')
        self.titleLabel = tk.Label(self.main_frame, text = "mode select", font=("courier", "40", "bold"), fg ="white", bg = "turquoise")
        self.titleLabel.pack(anchor='center', expand=True)
        self.changePageButton1 = tk.Button(
            self.main_frame, text="word test",
            activeforeground = "turquoise",
            font=("courier", "20", "bold"),
            fg = "firebrick1",
            command=lambda : self.changePage(self.frame1))
        self.changePageButton1.pack(side = "right", pady = "100", padx="50")
        self.changePageButton2 = tk.Button(
            self.main_frame, text="add word",
            activeforeground = "turquoise",
            font=("courier", "20", "bold"),
            fg = "tan1",
            command=lambda : self.changePage(self.frame2))
        self.changePageButton2.pack(side = "left", pady = "100", padx="50")

        #-----------------------------#

        self.frame1 = tk.Frame(width=WIDTH, height=HEIGHT)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame1.configure(bg='black')
        self.entry = tk.Entry(self.frame1,bg="black", fg="white", highlightbackground="lightgreen", highlightcolor = "red", selectbackground = "pink", selectforeground = "black")
        self.entry.bind("<Return>",self.switch)
        self.entry.pack(expand = True)
        self.question_text = tk.StringVar()
        self.question_text.set("Click and Press enter to start")
        self.question = tk.Label(self.frame1, textvariable=self.question_text, font=("courier", "20", "bold"), fg ="white", bg = "black")
        self.question.pack(side = "top", before = self.entry)

        self.answer_text = tk.StringVar()
        self.answer_text.set("")
        self.question = tk.Label(self.frame1, textvariable=self.answer_text, font=("courier", "20", "bold"), fg ="white", bg = "black")
        self.question.pack(side = "bottom", after = self.entry)

        self.index = 0
        self.step = 0

        # making test list
        English = [k for k in word_dict.keys()]
        self.test_list = []
        for word in English:
            if retest_date[word] < dt_now:
                self.test_list.append(word)
 
        #-----------------------------#

        self.frame2 = tk.Frame(width=WIDTH, height=HEIGHT)
        self.frame2.grid(row=0, column=0, sticky="nsew")
        self.frame2.configure(bg='black')
        self.entry_english = tk.Entry(self.frame2,bg="black", fg="white", highlightbackground="lightgreen", highlightcolor = "red", selectbackground = "pink", selectforeground = "black")
        self.entry_english.pack(pady = "25")
        self.entry_japanese = tk.Entry(self.frame2,bg="black", fg="white", highlightbackground="lightgreen", highlightcolor = "red", selectbackground = "pink", selectforeground = "black")
        self.entry_japanese.bind("<Return>",self.confirm_add_word)
        self.entry_japanese.pack(pady = "25")
        self.label1 = tk.Label(self.frame2, text="English", font=("courier", "20", "bold"), fg ="white", bg = "black")
        self.label1.pack(before = self.entry_english, pady = "5")
        self.label2 = tk.Label(self.frame2, text="Japanese", font=("courier", "20", "bold"), fg ="white", bg = "black")
        self.label2.pack(before = self.entry_japanese, pady = "5")

        self.confirm_text = tk.StringVar()
        self.confirm_text.set("")
        self.label3 = tk.Label(self.frame2, textvariable=self.confirm_text, font=("courier", "20", "bold"), fg ="white", bg = "black")
        self.label3.pack(side = "bottom", pady = "5")
        

        #-----------------------------#

        self.main_frame.tkraise()
    
    def switch(self,event):
        if self.index == len(self.test_list):
            # add datetime of test
            with open('datetimelog.csv', 'a') as f:
                f.write(str(dt_now)+"\n")
            f.close()
            self.master.destroy()
            
        else:
            if self.step == 0:
                self.view_question()
                self.step = 1
            else:
                self.judge()
                self.step = 0
                self.index += 1

    # display word of question
    def view_question(self):
        en = self.test_list[self.index]
        self.question_text.set("No."+str(self.index+1)+" /"+str(len(self.test_list))+"\n"+en)
        self.answer_text.set("")
    
    # answer judgment function
    def judge(self):
        def correct(en):
            correct_count[en] += 1
            self.answer_text.set("Your answer is correcdt!!")
        def mistake(en):
            if (correct_count[en] > 0):
                correct_count[en] -= 1
            self.answer_text.set("correct is "+str(word_dict[en]))


        # confirm word
        en = self.test_list[self.index]

        # judge word
        user_ans = self.entry.get()
        if(len(word_dict[en].split("，"))>1):
            if(set(user_ans.split("，")) == set(word_dict[en].split("，"))):
                correct(en)
            else :
                mistake(en)
        else:
            if(user_ans == word_dict[en]):
                correct(en)
            else :
                mistake(en)
        self.entry.delete(0,tk.END)

    
    def confirm_add_word(self, event):
        self.confirm_text.set("Do you add these words?\npress enter")
        self.entry_japanese.bind("<Return>",self.add_word)
    
    def add_word(self, event):
        en = self.entry_english.get()
        jp = self.entry_japanese.get()
        word_dict[en] = str(jp)
        correct_count[en] = 0
        retest_date[en] = dt_now
        self.confirm_text.set("completed!\npress enter if you add more words")
        self.entry_japanese.bind("<Return>",self.add_word_reset)
    
    def add_word_reset(self, event):
        self.entry_english.delete(0,tk.END)
        self.entry_japanese.delete(0,tk.END)
        self.confirm_text.set("")
        self.entry_japanese.bind("<Return>",self.confirm_add_word)
    
    # Screen transition function
    def changePage(self, page):
        page.tkraise()

def GUI():
    win = tk.Tk()
    app = Application(master =  win)
    app.mainloop()

def determine_the_date():
    keys = [k for k in word_dict.keys()]
    for en in keys:
        if correct_count[en] < 2:
            retest_date[en] = dt_now
        else:
            retest_date[en] = dt_now + datetime.timedelta(days=correct_count[en])



def main():
    readFILE()
    backup()
    GUI()
    determine_the_date()
    writeFILE()

main()