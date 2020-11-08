class AgentCannotProcessProfilerOutput(Exception):
    """
    An exception occurred while trying to process the results of the profiler.
    Please review the QuickPotato documentation and validate your raw profiled output.
    """
    def __str__(self):
        return self.__doc__


class AgentCannotFindMethod(Exception):
    """
    The profiling agent has not detected any method to collect metrics from.
    Please review the use of the 'profile' decorator in the QuickPotato documentation.
    """
    def __str__(self):
        return self.__doc__


class DatabaseSchemaCannotBeSpawned(Exception):
    """
    It was not possible to create a database with a specified connection URL, p
    lease review your URL and try again.
    For more help, please consult the QuickPotato Documentation.
    """
    def __str__(self):
        return self.__doc__


class DatabaseTableCannotBeSpawned(Exception):
    """
    It was not possible to create a table within the test cases database.
    Please review your connection URL and database name.
    For more help, please consult the QuickPotato Documentation.
    """
    def __str__(self):
        return self.__doc__


class DatabaseConnectionCannotBeSpawned(Exception):
    """
    It was not possible to create a connection to the database server.
    Please review your connection URL.
    For more help, please consult the QuickPotato Documentation.
    """
    def __str__(self):
        return self.__doc__


class NeedsKeyWordArguments(Exception):
    """
    The decorator was called with positional arguments.
    Please call the decorator with the keyword arguments.
    """
    def __str__(self):
        return self.__doc__
