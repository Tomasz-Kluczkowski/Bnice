import pytest

from django.db.models import Sum
from dashboard.models import Smiley, Oopsy
from dashboard.services import StarAwarding

# Mark all tests as requiring database.
pytestmark = pytest.mark.django_db


class TestStarAwarding:

    def test_str(self, star_awarding_base):
        """Confirm string representation is correct."""
        assert star_awarding_base.__str__() == ("smiley points: 5\n"
                                                "oopsy points: 5\n"
                                                "total points: 0\n"
                                                "star points: 15")

    def test_update_smiley_points(self, star_awarding_base):
        """Check if smiley points are counted correctly."""
        star_awarding_base.update_smiley_points()
        assert star_awarding_base.smiley_points == 5

    def test_update_oopsy_points(self, star_awarding_base):
        """Check if oopsy points are counted correctly."""
        star_awarding_base.update_oopsy_points()
        assert star_awarding_base.oopsy_points == 5

    def test_update_total_points(self, star_awarding_base):
        """Confirm total points are counted correctly."""
        star_awarding_base.update_total_points()
        assert star_awarding_base.total_points == 0

    # Test get_sum_action_points - all possibilities

    def test_get_sum_action_points_claimed_smiley_no_remaining_points(self, claimed_smiley_no_remaining_points,
                                                                      smileys_with_same_description,
                                                                      oopsy_custom_description):
        """Confirm claimed smiley with no remaining points is not counted towards total points."""
        smileys = Smiley.objects.all()
        oopsy = Oopsy.objects.filter(pk=1)
        assert smileys.count() == 6
        star_awarding = StarAwarding(smileys, oopsy, 15)
        assert star_awarding.get_sum_action_points(smileys) == 25

    def test_get_sum_action_points_claimed_oopsy_no_remaining_points(self, claimed_oopsy_no_remaining_points,
                                                                     oopsies_with_same_description,
                                                                     smiley_custom_description):
        """Confirm claimed oopsy with no remaining points is not counted towards total points."""
        smiley = Smiley.objects.filter(pk=1)
        oopsies = Oopsy.objects.all()
        assert oopsies.count() == 6
        star_awarding = StarAwarding(smiley, oopsies, 15)
        assert star_awarding.get_sum_action_points(oopsies) == 25

    def test_get_sum_action_points_claimed_smiley_remaining_points(self, claimed_smiley_remaining_points,
                                                                   smileys_with_same_description, oopsy_custom_description):
        """Confirm remaining points from claimed smiley are counted towards total points."""
        smileys = Smiley.objects.all()
        oopsy = Oopsy.objects.filter(pk=1)
        assert smileys.count() == 6
        star_awarding = StarAwarding(smileys, oopsy, 15)
        assert star_awarding.get_sum_action_points(smileys) == 26

    def test_claim_all_oopsies(self, oopsies_with_same_description, smiley_custom_description):
        """Confirm claim_all_oopsies updates status of all oopsies to claimed."""
        smiley = Smiley.objects.filter(pk=1)
        oopsies = Oopsy.objects.all()
        star_awarding = StarAwarding(smiley, oopsies, 15)
        star_awarding.claim_all_oopsies()
        claimed_oopsies = Oopsy.objects.filter(claimed=True)
        assert claimed_oopsies.count() == 5

    # Test award_star - all possibilities
    # Case 1
    # No oopsies, smileys match exactly star_points required, no remaining
    # points after star is awarded.
    # Case 2
    # With oopsy giving negative score, smileys match exactly start_points
    # required.
    # Case 3
    # No oopsies. Last smiley has too many points and some go as remaining.
    # Case 4
    # With oopsy, last smiley has too many points and some will be remaining.
    # Case 5
    # Enough smiley points to award multiple stars.
    def test_award_star_only_smileys_no_remaining_points(self, smileys_with_same_description):
        """Confirm all smileys are consumed and no points remain."""
        smileys = Smiley.objects.all()
        # Create an empty oopsy queryset.
        oopsy = Oopsy.objects.all()
        star_awarding = StarAwarding(smileys, oopsy, 25)
        star_awarding.award_star()
        smileys = Smiley.objects.filter(claimed=True, points_remaining=0)
        assert smileys.count() == 5
        assert Smiley.objects.filter(star_awarded=True).count() == 1
        remaining_points = smileys.aggregate(Sum('points_remaining'))
        assert remaining_points['points_remaining__sum'] == 0

    def test_award_star_no_remaining_points(self, smileys_with_same_description, oopsy_custom_description):
        """Confirm all smileys are consumed and no points remain and oopsy reduces points."""
        smileys = Smiley.objects.all()
        oopsy = Oopsy.objects.all()
        star_awarding = StarAwarding(smileys, oopsy, 20)
        star_awarding.award_star()
        smileys = Smiley.objects.filter(claimed=True, points_remaining=0)
        assert smileys.count() == 5
        assert Smiley.objects.filter(star_awarded=True).count() == 1
        remaining_points = smileys.aggregate(Sum('points_remaining'))
        assert remaining_points['points_remaining__sum'] == 0

    def test_award_star_only_smileys_with_remaining_points(self, smileys_with_same_description):
        """Confirm all smileys are consumed and points remain."""
        smileys = Smiley.objects.all()
        # Create an empty oopsy queryset.
        oopsy = Oopsy.objects.all()
        star_awarding = StarAwarding(smileys, oopsy, 24)
        star_awarding.award_star()
        smileys_no_remaining = Smiley.objects.filter(claimed=True, points_remaining=0)
        assert smileys_no_remaining.count() == 4
        smiley_with_remaining = Smiley.objects.filter(claimed=True, points_remaining=1)
        assert smiley_with_remaining.count() == 1
        assert Smiley.objects.filter(star_awarded=True).count() == 1
        remaining_points = smileys.aggregate(Sum('points_remaining'))
        assert remaining_points['points_remaining__sum'] == 1

    def test_award_star_with_remaining_points(self, smileys_with_same_description, oopsy_custom_description):
        """Confirm all smileys are consumed and points remain and oopsy points are negative."""
        smileys = Smiley.objects.all()
        oopsy = Oopsy.objects.all()
        star_awarding = StarAwarding(smileys, oopsy, 19)
        star_awarding.award_star()
        smileys_no_remaining = Smiley.objects.filter(claimed=True, points_remaining=0)
        assert smileys_no_remaining.count() == 4
        smiley_with_remaining = Smiley.objects.filter(claimed=True, points_remaining=1)
        assert smiley_with_remaining.count() == 1
        assert Smiley.objects.filter(star_awarded=True).count() == 1
        remaining_points = smileys.aggregate(Sum('points_remaining'))
        assert remaining_points['points_remaining__sum'] == 1

    def test_award_star_multiple_stars(self, smileys_with_same_description, oopsy_custom_description):
        """Confirm multiple stars are correctly awarded."""
        smileys = Smiley.objects.all()
        oopsy = Oopsy.objects.all()
        star_awarding = StarAwarding(smileys, oopsy, 9)
        star_awarding.award_star()
        smileys_no_remaining = Smiley.objects.filter(claimed=True,
                                                     points_remaining=0)
        assert smileys_no_remaining.count() == 4
        smiley_with_remaining = Smiley.objects.filter(claimed=True,
                                                      points_remaining__gt=0)
        assert smiley_with_remaining.count() == 1
        assert Smiley.objects.filter(star_awarded=True).count() == 2
        remaining_points = smileys.aggregate(Sum('points_remaining'))
        assert remaining_points['points_remaining__sum'] == 2

    def test_award_star_multiple_stars_use_all(self, claimed_smiley_no_remaining_points, smileys_with_same_description):
        """Confirm multiple stars are correctly awarded."""
        smileys = Smiley.objects.all()
        assert smileys.count() == 6
        oopsy = Oopsy.objects.all()
        star_awarding = StarAwarding(smileys, oopsy, 8)
        assert star_awarding.get_sum_action_points(smileys) == 25
        star_awarding.award_star()
        smileys_no_remaining = Smiley.objects.filter(claimed=True, points_remaining=0)
        assert smileys_no_remaining.count() == 5
        smiley_with_remaining = Smiley.objects.filter(claimed=True, points_remaining__gt=0)
        assert smiley_with_remaining.count() == 1
        assert Smiley.objects.filter(star_awarded=True).count() == 3
        remaining_points = smileys.aggregate(Sum('points_remaining'))
        assert remaining_points['points_remaining__sum'] == 1
