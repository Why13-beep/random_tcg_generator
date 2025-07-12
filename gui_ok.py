import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from card_logic import card_parameter, export_to_json, get_next_id


class CardGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TCG Card Generator Pro")
        self.geometry("1000x900")
        self.configure(fg_color="#303030")
        self.current_card = None
        self.build_ui()

    def message_popup(self, title, message):
        from tkinter import messagebox
        #messagebox.showwarning(title, message)
        confirm_popup = ctk.CTkToplevel()
        confirm_popup.title(title)
        confirm_popup.geometry("300x150")
        confirm_popup.grab_set()

        ctk.CTkLabel(confirm_popup, text=message, wraplength=280).pack(pady=20)
        ctk.CTkButton(confirm_popup, text="OK", command=confirm_popup.destroy).pack(pady=10)


    def build_ui(self):
        # sidebar
        sidebar = ctk.CTkFrame(self, fg_color="#2a2a2a", border_width=2, corner_radius=10, border_color="#555555")
        sidebar.pack(side="left", fill="y", expand=False, padx=10, pady=10)

        ctk.CTkLabel(sidebar, text="Card Generator", font=("Arial", 20, "bold"), width=250).pack(pady=20, padx=10)

        self.color_var = ctk.StringVar()
        ctk.CTkLabel(sidebar, text="Card Color:", font=("Arial", 14)).pack()
        self.color_menu = ctk.CTkOptionMenu(sidebar, variable=self.color_var,
                                            values=["Red", "Blue", "Green", "Purple", "Black", "Grey"])
        self.color_menu.pack(pady=5)

        self.color_styles = {
            "Red": "#d34a4a",
            "Blue": "#3a7bd5",
            "Green": "#4caf50",
            "Purple": "#9b59b6",
            "Black": "#2c2c2c",
            "Grey": "#7f8c8d"
        }

        def update_option_menu_color(*args):
            color_name = self.color_var.get()
            color_hex = self.color_styles.get(color_name, "#d34a4a")
            self.color_menu.configure(button_color=color_hex, fg_color=color_hex)

        self.color_var.trace_add("write", update_option_menu_color)

        self.level_var = ctk.StringVar(value="1")
        ctk.CTkLabel(sidebar, text="Card Level:", font=("Arial", 14)).pack()
        for i in range(1, 5):
            ctk.CTkRadioButton(sidebar, text=str(i), variable=self.level_var, value=str(i)).pack(anchor="w", padx=30)

        ctk.CTkButton(sidebar, text="Generate Card", width=120, height=50, command=self.generate_card).pack(pady=20)
        ctk.CTkButton(sidebar, text="Save to JSON", width=120, height=50, command=self.show_save_popup).pack(pady=20)

        # display
        display_frame = ctk.CTkFrame(self)
        display_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.card_fig = plt.Figure(figsize=(6, 4), dpi=100, facecolor="#303030")
        self.card_ax = self.card_fig.add_subplot(111)
        self.card_ax.axis("off")
        self.card_canvas = FigureCanvasTkAgg(self.card_fig, master=display_frame)
        self.card_canvas.get_tk_widget().pack(fill="both", expand=True)

        self.radar_fig = plt.Figure(figsize=(4, 4), dpi=100, facecolor="#2B2B2B")
        self.radar_ax = self.radar_fig.add_subplot(111, polar=True)
        self.radar_ax.set_facecolor("#2a2a2a")

        self.radar_ax.grid(color="gray", linestyle="dotted", linewidth=0.6)
        self.radar_ax.spines["polar"].set_color("#999")
        self.radar_ax.spines["polar"].set_linewidth(1)

        self.radar_ax.tick_params(colors="white", labelsize=10)

        self.radar_canvas = FigureCanvasTkAgg(self.radar_fig, master=display_frame)
        self.radar_canvas.get_tk_widget().pack(fill="both", expand=True)

    def generate_card(self):
        color = self.color_var.get()
        level = self.level_var.get()

        if not color or not level:
            self. message_popup("Error", "Please select both color and level")
            #messagebox.showwarning("Input Error", "Please select both color and level")
            return
        
        result = card_parameter(color, level)    

        if isinstance(result, str):
            self. message_popup("Error", "Please select both color and level")
            #messagebox.showerror("Generation Error", result)
            return
                
        name, parameter = result
        self.current_name = name
        self.current_card = {}
        print(f"{result}")
        for i in parameter:
            self.current_card.update(i)
        print(parameter)
            
        self.update_display()

    def show_save_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Save Card")
        popup.geometry("300x150")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Enter filename:").pack(pady=10)
        filename_entry = ctk.CTkEntry(popup, placeholder_text="my_card")
        filename_entry.pack(pady=5)
        filename_entry.focus()

        def save_file():
            filename = filename_entry.get().strip()

            def custom_info(title, message):
                confirm_popup = ctk.CTkToplevel()
                confirm_popup.title(title)
                confirm_popup.geometry("300x150")
                confirm_popup.grab_set()

                ctk.CTkLabel(confirm_popup, text=message, wraplength=280).pack(pady=20)
                ctk.CTkButton(confirm_popup, text="OK", command=confirm_popup.destroy).pack(pady=10)

            if not filename:
                self. message_popup("Error", "Filename cannot be empty.")
                return

            if not filename.endswith(".json"):
                filename += ".json"

            import os
            from card_logic import export_to_json, get_next_id
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            if not os.path.isabs(filename):
                filename = os.path.join(BASE_DIR, filename)                

            if self.current_card:
                color= self.current_card.get("Color")
                level = self.current_card.get("Level")

                from card_logic import get_next_id
                next_id = get_next_id(color,level, filename)
                self.current_card["ID"] = next_id

                export_to_json(self.current_card, filename)
                popup.after(100,popup.destroy)
                self.message_popup("Success", f"Card saved as:\n{filename}")
                
            else:
                self. message_popup("Warning", "No card generated yet.")

        ctk.CTkButton(popup, text="Save", command=save_file).pack(pady=10)
        popup.bind("<Return>", lambda event: save_file())

    def update_display(self):
        self.card_ax.clear()
        self.card_ax.axis("off")

        color_name = card_parameter(color="Grey",level= 1)
        color_map = {
            "Red": "#d34a4a",
            "Blue": "#4a90d3",
            "Green": "#4ad375",
            "Purple": "#a84ad3",
            "Black": "#000000",
            "Grey": "#aaaaaa"
        }
        theme_color = color_map.get(color_name, "white")

        name = getattr(self,"current_name", "Unknow Monster")
        theme_color = color_map.get(self.current_card.get("Color", "Grey"), "white")
        lines = [f"{key}: {value}" for key, value in self.current_card.items()]
        display_text = "\n".join(lines)

        self.card_ax.text(0.5, 0.85, name, va="center", ha="center", fontsize=20, fontweight="bold", color=theme_color)
        self.card_ax.text(0.5, 0.5, display_text, va="center", ha="center", fontsize=12, color=theme_color,
                          wrap=True, family="monospace")
        self.card_canvas.draw()

        card = self.current_card
        stats = ['HP', 'ATK', 'DEF']
        values = [card['HP'], card['ATK'], card['DEF']]
        max_values = [1800, 1300, 1300]
        normalized = [v / m * 100 for v, m in zip(values, max_values)]

        angles = np.linspace(0, 2 * np.pi, len(stats), endpoint=False)
        normalized += [normalized[0]]
        angles = np.concatenate((angles, [angles[0]]))

        self.radar_ax.clear()
        self.radar_ax.set_facecolor('#2a2a2a')
        self.radar_ax.grid(color='gray', linestyle='dotted', linewidth=0.5)

        self.radar_ax.plot(angles, normalized, linewidth=3, color=card['Color'].lower(), marker='o')
        self.radar_ax.fill(angles, normalized, alpha=0.4, color=card['Color'].lower())

        self.radar_ax.set_xticks(angles[:-1])
        self.radar_ax.set_xticklabels(stats, color='white', fontweight='bold', fontsize=10)
        self.radar_ax.set_yticklabels([])
        self.radar_ax.set_ylim(0, 120)

        for spine in self.radar_ax.spines.values():
            spine.set_color('#888')
            spine.set_linewidth(1)

        self.radar_canvas.draw()


if __name__ == "__main__":
    app = CardGeneratorApp()
    app.mainloop()
