#Change DESTDIR to the target directory for your installation.
#Alternatively, specify DESTDIR as an argument to the makefile.
DESTDIR=$(PWD)
SHELL='/bin/bash'
MAGDIR=$(PWD)
FILE_MODE=ug+rw,o-rw
DIR_MODE=ug+rwX,o-rwX
INST=install --mode=$(FILE_MODE)
INSTDIR=install --mode=$(DIR_MODE)

all: install

build: sqlite3/magpie.db pml/graph/traverse resources resources/static

sqlite3/magpie.db:
	@echo "Setting up sample database"
	$(INSTDIR) -d sqlite3
	$(INST) ./dataload/magpie.db ./sqlite3/
	@echo "Done!"
	
pml/graph/traverse:
	@echo "Building PML tools"
	$(MAKE) -C pml
	@echo "Done!"

resources: 
	@echo "Collecting media content"
	$(INSTDIR) -d resources ./resources/media
	$(INST) ./dataload/media/* ./resources/media/
	$(INST) ./dataload/media/.htaccess ./resources/media/
	@echo "Done!"
	
resources/static:
	@echo "Collecting static content"
	python ./django_magpie/manage.py collectstatic --noinput
	@echo "Done!"

clean: 
	$(MAKE) clean -C pml
	find ./django_magpie/ -type f -name "*.pyc" -exec rm -f {} \;

install: build
	@if [ ! -z $(DESTDIR) ]; then echo "Creating symlinks"; cd $(DESTDIR); ln -s $(MAGDIR)/django_magpie/magpie.wsgi magpie.wsgi; ln -s $(MAGDIR)/resources/media media; ln -s $(MAGDIR)/resources/static static; fi
	@echo "Done!"
	
test: build
	python2 ./django_magpie/manage.py test
	
distclean: clean 
	rm -rf ./sqlite3
	rm -rf ./resources/
	rm ./pml/graph/traverse
	rm ./pml/graph/print_io
	if [ ! -z $(DESTDIR) ]; then echo "Destroying symlinks"; cd $(DESTDIR); rm magpie.wsgi; rm media; rm static; cd $(MAGDIR); fi;
