
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

SNS_STYLE = {
    'axes.axisbelow': True,
    'axes.edgecolor': '.4',
    'axes.facecolor': 'white',
    'axes.grid': False,
    'axes.labelcolor': '.20',
    'axes.spines.bottom': True,
    'axes.spines.left': True,
    'axes.spines.right': False,
    'axes.spines.top': False,
    'figure.facecolor': 'white',
    'font.family': ['sans-serif'],
    'font.sans-serif': ['Arial',
    'DejaVu Sans',
    'Liberation Sans',
    'Bitstream Vera Sans',
    'sans-serif'],
    'grid.color': '.10',
    'grid.linestyle': '-',
    'image.cmap': 'rocket',
    'lines.solid_capstyle': 'round',
    'patch.edgecolor': 'r',
    'patch.force_edgecolor': True,
    'text.color': '.15',
    'xtick.bottom': False,
    'xtick.color': '.15',
    'xtick.direction': 'out',
    'xtick.top': False,
    'ytick.color': '.15',
    'ytick.direction': 'out',
    'ytick.left': False,
    'ytick.right': False
}

def sns_init():
    sns.set_style("darkgrid", SNS_STYLE)
    

def hist(d,des = 'hist.jpg', lb = ''):
    plt.figure()
    sns.distplot(d, hist=False, color="r", kde_kws={"shade": True}, label = lb).figure.savefig(des)
    
def simpleTable(l):
    df = pd.DataFrame(l,columns = ['property','value'])
    return df
# ref https://thispointer.com/python-pandas-how-to-convert-lists-to-a-dataframe/

def data_display(d):
    print('max:')
    print(max(d))
    print('zeros in data:')
    print(d.count(0))
    sns.set_style('darkgrid')
    return sns.distplot(d)

def line_plot(x,y,x_label = 'x', y_label ='y'):
    plt.plot(x,y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    return plt.show()

def data_display(d):
    print('max: %d' % max(d))
    print('var: %f' % np.var(d))
    print('zeros in data: %d' % d.count(0))
    d = pd.Series(d, name="oligo_num")
    sns.set_style('darkgrid')
    return sns.distplot(d,bins = 80)

def jointplot():
    x, y = np.random.multivariate_normal([1,2], [[1,2],[1,2]], 1000).T
    with sns.axes_style("white"):
        return sns.jointplot(x=x, y=y, kind="hex", color="k")