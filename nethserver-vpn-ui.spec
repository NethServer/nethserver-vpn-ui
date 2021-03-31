Summary: NethServer VPN UI module
Name: nethserver-vpn-ui
Version: 1.6.4
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
(cd root; find . -depth -print | cpio -dump %{buildroot})

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/nethserver-vpn-ui/
tar xf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/nethserver-vpn-ui/

%{genfilelist} %{buildroot} --file /etc/sudoers.d/50_nsapi_nethserver_vpn_ui 'attr(0440,root,root)' > %{name}-%{version}-filelist
echo "%doc COPYING" >> %{name}-%{version}-filelist


%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)

%changelog
* Wed Mar 31 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.4-1
- IPSEC: Tunnel name cannot contain spaces - Bug NethServer/dev#6469

* Thu Jan 28 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.3-1
- Delete conntrack connection with ipsec tunnel - NethServer/dev#6393

* Mon Jan 11 2021 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.2-1
- UI issue on tables using vue-good-table - Bug NethServer/dev#6390

* Wed Dec 16 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.1-1
- OpenVPN RW: sorting not working on accounts table - Bug NethServer/dev#6360

* Tue Dec 01 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.0-1
- RemoteNetworks also with the subnet topology - NethServer/dev#6345

* Fri Nov 20 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.5-1
- OpenVPN: Display a FQDN placeholder When Remote is empty - NethServer/dev#6337

* Thu Nov 19 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.4-1
- OpenVPN RW: certificate not created if account name contains key spaces - Bug NethServer/dev#6336

* Tue Aug 25 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.3-1
- VPN Roadwarrior: unable to load accounts - Bug NethServer/dev#6242

* Thu Jul 02 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.2-1
- Human readable numbers in Cockpit dashboards - NethServer/dev#6206

* Mon Jun 08 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.1-1
- OpenVPN: custom mail text - NethServer/dev#6193

* Fri May 29 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.0-1
- OpenVPN Tunnels: Cannot disable WAN priority rule - Bug NethServer/dev#6182
- OpenVPN RW: Don't restart service immediately on user creation/deletion - NethServer/dev#6177

* Wed May 06 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.0-1
- VPN RW: optional push dhcp settings - NethServer/dev#6146
- VPN RW: Export connection history - NethServer/dev#6147
- VPN RW: Show client-to-client mode in bridged mode - Bug NethServer/dev#6148

* Wed Apr 29 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.1-1
- VPN R2W : Custom certificate EOL - NethServer/dev#6145
- nethserver-vpn-ui: display the shortname before to email the client configuration - NethServer/dev#6142

* Tue Apr 28 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.0-1
- nethserver-vpn: textarea save empty line - Bug NethServer/dev#6141
- Use subnet topology for OpenVPN roadwarrior - NethServer/dev#6133
- OpenVPN: New policy certificate-otp for RW - NethServer/dev#6112

* Fri Apr 03 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.11-1
- Pasting PSK Missing newline OVPN P2P - Bug NethServer/dev#6103

* Wed Mar 04 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.10-1
- Cockpit : OpenVPN tunnel client p2p mode not working - Bug NethServer/dev#6077

* Wed Feb 05 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.9-1
- Cockpit - VPN. IPSec improvements - NethServer/dev#6049

* Wed Dec 18 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.8-1
- Cockpit: the wan pppoe cannot be selected in the ipsec menu - Bug NethServer/dev#5989

* Mon Dec 16 2019 Davide Principi <davide.principi@nethesis.it> - 1.2.7-1
- Cockpit: firefox downloaded files are not named properly - Bug NethServer/dev#5988
- ui. fixed missing popup with vpn stats

* Fri Nov 22 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.6-1
- OpenVPN: re-created user can't access roadwarrior server - Bug NethServer/dev#5949

* Thu Nov 21 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.5-1
- UI: domain menu not correctly shown - Bug Nethserver/dev#5942

* Thu Nov 21 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.4-1
- OpenVPN tunnel: Wrong protocol written in the client configuration file - Bug NethServer/dev#5929

* Mon Oct 28 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.3-1
- Cockpit: error in managing more than 100 tunnels openvpn-server - Bug Nethserver/dev#5886
- Logs page in Cockpit - Bug NethServer/dev#5866

* Thu Oct 10 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.2-1
- Cockpit: improve English labels - NethServer/dev#5856

* Mon Oct 07 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.1-1
- Cockpit downloads fail on Firefox - Bug Nethserver/dev#5855

* Tue Oct 01 2019 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.0-1
- OpenVPN RW: host duplication when editing reserved IP - Bug NethServer/dev#5850
- Sudoers based authorizations for Cockpit UI - NethServer/dev#5805

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
