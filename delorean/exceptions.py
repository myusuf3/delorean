class DeloreanError(Exception):
    """
    Base Delorean Exception class
    """

    def __init__(self, msg):
        self.msg = unicode(msg)
        Exception.__init__(self, msg)

    def __str__(self):
        return self.msg
