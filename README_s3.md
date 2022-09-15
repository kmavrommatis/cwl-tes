# tests for the s3 api



```
source ~/venv3/bin/activate
./cwl-tes --debug --remote-storage-url s3://celgene-rnd-riku-researchanalytics/funnel_1/ --tes http://localhost:8000 tests/hashsplitter-workflow.cwl.yml --input s3://celgene-rnd-riku-researchanalytics/funnel/tests/resources/test.txt
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
source ~/venv3/bin/activate
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
source ~/venv3/bin/activate
./cwl-tes --debug --remote-storage-url s3://celgene-rnd-riku-researchanalytics/funnel_1/ --tes http://localhost:8000 tests/hashsplitter-workflow.cwl.yml hashsplitter-input_failed.json

```

exits with non-zero code



ERRORS:

----

Set the proper fetcher:

```
$./cwl-tes --debug   --remote-storage-url s3://celgene-rnd-riku-researchanalytics/funnel_1/ --tes http://localhost:8000 tests/hashsplitter-workflow.cwl.yml --input s3://celgene-rnd-riku-researchanalytics/funnel/tests/resources/test.txt
```


Output

```
./cwl-tes 0.3.0 with cwltool 3.1.20220502060230
Submitting workflow: 030d4321-af8f-4baa-b54f-e7f358e55c0c
INFO ./cwl-tes 0.3.0 with cwltool 3.1.20220502060230
Traceback (most recent call last):
  File "/Users/mavrommk/workspace/cwlteslatest/./cwl-tes", line 11, in <module>
    cwl_tes.main.main(sys.argv[1:])
  File "/Users/mavrommk/workspace/cwlteslatest/cwl_tes/main.py", line 239, in main
    retval = cwltool.main.main(
  File "/Users/mavrommk/miniconda3/envs/cwlteslatest/lib/python3.9/site-packages/cwltool/main.py", line 1081, in main
    loadingContext = setup_loadingContext(loadingContext, runtimeContext, args)
  File "/Users/mavrommk/miniconda3/envs/cwlteslatest/lib/python3.9/site-packages/cwltool/main.py", line 739, in setup_loadingContext
    loadingContext.loader = default_loader(
  File "/Users/mavrommk/miniconda3/envs/cwlteslatest/lib/python3.9/site-packages/cwltool/load_tool.py", line 71, in default_loader
    return Loader(
  File "/Users/mavrommk/miniconda3/envs/cwlteslatest/lib/python3.9/site-packages/schema_salad/ref_resolver.py", line 191, in __init__
    self.fetcher = self.fetcher_constructor(self.cache, self.session)
  File "/Users/mavrommk/workspace/cwlteslatest/cwl_tes/fetcher_s3.py", line 17, in __init__
    super(CollectionFetcher, self).__init__(cache, session)
NameError: name 'CollectionFetcher' is not defined
```

Replace CollectionFetcher with DefaultFetcher
RESOLVED


----

tes not found

```
ERROR Unexpected exception
Traceback (most recent call last):
  File "/Users/mavrommk/miniconda3/envs/cwltes/lib/python3.10/site-packages/cwltool/workflow.py", line 457, in job
    yield from self.embedded_tool.job(
  File "/Users/mavrommk/miniconda3/envs/cwltes/lib/python3.10/site-packages/cwltool/command_line_tool.py", line 1006, in job
    j = self.make_job_runner(runtimeContext)(
  File "/Users/mavrommk/workspace/cwlteslatest/cwl_tes/tes.py", line 246, in __init__
    self.client = tes.HTTPClient(url, token=token)
NameError: name 'tes' is not defined
DEBUG job: <cwltool.workflow_job.WorkflowJob object at 0x107d15c60>, runtime_context: <cwltool.context.RuntimeContext object at 0x1075231f0>, TMPDIR_LOCK: <unlocked _thread.lock object at 0x106b96fc0>
ERROR [step sha] Cannot make job: name 'tes' is not defined
INFO [workflow ] start
DEBUG
Traceback (most recent call last):
  File "/Users/mavrommk/miniconda3/envs/cwltes/lib/python3.10/site-packages/cwltool/workflow.py", line 457, in job
    yield from self.embedded_tool.job(
  File "/Users/mavrommk/miniconda3/envs/cwltes/lib/python3.10/site-packages/cwltool/command_line_tool.py", line 1006, in job
    j = self.make_job_runner(runtimeContext)(
  File "/Users/mavrommk/workspace/cwlteslatest/cwl_tes/tes.py", line 246, in __init__
    self.client = tes.HTTPClient(url, token=token)
NameError: name 'tes' is not defined

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/mavrommk/miniconda3/envs/cwltes/lib/python3.10/site-packages/cwltool/workflow_job.py", line 853, in job
    for newjob in step.iterable:
  File "/Users/mavrommk/miniconda3/envs/cwltes/lib/python3.10/site-packages/cwltool/workflow_job.py", line 777, in try_make_job
    yield from jobs
  File "/Users/mavrommk/miniconda3/envs/cwltes/lib/python3.10/site-packages/cwltool/workflow_job.py", line 76, in job
    yield from self.step.job(joborder, output_callback, runtimeContext)
  File "/Users/mavrommk/miniconda3/envs/cwltes/lib/python3.10/site-packages/cwltool/workflow.py", line 467, in job
    raise WorkflowException(str(exc)) from exc
cwltool.errors.WorkflowException: name 'tes' is not defined
INFO [workflow ] completed permanentFail
```

Installed py-tes

----

