# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:43:36 2017

@author: Raluca Sandu
"""
import os
import time
import pandas as pd
import plotHistDistances as pm
from distancemetrics import DistanceMetrics
from volumemetrics import VolumeMetrics
import DistancesVolumes_twinAxes as twinAxes
import distances_boxplots_all_lesions as bpLesions


def main_distance_volume_metrics(patient_id, ablation_segmentation, tumor_segmentation, lesion_id, ablation_date, dir_plots,
                                 FLAG_SAVE_TO_EXCEL=True, title='Ablation to Tumor Euclidean Distances'):

    patient_id = patient_id
    df_metrics_all = pd.DataFrame()

    # distanceMaps_allPatients = []
    perc_5_0_allPatients = []
    perc_0_5_allPatients = []
    perce_5_10_allPatients = []

    evalmetrics = DistanceMetrics(ablation_segmentation, tumor_segmentation)
    df_distances_1set = evalmetrics.get_SitkDistances()
    # call function to compute volume metrics
    evaloverlap = VolumeMetrics()
    evaloverlap.set_image_object(ablation_segmentation, tumor_segmentation)
    evaloverlap.set_volume_metrics()
    df_volumes_1set = evaloverlap.get_volume_metrics_df()
    df_metrics = pd.concat([df_volumes_1set, df_distances_1set], axis=1)
    # df_metrics_all = df_metrics_all.append(df_metrics)
    distanceMap = evalmetrics.get_surface_distances()
    # distanceMaps_allPatients.append(distanceMap)
    num_surface_pixels = evalmetrics.num_tumor_surface_pixels
    # %% surfaces distance percentages

    #  plot the color coded histogram of the distances
    try:
        sum_perc_nonablated, sum_perc_insuffablated, sum_perc_ablated = pm.plotHistDistances(pat_name=patient_id,
                                                                                             trajectory_idx=lesion_id,
                                                                                             pathology="CRLM",
                                                                                             rootdir=dir_plots,
                                                                                             distanceMap=distanceMap,
                                                                                             num_voxels=num_surface_pixels,
                                                                                             title=title)

        df_metrics_all = df_metrics_all.append(df_metrics)
        # distanceMaps_allPatients.append(distanceMap)
        perc_0_5_allPatients.append(sum_perc_nonablated)
        perc_0_5_allPatients.append(sum_perc_insuffablated)
        perce_5_10_allPatients.append(sum_perc_ablated)

    except Exception:
        # append empty dataframe
        numRows, numCols = df_metrics_all.shape
        numRows = 1
        df_empty = pd.DataFrame(index=range(numRows), columns=range(numCols))
        df_metrics_all = df_metrics_all.append(df_empty)
        # append empty DataFrame
        # distanceMaps_allPatients.append([])
        # TODO: set the columns as well
        print(patient_id, 'error computing the distances and volumes')

    # %%
    # add the Distance Map to the input dataframe. to be written to Excel
    # df_patientdata['DistanceMaps'] = distanceMaps_allPatients
    df_metrics_all.index = list(range(len(df_metrics_all)))
    df_metrics_all['DistanceMaps'] = distanceMap
    # df_final = pd.concat([distanceMaps_allPatients, df_metrics_all], axis=1)

    # data_distances_to_plot = df_patients_sorted['DistanceMaps'].tolist()
    # data_volumes_to_plot = df_patients_sorted['Tumour coverage ratio']
    # plot Boxplot per patient
    # bpLesions.plotBoxplots(data_distances_to_plot, rootdir)
    # plot distances in Boxplot vs Tumor Coverage Ratio
    # twinAxes.plotBoxplots(data_distances_to_plot, data_volumes_to_plot, rootdir)
    # %%
    ''' save to excel the average of the distance metrics '''
    if FLAG_SAVE_TO_EXCEL:
        print('writing to Excel....', dir_plots)
        timestr = time.strftime("%H%M%S-%Y%m%d")
        filename = patient_id + '_' + lesion_id + '_' + title + '-' + ablation_date + '.xlsx'
        filepath_excel = os.path.join(dir_plots, filename)
        writer = pd.ExcelWriter(filepath_excel)
        df_metrics_all.to_excel(writer, index=False, float_format='%.2f')
        writer.save()

