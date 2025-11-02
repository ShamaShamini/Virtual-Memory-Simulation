# Virtual Memory Simulator  
**Interactive GUI Tool for Demand Paging & Page Faults**  

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)  
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)](https://docs.python.org/3/library/tkinter.html)  
[![OS](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()  
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Status](https://img.shields.io/badge/Status-Complete-success)]()

---

## Overview  
A **real-time, visual simulator** of **virtual memory paging** using **demand paging** and **page fault handling**.  
Built with **Python + Tkinter**, it teaches how operating systems:  
- Translate **logical → physical addresses**  
- Manage **page tables**  
- Handle **page faults** with **animated frame loading**  

Perfect for **OS courses**, **labs**, and **self-study**.

---

## Features  
- **Address translation** with page & offset breakdown  
- **Page fault animation** (frame flashes **red → green**)  
- **Live page table** (color-coded: green = loaded, red = not)  
- **Physical memory frames** (Canvas visualization)  
- **Input validation** + error popups  
- **No dependencies** — pure Python standard library  
- **Cross-platform**: Windows, macOS, Linux  

---

## System Model  
| Parameter         | Value                  |
|-------------------|------------------------|
| **Page Size**     | 1024 bytes (1 KB)      |
| **Logical Memory**| 8 pages (0–7)          |
| **Physical Memory**| 4 frames (0–3)         |
| **Address Range** | 0 – 8191               |
| **Replacement**   | None (fills frames 0→3)|

---




## 🚀 How to Run

### 1. Prerequisites

* **Python 3.7+**
* *No external packages are required.*

### 2. Clone or Download

```bash
git clone [https://github.com/ShamaShamini/virtual-memory-simulator.git](https://github.com/ShamaShamini/virtual-memory-simulator.git)
cd virtual-memory-simulator

```
### 3. Run the Simulator

```bash
python virtual_memory_simulator.py

```

## 🛠️ Usage

1.  Enter a **logical address** ($0$ – $8191$) in the input field.
2.  Press **Enter** or click the **"Translate"** button.
3.  **Observe the results:**
    * **Result:** Page, offset, physical address
    * **Page Table:** Updated mapping
    * **Frames:** Visual allocation + animation





## 🚀 Future Enhancements

* **Add Page Replacement:** Implement algorithms (FIFO, LRU, Optimal).
* **Live Statistics:** Integrate fault rate statistics and charts.
* **Multi-Process Simulation:** Model multiple processes with separate page tables.
* **Disk Swap Space:** Visualize the interaction with the simulated disk swap space.
* **Step-by-Step Mode:** Provide a feature for manual, step-by-step execution.
* **Configuration:** Add GUI options for custom page size and memory configurations.
"""
