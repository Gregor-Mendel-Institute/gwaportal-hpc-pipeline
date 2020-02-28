from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from .celery import app
from fabric import Connection

from . import fabfile as hpc

logger = get_task_logger(__name__)

c = Connection(hpc.hosts[0])

@app.task(serializer='json')
def start_gwas(studyid):
    retval = hpc.submit_gwas(c,studyid)
    return retval


@app.task(serializer='json')
def check_gwas_job(studyid,saga_job_id,slurm_job_id):
    logger.info('Checking job state')
    status = hpc.check_job_state(c,slurm_job_id,studyid)
    retval = {'status':status}
    return retval
