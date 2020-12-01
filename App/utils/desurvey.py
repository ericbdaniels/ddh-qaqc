import numpy as np
import pandas as pd


def tangent_desurvey(length: float, azimuth: float, dip: float):
    """Basic tangent desurvey method

    Args:
        length (float): distance between survey pts
        azimuth (float): azimuth (degrees)
        dip (float): dip (degrees)

    Returns:
        tuple: x,y,z coordinates
    """
    rad_az = np.deg2rad(azimuth)
    rad_dip = np.deg2rad(90 - dip)
    x = length * np.cos(rad_az) * np.sin(rad_dip)
    y = length * np.sin(rad_az) * np.sin(rad_dip)
    z = length * np.cos(rad_dip)
    return x, y, z


def mincurve_desurvey(
    length: float, azm1: float, dip1: float, azm2: float, dip2: float
):
    """Desurvey interval by minimum curvature
        This code praphrased from: Adrian Martinez Vargas OPENGEOSTAT

    Args:
        length (float): distance between survey pts
        azm1 (float): azimuth, top of interval (degrees)
        dip1 (float): dip, top of interval (degrees)
        azm2 (float): azimuth, bottom of interval (degrees)
        dip2 (float): dip, bottom of interval (degrees)

    Returns:
        tuple: x,y,z coordinates
    """

    i1 = np.deg2rad(90 - dip1)
    a1 = np.deg2rad(azm1)

    i2 = np.deg2rad(90 - dip2)
    a2 = np.deg2rad(azm2)

    # calculate the dog-leg (dl) and the Ratio Factor (rf)
    dl = np.arccos(np.cos(i2 - i1) - np.sin(i1) * np.sin(i2) * (1 - np.cos(a2 - a1)))

    if dl != 0.0:
        rf = 2 * np.tan(dl / 2) / dl  # minimum curvature
    else:
        rf = 1  # balanced tangential

    z = 0.5 * length * (np.cos(i1) + np.cos(i2)) * rf
    y = 0.5 * length * (np.sin(i1) * np.cos(a1) + np.sin(i2) * np.cos(a2)) * rf
    x = 0.5 * length * (np.sin(i1) * np.sin(a1) + np.sin(i2) * np.sin(a2)) * rf

    return x, y, z


def desurvey(survey, collar, interp_type="mincurve"):
    def get_coords(row):
        if np.isnan(row.length):
            icollar = collar[collar.DHID == row.DHID]
            return {
                "dhid": row.DHID,
                "x": icollar.X.values[0],
                "y": icollar.Y.values[0],
                "z": icollar.Z.values[0],
            }
        else:
            if interp_type == "mincurve":
                x, y, z = mincurve_desurvey(
                    row.length, row.AZIMUTH, row.DIP, row.AZIMUTH2, row.DIP2
                )
                return {"dhid": row.DHID, "x": x, "y": y, "z": -z}
            elif interp_type == "tangent":
                x, y, z = tangent_desurvey(row.length, row.AZIMUTH, row.DIP)
                return {"dhid": row.DHID, "x": x, "y": y, "z": -z}
            else:
                raise ValueError(f"Invalid interpolation method: {interp_type}")

    bhid_groups = survey.groupby("DHID")
    survey["length"] = bhid_groups["DEPTH"].diff()
    survey["AZIMUTH2"] = bhid_groups["AZIMUTH"].shift(1)
    survey["DIP2"] = bhid_groups["DIP"].shift(1)
    coords = survey.apply(get_coords, axis=1, result_type="expand")
    coords["z"] = coords.groupby("dhid")["z"].cumsum()
    return coords