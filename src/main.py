import word_check, winsound, ctypes, pystray

from pynput.keyboard import Listener, Controller
from PIL import Image as img_
from tkinter import Tk, ttk, PhotoImage, Text, W, E, StringVar, Button, Entry, Frame, Label

mismatches_found = [None] * 50

layouts = {
    "0x429": "fa",   # Farsi
    "0x409": "en",   # English - United States
    "0x809": "en",   # English - United Kingdom	
    "0x0c09": "en",  # English - Australia			
    "0x2809": "en",  # English - Belize			
    "0x1009": "en",  # English - Canada			
    "0x2409": "en",  # English - Caribbean			
    "0x3c09": "en",  # English - Hong Kong SAR		
    "0x4009": "en",  # English - India				
    "0x3809": "en",  # English - Indonesia			
    "0x1809": "en",  # English - Ireland			
    "0x2009": "en",  # English - Jamaica			
    "0x4409": "en",  # English - Malaysia			
    "0x1409": "en",  # English - New Zealand		
    "0x3409": "en",  # English - Philippines		
    "0x4809": "en",  # English - Singapore			
    "0x1c09": "en",  # English - South Africa		
    "0x2c09": "en",  # English - Trinidad			
    "0x3009": "en",  # English - Zimbabwe			
}

word_in_memory = {
    "word-en": "",
    "word-fa": ""
}

controller = Controller()

def boop(): 
    for i in range(3): winsound.Beep(3000, 100)

def get_layout():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    klid = user32.GetKeyboardLayout(thread_id)
    lid = klid & (2**16 - 1)
    lid_hex = hex(lid)

    return layouts[lid_hex]

def correct():
    lang = get_layout()
    word_in_memory["word-fa"] = word_check.en_to_fa(word_in_memory["word-en"])
    result = word_check.lookup_word(word_in_memory, lang)

    if result[0]: print(result[1])
    else: 
        boop(); print(f"\033[91m{result[1]}\033[0m")
        mismatches_found.pop(0)
        mismatches_found.append(f"{result[1]}")

    word_in_memory["word-en"] = ""

def on_press(key): 
    key = str(key)
    if key == "Key.backspace" and word_in_memory["word-en"] != "": 
        word_in_memory["word-en"] = word_in_memory["word-en"][:-1]
    elif key in ["Key.shift", "Key.ctrl_l", "Key.ctrl_r"]: pass
    elif key in ["Key.space", "Key.enter", "'?'", "'!'", "'.'"]: correct()
    else: word_in_memory["word-en"] += str(key)[1]

listener_key = Listener(on_press=on_press)
listener_key.start()

is_checking = True
tkinter_running_mismatch = False
window_global_mismatch = None
tkinter_running_dictionary = False
window_global_dictionary = None

def on_clicked_check(icon, item):
    global is_checking
    global listener_key
    is_checking = not item.checked
    if is_checking: listener_key = Listener(on_press=on_press); listener_key.start()
    else: listener_key.stop()

def make_window_mismatch():
    global window_global_mismatch, tkinter_running_mismatch, window_global_dictionary, tkinter_running_dictionary

    if tkinter_running_dictionary: window_global_dictionary.destroy(); tkinter_running_dictionary = False

    root = Tk()
    root.title("Mismatches Found")
    root.iconphoto(False, PhotoImage(file = "icon/keyboard_icon.png"))
    root.geometry('300x200-50+40')

    text = ""
    for mismatch in mismatches_found:
        if mismatch != None: text += f"{mismatch} "

    t = Text(root, width = 40, height = 5, wrap = "word")
    ys = ttk.Scrollbar(root, orient = 'vertical', command = t.yview)
    xs = ttk.Scrollbar(root, orient = 'horizontal', command = t.xview)
    t['yscrollcommand'] = ys.set
    t['xscrollcommand'] = xs.set
    t.insert('end', text)
    t.grid(column = 0, row = 0, sticky = 'nwes')
    xs.grid(column = 0, row = 1, sticky = 'we')
    ys.grid(column = 1, row = 0, sticky = 'ns')

    root.protocol("WM_DELETE_WINDOW", on_quit)
    ttk.Button(root, text="Restart Window", command=on_restart).grid(column=0, columnspan=2, row=1, sticky=(W,E))

    root.grid_columnconfigure(0, weight = 1)
    root.grid_rowconfigure(0, weight = 1)
    
    root.focus_force()

    window_global_mismatch = root; tkinter_running_mismatch = True; root.mainloop()

def make_window_dictionary():

    word_to_be = {
        "action": None,
        "word": "",
        "lang": ""
    }
    
    global window_global_mismatch, tkinter_running_mismatch, window_global_dictionary, tkinter_running_dictionary

    if tkinter_running_mismatch: window_global_mismatch.destroy(); tkinter_running_mismatch = False

    root = Tk()
    root.title("Change dictionary")
    root.iconphoto(False, PhotoImage(file = "icon/keyboard_icon.png"))
    root.geometry('200x180-50+40')
    root.resizable(False, False)

    frame = Frame(master=root, width=150, height=150); frame.pack()

    lang = StringVar()
    
    english = ttk.Radiobutton(root, text='English', variable=lang, value='en')
    farsi = ttk.Radiobutton(root, text='Farsi', variable=lang, value='fa')

    english.place(x=5, y=10); farsi.place(x=5, y=30)
    entry = Entry(root); entry.place(x=5, y=60)

    label = Label(root, text="", wraplength=190); label.place(x=5, y=130)

    def add_word(): 
        cur_word = entry.get(); cur_lang = lang.get()
        if cur_word == "": label.config(text="Nothing to add!")
        if cur_lang == "": label.config(text="No language selected!")

        if cur_lang == "en": 
            try: 
                word_check.eng_arr.index(cur_word)
                label.config(text=f"Word {cur_word} alredy exists!"); return
            except ValueError:
                word_check.eng_arr.append(cur_word)
                with open("dict/english.txt", mode="w", encoding="utf-8") as f: 
                    for word in word_check.eng_arr: f.write(f"{word}\n")
                label.config(text=f"Successfuly added {cur_word} to english dictionary!"); return
        elif cur_lang == "fa": 
            try:
                word_check.far_arr.index(cur_word)
                label.config(text=f"Word {cur_word} alredy exists!"); return
            except ValueError:
                word_check.far_arr.append(cur_word)
                with open("dict/farsi.txt", mode="w", encoding="utf-8") as f: 
                    for word in word_check.far_arr: f.write(f"{word}\n")
                label.config(text=f"Successfuly added {cur_word} to farsi dictionary!"); return

    def remove_word(): 
        cur_word = entry.get(); cur_lang = lang.get()
        if cur_word == "": label.config(text="Nothing to remove!")
        if cur_lang == "": label.config(text="No language selected!")

        if cur_lang == "en": 
            try: word_check.eng_arr.remove(cur_word)
            except ValueError: label.config(text=f"Word {cur_word} doesn't exist!"); return
            with open("dict/english.txt", mode="w", encoding="utf-8") as f: 
                for word in word_check.eng_arr: f.write(f"{word}\n")
            label.config(text=f"Successfuly removed {cur_word} from english dictionary!"); return
        elif cur_lang == "fa": 
            try: word_check.far_arr.remove(cur_word)
            except ValueError: label.config(text=f"Word {cur_word} doesn't exist!"); return
            with open("dict/farsi.txt", mode="w", encoding="utf-8") as f: 
                for word in word_check.far_arr: f.write(f"{word}\n")
            label.config(text=f"Successfuly removed {cur_word} from farsi dictionary!"); return


    button_add = Button(root, text="add", command=add_word)
    button_remove = Button(root, text="remove", command=remove_word)
    button_add.place(x=5, y=90); button_remove.place(x=40, y=90)

    root.protocol("WM_DELETE_WINDOW", on_quit)

    root.grid_columnconfigure(0, weight = 1)
    root.grid_rowconfigure(0, weight = 1)
    
    root.focus_force()

    window_global_dictionary = root; tkinter_running_dictionary = True; root.mainloop()


def on_quit():
    global window_global_mismatch, tkinter_running_mismatch, window_global_dictionary, tkinter_running_dictionary

    if tkinter_running_mismatch: window_global_mismatch.destroy(); tkinter_running_mismatch = False
    if tkinter_running_dictionary: window_global_dictionary.destroy(); tkinter_running_dictionary = False

def on_restart():
    global window_global_mismatch, tkinter_running_mismatch

    if tkinter_running_mismatch: window_global_mismatch.destroy(); tkinter_running_mismatch = False

    make_window_mismatch()

def on_clicked_exit(icon, item): 
    on_quit()
    icon.stop()

def on_clicked_mismatch(icon, item):
    global window_global_mismatch, tkinter_running_mismatch

    if tkinter_running_mismatch: window_global_mismatch.destroy(); tkinter_running_mismatch = False

    make_window_mismatch()

def on_clicked_dictionary(icon, item):
    global window_global_dictionary, tkinter_running_dictionary

    if tkinter_running_dictionary: window_global_dictionary.destroy(); tkinter_running_dictionary = False

    make_window_dictionary()

item_exit = pystray.MenuItem(
                            'Exit',
                            on_clicked_exit)

item_check = pystray.MenuItem(
                            "Is Checking",
                            on_clicked_check,
                            checked=lambda item: is_checking)

item_mismatches = pystray.MenuItem(
                            'Last Mismatches',
                            on_clicked_mismatch)

item_dictionary = pystray.MenuItem(
                            'Change Dictionary',
                            on_clicked_dictionary)

icon = pystray.Icon(
    'Keyboard en-fa',
    title="Keyboard Layout Checker",
    icon=img_.open("icon/keyboard_icon.png"),
    menu=pystray.Menu(item_check, item_mismatches, item_dictionary, item_exit))

icon.run()

