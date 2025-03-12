import tkinter as tk
from tkinter import ttk, scrolledtext

class MultiTypeBalatroCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Type Balatro Calculator")
        self.root.geometry("450x600")
        
        # Create main frame with scrollbar
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Base values frame
        base_frame = ttk.LabelFrame(self.scrollable_frame, text="Base Values", padding=10)
        base_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(base_frame, text="Base Chips:").grid(row=0, column=0, sticky="w", pady=5)
        self.chips_var = tk.StringVar(value="100")
        ttk.Entry(base_frame, textvariable=self.chips_var, width=10).grid(row=0, column=1, pady=5)
        
        ttk.Label(base_frame, text="Base Multiplier:").grid(row=1, column=0, sticky="w", pady=5)
        self.mult_var = tk.StringVar(value="15")
        ttk.Entry(base_frame, textvariable=self.mult_var, width=10).grid(row=1, column=1, pady=5)
        
        # Type management frame
        type_mgmt_frame = ttk.Frame(self.scrollable_frame, padding=10)
        type_mgmt_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(type_mgmt_frame, text="Number of Types:").grid(row=0, column=0, sticky="w", pady=5)
        self.num_types_var = tk.StringVar(value="2")
        ttk.Entry(type_mgmt_frame, textvariable=self.num_types_var, width=10).grid(row=0, column=1, pady=5)
        ttk.Button(type_mgmt_frame, text="Create Type Fields", command=self.create_type_fields).grid(row=0, column=2, pady=5, padx=5)
        
        # Container for type sections
        self.types_container = ttk.Frame(self.scrollable_frame)
        self.types_container.pack(fill="x", padx=10, pady=5)
        
        # Results section
        result_frame = ttk.Frame(self.scrollable_frame, padding=10)
        result_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(result_frame, text="Calculate", command=self.calculate).pack(pady=10)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=10, wrap=tk.WORD)
        self.result_text.pack(fill="both", expand=True)
        
        # Store type entry fields
        self.type_entries = []
        
        # Create default type fields
        self.create_type_fields()
    
    def create_type_fields(self):
        # Clear previous type fields
        for widget in self.types_container.winfo_children():
            widget.destroy()
        
        # Clear stored entries
        self.type_entries = []
        
        # Get number of types
        try:
            num_types = int(self.num_types_var.get())
            
            # Create sections for each type
            for i in range(num_types):
                type_frame = ttk.LabelFrame(self.types_container, text=f"Type {i+1}", padding=10)
                type_frame.pack(fill="x", pady=5)
                
                # Type value
                ttk.Label(type_frame, text="Type Value:").grid(row=0, column=0, sticky="w", pady=2)
                type_var = tk.StringVar(value="1.5")
                ttk.Entry(type_frame, textvariable=type_var, width=10).grid(row=0, column=1, pady=2)
                
                # Triggers
                ttk.Label(type_frame, text="Triggers:").grid(row=1, column=0, sticky="w", pady=2)
                trigs_var = tk.StringVar(value="3")
                ttk.Entry(type_frame, textvariable=trigs_var, width=10).grid(row=1, column=1, pady=2)
                
                # Modifiers
                ttk.Label(type_frame, text="Modifiers:").grid(row=2, column=0, sticky="w", pady=2)
                mods_var = tk.StringVar(value="2")
                ttk.Entry(type_frame, textvariable=mods_var, width=10).grid(row=2, column=1, pady=2)
                
                # Cards
                ttk.Label(type_frame, text="Cards:").grid(row=3, column=0, sticky="w", pady=2)
                cards_var = tk.StringVar(value="5")
                ttk.Entry(type_frame, textvariable=cards_var, width=10).grid(row=3, column=1, pady=2)
                
                # Store the entry variables for this type
                self.type_entries.append({
                    'type_var': type_var,
                    'trigs_var': trigs_var,
                    'mods_var': mods_var,
                    'cards_var': cards_var
                })
        except ValueError:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please enter a valid number for types")
    
    def format_number(self, number):
        """Format number to use scientific notation if > 99,999,999,999"""
        if number > 99999999999:
            return f"{number:.4e}"
        else:
            return f"{number:.2f}"
    
    def calculate(self):
        try:
            # Clear result text
            self.result_text.delete(1.0, tk.END)
            
            # Get base values
            chips = float(self.chips_var.get())
            mult = float(self.mult_var.get())
            
            # Calculate result for each type
            type_results = []
            calculation_steps = []
            
            for i, type_entry in enumerate(self.type_entries):
                # Get values for this type
                type_val = float(type_entry['type_var'].get())
                trigs = float(type_entry['trigs_var'].get())
                mods = float(type_entry['mods_var'].get())
                cards = float(type_entry['cards_var'].get())
                
                # Calculate for this type: ((type)^(trigs*mods))^(cards)
                inner_power = trigs * mods
                inner_result = type_val ** inner_power
                type_result = inner_result ** cards
                
                type_results.append(type_result)
                
                # Record calculation steps
                step = (
                    f"Type {i+1} calculation:\n"
                    f"  Step 1: {type_val}^({trigs}*{mods}) = {type_val}^{inner_power} = {self.format_number(inner_result)}\n"
                    f"  Step 2: {self.format_number(inner_result)}^{cards} = {self.format_number(type_result)}\n"
                )
                calculation_steps.append(step)
            
            # Multiply all type results together
            combined_type_result = 1
            for result in type_results:
                combined_type_result *= result
            
            # Calculate final result
            final_result = combined_type_result * mult * chips
            
            # Format the formula
            formula = ""
            for i in range(len(self.type_entries)):
                if i > 0:
                    formula += "*"
                formula += f"(((type{i+1})^(trigs{i+1}*mods{i+1}))^(cards{i+1}))"
            formula += "*(mult)*(chips)"
            
            # Display formula and results
            self.result_text.insert(tk.END, f"Formula: {formula}\n\n")
            
            # Add each type calculation
            for step in calculation_steps:
                self.result_text.insert(tk.END, step + "\n")
            
            # Add final steps
            self.result_text.insert(tk.END, f"Combined type result: {self.format_number(combined_type_result)}\n\n")
            self.result_text.insert(tk.END, f"Final calculation: {self.format_number(combined_type_result)} * {mult} * {chips} = {self.format_number(final_result)}\n\n")
            self.result_text.insert(tk.END, f"Final chips: {self.format_number(final_result)}")
            
        except ValueError:
            self.result_text.insert(tk.END, "Please enter valid numbers in all fields")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error in calculation: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiTypeBalatroCalculator(root)
    root.mainloop()