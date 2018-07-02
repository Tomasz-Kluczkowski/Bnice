# Place service functions here


class StarAwarding:
    """Class to help awarding stars.

    This helper class is to be used in views when we have to decide if stars
    should be awarded. The smiley which completes the amount of points required
    to earn a star will get attribute star_awarded set to True.
    If the smiley had more points than was needed to award a star they will
    be saved as points_remaining on the last smiley accessed before terminating
    the loop.

    """

    def __init__(self, smileys, oopsies, star_points):
        """Initialize class.

        Parameters
        ----------
        smileys : Queryset(Smiley)
            Django queryset of filtered Smiley objects
            (for current child in view).
        oopsies : Queryset(Ooopsy)
            Django queryset of filtered Oopsy objects
            (for current child in view).
        star_points : int
            Attribute of Child object. Amount of points required to earn a
            star.
        """
        self.smileys = smileys
        self.oopsies = oopsies
        self.star_points = star_points
        self.smiley_points = self.get_sum_action_points(self.smileys)
        self.oopsy_points = self.get_sum_action_points(self.oopsies)
        self.total_points = self.smiley_points - self.oopsy_points

    def __str__(self):
        return ("smiley points: {0}\n"
                "oopsy points: {1}\n"
                "total points: {2}\n"
                "star points: {3}".format(self.smiley_points,
                                          self.oopsy_points,
                                          self.total_points,
                                          self.star_points))

    def update_smiley_points(self):
        """Renews sum of smiley_points.

        Returns
        -------
            None
        """
        self.smiley_points = self.get_sum_action_points(self.smileys)

    def update_oopsy_points(self):
        """Renews sum of oopsy_points.

        Returns
        -------
            None
        """
        self.oopsy_points = self.get_sum_action_points(self.oopsies)

    def update_total_points(self):
        """Renews total_points.

        Returns
        -------
            None
        """
        self.update_smiley_points()
        self.update_oopsy_points()
        self.total_points = self.smiley_points - self.oopsy_points

    def get_sum_action_points(self, actions):
        """Get total number of points for action collection.

        Calculate sum of positive or negative points collected by child based
        on action type and owner.

        Parameters
        ----------
        actions : Queryset(Action)
            Django queryset of filtered Action objects
            (for current child in view).

        Returns
        -------
            action_points : int
                Total amount of points collected per action type.
                Returns 0 if no points were collected.
        """
        action_points = 0
        if not actions:
            return 0
        for action in actions:
            # Action fully consumed.
            if action.claimed and action.points_remaining == 0:
                continue
            # Action not claimed.
            elif not action.claimed:
                action_points += action.points
            # Always add remaining points no matter if action is claimed or
            # not.
            action_points += action.points_remaining

        return action_points

    def claim_all_oopsies(self):
        """Claim all oopsies.

        Changes claimed field to True on all oopsies as they get all consumed
        before a star can be awarded.

        Returns
        -------
            None
        """
        self.oopsies.update(claimed=True)
        for oopsy in self.oopsies:
            oopsy.save()

    def award_star(self):
        """Iterate through smileys and oopsies and award stars.

        Count points during the iteration and add star_awarded = True to the
        smiley which completes the amount of points required for a star.

        Returns
        -------
            None
        """
        # Any remaining points should be saved in memory first as
        # points_counter until we get to the last smiley in queryset where if
        # points_counter is > 0 we have to save it on that last smiley object.
        points_counter = 0
        last_smiley_ix = self.smileys.count() - 1
        # Confirm that we can award a star.
        if self.total_points >= self.star_points:
            # Make sure all oopsies are consumed.
            self.claim_all_oopsies()
            # Start counting having the negative points as the initial value
            # and increase it until points_counter >= star_points.
            points_counter -= self.oopsy_points
            # Now iterate over smileys marking all as claimed until a star
            # is earned.
            for ix, smiley in enumerate(self.smileys):
                # For smileys that were completely consumed skip.
                if smiley.claimed and smiley.points_remaining == 0:
                    continue
                # Unclaimed smileys.
                elif not smiley.claimed:
                    points_counter += smiley.points
                # Always add any remaining points and set claimed to True
                # no matter if smiley was claimed or not.
                points_counter += smiley.points_remaining
                smiley.points_remaining = 0
                smiley.claimed = True
                # Check if star can be awarded.
                if points_counter >= self.star_points:
                    smiley.star_awarded = True
                    # Remaining points will be stored on points_counter until
                    # we reach the last item in the iteration.
                    points_counter = points_counter - self.star_points
                    # If we are on the last smiley save remaining points on it.
                    if ix == last_smiley_ix and points_counter > 0:
                        smiley.points_remaining = points_counter
                smiley.save()
                self.update_total_points()
                # After awarding a star abort if sum of points is too
                # little to award another star.
                if self.total_points + points_counter < self.star_points:
                    break
