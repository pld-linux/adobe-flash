#
# Conditional build:
# _with_ra			- build in RA environment
#
Summary:	Flash plugin for Netscape-compatible WWW browsers
Summary(pl):	Wtyczka Flash dla przegl±darek WWW zgodnych z Netscape
Name:		macromedia-flash
Version:	6.0r79
Release:	2
License:	Free to use, non-distributable
Group:		X11/Applications/Multimedia
Source0:	http://download.macromedia.com/pub/shockwave/flash/english/linux/%{version}/install_flash_player_6_linux.tar.gz
# NoSource0-md5: a6f73da96f89d3dba4fadd4020dd7f38
NoSource:	0
URL:		http://www.macromedia.com/software/flash/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
Flash plugin for Netscape-compatible WWW browsers.

%description -l pl
Wtyczka Flash dla przegl±darek WWW zgodnych z Netscape.

%package -n mozilla-plugin-macromedia-flash
Summary:	Flash plugin for Mozilla based browsers
Summary(pl):	Wtyczka Flash dla przegl±darek opartych na Mozilli
Group:		X11/Applications/Multimedia
PreReq:		mozilla-embedded >= 1.0
Requires:	compat-libstdc++-2.10
Obsoletes:	flash-plugin

%description -n mozilla-plugin-macromedia-flash
This package contains flash plugin for Mozilla based browsers, i.e.
mozilla itself, galeon or skipstone.

%description -n mozilla-plugin-macromedia-flash -l pl
Pakiet zawiera wtyczkê dla technologii Flash dla przegl±darek opartych
na Mozilli, np.: mozilli jako takiej, galeona czy te¿ skipstone'a.

%package -n konqueror-plugin-macromedia-flash
Summary:	Flash plugin for konqueror based browser
Summary(pl):	Wtyczka obs³uguj±ca Flash dla przegl±darek opartych na konquerorze
Group:		X11/Applications/Multimedia
PreReq:		konqueror >= 3.0.8-2.3
Requires:	compat-libstdc++-2.10
Obsoletes:	flash-plugin

%description -n konqueror-plugin-macromedia-flash
This package contains flash plugin for konqueror based browsers, i.e.
konqueror itself or netraider.

%description -n konqueror-plugin-macromedia-flash -l pl
Pakiet zawiera wtyczkê obs³uguj±c± technologiê Flash dla przegl±darek
opartych na konquerorze, czyli konquerora jako takiego oraz
netraidera.

%prep
%setup -q -n install_flash_player_6_linux

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/{mozilla/plugins,/kde3/plugins/konqueror}

install *.{so,xpt} $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins
install *.so $RPM_BUILD_ROOT%{_libdir}/kde3/plugins/konqueror

%clean
rm -rf $RPM_BUILD_ROOT

%post -n mozilla-plugin-macromedia-flash
umask 022
rm -f %{_libdir}/mozilla/components/{compreg,xpti}.dat
MOZILLA_FIVE_HOME=%{_libdir}/mozilla %{_bindir}/regxpcom

%postun -n mozilla-plugin-macromedia-flash
umask 022
rm -f %{_libdir}/mozilla/components/{compreg,xpti}.dat
MOZILLA_FIVE_HOME=%{_libdir}/mozilla %{_bindir}/regxpcom

%files -n mozilla-plugin-macromedia-flash
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mozilla/plugins/*.so
%{_libdir}/mozilla/plugins/*.xpt

%files -n konqueror-plugin-macromedia-flash
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kde3/plugins/konqueror/*.so
