def jobsMapping = [
  tags: [jobName:"App GWAPortal", jobTags: "reload", extraVars: "app_generic_image_tag: latest"],
  master: [jobName:"App GWAPortal", jobTags: "reload", extraVars: "app_generic_image_tag: master"]
]

buildDockerImage([
    imageName: "gwaportal-hpc-pipeline",
    pushRegistryNamespace: "nordborglab/gwaportal",
    pushBranches: ['develop', 'master'],
    tower: jobsMapping
])