#!/usr/local/bin/perl
# Enable the Minecraft server at boot, or not

use strict;
use warnings;
require './minecraft-lib.pl';
our (%text, %in, %config);
&ReadParse();

&foreign_require("init");
my $starting = &init::action_status($config{'init_name'});
if ($starting != 2 && $in{'boot'}) {
	# Enable at boot
	my $pidfile = &get_pid_file();
	my $startcmd = &get_start_command()." & echo \$! >$pidfile";
	my $stopcmd = "kill `cat $pidfile` && rm -f $pidfile";
	&init::enable_at_boot($config{'init_name'},
		"Start Minecraft server",
		$startcmd,
		$stopcmd,
		undef,
		{ 'fork' => 1 },
		);
	&webmin_log("atboot");
	}
elsif ($starting == 2 && !$in{'boot'}) {
	# Disable at boot
	&init::disable_at_boot($config{'init_name'});
	&webmin_log("delboot");
	}

&redirect("");

