import numpy as np
from src.domain.user import User


class Clustering:
    """
    Clustering class to handle user clustering based on weighted preferences.
    Each user assigns a numeric score to other users, indicating preference strength.
    """

    @staticmethod
    def __build_affinity_matrix(preferences: dict[User, dict[User, int]]) -> tuple[np.ndarray, list[User]]:
        """
        Builds an affinity matrix from weighted user preferences.
        Each element (i, j) in the matrix represents the score given by user i to user j.
        Args:
            preferences (dict[User, dict[User, int]]): 
                A dictionary where each key is a User, and the value is a dict of other Users
                associated with a numeric weight indicating preference strength.
        Returns:
            tuple[np.ndarray, list[User]]: 
                A square affinity matrix and the corresponding list of users (row/column indices).
        """
        users = list(preferences.keys())
        size = len(users)
        matrix = np.zeros((size, size), dtype=int)

        for i, user in enumerate(users):
            prefs = preferences.get(user, {})
            for preferred, score in prefs.items():
                if preferred in users:
                    j = users.index(preferred)
                    matrix[i][j] = score

        return matrix, users

    @staticmethod
    def __score_group(group_indices: list[int], matrix: np.ndarray) -> int:
        """
        Computes the affinity score of a group as the sum of all mutual preferences within the group.
        Args:
            group_indices (list[int]): List of indices of users in the group.
            matrix (np.ndarray): The affinity matrix.
        Returns:
            int: Total mutual affinity score within the group.
        """
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
        """
        Computes a list of group sizes that divide the total number of users as evenly as possible.
        Args:
            total (int): Total number of users.
            group_size (int): Desired maximum size per group.
        Returns:
            list[int]: List of group sizes that sum to total.
        Raises:
            ValueError: If no fair division is possible without creating a group of size 1.
        """
        for r in range(group_size):
            g = (total - r * (group_size - 1)) // group_size
            if g * group_size + r * (group_size - 1) == total:
                return [group_size] * g + [group_size - 1] * r
        raise ValueError("Impossible to distribute users fairly without 1-sized group.")

    @staticmethod
    def __compute_affinity_score(i: int, ungrouped: set[int], matrix: np.ndarray) -> int:
        """
        Computes how well a user connects (via preference scores) to the ungrouped population.
        Args:
            i (int): Index of the user.
            ungrouped (set[int]): Indices of ungrouped users.
            matrix (np.ndarray): The affinity matrix.
        Returns:
            int: Total bidirectional affinity score with ungrouped users.
        """
        return sum(matrix[i][j] + matrix[j][i] for j in ungrouped if j != i)

    @staticmethod
    def __find_best_leader(ungrouped: set[int], matrix: np.ndarray) -> int:
        """
        Selects the user who is best connected to others (highest affinity sum) as group leader.
        Args:
            ungrouped (set[int]): Indices of users not yet grouped.
            matrix (np.ndarray): The affinity matrix.
        Returns:
            int: Index of the most connected user among ungrouped ones.
        """
        return max(ungrouped, key=lambda i: Clustering.__compute_affinity_score(i, ungrouped, matrix))

    @staticmethod
    def __find_best_partners(leader_index: int, ungrouped: set[int], matrix: np.ndarray, num_partners: int) -> list[int]:
        """
        Selects the best `num_partners` users to group with a given leader based on mutual scores.
        Args:
            leader_index (int): Index of the leader user.
            ungrouped (set[int]): Indices of ungrouped users.
            matrix (np.ndarray): The affinity matrix.
            num_partners (int): Number of partners to select.
        Returns:
            list[int]: Indices of selected partner users.
        """
        scores = [
            (j, matrix[leader_index][j] + matrix[j][leader_index])
            for j in ungrouped if j != leader_index
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        return [j for j, _ in scores[:num_partners]]

    @staticmethod
    def __form_group(leader: int, partners: list[int]) -> list[int]:
        """
        Forms a group from a leader and their selected partners.
        Args:
            leader (int): Index of the leader.
            partners (list[int]): List of partner indices.
        Returns:
            list[int]: Complete list of indices forming the group.
        """
        return [leader] + partners

    @staticmethod
    def __cluster_users_greedy_balanced(preferences: dict[User, dict[User, int]], group_size: int) -> list[list[User]]:
        """
        Clusters users into balanced groups using a greedy algorithm based on preference weights.
        Args:
            preferences (dict[User, dict[User, int]]): User preference weights toward others.
            group_size (int): Target group size.
        Returns:
            list[list[User]]: List of groups with users.
        """
        matrix, user_list = Clustering.__build_affinity_matrix(preferences)
        total_users = len(user_list)

        if total_users == 0:
            return []

        group_sizes = Clustering.__compute_balanced_group_sizes(total_users, group_size)
        ungrouped = set(range(total_users))
        groups = []

        for size in group_sizes:
            if not ungrouped:
                break
            leader = Clustering.__find_best_leader(ungrouped, matrix)
            partners = Clustering.__find_best_partners(leader, ungrouped, matrix, size - 1)
            group_indices = Clustering.__form_group(leader, partners)
            group = [user_list[i] for i in group_indices]
            groups.append(group)
            ungrouped -= set(group_indices)

        return groups

    @staticmethod
    def cluster(preferences: dict[User, dict[User, int]], group_size: int) -> tuple[list[list[User]], int]:
        """
        Public method to perform clustering and return total affinity score.
        Args:
            preferences (dict[User, dict[User, int]]): User-to-user affinity weights.
            group_size (int): Desired number of users per group.
        Returns:
            tuple[list[list[User]], int]: Final grouped users and total affinity score.
        """
        groups = Clustering.__cluster_users_greedy_balanced(preferences, group_size)
        matrix, user_list = Clustering.__build_affinity_matrix(preferences)

        total_score = 0
        for group in groups:
            indices = [user_list.index(u) for u in group]
            total_score += Clustering.__score_group(indices, matrix)

        return groups, total_score