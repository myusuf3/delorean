from datetime import timedelta, datetime, time, date, tzinfo


class Delorean(object):
    """ The :class" `Delorean <Delorean>` object. It carries out all 
    functionality of the Delorean.
    """
    def __init__(self):
        #:datetime object
        self.now = datetime.utcnow()
    
    def __repr__(self):
        return '<Delorean[%s]>' % (self.now)
    
    def today(self):
        return self.now.date()
    
    def tomorrow(self):
        one_day = timedelta(days=1)
        today = datetime.utcnow()
        tomorow = today + one_day
        return tomorrow
    
    def timetravel(self, days=0, minutes=0, 
        hours=0, seconds=0, milliseconds=0, microseconds=0, weeks=0):
        """ This accepts negative values which is cool since it kind of works like time travel.
        """

        travel = timedelta(days=days, hours=hours, 
                            minutes=minutes, seconds=seconds, milliseconds=milliseconds, microseconds=microseconds)
        self.now = self.now + travel

        return self.now



class DeloreanDateTime(object):
    def __init__(self):
        pass


