# Place service functions here
def get_total_points(smileys, oopsies):
    """Get total number of points collected.

    Calculate sum of positive and negative points collected by child.

    Parameters
    ----------
    smileys : Queryset(Smiley)
        Django queryset of filtered Smiley objects (for current child in view).
    oopsies : Queryset(Oopsy)
        Django queryset of filtered Oopsy objects (for current child in view).

    Returns
    -------
        total_points : int or None
            Total amount of points collected. Can be negative.
            Returns None if no points were collected.
    """
    total_points = 0
    if not smileys and not oopsies:
        return None
    # Count smileys as positive points, oopsies as negative.
    for smiley in smileys:
        total_points += smiley.points
    for oopsy in oopsies:
            total_points -= oopsy.points

    return total_points
