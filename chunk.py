import tkinter as tk
from tkinter import ttk, messagebox
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Korean translations for dependency relations (구성성분)
dep_translations = {
    "nsubj": "주어", "attr": "보어", "cop": "계사",
    "dobj": "목적어", "iobj": "간접목적어", "amod": "형용사수식어", 
    "advmod": "부사어", "det": "한정사", "compound": "복합어", 
    "conj": "접속어", "cc": "접속사", "prep": "전치사", 
    "pobj": "전치사목적어", "aux": "조동사", "ROOT": "핵심어",
    "punct": "구두점"
}

# Korean translations for parts of speech (품사)
pos_translations = {
    "ADJ": "형용사", "ADP": "전치사", "ADV": "부사", "AUX": "조동사",
    "CCONJ": "접속사", "DET": "한정사", "INTJ": "감탄사", "NOUN": "명사",
    "NUM": "수사", "PART": "불변화사", "PRON": "대명사", "PROPN": "고유명사",
    "PUNCT": "구두점", "SCONJ": "종속접속사", "SYM": "기호", "VERB": "동사",
    "X": "기타", "SPACE": "공백"
}

def create_tree_diagram(canvas, doc):
    canvas.delete("all")  # Clear previous drawing
    
    # Calculate positions
    word_width = 140
    word_height = 80
    arrow_height = 40
    total_width = len(doc) * word_width
    start_x = 20
    eng_y = 150
    const_y = eng_y + 20
    pos_y = const_y + 20
    arrow_y = eng_y - arrow_height - 10

    # Draw the main horizontal line
    canvas.create_line(start_x, eng_y, start_x + total_width, eng_y, width=2)

    for i, token in enumerate(doc):
        x = start_x + i * word_width

        # Draw English word
        canvas.create_text(x + word_width/2, eng_y + 15, text=token.text, font=("Arial", 12, "bold"))
        
        # Draw constituent (구성성분) in Korean
        dep_kr = dep_translations.get(token.dep_, token.dep_)
        canvas.create_text(x + word_width/2, const_y + 15, text=f"구성성분: {dep_kr}", font=("Arial", 10), fill="blue")
        
        # Draw POS tag (품사) in Korean
        pos_kr = pos_translations.get(token.pos_, token.pos_)
        canvas.create_text(x + word_width/2, pos_y + 15, text=f"품사: {pos_kr}", font=("Arial", 10), fill="green")

        # Draw arrow and dependency
        if token.dep_ != "ROOT":
            head_index = token.head.i
            head_x = start_x + head_index * word_width + word_width/2
            current_x = x + word_width/2
            
            # Draw arrow
            canvas.create_line(current_x, arrow_y, head_x, arrow_y, 
                               arrow=tk.LAST, smooth=True, width=2)
            
            # Draw dependency label in Korean
            label_x = (current_x + head_x) / 2
            canvas.create_text(label_x, arrow_y - 15, text=dep_kr, 
                               font=("Arial", 9), fill="red")

    # Adjust canvas size and scrollregion
    canvas.config(width=total_width + 40, scrollregion=(0, 0, total_width + 40, pos_y + 50))

def analyze_sentence():
    sentence = entry.get()
    
    if not sentence:
        messagebox.showerror("Error", "Please enter a sentence.")
        return

    doc = nlp(sentence)
    create_tree_diagram(canvas, doc)

# Create main window
root = tk.Tk()
root.title("영어 문장 구조 다이어그램")
root.geometry("800x400")

# Input field
entry_label = tk.Label(root, text="영어 문장을 입력하세요:")
entry_label.pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Analyze button
analyze_button = tk.Button(root, text="다이어그램 생성", command=analyze_sentence)
analyze_button.pack(pady=10)

# Create a frame for the canvas and scrollbar
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Canvas for drawing
canvas = tk.Canvas(frame, bg="white", height=300)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar
h_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

canvas.configure(xscrollcommand=h_scrollbar.set)

# Run main loop
root.mainloop()