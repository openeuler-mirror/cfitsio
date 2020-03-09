Name:              cfitsio
Version:           3.450
Release:           5
Summary:           Library for manipulating FITS data files
License:           MIT
URL:               http://heasarc.gsfc.nasa.gov/fitsio/
Source0:           https://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio3450.tar.gz

Patch0000:         cfitsio-zlib.patch
Patch0001:         cfitsio-noversioncheck.patch
Patch0002:         cfitsio-pkgconfig.patch
Patch0003:         cfitsio-ldflags.patch

BuildRequires:     gcc-gfortran zlib-devel bzip2-devel
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%description
CFITSIO is a library of C and FORTRAN subroutines for reading and writing data files
in FITS (Flexible Image Transmission System) data format. CFITSIO frees programmers
from the internal complexity of the FITS file format by providing a set of easy-to-use
high-level routines, thereby simplifying the task of writing software that processes
FITS files. At the same time, CFITSIO provides many advanced features, making it the
most widely used FITS file programming interface in the astronomy community.

%package devel
Summary:            Required headers when building programs against cfitsio.
Requires:           %{name} = %{version}-%{release} pkgconfig
Provides:           %{name}-static = %{version}-%{release}
Obsoletes:          %{name}-static < %{version}-%{release}

%description devel
Header files needed when building a program against the cfitsio library.
Static cfitsio library.

%package help
Summary:            Documentation for cfitsio
BuildArch:          noarch
Provides:           %{name}-docs = %{version}-%{release}
Obsoletes:          %{name}-docs < %{version}-%{release}

%description help
Stand-alone documentation for cfitsio.

%package -n fpack
Summary:             FITS image compression and decompression utilities
Requires:            %{name} = %{version}-%{release}

%description -n fpack
fpack can best compress images in FITS format, while funpack can
restore them to their original state.

* Lossless compression of images in integer format using the Rice compression algorithm.
* Compression ratio is usually 30% better than GZIP
* Compression speed is 3 times faster than GZIP
* Decompression speed is the same as GUNZIP

* Floating point images are compressed using a lossy algorithm
* Truncate image pixel noise by a user-specified amount to produce
a higher compression rate than lossless techniques
* The scientific measurement accuracy in the compressed image (relative
to the accuracy in the original image) depends on the amount of compression

%prep
%autosetup  -n cfitsio -p1
cd zlib
rm adler32.c crc32.c deflate.c infback.c inffast.c inflate.c inflate.h inftrees.c inftrees.h zlib.h \
deflate.h trees.c trees.h uncompr.c zconf.h zutil.c zutil.h crc32.h  inffast.h  inffixed.h 
cd -

%build
%configure --enable-reentrant --with-bzip2
make shared
make fpack
make funpack

%check
make testprog
LD_LIBRARY_PATH=. ./testprog > testprog.lis
cmp -s testprog.lis testprog.out
cmp -s testprog.fit testprog.std

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}/%{name}
make LIBDIR=%{_libdir} INCLUDEDIR=%{_includedir}/%{name} CFITSIO_LIB=%{buildroot}%{_libdir} \
 CFITSIO_INCLUDE=%{buildroot}%{_includedir}/%{name} \
install
cp -p f{,un}pack %{buildroot}%{_bindir}

chmod 755 %{buildroot}%{_libdir}/libcfitsio.so.*
chmod 755 %{buildroot}%{_bindir}/f{,un}pack

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README License.txt docs/changes.txt
%{_libdir}/libcfitsio.so.*

%files devel
%doc cookbook.*
%doc License.txt
%{_includedir}/%{name}
%{_libdir}/libcfitsio.so
%{_libdir}/pkgconfig/cfitsio.pc
%{_libdir}/libcfitsio.a

%files help
%doc docs/fitsio.doc docs/fitsio.pdf docs/cfitsio.pdf License.txt

%files -n fpack
%doc docs/fpackguide.pdf License.txt
%{_bindir}/fpack
%{_bindir}/funpack

%changelog
* Mon Mar 09 2020 yangjian<yangjian79@huawei.com> - 3.450-5
- Fix changelog  problem

* Mon Mar 09 2020 yangjian<yangjian79@huawei.com> - 3.450-4
- To fix files problem

* Wed Mar 04 2020 yangjian<yangjian79@huawei.com> - 3.450-3
- Package init
