import numpy as np
import pandas as pd
from common.dataframe_preparation.common_cleaner import replace_basic_columns, replace_published_date


def clean_article_dataframe(dataframe):

    dataframe = replace_basic_columns(dataframe)

    dataframe = replace_published_date(dataframe)

    dataframe['title'].replace('', np.nan, inplace=True)

    dataframe = dataframe.dropna(subset=['title'])

    dataframe.rename(
        columns={
            'cse_url': 'url',
            'meta_author': 'author',
            'meta_site_name': 'sitename',
            'meta_type': 'type'
        },
        inplace=True
    )

    dataframe_export = dataframe[[
        'title',
        'description',
        'url',
        'image',
        'date',
        'author',
        'sitename',
        'type']]

    return dataframe_export


def filter_article_property(data):

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
            meta_author = metatags.get("author", "")
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
                'meta_author': meta_author,
                'meta_site_name': meta_site_name,
                'meta_type': meta_type,
            }

            dataframe = dataframe.append(row, ignore_index=True)

        cleaned_article = clean_article_dataframe(dataframe)

    return cleaned_article.to_json(orient='records')
