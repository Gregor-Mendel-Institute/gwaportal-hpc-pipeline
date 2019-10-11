from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('gwaportal_hpc_pipeline',
    include=['gwaportal_hpc_pipeline.gwas','gwaportal_hpc_pipeline.snps']
)
  
app.config_from_object('gwaportal_hpc_pipeline.celeryconfig')

if __name__ == '__main__':
    app.start()

