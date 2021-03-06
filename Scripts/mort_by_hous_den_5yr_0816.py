# Mortgage share of income by population density
import pandas as pd
import numpy as np
import array

file = pd.read_csv('county_rent_mort_inc_units_5yr.csv')

yrs_dict = {}
for year in range(2008, 2017):
    print(year)
    yr_df = file[file.Year == year].dropna(subset=['Housing_Den'])
    yr_df.Total_Owned = yr_df.Total_Owned.astype(int)  # For np.full in line 31
    
    # FIPS grouped by county population density
    homes200 = yr_df.FIPS[(yr_df.Year == year) & (yr_df.Housing_Den > 200)].values
    homes75 = yr_df.FIPS[(yr_df.Year == year) & (yr_df.Housing_Den > 75) & (yr_df.Housing_Den <= 200)].values
    homes30 = yr_df.FIPS[(yr_df.Year == year) & (yr_df.Housing_Den > 30) & (yr_df.Housing_Den <= 75)].values
    homes20 = yr_df.FIPS[(yr_df.Year == year) & (yr_df.Housing_Den > 20) & (yr_df.Housing_Den <= 30)].values
    homes10 = yr_df.FIPS[(yr_df.Year == year) & (yr_df.Housing_Den > 10) & (yr_df.Housing_Den <= 20)].values
    homes5 = yr_df.FIPS[(yr_df.Year == year) & (yr_df.Housing_Den > 5) & (yr_df.Housing_Den <= 10)].values
    homesless5 = yr_df.FIPS[yr_df.Housing_Den <= 5].values
    
    groups_dict = {}
    fips_groups = [homes200, homes75, homes30, homes20, homes10, homes5, homesless5]
    groups = ['200', '75', '30', '20', '10', '5', 'Less5']
    counter = 0
    for fips_group in fips_groups:
        fips_mort = array.array('f')
        for fips in fips_group:
            med_mort = yr_df.Med_Mort[yr_df.FIPS == fips].iloc[0]
            home_count = yr_df.Total_Owned[yr_df.FIPS == fips].iloc[0]
            fips_mort.extend(np.full(home_count, med_mort))
        groups_dict[groups[counter]] = np.median(fips_mort).round(3)
        counter += 1
    yrs_dict[year] = groups_dict

df = pd.DataFrame(yrs_dict)
df = df.transpose()
df.columns = ['More than 200', '75 to 200', '30 to 75', '20 to 30', '10 to 20', '5 to 10', 'Less than 5']
df['Year'] = list(range(2008, 2017))
df = df.melt(id_vars='Year', var_name='Hous_Den', value_name='Med_Mort')
df.to_csv('mort_by_hous_den_5yr_0816.csv', index=False)