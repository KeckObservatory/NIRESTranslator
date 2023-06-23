"""
Sets the following detector parameters:
- integration time
- number of coadds
- readout mode (what type of sampling)
- number of samples

Arguments:
- sv (required, enum(s, v, sv) )
- Integration time (optional, float)
- Co-adds (optional, int)
- sampmode (UTR/1, PCDS/2, MCDS/3, Single/4)
- nsamp (optional, int)

Replaces:
tint(s/v)
coadd(s/v)
sampmode(s/v)
nsamp(s/v)
"""