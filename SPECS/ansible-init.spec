%define ansible_runuser	root
%define ansible_home	%(getent passwd %{ansible_runuser} | cut -d: -f6)

Name:		ansible-init      
Version:	0.3
Release:	1%{?dist}
Summary:	A custom Ansible init script
Group:		System Environment/Daemons
License:	BSD
URL:		https://github.com/linuxhq/rpmbuild-%{name}
Source0:	ansible.init
Source1:	ansible.ssh_config
Source2:	ansible.sysconfig
BuildArch:	noarch
BuildRequires:	openssh
Requires:	ansible, coreutils, git
Requires(post):	chkconfig

%description
A custom Ansible init script

%prep
%build
%install
%{__install} -d -m 0700 %{buildroot}%{ansible_home}/.ssh \
                        %{buildroot}%{_sysconfdir}/pki/ansible/private
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/pki/ansible/public \
                        %{buildroot}%{_sysconfdir}/rc.d/init.d \
                        %{buildroot}%{_sysconfdir}/sysconfig

%{__install} -m 0755 %{SOURCE0} \
                     %{buildroot}%{_sysconfdir}/rc.d/init.d/ansible
%{__install} -m 0600 %{SOURCE1} \
                     %{buildroot}%{ansible_home}/.ssh/config
%{__install} -m 0600 %{SOURCE2} \
                     %{buildroot}%{_sysconfdir}/sysconfig/ansible

ssh-keygen -b 4096 \
           -C ansible@localhost \
           -f %{buildroot}%{_sysconfdir}/pki/ansible/private/ansible.pem \
           -N '' \
           -t rsa

%{__mv} -f %{buildroot}%{_sysconfdir}/pki/ansible/private/ansible.pem.pub \
           %{buildroot}%{_sysconfdir}/pki/ansible/public/ansible.pub

%post
/sbin/chkconfig --add ansible

%preun
/sbin/service ansible stop >/dev/null 2>&1
/sbin/chkconfig --del ansible

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{ansible_home}/.ssh/config
%{_sysconfdir}/pki/ansible
%{_sysconfdir}/rc.d/init.d/ansible
%config(noreplace) %{_sysconfdir}/sysconfig/ansible

%changelog
* Fri Jun 17 2016 Taylor Kimball <tkimball@linuxhq.org> - 0.3-1
- Add ssh_config to ansbile_runuser account.

* Thu Jun 16 2016 Taylor Kimball <tkimball@linuxhq.org> - 0.2-1
- Generate private ssh key for automated git clones.

* Fri Apr 29 2016 Taylor Kimball <tkimball@linuxhq.org> - 0.1-1
- Initial build.
