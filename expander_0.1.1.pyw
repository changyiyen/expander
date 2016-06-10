#!/usr/bin/python3

# Expander: a simple graphical acronym expander
# Author: Chang-Yi Yen <changyiyen@gmail.com>
# License: MIT
# Version: 0.1.1

import tkinter as tk
import re
import json
import csv

class Application(tk.Frame):
	# The New Mexico Tech docs don't seem to mention what parameters the Frame
	# constructor takes. Might need to look at the source.
	def __init__(self, table=None, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.create_widgets(table)

	def create_widgets(self, table):
		self.top_frame = tk.Frame(padx=10, pady=10)
		self.top_frame.grid()
		
		# initialization of various variables
		self.table = table
		self.original_text = ""

		# lower frame: text box
		self.lower_frame = tk.Frame(self.top_frame)
		self.lower_frame.grid(row=1)
		## text box
		self.textbox = tk.Text(self.lower_frame,
			height=15, width=100, undo=True, wrap=tk.WORD
		)
		self.textbox.grid(row=0, column=0)

		# upper frame: label, context selector, apply, undo, redo, quit
		self.upper_frame = tk.Frame(self.top_frame)
		self.upper_frame.grid(row=0)
		## label
		self.instruction_label = tk.Label(self.upper_frame,
			text="Context: "
		)
		self.instruction_label.grid(row=0, column=0)
		## context selector
		contexts = list(table.keys())
		self.context_v = tk.StringVar()
		self.context_v.set(contexts[0])
		self.context_menu = tk.OptionMenu(self.upper_frame,
			self.context_v, *contexts
		)
		self.context_menu.grid(row=0, column=1)
		## apply button
		self.apply_button = tk.Button(self.upper_frame,
			text="Apply", command=self.apply
		)
		self.apply_button.grid(row=0, column=2)
		## undo button
		self.undo_button = tk.Button(self.upper_frame,
			text="Undo", command=self.textbox.edit_undo
		)
		self.undo_button.grid(row=0, column=3)
		## redo button
		self.redo_button = tk.Button(self.upper_frame,
			text="Redo", command=self.textbox.edit_redo
		)
		self.redo_button.grid(row=0, column=4)
		## quit button
		self.quit_button = tk.Button(self.upper_frame,
			text="Quit", command=self.quit
		)
		self.quit_button.grid(row=0, column=5)

	# Other functions go here
	def apply(self):
		self.original_text = tk.StringVar()
		self.original_text = self.textbox.get(0.0, tk.END)
		# Not sure if this cast is necessary...
		text = str(self.original_text)
		d = self.table[self.context_v.get()]
		for i in d:
			text = re.sub(i, d[i], text)
		# The Text widget doesn't seem to have a "replace" function,
		# so we're dealing with this by deleting and re-inserting the
		# text.
		self.textbox.delete(0.0, tk.END)
		self.textbox.insert(0.0, text)
		# We're deleting one character here (a newline), because
		# insert() always adds one for some reason
		self.textbox.delete(tk.INSERT)
		return False
	def quit(self):
		self.top_frame.winfo_toplevel().destroy()

try:
	conversion_table = json.load(
		open('conversion_table.json', mode='r', encoding='utf8')
	)
except:
	conversion_table_csv = csv.reader(
		open('conversion_table.csv', mode='r', encoding='utf8')
	)
	conversion_table = {'':{'':''}}
	for line in conversion_table_csv:
		#print(line[0], line[1], line[2])
		if line[0] not in conversion_table:
			conversion_table[line[0]] = {}
		conversion_table[line[0]][line[1]] = line[2]
	print(conversion_table)

app = Application(table=conversion_table)
app.master.title('expander 0.1.1')
app.mainloop()
