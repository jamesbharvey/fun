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
    return 1 if is_mounted($dir);
    system "mkdir","-p","/tmp/uriah/$dir";
    system "mount","-t","smbfs", "smb://videos:1\@uriah/$dir", "/tmp/uriah/$dir";
}

do_mount("Grown-ups");
do_mount("KidsVideo");
do_mount("books"); 
do_mount("comics");

opendir(my $dh, ".") || die;
my @dirs = grep { !/^\./ && -d $_ } readdir $dh;
closedir $dh;

for my $dir (@dirs) {
    my $dir_to_pop = pushd $dir; # pop happens automagically
    next unless -s "move_tv_shows_to.txt";
    open my $dest_fh, "move_tv_shows_to.txt";
    my $dest_path = <$dest_fh>;
    chomp $dest_path;
    close $dest_fh;

    opendir(my $dh, ".") || die;
    my @to_move = grep { !/^\./ && ($_ ne "move_tv_shows_to.txt") } readdir $dh;
    closedir $dh;
    system "mkdir","-p","/tmp/uriah/$dest_path";
    for my $item (@to_move) {
	print  "mv \"$item\" /tmp/uriah/$dest_path","\n";
	system "mv", "-vn","$item", "/tmp/uriah/$dest_path";
    }
}

system "umount","/tmp/uriah/Grown-ups";
system "umount","/tmp/uriah/KidsVideo";
system "umount","/tmp/uriah/books";
system "umount","/tmp/uriah/comics";

