SHELL='/bin/bash'
MAGDIR=$(PWD)
FILE_MODE=ug+rwX,o+rX
INSTALL=install --mode=${FILE_MODE}

all: install

build:
	$(MAKE) -C pml
	mkdir -m 775 -p sqlite3
	mkdir -m 775 -p resources
	mkdir -m 775 -p ./resources/media
	mkdir -m 775 -p ./resources/static
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
