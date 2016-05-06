# edison_usr_local_bin

### Installing Python 3.4

Reference: https://communities.intel.com/thread/59799?start=0&tstart=0

  wget --no-check-certificate https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
  l
  tar -xvzf Python-3.4.2.tgz
  l
  mkdir ../unpacked
  mv Python-3.4.2 ../unpacked
  cd ../unpacked
  l
  cd Python-3.4.2/
  ./configure --with-pydebug
  make -s -j2
  ls -al
  ./python -V
  cp python python3.4.2
  mv python3.4.2 /usr/bin
  cd /usr/bin
  ln -s python3.4.2 python3
  cd
  which python3
  python3 -V
  ls -al /usr/bin/python*


