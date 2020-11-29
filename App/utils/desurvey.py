import numpy as np


def simple_desurvey(depth, azimuth, dip):
    rad_az = np.deg2rad(azimuth)
    rad_dip = np.deg2rad(90 - dip)
    x = depth * np.cos(rad_az) * np.sin(rad_dip)
    y = depth * np.sin(rad_az) * np.sin(rad_dip)
    z = depth * np.cos(rad_dip)
    return x, y, z


def mincurve_desurvey(len12: float, azm1: float, dip1: float, azm2: float, dip2: float):

    """
    THIS CODE FROM : Adrian Martinez Vargas OPENGEOSTAT

    dsmincurb(len12, azm1, dip1, azm2, dip2)

    Desurvey one interval with minimum curvature

    Given a line with length ``len12`` and endpoints p1,p2 with
    direction angles ``azm1, dip1, azm2, dip2``, this function returns
    the differences in coordinate ``dz,dn,de`` of p2, assuming
    p1 with coordinates (0,0,0)

    Parameters
    ----------
    len12, azm1, dip1, azm2, dip2: float
        len12 is the length between a point 1 and a point 2.
        azm1, dip1, azm2, dip2 are direction angles azimuth, with 0 or
        360 pointing north and dip angles measured from horizontal
        surface positive downward. All these angles are in degrees.


    Returns
    -------
    out : tuple of floats, ``(dz,dn,de)``
        Differences in elevation, north coordinate (or y) and
        east coordinate (or x) in an Euclidean coordinate system.

    See Also
    --------
    ang2cart,

    Notes
    -----
    The equations were derived from the paper:
        http://www.cgg.com/data//1/rec_docs/2269_MinimumCurvatureWellPaths.pdf

    The minimum curvature is a weighted mean based on the
    dog-leg (dl) value and a Ratio Factor (rf = 2*tan(dl/2)/dl )
    if dl is zero we assign rf = 1, which is equivalent to  balanced
    tangential desurvey method. The dog-leg is zero if the direction
    angles at the endpoints of the desurvey intervals are equal.

    Example
    --------

    >>> dsmincurb(len12=10, azm1=45, dip1=75, azm2=90, dip2=20)
    (7.207193374633789, 1.0084573030471802, 6.186459064483643)

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

    z = 0.5 * len12 * (np.cos(i1) + np.cos(i2)) * rf
    y = 0.5 * len12 * (np.sin(i1) * np.cos(a1) + np.sin(i2) * np.cos(a2)) * rf
    x = 0.5 * len12 * (np.sin(i1) * np.sin(a1) + np.sin(i2) * np.sin(a2)) * rf

    return x, y, z
