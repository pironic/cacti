#!/usr/bin/perl
use warnings;
use strict;
use LWP::Simple;
use Date::Parse;
use Switch;

my $timeout = 200;
my $total_time = 36;
my $httpaddr = "http://www.weatheroffice.gc.ca/almanac/almanac_e.html?yyc";
my $content;
my $fail = 0;
my $tries = 0;
my %data;
my %trash;
my @keys;
my @units;

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

# find the now table.
my $indexOfStart = index($content, "<table summary=");
my $indexOfEnd = index($content, "</table>", $indexOfStart);

my $_ = substr($content,$indexOfStart,$indexOfEnd - $indexOfStart);
#print $_;

#s/nbsp;/ /g;
#s/<.+?>//g;
#s/\s+/ /g;

#whats on the site vs what do we want to output
@keys = ("avg_max_temp","avg_min_temp","freq_precip","max_temp","min_temp","max_precip","max_rain","max_snowfall","max_snowOnGround");
@units = ("&deg;C","&deg;C","%","&deg;C","&deg;C","mm","mm","cm","cm");

my $n = 0;
my $indexValue = index($_,"<td headers=\"header1 header", 0);
for(; $indexValue != -1;)
{
   my $indexValueStart = index($_,">",$indexValue)+1;
   my $indexValueEnd = index($_,$units[$n],$indexValue+2);

   my $temp = $keys[$n];
   #print "debug: " . $temp . ":" .substr($_,$indexValueStart,$indexValueEnd-$indexValueStart);
     $data{$temp} = substr($_,$indexValueStart,$indexValueEnd-$indexValueStart);

   #print substr($_,$indexValueStart,$indexValueEnd-$indexValueStart) . "\n";
   $indexValue = index($_,"<td headers=\"header1 header",$indexValue+1);
   $n++;
}

for (keys %data) {
  printf "%s:%s ", $_, $data{$_};
}
print "\n";
