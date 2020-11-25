from subprocess import Popen, PIPE, STDOUT

from celery import shared_task


@shared_task(bind=True)
def launch(self, data):
    res = []
    print(f'Script path: {data["script"]}')
    process = Popen(
        f"/usr/src/nextflow run {data['script']}",
        bufsize=1,
        stdout=PIPE,
        stderr=STDOUT,
        stdin=PIPE,
        shell=True
    )

    for line in iter(process.stdout.readline, b''):
        line = line.decode('utf-8')
        res.append(line)
        print(line)
    process.wait()
    return res
