import customtkinter as ctk
import sys

import subprocess
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AI60SecondsStudio(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI60Seconds Studio")
        self.geometry("700x500")

        self.heading = ctk.CTkLabel(
            self,
            text="AI60Seconds Studio",
            font=("Arial", 32, "bold")
        )
        self.heading.pack(pady=30)

        self.status = ctk.CTkLabel(
            self,
            text="Status: Ready",
            font=("Arial", 18)
        )
        self.status.pack(pady=10)

        self.generate_one_btn = ctk.CTkButton(
            self,
            text="Generate 1 Short",
            font=("Arial", 18),
            height=50,
            command=lambda: self.run_bot(1)
        )
        self.generate_one_btn.pack(pady=15, padx=80, fill="x")

        self.generate_ten_btn = ctk.CTkButton(
            self,
            text="Generate 10 Shorts",
            font=("Arial", 18),
            height=50,
            command=lambda: self.run_bot(10)
        )
        self.generate_ten_btn.pack(pady=15, padx=80, fill="x")

        self.output_box = ctk.CTkTextbox(
            self,
            width=620,
            height=220,
            font=("Consolas", 13)
        )
        self.output_box.pack(pady=20)

    def run_bot(self, count):
        thread = threading.Thread(target=self._run_bot_thread, args=(count,))
        thread.start()

    def _run_bot_thread(self, count):
        self.status.configure(text=f"Status: Generating {count} Short(s)...")
        self.output_box.insert("end", f"\nRunning bot.py --count {count}\n")

        try:
            process = subprocess.Popen(
    [sys.executable, "bot.py", "--count", str(count)],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

            for line in process.stdout:
                self.output_box.insert("end", line)
                self.output_box.see("end")

            process.wait()

            self.status.configure(text="Status: Complete")
            self.output_box.insert("end", "\nDone!\n")

        except Exception as e:
            self.status.configure(text="Status: Error")
            self.output_box.insert("end", f"\nERROR: {e}\n")


if __name__ == "__main__":
    app = AI60SecondsStudio()
    app.mainloop()