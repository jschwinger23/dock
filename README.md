# dock
Docker in Python

# Steps

1. Namespace, Cgroups, Pipe
   - `dock run -it /bin/bash`
   - `dock run -it -m100m -cpuset1 -cpushare512 /bin/bash`
2. Image
   - `dock run -v $(pwd):/src`
   - `dock commit`
   - `dock run <image>`
3. Container
   - `dock -d`
   - `dock ps [-a]`
   - `dock logs <container>`
   - `dock exec`
   - `dock loads`
   - `dock stop`
   - `dock rm [-f]`
   - `dock -e`
