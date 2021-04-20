import numpy as np
import pandas as pd
from dateutil.parser import parse
import tldextract


def replace_basic_columns(dataframe):

    pd.set_option('mode.chained_assignment', None)

    dataframe["title"] = np.nan
    dataframe["description"] = np.nan
    dataframe["image"] = np.nan

    for index in dataframe.index:

        if(pd.isnull(dataframe['meta_title'][index])):
            dataframe['title'][index] = dataframe['cse_title'][index]
        else:
            dataframe['title'][index] = dataframe['meta_title'][index]

        if(pd.isnull(dataframe['meta_description'][index])):
            dataframe['description'][index] = dataframe['cse_description'][index]
        else:
            dataframe['description'][index] = dataframe['meta_description'][index]

        if(pd.isnull(dataframe['meta_site_name'][index])):
            dataframe['meta_site_name'][index] = tldextract.extract(
                dataframe['url'][index]).domain.capitalize()

        if(pd.isnull(dataframe['meta_image'][index])):
            dataframe['image'][index] = dataframe['cse_image'][index]
        else:
            dataframe['image'][index] = dataframe['meta_image'][index]
            # if(dataframe_new['image'][index][0] == '/' and dataframe_new['image'][index][1] == '/'):
            #     dataframe_new['image'][index] = dataframe_new['image'][index].replace(
            #         "//", "https://")

    return dataframe


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def replace_published_date(dataframe):

    pd.set_option('mode.chained_assignment', None)

    month_dict = {
        "ม.ค.": "Jan",
        "ก.พ.": "Feb",
        "มี.ค.": "Mar",
        "เม.ย.": "Apr",
        "พ.ค.": "May",
        "มิ.ย.": "Jun",
        "ก.ค.": "Jul",
        "ส.ค.": "Aug",
        "ก.ย.": "Sep",
        "ต.ค.": "Oct",
        "พ.ย.": "Nov",
        "ธ.ค.": "Dec",
    }

    dataframe["date"] = np.nan

    dataframe['meta_article_published_time'] = pd.to_datetime(
        dataframe['meta_article_published_time'], format='%Y-%m-%d %H:%M:%S', utc=True).dt.strftime('%d/%m/%Y')

    for index in dataframe.index:

        if(pd.isnull(dataframe['meta_article_published_time'][index])):
            date = dataframe['cse_description'][index].split(' ... ')[
                0]
            for word, initial in month_dict.items():
                date = date.replace(word, initial)
            if is_date(date):
                dataframe['date'][index] = date
            else:
                dataframe['date'][index] = np.nan
        else:
            dataframe['date'][index] = dataframe['meta_article_published_time'][index]

    dataframe['date'] = pd.to_datetime(
        dataframe['date']).dt.strftime('%d/%m/%Y')

    return dataframe
