#
# Conditional build:
%bcond_with	license_agreement	# generates package
#
Summary:	Flash plugin for Netscape-compatible WWW browsers
Summary(pl):	Wtyczka Flash dla przegl±darek WWW zgodnych z Netscape
%define		base_name	macromedia-flash
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	7.0r25
Release:	2.22%{?with_license_agreement:wla}
License:	Free to use, non-distributable
Group:		X11/Applications/Multimedia
%if %{with license_agreement}
Source0:	http://fpdownload.macromedia.com/get/shockwave/flash/english/linux/%{version}/install_flash_player_7_linux.tar.gz
# NoSource0-md5:	79c59a5ea29347e01c8e6575dd054cd1
%else
Source0:	license-installer.sh
%endif
URL:		http://www.macromedia.com/software/flash/
BuildRequires:	rpmbuild(macros) >= 1.224
Requires:	browser-plugins
%if %{without license_agreement}
Requires:	/usr/bin/builder
%endif
Obsoletes:	flash-plugin
Obsoletes:	mozilla-plugin-macromedia-flash
Obsoletes:	mozilla-firefox-plugin-macromedia-flash
Obsoletes:	konqueror-plugin-macromedia-flash
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/browser-plugins

# TODO: galeon and skipstone.
# use macro, otherwise extra LF inserted along with the ifarch
%define	browsers mozilla, mozilla-firefox, konqueror, opera

%description
Flash plugin for Netscape-compatible WWW browsers.

Supported browsers: %{browsers}.

%description -l pl
Wtyczka Flash dla przegl±darek WWW zgodnych z Netscape.

Supported browsers: %{browsers}.

%prep
%if %{with license_agreement}
%setup -q -n install_flash_player_7_linux
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
' %{SOURCE0} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else

install -d $RPM_BUILD_ROOT%{_plugindir}
install *.{so,xpt} $RPM_BUILD_ROOT%{_plugindir}

%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{without license_agreement}
%pre
%{_bindir}/%{base_name}.install

%else

%triggerin -- mozilla-firefox
%nsplugin_install -d %{_libdir}/mozilla-firefox/plugins libflashplayer.so flashplayer.xpt

%triggerun -- mozilla-firefox
%nsplugin_uninstall -d %{_libdir}/mozilla-firefox/plugins libflashplayer.so flashplayer.xpt

%triggerin -- mozilla
%nsplugin_install -d %{_libdir}/mozilla/plugins libflashplayer.so flashplayer.xpt
umask 022
rm -f /usr/%{_lib}/mozilla/components/{compreg,xpti}.dat
if [ -x /usr/bin/regxpcom ]; then
	MOZILLA_FIVE_HOME=/usr/%{_lib}/mozilla /usr/bin/regxpcom
fi

%triggerun -- mozilla
%nsplugin_uninstall -d %{_libdir}/mozilla/plugins libflashplayer.so flashplayer.xpt
umask 022
rm -f /usr/%{_lib}/mozilla/components/{compreg,xpti}.dat
if [ -x /usr/bin/regxpcom ]; then
	MOZILLA_FIVE_HOME=/usr/%{_lib}/mozilla /usr/bin/regxpcom
fi

%triggerin -- konqueror
%nsplugin_install -d %{_libdir}/kde3/plugins/konqueror libflashplayer.so

%triggerun -- konqueror
%nsplugin_uninstall -d %{_libdir}/kde3/plugins/konqueror libflashplayer.so

%triggerin -- opera
%nsplugin_install -d %{_libdir}/opera/plugins libflashplayer.so

%triggerun -- opera
%nsplugin_uninstall -d %{_libdir}/opera/plugins libflashplayer.so

%endif

%files
%defattr(644,root,root,755)

%if %{without license_agreement}
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}

%else
%attr(755,root,root) %{_plugindir}/*.so
%{_plugindir}/*.xpt
%endif
