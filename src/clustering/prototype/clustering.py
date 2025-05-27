import numpy as np
from student import Student

def build_affinity_matrix(students: list[Student]) -> np.ndarray:
    """
    """
    size = len(students)
    matrix = np.zeros((size, size), dtype=int)

    for i, student in enumerate(students):
        max_points = len(student.preferences)
        for rank, preferred in enumerate(student.preferences):
            if preferred in students:
                j = students.index(preferred)
                weight = max_points - rank  # Ex: 3 préférences → 3, 2, 1
                matrix[i][j] = weight

    return matrix



def generate_combinations(items: list, r: int) -> list[list]:
    """
    """
    def helper(start, current):
        if len(current) == r:
            combinations.append(current[:])
            return
        for i in range(start, len(items)):
            current.append(items[i])
            helper(i + 1, current)
            current.pop()

    combinations = []
    helper(0, [])
    return combinations

def score_group(group_indices: list[int], affinity_matrix: np.ndarray) -> int:
    """
    """
    score = 0
    for i in group_indices:
        for j in group_indices:
            if i != j:
                score += affinity_matrix[i][j]
    return score

def cluster_students(students: list[Student], group_size: int) -> list[list[Student]]:
    """
    """
    affinity_matrix = build_affinity_matrix(students)
    student_indices = list(range(len(students)))
    group_sizes = compute_group_distribution(len(students), group_size)
    ungrouped = student_indices[:]
    groups = []

    for size in group_sizes:
        best_group = []
        best_score = -1
        possible_groups = generate_combinations(ungrouped, size)

        for group in possible_groups:
            score = score_group(group, affinity_matrix)
            if score > best_score:
                best_score = score
                best_group = group

        groups.append([students[i] for i in best_group])
        for i in best_group:
            ungrouped.remove(i)

    return groups



def compute_group_distribution(total_students: int, group_size: int) -> list[int]:
    """
    """
    for r in range(group_size):
        g = (total_students - r * (group_size - 1)) // group_size
        if g * group_size + r * (group_size - 1) == total_students:
            return [group_size] * g + [group_size - 1] * r
    raise ValueError("Unable to distribute students without creating a group of size 1.")
