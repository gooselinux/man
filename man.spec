%define usecache 0
%define cache /var/cache/man

Summary: A set of documentation tools: man, apropos and whatis
Name: man
Version: 1.6f
Release: 29%{?dist}
License: GPLv2
Group: System Environment/Base
URL: http://primates.ximian.com/~flucifredi/man/
Source0: http://primates.ximian.com/~flucifredi/man/man-%{version}.tar.gz
Source2: makewhatis.crondaily
Source3: mess.ru
Source4: man-cmp.sh
Source5: man.lang
Patch1: man-1.5m2-confpath.patch
Patch2: man-1.5h1-make.patch
Patch6: man-1.5m2-apropos.patch
Patch10: man-1.6f-i18n_makewhatis.patch
Patch12: man-1.5m2-posix.patch
Patch18: man-1.6f-pipe_makewhatis.patch
Patch19: man-1.5p-sec.patch
Patch20: man-1.5p-xorg.patch
Patch21: man-1.6b-i18n_nroff.patch
Patch22: man-1.6b-man-pages.patch
Patch24: man-1.6c-disp.patch
Patch25: man-1.6f-dashes.patch
Patch26: man-1.6d-updates.patch
Patch27: man-1.6e-chmod.patch
Patch28: man-1.6f-i18n_makewhatis_2.patch
Patch29: man-1.6f-fr_translation.patch
Patch30: man-1.6f-loc.patch
Patch31: man-1.6f-tty.patch
Patch32: man-1.6f-dashes2.patch
Patch33: man-1.6f-star.patch
Patch34: man-1.6f-lang_C.patch
Patch35: man-1.6f-makewhatis_whis.patch
# add the option:
# -U: update database with pages added since last makewhatis run
# fix the description of option "-u"
Patch36: man-1.6f-makewhatis_update.patch
Patch37: man-1.6f-makewhatis_perf.patch
Patch38: man-1.6f-makewhatis_use.patch
Patch39: man-1.6f-man2html-suffixes.patch
# 542852 -  'man cut cut' throws an error
Patch40: man-1.6f-diff.patch
Patch41: man-1.6f-override_dir.patch
Patch42: man-1.6f-makewhatis_vari.patch
# fix: 607540 - man-debuginfo incomplete
Patch43: man-1.6f-debuginfo.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: coreutils
Requires: less, groff >= 1.18, nroff-i18n, findutils, mktemp >= 1.5-2.1.5x
Requires: bzip2, gzip, rpm, lzma
BuildRequires: less, groff

%description
The man package includes three tools for finding information and/or
documentation about your Linux system: man, apropos, and whatis. The
man system formats and displays on-line manual pages about commands or
functions on your system. Apropos searches the whatis database
(containing short descriptions of system commands) for a string.
Whatis searches its own database for a complete word.

The man package should be installed on your system because it is the
primary way to find documentation on a Linux system.

%prep
%setup -q
%patch1 -p1 -b .confpath
%patch2 -p1 -b .make
%patch6 -p1 -b .apropos
%patch10 -p1 -b .i18n_makewhatis
%patch12 -p1 -b .posix
%patch18 -p1 -b .pipe
%patch19 -p1 -b .sec
%patch20 -p1 -b .xorg
%patch21 -p1 -b .i18n_nroff
%patch22 -p1 -b .up
%patch24 -p1 -b .disp
%patch25 -p1 -b .dash
%patch26 -p1 -b .upd
%patch27 -p1 -b .chmod
%patch28 -p1 -b .i18n_makewhatis2
%patch29 -p1 -b .fr
%patch30 -p1 -b .loc
%patch31 -p1 -b .tty
%patch32 -p1 -b .dash2
%patch33 -p1 -b .star
%patch34 -p1 -b .lang
%patch35 -p1 -b .whis
%patch36 -p1 -b .update
%patch37 -p1 -b .perf
%patch38 -p1 -b .use
%patch39 -p1 -b .suff
%patch40 -p1 -b .diff
%patch41 -p1 -b .overrides
%patch42 -p1 -b .vari
%patch43 -p1 -b .db

cp -f %{SOURCE3} msgs   # replace bad ru trans
cp -f %{SOURCE5} ./

for src in $(find msgs -type f -name 'mess.[a-z][a-z]'); do
   lang=$(echo ${src} | sed -r 's;.*([a-z]{2})$;\1;')
   if   [ ${lang} = ja ]; then charset=euc-jp
   elif [ ${lang} = ko ]; then charset=euc-kr
   elif [ ${lang} = ru ]; then charset=koi8-r
   elif [ ${lang} = da ]; then charset=iso-8859-1
   elif [ ${lang} = de ]; then charset=utf-8
   elif [ ${lang} = en ]; then charset=iso-8859-1
   elif [ ${lang} = es ]; then charset=iso-8859-1
   elif [ ${lang} = fi ]; then charset=iso-8859-1
   elif [ ${lang} = fr ]; then charset=iso-8859-1
   elif [ ${lang} = it ]; then charset=iso-8859-1
   elif [ ${lang} = pt ]; then charset=iso-8859-1
   elif [ ${lang} = nl ]; then charset=iso-8859-1
   elif [ ${lang} = cs ]; then charset=iso-8859-2
   elif [ ${lang} = hr ]; then charset=iso-8859-2
   elif [ ${lang} = pl ]; then charset=iso-8859-2
   elif [ ${lang} = ro ]; then charset=iso-8859-2
   elif [ ${lang} = sl ]; then charset=iso-8859-2
   elif [ ${lang} = bg ]; then charset=cp1251
   elif [ ${lang} = el ]; then charset=iso-8859-7
   else
      echo === LANGUAGE ${lang}: MUST SPECIFY CHARSET/ENCODING
      exit 1
   fi
   iconv -t utf-8 -f ${charset} -o ${src}.utf ${src} && mv ${src}.utf ${src}
done

%build
./configure -default  -confdir /etc +fhs +lang all 

find . -type f|xargs perl -pi -e 's,man\.conf \(5\),man.config (5),g'
for i in $(find man -name man.conf.man); do
   mv $i ${i%man.conf.man}man.config.5
done

# HACK: Make output default to using -c; otherwise it appears broken.
perl -pi -e "s/nroff /nroff -c /" conf_script

touch Makefile   # make sure Make thinks we ran configure

cat conf_script |sed -e "s|^s,@cmp@,.*|s,@cmp@,%{_libexecdir}/man-cmp.sh,|g" > conf_script.aux
mv conf_script.aux conf_script
chmod 755 conf_script

make CC="gcc $RPM_OPT_FLAGS"
%if %{usecache}
cat src/man.conf |sed -e "s,^NOCACHE,# NOCACHE,g" > man.conf
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/cron.daily
mkdir -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_sbindir}
make install PREFIX=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man5
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
mkdir -p $RPM_BUILD_ROOT/etc

for src in $(find man -type f -name '*.[1-9n]'); do
   lang=$(echo ${src} | sed -r 's;.*/([a-z]{2})/.*;\1;')
   page=$(basename ${src})
   sect=$(echo ${page} | sed -r 's;.*([1-9n])$;man\1;')
   dir=${RPM_BUILD_ROOT}%{_mandir}
   if   [ ${lang} = ja ]; then charset=euc-jp
   elif [ ${lang} = ko ]; then charset=euc-kr
   elif [ ${lang} = da ]; then charset=iso-8859-1
   elif [ ${lang} = de ]; then charset=iso-8859-1
   elif [ ${lang} = en ]; then charset=iso-8859-1
   elif [ ${lang} = es ]; then charset=iso-8859-1
   elif [ ${lang} = fi ]; then charset=iso-8859-1
   elif [ ${lang} = fr ]; then charset=iso-8859-1
   elif [ ${lang} = it ]; then charset=iso-8859-1
   elif [ ${lang} = pt ]; then charset=iso-8859-1
   elif [ ${lang} = nl ]; then charset=iso-8859-1
   elif [ ${lang} = cs ]; then charset=iso-8859-2
   elif [ ${lang} = hr ]; then charset=iso-8859-2
   elif [ ${lang} = pl ]; then charset=iso-8859-2
   elif [ ${lang} = ro ]; then charset=iso-8859-2
   elif [ ${lang} = sl ]; then charset=iso-8859-2
   elif [ ${lang} = bg ]; then charset=cp1251
   elif [ ${lang} = el ]; then charset=iso-8859-7
   else
      echo === LANGUAGE ${lang}: MUST SPECIFY CHARSET/ENCODING
      exit 1
   fi
   mkdir -p ${dir}/${lang}/${sect}
   iconv -t utf-8 -f ${charset} -o ${dir}/${lang}/${sect}/${page} ${src}

   # ensure POSIX/C locale only has ASCII subset and no latin-1 
   if [ ${lang} = en ]; then
      mkdir -p ${dir}/${sect}
      iconv -t ascii//translit -f ${charset} -o ${dir}/${sect}/${page} ${src}
   fi
done

install -m 644 src/man.conf $RPM_BUILD_ROOT/etc/man.config

install -m755 %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.daily/makewhatis.cron

mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}
install -m755 %{SOURCE4} $RPM_BUILD_ROOT/%{_libexecdir}/man-cmp.sh

mkdir -p $RPM_BUILD_ROOT/%{cache}
touch $RPM_BUILD_ROOT/%{cache}/whatis

mkdir -p $RPM_BUILD_ROOT/%{cache}/local
mkdir -p $RPM_BUILD_ROOT/%{cache}/X11R6
for i in 1 2 3 4 5 6 7 8 9 n; do
        mkdir -p $RPM_BUILD_ROOT/%{cache}/cat$i
        mkdir -p $RPM_BUILD_ROOT/%{cache}/local/cat$i
        mkdir -p $RPM_BUILD_ROOT/%{cache}/X11R6/cat$i
done


# added man2html stuff
cd man2html
make install DESTDIR=$RPM_BUILD_ROOT

for src in $(find $RPM_BUILD_ROOT%{_mandir} -type f -name '*.[1-9n]'); do
   gzip -9 ${src}
done

# symlinks for manpath
( cd $RPM_BUILD_ROOT
  ln -s man .%{_bindir}/manpath
  ln -s man.1.gz .%{_mandir}/man1/manpath.1.gz
)

# move locale files to proper directories
for i in `ls $RPM_BUILD_ROOT%{_datadir}/locale/`; do
  mkdir  $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES
  mv $RPM_BUILD_ROOT%{_datadir}/locale/$i/man $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/man
done

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_bindir}/man2dvi
rm -rf $RPM_BUILD_ROOT%{_prefix}/etc

%preun
[ $1 = 0 ] || exit 0
rm -f %{cache}/cat[123456789n]/* 2>/dev/null || :
rm -f %{cache}/local/cat[123456789n]/* 2>/dev/null || :
rm -f %{cache}/X11R6/cat[123456789n]/* 2>/dev/null || :


%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING
%{_sysconfdir}/cron.daily/makewhatis.cron
%config(noreplace) %{_sysconfdir}/man.config
%if %{usecache}
%attr(2755,root,man)    %{_bindir}/man
%else
%attr(0755,root,root)   %{_bindir}/man
%endif
%{_bindir}/manpath
%{_bindir}/apropos
%{_bindir}/whatis
%{_bindir}/man2html
%{_sbindir}/makewhatis
%{_libexecdir}/man-cmp.sh
%{_mandir}/man5/man.config.5*
%{_mandir}/man1/*
%{_mandir}/man8/makewhatis.8*
%ghost %{cache}/whatis
%attr(0755,root,root)   %dir %{cache}
%attr(0755,root,man)    %dir %{cache}/cat[123456789n]
%attr(0755,root,man)    %dir %{cache}/local
%attr(0755,root,man)    %dir %{cache}/local/cat[123456789n]
%attr(0755,root,man)    %dir %{cache}/X11R6
%attr(0755,root,man)    %dir %{cache}/X11R6/cat[123456789n]


%changelog
* Thu Jun 24 2010 Ivana Hutarova Varekova <varekova at redhat.com> - 1.6f-29
- Resolves: #607540
  man-debuginfo incomplete

* Tue Feb 16 2010 Ivana Hutarova Varekova <varekova at redhat.com> - 1.6f-28
- Resolves: #543948
  fix attr stuf

* Tue Feb 16 2010 Ivana Hutarova Varekova <varekova at redhat.com> - 1.6f-27
- Resolves: #543948
  add patches description and documentation

* Mon Feb  1 2010 Ivana Hutarova Varekova <varekova at redhat.com> - 1.6f-26
- Resolves: #560587
  fix the variable name bug in makewhatis script

* Tue Jan 26 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.6f-25
- Resolves: #558716
  man needs to go through additional subpaths

* Tue Dec  1 2009 Ivana Varekova <varekova@redhat.com> - 1.6f-24
- fix the problem: #542852 -  'man cut cut' throws an error

* Mon Oct 12 2009 Ivana Varekova <varekova@redhat.com> - 1.6f-23
- fix man2html to enable to use longer suffixes (#526112)

* Tue Aug 11 2009 Ivana Varekova <varekova@redhat.com> - 1.6f-22
- fix makewhatis format bug (#513553)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6f-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 21 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6f-20
- Don't remove cache and whatis database on updates
- Ghost whatis database

* Tue Apr 21 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6f-19
- The daily cron job is not a configuration file

* Sun Apr 19 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.6f-18
- Get rid of slow weekly updates
- Make daily updates reliable
- Speed up initial indexation

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6f-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Ivana Varekova <varekova@redhat.com> - 1.6f-16
- Resolves: #481650
  makewhat fails if /usr is read-only

* Thu Feb 12 2009 Ivana Varekova <varekova@redhat.com> - 1.6f-15
- Resolves: #485014
  Do not use .mo suffix for gencat message catalogs

* Fri Nov 21 2008 Ivana Varekova <varekova@redhat.com> - 1.6f-14
- Resolves: #456162
  locale settings problem

* Thu Nov 20 2008 Ivana Varekova <varekova@redhat.com> - 1.6f-13
- Resolves: #458042
  makewhatis error on file name with shell meta-characters

* Tue Nov 18 2008 Ivana Varekova <varekova@redhat.com> - 1.6f-12
- Resolves: #471784
  makewhatis problem with man-pages with dash in its name

* Tue Sep 16 2008 Ivana Varekova <varekova@redhat.com> - 1.6f-11
- Resolves: #460765
  remove makewhatis patch which adds data from rpm database 
  

* Fri Sep 12 2008 Ivana Varekova <varekova@redhat.com> - 1.6f-10
- Resolves: #461775
  man needs lzma

* Mon Sep  1 2008 Ivana Varekova <varekova@redhat.com> - 1.6f-9
- update patches

* Mon Jun  9 2008 Ivana Varekova <varekova@redhat.com> - 1.6f-8
- Resolves: #449272 
  Latest man behaves very strange for non-existing man pages
- Resolves: #449275
  Unowned directories where man package provides content for

* Mon Jun  2 2008 Ivana Varekova <varekova@redhat.com> - 1.6f-7
- Resolves: #448049
  Error messages will exhibit when quit from mount man page

* Wed May 14 2008 Ivana Varekova <varekova@redhat.com> - 1.6f-6
- Resolves: #439314
  move locale files
- spec file cleanup

* Wed Apr 16 2008 Ivana Varekova <varekova@redhat.com> - 1.6f -5
- Resolves: #442192
  fix fr translation

* Mon Apr  7 2008 Ivana Varekova <varekova@redhat.com> - 1.6f-4
- Resolves: #441074
  double UTF-8 conversion in German messages

* Tue Mar 25 2008 Ivana Varekova <varekova@redhat.com> - 1.6f-3
- Resolves 438742: 
  makewhatis patch problem

* Fri Mar 21 2008 Ivana Varekova <varekova@redhat.com> - 1.6f-2
- remove diffutils dependency (#431352)
  thanks Ville Skyttä

* Fri Mar 14 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 1.6f-1
- new version

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.6e-4
- Autorebuild for GCC 4.3

* Mon Mar 12 2007 Ivana Varekova <varekova@redhat.com> - 1.6e-3
- incorporate the package review feedback

* Tue Jan  9 2007 Ivana Varekova <varekova@redhat.com> - 1.6e-2
- Resolves: 221868
  man use incorrect groff option
- spec file cleanup

* Mon Dec 11 2006 Ivana Varekova <varekova@redhat.com> - 1.6e-1
- update to 1.6e

* Thu Oct 26 2006 Ivana Varekova <varekova@redhat.com> - 1.6d-3
- add MAKEWHATISDBUPDATES option (bug 210501)

* Tue Oct 24 2006 Ivana Varekova <varekova@redhat.com> - 1.6d-2
- makewhatis overlooks man pages with two dashes in SH line
  (bug 208216)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.6d-1.1
- rebuild

* Thu Jun 22 2006 Ivana Varekova <varekova@redhat.com> - 1.6d-1
- update to 1.6d

* Thu Jun 22 2006 Ivana Varekova <varekova@redhat.com> - 1.6c-4
- add directories to file list (bug 192995)

* Mon May 01 2006 Ivana Varekova <varekova@redhat.com> - 1.6c-3
- fix man displaying problem (bug 190287) - thanks JW

* Mon Feb 27 2006 Ivana Varekova <varekova@redhat.com> - 1.6c-2
- fix the encoding of the Bulgarian translation  

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.6c-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.6c-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Florian La Roche <laroche@redhat.com>
- 1.6c

* Tue Dec 13 2005 Ivana Varekova <varekova@redhat.com> 1.6b-2
- makewhatis change - add info about packages (bug 175595)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Ivana Varekova <varekova@redhat.com> 1.6b-1
- update to 1.6b

* Mon Oct 31 2005 Ivana Varekova <varekova@redhat.com> 1.5p-7
- add ?x sections to MANSECT variable (bug 172002) 

* Tue May 17 2005 Ivana Varekova <varekova@redhat.com> 1.5p-6
- change patch 18 (less hard solution) and 
  patch 13 (don't change exit number in one case)

* Wed Apr 13 2005 Ivana Varekova <varekova@redhat.com> 1.5p-5
- fix bug 146849 - makewhatis from cron produce error message
  "zcat: stdout: Broken pipe" (patch 18)
- fix makewhatis problem with sections (patch 19)
- delete strips

* Thu Mar 29 2005 Ivana Varekova <varekova@redhat.com> 1.5p-4
- fix bug 140732 in man pages and the rest of bug 140207 change 
   in man-pages again (patch 17)

* Thu Mar 22 2005 Ivana Varekova <varekova@redhat.com> 1.5p-3
- fix bug 142673 - bugs in man2html

* Thu Mar 16 2005 Ivana Varekova <varekova@redhat.com> 1.5p-2
- fix bug 140178 - correct one typo 
- fix bug 140202 - problem with makewhatis exit (patch 13)
- fix bug 140207 - problem with makewhatis -u  (patch 14)
  the fixed version update information about man-pages which 
  are less then one day old (it is used in day update)
  (man-pages may be fixed)
- fix bug 140729 - makewhatis removed to /usr/sbin  
- fix bug 146631 - two-part locale dir-name is support (patch 15)
- changed makewhatis version

* Mon Mar  7 2005 Ivana Varekova <varekova@redhat.com> 1.5p-1
- rebuilt new version #147716

* Fri Mar  4 2005 Ivana Varekova <varekova@redhat.com> 1.5m2-13
- rebuilt 

* Mon Feb 14 2005 Adrian Havill <havill@redhat.com>
- rebuilt

* Tue Oct 13 2004 Adrian Havill <havill@redhat.com> 1.5m2-9
- make sure we touch Makefile timestamp so make doesn't get
  confused and think we haven't run configure
- replace russian messages (#134387) Thanks to Leonid Kanter

* Sun Aug 1 2004 Alan Cox <alan@redhat.com>
- Fix requirements (#126601)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 31 2004 Adrian Havill <havill@redhat.com> 1.5m2-6
- reorder MANSECT so that normal pages (with translations) take
  precedence over the English-only POSIX pages (#119554)

* Wed Mar 24 2004 Adrian Havill <havill@redhat.com> 1.5m2-5
- force use of /usr/bin/gunzip and not /bin/gunzip for compatibility
  with rescue environments (#118087)
- add POSIX sections to MANSECT in man.config, giving preference to the
  POSIX pages over the non-POSIX

* Fri Mar 12 2004 Adrian Havill <havill@redhat.com> 1.5m2-4
- direct nroff stderr to /dev/null so no broken pipe err msgs appear
  when the user quits an error page prior to the full display (#117463)
- removed bogus whatis search-n-destroy trigger (#117961)
- don't complain about no lang resource when lang is C/POSIX (#108934)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 09 2004 Adrian Havill <havill@redhat.com> 1.5m2-2
- add all locale man pages
- convert all msgs and manpages to utf-8
- downconvert via transliteration C locale man pages just in case
- patch #3, #8, #10, #17, #29, #31 no longer needed-- made it upstream
- patch #9, #14 and #19 now superfluous-- strs already termed and len checked
- disable patch #22: defer cat creation to existence of dir, not conf directive
- patch #32 mostly merged upstream. Keep the "-a" in grep though so all
  locales' grep see man pages as text not binary (patch 37)
- iconv patch no longer needed now that utf-8-to-legacy conversion is not
  needed
- patch #52 and #53 not needed: CJK all point to nroff instead of groff, let
  the nroff script decide, based on the charset of the environment and/or the
  charset of the man page, as to what parameters to pass to groff (and
  whether iconv preprocessing is necessary)
- the string "NROFF_OLD_CHARSET", if present in the man.config for the NROFF
  path, will now be replaced by the old character set so that nroff can figure
  out what the character set/encoding is
- fix man to reflect status codes returned by forked child processes (#115204)
- lots of makewhatis changes: re-add custom rh client stuff (/usr/bin vs
  /usr/sbin), -o option, /var/cache/man, utf-8 verification, convert the
  encoding spaghetti in the makewhatis awk script to UTF-8, identify languages
  in comments

* Thu Oct 09 2003 Adrian Havill <havill@redhat.com> 1.5k-12
- restore russian locale (#81929)
- force utf locale with jnroff (#105764)
- don't let awk in makewhatis scan files that aren't man pages (#105594)

* Wed Oct 01 2003 Adrian Havill <havill@redhat.com> 1.5k-11
- Use UTF-8 in makewhatis when searching for non-English versions of the
  phrase "NAME" in man pages
- add "-o" option to makeis to specify an alternate whatis db location
- move makewhatis from /sbin to /usr/bin, chmod o+x it as the whatis db is
  writable only by root anyway

* Wed Aug 20 2003 Adrian Havill <havill@redhat.com> 1.5k-10
- added auto-detect for utf8 and conversion to allow gripes() and others
  to correctly output to some charsets (#88605)

* Fri Aug 08 2003 Adrian Havill <havill@redhat.com> 1.5k-9
- cleaned up apropos script bugs (#97006)
- merged all apropos changes into one cleaner patch
- fix the search/replace for man.conf

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 22 2003 Jeremy Katz <katzj@redhat.com> 1.5k-7
- fix build with gcc 3.3

* Mon Feb 10 2003 Adrian Havill <havill@redhat.com> 1.5k-6
- added patch for korean (#83934)

* Thu Feb 06 2003 Adrian Havill <havill@redhat.com> 1.5k-5
- marked man.config as noreplace config (#82088)
- moved man.config from /usr/share to /etc even though +fhs (#81964)
- removed bad argcat patch which made bogus grep queries (#82684)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Adrian Havill <havill@redhat.com> 1.5k-2
- bump version from j to k
- adjust patches to reflect upstream integration

* Wed Jan  8 2003 Adrian Havill <havill@redhat.com> 1.5j-16
- require groff 1.18 because prev vers don't have -c getopt (#77847)
- added /usr/local/share/man to MANPATH (#65467)

* Mon Jan  6 2003 Adrian Havill <havill@redhat.com> 1.5j-14
- don't run trojan sh cmd that have unsafe chars munged (#79289)
- made apropos command more robust (#62606)

* Tue Dec 10 2002 Joe Orton <jorton@redhat.com> 1.5j-13
- include makewhatis.8 (#65511)

* Fri Nov 22 2002 Tim Powers <timp@redhat.com>
- remove unpackaged files from the buildroot

* Tue Sep 03 2002 Karsten Hopp <karsten@redhat.de> 1.5j-11
- fix segfault when running  'man --' (#73212)

* Mon Sep  2 2002 Bill Nottingham <notting@redhat.com> 1.5j-10
- use nroff -c

* Fri Jul 12 2002 Phil Knirsch <pknirsch@redhat.com> 1.5j-9
- Changed output of groff to latin1 instead of utf8 as utf8 seems to be broken
  ATM.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.5j-8
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com> 1.5j-7
- automated rebuild

* Mon Mar 25 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.5j-6
- Fix bugs #60676 and #61105
- Add /usr/local/man and /usr/X11R6/man to makewhatis default paths


* Tue Feb 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.5j-5
- Fix up filename quoting in makewhatis (#60289)

* Mon Feb 25 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.5j-3
- Fix bugs #60131, #60088
- Don't send makewhatis output to /dev/tty (#60285)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Nov 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5j-1
- Update to 1.5j

* Fri Aug 31 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.5i2-6
- set LC_CTYPE, not just LC_MESSAGES. That way, the messages 
  requested can also be displayed (#52978)

* Mon Aug 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i2-5
- Make sure the trigger exits cleanly (#51940)

* Wed Jul 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i2-4
- Don't create warnings on fresh installs

* Tue Jul 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i2-3
- Restore /var/cache/man directories even if we've built without usecache.
  This allows users to enable catman caching manually (#48762) and shuts
  up tmpwatch (#47784 and its 1000 duplicates)

* Wed Jul  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i2-2
- Fix makewhatis interoperability with gawk 3.1.x (#46405)
- Fix initial creation of whatis database if makewhatis is run with "-u"
  even then (e.g. by cron) (#45646)
- Fix #45827
- Require current mktemp (#43134)
- Fix #42915
- Fix paths on old distributions (#42031)

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i2-1
- 1.5i2

* Thu Jun 07 2001 Harald Hoyer <harald@redhat.de> 1.5i-9
- Some fixes for secure pathnames
- remove cache directories
- remove sgid
- fixed man.1 to refer to man.config(5)
- fixed makewhatis

* Thu May 31 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i-8
- Some fixes to legacy path support

* Mon May 28 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i-7
- Fix up another buffer overrun (#42450)
- Add "`" and "$(" to the list of illegal filename parts in makewhatis (#42450)
- Add a define toggle to build 5.x and 6.x errata correctly (#42031, #42192)
- 
* Thu May 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i-6
- Fix up potential GID man -> root exploit (#41805)

* Thu May 17 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i-5
- Fix up support for UTF-8 locales (#39139)

* Sun May 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i-4
- More workarounds for "detecting" stuff that isn't in the build roots

* Sun May  6 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i-3
- Fix up makewhatis (#39217)

* Mon Apr 30 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i-2
- break the configure script. We want man to use less even though it
  can't be found at build time.

* Tue Apr 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5i-1
- 1.5i (Fixes #23258, #31805, #33276)
- Fix apropos and whatis for pages that contain non-ascii characters (#21619)
- Look for legacy whatis databases in $manpath (#33897)

* Sun Feb  4 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Require findutils for makewhatis (Bug #25615)

* Fri Jan 19 2001 Jeff Johnson <jbj@redhat.com>
- Use PreReq: not Requires(post,preun).

* Mon Jan  8 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- s/Prereq/Requires(post,preun)/ (this should fix #22775)

* Fri Dec 29 2000 Bill Nottngham <notting@redhat.com>
- tweak prereqs

* Mon Dec 18 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese patches.

* Mon Dec 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Requires(preun,post) fileutils

* Thu Oct 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix yet another security problem (MANSECT overrun), Bug #19351

* Thu Oct 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix trailing garbage when a man page doesn't end with a newline (Bug #9026)
- Look for files in other man directories if the first match isn't
  accessible (Bug #10254)

* Mon Oct  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Move whatis database to {cache}/whatis to allow read-only /usr
  filesystems (Bug #18383)
- Don't use predictable filenames in makewhatis (not reported, spotted while
  fixing 18383)

* Wed Oct  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add internationalization support, based on patch from noa@noa.tm (Bug #7680)

* Wed Aug 23 2000 Tim Powers <timp@redhat.com>
- fix bad man path for makewhatis in bug #16754

* Tue Aug 15 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up .so handling in some odd cases (Bug #16171)

* Fri Aug  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up the fix for #14278, this fixes #11621 as well.

* Thu Jul 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Get rid of random <AD>s (Bug #14278, thanks, Tim)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 30 2000 Bill Nottingham <notting@redhat.com>
- makewhatis makes predicatable filenames in /tmp. Bad.

* Mon Jun 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- gzip the man pages manually - since file doesn't recognize them as
  man pages, the build root policy doesn't do it (Bug #12015)

* Tue May 16 2000 Preston Brown <pbrown@redhat.com>
- default man path is now {_mandir}.  /usr/man maintained for compat.
- remove +sgid option to allow builds as a normal user.  SPEC file maintains
  proper permissions.

* Wed Mar  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add kerberos man paths to man.config (Bug #11168 + extra fixes)

* Tue Feb 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.5h1 - this has a better fix for the security problems.
- remove manpath patch (now in base)
- remove loop patch (now in base)

* Mon Feb 28 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix security problems related to buffer overruns caused by oversized
  enviroment variables

* Thu Feb  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- deal with rpm gziping man pages
- fix file locking (Bug #8947)

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip man2html

* Fri Sep 10 1999 Cristian Gafton <gafton@redhat.com>
- revert to latin1 instead of ascii

* Wed Jun 16 1999 Cristian Gafton <gafton@redhat.com>
- fixed man2html loop on terminfo.5 (patrch from the author; #3316)

* Mon May 10 1999 Michael K. Johnson <johnsonm@redhat.com>
- fixed #2532 by adding /usr/local/sbin as a MANPATH_MAP

* Fri Apr 09 1999 Michael K. Johnson <johnsonm@redhat.com>
- cron.weekly rebuilds, cron.daily updates in minimal time

* Fri Apr 09 1999 Preston Brown <pbrown@redhat.com>
- man 1.5g bugfix release

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Feb 18 1999 Jeff Johnson <jbj@redhat.com>
- add manpath symlinks (#1138).

* Fri Feb 12 1999 Michael Maher <mike@redhat.com>
- fixed bug #792
- added man2html files

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0
- upgraded to 1.5e
- properly buildrooted

* Thu Aug 13 1998 Jeff Johnson <jbj@redhat.com>
- enable fsstnd organization
- change /var/catman/X11 to X11R6
- post/preun to clean up cat litter

* Tue Jun 02 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Tue Jun 02 1998 Erik Troan <ewt@redhat.com>
- you can't do free(malloc(10) + 4) <sigh>

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.5d

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- updated to 1.5a

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- uses a build root

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- updated to man-1.4j, which fixes some security problems; release 1 is
  for RH 4.2, release 2 is for glibc
 
* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Mar 25 1997 Erik Troan <ewt@redhat.com>
- Added /usr/lib/perl5/man to default manpath
