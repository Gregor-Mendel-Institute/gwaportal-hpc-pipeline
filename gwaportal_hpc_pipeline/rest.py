import requests
import shutil
import tempfile

class Restclient(object):

    def __init__(self,host,username,password):
        self.host = host
        self.auth = (username,password)

    def get_phenotype_data(self,studyid):
        headers = {'Accept':'application/json'}
        URL = '%s/provider/study/%s/studygwasdata' % (self.host,studyid)
        r = requests.get(URL,headers=headers,auth=self.auth, verify=False)
        if r.status_code == 200:
            return r.json()
        raise Exception(r.text)

    def get_candidate_genes(self,candidate_gene_id):
        headers = {'Accept':'application/json'}
        URL = '%s/provider/candidategenelist/%s/genes' % (self.host,candidate_gene_id)
        r = requests.get(URL,headers=headers,auth=self.auth, verify=False)
        if r.status_code == 200:
            return r.json()
        raise Exception(r.text)

