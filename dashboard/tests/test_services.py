import pytest

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

    def test_get_sum_action_points_claimed_smiley_no_remaining_points(
            self, claimed_smiley_no_remaining_points,
            smileys_with_same_description, oopsy_custom_description):
        """Confirm claimed smiley with no remaining points is not counted
        towards total points."""
        smileys = Smiley.objects.all()
        oopsy = Oopsy.objects.filter(pk=1)
        assert smileys.count() == 6
        star_awarding = StarAwarding(smileys, oopsy, 15)
        assert star_awarding.get_sum_action_points(smileys) == 25

    def test_get_sum_action_points_claimed_oopsy_no_remaining_points(
            self, claimed_oopsy_no_remaining_points,
            oopsies_with_same_description, smiley_custom_description):
        """Confirm claimed oopsy with no remaining points is not counted
        towards total points."""
        smiley = Smiley.objects.filter(pk=1)
        oopsies = Oopsy.objects.all()
        assert oopsies.count() == 6
        star_awarding = StarAwarding(smiley, oopsies, 15)
        assert star_awarding.get_sum_action_points(oopsies) == 25

    def test_get_sum_action_points_claimed_smiley_remaining_points(
            self, claimed_smiley_remaining_points,
            smileys_with_same_description, oopsy_custom_description):
        """Confirm remaining points from claimed smiley are counted towards
        total points."""
        smileys = Smiley.objects.all()
        oopsy = Oopsy.objects.filter(pk=1)
        assert smileys.count() == 6
        star_awarding = StarAwarding(smileys, oopsy, 15)
        assert star_awarding.get_sum_action_points(smileys) == 26

    def test_claim_all_oopsies(self, oopsies_with_same_description,
                               smiley_custom_description):
        """Confirm claim_all_oopsies updates status of all oopsies to
        claimed."""
        smiley = Smiley.objects.filter(pk=1)
        oopsies = Oopsy.objects.all()
        star_awarding = StarAwarding(smiley, oopsies, 15)
        star_awarding.claim_all_oopsies()
        claimed_oopsies = Oopsy.objects.filter(claimed=True)
        assert claimed_oopsies.count() == 5

