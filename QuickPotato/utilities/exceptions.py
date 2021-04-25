class UnAcceptableTestIdFound(Exception):
    """
    QuickPotato has detected that your selected test are not found or are untested with
    boundary or regression test. If the latter is true you can bypass this check by enabling:

    options.allow_the_selection_of_untested_or_failed_test_ids = True

    """
    def __str__(self):
        return self.__doc__


class CouchPotatoCannotFindMethod(Exception):
    """
    QuickPotato has not detected any method to collect metrics from.
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


class UnableToGenerateVisualizations(Exception):
    """
    It was not possible to generate the requested visualization.
    Please review your input parameters.
    For more help, please consult the QuickPotato Documentation.
    """
    def __str__(self):
        return self.__doc__


class UnableToExportVisualization(Exception):
    """
    It was not possible to export the requested visualization to the disk.
    Please review your input parameters and verify if the folder exists.
    For more help, please consult the QuickPotato Documentation.
    """
    def __str__(self):
        return self.__doc__
