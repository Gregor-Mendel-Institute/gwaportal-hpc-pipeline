import os, pwd, logging,tempfile, re
from fabric import task
from gwaportal_hpc_pipeline import *

SBATCH_PATTERN = re.compile(r"Submitted batch job ([0-9]*)")

USER = os.environ.get('HPC_USER',pwd.getpwuid(os.getuid()).pw_name)
HOME = '/users/%s' % USER
SCRIPTS_FOLDER = os.path.join(HOME,"scripts/gwaportal")
GWAS_SCRIPT = os.path.join(SCRIPTS_FOLDER, "pygwas.sh")
WORKDIR='/scratch-cbe/users/%s/GWASDATA' % USER

logger = logging.getLogger(__name__)

hosts = ["hpc"]

def _get_folders(study_id):
    data_folder = os.path.join(WORKDIR, str(study_id))
    input_folder = os.path.join(data_folder, 'INPUT')
    output_folder = os.path.join(data_folder, 'OUTPUT')
    log_folder = os.path.join(data_folder, 'LOG')
    return input_folder, output_folder, log_folder

@task(hosts=hosts)
def stage_in_phenotype(c,study_id):
    phenotype_file_path = None
    try:
        input_folder, output_folder, log_folder = _get_folders(study_id)
        logger.info('Downloading phenotype file')
        data = restclient.get_phenotype_data(study_id)
        phenotype_data = data['csvData']
        fd, phenotype_file_path = tempfile.mkstemp()
        os.write(fd, phenotype_data.encode())
        os.close(fd)
        logger.info('Staging in phenotype file')
        c.run("mkdir -p %s %s %s" % (input_folder,output_folder,log_folder))
        c.put(phenotype_file_path, "%s/%s.csv" % (input_folder, study_id))
        return data
    except Exception as err:
        logger.exception("Fatal error in main loop")
        raise err
    finally:
        if phenotype_file_path:
          os.unlink(phenotype_file_path)

@task(hosts=hosts)
def stage_out_result(c, job_id, study_id):
    logger.info("Staging out GWAS results for study %s" % study_id)
    logger.info("Checking error log files and output files")
    input_folder, output_folder, log_folder = _get_folders(study_id)
    error_filename = os.path.join(log_folder,"%s.err" % job_id)
    error_file_size = c.run('stat -c \'%s\' {0}'.format(error_filename), warn=True)
    if error_file_size.failed or int(error_file_size.stdout) > 0:
        return "FAILED"
    
    output_filename = os.path.join(output_folder, "%s.hdf5" % study_id)
    output_file_size = c.run('stat -c \'%s\' {0}'.format(output_filename), warn=True)
    if output_file_size.failed or int(output_file_size.stdout) == 0:
      return "FAILED"
    logger.info("Staging out files and cleanup")
    c.get(output_filename, os.path.join(STUDY_DATA_FOLDER, '%s.hdf5' % str(study_id)))
    c.run("rm -rf %s" % os.path.join(WORKDIR, str(study_id)))
    return "DONE"
    
@task(hosts=hosts)
def check_job_state(c, job_id,study_id):
    try:
        logger.info('Getting job state from HPC for study %s and jobid %s' % (study_id,job_id))
        check_cmd = "sacct -j %s.batch -o state -pn" % job_id
        check_output = c.run(check_cmd)
        status = check_output.stdout.strip()
        if status == "": 
            status = "RUNNING"
        else:
            status = status[:-1]
        logger.info('Job state is %s' % status) 
        if status == "COMPLETED":
          status = stage_out_result(c, job_id, study_id)
        elif status in ("CANCELED", "OUT_OF_MEMORY"):
          status = "Failed"
        return status 
    except Exception as err:
        logger.exception("Failed to check exception")
        raise err
        

@task(hosts=hosts)
def submit_gwas(c,study_id):     
    input_folder, output_folder, log_folder = _get_folders(study_id)
    data = stage_in_phenotype(c,study_id) 
    logger.info("Submit GWAS analysis")
    analysis = data['analysisMethod']
    genotype = data['genotype']
    transformation = data['transformation']
    runtime = round((data['runtime'] + data['runtime']*0.5)/60)
    runtime = max(runtime,10)
    params = {"time": runtime, "name": "GWA_%s" % study_id, 
              "workdir": log_folder, "id":study_id, 
              "analysis": analysis.lower(), 
              "genotype": genotype,
              "script": GWAS_SCRIPT
             }
    sbatch_cmd = "sbatch -D %(workdir)s -J %(name)s -t %(time)s --mem 6G  %(script)s %(id)s %(analysis)s %(genotype)s" % params
    logger.info("SBATCH call: %s" % sbatch_cmd)
    sbatch_output = c.run(sbatch_cmd)
    if sbatch_output.failed:
      raise Exception("Failed to submit Job: %s" % sbatch_output.stderr)
    match = SBATCH_PATTERN.match(sbatch_output.stdout)
    if not match:
        raise Exception('Failed to get jobid' % sbatch_output.stdout )
    job_id = match.group(1)
    logger.info('GWAS job sucessfully submitted (%s)' % job_id)
    return {'sge_job_id':job_id, 'saga_job_id':''}

