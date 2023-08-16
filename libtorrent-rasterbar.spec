# WARNING: qbittorrent 4.1.x uses 1.1.x/1.2.x, not 2.x
#
%define		tagver	%(echo %{version} | tr . _)
Summary:	A C++ BitTorrent library
Summary(hu.UTF-8):	C++ BitTorrent könyvtár
Summary(pl.UTF-8):	Biblioteka BitTorrenta napisana w C++
Name:		libtorrent-rasterbar
Version:	1.2.7
Release:	9
Epoch:		2
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/arvidn/libtorrent/releases
Source0:	https://github.com/arvidn/libtorrent/releases/download/libtorrent_%{tagver}/%{name}-%{version}.tar.gz
# Source0-md5:	0c5e9d3c141704d1801f6da65c4554fe
URL:		http://www.rasterbar.com/products/libtorrent/
BuildRequires:	GeoIP-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	boost-devel >= 1.58
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	boost-python3-devel >= 1.58
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
BuildRequires:	util-linux
BuildRequires:	which
BuildRequires:	zlib-devel
Obsoletes:	rb_libtorrent < 0.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		boost_py3ver %(echo %{py3_ver} | tr -d .)

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
Requires:	boost-devel >= 1.58
Requires:	libstdc++-devel >= 6:4.7
Requires:	openssl-devel
Obsoletes:	rb_libtorrent-devel < 0.13

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
Obsoletes:	rb_libtorrent-static < 0.13

%description static
Static libtorrent-rasterbar library.

%description static -l hu.UTF-8
Statikus libtorrent-rasterbar könyvtár.

%description static -l pl.UTF-8
Statyczna biblioteka libtorrent-rasterbar.

%package -n python3-libtorrent-rasterbar
Summary:	Python 3 bindings for libtorrent-rasterbar
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki libtorrent-rasterbar
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	python-libtorrent-rasterbar < 2:1.2.7-8

%description -n python3-libtorrent-rasterbar
Python 3 bindings for libtorrent-rasterbar.

%description -n python3-libtorrent-rasterbar -l pl.UTF-8
Wiązania Pythona 3 do biblioteki libtorrent-rasterbar.

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
	PYTHON=%{__python3} \
	--disable-silent-rules \
	--enable-python-binding \
	--with-boost-libdir=%{_libdir} \
	--with-boost-system=boost_system \
	--with-boost-python=boost_python%{boost_py3ver}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# fix python bindings install mixup
%{__mv} $RPM_BUILD_ROOT%{py3_sitedir}/python_libtorrent-*.egg/* $RPM_BUILD_ROOT%{py3_sitedir}/
%{__mv} $RPM_BUILD_ROOT%{py3_sitedir}/{EGG-INFO,libtorrent-%{version}-py%{py3_ver}.egg-info}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING
%attr(755,root,root) %{_libdir}/libtorrent-rasterbar.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtorrent-rasterbar.so.10

%files devel
%defattr(644,root,root,755)
%doc docs/
%attr(755,root,root) %{_libdir}/libtorrent-rasterbar.so
%{_libdir}/libtorrent-rasterbar.la
%{_includedir}/libtorrent
%{_pkgconfigdir}/libtorrent-rasterbar.pc
%{_datadir}/cmake/Modules/FindLibtorrentRasterbar.cmake

%files static
%defattr(644,root,root,755)
%{_libdir}/libtorrent-rasterbar.a

%files -n python3-libtorrent-rasterbar
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/libtorrent.*.so
%{py3_sitedir}/libtorrent-*.egg-info
