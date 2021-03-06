#!/usr/bin/perl
use warnings;
use strict;
use LWP::Simple;
use Date::Parse;
use Switch;

my $timeout = 200;
my $total_time = 36;
my $httpaddr =  "http://raptr.com/" . $ARGV[0] . "/games";
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

# find the now table.
my $indexOfStart = index($content, "class=\"about\"");
my $indexOfEnd = index($content, "<div class=\"ft hidden\"><\/div>\n", $indexOfStart);

my $_ = substr($content,$indexOfStart,$indexOfEnd - $indexOfStart);

#s/nbsp;/ /g;
#s/<.+?>//g;
#s/\s+/ /g;
print $content;

# @keys = ("Temperature","WindDirection","WindSpeedLow","WindSpeedHigh","BaroPressure","Precipitation","Lightning","QueryTime");

# my $n = 0;
# my $indexValue = index($_,"<td class=\"value\"", 0);
# for(; $indexValue != -1;)
# {
   # my $indexValueStart = index($_,">",$indexValue)+1;
   # my $indexValueEnd = index($_,"<",$indexValue+2);

   # my $temp =  $keys[$n];
   # #print "debug: " . $temp;
   # if ($temp eq "WindDirection") {
     # #god damned wind direction
     # switch(substr($_,$indexValueStart,$indexValueEnd-$indexValueStart)) {
       # case ("N") { $data{WindDirection} = 1; }
       # case ("NNE") { $data{WindDirection} = 1.5; }
       # case ("NE") { $data{WindDirection} = 2; }
       # case ("NEE") { $data{WindDirection} = 2.5; }
       # case ("E") { $data{WindDirection} = 3; }
       # case ("SSE") { $data{WindDirection} = 3.5; }
       # case ("SE") { $data{WindDirection} = 4; }
       # case ("SEE") { $data{WindDirection} = 4.5; }
       # case ("S") { $data{WindDirection} = 5; }
       # case ("SSW") { $data{WindDirection} = 5.5; }
       # case ("SW") { $data{WindDirection} = 6; }
       # case ("SWW") { $data{WindDirection} = 6.5; }
       # case ("W") { $data{WindDirection} = 7; }
       # case ("NNW") { $data{WindDirection} = 7.5; }
       # case ("NW") { $data{WindDirection} = 8; }
       # case ("NWW") { $data{WindDirection} = 8.5; }
       # else { $data{WindDirection} = 9; }
     # }
   # } elsif ($temp eq "QueryTime") {
     # my $tempDate = substr($_,$indexValueStart,($indexValueEnd-$indexValueStart)-6);
     # my $tempTime = substr($_,$indexValueEnd-5,5);

     # $data{$temp} = str2time($tempDate . " 2011 " . $tempTime);
   # } else {
     # # not wind direction so just store it
     # $data{$temp} = substr($_,$indexValueStart,$indexValueEnd-$indexValueStart);
   # }

   # #print substr($_,$indexValueStart,$indexValueEnd-$indexValueStart) . "\n";
   # $indexValue = index($_,"<td class=\"value\"",$indexValue+1);
   # if ($indexValue == -1) {
     # $indexValue = index($_,"id=\"timestamp\">",$indexValueEnd);
   # }
   # $n++;
# }

# for (keys %data) {
  # printf "%s:%s ", $_, $data{$_};
# }
print "\n";
