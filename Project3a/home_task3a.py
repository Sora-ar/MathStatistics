import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Entry, StringVar, OptionMenu, filedialog, messagebox, Frame, Canvas, Scrollbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Ініціалізація словника для симптомів кожної хвороби
disease_symptoms = {
    'Stones': np.zeros((7, 5)),
    'Hepatitis': np.zeros((7, 5)),
    'Ascariasis': np.zeros((7, 5))
}

# Функція для обробки кожного CSV файлу
def process_file(filename, disease_name):
    with open(filename, "r") as text_file:
        lin = text_file.readlines()

    D1Size = len(lin)
    Diagnose = D1Size - 1
    print(f"Кількість діагнозів для {disease_name}: {Diagnose}")

    for i in range(1, D1Size):
        data = lin[i].strip().split(';')

        try:
            Age = int(data[0])  # Припускаємо, що вік у першій колонці
            symptom = data[2].lower()  # Припускаємо, що симптом у третій колонці
        except (IndexError, ValueError):
            continue  # Пропускаємо рядки з неправильним форматом

        # Обробка вікових категорій
        if Age < 20:
            disease_symptoms[disease_name][1, 1] += 1
        elif 20 <= Age < 40:
            disease_symptoms[disease_name][1, 2] += 1
        elif 40 <= Age < 60:
            disease_symptoms[disease_name][1, 3] += 1
        else:
            disease_symptoms[disease_name][1, 4] += 1

        # Обробка симптомів
        if symptom == 'eye':
            disease_symptoms[disease_name][3, 1] += 1
        elif symptom == 'skin':
            disease_symptoms[disease_name][3, 2] += 1
        else:
            disease_symptoms[disease_name][3, 3] += 1

    return Diagnose  # Повертаємо кількість діагнозів

class DiseaseDiagnosisApp:
    def __init__(self, master):
        self.master = master
        master.title("Діагностика Хвороб за Методом Байєса")

        # Змінні для зберігання шляху до файлів
        self.file_paths = {disease: "" for disease in disease_symptoms.keys()}

        # Кнопки для завантаження файлів
        row = 0
        for disease in disease_symptoms.keys():
            Label(master, text=f"Файл для {disease}:").grid(row=row, column=0, sticky='e')
            Button(master, text="Завантажити", command=lambda d=disease: self.load_file(d)).grid(row=row, column=1, padx=5, pady=5)
            row += 1

        # Поле вводу віку пацієнта
        Label(master, text="Вік пацієнта:").grid(row=row, column=0, sticky='e')
        self.age_entry = Entry(master)
        self.age_entry.grid(row=row, column=1, padx=5, pady=5)
        row += 1

        # Вибір симптому
        Label(master, text="Симптом пацієнта:").grid(row=row, column=0, sticky='e')
        self.symptom_var = StringVar(master)
        self.symptom_var.set("eye")  # Значення за замовчуванням
        symptom_options = ["eye", "skin", "no"]
        OptionMenu(master, self.symptom_var, *symptom_options).grid(row=row, column=1, padx=5, pady=5)
        row += 1

        # Кнопка для запуску діагностики
        Button(master, text="Розрахувати Діагноз", command=self.calculate_diagnosis).grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

    def load_file(self, disease_name):
        filename = filedialog.askopenfilename(title=f"Виберіть файл для {disease_name}",
                                              filetypes=(("CSV файли", "*.csv"), ("Усі файли", "*.*")))
        if filename:
            self.file_paths[disease_name] = filename
            messagebox.showinfo("Успіх", f"Файл для {disease_name} завантажено успішно!")

    def calculate_diagnosis(self):
        # Перевірка, чи всі файли завантажені
        for disease, path in self.file_paths.items():
            if not path or not os.path.exists(path):
                messagebox.showerror("Помилка", f"Файл для {disease} не завантажено або не існує!")
                return

        # Обробка файлів та розрахунок ймовірностей
        Diagnose_dict = {}
        for disease, path in self.file_paths.items():
            Diagnose_dict[disease] = process_file(path, disease)

        # Отримання даних пацієнта
        try:
            patient_age = int(self.age_entry.get())
        except ValueError:
            messagebox.showerror("Помилка", "Будь ласка, введіть коректний вік!")
            return

        patient_symptom = self.symptom_var.get()

        # Розрахунок ймовірностей
        diagnosis_results = {}
        for disease, symptoms in disease_symptoms.items():
            Diagnose = Diagnose_dict[disease]

            # Визначення ймовірностей за віком
            if patient_age < 20:
                age_prob = symptoms[1, 1] / (Diagnose + 1e-5)
            elif 20 <= patient_age < 40:
                age_prob = symptoms[1, 2] / (Diagnose + 1e-5)
            elif 40 <= patient_age < 60:
                age_prob = symptoms[1, 3] / (Diagnose + 1e-5)
            else:
                age_prob = symptoms[1, 4] / (Diagnose + 1e-5)

            # Визначення ймовірностей за симптомом
            if patient_symptom == 'eye':
                symptom_prob = symptoms[3, 1] / (Diagnose + 1e-5)
            elif patient_symptom == 'skin':
                symptom_prob = symptoms[3, 2] / (Diagnose + 1e-5)
            else:
                symptom_prob = symptoms[3, 3] / (Diagnose + 1e-5)

            # Ймовірність діагнозу на основі теорії Байєса
            diagnosis_prob = age_prob * symptom_prob
            diagnosis_results[disease] = diagnosis_prob

            print(f"Ймовірність діагнозу для {disease} пацієнта віком {patient_age} з симптомом '{patient_symptom}': {diagnosis_prob:.4f}")

        # Візуалізація результатів
        self.show_results(diagnosis_results, Diagnose_dict, patient_age, patient_symptom)

    def show_results(self, diagnosis_results, Diagnose_dict, patient_age, patient_symptom):
        # Створення нового вікна для результатів
        result_window = Tk()
        result_window.title("Результати Діагностики")
        result_window.geometry("800x600")  # Встановлюємо початковий розмір вікна

        # Створення Canvas з Scrollbar
        canvas = Canvas(result_window)
        scrollbar = Scrollbar(result_window, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        row = 0
        for disease, prob in diagnosis_results.items():
            Label(scrollable_frame, text=f"Ймовірність діагнозу для {disease}: {prob:.4f}").grid(row=row, column=0, padx=10, pady=5)
            row += 1

        # Візуалізація розподілу за віком та симптомами для кожної хвороби
        for disease, path in self.file_paths.items():
            symptoms = disease_symptoms[disease]
            Diagnose = Diagnose_dict[disease]

            # Вік
            fig_age, ax_age = plt.subplots(figsize=(4, 3))
            age_groups = ['<20', '20-39', '40-59', '60+']
            age_counts = [symptoms[1, 1], symptoms[1, 2], symptoms[1, 3], symptoms[1, 4]]

            ax_age.bar(age_groups, age_counts, color='lightblue')
            ax_age.set_xlabel('Вікові групи')
            ax_age.set_ylabel('Кількість випадків')
            ax_age.set_title(f'Розподіл віку для {disease}')

            for index, value in enumerate(age_counts):
                ax_age.text(index, value, f"{(value / Diagnose * 100):.1f}%", ha='center', va='bottom')

            # Симптоми
            fig_symptom, ax_symptom = plt.subplots(figsize=(4, 3))
            symptom_groups = ['Eye', 'Skin', 'No']
            symptom_counts = [symptoms[3, 1], symptoms[3, 2], symptoms[3, 3]]

            ax_symptom.bar(symptom_groups, symptom_counts, color='orange')
            ax_symptom.set_xlabel('Категорії симптомів')
            ax_symptom.set_ylabel('Кількість випадків')
            ax_symptom.set_title(f'Розподіл симптомів для {disease}')

            for index, value in enumerate(symptom_counts):
                ax_symptom.text(index, value, f"{(value / Diagnose * 100):.1f}%", ha='center', va='bottom')

            # Відображення графіків у прокручуваній області
            frame_age = Frame(scrollable_frame)
            frame_age.grid(row=row, column=0, padx=10, pady=5)
            canvas_age = FigureCanvasTkAgg(fig_age, master=frame_age)
            canvas_age.draw()
            canvas_age.get_tk_widget().pack()

            frame_symptom = Frame(scrollable_frame)
            frame_symptom.grid(row=row, column=1, padx=10, pady=5)
            canvas_symptom = FigureCanvasTkAgg(fig_symptom, master=frame_symptom)
            canvas_symptom.draw()
            canvas_symptom.get_tk_widget().pack()

            row += 1

            plt.close(fig_age)
            plt.close(fig_symptom)

        # Візуалізація ймовірностей діагнозів
        fig_diagnosis, ax_diagnosis = plt.subplots(figsize=(6, 4))
        diseases = list(diagnosis_results.keys())
        probabilities = list(diagnosis_results.values())

        ax_diagnosis.bar(diseases, probabilities, color='green')
        ax_diagnosis.set_xlabel('Хвороби')
        ax_diagnosis.set_ylabel('Ймовірність')
        ax_diagnosis.set_title('Ймовірності Діагнозів')
        ax_diagnosis.set_ylim(0, max(probabilities) * 1.2)

        for index, value in enumerate(probabilities):
            ax_diagnosis.text(index, value, f"{value:.2f}", ha='center', va='bottom')

        frame_diagnosis = Frame(scrollable_frame)
        frame_diagnosis.grid(row=row, column=0, columnspan=2, padx=10, pady=10)
        canvas_diagnosis = FigureCanvasTkAgg(fig_diagnosis, master=frame_diagnosis)
        canvas_diagnosis.draw()
        canvas_diagnosis.get_tk_widget().pack()

        plt.close(fig_diagnosis)

        result_window.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = DiseaseDiagnosisApp(root)
    root.mainloop()
