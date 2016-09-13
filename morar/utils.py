import numpy as np
import pandas as pd
from sklearn.preprocessing import Imputer

"""
Utility functions
"""

def get_featuredata(data, metadata_string="Metadata", prefix=True):
    """
    identifies columns in a dataframe that are not labelled with the
    metadata prefix. Its assumed everything not labelled metadata is
    featuredata

    Parameters
    ----------

    data : pandas DataFrame
        DataFrame

    metadata_string : string (default="Metadata")
        string that denotes a column is a metadata column

    prefix: boolean (default=True)
        if True, then only columns that are prefixed with metadata_string are
        selected as metadata. If False, then any columns that contain the
        metadata_string are selected as metadata columns

    Returns
    -------
    f_cols : list
        List of feature column labels
    """
    if prefix:
        f_cols = [i for i in data.columns if not i.startswith(metadata_string)]
    elif prefix == False:
        f_cols = [i for i in data.columns if metadata_string not in i]
    return f_cols


def get_metadata(data, metadata_string="Metadata", prefix=True):
    """
    identifies column in a dataframe that are labelled with the metadata_prefix

    Parameters
    ----------
    data : pandas DataFrame
        DataFrame

    metadata_string : string (default="Metadata")
        string that denotes a column is a metadata column

    prefix: boolean (default=True)
        if True, then only columns that are prefixed with metadata_string are
        selected as metadata. If False, then any columns that contain the
        metadata_string are selected as metadata columns

    Returns
    -------
    m_cols : list
        list of metadata column labels
    """
    if prefix:
        m_cols = [i for i in data.columns if i.startswith(metadata_string)]
    elif prefix is False:
        m_cols = [i for i in data.columns if metadata_string in i]
    return m_cols



def is_all_nan(data):
    """
    Returns column name if all values in that column are np.nan

    Parameters
    ----------
    df : pandas DataFrame
        DataFrame

    Returns
    -------
    out_cols : list
        column names containing all np.nan values
    """
    is_null = data.isnull().sum()
    nrows = data.shape[0]
    out_cols = []
    for i in is_null.index:
        if is_null[i] == nrows:
            out_cols.append(i)
    return out_cols


def get_image_quality(data):
    """
    Returns list of column names from the CelLProfiler ImageQuality module
    that are present in df.

    Parameters
    ----------
    data : pandas DataFrame
        DataFrame

    Returns
    -------
    im_qc_cols : list
        list of ImageQuality columns contained in df
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("not a pandas DataFrame")
    colnames = data.columns.tolist()
    im_qc_cols = [col for col in colnames if "ImageQuality" in col]
    if len(im_qc_cols) == 0:
        raise ValueError("no ImageQuality measurements found")
    else:
        return im_qc_cols


def impute(data, method="median", **kwargs):
    """
    Impute missing feature values by using the feature average.

    Parameters
    ----------
    data : pandas DataFrame
        DataFrame
    method : string (default="median")
        method with which to calculate the feature average. Options: "mean",
        "median".
    **kwargs : additional args to utils.get_metadata / utils.get_featuredata
        and sklearn.preprocessing.Imputer

    Returns
    -------
    data_out : pandas DataFrame
        DataFrame with imputed missing values
    """
    imp = Imputer(strategy=method, **kwargs)
    data_feature = data[get_featuredata(data, **kwargs)].copy()
    imputed_data = imp.fit_transform(data_feature)
    data[get_featuredata(data, **kwargs)] = imputed_data
    return data