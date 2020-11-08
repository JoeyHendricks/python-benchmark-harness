from QuickPotato.profiling.intrusive import performance_critical
import math


@performance_critical
def slow_method():
    num = 6 ** 6 ** 6
    return len(str(num))


@performance_critical
def fast_method():
    num = 6 ** 6 ** 6
    return int(math.log10(num))
