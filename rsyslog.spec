%global mysql_config_path %{_libdir}/mysql
%global _exec_prefix %{nil}
%global _libdir %{_exec_prefix}/%{_lib}
%define rsyslog_pkidir %{_sysconfdir}/pki/rsyslog
%global rsyslog_statedir /var/lib/rsyslog

Summary: Enhanced system logging and kernel message trapping daemons
Name: rsyslog
Version: 5.8.10
Release: 12%{?dist}
License: (GPLv3+ and ASL 2.0)
Group: System Environment/Daemons
URL: http://www.rsyslog.com/
Source0: http://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
Source1: rsyslog.init
Source2: rsyslog.conf
Source3: rsyslog.sysconfig
Source4: rsyslog.log
Patch0: rsyslog-5.8.7-sysklogd-compat-1-template.patch
Patch1: rsyslog-5.8.7-sysklogd-compat-2-option.patch
Patch2: rsyslog-5.8.10-bz820311.patch
Patch3: rsyslog-5.8.10-bz820996.patch
Patch4: rsyslog-5.8.10-bz822118.patch
Patch6: rsyslog-5.8.10-bz886004.patch
Patch7: rsyslog-5.8.10-bz886004-regression.patch
Patch8: rsyslog-5.8.10-bz924754-large-grps.patch
Patch9: rsyslog-5.8.10-bz951727-pritext.patch
Patch10: rsyslog-5.8.10-bz963942-maxFileSize.patch
Patch11: rsyslog-5.8.10-bz893197-missingHostname.patch
Patch12: rsyslog-5.8.10-bz886117-numerical-uid.patch
Patch13: rsyslog-5.8.10-bz862517.patch
Patch14: rsyslog-5.8.10-rhbz1142373-cve-2014-3634.patch
Patch15: rsyslog-5.8.10-rhbz1109155-regex-segv.patch
Patch16: rsyslog-5.8.10-rhbz1491428-DA-queue-abort.patch
Patch17: rsyslog-5.8.10-bz1392400-man-page.patch

BuildRequires: zlib-devel
Requires: logrotate >= 3.5.2
Requires: bash >= 2.0
Requires(post): /sbin/chkconfig coreutils
Requires(preun): /sbin/chkconfig /sbin/service
Requires(postun): /sbin/service
Provides: syslog
Obsoletes: sysklogd <= 1.4.1-46
# newer version of selinux-policy is needed, reference: #838148
Conflicts: selinux-policy < 3.7.19-128
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%package mysql
Summary: MySQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: mysql-devel >= 4.0

%package pgsql
Summary: PostgresSQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: postgresql-devel

%package gssapi
Summary: GSSAPI authentication and encryption support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: krb5-devel 

%package relp
Summary: RELP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librelp-devel 

%package gnutls
Summary: TLS protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: gnutls-devel

%package snmp
Summary: SNMP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: net-snmp-devel

%description
Rsyslog is an enhanced, multi-threaded syslog daemon. It supports MySQL,
syslog/TCP, RFC 3195, permitted sender lists, filtering on any message part,
and fine grain output format control. It is compatible with stock sysklogd
and can be used as a drop-in replacement. Rsyslog is simple to set up, with
advanced features suitable for enterprise-class, encryption-protected syslog
relay chains.

%description mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

%description pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

%description gssapi
The rsyslog-gssapi package contains the rsyslog plugins which support GSSAPI 
authentication and secure connections. GSSAPI is commonly used for Kerberos 
authentication.

%description relp
The rsyslog-relp package contains the rsyslog plugins that provide
the ability to receive syslog messages via the reliable RELP
protocol. 

%description gnutls
The rsyslog-gnutls package contains the rsyslog plugins that provide the
ability to receive syslog messages via upcoming syslog-transport-tls
IETF standard protocol.

%description snmp
The rsyslog-snmp package contains an rsyslog plugin that provides the
ability to send syslog messages as SNMPv1 and SNMPv2c traps.

%prep
%setup -q
%patch0 -p1 -b .sysklogd-compat-1-template
%patch1 -p1 -b .sysklogd-compat-2-option
%patch2 -p1 -b .bz820311
%patch3 -p1 -b .bz820996
%patch4 -p1 -b .bz822118
%patch6 -p1 -b .bz886004
%patch7 -p1 -b .bz886004-regression
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

%patch16 -p1 -b .DA-queue-abort
%patch17 -p1 -b .man-pages

%build
# workaround for mysql_conf multilib issue, bug #694414
export PATH="%{mysql_config_path}:$PATH"

export CFLAGS="$RPM_OPT_FLAGS -fpie -DSYSLOGD_PIDNAME=\\\"syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%configure	--disable-static \
		--disable-testbench \
		--enable-gnutls \
		--enable-gssapi-krb5 \
		--enable-imfile \
		--enable-impstats \
		--enable-imptcp \
		--enable-mail \
		--enable-mysql \
		--enable-omprog \
		--enable-omuxsock \
		--enable-pgsql \
		--enable-pmlastmsg \
		--enable-relp \
		--enable-snmp \
		--enable-unlimited-select \
		--with-systemdsystemunitdir=no \

make V=1

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/rsyslog.d
install -d -m 700 $RPM_BUILD_ROOT%{rsyslog_statedir}
install -d -m 700 $RPM_BUILD_ROOT%{rsyslog_pkidir}

install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/rsyslog
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rsyslog.conf
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rsyslog
install -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/syslog

#get rid of *.la
rm $RPM_BUILD_ROOT/%{_libdir}/rsyslog/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rsyslog
for n in /var/log/{messages,secure,maillog,spooler}
do
	[ -f $n ] && continue
	umask 066 && touch $n
done

%preun
if [ $1 = 0 ]; then
	service rsyslog stop >/dev/null 2>&1 ||:
	/sbin/chkconfig --del rsyslog
fi

%postun
if [ "$1" -ge "1" ]; then
	service rsyslog condrestart > /dev/null 2>&1 ||:
fi	

%triggerun -- rsyslog < 4.6.2-5
# previous versions used a different lock file, which would break condrestart
[ -f /var/lock/subsys/rsyslogd ] || exit 0
mv /var/lock/subsys/rsyslogd /var/lock/subsys/rsyslog
[ -f /var/run/rklogd.pid ] || exit 0
/bin/kill `cat /var/run/rklogd.pid 2> /dev/null` > /dev/null 2>&1 ||:

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* ChangeLog NEWS README doc/*html
%dir %{_libdir}/rsyslog
%{_libdir}/rsyslog/imklog.so
%{_libdir}/rsyslog/immark.so
%{_libdir}/rsyslog/impstats.so
%{_libdir}/rsyslog/imptcp.so
%{_libdir}/rsyslog/imtcp.so
%{_libdir}/rsyslog/imudp.so
%{_libdir}/rsyslog/imuxsock.so
%{_libdir}/rsyslog/imfile.so
%{_libdir}/rsyslog/lmnet.so
%{_libdir}/rsyslog/lmregexp.so
%{_libdir}/rsyslog/lmtcpclt.so
%{_libdir}/rsyslog/lmtcpsrv.so
%{_libdir}/rsyslog/lmnetstrms.so
%{_libdir}/rsyslog/lmnsd_ptcp.so
%{_libdir}/rsyslog/lmstrmsrv.so
%{_libdir}/rsyslog/lmzlibw.so
%{_libdir}/rsyslog/ommail.so
%{_libdir}/rsyslog/omprog.so
%{_libdir}/rsyslog/omruleset.so
%{_libdir}/rsyslog/omtesting.so
%{_libdir}/rsyslog/omuxsock.so
%{_libdir}/rsyslog/pmlastmsg.so
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/syslog
%dir %{_sysconfdir}/rsyslog.d
%dir %{rsyslog_statedir}
%dir %{rsyslog_pkidir}
%{_initrddir}/rsyslog
%{_sbindir}/rsyslogd
%{_mandir}/*/*

%files mysql
%defattr(-,root,root)
%doc plugins/ommysql/createDB.sql
%{_libdir}/rsyslog/ommysql.so

%files pgsql
%defattr(-,root,root)
%doc plugins/ompgsql/createDB.sql
%{_libdir}/rsyslog/ompgsql.so

%files gssapi
%defattr(-,root,root)
%{_libdir}/rsyslog/lmgssutil.so
%{_libdir}/rsyslog/imgssapi.so
%{_libdir}/rsyslog/omgssapi.so

%files relp
%defattr(-,root,root)
%{_libdir}/rsyslog/imrelp.so
%{_libdir}/rsyslog/omrelp.so

%files gnutls
%defattr(-,root,root)
%{_libdir}/rsyslog/lmnsd_gtls.so

%files snmp
%defattr(-,root,root)
%{_libdir}/rsyslog/omsnmp.so

%changelog
* Fri Dec 01 2017 Jiri Vymazal <jvymazal@redhat.com> 5.8.10-12
RHEL-6.10 ERRATUM

- added a patch fixing manpages
  resolves: rhbz#1392400

* Mon Nov 06 2017 Jiri Vymazal <jvymazal@redhat.com> 5.8.10-11
RHEL-6.10 ERRATUM

- add a patch fixing possible ABRT in DA queues
  resolves: rhbz#1491428

* Tue Dec 09 2014 Tomas Heinrich <theinric@redhat.com> 5.8.10-10
- add a patch to fix a segfault in the regex module
  resolves: #1109155
- explicitly disable systemd service file generation
- turn on verbose make output

* Fri Oct 10 2014 Tomas Heinrich <theinric@redhat.com> 5.8.10-9
- fix CVE-2014-3634
  resolves: #1149149

* Wed Aug 14 2013 Tomas Heinrich <theinric@redhat.com> 5.8.10-8
- drop patch 5 which introduced a regression
  resolves: #927405
  reverts: #847568
- add a patch to prevent 'RepeatedMsgReduction' causing missing hostnames
  resolves: #893197
- add a patch to enable specifying UID/GID as a number
  resolves: #886117
- add a patch to prevent a segfault in gssapi
  resolves: #862517

* Tue Jul 16 2013 Tomas Heinrich <theinric@redhat.com> 5.8.10-7
- add a patch to support large groups in the $FileGroup directive
  resolves: #924754
- add a patch to fix 'pri-text' property format
  resolves: #951727
- add a patch to fix the behavior of the *QueueMaxFileSize directives
  resolves: #963942

* Wed Jan 09 2013 Tomas Heinrich <theinric@redhat.com> 5.8.10-6
- the previous patch to enable RFC3339 timestamps revealed a bug
  in the upstream code - adding another patch
  Resolves: #886004

* Tue Jan 08 2013 Tomas Heinrich <theinric@redhat.com> 5.8.10-5
- add a patch to permit RFC3339 timestamps in messages comming from
  the local log socket, patch taken from upstream - commit:
  bfae69d68b0032a383821a54bc52aeff36a90e52
  Resolves: #886004

* Sun Oct 14 2012 Tomas Heinrich <theinric@redhat.com> 5.8.10-4
- add patch to correct the order in which selector filters are added
  Resolves: #847568

* Fri Oct 12 2012 Tomas Heinrich <theinric@redhat.com> 5.8.10-3
- add 'conflicts' on incompatible version of selinux-policy
  Resolves: #838148

* Thu May 17 2012 Tomas Heinrich <theinric@redhat.com> 5.8.10-2
- add patch to update information on debugging in the man page
  Resolves: #820311
- add patch to prevent debug output to stdout after forking
  Resolves: #820996
- add patch to support ssl certificates with domain names longer than 128 chars
  Resolves: #822118

* Wed Apr 25 2012 Tomas Heinrich <theinric@redhat.com> 5.8.10-1
- rebase to rsyslog 5.8.10
  Resolves: #803550
  Resolves: #805424
  Resolves: #813079
  Resolves: #813084
- consider lock file in 'status' action
  Resolves: #807608
- add impstats and imptcp modules
- include new license text files
- specify which versions of sysklogd are obsoleted

* Tue Feb 07 2012 Tomas Heinrich <theinric@redhat.com> 5.8.7-1
- rebase to rsyslog-5.8.7
  - change license from 'GPLv3+' to '(GPLv3+ and ASL 2.0)'
    http://blog.gerhards.net/2012/01/rsyslog-licensing-update.html
  - remove patches obsoleted by rebase
  - add patches for better sysklogd compatibility (taken from upstream)
  - update included files for the new major version
  Resolves: #672182
  Resolves: #727380
  Resolves: #756664
  Resolves: #767527
  Resolves: #769025
- add several directories for storing auxiliary data
  Resolves: #740420
- fix source package URL

* Wed Oct 05 2011 Tomas Heinrich <theinric@redhat.com> 4.6.2-12
- fix typo in RSYSLOG_SysklogdFileFormat documentation
  Resolves: #737096

* Thu Sep 29 2011 Tomas Heinrich <theinric@redhat.com> 4.6.2-11
- provide configuration directive for sysklogd message format compatibility
- provide log format template for sysklogd message format compatibility
  Resolves: #737096 

* Wed Aug 31 2011 Tomas Heinrich <theinric@redhat.com> 4.6.2-10
- add patch to resolve buffer overflow (CVE-2011-3200)
  Resolves: #733648

* Mon Aug 22 2011 Tomas Heinrich <theinric@redhat.com> 4.6.2-9
- use proper lock file in 'status' action
  Resolves: #698705

* Mon Aug 08 2011 Tomas Heinrich <theinric@redhat.com> 4.6.2-8
- workaround the mysql_conf multilib issue by directly using
  the arch-specific script
  Resolves: #694414

* Mon Aug 08 2011 Tomas Heinrich <theinric@redhat.com> 4.6.2-7
- add patch to correct the behavior of the ActionExecOnlyOnceEveryInterval
  configuration directive
  Resolves: #727208

* Wed Aug 03 2011 Tomas Heinrich <theinric@redhat.com> 4.6.2-6
- add patch to prevent tight loop when using TLS
  Resolves: #661858

* Tue Aug 02 2011 Tomas Heinrich <theinric@redhat.com> 4.6.2-5
- provide omsnmp module in rsyslog-snmp subpackage
  Resolves: #618488
- modify logrotate configuration to omit boot.log
  Resolves: #683537
- use correct lock file name
  Resolves: #698705
- provide ommail module
  Resolves: #702314

* Wed Jun 08 2011 Tomas Heinrich <theinric@redhat.com> 4.6.2-4
- add patch to resolve short int overflow
  Resolves: #701782

* Wed Feb 16 2011 Tomas Heinrich <theinric@redhat.com> 4.6.2-3
- build rsyslog with PIE and RELRO
  Resolves: #642994
- add ChangeLog file to documentation
- add /etc/pki/rsyslog directory

* Tue Jun 08 2010 Tomas Heinrich <theinric@redhat.com> 4.6.2-2
- Fix a potential segfault upon SIGHUP induced restart
  Resolves: #598421
- Add Obsoletes: sysklogd
  Resolves: #513277

* Wed May 19 2010 Tomas Heinrich <theinric@redhat.com> 4.6.2-1
- upgrade to new upstream stable version 4.6.2
  Resolves: #554998
- correct the default value of the OMFileFlushOnTXEnd directive
- add upstream fix for message-induced off-by-one error
- change the default value of the HUPisRestart directive to enabled
- remove autoconf, automake, libtool from BuildRequires
- change exec-prefix to nil
- redefine _libdir as it doesn't use _exec_prefix
  Resolves: #591860

* Wed Mar 31 2010 Tomas Heinrich <theinric@redhat.com> - 4.4.2-4
- change init script error code
  Resolves: #539065

* Wed Feb 03 2010 Tomas Heinrich <theinric@redhat.com> - 4.4.2-3
- remove '_smp_mflags' make argument as it seems to be
  producing corrupted builds
  Resolves: #556522

* Wed Jan 27 2010 Tomas Heinrich <theinric@redhat.com> - 4.4.2-2
- rebuild for #556522

* Thu Jan 14 2010 Tomas Heinrich <theinric@redhat.com> - 4.4.2-1
- upgrade to new upstream stable version 4.4.2
  Resolves: #554998
- add support for arbitrary number of open file descriptors
- run libtoolize to avoid errors due mismatching libtool version
- change exec-prefix to /

* Mon Nov 23 2009 Dennis Gregorovic <dgregor@redhat.com> - 4.4.1-2.1
- Rebuilt for RHEL 6

* Mon Sep 14 2009 Tomas Heinrich <theinric@redhat.com> 4.4.1-2
- adjust init script according to guidelines (#522071)

* Thu Sep 03 2009 Tomas Heinrich <theinric@redhat.com> 4.4.1-1
- upgrade to new upstream stable version

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 4.2.0-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Tomas Heinrich <theinric@redhat.com> 4.2.0-1
- upgrade

* Mon Apr 13 2009 Tomas Heinrich <theinric@redhat.com> 3.21.11-1
- upgrade

* Tue Mar 31 2009 Lubomir Rintel <lkundrak@v3.sk> 3.21.10-4
- Backport HUPisRestart option

* Wed Mar 18 2009 Tomas Heinrich <theinric@redhat.com> 3.21.10-3
- fix variables' type conversion in expression-based filters (#485937)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.21.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Tomas Heinrich <theinric@redhat.com> 3.21.10-1
- upgrade

* Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> 3.21.9-3
- rebuild for dependencies

* Wed Jan 07 2009 Tomas Heinrich <theinric@redhat.com> 3.21.9-2
- fix several legacy options handling
- fix internal message output (#478612)

* Mon Dec 15 2008 Peter Vrabec <pvrabec@redhat.com> 3.21.9-1
- update is fixing $AllowedSender security issue

* Mon Sep 15 2008 Peter Vrabec <pvrabec@redhat.com> 3.21.3-4
- use RPM_OPT_FLAGS
- use same pid file and logrotate file as syslog-ng (#441664)
- mark config files as noreplace (#428155)

* Mon Sep 01 2008 Tomas Heinrich <theinric@redhat.com> 3.21.3-3
- fix a wrong module name in the rsyslog.conf manual page (#455086)
- expand the rsyslog.conf manual page (#456030)

* Thu Aug 28 2008 Tomas Heinrich <theinric@redhat.com> 3.21.3-2
- fix clock rollback issue (#460230)

* Wed Aug 20 2008 Peter Vrabec <pvrabec@redhat.com> 3.21.3-1
- upgrade to bugfix release

* Wed Jul 23 2008 Peter Vrabec <pvrabec@redhat.com> 3.21.0-1
- upgrade

* Mon Jul 14 2008 Peter Vrabec <pvrabec@redhat.com> 3.19.9-2
- adjust default config file

* Fri Jul 11 2008 Lubomir Rintel <lkundrak@v3.sk> 3.19.9-1
- upgrade

* Wed Jun 25 2008 Peter Vrabec <pvrabec@redhat.com> 3.19.7-3
- rebuild because of new gnutls

* Fri Jun 13 2008 Peter Vrabec <pvrabec@redhat.com> 3.19.7-2
- do not translate Oopses (#450329)

* Fri Jun 13 2008 Peter Vrabec <pvrabec@redhat.com> 3.19.7-1
- upgrade

* Wed May 28 2008 Peter Vrabec <pvrabec@redhat.com> 3.19.4-1
- upgrade

* Mon May 26 2008 Peter Vrabec <pvrabec@redhat.com> 3.19.3-1
- upgrade to new upstream release

* Wed May 14 2008 Tomas Heinrich <theinric@redhat.com> 3.16.1-1
- upgrade

* Tue Apr 08 2008 Peter Vrabec <pvrabec@redhat.com> 3.14.1-5
- prevent undesired error description in legacy 
  warning messages

* Tue Apr 08 2008 Peter Vrabec <pvrabec@redhat.com> 3.14.1-4
- adjust symbol lookup method to 2.6 kernel 

* Tue Apr 08 2008 Peter Vrabec <pvrabec@redhat.com> 3.14.1-3
- fix segfault of expression based filters

* Mon Apr 07 2008 Peter Vrabec <pvrabec@redhat.com> 3.14.1-2
- init script fixes (#441170,#440968)

* Fri Apr 04 2008 Peter Vrabec <pvrabec@redhat.com> 3.14.1-1
- upgrade

* Tue Mar 25 2008 Peter Vrabec <pvrabec@redhat.com> 3.12.4-1
- upgrade

* Wed Mar 19 2008 Peter Vrabec <pvrabec@redhat.com> 3.12.3-1
- upgrade 
- fix some significant memory leaks

* Tue Mar 11 2008 Peter Vrabec <pvrabec@redhat.com> 3.12.1-2
- init script fixes (#436854)
- fix config file parsing (#436722)

* Thu Mar 06 2008 Peter Vrabec <pvrabec@redhat.com> 3.12.1-1
- upgrade

* Wed Mar 05 2008 Peter Vrabec <pvrabec@redhat.com> 3.12.0-1
- upgrade

* Mon Feb 25 2008 Peter Vrabec <pvrabec@redhat.com> 3.11.5-1
- upgrade

* Fri Feb 01 2008 Peter Vrabec <pvrabec@redhat.com> 3.11.0-1
- upgrade to the latests development release
- provide PostgresSQL support
- provide GSSAPI support

* Mon Jan 21 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-7
- change from requires sysklogd to conflicts sysklogd

* Fri Jan 18 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-6
- change logrotate file
- use rsyslog own pid file

* Thu Jan 17 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-5
- fixing bad descriptor (#428775)

* Wed Jan 16 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-4
- rename logrotate file

* Wed Jan 16 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-3
- fix post script and init file

* Wed Jan 16 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-2
- change pid filename and use logrotata script from sysklogd

* Tue Jan 15 2008 Peter Vrabec <pvrabec@redhat.com> 2.0.0-1
- upgrade to stable release
- spec file clean up

* Wed Jan 02 2008 Peter Vrabec <pvrabec@redhat.com> 1.21.2-1
- new upstream release

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.19.11-2
- Rebuild for deps

* Thu Nov 29 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.11-1
- new upstream release
- add conflicts (#400671)

* Mon Nov 19 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.10-1
- new upstream release

* Wed Oct 03 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.6-3
- remove NUL character from recieved messages

* Tue Sep 25 2007 Tomas Heinrich <theinric@redhat.com> 1.19.6-2
- fix message suppression (303341)

* Tue Sep 25 2007 Tomas Heinrich <theinric@redhat.com> 1.19.6-1
- upstream bugfix release

* Tue Aug 28 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.2-1
- upstream bugfix release
- support for negative app selector, patch from 
  theinric@redhat.com

* Fri Aug 17 2007 Peter Vrabec <pvrabec@redhat.com> 1.19.0-1
- new upstream release with MySQL support(as plugin)

* Wed Aug 08 2007 Peter Vrabec <pvrabec@redhat.com> 1.18.1-1
- upstream bugfix release

* Mon Aug 06 2007 Peter Vrabec <pvrabec@redhat.com> 1.18.0-1
- new upstream release

* Thu Aug 02 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.6-1
- upstream bugfix release

* Mon Jul 30 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.5-1
- upstream bugfix release
- fix typo in provides 

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 1.17.2-4
- rebuild for toolchain bug

* Tue Jul 24 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.2-3
- take care of sysklogd configuration files in %%post

* Tue Jul 24 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.2-2
- use EVR in provides/obsoletes sysklogd

* Mon Jul 23 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.2-1
- upstream bug fix release

* Fri Jul 20 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.1-1
- upstream bug fix release
- include html docs (#248712)
- make "-r" option compatible with sysklogd config (248982)

* Tue Jul 17 2007 Peter Vrabec <pvrabec@redhat.com> 1.17.0-1
- feature rich upstream release

* Thu Jul 12 2007 Peter Vrabec <pvrabec@redhat.com> 1.15.1-2
- use obsoletes and hadle old config files

* Wed Jul 11 2007 Peter Vrabec <pvrabec@redhat.com> 1.15.1-1
- new upstream bugfix release

* Tue Jul 10 2007 Peter Vrabec <pvrabec@redhat.com> 1.15.0-1
- new upstream release introduce capability to generate output 
  file names based on templates

* Tue Jul 03 2007 Peter Vrabec <pvrabec@redhat.com> 1.14.2-1
- new upstream bugfix release

* Mon Jul 02 2007 Peter Vrabec <pvrabec@redhat.com> 1.14.1-1
- new upstream release with IPv6 support

* Tue Jun 26 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.5-3
- add BuildRequires for  zlib compression feature

* Mon Jun 25 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.5-2
- some spec file adjustments.
- fix syslog init script error codes (#245330)

* Fri Jun 22 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.5-1
- new upstream release

* Fri Jun 22 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.4-2
- some spec file adjustments.

* Mon Jun 18 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.4-1
- upgrade to new upstream release

* Wed Jun 13 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.2-2
- DB support off

* Tue Jun 12 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.2-1
- new upstream release based on redhat patch

* Fri Jun 08 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.1-2
- rsyslog package provides its own kernel log. daemon (rklogd)

* Mon Jun 04 2007 Peter Vrabec <pvrabec@redhat.com> 1.13.1-1
- Initial rpm build
