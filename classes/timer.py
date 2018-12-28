# Class for measuring elapsed time between calls to self.print
import time

class Performance_timer():
    def __init__(self, output):
        self.timer_start = time.perf_counter()
        self.last = 0.0
        print(output)

    # Print time elapsed since last print and total time since creation
    def print(self, output):
        now = float(self)
        print(output, "in: %.4fs" % float(now-self.last), "(total: %.4fs)" % now)
        self.last = now

    def done(self, output):
        print(output, "in", self)

    def __str__(self):
        return "%.4f" % (time.perf_counter()-self.timer_start)

    def __float__(self):
        return float("%.4f" % (time.perf_counter()-self.timer_start))
