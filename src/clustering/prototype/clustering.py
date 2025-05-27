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
                weight = max_points - rank
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

def compute_balanced_group_sizes(total: int, group_size: int) -> list[int]:
    """
    """
    for r in range(group_size):
        g = (total - r * (group_size - 1)) // group_size
        if g * group_size + r * (group_size - 1) == total:
            return [group_size] * g + [group_size - 1] * r
    raise ValueError("Impossible to distribute students fairly without 1-sized group.")

def cluster_students_greedy_balanced(students: list[Student], group_size: int) -> list[list[Student]]:
    """
    """
    affinity_matrix = build_affinity_matrix(students)
    total_students = len(students)
    group_sizes = compute_balanced_group_sizes(total_students, group_size)

    student_indices = list(range(total_students))
    ungrouped = set(student_indices)
    groups = []

    for size in group_sizes:
        best_index = max(
            ungrouped,
            key=lambda i: sum(affinity_matrix[i][j] + affinity_matrix[j][i] for j in ungrouped if j != i)
        )

        scores = [(j, affinity_matrix[best_index][j] + affinity_matrix[j][best_index])
                  for j in ungrouped if j != best_index]
        scores.sort(key=lambda x: x[1], reverse=True)

        group = [best_index] + [j for j, _ in scores[:size - 1]]
        groups.append([students[i] for i in group])
        ungrouped -= set(group)

    return groups