class VariableData:

    def __init__(self):
        self.setLocalVars = dict()
        self.setEnvVars = dict()
        self.setAliasVars = dict()
        self.setPathVars = set()
        self.setPathValues = dict()
        self.setModules = set()
        self.conflict = set()
