# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import math
import numpy as np
from argparse import ArgumentParser

# -- Setup argument parser ####
parser = ArgumentParser(description="Import pairing form result.")
parser.add_argument(dest="tutor_csv", help="Student application csv entry.")
parser.add_argument(dest="student_csv", help="Tutor application csv entry.")
parser.add_argument(dest="save_directory", help="Where you would like to save the files.")
# ----------------
def initial_table(test):
    """
    Creating initial table with times available on all days, name, email.
    :param test: The table from the form that tutors fill out
    :return: fin_table with table in the form of 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
    'Friday', 'Saturday', 'Sunday' and tutor information as well as lists (name_list, email_list, last_updated_date)
    """
    dict = {}
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    time_slot = ["1", "2", "3", "4", "5"]
    error = []
    for d in range(0, len(days)):
        dict[days[d]] = []
    name_list = []
    email_list = []
    language_list = []
    interest_list = []
    submission_date = []
    for i in range(0, len(test)):
        name_list.append(test["Your First + Last Name"][i])
        email_list.append(test["Your Email"][i])
        language_list.append(test["Language"][i])
        interest_list.append(test["Interest"][i])
        submission_date.append(test["Submission Date"][i])
        Monday = []
        Tuesday = []
        Wednesday = []
        Thursday = []
        Friday = []
        Saturday = []
        Sunday = []
        for d in range(0, len(days)):
            for nn in range(1, 6):
                if (
                    test[f"{days[d]} Time {nn}"][i] != "PM\nPM"
                    and pd.isna(test[f"{days[d]} Time {nn}"][i]) == False
                ):
                    if (
                        test[f"{days[d]} Time {nn}"][i][22:23] == ":"
                        and test[f"{days[d]} Time {nn}"][i][21:22] != "0"
                    ):  # test['Monday Time 2'][0] '08:00 PM - 09:00 PM (1:00)'
                        if d == 0:
                            Monday.append(test[f"{days[d]} Time {nn}"][i][:-7])
                        elif d == 1:
                            Tuesday.append(test[f"{days[d]} Time {nn}"][i][:-7])
                        elif d == 2:
                            Wednesday.append(
                                test[f"{days[d]} Time {nn}"][i][:-7]
                            )
                        elif d == 3:
                            Thursday.append(
                                test[f"{days[d]} Time {nn}"][i][:-7]
                            )
                        elif d == 4:
                            Friday.append(test[f"{days[d]} Time {nn}"][i][:-7])
                        elif d == 5:
                            Saturday.append(
                                test[f"{days[d]} Time {nn}"][i][:-7]
                            )
                        elif d == 6:
                            Sunday.append(test[f"{days[d]} Time {nn}"][i][:-7])
                    else:
                        error.append(test["Your First + Last Name"][i])

        dict["Monday"].append(Monday)
        dict["Tuesday"].append(Tuesday)
        dict["Wednesday"].append(Wednesday)
        dict["Thursday"].append(Thursday)
        dict["Friday"].append(Friday)
        dict["Saturday"].append(Saturday)
        dict["Sunday"].append(Sunday)

    fin_table = pd.DataFrame(dict)
    fin_table.insert(0, "Name", name_list)
    fin_table.insert(1, "Email", email_list)
    fin_table.insert(2, "Language", language_list)
    fin_table.insert(3, "Interest", interest_list)
    fin_table.insert(4, "Submission Date", submission_date)

    for day in days:
        for k in range(0, len(fin_table)):
            fin_table[day][k] = unique(fin_table[day][k])

    return (
        fin_table,
        name_list,
        email_list,
        language_list,
        interest_list,
        submission_date,
        error,
    )


def vectorize_table(
    fin_table,
    name_list,
    email_list,
    language_list,
    interest_list,
    submission_date,
):
    """
    Creating vector for comparison
    :param fin_table: Table from initialization
    :return: the table with time in vector form
    """
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    dict_comparison = {}
    for d in range(0, len(days)):
        dict_comparison[days[d]] = []

    for i in range(0, len(fin_table)):
        for j in range(0, len(days)):
            temp_vector = []
            for k in range(0, len(fin_table[days[j]][i])):
                if (
                    fin_table[days[j]][i][k][6:8] == "PM"
                    and fin_table[days[j]][i][k][17:19] == "PM"
                ):
                    if fin_table[days[j]][i][k][0:2] != "12":
                        start_hour = (
                            int(fin_table[days[j]][i][k][0:2]) + 12
                        )  # fin_table[days[j]][i][k][0:2] #Start Time Hour
                    else:
                        start_hour = int(fin_table[days[j]][i][k][0:2])

                    if fin_table[days[j]][i][k][11:13] != "12":
                        end_hour = (
                            int(fin_table[days[j]][i][k][11:13]) + 12
                        )  # fin_table[days[j]][i][k][11: 13] #End Time Hour
                    else:
                        end_hour = int(fin_table[days[j]][i][k][11:13])

                elif (
                    fin_table[days[j]][i][k][6:8] == "AM"
                    and fin_table[days[j]][i][k][17:19] == "AM"
                ):
                    start_hour = int(fin_table[days[j]][i][k][0:2])
                    end_hour = int(fin_table[days[j]][i][k][11:13])
                elif (
                    fin_table[days[j]][i][k][6:8] == "AM"
                    and fin_table[days[j]][i][k][17:19] == "PM"
                ):
                    start_hour = int(fin_table[days[j]][i][k][0:2])
                    if fin_table[days[j]][i][k][11:13] != "12":
                        end_hour = (
                            int(fin_table[days[j]][i][k][11:13]) + 12
                        )  # fin_table[days[j]][i][k][11: 13] #End Time Hour
                    else:
                        end_hour = int(fin_table[days[j]][i][k][11:13])

                start_minutes = (
                    int(fin_table[days[j]][i][k][3:5]) / 60
                )  # Start Time Minutes
                end_minutes = (
                    int(fin_table[days[j]][i][k][14:16]) / 60
                )  # End Time Minutes
                start_time = start_hour + start_minutes
                end_time = end_hour + end_minutes
                temp_vector.append([start_time, end_time])
            if len(fin_table[days[j]][i]) == 0:
                dict_comparison[days[j]].append([0, 0])
            else:
                dict_comparison[days[j]].append(temp_vector)

    comparison_table = pd.DataFrame(dict_comparison)
    comparison_table.insert(0, "Name", name_list)
    comparison_table.insert(1, "Email", email_list)
    comparison_table.insert(2, "Language", language_list)
    comparison_table.insert(3, "Interest", interest_list)
    comparison_table.insert(4, "Submission Date", submission_date)
    return comparison_table


def comparison(tutor, student):
    """
    :param tutor: the vectorized tutor table
    :param student: the vecotrized student table
    :return: the df with rating, student name, tutor name, student email, and tutor email
    """
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    rating_list = []
    tutor_list = []
    student_list = []
    Monday = []
    Tuesday = []
    Wednesday = []
    Thursday = []
    Friday = []
    Saturday = []
    Sunday = []
    tutor_email = []
    student_email = []
    tutor_language = []
    student_language = []
    tutor_interst = []
    student_interest = []

    for j in range(0, len(student)):
        for l in range(0, len(tutor)):
            rating = 0
            for k in range(0, len(days)):
                temp_vector = []
                for m in range(0, len(tutor[days[k]][l])):
                    for n in range(0, len(student[days[k]][j])):
                        if student[days[k]][j] != [0, 0] and tutor[days[k]][
                            l
                        ] != [0, 0]:
                            tutor_start = tutor[days[k]][l][m][0]
                            tutor_end = tutor[days[k]][l][m][1]
                            student_start = student[days[k]][j][n][0]
                            student_end = student[days[k]][j][n][1]
                            if (
                                (tutor_start == student_end)
                                or (tutor_end == student_start)
                                or (
                                    student_start < tutor_start
                                    and student_end < tutor_start
                                )
                                or (
                                    student_start > tutor_start
                                    and student_start > tutor_end
                                )
                                or (
                                    (tutor_start < student_start)
                                    and (tutor_end < student_start)
                                    and (tutor_end < student_end)
                                    and ((student_start - tutor_end) < 1)
                                )
                                or (
                                    (student_start < tutor_start)
                                    and (student_end < tutor_end)
                                    and (tutor_start < student_end)
                                    and ((tutor_start - student_end) < 1)
                                )
                            ):
                                rating += 0
                            else:
                                rating += 1

                                if tutor_start <= student_start:
                                    record_start_time = student_start
                                else:
                                    record_start_time = tutor_start

                                if tutor_end <= student_end:
                                    record_end_time = tutor_end
                                else:
                                    record_end_time = student_end
                                temp_vector.append(
                                    [record_start_time, record_end_time]
                                )

                if k == 0:
                    Monday.append(temp_vector)
                elif k == 1:
                    Tuesday.append(temp_vector)
                elif k == 2:
                    Wednesday.append(temp_vector)
                elif k == 3:
                    Thursday.append(temp_vector)
                elif k == 4:
                    Friday.append(temp_vector)
                elif k == 5:
                    Saturday.append(temp_vector)
                elif k == 6:
                    Sunday.append(temp_vector)
            rating_list.append(rating)
            tutor_list.append(tutor["Name"][l])
            student_list.append(student["Name"][j])
            tutor_email.append(tutor["Email"][l])
            student_email.append(student["Email"][j])
            tutor_language.append(tutor["Language"][l])
            student_language.append(student["Language"][j])
            tutor_interst.append(tutor["Interest"][l])
            student_interest.append(student["Interest"][j])
    d = {
        "Student Name": student_list,
        "Tutor Name": tutor_list,
        "Tutor Language": tutor_language,
        "Student Language": student_language,
        "Tutor Interest": tutor_interst,
        "Student Interest": student_interest,
        "Rating": rating_list,
        "Monday": Monday,
        "Tuesday": Tuesday,
        "Wednesday": Wednesday,
        "Thursday": Thursday,
        "Friday": Friday,
        "Saturday": Saturday,
        "Sunday": Sunday,
        "Student Email": student_email,
        "Tutor Email": tutor_email,
    }
    df = pd.DataFrame(data=d)

    return df


def check(df, student_name_list):
    # Step 0: Make sure all students have pairing
    need_to_ask_for_availability = []
    for s in range(0, len(student_name_list)):
        student_df = df[df["Student Name"].isin([student_name_list[s]])]
        if sum(student_df["Rating"]) == 0:
            need_to_ask_for_availability.append(student_name_list[s])
    return need_to_ask_for_availability


def unique(list):
    unique_list = []
    for x in list:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def match(df):
    # Clean up df
    # Step 1: Make sure student with ELL needs match with tutor who speak that - first round of pairing
    # 1.1 select the language student
    language_students = df[df["Student Language"] != "English"]
    language_students = language_students[
        language_students["Student Language"]
        == language_students["Tutor Language"]
    ]
    # Selecting necessary list
    language_need_student_list = unique(list(language_students["Student Name"]))
    language_list = unique(list(language_students["Student Language"]))
    ranking_total = []
    for ln in range(0, len(language_need_student_list)):
        language_student = language_students[
            language_students["Student Name"].isin(
                [language_need_student_list[ln]]
            )
        ]
        total = sum(language_student["Rating"])
        unique_language = unique(list(language_student["Student Language"]))
        total_vector = [total] * len(
            language_student
        )  # Adjusting vector length
        if len(ranking_total) == 0:
            ranking_total = total_vector
        else:
            ranking_total = ranking_total + total_vector

    language_students.insert(0, "Ranking Total", ranking_total)
    language_students = language_students[language_students["Rating"] != 0]

    # Keep in mind this table only contains the population with language tutors
    # If no pairing is made in this step, it's fine

    # Initializing the vectors
    paired_tutor = []
    paired_student = []
    paired_language = []
    paired_tutor_email = []
    paired_student_email = []
    unpaired_student = []
    unpaired_student_lan = []
    Monday_time = []
    Tuesday_time = []
    Wednesday_time = []
    Thursday_time = []
    Friday_time = []
    Saturday_time = []
    Sunday_time = []
    tutor_interest_fin = []
    student_interest_fin = []

    # ELL Pairing Block
    for lan in range(0, len(language_list)):
        one_language_students = language_students[
            language_students["Student Language"].isin([language_list[lan]])
        ]
        one_language_students["Order"] = one_language_students[
            "Ranking Total"
        ].rank(method="dense", ascending=True)
        one_language_students = one_language_students.sort_values(
            by=["Order"], ascending=True
        )
        unique_student_list = unique(
            list(one_language_students["Student Name"])
        )
        print(
            f"The number of {language_list[lan]} Tutor: {len(unique(list(one_language_students['Tutor Name'])))}"
        )
        print(
            f"The number of {language_list[lan]} Student: {len(unique_student_list)}"
        )
        for ol in range(0, len(unique_student_list)):
            if len(one_language_students) != 0:
                new_unique_student_list = unique(
                    list(one_language_students["Student Name"])
                )
                if unique_student_list[ol] in new_unique_student_list:
                    to_be_paired = one_language_students[
                        one_language_students["Student Name"].isin(
                            [unique_student_list[ol]]
                        )
                    ]
                    to_be_paired["Order_Rating"] = to_be_paired["Rating"].rank(
                        method="dense", ascending=False
                    )
                    to_be_paired = to_be_paired.sort_values(
                        by=["Order_Rating"], ascending=True
                    )
                    to_be_paired = to_be_paired.reset_index(drop=True)
                    tutor_pair = to_be_paired["Tutor Name"][0]
                    Monday_time.append(to_be_paired["Monday"][0])
                    Tuesday_time.append(to_be_paired["Tuesday"][0])
                    Wednesday_time.append(to_be_paired["Wednesday"][0])
                    Thursday_time.append(to_be_paired["Thursday"][0])
                    Friday_time.append(to_be_paired["Friday"][0])
                    Saturday_time.append(to_be_paired["Saturday"][0])
                    Sunday_time.append(to_be_paired["Sunday"][0])
                    tutor_email_i = to_be_paired["Tutor Email"][0]
                    tutor_interest_i = to_be_paired["Tutor Interest"][0]
                    student_interest_i = to_be_paired["Student Interest"][0]
                    # Delete the paired information out of the complete table
                    new_one_language_students = one_language_students[
                        ~one_language_students["Student Name"].isin(
                            [unique_student_list[ol]]
                        )
                    ]
                    new_one_language_students = new_one_language_students[
                        ~new_one_language_students["Tutor Name"].isin(
                            [tutor_pair]
                        )
                    ]
                    # Use these two vectors to move the students/tutors from the entire population table
                    paired_tutor.append(tutor_pair)
                    paired_student.append(unique_student_list[ol])
                    # Additional vectors for final table
                    tutor_interest_fin.append(tutor_interest_i)
                    student_interest_fin.append(student_interest_i)
                    paired_language.append(language_list[lan])
                    paired_tutor_email.append(tutor_email_i)
                    paired_student_email.append(
                        to_be_paired["Student Email"][0]
                    )
                    # Updating the table
                    one_language_students = new_one_language_students
                else:
                    unpaired_student.append(unique_student_list[ol])
                    unpaired_student_lan.append(language_list[lan])
            else:
                unpaired_student.append(unique_student_list[ol])
                unpaired_student_lan.append(language_list[lan])

    ELL_d = {
        "Student": paired_student,
        "Tutor": paired_tutor,
        "Language": paired_language,
        "Student Email": paired_student_email,
        "Tutor Email": paired_tutor_email,
        "Monday": Monday_time,
        "Tuesday": Tuesday_time,
        "Wednesday": Wednesday_time,
        "Thursday": Thursday_time,
        "Friday": Friday_time,
        "Saturday": Saturday_time,
        "Sunday": Sunday_time,
    }

    ELL_df = pd.DataFrame(data=ELL_d)

    ELL_Unpaired = {
        "Student": unpaired_student,
        "Language": unpaired_student_lan,
    }
    ELL_Unpaired_df = pd.DataFrame(data=ELL_Unpaired)

    # Step 2: Remove those student from step 1 in both df and the student name list
    removed_df = df[~df["Student Name"].isin(paired_student)]
    removed_df = removed_df[~removed_df["Tutor Name"].isin(paired_tutor)]
    removed_df = removed_df[removed_df["Rating"] != 0]
    distinct_list_of_student = unique(list(removed_df["Student Name"]))
    removed_df2 = removed_df
    # Initializing vectors
    Monday_time = []
    Tuesday_time = []
    Wednesday_time = []
    Thursday_time = []
    Friday_time = []
    Saturday_time = []
    Sunday_time = []
    unpaired_student = []
    unpaired_student_lan = []
    paired_tutor = []
    paired_student = []
    paired_language = []
    paired_student_email = []
    paired_tutor_email = []
    tutor_interest_fin = []
    student_interest_fin = []

    ranking_total = []
    for ln in range(0, len(distinct_list_of_student)):
        removed_df_student = removed_df[
            removed_df["Student Name"].isin([distinct_list_of_student[ln]])
        ]
        total = sum(removed_df_student["Rating"])
        total_vector = [total] * len(
            removed_df_student
        )  # Adjusting vector length
        if len(ranking_total) == 0:
            ranking_total = total_vector
        else:
            ranking_total = ranking_total + total_vector

    removed_df.insert(0, "Ranking Total", ranking_total)
    removed_df["Order"] = removed_df["Ranking Total"].rank(
        method="dense", ascending=True
    )  # ordering the column so lower ranking total goes first
    removed_df = removed_df.sort_values(by="Order")
    distinct_list_of_student = unique(list(removed_df["Student Name"]))
    # 1.Making sure all student has pairing, student with lower rankings will be ranked first
    for k in range(0, len(distinct_list_of_student)):
        if len(removed_df) != 0:
            new_distinct_list_of_student = unique(
                list(removed_df["Student Name"])
            )
            if distinct_list_of_student[k] in new_distinct_list_of_student:
                # Selecting one student
                to_be_paired = removed_df[
                    removed_df["Student Name"].isin(
                        [distinct_list_of_student[k]]
                    )
                ]
                to_be_paired["Order_Rating"] = to_be_paired["Rating"].rank(
                    method="dense", ascending=False
                )
                to_be_paired = to_be_paired.sort_values(
                    by=["Order_Rating"], ascending=True
                )
                to_be_paired = to_be_paired.reset_index(drop=True)

                for r in range(0, len(to_be_paired)):
                    tutor_pair = to_be_paired["Tutor Name"][r]
                    tutor_email_i = to_be_paired["Tutor Email"][r]
                    tutor_interest_i = to_be_paired["Tutor Interest"][r]
                    student_interest_i = to_be_paired["Student Interest"][r]

                    # Delete the paired information out of the complete table
                    new_removed_df = removed_df[
                        ~removed_df["Student Name"].isin(
                            [distinct_list_of_student[k]]
                        )
                    ]
                    new_removed_df = new_removed_df.reset_index(drop=True)

                    # If repairing all the rating of the previous one, and still cannot ensure everyone is paired, keep the current pairing
                    check_reduction = []
                    for n in range(0, len(new_removed_df)):
                        if new_removed_df["Tutor Name"][n] == tutor_pair:
                            check_reduction.append(
                                new_removed_df["Ranking Total"][n]
                                - new_removed_df["Rating"][n]
                            )

                    if 0 not in check_reduction:
                        new_removed_df = new_removed_df[
                            ~new_removed_df["Tutor Name"].isin([tutor_pair])
                        ]
                        Monday_time.append(to_be_paired["Monday"][r])
                        Tuesday_time.append(to_be_paired["Tuesday"][r])
                        Wednesday_time.append(to_be_paired["Wednesday"][r])
                        Thursday_time.append(to_be_paired["Thursday"][r])
                        Friday_time.append(to_be_paired["Friday"][r])
                        Saturday_time.append(to_be_paired["Saturday"][r])
                        Sunday_time.append(to_be_paired["Sunday"][r])

                        # Use these two vectors to move the students/tutors from the entire population table
                        paired_tutor.append(tutor_pair)
                        paired_student.append(distinct_list_of_student[k])
                        # Additional vectors for final table
                        paired_language.append("English")
                        paired_tutor_email.append(tutor_email_i)
                        paired_student_email.append(
                            to_be_paired["Student Email"][0]
                        )
                        tutor_interest_fin.append(tutor_interest_i)
                        student_interest_fin.append(student_interest_i)
                        # Updating the table
                        removed_df = new_removed_df
                        break
                    elif 0 in check_reduction:
                        pass
            else:
                unpaired_student.append(distinct_list_of_student[k])
                unpaired_student_lan.append("English")
        else:
            unpaired_student.append(distinct_list_of_student[k])
            unpaired_student_lan.append("English")

    Unpaired2 = {"Student": unpaired_student, "Language": unpaired_student_lan}
    Unpaired_df2 = pd.DataFrame(data=Unpaired2)

    Paired_d = {
        "Student": paired_student,
        "Tutor": paired_tutor,
        "Language": paired_language,
        "Student Email": paired_student_email,
        "Tutor Email": paired_tutor_email,
        "Monday": Monday_time,
        "Tuesday": Tuesday_time,
        "Wednesday": Wednesday_time,
        "Thursday": Thursday_time,
        "Friday": Friday_time,
        "Saturday": Saturday_time,
        "Sunday": Sunday_time,
    }

    Paired_df = pd.DataFrame(data=Paired_d)

    return (
        language_list,
        language_students,
        distinct_list_of_student,
        removed_df2,
        ELL_df,
        ELL_Unpaired_df,
        Paired_df,
        Unpaired_df2,
    )


def other_option(
    language_list, language_students, distinct_list_of_student, removed_df2
):
    STUDENT = []
    LANGUAGE = []
    other_option = []

    for lan in range(0, len(language_list)):
        one_language_students = language_students[
            language_students["Student Language"].isin([language_list[lan]])
        ]
        one_language_students["Order"] = one_language_students[
            "Ranking Total"
        ].rank(method="dense", ascending=True)
        one_language_students = one_language_students.sort_values(
            by=["Order"], ascending=True
        )
        unique_student_list = unique(
            list(one_language_students["Student Name"])
        )
        for ol in range(0, len(unique_student_list)):
            indiv_student = one_language_students[
                one_language_students["Student Name"].isin(
                    [unique_student_list[ol]]
                )
            ]
            indiv_student = indiv_student.reset_index(drop=True)
            indiv_option = []
            STUDENT.append(unique_student_list[ol])
            LANGUAGE.append(language_list[lan])
            for indiv in range(0, len(indiv_student)):
                indiv_option.append(indiv_student["Tutor Name"][indiv])
            other_option.append(indiv_option)

    for k in range(0, len(distinct_list_of_student)):
        removed_df2["Order"] = removed_df2["Ranking Total"].rank(
            method="dense", ascending=True
        )
        indiv_student = removed_df2[
            removed_df2["Student Name"].isin([distinct_list_of_student[k]])
        ]
        indiv_student = indiv_student.reset_index(drop=True)
        indiv_option = []
        STUDENT.append(distinct_list_of_student[k])
        LANGUAGE.append("English")
        for indiv in range(0, len(indiv_student)):
            indiv_option.append(indiv_student["Tutor Name"][indiv])
        other_option.append(indiv_option)

    Other_option_d = {
        "Student": STUDENT,
        "Language": LANGUAGE,
        "Other Option": other_option,
    }

    Other_option_df = pd.DataFrame(data=Other_option_d)

    return Other_option_df


def match_with_interest(df):
    # Step 1: Make sure student with ELL needs match with tutor who speak that - first round of pairing
    # 1.1 select the language student
    language_students = df[df["Student Language"] != "English"]
    language_students = language_students[
        language_students["Student Language"]
        == language_students["Tutor Language"]
    ]
    # Selecting necessary list
    language_need_student_list = unique(list(language_students["Student Name"]))
    language_list = unique(list(language_students["Student Language"]))
    ranking_total = []
    for ln in range(0, len(language_need_student_list)):
        language_student = language_students[
            language_students["Student Name"].isin(
                [language_need_student_list[ln]]
            )
        ]
        total = sum(language_student["Rating"])
        unique_language = unique(list(language_student["Student Language"]))
        total_vector = [total] * len(
            language_student
        )  # Adjusting vector length
        if len(ranking_total) == 0:
            ranking_total = total_vector
        else:
            ranking_total = ranking_total + total_vector

    language_students.insert(0, "Ranking Total", ranking_total)
    language_students = language_students[language_students["Rating"] != 0]

    # Keep in mind this table only contains the population with language tutors
    # If no pairing is made in this step, it's fine

    # Initializing the vectors
    paired_tutor = []
    paired_student = []
    paired_language = []
    paired_tutor_email = []
    paired_student_email = []
    unpaired_student = []
    unpaired_student_lan = []
    Monday_time = []
    Tuesday_time = []
    Wednesday_time = []
    Thursday_time = []
    Friday_time = []
    Saturday_time = []
    Sunday_time = []
    tutor_interest_fin = []
    student_interest_fin = []

    # ELL Pairing Block
    for lan in range(0, len(language_list)):
        one_language_students = language_students[
            language_students["Student Language"].isin([language_list[lan]])
        ]
        one_language_students["Order"] = one_language_students[
            "Ranking Total"
        ].rank(method="dense", ascending=True)
        one_language_students = one_language_students.sort_values(
            by=["Order"], ascending=True
        )
        unique_student_list = unique(
            list(one_language_students["Student Name"])
        )

        for ol in range(0, len(unique_student_list)):
            if len(one_language_students) != 0:
                new_unique_student_list = unique(
                    list(one_language_students["Student Name"])
                )
                if unique_student_list[ol] in new_unique_student_list:
                    to_be_paired = one_language_students[
                        one_language_students["Student Name"].isin(
                            [unique_student_list[ol]]
                        )
                    ]
                    to_be_paired["Order_Rating"] = to_be_paired["Rating"].rank(
                        method="dense", ascending=False
                    )
                    to_be_paired = to_be_paired.sort_values(
                        by=["Order_Rating"], ascending=True
                    )
                    to_be_paired = to_be_paired.reset_index(drop=True)
                    tutor_pair = to_be_paired["Tutor Name"][0]
                    Monday_time.append(to_be_paired["Monday"][0])
                    Tuesday_time.append(to_be_paired["Tuesday"][0])
                    Wednesday_time.append(to_be_paired["Wednesday"][0])
                    Thursday_time.append(to_be_paired["Thursday"][0])
                    Friday_time.append(to_be_paired["Friday"][0])
                    Saturday_time.append(to_be_paired["Saturday"][0])
                    Sunday_time.append(to_be_paired["Sunday"][0])
                    tutor_email_i = to_be_paired["Tutor Email"][0]
                    tutor_interest_i = to_be_paired["Tutor Interest"][0]
                    student_interest_i = to_be_paired["Student Interest"][0]
                    # Delete the paired information out of the complete table
                    new_one_language_students = one_language_students[
                        ~one_language_students["Student Name"].isin(
                            [unique_student_list[ol]]
                        )
                    ]
                    new_one_language_students = new_one_language_students[
                        ~new_one_language_students["Tutor Name"].isin(
                            [tutor_pair]
                        )
                    ]
                    # Use these two vectors to move the students/tutors from the entire population table
                    paired_tutor.append(tutor_pair)
                    paired_student.append(unique_student_list[ol])
                    # Additional vectors for final table
                    tutor_interest_fin.append(tutor_interest_i)
                    student_interest_fin.append(student_interest_i)
                    paired_language.append(language_list[lan])
                    paired_tutor_email.append(tutor_email_i)
                    paired_student_email.append(
                        to_be_paired["Student Email"][0]
                    )
                    # Updating the table
                    one_language_students = new_one_language_students
                else:
                    unpaired_student.append(unique_student_list[ol])
                    unpaired_student_lan.append(language_list[lan])
            else:
                unpaired_student.append(unique_student_list[ol])
                unpaired_student_lan.append(language_list[lan])

    # Step 2: Remove those student from step 1 in both df and the student name list
    removed_df = df[~df["Student Name"].isin(paired_student)]
    removed_df = removed_df[~removed_df["Tutor Name"].isin(paired_tutor)]
    removed_df = removed_df[removed_df["Rating"] != 0]
    distinct_list_of_student = unique(list(removed_df["Student Name"]))
    removed_df2 = removed_df
    # Initializing vectors
    Monday_time = []
    Tuesday_time = []
    Wednesday_time = []
    Thursday_time = []
    Friday_time = []
    Saturday_time = []
    Sunday_time = []
    unpaired_student = []
    unpaired_student_lan = []
    paired_tutor = []
    paired_student = []
    paired_language = []
    paired_student_email = []
    paired_tutor_email = []
    tutor_interest_fin = []
    student_interest_fin = []

    ranking_total = []
    for ln in range(0, len(distinct_list_of_student)):
        removed_df_student = removed_df[
            removed_df["Student Name"].isin([distinct_list_of_student[ln]])
        ]
        total = sum(removed_df_student["Rating"])
        total_vector = [total] * len(
            removed_df_student
        )  # Adjusting vector length
        if len(ranking_total) == 0:
            ranking_total = total_vector
        else:
            ranking_total = ranking_total + total_vector

    removed_df.insert(0, "Ranking Total", ranking_total)
    removed_df["Order"] = removed_df["Ranking Total"].rank(
        method="dense", ascending=True
    )  # ordering the column so lower ranking total goes first
    removed_df = removed_df.sort_values(by="Order")
    distinct_list_of_student = unique(list(removed_df["Student Name"]))
    # 1.Making sure all student has pairing, student with lower rankings will be ranked first
    for k in range(0, len(distinct_list_of_student)):
        if len(removed_df) != 0:
            new_distinct_list_of_student = unique(
                list(removed_df["Student Name"])
            )
            if distinct_list_of_student[k] in new_distinct_list_of_student:
                # Selecting one student
                to_be_paired = removed_df[
                    removed_df["Student Name"].isin(
                        [distinct_list_of_student[k]]
                    )
                ]
                to_be_paired["column_c"] = np.where(
                    to_be_paired["Student Interest"]
                    == to_be_paired["Tutor Interest"],
                    to_be_paired["Rating"],
                    to_be_paired["Rating"] + 5,
                )
                to_be_paired["Order_Rating"] = to_be_paired["Rating"].rank(
                    method="dense", ascending=False
                )
                to_be_paired = to_be_paired.sort_values(
                    by=["Order_Rating"], ascending=True
                )
                to_be_paired = to_be_paired.reset_index(drop=True)

                for r in range(0, len(to_be_paired)):
                    tutor_pair = to_be_paired["Tutor Name"][r]
                    tutor_email_i = to_be_paired["Tutor Email"][r]
                    tutor_interest_i = to_be_paired["Tutor Interest"][r]
                    student_interest_i = to_be_paired["Student Interest"][r]

                    # Delete the paired information out of the complete table
                    new_removed_df = removed_df[
                        ~removed_df["Student Name"].isin(
                            [distinct_list_of_student[k]]
                        )
                    ]
                    new_removed_df = new_removed_df.reset_index(drop=True)
                    # If repairing all the rating of the previous one, and still cannot ensure everyone is paired, keep the current pairing
                    check_reduction = []
                    for n in range(0, len(new_removed_df)):
                        if new_removed_df["Tutor Name"][n] == tutor_pair:
                            check_reduction.append(
                                new_removed_df["Ranking Total"][n]
                                - new_removed_df["Rating"][n]
                            )

                    if 0 not in check_reduction:
                        new_removed_df = new_removed_df[
                            ~new_removed_df["Tutor Name"].isin([tutor_pair])
                        ]
                        Monday_time.append(to_be_paired["Monday"][r])
                        Tuesday_time.append(to_be_paired["Tuesday"][r])
                        Wednesday_time.append(to_be_paired["Wednesday"][r])
                        Thursday_time.append(to_be_paired["Thursday"][r])
                        Friday_time.append(to_be_paired["Friday"][r])
                        Saturday_time.append(to_be_paired["Saturday"][r])
                        Sunday_time.append(to_be_paired["Sunday"][r])

                        # Use these two vectors to move the students/tutors from the entire population table
                        paired_tutor.append(tutor_pair)
                        paired_student.append(distinct_list_of_student[k])
                        # Additional vectors for final table
                        paired_language.append("English")
                        paired_tutor_email.append(tutor_email_i)
                        paired_student_email.append(
                            to_be_paired["Student Email"][0]
                        )
                        tutor_interest_fin.append(tutor_interest_i)
                        student_interest_fin.append(student_interest_i)
                        # Updating the table
                        removed_df = new_removed_df
                        break
                    elif 0 in check_reduction:
                        pass
            else:
                unpaired_student.append(distinct_list_of_student[k])
                unpaired_student_lan.append("English")
        else:
            unpaired_student.append(distinct_list_of_student[k])
            unpaired_student_lan.append("English")

    Unpaired2 = {"Student": unpaired_student, "Language": unpaired_student_lan}
    Unpaired_df2 = pd.DataFrame(data=Unpaired2)

    Paired_d = {
        "Student": paired_student,
        "Tutor": paired_tutor,
        "Language": paired_language,
        "Student Email": paired_student_email,
        "Tutor Email": paired_tutor_email,
        "Monday": Monday_time,
        "Tuesday": Tuesday_time,
        "Wednesday": Wednesday_time,
        "Thursday": Thursday_time,
        "Friday": Friday_time,
        "Saturday": Saturday_time,
        "Sunday": Sunday_time,
    }

    Paired_df = pd.DataFrame(data=Paired_d)

    return Paired_df, Unpaired_df2


def clean_up(table_in):
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    for day in days:
        for k in range(0, len(table_in)):
            table_in[day][k] = unique(table_in[day][k])
    return table_in


def time_convert_format(Paired):
    # Converting time format
    Paired2 = Paired.copy()
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    for day in days:
        for i in range(0, len(Paired)):
            store = []
            if len(Paired[day][i]) == 0:
                Paired2[day][i] = " "
            else:
                for ii in range(len(Paired[day][i])):
                    start_hour = math.floor(Paired[day][i][ii][0])
                    end_hour = math.floor(Paired[day][i][ii][1])
                    start_minute = int(
                        (Paired[day][i][ii][0] - start_hour) * 60
                    )
                    end_minute = int((Paired[day][i][ii][1] - end_hour) * 60)

                    if start_minute == 0:
                        start_minute = "00"
                    if end_minute == 0:
                        end_minute = "00"
                    time_converted = f"{str(start_hour)}:{str(start_minute)} ~ {str(end_hour)}:{(end_minute)}"
                    store.append(time_converted)

            Paired2[day][i] = store
    return Paired2


def replace_cell_time(input):
    if len(input) == 0:
        return ""
    else:
        return input


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    args = parser.parse_args()
    tutor_initial_csv = pd.read_csv(args.tutor_csv)
    student_initial_csv = pd.read_csv(args.student_csv)

    # /************************************************ Execution Starts ************************************************
    (
        tutor,
        tutor_name_list,
        tutor_email_list,
        tutor_language_list,
        tutor_interest_list,
        tutor_submission_date,
        tutor_error,
    ) = initial_table(tutor_initial_csv)
    (
        student,
        student_name_list,
        student_email_list,
        student_language_list,
        student_interest_list,
        student_submission_date,
        student_error,
    ) = initial_table(student_initial_csv)

    tutor_comparison_table = vectorize_table(
        tutor,
        tutor_name_list,
        tutor_email_list,
        tutor_language_list,
        tutor_interest_list,
        tutor_submission_date,
    )
    student_comparison_table = vectorize_table(
        student,
        student_name_list,
        student_email_list,
        student_language_list,
        student_interest_list,
        student_submission_date,
    )

    df = comparison(tutor_comparison_table, student_comparison_table)

    student_name_list = unique(list(df["Student Name"]))
    need_to_ask_for_availability = check(df, student_name_list)

    (
        language_list,
        language_students,
        distinct_list_of_student,
        removed_df2,
        ELL_df,
        ELL_Unpaired_df,
        Paired_df,
        Unpaired_df2,
    ) = match(df)

    Paired_interest, Unpaired_interest = match_with_interest(df)
    Other_option_df = other_option(
        language_list, language_students, distinct_list_of_student, removed_df2
    )

    # Output needed:
    Paired = pd.concat([ELL_df, Paired_df])
    Unpaired = pd.concat([ELL_Unpaired_df, Unpaired_df2])
    Paired_Interest = pd.concat([ELL_df, Paired_interest])
    Unpaired_Interest = pd.concat([ELL_Unpaired_df, Unpaired_interest])

    Unpaired_name_list = unique(list(Unpaired["Student"]))
    unpaired_interest_name_list = unique(list(Unpaired_Interest["Student"]))

    lan = []
    for f in range(0, len(Unpaired_name_list)):
        selected = Unpaired[Unpaired["Student"] == Unpaired_name_list[f]]
        selected = selected.reset_index(drop=True)
        if len(selected) != 1:
            temp = []
            for fi in range(0, len(selected)):
                temp.append(selected["Language"][fi])
            lan.append(temp)
        else:
            lan.append(selected["Language"][0])

    Unpaired_df = {"Student": Unpaired_name_list, "Language": lan}
    Unpaired = pd.DataFrame(data=Unpaired_df)

    lan = []
    for f in range(0, len(unpaired_interest_name_list)):
        selected = Unpaired_Interest[
            Unpaired_Interest["Student"] == unpaired_interest_name_list[f]
        ]
        selected = selected.reset_index(drop=True)
        if len(selected) != 1:
            temp = []
            for fi in range(0, len(selected)):
                temp.append(selected["Language"][fi])
            lan.append(temp)
        else:
            lan.append(selected["Language"][0])

    Unpaired_Interest_df = {
        "Student": unpaired_interest_name_list,
        "Language": lan,
    }
    Unpaired_Interest = pd.DataFrame(data=Unpaired_Interest_df)

    Paired = Paired.reset_index(drop=True)
    Unpaired = Unpaired.reset_index(drop=True)
    Paired_Interest = Paired_Interest.reset_index(drop=True)
    Unpaired_Interest = Unpaired_Interest.reset_index(drop=True)

    unpaired_tutor_list = []
    paired_tutors = Paired["Tutor"].tolist()

    # Check for the final time if there is possible re-pairing
    for t in tutor_name_list:
        if t not in paired_tutors:
            unpaired_tutor_list.append(t)

    if len(unpaired_tutor_list) != 0 and len(Unpaired) != 0:
        for i in range(0, len(Unpaired)):
            s_name = Unpaired["Student"][i]
            selected = Other_option_df[Other_option_df["Student"] == s_name]
            option_list = list(selected["Other Option"])[0]
            for k in range(0, len(Paired)):
                tutor_previously_paired = Paired["Tutor"][k]
                if tutor_previously_paired in (option_list):
                    replace_s = Paired["Student"][k]
                    replace_s_options_table = Other_option_df[
                        Other_option_df["Student"] == replace_s
                    ]
                    replace_s_options = list(
                        replace_s_options_table["Other Option"]
                    )[0]
                    for jj in range(0, len(replace_s_options)):
                        maybe_replace_tutor = replace_s_options[jj]
                        if maybe_replace_tutor in unpaired_tutor_list:
                            s_rows = df[df["Student Name"] == s_name]
                            row = s_rows[
                                s_rows["Tutor Name"] == tutor_previously_paired
                            ]
                            Paired["Student"][k] = s_name

                            Paired["Student Email"][k] = list(
                                row["Student Email"]
                            )[0]
                            Paired["Tutor Email"][k] = list(row["Tutor Email"])[
                                0
                            ]
                            Paired["Monday"][k] = replace_cell_time(
                                list(row["Monday"])[0]
                            )
                            Paired["Tuesday"][k] = replace_cell_time(
                                list(row["Tuesday"])[0]
                            )
                            Paired["Wednesday"][k] = replace_cell_time(
                                list(row["Wednesday"])[0]
                            )
                            Paired["Thursday"][k] = replace_cell_time(
                                list(row["Thursday"])[0]
                            )
                            Paired["Friday"][k] = replace_cell_time(
                                list(row["Friday"])[0]
                            )
                            Paired["Saturday"][k] = replace_cell_time(
                                list(row["Saturday"])[0]
                            )
                            Paired["Sunday"][k] = replace_cell_time(
                                list(row["Sunday"])[0]
                            )
                            if (
                                list(row["Tutor Language"])[0]
                                != list(row["Student Language"])[0]
                            ):
                                Paired["Language"][k] = "English"
                            else:
                                Paired["Language"][k] = list(
                                    row["Tutor Language"]
                                )[0]

                            replace_rows = df[df["Student Name"] == replace_s]
                            replace_row = replace_rows[
                                replace_rows["Tutor Name"]
                                == maybe_replace_tutor
                            ]
                            if (
                                list(replace_row["Tutor Language"])[0]
                                != list(replace_row["Student Language"])[0]
                            ):
                                insert_language = "English"
                            else:
                                insert_language = list(
                                    replace_row["Tutor Language"]
                                )[0]

                            new_row = {
                                "Student": replace_s,
                                "Tutor": maybe_replace_tutor,
                                "Language": insert_language,
                                "Student Email": list(
                                    replace_row["Student Email"]
                                )[0],
                                "Tutor Email": list(replace_row["Tutor Email"])[
                                    0
                                ],
                                "Monday": list(replace_row["Monday"])[0],
                                "Tuesday": list(replace_row["Tuesday"])[0],
                                "Wednesday": list(replace_row["Wednesday"])[0],
                                "Thursday": list(replace_row["Thursday"])[0],
                                "Friday": list(replace_row["Friday"])[0],
                                "Saturday": list(replace_row["Saturday"])[0],
                                "Sunday": list(replace_row["Sunday"])[0],
                            }
                            # append row to the dataframe
                            Paired = Paired.append(new_row, ignore_index=True)
                            Unpaired = Unpaired[Unpaired["Student"] != s_name]
                            unpaired_tutor_list.remove(maybe_replace_tutor)
                            break
                break

    Paired2 = time_convert_format(Paired)
    Paired2 = clean_up(Paired2)
    # Paired_Interest2 = time_convert_format(Paired_Interest)
    # Paired_Interest2 = clean_up(Paired_Interest2)

    Paired2.to_csv(args.save_directory + "Paired.csv")
    Unpaired.to_csv(args.save_directory + "Unpaired.csv")
    # Paired_Interest2.to_csv()
    # Unpaired_Interest.to_csv()
    df.to_csv(args.save_directory + "available_times.csv")
    Other_option_df.to_csv(args.save_directory + "tutor_options_per_students.csv")
    # Other_option_df: show all the other pairing options.
    # If a student is ELL student, both English and that language would show up if initial pairing was unsuccessful.
    # Other_option_df needs to be used with df if more information is needed.

    print('---------------------Ignore Warnings above---------------------')
    print(f"Woohoo! We paired {len(Paired2)} students and tutors. The information is in Paired.csv")
    print(f"This is the list of unpaired tutors: {unpaired_tutor_list}")
    print('Unpaired students are in Unpaired.csv. Other csv might be helpful for repairing.')

    # ************************************************ Execution Ends ************************************************/
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
