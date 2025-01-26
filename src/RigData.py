class RigData:
    class Joint:
        def __init__(self, name, rig_data):
            self.name = name
            rig_data.joints.append(self)
            self.keyframes = [] # should contain a tuple with xyz
            self.children = [] # should contain other joints

        def add_keyframe(self, x, y, z):
            self.keyframes.append((x, y, z))

        def __str__(self):
            return self.name

    def __init__(self):
        self.joints = []

