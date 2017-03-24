%define name hbase
%define version 1.0.3
%define __jar_repack %{nil}

Name: %{name}
Version: %{version}
Release: 3%{?dist}
Summary: HBase is the Hadoop database. Use it when you need random, realtime read/write access to your Big Data. This project's goal is the hosting of very large tables -- billions of rows X millions of columns -- atop clusters of commodity hardware. 
URL: http://hbase.apache.org/
Group: Development/Libraries
License: ASL 2.0
Source0: %{name}-%{version}-bin.tar.gz
Source1: hbase-master.init
Source2: hbase-regionserver.init
Source3: hbase-rest.init
Source4: hbase-thrift.init
BuildArch: noarch
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires: coreutils, /usr/sbin/useradd, /sbin/chkconfig, /sbin/service
Requires: hadoop-hdfs, zookeeper >= 3.3.1, bigtop-utils >= 0.7
Requires(postun): /usr/sbin/userdel

%description
HBase is an open-source, distributed, column-oriented store modeled after Google' Bigtable: A Distributed Storage System for Structured Data by Chang et al. Just as Bigtable leverages the distributed data storage provided by the Google File System, HBase provides Bigtable-like capabilities on top of Hadoop. HBase includes:

    * Convenient base classes for backing Hadoop MapReduce jobs with HBase tables
    * Query predicate push down via server side scan and get filters
    * Optimizations for real time queries
    * A high performance Thrift gateway
    * A REST-ful Web service gateway that supports XML, Protobuf, and binary data encoding options
    * Cascading source and sink modules
    * Extensible jruby-based (JIRB) shell
    * Support for exporting metrics via the Hadoop metrics subsystem to files or Ganglia; or via JMX

%package master
Summary: The Hadoop HBase master Server.
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires: /lib/lsb/init-functions

%description master
HMaster is the "master server" for a HBase. There is only one HMaster for a single HBase deployment.

%package regionserver
Summary: The Hadoop HBase RegionServer server.
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires: /lib/lsb/init-functions

%description regionserver 
HRegionServer makes a set of HRegions available to clients. It checks in with the HMaster. There are many HRegionServers in a single HBase deployment.

%package thrift
Summary: The Hadoop HBase Thrift Interface
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires: /lib/lsb/init-functions

%description thrift
ThriftServer - this class starts up a Thrift server which implements the Hbase API specified in the Hbase.thrift IDL file.
"Thrift is a software framework for scalable cross-language services development. It combines a powerful software stack with a code generation engine to build services that work efficiently and seamlessly between C++, Java, Python, PHP, and Ruby. Thrift was developed at Facebook, and we are now releasing it as open source." For additional information, see http://developers.facebook.com/thrift/. Facebook has announced their intent to migrate Thrift into Apache Incubator.

%package doc
Summary: Hbase Documentation
Group: Documentation
BuildArch: noarch
Obsoletes: %{name}-docs

%description doc
Documentation for Hbase

%package rest
Summary: The Apache HBase REST gateway
Group: System/Daemons
Requires: %{name} = %{version}-%{release}
Requires(pre): %{name} = %{version}-%{release}
Requires: /lib/lsb/init-functions

%description rest
The Apache HBase REST gateway

%prep
%setup -n %{name}-%{version}

%pre
/usr/bin/getent passwd %{name} > /dev/null 2>&1 || /usr/sbin/useradd -r -d /usr/lib/hbase -s /sbin/nologin -U %{name}

%install
%__mkdir -p $RPM_BUILD_ROOT/usr/lib/hbase $RPM_BUILD_ROOT/var/run/hbase $RPM_BUILD_ROOT/var/log/hbase $RPM_BUILD_ROOT/etc/hbase $RPM_BUILD_ROOT/etc/rc.d/init.d
%__cp -rp lib $RPM_BUILD_ROOT/usr/lib/hbase/
%__cp -rp conf $RPM_BUILD_ROOT/usr/lib/hbase/
%__cp -rp docs $RPM_BUILD_ROOT/usr/lib/hbase/
%__cp -rp bin $RPM_BUILD_ROOT/usr/lib/hbase/
%__chmod -R 0755 $RPM_BUILD_ROOT/usr/lib/hbase/bin
%__install -m 0644 CHANGES.txt LICENSE.txt NOTICE.txt README.txt $RPM_BUILD_ROOT/usr/lib/hbase/
%__install -m 0755 %SOURCE1 $RPM_BUILD_ROOT/etc/rc.d/init.d/hbase-master
%__install -m 0755 %SOURCE2 $RPM_BUILD_ROOT/etc/rc.d/init.d/hbase-regionserver
%__install -m 0755 %SOURCE3 $RPM_BUILD_ROOT/etc/rc.d/init.d/hbase-rest
%__install -m 0755 %SOURCE4 $RPM_BUILD_ROOT/etc/rc.d/init.d/hbase-thrift

%files
%dir %attr(0755,hbase,hbase) /var/log/hbase
%dir %attr(0755,hbase,hbase) /var/run/hbase
%dir %attr(0755,hbase,hbase) /etc/hbase
/usr/lib/hbase/lib
/usr/lib/hbase/bin
/usr/lib/hbase/conf

%doc
/usr/lib/hbase/CHANGES.txt
/usr/lib/hbase/LICENSE.txt
/usr/lib/hbase/NOTICE.txt
/usr/lib/hbase/README.txt
/usr/lib/hbase/docs

%files master
%attr(0755,root,root) /etc/rc.d/init.d/hbase-master

%files regionserver
%attr(0755,root,root) /etc/rc.d/init.d/hbase-regionserver

%files rest
%attr(0755,root,root) /etc/rc.d/init.d/hbase-rest

%files thrift
%attr(0755,root,root) /etc/rc.d/init.d/hbase-thrift

