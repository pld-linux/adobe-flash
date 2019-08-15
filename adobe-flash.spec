# NOTES:
# - release archives: http://helpx.adobe.com/flash-player/kb/archived-flash-player-versions.html
# TODO: package kde4 component
#
# Conditional build:
%bcond_with	license_agreement	# generates package

%ifarch %{ix86}
%define		libmark	%{nil}
%endif
%ifarch %{x8664}
%define		libmark	()(64bit)
%endif

%define		base_name	adobe-flash
%define		rel 1
Summary:	Flash (NPAPI based) plugin for Netscape-compatible WWW browsers
Summary(pl.UTF-8):	Wtyczka Flash oparta na NPAPI dla przeglądarek WWW zgodnych z Netscape
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	32.0.0.238
Release:	%{rel}%{?with_license_agreement:wla}
Epoch:		1
License:	Free to use, non-distributable
Group:		X11/Applications/Multimedia
%if %{with license_agreement}
Source0:	https://fpdownload.adobe.com/get/flashplayer/pdc/%{version}/flash_player_npapi_linux.i386.tar.gz?/flash-%{version}.i386.tar.gz
# NoSource0-md5:	a8a9afbdf0eb65ba074b8fbe036cc8d7
NoSource:	0
Source1:	https://fpdownload.adobe.com/get/flashplayer/pdc/%{version}/flash_player_npapi_linux.x86_64.tar.gz?/flash-%{version}.x86_64.tar.gz
# NoSource1-md5:	48a8993ee6eaa0e08fde5ccab58d4fa7
NoSource:	1
%else
Source3:	http://svn.pld-linux.org/svn/license-installer/license-installer.sh
# Source3-md5:	39dd73d36280769d0f74d642c7b0c6d3
%endif
Source2:	mms.cfg
#URL:		http://www.adobe.com/products/flashplayer/
URL:		http://labs.adobe.com/downloads/flashplayer.html
Patch0:		desktop.patch
%if %{with license_agreement}
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	sed >= 4.0
Requires:	browser-plugins >= 2.0
Requires:	hicolor-icon-theme
# dlopened by player
Requires:	libasound.so.2%{libmark}
Requires:	libcurl.so.4%{libmark}
%else
Requires:	rpm-build-tools >= 4.4.37
Requires:	rpmbuild(macros) >= 1.544
%endif
Requires:	cpuinfo(sse2)
Provides:	browser(flash)
Provides:	macromedia-flash
Obsoletes:	flash-plugin
Obsoletes:	konqueror-plugin-macromedia-flash
Obsoletes:	macromedia-flash
Obsoletes:	mozilla-firefox-plugin-macromedia-flash
Obsoletes:	mozilla-plugin-macromedia-flash
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/adobe

# So that building package on AC system won't write package name dep that Th system can't understand (libstdc++4)
%define		_noautoreqdep	libstdc++.so.6

# No debuginfo to be stored
%define		_enable_debug_packages	0

%description
Adobe(R) Flash(R) Player for Linux - the next-generation client
runtime for engaging with Flash content and applications on Linux.

This package contains NPAPI based plugin.

%description -l pl.UTF-8
Adobe(R) Flash(R) Player - środowisko nowej generacji do obsługi
treści i aplikacji we Flashu pod Linuksem.

Ten pakiet zawiera wtyczkę opartą na NPAPI.

%prep
%if %{with license_agreement}
%ifarch %{x8664}
%setup -q -T -c -b 1
%else
%setup -q -T -c -b 0
%endif
%patch0 -p1

%build
s=$(echo '%{version}' | tr . ,)
v=$(strings libflashplayer.so | grep -m 1 'LNX ' | sed 's/.*LNX //')
if [ "$v" != "$s" ]; then
	: wrong version
	exit 1
fi
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{without license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
	s,@DATADIR@,%{_datadir}/%{base_name},g
	s,@COPYSOURCES@,mms.cfg desktop.patch,g
' %{SOURCE3} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

cp -p %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{base_name}
cp -p %{PATCH0} $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_browserpluginsdir},%{_bindir},%{_desktopdir},%{_iconsdir}}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/mms.cfg
install -p *.so $RPM_BUILD_ROOT%{_browserpluginsdir}
install -p usr/bin/flash-player-properties $RPM_BUILD_ROOT%{_bindir}
cp -p usr/share/applications/flash-player-properties.desktop $RPM_BUILD_ROOT%{_desktopdir}/flash-player-properties.desktop
cp -a usr/share/icons/* $RPM_BUILD_ROOT%{_iconsdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{without license_agreement}
%post
%{_bindir}/%{base_name}.install
%else
%post
%update_browser_plugins
%update_icon_cache hicolor

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi
%update_icon_cache hicolor
%endif

%files
%defattr(644,root,root,755)
%if %{without license_agreement}
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%else
%doc readme.txt
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mms.cfg
%attr(755,root,root) %{_bindir}/flash-player-properties
%attr(755,root,root) %{_browserpluginsdir}/libflashplayer.so
%{_desktopdir}/flash-player-properties.desktop
%{_iconsdir}/hicolor/*/apps/flash-player-properties.png
%endif
