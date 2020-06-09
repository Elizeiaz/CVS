class IncorrectCVSVersionError(Exception):
    def __init__(self, text):
        self.txt = text


class CVSNotInitializedError(Exception):
    def __init__(self, text):
        self.txt = text


class TrackFilesIsEmptyError(Exception):
    def __init__(self, text):
        self.txt = text
