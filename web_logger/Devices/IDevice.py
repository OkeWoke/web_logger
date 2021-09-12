import abc
import time

class IDevice(metaclass=abc.ABCMeta):
    def __init__(self):
        self.name = ""
        self.dimensions = {}

    def get_dimensions(self):
        return sorted(self.dimensions.keys())

    def get_current_value(self):
        """Returns list with current values in order of sorted dimensions dict keys"""
        return self.dimensions
    
    def get_time_series(self, n):
        """Returns dimensions like dict with list of last n values as the value"""
        time_series = {}
        for col in self.get_dimensions():
            with open("{0}_{1}.log".format(self.name, col), "r") as f:
                time_series[col] = [f.readline()]
                for i in range(n-1):
                    val = f.readline()
                    if val=='':
                        break
                    time_series[col].append(val)
        return time_series

    def log(self):
        """Log current dimensions dict vals to disk"""
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        for col in self.get_dimensions():
            with open("{0}_{1}.log".format(self.name, col), "a+") as f:
                f.write(time_str)
                f.write(", ")
                f.write(self.dimensions[col])
                f.write('\n')
    
    @abc.abstractmethod
    def poll(self):
        """Implementation should internally update dimensions dict with this function, perhaps setup on a thread/periodically..."""
        pass
