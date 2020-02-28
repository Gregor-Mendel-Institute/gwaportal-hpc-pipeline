from .rest import Restclient
import os

HPC_HOST = os.environ['HPC_HOST']
HPC_USER = os.environ.get('HPC_USER',None)
REST_HOST = os.environ['REST_HOST']
REST_USERNAME = os.environ['REST_USERNAME']
REST_PASSWORD = os.environ['REST_PASSWORD']
GENOTYPE_FOLDER = os.environ['GENOTYPE']
STUDY_DATA_FOLDER=os.environ['OUTPUT_FOLDER']
SSH_KEY_FILENAME = os.environ.get('SSH_KEY_FILENAME', None)

restclient = Restclient(REST_HOST,REST_USERNAME,REST_PASSWORD)
