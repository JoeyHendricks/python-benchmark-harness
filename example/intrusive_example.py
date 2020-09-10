from QuickPotato.inspect.intrusive import performance_critical


@performance_critical()
def example():
    return 1 + 1
