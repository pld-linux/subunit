#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_with	python		# python modules/tools [more recent version in python-subunit.spec]
#
%include	/usr/lib/rpm/macros.perl
Summary:	subunit - a streaming protocol for test results
Summary(pl.UTF-8):	subunit - protokół strumieniowy do wyników testów
Name:		subunit
Version:	1.1.0
Release:	5
License:	Apache v2.0 or BSD
Group:		Development/Tools
Source0:	https://github.com/testing-cabal/subunit/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c1d0cf2363a0fcae3714de7ae83923e7
Patch0:		%{name}-link.patch
URL:		https://code.launchpad.net/subunit
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	check-devel >= 0.9.4
BuildRequires:	cppunit-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
Requires:	%{name}-perl = %{version}-%{release}
# subpackage or more recent package built from python-subunit.spec
Requires:	subunit-python >= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Subunit is a streaming protocol for test results.

%description -l pl.UTF-8
Subunit to protokół strumieniowy do wyników testów.

%package perl
Summary:	Perl tools for Subunit streaming protocol for test results
Summary(pl.UTF-8):	Perlowe narzędzia dla protokołu strumieniowego do wyników testów Subunit
Group:		Development/Tools
Requires:	perl-Subunit = %{version}-%{release}

%description perl
Perl tools for Subunit streaming protocol for test results.

%description perl -l pl.UTF-8
Perlowe narzędzia dla protokołu strumieniowego do wyników testów
Subunit.

%package python
Summary:	Python tools for Subunit streaming protocol for test results
Summary(pl.UTF-8):	Pythonowe narzędzia dla protokołu strumieniowego do wyników testów Subunit
Group:		Development/Tools
Requires:	python-subunit = %{version}-%{release}

%description python
Python tools for Subunit streaming protocol for test results.

%description python -l pl.UTF-8
Pythonowe narzędzia dla protokołu strumieniowego do wyników testów
Subunit.

%package libs
Summary:	Subunit shared library
Summary(pl.UTF-8):	Biblioteka współdzielona Subunit
Group:		Libraries

%description libs
Subunit shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona Subunit.

%package devel
Summary:	Development files for Subunit library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Subunit
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for Subunit library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki Subunit.

%package static
Summary:	Static Subunit library
Summary(pl.UTF-8):	Statyczna biblioteka Subunit
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Subunit library.

%description static -l pl.UTF-8
Statyczna biblioteka Subunit.

%package -n cppunit-subunit
Summary:	SubunitTestProgressListener for CPPUnit - shared library
Summary(pl.UTF-8):	SubunitTestProgressListener dla biblioteki CPPUnit - biblioteka współdzielona
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n cppunit-subunit
SubunitTestProgressListener for CPPUnit - shared library.

%description -n cppunit-subunit -l pl.UTF-8
SubunitTestProgressListener dla biblioteki CPPUnit - biblioteka
współdzielona.

%package -n cppunit-subunit-devel
Summary:	SubunitTestProgressListener for CPPUnit - development files
Summary(pl.UTF-8):	SubunitTestProgressListener dla biblioteki CPPUnit - pliki programistyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	cppunit-devel
Requires:	cppunit-subunit = %{version}-%{release}
Requires:	libstdc++-devel

%description -n cppunit-subunit-devel
SubunitTestProgressListener for CPPUnit - development files.

%description -n cppunit-subunit-devel -l pl.UTF-8
SubunitTestProgressListener dla biblioteki CPPUnit - pliki
programistyczne.

%package -n cppunit-subunit-static
Summary:	SubunitTestProgressListener for CPPUnit - static library
Summary(pl.UTF-8):	SubunitTestProgressListener dla biblioteki CPPUnit - biblioteka statyczna
Group:		Development/Libraries
Requires:	cppunit-subunit-devel = %{version}-%{release}

%description -n cppunit-subunit-static
SubunitTestProgressListener for CPPUnit - static library.

%description -n cppunit-subunit-static -l pl.UTF-8
SubunitTestProgressListener dla biblioteki CPPUnit - biblioteka
statyczna.

%package -n perl-Subunit
Summary:	Subunit support for Perl language
Summary(pl.UTF-8):	Obsługa protokołu Subunit dla języka Perl
Group:		Development/Languages/Perl

%description -n perl-Subunit
Subunit support for Perl language.

%description -n perl-Subunit -l pl.UTF-8
Obsługa protokołu Subunit dla języka Perl.

%package -n python-subunit
Summary:	Subunit support for Python language
Summary(pl.UTF-8):	Obsługa protokołu Subunit dla języka Python
Group:		Development/Languages/Python

%description -n python-subunit
Subunit support for Python language.

%description -n python-subunit -l pl.UTF-8
Obsługa protokołu Subunit dla języka Python.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env python,/usr/bin/python,' filters/*subunit*

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make} \
	INSTALLDIRS=vendor

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%if %{with python}
%py_postclean
%else
# python tools
%{__rm} $RPM_BUILD_ROOT%{_bindir}/subunit-{1to2,2to1,filter,ls,notify,output,stats,tags}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/subunit2{csv,gtk,junitxml,pyunit}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/tap2subunit
# python modules
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/subunit
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n cppunit-subunit -p /sbin/ldconfig
%postun	-n cppunit-subunit -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc BSD COPYING NEWS README

%files perl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/subunit-diff

%if %{with python}
%files python
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/subunit-1to2
%attr(755,root,root) %{_bindir}/subunit-2to1
%attr(755,root,root) %{_bindir}/subunit-filter
%attr(755,root,root) %{_bindir}/subunit-ls
%attr(755,root,root) %{_bindir}/subunit-notify
%attr(755,root,root) %{_bindir}/subunit-output
%attr(755,root,root) %{_bindir}/subunit-stats
%attr(755,root,root) %{_bindir}/subunit-tags
%attr(755,root,root) %{_bindir}/subunit2csv
%attr(755,root,root) %{_bindir}/subunit2gtk
%attr(755,root,root) %{_bindir}/subunit2junitxml
%attr(755,root,root) %{_bindir}/subunit2pyunit
%attr(755,root,root) %{_bindir}/tap2subunit
%endif

%files libs
%defattr(644,root,root,755)
%doc c/README
%attr(755,root,root) %{_libdir}/libsubunit.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsubunit.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsubunit.so
%dir %{_includedir}/subunit
%{_includedir}/subunit/child.h
%{_pkgconfigdir}/libsubunit.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsubunit.a
%endif

%files -n cppunit-subunit
%defattr(644,root,root,755)
%doc c++/README
%attr(755,root,root) %{_libdir}/libcppunit_subunit.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcppunit_subunit.so.0

%files -n cppunit-subunit-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcppunit_subunit.so
%{_includedir}/subunit/SubunitTestProgressListener.h
%{_pkgconfigdir}/libcppunit_subunit.pc

%if %{with static_libs}
%files -n cppunit-subunit-static
%defattr(644,root,root,755)
%{_libdir}/libcppunit_subunit.a
%endif

%files -n perl-Subunit
%defattr(644,root,root,755)
%{perl_vendorlib}/Subunit.pm
%{perl_vendorlib}/Subunit

%if %{with python}
%files -n python-subunit
%defattr(644,root,root,755)
%{py_sitescriptdir}/subunit
%endif
