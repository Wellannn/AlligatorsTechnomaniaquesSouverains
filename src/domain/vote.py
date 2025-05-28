import uuid
from datetime import datetime
from typing import List

class Vote:
    """
    Represents a vote for a group project.
    Each vote has a unique identifier, a title, a group size, a list of eligible students, a list of teachers, an end date, a reliability score, and preferences.
    """
    def __init__(self,
                title: str,
                group_size: int,
                eligible_students: List[str],
                teachers: List[str],
                end_date: datetime,
                reliability_score: float = 0.0,
                preference: dict = None) -> None:
        """
        Initializes a new vote with a title, group size, eligible students, teachers, end date, reliability score, and preferences.
        Args:
            title (str): The title of the vote.
            group_size (int): The size of the group for the vote.
            eligible_students (List[str]): A list of eligible students for the vote.
            teachers (List[str]): A list of teachers associated with the vote.
            end_date (datetime): The end date of the vote.
            reliability_score (float, optional): The reliability score of the vote. Defaults to 0.0.
            preference (dict, optional): A dictionary of preferences for the vote. Defaults to an empty dictionary.
        Returns:
            None
        """

        if preference is None:
            preference = {}
        self.id = str(uuid.uuid4())
        self.title = title
        self.group_size = group_size
        self.eligible_students = eligible_students
        self.teachers = teachers
        self.end_date = end_date
        self.reliability_score = reliability_score
        self.preferennces = preference

    def is_active(self) -> bool:
        """
        Checks if the vote is still active based on the current date and the end date of the vote.
        Returns:
            bool: True if the vote is still active, False otherwise.
        """
        return datetime.now() < self.end_date