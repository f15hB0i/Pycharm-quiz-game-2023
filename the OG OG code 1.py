import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
import time


class MotorcycleQuiz:
    def __init__(self, master):
        self.master = master
        self.score = 0
        self.current_question = 0
        self.timer_running = False
        self.question_history = []

        self.questions = [
            {
                "question": "Which motorcycle manufacturer is known for producing the Gold Wing model?",
                "options": ["Yamaha", "Suzuki", "Honda", "Kawasaki"],
                "correct_option": 2
            },
            {
                "question": "What is the engine configuration of a Harley-Davidson Sportster Iron 883?",
                "options": ["Inline-4", "V-Twin", "Parallel-Twin", "Single Cylinder"],
                "correct_option": 1
            },
            {
                "question": "Which country is KTM motorcycles originally from?",
                "options": ["United States", "Germany", "Japan", "Austria"],
                "correct_option": 3
            },
            {
                "question": "What does the term 'cruiser' typically refer to in the context of motorcycles?",
                "options": ["A lightweight motorcycle", "A motorcycle designed for off-road riding",
                            "A motorcycle with a relaxed riding position",
                            "A motorcycle with a high-performance engine"],
                "correct_option": 2
            },
            {
                "question": "Which motorcycle brand is known for its iconic Bonneville model?",
                "options": ["Ducati", "Triumph", "Harley-Davidson", "BMW"],
                "correct_option": 1
            },
            {
                "question": "What is the displacement of a Honda CBR1000RR Fireblade?",
                "options": ["500cc", "750cc", "1000cc", "1200cc"],
                "correct_option": 2
            },
            {
                "question": "Which motorcycle brand has a model called 'Ninja'?",
                "options": ["Kawasaki", "Suzuki", "Yamaha", "Honda"],
                "correct_option": 0
            },
            {
                "question": "What is the maximum speed of a Ducati Panigale V4?",
                "options": ["180 mph", "200 mph", "220 mph", "240 mph"],
                "correct_option": 1
            },
            {
                "question": "Which motorcycle manufacturer is known for its GSX-R series?",
                "options": ["Yamaha", "Suzuki", "Honda", "Kawasaki"],
                "correct_option": 1
            },
            {
                "question": "What does ABS stand for in the context of motorcycles?",
                "options": ["Automatic Braking System", "Anti-Lock Braking System", "Active Braking System",
                            "Advanced Braking System"],
                "correct_option": 1
            },
            {
                "question": "What is the full form of the motorcycle term 'CBR' in Honda CBR motorcycles?",
                "options": ["City Bike Racer", "Cruiser Bike Racer", "Cafe Racer", "Cubic Bore Racer"],
                "correct_option": 3
            },
            {
                "question": "Which motorcycle brand is known for its adventure touring models such as the Multistrada and Panigale V4?",
                "options": ["Triumph", "Kawasaki", "Ducati", "BMW"],
                "correct_option": 2
            },
            {
                "question": "What is the maximum power output of the Kawasaki Ninja H2R?",
                "options": ["200 hp", "300 hp", "400 hp", "500 hp"],
                "correct_option": 1
            },
            {
                "question": "Which motorcycle brand is known for its 'Africa Twin' adventure bike?",
                "options": ["Honda", "Suzuki", "Yamaha", "KTM"],
                "correct_option": 0
            },
            {
                "question": "What is the engine displacement of a Suzuki Hayabusa?",
                "options": ["1000cc", "1300cc", "1500cc", "1800cc"],
                "correct_option": 1
            }
        ]

        self.question_label = tk.Label(self.master, text="", font=("Arial", 12))
        self.question_label.pack()

        self.radio_var = tk.IntVar()
        self.option_buttons = []
        for i in range(4):
            option_button = tk.Radiobutton(self.master, text="", font=("Arial", 10), variable=self.radio_var, value=i)
            option_button.pack()
            self.option_buttons.append(option_button)

        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_answer, font=("Arial", 10))
        self.submit_button.pack()

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.master, variable=self.progress_var)
        self.progress_bar.pack()

        self.timer_label = tk.Label(self.master, text="", font=("Arial", 10))
        self.timer_label.pack()

        self.history_button = tk.Button(self.master, text="View History", command=self.show_question_history, font=("Arial", 10))
        self.history_button.pack()

        self.start_timer()
        self.next_question()

    def start_timer(self):
        self.timer_running = True
        self.timer_thread = Thread(target=self.run_timer)
        self.timer_thread.start()

    def run_timer(self):
        timer_value = 10  # Timer duration per question in seconds

        while self.timer_running and timer_value >= 0:
            self.timer_label.config(text=f"Time Left: {timer_value} seconds")
            self.progress_var.set((10 - timer_value) / 10 * 100)
            time.sleep(1)
            timer_value -= 1

        if timer_value < 0:
            self.submit_answer()

    def stop_timer(self):
        self.timer_running = False
        self.timer_thread.join()

    def next_question(self):
        self.stop_timer()

        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.question_label.config(text=question["question"])

            options = question["options"]
            for i in range(4):
                self.option_buttons[i].config(text=options[i])

            self.radio_var.set(-1)

            self.start_timer()
        else:
            self.stop_timer()
            self.show_score_report()

    def submit_answer(self):
        self.stop_timer()

        if self.radio_var.get() == -1:
            messagebox.showwarning("Warning", "Please select an option.")
        else:
            question = self.questions[self.current_question]
            if self.radio_var.get() == question["correct_option"]:
                self.score += 1

            self.question_history.append({
                "question": question["question"],
                "selected_option": question["options"][self.radio_var.get()],
                "correct_option": question["options"][question["correct_option"]]
            })

            self.current_question += 1
            self.next_question()

    def show_score_report(self):
        report = f"Quiz Complete\nYou scored {self.score} out of {len(self.questions)}"
        messagebox.showinfo("Quiz Report", report)

    def show_question_history(self):
        history_text = "Question History:\n\n"
        for i, entry in enumerate(self.question_history):
            history_text += f"Question {i+1}:\n"
            history_text += f"Question: {entry['question']}\n"
            history_text += f"Your Answer: {entry['selected_option']}\n"
            history_text += f"Correct Answer: {entry['correct_option']}\n\n"

        messagebox.showinfo("Question History", history_text)


root = tk.Tk()
root.title("Motorcycle Quiz")
root.geometry("400x400")
quiz = MotorcycleQuiz(root)
root.mainloop()
