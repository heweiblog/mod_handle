ifeq ($(origin PYENV_ROOT), undefined)
$(error `pyenv` is required for the Target.)
endif


PYVER := $(lastword $(shell python --version 2>&1))
APPVER := $(strip $(shell cat version))
GITBRANCH := $(strip $(shell git rev-parse --abbrev-ref HEAD))
GITCOMMIT := $(strip $(shell git rev-parse --short HEAD))

PIP := $(strip $(shell pip list))

all: build


rpm: build
	mkdir -p hcrm-$(APPVER)/bin hcrm-$(APPVER)/etc
	cp dist/hcrm hcrm-$(APPVER)/bin
	cp dist/hcrm_db_init hcrm-$(APPVER)/bin
	cp -r etc hcrm-$(APPVER)
	tar cvzf ~/rpmbuild/SOURCES/hcrm-$(APPVER).tar.gz hcrm-$(APPVER)
	rpmbuild -bb --define "DRMSVER $(APPVER)" --define "GITBRANCH $(GITBRANCH)" --define "GITCOMMIT $(GITCOMMIT)" rpm.spec
	rm -rf hcrm-$(APPVER)


TGT=hcrm
rpmclean: clean	
	cp -r ~/rpmbuild/RPMS/x86_64/$(TGT)-$(APPVER)-$(GITBRANCH)_$(GITCOMMIT)* ./  
	rm -rf ~/rpmbuild/SOURCES/$(TGT)-$(APPVER)* \
	~/rpmbuild/BUILD/$(TGT)-$(APPVER)* \
	~/rpmbuild/RPMS/x86_64/$(TGT)-$(APPVER)* \
	~/rpmbuild/SPEC/$(TGT)-$(APPVER)* 


pack:
	md5sum $(TGT)-$(APPVER)-$(GITBRANCH)_$(GITCOMMIT).*.x86_64.rpm > md5
	mkdir $(TGT)-$(APPVER)-$(GITBRANCH)_$(GITCOMMIT).x86_64.rpm
	mv $(TGT)-$(APPVER)-$(GITBRANCH)_$(GITCOMMIT).*.x86_64.rpm md5 $(TGT)-$(APPVER)-$(GITBRANCH)_$(GITCOMMIT).x86_64.rpm
	tar -zcvf $(TGT)-$(APPVER)-$(GITBRANCH)_$(GITCOMMIT).x86_64.rpm.tar.gz $(TGT)-$(APPVER)-$(GITBRANCH)_$(GITCOMMIT).x86_64.rpm
	rm -rf $(TGT)-$(APPVER)-$(GITBRANCH)_$(GITCOMMIT).x86_64.rpm


build: clean
	./script/check_lib
	env LD_LIBRARY_PATH=$(LD_LIBRARY_PATH):$(PYENV_ROOT)/versions/$(PYVER)/lib/ pyinstaller -F script/hcrm_db_init.py
	env LD_LIBRARY_PATH=$(LD_LIBRARY_PATH):$(PYENV_ROOT)/versions/$(PYVER)/lib/ pyinstaller -F src/hcrm.py


.PHONY: clean


clean:
	rm -rf build dist
	rm -rf hcrm-$(APPVER)
	rm -rf hcrm.spec hcrm_db_init.spec
	rm -rf script/__pycache__/
	rm -rf src/__pycache__/
	rm -rf src/common/__pycache__/
	rm -rf src/resources/__pycache__/
	rm -rf src/models/__pycache__/
