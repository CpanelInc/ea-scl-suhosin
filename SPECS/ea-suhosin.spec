%define debug_package %{nil}

# Package namespaces
%global ns_name ea
%global ns_dir /opt/cpanel
%global _scl_prefix %ns_dir
%global suhosin_sodir ./

%scl_package %scl

# This makes the ea-php<ver>-build macro stuff work
%scl_package_override

# OBS builds the 32-bit targets as arch 'i586', and more typical
# 32-bit architecture is 'i386', but 32-bit archive is named 'x86'.
# 64-bit archive is 'x86-64', rather than 'x86_64'.
%if "%{_arch}" == "i586" || "%{_arch}" == "i386"
%global archive_arch x86
%else
%if "%{_arch}" == "x86_64"
%global archive_arch x86-64
%else
%global archive_arch %{_arch}
%endif
%endif

Name:    %{?scl_prefix}php-suhosin
Vendor:  cPanel, Inc.
Summary: Protective PHP Hardening Extension
Version: 0.9.38
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 3
Release: %{release_prefix}%{?dist}.cpanel
License: PHP
Group:   Development/Languages
URL: https://suhosin.org/stories/index.html
Source: suhosin-0.9.38.tar.gz
Source1: 300-suhosin.ini

BuildRequires: scl-utils-build
BuildRequires: %{?scl_prefix}scldevel
BuildRequires: %{?scl_prefix}build
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: autoconf, automake, libtool
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Requires:      %{?scl_prefix}php-cli


%description
Suhosin (pronounced 'su-ho-shin') is an advanced protection system for PHP installations. It was designed to protect servers and users from known and unknown flaws in PHP applications and the PHP core. Suhosin comes in two independent parts, that can be used separately or in combination. The first part is a small patch against the PHP core, that implements a few low-level protections against buffer overflows or format string vulnerabilities and the second part is a powerful PHP extension that implements numerous other protections.

%prep
%setup -n suhosin-%{version}

%build
%{_scl_root}/usr/bin/phpize

%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}
install -d -m 755 $RPM_BUILD_ROOT%{php_extdir}
install -d -m 755 $RPM_BUILD_ROOT%{php_inidir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{php_inidir}
install -m 755 modules/suhosin.so $RPM_BUILD_ROOT%{php_extdir}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{php_extdir}/suhosin.so
%config(noreplace) %{php_inidir}/300-suhosin.ini

%changelog
* Tue Feb 18 2020 Tim Mullin <tim@cpanel.net> - 0.9.38-3
- EA-8865: Add php-cli as a dependency

* Thu Mar 30 2017 Cory McIntire <cory@cpanel.net> - 0.9.38-2
- EA-5977: Spiff up for Release - Take out of Experimental

* Mon Mar 13 2017 Jacob Perkins <jacob.perkins@cpanel.net> - 0.9.38-1
- Initial creation
