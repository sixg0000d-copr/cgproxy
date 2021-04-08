%bcond_without check

%global __provides_exclude_from ^(%{_libdir}/%{name}/.*\\.so.*)$
%global forgeurl                https://github.com/springzfx/cgproxy
Version:                        0.19

%forgemeta

Name:            cgproxy
Release:         1%{?dist}
Summary:         Transparent Proxy with cgroup v2
License:         GPLv2
URL:             %{forgeurl}

Source0:         %{forgesource}

# firewalld-edition: https://github.com/sixg0000d/cgproxy/tree/firewalld
Patch0:          0001-update-readme-18.patch
Patch1:          0002-use-CMAKE_INSTALL_FULL_XXX-instead-because-cmake-s-i.patch
Patch2:          0003-test-tools-find-header-files-in-build-dir.patch
Patch3:          0004-update-to-new-path.patch
Patch4:          0005-firewalld-edition.patch

BuildRequires:   cmake >= 3.14
BuildRequires:   gcc
BuildRequires:   gcc-c++
BuildRequires:   make
BuildRequires:   json-devel
BuildRequires:   libbpf-devel
BuildRequires:   systemd-rpm-macros

%{?systemd_requires}
Requires:        firewalld
Requires:        xmlstarlet

%description
cgproxy will transparent proxy anything running in specific cgroup.
It resembles with proxychains and tsocks in default setting.


%prep
%forgeautosetup -p 1


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

%dir %{_sysconfdir}/cgproxy
%config(noreplace) %{_sysconfdir}/cgproxy/config.json

%{_unitdir}/cgproxy.service


# scriptlets >>
%post
if [ $1 -eq 1 ] && [ -e "%{_sysconfdir}/firewalld/firewalld.conf" ]; then
    # Package installation, not upgrade
    sed -e 's/^FirewallBackend=.*$/FirewallBackend=iptables/g' -i %{_sysconfdir}/firewalld/firewalld.conf || :
fi
%systemd_post cgproxy.service

%preun
%systemd_preun cgproxy.service

%postun
%systemd_postun_with_restart cgproxy.service
# << scriptlets


%changelog
* Thu Apr 08 2021 sixg0000d <sixg0000d@gmail.com>
- Initial cgproxy build
