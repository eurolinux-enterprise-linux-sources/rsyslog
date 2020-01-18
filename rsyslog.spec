%define rsyslog_statedir %{_sharedstatedir}/rsyslog
%define rsyslog_pkidir %{_sysconfdir}/pki/rsyslog
%define rsyslog_docdir %{_docdir}/%{name}-%{version}
%if 0%{?rhel} >= 7
%global want_hiredis 0
%global want_mongodb 0
%global want_rabbitmq 0
%else
%global want_hiredis 1
%global want_mongodb 1
%global want_rabbitmq 1
%endif

Summary: Enhanced system logging and kernel message trapping daemon
Name: rsyslog
Version: 8.24.0
Release: 41%{?dist}
License: (GPLv3+ and ASL 2.0)
Group: System Environment/Daemons
URL: http://www.rsyslog.com/
Source0: http://www.rsyslog.com/files/download/rsyslog/%{name}-%{version}.tar.gz
Source1: http://www.rsyslog.com/files/download/rsyslog/%{name}-doc-%{version}.tar.gz
Source2: rsyslog.conf
Source3: rsyslog.sysconfig
Source4: rsyslog.log

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: bison
BuildRequires: flex
BuildRequires: libfastjson-devel
BuildRequires: libestr-devel >= 0.1.9
BuildRequires: libuuid-devel
BuildRequires: pkgconfig
BuildRequires: python-docutils
BuildRequires: python-sphinx
# it depens on rhbz#1419228
BuildRequires: systemd-devel >= 219-39
BuildRequires: zlib-devel

Requires: logrotate >= 3.5.2
Requires: bash >= 2.0
Requires: libestr >= 0.1.9
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Provides: syslog
Obsoletes: sysklogd < 1.5-11

# tweak the upstream service file to honour configuration from /etc/sysconfig/rsyslog
Patch0: rsyslog-8.24.0-sd-service.patch
Patch1: rsyslog-8.24.0-msg_c_nonoverwrite_merge.patch
#Patch2: rsyslog-8.24.0-rhbz1188503-imjournal-default-tag.patch

Patch3: rsyslog-8.24.0-rhbz1303617-imfile-wildcards.patch
Patch4: rsyslog-8.24.0-doc-polling-by-default.patch
Patch5: rsyslog-8.24.0-rhbz1399569-flushontxend.patch
Patch6: rsyslog-8.24.0-rhbz1400594-tls-config.patch
Patch7: rsyslog-8.24.0-rhbz1401870-watermark.patch

Patch8: rsyslog-8.24.0-rhbz1403831-missing-cmd-line-switches.patch
Patch9: rsyslog-8.24.0-rhbz1245194-imjournal-ste-file.patch
Patch10: rsyslog-8.24.0-doc-rhbz1507028-recover_qi.patch
Patch11: rsyslog-8.24.0-rhbz1088021-systemd-time-backwards.patch
Patch12: rsyslog-8.24.0-rhbz1403907-imudp-deprecated-parameter.patch
Patch13: rsyslog-8.24.0-rhbz1196230-ratelimit-add-source.patch
Patch14: rsyslog-8.24.0-rhbz1422789-missing-chdir-w-chroot.patch
Patch15: rsyslog-8.24.0-rhbz1422414-glbDoneLoadCnf-segfault.patch
Patch16: rsyslog-8.24.0-rhbz1427828-set-unset-not-checking-varName.patch

Patch17: rsyslog-8.24.0-rhbz1427821-backport-num2ipv4.patch
Patch18: rsyslog-8.24.0-rhbz1427821-str2num-emty-string-handle.patch

Patch19: rsyslog-8.24.0-rhbz1165236-snmp-mib.patch
Patch20: rsyslog-8.24.0-rhbz1419228-journal-switch-persistent.patch
Patch21: rsyslog-8.24.0-rhbz1431616-pmrfc3164sd-backport.patch

Patch22: rsyslog-8.24.0-rhbz1056548-getaddrinfo.patch

Patch23: rsyslog-8.24.0-rhbz1401456-sd-service-network.patch
Patch24: rsyslog-8.24.0-doc-rhbz1459896-queues-defaults.patch
Patch25: rsyslog-8.24.0-rhbz1497985-journal-reloaded-message.patch
Patch26: rsyslog-8.24.0-rhbz1462160-set.statement-crash.patch
Patch27: rsyslog-8.24.0-rhbz1488186-fixed-nullptr-check.patch
Patch28: rsyslog-8.24.0-rhbz1505103-omrelp-rebindinterval.patch

Patch29: rsyslog-8.24.0-rhbz1538372-imjournal-duplicates.patch
Patch30: rsyslog-8.24.0-rhbz1511485-deserialize-property-name.patch

Patch31: rsyslog-8.24.0-rhbz1512551-caching-sockaddr.patch
Patch32: rsyslog-8.24.0-rhbz1531295-imfile-rewrite-with-symlink.patch
Patch33: rsyslog-8.24.0-rhbz1582517-buffer-overflow-memcpy-in-parser.patch
Patch34: rsyslog-8.24.0-rhbz1591819-msg-loss-shutdown.patch
Patch35: rsyslog-8.24.0-rhbz1539193-mmkubernetes-new-plugin.patch
Patch36: rsyslog-8.24.0-rhbz1507145-omelastic-client-cert.patch
Patch37: rsyslog-8.24.0-doc-rhbz1507145-omelastic-client-cert-and-config.patch
Patch38: rsyslog-8.24.0-rhbz1565214-omelasticsearch-replace-cJSON-with-libfastjson.patch
Patch39: rsyslog-8.24.0-rhbz1565214-omelasticsearch-write-op-types-bulk-rejection-retries.patch
Patch40: rsyslog-8.24.0-doc-rhbz1539193-mmkubernetes-new-plugin.patch
Patch41: rsyslog-8.24.0-doc-rhbz1538372-imjournal-duplicates.patch
Patch42: rsyslog-8.24.0-rhbz1597264-man-page-fix.patch
Patch43: rsyslog-8.24.0-rhbz1559408-async-writer.patch
Patch44: rsyslog-8.24.0-rhbz1600462-wrktable-realloc-null.patch

Patch45: rsyslog-8.24.0-rhbz1632659-omfwd-mem-corruption.patch
Patch46: rsyslog-8.24.0-rhbz1649250-imfile-rotation.patch
Patch47: rsyslog-8.24.0-rhbz1658288-imptcp-octet-segfault.patch
Patch48: rsyslog-8.24.0-rhbz1622767-mmkubernetes-stop-on-pod-delete.patch
Patch49: rsyslog-8.24.0-rhbz1685901-symlink-error-flood.patch
Patch50: rsyslog-8.24.0-rhbz1632211-journal-cursor-fix.patch
Patch51: rsyslog-8.24.0-rhbz1666365-internal-messages-memory-leak.patch
Patch52: rsyslog-8.24.0-doc-rhbz1625935-mmkubernetes-CRI-O.patch
Patch53: rsyslog-8.24.0-rhbz1656860-imfile-buffer-overflow.patch
Patch54: rsyslog-8.24.0-rhbz1725067-imjournal-memleak.patch

%package crypto
Summary: Encryption support
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libgcrypt-devel

%package doc
Summary: HTML Documentation for rsyslog
Group: Documentation
#no reason to have arched documentation
BuildArch: noarch

%package elasticsearch
Summary: ElasticSearch output module for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libcurl-devel

%if %{want_hiredis}
%package hiredis
Summary: Redis support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: hiredis-devel
%endif

%package mmjsonparse
Summary: JSON enhanced logging support
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmnormalize
Summary: Log normalization support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libee-devel
BuildRequires: liblognorm-devel

%package mmaudit
Summary: Message modification module supporting Linux audit format
Group: System Environment/Daemons
Requires: %name = %version-%release

%package mmsnmptrapd
Summary: Message modification module for snmptrapd generated messages
Group: System Environment/Daemons
Requires: %name = %version-%release

%package libdbi
Summary: Libdbi database support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libdbi-devel

%package mysql
Summary: MySQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: mysql >= 4.0
BuildRequires: mysql-devel >= 4.0

%if %{want_mongodb}
%package mongodb
Summary: MongoDB support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libmongo-client-devel
%endif

%package pgsql
Summary: PostgresSQL support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: postgresql-devel

%if %{want_rabbitmq}
%package rabbitmq
Summary: RabbitMQ support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librabbitmq-devel >= 0.2
%endif

%package gssapi
Summary: GSSAPI authentication and encryption support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: krb5-devel

%package relp
Summary: RELP protocol support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
Requires: librelp >= 1.0.3
BuildRequires: librelp-devel >= 1.0.3

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

%package udpspoof
Summary: Provides the omudpspoof module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libnet-devel

%package kafka
Summary: Provides kafka support for rsyslog
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: librdkafka-devel

%package mmkubernetes
Summary: Provides the mmkubernetes module
Group: System Environment/Daemons
Requires: %name = %version-%release
BuildRequires: libcurl-devel

%description
Rsyslog is an enhanced, multi-threaded syslog daemon. It supports MySQL,
syslog/TCP, RFC 3195, permitted sender lists, filtering on any message part,
and fine grain output format control. It is compatible with stock sysklogd
and can be used as a drop-in replacement. Rsyslog is simple to set up, with
advanced features suitable for enterprise-class, encryption-protected syslog
relay chains.

%description crypto
This package contains a module providing log file encryption and a
command line tool to process encrypted logs.

%description doc
This subpackage contains documentation for rsyslog.

%description elasticsearch
This module provides the capability for rsyslog to feed logs directly into
Elasticsearch.

%if %{want_hiredis}
%description hiredis
This module provides output to Redis.
%endif

%description mmjsonparse
This module provides the capability to recognize and parse JSON enhanced
syslog messages.

%description mmnormalize
This module provides the capability to normalize log messages via liblognorm.

%description mmaudit
This module provides message modification supporting Linux audit format
in various settings.

%description mmsnmptrapd
This message modification module takes messages generated from snmptrapd and
modifies them so that they look like they originated from the read originator.

%description libdbi
This module supports a large number of database systems via
libdbi. Libdbi abstracts the database layer and provides drivers for
many systems. Drivers are available via the libdbi-drivers project.

%description mysql
The rsyslog-mysql package contains a dynamic shared object that will add
MySQL database support to rsyslog.

%if %{want_mongodb}
%description mongodb
The rsyslog-mongodb package contains a dynamic shared object that will add
MongoDB database support to rsyslog.
%endif

%description pgsql
The rsyslog-pgsql package contains a dynamic shared object that will add
PostgreSQL database support to rsyslog.

%if %{want_rabbitmq}
%description rabbitmq
This module allows rsyslog to send messages to a RabbitMQ server.
%endif

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
The rsyslog-snmp package contains the rsyslog plugin that provides the
ability to send syslog messages as SNMPv1 and SNMPv2c traps.

%description udpspoof
This module is similar to the regular UDP forwarder, but permits to
spoof the sender address. Also, it enables to circle through a number
of source ports.

%description kafka
The rsyslog-kafka package provides module for Apache Kafka output.

%description mmkubernetes
The rsyslog-mmkubernetes package provides module for adding kubernetes 
container metadata. 

%prep
# set up rsyslog-doc sources
%setup -q -a 1 -T -c
%patch4 -p1 
%patch10 -p1
%patch24 -p1
%patch37 -p1
%patch40 -p1
%patch41 -p1
%patch52 -p1
#regenerate the docs
mv build/searchindex.js searchindex_backup.js
sphinx-build -b html source build
#clean up
mv searchindex_backup.js build/searchindex.js
rm -r LICENSE README.md build.sh source build/objects.inv
mv build doc

# set up rsyslog sources
%setup -q -D

%patch0 -p1 -b .service
%patch1 -p1 -b .msg_merge
#%patch2 is obsoleted by patch25
%patch3 -p1 -b .wildcards
#%patch4 is applied right after doc setup 

%patch5 -p1 -b .flushontxend
%patch6 -p1 -b .tls-config
%patch7 -p1 -b .watermark 

%patch8 -p1 -b .missg-cmd-line-switches
%patch9 -p1 -b .ste-file
#%patch10 is applied right after doc setup 
%patch11 -p1 -b .systemd-time
%patch12 -p1 -b .imudp-deprecated-parameter
%patch13 -p1 -b .ratelimit-add-source
%patch14 -p1 -b .missing-chdir-w-chroot
%patch15 -p1 -b .glbDoneLoadCnf-segfault
%patch16 -p1 -b .set-unset-check-varName

%patch17 -p1 -b .num2ipv4
%patch18 -p1 -b .str2num-handle-emty-strings
%patch19 -p1 -b .snmp-mib
%patch20 -p1 -b .journal-switch
%patch21 -p1 -b .pmrfc3164sd
%patch22 -p1 -b .getaddrinfo

%patch23 -p1 -b .sd-service-network
#%patch24 is applied right after doc setup
%patch25 -p1 -b .journal-reloaded
%patch26 -p1 -b .set-statement-crash
%patch27 -p1 -b .nullptr-check
%patch28 -p1 -b .rebindinterval

%patch29 -p1 -b .imjournal-duplicates
%patch30 -p1 -b .property-deserialize

%patch31 -p1 -b .caching-sockaddr
%patch32 -p1 -b .imfile-symlink
%patch33 -p1 -b .buffer-overflow
%patch34 -p1 -b .msg-loss-shutdown
%patch35 -p1 -b .kubernetes-metadata
%patch36 -p1 -b .omelasticsearch-cert
#%patch37 is applied right after doc setup
%patch38 -p1 -b .omelasticsearch-libfastjson
%patch39 -p1 -b .omelasticsearch-bulk-rejection
#%patch40 is applied right after doc setup
#%patch41 is applied right after doc setup
%patch42 -p1 -b .manpage
%patch43 -p1 -b .async-writer
%patch44 -p1 -b .null-realloc-chk

%patch45 -p1 -b .omfwd-mem-corrupt
%patch46 -p1 -b .imfile-rotation
%patch47 -p1 -b .imptcp-octet-count
%patch48 -p1 -b .mmkubernetes-stop
%patch49 -p1 -b .symlink-err-flood
%patch50 -p1 -b .imjournal-cursor
%patch51 -p1 -b .internal-msg-memleak
#%patch52 is applied right after doc setup
%patch53 -p1 -b .imfile-buffer-overflow
%patch54 -p1 -b .imjournal-memleak

autoreconf 

%build
%ifarch sparc64
#sparc64 need big PIE
export CFLAGS="$RPM_OPT_FLAGS -fPIE -DPATH_PIDFILE=\\\"/var/run/syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpie -DPATH_PIDFILE=\\\"/var/run/syslogd.pid\\\""
export LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
%endif

%if %{want_hiredis}
# the hiredis-devel package doesn't provide a pkg-config file
export HIREDIS_CFLAGS=-I/usr/include/hiredis
export HIREDIS_LIBS=-L%{_libdir}
%endif
sed -i 's/%{version}/%{version}-%{release}/g' configure.ac
%configure \
	--prefix=/usr \
	--disable-static \
	--disable-testbench \
	--disable-liblogging-stdlog \
	--enable-elasticsearch \
	--enable-generate-man-pages \
	--enable-gnutls \
	--enable-gssapi-krb5 \
	--enable-imdiag \
	--enable-imfile \
	--enable-imjournal \
	--enable-impstats \
	--enable-imptcp \
	--enable-libdbi \
	--enable-mail \
	--enable-mmanon \
	--enable-mmaudit \
	--enable-mmcount \
	--enable-mmjsonparse \
	--enable-mmnormalize \
	--enable-mmsnmptrapd \
	--enable-mmutf8fix \
	--enable-mmkubernetes \
	--enable-mysql \
%if %{want_hiredis}
	--enable-omhiredis \
%endif
	--enable-omjournal \
%if %{want_mongodb}
	--enable-ommongodb \
%endif
	--enable-omprog \
%if %{want_rabbitmq}
	--enable-omrabbitmq \
%endif
	--enable-omruleset \
	--enable-omstdout \
	--enable-omudpspoof \
	--enable-omuxsock \
	--enable-omkafka \
	--enable-pgsql \
	--enable-pmaixforwardedfrom \
	--enable-pmcisconames \
	--enable-pmlastmsg \
	--enable-pmrfc3164sd \
	--enable-pmsnare \
	--enable-relp \
	--enable-snmp \
	--enable-unlimited-select \
	--enable-usertools \

make

%install
make DESTDIR=%{buildroot} install

install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
install -d -m 755 %{buildroot}%{_sysconfdir}/rsyslog.d
install -d -m 700 %{buildroot}%{rsyslog_statedir}
install -d -m 700 %{buildroot}%{rsyslog_pkidir}
install -d -m 755 %{buildroot}%{rsyslog_docdir}/html

install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rsyslog.conf
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/rsyslog
install -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/syslog
install -p -m 644 plugins/ommysql/createDB.sql %{buildroot}%{rsyslog_docdir}/mysql-createDB.sql
install -p -m 644 plugins/ompgsql/createDB.sql %{buildroot}%{rsyslog_docdir}/pgsql-createDB.sql
# extract documentation
cp -r doc/* %{buildroot}%{rsyslog_docdir}/html
# get rid of libtool libraries
rm -f %{buildroot}%{_libdir}/rsyslog/*.la
# get rid of socket activation by default
sed -i '/^Alias/s/^/;/;/^Requires=syslog.socket/s/^/;/' %{buildroot}%{_unitdir}/rsyslog.service

# convert line endings from "\r\n" to "\n"
cat tools/recover_qi.pl | tr -d '\r' > %{buildroot}%{_bindir}/rsyslog-recover-qi.pl

%post
for n in /var/log/{messages,secure,maillog,spooler}
do
	[ -f $n ] && continue
	umask 066 && touch $n
done
%systemd_post rsyslog.service

%preun
%systemd_preun rsyslog.service

%postun
%systemd_postun_with_restart rsyslog.service

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* ChangeLog
%exclude %{rsyslog_docdir}/html
%exclude %{rsyslog_docdir}/mysql-createDB.sql
%exclude %{rsyslog_docdir}/pgsql-createDB.sql
%dir %{_libdir}/rsyslog
%dir %{_sysconfdir}/rsyslog.d
%dir %{rsyslog_statedir}
%dir %{rsyslog_pkidir}
%{_sbindir}/rsyslogd
%attr(755,root,root) %{_bindir}/rsyslog-recover-qi.pl
%{_mandir}/man5/rsyslog.conf.5.gz
%{_mandir}/man8/rsyslogd.8.gz
%{_unitdir}/rsyslog.service
%config(noreplace) %{_sysconfdir}/rsyslog.conf
%config(noreplace) %{_sysconfdir}/sysconfig/rsyslog
%config(noreplace) %{_sysconfdir}/logrotate.d/syslog
# plugins
%{_libdir}/rsyslog/imdiag.so
%{_libdir}/rsyslog/imfile.so
%{_libdir}/rsyslog/imjournal.so
%{_libdir}/rsyslog/imklog.so
%{_libdir}/rsyslog/immark.so
%{_libdir}/rsyslog/impstats.so
%{_libdir}/rsyslog/imptcp.so
%{_libdir}/rsyslog/imtcp.so
%{_libdir}/rsyslog/imudp.so
%{_libdir}/rsyslog/imuxsock.so
%{_libdir}/rsyslog/lmnet.so
%{_libdir}/rsyslog/lmnetstrms.so
%{_libdir}/rsyslog/lmnsd_ptcp.so
%{_libdir}/rsyslog/lmregexp.so
%{_libdir}/rsyslog/lmstrmsrv.so
%{_libdir}/rsyslog/lmtcpclt.so
%{_libdir}/rsyslog/lmtcpsrv.so
%{_libdir}/rsyslog/lmzlibw.so
%{_libdir}/rsyslog/mmanon.so
%{_libdir}/rsyslog/mmcount.so
%{_libdir}/rsyslog/mmexternal.so
%{_libdir}/rsyslog/mmutf8fix.so
%{_libdir}/rsyslog/omjournal.so
%{_libdir}/rsyslog/ommail.so
%{_libdir}/rsyslog/omprog.so
%{_libdir}/rsyslog/omruleset.so
%{_libdir}/rsyslog/omstdout.so
%{_libdir}/rsyslog/omtesting.so
%{_libdir}/rsyslog/omuxsock.so
%{_libdir}/rsyslog/pmaixforwardedfrom.so
%{_libdir}/rsyslog/pmcisconames.so
%{_libdir}/rsyslog/pmlastmsg.so
%{_libdir}/rsyslog/pmrfc3164sd.so
%{_libdir}/rsyslog/pmsnare.so

%files crypto
%defattr(-,root,root)
%{_bindir}/rscryutil
%{_mandir}/man1/rscryutil.1.gz
%{_libdir}/rsyslog/lmcry_gcry.so

%files doc
%defattr(-,root,root)
%doc %{rsyslog_docdir}/html

%files elasticsearch
%defattr(-,root,root)
%{_libdir}/rsyslog/omelasticsearch.so

%if %{want_hiredis}
%files hiredis
%defattr(-,root,root)
%{_libdir}/rsyslog/omhiredis.so
%endif

%files libdbi
%defattr(-,root,root)
%{_libdir}/rsyslog/omlibdbi.so

%files mmaudit
%defattr(-,root,root)
%{_libdir}/rsyslog/mmaudit.so

%files mmjsonparse
%defattr(-,root,root)
%{_libdir}/rsyslog/mmjsonparse.so

%files mmnormalize
%defattr(-,root,root)
%{_libdir}/rsyslog/mmnormalize.so

%files mmsnmptrapd
%defattr(-,root,root)
%{_libdir}/rsyslog/mmsnmptrapd.so

%files mysql
%defattr(-,root,root)
%doc %{rsyslog_docdir}/mysql-createDB.sql
%{_libdir}/rsyslog/ommysql.so

%if %{want_mongodb}
%files mongodb
%defattr(-,root,root)
%{_bindir}/logctl
%{_libdir}/rsyslog/ommongodb.so
%endif

%files pgsql
%defattr(-,root,root)
%doc %{rsyslog_docdir}/pgsql-createDB.sql
%{_libdir}/rsyslog/ompgsql.so

%if %{want_rabbitmq}
%files rabbitmq
%defattr(-,root,root)
%{_libdir}/rsyslog/omrabbitmq.so
%endif

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

%files udpspoof
%defattr(-,root,root)
%{_libdir}/rsyslog/omudpspoof.so

%files kafka
%{_libdir}/rsyslog/omkafka.so

%files mmkubernetes
%{_libdir}/rsyslog/mmkubernetes.so

%changelog
* Tue Jul 23 2019 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-41
RHEL 7.7.z ERRATUM
- added patch resolving memory leaks in imjournal
  resolves: rhbz#1725067

* Mon Apr 08 2019 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-38
RHEL 7.7 ERRATUM
- added patch increasing max path size preventing buffer overflow
  with too long paths
  resolves: rhbz#1656860

* Wed Mar 20 2019 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-37
RHEL 7.7 ERRATUM
- edited patch fixing mmkubernetes halt after pod deletition
  (covscan found an issue in previous version)
  resolves: rhbz#1622767
- added patch stopping flooding logs with journald errors
  resolves: rhbz#1632211
- added patch stopping flooding logs with symlink false-positives
  resolves: rhbz#1685901
- added patch stopping memory leak when processing internal msgs
  resolves: rhbz#1666365
- added documentation patch with info about CRI-O to mmkubernetes
  resolves: rhbz#1625935

* Wed Feb 27 2019 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-36
RHEL 7.7 ERRATUM
- added patch fixing mmkubernetes halt after pod deletition
  resolves: rhbz#1622767

* Mon Jan 28 2019 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-35
RHEL 7.7 ERRATUM
- added patch fixing memory corruption in omfwd module
  resolves: rhbz#1632659
- added patch fixing imfile sopping monitor after rotation
  resolves: rhbz#1649250
- added patch addressing imptcp CVE-2018-16881
  resolves: rhbz#1658288

* Tue Aug 07 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-34
RHEL 7.6 ERRATUM
- updated imfile rewrite patch with parent name bugfix
  resolves: rhbz#1531295

* Tue Aug 07 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-33
RHEL 7.6 ERRATUM
- updated imfile rewrite patch with extended symlink watching
  resolves: rhbz#1531295
- updated mmkubernetes patch to accept dots in pod name
  resolves: rhbz#1539193

* Fri Aug 03 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-32
RHEL 7.6 ERRATUM
- updated imfile rewrite patch with no log on EACCES
  resolves: rhbz#1531295
- removed now needless build-deps

* Mon Jul 30 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-31
RHEL 7.6 ERRATUM
- added new patch fixing ompipe dropping messages when pipe full
  resolves: rhbz#1591819
- updated mmkubernetes patch to accept non-kubernetes containers
  resolves: rhbz#1539193
  resolves: rhbz#1609023
- removed json-parsing patches as the bug is now fixed in liblognorm

* Wed Jul 25 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-30
RHEL 7.6 ERRATUM
- updated imfile rewrite patch with next bugfix
  resolves: rhbz#1531295
- updated imjournal duplicates patch making slower code optional
  and added corresponding doc patch
  resolves: rhbz#1538372

* Mon Jul 23 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-29
RHEL 7.6 ERRATUM
- updated imfile rewrite patch with another bugfix
  resolves: rhbz#1531295

* Fri Jul 20 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-28
RHEL 7.6 ERRATUM
- updated imfile rewrite patch fixing next round of regressions
  resolves: rhbz#1531295
  resolves: rhbz#1602156
- updated mmkubernetes patch with NULL ret-check
  resolves: rhbz#1539193

* Tue Jul 17 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-27
RHEL 7.6 ERRATUM
- updated imfile rewrite patch fixing last update regressions
  resolves: rhbz#1531295
- added patch fixing deadlock in async logging
  resolves: rhbz#1559408
- added patch fixing NULL access in worktable create
  resolves: rhbz#1600462
- now putting release number into configure to have it present
  in error messages

* Mon Jul 09 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-26
RHEL 7.6 ERRATUM
- updated imfile rewrite patch according to early testing
  resolves: rhbz#1531295
- added patch fixing pid file name in manpage
  resolves: rhbz#1597264
- updated json-parsing patch with one more bugfix
  resolves: rhbz#1565219

* Fri Jun 29 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-24
RHEL 7.6 ERRATUM
- updated imfile rewrite patch with fixes from covscan
  resolves: rhbz#1531295
- updated mmkubernetes patch with fixes from covscan
  resolves: rhbz#1539193
- updated imjournal duplicates patch with fixes from covscan
  resolves: rhbz#1538372
- updated omelastic enhancement patch with fixes from covscan
  resolves: rhbz#1565214

* Wed Jun 27 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-23
RHEL 7.6 ERRATUM
- added backport of leading $ support to json-parsing patch
  resolves: rhbz#1565219
- The required info is already contained in rsyslog-doc package
  so there is no patch for this one
  resolves: rhbz#1553700

* Tue Jun 26 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-22
RHEL 7.6 ERRATUM
- edited patch for top-level json parsing with bugfix
  resolves: rhbz#1565219
- renamed doc patches and added/updated new ones for mmkubernetes
  omelasticsearch and json parsing
- renamed patch fixing buffer overflow in parser - memcpy()
  resolves: rhbz#1582517

* Mon Jun 25 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-21
RHEL 7.6 ERRATUM
- fixed imfile rewrite backport patch, added few more bugfixes
  resolves: rhbz#1531295
- added also doc patch for omelastic client certs
  resolves: rhbz#1507145
- cleaned and shortened patch for omelastic error handling
  resolves: rhbz#1565214
- enabled patch for json top-level parsing
  resolves: rhbz#1565219
- merged mmkubernetes patches into one and enabled the module
  resolves: rhbz#1539193
  resolves: rhbz#1589924
  resolves: rhbz#1590582

* Sun Jun 24 2018 Noriko Hosoi <nhosoi@redhat.com> - 8.24.0-21
RHEL 7.6 ERRATUM
resolves: rhbz#1582517 - Buffer overflow in memcpy() in parser.c
resolves: rhbz#1539193 - RFE: Support for mm kubernetes plugin
resolves: rhbz#1589924 - RFE: Several fixes for mmkubernetes
resolves: rhbz#1590582 - mmkubernetes - use version=2 in rulebase files to avoid memory leak
resolves: rhbz#1507145 - RFE: omelasticsearch support client cert authentication
resolves: rhbz#1565214 - omelasticsearch needs better handling for bulk index rejections and other errors
Disables Patch32: rsyslog-8.24.0-rhbz1531295-imfile-rewrite-with-symlink.patch
Disables Patch34: rsyslog-8.24.0-rhbz1565219-parse-json-into-top-level-fields-in-mess.patch; It BuildRequires/Requires: libfastjson >= 0.99.4-3

* Fri Jun 01 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-20
RHEL 7.6 ERRATUM
- added a patch backporting imfile module rewrite and 
  adding symlink support
	resolves: rhbz#1531295

* Tue May 29 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-19
RHEL 7.6 ERRATUM
- added new kafka sub-package with enabling of omkafka module
  resolves: rhbz#1482819

* Thu May 17 2018 Radovan Sroka <rsroka@redhat.com> - 8.24.0-18
- caching the whole sockaddr structure instead of sin_addr causing memory leak
  resolves: rhbz#1512551

* Fri Apr 27 2018 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-17
RHEL 7.6 ERRATUM
- fixed imjournal duplicating messages on log rotation
  resolves: rhbz#1538372
- re-enabled 32-bit arches to not break dependent packages
  resolves: rhbz#1571850

* Thu Nov 09 2017 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-16
RHEL 7.5 ERRATUM
- edited the patch to conform to latest upstream doc
  resolves: rhbz#1459896 (failedQA)
- disabled 32-bit builds on all arches as they are not shipped
  anymore in RHEL7

* Tue Oct 31 2017 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-15
RHEL 7.5 ERRATUM
- made rsyslog-doc noarch and fixed search on doc regeneration
  resolves: rhbz#1507028

* Tue Oct 31 2017 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-14
RHEL 7.5 ERRATUM
- renamed patch for undocumented recover_qi script to correct bz number
  resolves: rhbz#1507028
- added patch ensuring relp conneciton is active before closing it
  resolves: rhbz#1505103

* Mon Oct 09 2017 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-13
RHEL 7.5 ERRATUM
- added patch to properly resolve FQDN
  resolves: rhbz#1401456
- added documentation patch correcting qeues default values
  resolves: rhbz#1459896
- added patch adjusting log level of journal reloaded msg
  resolves: rhbz#1497985 
- added patch to prevent crash with invalid set statement
  this also obsoletes patch2 (for 1188503) 
  resolves: rhbz#1462160
- added patch with nullptr check to prevent ABRT
  resolves: rhbz#1488186

* Wed May 10 2017 Radovan Sroka <rsroka@redhat.com> - 8.24.0-12
- added BuildRequires for systemd >= 219-39 depends on rhbz#1419228

* Tue May 09 2017 Radovan Sroka <rsroka@redhat.com> - 8.24.0-11
RHEL 7.4 ERRATUM
- added new patch that backports num2ipv4 due to rhbz#1427821
  resolves: rhbz#1427821
- enable pmrfc3164sd module
  resolves: rhbz#1431616

* Wed May 03 2017 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-10
RHEL 7.4 ERRATUM
- edited patches Patch19 and Patch21
  resolves: rhbz#1419228(coverity scan problems)
  resolves: rhbz#1056548(failed QA, coverity scan problems)

* Tue May 02 2017 Jiri Vymazal <jvymazal@redhat.com> - 8.24.0-9
RHEL 7.4 ERRATUM
- added autoreconf call
- added patch to replace gethostbyname with getaddrinfo call
  resolves: rhbz#1056548(failed QA)

* Wed Apr 19 2017 Radovan Sroka <rsroka@redhat.com> - 8.24.0-8
RHEL 7.4 ERRATUM
- added dependency automake autoconf libtool due to yum-builddep
- reenable omruleset module
  resolves: rhbz#1431615
  resolves: rhbz#1428403
  resolves: rhbz#1427821(fix regression, failed QA)
  resolves: rhbz#1432069
- resolves: rhbz#1165236
  resolves: rhbz#1419228
  resolves: rhbz#1431616 
  resolves: rhbz#1196230(failed QA)

* Thu Mar 02 2017 Radovan Sroka <rsroka@redhat.com> - 8.24.0-7
- reverted logrotate file that was added by mistake

* Wed Mar 01 2017 Radovan Sroka <rsroka@redhat.com> - 8.24.0-6
- RHEL 7.4 ERRATUM
- rsyslog rebase to 8.24
- added patch to prevent segfault while setting aclResolveHostname
  config options
  resolves: rhbz#1422414
- added patch to check config variable names at startup
  resolves: rhbz#1427828
- added patch for str2num to handle empty strings
  resolves: rhbz#1427821
- fixed typo in added-chdir patch
  resolves: rhbz#1422789
- added patch to log source process when beginning rate-limiting
  resolves: rhbz#1196230
- added patch to chdir after chroot
  resolves: rhbz#1422789
- added patch to remove "inputname" imudp module parameter 
  deprecation warnings
  resolves: rhbz#1403907
- added patch which resolves situation when time goes backwards
  and statefile is invalid
  resolves rhbz#1088021
- added a patch to bring back deprecated cmd-line switches and
  remove associated warnings
  resolves: rhbz#1403831
- added documentation recover_qi.pl
  resolves: rhbz#1286707
- add another setup for doc package
- add --enable-generate-man-pages to configure parameters;
  the rscryutil man page isn't generated without it
  https://github.com/rsyslog/rsyslog/pull/469
- enable mmcount, mmexternal modules
- remove omruleset and pmrfc3164sd modules

* Thu Jul 14 2016 Tomas Heinrich <theinric@redhat.com> 7.4.7-16
- add a patch to prevent races in libjson-c calls
  resolves: rhbz#1222746

* Sun Jul 10 2016 Tomas Heinrich <theinric@redhat.com> 7.4.7-15
- add a patch to make state file handling in imjournal more robust
  resolves: rhbz#1245194
- add a patch to support wildcards in imfile
  resolves: rhbz#1303617

* Fri May 20 2016 Tomas Heinrich <theinric@redhat.com> 7.4.7-14
- add a patch to prevent loss of partial messages
  resolves: rhbz#1312459
- add a patch to allow multiple rulesets in imrelp
  resolves: rhbz#1223566
- add a patch to fix a race condition during shutdown
  resolves: rhbz#1295798
- add a patch to backport the mmutf8fix plugin
  resolves: rhbz#1146237
- add a patch to order service startup after the network
  resolves: rhbz#1263853

* Mon May 16 2016 Tomas Heinrich <theinric@redhat.com> 7.4.7-13
- add a patch to prevent crashes when using multiple rulesets
  resolves: rhbz#1224336
- add a patch to keep the imjournal state file updated
  resolves: rhbz#1216957
- add a patch to fix an undefined behavior caused by the maxMessageSize directive
  resolves: rhbz#1214257
- add a patch to prevent crashes when using rulesets with a parser
  resolves: rhbz#1282687

* Fri Aug 28 2015 Tomas Heinrich <theinric@redhat.com> 7.4.7-12
- amend the patch for rhbz#1151041
  resolves: rhbz#1257150

* Tue Aug 18 2015 Radovan Sroka <rsroka@redhat.com> 7.4.7-11
- add patch that resolves config.guess system-recognition on ppc64le architecture
  resolves: rhbz:1254511

* Mon Aug 03 2015 Tomas Heinrich <theinric@redhat.com> 7.4.7-10
- add a patch to prevent field truncation in imjournal
  resolves: rhbz#1101602
- add a patch to enable setting a default TAG
  resolves: rhbz#1188503
- add a patch to fix a nonfunction hostname setting in imuxsock
  resolves: rhbz#1184402

* Mon Jul 20 2015 Tomas Heinrich <theinric@redhat.com> 7.4.7-9
- update the patch fixing a race condition in directory creation
  resolves: rhbz#1202489
- improve provided documentation
  - move documentation from all subpackages under a single directory
  - add missing images
  - remove doc files without content
  - add a patch making various corrections to the HTML documentation
  resolves: rhbz#1238713
- add a patch to prevent division-by-zero errors
  resolves: rhbz#1078878
- add a patch to clarify usage of the SysSock.Use option
  resolves: rhbz#1143846
- add a patch to support arbitrary number of listeners in imuxsock
  - drop patch for rhbz#1053669 as it has been merged into this one
  resolves: rhbz#1151041

* Fri Jul 03 2015 Tomas Heinrich <theinric@redhat.com> 7.4.7-8
- modify the service file to automatically restart rsyslog on failure
  resolves: rhbz#1061322
- add explicitly versioned dependencies on libraries which do not have
  correctly versioned sonames
  resolves: rhbz#1107839
- make logrotate tolerate missing log files
  resolves: rhbz#1144465
- backport the mmcount plugin
  resolves: rhbz#1151037
- set the default service umask to 0066
  resolves: rhbz#1228192
- add a patch to make imjournal sanitize messages as imuxsock does it
  resolves: rhbz#743890
- add a patch to fix a bug preventing certain imuxsock directives from
  taking effect
  resolves: rhbz#1184410
- add a patch to fix a race condition in directory creation
  resolves: rhbz#1202489

* Tue Oct 07 2014 Tomas Heinrich <theinric@redhat.com> 7.4.7-7
- fix CVE-2014-3634
  resolves: #1149153

* Wed Mar 26 2014 Tomas Heinrich <theinric@redhat.com> 7.4.7-6
- disable the imklog plugin by default
  the patch for rhbz#1038136 caused duplication of kernel messages since the
  messages read by the imklog plugin were now also pulled in from journald
  resolves: #1078654

* Wed Feb 19 2014 Tomas Heinrich <theinric@redhat.com> 7.4.7-5
- move the rscryutil man page to the crypto subpackage
  resolves: #1056565
- add a patch to prevent message loss in imjournal
  rsyslog-7.4.7-bz1038136-imjournal-message-loss.patch
  resolves: #1038136

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 7.4.7-4
- Mass rebuild 2014-01-24

* Mon Jan 20 2014 Tomas Heinrich <theinric@redhat.com> 7.4.7-3
- replace rsyslog-7.3.15-imuxsock-warning.patch
  with rsyslog-7.4.7-bz1053669-imuxsock-wrn.patch
  resolves: #1053669
- add rsyslog-7.4.7-bz1052266-dont-link-libee.patch to prevent
  linking the main binary with libee
  resolves: #1052266
- add rsyslog-7.4.7-bz1054171-omjournal-warning.patch to fix
  a condition for issuing a warning in omjournal
  resolves: #1054171
- drop the "v5" string from the conf file as it's misleading
  resolves: #1040036

* Wed Jan 15 2014 Honza Horak <hhorak@redhat.com> - 7.4.7-2
- Rebuild for mariadb-libs
  Related: #1045013

* Mon Jan 06 2014 Tomas Heinrich <theinric@redhat.com> 7.4.7-1
- rebase to 7.4.7
  add requirement on libestr >= 0.1.9
  resolves: #836485
  resolves: #1020854
  resolves: #1040036
- drop patch 4; not needed anymore
  rsyslog-7.4.2-imuxsock-rfc3339.patch
- install the rsyslog-recover-qi.pl tool
- fix a typo in a package description
- add missing defattr directives
- add a patch to remove references to Google ads in the html docs
  rsyslog-7.4.7-bz1030044-remove-ads.patch
  Resolves: #1030043
- add a patch to allow numeric specification of UIDs/GUIDs
  rsyslog-7.4.7-numeric-uid.patch
  resolves: #1032198
- change the installation prefix to "/usr"
  resolves: #1032223
- fix a bad date in the changelog
  resolves: #1043622
- resolve a build issue with missing mysql_config by adding
  additional BuildRequires for the mysql package
- add a patch to resolve build issue on ppc
  rsyslog-7.4.7-omelasticsearch-atomic-inst.patch

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 7.4.2-5
- Mass rebuild 2013-12-27

* Wed Nov 06 2013 Tomas Heinrich <theinric@redhat.com> 7.4.2-4
- add a patch to fix issues with rfc 3339 timestamp parsing
  resolves: #1020826

* Fri Jul 12 2013 Jan Safranek <jsafrane@redhat.com> - 7.4.2-3
- Rebuilt for new net-snmp

* Wed Jul 10 2013 Tomas Heinrich <theinric@redhat.com> 7.4.2-2
- make compilation of the rabbitmq plugin optional
  resolves: #978919

* Tue Jul 09 2013 Tomas Heinrich <theinric@redhat.com> 7.4.2-1
- rebase to 7.4.2
  most importantly, this release fixes a potential vulnerability,
  see http://www.lsexperts.de/advisories/lse-2013-07-03.txt
  the impact should be low as only those using the omelasticsearch
  plugin with a specific configuration are exposed

* Mon Jun 17 2013 Tomas Heinrich <theinric@redhat.com> 7.4.1-1
- rebase to 7.4.1
  this release adds code that somewhat mitigates damage in cases
  where large amounts of messages are received from systemd
  journal (see rhbz#974132)
- regenerate patch 0
- drop patches merged upstream: 4..8
- add a dependency on the version of systemd which resolves the bug
  mentioned above
- update option name in rsyslog.conf

* Wed Jun 12 2013 Tomas Heinrich <theinric@redhat.com> 7.4.0-1
- rebase to 7.4.0
- drop autoconf automake libtool from BuildRequires
- depends on systemd >= 201 because of the sd_journal_get_events() api
- add a patch to prevent a segfault in imjournal caused by a bug in
  systemd journal
- add a patch to prevent an endless loop in the ratelimiter
- add a patch to prevent another endless loop in the ratelimiter
- add a patch to prevent a segfault in imjournal for undefined state file
- add a patch to correctly reset state in the ratelimiter

* Tue Jun 04 2013 Tomas Heinrich <theinric@redhat.com> 7.3.15-1.20130604git6e72fa6
- rebase to an upstream snapshot, effectively version 7.3.15
  plus several more changes
- drop patches 3, 4 - merged upstream
- add a patch to silence warnings emitted by the imuxsock module
- drop the imkmsg plugin
- enable compilation of additional modules
  imjournal, mmanon, omjournal, omrabbitmq
- new subpackages: crypto, rabbitmq
- add python-docutils and autoconf to global BuildRequires
- drop the option for backwards compatibility from the
  sysconfig file - it is no longer supported
- call autoreconf to prepare the snapshot for building
- switch the local message source from imuxsock to imjournal
  the imuxsock module is left enabled so it is easy to swich back to
  it and because systemd drops a file into /etc/rsyslog.d which only
  imuxsock can parse

* Wed Apr 10 2013 Tomas Heinrich <theinric@redhat.com> 7.3.10-1
- rebase to 7.3.10
- add a patch to resolve #950088 - ratelimiter segfault, merged upstream
  rsyslog-7.3.10-ratelimit-segv.patch
- add a patch to correct a default value, merged upstream
  rsyslog-7.3.10-correct-def-val.patch
- drop patch 5 - fixed upstream

* Thu Apr 04 2013 Tomas Heinrich <theinric@redhat.com> 7.3.9-1
- rebase to 7.3.9

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Tomas Heinrich <theinric@redhat.com> 7.2.5-2
- update a line in rsyslog.conf for the new syntax

* Sun Jan 13 2013 Tomas Heinrich <theinric@redhat.com> 7.2.5-1
- upgrade to upstream version 7.2.5
- update the compatibility mode in sysconfig file

* Mon Dec 17 2012 Tomas Heinrich <theinric@redhat.com> 7.2.4-2
- add a condition to disable several subpackages

* Mon Dec 10 2012 Tomas Heinrich <theinric@redhat.com> 7.2.4-1
- upgrade to upstream version 7.2.4
- remove trailing whitespace

* Tue Nov 20 2012 Tomas Heinrich <theinric@redhat.com> 7.2.2-1
- upgrade to upstream version 7.2.2
  update BuildRequires
- remove patches merged upstream
  rsyslog-5.8.7-sysklogd-compat-1-template.patch
  rsyslog-5.8.7-sysklogd-compat-2-option.patch
  rsyslog-5.8.11-close-fd1-when-forking.patch
- add patch from Milan Bartos <mbartos@redhat.com>
  rsyslog-7.2.1-msg_c_nonoverwrite_merge.patch
- remove the rsyslog-sysvinit package
- clean up BuildRequires, Requires
- remove the 'BuildRoot' tag
- split off a doc package
- compile additional modules (some of them in separate packages):
  elasticsearch
  hiredis
  mmjsonparse
  mmnormalize
  mmaudit
  mmsnmptrapd
  mongodb
- correct impossible timestamps in older changelog entries
- correct typos, trailing spaces, etc
- s/RPM_BUILD_ROOT/{buildroot}/
- remove the 'clean' section
- replace post* scriptlets with systemd macros

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Tomas Heinrich <theinric@redhat.com> 5.8.11-2
- update systemd patch: remove the 'ExecStartPre' option

* Wed May 23 2012 Tomas Heinrich <theinric@redhat.com> 5.8.11-1
- upgrade to new upstream stable version 5.8.11
- add impstats and imptcp modules
- include new license text files
- consider lock file in 'status' action
- add patch to update information on debugging in the man page
- add patch to prevent debug output to stdout after forking
- add patch to support ssl certificates with domain names longer than 128 chars

* Fri Mar 30 2012 Jon Ciesla <limburgher@gmail.com> 5.8.7-2
- libnet rebuild.

* Mon Jan 23 2012 Tomas Heinrich <theinric@redhat.com> 5.8.7-1
- upgrade to new upstream version 5.8.7
- change license from 'GPLv3+' to '(GPLv3+ and ASL 2.0)'
  http://blog.gerhards.net/2012/01/rsyslog-licensing-update.html
- use a specific version for obsoleting sysklogd
- add patches for better sysklogd compatibility (taken from upstream)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 25 2011 Tomas Heinrich <theinric@redhat.com> 5.8.6-1
- upgrade to new upstream version 5.8.6
- obsolete sysklogd
  Resolves: #748495

* Tue Oct 11 2011 Tomas Heinrich <theinric@redhat.com> 5.8.5-3
- modify logrotate configuration to omit boot.log
  Resolves: #745093

* Tue Sep 06 2011 Tomas Heinrich <theinric@redhat.com> 5.8.5-2
- add systemd-units to BuildRequires for the _unitdir macro definition

* Mon Sep 05 2011 Tomas Heinrich <theinric@redhat.com> 5.8.5-1
- upgrade to new upstream version (CVE-2011-3200)

* Fri Jul 22 2011 Tomas Heinrich <theinric@redhat.com> 5.8.2-3
- move the SysV init script into a subpackage
- Resolves: 697533

* Mon Jul 11 2011 Tomas Heinrich <theinric@redhat.com> 5.8.2-2
- rebuild for net-snmp-5.7 (soname bump in libnetsnmp)

* Mon Jun 27 2011 Tomas Heinrich <theinric@redhat.com> 5.8.2-1
- upgrade to new upstream version 5.8.2

* Mon Jun 13 2011 Tomas Heinrich <theinric@redhat.com> 5.8.1-2
- scriptlet correction
- use macro in unit file's path

* Fri May 20 2011 Tomas Heinrich <theinric@redhat.com> 5.8.1-1
- upgrade to new upstream version
- correct systemd scriptlets (#705829)

* Mon May 16 2011 Bill Nottingham <notting@redhat.com> - 5.7.9-3
- combine triggers (as rpm will only execute one) - fixes upgrades (#699198)

* Tue Apr 05 2011 Tomas Heinrich <theinric@redhat.com> 5.7.10-1
- upgrade to new upstream version 5.7.10

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 5.7.9-2
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Fri Mar 18 2011 Tomas Heinrich <theinric@redhat.com> 5.7.9-1
- upgrade to new upstream version 5.7.9
- enable compilation of several new modules,
  create new subpackages for some of them
- integrate changes from Lennart Poettering
  to add support for systemd
  - add rsyslog-5.7.9-systemd.patch to tweak the upstream
    service file to honour configuration from /etc/sysconfig/rsyslog

* Fri Mar 18 2011 Dennis Gilmore <dennis@ausil.us> - 5.6.2-3
- sparc64 needs big PIE

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Tomas Heinrich <theinric@redhat.com> 5.6.2-1
- upgrade to new upstream stable version 5.6.2
- drop rsyslog-5.5.7-remove_include.patch; applied upstream
- provide omsnmp module
- use correct name for lock file (#659398)
- enable specification of the pid file (#579411)
- init script adjustments

* Wed Oct 06 2010 Tomas Heinrich <theinric@redhat.com> 5.5.7-1
- upgrade to upstream version 5.5.7
- update configuration and init files for the new major version
- add several directories for storing auxiliary data
- add ChangeLog to documentation
- drop unlimited-select.patch; integrated upstream
- add rsyslog-5.5.7-remove_include.patch to fix compilation

* Tue Sep 07 2010 Tomas Heinrich <theinric@redhat.com> 4.6.3-2
- build rsyslog with PIE and RELRO

* Thu Jul 15 2010 Tomas Heinrich <theinric@redhat.com> 4.6.3-1
- upgrade to new upstream stable version 4.6.3

* Wed Apr 07 2010 Tomas Heinrich <theinric@redhat.com> 4.6.2-1
- upgrade to new upstream stable version 4.6.2
- correct the default value of the OMFileFlushOnTXEnd directive

* Thu Feb 11 2010 Tomas Heinrich <theinric@redhat.com> 4.4.2-6
- modify rsyslog-4.4.2-unlimited-select.patch so that
  running autoreconf is not needed
- remove autoconf, automake, libtool from BuildRequires
- change exec-prefix to nil

* Wed Feb 10 2010 Tomas Heinrich <theinric@redhat.com> 4.4.2-5
- remove '_smp_mflags' make argument as it seems to be
  producing corrupted builds

* Mon Feb 08 2010 Tomas Heinrich <theinric@redhat.com> 4.4.2-4
- redefine _libdir as it doesn't use _exec_prefix

* Thu Dec 17 2009 Tomas Heinrich <theinric@redhat.com> 4.4.2-3
- change exec-prefix to /

* Wed Dec 09 2009 Robert Scheck <robert@fedoraproject.org> 4.4.2-2
- run libtoolize to avoid errors due mismatching libtool version

* Thu Dec 03 2009 Tomas Heinrich <theinric@redhat.com> 4.4.2-1
- upgrade to new upstream stable version 4.4.2
- add support for arbitrary number of open file descriptors

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
- add BuildRequires for zlib compression feature

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
