from src.clustering.clustering import Clustering
from src.domain.user import User


class AlgoService:
    """
    AlgoService class to handle clustering operations.
    It uses the Clustering class to perform user clustering based on weighted preferences.
    """

    def __init__(self, preferences: dict[User, dict[User, int]]):
        """
        Initializes the AlgoService with user preferences.
        Args:
            preferences (dict[User, dict[User, int]]): 
                A dictionary where each key is a User, and the value is a dict of other Users
                associated with a numeric weight indicating preference strength.
        """
        self.preferences = preferences
        self.clustering = Clustering()
        
    def cluster_users(self, group_size: int) -> list[list[User]]:
        """
        Clusters users based on their preferences into groups of a specified size.
        Args:
            group_size (int): Desired size of each group.
        Returns:
            list[list[User]]: A list of user groups, each containing users clustered together.
        """
        return self.clustering.cluster_users(self.preferences, group_size)