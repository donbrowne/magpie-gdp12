SHELL='/bin/bash'
ESCPATH=$(subst /,\/,$(PWD))

all: build

build:
	$(MAKE) -C pml
	mkdir sqlite3
	cp ./dataload/magpie.db ./sqlite3/
	python2 ./django_magpie/manage.py collectstatic

clean:
	$(MAKE) clean -C pml

install: sqlite3
	@echo "Setting up Magpie application instance"
	@echo "Using the current working directory as the path to this folder"
	@echo "Configuring wsgi script and settings.py"
	sed -i "s/PATH/$(ESCPATH)/g" ./django_magpie/magpie.wsgi
	sed -i "1 c\URL_ROOT='$(URL)'" ./django_magpie/settings.py
	@if [ ! -z $(DESTDIR) ]; then echo "Creating symlinks"; cd $(fsPath); ln -s $path/django_magpie/magpie.wsgi magpie.wsgi; ln -s $path/resources/media media; ln -s $path/resources/static static; fi
	@echo "Done!"
	
test:
	python ./django_magpie/manage.py test
	
distclean: sqlite3 
	rm -rf sqlite3
	rm -rf ./resources/static/*

	if [ ! -z $(DESTDIR) ]; 
	then
	echo "Destroying symlinks"
	rm $(DESTDIR)/magpie.wsgi
	rm $(DESTDIR)/media
	rm $(DESTDIR)/static
	fi
