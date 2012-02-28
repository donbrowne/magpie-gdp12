INSTALLATION INSTRUCTIONS:

Installation instructions are for Ubuntu, specifically tested against
versions 10.04 and 10.10, for other distributions, consult the docs 
folder.

STEP 1:

From the directory in which you found this file, run:

  chmod +x *.sh

STEP 2:
(This step is only necessary when setting up Magpie on your computer for
the first time. If you are setting up an additional instance, skip this)

From the same directory, run:
  
  sudo ./setup_ubuntu.sh
  
STEP 3:
(This step is only necessary when building from the SVN. If you are 
installing from the tarball, skip this)

From the same directory, run:

  ./setup_db.sh
  
During the execution of the script, it will ask you the details needed
to set up the Django database.
  
STEP 4:

From the same directory, run:

  ./configure_instance.sh
  
Note that this script requires you to answer two questions.

Once this script has finished, it is possible to access the site from 
the URL specified when the script finished. It is of the form

  http://NAME.HOSTNAME
  
Where HOSTNAME is your hostname, and NAME is the subdomain name you gave
the script when it asked you for one (which defaults to 'magpie' if left 
blank).
