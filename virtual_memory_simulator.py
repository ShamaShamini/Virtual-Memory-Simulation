import tkinter as tk
from tkinter import ttk, messagebox

# -------------------------------------------------
PAGE_SIZE = 1024
NUM_PAGES = 8
NUM_FRAMES = 4
# -------------------------------------------------


class VirtualMemoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Memory Simulator – Paging with Page Faults")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        # ---------- data ----------
        self.page_table = [-1] * NUM_PAGES          # page → frame
        self.frame_occupied = [False] * NUM_FRAMES
        self.next_frame = 0

        # ---------- UI ----------
        self.setup_ui()
        self.update_display()

    # ------------------------------------------------------------------
    def setup_ui(self):
        # Title
        tk.Label(
            self.root,
            text="Virtual Memory Paging Simulator",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
        ).pack(pady=10)

        # ---- Input ----------------------------------------------------
        inp = tk.Frame(self.root, bg="#f0f0f0")
        inp.pack(pady=10)

        tk.Label(inp, text="Logical Address (0–8191):",
                 font=("Arial", 11), bg="#f0f0f0").pack(side=tk.LEFT)

        self.addr_entry = tk.Entry(inp, width=12, font=("Arial", 11))
        self.addr_entry.pack(side=tk.LEFT, padx=5)
        self.addr_entry.bind("<Return>", lambda e: self.translate())

        tk.Button(
            inp,
            text="Translate",
            command=self.translate,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        # ---- Result ---------------------------------------------------
        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Courier", 11),
            bg="#f0f0f0",
            fg="#2c3e50",
            justify=tk.LEFT,
        )
        self.result_label.pack(pady=10)

        # ---- Page Table -----------------------------------------------
        ptf = tk.LabelFrame(
            self.root,
            text="Page Table",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
        )
        ptf.pack(pady=10, fill=tk.X, padx=20)

        self.pt_tree = ttk.Treeview(
            ptf,
            columns=("Page", "Frame", "Status"),
            show="headings",
            height=8,
        )
        for col in ("Page", "Frame", "Status"):
            self.pt_tree.heading(col, text=col)
        self.pt_tree.column("Page", width=80, anchor="center")
        self.pt_tree.column("Frame", width=80, anchor="center")
        self.pt_tree.column("Status", width=120, anchor="center")
        self.pt_tree.pack()

        # ---- Physical Memory -----------------------------------------
        pmf = tk.LabelFrame(
            self.root,
            text="Physical Memory Frames",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
        )
        pmf.pack(pady=10, fill=tk.X, padx=20)

        self.canvas = tk.Canvas(pmf, height=120, bg="white")
        self.canvas.pack(fill=tk.X, padx=10, pady=5)

        self.frame_labels = []          # list of (rect_id, text_id)
        w = 180
        for i in range(NUM_FRAMES):
            x0 = 30 + i * (w + 20)
            rect = self.canvas.create_rectangle(
                x0, 20, x0 + w, 100, fill="#ddd", outline="#999", width=2
            )
            txt = self.canvas.create_text(
                x0 + w // 2, 60,
                text=f"Frame {i}\nFree",
                font=("Arial", 10),
                justify="center",
            )
            self.frame_labels.append((rect, txt))

        # ---- Footer ---------------------------------------------------
        tk.Label(
            self.root,
            text=f"Page Size: {PAGE_SIZE} bytes | Max Address: {NUM_PAGES * PAGE_SIZE - 1}",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#7f8c8d",
        ).pack(pady=10)

    # ------------------------------------------------------------------
    def translate(self):
        # ---- parse input ------------------------------------------------
        try:
            logical = int(self.addr_entry.get().strip())
            if not (0 <= logical < NUM_PAGES * PAGE_SIZE):
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid",
                f"Address must be an integer between 0 and {NUM_PAGES * PAGE_SIZE - 1}",
            )
            return

        page = logical // PAGE_SIZE
        offset = logical % PAGE_SIZE

        lines = [
            f"Logical Address: {logical}",
            f"├─ Page Number: {page}",
            f"└─ Offset: {offset}",
        ]

        # ---- page hit ---------------------------------------------------
        if self.page_table[page] != -1:
            frame = self.page_table[page]
            phys = frame * PAGE_SIZE + offset
            lines += [
                f"Page {page} already in Frame {frame}",
                f"→ Physical Address: {phys}",
            ]
            self.highlight_frame(frame, "#27ae60")          # green
        else:
            # ---- page fault --------------------------------------------
            lines.append(f"*** PAGE FAULT: Page {page} not in memory ***")
            if self.next_frame >= NUM_FRAMES:
                lines.append("No free frames! Cannot load page.")
                self.result_label.config(text="\n".join(lines), fg="red")
                self.update_display()
                return

            frame = self.next_frame
            self.page_table[page] = frame
            self.frame_occupied[frame] = True
            self.next_frame += 1

            phys = frame * PAGE_SIZE + offset
            lines += [
                f"→ Loading Page {page} → Frame {frame}",
                f"→ Physical Address: {phys}",
            ]

            # flash red → green
            self.highlight_frame(frame, "#e74c3c")
            self.root.after(500, lambda: self.highlight_frame(frame, "#27ae60"))

        self.result_label.config(text="\n".join(lines), fg="#2c3e50")
        self.update_display()
        self.addr_entry.delete(0, tk.END)

    # ------------------------------------------------------------------
    def highlight_frame(self, frame, colour):
        """Colour a frame rectangle and update its text."""
        rect_id, txt_id = self.frame_labels[frame]
        # find which page lives in this frame
        page_in_frame = next(
            (p for p, f in enumerate(self.page_table) if f == frame), None
        )
        new_text = f"Frame {frame}\nPage {page_in_frame}"
        self.canvas.itemconfig(rect_id, fill=colour)
        self.canvas.itemconfig(txt_id, text=new_text)

    # ------------------------------------------------------------------
    def update_display(self):
        # ---- Page Table ------------------------------------------------
        self.pt_tree.delete(*self.pt_tree.get_children())
        for p in range(NUM_PAGES):
            f = self.page_table[p]
            status = "Loaded" if f != -1 else "Not Loaded"
            tag = "green" if f != -1 else "red"
            self.pt_tree.insert(
                "", "end", values=(p, f if f != -1 else "-", status), tags=(tag,)
            )
        self.pt_tree.tag_configure("green", foreground="green")
        self.pt_tree.tag_configure("red", foreground="red")

        # ---- Physical Frames -------------------------------------------
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


# ----------------------------------------------------------------------
def main():
    root = tk.Tk()
    VirtualMemoryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()