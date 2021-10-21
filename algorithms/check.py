#!/usr/bin/env python
from enum import IntEnum
import numpy as np
import pandas as pd
import argparse

time_interval = 0.5
tol = 1e-7


class StatusCodes(IntEnum):
    """
    Status codes of battery charging action,
    0 means normal,
    1 means the charging power exceeds maximum allowed power (charging beyond capacity or higher than max power)
    2 means the discharging power exceeds maximum allowed power (discharging more energy than available or higher than max power)
    """
    NORMAL = 0
    EXCEEDING_MAX_CHARGE_POWER = 1
    EXCEEDING_MAX_DISCHARGE_POWER = 2


class Battery:
    battery_power = 300.0
    battery_capacity = 580.0
    charge_efficiency = 0.9
    discharge_efficiency = 0.9
    marginal_loss_factor = 0.991
    fixed_oNm = 8.1
    variable_oNm = 0

    def __init__(self, initial_capacity=0):
        """
        Create a battery with specific initial capacity
        :param initial_capacity: The power the battery starts with
        """
        assert 0 <= initial_capacity <= self.battery_capacity, "Enter valid initial capacity!"
        self.capacity = initial_capacity
        self.max_charge = -min(self.battery_power, (self.battery_capacity - self.capacity) / self.charge_efficiency / time_interval)
        self.max_discharge = min(self.battery_power, self.capacity / time_interval)

    def charge(self, power, spot_price=None):
        """
        Charge the battery with specific power, and output the status codes of this action (revenue as well if
        spot price is provided)
        :param power: The power to charge the battery (positive: discharge, negative: charge)
        :param spot_price: Current electricity price
        :return: Tuple of (Status code, revenue)
        """
        flag = StatusCodes.NORMAL
        # Only treat spot price as 0 if not provided
        if spot_price is None:
            spot_price = 0
        revenue = 0

        # Check for possible errors and assign error codes
        if power < self.max_charge - tol:
            flag = StatusCodes.EXCEEDING_MAX_CHARGE_POWER
            power = self.max_charge
        elif power > self.max_discharge + tol:
            flag = StatusCodes.EXCEEDING_MAX_DISCHARGE_POWER
            power = self.max_discharge

        # Charge/discharge battery, clip the value to avoid rounding error
        power = np.clip(power, self.max_charge, self.max_discharge)
        if power < 0:
            market_dispatch = power * time_interval
            self.capacity -= market_dispatch * self.charge_efficiency
            revenue = spot_price * market_dispatch / self.marginal_loss_factor
        if power > 0:
            market_dispatch = power * time_interval * self.discharge_efficiency
            self.capacity -= market_dispatch / self.discharge_efficiency
            revenue = spot_price * market_dispatch * self.marginal_loss_factor

        # Recompute the thresholds
        self.max_charge = -min(self.battery_power, (self.battery_capacity - self.capacity) / self.charge_efficiency / time_interval)
        self.max_discharge = min(self.battery_power, self.capacity / time_interval)
        return flag, revenue


def check_submission(df, spot_prices=None, include_capacity=False, include_revenue=False):
    initial_charge = df.loc[0, "capacity"]
    battery = Battery(initial_charge)
    flags = []
    capacities = []
    revenues = []
    for idx, (datetime, power, capacity) in df.iterrows():
        spot_price = 0 if spot_prices is None else spot_prices[idx]
        if include_capacity:
            capacities.append(battery.capacity)
        flag, revenue = battery.charge(power, spot_price)
        flags.append(flag)
        revenues.append(revenue)
    results = pd.DataFrame({"datetime": df.datetime, "flag": flags})
    if include_capacity: results["capacity"] = capacities
    if include_revenue: results["revenue"] = revenues
    return results


parser = argparse.ArgumentParser(description="Check MAST30034 Battery project submission file."
                                             " In the flag column of the output file: 0 stands for normal."
                                             " 1 means the charging power is above the limit."
                                             " 2 means the discharging power is above the limit.")
parser.add_argument("--submission", metavar="IN", type=pd.read_csv, nargs=1, required=True,
                    help="Path to the submission file to be checked.")
# Waiting for full release when this is available.
# parser.add_argument("--market", metavar="M", type=pd.read_excel, nargs=1, required=False, default=None,
#                     help="Path to the market data file to compute revenue.")
parser.add_argument("--result", metavar="OUT", type=str, nargs=1, required=True,
                    help="Path where the output file should be stored.")


# Execute the codes only if this file is run as main.
if __name__ == "__main__":
    args = parser.parse_args()
    submission = args.submission[0]
    # market_data = args.market
    # if market_data is not None:
    #     spot_prices = market_data["Regions VIC Trading Price ($/MWh)"]
    spot_prices = None
    results = check_submission(submission, spot_prices=spot_prices, include_revenue=spot_prices is not None)
