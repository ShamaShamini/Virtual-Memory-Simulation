# Virtual Memory Simulator (Text Mode) – Count All Inputs, No Replacement
PAGE_SIZE = 1024
NUM_PAGES = 8
NUM_FRAMES = 4
MAX_TRANSLATIONS = 10


class VirtualMemorySimulator:
    def __init__(self):
        self.page_table = [-1] * NUM_PAGES
        self.frame_occupied = [False] * NUM_FRAMES
        self.next_frame = 0
        self.translation_count = 0

    def translate(self, logical):
        page = logical // PAGE_SIZE
        offset = logical % PAGE_SIZE

        lines = []
        lines.append(f"Logical Address: {logical}")
        lines.append(f"  Page Number: {page}")
        lines.append(f"  Offset: {offset}")

        # Page already loaded
        if self.page_table[page] != -1:
            frame = self.page_table[page]
            phys = frame * PAGE_SIZE + offset
            lines.append(f"Page {page} already in Frame {frame}")
            lines.append(f"→ Physical Address: {phys}")
        else:
            # Page fault
            lines.append(f"*** PAGE FAULT: Page {page} not in memory ***")

            # Check if free frame available
            if all(self.frame_occupied):
                lines.append("❌ No free frames available! Cannot load page.")
            else:
                # Load page into next free frame
                frame = self.next_frame
                if self.frame_occupied[frame]:
                    for i in range(NUM_FRAMES):
                        if not self.frame_occupied[i]:
                            frame = i
                            break

                self.page_table[page] = frame
                self.frame_occupied[frame] = True
                self.next_frame = frame + 1 if frame + 1 < NUM_FRAMES else NUM_FRAMES

                phys = frame * PAGE_SIZE + offset
                lines.append(f"→ Loading Page {page} → Frame {frame}")
                lines.append(f"→ Physical Address: {phys}")

        return "\n".join(lines)

    def print_page_table(self):
        print("\nPAGE TABLE:")
        print("---------------------------------")
        print("Page | Frame | Status")
        print("---------------------------------")
        for p in range(NUM_PAGES):
            f = self.page_table[p]
            status = "Loaded" if f != -1 else "Not Loaded"
            frame_display = f if f != -1 else "-"
            print(f"{p:4} | {frame_display:5} | {status}")
        print("---------------------------------")

    def run(self):
        max_addr = NUM_PAGES * PAGE_SIZE - 1
        print("=== Virtual Memory Simulator (Text Mode) ===")
        print(f"Page Size: {PAGE_SIZE} bytes")
        print(f"Logical Address Range: 0 – {max_addr}")
        print(f"Maximum Inputs: {MAX_TRANSLATIONS}")
        print("--------------------------------------------\n")

        while self.translation_count < MAX_TRANSLATIONS:
            inp = input(f"[{self.translation_count + 1}/{MAX_TRANSLATIONS}] Enter logical address: ").strip()

            # Increment translation count for every input
            self.translation_count += 1

            # Check if integer
            if not inp.isdigit():
                print("Error: Please enter a valid integer.\n")
                continue  # counted, but no page table

            logical = int(inp)

            # Validate range
            if not (0 <= logical <= max_addr):
                print(f"Error: Invalid address! Enter 0–{max_addr}.\n")
                continue  # counted, but no page table

            # Valid translation
            result = self.translate(logical)
            print(result)
            self.print_page_table()
            print()

        print("\nMaximum number of translations reached! Program ending.")


if __name__ == "__main__":
    sim = VirtualMemorySimulator()
    sim.run()
