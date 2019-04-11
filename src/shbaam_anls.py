#!/usr/bin/env python
#*******************************************************************************
#shbaam_analysis.py
#*******************************************************************************

#Purpose:
# Combine GLDAS and GRACE anomalies to compute groundwater anomalies & exports
# a csv file to and summary figures (GRACE & GLDAS, and GW anomalies)

#Authors:
#A.J. Purdy
#Cedric H. David


#*******************************************************************************
#Import Python modules
#*******************************************************************************
import sys
import glob
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np


#*******************************************************************************
#Declaration of variables (given as command line arguments)
#*******************************************************************************
# 1 - IN_DIR_PATH
# 2 - REGION
# 3 - OUT_CSV_FILENAME

#*******************************************************************************
#Get command line arguments
# IN_DIR_PATH = output/SERVIR_STK/
# REGION = NorthWestBangladesh

#*******************************************************************************
IS_arg = len(sys.argv)

if IS_arg != 4:
     print('PLEASE ENTER DIRECTORY WITH GLDAS and GRACE MAPS, REGION OF INTEREST, and output file')
     print('\n./shbaam_analysis.py ../output/SERVIR_STK/ NorthWestBD ../output/SERVIR_STK/timeseries_NorthWestBD_ALLa.csv\n')
     raise SystemExit(22)

IN_DIR_PATH = sys.argv[1]
REGION = sys.argv[2]
OUT_CSV_FILENAME = sys.argv[3]

#*******************************************************************************
#Print input information
#*******************************************************************************
print('Command line inputs')
print(' - '+IN_DIR_PATH)
print(' - '+REGION)

#*******************************************************************************
#Check if files exist in output folder
#*******************************************************************************
if len(glob.glob(IN_DIR_PATH+'*' + REGION +'*'+ '.csv')) < 5:
     print('PLEASE execute shbaam_conc.py & shbaam_ldas_anoms.py before executing this script')
     raise SystemExit(22)

#*******************************************************************************
#Read GRACE and GLDAS csv files & compute groundwater anomalies
#*******************************************************************************
time_series_files = glob.glob(IN_DIR_PATH+'*' + REGION + '*'+'.csv')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Create output dataframe for ALL variables
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
df_all = pd.DataFrame()
for f in time_series_files:
     if 'CLM' in f or 'MOS' in f or 'NOAH' in f or 'VIC' in f:
          df_i = pd.read_csv(f)
          df_all['date']=df_i.date
          for h in list(df_i)[1:]:
               if 'CLM' in f:
                    df_all[h+'_CLM']=df_i[h]
               if 'MOS' in f:
                    df_all[h+'_MOS']=df_i[h]
               if 'NOAH' in f:
                    df_all[h+'_NOAH']=df_i[h]
               if 'VIC' in f:
                    df_all[h+'_VIC']=df_i[h]

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Combine all GLDAS models
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

df_all["SMTa_mean"]=(df_all.SMTa_MOS + df_all.SMTa_NOAH + df_all.SMTa_VIC
                                + df_all.SMTa_CLM)/4

df_all["Canopint_mean"]=(df_all.Canopint_MOS + df_all.Canopint_NOAH + df_all.Canint_VIC
                                + df_all.Canopint_CLM)/4

df_all["SWE_mean"]=(df_all.SWE_MOS + df_all.SWE_NOAH + df_all.SWE_VIC
                                + df_all.SWE_CLM)/4
df_all.set_index(pd.to_datetime(df_all.date), inplace=True)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Read in GRACE data and set time index
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

for f in time_series_files:
     if 'GRC' in f:
          grc_df = pd.read_csv(f)
          grc_df.columns = ['date_grc', 'twsa']
          grc_df.set_index(pd.to_datetime(grc_df.date_grc), inplace=True)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Resample GRACE to GLDAS time stamp.
# GRACE INTERPOLATION
# Groundwater anomaly computation
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def GRACE_interp(grc_df):
    '''

    :param grc_df: input GRACE dataframe (output from shbaam_twsa.py)
    :return df_sync_gr: gap-filled GRACE data following below methods

    # We follow the methods of Hamlington et al., 2019 'Amplitude Modulation of Seasonal
    # Variability in Terrestrial Water Storage'.
    # 1. Compute and remove trend from original data
    # 2. Compute climatology
    # 3. Remove climatology from original data
    # 4. Gap-fill climatology-free data (inter-annual variations) by cubic interpolation
    # 5. Add climatology back to the gap-filled data to get filled TWSA
    '''
    df_sync_grc = grc_df.resample('M').fillna(method='pad', limit=1)
    x = np.arange(df_sync_grc.index.size)
    df_sync_grc['x']=x
    df_nonans = df_sync_grc.dropna()
    X = np.array(df_nonans.x)
    fit = np.polyfit(X, df_nonans.twsa, 1)
    fit_fn = np.poly1d(fit)
    df_sync_grc['linear_trend']= fit_fn(x)
    df_sync_grc['iav']=df_sync_grc.twsa-df_sync_grc.linear_trend
    df_sync_grc['month_num']=df_sync_grc.index.month
    month_clim = df_sync_grc.iav.groupby(df_sync_grc.index.month).mean()
    clim_dict = month_clim.to_dict()
    df_sync_grc['clim']=df_sync_grc['month_num'].map(clim_dict)
    df_sync_grc['noclim']=df_sync_grc.twsa-df_sync_grc.clim
    df_sync_grc['noclim_fill'] = df_sync_grc.noclim.fillna(method='pad', limit=1).interpolate(method='cubic', limit=3)
    df_sync_grc['twsa_fill'] =df_sync_grc.noclim_fill+df_sync_grc.clim
    return df_sync_grc

df_sync_grc = GRACE_interp(grc_df)
df_all = df_all[(df_all['date'] < '2016-09-01')]
df_sync_gldas = df_all.resample('M').pad()
df_sync_gldas['grace_twsa'] = df_sync_grc['twsa_fill']
df_sync_gldas['gw_a'] = df_sync_gldas.grace_twsa - df_sync_gldas.SMTa_mean - df_sync_gldas.Canopint_mean - df_sync_gldas.SWE_mean

# Saving CSV
df_sync_out = df_sync_gldas[['gw_a', 'grace_twsa', 'SMTa_mean', 'Canopint_mean', 'SWE_mean']]
df_sync_out.rename(columns={'Canopint_mean':'CANa','SWE_mean':'SWEa'})
df_sync_out.to_csv(OUT_CSV_FILENAME)

#*******************************************************************************
#Create figure of GLDAS water storage anomalies
#*******************************************************************************

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Check if output directory exist if not create directory
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
OUT_FIG_DIR = IN_DIR_PATH+os.sep+'figures'
if not os.path.isdir(OUT_FIG_DIR):
    os.mkdir(OUT_FIG_DIR)
    print('making directory:\t'+OUT_FIG_DIR)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Plot GLDAS anomalies on separate plots & save to shbaam/output/figures/
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

fig1, axs = plt.subplots(4, 1, figsize=(8, 6.5), facecolor='k', sharex=True)
fig1.subplots_adjust(hspace=0)
axs[0].set_title(REGION + '\nWater Storage Changes')
axs[0].plot(df_sync_gldas.SWE_mean)
axs[0].set_ylabel('SWE\n (cm)\n')
# axs[0].set_ylim([-.24, .24])
axs[1].plot(df_sync_gldas.Canopint_mean)
# axs[1].set_ylim([-.24, .24])
axs[1].set_ylabel('Canopy\nStorage (cm)')
axs[2].plot(df_sync_gldas.SMTa_mean)
axs[2].set_ylabel('Soil \nMoisture \n(cm)\n')
# axs[2].set_ylim([-30., 32.2])
axs[3].plot(df_sync_grc.twsa_fill)
axs[3].set_ylabel('TWSA\n(cm)')
# axs[3].set_ylim([-55., 65.2])
plt.tight_layout()
fig1.savefig(OUT_FIG_DIR + os.sep + 'water_comps_' + REGION + '.png', dpi=200)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Plot GRACE groundwater anomaly & save to shbaam/output/figures/
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

fig2 = plt.figure(figsize=(6,4))
plt.title(REGION + ' Groundwater Anomalies')
df_sync_gldas.gw_a.plot()
plt.ylabel('Water Storage (cm)')
plt.xlabel(' ')
plt.tight_layout()
fig2.savefig(OUT_FIG_DIR + os.sep + 'gwa_' + REGION + '.png', dpi=200)


#*******************************************************************************
# End
#*******************************************************************************
