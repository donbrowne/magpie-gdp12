SHELL='/bin/bash'
MAGDIR=$(PWD)
FILE_MODE=660
DIR_MODE=770
INSTALL=install --mode=${FILE_MODE}
MKDIR=mkdir -m {DIR_MODE} -p

all: install

build:
	$(MAKE) -C pml
	$(MKDIR) sqlite3
	$(MKDIR) resources
	$(MKDIR) ./resources/media
	$(MKDIR) ./resources/static
	$(INSTALL) ./dataload/magpie.db ./sqlite3/
	$(INSTALL) ./dataload/media/* ./resources/media/
	python2 ./django_magpie/manage.py collectstatic
	touch build

clean: 
	$(MAKE) clean -C pml
	rm build
	rm ./django_magpie/*.pyc

install: build
	@echo "Setting up Magpie application instance"
	@echo "Using the current working directory as the path to this folder"
	@echo "Configuring wsgi script and settings.py"
	@if [ ! -z $(DESTDIR) ]; then echo "Creating symlinks"; cd $(DESTDIR); ln -s $(MAGDIR)/django_magpie/magpie.wsgi magpie.wsgi; ln -s $(MAGDIR)/resources/media media; ln -s $(MAGDIR)/resources/static static; fi
	@echo "Done!"
	
test: build
	python ./django_magpie/manage.py test
	
distclean: clean 
	rm -rf ./sqlite3
	rm -rf ./resources/static/*
	rm -rf ./resources/media/*
	rm ./pml/graph/traverse
	rm ./pml/graph/print_io
	if [ ! -z $(DESTDIR) ]; then echo "Destroying symlinks"; cd $(DESTDIR); rm magpie.wsgi; rm media; rm static; cd $(MAGDIR); fi;
