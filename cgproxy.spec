%bcond_without check

%global forgeurl https://github.com/springzfx/cgproxy/
Version:        0.20

%forgemeta

Name:           cgproxy
Release:        1%{?dist}
Summary:        Transparent Proxy with cgroup v2
License:        GPLv2
URL:            %{forgeurl}

Source0:        %{forgesource}

Patch0:         52.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.14
BuildRequires:  clang
BuildRequires:  json-devel
BuildRequires:  libbpf-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  bpftool
BuildRequires:  git-core


%description
cgproxy will transparent proxy anything running in specific cgroup.
It resembles with proxychains and tsocks in default setting.


%prep
%forgeautosetup -S git


%build
%cmake \
%{?with_check: -Dbuild_test=ON } \
               -Dbuild_execsnoop_dl=ON \
               -Dbuild_static=OFF
%cmake_build


%install
%cmake_install


%if %{with check}
%check
%ctest
%endif


%files
%license LICENSE
%doc readme.md
%{_mandir}/man1/*.1.*

%{_bindir}/cgnoproxy
%{_bindir}/cgproxy
%{_bindir}/cgproxyd

%dir %{_libdir}/cgproxy
%{_libdir}/cgproxy/libexecsnoop.so

%dir %{_datadir}/cgproxy
%dir %{_datadir}/cgproxy/scripts
%{_datadir}/cgproxy/scripts/cgroup-tproxy.sh
%{_datadir}/cgproxy/scripts/iptables.sh
%{_datadir}/cgproxy/scripts/nftables.sh

%dir %{_sysconfdir}/cgproxy
%config(noreplace) %{_sysconfdir}/cgproxy/config.json

%{_unitdir}/cgproxy.service


# scriptlets >>
%post
%systemd_post cgproxy.service

%preun
%systemd_preun cgproxy.service

%postun
%systemd_postun_with_restart cgproxy.service
# << scriptlets


%changelog
* Sun Nov 26 2023 sixg0000d <sixg0000d@gmail.com>
- Initial package
