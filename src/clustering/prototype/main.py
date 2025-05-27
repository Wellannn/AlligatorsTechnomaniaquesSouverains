import argparse
import random
from student import Student
import clustering

first_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hugo", "Ivy", "Jack", "Luna", "Mia", "Noah", "Olivia", "Paul", "Quinn", "Rose", "Sam", "Tina", "Ugo"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Taylor", "Lee"]

def generate_students(n=80, max_preferences=5):
    students = []
    for i in range(n):
        fn = random.choice(first_names)
        ln = random.choice(last_names) + str(i)  # Ajoute un index pour éviter les doublons
        students.append(Student(fn, ln))

    # Ajouter des préférences à chaque étudiant
    for student in students:
        others = [s for s in students if s != student]
        num_prefs = random.randint(1, max_preferences)
        student.preferences = random.sample(others, num_prefs)

    return students

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--group-size", type=int, default=5, help="Taille des groupes")
    parser.add_argument("--students", type=int, default=80, help="Nombre d'étudiants")
    parser.add_argument("--max-prefs", type=int, default=5, help="Max de préférences par étudiant")
    args = parser.parse_args()

    students = generate_students(n=args.students, max_preferences=args.max_prefs)

    print(f"{len(students)} étudiants générés.")
    groups = clustering.cluster_students_greedy_balanced(students, args.group_size)
    affinity_matrix = clustering.build_affinity_matrix(students)

    print("\n=== GROUPES FORMÉS ===")
    total_score = 0

    for i, group in enumerate(groups):
        group_indices = [students.index(s) for s in group]
        score = clustering.score_group(group_indices, affinity_matrix)
        total_score += score
        print(f"Groupe {i+1}: {[str(s) for s in group]} | Score: {score}")

    print(f"\nScore total de répartition : {total_score}")

if __name__ == "__main__":
    main()
