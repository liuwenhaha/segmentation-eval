# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 16:15:51 2017

@author: Raluca Sandu
"""
import os
import utils.graphing as gh
import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np
import matplotlib.font_manager as font_manager

np.seterr(divide='ignore', invalid='ignore')
plt.style.use('ggplot')


# %%

def plotHistDistances(pat_name, lesion_id, rootdir, distanceMap, num_voxels, title, ablation_date):
    # PLOT THE HISTOGRAM FOR THE MAUERER EUCLIDIAN DISTANCES
    lesion_id_str = str(lesion_id)
    lesion_id = lesion_id_str.split('.')[0]
    figName_hist = 'Pat_' + str(pat_name) + '_Lesion' + str(lesion_id) + '_AblationDate_' + ablation_date + '_histogram'
    min_val = int(np.floor(min(distanceMap)))
    max_val = int(np.ceil(max(distanceMap)))
    fig, ax = plt.subplots(figsize=(18, 16))

    col_height, bins, patches = ax.hist(distanceMap, ec='darkgrey', bins=range(min_val - 1, max_val + 1))

    voxels_nonablated = []
    voxels_insuffablated = []
    voxels_ablated = []

    for b, p, col_val in zip(bins, patches, col_height):
        if b < 0:
            voxels_nonablated.append(col_val)
        elif 0 <= b <= 5:
            voxels_insuffablated.append(col_val)
        elif b > 5:
            voxels_ablated.append(col_val)
    # %%
    '''calculate the total percentage of surface for ablated, non-ablated, insufficiently ablated'''

    voxels_nonablated = np.asarray(voxels_nonablated)
    voxels_insuffablated = np.asarray(voxels_insuffablated)
    voxels_ablated = np.asarray(voxels_ablated)

    sum_perc_nonablated = ((voxels_nonablated / num_voxels) * 100).sum()
    sum_perc_insuffablated = ((voxels_insuffablated / num_voxels) * 100).sum()
    sum_perc_ablated = ((voxels_ablated / num_voxels) * 100).sum()
    # %%
    '''iterate through the bins to change the colors of the patches bases on the range [mm]'''
    for b, p, col_val in zip(bins, patches, col_height):
        if b < 0:
            plt.setp(p, label='Ablation Surface Margin ' + r'$x < 0$' + 'mm :' + " %.2f" % sum_perc_nonablated + '%')
        elif 0 <= b <= 5:
            plt.setp(p, 'facecolor', 'orange',
                     label='Ablation Surface Margin ' + r'$0 \leq  x \leq 5$' + 'mm: ' + "%.2f" % sum_perc_insuffablated + '%')
        elif b > 5:
            plt.setp(p, 'facecolor', 'darkgreen',
                     label='Ablation Surface Margin ' + r'$x > 5$' + 'mm: ' + " %.2f" % sum_perc_ablated + '%')
    # %%
    '''edit the axes limits and labels'''
    # csfont = {'fontname': 'Times New Roman'}
    plt.xlabel('Euclidean Distances (mm)', fontsize=30, color='black')
    plt.tick_params(labelsize=30, color='black')
    ax.tick_params(colors='black', labelsize=30)
    plt.grid(True)
    # TODO: set equal axis limits
    ax.set_xlim([-15, 15])

    # edit the y-ticks: change to percentage of surface
    yticks, locs = plt.yticks()
    percent = (yticks / num_voxels) * 100
    percentage_surface_rounded = np.round(percent)
    yticks_percent = [str(x) + '%' for x in percentage_surface_rounded]
    new_yticks = (percentage_surface_rounded * yticks) / percent
    new_yticks[0] = 0
    plt.yticks(new_yticks, yticks_percent)

    plt.ylabel('Frequency of percentage of tumor surface voxels', fontsize=30, color='black')

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    # font = font_manager.FontProperties(family='Times New Roman',
    #                                    style='normal', size=30)
    # plt.legend(by_label.values(), by_label.keys(), fontsize=30, loc='best', prop=font)
    plt.legend(by_label.values(), by_label.keys(), fontsize=30, loc='best')

    # ax.legend(prop=font)
    plt.title(title + '. Patient ' + str(pat_name) + '. Lesion ' + str(lesion_id), fontsize=30)
    figpathHist = os.path.join(rootdir, figName_hist)
    gh.save(figpathHist, width=18, height=16, ext=['png'])

    # return the percentages
    return sum_perc_nonablated, sum_perc_insuffablated, sum_perc_ablated
