#
# Conditional build:
%bcond_with	license_agreement	# generates package
#
%define		_ver_major	9
%define		_ver_minor	0
%define		_ver_patch	21
%define		_ver_serial	78
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
#Source0:	http://download.macromedia.com/pub/labs/flashplayer9_update/FP9_plugin_beta_101806.tar.gz
Source0:	http://download.macromedia.com/pub/labs/flashplayer9_update/FP9_plugin_beta_112006.tar.gz
# NoSource0-md5:	3ab408f85ae6d8180cc913edf97bf3eb
%else
Source0:	license-installer.sh
# NoSource0-md5:	3ab408f85ae6d8180cc913edf97bf3eb
%endif
URL:		http://labs.adobe.com/technologies/flashplayer9/
%if %{with license_agreement}
BuildRequires:	rpmbuild(macros) >= 1.357
Requires:	browser-plugins >= 2.0
%else
Requires:	rpm-build-tools
%endif
Obsoletes:	flash-plugin
Obsoletes:	konqueror-plugin-macromedia-flash
Obsoletes:	mozilla-firefox-plugin-macromedia-flash
Obsoletes:	mozilla-plugin-macromedia-flash
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Adobe(R) Flash(R) Player is the high-performance, lightweight, highly expressive
client runtime that delivers powerful and consistent user experiences across
major operating systems, browsers, mobile phones, and devices. Installed on
over 700 million Internet-connected desktops and mobile devices, Flash Player
enables organizations and individuals to build and deliver great digital
experiences to their end users.

%description -l pl
Wtyczka Flash dla przegl±darek WWW zgodnych z Netscape.

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

install -d $RPM_BUILD_ROOT%{_browserpluginsdir}
install *.so $RPM_BUILD_ROOT%{_browserpluginsdir}

%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{without license_agreement}
%post
%{_bindir}/%{base_name}.install
%else
%post
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi
%endif

%files
%defattr(644,root,root,755)
%if %{without license_agreement}
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}
%else
%doc *.txt
%attr(755,root,root) %{_browserpluginsdir}/*.so
%endif
