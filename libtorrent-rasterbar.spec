Summary:	A C++ BitTorrent library
Summary(hu.UTF-8):	C++ BitTorrent könyvtár
Summary(pl.UTF-8):	Biblioteka BitTorrenta napisana w C++
Name:		libtorrent-rasterbar
Version:	0.14
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/libtorrent/%{name}-%{version}.tar.gz
# Source0-md5:	d4577ac07cff34b4a8202edc24383b8b
URL:		http://www.rasterbar.com/products/libtorrent/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	sed >= 4.0
BuildRequires:	which
BuildRequires:	util-linux-ng
BuildRequires:	zlib-devel
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
libtorrent-rasterbar jest biblioteką napisaną w C++ która aspiruje do
bycia dobrą alternatywą dla wszystkich innych implementacji
BitTorrenta. Jest to biblioteka a nie pełnoprawny klient, jakkolwiek
pakiet zawiera działającego przykładowego klienta.

Główne cele biblioteki to bycie bardzo efektywną (w rozumieniu
wykorzystania procesora i pamięci) jak również łatwą w użyciu zarówno
dla użytkownika, jak i programisty.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
License:	BSD, zlib/libpng License, Boost Software License
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel
Requires:	openssl-devel

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

Różne pliki źródłowe i nagłówki dostarcozne z tym pakietem są
licencjonowane pod zmienioną licencją BSD, zlib/libpng i Boost Public.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libtorrent-rasterbar library.

%description static -l hu.UTF-8
Statikus libtorrent-rasterbar könyvtár.

%description static -l pl.UTF-8
Statyczna biblioteka libtorrent-rasterbar.

%prep
%setup -q

## Some of the sources and docs are executable, which makes rpmlint against
## the resulting -debuginfo and -devel packages, respectively, quite angry. :]
find src docs -type f | xargs chmod a-x
find -type f -regex '.*\.[hc]pp' | xargs chmod a-x
## The RST files are the sources used to create the final HTML files; and are
## not needed.
rm -f docs/*.rst

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoconf}
%{__automake}
%configure \
	--with-boost-system=boost_system \
	--with-boost-filesystem=boost_filesystem \
	--with-boost-thread=boost_thread \
	--with-boost-regex=boost_regex \
	--with-boost-program-options=boost_program_options \
	--with-{asio,zlib}=system \
	--with-ssl

%{__make} LDFLAGS="-L%{_libdir}64 %{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
## Ensure that we preserve our timestamps properly.
#export CPPROG="%{__cp} -p"
#make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -c -p"
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

## Do the renaming due to the somewhat limited %{_bindir} namespace.
rename client torrent_client $RPM_BUILD_ROOT%{_bindir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING README
%attr(755,root,root) %{_libdir}/libtorrent-rasterbar.so*

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
