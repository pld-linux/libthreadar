#
# Conditional build:
%bcond_without	apidocs		# doxygen API documentation
%bcond_without	static_libs	# static library
#
Summary:	C++ classes to work with threads
Summary(pl.UTF-8):	Klasy C++ do pracy z wątkami
Name:		libthreadar
Version:	1.0.1
Release:	1
License:	LGPL v3+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libthreadar/%{name}-%{version}.tar.gz
# Source0-md5:	c7b6ebf2966bdf64d4166726eadb372e
URL:		http://libthreadar.sourceforge.net/
%{?with_apidocs:BuildRequires:	doxygen >= 1.3}
BuildRequires:	libstdc++-devel >= 6:4.7
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

%description apidocs
API documentation for libthreadar library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libthreadar.

%prep
%setup -q

%build
%configure \
	%{!?with_apidocs:--disable-build-html} \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libthreadar*.la

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
%attr(755,root,root) %ghost %{_libdir}/libthreadar.so.0

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
%doc doc/html/*
%endif
