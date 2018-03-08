# RPM spec file for mssql-cli
# Definition of macros used - https://fedoraproject.org/wiki/Packaging:RPMMacros?rd=Packaging/RPMMacros

# .el7.centos -> .el7
%if 0%{?rhel} == 7
  %define dist .el7
%endif

%define name           mssql-cli
%define release        1%{?dist}
%define version        0.10.0
%define repo_path      %{getenv:REPO_PATH}
%define cli_lib_dir    %{_libdir}/mssql-cli

Summary:        Microsoft SQL Server CLI
License:        BSD-3
Name:           %{name}
Version:        %{version}
Release:        %{release}
Url:            https://github.com/dbcli/mssql-cli/blob/master/doc/installation_guide.md
BuildArch:      x86_64
Requires:       python

BuildRequires:  gcc
BuildRequires:  python
BuildRequires:  libffi-devel
BuildRequires:  python-devel
BuildRequires:  openssl-devel

%description
    We’re excited to introduce mssql-cli, a new and interactive command line query tool for SQL Server.
    This open source tool works cross-platform and proud to be a part of the dbcli.org community.

%install
cd ${repo_path}
python3 build.py freeze
cp -a build/./* {buildroot}%{cli_lib_dir}
cd -

# Create executable
mkdir -p %{buildroot}%{_bindir}
printf "if [ -z ${PYTHONIOENCODING+x} ]; then export PYTHONIOENCODING=utf8; fi" > %{buildroot}%{_bindir}/mssql-cli
printf '#!/usr/bin/env bash\n%{cli_lib_dir}/main "$@"' > %{buildroot}%{_bindir}/mssql-cli

%files
%attr(-,root,root) %{cli_lib_dir}
%attr(0755,root,root) %{_bindir}/mssql-cli
