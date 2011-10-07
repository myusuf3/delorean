from datetime import timedelta, datetime, time, date, tzinfo


class Delorean(object):
    """ The :class" `Delorean <Delorean>` object. It carries out all 
    functionality of the Delorean.
    """
    def __init__(self):
        #:datetime object
        self.utcdatetime = datetime.utcnow()
    
    def __repr__(self):
        return '<Delorean[%s]>' % (self.utcdatetime)

    def time(self):
        return self.utcdatetime.time()
    
    def tomorrow(self):
        one_day = timedelta(days=1)
        today = self.utcdatetime
        tomorrow = today + one_day
        self.utcdatetime = tomorrow
    
    def date(self):
        return self.utcdatetime.date()
            
    def timetravel(self, days=0, minutes=0, 
        hours=0, seconds=0, milliseconds=0, microseconds=0, weeks=0):
        """ This accepts negative values which is cool since it kind of works like time travel.
        """

        travel = timedelta(days=days, hours=hours, 
                            minutes=minutes, seconds=seconds, milliseconds=milliseconds, microseconds=microseconds)
        self.utcdatetime = self.utcdatetime + travel
        return self.utcdatetime



class DeloreanDateTime(object):
    def __init__(self):
        pass


class DeloreanTime(object):
    def __init__(self):
        pass





