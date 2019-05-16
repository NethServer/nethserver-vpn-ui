Summary: NethServer VPN UI module
Name: nethserver-vpn-ui
Version: 0.0.1
Release: 1%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
# Build Source1 by executing prep-sources
Source1: %{name}-cockpit.tar.gz

BuildArch: noarch

Requires: nethserver-firewall-base, nethserver-pulledpork

BuildRequires: nethserver-devtools

%description
VPN UI module for NethServer.


%prep
%setup -q

%build
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

%changelog
* Thu May 16 2019 Edoardo Spadoni <edoardo.spadoni@nethesis.it> - 1.0.0-0
- First implementation
