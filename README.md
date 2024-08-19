# File Descriptions 

### 15dg_Spectra.ipynb
Spectra(not flux calibrated)  in the two filters compared to skymodel.

### SExtractor_S240615dg.ipynb
Crossmatch of XRay Candidate Counterparts with WFI Images within 90% error region and lightcurves generated.

### gaia.py 
Queries Gaia Database for Galaxies/QSOs within a search region(needs to be edited in line 42), and if found, gets details from NASA Extragalactic Database within a 3'' radius. <br>
Run, for example, `python3 gaia.py --pos 'h:m:s d:m:s'`

### z_Matched_Filtering.ipynb
Matched filtering HET spectrum with spectral lines(e.g. O-II) from templates for confirming photo-z.

### z_overplot_spectra(1).ipynb
Redshift confirmation by `specutils` line finding and by overplotting templates.
