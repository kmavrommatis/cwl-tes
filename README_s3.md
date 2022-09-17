# important note

I am not a seasoned python developer. This has been one of my first python projects.
I had to work on it out of necessity, i.e. ability to work with the latest CWL version on an AWS environment.
Much of the code is hacky since I was not able to find the proper way to address some of the issues. 

If anybody is interested in using it, do it at your own risk.

# install 

```
conda create -n cwltes python=3.8

conda activate cwltes

pip3 install -r requirements.txt

```

# test 


```
conda activate cwltes
./cwl-tes --debug --remote-storage-url s3://celgene-rnd-riku-researchanalytics/funnel_1/ --tes http://localhost:8000 tests/hashsplitter-workflow.cwl.yml --input s3://celgene-rnd-riku-researchanalytics/funnel/tests/resources/test.txt
```

 on RCE 2.0

```
./cwl-tes --debug --remote-storage-url s3://aac-ue1-s0-ni-00-001-results/ngs2_tests/cwltes/ --tes http://10.180.9.200:8003/tesw/ tests/hashsplitter-workflow.cwl.yml --input s3://aac-ue1-s0-ni-00-001-data/ngs2_tests/cwltes/test.txt
```


The above command works. Produces output on s3 and a json output as such on stdout.

```
{
    "output": {
        "location": "s3://celgene-rnd-riku-researchanalytics/funnel_1/a7758d0f-a35f-4398-99c2-d6a955d71d76/unify/unify",
        "basename": "unify",
        "class": "File",
        "size": 472
    }
}

```



```
conda activate cwltes
./cwl-tes --debug --remote-storage-url s3://celgene-rnd-riku-researchanalytics/funnel_1/ --tes http://localhost:8000 tests/hashsplitter-workflow.cwl.yml hashsplitter-input.json
```



works as well.


In stderr the line 

```
Submitting workflow: 171084b1-4faa-4dee-bc52-eb33c8084f2b
```

contains the id of the workflow

if a pipeline succeeds the script returns exit code 0

if a pipeline fails e.g.

```
conda activate cwltes
./cwl-tes --debug --remote-storage-url s3://celgene-rnd-riku-researchanalytics/funnel_1/ --tes http://localhost:8000 tests/hashsplitter-workflow.cwl.yml hashsplitter-input_failed.json

```

