# Module Overview

## `analysis.py` - Contains LPC Analysis Functions
- `arburg_vector()` - Single signal LPC analysis
- `arburg_matrix()` - Multiple signal LPC analysis
- `arburg_warped_vector()` - Frequency warped LPC for single signal
- `arburg_warped_matrix()` - Frequency warped LPC for multiple signals

## `synthesis.py` - Contains Signal Generation
- `gen_ts()` - Generate time series using LPC coefficients

## `utils.py` - Contains Utility Functions
- `arcoeff_to_cep()` - Convert LPC to cepstral coefficients
- `cep_to_arcoeff()` - Convert cepstral back to LPC coefficients
- `freqz()` - Calculate frequency response
- `arcoeff_warp()` - Warp LPC coefficients
