class Repository:

    def __init__(self, data):

        self.id = data["id"]
        self.name = data["name"]
        self.full_name = data["full_name"]
        self.owner = data["owner"]["login"]
        self.default_branch = data["default_branch"]
        self.private = data["private"]

    def __repr__(self):

        return f"{self.owner}/{self.name}"