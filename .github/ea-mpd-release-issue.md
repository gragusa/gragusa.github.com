The ECB's EA-MPD workbook (https://www.ecb.europa.eu/pub/pdf/annex/Dataset_EA-MPD.xlsx) has a Last-Modified date (in the title) that differs from the one recorded in `factors/ea-mpd-last-modified.txt`.

To publish a new vintage:

1. In mpfactors, run `rotate_script.jl` (it downloads the workbook), then `04factor_plots.R`.
2. Copy the new files from `rotated_factors/` and `surprise_data/` into `factors/data/`.
3. Run `python3 scripts/check-ea-mpd.py --record`.
4. Commit and push. A commit message with `Closes #N`, where N is this issue's number, closes it.

If the release does not call for a new vintage, do steps 3 and 4 only.

This check runs every Monday. It opens a new issue as long as the recorded date differs from the ECB's.
