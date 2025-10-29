import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import json
import os
from pathlib import Path

class CyberpunkNFTGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("metaMAKER")
        self.root.geometry("1400x850")
        self.root.configure(bg='#0a0e27')
        
        self.colors = {
            'bg': '#0a0e27',
            'bg_secondary': '#1a1f3a',
            'accent': '#00ff9f',
            'accent2': '#00d4ff',
            'text': '#e0e0e0',
            'text_dim': '#8892b0',
            'border': '#00ff9f',
            'button': '#162447',
            'button_hover': '#1f4068'
        }
        
        self.image_folder = None
        self.image_files = []
        self.current_index = 0
        self.attributes = []
        self.creators = []
        self.current_image = None
        
        self.create_ui()
        
    def create_ui(self):
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=8, pady=8)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        title_frame.grid(row=0, column=0, columnspan=3, sticky='ew', pady=(0, 8))
        
        title = tk.Label(title_frame,
                        text="⚡ metaMAKER ⚡",
                        font=('Orbitron', 24, 'bold'),
                        fg=self.colors['accent'],
                        bg=self.colors['bg'])
        title.pack()
        
        subtitle = tk.Label(title_frame,
                           text="// SOLANA STANDARD METADATA //",
                           font=('Orbitron', 11),
                           fg=self.colors['text_dim'],
                           bg=self.colors['bg'])
        subtitle.pack()
        
        left_column = tk.Frame(main_frame, bg=self.colors['bg'])
        left_column.grid(row=1, column=0, sticky='nsew', padx=(0, 4))
        
        self.create_folder_section(left_column)
        self.create_basic_info_section(left_column)
        self.create_creators_section(left_column)
        
        middle_column = tk.Frame(main_frame, bg=self.colors['bg'])
        middle_column.grid(row=1, column=1, sticky='nsew', padx=4)
        
        self.create_image_preview_section(middle_column)
        self.create_attributes_section(middle_column)
        
        right_column = tk.Frame(main_frame, bg=self.colors['bg'])
        right_column.grid(row=1, column=2, sticky='nsew', padx=(4, 0))
        
        self.create_control_section(right_column)
        self.create_preview_section(right_column)
        
    def create_cyber_card(self, parent, title, height=None):
        card = tk.Frame(parent, bg=self.colors['bg_secondary'], 
                       highlightbackground=self.colors['border'],
                       highlightthickness=2)
        if height:
            card.pack(fill='x', pady=4, padx=2, ipady=height)
        else:
            card.pack(fill='both', expand=True, pady=4, padx=2)
        
        header = tk.Frame(card, bg=self.colors['bg_secondary'])
        header.pack(fill='x', padx=8, pady=(6, 4))
        
        title_label = tk.Label(header,
                              text=f"// {title} //",
                              font=('Orbitron', 10, 'bold'),
                              fg=self.colors['accent2'],
                              bg=self.colors['bg_secondary'])
        title_label.pack(anchor='w')
        
        content = tk.Frame(card, bg=self.colors['bg_secondary'])
        content.pack(fill='both', expand=True, padx=8, pady=(0, 8))
        
        return content
    
    def create_folder_section(self, parent):
        content = self.create_cyber_card(parent, "IMAGE FOLDER")
        
        self.folder_btn = tk.Button(content,
                                    text="⚡ SELECT",
                                    command=self.select_folder,
                                    font=('Orbitron', 10, 'bold'),
                                    bg=self.colors['button'],
                                    fg=self.colors['accent'],
                                    activebackground=self.colors['button_hover'],
                                    activeforeground=self.colors['accent'],
                                    bd=2,
                                    relief='solid',
                                    padx=15,
                                    pady=8,
                                    cursor='hand2')
        self.folder_btn.pack(fill='x', pady=3)
        
        self.folder_label = tk.Label(content,
                                     text="No folder",
                                     font=('Consolas', 8),
                                     fg=self.colors['text_dim'],
                                     bg=self.colors['bg_secondary'],
                                     wraplength=280,
                                     justify='left')
        self.folder_label.pack(anchor='w', pady=(4, 0))
        
        self.image_count_label = tk.Label(content,
                                          text="Images: 0 | Current: 0",
                                          font=('Orbitron', 9, 'bold'),
                                          fg=self.colors['accent'],
                                          bg=self.colors['bg_secondary'])
        self.image_count_label.pack(anchor='w', pady=(4, 0))
        
    def create_basic_info_section(self, parent):
        content = self.create_cyber_card(parent, "BASIC INFO")
        
        tk.Label(content,
                text="NAME (# = number):",
                font=('Orbitron', 9, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_secondary']).pack(anchor='w', pady=(0, 2))
        
        self.name_entry = tk.Entry(content,
                                   font=('Consolas', 10),
                                   bg=self.colors['button'],
                                   fg=self.colors['text'],
                                   insertbackground=self.colors['accent'],
                                   relief='solid',
                                   bd=2)
        self.name_entry.pack(fill='x', pady=(0, 6), ipady=4)
        self.name_entry.insert(0, "Collection #")
        
        tk.Label(content,
                text="SYMBOL:",
                font=('Orbitron', 9, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_secondary']).pack(anchor='w', pady=(0, 2))
        
        self.symbol_entry = tk.Entry(content,
                                     font=('Consolas', 10),
                                     bg=self.colors['button'],
                                     fg=self.colors['text'],
                                     insertbackground=self.colors['accent'],
                                     relief='solid',
                                     bd=2)
        self.symbol_entry.pack(fill='x', pady=(0, 6), ipady=4)
        
        tk.Label(content,
                text="SELLER FEE BASIS POINTS:",
                font=('Orbitron', 9, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_secondary']).pack(anchor='w', pady=(0, 2))
        
        self.seller_fee_entry = tk.Entry(content,
                                         font=('Consolas', 10),
                                         bg=self.colors['button'],
                                         fg=self.colors['text'],
                                         insertbackground=self.colors['accent'],
                                         relief='solid',
                                         bd=2)
        self.seller_fee_entry.pack(fill='x', pady=(0, 6), ipady=4)
        self.seller_fee_entry.insert(0, "500")
        
        tk.Label(content,
                text="DESCRIPTION:",
                font=('Orbitron', 9, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_secondary']).pack(anchor='w', pady=(0, 2))
        
        self.description_text = tk.Text(content,
                                       height=3,
                                       font=('Consolas', 9),
                                       bg=self.colors['button'],
                                       fg=self.colors['text'],
                                       insertbackground=self.colors['accent'],
                                       relief='solid',
                                       bd=2,
                                       wrap='word')
        self.description_text.pack(fill='x', pady=(0, 3))
        
    def create_creators_section(self, parent):
        content = self.create_cyber_card(parent, "CREATORS")
        
        add_btn = tk.Button(content,
                           text="⊕ ADD CREATOR",
                           command=self.add_creator,
                           font=('Orbitron', 9, 'bold'),
                           bg=self.colors['button'],
                           fg=self.colors['accent'],
                           activebackground=self.colors['button_hover'],
                           activeforeground=self.colors['accent'],
                           bd=2,
                           relief='solid',
                           padx=10,
                           pady=6,
                           cursor='hand2')
        add_btn.pack(fill='x', pady=(0, 6))
        
        self.creators_frame = tk.Frame(content, bg=self.colors['bg_secondary'])
        self.creators_frame.pack(fill='both', expand=True)
        
    def add_creator(self):
        creator_container = tk.Frame(self.creators_frame,
                                     bg=self.colors['button'],
                                     highlightbackground=self.colors['accent2'],
                                     highlightthickness=1)
        creator_container.pack(fill='x', pady=3)
        
        inner_frame = tk.Frame(creator_container, bg=self.colors['button'])
        inner_frame.pack(fill='x', padx=6, pady=6)
        
        tk.Label(inner_frame,
                text="ADDRESS:",
                font=('Orbitron', 8, 'bold'),
                fg=self.colors['accent2'],
                bg=self.colors['button']).grid(row=0, column=0, sticky='w', pady=2)
        
        address_entry = tk.Entry(inner_frame,
                                font=('Consolas', 8),
                                bg=self.colors['bg'],
                                fg=self.colors['text'],
                                insertbackground=self.colors['accent'],
                                relief='solid',
                                bd=1)
        address_entry.grid(row=0, column=1, sticky='ew', padx=(6, 6), pady=2, ipady=2)
        
        tk.Label(inner_frame,
                text="SHARE %:",
                font=('Orbitron', 8, 'bold'),
                fg=self.colors['accent2'],
                bg=self.colors['button']).grid(row=1, column=0, sticky='w', pady=2)
        
        share_entry = tk.Entry(inner_frame,
                              font=('Consolas', 8),
                              bg=self.colors['bg'],
                              fg=self.colors['text'],
                              insertbackground=self.colors['accent'],
                              relief='solid',
                              bd=1,
                              width=10)
        share_entry.grid(row=1, column=1, sticky='w', padx=(6, 6), pady=2, ipady=2)
        share_entry.insert(0, "100")
        
        remove_btn = tk.Button(inner_frame,
                              text="✕",
                              command=lambda: self.remove_creator(creator_container, (address_entry, share_entry)),
                              font=('Orbitron', 9, 'bold'),
                              bg=self.colors['bg'],
                              fg='#ff0055',
                              activebackground='#ff0055',
                              activeforeground='#ffffff',
                              bd=1,
                              relief='solid',
                              width=3,
                              cursor='hand2')
        remove_btn.grid(row=0, column=2, rowspan=2, padx=(4, 0))
        
        inner_frame.columnconfigure(1, weight=1)
        
        self.creators.append((address_entry, share_entry))
        
    def remove_creator(self, container, entries):
        container.destroy()
        self.creators.remove(entries)
        
    def create_image_preview_section(self, parent):
        content = self.create_cyber_card(parent, "IMAGE PREVIEW")
        
        self.image_label = tk.Label(content,
                                    text="No image loaded",
                                    font=('Orbitron', 10),
                                    fg=self.colors['text_dim'],
                                    bg=self.colors['bg'],
                                    width=40,
                                    height=15)
        self.image_label.pack(fill='both', expand=True, padx=4, pady=4)
        
    def create_attributes_section(self, parent):
        content = self.create_cyber_card(parent, "ATTRIBUTES")
        
        add_btn = tk.Button(content,
                           text="⊕ ADD ATTRIBUTE",
                           command=self.add_attribute,
                           font=('Orbitron', 9, 'bold'),
                           bg=self.colors['button'],
                           fg=self.colors['accent'],
                           activebackground=self.colors['button_hover'],
                           activeforeground=self.colors['accent'],
                           bd=2,
                           relief='solid',
                           padx=10,
                           pady=6,
                           cursor='hand2')
        add_btn.pack(fill='x', pady=(0, 6))
        
        attr_canvas = tk.Canvas(content, bg=self.colors['bg_secondary'], 
                               height=150, highlightthickness=0)
        attr_scrollbar = tk.Scrollbar(content, orient="vertical", command=attr_canvas.yview)
        
        self.attributes_frame = tk.Frame(attr_canvas, bg=self.colors['bg_secondary'])
        
        self.attributes_frame.bind(
            "<Configure>",
            lambda e: attr_canvas.configure(scrollregion=attr_canvas.bbox("all"))
        )
        
        attr_canvas.create_window((0, 0), window=self.attributes_frame, anchor="nw")
        attr_canvas.configure(yscrollcommand=attr_scrollbar.set)
        
        attr_canvas.pack(side='left', fill='both', expand=True)
        attr_scrollbar.pack(side='right', fill='y')
        
    def add_attribute(self):
        attr_container = tk.Frame(self.attributes_frame,
                                 bg=self.colors['button'],
                                 highlightbackground=self.colors['accent2'],
                                 highlightthickness=1)
        attr_container.pack(fill='x', pady=3)
        
        inner_frame = tk.Frame(attr_container, bg=self.colors['button'])
        inner_frame.pack(fill='x', padx=6, pady=6)
        
        tk.Label(inner_frame,
                text="TRAIT:",
                font=('Orbitron', 8, 'bold'),
                fg=self.colors['accent2'],
                bg=self.colors['button']).grid(row=0, column=0, sticky='w', pady=2)
        
        trait_entry = tk.Entry(inner_frame,
                              font=('Consolas', 8),
                              bg=self.colors['bg'],
                              fg=self.colors['text'],
                              insertbackground=self.colors['accent'],
                              relief='solid',
                              bd=1)
        trait_entry.grid(row=0, column=1, sticky='ew', padx=(6, 6), pady=2, ipady=2)
        
        tk.Label(inner_frame,
                text="VALUE:",
                font=('Orbitron', 8, 'bold'),
                fg=self.colors['accent2'],
                bg=self.colors['button']).grid(row=1, column=0, sticky='w', pady=2)
        
        value_entry = tk.Entry(inner_frame,
                              font=('Consolas', 8),
                              bg=self.colors['bg'],
                              fg=self.colors['text'],
                              insertbackground=self.colors['accent'],
                              relief='solid',
                              bd=1)
        value_entry.grid(row=1, column=1, sticky='ew', padx=(6, 6), pady=2, ipady=2)
        
        remove_btn = tk.Button(inner_frame,
                              text="✕",
                              command=lambda: self.remove_attribute(attr_container, (trait_entry, value_entry)),
                              font=('Orbitron', 9, 'bold'),
                              bg=self.colors['bg'],
                              fg='#ff0055',
                              activebackground='#ff0055',
                              activeforeground='#ffffff',
                              bd=1,
                              relief='solid',
                              width=3,
                              cursor='hand2')
        remove_btn.grid(row=0, column=2, rowspan=2, padx=(4, 0))
        
        inner_frame.columnconfigure(1, weight=1)
        
        self.attributes.append((trait_entry, value_entry))
        
    def remove_attribute(self, container, entries):
        container.destroy()
        self.attributes.remove(entries)
        
    def create_control_section(self, parent):
        content = self.create_cyber_card(parent, "CONTROLS")
        
        nav_frame = tk.Frame(content, bg=self.colors['bg_secondary'])
        nav_frame.pack(fill='x', pady=(0, 8))
        
        self.prev_btn = tk.Button(nav_frame,
                                  text="◄◄ PREV",
                                  command=self.previous_image,
                                  font=('Orbitron', 10, 'bold'),
                                  bg=self.colors['button'],
                                  fg=self.colors['accent2'],
                                  activebackground=self.colors['button_hover'],
                                  activeforeground=self.colors['accent2'],
                                  bd=2,
                                  relief='solid',
                                  padx=15,
                                  pady=10,
                                  state='disabled',
                                  cursor='hand2')
        self.prev_btn.pack(side='left', fill='x', expand=True, padx=(0, 4))
        
        self.next_btn = tk.Button(nav_frame,
                                 text="NEXT ►►",
                                 command=self.next_image,
                                 font=('Orbitron', 10, 'bold'),
                                 bg=self.colors['button'],
                                 fg=self.colors['accent2'],
                                 activebackground=self.colors['button_hover'],
                                 activeforeground=self.colors['accent2'],
                                 bd=2,
                                 relief='solid',
                                 padx=15,
                                 pady=10,
                                 state='disabled',
                                 cursor='hand2')
        self.next_btn.pack(side='left', fill='x', expand=True, padx=(4, 0))
        
        save_btn = tk.Button(content,
                            text="💾 SAVE CURRENT",
                            command=self.save_current,
                            font=('Orbitron', 10, 'bold'),
                            bg=self.colors['button'],
                            fg=self.colors['accent'],
                            activebackground=self.colors['button_hover'],
                            activeforeground=self.colors['accent'],
                            bd=2,
                            relief='solid',
                            padx=15,
                            pady=10,
                            cursor='hand2')
        save_btn.pack(fill='x', pady=(0, 6))
        
        save_all_btn = tk.Button(content,
                                text="💾 GENERATE ALL",
                                command=self.save_all,
                                font=('Orbitron', 10, 'bold'),
                                bg=self.colors['button'],
                                fg='#00ff00',
                                activebackground=self.colors['button_hover'],
                                activeforeground='#00ff00',
                                bd=2,
                                relief='solid',
                                padx=15,
                                pady=10,
                                cursor='hand2')
        save_all_btn.pack(fill='x', pady=(0, 6))
        
        update_btn = tk.Button(content,
                              text="⟳ UPDATE PREVIEW",
                              command=self.update_preview,
                              font=('Orbitron', 9, 'bold'),
                              bg=self.colors['button'],
                              fg=self.colors['accent2'],
                              activebackground=self.colors['button_hover'],
                              activeforeground=self.colors['accent2'],
                              bd=2,
                              relief='solid',
                              padx=12,
                              pady=8,
                              cursor='hand2')
        update_btn.pack(fill='x')
        
    def create_preview_section(self, parent):
        preview_card = tk.Frame(parent, bg=self.colors['bg_secondary'], 
                               highlightbackground=self.colors['border'],
                               highlightthickness=2)
        preview_card.pack(fill='both', expand=True, pady=(4, 0), padx=2)
        
        header = tk.Frame(preview_card, bg=self.colors['bg_secondary'])
        header.pack(fill='x', padx=8, pady=(6, 4))
        
        tk.Label(header,
                text="// JSON PREVIEW //",
                font=('Orbitron', 10, 'bold'),
                fg=self.colors['accent2'],
                bg=self.colors['bg_secondary']).pack(anchor='w')
        
        content = tk.Frame(preview_card, bg=self.colors['bg_secondary'])
        content.pack(fill='both', expand=True, padx=8, pady=(0, 8))
        
        self.preview_text = scrolledtext.ScrolledText(content,
                                                      font=('Consolas', 9),
                                                      bg=self.colors['button'],
                                                      fg='#00ff00',
                                                      insertbackground=self.colors['accent'],
                                                      relief='solid',
                                                      bd=2,
                                                      wrap='word')
        self.preview_text.pack(fill='both', expand=True)
        
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Image Folder")
        if folder:
            self.image_folder = folder
            self.image_files = sorted([f for f in os.listdir(folder) 
                                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))])
            self.current_index = 0
            
            metadata_folder = os.path.join(self.image_folder, "metadata")
            os.makedirs(metadata_folder, exist_ok=True)
            
            self.folder_label.config(text=f"📁 {folder}")
            self.update_image_counter()
            
            if self.image_files:
                self.prev_btn.config(state='normal')
                self.next_btn.config(state='normal')
                self.load_current_image()
                self.update_preview()
                messagebox.showinfo("Success", f"✓ Loaded {len(self.image_files)} images!\n✓ Metadata folder created")
            else:
                messagebox.showwarning("Warning", "⚠ No images found!")
                
    def load_current_image(self):
        if not self.image_files:
            return
            
        try:
            image_path = os.path.join(self.image_folder, self.image_files[self.current_index])
            img = Image.open(image_path)
            
            max_size = (350, 350)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img)
            self.current_image = photo
            
            self.image_label.config(image=photo, text="")
        except Exception as e:
            self.image_label.config(text=f"Error loading image:\n{str(e)}")
            
    def update_image_counter(self):
        if self.image_files:
            self.image_count_label.config(
                text=f"Total: {len(self.image_files)} | #{self.current_index + 1} | {self.image_files[self.current_index]}"
            )
        else:
            self.image_count_label.config(text="Images: 0 | Current: 0")
            
    def previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_image_counter()
            self.load_current_image()
            self.update_preview()
            
    def next_image(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.update_image_counter()
            self.load_current_image()
            self.update_preview()
            
    def generate_metadata(self, index=None):
        if not self.image_files:
            return None
        
        if index is None:
            index = self.current_index
            
        name = self.name_entry.get()
        symbol = self.symbol_entry.get()
        description = self.description_text.get("1.0", "end-1c")
        
        try:
            seller_fee = int(self.seller_fee_entry.get())
        except ValueError:
            seller_fee = 0
        
        if "#" in name:
            name = name.replace("#", str(index))
        else:
            name = f"{name} #{index}"
            
        metadata = {
            "name": name,
            "symbol": symbol,
            "description": description,
            "seller_fee_basis_points": seller_fee,
            "image": "",
            "attributes": [],
            "properties": {
                "creators": []
            }
        }
        
        for trait_entry, value_entry in self.attributes:
            trait_type = trait_entry.get()
            value = value_entry.get()
            if trait_type and value:
                metadata["attributes"].append({
                    "trait_type": trait_type,
                    "value": value
                })
        
        for address_entry, share_entry in self.creators:
            address = address_entry.get()
            try:
                share = int(share_entry.get())
                if address and share > 0:
                    metadata["properties"]["creators"].append({
                        "address": address,
                        "share": share
                    })
            except ValueError:
                pass
                
        return metadata
        
    def update_preview(self):
        metadata = self.generate_metadata()
        if metadata:
            json_str = json.dumps(metadata, indent=2)
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("1.0", json_str)
            
    def save_current(self):
        if not self.image_files:
            messagebox.showerror("Error", "⚠ No images loaded!")
            return
            
        metadata = self.generate_metadata()
        if metadata:
            metadata_folder = os.path.join(self.image_folder, "metadata")
            os.makedirs(metadata_folder, exist_ok=True)
            
            output_path = os.path.join(metadata_folder, f"{self.current_index}.json")
            
            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
            messagebox.showinfo("Success", f"✓ Saved: {self.current_index}.json")
            
    def save_all(self):
        if not self.image_files:
            messagebox.showerror("Error", "⚠ No images loaded!")
            return
            
        if not messagebox.askyesno("Confirm", f"Generate metadata for all {len(self.image_files)} images?"):
            return
        
        metadata_folder = os.path.join(self.image_folder, "metadata")
        os.makedirs(metadata_folder, exist_ok=True)
            
        saved = 0
        for i in range(len(self.image_files)):
            metadata = self.generate_metadata(index=i)
            if metadata:
                output_path = os.path.join(metadata_folder, f"{i}.json")
                
                with open(output_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                saved += 1
            
        messagebox.showinfo("Complete", f"✓ Generated {saved} metadata files in /metadata folder!")
        self.update_preview()

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberpunkNFTGenerator(root)
    root.mainloop()
