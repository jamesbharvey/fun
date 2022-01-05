#!/usr/bin/perl

use strict;
use warnings;
use File::pushd;
use File::Copy 'move';

for (<*>) {
    next if /^\./;
    next unless -d;
    my $dir = pushd $_;
    opendir(my $dh, '.') || die "Can't open /!!: $!";
    while (my $file = readdir $dh) {
	next if $file =~ /^\./;
	print "$file\n";
	die "file already exists!!" if -e "../$file";
	move $file, "../$file";
    }
    closedir $dh;
    #popd; happens automagically
}
