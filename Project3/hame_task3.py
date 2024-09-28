import numpy as np
import matplotlib.pyplot as plt

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

        Age = int(data[0])  # Припускаємо, що вік у першій колонці
        symptom = data[2]  # Припускаємо, що симптом у третій колонці

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


# Обробка кожного файлу хвороби та зберігання кількості діагнозів
Diagnose_dict = {}
for disease_name in disease_symptoms.keys():
    filename = f"{disease_name}_var2.csv"  # Генеруємо назву файлу
    Diagnose_dict[disease_name] = process_file(filename, disease_name)

# Розрахунок ймовірностей для кожної хвороби
for disease_name, symptoms in disease_symptoms.items():
    Diagnose = Diagnose_dict[disease_name]  # Отримуємо кількість діагнозів для поточної хвороби
    PrKD = symptoms / (Diagnose + 1e-5)  # Уникаємо ділення на нуль
    print(f"Матриця ймовірностей (PrKD) для {disease_name}:")
    print(PrKD)

    # Візуалізація розподілу за віком
    plt.figure(figsize=(10, 6))
    age_groups = ['<20', '20-39', '40-59', '60+']
    age_counts = [symptoms[1, 1], symptoms[1, 2], symptoms[1, 3], symptoms[1, 4]]

    plt.bar(age_groups, age_counts, color='lightblue')
    plt.xlabel('Вікові групи')
    plt.ylabel('Кількість випадків')
    plt.title(f'Розподіл симптомів за віковими групами для {disease_name}')

    # Додаємо підписи в процентах
    for index, value in enumerate(age_counts):
        plt.text(index, value, f"{(value / Diagnose * 100):.1f}%", ha='center', va='bottom')

    plt.show()

    # Візуалізація розподілу за симптомами
    plt.figure(figsize=(10, 6))
    symptom_groups = ['Eye', 'Skin', 'Other']
    symptom_counts = [symptoms[3, 1], symptoms[3, 2], symptoms[3, 3]]

    plt.bar(symptom_groups, symptom_counts, color='orange')
    plt.xlabel('Категорії симптомів')
    plt.ylabel('Кількість випадків')
    plt.title(f'Розподіл симптомів за категоріями для {disease_name}')

    # Додаємо підписи в процентах
    for index, value in enumerate(symptom_counts):
        plt.text(index, value, f"{(value / Diagnose * 100):.1f}%", ha='center', va='bottom')

    plt.show()

# Метод Байеса для діагностики конкретного пацієнта
patient_age = 19
patient_symptom = 'skin'  # Враховуємо симптом

for disease_name in disease_symptoms.keys():
    Diagnose = Diagnose_dict[disease_name]  # Отримуємо кількість діагнозів для поточної хвороби

    # Визначаємо ймовірності для діагностики
    if patient_age < 20:
        age_prob = disease_symptoms[disease_name][1, 1] / (Diagnose + 1e-5)
    elif 20 <= patient_age < 40:
        age_prob = disease_symptoms[disease_name][1, 2] / (Diagnose + 1e-5)
    elif 40 <= patient_age < 60:
        age_prob = disease_symptoms[disease_name][1, 3] / (Diagnose + 1e-5)
    else:
        age_prob = disease_symptoms[disease_name][1, 4] / (Diagnose + 1e-5)

    if patient_symptom == 'eye':
        symptom_prob = disease_symptoms[disease_name][3, 1] / (Diagnose + 1e-5)
    elif patient_symptom == 'skin':
        symptom_prob = disease_symptoms[disease_name][3, 2] / (Diagnose + 1e-5)
    else:
        symptom_prob = disease_symptoms[disease_name][3, 3] / (Diagnose + 1e-5)

    # Ймовірність діагнозу на основі теорії Байеса
    diagnosis_prob = age_prob * symptom_prob
    print(
        f"Ймовірність діагнозу для {disease_name} пацієнта віком {patient_age} з симптомом '{patient_symptom}': {diagnosis_prob:.4f}")

    # Додамо графік для симптомів пацієнта
    plt.figure(figsize=(10, 6))
    patient_symptoms = [age_prob, symptom_prob]
    symptom_labels = ['Ймовірність за віком', 'Ймовірність за симптомом']
    plt.bar(symptom_labels, patient_symptoms, color=['lightgreen', 'lightcoral'])
    plt.ylabel('Ймовірність')
    plt.title(f'Ймовірності симптомів для пацієнта з {disease_name}')
    plt.ylim(0, 1)  # Встановлюємо межі для ймовірності

    # Додаємо підписи в процентах
    for index, value in enumerate(patient_symptoms):
        plt.text(index, value, f"{(value * 100):.1f}%", ha='center', va='bottom')

    plt.show()