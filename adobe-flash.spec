#
# Conditional build:
%bcond_with	license_agreement	# generates package

%define		ver_major	10
%define		ver_minor	0
%define		ver_patch	45
%define		ver_serial	2

%ifarch %{x8664}
%define		libmark		()(64bit)
%else
%define		libmark		%{nil}
%endif

%define		base_name	adobe-flash
%define		rel 2
Summary:	Flash plugin for Netscape-compatible WWW browsers
Summary(pl.UTF-8):	Wtyczka Flash dla przeglądarek WWW zgodnych z Netscape
%if %{with license_agreement}
Name:		%{base_name}
%else
Name:		%{base_name}-installer
%endif
Version:	%{ver_major}.%{ver_minor}.%{ver_patch}.%{ver_serial}
Release:	%{rel}%{?with_license_agreement:wla}
Epoch:		1
License:	Free to use, non-distributable
Group:		X11/Applications/Multimedia
%if %{with license_agreement}
Source0:	http://fpdownload.macromedia.com/get/flashplayer/current/install_flash_player_10_linux.tar.gz
# NoSource0-md5:	dbfc776cd4310250cde078e0bf0472e7
Source1:	http://download.macromedia.com/pub/labs/flashplayer10/libflashplayer-%{version}.linux-x86_64.so.tar.gz
# NoSource1-md5:	4a4561e456612a6751653b58342d53df
%else
Source2:	http://svn.pld-linux.org/svn/license-installer/license-installer.sh
# Source2-md5:	329c25f457fea66ec502b7ef70cb9ede
%endif
URL:		http://www.adobe.com/products/flashplayer/
%if %{with license_agreement}
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	sed >= 4.0
Requires:	browser-plugins >= 2.0
# dlopened by player
Requires:	libasound.so.2%{libmark}
Requires:	libcurl.so.4%{libmark}
%else
Requires:	rpm-build-macros >= 1.544
Requires:	rpm-build-tools >= 4.4.37
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
s='LNX %{ver_major},%{ver_minor},%{ver_patch},%{ver_serial}'
v=$(strings libflashplayer.so | grep "$s")
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
' %{SOURCE2} > $RPM_BUILD_ROOT%{_bindir}/%{base_name}.install

install %{_specdir}/%{base_name}.spec $RPM_BUILD_ROOT%{_datadir}/%{base_name}

%else

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_browserpluginsdir}}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/mms.cfg
# http://www.adobe.com/cfusion/knowledgebase/index.cfm?id=16701594
# http://www.adobe.com/devnet/flashplayer/articles/flash_player_admin_guide.html
AutoUpdateDisable=1
AutoUpdateInterval=0
# OverrideGPUValidation=true
EOF
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
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mms.cfg
%attr(755,root,root) %{_browserpluginsdir}/*.so
%endif
