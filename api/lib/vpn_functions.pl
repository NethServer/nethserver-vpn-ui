#!/usr/bin/perl

#
# Copyright (C) 2019 Nethesis S.r.l.
# http://www.nethesis.it - nethserver@nethesis.it
#
# This script is part of NethServer.
#
# NethServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# NethServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NethServer.  If not, see COPYING.
#

use strict;
use warnings;
use JSON;
use esmith::ConfigDB;
use NetAddr::IP;

require '/usr/libexec/nethserver/api/lib/helper_functions.pl';

sub ipsec_status {
    my $ret;
    open(FH, "ipsec whack --trafficstatus|");
    while (<FH>) {
        # remove connection number
        $_ =~ s/^(.*:\s+)//;
        my ($name, $type, $started, $in, $out, $id) = split(/, /);
        $name =~ /^"(.*)_/; # extract tunnel name
        $name = $1;
        # cleanup vars
        $type =~ s/^(.*)=//;
        $started =~ s/^(.*)=//;
        $in =~ s/^(.*)=//;
        $out =~ s/^(.*)=//;
        $ret->{$name} = {
            type => $type,
            started => $started,
            received_bytes => $in,
            sent_bytes => $out
        }
    }
    close(FH);

    return $ret;
}

sub random {
    my $min = shift;
    my $max = shift;

    return int(rand($max-$min)) + $min;
}

sub is_used_network {
    my $net = shift;
    my $exclude = shift || '';

    my $db = esmith::ConfigDB->open_ro();
    my $vdb = esmith::ConfigDB->open_ro('vpn');

    # check inside tunnels
    foreach ($vdb->get_all()) {
        next if ($_->key eq $exclude || $_->prop('type') eq 'openvpn-tunnel-server');
        return 1 if (($_->prop('Network') || '') eq $net);
    }

    # check host to net server
   my $addr = $db->get_prop('openvpn@host-to-net', 'Network');
   my $mask = $db->get_prop('openvpn@host-to-net', 'Netmask');
   if ($addr && $mask) {
       my $hnet = NetAddr::IP->new($addr, $mask);
       return 1 if ($hnet->network."" eq $net);
   }

   return 0;
}

sub is_used_port {
    my $port = shift;
    my $exclude = shift || '';

    my $db = esmith::ConfigDB->open_ro();
    my $vdb = esmith::ConfigDB->open_ro('vpn');

    # check inside tunnels
    foreach ($vdb->get_all()) {
        next if ($_->key eq $exclude || $_->prop('type') eq 'openvpn-tunnel-server');
        return 1 if (($_->prop('Port') || '') eq $port);
    }

    # check host to net server
    return 1 if ($db->get_prop('openvpn@host-to-net','UDPPort') eq $port);

    return 0;
}

sub openvpn_algorithms {
    my $ret = {'ciphers' => [], 'digests' => []};

    open(FH, "/usr/sbin/openvpn --show-ciphers|");
    while (<FH>) {
        if (index($_,'(')>=0) {
            my $description = 'weak';
            my @tmp = split(/\s+/, $_);
            if ($tmp[0] =~ m/(192|256|384|512)/) {
                $description = 'strong';
            }
            push(@{$ret->{'ciphers'}}, {name => $tmp[0], description => $description});
        }
    }
    close(FH);

    open(FH, "/usr/sbin/openvpn --show-digests|");
    while (<FH>) {
        if (index($_,'bit')>=0) {
            my $description = 'weak';
            my @tmp = split(/\s+/, $_);
            if ($tmp[0] =~ m/(224|256|384|512|whirlpool)/) {
                $description = 'strong';
            }
            push(@{$ret->{'digests'}}, {name => $tmp[0], description => $description});
        }
    }
    close(FH);

    return $ret;
}
