#
# Conditional build:
%bcond_without	apidocs		# doxygen API documentation
%bcond_without	static_libs	# static library
#
Summary:	C++ classes to work with threads
Summary(pl.UTF-8):	Klasy C++ do pracy z wątkami
Name:		libthreadar
Version:	1.4.0
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	https://downloads.sourceforge.net/libthreadar/%{name}-%{version}.tar.gz
# Source0-md5:	88c53a1981d91c22e56e122c609e1c11
URL:		https://libthreadar.sourceforge.net/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	libtool >= 2:1.5
%{?with_apidocs:BuildRequires:	doxygen >= 1.3}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpm-build >= 4.6
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libthreadar provides C++ classes for manipulating threads and
propagating back exception from thread to parent thread when the
parent calls the join() method.

%description -l pl.UTF-8
Biblioteka libthreadar dostarcza klasy C++ do operowania na wątkach i
propagowania wyjątków z wątku do wątku rodzica, kiedy rodzic wywołuje
metodę join().

%package devel
Summary:	Header files for libthreadar library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libthreadar
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7

%description devel
Header files for libthreadar library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libthreadar.

%package static
Summary:	Static libthreadar library
Summary(pl.UTF-8):	Statyczna biblioteka libthreadar
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libthreadar library.

%description static -l pl.UTF-8
Statyczna biblioteka libthreadar.

%package apidocs
Summary:	API documentation for libthreadar library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libthreadar
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libthreadar library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libthreadar.

%prep
%setup -q

# don't use static linking
%{__sed} -i -e '/ = -all-static$/d' doc/examples/Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-build-html} \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libthreadar.la

# packaged as %doc in -apidocs
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/libthreadar/{README,html}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libthreadar.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libthreadar.so.1000

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libthreadar.so
%{_includedir}/libthreadar
%{_pkgconfigdir}/libthreadar.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libthreadar.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/{search,*.css,*.html,*.js,*.png}
%endif
