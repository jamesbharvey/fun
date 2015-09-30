#!/usr/bin/perl

use feature qw(say);
use warnings;
use strict;
use autodie;
use Data::Dumper;
use FindBin;
use lib "$FindBin::Bin/../lib/perl";
use Number::Bytes::Human qw(format_bytes);
use Term::ReadLine;
use File::Basename qw(basename);
use Getopt::Long qw(GetOptions);

my $test;
my $noprompt;

GetOptions("test"     => \$test,
           "noprompt" => \$noprompt)
    or die "Error in command line arguments.\n";

my %files;
my %unduplicated;

my $term = Term::ReadLine->new('CB[RZ] deduper');

my $remaining_bytes = 0;

sub add_entry {
    my $filename = shift;
    my $key = canonicalize($filename);
    $files{$key} ||= []; 
    push @{$files{$key}} ,$filename;
}

sub canonicalize {
    my $filename = shift;
    $filename = basename($filename);      #strip directory if there
    $filename =~ s/\.cb[rz]$//i;          #strip file type
    $filename =~ s/\([^\(\)]*?\)//g;      #get rid of anything inside any ()'s
    $filename =~ s/\s+/ /g;               #replace multiple whitespace chars with one
    $filename =~ s/^\s+//;                #strip leading whitespace
    $filename =~ s/\s+$//;                #strip trailing whitespace
    $filename =~ s/(\b)0+(\d+\b)/$1$2/g;  #strip leading zeroes in numbers
    $filename = lc $filename;
    return $filename;
}

while (<*/*.cbr>) {
    add_entry($_);
}
while (<*/*.cbz>) {
    add_entry($_);
}

# we only want to delete duplicates

for (keys %files) {
    next if @{$files{$_}} > 1;
    $unduplicated{$_} = delete $files{$_};
    $remaining_bytes += (stat $unduplicated{$_}->[0])[7];
}


# keep only the smallest file

my $bytes_saved = 0;
my $num_files_deleted = 0;
my $prompt = "Execute:y/n?";

for my $key (keys %files) {
    my @candidates = map { [ $_ , (stat($_))[7] ] } @{$files{$key}};
    @candidates = sort { $a->[1] <=> $b->[1] } @candidates;
    my $keep = shift @candidates;

    say "#######################################################";
    say "Keep:   ",$keep->[0] , ", ",format_bytes($keep->[1]);
    for (@candidates) {
        say "Delete: ",$_->[0] , ", ",format_bytes($_->[1]);
    }
    say "#######################################################";

    if ($test) {
	$num_files_deleted++;
	for (@candidates) {
	    $bytes_saved += $_->[1];
	}
	next;
    }

    if ($noprompt) {
        for (@candidates) {
            say "deleting [",$_->[0],"]....";
            if (unlink $_->[0]) {
                $num_files_deleted++;
                $bytes_saved += $_->[1];
            } else {
                warn "Could not unlink $_->[0]: $!";
            }
        }
	next;
    }

    my $have_answer = 0;
    my $answer;
    while ( not $have_answer ) {
        $answer = lc $term->readline($prompt);
        $have_answer = ($answer eq 'y' or $answer eq 'n') ? 1 : 0;
        last if $have_answer;
        say "Please answer y or n."
    }
    if ($answer eq 'y') {
        for (@candidates) {
            say "deleting [",$_->[0],"]....";
            if (unlink $_->[0]) {
                $num_files_deleted++;
                $bytes_saved += $_->[1];
            } else { 
                warn "Could not unlink $_->[0]: $!";
            }

        }
    }
    if ($answer eq 'n') {
        say "Skipping deletion......:";
    } 
}

say "[$num_files_deleted] files deleted saving [",format_bytes($bytes_saved),"] of space.";
say "[",scalar(keys %unduplicated) + scalar(keys %files),"] unique files remaining for [",format_bytes($remaining_bytes),"]."




