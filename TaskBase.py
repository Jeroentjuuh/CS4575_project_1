class TaskBase:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return f"Task: {self.name} - {self.description} - {self.priority}"

    def __repr__(self):
        return f"Task: {self.name} - {self.description} - {self.priority}"
    
    def run(self, video = None, watchtime = 30):
        raise NotImplementedError("Subclasses must implement this method")