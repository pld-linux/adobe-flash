#
# TODO: package kde4 component
#
# Conditional build:
%bcond_with	license_agreement	# generates package

%define		ver32	11.2.202.236
%define		ver64	11.2.202.236

%ifarch %{ix86}
%define		version	%{ver32}
%define		libmark	%{nil}
%endif
%ifarch %{x8664}
%define		version	%{ver64}
%define		libmark	()(64bit)
%endif

%define		base_name	adobe-flash
%define		rel 1
Summary:	Flash plugin for Netscape-compatible WWW browsers
Summary(pl.UTF-8):	Wtyczka Flash dla przeglądarek WWW zgodnych z Netscape
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	%{version}
Release:	%{rel}%{?with_license_agreement:wla}
Epoch:		1
License:	Free to use, non-distributable
Group:		X11/Applications/Multimedia
%if %{with license_agreement}
Source0:	http://fpdownload.macromedia.com/get/flashplayer/pdc/%{ver32}/install_flash_player_11_linux.i386.tar.gz
# NoSourceSource0-md5:	9f0e97cae13bae7a490b0505a543b373
NoSource:	0
Source1:	http://fpdownload.macromedia.com/get/flashplayer/pdc/%{ver64}/install_flash_player_11_linux.x86_64.tar.gz
# NoSourceSource1-md5:	d508ebb81be22585bf79df75908247c7
NoSource:	1
%else
Source3:	http://svn.pld-linux.org/svn/license-installer/license-installer.sh
# Source3-md5:	329c25f457fea66ec502b7ef70cb9ede
%endif
Source2:	mms.cfg
URL:		http://www.adobe.com/products/flashplayer/
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

%description -l pl.UTF-8
Adobe(R) Flash(R) Player - środowisko nowej generacji do obsługi
treści i aplikacji we Flashu pod Linuksem.

%prep
%if %{with license_agreement}
%ifarch %{x8664}
%setup -q -T -c -b 1
%else
%setup -q -T -c -b 0
%endif
%patch0 -p1

%build
s=$(echo 'LNX %{version}' | tr . ,)
v=$(strings libflashplayer.so | grep '^LNX ')
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
' %{SOURCE3} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

cp -p %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_browserpluginsdir},%{_bindir},%{_desktopdir},%{_iconsdir}}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/mms.cfg
install -p *.so $RPM_BUILD_ROOT%{_browserpluginsdir}
install usr/bin/flash-player-properties $RPM_BUILD_ROOT%{_bindir}
install usr/share/applications/flash-player-properties.desktop $RPM_BUILD_ROOT%{_desktopdir}/flash-player-properties.desktop
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
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mms.cfg
%attr(755,root,root) %{_bindir}/flash-player-properties
%attr(755,root,root) %{_browserpluginsdir}/*.so
%{_desktopdir}/flash-player-properties.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%endif
