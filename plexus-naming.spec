# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'

%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}

%define section     free

%define namedversion 1.0-alpha-3

%define parent plexus
%define subname naming

Name:           plexus-naming
Version:        1.0
Release:        %mkrel 0.a3.1.0.1
Epoch:          0
Summary:        Plexus Naming Component
License:        Apache Software License 2.0
Group:          Development/Java
URL:            http://plexus.codehaus.org/
Source0:        %{name}-%{namedversion}.tar.gz
# svn export http://svn.codehaus.org/plexus/plexus-components/tags/plexus-registry-1.0-alpha-3/
Source1:        plexus-naming-1.0-build.xml
Source2:        plexus-naming-settings.xml
Source3:        plexus-naming-1.0-jpp-depmap.xml
Source4:        plexus-naming-components.xml
Patch0:         plexus-naming-1.0-pom.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRequires:  jpackage-utils >= 0:1.7.3
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  junit
BuildRequires:  hsqldb
BuildRequires:  jakarta-commons-logging
%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4-10jpp
BuildRequires:  maven2-common-poms
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-release
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-surefire
BuildRequires:  plexus-maven-plugin
%endif
BuildRequires:  directory-naming
BuildRequires:  avalon-framework
BuildRequires:  geronimo-javamail-1.3.1-api
BuildRequires:  jakarta-commons-collections
BuildRequires:  jakarta-commons-dbcp
BuildRequires:  jakarta-commons-digester
BuildRequires:  jakarta-commons-pool
BuildRequires:  plexus-cdc
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-component-api 
BuildRequires:  plexus-containers-container-default 
BuildRequires:  plexus-utils 

%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif

Requires:  directory-naming
Requires:  jakarta-commons-pool
Requires:  plexus-classworlds
Requires:  plexus-container-default 
Requires:  plexus-utils 
Requires(post):    jpackage-utils >= 0:1.7.3
Requires(postun):  jpackage-utils >= 0:1.7.3

%description
The Plexus project seeks to create end-to-end developer tools for 
writing applications. At the core is the container, which can be 
embedded or for a full scale application server. There are many 
reusable components for hibernate, form processing, jndi, i18n, 
velocity, etc. Plexus also includes an application server which 
is like a J2EE application server, without all the baggage.


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}
cp %{SOURCE1} build.xml
cp %{SOURCE2} settings.xml
mkdir -p target/classes/META-INF/plexus/
cp %{SOURCE4} target/classes/META-INF/plexus/components.xml
%patch0 -b .sav0

%build
sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" settings.xml

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

%if %{with_maven}
    mvn-jpp \
        -e \
        -s $(pwd)/settings.xml \
        -Dmaven.test.failure.ignore=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE3} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%else
export CLASSPATH=$(build-classpath \
commons-collections \
commons-logging \
commons-dbcp \
commons-pool \
directory-naming/naming-config \
directory-naming/naming-core \
directory-naming/naming-factory \
directory-naming/naming-java \
hsqldb \
plexus/classworlds \
plexus/containers-component-api \
plexus/containers-container-default \
plexus/utils \
)
CLASSPATH=$CLASSPATH:target/classes:target/test-classes
%{ant} -Dbuild.sysclasspath=only jar javadoc
%endif

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 target/%{name}-%{namedversion}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{parent}/%{subname}-%{version}.jar
%add_to_maven_depmap org.codehaus.plexus %{name} %{version} JPP/%{parent} %{subname}

(cd $RPM_BUILD_ROOT%{_javadir}/plexus && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%{_javadir}/%{parent}/*
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
