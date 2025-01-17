from otree.api import Page, WaitPage
from .models import Constants
import random
import time
from otree.api import WaitPage
from otree.api import Currency as c, currency_range



class Countdown(Page):
    timeout_seconds = 180

    def is_displayed(self):
        return self.round_number == 4


class Countdown_2(Page):
    timeout_seconds = 180

    def is_displayed(self):
        return self.round_number == 8



class MatchingWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.individual_rounds + 1

    def after_all_players_arrive(self):
        if self.round_number == Constants.individual_rounds + 1:
            players = self.subsession.get_players()
            group_matrix = []
            for i in range(0, len(players), Constants.players_per_group):
                group = players[i:i + Constants.players_per_group]
                group_matrix.append(group)

                # Record partner IDs
                if len(group) == 2:
                    group[0].partner_id = group[1].id_in_subsession
                    group[1].partner_id = group[0].id_in_subsession

            self.subsession.set_group_matrix(group_matrix)
class DummyWaitPage(WaitPage):
    group_by_arrival_time = True

    def is_displayed(self):
        return False  # This page will never be displayed

    def after_all_players_arrive(self):
        pass  # This will never be called


class WelcomeStructure(Page):
    template_name = 'investment_game/welcome_structure.html'

    def is_displayed(self):
        return self.round_number == 1


class HowToWin(Page):
    template_name = 'investment_game/how_to_win.html'

    def is_displayed(self):
        return self.round_number == 1


class EarningsCalculation(Page):
    template_name = 'investment_game/earnings_calculation.html'

    def is_displayed(self):
        return self.round_number == 1

class example(Page):
    template_name = 'investment_game/example.html'

    def is_displayed(self):
        return self.round_number == 1


class IndividualRoundsSummary(Page):
    form_model = 'player'
    form_fields = ['close_field']

    def is_displayed(self):
        return (self.round_number == 4) or (self.round_number == 12)

    def vars_for_template(self):
        if self.round_number == 4:
            total_earnings = sum([p.earnings for p in self.player.in_rounds(1, 4)])
            rounds = self.player.in_rounds(1, 4)
        elif self.round_number == 12:
            total_earnings = sum([p.earnings for p in self.player.in_rounds(9, 12)])
            rounds = self.player.in_rounds(9, 12)
        else:
            total_earnings = 0
            rounds = []

        return {
            'total_earnings': total_earnings,
            'individual_rounds': Constants.individual_rounds,
            'rounds': rounds
        }

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class InvestmentPage(Page):
    form_model = 'player'
    form_fields = ['investment']

    def is_displayed(self):
        return (1 <= self.round_number <= 4) or (9 <= self.round_number <= 12)

    def vars_for_template(self):
        if self.player.success_number is None:
            self.player.success_number = random.randint(1, 6)

        return {
            'success_number': self.player.success_number,
            'current_round': self.round_number,
            'total_rounds': Constants.individual_rounds,
            'round_number': self.round_number

        }


class DiceRollingPage(Page):
    def is_displayed(self):
        return (1 <= self.round_number <= 4) or (9 <= self.round_number <= 12)

    def vars_for_template(self):
        self.player.dice_roll = random.randint(1, 6)
        return {
            'dice_roll': self.player.dice_roll,
            'current_round': self.round_number,
            'total_rounds': Constants.individual_rounds,
            'round_number': self.round_number

        }

    def before_next_page(self):
        self.player.success = self.player.dice_roll == self.player.success_number
        if self.player.success:
            self.player.earnings = self.player.investment * 6
        else:
            self.player.earnings = self.player.investment * -1
        self.participant.vars['total_earnings'] = self.participant.vars.get('total_earnings', 0) + self.player.earnings

class ResultsPage(Page):
    def is_displayed(self):
        return (1 <= self.round_number <= 4) or (9 <= self.round_number <= 12)

    def vars_for_template(self):
        if self.player.success:
            self.player.earnings = (6 * self.player.investment)
        else:
            self.player.earnings = -1 *  self.player.investment

        self.participant.vars['total_earnings'] = self.participant.vars.get('total_earnings', 0) + self.player.earnings

        return {
            'investment': f"{self.player.investment:.2f}",
            'dice_roll': self.player.dice_roll,
            'success_number': self.player.success_number,
            'success': self.player.success,
            'earnings': f"{self.player.earnings:.2f}",
            'round_number': self.round_number,
            'total_rounds': Constants.individual_rounds
        }


class EndSlide(Page):
    template_name = 'investment_game/EndSlide.html'
    form_model = 'player'
    form_fields = ['close_field']

    def is_displayed(self):
        return (self.round_number == 4) or (self.round_number == 12)

    def vars_for_template(self):
        if self.round_number == 4:
            fourth_round_earnings = self.player.in_round(4).earnings
        elif self.round_number ==12:
            fourth_round_earnings = self.player.in_round(12).earnings
        else:
            total_earnings = 0
            rounds = []
        return {
            'fourth_round_earnings': fourth_round_earnings
        }

class TotalEarningsPage(Page):
    def is_displayed(self):
        return self.round_number in [3, 6]


class GroupInvestmentStart(Page):
    def is_displayed(self):
        return self.round_number == Constants.individual_rounds + 1
    def vars_for_template(self):
        return {
            'group_round': self.round_number - Constants.individual_rounds,
        }

class GroupInvestmentStart2(Page):
    def is_displayed(self):
        return self.round_number == Constants.individual_rounds + 1
    def vars_for_template(self):
        return {
            'group_round': self.round_number - Constants.individual_rounds,
        }


class GroupInvestmentStart4(Page):
    def is_displayed(self):
        return self.round_number == Constants.individual_rounds + 1
    def vars_for_template(self):
        return {
            'group_round': self.round_number - Constants.individual_rounds,
            'page_type': 'start' if self.round_number == Constants.individual_rounds + 1 else 'instructions'

        }

class GroupWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.individual_rounds + 1

    def after_all_players_arrive(self):
        pass



class GroupInvestmentPage(Page):
    form_model = 'group'
    form_fields = ['group_investment']

    def vars_for_template(self):
        if self.group.field_maybe_none('success_number_group') is None:
            self.group.success_number_group = random.randint(1, 6)
            for p in self.group.get_players():
                p.success_number_group = self.group.success_number_group

        return {
            'success_number': self.group.success_number_group,
            'partner_id': self.player.get_others_in_group()[0].id_in_group,
            'group_round': self.round_number - Constants.individual_rounds,
            'total_group_rounds': Constants.group_rounds,
            'group_investment': self.group.field_maybe_none('group_investment') or 0,
            'conversation_history': self.group.conversation_history

        }

    @staticmethod
    def live_method(player, data):
        group = player.group
        players = group.get_players()
        round_count = group.field_maybe_none('round_count') or 0

        if data['type'] == 'propose':
            player.investment_amount = float(data['amount'])

            if all(p.field_maybe_none('investment_amount') is not None for p in players):
                round_count += 1
                group.round_count = round_count

                # Check if proposals match
                if players[0].investment_amount == players[1].investment_amount:
                    group.group_investment = players[0].investment_amount
                    group.investment_agreed = True
                    return {0: {'type': 'round_result', 'round': round_count, 'match': True,
                                'amount': group.group_investment,'history': group.conversation_history}}
                else:
                    # Reset proposals for next round
                    for p in players:
                        p.investment_amount = None

                    if round_count > 3:  # Changed from >= 4 to > 3
                        default_options = [0, 0.5, 1, 1.5, 2]
                        group.group_investment = random.choice(default_options)
                        group.investment_agreed = True
                        return {0: {'type': 'round_result', 'round': round_count, 'match': False,
                                    'amount': group.group_investment, 'history': group.conversation_history}}
                    else:
                        return {0: {'type': 'round_result', 'round': round_count, 'match': False, 'history': group.conversation_history}}

        return {player.id_in_group: {'type': 'wait'}}

    def is_displayed(self):
        return (5 <= self.round_number <= 8)

    def before_next_page(self):
        if not self.group.field_maybe_none('investment_agreed'):
            default_options = [0, 0.5, 1, 1.5, 2]
            self.group.group_investment = random.choice(default_options)
            self.group.investment_agreed = True

        for p in self.group.get_players():
            p.investment_amount = self.group.group_investment

    def error_message(self, values):
        if not self.group.field_maybe_none('investment_agreed'):
            return "You must reach an agreement before proceeding."


class GroupInvestmentWaitPage(WaitPage):
    def is_displayed(self):
        return (5 <= self.round_number <= 8)

    def after_all_players_arrive(self):
        if all(p.agreed_on_investment for p in self.group.get_players()):
            self.group.investment_agreed = True
            self.group.group_investment = self.group.get_players()[0].investment_amount
        else:
            self.group.investment_agreed = False
            self.group.group_investment = self.group.field_maybe_none('group_investment') or 0

        print(f"After wait page: Group investment set to: {self.group.group_investment} puntos")

class GroupDiceRollingPage(Page):
    def is_displayed(self):
        return (5 <= self.round_number <= 8)

    def vars_for_template(self):
        if self.group.field_maybe_none('dice_roll') is None:
            self.group.dice_roll = random.randint(1, 6)

        self.group.success = self.group.dice_roll == self.group.success_number_group
        group_investment = self.group.field_maybe_none('group_investment')
        if group_investment is not None:
            if self.group.success:
                self.group.group_earnings = group_investment * 6
            else:
                self.group.group_earnings = group_investment * -1
        else:
            self.group.group_earnings = 0

        return {
            'dice_roll': self.group.dice_roll,
            'success_number': self.group.success_number_group,
            'group_round': self.round_number - Constants.individual_rounds,
            'total_group_rounds': Constants.group_rounds,
            'group_investment': group_investment
        }


class GroupResultsPage(Page):
    def is_displayed(self):
        return (5 <= self.round_number <= 8)

    def vars_for_template(self):
        group_investment = self.group.group_investment
        if group_investment is None:
            group_investment = 0
        print(f"Group investment retrieved: {group_investment} ")

        if self.group.field_maybe_none('dice_roll') is None:
            self.group.dice_roll = random.randint(1, 6)

        success = self.group.dice_roll == self.group.success_number_group
        self.group.success = success
        print(f"Dice roll: {self.group.dice_roll}, Success number: {self.group.success_number_group}")
        print(f"Success determined: {success}")

        if success:
            group_earnings = 6 * group_investment
        else:
            group_earnings = -1 * group_investment

        self.group.group_earnings = group_earnings
        print(f"Group earnings calculated: {group_earnings} ")

        # Save the 4th round earnings
        if self.round_number == Constants.individual_rounds + 4:  # Assuming 4 group rounds
            self.group.fourth_round_earnings = group_earnings

        individual_earnings = group_earnings // Constants.players_per_group
        for p in self.group.get_players():
            p.earnings = individual_earnings
            p.participant.payoff += individual_earnings
        print(f"Individual earnings calculated: {individual_earnings} ")

        return {
            'group_investment': group_investment,
            'dice_roll': self.group.dice_roll,
            'success_number': self.group.success_number_group,
            'success': success,
            'group_earnings': group_earnings,
            'individual_earnings': individual_earnings,
            'group_round': self.round_number - Constants.individual_rounds,
            'total_group_rounds': Constants.group_rounds
        }
class FourthRoundSummary(Page):
    def is_displayed(self):
        return (self.round_number == 4) or (self.round_number == 12)
    def vars_for_template(self):
        return {
            'fourth_round_earnings': self.group.fourth_round_earnings,
        }

class GroupEndSlide(Page):
    def is_displayed(self):
        return self.round_number == 8

    def vars_for_template(self):
        fourth_round = self.group.in_round(Constants.individual_rounds + 4)
        fourth_round_earnings = fourth_round.group_earnings if fourth_round.group_earnings is not None else 0
        individual_earnings = fourth_round_earnings / Constants.players_per_group

        return {
            'fourth_round_earnings': round(fourth_round_earnings, 2),
            'individual_earnings': round(individual_earnings, 2)
        }


class GroupInvestmentSummary(Page):
    form_model = 'player'
    form_fields = ['close_field']

    def is_displayed(self):
        return self.round_number == 8

    def vars_for_template(self):
        group_rounds = self.player.in_rounds(Constants.individual_rounds + 1, Constants.num_rounds)
        total_group_earnings = sum(p.group.group_earnings for p in group_rounds if p.group.field_maybe_none('group_earnings') is not None)
        total_earnings = sum(p.earnings for p in self.player.in_all_rounds() if p.field_maybe_none('earnings') is not None)

        return {
            'group_rounds': group_rounds,
            'total_group_earnings': total_group_earnings,
            'group_earnings': total_group_earnings,  # Add this line
            'final_earnings': self.participant.payoff
        }

class SurveyIntroduc(Page):
    template_name = 'investment_game/SurveyIntroduc.html'

    def is_displayed(self):
        return self.round_number == 12
class TotalEarningsSummary(Page):
    form_model = 'player'
    form_fields = ['continue_field']

    def is_displayed(self):
        return self.round_number == Constants.individual_rounds

    def vars_for_template(self):
        previous_rounds = self.player.in_all_rounds()[:Constants.individual_rounds]
        return {
            'total_earnings': self.participant.vars['total_earnings'],
            'previous_rounds': previous_rounds,
            'phase': 'Individual' if self.round_number <= Constants.individual_rounds else 'Group',
        }

    def error_message(self, values):
        if values['continue_field'].lower() != 'close':
            return 'Please type "close" in the box below to finalize your investment earnings.'


class SurveyPage(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'major']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class PauseSlide(Page):
    form_model = 'player'
    form_fields = ['close_field']

    def is_displayed(self):
        return (self.round_number == 3) or (self.round_number == 11)

    def vars_for_template(self):
        if self.round_number == 3:
            total_earnings = sum([p.earnings for p in self.player.in_rounds(1, 3)])
            rounds = self.player.in_rounds(1, 3)

        elif self.round_number == 11:
            total_earnings = sum([p.earnings for p in self.player.in_rounds(9, 11)])
            rounds = self.player.in_rounds(9, 11)
        else:
            phase = "Group"
            rounds = self.player.in_rounds(Constants.individual_rounds + 1, Constants.individual_rounds + 3)

        rounds_data = []
        total_earnings = 0
        for r in rounds:
            investment = r.field_maybe_none('investment')
            success = r.field_maybe_none('success')
            earnings = r.field_maybe_none('earnings')
            total_earnings += earnings if earnings is not None else 0
            rounds_data.append({
                'round_number': r.round_number,
                'investment': investment,
                'success': success,
                'earnings': earnings
            })

        return {
            'total_earnings': total_earnings,
            'rounds': rounds_data
        }

    def error_message(self, values):
        if values['close_field'].lower() != 'close':
            return 'Please type "close" in the box below to finalize your investment earnings.'


class GroupPauseSlide(Page):
    form_model = 'player'
    form_fields = ['close_field']

    def is_displayed(self):
        return self.round_number == 7

    def vars_for_template(self):
        phase = "Group"
        rounds = self.player.in_rounds(Constants.individual_rounds + 1, Constants.individual_rounds + 3)

        rounds_data = []
        total_earnings = 0
        for r in rounds:
            group_investment = r.group.field_maybe_none('group_investment')
            success = r.group.field_maybe_none('success')
            group_earnings = r.group.field_maybe_none('group_earnings')
            individual_earnings = r.field_maybe_none('earnings')
            total_earnings += group_earnings if group_earnings is not None else 0  # Accumulate group earnings
            rounds_data.append({
                'round_number': r.round_number - Constants.individual_rounds,
                'group_investment': group_investment,
                'success': success,
                'group_earnings': group_earnings,
                'individual_earnings': individual_earnings
            })

        return {
            'phase': phase,
            'total_earnings': total_earnings,
            'rounds': rounds_data
        }

    def error_message(self, values):
        if values['close_field'].lower() != 'close':
            return 'Please type "close" in the box below to finalize your investment earnings.'


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age_check', 'gender', 'career', 'native_language', 'university_year', 'gpa', 'smoker', 'alcohol', 'drugs', 'weekly_spending']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['crt_linda', 'crt_bat', 'crt_widget', 'crt_lake', 'crt_double']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class FinancialLiteracy(Page):
    form_model = 'player'
    form_fields = ['fin_change', 'fin_lottery', 'fin_sale', 'fin_disease', 'fin_cardealer', 'fin_interest']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class RiskAttitudes(Page):
    form_model = 'player'
    form_fields = ['risk_general', 'risk_driving', 'risk_career', 'risk_health']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class DecisionMakingScenarios(Page):
    form_model = 'player'
    form_fields = ['scenario_jar', 'monty_hall']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds



class EndPage(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        self.player.exit_survey_completed = True
    pass



class GroupInvestmentSummary(Page):
    def is_displayed(self):
        return self.round_number == 8

    def vars_for_template(self):
        group_rounds = self.player.in_rounds(Constants.individual_rounds + 1, Constants.num_rounds)
        total_group_earnings = sum(p.group.group_earnings for p in group_rounds if p.group.field_maybe_none('group_earnings') is not None)
        total_earnings = sum(p.earnings for p in self.player.in_all_rounds() if p.field_maybe_none('earnings') is not None)

        return {
            'group_rounds': group_rounds,
            'total_group_earnings': total_group_earnings,
            'group_earnings': total_group_earnings,  # Add this line
            'final_earnings': self.participant.payoff
        }

class SecondIndivid(Page):
    def is_displayed(self):
            return self.round_number == 8



page_sequence = [
    WelcomeStructure,
    HowToWin,
    example,
    InvestmentPage,
    DiceRollingPage,
    ResultsPage,
    PauseSlide,
    EndSlide,
    Countdown,
    GroupInvestmentStart,
    GroupInvestmentStart2,
    GroupInvestmentStart4,
    GroupInvestmentWaitPage,

    GroupInvestmentPage,
    GroupInvestmentWaitPage,
    GroupDiceRollingPage,
    GroupResultsPage,
    GroupInvestmentWaitPage,
    GroupPauseSlide,
    GroupEndSlide,

    Countdown_2,
    SecondIndivid,
    SurveyIntroduc,
    Demographics,
    CognitiveReflectionTest,
    FinancialLiteracy,
    RiskAttitudes,
    DecisionMakingScenarios,
    EndPage
]
