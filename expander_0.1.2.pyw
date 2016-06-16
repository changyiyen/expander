#!/usr/bin/python3

# Expander: a simple graphical acronym expander
# Author: Chang-Yi Yen <changyiyen@gmail.com>
# License: MIT
# Version: 0.1.2

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

		# lower frame: text box, scrollbar, lower right frame
		self.lower_frame = tk.Frame(self.top_frame)
		self.lower_frame.grid(row=1)
		## text box
		self.textbox = tk.Text(self.lower_frame,
			height=15, width=75, undo=True, wrap=tk.WORD
		)
		self.textbox.pack(side=tk.LEFT)
		## scrollbar
		self.text_scrollbar = tk.Scrollbar(self.lower_frame)
		self.text_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
		### link scrollbar to textbox
		self.textbox.config(yscrollcommand=self.text_scrollbar.set)
		self.text_scrollbar.config(command=self.textbox.yview)

		# lower right frame: order selector, scrollbar, button group
		self.lower_right_frame = tk.Frame(self.lower_frame,
			padx=10, pady=10
		)
		self.lower_right_frame.pack(side=tk.RIGHT)
		## order selector
		self.ordering_box = tk.Listbox(self.lower_right_frame)
		self.ordering_box.pack(side=tk.LEFT)
		### initialize the ordering list
		for i in self.table:
			self.ordering_box.insert(tk.END, i)
		## scrollbar
		self.ordering_scrollbar = tk.Scrollbar(self.lower_right_frame)
		self.ordering_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
		### link scrollbar to ordering selector
		self.ordering_box.config(yscrollcommand=self.ordering_scrollbar.set)
		self.ordering_scrollbar.config(command=self.ordering_box.yview)

		# button group: up, down, apply all
		self.lower_frame_buttons = tk.Frame(self.lower_right_frame,
			padx=10, pady=10
		)
		self.lower_frame_buttons.pack(side=tk.LEFT)
		## up button
		self.up_button = tk.Button(self.lower_frame_buttons,
			text="Up", command=self.ordering_up
		)
		self.up_button.pack(side=tk.TOP, fill=tk.X)
		## down button
		self.down_button = tk.Button(self.lower_frame_buttons,
			text="Down", command=self.ordering_down
		)
		self.down_button.pack(side=tk.TOP, fill=tk.X)
		## apply all button
		self.apply_all_button = tk.Button(self.lower_frame_buttons,
			text="Apply all", command=self.apply_all
		)
		self.apply_all_button.pack(side=tk.TOP, fill=tk.X)

		# upper frame: label, context selector, apply, undo, redo, quit
		self.upper_frame = tk.Frame(self.top_frame, padx=10, pady=10)
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
		self.undo_button.grid(row=0, column=4)
		## redo button
		self.redo_button = tk.Button(self.upper_frame,
			text="Redo", command=self.textbox.edit_redo
		)
		self.redo_button.grid(row=0, column=5)
		## quit button
		self.quit_button = tk.Button(self.upper_frame,
			text="Quit", command=self.quit
		)
		self.quit_button.grid(row=0, column=6)

	# Other functions go here
	def apply(self):
		self.original_text = tk.StringVar()
		self.original_text = self.textbox.get(0.0, tk.END)
		# Not sure if this cast is necessary...
		text = str(self.original_text)
		d = self.table[self.context_v.get()]
		for i in d:
			text = re.sub('\\b'+i+'\\b', d[i], text)
		# The Text widget doesn't seem to have a "replace" function,
		# so we're dealing with this by deleting and re-inserting the
		# text.
		self.textbox.delete(0.0, tk.END)
		self.textbox.insert(0.0, text)
		# We're deleting one character here (a newline), because
		# insert() always adds one for some reason
		self.textbox.delete(tk.INSERT)
		return False
	def apply_all(self):
		d = self.table
		for context in self.ordering_box.get(0, tk.END):
			self.original_text = tk.StringVar()
			self.original_text = self.textbox.get(0.0, tk.END)
			text = str(self.original_text)
			for i in d[context]:
				text = re.sub('\\b'+i+'\\b', d[context][i], text)
			self.textbox.delete(0.0, tk.END)
			self.textbox.insert(0.0, text)
			self.textbox.delete(tk.INSERT)
		return False
	def ordering_up(self):
		selected_i = int(self.ordering_box.curselection()[0])
		selected_s = self.ordering_box.get(selected_i)
		if selected_i == 0:
			return False
		self.ordering_box.insert(selected_i-1, selected_s)
		self.ordering_box.delete(selected_i+1)
	def ordering_down(self):
		selected_i = int(self.ordering_box.curselection()[0])
		selected_s = self.ordering_box.get(selected_i)
		if selected_i == tk.END:
			return False
		self.ordering_box.insert(selected_i+2, selected_s)
		self.ordering_box.delete(selected_i)
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
	#conversion_table = {'':{'':''}}
	conversion_table = {}
	for line in conversion_table_csv:
		if line[0] not in conversion_table:
			conversion_table[line[0]] = {}
		conversion_table[line[0]][line[1]] = line[2]
	print(conversion_table)

app = Application(table=conversion_table)
app.master.title('expander 0.1.2')
app.mainloop()
