import bpdb
"""

Initial exploration into the sample data provided by the competition.

"""

import os
from typing import List
from typing import Dict

import pandas as pd


def main():
    data_folder = "sample_data/"

    news_data_df = pd.read_csv(os.path.join(data_folder, "news_sample.csv"))
    market_data_df = pd.read_csv(os.path.join(data_folder, "marketdata_sample.csv"))

    news_data_df["assetCodes"] = convert_asset_codes(news_data_df["assetCodes"])
    asset_code_map = create_asset_code_map(news_data_df["assetCodes"])
    bpdb.set_trace()  # ------------------------------ Breakpoint ------------------------------ #
    pass


def convert_asset_codes(codes_series):
    """ This will convert the asset codes

    :param codes_series: this is a pandas.Series in which each element is
        a list of asset codes
    """
    from ast import literal_eval
    codes_series = codes_series.map(literal_eval)
    return codes_series


def create_asset_code_map(codes_series: pd.Series) -> Dict[str, List[int]]:
    """ This will create a mapping from asset code to index of data series
        that contain the asset-code.

    :param codes_series: this is a pandas.Series in which each element is
        a list of asset codes
    """
    asset_code_map = dict()

    for ind, asset_codes in enumerate(codes_series):
        for asset_code in asset_codes:
            asset_code_map.setdefault(asset_code, []).append(ind)
    return asset_code_map


# TODO:
def conform_dataframe_for_candleplot():
    pass


if __name__ == "__main__":
    main()
