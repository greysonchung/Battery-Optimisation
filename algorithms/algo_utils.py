import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg')

def plot_actions(spot_price, action, closing_capacity=None, start=0, end=-1):
    """
    Notes: Plot where the algorithm charges and discharges
    ----------
    Parameters
    ----------
    spot_price       : dataframe with spot_price & forecast columns
    action           : discharge if value > 0, charge if value < 0
    closing_capacity : plot closing capacity if provided
    start            : start index (default=0)
    end              : end index (default=300)
    
    Returns
    -------
    plot with discharge and charge verticle lines
    """
    
    def legend_without_duplicate_labels(ax):
        handles, labels = ax.get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        ax.legend(*zip(*unique), fontsize=10)
        
    spot_price = pd.Series(spot_price)
    if closing_capacity is not None:
        closing_capacity = pd.Series(closing_capacity)
        fig, axs = plt.subplots(2, 1, figsize=(14,5), gridspec_kw={'height_ratios': [3, 1]})
        axs[0].plot(spot_price[start:end], label='Spot Price')
        axs[0].set_ylabel('Spot Price (AUD)', fontsize=10)
        lw=1.5
        for xc in spot_price.index[start:end]:
            if action[xc] > 0:
                axs[0].axvline(x=xc, c='red', linestyle='dotted', label='Discharge', lw=lw)
                axs[1].axvline(x=xc, c='red', linestyle='dotted', lw=lw)
            elif action[xc] < 0:
                axs[0].axvline(x=xc, c='green', label='Charge', lw=lw)
                axs[1].axvline(x=xc, c='green', lw=lw)
        legend_without_duplicate_labels(axs[0])
        axs[0].set_xlim(spot_price.index[start], spot_price.index[end])
        capacity = closing_capacity[start:end]
        pos = capacity - capacity.shift(1) > 0
        neg = capacity - capacity.shift(1) < 0
        axs[1].bar(capacity.index[pos],capacity[pos],color='green', align='center')
        axs[1].bar(capacity.index[neg],capacity[neg],color='red', align='center')
        axs[1].set_ylabel('Capacity (MWh)', fontsize=10)
        axs[1].set_xlim(closing_capacity.index[start], closing_capacity.index[end])
        
    else:
        fig, ax = plt.subplots(figsize=(11,3))
        plt.plot(spot_price[start:end])
        plt.ylabel('Spot Price', fontsize=10)
        plt.xlabel('Datetime', fontsize=10)
        for xc in spot_price.index[start:end]:
            if action[xc] > 0:
                ax.axvline(x=xc, c='red', linestyle='dotted', label='discharge')
            elif action[xc] < 0:
                ax.axvline(x=xc, c='green', linestyle='dotted', label='charge')
        legend_without_duplicate_labels(ax)
    plt.tight_layout()    
    
    return plt.show()