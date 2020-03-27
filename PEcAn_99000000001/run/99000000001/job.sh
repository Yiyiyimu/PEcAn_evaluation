#!/bin/bash

# redirect output
exec 3>&1
exec &> "/home/carya/output//PEcAn_99000000001/out/99000000001/logfile.txt"

# host specific setup


# create output folder
mkdir -p "/home/carya/output//PEcAn_99000000001/out/99000000001"

# see if application needs running
if [ ! -e "/home/carya/output//PEcAn_99000000001/out/99000000001/sipnet.out" ]; then
  cd "/home/carya/output//PEcAn_99000000001/run/99000000001"
  ln -s "/home/carya/sites/niwot/niwot.clim" sipnet.clim

  "/usr/local/bin/sipnet.r136"
  STATUS=$?
  
  # copy output
  mv "/home/carya/output//PEcAn_99000000001/run/99000000001/sipnet.out" "/home/carya/output//PEcAn_99000000001/out/99000000001"

  # check the status
  if [ $STATUS -ne 0 ]; then
  	echo -e "ERROR IN MODEL RUN\nLogfile is located at '/home/carya/output//PEcAn_99000000001/out/99000000001/logfile.txt'" >&3
  	exit $STATUS
  fi

  # convert to MsTMIP
  echo "require (PEcAn.SIPNET)
    model2netcdf.SIPNET('/home/carya/output//PEcAn_99000000001/out/99000000001', 40.0329, -105.546, '2002/01/01', '2005/12/31', FALSE, '136')
    " | R --no-save
fi

# copy readme with specs to output
cp  "/home/carya/output//PEcAn_99000000001/run/99000000001/README.txt" "/home/carya/output//PEcAn_99000000001/out/99000000001/README.txt"

# run getdata to extract right variables

# host specific teardown


# all done
echo -e "MODEL FINISHED\nLogfile is located at '/home/carya/output//PEcAn_99000000001/out/99000000001/logfile.txt'" >&3
