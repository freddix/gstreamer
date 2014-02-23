%define		gst_major_ver	1.0

Summary:	GStreamer Streaming-media framework runtime
Name:		gstreamer
Version:	1.2.3
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gstreamer/%{name}-%{version}.tar.xz
# Source0-md5:	8155b9c7574ccaa361cc504e8e0e72dc
Patch0:		%{name}-without_ps_pdf.patch
Patch1:		%{name}-eps.patch
Patch2:		%{name}-inspect-rpm-format.patch
URL:		http://gstreamer.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	check-devel
BuildRequires:	flex
BuildRequires:	gettext-autopoint
BuildRequires:	glib-gio-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	nasm
BuildRequires:	perl-base
BuildRequires:	pkg-config
BuildRequires:	popt-devel
BuildRequires:	xmlto
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		gstdatadir	%{_datadir}/gstreamer-%{gst_major_ver}
%define		gstlibdir	%{_libdir}/gstreamer-%{gst_major_ver}
%define		gstincludedir	%{_includedir}/gstreamer-%{gst_major_ver}

%description
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related. Its plugin-based architecture means
that new data types or processing capabilities can be added simply by
installing new plugins.

%package libs
Summary:	GStreamer libraries
Group:		Libraries

%description libs
GStreamer libraries.

%package devel
Summary:	Include files for GStreamer streaming-media framework
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the includes files necessary to develop
applications and plugins for GStreamer.

%package apidocs
Summary:	GStreamer API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GStreamer API documentation.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__autopoint}
patch -p0 < common/gettext.patch
%{__libtoolize}
%{__aclocal} -I common/m4 -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-debug		\
	--disable-examples	\
	--disable-pspdf		\
	--disable-silent-rules	\
	--disable-static	\
	--disable-tests		\
	--enable-docbook	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{gstdatadir}/presets,%{_docdir}/%{name}-devel-%{version}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_docdir}/%{name}-{%{gst_major_ver},%{version}}
mv $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/{manual,pwg} \
	$RPM_BUILD_ROOT%{_docdir}/%{name}-devel-%{version}

%find_lang %{name} --all-name --with-gnome

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{gstlibdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/gst-inspect-%{gst_major_ver}
%attr(755,root,root) %{_bindir}/gst-launch-%{gst_major_ver}
%attr(755,root,root) %{_bindir}/gst-typefind-%{gst_major_ver}
%attr(755,root,root) %{gstlibdir}/gst-plugin-scanner
%attr(755,root,root) %{gstlibdir}/*.so

%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%dir %{gstdatadir}
%dir %{gstdatadir}/presets
%dir %{gstlibdir}
%attr(755,root,root) %ghost %{_libdir}/lib*-%{gst_major_ver}.so.?
%attr(755,root,root) %{_libdir}/lib*-%{gst_major_ver}.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*-%{gst_major_ver}.so
%{_aclocaldir}/gst-element-check-%{gst_major_ver}.m4
%{gstincludedir}
%{_pkgconfigdir}/*-%{gst_major_ver}.pc
%{_datadir}/gir-1.0/*.gir

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/%{name}-devel-%{version}
%{_gtkdocdir}/%{name}-%{gst_major_ver}
%{_gtkdocdir}/%{name}-libs-%{gst_major_ver}
%{_gtkdocdir}/%{name}-plugins-%{gst_major_ver}

