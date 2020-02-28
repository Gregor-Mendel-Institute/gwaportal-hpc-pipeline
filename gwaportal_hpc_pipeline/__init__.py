from .rest import Restclient
import os

HPC_HOST = os.environ['HPC_HOST']
REST_HOST = os.environ['REST_HOST']
REST_USERNAME = os.environ['REST_USERNAME']
REST_PASSWORD = os.environ['REST_PASSWORD']
GENOTYPE_FOLDER = os.environ.get('GENOTYPE','/net/gmi.oeaw.ac.at/gwasapp/DATA_NEW_BROWSER/PYGWAS_GENOTYPES')
STUDY_DATA_FOLDER=os.environ.get('OUTPUT_FOLDER','/mnt/gwasapp/DATA_NEW_BROWSER/study')

restclient = Restclient(REST_HOST,REST_USERNAME,REST_PASSWORD)
