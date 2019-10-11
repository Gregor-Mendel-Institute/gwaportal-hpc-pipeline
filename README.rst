GWA-Portal HPC pipeline
==========

GWA-Portal HPC pipeline provides task that can be run on the HPC cluster via celery and fabric.   
Typical usage is to start a celery worker:

    celery worker --app=gwaportal_hpc_pipeline
