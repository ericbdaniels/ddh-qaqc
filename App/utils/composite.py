import numpy as np
import pandas as pd


def composite(ifrom, ito, values, comp_length=1.0, min_comp_length=-1.0):
    """
    cfrom,cto,clen,cvar,cacum= composite(ifrom, ito, values,
                                        comp_length = 1, min_comp_length=-1)

    Composite intervals in a single drillhole. The From-To
    intervals may be sorted.

    Parameters
    ----------
    ifrom, ito:     1D arrays of floats
        From - To  interval
    values :   1D array of floats/integers
        variable,
    comp_length: Optional, float, default 1.
        length of the compositing intervals
    min_comp_length: Optional, float, defaul -1.
        minimum length of the composite, if <=0 then min_comp_length = comp_length/2.

    Return
    -------
    (cfrom, cto, clen, cvar, cacum)
    cfrom, cto:  1D arrays of floats
         From, To composited intervals
    clen, cvar, cacum:  1D arrays of floats
         total length of intervals composited
         variable composited
         variable accumulated

    """

    assert ifrom.shape == ito.shape, "Error: ifrom and ito with different shape"
    assert all(ifrom < ito), "Error: ifrom >= ito, wrong or zero length intervals"
    assert all(np.isfinite(ifrom)), "Error: ifrom with not finite elements"
    assert all(np.isfinite(ito)), "Error: ito with not finite elements"

    if min_comp_length <= 0:
        min_comp_length = comp_length / 2.0

    ncomp = int(ito[-1] / comp_length + 1)
    nintrb = len(ifrom)

    # create the composite arrays
    cfrom = np.arange(0.0, ito[-1] + comp_length, comp_length)
    cto = cfrom + comp_length
    clen = np.zeros(cto.shape)
    cvar = np.zeros(cto.shape)
    cvar[:] = np.nan
    cacum = np.zeros(cto.shape)

    iprop = np.zeros(ito.shape)

    # for each composite
    for i in range(ncomp):

        # initialize proportions
        iprop[:] = 0

        # for each interval
        for l in range(nintrb):

            # ignore interval if variable is nan
            if np.isnan(values[l]):
                continue

            # case a, below the composite
            if ifrom[l] >= cto[i]:
                break

            # case b, over the composite
            if ito[l] <= cfrom[i]:
                continue

            # --these are overlap--

            # case overlap top or contained
            if ito[l] > cfrom[i] and ito[l] <= cto[i]:

                # case c, interval in composite
                if ifrom[l] >= cfrom[i]:
                    iprop[l] = ito[l] - ifrom[l]

                # case d, overlap top
                else:
                    iprop[l] = ito[l] - cfrom[i]

            # case e, composite in interval
            if ifrom[l] < cfrom[i] and ito[l] > cto[i]:
                iprop[l] = cto[i] - cfrom[i]
                continue

            # case f, overlap bottom
            if ifrom[l] >= cfrom[i] and ifrom[l] < cto[i] and ito[l] > cto[i]:
                iprop[l] = cto[i] - ifrom[l]
                continue

        clen[i] = np.nansum(iprop)

        if clen[i] > min_comp_length:
            cacum[i] = np.nansum(values * iprop)
            cvar[i] = cacum[i] / clen[i]  # wighted average
        else:
            cvar[i] = np.nan
            cacum[i] = np.nan

    return pd.DataFrame({"from": cfrom, "to": cto, "ilen": clen, "value": cvar})


def composite_dh(dh, comp_len, var_name):
    comps = composite(dh.FROM.values, dh.TO.values, dh[var_name].values, comp_len)
    comps = comps[np.isfinite(comps.value)]
    comps["midpt"] = ((comps["to"] - comps["from"]) / 2) + comps["from"]
    comps["X"] = np.interp(comps.midpt, dh.midpt, dh.X)
    comps["Y"] = np.interp(comps.midpt, dh.midpt, dh.Y)
    comps["Z"] = np.interp(comps.midpt, dh.midpt, dh.Z)
    comps["comp_length"] = comp_len
    comps["var"] = var_name
    return comps.reset_index()
