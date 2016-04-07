%define name Producs Manager
%define version 0.1
%define unmangled_version 0.1
%define release 1

Summary: Venta de articulos
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Daniel Souto <dsoutofernandez @danielcastelao.org>
Url: http://google.es

%description
UNKNOWN

%prep
%setup -n %{name}-%{unmangled_version}

%build
python Setup.py build

%install
python Setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
