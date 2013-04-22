#!/usr/bin/perl
use warnings;
use strict;
use LWP::Simple;
use Date::Parse;
use Switch;

my $timeout = 200;
my $total_time = 36;
my $httpaddr =  $ARGV[0];
my $content;
my $fail = 0;
my $tries = 0;
my %data;
my %trash;
my @keys;

do{
  eval {
    local $SIG{ALRM} = sub { die "alarm\n" };
    alarm $timeout;
    $tries++;
    $content = LWP::Simple::get($httpaddr);
    alarm 0;
  };
} while (!$content && $tries <= int($total_time / $timeout));

$data{Tries} = $tries;

if (!$content) {
  exit(2);
}

my @values = split(' ',$content);

foreach my $val (@values) {
  print "$val ";
}

