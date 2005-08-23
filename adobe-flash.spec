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
Release:	2%{?with_license_agreement:wla}.1
License:	Free to use, non-distributable
Group:		X11/Applications/Multimedia
%if %{with license_agreement}
Source0:	http://fpdownload.macromedia.com/get/shockwave/flash/english/linux/%{version}/install_flash_player_7_linux.tar.gz
# NoSource0-md5:	79c59a5ea29347e01c8e6575dd054cd1
%endif
URL:		http://www.macromedia.com/software/flash/
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Flash plugin for Netscape-compatible WWW browsers.

%description -l pl
Wtyczka Flash dla przegl±darek WWW zgodnych z Netscape.

%package -n mozilla-plugin-macromedia-flash
Summary:	Flash plugin for Mozilla based browsers
Summary(pl):	Wtyczka Flash dla przegl±darek opartych na Mozilli
Group:		X11/Applications/Multimedia
PreReq:		mozilla-embedded >= 1.0
Obsoletes:	flash-plugin

%description -n mozilla-plugin-macromedia-flash
This package contains flash plugin for Mozilla based browsers, i.e.
mozilla itself, galeon or skipstone.

%description -n mozilla-plugin-macromedia-flash -l pl
Pakiet zawiera wtyczkê dla technologii Flash dla przegl±darek opartych
na Mozilli, np.: mozilli jako takiej, galeona czy te¿ skipstone'a.

%package -n mozilla-firefox-plugin-macromedia-flash
Summary:	Flash plugin for Mozilla Firefox browser
Summary(pl):	Wtyczka Flash dla Mozilla Firefox
Group:		X11/Applications/Multimedia
PreReq:		mozilla-firefox
Obsoletes:	flash-plugin

%description -n mozilla-firefox-plugin-macromedia-flash
This package contains flash plugin for Mozilla Firefox browser.

%description -n mozilla-firefox-plugin-macromedia-flash -l pl
Pakiet zawiera wtyczkê dla technologii Flash dla przegl±darki
Mozilla Firefox.

%package -n konqueror-plugin-macromedia-flash
Summary:	Flash plugin for Konqueror browser
Summary(pl):	Wtyczka obs³uguj±ca Flash dla przegl±darki Konqueror
Group:		X11/Applications/Multimedia
PreReq:		konqueror >= 3.0.8-2.3
Obsoletes:	flash-plugin

%description -n konqueror-plugin-macromedia-flash
This package contains flash plugin for Konqueror browser.

%description -n konqueror-plugin-macromedia-flash -l pl
Pakiet zawiera wtyczkê obs³uguj±c± technologiê Flash dla przegl±darki
Konqueror.

%prep
%if %{with license_agreement}
%setup -q -n install_flash_player_7_linux
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if ! %{with license_agreement}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{base_name}}

cat <<'EOF' >$RPM_BUILD_ROOT%{_bindir}/%{base_name}.install
#!/bin/sh
if [ "$1" = "--with" -a "$2" = "license_agreement" ]; then
	TMPDIR=`rpm --eval "%%{tmpdir}"`; export TMPDIR
	SPECDIR=`rpm --eval "%%{_specdir}"`; export SPECDIR
	SRPMDIR=`rpm --eval "%%{_srcrpmdir}"`; export SRPMDIR
	SOURCEDIR=`rpm --eval "%%{_sourcedir}"`; export SOURCEDIR
	BUILDDIR=`rpm --eval "%%{_builddir}"`; export BUILDDIR
	RPMDIR=`rpm --eval "%%{_rpmdir}"`; export RPMDIR
	BACKUP=0
	mkdir -p $TMPDIR $SPECDIR $SRPMDIR $RPMDIR $SRPMDIR $SOURCEDIR $BUILDDIR
	if [ -f $SPECDIR/%{base_name}.spec ]; then
		BACKUP=1
		mv -f $SPECDIR/%{base_name}.spec $SPECDIR/%{base_name}.spec.prev
	fi
	if echo "$3" | grep '\.src\.rpm$' >/dev/null; then
		( cd $SRPMDIR
		if echo "$3" | grep '://' >/dev/null; then
			wget --passive-ftp -t0 "$3"
		else
			cp -f "$3" .
		fi
		rpm2cpio `basename "$3"` | ( cd $TMPDIR; cpio -i %{base_name}.spec )
		)
		cp -i $TMPDIR/%{base_name}.spec $SPECDIR/%{base_name}.spec || exit 1
	else
		cp -i "$3" $SPECDIR || exit 1
	fi
	( cd $SPECDIR
	%{_bindir}/builder -nc -ncs --with license_agreement --opts --target=%{_target_cpu} %{base_name}.spec
	if [ "$?" -ne 0 ]; then
		exit 2
	fi
	RPMNAME1=mozilla-plugin-macromedia-flash-%{version}-%{release}wla.%{_target_cpu}.rpm
	RPMNAME2=mozilla-firefox-plugin-macromedia-flash-%{version}-%{release}wla.%{_target_cpu}.rpm
	RPMNAME3=konqueror-plugin-macromedia-flash-%{version}-%{release}wla.%{_target_cpu}.rpm
	RPMNAMES=
	if rpm -q --whatprovides mozilla-embedded >/dev/null 2>&1; then
		RPMNAMES=$RPMDIR/$RPMNAME1
		echo "Installing $RPMNAME1"
	else
		echo "Not installing $RPMNAME1"
	fi
	if rpm -q mozilla-firefox >/dev/null 2>&1; then
		RPMNAMES="$RPMNAMES $RPMDIR/$RPMNAME2"
		echo "Installing $RPMNAME2"
	else
		echo "Not installing $RPMNAME2"
	fi
	if rpm -q konqueror >/dev/null 2>&1; then
		RPMNAMES="$RPMNAMES $RPMDIR/$RPMNAME3"
		echo "Installing $RPMNAME3"
	else
		echo "Not installing $RPMNAME3"
	fi
	rpm -U $RPMNAMES || echo -e "Install manually the file(s):\n   $RPMNAMES" )
	if [ "$BACKUP" -eq 1 ]; then
		if [ -f $SPECDIR/%{base_name}.spec.prev ]; then
			mv -f $SPECDIR/%{base_name}.spec.prev $SPECDIR/%{base_name}.spec
		fi
	fi
else
	echo "
License issues made us not to include inherent files into
this package by default. If you want to create full working
package please build it with the following command:

$0 --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
fi
EOF

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else

install -d $RPM_BUILD_ROOT%{_libdir}/{mozilla/plugins,/mozilla-firefox/plugins,/kde3/plugins/konqueror}

install *.{so,xpt} $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins
install *.{so,xpt} $RPM_BUILD_ROOT%{_libdir}/mozilla-firefox/plugins
install *.so $RPM_BUILD_ROOT%{_libdir}/kde3/plugins/konqueror

%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if ! %{with license_agreement}
%pre
echo "
License issues made us not to include inherent files into
this package by default. If you want to create full working
package please build it with the following command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
%endif

%post -n mozilla-plugin-macromedia-flash
umask 022
rm -f /usr/%{_lib}/mozilla/components/{compreg,xpti}.dat
if [ -x /usr/bin/regxpcom ]; then
	MOZILLA_FIVE_HOME=/usr/%{_lib}/mozilla /usr/bin/regxpcom
fi

%postun -n mozilla-plugin-macromedia-flash
umask 022
rm -f /usr/%{_lib}/mozilla/components/{compreg,xpti}.dat
if [ -x /usr/bin/regxpcom ]; then
	MOZILLA_FIVE_HOME=/usr/%{_lib}/mozilla /usr/bin/regxpcom
fi

%if ! %{with license_agreement}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{base_name}.install
%{_datadir}/%{base_name}

%else
%files -n mozilla-plugin-macromedia-flash
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mozilla/plugins/*.so
%{_libdir}/mozilla/plugins/*.xpt

%files -n mozilla-firefox-plugin-macromedia-flash
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mozilla-firefox/plugins/*.so
%{_libdir}/mozilla-firefox/plugins/*.xpt

%files -n konqueror-plugin-macromedia-flash
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kde3/plugins/konqueror/*.so
%endif
