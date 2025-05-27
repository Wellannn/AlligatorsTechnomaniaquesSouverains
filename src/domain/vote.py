import uuid
from datetime import datetime
from typing import List

class Vote:
    def __init__(
        self,
        title: str,
        group_size: int,
        eligible_students: List[str],
        teachers: List[str],
        end_date: datetime,
        reliability_score= None,
        preference= None):

        if preference is None:
            preference = {}
        if reliability_score is None:
            reliability_score = 0.0
        self.id = str(uuid.uuid4())
        self.title = title
        self.group_size = group_size
        self.eligible_students = eligible_students
        self.teachers = teachers
        self.end_date = end_date
        self.reliability_score = reliability_score
        self.preferennces = preference

    def is_active(self) -> bool:
        """Retourne True si la date actuelle est antérieure à la date de fin du vote."""
        return datetime.now() < self.end_date

    def display_info(self):
        """Affiche les informations du vote."""
        print(f"Vote: {self.title}")
        print(f"Groupe de {self.group_size} personnes")
        print(f"Étudiants éligibles: {len(self.eligible_students)}")
        print(f"Enseignants: {', '.join(self.teachers)}")
        print(f"Date de fin: {self.end_date}")
        print(f"Score de fiabilité: {self.reliability_score}")
