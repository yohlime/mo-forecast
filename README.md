# MO Automated WRF system

## Installation
---

### Installation Requirements
- bash environment
- slurm
- preinstalled WRF system
- python 3.7+

### 1. Clone the repo
```
git clone http://rcs.observatory.ph/git/egozo/mo_forecast.git ~/forecast
```

### 2. Create a configuration file
```
cd ~/forecast
cp set_cron_env.sh.sample set_cron_env.sh
vi set_cron_env.sh
```

### 3. Setup required paths/files
- __input__/ - input files needed by the WRF system (eg. GFS, etc.)
- __output__/ - location of files created by post processing scripts
- __model__/ - WRF system executables and related files
    - __WPS__/ - should contain _geogrid.exe_, _ungrib.exe_, _metgrid.exe_ and related files like _namelist.wps_, _geog/_ and _VTable_. Can be a symbolic link to _\<WPS SRC DIR\>/_.
    - __WRF__/ - should contain _real.exe_, _wrf.exe_ and related files like _namelist.wrf_. Can be a symbolic link to _\<WRF SRC DIR\>/test/em_real_.

### 4. Create a cron entry
```
# 5-day forecast ensemble
# 00Z and 12Z
40 2,14 * * * . $HOME/forecast/set_cron_env.sh; . $HOME/forecast/scripts/run_fcst.sh
```