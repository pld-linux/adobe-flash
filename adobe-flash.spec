#
# Conditional build:
%bcond_with	license_agreement	# generates package
#
%define		_ver_major	9
%define		_ver_minor	0
%define		_ver_patch	21
%define		_ver_serial	55
%define		base_name	macromedia-flash
Summary:	Flash plugin for Netscape-compatible WWW browsers
Summary(pl):	Wtyczka Flash dla przegl±darek WWW zgodnych z Netscape
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
%define		_rel 2
Version:	%{_ver_major}.%{_ver_minor}.%{_ver_patch}.%{_ver_serial}
Release:	%{_rel}%{?with_license_agreement:wla}
License:	Free to use, non-distributable
Group:		X11/Applications/Multimedia
%if %{with license_agreement}
Source0:	http://download.macromedia.com/pub/labs/flashplayer9_update/FP9_plugin_beta_101806.tar.gz
# NoSource0-md5:	0b234c5d0eaf254ef8af364fb9ed97f2
%else
Source0:	license-installer.sh
# NoSource0-md5:	0b234c5d0eaf254ef8af364fb9ed97f2
%endif
URL:		http://www.adobe.com/products/flashplayer/
%if %{with license_agreement}
BuildRequires:	rpmbuild(macros) >= 1.236
Requires:	browser-plugins(%{_target_base_arch})
%else
Requires:	rpm-build-tools
%endif
Obsoletes:	flash-plugin
Obsoletes:	konqueror-plugin-macromedia-flash
Obsoletes:	mozilla-firefox-plugin-macromedia-flash
Obsoletes:	mozilla-plugin-macromedia-flash
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/browser-plugins

# TODO: galeon and skipstone.
# use macro, otherwise extra LF inserted along with the ifarch
%define	browsers mozilla, mozilla-firefox, mozilla-firefox-bin, konqueror, opera, seamonkey

%description
Adobe(R) Flash(R) Player is the high-performance, lightweight, highly expressive
client runtime that delivers powerful and consistent user experiences across
major operating systems, browsers, mobile phones, and devices. Installed on
over 700 million Internet-connected desktops and mobile devices, Flash Player
enables organizations and individuals to build and deliver great digital
experiences to their end users.

Supported browsers: %{browsers}.

%description -l pl
Wtyczka Flash dla przegl±darek WWW zgodnych z Netscape.

Obs³ugiwane przegl±darki: %{browsers}.

%prep
%if %{with license_agreement}
%setup -q -n flash-player-plugin-%{_ver_major}.%{_ver_minor}.%{_ver_patch}.%{_ver_serial}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if !%{with license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

sed -e '
	s/@BASE_NAME@/%{base_name}/g
	s/@TARGET_CPU@/%{_target_cpu}/g
	s-@VERSION@-%{version}-g
	s-@RELEASE@-%{release}-g
	s,@SPECFILE@,%{_datadir}/%{base_name}/%{base_name}.spec,g
' %{SOURCE0} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else

install -d $RPM_BUILD_ROOT%{_plugindir}
install *.so $RPM_BUILD_ROOT%{_plugindir}

%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if !%{with license_agreement}
%post
%{_bindir}/%{base_name}.install

%else

%triggerin -- mozilla-firefox
%nsplugin_install -d %{_libdir}/mozilla-firefox/plugins libflashplayer.so

%triggerun -- mozilla-firefox
%nsplugin_uninstall -d %{_libdir}/mozilla-firefox/plugins libflashplayer.so

%triggerin -- mozilla-firefox-bin
%nsplugin_install -d %{_libdir}/mozilla-firefox-bin/plugins libflashplayer.so

%triggerun -- mozilla-firefox-bin
%nsplugin_uninstall -d %{_libdir}/mozilla-firefox-bin/plugins libflashplayer.so

%triggerin -- mozilla
%nsplugin_install -d %{_libdir}/mozilla/plugins libflashplayer.so

%triggerun -- mozilla
%nsplugin_uninstall -d %{_libdir}/mozilla/plugins libflashplayer.so

%triggerin -- konqueror
%nsplugin_install -d %{_libdir}/kde3/plugins/konqueror libflashplayer.so

%triggerun -- konqueror
%nsplugin_uninstall -d %{_libdir}/kde3/plugins/konqueror libflashplayer.so

%triggerin -- opera
%nsplugin_install -d %{_libdir}/opera/plugins libflashplayer.so

%triggerun -- opera
%nsplugin_uninstall -d %{_libdir}/opera/plugins libflashplayer.so

%triggerin -- seamonkey
%nsplugin_install -d %{_libdir}/seamonkey/plugins libflashplayer.so

%triggerun -- seamonkey
%nsplugin_uninstall -d %{_libdir}/seamonkey/plugins libflashplayer.so

# as rpm removes the old obsoleted package files after the triggers
# above are ran, add another trigger to make the links there.
%triggerpostun -- mozilla-firefox-plugin-macromedia-flash
%nsplugin_install -f -d %{_libdir}/mozilla-firefox/plugins libflashplayer.so flashplayer.xpt

%triggerpostun -- mozilla-plugin-macromedia-flash
%nsplugin_install -f -d %{_libdir}/mozilla/plugins libflashplayer.so flashplayer.xpt

%triggerpostun -- konqueror-plugin-macromedia-flash
%nsplugin_install -f -d %{_libdir}/kde3/plugins/konqueror libflashplayer.so
%endif

%files
%defattr(644,root,root,755)

%if !%{with license_agreement}
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}

%else
%doc *.txt
%attr(755,root,root) %{_plugindir}/*.so
%endif
