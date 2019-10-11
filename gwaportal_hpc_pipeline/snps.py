from __future__ import absolute_import
from celery.utils.log import get_task_logger
from .celery import app

logger = get_task_logger(__name__)

ELASTICSEARCH_HOST = "http://elasticsearch.gmi.oeaw.ac.at:9200"
TOP_SNP_LIMIT=1000

@app.task(serializer='json',ignore_result=True)
def index_top_study_snps(studyid,experimentid):
    top_snps = _get_top_snps(studyid)
    # DOESNT WORK UNTIL nested objects can be filtered by matches hits
    #req = _indexTopSNPs(studyid,phenotypeid,top_snps)
    top_snps_sorted = top_snps[numpy.argsort(top_snps['chr'])]
    annotation = _retrieveAnnotation(top_snps_sorted)
    req = _indexTopSNPsSeparately(studyid,top_snps_sorted,annotation,experimentid)

def _retrieveAnnotation(top_snps):
    chr_annotation = []
    for chr in range(1,6):
        chr_snps = top_snps['position'][numpy.where(top_snps['chr'] == str(chr))]
        payload = simplejson.dumps({'ids':chr_snps.tolist()})
        url = '%s/annot_chr%s/snps/_mget' % (ELASTICSEARCH_HOST,chr)
        req = requests.get(url,data=payload)
        if req.status_code in [200,201,202]:
            docs = req.json()
            chr_annotation.extend(docs['docs'])
    return chr_annotation


def _getSNPDocument(snp):
    doc = {u'chr':snp[0],u'position':int(snp[1]),u'score':float(snp[2]),u'overFDR':bool(snp[5])}
    if not numpy.isnan(snp[3]):
        doc[u'maf'] = float(snp[3])
    if not numpy.isnan(snp[4]):
        doc[u'mac'] = int(snp[4])
    return doc

def _indexTopSNPsSeparately(studyid,snps,annotations,experimentid):
    url = '%s/_bulk' % ELASTICSEARCH_HOST
    payload = ''
    bulk_index = "gdpdm"
    i = 0
    for snp in snps:
        snp_to_index = _getSNPDocument(snp)
        annotation = annotations[i]
        if annotation['exists']:
            if 'gene' in annotation['_source']:
                snp_to_index['gene'] = annotation['_source']['gene']
            snp_to_index['annotation'] = annotation['_source']['annotation']
            snp_to_index['inGene'] = bool(annotation['_source']['inGene'])
        snp_to_index['studyid'] = studyid
        id = "%s_%s_%s" % (studyid,snp_to_index['chr'],snp_to_index['position'])
        action = '{"index":{"_index":"%s","_type":"%s","_id":"%s","_parent":"%s","_routing":"%s"}}\n' % (bulk_index,"meta_analysis_snps",id,studyid,experimentid)
        data = simplejson.dumps(snp_to_index)+'\n'
        payload = payload + action + data
        i = i + 1
    req = requests.put(url,data=payload)
    if req.status_code in [200,201,202]:
        return req.json()
    else:
        raise Exception(str(req.text))

def _indexTopSNPs(studyid,phenotypeid,snps):
    url = '%s/%s/%s/%s/_update?routing=%s' % (ELASTICSEARCH_HOST,"gdpdm","study",studyid,phenotypeid)
    top_snps = []
    for snp in snps:
        top_snps.append(_getSNPDocument(snp))
    top_snps_to_index = {'doc':{'top_snps':top_snps}}
    data = simplejson.dumps(top_snps_to_index,encoding='cp1252')+'\n'
    payload = data
    req = requests.post(url,data=payload)
    if req.status_code in [200,201,202]:
        return req.json()
    else:
        raise Exception(str(req.text))


def _get_top_snps(studyid):
    hdf5_file = '%s/%s.hdf5' % (saga_gwa.STUDY_DATA_FOLDER,studyid)
    return utils.get_top_snps(hdf5_file,TOP_SNP_LIMIT)

