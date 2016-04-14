echo "Requesting vis node for" ${1-1:00:00}
srun -A CS381V-Visual-Recogn -p vis -t ${1-1:00:00} -n 1 --pty /bin/bash -l
