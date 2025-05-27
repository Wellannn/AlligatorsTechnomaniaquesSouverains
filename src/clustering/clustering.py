import numpy as np
from src.domain.user import User


class Clustering:
    """
    Clustering class to handle user clustering based on preferences.
    This class provides methods to build an affinity matrix, score groups, and cluster users into balanced groups.
    """
    
    @staticmethod
    def __build_affinity_matrix(preferences: dict[User, list[User]]) -> tuple[np.ndarray, list[User]]:
        """
        Builds an affinity matrix based on user preferences.
        Args:
            preferences (dict[User, list[User]]): Dictionary mapping each User to their preference list.
        Returns:
            tuple: (affinity matrix, list of users in index order)
        """
        users = list(preferences.keys())
        size = len(users)
        matrix = np.zeros((size, size), dtype=int)

        for i, user in enumerate(users):
            prefs = preferences.get(user, [])
            max_points = len(prefs)
            for rank, preferred in enumerate(prefs):
                if preferred in users:
                    j = users.index(preferred)
                    weight = max_points - rank
                    matrix[i][j] = weight

        return matrix, users

    @staticmethod
    def __score_group(group_indices: list[int], matrix: np.ndarray) -> int:
        score = 0
        used_pairs = set()
        for i in group_indices:
            for j in group_indices:
                if i != j and (j, i) not in used_pairs:
                    score += matrix[i][j] + matrix[j][i]
                    used_pairs.add((i, j))
        return int(score)

    @staticmethod
    def __compute_balanced_group_sizes(total: int, group_size: int) -> list[int]:
        for r in range(group_size):
            g = (total - r * (group_size - 1)) // group_size
            if g * group_size + r * (group_size - 1) == total:
                return [group_size] * g + [group_size - 1] * r
        raise ValueError("Impossible to distribute users fairly without 1-sized group.")

    @staticmethod
    def __compute_affinity_score(i: int, ungrouped: set[int], matrix: np.ndarray) -> int:
        return sum(matrix[i][j] + matrix[j][i] for j in ungrouped if j != i)

    @staticmethod
    def __find_best_leader(ungrouped: set[int], matrix: np.ndarray) -> int:
        return max(ungrouped, key=lambda i: Clustering.__compute_affinity_score(i, ungrouped, matrix))

    @staticmethod
    def __find_best_partners(leader_index: int, ungrouped: set[int], matrix: np.ndarray, num_partners: int) -> list[int]:
        scores = [
            (j, matrix[leader_index][j] + matrix[j][leader_index])
            for j in ungrouped if j != leader_index
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        return [j for j, _ in scores[:num_partners]]

    @staticmethod
    def __form_group(leader: int, partners: list[int]) -> list[int]:
        return [leader] + partners

    @staticmethod
    def __cluster_users_greedy_balanced(preferences: dict[User, list[User]], group_size: int) -> list[list[User]]:
        """
        Clusters users into balanced groups using a greedy approach based on affinity scores.
        """
        matrix, user_list = Clustering.__build_affinity_matrix(preferences)
        total_users = len(user_list)
        group_sizes = Clustering.__compute_balanced_group_sizes(total_users, group_size)

        ungrouped = set(range(total_users))
        groups = []

        for size in group_sizes:
            leader = Clustering.__find_best_leader(ungrouped, matrix)
            partners = Clustering.__find_best_partners(leader, ungrouped, matrix, size - 1)
            group_indices = Clustering.__form_group(leader, partners)
            group = [user_list[i] for i in group_indices]
            groups.append(group)
            ungrouped -= set(group_indices)

        return groups

    @staticmethod
    def cluster(preferences: dict[User, list[User]], group_size: int) -> tuple[list[list[User]], int]:
        """
        Main function to cluster users and calculate the total affinity score.
        """
        groups = Clustering.__cluster_users_greedy_balanced(preferences, group_size)
        matrix, user_list = Clustering.__build_affinity_matrix(preferences)

        total_score = 0
        for group in groups:
            indices = [user_list.index(u) for u in group]
            total_score += Clustering.__score_group(indices, matrix)

        return groups, total_score