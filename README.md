# Chained Hashing

Encode and decode files with chained hashing.

Requires Python 3.9+.

## Installation

## From Source

```bash
python3 -m pip install git+https://github.com/xsc27/chained-hashing.git
```

## Usage

### Command Line Interface

```text
❯ chained_hashing --help
usage: chained_hashing [-h] [-v] [-l {notset,debug,info,warning,error,critical}] {run} ...

Encode and decode files with chained hashing.

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l {notset,debug,info,warning,error,critical}, --log-level {notset,debug,info,warning,error,critical}
                        Set log level

actions:
  {run}
    run                 Execute
```

### Container Image

```text
❯ docker container run ghcr.io/xsc27/chained_hashing:latest
usage: chained_hashing [-h] [-v]
                       [-l {notset,debug,info,warning,error,critical}]
                       {run} ...

Encode and decode files with chained hashing.

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l {notset,debug,info,warning,error,critical}, --log-level {notset,debug,info,warning,error,critical}
                        Set log level

actions:
  {run}
    run                 Execute command
```

# License

Copyright 2021 Carlos Meza

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

```
 http://www.apache.org/licenses/LICENSE-2.0
```

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
