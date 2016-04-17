#!/usr/bin/perl

use feature qw(say);
use warnings;
use strict;
use autodie;
use Data::Dumper;
use FindBin;
use lib "$FindBin::Bin/../lib/perl";
use File::pushd;



sub my_system
{
    say join " ",@_;
    die @_ unless 0 == system @_;
}

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
    return 1 if is_mounted $dir;
    my_system "mkdir","-p","/tmp/uriah/$dir";
    my_system "mount","-t","smbfs", "smb://videos:1\@uriah/$dir", "/tmp/uriah/$dir";
}

do_mount "Grown-ups";
do_mount "KidsVideo";
do_mount "books"; 
do_mount "comics";

opendir(my $dh, ".") || die;
my @dirs = grep { !/^\./ && -d $_ } readdir $dh;
closedir $dh;

for my $dir (@dirs) {
    my $dir_to_pop = pushd $dir; # pop happens automagically
    my $dest_file;
    $dest_file = "move_tv_shows_to.txt " if -s "move_tv_shows_to.txt";
    $dest_file = "move_media_files_to.txt " if -s "move_media_files_to.txt";
    next unless defined $dest_file;
    open(my $dest_fh, $dest_file);
    my $dest_path = <$dest_fh>;
    chomp $dest_path;
    close $dest_fh;

    opendir my $dh, ".";
    my @to_move = grep { !/^\./ && ($_ ne "move_tv_shows_to.txt") && ($_ ne "move_media_files_to.txt") } readdir $dh;
    closedir $dh;
    my_system "mkdir","-p","/tmp/uriah/$dest_path";
    for my $item (@to_move) {
	my_system "mv", "-vn","$item", "/tmp/uriah/$dest_path";
    }
}

my_system "umount","/tmp/uriah/Grown-ups";
my_system "umount","/tmp/uriah/KidsVideo";
my_system "umount","/tmp/uriah/books";
my_system "umount","/tmp/uriah/comics";

