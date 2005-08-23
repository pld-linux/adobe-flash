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
Release:	2.13%{?with_license_agreement:wla}
License:	Free to use, non-distributable
Group:		X11/Applications/Multimedia
%if %{with license_agreement}
Source0:	http://fpdownload.macromedia.com/get/shockwave/flash/english/linux/%{version}/install_flash_player_7_linux.tar.gz
# NoSource0-md5:	79c59a5ea29347e01c8e6575dd054cd1
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

# TODO: opera, galeon and skipstone.
# use macro, otherwise extra LF inserted along with the ifarch
%define	browsers mozilla, mozilla-firefox, konqueror

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
	RPMNAME=%{base_name}-%{version}-%{release}wla.%{_target_cpu}.rpm
	RPMNAMES="$RPMNAMES $RPMDIR/$RPMNAME"
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

install -d $RPM_BUILD_ROOT%{_plugindir}
install *.{so,xpt} $RPM_BUILD_ROOT%{_plugindir}

%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{without license_agreement}
%pre
echo "
License issues made us not to include inherent files into
this package by default. If you want to create full working
package please build it with the following command:

%{base_name}.install --with license_agreement %{_datadir}/%{base_name}/%{base_name}.spec
"
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
