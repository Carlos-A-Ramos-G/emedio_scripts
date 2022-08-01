#!/usr/bin/env python
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns

def sorting(index):
    return [int(resname[4:]) for resname in index]


def residue_column_formating(df, col):
    res = lambda row: row[col][:3] + ' ' + row[col][4:].split('@',1)[0]
    df[col.upper()] = df.apply(res, axis=1)
    return df.drop(col, axis=1)


def normalize_df_column(df, col="Frac"):
    df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    return df


def raw_df_hbonds(data, R1, R2):
    """data is the hbonds analysis output file from cpptraj 
    R1 an R2 are the regions selected to include in the hbond analysis. 
    df_hb_data is a dataframe that includes the interactions
    as donor and acceptor of every residue in the regions R1 and R2.
    """
    hb = pd.read_csv(data, delimiter=r"\s+")
#    hb = hb[hb.Frac > 0.05]
    R1_as_acc = hb.rename(columns = {"#Acceptor": R1, "Donor": R2})
    R2_as_acc = hb.rename(columns = {"Donor": R1, "#Acceptor": R2})
    df_hb_data = pd.concat([R1_as_acc, R2_as_acc])
    df_hb_data.reset_index(drop=True, inplace=True)
    return df_hb_data

def df_agregation(df, reg1, reg2, col='Frac'):
    df = df.groupby([reg1, reg2])[col].sum().reset_index()
    df = normalize_df_column(df)
    df = df.pivot_table(columns = reg1, index = reg2, values=col)
    df = df.fillna(0)
    df = df.sort_index(axis=0, key=sorting)
    df = df.sort_index(axis=1, key=sorting)
    return df

def hbonds_matrix(data, R1, R2, res_i_r1, res_f_r1, col='Frac'):
    """data is the cpptraj output file
    R1 and R2 are the regions selected to include in the hbond analysis.
    res_i_r1 and res_f_ri are the first and last residue in the region 1
    this function returns the hbonds matrix normalized to be ploted"""
    df = raw_df_hbonds(data, R1, R2)
    reg1 = R1.upper()
    reg2 = R2.upper()
    reg1_res = [str(res) for res in range(res_i_r1, res_f_r1 + 1)]
    df = residue_column_formating(df, R1)
    df = residue_column_formating(df, R2)
    matrix = pd.DataFrame({})
    for i , row in df.iterrows():
        condition1 = df[reg1][i][4:] in reg1_res        
        condition2 = df[reg2][i][4:] in reg1_res
        if condition1 == True and condition2 == False:
            matrix = matrix.append(df.loc[[i]], ignore_index=True)
    return df_agregation(matrix, reg1, reg2, col)

def single_plot(cpptraj_out, region_one, region_two, first_resid_R1, last_resid_R1):
    df = hbonds_matrix(cpptraj_out, region_one, region_two, first_resid_R1, last_resid_R1)
    plt.title('H-Bonds Interactions', fontsize=15)
    sns.heatmap(df, cmap='Blues',linewidths=0.1, linecolor='gray', xticklabels=True, yticklabels=True)
    plt.show()

def compare_plot(cpptraj_out1, cpptraj_out2, region_one, region_two, first_resid_R1, last_resid_R1):
    df1 = hbonds_matrix(cpptraj_out1, region_one, region_two, first_resid_R1, last_resid_R1)
    df2 = hbonds_matrix(cpptraj_out2, region_one, region_two, first_resid_R1, last_resid_R1)
    dif = (df1 - df2).fillna(0)
    
    plt.subplot(1,3,1)
    plt.title('Interactions traj1', fontsize=15)
    sns.heatmap(df1, cmap='Blues',linewidths=0.1, linecolor='gray', xticklabels=True, yticklabels=True) 
    
    plt.subplot(1,3,2)
    plt.title('Interactions traj2', fontsize=15)
    sns.heatmap(df2, cmap='Blues',linewidths=0.1, linecolor='gray', xticklabels=True, yticklabels=True) 

    plt.subplot(1,3,3)
    plt.title('Interactions traj1 - traj2', fontsize=15)
    cmap = sns.diverging_palette(20,250, as_cmap=True)
    dif = dif.sort_index(axis=0, key=sorting)
    dif = dif.sort_index(axis=1, key=sorting)
    sns.heatmap(dif,cmap=cmap,linewidths=0.1, center =0.0,linecolor='gray', xticklabels=True, yticklabels=True)

region_one =    'substrate'    #input('Enter a string for the region/molecule to plot in the X axys > ')#'loop'
first_resid_R1= 1    #int(input(f'What is the resid of the FIRST residue in {region_one} > '))#135
last_resid_R1 = 10    #int(input(f'What is the resid of the LAST residue in {region_one} > '))#159
cpptraj_out1 =  'all_avg_traj1.out'    #input('Enter the path for the cpptraj.out file for the FIRST trajectory to compare > ')#"all_avg_traj1.out"
compare =       "yes"    #input('Do you want to compare this hbond analysis with another trajectory? yes/no > ')

region_two = 'protein'


if compare == 'yes':
    cpptraj_out2 = input('Enter the path for the cpptraj.out file for the SECOND trajectory to compare > ')#"all_avg_traj1.out"
    plt.figure(figsize=(15,8))
    compare_plot(cpptraj_out1,cpptraj_out2, region_one, region_two, first_resid_R1, last_resid_R1)
    plt.tight_layout()
elif compare == 'no':
    single_plot(cpptraj_out1, region_one, region_two, first_resid_R1, last_resid_R1)
else:
    compare = input('Do you want to compare this hbond analysis with another trajectory? yes/no > ')

plt.show()
