

class Student:
    """
    """
    def __init__(self, name: str, last_name: str, preferences: list["Student"] = None) -> None:
        """
        """
        self.name = name
        self.last_name = last_name
        self.preferences = preferences
        
    def __repr__(self) -> str:
        """
        """
        return f"Student(name={self.name}, last_name={self.last_name})"
    
    def __str__(self) -> str:
        """
        """
        return f"{self.name} {self.last_name}"
    
    def __eq__(self, other: "Student") -> bool:
        """
        """
        if not isinstance(other, Student):
            return False
        return self.name == other.name and self.last_name == other.last_name
    
    def __hash__(self) -> int:
        """
        """
        return hash((self.name, self.last_name))
    
    
        
    
    