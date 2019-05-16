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
