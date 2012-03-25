#!/usr/bin/tclsh8.5
# requires Tcldot (loaded later if graph not cached)
lappend auto_path /usr/lib/tcltk/graphviz/
package require Tcldot
set WWW /Home/staff/stric/public_html/tmp/webdot
set CACHE "$WWW/cache"
set MYDATA "$WWW/data"

# directory containing TrueType fonts for GIFs
set TTFDIR /pkg/fonts/ttf
set env(DOTFONTPATH) $TTFDIR

# ghostscript is used for .pdf
set GS /usr/local/bin/gs

# ps2epsi is used for .epsi (ps2epsi is a part of gs)
#
# NB: The ps2epsi shell script was modified to explicitly 
# set PATH for all its supporting executables. The CGI 
# environment does not provide a useful PATH.
set PS2EPSI /usr/local/bin/ps2epsi

# That should be all that needs adjusting in new installations


#######################################################################
# Copyright (c) Lucent Technologies. 1994, 1995, 1996, 1997, 1998.    #
#                                                                     #
# This code is licensed by AT&T Corp.  For the terms and conditions   #
# of the license, see http://www.research.att.com/sw/tools/graphviz   #
#######################################################################

#######################################################################
# WebDot, the Server                                                  #
#                                                                     #
# John Ellson, ellson@lucent.com                                      #
#######################################################################

##### TO DO #####
# - provide an annotated dot file in html for lynx clients
# - pass on other response codes directly to client
# - handle TZ in Expires header
# - add http_proxy and no_proxy support
# - improve organization of this code for easier maintenance
# - client side get-if-modified-since support
# - form for simple url to dot file
# - form for direct dot graph entry
#################

# prefix exceptions with valid http header
proc error {m} {
	puts "Content-Type: text/plain\n\n$m"
	exit
}
proc unknown {m args} {error "Invalid command name: $m"}

# define the set of mime.types that we can convert graphs to
set mime(dot)   "application/x-dot"
set mime(gif)   "image/gif"
set mime(mif)   "application/x-mif"
set mime(hpgl)  "application/x-hpgl"
set mime(pcl)   "application/x-pcl"
set mime(tcl)   "application/x-tcl"
set mime(vrml)  "x-world/x-vrml"
set mime(vtx)   "application/x-vtx"
set mime(ps)	"application/postscript"
set mime(epsi)	"application/postscript"
set mime(pdf)	"application/pdf"
set mime(map)   "text/plain"
set mime(tclmap) "text/plain"
set mime(txt)   "text/plain"
set mime(src)   "text/plain"

# Used to process Expires headers that come in all flavors ;-(
proc convert_time {s} {
	# converts various time formats into ticks
	# the first two formats are accepted by tcl's clock scan
	# the requirements for these format comes from RFC 2068 (HTTP/1.1)

### the preferred format of RFC 822, updated by RFC 1123
### e.g. "Sun, 06 Nov 1994 08:49:37 GMT"

### ANSI C's asctime() format
### e.g. "Sun Nov  6 08:49:37 1994"

	if {![catch {clock scan $s -gmt 1} t]} {return $t}

### RFC 850, obsoleted by RFC 1036  (deprecated because of 2 digit year)
### e.g. "Sunday, 06-Nov-94 08:49:37 GMT"

	if {[scan $s {%*s %[^-]-%[^-]-%s %[^:]:%[^:]:%s %*s} \
			dy mo yr hr mi sc] == 6} {
		# at least this shouldn't die at the same time as everybody elses ;-)
		if {$yr < 96} {set yr 20$yr} {set yr 19$yr}
	} {
		error "Failure to recognize date format: $s"
	}

	# January is represented as month 1
	set mo [lsearch {- Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec} $mo]
	if {[catch {clock scan "$mo/$dy/$yr $hr:$mi:$sc" -gmt 1} t]} {
		error "Failure to match date format: $s"
	}
	return $t
}

# get a url over the net
proc get {url cache_dir no_cache} {
	set timeout 60000

	# parse the url into component parts
	if {[scan $url {%[^:]://%[^/]%s} protocol serverport path] != 3} {
		error "bad URL $url"
	}
	if {[scan $serverport {%[^:]:%s} server port] == 1} {set port 80}
	# prepare cache for result
	set ResponseCode ""
	set LastModified ""
	set Expires ""
	regsub -all {~} $path {%7E} path
	set cache_dir $cache_dir/$protocol/$serverport$path
	if [file isdirectory $cache_dir] {
		if {! [catch {open $cache_dir/.info r} f]} {
			foreach {LastModified Expires} [read $f] {break}
			close $f
		}
	} {
		if {[catch {file mkdir $cache_dir}]} {
			error "failure to create cache directory: $cache_dir"
		}
	}
	set LocalTime [clock seconds]

	# see if source is a local file
	if {$protocol == "file" && $server == "localhost"} {
		if {![file exists $cache_dir/.src]} {
			exec ln -s $path $cache_dir/.src
		}
		set LastModified [clock format [file mtime $path] \
			-format {%a, %d %b %Y %T GMT} -gmt 1]

	# see if we can use straight from cache
	} elseif {$Expires == "" || $no_cache \
	  || [convert_time $Expires] < $LocalTime} {
		# no - so open connection to server
		if {$protocol != "http" || $server == "localhost"} {
			error "unsupported url: $url"
		}
		if {[catch {socket $server $port} skt]} {
			error "failure to connect to $server:$port"
		}

		# send request
		regsub -all {%7E} $path {~} lpath
		puts $skt "GET $lpath HTTP/1.0"
		puts $skt "User-Agent: webdot"
		puts $skt "Accept: */*"
		if {$no_cache} {
			puts $skt "Pragma: no-cache"
		} {
			if {$LastModified != ""} {
				puts $skt "If-Modified-Since: $LastModified"
			}
		}
		puts $skt ""
		flush $skt

		# get response
		set start [clock seconds]
		set inbody 0
		while {$inbody < 2} {
			set selread {}
			after $timeout "error \"timeout on select read from $url\""
			fileevent $skt readable "set selread $skt"
			vwait selread
			after cancel "error \"timeout on select read from $url\""
			if {! $inbody} {
				# still processing header
				if {[catch {gets $skt} line]} {
					error "failure reading from: $url\r\nresponse was: $line"
				}
				regsub -all \r $line {} line
				switch [string tolower [lindex $line 0]] {
					"http/1.0" - "http/1.1" {
						scan $line {%*s %d %*s} ResponseCode
						switch $ResponseCode {
							200 {
								if {[catch {open $cache_dir/.src w} f_src]} {
									error "failure to open $cache_dir/.src for write"
								}
							}
							304 {set inbody 2}
 							404 {
								error "URL \"$protocol://$server:$port$lpath\" was not found"
							}
							default {
								error "Response Code = $ResponseCode"
							}
						}
					}
					"last-modified:" {scan $line {%*s %[^~]} LastModified}
					"expires:" {scan $line {%*s %[^~]} Expires}
					"" {
						incr inbody
						if {$ResponseCode == "200"} {
							if {[catch {open $cache_dir/.info w} f_info]} {
								error "failure to open $cache_dir/.info for write"
							}
							puts -nonewline $f_info [list $LastModified $Expires]
							close $f_info
						}
					}
				}
			} {
				# in body - copy directly so no prob with binary data
				fconfigure $skt -translation binary
				fconfigure $f_src -translation binary
				fcopy $skt $f_src
				close $f_src
				incr inbody
			}
		}
		close $skt
	}

	# return directory containing cached copy (in .src) and timestamps
	return [list $cache_dir $LastModified $Expires]
}

# URL attributes of graph objects can be relative, and URLs of nodes
# can contain the escape sequence "\N" which will be replaced by the
# name of the node
proc make_absolute_url {protocol serverport dirname ref name} {
	regsub -all {\\N} $ref $name ref
	if {[scan $ref {%[^:]://%s} . .] != 2} {
		if {[string range $ref 0 0] == "/"} {
			set ref $protocol://$serverport$ref
		} {
			set ref $protocol://$serverport/$dirname/$ref
		}
	}
	return $ref
}

#--------------------------------------
# some shorthand procs for generating html pages

proc head {t} {
	return "Content-Type: text/html

<html>
<head>
<title>$t</title>
</head>
<body bgcolor=#ffffff>
<h1>$t</h1>"
}

proc tail {} {
	return {</hr>
<address>
<a href=mailto:ellson@lucent.com>jce</a>
</address>
</body>
</html>}
}

proc include {fn} {
	if {[catch {open $fn r} f]} {
		error "Unable to open $fn for read"
	}
	set a [read $f]
	close $f
	return $a
}

#--------------------------------------
# check cgi environment
if {![info exists env(SERVER_NAME)]} {error "Missing: SERVER_NAME"}
if {![info exists env(SERVER_PORT)]} {error "Missing: SERVER_PORT"}
if {![info exists env(SCRIPT_NAME)]} {error "Missing: SCRIPT_NAME"}
if {![info exists env(REQUEST_METHOD)] \
  || [lsearch {GET HEAD} $env(REQUEST_METHOD)] == -1} {
	error "Missing or unsupported: REQUEST_METHOD"
}
set server_port ":$env(SERVER_PORT)"
if {$server_port == ":80"} {set server_port {}}
set SELF http://$env(SERVER_NAME)$server_port$env(SCRIPT_NAME)
if {![info exists env(PATH_INFO)]} {
	set path_info "/"
} {
	regsub -all {\%3D} $env(PATH_INFO) {=} path_info
}
if {[info exists env(HTTP_IF_MODIFIED_SINCE)]} {
	set IfModifiedSince $env(HTTP_IF_MODIFIED_SINCE)
} {
	set IfModifiedSince {}
}
set no_cache 0
if {[info exists env(HTTP_PRAGMA)] && $env(HTTP_PRAGMA) == "no-cache"} {
	set no_cache 1
}

# check legal url for this application
if {[scan $path_info {/%[^=]=%s} type url] == 2} {
	# deprecated path_info format -  "/type=source_url"
	# retained for compatibility with old webdot
	# clients that use the file extension of the URL don't work with this
	if {[scan $url {%[^:]://%[^/]/%s} protocol serverport path] != 3} {
	   error "Unable to find URL in: $path_info"
	}
} {
	# prefered path_info format - "/source_url.type"
	# still not perfect. Now I have to hassle with file extents
	if {[scan $path_info {/%[^:]://%[^/]/%s} protocol serverport path] != 3} {
		set protocol http
		set serverport $env(SERVER_NAME)$server_port
		set path_info $env(SCRIPT_NAME)/[file tail $path_info]
		scan $path_info {/%s} path
	}
	set protocol [file tail $protocol]
	regsub -all {~} $path {%7E} p
	set type [file extension $p]
	if {[set l [string length $type]] > 1} {
		set path [string range $path 0 [expr [string length $path] - $l - 1]]
		set type [string range $type 1 end]
	}
	set url $protocol://$serverport/$path
}
regsub -all {~} $path {%7E} p
if {[string index $p [expr [string length $p] - 1]] == "/"} {
	set fn ""
} {
	set fn [file tail $p]
}
set ft [file extension $p]
set dirname [string range $path 0 [expr [string length $path] \
									  - [string length $fn] - 2]]
# now check for security
if {$protocol != "http"} {
	error "This application only supports http: urls."
}
scan $serverport {%[^:]:%s} server port
if {$server == "localhost"} {
	error "Nice try, but you can't see our files that way!"
}

# if it is a pointer to this server then make sure that only
#	local data is allowed
if {[scan $url "$SELF%s" path] == 1} {
	set path_info $env(SCRIPT_NAME)/$fn
	scan $path_info {/%s} path
}

# type ismap is deprecated - retained for backward compatibility
if {$type == "ismap"} {set type map}

# Pretend to be a file server to emit some adaptive pages
if {$type == "help"
  || $type == "tclhelp"
  || ("/$dirname" == $env(SCRIPT_NAME) && $ft == "")} {
	if {$fn != {} && $type != "help" && $type != "tclhelp" && $type != {}} {
		set fn $fn.$type
		set ft .$type
	}

	if {$fn == {} 
	  || $fn == "index.html"
	  || $type == "help"
	  || $type == "tclhelp"} {
		puts "[head {Webdot Graph Server}]"
		if {$type == "help" || $type == "tclhelp"} {
			puts "goo $url"
			set graph $url
		} {
			set graph $SELF/demo.dot
		}
		if {$type == "tclhelp"} {
			puts "<embed width=600 height=400 src=$SELF/$graph.tcl>"
		} {
			puts "<a href=$SELF/$graph.map>
<img src=$SELF/$graph.gif ismap>
</a>"
		}

		puts "<p>
<h3>WebDot can serve <a href=$SELF/$graph.src>this graph</a> (dot source)
in the following formats:</h3>
<table border=0><tr>
<td><a href=$SELF/$graph.src>text/plain(dot source)</a></td>
<td><a href=$SELF/$graph.gif>image/gif</a></td>
<td><a href=$SELF/$graph.map>text/plain(imagemap)</a></td>
</tr><tr>
<td><a href=$SELF/$graph.pcl>application/x-pcl</a></td>
<td><a href=$SELF/$graph.hpgl>application/x-hpgl</a></td>
<td><a href=$SELF/$graph.dot>application/x-dot</a></td>
</tr><tr>
<td><a href=$SELF/$graph.pdf>application/pdf(PDF)</a></td>
<td><a href=$SELF/$graph.ps>application/postscript(PS)</a></td>
<td><a href=$SELF/$graph.epsi>application/postscript(EPSI)</a></td>
</tr><tr>
<td><a href=$SELF/$graph.tcl>application/x-tcl(Tclet)</a></td>
<td><a href=$SELF/$graph.mif>application/x-mif(FrameMaker)</a></td>
</tr><tr>
<td><a href=$SELF/$graph.vrml>x-world/x-vrml(VRML)</a></td>
<td><a href=$SELF/$graph.vtx>application/x-vtx(Visual Thought)</a></td>
</tr></table>
</pre>
<p>
\(There is also a version of this page with the"
		if {$type == "tclhelp"} {
			puts "<a href=$SELF/$graph.help>graph in a GIF</a>.\)"
		} {
			puts "<a href=$SELF/$graph.tclhelp>graph in a Tclet</a>
for the <a href=http://www.sunlabs.com/tcl/plugin/>Tcl Plugin</a>.\)"
		}
		puts "<hr>
<b>WebDot</b> is a server program that converts graphs described in the
<a href=$SELF/dot.txt>DOT abstract graph description language</a>
into GIFS that can be included in HTML pages.
The graphs can contain mouse-sensitive nodes simply by giving the node a URL 
attribute, so there is no need to worry about x-y coordinates.
<p>
<hr>
<font size=+2><a href=$SELF/example1.html>Tutorial examples.</a>
<a href=http://www.research.att.com/~north/webdot/demo/>Demo graphs.</a></font>
<hr>
<p>
<b>Other information:</b>
<a href=$SELF/tcldot.txt>TclDot man page</a>. 
<a href=$SELF/dot.txt>Dot man page</a>.
<p>
You don't need to download WebDot in order to use it, but if you
want to reuse or extend this software here are the sources:
<pre>
<a href=$SELF/source>WebDot cgi program</a>.
<a href=http://www.research.att.com/sw/tools/graphviz/>TclDot sources (part of graphviz)</a>.
<a href=http://www.boutell.com/gd/>GD sources</a>.  <a href=ftp://ftp.smli.com/pub/tcl>Tcl sources</a>.
</pre>
[tail]"
		exit
	}

	if {$fn == "example1.html"} {
		puts "[head {WebDot Example}]
<a href=$SELF/>\[WebDot Home |</a>
<a href=$SELF/example2.html>Next Example\]</a>
<p>
If the URL:
<pre>
<a href=$SELF/example1.dot>$SELF/example1.dot</a>
</pre>
points to the file:
<pre>[include $MYDATA/example1.dot]</pre>
then this (rather long) anchor in a document:
<pre>
&lt;img src=$SELF/<b>$SELF/example1.dot</b>.gif&gt;
</pre>
produces this result:
<p align=center>
<img src=$SELF/$SELF/example1.dot.gif>
<p>
The URL in the anchor has three parts:
<ol>
<li>The URL of the WebDot server: $SELF/
<li>The URL of your .dot file: <b>$SELF/example1.dot</b>
<li>The output format to be provided by the server: .gif
</ol>
[tail]"
		exit
	}
	
	if {$fn == "example2.html"} {
		puts "[head {WebDot Architecture}]
<a href=$SELF/>\[WebDot Home |</a>
<a href=$SELF/example1.html>Previous Example\]</a>
<p>
This file:
<pre>[include $MYDATA/example2.dot]</pre>
with this html:
<pre>
  &lt;a href=$SELF/$SELF/example2.dot.map&gt;
	&lt;img src=$SELF/$SELF/example2.dot.gif ismap&gt;
  &lt;/a&gt;
</pre>
produces this clickable result (note that the \"Graph by WebDot\" 
signature in the graph is also clickable):
<p align=center>
<a href=$SELF/$SELF/example2.dot.map>
<img src=$SELF/$SELF/example2.dot.gif ismap>
</a>
[tail]"
		exit
	}
	
	if {$fn == "source"} {
		puts "Content-Type: text/plain\n\n[include [pwd]/[file tail $argv0]]"
		exit
	}

	if {$ft == ".dot" || $ft == ".txt"} {
		puts "Content-Type: text/plain\n\n[include $MYDATA/$fn]"
		exit
	}
	
	if {$ft == ".gif"} {
		set fn $MYDATA/$fn
		if {[catch {open $fn r} f]} {
			error "Unable to open $fn"
		}
		puts "Content-Type: image/gif\n"
		flush stdout
		fconfigure $f -translation binary
		fconfigure stdout -translation binary
		fcopy $f stdout
		flush stdout
		close $f
		exit
	}
	
	if {$ft == ".html"} {
		set fn $MYDATA/$fn
		if {[catch {open $fn r} f]} {
			error "Unable to open $fn"
		}
		puts "Content-Type: text/html\n\n[read $f]"
		close $f
		exit
	}
	
	error "Unknown file type: $ft"
}

#--------------------------------------
# OK so maybe we have real work to do!

# get source file into cache (may already be there)
set Expires {}
set LastModified {}
set t_url $url
if {[scan $t_url "$SELF%s" p] == 1} {
	#only support files in webdot directory for security reasons
	set t_url file://localhost$MYDATA/[file tail $p]
}
foreach {cache_dir LastModified Expires} [get $t_url $CACHE $no_cache] {break}

if {$type == "pdf"} {
	# for pdf we first need the ps 
	set secondstep pdf
	set type ps
} elseif {$type == "epsi"} {
	# for epsi we first need the ps 
	set secondstep epsi
	set type ps
}

# now see if we can use product from cache
if {![file exists $cache_dir/.$type] \
  || [file mtime $cache_dir/.$type] < [file mtime $cache_dir/.src]
  || [file size $cache_dir/.$type] == 0} {

	# no - so now we need to build it and save it in cache

	# we're going to need the tcldot extension to process the graph
	package require Tcldot

	if {[catch {open $cache_dir/.$type w} f_out]} {
		error "Unable to open cache file for write: $cache_dir/.$type"
	}
	
	# read in source file from cache
	if {[catch {open $cache_dir/.src r} f]} {
		error "Unable to open cache file for read: $cache_dir/.src"
	}
	if {[catch {dotread $f} g]} {
		error "Invalid dot file at: $url\nerror: $g\nfile: $cache_dir/.src"
	}
	close $f
	
	if {$type == "dot" || $type == "map" || $type == "tclmap"} {
		# expand relative URLs if we need them in the output format
		set name [$g showname]
		if {! [catch {$g queryattr BGURL} bg_url]} {
			set bg_url [lindex $bg_url 0]
			if {$bg_url != {}} {
				$g setattr BGURL [make_absolute_url $protocol $serverport $dirname $bg_url $name]
			}
		}
		if {! [catch {$g queryattr URL} g_url]} {
			set g_url [lindex $g_url 0]
			if {$g_url != {}} {
				$g setattr URL [make_absolute_url $protocol $serverport $dirname $g_url $name]
			}
		}
		foreach n [$g listnodes] {
			set name [$n showname]
			if {! [catch {$n queryattr URL} n_url]} {
				set n_url [lindex $n_url 0]
				if {$n_url != {}} {
				   $n setattr URL [make_absolute_url $protocol $serverport $dirname $n_url $name]
				}
			}
			foreach e [$n listout] {
				 set name [$e showname]
				 if {! [catch {$e queryattr URL} e_url]} {
					 set e_url [lindex $e_url 0]
					 if {$e_url != {}} {
						 $e setattr URL [make_absolute_url $protocol $serverport $dirname $e_url $name]
					 }
				 }
			}
		}
	}
	
	# if we're going to do client-side layout then use the
	# canonical dot format and don't bother with server side layout.
	if {$type != "dot"} {$g layout}

	if {$type == "gif"} {
		scan [$g queryattr bb] "{%dp %dp %dp %dp}" ulx uly lrx lry
		set sizex [expr (($lrx - $ulx) * 96/72) + 2] 
		set sizey [expr (($lry - $uly) * 96/72) + 14]
		if {$sizex < 94} {set sizex 94}
		set gd [gd create $sizex $sizey]
		set transparent [gd color new $gd 254 254 254]
		gd color transparent $gd $transparent
		set hyperlink_blue [gd color new $gd 0 0 238]
		if {! [catch {$g queryattr BGURL} bgurl]} {
			set bgurl [lindex $bgurl 0]
			if {$bgurl != {}} {
				set bgurl [make_absolute_url $protocol $serverport $dirname $bgurl [$g showname]]
				if {[scan $bgurl "$SELF%s" p] == 1} {
					#only support files in webdot directory for security reasons
					set bgurl file://localhost$MYDATA/[file tail $p]
				} {
					if {[scan $bgurl {http://%[^/]/%s} serverport path] != 2} {
						error "Unable to find http URL in: $bgurl"
					}
					scan $serverport {%[^:]:%s} server port
					if {$server == "localhost"} {
						error "Nice try, but you can't see our files that way!"
					}
				}
				foreach {bg_cache_dir . .} [get $bgurl $CACHE $no_cache] {break}
				if {[catch {open $bg_cache_dir/.src r} bgf]} {
					error "Unable to open background image file: $bg_cache_dir/.src"
				}
				gd tile $gd [gd createFromGIF $bgf]
				close $bgf
				gd fill $gd tiled 0 0
			}
		}
		set urlsfound 0
		if {! [catch {$g queryattr URL} g_url]} {set urlsfound 1}
		foreach n [$g listnodes] {
			if {! [catch {$n queryattr URL} n_url]} {
				set urlsfound 1
				break
			}
			foreach e [$n listout] {
				if {! [catch {$e queryattr URL} e_url]} {
					set urlsfound 1
					break
				}
			}
		}
#		if {$urlsfound} {
#			gd text $gd $hyperlink_blue \
#				$TTFDIR/times.ttf 11.0 0.0 \
#				[expr $sizex - 85] [expr $sizey - 4] \
#				"Graph by WebDot"
#		}
		$g rendergd $gd
		gd writeGIF $gd $f_out
	
	} elseif {$type == "dot"} {
		$g write $f_out canon
	} elseif {$type == "map"} {
		$g write $f_out ismap
	} elseif {$type == "tcl"} {
		if {[catch {open $MYDATA/tclet.tcl} f_in]} {
			error "Unable to open tclet file for read: $MYDATA/tclet.tcl"
		}
		# output the base tclet code
		fcopy $f_in $f_out
		close $f_in

		# suppress warning about Tkspline
		puts $f_out "set __tkgen_smooth_type true"

		# output commands that render the graph on the canvas
		puts $f_out [$g render]
	} elseif {$type == "tclmap"} {
		if {! [catch {$g queryattr URL} url]} {
			set urls($g) $url
		}
		foreach n [$g listnodes] {
			if {! [catch {$n queryattr URL} url]} {
				set urls($n) $url
			}
			foreach e [$n listout] {
				if {! [catch {$e queryattr URL} url]} {
					set urls($e) $url
				}
			}
		}
		if {[array exists urls]} {
			puts $f_out [array get urls]
		}
	} {
		# vrml produces gifs for each node, so cd to private dir
		set oldwd [pwd]
		cd $cache_dir
		$g write $f_out $type
		cd $oldwd
	}
	
	if {$type == "map"} {
		scan [$g queryattr bb] "{%dp %dp %dp %dp}" ulx uly lrx lry
                set sizex [expr (($lrx - $ulx) * 96/72) + 2 -1]
                set sizey [expr (($lry - $uly) * 96/72) + 14 -1]
                if {$sizex < 94} {set sizex 94}
		puts $f_out "rectangle ([expr $sizex - 86],$sizey) ($sizex,[expr $sizey - 11]) $SELF/$url.help"
	}
	close $f_out
}
if {[info exists secondstep]} {
	set type $secondstep
	if {![file exists $cache_dir/.$type] \
	  || [file mtime $cache_dir/.$type] < [file mtime $cache_dir/.src]
	  || [file size $cache_dir/.$type] == 0} {
		
		set curdir [pwd]
		cd $cache_dir
		if {$type == "pdf"} {
			exec $GS -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=.pdf .ps
		} elseif {$type == "epsi"} {
			exec $PS2EPSI .ps .epsi
		}
		cd $curdir
	}
}

# now the product is in the cache and we can ship it
if {[catch {open $cache_dir/.$type r} f]} {
   error "Unable to open cache file for read: $cache_dir/.$type"
}
# send output header
switch -- $type {
	dot - gif - mif - ps - epsi - pdf - hpgl - pcl - vrml - vtx - src {
		if {$Expires != {}} {puts "Expires: $Expires"}
		if {$LastModified != {}} {puts "Last-Modified: $LastModified"}
		puts "Content-Type: $mime($type)"
	}
	tcl {
		if {$Expires != {}} {puts "Expires: $Expires"}
		if {$LastModified != {}} {puts "Last-Modified: $LastModified"}
		puts "Pragma: no-cache"
		puts "Content-Type: $mime($type)"
	}
	map {
		if {! [info exists env(QUERY_STRING)] \
		  || $env(QUERY_STRING) == {}} {
			if {$Expires != {}} {puts "Expires: $Expires"}
			if {$LastModified != {}} {puts "Last-Modified: $LastModified"}
			puts "Content-Type: $mime($type)"
			set x {}
			set y {}
		} {
			foreach {x y} [split $env(QUERY_STRING) ,] {break}
		}
	}
	tclmap {
		if {! [info exists env(QUERY_STRING)] \
		  || $env(QUERY_STRING) == {}} {
			if {$Expires != {}} {puts "Expires: $Expires"}
			if {$LastModified != {}} {puts "Last-Modified: $LastModified"}
			puts "Content-Type: $mime($type)"
			set query {}
		} {
			set query $env(QUERY_STRING)
		}
	}
	default {error "I don't know how to make type: $type"}
}
if {($type == "map") && $x != {}} {
	set defaulturl {}
	foreach l [split [read $f] \n] {
		if {[scan $l {rectangle (%d,%d) (%d,%d) %s} x1 y1 x2 y2 xy_url]} {
			if {$x >= $x1 && $x <= $x2 && $y <= $y1 && $y >= $y2} {
					puts "Location: $xy_url\n"
					set defaulturl {}
					break
			}
		} {
			scan $l {default %s} defaulturl
		}
	}
	if {$defaulturl != {}} {
		puts "Location: $defaulturl\n"
	} {
		error "No default URL was specified in the graph."
	}
} elseif {($type == "tclmap") && $query != {}} {
	array set urls [read $f]
	if {[info exists urls($query)]} {
		puts "Location: $urls($query)\n"
	} {
		error "no URL for $query"
	}
} {
	puts "Content-Length: [file size $cache_dir/.$type]\n"
	if {$env(REQUEST_METHOD) != "HEAD"} {
		flush stdout
		fconfigure $f -translation binary
		fconfigure stdout -translation binary
		fcopy $f stdout
		flush stdout
		puts ""
	}
}
close $f


