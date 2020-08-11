import numpy as np
from graphy2 import pd


class Data:
    def __init__(self, data, rounding=3, case_control_totals=True):
        self._data = data
        self._round = rounding
        self.case_control_totals = case_control_totals

    def construct_odds_table(self):
        """
        Format the odd's into a table format

        :return: Odd's table
        """

        Data(self._data).non_event_totals()

        plotting = [pd.DataFrame(self.confidence_interval(upper=False)), pd.DataFrame(self.confidence_interval()),
                    self._compute_odds(), self._relative_weights()]

        reduced = [self._data.iloc[:, 0], pd.DataFrame(self.format_events()), pd.DataFrame(self.format_events("Controls")),
                   pd.DataFrame(self._odds_confidence_interval()), pd.DataFrame(self._relative_weights())]

        table_data = pd.concat(reduced, axis=1)
        table_data.columns = ["Study", "Case (n/N)", "Control (n/N)", "OR (95% CI)", "Weight"]
        plot_data = pd.concat(plotting, axis=1)
        plot_data.columns = ["Lower", "Upper", "Odds", "Relative Weight"]
        return table_data, plot_data

    def non_event_totals(self):
        if self.case_control_totals:
            # Then calculate the non_event case/control and set index to these new columns
            self._data["non_event_case"] = self._data.iloc[:, 2] - self._data.iloc[:, 1]
            self._data["non_event_control"] = self._data.iloc[:, 4] - self._data.iloc[:, 3]
            self._data["Study_total"] = self._data.iloc[:, 2] + self._data.iloc[:, 4]
            self._data.columns = ["Trail", "Event Cases", "Total Cases", "Event Controls", "Total Controls",
                                  "Non-event Cases", "Non-event Controls", "Study Total"]

        else:
            # Calculate the totals for cases and controls and set indexes accordingly
            self._data["case_total"] = self._data.iloc[:, 1] + self._data.iloc[:, 2]
            self._data["control_totals"] = self._data.iloc[:, 3] + self._data.iloc[:, 4]
            self._data["Study_total"] = self._data.iloc[:, 5] + self._data.iloc[:, 6]
            self._data.columns = ["Trail", "Event Cases", "Non-event Cases", "Event Controls", "Non-event Controls",
                                  "Total Cases", "Total Controls", "Study Total"]

        self._data = self._data[["Trail", "Event Cases", "Non-event Cases", "Total Cases", "Event Controls",
                                 "Non-event Controls", "Total Controls", "Study Total"]]

    def _compute_odds(self):
        return round((self._data["Event Cases"] * self._data["Non-event Controls"]) /
                     (self._data["Event Controls"] * self._data["Non-event Cases"]), self._round)

    def _log_odds_standard_error(self):
        return round(np.sqrt((1 / self._data.iloc[:, 1]) + (1 / self._data.iloc[:, 2]) +
                             (1 / self._data.iloc[:, 4]) + (1 / self._data.iloc[:, 5])), self._round)

    def confidence_interval(self, upper=True):
        if upper:
            return np.exp(np.log(self._compute_odds()) + (1.96 * self._log_odds_standard_error()))
        else:
            return np.exp(np.log(self._compute_odds()) - (1.96 * self._log_odds_standard_error()))

    def _odds_confidence_interval(self):
        return [f"{odd}[{round(low, self._round)}-{round(high, self._round)}]" for odd, low, high in
                zip(self._compute_odds(), self.confidence_interval(upper=False), self.confidence_interval())]

    def _relative_weights(self):
        weight = (2 * (self._data["Study Total"] * self._data["Study Total"])) * (self._data["Study Total"] * 2) / \
                 (self._data["Study Total"] * self._data["Study Total"] * np.square(self._compute_odds()))

        return round(weight / weight.sum(), self._round)

    def format_events(self, case_control="Cases"):
        return [f"{c}/{t}" for c, t in zip(self._data[f"Event {case_control}"], self._data[f"Total {case_control}"])]

        # return self._data[f"Event {case_control}"].str.cat(self._data[f"Total {case_control}"], sep="/")

    # df["treat_nums"] = df["deaths_plasma"].str.cat(df["total_cases"], sep="/")
    # df["control_nums"] = df["deaths_control"].str.cat(df["total_control"], sep="/")

    def relative_risk(self):
        pass


    # # todo rounding needs to be exposed as a style set
    # def odds_ratio(self, sub_grouping=None):
    #     """
    #     calculates the Odds ratio with a confidence internal
    #
    #     Further information
    #     ----------------------
    #     There are two core formats of case-control and cohort study's. In the former the only viable option is an odd's
    #     ratio. However, regardless of type the data can take to core types.
    #
    #     In the event-total we have          event-case[1], total-case[2],     event-control[3], total-control[4]
    #     In the event-none-event we have     event-case[1], non-event-case[2], event-control[3], non-event-control[4]
    #
    #     In a case control manner the total isn't the same total when looking at a cohort study. But for odds we want the
    #     2nd case outcome, so if presented the first case these columns need to be calculated and indexes re-cast to be
    #     the new generated columns
    #
    #     In the first case we need to calculate non-event case nad control from the total whilst in the second we are
    #     good to go.
    #
    #     This assumes a event-case[1], total-case[2], event-control[3], total-control[4], style of data frame with
    #     variable_name[data frame index] formatting, with the study name as the first positional column. As such to
    #     calculate the odds we need the following formula
    #
    #     Odds_ratio = event-case[1]      * (total-control[4] - event-control[3]) /
    #                  event-control[3]   * (total-case[2]    - event-case[1])
    #
    #     Odds ratio's are not normally distributed, so we need to take the natural log of the odds ratio to compute the
    #     confidence limits on a logarithmic scale, then convert them back.
    #
    #     Odds ratio Confidence internal = e^(log(OR)+-[1.96*SE(log(OR))])
    #     Log Odds ratio standard errors = sqrt(1/[1] + 1/[2] + 1/[3] + 1/[4])
    #
    #     Source: "http://sphweb.bumc.bu.edu/otlt/MPH-Modules/PH717-QuantCore/PH717_ComparingFrequencies/
    #              PH717_ComparingFrequencies8.html"
    #
    #     :key case_control_totals: The data has case-exposure, control-exposure and the total number of cases and
    #         controls if true. If false, then the data has case/control-exposure case/control-non_exposure.
    #     :type case_control_totals: bool
    #
    #     :param sub_grouping: A list, or list of lists, that represents sub groups. Each sub group list takes the form
    #         of [start_index, end_index, name]. Can also be None if no sub grouping is present
    #     :type sub_grouping: list[int, int, str] | list[list[int, int, str]] | None
    #
    #     :return: The summary input + the new dataframe
    #     """
    #     # todo, take a list that is the sub-group (use the sub group with the 2nd type of binary data)


