import subprocess

lm_util = r"C:\Program Files (x86)\ArcGIS\LicenseManager\bin\lmutil.exe"

s = {
    'port': 27000,
    'hostname': 'gv-gislicense'

}
# process = subprocess.Popen([lm_util, "lmstat", "-f -c {}@{}".format(s['port'], s['hostname'])],
#                            stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

process = subprocess.Popen([lm_util, "lmstat", "-f", "-c", "{}@{}".format(s['port'], s['hostname'])],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)

lines = process.stdout.read()

print(lines)