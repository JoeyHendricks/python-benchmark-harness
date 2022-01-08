

def check_max_boundary(value: float, boundary: float or None) -> bool or None:
    """

    :param value:
    :param boundary:
    :return:
    """
    if boundary is None:
        return None

    elif value < boundary:
        return True

    else:
        return False


def check_min_boundary(value: float, boundary: float or None) -> bool or None:
    """

    :param value:
    :param boundary:
    :return:
    """
    if boundary is None:
        return None

    elif value > boundary:
        return True

    else:
        return False


def check_letter_rank_boundary(boundary_letter_rank: str, current_letter_rank: str) -> bool:
    """
    
    :param boundary_letter_rank: 
    :param current_letter_rank: 
    :return: 
    """
    # Determine rank as a number using the matrix
    letter_rank_matrix = {"S": 7, "A": 6, "B": 5, "C": 4, "D": 3, "E": 2, "F": 1}
    boundary_rank = letter_rank_matrix[boundary_letter_rank]
    active_rank = letter_rank_matrix[current_letter_rank[0]]

    # See if rank falls under or above the set boundary
    if active_rank >= boundary_rank:
        return True
    else:
        return False
