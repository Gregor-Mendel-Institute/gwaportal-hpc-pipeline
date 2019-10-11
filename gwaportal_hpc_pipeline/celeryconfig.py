from kombu import Exchange, Queue
import os
broker_url = os.environ.get('CELERY_BROKER', None)
result_backend= 'rpc'
result_persistent = True
task_serializer = 'json'
result_serializer = 'json'

gwas_exchange = Exchange('gwas', type='direct')
topsnps_exchange = Exchange('topsnps', type='direct')
enrichment_exchange = Exchange('enrichment', type='direct')

task_queues = (
    Queue('gwas.portal.hpc', gwas_exchange, routing_key='gwas.portal.hpc'),
    Queue('gwas.portal.hpc.check_jobs',gwas_exchange,routing_key='gwas.portal.hpc.check_jobs'),
    Queue('topsnps',topsnps_exchange, routing_key='topsnps'),
    #Queue('enrichment',enrichment_exchange,routing_key='enrichment'),
    #Queue('enrichment.check_jobs',enrichment_exchange,routing_key='enrichment.check_jobs')
)


task_routes = {
        'gwaportal_hpc_pipeline.gwas.start_gwas':{'queue':'gwas.portal.hpc'},
        'gwaportal_hpc_pipeline.gwas.check_gwas_job':{'queue':'gwas.portal.hpc.check_jobs'},
        'gwaportal_hpc_pipeline.snps.index_top_study_snps':{'queue':'topsnps'},
        #'gwaportal_hpc_pipeline.enrichment.start_saga':{'queue':'enrichment'},
        #'gwaportal_hpc_pipeline.enrichment.check_saga_job':{'queue':'enrichment.check_jobs'}
}

# Name and email addresses of recipients
ADMINS = (
    ("HPCSubmitWorker", "hpcsubmitworker@gmi.oeaw.ac.at"),
)

# Email address used as sender (From field).
SERVER_EMAIL = "hpcsubmitworker@gmi.oeaw.ac.at"

EMAIL_HOST = "exhc01.gmi.oeaw.ac.at"
EMAIL_PORT = 25
EMAIL_HOST_USER = "hpcsubmitworker@gmi.oeaw.ac.at"
