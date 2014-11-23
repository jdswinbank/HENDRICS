from __future__ import division, print_function
import argparse
from mp_io import mp_save_data, mp_get_file_type
import numpy as np


def sum_fspec(files, outname=None):
    '''Takes a bunch of (C)PDSs and sums them'''

    # Read first file
    ftype0, contents = mp_get_file_type(args.files[0])
    pdstype = ftype0.replace('reb', '')
    freq0 = contents['freq']
    pds0 = contents[pdstype]
    epds0 = contents['e' + pdstype]
    nchunks0 = contents['n' + pdstype]
    rebin0 = contents['rebin']
    norm0 = contents['norm']

    tot_pds = pds0 * nchunks0
    tot_epds = epds0 ** 2 * nchunks0
    tot_npds = nchunks0
    tot_contents = contents.copy()
    if outname is None:
        outname = 'tot_' + ftype0 + '.p'

    for f in args.files[1:]:
        ftype, contents = mp_get_file_type(f)
        pdstype = ftype.replace('reb', '')
        freq = contents['freq']
        pds = contents[pdstype]
        epds = contents['e' + pdstype]
        nchunks = contents['n' + pdstype]
        rebin = contents['rebin']
        norm = contents['norm']

        assert ftype == ftype0, 'Files must all be of the same kind'
        assert np.all(rebin == rebin0), \
            'Files must be rebinned in the same way'
        assert (np.all(freq == freq0)), 'Frequencies must coincide'
        assert norm == norm0, 'Files must have the same normalization'

        tot_pds += pds * nchunks
        tot_epds += epds ** 2 * nchunks ** 2
        tot_npds += nchunks

    tot_contents[pdstype] = tot_pds / tot_npds
    tot_contents['e' + pdstype] = np.sqrt(tot_epds) / tot_npds
    tot_contents['n' + pdstype] = tot_npds

    print ('Saving %s to %s' % (pdstype, outname))
    mp_save_data(tot_contents, open(outname, 'wb'), ftype)

    return tot_contents


if __name__ == '__main__':
    description = 'Sums (C)PDSs contained in different files'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("files", help="List of light curve files", nargs='+')

    parser.add_argument("-o", "--outname", type=str, default=None,
                        help='Output file name for summed (C)PDS. Default:' +
                        ' tot_(c)pds.p')

    args = parser.parse_args()

    sum_fspec(args.files, args.outname)
