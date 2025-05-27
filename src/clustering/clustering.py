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
        Builds an affinity matrix from user preferences, where each entry represents the affinity score between two users.
        Args:
            preferences (dict[User, list[User]]): A dictionary where keys are User objects and values are lists of preferred User objects.
        Returns:
            tuple[np.ndarray, list[User]]: A tuple containing the affinity matrix and a list of users.
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
        """
        Computes the affinity score for a group of users based on their indices in the affinity matrix.
        Args:
            group_indices (list[int]): A list of indices representing the users in the group.
            matrix (np.ndarray): The affinity matrix.
        Returns:
            int: The total affinity score for the group.
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
        Computes balanced group sizes based on the total number of users and the desired group size.
        Args:
            total (int): Total number of users.
            group_size (int): Desired size of each group.
        Returns:
            list[int]: A list of group sizes that balances the total number of users.
        Raises:
            ValueError: If it is impossible to distribute users fairly without a 1-sized group.
        """
        for r in range(group_size):
            g = (total - r * (group_size - 1)) // group_size
            if g * group_size + r * (group_size - 1) == total:
                return [group_size] * g + [group_size - 1] * r
        raise ValueError("Impossible to distribute users fairly without 1-sized group.")

    @staticmethod
    def __compute_affinity_score(i: int, ungrouped: set[int], matrix: np.ndarray) -> int:
        """
        Computes the affinity score for a user based on their connections to ungrouped users.
        Args:
            i (int): Index of the user in the affinity matrix.
            ungrouped (set[int]): Set of indices of users that are not yet grouped.
            matrix (np.ndarray): The affinity matrix.
        Returns:
            int: The total affinity score for the user with respect to the ungrouped users.
        """
        return sum(matrix[i][j] + matrix[j][i] for j in ungrouped if j != i)

    @staticmethod
    def __find_best_leader(ungrouped: set[int], matrix: np.ndarray) -> int:
        """
        Finds the best leader from the ungrouped users based on their affinity scores.
        Args:
            ungrouped (set[int]): Set of indices of users that are not yet grouped.
            matrix (np.ndarray): The affinity matrix.
        Returns:
            int: The index of the user who has the highest affinity score with respect to the ungrouped users.
        """
        return max(ungrouped, key=lambda i: Clustering.__compute_affinity_score(i, ungrouped, matrix))

    @staticmethod
    def __find_best_partners(leader_index: int, ungrouped: set[int], matrix: np.ndarray, num_partners: int) -> list[int]:
        """
        Finds the best partners for a leader based on their affinity scores with respect to the ungrouped users.
        Args:
            leader_index (int): Index of the leader in the affinity matrix.
            ungrouped (set[int]): Set of indices of users that are not yet grouped.
            matrix (np.ndarray): The affinity matrix.
            num_partners (int): Number of partners to select for the group.
        Returns:
            list[int]: A list of indices of the best partners for the leader.
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
        Forms a group by combining the leader with their partners.
        Args:
            leader (int): Index of the leader in the affinity matrix.
            partners (list[int]): List of indices of partners to be included in the group.
        Returns:
            list[int]: A list containing the index of the leader followed by the indices of the partners.
        """
        return [leader] + partners

    @staticmethod
    def __cluster_users_greedy_balanced(preferences: dict[User, list[User]], group_size: int) -> list[list[User]]:
        """
        Clusters users into balanced groups based on their preferences using a greedy approach.
        Args:
            preferences (dict[User, list[User]]): A dictionary where keys are User objects and values are lists of preferred User objects.
            group_size (int): Desired size of each group.
        Returns:
            list[list[User]]: A list of groups, where each group is a list of User objects.
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
        Clusters users into balanced groups based on their preferences and computes the total affinity score for the groups.
        Args:
            preferences (dict[User, list[User]]): A dictionary where keys are User objects and values are lists of preferred User objects.
            group_size (int): Desired size of each group.
        Returns:
            tuple[list[list[User]], int]: A tuple containing a list of groups (each group is a list of User objects) and the total affinity score for all groups.
        """
        groups = Clustering.__cluster_users_greedy_balanced(preferences, group_size)
        matrix, user_list = Clustering.__build_affinity_matrix(preferences)

        total_score = 0
        for group in groups:
            indices = [user_list.index(u) for u in group]
            total_score += Clustering.__score_group(indices, matrix)

        return groups, total_score