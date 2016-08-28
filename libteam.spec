Summary:	Library for controlling team network device
Summary(pl.UTF-8):	Biblioteka do sterowania grupowymi urządzeniami sieciowymi
Name:		libteam
Version:	1.26
Release:	3
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://libteam.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	f8529a3bfee28500bef5faff6aeb0063
Source1:	teamd.sysconfig
Source2:	teamd-lvl1-service-generator
Source3:	teamd-lvl2-service-generator
Source4:	teamd@.service
Source5:	teamd-lvl1.target
Source6:	teamd-lvl2.target
# You might not be able to shut down your system without this:
# https://lists.fedorahosted.org/archives/list/libteam@lists.fedorahosted.org/thread/QYCLFVANHB47URKOST5HFT5EVWPRHGVQ/
Source7:	teamd-shutdown-workaround.service
Patch0:		%{name}-link.patch
URL:		http://libteam.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	jansson-devel
# if non-root --with-group or --with-user
#BuildRequires:	libcap-devel
BuildRequires:	libdaemon-devel
BuildRequires:	libnl-devel >= 3.2
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	zeromq-devel >= 3.2.0
Requires:	libnl >= 3.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The purpose of the Team driver is to provide a mechanism to team
multiple NICs (ports) into one logical one (teamdev) at L2 layer. The
process is called "channel bonding", "Ethernet bonding", "channel
teaming", "link aggregation", etc. This is already implemented in the
Linux kernel by the bonding driver.

One thing to note is that Team driver project does try to provide the
similar functionality as the bonding driver, however architecturally
it is quite different from bonding driver. Team driver is modular,
userspace driven, very lean and efficient, and it does have some
distinct advantages over bonding. The way Team is configured differs
dramatically from the way bonding is.

%description -l pl.UTF-8
Celem sterownika Team jest dostarczenie mechanizmu do grupowania
(team) wielu interfejsów (portów) sieciowych (czyli NIC) w jeden
logiczny (teamdev) w warstwie L2. Proces ten jest nazywany
"channel bonding", "Ethernet bonding", "channel teaming", "link
aggregation" itp. Jest to już zaimplementowane w jądrze Linuksa
poprzez sterownik bonding.

Należy zauważyć, że projekt sterownika Team próbuje zapewnić
podobną funkcjonalność co sterownik bonding, ale architektonicznie
różni się od niego. Jest modularny, działa w przestrzeni użytkownika,
jest bardzo lekki i wydajny, ma też kilka zalet, których nie ma
bonding. Sposób konfiguracji sterownika Team znacząco różni się od
konfiguracji sterownika bonding.

%package devel
Summary:	Header files for libteam library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libteam
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libnl-devel >= 3.2

%description devel
Header files for libteam library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libteam.

%package static
Summary:	Static libteam library
Summary(pl.UTF-8):	Statyczna biblioteka libteam
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libteam library.

%description static -l pl.UTF-8
Statyczna biblioteka libteam.

%package -n libteamdctl
Summary:	Teamd daemon control library
Summary(pl.UTF-8):	Biblioteka sterująca demonem teamd
Group:		Libraries
Requires:	zeromq >= 3.2.0
Conflicts:	teamd < 1.26-3

%description -n libteamdctl
Teamd daemon control library.

%description -n libteamdctl -l pl.UTF-8
Biblioteka sterująca demonem teamd.

%package -n libteamdctl-devel
Summary:	Header file for libteamdctl library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libteamdctl
Group:		Development/Libraries
Requires:	libteamdctl = %{version}-%{release}
Requires:	dbus-devel
Requires:	libdaemon-devel
Requires:	systemd-devel
Requires:	zeromq-devel >= 3.2.0

%description -n libteamdctl-devel
Header file for libteamdctl library.

%description -n libteamdctl-devel -l pl.UTF-8
Plik nagłówkowy biblioteki libteamdctl.

%package -n libteamdctl-static
Summary:	Static libteamdctl library
Summary(pl.UTF-8):	Statyczna biblioteka libteamdctl
Group:		Development/Libraries
Requires:	libteamdctl-devel = %{version}-%{release}

%description -n libteamdctl-static
Static libteamdctl library.

%description -n libteamdctl-static -l pl.UTF-8
Statyczna biblioteka libteamdctl.

%package -n teamd
Summary:	Team network device control daemon
Summary(pl.UTF-8):	Demon sterujący grupowymi urządzeniami sieciowymi
Group:		Networking/Admin
Requires:	%{name} = %{version}-%{release}
Requires:	libteamdctl = %{version}-%{release}

%description -n teamd
The teamd package contains team network device control daemon.

%description -n teamd -l pl.UTF-8
Ten pakiet zawiera demona sterującego grupowymi urządzeniami
sieciowymi.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/dbus-1/system.d \
	$RPM_BUILD_ROOT/etc/sysconfig \
	$RPM_BUILD_ROOT/lib/systemd/{system-generators,system}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install teamd/dbus/teamd.conf $RPM_BUILD_ROOT/etc/dbus-1/system.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/teamd
install %{SOURCE2} $RPM_BUILD_ROOT/lib/systemd/system-generators
install %{SOURCE3} $RPM_BUILD_ROOT/lib/systemd/system-generators
install %{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}
install %{SOURCE5} $RPM_BUILD_ROOT%{systemdunitdir}
install %{SOURCE6} $RPM_BUILD_ROOT%{systemdunitdir}
install %{SOURCE7} $RPM_BUILD_ROOT%{systemdunitdir}

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n libteamdctl -p /sbin/ldconfig
%postun	-n libteamdctl -p /sbin/ldconfig

%post -n teamd
export NORESTART="yes"
%systemd_post teamd-lvl1.target teamd-lvl2.target

%preun -n teamd
%systemd_preun teamd-lvl1.target teamd-lvl2.target

%postun -n teamd
%systemd_reload

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/teamnl
%attr(755,root,root) %{_libdir}/libteam.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libteam.so.5
%{_mandir}/man8/teamnl.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libteam.so
%{_includedir}/team.h
%{_pkgconfigdir}/libteam.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libteam.a

%files -n libteamdctl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libteamdctl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libteamdctl.so.0

%files -n libteamdctl-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libteamdctl.so
%{_includedir}/teamdctl.h
%{_pkgconfigdir}/libteamdctl.pc

%files -n libteamdctl-static
%defattr(644,root,root,755)
%{_libdir}/libteamdctl.a

%files -n teamd
%defattr(644,root,root,755)
%doc README teamd/example_configs
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/teamd
/etc/dbus-1/system.d/teamd.conf
%{systemdunitdir}/teamd@.service
%{systemdunitdir}/teamd-lvl?.target
%{systemdunitdir}/teamd-shutdown-workaround.service
%attr(755,root,root) %{_bindir}/bond2team
%attr(755,root,root) %{_bindir}/teamd
%attr(755,root,root) %{_bindir}/teamdctl
%attr(755,root,root) /lib/systemd/system-generators/teamd-lvl?-service-generator
%{_mandir}/man1/bond2team.1*
%{_mandir}/man5/teamd.conf.5*
%{_mandir}/man8/teamd.8*
%{_mandir}/man8/teamdctl.8*
