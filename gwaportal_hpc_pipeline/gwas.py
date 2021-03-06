from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from .celery import app
from fabric import Connection

from . import fabfile as hpc

logger = get_task_logger(__name__)

connect_kwargs=None

if hpc.SSH_KEY_FILENAME:
    connect_kwargs = { "key_filename": hpc.SSH_KEY_FILENAME}

c = Connection(hpc.hosts[0], user=hpc.HPC_USER, connect_kwargs=connect_kwargs)

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
