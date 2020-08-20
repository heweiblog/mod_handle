Name: hcrm
Version: %{DRMSVER}
Release: %{GITBRANCH}_%{GITCOMMIT}%{?dist}
Summary: DRMS Server for YamuDNS

Group: Yamu Tech Co Ltd.
License: GPLv3+
URL: http://www.yamu.com/
Source0: %{name}-%{version}.tar.gz

BuildRequires: info
Requires: info

%description
Dns Configuration middleware

%define debug_package %{nil}

%prep
%setup -q


%build
exit 0
#%configure
#make %{?_smp_mflags}


%define hcrm_ini %{_sysconfdir}/hcrm.ini

%pre
if [ -f %{hcrm_ini} ]; then cp %{hcrm_ini} %{hcrm_ini}.old;fi


%install
mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/init.d
mkdir -p ${RPM_BUILD_ROOT}/var/hcrm/log

install -m 0755 bin/%{name} ${RPM_BUILD_ROOT}/%{_bindir}
install -m 0755 bin/hcrm_db_init ${RPM_BUILD_ROOT}/%{_bindir}
install -m 0755 etc/%{name} ${RPM_BUILD_ROOT}/%{_sysconfdir}/init.d
install -m 0644 etc/%{name}.ini ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}.ini
install -m 0644 etc/switch.json ${RPM_BUILD_ROOT}/var/hcrm
install -m 0644 etc/handle_switch.json ${RPM_BUILD_ROOT}/var/hcrm
install -m 0644 etc/threshold.json ${RPM_BUILD_ROOT}/var/hcrm
install -m 0755 etc/back_conf ${RPM_BUILD_ROOT}/var/hcrm

exit 0

%make_install


%post
if [ "$1" = "1" ]
then
    chkconfig --add hcrm
fi
/var/hcrm/back_conf


%files
%{_bindir}/%{name}
%{_bindir}/hcrm_db_init
%{_sysconfdir}/init.d/%{name}
%config%{_sysconfdir}/%{name}.ini
/var/hcrm/log/
/var/hcrm/switch.json
/var/hcrm/handle_switch.json
/var/hcrm/threshold.json
/var/hcrm/back_conf


%doc


%preun
if [ "$1" = "0" ]
then
    chkconfig --del hcrm
fi


%define __debug_install_post   \
%{_rpmconfigdir}/find-debuginfo.sh %{?_find_debuginfo_opts} "%{_builddir}/%{?buildsubdir}"\
%{nil}

%changelog


