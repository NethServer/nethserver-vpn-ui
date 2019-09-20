Summary: NethServer VPN UI module
Name: nethserver-vpn-ui
Version: 1.1.0
Release: 1%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
# Build Source1 by executing prep-sources
Source1: %{name}-cockpit.tar.gz

BuildArch: noarch

Requires: nethserver-firewall-base

BuildRequires: nethserver-devtools

%description
VPN UI module for NethServer.


%prep
%setup -q

%build
sed -i 's/_RELEASE_/%{version}/' %{name}.json
%{makedocs}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/nethserver-vpn/
tar xf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/nethserver-vpn/

%post

%preun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/share/cockpit/%{name}/*
/usr/share/cockpit/nethserver/applications/*
/usr/libexec/nethserver/api/nethserver-vpn/*
%attr(0440,root,root) /etc/sudoers.d/50_nsapi_nethserver_vpn_ui

%changelog
* Wed Sep 18 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.1.0-1
- Statistics on OpenVPN connections - NethServer/dev#5827

* Tue Sep 03 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.2-1
- Cockpit. List correct application version - Nethserver/dev#5819

* Fri Jul 05 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.1-1
- Prevent failures if some VPN  modules are not installed

* Wed Jun 19 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.0-1
- VPN Cockpit UI - NethServer/dev#5760

* Thu May 16 2019 Edoardo Spadoni <edoardo.spadoni@nethesis.it> - 0.0.0-0
- First implementation
