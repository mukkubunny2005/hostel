import enum

class GenderEnum(str, enum.Enum):
    Male = "Male"
    Female = "Female"


class GovtIDEnum(str, enum.Enum):
    Aadhar = "Aadhar"
    PAN = "PAN"
    VoterID = "VoterID"

class NecessityEnum(str, enum.Enum):
    Student = "Student"
    Employee = "Employee"
    SelfEmployment = "Self Employee"
    Other = "Other"

class FoodEnum(str, enum.Enum):
    Veg = "Veg"
    NonVeg = "Non Veg"
    Both = "Both"
    
class RoomEnum(str, enum.Enum):
    AC = "AC"
    NONAC = "Non AC"