import matplotlib as mpl
import numpy as np
import pickle


mpl.rcParams.update({
    'font.family': 'normal',
    'font.serif': [],
    'font.sans-serif': [],
    'font.monospace': [],
    'font.size': 12,
    'text.usetex': False,
})


import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns

sns.set_context('paper', font_scale=2.5)
sns.set_style('white')
sns.mpl.rcParams['legend.frameon'] = 'False'


def plot_check(data, name, r_list=None, s_list=None, fpath=None):
    colors = ['#1144AA', '#00B454', '#FFF800', '#FFB300', '#CE0071']
    marker = ['o', 's', '*', 'D', 'p']

    r_list = r_list or list(data.keys())
    s_list = s_list or list(data[r_list[0]].keys())

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    plt.subplots_adjust(wspace=0.3)

    ax1.set_title('ALS')
    ax1.set_xlabel('Number of iterations')
    ax1.set_ylabel('Error')

    ax2.set_title('ANOVA-ALS')
    ax2.set_xlabel('Number of iterations')
    ax2.set_ylabel('Error')

    if name == 'Dixon':
        ax1.set_ylim(6.E-10, 2.E+1)
        ax2.set_ylim(6.E-10, 2.E+1)
    elif name == 'Piston':
        ax1.set_ylim(1.E-3, 3.E+0)
        ax2.set_ylim(1.E-3, 3.E+0)
    elif name == 'PDE-VOI':
        ax1.set_ylim(5.E-6, 3.E+0)
        ax2.set_ylim(5.E-6, 3.E+0)

    for i, r in enumerate(r_list):
        label = f'r = {r}'

        e_als_rnd = [data[r][s]['e_als_rnd'] for s in s_list]
        e_als_rnd_avg = []
        e_als_rnd_min = []
        e_als_rnd_max = []
        for e in e_als_rnd:
            e = np.array(e)
            e_als_rnd_avg.append(np.mean(e))
            e_als_rnd_min.append(np.min(e))
            e_als_rnd_max.append(np.max(e))

            if False:
                from scipy.stats import t as stats
                k = len(e)
                m = np.mean(e)
                v = np.mean(e**2) - np.mean(e)**2
                e1 = np.sqrt(v/k) * stats.interval(0.95, k)[0]
                e2 = np.sqrt(v/k) * stats.interval(0.95, k)[1]
                e_als_rnd_min.append(m - e1)
                e_als_rnd_max.append(m - e2)

        if False:
            e_als_rnd_var = [np.quantile(e, 0.95) for e in e_als_rnd]
            e_als_rnd_min = np.array(e_als_rnd_avg) - np.array(e_als_rnd_var)
            e_als_rnd_max = np.array(e_als_rnd_avg) + np.array(e_als_rnd_var)

        ax1.plot(s_list, e_als_rnd_avg, label=label,
            marker=marker[i], markersize=8, linewidth=3, color=colors[i])
        ax1.fill_between(s_list, e_als_rnd_min, e_als_rnd_max,
            alpha=0.2, color=colors[i])

        e_als_ano = [data[r][s]['e_als_ano'] for s in s_list]

        ax2.plot(s_list, e_als_ano, label=label,
            marker=marker[i], markersize=8, linewidth=3, color=colors[i])

    prep_ax(ax1, xlog=True, ylog=True, leg=True)
    prep_ax(ax2, xlog=True, ylog=True)

    if fpath:
        plt.savefig(fpath, bbox_inches='tight')
    else:
        plt.show()


def plot_check_big(data, r_list, s_list, fpath=None):
    colors = ['#00B454', '#FFF800', '#FFB300']
    marker = ['s', '*', 'D']

    fig, axs = plt.subplots(1, 3, figsize=(24, 8))
    plt.subplots_adjust(wspace=0.3)

    for ax, (name, res) in zip(axs, data.items()):
        ax.set_xlabel('Number of iterations')
        ax.set_ylabel('Error')
        ax.set_title(f'ANOVA-ALS for {name}')

        for i, r in enumerate(r_list):
            label = f'r = {r}'

            e_als_ano = [res[r][s]['e_als_ano'] for s in s_list]

            ax.plot(s_list, e_als_ano, label=label,
                marker=marker[i], markersize=8, linewidth=3, color=colors[i])

        prep_ax(ax, xlog=True, ylog=True, leg=True)

    if fpath:
        plt.savefig(fpath, bbox_inches='tight')
    else:
        plt.show()


def prep_ax(ax, xlog=False, ylog=False, leg=False, xint=False, xticks=None):
    if xlog:
        ax.semilogx()
    if ylog:
        ax.semilogy()

    if leg:
        ax.legend(loc='best', frameon=True)

    ax.grid(ls=":")

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    if xint:
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    if xticks is not None:
        ax.set(xticks=xticks, xticklabels=xticks)
