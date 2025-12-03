import tkinter as tk
from tkinter import ttk, messagebox

PAGE_SIZE = 1024
NUM_PAGES = 8
NUM_FRAMES = 4
MAX_Translations = 10  # Allow exactly 10 Translations 

class VirtualMemoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Memory Simulator – Paging with Page Faults")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        self.page_table = [-1] * NUM_PAGES
        self.frame_occupied = [False] * NUM_FRAMES
        self.next_frame = 0
        self.attempt_count = 0  # Counter for every click/enter

        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        # Title + Attempt Counter
        header = tk.Frame(self.root, bg="#f0f0f0")
        header.pack(pady=10)

        tk.Label(header, text="Virtual Memory Paging Simulator",
                 font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#2c3e50").pack()

        self.counter_label = tk.Label(header,
                                     text=f"Attempts used: 0 / {MAX_ATTEMPTS}",
                                     font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#e74c3c")
        self.counter_label.pack(pady=5)

        # Input
        inp = tk.Frame(self.root, bg="#f0f0f0")
        inp.pack(pady=10)

        tk.Label(inp, text="Logical Address (0–8191):",
                 font=("Arial", 11), bg="#f0f0f0").pack(side=tk.LEFT)

        self.addr_entry = tk.Entry(inp, width=12, font=("Arial", 11))
        self.addr_entry.pack(side=tk.LEFT, padx=5)
        self.addr_entry.bind("<Return>", lambda e: self.translate())

        self.translate_btn = tk.Button(inp, text="Translate", command=self.translate,
                                      bg="#3498db", fg="white", font=("Arial", 10, "bold"))
        self.translate_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(inp, text="Reset All", command=self.reset_all,
                  bg="#e74c3c", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

        # Result
        self.result_label = tk.Label(self.root, text="", font=("Courier", 11),
                                    bg="#f0f0f0", fg="#2c3e50", justify=tk.LEFT)
        self.result_label.pack(pady=10)

        # Page Table
        ptf = tk.LabelFrame(self.root, text="Page Table", font=("Arial", 12, "bold"), padx=10, pady=10)
        ptf.pack(pady=10, fill=tk.X, padx=20)
        self.pt_tree = ttk.Treeview(ptf, columns=("Page", "Frame", "Status"), show="headings", height=8)
        for col in ("Page", "Frame", "Status"):
            self.pt_tree.heading(col, text=col)
            self.pt_tree.column(col, width=100, anchor="center")
        self.pt_tree.pack()

        # Physical Memory
        pmf = tk.LabelFrame(self.root, text="Physical Memory Frames", font=("Arial", 12, "bold"), padx=10, pady=10)
        pmf.pack(pady=10, fill=tk.X, padx=20)
        self.canvas = tk.Canvas(pmf, height=120, bg="white")
        self.canvas.pack(fill=tk.X, padx=10, pady=5)
        self.frame_labels = []
        w = 180
        for i in range(NUM_FRAMES):
            x0 = 30 + i * (w + 20)
            rect = self.canvas.create_rectangle(x0, 20, x0 + w, 100, fill="#ddd", outline="#999", width=2)
            txt = self.canvas.create_text(x0 + w // 2, 60, text=f"Frame {i}\nFree", font=("Arial", 10))
            self.frame_labels.append((rect, txt))

        # Footer
        tk.Label(self.root,
                 text=f"Page Size: {PAGE_SIZE} bytes | Max Address: {NUM_PAGES * PAGE_SIZE - 1} | Max 10 attempts",
                 font=("Arial", 9), bg="#f0f0f0", fg="#7f8c8d").pack(pady=10)

    def translate(self):
        # Increment attempt counter
        self.attempt_count += 1
        self.counter_label.config(text=f"Attempts used: {self.attempt_count} / {MAX_ATTEMPTS}")

        # Process the input (even on 10th attempt)
        text = self.addr_entry.get().strip()
        if not text:
            self.result_label.config(text="Error: Empty input!", fg="red")
        else:
            try:
                logical = int(text)
                if not (0 <= logical < NUM_PAGES * PAGE_SIZE):
                    raise ValueError
                page = logical // PAGE_SIZE
                offset = logical % PAGE_SIZE
                lines = [f"Logical Address: {logical}",
                         f"├─ Page Number: {page}",
                         f"└─ Offset: {offset}"]

                if self.page_table[page] != -1:
                    frame = self.page_table[page]
                    phys = frame * PAGE_SIZE + offset
                    lines += [f"Page {page} already in Frame {frame}",
                              f"→ Physical Address: {phys}"]
                    self.highlight_frame(frame, "#27ae60")
                else:
                    lines.append(f"*** PAGE FAULT: Page {page} not in memory ***")
                    if all(self.frame_occupied):
                        lines.append("No free frames! Cannot load page.")
                    else:
                        frame = self.next_frame
                        self.page_table[page] = frame
                        self.frame_occupied[frame] = True
                        self.next_frame += 1
                        phys = frame * PAGE_SIZE + offset
                        lines += [f"→ Loading Page {page} → Frame {frame}",
                                  f"→ Physical Address: {phys}"]
                        self.highlight_frame(frame, "#e74c3c")
                        self.root.after(500, lambda: self.highlight_frame(frame, "#27ae60"))

                self.result_label.config(text="\n".join(lines), fg="#2c3e50")
                self.update_display()

            except ValueError:
                self.result_label.config(text="Error: Invalid address!\nMust be 0–8191", fg="red")

        # Clear input
        self.addr_entry.delete(0, tk.END)

        # Disable input after processing 10th attempt
        if self.attempt_count >= MAX_ATTEMPTS:
            self.addr_entry.config(state="disabled")
            self.translate_btn.config(state="disabled")
            self.result_label.config(text=self.result_label.cget("text") + "\n\nMax 10 attempts reached! Click 'Reset All'.")
            messagebox.showinfo("Limit Reached",
                                f"You have used all {MAX_ATTEMPTS} attempts!\nClick 'Reset All' to start over.")

    def highlight_frame(self, frame, colour):
        rect_id, txt_id = self.frame_labels[frame]
        page_in_frame = next((p for p, f in enumerate(self.page_table) if f == frame), None)
        new_text = f"Frame {frame}\nPage {page_in_frame if page_in_frame is not None else '-'}"
        self.canvas.itemconfig(rect_id, fill=colour)
        self.canvas.itemconfig(txt_id, text=new_text)

    def update_display(self):
        self.pt_tree.delete(*self.pt_tree.get_children())
        for p in range(NUM_PAGES):
            f = self.page_table[p]
            status = "Loaded" if f != -1 else "Not Loaded"
            tag = "green" if f != -1 else "red"
            self.pt_tree.insert("", "end", values=(p, f if f != -1 else "-", status), tags=(tag,))
        self.pt_tree.tag_configure("green", foreground="green")
        self.pt_tree.tag_configure("red", foreground="red")

        for i in range(NUM_FRAMES):
            rect_id, txt_id = self.frame_labels[i]
            if self.frame_occupied[i]:
                page = next((p for p, f in enumerate(self.page_table) if f == i), None)
                txt = f"Frame {i}\nPage {page}"
                colour = "#90ee90"
            else:
                txt = f"Frame {i}\nFree"
                colour = "#ddd"
            self.canvas.itemconfig(rect_id, fill=colour)
            self.canvas.itemconfig(txt_id, text=txt)

    def reset_all(self):
        if messagebox.askyesno("Reset", "Clear memory and reset attempt counter?"):
            self.page_table = [-1] * NUM_PAGES
            self.frame_occupied = [False] * NUM_FRAMES
            self.next_frame = 0
            self.attempt_count = 0
            self.counter_label.config(text=f"Attempts used: 0 / {MAX_ATTEMPTS}")
            self.addr_entry.config(state="normal")
            self.translate_btn.config(state="normal")
            self.addr_entry.delete(0, tk.END)
            self.result_label.config(text="")
            self.update_display()

def main():
    root = tk.Tk()
    VirtualMemoryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

