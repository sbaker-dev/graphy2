import numpy as np
from graphy2 import pd


class Data:
    def __init__(self, data, rounding=3):
        self._data = data
        self._round = rounding

    # todo rounding needs to be exposed as a style set
    def odds_ratio(self, case_control_totals=True, sub_grouping=None):
        """
        calculates the Odds ratio with a confidence internal

        Further information
        ----------------------
        There are two core formats of case-control and cohort study's. In the former the only viable option is an odd's
        ratio. However, regardless of type the data can take to core types.

        In the event-total we have          event-case[1], total-case[2],     event-control[3], total-control[4]
        In the event-none-event we have     event-case[1], non-event-case[2], event-control[3], non-event-control[4]

        In a case control manner the total isn't the same total when looking at a cohort study. But for odds we want the
        2nd case outcome, so if presented the first case these columns need to be calculated and indexes re-cast to be
        the new generated columns

        In the first case we need to calculate non-event case nad control from the total whilst in the second we are
        good to go.

        This assumes a event-case[1], total-case[2], event-control[3], total-control[4], style of data frame with
        variable_name[data frame index] formatting, with the study name as the first positional column. As such to
        calculate the odds we need the following formula

        Odds_ratio = event-case[1]      * (total-control[4] - event-control[3]) /
                     event-control[3]   * (total-case[2]    - event-case[1])

        Odds ratio's are not normally distributed, so we need to take the natural log of the odds ratio to compute the
        confidence limits on a logarithmic scale, then convert them back.

        Odds ratio Confidence internal = e^(log(OR)+-[1.96*SE(log(OR))])
        Log Odds ratio standard errors = sqrt(1/[1] + 1/[2] + 1/[3] + 1/[4])

        Source: "http://sphweb.bumc.bu.edu/otlt/MPH-Modules/PH717-QuantCore/PH717_ComparingFrequencies/
                 PH717_ComparingFrequencies8.html"

        :key case_control_totals: The data has case-exposure, control-exposure and the total number of cases and
            controls if true. If false, then the data has case/control-exposure case/control-non_exposure.
        :type case_control_totals: bool

        :param sub_grouping: A list, or list of lists, that represents sub groups. Each sub group list takes the form
            of [start_index, end_index, name]. Can also be None if no sub grouping is present
        :type sub_grouping: list[int, int, str] | list[list[int, int, str]] | None

        :return: The summary input + the new dataframe
        """
        # todo, take a list that is the sub-group (use the sub group with the 2nd type of binary data)
        # todo append rows for groups and for totals

        # Creates Order of "Trail", "Event Cases", "Non-event Case", "Total Cases", "Event Control", "Non-event Control"
        # "Total Controls", "Study Total"
        self._non_event_totals(case_control_totals)
        odds = pd.DataFrame(self._compute_odds())
        confidence_interval = pd.DataFrame(self._odds_confidence_interval())
        self._relative_weights()



        return pd.concat([df, self._data["N"], self._data["Odds Ratio(95% CI)"], self._data["Relative Weight"]], axis=1,
                         join="outer")

    def _non_event_totals(self, case_control_totals):
        if case_control_totals:
            # Then calculate the non_event case/control and set index to these new columns
            self._data["non_event_case"] = self._data.iloc[:, 2] - self._data.iloc[:, 1]
            self._data["non_event_control"] = self._data.iloc[:, 4] - self._data.iloc[:, 3]
            self._data["Study_total"] = self._data.iloc[:, 2] + self._data.iloc[:, 4]
            self._data.columns = ["Trail", "Event Cases", "Total Cases", "Event Control", "Total Controls",
                                  "Non-event Case", "Non-event Control", "Study Total"]

        else:
            # Calculate the totals for cases and controls and set indexes accordingly
            self._data["case_total"] = self._data.iloc[:, 1] + self._data.iloc[:, 2]
            self._data["control_totals"] = self._data.iloc[:, 3] + self._data.iloc[:, 4]
            self._data["Study_total"] = self._data.iloc[:, 5] + self._data.iloc[:, 6]
            self._data.columns = ["Trail", "Event Cases", "Non-event Case", "Event Control", "Non-event Control",
                                  "Total Cases", "Total Controls", "Study Total"]

        self._data = self._data[["Trail", "Event Cases", "Non-event Case", "Total Cases", "Event Control",
                                 "Non-event Control", "Total Controls", "Study Total"]]

    def _compute_odds(self):
        return round((self._data["Event Cases"] * self._data["Non-event Control"]) /
                     (self._data["Event Control"] * self._data["Non-event Case"]), self._round)

    def _log_odds_standard_error(self):
        return round(np.sqrt((1 / self._data.iloc[:, 1]) + (1 / self._data.iloc[:, 2]) +
                             (1 / self._data.iloc[:, 4]) + (1 / self._data.iloc[:, 5])), self._round)

    def _odds_confidence_interval(self):
        odds = self._compute_odds()
        se = self._log_odds_standard_error()
        upper = np.exp(np.log(odds) + (1.96 * se))
        lower = np.exp(np.log(odds) - (1.96 * se))

        return [f"{odd}[{round(low, self._round)}-{round(high, self._round)}]" for odd, low, high in
                zip(odds, upper, lower)]

    def _relative_weights(self):
        weight = (2 * (self._data["Study Total"] * self._data["Study Total"])) * (self._data["Study Total"] * 2) / \
                 (self._data["Study Total"] * self._data["Study Total"] * np.square(self._compute_odds()))

        return round(weight / weight.sum(), self._round)

    def relative_risk(self):
        pass



