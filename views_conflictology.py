from viewser import Queryset, Column
import numpy as np
import pandas as pd

def conflictology_benchmark(partition, steps, loa, conflictology_period, outcome):
    """
    This function returns the forecast for the conflictology benchmark.
    
    Parameters:
    partition (dict): A dictionary containing the training and prediction dataframes.
    steps (list): A list of integers representing the steps to forecast.
    loa (str): The level of analysis, either 'cm' for country-month or 'pgm' for priogrid-month.
    conflictology_period (int): The number of months to use for the conflictology forecast.
    outcome (str): The outcome variable, either 'sb' for state-based conflict, 'ns' for non-state conflict or 'os' for one-sided conflict.
    
    Returns:
    df (DataFrame): A dataframe containing the forecast for the conflictology benchmark.
    """
    
    df = views_conflictology_forecast(
        partition.get('predict'), partition.get('train'), loa, conflictology_period, outcome)
    df = df[[f'step_pred_{i}' for i in steps]]
    return df


def views_conflictology_forecast(start_month_of_forecast, training_period, level, months_of_conflictology, outcome):
    """
    This function returns the forecast for the conflictology benchmark.
    
    Parameters:
    start_month_of_forecast (tuple): A tuple containing the start and end months of the forecast.
    training_period (tuple): A tuple containing the start and end months of the training period.
    level (str): The level of analysis, either 'cm' for country-month or 'pgm' for priogrid-month.
    months_of_conflictology (int): The number of months to use for the conflictology forecast.
    outcome (str): The outcome variable, either 'sb' for state-based conflict, 'ns' for non-state conflict or 'os' for one-sided conflict.
    
    Returns:
    forecast (DataFrame): A dataframe containing the forecast for the conflictology benchmark.
    """
    
    # add asserts
    assert level in ['cm', 'pgm'], "level must be either 'cm' or 'pgm'"
    assert outcome in ['sb', 'ns',
                       'os'], "outcome must be either 'sb', 'ns' or 'os'"
    assert isinstance(start_month_of_forecast,
                      tuple), "start_month_of_forecast must be a tuple"
    assert isinstance(
        training_period, tuple), "training_period must be a tuple"
    # assert training period is a tuple of two integers in the range of 1 to 850
    assert isinstance(
        training_period, tuple), "training_period must be a tuple"
    assert len(training_period) == 2, "training_period must have two elements"
    assert all(isinstance(i, int)
               for i in training_period), "both elements of training_period must be integers"
    assert all(
        1 <= i <= 850 for i in training_period), "both elements of training_period must be in the range of 1 to 850"
    assert isinstance(start_month_of_forecast,
                      tuple), "start_month_of_forecast must be a tuple"
    # assert start_month_of_forecast is a tuple of two integers in the range of 1 to 850
    assert len(
        start_month_of_forecast) == 2, "start_month_of_forecast must have two elements"
    assert all(isinstance(i, int)
               for i in start_month_of_forecast), "both elements of start_month_of_forecast must be integers"
    assert all(isinstance(i, int)
               for i in start_month_of_forecast), "both elements of start_month_of_forecast must be integers"

    assert isinstance(months_of_conflictology,
                      int), "months_of_conflictology must be an integer"
    assert start_month_of_forecast[0] > training_period[1], "start_month_of_forecast must be greater than the training_period"
    assert months_of_conflictology > 0, "months_of_conflictology must be greater than 0"
    assert months_of_conflictology < 850, "months_of_conflictology must be less than 850"

    if level == 'cm':
        if outcome == 'sb':
            qs_conflictology = (Queryset("conflictology", "country_month" if level == 'cm' else "priogrid_month")

                                # target variable
                                .with_column(Column("ln_ged_sb", from_loa="country_month" if level == 'cm' else "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                                             .transform.ops.ln()
                                             .transform.missing.fill()
                                             )

                                )

        if outcome == 'ns':
            qs_conflictology = (Queryset("conflictology", "country_month" if level == 'cm' else "priogrid_month")
                                # target variable
                                .with_column(Column("ln_ged_ns", from_loa="country_month" if level == 'cm' else "priogrid_month", from_column="ged_ns_best_sum_nokgi")
                                             .transform.ops.ln()
                                             .transform.missing.fill()
                                             )

                                )

        if outcome == 'os':
            qs_conflictology = (Queryset("conflictology", "country_month" if level == 'cm' else "priogrid_month")
                                # target variable
                                .with_column(Column("ln_ged_os", from_loa="country_month" if level == 'cm' else "priogrid_month", from_column="ged_os_best_sum_nokgi")
                                             .transform.ops.ln()
                                             .transform.missing.fill()
                                             )
                                )

        df_conflictology = qs_conflictology.publish().fetch()

        # In[271]:

        df_conflictology

        # In[272]:

        df_conflictology.reset_index(inplace=True)

        # In[273]:

        # create a dataframe with a particular country_id
        df_conflictology_47 = df_conflictology[df_conflictology['country_id'] == 47]

        # In[274]:

        df_conflictology_47

        # In[275]:

        df_conflictology_47[f'step_pred_1'] = None

        # In[276]:

        df_conflictology_47

        # In[277]:

        len(df_conflictology_47)

        # In[278]:

        # Initialize the column with empty lists
        df_conflictology_47['step_pred_1'] = [None]*len(df_conflictology_47)

        # For each row in the DataFrame
        for i in range(0, len(df_conflictology_47)):
            # Create a list of the ln_ged_sb values from the previous 12 months
            df_conflictology_47['step_pred_1'].iloc[i] = df_conflictology_47[f'ln_ged_{outcome}'].iloc[i-12:i].values.tolist()

        # In[279]:

        df_conflictology_47.loc[df_conflictology_47['month_id']
                                == 483, 'step_pred_1'].values[0]

        # In[280]:

        df_conflictology_47.loc[df_conflictology_47['month_id']
                                == 482, 'step_pred_1'].values[0]

        # In[281]:

        df = df_conflictology_47

        # In[282]:

        df

        # In[283]:

        df = df.drop(columns=f"ln_ged_{outcome}")

        # In[284]:

        df

        # In[285]:

        df = df.explode("step_pred_1").fillna(0)

        df['draw'] = df.groupby(['month_id', 'country_id']).cumcount()
        df.set_index(['month_id', 'country_id', 'draw'], inplace=True)

        # In[286]:

        df

        # In[287]:

        for i in range(2, 37):
            df[f'step_pred_{i}'] = df['step_pred_1'].shift(i-1)

        # In[288]:

        df

        # In[289]:

        df_conflictology_country = {}
        for i in range(1, 247):
            df_conflictology_country[i] = df_conflictology[df_conflictology['country_id'] == i]

        # In[290]:

        df_conflictology_country

        # In[291]:

        for i in range(1, 247):
            df = df_conflictology_country[i]
            ln_ged_sb_values = df[f'ln_ged_{outcome}'].tolist()
            step_pred_1_values = []

            for k in range(len(df)):
                if k < 12:
                    step_pred_1_values.append(None)
                else:
                    step_pred_1_values.append(
                        ln_ged_sb_values[k-(start_month_of_forecast[1]-training_period[1])+1-months_of_conflictology:k-(start_month_of_forecast[1]-training_period[1])+1])

            df['step_pred_1'] = step_pred_1_values

        # In[292]:

        df = df_conflictology_country[1]
        selected_rows = df['step_pred_1'][df['month_id'] == 483]
        count = sum(len(x) for x in selected_rows if x is not None)

        # In[293]:

        count

        # In[294]:

        for i in range(1, 247):
            df_conflictology_country[i] = df_conflictology_country[i].drop(
                columns=f"ln_ged_{outcome}")
            df_conflictology_country[i] = df_conflictology_country[i].explode(
                "step_pred_1").fillna(0)
            df_conflictology_country[i]['draw'] = df_conflictology_country[i].groupby(
                ['month_id', 'country_id']).cumcount()
            df_conflictology_country[i].set_index(
                ['month_id', 'country_id', 'draw'], inplace=True)
            for x in range(2, 37):
                df_conflictology_country[i][f'step_pred_{x}'] = df_conflictology_country[i]['step_pred_1'].shift(x-1).fillna(0)

        # In[295]:

        df_conflictology_country[69]

        # In[296]:

        df_sss = df_conflictology_country[47]
        # find values in step_pred_1 for a particular month_id
        df_sss.reset_index(inplace=True)
        month_id = 482
        values = df_sss['step_pred_1'][df_sss['month_id'] == month_id]

        # In[297]:

        values

        # In[298]:

        df_sss = df_conflictology_country[47]
        # find values in step_pred_1 for a particular month_id
        df_sss.reset_index(inplace=True)
        month_id = 482
        values = df_sss['step_pred_1'][df_sss['month_id'] == month_id]

        # In[299]:

        values

        # In[300]:

        df_conflictology_country

        # In[301]:

        for i in range(1, 247):
            df_conflictology_country[i].reset_index(inplace=True)

        # In[302]:

        df_conflictology_country

        # In[303]:

        df_all = pd.concat(df_conflictology_country.values())

        # In[304]:

        df_all

        # In[305]:

        df_all.set_index(['month_id', 'country_id', 'draw'], inplace=True)

        # In[306]:

        df_all.drop(columns="level_0", inplace=True)
        df_all.drop(columns="index", inplace=True)

        # In[307]:

        df_all

        # In[308]:

        # Assuming df_conflictology_country is a DataFrame
        df_forecast = df_all
        df_forecast.reset_index(inplace=True)
        forecast = df_forecast[(df_forecast['month_id'] >= start_month_of_forecast[0]) & (
            df_forecast['month_id'] <= start_month_of_forecast[1])]

        # In[310]:

        forecast.set_index(['month_id', 'country_id', 'draw'], inplace=True)

        # In[ ]:

        # forecast.drop(columns="level_0", inplace=True)

        # In[312]:

        forecast

        # ### The above is an algorithm _______________
        return forecast

    if level == 'pgm':
        if outcome == 'sb':
            qs_conflictology = (Queryset("conflictology", "country_month" if level == 'cm' else "priogrid_month")

                                # target variable
                                .with_column(Column("ln_ged_sb", from_loa="country_month" if level == 'cm' else "priogrid_month", from_column="ged_sb_best_sum_nokgi")
                                             .transform.ops.ln()
                                             .transform.missing.fill()
                                             )

                                )

        if outcome == 'ns':
            qs_conflictology = (Queryset("conflictology", "country_month" if level == 'cm' else "priogrid_month")
                                # target variable
                                .with_column(Column("ln_ged_ns", from_loa="country_month" if level == 'cm' else "priogrid_month", from_column="ged_ns_best_sum_nokgi")
                                             .transform.ops.ln()
                                             .transform.missing.fill()
                                             )

                                )

        if outcome == 'os':
            qs_conflictology = (Queryset("conflictology", "country_month" if level == 'cm' else "priogrid_month")
                                # target variable
                                .with_column(Column("ln_ged_os", from_loa="country_month" if level == 'cm' else "priogrid_month", from_column="ged_os_best_sum_nokgi")
                                             .transform.ops.ln()
                                             .transform.missing.fill()
                                             )
                                )

        df_conflictology = qs_conflictology.publish().fetch()

        # In[271]:

        df_conflictology

        # In[272]:

        df_conflictology.reset_index(inplace=True)

        # In[273]:

        # create a dataframe with a particular country_id
        df_conflictology_country = {}
        for i in range(62356, 190512):
            df_conflictology_country[i] = df_conflictology[df_conflictology['priogrid_gid'] == i]

        # In[290]:

        df_conflictology_country

        # In[291]:

        for i in range(62356, 190512):
            df = df_conflictology_country[i]
            ln_ged_sb_values = df[f'ln_ged_{outcome}'].tolist()
            step_pred_1_values = []

            for k in range(len(df)):
                if k < 12:
                    step_pred_1_values.append(None)
                else:
                    step_pred_1_values.append(
                        ln_ged_sb_values[k-(start_month_of_forecast[1]-training_period[1]+1)-months_of_conflictology:k-(start_month_of_forecast[1]-training_period[1])+1])

            df['step_pred_1'] = step_pred_1_values

        # In[292]:

        # In[293]:

        # In[294]:

        for i in range(62356, 190512):
            df_conflictology_country[i] = df_conflictology_country[i].drop(
                columns=f"ln_ged_{outcome}")
            df_conflictology_country[i] = df_conflictology_country[i].explode(
                "step_pred_1").fillna(0)
            df_conflictology_country[i]['draw'] = df_conflictology_country[i].groupby(
                ['month_id', 'priogrid_gid']).cumcount()
            df_conflictology_country[i].set_index(
                ['month_id', 'priogrid_gid', 'draw'], inplace=True)
            for x in range(2, 37):
                df_conflictology_country[i][f'step_pred_{x}'] = df_conflictology_country[i]['step_pred_1'].shift(x-1).fillna(0)

        # In[295]:

        # In[296]:

        # In[301]:

        for i in range(62356, 190512):
            df_conflictology_country[i].reset_index(inplace=True)

        # In[302]:

        df_conflictology_country

        # In[303]:

        df_all = pd.concat(df_conflictology_country.values())

        # In[304]:

        df_all

        # In[305]:

        df_all.set_index(['month_id', 'priogrid_gid', 'draw'], inplace=True)

        # In[306]:

        # df_all.drop(columns="level_0", inplace=True)
        # df_all.drop(columns="index", inplace=True)

        # In[307]:

        df_all

        # In[308]:

        # Assuming df_conflictology_country is a DataFrame
        df_forecast = df_all
        df_forecast.reset_index(inplace=True)
        forecast = df_forecast[(df_forecast['month_id'] >= start_month_of_forecast[0]) & (
            df_forecast['month_id'] <= start_month_of_forecast[1])]

        # In[310]:

        forecast.set_index(['month_id', 'priogrid_gid', 'draw'], inplace=True)

        # In[ ]:

        # forecast.drop(columns="level_0", inplace=True)

        # In[312]:

        forecast

        # ### The above is an algorithm _______________
        return forecast
