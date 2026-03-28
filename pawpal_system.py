from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from enum import Enum


class TaskCategory(Enum):
    """Enum for task categories"""
    FEEDING = "Feeding"
    WALKING = "Walking"
    MEDICATION = "Medication"
    GROOMING = "Grooming"
    PLAY = "Play"
    OTHER = "Other"


@dataclass
class Task:
    """Represents a pet care task"""
    name: str
    duration: int  # duration in minutes
    priority: int  # 1-5, where 5 is highest priority
    category: TaskCategory
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    def mark_completed(self) -> None:
        """Mark the task as completed"""
        self.completed = True
    
    def edit_task(self, **kwargs) -> None:
        """Edit task attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


@dataclass
class Pet:
    """Represents a pet"""
    name: str
    species: str
    age: int  # age in years
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the pet"""
        self.tasks.append(task)
    
    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet"""
        if task in self.tasks:
            self.tasks.remove(task)
    
    def get_tasks(self) -> List[Task]:
        """Get all tasks for the pet"""
        return self.tasks


class Owner:
    """Represents a pet owner"""
    
    def __init__(self, name: str, daily_time_available: int = 0, preferences: dict = None):
        """
        Initialize an Owner
        
        Args:
            name: Owner's name
            daily_time_available: Available time in minutes per day
            preferences: Dictionary of owner preferences
        """
        self.name = name
        self.daily_time_available = daily_time_available
        self.preferences = preferences if preferences is not None else {}
        self.pets: List[Pet] = []
    
    def update_preferences(self, **kwargs) -> None:
        """Update owner preferences"""
        self.preferences.update(kwargs)
    
    def update_time_available(self, minutes: int) -> None:
        """Update available daily time"""
        self.daily_time_available = minutes
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection"""
        self.pets.append(pet)
    
    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's collection"""
        if pet in self.pets:
            self.pets.remove(pet)


class Scheduler:
    """Creates the daily plan for pet care tasks"""
    
    def __init__(self, owner: Owner):
        """
        Initialize the Scheduler
        
        Args:
            owner: The pet owner object
        """
        self.owner = owner
        self.daily_plan: List[Task] = []
    
    def generate_plan(self) -> List[Task]:
        """
        Generate a daily plan based on all pets' tasks and owner's time available
        
        Returns:
            List of tasks sorted and scheduled for the day
        """
        # Collect all tasks from all pets
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.get_tasks())
        
        # Sort by priority and fit within available time
        self.daily_plan = self.sort_tasks_by_priority(all_tasks)
        return self.daily_plan
    
    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by priority (highest priority first)
        
        Args:
            tasks: List of tasks to sort
            
        Returns:
            Sorted list of tasks
        """
        return sorted(tasks, key=lambda task: task.priority, reverse=True)
    
    def explain_plan(self) -> str:
        """
        Generate a human-readable explanation of the daily plan
        
        Returns:
            String explanation of the scheduled tasks
        """
        if not self.daily_plan:
            return "No tasks scheduled for today."
        
        explanation = "Daily Pet Care Plan:\n"
        total_time = sum(task.duration for task in self.daily_plan)
        explanation += f"Total time required: {total_time} minutes\n"
        explanation += f"Available time: {self.owner.daily_time_available} minutes\n\n"
        
        for i, task in enumerate(self.daily_plan, 1):
            explanation += f"{i}. {task.name} ({task.category.value})\n"
            explanation += f"   Duration: {task.duration} min | Priority: {task.priority}/5\n"
        
        return explanation
