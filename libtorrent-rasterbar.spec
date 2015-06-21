Summary:	A C++ BitTorrent library
Summary(hu.UTF-8):	C++ BitTorrent könyvtár
Summary(pl.UTF-8):	Biblioteka BitTorrenta napisana w C++
Name:		libtorrent-rasterbar
Version:	1.0.5
Release:	1
Epoch:		1
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libtorrent/%{name}-%{version}.tar.gz
# Source0-md5:	d09521d34092ba430f430572c9e2b3d3
URL:		http://www.rasterbar.com/products/libtorrent/
BuildRequires:	GeoIP-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	boost-devel >= 1.36
BuildRequires:	boost-python-devel >= 1.36
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	python-devel >= 1:2.4
BuildRequires:	python-modules >= 1:2.4
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
BuildRequires:	util-linux
BuildRequires:	which
BuildRequires:	zlib-devel
Obsoletes:	rb_libtorrent
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libtorrent-rasterbar is a C++ library that aims to be a good
alternative to all the other BitTorrent implementations around. It is
a library and not a full featured client, although it comes with a
working example client.

Its main goals are to be very efficient (in terms of CPU and memory
usage) as well as being very easy to use both as a user and developer.

%description -l hu.UTF-8
libtorrent-rasterbar egy C++ könyvtár, amely egy jó alternatívája
kíván lenni az összes többi BitTorrent implementációjának. Ez "csak"
egy könyvtár, és nem egy szolgáltatásgazdag kliens, habár ad egy
működő példa-klienst.

A fő céljai, hogy nagyon hatékony legyen (CPU és memória-használat) és
könnyű legyen használni mind a felhasználóknak, mind a fejlesztőknek.

%description -l pl.UTF-8
libtorrent-rasterbar jest napisaną w C++ biblioteką, która aspiruje do
bycia dobrą alternatywą dla wszystkich innych implementacji
BitTorrenta. Jest to biblioteka a nie pełnoprawny klient, aczkolwiek
pakiet zawiera działającego przykładowego klienta.

Główne cele biblioteki to bycie bardzo efektywną (w rozumieniu
wykorzystania procesora i pamięci) jak również łatwą w użyciu zarówno
dla użytkownika, jak i programisty.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
License:	BSD, zlib/libpng License, Boost Software License
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	boost-devel
Requires:	openssl-devel
Obsoletes:	rb_libtorrent-devel

%description    devel
The libtorrent-rasterbar-devel package contains libraries and header
files for developing applications that use libtorrent-rasterbar.

The various source and header files included in this package are
licensed under the revised BSD, zlib/libpng, and Boost Public
licenses.

%description devel -l hu.UTF-8
A libtorrent-rasterbar-devel csomag tartalmazza a könyvtári és
fejlesztői fájlokat, amellyel libtorrent-rasterbar-t használó
alkalmazásokat fejleszthetsz.

%description devel -l pl.UTF-8
Pakiet libtorrent-rasterbar-devel zawiera biblioteki i nagłówki do
rozwijania aplikacji używających libtorrent-rasterbar.

Różne pliki źródłowe i nagłówki dostarczone z tym pakietem są
licencjonowane pod zmienioną licencją BSD, zlib/libpng i Boost Public
License.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	rb_libtorrent-static

%description static
Static libtorrent-rasterbar library.

%description static -l hu.UTF-8
Statikus libtorrent-rasterbar könyvtár.

%description static -l pl.UTF-8
Statyczna biblioteka libtorrent-rasterbar.

%package -n python-libtorrent-rasterbar
Summary:	Python bindings for libtorrent-rasterbar
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libtorrent-rasterbar
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n python-libtorrent-rasterbar
Python bindings for libtorrent-rasterbar.

%description -n python-libtorrent-rasterbar -l pl.UTF-8
Wiązania Pythona do biblioteki libtorrent-rasterbar.

%prep
%setup -q

## Some of the sources and docs are executable, which makes rpmlint against
## the resulting -debuginfo and -devel packages, respectively, quite angry. :]
find src docs -type f | xargs chmod a-x
find -type f -regex '.*\.[hc]pp' | xargs chmod a-x
## The RST files are the sources used to create the final HTML files; and are
## not needed.
%{__rm} docs/*.rst

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	LIBS="-lpthread -lrt" \
	--disable-silent-rules \
	--enable-python-binding \
	--with-boost-libdir=%{_libdir} \
	--with-boost-system=boost_system \
	--with-boost-filesystem=boost_filesystem \
	--with-boost-thread=boost_thread \
	--with-boost-regex=boost_regex \
	--with-boost-program-options=boost_program_options \
	--with-asio=system \
	--with-zlib=system \
	--with-libgeoip=system \
	--with-ssl

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING README
%attr(755,root,root) %{_libdir}/libtorrent-rasterbar.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtorrent-rasterbar.so.8

%files devel
%defattr(644,root,root,755)
%doc docs/
%attr(755,root,root) %{_libdir}/libtorrent-rasterbar.so
%{_libdir}/libtorrent-rasterbar.la
%{_pkgconfigdir}/libtorrent-rasterbar.pc
%{_includedir}/libtorrent

%files static
%defattr(644,root,root,755)
%{_libdir}/libtorrent-rasterbar.a

%files -n python-libtorrent-rasterbar
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/libtorrent.so
%{py_sitedir}/python_libtorrent-*.egg-info
