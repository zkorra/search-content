import requests
import numpy as np
import pandas as pd
import datetime
from dateutil.parser import parse
import tldextract
import json
from dataframe_cleaner import replace_basic_columns


def clean_course_dataframe(dataframe):

    dataframe = replace_basic_columns(dataframe)

    dataframe_export = dataframe[[
        'title',
        'description',
        'url',
        'image',
        'meta_site_name',
        'meta_type',
        'udemy_category',
        # 'udemy_instructor',
        'udemy_price'
    ]]

    return dataframe_export


def filter_course_property(data):

    dataframe = pd.DataFrame(columns=[
        'cse_title',
        'cse_description',
        'url',
        'cse_image',
        'meta_title',
        'meta_description',
        'meta_url',
        'meta_image',
        'meta_site_name',
        'meta_type',
        'udemy_category',
        'udemy_instructor',
        'udemy_price'
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
            url = result_item.get("link")
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
            # get meta website name
            meta_site_name = metatags.get("og:site_name", "")
            #
            # get meta article type
            meta_type = metatags.get("og:type", "")
            #
            # get category from udemy
            udemy_category = metatags.get("udemy_com:category", "")
            #
            # get instructor from udemy
            udemy_instructor = metatags.get("udemy_com:instructor", "")
            #
            # get price from udemy
            udemy_price = metatags.get("udemy_com:price", "")

            row = {
                'cse_title': cse_title,
                'cse_description': cse_description,
                'url': url,
                'cse_image': cse_image,
                'meta_title': meta_title,
                'meta_description': meta_description,
                'meta_url': meta_url,
                'meta_image': meta_image,
                'meta_site_name': meta_site_name,
                'meta_type': meta_type,
                'udemy_category': udemy_category,
                'udemy_instructor': udemy_instructor,
                'udemy_price': udemy_price
            }

            dataframe = dataframe.append(row, ignore_index=True)

        cleaned_course = clean_course_dataframe(dataframe)

    return cleaned_course.to_json(orient='records')
