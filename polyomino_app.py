
from tkinter import *
import math
import polyomino as _mino

SYM_OPTS = ["free", "one-sided", "fixed"]
SYM_COLORS = {'|-\\/%@+XO': "tan",
            '|-%+': "magenta",
            '\\/%X': "yellow",
            '%@': "cyan",
            '|': "red",
            '-': "red",
            '\\': "green",
            '/': "green",
            '%': "blue",
            '?': "gray"}
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

def draw_mino(canvas, mino, x, y, size, fill):
    """Draw the polyomino on the specified canvas objecct."""
    for i, j in mino:
        canvas.create_rectangle([x + size*i, y+size*j,
                                 x+size*(i+1), y+size*(j+1)],
                                fill=fill)

class PolyominoApp(Frame):
    def __init__(self, master):
        
        main = Frame(master)
        main.pack()

        # Size
        textframe = Frame(main)
        textframe.pack()
        Label(textframe, text="Size: ").pack(side=LEFT)

        self.scale_size = Scale(textframe, from_=0, to=11, orient=HORIZONTAL)
        self.scale_size.pack(side=LEFT)
        

        # Make the symmetry-choice buttons
        symframe = Frame(main)
        symframe.pack()
        self.sym_value = IntVar()
        self.sym_value.set(0)

        for index, opt in enumerate(SYM_OPTS):
            button = Radiobutton(symframe,
                                 text=opt,
                                 variable=self.sym_value,
                                 value=index)
            button.pack(anchor=W, side=LEFT)

        # Make the "highlight symmetries" checkbox
        self.symcolor_value = IntVar()
        self.check_symcolor = Checkbutton(main, text="Highlight symmetries",
                                        variable=self.symcolor_value)
        self.check_symcolor.pack()

        # Make the submit button
        self.btn_submit = Button(main, text="Generate", command=self.submit)
        self.btn_submit.pack()

        # Canvas to show the results
        canvasframe = Frame(main)
        canvasframe.pack()

        yscroll = Scrollbar(canvasframe)
        yscroll.pack(side=RIGHT, fill=Y)

        self.canvas = Canvas(canvasframe, bg="white",
                             width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
                             scrollregion=(0,0,CANVAS_WIDTH,CANVAS_HEIGHT*2),
                             yscrollcommand=yscroll.set)
        self.canvas.pack(side=LEFT, fill=BOTH)
        yscroll.config(command=self.canvas.yview)
        
    def submit(self):
        # clear the canvas
        self.canvas.delete(ALL)

##        try:
        n = int(self.scale_size.get())
##        except ValueError:
##            self.canvas.create_text(100, 100,
##                                    text="Must input number", fill="red")
##            return
        sym = self.sym_value.get()
        symcolor = self.symcolor_value.get()
        
        if sym == 0:
            minos = sorted(_mino.free(_mino.generate(n)), key=_mino.mino_key)
        elif sym == 1:
            minos = sorted(_mino.one_sided(_mino.generate(n)), key=_mino.mino_key)
        else:
            minos = sorted(_mino.generate(n), key=_mino.mino_key)

        text = ("There are {0} {1} polyominoes of order {2}".format(
            len(minos), SYM_OPTS[sym], n))
        self.canvas.create_text(CANVAS_WIDTH//2, 25, text=text)

        # Determine sizes
        size = 5
        padding = 2
        margin = 40
        minos_per_line = (CANVAS_WIDTH - margin * 2) // ((n + padding) * size)
        ypos = margin

        scroll_height = 2*margin + (n+padding)*size*(len(minos)//minos_per_line)
        self.canvas.config(scrollregion=(0,0,CANVAS_WIDTH, scroll_height))
        while minos:
            for i in range(minos_per_line):
                if not minos:
                    break
                xpos = margin + ((n + padding) * size) * i
                mino = minos.pop()
                draw_mino(self.canvas, mino,
                          xpos, ypos, size,
                          fill=(SYM_COLORS[mino.symmetry()]
                                if symcolor else "gray"))
            ypos += (n+padding) * size
            

root = Tk()
root.wm_title("Polyomino App")
app = PolyominoApp(root)
root.mainloop()
