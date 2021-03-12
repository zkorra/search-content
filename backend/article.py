import requests
import numpy as np
import pandas as pd
import datetime
from dateutil.parser import parse
import tldextract


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


def cleanArticles(dataframe):

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

    dataframe["title"] = np.nan
    dataframe["description"] = np.nan
    dataframe["image"] = np.nan
    dataframe["date"] = np.nan

    dataframe['meta_article_published_time'] = pd.to_datetime(
        dataframe['meta_article_published_time'], format='%Y-%m-%d %H:%M:%S', utc=True).dt.strftime('%d/%m/%Y')

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
                dataframe_new['cse_url'][index]).domain.capitalize()

        # if(pd.isnull(dataframe_new['meta_image'][index])):
        #     dataframe_new['image'][index] = dataframe_new['cse_image'][index]
        # else:
        #     dataframe_new['image'][index] = dataframe_new['meta_image'][index]
        #     if(dataframe_new['image'][index][0] == '/' and dataframe_new['image'][index][1] == '/'):
        #         dataframe_new['image'][index] = dataframe_new['image'][index].replace(
        #             "//", "https://")

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

    dataframe_export = dataframe[[
        'title',
        'description',
        'cse_url',
        'image',
        'date',
        'meta_article_author',
        'meta_author',
        'meta_section',
        'meta_site_name',
        'meta_type']]

    return dataframe_export


def getArticles(data):

    dataframe = pd.DataFrame(columns=[
        'cse_title',
        'cse_description',
        'cse_url',
        'cse_image',
        'meta_title',
        'meta_description',
        'meta_url',
        'meta_image',
        'meta_article_published_time',
        'meta_article_author',
        'meta_author',
        'meta_section',
        'meta_site_name',
        'meta_type',
    ])

    # get the result items
    result_items = data.get("items")

    if result_items:
        # iterate over 10 results found
        for i, result_item in enumerate(result_items, start=1):

            pagemap = result_item.get("pagemap")
            metatags = pagemap.get("metatags")[0]

            # get the page title
            cse_title = result_item.get("title")
            #
            # page snippet
            cse_description = result_item.get("snippet")
            #
            # extract the page url
            cse_url = result_item.get("link")
            #
            # extract image url if exists
            if "cse_image" in pagemap:
                cse_image = pagemap.get("cse_image")[0].get("src")
            else:
                cse_image = ""
            #
            # get meta title
            meta_title = metatags.get("og:title", "")
            #
            # get meta description
            meta_description = metatags.get("og:description", "")
            #
            # get meta url
            meta_url = metatags.get("og:url", "")
            #
            # get meta image url
            meta_image = metatags.get("og:image", "")
            #
            # get meta publish time
            meta_article_published_time = metatags.get(
                "article:published_time", "")
            #
            # get meta author
            meta_article_author = metatags.get("article:author", "")
            #
            # get meta author
            meta_author = metatags.get("author", "")
            #
            # get meta article section
            meta_section = metatags.get("article:section", "")
            #
            # get meta website name
            meta_site_name = metatags.get("og:site_name", "")
            #
            # get meta article type
            meta_type = metatags.get("og:type", "")

            row = {
                'cse_title': cse_title,
                'cse_description': cse_description,
                'cse_url': cse_url,
                'cse_image': cse_image,
                'meta_title': meta_title,
                'meta_description': meta_description,
                'meta_url': meta_url,
                'meta_image': meta_image,
                'meta_article_published_time': meta_article_published_time,
                'meta_article_author': meta_article_author,
                'meta_author': meta_author,
                'meta_section': meta_section,
                'meta_site_name': meta_site_name,
                'meta_type': meta_type,
            }

            dataframe = dataframe.append(row, ignore_index=True)

        cleanedDataframe = cleanArticles(dataframe)

    return cleanedDataframe.to_json(orient='records')
