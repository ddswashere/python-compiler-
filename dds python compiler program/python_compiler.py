#!/usr/bin/env python3
"""
Python Script Compiler by dds
A modern Windows GUI application for compiling Python scripts to bytecode (.pyc files)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import py_compile
import os
import sys
import traceback
from pathlib import Path
import threading
import time

class PythonCompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Script Compiler by dds")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure style
        self.setup_styles()
        
        # Variables
        self.selected_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.compilation_status = tk.StringVar(value="Ready to compile")
        
        # Create UI
        self.create_widgets()
        
        # Set default output directory
        self.output_dir.set(str(Path.cwd() / "compiled"))
        
    def setup_styles(self):
        """Configure modern styling for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        style.configure('Status.TLabel', font=('Segoe UI', 10))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        
    def create_widgets(self):
        """Create and arrange all UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Python Script Compiler by dds", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Input File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Python File:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        ttk.Entry(file_frame, textvariable=self.selected_file, state='readonly').grid(row=0, column=1, sticky="ew", padx=(0, 10))
        ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(row=0, column=2)
        
        # Output directory section
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output Dir:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        ttk.Entry(output_frame, textvariable=self.output_dir).grid(row=0, column=1, sticky="ew", padx=(0, 10))
        ttk.Button(output_frame, text="Browse", command=self.browse_output_dir).grid(row=0, column=2)
        
        # Compile button
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        self.compile_btn = ttk.Button(button_frame, text="Compile Python Script", 
                                     command=self.compile_script, style='Accent.TButton')
        self.compile_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(button_frame, textvariable=self.compilation_status, style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
        # Output area
        output_frame = ttk.LabelFrame(main_frame, text="Compilation Output", padding="10")
        output_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, font=('Consolas', 9))
        self.output_text.grid(row=0, column=0, sticky="nsew")
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
    def browse_file(self):
        """Open file dialog to select Python file"""
        filename = filedialog.askopenfilename(
            title="Select Python File",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if filename:
            self.selected_file.set(filename)
            self.log_output(f"Selected file: {filename}")
            
    def browse_output_dir(self):
        """Open directory dialog to select output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
            self.log_output(f"Output directory: {directory}")
            
    def log_output(self, message):
        """Add message to output text area"""
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
        
    def compile_script(self):
        """Compile the selected Python script"""
        if not self.selected_file.get():
            messagebox.showerror("Error", "Please select a Python file first!")
            return
            
        if not self.output_dir.get():
            messagebox.showerror("Error", "Please select an output directory!")
            return
            
        # Start compilation in a separate thread
        self.compile_btn.config(state='disabled')
        self.progress.start()
        self.compilation_status.set("Compiling...")
        
        thread = threading.Thread(target=self._compile_worker)
        thread.daemon = True
        thread.start()
        
    def _compile_worker(self):
        """Worker thread for compilation"""
        try:
            input_file = self.selected_file.get()
            output_dir = self.output_dir.get()
            
            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            self.log_output(f"Starting compilation of: {input_file}")
            self.log_output(f"Output directory: {output_dir}")
            self.log_output("-" * 50)
            
            # Get the filename without extension
            file_name = Path(input_file).stem
            output_file = Path(output_dir) / f"{file_name}.pyc"
            
            # Compile the file
            py_compile.compile(input_file, str(output_file), doraise=True)
            
            # Success
            self.log_output(f"✓ Compilation successful!")
            self.log_output(f"✓ Output file: {output_file}")
            self.log_output(f"✓ File size: {output_file.stat().st_size} bytes")
            
            # Update status
            self.root.after(0, lambda: self.compilation_status.set("Compilation successful!"))
            self.root.after(0, lambda: self.status_label.config(style='Success.TLabel'))
            
        except py_compile.PyCompileError as e:
            error_msg = f"Compilation error: {str(e)}"
            self.log_output(f"✗ {error_msg}")
            self.root.after(0, lambda: self.compilation_status.set("Compilation failed!"))
            self.root.after(0, lambda: self.status_label.config(style='Error.TLabel'))
            self.root.after(0, lambda: messagebox.showerror("Compilation Error", error_msg))
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.log_output(f"✗ {error_msg}")
            self.log_output(f"Traceback: {traceback.format_exc()}")
            self.root.after(0, lambda: self.compilation_status.set("Compilation failed!"))
            self.root.after(0, lambda: self.status_label.config(style='Error.TLabel'))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            
        finally:
            # Re-enable UI
            self.root.after(0, lambda: self.compile_btn.config(state='normal'))
            self.root.after(0, lambda: self.progress.stop())
            self.log_output("-" * 50)

def main():
    root = tk.Tk()
    app = PythonCompilerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 