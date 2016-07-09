# rpmbuild-ansible-init

Create a ansible-init RPM for RHEL/CentOS.

## Requirements

To download package sources and install build dependencies

    yum -y install rpmdevtools yum-utils

## Build process

To build the package follow the steps outlined below

    git clone https://github.com/linuxhq/rpmbuild-ansible-init.git rpmbuild
    spectool -g -R rpmbuild/SPECS/ansible-init.spec
    yum-builddep rpmbuild/SPECS/ansible-init.spec
    rpmbuild -ba rpmbuild/SPECS/ansible-init.spec

## License

BSD

## Author Information

This package was created by [Taylor Kimball](http://www.linuxhq.org).
