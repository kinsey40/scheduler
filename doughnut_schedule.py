"""
Author: Nicholas Kinsey (kinsey40)

Date: 05/11/2017

Description:
A script designed to create a scheduling procedure. In this instance for the
doughnuts, which are bought by two of the graduates each week on a rolling rota.
Use the unavilable dates setting and participants, to edit both the participants
and the avaliability of those individuals. Furthermore, it can be customized by
editing the start date, so it can be used for future graduate intakes.

Inputs:
Manually input variables in the global variables section

Outputs:
A csv file to the stated location.
"""

############ TO DO #############
# Allow for non-even no. of participants (various numbers) ~10hrs
################################

""" *** IMPORT LIBRARIES *** """
import numpy as np
import pandas as pd
import datetime
import random
import sys
from random import randint
from datetime import date
from datetime import timedelta
from datetime import datetime as dt

""" *** GLOBAL VARIABLES *** """
# Set the parameters
CSV_SAVE_LOC = "/home/kinsey40/Documents/Roke/Doughnuts/Doughnut_Schedule_Created.csv"
PARTICIPANTS = ['NK', 'CB', 'GW', 'DB', 'HK', 'MG', 'FP', 'FO', 'FI', 'FU', 'FY', 'FH', 'FT', 'FR']
START_DATE = datetime.date(2017, 10, 20) # Year, month, day

# Max no. of times you can be with the same person
SAME_NO_OF_TIMES = 5

# Insert unavilable dates here
NK_UNAVAILABLE_DATES = [datetime.date(2018, 6, 1), datetime.date(2018, 9, 7)]
CB_UNAVAILABLE_DATES = []
GW_UNAVAILABLE_DATES = [datetime.date(2018, 8, 17)]
DB_UNAVAILABLE_DATES = [datetime.date(2018, 9, 21)]
HK_UNAVAILABLE_DATES = [datetime.date(2018, 10, 5)]
MG_UNAVAILABLE_DATES = []
FP_UNAVAILABLE_DATES = []
FO_UNAVAILABLE_DATES = []
FI_UNAVAILABLE_DATES = []
FU_UNAVAILABLE_DATES = []
FY_UNAVAILABLE_DATES = []
FH_UNAVAILABLE_DATES = []
FT_UNAVAILABLE_DATES = []
FR_UNAVAILABLE_DATES = []

GLOBAL_REMOVE_DATES = [datetime.date(2017, 12, 22), datetime.date(2017, 12, 29)]
ALREADY_DONE_DATES = [datetime.date(2017, 10, 20), datetime.date(2017, 10, 27)]
ALREADY_DONE_PERSON_1 = ['NK', 'CB']
ALREADY_DONE_PERSON_2 = ['GW', 'MG']

DATE_TODAY = datetime.date.today()
UPDATE = True
CURRENT_SCHEDULE_LOC = "/home/kinsey40/Documents/Roke/Doughnuts/Doughnut_Schedule_Created.csv"

""" *** FUNCTIONS *** """
def how_many_times(participants, limit_value=52):

    # Find the no. of participants
    no_of_ppl = len(participants)

    # Define two seperate counters
    counter = 0
    counter_2 = 0

    # Account for all the dates that are removed from the system
    limit = limit_value - len(GLOBAL_REMOVE_DATES)

    # Perform while loop, altering the counters respectively
    while counter < limit:
        counter += (no_of_ppl / 2)
        counter_2 += 1

    # Examine the differences
    upper_diff = counter - limit
    lower_diff = limit - (counter - no_of_ppl)

    # If the upper diff. is smaller, return where counter2 got to
    if upper_diff <= lower_diff:

        no_of_weeks = counter_2 * (no_of_ppl / 2)
        return counter_2, int(no_of_weeks)

    # If the lower diff. is smaller, return where it would have got to
    elif upper_diff > lower_diff:

        no_of_times = counter_2 - 1
        no_of_weeks = no_of_times * (no_of_ppl / 2)
        return no_of_times, int(no_of_weeks)

    # Return an error if the calculation fails
    else:

        print("Error with calculation in how many times")
        return 1

def create_dataframe(start_date, no_of_weeks):

    # Form the DF, set the initial date and timedelta
    df = pd.DataFrame(columns = ['date', 'person_1', 'person_2'])
    df.at[0, 'date'] = start_date
    week = timedelta(days=7)

    # Initialize a counter and old date variable
    week_counter = 1
    old_date = df.at[week_counter-1, 'date']
    found_removed_date = False

    # Put the dates into the df, leaving other cols empty for now
    while week_counter < no_of_weeks:
        new_date = old_date + week

        if new_date not in GLOBAL_REMOVE_DATES:
            df.at[week_counter,'date'] = new_date
            old_date = new_date
            week_counter += 1
        else:
            old_date = new_date

    #print(df)
    #sys.exit(0)
    return df

def populate_dataframe(df_true, no_of_times, participants, unavailable_dates):

    print("populating...")

    # Create a copy of the df
    df = df_true.copy()

    # Create a list with values from zero to len(df), these represents the weeks
    df_dropped_nans = df.dropna(axis=0, how='any')
    values = list(range(0, len(df)))
    values_2 = list(range(0, len(df)))
    del values[0:len(df_dropped_nans)]
    del values_2[0:len(df_dropped_nans)]
    all_values = values + values_2

    # A checker to see if anything goes wrong
    checker = False
    bugger = False

    while not checker:
        # Iterate over the individuals, and their unavailable_dates
        for person_number, (person, ind_unavailable_dates) in enumerate(zip(participants, unavailable_dates)):
            number = 0
            last_person = False
            other_people_for_person = []
            identified_weeks_for_person = []

            # Count the number of values for each person already present in df, adjust accordingly
            value_counts_1 = df_dropped_nans.groupby('person_1').person_1.count()
            value_counts_2 = df_dropped_nans.groupby('person_2').person_2.count()
            count_for_person_1 = 0
            count_for_person_2 = 0

            if person in value_counts_1.index:
                count_for_person_1 = value_counts_1.loc[person,]

            if person in value_counts_2.index:
                count_for_person_2 = value_counts_2.loc[person,]

            both_value_counts = count_for_person_1 + count_for_person_2
            person_no_of_times = no_of_times - both_value_counts

            # Issues arise sometimes with the last person, if this occurs, re-run
            if person_number == len(participants)-1:
                last_person = True

                # Check that one person can't do a week by themself
                if len(all_values) == len(set(all_values)):
                    print("All values unique, continuing...")
                else:
                    print("Last participant error, re-running...")
                    checker = True
                    return df, 0

            # Iterate over the number of times each individual does it
            while number < person_no_of_times and len(all_values) > 0:

                # Select an element from the list of weeks
                if len(all_values) == 1:
                    loc = 0
                else:
                    loc = randint(0, len(all_values)-1)
                element_val = all_values[loc]
                variable = False

                # Check to see if that person has already been assigned that week
                if element_val in identified_weeks_for_person:
                    print("Same person on the same week")
                    variable = True

                    if last_person:
                        print("Same person error, re-running...")
                        checker = True
                        return df, 0
                    continue
                else:
                    pass

                # Check to see that individual can do those dates
                for un_dates in ind_unavailable_dates:

                    if df.loc[element_val, "date"] == un_dates:
                        print("Picking a new number...")
                        variable = True

                        if last_person:
                            print("Last person, can't do date, re-running...")
                            checker = True
                            return df, 0
                        break;
                    else:
                        continue

                # Prevents same person doing it two weeks in a row
                if element_val == 0:
                    if df.loc[element_val + 1, "person_1"] == person or \
                       df.loc[element_val + 1, "person_2"] == person:
                        variable = True

                        if last_person:
                            print("Last person, can't do dual weeks, re-running...")
                            checker = True
                            return df, 0

                elif element_val == len(df) - 1:
                    if df.loc[element_val - 1, "person_1"] == person or \
                       df.loc[element_val - 1, "person_2"] == person:
                        variable = True

                        if last_person:
                            print("Last person, can't do dual weeks, re-running...")
                            checker = True
                            return df, 0

                else:
                    if df.loc[element_val - 1, "person_1"] == person or \
                       df.loc[element_val + 1, "person_1"] == person or \
                       df.loc[element_val - 1, "person_2"] == person or \
                       df.loc[element_val + 1, "person_2"] == person:
                        variable = True

                        if last_person:
                            print("Last person, can't do dual weeks, re-running...")
                            checker = True
                            return df, 0

                # Check to see if been with intended person for too many times
                if not (pd.isnull(df.loc[element_val, "person_1"]) or pd.isnull(df.loc[element_val, "person_2"]) and variable):

                    if not pd.isnull(df.loc[element_val, "person_1"]):
                        other_person = df.loc[element_val, "person_1"]

                    else:
                        other_person = df.loc[element_val, "person_2"]

                    # Count number of occurences of being with that person
                    count_other_people = other_people_for_person.count(other_person)

                    # Evaluate against set global parameter
                    if count_other_people >= SAME_NO_OF_TIMES:
                        print("Been with this person too many times")

                        if last_person:
                            print("Same person error, re-running...")
                            checker = True
                            return df, 0
                        continue

                    # Append if within the limit
                    else:
                        other_people_for_person.append(other_person)

                # Re-pick a new date, as that person can't do that date
                if variable:
                    continue

                # Set the values in the DataFrame
                else:
                    if pd.isnull(df.loc[element_val, "person_1"]):
                        df.loc[element_val, "person_1"] = person
                        identified_weeks_for_person.append(element_val)

                    elif pd.isnull(df.loc[element_val, "person_2"]):
                        df.loc[element_val, "person_2"] = person
                        identified_weeks_for_person.append(element_val)

                    else:
                        checker=True
                        return df, 0
                        print("Error in checking DataFrame")

                    # Delete that entry from the list, so it can't be picked again, move while-loop forward
                    del all_values[loc]
                    number += 1

                # DataFrame formed correctly, exit the loop
                if len(all_values) <= 0:
                    print("Table has been formed, exiting loop")
                    checker=True

    return df, 1

def export_table(df, export_loc):

    df.to_csv(export_loc, header=True, index_label="week_no")
    print("Table has been exported")

def already_done_weeks(df, dates, p1, p2):

    for value, (date, person_1, person_2) in enumerate(zip(dates, p1, p2)):
        df.at[value, "date"] = date
        df.at[value, "person_1"] = person_1
        df.at[value, "person_2"] = person_2

    return df

def form_past_schedule(df):

    for index, row in df.iterrows():

        if dt.strptime(row["date"], "%Y-%m-%d") >= datetime.datetime.combine(DATE_TODAY, datetime.time.min):
            week_no = index
            print("We are on week no:", week_no)
            break;

            if len(df)-week_no < (len(PARTICIPANTS)/4):
                print("Very close to end, can't perform update now...")
                sys.exit(0)

        else:
            continue

    # Select weeks that have already occured
    df_keep = df[0:week_no]
    other_dates = df.loc[week_no:len(df), "date"]
    other_dates_labeled = pd.DataFrame({"date":other_dates.values})

    # Concat. the future dates back on
    new_df = pd.concat([df_keep, other_dates_labeled], ignore_index=True, axis=0)

    return new_df

def caller():

    if (len(PARTICIPANTS) % 2 != 0):
        print("Number of Participants must be a multiple of 2")
        return 1

    unavailable_dates = [NK_UNAVAILABLE_DATES,
                        CB_UNAVAILABLE_DATES,
                        GW_UNAVAILABLE_DATES,
                        DB_UNAVAILABLE_DATES,
                        HK_UNAVAILABLE_DATES,
                        MG_UNAVAILABLE_DATES,
                        FP_UNAVAILABLE_DATES,
                        FO_UNAVAILABLE_DATES,
                        FI_UNAVAILABLE_DATES,
                        FU_UNAVAILABLE_DATES,
                        FY_UNAVAILABLE_DATES,
                        FH_UNAVAILABLE_DATES,
                        FT_UNAVAILABLE_DATES,
                        FR_UNAVAILABLE_DATES]

    # Call the functions
    no_of_times, no_of_weeks = how_many_times(PARTICIPANTS)

    # Check if this is an update or not
    if not UPDATE:
        unpopulated_df = create_dataframe(START_DATE, no_of_weeks)
        unpopulated_df = already_done_weeks(unpopulated_df, ALREADY_DONE_DATES, ALREADY_DONE_PERSON_1, ALREADY_DONE_PERSON_2)

    else:
        try:
            current_schedule = pd.read_csv(CURRENT_SCHEDULE_LOC, header=0, usecols=["date", "person_1", "person_2"])
        except:
            print("Error in locating schedule, for update")

        unpopulated_df = form_past_schedule(current_schedule)

    # A variable to track successful execution
    success_variable = 0

    # Keep trying until the dataframe is formed
    while success_variable != 1:
        unpopulated_df_copy = unpopulated_df.copy()
        df_return, success_variable = populate_dataframe(unpopulated_df_copy, no_of_times, PARTICIPANTS, unavailable_dates)

    # Export the table to the relevant location
    export_table(df_return, CSV_SAVE_LOC)

""" *** MAIN SCRIPT *** """
if __name__ == "__main__":

    # Call the caller function
    caller()

""" *** END OF FILE *** """
