Summary:	Cross AMD64 GNU binary utility development utilities - binutils
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - AMD64 binutils
Summary(fr):	Utilitaires de d�veloppement binaire de GNU - AMD64 binutils
Summary(pl):	Skro�ne narz�dzia programistyczne GNU dla AMD64 - binutils
Summary(pt_BR):	Utilit�rios para desenvolvimento de bin�rios da GNU - AMD64 binutils
Summary(tr):	GNU geli�tirme ara�lar� - AMD64 binutils
Name:		crossamd64-binutils
Version:	2.15.91.0.2
Release:	2
License:	GPL
Group:		Development/Tools
Source0:	ftp://ftp.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
# Source0-md5:	41983069bef07af4f1350c6d30666b2d
Patch0:		binutils-pr290.patch
Patch1:		binutils-pr338.patch
URL:		http://sources.redhat.com/binutils/
BuildRequires:	automake
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
ExcludeArch:	amd64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		amd64-pld-linux
%define		arch		%{_prefix}/%{target}

%description
Binutils is a collection of binary utilities, including:
- ar - create, modify and extract from archives,
- nm - lists symbols from object files,
- objcopy - copy and translate object files,
- objdump - display information from object files,
- ranlib - generate an index for the contents of an archive,
- size - list the section sizes of an object or archive file,
- strings - list printable strings from files,
- strip - discard symbols,
- c++filt - a filter for demangling encoded C++ symbols,
- addr2line - convert addresses to file and line,
- nlmconv - convert object code into an NLM.

This package contains the cross version for AMD64.

%description -l pl
Pakiet binutils zawiera zestaw narz�dzi umo�liwiaj�cych kompilacj�
program�w. Znajduj� si� tutaj mi�dzy innymi assembler, konsolidator
(linker), a tak�e inne narz�dzia do manipulowania binarnymi plikami
program�w i bibliotek.

Ten pakiet zawiera wersj� skro�n� generuj�c� kod dla AMD64.

%prep
%setup -q -n binutils-%{version}
%patch0 -p0
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub .

# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
./configure \
	--disable-shared \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--enable-64-bit-bfd \
	--target=%{target}

%{__make} all \
	tooldir=%{_prefix} \
	EXEEXT=""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

# remove these man pages unless we cross-build for win*/netware platforms.
# however, this should be done in Makefiles.
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{*dlltool,*nlmconv,*windres}.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/%{target}-*
%dir %{arch}
%dir %{arch}/bin
%attr(755,root,root) %{arch}/bin/*
%dir %{arch}/lib
%dir %{arch}/lib/*
%{arch}/lib/ldscripts/*
%{_mandir}/man?/%{target}-*
