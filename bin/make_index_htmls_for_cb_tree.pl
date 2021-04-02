#!/usr/bin/perl

use feature qw(say);
use warnings;
use strict;
use autodie;
use FindBin;
use lib "$FindBin::Bin/../lib/perl";
use File::pushd;

my @directories = `find . -type d`;
@directories = grep { ! /^\.$/ } @directories;
@directories = sort @directories;

for my $dir (@directories) {
    chomp $dir;
    next if -f "$dir/index.html";
    next if $dir =~ /cant\_unrar/;
    say "doing dir:$dir";
    opendir(my $handle, $dir);
    my @items = readdir($handle);
    @items = grep { /\.(cbr|cbz|pdf)$/i } @items; 
    if (@items > 0) {
        my $dir_to_pop = pushd $dir; # pop happens automagically
        system("~/fun/bin/cbthumb");
    }
}
