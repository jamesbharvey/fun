#!/usr/bin/perl

use feature qw(say);
use warnings;
use strict;
use autodie;
use Data::Dumper;
use FindBin;
use lib "$FindBin::Bin/../lib/perl";
use File::pushd;


sub is_mounted
{
    my $dir = shift;
    $dir = qr{$dir};
    my @mount_output = `mount`;
    for (@mount_output) {
	return 1 if /\b\/tmp\/uriah\/$dir\b/;
    }
    return 0;
}

sub do_mount
{
    my $dir = shift;
    system "mkdir","-p","/tmp/uriah/$dir";
    system "mount","-t","smbfs", "smb://videos:1\@uriah/$dir", "/tmp/uriah/$dir";
}

do_mount("Grown-ups") if not is_mounted("Grown-ups");
do_mount("KidsVideo") if not is_mounted("KidsVideo");
 
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
    $dest_path =~ s/([)(])/\\$1/g;

    opendir(my $dh, ".") || die;
    my @to_copy = grep { !/^\./ && ($_ ne "move_tv_shows_to.txt") } readdir $dh;
    closedir $dh;
    for my $item (@to_copy) {
	$item =~ s/ /\\ /g;
	print  "mv $item /tmp/uriah/$dest_path","\n";
	system "mv", "$item", "/tmp/uriah/$dest_path";
    }
}

system "umount","/tmp/uriah/Grown-ups";
system "umount","/tmp/uriah/KidsVideo";

