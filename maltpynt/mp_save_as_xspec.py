# Licensed under a 3-clause BSD style license - see LICENSE.rst

from __future__ import (absolute_import, unicode_literals, division,
                        print_function)

from .mp_io import mp_get_file_type
import numpy as np
from .mp_io import mp_get_file_extension
import subprocess as sp


def mp_save_as_xspec(fname, direct_save=False):
    ftype, contents = mp_get_file_type(fname)

    outroot = fname.replace(mp_get_file_extension(fname), '')
    outname = outroot + '_xsp.dat'

    if 'freq' in list(contents.keys()):
        freq = contents['freq']
        pds = contents[ftype]
        epds = contents['e' + ftype]
        df = freq[1] - freq[0]

        np.savetxt(outname, np.transpose([freq - df / 2,
                                          freq + df / 2,
                                          pds.real * df,
                                          epds * df]))
    elif 'flo' in list(contents.keys()):
        ftype = ftype.replace('reb', '')
        flo = contents['flo']
        fhi = contents['fhi']
        pds = contents[ftype]
        epds = contents['e' + ftype]
        df = fhi - flo
        np.savetxt(outname, np.transpose([flo, fhi,
                                          pds.real * df,
                                          epds * df]))
    else:
        raise Exception('File type not recognized')

    if direct_save:
        sp.check_call('flx2xsp {} {}.pha {}.rsp'.format(
            outname, outroot, outroot).split())


if __name__ == '__main__':
    import sys

    print('Calling script...')

    args = sys.argv[1:]

    sp.check_call(['MP2xspec'] + args)
