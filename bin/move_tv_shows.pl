#!/usr/bin/perl

use feature qw(say);
use warnings;
use strict;
use autodie;
use Data::Dumper;
use FindBin;
use lib "$FindBin::Bin/../lib/perl";
use File::pushd;

#mount -t smbfs smb://admin:password@win/share
#mv Arrow.S04E09.720p.HDTV.X264-DIMENSION\[rarbg\]/ /tmp/uriah/Video/TV/Arrow

system "mkdir -p /tmp/uriah/Grown-ups";
system "mkdir -p /tmp/uriah/KidsVideo";

#system "mount -t smbfs smb://videos:1\@uriah/Grown-ups /tmp/uriah/Grown-ups";
system "mount -t smbfs smb://videos:1\@uriah/KidsVideo /tmp/uriah/KidsVideo";

opendir(my $dh, ".") || die;
my @tvdirs = grep { !/^\./ && -d $_ } readdir $dh;
closedir $dh;

for my $dir (@tvdirs) {
    my $dir_to_pop = pushd $dir; # pop happens automagically
    next unless -s "move_tv_shows_to.txt";
    open my $dest_fh, "move_tv_shows_to.txt";
    my $dest_path = <$dest_fh>;
    chomp $dest_path;
    close $dest_fh;
    $dest_path =~ s/ /\\ /g;
    opendir(my $dh, ".") || die;
    my @to_copy = grep { !/^\./ && ($_ ne "move_tv_shows_to.txt") } readdir $dh;
    closedir $dh;
    for my $item (@to_copy) {
	$item =~ s/ /\\ /g;
	print  "mv $item /tmp/uriah/$dest_path","\n";
	system "mv $item /tmp/uriah/$dest_path";

    }
}



