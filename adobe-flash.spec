#
# Conditional build:
%bcond_with	license_agreement	# generates package

%define		ver32	11.0.1.60
%define		ver64	11.0.1.60

%ifarch %{ix86}
%define		version	%{ver32}
%define		libmark	%{nil}
%endif
%ifarch %{x8664}
%define		version	%{ver64}
%define		libmark	()(64bit)
%endif

%define		base_name	adobe-flash
%define		rel 0.1
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
#Source0:	http://download.macromedia.com/pub/labs/flashplatformruntimes/flashplayer10-3/flashplayer10-3_rc1_lin_042011.tar.gz
Source0:	http://download.macromedia.com/pub/labs/flashplatformruntimes/flashplayer11/flashplayer11_b1_install_lin_32_071311.tar.gz#/%{base_name}-%{ver32}.tgz
# NoSource0-md5:	8816dfa0bbb4210df5a37e061834c24a
NoSource:	0
##Source1:	http://download.macromedia.com/pub/labs/flashplayer10/libflashplayer-%{version}.linux-x86_64.so.tar.gz
Source1:	http://download.macromedia.com/pub/labs/flashplatformruntimes/flashplayer11/flashplayer11_b1_install_lin_64_071311.tar.gz#/%{base_name}64-%{ver64}.tgz
# NoSource1-md5:	806b348cfb27054568d9f63d13bee3fd
NoSource:	1
Source2:	mms.cfg
%else
Source3:	http://svn.pld-linux.org/svn/license-installer/license-installer.sh
# Source3-md5:	329c25f457fea66ec502b7ef70cb9ede
%endif
Source4:	memcpy-to-memmove.sh
URL:		http://www.adobe.com/products/flashplayer/
%if %{with license_agreement}
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	sed >= 4.0
Requires:	browser-plugins >= 2.0
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

%build
s=$(echo 'LNX %{version}' | tr . ,)
v=$(strings libflashplayer.so | grep '^LNX ')
if [ "$v" != "$s" ]; then
	: wrong version
	exit 1
fi

%ifarch %{x8664}
# Bug #354073: Patch binary to use memmove instead of memcpy from
# Redhat's bug https://bugzilla.redhat.com/show_bug.cgi?id=638477#c94
cp libflashplayer.so libflashplayer.so.orig
/bin/bash %{SOURCE4} libflashplayer.so \
|| (echo "memcpy-to-memmove.sh failed" && exit 1)
%endif
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

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_browserpluginsdir}}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/mms.cfg
install -p *.so $RPM_BUILD_ROOT%{_browserpluginsdir}
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
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mms.cfg
%attr(755,root,root) %{_browserpluginsdir}/*.so
%endif
