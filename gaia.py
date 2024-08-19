from astroquery.gaia import Gaia
from selenium import webdriver
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--pos', type=str, help= "Position RA/Dec h:m:s<space>d:m:s as a single string")
args = parser.parse_args()

if args.pos==True: 
    pos = args.pos
else:
    raise ValueError("Give position RA/Dec h:m:s<space>d:m:s as a single string")

#pos='0:31:23.6938 +46:06:06.951'

def convert(pos):

    RA,Dec=pos.split()
    
    hms=[float(i) for i in RA.split(':')]
    ra= 15*(hms[0]+hms[1]/60+hms[2]/3600)

    dms=[float(i) for i in Dec.split(':')]
    if dms[0]>0:
        dec= dms[0]+dms[1]/60+dms[2]/3600
    else:
        dec = dms[0]-(float(dms[1])/60)-(float(dms[2])/3600)
    return ra,dec

def query(pos):

    query = ('''
    SELECT top 5 ra,dec,pm,parallax,in_galaxy_candidates,in_qso_candidates,DISTANCE(
        POINT'''+str(pos)+''',
        POINT(ra, dec)) AS ang_sep
    FROM gaiadr3.gaia_source
    WHERE 1 = CONTAINS(
    POINT'''
    +str(pos)+
    ''',
    CIRCLE(ra, dec, 1))
    ORDER BY ang_sep ASC
    ''')
    
    job = Gaia.launch_job_async(query)
    r = job.get_results()

    return r

def search_ned(pos):

    '''
    Search the NED Database for objects within 3 as
    '''
    
    ra,dec=pos
    driver = webdriver.Firefox()
    driver.get('https://ned.ipac.caltech.edu/conesearch?search_type='+
            'Near%20Position%20Search&in_csys=Equatorial'
            '&in_equinox=J2000&ra='+str(np.round(ra,4))+'d&dec='+str(np.round(dec,4))+'d&radius=0.05')

pos=convert(pos)
table=query(pos)
candidates=table[table['in_galaxy_candidates']==True]
candidates['dist(kpc)']=1/candidates['parallax']
candidates.pprint()

if len(candidates)>1:
    print('Multiple galaxy candidates found, reduce search radius.')
    exit()

response=input('Proceed with this candidate?y/n')

if response=='y':
    print(pos)
    search_ned(pos)
